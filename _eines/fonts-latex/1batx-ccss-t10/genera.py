# Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (1r Batxillerat CCSS, Unitat 10: Distribucions de probabilitat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Bilingüe: T(valencià, castellà); genera-es.py l'executa amb FM_LANG=es i escriu els -es.tex.
# Les 6 seccions segueixen els apunts (materials/1batx-ccss/t10-distribucions-probabilitat.html): variables aleatòries
# discretes (10.1-10.2), distribució binomial i la seua taula (10.3-10.4), variables contínues i funció de densitat (10.5),
# la normal típica i la seua taula (10.6-10.7), tipificació i problemes (10.8) i aproximació de la binomial a la normal (10.9).
# Alguns exercicis de les seccions 2, 5 i 6 són de la PAU d'altres comunitats (els mateixos que a la fitxa de la unitat 10 de
# 2n Batx CCSS, _eines/fonts-latex/2batx-ccss-t10, d'on vénen també gauss(), Phi() i zinv()).
# Les probabilitats de la normal es calculen com a la PAU valenciana: z arredonit a dues decimals i valor de la taula N(0,1)
# amb quatre decimals (Phi); en els problemes inversos es pren el valor de la taula més pròxim (zinv). Les discretes, amb
# fraccions exactes (Fraction). Cada resultat es comprova amb ck().
# Ús: python3 genera.py && python3 genera-es.py, i pdflatex (dues vegades) dels quatre .tex
import os, re, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return (es if ES else va).replace("\\'", "'")
NCHK = [0]
def ck(x, y, tol=1e-9):
    assert abs(float(x) - float(y)) <= tol, (x, y); NCHK[0] += 1; return x

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def pau(t): return '\\pau{%s}' % t
def E(st, q, s): return (st, q, s)

# ---------- nombres ----------
def fr(f):
    f = Fr(f)
    if f.denominator == 1: return str(f.numerator)
    return ('-' if f < 0 else '') + r'\frac{%d}{%d}' % (abs(f.numerator), f.denominator)
def dc(x, k=4):
    s = ('%.*f' % (k, float(x))).rstrip('0').rstrip('.')
    return s.replace('.', '{,}')
def d4(x): return ('%.4f' % float(x)).replace('.', '{,}')
def N2(x): return r'\res{%s}' % d4(x)

# ---------- binomial i normal com a la PAU ----------
def pmf(n, p, k): return math.comb(n, k) * p ** k * (1 - p) ** (n - k)
def r4(x): return round(x, 4)
def r2(z): return math.floor(abs(z) * 100 + 0.5 + 1e-9) / 100 * (1 if z >= 0 else -1)
def Phi(z):
    z = r2(z)
    if z < 0: return round(1 - Phi(-z), 4)
    if z >= 4: return 1.0
    return round(0.5 * (1 + math.erf(z / math.sqrt(2))), 4)
TAB = [(r / 10 + c / 100, Phi(r / 10 + c / 100)) for r in range(40) for c in range(10)]
def zinv(p):
    """z amb P(Z <= z) = p, prenent el valor de la taula més pròxim (mitjana si n'hi ha dos d'igual de pròxims)"""
    neg = p < 0.5; pp = 1 - p if neg else p
    d = min(abs(v - pp) for _, v in TAB); zs_ = [z for z, v in TAB if abs(abs(v - pp) - d) < 1e-12]
    z = sum(zs_) / len(zs_)
    return -z if neg else z
def zs(x, m, s): return r2((x - m) / s)
def aprox(n, p, lo, hi):
    m = n * p; s = math.sqrt(n * p * (1 - p))
    if lo is None: return Phi(zs(hi, m, s))
    if hi is None: return 1 - Phi(zs(lo, m, s))
    return Phi(zs(hi, m, s)) - Phi(zs(lo, m, s))

# ---------- figures ----------
def gauss(shade, ticks=(), w=4.2):
    """campana N(0,1); shade: llista d'intervals en unitats de z (None = infinit); ticks: [(z, etiqueta)]"""
    sx = w / 7.0
    o = [r'\begin{tikzpicture}[x=%.3fcm,y=1.6cm,baseline=(current bounding box.center)]' % sx]
    for a, b in shade:
        a = -3.5 if a is None else max(a, -3.5); b = 3.5 if b is None else min(b, 3.5)
        o.append(r'\fill[accent!35] (%.3f,0) -- plot[domain=%.3f:%.3f,samples=60,smooth] (\x,{exp(-\x*\x/2)}) -- (%.3f,0) -- cycle;' % (a, a, b, b))
    o.append(r'\draw[muted,-latex] (-3.6,0)--(3.7,0);')
    o.append(r'\draw[teal,thick] plot[domain=-3.5:3.5,samples=90,smooth] (\x,{exp(-\x*\x/2)});')
    for z, l in ticks:
        o.append(r'\draw[muted] (%.3f,0.05)--(%.3f,-0.05) node[below,font=\scriptsize,text=navy]{$%s$};' % (z, z, l))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def dens(pts, c, d, xt, yt, sx=0.55, sy=3.0):
    """densitat lineal a trossos pts=[(x, y)] amb l'àrea entre c i d ombrejada; xt, yt: marques dels eixos"""
    def f(x):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= x <= x1: return y0 + (y1 - y0) * (x - x0) / (x1 - x0) if x1 > x0 else max(y0, y1)
        return 0
    xs = sorted(set([c, d] + [x for x, _ in pts if c < x < d]))
    poly = ' -- '.join('(%.3f,%.4f)' % (x, f(x)) for x in xs)
    o = [r'\begin{tikzpicture}[x=%.3fcm,y=%.3fcm,baseline=(current bounding box.center)]' % (sx, sy)]
    o.append(r'\fill[accent!35] (%.3f,0) -- %s -- (%.3f,0) -- cycle;' % (c, poly, d))
    x0, x1 = pts[0][0] - 0.8, pts[-1][0] + 0.8
    o.append(r'\draw[muted,-latex] (%.2f,0)--(%.2f,0) node[right,font=\scriptsize]{$x$};' % (x0, x1))
    o.append(r'\draw[muted,-latex] (%.2f,0)--(%.2f,%.3f);' % (x0 + 0.3, x0 + 0.3, max(y for _, y in pts) * 1.3))
    o.append(r'\draw[teal,thick] (%.2f,0) -- (%.3f,0) -- %s -- (%.3f,0) -- (%.2f,0);' % (x0, pts[0][0], ' -- '.join('(%.3f,%.4f)' % p for p in pts), pts[-1][0], x1 - 0.3))
    for x, l in xt: o.append(r'\draw[muted] (%.3f,0.03)--(%.3f,-0.03) node[below,font=\scriptsize,text=navy]{$%s$};' % (x, x, l))
    for y, l in yt: o.append(r'\draw[muted,dashed] (%.2f,%.4f)--(%.3f,%.4f); \node[left,font=\scriptsize,text=navy] at (%.2f,%.4f) {$%s$};' % (x0 + 0.3, y, pts[-1][0], y, x0 + 0.3, y, l))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def bars(xs, ps, w=0.5, sy=4.0):
    o = [r'\begin{tikzpicture}[x=0.8cm,y=%.2fcm,baseline=(current bounding box.center)]' % sy]
    o.append(r'\draw[muted,-latex] (%.2f,0)--(%.2f,0);' % (min(xs) - 0.7, max(xs) + 0.8))
    for x, p in zip(xs, ps):
        o.append(r'\fill[accent!70] (%.2f,0) rectangle (%.2f,%.4f); \node[below,font=\scriptsize,text=navy] at (%.2f,0) {$%s$}; \node[above,font=\scriptsize,text=navy] at (%.2f,%.4f) {$%s$};' % (x - w / 4, x + w / 4, float(p), x, x, x, float(p), fr(p)))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def cen(*gs): return '\n\n\\begin{center}' + '\\qquad'.join(gs) + '\\end{center}\n'

S_ = []
def sec(title): S_.append((title, [])); return S_[-1][1]
def EV(xs, ps):
    mu = sum(Fr(x) * p for x, p in zip(xs, ps)); m2 = sum(Fr(x) ** 2 * p for x, p in zip(xs, ps))
    return mu, m2, m2 - mu ** 2

# =====================================================================
# 1. Variables aleatòries discretes
X = sec(T("Variables aleatòries discretes", "Variables aleatorias discretas"))
X.append(E(1, T("Digues si les variables aleatòries següents són discretes o contínues:", "Di si las variables aleatorias siguientes son discretas o continuas:") + tasks(2, [
    T("El nombre de germans d'un alumne.", "El número de hermanos de un alumno."), T("El temps que tarda un autobús a arribar.", "El tiempo que tarda un autobús en llegar."),
    T("El pes d'un nadó.", "El peso de un recién nacido."), T("El nombre de clients que entren en una botiga en una hora.", "El número de clientes que entran en una tienda en una hora."),
    T("La temperatura màxima d'un dia.", "La temperatura máxima de un día."), T("El nombre de cares en 10 llançaments d'una moneda.", "El número de caras en 10 lanzamientos de una moneda.")]),
    tasks(2, [r'\rest{%s}' % T('Discreta', 'Discreta'), r'\rest{%s}' % T('Contínua', 'Continua'), r'\rest{%s}' % T('Contínua', 'Continua'), r'\rest{%s}' % T('Discreta', 'Discreta'),
              r'\rest{%s}' % T('Contínua', 'Continua'), r'\rest{%s}' % T('Discreta', 'Discreta')])))

