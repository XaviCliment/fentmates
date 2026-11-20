# Genera t1-fitxa-exercicis.tex i t1-fitxa-solucions.tex (1r Batxillerat CCSS, Unitat 1: Nombres reals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Bilingüe: T(valencià, castellà); genera-es.py l'executa amb FM_LANG=es i escriu els -es.tex.
# Parteix de la fitxa de la unitat 1 de 1r Batx MI (_eines/fonts-latex/1batx-mi-t1), amb les seccions dels apunts de CCSS
# (sense entorns ni diferència d'intervals, i amb més exercicis de forma exponencial, índex comú i problemes de context).
# Les solucions es calculen ací amb fraccions exactes (decimals periòdics, intervals, desigualtats amb valor absolut) i
# CHK (al final) les compara amb els valors escrits; les de radicals i logaritmes es comproven numèricament (cn).
# Dins de les fórmules, «, » (coma i espai) separa elements (intervals, coordenades) i «2,45» és un decimal (icomma).
# Ús: python3 genera.py && python3 genera-es.py, i pdflatex (dues vegades) dels quatre .tex
import os, re, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va
INF = float('inf')
r2, r3, r5, r6 = math.sqrt(2), math.sqrt(3), math.sqrt(5), math.sqrt(6)
def rt(x, n): return math.copysign(abs(x) ** (1 / n), x)
lg = math.log10

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def R(t): return r'$\res{' + t + '}$'
def RR(pre, t): return '$' + pre + r'\res{' + t + '}$'
def tn(x):
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    return ('-' if x < 0 else '') + r'\frac{%d}{%d}' % (abs(x.numerator), x.denominator)

CHK = []
def ck(x, y):
    CHK.append((x == y, (x, y))); return x
def cn(x, y, eps=1e-9):
    """comprovació numèrica (x i y poden ser llistes)"""
    if isinstance(x, (list, tuple)):
        for a, b in zip(x, y): cn(a, b, eps)
        assert len(x) == len(y), (x, y)
        return
    CHK.append((abs(x - y) < eps * max(1, abs(y)), (x, y)))

# ---------- decimals periòdics ----------
def per(ent, ante, peri):
    """valor exacte de ent,ante(peri)"""
    sg = -1 if ent.startswith('-') else 1
    ent = ent.lstrip('-')
    if not peri: return sg * F(int(ent + ante), 10 ** len(ante))
    full, part = int(ent + ante + peri), int(ent + ante)
    return sg * F(full - part, int('9' * len(peri) + '0' * len(ante)))

# ---------- intervals: (a, tancat_a, b, tancat_b) ----------
def norm(L):
    L = sorted([I for I in L if I[0] < I[2] or (I[0] == I[2] and I[1] and I[3])], key=lambda I: (I[0], not I[1]))
    out = []
    for a, ac, b, bc in L:
        if out and (a < out[-1][2] or (a == out[-1][2] and (out[-1][3] or ac))):
            pa, pac, pb, pbc = out[-1]
            if b > pb: out[-1] = (pa, pac, b, bc)
            elif b == pb: out[-1] = (pa, pac, pb, pbc or bc)
        else: out.append((a, ac, b, bc))
    return out
def cap(S, T_):
    r = []
    for a, ac, b, bc in S:
        for c, cc, d, dc in T_:
            r.append((max(a, c), ac if a > c else cc if c > a else ac and cc, min(b, d), bc if b < d else dc if d < b else bc and dc))
    return norm(r)
def cup(S, T_): return norm(S + T_)
def compl(S):
    r, a, ac = [], -INF, False
    for c, cc, d, dc in norm(S):
        r.append((a, ac, c, not cc)); a, ac = d, not dc
    r.append((a, ac, INF, False)); return norm(r)
def P(s):
    """'[-3,2)U(5,inf)' -> conjunt"""
    out = []
    for p in s.split('U'):
        m = re.match(r'^([\[\(])([^,]+),([^,]+)([\]\)])$', p.strip())
        def num(t): return -INF if t == '-inf' else INF if t == 'inf' else F(t)
        out.append((num(m.group(2)), m.group(1) == '[', num(m.group(3)), m.group(4) == ']'))
    return norm(out)
RE = P('(-inf,inf)')
def ivt(I):
    a, ac, b, bc = I
    if a == b: return r'\{%s\}' % tn(a)
    ta = r'-\infty' if a == -INF else tn(a)
    tb = r'+\infty' if b == INF else tn(b)
    return ('[' if ac else '(') + ta + ', ' + tb + (']' if bc else ')')
def st(S):
    S = norm(S)
    if not S: return r'\varnothing'
    if S == RE: return r'\mathbb R'
    return r'\cup'.join(ivt(I) for I in S)
def absI(a, b, op, r):
    """conjunt solució de |a·x+b| op r (a != 0)"""
    a, b, r = F(a), F(b), F(r)
    if r < 0 or (r == 0 and op in '<>'):
        if r < 0: return [] if op in ('<', '<=') else RE
        return [] if op == '<' else compl([(-b / a, True, -b / a, True)])
    p, q = sorted([(-r - b) / a, (r - b) / a])
    if op == '<': return norm([(p, False, q, False)])
    if op == '<=': return norm([(p, True, q, True)])
    if op == '>': return compl([(p, True, q, True)])
    return compl([(p, False, q, False)])

def recta(S, lo=None, hi=None):
    """dibuix TikZ d'un conjunt de la recta real"""
    S = norm(S)
    pts = [float(v) for I in S for v in (I[0], I[2]) if abs(v) != INF] or [0]
    if lo is None: lo = math.floor(min(pts)) - 1
    if hi is None: hi = math.ceil(max(pts)) + 1
    if hi - lo < 6: c = (hi + lo) / 2; lo, hi = math.floor(c - 3), math.ceil(c + 3)
    step = 2 if hi - lo > 14 else 1
    sc = min(0.42, 7.2 / (hi - lo + 1.4))
    o = [r'\begin{tikzpicture}[x=%.3fcm,baseline=-3pt]' % sc,
         r'\draw[-latex,muted] (%g,0)--(%g,0);' % (lo - 0.6, hi + 0.7)]
    v = math.ceil(lo / step) * step
    while v <= hi:
        o.append(r'\draw[muted] (%d,0.1)--(%d,-0.1) node[below=-1pt,font=\scriptsize,text=muted]{$%d$};' % (v, v, v)); v += step
    for a, ac, b, bc in S:
        xa = lo - 0.45 if a == -INF else float(a); xb = hi + 0.45 if b == INF else float(b)
        if a != b: o.append(r'\draw[accent,line width=2.6pt] (%g,0)--(%g,0);' % (xa, xb))
        if a == -INF: o.append(r'\fill[accent] (%g,0)--(%g,0.17)--(%g,-0.17)--cycle;' % (xa - 0.3, xa + 0.1, xa + 0.1))
        if b == INF: o.append(r'\fill[accent] (%g,0)--(%g,0.17)--(%g,-0.17)--cycle;' % (xb + 0.3, xb - 0.1, xb - 0.1))
        for x, c, lab in ((a, ac, True), (b, bc, a != b)):
            if abs(x) == INF or not lab: continue
            o.append((r'\fill[accent] (%g,0) circle (2.3pt);' if c else r'\filldraw[fill=white,draw=accent,line width=1.1pt] (%g,0) circle (2.3pt);') % float(x))
            if F(x).denominator != 1: o.append(r'\node[above=1pt,font=\scriptsize,text=accent] at (%g,0) {$%s$};' % (float(x), tn(x)))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def RI(s, lo=None, hi=None):
    """solució d'interval: el conjunt emmarcat i la recta"""
    S = P(s) if isinstance(s, str) else s
    if not norm(S): return R(r'\varnothing')
    return R(st(S)) + r'\\[2pt]' + recta(S, lo, hi)
def d3(x, k=3): return ('%.*f' % (k, x)).replace('.', ',')

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Nombres reals
gen = [per('0', '1', '6'), per('2', '', '09'), per('-1', '2', '45'), per('3', '', '12'), per('0', '4', '5'), per('2', '45', '')]
ck(gen, [F(1, 6), F(23, 11), F(-137, 110), F(103, 33), F(41, 90), F(49, 20)])
e4 = [per('2', '', '7') + per('3', '', '4') - per('1', '', '1'),
      per('1', '', '8') + per('0', '', '1'),
      per('0', '', '3') * per('1', '', '5') - per('0', '1', '6'),
      (per('1', '', '2') + F(1, 2)) * per('0', '', '18')]
