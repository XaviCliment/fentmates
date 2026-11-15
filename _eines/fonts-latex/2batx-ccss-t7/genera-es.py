# Versió en castellà de genera.py. Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 7: Representació gràfica de funcions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les gràfiques (de l'enunciat i de les solucions) es calculen ací mateix amb Python i es dibuixen amb TikZ com a
# poligonals (graf), així no depenem de les funcions matemàtiques de TikZ. Al final, CHK comprova numèricament
# els resultats de les solucions.
# Ús: python3 genera.py && pdflatex t7-fitxa-exercicis.tex (dues vegades) && pdflatex t7-fitxa-solucions.tex
import os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))
ln, e, sq = math.log, math.exp, math.sqrt

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def pw(*rows, name='f(x)'):
    return name + r'=\begin{cases}' + r'\\[3pt]'.join(r'%s&\text{si }%s' % r for r in rows) + r'\end{cases}'
def dm(s): return r'\[' + s + r'\]'
def fx(s, n='f'): return '$' + n + '(x)=' + s + '$'

# ---------- gràfiques ----------
def nice(r):
    for s in (0.5, 1, 2, 5, 10, 20, 50, 100):
        if r / s <= 8: return s
    return 200
def fnum(v): return ('%g' % v).replace('.', '{,}')
def graf(curves, box, va=(), ha=(), oa=(), pts=(), mx=(), mn=(), opn=(), labs=(), w=6.0, h=4.4):
    """curves: llista de funcions o de (f, a, b); box: (x0, x1, y0, y1)."""
    x0, x1, y0, y1 = box
    sx, sy = w / (x1 - x0), h / (y1 - y0)
    stx, sty = nice(x1 - x0), nice(y1 - y0)
    o = [r'\begin{tikzpicture}[x=%.4fcm,y=%.4fcm,baseline=(current bounding box.center)]' % (sx, sy)]
    o.append(r'\draw[muted!25,very thin,xstep=%g,ystep=%g] (%g,%g) grid (%g,%g);' % (stx, sty, x0, y0, x1, y1))
    if y0 <= 0 <= y1: o.append(r'\draw[-latex,muted] (%g,0)--(%g,0);' % (x0, x1 + 0.35 / sx))
    if x0 <= 0 <= x1: o.append(r'\draw[-latex,muted] (0,%g)--(0,%g);' % (y0, y1 + 0.35 / sy))
    ay = 0 if y0 <= 0 <= y1 else y0
    ax = 0 if x0 <= 0 <= x1 else x0
    k = math.ceil(x0 / stx)
    while k * stx <= x1 + 1e-9:
        t = k * stx
        if abs(t) > 1e-9 and t < x1 - 1e-9: o.append(r'\node[below,font=\tiny,text=muted,inner sep=1.5pt] at (%g,%g) {$%s$};' % (t, ay, fnum(t)))
        k += 1
    k = math.ceil(y0 / sty)
    while k * sty <= y1 + 1e-9:
        t = k * sty
        if abs(t) > 1e-9 and t < y1 - 1e-9: o.append(r'\node[left,font=\tiny,text=muted,inner sep=1.5pt] at (%g,%g) {$%s$};' % (ax, t, fnum(t)))
        k += 1
    o.append(r'\begin{scope}\clip (%g,%g) rectangle (%g,%g);' % (x0, y0, x1, y1))
    for a in va: o.append(r'\draw[teal,dashed,thick] (%g,%g)--(%g,%g);' % (a, y0, a, y1))
    for b in ha: o.append(r'\draw[teal,dashed,thick] (%g,%g)--(%g,%g);' % (x0, b, x1, b))
    for m, n in oa: o.append(r'\draw[teal,dashed,thick] (%g,%g)--(%g,%g);' % (x0, m * x0 + n, x1, m * x1 + n))
    lim, span = 3 * (y1 - y0), y1 - y0
    for c in curves:
        f, a, b = (c, x0, x1) if callable(c) else c
        a, b = max(a, x0), min(b, x1)
        cuts = sorted([a, b] + [v for v in va if a < v < b])
        for p, q in zip(cuts, cuts[1:]):
            N, seg, prev = 360, [], None
            for i in range(N + 1):
                x = p + (q - p) * i / N
                if i == 0: x += (q - p) * 1e-6
                if i == N: x -= (q - p) * 1e-6
                try: y = f(x)
                except (ValueError, ZeroDivisionError, OverflowError): y = None
                if y is None or not math.isfinite(y) or y < y0 - lim or y > y1 + lim or (prev is not None and abs(y - prev) > 1.5 * span):
                    if len(seg) > 1: o.append(r'\draw[accent,line width=1.4pt,line join=round] ' + '--'.join(seg) + ';')
                    seg, prev = [], None
                    if y is None or not math.isfinite(y) or y < y0 - lim or y > y1 + lim: continue
                seg.append('(%.3f,%.3f)' % (x, y)); prev = y
            if len(seg) > 1: o.append(r'\draw[accent,line width=1.4pt,line join=round] ' + '--'.join(seg) + ';')
    o.append(r'\end{scope}')
    for x, y in pts: o.append(r'\fill[navy] (%g,%g) circle (2pt);' % (x, y))
    for x, y in opn: o.append(r'\filldraw[fill=white,draw=accent,line width=1pt] (%g,%g) circle (2.2pt);' % (x, y))
    for x, y in mx: o.append(r'\fill[green!50!black] (%g,%g) circle (2.6pt);' % (x, y))
    for x, y in mn: o.append(r'\fill[red!70!black] (%g,%g) circle (2.6pt);' % (x, y))
    for x, y, t, pos in labs: o.append(r'\node[%s,font=\scriptsize,fill=white,fill opacity=.8,text opacity=1,inner sep=1pt] at (%g,%g) {$%s$};' % (pos, x, y, t))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def cen(*gs): return '\n\n\\begin{center}' + '\\qquad'.join(gs) + '\\end{center}\n'

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S.append(("Dominio y puntos de corte con los ejes", [
 (1, r"Calcula el dominio de las funciones siguientes:" + tasks(3, [fx(r'x^3-5x+2'), fx(r'\dfrac{x+3}{x^2-9}'), fx(r'\dfrac{2x}{x^2+x-6}'), fx(r'\dfrac{5}{x^2+9}'), fx(r'e^{\frac{1}{x-2}}'), fx(r'\dfrac{x-1}{x^3-x}')])
     + recorda(r"Polinomios: $\mathbb R$. Fracciones: quitamos los valores que anulan el denominador. Exponenciales: el dominio del exponente."),
     tasks(2, [r"$\res{\mathbb R}$", r"$x^2-9=0\Rightarrow x=\pm3$: $\res{\mathbb R-\{-3,3\}}$", r"$(x+3)(x-2)=0$: $\res{\mathbb R-\{-3,2\}}$",
               r"$x^2+9\neq0$: $\res{\mathbb R}$", r"$\res{\mathbb R-\{2\}}$", r"$x(x-1)(x+1)=0$: $\res{\mathbb R-\{-1,0,1\}}$"])),
 (2, r"Calcula el dominio de las funciones logarítmicas siguientes:" + tasks(3, [fx(r'\ln(2x-6)'), fx(r'\ln(x^2-9)'), fx(r'\ln(x^2+1)'), fx(r'\ln\dfrac{x+1}{x-3}'), fx(r'\dfrac{\ln x}{x-2}'), fx(r'\ln(4-x^2)')])
     + recorda(r"El argumento del logaritmo debe ser estrictamente positivo. Si hace falta, haz una tabla de signos."),
     tasks(2, [r"$2x-6>0$: $\res{(3,+\infty)}$", r"$\res{(-\infty,-3)\cup(3,+\infty)}$", r"$x^2+1>0$ siempre: $\res{\mathbb R}$",
               r"$\res{(-\infty,-1)\cup(3,+\infty)}$", r"$x>0$ y $x\neq2$: $\res{(0,2)\cup(2,+\infty)}$", r"$\res{(-2,2)}$"])),
 (1, r"Halla los puntos de corte con los ejes de coordenadas:" + tasks(3, [fx(r'x^3-x^2-6x'), fx(r'x^4-5x^2+4'), fx(r'\dfrac{x^2-4}{x+1}'), fx(r'\dfrac{x+2}{x^2+1}'), fx(r'e^{x}-e'), fx(r'\ln(2x-1)')])
     + recorda(r"Eje OX: resolvemos $f(x)=0$. Eje OY: calculamos $f(0)$, si $0$ es del dominio."),
     tasks(2, [r"$x(x-3)(x+2)=0$: $\res{(-2,0),\ (0,0),\ (3,0)}$; OY: $(0,0)$", r"$(x^2-1)(x^2-4)=0$: $\res{(\pm1,0),\ (\pm2,0)}$; OY: $\res{(0,4)}$",
               r"OX: $\res{(-2,0),\ (2,0)}$; OY: $\res{(0,-4)}$", r"OX: $\res{(-2,0)}$; OY: $\res{(0,2)}$",
               r"OX: $e^x=e\Rightarrow\res{(1,0)}$; OY: $\res{(0,1-e)}$", r"OX: $2x-1=1\Rightarrow\res{(1,0)}$; OY: no, porque el dominio es $\left(\frac12,+\infty\right)$"])),
 (2, r"Calcula el dominio de las funciones radicales siguientes:" + tasks(3, [fx(r'\sqrt{3x-6}'), fx(r'\sqrt{10-2x}'), fx(r'\sqrt{x^2-16}'), fx(r'\sqrt{x^2-4x+3}'), fx(r'\dfrac{x}{\sqrt{x+5}}'), fx(r'\sqrt[3]{x^2-7}')])
     + recorda(r"Raíz de índice par: el radicando debe ser $\geq0$ (los extremos donde vale 0 sí entran); si la raíz está en el denominador, debe ser $>0$. Raíz de índice impar: el dominio del radicando."),
     tasks(2, [r"$3x-6\geq0\Rightarrow x\geq2$: $\res{[2,+\infty)}$", r"$10-2x\geq0\Rightarrow x\leq5$: $\res{(-\infty,5]}$", r"$\res{(-\infty,-4]\cup[4,+\infty)}$",
               r"$(x-1)(x-3)\geq0$: $\res{(-\infty,1]\cup[3,+\infty)}$", r"$x+5>0$ (denominador): $\res{(-5,+\infty)}$", r"Índice impar: $\res{\mathbb R}$"])),
 (2, r"Halla los puntos de corte con los ejes de las funciones radicales siguientes. Recuerda calcular primero el dominio:" + tasks(2, [fx(r'\sqrt{x^2-9}'), fx(r'\sqrt{x+5}-3'), fx(r'\sqrt{16-x^2}'), fx(r'\sqrt{x+1}-x+1')])
     + recorda(r"$\sqrt{g(x)}=0\iff g(x)=0$. Si hay más términos, aislamos la raíz y elevamos al cuadrado; después \textbf{comprobamos} las soluciones, porque al elevar al cuadrado pueden aparecer soluciones falsas."),
     tasks(1, [r"Dominio $(-\infty,-3]\cup[3,+\infty)$. OX: $x^2-9=0\Rightarrow\res{(-3,0),\ (3,0)}$. OY: $0$ no es del dominio, \rest{no corta}.",
               r"Dominio $[-5,+\infty)$. OX: $\sqrt{x+5}=3\Rightarrow x+5=9\Rightarrow\res{(4,0)}$. OY: $f(0)=\sqrt5-3$, $\res{\left(0,\sqrt5-3\right)}$.",
               r"Dominio $[-4,4]$. OX: $\res{(-4,0),\ (4,0)}$. OY: $\res{(0,4)}$.",
               r"Dominio $[-1,+\infty)$. OX: $\sqrt{x+1}=x-1\Rightarrow x+1=x^2-2x+1\Rightarrow x^2-3x=0\Rightarrow x=0,\ x=3$. Comprobamos: $x=3$: $2-3+1=0$ \checkmark; \ $x=0$: $1+1=2\neq0$ (falsa). Solo $\res{(3,0)}$. OY: $\res{(0,2)}$."])),
 (2, r"Calcula $a$ para que la gráfica de $f(x)=x^2+ax+4$ corte el eje OX en $x=1$. ¿Cuál es el otro punto de corte con OX? ¿Y el corte con OY?",
     r"$f(1)=5+a=0\Rightarrow\res{a=-5}$. \ $x^2-5x+4=(x-1)(x-4)$: el otro corte es $\res{(4,0)}$. OY: $\res{(0,4)}$."),
]))