P2 = [Fr(1, 4), Fr(1, 2), Fr(1, 4)]; mu, m2, v = EV([0, 1, 2], P2); ck(mu, 1); ck(v, Fr(1, 2))
X.append(E(1, T("Llancem dues monedes i $X$ és el nombre de cares obtingudes.", "Lanzamos dos monedas y $X$ es el número de caras obtenidas.") + tasks(1, [
    T("Fes la taula de la funció de probabilitat i representa-la amb un diagrama de barres.", "Haz la tabla de la función de probabilidad y represéntala con un diagrama de barras."),
    T("Troba la funció de distribució $F(x)=P(X\\leq x)$ per a cada valor.", "Halla la función de distribución $F(x)=P(X\\leq x)$ para cada valor."),
    T("Calcula la mitjana i la desviació típica.", "Calcula la media y la desviación típica.")])
    + recorda(T(r"$\mu=\sum x_i\,p_i$; \ $\sigma^2=\sum x_i^2\,p_i-\mu^2$; \ $\sigma=\sqrt{\sigma^2}$.", r"$\mu=\sum x_i\,p_i$; \ $\sigma^2=\sum x_i^2\,p_i-\mu^2$; \ $\sigma=\sqrt{\sigma^2}$.")),
    tasks(1, [T(r'Espai mostral: CC, CX, XC, XX. \ $P(X=0)=\frac14$, $P(X=1)=\frac12$, $P(X=2)=\frac14$.', r'Espacio muestral: CC, CX, XC, XX. \ $P(X=0)=\frac14$, $P(X=1)=\frac12$, $P(X=2)=\frac14$.') + cen(bars([0, 1, 2], P2)),
              r'$F(0)=\frac14$, \ $F(1)=\frac34$, \ $F(2)=1$.',
              r'$\mu=0+\frac12+\frac24=\res{1}$; \ $\sigma^2=\frac12+1-1=\frac12\Rightarrow\res{\sigma=\sqrt{0{,}5}\approx0{,}707}$'])))

P3 = [Fr(k, 10) for k in (1, 2, 3, 4)]; mu, m2, v = EV([1, 2, 3, 4], P3); ck(mu, 3); ck(m2, 10); ck(v, 1); ck(P3[2] + P3[3], Fr(7, 10))
X.append(E(1, T("Una variable aleatòria $X$ pren els valors 1, 2, 3 i 4 amb probabilitats $k$, $2k$, $3k$ i $4k$.", "Una variable aleatoria $X$ toma los valores 1, 2, 3 y 4 con probabilidades $k$, $2k$, $3k$ y $4k$.") + tasks(3, [
    T('Calcula $k$.', 'Calcula $k$.'), T('Calcula $\\mu$ i $\\sigma$.', 'Calcula $\\mu$ y $\\sigma$.'), T('Calcula $P(X\\geq3)$ i $P(X\\lt3)$.', 'Calcula $P(X\\geq3)$ y $P(X\\lt3)$.')]),
    tasks(1, [r'$k+2k+3k+4k=1\Rightarrow10k=1\Rightarrow\res{k=0{,}1}$', r'$\mu=0{,}1+0{,}4+0{,}9+1{,}6=\res{3}$; \ $\sigma^2=0{,}1+0{,}8+2{,}7+6{,}4-3^2=1\Rightarrow\res{\sigma=1}$',
              r'$P(X\geq3)=0{,}3+0{,}4=\res{0{,}7}$; \ $P(X<3)=1-0{,}7=\res{0{,}3}$'])))

sums = {s: Fr(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s), 36) for s in range(2, 13)}
mu, m2, v = EV(list(sums), list(sums.values())); ck(mu, 7); ck(v, Fr(35, 6)); ck(sums[10] + sums[11] + sums[12], Fr(1, 6))
X.append(E(2, T("Llancem dos daus i $X$ és la suma dels punts. Fes la taula de la funció de probabilitat i calcula $P(X\\geq10)$, la mitjana i la desviació típica.",
                "Lanzamos dos dados y $X$ es la suma de los puntos. Haz la tabla de la función de probabilidad y calcula $P(X\\geq10)$, la media y la desviación típica."),
    r'\par{\centering\small\renewcommand{\arraystretch}{1.3}\begin{tabular}{c|' + 'c' * 11 + r'}$x_i$ & ' + ' & '.join(str(s) for s in sums) + r'\\\hline $p_i$ & ' + ' & '.join('$\\frac{%d}{36}$' % (p * 36) for p in sums.values()) + r'\end{tabular}\par}\smallskip' + '\n'
    + r'$P(X\geq10)=\frac{3+2+1}{36}=\res{\frac16}$; \ $\mu=\frac{252}{36}=\res{7}$ ' + T('(per simetria)', '(por simetría)') + r'; \ $\sigma^2=\frac{1974}{36}-49=\frac{35}{6}\Rightarrow\res{\sigma\approx2{,}415}$.'))
ck(sum(Fr(s) ** 2 * p for s, p in sums.items()), Fr(1974, 36))

P5 = [Fr(4, 6) * Fr(3, 5), 2 * Fr(4, 6) * Fr(2, 5), Fr(2, 6) * Fr(1, 5)]; mu, m2, v = EV([0, 1, 2], P5)
ck(P5[0], Fr(2, 5)); ck(P5[1], Fr(8, 15)); ck(P5[2], Fr(1, 15)); ck(mu, Fr(2, 3)); ck(v, Fr(16, 45))
X.append(E(2, T("Una urna conté 4 boles blanques i 2 de negres. Traiem dues boles sense reemplaçament i $X$ és el nombre de boles negres. Troba la funció de probabilitat de $X$, la mitjana i la desviació típica.",
                "Una urna contiene 4 bolas blancas y 2 negras. Sacamos dos bolas sin reemplazamiento y $X$ es el número de bolas negras. Halla la función de probabilidad de $X$, la media y la desviación típica.")
    + recorda(T("fes un diagrama d'arbre: la segona extracció depén de la primera.", "haz un diagrama de árbol: la segunda extracción depende de la primera.")),
    r'$P(X=0)=\frac46\cdot\frac35=\frac25$, \ $P(X=1)=\frac46\cdot\frac25+\frac26\cdot\frac45=\frac8{15}$, \ $P(X=2)=\frac26\cdot\frac15=\frac1{15}$. \ '
    + r'$\mu=\frac8{15}+\frac2{15}=\res{\frac23}$; \ $\sigma^2=\frac8{15}+\frac4{15}-\frac49=\frac{16}{45}\Rightarrow\res{\sigma\approx0{,}596}$.'))

P6 = [Fr(1, 6), Fr(1, 6), Fr(4, 6)]; mu, m2, v = EV([3, 1, -1], P6); ck(mu, 0); ck(v, Fr(7, 3))
X.append(E(2, T("En un joc es paga 1 euro per llançar un dau. Si ix un 6 es cobren 4 euros; si ix un 5, 2 euros; i en cas contrari no es cobra res. Siga $X$ el guany net del jugador. Calcula el guany esperat i la desviació típica. És un joc just?",
                "En un juego se paga 1 euro por lanzar un dado. Si sale un 6 se cobran 4 euros; si sale un 5, 2 euros; y en caso contrario no se cobra nada. Sea $X$ la ganancia neta del jugador. Calcula la ganancia esperada y la desviación típica. ¿Es un juego justo?")
    + recorda(T("el guany net és el que es cobra menys el que es paga. Un joc és just si el guany esperat és 0.", "la ganancia neta es lo que se cobra menos lo que se paga. Un juego es justo si la ganancia esperada es 0.")),
    T(r'$X$ pren els valors $3$, $1$ i $-1$ amb probabilitats $\frac16$, $\frac16$ i $\frac46$. \ $\mu=\frac{3+1-4}{6}=\res{0}$: \rest{és un joc just}. \ $\sigma^2=\frac{9+1+4}{6}=\frac73\Rightarrow\res{\sigma\approx1{,}53}$ euros.',
      r'$X$ toma los valores $3$, $1$ y $-1$ con probabilidades $\frac16$, $\frac16$ y $\frac46$. \ $\mu=\frac{3+1-4}{6}=\res{0}$: \rest{es un juego justo}. \ $\sigma^2=\frac{9+1+4}{6}=\frac73\Rightarrow\res{\sigma\approx1{,}53}$ euros.')))

a7, b7 = Fr(15, 100), Fr(35, 100); mu, m2, v = EV([0, 1, 2], [a7, Fr(1, 2), b7]); ck(a7 + b7, Fr(1, 2)); ck(mu, Fr(12, 10)); ck(v, Fr(46, 100))
X.append(E(3, T("Una variable aleatòria pren els valors 0, 1 i 2 amb probabilitats $a$, $0{,}5$ i $b$. Si la mitjana és $1{,}2$, calcula $a$, $b$ i la variància.",
                "Una variable aleatoria toma los valores 0, 1 y 2 con probabilidades $a$, $0{,}5$ y $b$. Si la media es $1{,}2$, calcula $a$, $b$ y la varianza."),
    r'$\left\{\begin{array}{l}a+0{,}5+b=1\\ 0{,}5+2b=1{,}2\end{array}\right.\Rightarrow\res{b=0{,}35},\ \res{a=0{,}15}$; \ $\sigma^2=0{,}5+4\cdot0{,}35-1{,}2^2=\res{0{,}46}$.'))

