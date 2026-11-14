# Versió en castellà de genera.py. Genera t1-fitxa-exercicis-es.tex i t1-fitxa-solucions-es.tex. Original: genera t1-fitxa-exercicis.tex i t1-fitxa-solucions.tex (1r Batxillerat MI, Unitat 1: Nombres reals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Els exercicis 1-42 són els de la fitxa del departament (amb la mateixa numeració); la secció 6 n'afegeix 12 de nous.
# Les solucions numèriques es calculen ací amb fraccions exactes (decimals periòdics, operacions combinades, potències,
# intervals) i CHK (al final) les compara amb els valors escrits. Les solucions d'intervals porten la recta dibuixada amb TikZ.
# Dins de les fórmules, «, » (coma i espai) separa elements (intervals, coordenades) i «2,45» és un decimal (icomma).
# Ús: python3 genera.py && pdflatex t1-fitxa-exercicis.tex (dues vegades) && pdflatex t1-fitxa-solucions.tex (dues vegades)
import os, re, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
INF = float('inf')

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def R(t): return r'$\res{' + t + '}$'
def tn(x):
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    return ('-' if x < 0 else '') + r'\frac{%d}{%d}' % (abs(x.numerator), x.denominator)

CHK = []
def ck(x, y):
    CHK.append((x, y)); return x

# ---------- decimals periòdics ----------
def per(ent, ante, peri):
    """valor exacte de ent,ante(peri)"""
    if not peri: return F(int(ent + ante), 10 ** len(ante))
    full, part = int(ent + ante + peri), int(ent + ante)
    return F(full - part, int('9' * len(peri) + '0' * len(ante)))

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
def cap(S, T):
    r = []
    for a, ac, b, bc in S:
        for c, cc, d, dc in T:
            r.append((max(a, c), ac if a > c else cc if c > a else ac and cc, min(b, d), bc if b < d else dc if d < b else bc and dc))
    return norm(r)
def cup(S, T): return norm(S + T)
def compl(S):
    r, a, ac = [], -INF, False
    for c, cc, d, dc in norm(S):
        r.append((a, ac, c, not cc)); a, ac = d, not dc
    r.append((a, ac, INF, False)); return norm(r)
def minus(S, T): return cap(S, compl(T))
def P(s):
    """'[-3,2)U(5,inf)' -> conjunt"""
    out = []
    for p in s.split('U'):
        m = re.match(r'^([\[\(])([^,]+),([^,]+)([\]\)])$', p.strip())
        def num(t): return -INF if t == '-inf' else INF if t == 'inf' else F(t)
        out.append((num(m.group(2)), m.group(1) == '[', num(m.group(3)), m.group(4) == ']'))
    return norm(out)
def ivt(I):
    a, ac, b, bc = I
    if a == b: return r'\{%s\}' % tn(a)
    ta = r'-\infty' if a == -INF else tn(a)
    tb = r'+\infty' if b == INF else tn(b)
    return ('[' if ac else '(') + ta + ', ' + tb + (']' if bc else ')')
def st(S): return r'\cup'.join(ivt(I) for I in norm(S)) if norm(S) else r'\varnothing'

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
    return R(st(S)) + r'\\[2pt]' + recta(S, lo, hi)

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Classificació dels nombres
e3 = [per('2', '', '7') + per('3', '', '4') - per('1', '', '1'),
      per('1', '2', '3') + per('4', '572', '') - per('2', '5', '67'),
      per('1', '', '8') + per('0', '', '1'),
      per('3', '', '45') * per('1', '23', '4') - F(5, 2)]
ck(e3, [F(46, 9), F(40066, 12375), F(2), F(397, 225)])
ck([per('1', '2', '3'), per('2', '5', '67'), per('3', '', '45'), per('1', '23', '4')], [F(37, 30), F(1271, 495), F(38, 11), F(1111, 900)])
S.append(("Clasificación de los números", [
 (1, r"Indica el menor de los conjuntos numéricos a los que pertenecen los números siguientes:" + tasks(5, [r"$\sqrt5$", r"$2$", r"$-3$", r"$24/6$", r"$2,45$", r"$-1,33$", r"$2,3\widehat{45}$", r"$\pi$", r"$5/12$", r"$0$"]),
     tasks(5, [R(r"\mathbb I"), R(r"\mathbb N"), R(r"\mathbb Z"), R(r"4\in\mathbb N"), R(r"\mathbb Q"), R(r"\mathbb Q"), R(r"\mathbb Q"), R(r"\mathbb I"), R(r"\mathbb Q"), R(r"\mathbb N")])),
 (1, r"Razona si las afirmaciones siguientes son verdaderas o falsas:" + tasks(1, [r"Todo número entero es racional.", r"Todo número decimal se puede expresar en forma de fracción.",
      r"Todo número natural se puede escribir como una fracción.", r"Si se suman dos números racionales, el resultado es siempre un número racional.",
      r"Si se multiplican dos números racionales no enteros, el resultado es siempre un número racional no entero."]),
     tasks(1, [r"\rest{Verdadera}: todo entero $n$ se puede escribir como $\frac n1$.", r"\rest{Falsa}: solo los exactos y los periódicos; $\pi=3,1415\ldots$ no.",
               r"\rest{Verdadera}: por ejemplo, $5=\frac{10}{2}$.", r"\rest{Verdadera}: $\frac ab+\frac cd=\frac{ad+bc}{bd}$, que es una fracción.",
               r"\rest{Falsa}: $\frac32\cdot\frac23=1$, o bien $2,5\cdot0,4=1$."])),
 (2, r"Realiza las operaciones siguientes escribiendo previamente los números en forma de fracción:" + tasks(2, [r"$2,\widehat7+3,\widehat4-1,\widehat1$", r"$1,\widehat8+0,\widehat1$", r"$1,2\widehat3+4,572-2,5\widehat{67}$", r"$3,\widehat{45}\cdot1,23\widehat4-2,5$"])
     + recorda(r"Fracción generatriz: en el numerador, el número sin coma menos la parte no periódica; en el denominador, tantos 9 como cifras tiene el período y tantos 0 como cifras tiene el anteperíodo."),
     tasks(2, [r"$\frac{25}{9}+\frac{31}{9}-\frac{10}{9}=" + R(tn(e3[0])).strip('$') + "$", r"$\frac{17}{9}+\frac19=" + R(tn(e3[2])).strip('$') + "$",
               r"$\frac{37}{30}+\frac{1143}{250}-\frac{1271}{495}=" + R(tn(e3[1])).strip('$') + "$", r"$\frac{38}{11}\cdot\frac{1111}{900}-\frac52=" + R(tn(e3[3])).strip('$') + "$"])
     + r"(En la ficha original el apartado b) ponía $1\widehat8$; lo hemos leído como $1,\widehat8$.)"),
]))

