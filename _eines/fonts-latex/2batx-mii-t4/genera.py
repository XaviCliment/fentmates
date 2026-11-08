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
S.append(("Angles entre rectes i plans", [
 (1, r"Calcula l'angle que formen les rectes:" + tasks(1, [r"$r:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z}{-2}$ \ i \ $s:(x,y,z)=(0,1,3)+\lambda\,(4,0,3)$",
     r"$r:" + sy('x+y=1', 'y-z=2') + r"$ \ i \ $s:x=y=z$"]) + recorda(r"$\cos\alpha=\dfrac{|\vec d_r\cdot\vec d_s|}{|\vec d_r|\,|\vec d_s|}$, sempre entre $0^\circ$ i $90^\circ$."),
     tasks(1, [r"$\cos\alpha=\dfrac{|8+0-6|}{3\cdot5}=\dfrac{2}{15}$ \ $\Rightarrow$ \ $\res{\alpha\approx82{,}34^\circ}$",
               r"$\vec d_r=(1,1,0)\times(0,1,-1)=(-1,1,1)$; \ $\cos\alpha=\dfrac{|-1+1+1|}{\sqrt3\cdot\sqrt3}=\dfrac13$ \ $\Rightarrow$ \ $\res{\alpha\approx70{,}53^\circ}$"])),
 (1, r"Calcula l'angle que forma la recta $r:\dfrac{x-2}{1}=\dfrac{y}{-1}=\dfrac{z+1}{2}$ amb cadascun dels plans següents:" + tasks(2, [r"$\pi_1:x+y+z=4$", r"$\pi_2:2x-2y+4z=1$"]),
     tasks(1, [r"$\sin\alpha=\dfrac{|1-1+2|}{\sqrt6\cdot\sqrt3}=\dfrac{2}{\sqrt{18}}=\dfrac{\sqrt2}{3}$ \ $\Rightarrow$ \ $\res{\alpha\approx28{,}13^\circ}$",
               r"$\vec n_2=(2,-2,4)=2\,\vec d$: la recta és perpendicular al pla, \ $\res{\alpha=90^\circ}$"])),
 (1, r"Calcula l'angle que formen els plans:" + tasks(2, [r"$x+y=3$ \ i \ $x+z=1$", r"$2x-y+2z=0$ \ i el pla $OXY$"]),
     tasks(2, [r"$\cos\alpha=\dfrac{1}{\sqrt2\sqrt2}=\dfrac12$: \ $\res{\alpha=60^\circ}$", r"$\vec n_{OXY}=(0,0,1)$: \ $\cos\alpha=\dfrac23$, \ $\res{\alpha\approx48{,}19^\circ}$"])),
 (2, r"Calcula els angles que forma la recta de vector director $(2,-1,2)$ amb cadascun dels eixos de coordenades.",
     r"Amb $\vec i$, $\vec j$, $\vec k$: \ $\cos\alpha=\dfrac23$, \ $\cos\beta=\dfrac13$, \ $\cos\gamma=\dfrac23$ \ $\Rightarrow$ \ $\res{\alpha=\gamma\approx48{,}19^\circ,\ \beta\approx70{,}53^\circ}$ \ (són els cosinus directors: $\cos^2\alpha+\cos^2\beta+\cos^2\gamma=1$)."),
 (2, r"Troba $m$ perquè la recta $(x,y,z)=(1,0,0)+\lambda\,(1,m,1)$ forme un angle de $30^\circ$ amb el pla $z=0$.",
     r"$\sin30^\circ=\dfrac{|1|}{\sqrt{2+m^2}}=\dfrac12$ \ $\Rightarrow$ \ $2+m^2=4$ \ $\Rightarrow$ \ $\res{m=\pm\sqrt2}$"),
 (2, r"Hi ha algun valor de $k$ per al qual els plans $x+ky+z=0$ i $2x-y+kz=3$ siguen perpendiculars? I paral·lels?",
     r"$\vec n_1\cdot\vec n_2=2-k+k=2\neq0$: \ \rest{mai no són perpendiculars}. Per a ser paral·lels caldria $\dfrac12=\dfrac{k}{-1}=\dfrac1k$, és a dir, $k=-\tfrac12$ i $k=2$ alhora: \ \rest{tampoc no poden ser paral·lels}."),
]))

# =====================================================================
# 2. Distància entre punts i d'un punt a un pla
ck(pdist2([2, -1, 3], [3, -6, 2, 1]) == F(19 ** 2, 49) and pdist2([0, 0, 0], [3, 2, 1, -6]) == F(36, 14) and rad(F(36, 14)) == r'\dfrac{3\sqrt{14}}{7}' and n2(sub([3, -1, 5], [1, 2, -1])) == 49)
ck(projp([3, 3, -1], [1, 1, -1, -1]) == [1, 1, 1] and pdist2([3, 3, -1], [1, 1, -1, -1]) == 12)
ck(all(pdist2([0, 0, t_], [2, 1, -2, -1]) == 9 for t_ in (-5, 4)))
ck(all(pdist2([1, a_, 1], [1, 2, 2, -3]) == 4 for a_ in (3, -3)))
S.append(("Distància entre punts i d'un punt a un pla", [
 (1, r"Calcula:" + tasks(1, [r"la distància del punt $P(2,-1,3)$ al pla $3x-6y+2z+1=0$;", r"la distància de l'origen al pla $\dfrac x2+\dfrac y3+\dfrac z6=1$;", r"la distància entre els punts $A(1,2,-1)$ i $B(3,-1,5)$."])
     + recorda(r"$d(P,\pi)=\dfrac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}$"),
     tasks(1, [r"$\dfrac{|6+6+6+1|}{\sqrt{9+36+4}}=\res{\dfrac{19}{7}}$", r"El pla és $3x+2y+z-6=0$: \ $\dfrac{6}{\sqrt{14}}=\res{\dfrac{3\sqrt{14}}{7}}$", r"$|(2,-3,6)|=\sqrt{49}=\res{7}$"])),
 (1, r"Troba la projecció ortogonal del punt $P(3,3,-1)$ sobre el pla $\pi:x+y-z=1$ i comprova que la distància de $P$ a la projecció és $d(P,\pi)$.",
     r"Recta per $P$ perpendicular: $(3+t,\ 3+t,\ -1-t)$; \ en el pla, $7+3t=1$, $t=-2$: \ $\res{Q(1,1,1)}$. \ $|\overrightarrow{PQ}|=|(-2,-2,2)|=2\sqrt3$ \ i \ $d(P,\pi)=\dfrac{6}{\sqrt3}=2\sqrt3$ \ \checkmark"),
 (2, r"Troba els punts de l'eix $OZ$ que disten 3 unitats del pla $2x+y-2z=1$.",
     r"$(0,0,t)$: \ $\dfrac{|-2t-1|}{3}=3$ \ $\Rightarrow$ \ $-2t-1=\pm9$: \ $\res{(0,0,-5)\ \text{i}\ (0,0,4)}$"),
 (2, r"Troba $a$ perquè el punt $P(1,a,1)$ diste 2 unitats del pla $x+2y+2z-3=0$.",
     r"$\dfrac{|1+2a+2-3|}{3}=\dfrac{|2a|}{3}=2$ \ $\Rightarrow$ \ $\res{a=\pm3}$"),
]))

# =====================================================================
# 3. Distància d'un punt a una recta
ck(ldist2([1, 2, 3], [0, 0, 0], [1, 1, 1]) == 2 and cross([1, 2, 3], [1, 1, 1]) == [-1, 2, -1])
d3b = cross([1, -1, 0], [0, 0, 1]); ck(d3b == [-1, -1, 0] and ldist2([0, 1, -1], [0, 0, 2], [1, 1, 0]) == F(19, 2) and rad(F(19, 2)) == r'\dfrac{\sqrt{38}}{2}')
ck(projl([3, 1, 4], [1, 0, 1], [1, 1, 1]) == [3, 2, 3] and ldist2([3, 1, 4], [1, 0, 1], [1, 1, 1]) == 2)
ck(add([1, 1, 0], [2, 1, 2]) == [3, 2, 2] and sub([1, 1, 0], [2, 1, 2]) == [-1, 0, -2] and n2([2, 1, 2]) == 9)
ck(ldist2([1, 1, 1], [1, 0, 0], [-1, 1, 0]) == F(3, 2))
S.append(("Distància d'un punt a una recta", [
 (1, r"Calcula la distància:" + tasks(1, [r"del punt $P(1,2,3)$ a la recta $x=y=z$;", r"del punt $P(0,1,-1)$ a la recta $r:" + sy('x-y=0', 'z=2') + r"$"])
     + recorda(r"$d(P,r)=\dfrac{|\overrightarrow{AP}\times\vec d|}{|\vec d|}$, amb $A\in r$ i $\vec d$ un vector director de $r$."),
     tasks(1, [r"$A=O$, $\vec d=(1,1,1)$: \ $\overrightarrow{OP}\times\vec d=(-1,2,-1)$, \ $d=\dfrac{\sqrt6}{\sqrt3}=\res{\sqrt2}$",
               r"$\vec d=(1,1,0)$, $A(0,0,2)$: \ $\overrightarrow{AP}\times\vec d=(3,-3,-1)$, \ $d=\dfrac{\sqrt{19}}{\sqrt2}=\res{\dfrac{\sqrt{38}}{2}}$"])),
 (2, r"Troba el punt $Q$ de la recta $r:(x,y,z)=(1,0,1)+\lambda\,(1,1,1)$ més pròxim a $P(3,1,4)$, la distància de $P$ a $r$ i la recta que passa per $P$ i talla perpendicularment $r$.",
     r"$\overrightarrow{QP}\cdot\vec d=0$: \ $(2-\lambda)+(1-\lambda)+(3-\lambda)=0$, $\lambda=2$: \ $\res{Q(3,2,3)}$. \ $d(P,r)=|\overrightarrow{QP}|=|(0,-1,1)|=\res{\sqrt2}$. \ Recta: \ $\res{(x,y,z)=(3,1,4)+\mu\,(0,1,-1)}$"),
 (2, r"Troba els punts de la recta $r:(x,y,z)=(1,1,0)+\lambda\,(2,1,2)$ que estan a 3 unitats del punt $A(1,1,0)$.",
     r"$d=|\lambda|\cdot|(2,1,2)|=3|\lambda|=3$ \ $\Rightarrow$ \ $\lambda=\pm1$: \ $\res{(3,2,2)\ \text{i}\ (-1,0,-2)}$"),
 (2, r"Calcula l'altura del triangle de vèrtexs $A(1,0,0)$, $B(0,1,0)$ i $C(1,1,1)$ corresponent al costat $AB$.",
     r"És $d(C,r_{AB})$: \ $\overrightarrow{AB}=(-1,1,0)$, \ $\overrightarrow{AC}\times\overrightarrow{AB}=(-1,-1,1)$ \ $\Rightarrow$ \ $h=\dfrac{\sqrt3}{\sqrt2}=\res{\dfrac{\sqrt6}{2}}$"),
]))