F8 = [Fr(1, 10), Fr(4, 10), Fr(8, 10), Fr(1)]; P8 = [F8[0]] + [F8[i] - F8[i - 1] for i in range(1, 4)]; mu, _, _ = EV([0, 1, 2, 3], P8)
ck(P8[1] + P8[2], Fr(7, 10)); ck(mu, Fr(17, 10))
X.append(E(2, T("La funció de distribució d'una variable discreta $X$ és $F(0)=0{,}1$, $F(1)=0{,}4$, $F(2)=0{,}8$ i $F(3)=1$ (i $X$ només pren aquests valors). Troba la funció de probabilitat, $P(1\\leq X\\leq2)$ i la mitjana.",
                "La función de distribución de una variable discreta $X$ es $F(0)=0{,}1$, $F(1)=0{,}4$, $F(2)=0{,}8$ y $F(3)=1$ (y $X$ solo toma estos valores). Halla la función de probabilidad, $P(1\\leq X\\leq2)$ y la media."),
    T(r'Restem valors consecutius: $p_0=0{,}1$, $p_1=0{,}3$, $p_2=0{,}4$, $p_3=0{,}2$. \ $P(1\leq X\leq2)=F(2)-F(0)=\res{0{,}7}$; \ $\mu=0{,}3+0{,}8+0{,}6=\res{1{,}7}$.',
      r'Restamos valores consecutivos: $p_0=0{,}1$, $p_1=0{,}3$, $p_2=0{,}4$, $p_3=0{,}2$. \ $P(1\leq X\leq2)=F(2)-F(0)=\res{0{,}7}$; \ $\mu=0{,}3+0{,}8+0{,}6=\res{1{,}7}$.')))

# =====================================================================
# 2. Distribució binomial
X = sec(T("La distribució binomial", "La distribución binomial"))
X.append(E(1, T("Digues si les variables següents segueixen una distribució binomial i, si és així, indica'n els paràmetres:", "Di si las variables siguientes siguen una distribución binomial y, si es así, indica sus parámetros:") + tasks(1, [
    T("Nombre de sisos en 12 llançaments d'un dau.", "Número de seises en 12 lanzamientos de un dado."),
    T("Nombre de boles roges en traure 3 boles, sense reemplaçament, d'una urna amb 4 roges i 6 blanques.", "Número de bolas rojas al sacar 3 bolas, sin reemplazamiento, de una urna con 4 rojas y 6 blancas."),
    T("Nombre de peces defectuoses en una mostra de 50, si el 2\\,\\% de la producció és defectuosa.", "Número de piezas defectuosas en una muestra de 50, si el 2\\,\\% de la producción es defectuosa."),
    T("Nombre de llançaments d'una moneda fins que ix la primera cara.", "Número de lanzamientos de una moneda hasta que sale la primera cara.")])
    + recorda(T("una binomial $B(n,p)$ compta els èxits en $n$ proves independents amb la mateixa probabilitat d'èxit $p$.", "una binomial $B(n,p)$ cuenta los éxitos en $n$ pruebas independientes con la misma probabilidad de éxito $p$.")),
    tasks(1, [T(r'\rest{Sí}: $B\left(12,\frac16\right)$.', r'\rest{Sí}: $B\left(12,\frac16\right)$.'), T(r'\rest{No}: sense reemplaçament, la probabilitat de roja canvia en cada extracció.', r'\rest{No}: sin reemplazamiento, la probabilidad de roja cambia en cada extracción.'),
              T(r'\rest{Sí}: $B(50;\ 0{,}02)$ (la producció és molt gran: les proves són pràcticament independents).', r'\rest{Sí}: $B(50;\ 0{,}02)$ (la producción es muy grande: las pruebas son prácticamente independientes).'),
              T(r'\rest{No}: el nombre de proves no està fixat.', r'\rest{No}: el número de pruebas no está fijado.')])))
d5 = [pmf(5, 1 / 6, 2), 1 - (5 / 6) ** 5]; ck(d5[0], 0.1608, 5e-5); ck(d5[1], 0.5981, 5e-5)
X.append(E(1, T("Es llança un dau 5 vegades. Calcula la probabilitat d'obtindre exactament dos cincs i la d'obtindre almenys un cinc.", "Se lanza un dado 5 veces. Calcula la probabilidad de obtener exactamente dos cincos y la de obtener al menos un cinco.")
    + recorda(r'$P(X=k)=\binom nk\,p^k\,q^{\,n-k}$, \ $q=1-p$.'),
    r'$X\sim B\left(5,\frac16\right)$: \ $P(X=2)=\binom52\left(\frac16\right)^2\left(\frac56\right)^3=10\cdot\frac{125}{7776}=' + N2(d5[0]) + r'$; \ $P(X\geq1)=1-\left(\frac56\right)^5=' + N2(d5[1]) + '$.'))
t8 = [pmf(8, 1 / 3, 4), 1 - pmf(8, 1 / 3, 0), 8 / 3, math.sqrt(8 * 2 / 9)]; ck(r4(t8[0]), 0.1707); ck(r4(t8[1]), 1 - 0.0390); ck(t8[3], 1.3333, 5e-5)
X.append(E(2, T("Un test té 8 preguntes amb 3 opcions cadascuna, de les quals només una és correcta. Un alumne contesta totes les preguntes a l'atzar.", "Un test tiene 8 preguntas con 3 opciones cada una, de las cuales solo una es correcta. Un alumno contesta todas las preguntas al azar.") + tasks(1, [
    T("Quina distribució segueix el nombre d'encerts? Quants encerts s'esperen? Quina és la desviació típica?", "¿Qué distribución sigue el número de aciertos? ¿Cuántos aciertos se esperan? ¿Cuál es la desviación típica?"),
    T("Calcula la probabilitat d'encertar-ne exactament 4 i la d'encertar-ne almenys una.", "Calcula la probabilidad de acertar exactamente 4 y la de acertar al menos una.")]),
    tasks(1, [T(r'$X\sim B\left(8,\frac13\right)$; \ $\mu=np=\frac83\approx\res{2{,}67}$ encerts; \ $\sigma=\sqrt{8\cdot\frac13\cdot\frac23}=\frac43\approx\res{1{,}33}$',
                r'$X\sim B\left(8,\frac13\right)$; \ $\mu=np=\frac83\approx\res{2{,}67}$ aciertos; \ $\sigma=\sqrt{8\cdot\frac13\cdot\frac23}=\frac43\approx\res{1{,}33}$'),
              r'$P(X=4)=\binom84\left(\frac13\right)^4\left(\frac23\right)^4=70\cdot\frac{16}{6561}=' + N2(t8[0]) + r'$; \ $P(X\geq1)=1-\left(\frac23\right)^8=' + N2(t8[1]) + '$'])))
cy = [pmf(10, 0.1, 2), pmf(10, 0.1, 0) + pmf(10, 0.1, 1)]; ck(cy[0], 0.1937, 5e-5); ck(cy[1], 0.7361, 5e-5)
X.append(E(2, pau(T('Castella i Lleó, PAU ordinària 2026', 'Castilla y León, PAU ordinaria 2026')) + T("El 90\\,\\% dels joves d'entre 25 i 34 anys compra per Internet. Una botiga fa una enquesta a 10 clients joves.", "El 90\\,\\% de los jóvenes de entre 25 y 34 años compra por Internet. Una tienda hace una encuesta a 10 clientes jóvenes.") + tasks(1, [
    T("Calcula la probabilitat que exactament 2 dels 10 clients no facen compres en línia.", "Calcula la probabilidad de que exactamente 2 de los 10 clientes no hagan compras en línea."),
    T("Calcula la probabilitat que menys de 2 clients no facen compres en línia.", "Calcula la probabilidad de que menos de 2 clientes no hagan compras en línea.")]),
    T(r'$X=$ «nombre de clients que no compren en línia» $\sim B(10;\ 0{,}1)$.', r'$X=$ «número de clientes que no compran en línea» $\sim B(10;\ 0{,}1)$.') + tasks(1, [
        r'$P(X=2)=\binom{10}{2}0{,}1^2\,0{,}9^8=' + N2(cy[0]) + '$', r'$P(X<2)=P(X=0)+P(X=1)=0{,}9^{10}+10\cdot0{,}1\cdot0{,}9^9=' + N2(cy[1]) + '$'])))
b5 = [r4(pmf(5, .25, k)) for k in range(6)]; ck(b5[0], .2373); ck(b5[1], .3955); ck(b5[2], .2637)
X.append(E(1, T("Siga $X\\sim B(5;\\ 0{,}25)$. Calcula amb la taula de la binomial:", "Sea $X\\sim B(5;\\ 0{,}25)$. Calcula con la tabla de la binomial:") + tasks(4, [r'$P(X=2)$', r'$P(X\leq1)$', r'$P(X\geq4)$', r'$P(X>0)$'])
    + recorda(T("la taula dona $P(X=x)$ per a $n\\leq9$. Per a les acumulades, suma caselles de la mateixa columna o fes el contrari.", "la tabla da $P(X=x)$ para $n\\leq9$. Para las acumuladas, suma casillas de la misma columna o haz el contrario.")),
    T(r'Bloc $n=5$, columna $p=0{,}25$:', r'Bloque $n=5$, columna $p=0{,}25$:') + tasks(2, [r'$' + N2(b5[2]) + '$', r'$0{,}2373+0{,}3955=' + N2(b5[0] + b5[1]) + '$', r'$0{,}0146+0{,}0010=' + N2(b5[4] + b5[5]) + '$', r'$1-0{,}2373=' + N2(1 - b5[0]) + '$'])))
