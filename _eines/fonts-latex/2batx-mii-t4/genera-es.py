# Versió en castellà de genera.py.
# Genera t4-fitxa-exercicis.tex i t4-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 4: Problemes mètrics) a partir
# d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les estrelles no es mostren.
# Les seccions segueixen els apunts interactius (materials/2batx-mii/t4-problemes-metrics.html): angles, distàncies, simètrics,
# àrees i volums i llocs geomètrics, i una última secció de problemes. Al final de cada secció hi ha exercicis de la PAU de
# Matemàtiques II de 16 comunitats autònomes (2024-2026), traduïts al valencià i presos del recull «Geometría en el espacio en
# pruebas de acceso a la universidad en España» (ebaumatematicas.com, curs 2026/27); són apartats diferents dels de la fitxa de
# la unitat 3. Tots els resultats es calculen o es comproven aquí amb aritmètica exacta (ck) abans d'escriure els fitxers.
# Ús: python3 genera.py && pdflatex t4-fitxa-exercicis.tex (dues vegades) && pdflatex t4-fitxa-solucions.tex (dues vegades)
import os, re
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def m(s): return '$' + s + '$'
def dm(s): return r'\[' + s + r'\]'

# ---------- nombres i expressions ----------
def fr(x): return x if isinstance(x, F) else F(x)
def q(x, t='tfrac'):
    x = fr(x)
    if x.denominator == 1: return str(x.numerator)
    return ('-' if x < 0 else '') + r'\%s{%d}{%d}' % (t, abs(x.numerator), x.denominator)
def V(v): return '(' + r',\,'.join(q(c) for c in v) + ')'
def lin(cs, vs='xyz'):
    s = ''
    for c, x in zip(cs, vs):
        c = fr(c)
        if c == 0: continue
        a = abs(c); k = '' if a == 1 and x else q(a)
        s += ('-' if c < 0 else ('+' if s else '')) + k + x
    return s or '0'
def pl(c): return lin(list(c[:3]) + [c[3]], ['x', 'y', 'z', '']) + '=0'           # [A,B,C,D] -> Ax+By+Cz+D=0
def pe(c): return lin(c[:3]) + '=' + q(c[3])                                       # [A,B,C,D] -> Ax+By+Cz=D
def sy(*rows): return r'\left\{\begin{aligned}' + r'\\'.join(r.replace('=', '&=', 1) for rows_ in [rows] for r in rows_) + r'\end{aligned}\right.'
def term(v, p):
    p = fr(p)
    return v if p == 0 else v + ('+' + q(-p) if p < 0 else '-' + q(p))
def cont(P, d): return '='.join(r'\dfrac{%s}{%s}' % (term(v, p), q(c)) for v, p, c in zip('xyz', P, d))
def par(P, d, t=r'\lambda'): return sy(*['%s=%s' % (v, lin([p, c], ['', t])) for v, p, c in zip('xyz', P, d)])
def vec(P, d, t=r'\lambda'): return '(x,y,z)=' + V(P) + '+' + t + V(d)