# --- simetries ---
HALF = [(0, 0), (1, 2), (3, -1), (4, 0)]
def poly_line(P): return r'\draw[accent,line width=1.4pt] ' + '--'.join('(%g,%g)' % p for p in P) + ';'
def tzhalf(P, sc=0.55):
    g = r'\draw[muted!25,very thin] (-4,-3) grid (4,3);\draw[-latex,muted] (-4,0)--(4.4,0);\draw[-latex,muted] (0,-3)--(0,3.4);'
    for t in (-4, -2, 2, 4): g += r'\node[below,font=\tiny,text=muted] at (%d,0) {$%d$};' % (t, t)
    for t in (-2, 2): g += r'\node[left,font=\tiny,text=muted] at (0,%d) {$%d$};' % (t, t)
    return r'\begin{tikzpicture}[scale=%s,baseline=(current bounding box.center)]%s%s\end{tikzpicture}' % (sc, g, poly_line(P))
G_HALF = tzhalf(HALF)
G_EVEN = tzhalf([(-x, y) for x, y in reversed(HALF)] + HALF[1:])
G_ODD = tzhalf([(-x, -y) for x, y in reversed(HALF)] + HALF[1:])
S.append(("Simetrías", [
 (1, r"Estudia si las funciones siguientes son pares, impares o ninguna de las dos cosas:" + tasks(4, [fx(r'x^4-x^2'), fx(r'x^3+2x'), fx(r'x^3+x^2'), fx(r'\dfrac{x^2}{x^2+1}'), fx(r'\dfrac{x}{x^2-4}'), fx(r'e^{-x^2}+1'), fx(r'\ln(x^2+1)'), fx(r'\dfrac{x+1}{x}')])
     + recorda(r"Par: $f(-x)=f(x)$ (simétrica respecto del eje OY). Impar: $f(-x)=-f(x)$ (simétrica respecto del origen)."),
     tasks(4, [r"\rest{par}", r"\rest{impar}", r"\rest{ninguna}", r"\rest{par}", r"\rest{impar}", r"\rest{par}", r"\rest{par}", r"\rest{ninguna}: $f(-x)=\frac{x-1}{x}$"])),
 (2, r"Estudia la simetría de las funciones radicales siguientes. Antes, comprueba si el dominio es simétrico:" + tasks(4, [fx(r'\sqrt{x^2+9}'), fx(r'x\sqrt{4-x^2}'), fx(r'\sqrt{x+4}'), fx(r'\dfrac{x^3}{\sqrt{x^2+1}}')]),
     tasks(2, [r"Dominio $\mathbb R$, $f(-x)=\sqrt{x^2+9}=f(x)$: \rest{par}", r"Dominio $[-2,2]$, $f(-x)=-x\sqrt{4-x^2}=-f(x)$: \rest{impar}",
               r"Dominio $[-4,+\infty)$, no simétrico: \rest{ninguna}", r"Dominio $\mathbb R$, $f(-x)=\frac{-x^3}{\sqrt{x^2+1}}=-f(x)$: \rest{impar}"])),
 (2, r"La gráfica siguiente muestra una función $f$ solo para $0\leq x\leq4$. Complétala en $[-4,4]$ en cada caso:" + tasks(2, [r"si $f$ es par;", r"si $f$ es impar."]) + cen(G_HALF),
     r"Par: reflejamos respecto del eje OY. Impar: giramos 180° alrededor del origen." + cen(G_EVEN, G_ODD)),
]))

