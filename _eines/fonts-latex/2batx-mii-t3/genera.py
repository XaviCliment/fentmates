# Genera t3-fitxa-exercicis.tex i t3-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 3: Vectors i aplicacions.
# Rectes, plans i feixos de plans) a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a
# Batxillerat les estrelles no es mostren. Les seccions segueixen els apunts interactius (materials/2batx-mii/t3-...html) i
# no fan servir res de geometria mètrica (angles entre rectes i plans, distàncies, simètrics respecte d'una recta o d'un pla),
# que és de la unitat 4. Al final de cada secció hi ha exercicis de la PAU de Matemàtiques II de 16 comunitats autònomes
# (2024-2026), traduïts al valencià i presos del recull «Geometría en el espacio en pruebas de acceso a la universidad en
# España» (ebaumatematicas.com, curs 2026/27), sense els apartats mètrics. Tots els resultats es calculen o es comproven
# aquí amb aritmètica exacta (ck) abans d'escriure els fitxers.
# Ús: python3 genera.py && pdflatex t3-fitxa-exercicis.tex (dues vegades) && pdflatex t3-fitxa-solucions.tex (dues vegades)
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

# =====================================================================
# 1. Vectors a l'espai i aplicacions
A, B, C = [1, -2, 3], [3, -1, 1], [-1, 2, 7]
AB, AC = sub(B, A), sub(C, A)
ck(AB == [2, 1, -2] and AC == [-2, 4, 4] and n2(AB) == 9 and n2(AC) == 36)
ck(add(mul(AB, 3), AC) == [4, 7, -2] and mul(AB, -3) == [-6, -3, 6])
M1, A1 = [1, -2, 4], [3, 0, -1]
ck(sub(mul(M1, 2), A1) == [-1, -4, 9] and sub(mul([0, 1, -2], 2), [2, -3, 1]) == [-2, 5, -5])
A4, B4 = [-2, 1, 5], [4, -5, -1]
ck(add(A4, mul(sub(B4, A4), F(1, 3))) == [0, -1, 3] and add(A4, mul(sub(B4, A4), F(2, 3))) == [2, -3, 1])
ck(par_([1, 1, -2], sub([4, 3, -4], [1, 0, 2])))                             # a = 4, b = -4
ck(sub(add([1, 2, -1], [2, -1, 4]), [3, 0, 2]) == [0, 1, 1] and mul(add([1, 2, -1], [2, -1, 4]), F(1, 2)) == [F(3, 2), F(1, 2), F(3, 2)])
ck(sub(sub(mul([1, 2, 0], 3), [2, 1, -3]), [-1, 4, 2]) == [2, 1, 1])
ck(add([1, -1, 2], mul(sub([7, 5, -4], [1, -1, 2]), F(2, 3))) == [5, 3, -2])
S.append(("Vectors a l'espai i aplicacions", [
 (1, r"Siguen $A(1,-2,3)$, $B(3,-1,1)$ i $C(-1,2,7)$." + tasks(2, [r"Calcula $\overrightarrow{AB}$, $\overrightarrow{AC}$ i els seus mòduls.", r"Troba un vector unitari amb la direcció i el sentit de $\overrightarrow{AC}$.",
     r"Troba un vector de mòdul 9 paral·lel a $\overrightarrow{AB}$ i de sentit contrari.", r"Calcula $3\overrightarrow{AB}+\overrightarrow{AC}$."]),
     tasks(2, [r"$\overrightarrow{AB}=(2,1,-2)$, $|\overrightarrow{AB}|=\sqrt{9}=\res{3}$; \ $\overrightarrow{AC}=(-2,4,4)$, $|\overrightarrow{AC}|=\sqrt{36}=\res{6}$",
               r"$\dfrac{\overrightarrow{AC}}{6}=\res{\left(-\tfrac13,\tfrac23,\tfrac23\right)}$", r"$-3\,\overrightarrow{AB}=\res{(-6,-3,6)}$", r"$\res{(4,7,-2)}$"])),
 (1, r"El punt mig del segment $AB$ és $M(1,-2,4)$ i $A(3,0,-1)$. Calcula $B$. Troba també el simètric de $P(2,-3,1)$ respecte del punt $Q(0,1,-2)$."
     + recorda(r"El punt mig de $A$ i $B$ és $M=\frac{A+B}{2}$; per tant, $B=2M-A$. El simètric d'un punt respecte d'un altre es calcula igual."),
     r"$B=2M-A=\res{(-1,-4,9)}$. \qquad $P'=2Q-P=\res{(-2,5,-5)}$"),
 (2, r"Divideix en tres parts iguals el segment d'extrems $A(-2,1,5)$ i $B(4,-5,-1)$.",
     r"$\overrightarrow{AB}=(6,-6,-6)$, \ $\tfrac13\overrightarrow{AB}=(2,-2,-2)$: \ $P_1=A+\tfrac13\overrightarrow{AB}=\res{(0,-1,3)}$, \ $P_2=A+\tfrac23\overrightarrow{AB}=\res{(2,-3,1)}$"),
 (2, r"Troba $a$ i $b$ perquè els punts $A(1,0,2)$, $B(2,1,0)$ i $C(a,3,b)$ estiguen alineats.",
     r"$\overrightarrow{AB}=(1,1,-2)$ i $\overrightarrow{AC}=(a-1,3,b-2)$ han de ser proporcionals: $\dfrac{a-1}{1}=\dfrac31=\dfrac{b-2}{-2}$ \ $\Rightarrow$ \ $\res{a=4,\ b=-4}$"),
 (2, r"Els punts $A(1,2,-1)$, $B(3,0,2)$ i $C(2,-1,4)$ són tres vèrtexs consecutius del paral·lelogram $ABCD$. Calcula el quart vèrtex $D$ i el centre del paral·lelogram.",
     r"$\overrightarrow{AD}=\overrightarrow{BC}$: \ $D=A+C-B=\res{(0,1,1)}$. Les diagonals es tallen en el punt mig: \ centre $=\dfrac{A+C}{2}=\res{\left(\tfrac32,\tfrac12,\tfrac32\right)}$"),
 (2, r"El baricentre del triangle $ABC$ és $G(1,2,0)$, amb $A(2,1,-3)$ i $B(-1,4,2)$. Troba el vèrtex $C$.",
     r"$G=\dfrac{A+B+C}{3}\Rightarrow C=3G-A-B=(3-2+1,\ 6-1-4,\ 0+3-2)=\res{(2,1,1)}$"),
 (2, r"Troba el punt $P$ del segment $AB$, amb $A(1,-1,2)$ i $B(7,5,-4)$, que compleix $\overline{AP}=2\,\overline{PB}$.",
     r"$P$ és a dos terços del segment des de $A$: \ $P=A+\tfrac23\overrightarrow{AB}=(1,-1,2)+\tfrac23(6,6,-6)=\res{(5,3,-2)}$"),
]))

# =====================================================================
# 2. Dependència lineal i bases
u2, v2, w2 = [1, 2, -1], [2, 1, 3], [0, 3, -5]
ck(det3(u2, v2, w2) == 0 and add(mul(u2, 2), mul(v2, -1)) == w2)
for a in [F(k, 2) for k in range(-12, 13)]:
    ck(det3([1, 1, 1], [1, a, 1], [1, 1, a * a]) == (a - 1) ** 2 * (a + 1))
