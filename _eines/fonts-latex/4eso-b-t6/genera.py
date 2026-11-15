# Genera t6-fitxa-exercicis.tex i t6-fitxa-solucions.tex (4t ESO Matemàtiques B, Unitat 6: Vectors i rectes)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py.
# Recull TOTS els exercicis de les dues fitxes del departament («Fitxa 6 Geometria analítica», 14 exercicis, i «Vectors i
# equacions de rectes», 10 exercicis; marcats amb (D) en aquest codi) i hi afegeix variacions dels exercicis del llibre
# (vectors 1-12 i 42-77, equacions 78-96, posició relativa 97-109 i 32-41: sempre amb dades noves) i exercicis nous.
# Les 8 seccions segueixen els apartats dels apunts (6.1-6.8).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es). Tots els resultats es calculen ací amb fraccions exactes (vectors, rectes, punts de tall)
# i ck() comprova els que s'escriuen a mà.
# Ús: python3 genera.py && pdflatex t6-fitxa-exercicis.tex (dues vegades) && pdflatex t6-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va
_dec = dec
def dec(x, k=2): return _dec(x, k)   # dues xifres decimals per defecte

# ---------- nombres, punts i vectors ----------
def tp(x): return '(' + tn(x) + ')' if F(x) < 0 else tn(x)          # entre parèntesis si és negatiu
def pt(p): return r'(%s,\,%s)' % (tn(p[0]), tn(p[1]))
def V(n): return r'\overrightarrow{%s}' % n
def vsub(p, q): return (F(p[0]) - F(q[0]), F(p[1]) - F(q[1]))
def vadd(p, q): return (F(p[0]) + F(q[0]), F(p[1]) + F(q[1]))
def vmul(k, p): return (F(k) * F(p[0]), F(k) * F(p[1]))
def dot(u, v): return F(u[0]) * F(v[0]) + F(u[1]) * F(v[1])
def n2(u): return dot(u, u)
def mid(p, q): return ((F(p[0]) + F(q[0])) / 2, (F(p[1]) + F(q[1])) / 2)
def par(u, v): return F(u[0]) * F(v[1]) - F(u[1]) * F(v[0]) == 0
def prm(v):
    v = (F(v[0]), F(v[1])); m = math.lcm(v[0].denominator, v[1].denominator); a, b = int(v[0] * m), int(v[1] * m)
    g = math.gcd(a, b) or 1
    return (a // g, b // g)
def surd(n):
    a, b, i = 1, n, 2
    while i * i <= b:
        while b % (i * i) == 0: b //= i * i; a *= i
        i += 1
    return a, b
def sq(n, ap=True):
    """√n simplificada (n enter) i, si no és exacta, aproximada"""
    n = int(n); a, b = surd(n)
    if b == 1: return str(a)
    s = (r'\sqrt{%d}' % b) if a == 1 else (r'%d\sqrt{%d}' % (a, b))
    if s != r'\sqrt{%d}' % n: s = r'\sqrt{%d}=' % n + s
    return s + (r'\approx' + dec(math.sqrt(n), 2) if ap else '')
def comps(A, B, nA='A', nB='B'):
    """\\overrightarrow{AB}=(b1-a1,\\,b2-a2)=(…)"""
    v = vsub(B, A)
    return V(nA + nB) + r'=(%s-%s,\,%s-%s)=%s' % (tn(B[0]), tp(A[0]), tn(B[1]), tp(A[1]), pt(v)), v
def dres(v):
    """\\sqrt{a^2+b^2}=\\sqrt{n}(=a\\sqrt{b})≈… amb el resultat final emmarcat"""
    n = int(n2(v)); a, b = surd(n)
    t = r'\sqrt{%s^2+%s^2}=' % (tp(v[0]), tp(v[1]))
    if b == 1: return t + r'\sqrt{%d}=' % n + Rm(str(a))
    if a == 1: return t + Rm(r'\sqrt{%d}' % n) + r'\approx' + dec(math.sqrt(n), 2)
    return t + r'\sqrt{%d}=' % n + Rm(r'%d\sqrt{%d}' % (a, b)) + r'\approx' + dec(math.sqrt(n), 2)

# ---------- rectes ----------
def poly(terms):
    s = ''
    for c, v in terms:
        c = F(c)
        if c == 0: continue
        a = abs(c); body = v if (v and a == 1) else tn(a) + v
        s += ('-' if c < 0 else ('+' if s else '')) + body
    return s or '0'
class L:
    """recta Ax+By+C=0 amb coeficients enters primitius i el primer positiu"""
    def __init__(s, A, B, C):
        A, B, C = F(A), F(B), F(C)
        m = math.lcm(A.denominator, B.denominator, C.denominator)
        a, b, c = int(A * m), int(B * m), int(C * m)
        g = math.gcd(math.gcd(a, b), c) or 1
        a, b, c = a // g, b // g, c // g
        if a < 0 or (a == 0 and b < 0): a, b, c = -a, -b, -c
        s.A, s.B, s.C = a, b, c
    def t(s): return poly([(s.A, 'x'), (s.B, 'y'), (s.C, '')]) + '=0'
    def __eq__(s, o): return (s.A, s.B, s.C) == (o.A, o.B, o.C)
    def __repr__(s): return s.t()
    def has(s, p): return s.A * F(p[0]) + s.B * F(p[1]) + s.C == 0
    def n(s): return (s.A, s.B)
    def d(s): return (-s.B, s.A)
    def m(s): return F(-s.A, s.B) if s.B else None
    def nn(s): return F(-s.C, s.B) if s.B else None
    def expl(s): return 'y=' + poly([(s.m(), 'x'), (s.nn(), '')])
def ldir(p, d): return L(d[1], -F(d[0]), F(d[0]) * F(p[1]) - F(d[1]) * F(p[0]))
def lnorm(p, n): return L(n[0], n[1], -dot(n, p))
def l2(p, q): return ldir(p, vsub(q, p))
def lm(p, m): return ldir(p, (1, m))
def inter(r, s):
    det = r.A * s.B - s.A * r.B
    if det == 0: return None
    return (F(r.B * s.C - s.B * r.C, det), F(s.A * r.C - r.A * s.C, det))
def pos(r, s):
    if inter(r, s): return 'sec'
    return 'coi' if r == s else 'par'
def mT(m):
    """coeficient del pendent davant d'un parèntesi: 1 -> '', -1 -> '-'"""
    return '' if m == 1 else '-' if m == -1 else tn(m)
def ptpend(p, m):
    rhs = '0' if m == 0 else (tn(m) + 'x' if m not in (1, -1) else mT(m) + 'x') if F(p[0]) == 0 else mT(m) + '(' + poly([(1, 'x'), (-F(p[0]), '')]) + ')'
    return poly([(1, 'y'), (-F(p[1]), '')]) + '=' + rhs
def vect(p, d, par_=r'\lambda'): return r'(x,y)=%s+%s%s' % (pt(p), par_, pt(d))
def param(p, d, par_=r'\lambda'):
    return r'\left\{\begin{array}{l}x=%s\\ y=%s\end{array}\right.' % (poly([(p[0], ''), (d[0], par_)]), poly([(p[1], ''), (d[1], par_)]))
def cont(p, d): return r'\dfrac{%s}{%s}=\dfrac{%s}{%s}' % (poly([(1, 'x'), (-F(p[0]), '')]), tn(d[0]), poly([(1, 'y'), (-F(p[1]), '')]), tn(d[1]))
LBL = {'vec': T('Vectorial', 'Vectorial'), 'par': T('Paramètriques', 'Paramétricas'), 'con': T('Contínua', 'Continua'),
       'pp': T('Punt-pendent', 'Punto-pendiente'), 'exp': T('Explícita', 'Explícita'), 'gen': T('General', 'General')}
def eqs(p, d, skip=()):
    """totes les equacions de la recta per p amb director d (llista de cadenes)"""
    r = ldir(p, d); o = []
    if 'vec' not in skip: o.append(LBL['vec'] + ': $' + vect(p, d) + '$')
    if 'par' not in skip: o.append(LBL['par'] + ': $' + param(p, d) + '$')
    if 'con' not in skip:
        o.append(LBL['con'] + ': $' + cont(p, d) + '$' if F(d[0]) and F(d[1]) else LBL['con'] + T(': no es pot escriure (una component de $\\vec v$ és 0)', ': no se puede escribir (una componente de $\\vec v$ es 0)'))
    if F(d[0]):
        m = F(d[1]) / F(d[0])
        if 'pp' not in skip: o.append(LBL['pp'] + ': $' + ptpend(p, m) + '$')
        if 'exp' not in skip: o.append(LBL['exp'] + ': $' + r.expl() + '$')
    o.append(LBL['gen'] + r': $\res{' + r.t() + '}$')
    return o, r
def lst2(xs): return r'\begin{multicols}{2}' + lst(xs) + r'\end{multicols}'
def lst(xs): return r'\begin{itemize}[leftmargin=*,itemsep=1pt,topsep=2pt]' + ''.join(r'\item ' + x for x in xs) + r'\end{itemize}'
def items(*xs): return r'\begin{enumerate}[label=\alph*),leftmargin=*,itemsep=2pt,topsep=2pt]' + ''.join(r'\item ' + x for x in xs) + r'\end{enumerate}'
def POS(k): return {'sec': T('secants', 'secantes'), 'par': T('paral·leles', 'paralelas'), 'coi': T('coincidents', 'coincidentes')}[k]

# ---------- figures TikZ ----------
def fig(objs, box=(-6, 6, -6, 6), sc=0.36):
    """objs: ('l', recta, color, etiqueta?) | ('p', punt, etiqueta, posició) | ('v', p, q, color, etiqueta?) | ('s', p, q, color) | ('poly', [punts], color)"""
    x0, x1, y0, y1 = box
    o = [r'\begin{tikzpicture}[scale=%g,baseline=(current bounding box.center)]' % sc,
         r'\draw[muted!25,very thin] (%d,%d) grid (%d,%d);' % (x0, y0, x1, y1),
         r'\draw[-latex,muted] (%g,0)--(%g,0) node[right,font=\scriptsize]{$x$}; \draw[-latex,muted] (0,%g)--(0,%g) node[above,font=\scriptsize]{$y$};' % (x0 - .3, x1 + .5, y0 - .3, y1 + .5),
         r'\foreach \i in {%d,%d,...,%d}{\ifnum\i=0\else\node[font=\tiny,text=muted,below] at (\i,0) {$\i$};\fi}' % (x0 + (x0 % 2), x0 + (x0 % 2) + 2, x1),
         r'\foreach \i in {%d,%d,...,%d}{\ifnum\i=0\else\node[font=\tiny,text=muted,left] at (0,\i) {$\i$};\fi}' % (y0 + (y0 % 2), y0 + (y0 % 2) + 2, y1),
         r'\begin{scope}\clip (%d,%d) rectangle (%d,%d);' % (x0, y0, x1, y1)]
    late = []
    for ob in objs:
        if ob[0] == 'l':
            r, col = ob[1], ob[2]
            if r.B: a, b = (x0, float(F(-r.C - r.A * x0, r.B))), (x1, float(F(-r.C - r.A * x1, r.B)))
            else: a, b = (float(F(-r.C, r.A)), y0), (float(F(-r.C, r.A)), y1)
            o.append(r'\draw[%s,thick] (%g,%g)--(%g,%g);' % (col, a[0], a[1], b[0], b[1]))
            if len(ob) > 3: late.append(r'\node[%s,font=\small\itshape,fill=white,inner sep=1pt] at (%g,%g) {$%s$};' % (col, ob[3][0], ob[3][1], ob[4]))
        elif ob[0] == 's': o.append(r'\draw[%s,thick] (%g,%g)--(%g,%g);' % (ob[3], float(ob[1][0]), float(ob[1][1]), float(ob[2][0]), float(ob[2][1])))
        elif ob[0] == 'poly': o.append(r'\filldraw[fill=%s!15,draw=%s,thick] ' % (ob[2], ob[2]) + '--'.join('(%g,%g)' % (float(p[0]), float(p[1])) for p in ob[1]) + '--cycle;')
    o.append(r'\end{scope}')
    for ob in objs:
        if ob[0] == 'v':
            o.append(r'\draw[-{Latex[length=2.2mm]},%s,line width=1.1pt] (%g,%g)--(%g,%g);' % (ob[3], float(ob[1][0]), float(ob[1][1]), float(ob[2][0]), float(ob[2][1])))
            if len(ob) > 4: o.append(r'\node[%s,font=\small,%s] at (%g,%g) {$%s$};' % (ob[3], ob[5] if len(ob) > 5 else 'above left', (float(ob[1][0]) + float(ob[2][0])) / 2, (float(ob[1][1]) + float(ob[2][1])) / 2, ob[4]))
        elif ob[0] == 'p':
            o.append(r'\fill[navy] (%g,%g) circle (2.4pt) node[%s,font=\scriptsize]{$%s$};' % (float(ob[1][0]), float(ob[1][1]), ob[3] if len(ob) > 3 else 'above right', ob[2]))
    o += late
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def cen(*gs): return '\n\n\\begin{center}' + '\\qquad'.join(gs) + '\\end{center}\n'

S = []
def sec(title): S.append((title, [])); return S[-1][1]

# =====================================================================
# 1. Vectors
E = sec(T('Vectors', 'Vectores'))
# llibre 1 (variació)
d1 = [((2, 5), (4, -1)), ((-3, 2), (1, 6)), ((0, -4), (-5, -1)), ((3, 3), (3, -2))]
E.append((1, T(r"Calcula les components del vector $\overrightarrow{AB}$ coneixent-ne l'origen $A$ i l'extrem $B$:", r"Calcula las componentes del vector $\overrightarrow{AB}$ conociendo su origen $A$ y su extremo $B$:") +
          tasks(2, [r'$A%s$, \ $B%s$' % (pt(a), pt(b)) for a, b in d1]),
          tasks(2, ['$' + comps(a, b)[0].rsplit('=', 1)[0] + '=' + Rm(pt(vsub(b, a))) + '$' for a, b in d1])))
# llibre 4/56 (variació)
d2 = [(6, 8), (-5, 12), (2, -3), (-4, -4), (0, -7), (8, -6)]
ck([n2(v) for v in d2], [100, 169, 13, 32, 49, 100])
def mres(v):
    a, b = surd(int(n2(v)))
    return Rm(str(a)) if b == 1 else Rm(sq(n2(v)).split('=')[-1].split(r'\approx')[0]) + r'\approx' + dec(math.sqrt(n2(v)), 2)
E.append((1, T(r"Calcula el mòdul dels vectors següents:", r"Calcula el módulo de los vectores siguientes:") +
          tasks(3, [r'$\vec %s=%s$' % (c, pt(v)) for c, v in zip('abcdef', d2)]),
          tasks(2, [r'$\sqrt{%s^2+%s^2}=\sqrt{%d}=%s$' % (tp(v[0]), tp(v[1]), n2(v), mres(v)) for v in d2])))
# departament, fitxa de repàs 1
A, B, C = (3, -2), (-4, 1), (5, 2)
cAB, vAB = comps(A, B); cBC, vBC = comps(B, C, 'B', 'C'); vAC = vsub(C, A)
ck((vAB, vBC, n2(vAB), n2(vAC)), ((-7, 3), (9, 1), 58, 20))
E.append((1, T(r"Siguen els punts $A(3,-2)$, $B(-4,1)$ i $C(5,2)$. Troba:" + items(r"Els vectors $\overrightarrow{AB}$ i $\overrightarrow{BC}$.", r"El mòdul del vector $\overrightarrow{AB}$.", r"La distància del punt $A$ al punt $C$."),
                 r"Sean los puntos $A(3,-2)$, $B(-4,1)$ y $C(5,2)$. Halla:" + items(r"Los vectores $\overrightarrow{AB}$ y $\overrightarrow{BC}$.", r"El módulo del vector $\overrightarrow{AB}$.", r"La distancia del punto $A$ al punto $C$.")),
          items('$' + cAB.rsplit('=', 1)[0] + '=' + Rm(pt(vAB)) + r'$; \ $' + cBC.rsplit('=', 1)[0] + '=' + Rm(pt(vBC)) + '$',
                r'$|\overrightarrow{AB}|=\sqrt{49+9}=' + Rm(r'\sqrt{58}') + r'\approx' + dec(math.sqrt(58), 2) + '$',
                r'$\overrightarrow{AC}=%s$, \ $d(A,C)=\sqrt{4+16}=\sqrt{20}=' % pt(vAC) + Rm(r'2\sqrt5') + r'\approx' + dec(math.sqrt(20), 2) + '$')))
# llibre 49 i 51 (variació): extrem i origen
d4 = [((4, -1), (-3, 2)), ((-2, -5), (1, 3)), ((6, 0), (-4, -4)), ((-3, 7), (5, -6))]
d5 = [((-2, 4), (1, 1)), ((5, -3), (0, 0)), ((-1, -6), (-4, 2)), ((3, 3), (2, -5))]
E.append((1, T(r"Calcula el punt que falta en cada cas:" + items(
    r"L'extrem $B$, si $\overrightarrow{AB}=\vec v$ té l'origen en $A$: \ " + '; \\ '.join(r'$\vec v=%s$, $A%s$' % (pt(v), pt(a)) for v, a in d4) + '.',
    r"L'origen $A$, si $\overrightarrow{AB}=\vec v$ té l'extrem en $B$: \ " + '; \\ '.join(r'$\vec v=%s$, $B%s$' % (pt(v), pt(b)) for v, b in d5) + '.'),
    r"Calcula el punto que falta en cada caso:" + items(
    r"El extremo $B$, si $\overrightarrow{AB}=\vec v$ tiene el origen en $A$: \ " + '; \\ '.join(r'$\vec v=%s$, $A%s$' % (pt(v), pt(a)) for v, a in d4) + '.',
    r"El origen $A$, si $\overrightarrow{AB}=\vec v$ tiene el extremo en $B$: \ " + '; \\ '.join(r'$\vec v=%s$, $B%s$' % (pt(v), pt(b)) for v, b in d5) + '.')),
    items(r'$B=A+\vec v$: \ ' + '; \\ '.join('$' + Rm(pt(vadd(a, v))) + '$' for v, a in d4),
          r'$A=B-\vec v$: \ ' + '; \\ '.join('$' + Rm(pt(vsub(b, v))) + '$' for v, b in d5))))
ck([vadd(a, v) for v, a in d4], [(1, 1), (-1, -2), (2, -4), (2, 1)])
# llibre 3 (variació)
E.append((2, T(r"El vector $\vec v=(4,-3)$ es dibuixa a partir de diferents punts. Escriu tres parells de punts origen-extrem que el representen: un amb l'origen en $O(0,0)$, un altre amb l'origen en $(-1,5)$ i un altre amb l'extrem en $O(0,0)$.",
                 r"El vector $\vec v=(4,-3)$ se dibuja a partir de diferentes puntos. Escribe tres pares de puntos origen-extremo que lo representen: uno con el origen en $O(0,0)$, otro con el origen en $(-1,5)$ y otro con el extremo en $O(0,0)$."),
          T(r"$O(0,0)\to" + Rm('(4,-3)') + r"$; \ $(-1,5)\to" + Rm('(3,2)') + r"$; \ $" + Rm('(-4,3)') + r"\to O(0,0)$. Tots són equipol·lents: el mateix vector lliure.",
            r"$O(0,0)\to" + Rm('(4,-3)') + r"$; \ $(-1,5)\to" + Rm('(3,2)') + r"$; \ $" + Rm('(-4,3)') + r"\to O(0,0)$. Todos son equipolentes: el mismo vector libre.")))
# llibre 42/44 (variació): vectors dibuixats
VF = [('a', (-5, 1), (-2, 3)), ('b', (1, 3), (4, 5)), ('c', (-4, -1), (-4, -4)), ('d', (5, -1), (2, -3)), ('e', (-1, -3), (3, -4))]
cols = ['accent', 'teal', 'navy', 'violet', 'orange']
figv = fig([('v', p, q, col, r'\vec ' + n, 'above left') for (n, p, q), col in zip(VF, cols)], box=(-6, 6, -5, 6), sc=0.45)
sol = [r'$\vec %s$: $%s\to%s$, \ $\vec %s=%s$, \ $|\vec %s|=%s$' % (n, pt(p), pt(q), n, Rm(pt(vsub(q, p))), n, sq(n2(vsub(q, p)))) for n, p, q in VF]
ck((vsub(VF[0][2], VF[0][1]), vsub(VF[1][2], VF[1][1]), vsub(VF[3][2], VF[3][1])), ((3, 2), (3, 2), (-3, -2)))
E.append((1, T(r"Observa els vectors del dibuix." + items(r"Indica l'origen, l'extrem i les components de cada vector, i calcula'n el mòdul.", r"Quins vectors són equipol·lents? Quin és l'oposat de $\vec a$?"),
                 r"Observa los vectores del dibujo." + items(r"Indica el origen, el extremo y las componentes de cada vector, y calcula su módulo.", r"¿Qué vectores son equipolentes? ¿Cuál es el opuesto de $\vec a$?")) + cen(figv),
          items(lst(sol), T(r"$\vec a$ i $\vec b$ són " + Rm(r'\text{equipol·lents}') + r" (components $(3,2)$); l'oposat de $\vec a$ és " + Rm(r'\vec d=(-3,-2)') + '.',
                            r"$\vec a$ y $\vec b$ son " + Rm(r'\text{equipolentes}') + r" (componentes $(3,2)$); el opuesto de $\vec a$ es " + Rm(r'\vec d=(-3,-2)') + '.'))))
# llibre 2 (variació)
A, B, C = (-2, 1), (3, 4), (2, -2)
fig2 = fig([('poly', [A, B, C], 'teal'), ('v', A, B, 'accent'), ('v', B, C, 'accent'), ('v', C, A, 'accent'), ('p', A, 'A', 'left'), ('p', B, 'B', 'above'), ('p', C, 'C', 'below')], box=(-4, 5, -4, 6), sc=0.32)
s1 = [comps(A, B), comps(B, C, 'B', 'C'), comps(C, A, 'C', 'A')]
ck(vadd(vadd(s1[0][1], s1[1][1]), s1[2][1]), (0, 0))
E.append((2, T(r"Representa el triangle de vèrtexs $A(-2,1)$, $B(3,4)$ i $C(2,-2)$ i calcula les components dels vectors $\overrightarrow{AB}$, $\overrightarrow{BC}$ i $\overrightarrow{CA}$. Quant val $\overrightarrow{AB}+\overrightarrow{BC}+\overrightarrow{CA}$? Per què?",
                 r"Representa el triángulo de vértices $A(-2,1)$, $B(3,4)$ y $C(2,-2)$ y calcula las componentes de los vectores $\overrightarrow{AB}$, $\overrightarrow{BC}$ y $\overrightarrow{CA}$. ¿Cuánto vale $\overrightarrow{AB}+\overrightarrow{BC}+\overrightarrow{CA}$? ¿Por qué?"),
          cen(fig2) + '$' + r'$; \ $'.join(c.rsplit('=', 1)[0] + '=' + Rm(pt(v)) for c, v in s1) + '$. ' +
          T(r"La suma és $" + Rm(r'\vec 0=(0,0)') + r"$: si anem de $A$ a $B$, de $B$ a $C$ i de $C$ a $A$, tornem al punt de partida.",
            r"La suma es $" + Rm(r'\vec 0=(0,0)') + r"$: si vamos de $A$ a $B$, de $B$ a $C$ y de $C$ a $A$, volvemos al punto de partida.")))

# =====================================================================
# 2. Operacions amb vectors
E = sec(T('Operacions amb vectors', 'Operaciones con vectores'))
u, v = (2, -3), (-1, 4)
o2 = [(r'\vec u+\vec v', vadd(u, v)), (r'\vec u-\vec v', vsub(u, v)), (r'3\vec u', vmul(3, u)), (r'-2\vec v', vmul(-2, v)),
      (r'2\vec u+3\vec v', vadd(vmul(2, u), vmul(3, v))), (r'\tfrac12\vec u-\vec v', vsub(vmul(F(1, 2), u), v))]
ck([x[1] for x in o2], [(1, 1), (3, -7), (6, -9), (2, -8), (1, 6), (2, F(-11, 2))])
E.append((1, T(r"Donats els vectors $\vec u=(2,-3)$ i $\vec v=(-1,4)$, calcula:", r"Dados los vectores $\vec u=(2,-3)$ y $\vec v=(-1,4)$, calcula:") + tasks(3, ['$' + e + '$' for e, _ in o2]),
          tasks(3, ['$' + e + '=' + Rm(pt(r)) + '$' for e, r in o2])))
a, b, c = (1, -4), (-2, 3), (5, 0)
o3 = [(r'\vec a+\vec b+\vec c', vadd(vadd(a, b), c)), (r'2\vec a-\vec b+\vec c', vadd(vsub(vmul(2, a), b), c)),
      (r'-\vec a+3\vec b-2\vec c', vsub(vadd(vmul(-1, a), vmul(3, b)), vmul(2, c))), (r'\tfrac15\vec c-\tfrac12\vec b', vsub(vmul(F(1, 5), c), vmul(F(1, 2), b)))]
ck([x[1] for x in o3], [(4, -1), (9, -11), (-17, 13), (2, F(-3, 2))])
E.append((1, T(r"Amb $\vec a=(1,-4)$, $\vec b=(-2,3)$ i $\vec c=(5,0)$, opera:", r"Con $\vec a=(1,-4)$, $\vec b=(-2,3)$ y $\vec c=(5,0)$, opera:") + tasks(2, ['$' + e + '$' for e, _ in o3]),
          tasks(2, ['$' + e + '=' + Rm(pt(r)) + '$' for e, r in o3])))
# representació gràfica
u, v = (3, 1), (-1, 2)
fg = fig([('v', (0, 0), u, 'accent', r'\vec u', 'below right'), ('v', (0, 0), v, 'teal', r'\vec v', 'left'), ('v', u, vadd(u, v), 'teal'), ('v', v, vadd(u, v), 'accent'),
          ('v', (0, 0), vadd(u, v), 'navy', r'\vec u+\vec v', 'left'), ('v', v, u, 'violet', r'\vec u-\vec v', 'above right'), ('v', (0, -2), vadd((0, -2), vmul(2, u)), 'orange', r'2\vec u', 'below right')], box=(-2, 7, -3, 4), sc=0.55)
E.append((2, T(r"Dibuixa els vectors $\vec u=(3,1)$ i $\vec v=(-1,2)$ amb origen en $O(0,0)$ i, gràficament, $\vec u+\vec v$ (regla del paral·lelogram), $\vec u-\vec v$ i $2\vec u$. Comprova analíticament els resultats.",
                 r"Dibuja los vectores $\vec u=(3,1)$ y $\vec v=(-1,2)$ con origen en $O(0,0)$ y, gráficamente, $\vec u+\vec v$ (regla del paralelogramo), $\vec u-\vec v$ y $2\vec u$. Comprueba analíticamente los resultados."),
          cen(fg) + r"$\vec u+\vec v=" + Rm('(2,3)') + r"$ (" + T('diagonal del paral·lelogram', 'diagonal del paralelogramo') + r"); \ $\vec u-\vec v=" + Rm('(4,-1)') + r"$ (" +
          T(r"va de la punta de $\vec v$ a la de $\vec u$", r"va de la punta de $\vec v$ a la de $\vec u$") + r"); \ $2\vec u=" + Rm('(6,2)') + '$ (' + T('en taronja, dibuixat a partir de $(0,-2)$', 'en naranja, dibujado a partir de $(0,-2)$') + ').'))
ck((vadd(u, v), vsub(u, v)), ((2, 3), (4, -1)))
# llibre 5/63 (variació): paral·lels
pp = [((2, -6), (-1, 3)), ((4, 6), (6, 9)), ((3, 5), (5, 3)), ((-2, 8), (1, 4)), ((0, 5), (0, -2)), ((10, -4), (-15, 6))]
def ps(u, v):
    cond = (r'\dfrac{%d}{%d}' % (u[0], v[0]) if u[0] and v[0] else '') + ('=' if u[0] and v[0] else '') + (r'\dfrac{%d}{%d}' % (u[1], v[1]) if u[1] and v[1] else '')
    if not (u[0] and v[0] and u[1] and v[1]): cond = r'%d\cdot%s=%d\cdot%s' % (u[0], tp(v[1]), u[1], tp(v[0]))
    if par(u, v):
        k = F(v[0], u[0]) if u[0] else F(v[1], u[1])
        return '$' + cond + '$: $' + Rm(r'\text{sí}') + r'$ \ ($\vec v=%s\vec u$)' % tn(k)
    return r'$\dfrac{%d}{%d}\neq\dfrac{%d}{%d}$: $' % (u[0], v[0], u[1], v[1]) + Rm(r'\text{no}') + '$'
ck([par(u, v) for u, v in pp], [True, True, False, False, True, True])
E.append((1, T(r"Esbrina si són paral·lels els vectors $\vec u$ i $\vec v$:", r"Averigua si son paralelos los vectores $\vec u$ y $\vec v$:") +
          tasks(3, [r'$\vec u=%s$, $\vec v=%s$' % (pt(u), pt(v)) for u, v in pp]), tasks(2, [ps(u, v) for u, v in pp])))
# llibre 66 (variació)
E.append((2, T(r"Calcula $x$ en cada cas perquè els vectors siguen paral·lels:" + tasks(3, [r'$\vec u=(x,3)$, $\vec v=(12,x)$', r'$\vec a=(2,-5)$, $\vec b=(x,10)$', r'$\vec c=(x,x+1)$, $\vec d=(3,4)$']),
                 r"Calcula $x$ en cada caso para que los vectores sean paralelos:" + tasks(3, [r'$\vec u=(x,3)$, $\vec v=(12,x)$', r'$\vec a=(2,-5)$, $\vec b=(x,10)$', r'$\vec c=(x,x+1)$, $\vec d=(3,4)$'])),
          tasks(2, [r'$\dfrac{x}{12}=\dfrac{3}{x}\Rightarrow x^2=36\Rightarrow ' + Rm(r'x=\pm6') + '$', r'$\dfrac{2}{x}=\dfrac{-5}{10}\Rightarrow ' + Rm('x=-4') + '$',
                    r'$4x=3(x+1)\Rightarrow ' + Rm('x=3') + '$'])))
for x in (6, -6): assert par((x, 3), (12, x))
assert par((2, -5), (-4, 10)) and par((3, 4), (3, 4))
# llibre 12 (variació)
E.append((2, T(r"Escriu un vector $\vec u$ amb la mateixa direcció que $\vec v=(-3,9)$, sentit contrari i mòdul la tercera part del de $\vec v$. Quina operació hem d'aplicar a $\vec u$ per a tornar a obtindre $\vec v$?",
                 r"Escribe un vector $\vec u$ con la misma dirección que $\vec v=(-3,9)$, sentido contrario y módulo la tercera parte del de $\vec v$. ¿Qué operación hay que aplicar a $\vec u$ para volver a obtener $\vec v$?"),
          r"$\vec u=-\tfrac13\vec v=" + Rm('(1,-3)') + r"$; \ $" + Rm(r'\vec v=-3\vec u') + "$."))
ck(vmul(F(-1, 3), (-3, 9)), (1, -3))
# nou: equació vectorial
u, v = (1, -5), (2, -1)
x_ = vmul(F(1, 3), vsub(vmul(2, v), u))
ck(vadd(vmul(3, x_), u), vmul(2, v))
E.append((3, T(r"Troba el vector $\vec x$ que compleix $3\vec x+\vec u=2\vec v$, sabent que $\vec u=(1,-5)$ i $\vec v=(2,-1)$.",
                 r"Halla el vector $\vec x$ que cumple $3\vec x+\vec u=2\vec v$, sabiendo que $\vec u=(1,-5)$ y $\vec v=(2,-1)$."),
          r"$3\vec x=2\vec v-\vec u=(4,-2)-(1,-5)=(3,3)\Rightarrow\vec x=" + Rm(pt(x_)) + "$"))

# =====================================================================
# 3. Producte escalar. Vectors perpendiculars
E = sec(T('Producte escalar. Vectors perpendiculars', 'Producto escalar. Vectores perpendiculares'))
pe = [((3, 2), (1, -4)), ((-2, 5), (4, -1)), ((6, -3), (1, 2)), ((0, 3), (-5, 7))]
def dsol(u, v):
    d = dot(u, v)
    w = T('perpendiculars', 'perpendiculares') if d == 0 else T('angle agut', 'ángulo agudo') if d > 0 else T('angle obtús', 'ángulo obtuso')
    return r'$%d\cdot%s+%s\cdot%s=%s$ \ (%s)' % (u[0], tp(v[0]), tp(u[1]), tp(v[1]), Rm(tn(d)), w)
ck([dot(u, v) for u, v in pe], [-5, -13, 0, 21])
E.append((1, T(r"Calcula el producte escalar $\vec u\cdot\vec v$ i indica si els vectors formen un angle agut, recte o obtús:", r"Calcula el producto escalar $\vec u\cdot\vec v$ e indica si los vectores forman un ángulo agudo, recto u obtuso:") +
          tasks(2, [r'$\vec u=%s$, $\vec v=%s$' % (pt(u), pt(v)) for u, v in pe]), tasks(2, [dsol(u, v) for u, v in pe])))
# departament, fitxa 6 ex. 2
A, B, C, D = (8, -4), (1, 5), (7, -2), (3, -8)
AB, CD, DA = vsub(B, A), vsub(D, C), vsub(A, D)
r2 = [vadd(AB, CD), vsub(AB, vmul(3, CD)), dot(vmul(2, AB), CD), dot(vmul(5, AB), vmul(-1, DA)), n2(AB), n2(CD)]
ck(r2, [(-11, 3), (5, 27), -52, -5, 130, 52])
E.append((1, T(r"Fes les operacions següents amb vectors sabent que $A(8,-4)$, $B(1,5)$, $C(7,-2)$ i $D(3,-8)$:", r"Haz las siguientes operaciones con vectores sabiendo que $A(8,-4)$, $B(1,5)$, $C(7,-2)$ y $D(3,-8)$:") +
          tasks(3, [r'$\overrightarrow{AB}+\overrightarrow{CD}$', r'$\overrightarrow{AB}-3\overrightarrow{CD}$', r'$2\overrightarrow{AB}\cdot\overrightarrow{CD}$',
                    r'$5\overrightarrow{AB}\cdot(-\overrightarrow{DA})$', r'$|\overrightarrow{AB}|$', r'$|\overrightarrow{CD}|$']),
          r"$\overrightarrow{AB}=(-7,9)$, \ $\overrightarrow{CD}=(-4,-6)$, \ $\overrightarrow{DA}=(5,4)$." +
          tasks(2, ['$' + Rm(pt(r2[0])) + '$', r'$(-7,9)-(-12,-18)=' + Rm(pt(r2[1])) + '$', r'$(-14,18)\cdot(-4,-6)=56-108=' + Rm('-52') + '$',
                    r'$(-35,45)\cdot(-5,-4)=175-180=' + Rm('-5') + '$', r'$\sqrt{49+81}=' + Rm(r'\sqrt{130}') + r'\approx' + dec(math.sqrt(130)) + '$',
                    r'$\sqrt{16+36}=\sqrt{52}=' + Rm(r'2\sqrt{13}') + r'\approx' + dec(math.sqrt(52)) + '$'])))
# llibre 5/63 (variació): paral·lels, perpendiculars o cap
pq = [((2, 1), (-1, 2)), ((-6, 4), (3, -2)), ((5, 2), (2, 5)), ((4, -6), (9, 6)), ((1, 1), (-3, -3)), ((7, 0), (0, -2))]
def pps(u, v):
    if dot(u, v) == 0: return r'$\vec u\cdot\vec v=%d\cdot%s+%s\cdot%s=0$: $' % (u[0], tp(v[0]), tp(u[1]), tp(v[1])) + Rm(T(r'\text{perpendiculars}', r'\text{perpendiculares}')) + '$'
    if par(u, v): return r'$%d\cdot%s=%s\cdot%s$: $' % (u[0], tp(v[1]), tp(u[1]), tp(v[0])) + Rm(T(r'\text{paral·lels}', r'\text{paralelos}')) + '$'
    return r'$\vec u\cdot\vec v=%s\neq0$ ' % tn(dot(u, v)) + T('i no proporcionals: ', 'y no proporcionales: ') + '$' + Rm(T(r'\text{cap}', r'\text{ninguno}')) + '$'
def pps2(s): return s
ck([('pe' if dot(u, v) == 0 else 'pa' if par(u, v) else 'no') for u, v in pq], ['pe', 'pa', 'no', 'pe', 'pa', 'pe'])
E.append((1, T(r"Determina si aquests parells de vectors són paral·lels, perpendiculars o cap de les dues coses:", r"Determina si estos pares de vectores son paralelos, perpendiculares o ninguna de las dos cosas:") +
          tasks(3, [r'$\vec u=%s$, $\vec v=%s$' % (pt(u), pt(v)) for u, v in pq]), tasks(2, [pps2(pps(u, v)) for u, v in pq])))
# llibre 6 (variació) i perpendiculars a un vector
E.append((2, T(r"Escriu dos vectors perpendiculars a $\vec v=(5,-2)$ i dos de paral·lels, un amb el mateix sentit i l'altre amb sentit contrari. Demostra que, per a qualsevol vector $\vec v=(v_1,v_2)$, el vector $\vec w=(-v_2,v_1)$ és perpendicular a $\vec v$.",
                 r"Escribe dos vectores perpendiculares a $\vec v=(5,-2)$ y dos paralelos, uno con el mismo sentido y otro con sentido contrario. Demuestra que, para cualquier vector $\vec v=(v_1,v_2)$, el vector $\vec w=(-v_2,v_1)$ es perpendicular a $\vec v$."),
          T(r"Perpendiculars: $" + Rm('(2,5)') + r"$ i $" + Rm('(-2,-5)') + r"$ ($10-10=0$). Paral·lels: $" + Rm('(10,-4)') + r"$ (mateix sentit) i $" + Rm('(-5,2)') + r"$ (sentit contrari). \ $\vec v\cdot\vec w=v_1(-v_2)+v_2v_1=" + Rm('0') + "$.",
            r"Perpendiculares: $" + Rm('(2,5)') + r"$ y $" + Rm('(-2,-5)') + r"$ ($10-10=0$). Paralelos: $" + Rm('(10,-4)') + r"$ (mismo sentido) y $" + Rm('(-5,2)') + r"$ (sentido contrario). \ $\vec v\cdot\vec w=v_1(-v_2)+v_2v_1=" + Rm('0') + "$.")))
assert dot((5, -2), (2, 5)) == 0
# llibre 65 (variació)
E.append((2, T(r"Calcula $x$ perquè els vectors siguen perpendiculars:" + tasks(3, [r'$\vec u=(3,x)$, $\vec v=(x+1,-2)$', r'$\vec a=(x,-4)$, $\vec b=(6,3)$', r'$\vec c=(x,2)$, $\vec d=(x,-8)$']),
                 r"Calcula $x$ para que los vectores sean perpendiculares:" + tasks(3, [r'$\vec u=(3,x)$, $\vec v=(x+1,-2)$', r'$\vec a=(x,-4)$, $\vec b=(6,3)$', r'$\vec c=(x,2)$, $\vec d=(x,-8)$'])),
          tasks(2, [r'$3(x+1)-2x=0\Rightarrow ' + Rm('x=-3') + '$', r'$6x-12=0\Rightarrow ' + Rm('x=2') + '$', r'$x^2-16=0\Rightarrow ' + Rm(r'x=\pm4') + '$'])))
assert dot((3, -3), (-2, -2)) == 0 and dot((2, -4), (6, 3)) == 0 and dot((4, 2), (4, -8)) == 0 and dot((-4, 2), (-4, -8)) == 0
# llibre 62 (variació)
a, b, c = (2, -1), (1, 2), (-4, 2)
fg = fig([('v', (0, 0), a, 'accent', r'\vec a', 'below'), ('v', (0, 0), b, 'teal', r'\vec b', 'left'), ('v', (0, 0), c, 'navy', r'\vec c', 'above')], box=(-5, 3, -2, 3), sc=0.42)
E.append((2, T(r"Representa els vectors $\vec a=(2,-1)$, $\vec b=(1,2)$ i $\vec c=(-4,2)$. Quina relació hi ha entre cada parell?", r"Representa los vectores $\vec a=(2,-1)$, $\vec b=(1,2)$ y $\vec c=(-4,2)$. ¿Qué relación hay entre cada par?"),
          cen(fg) + r"$\vec a\cdot\vec b=2-2=0$: $" + Rm(r'\vec a\perp\vec b') + r"$; \ $\vec c=-2\vec a$: $" + Rm(r'\vec a\parallel\vec c') + "$ (" + T("sentit contrari", "sentido contrario") +
          r"); \ $\vec b\cdot\vec c=-4+4=0$: $" + Rm(r'\vec b\perp\vec c') + '$.'))
assert dot(a, b) == 0 and dot(b, c) == 0 and par(a, c)
# nou
E.append((3, T(r"Troba els vectors perpendiculars a $\vec v=(3,4)$ que tenen mòdul 10.", r"Halla los vectores perpendiculares a $\vec v=(3,4)$ que tienen módulo 10."),
          T(r"Un perpendicular és $(-4,3)$, de mòdul 5. Multiplicant per $\pm2$: $" + Rm('(-8,6)') + r"$ i $" + Rm('(8,-6)') + "$.",
            r"Un perpendicular es $(-4,3)$, de módulo 5. Multiplicando por $\pm2$: $" + Rm('(-8,6)') + r"$ y $" + Rm('(8,-6)') + "$.")))
assert dot((3, 4), (-8, 6)) == 0 and n2((-8, 6)) == 100

# =====================================================================
# 4. Aplicacions dels vectors
E = sec(T('Aplicacions dels vectors', 'Aplicaciones de los vectores'))
# departament, fitxa 6 ex. 1
A, B = (4, 0), (-1, 1)
fg = fig([('v', A, B, 'accent', r'\overrightarrow{AB}', 'above'), ('p', A, 'A', 'below'), ('p', B, 'B', 'above left')], box=(-3, 6, -2, 3), sc=0.42)
E.append((1, T(r"Calcula la distància entre els punts $A(4,0)$ i $B(-1,1)$. Representa el vector $\overrightarrow{AB}$. Escriu un vector perpendicular i un de paral·lel a $\overrightarrow{AB}$.",
                 r"Calcula la distancia entre los puntos $A(4,0)$ y $B(-1,1)$. Representa el vector $\overrightarrow{AB}$. Escribe un vector perpendicular y uno paralelo a $\overrightarrow{AB}$."),
          cen(fg) + r"$\overrightarrow{AB}=(-5,1)$, \ $d(A,B)=\sqrt{25+1}=" + Rm(r'\sqrt{26}') + r"\approx" + dec(math.sqrt(26)) + r"$; \ " + T("perpendicular", "perpendicular") + ": $" + Rm('(1,5)') + r"$; \ " + T("paral·lel", "paralelo") + ": $" + Rm('(-10,2)') + "$."))
ck(n2(vsub(B, A)), 26)
# llibre 57 (variació): distàncies
dd = [((1, 2), (4, 6)), ((-3, 5), (2, -7)), ((0, -2), (-4, -2)), ((-1, -1), (2, 2)), ((3, -4), (-2, 1)), ((-6, 0), (0, 8))]
ck([n2(vsub(q, p)) for p, q in dd], [25, 169, 16, 18, 50, 100])
E.append((1, T(r"Calcula la distància entre els punts $A$ i $B$:", r"Calcula la distancia entre los puntos $A$ y $B$:") + tasks(3, [r'$A%s$, $B%s$' % (pt(p), pt(q)) for p, q in dd]),
          tasks(2, ['$' + dres(vsub(q, p)) + '$' for p, q in dd])))
# llibre 72/73 (variació) + departament 3
pm = [((2, 6), (8, 0)), ((-3, 4), (5, -2)), ((1, -5), (-2, 2)), ((0, 7), (-6, -3)), ((2, 1), (-4, 3))]
ck([mid(p, q) for p, q in pm], [(5, 3), (1, 1), (F(-1, 2), F(-3, 2)), (-3, 2), (-1, 2)])
E.append((1, T(r"Calcula el punt mig del segment d'extrems $P$ i $Q$ (l'últim és de la fitxa del departament):", r"Calcula el punto medio del segmento de extremos $P$ y $Q$ (el último es de la ficha del departamento):") +
          tasks(3, [r'$P%s$, $Q%s$' % (pt(p), pt(q)) for p, q in pm]),
          tasks(3, [r'$\left(\frac{%s+%s}{2},\frac{%s+%s}{2}\right)=%s$' % (tn(p[0]), tp(q[0]), tn(p[1]), tp(q[1]), Rm(pt(mid(p, q)))) for p, q in pm])))
# llibre 74 (variació)
am = [((1, 4), (3, 1)), ((-2, 0), (0, 3)), ((4, -3), (1, -1)), ((-5, 2), (-1, -2))]
ex_ = [vsub(vmul(2, m), a) for a, m in am]
ck(ex_, [(5, -2), (2, 6), (-2, 1), (3, -6)])
E.append((1, T(r"$M$ és el punt mig del segment $AB$. Calcula l'extrem $B$:", r"$M$ es el punto medio del segmento $AB$. Calcula el extremo $B$:") + tasks(2, [r'$A%s$, $M%s$' % (pt(a), pt(m)) for a, m in am]),
          tasks(2, [r'$B=A+2\overrightarrow{AM}=%s+2%s=%s$' % (pt(a), pt(vsub(m, a)), Rm(pt(b))) for (a, m), b in zip(am, ex_)])))
# departament 4 + un altre
s4 = vsub(vmul(2, (2, -8)), (-1, 0)); s5 = vsub(vmul(2, (1, 1)), (3, -2))
ck((s4, s5), ((5, -16), (-1, 4)))
E.append((1, T(r"Calcula el punt simètric $A'$ del punt $A(-1,0)$ respecte de $B(2,-8)$. Calcula també el simètric de $P(3,-2)$ respecte de $Q(1,1)$.",
                 r"Calcula el punto simétrico $A'$ del punto $A(-1,0)$ respecto de $B(2,-8)$. Calcula también el simétrico de $P(3,-2)$ respecto de $Q(1,1)$."),
          T(r"$B$ és el punt mig de $AA'$: $\frac{-1+x}{2}=2$, $\frac{0+y}{2}=-8$ $\Rightarrow A'" + Rm('(5,-16)') + r"$. \ $P'=P+2\overrightarrow{PQ}=(3,-2)+2(-2,3)=" + Rm('(-1,4)') + "$.",
            r"$B$ es el punto medio de $AA'$: $\frac{-1+x}{2}=2$, $\frac{0+y}{2}=-8$ $\Rightarrow A'" + Rm('(5,-16)') + r"$. \ $P'=P+2\overrightarrow{PQ}=(3,-2)+2(-2,3)=" + Rm('(-1,4)') + "$.")))
# departament 5 i 6 + llibre 52 (variació)
assert par(vsub((5, 2), (3, 1)), vsub((1, 0), (3, 1)))
assert not par(vsub((1, 5), (-1, 2)), vsub((4, 7), (1, 5)))
assert par(vsub((0, 3), (1, 1)), vsub((2, -1), (1, 1)))
E.append((2, T(r"Punts alineats:" + items(r"Determina si els punts $A(3,1)$, $B(5,2)$ i $C(1,0)$ estan alineats.", r"Calcula el valor de $k$ perquè els punts $A(1,1)$, $B(0,3)$ i $C(2,k)$ estiguen alineats.",
                                           r"Comprova que els punts $P(-1,2)$, $Q(1,5)$ i $R(4,7)$ no estan alineats i que, per tant, formen un triangle."),
                 r"Puntos alineados:" + items(r"Determina si los puntos $A(3,1)$, $B(5,2)$ y $C(1,0)$ están alineados.", r"Calcula el valor de $k$ para que los puntos $A(1,1)$, $B(0,3)$ y $C(2,k)$ estén alineados.",
                                           r"Comprueba que los puntos $P(-1,2)$, $Q(1,5)$ y $R(4,7)$ no están alineados y que, por tanto, forman un triángulo.")),
          items(r"$\overrightarrow{AB}=(2,1)$, $\overrightarrow{AC}=(-2,-1)$: $\frac{2}{-2}=\frac{1}{-1}$: " + Rm(T(r'\text{sí que estan alineats}', r'\text{sí están alineados}')).join('$$'),
                r"$\overrightarrow{AB}=(-1,2)$, $\overrightarrow{AC}=(1,k-1)$: $\frac{1}{-1}=\frac{k-1}{2}\Rightarrow k-1=-2\Rightarrow " + Rm('k=-1') + '$',
                r"$\overrightarrow{PQ}=(2,3)$, $\overrightarrow{QR}=(3,2)$: $\frac23\neq\frac32$: " + Rm(T(r'\text{no estan alineats}', r'\text{no están alineados}')).join('$$'))))
# departament, fitxa de repàs 2 + llibre 54/55 (variació)
D2 = vadd((2, 1), vsub((10, -1), (7, -3)))
D3 = vadd((-2, 1), vsub((4, 0), (1, 3)))
ck((D2, D3), ((5, 3), (1, -2)))
E.append((2, T(r"Paral·lelograms:" + items(r"Calcula el quart vèrtex $B$ del paral·lelogram $ABCD$ si $A(2,1)$, $C(10,-1)$ i $D(7,-3)$.", r"Calcula el punt $D$ perquè $A(-2,1)$, $B(1,3)$, $C(4,0)$ i $D$ siguen els vèrtexs (en aquest ordre) d'un paral·lelogram."),
                 r"Paralelogramos:" + items(r"Calcula el cuarto vértice $B$ del paralelogramo $ABCD$ si $A(2,1)$, $C(10,-1)$ y $D(7,-3)$.", r"Calcula el punto $D$ para que $A(-2,1)$, $B(1,3)$, $C(4,0)$ y $D$ sean los vértices (en este orden) de un paralelogramo.")),
          items(r"$\overrightarrow{AB}=\overrightarrow{DC}=(3,2)\Rightarrow B=A+\overrightarrow{DC}=" + Rm('(5,3)') + '$', r"$\overrightarrow{AD}=\overrightarrow{BC}=(3,-3)\Rightarrow D=" + Rm('(1,-2)') + '$')))
# departament, fitxa de repàs 3
assert dot(vsub((5, -1), (-4, 2)), vsub((-2, 8), (-4, 2))) == 0
E.append((2, T(r"Comprova mitjançant vectors que el triangle de vèrtexs $A(-4,2)$, $B(5,-1)$ i $C(-2,8)$ és rectangle.", r"Comprueba mediante vectores que el triángulo de vértices $A(-4,2)$, $B(5,-1)$ y $C(-2,8)$ es rectángulo."),
          r"$\overrightarrow{AB}=(9,-3)$, $\overrightarrow{AC}=(2,6)$: $\overrightarrow{AB}\cdot\overrightarrow{AC}=18-18=0$. " + T(r"És rectangle en $" + Rm('A') + "$.", r"Es rectángulo en $" + Rm('A') + "$.")))
# departament, fitxa de repàs 4
A, B, C = (4, -2), (5, 2), (9, 1)
D4 = vadd(A, vsub(C, B))
assert dot(vsub(B, A), vsub(C, B)) == 0 and n2(vsub(B, A)) == n2(vsub(C, B)) == 17
ck(D4, (8, -3))
E.append((2, T(r"Els punts $A(4,-2)$, $B(5,2)$ i $C(9,1)$ són vèrtexs d'un quadrat. Troba l'altre vèrtex.", r"Los puntos $A(4,-2)$, $B(5,2)$ y $C(9,1)$ son vértices de un cuadrado. Halla el otro vértice."),
          T(r"$\overrightarrow{AB}=(1,4)$ i $\overrightarrow{BC}=(4,-1)$ són perpendiculars ($4-4=0$) i tenen el mateix mòdul ($\sqrt{17}$): $A$, $B$ i $C$ són consecutius. \ $D=A+\overrightarrow{BC}=" + Rm('(8,-3)') + "$.",
            r"$\overrightarrow{AB}=(1,4)$ y $\overrightarrow{BC}=(4,-1)$ son perpendiculares ($4-4=0$) y tienen el mismo módulo ($\sqrt{17}$): $A$, $B$ y $C$ son consecutivos. \ $D=A+\overrightarrow{BC}=" + Rm('(8,-3)') + "$.")))
# llibre 59 (variació)
Q = [(1, 1), (4, 2), (3, 5), (0, 4)]
sides = [vsub(Q[(i + 1) % 4], Q[i]) for i in range(4)]
assert all(n2(s) == 10 for s in sides) and dot(sides[0], sides[1]) == 0
E.append((2, T(r"Verifica que el quadrilàter de vèrtexs $A(1,1)$, $B(4,2)$, $C(3,5)$ i $D(0,4)$ és un quadrat i calcula'n el perímetre i l'àrea.", r"Verifica que el cuadrilátero de vértices $A(1,1)$, $B(4,2)$, $C(3,5)$ y $D(0,4)$ es un cuadrado y calcula su perímetro y su área."),
          r"$\overrightarrow{AB}=(3,1)$, $\overrightarrow{BC}=(-1,3)$, $\overrightarrow{CD}=(-3,-1)$, $\overrightarrow{DA}=(1,-3)$: " +
          T(r"tots tenen mòdul $\sqrt{10}$ i $\overrightarrow{AB}\cdot\overrightarrow{BC}=-3+3=0$: és un quadrat. ", r"todos tienen módulo $\sqrt{10}$ y $\overrightarrow{AB}\cdot\overrightarrow{BC}=-3+3=0$: es un cuadrado. ") +
          r"$P=" + Rm(r'4\sqrt{10}\approx' + dec(4 * math.sqrt(10)) + r'\ \text{u}') + r"$; \ $S=(\sqrt{10})^2=" + Rm(r'10\ \text{u}^2') + "$."))
# llibre 60 (variació)
R4 = [(2, 5), (0, 2), (2, -1), (4, 2)]
assert len({n2(vsub(R4[(i + 1) % 4], R4[i])) for i in range(4)}) == 1
E.append((2, T(r"Els vèrtexs d'un rombe són $A(2,5)$, $B(0,2)$, $C(2,-1)$ i $D(4,2)$. Comprova que tots els costats mesuren igual i calcula la longitud de les diagonals i l'àrea del rombe.",
                 r"Los vértices de un rombo son $A(2,5)$, $B(0,2)$, $C(2,-1)$ y $D(4,2)$. Comprueba que todos los lados miden lo mismo y calcula la longitud de las diagonales y el área del rombo."),
          T(r"Costats: $(-2,-3)$, $(2,-3)$, $(2,3)$, $(-2,3)$, tots de mòdul $\sqrt{13}$. \ Diagonals: $|\overrightarrow{AC}|=|(0,-6)|=" + Rm('6') + r"$, \ $|\overrightarrow{BD}|=|(4,0)|=" + Rm('4') + r"$. \ $S=\frac{6\cdot4}{2}=" + Rm(r'12\ \text{u}^2') + "$.",
            r"Lados: $(-2,-3)$, $(2,-3)$, $(2,3)$, $(-2,3)$, todos de módulo $\sqrt{13}$. \ Diagonales: $|\overrightarrow{AC}|=|(0,-6)|=" + Rm('6') + r"$, \ $|\overrightarrow{BD}|=|(4,0)|=" + Rm('4') + r"$. \ $S=\frac{6\cdot4}{2}=" + Rm(r'12\ \text{u}^2') + "$.")))
# llibre 61 (variació)
A, B, C = (-2, -1), (4, 2), (1, 5)
ck([n2(vsub(B, A)), n2(vsub(C, B)), n2(vsub(A, C))], [45, 18, 45])
per_ = 2 * math.sqrt(45) + math.sqrt(18)
E.append((2, T(r"Calcula els vectors que formen els costats del triangle de vèrtexs $A(-2,-1)$, $B(4,2)$ i $C(1,5)$, i el seu perímetre. Quin tipus de triangle és segons els costats?",
                 r"Calcula los vectores que forman los lados del triángulo de vértices $A(-2,-1)$, $B(4,2)$ y $C(1,5)$, y su perímetro. ¿Qué tipo de triángulo es según sus lados?"),
          r"$\overrightarrow{AB}=(6,3)$, $|\overrightarrow{AB}|=\sqrt{45}=3\sqrt5$; \ $\overrightarrow{BC}=(-3,3)$, $|\overrightarrow{BC}|=\sqrt{18}=3\sqrt2$; \ $\overrightarrow{CA}=(-3,-6)$, $|\overrightarrow{CA}|=3\sqrt5$. \ $P=" +
          Rm(r'6\sqrt5+3\sqrt2\approx' + dec(per_) + r'\ \text{u}') + r"$; \ " + T("és ", "es ") + "$" + Rm(T(r'\text{isòsceles}', r'\text{isósceles}')) + "$."))
# llibre 76/77 (variació)
c_ = mid((-3, 4), (5, -2)); ck((c_, n2(vsub((5, -2), c_))), ((1, 1), 25))
t_ = mid((-2, 3), (6, -1)); ck(t_, (2, 1))
E.append((2, T(r"Circumferències:" + items(r"Els punts $P(-3,4)$ i $Q(5,-2)$ són els extrems d'un diàmetre d'una circumferència. Calcula'n el centre i el radi.",
                                             r"Dues circumferències del mateix radi són tangents exteriors i tenen els centres en $A(-2,3)$ i $B(6,-1)$. Troba el punt de tangència."),
                 r"Circunferencias:" + items(r"Los puntos $P(-3,4)$ y $Q(5,-2)$ son los extremos de un diámetro de una circunferencia. Calcula su centro y su radio.",
                                             r"Dos circunferencias del mismo radio son tangentes exteriores y tienen los centros en $A(-2,3)$ y $B(6,-1)$. Halla el punto de tangencia.")),
          items(T(r"El centre és el punt mig: $C=" + Rm('(1,1)') + r"$; \ $r=d(C,Q)=\sqrt{16+9}=" + Rm('5') + "$.", r"El centro es el punto medio: $C=" + Rm('(1,1)') + r"$; \ $r=d(C,Q)=\sqrt{16+9}=" + Rm('5') + "$."),
                T(r"Com que els radis són iguals, és el punt mig de $AB$: $" + Rm('(2,1)') + "$.", r"Como los radios son iguales, es el punto medio de $AB$: $" + Rm('(2,1)') + "$."))))
# nous
E.append((3, T(r"Troba el punt $P$ de l'eix d'abscisses que està a la mateixa distància de $A(1,3)$ que de $B(5,1)$.", r"Halla el punto $P$ del eje de abscisas que está a la misma distancia de $A(1,3)$ que de $B(5,1)$."),
          r"$P(x,0)$: $(x-1)^2+9=(x-5)^2+1\Rightarrow -2x+10=-10x+26\Rightarrow 8x=16\Rightarrow x=2$. \ $" + Rm('P(2,0)') + r"$ \ ($d=\sqrt{10}$)."))
assert n2(vsub((2, 0), (1, 3))) == n2(vsub((2, 0), (5, 1))) == 10
A, B, C = (0, 0), (6, 2), (2, 6)
M, N = mid(A, C), mid(B, C)
ck((M, N, vsub(N, M)), ((1, 3), (4, 4), (3, 1)))
E.append((3, T(r"En el triangle de vèrtexs $A(0,0)$, $B(6,2)$ i $C(2,6)$, siguen $M$ i $N$ els punts mitjos dels costats $AC$ i $BC$. Comprova que el segment $MN$ és paral·lel al costat $AB$ i que en mesura la meitat.",
                 r"En el triángulo de vértices $A(0,0)$, $B(6,2)$ y $C(2,6)$, sean $M$ y $N$ los puntos medios de los lados $AC$ y $BC$. Comprueba que el segmento $MN$ es paralelo al lado $AB$ y que mide la mitad."),
          r"$M(1,3)$, $N(4,4)$, $\overrightarrow{MN}=(3,1)=\tfrac12(6,2)=" + Rm(r'\tfrac12\overrightarrow{AB}') + r"$: " + T(r"paral·lels i de mòdul la meitat ($\sqrt{10}$ i $2\sqrt{10}$).", r"paralelos y de módulo la mitad ($\sqrt{10}$ y $2\sqrt{10}$).")))

# =====================================================================
# 5. Equacions vectorial, paramètriques i contínua
E = sec(T('Equacions vectorial, paramètriques i contínua', 'Ecuaciones vectorial, paramétricas y continua'))
# llibre 78/81/87 (variació)
pv = [((2, -1), (3, 4)), ((0, 5), (-2, 1)), ((-4, -3), (1, -5)), ((6, 0), (-3, -3))]
E.append((1, T(r"Escriu les equacions vectorial, paramètriques i contínua de la recta que passa pel punt $A$ i té vector director $\vec v$:", r"Escribe las ecuaciones vectorial, paramétricas y continua de la recta que pasa por el punto $A$ y tiene vector director $\vec v$:") +
          tasks(2, [r'$A%s$, $\vec v=%s$' % (pt(p), pt(d)) for p, d in pv]),
          tasks(2, ['$' + vect(p, d) + r'$\\ $' + param(p, d) + r'$\quad $' + Rm(cont(p, d)) + '$' for p, d in pv], gap='6pt')))
# llibre 79/82/88 (variació)
pp2 = [((1, 2), (4, -1)), ((-2, 0), (3, 4)), ((5, -3), (-1, -6)), ((0, 0), (-4, 6))]
def dvec(p, q):
    d = vsub(q, p); s = prm(d)
    if s[0] < 0 or (s[0] == 0 and s[1] < 0): s = (-s[0], -s[1])
    return d, s
sols = []
for p, q in pp2:
    d, s = dvec(p, q)
    sols.append(r'$\overrightarrow{AB}=%s%s$\\ $%s$\\ $%s$\quad $%s$' % (pt(d), (r'\parallel' + pt(s)) if tuple(s) != tuple(d) else '', vect(p, s), param(p, s), Rm(cont(p, s))))
E.append((1, T(r"Escriu les equacions vectorial, paramètriques i contínua de la recta que passa pels punts $A$ i $B$:", r"Escribe las ecuaciones vectorial, paramétricas y continua de la recta que pasa por los puntos $A$ y $B$:") +
          tasks(2, [r'$A%s$, $B%s$' % (pt(p), pt(q)) for p, q in pp2]), tasks(2, sols, gap='6pt')))
# llibre 80/83 (variació): rectes dibuixades
r1, r2, r3, r4 = l2((-4, -3), (2, 1)), l2((0, 4), (3, -2)), l2((-5, 5), (1, 3)), L(1, 0, -4)
fgl = fig([('l', r1, 'accent', (-5.3, -3.3), 'r'), ('l', r2, 'teal', (3.5, -2.1), 's'), ('l', r3, 'navy', (-5.4, 4.3), 't'), ('l', r4, 'violet', (4.4, -5.3), 'u')], box=(-6, 6, -6, 6), sc=0.42)
E.append((1, T(r"Escriu l'equació vectorial i les paramètriques de les rectes representades. Quina d'elles no es pot escriure en forma contínua? Per què?",
                 r"Escribe la ecuación vectorial y las paramétricas de las rectas representadas. ¿Cuál de ellas no se puede escribir en forma continua? ¿Por qué?") + cen(fgl),
          T(r"(Hi ha moltes respostes correctes: depenen del punt i del vector que es prenga.)", r"(Hay muchas respuestas correctas: dependen del punto y del vector que se tome.)") +
          lst([r'$r$: ' + T('passa per', 'pasa por') + r' $(-4,-3)$ i $(2,1)$: \ $' + Rm(vect((-1, -1), (3, 2))) + r'$, \ $' + param((-1, -1), (3, 2)) + '$',
               r'$s$: ' + T('passa per', 'pasa por') + r' $(0,4)$ i $(1,2)$: \ $' + Rm(vect((0, 4), (1, -2))) + r'$, \ $' + param((0, 4), (1, -2)) + '$',
               r'$t$: ' + T('passa per', 'pasa por') + r' $(-5,5)$ i $(1,3)$: \ $' + Rm(vect((1, 3), (3, -1))) + r'$, \ $' + param((1, 3), (3, -1)) + '$',
               r'$u$: ' + T(r'vertical, passa per $(4,0)$', r'vertical, pasa por $(4,0)$') + r': \ $' + Rm(vect((4, 0), (0, 1))) + r'$, \ $' + param((4, 0), (0, 1)) + '$. ' +
               T(r'El vector director $(0,1)$ té una component nul·la i no podem dividir per 0: la recta és $x=4$.', r'El vector director $(0,1)$ tiene una componente nula y no podemos dividir entre 0: la recta es $x=4$.')]).replace(' i $', T(' i $', ' y $'))))
assert r1.has((-1, -1)) and r1.has((2, 1)) and r2.has((1, 2)) and r3.has((1, 3)) and r3.has((-2, 4))
# llibre 85/86 (variació)
Pq = (3, -1)
lines86 = [(r'(x,y)=(1,3)+\lambda(1,-2)', ldir((1, 3), (1, -2))), (r'\left\{\begin{array}{l}x=5-2\lambda\\ y=2+\lambda\end{array}\right.', ldir((5, 2), (-2, 1))),
           (r'\dfrac{x-7}{4}=\dfrac{y+3}{-2}', ldir((7, -3), (4, -2))), (r'\dfrac{x+1}{2}=\dfrac{y-1}{3}', ldir((-1, 1), (2, 3)))]
ck([r.has(Pq) for _, r in lines86], [True, False, True, False])
E.append((2, T(r"Comprova si el punt $P(3,-1)$ pertany a cadascuna d'aquestes rectes:", r"Comprueba si el punto $P(3,-1)$ pertenece a cada una de estas rectas:") + tasks(2, ['$' + e + '$' for e, _ in lines86], gap='6pt'),
          tasks(2, [r"$3=1+\lambda\Rightarrow\lambda=2$; \ $-1=3-2\lambda\Rightarrow\lambda=2$: " + T("el mateix", "el mismo") + r" $\lambda$, $" + Rm(r'P\in r') + '$',
                    r"$3=5-2\lambda\Rightarrow\lambda=1$; \ $-1=2+\lambda\Rightarrow\lambda=-3$: $" + Rm(r'P\notin r') + '$',
                    r"$\frac{3-7}{4}=-1$, \ $\frac{-1+3}{-2}=-1$: $" + Rm(r'P\in r') + '$',
                    r"$\frac{3+1}{2}=2$, \ $\frac{-1-1}{3}=-\frac23$: $" + Rm(r'P\notin r') + '$'], gap='4pt')))
# nou
lam = F(-7 - 1, -4)
ck((lam, 3 + 2 * lam), (2, 7))
E.append((2, T(r"Donada la recta $r:\left\{\begin{array}{l}x=3+2\lambda\\ y=1-4\lambda\end{array}\right.$" + items(r"Troba tres punts de $r$.", r"Calcula $k$ perquè el punt $(k,-7)$ siga de $r$.", r"Escriu l'equació contínua de $r$ i comprova amb ella el resultat de l'apartat anterior."),
                 r"Dada la recta $r:\left\{\begin{array}{l}x=3+2\lambda\\ y=1-4\lambda\end{array}\right.$" + items(r"Halla tres puntos de $r$.", r"Calcula $k$ para que el punto $(k,-7)$ esté en $r$.", r"Escribe la ecuación continua de $r$ y comprueba con ella el resultado del apartado anterior.")),
          items(r"$\lambda=0,1,-1$: $" + Rm('(3,1)') + r"$, $" + Rm('(5,-3)') + r"$, $" + Rm('(1,5)') + "$",
                r"$-7=1-4\lambda\Rightarrow\lambda=2\Rightarrow k=3+4=" + Rm('7') + "$",
                r"$" + Rm(r'\dfrac{x-3}{2}=\dfrac{y-1}{-4}') + r"$; \ $\frac{7-3}{2}=2=\frac{-7-1}{-4}$\checkmark")))
# llibre: rectes paral·leles als eixos
E.append((2, T(r"Escriu les equacions de les rectes paral·leles als eixos que passen per $P(-2,5)$: en forma vectorial i de manera senzilla. Quines són les equacions dels eixos de coordenades?",
                 r"Escribe las ecuaciones de las rectas paralelas a los ejes que pasan por $P(-2,5)$: en forma vectorial y de manera sencilla. ¿Cuáles son las ecuaciones de los ejes de coordenadas?"),
          T(r"Paral·lela a $OX$: $(x,y)=(-2,5)+\lambda(1,0)$, és a dir, $" + Rm('y=5') + r"$. \ Paral·lela a $OY$: $(x,y)=(-2,5)+\lambda(0,1)$, és a dir, $" + Rm('x=-2') + r"$. \ Eixos: $" + Rm('y=0') + r"$ (eix $OX$) i $" + Rm('x=0') + r"$ (eix $OY$).",
            r"Paralela a $OX$: $(x,y)=(-2,5)+\lambda(1,0)$, es decir, $" + Rm('y=5') + r"$. \ Paralela a $OY$: $(x,y)=(-2,5)+\lambda(0,1)$, es decir, $" + Rm('x=-2') + r"$. \ Ejes: $" + Rm('y=0') + r"$ (eje $OX$) y $" + Rm('x=0') + r"$ (eje $OY$).")))

# =====================================================================
# 6. Pendent. Equacions punt-pendent, explícita i general
E = sec(T('Pendent. Equacions punt-pendent, explícita i general', 'Pendiente. Ecuaciones punto-pendiente, explícita y general'))
sl = [((1, 2), (3, 8)), ((-2, 4), (2, 2)), ((0, -3), (5, -3)), ((4, 1), (4, 6))]
def slsol(p, q):
    if p[0] == q[0]: return T(r'$\Delta x=0$: recta vertical, ', r'$\Delta x=0$: recta vertical, ') + '$' + Rm(T(r'\text{no té pendent}', r'\text{no tiene pendiente}')) + '$'
    m = F(q[1] - p[1], q[0] - p[0])
    return r'$m=\dfrac{%s-%s}{%s-%s}=%s$' % (tn(q[1]), tp(p[1]), tn(q[0]), tp(p[0]), Rm(tn(m)))
E.append((1, T(r"Calcula el pendent de la recta que passa pels punts $A$ i $B$. És creixent o decreixent?", r"Calcula la pendiente de la recta que pasa por los puntos $A$ y $B$. ¿Es creciente o decreciente?") +
          tasks(2, [r'$A%s$, $B%s$' % (pt(p), pt(q)) for p, q in sl]),
          tasks(2, [slsol(p, q) + (' (' + (T('creixent', 'creciente') if F(q[1] - p[1], q[0] - p[0]) > 0 else T('decreixent', 'decreciente') if F(q[1] - p[1], q[0] - p[0]) < 0 else T('horitzontal', 'horizontal')) + ')' if p[0] != q[0] else '') for p, q in sl], gap='4pt')))
# llibre 91 (variació)
mp = [(4, (1, -2)), (-3, (0, 5)), (F(1, 2), (-4, 1)), (F(-2, 3), (3, 0))]
E.append((1, T(r"Escriu l'equació punt-pendent i l'explícita de la recta que té pendent $m$ i passa pel punt $A$:", r"Escribe la ecuación punto-pendiente y la explícita de la recta que tiene pendiente $m$ y pasa por el punto $A$:") +
          tasks(2, [r'$m=%s$, $A%s$' % (tn(m), pt(p)) for m, p in mp]),
          tasks(2, [r'$%s$; \ $%s$' % (ptpend(p, m), Rm(lm(p, m).expl())) for m, p in mp], gap='4pt')))
ck([lm(p, m).expl() for m, p in mp], ['y=4x-6', 'y=-3x+5', r'y=\frac{1}{2}x+3', r'y=-\frac{2}{3}x+2'])
# departament, fitxa de repàs 8
r = L(1, 1, -2)
E.append((1, T(r"L'equació de la recta $r$ és $y=-x+2$." + items(r"Quin és el valor del pendent?", r"Determina les coordenades d'un dels seus vectors directors.", r"Troba dos punts de la recta i dibuixa-la.", r"El punt $A(-1,4)$ pertany a aquesta recta?"),
                 r"La ecuación de la recta $r$ es $y=-x+2$." + items(r"¿Cuál es el valor de la pendiente?", r"Determina las coordenadas de uno de sus vectores directores.", r"Halla dos puntos de la recta y dibújala.", r"¿El punto $A(-1,4)$ pertenece a esta recta?")),
          items('$' + Rm('m=-1') + '$', r'$' + Rm('(1,-1)') + '$', r'$' + Rm('(0,2)') + r'$ i $' + Rm('(2,0)') + '$' + cen(fig([('l', r, 'accent'), ('p', (0, 2), '(0,2)', 'right'), ('p', (2, 0), '(2,0)', 'above right')], box=(-3, 4, -2, 4), sc=0.3)),
                r"$-(-1)+2=3\neq4$: $" + Rm(r'A\notin r') + '$').replace(r'$ i $', T(r'$ i $', r'$ y $'))))
assert not r.has((-1, 4))
# departament, fitxa de repàs 5, 6 i 7; fitxa 6 ex. 7
o5, r5 = eqs((2, 2), (-4, 2)); o6, r6 = eqs((-3, -4), (1, 1)); o7, r7 = eqs((5, -1), (1, 2)); o8, r8 = eqs((1, 0), (2, 6))
ck((r5.t(), r6.t(), r7.t(), r8.t()), ('x+2y-6=0', 'x-y-1=0', '2x-y-11=0', '3x-y-3=0'))
assert r6.has((-1, -2))
E.append((1, T(r"La recta $r$ passa pel punt $P(2,2)$ i té vector director $\vec v=(-4,2)$. Troba totes les seues equacions.", r"La recta $r$ pasa por el punto $P(2,2)$ y tiene vector director $\vec v=(-4,2)$. Halla todas sus ecuaciones."), lst2(o5)))
E.append((1, T(r"Troba les equacions de la recta que passa pels punts $P(-3,-4)$ i $Q(-1,-2)$.", r"Halla las ecuaciones de la recta que pasa por los puntos $P(-3,-4)$ y $Q(-1,-2)$."),
          r"$\overrightarrow{PQ}=(2,2)\parallel(1,1)$, $m=1$." + lst2(o6)))
E.append((1, T(r"La recta $r$ passa pel punt $P(5,-1)$ i té pendent 2. Troba totes les equacions de la recta.", r"La recta $r$ pasa por el punto $P(5,-1)$ y tiene pendiente 2. Halla todas las ecuaciones de la recta."),
          T(r"Vector director $(1,2)$.", r"Vector director $(1,2)$.") + lst2(o7)))
E.append((1, T(r"Escriu l'equació vectorial de la recta $r$ que passa pels punts $A(1,0)$ i $B(3,6)$, i dedueix-ne totes les altres equacions.\label{ex:r7}", r"Escribe la ecuación vectorial de la recta $r$ que pasa por los puntos $A(1,0)$ y $B(3,6)$, y deduce todas las demás ecuaciones.\label{ex:r7}"),
          r"$\overrightarrow{AB}=(2,6)$." + lst2(o8)))
# departament, fitxa de repàs 9
f9 = [(r'\left\{\begin{array}{l}x=2-t\\ y=-3+2t\end{array}\right.', (2, -3), (-1, 2)), (r'(x,y)=(0,3)+t(2,1)', (0, 3), (2, 1)),
      (r'y=3x-1', (0, -1), (1, 3)), (r'y-3=3(x-5)', (5, 3), (1, 3)), (r'2x+y-5=0', (0, 5), (1, -2))]
sol9 = []
for e, p, d in f9:
    o, rr = eqs(p, d)
    sol9.append('$' + e + '$:' + lst2([x.replace(r'\lambda', 't') for x in o]))
ck([eqs(p, d)[1].t() for _, p, d in f9], ['2x+y-1=0', 'x-2y+6=0', '3x-y-1=0', '3x-y-12=0', '2x+y-5=0'])
E.append((2, T(r"Escriu l'equació de les rectes següents en totes les formes possibles:", r"Escribe la ecuación de las rectas siguientes en todas las formas posibles:") + tasks(3, ['$' + e + '$' for e, _, _ in f9], gap='6pt'),
          items(*sol9)))
# departament, fitxa de repàs 10
M = (-2, 1)
f10 = [(r'(x,y)=(3,2)+t(4,-3)', ldir((3, 2), (4, -3)), r'$-2=3+4t\Rightarrow t=-\frac54$; \ $1=2-3t\Rightarrow t=\frac13$'),
       (r'\dfrac{x-5}{2}=\dfrac{3-y}{4}', L(2, 1, -13), r'$\frac{-2-5}{2}=-\frac72$; \ $\frac{3-1}{4}=\frac12$'),
       (r'3x+5y+30=0', L(3, 5, 30), r'$-6+5+30=29\neq0$'), (r'y=\dfrac{x}{2}+2', L(1, -2, 4), r'$\frac{-2}{2}+2=1$\checkmark'),
       (r'y+2=3(x+5)', L(3, -1, 13), r'$1+2=3$; \ $3(-2+5)=9$')]
ck([r.has(M) for _, r, _ in f10], [False, False, False, True, False])
assert L(2, 1, -13).has((5, 3)) and L(2, 1, -13).has((7, -1))
E.append((2, T(r"Dedueix si el punt $M(-2,1)$ pertany o no a cadascuna de les rectes següents:", r"Deduce si el punto $M(-2,1)$ pertenece o no a cada una de las rectas siguientes:") + tasks(3, ['$' + e + '$' for e, _, _ in f10], gap='6pt'),
          items(*[s + ': $' + Rm(r'M\in r' if r.has(M) else r'M\notin r') + '$' for _, r, s in f10])))
# departament, fitxa 6 ex. 13
E.append((1, T(r"Indica un punt i un vector de les rectes:", r"Indica un punto y un vector de las rectas:") +
          tasks(2, [r'$(x,y)=(2,4)+\lambda(5,-3)$', r'$\dfrac{x-3}{3}=\dfrac{y+2}{2}$', r'$\left\{\begin{array}{l}x=-1+9\lambda\\ y=-8-6\lambda\end{array}\right.$', r'$2x-3y+8=0$'], gap='6pt'),
          tasks(2, [r'$' + Rm('(2,4)') + r'$, \ $' + Rm('(5,-3)') + '$', r'$' + Rm('(3,-2)') + r'$, \ $' + Rm('(3,2)') + '$', r'$' + Rm('(-1,-8)') + r'$, \ $' + Rm('(9,-6)') + '$',
                    r'$' + Rm('(-4,0)') + r'$, \ $' + Rm('(3,2)') + r'$ \ ($\vec v=(-B,A)$)'])))
assert L(2, -3, 8).has((-4, 0))
# llibre 94 (variació)
g94 = [L(3, -4, 12), L(2, 1, -5), L(1, 0, -3), L(0, 5, 10)]
def g94s(r):
    if r.B == 0: return T(r'Vertical ($x=3$): ', r'Vertical ($x=3$): ') + T('no té pendent ni ordenada en l\'origen', 'no tiene pendiente ni ordenada en el origen') + r'; \ $\vec v=' + Rm('(0,1)') + r'$, \ $\vec n=' + Rm('(1,0)') + '$'
    return r'$m=%s$, \ $n=%s$, \ $\vec v=%s$, \ $\vec n=%s$' % (Rm(tn(r.m())), Rm(tn(r.nn())), Rm(pt(r.d() if r.d()[0] >= 0 else (-r.d()[0], -r.d()[1]))), Rm(pt(r.n())))
E.append((1, T(r"Calcula el pendent, l'ordenada en l'origen, un vector director i un vector normal de les rectes:", r"Calcula la pendiente, la ordenada en el origen, un vector director y un vector normal de las rectas:") +
          tasks(2, ['$3x-4y+12=0$', '$2x+y-5=0$', '$x-3=0$', '$5y+10=0$']), tasks(1, [g94s(r) for r in g94])))
ck([(g94[0].m(), g94[0].nn()), (g94[1].m(), g94[1].nn()), (g94[3].m(), g94[3].nn())], [(F(3, 4), 3), (-2, 5), (0, -2)])
# llibre 95/96 (variació)
g95 = [('A(2,-3)', 'B(5,1)', l2((2, -3), (5, 1))), ('A(-1,4)', 'B(3,4)', l2((-1, 4), (3, 4))), (r'A(0,-2)', r'\vec v=(3,-1)', ldir((0, -2), (3, -1))), (r'A(4,1)', r'\vec n=(2,-5)', lnorm((4, 1), (2, -5)))]
ck([r.t() for _, _, r in g95], ['4x-3y-17=0', 'y-4=0', 'x+3y+6=0', '2x-5y-3=0'])
s95 = [r"$\overrightarrow{AB}=(3,4)$, $\vec n=(4,-3)$: $4x-3y+C=0$, $8+9+C=0\Rightarrow C=-17$: $" + Rm('4x-3y-17=0') + '$',
       r"$\overrightarrow{AB}=(4,0)$: " + T("recta horitzontal", "recta horizontal") + " $" + Rm('y-4=0') + '$',
       r"$\vec n=(1,3)$: $x+3y+C=0$, $-6+C=0\Rightarrow C=6$: $" + Rm('x+3y+6=0') + '$',
       r"$2x-5y+C=0$, $8-5+C=0\Rightarrow C=-3$: $" + Rm('2x-5y-3=0') + '$']
E.append((2, T(r"Calcula l'equació general de la recta:", r"Calcula la ecuación general de la recta:") +
          tasks(2, [T(r'Que passa per $%s$ i $%s$.', r'Que pasa por $%s$ y $%s$.') % (a, b) if 'B' in b else T(r'Que passa per $%s$ amb $%s$.', r'Que pasa por $%s$ con $%s$.') % (a, b) for a, b, _ in g95]),
          tasks(1, s95)))
# llibre 90/92 (variació)
g90 = [((2, -1), (4, 2)), ((-3, 5), (-2, 6)), ((0, 4), (3, -2)), ((-1, -2), (5, 0))]
ck([ldir(p, d).expl() for p, d in g90], [r'y=\frac{1}{2}x-2', 'y=-3x-4', r'y=-\frac{2}{3}x+4', 'y=-2'])
E.append((1, T(r"Calcula l'equació explícita de la recta que passa pel punt $A$ i té vector director $\vec v$:", r"Calcula la ecuación explícita de la recta que pasa por el punto $A$ y tiene vector director $\vec v$:") +
          tasks(2, [r'$A%s$, $\vec v=%s$' % (pt(p), pt(d)) for p, d in g90]),
          tasks(2, [r'$m=%s$: \ $%s\Rightarrow %s$' % (tn(F(d[1], d[0])), ptpend(p, F(d[1], d[0])), Rm(ldir(p, d).expl())) for p, d in g90], gap='4pt')))
# llibre 100 c, d (variació)
ra = lm((4, 0), F(-3, 2)); rb = L(0, 1, 2); rc = l2((0, 0), (2, -5))
ck((ra.expl(), rc.expl()), (r'y=-\frac{3}{2}x+6', r'y=-\frac{5}{2}x'))
E.append((2, T(r"Calcula l'equació explícita de la recta en cada cas:" + items(r"El pendent és $-\frac32$ i talla l'eix $OX$ en el punt d'abscissa $x=4$.", r"És paral·lela a l'eix $OX$ i la seua ordenada en l'origen és $-2$.", r"Passa per l'origen de coordenades i pel punt $(2,-5)$."),
                 r"Calcula la ecuación explícita de la recta en cada caso:" + items(r"La pendiente es $-\frac32$ y corta el eje $OX$ en el punto de abscisa $x=4$.", r"Es paralela al eje $OX$ y su ordenada en el origen es $-2$.", r"Pasa por el origen de coordenadas y por el punto $(2,-5)$.")),
          items(r"$y-0=-\frac32(x-4)\Rightarrow " + Rm(ra.expl()) + '$', T(r"Pendent 0: $", r"Pendiente 0: $") + Rm('y=-2') + '$', r"$m=-\frac52$, $n=0$: $" + Rm(rc.expl()) + '$')))
# nou
r = L(3, 4, -12)
E.append((3, T(r"La recta $r:3x+4y-12=0$ talla els eixos de coordenades en els punts $P$ i $Q$. Calcula'ls i troba l'àrea i el perímetre del triangle que formen amb l'origen.",
                 r"La recta $r:3x+4y-12=0$ corta los ejes de coordenadas en los puntos $P$ y $Q$. Calcúlalos y halla el área y el perímetro del triángulo que forman con el origen."),
          r"$y=0\Rightarrow x=4$: $" + Rm('P(4,0)') + r"$; \ $x=0\Rightarrow y=3$: $" + Rm('Q(0,3)') + r"$. \ " + T("Triangle rectangle de catets 4 i 3", "Triángulo rectángulo de catetos 4 y 3") +
          r": $S=\frac{4\cdot3}{2}=" + Rm(r'6\ \text{u}^2') + r"$, \ $d(P,Q)=5$, \ $" + Rm(r'P=12\ \text{u}') + "$."))
assert r.has((4, 0)) and r.has((0, 3))

# =====================================================================
# 7. Posició relativa de dues rectes
E = sec(T('Posició relativa de dues rectes', 'Posición relativa de dos rectas'))
# llibre 98 (variació)
p98 = [(L(1, 1, -5), L(2, -1, -1)), (L(3, -2, -4), L(1, 4, 8)), (L(2, 3, 0), L(1, -1, -5)), (L(4, -2, 3), L(2, 2, -3))]
ck([inter(r, s) for r, s in p98], [(2, 3), (0, -2), (3, -2), (0, F(3, 2))])
s98 = [T('Sumant', 'Sumando') + r": $3x=6\Rightarrow x=2,\ y=3$: \ $" + Rm('(2,3)') + '$',
       r"$x=-8-4y\Rightarrow 3(-8-4y)-2y=4\Rightarrow y=-2,\ x=0$: \ $" + Rm('(0,-2)') + '$',
       r"$x=y+5\Rightarrow 2y+10+3y=0\Rightarrow y=-2,\ x=3$: \ $" + Rm('(3,-2)') + '$',
       T('Sumant', 'Sumando') + r": $6x=0\Rightarrow x=0,\ y=\frac32$: \ $" + Rm(r'\left(0,\tfrac32\right)') + '$']
E.append((1, T(r"Calcula el punt de tall de cada parell de rectes:", r"Calcula el punto de corte de cada par de rectas:") +
          tasks(2, [r'$\left\{\begin{array}{l}%s\\ %s\end{array}\right.$' % (r.t(), s.t()) for r, s in p98], gap='6pt'), tasks(2, s98, gap='4pt')))
# llibre 101 (variació)
p101 = [(L(2, -1, 3), L(-4, 2, -6)), (L(1, 3, -2), L(2, 6, 1)), (L(3, -1, 1), L(1, 2, -5)), (r'\tfrac12x+y-1=0', L(1, 2, -2))]
def rat(a, b): return r'\frac{%d}{%d}' % (a, b)
s101 = [r"$\frac{2}{-4}=\frac{-1}{2}=\frac{3}{-6}$: " + '$' + Rm(T(r'\text{coincidents}', r'\text{coincidentes}')) + '$',
        r"$\frac12=\frac36\neq\frac{-2}{1}$: $" + Rm(T(r'\text{paral·leles}', r'\text{paralelas}')) + '$',
        r"$\frac31\neq\frac{-1}{2}$: $" + Rm(T(r'\text{secants}', r'\text{secantes}')) + r"$ " + T('en', 'en') + r" $\left(\frac37,\frac{16}{7}\right)$",
        r"$\frac{1/2}{1}=\frac12=\frac{-1}{-2}$: $" + Rm(T(r'\text{coincidents}', r'\text{coincidentes}')) + '$']
ck([pos(*p101[0]), pos(*p101[1]), pos(*p101[2]), pos(L(1, 2, -2), L(1, 2, -2)), inter(*p101[2])], ['coi', 'par', 'sec', 'coi', (F(3, 7), F(16, 7))])
E.append((1, T(r"Estudia la posició relativa d'aquests parells de rectes comparant-ne els coeficients:", r"Estudia la posición relativa de estos pares de rectas comparando sus coeficientes:") +
          tasks(2, [r'$\left\{\begin{array}{l}%s\\ %s\end{array}\right.$' % (r if isinstance(r, str) else r.t(), s.t()) for r, s in p101], gap='6pt'), tasks(2, s101, gap='4pt')))
# departament, fitxa 6 ex. 11 (a l'apartat d el departament escriu «y = 3/2 − 2»: s'entén y = (3/2)x − 2)
ra, sa = L(2, 3, -5), L(2, -3, -11); rb, sb = L(2, -1, -3), L(-2, 1, -1); rc, sc_ = l2((2, 3), (4, 7)), l2((2, 7), (7, 8)); rd, sd = l2((2, 4), (4, 7)), lm((0, -2), F(3, 2))
ck([inter(ra, sa), pos(rb, sb), rc.t(), sc_.t(), inter(rc, sc_), rd.t(), sd.t(), pos(rd, sd)],
   [(4, -1), 'par', '2x-y-1=0', 'x-5y+33=0', (F(38, 9), F(67, 9)), '3x-2y+2=0', '3x-2y-4=0', 'par'])
E.append((1, T(r"Estudia analíticament la posició relativa dels parells de rectes següents. Si es tallen, calcula el punt de tall:", r"Estudia analíticamente la posición relativa de los siguientes pares de rectas. Si se cortan, calcula el punto de corte:") +
          tasks(2, [r'$r:2x+3y-5=0$\\ $s:2x-3y-11=0$', r'$r:2x-y-3=0$\\ $s:-2x+y-1=0$',
                    T(r'$r$: recta que passa per $A(2,3)$ i $B(4,7)$\\ $s$: recta que passa per $C(2,7)$ i $D(7,8)$', r'$r$: recta que pasa por $A(2,3)$ y $B(4,7)$\\ $s$: recta que pasa por $C(2,7)$ y $D(7,8)$'),
                    T(r'$r$: recta que passa per $A(2,4)$ i $B(4,7)$\\ $s:y=\frac32x-2$', r'$r$: recta que pasa por $A(2,4)$ y $B(4,7)$\\ $s:y=\frac32x-2$')], gap='6pt'),
          items(r"$\frac22\neq\frac{3}{-3}$: " + T('secants', 'secantes') + r". " + T('Sumant', 'Sumando') + r": $4x=16\Rightarrow x=4$, $y=-1$: $" + Rm('(4,-1)') + '$',
                r"$\frac{2}{-2}=\frac{-1}{1}\neq\frac{-3}{-1}$: $" + Rm(T(r'\text{paral·leles}', r'\text{paralelas}')) + '$',
                r"$r:2x-y-1=0$ ($\vec v=(2,4)$), \ $s:x-5y+33=0$ ($\vec v=(5,1)$): " + T('secants', 'secantes') + r". \ $y=2x-1\Rightarrow x-10x+5+33=0\Rightarrow x=\frac{38}{9}$, $y=\frac{67}{9}$: $" + Rm(r'\left(\tfrac{38}{9},\tfrac{67}{9}\right)') + '$',
                r"$r:3x-2y+2=0$ ($m=\frac32$, $y=\frac32x+1$) " + T('i', 'y') + r" $s:3x-2y-4=0$: " + T('mateix pendent i diferent ordenada en l\'origen', 'misma pendiente y distinta ordenada en el origen') + r": $" + Rm(T(r'\text{paral·leles}', r'\text{paralelas}')) + '$')))
# llibre 99/102 (variació)
q1 = (ldir((1, 2), (2, -1)), ldir((3, 1), (-4, 2))); q2 = (ldir((2, 1), (1, -3)), ldir((0, 4), (2, -6))); q3 = (ldir((-1, 3), (2, 1)), L(1, -1, 1)); q4 = (L(2, 1, -4), ldir((1, 1), (1, -1)))
ck([pos(*q1), pos(*q2), inter(*q3), inter(*q4)], ['coi', 'par', (5, 6), (2, 0)])
E.append((2, T(r"Estudia la posició relativa de les rectes i, si es tallen, troba el punt de tall:", r"Estudia la posición relativa de las rectas y, si se cortan, halla el punto de corte:") +
          tasks(2, [r'$r:(x,y)=(1,2)+\lambda(2,-1)$\\ $s:\dfrac{x-3}{-4}=\dfrac{y-1}{2}$', r'$r:\left\{\begin{array}{l}x=2+\lambda\\ y=1-3\lambda\end{array}\right.$\\ $s:(x,y)=(0,4)+\mu(2,-6)$',
                    r'$r:\left\{\begin{array}{l}x=-1+2\lambda\\ y=3+\lambda\end{array}\right.$\\ $s:x-y+1=0$', r'$r:2x+y-4=0$\\ $s:(x,y)=(1,1)+\lambda(1,-1)$'], gap='8pt'),
          items(T(r"$\vec v_r=(2,-1)$, $\vec v_s=(-4,2)$: paral·lels. $(1,2)\in s$? $\frac{1-3}{-4}=\frac12$, $\frac{2-1}{2}=\frac12$: sí, $" + Rm(r'\text{coincidents}') + '$',
                  r"$\vec v_r=(2,-1)$, $\vec v_s=(-4,2)$: paralelos. ¿$(1,2)\in s$? $\frac{1-3}{-4}=\frac12$, $\frac{2-1}{2}=\frac12$: sí, $" + Rm(r'\text{coincidentes}') + '$'),
                T(r"$\vec v_r=(1,-3)$, $\vec v_s=(2,-6)$: paral·lels. $(2,1)\in s$? $2=2\mu\Rightarrow\mu=1$, $1=4-6\mu\Rightarrow\mu=\frac12$: no, $" + Rm(r'\text{paral·leles}') + '$',
                  r"$\vec v_r=(1,-3)$, $\vec v_s=(2,-6)$: paralelos. ¿$(2,1)\in s$? $2=2\mu\Rightarrow\mu=1$, $1=4-6\mu\Rightarrow\mu=\frac12$: no, $" + Rm(r'\text{paralelas}') + '$'),
                T(r"$\vec v_r=(2,1)$, $\vec v_s=(1,1)$: secants. Substituïm $r$ en $s$: $-1+2\lambda-3-\lambda+1=0\Rightarrow\lambda=3$: $" + Rm('(5,6)') + '$',
                  r"$\vec v_r=(2,1)$, $\vec v_s=(1,1)$: secantes. Sustituimos $r$ en $s$: $-1+2\lambda-3-\lambda+1=0\Rightarrow\lambda=3$: $" + Rm('(5,6)') + '$'),
                T(r"$\vec v_r=(-1,2)$, $\vec v_s=(1,-1)$: secants. $2(1+\lambda)+(1-\lambda)-4=0\Rightarrow\lambda=1$: $" + Rm('(2,0)') + '$',
                  r"$\vec v_r=(-1,2)$, $\vec v_s=(1,-1)$: secantes. $2(1+\lambda)+(1-\lambda)-4=0\Rightarrow\lambda=1$: $" + Rm('(2,0)') + '$'))))
# llibre 99 b (variació)
r_, s_ = L(3, -2, -7), L(1, 1, -5)
ck(inter(r_, s_), (F(17, 5), F(8, 5)))
E.append((2, T(r"Determina el punt de tall de les rectes $r:\dfrac{x-1}{2}=\dfrac{y+2}{3}$ i $s:y-1=-(x-4)$, passant abans les dues a forma general.", r"Determina el punto de corte de las rectas $r:\dfrac{x-1}{2}=\dfrac{y+2}{3}$ y $s:y-1=-(x-4)$, pasando antes las dos a forma general."),
          r"$r:3x-3=2y+4\Rightarrow 3x-2y-7=0$; \ $s:y-1=-x+4\Rightarrow x+y-5=0$. \ $y=5-x\Rightarrow 3x-10+2x-7=0\Rightarrow x=\frac{17}{5}$, $y=\frac85$: $" + Rm(r'\left(\tfrac{17}{5},\tfrac85\right)') + '$'))
# llibre 34 (variació)
E.append((2, T(r"Paràmetres:" + items(r"Quant ha de valdre $a$ perquè les rectes $r:y=ax-3$ i $s:\dfrac{x-1}{3}=\dfrac{y+2}{-6}$ siguen paral·leles?", r"Quant ha de valdre $b$ perquè $3x+by-2=0$ i $6x-4y+1=0$ siguen paral·leles? Poden ser coincidents per a algun valor de $b$?"),
                 r"Parámetros:" + items(r"¿Cuánto tiene que valer $a$ para que las rectas $r:y=ax-3$ y $s:\dfrac{x-1}{3}=\dfrac{y+2}{-6}$ sean paralelas?", r"¿Cuánto tiene que valer $b$ para que $3x+by-2=0$ y $6x-4y+1=0$ sean paralelas? ¿Pueden ser coincidentes para algún valor de $b$?")),
          items(r"$m_s=\frac{-6}{3}=-2$, $m_r=a$: $" + Rm('a=-2') + T(r"$ (i $r\neq s$: $(1,-2)\notin r$)", r"$ (y $r\neq s$: $(1,-2)\notin r$)"),
                r"$\frac36=\frac{b}{-4}\Rightarrow " + Rm('b=-2') + T(r"$. No poden ser coincidents: $\frac{-2}{1}\neq\frac12$.", r"$. No pueden ser coincidentes: $\frac{-2}{1}\neq\frac12$."))))
assert not L(2, 1, 3).has((1, -2)) and pos(L(3, -2, -2), L(6, -4, 1)) == 'par'
# nous
ck((pos(L(-6, 3, -12), L(2, -1, 4)), inter(L(1, 1, -3), L(2, -1, 0))), ('coi', (1, 2)))
E.append((3, T(r"Problemes amb paràmetres:" + items(r"Calcula $a$ i $b$ perquè les rectes $ax+3y+b=0$ i $2x-y+4=0$ siguen coincidents.", r"Troba $m$ perquè les tres rectes $x+y-3=0$, $2x-y=0$ i $mx+2y-5=0$ passen per un mateix punt."),
                 r"Problemas con parámetros:" + items(r"Calcula $a$ y $b$ para que las rectas $ax+3y+b=0$ y $2x-y+4=0$ sean coincidentes.", r"Halla $m$ para que las tres rectas $x+y-3=0$, $2x-y=0$ y $mx+2y-5=0$ pasen por un mismo punto.")),
          items(r"$\frac a2=\frac{3}{-1}=\frac b4\Rightarrow " + Rm('a=-6') + r",\ " + Rm('b=-12') + '$',
                T(r"Punt de tall de les dues primeres: sumant, $3x-3=0$, $(1,2)$. Substituint en la tercera: $m+4-5=0\Rightarrow " + Rm('m=1') + '$',
                  r"Punto de corte de las dos primeras: sumando, $3x-3=0$, $(1,2)$. Sustituyendo en la tercera: $m+4-5=0\Rightarrow " + Rm('m=1') + '$'))))

# =====================================================================
# 8. Rectes paral·leles i perpendiculars. Mediatriu
E = sec(T('Rectes paral·leles i perpendiculars. Mediatriu', 'Rectas paralelas y perpendiculares. Mediatriz'))
# departament, fitxa 6 ex. 8
s8 = lm((4, 4), F(1, 2)); r7 = l2((1, 0), (3, 6))
ck((s8.expl(), inter(s8, r7)), (r'y=\frac{1}{2}x+2', (2, 3)))
E.append((1, T(r"Escriu l'equació de la recta $s$, paral·lela a $y=\frac12x$, que passa pel punt $A(4,4)$. Calcula el punt de tall de la recta $s$ amb la recta $r$ de l'exercici \ref{ex:r7}.",
                 r"Escribe la ecuación de la recta $s$, paralela a $y=\frac12x$, que pasa por el punto $A(4,4)$. Calcula el punto de corte de la recta $s$ con la recta $r$ del ejercicio \ref{ex:r7}."),
          r"$m=\frac12$: $y-4=\frac12(x-4)\Rightarrow " + Rm(r'y=\tfrac12x+2') + r"$. \ $r:y=3x-3$: $3x-3=\frac12x+2\Rightarrow x=2$, $y=3$: $" + Rm('(2,3)') + '$'))
# departament, fitxa 6 ex. 9 i 10
E.append((1, T(r"Calcula l'equació general de la recta perpendicular a $3x-y=1$ que passa pel punt $A(0,1)$.", r"Calcula la ecuación general de la recta perpendicular a $3x-y=1$ que pasa por el punto $A(0,1)$."),
          r"$x+3y+K=0$; \ $0+3+K=0\Rightarrow K=-3$: \ $" + Rm('x+3y-3=0') + '$'))
E.append((1, T(r"Calcula l'equació de la recta paral·lela a la recta $2x-3y+4=0$ que passa pel punt $A(-1,2)$.", r"Calcula la ecuación de la recta paralela a la recta $2x-3y+4=0$ que pasa por el punto $A(-1,2)$."),
          r"$2x-3y+K=0$; \ $-2-6+K=0\Rightarrow K=8$: \ $" + Rm('2x-3y+8=0') + '$'))
assert lnorm((0, 1), (1, 3)).t() == 'x+3y-3=0' and lnorm((-1, 2), (2, -3)).t() == '2x-3y+8=0'
# departament, fitxa 6 ex. 12
r12 = L(3, 1, -2); s12 = lnorm((2, -1), (3, 1)); t12 = lnorm((2, -1), (1, -3))
ck((s12.t(), t12.t(), inter(r12, t12)), ('3x+y-5=0', 'x-3y-5=0', (F(11, 10), F(-13, 10))))
E.append((2, T(r"Donada la recta $r:3x+y-2=0$, calcula la recta $s$ paral·lela a $r$ i la recta $t$ perpendicular a $r$ que passen totes dues pel punt $P(2,-1)$. Calcula el punt de tall de les rectes $r$ i $t$.",
                 r"Dada la recta $r:3x+y-2=0$, calcula la recta $s$ paralela a $r$ y la recta $t$ perpendicular a $r$ que pasan ambas por el punto $P(2,-1)$. Calcula el punto de corte de las rectas $r$ y $t$."),
          r"$s:3x+y+K=0$, $6-1+K=0$: $" + Rm('3x+y-5=0') + r"$. \ $t:x-3y+K=0$, $2+3+K=0$: $" + Rm('x-3y-5=0') + r"$. \ $y=2-3x\Rightarrow x-6+9x-5=0\Rightarrow x=\frac{11}{10}$, $y=-\frac{13}{10}$: $" +
          Rm(r'\left(\tfrac{11}{10},-\tfrac{13}{10}\right)') + '$'))
# departament, fitxa 6 ex. 14
med = lnorm(mid((4, 0), (-2, 6)), vsub((-2, 6), (4, 0)))
ck(med.t(), 'x-y+2=0')
E.append((1, T(r"Calcula l'equació de la recta mediatriu del segment format pels punts $A(4,0)$ i $B(-2,6)$.", r"Calcula la ecuación de la recta mediatriz del segmento formado por los puntos $A(4,0)$ y $B(-2,6)$."),
          r"$M(1,3)$, $\overrightarrow{AB}=(-6,6)\parallel(1,-1)$ " + T('(vector normal)', '(vector normal)') + r": $x-y+K=0$, $1-3+K=0$: $" + Rm('x-y+2=0') + '$'))
# llibre 35 (variació)
P_ = (-2, 3)
l35 = [L(2, 5, -1), L(1, -4, 3), L(-3, 1, 2), L(6, 2, -7)]
def ps35(r):
    pa = lnorm(P_, r.n()); pe = lnorm(P_, (r.B, -r.A))
    return T('paral·lela', 'paralela') + r': $' + Rm(pa.t()) + r'$; \ perpendicular: $' + Rm(pe.t()) + '$'
ck([(lnorm(P_, r.n()).t(), lnorm(P_, (r.B, -r.A)).t()) for r in l35], [('2x+5y-11=0', '5x-2y+16=0'), ('x-4y+14=0', '4x+y+5=0'), ('3x-y+9=0', 'x+3y-7=0'), ('3x+y+3=0', 'x-3y+11=0')])
E.append((1, T(r"Calcula les equacions d'una recta paral·lela i d'una perpendicular a cadascuna d'aquestes rectes que passen pel punt $P(-2,3)$:", r"Calcula las ecuaciones de una recta paralela y de una perpendicular a cada una de estas rectas que pasen por el punto $P(-2,3)$:") +
          tasks(4, ['$2x+5y-1=0$', '$x-4y+3=0$', '$-3x+y+2=0$', '$6x+2y-7=0$']), tasks(1, [ps35(r) for r in l35])))
# llibre 104/106 (variació)
ra = lm((2, -4), -3); rb = lm((4, 1), F(-1, 4))
ck((ra.expl(), rb.expl()), ('y=-3x+2', r'y=-\frac{1}{4}x+2'))
E.append((1, T(r"Rectes en forma explícita:" + items(r"Troba l'equació de la recta paral·lela a $y=-3x+1$ que passa pel punt $B(2,-4)$.", r"Determina l'equació de la recta que passa pel punt $A(4,1)$ i és perpendicular a la recta $y=4x-5$."),
                 r"Rectas en forma explícita:" + items(r"Halla la ecuación de la recta paralela a $y=-3x+1$ que pasa por el punto $B(2,-4)$.", r"Determina la ecuación de la recta que pasa por el punto $A(4,1)$ y es perpendicular a la recta $y=4x-5$.")),
          items(r"$m=-3$: $y+4=-3(x-2)\Rightarrow " + Rm('y=-3x+2') + '$', r"$m'=-\frac14$: $y-1=-\frac14(x-4)\Rightarrow " + Rm(r'y=-\tfrac14x+2') + '$')))
# llibre 105/107 (variació)
E.append((2, T(r"Escriu les equacions demanades:" + items(r"Equacions paramètriques de la recta paral·lela a $r:\left\{\begin{array}{l}x=3+2t\\ y=-1-5t\end{array}\right.$ que passa per $C(1,4)$.",
                                                       r"Equació contínua de la recta perpendicular a $\dfrac{x+1}{4}=\dfrac{y-2}{-1}$ que passa per $B(0,-3)$."),
                 r"Escribe las ecuaciones pedidas:" + items(r"Ecuaciones paramétricas de la recta paralela a $r:\left\{\begin{array}{l}x=3+2t\\ y=-1-5t\end{array}\right.$ que pasa por $C(1,4)$.",
                                                       r"Ecuación continua de la recta perpendicular a $\dfrac{x+1}{4}=\dfrac{y-2}{-1}$ que pasa por $B(0,-3)$.")),
          items(T(r"Mateix vector director $(2,-5)$: $" + Rm(param((1, 4), (2, -5), 't')) + '$', r"Mismo vector director $(2,-5)$: $" + Rm(param((1, 4), (2, -5), 't')) + '$'),
                T(r"Director perpendicular a $(4,-1)$: $(1,4)$. \ $" + Rm(r'\dfrac{x}{1}=\dfrac{y+3}{4}') + '$', r"Director perpendicular a $(4,-1)$: $(1,4)$. \ $" + Rm(r'\dfrac{x}{1}=\dfrac{y+3}{4}') + '$'))))
assert dot((4, -1), (1, 4)) == 0
# llibre 108/109 (variació)
X1 = inter(L(2, -1, -1), L(1, 1, -5)); X2 = inter(L(1, -1, 1), L(2, 1, -7))
ck((X1, X2), ((2, 3), (2, 3)))
E.append((2, T(r"Rectes que passen per un punt de tall:" + items(r"Calcula l'equació de la recta paral·lela a $\dfrac{x-2}{3}=\dfrac{y}{-2}$ que passa per la intersecció de les rectes $y=2x-1$ i $x+y-5=0$.",
                                                                r"Escriu l'equació de la recta perpendicular a $\left\{\begin{array}{l}x=1+2t\\ y=-t\end{array}\right.$ que passa pel punt d'intersecció de les rectes $x-y+1=0$ i $2x+y-7=0$."),
                 r"Rectas que pasan por un punto de corte:" + items(r"Calcula la ecuación de la recta paralela a $\dfrac{x-2}{3}=\dfrac{y}{-2}$ que pasa por la intersección de las rectas $y=2x-1$ y $x+y-5=0$.",
                                                                r"Escribe la ecuación de la recta perpendicular a $\left\{\begin{array}{l}x=1+2t\\ y=-t\end{array}\right.$ que pasa por el punto de intersección de las rectas $x-y+1=0$ y $2x+y-7=0$.")),
          items(r"$2x-1=5-x\Rightarrow x=2$, $y=3$; \ " + T('director', 'director') + r" $(3,-2)$: \ $" + Rm(r'\dfrac{x-2}{3}=\dfrac{y-3}{-2}') + '$',
                T(r"Sumant: $3x-6=0\Rightarrow(2,3)$; director perpendicular a $(2,-1)$: $(1,2)$: \ $" + Rm('(x,y)=(2,3)+t(1,2)') + '$', r"Sumando: $3x-6=0\Rightarrow(2,3)$; director perpendicular a $(2,-1)$: $(1,2)$: \ $" + Rm('(x,y)=(2,3)+t(1,2)') + '$'))))
# llibre 39/40 (variació)
r39 = lm((0, 2), F(-2, 3))
ck((lm((3, -1), F(-2, 3)).expl(), lm((0, 0), F(3, 2)).expl()), (r'y=-\frac{2}{3}x+1', r'y=\frac{3}{2}x'))
E.append((2, T(r"Considera la recta $r:y=-\frac23x+2$." + items(r"Calcula l'equació explícita de la paral·lela a $r$ que passa per $P(3,-1)$.", r"Determina l'equació punt-pendent de la perpendicular a $r$ que passa per l'origen.",
                                                                  r"Escriu en forma contínua la paral·lela a $r$ que passa per $Q(0,5)$.", r"Calcula la paral·lela i la perpendicular a la recta $y=-4$ que passen per $(3,2)$."),
                 r"Considera la recta $r:y=-\frac23x+2$." + items(r"Calcula la ecuación explícita de la paralela a $r$ que pasa por $P(3,-1)$.", r"Determina la ecuación punto-pendiente de la perpendicular a $r$ que pasa por el origen.",
                                                                  r"Escribe en forma continua la paralela a $r$ que pasa por $Q(0,5)$.", r"Calcula la paralela y la perpendicular a la recta $y=-4$ que pasan por $(3,2)$.")),
          items(r"$y+1=-\frac23(x-3)\Rightarrow " + Rm(r'y=-\tfrac23x+1') + '$', r"$m'=\frac32$: \ $" + Rm(r'y-0=\tfrac32(x-0)') + r"$, " + T('és a dir', 'es decir') + r" $y=\frac32x$",
                T(r"Vector director $(3,-2)$: \ $", r"Vector director $(3,-2)$: \ $") + Rm(r'\dfrac{x}{3}=\dfrac{y-5}{-2}') + '$',
                T(r"$y=-4$ és horitzontal: paral·lela $" + Rm('y=2') + r"$, perpendicular $" + Rm('x=3') + '$', r"$y=-4$ es horizontal: paralela $" + Rm('y=2') + r"$, perpendicular $" + Rm('x=3') + '$'))))
# mediatriu (nou)
A, B = (-3, 1), (5, -3)
mm = lnorm(mid(A, B), vsub(B, A))
ck((mid(A, B), mm.t(), n2(vsub((3, 3), A)), n2(vsub((3, 3), B))), ((1, -1), '2x-y-3=0', 40, 40))
E.append((2, T(r"Calcula la mediatriu del segment d'extrems $A(-3,1)$ i $B(5,-3)$. Comprova que el punt $P(3,3)$ és de la mediatriu i que està a la mateixa distància de $A$ que de $B$.",
                 r"Calcula la mediatriz del segmento de extremos $A(-3,1)$ y $B(5,-3)$. Comprueba que el punto $P(3,3)$ está en la mediatriz y que está a la misma distancia de $A$ que de $B$."),
          r"$M(1,-1)$, $\overrightarrow{AB}=(8,-4)\parallel(2,-1)$: $2x-y+K=0$, $2+1+K=0$: $" + Rm('2x-y-3=0') + r"$. \ $6-3-3=0$\checkmark; \ $d(P,A)=\sqrt{36+4}=\sqrt{40}=d(P,B)=\sqrt{4+36}$\checkmark"))
# altura d'un triangle (nou)
A, B, C = (1, 1), (7, 3), (3, 7)
hC = lnorm(C, vsub(B, A)); rAB = l2(A, B); H = inter(hC, rAB)
ck((hC.t(), rAB.t(), H, n2(vsub(C, H)), n2(vsub(B, A))), ('3x+y-16=0', 'x-3y+2=0', (F(23, 5), F(11, 5)), F(128, 5), 40))
E.append((3, T(r"En el triangle de vèrtexs $A(1,1)$, $B(7,3)$ i $C(3,7)$, calcula l'equació de l'altura que surt de $C$ (la perpendicular a $AB$ que passa per $C$), el peu $H$ d'aquesta altura i l'àrea del triangle.",
                 r"En el triángulo de vértices $A(1,1)$, $B(7,3)$ y $C(3,7)$, calcula la ecuación de la altura que sale de $C$ (la perpendicular a $AB$ que pasa por $C$), el pie $H$ de esta altura y el área del triángulo."),
          r"$\overrightarrow{AB}=(6,2)\parallel(3,1)$. " + T("Altura", "Altura") + r": $3x+y+K=0$, $9+7+K=0$: $" + Rm('3x+y-16=0') + r"$. \ " + T("Recta", "Recta") + r" $AB$: $x-3y+2=0$. \ $x=3y-2\Rightarrow 10y-22=0$: $" +
          Rm(r'H\left(\tfrac{23}{5},\tfrac{11}{5}\right)') + r"$. \ $h=|\overrightarrow{HC}|=\sqrt{\tfrac{64}{25}+\tfrac{576}{25}}=\tfrac{8\sqrt{10}}{5}$, \ $|\overrightarrow{AB}|=2\sqrt{10}$, \ $S=\frac12\cdot2\sqrt{10}\cdot\frac{8\sqrt{10}}{5}=" + Rm(r'16\ \text{u}^2') + '$'))
assert F(1, 2) * F(1) * 2 * 8 * 10 / 5 == 16
# rectangle / quadrat (nou)
A, B = (-1, 0), (3, 2)
pB = lnorm(B, vsub(B, A)); Cq = (1, 6)
assert pB.t() == '2x+y-8=0' and pB.has(Cq)
Dq = vadd(A, vsub(Cq, B))
ck((Dq, n2(vsub(B, A)), n2(vsub(Cq, B))), ((-3, 4), 20, 20))
E.append((3, T(r"Els punts $A(-1,0)$ i $B(3,2)$ són dos vèrtexs consecutius d'un rectangle $ABCD$. El vèrtex $C$ és sobre la perpendicular a $AB$ que passa per $B$ i té abscissa $x=1$. Calcula $C$ i $D$, i comprova que, de fet, $ABCD$ és un quadrat.",
                 r"Los puntos $A(-1,0)$ y $B(3,2)$ son dos vértices consecutivos de un rectángulo $ABCD$. El vértice $C$ está sobre la perpendicular a $AB$ que pasa por $B$ y tiene abscisa $x=1$. Calcula $C$ y $D$, y comprueba que, de hecho, $ABCD$ es un cuadrado."),
          r"$\overrightarrow{AB}=(4,2)\parallel(2,1)$; " + T('perpendicular per', 'perpendicular por') + r" $B$: $2x+y-8=0$; \ $x=1\Rightarrow y=6$: $" + Rm('C(1,6)') + r"$. \ $D=A+\overrightarrow{BC}=(-1,0)+(-2,4)=" + Rm('D(-3,4)') + r"$. \ $|\overrightarrow{AB}|=|\overrightarrow{BC}|=\sqrt{20}$: " + T("costats consecutius iguals i perpendiculars, és un quadrat (d'àrea 20 u²).", "lados consecutivos iguales y perpendiculares, es un cuadrado (de área 20 u²).")))

PRE = r'''\usetikzlibrary{arrows.meta}
\usepackage{multicol}
\usepackage{enumitem}
\definecolor{violet}{HTML}{7C3AED}
\definecolor{orange}{HTML}{EA8A1F}
'''
TIT = T('Vectors i rectes', 'Vectores y rectas')
build(HERE, 6, TIT, S,
      T("vectors, components, mòdul, producte escalar, punt mig, distància, punts alineats, equacions de la recta, pendent, posició relativa, rectes perpendiculars, mediatriu",
        "vectores, componentes, módulo, producto escalar, punto medio, distancia, puntos alineados, ecuaciones de la recta, pendiente, posición relativa, paralelas, perpendiculares, mediatriz"),
      T(r"Resol-los al quadern mostrant tots els passos. Fes un dibuix aproximat en uns eixos de coordenades sempre que t'ajude: et permet detectar errors. Dona els resultats de manera exacta (fraccions i arrels) i, si cal, també aproximats. La fitxa recull tots els exercicis de les fitxes del departament i n'afegeix de nous.",
        r"Resuélvelos en el cuaderno mostrando todos los pasos. Haz un dibujo aproximado en unos ejes de coordenadas siempre que te ayude: te permite detectar errores. Da los resultados de manera exacta (fracciones y raíces) y, si hace falta, también aproximados. La ficha recoge todos los ejercicios de las fichas del departamento y añade otros nuevos."),
      T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Quan una recta es pot escriure de moltes maneres (amb un altre punt o un altre vector director), la teua resposta pot ser diferent i igualment correcta: comprova-ho passant-la a forma general. Pots comprovar molts resultats amb les eines interactives dels apunts de la unitat i amb el laboratori del triangle.",
        r"Intenta resolver cada ejercicio antes de mirar su solución. Cuando una recta se puede escribir de muchas maneras (con otro punto u otro vector director), tu respuesta puede ser diferente e igualmente correcta: compruébalo pasándola a forma general. Puedes comprobar muchos resultados con las herramientas interactivas de los apuntes de la unidad y con el laboratorio del triángulo."),
      PRE, lang='es' if ES else 'va')