# --- asímptotes ---
def lect(x): return (x - 1) ** 2 / (x + 1)
G_LECT = graf([lect], (-9, 6, -14, 8), va=[-1], oa=[(1, -3)], pts=[(1, 0), (0, 1)], mx=[(-3, -8)], mn=[(1, 0)], w=6.6, h=5.2)
S.append(("Asíntotas", [
 (1, r"Calcula las asíntotas verticales y horizontales de estas funciones racionales y estudia los límites laterales en cada asíntota vertical:" + tasks(3, [fx(r'\dfrac{3x-1}{x+2}'), fx(r'\dfrac{x^2+1}{x^2-4}'), fx(r'\dfrac{2x}{x^2+1}'), fx(r'\dfrac{x-3}{x^2-9}'), fx(r'\dfrac{5}{(x-1)^2}')])
     + recorda(r"AV: donde se anula el denominador y el numerador no (límite $\frac{k}{0}$). AH: grado $P<$ grado $Q\Rightarrow y=0$; grados iguales $\Rightarrow y=$ cociente de los coeficientes principales."),
     tasks(1, [r"AV $\res{x=-2}$ ($\lim_{x\to-2^-}f=+\infty$, $\lim_{x\to-2^+}f=-\infty$); AH $\res{y=3}$.",
               r"AV $\res{x=-2}$ ($+\infty$ por la izquierda, $-\infty$ por la derecha) y $\res{x=2}$ ($-\infty$ por la izquierda, $+\infty$ por la derecha); AH $\res{y=1}$.",
               r"Ninguna AV ($x^2+1\neq0$); AH $\res{y=0}$.",
               r"En $x=3$: $\frac00$, $f(x)=\frac{1}{x+3}\to\frac16$: no hay AV (agujero en $\left(3,\frac16\right)$). AV $\res{x=-3}$ ($-\infty$ por la izquierda, $+\infty$ por la derecha); AH $\res{y=0}$.",
               r"AV $\res{x=1}$ ($+\infty$ por los dos lados); AH $\res{y=0}$."])),
 (2, r"Calcula las asíntotas oblicuas por el método del cociente (haz la división $P(x):Q(x)$) y también las verticales. En los apartados a) y b), estudia la posición de la gráfica respecto de la asíntota oblicua." + tasks(2, [fx(r'\dfrac{x^2+1}{x-2}'), fx(r'\dfrac{2x^2-3x}{x+1}'), fx(r'\dfrac{x^3-1}{x^2}'), fx(r'\dfrac{x^2-x+2}{x-1}')])
     + recorda(r"Si grado $P=$ grado $Q+1$: $P(x)=Q(x)\cdot C(x)+R(x)\Rightarrow f(x)=C(x)+\dfrac{R(x)}{Q(x)}$ y la asíntota oblicua es $y=C(x)$. El signo de $\frac{R(x)}{Q(x)}$ dice si la gráfica queda por encima o por debajo."),
     tasks(1, [r"$x^2+1=(x-2)(x+2)+5$: AO $\res{y=x+2}$, AV $\res{x=2}$. $\frac{5}{x-2}>0$ si $x\to+\infty$ (por encima) y $<0$ si $x\to-\infty$ (por debajo).",
               r"$2x^2-3x=(x+1)(2x-5)+5$: AO $\res{y=2x-5}$, AV $\res{x=-1}$. Por encima cuando $x\to+\infty$ y por debajo cuando $x\to-\infty$.",
               r"$f(x)=x-\frac{1}{x^2}$: AO $\res{y=x}$, AV $\res{x=0}$ ($-\infty$ por los dos lados).",
               r"$x^2-x+2=(x-1)\cdot x+2$: AO $\res{y=x}$, AV $\res{x=1}$."])),
 (2, r"Calcula las asíntotas de las funciones exponenciales y logarítmicas siguientes:" + tasks(3, [fx(r'3-e^{x}'), fx(r'2e^{-x}+1'), fx(r'\ln(x-4)'), fx(r'\ln(x^2+1)'), fx(r'e^{1/x}'), fx(r'x\,e^{-x}')])
     + recorda(r"$\lim_{x\to-\infty}e^x=0$, $\lim_{x\to+\infty}e^{-x}=0$ y $\lim_{x\to0^+}\ln x=-\infty$. La exponencial crece más rápido que cualquier potencia."),
     tasks(2, [r"AH $\res{y=3}$ cuando $x\to-\infty$.", r"AH $\res{y=1}$ cuando $x\to+\infty$.", r"AV $\res{x=4}$ ($\lim_{x\to4^+}f=-\infty$).", r"\rest{No tiene}: dominio $\mathbb R$ y $\lim_{x\to\pm\infty}f=+\infty$.",
               r"AV $\res{x=0}$ ($\lim_{x\to0^+}f=+\infty$; por la izquierda $\to0$); AH $\res{y=1}$ por los dos lados.", r"AH $\res{y=0}$ cuando $x\to+\infty$."])),
 (2, r"Asíntotas con parámetros:" + tasks(1, [r"Calcula $a$ y $b$ para que la función $f(x)=\dfrac{ax^2+b}{x-1}$ tenga la asíntota oblicua $y=2x+2$ y pase por el punto $(2,11)$.",
               r"¿Para qué valor de $k$ la función $g(x)=\dfrac{x^2+k}{x-2}$ no tiene asíntota vertical? ¿Cómo es la gráfica en este caso?"]),
     tasks(1, [r"$ax^2+b=(x-1)(ax+a)+(a+b)$: AO $y=ax+a\Rightarrow\res{a=2}$. \ $f(2)=8+b=11\Rightarrow\res{b=3}$.",
               r"El numerador debe anularse en $x=2$: $4+k=0\Rightarrow\res{k=-4}$. Entonces $g(x)=\frac{(x-2)(x+2)}{x-2}=x+2$ si $x\neq2$: una \rest{recta con un agujero} en $(2,4)$."])),
 (1, r"Observa la gráfica de la función $f$ (las líneas discontinuas son asíntotas) y responde:" + cen(G_LECT) + tasks(2, [r"¿Cuál es el dominio?", r"¿Cuáles son los puntos de corte con los ejes?", r"¿Cuáles son las asíntotas?", r"¿Cuáles son los intervalos de crecimiento y de decrecimiento y los extremos relativos?"]),
     tasks(2, [r"$\res{\mathbb R-\{-1\}}$", r"$\res{(1,0)}$ y $\res{(0,1)}$", r"AV $\res{x=-1}$ y AO $\res{y=x-3}$", r"Creciente en $\res{(-\infty,-3)\cup(1,+\infty)}$, decreciente en $\res{(-3,-1)\cup(-1,1)}$; máximo $\res{(-3,-8)}$, mínimo $\res{(1,0)}$."])
     + r" (Es $f(x)=\frac{(x-1)^2}{x+1}$.)"),
]))