ck(rank([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 1 and rank([[1, 1, 1], [1, -1, 1], [1, 1, 1]]) == 2)
ck(det3([1, 1, 0], [0, 1, 1], [1, 0, 1]) == 2 and add(add(mul([1, 1, 0], 1), mul([0, 1, 1], 0)), mul([1, 0, 1], 2)) == [3, 1, 2])
ck(det3([1, 1, 0], [0, 1, 1], [1, 0, 1]) != 0 and det3([1, -1, 0], [0, 1, -1], [-1, 0, 1]) == 0)
ck(add(mul([1, 1, 0], 2), mul([0, 1, 1], 3)) == [2, 5, 3] and rank([[1, 1, 0], [0, 1, 1], [1, 2, 3]]) == 3)
S.append(("Dependència lineal i bases", [
 (1, r"Estudia si els vectors $\vec u=(1,2,-1)$, $\vec v=(2,1,3)$ i $\vec w=(0,3,-5)$ són linealment independents. Si no ho són, escriu $\vec w$ com a combinació lineal de $\vec u$ i $\vec v$.",
     r"$" + vm([u2, v2, w2]) + r"=1(-5-9)-2(-10-0)-1(6-0)=0$: \ \rest{linealment dependents}. \ $\vec w=a\vec u+b\vec v$: \ $a+2b=0$, $2a+b=3$ $\Rightarrow$ $a=2$, $b=-1$, i la tercera es compleix ($-2-3=-5$): \ $\res{\vec w=2\vec u-\vec v}$"),
 (2, r"Considera els vectors $\vec u=(1,1,1)$, $\vec v=(1,a,1)$ i $\vec w=(1,1,a^2)$." + tasks(1, [r"Per a quins valors de $a$ formen una base de $\mathbb R^3$?", r"Calcula el rang del conjunt $\{\vec u,\vec v,\vec w\}$ per als altres valors de $a$."]),
     tasks(1, [r"$" + r"\begin{vmatrix}1&1&1\\1&a&1\\1&1&a^2\end{vmatrix}=a^3-a^2-a+1=(a-1)^2(a+1)$: \ base si \ $\res{a\neq1\ \text{i}\ a\neq-1}$",
               r"Si $a=1$, els tres vectors són $(1,1,1)$: \ rang $\res{1}$. Si $a=-1$, $\vec w=\vec u$ però $\vec v=(1,-1,1)$ no és proporcional a $\vec u$: \ rang $\res{2}$."])),
 (2, r"Comprova que $\mathcal B=\{(1,1,0),(0,1,1),(1,0,1)\}$ és una base i calcula les coordenades del vector $\vec x=(3,1,2)$ en aquesta base.",
     r"El determinant val $2\neq0$: és una base. \ $a(1,1,0)+b(0,1,1)+c(1,0,1)=(3,1,2)$: \ $a+c=3$, $a+b=1$, $b+c=2$. Sumant, $a+b+c=3$, d'on $c=2$, $a=1$, $b=0$: \ $\res{\vec x=(1,0,2)_{\mathcal B}}$"),
 (2, r"Es pot escriure $(1,2,3)$ com a combinació lineal de $(1,1,0)$ i $(0,1,1)$? I $(2,5,3)$?",
     r"$a(1,1,0)+b(0,1,1)=(a,a+b,b)$. Per a $(1,2,3)$: $a=1$, $b=3$, però $a+b=4\neq2$: \ \rest{no}. Per a $(2,5,3)$: $a=2$, $b=3$ i $a+b=5$ \ \checkmark: \ $\res{(2,5,3)=2(1,1,0)+3(0,1,1)}$"),
 (3, r"Siga $\{\vec u,\vec v,\vec w\}$ una base. Estudia si són linealment independents:" + tasks(2, [r"$\{\vec u+\vec v,\ \vec v+\vec w,\ \vec u+\vec w\}$", r"$\{\vec u-\vec v,\ \vec v-\vec w,\ \vec w-\vec u\}$"])
     + recorda(r"Escriu cada vector nou amb coordenades en la base $\{\vec u,\vec v,\vec w\}$ i calcula el determinant d'aquestes coordenades."),
     tasks(1, [r"Coordenades $(1,1,0)$, $(0,1,1)$, $(1,0,1)$: determinant $2\neq0$: \ \rest{independents}.", r"La suma dels tres vectors és $\vec 0$ (el determinant de les coordenades és 0): \ \rest{dependents}."])),
]))

# =====================================================================
# 3. Producte escalar
import math
u3, v3 = [1, -2, 2], [3, 0, -4]
ck(dot(u3, v3) == -5 and n2(u3) == 9 and n2(v3) == 25 and mul(v3, F(-5, 25)) == [F(-3, 5), 0, F(4, 5)])
ang = math.degrees(math.acos(-1 / 3)); ck(abs(ang - (109 + 28 / 60 + 16 / 3600)) < 1 / 3600)
for mm in (17, -1):
    ck(4 * (4 + mm) ** 2 == 6 * (5 + mm * mm) and 4 + mm > 0)
ck(dot([2, -3, -4], [1, 2, -1]) == 0 and dot([2, -3, -4], [2, 0, 1]) == 0 and n2([2, -3, -4]) == 29)
ck(dot([1, 1, 3], [2, 1, -1]) == 0)
uu, vv, uv = 9, 16, 6
ck(uu + vv + 2 * uv == 37 and uu + vv - 2 * uv == 13 and 2 * uu + 6 * uv - uv - 3 * vv == 0)
A6, B6, C6 = [1, 1, 1], [3, 2, -1], [2, 3, 3]
ck(dot(sub(B6, A6), sub(C6, A6)) == 0 and n2(sub(B6, A6)) == n2(sub(C6, A6)) == 9)
ck(F(1, 2) + F(1, 4) + F(1, 4) == 1)
S.append(("Producte escalar", [
 (1, r"Donats $\vec u=(1,-2,2)$ i $\vec v=(3,0,-4)$, calcula:" + tasks(2, [r"$\vec u\cdot\vec v$, $|\vec u|$ i $|\vec v|$.", r"L'angle que formen.", r"La projecció escalar de $\vec u$ sobre $\vec v$.", r"El vector projecció de $\vec u$ sobre $\vec v$."]),
     tasks(2, [r"$\vec u\cdot\vec v=3-8=\res{-5}$; $|\vec u|=\res{3}$, $|\vec v|=\res{5}$", r"$\cos\alpha=\dfrac{-5}{15}=-\dfrac13\Rightarrow\res{\alpha\approx109^\circ28'16''}$",
               r"$\dfrac{\vec u\cdot\vec v}{|\vec v|}=\res{-1}$", r"$\dfrac{\vec u\cdot\vec v}{|\vec v|^2}\vec v=-\dfrac15(3,0,-4)=\res{\left(-\tfrac35,0,\tfrac45\right)}$"])),
 (2, r"Troba els vectors de mòdul $\sqrt{29}$ que són perpendiculars alhora a $(1,2,-1)$ i a $(2,0,1)$ (sense fer servir el producte vectorial).",
     r"$(x,y,z)$: \ $x+2y-z=0$, \ $2x+z=0$ $\Rightarrow$ $z=-2x$, $y=-\tfrac32x$: els vectors són proporcionals a $(2,-3,-4)$, que té mòdul $\sqrt{29}$: \ $\res{\pm(2,-3,-4)}$"),
 (2, r"Troba $m$ perquè els vectors $(2,m,1)$ i $(1,1,2)$ formen un angle de $60^\circ$.",
     r"$\cos60^\circ=\dfrac{4+m}{\sqrt{5+m^2}\,\sqrt6}=\dfrac12\Rightarrow2(4+m)=\sqrt6\sqrt{5+m^2}$. Elevant al quadrat: $m^2-16m-17=0$, \ $m=17$ o $m=-1$. Totes dues fan $4+m>0$: \ $\res{m=17\ \text{o}\ m=-1}$"),
 (2, r"Calcula els angles que forma el vector $\vec v=(2,-1,2)$ amb els eixos de coordenades. Pot haver-hi un vector que forme $45^\circ$ amb l'eix $OX$ i $60^\circ$ amb l'eix $OY$? Quin angle formaria amb l'eix $OZ$?",
     r"$\cos\alpha=\tfrac23$, $\cos\beta=-\tfrac13$, $\cos\gamma=\tfrac23$: \ $\res{\alpha=\gamma\approx48^\circ11',\ \beta\approx109^\circ28'}$. Com que $\cos^2\alpha+\cos^2\beta+\cos^2\gamma=1$: $\tfrac12+\tfrac14+\cos^2\gamma=1\Rightarrow\cos\gamma=\pm\tfrac12$: \ sí, i $\res{\gamma=60^\circ\ \text{o}\ 120^\circ}$"),
 (3, r"Sabem que $|\vec u|=3$, $|\vec v|=4$ i $\vec u\cdot\vec v=6$. Calcula:" + tasks(2, [r"L'angle que formen $\vec u$ i $\vec v$.", r"$|\vec u+\vec v|$ i $|\vec u-\vec v|$.", r"$(2\vec u-\vec v)\cdot(\vec u+3\vec v)$. Què hi observes?"])
     + recorda(r"$|\vec a|^2=\vec a\cdot\vec a$, i el producte escalar és distributiu."),
     tasks(2, [r"$\cos\alpha=\tfrac{6}{12}=\tfrac12$: \ $\res{60^\circ}$", r"$|\vec u+\vec v|^2=9+16+12=37$: $\res{\sqrt{37}}$; \ $|\vec u-\vec v|^2=9+16-12$: $\res{\sqrt{13}}$",
               r"$2\cdot9+6\cdot6-6-3\cdot16=\res{0}$: \ els vectors $2\vec u-\vec v$ i $\vec u+3\vec v$ són perpendiculars."])),
 (2, r"Demostra que el triangle de vèrtexs $A(1,1,1)$, $B(3,2,-1)$ i $C(2,3,3)$ és rectangle i isòsceles, i calcula'n els angles.",
     r"$\overrightarrow{AB}=(2,1,-2)$, $\overrightarrow{AC}=(1,2,2)$: $\overrightarrow{AB}\cdot\overrightarrow{AC}=0$ i $|\overrightarrow{AB}|=|\overrightarrow{AC}|=3$: rectangle en $A$ i isòsceles. \ Angles: \ $\res{\hat A=90^\circ,\ \hat B=\hat C=45^\circ}$"),
 (1, r"Troba $m$ perquè els vectors $(m,1,3)$ i $(2,m,-1)$ siguen perpendiculars.", r"$2m+m-3=0\Rightarrow\res{m=1}$"),
]))

# =====================================================================
# 4. Producte vectorial i mixt
ck(cross([2, -1, 3], [1, 0, -2]) == [2, 7, 1] and dot([2, 7, 1], [2, -1, 3]) == 0 and dot([2, 7, 1], [1, 0, -2]) == 0)
A7, B7, C7 = [1, 0, 1], [2, 1, 3], [0, 2, 1]
ck(cross(sub(B7, A7), sub(C7, A7)) == [-4, -2, 3] and n2([-4, -2, 3]) == 29)
A8, B8, D8 = [1, 1, 0], [3, 2, 1], [0, 3, 2]
ck(cross(sub(B8, A8), sub(D8, A8)) == [0, -5, 5] and sub(add(B8, D8), A8) == [2, 4, 3])
for k in (2, -2): ck(cross([-1, 1, 0], [-1, 0, k]) == [k, k, 1] and n2([k, k, 1]) == 9)
A9, B9, C9 = [1, 1, 1], [3, 1, 0], [1, 4, 2]
for a in range(-5, 15): ck(det3(sub(B9, A9), sub(C9, A9), sub([1, a, 3], A9)) == 2 * (7 - a))
for a in range(-5, 6): ck(det3([1, 1, -1], [0, -2, 2], [a - 1, -1, a - 1]) == -2 * a + 4)
ck(det3([1, 1, -1], [0, -2, 2], [1, -1, 1]) == 0)
S.append(("Producte vectorial i producte mixt. Àrees i volums", [
 (1, r"Siguen $\vec u=(2,-1,3)$ i $\vec v=(1,0,-2)$. Calcula $\vec u\times\vec v$ i $\vec v\times\vec u$, i comprova que $\vec u\times\vec v$ és perpendicular a $\vec u$ i a $\vec v$.",
     r"$\vec u\times\vec v=\begin{vmatrix}\vec i&\vec j&\vec k\\2&-1&3\\1&0&-2\end{vmatrix}=\res{(2,7,1)}$, \ $\vec v\times\vec u=\res{(-2,-7,-1)}$. \ $(2,7,1)\cdot(2,-1,3)=4-7+3=0$, \ $(2,7,1)\cdot(1,0,-2)=2-2=0$."),
 (2, r"Donats $A(1,0,1)$, $B(2,1,3)$ i $C(0,2,1)$, troba els vectors unitaris perpendiculars al pla que determinen i l'àrea del triangle $ABC$.",
     r"$\overrightarrow{AB}\times\overrightarrow{AC}=(1,1,2)\times(-1,2,0)=(-4,-2,3)$, de mòdul $\sqrt{29}$: \ $\res{\pm\tfrac{1}{\sqrt{29}}(-4,-2,3)}$; \ àrea $=\res{\tfrac{\sqrt{29}}{2}\ u^2}$"),
 (2, r"Els punts $A(1,1,0)$, $B(3,2,1)$ i $D(0,3,2)$ són vèrtexs del paral·lelogram $ABCD$. Calcula el vèrtex $C$ i l'àrea del paral·lelogram.",
     r"$C=B+D-A=\res{(2,4,3)}$. \ $\overrightarrow{AB}\times\overrightarrow{AD}=(2,1,1)\times(-1,2,2)=(0,-5,5)$: \ àrea $=\sqrt{50}=\res{5\sqrt2\ u^2}$"),
 (2, r"Troba $k$ perquè el triangle de vèrtexs $A(1,0,0)$, $B(0,1,0)$ i $C(0,0,k)$ tinga àrea $\tfrac32$.",
     r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-1,1,0)\times(-1,0,k)=(k,k,1)$; \ $\tfrac12\sqrt{2k^2+1}=\tfrac32\Rightarrow2k^2+1=9$: \ $\res{k=\pm2}$"),
 (2, r"Troba $a$ perquè el tetraedre de vèrtexs $A(1,1,1)$, $B(3,1,0)$, $C(1,4,2)$ i $D(1,a,3)$ tinga volum 2.",
     r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[2, 0, -1], [0, 3, 1], [0, 'a-1', 2]]) + r"=2(6-a+1)=2(7-a)$. \ $\dfrac{|2(7-a)|}{6}=2\Rightarrow|7-a|=6$: \ $\res{a=1\ \text{o}\ a=13}$"),
 (2, r"Troba $a$ perquè els punts $A(1,2,1)$, $B(2,3,0)$, $C(1,0,3)$ i $D(a,1,a)$ siguen coplanaris.",
     r"$\overrightarrow{AB}=(1,1,-1)$, $\overrightarrow{AC}=(0,-2,2)$, $\overrightarrow{AD}=(a-1,-1,a-1)$: \ $\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=-2a+4=0\Rightarrow\res{a=2}$"),
 (3, r"Sabem que $[\vec u,\vec v,\vec w]=5$. Calcula:" + tasks(3, [r"$[\vec w,\vec v,\vec u]$", r"$[2\vec u,\ \vec v-\vec w,\ 3\vec w]$", r"$[\vec u+\vec v,\ \vec v,\ \vec w]$"])
     + recorda(r"El producte mixt és un determinant: aplica'n les propietats (permutar files, treure factors, sumar a una fila una combinació de les altres)."),
     tasks(3, [r"$\res{-5}$ (hem permutat dues files)", r"$2\cdot3\,[\vec u,\vec v-\vec w,\vec w]=6\,[\vec u,\vec v,\vec w]=\res{30}$", r"$[\vec u,\vec v,\vec w]+[\vec v,\vec v,\vec w]=\res{5}$"])),
]))

# =====================================================================
# 5. Equacions de rectes i plans
A10, B10 = [2, -1, 3], [4, 0, 1]
d10 = sub(B10, A10); ck(d10 == [2, 1, -2])
for t in range(-3, 4):
    X = add(A10, mul(d10, t)); ck(X[0] - 2 * X[1] - 4 == 0 and 2 * X[1] + X[2] - 1 == 0)
