# Genera t5-fitxa-exercicis.tex i t5-fitxa-solucions.tex (1r Batxillerat MI, Unitat 5: Geometria analítica en el pla)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Totes les solucions es calculen ací amb fraccions exactes (rectes, punts de tall, distàncies, àrees…) i CHK (al final)
# les compara amb els valors esperats. Algunes solucions porten la figura dibuixada amb TikZ.
# (Les paraules clau del PDF no poden portar «·»: amb hyperref, el preàmbul no compila.)
# Ús: python3 genera.py && pdflatex t5-fitxa-exercicis.tex (dues vegades) && pdflatex t5-fitxa-solucions.tex (dues vegades)
import os, re, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- nombres ----------
def tn(x):
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    return ('-' if x < 0 else '') + r'\frac{%d}{%d}' % (abs(x.numerator), x.denominator)
def tp(x): return '(' + tn(x) + ')' if F(x) < 0 else tn(x)
def pt(p): return r'(%s,\,%s)' % (tn(p[0]), tn(p[1]))
def dec(x, k=2):
    s = ('%.*f' % (k, float(x))).rstrip('0').rstrip('.')
    return s.replace('.', '{,}')
def surd(n):
    a, b, i = 1, n, 2
    while i * i <= b:
        while b % (i * i) == 0: b //= i * i; a *= i
        i += 1
    return a, b
def sq(n):
    if n == 0: return '0'
    a, b = surd(n)
    return str(a) if b == 1 else ('' if a == 1 else str(a)) + r'\sqrt{%d}' % b
def droot(num, S):
    """num/√S racionalitzat"""
    a, b = surd(S)
    f = F(num, a * (1 if b == 1 else b))
    if b == 1: return tn(f)
    top = ('' if abs(f.numerator) == 1 else str(abs(f.numerator))) + r'\sqrt{%d}' % b
    return ('-' if f < 0 else '') + (top if f.denominator == 1 else r'\frac{%s}{%d}' % (top, f.denominator))
def ap(x): return r'\approx ' + dec(x)
def dms(x):
    s = round(x * 3600); d, m, q = s // 3600, (s % 3600) // 60, s % 60
    return '%d^\\circ' % d + ("%d'" % m if m or q else '') + ("%d''" % q if q else '')

# ---------- vectors i rectes ----------
def vsub(p, q): return (F(p[0]) - F(q[0]), F(p[1]) - F(q[1]))
def vadd(p, q): return (F(p[0]) + F(q[0]), F(p[1]) + F(q[1]))
def vmul(k, p): return (F(k) * p[0], F(k) * p[1])
def dot(u, v): return F(u[0]) * v[0] + F(u[1]) * v[1]
def n2(u): return dot(u, u)
def mid(p, q): return ((F(p[0]) + q[0]) / 2, (F(p[1]) + q[1]) / 2)
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
def ldir(p, d): return L(d[1], -F(d[0]), F(d[0]) * F(p[1]) - F(d[1]) * F(p[0]))
def lnorm(p, n): return L(n[0], n[1], -dot(n, p))
def l2(p, q): return ldir(p, vsub(q, p))
def inter(r, s):
    det = r.A * s.B - s.A * r.B
    if det == 0: return None
    return (F(r.B * s.C - s.B * r.C, det), F(s.A * r.C - r.A * s.C, det))
def proj(p, r):
    lam = -F(r.A * F(p[0]) + r.B * F(p[1]) + r.C, r.A ** 2 + r.B ** 2)
    return (F(p[0]) + lam * r.A, F(p[1]) + lam * r.B)
def dpr(p, r):
    """(|numerador|, A²+B²)"""
    return abs(r.A * F(p[0]) + r.B * F(p[1]) + r.C), r.A ** 2 + r.B ** 2
def angv(u, v): return math.degrees(math.acos(float(dot(u, v)) / math.sqrt(float(n2(u) * n2(v)))))
def angl(u, v): return math.degrees(math.acos(abs(float(dot(u, v))) / math.sqrt(float(n2(u) * n2(v)))))
def argd(v):
    a = math.degrees(math.atan2(float(v[1]), float(v[0])))
    return a + 360 if a < 0 else a