ck(e4, [F(46, 9), F(2), F(19, 54), F(31, 99)])
S.append((T("Nombres reals", "Números reales"), [
 (1, T(r"Indica el menor dels conjunts numèrics ($\mathbb N$, $\mathbb Z$, $\mathbb Q$ o $\mathbb I$) als quals pertanyen els nombres següents:",
       r"Indica el menor de los conjuntos numéricos ($\mathbb N$, $\mathbb Z$, $\mathbb Q$ o $\mathbb I$) a los que pertenecen los números siguientes:")
     + tasks(5, [r"$\sqrt5$", r"$2$", r"$-3$", r"$24/6$", r"$2,45$", r"$-1,33$", r"$2,3\widehat{45}$", r"$\pi$", r"$5/12$", r"$\sqrt{\frac94}$"]),
     tasks(5, [R(r"\mathbb I"), R(r"\mathbb N"), R(r"\mathbb Z"), R(r"4\in\mathbb N"), R(r"\mathbb Q"), R(r"\mathbb Q"), R(r"\mathbb Q"), R(r"\mathbb I"), R(r"\mathbb Q"), R(r"\frac32\in\mathbb Q")])),
 (1, T(r"Raona si les afirmacions següents són verdaderes o falses:", r"Razona si las afirmaciones siguientes son verdaderas o falsas:")
     + tasks(1, [T(r"Tot nombre enter és racional.", r"Todo número entero es racional."),
                 T(r"Tot nombre decimal es pot expressar en forma de fracció.", r"Todo número decimal se puede expresar en forma de fracción."),
                 T(r"Tot nombre natural es pot escriure com una fracció.", r"Todo número natural se puede escribir como una fracción."),
                 T(r"Si es sumen dos nombres racionals, el resultat és sempre un nombre racional.", r"Si se suman dos números racionales, el resultado es siempre un número racional."),
                 T(r"Si es multipliquen dos nombres irracionals, el resultat és sempre irracional.", r"Si se multiplican dos números irracionales, el resultado es siempre irracional.")]),
     tasks(1, [T(r"\rest{Verdadera}: tot enter $n$ es pot escriure com $\frac n1$.", r"\rest{Verdadera}: todo entero $n$ se puede escribir como $\frac n1$."),
               T(r"\rest{Falsa}: només els exactes i els periòdics; $\pi=3,1415\ldots$ no.", r"\rest{Falsa}: solo los exactos y los periódicos; $\pi=3,1415\ldots$ no."),
               T(r"\rest{Verdadera}: per exemple, $5=\frac{10}{2}$.", r"\rest{Verdadera}: por ejemplo, $5=\frac{10}{2}$."),
               T(r"\rest{Verdadera}: $\frac ab+\frac cd=\frac{ad+bc}{bd}$, que és una fracció.", r"\rest{Verdadera}: $\frac ab+\frac cd=\frac{ad+bc}{bd}$, que es una fracción."),
               T(r"\rest{Falsa}: $\sqrt2\cdot\sqrt8=\sqrt{16}=4$.", r"\rest{Falsa}: $\sqrt2\cdot\sqrt8=\sqrt{16}=4$.")])),
 (1, T(r"Troba la fracció generatriu i simplifica-la:", r"Halla la fracción generatriz y simplifícala:")
     + tasks(3, [r"$0,1\widehat6$", r"$2,\widehat{09}$", r"$-1,2\widehat{45}$", r"$3,\widehat{12}$", r"$0,4\widehat5$", r"$2,45$"])
     + recorda(T(r"Fracció generatriu: al numerador, el nombre sense coma (fins al final del primer període) menys la part no periòdica; al denominador, tants 9 com xifres té el període i tants 0 com xifres té l'anteperíode.",
                 r"Fracción generatriz: en el numerador, el número sin coma (hasta el final del primer periodo) menos la parte no periódica; en el denominador, tantos 9 como cifras tiene el periodo y tantos 0 como cifras tiene el anteperiodo.")),
     tasks(3, [R(tn(x)) for x in gen])),
 (2, T(r"Realitza les operacions següents escrivint prèviament els nombres en forma de fracció:", r"Realiza las operaciones siguientes escribiendo previamente los números en forma de fracción:")
     + tasks(2, [r"$2,\widehat7+3,\widehat4-1,\widehat1$", r"$1,\widehat8+0,\widehat1$", r"$0,\widehat3\cdot1,\widehat5-0,1\widehat6$", r"$\left(1,\widehat2+0,5\right)\cdot0,\widehat{18}$"]),
     tasks(2, [RR(r"\frac{25}{9}+\frac{31}{9}-\frac{10}{9}=", tn(e4[0])), RR(r"\frac{17}{9}+\frac19=", tn(e4[1])),
               RR(r"\frac13\cdot\frac{14}{9}-\frac16=", tn(e4[2])), RR(r"\frac{31}{18}\cdot\frac{2}{11}=", tn(e4[3]))])
     + T(r"Fixa't en b): $1,\widehat8+0,\widehat1=1,\widehat9=2$.", r"Fíjate en b): $1,\widehat8+0,\widehat1=1,\widehat9=2$.")),
 (2, T(r"Classifica cada nombre en el menor conjunt numèric. Opera primer!", r"Clasifica cada número en el menor conjunto numérico. ¡Opera primero!")
     + tasks(3, [r"$\sqrt2\cdot\sqrt8$", r"$\sqrt2+\sqrt8$", r"$\pi-\pi$", r"$0,1010010001\ldots$", r"$-\sqrt{\frac94}$", r"$\sqrt{-4}$"]),
     tasks(3, [R(r"4\in\mathbb N"), R(r"3\sqrt2\in\mathbb I"), R(r"0\in\mathbb N"), R(r"\mathbb I") + T(r" (no és periòdic)", r" (no es periódico)"), R(r"-\frac32\in\mathbb Q"),
               T(r"No és un nombre real.", r"No es un número real.")])),
]))

# =====================================================================
# 2. Intervals i semirectes
S.append((T("Intervals i semirectes", "Intervalos y semirrectas"), [
 (1, T(r"Completa la taula següent:", r"Completa la tabla siguiente:") + '\n\n\\begin{center}\\renewcommand{\\arraystretch}{1.5}\\begin{tabular}{|C{4.6cm}|C{3.2cm}|C{6cm}|}\\hline\\rowcolor{soft}\\textbf{'
     + T('Desigualtat', 'Desigualdad') + '} & \\textbf{' + T('Interval', 'Intervalo') + '} & \\textbf{' + T('Representació', 'Representación') + '}\\\\\\hline'
     r'$\{x\in\mathbb R\ /\ x<-3\}$ & & \\\hline & $x\in[-2, 4)$ & \\\hline $\{x\in\mathbb R\ /\ -5<x\le-3\}$ & & \\\hline & $x\in(4, +\infty)$ & \\\hline\end{tabular}\end{center}',
     tasks(2, [r"$x<-3$: " + RI('(-inf,-3)'), r"$-2\le x<4$: " + RI('[-2,4)'), r"$-5<x\le-3$: " + RI('(-5,-3]'), r"$x>4$: " + RI('(4,inf)')])),
 (1, T(r"Escriu com a interval o semirecta i representa els conjunts numèrics següents:", r"Escribe como intervalo o semirrecta y representa los conjuntos numéricos siguientes:")
     + tasks(2, [T(r"Nombres majors que 3.", r"Números mayores que 3."), r"$\{x\in\mathbb R/2\le x\le5\}$", r"$\{x\in\mathbb R/3<x\le7\}$", T(r"Nombres menors que 1 excloent-ne el 0.", r"Números menores que 1 excluyendo el 0."),
                 T(r"Nombres reals positius.", r"Números reales positivos."), r"$\{x\in\mathbb R/-2\le x<5\}$", T(r"Nombres no negatius.", r"Números no negativos."), r"$\{x\in\mathbb R/x\le-1\}$"]),
     tasks(2, [RI('(3,inf)'), RI('[2,5]'), RI('(3,7]'), RI('(-inf,0)U(0,1)'), RI('(0,inf)'), RI('[-2,5)'), RI('[0,inf)'), RI('(-inf,-1]')])),
 (1, T(r"Expressa com a desigualtat, com a interval i representa:", r"Expresa como desigualdad, como intervalo y representa:")
     + tasks(2, [T(r"$x$ és menor que $-5$.", r"$x$ es menor que $-5$."), T(r"3 és menor o igual que $x$.", r"3 es menor o igual que $x$."),
                 T(r"$x$ està comprès entre $-5$ i 1.", r"$x$ está comprendido entre $-5$ y 1."), T(r"$x$ està entre $-2$ i 0, tots dos inclosos.", r"$x$ está entre $-2$ y 0, ambos incluidos."),
                 T(r"$x$ és major o igual que $-1$ i menor que 6.", r"$x$ es mayor o igual que $-1$ y menor que 6."), T(r"$x$ no és major que 2.", r"$x$ no es mayor que 2.")]),
     tasks(2, [r"$x<-5$: " + RI('(-inf,-5)'), r"$x\ge3$: " + RI('[3,inf)'), r"$-5<x<1$: " + RI('(-5,1)'), r"$-2\le x\le0$: " + RI('[-2,0]'),
               r"$-1\le x<6$: " + RI('[-1,6)'), r"$x\le2$: " + RI('(-inf,2]')])),
 (1, T(r"Escriu la desigualtat que verifica tot nombre $x$ que pertany a aquests intervals i semirectes, i representa'ls:",
       r"Escribe la desigualdad que verifica todo número $x$ que pertenece a estos intervalos y semirrectas, y represéntalos:")
     + tasks(4, [r"$[-2, 7]$", r"$[13, +\infty)$", r"$(-\infty, 0)$", r"$(-3, 0]$", r"$\left[\frac32, 6\right)$", r"$(-\infty, +\infty)$", r"$(1, 6)$", r"$(0, 4]$",
                 r"$(-\infty, 2)$", r"$(-\infty, -5]$", r"$(-1, +\infty)$", r"$\left(2, \frac72\right)$"]),
     tasks(2, [r"$-2\le x\le7$ " + recta(P('[-2,7]')), r"$x\ge13$ " + recta(P('[13,inf)')), r"$x<0$ " + recta(P('(-inf,0)')), r"$-3<x\le0$ " + recta(P('(-3,0]')),
               r"$\frac32\le x<6$ " + recta(P('[3/2,6)')), r"$x\in\mathbb R$ " + recta(P('(-inf,inf)'), -3, 3), r"$1<x<6$ " + recta(P('(1,6)')), r"$0<x\le4$ " + recta(P('(0,4]')),
               r"$x<2$ " + recta(P('(-inf,2)')), r"$x\le-5$ " + recta(P('(-inf,-5]')), r"$x>-1$ " + recta(P('(-1,inf)')), r"$2<x<\frac72$ " + recta(P('(2,7/2)'))])),
 (1, T(r"Quins nombres enters pertanyen a cadascun dels conjunts següents?", r"¿Qué números enteros pertenecen a cada uno de los conjuntos siguientes?")
     + tasks(4, [r"$[-2, 3)$", r"$\left(-1, \frac52\right]$", r"$(-4, -1)$", r"$(3, 4)$"]),
     tasks(4, [R(r"-2,\,-1,\,0,\,1,\,2"), R(r"0,\,1,\,2"), R(r"-3,\,-2"), T(r"Cap: ", r"Ninguno: ") + R(r"\varnothing")])),
]))
ck([[n for n in range(-10, 10) if -2 <= n < 3], [n for n in range(-10, 10) if -1 < n <= F(5, 2)], [n for n in range(-10, 10) if -4 < n < -1], [n for n in range(-10, 10) if 3 < n < 4]],
   [[-2, -1, 0, 1, 2], [0, 1, 2], [-3, -2], []])