ck(online(A10, d10, [0, -2, 5]) and not online(A10, d10, [6, 1, 0]))
X11, d11 = meet2([1, -1, 1, -2], [2, 1, -1, -1]); ck(d11 == [0, 1, 1] and onp([1, -1, 1, -2], [1, -1, 0]) and onp([2, 1, -1, -1], [1, -1, 0]))
ck(plane3([1, 0, 2], [2, 1, 0], [0, 3, 1]) == [5, 3, 4, -13])
ck(plane(cross([2, 1, -1], [1, 0, 3]), [2, -1, 1]) == [3, -7, -1, -12])
P13, Q13, d13 = [1, -1, 0], [-1, 2, 1], [1, 2, -1]
ck(par_(d13, [-2, -4, 2]) and not online(P13, d13, Q13) and plane(cross(d13, sub(Q13, P13)), P13) == [5, 1, 7, -4])
ck(all(onp([3, -2, 1, -6], p) for p in ([2, 0, 0], [0, -3, 0], [0, 0, 6])))
ck(F(3 * 6 * 4, 6) == 12 and all(onp([4, -2, 3, -12], p) for p in ([3, 0, 0], [0, -6, 0], [0, 0, 4])))
ck(prim(cross([1, 1, 0], [0, 1, -1])) == [1, -1, -1])
ck(plane(cross([1, 2, 0], [0, 1, 3]), [1, 0, -1]) == [6, -3, 1, -5])
ck(online([2, -1, 1], [3, 2, -1], [5, 1, 0]))
S.append(("Equacions de rectes i plans", [
 (1, r"Escriu les equacions vectorial, paramètriques, contínua i implícites de la recta $r$ que passa per $A(2,-1,3)$ i $B(4,0,1)$. Els punts $C(0,-2,5)$ i $D(6,1,0)$ són de $r$?",
     r"$\vec d=\overrightarrow{AB}=(2,1,-2)$. \ " + m(vec(A10, d10)) + r"; \quad " + m(par(A10, d10)) + r"; \quad " + m(cont(A10, d10)) + r"; \quad " + m(sy('x-2y-4=0', '2y+z-1=0'))
     + r". \ $C$: $\lambda=-1$ dona $(0,-2,5)$: \rest{$C\in r$}. \ $D$: de $x=6$ ix $\lambda=2$, però aleshores $z=-1\neq0$: \rest{$D\notin r$}."),
 (1, r"Escriu en forma paramètrica la recta $r:" + sy('x-y+z=2', '2x+y-z=1') + r"$",
     r"$\vec d=(1,-1,1)\times(2,1,-1)=(0,3,3)\parallel(0,1,1)$. Sumant les equacions: $3x=3$, $x=1$; amb $z=0$, $y=-1$: \ $\res{r:\ x=1,\ y=-1+\lambda,\ z=\lambda}$"),
 (1, r"Troba les equacions paramètriques i general del pla que passa per $A(1,0,2)$, $B(2,1,0)$ i $C(0,3,1)$.",
     r"$\overrightarrow{AB}=(1,1,-2)$, $\overrightarrow{AC}=(-1,3,-1)$: \ " + m(par2([1, 0, 2], [1, 1, -2], [-1, 3, -1]))
     + r"; \ $\vec n=\overrightarrow{AB}\times\overrightarrow{AC}=(5,3,4)$: \ $\res{5x+3y+4z-13=0}$"),
 (2, r"Troba l'equació general del pla que passa per $P(2,-1,1)$ i és paral·lel a les rectes $r:\dfrac{x-1}{2}=\dfrac y1=\dfrac{z+1}{-1}$ i $s:(x,y,z)=(0,1,0)+\mu(1,0,3)$.",
     r"$\vec n=(2,1,-1)\times(1,0,3)=(3,-7,-1)$: \ $3(x-2)-7(y+1)-(z-1)=0$, \ $\res{3x-7y-z-12=0}$"),
 (2, r"Comprova que les rectes $r:\dfrac{x-1}{1}=\dfrac{y+1}{2}=\dfrac{z}{-1}$ i $s:\dfrac{x+1}{-2}=\dfrac{y-2}{-4}=\dfrac{z-1}{2}$ són paral·leles i troba el pla que les conté.",
     r"$\vec d_s=(-2,-4,2)=-2\vec d_r$ i $Q(-1,2,1)\notin r$ ($\tfrac{-2}{1}\neq\tfrac32$): paral·leles. Pla per $P(1,-1,0)$ amb vectors $\vec d_r$ i $\overrightarrow{PQ}=(-2,3,1)$: \ $\vec n=(5,1,7)$, \ $\res{5x+y+7z-4=0}$"),
 (2, r"Escriu l'equació segmentària i la general del pla que talla els eixos en $(2,0,0)$, $(0,-3,0)$ i $(0,0,6)$. Quin volum té el tetraedre que formen el pla $4x-2y+3z=12$ i els plans coordenats?",
     r"$\dfrac x2+\dfrac{y}{-3}+\dfrac z6=1$, \ $\res{3x-2y+z-6=0}$. \ El pla $4x-2y+3z=12$ talla els eixos en $(3,0,0)$, $(0,-6,0)$ i $(0,0,4)$: \ $V=\dfrac{3\cdot6\cdot4}{6}=\res{12\ u^3}$"),
 (2, r"Troba el pla que passa per l'origen i és perpendicular a la recta $r:" + sy('x+y=1', 'y-z=2') + r"$, i la recta que passa per $A(1,2,3)$ i és perpendicular al pla $2x-y+3z=5$.",
     r"$\vec d_r=(1,1,0)\times(0,1,-1)=(-1,1,1)$, que és normal al pla: \ $\res{x-y-z=0}$. \ La recta té director $(2,-1,3)$: \ $\res{(x,y,z)=(1,2,3)+\lambda(2,-1,3)}$"),
 (1, r"Passa a forma general el pla $(x,y,z)=(1,0,-1)+\lambda(1,2,0)+\mu(0,1,3)$ i troba $a$, $b$ perquè $P(a,1,b)$ siga de la recta $\dfrac{x-2}{3}=\dfrac{y+1}{2}=\dfrac{z-1}{-1}$.",
     r"$\vec n=(1,2,0)\times(0,1,3)=(6,-3,1)$: \ $\res{6x-3y+z-5=0}$. \ $\tfrac{1+1}{2}=1$: \ $a=2+3=5$, $b=1-1=0$: \ $\res{a=5,\ b=0}$"),
]))

# =====================================================================
# 6. Posicions relatives
P14, d14 = [1, -2, 0], [2, -1, 3]
ck(pos_rr(P14, d14, [3, -3, 4], [4, -2, 6]) == 'paral·leles')
pl14 = plane(cross(d14, sub([3, -3, 4], P14)), P14); ck(onp(pl14, [3, -3, 4]) and onp(pl14, P14) and dot(pl14[:3], d14) == 0)
ck(pos_rr([1, 0, 2], [2, 1, -1], [0, 3, 1], [1, -2, 1]) == "s'encreuen" and det3([2, 1, -1], [1, -2, 1], [-1, 3, -1]) == -3)
for a in range(-3, 8):
    ck(det3([1, 2, 1], [1, 0, 1], sub([0, 1, 3], [1, 2, a])) == -2 * (3 - a) - 2)
ck(pos_rr([1, 2, 4], [1, 2, 1], [0, 1, 3], [1, 0, 1]) == 'secants' and meet_ll([1, 2, 4], [1, 2, 1], [0, 1, 3], [1, 0, 1])[2] == [F(1, 2), 1, F(7, 2)])
for k in range(-9, 10): ck(pos_rp([2, -1, 0], [1, 1, 2], [3, -1, -1, k]) == ('continguda' if k == -7 else 'paral·lels'))
X15, d15 = meet2([1, 1, -1, -1], [2, -1, 1, -2]); X15 = [F(1), F(0), F(0)]; ck(d15 == [0, 1, 1] and onp([1, 1, -1, -1], X15) and onp([2, -1, 1, -2], X15))
for mm in range(-4, 5): ck(pos_rp(X15, d15, [1, mm, 1, -2]) == ('paral·lels' if mm == -1 else 'secants'))
ck(meet_lp(X15, d15, [1, 1, 1, -2])[1] == [1, F(1, 2), F(1, 2)])
for a in range(-4, 4):
    for b in range(-3, 5):
        r_ = rank([[2, -1, 3], [4, a, 6]]); R_ = rank([[2, -1, 3, 1], [4, a, 6, b]])
        ck((r_, R_) == ((1, 1) if a == -2 and b == 2 else (1, 2) if a == -2 else (2, 2)))
X16, d16 = meet2([2, -1, 3, -1], [4, 1, 6, -2]); ck(onp([2, -1, 3, -1], [F(1, 2), 0, 0]) and onp([4, 1, 6, -2], [F(1, 2), 0, 0]) and par_(d16, [3, 0, -2]))
ck(meet_lp([2, 1, 0], [0, 1, 1], [1, 1, 1, -3])[1] == [2, 1, 0] and onp([1, 1, 1, -3], [1, 1, 1]))
S.append(("Posicions relatives de rectes i plans", [
 (1, r"Estudia la posició relativa de $r:\dfrac{x-1}{2}=\dfrac{y+2}{-1}=\dfrac z3$ i $s:(x,y,z)=(3,-3,4)+\mu(4,-2,6)$. Si són coplanàries, troba el pla que les conté.",
     r"$\vec d_s=2\vec d_r$ i $Q(3,-3,4)\notin r$ ($\tfrac22=1$ però $\tfrac43\neq1$): \ \rest{paral·leles}. Pla per $P(1,-2,0)$ amb $\vec d_r$ i $\overrightarrow{PQ}=(2,-1,4)$: \ $\res{" + pl(pl14) + "}$"),
 (1, r"Estudia la posició relativa de $r:(x,y,z)=(1,0,2)+\lambda(2,1,-1)$ i $s:(x,y,z)=(0,3,1)+\mu(1,-2,1)$.",
     r"Els directors no són proporcionals i $\big[\vec d_r,\vec d_s,\overrightarrow{PQ}\big]=" + vm([[2, 1, -1], [1, -2, 1], [-1, 3, -1]]) + r"=-3\neq0$: \ \rest{s'encreuen}."),
 (2, r"Troba $a$ perquè les rectes $r:\dfrac{x-1}{1}=\dfrac{y-2}{2}=\dfrac{z-a}{1}$ i $s:(x,y,z)=(0,1,3)+\mu(1,0,1)$ es tallen, i calcula el punt de tall.",
     r"$\overrightarrow{PQ}=(-1,-1,3-a)$: \ $\big[\vec d_r,\vec d_s,\overrightarrow{PQ}\big]=" + vm([[1, 2, 1], [1, 0, 1], [-1, -1, '3-a']]) + r"=2a-8=0\Rightarrow\res{a=4}$. \ $1+\lambda=\mu$, $2+2\lambda=1$, $4+\lambda=3+\mu$ $\Rightarrow$ $\lambda=-\tfrac12$, $\mu=\tfrac12$: \ $\res{\left(\tfrac12,1,\tfrac72\right)}$"),
 (2, r"Estudia, segons els valors de $k$, la posició relativa de $r:(x,y,z)=(2,-1,0)+\lambda(1,1,2)$ i $\pi:3x-y-z+k=0$.",
     r"$\vec n\cdot\vec d=3-1-2=0$: la recta és paral·lela al pla o hi és continguda. $P(2,-1,0)$: $6+1+k=0\iff k=-7$. \ \rest{Si $k=-7$, $r\subset\pi$; si $k\neq-7$, paral·lels.}"),
 (2, r"Estudia, segons els valors de $m$, la posició de la recta $r:" + sy('x+y-z=1', '2x-y+z=2') + r"$ i el pla $\pi:x+my+z=2$. Troba el punt de tall quan $m=1$.",
     r"$r$: $(1,\lambda,\lambda)$. \ $\vec n\cdot\vec d=(1,m,1)\cdot(0,1,1)=m+1$. \ \rest{Si $m\neq-1$, secants}; si $m=-1$, $P(1,0,0)$ dona $1\neq2$: \rest{paral·lels}. \ Per a $m=1$: $1+2\lambda=2$, $\lambda=\tfrac12$: \ $\res{\left(1,\tfrac12,\tfrac12\right)}$"),
 (2, r"Estudia la posició relativa dels plans $\pi_1:2x-y+3z=1$ i $\pi_2:4x+ay+6z=b$ segons els valors de $a$ i $b$. Per a $a=1$, $b=2$, troba la recta en què es tallen.",
     r"Si $a\neq-2$: \rest{secants}. Si $a=-2$, $b=2$: \rest{coincidents}. Si $a=-2$, $b\neq2$: \rest{paral·lels}. \ Per a $a=1$, $b=2$: $\vec d=(2,-1,3)\times(4,1,6)=(-9,0,6)\parallel(3,0,-2)$ i, amb $z=0$, $x=\tfrac12$, $y=0$: \ $\res{(x,y,z)=\left(\tfrac12,0,0\right)+\lambda(3,0,-2)}$"),
 (3, r"Troba la recta que passa per $P(1,1,1)$, és paral·lela al pla $\pi:x+y+z=0$ i talla la recta $s:(x,y,z)=(2,1,0)+\mu(0,1,1)$."
     + recorda(r"La recta buscada està continguda en el pla paral·lel a $\pi$ que passa per $P$. Talla $s$ en el punt on $s$ talla aquest pla."),
     r"Pla per $P$ paral·lel a $\pi$: $x+y+z=3$. Talla $s$: $2+1+\mu+\mu=3$, $\mu=0$: $X(2,1,0)$. \ $\overrightarrow{PX}=(1,0,-1)$: \ $\res{(x,y,z)=(1,1,1)+\lambda(1,0,-1)}$"),
]))

# =====================================================================
# 7. Tres plans
E1 = lambda a: [[1, 1, -1, 1], [2, -1, 1, 2], [1, -2, 2, a]]
ck(pos3(E1(1))[2] == 'recta' and all(pos3(E1(a))[2] == 'prisma' for a in range(-5, 6) if a != 1))
X17, d17 = meet2([1, 1, -1, -1], [2, -1, 1, -2]); ck(all(1 - 2 * t + 2 * t == 1 for t in range(3)))
E2 = lambda k: [[k, 1, 1, k], [1, k, 1, k], [1, 1, k, k]]
for k in [F(v, 2) for v in range(-10, 11)]:
    t = pos3(E2(k))[2]
    ck(t == ('coinc' if k == 1 else 'prisma' if k == -2 else 'punt'))
    if t == 'punt':
        x = k / (k + 2); ck(all(sum(fr(c) * x for c in r[:3]) == r[3] for r in E2(k)))