def prm(v):
    g = math.gcd(int(v[0]), int(v[1])) or 1
    return (int(v[0]) // g, int(v[1]) // g)
def eqs(p, d):
    """totes les equacions de la recta per p amb director d"""
    a, b, u1, u2 = F(p[0]), F(p[1]), F(d[0]), F(d[1]); r = ldir(p, d)
    o = [r'Vectorial: $(x,y)=%s+\lambda%s$' % (pt(p), pt(d)),
         r'Paramètriques: $\left\{\begin{array}{l}x=%s\\ y=%s\end{array}\right.$' % (poly([(a, ''), (u1, r'\lambda')]), poly([(b, ''), (u2, r'\lambda')])),
         r'Contínua: $\dfrac{%s}{%s}=\dfrac{%s}{%s}$' % (poly([(1, 'x'), (-a, '')]), tn(u1), poly([(1, 'y'), (-b, '')]), tn(u2))]
    if u1:
        m = u2 / u1; n = b - m * a
        o.append(r'Punt-pendent: $%s=%s(%s)$' % (poly([(1, 'y'), (-b, '')]), '' if m == 1 else '-' if m == -1 else tn(m), poly([(1, 'x'), (-a, '')])))
        o.append(r'Explícita: $y=%s$' % poly([(m, 'x'), (n, '')]))
    o.append(r'General: $\res{%s}$' % r.t())
    return o, r

# ---------- figures ----------
def fig(objs, box=(-6, 6, -6, 6), sc=0.38):
    """objs: ('l', recta, color) | ('p', punt, etiqueta, posició) | ('s', p, q, color) | ('poly', [punts], color)"""
    x0, x1, y0, y1 = box
    o = [r'\begin{tikzpicture}[scale=%g,baseline=(current bounding box.center)]' % sc,
         r'\draw[muted!25,very thin] (%d,%d) grid (%d,%d);' % (x0, y0, x1, y1),
         r'\draw[-latex,muted] (%g,0)--(%g,0) node[right,font=\scriptsize]{$x$}; \draw[-latex,muted] (0,%g)--(0,%g) node[above,font=\scriptsize]{$y$};' % (x0 - .3, x1 + .5, y0 - .3, y1 + .5),
         r'\begin{scope}\clip (%d,%d) rectangle (%d,%d);' % (x0, y0, x1, y1)]
    for ob in objs:
        if ob[0] == 'l':
            r, col = ob[1], ob[2]
            if r.B: o.append(r'\draw[%s,thick] (%g,%g)--(%g,%g);' % (col, x0, float(F(-r.C - r.A * x0, r.B)), x1, float(F(-r.C - r.A * x1, r.B))))
            else: o.append(r'\draw[%s,thick] (%g,%g)--(%g,%g);' % (col, float(F(-r.C, r.A)), y0, float(F(-r.C, r.A)), y1))
        elif ob[0] == 's': o.append(r'\draw[%s,thick] (%g,%g)--(%g,%g);' % (ob[3], float(ob[1][0]), float(ob[1][1]), float(ob[2][0]), float(ob[2][1])))
        elif ob[0] == 'poly': o.append(r'\filldraw[fill=%s!15,draw=%s,thick] ' % (ob[2], ob[2]) + '--'.join('(%g,%g)' % (float(p[0]), float(p[1])) for p in ob[1]) + '--cycle;')
    o.append(r'\end{scope}')
    for ob in objs:
        if ob[0] == 'p':
            o.append(r'\fill[navy] (%g,%g) circle (2.2pt) node[%s,font=\scriptsize]{$%s$};' % (float(ob[1][0]), float(ob[1][1]), ob[3] if len(ob) > 3 else 'above right', ob[2]))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def cen(*gs): return '\n\n\\begin{center}' + '\\qquad'.join(gs) + '\\end{center}\n'

CHK = []
def ck(x, y):
    CHK.append((x, y)); return x

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Vectors i operacions
A1, B1 = (3, -1), (-2, 4); v1 = vsub(B1, A1)
ck(v1, (-5, 5)); ck(n2(v1), 50)
args = [(3, 3), (-1, 1), (-4, -4), (0, -3), (5, 0), (2, -2)]
argv = [argd(v) for v in args]; ck([round(a) for a in argv], [45, 135, 225, 270, 0, 315])
u4, v4, w4 = (2, -3), (-1, 4), (5, 0)
r4 = [vsub(vadd(u4, v4), w4), vsub(vmul(3, u4), vmul(2, v4)), vadd(vsub(vmul(F(1, 2), w4), u4), v4), vadd(vmul(-2, vsub(u4, v4)), vmul(3, w4))]
ck(r4, [(-4, 1), (8, -17), (F(-1, 2), 7), (9, 14)])
S.append(("Vectors i operacions amb vectors", [
 (1, r"Donats els punts $A(3,-1)$ i $B(-2,4)$, calcula:" + tasks(2, [r"Les components de $\overrightarrow{AB}$ i de $\overrightarrow{BA}$.", r"El mòdul de $\overrightarrow{AB}$.",
      r"Un vector unitari amb la mateixa direcció i sentit que $\overrightarrow{AB}$.", r"Un vector de mòdul 10 amb la mateixa direcció i sentit contrari."]),
     tasks(2, [r"$\overrightarrow{AB}=\res{%s}$, $\overrightarrow{BA}=\res{%s}$" % (pt(v1), pt(vmul(-1, v1))), r"$|\overrightarrow{AB}|=\sqrt{25+25}=\res{%s}%s$" % (sq(50), ap(50 ** .5)),
               r"$\dfrac{(-5,5)}{5\sqrt2}=\res{\left(-\tfrac{\sqrt2}{2},\,\tfrac{\sqrt2}{2}\right)}$", r"$10\cdot\left(\tfrac{\sqrt2}{2},-\tfrac{\sqrt2}{2}\right)=\res{(5\sqrt2,\,-5\sqrt2)}$"])),
 (1, r"Calcula l'argument (l'angle amb el semieix positiu $OX$) de cada vector. Fixa't en el quadrant!" + tasks(3, [r"$\vec a=%s$" % pt(v) for v in args]),
     tasks(3, [r"$\res{%s^\circ}$" % round(a) for a in argv]) + r"La calculadora dona $\arctan\frac{v_2}{v_1}$ entre $-90^\circ$ i $90^\circ$: si $v_1<0$ cal sumar-hi $180^\circ$."),
 (1, r"Calcula les components d'un vector $\vec v$ si:" + tasks(3, [r"$|\vec v|=4$, argument $30^\circ$", r"$|\vec v|=10$, argument $135^\circ$", r"$|\vec v|=6$, argument $240^\circ$"])
     + recorda(r"$\vec v=\big(|\vec v|\cos\alpha,\ |\vec v|\sin\alpha\big)$."),
     tasks(3, [r"$\res{(2\sqrt3,\,2)}$", r"$\res{(-5\sqrt2,\,5\sqrt2)}$", r"$\res{(-3,\,-3\sqrt3)}$"])),
 (1, r"Siguen $\vec u=(2,-3)$, $\vec v=(-1,4)$ i $\vec w=(5,0)$. Calcula:" + tasks(2, [r"$\vec u+\vec v-\vec w$", r"$3\vec u-2\vec v$", r"$\tfrac12\vec w-\vec u+\vec v$", r"$-2(\vec u-\vec v)+3\vec w$"]),
     tasks(2, [r"$\res{%s}$" % pt(r) for r in r4])),
 (2, r"Calcula $x$ i $y$ perquè es complisca $(x,3)+2(1,y)=(5,-1)$. Després, troba $k$ perquè el vector $(k,4)$ tinga mòdul 5.",
     r"$x+2=5$ i $3+2y=-1$: $\res{x=3,\ y=-2}$. \quad $\sqrt{k^2+16}=5\Rightarrow k^2=9\Rightarrow\res{k=\pm3}$."),
 (2, r"Troba $m$ perquè els vectors $\vec u=(m,-2)$ i $\vec v=(6,3)$ siguen paral·lels. Per a aquest valor, quin nombre $k$ compleix $\vec u=k\vec v$?",
     r"$\dfrac m6=\dfrac{-2}{3}\Rightarrow\res{m=-4}$; aleshores $(-4,-2)=\res{-\tfrac23}\,(6,3)$."),
 (2, r"Comprova que $\vec u=(1,2)$ i $\vec v=(3,-1)$ formen una base i escriu $\vec w=(1,9)$ com a combinació lineal de $\vec u$ i $\vec v$.",
     r"$\frac13\neq\frac{2}{-1}$: no són paral·lels, formen base. $a(1,2)+b(3,-1)=(1,9)\Rightarrow\left\{\begin{array}{l}a+3b=1\\2a-b=9\end{array}\right.\Rightarrow a=4,\ b=-1$: $\res{\vec w=4\vec u-\vec v}$."),
]))
ck(vadd(vmul(4, (1, 2)), vmul(-1, (3, -1))), (1, 9))

# =====================================================================
# 2. Aplicacions
T8 = [(-2, 1), (4, 3), (2, -5)]
m8 = [mid(T8[0], T8[1]), mid(T8[1], T8[2]), mid(T8[2], T8[0])]; ck(m8, [(1, 2), (3, -1), (0, -2)])
B9 = vsub(vmul(2, (1, -2)), (4, 3)); ck(B9, (-2, -7))
A10, B10 = (-3, 4), (9, -2); d10 = [vadd(A10, vmul(F(i, 3), vsub(B10, A10))) for i in (1, 2)]; ck(d10, [(1, 2), (5, 0)])
A11, B11 = (1, -1), (11, 4); d11 = [vadd(A11, vmul(F(i, 5), vsub(B11, A11))) for i in range(1, 5)]
A14, B14, C14 = (-1, -2), (4, -1), (5, 3); D14 = vadd(A14, vsub(C14, B14)); ck(D14, (0, 2))
S.append(("Aplicacions geomètriques dels vectors", [
 (1, r"Calcula els punts mitjans dels costats del triangle de vèrtexs $A(-2,1)$, $B(4,3)$ i $C(2,-5)$.",
     r"$M_{AB}=\res{%s}$, \quad $M_{BC}=\res{%s}$, \quad $M_{CA}=\res{%s}$" % tuple(pt(p) for p in m8)),
 (1, r"El punt $M(1,-2)$ és el punt mig del segment $AB$. Si $A(4,3)$, quines són les coordenades de $B$?",
     r"$\frac{4+b_1}{2}=1$, $\frac{3+b_2}{2}=-2$: $\res{B%s}$ (o bé $B=2M-A$)." % pt(B9)),
 (1, r"Troba els punts que divideixen el segment d'extrems $A(-3,4)$ i $B(9,-2)$ en tres parts iguals.",
     r"$\overrightarrow{AB}=(12,-6)$, $\frac13\overrightarrow{AB}=(4,-2)$: $\res{M%s}$, $\res{N%s}$." % (pt(d10[0]), pt(d10[1]))),
 (2, r"Divideix el segment d'extrems $A(1,-1)$ i $B(11,4)$ en cinc parts iguals.",
     r"$\frac15\overrightarrow{AB}=(2,1)$: $\res{%s}$" % r'},\ \res{'.join(pt(p) for p in d11)),
 (1, r"Estudia si els punts estan alineats:" + tasks(2, [r"$A(1,3)$, $B(3,7)$, $C(-2,-3)$", r"$A(0,2)$, $B(3,4)$, $C(6,7)$"])
     + r"Calcula $k$ perquè $A(-1,2)$, $B(2,k)$ i $C(5,-4)$ estiguen alineats.",
     tasks(2, [r"$\overrightarrow{AB}=(2,4)$, $\overrightarrow{AC}=(-3,-6)$: $\frac{-3}{2}=\frac{-6}{4}$, \rest{sí} estan alineats.", r"$\overrightarrow{AB}=(3,2)$, $\overrightarrow{AC}=(6,5)$: $\frac63\neq\frac52$, \rest{no}."])
     + r"$\overrightarrow{AB}=(3,k-2)$, $\overrightarrow{AC}=(6,-6)$: $\frac{k-2}{3}=\frac{-6}{6}\Rightarrow k-2=-3\Rightarrow\res{k=-1}$."),
 (1, r"Calcula el simètric del punt $P(2,-3)$ respecte del punt $Q(-1,4)$, i el simètric de $R(5,1)$ respecte de l'origen.",
     r"$P'=2Q-P=\res{%s}$; \quad $R'=\res{(-5,-1)}$." % pt(vsub(vmul(2, (-1, 4)), (2, -3)))),
 (2, r"Tres vèrtexs consecutius d'un paral·lelogram $ABCD$ són $A(-1,-2)$, $B(4,-1)$ i $C(5,3)$. Troba el vèrtex $D$ i el centre del paral·lelogram.",
     r"$\overrightarrow{AD}=\overrightarrow{BC}=(1,4)\Rightarrow\res{D%s}$. El centre és el punt mig de les diagonals: $\res{%s}$." % (pt(D14), pt(mid(A14, C14)))
     + cen(fig([('poly', [A14, B14, C14, D14], 'teal'), ('p', A14, 'A', 'below left'), ('p', B14, 'B', 'below right'), ('p', C14, 'C', 'above right'), ('p', D14, 'D', 'above left'), ('p', mid(A14, C14), 'M', 'right')], (-3, 7, -4, 5)))),
]))
ck(mid(B14, D14), mid(A14, C14))

# =====================================================================
# 3. Producte escalar
u15, v15 = (3, -2), (4, 1); a15 = angv(u15, v15)
p16 = [((1, 2), (-2, 1)), ((1, 1), (-1, 0)), ((3, 4), (-4, -3)), ((2, -1), (1, 3))]
a16 = [angv(*p) for p in p16]
A20, B20, C20 = (1, 1), (5, 3), (3, 7); ck(dot(vsub(A20, B20), vsub(C20, B20)), 0)
S.append(("Producte escalar i angle de dos vectors", [
 (1, r"Siguen $\vec u=(3,-2)$ i $\vec v=(4,1)$. Calcula $\vec u\cdot\vec v$, $|\vec u|$, $|\vec v|$ i l'angle que formen.",
     r"$\vec u\cdot\vec v=12-2=\res{%s}$; $|\vec u|=\res{\sqrt{13}}$, $|\vec v|=\res{\sqrt{17}}$; $\cos\alpha=\dfrac{10}{\sqrt{221}}\Rightarrow\res{\alpha\approx %s}$" % (dot(u15, v15), dms(a15))),
 (1, r"Calcula l'angle que formen els vectors:" + tasks(2, [r"$%s$ i $%s$" % (pt(a), pt(b)) for a, b in p16]),
     tasks(2, [r"$\cos\alpha=\frac{%s}{%s\cdot%s}\Rightarrow\res{%s}$" % (dot(a, b), sq(n2(a)), sq(n2(b)), dms(x)) for (a, b), x in zip(p16, a16)])),
 (2, r"Si $|\vec u|=2$, $|\vec v|=5$ i l'angle que formen és de $120^\circ$, calcula:" + tasks(3, [r"$\vec u\cdot\vec v$", r"$(2\vec u+\vec v)\cdot(\vec u-\vec v)$", r"$|\vec u+\vec v|$"])
     + recorda(r"$\vec u\cdot\vec u=|\vec u|^2$ i el producte escalar és distributiu."),
     tasks(1, [r"$2\cdot5\cdot\cos120^\circ=\res{-5}$", r"$2|\vec u|^2-\vec u\cdot\vec v-|\vec v|^2=8+5-25=\res{-12}$", r"$\sqrt{4+25+2(-5)}=\res{\sqrt{19}}$"])),
 (2, r"Troba $m$ perquè $\vec u=(m,2)$ i $\vec v=(3,-6)$ siguen perpendiculars. Troba també $k$ perquè $(1,k)$ forme un angle de $60^\circ$ amb $(1,0)$.",
     r"$3m-12=0\Rightarrow\res{m=4}$. \quad $\cos60^\circ=\dfrac{1}{\sqrt{1+k^2}}=\dfrac12\Rightarrow1+k^2=4\Rightarrow\res{k=\pm\sqrt3}$."),
 (1, r"Troba els vectors unitaris perpendiculars a $\vec v=(6,-8)$.",
     r"Un perpendicular és $(8,6)$, de mòdul 10: $\res{\pm\left(\tfrac45,\tfrac35\right)}$."),
 (2, r"Comprova que el triangle de vèrtexs $A(1,1)$, $B(5,3)$ i $C(3,7)$ és rectangle i isòsceles. Quant mesuren els seus angles?",
     r"$\overrightarrow{BA}\cdot\overrightarrow{BC}=(-4,-2)\cdot(-2,4)=0$: \rest{angle recte en $B$}. $|\overrightarrow{BA}|=|\overrightarrow{BC}|=\sqrt{20}$: isòsceles. Angles: $\res{90^\circ,\ 45^\circ,\ 45^\circ}$."
     + cen(fig([('poly', [A20, B20, C20], 'teal'), ('p', A20, 'A', 'below left'), ('p', B20, 'B', 'right'), ('p', C20, 'C', 'above')], (-1, 7, -1, 8)))),
 (2, r"Calcula la projecció del vector $\vec u=(2,5)$ sobre la direcció de $\vec v=(3,-4)$. Què indica el signe?",
     r"$\dfrac{\vec u\cdot\vec v}{|\vec v|}=\dfrac{6-20}{5}=\res{-\tfrac{14}{5}}$: és negativa perquè l'angle és obtús."),
]))
ck(round(a15, 2), 47.73); ck(round(angv((1, 1), (-1, 0))), 135); ck(round(angv((1, 2), (-2, 1))), 90)

# =====================================================================
# 4. Equacions de la recta
e22, r22 = eqs((2, -1), (3, 4)); ck(r22, L(4, -3, -11))
e23, r23 = eqs((-1, 3), (1, -2)); ck(r23, L(2, 1, -1))
r24 = L(3, 2, -8); ck(r24.has((4, -2)), True); ck(r24.m(), F(-3, 2))
r25 = L(2, -5, 10)
r28 = lnorm((1, 5), (3, -1)); ck(r28, L(3, -1, 2))
S.append(("Equacions de la recta", [
 (1, r"Escriu totes les equacions (vectorial, paramètriques, contínua, punt-pendent, explícita i general) de la recta que passa per $P(2,-1)$ i té vector director $\vec u=(3,4)$.",
     tasks(1, e22)),
 (1, r"Escriu totes les equacions de la recta que passa per $A(-1,3)$ i $B(3,-5)$.",
     r"$\overrightarrow{AB}=(4,-8)\parallel(1,-2)$." + tasks(1, e23)),
 (1, r"Troba les equacions punt-pendent, explícita i general de la recta que passa per $P(4,-2)$ i té pendent $-\tfrac32$.",
     r"$y+2=-\tfrac32(x-4)$; \quad $y=-\tfrac32x+4$; \quad $\res{%s}$" % r24.t()),
 (1, r"Donada la recta $r:2x-5y+10=0$, troba: el pendent, els punts de tall amb els eixos, un vector director, un vector normal i unes equacions paramètriques.",
     r"$m=\res{\tfrac25}$; talls: $\res{(-5,0)}$ i $\res{(0,2)}$; $\vec u=\res{(5,2)}$, $\vec n=\res{(2,-5)}$; $\left\{\begin{array}{l}x=5\lambda\\ y=2+2\lambda\end{array}\right.$"),
 (1, r"Comprova si els punts $P(7,1)$ i $Q(4,0)$ pertanyen a la recta $r:\left\{\begin{array}{l}x=1+3\lambda\\ y=-3+2\lambda\end{array}\right.$ Calcula $k$ perquè $(k,5)$ siga de $r$.",
     r"$P$: $\lambda=2$ en les dues equacions: \rest{$P\in r$}. $Q$: $\lambda=1$ i $\lambda=\tfrac32$: \rest{$Q\notin r$}. $5=-3+2\lambda\Rightarrow\lambda=4\Rightarrow\res{k=13}$."),
 (1, r"Escriu l'equació de la recta:" + tasks(2, [r"Paral·lela a l'eix $OX$ per $(3,-2)$.", r"Paral·lela a l'eix $OY$ per $(3,-2)$.", r"Que passa per l'origen i per $(3,-2)$.", r"Bisectriu del 1r i 3r quadrants."]),
     tasks(2, [r"$\res{y=-2}$", r"$\res{x=3}$", r"$\res{%s}$" % l2((0, 0), (3, -2)).t(), r"$\res{y=x}$"])),
 (1, r"Troba l'equació general de la recta que passa per $P(1,5)$ i té vector normal $\vec n=(3,-1)$.",
     r"$3(x-1)-(y-5)=0\Rightarrow\res{%s}$" % r28.t()),
 (2, r"Troba l'equació de la recta que passa per $(2,3)$ i forma un angle de $135^\circ$ amb el semieix positiu $OX$, i la de la recta que talla l'eix $OY$ en $(0,-4)$ i forma un angle de $60^\circ$ amb $OX$.",
     r"$m=\tan135^\circ=-1$: $y-3=-(x-2)\Rightarrow\res{x+y-5=0}$. \quad $m=\tan60^\circ=\sqrt3$: $\res{y=\sqrt3\,x-4}$."),
]))
ck(r25.m(), F(2, 5)); ck(r25.has((-5, 0)) and r25.has((0, 2)), True)
ck(ldir((1, -3), (3, 2)).has((7, 1)), True); ck(ldir((1, -3), (3, 2)).has((4, 0)), False); ck(ldir((1, -3), (3, 2)).has((13, 5)), True)

# =====================================================================
# 5. Posicions relatives
p30 = [(L(2, -3, 1), L(4, 1, -5)), (L(1, -2, 3), L(-3, 6, -9)), (L(3, 1, -2), L(6, 2, 1))]
X30 = inter(*p30[0]); ck(X30, (1, 1))
r31, s31 = ldir((1, -1), (2, 1)), ldir((3, 0), (-4, 2)); X31 = inter(r31, s31); ck(X31, (3, 0))
r32 = ldir((2, 1), (1, -3)); ck(r32, L(3, 1, -7))
S.append(("Posicions relatives de dues rectes", [
 (1, r"Estudia la posició relativa de cada parell de rectes i, si es tallen, troba el punt de tall:" + tasks(1, [r"$r:2x-3y+1=0$, \quad $s:4x+y-5=0$", r"$r:x-2y+3=0$, \quad $s:-3x+6y-9=0$", r"$r:3x+y-2=0$, \quad $s:6x+2y+1=0$"]),
     tasks(1, [r"$\frac24\neq\frac{-3}{1}$: \rest{secants} en $\res{%s}$." % pt(X30), r"$\frac{1}{-3}=\frac{-2}{6}=\frac{3}{-9}$: \rest{coincidents}.", r"$\frac36=\frac12\neq\frac{-2}{1}$: \rest{paral·leles}."])),
 (1, r"Estudia la posició relativa de $r:\left\{\begin{array}{l}x=1+2\lambda\\ y=-1+\lambda\end{array}\right.$ i $s:\left\{\begin{array}{l}x=3-4\mu\\ y=2\mu\end{array}\right.$",
     r"Directors $(2,1)$ i $(-4,2)$, no proporcionals: \rest{secants}. $\left\{\begin{array}{l}1+2\lambda=3-4\mu\\ -1+\lambda=2\mu\end{array}\right.\Rightarrow\mu=0,\ \lambda=1$: punt de tall $\res{%s}$." % pt(X31)),
 (1, r"Estudia la posició relativa de $r:\left\{\begin{array}{l}x=2+\lambda\\ y=1-3\lambda\end{array}\right.$ i $s:3x+y-7=0$.",
     r"$\vec u_r\cdot\vec n_s=(1,-3)\cdot(3,1)=0$: paral·leles o coincidents. $(2,1)\in r$ i $6+1-7=0$: \rest{coincidents}."),
 (2, r"Troba $a$ perquè les rectes $ax+3y-2=0$ i $2x-y+5=0$ siguen: a) secants; b) paral·leles. Poden ser coincidents?",
     r"a) $\frac a2\neq\frac{3}{-1}$: $\res{a\neq-6}$. b) $\res{a=-6}$ (i $\frac{-2}{5}\neq-3$). \rest{No}: amb $a=-6$ els termes independents no són proporcionals."),
 (2, r"Calcula $m$ i $n$ perquè les rectes $mx+2y+n=0$ i $3x-y+4=0$ siguen coincidents.",
     r"$\frac m3=\frac{2}{-1}=\frac n4\Rightarrow\res{m=-6,\ n=-8}$."),
 (2, r"Les rectes $r:x-y+1=0$, $s:x+y-5=0$ i $t:y=-1$ determinen un triangle. Troba'n els vèrtexs.",
     r"$r\cap s=\res{%s}$, \quad $r\cap t=\res{%s}$, \quad $s\cap t=\res{%s}$" % (pt(inter(L(1, -1, 1), L(1, 1, -5))), pt(inter(L(1, -1, 1), L(0, 1, 1))), pt(inter(L(1, 1, -5), L(0, 1, 1))))
     + cen(fig([('l', L(1, -1, 1), 'navy'), ('l', L(1, 1, -5), 'accent'), ('l', L(0, 1, 1), 'teal'), ('p', (2, 3), '', 'above'), ('p', (-2, -1), '', 'below'), ('p', (6, -1), '', 'below')], (-4, 8, -3, 6)))),
]))
ck(inter(L(1, -1, 1), L(1, 1, -5)), (2, 3)); ck(inter(L(1, 1, -5), L(0, 1, 1)), (6, -1))

# =====================================================================
# 6. Paral·lelisme i perpendicularitat
r36 = L(3, -2, 5); P36 = (2, -1); par36, per36 = lnorm(P36, r36.n()), lnorm(P36, r36.d()); ck((par36, per36), (L(3, -2, -8), L(2, 3, -1)))
P37 = (0, -2); par37, per37 = ldir(P37, (-2, 1)), lnorm(P37, (-2, 1)); ck((par37, per37), (L(1, 2, 4), L(2, -1, -2)))
A40, B40, C40 = (1, 1), (7, 3), (3, 7); h40 = lnorm(C40, vsub(B40, A40)); H40 = inter(h40, l2(A40, B40)); ck(H40, (F(23, 5), F(11, 5)))
A41, B41 = (-3, 2), (5, -4); m41 = lnorm(mid(A41, B41), vsub(B41, A41)); ck(m41, L(4, -3, -7))
S.append(("Paral·lelisme i perpendicularitat", [
 (1, r"Troba les rectes paral·lela i perpendicular a $r:3x-2y+5=0$ que passen per $P(2,-1)$.",
     r"Paral·lela: $3x-2y+K=0$, $6+2+K=0$: $\res{%s}$. \quad Perpendicular: $2x+3y+K=0$, $4-3+K=0$: $\res{%s}$." % (par36.t(), per36.t())),
 (1, r"Troba les rectes paral·lela i perpendicular a $r:\left\{\begin{array}{l}x=1-2\lambda\\ y=3+\lambda\end{array}\right.$ que passen per $A(0,-2)$. Dona-les en forma general.",
     r"Paral·lela (director $(-2,1)$): $\res{%s}$. \quad Perpendicular (director $(1,2)$): $\res{%s}$." % (par37.t(), per37.t())),
 (1, r"Donada $r:y=-\tfrac13x+2$, troba les equacions explícites de les rectes paral·lela i perpendicular a $r$ que passen per $(-3,4)$.",
     r"Paral·lela ($m=-\tfrac13$): $\res{y=-\tfrac13x+3}$. \quad Perpendicular ($m'=3$): $\res{y=3x+13}$."),
 (2, r"Calcula $k$ perquè les rectes $kx-2y+1=0$ i $3x+(k+1)y-4=0$ siguen perpendiculars. Poden ser paral·leles?",
     r"$(k,-2)\cdot(3,k+1)=3k-2k-2=0\Rightarrow\res{k=2}$. Paral·leles: $\frac k3=\frac{-2}{k+1}\Rightarrow k^2+k+6=0$, sense solució real: \rest{mai no ho són}."),
 (2, r"En el triangle de vèrtexs $A(1,1)$, $B(7,3)$ i $C(3,7)$, troba l'equació de l'altura que surt de $C$ i el peu d'aquesta altura.",
     r"Altura: perpendicular a $\overrightarrow{AB}=(6,2)$ per $C$: $\res{%s}$. Recta $AB$: $%s$. Peu: $\res{H%s}$." % (h40.t(), l2(A40, B40).t(), pt(H40))),
 (2, r"Troba la mediatriu del segment d'extrems $A(-3,2)$ i $B(5,-4)$. Comprova-la amb la definició (punts que equidisten de $A$ i de $B$).",
     r"$M(1,-1)$, $\vec n=\overrightarrow{AB}=(8,-6)\parallel(4,-3)$: $\res{%s}$. \par Definició: $(x+3)^2+(y-2)^2=(x-5)^2+(y+4)^2\Rightarrow16x-12y-28=0$ \checkmark" % m41.t()),
]))
ck(l2(A40, B40), L(1, -3, 2))

# =====================================================================
# 7. Angles
a42 = angl((3, -1), (1, 2)); a43 = angl((2, -1), (-1, 3)); a44 = angl((1, 2), (1, -1))
ck(round(a43, 6), 45.0)
l46 = [lnorm((1, 2), (2, -1)), lnorm((1, 2), (1, 2))]
ck([round(angl(l.d(), (3, 1)), 6) for l in l46], [45.0, 45.0])
S.append(("Angle de dues rectes", [
 (1, r"Calcula l'angle que formen les rectes $r:3x-y+2=0$ i $s:x+2y-1=0$.",
     r"$\cos\alpha=\dfrac{|(3,-1)\cdot(1,2)|}{\sqrt{10}\sqrt5}=\dfrac{1}{\sqrt{50}}\Rightarrow\res{\alpha\approx %s}$" % dms(a42)),
 (1, r"Calcula l'angle de $r:\left\{\begin{array}{l}x=1+2\lambda\\ y=3-\lambda\end{array}\right.$ i $s:\left\{\begin{array}{l}x=2-\lambda\\ y=4+3\lambda\end{array}\right.$",
     r"$\cos\alpha=\dfrac{|(2,-1)\cdot(-1,3)|}{\sqrt5\sqrt{10}}=\dfrac{5}{\sqrt{50}}=\dfrac{\sqrt2}{2}\Rightarrow\res{\alpha=45^\circ}$"),
 (1, r"Calcula l'angle de les rectes $y=2x-1$ i $y=-x+4$.",
     r"Directors $(1,2)$ i $(1,-1)$: $\cos\alpha=\dfrac{1}{\sqrt{10}}\Rightarrow\res{\alpha\approx %s}$" % dms(a44)),
 (1, r"Quin angle forma cada recta amb l'eix $OX$? \quad a) $3x-3y+1=0$ \quad b) $x+2y=0$",
     r"a) $m=1$: $\res{45^\circ}$. \quad b) $m=-\tfrac12$: la recta forma $\res{%s}$ amb l'eix (l'angle d'inclinació és $%s$)." % (dms(math.degrees(math.atan(0.5))), dms(180 - math.degrees(math.atan(0.5))))),
 (3, r"Troba les rectes que passen per $P(1,2)$ i formen un angle de $45^\circ$ amb la recta $r:x-3y+1=0$.",
     r"$m_r=\tfrac13$. $\left|\dfrac{m-\frac13}{1+\frac m3}\right|=1\Rightarrow m=2$ o $m=-\tfrac12$: $\res{%s}$ i $\res{%s}$." % (l46[0].t(), l46[1].t())),
]))

# =====================================================================
# 8. Distàncies
A47, B47, C47 = (-1, 2), (3, 5), (6, 1); ck((n2(vsub(B47, A47)), n2(vsub(C47, B47)), n2(vsub(A47, C47))), (25, 25, 50))
P48 = (3, -2); l48 = [L(4, -3, 2), L(2, -1, 1), L(1, 0, 1), ldir((1, 2), (1, -1))]
d48 = [dpr(P48, l) for l in l48]; ck([F(a) ** 2 / b for a, b in d48], [16, F(81, 5), 16, 2])  # distàncies al quadrat
ck(dpr((-1, 2), L(6, 8, 15)), (25, 100))
S.append(("Distàncies", [
 (1, r"Calcula les longituds dels costats del triangle de vèrtexs $A(-1,2)$, $B(3,5)$ i $C(6,1)$ i classifica'l. Quin és el seu perímetre?",
     r"$|AB|=\res{5}$, $|BC|=\res{5}$, $|CA|=\res{5\sqrt2}$: isòsceles i, com que $25+25=50$, \rest{rectangle} en $B$. Perímetre: $\res{10+5\sqrt2}\approx17{,}07$."),
 (1, r"Calcula la distància del punt $P(3,-2)$ a cadascuna de les rectes:" + tasks(2, [r"$4x-3y+2=0$", r"$y=2x+1$", r"$x=-1$", r"$\left\{\begin{array}{l}x=1+\lambda\\ y=2-\lambda\end{array}\right.$"]),
     tasks(2, [r"$\dfrac{|12+6+2|}{5}=\res{4}$", r"$2x-y+1=0$: $\dfrac{9}{\sqrt5}=\res{\tfrac{9\sqrt5}{5}}\approx4{,}02$", r"$\res{4}$", r"$x+y-3=0$: $\dfrac{|-2|}{\sqrt2}=\res{\sqrt2}$"])),
 (1, r"Comprova que les rectes $r:3x+4y-5=0$ i $s:6x+8y+15=0$ són paral·leles i calcula la distància entre elles.",
     r"$\frac36=\frac48\neq\frac{-5}{15}$: paral·leles. $(-1,2)\in r$: $d=\dfrac{|-6+16+15|}{10}=\res{\tfrac52}$."),
 (2, r"Troba els punts de l'eix $OY$ que estan a distància 2 de la recta $3x-4y+1=0$.",
     r"$(0,y)$: $\dfrac{|-4y+1|}{5}=2\Rightarrow-4y+1=\pm10$: $\res{\left(0,-\tfrac94\right)}$ i $\res{\left(0,\tfrac{11}{4}\right)}$."),
 (2, r"Troba les rectes paral·leles a $5x-12y+3=0$ que estan a distància 2 d'ella.",
     r"$5x-12y+K=0$ amb $\dfrac{|K-3|}{13}=2$: $\res{5x-12y+29=0}$ i $\res{5x-12y-23=0}$."),
 (2, r"Una circumferència té el centre en $C(2,-1)$ i és tangent a la recta $3x+4y-12=0$. Quin és el seu radi?",
     r"El radi és la distància del centre a la recta: $\dfrac{|6-4-12|}{5}=\res{2}$."),
]))
ck([F(abs(F(-4 * y + 1)), 5) for y in (F(-9, 4), F(11, 4))], [2, 2]); ck([abs(K - 3) / F(13) for K in (29, -23)], [2, 2])

# =====================================================================
# 9. Problemes mètrics
r53 = L(2, -1, 5); M53 = proj((-3, 4), r53); P53 = vsub(vmul(2, M53), (-3, 4)); ck((M53, P53), ((-1, 3), (1, 2)))
b55 = [L(14, 112, -23), L(64, -8, -3)]
ck(b55[0], L(13 * 3 - 5 * 5, 13 * 4 + 5 * 12, -13 - 10)); ck(b55[1], L(13 * 3 + 25, 13 * 4 - 60, -13 + 10)); ck(dot(b55[0].n(), b55[1].n()), 0)
A57, B57, C57 = (-2, 0), (4, 2), (1, 6); med57 = l2(A57, mid(B57, C57)); alt57 = lnorm(A57, vsub(C57, B57))
G57 = (F(A57[0] + B57[0] + C57[0], 3), F(A57[1] + B57[1] + C57[1], 3)); ar57 = abs(F((B57[0] - A57[0]) * (C57[1] - A57[1]) - (B57[1] - A57[1]) * (C57[0] - A57[0]), 2))
ck((med57, alt57, G57, ar57), (L(8, -9, 16), L(3, -4, 6), (1, F(8, 3)), 15))
A59, B59, C59 = (-3, 0), (3, 0), (1, 4); H59 = inter(lnorm(C59, vsub(B59, A59)), lnorm(A59, vsub(C59, B59))); ck(H59, (1, 2))
ck(inter(lnorm(B59, vsub(C59, A59)), lnorm(C59, vsub(B59, A59))), (1, 2))
X61 = inter(lnorm(mid((1, 0), (5, 2)), (4, 2)), L(1, -1, 0)); ck(X61, (F(7, 3), F(7, 3)))
S.append(("Problemes mètrics", [
 (2, r"Troba la projecció del punt $P(-3,4)$ sobre la recta $r:2x-y+5=0$ i el simètric de $P$ respecte de $r$.",
     r"Perpendicular per $P$: $(x,y)=(-3,4)+\lambda(2,-1)$. En $r$: $5\lambda-5=0\Rightarrow\lambda=1$: $\res{M%s}$, \ $P'=2M-P=\res{%s}$." % (pt(M53), pt(P53))
     + cen(fig([('l', r53, 'navy'), ('s', (-3, 4), P53, 'accent'), ('p', (-3, 4), 'P', 'left'), ('p', M53, 'M', 'below right'), ('p', P53, "P'", 'right')], (-5, 4, -1, 6)))),
 (1, r"Calcula el simètric del punt $P(4,1)$ respecte de la recta $y=x$ i respecte de la recta $x=2$.",
     r"Respecte de $y=x$: $\res{(1,4)}$ (s'intercanvien les coordenades). Respecte de $x=2$: $\res{(0,1)}$."),
 (3, r"Troba les bisectrius dels angles que formen les rectes $r:3x+4y-1=0$ i $s:5x-12y+2=0$. Comprova que són perpendiculars.",
     r"$\dfrac{3x+4y-1}{5}=\pm\dfrac{5x-12y+2}{13}$: $\res{%s}$ i $\res{%s}$. \ $(14,112)\cdot(64,-8)=0$ \checkmark" % (b55[0].t(), b55[1].t())),
 (2, r"Calcula l'àrea del triangle determinat per les rectes $r:x-y+1=0$, $s:x+y-5=0$ i $t:y=-1$ (exercici 35).",
     r"Vèrtexs $(2,3)$, $(-2,-1)$, $(6,-1)$. Base sobre $t$: $8$; altura: $d\big((2,3),t\big)=4$. $S=\dfrac{8\cdot4}{2}=\res{16\ \text{u}^2}$."),
 (2, r"En el triangle $A(-2,0)$, $B(4,2)$, $C(1,6)$, calcula:" + tasks(2, [r"La mitjana que surt de $A$.", r"L'altura que surt de $A$.", r"El baricentre.", r"L'àrea."]),
     tasks(2, [r"$M_{BC}=\left(\tfrac52,4\right)$: $\res{%s}$" % med57.t(), r"$\perp\overrightarrow{BC}=(-3,4)$: $\res{%s}$" % alt57.t(), r"$\res{G%s}$" % pt(G57), r"$\tfrac12|6\cdot6-2\cdot3|=\res{15\ \text{u}^2}$"])),
 (2, r"Troba el circumcentre i el radi de la circumferència circumscrita al triangle $A(0,0)$, $B(6,0)$, $C(0,4)$.",
     r"Mediatrius de $AB$ i $AC$: $x=3$, $y=2$: $\res{O(3,2)}$; $R=d(O,A)=\res{\sqrt{13}}$. (És el punt mig de la hipotenusa $BC$: el triangle és rectangle.)"),
 (2, r"Troba l'ortocentre del triangle de vèrtexs $A(-3,0)$, $B(3,0)$ i $C(1,4)$.",
     r"Altura de $C$: $x=1$. Altura de $A$ ($\perp\overrightarrow{BC}=(-2,4)$): $x-2y+3=0$. Ortocentre: $\res{H%s}$." % pt(H59)),
 (2, r"Els punts $A(1,1)$ i $C(5,5)$ són vèrtexs oposats d'un quadrat. Troba els altres dos vèrtexs i l'àrea del quadrat.",
     r"Centre $(3,3)$; la mitja diagonal $(2,2)$ girada $90^\circ$ és $(2,-2)$: $\res{B(5,1)}$, $\res{D(1,5)}$. Àrea: $\dfrac{d^2}{2}=\dfrac{32}{2}=\res{16\ \text{u}^2}$."
     + cen(fig([('poly', [(1, 1), (5, 1), (5, 5), (1, 5)], 'teal'), ('s', (1, 1), (5, 5), 'navy'), ('p', (1, 1), 'A', 'below left'), ('p', (5, 1), 'B', 'below right'), ('p', (5, 5), 'C', 'above right'), ('p', (1, 5), 'D', 'above left')], (-1, 7, -1, 7)))),
 (3, r"Troba el punt de la recta $y=x$ que està a la mateixa distància de $A(1,0)$ que de $B(5,2)$.",
     r"És a la mediatriu de $AB$: $M(3,1)$, $\vec n=(4,2)\parallel(2,1)$: $2x+y-7=0$. Amb $y=x$: $\res{%s}$." % pt(X61)),
]))
ck(n2(vsub((3, 2), (0, 0))), 13)

for l, r in CHK:
    assert l == r, (l, r)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={geometria analítica, vectors, producte escalar, equacions de la recta, posicions relatives, rectes perpendiculars, angles, distàncies, mediatriu, bisectriu}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques I}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