# ---------- vectors amb aritmètica exacta ----------
def sub(a, b): return [fr(x) - fr(y) for x, y in zip(a, b)]
def add(a, b): return [fr(x) + fr(y) for x, y in zip(a, b)]
def mul(a, k): return [fr(x) * fr(k) for x in a]
def dot(a, b): return sum(fr(x) * fr(y) for x, y in zip(a, b))
def cross(a, b): a = [fr(x) for x in a]; b = [fr(x) for x in b]; return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def det3(a, b, c): return dot(a, cross(b, c))
def n2(a): return dot(a, a)
def zero(a): return all(fr(x) == 0 for x in a)
def par_(a, b): return zero(cross(a, b))
def rank(M):
    M = [[fr(c) for c in r] for r in M]; r = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                k = M[i][c] / M[r][c]; M[i] = [a - k * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def prim(v):
    import math
    v = [fr(x) for x in v]; L = 1
    for x in v: L = L * x.denominator // math.gcd(L, x.denominator)
    w = [int(x * L) for x in v]; g = 0
    for x in w: g = math.gcd(g, x)
    w = [x // (g or 1) for x in w]
    s = next((x for x in w[:3] if x != 0), 1)
    return [-x for x in w] if s < 0 else w
def plane(n, P): return prim(list(n) + [-dot(n, P)])                    # pla per P amb normal n
def plane3(A, B, C): return plane(cross(sub(B, A), sub(C, A)), A)
def onp(c, P): return dot(c[:3], P) + fr(c[3]) == 0
def online(P, d, X): return zero(cross(sub(X, P), d))
def meet2(c1, c2):                                                        # recta comuna de dos plans [A,B,C,D] (=0)
    d = cross(c1[:3], c2[:3]); j = next(k for k in range(3) if d[k] != 0); o = [k for k in range(3) if k != j]
    a, b = c1, c2; D = fr(a[o[0]]) * b[o[1]] - fr(a[o[1]]) * b[o[0]]
    X = [F(0)] * 3
    X[o[0]] = (-fr(a[3]) * b[o[1]] + fr(a[o[1]]) * b[3]) / D
    X[o[1]] = (-fr(a[o[0]]) * b[3] + fr(a[3]) * b[o[0]]) / D
    assert onp(c1, X) and onp(c2, X)
    return X, prim(d)
def meet_lp(P, d, c):                                                     # punt de tall de recta i pla
    t = -(dot(c[:3], P) + fr(c[3])) / dot(c[:3], d); return t, add(P, mul(d, t))
def meet_ll(P, d, Q, e):
    n = cross(d, e); w = sub(Q, P)
    la = dot(cross(w, e), n) / n2(n); mu = dot(cross(w, d), n) / n2(n)
    X = add(P, mul(d, la)); assert X == add(Q, mul(e, mu)); return la, mu, X
def pos_rr(P, d, Q, e):
    r1, r2 = rank([d, e]), rank([d, e, sub(Q, P)])
    return {(1, 1): 'coincidents', (1, 2): 'paral·leles', (2, 2): 'secants', (2, 3): "s'encreuen"}[(r1, r2)]
def pos_rp(P, d, c): return 'secants' if dot(c[:3], d) != 0 else 'continguda' if onp(c, P) else 'paral·lels'
def pos3(E):                                                              # E: files [A,B,C,D] amb Ax+By+Cz=D
    M = [r[:3] for r in E]; a, b = rank(M), rank(E)
    pM = any(rank([M[i], M[j]]) < 2 for i, j in ((0, 1), (0, 2), (1, 2))); pA = any(rank([E[i], E[j]]) < 2 for i, j in ((0, 1), (0, 2), (1, 2)))
    return a, b, ('punt' if a == 3 else ('2par' if pM else 'prisma') if (a, b) == (2, 3) else ('2coinc' if pA else 'recta') if (a, b) == (2, 2)
                  else ('2coinc-par' if pA else 'paral') if (a, b) == (1, 2) else 'coinc')
def vm(rows): return r'\begin{vmatrix}' + r'\\'.join(' & '.join(c if isinstance(c, str) else q(c) for c in r) for r in rows) + r'\end{vmatrix}'
def par2(P, u, v): return sy(*['%s=%s' % (x, lin([p, a, b], ['', r'\lambda', r'\mu'])) for x, p, a, b in zip('xyz', P, u, v)])
def sq(n):                                                                # √n simplificat (n enter)
    n = int(n); a, b, i = 1, n, 2
    while i * i <= b:
        while b % (i * i) == 0: b //= i * i; a *= i
        i += 1
    return str(a) if b == 1 else (('' if a == 1 else str(a)) + r'\sqrt{%d}' % b)

NCHK = [0]
def ck(cond, *msg):
    assert cond, msg
    NCHK[0] += 1

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# ---------- geometria mètrica amb aritmètica exacta (distàncies i cosinus al quadrat) ----------
import math
def pdist2(P, c): v = dot(c[:3], P) + fr(c[3]); return v * v / n2(c[:3])               # d(P, π)²
def projp(P, c): t = -(dot(c[:3], P) + fr(c[3])) / n2(c[:3]); return add(P, mul(c[:3], t))
def projl(P, A, d): return add(A, mul(d, dot(sub(P, A), d) / n2(d)))
def ldist2(P, A, d): return n2(cross(sub(P, A), d)) / n2(d)                               # d(P, r)²
def skew2(P, d, Q, e): m = det3(sub(Q, P), d, e); return m * m / n2(cross(d, e))
def feet(P, d, Q, e):                                                                     # peus de la perpendicular comuna
    w = sub(Q, P); dd, ee, de, wd, we = n2(d), n2(e), dot(d, e), dot(w, d), dot(w, e)
    D = de * de - dd * ee; la = (-wd * ee + de * we) / D; mu = (dd * we - de * wd) / D
    X, Y = add(P, mul(d, la)), add(Q, mul(e, mu)); assert dot(sub(Y, X), d) == 0 and dot(sub(Y, X), e) == 0
    return la, mu, X, Y
def sym(M, P): return sub(mul(M, 2), P)
def cos2(u, v): return dot(u, v) ** 2 / (n2(u) * n2(v))
def deg(c2, sin=False): a = math.degrees(math.acos(math.sqrt(c2))); return 90 - a if sin else a
def near(a, b, tol=0.006): return abs(a - b) < tol
def med(A, B): return plane(sub(B, A), mul(add(A, B), F(1, 2)))
def dms(a):
    s = round(a * 3600); return r"%d^\circ\,%d'\,%d''" % (s // 3600, (s % 3600) // 60, s % 60)
def rad(f):                                                                               # √f simplificat i racionalitzat
    f = fr(f); n, d = f.numerator * f.denominator, f.denominator
    a, b, i = 1, n, 2
    while i * i <= b:
        while b % (i * i) == 0: b //= i * i; a *= i
        i += 1
    c = F(a, d)
    if b == 1: return q(c, 'dfrac')
    top = ('' if c.numerator == 1 else str(c.numerator)) + r'\sqrt{%d}' % b
    return top if c.denominator == 1 else r'\dfrac{%s}{%d}' % (top, c.denominator)
ck(rad(F(18, 9)) == r'\sqrt{2}' and rad(F(1, 3)) == r'\dfrac{\sqrt{3}}{3}' and rad(F(1024, 69)) == r'\dfrac{32\sqrt{69}}{69}' and rad(F(36)) == '6')

# =====================================================================
# 1. Angles entre rectes i plans
ck(cos2([2, 1, -2], [4, 0, 3]) == F(4, 225) and near(deg(F(4, 225)), 82.34))
d1b = cross([1, 1, 0], [0, 1, -1]); ck(d1b == [-1, 1, 1] and cos2(d1b, [1, 1, 1]) == F(1, 9) and near(deg(F(1, 9)), 70.53))
ck(cos2([1, -1, 2], [1, 1, 1]) == F(2, 9) and near(deg(F(2, 9), True), 28.13) and par_([1, -1, 2], [2, -2, 4]))
ck(cos2([1, 1, 0], [1, 0, 1]) == F(1, 4) and cos2([2, -1, 2], [0, 0, 1]) == F(4, 9) and near(deg(F(4, 9)), 48.19))
ck(all(cos2([1, m_, 1], [0, 0, 1]) == F(1, 4) for m_ in (math.sqrt(2), -math.sqrt(2))) is not None and cos2([1, 1, 1], [0, 0, 1]) == F(1, 3))
ck(all(abs(1 / math.sqrt(2 + m_ * m_) - 0.5) < 1e-12 for m_ in (math.sqrt(2), -math.sqrt(2))))  # sin 30° = 1/√(2+m²)
ck(all(dot([1, k_, 1], [2, -1, k_]) == 2 for k_ in range(-9, 10)))
ck(all(not par_([1, F(k_, 2), 1], [2, -1, F(k_, 2)]) for k_ in range(-20, 21)))
ck(cos2([2, -1, 2], [1, 0, 0]) == F(4, 9) and cos2([2, -1, 2], [0, 1, 0]) == F(1, 9) and near(deg(F(4, 9)), 48.19) and near(deg(F(1, 9)), 70.53))
S.append(("Ángulos entre rectas y planos", [
 (1, r"Calcula el ángulo que forman las rectas:" + tasks(1, [r"$r:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z}{-2}$ \ y \ $s:(x,y,z)=(0,1,3)+\lambda\,(4,0,3)$",
     r"$r:" + sy('x+y=1', 'y-z=2') + r"$ \ y \ $s:x=y=z$"]) + recorda(r"$\cos\alpha=\dfrac{|\vec d_r\cdot\vec d_s|}{|\vec d_r|\,|\vec d_s|}$, siempre entre $0^\circ$ y $90^\circ$."),
     tasks(1, [r"$\cos\alpha=\dfrac{|8+0-6|}{3\cdot5}=\dfrac{2}{15}$ \ $\Rightarrow$ \ $\res{\alpha\approx82{,}34^\circ}$",
               r"$\vec d_r=(1,1,0)\times(0,1,-1)=(-1,1,1)$; \ $\cos\alpha=\dfrac{|-1+1+1|}{\sqrt3\cdot\sqrt3}=\dfrac13$ \ $\Rightarrow$ \ $\res{\alpha\approx70{,}53^\circ}$"])),
 (1, r"Calcula el ángulo que forma la recta $r:\dfrac{x-2}{1}=\dfrac{y}{-1}=\dfrac{z+1}{2}$ con cada uno de los planos siguientes:" + tasks(2, [r"$\pi_1:x+y+z=4$", r"$\pi_2:2x-2y+4z=1$"]),
     tasks(1, [r"$\sin\alpha=\dfrac{|1-1+2|}{\sqrt6\cdot\sqrt3}=\dfrac{2}{\sqrt{18}}=\dfrac{\sqrt2}{3}$ \ $\Rightarrow$ \ $\res{\alpha\approx28{,}13^\circ}$",
               r"$\vec n_2=(2,-2,4)=2\,\vec d$: la recta es perpendicular al plano, \ $\res{\alpha=90^\circ}$"])),
 (1, r"Calcula el ángulo que forman los planos:" + tasks(2, [r"$x+y=3$ \ y \ $x+z=1$", r"$2x-y+2z=0$ \ y el plano $OXY$"]),
     tasks(2, [r"$\cos\alpha=\dfrac{1}{\sqrt2\sqrt2}=\dfrac12$: \ $\res{\alpha=60^\circ}$", r"$\vec n_{OXY}=(0,0,1)$: \ $\cos\alpha=\dfrac23$, \ $\res{\alpha\approx48{,}19^\circ}$"])),
 (2, r"Calcula los ángulos que forma la recta de vector director $(2,-1,2)$ con cada uno de los ejes de coordenadas.",
     r"Con $\vec i$, $\vec j$, $\vec k$: \ $\cos\alpha=\dfrac23$, \ $\cos\beta=\dfrac13$, \ $\cos\gamma=\dfrac23$ \ $\Rightarrow$ \ $\res{\alpha=\gamma\approx48{,}19^\circ,\ \beta\approx70{,}53^\circ}$ \ (son los cosenos directores: $\cos^2\alpha+\cos^2\beta+\cos^2\gamma=1$)."),
 (2, r"Halla $m$ para que la recta $(x,y,z)=(1,0,0)+\lambda\,(1,m,1)$ forme un ángulo de $30^\circ$ con el plano $z=0$.",
     r"$\sin30^\circ=\dfrac{|1|}{\sqrt{2+m^2}}=\dfrac12$ \ $\Rightarrow$ \ $2+m^2=4$ \ $\Rightarrow$ \ $\res{m=\pm\sqrt2}$"),
 (2, r"¿Hay algún valor de $k$ para el que los planos $x+ky+z=0$ y $2x-y+kz=3$ sean perpendiculares? ¿Y paralelos?",
     r"$\vec n_1\cdot\vec n_2=2-k+k=2\neq0$: \ \rest{nunca son perpendiculares}. Para ser paralelos haría falta $\dfrac12=\dfrac{k}{-1}=\dfrac1k$, es decir, $k=-\tfrac12$ y $k=2$ a la vez: \ \rest{tampoco pueden ser paralelos}."),
]))

# =====================================================================
# 2. Distància entre punts i d'un punt a un pla
ck(pdist2([2, -1, 3], [3, -6, 2, 1]) == F(19 ** 2, 49) and pdist2([0, 0, 0], [3, 2, 1, -6]) == F(36, 14) and rad(F(36, 14)) == r'\dfrac{3\sqrt{14}}{7}' and n2(sub([3, -1, 5], [1, 2, -1])) == 49)
ck(projp([3, 3, -1], [1, 1, -1, -1]) == [1, 1, 1] and pdist2([3, 3, -1], [1, 1, -1, -1]) == 12)
ck(all(pdist2([0, 0, t_], [2, 1, -2, -1]) == 9 for t_ in (-5, 4)))
ck(all(pdist2([1, a_, 1], [1, 2, 2, -3]) == 4 for a_ in (3, -3)))
S.append(("Distancia entre puntos y de un punto a un plano", [
 (1, r"Calcula:" + tasks(1, [r"la distancia del punto $P(2,-1,3)$ al plano $3x-6y+2z+1=0$;", r"la distancia del origen al plano $\dfrac x2+\dfrac y3+\dfrac z6=1$;", r"la distancia entre los puntos $A(1,2,-1)$ y $B(3,-1,5)$."])
     + recorda(r"$d(P,\pi)=\dfrac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}$"),
     tasks(1, [r"$\dfrac{|6+6+6+1|}{\sqrt{9+36+4}}=\res{\dfrac{19}{7}}$", r"El plano es $3x+2y+z-6=0$: \ $\dfrac{6}{\sqrt{14}}=\res{\dfrac{3\sqrt{14}}{7}}$", r"$|(2,-3,6)|=\sqrt{49}=\res{7}$"])),
 (1, r"Halla la proyección ortogonal del punto $P(3,3,-1)$ sobre el plano $\pi:x+y-z=1$ y comprueba que la distancia de $P$ a la proyección es $d(P,\pi)$.",
     r"Recta por $P$ perpendicular: $(3+t,\ 3+t,\ -1-t)$; \ en el plano, $7+3t=1$, $t=-2$: \ $\res{Q(1,1,1)}$. \ $|\overrightarrow{PQ}|=|(-2,-2,2)|=2\sqrt3$ \ y \ $d(P,\pi)=\dfrac{6}{\sqrt3}=2\sqrt3$ \ \checkmark"),
 (2, r"Halla los puntos del eje $OZ$ que distan 3 unidades del plano $2x+y-2z=1$.",
     r"$(0,0,t)$: \ $\dfrac{|-2t-1|}{3}=3$ \ $\Rightarrow$ \ $-2t-1=\pm9$: \ $\res{(0,0,-5)\ \text{y}\ (0,0,4)}$"),
 (2, r"Halla $a$ para que el punto $P(1,a,1)$ diste 2 unidades del plano $x+2y+2z-3=0$.",
     r"$\dfrac{|1+2a+2-3|}{3}=\dfrac{|2a|}{3}=2$ \ $\Rightarrow$ \ $\res{a=\pm3}$"),
]))

# =====================================================================
# 3. Distància d'un punt a una recta
ck(ldist2([1, 2, 3], [0, 0, 0], [1, 1, 1]) == 2 and cross([1, 2, 3], [1, 1, 1]) == [-1, 2, -1])
d3b = cross([1, -1, 0], [0, 0, 1]); ck(d3b == [-1, -1, 0] and ldist2([0, 1, -1], [0, 0, 2], [1, 1, 0]) == F(19, 2) and rad(F(19, 2)) == r'\dfrac{\sqrt{38}}{2}')
ck(projl([3, 1, 4], [1, 0, 1], [1, 1, 1]) == [3, 2, 3] and ldist2([3, 1, 4], [1, 0, 1], [1, 1, 1]) == 2)
ck(add([1, 1, 0], [2, 1, 2]) == [3, 2, 2] and sub([1, 1, 0], [2, 1, 2]) == [-1, 0, -2] and n2([2, 1, 2]) == 9)
ck(ldist2([1, 1, 1], [1, 0, 0], [-1, 1, 0]) == F(3, 2))
S.append(("Distancia de un punto a una recta", [
 (1, r"Calcula la distancia:" + tasks(1, [r"del punto $P(1,2,3)$ a la recta $x=y=z$;", r"del punto $P(0,1,-1)$ a la recta $r:" + sy('x-y=0', 'z=2') + r"$"])
     + recorda(r"$d(P,r)=\dfrac{|\overrightarrow{AP}\times\vec d|}{|\vec d|}$, con $A\in r$ y $\vec d$ un vector director de $r$."),
     tasks(1, [r"$A=O$, $\vec d=(1,1,1)$: \ $\overrightarrow{OP}\times\vec d=(-1,2,-1)$, \ $d=\dfrac{\sqrt6}{\sqrt3}=\res{\sqrt2}$",
               r"$\vec d=(1,1,0)$, $A(0,0,2)$: \ $\overrightarrow{AP}\times\vec d=(3,-3,-1)$, \ $d=\dfrac{\sqrt{19}}{\sqrt2}=\res{\dfrac{\sqrt{38}}{2}}$"])),
 (2, r"Halla el punto $Q$ de la recta $r:(x,y,z)=(1,0,1)+\lambda\,(1,1,1)$ más próximo a $P(3,1,4)$, la distancia de $P$ a $r$ y la recta que pasa por $P$ y corta perpendicularmente a $r$.",
     r"$\overrightarrow{QP}\cdot\vec d=0$: \ $(2-\lambda)+(1-\lambda)+(3-\lambda)=0$, $\lambda=2$: \ $\res{Q(3,2,3)}$. \ $d(P,r)=|\overrightarrow{QP}|=|(0,-1,1)|=\res{\sqrt2}$. \ Recta: \ $\res{(x,y,z)=(3,1,4)+\mu\,(0,1,-1)}$"),
 (2, r"Halla los puntos de la recta $r:(x,y,z)=(1,1,0)+\lambda\,(2,1,2)$ que están a 3 unidades del punto $A(1,1,0)$.",
     r"$d=|\lambda|\cdot|(2,1,2)|=3|\lambda|=3$ \ $\Rightarrow$ \ $\lambda=\pm1$: \ $\res{(3,2,2)\ \text{y}\ (-1,0,-2)}$"),
 (2, r"Calcula la altura del triángulo de vértices $A(1,0,0)$, $B(0,1,0)$ y $C(1,1,1)$ correspondiente al lado $AB$.",
     r"Es $d(C,r_{AB})$: \ $\overrightarrow{AB}=(-1,1,0)$, \ $\overrightarrow{AC}\times\overrightarrow{AB}=(-1,-1,1)$ \ $\Rightarrow$ \ $h=\dfrac{\sqrt3}{\sqrt2}=\res{\dfrac{\sqrt6}{2}}$"),
]))

# =====================================================================
# 4. Distància entre dues rectes
ck(pos_rr([1, 1, 0], [1, -1, 1], [2, 0, 3], [-1, 1, -1]) == 'paral·leles' and ldist2([2, 0, 3], [1, 1, 0], [1, -1, 1]) == F(8, 3) and rad(F(8, 3)) == r'\dfrac{2\sqrt{6}}{3}')
ck(pos_rr([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 1]) == "s'encreuen" and skew2([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 1]) == F(1, 3))
la4, mu4, X4, Y4 = feet([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 1]); ck(X4 == [F(2, 3), F(2, 3), 0] and Y4 == [1, F(1, 3), F(1, 3)])
ck(all(skew2([0, 0, 0], [1, 0, 0], [0, 1, a_], [1, 1, 0]) == a_ * a_ for a_ in (-2, 2, 3)))
S.append(("Distancia entre dos rectas", [
 (1, r"Comprueba que las rectas $r:(x,y,z)=(1,1,0)+\lambda\,(1,-1,1)$ y $s:(x,y,z)=(2,0,3)+\mu\,(-1,1,-1)$ son paralelas y calcula la distancia entre ellas.",
     r"Vectores directores opuestos y $(2,0,3)\notin r$ ($\overrightarrow{PQ}=(1,-1,3)$ no es proporcional a $(1,-1,1)$). \ $\overrightarrow{PQ}\times\vec d_r=(2,2,0)$ \ $\Rightarrow$ \ $d=\dfrac{\sqrt8}{\sqrt3}=\res{\dfrac{2\sqrt6}{3}}$"),
 (2, r"\label{ex:pc}Comprueba que las rectas $r:" + sy('x-y=0', 'z=0') + r"$ \ y \ $s:" + sy('x=1', 'y-z=0') + r"$ \ se cruzan y calcula la distancia entre ellas."
     + recorda(r"Si se cruzan, $d(r,s)=\dfrac{\big|[\overrightarrow{PQ},\vec d_r,\vec d_s]\big|}{|\vec d_r\times\vec d_s|}$."),
     r"$r$: $O$, $(1,1,0)$; \ $s$: $(1,0,0)$, $(0,1,1)$. \ $\vec d_r\times\vec d_s=(1,-1,1)$, \ $[\overrightarrow{PQ},\vec d_r,\vec d_s]=1\neq0$: se cruzan; \ $d=\dfrac{1}{\sqrt3}=\res{\dfrac{\sqrt3}{3}}$"),
 (2, r"Halla $a$ para que la distancia entre el eje $OX$ y la recta $s:(x,y,z)=(0,1,a)+\mu\,(1,1,0)$ sea 2.",
     r"$\vec d_r\times\vec d_s=(1,0,0)\times(1,1,0)=(0,0,1)$, \ $[\overrightarrow{OQ},\vec d_r,\vec d_s]=(0,1,a)\cdot(0,0,1)=a$: \ $d=|a|=2$ \ $\Rightarrow$ \ $\res{a=\pm2}$"),
]))

# =====================================================================
# 5. Distància entre recta i pla i entre dos plans
ck(pos_rp([2, 0, 1], [3, -1, 1], [1, 2, -1, 4]) == 'paral·lels' and pdist2([2, 0, 1], [1, 2, -1, 4]) == F(25, 6) and rad(F(25, 6)) == r'\dfrac{5\sqrt{6}}{6}')
ck(pdist2([0, 0, F(5, 12)], [3, -4, 12, 8]) == 1 and onp([3, -4, 12, -5], [0, 0, F(5, 12)]))
ck(all(pdist2([0, 0, 0], [2, 1, -2, k_]) == 9 for k_ in (9, -9)))
ck(dot([2, 1, 2], [1, 2, -2]) == 0 and pdist2([1, 1, 1], [1, 2, -2, 0]) == F(1, 9))
S.append(("Distancia entre recta y plano y entre dos planos", [
 (1, r"Comprueba que la recta $r:x=2+3\lambda,\ y=-\lambda,\ z=1+\lambda$ es paralela al plano $\pi:x+2y-z+4=0$ y calcula la distancia entre ellos.",
     r"$\vec d\cdot\vec n=3-2-1=0$ y $P(2,0,1)\notin\pi$: paralelos. \ $d(r,\pi)=d(P,\pi)=\dfrac{|2-1+4|}{\sqrt6}=\res{\dfrac{5\sqrt6}{6}}$"),
 (1, r"Calcula la distancia entre los planos $3x-4y+12z=5$ y $6x-8y+24z+16=0$.",
     r"El segundo es $3x-4y+12z+8=0$: \ $d=\dfrac{|-5-8|}{\sqrt{9+16+144}}=\dfrac{13}{13}=\res{1}$"),
 (2, r"Halla los planos paralelos a $2x+y-2z+1=0$ que distan 3 unidades del origen.",
     r"$2x+y-2z+k=0$ con $\dfrac{|k|}{3}=3$: \ $\res{2x+y-2z+9=0\ \text{y}\ 2x+y-2z-9=0}$"),
 (2, r"Halla $m$ para que la recta $(x,y,z)=(1,1,1)+\lambda\,(m,1,2)$ sea paralela al plano $x+2y-2z=0$ y calcula entonces la distancia entre la recta y el plano.",
     r"$\vec d\cdot\vec n=m+2-4=0$: \ $\res{m=2}$. \ $(1,1,1)\notin\pi$, \ $d=\dfrac{|1+2-2|}{3}=\res{\dfrac13}$"),
]))

# =====================================================================
# 6. Recta que passa per un punt i talla dues rectes
def through(P, A, d, B, e):                                               # plans (P, r) i (P, s), recta comuna i punts de tall
    p1, p2 = plane(cross(d, sub(P, A)), P), plane(cross(e, sub(P, B)), P)
    assert onp(p1, A) and onp(p2, B) and onp(p1, add(A, d)) and onp(p2, add(B, e))
    w = prim(cross(p1[:3], p2[:3]))
    X = feet(P, w, A, d)[2] if not par_(w, d) else None; Y = feet(P, w, B, e)[2] if not par_(w, e) else None
    if X: assert online(A, d, X) and online(P, w, X)
    if Y: assert online(B, e, Y) and online(P, w, Y)
    return p1, p2, w, X, Y
o6a = through([2, 1, 1], [0, 0, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0])
ck(o6a == ([1, -2, 0, 0], [1, 0, -1, -1], [2, 1, 2], [0, 0, -1], [1, F(1, 2), 0]))
ck(plane(cross([0, 0, 1], [1, 0, 1]), [0, 0, 0]) == [0, 1, 0, 0] and plane(cross([0, 1, 0], [1, 0, 1]), [1, 0, 0]) == [1, 0, -1, -1] and online([0, 0, -1], [1, 0, 1], [1, 0, 0]))
t6, X6 = meet_lp([0, 0, 0], [1, 2, 0], [1, 1, 1, -3]); ck(X6 == [1, 2, 0] and sub(X6, [1, 1, 1]) == [0, 1, -1] and dot([0, 1, -1], [1, 1, 1]) == 0)
o6d = through([0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0]); ck(o6d[0] == [0, 0, 1, 0] and o6d[1] == [0, 1, 0, 0] and par_(o6d[2], [1, 0, 0]) and o6d[4] is None and o6d[3] == [1, 0, 0])
S.append(("Recta que pasa por un punto y corta a dos rectas", [
 (1, r"Halla la recta que pasa por el punto $P(2,1,1)$ y corta a las rectas $r:" + sy('x=0', 'y=0') + r"$ \ y \ $s:" + sy('x=1', 'z=0') + r"$ \ Calcula también los puntos de corte."
     + recorda(r"$t=\pi_1\cap\pi_2$, donde $\pi_1$ es el plano que contiene $P$ y $r$, y $\pi_2$, el que contiene $P$ y $s$. Comprueba que $t$ no es paralela a $r$ ni a $s$."),
     r"$\pi_1$ ($P$ y el eje $OZ$): $x-2y=0$; \ $\pi_2$ ($P$ y $s$): $x-z-1=0$. \ $\res{t:" + sy('x-2y=0', 'x-z-1=0') + r"}$, \ vector director $(2,1,2)$. \ Corta a $r$ en $\res{(0,0,-1)}$ y a $s$ en $\res{\left(1,\tfrac12,0\right)}$"),
 (2, r"Halla la recta paralela al vector $\vec v=(1,0,1)$ que corta a las rectas $r$ y $s$ del ejercicio anterior.",
     r"$\pi_1$ contiene $r$ y $\vec v$: $y=0$; \ $\pi_2$ contiene $s$ y $\vec v$: $x-z-1=0$. \ $\res{t:" + sy('y=0', 'x-z-1=0') + r"}$, \ es decir, $(x,y,z)=(0,0,-1)+k\,(1,0,1)$, que corta a $r$ en $(0,0,-1)$ y a $s$ en $(1,0,0)$."),
 (2, r"Halla la recta contenida en el plano $\pi:x+y+z=3$ que pasa por el punto $P(1,1,1)$ y corta a la recta $r:(x,y,z)=\lambda\,(1,2,0)$.",
     r"$r\cap\pi$: $3\lambda=3$, $X(1,2,0)$. La recta es $PX$: \ $\res{(x,y,z)=(1,1,1)+k\,(0,1,-1)}$ \ (está en $\pi$: $P\in\pi$ y $(0,1,-1)\perp(1,1,1)$)."),
 (2, r"Razona que no existe ninguna recta que pase por el origen y corte a las rectas $r:(x,y,z)=(1,0,0)+\lambda\,(0,1,0)$ y $s:(x,y,z)=(0,0,1)+\mu\,(1,0,0)$.",
     r"$\pi_1$ ($O$ y $r$): $z=0$; \ $\pi_2$ ($O$ y $s$): $y=0$. Su intersección es el eje $OX$, que corta a $r$ en $(1,0,0)$ pero \rest{es paralelo a $s$} (y no la contiene): no hay solución."),
]))

# =====================================================================
# 7. Perpendicular comuna
def comperp(P, d, Q, e):                                                  # plans (r, w) i (s, w), peus i distància²
    w = prim(cross(d, e)); pr, ps = plane(cross(d, w), P), plane(cross(e, w), Q)
    la, mu, X, Y = feet(P, d, Q, e); assert onp(pr, X) and onp(ps, X) and onp(pr, Y) and onp(ps, Y)
    return w, pr, ps, X, Y, n2(sub(Y, X))
c7a = comperp([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 1]); ck(c7a[0] == [1, -1, 1] and c7a[3] == [F(2, 3), F(2, 3), 0] and c7a[4] == [1, F(1, 3), F(1, 3)] and c7a[5] == F(1, 3))
c7b = comperp([1, 0, 0], [1, 1, 0], [0, 0, 1], [1, -1, 0]); ck(c7b[0] == [0, 0, 1] and c7b[1] == [1, -1, 0, -1] and c7b[2] == [1, 1, 0, 0] and c7b[3] == [F(1, 2), F(-1, 2), 0] and c7b[4] == [F(1, 2), F(-1, 2), 1] and c7b[5] == 1)
S.append(("Perpendicular común", [
 (2, r"Halla los puntos $X\in r$ e $Y\in s$ más próximos de las rectas $r:" + sy('x-y=0', 'z=0') + r"$ \ y \ $s:" + sy('x=1', 'y-z=0') + r"$ \ del ejercicio \ref{ex:pc} y su perpendicular común. Comprueba que $|\overrightarrow{XY}|=d(r,s)$."
     + recorda(r"Con los puntos genéricos $X\in r$, $Y\in s$, impón $\overrightarrow{XY}\perp\vec d_r$ y $\overrightarrow{XY}\perp\vec d_s$."),
     r"$X(\lambda,\lambda,0)$, $Y(1,\mu,\mu)$: \ $1-2\lambda+\mu=0$, \ $2\mu-\lambda=0$ \ $\Rightarrow$ \ $\lambda=\tfrac23$, $\mu=\tfrac13$: \ $\res{X\left(\tfrac23,\tfrac23,0\right),\ Y\left(1,\tfrac13,\tfrac13\right)}$; \ perpendicular común: \ $\res{(x,y,z)=\left(\tfrac23,\tfrac23,0\right)+t\,(1,-1,1)}$. \ $|\overrightarrow{XY}|=\left|\left(\tfrac13,-\tfrac13,\tfrac13\right)\right|=\tfrac{\sqrt3}{3}$ \ \checkmark"),
 (2, r"Sean $r:(x,y,z)=(1,0,0)+\lambda\,(1,1,0)$ y $s:(x,y,z)=(0,0,1)+\mu\,(1,-1,0)$. Halla la perpendicular común por el método de los planos y comprueba el resultado con los puntos genéricos. ¿Cuál es la distancia entre $r$ y $s$?"
     + recorda(r"$\vec w=\vec d_r\times\vec d_s$; \ $\pi_r$ contiene $r$ y $\vec w$; \ $\pi_s$ contiene $s$ y $\vec w$; \ la perpendicular común es $\pi_r\cap\pi_s$."),
     r"$\vec w\parallel(0,0,1)$; \ $\pi_r:x-y-1=0$, \ $\pi_s:x+y=0$: \ $\res{t:" + sy('x-y-1=0', 'x+y=0') + r"}$, \ es decir, $x=\tfrac12$, $y=-\tfrac12$. \ Puntos genéricos: $\lambda=-\tfrac12$, $\mu=\tfrac12$, \ $X\left(\tfrac12,-\tfrac12,0\right)$, $Y\left(\tfrac12,-\tfrac12,1\right)$; \ $d=|\overrightarrow{XY}|=\res{1}$"),
]))

# =====================================================================
# 6. Simètrics respecte d'un punt i d'una recta
ck(sym([0, 1, -1], [1, -2, 3]) == [-1, 4, -5] and mul(add([1, -2, 3], [5, 0, 1]), F(1, 2)) == [3, -1, 2])
M6 = projl([2, 1, 0], [0, 0, 1], [1, 0, 1]); ck(M6 == [F(1, 2), 0, F(3, 2)] and sym(M6, [2, 1, 0]) == [-1, -1, 3])
ck(sym(projl([1, 2, 3], [0, 0, 0], [1, 0, 0]), [1, 2, 3]) == [1, -2, -3])
d6 = cross([1, 1, 0], [0, 0, 1]); ck(d6 == [1, -1, 0] and projl([0, 0, 1], [1, 1, 0], d6) == [1, 1, 0] and sym([1, 1, 0], [0, 0, 1]) == [2, 2, -1])
S.append(("Simétricos respecto de un punto y de una recta", [
 (1, r"Calcula el simétrico de $A(1,-2,3)$ respecto del punto $B(0,1,-1)$. Halla también el punto $M$ respecto del cual $A$ y $A'(5,0,1)$ son simétricos.",
     r"$A'=2B-A=\res{(-1,4,-5)}$. \qquad $M$ es el punto medio: \ $M=\dfrac{A+A'}{2}=\res{(3,-1,2)}$"),
 (2, r"Calcula el simétrico del punto $P(2,1,0)$ respecto de la recta $r:(x,y,z)=(0,0,1)+\lambda\,(1,0,1)$."
     + recorda(r"Plano por $P$ perpendicular a $r$ $\to$ $M=r\cap\pi$ $\to$ $P'=2M-P$."),
     r"Plano: $x+z=2$; \ corte: $\lambda+1+\lambda=2$, $\lambda=\tfrac12$, \ $M\left(\tfrac12,0,\tfrac32\right)$; \ $P'=2M-P=\res{(-1,-1,3)}$"),
 (2, r"Calcula el simétrico de:" + tasks(1, [r"$P(1,2,3)$ respecto del eje $OX$;", r"$P(0,0,1)$ respecto de la recta $r:" + sy('x+y=2', 'z=0') + r"$"]),
     tasks(1, [r"$M(1,0,0)$: \ $\res{P'(1,-2,-3)}$", r"$\vec d=(1,-1,0)$, $A(1,1,0)$; \ $\overrightarrow{AP}\cdot\vec d=0$, de modo que $M=A=(1,1,0)$: \ $\res{P'(2,2,-1)}$"])),
]))

# =====================================================================
# 7. Simètrics respecte d'un pla
ck(projp([3, 1, 2], [2, -1, 1, -1]) == [1, 2, 1] and sym([1, 2, 1], [3, 1, 2]) == [-1, 3, 0])
ck(sym(projp([1, 2, 3], [0, 0, 1, 0]), [1, 2, 3]) == [1, 2, -3] and sym(projp([1, 2, 3], [1, -1, 0, 0]), [1, 2, 3]) == [2, 1, 3])
ck(med([1, 2, -1], [3, 0, 1]) == [1, -1, 1, -1])
t7, X7 = meet_lp([1, 1, 1], [1, 2, 0], [1, 1, 1, 0]); ck(t7 == -1 and X7 == [0, -1, 1])
ck(projp([1, 1, 1], [1, 1, 1, 0]) == [0, 0, 0] and sub([-1, -1, -1], X7) == [-1, 0, -2])
ck(pos_rp([2, 0, 0], [0, 1, -1], [0, 1, 1, -4]) == 'paral·lels' and projp([2, 0, 0], [0, 1, 1, -4]) == [2, 2, 2] and sym([2, 2, 2], [2, 0, 0]) == [2, 4, 4])
S.append(("Simétricos respecto de un plano", [
 (1, r"Calcula el simétrico del punto $P(3,1,2)$ respecto del plano $\pi:2x-y+z-1=0$."
     + recorda(r"Recta por $P$ con vector director $\vec n$ $\to$ $M=s\cap\pi$ (la proyección) $\to$ $P'=2M-P$."),
     r"$(3+2t,\ 1-t,\ 2+t)$: \ $6+6t=0$, $t=-1$, \ $M(1,2,1)$; \ $P'=\res{(-1,3,0)}$"),
 (1, r"Calcula los simétricos del punto $A(1,2,3)$ respecto de los planos $z=0$ y $x=y$.",
     tasks(2, [r"$\res{(1,2,-3)}$", r"$x-y=0$: \ $M\left(\tfrac32,\tfrac32,3\right)$, \ $\res{(2,1,3)}$"])),
 (2, r"Halla el plano respecto del cual son simétricos los puntos $P(1,2,-1)$ y $P'(3,0,1)$.",
     r"Es perpendicular a $\overrightarrow{PP'}=(2,-2,2)$ y pasa por el punto medio $(2,1,0)$: \ $\res{x-y+z-1=0}$"),
 (3, r"Sean $r:(x,y,z)=(1,1,1)+\lambda\,(1,2,0)$ y $\pi:x+y+z=0$." + tasks(1, [r"Calcula la recta simétrica de $r$ respecto de $\pi$.", r"Calcula la proyección ortogonal de $r$ sobre $\pi$."]),
     tasks(1, [r"Corte: $3+3\lambda=0$, \ $X(0,-1,1)$. \ Simétrico de $A(1,1,1)$: $M=O$, $A'(-1,-1,-1)$. \ $r':\ \res{(x,y,z)=(0,-1,1)+\mu\,(1,0,2)}$",
               r"Es la recta que pasa por $X$ y por la proyección $M=O$ de $A$: \ $\res{(x,y,z)=\mu\,(0,-1,1)}$"])),
 (2, r"Calcula la recta simétrica de $r:(x,y,z)=(2,0,0)+\lambda\,(0,1,-1)$ respecto del plano $y+z=4$.",
     r"$\vec d\cdot\vec n=0$ y $(2,0,0)\notin\pi$: paralelos. \ Simétrico de $A(2,0,0)$: $M(2,2,2)$, $A'(2,4,4)$. \ $r':\ \res{(x,y,z)=(2,4,4)+\mu\,(0,1,-1)}$"),
]))

# =====================================================================
# 8. Àrees i volums
A8, B8, C8 = [1, 2, 0], [3, 0, 1], [0, 1, 2]
cr8 = cross(sub(B8, A8), sub(C8, A8)); ck(cr8 == [-3, -5, -4] and n2(cr8) == 50 and n2(sub(B8, A8)) == 9)
ck(cos2(sub(B8, A8), sub(C8, A8)) == F(4, 54) and near(deg(F(4, 54)), 74.21) and dot(sub(B8, A8), sub(C8, A8)) > 0)
ck(det3(sub([0, 1, 0], [1, 0, 0]), sub([0, 0, 1], [1, 0, 0]), sub([2, 2, 2], [1, 0, 0])) == 5 and pdist2([2, 2, 2], [1, 1, 1, -1]) == F(25, 3))
ck(det3([1, 0, 0], [0, 1, 0], [1, 1, 12]) == 12)
A8b, B8b, C8b = [1, 0, 1], [2, 1, 0], [4, 2, 1]
D8b = sub(add(A8b, C8b), B8b); ck(D8b == [3, 1, 2] and cross(sub(B8b, A8b), sub(D8b, A8b)) == [2, -3, -1] and n2([2, -3, -1]) == 14)
ck(pdist2([0, 0, 0], [2, 3, 6, -12]) == F(144, 49) and F(6 * 4 * 2, 6) == 8 and 3 * 8 / F(12, 7) == 14)
S.append(("Áreas y volúmenes", [
 (1, r"Considera el triángulo de vértices $A(1,2,0)$, $B(3,0,1)$ y $C(0,1,2)$." + tasks(1, [r"Calcula su área.", r"Calcula el ángulo del vértice $A$.", r"Calcula la altura correspondiente al lado $AB$."])
     + recorda(r"$S=\tfrac12|\overrightarrow{AB}\times\overrightarrow{AC}|$. Para el ángulo de un triángulo no ponemos valor absoluto al producto escalar."),
     tasks(1, [r"$\overrightarrow{AB}\times\overrightarrow{AC}=(2,-2,1)\times(-1,-1,2)=(-3,-5,-4)$: \ $S=\dfrac{\sqrt{50}}{2}=\res{\dfrac{5\sqrt2}{2}}$",
               r"$\cos\hat A=\dfrac{-2+2+2}{3\sqrt6}=\dfrac{\sqrt6}{9}$ \ $\Rightarrow$ \ $\res{\hat A\approx74{,}21^\circ}$", r"$h=\dfrac{2S}{|\overrightarrow{AB}|}=\res{\dfrac{5\sqrt2}{3}}$"])),
 (2, r"Calcula el volumen del tetraedro de vértices $A(1,0,0)$, $B(0,1,0)$, $C(0,0,1)$ y $D(2,2,2)$, y su altura desde $D$.",
     r"$[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}]=" + vm([[-1, 1, 0], [-1, 0, 1], [1, 2, 2]]) + r"=5$: \ $\res{V=\tfrac56}$. \ Plano $ABC$: $x+y+z-1=0$; \ $h=d(D,\pi)=\dfrac{5}{\sqrt3}=\res{\dfrac{5\sqrt3}{3}}$"),
 (2, r"Halla $a$ para que el tetraedro de vértices $O$, $(1,0,0)$, $(0,1,0)$ y $(1,1,a)$ tenga volumen 2.",
     r"$V=\tfrac16" + vm([[1, 0, 0], [0, 1, 0], [1, 1, 'a']]) + r"=\dfrac{|a|}{6}=2$ \ $\Rightarrow$ \ $\res{a=\pm12}$"),
 (2, r"Tres vértices consecutivos de un paralelogramo $ABCD$ son $A(1,0,1)$, $B(2,1,0)$ y $C(4,2,1)$. Halla el cuarto vértice y el área del paralelogramo.",
     r"$D=A+C-B=\res{(3,1,2)}$. \ $S=|\overrightarrow{AB}\times\overrightarrow{AD}|=|(1,1,-1)\times(2,1,1)|=|(2,-3,-1)|=\res{\sqrt{14}}$"),
 (2, r"El plano $\pi:2x+3y+6z=12$ corta los ejes en $A$, $B$ y $C$. Calcula el volumen del tetraedro $OABC$, la distancia del origen a $\pi$ y, con estos dos datos, el área del triángulo $ABC$.",
     r"$A(6,0,0)$, $B(0,4,0)$, $C(0,0,2)$: \ $V=\tfrac16\cdot6\cdot4\cdot2=\res{8}$. \ $d(O,\pi)=\dfrac{12}{7}$. \ $S=\dfrac{3V}{h}=\dfrac{24}{12/7}=\res{14}$"),
]))

# =====================================================================
# 9. Llocs geomètrics
ck(med([2, 1, -1], [0, 3, 1]) == [1, -1, -1, 1])
c9a, c9b = [1, 1, -1, -1], [1, -1, 1, -3]
ck([a - b for a, b in zip(c9a, c9b)] == [0, 2, -2, 2] and [a + b for a, b in zip(c9a, c9b)] == [2, 0, 0, -4])
ck(all(pdist2(P_, c9a) == pdist2(P_, c9b) for P_ in ([2, 0, 0], [2, 5, -3], [0, 0, 1], [7, 1, 2])))
ck(all(pdist2(P_, [2, -1, 2, -1]) == pdist2(P_, [2, -1, 2, -7]) for P_ in ([2, 0, 0], [0, -4, 0], [1, 0, 1])))
ck(n2(sub([3, 2, -1], [1, 0, -2])) == 9 and plane(sub([3, 2, -1], [1, 0, -2]), [3, 2, -1]) == [2, 2, 1, -9])
ck(pdist2([2, -1, 1], [1, 2, 2, 7]) == 9 and projp([2, -1, 1], [1, 2, 2, 7]) == [1, -3, -1])
ck(med([1, 0, 0], [0, 1, 0]) == [1, -1, 0, 0] and med([0, 1, 0], [0, 0, 1]) == [0, 1, -1, 0])
S.append(("Lugares geométricos", [
 (1, r"Halla el plano mediador del segmento de extremos $A(2,1,-1)$ y $B(0,3,1)$ de dos maneras: imponiendo $d(X,A)=d(X,B)$ y con el punto medio y el vector $\overrightarrow{AB}$.",
     r"$(x-2)^2+(y-1)^2+(z+1)^2=x^2+(y-3)^2+(z-1)^2$ \ $\Rightarrow$ \ $-4x+4y+4z-4=0$. \ O bien: $\overrightarrow{AB}=(-2,2,2)$, $M(1,2,0)$. \ $\res{x-y-z+1=0}$"),
 (2, r"Halla los planos bisectores de los planos $\pi_1:x+y-z=1$ y $\pi_2:x-y+z=3$."
     + recorda(r"Son los puntos que equidistan de los dos planos: $\dfrac{|A_1x+B_1y+C_1z+D_1|}{|\vec n_1|}=\dfrac{|A_2x+B_2y+C_2z+D_2|}{|\vec n_2|}$."),
     r"$|\vec n_1|=|\vec n_2|=\sqrt3$: \ $x+y-z-1=\pm(x-y+z-3)$: \ $\res{y-z+1=0}$ \ y \ $\res{x=2}$ \ (perpendiculares entre sí)."),
 (1, r"Halla el lugar geométrico de los puntos que equidistan de los planos $2x-y+2z=1$ y $2x-y+2z=7$.",
     r"$|2x-y+2z-1|=|2x-y+2z-7|$: el signo $+$ es imposible y el $-$ da \ $\res{2x-y+2z=4}$, el plano paralelo situado a media distancia."),
 (2, r"Escribe la ecuación de la esfera de centro $C(1,0,-2)$ que pasa por el punto $P(3,2,-1)$ y la del plano tangente a la esfera en $P$.",
     r"$R=|\overrightarrow{CP}|=|(2,2,1)|=3$: \ $\res{(x-1)^2+y^2+(z+2)^2=9}$. \ El plano tangente es perpendicular al radio $\overrightarrow{CP}$: \ $\res{2x+2y+z-9=0}$"),
 (2, r"Halla la esfera de centro $C(2,-1,1)$ tangente al plano $x+2y+2z+7=0$ y el punto de tangencia.",
     r"$R=d(C,\pi)=\dfrac{|2-2+2+7|}{3}=3$: \ $\res{(x-2)^2+(y+1)^2+(z-1)^2=9}$. \ Punto de tangencia = proyección de $C$: \ $\res{(1,-3,-1)}$"),
 (3, r"Halla el lugar geométrico de los puntos del espacio que equidistan de $A(1,0,0)$, $B(0,1,0)$ y $C(0,0,1)$.",
     r"Debe estar en el plano mediador de $AB$ ($x=y$) y en el de $BC$ ($y=z$): \ es la recta \ $\res{x=y=z}$, perpendicular al plano $ABC$ por su circuncentro."),
]))

# =====================================================================
# 10. Problemes i qüestions
ck(meet_lp([1, 2, 5], [1, 0, -1], [0, 0, 1, 0]) == (5, [6, 2, 0]) and sym(projp([1, 2, 5], [0, 0, 1, 0]), [1, 2, 5]) == [1, 2, -5] and sub([6, 2, 0], [1, 2, -5]) == [5, 0, 5])
B10 = sym(projp([4, 5, 1], [0, 0, 1, 0]), [4, 5, 1]); ck(B10 == [4, 5, -1])
t10, X10 = meet_lp([1, 1, 2], sub(B10, [1, 1, 2]), [0, 0, 1, 0]); ck(t10 == F(2, 3) and X10 == [3, F(11, 3), 0] and n2(sub(B10, [1, 1, 2])) == 34)
S.append(("Problemas y cuestiones", [
 (2, r"Un rayo de luz sale del punto $P(1,2,5)$ en la dirección del vector $(1,0,-1)$, se refleja en un espejo situado en el plano $z=0$ y continúa. Halla el punto donde toca el espejo y la ecuación del rayo reflejado."
     + recorda(r"El rayo reflejado es la recta que pasa por el punto de incidencia y por el simétrico de $P$ respecto del espejo."),
     r"$(1+t,\ 2,\ 5-t)$ con $z=0$: \ $t=5$, \ $\res{X(6,2,0)}$. \ $P'(1,2,-5)$, \ $\overrightarrow{P'X}=(5,0,5)$: \ rayo reflejado \ $\res{(x,y,z)=(6,2,0)+\mu\,(1,0,1)},\ \mu\ge0$"),
 (3, r"Sean $A(1,1,2)$ y $B(4,5,1)$, ambos por encima del plano $z=0$. Halla el punto $X$ del plano $z=0$ que hace mínima la suma $d(A,X)+d(X,B)$ y el valor de esta suma mínima.",
     r"Si $B'(4,5,-1)$ es el simétrico de $B$, $d(X,B)=d(X,B')$ y el camino más corto es el segmento $AB'$. \ $A+t\,(3,4,-3)$ con $z=0$: $t=\tfrac23$: \ $\res{X\left(3,\tfrac{11}{3},0\right)}$; \ suma mínima \ $|\overrightarrow{AB'}|=\res{\sqrt{34}}$"),
 (2, r"Razona si son ciertas o falsas las afirmaciones siguientes:" + tasks(1, [r"Dos planos perpendiculares a un mismo plano son siempre paralelos entre sí.", r"Si una recta es perpendicular a un plano, es perpendicular a todas las rectas contenidas en el plano.",
     r"La distancia entre dos rectas que se cruzan puede ser 0.", r"Si $d(P,\pi)=0$, el punto $P$ está en el plano $\pi$."]),
     tasks(1, [r"\rest{Falsa}: por ejemplo, $x=0$ e $y=0$ son perpendiculares a $z=0$ y se cortan.", r"\rest{Cierta}: su vector director es proporcional a $\vec n$, que es perpendicular a cualquier vector del plano (también si la recta del plano no pasa por el punto de corte: se cruzan perpendicularmente).",
               r"\rest{Falsa}: si se cruzan no tienen ningún punto común y $[\overrightarrow{PQ},\vec d_r,\vec d_s]\neq0$, por tanto $d>0$.", r"\rest{Cierta}: $|Ax_0+By_0+Cz_0+D|=0$ quiere decir que $P$ cumple la ecuación del plano."])),
]))

SEC = {t: exs for t, exs in S}
def pau(sec, *exs): SEC[sec].extend(exs)

# =====================================================================
# PAU d'altres comunitats (recull ebaumatematicas 2026/27, bloc de geometria a l'espai)
# ---------- 1. Angles
t_, Q_ = meet_lp([-21, 3, 5], [11, -1, -2], [1, 3, 2, -10]); ck(t_ == 3 and Q_ == [12, 0, -1] and cos2([11, -1, -2], [1, 3, 2]) == F(16, 1764) and near(deg(F(16, 1764), True), 5.46))
ck(all(abs(6 * a_ * a_ - 16 * a_ - 1) < 1e-9 for a_ in ((8 + math.sqrt(70)) / 6, (8 - math.sqrt(70)) / 6)))
a13 = (8 + math.sqrt(70)) / 6; ck(abs(math.degrees(math.acos((2 * a13 - 1) / (math.sqrt(1 + 2 * a13 * a13) * math.sqrt(5)))) - 60) < 1e-9)
a13b = (8 - math.sqrt(70)) / 6; ck(abs(math.degrees(math.acos((2 * a13b - 1) / (math.sqrt(1 + 2 * a13b * a13b) * math.sqrt(5)))) - 120) < 1e-9)
nPB = plane3([2, 3, 4], [3, -1, -2], [5, -1, 2]); ck(nPB == [2, 2, -1, -6] and cos2([1, 6, 8], [2, 2, -1]) == F(4, 101) and dms(deg(F(4, 101), True)) == r"11^\circ\,28'\,44''" and onp(nPB, [6, -5, -4]))
dC8 = cross([2, -3, -1], [1, 1, 2]); ck(par_(dC8, [1, 1, -1]) and onp([1, 3, 2, 3], [1, 0, -2]) and dot([2, -3, -1], [1, 0, -2]) == 4 and dot([1, 1, 2], [1, 0, -2]) == -3)
ck(cos2([1, 1, -1], [1, 3, 2]) == F(4, 42) and near(deg(F(4, 42), True), 17.98))
d12 = cross([1, 1, 1], [4, -1, 1]); ck(d12 == [2, 3, -5] and cross([1, 1, -2], d12) == [1, 1, 1])
X12 = [F(2, 5), F(-7, 5), 0]; ck(onp([1, 1, 1, 1], X12) and onp([4, -1, 1, -3], X12) and onp([1, 1, -2, 1], X12))
pau("Ángulos entre rectas y planos",
 (2, r"\pau{Canarias, extraordinaria 2026} Se sabe que el plano $\pi:x+3y+2z=10$ y la recta $r:\dfrac{x+21}{11}=3-y=\dfrac{5-z}{2}$ son secantes." + tasks(1, [r"Halla el punto de corte del plano $\pi$ y la recta $r$.", r"Calcula el ángulo que forman el plano $\pi$ y la recta $r$."]),
     tasks(1, [r"$r:(-21+11t,\ 3-t,\ 5-2t)$; \ en $\pi$: $4t-2=10$, $t=3$: \ $\res{Q(12,0,-1)}$", r"$\vec d=(11,-1,-2)$, $\vec n=(1,3,2)$: \ $\sin\alpha=\dfrac{|11-3-4|}{\sqrt{126}\,\sqrt{14}}=\dfrac{4}{42}=\dfrac{2}{21}$ \ $\Rightarrow$ \ $\res{\alpha\approx5{,}47^\circ}$"])),
 (2, r"\pau{Castilla-La Mancha, ordinaria 2024} Sean los vectores $\vec u=(1,a,a)$ y $\vec v=(-1,0,2)$, con $a\in\mathbb R$. Determina el valor de $a$ para que el ángulo entre los vectores $\vec u$ y $\vec v$ sea de $60^\circ$.",
     r"$\vec u\cdot\vec v=2a-1=|\vec u|\,|\vec v|\cos60^\circ=\tfrac12\sqrt{1+2a^2}\,\sqrt5$. \ Hace falta $2a-1>0$; elevando al cuadrado: $6a^2-16a-1=0$, \ $a=\dfrac{8\pm\sqrt{70}}{6}$. \ Solo sirve \ $\res{a=\dfrac{8+\sqrt{70}}{6}\approx2{,}73}$ \ (la otra da $120^\circ$)."),
 (2, r"\pau{País Vasco, extraordinaria 2025} Sean $\pi$ el plano que pasa por los puntos $A(2,3,4)$, $B(3,-1,-2)$, $C(5,-1,2)$ y $r$ la recta que pasa por los puntos $D(6,-5,-4)$, $E(7,1,4)$." + tasks(1, [r"Calcula el ángulo entre el plano $\pi$ y la recta $r$, expresando el resultado en grados, minutos y segundos.", r"En caso de que $r$ y $\pi$ se corten, calcula el punto de intersección. En caso contrario, calcula la distancia entre la recta $r$ y el plano $\pi$."]),
     tasks(1, [r"$\vec n\parallel\overrightarrow{AB}\times\overrightarrow{AC}=(-16,-16,8)$, \ $\vec n=(2,2,-1)$, \ $\vec d=(1,6,8)$: \ $\sin\alpha=\dfrac{6}{3\sqrt{101}}=\dfrac{2}{\sqrt{101}}$ \ $\Rightarrow$ \ $\res{\alpha\approx" + dms(deg(F(4, 101), True)) + r"}$",
               r"$\pi:2x+2y-z-6=0$; \ se cortan ($\vec d\cdot\vec n\neq0$) y $D$ ya está en el plano: \ $\res{D(6,-5,-4)}$"])),
 (2, r"\pau{Canarias, extraordinaria 2024}" + tasks(1, [r"Justifica si pueden existir vectores $\vec u$ y $\vec v$, con el mismo origen, que cumplan $|\vec u|=2$, $|\vec v|=3$ y $\vec u\cdot\vec v=8$.",
     r"Dados el plano $\pi:x+3y+2z+3=0$ y la recta $r:" + sy('2x-3y-z=4', 'x+y+2z=-3') + r"$, que son secantes, calcula el punto de corte de la recta y el plano y el ángulo que forman."]),
     tasks(1, [r"$|\vec u\cdot\vec v|\le|\vec u|\,|\vec v|=6<8$ (sería $\cos\alpha=\tfrac43>1$): \ \rest{no pueden existir}.", r"$\vec d\parallel(2,-3,-1)\times(1,1,2)=(-5,-5,5)$, $\vec d=(1,1,-1)$. \ Punto: $\res{P(1,0,-2)}$. \ $\sin\alpha=\dfrac{2}{\sqrt3\sqrt{14}}$ \ $\Rightarrow$ \ $\res{\alpha\approx17{,}98^\circ}$"])),
 (2, r"\pau{La Rioja, ordinaria 2024} Halla la ecuación continua de la recta $s$ que está contenida en el plano $\pi:x+y-2z+1=0$ y corta perpendicularmente a la recta $r:" + sy('x+y+z=-1', '4x-y+z=3') + r"$",
     r"$\vec d_r=(1,1,1)\times(4,-1,1)=(2,3,-5)$. \ $r\cap\pi=\left(\tfrac25,-\tfrac75,0\right)$. \ $\vec d_s=\vec n\times\vec d_r=(1,1,1)$: \ $\res{s:x-\tfrac25=y+\tfrac75=z}$"),
)

# ---------- 2. Distància a un pla
ck(projp([0, -1, -2], [1, 2, 3, -6]) == [1, 1, 1] and pdist2([0, -1, -2], [1, 2, 3, -6]) == 14 and dot([1, 2, 3], [1, 1, -1]) == 0)
ck(projp([1, 3, 0], [1, 2, -2, 7]) == [F(-5, 9), F(-1, 9), F(28, 9)] and pdist2([1, 3, 0], [1, 2, -2, 7]) == F(196, 9) and pdist2([1, 3, 0], [1, 2, -2, -21]) == F(196, 9))
ck(plane3([1, 0, 1], [0, 1, 0], [1, 1, 1]) == [1, 0, -1, 0] and all(pdist2([a_, 0, 0], [1, 0, -1, 0]) == 2 for a_ in (2, -2)))
ck(all(pdist2([0, 0, 0], [2, 2, 1, k_]) == 4 for k_ in (6, -6)) and projp([0, 0, 0], [2, 2, 1, -5]) == [F(10, 9), F(10, 9), F(5, 9)] and n2(cross([F(10, 9), F(10, 9), F(5, 9)], [3, 3, 3])) == F(50, 9))
ck(all(abs(det3([0, 2, -2], [1, 2, m_], [2, 3, 2])) == 18 for m_ in (5, -4)) and plane3([0, 2, -2], [1, 2, 0], [2, 3, 2]) == [2, 0, -1, -2] and pdist2([0, 0, 0], [2, 0, -1, -2]) == F(4, 5))
pau("Distancia entre puntos y de un punto a un plano",
 (2, r"\pau{Asturias, ordinaria 2026} Se considera el plano $\pi:x+2y+3z=6$ y el punto $P(0,-1,-2)$." + tasks(1, [r"Halla la ecuación de una recta paralela a $\pi$ que contenga el punto $P$. ¿Es única esta recta?", r"Calcula el punto $Q\in\pi$ que dista menos de $P$. ¿Qué distancia hay entre $P$ y $Q$?"]),
     tasks(1, [r"Basta un vector director perpendicular a $\vec n=(1,2,3)$: $\res{(x,y,z)=(0,-1,-2)+\lambda\,(1,1,-1)}$. \rest{No es única} (hay infinitas).", r"$(t,\ -1+2t,\ -2+3t)$: $14t-14=0$, $t=1$: \ $\res{Q(1,1,1)}$, \ $d(P,Q)=\res{\sqrt{14}}$"])),
 (2, r"\pau{Cataluña, extraordinaria 2024} Considera el punto $P(1,3,0)$ y el plano $\pi:x+2y-2z=-7$." + tasks(1, [r"Sea $r$ la recta perpendicular a $\pi$ que pasa por $P$. Calcula el punto de intersección de $\pi$ con $r$.", r"Calcula la distancia $d$ del punto $P$ al plano $\pi$.", r"Calcula la ecuación de otro plano $\pi'$ paralelo a $\pi$ que también esté a distancia $d$ de $P$."]),
     tasks(1, [r"$(1+t,\ 3+2t,\ -2t)$: $14+9t=0$: \ $\res{\left(-\tfrac59,-\tfrac19,\tfrac{28}{9}\right)}$", r"$d=\dfrac{|1+6+7|}{3}=\res{\dfrac{14}{3}}$", r"$x+2y-2z+k=0$ con $|7+k|=14$, $k\neq7$: \ $\res{x+2y-2z-21=0}$"])),
 (2, r"\pau{Galicia, ordinaria 2026} Considera los puntos $P(1,0,1)$, $Q(0,1,0)$ y $R(1,1,1)$." + tasks(1, [r"Demuestra que $P$, $Q$ y $R$ no están alineados y obtén la ecuación implícita del plano $\pi$ que pasa por ellos.", r"Calcula el valor o valores de $a$ que hacen que la distancia del punto $S(a,0,0)$ a este plano sea igual a $\sqrt2$ unidades de longitud."]),
     tasks(1, [r"$\overrightarrow{PQ}\times\overrightarrow{PR}=(-1,1,-1)\times(0,1,0)=(1,0,-1)\neq\vec0$: \ $\res{\pi:x-z=0}$", r"$\dfrac{|a|}{\sqrt2}=\sqrt2$: \ $\res{a=\pm2}$"])),
 (2, r"\pau{Asturias, extraordinaria 2026} Dado el plano $\pi:2x+2y+z=5$:" + tasks(1, [r"Halla la ecuación de un plano paralelo a $\pi$ cuya distancia al origen sea 2. ¿Hay más de un plano que cumpla estas condiciones?", r"Calcula el punto $P$ del plano $\pi$ que está más próximo al origen $O$.", r"Calcula el área del paralelogramo formado por los segmentos $OP$ y $OQ$, donde $Q(3,3,3)$."]),
     tasks(1, [r"$2x+2y+z+k=0$ con $\dfrac{|k|}{3}=2$: \ \rest{hay dos}, \ $\res{2x+2y+z\pm6=0}$", r"Proyección de $O$: \ $\res{P\left(\tfrac{10}{9},\tfrac{10}{9},\tfrac59\right)}$", r"$|\overrightarrow{OP}\times\overrightarrow{OQ}|=\left|\left(\tfrac53,-\tfrac53,0\right)\right|=\res{\dfrac{5\sqrt2}{3}}$"])),
 (2, r"\pau{Andalucía, ordinaria 2025} Sean los puntos $O(0,0,0)$, $A(0,2,-2)$, $B(1,2,m)$ y $C(2,3,2)$." + tasks(1, [r"Halla los valores de $m$ para que el tetraedro determinado por los puntos $O$, $A$, $B$ y $C$ tenga un volumen de 3 unidades cúbicas.", r"Para $m=0$, calcula la distancia del punto $O$ al plano que pasa por los puntos $A$, $B$ y $C$."]),
     tasks(1, [r"$[\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC}]=4m-2$; \ $\dfrac{|4m-2|}{6}=3$: \ $\res{m=5\ \text{o}\ m=-4}$", r"Plano $ABC$: $2x-z-2=0$; \ $d(O,\pi)=\dfrac{2}{\sqrt5}=\res{\dfrac{2\sqrt5}{5}}$"])),
)

# ---------- 3. Distància d'un punt a una recta
ck(ldist2([0, 1, 1], [0, 0, 11], [3, 1, -1]) == 90 and plane([3, 1, -1], [0, 1, 1]) == [3, 1, -1, 0])
ck(all(n2(sub([2 + s_, 1 + 2 * s_, s_], [1, 1, 1])) == 6 * s_ * s_ + 2 for s_ in range(-3, 4)) and plane3([2, 1, 0], [3, 3, 1], [1, 1, 1]) == [1, -1, 1, -1] and ldist2([1, 1, 1], [2, 1, 0], [1, 2, 1]) == 2)
ck(plane([-4, 3, 0], [1, -1, 0]) == [4, -3, 0, -7] and ldist2([1, -1, 0], [0, 1, -1], [-4, 3, 0]) == 2 and cos2([-4, 3, 0], [1, -2, 3]) == F(100, 350) and near(deg(F(100, 350), True), 32.31))
ck(plane3([0, 0, 4], [-3, 0, 0], [0, -2, 0]) == [4, 6, -3, 12] and ldist2([1, 1, 1], [0, 0, 4], [-3, 0, -4]) == F(194, 25) and abs(det3([0, 0, 4], [-3, 0, 0], [0, -2, 0])) == 24)
pau("Distancia de un punto a una recta",
 (2, r"\pau{La Rioja, extraordinaria 2026} Sean la recta $r:\dfrac x3=y=\dfrac{z-11}{-1}$ y el punto $P(0,1,1)$." + tasks(1, [r"Determina la ecuación del plano que pasa por el punto $P$ y es perpendicular a la recta $r$.", r"Halla la distancia de $P$ a la recta $r$."]),
     tasks(1, [r"$\res{3x+y-z=0}$", r"$A(0,0,11)$, $\overrightarrow{AP}\times\vec d=(0,1,-10)\times(3,1,-1)=(9,-30,-3)$: \ $d=\dfrac{\sqrt{990}}{\sqrt{11}}=\sqrt{90}=\res{3\sqrt{10}}$"])),
 (2, r"\pau{Cantabria, ordinaria 2025} Considera la recta $r:" + sy('2x-y=3', 'y-2z=1') + r"$ \ y el punto $P(1,1,1)$." + tasks(1, [r"Determina los puntos de $r$ que están a una distancia de $\sqrt{14}$ unidades de $P$.", r"Obtén la ecuación del plano que contiene $r$ y $P$.", r"Calcula la distancia entre $r$ y $P$."]),
     tasks(1, [r"$r:(2+t,\ 1+2t,\ t)$; \ $6t^2+2=14$, $t=\pm\sqrt2$: \ $\res{\left(2\pm\sqrt2,\ 1\pm2\sqrt2,\ \pm\sqrt2\right)}$", r"$\res{x-y+z-1=0}$", r"$\overrightarrow{AP}\times\vec d=(-1,0,1)\times(1,2,1)=(-2,2,-2)$: \ $d=\dfrac{\sqrt{12}}{\sqrt6}=\res{\sqrt2}$"])),
 (2, r"\pau{Extremadura, extraordinaria 2025} Dados la recta $s:\dfrac{x}{-4}=\dfrac{y-1}{3}=\dfrac{z+1}{0}$, el plano $\pi:x-2y+3z-6=0$ y el punto $P(1,-1,0)$:" + tasks(1, [r"Obtén la ecuación del plano perpendicular a la recta $s$ que pasa por $P$.", r"Calcula la distancia del punto $P$ a la recta $s$.", r"Calcula el ángulo que forma la recta $s$ con el plano $\pi$."]),
     tasks(1, [r"$\res{4x-3y-7=0}$", r"$\overrightarrow{AP}\times\vec d=(1,-2,1)\times(-4,3,0)=(-3,-4,-5)$: \ $d=\dfrac{\sqrt{50}}{5}=\res{\sqrt2}$", r"$\sin\alpha=\dfrac{|-4-6|}{5\sqrt{14}}=\dfrac{2}{\sqrt{14}}$ \ $\Rightarrow$ \ $\res{\alpha\approx32{,}31^\circ}$"])),
 (2, r"\pau{Cantabria, ordinaria 2026} Considera los puntos $A(0,0,4)$, $B(-3,0,0)$ y $C(0,-2,0)$." + tasks(1, [r"Halla la ecuación general del plano que contiene $A$, $B$ y $C$.", r"Calcula la distancia entre el punto $P(1,1,1)$ y la recta que contiene $A$ y $B$.", r"Calcula el volumen del tetraedro de vértices $A$, $B$, $C$ y $D(0,0,0)$."]),
     tasks(1, [r"$\res{4x+6y-3z+12=0}$", r"$\overrightarrow{AP}\times\overrightarrow{AB}=(1,1,-3)\times(-3,0,-4)=(-4,13,3)$: \ $d=\dfrac{\sqrt{194}}{5}\approx\res{2{,}79}$", r"$V=\tfrac16|{-24}|=\res{4}$"])),
)

# ---------- 4. Dues rectes
P7, d7, Q7, e7 = [2, -1, 3], [1, -2, 2], [1, 4, 4], [2, -1, -2]
ck(pos_rr([1, 5, 0], [0, 1, 1], [7, -5, 7], [3, 1, 0]) == "s'encreuen" and skew2([1, 5, 0], [0, 1, 1], [7, -5, 7], [3, 1, 0]) == 171 and rad(171) == r'3\sqrt{19}')
n5 = cross([0, 1, 1], [3, 1, 0]); ck(plane(cross([0, 1, 1], n5), [1, 5, 0]) == [6, 1, -1, -11] and plane(cross([3, 1, 0], n5), [7, -5, 7]) == [3, -9, -10, 4])
la5, mu5, X5, Y5 = feet([1, 5, 0], [0, 1, 1], [7, -5, 7], [3, 1, 0]); ck(n2(sub(Y5, X5)) == 171)
la2, mu2, X2, Y2 = feet([0, -3, 2], [1, 1, -2], [-4, 1, -1], [3, 1, 2]); ck(par_(sub(Y2, X2), [2, -4, -1]) and online([-1, 2, 1], [2, -4, -1], X2))
ck(skew2([-4, 4, 1], [5, -4, -2], [-2, 7, -1], [4, -4, 0]) == F(64, 9) and pos_rr([-4, 4, 1], [5, -4, -2], [-2, 7, -1], [4, -4, 0]) == "s'encreuen")
ck(skew2([5, -1, 8], [1, 0, 2], [2, 2, -1], [3, -1, 4]) == 9)
pau("Distancia entre dos rectas",
 (2, r"\pau{País Vasco, ordinaria 2025} Se consideran la recta $r$ que pasa por los puntos $A(-4,4,1)$ y $B(1,0,-1)$ y la recta $s$ que pasa por los puntos $C(-2,7,-1)$ y $D(2,3,-1)$." + tasks(1, [r"Calcula la posición relativa de la recta $r$ respecto de la recta $s$.", r"En caso de que sean paralelas o se crucen, calcula la distancia entre ellas. Si se cortan, calcula el punto de intersección."]),
     tasks(1, [r"$\vec d_r=(5,-4,-2)$, $\vec d_s=(4,-4,0)$, $[\overrightarrow{AC},\vec d_r,\vec d_s]=-32\neq0$: \ \rest{se cruzan}", r"$|\vec d_r\times\vec d_s|=|(-8,-8,-4)|=12$: \ $d=\dfrac{32}{12}=\res{\dfrac83}$"])),
 (2, r"\pau{La Rioja, extraordinaria 2025} Calcula la distancia entre las rectas $r:" + sy(r'x=5+\lambda', 'y=-1', r'z=8+2\lambda') + r"$ \ y \ $s:" + sy(r'x=2+3\mu', r'y=2-\mu', r'z=-1+4\mu') + r"$",
     r"$\vec d_r\times\vec d_s=(2,2,-1)$, $\overrightarrow{PQ}=(-3,3,-9)$, $[\overrightarrow{PQ},\vec d_r,\vec d_s]=9$: \ $d=\dfrac93=\res{3}$"),
)

# ---------- 5. Recta i pla, dos plans
dA3 = cross([1, -1, 1], [1, 2, -1]); ck(dA3 == [-1, 2, 3] and dot([-8, -1, -2], dA3) == 0 and pdist2([F(10, 3), F(1, 3), 0], [-8, -1, -2, -5]) == F(1024, 69))
ck(pos_rp([0, 1, -1], [3, -1, 2], [1, 1, -1, -3]) == 'paral·lels' and pdist2([0, 1, -1], [1, 1, -1, -3]) == F(1, 3) and plane([3, -1, 2], [0, 1, -1]) == [3, -1, 2, 3])
ck(plane3([1, 1, 0], [3, 2, 3], [2, -1, 1]) == [7, 1, -5, -8] and pos_rp([1, 1, 0], [2, 1, 3], [1, 1, -1, -1]) == 'paral·lels' and pdist2([1, 1, 0], [1, 1, -1, -1]) == F(1, 3))
ck(pos_rp([1, -1, 2], [2, 1, -1], [2, -1, 3, -5]) == 'paral·lels' and pdist2([1, -1, 2], [2, -1, 3, -5]) == F(16, 14))
ck(pos_rp([1, 0, 2], [-3, 2, -1], [1, 1, -1, -2]) == 'paral·lels' and all(pdist2([1, 0, 2], [1, 1, -1, k_]) == 12 for k_ in (7, -5)))
ck(pdist2([0, 1, 3], [2, -1, 1, -5]) == F(9, 6) and onp([2, -1, 1, -2], [0, 1, 3]) and pdist2([0, 0, 2], [2, -1, 1, -5]) == F(9, 6) and pdist2([0, 0, 8], [2, -1, 1, -5]) == F(9, 6))
pau("Distancia entre recta y plano y entre dos planos",
 (2, r"\pau{Andalucía, extraordinaria 2025} Considera la recta $r:" + sy('x-y+z=3', 'x+2y-z=4') + r"$ \ y el plano $\pi:mx-y-2z=5$." + tasks(1, [r"Halla $m$ para que $r$ y $\pi$ sean paralelos.", r"Para $m=-8$, calcula la distancia de la recta $r$ al plano $\pi$."]),
     tasks(1, [r"$\vec d=(1,-1,1)\times(1,2,-1)=(-1,2,3)$; \ $\vec d\cdot\vec n=-m-8=0$: \ $\res{m=-8}$ \ (y $r\not\subset\pi$)", r"$P\left(\tfrac{10}{3},\tfrac13,0\right)\in r$: \ $d=\dfrac{32}{\sqrt{69}}=\res{\dfrac{32\sqrt{69}}{69}}$"])),
 (2, r"\pau{Extremadura, ordinaria 2025}" + tasks(1, [r"Comprueba que el plano $\pi:x+y-z=3$ y la recta $r:\dfrac x3=\dfrac{y-1}{-1}=\dfrac{z+1}{2}$ no se cortan.", r"Calcula la distancia entre el plano $\pi$ y la recta $r$.", r"Obtén la ecuación del plano perpendicular a la recta $r$ que pasa por el punto $(0,1,-1)$."]),
     tasks(1, [r"$\vec d\cdot\vec n=3-1-2=0$ y $(0,1,-1)\notin\pi$: \ \rest{paralelos}", r"$d=\dfrac{|0+1+1-3|}{\sqrt3}=\res{\dfrac{\sqrt3}{3}}$", r"$\res{3x-y+2z+3=0}$"])),
 (2, r"\pau{Galicia, extraordinaria 2026} Considera la recta $r:\dfrac{x-1}{2}=\dfrac{y-1}{1}=\dfrac z3$." + tasks(1, [r"Calcula la ecuación implícita o general del plano $\pi$ que contiene la recta $r$ y el punto $Q(2,-1,1)$.", r"Comprueba que la recta $r$ es paralela al plano $\pi':x+y-z-1=0$. Calcula la distancia de $r$ a $\pi'$."]),
     tasks(1, [r"$\overrightarrow{AQ}\times\vec d=(1,-2,1)\times(2,1,3)=(-7,-1,5)$: \ $\res{7x+y-5z-8=0}$", r"$\vec d\cdot\vec n=2+1-3=0$; \ $d=\dfrac{|1+1-0-1|}{\sqrt3}=\res{\dfrac{\sqrt3}{3}}$"])),
 (2, r"\pau{Murcia, ordinaria 2026} Considera el plano $\pi:2x-y+3z-5=0$ y la recta $r:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$." + tasks(1, [r"Estudia la posición relativa de $r$ y $\pi$.", r"Si $r$ corta a $\pi$ en un solo punto, calcula este punto y el ángulo que forma $r$ con $\pi$. Si $r$ es paralela a $\pi$, calcula la distancia de $r$ a $\pi$."]),
     tasks(1, [r"$\vec d\cdot\vec n=4-1-3=0$ y $(1,-1,2)\notin\pi$: \ \rest{paralelos}", r"$d=\dfrac{|2+1+6-5|}{\sqrt{14}}=\res{\dfrac{4}{\sqrt{14}}=\dfrac{2\sqrt{14}}{7}}$"])),
 (2, r"\pau{Castilla y León, extraordinaria 2025} Sean el plano $\pi:x+y-z=2$ y la recta $r:\dfrac{x-1}{-3}=\dfrac y2=\dfrac{z-2}{-1}$. Calcula la ecuación de un plano $\pi'$ paralelo al plano $\pi$ que esté a una distancia de $2\sqrt3$ unidades de la recta $r$. ¿Es único este plano? Justifica la respuesta.",
     r"$r\parallel\pi$ ($-3+2+1=0$). $\pi':x+y-z+k=0$ con $\dfrac{|1+0-2+k|}{\sqrt3}=2\sqrt3$, $|k-1|=6$: \ \rest{dos planos}, \ $\res{x+y-z+7=0}$ \ y \ $\res{x+y-z-5=0}$"),
 (2, r"\pau{Cataluña, extraordinaria 2025} Considera el plano $\pi:2x-y+z=5$ y el punto $P(0,1,3)$." + tasks(1, [r"Comprueba que la distancia del punto $P$ al plano $\pi$ es $\dfrac{\sqrt6}{2}$.", r"Halla la ecuación general de un plano $\pi_1$ paralelo a $\pi$ que pase por el punto $P$. ¿Cuánto vale la distancia entre $\pi_1$ y $\pi$?", r"Halla la ecuación general de un segundo plano $\pi_2$, distinto de $\pi_1$, que sea paralelo a $\pi$ y que esté a una distancia $\dfrac{\sqrt6}{2}$ de $\pi$."]),
     tasks(1, [r"$\dfrac{|0-1+3-5|}{\sqrt6}=\dfrac{3}{\sqrt6}=\dfrac{\sqrt6}{2}$ \ \checkmark", r"$\res{2x-y+z-2=0}$, \ distancia $\res{\dfrac{\sqrt6}{2}}$ (la de $P$)", r"$2x-y+z+k=0$, $|k+5|=3$, $k\neq-2$: \ $\res{2x-y+z-8=0}$"])),
)

# ---------- 6. Recta per un punt que talla dues rectes
o6n = through([2, 4, -2], [-1, -2, 1], [1, 0, 3], [2, -1, 0], [-1, 2, 1]); ck(o6n[0] == [3, -2, -1, 0] and o6n[1] == [9, 2, 5, -16] and par_(o6n[2], [1, 3, -3]) and o6n[3] == [0, -2, 4] and o6n[4] == [1, 1, 1])
ck(online([2, 4, -2], [1, 3, -3], [1, 1, 1]) and not online([2, 4, 3], [1, 3, -3], [2, 4, -2]))   # la solució del recull porta (z-3), errata
ck(meet_lp([0, 0, 0], [1, 1, 1], [1, 1, 0, 0]) == (0, [0, 0, 0]) and onp([1, 1, 0, 0], [1, -1, 0]))
Am, dm, Bm = [2, -1, 0], [3, -1, 1], [3, -2, 0]; dsm = cross([1, -1, 0], [1, 0, 1])
ck(cross(dm, dsm) == [0, -4, -4] and det3(sub(Bm, Am), dm, dsm) == 4 and plane(dm, [5, -1, 2]) == [3, -1, 1, -18])
ck(dsm == [-1, -1, 1] and onp([1, -1, 0, -5], Bm) and onp([1, 0, 1, -3], Bm) and pos_rr(Am, dm, Bm, dsm) == "s'encreuen" and skew2(Am, dm, Bm, dsm) == F(1, 2))
ck(projl([5, -1, 2], Am, dm) == [5, -2, 1] and sub([5, -2, 1], [5, -1, 2]) == [0, -1, -1])
pau("Recta que pasa por un punto y corta a dos rectas",
 (2, r"\pau{Navarra, extraordinaria 2026} Halla la ecuación continua de la recta $t$ que pasa por el punto $A(2,4,-2)$ y corta a las rectas $s:\dfrac{x-2}{-1}=\dfrac{y+1}{2}=\dfrac z1$ \ y \ $r:" + sy(r'x=-1+\lambda', 'y=-2', r'z=1+3\lambda') + r"$",
     r"Plano por $A$ y $r$: normal $(1,0,3)\times(3,6,-3)\parallel(3,-2,-1)$, \ $3x-2y-z=0$. \ Plano por $A$ y $s$: normal $(-1,2,1)\times(0,5,-2)\parallel(9,2,5)$, \ $9x+2y+5z-16=0$. \ Vector director $(1,3,-3)$: \ $\res{t:\dfrac{x-2}{1}=\dfrac{y-4}{3}=\dfrac{z+2}{-3}}$. Corta a $r$ en $(0,-2,4)$ y a $s$ en $(1,1,1)$."),
 (2, r"\pau{Castilla y León, extraordinaria 2026} Dados el plano $\pi:x+y=0$, el punto $A(1,-1,0)$ y la recta $s:x=y=z$, halla la recta $r$, en forma paramétrica, que pasa por $A$, está contenida en $\pi$ y corta a la recta $s$.",
     r"$s\cap\pi$: $(t,t,t)$ con $2t=0$: $O(0,0,0)$. La recta es $AO$ ($A\in\pi$): \ $\res{r:" + sy(r'x=1+\lambda', r'y=-1-\lambda', 'z=0') + r"}$"),
 (2, r"\pau{Madrid, extraordinaria 2024} Dados el punto $P(5,-1,2)$ y las rectas $r:\dfrac{x-2}{3}=\dfrac{y+1}{-1}=\dfrac{z}{1}$ \ y \ $s:" + sy('x-y=5', 'x+z=3') + r"$" + tasks(1, [r"Estudia la posición relativa de las dos rectas y halla la distancia entre ellas.", r"Determina una ecuación de la recta que pasa por $P$ y corta perpendicularmente a la recta $r$."]),
     tasks(1, [r"$\vec d_s=(1,-1,0)\times(1,0,1)=(-1,-1,1)$, $B(3,-2,0)$; \ $[\overrightarrow{AB},\vec d_r,\vec d_s]=4\neq0$: \rest{se cruzan}; \ $|\vec d_r\times\vec d_s|=|(0,-4,-4)|=4\sqrt2$: \ $d=\res{\dfrac{\sqrt2}{2}\approx0{,}71}$",
               r"Proyección de $P$ sobre $r$: plano $3x-y+z=18$, $M(5,-2,1)$. \ $\res{(x,y,z)=(5,-1,2)+k\,(0,1,1)}$"])),
)

# ---------- 7. Perpendicular comuna
c7n = comperp([3, 7, 0], [1, -3, -1], [4, -1, 0], [-1, 1, -1]); ck(c7n[3] == [5, 1, -2] and c7n[4] == [3, 0, -1] and par_(c7n[0], [2, 1, -1]) and onp([1, 1, -2, -10], [3, 7, 0]) and onp([1, 0, 1, -3], [3, 7, 0]))
ck(cross([1, 1, -2], [1, 0, 1]) == [1, -3, -1] and online([3, 0, -1], [2, 1, -1], [5, 1, -2]))
pau("Perpendicular común",
 (2, r"\pau{Murcia, ordinaria 2025} Considera las rectas $r:" + sy('x=1', 'y=5+\lambda', 'z=\lambda') + r"$ \ y \ $s:" + sy(r'x=7+3\mu', r'y=-5+\mu', 'z=7') + r"$" + tasks(1, [r"Comprueba que se cruzan.", r"Halla la ecuación de la recta perpendicular a ambas.", r"Calcula la distancia entre $r$ y $s$."]),
     tasks(1, [r"$[\overrightarrow{PQ},\vec d_r,\vec d_s]=" + vm([[6, -10, 7], [0, 1, 1], [3, 1, 0]]) + r"=-57\neq0$", r"$\vec n=\vec d_r\times\vec d_s=(-1,3,-3)$; planos que contienen cada recta y $\vec n$: \ $\res{t:" + sy('6x+y-z-11=0', '3x-9y-10z+4=0') + r"}$",
               r"$d=\dfrac{57}{\sqrt{19}}=\res{3\sqrt{19}}$"])),
 (2, r"\pau{Navarra, ordinaria 2026} Halla la ecuación continua de la recta $t$ que corta perpendicularmente a las rectas $r:\dfrac x1=\dfrac{y+3}{1}=\dfrac{z-2}{-2}$ \ y \ $s:" + sy(r'x=-4+3\lambda', r'y=1+\lambda', r'z=-1+2\lambda') + r"$",
     r"$X(\lambda,-3+\lambda,2-2\lambda)$, $Y(-4+3\mu,1+\mu,-1+2\mu)$; \ $\overrightarrow{XY}\perp\vec d_r,\vec d_s$ \ $\Rightarrow$ \ $X" + V(X2) + r"$, $Y" + V(Y2) + r"$: \ $\res{t:\dfrac{x+1}{2}=\dfrac{y-2}{-4}=\dfrac{z-1}{-1}}$"),
 (2, r"\pau{Navarra, extraordinaria 2025} Calcula la ecuación continua de la recta $t$ que corta perpendicularmente a las rectas $r:" + sy('x+y-2z-10=0', 'x+z-3=0') + r"$ \ y \ $s:\dfrac{x-4}{-1}=\dfrac{y+1}{1}=\dfrac{z}{-1}$",
     r"$\vec d_r=(1,1,-2)\times(1,0,1)=(1,-3,-1)$, $P(3,7,0)\in r$. \ Puntos genéricos: $X(3+\lambda,7-3\lambda,-\lambda)$, $Y(4-\mu,-1+\mu,-\mu)$; \ $\overrightarrow{XY}\perp\vec d_r,\vec d_s$ \ $\Rightarrow$ \ $X(5,1,-2)$, $Y(3,0,-1)$: \ $\res{t:\dfrac{x-3}{2}=\dfrac{y}{1}=\dfrac{z+1}{-1}}$"),
)

# ---------- 6. Simètrics (punt i recta)
M10 = projl([1, 0, -1], [1, 0, 0], [1, 2, 2]); ck(M10 == [F(7, 9), F(-4, 9), F(-4, 9)] and sym(M10, [1, 0, -1]) == [F(5, 9), F(-8, 9), F(1, 9)])
M5 = projl([4, -3, 0], [-2, 0, 1], [0, -1, -1]); ck(M5 == [-2, -2, -1] and sym(M5, [4, -3, 0]) == [-8, -1, -2])
pau("Simétricos respecto de un punto y de una recta",
 (2, r"\pau{Castilla y León, ordinaria 2024} Halla el punto simétrico del punto $P(1,0,-1)$ respecto de la recta $r:\dfrac{x-1}{1}=\dfrac y2=\dfrac z2$.",
     r"Plano por $P$ perpendicular: $x+2y+2z+1=0$; \ $9\lambda+2=0$, \ $M" + V(M10) + r"$: \ $\res{P'" + V(sym(M10, [1, 0, -1])) + r"}$"),
 (2, r"\pau{País Vasco, extraordinaria 2025} Halla el punto $P'$ simétrico de $P(4,-3,0)$ respecto de la recta $r$ que pasa por los puntos $A(-2,0,1)$ y $B(-2,-1,0)$.",
     r"$\vec d=(0,-1,-1)$; plano por $P$: $y+z+3=0$; \ $M(-2,-2,-1)$: \ $\res{P'(-8,-1,-2)}$"),
)

# ---------- 7. Simètrics respecte d'un pla
ck(cross([1, -2, 1], [0, 1, -1]) == [1, 1, 1] and projl([2, 2, 1], [4, 1, 0], [1, 1, 1]) == [4, 1, 0] and sym([4, 1, 0], [2, 2, 1]) == [6, 0, -1])
ck(sym(projp([1, -1, -3], [1, -2, 1, 6]), [1, -1, -3]) == [-1, 3, -5])
t1_, X1_ = meet_lp([0, -1, 3], [-2, 2, 2], [1, -2, 1, -3]); ck(X1_ == [-1, 0, 4] and par_(cross([1, -2, 1], [-2, 2, 2]), [3, 2, 1]) and sym(projp([1, 1, 1], [1, -2, 1, -3]), [1, 1, 1]) == [2, -1, 2])
ck(cross([4, -7, 2], [0, 1, -2]) == [12, 8, 4] and dot([3, 2, 1], [-1, 2, 1]) != 0 and sym(projp([1, 0, 2], [-1, 2, 1, 1]), [1, 0, 2]) == [F(5, 3), F(-4, 3), F(4, 3)])
ck(dot([1, 2, -3], [2, -1, 0]) == 0 and sym(projp([2, 3, -4], [1, 2, -3, -6]), [2, 3, -4]) == [0, -1, 2] and pdist2([2, 3, -4], [1, 2, -3, -6]) == 14)
ck(sym(projp([1, 0, 0], [2, 1, -1, -3]), [1, 0, 0]) == [F(5, 3), F(1, 3), F(-1, 3)])
ck(sym(projp([2, 0, 0], [2, 2, -1, -13]), [2, 0, 0]) == [6, 4, -2] and pdist2([2, 0, 0], [2, 2, -1, -13]) == 9 and dot([2, 2, -1], [1, 1, 4]) == 0)
ck(sym([2, -1, 2], [3, 0, -1]) == [1, -2, 5] and sym(projp([3, 0, -1], [1, 2, 1, -8]), [3, 0, -1]) == [5, 4, 1])
pau("Simétricos respecto de un plano",
 (2, r"\pau{Andalucía, ordinaria 2024}" + tasks(1, [r"Halla el punto simétrico de $P(2,2,1)$ respecto de la recta $r:" + sy('x-2y+z=2', 'y-z=1') + r"$", r"Halla el punto simétrico de $Q(1,-1,-3)$ respecto del plano $\pi:x-2y+z+6=0$."]),
     tasks(1, [r"$\vec d=(1,1,1)$, $A(4,1,0)$; plano por $P$: $x+y+z=5$, que corta a $r$ en $M=A$: \ $\res{P'(6,0,-1)}$", r"$(1+t,\ -1-2t,\ -3+t)$: $6+6t=0$, $M(0,1,-4)$: \ $\res{Q'(-1,3,-5)}$"])),
 (2, r"\pau{Andalucía, extraordinaria 2026} Considera la recta $r:" + sy(r'x=-2\lambda', r'y=-1+2\lambda', r'z=3+2\lambda') + r"$ \ y el plano $\pi:x-2y+z-3=0$." + tasks(1, [r"Determina la ecuación de la recta que corta perpendicularmente a $r$ y está contenida en $\pi$.", r"Halla el punto simétrico de $P(1,1,1)$ respecto de $\pi$."]),
     tasks(1, [r"$r\cap\pi=(-1,0,4)$; vector director $\vec n\times\vec d_r\parallel(3,2,1)$: \ $\res{(x,y,z)=(-1,0,4)+\lambda\,(3,2,1)}$", r"$\res{P'(2,-1,2)}$"])),
 (2, r"\pau{Canarias, ordinaria 2025} Se consideran el punto $A(1,0,2)$, el plano $\pi:-x+2y+z+1=0$ y la recta $r:" + sy('4x-7y+2z=7', 'y-2z+5=0') + r"$" + tasks(1, [r"Halla la posición relativa del plano $\pi$ y la recta $r$.", r"Halla el punto simétrico de $A$ respecto del plano $\pi$."]),
     tasks(1, [r"$\vec d\parallel(3,2,1)$, $\vec d\cdot\vec n=2\neq0$: \ \rest{se cortan en un punto}", r"$\res{A'\left(\tfrac53,-\tfrac43,\tfrac43\right)}$"])),
 (2, r"\pau{Extremadura, extraordinaria 2026} Dados los planos $\pi_1:x+ky-3z-6=0$, $\pi_2:2x-y-5=0$ y el punto $A(2,3,-4)$:" + tasks(1, [r"Calcula el valor de $k$ para que los planos $\pi_1$ y $\pi_2$ sean perpendiculares.", r"Para $k=2$, calcula el simétrico del punto $A$ respecto del plano $\pi_1$.", r"Para $k=2$, calcula la distancia del punto $A$ al plano $\pi_1$."]),
     tasks(1, [r"$2-k=0$: \ $\res{k=2}$", r"$(2+t,\ 3+2t,\ -4-3t)$: $14+14t=0$, $M(1,1,-1)$: \ $\res{A'(0,-1,2)}$", r"$\dfrac{14}{\sqrt{14}}=\res{\sqrt{14}}$"])),
 (2, r"\pau{País Vasco, extraordinaria 2026} Sea $P$ el punto de corte de las rectas $r_1:" + sy('x=1+t', 'y=0', 'z=-t') + r"$ \ y \ $r_2:" + sy('x=s', 'y=-1+s', 'z=0') + r"$ \ Calcula el punto $P'$ simétrico de $P$ respecto del plano de ecuación $2x+y-z=3$.",
     r"$1+t=s$, $0=-1+s$, $-t=0$: \ $P(1,0,0)$. \ $(1+2t,\ t,\ -t)$: $6t-1=0$: \ $\res{P'\left(\tfrac53,\tfrac13,-\tfrac13\right)}$"),
 (2, r"\pau{Madrid, ordinaria 2026} Dados el plano $\pi:2x+2y-z=13$ y la recta $r:\dfrac{x-2}{1}=\dfrac y1=\dfrac z4$:" + tasks(1, [r"Halla el punto simétrico del punto $P(2,0,0)$ respecto del plano $\pi$.", r"Halla la distancia entre el plano $\pi$ y la recta $r$."]),
     tasks(1, [r"$(2+2t,\ 2t,\ -t)$: $9t-9=0$, $M(4,2,-1)$: \ $\res{P'(6,4,-2)}$", r"$\vec d\cdot\vec n=2+2-4=0$: paralelos; \ $d=\dfrac{|4-13|}{3}=\res{3}$"])),
 (2, r"\pau{Galicia, extraordinaria 2026} Considera el punto $P(3,0,-1)$." + tasks(1, [r"Calcula el punto $P'$ simétrico de $P$ respecto del punto $Q(2,-1,2)$.", r"Calcula el punto $P''$ simétrico de $P$ respecto del plano $\pi:x+2y+z-8=0$."]),
     tasks(1, [r"$P'=2Q-P=\res{(1,-2,5)}$", r"$(3+t,\ 2t,\ -1+t)$: $6t-6=0$, $M(4,2,0)$: \ $\res{P''(5,4,1)}$"])),
)

# ---------- 8. Àrees i volums
A_1, B_1 = [0, 5, -1], [-3, 11, -10]
ck(par_(sub(B_1, A_1), [1, -2, 3]) and ldist2(A_1, [3, -2, 0], [1, -2, 3]) == F(426, 14) and n2(sub(B_1, A_1)) == 126 and plane3(A_1, [3, -2, 0], [4, -4, 3]) == [19, 8, -1, -41])
ck(F(126) * F(426, 14) / 4 == F(9 * 426, 4))
A_8, B_8, C_8 = [6, 2, -1], [3, 0, 5], [-2, 1, 2]
angs = [deg(cos2(sub(Y, X), sub(Z, X))) for X, Y, Z in ((A_8, B_8, C_8), (B_8, A_8, C_8), (C_8, A_8, B_8))]
ck(all(dot(sub(Y, X), sub(Z, X)) > 0 for X, Y, Z in ((A_8, B_8, C_8), (B_8, A_8, C_8), (C_8, A_8, B_8))) and near(angs[0], 43.05) and near(angs[1], 83.07) and near(angs[2], 53.88) and abs(sum(angs) - 180) < 1e-9)
ck(n2(cross(sub(B_8, A_8), sub(C_8, A_8))) == 1690 and rad(F(1690, 4)) == r'\dfrac{13\sqrt{10}}{2}')
ck(cross([-1, 1, 0], [0, -2, -2]) == [-2, -2, 2] and dot([-1, 1, 0], [0, -2, -2]) == -2 and n2([-2, -2, 2]) == 12)
ck(pdist2([0, 1, 1], [1, 1, 0, -2]) == F(1, 2) and projp([0, 1, 1], [1, 1, 0, -2]) == [F(1, 2), F(3, 2), 1] and n2(cross([2, -1, -1], [0, 1, -1])) == 12)
dN = cross([2, 2, 1], [2, 0, -1]); ck(par_(dN, [1, -2, 2]) and onp([2, 2, 1, 0], [1, -1, 0]) and onp([2, 0, -1, -2], [1, -1, 0]))
FN = projl([4, 5, 0], [1, -1, 0], [1, -2, 2]); ck(FN == [0, 1, -2] and n2(sub([4, 5, 0], FN)) == 36 and sub(FN, [1, -2, 2]) == [-1, 3, -4] and add(FN, [1, -2, 2]) == [1, -1, 0])
pau("Áreas y volúmenes",
 (2, r"\pau{Cantabria, extraordinaria 2026} Considera los puntos $A(0,5,-1)$ y $B(-3,11,-10)$ y la recta $r:\dfrac{x-3}{1}=\dfrac{y+2}{-2}=\dfrac z3$." + tasks(1, [r"Estudia la posición relativa de $r$ y la recta que contiene $A$ y $B$.", r"Calcula el área del triángulo formado por los vértices $A$, $B$ y un punto genérico de $r$.", r"Halla la ecuación general o implícita del plano que contiene $r$ y $A$."]),
     tasks(1, [r"$\overrightarrow{AB}=(-3,6,-9)=-3\,(1,-2,3)$ y $A\notin r$: \ \rest{paralelas}", r"Base $|\overrightarrow{AB}|=3\sqrt{14}$, altura $d(A,r)=\dfrac{\sqrt{426}}{\sqrt{14}}$ (constante): \ $S=\res{\dfrac{3\sqrt{426}}{2}\approx30{,}96}$", r"$\res{19x+8y-z-41=0}$"])),
 (2, r"\pau{Cantabria, ordinaria 2024} Sean $A(6,2,-1)$, $B(3,0,5)$ y $C(-2,1,2)$ los vértices de un triángulo." + tasks(1, [r"Calcula los ángulos internos del triángulo.", r"Calcula el área del triángulo."]),
     tasks(1, [r"Con los vectores que salen de cada vértice: \ $\res{\hat A\approx" + ('%.2f' % angs[0]).replace('.', '{,}') + r"^\circ,\ \hat B\approx" + ('%.2f' % angs[1]).replace('.', '{,}') + r"^\circ,\ \hat C\approx" + ('%.2f' % angs[2]).replace('.', '{,}') + r"^\circ}$",
               r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-3,-2,6)\times(-8,-1,3)$, de módulo $\sqrt{1690}$: \ $S=\res{\dfrac{13\sqrt{10}}{2}}$"])),
 (2, r"\pau{Extremadura, ordinaria 2024} Dados los puntos $A(1,2,1)$, $B(0,3,1)$ y $C(1,0,-1)$, determina:" + tasks(1, [r"un vector unitario y ortogonal a los vectores $\overrightarrow{AB}$ y $\overrightarrow{AC}$;", r"el ángulo determinado por estos vectores;", r"el área del triángulo que forman $A$, $B$ y $C$."]),
     tasks(1, [r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-2,-2,2)$: \ $\res{\left(-\tfrac{1}{\sqrt3},-\tfrac{1}{\sqrt3},\tfrac{1}{\sqrt3}\right)}$ (o el opuesto)", r"$\cos\alpha=\dfrac{-2}{\sqrt2\,\sqrt8}=-\dfrac12$: \ $\res{120^\circ}$", r"$S=\tfrac12\sqrt{12}=\res{\sqrt3}$"])),
 (2, r"\pau{Madrid, ordinaria 2025} Sean el punto $P(0,1,1)$ y el plano $\pi:x+y=2$." + tasks(1, [r"Halla la distancia del punto $P$ al plano $\pi$.", r"Determina el punto $Q$ del plano $\pi$ cuya distancia a $P$ es igual a la distancia de $P$ a $\pi$.", r"Halla el área del triángulo formado por $P$ y los puntos de corte del plano $\pi$ con los ejes de coordenadas."]),
     tasks(1, [r"$\res{\dfrac{\sqrt2}{2}}$", r"Es la proyección: \ $\res{Q\left(\tfrac12,\tfrac32,1\right)}$", r"$\pi$ corta los ejes en $(2,0,0)$ y $(0,2,0)$ (es paralelo a $OZ$): \ $S=\tfrac12|(2,-1,-1)\times(0,1,-1)|=\tfrac12|(2,2,2)|=\res{\sqrt3}$"])),
 (2, r"\pau{Navarra, extraordinaria 2024} El punto $P(4,5,0)$ es el punto medio de un lado de un cuadrado. El lado paralelo al anterior está contenido en la recta $r:" + sy('2x+2y+z=0', '2x-z-2=0') + r"$ \ Calcula los dos vértices que determinan este segundo lado.",
     r"$\vec d=(1,-2,2)$; la proyección de $P$ sobre $r$ es $(0,1,-2)$, el punto medio del segundo lado, y el lado mide $d(P,r)=6$. Los vértices distan 3 de este punto: $(0,1,-2)\pm(1,-2,2)$: \ $\res{(1,-1,0)\ \text{y}\ (-1,3,-4)}$"),
)

# ---------- 9. Llocs geomètrics
ck(F(3, 2) ** 2 - 8 * F(3, 2) + 16 + F(55, 4) == 20 and F(3, 2) ** 2 + 4 + F(55, 4) == 20)
dr10, ds10 = cross([0, 1, 0], [2, 0, -1]), cross([1, 1, 0], [0, 0, 1]); ck(par_(dr10, [1, 0, 2]) and ds10 == [1, -1, 0] and cross([1, 0, 2], [1, -1, 0]) == [2, 2, -1])
ck(pdist2([0, 0, 0], [2, 2, -1, 7]) == pdist2([-7, 0, 0], [2, 2, -1, 7]))
c1y, c2y = [2, -3, 1, -4], [2, -3, 1, 2]                           # π1 (a=4) i π2 (b=-2)
ck(par_(cross([0, 2, 6], [1, 0, -2]), [2, -3, 1]) and onp(c2y, [0, 2, 4]) and [(a + b) / 2 for a, b in zip(c1y, c2y)] == [2, -3, 1, -1])
ck(par_(cross([0, 2, 6], [1, 0, 0]), [0, 3, -1]) and all(onp([2, -3, 1, -1], [F(3, 2), l_, -2 + 3 * l_]) and onp([0, 3, -1, -2], [F(3, 2), l_, -2 + 3 * l_]) for l_ in range(-2, 3)))
ck(plane(cross(sub([3, -3, 6], [1, -1, 2]), [1, 1, 0]), [1, -1, 2]) == [1, -1, -1, 0] and all(onp(med([1, -1, 2], [3, -3, 6]), [2 + l_, -2 + l_, 4]) and onp([1, -1, -1, 0], [2 + l_, -2 + l_, 4]) for l_ in range(-2, 3)))
ck(med([1, 2, 3], [-3, -2, 3]) == [1, 1, 0, 1] and pdist2([1, 2, 3], [1, 1, 0, 1]) == 8 and onp([1, 1, 0, 1], [-7, 6, 3]) and n2(cross([-4, -4, 0], [-8, 4, 0])) == 48 ** 2)
ck(cos2([1, 1, 1], [1, 1, -1]) == F(1, 9) and near(deg(F(1, 9)), 70.53) and pos_rp([1, -1, 0], [2, 1, 3], [1, 1, -1, -3]) == 'paral·lels')
ck(all(pdist2([1 + 2 * t_, -1 + t_, 3 * t_], [1, 1, 1, 3]) == pdist2([1 + 2 * t_, -1 + t_, 3 * t_], [1, 1, -1, -3]) for t_ in (0, -1)))
ck(med([3, 3, 5], [1, -1, 1]) == [1, 2, 2, -10] and all(pdist2([10, 0, 0], [1, 2, 2, k_]) == 36 for k_ in (8, -28)))
ck(med([1, -1, 3], [2, 1, -1]) == [2, 4, -8, 5] and n2(sub([F(7, 3), F(1, 3), F(1, 3)], [1, -1, 3])) + n2(sub([F(7, 3), F(1, 3), F(1, 3)], [2, 1, -1])) + 21 == 34)
ck(all(n2(sub([2 + t_, t_, t_], [1, -1, 3])) + n2(sub([2 + t_, t_, t_], [2, 1, -1])) + 21 == 34 for t_ in (0, F(1, 3))))
ck(med([1, 1, 2], [-1, 0, 3]) == [2, 1, -1, 2] and pdist2([1, 1, 2], [2, 1, -1, 2]) == F(9, 6))
pau("Lugares geométricos",
 (2, r"\pau{Andalucía, extraordinaria 2024} Considera los puntos $A(4,0,0)$ y $B(0,2,0)$. Calcula los puntos del plano $OXZ$ que forman un triángulo equilátero con $A$ y $B$.",
     r"$C(x,0,z)$ con $|\overrightarrow{CA}|^2=|\overrightarrow{CB}|^2=|\overrightarrow{AB}|^2=20$: \ $(x-4)^2+z^2=x^2+4+z^2=20$ \ $\Rightarrow$ \ $x=\tfrac32$, $z^2=\tfrac{55}{4}$: \ $\res{C\left(\tfrac32,0,\pm\tfrac{\sqrt{55}}{2}\right)}$"),
 (2, r"\pau{Andalucía, ordinaria 2024} Considera las rectas $r:" + sy('y=0', '2x-z=0') + r"$ \ y \ $s:" + sy('x+y+7=0', 'z=0') + r"$" + tasks(1, [r"Estudia la posición relativa de $r$ y $s$.", r"Calcula la ecuación del plano paralelo a $r$ y a $s$ que equidista de ambas rectas."]),
     tasks(1, [r"$\vec d_r=(1,0,2)$, $\vec d_s=(1,-1,0)$, $[\overrightarrow{OQ},\vec d_r,\vec d_s]\neq0$ con $Q(-7,0,0)$: \ \rest{se cruzan}", r"$\vec n=\vec d_r\times\vec d_s=(2,2,-1)$; \ $2x+2y-z+k=0$ con $|k|=|k-14|$: \ $\res{2x+2y-z+7=0}$"])),
 (2, r"\pau{Castilla y León, ordinaria 2026} Dados el plano $\pi_1:2x-3y+z=a$ y el plano $\pi_2$ determinado por el punto $P(0,2,4)$ y los vectores directores $\vec v_1=(0,2,6)$ y $\vec v_2=(1,0,b)$:" + tasks(1, [r"Calcula los valores de $a$ y $b$ para que $\pi_1$ y $\pi_2$ sean paralelos y distintos.", r"Para $a=1$ y $b=0$, determina las ecuaciones paramétricas de la recta intersección de $\pi_1$ y $\pi_2$.", r"Para $a=4$ y $b=-2$, determina los puntos que están a igual distancia de $\pi_1$ y $\pi_2$."]),
     tasks(1, [r"$\vec v_1\times\vec v_2=(2b,6,-2)\parallel(2,-3,1)$: $\res{b=-2}$; entonces $\pi_2:2x-3y+z=-2$, y son distintos si $\res{a\neq-2}$", r"$\pi_2:3y-z=2$: \ $\res{x=\tfrac32,\ y=\lambda,\ z=-2+3\lambda}$", r"Planos paralelos $2x-3y+z=4$ y $2x-3y+z=-2$: el plano a media distancia, \ $\res{2x-3y+z-1=0}$"])),
 (2, r"\pau{Cataluña, ordinaria 2025} Considera el plano $\pi:x+y=0$." + tasks(1, [r"Calcula la ecuación del plano $\pi'$ que es perpendicular a $\pi$ y contiene los puntos $P(1,-1,2)$ y $Q(3,-3,6)$.", r"Calcula la ecuación paramétrica de la recta contenida en $\pi'$ que contiene los puntos de $\pi'$ que están a la misma distancia de $P$ que de $Q$."]),
     tasks(1, [r"$\vec n'\parallel\overrightarrow{PQ}\times\vec n=(2,-2,4)\times(1,1,0)$: \ $\res{x-y-z=0}$", r"Es $\pi'\cap$ (plano mediador $x-y+2z=12$): \ $\res{x=2+\lambda,\ y=-2+\lambda,\ z=4}$"])),
 (2, r"\pau{Cataluña, ordinaria 2024} Considera los puntos $A(1,2,3)$ y $B(-3,-2,3)$." + tasks(1, [r"Calcula la ecuación del plano $\pi$ que es perpendicular a la recta $AB$ y que pasa por el punto medio entre $A$ y $B$. Justifica que este plano está formado, precisamente, por los puntos $P$ que están a igual distancia de $A$ que de $B$.", r"Calcula las distancias de $A$ y de $B$ al plano $\pi$ y comprueba que son iguales. ¿Es una casualidad?", r"Sea $C(-7,6,3)$. ¿El triángulo $ABC$ es isósceles? Calcula su área."]),
     tasks(1, [r"$\res{x+y+1=0}$; \ $d(P,A)^2=d(P,B)^2$ se reduce a $8x+8y+8=0$.", r"$d(A,\pi)=d(B,\pi)=\res{2\sqrt2}$: no es casualidad, $B$ es el simétrico de $A$ respecto de $\pi$.", r"$C\in\pi$, por tanto $CA=CB$: \ \rest{isósceles}. \ $S=\tfrac12|(-4,-4,0)\times(-8,4,0)|=\res{24}$"])),
 (2, r"\pau{Murcia, extraordinaria 2024} Considera los planos $x+y+z=-3$ y $x+y-z=3$ y la recta $r:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac z3$." + tasks(1, [r"Comprueba que ambos planos se cortan y calcula el ángulo que forman.", r"Estudia la posición relativa de la recta $r$ con el plano $x+y-z=3$.", r"Determina los puntos de la recta $r$ que equidistan de ambos planos."]),
     tasks(1, [r"$\cos\alpha=\dfrac13$: \ $\res{\alpha\approx70{,}53^\circ}$", r"$\vec d\cdot\vec n=2+1-3=0$ y $(1,-1,0)$ no está en el plano: \ \rest{paralelos}", r"$(1+2t,-1+t,3t)$: $\dfrac{|6t+3|}{\sqrt3}=\dfrac{3}{\sqrt3}$, $t=0$ o $t=-1$: \ $\res{(1,-1,0)\ \text{y}\ (-1,-2,-3)}$"])),
 (2, r"\pau{Navarra, extraordinaria 2025} Calcula la ecuación del plano que equidista de los puntos $A(3,3,5)$ y $B(1,-1,1)$. Calcula la ecuación de los planos que distan 6 unidades del plano anterior.",
     r"Plano mediador: \ $\res{x+2y+2z-10=0}$. \ $x+2y+2z+k=0$ con $\dfrac{|k+10|}{3}=6$: \ $\res{x+2y+2z+8=0}$ \ y \ $\res{x+2y+2z-28=0}$"),
 (2, r"\pau{Madrid, extraordinaria 2024} Sean los puntos $P(1,-1,3)$ y $Q(2,1,-1)$." + tasks(1, [r"Determina una ecuación del plano respecto del cual ambos puntos son simétricos.", r"El segmento $PQ$ es uno de los tres lados de un triángulo en el que la suma de los cuadrados de las longitudes de los lados es 34 y el tercer vértice se encuentra en la recta $r:x-2=y=z$. Calcula las coordenadas del tercer vértice sabiendo que ninguna de sus coordenadas es nula."]),
     tasks(1, [r"Plano mediador: \ $\res{2x+4y-8z+5=0}$", r"$R(2+t,t,t)$: $21+|PR|^2+|QR|^2=34+6t^2-2t=34$, \ $t=0$ (no vale: $R(2,0,0)$) o $t=\tfrac13$: \ $\res{R\left(\tfrac73,\tfrac13,\tfrac13\right)}$"])),
 (2, r"\pau{País Vasco, ordinaria 2026} Sean los puntos $A(1,1,2)$ y $B(-1,0,3)$." + tasks(1, [r"Halla la ecuación del plano $\pi$ que cumple que $A$ y $B$ son simétricos respecto de $\pi$.", r"¿Cuál es la distancia de $A$ a $\pi$?"]),
     tasks(1, [r"$\res{2x+y-z+2=0}$", r"$\dfrac{|2+1-2+2|}{\sqrt6}=\res{\dfrac{\sqrt6}{2}}$"])),
)

# ---------- 10. Problemes
G4 = mul(add([2, 1, 3], [0, -1, 1]), F(1, 2)); ck(G4 == [1, 0, 2] and dot(sub([0, -1, 1], [2, 1, 3]), sub([1, 1, 1], G4)) == 0)
ck(projp([1, 2, 1], [1, 1, 3, 0]) == [F(5, 11), F(16, 11), F(-7, 11)] and pdist2([1, 2, 1], [1, 1, 3, 0]) == F(36, 11))
ck(pos_rr([2, -1, 3], [1, -2, 2], [1, 4, 4], [2, -1, -2]) == "s'encreuen" and feet(P7, d7, Q7, e7)[2:] == ([1, 1, 1], [3, 3, 2]) and skew2(P7, d7, Q7, e7) == 9)
ck(pdist2([1, 2, 1], [2, -2, 1, -1]) == F(4, 9) and projp([1, 2, 1], [2, -2, 1, -1]) == [F(13, 9), F(14, 9), F(11, 9)])
ABa, ACa = [2, 0, F(1, 2)], [F(3, 2), 3, 1]; cra = cross(ABa, ACa); ck(cra == [F(-3, 2), F(-5, 4), 6])
ck(all(dot([3 * l_, 1 + l_, 3], cra) == (67 - 23 * l_) / F(4) for l_ in (0, 1, F(1, 2))) and n2(cra) == F(637, 16))
ck(F(67, 24) == F(16.75) / 6 and (F(11, 6) * 3) ** 2 / (n2(cra) / 4) == F(44 ** 2 * 13, 91 ** 2))
ck(abs(float(F(44, 24) * 3) / (math.sqrt(637) / 8) - 44 * math.sqrt(13) / 91) < 1e-12)
ck(sym(projp([1, 2, 6], [1, 1, 1, -6]), [1, 2, 6]) == [-1, 0, 4] and n2(sub([-1, 0, 4], [1, 2, 6])) == 12)
ck(det3(sub([1, 2, 0], [0, 1, -2]), sub([0, 0, 1], [0, 1, -2]), sub([1, 0, 6], [0, 1, -2])) == 0 and plane3([0, 1, -2], [1, 2, 0], [0, 0, 1]) == [5, -3, -1, 1] and pdist2([1, 2, 3], [5, -3, -1, 1]) == F(9, 35))
nB = cross([2, -1, 3], [-1, 2, 1]); ck(nB == [-7, -5, 3] and n2(nB) == 83 and add([2, -1, 3], [-1, 2, 1]) == [1, 1, 4])
pau("Problemas y cuestiones",
 (2, r"\pau{Asturias, ordinaria 2026} Un móvil se desplaza en línea recta desde el punto $P(2,1,3)$ hacia el punto $Q(0,-1,1)$. Cuando llega a la mitad de la distancia de $P$ a $Q$ hace un giro y se desplaza por la recta que pasa por $H(1,1,1)$." + tasks(1, [r"Calcula las coordenadas del punto en el que hace el giro.", r"Calcula la recta por la que se desplaza el móvil después del giro.", r"Calcula el ángulo de giro del móvil."]),
     tasks(1, [r"Punto medio: \ $\res{G(1,0,2)}$", r"$\overrightarrow{GH}=(0,1,-1)$: \ $\res{x=1,\ y=\lambda,\ z=2-\lambda}$", r"$\overrightarrow{PQ}\cdot\overrightarrow{GH}=(-2,-2,-2)\cdot(0,1,-1)=0$: \ $\res{90^\circ}$"])),
 (2, r"\pau{Murcia, extraordinaria 2025} Un helicóptero situado en el punto $P(1,2,1)$ quiere aterrizar en el plano $\pi:x+y+3z=0$." + tasks(1, [r"Calcula la ecuación en forma continua de la recta de la trayectoria que lo lleve al punto más próximo de $\pi$.", r"Halla este punto.", r"Calcula la distancia que debe recorrer."]),
     tasks(1, [r"$\res{\dfrac{x-1}{1}=\dfrac{y-2}{1}=\dfrac{z-1}{3}}$", r"$6+11t=0$: \ $\res{\left(\tfrac{5}{11},\tfrac{16}{11},-\tfrac{7}{11}\right)}$", r"$d=\dfrac{6}{\sqrt{11}}=\res{\dfrac{6\sqrt{11}}{11}\approx1{,}81}$"])),
 (2, r"\pau{Asturias, ordinaria 2025} Se están construyendo dos puentes rectos en un tramo de autovía, uno para cada carril. Los puentes siguen las ecuaciones $r_1(t)=(2+t,\,-1-2t,\,3+2t)$ y $r_2(s)=(1+2s,\,4-s,\,4-2s)$." + tasks(1, [r"Estudia si los puentes son paralelos, se cortan o se cruzan.", r"La empresa quiere construir un puente de servicio que los una y que sea lo más corto posible. ¿Qué longitud tendrá la vía de servicio? Indica sus puntos inicial y final."]),
     tasks(1, [r"$[\overrightarrow{PQ},\vec d_1,\vec d_2]=27\neq0$: \ \rest{se cruzan}", r"Perpendicular común: \ $\res{E(1,1,1),\ F(3,3,2)}$, \ longitud $|\overrightarrow{EF}|=\res{3}$"])),
 (2, r"\pau{Madrid, extraordinaria 2026} Se consideran el punto $P(1,2,1)$ y el plano de ecuación $2x-2y+z=1$. Se traza un cubo con una cara en el plano y un vértice en el punto $P$." + tasks(1, [r"Determina la longitud del lado del cubo y su volumen.", r"Halla otro vértice del cubo."]),
     tasks(1, [r"Lado $=d(P,\pi)=\dfrac{|2-4+1-1|}{3}=\res{\dfrac23}$; \ volumen $\res{\dfrac{8}{27}}$", r"El vértice de la cara del plano que está debajo de $P$ (la proyección): \ $\res{\left(\tfrac{13}{9},\tfrac{14}{9},\tfrac{11}{9}\right)}$"])),
 (3, r"\pau{Aragón, extraordinaria 2025} Se quiere construir una estructura en forma de tetraedro cuya base tiene como vértices los puntos $A(0,0,0)$, $B\left(2,0,\tfrac12\right)$ y $C\left(\tfrac32,3,1\right)$; el vértice superior, $D$, se encuentra en una viga recta entre los puntos $E(0,1,3)$ y $F(3,2,3)$, es decir, $D=E+\lambda\,\overrightarrow{EF}$ con $\lambda\in[0,1]$." + tasks(1, [r"Calcula el volumen máximo de esta estructura (todos los datos están en metros).", r"Teniendo en cuenta que el volumen de una pirámide es un tercio del área de la base por la altura, calcula la altura de la estructura (desde $D$ hasta la base) si tomamos $\lambda=1$."]),
     tasks(1, [r"$D(3\lambda,1+\lambda,3)$; \ $V=\tfrac16\big|[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}]\big|=\dfrac{67-23\lambda}{24}$, máximo en $\lambda=0$: \ $\res{V=\dfrac{67}{24}\approx2{,}79\ \text{m}^3}$",
               r"$V=\dfrac{11}{6}$, \ $S_{ABC}=\tfrac12\left|\left(-\tfrac32,-\tfrac54,6\right)\right|=\dfrac{7\sqrt{13}}{8}$: \ $h=\dfrac{3V}{S}=\res{\dfrac{44\sqrt{13}}{91}\approx1{,}74\ \text{m}}$"])),
 (2, r"\pau{Castilla-La Mancha, ordinaria 2026} En un parque público se está instalando un sistema de vigilancia mediante sensores de movimiento a ambos lados de un muro recto, representado por el plano $\pi:x+y+z-6=0$. Uno de los sensores está situado en el punto $P(1,2,6)$ y se quiere instalar un segundo sensor en el punto $P'$, simétrico del anterior respecto del plano $\pi$." + tasks(1, [r"Determina razonadamente las coordenadas del punto de instalación del segundo sensor, $P'$.", r"Calcula la distancia entre los dos sensores."]),
     tasks(1, [r"$M(0,1,5)$: \ $\res{P'(-1,0,4)}$", r"$|\overrightarrow{PP'}|=2\,d(P,\pi)=\res{2\sqrt3}$"])),
 (2, r"\pau{Castilla-La Mancha, extraordinaria 2025} Para las fiestas del Corpus de Toledo se instalan toldos en las calles por donde pasa la procesión. En uno de ellos, los operarios colocan los puntos de apoyo $A(0,1,-2)$, $B(1,2,0)$, $C(0,0,1)$ y $D(1,0,m)$, con $m\in\mathbb R$." + tasks(1, [r"Calcula el valor de $m$ para que los cuatro puntos sean coplanarios.", r"Determina la ecuación del plano $\pi$ que contiene el toldo.", r"Si los adornos florales deben estar como mínimo a 1 metro de distancia del toldo y se ha colocado un adorno de flores en el punto $P(1,2,3)$, ¿estará correctamente situado?"]),
     tasks(1, [r"$[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}]=6-m=0$: \ $\res{m=6}$", r"$\res{5x-3y-z+1=0}$", r"$d(P,\pi)=\dfrac{3}{\sqrt{35}}\approx0{,}51<1$: \ \rest{no está bien situado}"])),
 (2, r"\pau{Islas Baleares, ordinaria 2024} Consideramos los puntos $A(0,0,0)$, $B(2,-1,3)$ y $C(-1,2,1)$." + tasks(1, [r"Calcula el punto $D$ tal que $ABDC$ sea un paralelogramo.", r"Calcula uno de los puntos $E$ del espacio de manera que la recta $AE$ sea perpendicular al plano $ABC$ y la distancia entre los puntos $A$ y $E$ sea 1.", r"Escribe la ecuación de uno de los planos paralelos al plano $ABC$ que distan una unidad de este."]),
     tasks(1, [r"$D=B+C-A=\res{(1,1,4)}$", r"$\vec n=\overrightarrow{AB}\times\overrightarrow{AC}=(-7,-5,3)$, $|\vec n|=\sqrt{83}$: \ $\res{E=\pm\tfrac{1}{\sqrt{83}}(-7,-5,3)}$", r"$\res{7x+5y-3z\pm\sqrt{83}=0}$"])),
)

# =====================================================================
print(NCHK[0], 'comprovacions correctes')
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre = pre.replace(r'\usepackage{amsmath,amssymb}', r'\usepackage{amsmath,amssymb}' + '\n' + r'\allowdisplaybreaks')
pre += '\n\\setlength{\\emergencystretch}{3em}  % les fórmules llargues (equacions de rectes, ternes) passen a la línia següent\n'
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU d'altres comunitats
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura
TIT = "Problemas métricos"
KW = "ángulos, distancias, perpendicular común, proyecciones, simétricos, áreas, volúmenes, plano mediador, planos bisectores, esfera, PAU"
# espai fi després de les comes de les ternes de coordenades: (1,-2,3) -> (1,\,-2,\,3)
TRI = re.compile(r'\((-?[\w\\{}.+\-]+),(-?[\w\\{}.+\-]+),(-?[\w\\{}.+\-]+)\)')
# i les equacions amb fraccions (equació contínua…) no es parteixen entre dues línies
INL = re.compile(r'(?<![\\$])\$([^$]+)\$')
def esp(t):
    t = TRI.sub(lambda mm: '(' + r',\,'.join(mm.groups()) + ')', t)
    return INL.sub(lambda mm: r'\mbox{$' + mm.group(1) + '$}' if r'\dfrac' in mm.group(1) and len(mm.group(1)) < 260 and r'\begin' not in mm.group(1) else mm.group(0), t)
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 4: %s' % (t, TIT), capcalera='%s · Unidad 4: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-mii')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-mii') + '{' + ('Soluciones de la ficha · Unidad 4' if sol else 'Ficha de ejercicios · Unidad 4') + r'}{\raggedright ' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Las distancias y los ángulos se dan exactos (con raíces simplificadas) y, cuando hace falta, aproximados con dos cifras decimales. Si una recta o un plano de tu solución se escribe de otra manera, comprueba que es el mismo (un punto común y vectores proporcionales). Puedes comprobar los resultados con el laboratorio métrico de los apuntes interactivos."
             if sol else r"Resuelve los ejercicios en el cuaderno justificando cada paso. Haz un esbozo cuando te ayude a ver la situación y comprueba siempre los resultados (que la proyección está en el plano o en la recta, que el punto medio del segmento $PP'$ es el punto $M$\ldots). Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de otras comunidades autónomas (2024--2026).") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, qq, s in exs:
            n += 1
            lab = re.search(r'\\label\{[^}]*\}', qq)
            if sol:
                head = re.sub(r'(\\pau\{[^}]*\}).*', r'\1', qq, flags=re.S) if qq.startswith('\\pau{') else ''
                s = re.sub(r'\\begin\{tasks\}\([23]\)', r'\\begin{tasks}(1)', s)   # a les solucions, un apartat per línia
                out.append(esp('\\ex{%d} %s%s\n\n' % (st, (lab.group(0) if lab else '') + head, s)))
            else:
                out.append(esp('\\ex{%d} %s\n\n' % (st, qq)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con el laboratorio métrico de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't4-fitxa-solucions-es.tex' if sol else 't4-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
regs = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
print(n, 'ejercicios,', npau, 'de la PAU de', len(regs), 'comunidades:', ', '.join(regs))