# =====================================================================
# 3. Valor absolut
eq13 = [[-5, 5], [1, 5], [-4, 3], [], [2], [4, 6]]
def absEq(a, b, r):
    if r < 0: return []
    return sorted({F(r - b, a), F(-r - b, a)})
ck([absEq(1, 0, 5), absEq(1, -3, 2), absEq(2, 1, 7), absEq(1, 4, -1), absEq(3, -6, 0), absEq(-1, 5, 1)], eq13)
d14 = [absI(1, 0, '<', 3), absI(1, 0, '>=', 3), absI(1, -2, '<=', 3), absI(1, -4, '>', 2), absI(2, -1, '>', 1), absI(-5, 3, '<', 7),
       absI(1, 1, '<=', F(1, 2)), absI(-5, 25, '<=', -2), absI(1, F(3, 4), '>', -1)]
ck(d14, [P('(-3,3)'), P('(-inf,-3]U[3,inf)'), P('[-1,5]'), P('(-inf,2)U(6,inf)'), P('(-inf,0)U(1,inf)'), P('(-4/5,2)'), P('[-3/2,-1/2]'), [], RE])
ck([absI(1, -4, '<', 3), absI(1, 2, '<=', 3), absI(1, -2, '>', 3), absI(1, 0, '<=', F(1, 2))], [P('(1,7)'), P('[-5,1]'), P('(-inf,-1)U(5,inf)'), P('[-1/2,1/2]')])
cn([abs(-7), abs(3 - 8), -abs(-5), abs(-2) + abs(5), abs(-3 * 4), abs(abs(-5) - 8), abs(math.pi - 4), abs(1 - r3)], [7, 5, -5, 7, 12, 3, 4 - math.pi, r3 - 1])
S.append((T("Valor absolut", "Valor absoluto"), [
 (1, T(r"Calcula:", r"Calcula:") + tasks(4, [r"$|-7|$", r"$|3-8|$", r"$-|-5|$", r"$|-2|+|5|$", r"$|(-3)\cdot4|$", r"$\big||-5|-8\big|$", r"$|\pi-4|$", r"$|1-\sqrt3|$"]),
     tasks(4, [R("7"), R("5"), R("-5"), R("7"), R("12"), R("3"), R(r"4-\pi"), R(r"\sqrt3-1")]) + T(r"Als apartats g) i h), el de dins és negatiu: canviem el signe.", r"En los apartados g) y h), lo de dentro es negativo: cambiamos el signo.")),
 (1, T(r"Calcula la distància entre els parells de nombres següents:", r"Calcula la distancia entre los pares de números siguientes:")
     + tasks(4, [r"$-4$ " + T("i", "y") + r" $6$", r"$2$ " + T("i", "y") + r" $7$", r"$-3$ " + T("i", "y") + r" $-9$", r"$-\frac12$ " + T("i", "y") + r" $\frac32$"]),
     tasks(4, [RR(r"|-4-6|=", "10"), RR(r"|2-7|=", "5"), RR(r"|-3+9|=", "6"), RR(r"\left|-\tfrac12-\tfrac32\right|=", "2")])),
 (2, T(r"Resol les equacions següents:", r"Resuelve las ecuaciones siguientes:") + tasks(3, [r"$|x|=5$", r"$|x-3|=2$", r"$|2x+1|=7$", r"$|x+4|=-1$", r"$|3x-6|=0$", r"$|5-x|=1$"])
     + recorda(T(r"Si $r>0$, \ $|A|=r\iff A=r$ o $A=-r$.", r"Si $r>0$, \ $|A|=r\iff A=r$ o $A=-r$.")),
     tasks(3, [R(r"x=\pm5"), R(r"x=1,\ x=5"), R(r"x=3,\ x=-4"), T(r"No té solució.", r"No tiene solución."), R("x=2"), R(r"x=4,\ x=6")])),
 (2, T(r"Esbrina per a quins valors de $x$ es compleixen les desigualtats següents. Escriu la solució com a interval i representa-la:",
       r"Averigua para qué valores de $x$ se cumplen las desigualdades siguientes. Escribe la solución como intervalo y represéntala:")
     + tasks(3, [r"$|x|<3$", r"$|x|\ge3$", r"$|x-2|\le3$", r"$|x-4|>2$", r"$|2x-1|>1$", r"$|-5x+3|<7$", r"$|x+1|\le\frac12$", r"$|-5x+25|\le-2$", r"$\left|x+\frac34\right|>-1$"])
     + recorda(T(r"Si $r>0$: \ $|A|<r\iff -r<A<r$ \quad i \quad $|A|>r\iff A<-r$ o $A>r$. En multiplicar o dividir per un nombre negatiu, la desigualtat canvia de sentit.",
                 r"Si $r>0$: \ $|A|<r\iff -r<A<r$ \quad y \quad $|A|>r\iff A<-r$ o $A>r$. Al multiplicar o dividir por un número negativo, la desigualdad cambia de sentido.")),
     tasks(2, [RI(x) for x in d14[:7]] + [R(r"\varnothing") + T(r" (un valor absolut no pot ser negatiu)", r" (un valor absoluto no puede ser negativo)"),
                                          R(r"\mathbb R") + T(r" (sempre es compleix)", r" (siempre se cumple)")])),
 (2, T(r"Expressa cada conjunt amb una desigualtat amb valor absolut (busca el centre i el radi):", r"Expresa cada conjunto con una desigualdad con valor absoluto (busca el centro y el radio):")
     + tasks(4, [r"$(1, 7)$", r"$[-5, 1]$", r"$(-\infty, -1)\cup(5, +\infty)$", r"$\left[-\frac12, \frac12\right]$"]),
     tasks(4, [R(r"|x-4|<3"), R(r"|x+2|\le3"), R(r"|x-2|>3"), R(r"|x|\le\frac12")])),
]))

# =====================================================================
# 4. Unió i intersecció d'intervals
A, B, C, D, E = P('[-3,2]'), P('[0,5]'), P('[2,inf)'), P('(0,10)'), P('(2,7/2)')
r16 = [cap(A, B), cap(A, D), cup(A, B), cap(cup(A, B), C), cap(A, C), cup(B, C), cap(C, D), cap(E, B), cup(A, E)]
ck(r16, [P('[0,2]'), P('(0,2]'), P('[-3,5]'), P('[2,5]'), P('[2,2]'), P('[0,inf)'), P('[2,10)'), P('(2,7/2)'), P('[-3,7/2)')])
A, B, C, D, E = P('(-inf,-4]'), P('[2,5)'), P('[-6,1]'), P('[0,inf)'), P('(-2,-1)')
r17 = [cup(A, B), cap(B, C), cap(D, C), cup(A, cap(B, D)), cap(B, cup(A, E)), cap(cap(B, D), E), cap(cup(B, C), A), cup(A, C), cap(C, E), cap(A, D)]
ck(r17, [P('(-inf,-4]U[2,5)'), [], P('[0,1]'), P('(-inf,-4]U[2,5)'), [], [], P('[-6,-4]'), P('(-inf,1]'), P('(-2,-1)'), []])
r18 = [cap(P('(-inf,3)'), P('[5,inf)')), cap(P('(0,inf)'), P('(-inf,4)')), cap(P('(-inf,-1]'), P('(1,inf)')), cap(P('(-inf,3)'), P('[-2,inf)')),
       cup(P('(-inf,-1)'), P('[2,inf)')), cup(P('(0,inf)'), P('(-inf,4)'))]