E3 = lambda a, b: [[1, 1, 1, 2], [1, -1, 2, 1], [3, 1, a, b]]
for a in range(0, 8):
    for b in range(0, 9):
        ck(pos3(E3(a, b))[2] == ('punt' if a != 4 else 'recta' if b == 5 else 'prisma'))
ck(pos3([[1, -1, 0, 0], [0, 1, -1, 0], [1, 0, -1, 1]])[2] == 'prisma' and pos3([[1, -1, 0, 0], [0, 1, -1, 0], [0, 0, 1, 0]])[2] == 'punt')
S.append(("Posició relativa de tres plans", [
 (2, r"Estudia, segons el valor de $a$, la posició relativa dels plans $\pi_1:x+y-z=1$, $\pi_2:2x-y+z=2$ i $\pi_3:x-2y+2z=a$. Quan tinguen una recta comuna, troba-la.",
     r"$|M|=0$ i $\mathrm{rg}\,M=2$ (de fet, la 3a fila de $M$ és la 2a menys la 1a). $\mathrm{rg}\,M^*=2\iff a=2-1=1$. \ \rest{Si $a=1$: secants en una recta; si $a\neq1$: prisma} (no hi ha dos plans paral·lels). \ Recta: \ $\res{x=1,\ y=\lambda,\ z=\lambda}$"),
 (3, r"Discuteix, segons els valors de $k$, la posició relativa dels plans $kx+y+z=k$, \ $x+ky+z=k$, \ $x+y+kz=k$, i troba el punt comú quan n'hi haja un de sol.",
     r"$|M|=(k-1)^2(k+2)$. \ \rest{Si $k\neq1,-2$: secants en un punt.} \ \rest{Si $k=1$: coincidents} (els tres són $x+y+z=1$). \ Si $k=-2$: $\mathrm{rg}\,M=2$ i, sumant les tres equacions, $0=-6$: $\mathrm{rg}\,M^*=3$ i cap parell és paral·lel: \rest{prisma}. \ Punt: per simetria $x=y=z$, i $(k+2)x=k$: \ $\res{x=y=z=\tfrac{k}{k+2}}$"),
 (2, r"Troba $a$ i $b$ perquè els plans $x+y+z=2$, $x-y+2z=1$ i $3x+y+az=b$ tinguen una recta en comú. Què passa si $a=4$ i $b\neq5$? I si $a\neq4$?",
     r"Cal que el tercer siga combinació dels dos primers: $2\pi_1+\pi_2$ dona $3x+y+4z=5$: \ $\res{a=4,\ b=5}$. \ Si $a=4$ i $b\neq5$: $\mathrm{rg}\,M=2$, $\mathrm{rg}\,M^*=3$: \rest{prisma}. \ Si $a\neq4$: \rest{secants en un punt}."),
 (2, r"Donats $\pi_1:x-y=0$ i $\pi_2:y-z=0$, escriu un pla $\pi_3$ tal que els tres plans" + tasks(2, [r"formen un prisma;", r"es tallen en un sol punt."]),
     tasks(2, [r"Ha de ser paral·lel a la recta $\pi_1\cap\pi_2$ (director $(1,1,1)$) sense contindre-la; per exemple, $\res{x-z=1}$.", r"Qualsevol pla no paral·lel a $(1,1,1)$; per exemple, $\res{z=0}$."])),
]))

# =====================================================================
# 8. Feixos de plans
r1, r2 = [1, -1, 1, -1], [2, 1, 0, -3]
X18, d18 = meet2(r1, r2)
fx = lambda la: [fr(a) + la * b for a, b in zip(r1, r2)]
ck(prim(fx(F(-1, 3))) == [1, -4, 3, 0] and onp([1, -4, 3, 0], X18) and dot([1, -4, 3], d18) == 0)
ck(all(fx(F(v, 4))[2] != 0 for v in range(-40, 41)) and r2[2] == 0)                  # cap λ: el pla paral·lel a OZ és π₂
ck(prim(fx(F(1, 2))) == [4, -1, 2, -5] and dot([4, -1, 2], [1, 2, -1]) == 0 and onp([4, -1, 2, -5], X18) and dot([4, -1, 2], d18) == 0)
ck(onp([2, -1, 2, -7], [1, -1, 2]))
for k in (6, -6): ck(abs(F(k, 2) * k * F(k, 2)) / 6 == 9)
c19 = prim([fr(a) + 2 * b for a, b in zip([1, -2, 0, -1], [0, 3, -1, -1])]); ck(c19 == [1, 4, -2, -3] and onp(c19, [1, 1, 1]) and onp(c19, [1, 0, -1]) and onp(c19, [3, 1, 2]))
S.append(("Feixos de plans", [
 (1, r"Siga $r:" + sy('x-y+z=1', '2x+y=3') + r"$. Escriu el feix de plans d'eix $r$ i troba el pla del feix que passa per l'origen.",
     r"$(x-y+z-1)+\lambda(2x+y-3)=0$. \ En $O$: $-1-3\lambda=0$, $\lambda=-\tfrac13$: \ $\res{x-4y+3z=0}$"),
 (2, r"Amb la recta $r$ de l'exercici anterior, troba el pla que conté $r$ i és paral·lel a l'eix $OZ$, i el pla que conté $r$ i és perpendicular a $\pi:x+2y-z=0$.",
     r"$\vec n=(1+2\lambda,\ -1+\lambda,\ 1)$. Paral·lel a $OZ$ vol dir $\vec n\cdot(0,0,1)=0$, és a dir, $1=0$: cap $\lambda$! El pla que perdem en el feix, $2x+y-3=0$, sí que és paral·lel a $OZ$: \ $\res{2x+y-3=0}$. \ Perpendicular a $\pi$: $\vec n\cdot(1,2,-1)=4\lambda-2=0$, $\lambda=\tfrac12$: \ $\res{4x-y+2z-5=0}$"),
 (2, r"Troba el pla paral·lel a $2x-y+2z=1$ que passa per $A(1,-1,2)$, i els plans d'aquest feix que formen amb els plans coordenats un tetraedre de volum 9.",
     r"$2x-y+2z+k=0$, \ $2+1+4+k=0$: \ $\res{2x-y+2z-7=0}$. \ El pla $2x-y+2z=k$ talla els eixos en $\left(\tfrac k2,0,0\right)$, $(0,-k,0)$, $\left(0,0,\tfrac k2\right)$: $V=\dfrac{|k|^3}{24}=9\Rightarrow|k|=6$: \ $\res{2x-y+2z=\pm6}$"),
 (2, r"Escriu la recta $r:\dfrac{x-1}{2}=\dfrac y1=\dfrac{z+1}{3}$ com a intersecció de dos plans i troba, amb el feix de plans, el pla que conté $r$ i passa per $P(1,1,1)$.",
     r"$r:" + sy('x-2y-1=0', '3y-z-1=0') + r"$; \ feix $(x-2y-1)+\lambda(3y-z-1)=0$; \ en $P$: $-2+\lambda=0$, $\lambda=2$: \ $\res{x+4y-2z-3=0}$"),
]))

# =====================================================================
# 9. Problemes i qüestions
ck(dot(cross([-2, 2, 0], [-2, 0, 2]), [1, 1, 1]) != 0 and cross([-2, 2, 0], [-2, 0, 2]) == [4, 4, 4] and onp([1, 1, 1, -2], [F(2, 3)] * 3))
t20, X20 = meet_lp([1, 2, 0], [2, 1, 3], [1, 1, 1, -12]); ck(t20 == F(3, 2) and X20 == [4, F(7, 2), F(9, 2)] and add([1, 2, 0], mul([2, 1, 3], 2)) == [5, 4, 6])
S.append(("Problemes i qüestions", [
 (2, r"Raona si són certes o falses les afirmacions següents:" + tasks(1, [r"Si $\vec u\cdot\vec v=0$ i $\vec u\times\vec v=\vec 0$, aleshores algun dels dos vectors és nul.", r"Tres vectors no nuls i perpendiculars dos a dos formen una base.",
     r"Si $[\vec u,\vec v,\vec w]=0$, algun dels tres vectors és nul.", r"Dues rectes que no tenen cap punt en comú són paral·leles.", r"Si $\vec u\times\vec v=\vec u\times\vec w$ i $\vec u\neq\vec 0$, aleshores $\vec v=\vec w$."]),
     tasks(1, [r"\rest{Certa}: si tots dos són no nuls, $\cos\alpha=0$ i $\sin\alpha=0$ alhora, impossible.", r"\rest{Certa}: no poden ser coplanaris (si $\vec w$ fóra combinació de $\vec u$ i $\vec v$, multiplicant escalarment per $\vec w$ tindríem $|\vec w|^2=0$).",
               r"\rest{Falsa}: per exemple $(1,0,0)$, $(0,1,0)$, $(1,1,0)$.", r"\rest{Falsa}: es poden encreuar.", r"\rest{Falsa}: només cal que $\vec u\times(\vec v-\vec w)=\vec 0$, és a dir, $\vec v-\vec w\parallel\vec u$; per exemple $\vec u=\vec i$, $\vec v=\vec j$, $\vec w=\vec i+\vec j$."])),
 (2, r"Un cub té un vèrtex en l'origen, tres arestes sobre els semieixos positius i aresta 2. Troba l'equació del pla que passa pels vèrtexs $A(2,0,0)$, $B(0,2,0)$ i $C(0,0,2)$, l'àrea del triangle $ABC$ i el punt on la diagonal del cub que ix de l'origen talla aquest pla.",
     r"Segmentària: $\tfrac x2+\tfrac y2+\tfrac z2=1$: \ $\res{x+y+z=2}$. \ $\overrightarrow{AB}\times\overrightarrow{AC}=(4,4,4)$: àrea $=\tfrac12\cdot4\sqrt3=\res{2\sqrt3\ u^2}$. \ Diagonal $(t,t,t)$: $3t=2$: \ $\res{\left(\tfrac23,\tfrac23,\tfrac23\right)}$"),
 (2, r"Un dron ix del punt $P(1,2,0)$ i vola en línia recta en la direcció del vector $(2,1,3)$. A la seua trajectòria hi ha la teulada inclinada d'una nau, continguda en el pla $x+y+z=12$, i un pal vertical que passa pel punt $(5,4,0)$. Amb quin dels dos obstacles topa primer?",
     r"Trajectòria: $(1+2\lambda,\ 2+\lambda,\ 3\lambda)$, $\lambda\ge0$. Teulada: $3+6\lambda=12$, $\lambda=\tfrac32$, punt $\left(4,\tfrac72,\tfrac92\right)$. Pal ($x=5$, $y=4$): $\lambda=2$ compleix les dues, punt $(5,4,6)$. \ \rest{Topa primer amb la teulada} ($\tfrac32<2$)."),
]))

SEC = {t: exs for t, exs in S}
def pau(sec, *exs): SEC[sec].extend(exs)

# =====================================================================
# PAU d'altres comunitats (recull ebaumatematicas 2026/27), sense els apartats de geometria mètrica
# ---------- 1. Vectors i aplicacions
ck(par_(sub([3, 6, 1], [1, 2, -1]), sub([0, 0, -2], [1, 2, -1])))                         # CLM: m = 0
ck(all(not par_(sub([3, 6, 1], [1, 2, -1]), sub([m_, m_, m_ - 2], [1, 2, -1])) for m_ in range(1, 9)))
A_, B_, C_ = [1, 1, 1], [4, 1, 5], [1, 10, 1]
ck(sub(add(B_, C_), A_) == [4, 10, 5] and n2(sub(B_, A_)) == 25 and n2(sub(C_, A_)) == 81 and dot(sub(B_, A_), sub(C_, A_)) == 0)
pau("Vectors a l'espai i aplicacions",
 (2, r"\pau{Castella-la Manxa, extraordinària 2026} Es consideren els punts $A(1,2,-1)$, $B(3,6,1)$ i $C(m,m,m-2)$, on $m$ és un nombre real. Determina el valor de $m$ perquè els punts $A$, $B$ i $C$ estiguen alineats.",
     r"$\overrightarrow{AB}=(2,4,2)\parallel(1,2,1)$ i $\overrightarrow{AC}=(m-1,m-2,m-1)$: cal $m-2=2(m-1)$, \ $\res{m=0}$ (i aleshores $\overrightarrow{AC}=(-1,-2,-1)$ \checkmark)."),
 (2, r"\pau{Catalunya, extraordinària 2026} L'Aina vol fer un croquis en 3D d'una capsa amb un programa informàtic. Situa un costat de la tapa des del vèrtex $A(1,1,1)$ fins al vèrtex $B(4,1,5)$, i l'altre costat de la tapa des del vèrtex $A$ fins al vèrtex $C(1,10,1)$. Quines són les coordenades del quart vèrtex de la tapa? Calcula les longituds dels dos costats de la tapa.",
     r"La tapa és el paral·lelogram de costats $AB$ i $AC$: \ $D=B+C-A=\res{(4,10,5)}$. \ $|\overrightarrow{AB}|=|(3,0,4)|=\res{5}$, \ $|\overrightarrow{AC}|=|(0,9,0)|=\res{9}$. (A més, $\overrightarrow{AB}\cdot\overrightarrow{AC}=0$: la tapa és un rectangle.)"),
)