# --- monotonia ---
S.append(("Monotonía y extremos relativos", [
 (1, r"Estudia la monotonía y calcula los máximos y mínimos relativos:" + tasks(2, [fx(r'x^3-12x+1'), fx(r'x^2e^{-x}'), fx(r'x-\ln x'), fx(r'\dfrac{4x}{x^2+1}')])
     + recorda(r"Resolvemos $f'(x)=0$, hacemos la tabla de signos de $f'$ (con los puntos que no son del dominio) y damos los extremos como puntos $(a,f(a))$."),
     tasks(1, [r"$f'(x)=3(x-2)(x+2)$: creciente en $\res{(-\infty,-2)\cup(2,+\infty)}$, decreciente en $\res{(-2,2)}$; máximo $\res{(-2,17)}$, mínimo $\res{(2,-15)}$.",
               r"$f'(x)=x(2-x)e^{-x}$: decreciente en $\res{(-\infty,0)\cup(2,+\infty)}$, creciente en $\res{(0,2)}$; mínimo $\res{(0,0)}$, máximo $\res{\left(2,\frac{4}{e^2}\right)}$.",
               r"Dominio $(0,+\infty)$, $f'(x)=\frac{x-1}{x}$: decreciente en $\res{(0,1)}$, creciente en $\res{(1,+\infty)}$; mínimo $\res{(1,1)}$.",
               r"$f'(x)=\frac{4(1-x^2)}{(x^2+1)^2}$: decreciente en $\res{(-\infty,-1)\cup(1,+\infty)}$, creciente en $\res{(-1,1)}$; mínimo $\res{(-1,-2)}$, máximo $\res{(1,2)}$."])),
]))