# =====================================================================
# 2. Valor absolut
S.append(("Valor absoluto", [
 (2, r"Averigua para qué valores de $x$ se cumplen las desigualdades siguientes:" + tasks(3, [r"$|x|<3$", r"$|x|\ge3$", r"$|x-2|\le3$", r"$|x|\le5$", r"$|x-4|<2$", r"$|x-4|\le2$", r"$|x-4|>2$",
      r"$|2x-1|>1$", r"$|-5x+3|<7$", r"$\left|\frac{3x}{2}-6\right|>10$", r"$\left|1-\frac{2x}{5}\right|\le3$", r"$|-5x+25|\le-2$", r"$\left|x+\frac34\right|>-1$"])
     + recorda(r"Si $r>0$: \ $|A|<r\iff -r<A<r$ \quad y \quad $|A|>r\iff A<-r$ o $A>r$. Al multiplicar o dividir por un número negativo, la desigualdad cambia de sentido."),
     tasks(2, [RI('(-3,3)'), RI('(-inf,-3]U[3,inf)'), RI('[-1,5]'), RI('[-5,5]'), RI('(2,6)'), RI('[2,6]'), RI('(-inf,2)U(6,inf)'), RI('(-inf,0)U(1,inf)'),
               RI('(-4/5,2)'), RI('(-inf,-8/3)U(32/3,inf)'), RI('[-5,10]'), R(r"\varnothing") + r" (un valor absoluto no puede ser negativo)", R(r"\mathbb R") + r" (siempre se cumple)"])),
]))

# =====================================================================
# 3. Intervals i entorns
A9, B9, C9, D9, E9, F9 = P('[-3,2]'), P('[0,5]'), P('[2,inf)'), P('(0,10)'), P('(2,7/2)'), P('(1,5/2)')
r9 = [cap(A9, B9), cap(A9, D9), cup(A9, B9), cap(cup(A9, B9), C9), cap(E9, F9), minus(F9, C9), cap(minus(B9, E9), A9), cap(cup(A9, B9), cap(E9, F9)), minus(cap(A9, B9), cup(D9, F9))]
ck(r9, [P('[0,2]'), P('(0,2]'), P('[-3,5]'), P('[2,5]'), P('(2,5/2)'), P('(1,2)'), P('[0,2]'), P('(2,5/2)'), P('[0,0]')])
A10, B10, C10, D10, E10 = P('(-inf,-4]'), P('[2,5)'), P('[-6,1]'), P('[0,inf)'), P('(-2,-1)')
r10 = [cup(A10, B10), cap(B10, C10), cap(D10, C10), cup(A10, cap(B10, D10)), cap(B10, cup(A10, E10)), cap(cap(B10, D10), E10), cap(cup(B10, C10), A10), minus(D10, B10), minus(C10, E10), minus(cup(A10, C10), cap(C10, E10))]
ck(r10, [P('(-inf,-4]U[2,5)'), [], P('[0,1]'), P('(-inf,-4]U[2,5)'), [], [], P('[-6,-4]'), P('[0,2)U[5,inf)'), P('[-6,-2]U[-1,1]'), P('(-inf,-2]U[-1,1]')])
S.append(("Intervalos y entornos", [
 (1, r"Completa la tabla siguiente:" + '\n\n\\begin{center}\\renewcommand{\\arraystretch}{1.5}\\begin{tabular}{|C{4.6cm}|C{3.2cm}|C{6cm}|}\\hline\\rowcolor{soft}\\textbf{Desigualdad} & \\textbf{Intervalo} & \\textbf{Representación}\\\\\\hline'
     r'$\{x\in\mathbb R\ /\ x<-3\}$ & & \\\hline & $x\in[-2, 4)$ & \\\hline $\{x\in\mathbb R\ /\ -5<x\le-3\}$ & & \\\hline & $x\in(4, \infty)$ & \\\hline\end{tabular}\end{center}',
     tasks(2, [r"$x<-3$: " + RI('(-inf,-3)'), r"$-2\le x<4$: " + RI('[-2,4)'), r"$-5<x\le-3$: " + RI('(-5,-3]'), r"$x>4$: " + RI('(4,inf)')])),
 (1, r"Representa los conjuntos numéricos siguientes:" + tasks(3, [r"Números mayores que 3.", r"$\{x\in\mathbb R/2\le x\le5\}$", r"$\{x\in\mathbb R/3<x\le7\}$", r"Números menores que 1 excluyendo el 0.",
      r"$(-3, -1)$", r"$[4, +\infty)$", r"Números reales positivos.", r"$\{x\in\mathbb R/-2\le x<5\}$", r"$3x-2\le7$", r"$-4x+1>8$", r"$|x|<5$", r"$|5x-6|\ge3$"]),
     tasks(2, [RI('(3,inf)'), RI('[2,5]'), RI('(3,7]'), RI('(-inf,0)U(0,1)'), RI('(-3,-1)'), RI('[4,inf)'), RI('(0,inf)'), RI('[-2,5)'), RI('(-inf,3]'), RI('(-inf,-7/4)'), RI('(-5,5)'), RI('(-inf,3/5]U[9/5,inf)')])),
 (1, r"Expresa como desigualdad, como intervalo y representa:" + tasks(2, [r"$x$ es menor que $-5$.", r"3 es menor o igual que $x$.", r"$x$ está comprendido entre $-5$ y 1.", r"$x$ está entre $-2$ y 0, ambos incluidos."]),
     tasks(2, [r"$x<-5$: " + RI('(-inf,-5)'), r"$x\ge3$: " + RI('[3,inf)'), r"$-5<x<1$: " + RI('(-5,1)'), r"$-2\le x\le0$: " + RI('[-2,0]')])),
 (1, r"Escribe la desigualdad que verifica todo número $x$ que pertenece a estos intervalos y represéntalos gráficamente:" + tasks(4, [r"$[-2, 7]$", r"$[13, +\infty)$", r"$(-\infty, 0)$", r"$(-3, 0]$",
      r"$\left[\frac32, 6\right)$", r"$(-\infty, +\infty)$", r"$(1, 6)$", r"$(0, 4]$", r"$(-\infty, 2)$", r"$\left[2, \frac43\right]$", r"$(-1, +\infty)$", r"$\left(2, \frac72\right)$"]),
     tasks(2, [r"$-2\le x\le7$ " + recta(P('[-2,7]')), r"$x\ge13$ " + recta(P('[13,inf)')), r"$x<0$ " + recta(P('(-inf,0)')), r"$-3<x\le0$ " + recta(P('(-3,0]')),
               r"$\frac32\le x<6$ " + recta(P('[3/2,6)')), r"$x\in\mathbb R$ " + recta(P('(-inf,inf)'), -3, 3), r"$1<x<6$ " + recta(P('(1,6)')), r"$0<x\le4$ " + recta(P('(0,4]')),
               r"$x<2$ " + recta(P('(-inf,2)')), r"Ninguno: $2>\frac43$, es $\res{\varnothing}$ (¿quizá era $\left[\frac43, 2\right]$?).", r"$x>-1$ " + recta(P('(-1,inf)')), r"$2<x<\frac72$ " + recta(P('(2,7/2)'))])),
 (2, r"Dados los intervalos $A=[-3, 2]$, $B=[0, 5]$, $C=[2, +\infty)$, $D=(0, 10)$, $E=\left(2, \frac72\right)$ y $F=\left(1, \frac52\right)$, calcula:"
     + tasks(3, [r"$A\cap B$", r"$A\cap D$", r"$A\cup B$", r"$(A\cup B)\cap C$", r"$E\cap F$", r"$F-C$", r"$(B-E)\cap A$", r"$(A\cup B)\cap(E\cap F)$", r"$(A\cap B)-(D\cup F)$"]),
     tasks(3, [R(st(x)) for x in r9])),
 (2, r"Dados los intervalos $A=\,]-\infty, -4]$, $B=[2, 5[$, $C=[-6, 1]$, $D=[0, +\infty[$ y $E=\,]-2, -1[$, calcula:"
     + tasks(3, [r"$A\cup B$", r"$B\cap C$", r"$D\cap C$", r"$A\cup(B\cap D)$", r"$B\cap(A\cup E)$", r"$B\cap D\cap E$", r"$(B\cup C)\cap A$", r"$D-B$", r"$C-E$", r"$(A\cup C)-(C\cap E)$"]),
     tasks(2, [R(st(x)) for x in r10])),
 (1, r"Escribe en forma de intervalo los números que verifican las desigualdades siguientes:" + tasks(4, [r"$x<3$ y $x\ge5$", r"$x>0$ y $x<4$", r"$x\le-1$ y $x>1$", r"$x<3$ y $x\ge-2$"]),
     tasks(4, [R(r"\varnothing"), R(st(cap(P('(-inf,4)'), P('(0,inf)')))), R(r"\varnothing"), R(st(cap(P('(-inf,3)'), P('[-2,inf)'))))])),
]))

