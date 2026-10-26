# Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 7: Representació gràfica de funcions)
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
S.append(("Domini i punts de tall amb els eixos", [
 (1, r"Calcula el domini de les funcions següents:" + tasks(3, [fx(r'x^3-5x+2'), fx(r'\dfrac{x+3}{x^2-9}'), fx(r'\dfrac{2x}{x^2+x-6}'), fx(r'\dfrac{5}{x^2+9}'), fx(r'e^{\frac{1}{x-2}}'), fx(r'\dfrac{x-1}{x^3-x}')])
     + recorda(r"Polinomis: $\mathbb R$. Fraccions: traiem els valors que anul·len el denominador. Exponencials: el domini de l'exponent."),
     tasks(2, [r"$\res{\mathbb R}$", r"$x^2-9=0\Rightarrow x=\pm3$: $\res{\mathbb R-\{-3,3\}}$", r"$(x+3)(x-2)=0$: $\res{\mathbb R-\{-3,2\}}$",
               r"$x^2+9\neq0$: $\res{\mathbb R}$", r"$\res{\mathbb R-\{2\}}$", r"$x(x-1)(x+1)=0$: $\res{\mathbb R-\{-1,0,1\}}$"])),
 (2, r"Calcula el domini de les funcions logarítmiques següents:" + tasks(3, [fx(r'\ln(2x-6)'), fx(r'\ln(x^2-9)'), fx(r'\ln(x^2+1)'), fx(r'\ln\dfrac{x+1}{x-3}'), fx(r'\dfrac{\ln x}{x-2}'), fx(r'\ln(4-x^2)')])
     + recorda(r"L'argument del logaritme ha de ser estrictament positiu. Si cal, fes una taula de signes."),
     tasks(2, [r"$2x-6>0$: $\res{(3,+\infty)}$", r"$\res{(-\infty,-3)\cup(3,+\infty)}$", r"$x^2+1>0$ sempre: $\res{\mathbb R}$",
               r"$\res{(-\infty,-1)\cup(3,+\infty)}$", r"$x>0$ i $x\neq2$: $\res{(0,2)\cup(2,+\infty)}$", r"$\res{(-2,2)}$"])),
 (1, r"Troba els punts de tall amb els eixos de coordenades:" + tasks(3, [fx(r'x^3-x^2-6x'), fx(r'x^4-5x^2+4'), fx(r'\dfrac{x^2-4}{x+1}'), fx(r'\dfrac{x+2}{x^2+1}'), fx(r'e^{x}-e'), fx(r'\ln(2x-1)')])
     + recorda(r"Eix OX: resolem $f(x)=0$. Eix OY: calculem $f(0)$, si $0$ és del domini."),
     tasks(2, [r"$x(x-3)(x+2)=0$: $\res{(-2,0),\ (0,0),\ (3,0)}$; OY: $(0,0)$", r"$(x^2-1)(x^2-4)=0$: $\res{(\pm1,0),\ (\pm2,0)}$; OY: $\res{(0,4)}$",
               r"OX: $\res{(-2,0),\ (2,0)}$; OY: $\res{(0,-4)}$", r"OX: $\res{(-2,0)}$; OY: $\res{(0,2)}$",
               r"OX: $e^x=e\Rightarrow\res{(1,0)}$; OY: $\res{(0,1-e)}$", r"OX: $2x-1=1\Rightarrow\res{(1,0)}$; OY: no, perquè el domini és $\left(\frac12,+\infty\right)$"])),
 (2, r"Calcula el domini de les funcions radicals següents:" + tasks(3, [fx(r'\sqrt{3x-6}'), fx(r'\sqrt{10-2x}'), fx(r'\sqrt{x^2-16}'), fx(r'\sqrt{x^2-4x+3}'), fx(r'\dfrac{x}{\sqrt{x+5}}'), fx(r'\sqrt[3]{x^2-7}')])
     + recorda(r"Arrel d'índex parell: el radicand ha de ser $\geq0$ (els extrems on val 0 sí que hi entren); si l'arrel és al denominador, ha de ser $>0$. Arrel d'índex senar: el domini del radicand."),
     tasks(2, [r"$3x-6\geq0\Rightarrow x\geq2$: $\res{[2,+\infty)}$", r"$10-2x\geq0\Rightarrow x\leq5$: $\res{(-\infty,5]}$", r"$\res{(-\infty,-4]\cup[4,+\infty)}$",
               r"$(x-1)(x-3)\geq0$: $\res{(-\infty,1]\cup[3,+\infty)}$", r"$x+5>0$ (denominador): $\res{(-5,+\infty)}$", r"Índex senar: $\res{\mathbb R}$"])),
 (2, r"Troba els punts de tall amb els eixos de les funcions radicals següents. Recorda calcular primer el domini:" + tasks(2, [fx(r'\sqrt{x^2-9}'), fx(r'\sqrt{x+5}-3'), fx(r'\sqrt{16-x^2}'), fx(r'\sqrt{x+1}-x+1')])
     + recorda(r"$\sqrt{g(x)}=0\iff g(x)=0$. Si hi ha més termes, aïllem l'arrel i elevem al quadrat; després \textbf{comprovem} les solucions, perquè en elevar al quadrat poden aparéixer solucions falses."),
     tasks(1, [r"Domini $(-\infty,-3]\cup[3,+\infty)$. OX: $x^2-9=0\Rightarrow\res{(-3,0),\ (3,0)}$. OY: $0$ no és del domini, \rest{no talla}.",
               r"Domini $[-5,+\infty)$. OX: $\sqrt{x+5}=3\Rightarrow x+5=9\Rightarrow\res{(4,0)}$. OY: $f(0)=\sqrt5-3$, $\res{\left(0,\sqrt5-3\right)}$.",
               r"Domini $[-4,4]$. OX: $\res{(-4,0),\ (4,0)}$. OY: $\res{(0,4)}$.",
               r"Domini $[-1,+\infty)$. OX: $\sqrt{x+1}=x-1\Rightarrow x+1=x^2-2x+1\Rightarrow x^2-3x=0\Rightarrow x=0,\ x=3$. Comprovem: $x=3$: $2-3+1=0$ \checkmark; \ $x=0$: $1+1=2\neq0$ (falsa). Només $\res{(3,0)}$. OY: $\res{(0,2)}$."])),
 (2, r"Calcula $a$ perquè la gràfica de $f(x)=x^2+ax+4$ talle l'eix OX en $x=1$. Quin és l'altre punt de tall amb OX? I el tall amb OY?",
     r"$f(1)=5+a=0\Rightarrow\res{a=-5}$. \ $x^2-5x+4=(x-1)(x-4)$: l'altre tall és $\res{(4,0)}$. OY: $\res{(0,4)}$."),
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
S.append(("Simetries", [
 (1, r"Estudia si les funcions següents són parelles, senars o cap de les dues coses:" + tasks(4, [fx(r'x^4-x^2'), fx(r'x^3+2x'), fx(r'x^3+x^2'), fx(r'\dfrac{x^2}{x^2+1}'), fx(r'\dfrac{x}{x^2-4}'), fx(r'e^{-x^2}+1'), fx(r'\ln(x^2+1)'), fx(r'\dfrac{x+1}{x}')])
     + recorda(r"Parella: $f(-x)=f(x)$ (simètrica respecte de l'eix OY). Senar: $f(-x)=-f(x)$ (simètrica respecte de l'origen)."),
     tasks(4, [r"\rest{parella}", r"\rest{senar}", r"\rest{cap}", r"\rest{parella}", r"\rest{senar}", r"\rest{parella}", r"\rest{parella}", r"\rest{cap}: $f(-x)=\frac{x-1}{x}$"])),
 (2, r"Estudia la simetria de les funcions radicals següents. Abans, comprova si el domini és simètric:" + tasks(4, [fx(r'\sqrt{x^2+9}'), fx(r'x\sqrt{4-x^2}'), fx(r'\sqrt{x+4}'), fx(r'\dfrac{x^3}{\sqrt{x^2+1}}')]),
     tasks(2, [r"Domini $\mathbb R$, $f(-x)=\sqrt{x^2+9}=f(x)$: \rest{parella}", r"Domini $[-2,2]$, $f(-x)=-x\sqrt{4-x^2}=-f(x)$: \rest{senar}",
               r"Domini $[-4,+\infty)$, no simètric: \rest{cap}", r"Domini $\mathbb R$, $f(-x)=\frac{-x^3}{\sqrt{x^2+1}}=-f(x)$: \rest{senar}"])),
 (2, r"La gràfica següent mostra una funció $f$ només per a $0\leq x\leq4$. Completa-la en $[-4,4]$ en cada cas:" + tasks(2, [r"si $f$ és parella;", r"si $f$ és senar."]) + cen(G_HALF),
     r"Parella: reflectim respecte de l'eix OY. Senar: girem 180° al voltant de l'origen." + cen(G_EVEN, G_ODD)),
]))

# --- asímptotes ---
def lect(x): return (x - 1) ** 2 / (x + 1)
G_LECT = graf([lect], (-9, 6, -14, 8), va=[-1], oa=[(1, -3)], pts=[(1, 0), (0, 1)], mx=[(-3, -8)], mn=[(1, 0)], w=6.6, h=5.2)
S.append(("Asímptotes", [
 (1, r"Calcula les asímptotes verticals i horitzontals d'aquestes funcions racionals i estudia els límits laterals en cada asímptota vertical:" + tasks(3, [fx(r'\dfrac{3x-1}{x+2}'), fx(r'\dfrac{x^2+1}{x^2-4}'), fx(r'\dfrac{2x}{x^2+1}'), fx(r'\dfrac{x-3}{x^2-9}'), fx(r'\dfrac{5}{(x-1)^2}')])
     + recorda(r"AV: on s'anul·la el denominador i el numerador no (límit $\frac{k}{0}$). AH: grau $P<$ grau $Q\Rightarrow y=0$; graus iguals $\Rightarrow y=$ quocient dels coeficients principals."),
     tasks(1, [r"AV $\res{x=-2}$ ($\lim_{x\to-2^-}f=+\infty$, $\lim_{x\to-2^+}f=-\infty$); AH $\res{y=3}$.",
               r"AV $\res{x=-2}$ ($+\infty$ per l'esquerra, $-\infty$ per la dreta) i $\res{x=2}$ ($-\infty$ per l'esquerra, $+\infty$ per la dreta); AH $\res{y=1}$.",
               r"Cap AV ($x^2+1\neq0$); AH $\res{y=0}$.",
               r"En $x=3$: $\frac00$, $f(x)=\frac{1}{x+3}\to\frac16$: no hi ha AV (forat en $\left(3,\frac16\right)$). AV $\res{x=-3}$ ($-\infty$ per l'esquerra, $+\infty$ per la dreta); AH $\res{y=0}$.",
               r"AV $\res{x=1}$ ($+\infty$ pels dos costats); AH $\res{y=0}$."])),
 (2, r"Calcula les asímptotes obliqües pel mètode del quocient (fes la divisió $P(x):Q(x)$) i també les verticals. En els apartats a) i b), estudia la posició de la gràfica respecte de l'asímptota obliqua." + tasks(2, [fx(r'\dfrac{x^2+1}{x-2}'), fx(r'\dfrac{2x^2-3x}{x+1}'), fx(r'\dfrac{x^3-1}{x^2}'), fx(r'\dfrac{x^2-x+2}{x-1}')])
     + recorda(r"Si grau $P=$ grau $Q+1$: $P(x)=Q(x)\cdot C(x)+R(x)\Rightarrow f(x)=C(x)+\dfrac{R(x)}{Q(x)}$ i l'asímptota obliqua és $y=C(x)$. El signe de $\frac{R(x)}{Q(x)}$ diu si la gràfica queda per damunt o per davall."),
     tasks(1, [r"$x^2+1=(x-2)(x+2)+5$: AO $\res{y=x+2}$, AV $\res{x=2}$. $\frac{5}{x-2}>0$ si $x\to+\infty$ (per damunt) i $<0$ si $x\to-\infty$ (per davall).",
               r"$2x^2-3x=(x+1)(2x-5)+5$: AO $\res{y=2x-5}$, AV $\res{x=-1}$. Per damunt quan $x\to+\infty$ i per davall quan $x\to-\infty$.",
               r"$f(x)=x-\frac{1}{x^2}$: AO $\res{y=x}$, AV $\res{x=0}$ ($-\infty$ pels dos costats).",
               r"$x^2-x+2=(x-1)\cdot x+2$: AO $\res{y=x}$, AV $\res{x=1}$."])),
 (2, r"Calcula les asímptotes de les funcions exponencials i logarítmiques següents:" + tasks(3, [fx(r'3-e^{x}'), fx(r'2e^{-x}+1'), fx(r'\ln(x-4)'), fx(r'\ln(x^2+1)'), fx(r'e^{1/x}'), fx(r'x\,e^{-x}')])
     + recorda(r"$\lim_{x\to-\infty}e^x=0$, $\lim_{x\to+\infty}e^{-x}=0$ i $\lim_{x\to0^+}\ln x=-\infty$. L'exponencial creix més ràpid que qualsevol potència."),
     tasks(2, [r"AH $\res{y=3}$ quan $x\to-\infty$.", r"AH $\res{y=1}$ quan $x\to+\infty$.", r"AV $\res{x=4}$ ($\lim_{x\to4^+}f=-\infty$).", r"\rest{No en té}: domini $\mathbb R$ i $\lim_{x\to\pm\infty}f=+\infty$.",
               r"AV $\res{x=0}$ ($\lim_{x\to0^+}f=+\infty$; per l'esquerra $\to0$); AH $\res{y=1}$ pels dos costats.", r"AH $\res{y=0}$ quan $x\to+\infty$."])),
 (2, r"Asímptotes amb paràmetres:" + tasks(1, [r"Calcula $a$ i $b$ perquè la funció $f(x)=\dfrac{ax^2+b}{x-1}$ tinga l'asímptota obliqua $y=2x+2$ i passe pel punt $(2,11)$.",
               r"Per a quin valor de $k$ la funció $g(x)=\dfrac{x^2+k}{x-2}$ no té asímptota vertical? Com és la gràfica en aquest cas?"]),
     tasks(1, [r"$ax^2+b=(x-1)(ax+a)+(a+b)$: AO $y=ax+a\Rightarrow\res{a=2}$. \ $f(2)=8+b=11\Rightarrow\res{b=3}$.",
               r"Cal que el numerador s'anul·le en $x=2$: $4+k=0\Rightarrow\res{k=-4}$. Aleshores $g(x)=\frac{(x-2)(x+2)}{x-2}=x+2$ si $x\neq2$: una \rest{recta amb un forat} en $(2,4)$."])),
 (1, r"Observa la gràfica de la funció $f$ (les línies discontínues són asímptotes) i respon:" + cen(G_LECT) + tasks(2, [r"Quin és el domini?", r"Quins són els punts de tall amb els eixos?", r"Quines són les asímptotes?", r"Quins són els intervals de creixement i de decreixement i els extrems relatius?"]),
     tasks(2, [r"$\res{\mathbb R-\{-1\}}$", r"$\res{(1,0)}$ i $\res{(0,1)}$", r"AV $\res{x=-1}$ i AO $\res{y=x-3}$", r"Creixent en $\res{(-\infty,-3)\cup(1,+\infty)}$, decreixent en $\res{(-3,-1)\cup(-1,1)}$; màxim $\res{(-3,-8)}$, mínim $\res{(1,0)}$."])
     + r" (És $f(x)=\frac{(x-1)^2}{x+1}$.)"),
]))

# --- monotonia ---
S.append(("Monotonia i extrems relatius", [
 (1, r"Estudia la monotonia i calcula els màxims i mínims relatius:" + tasks(2, [fx(r'x^3-12x+1'), fx(r'x^2e^{-x}'), fx(r'x-\ln x'), fx(r'\dfrac{4x}{x^2+1}')])
     + recorda(r"Resolem $f'(x)=0$, fem la taula de signes de $f'$ (amb els punts que no són del domini) i donem els extrems com a punts $(a,f(a))$."),
     tasks(1, [r"$f'(x)=3(x-2)(x+2)$: creixent en $\res{(-\infty,-2)\cup(2,+\infty)}$, decreixent en $\res{(-2,2)}$; màxim $\res{(-2,17)}$, mínim $\res{(2,-15)}$.",
               r"$f'(x)=x(2-x)e^{-x}$: decreixent en $\res{(-\infty,0)\cup(2,+\infty)}$, creixent en $\res{(0,2)}$; mínim $\res{(0,0)}$, màxim $\res{\left(2,\frac{4}{e^2}\right)}$.",
               r"Domini $(0,+\infty)$, $f'(x)=\frac{x-1}{x}$: decreixent en $\res{(0,1)}$, creixent en $\res{(1,+\infty)}$; mínim $\res{(1,1)}$.",
               r"$f'(x)=\frac{4(1-x^2)}{(x^2+1)^2}$: decreixent en $\res{(-\infty,-1)\cup(1,+\infty)}$, creixent en $\res{(-1,1)}$; mínim $\res{(-1,-2)}$, màxim $\res{(1,2)}$."])),
]))

# --- representació: polinòmiques i racionals ---
REP = recorda(r"Domini, talls, simetria, asímptotes, monotonia i extrems; després situem tota la informació i dibuixem.")
def rep(fn): return r"Fes l'estudi complet i representa " + fn + "."
S.append(("Representació de funcions polinòmiques i racionals", [
 (1, rep(fx(r'x^3-3x^2')) + REP,
     r"Domini $\mathbb R$. Talls $(0,0)$, $(3,0)$. Sense simetria ni asímptotes. $f'(x)=3x(x-2)$: màxim $\res{(0,0)}$, mínim $\res{(2,-4)}$."
     + cen(graf([lambda x: x**3 - 3*x*x], (-1.5, 3.8, -5, 1.5), pts=[(3, 0)], mx=[(0, 0)], mn=[(2, -4)]))),
 (1, rep(fx(r'-x^3+3x+2')),
     r"Domini $\mathbb R$. $-(x+1)^2(x-2)=0$: talls $(-1,0)$, $(2,0)$; OY $(0,2)$. $f'(x)=-3(x-1)(x+1)$: mínim $\res{(-1,0)}$, màxim $\res{(1,4)}$."
     + cen(graf([lambda x: -x**3 + 3*x + 2], (-2.5, 3, -2, 5), pts=[(2, 0), (0, 2)], mx=[(1, 4)], mn=[(-1, 0)]))),
 (2, rep(fx(r'x^4-4x^2')),
     r"Domini $\mathbb R$. Talls $(0,0)$, $(\pm2,0)$. \rest{Parella}. $f'(x)=4x(x^2-2)$: màxim $\res{(0,0)}$, mínims $\res{(\pm\sqrt2,-4)}$."
     + cen(graf([lambda x: x**4 - 4*x*x], (-2.7, 2.7, -5, 4), pts=[(-2, 0), (2, 0)], mx=[(0, 0)], mn=[(-sq(2), -4), (sq(2), -4)]))),
 (1, rep(fx(r'\dfrac{x+1}{x-1}')),
     r"Domini $\mathbb R-\{1\}$. Talls $(-1,0)$, $(0,-1)$. AV $\res{x=1}$ ($-\infty$ per l'esquerra, $+\infty$ per la dreta), AH $\res{y=1}$. $f'(x)=\frac{-2}{(x-1)^2}<0$: decreixent en $(-\infty,1)$ i en $(1,+\infty)$, sense extrems."
     + cen(graf([lambda x: (x + 1) / (x - 1)], (-5, 6, -5, 6), va=[1], ha=[1], pts=[(-1, 0), (0, -1)]))),
 (2, rep(fx(r'\dfrac{x^2+1}{x^2-1}')),
     r"Domini $\mathbb R-\{-1,1\}$. No talla OX; OY $(0,-1)$. \rest{Parella}. AV $\res{x=\pm1}$, AH $\res{y=1}$. $f'(x)=\frac{-4x}{(x^2-1)^2}$: creixent en $(-\infty,-1)\cup(-1,0)$, decreixent en $(0,1)\cup(1,+\infty)$; màxim $\res{(0,-1)}$."
     + cen(graf([lambda x: (x*x + 1) / (x*x - 1)], (-4, 4, -5, 6), va=[-1, 1], ha=[1], mx=[(0, -1)]))),
 (2, rep(fx(r'\dfrac{x}{x^2+1}')),
     r"Domini $\mathbb R$. Tall $(0,0)$. \rest{Senar}. AH $\res{y=0}$. $f'(x)=\frac{1-x^2}{(x^2+1)^2}$: mínim $\res{\left(-1,-\frac12\right)}$, màxim $\res{\left(1,\frac12\right)}$."
     + cen(graf([lambda x: x / (x*x + 1)], (-6, 6, -1, 1), ha=[0], pts=[(0, 0)], mx=[(1, 0.5)], mn=[(-1, -0.5)]))),
 (3, rep(fx(r'\dfrac{x^2}{x-2}')),
     r"Domini $\mathbb R-\{2\}$. Tall $(0,0)$. AV $\res{x=2}$; $x^2=(x-2)(x+2)+4$: AO $\res{y=x+2}$. $f'(x)=\frac{x(x-4)}{(x-2)^2}$: màxim $\res{(0,0)}$, mínim $\res{(4,8)}$."
     + cen(graf([lambda x: x*x / (x - 2)], (-6, 10, -10, 16), va=[2], oa=[(1, 2)], mx=[(0, 0)], mn=[(4, 8)]))),
 (3, rep(fx(r'\dfrac{x^2-2x+2}{x-1}')),
     r"Domini $\mathbb R-\{1\}$. No talla OX ($\Delta<0$); OY $(0,-2)$. $f(x)=x-1+\frac{1}{x-1}$: AV $\res{x=1}$, AO $\res{y=x-1}$. $f'(x)=\frac{x(x-2)}{(x-1)^2}$: màxim $\res{(0,-2)}$, mínim $\res{(2,2)}$."
     + cen(graf([lambda x: (x*x - 2*x + 2) / (x - 1)], (-4, 6, -7, 7), va=[1], oa=[(1, -1)], mx=[(0, -2)], mn=[(2, 2)]))),
 (3, rep(fx(r'\dfrac{x^3}{x^2-1}')),
     r"Domini $\mathbb R-\{-1,1\}$. Tall $(0,0)$. \rest{Senar}. AV $\res{x=\pm1}$; $x^3=(x^2-1)x+x$: AO $\res{y=x}$. $f'(x)=\frac{x^2(x^2-3)}{(x^2-1)^2}$: màxim $\res{\left(-\sqrt3,-\frac{3\sqrt3}{2}\right)}$, mínim $\res{\left(\sqrt3,\frac{3\sqrt3}{2}\right)}$; en $x=0$ no hi ha extrem."
     + cen(graf([lambda x: x**3 / (x*x - 1)], (-5, 5, -6, 6), va=[-1, 1], oa=[(1, 0)], pts=[(0, 0)], mx=[(-sq(3), -1.5*sq(3))], mn=[(sq(3), 1.5*sq(3))]))),
]))

# --- exponencials i logarítmiques ---
S.append(("Representació de funcions exponencials i logarítmiques", [
 (1, r"Representa en els mateixos eixos $f(x)=2^x$, $g(x)=2^x-4$ i $h(x)=2^{x-1}$. Indica el domini, l'asímptota i els punts de tall de cadascuna.",
     r"Totes tenen domini $\mathbb R$ i són creixents. $f$: AH $y=0$, tall $(0,1)$. \ $g$: AH $\res{y=-4}$, talls $\res{(2,0)}$ i $\res{(0,-3)}$. \ $h$: AH $y=0$, tall $\res{\left(0,\frac12\right)}$ (és $f$ desplaçada 1 unitat a la dreta)."
     + cen(graf([lambda x: 2**x, lambda x: 2**x - 4, lambda x: 2**(x - 1)], (-4, 4, -5, 6), ha=[0, -4], pts=[(0, 1), (2, 0), (0, -3), (0, 0.5)],
                labs=[(2.6, 6.1, 'f', 'below'), (3.6, 4.6, 'h', 'right'), (3.5, 3.1, 'g', 'right')]))),
 (1, rep(fx(r'\ln(x-1)+2')),
     r"Domini $(1,+\infty)$. AV $\res{x=1}$ ($\lim_{x\to1^+}f=-\infty$). OX: $\ln(x-1)=-2\Rightarrow\res{x=1+e^{-2}\approx1{,}14}$; no talla OY. Creixent, sense extrems ni AH."
     + cen(graf([lambda x: ln(x - 1) + 2 if x > 1 else None], (-1, 8, -3, 5), va=[1], pts=[(1 + e(-2), 0)]))),
 (2, rep(fx(r'x\,e^{-x}')),
     r"Domini $\mathbb R$. Tall $(0,0)$. $\lim_{x\to+\infty}x\,e^{-x}=0$: AH $\res{y=0}$ per la dreta; $\lim_{x\to-\infty}f=-\infty$. $f'(x)=(1-x)e^{-x}$: creixent en $(-\infty,1)$, decreixent en $(1,+\infty)$; màxim $\res{\left(1,\frac1e\right)}$."
     + cen(graf([lambda x: x * e(-x)], (-1.5, 7, -2, 0.8), ha=[0], pts=[(0, 0)], mx=[(1, 1 / math.e)]))),
 (2, rep(fx(r'e^{-x^2}')),
     r"Domini $\mathbb R$. Tall $(0,1)$; no talla OX. \rest{Parella}. AH $\res{y=0}$. $f'(x)=-2x\,e^{-x^2}$: creixent en $(-\infty,0)$, decreixent en $(0,+\infty)$; màxim $\res{(0,1)}$."
     + cen(graf([lambda x: e(-x*x)], (-3, 3, -0.4, 1.4), ha=[0], mx=[(0, 1)]))),
 (2, rep(fx(r'x-\ln x')),
     r"Domini $(0,+\infty)$. No talla els eixos ($f\geq1$). $\lim_{x\to0^+}(x-\ln x)=+\infty$: AV $\res{x=0}$; sense AH. $f'(x)=\frac{x-1}{x}$: mínim $\res{(1,1)}$."
     + cen(graf([lambda x: x - ln(x) if x > 0 else None], (-0.5, 6, -0.5, 5), va=[0], mn=[(1, 1)]))),
 (3, rep(fx(r'\ln(x^2-4)')),
     r"Domini $(-\infty,-2)\cup(2,+\infty)$. OX: $x^2-4=1\Rightarrow\res{(\pm\sqrt5,0)}$; no talla OY. \rest{Parella}. AV $\res{x=\pm2}$ ($f\to-\infty$). $f'(x)=\frac{2x}{x^2-4}$: decreixent en $(-\infty,-2)$, creixent en $(2,+\infty)$; sense extrems."
     + cen(graf([lambda x: ln(x*x - 4) if abs(x) > 2 else None], (-6, 6, -4, 4), va=[-2, 2], pts=[(-sq(5), 0), (sq(5), 0)]))),
]))

# --- a trossos ---
S.append(("Funcions definides a trossos", [
 (1, r"Representa la funció següent i estudia'n la continuïtat i la monotonia:" + dm(pw((r'x+2', 'x<0'), (r'2', r'0\leq x<2'), (r'6-2x', r'x\geq2'))),
     r"En $x=0$: laterals $2$ i $2$, $f(0)=2$: contínua. En $x=2$: laterals $2$ i $2$: contínua. \rest{Contínua en $\mathbb R$}. Creixent en $\res{(-\infty,0)}$, constant en $\res{(0,2)}$, decreixent en $\res{(2,+\infty)}$."
     + cen(graf([(lambda x: x + 2, -6, 0), (lambda x: 2, 0, 2), (lambda x: 6 - 2*x, 2, 6)], (-5, 5, -3, 4), pts=[(-2, 0), (3, 0), (0, 2)]))),
 (2, r"Representa" + dm(pw((r'x^2-1', r'x\leq1'), (r'\ln x', 'x>1'))) + r"i indica'n els punts de tall, la continuïtat, la monotonia i els extrems relatius.",
     r"Talls $(-1,0)$, $(1,0)$, $(0,-1)$. En $x=1$: laterals $0$ i $\ln1=0$: \rest{contínua}. Decreixent en $\res{(-\infty,0)}$, creixent en $\res{(0,+\infty)}$; mínim $\res{(0,-1)}$."
     + cen(graf([(lambda x: x*x - 1, -6, 1), (lambda x: ln(x), 1, 8)], (-3, 7, -1.6, 3), pts=[(-1, 0), (1, 0)], mn=[(0, -1)]))),
 (2, r"Representa" + dm(pw((r'2^x', r'x\leq1'), (r'\dfrac{4}{x}', 'x>1'))) + r"i estudia'n la continuïtat, les asímptotes i la monotonia. Té algun extrem relatiu en $x=1$?",
     r"En $x=1$: per l'esquerra $2$, per la dreta $4$: \rest{salt finit}. AH $\res{y=0}$ pels dos costats. Creixent en $(-\infty,1)$ i decreixent en $(1,+\infty)$. En $x=1$ \rest{no hi ha extrem}: $f(1)=2$, però a la dreta hi ha valors pròxims a 4."
     + cen(graf([(lambda x: 2**x, -6, 1.000001), (lambda x: 4 / x, 1, 8)], (-4, 7, -0.6, 5), ha=[0], pts=[(1, 2), (0, 1)], opn=[(1, 4)]))),
 (3, r"Considera la funció" + dm(pw((r'x^2+a', 'x<1'), (r'\dfrac{b}{x}', r'x\geq1'))) + tasks(1, [r"Calcula $a$ i $b$ perquè $f$ siga contínua i la seua gràfica passe pel punt $(2,1)$.", r"Per a aquests valors, representa-la i indica'n les asímptotes i els extrems relatius."]),
     tasks(1, [r"$f(2)=\frac b2=1\Rightarrow\res{b=2}$. Continuïtat en $x=1$: $1+a=2\Rightarrow\res{a=1}$.",
               r"AH $\res{y=0}$ per la dreta. Decreixent en $(-\infty,0)$, creixent en $(0,1)$, decreixent en $(1,+\infty)$: mínim $\res{(0,1)}$ i màxim $\res{(1,2)}$ (punt angulós)."])
     + cen(graf([(lambda x: x*x + 1, -6, 1), (lambda x: 2 / x, 1, 9)], (-3, 7, -0.5, 4), ha=[0], mx=[(1, 2)], mn=[(0, 1)]))),
]))

# --- context ---
S.append(("Problemes amb context", [
 (2, r"Una empresa té uns costos fixos de 200 € i un cost de 3 € per cada unitat produïda. El cost mitjà per unitat quan en produeix $x$ és $CM(x)=\dfrac{3x+200}{x}$." + tasks(1, [r"Quin domini té sentit per a aquesta funció?", r"Calcula'n les asímptotes i interpreta-les.", r"Estudia'n la monotonia i representa-la."]),
     tasks(1, [r"$\res{x>0}$ (unitats produïdes).", r"AV $\res{x=0}$: si es produeixen molt poques unitats, el cost mitjà es dispara. AH $\res{y=3}$: si es produeixen moltes unitats, el cost mitjà s'acosta a 3 € (els costos fixos es reparteixen).",
               r"$CM'(x)=-\frac{200}{x^2}<0$: \rest{sempre decreixent}."])
     + cen(graf([lambda x: (3*x + 200) / x if x > 0 else None], (-10, 200, -2, 20), va=[0], ha=[3]))),
 (2, r"La població d'una espècie de peixos en un embassament, en milers d'exemplars, ve donada per $P(t)=\dfrac{60t+20}{t+2}$, on $t$ són els anys des que es va començar a estudiar ($t\geq0$)." + tasks(1, [r"Quina era la població inicial?", r"La població creix o decreix? Justifica-ho.", r"Què passarà a llarg termini? Representa la funció."]),
     tasks(1, [r"$P(0)=\res{10}$ milers.", r"$P'(t)=\frac{100}{(t+2)^2}>0$: \rest{sempre creix}.", r"$\lim_{t\to+\infty}P(t)=60$: AH $y=60$; s'acosta a $\res{60\,000}$ peixos sense arribar-hi."])
     + cen(graf([lambda t: (60*t + 20) / (t + 2)], (-2, 40, -5, 70), ha=[60], pts=[(0, 10)]))),
 (2, r"La concentració d'un medicament en la sang (mg/l) $t$ hores després de prendre'l és $C(t)=10\,t\,e^{-t/2}$, $t\geq0$." + tasks(1, [r"Quan s'arriba a la concentració màxima? Quina és?", r"Què passa amb la concentració amb el pas del temps?", r"Representa la funció."]),
     tasks(1, [r"$C'(t)=10\,e^{-t/2}\left(1-\frac t2\right)=0\Rightarrow t=2$ (creix abans i decreix després): màxim a les $\res{2}$ h, amb $C(2)=\frac{20}{e}\approx\res{7{,}36}$ mg/l.",
               r"$\lim_{t\to+\infty}10t\,e^{-t/2}=0$: AH $y=0$, el medicament \rest{s'elimina}.", r"Vegeu la gràfica."])
     + cen(graf([lambda t: 10 * t * e(-t / 2) if t >= 0 else None], (-1, 14, -1, 9), ha=[0], pts=[(0, 0)], mx=[(2, 20 / math.e)]))),
 (3, r"Una botiga calcula que el cost (en centenars d'euros) de fer comandes de $x$ caixes i d'emmagatzemar-les és $C(x)=\dfrac{(x+8)^2}{2x}$, $x>0$." + tasks(1, [r"Calcula'n les asímptotes pel mètode del quocient.", r"Quantes caixes ha de demanar cada vegada perquè el cost siga mínim? Quin és aquest cost?", r"Representa la funció."]),
     tasks(1, [r"$(x+8)^2=x^2+16x+64$ i $\frac{x^2+16x+64}{2x}=\frac x2+8+\frac{32}{x}$: AV $\res{x=0}$, AO $\res{y=\frac x2+8}$.",
               r"$C'(x)=\frac12-\frac{32}{x^2}=0\Rightarrow x=8$, $C''(8)>0$: $\res{8}$ caixes, amb un cost de $C(8)=\res{16}$ centenars (1\,600 €)."])
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
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={representació gràfica, domini, punts de tall, simetria, funcions radicals, asímptotes, asímptota obliqua, monotonia, màxims, mínims, funcions racionals, exponencials, logarítmiques, a trossos}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

TIT = "Representació gràfica de funcions"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 7: %s. 2n de Batxillerat CCSS}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 7: %s · 2n Batxillerat CCSS" % (t, TIT))
    assert 'Unitat 7' in p and 'unitat 7' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques CCSS}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 7' if sol else "Fitxa d'exercicis · Unitat 7") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. A les gràfiques, les línies discontínues són asímptotes, els punts verds són màxims i els rojos, mínims. Pots comprovar qualsevol estudi amb l'eina «Estudi complet d'una funció» dels apunts interactius de la unitat."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos. Quan hages de representar una funció, segueix el guió: domini, punts de tall, simetria, asímptotes, monotonia i extrems; després situa tota la informació en els eixos i dibuixa la gràfica.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb l\'eina d\'estudi complet d\'una funció dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't7-fitxa-solucions.tex' if sol else 't7-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