ck(r18, [[], P('(0,4)'), [], P('[-2,3)'), P('(-inf,-1)U[2,inf)'), RE])
A19 = absI(1, -1, '<', 2)
r19 = [A19, cup(A19, P('[2,inf)')), cap(A19, P('[2,inf)'))]
ck(r19, [P('(-1,3)'), P('(-1,inf)'), P('[2,3)')])
S.append((T("Unió i intersecció d'intervals", "Unión e intersección de intervalos"), [
 (2, T(r"Donats els intervals $A=[-3, 2]$, $B=[0, 5]$, $C=[2, +\infty)$, $D=(0, 10)$ i $E=\left(2, \frac72\right)$, calcula:",
       r"Dados los intervalos $A=[-3, 2]$, $B=[0, 5]$, $C=[2, +\infty)$, $D=(0, 10)$ y $E=\left(2, \frac72\right)$, calcula:")
     + tasks(3, [r"$A\cap B$", r"$A\cap D$", r"$A\cup B$", r"$(A\cup B)\cap C$", r"$A\cap C$", r"$B\cup C$", r"$C\cap D$", r"$E\cap B$", r"$A\cup E$"])
     + recorda(T(r"Dibuixa els intervals l'un damunt de l'altre en la mateixa recta. La unió ($\cup$) són els nombres que estan en algun dels dos; la intersecció ($\cap$), els que estan en tots dos alhora.",
                 r"Dibuja los intervalos uno encima del otro en la misma recta. La unión ($\cup$) son los números que están en alguno de los dos; la intersección ($\cap$), los que están en los dos a la vez.")),
     tasks(3, [R(st(x)) for x in r16]) + T(r"A l'apartat e), l'únic nombre comú és el 2.", r"En el apartado e), el único número común es el 2.")),
 (2, T(r"Donats $A=(-\infty, -4]$, $B=[2, 5)$, $C=[-6, 1]$, $D=[0, +\infty)$ i $E=(-2, -1)$, calcula:", r"Dados $A=(-\infty, -4]$, $B=[2, 5)$, $C=[-6, 1]$, $D=[0, +\infty)$ y $E=(-2, -1)$, calcula:")
     + tasks(3, [r"$A\cup B$", r"$B\cap C$", r"$D\cap C$", r"$A\cup(B\cap D)$", r"$B\cap(A\cup E)$", r"$B\cap D\cap E$", r"$(B\cup C)\cap A$", r"$A\cup C$", r"$C\cap E$", r"$A\cap D$"]),
     tasks(2, [R(st(x)) for x in r17])),
 (1, T(r"Escriu en forma d'interval els nombres que verifiquen:", r"Escribe en forma de intervalo los números que verifican:")
     + tasks(3, [T(r"$x<3$ i $x\ge5$", r"$x<3$ y $x\ge5$"), T(r"$x>0$ i $x<4$", r"$x>0$ y $x<4$"), T(r"$x\le-1$ i $x>1$", r"$x\le-1$ y $x>1$"),
                 T(r"$x<3$ i $x\ge-2$", r"$x<3$ y $x\ge-2$"), r"$x<-1$ " + T("o", "o") + r" $x\ge2$", r"$x>0$ " + T("o", "o") + r" $x<4$"]),
     tasks(3, [R(st(x)) for x in r18]) + T(r"«i» és una intersecció i «o», una unió.", r"«y» es una intersección y «o», una unión.")),
 (2, T(r"Siga $A$ el conjunt dels nombres que compleixen $|x-1|<2$ i $B=[2, +\infty)$. Escriu $A$ com a interval i calcula $A\cup B$ i $A\cap B$. Representa'ls.",
       r"Sea $A$ el conjunto de los números que cumplen $|x-1|<2$ y $B=[2, +\infty)$. Escribe $A$ como intervalo y calcula $A\cup B$ y $A\cap B$. Represéntalos.")
     , tasks(3, [r"$A=$ " + RI(r19[0]), r"$A\cup B=$ " + RI(r19[1]), r"$A\cap B=$ " + RI(r19[2])])),
]))

# =====================================================================
# 5. Radicals
cn([math.sqrt(16), rt(-8, 3), rt(32, 5), rt(27 / 8, 3), rt(0.064, 3), rt(81, 4), rt(-1 / 32, 5)], [4, -2, 2, 1.5, 0.4, 3, -0.5])
cn([8 ** (2 / 3), 81 ** 0.75, (1 / 32) ** (-2 / 5), 16 ** 0.75, 27 ** (-1 / 3), 25 ** 1.5], [4, 27, 4, 8, 1 / 3, 125])
a_, b_, x_, y_, z_, m_, n_ = 1.7, 2.3, 1.3, 0.8, 2.9, 1.9, 0.6
cn([rt(2 ** 4, 6), rt(a_ ** 6, 9), rt(8 * a_ ** 3, 15), rt(16 * a_ ** 4, 8), rt(0.027, 6), rt(x_ ** 8 * y_ ** 4, 12), rt(25, 4), rt(64, 6)],
   [rt(4, 3), rt(a_ ** 2, 3), rt(2 * a_, 5), math.sqrt(2 * a_), math.sqrt(0.3), rt(x_ ** 2 * y_, 3), r5, 2])
cn([rt(8, 6), rt(9, 6), rt(n_ ** 8, 12), rt(m_ ** 9, 12), rt(n_ ** 10, 12), rt(a_ ** 6, 12), rt(a_ ** 8, 12), rt(a_ ** 9, 12), rt(25 * x_ ** 2 * y_ ** 4, 6), rt(216 * x_ ** 9 * z_ ** 3, 6)],
   [r2, rt(3, 3), rt(n_ ** 2, 3), rt(m_ ** 3, 4), rt(n_ ** 5, 6), math.sqrt(a_), rt(a_ ** 2, 3), rt(a_ ** 3, 4), rt(5 * x_ * y_ ** 2, 3), math.sqrt(6 * x_ ** 3 * z_)])
CHK.append((rt(5, 3) < r3 < rt(10, 4) and rt(6, 6) < r2 < rt(3, 3) and rt(2, 3) < rt(3, 4), 'ordre'))
ck([5 ** 4, 3 ** 6, 10 ** 3, 2 ** 4, 3 ** 3], [625, 729, 1000, 16, 27])
cn([math.sqrt(8), math.sqrt(12), rt(16, 3), rt(54, 3), rt(64, 5), math.sqrt(27 / 4), 3 * math.sqrt(8 * a_ ** 3), rt(54 * a_ ** 4, 3), math.sqrt(72 * x_ ** 3 * y_ ** 4), rt(32 * x_ ** 6, 4)],
   [2 * r2, 2 * r3, 2 * rt(2, 3), 3 * rt(2, 3), 2 * rt(2, 5), 3 * r3 / 2, 6 * a_ * math.sqrt(2 * a_), 3 * a_ * rt(2 * a_, 3), 6 * x_ * y_ ** 2 * math.sqrt(2 * x_), 2 * x_ * rt(2 * x_ ** 2, 4)])
cn([7 * math.sqrt(a_), 2 * a_ * math.sqrt(3 * a_), x_ * math.sqrt(1 / x_), 1.5 * math.sqrt(2 / 3), 2 * rt(3, 3), 3 * rt(2, 3), 2 / 3 * rt(81 / 4, 3), a_ ** 2 * math.sqrt(a_)],
   [math.sqrt(49 * a_), math.sqrt(12 * a_ ** 3), math.sqrt(x_), math.sqrt(1.5), rt(24, 3), rt(54, 3), rt(6, 3), math.sqrt(a_ ** 5)])
cn([math.sqrt(8) + math.sqrt(18) + math.sqrt(32) + math.sqrt(50), math.sqrt(28) + math.sqrt(63) - math.sqrt(175), 3 * r2 - 3 * math.sqrt(8) + 3 * math.sqrt(18),
    2 * a_ * r3 - math.sqrt(27 * a_ ** 2) + a_ * math.sqrt(12), 5 * math.sqrt(20) - 2 * math.sqrt(45) + r5, math.sqrt(18) + 5 * math.sqrt(12) - 2 * r2 - math.sqrt(243),
    math.sqrt(1 / 3) + math.sqrt(27), 2 * rt(16, 3) - rt(54, 3) + rt(250, 3)],
   [14 * r2, 0, 6 * r2, a_ * r3, 5 * r5, r2 + r3, 10 * r3 / 3, 6 * rt(2, 3)])
cn([r5 * r6, math.sqrt(12) * r3, rt(4, 3) * rt(16, 3), r5 * rt(6, 3), math.sqrt(20) / r5, rt(9 * x_ ** 5 * y_ ** 3, 4) / rt(3 * x_ ** 3 * y_, 4), r2 / rt(2, 3), math.sqrt(a_) * rt(a_, 3) * rt(a_, 4)],
   [math.sqrt(30), 6, 4, rt(4500, 6), 2, rt(3 * x_ ** 2 * y_ ** 2, 4), rt(2, 6), a_ * rt(a_, 12)])
cn([r3 ** 4, rt(2, 3) ** 6, r2 ** 5, rt(a_ ** 3, 4) ** 2, math.sqrt(math.sqrt(8)), rt(math.sqrt(32), 3), math.sqrt(2 * r2), (2 * r3) ** 2, rt((27 * x_ ** 3 * y_ ** 6) ** 5, 3)],
   [9, 4, 4 * r2, a_ * math.sqrt(a_), rt(8, 4), rt(32, 6), rt(8, 4), 12, 243 * x_ ** 5 * y_ ** 10])