# =====================================================================
# 4. Potències i arrels
e16 = [F(3, 4) ** 2 - F(5, 8),
       F(-1, 2) ** 2 + F(3, 2) ** 3 - F(5, 3) ** 2,
       (F(5, 6) - F(4, 5)) ** -1 * F(2, 3) ** -1 + F(1, 2) ** -1,
       (F(5, 2) + F(2, 5)) ** -1 / F(7, 3) ** -1 - F(4, 3) ** 2,
       (F(2, 3) + 4) / per('1', '', '7') - 2,
       (1 - F(3, 4)) ** -2 * (per('3', '', '42') - 1) + 4,
       (3 - F(4, 5) * F(23, 10)) ** -1 + per('3', '2', '4'),
       ((F(-3, 5) ** 3 * F(-3, 5) ** 2) ** 3 / F(-3, 5) ** 15) - F(4, 3) ** 3 * F(3, 2) ** 4,
       (((F(1, 3) - 1) * (-1 + F(1, 4))) ** 2 / (2 - F(3, 2)) ** 2) + (F(-1, 5) ** 2 * F(-5, 3)) * (F(5, 4) + 10),
       ((F(3, 2) - 4) / (1 - F(8, 3)) + F(1, 2)) ** 4 - (1 + F(2, 3)) ** 2 * (1 - F(2, 5)) ** 3]