ck(b5[4], .0146); ck(b5[5], .0010)
b7 = [r4(pmf(7, .2, k)) for k in range(2)]; ck(b7[0], .2097); ck(b7[1], .3670)
X.append(E(2, T("El 80\\,\\% dels clients d'una botiga està satisfet amb l'atenció rebuda. Es trien 7 clients a l'atzar. Calcula, amb la taula, la probabilitat que:", "El 80\\,\\% de los clientes de una tienda está satisfecho con la atención recibida. Se eligen 7 clientes al azar. Calcula, con la tabla, la probabilidad de que:") + tasks(1, [
    T("n'estiguen satisfets exactament 6;", "estén satisfechos exactamente 6;"), T("n'estiguen satisfets almenys 6;", "estén satisfechos al menos 6;"), T("n'estiguen satisfets com a molt 5.", "estén satisfechos como mucho 5.")]),
    T(r'$X\sim B(7;\ 0{,}8)$ no és a la taula ($p>0{,}5$). Comptem els no satisfets: $Y=7-X\sim B(7;\ 0{,}2)$.', r'$X\sim B(7;\ 0{,}8)$ no está en la tabla ($p>0{,}5$). Contamos los no satisfechos: $Y=7-X\sim B(7;\ 0{,}2)$.') + tasks(1, [
        r'$P(X=6)=P(Y=1)=' + N2(b7[1]) + '$', r'$P(X\geq6)=P(Y\leq1)=0{,}2097+0{,}3670=' + N2(b7[0] + b7[1]) + '$', r'$P(X\leq5)=1-P(X\geq6)=' + N2(1 - b7[0] - b7[1]) + '$'])))
b4 = [r4(pmf(4, .5, k)) for k in range(5)]; ck(b4[2], .375); ck(1 - b4[4], .9375)
X.append(E(1, T("En una família amb 4 fills, la probabilitat que cada fill siga xic és $0{,}5$. Calcula la probabilitat que hi haja exactament 2 xics, i que hi haja almenys una xica. Quants xics s'esperen?",
                "En una familia con 4 hijos, la probabilidad de que cada hijo sea chico es $0{,}5$. Calcula la probabilidad de que haya exactamente 2 chicos, y de que haya al menos una chica. ¿Cuántos chicos se esperan?"),
    T(r'$X=$ «nombre de xics» $\sim B(4;\ 0{,}5)$: \ $P(X=2)=\binom42\,0{,}5^4=' + N2(b4[2]) + r'$; \ $P(\text{almenys una xica})=1-P(X=4)=1-0{,}0625=' + N2(1 - b4[4]) + r'$; \ $\mu=4\cdot0{,}5=\res{2}$ xics.',
      r'$X=$ «número de chicos» $\sim B(4;\ 0{,}5)$: \ $P(X=2)=\binom42\,0{,}5^4=' + N2(b4[2]) + r'$; \ $P(\text{al menos una chica})=1-P(X=4)=1-0{,}0625=' + N2(1 - b4[4]) + r'$; \ $\mu=4\cdot0{,}5=\res{2}$ chicos.')))
m3 = [50 * .03, math.sqrt(50 * .03 * .97), .97 ** 50, .97 ** 50 + 50 * .03 * .97 ** 49]; ck(m3[2], 0.2181, 5e-5); ck(m3[3], 0.5553, 5e-5); ck(m3[1], 1.2062, 5e-5)
X.append(E(2, T("Una màquina fabrica un 3\\,\\% de peces defectuoses. Les peces s'envasen en caixes de 50.", "Una máquina fabrica un 3\\,\\% de piezas defectuosas. Las piezas se envasan en cajas de 50.") + tasks(1, [
    T("Quantes peces defectuoses hi ha, de mitjana, en una caixa? Amb quina desviació típica?", "¿Cuántas piezas defectuosas hay, de media, en una caja? ¿Con qué desviación típica?"),
    T("Quina és la probabilitat que una caixa no tinga cap peça defectuosa? I que en tinga com a molt una?", "¿Cuál es la probabilidad de que una caja no tenga ninguna pieza defectuosa? ¿Y de que tenga como mucho una?")]),
    tasks(1, [r'$X\sim B(50;\ 0{,}03)$: \ $\mu=50\cdot0{,}03=\res{1{,}5}$; \ $\sigma=\sqrt{50\cdot0{,}03\cdot0{,}97}\approx\res{1{,}21}$',
              r'$P(X=0)=0{,}97^{50}=' + N2(m3[2]) + r'$; \ $P(X\leq1)=0{,}97^{50}+50\cdot0{,}03\cdot0{,}97^{49}=' + N2(m3[3]) + '$'])))
ck(1 - .5 ** 7 > .99 and 1 - .5 ** 6 < .99, 1)
X.append(E(3, T("Quantes vegades, com a mínim, cal llançar una moneda perquè la probabilitat d'obtindre almenys una cara siga més gran que $0{,}99$?", "¿Cuántas veces, como mínimo, hay que lanzar una moneda para que la probabilidad de obtener al menos una cara sea mayor que $0{,}99$?"),
    T(r'$P(\text{almenys una cara})=1-0{,}5^n>0{,}99\iff0{,}5^n<0{,}01\iff2^n>100$. Com que $2^6=64$ i $2^7=128$: \ $\res{n=7}$ llançaments.',
      r'$P(\text{al menos una cara})=1-0{,}5^n>0{,}99\iff0{,}5^n<0{,}01\iff2^n>100$. Como $2^6=64$ y $2^7=128$: \ $\res{n=7}$ lanzamientos.')))

# =====================================================================
# 3. Variables contínues
X = sec(T("Variables aleatòries contínues. Funció de densitat", "Variables aleatorias continuas. Función de densidad"))
u = [Fr(2, 6), Fr(4, 6)]; ck(u[0], Fr(1, 3)); ck(u[1], Fr(2, 3))
X.append(E(1, T("Siga $f(x)=\\frac16$ si $2\\leq x\\leq8$ (i $f(x)=0$ en cas contrari).", "Sea $f(x)=\\frac16$ si $2\\leq x\\leq8$ (y $f(x)=0$ en otro caso).") + tasks(1, [
    T("Comprova que és una funció de densitat i dibuixa-la.", "Comprueba que es una función de densidad y dibújala."),
    T("Calcula $P(X\\lt4)$, $P(3\\leq X\\leq7)$ i $P(X=5)$.", "Calcula $P(X\\lt4)$, $P(3\\leq X\\leq7)$ y $P(X=5)$."), T("Quina és la mitjana?", "¿Cuál es la media?")])
    + recorda(T("la probabilitat és l'àrea davall de la funció de densitat; l'àrea total ha de ser 1.", "la probabilidad es el área bajo la función de densidad; el área total tiene que ser 1.")),
    tasks(1, [T(r'$f(x)\geq0$ i l\'àrea és un rectangle de base 6 i altura $\frac16$: $6\cdot\frac16=1$ \checkmark', r'$f(x)\geq0$ y el área es un rectángulo de base 6 y altura $\frac16$: $6\cdot\frac16=1$ \checkmark')
              + cen(dens([(2, 1 / 6), (8, 1 / 6)], 3, 7, [(2, '2'), (3, '3'), (7, '7'), (8, '8')], [(1 / 6, r'\frac16')], sx=0.5, sy=6)),
              r'$P(X<4)=2\cdot\frac16=\res{\frac13}$; \ $P(3\leq X\leq7)=4\cdot\frac16=\res{\frac23}$; \ $P(X=5)=\res{0}$', r'$\mu=\frac{2+8}{2}=\res{5}$'])))
k2 = Fr(1, 8); ck(4 * 4 * k2 / 2, 1); ck(2 * 2 * k2 / 2, Fr(1, 4)); ck(1 - 3 * 3 * k2 / 2, Fr(7, 16))
X.append(E(2, T("Calcula $k$ perquè $f(x)=k\\,x$ si $0\\leq x\\leq4$ (i 0 en cas contrari) siga una funció de densitat. Després calcula $P(X\\leq2)$ i $P(X\\gt3)$.",
                "Calcula $k$ para que $f(x)=k\\,x$ si $0\\leq x\\leq4$ (y 0 en otro caso) sea una función de densidad. Después calcula $P(X\\leq2)$ y $P(X\\gt3)$."),
    T(r'La regió és un triangle de base 4 i altura $f(4)=4k$: $\frac{4\cdot4k}{2}=8k=1\Rightarrow\res{k=\frac18}$. \ $P(X\leq2)$: triangle de base 2 i altura $f(2)=\frac14$: $\frac{2\cdot\frac14}{2}=\res{\frac14}$. \ $P(X>3)=1-P(X\leq3)=1-\frac{3\cdot\frac38}{2}=1-\frac9{16}=\res{\frac7{16}}$.',
      r'La región es un triángulo de base 4 y altura $f(4)=4k$: $\frac{4\cdot4k}{2}=8k=1\Rightarrow\res{k=\frac18}$. \ $P(X\leq2)$: triángulo de base 2 y altura $f(2)=\frac14$: $\frac{2\cdot\frac14}{2}=\res{\frac14}$. \ $P(X>3)=1-P(X\leq3)=1-\frac{3\cdot\frac38}{2}=1-\frac9{16}=\res{\frac7{16}}$.')
    + cen(dens([(0, 0), (4, .5)], 3, 4, [(0, '0'), (2, '2'), (3, '3'), (4, '4')], [(.5, r'\frac12')], sx=0.7, sy=3))))
X.append(E(1, T("El retard d'un tren (en minuts) es distribueix uniformement entre 0 i 20 minuts. Calcula la probabilitat que el retard siga superior a 15 minuts, que estiga entre 5 i 12 minuts, i el retard mitjà.",
                "El retraso de un tren (en minutos) se distribuye uniformemente entre 0 y 20 minutos. Calcula la probabilidad de que el retraso sea superior a 15 minutos, de que esté entre 5 y 12 minutos, y el retraso medio."),
    r'$X\sim U(0,20)$, $f(x)=\frac1{20}$: \ $P(X>15)=\frac5{20}=\res{0{,}25}$; \ $P(5\leq X\leq12)=\frac7{20}=\res{0{,}35}$; \ $\mu=\res{10}$ ' + T('minuts.', 'minutos.')))