# --- representació: polinòmiques i racionals ---
REP = recorda(r"Dominio, cortes, simetría, asíntotas, monotonía y extremos; después situamos toda la información y dibujamos.")
def rep(fn): return r"Haz el estudio completo y representa " + fn + "."
S.append(("Representación de funciones polinómicas y racionales", [
 (1, rep(fx(r'x^3-3x^2')) + REP,
     r"Dominio $\mathbb R$. Cortes $(0,0)$, $(3,0)$. Sin simetría ni asíntotas. $f'(x)=3x(x-2)$: máximo $\res{(0,0)}$, mínimo $\res{(2,-4)}$."
     + cen(graf([lambda x: x**3 - 3*x*x], (-1.5, 3.8, -5, 1.5), pts=[(3, 0)], mx=[(0, 0)], mn=[(2, -4)]))),
 (1, rep(fx(r'-x^3+3x+2')),
     r"Dominio $\mathbb R$. $-(x+1)^2(x-2)=0$: cortes $(-1,0)$, $(2,0)$; OY $(0,2)$. $f'(x)=-3(x-1)(x+1)$: mínimo $\res{(-1,0)}$, máximo $\res{(1,4)}$."
     + cen(graf([lambda x: -x**3 + 3*x + 2], (-2.5, 3, -2, 5), pts=[(2, 0), (0, 2)], mx=[(1, 4)], mn=[(-1, 0)]))),
 (2, rep(fx(r'x^4-4x^2')),
     r"Dominio $\mathbb R$. Cortes $(0,0)$, $(\pm2,0)$. \rest{Par}. $f'(x)=4x(x^2-2)$: máximo $\res{(0,0)}$, mínimos $\res{(\pm\sqrt2,-4)}$."
     + cen(graf([lambda x: x**4 - 4*x*x], (-2.7, 2.7, -5, 4), pts=[(-2, 0), (2, 0)], mx=[(0, 0)], mn=[(-sq(2), -4), (sq(2), -4)]))),
 (1, rep(fx(r'\dfrac{x+1}{x-1}')),
     r"Dominio $\mathbb R-\{1\}$. Cortes $(-1,0)$, $(0,-1)$. AV $\res{x=1}$ ($-\infty$ por la izquierda, $+\infty$ por la derecha), AH $\res{y=1}$. $f'(x)=\frac{-2}{(x-1)^2}<0$: decreciente en $(-\infty,1)$ y en $(1,+\infty)$, sin extremos."
     + cen(graf([lambda x: (x + 1) / (x - 1)], (-5, 6, -5, 6), va=[1], ha=[1], pts=[(-1, 0), (0, -1)]))),
 (2, rep(fx(r'\dfrac{x^2+1}{x^2-1}')),
     r"Dominio $\mathbb R-\{-1,1\}$. No corta OX; OY $(0,-1)$. \rest{Par}. AV $\res{x=\pm1}$, AH $\res{y=1}$. $f'(x)=\frac{-4x}{(x^2-1)^2}$: creciente en $(-\infty,-1)\cup(-1,0)$, decreciente en $(0,1)\cup(1,+\infty)$; máximo $\res{(0,-1)}$."
     + cen(graf([lambda x: (x*x + 1) / (x*x - 1)], (-4, 4, -5, 6), va=[-1, 1], ha=[1], mx=[(0, -1)]))),
 (2, rep(fx(r'\dfrac{x}{x^2+1}')),
     r"Dominio $\mathbb R$. Corte $(0,0)$. \rest{Impar}. AH $\res{y=0}$. $f'(x)=\frac{1-x^2}{(x^2+1)^2}$: mínimo $\res{\left(-1,-\frac12\right)}$, máximo $\res{\left(1,\frac12\right)}$."
     + cen(graf([lambda x: x / (x*x + 1)], (-6, 6, -1, 1), ha=[0], pts=[(0, 0)], mx=[(1, 0.5)], mn=[(-1, -0.5)]))),
 (3, rep(fx(r'\dfrac{x^2}{x-2}')),
     r"Dominio $\mathbb R-\{2\}$. Corte $(0,0)$. AV $\res{x=2}$; $x^2=(x-2)(x+2)+4$: AO $\res{y=x+2}$. $f'(x)=\frac{x(x-4)}{(x-2)^2}$: máximo $\res{(0,0)}$, mínimo $\res{(4,8)}$."
     + cen(graf([lambda x: x*x / (x - 2)], (-6, 10, -10, 16), va=[2], oa=[(1, 2)], mx=[(0, 0)], mn=[(4, 8)]))),
 (3, rep(fx(r'\dfrac{x^2-2x+2}{x-1}')),
     r"Dominio $\mathbb R-\{1\}$. No corta OX ($\Delta<0$); OY $(0,-2)$. $f(x)=x-1+\frac{1}{x-1}$: AV $\res{x=1}$, AO $\res{y=x-1}$. $f'(x)=\frac{x(x-2)}{(x-1)^2}$: máximo $\res{(0,-2)}$, mínimo $\res{(2,2)}$."
     + cen(graf([lambda x: (x*x - 2*x + 2) / (x - 1)], (-4, 6, -7, 7), va=[1], oa=[(1, -1)], mx=[(0, -2)], mn=[(2, 2)]))),
 (3, rep(fx(r'\dfrac{x^3}{x^2-1}')),
     r"Dominio $\mathbb R-\{-1,1\}$. Corte $(0,0)$. \rest{Impar}. AV $\res{x=\pm1}$; $x^3=(x^2-1)x+x$: AO $\res{y=x}$. $f'(x)=\frac{x^2(x^2-3)}{(x^2-1)^2}$: máximo $\res{\left(-\sqrt3,-\frac{3\sqrt3}{2}\right)}$, mínimo $\res{\left(\sqrt3,\frac{3\sqrt3}{2}\right)}$; en $x=0$ no hay extremo."
     + cen(graf([lambda x: x**3 / (x*x - 1)], (-5, 5, -6, 6), va=[-1, 1], oa=[(1, 0)], pts=[(0, 0)], mx=[(-sq(3), -1.5*sq(3))], mn=[(sq(3), 1.5*sq(3))]))),
]))