ck(e16, [F(-1, 16), F(61, 72), F(47), F(-254, 261), F(5, 8), F(1412, 33), F(5359, 1305), F(-11), F(1, 4), F(77, 5)])
e17 = [F(3) ** -2, F(-3) ** -2, F(-2) ** -1, None, F(-1, 2) ** -1, F(2, 3) ** -2, F(-3, 4) ** -2, (2 - F(1, 2)) ** -1, (F(1, 5) - 2) ** -2, (F(16, 5) - F(12, 10)) ** -3, (F(3, 4) - F(5, 6)) ** -2, (F(13, 10) - F(4, 5)) ** -2]
ck(e17, [F(1, 9), F(1, 9), F(-1, 2), None, F(-2), F(9, 4), F(16, 9), F(2, 3), F(25, 81), F(1, 8), F(144), F(4)])
ck([F(1, 3) ** 2 * F(3, 5), F(-1, 3) ** 3 * F(6, 5) * -5, F(3, 4) / F(5, 6), F(-3, 2) / F(3, 4), F(9 * -2, 6), F(-2 * (-3) ** 3, 9)], [F(1, 15), F(2, 9), F(9, 10), F(-2), F(-3), F(6)])
ck(F(32 ** 6 * 27 ** 4 * 30 ** 3, 10 ** 5 * 15 ** 14), F(2 ** 28 * 3, 5 ** 16))
ck(F(48 ** 3 * 9 ** 2 * 36 ** 5, 8), F(2 ** 19 * 3 ** 17))
S.append(("Potencias y raíces", [
 (1, r"Calcula las potencias siguientes:" + tasks(5, [r"$2^3$", r"$(-3)^2$", r"$-3^2$", r"$(-0,15)^2$", r"$(0,01)^4$", r"$\left(\frac15\right)^2$", r"$\left(-\frac32\right)^2$", r"$\left(-\frac23\right)^3$", r"$\left(-\frac13\right)^4$", r"$(-0,003)^5$"]),
     tasks(5, [R("8"), R("9"), R("-9"), R("0,0225"), R("10^{-8}"), R(r"\frac{1}{25}"), R(r"\frac94"), R(r"-\frac{8}{27}"), R(r"\frac{1}{81}"), R(r"-2,43\cdot10^{-13}")])),
 (1, r"Reduce las expresiones a una sola potencia, aplicando las propiedades de las potencias:" + tasks(2, [r"$(-3)^2\cdot(-3)^3\cdot(-3)$", r"$\left(\frac12\right)^2\cdot\left(\frac12\right)^5\cdot\left(\frac12\right)^3\cdot\frac12$",
      r"$[(-3)^2]^3$", r"$(-3^2)^3$", r"$(-1^4)^3$", r"$\left[\left(\frac12\right)^2\right]^5$", r"$\{[(-3^2)^3]^5\}^3$", r"$\{[(-0,1)^2]^3\}^3$", r"$(-3)^6:(-3)^6$", r"$(-4)^5:(-4)^3$",
      r"$\left(-\frac23\right)^3:\left(-\frac23\right)$", r"$(\sqrt x)^5:(\sqrt x)^3$", r"$\left(\frac13\right)^{-2}\cdot3^7\cdot3^{-8}\cdot\left(\frac13\right)^3$", r"$\left[\left(\frac23\right)^5\right]^{-1}\cdot\left(\frac32\right)\cdot\left(\frac23\right)^{-3}$"]),
     tasks(2, [R("(-3)^6"), R(r"\left(\frac12\right)^{11}"), R("(-3)^6=3^6"), R("(-9)^3=-3^6"), R("(-1)^3=-1"), R(r"\left(\frac12\right)^{10}"), R("(-9)^{45}=-3^{90}"), R("(-0,1)^{18}=0,1^{18}"),
               R("(-3)^0=1"), R("(-4)^2"), R(r"\left(-\frac23\right)^2"), R(r"(\sqrt x)^2=x"), R("3^{2+7-8-3}=3^{-2}"), R(r"\left(\frac23\right)^{-9}=\left(\frac32\right)^9")])),
 (2, r"Simplifica al máximo las expresiones siguientes:" + tasks(3, [r"$\dfrac{2^7\cdot2^{-8}}{2^4\cdot2^5}$", r"$\dfrac{a^4\cdot(b\cdot c)^6\cdot a^{-2}}{b^3\cdot c^5}$", r"$\dfrac{(p\cdot q)^3\cdot(p^2\cdot q^3)^2}{(p\cdot q)^{-2}}$",
      r"$\dfrac{32^6\cdot27^4\cdot30^3}{10^5\cdot15^{14}}$", r"$\dfrac18\cdot48^3\cdot9^2\cdot36^5$", r"$\dfrac{2^{-3}\cdot5^{\frac12}\cdot(2^4)^{\frac12}}{5^{-\frac32}\cdot2^{-5}}$"]),
     tasks(3, [R("2^{-10}"), R("a^2b^3c"), R("p^9q^{11}"), R(r"\frac{2^{28}\cdot3}{5^{16}}"), R(r"2^{19}\cdot3^{17}"), R(r"2^4\cdot5^2=400")])),
 (2, r"Calcula de dos formas (operando primero dentro del corchete, o aplicando las propiedades) las potencias siguientes:" + tasks(3, [r"$\left[\left(\frac13\right)^2\cdot\left(\frac35\right)\right]^3$",
      r"$\left(\frac34:\frac56\right)^3$", r"$\left[\dfrac{3^2\cdot(-2)}{6}\right]^2$", r"$\left[\left(-\frac13\right)^3\cdot\left(\frac65\right)\cdot(-5)\right]^4$", r"$\left[\left(-\frac32\right):\left(\frac34\right)\right]^5$", r"$\left[\dfrac{(-2)\cdot(-3)^3}{9}\right]^2$"]),
     tasks(3, [R(r"\left(\frac{1}{15}\right)^3=\frac{1}{3375}"), R(r"\left(\frac{9}{10}\right)^3=\frac{729}{1000}"), R("(-3)^2=9"), R(r"\left(\frac29\right)^4=\frac{16}{6561}"), R("(-2)^5=-32"), R("6^2=36")])),
 (2, r"Calcula el valor de las expresiones siguientes:" + tasks(2, [r"$\left(\frac34\right)^2-\frac58$", r"$\left(-\frac12\right)^2+\left(\frac32\right)^3-\left(\frac53\right)^2$",
      r"$\left(\frac56-\frac45\right)^{-1}\cdot\left(\frac23\right)^{-1}+\left(\frac12\right)^{-1}$", r"$\left(\frac52+\frac25\right)^{-1}:\left(\frac73\right)^{-1}-\left(\frac43\right)^2$",
      r"$\left(\frac23+4\right):1,\widehat7-2$", r"$\left(1-\frac34\right)^{-2}\cdot\left(3,\widehat{42}-1\right)+4$", r"$\left(3-\frac45\cdot2,3\right)^{-1}+3,2\widehat4$"])
     + tasks(1, [r"$\left\{\left[\left(-\frac35\right)^3\cdot\left(-\frac35\right)^2\right]^3:\left(-\frac35\right)^{15}\right\}-\left(\frac43\right)^3\cdot\left(\frac32\right)^4$",
      r"$\left\{\left[\left(\frac13-1\right)\cdot\left(-1+\frac14\right)\right]^2:\left(2-\frac32\right)^2\right\}+\left[\left(-\frac15\right)^2\cdot\left(-\frac53\right)\right]\cdot\left(\frac54+10\right)$",
      r"$\left[\left(\frac32-4\right):\left(1-\frac83\right)+\frac12\right]^4-\left(1+\frac23\right)^2\cdot\left(1-\frac25\right)^3$"]).replace(r'\begin{tasks}(1)', r'\begin{tasks}[start=8](1)'),
     tasks(4, [R(tn(x)) for x in e16])),
 (1, r"Calcula las potencias de exponente negativo siguientes:" + tasks(4, [r"$3^{-2}$", r"$(-3)^{-2}$", r"$(-2)^{-1}$", r"$(\sqrt3)^{-1}$", r"$\left(-\frac12\right)^{-1}$", r"$\left(\frac23\right)^{-2}$",
      r"$\left(-\frac34\right)^{-2}$", r"$\left(2-\frac12\right)^{-1}$", r"$\left(\frac15-2\right)^{-2}$", r"$\left(\frac{16}{5}-1,2\right)^{-3}$", r"$\left(\frac34-\frac56\right)^{-2}$", r"$\left(1,3-\frac45\right)^{-2}$"]),
     tasks(4, [R(r"\frac{\sqrt3}{3}") if x is None else R(tn(x)) for x in e17])),
 (1, r"Calcula el valor de los radicales siguientes, justificando la respuesta:" + tasks(5, [r"$\sqrt{16}$", r"$\sqrt[3]{-8}$", r"$\sqrt[5]{32}$", r"$\sqrt[3]{\frac{27}{8}}$", r"$\sqrt[3]{0,064}$"]),
     tasks(5, [R("4") + r" ($4^2=16$)", R("-2") + r" ($(-2)^3=-8$)", R("2") + r" ($2^5=32$)", R(r"\frac32"), R("0,4")])),
 (1, r"Simplifica al máximo posible los radicales siguientes:" + tasks(5, [r"$\sqrt[3]{4a^4}$", r"$\sqrt[15]{8a^3}$", r"$\sqrt[6]{0,027}$", r"$\sqrt[8]{16a^4}$", r"$\sqrt[3]{a^2b^5}$"]),
     tasks(5, [R(r"a\sqrt[3]{4a}"), R(r"\sqrt[5]{2a}"), R(r"\sqrt{0,3}"), R(r"\sqrt{2a}"), R(r"b\sqrt[3]{a^2b^2}")])),
 (2, r"Reduce los radicales de cada apartado a mínimo común índice:" + tasks(3, [r"$\sqrt[3]{n^2},\ \sqrt[4]{m^3},\ \sqrt[6]{n^5}$", r"$\sqrt{a^3},\ \sqrt[4]{m},\ \sqrt[5]{n^5},\ \sqrt[10]{a^3}$", r"$\sqrt[3]{5xy^2},\ \sqrt{6x^3z},\ \sqrt[6]{\frac{3xy^3}{2z}}$"]),
     tasks(1, [R(r"\sqrt[12]{n^8},\ \sqrt[12]{m^9},\ \sqrt[12]{n^{10}}"), R(r"\sqrt[20]{a^{30}},\ \sqrt[20]{m^5},\ \sqrt[20]{n^{20}},\ \sqrt[20]{a^6}"), R(r"\sqrt[6]{25x^2y^4},\ \sqrt[6]{216x^9z^3},\ \sqrt[6]{\frac{3xy^3}{2z}}")])),
 (2, r"Realiza las operaciones indicadas:" + tasks(2, [r"$\sqrt{1+\sqrt{6+\sqrt{5+\sqrt{16}}}}$", r"$\sqrt{3a^2+\sqrt{6a^4-\sqrt{25a^8}}}$", r"$\sqrt{25\sqrt{81\sqrt{256}}}$", r"$\left(\sqrt{a\sqrt{b\sqrt{c\sqrt d}}}\right)^{32}$"]),
     tasks(2, [R("2"), R("2|a|"), R("30"), R("a^{16}b^8c^4d^2")])),
 (1, r"Calcula las raíces siguientes por el método más fácil:" + tasks(3, [r"$\sqrt[3]{8\cdot27\cdot64}$", r"$\sqrt[5]{243\cdot32\cdot0,00001}$", r"$\sqrt{49\cdot121\cdot169}$", r"$\sqrt{25:0,0001}$",
      r"$\sqrt[3]{8:0,064}$", r"$\sqrt[4]{20736:256}$", r"$\sqrt[5]{243:32}$", r"$\sqrt{49^3}$", r"$\sqrt[3]{0,064^2}$", r"$\sqrt[3]{2197^4}$", r"$\sqrt[4]{6561^3}$", r"$\sqrt[5]{0,00032^4}$"]),
     tasks(4, [R("24"), R("0,6"), R("1001"), R("500"), R("5"), R("3"), R(r"\frac32"), R("343"), R("0,16"), R("28561"), R("729"), R("0,0016")])),
 (2, r"Extrae todos los factores posibles de cada uno de los radicales siguientes:" + tasks(4, [r"$\sqrt8$", r"$\sqrt{12}$", r"$\sqrt[3]{16}$", r"$\sqrt[3]{54}$", r"$\sqrt[5]{64}$", r"$\sqrt{\frac{27}{4}}$",
      r"$\sqrt[5]{\frac{5x^{10}}{y^8}}$", r"$\sqrt[3]{\frac{8x^4y^3z}{n^6}}$", r"$3\sqrt{8a^3}$", r"$2x^2y\sqrt{x^4y^3}$", r"$\frac{xy^2}{3}\sqrt{27xy^3}$", r"$\sqrt[4]{\frac{32x^6}{81y^5}}$"]),
     tasks(4, [R(r"2\sqrt2"), R(r"2\sqrt3"), R(r"2\sqrt[3]2"), R(r"3\sqrt[3]2"), R(r"2\sqrt[5]2"), R(r"\frac{3\sqrt3}{2}"), R(r"\frac{x^2}{y}\sqrt[5]{\frac{5}{y^3}}"), R(r"\frac{2xy}{n^2}\sqrt[3]{xz}"),
               R(r"6a\sqrt{2a}"), R(r"2x^4y^2\sqrt y"), R(r"xy^3\sqrt{3xy}"), R(r"\frac{2x}{3y}\sqrt[4]{\frac{2x^2}{y}}")])),
 (2, r"Introduce el coeficiente dentro del radical correspondiente y simplifica:" + tasks(4, [r"$7\sqrt a$", r"$2a\sqrt{3a}$", r"$3+\sqrt7$", r"$x\sqrt{\frac1x}$", r"$x^3y\sqrt{xy}$", r"$\frac13\sqrt[4]{\frac{27}{2}}$",
      r"$\frac32\sqrt{\frac23}$", r"$\frac2a\sqrt{\frac{ax}{2}}$", r"$\frac{3}{2xy}\sqrt{\frac{2xz}{y}}$", r"$\frac23\sqrt[3]{\frac{81}{4}}$", r"$\left(1+\frac12\right)\sqrt[3]{\frac{4}{81}}$", r"$\frac{a-b}{a+b}\sqrt{\frac{a+b}{a-b}}$", r"$(x+y)\sqrt{\frac{x-y}{x+y}}$"]),
     tasks(3, [R(r"\sqrt{49a}"), R(r"\sqrt{12a^3}"), r"No se puede: es una suma.", R(r"\sqrt x"), R(r"\sqrt{x^7y^3}"), R(r"\sqrt[4]{\frac16}"), R(r"\sqrt{\frac32}"), R(r"\sqrt{\frac{2x}{a}}"),
               R(r"\sqrt{\frac{9z}{2xy^3}}"), R(r"\sqrt[3]6"), R(r"\sqrt[3]{\frac16}"), R(r"\sqrt{\frac{a-b}{a+b}}"), R(r"\sqrt{x^2-y^2}")])),
 (2, r"Racionaliza el denominador de las expresiones siguientes:" + tasks(4, [r"$\dfrac{5}{\sqrt5}$", r"$\dfrac{2\sqrt6}{\sqrt2}$", r"$\sqrt{\dfrac52}$", r"$\dfrac{3}{\sqrt5}$", r"$\sqrt[3]{\dfrac32}$", r"$\dfrac{3}{2\sqrt[3]4}$",
      r"$\dfrac{3y}{x\sqrt y}$", r"$\dfrac{x\sqrt y}{y\sqrt x}$", r"$\dfrac{2\sqrt{12}}{5\sqrt3}$", r"$\dfrac{3\sqrt2}{\sqrt6}$", r"$\dfrac{3xy^2}{\sqrt[3]{x^2y}}$", r"$\dfrac{6(3-y)}{\sqrt[3]{(3-y)^2}}$", r"$\dfrac{-4}{\sqrt[4]3\cdot\sqrt[3]2}$"]),
     tasks(4, [R(r"\sqrt5"), R(r"2\sqrt3"), R(r"\frac{\sqrt{10}}{2}"), R(r"\frac{3\sqrt5}{5}"), R(r"\frac{\sqrt[3]{12}}{2}"), R(r"\frac{3\sqrt[3]2}{4}"), R(r"\frac{3\sqrt y}{x}"), R(r"\frac{\sqrt{xy}}{y}"),
               R(r"\frac45"), R(r"\sqrt3"), R(r"3y\sqrt[3]{xy^2}"), R(r"6\sqrt[3]{3-y}"), R(r"-\frac23\sqrt[4]{27}\,\sqrt[3]4")])),
 (2, r"Racionaliza el denominador de las expresiones siguientes:" + tasks(4, [r"$\dfrac{1}{\sqrt2+\sqrt3}$", r"$\dfrac{2}{\sqrt2-1}$", r"$\dfrac{\sqrt2}{3-\sqrt2}$", r"$\dfrac{1-\sqrt2}{1+\sqrt2}$", r"$\dfrac{\sqrt5-2}{3-2\sqrt5}$",
      r"$\dfrac{1}{\sqrt x-\sqrt y}$", r"$\dfrac{\sqrt{2y}}{\sqrt2-\sqrt y}$", r"$\dfrac{\sqrt{xy}}{2\sqrt x-3\sqrt y}$", r"$\dfrac{5}{2(\sqrt3-\sqrt2)}$", r"$\dfrac{\sqrt2}{2\sqrt2+1}$", r"$\dfrac{2+\sqrt2}{2-\sqrt2}$",
      r"$\dfrac{-\sqrt2}{\sqrt[3]2(\sqrt{125}+2)}$", r"$\dfrac{1}{\sqrt{3+\sqrt6}}$"])
     + recorda(r"Si en el denominador hay una suma o una resta con raíces, multiplicamos por el conjugado: $(a+b)(a-b)=a^2-b^2$."),
     tasks(3, [R(r"\sqrt3-\sqrt2"), R(r"2\sqrt2+2"), R(r"\frac{3\sqrt2+2}{7}"), R(r"2\sqrt2-3"), R(r"\frac{\sqrt5-4}{11}"), R(r"\frac{\sqrt x+\sqrt y}{x-y}"), R(r"\frac{2\sqrt y+y\sqrt2}{2-y}"),
               R(r"\frac{2x\sqrt y+3y\sqrt x}{4x-9y}"), R(r"\frac{5(\sqrt3+\sqrt2)}{2}"), R(r"\frac{4-\sqrt2}{7}"), R(r"3+2\sqrt2"), R(r"-\frac{\sqrt[6]2\,(5\sqrt5-2)}{121}"), R(r"\frac{(3-\sqrt6)\sqrt{3+\sqrt6}}{3}")])),
 (2, r"Comprueba que los radicales de cada apartado son semejantes:" + tasks(2, [r"$5\sqrt2,\ 3\sqrt8,\ \sqrt{18}$", r"$\sqrt{3a^2},\ \sqrt{27},\ \sqrt{\frac13},\ 2\sqrt{\frac{4}{27}}$",
      r"$\sqrt[3]{81},\ \sqrt[3]{24},\ \sqrt[6]9,\ \sqrt[3]{\frac19a^3}$", r"$3\sqrt[4]{2xy},\ \sqrt[4]{32x^5y},\ \sqrt[4]{2x^9y^5}$"]),
     tasks(2, [R(r"5\sqrt2,\ 6\sqrt2,\ 3\sqrt2"), R(r"a\sqrt3,\ 3\sqrt3,\ \frac{\sqrt3}{3},\ \frac{4\sqrt3}{9}"), R(r"3\sqrt[3]3,\ 2\sqrt[3]3,\ \sqrt[3]3,\ \frac a3\sqrt[3]3"), R(r"3\sqrt[4]{2xy},\ 2x\sqrt[4]{2xy},\ x^2y\sqrt[4]{2xy}")])),
 (1, r"Calcula y simplifica:" + tasks(3, [r"$\sqrt{25:0,01}$", r"$\sqrt[4]{9x^5y^3}:\sqrt[4]{3x^3y}$", r"$\sqrt[3]{(27x^3y^6)^5}$"]),
     tasks(3, [R("50"), R(r"\sqrt[4]{3x^2y^2}"), R(r"243x^5y^{10}")])),
 (2, r"Realiza las sumas y restas siguientes:" + tasks(2, [r"$\sqrt8+\sqrt{18}+\sqrt{32}+\sqrt{50}$", r"$\sqrt{28}+\sqrt{63}-\sqrt{175}$", r"$6\sqrt3-4\sqrt3+5\sqrt3$", r"$3\sqrt2+5\sqrt2-8\sqrt2$",
      r"$3\sqrt2-3\sqrt8+3\sqrt{18}$", r"$2a\sqrt3-\sqrt{27a^2}+a\sqrt{12}$", r"$(3+a)\sqrt5-\sqrt{125}+\sqrt{5a^2}$", r"$7\sqrt{54}-3\sqrt{18}+\sqrt{24}-\frac35\sqrt{50}-\sqrt6$",
      r"$\sqrt{\frac13}+\sqrt{27}$", r"$\sqrt{\frac12}+\sqrt2+\sqrt[4]4+\sqrt[6]8+\sqrt[4]{64}$", r"$2\sqrt{\frac34}-\sqrt{27}+\frac14\sqrt{12}-3\sqrt{\frac{75}{9}}$", r"$\sqrt{18}+5\sqrt{12}-2\sqrt2-\sqrt{243}$",
      r"$2\sqrt3+5\sqrt[6]{27}-3\sqrt{12}$", r"$5\sqrt{20}-2\sqrt{45}+\sqrt5$"]),
     tasks(4, [R(r"14\sqrt2"), R("0"), R(r"7\sqrt3"), R("0"), R(r"6\sqrt2"), R(r"a\sqrt3"), R(r"(2a-2)\sqrt5"), R(r"22\sqrt6-12\sqrt2"), R(r"\frac{10\sqrt3}{3}"), R(r"\frac{11\sqrt2}{2}"), R(r"-\frac{13\sqrt3}{2}"), R(r"\sqrt2+\sqrt3"), R(r"\sqrt3"), R(r"5\sqrt5")])
     + r"(En los apartados f) y g) suponemos $a\ge0$.)"),
 (2, r"Realiza las operaciones siguientes:" + tasks(2, [r"$\sqrt5\cdot\sqrt6$", r"$\sqrt5\cdot\sqrt[3]6$", r"$(\sqrt2)^2+(\sqrt2)^3+(\sqrt2)^4$", r"$a\cdot\sqrt a\cdot\sqrt[3]a\cdot\sqrt[4]a$", r"$(\sqrt3)^5-(\sqrt3)^3-(2\sqrt3)^2$",
      r"$2\sqrt3\left(\sqrt[3]4-\sqrt[3]3\right)$", r"$\sqrt{\frac23}\cdot\sqrt[3]{\frac23}\cdot\sqrt[4]{\frac32}$", r"$\sqrt{12}\cdot\sqrt{\frac34}\cdot\sqrt{\frac{12}{5}}\cdot\sqrt{\frac{15}{4}}$", r"$\sqrt{10}\cdot\sqrt[3]{10}\cdot\sqrt[4]{10}$", r"$(\sqrt3+\sqrt2)^2$"]),
     tasks(2, [R(r"\sqrt{30}"), R(r"\sqrt[6]{5^3\cdot6^2}=\sqrt[6]{4500}"), R(r"6+2\sqrt2"), R(r"a^{\frac{25}{12}}=a^2\sqrt[12]a"), R(r"6\sqrt3-12"), R(r"2\sqrt[6]{432}-2\sqrt[6]{243}"),
               R(r"\sqrt[12]{\frac{128}{2187}}"), R(r"\sqrt{81}=9"), R(r"10\sqrt[12]{10}"), R(r"5+2\sqrt6")])),
 (2, r"Escribe las expresiones siguientes bajo un solo radical y simplifica los resultados:" + tasks(3, [r"$\sqrt{\sqrt8}$", r"$\sqrt{2\sqrt2}$", r"$\sqrt[3]{\sqrt{32}}$", r"$\sqrt{2\sqrt{3\sqrt[4]4}}$", r"$\sqrt[3]{5\sqrt[4]{5\sqrt[5]{5^2}}}$", r"$\sqrt[3]{3\sqrt[3]{\frac19}}$"]),
     tasks(3, [R(r"\sqrt[4]8"), R(r"\sqrt[4]8"), R(r"\sqrt[6]{32}"), R(r"\sqrt[4]{24}"), R(r"\sqrt[20]{5^9}"), R(r"\sqrt[9]3")])),
]))

