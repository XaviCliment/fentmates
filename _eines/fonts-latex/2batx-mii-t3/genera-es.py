# Versió en castellà de genera.py. Genera t3-fitxa-exercicis-es.tex i t3-fitxa-solucions-es.tex (2n Batxillerat Matemàtiques II, Unitat 3: Vectors i aplicacions.
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
S.append(("Vectores en el espacio y aplicaciones", [
 (1, r"Sean $A(1,-2,3)$, $B(3,-1,1)$ y $C(-1,2,7)$." + tasks(2, [r"Calcula $\overrightarrow{AB}$, $\overrightarrow{AC}$ y sus módulos.", r"Halla un vector unitario con la dirección y el sentido de $\overrightarrow{AC}$.",
     r"Halla un vector de módulo 9 paralelo a $\overrightarrow{AB}$ y de sentido contrario.", r"Calcula $3\overrightarrow{AB}+\overrightarrow{AC}$."]),
     tasks(2, [r"$\overrightarrow{AB}=(2,1,-2)$, $|\overrightarrow{AB}|=\sqrt{9}=\res{3}$; \ $\overrightarrow{AC}=(-2,4,4)$, $|\overrightarrow{AC}|=\sqrt{36}=\res{6}$",
               r"$\dfrac{\overrightarrow{AC}}{6}=\res{\left(-\tfrac13,\tfrac23,\tfrac23\right)}$", r"$-3\,\overrightarrow{AB}=\res{(-6,-3,6)}$", r"$\res{(4,7,-2)}$"])),
 (1, r"El punto medio del segmento $AB$ es $M(1,-2,4)$ y $A(3,0,-1)$. Calcula $B$. Halla también el simétrico de $P(2,-3,1)$ respecto del punto $Q(0,1,-2)$."
     + recorda(r"El punto medio de $A$ y $B$ es $M=\frac{A+B}{2}$; por tanto, $B=2M-A$. El simétrico de un punto respecto de otro se calcula igual."),
     r"$B=2M-A=\res{(-1,-4,9)}$. \qquad $P'=2Q-P=\res{(-2,5,-5)}$"),
 (2, r"Divide en tres partes iguales el segmento de extremos $A(-2,1,5)$ y $B(4,-5,-1)$.",
     r"$\overrightarrow{AB}=(6,-6,-6)$, \ $\tfrac13\overrightarrow{AB}=(2,-2,-2)$: \ $P_1=A+\tfrac13\overrightarrow{AB}=\res{(0,-1,3)}$, \ $P_2=A+\tfrac23\overrightarrow{AB}=\res{(2,-3,1)}$"),
 (2, r"Halla $a$ y $b$ para que los puntos $A(1,0,2)$, $B(2,1,0)$ y $C(a,3,b)$ estén alineados.",
     r"$\overrightarrow{AB}=(1,1,-2)$ y $\overrightarrow{AC}=(a-1,3,b-2)$ deben ser proporcionales: $\dfrac{a-1}{1}=\dfrac31=\dfrac{b-2}{-2}$ \ $\Rightarrow$ \ $\res{a=4,\ b=-4}$"),
 (2, r"Los puntos $A(1,2,-1)$, $B(3,0,2)$ y $C(2,-1,4)$ son tres vértices consecutivos del paralelogramo $ABCD$. Calcula el cuarto vértice $D$ y el centro del paralelogramo.",
     r"$\overrightarrow{AD}=\overrightarrow{BC}$: \ $D=A+C-B=\res{(0,1,1)}$. Las diagonales se cortan en el punto medio: \ centro $=\dfrac{A+C}{2}=\res{\left(\tfrac32,\tfrac12,\tfrac32\right)}$"),
 (2, r"El baricentro del triángulo $ABC$ es $G(1,2,0)$, con $A(2,1,-3)$ y $B(-1,4,2)$. Halla el vértice $C$.",
     r"$G=\dfrac{A+B+C}{3}\Rightarrow C=3G-A-B=(3-2+1,\ 6-1-4,\ 0+3-2)=\res{(2,1,1)}$"),
 (2, r"Halla el punto $P$ del segmento $AB$, con $A(1,-1,2)$ y $B(7,5,-4)$, que cumple $\overline{AP}=2\,\overline{PB}$.",
     r"$P$ está a dos tercios del segmento desde $A$: \ $P=A+\tfrac23\overrightarrow{AB}=(1,-1,2)+\tfrac23(6,6,-6)=\res{(5,3,-2)}$"),
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
S.append(("Dependencia lineal y bases", [
 (1, r"Estudia si los vectores $\vec u=(1,2,-1)$, $\vec v=(2,1,3)$ y $\vec w=(0,3,-5)$ son linealmente independientes. Si no lo son, escribe $\vec w$ como combinación lineal de $\vec u$ y $\vec v$.",
     r"$" + vm([u2, v2, w2]) + r"=1(-5-9)-2(-10-0)-1(6-0)=0$: \ \rest{linealmente dependientes}. \ $\vec w=a\vec u+b\vec v$: \ $a+2b=0$, $2a+b=3$ $\Rightarrow$ $a=2$, $b=-1$, y la tercera se cumple ($-2-3=-5$): \ $\res{\vec w=2\vec u-\vec v}$"),
 (2, r"Considera los vectores $\vec u=(1,1,1)$, $\vec v=(1,a,1)$ y $\vec w=(1,1,a^2)$." + tasks(1, [r"¿Para qué valores de $a$ forman una base de $\mathbb R^3$?", r"Calcula el rango del conjunto $\{\vec u,\vec v,\vec w\}$ para los demás valores de $a$."]),
     tasks(1, [r"$" + r"\begin{vmatrix}1&1&1\\1&a&1\\1&1&a^2\end{vmatrix}=a^3-a^2-a+1=(a-1)^2(a+1)$: \ base si \ $\res{a\neq1\ \text{y}\ a\neq-1}$",
               r"Si $a=1$, los tres vectores son $(1,1,1)$: \ rango $\res{1}$. Si $a=-1$, $\vec w=\vec u$ pero $\vec v=(1,-1,1)$ no es proporcional a $\vec u$: \ rango $\res{2}$."])),
 (2, r"Comprueba que $\mathcal B=\{(1,1,0),(0,1,1),(1,0,1)\}$ es una base y calcula las coordenadas del vector $\vec x=(3,1,2)$ en esta base.",
     r"El determinante vale $2\neq0$: es una base. \ $a(1,1,0)+b(0,1,1)+c(1,0,1)=(3,1,2)$: \ $a+c=3$, $a+b=1$, $b+c=2$. Sumando, $a+b+c=3$, de donde $c=2$, $a=1$, $b=0$: \ $\res{\vec x=(1,0,2)_{\mathcal B}}$"),
 (2, r"¿Se puede escribir $(1,2,3)$ como combinación lineal de $(1,1,0)$ y $(0,1,1)$? ¿Y $(2,5,3)$?",
     r"$a(1,1,0)+b(0,1,1)=(a,a+b,b)$. Para $(1,2,3)$: $a=1$, $b=3$, pero $a+b=4\neq2$: \ \rest{no}. Para $(2,5,3)$: $a=2$, $b=3$ y $a+b=5$ \ \checkmark: \ $\res{(2,5,3)=2(1,1,0)+3(0,1,1)}$"),
 (3, r"Sea $\{\vec u,\vec v,\vec w\}$ una base. Estudia si son linealmente independientes:" + tasks(2, [r"$\{\vec u+\vec v,\ \vec v+\vec w,\ \vec u+\vec w\}$", r"$\{\vec u-\vec v,\ \vec v-\vec w,\ \vec w-\vec u\}$"])
     + recorda(r"Escribe cada vector nuevo con coordenadas en la base $\{\vec u,\vec v,\vec w\}$ y calcula el determinante de estas coordenadas."),
     tasks(1, [r"Coordenadas $(1,1,0)$, $(0,1,1)$, $(1,0,1)$: determinante $2\neq0$: \ \rest{independientes}.", r"La suma de los tres vectores es $\vec 0$ (el determinante de las coordenadas es 0): \ \rest{dependientes}."])),
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
S.append(("Producto escalar", [
 (1, r"Dados $\vec u=(1,-2,2)$ y $\vec v=(3,0,-4)$, calcula:" + tasks(2, [r"$\vec u\cdot\vec v$, $|\vec u|$ y $|\vec v|$.", r"El ángulo que forman.", r"La proyección escalar de $\vec u$ sobre $\vec v$.", r"El vector proyección de $\vec u$ sobre $\vec v$."]),
     tasks(2, [r"$\vec u\cdot\vec v=3-8=\res{-5}$; $|\vec u|=\res{3}$, $|\vec v|=\res{5}$", r"$\cos\alpha=\dfrac{-5}{15}=-\dfrac13\Rightarrow\res{\alpha\approx109^\circ28'16''}$",
               r"$\dfrac{\vec u\cdot\vec v}{|\vec v|}=\res{-1}$", r"$\dfrac{\vec u\cdot\vec v}{|\vec v|^2}\vec v=-\dfrac15(3,0,-4)=\res{\left(-\tfrac35,0,\tfrac45\right)}$"])),
 (2, r"Halla los vectores de módulo $\sqrt{29}$ que son perpendiculares a la vez a $(1,2,-1)$ y a $(2,0,1)$ (sin utilizar el producto vectorial).",
     r"$(x,y,z)$: \ $x+2y-z=0$, \ $2x+z=0$ $\Rightarrow$ $z=-2x$, $y=-\tfrac32x$: los vectores son proporcionales a $(2,-3,-4)$, que tiene módulo $\sqrt{29}$: \ $\res{\pm(2,-3,-4)}$"),
 (2, r"Halla $m$ para que los vectores $(2,m,1)$ y $(1,1,2)$ formen un ángulo de $60^\circ$.",
     r"$\cos60^\circ=\dfrac{4+m}{\sqrt{5+m^2}\,\sqrt6}=\dfrac12\Rightarrow2(4+m)=\sqrt6\sqrt{5+m^2}$. Elevando al cuadrado: $m^2-16m-17=0$, \ $m=17$ o $m=-1$. Ambas hacen $4+m>0$: \ $\res{m=17\ \text{o}\ m=-1}$"),
 (2, r"Calcula los ángulos que forma el vector $\vec v=(2,-1,2)$ con los ejes de coordenadas. ¿Puede haber un vector que forme $45^\circ$ con el eje $OX$ y $60^\circ$ con el eje $OY$? ¿Qué ángulo formaría con el eje $OZ$?",
     r"$\cos\alpha=\tfrac23$, $\cos\beta=-\tfrac13$, $\cos\gamma=\tfrac23$: \ $\res{\alpha=\gamma\approx48^\circ11',\ \beta\approx109^\circ28'}$. Como $\cos^2\alpha+\cos^2\beta+\cos^2\gamma=1$: $\tfrac12+\tfrac14+\cos^2\gamma=1\Rightarrow\cos\gamma=\pm\tfrac12$: \ sí, y $\res{\gamma=60^\circ\ \text{o}\ 120^\circ}$"),
 (3, r"Sabemos que $|\vec u|=3$, $|\vec v|=4$ y $\vec u\cdot\vec v=6$. Calcula:" + tasks(2, [r"El ángulo que forman $\vec u$ y $\vec v$.", r"$|\vec u+\vec v|$ y $|\vec u-\vec v|$.", r"$(2\vec u-\vec v)\cdot(\vec u+3\vec v)$. ¿Qué observas?"])
     + recorda(r"$|\vec a|^2=\vec a\cdot\vec a$, y el producto escalar es distributivo."),
     tasks(2, [r"$\cos\alpha=\tfrac{6}{12}=\tfrac12$: \ $\res{60^\circ}$", r"$|\vec u+\vec v|^2=9+16+12=37$: $\res{\sqrt{37}}$; \ $|\vec u-\vec v|^2=9+16-12$: $\res{\sqrt{13}}$",
               r"$2\cdot9+6\cdot6-6-3\cdot16=\res{0}$: \ los vectores $2\vec u-\vec v$ y $\vec u+3\vec v$ son perpendiculares."])),
 (2, r"Demuestra que el triángulo de vértices $A(1,1,1)$, $B(3,2,-1)$ y $C(2,3,3)$ es rectángulo e isósceles, y calcula sus ángulos.",
     r"$\overrightarrow{AB}=(2,1,-2)$, $\overrightarrow{AC}=(1,2,2)$: $\overrightarrow{AB}\cdot\overrightarrow{AC}=0$ y $|\overrightarrow{AB}|=|\overrightarrow{AC}|=3$: rectángulo en $A$ e isósceles. \ Ángulos: \ $\res{\hat A=90^\circ,\ \hat B=\hat C=45^\circ}$"),
 (1, r"Halla $m$ para que los vectores $(m,1,3)$ y $(2,m,-1)$ sean perpendiculares.", r"$2m+m-3=0\Rightarrow\res{m=1}$"),
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
S.append(("Producto vectorial y producto mixto. Áreas y volúmenes", [
 (1, r"Sean $\vec u=(2,-1,3)$ y $\vec v=(1,0,-2)$. Calcula $\vec u\times\vec v$ y $\vec v\times\vec u$, y comprueba que $\vec u\times\vec v$ es perpendicular a $\vec u$ y a $\vec v$.",
     r"$\vec u\times\vec v=\begin{vmatrix}\vec i&\vec j&\vec k\\2&-1&3\\1&0&-2\end{vmatrix}=\res{(2,7,1)}$, \ $\vec v\times\vec u=\res{(-2,-7,-1)}$. \ $(2,7,1)\cdot(2,-1,3)=4-7+3=0$, \ $(2,7,1)\cdot(1,0,-2)=2-2=0$."),
 (2, r"Dados $A(1,0,1)$, $B(2,1,3)$ y $C(0,2,1)$, halla los vectores unitarios perpendiculares al plano que determinan y el área del triángulo $ABC$.",
     r"$\overrightarrow{AB}\times\overrightarrow{AC}=(1,1,2)\times(-1,2,0)=(-4,-2,3)$, de módulo $\sqrt{29}$: \ $\res{\pm\tfrac{1}{\sqrt{29}}(-4,-2,3)}$; \ área $=\res{\tfrac{\sqrt{29}}{2}\ u^2}$"),
 (2, r"Los puntos $A(1,1,0)$, $B(3,2,1)$ y $D(0,3,2)$ son vértices del paralelogramo $ABCD$. Calcula el vértice $C$ y el área del paralelogramo.",
     r"$C=B+D-A=\res{(2,4,3)}$. \ $\overrightarrow{AB}\times\overrightarrow{AD}=(2,1,1)\times(-1,2,2)=(0,-5,5)$: \ área $=\sqrt{50}=\res{5\sqrt2\ u^2}$"),
 (2, r"Halla $k$ para que el triángulo de vértices $A(1,0,0)$, $B(0,1,0)$ y $C(0,0,k)$ tenga área $\tfrac32$.",
     r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-1,1,0)\times(-1,0,k)=(k,k,1)$; \ $\tfrac12\sqrt{2k^2+1}=\tfrac32\Rightarrow2k^2+1=9$: \ $\res{k=\pm2}$"),
 (2, r"Halla $a$ para que el tetraedro de vértices $A(1,1,1)$, $B(3,1,0)$, $C(1,4,2)$ y $D(1,a,3)$ tenga volumen 2.",
     r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[2, 0, -1], [0, 3, 1], [0, 'a-1', 2]]) + r"=2(6-a+1)=2(7-a)$. \ $\dfrac{|2(7-a)|}{6}=2\Rightarrow|7-a|=6$: \ $\res{a=1\ \text{o}\ a=13}$"),
 (2, r"Halla $a$ para que los puntos $A(1,2,1)$, $B(2,3,0)$, $C(1,0,3)$ y $D(a,1,a)$ sean coplanarios.",
     r"$\overrightarrow{AB}=(1,1,-1)$, $\overrightarrow{AC}=(0,-2,2)$, $\overrightarrow{AD}=(a-1,-1,a-1)$: \ $\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=-2a+4=0\Rightarrow\res{a=2}$"),
 (3, r"Sabemos que $[\vec u,\vec v,\vec w]=5$. Calcula:" + tasks(3, [r"$[\vec w,\vec v,\vec u]$", r"$[2\vec u,\ \vec v-\vec w,\ 3\vec w]$", r"$[\vec u+\vec v,\ \vec v,\ \vec w]$"])
     + recorda(r"El producto mixto es un determinante: aplica sus propiedades (permutar filas, sacar factores, sumar a una fila una combinación de las otras)."),
     tasks(3, [r"$\res{-5}$ (hemos permutado dos filas)", r"$2\cdot3\,[\vec u,\vec v-\vec w,\vec w]=6\,[\vec u,\vec v,\vec w]=\res{30}$", r"$[\vec u,\vec v,\vec w]+[\vec v,\vec v,\vec w]=\res{5}$"])),
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
S.append(("Ecuaciones de rectas y planos", [
 (1, r"Escribe las ecuaciones vectorial, paramétricas, continua e implícitas de la recta $r$ que pasa por $A(2,-1,3)$ y $B(4,0,1)$. ¿Los puntos $C(0,-2,5)$ y $D(6,1,0)$ son de $r$?",
     r"$\vec d=\overrightarrow{AB}=(2,1,-2)$. \ " + m(vec(A10, d10)) + r"; \quad " + m(par(A10, d10)) + r"; \quad " + m(cont(A10, d10)) + r"; \quad " + m(sy('x-2y-4=0', '2y+z-1=0'))
     + r". \ $C$: $\lambda=-1$ da $(0,-2,5)$: \rest{$C\in r$}. \ $D$: de $x=6$ sale $\lambda=2$, pero entonces $z=-1\neq0$: \rest{$D\notin r$}."),
 (1, r"Escribe en forma paramétrica la recta $r:" + sy('x-y+z=2', '2x+y-z=1') + r"$",
     r"$\vec d=(1,-1,1)\times(2,1,-1)=(0,3,3)\parallel(0,1,1)$. Sumando las ecuaciones: $3x=3$, $x=1$; con $z=0$, $y=-1$: \ $\res{r:\ x=1,\ y=-1+\lambda,\ z=\lambda}$"),
 (1, r"Halla las ecuaciones paramétricas y general del plano que pasa por $A(1,0,2)$, $B(2,1,0)$ y $C(0,3,1)$.",
     r"$\overrightarrow{AB}=(1,1,-2)$, $\overrightarrow{AC}=(-1,3,-1)$: \ " + m(par2([1, 0, 2], [1, 1, -2], [-1, 3, -1]))
     + r"; \ $\vec n=\overrightarrow{AB}\times\overrightarrow{AC}=(5,3,4)$: \ $\res{5x+3y+4z-13=0}$"),
 (2, r"Halla la ecuación general del plano que pasa por $P(2,-1,1)$ y es paralelo a las rectas $r:\dfrac{x-1}{2}=\dfrac y1=\dfrac{z+1}{-1}$ y $s:(x,y,z)=(0,1,0)+\mu(1,0,3)$.",
     r"$\vec n=(2,1,-1)\times(1,0,3)=(3,-7,-1)$: \ $3(x-2)-7(y+1)-(z-1)=0$, \ $\res{3x-7y-z-12=0}$"),
 (2, r"Comprueba que las rectas $r:\dfrac{x-1}{1}=\dfrac{y+1}{2}=\dfrac{z}{-1}$ y $s:\dfrac{x+1}{-2}=\dfrac{y-2}{-4}=\dfrac{z-1}{2}$ son paralelas y halla el plano que las contiene.",
     r"$\vec d_s=(-2,-4,2)=-2\vec d_r$ y $Q(-1,2,1)\notin r$ ($\tfrac{-2}{1}\neq\tfrac32$): paralelas. Plano por $P(1,-1,0)$ con vectores $\vec d_r$ y $\overrightarrow{PQ}=(-2,3,1)$: \ $\vec n=(5,1,7)$, \ $\res{5x+y+7z-4=0}$"),
 (2, r"Escribe la ecuación segmentaria y la general del plano que corta los ejes en $(2,0,0)$, $(0,-3,0)$ y $(0,0,6)$. ¿Qué volumen tiene el tetraedro que forman el plano $4x-2y+3z=12$ y los planos coordenados?",
     r"$\dfrac x2+\dfrac{y}{-3}+\dfrac z6=1$, \ $\res{3x-2y+z-6=0}$. \ El plano $4x-2y+3z=12$ corta los ejes en $(3,0,0)$, $(0,-6,0)$ y $(0,0,4)$: \ $V=\dfrac{3\cdot6\cdot4}{6}=\res{12\ u^3}$"),
 (2, r"Halla el plano que pasa por el origen y es perpendicular a la recta $r:" + sy('x+y=1', 'y-z=2') + r"$, y la recta que pasa por $A(1,2,3)$ y es perpendicular al plano $2x-y+3z=5$.",
     r"$\vec d_r=(1,1,0)\times(0,1,-1)=(-1,1,1)$, que es normal al plano: \ $\res{x-y-z=0}$. \ La recta tiene vector director $(2,-1,3)$: \ $\res{(x,y,z)=(1,2,3)+\lambda(2,-1,3)}$"),
 (1, r"Pasa a forma general el plano $(x,y,z)=(1,0,-1)+\lambda(1,2,0)+\mu(0,1,3)$ y halla $a$, $b$ para que $P(a,1,b)$ sea de la recta $\dfrac{x-2}{3}=\dfrac{y+1}{2}=\dfrac{z-1}{-1}$.",
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
S.append(("Posiciones relativas de rectas y planos", [
 (1, r"Estudia la posición relativa de $r:\dfrac{x-1}{2}=\dfrac{y+2}{-1}=\dfrac z3$ y $s:(x,y,z)=(3,-3,4)+\mu(4,-2,6)$. Si son coplanarias, halla el plano que las contiene.",
     r"$\vec d_s=2\vec d_r$ y $Q(3,-3,4)\notin r$ ($\tfrac22=1$ pero $\tfrac43\neq1$): \ \rest{paralelas}. Plano por $P(1,-2,0)$ con $\vec d_r$ y $\overrightarrow{PQ}=(2,-1,4)$: \ $\res{" + pl(pl14) + "}$"),
 (1, r"Estudia la posición relativa de $r:(x,y,z)=(1,0,2)+\lambda(2,1,-1)$ y $s:(x,y,z)=(0,3,1)+\mu(1,-2,1)$.",
     r"Los vectores directores no son proporcionales y $\big[\vec d_r,\vec d_s,\overrightarrow{PQ}\big]=" + vm([[2, 1, -1], [1, -2, 1], [-1, 3, -1]]) + r"=-3\neq0$: \ \rest{se cruzan}."),
 (2, r"Halla $a$ para que las rectas $r:\dfrac{x-1}{1}=\dfrac{y-2}{2}=\dfrac{z-a}{1}$ y $s:(x,y,z)=(0,1,3)+\mu(1,0,1)$ se corten, y calcula el punto de corte.",
     r"$\overrightarrow{PQ}=(-1,-1,3-a)$: \ $\big[\vec d_r,\vec d_s,\overrightarrow{PQ}\big]=" + vm([[1, 2, 1], [1, 0, 1], [-1, -1, '3-a']]) + r"=2a-8=0\Rightarrow\res{a=4}$. \ $1+\lambda=\mu$, $2+2\lambda=1$, $4+\lambda=3+\mu$ $\Rightarrow$ $\lambda=-\tfrac12$, $\mu=\tfrac12$: \ $\res{\left(\tfrac12,1,\tfrac72\right)}$"),
 (2, r"Estudia, según los valores de $k$, la posición relativa de $r:(x,y,z)=(2,-1,0)+\lambda(1,1,2)$ y $\pi:3x-y-z+k=0$.",
     r"$\vec n\cdot\vec d=3-1-2=0$: la recta es paralela al plano o está contenida en él. $P(2,-1,0)$: $6+1+k=0\iff k=-7$. \ \rest{Si $k=-7$, $r\subset\pi$; si $k\neq-7$, paralelos.}"),
 (2, r"Estudia, según los valores de $m$, la posición de la recta $r:" + sy('x+y-z=1', '2x-y+z=2') + r"$ y el plano $\pi:x+my+z=2$. Halla el punto de corte cuando $m=1$.",
     r"$r$: $(1,\lambda,\lambda)$. \ $\vec n\cdot\vec d=(1,m,1)\cdot(0,1,1)=m+1$. \ \rest{Si $m\neq-1$, secantes}; si $m=-1$, $P(1,0,0)$ da $1\neq2$: \rest{paralelos}. \ Para $m=1$: $1+2\lambda=2$, $\lambda=\tfrac12$: \ $\res{\left(1,\tfrac12,\tfrac12\right)}$"),
 (2, r"Estudia la posición relativa de los planos $\pi_1:2x-y+3z=1$ y $\pi_2:4x+ay+6z=b$ según los valores de $a$ y $b$. Para $a=1$, $b=2$, halla la recta en la que se cortan.",
     r"Si $a\neq-2$: \rest{secantes}. Si $a=-2$, $b=2$: \rest{coincidentes}. Si $a=-2$, $b\neq2$: \rest{paralelos}. \ Para $a=1$, $b=2$: $\vec d=(2,-1,3)\times(4,1,6)=(-9,0,6)\parallel(3,0,-2)$ y, con $z=0$, $x=\tfrac12$, $y=0$: \ $\res{(x,y,z)=\left(\tfrac12,0,0\right)+\lambda(3,0,-2)}$"),
 (3, r"Halla la recta que pasa por $P(1,1,1)$, es paralela al plano $\pi:x+y+z=0$ y corta a la recta $s:(x,y,z)=(2,1,0)+\mu(0,1,1)$."
     + recorda(r"La recta buscada está contenida en el plano paralelo a $\pi$ que pasa por $P$. Corta a $s$ en el punto donde $s$ corta a este plano."),
     r"Plano por $P$ paralelo a $\pi$: $x+y+z=3$. Corta a $s$: $2+1+\mu+\mu=3$, $\mu=0$: $X(2,1,0)$. \ $\overrightarrow{PX}=(1,0,-1)$: \ $\res{(x,y,z)=(1,1,1)+\lambda(1,0,-1)}$"),
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
S.append(("Posición relativa de tres planos", [
 (2, r"Estudia, según el valor de $a$, la posición relativa de los planos $\pi_1:x+y-z=1$, $\pi_2:2x-y+z=2$ y $\pi_3:x-2y+2z=a$. Cuando tengan una recta común, hállala.",
     r"$|M|=0$ y $\mathrm{rg}\,M=2$ (de hecho, la 3.ª fila de $M$ es la 2.ª menos la 1.ª). $\mathrm{rg}\,M^*=2\iff a=2-1=1$. \ \rest{Si $a=1$: secantes en una recta; si $a\neq1$: prisma} (no hay dos planos paralelos). \ Recta: \ $\res{x=1,\ y=\lambda,\ z=\lambda}$"),
 (3, r"Discute, según los valores de $k$, la posición relativa de los planos $kx+y+z=k$, \ $x+ky+z=k$, \ $x+y+kz=k$, y halla el punto común cuando haya uno solo.",
     r"$|M|=(k-1)^2(k+2)$. \ \rest{Si $k\neq1,-2$: secantes en un punto.} \ \rest{Si $k=1$: coincidentes} (los tres son $x+y+z=1$). \ Si $k=-2$: $\mathrm{rg}\,M=2$ y, sumando las tres ecuaciones, $0=-6$: $\mathrm{rg}\,M^*=3$ y ningún par es paralelo: \rest{prisma}. \ Punto: por simetría $x=y=z$, y $(k+2)x=k$: \ $\res{x=y=z=\tfrac{k}{k+2}}$"),
 (2, r"Halla $a$ y $b$ para que los planos $x+y+z=2$, $x-y+2z=1$ y $3x+y+az=b$ tengan una recta en común. ¿Qué pasa si $a=4$ y $b\neq5$? ¿Y si $a\neq4$?",
     r"Hace falta que el tercero sea combinación de los dos primeros: $2\pi_1+\pi_2$ da $3x+y+4z=5$: \ $\res{a=4,\ b=5}$. \ Si $a=4$ y $b\neq5$: $\mathrm{rg}\,M=2$, $\mathrm{rg}\,M^*=3$: \rest{prisma}. \ Si $a\neq4$: \rest{secantes en un punto}."),
 (2, r"Dados $\pi_1:x-y=0$ y $\pi_2:y-z=0$, escribe un plano $\pi_3$ tal que los tres planos" + tasks(2, [r"formen un prisma;", r"se corten en un solo punto."]),
     tasks(2, [r"Debe ser paralelo a la recta $\pi_1\cap\pi_2$ (vector director $(1,1,1)$) sin contenerla; por ejemplo, $\res{x-z=1}$.", r"Cualquier plano no paralelo a $(1,1,1)$; por ejemplo, $\res{z=0}$."])),
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
S.append(("Haces de planos", [
 (1, r"Sea $r:" + sy('x-y+z=1', '2x+y=3') + r"$. Escribe el haz de planos de arista $r$ y halla el plano del haz que pasa por el origen.",
     r"$(x-y+z-1)+\lambda(2x+y-3)=0$. \ En $O$: $-1-3\lambda=0$, $\lambda=-\tfrac13$: \ $\res{x-4y+3z=0}$"),
 (2, r"Con la recta $r$ del ejercicio anterior, halla el plano que contiene a $r$ y es paralelo al eje $OZ$, y el plano que contiene a $r$ y es perpendicular a $\pi:x+2y-z=0$.",
     r"$\vec n=(1+2\lambda,\ -1+\lambda,\ 1)$. Paralelo a $OZ$ quiere decir $\vec n\cdot(0,0,1)=0$, es decir, $1=0$: ¡ningún $\lambda$! El plano que perdemos en el haz, $2x+y-3=0$, sí es paralelo a $OZ$: \ $\res{2x+y-3=0}$. \ Perpendicular a $\pi$: $\vec n\cdot(1,2,-1)=4\lambda-2=0$, $\lambda=\tfrac12$: \ $\res{4x-y+2z-5=0}$"),
 (2, r"Halla el plano paralelo a $2x-y+2z=1$ que pasa por $A(1,-1,2)$, y los planos de este haz que forman con los planos coordenados un tetraedro de volumen 9.",
     r"$2x-y+2z+k=0$, \ $2+1+4+k=0$: \ $\res{2x-y+2z-7=0}$. \ El plano $2x-y+2z=k$ corta los ejes en $\left(\tfrac k2,0,0\right)$, $(0,-k,0)$, $\left(0,0,\tfrac k2\right)$: $V=\dfrac{|k|^3}{24}=9\Rightarrow|k|=6$: \ $\res{2x-y+2z=\pm6}$"),
 (2, r"Escribe la recta $r:\dfrac{x-1}{2}=\dfrac y1=\dfrac{z+1}{3}$ como intersección de dos planos y halla, con el haz de planos, el plano que contiene a $r$ y pasa por $P(1,1,1)$.",
     r"$r:" + sy('x-2y-1=0', '3y-z-1=0') + r"$; \ haz $(x-2y-1)+\lambda(3y-z-1)=0$; \ en $P$: $-2+\lambda=0$, $\lambda=2$: \ $\res{x+4y-2z-3=0}$"),
]))

# =====================================================================
# 9. Problemes i qüestions
ck(dot(cross([-2, 2, 0], [-2, 0, 2]), [1, 1, 1]) != 0 and cross([-2, 2, 0], [-2, 0, 2]) == [4, 4, 4] and onp([1, 1, 1, -2], [F(2, 3)] * 3))
t20, X20 = meet_lp([1, 2, 0], [2, 1, 3], [1, 1, 1, -12]); ck(t20 == F(3, 2) and X20 == [4, F(7, 2), F(9, 2)] and add([1, 2, 0], mul([2, 1, 3], 2)) == [5, 4, 6])
S.append(("Problemas y cuestiones", [
 (2, r"Razona si son ciertas o falsas las afirmaciones siguientes:" + tasks(1, [r"Si $\vec u\cdot\vec v=0$ y $\vec u\times\vec v=\vec 0$, entonces alguno de los dos vectores es nulo.", r"Tres vectores no nulos y perpendiculares dos a dos forman una base.",
     r"Si $[\vec u,\vec v,\vec w]=0$, alguno de los tres vectores es nulo.", r"Dos rectas que no tienen ningún punto en común son paralelas.", r"Si $\vec u\times\vec v=\vec u\times\vec w$ y $\vec u\neq\vec 0$, entonces $\vec v=\vec w$."]),
     tasks(1, [r"\rest{Cierta}: si ambos son no nulos, $\cos\alpha=0$ y $\sin\alpha=0$ a la vez, imposible.", r"\rest{Cierta}: no pueden ser coplanarios (si $\vec w$ fuera combinación de $\vec u$ y $\vec v$, multiplicando escalarmente por $\vec w$ tendríamos $|\vec w|^2=0$).",
               r"\rest{Falsa}: por ejemplo $(1,0,0)$, $(0,1,0)$, $(1,1,0)$.", r"\rest{Falsa}: se pueden cruzar.", r"\rest{Falsa}: basta con que $\vec u\times(\vec v-\vec w)=\vec 0$, es decir, $\vec v-\vec w\parallel\vec u$; por ejemplo $\vec u=\vec i$, $\vec v=\vec j$, $\vec w=\vec i+\vec j$."])),
 (2, r"Un cubo tiene un vértice en el origen, tres aristas sobre los semiejes positivos y arista 2. Halla la ecuación del plano que pasa por los vértices $A(2,0,0)$, $B(0,2,0)$ y $C(0,0,2)$, el área del triángulo $ABC$ y el punto donde la diagonal del cubo que sale del origen corta este plano.",
     r"Segmentaria: $\tfrac x2+\tfrac y2+\tfrac z2=1$: \ $\res{x+y+z=2}$. \ $\overrightarrow{AB}\times\overrightarrow{AC}=(4,4,4)$: área $=\tfrac12\cdot4\sqrt3=\res{2\sqrt3\ u^2}$. \ Diagonal $(t,t,t)$: $3t=2$: \ $\res{\left(\tfrac23,\tfrac23,\tfrac23\right)}$"),
 (2, r"Un dron sale del punto $P(1,2,0)$ y vuela en línea recta en la dirección del vector $(2,1,3)$. En su trayectoria están el tejado inclinado de una nave, contenido en el plano $x+y+z=12$, y un poste vertical que pasa por el punto $(5,4,0)$. ¿Con cuál de los dos obstáculos choca primero?",
     r"Trayectoria: $(1+2\lambda,\ 2+\lambda,\ 3\lambda)$, $\lambda\ge0$. Tejado: $3+6\lambda=12$, $\lambda=\tfrac32$, punto $\left(4,\tfrac72,\tfrac92\right)$. Poste ($x=5$, $y=4$): $\lambda=2$ cumple ambas, punto $(5,4,6)$. \ \rest{Choca primero con el tejado} ($\tfrac32<2$)."),
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
pau("Vectores en el espacio y aplicaciones",
 (2, r"\pau{Castilla-La Mancha, extraordinaria 2026} Se consideran los puntos $A(1,2,-1)$, $B(3,6,1)$ y $C(m,m,m-2)$, donde $m$ es un número real. Determina el valor de $m$ para que los puntos $A$, $B$ y $C$ estén alineados.",
     r"$\overrightarrow{AB}=(2,4,2)\parallel(1,2,1)$ y $\overrightarrow{AC}=(m-1,m-2,m-1)$: hace falta $m-2=2(m-1)$, \ $\res{m=0}$ (y entonces $\overrightarrow{AC}=(-1,-2,-1)$ \checkmark)."),
 (2, r"\pau{Cataluña, extraordinaria 2026} Ana quiere hacer un croquis en 3D de una caja con un programa informático. Sitúa un lado de la tapa desde el vértice $A(1,1,1)$ hasta el vértice $B(4,1,5)$, y el otro lado de la tapa desde el vértice $A$ hasta el vértice $C(1,10,1)$. ¿Cuáles son las coordenadas del cuarto vértice de la tapa? Calcula las longitudes de los dos lados de la tapa.",
     r"La tapa es el paralelogramo de lados $AB$ y $AC$: \ $D=B+C-A=\res{(4,10,5)}$. \ $|\overrightarrow{AB}|=|(3,0,4)|=\res{5}$, \ $|\overrightarrow{AC}|=|(0,9,0)|=\res{9}$. (Además, $\overrightarrow{AB}\cdot\overrightarrow{AC}=0$: la tapa es un rectángulo.)"),
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
pau("Producto vectorial y producto mixto. Áreas y volúmenes",
 (2, r"\pau{Andalucía, ordinaria 2026} Considera los puntos $A(1,2,0)$, $B(2,m,1)$, $C(3,4,2)$ y $D(1,-1,m)$." + tasks(1, [r"Halla los valores de $m$ para los que los puntos son coplanarios.", r"Para $m=1$, calcula el área del triángulo de vértices $A$, $B$, $C$ y el volumen del tetraedro de vértices $A$, $B$, $C$, $D$."]),
     tasks(1, [r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[1, 'm-2', 1], [2, 2, 2], [0, -3, 'm']]) + r"=-2m^2+6m=-2m(m-3)$: \ $\res{m=0\ \text{o}\ m=3}$",
               r"$\overrightarrow{AB}\times\overrightarrow{AC}=(1,-1,1)\times(2,2,2)=(-4,0,4)$: \ área $=\tfrac12\sqrt{32}=\res{2\sqrt2\ u^2}$. \ El producto mixto vale $-2+6=4$: \ $V=\tfrac46=\res{\tfrac23\ u^3}$"])),
 (2, r"\pau{Aragón, ordinaria 2024} Dados los puntos $P_1(-2,1,1)$, $P_2(0,a,-2)$, $P_3(-1,1,-1)$ y $P_4(1,3,-3)$:" + tasks(1, [r"Calcula los valores de $a$ para que el tetraedro de vértices $P_1$, $P_2$, $P_3$ y $P_4$ tenga volumen $\tfrac13$.", r"Calcula el valor de $a$ para que los cuatro puntos sean coplanarios."]),
     tasks(1, [r"$\big[\overrightarrow{P_1P_2},\overrightarrow{P_1P_3},\overrightarrow{P_1P_4}\big]=" + vm([[2, 'a-1', -3], [1, 0, -2], [3, 2, -4]]) + r"=4-2a$; \ $\dfrac{|4-2a|}{6}=\dfrac13$: \ $\res{a=1\ \text{o}\ a=3}$", r"$4-2a=0$: \ $\res{a=2}$"])),
 (2, r"\pau{Asturias, ordinaria 2025} Se consideran los puntos $A(1,2,3)$, $B(-2,1,4)$, $C(3,0,5)$ y $D(0,-1,2)$." + tasks(1, [r"Estudia si los cuatro puntos pertenecen a un mismo plano.", r"Calcula el área del triángulo de vértices $A$, $B$ y $C$.", r"Calcula el volumen del tetraedro que forman los cuatro puntos."]),
     tasks(1, [r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[-3, -1, 1], [2, -2, 2], [-1, -3, -1]]) + r"=-32\neq0$: \ \rest{no son coplanarios}.",
               r"$\overrightarrow{AB}\times\overrightarrow{AC}=(0,8,8)$: \ área $=\tfrac12\cdot8\sqrt2=\res{4\sqrt2\ u^2}$", r"$V=\tfrac{32}{6}=\res{\tfrac{16}{3}\ u^3}$"])),
 (2, r"\pau{Castilla-La Mancha, ordinaria 2026} Dados los vectores $\vec u=(1,-1,a)$, $\vec v=(2,a,1)$ y $\vec w=(-1,1,-1)$:" + tasks(1, [r"Halla los valores reales de $a$ para que los tres vectores sean coplanarios. Justifica la respuesta.", r"Halla los valores reales de $a$ para que el volumen del paralelepípedo formado por los tres vectores sea $10\ u^3$."]),
     tasks(1, [r"$[\vec u,\vec v,\vec w]=" + vm([[1, -1, 'a'], [2, 'a', 1], [-1, 1, -1]]) + r"=a^2+a-2=(a+2)(a-1)$: \ $\res{a=-2\ \text{o}\ a=1}$",
               r"$|a^2+a-2|=10$: $a^2+a-12=0$ da $\res{a=3\ \text{o}\ a=-4}$, y $a^2+a+8=0$ no tiene soluciones reales."])),
 (2, r"\pau{Madrid, extraordinaria 2025} Sean los puntos $A(1,1,2)$, $B(2,-1,0)$, $C(-2,0,3)$ y $D(2,-3,-1)$." + tasks(1, [r"Comprueba que los puntos no son coplanarios y calcula el volumen del tetraedro que determinan.", r"Calcula el área de la cara $ABC$ del tetraedro y la longitud de la altura del tetraedro que parte del vértice $D$."])
     + recorda(r"El volumen de una pirámide es un tercio del área de la base por la altura."),
     tasks(1, [r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[1, -2, -2], [-3, -1, 1], [1, -4, -3]]) + r"=-3\neq0$: no son coplanarios. \ $V=\res{\tfrac12\ u^3}$",
               r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-4,5,-7)$: \ $S=\res{\tfrac{3\sqrt{10}}{2}\ u^2}$. \ $V=\tfrac13Sh\Rightarrow h=\dfrac{3V}{S}=\dfrac{3/2}{3\sqrt{10}/2}=\res{\tfrac{\sqrt{10}}{10}\ u}$"])),
 (2, r"\pau{Navarra, ordinaria 2024} Los puntos $A(4,-2,-3)$, $B(2,-1,1)$ y $C(0,-3,-1)$ son vértices de un rombo." + tasks(1, [r"Halla el cuarto vértice del rombo.", r"Calcula el área del rombo."]),
     tasks(1, [r"$|\overrightarrow{AB}|=|\overrightarrow{AC}|=\sqrt{21}$ y $|\overrightarrow{BC}|=\sqrt{12}$: los lados iguales son $AB$ y $AC$, y $A$ es el vértice común. \ $D=B+C-A=\res{(-2,-2,3)}$",
               r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-2,1,4)\times(-4,-1,2)=(6,-12,6)$: \ área $=\sqrt{216}=\res{6\sqrt6\ u^2}$"])),
 (2, r"\pau{Aragón, extraordinaria 2024} Sean $A(1,2,3)$, $B(1,0,-1)$ y $C(2,2,2)$ tres puntos del espacio, $\vec v_1$ el vector que va de $A$ a $B$, $\vec v_2$ el vector que va de $B$ a $C$ y $\vec v_3$ el vector que va de $C$ a $A$." + tasks(1, [r"Estudia si los vectores $\vec v_1$, $\vec v_2$ y $\vec v_3$ son linealmente independientes.", r"Calcula el área del triángulo de vértices $A$, $B$ y $C$."]),
     tasks(1, [r"$\vec v_1+\vec v_2+\vec v_3=\overrightarrow{AA}=\vec 0$: \ \rest{son linealmente dependientes} (sin hacer ningún cálculo).", r"$\overrightarrow{AB}\times\overrightarrow{AC}=(0,-2,-4)\times(1,0,-1)=(2,-4,2)$: \ área $=\tfrac12\sqrt{24}=\res{\sqrt6\ u^2}$"])),
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
pau("Ecuaciones de rectas y planos",
 (1, r"\pau{Andalucía, ordinaria 2025} Considera el punto $P(1,1,1)$ y la recta $r:\dfrac{x-1}{1}=\dfrac{y-2}{2}=\dfrac{z-3}{2}$. Halla el plano que pasa por el punto $P$ y contiene a la recta $r$.",
     r"Plano por $P$ con vectores $\vec d_r=(1,2,2)$ y $\overrightarrow{QP}=(0,-1,-2)$, donde $Q(1,2,3)\in r$: \ $\vec n=(-2,2,-1)$: \ $\res{2x-2y+z-1=0}$"),
 (2, r"\pau{Aragón, ordinaria 2025}" + tasks(1, [r"Halla las ecuaciones paramétricas de la recta $s$ que pasa por el punto $P(4,-3,0)$ y es perpendicular al plano $\pi:x-2y+z-1=0$.", r"Halla la ecuación del plano que contiene el punto $Q(1,2,3)$ y la recta $r:" + sy('x+y+z=1', 'x-2y=0') + r"$"]),
     tasks(1, [r"$\res{x=4+\lambda,\ y=-3-2\lambda,\ z=\lambda}$", r"$\vec d_r=(1,1,1)\times(1,-2,0)=(2,1,-3)$, $R(0,0,1)\in r$, $\overrightarrow{RQ}=(1,2,2)$: \ $\vec n=(8,-7,3)$: \ $\res{8x-7y+3z-3=0}$"])),
 (2, r"\pau{Cantabria, extraordinaria 2024} Sean $A(0,3,2)$, $B(4,1,3)$, $C(2,3,4)$ y $D(0,1,2)$ los vértices de un tetraedro." + tasks(1, [r"Obtén la ecuación vectorial del plano determinado por los puntos $A$, $B$ y $C$.", r"Calcula el volumen del tetraedro."]),
     tasks(1, [r"$\res{(x,y,z)=(0,3,2)+\alpha(4,-2,1)+\beta(2,0,2)}$", r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[4, -2, 1], [2, 0, 2], [0, -2, 0]]) + r"=12$: \ $V=\res{2\ u^3}$"])),
 (2, r"\pau{Castilla-La Mancha, extraordinaria 2026} Se consideran los puntos $A(1,1,0)$, $B(2,0,1)$, $C(0,2,1)$ y $D(a,1,2)$, con $a$ un número real." + tasks(1, [r"Determina la ecuación del plano que pasa por los puntos $A$, $B$ y $C$.", r"Determina los valores de $a$ para que el tetraedro formado por los cuatro puntos tenga volumen 3 unidades cúbicas."]),
     tasks(1, [r"$\overrightarrow{AB}\times\overrightarrow{AC}=(1,-1,1)\times(-1,1,1)=(-2,-2,0)$: \ $\res{x+y-2=0}$", r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=(-2,-2,0)\cdot(a-1,0,2)=2-2a$; \ $\tfrac{|2-2a|}{6}=3$: \ $\res{a=-8\ \text{o}\ a=10}$"])),
 (2, r"\pau{Castilla y León, extraordinaria 2026} Los puntos $A(1,1,1)$ y $B(0,2,0)$ son vértices consecutivos del paralelogramo $ABCD$, que tiene el centro en $E(0,0,1)$." + tasks(1, [r"Calcula las coordenadas de los otros vértices.", r"Halla la ecuación general del plano que contiene el paralelogramo.", r"Halla el volumen del tetraedro de vértices $A$, $B$, $E$ y el origen de coordenadas $O$."]),
     tasks(1, [r"$E$ es el punto medio de las diagonales: $C=2E-A=\res{(-1,-1,1)}$, \ $D=2E-B=\res{(0,-2,2)}$", r"$\overrightarrow{AB}\times\overrightarrow{AE}=(-1,1,-1)\times(-1,-1,0)=(-1,1,2)$: \ $\res{x-y-2z+2=0}$",
               r"$\big[\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OE}\big]=" + vm([[1, 1, 1], [0, 2, 0], [0, 0, 1]]) + r"=2$: \ $V=\res{\tfrac13\ u^3}$"])),
 (2, r"\pau{Cataluña, ordinaria 2026} Considera los puntos $P(1,0,-1)$, $Q(3,-2,0)$ y $R(1,1,1)$." + tasks(1, [r"Calcula la ecuación del plano que contiene los puntos $P$, $Q$ y $R$.", r"Comprueba que el área del triángulo $PQR$ es $\tfrac{3\sqrt5}{2}\ u^2$.", r"Determina las condiciones que deben cumplir las coordenadas de un cuarto punto $S(x,y,z)$ para que $P$, $Q$, $R$ y $S$ formen un tetraedro de volumen 1."]),
     tasks(1, [r"$\overrightarrow{PQ}\times\overrightarrow{PR}=(2,-2,1)\times(0,1,2)=(-5,-4,2)$: \ $\res{5x+4y-2z-7=0}$", r"$\tfrac12|(-5,-4,2)|=\tfrac12\sqrt{45}=\tfrac{3\sqrt5}{2}$ \ \checkmark",
               r"$\tfrac16\big|(-5,-4,2)\cdot(x-1,y,z+1)\big|=1\iff|5x+4y-2z-7|=6$: $S$ debe estar en uno de los planos \ $\res{5x+4y-2z-1=0}$ \ o \ $\res{5x+4y-2z-13=0}$"])),
 (2, r"\pau{Extremadura, extraordinaria 2026} Dados los puntos $A(4,3,3)$, $B(3,3,4)$, $C(1,0,4)$ y $D(4,0,1)$:" + tasks(1, [r"Justifica de forma razonada que los puntos $A$, $B$, $C$ y $D$ están en el mismo plano y halla la ecuación del plano que determinan.", r"Calcula el valor de $k$ para que el punto $P(7,k,2)$ pertenezca a la recta $r$ que pasa por los puntos $A$ y $C$."]),
     tasks(1, [r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[-1, 0, 1], [-3, -3, 1], [0, -3, -2]]) + r"=0$: son coplanarios. \ $\vec n=(3,-2,3)$: \ $\res{3x-2y+3z-15=0}$", r"$r:(4-3t,\ 3-3t,\ 3+t)$; $z=2$ da $t=-1$ y $x=7$ \checkmark: \ $\res{k=6}$"])),
 (2, r"\pau{Extremadura, ordinaria 2026}" + tasks(1, [r"Dados los vectores $\vec u=(0,3,-4)$ y $\vec v=(12,4,3)$, comprueba que el paralelogramo que forman es un rectángulo y calcula su área.", r"Halla la ecuación del plano formado por los vectores $\vec u$ y $\vec v$ y el punto $(1,0,0)$.", r"Obtén un vector perpendicular a los vectores $\vec u$ y $\vec v$ de módulo 13."]),
     tasks(1, [r"$\vec u\cdot\vec v=0+12-12=0$: rectángulo. \ $\vec u\times\vec v=(25,-48,-36)$, de módulo $\sqrt{4225}$: \ área $=\res{65\ u^2}$", r"$\res{25x-48y-36z-25=0}$", r"$\pm\tfrac{13}{65}(25,-48,-36)=\res{\pm\left(5,-\tfrac{48}{5},-\tfrac{36}{5}\right)}$"])),
 (2, r"\pau{Madrid, ordinaria 2025} Dados la recta $r:\dfrac{x-1}{2}=\dfrac y0=\dfrac{z-2}{1}$ y el plano $\pi:x+2y-3z=1$, halla una ecuación del plano que contiene a $r$ y es perpendicular a $\pi$.",
     r"Vectores directores $\vec d_r=(2,0,1)$ y $\vec n_\pi=(1,2,-3)$, punto $(1,0,2)$: \ $\vec n=(2,0,1)\times(1,2,-3)=(-2,7,4)$: \ $\res{2x-7y-4z+6=0}$"),
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
pau("Posiciones relativas de rectas y planos",
 (2, r"\pau{Asturias, extraordinaria 2024} Se consideran los puntos $A(1,1,1)$, $B(1,0,2)$, $C(-1,1,3)$ y $D(-1,0,1)$." + tasks(1, [r"Estudia si hay un plano que contenga los cuatro puntos.", r"Calcula la recta $r$ que pasa por $D$ y es perpendicular al plano $\pi$ que contiene $A$, $B$ y $C$.", r"Calcula el punto $P$ de intersección de $r$ y $\pi$."]),
     tasks(1, [r"$\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[0, -1, 1], [-2, 0, 2], [-2, -1, 0]]) + r"=6\neq0$: \ \rest{no hay ninguno}.", r"$\overrightarrow{AB}\times\overrightarrow{AC}=(-2,-2,-2)$: $\pi:x+y+z-3=0$; \ $\res{r:\dfrac{x+1}{1}=\dfrac y1=\dfrac{z-1}{1}}$",
               r"$(-1+t)+t+(1+t)-3=0$, $t=1$: \ $\res{P(0,1,2)}$"])),
 (2, r"\pau{Canarias, extraordinaria 2025} Se tienen las rectas $r:" + sy('x+y-2z=3', '2x+y-6z=2') + r"$ \ y \ $s:x-1=\dfrac y3=\dfrac{z+1}{2}$." + tasks(1, [r"Comprueba que $r$ y $s$ son coplanarias.", r"Halla la ecuación del plano que las contiene."]),
     tasks(1, [r"$\vec d_r=(1,1,-2)\times(2,1,-6)=(-4,2,-1)$, $R(-1,4,0)\in r$; $\vec d_s=(1,3,2)$, $Q(1,0,-1)$: \ $\big[\vec d_r,\vec d_s,\overrightarrow{RQ}\big]=" + vm([[-4, 2, -1], [1, 3, 2], [2, -4, -1]]) + r"=0$ \ \checkmark", r"$\vec d_r\times\vec d_s=(7,7,-14)\parallel(1,1,-2)$, por $Q$: \ $\res{x+y-2z-3=0}$"])),
 (2, r"\pau{Canarias, ordinaria 2026} Se conocen el plano $\pi:2x+3y=0$ y el punto $P(1,-5,1)$." + tasks(1, [r"Halla la recta $r$ perpendicular al plano $\pi$ que pasa por el punto $P$.", r"Halla la posición relativa de la recta $s:" + sy('-x+3y-3z=-3', '4x+9y-2z=-2') + r"$ \ con el plano $\pi$."]),
     tasks(1, [r"Vector director $\vec n_\pi=(2,3,0)$: \ $\res{r:\ x=1+2\lambda,\ y=-5+3\lambda,\ z=1}$", r"$\vec d_s=(-1,3,-3)\times(4,9,-2)=(21,-14,-21)\parallel(3,-2,-3)$; \ $\vec n\cdot\vec d_s=6-6=0$ y el punto $\left(1,-\tfrac23,0\right)\in s$ cumple $2-2=0$: \ \rest{$s$ está contenida en $\pi$}."])),
 (3, r"\pau{Canarias, extraordinaria 2024} Considera las rectas $r_1:" + sy('x-3y+2z+2=0', '2x+y-3z=3') + r"$ \ y \ $r_2:\dfrac{1-x}{2}=y=\dfrac{1-z}{2}$." + tasks(1, [r"Estudia la posición relativa de las dos rectas.", r"Halla la ecuación de la recta $s$ que tiene dirección perpendicular a las dos rectas y pasa por $P\left(0,\tfrac12,0\right)$. Calcula el punto de corte de $s$ con $r_1$."]),
     tasks(1, [r"$\vec d_1=(7,7,7)\parallel(1,1,1)$, $P_1(1,1,0)$; \ $\vec d_2=(-2,1,-2)$, $P_2(1,0,1)$: \ $\big[\vec d_1,\vec d_2,\overrightarrow{P_1P_2}\big]=" + vm([[1, 1, 1], [-2, 1, -2], [0, -1, 1]]) + r"=3\neq0$: \ \rest{se cruzan}.",
               r"$\vec d_1\times\vec d_2=(-3,0,3)\parallel(1,0,-1)$: \ $s:\left(\lambda,\tfrac12,-\lambda\right)$. Con $r_1:(1+\mu,1+\mu,\mu)$: $\mu=-\tfrac12$, $\lambda=\tfrac12$: \ $\res{\left(\tfrac12,\tfrac12,-\tfrac12\right)}$"])),
 (2, r"\pau{Cantabria, ordinaria 2024} Considera la recta $r:" + sy('x+y+z+5=0', 'x+2y-z=0') + r"$ \ y el plano $\pi:2x+y-az=3$. Razona si es posible dar algún valor al parámetro $a$ para que:" + tasks(1, [r"la recta esté contenida en el plano;", r"la recta y el plano sean paralelos;", r"la recta y el plano se corten. En caso afirmativo, da un valor de $a$ y calcula dónde se cortan."]),
     r"$\vec d_r=(1,1,1)\times(1,2,-1)=(-3,2,1)$, $R(-10,5,0)\in r$; \ $\vec n\cdot\vec d=-6+2-a=-4-a$. Si $a=-4$, $R$ da $-15\neq3$." + tasks(1, [r"\rest{Ningún valor de $a$.}", r"\rest{$a=-4$.}", r"\rest{Cualquier $a\neq-4$}; por ejemplo, con $a=2$ se cortan en $\res{(-1,-1,-3)}$."])),
 (2, r"\pau{Castilla y León, ordinaria 2025} Sean las rectas $r:\dfrac x4=\dfrac{y-1}{-2}=\dfrac z2$ y $s:x-1=\dfrac{y-m}{m-1}=\dfrac{z-3}{3}$." + tasks(1, [r"Comprueba que las rectas $r$ y $s$ se cortan para cualquier valor de $m$.", r"Para $m=6$, halla el punto de intersección de las rectas $r$ y $s$."]),
     tasks(1, [r"$P(0,1,0)\in r$, $Q(1,m,3)$: $\overrightarrow{PQ}=(1,m-1,3)=\vec d_s$, así que $\big[\vec d_r,\vec d_s,\overrightarrow{PQ}\big]=0$, y $\vec d_r=(4,-2,2)$ no es paralelo a $\vec d_s$: \rest{secantes para todo $m$}. (De hecho, $Q-\vec d_s=P$: el punto $P$ es de $s$.)", r"$\res{(0,1,0)}$ (para cualquier $m$)."])),
 (2, r"\pau{Castilla y León, extraordinaria 2025} Sean el plano $\pi:5x+my+z=2$ y la recta $r:(x,y,z)=(1,1,0)+t(-1,-1,2)$." + tasks(1, [r"Determina la posición relativa de $r$ y $\pi$ en función de $m$.", r"Para $m=1$, calcula el plano $\pi'$ que contiene a $r$ y es perpendicular a $\pi$."]),
     tasks(1, [r"$\vec n\cdot\vec d=-5-m+2=-3-m$; $P(1,1,0)$: $5+m=2\iff m=-3$. Si $m=-3$: \rest{$r\subset\pi$}; si $m\neq-3$: \rest{secantes}.", r"$\vec n'=(-1,-1,2)\times(5,1,1)=(-3,11,4)$: \ $\res{3x-11y-4z+8=0}$"])),
 (1, r"\pau{Galicia, extraordinaria 2025} Dadas las rectas" + dm(r"r:\dfrac{x-1}{2}=\dfrac{y-2}{-1}=\dfrac{z-1}{1}\qquad\text{y}\qquad s:\dfrac{x-2}{4}=\dfrac{y-1}{-2}=\dfrac{z-1}{2}") + r"" + tasks(1, [r"Calcula la posición relativa de las rectas $r$ y $s$.", r"Obtén la ecuación del plano que contiene las rectas $r$ y $s$."]),
     tasks(1, [r"$\vec d_s=2\vec d_r$ y $Q(2,1,1)\notin r$: \ \rest{paralelas}.", r"$\vec n=(2,-1,1)\times\overrightarrow{PQ}=(2,-1,1)\times(1,-1,0)=(1,1,-1)$: \ $\res{x+y-z-2=0}$"])),
 (2, r"\pau{Galicia, extraordinaria 2024} Considera el plano $\pi:x+2y-2z=0$ y la recta $r$ que pasa por los puntos $A(2,1,2)$ y $B(0,1,1)$." + tasks(1, [r"Estudia la posición relativa de la recta $r$ y el plano $\pi$.", r"Obtén la ecuación implícita o general del plano que contiene a $r$ y es perpendicular a $\pi$."]),
     tasks(1, [r"$\vec d=(-2,0,-1)$: $\vec n\cdot\vec d=-2+2=0$ y $A$: $2+2-4=0$: \ \rest{$r$ está contenida en $\pi$}.", r"$\vec n'=(-2,0,-1)\times(1,2,-2)=(2,-5,-4)$: \ $\res{2x-5y-4z+9=0}$"])),
 (1, r"\pau{Galicia, ordinaria 2024} Considera el plano $\pi:4x+2y+bz=2$ y la recta $r:\dfrac{x-2}{3}=\dfrac{y-c}{2}=\dfrac{z-3}{4}$, donde $b$ y $c$ son parámetros reales. Calcula los valores de $b$ y $c$ para que la recta $r$ esté contenida en $\pi$.",
     r"$\vec n\cdot\vec d=12+4+4b=0\Rightarrow b=-4$; el punto $(2,c,3)$ debe ser de $\pi$: $8+2c-12=2$: \ $\res{b=-4,\ c=3}$"),
 (2, r"\pau{Murcia, extraordinaria 2025} Considera la recta $r:" + sy('x+y+z=1', '-x-2y+z=0') + r"$ \ y el plano $\pi:2x+y+az=b$." + tasks(1, [r"Determina los valores de $a$ y $b$ para que el plano contenga a la recta.", r"¿Para qué valores de $a$ y $b$ la recta corta al plano? Halla el punto de corte en el caso $a=0$, $b=7$."]),
     tasks(1, [r"$\vec d=(3,-2,-1)$, $R(2,-1,0)\in r$: $\vec n\cdot\vec d=4-a=0$ y $4-1=b$: \ $\res{a=4,\ b=3}$", r"\rest{Si $a\neq4$} (cualquier $b$). Con $a=0$, $b=7$: $2(2+3t)+(-1-2t)=7$, $t=1$: \ $\res{(5,-3,-1)}$"])),
 (2, r"\pau{Navarra, extraordinaria 2024} Se consideran el plano $\pi:2x+y-z-5=0$, la recta $r:" + sy('x+2z+3=0', '-x-y+z+4=0') + r"$ \ y los puntos $A(3,2,-1)$ y $B(1,1,-1)$. Sea $C$ la intersección de la recta y el plano." + tasks(1, [r"Demuestra que los puntos $A$, $B$ y $C$ no están alineados.", r"Calcula el área del triángulo que forman los tres puntos."]),
     tasks(1, [r"$r:(-3+2t,\ 7-3t,\ t)$; en $\pi$: $2t-4=0$, $C(1,1,-2)$. \ $\overrightarrow{AB}\times\overrightarrow{AC}=(-2,-1,0)\times(-2,-1,-1)=(1,-2,0)\neq\vec 0$: \ \rest{no alineados}.", r"$\tfrac12|(1,-2,0)|=\res{\tfrac{\sqrt5}{2}\ u^2}$"])),
 (3, r"\pau{Navarra, ordinaria 2025} Calcula la ecuación continua de la recta $t$ que pasa por el punto $P(2,0,-1)$ y corta a las rectas $s:" + sy('2x+y-3z-6=0', '2x-3z-8=0') + r"$ \ y \ $r:\dfrac{x+1}{2}=\dfrac y1=\dfrac{z+2}{1}$."
     + recorda(r"La recta $t$ es la intersección del plano que contiene $P$ y $s$ con el plano que contiene $P$ y $r$."),
     r"Plano por $P$ que contiene a $s$ (haz): $(2x+y-3z-6)+\lambda(2x-3z-8)=0$; en $P$: $1-\lambda=0$: $4x+y-6z-14=0$. \ Plano por $P$ que contiene a $r$: $\vec n=(2,1,1)\times(3,0,1)=(1,1,-3)$: $x+y-3z-5=0$. \ $\vec d_t=(4,1,-6)\times(1,1,-3)=(3,6,3)$: \ $\res{t:\dfrac{x-2}{1}=\dfrac y2=\dfrac{z+1}{1}}$ \ (corta a $r$ en $(3,2,0)$ y a $s$ en $(1,-2,-2)$)."),
 (2, r"\pau{País Vasco, extraordinaria 2024} Se consideran la recta $r:" + sy('2x-y+z=0', 'x-y+4z=1') + r"$ \ y el plano $\pi:2x-3y+Az=10$." + tasks(1, [r"Calcula el valor del parámetro $A$ para que la recta $r$ y el plano $\pi$ sean paralelos.", r"Si $A=21$, calcula la intersección del plano $\pi$ y la recta $r$."]),
     tasks(1, [r"$\vec d=(2,-1,1)\times(1,-1,4)=(-3,-7,-1)$: $\vec n\cdot\vec d=-6+21-A=0$, $A=15$; y $(-1,-2,0)\in r$ da $4\neq10$: \ $\res{A=15}$", r"$\res{(2,5,1)}$"])),
 (1, r"\pau{Aragón, ordinaria 2026} Sean los planos $\pi:x-2y+4z+1=0$ y $\pi_d:2x-3y+6z=d$, con $d\in\mathbb R$." + tasks(1, [r"¿Hay algún valor de $d$ para el que los planos $\pi$ y $\pi_d$ no se cortan?", r"Calcula, para $d=-2$, los puntos de corte entre los planos $\pi$ y $\pi_d$."]),
     tasks(1, [r"Los vectores normales $(1,-2,4)$ y $(2,-3,6)$ no son proporcionales: \ \rest{no}: siempre se cortan en una recta.", r"$\vec d=(0,2,1)$ y, con $z=0$, $(-1,0,0)$: \ $\res{x=-1,\ y=2\lambda,\ z=\lambda}$"])),
)

# ---------- 7. Tres plans
E_ = lambda a: [[1, 1, 1, 1], [a - 1, 1, 1, a], [1, a - 1, -1, 0]]
for a in [F(v, 2) for v in range(-8, 13)]:
    ck(det3(*[r[:3] for r in E_(a)]) == a * (a - 2))
    t = pos3(E_(a))[2]
    ck(t == ('2coinc' if a == 0 else '2par' if a == 2 else 'punt'))
    if t == 'punt': ck(all(sum(fr(c) * x for c, x in zip(r[:3], [(a - 1) / (a - 2), 1 / (2 - a), 0])) == r[3] for r in E_(a)))
ck(all(all(sum(fr(c) * x for c, x in zip(r[:3], [F(1, 2), F(1, 2) - l, l])) == r[3] for r in E_(0)) for l in range(-3, 4)))
pau("Posición relativa de tres planos",
 (3, r"\pau{La Rioja, extraordinaria 2026} Determina los valores de $a$ para que los planos $\pi_1:x+y+z=1$, \ $\pi_2:(a-1)x+y+z=a$ \ y \ $\pi_3:x+(a-1)y-z=0$" + tasks(1, [r"se corten en un punto. En este caso, determina el punto de corte.", r"se corten en una recta. En este caso, determina la recta en forma paramétrica."]),
     r"$|M|=" + vm([[1, 1, 1], ['a-1', 1, 1], [1, 'a-1', -1]]) + r"=a(a-2)$." + tasks(1, [r"\rest{Si $a\neq0$ y $a\neq2$.} Restando $\pi_1$ de $\pi_2$: $(a-2)x=a-1$; \ $\res{\left(\tfrac{a-1}{a-2},\ \tfrac{1}{2-a},\ 0\right)}$",
     r"Si $a=0$: $\pi_2:-x+y+z=0$ y $\pi_3:x-y-z=0$ son coincidentes y cortan a $\pi_1$: \ \rest{$a=0$}, \ $\res{x=\tfrac12,\ y=\tfrac12-\lambda,\ z=\lambda}$. \ (Si $a=2$, $\pi_1\parallel\pi_2$: no hay ningún punto común.)"])),
)

# ---------- 8. Feixos de plans
ck(prim([fr(a) + 4 * b for a, b in zip([2, 1, -1, -4], [1, 1, -2, -3])]) == [6, 5, -9, -16] and onp([6, 5, -9, -16], [-2, 2, -2]))
X_ = [0, 1, 2]; ck(onp([1, -3, -2, 7], X_) and X_ == [0, 1 - 2 * 0, 2 + 0])
c_ = prim([fr(a) - F(3, 2) * b for a, b in zip([1, 1, -2, 0], [2, -3, 1, -1])]); ck(c_ == [4, -11, 7, -3] and onp(c_, X_))
pau("Haces de planos",
 (2, r"\pau{Murcia, extraordinaria 2026} Determina la ecuación del plano que contiene el punto $P(-2,2,-2)$ y la recta $r$ dada como intersección de dos planos: \ $r:" + sy('2x+y-z=4', 'x+y-2z=3') + r"$",
     r"Haz: $(2x+y-z-4)+\lambda(x+y-2z-3)=0$; en $P$: $-4+\lambda=0$, $\lambda=4$: \ $\res{6x+5y-9z-16=0}$"),
 (2, r"\pau{País Vasco, ordinaria 2025} Se consideran las rectas $r_1:" + sy('x+y-2z=0', '2x-3y+z=1') + r"$ \ y \ $r_2:" + sy('x=3t', 'y=1-2t', 'z=2+t') + r"$ \ Calcula la ecuación del plano que contiene a $r_1$ y pasa por el punto de intersección del plano $\pi:x-3y-2z+7=0$ y la recta $r_2$.",
     r"$r_2\cap\pi$: $3t-3(1-2t)-2(2+t)+7=7t=0$, punto $(0,1,2)$. \ Haz: $(x+y-2z)+\lambda(2x-3y+z-1)=0$; en $(0,1,2)$: $-3-2\lambda=0$, $\lambda=-\tfrac32$: \ $\res{4x-11y+7z-3=0}$"),
)

# ---------- 9. Problemes
A_, B_, C_, D_ = [-2, 3, 120], [20, 42, 120], [-1, 4, 165], [20, 43, 165]
ck(det3(sub(B_, A_), sub(C_, A_), sub(D_, A_)) == -1755)
ck(det3([1, 2, 3], [3, 2, 1], [5, 4, 3]) == 0 and prim(cross([2, 1, 1], [4, 3, 1])) == [1, -1, -1] and onp([1, -1, -1, 0], [1, 1, 0]))
M1_, M2_, M3_ = [2, 3, 6], [4, 4, 5], [5, 1, 4]
ck(plane3(M1_, M2_, M3_) == [4, -1, 7, -47])
T = [[3, 8, F(17, 2)], [4, 6, F(37, 4)], [2, 8, 8]]
ck(plane3(*T) == [4, -1, -8, 64] and onp([4, -1, -8, 64], [4, 16, 8]) and all(not onp([4, -1, -8, 64], [s_, 16, 8]) for s_ in range(-5, 12) if s_ != 4))
pau("Problemas y cuestiones",
 (2, r"\pau{Aragón, extraordinaria 2026} Estamos reparando una silla metálica que cojeaba, porque los extremos inferiores de sus cuatro patas no se apoyaban a la vez en un suelo plano. La silla está tumbada sobre una mesa de trabajo de 120 cm de altura y tiene cuatro patas de 45 cm de longitud cada una. Después de la reparación, los extremos inferiores de las patas están situados en los puntos $A(-2,3,120)$, $B(20,42,120)$, $C(-1,4,165)$ y $D(20,43,165)$. Cuando bajemos la silla de la mesa y la dejemos en el suelo, ¿cojeará o apoyará las cuatro patas sobre el suelo plano del taller?",
     r"Las cuatro patas se apoyan si los cuatro extremos son coplanarios: \ $\big[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}\big]=" + vm([[22, 39, 0], [1, 1, 45], [22, 40, 45]]) + r"=-1755\neq0$: \ \rest{no son coplanarios: la silla cojeará}."),
 (2, r"\pau{Islas Baleares, extraordinaria 2026} En un estudio de astronomía se modeliza una constelación artificial de satélites que orbitan alrededor de la Tierra. Tomamos un sistema de coordenadas con el origen en el centro de la Tierra (las unidades son decenas de miles de kilómetros) y situamos cinco satélites: $A(1,2,3)$, $B(3,2,1)$, $C(5,4,3)$, $D(2,1,1)$ y $E(4,3,1)$. Decimos que unos satélites forman un plano orbital si, junto con el centro de la Tierra, son coplanarios."
     + tasks(1, [r"Determina si los satélites $A$, $B$ y $C$ forman un plano orbital.", r"Proporciona un punto $F$ (distinto del origen) donde se podría colocar un sexto satélite para que los satélites $D$, $E$ y $F$ formen otro plano orbital."]),
     tasks(1, [r"$\big[\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC}\big]=" + vm([[1, 2, 3], [3, 2, 1], [5, 4, 3]]) + r"=0$: \ \rest{sí}.", r"El plano $ODE$ tiene vector normal $(2,1,1)\times(4,3,1)=(-2,2,2)$: $x-y-z=0$. Cualquier punto de este plano (no alineado con $O$, $D$, $E$); por ejemplo, \ $\res{F(1,1,0)}$"])),
 (2, r"\pau{Islas Baleares, ordinaria 2026} En un estudio de grabación se han colgado del techo tres micrófonos para grabar un concierto acústico. Tomamos un sistema de referencia con el origen en el suelo de la sala; el techo está a 7 m de altura. El micrófono $M_1$ tiene coordenadas $x=2$, $y=3$ y cuelga de un cable de 1 m; el micrófono $M_2$ tiene $x=4$, $y=4$ y cuelga de un cable de 2 m, y el micrófono $M_3$ tiene $x=5$, $y=1$ y cuelga de un cable de 3 m. Determina las coordenadas de los tres micrófonos y calcula la ecuación del plano que los contiene.",
     r"$\res{M_1(2,3,6),\ M_2(4,4,5),\ M_3(5,1,4)}$. \ $\overrightarrow{M_1M_2}\times\overrightarrow{M_1M_3}=(2,1,-1)\times(3,-2,-2)=(-4,1,-7)$: \ $\res{4x-y+7z-47=0}$"),
 (2, r"\pau{La Rioja, ordinaria 2026} En un chiringuito de playa se instala un toldo para los clientes. El toldo se coloca en los puntos de apoyo $\left(3,8,\tfrac{17}{2}\right)$, $\left(4,6,\tfrac{37}{4}\right)$, $(2,8,8)$ y $(s,16,8)$, con $s\in\mathbb R$." + tasks(1, [r"Determina la ecuación del plano que contiene el toldo.", r"Calcula el valor de $s$ para que los cuatro puntos sean coplanarios."]),
     tasks(1, [r"Vectores $\left(1,-2,\tfrac34\right)$ y $\left(-1,0,-\tfrac12\right)$; su producto vectorial es proporcional a $(4,-1,-8)$: \ $\res{4x-y-8z+64=0}$", r"$4s-16-64+64=0$: \ $\res{s=4}$"])),
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
TIT = "Vectores y aplicaciones. Rectas, planos y haces de planos"
KW = "vectores, producto escalar, producto vectorial, producto mixto, áreas, volúmenes, ecuaciones de la recta, ecuaciones del plano, posiciones relativas, haces de planos, PAU"
# espai fi després de les comes de les ternes de coordenades: (1,-2,3) -> (1,\,-2,\,3)
TRI = re.compile(r'\((-?[\w\\{}.+\-]+),(-?[\w\\{}.+\-]+),(-?[\w\\{}.+\-]+)\)')
# i les equacions amb fraccions (equació contínua…) no es parteixen entre dues línies
INL = re.compile(r'(?<![\\$])\$([^$]+)\$')
def esp(t):
    t = TRI.sub(lambda mm: '(' + r',\,'.join(mm.groups()) + ')', t)
    return INL.sub(lambda mm: r'\mbox{$' + mm.group(1) + '$}' if r'\dfrac' in mm.group(1) and len(mm.group(1)) < 260 else mm.group(0), t)
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 3: %s' % (t, TIT), capcalera='%s · Unidad 3: Vectores, rectas y planos' % t, pdfkeywords=KW, curs='2batx-mii')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-mii') + '{' + ('Soluciones de la ficha · Unidad 3' if sol else 'Ficha de ejercicios · Unidad 3') + r'}{\raggedright ' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Una recta o un plano se pueden escribir de muchas maneras: si tu punto o tu vector director son distintos, comprueba que el punto es de la recta (o del plano) y que los vectores son proporcionales. Puedes comprobar los resultados con las herramientas interactivas de los apuntes."
             if sol else r"Resuelve los ejercicios en el cuaderno justificando cada paso. Haz un esbozo cuando te ayude a ver la situación y comprueba siempre los resultados (que el punto hallado está en los planos, que el vector normal es perpendicular a los vectores directores\ldots). Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de otras comunidades autónomas (2024--2026); se han quitado los apartados de ángulos y distancias, que son de la unidad siguiente.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con las herramientas 3D de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't3-fitxa-solucions-es.tex' if sol else 't3-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
print(n, 'ejercicios,', npau, 'de la PAU de otras comunidades')