# --- exponencials i logarítmiques ---
S.append(("Representación de funciones exponenciales y logarítmicas", [
 (1, r"Representa en los mismos ejes $f(x)=2^x$, $g(x)=2^x-4$ y $h(x)=2^{x-1}$. Indica el dominio, la asíntota y los puntos de corte de cada una.",
     r"Todas tienen dominio $\mathbb R$ y son crecientes. $f$: AH $y=0$, corte $(0,1)$. \ $g$: AH $\res{y=-4}$, cortes $\res{(2,0)}$ y $\res{(0,-3)}$. \ $h$: AH $y=0$, corte $\res{\left(0,\frac12\right)}$ (es $f$ desplazada 1 unidad a la derecha)."
     + cen(graf([lambda x: 2**x, lambda x: 2**x - 4, lambda x: 2**(x - 1)], (-4, 4, -5, 6), ha=[0, -4], pts=[(0, 1), (2, 0), (0, -3), (0, 0.5)],
                labs=[(2.6, 6.1, 'f', 'below'), (3.6, 4.6, 'h', 'right'), (3.5, 3.1, 'g', 'right')]))),
 (1, rep(fx(r'\ln(x-1)+2')),
     r"Dominio $(1,+\infty)$. AV $\res{x=1}$ ($\lim_{x\to1^+}f=-\infty$). OX: $\ln(x-1)=-2\Rightarrow\res{x=1+e^{-2}\approx1{,}14}$; no corta OY. Creciente, sin extremos ni AH."
     + cen(graf([lambda x: ln(x - 1) + 2 if x > 1 else None], (-1, 8, -3, 5), va=[1], pts=[(1 + e(-2), 0)]))),
 (2, rep(fx(r'x\,e^{-x}')),
     r"Dominio $\mathbb R$. Corte $(0,0)$. $\lim_{x\to+\infty}x\,e^{-x}=0$: AH $\res{y=0}$ por la derecha; $\lim_{x\to-\infty}f=-\infty$. $f'(x)=(1-x)e^{-x}$: creciente en $(-\infty,1)$, decreciente en $(1,+\infty)$; máximo $\res{\left(1,\frac1e\right)}$."
     + cen(graf([lambda x: x * e(-x)], (-1.5, 7, -2, 0.8), ha=[0], pts=[(0, 0)], mx=[(1, 1 / math.e)]))),
 (2, rep(fx(r'e^{-x^2}')),
     r"Dominio $\mathbb R$. Corte $(0,1)$; no corta OX. \rest{Par}. AH $\res{y=0}$. $f'(x)=-2x\,e^{-x^2}$: creciente en $(-\infty,0)$, decreciente en $(0,+\infty)$; máximo $\res{(0,1)}$."
     + cen(graf([lambda x: e(-x*x)], (-3, 3, -0.4, 1.4), ha=[0], mx=[(0, 1)]))),
 (2, rep(fx(r'x-\ln x')),
     r"Dominio $(0,+\infty)$. No corta los ejes ($f\geq1$). $\lim_{x\to0^+}(x-\ln x)=+\infty$: AV $\res{x=0}$; sin AH. $f'(x)=\frac{x-1}{x}$: mínimo $\res{(1,1)}$."
     + cen(graf([lambda x: x - ln(x) if x > 0 else None], (-0.5, 6, -0.5, 5), va=[0], mn=[(1, 1)]))),
 (3, rep(fx(r'\ln(x^2-4)')),
     r"Dominio $(-\infty,-2)\cup(2,+\infty)$. OX: $x^2-4=1\Rightarrow\res{(\pm\sqrt5,0)}$; no corta OY. \rest{Par}. AV $\res{x=\pm2}$ ($f\to-\infty$). $f'(x)=\frac{2x}{x^2-4}$: decreciente en $(-\infty,-2)$, creciente en $(2,+\infty)$; sin extremos."
     + cen(graf([lambda x: ln(x*x - 4) if abs(x) > 2 else None], (-6, 6, -4, 4), va=[-2, 2], pts=[(-sq(5), 0), (sq(5), 0)]))),
]))