# ---------- 4. Producte vectorial i mixt
for m_ in range(-5, 8):
    ck(det3(sub([2, m_, 1], [1, 2, 0]), sub([3, 4, 2], [1, 2, 0]), sub([1, -1, m_], [1, 2, 0])) == -2 * m_ * (m_ - 3))
ck(n2(cross([1, -1, 1], [2, 2, 2])) == 32 and det3([1, -1, 1], [2, 2, 2], [0, -3, 1]) == 4)           # m = 1: àrea 2√2, V = 2/3
for a in range(-4, 8): ck(det3([2, a - 1, -3], [1, 0, -2], [3, 2, -4]) == 4 - 2 * a)
A_, B_, C_, D_ = [1, 2, 3], [-2, 1, 4], [3, 0, 5], [0, -1, 2]
ck(det3(sub(B_, A_), sub(C_, A_), sub(D_, A_)) == -32 and cross(sub(B_, A_), sub(C_, A_)) == [0, 8, 8])
for a in [F(v, 2) for v in range(-12, 13)]: ck(det3([1, -1, a], [2, a, 1], [-1, 1, -1]) == (a + 2) * (a - 1))
ck(sorted([a for a in range(-10, 11) if abs((a + 2) * (a - 1)) == 10]) == [-4, 3])
A_, B_, C_, D_ = [1, 1, 2], [2, -1, 0], [-2, 0, 3], [2, -3, -1]
ck(det3(sub(B_, A_), sub(C_, A_), sub(D_, A_)) == -3 and cross(sub(B_, A_), sub(C_, A_)) == [-4, 5, -7] and n2([-4, 5, -7]) == 90)
A_, B_, C_ = [4, -2, -3], [2, -1, 1], [0, -3, -1]
ck(n2(sub(B_, A_)) == n2(sub(C_, A_)) == 21 and n2(sub(C_, B_)) == 12 and sub(add(B_, C_), A_) == [-2, -2, 3] and n2(cross(sub(B_, A_), sub(C_, A_))) == 216)
A_, B_, C_ = [1, 2, 3], [1, 0, -1], [2, 2, 2]
ck(add(add(sub(B_, A_), sub(C_, B_)), sub(A_, C_)) == [0, 0, 0] and n2(cross(sub(B_, A_), sub(C_, A_))) == 24)
pau("Producte vectorial i producte mixt. Àrees i volums",
 (2, r"\pau{Andalusia, ordinària 2026} Considera els punts $A(1,2,0)$, $B(2,m,1)$, $C(3,4,2)$ i $D(1,-1,m)$." + tasks(1, [r"Troba els valors de $m$ per als quals els punts són coplanaris.", r"Per a $m=1$, calcula l'àrea del triangle de vèrtexs $A$, $B$, $C$ i el volum del tetraedre de vèrtexs $A$, $B$, $C$, $D$."]),
     tasks(1, [r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[1, 'm-2', 1], [2, 2, 2], [0, -3, 'm']]) + r"=-2m^2+6m=-2m(m-3)$: \ $\res{m=0\ \text{o}\ m=3}$",
               r"$\overrightarrow{AB}\times\overrightarrow{AC}=(1,-1,1)\times(2,2,2)=(-4,0,4)$: \ àrea $=\tfrac12\sqrt{32}=\res{2\sqrt2\ u^2}$. \ El producte mixt val $-2+6=4$: \ $V=\tfrac46=\res{\tfrac23\ u^3}$"])),
 (2, r"\pau{Aragó, ordinària 2024} Donats els punts $P_1(-2,1,1)$, $P_2(0,a,-2)$, $P_3(-1,1,-1)$ i $P_4(1,3,-3)$:" + tasks(1, [r"Calcula els valors de $a$ perquè el tetraedre de vèrtexs $P_1$, $P_2$, $P_3$ i $P_4$ tinga volum $\tfrac13$.", r"Calcula el valor de $a$ perquè els quatre punts siguen coplanaris."]),
     tasks(1, [r"$\big[\overrightarrow{P_1P_2},\overrightarrow{P_1P_3},\overrightarrow{P_1P_4}\big]=" + vm([[2, 'a-1', -3], [1, 0, -2], [3, 2, -4]]) + r"=4-2a$; \ $\dfrac{|4-2a|}{6}=\dfrac13$: \ $\res{a=1\ \text{o}\ a=3}$", r"$4-2a=0$: \ $\res{a=2}$"])),
 (2, r"\pau{Astúries, ordinària 2025} Es consideren els punts $A(1,2,3)$, $B(-2,1,4)$, $C(3,0,5)$ i $D(0,-1,2)$." + tasks(1, [r"Estudia si els quatre punts són d'un mateix pla.", r"Calcula l'àrea del triangle de vèrtexs $A$, $B$ i $C$.", r"Calcula el volum del tetraedre que formen els quatre punts."]),
     tasks(1, [r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[-3, -1, 1], [2, -2, 2], [-1, -3, -1]]) + r"=-32\neq0$: \ \rest{no són coplanaris}.",
               r"$\overrightarrow{AB}\times\overrightarrow{AC}=(0,8,8)$: \ àrea $=\tfrac12\cdot8\sqrt2=\res{4\sqrt2\ u^2}$", r"$V=\tfrac{32}{6}=\res{\tfrac{16}{3}\ u^3}$"])),
 (2, r"\pau{Castella-la Manxa, ordinària 2026} Donats els vectors $\vec u=(1,-1,a)$, $\vec v=(2,a,1)$ i $\vec w=(-1,1,-1)$:" + tasks(1, [r"Troba els valors reals de $a$ perquè els tres vectors siguen coplanaris. Justifica la resposta.", r"Troba els valors reals de $a$ perquè el volum del paral·lelepípede format pels tres vectors siga $10\ u^3$."]),
     tasks(1, [r"$[\vec u,\vec v,\vec w]=" + vm([[1, -1, 'a'], [2, 'a', 1], [-1, 1, -1]]) + r"=a^2+a-2=(a+2)(a-1)$: \ $\res{a=-2\ \text{o}\ a=1}$",
               r"$|a^2+a-2|=10$: $a^2+a-12=0$ dona $\res{a=3\ \text{o}\ a=-4}$, i $a^2+a+8=0$ no té solucions reals."])),
 (2, r"\pau{Madrid, extraordinària 2025} Siguen els punts $A(1,1,2)$, $B(2,-1,0)$, $C(-2,0,3)$ i $D(2,-3,-1)$." + tasks(1, [r"Comprova que els punts no són coplanaris i calcula el volum del tetraedre que determinen.", r"Calcula l'àrea de la cara $ABC$ del tetraedre i la longitud de l'altura del tetraedre que parteix del vèrtex $D$."])
     + recorda(r"El volum d'una piràmide és un terç de l'àrea de la base per l'altura."),
     tasks(1, [r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[1, -2, -2], [-3, -1, 1], [1, -4, -3]]) + r"=-3\neq0$: no són coplanaris. \ $V=\res{\tfrac12\ u^3}$",
               r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-4,5,-7)$: \ $S=\res{\tfrac{3\sqrt{10}}{2}\ u^2}$. \ $V=\tfrac13Sh\Rightarrow h=\dfrac{3V}{S}=\dfrac{3/2}{3\sqrt{10}/2}=\res{\tfrac{\sqrt{10}}{10}\ u}$"])),
 (2, r"\pau{Navarra, ordinària 2024} Els punts $A(4,-2,-3)$, $B(2,-1,1)$ i $C(0,-3,-1)$ són vèrtexs d'un rombe." + tasks(1, [r"Troba el quart vèrtex del rombe.", r"Calcula l'àrea del rombe."]),
     tasks(1, [r"$|\overrightarrow{AB}|=|\overrightarrow{AC}|=\sqrt{21}$ i $|\overrightarrow{BC}|=\sqrt{12}$: els costats iguals són $AB$ i $AC$, i $A$ és el vèrtex comú. \ $D=B+C-A=\res{(-2,-2,3)}$",
               r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-2,1,4)\times(-4,-1,2)=(6,-12,6)$: \ àrea $=\sqrt{216}=\res{6\sqrt6\ u^2}$"])),
 (2, r"\pau{Aragó, extraordinària 2024} Siguen $A(1,2,3)$, $B(1,0,-1)$ i $C(2,2,2)$ tres punts de l'espai, $\vec v_1$ el vector que va de $A$ a $B$, $\vec v_2$ el vector que va de $B$ a $C$ i $\vec v_3$ el vector que va de $C$ a $A$." + tasks(1, [r"Estudia si els vectors $\vec v_1$, $\vec v_2$ i $\vec v_3$ són linealment independents.", r"Calcula l'àrea del triangle de vèrtexs $A$, $B$ i $C$."]),
     tasks(1, [r"$\vec v_1+\vec v_2+\vec v_3=\overrightarrow{AA}=\vec 0$: \ \rest{són linealment dependents} (sense fer cap càlcul).", r"$\overrightarrow{AB}\times\overrightarrow{AC}=(0,-2,-4)\times(1,0,-1)=(2,-4,2)$: \ àrea $=\tfrac12\sqrt{24}=\res{\sqrt6\ u^2}$"])),
)

# ---------- 5. Equacions de rectes i plans
ck(plane(cross([1, 2, 2], sub([1, 1, 1], [1, 2, 3])), [1, 1, 1]) == [2, -2, 1, -1])
X_, d_ = meet2([1, 1, 1, -1], [1, -2, 0, 0]); ck(plane(cross(d_, sub([1, 2, 3], X_)), X_) == [8, -7, 3, -3])
A_, B_, C_, D_ = [0, 3, 2], [4, 1, 3], [2, 3, 4], [0, 1, 2]
ck(abs(det3(sub(B_, A_), sub(C_, A_), sub(D_, A_))) == 12)
ck(plane3([1, 1, 0], [2, 0, 1], [0, 2, 1]) == [1, 1, 0, -2])
for a in range(-10, 12): ck(abs(det3([1, -1, 1], [-1, 1, 1], [a - 1, 0, 2])) == abs(2 - 2 * a))
A_, B_, E_ = [1, 1, 1], [0, 2, 0], [0, 0, 1]
ck(sub(mul(E_, 2), A_) == [-1, -1, 1] and sub(mul(E_, 2), B_) == [0, -2, 2] and plane3(A_, B_, E_) == [1, -1, -2, 2] and det3(A_, B_, E_) == 2)
P_, Q_, R_ = [1, 0, -1], [3, -2, 0], [1, 1, 1]
c_ = plane3(P_, Q_, R_); ck(c_ == [5, 4, -2, -7] and n2(cross(sub(Q_, P_), sub(R_, P_))) == 45)
A_, B_, C_, D_ = [4, 3, 3], [3, 3, 4], [1, 0, 4], [4, 0, 1]
ck(det3(sub(B_, A_), sub(C_, A_), sub(D_, A_)) == 0 and plane3(A_, B_, C_) == [3, -2, 3, -15] and online(A_, sub(C_, A_), [7, 6, 2]))
u_, v_ = [0, 3, -4], [12, 4, 3]
ck(dot(u_, v_) == 0 and cross(u_, v_) == [25, -48, -36] and n2(cross(u_, v_)) == 65 ** 2 and plane(cross(u_, v_), [1, 0, 0]) == [25, -48, -36, -25])
ck(plane(cross([2, 0, 1], [1, 2, -3]), [1, 0, 2]) == [2, -7, -4, 6])
pau("Equacions de rectes i plans",
 (1, r"\pau{Andalusia, ordinària 2025} Considera el punt $P(1,1,1)$ i la recta $r:\dfrac{x-1}{1}=\dfrac{y-2}{2}=\dfrac{z-3}{2}$. Troba el pla que passa pel punt $P$ i conté la recta $r$.",
     r"Pla per $P$ amb vectors $\vec d_r=(1,2,2)$ i $\overrightarrow{QP}=(0,-1,-2)$, on $Q(1,2,3)\in r$: \ $\vec n=(-2,2,-1)$: \ $\res{2x-2y+z-1=0}$"),
 (2, r"\pau{Aragó, ordinària 2025}" + tasks(1, [r"Troba les equacions paramètriques de la recta $s$ que passa pel punt $P(4,-3,0)$ i és perpendicular al pla $\pi:x-2y+z-1=0$.", r"Troba l'equació del pla que conté el punt $Q(1,2,3)$ i la recta $r:" + sy('x+y+z=1', 'x-2y=0') + r"$"]),
     tasks(1, [r"$\res{x=4+\lambda,\ y=-3-2\lambda,\ z=\lambda}$", r"$\vec d_r=(1,1,1)\times(1,-2,0)=(2,1,-3)$, $R(0,0,1)\in r$, $\overrightarrow{RQ}=(1,2,2)$: \ $\vec n=(8,-7,3)$: \ $\res{8x-7y+3z-3=0}$"])),
 (2, r"\pau{Cantàbria, extraordinària 2024} Siguen $A(0,3,2)$, $B(4,1,3)$, $C(2,3,4)$ i $D(0,1,2)$ els vèrtexs d'un tetraedre." + tasks(1, [r"Obtín l'equació vectorial del pla determinat pels punts $A$, $B$ i $C$.", r"Calcula el volum del tetraedre."]),
     tasks(1, [r"$\res{(x,y,z)=(0,3,2)+\alpha(4,-2,1)+\beta(2,0,2)}$", r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[4, -2, 1], [2, 0, 2], [0, -2, 0]]) + r"=12$: \ $V=\res{2\ u^3}$"])),
 (2, r"\pau{Castella-la Manxa, extraordinària 2026} Es consideren els punts $A(1,1,0)$, $B(2,0,1)$, $C(0,2,1)$ i $D(a,1,2)$, amb $a$ un nombre real." + tasks(1, [r"Determina l'equació del pla que passa pels punts $A$, $B$ i $C$.", r"Determina els valors de $a$ perquè el tetraedre format pels quatre punts tinga volum 3 unitats cúbiques."]),
     tasks(1, [r"$\overrightarrow{AB}\times\overrightarrow{AC}=(1,-1,1)\times(-1,1,1)=(-2,-2,0)$: \ $\res{x+y-2=0}$", r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=(-2,-2,0)\cdot(a-1,0,2)=2-2a$; \ $\tfrac{|2-2a|}{6}=3$: \ $\res{a=-8\ \text{o}\ a=10}$"])),
 (2, r"\pau{Castella i Lleó, extraordinària 2026} Els punts $A(1,1,1)$ i $B(0,2,0)$ són vèrtexs consecutius del paral·lelogram $ABCD$, que té el centre en $E(0,0,1)$." + tasks(1, [r"Calcula les coordenades dels altres vèrtexs.", r"Troba l'equació general del pla que conté el paral·lelogram.", r"Troba el volum del tetraedre de vèrtexs $A$, $B$, $E$ i l'origen de coordenades $O$."]),
     tasks(1, [r"$E$ és el punt mig de les diagonals: $C=2E-A=\res{(-1,-1,1)}$, \ $D=2E-B=\res{(0,-2,2)}$", r"$\overrightarrow{AB}\times\overrightarrow{AE}=(-1,1,-1)\times(-1,-1,0)=(-1,1,2)$: \ $\res{x-y-2z+2=0}$",
               r"$\big[\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OE}\big]=" + vm([[1, 1, 1], [0, 2, 0], [0, 0, 1]]) + r"=2$: \ $V=\res{\tfrac13\ u^3}$"])),
 (2, r"\pau{Catalunya, ordinària 2026} Considera els punts $P(1,0,-1)$, $Q(3,-2,0)$ i $R(1,1,1)$." + tasks(1, [r"Calcula l'equació del pla que conté els punts $P$, $Q$ i $R$.", r"Comprova que l'àrea del triangle $PQR$ és $\tfrac{3\sqrt5}{2}\ u^2$.", r"Determina les condicions que han de complir les coordenades d'un quart punt $S(x,y,z)$ perquè $P$, $Q$, $R$ i $S$ formen un tetraedre de volum 1."]),
     tasks(1, [r"$\overrightarrow{PQ}\times\overrightarrow{PR}=(2,-2,1)\times(0,1,2)=(-5,-4,2)$: \ $\res{5x+4y-2z-7=0}$", r"$\tfrac12|(-5,-4,2)|=\tfrac12\sqrt{45}=\tfrac{3\sqrt5}{2}$ \ \checkmark",
               r"$\tfrac16\big|(-5,-4,2)\cdot(x-1,y,z+1)\big|=1\iff|5x+4y-2z-7|=6$: $S$ ha de ser d'un dels plans \ $\res{5x+4y-2z-1=0}$ \ o \ $\res{5x+4y-2z-13=0}$"])),
 (2, r"\pau{Extremadura, extraordinària 2026} Donats els punts $A(4,3,3)$, $B(3,3,4)$, $C(1,0,4)$ i $D(4,0,1)$:" + tasks(1, [r"Justifica de forma raonada que els punts $A$, $B$, $C$ i $D$ estan en el mateix pla i troba l'equació del pla que determinen.", r"Calcula el valor de $k$ perquè el punt $P(7,k,2)$ siga de la recta $r$ que passa pels punts $A$ i $C$."]),
     tasks(1, [r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[-1, 0, 1], [-3, -3, 1], [0, -3, -2]]) + r"=0$: són coplanaris. \ $\vec n=(3,-2,3)$: \ $\res{3x-2y+3z-15=0}$", r"$r:(4-3t,\ 3-3t,\ 3+t)$; $z=2$ dona $t=-1$ i $x=7$ \checkmark: \ $\res{k=6}$"])),
 (2, r"\pau{Extremadura, ordinària 2026}" + tasks(1, [r"Donats els vectors $\vec u=(0,3,-4)$ i $\vec v=(12,4,3)$, comprova que el paral·lelogram que formen és un rectangle i calcula'n l'àrea.", r"Troba l'equació del pla format pels vectors $\vec u$ i $\vec v$ i el punt $(1,0,0)$.", r"Obtín un vector perpendicular als vectors $\vec u$ i $\vec v$ de mòdul 13."]),
     tasks(1, [r"$\vec u\cdot\vec v=0+12-12=0$: rectangle. \ $\vec u\times\vec v=(25,-48,-36)$, de mòdul $\sqrt{4225}$: \ àrea $=\res{65\ u^2}$", r"$\res{25x-48y-36z-25=0}$", r"$\pm\tfrac{13}{65}(25,-48,-36)=\res{\pm\left(5,-\tfrac{48}{5},-\tfrac{36}{5}\right)}$"])),
 (2, r"\pau{Madrid, ordinària 2025} Donats la recta $r:\dfrac{x-1}{2}=\dfrac y0=\dfrac{z-2}{1}$ i el pla $\pi:x+2y-3z=1$, troba una equació del pla que conté $r$ i és perpendicular a $\pi$.",
     r"Vectors directors $\vec d_r=(2,0,1)$ i $\vec n_\pi=(1,2,-3)$, punt $(1,0,2)$: \ $\vec n=(2,0,1)\times(1,2,-3)=(-2,7,4)$: \ $\res{2x-7y-4z+6=0}$"),
)