cn([(r3 + r2) ** 2, (2 * r3 - 1) * (2 * r3 + 1), (r5 - 2) ** 2, r2 * (math.sqrt(8) - math.sqrt(18)), (1 + r2) ** 2 - math.sqrt(8)], [5 + 2 * r6, 11, 9 - 4 * r5, -2, 3])
S.append((T("Radicals", "Radicales"), [
 (1, T(r"Calcula el valor dels radicals següents, si existeixen:", r"Calcula el valor de los radicales siguientes, si existen:")
     + tasks(4, [r"$\sqrt{16}$", r"$\sqrt[3]{-8}$", r"$\sqrt[5]{32}$", r"$\sqrt[3]{\frac{27}{8}}$", r"$\sqrt[3]{0,064}$", r"$\sqrt[4]{81}$", r"$\sqrt[4]{-16}$", r"$\sqrt[5]{-\frac{1}{32}}$"]),
     tasks(4, [R("4"), R("-2"), R("2"), R(r"\frac32"), R("0,4"), R("3"), T(r"No existeix en $\mathbb R$ (índex parell i radicand negatiu).", r"No existe en $\mathbb R$ (índice par y radicando negativo)."), R(r"-\frac12")])),
 (1, T(r"Escriu en forma de potència els radicals de la primera fila i en forma de radical les potències de la segona:", r"Escribe en forma de potencia los radicales de la primera fila y en forma de radical las potencias de la segunda:")
     + tasks(5, [r"$\sqrt5$", r"$\sqrt[3]{x^2}$", r"$\sqrt[5]{a^3}$", r"$\dfrac{1}{\sqrt2}$", r"$\dfrac{1}{\sqrt[3]{a^2}}$", r"$3^{\frac25}$", r"$a^{\frac34}$", r"$5^{-\frac12}$", r"$x^{1,5}$", r"$2^{\frac53}$"])
     + recorda(r"$\sqrt[n]{a^m}=a^{\frac mn}$"),
     tasks(5, [R(r"5^{\frac12}"), R(r"x^{\frac23}"), R(r"a^{\frac35}"), R(r"2^{-\frac12}"), R(r"a^{-\frac23}"), R(r"\sqrt[5]{9}"), R(r"\sqrt[4]{a^3}"), R(r"\frac{1}{\sqrt5}"), R(r"\sqrt{x^3}"), R(r"\sqrt[3]{32}=2\sqrt[3]4")])),
 (1, T(r"Calcula sense calculadora passant a exponents fraccionaris:", r"Calcula sin calculadora pasando a exponentes fraccionarios:")
     + tasks(3, [r"$8^{\frac23}$", r"$81^{0,75}$", r"$\left(\dfrac{1}{32}\right)^{-\frac25}$", r"$16^{\frac34}$", r"$27^{-\frac13}$", r"$25^{\frac32}$"]),
     tasks(3, [RR(r"(2^3)^{\frac23}=2^2=", "4"), RR(r"(3^4)^{\frac34}=3^3=", "27"), RR(r"(2^{-5})^{-\frac25}=2^2=", "4"), RR(r"(2^4)^{\frac34}=2^3=", "8"), RR(r"(3^3)^{-\frac13}=3^{-1}=", r"\frac13"), RR(r"(5^2)^{\frac32}=5^3=", "125")])),
 (1, T(r"Simplifica els radicals següents:", r"Simplifica los radicales siguientes:")
     + tasks(4, [r"$\sqrt[6]{2^4}$", r"$\sqrt[9]{a^6}$", r"$\sqrt[15]{8a^3}$", r"$\sqrt[8]{16a^4}$", r"$\sqrt[6]{0,027}$", r"$\sqrt[12]{x^8y^4}$", r"$\sqrt[4]{25}$", r"$\sqrt[6]{64}$"]),
     tasks(4, [R(r"\sqrt[3]{4}"), R(r"\sqrt[3]{a^2}"), R(r"\sqrt[5]{2a}"), R(r"\sqrt{2a}"), R(r"\sqrt{0,3}"), R(r"\sqrt[3]{x^2y}"), R(r"\sqrt5"), R("2")])),
 (2, T(r"Redueix els radicals de cada apartat al mínim índex comú:", r"Reduce los radicales de cada apartado al mínimo índice común:")
     + tasks(2, [r"$\sqrt2,\ \sqrt[3]3$", r"$\sqrt[3]{n^2},\ \sqrt[4]{m^3},\ \sqrt[6]{n^5}$", r"$\sqrt a,\ \sqrt[3]{a^2},\ \sqrt[4]{a^3}$", r"$\sqrt[3]{5xy^2},\ \sqrt{6x^3z}$"]),
     tasks(2, [R(r"\sqrt[6]{8},\ \sqrt[6]{9}"), R(r"\sqrt[12]{n^8},\ \sqrt[12]{m^9},\ \sqrt[12]{n^{10}}"), R(r"\sqrt[12]{a^6},\ \sqrt[12]{a^8},\ \sqrt[12]{a^9}"), R(r"\sqrt[6]{25x^2y^4},\ \sqrt[6]{216x^9z^3}")])),
 (2, T(r"Ordena de menor a major reduint a índex comú:", r"Ordena de menor a mayor reduciendo a índice común:") + tasks(3, [r"$\sqrt3,\ \sqrt[3]5,\ \sqrt[4]{10}$", r"$\sqrt2,\ \sqrt[3]3,\ \sqrt[6]6$", r"$\sqrt[3]2,\ \sqrt[4]3$"]),
     tasks(1, [r"$\sqrt[12]{729},\ \sqrt[12]{625},\ \sqrt[12]{1000}\ \Rightarrow\ " + R(r"\sqrt[3]5<\sqrt3<\sqrt[4]{10}").strip('$') + "$",
               r"$\sqrt[6]{8},\ \sqrt[6]{9},\ \sqrt[6]{6}\ \Rightarrow\ " + R(r"\sqrt[6]6<\sqrt2<\sqrt[3]3").strip('$') + "$",
               r"$\sqrt[12]{16},\ \sqrt[12]{27}\ \Rightarrow\ " + R(r"\sqrt[3]2<\sqrt[4]3").strip('$') + "$"])),
 (2, T(r"Extrau tots els factors possibles de cadascun dels radicals següents:", r"Extrae todos los factores posibles de cada uno de los radicales siguientes:")
     + tasks(5, [r"$\sqrt8$", r"$\sqrt{12}$", r"$\sqrt[3]{16}$", r"$\sqrt[3]{54}$", r"$\sqrt[5]{64}$", r"$\sqrt{\frac{27}{4}}$", r"$3\sqrt{8a^3}$", r"$\sqrt[3]{54a^4}$", r"$\sqrt{72x^3y^4}$", r"$\sqrt[4]{32x^6}$"]),
     tasks(4, [R(r"2\sqrt2"), R(r"2\sqrt3"), R(r"2\sqrt[3]2"), R(r"3\sqrt[3]2"), R(r"2\sqrt[5]2"), R(r"\frac{3\sqrt3}{2}"), R(r"6a\sqrt{2a}"), R(r"3a\sqrt[3]{2a}"), R(r"6xy^2\sqrt{2x}"), R(r"2x\sqrt[4]{2x^2}")])),
 (2, T(r"Introdueix el coeficient dins del radical i simplifica:", r"Introduce el coeficiente dentro del radical y simplifica:")
     + tasks(3, [r"$7\sqrt a$", r"$2a\sqrt{3a}$", r"$x\sqrt{\frac1x}$", r"$\frac32\sqrt{\frac23}$", r"$2\sqrt[3]3$", r"$3\sqrt[3]2$", r"$\frac23\sqrt[3]{\frac{81}{4}}$", r"$a^2\sqrt a$", r"$3+\sqrt7$"]),
     tasks(3, [R(r"\sqrt{49a}"), R(r"\sqrt{12a^3}"), R(r"\sqrt x"), R(r"\sqrt{\frac32}"), R(r"\sqrt[3]{24}"), R(r"\sqrt[3]{54}"), R(r"\sqrt[3]6"), R(r"\sqrt{a^5}"),
               T(r"No es pot (és una suma).", r"No se puede (es una suma).")])),
 (2, T(r"Realitza les sumes i restes següents:", r"Realiza las sumas y restas siguientes:")
     + tasks(2, [r"$\sqrt8+\sqrt{18}+\sqrt{32}+\sqrt{50}$", r"$\sqrt{28}+\sqrt{63}-\sqrt{175}$", r"$3\sqrt2-3\sqrt8+3\sqrt{18}$", r"$2a\sqrt3-\sqrt{27a^2}+a\sqrt{12}$",
                 r"$5\sqrt{20}-2\sqrt{45}+\sqrt5$", r"$\sqrt{18}+5\sqrt{12}-2\sqrt2-\sqrt{243}$", r"$\sqrt{\frac13}+\sqrt{27}$", r"$2\sqrt[3]{16}-\sqrt[3]{54}+\sqrt[3]{250}$"])
     + recorda(T(r"Només es poden sumar radicals semblants (mateix índex i mateix radicand). Abans, extrau-ne els factors.", r"Solo se pueden sumar radicales semejantes (mismo índice y mismo radicando). Antes, extrae sus factores.")),
     tasks(4, [R(r"14\sqrt2"), R("0"), R(r"6\sqrt2"), R(r"a\sqrt3"), R(r"5\sqrt5"), R(r"\sqrt2+\sqrt3"), R(r"\frac{10\sqrt3}{3}"), R(r"6\sqrt[3]2")]) + T(r"(A l'apartat d) suposem $a\ge0$.)", r"(En el apartado d) suponemos $a\ge0$.)")),
 (2, T(r"Calcula i simplifica (redueix a índex comú quan calga):", r"Calcula y simplifica (reduce a índice común cuando haga falta):")
     + tasks(4, [r"$\sqrt5\cdot\sqrt6$", r"$\sqrt{12}\cdot\sqrt3$", r"$\sqrt[3]4\cdot\sqrt[3]{16}$", r"$\sqrt5\cdot\sqrt[3]6$", r"$\sqrt{20}:\sqrt5$", r"$\sqrt[4]{9x^5y^3}:\sqrt[4]{3x^3y}$", r"$\dfrac{\sqrt2}{\sqrt[3]2}$", r"$\sqrt a\cdot\sqrt[3]a\cdot\sqrt[4]a$"]),
     tasks(4, [R(r"\sqrt{30}"), R("6"), R("4"), R(r"\sqrt[6]{4500}"), R("2"), R(r"\sqrt[4]{3x^2y^2}"), R(r"\sqrt[6]2"), R(r"a\sqrt[12]a")])),
 (2, T(r"Calcula les potències i escriu davall d'un sol radical:", r"Calcula las potencias y escribe bajo un solo radical:")
     + tasks(3, [r"$(\sqrt3)^4$", r"$(\sqrt[3]2)^6$", r"$(\sqrt2)^5$", r"$\left(\sqrt[4]{a^3}\right)^2$", r"$(2\sqrt3)^2$", r"$\sqrt[3]{(27x^3y^6)^5}$", r"$\sqrt{\sqrt8}$", r"$\sqrt[3]{\sqrt{32}}$", r"$\sqrt{2\sqrt2}$"]),
     tasks(3, [R("9"), R("4"), R(r"4\sqrt2"), R(r"a\sqrt a"), R("12"), R(r"243x^5y^{10}"), R(r"\sqrt[4]8"), R(r"\sqrt[6]{32}"), R(r"\sqrt[4]8")])),
 (2, T(r"Opera i simplifica:", r"Opera y simplifica:") + tasks(3, [r"$(\sqrt3+\sqrt2)^2$", r"$(2\sqrt3-1)(2\sqrt3+1)$", r"$(\sqrt5-2)^2$", r"$\sqrt2\left(\sqrt8-\sqrt{18}\right)$", r"$(1+\sqrt2)^2-\sqrt8$"]),
     tasks(3, [R(r"5+2\sqrt6"), R("11"), R(r"9-4\sqrt5"), R("-2"), R("3")])),
]))