# el primer exercici de cada secció no fa salt de pàgina: així no queda separat del títol
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

TIT = "Geometria analítica en el pla"
# amb icomma, «(3,5)» queda sense espai després de la coma: l'afegim a les coordenades de les fórmules (no a les figures)
def sp(t): return re.sub(r'\$[^$]*\$', lambda m: re.sub(r'(?<=[0-9a-zA-Z]),(?=-?[0-9a-zA-Z])', r',\\,', m.group(0)), t)
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 5: %s. 1r de Batxillerat MI}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 5: %s · 1r Batxillerat MI" % (t, TIT))
    assert 'Unitat 5' in p and 'unitat 5' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques I}{1r Batx}{''' + ('Solucions de la fitxa · Unitat 5' if sol else "Fitxa d'exercicis · Unitat 5") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Els resultats es donen de manera exacta (fraccions i arrels) i, quan cal, amb el valor aproximat; els angles, en graus, minuts i segons. Pots comprovar-los amb els ginys dels apunts interactius de la unitat i amb el laboratori del triangle."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos. Fes un dibuix aproximat en uns eixos de coordenades sempre que t'ajude: et permet detectar errors. Dona els resultats de manera exacta (fraccions i arrels) i, si cal, també aproximats. Les equacions de les rectes, en forma general $Ax+By+C=0$ amb coeficients enters, si no es diu el contrari.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            n += 1
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, sp(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't5-fitxa-solucions.tex' if sol else 't5-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis;', len(CHK), 'comprovacions')