# ---------- 6. Posicions relatives
P_, d_ = [-1, 0, 1], [1, 1, 1]
ck(det3([0, -1, 1], [-2, 0, 2], [-2, -1, 0]) == 6 and plane3([1, 1, 1], [1, 0, 2], [-1, 1, 3]) == [1, 1, 1, -3] and meet_lp(P_, d_, [1, 1, 1, -3])[1] == [0, 1, 2])
X_, d_ = meet2([1, 1, -2, -3], [2, 1, -6, -2]); ck(par_(d_, [4, -2, 1]) and det3(d_, [1, 3, 2], sub([1, 0, -1], X_)) == 0 and plane(cross(d_, [1, 3, 2]), [1, 0, -1]) == [1, 1, -2, -3])
X_, d_ = meet2([-1, 3, -3, 3], [4, 9, -2, 2]); ck(par_(d_, [3, -2, -3]) and pos_rp(X_, d_, [2, 3, 0, 0]) == 'continguda')
X1, d1 = meet2([1, -3, 2, 2], [2, 1, -3, -3]); ck(par_(d1, [1, 1, 1]) and pos_rr(X1, d1, [1, 0, 1], [-2, 1, -2]) == "s'encreuen")
e_ = cross([1, 1, 1], [-2, 1, -2]); ck(par_(e_, [1, 0, -1]) and meet_ll([0, F(1, 2), 0], [1, 0, -1], X1, d1)[2] == [F(1, 2), F(1, 2), F(-1, 2)])
X_, d_ = meet2([1, 1, 1, 5], [1, 2, -1, 0]); ck(par_(d_, [-3, 2, 1]))
for a in range(-8, 6): ck(pos_rp(X_, d_, [2, 1, -a, -3]) == ('paral·lels' if a == -4 else 'secants'))
ck(meet_lp(X_, d_, [2, 1, -2, -3])[1] == [-1, -1, -3])
for m_ in range(-3, 10): ck(pos_rr([0, 1, 0], [4, -2, 2], [1, m_, 3], [1, m_ - 1, 3]) == 'secants' and online([1, m_, 3], [1, m_ - 1, 3], [0, 1, 0]))
for m_ in range(-6, 4): ck(pos_rp([1, 1, 0], [-1, -1, 2], [5, m_, 1, -2]) == ('continguda' if m_ == -3 else 'secants'))
ck(plane(cross([-1, -1, 2], [5, 1, 1]), [1, 1, 0]) == [3, -11, -4, 8])
ck(pos_rr([1, 2, 1], [2, -1, 1], [2, 1, 1], [4, -2, 2]) == 'paral·leles' and plane(cross([2, -1, 1], [1, -1, 0]), [1, 2, 1]) == [1, 1, -1, -2])
ck(pos_rp([2, 1, 2], [-2, 0, -1], [1, 2, -2, 0]) == 'continguda' and plane(cross([-2, 0, -1], [1, 2, -2]), [2, 1, 2]) == [2, -5, -4, 9])
ck(dot([4, 2, -4], [3, 2, 4]) == 0 and onp([4, 2, -4, -2], [2, 3, 3]))
X_, d_ = meet2([1, 1, 1, -1], [-1, -2, 1, 0]); ck(par_(d_, [3, -2, -1]))
for a in range(-3, 8): ck(pos_rp(X_, d_, [2, 1, a, -3]) == ('continguda' if a == 4 else 'secants'))
ck(onp([2, 1, 4, -3], [2, -1, 0]) and meet_lp(X_, d_, [2, 1, 0, -7])[1] == [5, -3, -1])
X_, d_ = meet2([1, 0, 2, 3], [-1, -1, 1, 4]); C_ = meet_lp(X_, d_, [2, 1, -1, -5])[1]
ck(C_ == [1, 1, -2] and n2(cross(sub([1, 1, -1], [3, 2, -1]), sub(C_, [3, 2, -1]))) == 5)
Xs, ds = meet2([2, 1, -3, -6], [2, 0, -3, -8]); c1 = prim([fr(a) + b for a, b in zip([2, 1, -3, -6], [2, 0, -3, -8])])
ck(c1 == [4, 1, -6, -14] and onp(c1, [2, 0, -1]) and plane(cross([2, 1, 1], sub([2, 0, -1], [-1, 0, -2])), [2, 0, -1]) == [1, 1, -3, -5])
ck(online(Xs, ds, [1, -2, -2]) and online([-1, 0, -2], [2, 1, 1], [3, 2, 0]) and online([2, 0, -1], [1, 2, 1], [1, -2, -2]) and online([2, 0, -1], [1, 2, 1], [3, 2, 0]))
t_ = prim(cross([4, 1, -6], [1, 1, -3])); ck(t_ == [1, 2, 1] and pos_rr([2, 0, -1], t_, [-1, 0, -2], [2, 1, 1]) == 'secants' and pos_rr([2, 0, -1], t_, Xs, ds) == 'secants')
X_, d_ = meet2([2, -1, 1, 0], [1, -1, 4, -1]); ck(par_(d_, [3, 7, 1]))
for A in range(0, 30): ck(pos_rp(X_, d_, [2, -3, A, -10]) == ('paral·lels' if A == 15 else 'secants'))
ck(meet_lp(X_, d_, [2, -3, 21, -10])[1] == [2, 5, 1])
ck(rank([[1, -2, 4], [2, -3, 6]]) == 2 and par_(meet2([1, -2, 4, 1], [2, -3, 6, 2])[1], [0, 2, 1]) and onp([1, -2, 4, 1], [-1, 0, 0]) and onp([2, -3, 6, 2], [-1, 0, 0]))
pau("Posicions relatives de rectes i plans",
 (2, r"\pau{Astúries, extraordinària 2024} Es consideren els punts $A(1,1,1)$, $B(1,0,2)$, $C(-1,1,3)$ i $D(-1,0,1)$." + tasks(1, [r"Estudia si hi ha un pla que continga els quatre punts.", r"Calcula la recta $r$ que passa per $D$ i és perpendicular al pla $\pi$ que conté $A$, $B$ i $C$.", r"Calcula el punt $P$ d'intersecció de $r$ i $\pi$."]),
     tasks(1, [r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[0, -1, 1], [-2, 0, 2], [-2, -1, 0]]) + r"=6\neq0$: \ \rest{no n'hi ha cap}.", r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-2,-2,-2)$: $\pi:x+y+z-3=0$; \ $\res{r:\dfrac{x+1}{1}=\dfrac y1=\dfrac{z-1}{1}}$",
               r"$(-1+t)+t+(1+t)-3=0$, $t=1$: \ $\res{P(0,1,2)}$"])),
 (2, r"\pau{Canàries, extraordinària 2025} Es tenen les rectes $r:" + sy('x+y-2z=3', '2x+y-6z=2') + r"$ \ i \ $s:x-1=\dfrac y3=\dfrac{z+1}{2}$." + tasks(1, [r"Comprova que $r$ i $s$ són coplanàries.", r"Troba l'equació del pla que les conté."]),
     tasks(1, [r"$\vec d_r=(1,1,-2)\times(2,1,-6)=(-4,2,-1)$, $R(-1,4,0)\in r$; $\vec d_s=(1,3,2)$, $Q(1,0,-1)$: \ $\big[\vec d_r,\vec d_s,\overrightarrow{RQ}\big]=" + vm([[-4, 2, -1], [1, 3, 2], [2, -4, -1]]) + r"=0$ \ \checkmark", r"$\vec d_r\times\vec d_s=(7,7,-14)\parallel(1,1,-2)$, per $Q$: \ $\res{x+y-2z-3=0}$"])),
 (2, r"\pau{Canàries, ordinària 2026} Es coneixen el pla $\pi:2x+3y=0$ i el punt $P(1,-5,1)$." + tasks(1, [r"Troba la recta $r$ perpendicular al pla $\pi$ que passa pel punt $P$.", r"Troba la posició relativa de la recta $s:" + sy('-x+3y-3z=-3', '4x+9y-2z=-2') + r"$ \ amb el pla $\pi$."]),
     tasks(1, [r"Director $\vec n_\pi=(2,3,0)$: \ $\res{r:\ x=1+2\lambda,\ y=-5+3\lambda,\ z=1}$", r"$\vec d_s=(-1,3,-3)\times(4,9,-2)=(21,-14,-21)\parallel(3,-2,-3)$; \ $\vec n\cdot\vec d_s=6-6=0$ i el punt $\left(1,-\tfrac23,0\right)\in s$ compleix $2-2=0$: \ \rest{$s$ està continguda en $\pi$}."])),
 (3, r"\pau{Canàries, extraordinària 2024} Considera les rectes $r_1:" + sy('x-3y+2z+2=0', '2x+y-3z=3') + r"$ \ i \ $r_2:\dfrac{1-x}{2}=y=\dfrac{1-z}{2}$." + tasks(1, [r"Estudia la posició relativa de les dues rectes.", r"Troba l'equació de la recta $s$ que té direcció perpendicular a les dues rectes i passa per $P\left(0,\tfrac12,0\right)$. Calcula el punt de tall de $s$ amb $r_1$."]),
     tasks(1, [r"$\vec d_1=(7,7,7)\parallel(1,1,1)$, $P_1(1,1,0)$; \ $\vec d_2=(-2,1,-2)$, $P_2(1,0,1)$: \ $\big[\vec d_1,\vec d_2,\overrightarrow{P_1P_2}\big]=" + vm([[1, 1, 1], [-2, 1, -2], [0, -1, 1]]) + r"=3\neq0$: \ \rest{s'encreuen}.",
               r"$\vec d_1\times\vec d_2=(-3,0,3)\parallel(1,0,-1)$: \ $s:\left(\lambda,\tfrac12,-\lambda\right)$. Amb $r_1:(1+\mu,1+\mu,\mu)$: $\mu=-\tfrac12$, $\lambda=\tfrac12$: \ $\res{\left(\tfrac12,\tfrac12,-\tfrac12\right)}$"])),
 (2, r"\pau{Cantàbria, ordinària 2024} Considera la recta $r:" + sy('x+y+z+5=0', 'x+2y-z=0') + r"$ \ i el pla $\pi:2x+y-az=3$. Raona si és possible donar algun valor al paràmetre $a$ perquè:" + tasks(1, [r"la recta estiga continguda en el pla;", r"la recta i el pla siguen paral·lels;", r"la recta i el pla es tallen. En cas afirmatiu, dona un valor de $a$ i calcula on es tallen."]),
     r"$\vec d_r=(1,1,1)\times(1,2,-1)=(-3,2,1)$, $R(-10,5,0)\in r$; \ $\vec n\cdot\vec d=-6+2-a=-4-a$. Si $a=-4$, $R$ dona $-15\neq3$." + tasks(1, [r"\rest{Cap valor de $a$.}", r"\rest{$a=-4$.}", r"\rest{Qualsevol $a\neq-4$}; per exemple, amb $a=2$ es tallen en $\res{(-1,-1,-3)}$."])),
 (2, r"\pau{Castella i Lleó, ordinària 2025} Siguen les rectes $r:\dfrac x4=\dfrac{y-1}{-2}=\dfrac z2$ i $s:x-1=\dfrac{y-m}{m-1}=\dfrac{z-3}{3}$." + tasks(1, [r"Comprova que les rectes $r$ i $s$ es tallen per a qualsevol valor de $m$.", r"Per a $m=6$, troba el punt d'intersecció de les rectes $r$ i $s$."]),
     tasks(1, [r"$P(0,1,0)\in r$, $Q(1,m,3)$: $\overrightarrow{PQ}=(1,m-1,3)=\vec d_s$, així que $\big[\vec d_r,\vec d_s,\overrightarrow{PQ}\big]=0$, i $\vec d_r=(4,-2,2)$ no és paral·lel a $\vec d_s$: \rest{secants per a tot $m$}. (De fet, $Q-\vec d_s=P$: el punt $P$ és de $s$.)", r"$\res{(0,1,0)}$ (per a qualsevol $m$)."])),
 (2, r"\pau{Castella i Lleó, extraordinària 2025} Siguen el pla $\pi:5x+my+z=2$ i la recta $r:(x,y,z)=(1,1,0)+t(-1,-1,2)$." + tasks(1, [r"Determina la posició relativa de $r$ i $\pi$ en funció de $m$.", r"Per a $m=1$, calcula el pla $\pi'$ que conté $r$ i és perpendicular a $\pi$."]),
     tasks(1, [r"$\vec n\cdot\vec d=-5-m+2=-3-m$; $P(1,1,0)$: $5+m=2\iff m=-3$. Si $m=-3$: \rest{$r\subset\pi$}; si $m\neq-3$: \rest{secants}.", r"$\vec n'=(-1,-1,2)\times(5,1,1)=(-3,11,4)$: \ $\res{3x-11y-4z+8=0}$"])),
 (1, r"\pau{Galícia, extraordinària 2025} Donades les rectes" + dm(r"r:\dfrac{x-1}{2}=\dfrac{y-2}{-1}=\dfrac{z-1}{1}\qquad\text{i}\qquad s:\dfrac{x-2}{4}=\dfrac{y-1}{-2}=\dfrac{z-1}{2}") + r"" + tasks(1, [r"Calcula la posició relativa de les rectes $r$ i $s$.", r"Obtín l'equació del pla que conté les rectes $r$ i $s$."]),
     tasks(1, [r"$\vec d_s=2\vec d_r$ i $Q(2,1,1)\notin r$: \ \rest{paral·leles}.", r"$\vec n=(2,-1,1)\times\overrightarrow{PQ}=(2,-1,1)\times(1,-1,0)=(1,1,-1)$: \ $\res{x+y-z-2=0}$"])),
 (2, r"\pau{Galícia, extraordinària 2024} Considera el pla $\pi:x+2y-2z=0$ i la recta $r$ que passa pels punts $A(2,1,2)$ i $B(0,1,1)$." + tasks(1, [r"Estudia la posició relativa de la recta $r$ i el pla $\pi$.", r"Obtín l'equació implícita o general del pla que conté $r$ i és perpendicular a $\pi$."]),
     tasks(1, [r"$\vec d=(-2,0,-1)$: $\vec n\cdot\vec d=-2+2=0$ i $A$: $2+2-4=0$: \ \rest{$r$ està continguda en $\pi$}.", r"$\vec n'=(-2,0,-1)\times(1,2,-2)=(2,-5,-4)$: \ $\res{2x-5y-4z+9=0}$"])),
 (1, r"\pau{Galícia, ordinària 2024} Considera el pla $\pi:4x+2y+bz=2$ i la recta $r:\dfrac{x-2}{3}=\dfrac{y-c}{2}=\dfrac{z-3}{4}$, on $b$ i $c$ són paràmetres reals. Calcula els valors de $b$ i $c$ perquè la recta $r$ estiga continguda en $\pi$.",
     r"$\vec n\cdot\vec d=12+4+4b=0\Rightarrow b=-4$; el punt $(2,c,3)$ ha de ser de $\pi$: $8+2c-12=2$: \ $\res{b=-4,\ c=3}$"),
 (2, r"\pau{Múrcia, extraordinària 2025} Considera la recta $r:" + sy('x+y+z=1', '-x-2y+z=0') + r"$ \ i el pla $\pi:2x+y+az=b$." + tasks(1, [r"Determina els valors de $a$ i $b$ perquè el pla contínga la recta.", r"Per a quins valors de $a$ i $b$ la recta talla el pla? Troba el punt de tall en el cas $a=0$, $b=7$."]),
     tasks(1, [r"$\vec d=(3,-2,-1)$, $R(2,-1,0)\in r$: $\vec n\cdot\vec d=4-a=0$ i $4-1=b$: \ $\res{a=4,\ b=3}$", r"\rest{Si $a\neq4$} (qualsevol $b$). Amb $a=0$, $b=7$: $2(2+3t)+(-1-2t)=7$, $t=1$: \ $\res{(5,-3,-1)}$"])),
 (2, r"\pau{Navarra, extraordinària 2024} Es consideren el pla $\pi:2x+y-z-5=0$, la recta $r:" + sy('x+2z+3=0', '-x-y+z+4=0') + r"$ \ i els punts $A(3,2,-1)$ i $B(1,1,-1)$. Siga $C$ la intersecció de la recta i el pla." + tasks(1, [r"Demostra que els punts $A$, $B$ i $C$ no estan alineats.", r"Calcula l'àrea del triangle que formen els tres punts."]),
     tasks(1, [r"$r:(-3+2t,\ 7-3t,\ t)$; en $\pi$: $2t-4=0$, $C(1,1,-2)$. \ $\overrightarrow{AB}\times\overrightarrow{AC}=(-2,-1,0)\times(-2,-1,-1)=(1,-2,0)\neq\vec 0$: \ \rest{no alineats}.", r"$\tfrac12|(1,-2,0)|=\res{\tfrac{\sqrt5}{2}\ u^2}$"])),
 (3, r"\pau{Navarra, ordinària 2025} Calcula l'equació contínua de la recta $t$ que passa pel punt $P(2,0,-1)$ i talla les rectes $s:" + sy('2x+y-3z-6=0', '2x-3z-8=0') + r"$ \ i \ $r:\dfrac{x+1}{2}=\dfrac y1=\dfrac{z+2}{1}$."
     + recorda(r"La recta $t$ és la intersecció del pla que conté $P$ i $s$ amb el pla que conté $P$ i $r$."),
     r"Pla per $P$ que conté $s$ (feix): $(2x+y-3z-6)+\lambda(2x-3z-8)=0$; en $P$: $1-\lambda=0$: $4x+y-6z-14=0$. \ Pla per $P$ que conté $r$: $\vec n=(2,1,1)\times(3,0,1)=(1,1,-3)$: $x+y-3z-5=0$. \ $\vec d_t=(4,1,-6)\times(1,1,-3)=(3,6,3)$: \ $\res{t:\dfrac{x-2}{1}=\dfrac y2=\dfrac{z+1}{1}}$ \ (talla $r$ en $(3,2,0)$ i $s$ en $(1,-2,-2)$)."),
 (2, r"\pau{País Basc, extraordinària 2024} Es consideren la recta $r:" + sy('2x-y+z=0', 'x-y+4z=1') + r"$ \ i el pla $\pi:2x-3y+Az=10$." + tasks(1, [r"Calcula el valor del paràmetre $A$ perquè la recta $r$ i el pla $\pi$ siguen paral·lels.", r"Si $A=21$, calcula la intersecció del pla $\pi$ i la recta $r$."]),
     tasks(1, [r"$\vec d=(2,-1,1)\times(1,-1,4)=(-3,-7,-1)$: $\vec n\cdot\vec d=-6+21-A=0$, $A=15$; i $(-1,-2,0)\in r$ dona $4\neq10$: \ $\res{A=15}$", r"$\res{(2,5,1)}$"])),
 (1, r"\pau{Aragó, ordinària 2026} Siguen els plans $\pi:x-2y+4z+1=0$ i $\pi_d:2x-3y+6z=d$, amb $d\in\mathbb R$." + tasks(1, [r"Hi ha algun valor de $d$ per al qual els plans $\pi$ i $\pi_d$ no es tallen?", r"Calcula, per a $d=-2$, els punts de tall entre els plans $\pi$ i $\pi_d$."]),
     tasks(1, [r"Els vectors normals $(1,-2,4)$ i $(2,-3,6)$ no són proporcionals: \ \rest{no; sempre es tallen en una recta}.", r"$\vec d=(0,2,1)$ i, amb $z=0$, $(-1,0,0)$: \ $\res{x=-1,\ y=2\lambda,\ z=\lambda}$"])),
)