# =====================================================================
# 6. Racionalització
cn([5 / r5, 2 * r6 / r2, 3 / r5, math.sqrt(5 / 2), 3 / (2 * rt(4, 3)), 6 / rt(3, 3), 3 * y_ / (x_ * math.sqrt(y_)), 2 * math.sqrt(12) / (5 * r3), 10 / rt(8, 4)],
   [r5, 2 * r3, 3 * r5 / 5, math.sqrt(10) / 2, 3 * rt(2, 3) / 4, 2 * rt(9, 3), 3 * math.sqrt(y_) / x_, 0.8, 5 * rt(2, 4)])
cn([1 / (r2 + r3), 2 / (r2 - 1), r2 / (3 - r2), (1 - r2) / (1 + r2), 4 / (r5 - 1), 5 / (2 * (r3 - r2)), (2 + r2) / (2 - r2), r3 / (r3 + 1), 1 / (math.sqrt(z_) - math.sqrt(y_))],
   [r3 - r2, 2 * r2 + 2, (3 * r2 + 2) / 7, 2 * r2 - 3, r5 + 1, 5 * (r3 + r2) / 2, 3 + 2 * r2, (3 - r3) / 2, (math.sqrt(z_) + math.sqrt(y_)) / (z_ - y_)])
cn([(r3 + 1) / (r3 - 1) - (r3 - 1) / (r3 + 1), 1 / r2 + 1 / (r2 + 1), 2 / r3 - 1 / (2 + r3)], [2 * r3, 3 * r2 / 2 - 1, 5 * r3 / 3 - 2])
S.append((T("Racionalització", "Racionalización"), [
 (2, T(r"Racionalitza el denominador de les expressions següents:", r"Racionaliza el denominador de las expresiones siguientes:")
     + tasks(5, [r"$\dfrac{5}{\sqrt5}$", r"$\dfrac{2\sqrt6}{\sqrt2}$", r"$\dfrac{3}{\sqrt5}$", r"$\sqrt{\dfrac52}$", r"$\dfrac{3}{2\sqrt[3]4}$", r"$\dfrac{6}{\sqrt[3]3}$", r"$\dfrac{3y}{x\sqrt y}$", r"$\dfrac{2\sqrt{12}}{5\sqrt3}$", r"$\dfrac{10}{\sqrt[4]8}$"])
     + recorda(T(r"Si al denominador hi ha una sola arrel, multipliquem dalt i baix pel que calga perquè l'arrel desaparega: $\dfrac{1}{\sqrt[n]{a^m}}=\dfrac{\sqrt[n]{a^{n-m}}}{a}$.",
                 r"Si en el denominador hay una sola raíz, multiplicamos arriba y abajo por lo que haga falta para que la raíz desaparezca: $\dfrac{1}{\sqrt[n]{a^m}}=\dfrac{\sqrt[n]{a^{n-m}}}{a}$.")),
     tasks(5, [R(r"\sqrt5"), R(r"2\sqrt3"), R(r"\frac{3\sqrt5}{5}"), R(r"\frac{\sqrt{10}}{2}"), R(r"\frac{3\sqrt[3]2}{4}"), R(r"2\sqrt[3]9"), R(r"\frac{3\sqrt y}{x}"), R(r"\frac45"), R(r"5\sqrt[4]2")])),
 (2, T(r"Racionalitza el denominador de les expressions següents:", r"Racionaliza el denominador de las expresiones siguientes:")
     + tasks(3, [r"$\dfrac{1}{\sqrt2+\sqrt3}$", r"$\dfrac{2}{\sqrt2-1}$", r"$\dfrac{\sqrt2}{3-\sqrt2}$", r"$\dfrac{1-\sqrt2}{1+\sqrt2}$", r"$\dfrac{4}{\sqrt5-1}$", r"$\dfrac{5}{2(\sqrt3-\sqrt2)}$",
                 r"$\dfrac{2+\sqrt2}{2-\sqrt2}$", r"$\dfrac{\sqrt3}{\sqrt3+1}$", r"$\dfrac{1}{\sqrt x-\sqrt y}$"])
     + recorda(T(r"Si al denominador hi ha una suma o una resta amb arrels, multipliquem pel conjugat: $(a+b)(a-b)=a^2-b^2$.", r"Si en el denominador hay una suma o una resta con raíces, multiplicamos por el conjugado: $(a+b)(a-b)=a^2-b^2$.")),
     tasks(3, [R(r"\sqrt3-\sqrt2"), R(r"2\sqrt2+2"), R(r"\frac{3\sqrt2+2}{7}"), R(r"2\sqrt2-3"), R(r"\sqrt5+1"), R(r"\frac{5(\sqrt3+\sqrt2)}{2}"), R(r"3+2\sqrt2"), R(r"\frac{3-\sqrt3}{2}"), R(r"\frac{\sqrt x+\sqrt y}{x-y}")])),
 (2, T(r"Racionalitza, opera i simplifica:", r"Racionaliza, opera y simplifica:") + tasks(3, [r"$\dfrac{\sqrt3+1}{\sqrt3-1}-\dfrac{\sqrt3-1}{\sqrt3+1}$", r"$\dfrac{1}{\sqrt2}+\dfrac{1}{\sqrt2+1}$", r"$\dfrac{2}{\sqrt3}-\dfrac{1}{2+\sqrt3}$"]),
     tasks(1, [RR(r"\dfrac{(\sqrt3+1)^2-(\sqrt3-1)^2}{2}=", r"2\sqrt3"), RR(r"\dfrac{\sqrt2}{2}+\sqrt2-1=", r"\frac{3\sqrt2}{2}-1"), RR(r"\dfrac{2\sqrt3}{3}-(2-\sqrt3)=", r"\frac{5\sqrt3}{3}-2")])),
]))