# =====================================================================
# 5. Logaritmes
ck(round(9 / math.log10(2), 1), 29.9)
ck([round(2 - .301, 3), round(.477 / .778, 3), round((.602 + .477 + .778) / 2, 4), round((.301 + .477 + .778) / (3 * .301), 3), round(2 * .477 - .301, 3), round(.631 + 1 + 2 * 1.465, 3)], [1.699, 0.613, 0.9285, 1.723, 0.653, 4.561])
l41 = [math.log(20, 3), math.log(7 / 5, 1 / 4), math.log(60, .5), math.log(3, 2 ** .5), math.log(2 ** (1 / 3), .4), math.log(3 ** .5, 2 ** .5)]
ck([round(x, 3) for x in l41], [2.727, -0.243, -5.907, 3.170, -0.252, 1.585])
def d3(x): return ('%.3f' % x).replace('.', ',')
S.append(("Logaritmos", [
 (1, r"Aplicando la definición, calcula el valor de los logaritmos siguientes:" + tasks(4, [r"$\log_2 8$", r"$\log_3 81$", r"$\log 1000$", r"$\log 0,0001$", r"$\ln e^{33}$", r"$\ln e^{-4}$", r"$\log_4 16$", r"$\log_4 0,25$"]),
     tasks(4, [R("3"), R("4"), R("3"), R("-4"), R("33"), R("-4"), R("2"), R("-1")]) + r"(El apartado e) lo hemos leído como $\ln e^{33}$; si fuera $\ln(3e^3)$, el resultado sería $3+\ln3\approx4,099$.)"),
 (1, r"Aplicando la definición, calcula el valor de los logaritmos siguientes:" + tasks(4, [r"$\log_3\sqrt{27}$", r"$\log_7\frac{1}{49}$", r"$\log_3 3\sqrt3$", r"$\log_3 0,\widehat3$", r"$\log_5\sqrt[3]{25}$", r"$\log_9\sqrt[3]3$", r"$\log_{\frac12}\sqrt8$", r"$\log_8 0,125$"]),
     tasks(4, [R(r"\frac32"), R("-2"), R(r"\frac32"), R("-1"), R(r"\frac23"), R(r"\frac16"), R(r"-\frac32"), R("-1")])),
 (2, r"Calcula, si es posible, el valor de $x$ en cada una de las expresiones siguientes:" + tasks(4, [r"$\log_x 8=-3$", r"$\log_{-3}\sqrt x=9$", r"$\log_3(-81)=x$", r"$\log_{\frac{1}{\sqrt2}}x=-2$", r"$\log_x\sqrt2=0$", r"$\log_1 2=x$", r"$\log_5 x=-1$", r"$\log_{\frac1a}a^2=x$"])
     + recorda(r"$\log_a b$ solo existe si $a>0$, $a\neq1$ y $b>0$."),
     tasks(2, [R(r"x=\frac12"), r"No: base negativa.", r"No: argumento negativo.", R("x=2"), r"No: $x^0=1\neq\sqrt2$.", r"No: la base no puede ser 1.", R(r"x=\frac15"), R("x=-2")])),
 (1, r"Halla el resultado de las expresiones siguientes mediante las propiedades de los logaritmos:" + tasks(1, [r"$2\log_4 16+\log_2 32-3\log_7 49$", r"$\log_2 8+\log_3 27+3\log_5 125$", r"$\log_5 625-\log_9 81+\log_8 64$"]),
     tasks(3, [r"$4+5-6=" + R("3").strip('$') + "$", r"$3+3+9=" + R("15").strip('$') + "$", r"$4-2+2=" + R("4").strip('$') + "$"])),
 (2, r"Una bacteria se duplica cada hora si tiene las condiciones óptimas. ¿Cuántas horas tendrán que pasar para que una bacteria inicial cree una colonia de mil millones de bacterias?",
     r"$2^t=10^9\Rightarrow t=\dfrac{9}{\log2}\approx29,9$. Tendrán que pasar unas " + R(r"30\ \text{horas}") + "."),
 (2, r"Considerando $\log2=0,301$, $\log3=0,477$ y $\log k=0,778$, calcula los logaritmos siguientes:" + tasks(3, [r"$\log50$", r"$\log0,\widehat3$", r"$\log_k3$", r"$\log\sqrt{12k}$", r"$\log_2\sqrt[3]{6k}$", r"$\log4,5$"]),
     tasks(2, [r"$2-\log2=" + R("1,699").strip('$') + "$", r"$-\log3=" + R("-0,477").strip('$') + "$", r"$\frac{0,477}{0,778}\approx" + R("0,613").strip('$') + "$",
               r"$\frac12(2\log2+\log3+\log k)=" + R("0,9285").strip('$') + "$", r"$\frac{\log2+\log3+\log k}{3\log2}\approx" + R("1,723").strip('$') + "$", r"$2\log3-\log2=" + R("0,653").strip('$') + "$"])),
 (2, r"Si $\log_3 2=0,631$ y $\log_3 5=1,465$, calcula el valor del logaritmo en base 3 de 150.",
     r"$\log_3150=\log_3(2\cdot3\cdot5^2)=0,631+1+2\cdot1,465=" + R("4,561").strip('$') + "$"),
 (2, r"Toma logaritmos decimales en las igualdades siguientes y desarrolla las expresiones:" + tasks(3, [r"$P=10x^3yz^3$", r"$Q=\dfrac{100x^2}{x+y}$", r"$R=\sqrt[3]{\dfrac{2x^2y^5}{3z^3}}$", r"$x=a^4b^3c^{\frac32}$", r"$y=\dfrac{\sqrt[3]{x^2}}{ax}$", r"$xy=\dfrac{(m+2n)n^2}{m-2n}$"]),
     tasks(1, [R(r"\log P=1+3\log x+\log y+3\log z"), R(r"\log Q=2+2\log x-\log(x+y)"), R(r"\log R=\tfrac13\left(\log2+2\log x+5\log y-\log3-3\log z\right)"),
               R(r"\log x=4\log a+3\log b+\tfrac32\log c"), R(r"\log y=-\tfrac13\log x-\log a"), R(r"\log x+\log y=\log(m+2n)+2\log n-\log(m-2n)")])),
 (2, r"Expresa el valor de $E$ en cada caso sin que aparezcan logaritmos:" + tasks(1, [r"$\log E=2-2\log x+\log y-5\log z$", r"$\log E=3\log2-4\log x+3\log y-2\log z$", r"$\log E=\log(x-2y)+\log(x+y)$", r"$\log E=3\log(x+10)-\log\frac{2x+20}{3}+\log\frac23$"]),
     tasks(2, [R(r"E=\frac{100y}{x^2z^5}"), R(r"E=\frac{8y^3}{x^4z^2}"), R(r"E=(x-2y)(x+y)"), R(r"E=(x+10)^2")])),
 (1, r"Con la ayuda de la calculadora, obtén aproximaciones hasta las milésimas de los logaritmos siguientes:" + tasks(3, [r"$\log_3 20$", r"$\log_{\frac14}\frac75$", r"$\log_{0,5}60$", r"$\log_{\sqrt2}3$", r"$\log_{\frac25}\sqrt[3]2$", r"$\log_{\sqrt2}\sqrt3$"])
     + recorda(r"Cambio de base: $\log_a x=\dfrac{\log x}{\log a}=\dfrac{\ln x}{\ln a}$."),
     tasks(3, [R(d3(x)) for x in l41])),
 (2, r"Determina el valor de $x$:" + tasks(4, [r"$8^x=1024$", r"$3^{x^2}=27$", r"$3^{x^2-6}=27$", r"$10^{x-1}=10^3$", r"$8^{x-3}=1024$", r"$(3^x)^2=27$", r"$3^{x^2}+18=27$", r"$2^{x^2-2x+1}=1$"]),
     tasks(4, [R(r"x=\frac{10}{3}"), R(r"x=\pm\sqrt3"), R(r"x=\pm3"), R("x=4"), R(r"x=\frac{19}{3}"), R(r"x=\frac32"), R(r"x=\pm\sqrt2"), R("x=1")])),
]))
ck([F(10, 3) * 3, 3 * (F(19, 3) - 3)], [10, 10])