# ---------- 7. Tres plans
E_ = lambda a: [[1, 1, 1, 1], [a - 1, 1, 1, a], [1, a - 1, -1, 0]]
for a in [F(v, 2) for v in range(-8, 13)]:
    ck(det3(*[r[:3] for r in E_(a)]) == a * (a - 2))
    t = pos3(E_(a))[2]
    ck(t == ('2coinc' if a == 0 else '2par' if a == 2 else 'punt'))
    if t == 'punt': ck(all(sum(fr(c) * x for c, x in zip(r[:3], [(a - 1) / (a - 2), 1 / (2 - a), 0])) == r[3] for r in E_(a)))
ck(all(all(sum(fr(c) * x for c, x in zip(r[:3], [F(1, 2), F(1, 2) - l, l])) == r[3] for r in E_(0)) for l in range(-3, 4)))
pau("Posició relativa de tres plans",
 (3, r"\pau{La Rioja, extraordinària 2026} Determina els valors de $a$ perquè els plans $\pi_1:x+y+z=1$, \ $\pi_2:(a-1)x+y+z=a$ \ i \ $\pi_3:x+(a-1)y-z=0$" + tasks(1, [r"es tallen en un punt. En aquest cas, determina el punt de tall.", r"es tallen en una recta. En aquest cas, determina la recta en forma paramètrica."]),
     r"$|M|=" + vm([[1, 1, 1], ['a-1', 1, 1], [1, 'a-1', -1]]) + r"=a(a-2)$." + tasks(1, [r"\rest{Si $a\neq0$ i $a\neq2$.} Restant $\pi_1$ de $\pi_2$: $(a-2)x=a-1$; \ $\res{\left(\tfrac{a-1}{a-2},\ \tfrac{1}{2-a},\ 0\right)}$",
     r"Si $a=0$: $\pi_2:-x+y+z=0$ i $\pi_3:x-y-z=0$ són coincidents i tallen $\pi_1$: \ \rest{$a=0$}, \ $\res{x=\tfrac12,\ y=\tfrac12-\lambda,\ z=\lambda}$. \ (Si $a=2$, $\pi_1\parallel\pi_2$: no hi ha cap punt comú.)"])),
)