# --- a trossos ---
S.append(("Funciones definidas a trozos", [
 (1, r"Representa la función siguiente y estudia su continuidad y su monotonía:" + dm(pw((r'x+2', 'x<0'), (r'2', r'0\leq x<2'), (r'6-2x', r'x\geq2'))),
     r"En $x=0$: laterales $2$ y $2$, $f(0)=2$: continua. En $x=2$: laterales $2$ y $2$: continua. \rest{Continua en $\mathbb R$}. Creciente en $\res{(-\infty,0)}$, constante en $\res{(0,2)}$, decreciente en $\res{(2,+\infty)}$."
     + cen(graf([(lambda x: x + 2, -6, 0), (lambda x: 2, 0, 2), (lambda x: 6 - 2*x, 2, 6)], (-5, 5, -3, 4), pts=[(-2, 0), (3, 0), (0, 2)]))),
 (2, r"Representa" + dm(pw((r'x^2-1', r'x\leq1'), (r'\ln x', 'x>1'))) + r"e indica sus puntos de corte, su continuidad, su monotonía y sus extremos relativos.",
     r"Cortes $(-1,0)$, $(1,0)$, $(0,-1)$. En $x=1$: laterales $0$ y $\ln1=0$: \rest{continua}. Decreciente en $\res{(-\infty,0)}$, creciente en $\res{(0,+\infty)}$; mínimo $\res{(0,-1)}$."
     + cen(graf([(lambda x: x*x - 1, -6, 1), (lambda x: ln(x), 1, 8)], (-3, 7, -1.6, 3), pts=[(-1, 0), (1, 0)], mn=[(0, -1)]))),
 (2, r"Representa" + dm(pw((r'2^x', r'x\leq1'), (r'\dfrac{4}{x}', 'x>1'))) + r"y estudia su continuidad, sus asíntotas y su monotonía. ¿Tiene algún extremo relativo en $x=1$?",
     r"En $x=1$: por la izquierda $2$, por la derecha $4$: \rest{salto finito}. AH $\res{y=0}$ por los dos lados. Creciente en $(-\infty,1)$ y decreciente en $(1,+\infty)$. En $x=1$ \rest{no hay extremo}: $f(1)=2$, pero a la derecha hay valores próximos a 4."
     + cen(graf([(lambda x: 2**x, -6, 1.000001), (lambda x: 4 / x, 1, 8)], (-4, 7, -0.6, 5), ha=[0], pts=[(1, 2), (0, 1)], opn=[(1, 4)]))),
 (3, r"Considera la función" + dm(pw((r'x^2+a', 'x<1'), (r'\dfrac{b}{x}', r'x\geq1'))) + tasks(1, [r"Calcula $a$ y $b$ para que $f$ sea continua y su gráfica pase por el punto $(2,1)$.", r"Para estos valores, represéntala e indica sus asíntotas y sus extremos relativos."]),
     tasks(1, [r"$f(2)=\frac b2=1\Rightarrow\res{b=2}$. Continuidad en $x=1$: $1+a=2\Rightarrow\res{a=1}$.",
               r"AH $\res{y=0}$ por la derecha. Decreciente en $(-\infty,0)$, creciente en $(0,1)$, decreciente en $(1,+\infty)$: mínimo $\res{(0,1)}$ y máximo $\res{(1,2)}$ (punto anguloso)."])
     + cen(graf([(lambda x: x*x + 1, -6, 1), (lambda x: 2 / x, 1, 9)], (-3, 7, -0.5, 4), ha=[0], mx=[(1, 2)], mn=[(0, 1)]))),
]))

# --- context ---
S.append(("Problemas con contexto", [
 (2, r"Una empresa tiene unos costes fijos de 200 € y un coste de 3 € por cada unidad producida. El coste medio por unidad cuando produce $x$ unidades es $CM(x)=\dfrac{3x+200}{x}$." + tasks(1, [r"¿Qué dominio tiene sentido para esta función?", r"Calcula sus asíntotas e interprétalas.", r"Estudia su monotonía y represéntala."]),
     tasks(1, [r"$\res{x>0}$ (unidades producidas).", r"AV $\res{x=0}$: si se producen muy pocas unidades, el coste medio se dispara. AH $\res{y=3}$: si se producen muchas unidades, el coste medio se acerca a 3 € (los costes fijos se reparten).",
               r"$CM'(x)=-\frac{200}{x^2}<0$: \rest{siempre decreciente}."])
     + cen(graf([lambda x: (3*x + 200) / x if x > 0 else None], (-10, 200, -2, 20), va=[0], ha=[3]))),
 (2, r"La población de una especie de peces en un embalse, en miles de ejemplares, viene dada por $P(t)=\dfrac{60t+20}{t+2}$, donde $t$ son los años desde que se empezó a estudiar ($t\geq0$)." + tasks(1, [r"¿Cuál era la población inicial?", r"¿La población crece o decrece? Justifícalo.", r"¿Qué pasará a largo plazo? Representa la función."]),
     tasks(1, [r"$P(0)=\res{10}$ miles.", r"$P'(t)=\frac{100}{(t+2)^2}>0$: \rest{siempre crece}.", r"$\lim_{t\to+\infty}P(t)=60$: AH $y=60$; se acerca a $\res{60\,000}$ peces sin llegar a alcanzarlos."])
     + cen(graf([lambda t: (60*t + 20) / (t + 2)], (-2, 40, -5, 70), ha=[60], pts=[(0, 10)]))),
 (2, r"La concentración de un medicamento en la sangre (mg/l) $t$ horas después de tomarlo es $C(t)=10\,t\,e^{-t/2}$, $t\geq0$." + tasks(1, [r"¿Cuándo se alcanza la concentración máxima? ¿Cuál es?", r"¿Qué ocurre con la concentración con el paso del tiempo?", r"Representa la función."]),
     tasks(1, [r"$C'(t)=10\,e^{-t/2}\left(1-\frac t2\right)=0\Rightarrow t=2$ (crece antes y decrece después): máximo a las $\res{2}$ h, con $C(2)=\frac{20}{e}\approx\res{7{,}36}$ mg/l.",
               r"$\lim_{t\to+\infty}10t\,e^{-t/2}=0$: AH $y=0$, el medicamento \rest{se elimina}.", r"Véase la gráfica."])
     + cen(graf([lambda t: 10 * t * e(-t / 2) if t >= 0 else None], (-1, 14, -1, 9), ha=[0], pts=[(0, 0)], mx=[(2, 20 / math.e)]))),
 (3, r"Una tienda calcula que el coste (en cientos de euros) de hacer pedidos de $x$ cajas y de almacenarlas es $C(x)=\dfrac{(x+8)^2}{2x}$, $x>0$." + tasks(1, [r"Calcula sus asíntotas por el método del cociente.", r"¿Cuántas cajas debe pedir cada vez para que el coste sea mínimo? ¿Cuál es ese coste?", r"Representa la función."]),
     tasks(1, [r"$(x+8)^2=x^2+16x+64$ y $\frac{x^2+16x+64}{2x}=\frac x2+8+\frac{32}{x}$: AV $\res{x=0}$, AO $\res{y=\frac x2+8}$.",
               r"$C'(x)=\frac12-\frac{32}{x^2}=0\Rightarrow x=8$, $C''(8)>0$: $\res{8}$ cajas, con un coste de $C(8)=\res{16}$ cientos (1\,600 €)."])
     + cen(graf([lambda x: (x + 8)**2 / (2 * x) if x > 0 else None], (-2, 40, -2, 40), va=[0], oa=[(0.5, 8)], mn=[(8, 16)]))),
]))