# =====================================================================
# 6. Ampliació i problemes (nous)
ck([per('0', '1', '6'), per('2', '', '09'), per('1', '2', '45'), per('0', '', '9')], [F(1, 6), F(23, 11), F(137, 110), F(1)])
ck(round(-(math.log10(3.2) - 4), 2), 3.49)
ck(math.ceil(math.log(1.5) / math.log(1.03)), 14)
ck(F(8) ** 0 * 4 * F(1, 3) / 8, F(1, 6))
S.append(("Ampliación y problemas", [
 (2, r"Clasifica cada número en el menor conjunto numérico. ¡Opera primero!" + tasks(3, [r"$\sqrt2\cdot\sqrt8$", r"$\sqrt2+\sqrt8$", r"$\pi-\pi$", r"$0,1010010001\ldots$", r"$-\sqrt{\frac94}$", r"$\sqrt{-4}$"]),
     tasks(3, [R(r"4\in\mathbb N"), R(r"3\sqrt2\in\mathbb I"), R(r"0\in\mathbb N"), R(r"\mathbb I") + r" (no es periódico)", R(r"-\frac32\in\mathbb Q"), r"No es un número real."])),
 (1, r"Halla la fracción generatriz y simplifícala:" + tasks(4, [r"$0,1\widehat6$", r"$2,\widehat{09}$", r"$-1,2\widehat{45}$", r"$0,\widehat9$"]),
     tasks(4, [R(r"\frac16"), R(r"\frac{23}{11}"), R(r"-\frac{137}{110}"), R("1")]) + r"Fíjate: $0,\widehat9$ y $1$ son el mismo número."),
 (2, r"Expresa cada conjunto con una desigualdad con valor absoluto (busca el centro y el radio):" + tasks(4, [r"$(1, 7)$", r"$[-5, 1]$", r"$(-\infty, -1)\cup(5, +\infty)$", r"$[-0,5;\ 0,5]$"]),
     tasks(4, [R(r"|x-4|<3"), R(r"|x+2|\le3"), R(r"|x-2|>3"), R(r"|x|\le0,5")])),
 (2, r"La temperatura $T$ de una nevera debe ser de $4\,^\circ$C con un margen de error de $1,5\,^\circ$C. Escribe esta condición con un valor absoluto y como intervalo. ¿Es aceptable una lectura de $5,7\,^\circ$C?",
     R(r"|T-4|\le1,5") + r", es decir, $T\in" + R(r"[2,5;\ 5,5]").strip('$') + r"$. Una lectura de $5,7\,^\circ$C \rest{no es aceptable}: $|5,7-4|=1,7>1,5$."),
 (1, r"Entornos:" + tasks(2, [r"Escribe como intervalo $B(-1;\ 2,5)$.", r"Escribe como intervalo el entorno cerrado de centro 3 y radio $\frac12$.", r"¿Centro y radio del intervalo $(-2, 8)$?", r"¿Qué enteros pertenecen a $B(0,5;\ 3)$?"]),
     tasks(2, [R(r"(-3,5;\ 1,5)"), R(r"\left[\frac52, \frac72\right]"), R(r"a=3,\ r=5"), R(r"-2,\,-1,\,0,\,1,\,2,\,3")])),
 (2, r"Un cuadrado tiene un área de $50\ \text{cm}^2$. Calcula su lado y su diagonal en forma de radical simplificado.",
     r"Lado: $\sqrt{50}=" + R(r"5\sqrt2\ \text{cm}").strip('$') + r"$. Diagonal: $\sqrt2\cdot5\sqrt2=" + R(r"10\ \text{cm}").strip('$') + r"$ (o bien $\sqrt{50+50}=10$)."),
 (2, r"Racionaliza, opera y simplifica:" + tasks(2, [r"$\dfrac{\sqrt3+1}{\sqrt3-1}-\dfrac{\sqrt3-1}{\sqrt3+1}$", r"$\dfrac{1}{\sqrt2}+\dfrac{1}{\sqrt2+1}$"]),
     tasks(2, [r"$\dfrac{(\sqrt3+1)^2-(\sqrt3-1)^2}{2}=" + R(r"2\sqrt3").strip('$') + "$", r"$\dfrac{\sqrt2}{2}+\sqrt2-1=" + R(r"\frac{3\sqrt2}{2}-1").strip('$') + "$"])),
 (2, r"Calcula sin calculadora pasando a exponentes fraccionarios:" + tasks(3, [r"$\dfrac{8^{2/3}\cdot27^{-1/3}}{16^{3/4}}$", r"$\left(\dfrac{1}{32}\right)^{-2/5}$", r"$81^{0,75}$"]),
     tasks(3, [r"$\dfrac{4\cdot\frac13}{8}=" + R(r"\frac16").strip('$') + "$", R("2^2=4"), R("3^3=27")])),
 (1, r"Encuentra el error en cada uno de estos cálculos y corrígelo:" + tasks(2, [r"$\sqrt{9+16}=3+4=7$", r"$-3^2=9$", r"$\log(5+5)=\log5+\log5$", r"$2^{-3}=-8$"]),
     tasks(2, [r"La raíz no se reparte en sumas: " + R(r"\sqrt{25}=5"), r"El exponente solo afecta al 3: " + R("-3^2=-9"), r"La propiedad es para el producto: " + R(r"\log10=1"), R(r"2^{-3}=\frac18")])),
 (2, r"El pH de una disolución es $\text{pH}=-\log[\text{H}^+]$." + tasks(1, [r"Calcula el pH si $[\text{H}^+]=3,2\cdot10^{-4}$ mol/L.", r"La sangre tiene un pH de 7,4. ¿Cuál es su concentración $[\text{H}^+]$?"]),
     tasks(1, [r"$\text{pH}=-(\log3,2-4)\approx" + R("3,49").strip('$') + "$", r"$[\text{H}^+]=10^{-7,4}\approx" + R(r"3,98\cdot10^{-8}\ \text{mol/L}").strip('$') + "$"])),
 (2, r"Ingresamos 2000 € en una cuenta al 3\,\% de interés compuesto anual. ¿Cuántos años tienen que pasar, como mínimo, para que haya 3000 €?",
     r"$2000\cdot1,03^t=3000\Rightarrow1,03^t=1,5\Rightarrow t=\dfrac{\log1,5}{\log1,03}\approx13,7$. Hacen falta " + R(r"14\ \text{años}") + "."),
 (3, r"Sin calculadora, ordena de menor a mayor $\log_2 10$, \ $3$ \ y \ $\log_3 10$. Justifícalo.",
     r"$2^3=8<10\Rightarrow\log_210>3$; \ $3^2=9<10<27=3^3\Rightarrow2<\log_310<3$. Por tanto, " + R(r"\log_310<3<\log_210") + "."),
]))