# ---------- 8. Feixos de plans
ck(prim([fr(a) + 4 * b for a, b in zip([2, 1, -1, -4], [1, 1, -2, -3])]) == [6, 5, -9, -16] and onp([6, 5, -9, -16], [-2, 2, -2]))
X_ = [0, 1, 2]; ck(onp([1, -3, -2, 7], X_) and X_ == [0, 1 - 2 * 0, 2 + 0])
c_ = prim([fr(a) - F(3, 2) * b for a, b in zip([1, 1, -2, 0], [2, -3, 1, -1])]); ck(c_ == [4, -11, 7, -3] and onp(c_, X_))
pau("Feixos de plans",
 (2, r"\pau{Múrcia, extraordinària 2026} Determina l'equació del pla que conté el punt $P(-2,2,-2)$ i la recta $r$ donada com a intersecció de dos plans: \ $r:" + sy('2x+y-z=4', 'x+y-2z=3') + r"$",
     r"Feix: $(2x+y-z-4)+\lambda(x+y-2z-3)=0$; en $P$: $-4+\lambda=0$, $\lambda=4$: \ $\res{6x+5y-9z-16=0}$"),
 (2, r"\pau{País Basc, ordinària 2025} Es consideren les rectes $r_1:" + sy('x+y-2z=0', '2x-3y+z=1') + r"$ \ i \ $r_2:" + sy('x=3t', 'y=1-2t', 'z=2+t') + r"$ \ Calcula l'equació del pla que conté $r_1$ i passa pel punt d'intersecció del pla $\pi:x-3y-2z+7=0$ i la recta $r_2$.",
     r"$r_2\cap\pi$: $3t-3(1-2t)-2(2+t)+7=7t=0$, punt $(0,1,2)$. \ Feix: $(x+y-2z)+\lambda(2x-3y+z-1)=0$; en $(0,1,2)$: $-3-2\lambda=0$, $\lambda=-\tfrac32$: \ $\res{4x-11y+7z-3=0}$"),
)

# ---------- 9. Problemes
A_, B_, C_, D_ = [-2, 3, 120], [20, 42, 120], [-1, 4, 165], [20, 43, 165]
ck(det3(sub(B_, A_), sub(C_, A_), sub(D_, A_)) == -1755)
ck(det3([1, 2, 3], [3, 2, 1], [5, 4, 3]) == 0 and prim(cross([2, 1, 1], [4, 3, 1])) == [1, -1, -1] and onp([1, -1, -1, 0], [1, 1, 0]))
M1_, M2_, M3_ = [2, 3, 6], [4, 4, 5], [5, 1, 4]
ck(plane3(M1_, M2_, M3_) == [4, -1, 7, -47])
T = [[3, 8, F(17, 2)], [4, 6, F(37, 4)], [2, 8, 8]]
ck(plane3(*T) == [4, -1, -8, 64] and onp([4, -1, -8, 64], [4, 16, 8]) and all(not onp([4, -1, -8, 64], [s_, 16, 8]) for s_ in range(-5, 12) if s_ != 4))
pau("Problemes i qüestions",
 (2, r"\pau{Aragó, extraordinària 2026} Estem reparant una cadira metàl·lica que coixejava, perquè els extrems inferiors de les seues quatre potes no recolzaven alhora en un terra pla. La cadira està tombada sobre una taula de treball de 120 cm d'altura i té quatre potes de 45 cm de longitud cadascuna. Després de la reparació, els extrems inferiors de les potes estan situats en els punts $A(-2,3,120)$, $B(20,42,120)$, $C(-1,4,165)$ i $D(20,43,165)$. Quan baixem la cadira de la taula i la deixem en el terra, coixejarà o recolzarà les quatre potes sobre el terra pla del taller?",
     r"Les quatre potes recolzen si els quatre extrems són coplanaris: \ $\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[22, 39, 0], [1, 1, 45], [22, 40, 45]]) + r"=-1755\neq0$: \ \rest{no són coplanaris: la cadira coixejarà}."),
 (2, r"\pau{Illes Balears, extraordinària 2026} En un estudi d'astronomia es modelitza una constel·lació artificial de satèl·lits que orbiten al voltant de la Terra. Prenem un sistema de coordenades amb l'origen en el centre de la Terra (les unitats són desenes de milers de quilòmetres) i hi situem cinc satèl·lits: $A(1,2,3)$, $B(3,2,1)$, $C(5,4,3)$, $D(2,1,1)$ i $E(4,3,1)$. Diem que uns satèl·lits formen un pla orbital si, juntament amb el centre de la Terra, són coplanaris."
     + tasks(1, [r"Determina si els satèl·lits $A$, $B$ i $C$ formen un pla orbital.", r"Proporciona un punt $F$ (diferent de l'origen) on es podria col·locar un sisè satèl·lit perquè els satèl·lits $D$, $E$ i $F$ formen un altre pla orbital."]),
     tasks(1, [r"$\big[\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC}\big]=" + vm([[1, 2, 3], [3, 2, 1], [5, 4, 3]]) + r"=0$: \ \rest{sí}.", r"El pla $ODE$ té normal $(2,1,1)\times(4,3,1)=(-2,2,2)$: $x-y-z=0$. Qualsevol punt d'aquest pla (no alineat amb $O$, $D$, $E$); per exemple, \ $\res{F(1,1,0)}$"])),
 (2, r"\pau{Illes Balears, ordinària 2026} En un estudi de gravació s'han penjat del sostre tres micròfons per a gravar un concert acústic. Prenem un sistema de referència amb l'origen en el terra de la sala; el sostre és a 7 m d'altura. El micròfon $M_1$ té coordenades $x=2$, $y=3$ i penja d'un cable de 1 m; el micròfon $M_2$ té $x=4$, $y=4$ i penja d'un cable de 2 m, i el micròfon $M_3$ té $x=5$, $y=1$ i penja d'un cable de 3 m. Determina les coordenades dels tres micròfons i calcula l'equació del pla que els conté.",
     r"$\res{M_1(2,3,6),\ M_2(4,4,5),\ M_3(5,1,4)}$. \ $\overrightarrow{M_1M_2}\times\overrightarrow{M_1M_3}=(2,1,-1)\times(3,-2,-2)=(-4,1,-7)$: \ $\res{4x-y+7z-47=0}$"),
 (2, r"\pau{La Rioja, ordinària 2026} En un xiringuito de platja s'instal·la un tendal per als clients. El tendal es col·loca en els punts de suport $\left(3,8,\tfrac{17}{2}\right)$, $\left(4,6,\tfrac{37}{4}\right)$, $(2,8,8)$ i $(s,16,8)$, amb $s\in\mathbb R$." + tasks(1, [r"Determina l'equació del pla que conté el tendal.", r"Calcula el valor de $s$ perquè els quatre punts siguen coplanaris."]),
     tasks(1, [r"Vectors $\left(1,-2,\tfrac34\right)$ i $\left(-1,0,-\tfrac12\right)$; el seu producte vectorial és proporcional a $(4,-1,-8)$: \ $\res{4x-y-8z+64=0}$", r"$4s-16-64+64=0$: \ $\res{s=4}$"])),
)

# =====================================================================
print(NCHK[0], 'comprovacions correctes')
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={vectors, producte escalar, producte vectorial, producte mixt, àrees, volums, equacions de la recta, equacions del pla, posicions relatives, feixos de plans, PAU}"
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

TIT = "Vectors i aplicacions. Rectes, plans i feixos de plans"
# espai fi després de les comes de les ternes de coordenades: (1,-2,3) -> (1,\,-2,\,3)
TRI = re.compile(r'\((-?[\w\\{}.+\-]+),(-?[\w\\{}.+\-]+),(-?[\w\\{}.+\-]+)\)')
# i les equacions amb fraccions (equació contínua…) no es parteixen entre dues línies
INL = re.compile(r'(?<![\\$])\$([^$]+)\$')
def esp(t):
    t = TRI.sub(lambda mm: '(' + r',\,'.join(mm.groups()) + ')', t)
    return INL.sub(lambda mm: r'\mbox{$' + mm.group(1) + '$}' if r'\dfrac' in mm.group(1) and len(mm.group(1)) < 260 else mm.group(0), t)
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 3: %s. 2n de Batxillerat MII}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 3: Vectors, rectes i plans · 2n Batxillerat MII" % t)
    assert 'MII}' in p and '2n Batxillerat MII' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques II}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 3' if sol else "Fitxa d'exercicis · Unitat 3") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Una recta o un pla es poden escriure de moltes maneres: si el teu punt o el teu vector director són diferents, comprova que el punt és de la recta (o del pla) i que els vectors són proporcionals. Pots comprovar els resultats amb les eines interactives dels apunts."
             if sol else r"Resol els exercicis al quadern justificant cada pas. Fes un esbós quan t'ajude a veure la situació i comprova sempre els resultats (que el punt trobat és dels plans, que el vector normal és perpendicular als vectors directors\ldots). Els exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat d'altres comunitats autònomes (2024--2026), traduïts al valencià; n'hem tret els apartats d'angles i distàncies, que són de la unitat següent.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb les eines 3D dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't3-fitxa-solucions.tex' if sol else 't3-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
print(n, 'exercicis,', npau, 'de la PAU d\'altres comunitats')