# =====================================================================
# 7. Logaritmes
L = lambda b, x: math.log(x) / math.log(b)
cn([L(2, 8), L(3, 81), lg(1000), lg(0.0001), L(4, 16), L(4, 0.25), L(5, 1)], [3, 4, 3, -4, 2, -1, 0])
cn([L(3, math.sqrt(27)), L(7, 1 / 49), L(3, 3 * r3), L(3, 1 / 3), L(5, rt(25, 3)), L(9, rt(3, 3)), L(0.5, 8), L(8, 0.125)], [1.5, -2, 1.5, -1, 2 / 3, 1 / 6, -3, -1])
cn([2 ** 3, (1 / 2) ** -3, 5 ** -1, 2 ** 5, 7 ** 2, 10 ** -2], [8, 8, 0.2, 32, 49, 0.01])
l38 = [L(3, 20), L(0.5, 60), L(r2, 3), L(7, 100), L(2, 0.3), L(5, 2)]
cn([round(x, 3) for x in l38], [2.727, -5.907, 3.170, 2.367, -1.737, 0.431])
S.append((T("Logaritmes", "Logaritmos"), [
 (1, T(r"Aplicant la definició, calcula el valor dels logaritmes següents:", r"Aplicando la definición, calcula el valor de los logaritmos siguientes:")
     + tasks(4, [r"$\log_2 8$", r"$\log_3 81$", r"$\log 1000$", r"$\log 0,0001$", r"$\ln e^{5}$", r"$\log_4 16$", r"$\log_4 0,25$", r"$\log_5 1$"])
     + recorda(T(r"$\log_a b=c\iff a^c=b$ \ ($a>0$, $a\neq1$, $b>0$). $\log$ és el logaritme en base 10 i $\ln$, en base $e$.", r"$\log_a b=c\iff a^c=b$ \ ($a>0$, $a\neq1$, $b>0$). $\log$ es el logaritmo en base 10 y $\ln$, en base $e$.")),
     tasks(4, [R("3"), R("4"), R("3"), R("-4"), R("5"), R("2"), R("-1"), R("0")])),
 (1, T(r"Aplicant la definició, calcula el valor dels logaritmes següents:", r"Aplicando la definición, calcula el valor de los logaritmos siguientes:")
     + tasks(4, [r"$\log_3\sqrt{27}$", r"$\log_7\frac{1}{49}$", r"$\log_3 3\sqrt3$", r"$\log_3 0,\widehat3$", r"$\log_5\sqrt[3]{25}$", r"$\log_9\sqrt[3]3$", r"$\log_{\frac12}8$", r"$\log_8 0,125$"]),
     tasks(4, [R(r"\frac32"), R("-2"), R(r"\frac32"), R("-1"), R(r"\frac23"), R(r"\frac16"), R("-3"), R("-1")])),
 (2, T(r"Calcula, si és possible, el valor de $x$ en cadascuna de les expressions següents:", r"Calcula, si es posible, el valor de $x$ en cada una de las expresiones siguientes:")
     + tasks(4, [r"$\log_x 8=3$", r"$\log_x 8=-3$", r"$\log_5 x=-1$", r"$\log_2 x=5$", r"$\log_x 49=2$", r"$\log_3(-81)=x$", r"$\log_x\sqrt2=0$", r"$\log x=-2$"])
     + recorda(T(r"$\log_a b$ només existeix si $a>0$, $a\neq1$ i $b>0$.", r"$\log_a b$ solo existe si $a>0$, $a\neq1$ y $b>0$.")),
     tasks(4, [R("x=2"), R(r"x=\frac12"), R(r"x=\frac15"), R("x=32"), R("x=7"), T(r"No existeix.", r"No existe."), r"No: $x^0=1\neq\sqrt2$.", R("x=0,01")])),
 (1, T(r"Amb l'ajuda de la calculadora i el canvi de base, obtín aproximacions fins a les mil·lèsimes:", r"Con la ayuda de la calculadora y el cambio de base, obtén aproximaciones hasta las milésimas:")
     + tasks(3, [r"$\log_3 20$", r"$\log_{0,5}60$", r"$\log_{\sqrt2}3$", r"$\log_7 100$", r"$\log_2 0,3$", r"$\log_5 2$"])
     + recorda(T(r"Canvi de base: $\log_a x=\dfrac{\log x}{\log a}=\dfrac{\ln x}{\ln a}$.", r"Cambio de base: $\log_a x=\dfrac{\log x}{\log a}=\dfrac{\ln x}{\ln a}$.")),
     tasks(3, [R(d3(x)) for x in l38])),
]))

# =====================================================================
# 8. Propietats dels logaritmes
cn([2 * L(4, 16) + L(2, 32) - 3 * L(7, 49), L(2, 8) + L(3, 27) + 3 * L(5, 125), L(5, 625) - L(9, 81) + L(8, 64), L(6, 4) + L(6, 9), L(2, 40) - L(2, 5), lg(20) + lg(5), L(3, 54) - L(3, 2), 2 * lg(5) + lg(4)],
   [3, 15, 4, 2, 3, 2, 3, 2])
l2, l3 = 0.301, 0.477
v40 = [2 * l2, l2 + l3, 1 - l2, 2 * l2 + l3, l3 - l2, l2 - 2, 2 * (l2 + l3) - 1, l3 / 2, -l3, 2 * l3 + 1 - l2]
cn([round(x, 4) for x in v40], [0.602, 0.778, 0.699, 1.079, 0.176, -1.699, 0.556, 0.2385, -0.477, 1.653])
cn([lg(4), lg(6), lg(5), lg(12), lg(1.5), lg(.02), lg(3.6), lg(r3), lg(1 / 3), lg(45)], v40, 3e-3)
cn([L(3, 150), L(3, 10 / 9)], [0.631 + 1 + 2 * 1.465, 0.631 + 1.465 - 2], 2e-3)
ck([round(0.631 + 1 + 2 * 1.465, 3), round(0.631 + 1.465 - 2, 3)], [4.561, 0.096])
S.append((T("Propietats dels logaritmes", "Propiedades de los logaritmos"), [
 (1, T(r"Troba el resultat de les expressions següents mitjançant les propietats dels logaritmes:", r"Halla el resultado de las expresiones siguientes mediante las propiedades de los logaritmos:")
     + tasks(2, [r"$2\log_4 16+\log_2 32-3\log_7 49$", r"$\log_2 8+\log_3 27+3\log_5 125$", r"$\log_5 625-\log_9 81+\log_8 64$", r"$\log_6 4+\log_6 9$", r"$\log_2 40-\log_2 5$", r"$\log 20+\log 5$",
                 r"$\log_3 54-\log_3 2$", r"$2\log 5+\log 4$"])
     + recorda(T(r"$\log_a(p\cdot q)=\log_a p+\log_a q$, \ $\log_a\frac pq=\log_a p-\log_a q$, \ $\log_a p^n=n\log_a p$.", r"$\log_a(p\cdot q)=\log_a p+\log_a q$, \ $\log_a\frac pq=\log_a p-\log_a q$, \ $\log_a p^n=n\log_a p$.")),
     tasks(2, [RR("4+5-6=", "3"), RR("3+3+9=", "15"), RR("4-2+2=", "4"), RR(r"\log_6 36=", "2"), RR(r"\log_2 8=", "3"), RR(r"\log 100=", "2"), RR(r"\log_3 27=", "3"), RR(r"\log(25\cdot4)=", "2")])),
 (2, T(r"Considerant $\log2=0,301$ i $\log3=0,477$, calcula sense calculadora:", r"Considerando $\log2=0,301$ y $\log3=0,477$, calcula sin calculadora:")
     + tasks(5, [r"$\log4$", r"$\log6$", r"$\log5$", r"$\log12$", r"$\log1,5$", r"$\log0,02$", r"$\log3,6$", r"$\log\sqrt3$", r"$\log0,\widehat3$", r"$\log45$"]),
     tasks(2, [RR(r"2\log2=", "0,602"), RR(r"\log2+\log3=", "0,778"), RR(r"\log\tfrac{10}{2}=1-\log2=", "0,699"), RR(r"2\log2+\log3=", "1,079"), RR(r"\log\tfrac32=\log3-\log2=", "0,176"),
               RR(r"\log\tfrac{2}{100}=\log2-2=", "-1,699"), RR(r"\log\tfrac{36}{10}=2\log6-1=", "0,556"), RR(r"\tfrac12\log3=", "0,2385"), RR(r"\log\tfrac13=-\log3=", "-0,477"), RR(r"\log\tfrac{90}{2}=2\log3+1-\log2=", "1,653")])),
 (2, T(r"Si $\log_3 2=0,631$ i $\log_3 5=1,465$, calcula $\log_3 150$ i $\log_3\frac{10}{9}$.", r"Si $\log_3 2=0,631$ y $\log_3 5=1,465$, calcula $\log_3 150$ y $\log_3\frac{10}{9}$."),
     tasks(1, [RR(r"\log_3150=\log_3(2\cdot3\cdot5^2)=0,631+1+2\cdot1,465=", "4,561"), RR(r"\log_3\tfrac{10}{9}=\log_32+\log_35-2=", "0,096")])),
 (2, T(r"Pren logaritmes decimals i desenvolupa les expressions:", r"Toma logaritmos decimales y desarrolla las expresiones:")
     + tasks(2, [r"$P=10x^3y$", r"$Q=\dfrac{100x^2}{x+y}$", r"$R=\dfrac{x^2\sqrt y}{z^3}$", r"$S=\sqrt[3]{a^2b}$"]),
     tasks(1, [R(r"\log P=1+3\log x+\log y"), R(r"\log Q=2+2\log x-\log(x+y)"), R(r"\log R=2\log x+\tfrac12\log y-3\log z"), R(r"\log S=\tfrac23\log a+\tfrac13\log b")])),
 (2, T(r"Expressa el valor de $E$ en cada cas sense que apareguen logaritmes:", r"Expresa el valor de $E$ en cada caso sin que aparezcan logaritmos:")
     + tasks(1, [r"$\log E=2-2\log x+\log y$", r"$\log E=3\log2-4\log x+3\log y$", r"$\log E=\log(x-2y)+\log(x+y)$", r"$\log E=\frac12\log x+\log3$", r"$\log E=1+\log a-2\log b$"]),
     tasks(2, [R(r"E=\frac{100y}{x^2}"), R(r"E=\frac{8y^3}{x^4}"), R(r"E=(x-2y)(x+y)"), R(r"E=3\sqrt x"), R(r"E=\frac{10a}{b^2}")])),
]))