for l, r in CHK:
    assert l == r, (l, r)
assert [len(x[1]) for x in S] == [3, 1, 7, 20, 11, 12], [len(x[1]) for x in S]

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "números reales, fracción generatriz, valor absoluto, entornos, intervalos, potencias, radicales, racionalización, logaritmos"
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

TIT = "Números reales"
# dins de les fórmules, «, » separa elements: hi posem un espai fi perquè icomma no el confonga amb una coma decimal
def sp(t): return re.sub(r'\$[^$]*\$', lambda m: m.group(0).replace(', ', r',\, '), t)
def build(sol):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 1: %s' % (t, TIT), capcalera='%s · Unidad 1: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-mi')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1batx-mi') + '{' + ('Soluciones de la ficha · Unidad 1' if sol else 'Ficha de ejercicios · Unidad 1') + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{7.8cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Los resultados se dan de manera exacta (fracciones y raíces) y, cuando hace falta, con el valor aproximado. Puedes comprobar los de intervalos, valor absoluto, radicales y logaritmos con las herramientas interactivas de los apuntes de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. Da los resultados de manera exacta (fracciones y raíces simplificadas, sin raíces en el denominador) y, si hace falta, también aproximados. Los ejercicios 1--42 son los de la ficha del departamento; la sección 6 tiene otros nuevos para ampliar y aplicar lo que has aprendido.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, sp(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't1-fitxa-solucions-es.tex' if sol else 't1-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(x[1]) for x in S), 'ejercicios;', len(CHK), 'comprobaciones')