ck(Fr(5, 20), .25); ck(Fr(7, 20), .35)
tri = [Fr(1, 2) * 1 * Fr(1, 4), 1 - 2 * Fr(1, 2) * 1 * Fr(1, 4), Fr(1, 2) * Fr(1, 2) * Fr(1, 8)]; ck(tri[0], Fr(1, 8)); ck(tri[1], Fr(3, 4)); ck(tri[2], Fr(1, 32))
X.append(E(2, T("La funció de densitat d'una variable $X$ és un triangle isòsceles amb base l'interval $[0,4]$ i el vèrtex en $x=2$.", "La función de densidad de una variable $X$ es un triángulo isósceles con base el intervalo $[0,4]$ y el vértice en $x=2$.") + tasks(1, [
    T("Quina altura ha de tindre el triangle?", "¿Qué altura tiene que tener el triángulo?"), T("Calcula $P(X\\leq1)$, $P(1\\leq X\\leq3)$ i $P(X\\geq3{,}5)$.", "Calcula $P(X\\leq1)$, $P(1\\leq X\\leq3)$ y $P(X\\geq3{,}5)$.")]),
    tasks(1, [r'$\frac{4\cdot h}{2}=1\Rightarrow\res{h=\frac12}$. ' + T('La recta de l\'esquerra és $f(x)=\\frac x4$.', 'La recta de la izquierda es $f(x)=\\frac x4$.'),
              T(r'$P(X\leq1)$: triangle de base 1 i altura $f(1)=\frac14$: $\res{\frac18}$; \ per simetria, $P(1\leq X\leq3)=1-2\cdot\frac18=\res{\frac34}$; \ $P(X\geq3{,}5)$: triangle de base $0{,}5$ i altura $\frac18$: $\res{\frac1{32}}$',
                r'$P(X\leq1)$: triángulo de base 1 y altura $f(1)=\frac14$: $\res{\frac18}$; \ por simetría, $P(1\leq X\leq3)=1-2\cdot\frac18=\res{\frac34}$; \ $P(X\geq3{,}5)$: triángulo de base $0{,}5$ y altura $\frac18$: $\res{\frac1{32}}$')
              + cen(dens([(0, 0), (2, .5), (4, 0)], 1, 3, [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4')], [(.5, r'\frac12')], sx=0.7, sy=3))])))
X.append(E(2, T("Raona si les funcions següents poden ser funcions de densitat (són 0 fora de l'interval indicat):", "Razona si las funciones siguientes pueden ser funciones de densidad (son 0 fuera del intervalo indicado):") + tasks(1, [
    r'$f(x)=0{,}5$ ' + T('en', 'en') + r' $[0,3]$', r'$f(x)=x-1$ ' + T('en', 'en') + r' $[0,2]$', r'$f(x)=0{,}25$ ' + T('en', 'en') + r' $[1,5]$']),
    tasks(1, [T(r'\rest{No}: l\'àrea és $3\cdot0{,}5=1{,}5\neq1$.', r'\rest{No}: el área es $3\cdot0{,}5=1{,}5\neq1$.'), T(r'\rest{No}: pren valors negatius (per exemple, $f(0)=-1$).', r'\rest{No}: toma valores negativos (por ejemplo, $f(0)=-1$).'),
              T(r'\rest{Sí}: és positiva i l\'àrea és $4\cdot0{,}25=1$ (és la uniforme $U(1,5)$).', r'\rest{Sí}: es positiva y el área es $4\cdot0{,}25=1$ (es la uniforme $U(1,5)$).')])))

# =====================================================================
# 4. La normal típica
X = sec(T("La distribució normal. La normal típica $N(0,1)$ i la seua taula", "La distribución normal. La normal tipificada $N(0,1)$ y su tabla"))
z4 = [Phi(1.53), 1 - Phi(2.05), Phi(-0.82), 1 - Phi(-1.2), Phi(1.5) - Phi(0.75), Phi(1) - Phi(-2), 2 * Phi(2.58) - 1]
ck(z4[0], .937); ck(z4[1], .0202); ck(z4[2], .2061); ck(z4[3], .8849); ck(z4[4], .1598); ck(z4[5], .8185); ck(z4[6], .9902)
X.append(E(1, T("Si $Z\\sim N(0,1)$, calcula amb la taula:", "Si $Z\\sim N(0,1)$, calcula con la tabla:") + tasks(3, [r'$P(Z\leq1{,}53)$', r'$P(Z>2{,}05)$', r'$P(Z<-0{,}82)$', r'$P(Z\geq-1{,}2)$', r'$P(0{,}75\leq Z\leq1{,}5)$', r'$P(-2< Z<1)$', r'$P(-2{,}58\leq Z\leq2{,}58)$'])
    + recorda(T(r"la taula dona $P(Z\leq z)$ per a $z\geq0$. \ $P(Z\geq z)=1-P(Z\leq z)$, \ $P(Z\leq-z)=1-P(Z\leq z)$. Dibuixa sempre la campana i l'àrea que busques.",
                r"la tabla da $P(Z\leq z)$ para $z\geq0$. \ $P(Z\geq z)=1-P(Z\leq z)$, \ $P(Z\leq-z)=1-P(Z\leq z)$. Dibuja siempre la campana y el área que buscas.")),
    tasks(2, [r'$' + N2(z4[0]) + '$', r'$1-0{,}9798=' + N2(z4[1]) + '$', r'$1-0{,}7939=' + N2(z4[2]) + '$', r'$P(Z\leq1{,}2)=' + N2(z4[3]) + '$', r'$0{,}9332-0{,}7734=' + N2(z4[4]) + '$',
              r'$0{,}8413-(1-0{,}9772)=' + N2(z4[5]) + '$', r'$2\cdot0{,}9951-1=' + N2(z4[6]) + '$'])))
r3 = [2 * Phi(1) - 1, 2 * Phi(2) - 1, 2 * Phi(3) - 1]; ck(r3[0], .6826); ck(r3[1], .9544); ck(r3[2], .9974)
X.append(E(1, T("Comprova amb la taula la regla 68--95--99,7: calcula $P(-1\\leq Z\\leq1)$, $P(-2\\leq Z\\leq2)$ i $P(-3\\leq Z\\leq3)$. Què signifiquen aquests resultats per a una variable $X\\sim N(\\mu,\\sigma)$?",
                "Comprueba con la tabla la regla 68--95--99,7: calcula $P(-1\\leq Z\\leq1)$, $P(-2\\leq Z\\leq2)$ y $P(-3\\leq Z\\leq3)$. ¿Qué significan estos resultados para una variable $X\\sim N(\\mu,\\sigma)$?"),
    r'$2\cdot0{,}8413-1=' + N2(r3[0]) + r'$; \ $2\cdot0{,}9772-1=' + N2(r3[1]) + r'$; \ $2\cdot0{,}9987-1=' + N2(r3[2]) + r'$. \ '
    + T(r'Entre $\mu\pm\sigma$ hi ha prop del 68\,\% dels valors; entre $\mu\pm2\sigma$, el 95\,\%, i entre $\mu\pm3\sigma$, gairebé tots (99,7\,\%).', r'Entre $\mu\pm\sigma$ hay cerca del 68\,\% de los valores; entre $\mu\pm2\sigma$, el 95\,\%, y entre $\mu\pm3\sigma$, casi todos (99,7\,\%).')
    + cen(gauss([(-1, 1)], [(-1, '-1'), (0, '0'), (1, '1')]), gauss([(-2, 2)], [(-2, '-2'), (0, '0'), (2, '2')]))))
ck(zinv(.8907), 1.23); ck(zinv(.9495), 1.64); ck(zinv(.25), -.67); ck(zinv(.95), 1.645)
X.append(E(2, T("Si $Z\\sim N(0,1)$, troba el valor de $k$ en cada cas:", "Si $Z\\sim N(0,1)$, halla el valor de $k$ en cada caso:") + tasks(2, [r'$P(Z\leq k)=0{,}8907$', r'$P(Z\geq k)=0{,}0505$', r'$P(Z\leq k)=0{,}25$', r'$P(-k\leq Z\leq k)=0{,}9$'])
    + recorda(T("busca la probabilitat \\emph{dins} de la taula; si és menor que 0,5, $k$ és negatiu.", "busca la probabilidad \\emph{dentro} de la tabla; si es menor que 0,5, $k$ es negativo.")),
    tasks(1, [T(r'El valor és a la taula: $\res{k=1{,}23}$', r'El valor está en la tabla: $\res{k=1{,}23}$'), r'$P(Z\leq k)=0{,}9495\Rightarrow\res{k=1{,}64}$',
              T(r'$P(Z\leq-k)=0{,}75$: més pròxim $0{,}7486\to0{,}67$, així que $\res{k\approx-0{,}67}$', r'$P(Z\leq-k)=0{,}75$: más próximo $0{,}7486\to0{,}67$, así que $\res{k\approx-0{,}67}$'),
              T(r'$2P(Z\leq k)-1=0{,}9\Rightarrow P(Z\leq k)=0{,}95$: entre $1{,}64$ i $1{,}65$, $\res{k\approx1{,}645}$', r'$2P(Z\leq k)-1=0{,}9\Rightarrow P(Z\leq k)=0{,}95$: entre $1{,}64$ y $1{,}65$, $\res{k\approx1{,}645}$')])))
q4 = [2 * (1 - Phi(1.5)), Phi(0) - Phi(-0.44), 1 - Phi(-2.35)]; ck(q4[0], .1336); ck(q4[1], .17); ck(q4[2], .9906)
X.append(E(2, T("Si $Z\\sim N(0,1)$, calcula $P(Z\\leq-1{,}5\\ \\text{o}\\ Z\\geq1{,}5)$, \\ $P(-0{,}44\\leq Z\\leq0)$ \\ i \\ $P(Z\\geq-2{,}35)$. Fes un dibuix de cada àrea.",
                "Si $Z\\sim N(0,1)$, calcula $P(Z\\leq-1{,}5\\ \\text{o}\\ Z\\geq1{,}5)$, \\ $P(-0{,}44\\leq Z\\leq0)$ \\ y \\ $P(Z\\geq-2{,}35)$. Haz un dibujo de cada área."),
    r'$2\,(1-0{,}9332)=' + N2(q4[0]) + r'$; \ $0{,}6700-0{,}5=' + N2(q4[1]) + r'$; \ $P(Z\leq2{,}35)=' + N2(q4[2]) + '$.'
    + cen(gauss([(None, -1.5), (1.5, None)], [(-1.5, '-1{,}5'), (1.5, '1{,}5')]), gauss([(-0.44, 0)], [(-0.44, '-0{,}44'), (0, '0')]), gauss([(-2.35, None)], [(-2.35, '-2{,}35'), (0, '0')]))))

# =====================================================================
# 5. Tipificació
X = sec(T("Tipificació. Problemes amb la normal", "Tipificación. Problemas con la normal"))
q = {}
q['b25'] = [Phi(zs(25, 15, 10)), Phi(zs(25, 15, 10)) - Phi(zs(5, 15, 10))]; ck(q['b25'][0], .8413); ck(q['b25'][1], .6826)
X.append(E(1, pau(T('Illes Balears, PBAU extraordinària 2025', 'Illes Balears, PBAU extraordinaria 2025')) + T("Quan un client entra en una botiga d'electrodomèstics, el temps (en minuts) que hi passa segueix una distribució $N(15,10)$.", "Cuando un cliente entra en una tienda de electrodomésticos, el tiempo (en minutos) que pasa en ella sigue una distribución $N(15,10)$.") + tasks(1, [
    T("Quina és la probabilitat que un client estiga dins de la botiga 25 minuts o menys?", "¿Cuál es la probabilidad de que un cliente esté dentro de la tienda 25 minutos o menos?"),
    T("Quina és la probabilitat que un client estiga dins de la botiga entre 5 i 25 minuts?", "¿Cuál es la probabilidad de que un cliente esté dentro de la tienda entre 5 y 25 minutos?")])
    + recorda(T(r"si $X\sim N(\mu,\sigma)$, aleshores $Z=\dfrac{X-\mu}{\sigma}\sim N(0,1)$. Arredoneix $z$ a dues decimals i fes servir la taula.", r"si $X\sim N(\mu,\sigma)$, entonces $Z=\dfrac{X-\mu}{\sigma}\sim N(0,1)$. Redondea $z$ a dos decimales y usa la tabla.")),
    tasks(1, [r'$P(X\leq25)=P\left(Z\leq\frac{25-15}{10}\right)=P(Z\leq1)=' + N2(q['b25'][0]) + '$', r'$P(-1\leq Z\leq1)=2\cdot0{,}8413-1=' + N2(q['b25'][1]) + '$'])
    + cen(gauss([(-1, 1)], [(-1, '-1'), (0, '0'), (1, '1')]))))
q['b21'] = [1 - Phi(zs(80, 70, 15)), Phi(zs(50, 70, 15)), Phi(zs(120, 70, 15)) - Phi(zs(60, 70, 15))]; ck(q['b21'][0], .2514); ck(q['b21'][1], .0918); ck(q['b21'][2], .7482)
X.append(E(1, pau(T('Illes Balears, PBAU ordinària 2021', 'Illes Balears, PBAU ordinaria 2021')) + T("El pes de les persones d'un col·legi major segueix una llei normal de mitjana 70 kg i desviació típica 15 kg. Triem una persona a l'atzar; calcula la probabilitat que:", "El peso de las personas de un colegio mayor sigue una ley normal de media 70 kg y desviación típica 15 kg. Elegimos una persona al azar; calcula la probabilidad de que:")
    + tasks(3, [T("pese més de 80 kg;", "pese más de 80 kg;"), T("pese menys de 50 kg;", "pese menos de 50 kg;"), T("pese entre 60 i 120 kg.", "pese entre 60 y 120 kg.")]),
    tasks(1, [r'$P(Z>0{,}67)=1-0{,}7486=' + N2(q['b21'][0]) + '$', r'$P(Z<-1{,}33)=1-0{,}9082=' + N2(q['b21'][1]) + '$', r'$P(-0{,}67< Z<3{,}33)=0{,}9996-0{,}2514=' + N2(q['b21'][2]) + '$'])))
q['ci'] = [1 - Phi(2), 2 * Phi(1) - 1]; ck(2000 * q['ci'][0], 45.6, 1e-6); ck(2000 * q['ci'][1], 1365.2, 1e-6)
X.append(E(1, T("En una universitat hi ha 2000 alumnes i el seu quocient intel·lectual (QI) segueix una distribució $N(100,15)$. Quants alumnes s'espera que tinguen un QI superior a 130? I entre 85 i 115?",
                "El coeficiente intelectual (CI) de los 2000 alumnos de una universidad sigue una distribución $N(100,15)$. ¿Cuántos alumnos se espera que tengan un CI superior a 130? ¿Y entre 85 y 115?"),
    r'$P(X>130)=P(Z>2)=1-0{,}9772=0{,}0228$; \ $2000\cdot0{,}0228=45{,}6\approx\res{46}$ ' + T('alumnes', 'alumnos') + r'. \ $P(85\leq X\leq115)=P(-1\leq Z\leq1)=0{,}6826$; \ $2000\cdot0{,}6826\approx\res{1365}$ ' + T('alumnes.', 'alumnos.')))
q['b23'] = 1 - Phi(zs(1.76, 1.62, .11)); ck(q['b23'], .102, 1e-4)
X.append(E(2, pau(T('Illes Balears, PBAU extraordinària 2023', 'Illes Balears, PBAU extraordinaria 2023')) + T("En una població, l'altura dels homes segueix una normal de mitjana 1,76 m i desviació típica 0,12 m, i la de les dones, una normal de mitjana 1,62 m i desviació típica 0,11 m.", "En una población, la altura de los hombres sigue una normal de media 1,76 m y desviación típica 0,12 m, y la de las mujeres, una normal de media 1,62 m y desviación típica 0,11 m.") + tasks(1, [
    T("Triem un home a l'atzar. Quina és la probabilitat que la seua altura siga major o igual que 1,76 m?", "Elegimos un hombre al azar. ¿Cuál es la probabilidad de que su altura sea mayor o igual que 1,76 m?"),
    T("Triem una dona a l'atzar. Quina és la probabilitat que la seua altura siga major o igual que 1,76 m?", "Elegimos una mujer al azar. ¿Cuál es la probabilidad de que su altura sea mayor o igual que 1,76 m?"),
    T("Què és més probable, que un home mesure menys d'1,76 m o que ho faça una dona?", "¿Qué es más probable, que un hombre mida menos de 1,76 m o que lo haga una mujer?")]),
    tasks(1, [T(r'1,76 és la mitjana dels homes: $\res{0{,}5}$', r'1,76 es la media de los hombres: $\res{0{,}5}$'), r'$P\left(Z\geq\frac{1{,}76-1{,}62}{0{,}11}\right)=P(Z\geq1{,}27)=1-0{,}8980=' + N2(q['b23']) + '$',
              T(r'Home: $0{,}5$; dona: $1-0{,}102=0{,}898$. \rest{És més probable que una dona mesure menys d\'1,76 m.}', r'Hombre: $0{,}5$; mujer: $1-0{,}102=0{,}898$. \rest{Es más probable que una mujer mida menos de 1,76 m.}')])))
q['c19'] = [1 - Phi(zs(62, 44, 18)), Phi(zs(40, 44, 18)), Phi(zs(30, 44, 18)) - Phi(zs(18, 44, 18))]; ck(250 * q['c19'][0], 40, 0.5); ck(250 * q['c19'][1], 103, 0.5); ck(250 * q['c19'][2], 36, 0.5)
X.append(E(2, pau(T('Canàries, EBAU juliol 2019', 'Canarias, EBAU julio 2019')) + T("En una empresa hi ha 250 empleats. La seua edat segueix una normal de mitjana 44 anys i desviació típica 18 anys.", "En una empresa hay 250 empleados. Su edad sigue una normal de media 44 años y desviación típica 18 años.") + tasks(1, [
    T("Quants empleats s'espera que tinguen més de 62 anys?", "¿Cuántos empleados se espera que tengan más de 62 años?"), T("Quants empleats s'espera que tinguen menys de 40 anys?", "¿Cuántos empleados se espera que tengan menos de 40 años?"),
    T("Quants empleats podrien aconseguir el carnet jove de transport si el requisit és ser major d'edat i no haver complit els 30 anys?", "¿Cuántos empleados podrían conseguir el carnet joven de transporte si el requisito es ser mayor de edad y no haber cumplido los 30 años?")]),
    T("Multipliquem cada probabilitat pel total d'empleats:", "Multiplicamos cada probabilidad por el total de empleados:") + tasks(1, [
        r'$P(Z>1)=0{,}1587$; \ $250\cdot0{,}1587\approx\res{40}$', r'$P(Z<-0{,}22)=1-0{,}5871=0{,}4129$; \ $250\cdot0{,}4129\approx\res{103}$',
        r'$P(18\leq X<30)=P(-1{,}44\leq Z<-0{,}78)=(1-0{,}7823)-(1-0{,}9251)=0{,}1428$; \ $250\cdot0{,}1428\approx\res{36}$'])))
z, k = zinv(0.9), 116 + zinv(0.9) * 42; xr = Phi(zs(200, 116, 42)) - Phi(zs(100, 116, 42)); ck(xr, .6252); ck(k, 169.76, 1e-6)
X.append(E(2, pau(T('Illes Balears, PAU extraordinària 2026', 'Illes Balears, PAU extraordinaria 2026')) + T("El temps que cada jove d'una població dedica cada dia a les xarxes socials segueix una normal de mitjana 116 minuts i desviació típica 42 minuts.", "El tiempo que cada joven de una población dedica cada día a las redes sociales sigue una normal de media 116 minutos y desviación típica 42 minutos.") + tasks(1, [
    T("Quina proporció de joves dedica entre 100 i 200 minuts a les xarxes socials?", "¿Qué proporción de jóvenes dedica entre 100 y 200 minutos a las redes sociales?"),
    T("En Joan és del 10\\,\\% de joves que més temps hi dedica. Quants minuts hi dedica, com a mínim?", "Juan es del 10\\,\\% de jóvenes que más tiempo les dedica. ¿Cuántos minutos les dedica, como mínimo?")])
    + recorda(T(r"en un problema invers busquem la probabilitat dins de la taula, llegim $z$ i desfem la tipificació: $x=\mu+z\,\sigma$.", r"en un problema inverso buscamos la probabilidad dentro de la tabla, leemos $z$ y deshacemos la tipificación: $x=\mu+z\,\sigma$.")),
    tasks(1, [r'$P(-0{,}38< Z<2)=0{,}9772-(1-0{,}6480)=' + N2(xr) + r'$: ' + T('el', 'el') + r' $62{,}52\,\%$.',
              T(r'$P(X\geq k)=0{,}1\Rightarrow P(Z\leq z)=0{,}9$: més pròxim $0{,}8997\to z=1{,}28$; \ $k=116+1{,}28\cdot42=\res{169{,}76}$ minuts.', r'$P(X\geq k)=0{,}1\Rightarrow P(Z\leq z)=0{,}9$: más próximo $0{,}8997\to z=1{,}28$; \ $k=116+1{,}28\cdot42=\res{169{,}76}$ minutos.')])
    + cen(gauss([(1.28, None)], [(0, '0'), (1.28, '1{,}28')]))))
zq = zinv(.75); ck(163 - zq * 7, 158.31, 1e-6)
X.append(E(2, pau(T('País Basc, EAU ordinària 2020', 'País Vasco, EAU ordinaria 2020')) + T("L'altura de les dones d'un país segueix una normal de mitjana 163 cm i desviació típica 7 cm. Una empresa de disfresses vol fer quatre talles, cadascuna adequada per al 25\\,\\% de les dones. Quines altures marquen el pas d'una talla a una altra?",
    "La altura de las mujeres de un país sigue una normal de media 163 cm y desviación típica 7 cm. Una empresa de disfraces quiere hacer cuatro tallas, cada una adecuada para el 25\\,\\% de las mujeres. ¿Qué alturas marcan el paso de una talla a otra?"),
    T(r'Són els quartils: $z=\pm0{,}67$ (per a $0{,}75$) i $z=0$. \ $163-0{,}67\cdot7=\res{158{,}31}$, \ $\res{163}$ \ i \ $163+0{,}67\cdot7=\res{167{,}69}$ cm.', r'Son los cuartiles: $z=\pm0{,}67$ (para $0{,}75$) y $z=0$. \ $163-0{,}67\cdot7=\res{158{,}31}$, \ $\res{163}$ \ y \ $163+0{,}67\cdot7=\res{167{,}69}$ cm.')))
z, k = zinv(.6), 250 + zinv(.6) * 50; tr = 6000 * (1 - Phi(zs(280, 250, 50))); ck(k, 262.5); ck(tr, 1645.8, 1e-6)
X.append(E(2, pau(T('País Basc, EAU ordinària 2020', 'País Vasco, EAU ordinaria 2020')) + T("El pes de les truites d'una piscifactoria segueix una normal de mitjana 250 g i desviació típica 50 g. Només són aptes per a la venda les que superen un pes determinat.", "El peso de las truchas de una piscifactoría sigue una normal de media 250 g y desviación típica 50 g. Solo son aptas para la venta las que superan un peso determinado.") + tasks(1, [
    T("Quin ha de ser aquest pes si es vol que el 40\\,\\% de les truites siguen aptes per a la venda?", "¿Cuál tiene que ser ese peso si se quiere que el 40\\,\\% de las truchas sean aptas para la venta?"),
    T("Si aquest pes s'estableix en 280 g i a la piscifactoria hi ha 6000 truites, quantes se'n podran vendre?", "Si ese peso se establece en 280 g y en la piscifactoría hay 6000 truchas, ¿cuántas se podrán vender?")]),
    tasks(1, [T(r'$P(Z\leq z)=0{,}6$: més pròxim $0{,}5987\to z=0{,}25$; \ $250+0{,}25\cdot50=\res{262{,}5}$ g', r'$P(Z\leq z)=0{,}6$: más próximo $0{,}5987\to z=0{,}25$; \ $250+0{,}25\cdot50=\res{262{,}5}$ g'),
              r'$P(Z>0{,}6)=1-0{,}7257=0{,}2743$; \ $6000\cdot0{,}2743\approx\res{1646}$ ' + T('truites', 'truchas')])))
ck(170 / zinv(.8023), 200)
X.append(E(3, pau(T('Castella i Lleó, EBAU juliol 2018', 'Castilla y León, EBAU julio 2018')) + T("En una empresa, el salari mitjà mensual és de 1400 euros i el 80,23\\,\\% dels treballadors cobra menys de 1570 euros. Calcula la desviació típica del salari, suposant que segueix una distribució normal.",
    "En una empresa, el salario medio mensual es de 1400 euros y el 80,23\\,\\% de los trabajadores cobra menos de 1570 euros. Calcula la desviación típica del salario, suponiendo que sigue una distribución normal."),
    r'$P\left(Z<\frac{170}{\sigma}\right)=0{,}8023\Rightarrow\frac{170}{\sigma}=0{,}85\Rightarrow\res{\sigma=200}$ euros.'))
zr = zinv(.88493); ck(183 - zr * 6.5, 175.2); ck(183 - 2 * zr * 6.5, 167.4)
X.append(E(3, pau(T('La Rioja, EBAU ordinària 2023', 'La Rioja, EBAU ordinaria 2023')) + T("L'estatura dels policies de França segueix una normal de desviació típica 6,5 cm, de manera que l'11,507\\,\\% mesura més de 183 cm.", "La estatura de los policías de Francia sigue una normal de desviación típica 6,5 cm, de manera que el 11,507\\,\\% mide más de 183 cm.") + tasks(1, [
    T("Calcula la mitjana de l'estatura.", "Calcula la media de la estatura."), T("Troba l'estatura que és superada pel 88,493\\,\\% dels policies.", "Halla la estatura que es superada por el 88,493\\,\\% de los policías.")]),
    tasks(1, [r'$P\left(Z\leq\frac{183-\mu}{6{,}5}\right)=0{,}88493\approx0{,}8849\Rightarrow\frac{183-\mu}{6{,}5}=1{,}2\Rightarrow\res{\mu=175{,}2}$ cm',
              T(r'Per simetria, $z=-1{,}2$: \ $175{,}2-1{,}2\cdot6{,}5=\res{167{,}4}$ cm', r'Por simetría, $z=-1{,}2$: \ $175{,}2-1{,}2\cdot6{,}5=\res{167{,}4}$ cm')])))

# =====================================================================
# 6. Aproximació de la binomial a la normal
X = sec(T("Aproximació de la distribució binomial a la normal", "Aproximación de la distribución binomial a la normal"))
ap = [aprox(100, .2, None, 15.5), aprox(100, .2, 19.5, 20.5), aprox(100, .2, 24.5, None)]
ck(ap[0], .1292); ck(ap[1], .1034); ck(ap[2], .1292); ck(abs(ap[0] - sum(pmf(100, .2, k) for k in range(16))) < 0.02, 1)
X.append(E(1, T("Siga $X\\sim B(100;\\ 0{,}2)$.", "Sea $X\\sim B(100;\\ 0{,}2)$.") + tasks(1, [
    T("Comprova que es pot aproximar per una normal i digues quina.", "Comprueba que se puede aproximar por una normal y di cuál."), T("Calcula aproximadament $P(X\\leq15)$, $P(X=20)$ i $P(X\\geq25)$.", "Calcula aproximadamente $P(X\\leq15)$, $P(X=20)$ y $P(X\\geq25)$.")])
    + recorda(T(r"si $np\geq5$ i $nq\geq5$, $B(n,p)\approx N\left(np,\sqrt{npq}\right)$. No oblides la correcció de continuïtat ($\pm0{,}5$).", r"si $np\geq5$ y $nq\geq5$, $B(n,p)\approx N\left(np,\sqrt{npq}\right)$. No olvides la corrección de continuidad ($\pm0{,}5$).")),
    tasks(1, [r'$np=20\geq5$, $nq=80\geq5$: \ $\res{X\'\sim N(20,\,4)}$ ($\sigma=\sqrt{100\cdot0{,}2\cdot0{,}8}=4$)',
              r'$P(X\leq15)\approx P(X\'\leq15{,}5)=P(Z\leq-1{,}13)=1-0{,}8708=' + N2(ap[0]) + r'$; \ $P(X=20)\approx P(19{,}5\leq X\'\leq20{,}5)=P(-0{,}13\leq Z\leq0{,}13)=' + N2(ap[1]) + r'$; \ $P(X\geq25)\approx P(X\'\geq24{,}5)=P(Z\geq1{,}13)=' + N2(ap[2]) + '$'])))
pa = aprox(400, .5, None, 189.5); ck(pa, .1469)
X.append(E(1, T("Llancem una moneda equilibrada 400 vegades. Calcula la probabilitat d'obtindre menys de 190 cares.", "Lanzamos una moneda equilibrada 400 veces. Calcula la probabilidad de obtener menos de 190 caras."),
    r'$X\sim B(400;\ 0{,}5)\approx N(200,\,10)$: \ $P(X<190)=P(X\leq189)\approx P(X\'\leq189{,}5)=P(Z\leq-1{,}05)=1-0{,}8531=' + N2(pa) + '$.'))
tf = aprox(100, .5, 59.5, None); ck(tf, .0287)
X.append(E(2, T("Un examen té 100 preguntes de vertader o fals. Per aprovar cal encertar-ne almenys 60. Quina és la probabilitat d'aprovar contestant totes les preguntes a l'atzar?",
                "Un examen tiene 100 preguntas de verdadero o falso. Para aprobar hay que acertar al menos 60. ¿Cuál es la probabilidad de aprobar contestando todas las preguntas al azar?"),
    r'$X\sim B(100;\ 0{,}5)\approx N(50,\,5)$: \ $P(X\geq60)\approx P(X\'\geq59{,}5)=P(Z\geq1{,}9)=1-0{,}9713=' + N2(tf) + '$.'
    + cen(gauss([(1.9, None)], [(0, '0'), (1.9, '1{,}9')]))))
a26 = aprox(1350, .4, 499.5, 580.5); ck(a26, .9756)
X.append(E(2, pau(T('Andalusia, PAU ordinària 2026 (adaptat)', 'Andalucía, PAU ordinaria 2026 (adaptado)')) + T("Un experiment té èxit amb probabilitat 0,4 i es repeteix 1350 vegades de manera independent. Siga $X$ el nombre d'èxits.", "Un experimento tiene éxito con probabilidad 0,4 y se repite 1350 veces de manera independiente. Sea $X$ el número de éxitos.") + tasks(1, [
    T("Quina distribució segueix $X$?", "¿Qué distribución sigue $X$?"), T("Calcula la probabilitat que $X$ siga major que 499 i menor o igual que 580.", "Calcula la probabilidad de que $X$ sea mayor que 499 y menor o igual que 580.")]),
    tasks(1, [r'$\res{X\sim B(1350;\ 0{,}4)}$', r'$\mu=540$, $\sigma=\sqrt{324}=18$: \ $P(500\leq X\leq580)\approx P(499{,}5\leq X\'\leq580{,}5)=P(-2{,}25\leq Z\leq2{,}25)=2\cdot0{,}9878-1=' + N2(a26) + '$'])))
cn = aprox(2500, .1, 269.5, None); ck(cn, .0968)
X.append(E(2, pau(T('Canàries, EBAU ordinària 2022 (adaptat)', 'Canarias, EBAU ordinaria 2022 (adaptado)')) + T("Una companyia d'assegurances té assegurats 2500 cotxes. La probabilitat que un cotxe tinga un accident al llarg d'un any és 0,1. Quants accidents s'esperen? Quina és la probabilitat que l'any que ve tinguen un accident almenys 270 cotxes?",
    "Una compañía de seguros tiene asegurados 2500 coches. La probabilidad de que un coche tenga un accidente a lo largo de un año es 0,1. ¿Cuántos accidentes se esperan? ¿Cuál es la probabilidad de que el año que viene tengan un accidente al menos 270 coches?"),
    r'$X\sim B(2500;\ 0{,}1)$: \ $\mu=\res{250}$ ' + T('accidents', 'accidentes') + r'; \ $\sigma=\sqrt{225}=15$. \ $P(X\geq270)\approx P(X\'\geq269{,}5)=P(Z\geq1{,}3)=1-0{,}9032=' + N2(cn) + '$.'))
ex3 = [sum(pmf(50, .3, k) for k in range(10, 21)), aprox(50, .3, 9.5, 20.5)]; ck(ex3[1], 2 * Phi(1.7) - 1); ck(ex3[0], .9120, 5e-5)
X.append(E(3, T("Siga $X\\sim B(50;\\ 0{,}3)$. Calcula $P(10\\leq X\\leq20)$ amb l'aproximació normal. Amb un ordinador s'obté el valor exacte, $" + d4(ex3[0]) + "$. Quin error es comet?",
                "Sea $X\\sim B(50;\\ 0{,}3)$. Calcula $P(10\\leq X\\leq20)$ con la aproximación normal. Con un ordenador se obtiene el valor exacto, $" + d4(ex3[0]) + "$. ¿Qué error se comete?"),
    r'$np=15$, $nq=35$: \ $N(15;\ \sqrt{10{,}5}\approx3{,}24)$. \ $P(9{,}5\leq X\'\leq20{,}5)=P(-1{,}70\leq Z\leq1{,}70)=2\cdot0{,}9554-1=' + N2(ex3[1]) + r'$. ' + T('L\'error és de només', 'El error es de solo') + r' $' + d4(abs(ex3[1] - ex3[0])) + '$.'))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("pdfkeywords={variable aleatòria, funció de probabilitat, funció de distribució, esperança, distribució binomial, funció de densitat, distribució uniforme, distribució normal, normal típica, tipificació, aproximació de la binomial a la normal}",
       "pdfkeywords={variable aleatoria, función de probabilidad, función de distribución, esperanza, distribución binomial, función de densidad, distribución uniforme, distribución normal, normal tipificada, tipificación, aproximación de la binomial a la normal}")
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les CCSS I}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\usepackage{enumitem}' + '\n'
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
pre += (r'\providecommand{\gt}{>}\providecommand{\lt}{<}' + '\n% quadre de recordatori (només a la fitxa d\'exercicis)\n'
        r'\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{'
        + T('Recorda', 'Recuerda') + r':}\ #1\end{tcolorbox}}' + '\n'
        + r'\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }' + '\n')

def fix(t):
    """Fora dels dibuixos: l'espai després de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
        # dins de les caixes de resultat, fraccions xicotetes (\tfrac) perquè la caixa no siga tan alta
        parts[i] = re.sub(r'(\\res\{[^{}]*?)\\frac(?=[{0-9])', r'\1\\tfrac', parts[i])
    return ''.join(parts)

TIT = T("Distribucions de probabilitat", "Distribuciones de probabilidad")
def build(sol):
    npau = sum(1 for _, exs in S_ for _, q_, _ in exs if '\\pau{' in q_)
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 10: %s' % (t, TIT), capcalera='%s · Unidad 10: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-ccss')
        cap = assignatura('1batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 10' if sol else 'Ficha de ejercicios · Unidad 10') + '}'
    else:
        t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                        "pdftitle={%s de la unitat 10: %s. 1r de Batxillerat CCSS}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 10: %s · 1r Batxillerat CCSS" % (t, TIT))
        assert 'Unitat 10' in p and 'unitat 10' in p
        cap = r'\capcalera{Matemàtiques CCSS}{1r Batx}{' + ('Solucions de la fitxa · Unitat 10' if sol else "Fitxa d'exercicis · Unitat 10") + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{11}% que el títol d\'una secció no quede sol al final del full\n\\input{../comu/fentmates.tex}\n\\fmcurs{1batx-ccss}\n\n'
               '\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '{\\raggedright ' + TIT + '}\n')
    if not sol:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.9cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Les probabilitats de la normal s'han calculat arredonint $z$ a dues decimals i llegint la taula $N(0,1)$, com es fa a la PAU. En els problemes inversos s'ha pres el valor de la taula més pròxim; per això alguns resultats poden diferir lleugerament dels que s'obtenen amb una calculadora.",
               r"Las probabilidades de la normal se han calculado redondeando $z$ a dos decimales y leyendo la tabla $N(0,1)$, como se hace en la PAU. En los problemas inversos se ha tomado el valor de la tabla más próximo; por eso algunos resultados pueden diferir ligeramente de los que se obtienen con una calculadora.")
             if sol else T(r"Resol els exercicis al quadern mostrant tots els passos: identifica la variable aleatòria i la seua distribució, fes un dibuix de l'àrea que busques i arredoneix $z$ a dues decimals. Fes servir les taules de la binomial i de la normal $N(0,1)$ que tens als apunts interactius de la unitat (són les de la PAU valenciana). Els " + str(npau) + r" exercicis marcats amb \textcolor{teal}{\faUniversity\ PAU} són de les proves d'accés a la universitat.",
                           r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos: identifica la variable aleatoria y su distribución, haz un dibujo del área que buscas y redondea $z$ a dos decimales. Usa las tablas de la binomial y de la normal $N(0,1)$ que tienes en los apuntes interactivos de la unidad (son las de la PAU valenciana). Los " + str(npau) + r" ejercicios marcados con \textcolor{teal}{\faUniversity\ PAU} son de las pruebas de acceso a la universidad."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q_, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, fix(s if sol else q_)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb la calculadora de probabilitats dels apunts interactius.", "¡Ánimo! Comprueba tus resultados con la calculadora de probabilidades de los apuntes interactivos.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = ('t10-fitxa-solucions' if sol else 't10-fitxa-exercicis') + ('-es' if ES else '') + '.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return npau

npau = build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'exercicis,', npau, 'de la PAU;', NCHK[0], 'comprovacions')