# =====================================================================
# 4. Distància entre dues rectes
ck(pos_rr([1, 1, 0], [1, -1, 1], [2, 0, 3], [-1, 1, -1]) == 'paral·leles' and ldist2([2, 0, 3], [1, 1, 0], [1, -1, 1]) == F(8, 3) and rad(F(8, 3)) == r'\dfrac{2\sqrt{6}}{3}')
ck(pos_rr([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 1]) == "s'encreuen" and skew2([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 1]) == F(1, 3))
la4, mu4, X4, Y4 = feet([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 1]); ck(X4 == [F(2, 3), F(2, 3), 0] and Y4 == [1, F(1, 3), F(1, 3)])
ck(all(skew2([0, 0, 0], [1, 0, 0], [0, 1, a_], [1, 1, 0]) == a_ * a_ for a_ in (-2, 2, 3)))
S.append(("Distància entre dues rectes", [
 (1, r"Comprova que les rectes $r:(x,y,z)=(1,1,0)+\lambda\,(1,-1,1)$ i $s:(x,y,z)=(2,0,3)+\mu\,(-1,1,-1)$ són paral·leles i calcula la distància entre elles.",
     r"Directors oposats i $(2,0,3)\notin r$ ($\overrightarrow{PQ}=(1,-1,3)$ no és proporcional a $(1,-1,1)$). \ $\overrightarrow{PQ}\times\vec d_r=(2,2,0)$ \ $\Rightarrow$ \ $d=\dfrac{\sqrt8}{\sqrt3}=\res{\dfrac{2\sqrt6}{3}}$"),
 (2, r"\label{ex:pc}Comprova que les rectes $r:" + sy('x-y=0', 'z=0') + r"$ \ i \ $s:" + sy('x=1', 'y-z=0') + r"$ \ s'encreuen i calcula la distància entre elles."
     + recorda(r"Si s'encreuen, $d(r,s)=\dfrac{\big|[\overrightarrow{PQ},\vec d_r,\vec d_s]\big|}{|\vec d_r\times\vec d_s|}$."),
     r"$r$: $O$, $(1,1,0)$; \ $s$: $(1,0,0)$, $(0,1,1)$. \ $\vec d_r\times\vec d_s=(1,-1,1)$, \ $[\overrightarrow{PQ},\vec d_r,\vec d_s]=1\neq0$: s'encreuen; \ $d=\dfrac{1}{\sqrt3}=\res{\dfrac{\sqrt3}{3}}$"),
 (2, r"Troba $a$ perquè la distància entre l'eix $OX$ i la recta $s:(x,y,z)=(0,1,a)+\mu\,(1,1,0)$ siga 2.",
     r"$\vec d_r\times\vec d_s=(1,0,0)\times(1,1,0)=(0,0,1)$, \ $[\overrightarrow{OQ},\vec d_r,\vec d_s]=(0,1,a)\cdot(0,0,1)=a$: \ $d=|a|=2$ \ $\Rightarrow$ \ $\res{a=\pm2}$"),
]))