# =====================================================================
# 9. Problemes
t45 = math.log(1.5) / math.log(1.03); t46 = math.log(0.4) / math.log(0.85); t47 = math.log(1.2) / math.log(1.02); t48 = 9 / lg(2)
cn([round(t45, 1), round(t46, 2), round(t47, 2), round(t48, 1)], [13.7, 5.64, 9.21, 29.9])
ck([math.ceil(t45), math.ceil(t46), math.ceil(t47), math.ceil(t48)], [14, 6, 10, 30])
CHK.append((abs(5.7 - 4) > 1.5 and math.log(10, 3) < 3 < math.log(10, 2), 'nevera i ordre'))
S.append((T("Problemes", "Problemas"), [
 (2, T(r"La temperatura $T$ d'una nevera ha de ser de $4\,^\circ$C amb un marge d'error de $1,5\,^\circ$C. Escriu aquesta condició amb un valor absolut i com a interval. És acceptable una lectura de $5,7\,^\circ$C?",
       r"La temperatura $T$ de una nevera tiene que ser de $4\,^\circ$C con un margen de error de $1,5\,^\circ$C. Escribe esta condición con un valor absoluto y como intervalo. ¿Es aceptable una lectura de $5,7\,^\circ$C?"),
     R(r"|T-4|\le1,5") + T(r", és a dir, $T\in", r", es decir, $T\in") + R(r"[2,5;\ 5,5]").strip('$') + T(r"$. Una lectura de $5,7\,^\circ$C \rest{no és acceptable}: $|5,7-4|=1,7>1,5$.", r"$. Una lectura de $5,7\,^\circ$C \rest{no es aceptable}: $|5,7-4|=1,7>1,5$.")),
 (2, T(r"Un quadrat té una àrea de $50\ \text{cm}^2$. Calcula'n el costat i la diagonal en forma de radical simplificat.", r"Un cuadrado tiene un área de $50\ \text{cm}^2$. Calcula su lado y su diagonal en forma de radical simplificado."),
     T(r"Costat: $\sqrt{50}=", r"Lado: $\sqrt{50}=") + R(r"5\sqrt2\ \text{cm}").strip('$') + r"$. Diagonal: $\sqrt2\cdot5\sqrt2=" + R(r"10\ \text{cm}").strip('$') + T(r"$ (o bé $\sqrt{50+50}=10$).", r"$ (o bien $\sqrt{50+50}=10$).")),
 (2, T(r"Ingressem 2\,000 € en un compte al 3\,\% d'interès compost anual. Quants anys han de passar, com a mínim, perquè hi haja 3\,000 €?",
       r"Ingresamos 2\,000 € en una cuenta al 3\,\% de interés compuesto anual. ¿Cuántos años tienen que pasar, como mínimo, para que haya 3\,000 €?"),
     r"$2000\cdot1,03^t=3000\Rightarrow1,03^t=1,5\Rightarrow t=\dfrac{\log1,5}{\log1,03}\approx13,7$. " + T("Calen ", "Hacen falta ") + R(T(r"14\ \text{anys}", r"14\ \text{años}")) + "."),
 (2, T(r"Un cotxe costa 20\,000 € i perd un 15\,\% del seu valor cada any. Quants anys han de passar perquè valga menys de 8\,000 €?",
       r"Un coche cuesta 20\,000 € y pierde un 15\,\% de su valor cada año. ¿Cuántos años tienen que pasar para que valga menos de 8\,000 €?"),
     r"$20000\cdot0,85^t=8000\Rightarrow0,85^t=0,4\Rightarrow t=\dfrac{\log0,4}{\log0,85}\approx5,64$. " + T("Valdrà menys de 8\\,000 € a partir de ", "Valdrá menos de 8\\,000 € a partir de ") + R(T(r"6\ \text{anys}", r"6\ \text{años}")) + "."),
 (2, T(r"Una ciutat té 50\,000 habitants i la població creix un 2\,\% cada any. Quants anys tardarà a arribar a 60\,000 habitants?",
       r"Una ciudad tiene 50\,000 habitantes y la población crece un 2\,\% cada año. ¿Cuántos años tardará en llegar a 60\,000 habitantes?"),
     r"$50000\cdot1,02^t=60000\Rightarrow1,02^t=1,2\Rightarrow t=\dfrac{\log1,2}{\log1,02}\approx9,21$. " + T("Caldran ", "Harán falta ") + R(T(r"10\ \text{anys}", r"10\ \text{años}")) + "."),
 (2, T(r"Un bacteri es duplica cada hora si té les condicions òptimes. Quantes hores hauran de passar perquè un bacteri inicial cree una colònia de mil milions de bacteris?",
       r"Una bacteria se duplica cada hora si tiene las condiciones óptimas. ¿Cuántas horas tendrán que pasar para que una bacteria inicial cree una colonia de mil millones de bacterias?"),
     r"$2^t=10^9\Rightarrow t=\dfrac{9}{\log2}\approx29,9$. " + T("Hauran de passar unes ", "Tendrán que pasar unas ") + R(T(r"30\ \text{hores}", r"30\ \text{horas}")) + "."),
 (1, T(r"Troba l'error en cadascun d'aquests càlculs i corregeix-lo:", r"Encuentra el error en cada uno de estos cálculos y corrígelo:")
     + tasks(2, [r"$\sqrt{9+16}=3+4=7$", r"$-3^2=9$", r"$\log(5+5)=\log5+\log5$", r"$2^{-3}=-8$", r"$\sqrt2+\sqrt3=\sqrt5$", r"$[1, 3)\cap(3, 5]=\{3\}$"]),
     tasks(2, [T(r"L'arrel no es reparteix en sumes: ", r"La raíz no se reparte en sumas: ") + R(r"\sqrt{25}=5"), T(r"L'exponent només afecta el 3: ", r"El exponente solo afecta al 3: ") + R("-3^2=-9"),
               T(r"La propietat és per al producte: ", r"La propiedad es para el producto: ") + R(r"\log10=1"), R(r"2^{-3}=\frac18"),
               T(r"No són semblants ($3,15\neq2,24$).", r"No son semejantes ($3,15\neq2,24$)."),
               T(r"El 3 no és de cap dels dos: ", r"El 3 no es de ninguno de los dos: ") + R(r"\varnothing")])),
 (3, T(r"Sense calculadora, ordena de menor a major $\log_2 10$, \ $3$ \ i \ $\log_3 10$. Justifica-ho.", r"Sin calculadora, ordena de menor a mayor $\log_2 10$, \ $3$ \ y \ $\log_3 10$. Justifícalo."),
     r"$2^3=8<10\Rightarrow\log_210>3$; \ $3^2=9<10<27=3^3\Rightarrow2<\log_310<3$. " + T("Per tant, ", "Por tanto, ") + R(r"\log_310<3<\log_210") + "."),
]))
ck(cap(P('[1,3)'), P('(3,5]')), [])
cn([r2 + r3, r5], [3.146, 2.236], 1e-3)

bad = [m for ok, m in CHK if not ok]
assert not bad, bad[:5]
NEX = sum(len(s_[1]) for s_ in S)
assert [len(x[1]) for x in S] == [5, 5, 5, 4, 12, 3, 4, 5, 8], [len(x[1]) for x in S]

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("nombres reals, fracció generatriu, intervals, semirectes, valor absolut, unió i intersecció, radicals, forma exponencial, índex comú, racionalització, logaritmes",
       "números reales, fracción generatriz, intervalos, semirrectas, valor absoluto, unión e intersección, radicales, forma exponencial, índice común, racionalización, logaritmos")
if not ES:
    pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: 'pdfkeywords={' + KW + '}', pre)
    pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les CCSS I}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{''' + T('Recorda', 'Recuerda') + r''':}\ #1\end{tcolorbox}}
'''

TIT = T("Nombres reals", "Números reales")
def spc(t):
    # «, » separa elements; amb icomma la coma és un símbol normal i un «-» darrere seu seria una resta: el posem entre claus
    return re.sub(r'\$[^$]*\$', lambda mm: re.sub(r',((?:\\,|\\ |\\;|\s)+)-', r',\1{-}', mm.group(0).replace(', ', r',\, ')), t)
def build(sol):
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 1: %s' % (t, TIT), capcalera='%s · Unidad 1: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-ccss')
        cap_ = assignatura('1batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 1' if sol else 'Ficha de ejercicios · Unidad 1') + '}'
    else:
        t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                        "pdftitle={%s de la unitat 1: %s. 1r de Batxillerat CCSS}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 1: %s · 1r Batxillerat CCSS" % (t, TIT))
        assert 'Unitat 1' in p and 'unitat 1' in p
        cap_ = r'\capcalera{Matemàtiques CCSS}{1r Batx}{' + ('Solucions de la fitxa · Unitat 1' if sol else "Fitxa d'exercicis · Unitat 1") + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + cap_ + r'''{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.9cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Els resultats es donen de manera exacta (fraccions i arrels) i, quan cal, amb el valor aproximat. Pots comprovar els d'intervals, valor absolut, radicals i logaritmes amb les eines interactives dels apunts de la unitat.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Los resultados se dan de manera exacta (fracciones y raíces) y, cuando hace falta, con el valor aproximado. Puedes comprobar los de intervalos, valor absoluto, radicales y logaritmos con las herramientas interactivas de los apuntes de la unidad.")
             if sol else T(r"Resol els exercicis al quadern mostrant tots els passos. Dona els resultats de manera exacta (fraccions i arrels simplificades, sense arrels al denominador) i, si cal, també aproximats. Escriu els conjunts com a intervals i representa'ls a la recta real.",
                           r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. Da los resultados de manera exacta (fracciones y raíces simplificadas, sin raíces en el denominador) y, si hace falta, también aproximados. Escribe los conjuntos como intervalos y represéntalos en la recta real."))
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + intro + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, spc(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = ('t1-fitxa-solucions' if sol else 't1-fitxa-exercicis') + ('-es' if ES else '') + '.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(NEX, T('exercicis;', 'ejercicios;'), len(CHK), T('comprovacions', 'comprobaciones'))