# ---------- comprovacions numèriques ----------
def nd(f, x, h=1e-6): return (f(x + h) - f(x - h)) / (2 * h)
CHK = [  # (valor de l'esquerra, valor de la dreta)
 (9 - 3 - 6, 0), (4 + 2 - 6, 0), (1 - 5 + 4, 0), (16 - 20 + 4, 0), ((0 + 2) / 1, 2), (e(1) - math.e, 0), (ln(2 * 1 - 1), 0), (1 - 5 + 4, 0), (16 - 20 + 4, 0),
 (lect(1), 0), (lect(0), 1), (lect(-3), -8), (nd(lect, -3), 0), (nd(lect, 1), 0), (lect(1e6) - (1e6 - 3), 0),
 ((1e6**2 + 1) / (1e6 - 2) - (1e6 + 2), 0), ((2 * 1e6**2 - 3e6) / (1e6 + 1) - (2e6 - 5), 0), ((1e6**2 - 1e6 + 2) / (1e6 - 1) - 1e6, 0),
 (1 / (3 + 3), 1 / 6), (nd(lambda x: x**3 - 12*x + 1, 2), 0), (8 - 24 + 1, -15), (-8 + 24 + 1, 17), (nd(lambda x: x*x*e(-x), 2), 0), (4 * e(-2), 4 / math.e**2),
 (nd(lambda x: 4*x / (x*x + 1), 1), 0), (4 / 2, 2), (nd(lambda x: x - ln(x), 1), 0),
 (nd(lambda x: x**3 - 3*x*x, 2), 0), (8 - 12, -4), (nd(lambda x: -x**3 + 3*x + 2, 1), 0), (-1 + 3 + 2, 4), (-(-1)**3 - 3 + 2, 0), (-8 + 6 + 2, 0),
 (nd(lambda x: x**4 - 4*x*x, sq(2)), 0), (4 - 8, -4), (nd(lambda x: x*x / (x - 2), 4), 0), (16 / 2, 8), (nd(lambda x: (x*x - 2*x + 2) / (x - 1), 2), 0), ((4 - 4 + 2) / 1, 2), (2 / -1, -2),
 (nd(lambda x: x**3 / (x*x - 1), sq(3)), 0), (3 * sq(3) / 2, sq(3)**3 / 2), (nd(lambda x: x / (x*x + 1), 1), 0),
 (2**2 - 4, 0), (2**-1, 0.5), (ln(e(-2)) + 2, 0), (nd(lambda x: x * e(-x), 1), 0), (1 - ln(1), 1), (ln(5 - 4), 0),
 (1 + 1, 2 / 1), (2 / 2, 1), (nd(lambda x: (x + 8)**2 / (2 * x), 8), 0), ((16)**2 / 16, 16), (nd(lambda t: 10 * t * e(-t / 2), 2), 0), ((60 * 0 + 20) / 2, 10),
 (nd(lambda t: (60*t + 20) / (t + 2), 3), 100 / 25), (2 * 4 + 3, 11),
 # radicals: talls
 (sq(3*3 - 9), 0), (sq(4 + 5) - 3, 0), (sq(16 - 16), 0), (sq(3 + 1) - 3 + 1, 0), (sq(0 + 1) - 0 + 1, 2), (sq(16 - 0), 4), (sq(0 + 1) + 1, 2),
 (1*1 - 4*1 + 3, 0), (3*3 - 4*3 + 3, 0), (sq(9 + 0) - sq(9 + 0), 0), (-1 * sq(4 - 1) + 1 * sq(4 - 1), 0),
]
for l, r in CHK: assert abs(l - r) < 1e-5 * (1 + abs(r)), (l, r)

# =====================================================================
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

TIT = "Representación gráfica de funciones"
KW = "representación gráfica, dominio, puntos de corte, simetría, funciones radicales, asíntotas, asíntota oblicua, monotonía, máximos, mínimos, funciones racionales, exponenciales, logarítmicas, a trozos"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 7: %s' % (t, TIT), capcalera='%s · Unidad 7: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-ccss')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 7' if sol else 'Ficha de ejercicios · Unidad 7') + '}{\\raggedright ' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. En las gráficas, las líneas discontinuas son asíntotas, los puntos verdes son máximos y los rojos, mínimos. Puedes comprobar cualquier estudio con la herramienta «Estudio completo de una función» de los apuntes interactivos de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. Cuando tengas que representar una función, sigue el guion: dominio, puntos de corte, simetría, asíntotas, monotonía y extremos; después sitúa toda la información en los ejes y dibuja la gráfica.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con la herramienta de estudio completo de una función de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't7-fitxa-solucions-es.tex' if sol else 't7-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