# =====================================================================
# 5. Distància entre recta i pla i entre dos plans
ck(pos_rp([2, 0, 1], [3, -1, 1], [1, 2, -1, 4]) == 'paral·lels' and pdist2([2, 0, 1], [1, 2, -1, 4]) == F(25, 6) and rad(F(25, 6)) == r'\dfrac{5\sqrt{6}}{6}')
ck(pdist2([0, 0, F(5, 12)], [3, -4, 12, 8]) == 1 and onp([3, -4, 12, -5], [0, 0, F(5, 12)]))
ck(all(pdist2([0, 0, 0], [2, 1, -2, k_]) == 9 for k_ in (9, -9)))
ck(dot([2, 1, 2], [1, 2, -2]) == 0 and pdist2([1, 1, 1], [1, 2, -2, 0]) == F(1, 9))
S.append(("Distància entre recta i pla i entre dos plans", [
 (1, r"Comprova que la recta $r:x=2+3\lambda,\ y=-\lambda,\ z=1+\lambda$ és paral·lela al pla $\pi:x+2y-z+4=0$ i calcula la distància entre ells.",
     r"$\vec d\cdot\vec n=3-2-1=0$ i $P(2,0,1)\notin\pi$: paral·lels. \ $d(r,\pi)=d(P,\pi)=\dfrac{|2-1+4|}{\sqrt6}=\res{\dfrac{5\sqrt6}{6}}$"),
 (1, r"Calcula la distància entre els plans $3x-4y+12z=5$ i $6x-8y+24z+16=0$.",
     r"El segon és $3x-4y+12z+8=0$: \ $d=\dfrac{|-5-8|}{\sqrt{9+16+144}}=\dfrac{13}{13}=\res{1}$"),
 (2, r"Troba els plans paral·lels a $2x+y-2z+1=0$ que disten 3 unitats de l'origen.",
     r"$2x+y-2z+k=0$ amb $\dfrac{|k|}{3}=3$: \ $\res{2x+y-2z+9=0\ \text{i}\ 2x+y-2z-9=0}$"),
 (2, r"Troba $m$ perquè la recta $(x,y,z)=(1,1,1)+\lambda\,(m,1,2)$ siga paral·lela al pla $x+2y-2z=0$ i calcula aleshores la distància entre la recta i el pla.",
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
S.append(("Recta que passa per un punt i talla dues rectes", [
 (1, r"Troba la recta que passa pel punt $P(2,1,1)$ i talla les rectes $r:" + sy('x=0', 'y=0') + r"$ \ i \ $s:" + sy('x=1', 'z=0') + r"$ \ Calcula també els punts de tall."
     + recorda(r"$t=\pi_1\cap\pi_2$, on $\pi_1$ és el pla que conté $P$ i $r$, i $\pi_2$, el que conté $P$ i $s$. Comprova que $t$ no és paral·lela a $r$ ni a $s$."),
     r"$\pi_1$ ($P$ i l'eix $OZ$): $x-2y=0$; \ $\pi_2$ ($P$ i $s$): $x-z-1=0$. \ $\res{t:" + sy('x-2y=0', 'x-z-1=0') + r"}$, \ director $(2,1,2)$. \ Talla $r$ en $\res{(0,0,-1)}$ i $s$ en $\res{\left(1,\tfrac12,0\right)}$"),
 (2, r"Troba la recta paral·lela al vector $\vec v=(1,0,1)$ que talla les rectes $r$ i $s$ de l'exercici anterior.",
     r"$\pi_1$ conté $r$ i $\vec v$: $y=0$; \ $\pi_2$ conté $s$ i $\vec v$: $x-z-1=0$. \ $\res{t:" + sy('y=0', 'x-z-1=0') + r"}$, \ és a dir, $(x,y,z)=(0,0,-1)+k\,(1,0,1)$, que talla $r$ en $(0,0,-1)$ i $s$ en $(1,0,0)$."),
 (2, r"Troba la recta continguda en el pla $\pi:x+y+z=3$ que passa pel punt $P(1,1,1)$ i talla la recta $r:(x,y,z)=\lambda\,(1,2,0)$.",
     r"$r\cap\pi$: $3\lambda=3$, $X(1,2,0)$. La recta és $PX$: \ $\res{(x,y,z)=(1,1,1)+k\,(0,1,-1)}$ \ (està en $\pi$: $P\in\pi$ i $(0,1,-1)\perp(1,1,1)$)."),
 (2, r"Raona que no hi ha cap recta que passe per l'origen i talle les rectes $r:(x,y,z)=(1,0,0)+\lambda\,(0,1,0)$ i $s:(x,y,z)=(0,0,1)+\mu\,(1,0,0)$.",
     r"$\pi_1$ ($O$ i $r$): $z=0$; \ $\pi_2$ ($O$ i $s$): $y=0$. La seua intersecció és l'eix $OX$, que talla $r$ en $(1,0,0)$ però \rest{és paral·lela a $s$} (i no la conté): no hi ha solució."),
]))

# =====================================================================
# 7. Perpendicular comuna
def comperp(P, d, Q, e):                                                  # plans (r, w) i (s, w), peus i distància²
    w = prim(cross(d, e)); pr, ps = plane(cross(d, w), P), plane(cross(e, w), Q)
    la, mu, X, Y = feet(P, d, Q, e); assert onp(pr, X) and onp(ps, X) and onp(pr, Y) and onp(ps, Y)
    return w, pr, ps, X, Y, n2(sub(Y, X))
c7a = comperp([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 1]); ck(c7a[0] == [1, -1, 1] and c7a[3] == [F(2, 3), F(2, 3), 0] and c7a[4] == [1, F(1, 3), F(1, 3)] and c7a[5] == F(1, 3))
c7b = comperp([1, 0, 0], [1, 1, 0], [0, 0, 1], [1, -1, 0]); ck(c7b[0] == [0, 0, 1] and c7b[1] == [1, -1, 0, -1] and c7b[2] == [1, 1, 0, 0] and c7b[3] == [F(1, 2), F(-1, 2), 0] and c7b[4] == [F(1, 2), F(-1, 2), 1] and c7b[5] == 1)
S.append(("Perpendicular comuna", [
 (2, r"Troba els punts $X\in r$ i $Y\in s$ més pròxims de les rectes $r:" + sy('x-y=0', 'z=0') + r"$ \ i \ $s:" + sy('x=1', 'y-z=0') + r"$ \ de l'exercici \ref{ex:pc} i la seua perpendicular comuna. Comprova que $|\overrightarrow{XY}|=d(r,s)$."
     + recorda(r"Amb els punts genèrics $X\in r$, $Y\in s$, imposa $\overrightarrow{XY}\perp\vec d_r$ i $\overrightarrow{XY}\perp\vec d_s$."),
     r"$X(\lambda,\lambda,0)$, $Y(1,\mu,\mu)$: \ $1-2\lambda+\mu=0$, \ $2\mu-\lambda=0$ \ $\Rightarrow$ \ $\lambda=\tfrac23$, $\mu=\tfrac13$: \ $\res{X\left(\tfrac23,\tfrac23,0\right),\ Y\left(1,\tfrac13,\tfrac13\right)}$; \ perpendicular comuna: \ $\res{(x,y,z)=\left(\tfrac23,\tfrac23,0\right)+t\,(1,-1,1)}$. \ $|\overrightarrow{XY}|=\left|\left(\tfrac13,-\tfrac13,\tfrac13\right)\right|=\tfrac{\sqrt3}{3}$ \ \checkmark"),
 (2, r"Siguen $r:(x,y,z)=(1,0,0)+\lambda\,(1,1,0)$ i $s:(x,y,z)=(0,0,1)+\mu\,(1,-1,0)$. Troba la perpendicular comuna pel mètode dels plans i comprova el resultat amb els punts genèrics. Quina és la distància entre $r$ i $s$?"
     + recorda(r"$\vec w=\vec d_r\times\vec d_s$; \ $\pi_r$ conté $r$ i $\vec w$; \ $\pi_s$ conté $s$ i $\vec w$; \ la perpendicular comuna és $\pi_r\cap\pi_s$."),
     r"$\vec w\parallel(0,0,1)$; \ $\pi_r:x-y-1=0$, \ $\pi_s:x+y=0$: \ $\res{t:" + sy('x-y-1=0', 'x+y=0') + r"}$, \ és a dir, $x=\tfrac12$, $y=-\tfrac12$. \ Punts genèrics: $\lambda=-\tfrac12$, $\mu=\tfrac12$, \ $X\left(\tfrac12,-\tfrac12,0\right)$, $Y\left(\tfrac12,-\tfrac12,1\right)$; \ $d=|\overrightarrow{XY}|=\res{1}$"),
]))

# =====================================================================
# 6. Simètrics respecte d'un punt i d'una recta
ck(sym([0, 1, -1], [1, -2, 3]) == [-1, 4, -5] and mul(add([1, -2, 3], [5, 0, 1]), F(1, 2)) == [3, -1, 2])
M6 = projl([2, 1, 0], [0, 0, 1], [1, 0, 1]); ck(M6 == [F(1, 2), 0, F(3, 2)] and sym(M6, [2, 1, 0]) == [-1, -1, 3])
ck(sym(projl([1, 2, 3], [0, 0, 0], [1, 0, 0]), [1, 2, 3]) == [1, -2, -3])
d6 = cross([1, 1, 0], [0, 0, 1]); ck(d6 == [1, -1, 0] and projl([0, 0, 1], [1, 1, 0], d6) == [1, 1, 0] and sym([1, 1, 0], [0, 0, 1]) == [2, 2, -1])
S.append(("Simètrics respecte d'un punt i d'una recta", [
 (1, r"Calcula el simètric de $A(1,-2,3)$ respecte del punt $B(0,1,-1)$. Troba també el punt $M$ respecte del qual $A$ i $A'(5,0,1)$ són simètrics.",
     r"$A'=2B-A=\res{(-1,4,-5)}$. \qquad $M$ és el punt mig: \ $M=\dfrac{A+A'}{2}=\res{(3,-1,2)}$"),
 (2, r"Calcula el simètric del punt $P(2,1,0)$ respecte de la recta $r:(x,y,z)=(0,0,1)+\lambda\,(1,0,1)$."
     + recorda(r"Pla per $P$ perpendicular a $r$ $\to$ $M=r\cap\pi$ $\to$ $P'=2M-P$."),
     r"Pla: $x+z=2$; \ tall: $\lambda+1+\lambda=2$, $\lambda=\tfrac12$, \ $M\left(\tfrac12,0,\tfrac32\right)$; \ $P'=2M-P=\res{(-1,-1,3)}$"),
 (2, r"Calcula el simètric de:" + tasks(1, [r"$P(1,2,3)$ respecte de l'eix $OX$;", r"$P(0,0,1)$ respecte de la recta $r:" + sy('x+y=2', 'z=0') + r"$"]),
     tasks(1, [r"$M(1,0,0)$: \ $\res{P'(1,-2,-3)}$", r"$\vec d=(1,-1,0)$, $A(1,1,0)$; \ $\overrightarrow{AP}\cdot\vec d=0$, de manera que $M=A=(1,1,0)$: \ $\res{P'(2,2,-1)}$"])),
]))

# =====================================================================
# 7. Simètrics respecte d'un pla
ck(projp([3, 1, 2], [2, -1, 1, -1]) == [1, 2, 1] and sym([1, 2, 1], [3, 1, 2]) == [-1, 3, 0])
ck(sym(projp([1, 2, 3], [0, 0, 1, 0]), [1, 2, 3]) == [1, 2, -3] and sym(projp([1, 2, 3], [1, -1, 0, 0]), [1, 2, 3]) == [2, 1, 3])
ck(med([1, 2, -1], [3, 0, 1]) == [1, -1, 1, -1])
t7, X7 = meet_lp([1, 1, 1], [1, 2, 0], [1, 1, 1, 0]); ck(t7 == -1 and X7 == [0, -1, 1])
ck(projp([1, 1, 1], [1, 1, 1, 0]) == [0, 0, 0] and sub([-1, -1, -1], X7) == [-1, 0, -2])
ck(pos_rp([2, 0, 0], [0, 1, -1], [0, 1, 1, -4]) == 'paral·lels' and projp([2, 0, 0], [0, 1, 1, -4]) == [2, 2, 2] and sym([2, 2, 2], [2, 0, 0]) == [2, 4, 4])
S.append(("Simètrics respecte d'un pla", [
 (1, r"Calcula el simètric del punt $P(3,1,2)$ respecte del pla $\pi:2x-y+z-1=0$."
     + recorda(r"Recta per $P$ amb director $\vec n$ $\to$ $M=s\cap\pi$ (la projecció) $\to$ $P'=2M-P$."),
     r"$(3+2t,\ 1-t,\ 2+t)$: \ $6+6t=0$, $t=-1$, \ $M(1,2,1)$; \ $P'=\res{(-1,3,0)}$"),
 (1, r"Calcula els simètrics del punt $A(1,2,3)$ respecte dels plans $z=0$ i $x=y$.",
     tasks(2, [r"$\res{(1,2,-3)}$", r"$x-y=0$: \ $M\left(\tfrac32,\tfrac32,3\right)$, \ $\res{(2,1,3)}$"])),
 (2, r"Troba el pla respecte del qual són simètrics els punts $P(1,2,-1)$ i $P'(3,0,1)$.",
     r"És perpendicular a $\overrightarrow{PP'}=(2,-2,2)$ i passa pel punt mig $(2,1,0)$: \ $\res{x-y+z-1=0}$"),
 (3, r"Siguen $r:(x,y,z)=(1,1,1)+\lambda\,(1,2,0)$ i $\pi:x+y+z=0$." + tasks(1, [r"Calcula la recta simètrica de $r$ respecte de $\pi$.", r"Calcula la projecció ortogonal de $r$ sobre $\pi$."]),
     tasks(1, [r"Tall: $3+3\lambda=0$, \ $X(0,-1,1)$. \ Simètric de $A(1,1,1)$: $M=O$, $A'(-1,-1,-1)$. \ $r':\ \res{(x,y,z)=(0,-1,1)+\mu\,(1,0,2)}$",
               r"És la recta que passa per $X$ i per la projecció $M=O$ de $A$: \ $\res{(x,y,z)=\mu\,(0,-1,1)}$"])),
 (2, r"Calcula la recta simètrica de $r:(x,y,z)=(2,0,0)+\lambda\,(0,1,-1)$ respecte del pla $y+z=4$.",
     r"$\vec d\cdot\vec n=0$ i $(2,0,0)\notin\pi$: paral·lels. \ Simètric de $A(2,0,0)$: $M(2,2,2)$, $A'(2,4,4)$. \ $r':\ \res{(x,y,z)=(2,4,4)+\mu\,(0,1,-1)}$"),
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
S.append(("Àrees i volums", [
 (1, r"Considera el triangle de vèrtexs $A(1,2,0)$, $B(3,0,1)$ i $C(0,1,2)$." + tasks(1, [r"Calcula'n l'àrea.", r"Calcula l'angle del vèrtex $A$.", r"Calcula l'altura corresponent al costat $AB$."])
     + recorda(r"$S=\tfrac12|\overrightarrow{AB}\times\overrightarrow{AC}|$. Per a l'angle d'un triangle no posem valor absolut al producte escalar."),
     tasks(1, [r"$\overrightarrow{AB}\times\overrightarrow{AC}=(2,-2,1)\times(-1,-1,2)=(-3,-5,-4)$: \ $S=\dfrac{\sqrt{50}}{2}=\res{\dfrac{5\sqrt2}{2}}$",
               r"$\cos\hat A=\dfrac{-2+2+2}{3\sqrt6}=\dfrac{\sqrt6}{9}$ \ $\Rightarrow$ \ $\res{\hat A\approx74{,}21^\circ}$", r"$h=\dfrac{2S}{|\overrightarrow{AB}|}=\res{\dfrac{5\sqrt2}{3}}$"])),
 (2, r"Calcula el volum del tetraedre de vèrtexs $A(1,0,0)$, $B(0,1,0)$, $C(0,0,1)$ i $D(2,2,2)$, i la seua altura des de $D$.",
     r"$[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}]=" + vm([[-1, 1, 0], [-1, 0, 1], [1, 2, 2]]) + r"=5$: \ $\res{V=\tfrac56}$. \ Pla $ABC$: $x+y+z-1=0$; \ $h=d(D,\pi)=\dfrac{5}{\sqrt3}=\res{\dfrac{5\sqrt3}{3}}$"),
 (2, r"Troba $a$ perquè el tetraedre de vèrtexs $O$, $(1,0,0)$, $(0,1,0)$ i $(1,1,a)$ tinga volum 2.",
     r"$V=\tfrac16" + vm([[1, 0, 0], [0, 1, 0], [1, 1, 'a']]) + r"=\dfrac{|a|}{6}=2$ \ $\Rightarrow$ \ $\res{a=\pm12}$"),
 (2, r"Tres vèrtexs consecutius d'un paral·lelogram $ABCD$ són $A(1,0,1)$, $B(2,1,0)$ i $C(4,2,1)$. Troba el quart vèrtex i l'àrea del paral·lelogram.",
     r"$D=A+C-B=\res{(3,1,2)}$. \ $S=|\overrightarrow{AB}\times\overrightarrow{AD}|=|(1,1,-1)\times(2,1,1)|=|(2,-3,-1)|=\res{\sqrt{14}}$"),
 (2, r"El pla $\pi:2x+3y+6z=12$ talla els eixos en $A$, $B$ i $C$. Calcula el volum del tetraedre $OABC$, la distància de l'origen a $\pi$ i, amb aquestes dues dades, l'àrea del triangle $ABC$.",
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
S.append(("Llocs geomètrics", [
 (1, r"Troba el pla mediador del segment d'extrems $A(2,1,-1)$ i $B(0,3,1)$ de dues maneres: imposant $d(X,A)=d(X,B)$ i amb el punt mig i el vector $\overrightarrow{AB}$.",
     r"$(x-2)^2+(y-1)^2+(z+1)^2=x^2+(y-3)^2+(z-1)^2$ \ $\Rightarrow$ \ $-4x+4y+4z-4=0$. \ O bé: $\overrightarrow{AB}=(-2,2,2)$, $M(1,2,0)$. \ $\res{x-y-z+1=0}$"),
 (2, r"Troba els plans bisectors dels plans $\pi_1:x+y-z=1$ i $\pi_2:x-y+z=3$."
     + recorda(r"Són els punts que equidisten dels dos plans: $\dfrac{|A_1x+B_1y+C_1z+D_1|}{|\vec n_1|}=\dfrac{|A_2x+B_2y+C_2z+D_2|}{|\vec n_2|}$."),
     r"$|\vec n_1|=|\vec n_2|=\sqrt3$: \ $x+y-z-1=\pm(x-y+z-3)$: \ $\res{y-z+1=0}$ \ i \ $\res{x=2}$ \ (perpendiculars entre si)."),
 (1, r"Troba el lloc geomètric dels punts que equidisten dels plans $2x-y+2z=1$ i $2x-y+2z=7$.",
     r"$|2x-y+2z-1|=|2x-y+2z-7|$: el signe $+$ és impossible i el $-$ dona \ $\res{2x-y+2z=4}$, el pla paral·lel situat a mitja distància."),
 (2, r"Escriu l'equació de l'esfera de centre $C(1,0,-2)$ que passa pel punt $P(3,2,-1)$ i la del pla tangent a l'esfera en $P$.",
     r"$R=|\overrightarrow{CP}|=|(2,2,1)|=3$: \ $\res{(x-1)^2+y^2+(z+2)^2=9}$. \ El pla tangent és perpendicular al radi $\overrightarrow{CP}$: \ $\res{2x+2y+z-9=0}$"),
 (2, r"Troba l'esfera de centre $C(2,-1,1)$ tangent al pla $x+2y+2z+7=0$ i el punt de tangència.",
     r"$R=d(C,\pi)=\dfrac{|2-2+2+7|}{3}=3$: \ $\res{(x-2)^2+(y+1)^2+(z-1)^2=9}$. \ Punt de tangència = projecció de $C$: \ $\res{(1,-3,-1)}$"),
 (3, r"Troba el lloc geomètric dels punts de l'espai que equidisten de $A(1,0,0)$, $B(0,1,0)$ i $C(0,0,1)$.",
     r"Ha d'estar en el pla mediador de $AB$ ($x=y$) i en el de $BC$ ($y=z$): \ és la recta \ $\res{x=y=z}$, perpendicular al pla $ABC$ pel seu circumcentre."),
]))

# =====================================================================
# 10. Problemes i qüestions
ck(meet_lp([1, 2, 5], [1, 0, -1], [0, 0, 1, 0]) == (5, [6, 2, 0]) and sym(projp([1, 2, 5], [0, 0, 1, 0]), [1, 2, 5]) == [1, 2, -5] and sub([6, 2, 0], [1, 2, -5]) == [5, 0, 5])
B10 = sym(projp([4, 5, 1], [0, 0, 1, 0]), [4, 5, 1]); ck(B10 == [4, 5, -1])
t10, X10 = meet_lp([1, 1, 2], sub(B10, [1, 1, 2]), [0, 0, 1, 0]); ck(t10 == F(2, 3) and X10 == [3, F(11, 3), 0] and n2(sub(B10, [1, 1, 2])) == 34)
S.append(("Problemes i qüestions", [
 (2, r"Un raig de llum ix del punt $P(1,2,5)$ en la direcció del vector $(1,0,-1)$, es reflecteix en un espill situat en el pla $z=0$ i continua. Troba el punt on toca l'espill i l'equació del raig reflectit."
     + recorda(r"El raig reflectit és la recta que passa pel punt d'incidència i pel simètric de $P$ respecte de l'espill."),
     r"$(1+t,\ 2,\ 5-t)$ amb $z=0$: \ $t=5$, \ $\res{X(6,2,0)}$. \ $P'(1,2,-5)$, \ $\overrightarrow{P'X}=(5,0,5)$: \ raig reflectit \ $\res{(x,y,z)=(6,2,0)+\mu\,(1,0,1)},\ \mu\ge0$"),
 (3, r"Siguen $A(1,1,2)$ i $B(4,5,1)$, tots dos per damunt del pla $z=0$. Troba el punt $X$ del pla $z=0$ que fa mínima la suma $d(A,X)+d(X,B)$ i el valor d'aquesta suma mínima.",
     r"Si $B'(4,5,-1)$ és el simètric de $B$, $d(X,B)=d(X,B')$ i el camí més curt és el segment $AB'$. \ $A+t\,(3,4,-3)$ amb $z=0$: $t=\tfrac23$: \ $\res{X\left(3,\tfrac{11}{3},0\right)}$; \ suma mínima \ $|\overrightarrow{AB'}|=\res{\sqrt{34}}$"),
 (2, r"Raona si són certes o falses les afirmacions següents:" + tasks(1, [r"Dos plans perpendiculars a un mateix pla són sempre paral·lels entre si.", r"Si una recta és perpendicular a un pla, és perpendicular a totes les rectes contingudes en el pla.",
     r"La distància entre dues rectes que s'encreuen pot ser 0.", r"Si $d(P,\pi)=0$, el punt $P$ és del pla $\pi$."]),
     tasks(1, [r"\rest{Falsa}: per exemple, $x=0$ i $y=0$ són perpendiculars a $z=0$ i es tallen.", r"\rest{Certa}: el seu director és proporcional a $\vec n$, que és perpendicular a qualsevol vector del pla (també si la recta del pla no passa pel punt de tall: s'encreuen perpendicularment).",
               r"\rest{Falsa}: si s'encreuen no tenen cap punt comú i $[\overrightarrow{PQ},\vec d_r,\vec d_s]\neq0$, per tant $d>0$.", r"\rest{Certa}: $|Ax_0+By_0+Cz_0+D|=0$ vol dir que $P$ compleix l'equació del pla."])),
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
pau("Angles entre rectes i plans",
 (2, r"\pau{Canàries, extraordinària 2026} Se sap que el pla $\pi:x+3y+2z=10$ i la recta $r:\dfrac{x+21}{11}=3-y=\dfrac{5-z}{2}$ són secants." + tasks(1, [r"Troba el punt de tall del pla $\pi$ i la recta $r$.", r"Calcula l'angle que formen el pla $\pi$ i la recta $r$."]),
     tasks(1, [r"$r:(-21+11t,\ 3-t,\ 5-2t)$; \ en $\pi$: $4t-2=10$, $t=3$: \ $\res{Q(12,0,-1)}$", r"$\vec d=(11,-1,-2)$, $\vec n=(1,3,2)$: \ $\sin\alpha=\dfrac{|11-3-4|}{\sqrt{126}\,\sqrt{14}}=\dfrac{4}{42}=\dfrac{2}{21}$ \ $\Rightarrow$ \ $\res{\alpha\approx5{,}47^\circ}$"])),
 (2, r"\pau{Castella-la Manxa, ordinària 2024} Siguen els vectors $\vec u=(1,a,a)$ i $\vec v=(-1,0,2)$, amb $a\in\mathbb R$. Determina el valor de $a$ perquè l'angle entre els vectors $\vec u$ i $\vec v$ siga de $60^\circ$.",
     r"$\vec u\cdot\vec v=2a-1=|\vec u|\,|\vec v|\cos60^\circ=\tfrac12\sqrt{1+2a^2}\,\sqrt5$. \ Cal $2a-1>0$; elevant al quadrat: $6a^2-16a-1=0$, \ $a=\dfrac{8\pm\sqrt{70}}{6}$. \ Només serveix \ $\res{a=\dfrac{8+\sqrt{70}}{6}\approx2{,}73}$ \ (l'altra dona $120^\circ$)."),
 (2, r"\pau{País Basc, extraordinària 2025} Siguen $\pi$ el pla que passa pels punts $A(2,3,4)$, $B(3,-1,-2)$, $C(5,-1,2)$ i $r$ la recta que passa pels punts $D(6,-5,-4)$, $E(7,1,4)$." + tasks(1, [r"Calcula l'angle entre el pla $\pi$ i la recta $r$, expressant el resultat en graus, minuts i segons.", r"En cas que $r$ i $\pi$ es tallen, calcula el punt d'intersecció. En cas contrari, calcula la distància entre la recta $r$ i el pla $\pi$."]),
     tasks(1, [r"$\vec n\parallel\overrightarrow{AB}\times\overrightarrow{AC}=(-16,-16,8)$, \ $\vec n=(2,2,-1)$, \ $\vec d=(1,6,8)$: \ $\sin\alpha=\dfrac{6}{3\sqrt{101}}=\dfrac{2}{\sqrt{101}}$ \ $\Rightarrow$ \ $\res{\alpha\approx" + dms(deg(F(4, 101), True)) + r"}$",
               r"$\pi:2x+2y-z-6=0$; \ es tallen ($\vec d\cdot\vec n\neq0$) i $D$ ja és del pla: \ $\res{D(6,-5,-4)}$"])),
 (2, r"\pau{Canàries, extraordinària 2024}" + tasks(1, [r"Justifica si poden existir vectors $\vec u$ i $\vec v$, amb el mateix origen, que complisquen $|\vec u|=2$, $|\vec v|=3$ i $\vec u\cdot\vec v=8$.",
     r"Donats el pla $\pi:x+3y+2z+3=0$ i la recta $r:" + sy('2x-3y-z=4', 'x+y+2z=-3') + r"$, que són secants, calcula el punt de tall de la recta i el pla i l'angle que formen."]),
     tasks(1, [r"$|\vec u\cdot\vec v|\le|\vec u|\,|\vec v|=6<8$ (seria $\cos\alpha=\tfrac43>1$): \ \rest{no poden existir}.", r"$\vec d\parallel(2,-3,-1)\times(1,1,2)=(-5,-5,5)$, $\vec d=(1,1,-1)$. \ Punt: $\res{P(1,0,-2)}$. \ $\sin\alpha=\dfrac{2}{\sqrt3\sqrt{14}}$ \ $\Rightarrow$ \ $\res{\alpha\approx17{,}98^\circ}$"])),
 (2, r"\pau{La Rioja, ordinària 2024} Troba l'equació contínua de la recta $s$ que està continguda en el pla $\pi:x+y-2z+1=0$ i talla perpendicularment la recta $r:" + sy('x+y+z=-1', '4x-y+z=3') + r"$",
     r"$\vec d_r=(1,1,1)\times(4,-1,1)=(2,3,-5)$. \ $r\cap\pi=\left(\tfrac25,-\tfrac75,0\right)$. \ $\vec d_s=\vec n\times\vec d_r=(1,1,1)$: \ $\res{s:x-\tfrac25=y+\tfrac75=z}$"),
)

# ---------- 2. Distància a un pla
ck(projp([0, -1, -2], [1, 2, 3, -6]) == [1, 1, 1] and pdist2([0, -1, -2], [1, 2, 3, -6]) == 14 and dot([1, 2, 3], [1, 1, -1]) == 0)
ck(projp([1, 3, 0], [1, 2, -2, 7]) == [F(-5, 9), F(-1, 9), F(28, 9)] and pdist2([1, 3, 0], [1, 2, -2, 7]) == F(196, 9) and pdist2([1, 3, 0], [1, 2, -2, -21]) == F(196, 9))
ck(plane3([1, 0, 1], [0, 1, 0], [1, 1, 1]) == [1, 0, -1, 0] and all(pdist2([a_, 0, 0], [1, 0, -1, 0]) == 2 for a_ in (2, -2)))
ck(all(pdist2([0, 0, 0], [2, 2, 1, k_]) == 4 for k_ in (6, -6)) and projp([0, 0, 0], [2, 2, 1, -5]) == [F(10, 9), F(10, 9), F(5, 9)] and n2(cross([F(10, 9), F(10, 9), F(5, 9)], [3, 3, 3])) == F(50, 9))
ck(all(abs(det3([0, 2, -2], [1, 2, m_], [2, 3, 2])) == 18 for m_ in (5, -4)) and plane3([0, 2, -2], [1, 2, 0], [2, 3, 2]) == [2, 0, -1, -2] and pdist2([0, 0, 0], [2, 0, -1, -2]) == F(4, 5))
pau("Distància entre punts i d'un punt a un pla",
 (2, r"\pau{Astúries, ordinària 2026} Es considera el pla $\pi:x+2y+3z=6$ i el punt $P(0,-1,-2)$." + tasks(1, [r"Troba l'equació d'una recta paral·lela a $\pi$ que continga el punt $P$. És única aquesta recta?", r"Calcula el punt $Q\in\pi$ que dista menys de $P$. Quina distància hi ha entre $P$ i $Q$?"]),
     tasks(1, [r"Cal un director perpendicular a $\vec n=(1,2,3)$; per exemple, $\res{(x,y,z)=(0,-1,-2)+\lambda\,(1,1,-1)}$. \rest{No és única} (n'hi ha infinites).", r"$(t,\ -1+2t,\ -2+3t)$: $14t-14=0$, $t=1$: \ $\res{Q(1,1,1)}$, \ $d(P,Q)=\res{\sqrt{14}}$"])),
 (2, r"\pau{Catalunya, extraordinària 2024} Considera el punt $P(1,3,0)$ i el pla $\pi:x+2y-2z=-7$." + tasks(1, [r"Siga $r$ la recta perpendicular a $\pi$ que passa per $P$. Calcula el punt d'intersecció de $\pi$ amb $r$.", r"Calcula la distància $d$ del punt $P$ al pla $\pi$.", r"Calcula l'equació d'un altre pla $\pi'$ paral·lel a $\pi$ que també estiga a distància $d$ de $P$."]),
     tasks(1, [r"$(1+t,\ 3+2t,\ -2t)$: $14+9t=0$: \ $\res{\left(-\tfrac59,-\tfrac19,\tfrac{28}{9}\right)}$", r"$d=\dfrac{|1+6+7|}{3}=\res{\dfrac{14}{3}}$", r"$x+2y-2z+k=0$ amb $|7+k|=14$, $k\neq7$: \ $\res{x+2y-2z-21=0}$"])),
 (2, r"\pau{Galícia, ordinària 2026} Considera els punts $P(1,0,1)$, $Q(0,1,0)$ i $R(1,1,1)$." + tasks(1, [r"Demostra que $P$, $Q$ i $R$ no estan alineats i obtín l'equació implícita del pla $\pi$ que passa per ells.", r"Calcula el valor o valors de $a$ que fan que la distància del punt $S(a,0,0)$ a aquest pla siga igual a $\sqrt2$ unitats de longitud."]),
     tasks(1, [r"$\overrightarrow{PQ}\times\overrightarrow{PR}=(-1,1,-1)\times(0,1,0)=(1,0,-1)\neq\vec0$: \ $\res{\pi:x-z=0}$", r"$\dfrac{|a|}{\sqrt2}=\sqrt2$: \ $\res{a=\pm2}$"])),
 (2, r"\pau{Astúries, extraordinària 2026} Donat el pla $\pi:2x+2y+z=5$:" + tasks(1, [r"Troba l'equació d'un pla paral·lel a $\pi$ la distància del qual a l'origen siga 2. Hi ha més d'un pla que complisca aquestes condicions?", r"Calcula el punt $P$ del pla $\pi$ que està més pròxim a l'origen $O$.", r"Calcula l'àrea del paral·lelogram format pels segments $OP$ i $OQ$, on $Q(3,3,3)$."]),
     tasks(1, [r"$2x+2y+z+k=0$ amb $\dfrac{|k|}{3}=2$: \ \rest{n'hi ha dos}, \ $\res{2x+2y+z\pm6=0}$", r"Projecció de $O$: \ $\res{P\left(\tfrac{10}{9},\tfrac{10}{9},\tfrac59\right)}$", r"$|\overrightarrow{OP}\times\overrightarrow{OQ}|=\left|\left(\tfrac53,-\tfrac53,0\right)\right|=\res{\dfrac{5\sqrt2}{3}}$"])),
 (2, r"\pau{Andalusia, ordinària 2025} Siguen els punts $O(0,0,0)$, $A(0,2,-2)$, $B(1,2,m)$ i $C(2,3,2)$." + tasks(1, [r"Troba els valors de $m$ perquè el tetraedre determinat pels punts $O$, $A$, $B$ i $C$ tinga un volum de 3 unitats cúbiques.", r"Per a $m=0$, calcula la distància del punt $O$ al pla que passa pels punts $A$, $B$ i $C$."]),
     tasks(1, [r"$[\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC}]=4m-2$; \ $\dfrac{|4m-2|}{6}=3$: \ $\res{m=5\ \text{o}\ m=-4}$", r"Pla $ABC$: $2x-z-2=0$; \ $d(O,\pi)=\dfrac{2}{\sqrt5}=\res{\dfrac{2\sqrt5}{5}}$"])),
)

# ---------- 3. Distància d'un punt a una recta
ck(ldist2([0, 1, 1], [0, 0, 11], [3, 1, -1]) == 90 and plane([3, 1, -1], [0, 1, 1]) == [3, 1, -1, 0])
ck(all(n2(sub([2 + s_, 1 + 2 * s_, s_], [1, 1, 1])) == 6 * s_ * s_ + 2 for s_ in range(-3, 4)) and plane3([2, 1, 0], [3, 3, 1], [1, 1, 1]) == [1, -1, 1, -1] and ldist2([1, 1, 1], [2, 1, 0], [1, 2, 1]) == 2)
ck(plane([-4, 3, 0], [1, -1, 0]) == [4, -3, 0, -7] and ldist2([1, -1, 0], [0, 1, -1], [-4, 3, 0]) == 2 and cos2([-4, 3, 0], [1, -2, 3]) == F(100, 350) and near(deg(F(100, 350), True), 32.31))
ck(plane3([0, 0, 4], [-3, 0, 0], [0, -2, 0]) == [4, 6, -3, 12] and ldist2([1, 1, 1], [0, 0, 4], [-3, 0, -4]) == F(194, 25) and abs(det3([0, 0, 4], [-3, 0, 0], [0, -2, 0])) == 24)
pau("Distància d'un punt a una recta",
 (2, r"\pau{La Rioja, extraordinària 2026} Siguen la recta $r:\dfrac x3=y=\dfrac{z-11}{-1}$ i el punt $P(0,1,1)$." + tasks(1, [r"Determina l'equació del pla que passa pel punt $P$ i és perpendicular a la recta $r$.", r"Troba la distància de $P$ a la recta $r$."]),
     tasks(1, [r"$\res{3x+y-z=0}$", r"$A(0,0,11)$, $\overrightarrow{AP}\times\vec d=(0,1,-10)\times(3,1,-1)=(9,-30,-3)$: \ $d=\dfrac{\sqrt{990}}{\sqrt{11}}=\sqrt{90}=\res{3\sqrt{10}}$"])),
 (2, r"\pau{Cantàbria, ordinària 2025} Considera la recta $r:" + sy('2x-y=3', 'y-2z=1') + r"$ \ i el punt $P(1,1,1)$." + tasks(1, [r"Determina els punts de $r$ que estan a una distància de $\sqrt{14}$ unitats de $P$.", r"Obtín l'equació del pla que conté $r$ i $P$.", r"Calcula la distància entre $r$ i $P$."]),
     tasks(1, [r"$r:(2+t,\ 1+2t,\ t)$; \ $6t^2+2=14$, $t=\pm\sqrt2$: \ $\res{\left(2\pm\sqrt2,\ 1\pm2\sqrt2,\ \pm\sqrt2\right)}$", r"$\res{x-y+z-1=0}$", r"$\overrightarrow{AP}\times\vec d=(-1,0,1)\times(1,2,1)=(-2,2,-2)$: \ $d=\dfrac{\sqrt{12}}{\sqrt6}=\res{\sqrt2}$"])),
 (2, r"\pau{Extremadura, extraordinària 2025} Donats la recta $s:\dfrac{x}{-4}=\dfrac{y-1}{3}=\dfrac{z+1}{0}$, el pla $\pi:x-2y+3z-6=0$ i el punt $P(1,-1,0)$:" + tasks(1, [r"Obtín l'equació del pla perpendicular a la recta $s$ que passa per $P$.", r"Calcula la distància del punt $P$ a la recta $s$.", r"Calcula l'angle que forma la recta $s$ amb el pla $\pi$."]),
     tasks(1, [r"$\res{4x-3y-7=0}$", r"$\overrightarrow{AP}\times\vec d=(1,-2,1)\times(-4,3,0)=(-3,-4,-5)$: \ $d=\dfrac{\sqrt{50}}{5}=\res{\sqrt2}$", r"$\sin\alpha=\dfrac{|-4-6|}{5\sqrt{14}}=\dfrac{2}{\sqrt{14}}$ \ $\Rightarrow$ \ $\res{\alpha\approx32{,}31^\circ}$"])),
 (2, r"\pau{Cantàbria, ordinària 2026} Considera els punts $A(0,0,4)$, $B(-3,0,0)$ i $C(0,-2,0)$." + tasks(1, [r"Troba l'equació general del pla que conté $A$, $B$ i $C$.", r"Calcula la distància entre el punt $P(1,1,1)$ i la recta que conté $A$ i $B$.", r"Calcula el volum del tetraedre de vèrtexs $A$, $B$, $C$ i $D(0,0,0)$."]),
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
pau("Distància entre dues rectes",
 (2, r"\pau{País Basc, ordinària 2025} Es consideren la recta $r$ que passa pels punts $A(-4,4,1)$ i $B(1,0,-1)$ i la recta $s$ que passa pels punts $C(-2,7,-1)$ i $D(2,3,-1)$." + tasks(1, [r"Calcula la posició relativa de la recta $r$ respecte de la recta $s$.", r"En cas que siguen paral·leles o s'encreuen, calcula la distància entre elles. Si es tallen, calcula el punt d'intersecció."]),
     tasks(1, [r"$\vec d_r=(5,-4,-2)$, $\vec d_s=(4,-4,0)$, $[\overrightarrow{AC},\vec d_r,\vec d_s]=-32\neq0$: \ \rest{s'encreuen}", r"$|\vec d_r\times\vec d_s|=|(-8,-8,-4)|=12$: \ $d=\dfrac{32}{12}=\res{\dfrac83}$"])),
 (2, r"\pau{La Rioja, extraordinària 2025} Calcula la distància entre les rectes $r:" + sy(r'x=5+\lambda', 'y=-1', r'z=8+2\lambda') + r"$ \ i \ $s:" + sy(r'x=2+3\mu', r'y=2-\mu', r'z=-1+4\mu') + r"$",
     r"$\vec d_r\times\vec d_s=(2,2,-1)$, $\overrightarrow{PQ}=(-3,3,-9)$, $[\overrightarrow{PQ},\vec d_r,\vec d_s]=9$: \ $d=\dfrac93=\res{3}$"),
)

# ---------- 5. Recta i pla, dos plans
dA3 = cross([1, -1, 1], [1, 2, -1]); ck(dA3 == [-1, 2, 3] and dot([-8, -1, -2], dA3) == 0 and pdist2([F(10, 3), F(1, 3), 0], [-8, -1, -2, -5]) == F(1024, 69))
ck(pos_rp([0, 1, -1], [3, -1, 2], [1, 1, -1, -3]) == 'paral·lels' and pdist2([0, 1, -1], [1, 1, -1, -3]) == F(1, 3) and plane([3, -1, 2], [0, 1, -1]) == [3, -1, 2, 3])
ck(plane3([1, 1, 0], [3, 2, 3], [2, -1, 1]) == [7, 1, -5, -8] and pos_rp([1, 1, 0], [2, 1, 3], [1, 1, -1, -1]) == 'paral·lels' and pdist2([1, 1, 0], [1, 1, -1, -1]) == F(1, 3))
ck(pos_rp([1, -1, 2], [2, 1, -1], [2, -1, 3, -5]) == 'paral·lels' and pdist2([1, -1, 2], [2, -1, 3, -5]) == F(16, 14))
ck(pos_rp([1, 0, 2], [-3, 2, -1], [1, 1, -1, -2]) == 'paral·lels' and all(pdist2([1, 0, 2], [1, 1, -1, k_]) == 12 for k_ in (7, -5)))
ck(pdist2([0, 1, 3], [2, -1, 1, -5]) == F(9, 6) and onp([2, -1, 1, -2], [0, 1, 3]) and pdist2([0, 0, 2], [2, -1, 1, -5]) == F(9, 6) and pdist2([0, 0, 8], [2, -1, 1, -5]) == F(9, 6))
pau("Distància entre recta i pla i entre dos plans",
 (2, r"\pau{Andalusia, extraordinària 2025} Considera la recta $r:" + sy('x-y+z=3', 'x+2y-z=4') + r"$ \ i el pla $\pi:mx-y-2z=5$." + tasks(1, [r"Troba $m$ perquè $r$ i $\pi$ siguen paral·lels.", r"Per a $m=-8$, calcula la distància de la recta $r$ al pla $\pi$."]),
     tasks(1, [r"$\vec d=(1,-1,1)\times(1,2,-1)=(-1,2,3)$; \ $\vec d\cdot\vec n=-m-8=0$: \ $\res{m=-8}$ \ (i $r\not\subset\pi$)", r"$P\left(\tfrac{10}{3},\tfrac13,0\right)\in r$: \ $d=\dfrac{32}{\sqrt{69}}=\res{\dfrac{32\sqrt{69}}{69}}$"])),
 (2, r"\pau{Extremadura, ordinària 2025}" + tasks(1, [r"Comprova que el pla $\pi:x+y-z=3$ i la recta $r:\dfrac x3=\dfrac{y-1}{-1}=\dfrac{z+1}{2}$ no es tallen.", r"Calcula la distància entre el pla $\pi$ i la recta $r$.", r"Obtín l'equació del pla perpendicular a la recta $r$ que passa pel punt $(0,1,-1)$."]),
     tasks(1, [r"$\vec d\cdot\vec n=3-1-2=0$ i $(0,1,-1)\notin\pi$: \ \rest{paral·lels}", r"$d=\dfrac{|0+1+1-3|}{\sqrt3}=\res{\dfrac{\sqrt3}{3}}$", r"$\res{3x-y+2z+3=0}$"])),
 (2, r"\pau{Galícia, extraordinària 2026} Considera la recta $r:\dfrac{x-1}{2}=\dfrac{y-1}{1}=\dfrac z3$." + tasks(1, [r"Calcula l'equació implícita o general del pla $\pi$ que conté la recta $r$ i el punt $Q(2,-1,1)$.", r"Comprova que la recta $r$ és paral·lela al pla $\pi':x+y-z-1=0$. Calcula la distància de $r$ a $\pi'$."]),
     tasks(1, [r"$\overrightarrow{AQ}\times\vec d=(1,-2,1)\times(2,1,3)=(-7,-1,5)$: \ $\res{7x+y-5z-8=0}$", r"$\vec d\cdot\vec n=2+1-3=0$; \ $d=\dfrac{|1+1-0-1|}{\sqrt3}=\res{\dfrac{\sqrt3}{3}}$"])),
 (2, r"\pau{Múrcia, ordinària 2026} Considera el pla $\pi:2x-y+3z-5=0$ i la recta $r:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$." + tasks(1, [r"Estudia la posició relativa de $r$ i $\pi$.", r"Si $r$ talla $\pi$ en un sol punt, calcula aquest punt i l'angle que forma $r$ amb $\pi$. Si $r$ és paral·lela a $\pi$, calcula la distància de $r$ a $\pi$."]),
     tasks(1, [r"$\vec d\cdot\vec n=4-1-3=0$ i $(1,-1,2)\notin\pi$: \ \rest{paral·lels}", r"$d=\dfrac{|2+1+6-5|}{\sqrt{14}}=\res{\dfrac{4}{\sqrt{14}}=\dfrac{2\sqrt{14}}{7}}$"])),
 (2, r"\pau{Castella i Lleó, extraordinària 2025} Siguen el pla $\pi:x+y-z=2$ i la recta $r:\dfrac{x-1}{-3}=\dfrac y2=\dfrac{z-2}{-1}$. Calcula l'equació d'un pla $\pi'$ paral·lel al pla $\pi$ que estiga a una distància de $2\sqrt3$ unitats de la recta $r$. És únic aquest pla? Justifica la resposta.",
     r"$r\parallel\pi$ ($-3+2+1=0$). $\pi':x+y-z+k=0$ amb $\dfrac{|1+0-2+k|}{\sqrt3}=2\sqrt3$, $|k-1|=6$: \ \rest{dos plans}, \ $\res{x+y-z+7=0}$ \ i \ $\res{x+y-z-5=0}$"),
 (2, r"\pau{Catalunya, extraordinària 2025} Considera el pla $\pi:2x-y+z=5$ i el punt $P(0,1,3)$." + tasks(1, [r"Comprova que la distància del punt $P$ al pla $\pi$ és $\dfrac{\sqrt6}{2}$.", r"Troba l'equació general d'un pla $\pi_1$ paral·lel a $\pi$ que passe pel punt $P$. Quant val la distància entre $\pi_1$ i $\pi$?", r"Troba l'equació general d'un segon pla $\pi_2$, diferent de $\pi_1$, que siga paral·lel a $\pi$ i que estiga a una distància $\dfrac{\sqrt6}{2}$ de $\pi$."]),
     tasks(1, [r"$\dfrac{|0-1+3-5|}{\sqrt6}=\dfrac{3}{\sqrt6}=\dfrac{\sqrt6}{2}$ \ \checkmark", r"$\res{2x-y+z-2=0}$, \ distància $\res{\dfrac{\sqrt6}{2}}$ (la de $P$)", r"$2x-y+z+k=0$, $|k+5|=3$, $k\neq-2$: \ $\res{2x-y+z-8=0}$"])),
)

# ---------- 6. Recta per un punt que talla dues rectes
o6n = through([2, 4, -2], [-1, -2, 1], [1, 0, 3], [2, -1, 0], [-1, 2, 1]); ck(o6n[0] == [3, -2, -1, 0] and o6n[1] == [9, 2, 5, -16] and par_(o6n[2], [1, 3, -3]) and o6n[3] == [0, -2, 4] and o6n[4] == [1, 1, 1])
ck(online([2, 4, -2], [1, 3, -3], [1, 1, 1]) and not online([2, 4, 3], [1, 3, -3], [2, 4, -2]))   # la solució del recull porta (z-3), errata
ck(meet_lp([0, 0, 0], [1, 1, 1], [1, 1, 0, 0]) == (0, [0, 0, 0]) and onp([1, 1, 0, 0], [1, -1, 0]))
Am, dm, Bm = [2, -1, 0], [3, -1, 1], [3, -2, 0]; dsm = cross([1, -1, 0], [1, 0, 1])
ck(cross(dm, dsm) == [0, -4, -4] and det3(sub(Bm, Am), dm, dsm) == 4 and plane(dm, [5, -1, 2]) == [3, -1, 1, -18])
ck(dsm == [-1, -1, 1] and onp([1, -1, 0, -5], Bm) and onp([1, 0, 1, -3], Bm) and pos_rr(Am, dm, Bm, dsm) == "s'encreuen" and skew2(Am, dm, Bm, dsm) == F(1, 2))
ck(projl([5, -1, 2], Am, dm) == [5, -2, 1] and sub([5, -2, 1], [5, -1, 2]) == [0, -1, -1])
pau("Recta que passa per un punt i talla dues rectes",
 (2, r"\pau{Navarra, extraordinària 2026} Troba l'equació contínua de la recta $t$ que passa pel punt $A(2,4,-2)$ i talla les rectes $s:\dfrac{x-2}{-1}=\dfrac{y+1}{2}=\dfrac z1$ \ i \ $r:" + sy(r'x=-1+\lambda', 'y=-2', r'z=1+3\lambda') + r"$",
     r"Pla per $A$ i $r$: normal $(1,0,3)\times(3,6,-3)\parallel(3,-2,-1)$, \ $3x-2y-z=0$. \ Pla per $A$ i $s$: normal $(-1,2,1)\times(0,5,-2)\parallel(9,2,5)$, \ $9x+2y+5z-16=0$. \ Director $(1,3,-3)$: \ $\res{t:\dfrac{x-2}{1}=\dfrac{y-4}{3}=\dfrac{z+2}{-3}}$. Talla $r$ en $(0,-2,4)$ i $s$ en $(1,1,1)$."),
 (2, r"\pau{Castella i Lleó, extraordinària 2026} Donats el pla $\pi:x+y=0$, el punt $A(1,-1,0)$ i la recta $s:x=y=z$, troba la recta $r$, en forma paramètrica, que passa per $A$, està continguda en $\pi$ i talla la recta $s$.",
     r"$s\cap\pi$: $(t,t,t)$ amb $2t=0$: $O(0,0,0)$. La recta és $AO$ ($A\in\pi$): \ $\res{r:" + sy(r'x=1+\lambda', r'y=-1-\lambda', 'z=0') + r"}$"),
 (2, r"\pau{Madrid, extraordinària 2024} Donats el punt $P(5,-1,2)$ i les rectes $r:\dfrac{x-2}{3}=\dfrac{y+1}{-1}=\dfrac{z}{1}$ \ i \ $s:" + sy('x-y=5', 'x+z=3') + r"$" + tasks(1, [r"Estudia la posició relativa de les dues rectes i troba la distància entre elles.", r"Determina una equació de la recta que passa per $P$ i talla perpendicularment la recta $r$."]),
     tasks(1, [r"$\vec d_s=(1,-1,0)\times(1,0,1)=(-1,-1,1)$, $B(3,-2,0)$; \ $[\overrightarrow{AB},\vec d_r,\vec d_s]=4\neq0$: \rest{s'encreuen}; \ $|\vec d_r\times\vec d_s|=|(0,-4,-4)|=4\sqrt2$: \ $d=\res{\dfrac{\sqrt2}{2}\approx0{,}71}$",
               r"Projecció de $P$ sobre $r$: pla $3x-y+z=18$, $M(5,-2,1)$. \ $\res{(x,y,z)=(5,-1,2)+k\,(0,1,1)}$"])),
)

# ---------- 7. Perpendicular comuna
c7n = comperp([3, 7, 0], [1, -3, -1], [4, -1, 0], [-1, 1, -1]); ck(c7n[3] == [5, 1, -2] and c7n[4] == [3, 0, -1] and par_(c7n[0], [2, 1, -1]) and onp([1, 1, -2, -10], [3, 7, 0]) and onp([1, 0, 1, -3], [3, 7, 0]))
ck(cross([1, 1, -2], [1, 0, 1]) == [1, -3, -1] and online([3, 0, -1], [2, 1, -1], [5, 1, -2]))
pau("Perpendicular comuna",
 (2, r"\pau{Múrcia, ordinària 2025} Considera les rectes $r:" + sy('x=1', 'y=5+\lambda', 'z=\lambda') + r"$ \ i \ $s:" + sy(r'x=7+3\mu', r'y=-5+\mu', 'z=7') + r"$" + tasks(1, [r"Comprova que s'encreuen.", r"Troba l'equació de la recta perpendicular a totes dues.", r"Calcula la distància entre $r$ i $s$."]),
     tasks(1, [r"$[\overrightarrow{PQ},\vec d_r,\vec d_s]=" + vm([[6, -10, 7], [0, 1, 1], [3, 1, 0]]) + r"=-57\neq0$", r"$\vec n=\vec d_r\times\vec d_s=(-1,3,-3)$; plans que contenen cada recta i $\vec n$: \ $\res{t:" + sy('6x+y-z-11=0', '3x-9y-10z+4=0') + r"}$",
               r"$d=\dfrac{57}{\sqrt{19}}=\res{3\sqrt{19}}$"])),
 (2, r"\pau{Navarra, ordinària 2026} Troba l'equació contínua de la recta $t$ que talla perpendicularment les rectes $r:\dfrac x1=\dfrac{y+3}{1}=\dfrac{z-2}{-2}$ \ i \ $s:" + sy(r'x=-4+3\lambda', r'y=1+\lambda', r'z=-1+2\lambda') + r"$",
     r"$X(\lambda,-3+\lambda,2-2\lambda)$, $Y(-4+3\mu,1+\mu,-1+2\mu)$; \ $\overrightarrow{XY}\perp\vec d_r,\vec d_s$ \ $\Rightarrow$ \ $X" + V(X2) + r"$, $Y" + V(Y2) + r"$: \ $\res{t:\dfrac{x+1}{2}=\dfrac{y-2}{-4}=\dfrac{z-1}{-1}}$"),
 (2, r"\pau{Navarra, extraordinària 2025} Calcula l'equació contínua de la recta $t$ que talla perpendicularment les rectes $r:" + sy('x+y-2z-10=0', 'x+z-3=0') + r"$ \ i \ $s:\dfrac{x-4}{-1}=\dfrac{y+1}{1}=\dfrac{z}{-1}$",
     r"$\vec d_r=(1,1,-2)\times(1,0,1)=(1,-3,-1)$, $P(3,7,0)\in r$. \ Punts genèrics: $X(3+\lambda,7-3\lambda,-\lambda)$, $Y(4-\mu,-1+\mu,-\mu)$; \ $\overrightarrow{XY}\perp\vec d_r,\vec d_s$ \ $\Rightarrow$ \ $X(5,1,-2)$, $Y(3,0,-1)$: \ $\res{t:\dfrac{x-3}{2}=\dfrac{y}{1}=\dfrac{z+1}{-1}}$"),
)

# ---------- 6. Simètrics (punt i recta)
M10 = projl([1, 0, -1], [1, 0, 0], [1, 2, 2]); ck(M10 == [F(7, 9), F(-4, 9), F(-4, 9)] and sym(M10, [1, 0, -1]) == [F(5, 9), F(-8, 9), F(1, 9)])
M5 = projl([4, -3, 0], [-2, 0, 1], [0, -1, -1]); ck(M5 == [-2, -2, -1] and sym(M5, [4, -3, 0]) == [-8, -1, -2])
pau("Simètrics respecte d'un punt i d'una recta",
 (2, r"\pau{Castella i Lleó, ordinària 2024} Troba el punt simètric del punt $P(1,0,-1)$ respecte de la recta $r:\dfrac{x-1}{1}=\dfrac y2=\dfrac z2$.",
     r"Pla per $P$ perpendicular: $x+2y+2z+1=0$; \ $9\lambda+2=0$, \ $M" + V(M10) + r"$: \ $\res{P'" + V(sym(M10, [1, 0, -1])) + r"}$"),
 (2, r"\pau{País Basc, extraordinària 2025} Troba el punt $P'$ simètric de $P(4,-3,0)$ respecte de la recta $r$ que passa pels punts $A(-2,0,1)$ i $B(-2,-1,0)$.",
     r"$\vec d=(0,-1,-1)$; pla per $P$: $y+z+3=0$; \ $M(-2,-2,-1)$: \ $\res{P'(-8,-1,-2)}$"),
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
pau("Simètrics respecte d'un pla",
 (2, r"\pau{Andalusia, ordinària 2024}" + tasks(1, [r"Troba el punt simètric de $P(2,2,1)$ respecte de la recta $r:" + sy('x-2y+z=2', 'y-z=1') + r"$", r"Troba el punt simètric de $Q(1,-1,-3)$ respecte del pla $\pi:x-2y+z+6=0$."]),
     tasks(1, [r"$\vec d=(1,1,1)$, $A(4,1,0)$; pla per $P$: $x+y+z=5$, que talla $r$ en $M=A$: \ $\res{P'(6,0,-1)}$", r"$(1+t,\ -1-2t,\ -3+t)$: $6+6t=0$, $M(0,1,-4)$: \ $\res{Q'(-1,3,-5)}$"])),
 (2, r"\pau{Andalusia, extraordinària 2026} Considera la recta $r:" + sy(r'x=-2\lambda', r'y=-1+2\lambda', r'z=3+2\lambda') + r"$ \ i el pla $\pi:x-2y+z-3=0$." + tasks(1, [r"Determina l'equació de la recta que talla perpendicularment $r$ i està continguda en $\pi$.", r"Troba el punt simètric de $P(1,1,1)$ respecte de $\pi$."]),
     tasks(1, [r"$r\cap\pi=(-1,0,4)$; director $\vec n\times\vec d_r\parallel(3,2,1)$: \ $\res{(x,y,z)=(-1,0,4)+\lambda\,(3,2,1)}$", r"$\res{P'(2,-1,2)}$"])),
 (2, r"\pau{Canàries, ordinària 2025} Es consideren el punt $A(1,0,2)$, el pla $\pi:-x+2y+z+1=0$ i la recta $r:" + sy('4x-7y+2z=7', 'y-2z+5=0') + r"$" + tasks(1, [r"Troba la posició relativa del pla $\pi$ i la recta $r$.", r"Troba el punt simètric de $A$ respecte del pla $\pi$."]),
     tasks(1, [r"$\vec d\parallel(3,2,1)$, $\vec d\cdot\vec n=2\neq0$: \ \rest{es tallen en un punt}", r"$\res{A'\left(\tfrac53,-\tfrac43,\tfrac43\right)}$"])),
 (2, r"\pau{Extremadura, extraordinària 2026} Donats els plans $\pi_1:x+ky-3z-6=0$, $\pi_2:2x-y-5=0$ i el punt $A(2,3,-4)$:" + tasks(1, [r"Calcula el valor de $k$ perquè els plans $\pi_1$ i $\pi_2$ siguen perpendiculars.", r"Per a $k=2$, calcula el simètric del punt $A$ respecte del pla $\pi_1$.", r"Per a $k=2$, calcula la distància del punt $A$ al pla $\pi_1$."]),
     tasks(1, [r"$2-k=0$: \ $\res{k=2}$", r"$(2+t,\ 3+2t,\ -4-3t)$: $14+14t=0$, $M(1,1,-1)$: \ $\res{A'(0,-1,2)}$", r"$\dfrac{14}{\sqrt{14}}=\res{\sqrt{14}}$"])),
 (2, r"\pau{País Basc, extraordinària 2026} Siga $P$ el punt de tall de les rectes $r_1:" + sy('x=1+t', 'y=0', 'z=-t') + r"$ \ i \ $r_2:" + sy('x=s', 'y=-1+s', 'z=0') + r"$ \ Calcula el punt $P'$ simètric de $P$ respecte del pla d'equació $2x+y-z=3$.",
     r"$1+t=s$, $0=-1+s$, $-t=0$: \ $P(1,0,0)$. \ $(1+2t,\ t,\ -t)$: $6t-1=0$: \ $\res{P'\left(\tfrac53,\tfrac13,-\tfrac13\right)}$"),
 (2, r"\pau{Madrid, ordinària 2026} Donats el pla $\pi:2x+2y-z=13$ i la recta $r:\dfrac{x-2}{1}=\dfrac y1=\dfrac z4$:" + tasks(1, [r"Troba el punt simètric del punt $P(2,0,0)$ respecte del pla $\pi$.", r"Troba la distància entre el pla $\pi$ i la recta $r$."]),
     tasks(1, [r"$(2+2t,\ 2t,\ -t)$: $9t-9=0$, $M(4,2,-1)$: \ $\res{P'(6,4,-2)}$", r"$\vec d\cdot\vec n=2+2-4=0$: paral·lels; \ $d=\dfrac{|4-13|}{3}=\res{3}$"])),
 (2, r"\pau{Galícia, extraordinària 2026} Considera el punt $P(3,0,-1)$." + tasks(1, [r"Calcula el punt $P'$ simètric de $P$ respecte del punt $Q(2,-1,2)$.", r"Calcula el punt $P''$ simètric de $P$ respecte del pla $\pi:x+2y+z-8=0$."]),
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
pau("Àrees i volums",
 (2, r"\pau{Cantàbria, extraordinària 2026} Considera els punts $A(0,5,-1)$ i $B(-3,11,-10)$ i la recta $r:\dfrac{x-3}{1}=\dfrac{y+2}{-2}=\dfrac z3$." + tasks(1, [r"Estudia la posició relativa de $r$ i la recta que conté $A$ i $B$.", r"Calcula l'àrea del triangle format pels vèrtexs $A$, $B$ i un punt genèric de $r$.", r"Troba l'equació general o implícita del pla que conté $r$ i $A$."]),
     tasks(1, [r"$\overrightarrow{AB}=(-3,6,-9)=-3\,(1,-2,3)$ i $A\notin r$: \ \rest{paral·leles}", r"Base $|\overrightarrow{AB}|=3\sqrt{14}$, altura $d(A,r)=\dfrac{\sqrt{426}}{\sqrt{14}}$ (constant): \ $S=\res{\dfrac{3\sqrt{426}}{2}\approx30{,}96}$", r"$\res{19x+8y-z-41=0}$"])),
 (2, r"\pau{Cantàbria, ordinària 2024} Siguen $A(6,2,-1)$, $B(3,0,5)$ i $C(-2,1,2)$ els vèrtexs d'un triangle." + tasks(1, [r"Calcula els angles interns del triangle.", r"Calcula l'àrea del triangle."]),
     tasks(1, [r"Amb els vectors que ixen de cada vèrtex: \ $\res{\hat A\approx" + ('%.2f' % angs[0]).replace('.', '{,}') + r"^\circ,\ \hat B\approx" + ('%.2f' % angs[1]).replace('.', '{,}') + r"^\circ,\ \hat C\approx" + ('%.2f' % angs[2]).replace('.', '{,}') + r"^\circ}$",
               r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-3,-2,6)\times(-8,-1,3)$, de mòdul $\sqrt{1690}$: \ $S=\res{\dfrac{13\sqrt{10}}{2}}$"])),
 (2, r"\pau{Extremadura, ordinària 2024} Donats els punts $A(1,2,1)$, $B(0,3,1)$ i $C(1,0,-1)$, determina:" + tasks(1, [r"un vector unitari i ortogonal als vectors $\overrightarrow{AB}$ i $\overrightarrow{AC}$;", r"l'angle determinat per aquests vectors;", r"l'àrea del triangle que formen $A$, $B$ i $C$."]),
     tasks(1, [r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-2,-2,2)$: \ $\res{\left(-\tfrac{1}{\sqrt3},-\tfrac{1}{\sqrt3},\tfrac{1}{\sqrt3}\right)}$ (o l'oposat)", r"$\cos\alpha=\dfrac{-2}{\sqrt2\,\sqrt8}=-\dfrac12$: \ $\res{120^\circ}$", r"$S=\tfrac12\sqrt{12}=\res{\sqrt3}$"])),
 (2, r"\pau{Madrid, ordinària 2025} Siguen el punt $P(0,1,1)$ i el pla $\pi:x+y=2$." + tasks(1, [r"Troba la distància del punt $P$ al pla $\pi$.", r"Determina el punt $Q$ del pla $\pi$ la distància del qual a $P$ és igual que la distància de $P$ a $\pi$.", r"Troba l'àrea del triangle format per $P$ i els punts de tall del pla $\pi$ amb els eixos de coordenades."]),
     tasks(1, [r"$\res{\dfrac{\sqrt2}{2}}$", r"És la projecció: \ $\res{Q\left(\tfrac12,\tfrac32,1\right)}$", r"$\pi$ talla els eixos en $(2,0,0)$ i $(0,2,0)$ (és paral·lel a $OZ$): \ $S=\tfrac12|(2,-1,-1)\times(0,1,-1)|=\tfrac12|(2,2,2)|=\res{\sqrt3}$"])),
 (2, r"\pau{Navarra, extraordinària 2024} El punt $P(4,5,0)$ és el punt mig d'un costat d'un quadrat. El costat paral·lel a l'anterior està contingut en la recta $r:" + sy('2x+2y+z=0', '2x-z-2=0') + r"$ \ Calcula els dos vèrtexs que determinen aquest segon costat.",
     r"$\vec d=(1,-2,2)$; la projecció de $P$ sobre $r$ és $(0,1,-2)$, el punt mig del segon costat, i el costat mesura $d(P,r)=6$. Els vèrtexs disten 3 d'aquest punt: $(0,1,-2)\pm(1,-2,2)$: \ $\res{(1,-1,0)\ \text{i}\ (-1,3,-4)}$"),
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
pau("Llocs geomètrics",
 (2, r"\pau{Andalusia, extraordinària 2024} Considera els punts $A(4,0,0)$ i $B(0,2,0)$. Calcula els punts del pla $OXZ$ que formen un triangle equilàter amb $A$ i $B$.",
     r"$C(x,0,z)$ amb $|\overrightarrow{CA}|^2=|\overrightarrow{CB}|^2=|\overrightarrow{AB}|^2=20$: \ $(x-4)^2+z^2=x^2+4+z^2=20$ \ $\Rightarrow$ \ $x=\tfrac32$, $z^2=\tfrac{55}{4}$: \ $\res{C\left(\tfrac32,0,\pm\tfrac{\sqrt{55}}{2}\right)}$"),
 (2, r"\pau{Andalusia, ordinària 2024} Considera les rectes $r:" + sy('y=0', '2x-z=0') + r"$ \ i \ $s:" + sy('x+y+7=0', 'z=0') + r"$" + tasks(1, [r"Estudia la posició relativa de $r$ i $s$.", r"Calcula l'equació del pla paral·lel a $r$ i a $s$ que equidista de totes dues rectes."]),
     tasks(1, [r"$\vec d_r=(1,0,2)$, $\vec d_s=(1,-1,0)$, $[\overrightarrow{OQ},\vec d_r,\vec d_s]\neq0$ amb $Q(-7,0,0)$: \ \rest{s'encreuen}", r"$\vec n=\vec d_r\times\vec d_s=(2,2,-1)$; \ $2x+2y-z+k=0$ amb $|k|=|k-14|$: \ $\res{2x+2y-z+7=0}$"])),
 (2, r"\pau{Castella i Lleó, ordinària 2026} Donats el pla $\pi_1:2x-3y+z=a$ i el pla $\pi_2$ determinat pel punt $P(0,2,4)$ i els vectors directors $\vec v_1=(0,2,6)$ i $\vec v_2=(1,0,b)$:" + tasks(1, [r"Calcula els valors de $a$ i $b$ perquè $\pi_1$ i $\pi_2$ siguen paral·lels i distints.", r"Per a $a=1$ i $b=0$, determina les equacions paramètriques de la recta intersecció de $\pi_1$ i $\pi_2$.", r"Per a $a=4$ i $b=-2$, determina els punts que estan a igual distància de $\pi_1$ i $\pi_2$."]),
     tasks(1, [r"$\vec v_1\times\vec v_2=(2b,6,-2)\parallel(2,-3,1)$: $\res{b=-2}$; aleshores $\pi_2:2x-3y+z=-2$, i són distints si $\res{a\neq-2}$", r"$\pi_2:3y-z=2$: \ $\res{x=\tfrac32,\ y=\lambda,\ z=-2+3\lambda}$", r"Plans paral·lels $2x-3y+z=4$ i $2x-3y+z=-2$: el pla a mitja distància, \ $\res{2x-3y+z-1=0}$"])),
 (2, r"\pau{Catalunya, ordinària 2025} Considera el pla $\pi:x+y=0$." + tasks(1, [r"Calcula l'equació del pla $\pi'$ que és perpendicular a $\pi$ i conté els punts $P(1,-1,2)$ i $Q(3,-3,6)$.", r"Calcula l'equació paramètrica de la recta continguda en $\pi'$ que conté els punts de $\pi'$ que estan a la mateixa distància de $P$ que de $Q$."]),
     tasks(1, [r"$\vec n'\parallel\overrightarrow{PQ}\times\vec n=(2,-2,4)\times(1,1,0)$: \ $\res{x-y-z=0}$", r"És $\pi'\cap$ (pla mediador $x-y+2z=12$): \ $\res{x=2+\lambda,\ y=-2+\lambda,\ z=4}$"])),
 (2, r"\pau{Catalunya, ordinària 2024} Considera els punts $A(1,2,3)$ i $B(-3,-2,3)$." + tasks(1, [r"Calcula l'equació del pla $\pi$ que és perpendicular a la recta $AB$ i que passa pel punt mig entre $A$ i $B$. Justifica que aquest pla està format, precisament, pels punts $P$ que estan a igual distància de $A$ que de $B$.", r"Calcula les distàncies de $A$ i de $B$ al pla $\pi$ i comprova que són iguals. És una casualitat?", r"Siga $C(-7,6,3)$. El triangle $ABC$ és isòsceles? Calcula'n l'àrea."]),
     tasks(1, [r"$\res{x+y+1=0}$; \ $d(P,A)^2=d(P,B)^2$ es redueix a $8x+8y+8=0$.", r"$d(A,\pi)=d(B,\pi)=\res{2\sqrt2}$: no és casualitat, $B$ és el simètric de $A$ respecte de $\pi$.", r"$C\in\pi$, per tant $CA=CB$: \ \rest{isòsceles}. \ $S=\tfrac12|(-4,-4,0)\times(-8,4,0)|=\res{24}$"])),
 (2, r"\pau{Múrcia, extraordinària 2024} Considera els plans $x+y+z=-3$ i $x+y-z=3$ i la recta $r:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac z3$." + tasks(1, [r"Comprova que tots dos plans es tallen i calcula l'angle que formen.", r"Estudia la posició relativa de la recta $r$ amb el pla $x+y-z=3$.", r"Determina els punts de la recta $r$ que equidisten de tots dos plans."]),
     tasks(1, [r"$\cos\alpha=\dfrac13$: \ $\res{\alpha\approx70{,}53^\circ}$", r"$\vec d\cdot\vec n=2+1-3=0$ i $(1,-1,0)$ no és del pla: \ \rest{paral·lels}", r"$(1+2t,-1+t,3t)$: $\dfrac{|6t+3|}{\sqrt3}=\dfrac{3}{\sqrt3}$, $t=0$ o $t=-1$: \ $\res{(1,-1,0)\ \text{i}\ (-1,-2,-3)}$"])),
 (2, r"\pau{Navarra, extraordinària 2025} Calcula l'equació del pla que equidista dels punts $A(3,3,5)$ i $B(1,-1,1)$. Calcula l'equació dels plans que disten 6 unitats del pla anterior.",
     r"Pla mediador: \ $\res{x+2y+2z-10=0}$. \ $x+2y+2z+k=0$ amb $\dfrac{|k+10|}{3}=6$: \ $\res{x+2y+2z+8=0}$ \ i \ $\res{x+2y+2z-28=0}$"),
 (2, r"\pau{Madrid, extraordinària 2024} Siguen els punts $P(1,-1,3)$ i $Q(2,1,-1)$." + tasks(1, [r"Determina una equació del pla respecte del qual tots dos punts són simètrics.", r"El segment $PQ$ és un dels tres costats d'un triangle en què la suma dels quadrats de les longituds dels costats és 34 i el tercer vèrtex es troba en la recta $r:x-2=y=z$. Calcula les coordenades del tercer vèrtex sabent que cap de les seues coordenades és nul·la."]),
     tasks(1, [r"Pla mediador: \ $\res{2x+4y-8z+5=0}$", r"$R(2+t,t,t)$: $21+|PR|^2+|QR|^2=34+6t^2-2t=34$, \ $t=0$ (no val: $R(2,0,0)$) o $t=\tfrac13$: \ $\res{R\left(\tfrac73,\tfrac13,\tfrac13\right)}$"])),
 (2, r"\pau{País Basc, ordinària 2026} Siguen els punts $A(1,1,2)$ i $B(-1,0,3)$." + tasks(1, [r"Troba l'equació del pla $\pi$ que compleix que $A$ i $B$ són simètrics respecte de $\pi$.", r"Quina és la distància de $A$ a $\pi$?"]),
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
pau("Problemes i qüestions",
 (2, r"\pau{Astúries, ordinària 2026} Un mòbil es desplaça en línia recta des del punt $P(2,1,3)$ cap al punt $Q(0,-1,1)$. Quan arriba a la meitat de la distància de $P$ a $Q$ fa un gir i es desplaça per la recta que passa per $H(1,1,1)$." + tasks(1, [r"Calcula les coordenades del punt en què fa el gir.", r"Calcula la recta per la qual es desplaça el mòbil després del gir.", r"Calcula l'angle de gir del mòbil."]),
     tasks(1, [r"Punt mig: \ $\res{G(1,0,2)}$", r"$\overrightarrow{GH}=(0,1,-1)$: \ $\res{x=1,\ y=\lambda,\ z=2-\lambda}$", r"$\overrightarrow{PQ}\cdot\overrightarrow{GH}=(-2,-2,-2)\cdot(0,1,-1)=0$: \ $\res{90^\circ}$"])),
 (2, r"\pau{Múrcia, extraordinària 2025} Un helicòpter situat en el punt $P(1,2,1)$ vol aterrar en el pla $\pi:x+y+3z=0$." + tasks(1, [r"Calcula l'equació en forma contínua de la recta de la trajectòria que el porte al punt més pròxim de $\pi$.", r"Troba aquest punt.", r"Calcula la distància que ha de recórrer."]),
     tasks(1, [r"$\res{\dfrac{x-1}{1}=\dfrac{y-2}{1}=\dfrac{z-1}{3}}$", r"$6+11t=0$: \ $\res{\left(\tfrac{5}{11},\tfrac{16}{11},-\tfrac{7}{11}\right)}$", r"$d=\dfrac{6}{\sqrt{11}}=\res{\dfrac{6\sqrt{11}}{11}\approx1{,}81}$"])),
 (2, r"\pau{Astúries, ordinària 2025} S'estan construint dos ponts rectes en un tram d'autovia, un per a cada carril. Els ponts segueixen les equacions $r_1(t)=(2+t,\,-1-2t,\,3+2t)$ i $r_2(s)=(1+2s,\,4-s,\,4-2s)$." + tasks(1, [r"Estudia si els ponts són paral·lels, es tallen o s'encreuen.", r"L'empresa vol construir un pont de servei que els unisca i que siga el més curt possible. Quina longitud tindrà la via de servei? Indica'n els punts inicial i final."]),
     tasks(1, [r"$[\overrightarrow{PQ},\vec d_1,\vec d_2]=27\neq0$: \ \rest{s'encreuen}", r"Perpendicular comuna: \ $\res{E(1,1,1),\ F(3,3,2)}$, \ longitud $|\overrightarrow{EF}|=\res{3}$"])),
 (2, r"\pau{Madrid, extraordinària 2026} Es consideren el punt $P(1,2,1)$ i el pla d'equació $2x-2y+z=1$. Es traça un cub amb una cara en el pla i un vèrtex en el punt $P$." + tasks(1, [r"Determina la longitud del costat del cub i el seu volum.", r"Troba un altre vèrtex del cub."]),
     tasks(1, [r"Costat $=d(P,\pi)=\dfrac{|2-4+1-1|}{3}=\res{\dfrac23}$; \ volum $\res{\dfrac{8}{27}}$", r"El vèrtex de la cara del pla que està sota $P$ (la projecció): \ $\res{\left(\tfrac{13}{9},\tfrac{14}{9},\tfrac{11}{9}\right)}$"])),
 (3, r"\pau{Aragó, extraordinària 2025} Es vol construir una estructura en forma de tetraedre la base de la qual té com a vèrtexs els punts $A(0,0,0)$, $B\left(2,0,\tfrac12\right)$ i $C\left(\tfrac32,3,1\right)$; el vèrtex superior, $D$, es troba en una biga recta entre els punts $E(0,1,3)$ i $F(3,2,3)$, és a dir, $D=E+\lambda\,\overrightarrow{EF}$ amb $\lambda\in[0,1]$." + tasks(1, [r"Calcula el volum màxim d'aquesta estructura (totes les dades estan en metres).", r"Tenint en compte que el volum d'una piràmide és un terç de l'àrea de la base per l'altura, calcula l'altura de l'estructura (des de $D$ fins a la base) si prenem $\lambda=1$."]),
     tasks(1, [r"$D(3\lambda,1+\lambda,3)$; \ $V=\tfrac16\big|[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}]\big|=\dfrac{67-23\lambda}{24}$, màxim en $\lambda=0$: \ $\res{V=\dfrac{67}{24}\approx2{,}79\ \text{m}^3}$",
               r"$V=\dfrac{11}{6}$, \ $S_{ABC}=\tfrac12\left|\left(-\tfrac32,-\tfrac54,6\right)\right|=\dfrac{7\sqrt{13}}{8}$: \ $h=\dfrac{3V}{S}=\res{\dfrac{44\sqrt{13}}{91}\approx1{,}74\ \text{m}}$"])),
 (2, r"\pau{Castella-la Manxa, ordinària 2026} En un parc públic s'està instal·lant un sistema de vigilància mitjançant sensors de moviment a banda i banda d'un mur recte, representat pel pla $\pi:x+y+z-6=0$. Un dels sensors està situat en el punt $P(1,2,6)$ i es vol instal·lar un segon sensor en el punt $P'$, simètric de l'anterior respecte del pla $\pi$." + tasks(1, [r"Determina raonadament les coordenades del punt d'instal·lació del segon sensor, $P'$.", r"Calcula la distància entre els dos sensors."]),
     tasks(1, [r"$M(0,1,5)$: \ $\res{P'(-1,0,4)}$", r"$|\overrightarrow{PP'}|=2\,d(P,\pi)=\res{2\sqrt3}$"])),
 (2, r"\pau{Castella-la Manxa, extraordinària 2025} Per a les festes del Corpus de Toledo s'instal·len tendals als carrers per on passa la processó. En un d'ells, els operaris col·loquen els punts de suport $A(0,1,-2)$, $B(1,2,0)$, $C(0,0,1)$ i $D(1,0,m)$, amb $m\in\mathbb R$." + tasks(1, [r"Calcula el valor de $m$ perquè els quatre punts siguen coplanaris.", r"Determina l'equació del pla $\pi$ que conté el tendal.", r"Si els adorns florals han d'estar com a mínim a 1 metre de distància del tendal i s'ha col·locat un adorn de flors en el punt $P(1,2,3)$, estarà correctament situat?"]),
     tasks(1, [r"$[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}]=6-m=0$: \ $\res{m=6}$", r"$\res{5x-3y-z+1=0}$", r"$d(P,\pi)=\dfrac{3}{\sqrt{35}}\approx0{,}51<1$: \ \rest{no està ben situat}"])),
 (2, r"\pau{Illes Balears, ordinària 2024} Considerem els punts $A(0,0,0)$, $B(2,-1,3)$ i $C(-1,2,1)$." + tasks(1, [r"Calcula el punt $D$ tal que $ABDC$ siga un paral·lelogram.", r"Calcula un dels punts $E$ de l'espai de manera que la recta $AE$ siga perpendicular al pla $ABC$ i la distància entre els punts $A$ i $E$ siga 1.", r"Escriu l'equació d'un dels plans paral·lels al pla $ABC$ que disten una unitat d'aquest."]),
     tasks(1, [r"$D=B+C-A=\res{(1,1,4)}$", r"$\vec n=\overrightarrow{AB}\times\overrightarrow{AC}=(-7,-5,3)$, $|\vec n|=\sqrt{83}$: \ $\res{E=\pm\tfrac{1}{\sqrt{83}}(-7,-5,3)}$", r"$\res{7x+5y-3z\pm\sqrt{83}=0}$"])),
)

# =====================================================================
print(NCHK[0], 'comprovacions correctes')
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={angles, distàncies, perpendicular comuna, projeccions, simètrics, àrees, volums, pla mediador, plans bisectors, esfera, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques II}')
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
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU d'altres comunitats
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Problemes mètrics"
# espai fi després de les comes de les ternes de coordenades: (1,-2,3) -> (1,\,-2,\,3)
TRI = re.compile(r'\((-?[\w\\{}.+\-]+),(-?[\w\\{}.+\-]+),(-?[\w\\{}.+\-]+)\)')
# i les equacions amb fraccions (equació contínua…) no es parteixen entre dues línies
INL = re.compile(r'(?<![\\$])\$([^$]+)\$')
def esp(t):
    t = TRI.sub(lambda mm: '(' + r',\,'.join(mm.groups()) + ')', t)
    return INL.sub(lambda mm: r'\mbox{$' + mm.group(1) + '$}' if r'\dfrac' in mm.group(1) and len(mm.group(1)) < 260 and r'\begin' not in mm.group(1) else mm.group(0), t)
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 4: %s. 2n de Batxillerat MII}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 4: Problemes mètrics · 2n Batxillerat MII" % t)
    assert 'MII}' in p and '2n Batxillerat MII' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques II}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 4' if sol else "Fitxa d'exercicis · Unitat 4") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Les distàncies i els angles es donen exactes (amb arrels simplificades) i, quan cal, aproximats amb dues xifres decimals. Si una recta o un pla de la teua solució s'escriu d'una altra manera, comprova que és el mateix (un punt comú i vectors proporcionals). Pots comprovar els resultats amb el laboratori mètric dels apunts interactius."
             if sol else r"Resol els exercicis al quadern justificant cada pas. Fes un esbós quan t'ajude a veure la situació i comprova sempre els resultats (que la projecció és del pla o de la recta, que el punt mig del segment $PP'$ és el punt $M$\ldots). Els exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat d'altres comunitats autònomes (2024--2026), traduïts al valencià.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb el laboratori mètric dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't4-fitxa-solucions.tex' if sol else 't4-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
regs = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
print(n, 'exercicis,', npau, 'de la PAU de', len(regs), 'comunitats:', ', '.join(regs))
