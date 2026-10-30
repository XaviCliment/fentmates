import os, re, sys
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

# Genera materials/3eso/t6-sistemes-equacions.html. Ús: python3 _eines/apunts/3eso-t6/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el JavaScript és a app.js i l'estil propi, a extra.css.
# Les solucions de tots els sistemes resolts es comproven amb sympy (cs).
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/3eso/t6-sistemes-equacions.html")

def L(va, es, en):
    return f'<span data-l="va">{va}</span><span data-l="es">{es}</span><span data-l="en">{en}</span>'
def P(va, es, en): return '<p>' + L(va, es, en) + '</p>'
def box(cls, title, body):
    head = f'<div class="bh">{title}</div>' if title else ''
    return f'<div class="box {cls}">{head}<div class="bb">{body}</div></div>\n'
def note(va, es, en, icon='💡'): return f'<div class="note"><p>{icon} {L(va, es, en)}</p></div>'
def ul(*items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def ol(*items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'
LV = {1: ('★☆☆', 'Nivell 1 · Bàsic', 'Nivel 1 · Básico', 'Level 1 · Basic'),
      2: ('★★☆', 'Nivell 2 · Intermedi', 'Nivel 2 · Intermedio', 'Level 2 · Intermediate'),
      3: ('★★★', 'Nivell 3 · Avançat', 'Nivel 3 · Avanzado', 'Level 3 · Advanced')}
def level(k, start, *probs):
    s, va, es, en = LV[k]
    st = f' start="{start}"' if start > 1 else ''
    return (f'<div class="lvl-h"><span class="stars">{s}</span><h3>{L(va, es, en)}</h3></div>\n'
            + box('ex', '', f'<ol class="ex-list"{st}>' + ''.join(probs) + '</ol>'))
def levels(*groups):
    out, n = '', 1
    for k, probs in enumerate(groups, 1):
        out += level(k, n, *probs); n += len(probs)
    return out
def prob(q, *steps):
    return '<li><p class="prob-q">' + q + '</p><div class="steps">' + ''.join(f'<div class="step">{s}</div>' for s in steps) + '</div></li>\n'
def practice(items, sol):
    lis = ''.join(f'<li><span class="stars">{st}</span> {t}</li>' for st, t in items)
    return box('pr', '✍ ' + L('Practica', 'Practica', 'Practice'),
               f'<ol class="ex-list">{lis}</ol><details class="sol"><summary>{L("Mostra la solució", "Mostrar la solución", "Show the solution")}</summary><div>{sol}</div></details>')
def sec(i, title, body):
    return (f'\n<!-- ======================= 6.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">6.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s): return r'\[' + s + r'\]'
def Lt(va, es, en): return r'\tri{%s}{%s}{%s}' % (va, es, en)
def SY(a, b): return r'\begin{cases}%s\\[2pt] %s\end{cases}' % (a, b)
def R(s): return r'\ \Rightarrow\ '.join(s)
def BX(xv, yv): return r'\boxed{x=%s,\ \ y=%s}' % (xv, yv)

# ---------- ginys ----------
def drill(kind, va, es, en, opts=False):
    row = (f'<div class="wrow dopts"></div><div class="wrow"><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>' if opts else
           f'<div class="wrow"><label>{L("Solució", "Solución", "Solution")} <input class="tin" type="text" inputmode="text" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat" placeholder="x = …, y = …"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>'
           + '<p class="hint-s">' + L("Escriu x = 3, y = −2 o bé 3; −2. Les fraccions, amb / (5/2).", "Escribe x = 3, y = −2 o bien 3; −2. Las fracciones, con / (5/2).", "Type x = 3, y = −2 or 3; −2. Fractions with / (5/2).") + '</p>')
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  {row}<div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-b="{v}">{t}</button>' for v, t in pairs) + '</div>'
def tin(k, lab, val, cls='w'):
    return f'<label>{lab} <input class="tin {cls}" type="text" inputmode="text" data-k="{k}" value="{val}" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="{k}"></label>'
def widget(wid, icon, title, rows, out='<div class="hsteps"></div>', extra_cls='', attrs=''):
    return (f'<div class="widget{extra_cls}" id="{wid}"{attrs}>\n  <div class="wt">{icon} {title}</div>\n'
            + ''.join(f'  {r}\n' for r in rows) + f'  {out}\n  <div class="info" aria-live="polite"></div>\n</div>\n')
HELP = '<p class="hint-s">' + L("Escriu cada equació amb el signe =, amb les incògnites x i y. Fraccions amb / ((x+1)/2) i el producte amb * o sense signe (3x).", "Escribe cada ecuación con el signo =, con las incógnitas x e y. Fracciones con / ((x+1)/2) y el producto con * o sin signo (3x).", "Type each equation with an = sign, using the unknowns x and y. Fractions with / ((x+1)/2) and products with * or no sign (3x).") + '</p>'
def two(e1, e2): return '<div class="wrow">' + tin('e1', L('1a equació', '1.ª ecuación', '1st equation'), e1) + tin('e2', L('2a equació', '2.ª ecuación', '2nd equation'), e2) + '</div>'
def solver(wid, m, title, e1, e2, qs):
    rows = [two(e1, e2), HELP, quick([(f'{a}|{b}', f'{a.replace("-", "−")} ; {b.replace("-", "−")}') for a, b in qs])]
    if m is None:
        rows.insert(0, '<div class="wrow"><div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{str(k == "auto").lower()}">{t}</button>' for k, t in [('auto', L('El més adequat', 'El más adecuado', 'Best one')), ('sub', L('Substitució', 'Sustitución', 'Substitution')), ('igu', L('Igualació', 'Igualación', 'Equalisation')), ('red', L('Reducció', 'Reducción', 'Elimination'))]) + '</div></div>')
    return widget(wid, '🧮', title, rows, extra_cls=' w-solve', attrs=f' data-m="{m}"' if m else '')
def grafw(wid, e1, e2, qs, ratio=False):
    return widget(wid, '📈', L('Mètode gràfic', 'Método gráfico', 'Graphical method'),
                  [two(e1, e2), HELP, quick([(f'{a}|{b}', f'{a.replace("-", "−")} ; {b.replace("-", "−")}') for a, b in qs])],
                  out='<div class="gout"></div>', extra_cls=' w-graf', attrs=' data-ratio' if ratio else '')

# ---------- comprovació amb sympy ----------
x, y, k = sp.symbols('x y k')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def S(s): return parse_expr(s.replace('[', '(').replace(']', ')'), transformations=TR, local_dict={'x': x, 'y': y, 'k': k}) if isinstance(s, str) else s
def EQ(e): l, r = e.split('='); return sp.expand(S(l) - S(r))
def cs(e1, e2, want):
    """want: (x, y) o 'SCI' / 'SI'"""
    A, B = EQ(e1), EQ(e2)
    sol = sp.solve([A, B], [x, y], dict=True)
    if want == 'SI': assert sol == [], (e1, e2, sol); return
    if want == 'SCI': assert len(sol) == 1 and len(sol[0]) == 1, (e1, e2, sol); return
    assert sol == [{x: sp.nsimplify(want[0]), y: sp.nsimplify(want[1])}], (e1, e2, sol, want)
def ok(e, xv, yv): assert EQ(e).subs({x: sp.nsimplify(xv), y: sp.nsimplify(yv)}) == 0, (e, xv, yv)
def nok(e, xv, yv): assert EQ(e).subs({x: sp.nsimplify(xv), y: sp.nsimplify(yv)}) != 0, (e, xv, yv)
def same(a, b): assert sp.expand(EQ(a) - EQ(b)) == 0, (a, b)
def prop(a, b):
    """dues equacions equivalents (una múltiple de l'altra)"""
    A, B = EQ(a), EQ(b); r = sp.simplify(A / B); assert r.is_number and r != 0, (a, b, r)

# ---------- gràfiques estàtiques (SVG) ----------
def svg_graph(lines, pts=(), R=6, cap=None):
    W = H = 300
    sx = lambda v: (v + R) / (2 * R) * W
    sy = lambda v: H - (v + R) / (2 * R) * H
    g = ''
    for i in range(-R, R + 1):
        g += f'<line class="grid" x1="{sx(i):.1f}" y1="0" x2="{sx(i):.1f}" y2="{H}"/><line class="grid" x1="0" y1="{sy(i):.1f}" x2="{W}" y2="{sy(i):.1f}"/>'
    g += f'<line class="ax" x1="0" y1="{sy(0):.1f}" x2="{W}" y2="{sy(0):.1f}"/><line class="ax" x1="{sx(0):.1f}" y1="0" x2="{sx(0):.1f}" y2="{H}"/>'
    for i in range(-R + 1, R):
        if i: g += f'<text class="tk" x="{sx(i):.1f}" y="{sy(0) + 13:.1f}" text-anchor="middle">{i}</text><text class="tk" x="{sx(0) - 5:.1f}" y="{sy(i) + 4:.1f}" text-anchor="end">{i}</text>'
    g += f'<text class="tk ax-l" x="{W - 6}" y="{sy(0) - 6:.1f}" text-anchor="end">x</text><text class="tk ax-l" x="{sx(0) + 6:.1f}" y="12">y</text>'
    for j, (a, b, c, *opt) in enumerate(lines):
        X = R + 1
        p = (-X, (c + a * X) / b, X, (c - a * X) / b) if b else (c / a, -X, c / a, X)
        cls = f'ln ln{opt[0] if opt else j}' + (' dash' if len(opt) > 1 and opt[1] else '')
        g += f'<line class="{cls}" x1="{sx(p[0]):.1f}" y1="{sy(p[1]):.1f}" x2="{sx(p[2]):.1f}" y2="{sy(p[3]):.1f}"/>'
        if b: assert True
    for px, py, cls, lab in pts:
        g += f'<circle class="{cls}" cx="{sx(px):.1f}" cy="{sy(py):.1f}" r="{7 if cls == "cut" else 4}"/>'
        if lab: g += f'<text class="plab" x="{sx(px) + 8:.1f}" y="{sy(py) - 8:.1f}">{lab}</text>'
    fig = f'<svg class="sgraf" viewBox="0 0 {W} {H}" role="img" aria-label="gràfica">{g}</svg>'
    return f'<figure>{fig}<figcaption>{cap}</figcaption></figure>' if cap else f'<figure>{fig}</figure>'
def figs(*f): return '<div class="figs">' + ''.join(f) + '</div>'
def tv(xs, ys, cls=''):
    return ('<div class="tbl-wrap"><table class="data tv %s"><tbody><tr><th>\\(x\\)</th>' % cls + ''.join(f'<td>\\({v}\\)</td>' for v in xs)
            + '</tr><tr><th>\\(y\\)</th>' + ''.join(f'<td>\\({v}\\)</td>' for v in ys) + '</tr></tbody></table></div>')
def tvc(e, xs, cls=''):
    """taula de valors d'una equació ax+by=c (comprovada)"""
    ys = []
    for xv in xs:
        sol = sp.solve(EQ(e).subs(x, xv), y); assert len(sol) == 1; ys.append(sol[0])
    return tv(xs, [str(v) for v in ys], cls)

# =====================================================================
# 6.1 Equacions lineals amb dues incògnites
# =====================================================================
s1 = box('def', L('Equació lineal amb dues incògnites', 'Ecuación lineal con dos incógnitas', 'Linear equation in two unknowns'),
  P(r"Una <strong>equació lineal</strong> (o de primer grau) <strong>amb dues incògnites</strong> és una equació que, un cop reduïda, es pot escriure així:",
    r"Una <strong>ecuación lineal</strong> (o de primer grado) <strong>con dos incógnitas</strong> es una ecuación que, una vez reducida, se puede escribir así:",
    r"A <strong>linear</strong> (first-degree) <strong>equation in two unknowns</strong> is one that, once simplified, can be written as:")
  + D(r"ax+by=c")
  + ul(L(r"\(x\) i \(y\) són les <strong>incògnites</strong>;", r"\(x\) e \(y\) son las <strong>incógnitas</strong>;", r"\(x\) and \(y\) are the <strong>unknowns</strong>;"),
       L(r"\(a\) i \(b\) són els <strong>coeficients</strong> (nombres que multipliquen les incògnites);", r"\(a\) y \(b\) son los <strong>coeficientes</strong> (números que multiplican a las incógnitas);", r"\(a\) and \(b\) are the <strong>coefficients</strong> (the numbers multiplying the unknowns);"),
       L(r"\(c\) és el <strong>terme independent</strong>.", r"\(c\) es el <strong>término independiente</strong>.", r"\(c\) is the <strong>constant term</strong>."))
  + P(r"Per exemple, \(2x+y=7\) o \(x-3y=0\). En canvi, \(x^2+y=5\) o \(xy=6\) <em>no</em> són lineals.",
      r"Por ejemplo, \(2x+y=7\) o \(x-3y=0\). En cambio, \(x^2+y=5\) o \(xy=6\) <em>no</em> son lineales.",
      r"For example, \(2x+y=7\) or \(x-3y=0\). On the other hand, \(x^2+y=5\) and \(xy=6\) are <em>not</em> linear."))
s1 += box('def', L('Solucions: parells de nombres', 'Soluciones: pares de números', 'Solutions: pairs of numbers'),
  P(r"Una <strong>solució</strong> és un <strong>parell de valors</strong> \((x,\,y)\) que fa certa la igualtat. Per a comprovar-ho, substituïm i calculem:",
    r"Una <strong>solución</strong> es un <strong>par de valores</strong> \((x,\,y)\) que hace cierta la igualdad. Para comprobarlo, sustituimos y calculamos:",
    r"A <strong>solution</strong> is a <strong>pair of values</strong> \((x,\,y)\) that makes the equality true. To check, substitute and work it out:")
  + D(r"2x+y=7:\qquad (1,\,5)\to 2\cdot1+5=7\ \checkmark\qquad (3,\,1)\to 2\cdot3+1=7\ \checkmark\qquad (2,\,2)\to 2\cdot2+2=6\neq7\ \times")
  + note(r"L'ordre importa: en el parell \((1,\,5)\) el primer nombre és la \(x\) i el segon, la \(y\). El parell \((5,\,1)\) és un altre: \(2\cdot5+1=11\neq7\).",
         r"El orden importa: en el par \((1,\,5)\) el primer número es la \(x\) y el segundo, la \(y\). El par \((5,\,1)\) es otro: \(2\cdot5+1=11\neq7\).",
         r"Order matters: in the pair \((1,\,5)\) the first number is \(x\) and the second is \(y\). The pair \((5,\,1)\) is a different one: \(2\cdot5+1=11\neq7\).", '⚠'))
ok('2x+y=7', 1, 5); ok('2x+y=7', 3, 1); nok('2x+y=7', 2, 2); nok('2x+y=7', 5, 1)
s1 += box('prop', L('Infinites solucions: la taula de valors', 'Infinitas soluciones: la tabla de valores', 'Infinitely many solutions: the table of values'),
  P(r"Una equació amb dues incògnites té <strong>infinites solucions</strong>: per a cada valor que donem a la \(x\), podem calcular el valor de la \(y\). El més còmode és <strong>aïllar la \(y\)</strong> i fer una <strong>taula de valors</strong>:",
    r"Una ecuación con dos incógnitas tiene <strong>infinitas soluciones</strong>: para cada valor que demos a la \(x\), podemos calcular el valor de la \(y\). Lo más cómodo es <strong>despejar la \(y\)</strong> y hacer una <strong>tabla de valores</strong>:",
    r"An equation in two unknowns has <strong>infinitely many solutions</strong>: for every value we give \(x\), we can work out \(y\). The easiest way is to <strong>isolate \(y\)</strong> and make a <strong>table of values</strong>:")
  + D(r"2x+y=7\ \Rightarrow\ y=7-2x")
  + tvc('2x+y=7', [-1, 0, 1, 2, 3, 4])
  + P(r"Cada columna de la taula és una solució: \((-1,\,9),\ (0,\,7),\ (1,\,5)\ldots\)", r"Cada columna de la tabla es una solución: \((-1,\,9),\ (0,\,7),\ (1,\,5)\ldots\)", r"Each column of the table is a solution: \((-1,\,9),\ (0,\,7),\ (1,\,5)\ldots\)"))
s1 += box('prop', L('La gràfica és una recta', 'La gráfica es una recta', 'The graph is a straight line'),
  P(r"Si representem les solucions com a punts \((x,\,y)\) en uns eixos de coordenades, queden <strong>alineats</strong>: la gràfica d'una equació lineal amb dues incògnites és una <strong>recta</strong>. Cada punt de la recta és una solució, i cada solució és un punt de la recta.",
    r"Si representamos las soluciones como puntos \((x,\,y)\) en unos ejes de coordenadas, quedan <strong>alineados</strong>: la gráfica de una ecuación lineal con dos incógnitas es una <strong>recta</strong>. Cada punto de la recta es una solución, y cada solución es un punto de la recta.",
    r"If we plot the solutions as points \((x,\,y)\) on a pair of axes, they line up: the graph of a linear equation in two unknowns is a <strong>straight line</strong>. Every point on the line is a solution, and every solution is a point on the line.")
  + figs(svg_graph([(2, 1, 7)], [(v, 7 - 2 * v, 'pt p0', None) for v in [-1, 0, 1, 2, 3, 4]], R=10, cap=r'\(2x+y=7\)'))
  + note(r"Per a dibuixar una recta n'hi ha prou amb <strong>dos punts</strong> (un tercer serveix per a comprovar). Tria valors de \(x\) que donen \(y\) enteres: és més fàcil situar els punts.",
         r"Para dibujar una recta basta con <strong>dos puntos</strong> (un tercero sirve para comprobar). Elige valores de \(x\) que den \(y\) enteras: es más fácil situar los puntos.",
         r"Two points are <strong>enough</strong> to draw a line (a third one is a good check). Choose values of \(x\) that give whole-number \(y\): the points are easier to plot.")
  + widget('w-line', '📈', L('Taula de valors i recta', 'Tabla de valores y recta', 'Table of values and line'),
           ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), '2x+y=7') + '</div>', HELP,
            quick([('2x+y=7', '2x+y = 7'), ('x-2y=4', 'x−2y = 4'), ('3x+2y=6', '3x+2y = 6'), ('y=2x-3', 'y = 2x−3'), ('x+y=0', 'x+y = 0'), ('x=3', 'x = 3')])],
           out='<div class="gout"></div>'))
s1 += levels(
 [prob(L(r"Quins d'aquests parells són solució de \(3x-y=5\)? \((2,\,1)\), \((0,\,-5)\), \((1,\,1)\), \((-1,\,-8)\).", r"¿Cuáles de estos pares son solución de \(3x-y=5\)? \((2,\,1)\), \((0,\,-5)\), \((1,\,1)\), \((-1,\,-8)\).", r"Which of these pairs are solutions of \(3x-y=5\)? \((2,\,1)\), \((0,\,-5)\), \((1,\,1)\), \((-1,\,-8)\)."),
       D(r"(2,1):\ 6-1=5\ \checkmark\qquad (0,-5):\ 0-(-5)=5\ \checkmark\qquad (1,1):\ 3-1=2\neq5\ \times\qquad (-1,-8):\ -3+8=5\ \checkmark"),
       P(r"Són solució \((2,\,1)\), \((0,\,-5)\) i \((-1,\,-8)\).", r"Son solución \((2,\,1)\), \((0,\,-5)\) y \((-1,\,-8)\).", r"\((2,\,1)\), \((0,\,-5)\) and \((-1,\,-8)\) are solutions.")),
  prob(L(r"Escriu tres solucions de \(x+2y=8\).", r"Escribe tres soluciones de \(x+2y=8\).", r"Write three solutions of \(x+2y=8\)."),
       P(r"Ací és més fàcil aïllar la \(x\): \(x=8-2y\). Donem valors a la \(y\):", r"Aquí es más fácil despejar la \(x\): \(x=8-2y\). Damos valores a la \(y\):", r"Here it's easier to isolate \(x\): \(x=8-2y\). Give values to \(y\):"),
       D(r"y=0\to x=8;\qquad y=1\to x=6;\qquad y=3\to x=2"),
       P(r"Per exemple, \((8,\,0)\), \((6,\,1)\) i \((2,\,3)\).", r"Por ejemplo, \((8,\,0)\), \((6,\,1)\) y \((2,\,3)\).", r"For example, \((8,\,0)\), \((6,\,1)\) and \((2,\,3)\)."))],
 [prob(L(r"Troba \(k\) perquè el parell \((2,\,-1)\) siga solució de \(kx+3y=5\).", r"Halla \(k\) para que el par \((2,\,-1)\) sea solución de \(kx+3y=5\).", r"Find \(k\) so that \((2,\,-1)\) is a solution of \(kx+3y=5\)."),
       D(r"k\cdot2+3\cdot(-1)=5\ \Rightarrow\ 2k-3=5\ \Rightarrow\ 2k=8\ \Rightarrow\ \boxed{k=4}")),
  prob(L(r"Fes una taula de valors i representa la recta \(2x-3y=6\).", r"Haz una tabla de valores y representa la recta \(2x-3y=6\).", r"Make a table of values and draw the line \(2x-3y=6\)."),
       D(r"-3y=6-2x\ \Rightarrow\ y=\frac{2x-6}{3}"),
       P(r"Triem valors de \(x\) que facen exacta la divisió entre 3:", r"Elegimos valores de \(x\) que hagan exacta la división entre 3:", r"Choose values of \(x\) that divide exactly by 3:")
       + tvc('2x-3y=6', [-3, 0, 3, 6]),
       figs(svg_graph([(2, -3, 6)], [(v, (2 * v - 6) / 3, 'pt p0', None) for v in [-3, 0, 3, 6]], R=8)))],
 [prob(L(r"Troba la solució de \(4x+y=18\) en què la \(y\) és el doble que la \(x\).", r"Halla la solución de \(4x+y=18\) en la que la \(y\) es el doble que la \(x\).", r"Find the solution of \(4x+y=18\) where \(y\) is twice \(x\)."),
       P(r"Si \(y=2x\), substituïm en l'equació:", r"Si \(y=2x\), sustituimos en la ecuación:", r"If \(y=2x\), substitute into the equation:"),
       D(r"4x+2x=18\ \Rightarrow\ 6x=18\ \Rightarrow\ x=3,\quad y=6"),
       P(r"La solució és \((3,\,6)\): \(12+6=18\) ✓. Fixa't que hem fet servir <em>dues</em> condicions: això és un sistema d'equacions!", r"La solución es \((3,\,6)\): \(12+6=18\) ✓. Fíjate en que hemos usado <em>dos</em> condiciones: ¡esto es un sistema de ecuaciones!", r"The solution is \((3,\,6)\): \(12+6=18\) ✓. Notice we used <em>two</em> conditions: that's a system of equations!"))])
ok('3x-y=5', 2, 1); ok('3x-y=5', 0, -5); nok('3x-y=5', 1, 1); ok('3x-y=5', -1, -8); ok('x+2y=8', 8, 0); ok('x+2y=8', 6, 1); ok('x+2y=8', 2, 3)
ok('4x+3y=5', 2, -1); cs('4x+y=18', 'y=2x', (3, 6))
s1 += practice([
  ('★', L(r"a) És \((-1,\,4)\) solució de \(5x+2y=3\)? b) I \((1,\,-1)\)?", r"a) ¿Es \((-1,\,4)\) solución de \(5x+2y=3\)? b) ¿Y \((1,\,-1)\)?", r"a) Is \((-1,\,4)\) a solution of \(5x+2y=3\)? b) What about \((1,\,-1)\)?")),
  ('★★', L(r"c) Fes una taula de valors de \(x-2y=4\) i representa-la. d) Troba \(m\) perquè \((3,\,{m})\) siga solució de \(2x-5y=1\).", r"c) Haz una tabla de valores de \(x-2y=4\) y represéntala. d) Halla \(m\) para que \((3,\,{m})\) sea solución de \(2x-5y=1\).", r"c) Make a table of values for \(x-2y=4\) and draw it. d) Find \(m\) so that \((3,\,{m})\) is a solution of \(2x-5y=1\).")),
  ('★★★', L(r"e) Escriu totes les solucions de \(x+y=4\) en què \(x\) i \(y\) són nombres naturals (incloent-hi el 0).", r"e) Escribe todas las soluciones de \(x+y=4\) en las que \(x\) e \(y\) son números naturales (incluido el 0).", r"e) Write all the solutions of \(x+y=4\) where \(x\) and \(y\) are natural numbers (including 0)."))],
  D(r"\text{a)}\ 5\cdot(-1)+2\cdot4=3\ \checkmark\ \text{%s}\qquad \text{b)}\ 5-2=3\ \checkmark\ \text{%s}" % (Lt('sí', 'sí', 'yes'), Lt('sí', 'sí', 'yes')))
  + P(r"c) \(y=\frac{x-4}{2}\):", r"c) \(y=\frac{x-4}{2}\):", r"c) \(y=\frac{x-4}{2}\):") + tvc('x-2y=4', [0, 2, 4, 6])
  + D(r"\text{d)}\ 6-5m=1\Rightarrow -5m=-5\Rightarrow m=1\qquad \text{e)}\ (0,4),\ (1,3),\ (2,2),\ (3,1),\ (4,0)"))
ok('5x+2y=3', -1, 4); ok('5x+2y=3', 1, -1); ok('2x-5y=1', 3, 1)
for i in range(5): ok('x+y=4', i, 4 - i)

# =====================================================================
# 6.2 Sistemes de dues equacions amb dues incògnites
# =====================================================================
s2 = box('def', L("Sistema d'equacions lineals", 'Sistema de ecuaciones lineales', 'System of linear equations'),
  P(r"Un <strong>sistema de dues equacions lineals amb dues incògnites</strong> està format per dues equacions de les quals busquem les <strong>solucions comunes</strong>. S'escriu amb una clau:",
    r"Un <strong>sistema de dos ecuaciones lineales con dos incógnitas</strong> está formado por dos ecuaciones de las que buscamos las <strong>soluciones comunes</strong>. Se escribe con una llave:",
    r"A <strong>system of two linear equations in two unknowns</strong> is a pair of equations whose <strong>common solutions</strong> we look for. It is written with a brace:")
  + D(SY(r"ax+by=c", r"a'x+b'y=c'") + r"\qquad\qquad " + SY(r"x+y=5", r"x-y=1"))
  + P(r"La <strong>solució del sistema</strong> és el parell \((x,\,y)\) que compleix <strong>les dues equacions alhora</strong>. <strong>Resoldre</strong> un sistema és trobar-ne totes les solucions.",
      r"La <strong>solución del sistema</strong> es el par \((x,\,y)\) que cumple <strong>las dos ecuaciones a la vez</strong>. <strong>Resolver</strong> un sistema es hallar todas sus soluciones.",
      r"The <strong>solution of the system</strong> is the pair \((x,\,y)\) that satisfies <strong>both equations at once</strong>. <strong>Solving</strong> a system means finding all its solutions.")
  + D(r"(3,\,2):\quad 3+2=5\ \checkmark,\quad 3-2=1\ \checkmark\qquad\qquad (4,\,1):\quad 4+1=5\ \checkmark,\quad 4-1=3\neq1\ \times")
  + P(r"\((3,\,2)\) és la solució del sistema; \((4,\,1)\) només és solució de la primera equació.", r"\((3,\,2)\) es la solución del sistema; \((4,\,1)\) solo es solución de la primera ecuación.", r"\((3,\,2)\) is the solution of the system; \((4,\,1)\) only solves the first equation."))
cs('x+y=5', 'x-y=1', (3, 2)); nok('x-y=1', 4, 1)
s2 += box('prop', L('Interpretació gràfica', 'Interpretación gráfica', 'Graphical meaning'),
  P(r"Cada equació és una recta. La solució del sistema és un punt que està en <strong>les dues rectes</strong> alhora: el <strong>punt de tall</strong>.",
    r"Cada ecuación es una recta. La solución del sistema es un punto que está en <strong>las dos rectas</strong> a la vez: el <strong>punto de corte</strong>.",
    r"Each equation is a line. The solution of the system is a point lying on <strong>both lines</strong>: the <strong>crossing point</strong>.")
  + figs(svg_graph([(1, 1, 5), (1, -1, 1)], [(3, 2, 'cut', '(3, 2)')], R=6, cap=r'\(x+y=5\ \) i \(\ x-y=1\)'))
  + note(r"Abans de resoldre un sistema, convé escriure cada equació en la <strong>forma reduïda</strong> \(ax+by=c\): les incògnites al primer membre, ordenades, i el nombre al segon. Si hi ha parèntesis o denominadors, primer els traiem (ho veurem en l'apartat 6.8).",
         r"Antes de resolver un sistema, conviene escribir cada ecuación en la <strong>forma reducida</strong> \(ax+by=c\): las incógnitas en el primer miembro, ordenadas, y el número en el segundo. Si hay paréntesis o denominadores, primero los quitamos (lo veremos en el apartado 6.8).",
         r"Before solving a system, write each equation in <strong>standard form</strong> \(ax+by=c\): the unknowns on the left, in order, and the number on the right. If there are brackets or fractions, clear them first (see section 6.8)."))
s2 += box('prop', L('Com resoldrem els sistemes?', '¿Cómo resolveremos los sistemas?', 'How will we solve systems?'),
  P(r"La idea de tots els mètodes algebraics és la mateixa: <strong>eliminar una incògnita</strong> per a obtindre una equació de primer grau amb una sola incògnita, que ja sabem resoldre. Veurem tres mètodes algebraics, <strong>substitució</strong>, <strong>igualació</strong> i <strong>reducció</strong>, i el <strong>mètode gràfic</strong>. Tots donen la mateixa solució.",
    r"La idea de todos los métodos algebraicos es la misma: <strong>eliminar una incógnita</strong> para obtener una ecuación de primer grado con una sola incógnita, que ya sabemos resolver. Veremos tres métodos algebraicos, <strong>sustitución</strong>, <strong>igualación</strong> y <strong>reducción</strong>, y el <strong>método gráfico</strong>. Todos dan la misma solución.",
    r"All the algebraic methods share one idea: <strong>eliminate one unknown</strong> to get a first-degree equation in a single unknown, which we already know how to solve. We'll see three algebraic methods, <strong>substitution</strong>, <strong>equalisation</strong> and <strong>elimination</strong>, plus the <strong>graphical method</strong>. They all give the same solution.")
  + widget('w-pair', '🔍', L('És solució del sistema?', '¿Es solución del sistema?', 'Is it a solution of the system?'),
           [two('x+y=5', 'x-y=1'), '<div class="wrow">' + tin('x', 'x =', '3', 's') + tin('y', 'y =', '2', 's') + '</div>', HELP,
            quick([('x+y=5|x-y=1|3|2', '(3, 2)'), ('x+y=5|x-y=1|4|1', '(4, 1)'), ('2x+3y=4|x-y=7|5|-2', '2x+3y=4, x−y=7: (5, −2)'), ('3x-2y=1|x+y=2|1|1', '3x−2y=1, x+y=2: (1, 1)'), ('x/2+y=3|x-y=0|2|2', 'x/2+y=3, x−y=0: (2, 2)')])])
  + drill('pair', 'Entrena: és solució?', 'Entrena: ¿es solución?', 'Train: is it a solution?', opts=True))
ok('2x+3y=4', 5, -2); ok('x-y=7', 5, -2); cs('3x-2y=1', 'x+y=2', (1, 1)); cs('x/2+y=3', 'x-y=0', (2, 2))
s2 += levels(
 [prob(L(r"Comprova si \((2,\,-1)\) és solució del sistema \(" + SY('3x+2y=4', 'x-y=3') + r"\).", r"Comprueba si \((2,\,-1)\) es solución del sistema \(" + SY('3x+2y=4', 'x-y=3') + r"\).", r"Check whether \((2,\,-1)\) is a solution of the system \(" + SY('3x+2y=4', 'x-y=3') + r"\)."),
       D(r"3\cdot2+2\cdot(-1)=6-2=4\ \checkmark\qquad 2-(-1)=3\ \checkmark"),
       P(r"Compleix les dues equacions: <strong>sí</strong> que és solució.", r"Cumple las dos ecuaciones: <strong>sí</strong> es solución.", r"It satisfies both equations: it <strong>is</strong> a solution."))],
 [prob(L(r"Quin d'aquests parells és la solució del sistema \(" + SY('x+2y=5', '2x-y=5') + r"\)? \((1,\,2)\), \((3,\,1)\), \((5,\,0)\).", r"¿Cuál de estos pares es la solución del sistema \(" + SY('x+2y=5', '2x-y=5') + r"\)? \((1,\,2)\), \((3,\,1)\), \((5,\,0)\).", r"Which of these pairs is the solution of the system \(" + SY('x+2y=5', '2x-y=5') + r"\)? \((1,\,2)\), \((3,\,1)\), \((5,\,0)\)."),
       D(r"(1,2):\ 1+4=5\ \checkmark,\ \ 2-2=0\ \times\qquad (3,1):\ 3+2=5\ \checkmark,\ \ 6-1=5\ \checkmark\qquad (5,0):\ 5\ \checkmark,\ \ 10\ \times"),
       P(r"Els tres compleixen la primera, però només \((3,\,1)\) compleix les dues: és la solució.", r"Los tres cumplen la primera, pero solo \((3,\,1)\) cumple las dos: es la solución.", r"All three satisfy the first, but only \((3,\,1)\) satisfies both: it's the solution."))],
 [prob(L(r"Troba \(a\) i \(b\) perquè \((2,\,-1)\) siga la solució de \(" + SY('ax+3y=5', '2x+by=7') + r"\).", r"Halla \(a\) y \(b\) para que \((2,\,-1)\) sea la solución de \(" + SY('ax+3y=5', '2x+by=7') + r"\).", r"Find \(a\) and \(b\) so that \((2,\,-1)\) is the solution of \(" + SY('ax+3y=5', '2x+by=7') + r"\)."),
       D(r"2a+3\cdot(-1)=5\ \Rightarrow\ 2a=8\ \Rightarrow\ \boxed{a=4}"),
       D(r"2\cdot2+b\cdot(-1)=7\ \Rightarrow\ 4-b=7\ \Rightarrow\ \boxed{b=-3}"))])
cs('3x+2y=4', 'x-y=3', (2, -1)); cs('x+2y=5', '2x-y=5', (3, 1)); ok('x+2y=5', 1, 2); ok('x+2y=5', 5, 0); cs('4x+3y=5', '2x-3y=7', (2, -1))
s2 += practice([
  ('★', L(r"a) És \((1,\,4)\) solució de \(" + SY('2x+y=6', 'x-y=-3') + r"\)?", r"a) ¿Es \((1,\,4)\) solución de \(" + SY('2x+y=6', 'x-y=-3') + r"\)?", r"a) Is \((1,\,4)\) a solution of \(" + SY('2x+y=6', 'x-y=-3') + r"\)?")),
  ('★★', L(r"b) Comprova quin dels parells \((0,\,3)\), \((2,\,1)\) i \((-1,\,5)\) és la solució de \(" + SY('2x+y=3', 'x+y=4') + r"\).", r"b) Comprueba cuál de los pares \((0,\,3)\), \((2,\,1)\) y \((-1,\,5)\) es la solución de \(" + SY('2x+y=3', 'x+y=4') + r"\).", r"b) Check which of \((0,\,3)\), \((2,\,1)\) and \((-1,\,5)\) is the solution of \(" + SY('2x+y=3', 'x+y=4') + r"\).")),
  ('★★★', L(r"c) Escriu un sistema que tinga la solució \((3,\,-2)\).", r"c) Escribe un sistema que tenga la solución \((3,\,-2)\).", r"c) Write a system whose solution is \((3,\,-2)\)."))],
  D(r"\text{a)}\ 2+4=6\ \checkmark,\ \ 1-4=-3\ \checkmark:\ \text{%s}\qquad \text{b)}\ (-1,\,5):\ -2+5=3\ \checkmark,\ \ -1+5=4\ \checkmark" % Lt('sí', 'sí', 'yes'))
  + P(r"c) Per exemple, \(x+y=1\) i \(x-y=5\) (hi ha infinites respostes possibles).", r"c) Por ejemplo, \(x+y=1\) y \(x-y=5\) (hay infinitas respuestas posibles).", r"c) For example, \(x+y=1\) and \(x-y=5\) (there are infinitely many possible answers)."))
cs('2x+y=6', 'x-y=-3', (1, 4)); cs('2x+y=3', 'x+y=4', (-1, 5)); nok('x+y=4', 0, 3); nok('2x+y=3', 2, 1); cs('x+y=1', 'x-y=5', (3, -2))

# =====================================================================
# 6.3 Mètode de substitució
# =====================================================================
s3 = box('prop', L('Mètode de substitució', 'Método de sustitución', 'Substitution method'),
  ol(L(r"<strong>Aïllem</strong> una incògnita en una de les equacions (la més fàcil: la que té coeficient \(1\) o \(-1\)).", r"<strong>Despejamos</strong> una incógnita en una de las ecuaciones (la más fácil: la que tiene coeficiente \(1\) o \(-1\)).", r"<strong>Isolate</strong> one unknown in one of the equations (the easiest: one with coefficient \(1\) or \(-1\))."),
     L(r"<strong>Substituïm</strong> l'expressió obtinguda en l'<strong>altra</strong> equació. Queda una equació amb una sola incògnita.", r"<strong>Sustituimos</strong> la expresión obtenida en la <strong>otra</strong> ecuación. Queda una ecuación con una sola incógnita.", r"<strong>Substitute</strong> that expression into the <strong>other</strong> equation. You get an equation in a single unknown."),
     L(r"<strong>Resolem</strong> aquesta equació.", r"<strong>Resolvemos</strong> esta ecuación.", r"<strong>Solve</strong> that equation."),
     L(r"<strong>Substituïm</strong> el valor trobat en l'expressió aïllada per a calcular l'altra incògnita.", r"<strong>Sustituimos</strong> el valor hallado en la expresión despejada para calcular la otra incógnita.", r"<strong>Substitute</strong> the value back into the isolated expression to find the other unknown."),
     L(r"<strong>Comprovem</strong> la solució en les dues equacions.", r"<strong>Comprobamos</strong> la solución en las dos ecuaciones.", r"<strong>Check</strong> the solution in both equations."))
  + D(SY('2x+y=7', '3x-2y=7'))
  + D(r"\text{1. }y=7-2x\qquad \text{2. }3x-2(7-2x)=7")
  + D(r"\text{3. }3x-14+4x=7\ \Rightarrow\ 7x=21\ \Rightarrow\ x=3\qquad \text{4. }y=7-2\cdot3=1")
  + P(r"Comprovació: \(2\cdot3+1=7\) ✓ i \(3\cdot3-2\cdot1=7\) ✓. La solució és \(x=3,\ y=1\).", r"Comprobación: \(2\cdot3+1=7\) ✓ y \(3\cdot3-2\cdot1=7\) ✓. La solución es \(x=3,\ y=1\).", r"Check: \(2\cdot3+1=7\) ✓ and \(3\cdot3-2\cdot1=7\) ✓. The solution is \(x=3,\ y=1\).")
  + note(r"Quan substituïm, l'expressió va sempre <strong>entre parèntesis</strong>: \(-2(7-2x)=-14+4x\). Si oblidem el parèntesi, el \(-2\) només multiplicaria el 7 i el resultat eixiria malament.",
         r"Cuando sustituimos, la expresión va siempre <strong>entre paréntesis</strong>: \(-2(7-2x)=-14+4x\). Si olvidamos el paréntesis, el \(-2\) solo multiplicaría al 7 y el resultado saldría mal.",
         r"When substituting, the expression always goes <strong>in brackets</strong>: \(-2(7-2x)=-14+4x\). Without the bracket, the \(-2\) would only multiply the 7 and the answer would come out wrong.", '⚠')
  + note(r"El mètode de substitució és el més còmode quan alguna incògnita té coeficient \(1\) o \(-1\), o quan ja està aïllada (per exemple, \(y=3x-2\)).",
         r"El método de sustitución es el más cómodo cuando alguna incógnita tiene coeficiente \(1\) o \(-1\), o cuando ya está despejada (por ejemplo, \(y=3x-2\)).",
         r"Substitution is easiest when one unknown has coefficient \(1\) or \(-1\), or is already isolated (e.g. \(y=3x-2\))."))
cs('2x+y=7', '3x-2y=7', (3, 1)); same('3x-2(7-2x)=7', '7x=21')
s3 += solver('w-sub', 'sub', L('Substitució pas a pas', 'Sustitución paso a paso', 'Substitution step by step'), '2x+y=7', '3x-2y=7',
             [('2x+y=7', '3x-2y=7'), ('x=2y', 'x+y=9'), ('x-2y=1', '3x+y=10'), ('y=3x-1', '2x+y=9'), ('2x+3y=1', '3x-4y=10'), ('x+2y=3', '2x+4y=1')])
s3 += drill('sub', 'Entrena: mètode de substitució', 'Entrena: método de sustitución', 'Train: substitution method')
s3 += levels(
 [prob(L(r"Resol \(" + SY('x=2y', 'x+y=9') + r"\).", r"Resuelve \(" + SY('x=2y', 'x+y=9') + r"\).", r"Solve \(" + SY('x=2y', 'x+y=9') + r"\)."),
       P(r"La \(x\) ja està aïllada: la substituïm en la segona equació.", r"La \(x\) ya está despejada: la sustituimos en la segunda ecuación.", r"\(x\) is already isolated: substitute it into the second equation."),
       D(R([r"2y+y=9", r"3y=9", r"y=3"]) + r"\qquad x=2\cdot3=6\qquad " + BX(6, 3))),
  prob(L(r"Resol \(" + SY('x+y=8', 'x-y=2') + r"\).", r"Resuelve \(" + SY('x+y=8', 'x-y=2') + r"\).", r"Solve \(" + SY('x+y=8', 'x-y=2') + r"\)."),
       D(r"x=8-y\ \Rightarrow\ (8-y)-y=2\ \Rightarrow\ -2y=-6\ \Rightarrow\ y=3"),
       D(r"x=8-3=5\qquad " + BX(5, 3)))],
 [prob(L(r"Resol \(" + SY('3x+y=11', '5x-2y=0') + r"\).", r"Resuelve \(" + SY('3x+y=11', '5x-2y=0') + r"\).", r"Solve \(" + SY('3x+y=11', '5x-2y=0') + r"\)."),
       D(r"y=11-3x\ \Rightarrow\ 5x-2(11-3x)=0"),
       D(R([r"5x-22+6x=0", r"11x=22", r"x=2"]) + r"\qquad y=11-3\cdot2=5"),
       P(r"Comprovació: \(6+5=11\) ✓; \(10-10=0\) ✓. Solució: \(x=2,\ y=5\).", r"Comprobación: \(6+5=11\) ✓; \(10-10=0\) ✓. Solución: \(x=2,\ y=5\).", r"Check: \(6+5=11\) ✓; \(10-10=0\) ✓. Solution: \(x=2,\ y=5\)."))],
 [prob(L(r"Resol per substitució \(" + SY('2x+3y=1', '3x-4y=10') + r"\), on cap incògnita té coeficient 1.", r"Resuelve por sustitución \(" + SY('2x+3y=1', '3x-4y=10') + r"\), donde ninguna incógnita tiene coeficiente 1.", r"Solve by substitution \(" + SY('2x+3y=1', '3x-4y=10') + r"\), where no unknown has coefficient 1."),
       D(r"2x=1-3y\ \Rightarrow\ x=\frac{1-3y}{2}"),
       D(r"3\cdot\frac{1-3y}{2}-4y=10\ \xrightarrow{\cdot2}\ 3(1-3y)-8y=20"),
       D(R([r"3-9y-8y=20", r"-17y=17", r"y=-1"]) + r"\qquad x=\frac{1-3\cdot(-1)}{2}=\frac{4}{2}=2"),
       P(r"Solució: \(x=2,\ y=-1\). Funciona, però apareixen fraccions: en aquests casos solen ser més còmodes la igualació o la reducció.", r"Solución: \(x=2,\ y=-1\). Funciona, pero aparecen fracciones: en estos casos suelen ser más cómodas la igualación o la reducción.", r"Solution: \(x=2,\ y=-1\). It works, but fractions appear: in cases like this, equalisation or elimination is usually easier."))])
cs('x=2y', 'x+y=9', (6, 3)); cs('x+y=8', 'x-y=2', (5, 3)); cs('3x+y=11', '5x-2y=0', (2, 5)); same('5x-2(11-3x)=0', '11x=22'); cs('2x+3y=1', '3x-4y=10', (2, -1)); same('3(1-3y)-8y=20', '-17y=17')
s3 += practice([
  ('★', L(r"a) \(" + SY('y=x+3', '2x+y=9') + r"\) b) \(" + SY('x-2y=1', '3x+y=10') + r"\)", r"a) \(" + SY('y=x+3', '2x+y=9') + r"\) b) \(" + SY('x-2y=1', '3x+y=10') + r"\)", r"a) \(" + SY('y=x+3', '2x+y=9') + r"\) b) \(" + SY('x-2y=1', '3x+y=10') + r"\)")),
  ('★★', L(r"c) \(" + SY('4x-y=5', '3x+2y=12') + r"\)", r"c) \(" + SY('4x-y=5', '3x+2y=12') + r"\)", r"c) \(" + SY('4x-y=5', '3x+2y=12') + r"\)")),
  ('★★★', L(r"d) \(" + SY('2x+5y=-1', '3x-2y=8') + r"\)", r"d) \(" + SY('2x+5y=-1', '3x-2y=8') + r"\)", r"d) \(" + SY('2x+5y=-1', '3x-2y=8') + r"\)"))],
  D(r"\text{a)}\ 2x+x+3=9\Rightarrow x=2,\ y=5\qquad \text{b)}\ x=1+2y\Rightarrow 3+6y+y=10\Rightarrow y=1,\ x=3")
  + D(r"\text{c)}\ y=4x-5\Rightarrow 3x+8x-10=12\Rightarrow x=2,\ y=3")
  + D(r"\text{d)}\ x=\frac{-1-5y}{2}\Rightarrow 3(-1-5y)-4y=16\Rightarrow -19y=19\Rightarrow y=-1,\ x=2"))
cs('y=x+3', '2x+y=9', (2, 5)); cs('x-2y=1', '3x+y=10', (3, 1)); cs('4x-y=5', '3x+2y=12', (2, 3)); cs('2x+5y=-1', '3x-2y=8', (2, -1)); same('3(-1-5y)-4y=16', '-19y=19')

# =====================================================================
# 6.4 Mètode d'igualació
# =====================================================================
s4 = box('prop', L("Mètode d'igualació", 'Método de igualación', 'Equalisation method'),
  ol(L(r"<strong>Aïllem la mateixa incògnita</strong> en les dues equacions.", r"<strong>Despejamos la misma incógnita</strong> en las dos ecuaciones.", r"<strong>Isolate the same unknown</strong> in both equations."),
     L(r"<strong>Igualem</strong> les dues expressions: si les dues són iguals a la mateixa incògnita, són iguals entre si.", r"<strong>Igualamos</strong> las dos expresiones: si las dos son iguales a la misma incógnita, son iguales entre sí.", r"<strong>Set</strong> the two expressions <strong>equal</strong>: both equal the same unknown, so they equal each other."),
     L(r"<strong>Resolem</strong> l'equació que en resulta, amb una sola incògnita.", r"<strong>Resolvemos</strong> la ecuación resultante, con una sola incógnita.", r"<strong>Solve</strong> the resulting equation in one unknown."),
     L(r"<strong>Substituïm</strong> el valor en qualsevol de les dues expressions aïllades.", r"<strong>Sustituimos</strong> el valor en cualquiera de las dos expresiones despejadas.", r"<strong>Substitute</strong> the value into either isolated expression."),
     L(r"<strong>Comprovem</strong> la solució.", r"<strong>Comprobamos</strong> la solución.", r"<strong>Check</strong> the solution."))
  + D(SY('x+y=5', 'x-2y=-1') + r"\qquad\Rightarrow\qquad " + SY('x=5-y', 'x=-1+2y'))
  + D(R([r"5-y=-1+2y", r"-y-2y=-1-5", r"-3y=-6", r"y=2"]) + r"\qquad x=5-2=3")
  + P(r"Comprovació: \(3+2=5\) ✓ i \(3-4=-1\) ✓. Solució: \(x=3,\ y=2\).", r"Comprobación: \(3+2=5\) ✓ y \(3-4=-1\) ✓. Solución: \(x=3,\ y=2\).", r"Check: \(3+2=5\) ✓ and \(3-4=-1\) ✓. Solution: \(x=3,\ y=2\).")
  + note(r"La igualació és molt còmoda quan la mateixa incògnita ja està aïllada en les dues equacions, com en \(y=2x-1,\ y=x+3\).", r"La igualación es muy cómoda cuando la misma incógnita ya está despejada en las dos ecuaciones, como en \(y=2x-1,\ y=x+3\).", r"Equalisation is very handy when the same unknown is already isolated in both equations, as in \(y=2x-1,\ y=x+3\)."))
cs('x+y=5', 'x-2y=-1', (3, 2))
s4 += box('prop', L('I si apareixen denominadors?', '¿Y si aparecen denominadores?', 'What if fractions appear?'),
  P(r"En aïllar pot aparéixer una fracció. Quan igualem, la traiem multiplicant els dos membres pel denominador:", r"Al despejar puede aparecer una fracción. Cuando igualamos, la quitamos multiplicando los dos miembros por el denominador:", r"Isolating may produce a fraction. When we equate, clear it by multiplying both sides by the denominator:")
  + D(SY('2x-y=3', '3x+2y=8') + r"\qquad\Rightarrow\qquad " + SY('y=2x-3', r'y=\frac{8-3x}{2}'))
  + D(R([r"2x-3=\frac{8-3x}{2}", r"2(2x-3)=8-3x", r"4x-6=8-3x", r"7x=14", r"x=2"]) + r"\qquad y=2\cdot2-3=1"))
cs('2x-y=3', '3x+2y=8', (2, 1)); same('2(2x-3)=8-3x', '7x=14')
s4 += solver('w-igu', 'igu', L('Igualació pas a pas', 'Igualación paso a paso', 'Equalisation step by step'), 'x+y=5', 'x-2y=-1',
             [('x+y=5', 'x-2y=-1'), ('y=2x-1', 'y=x+3'), ('x=2y+1', 'x=7-y'), ('2x-y=3', '3x+2y=8'), ('3x-2y=4', '5x+4y=14'), ('y=2x+1', '4x-2y=3')])
s4 += drill('igu', "Entrena: mètode d'igualació", 'Entrena: método de igualación', 'Train: equalisation method')
s4 += levels(
 [prob(L(r"Resol \(" + SY('y=2x-1', 'y=x+3') + r"\).", r"Resuelve \(" + SY('y=2x-1', 'y=x+3') + r"\).", r"Solve \(" + SY('y=2x-1', 'y=x+3') + r"\)."),
       D(R([r"2x-1=x+3", r"2x-x=3+1", r"x=4"]) + r"\qquad y=4+3=7\qquad " + BX(4, 7)))],
 [prob(L(r"Resol \(" + SY('x+3y=7', 'x-y=-1') + r"\).", r"Resuelve \(" + SY('x+3y=7', 'x-y=-1') + r"\).", r"Solve \(" + SY('x+3y=7', 'x-y=-1') + r"\)."),
       D(r"x=7-3y,\qquad x=-1+y"),
       D(R([r"7-3y=-1+y", r"-4y=-8", r"y=2"]) + r"\qquad x=-1+2=1\qquad " + BX(1, 2)))],
 [prob(L(r"Resol \(" + SY('3x-2y=4', '5x+4y=14') + r"\).", r"Resuelve \(" + SY('3x-2y=4', '5x+4y=14') + r"\).", r"Solve \(" + SY('3x-2y=4', '5x+4y=14') + r"\)."),
       P(r"Cap coeficient és 1. Aïllem la \(x\) de les dues:", r"Ningún coeficiente es 1. Despejamos la \(x\) de las dos:", r"No coefficient is 1. Isolate \(x\) in both:"),
       D(r"x=\frac{4+2y}{3},\qquad x=\frac{14-4y}{5}\qquad\Rightarrow\qquad \frac{4+2y}{3}=\frac{14-4y}{5}"),
       P(r"Multipliquem en creu (és com multiplicar pel m.c.m., 15):", r"Multiplicamos en cruz (es como multiplicar por el m.c.m., 15):", r"Cross-multiply (the same as multiplying by the LCM, 15):"),
       D(R([r"5(4+2y)=3(14-4y)", r"20+10y=42-12y", r"22y=22", r"y=1"]) + r"\qquad x=\frac{4+2}{3}=2\qquad " + BX(2, 1)))])
cs('y=2x-1', 'y=x+3', (4, 7)); cs('x+3y=7', 'x-y=-1', (1, 2)); cs('3x-2y=4', '5x+4y=14', (2, 1)); same('5(4+2y)=3(14-4y)', '22y=22')
s4 += practice([
  ('★', L(r"a) \(" + SY('y=3x', 'y=x+4') + r"\) b) \(" + SY('x=2y+1', 'x=7-y') + r"\)", r"a) \(" + SY('y=3x', 'y=x+4') + r"\) b) \(" + SY('x=2y+1', 'x=7-y') + r"\)", r"a) \(" + SY('y=3x', 'y=x+4') + r"\) b) \(" + SY('x=2y+1', 'x=7-y') + r"\)")),
  ('★★', L(r"c) \(" + SY('2x+y=1', '3x+y=3') + r"\)", r"c) \(" + SY('2x+y=1', '3x+y=3') + r"\)", r"c) \(" + SY('2x+y=1', '3x+y=3') + r"\)")),
  ('★★★', L(r"d) \(" + SY('4x-3y=2', '2x+5y=14') + r"\)", r"d) \(" + SY('4x-3y=2', '2x+5y=14') + r"\)", r"d) \(" + SY('4x-3y=2', '2x+5y=14') + r"\)"))],
  D(r"\text{a)}\ 3x=x+4\Rightarrow x=2,\ y=6\qquad \text{b)}\ 2y+1=7-y\Rightarrow y=2,\ x=5")
  + D(r"\text{c)}\ 1-2x=3-3x\Rightarrow x=2,\ y=-3")
  + D(r"\text{d)}\ \frac{2+3y}{4}=\frac{14-5y}{2}\Rightarrow 2+3y=2(14-5y)\Rightarrow 13y=26\Rightarrow y=2,\ x=2"))
cs('y=3x', 'y=x+4', (2, 6)); cs('x=2y+1', 'x=7-y', (5, 2)); cs('2x+y=1', '3x+y=3', (2, -3)); cs('4x-3y=2', '2x+5y=14', (2, 2)); same('2+3y=2(14-5y)', '13y=26')

# =====================================================================
# 6.5 Mètode de reducció
# =====================================================================
s5 = box('prop', L('Mètode de reducció', 'Método de reducción', 'Elimination method'),
  ol(L(r"<strong>Multipliquem</strong> una equació (o les dues) per nombres adequats perquè els coeficients d'una incògnita queden <strong>oposats</strong> (com \(6x\) i \(-6x\)).", r"<strong>Multiplicamos</strong> una ecuación (o las dos) por números adecuados para que los coeficientes de una incógnita queden <strong>opuestos</strong> (como \(6x\) y \(-6x\)).", r"<strong>Multiply</strong> one equation (or both) by suitable numbers so the coefficients of one unknown become <strong>opposites</strong> (like \(6x\) and \(-6x\))."),
     L(r"<strong>Sumem</strong> les dues equacions membre a membre: aquesta incògnita s'elimina.", r"<strong>Sumamos</strong> las dos ecuaciones miembro a miembro: esa incógnita se elimina.", r"<strong>Add</strong> the two equations side by side: that unknown disappears."),
     L(r"<strong>Resolem</strong> l'equació que queda.", r"<strong>Resolvemos</strong> la ecuación que queda.", r"<strong>Solve</strong> the equation that's left."),
     L(r"<strong>Substituïm</strong> el valor en una de les equacions inicials per a trobar l'altra incògnita, i <strong>comprovem</strong>.", r"<strong>Sustituimos</strong> el valor en una de las ecuaciones iniciales para hallar la otra incógnita, y <strong>comprobamos</strong>.", r"<strong>Substitute</strong> the value into one of the original equations to find the other unknown, and <strong>check</strong>."))
  + P(r"Si els coeficients ja són oposats, sumem directament:", r"Si los coeficientes ya son opuestos, sumamos directamente:", r"If the coefficients are already opposite, just add:")
  + D(r"\begin{array}{rrcr}3x&+2y&=&8\\5x&-2y&=&8\\\hline 8x&&=&16\end{array}\qquad\Rightarrow\qquad x=2,\qquad 3\cdot2+2y=8\ \Rightarrow\ 2y=2\ \Rightarrow\ y=1")
  + P(r"Si no, multipliquem. Per a eliminar la \(x\) en \(2x+3y=12,\ 3x-4y=1\), el m.c.m. de 2 i 3 és 6: multipliquem la primera per \(3\) i la segona per \(-2\).", r"Si no, multiplicamos. Para eliminar la \(x\) en \(2x+3y=12,\ 3x-4y=1\), el m.c.m. de 2 y 3 es 6: multiplicamos la primera por \(3\) y la segunda por \(-2\).", r"Otherwise, multiply. To eliminate \(x\) in \(2x+3y=12,\ 3x-4y=1\), the LCM of 2 and 3 is 6: multiply the first by \(3\) and the second by \(-2\).")
  + D(r"\begin{array}{lrrcr}\scriptstyle(\cdot3)&6x&+9y&=&36\\\scriptstyle(\cdot(-2))&-6x&+8y&=&-2\\\hline &&17y&=&34\end{array}\qquad\Rightarrow\qquad y=2,\qquad 2x+3\cdot2=12\ \Rightarrow\ x=3")
  + note(r"Quan multipliquem una equació per un nombre, el multipliquem per <strong>tots</strong> els termes, també pel del segon membre. Compte amb els signes en multiplicar per un nombre negatiu.",
         r"Cuando multiplicamos una ecuación por un número, lo multiplicamos por <strong>todos</strong> los términos, también por el del segundo miembro. Cuidado con los signos al multiplicar por un número negativo.",
         r"When you multiply an equation by a number, multiply <strong>every</strong> term, including the one on the right. Watch the signs when multiplying by a negative number.", '⚠')
  + note(r"La reducció és molt pràctica quan els coeficients d'una incògnita són iguals, oposats o múltiples, i en general quan no hi ha cap coeficient 1: així evitem les fraccions.",
         r"La reducción es muy práctica cuando los coeficientes de una incógnita son iguales, opuestos o múltiplos, y en general cuando no hay ningún coeficiente 1: así evitamos las fracciones.",
         r"Elimination is very handy when the coefficients of one unknown are equal, opposite or multiples, and in general when no coefficient is 1: it avoids fractions."))
cs('3x+2y=8', '5x-2y=8', (2, 1)); cs('2x+3y=12', '3x-4y=1', (3, 2)); same('3(2x+3y)-2(3x-4y)=36-2', '17y=34')
s5 += solver('w-red', 'red', L('Reducció pas a pas', 'Reducción paso a paso', 'Elimination step by step'), '2x+3y=12', '3x-4y=1',
             [('3x+2y=8', '5x-2y=8'), ('2x+3y=12', '3x-4y=1'), ('x+y=10', 'x-y=4'), ('2x+5y=1', '4x+3y=-5'), ('5x+3y=1', '2x-7y=25'), ('x+2y=3', '2x+4y=6')])
s5 += drill('red', 'Entrena: mètode de reducció', 'Entrena: método de reducción', 'Train: elimination method')
s5 += levels(
 [prob(L(r"Resol \(" + SY('x+y=10', 'x-y=4') + r"\).", r"Resuelve \(" + SY('x+y=10', 'x-y=4') + r"\).", r"Solve \(" + SY('x+y=10', 'x-y=4') + r"\)."),
       P(r"Els coeficients de la \(y\) ja són oposats. Sumem:", r"Los coeficientes de la \(y\) ya son opuestos. Sumamos:", r"The \(y\) coefficients are already opposite. Add:"),
       D(r"2x=14\ \Rightarrow\ x=7\qquad 7+y=10\ \Rightarrow\ y=3\qquad " + BX(7, 3)))],
 [prob(L(r"Resol \(" + SY('2x+5y=1', '4x+3y=-5') + r"\).", r"Resuelve \(" + SY('2x+5y=1', '4x+3y=-5') + r"\).", r"Solve \(" + SY('2x+5y=1', '4x+3y=-5') + r"\)."),
       P(r"Multipliquem la primera per \(-2\) per a eliminar la \(x\):", r"Multiplicamos la primera por \(-2\) para eliminar la \(x\):", r"Multiply the first by \(-2\) to eliminate \(x\):"),
       D(r"\begin{array}{rrcr}-4x&-10y&=&-2\\4x&+3y&=&-5\\\hline &-7y&=&-7\end{array}\qquad\Rightarrow\qquad y=1"),
       D(r"2x+5\cdot1=1\ \Rightarrow\ 2x=-4\ \Rightarrow\ x=-2\qquad " + BX(-2, 1)))],
 [prob(L(r"Resol \(" + SY('5x+3y=1', '2x-7y=25') + r"\).", r"Resuelve \(" + SY('5x+3y=1', '2x-7y=25') + r"\).", r"Solve \(" + SY('5x+3y=1', '2x-7y=25') + r"\)."),
       P(r"Eliminem la \(x\): m.c.m.(5, 2) = 10. Multipliquem la primera per \(2\) i la segona per \(-5\):", r"Eliminamos la \(x\): m.c.m.(5, 2) = 10. Multiplicamos la primera por \(2\) y la segunda por \(-5\):", r"Eliminate \(x\): LCM(5, 2) = 10. Multiply the first by \(2\) and the second by \(-5\):"),
       D(r"\begin{array}{rrcr}10x&+6y&=&2\\-10x&+35y&=&-125\\\hline &41y&=&-123\end{array}\qquad\Rightarrow\qquad y=-3"),
       D(r"5x+3\cdot(-3)=1\ \Rightarrow\ 5x=10\ \Rightarrow\ x=2\qquad " + BX(2, -3)))])
cs('x+y=10', 'x-y=4', (7, 3)); cs('2x+5y=1', '4x+3y=-5', (-2, 1)); same('-2*(2x+5y)+(4x+3y)=-2-5', '-7y=-7'); cs('5x+3y=1', '2x-7y=25', (2, -3)); same('2(5x+3y)-5(2x-7y)=2-125', '41y=-123')
s5 += practice([
  ('★', L(r"a) \(" + SY('2x+y=9', '3x-y=11') + r"\) b) \(" + SY('x+3y=5', '2x+y=5') + r"\)", r"a) \(" + SY('2x+y=9', '3x-y=11') + r"\) b) \(" + SY('x+3y=5', '2x+y=5') + r"\)", r"a) \(" + SY('2x+y=9', '3x-y=11') + r"\) b) \(" + SY('x+3y=5', '2x+y=5') + r"\)")),
  ('★★', L(r"c) \(" + SY('3x+4y=2', '2x-3y=7') + r"\)", r"c) \(" + SY('3x+4y=2', '2x-3y=7') + r"\)", r"c) \(" + SY('3x+4y=2', '2x-3y=7') + r"\)")),
  ('★★★', L(r"d) \(" + SY('7x+2y=3', '5x+3y=-1') + r"\)", r"d) \(" + SY('7x+2y=3', '5x+3y=-1') + r"\)", r"d) \(" + SY('7x+2y=3', '5x+3y=-1') + r"\)"))],
  D(r"\text{a)}\ 5x=20\Rightarrow x=4,\ y=1\qquad \text{b)}\ (\cdot(-2))\ -5y=-5\Rightarrow y=1,\ x=2")
  + D(r"\text{c)}\ (\cdot2),\ (\cdot(-3)):\ 17y=-17\Rightarrow y=-1,\ x=2")
  + D(r"\text{d)}\ (\cdot3),\ (\cdot(-2)):\ 11x=11\Rightarrow x=1,\ y=-2"))
cs('2x+y=9', '3x-y=11', (4, 1)); cs('x+3y=5', '2x+y=5', (2, 1)); cs('3x+4y=2', '2x-3y=7', (2, -1)); same('2(3x+4y)-3(2x-3y)=4-21', '17y=-17'); cs('7x+2y=3', '5x+3y=-1', (1, -2)); same('3(7x+2y)-2(5x+3y)=9+2', '11x=11')

# =====================================================================
# 6.6 Mètode gràfic
# =====================================================================
s6 = box('prop', L('Mètode gràfic', 'Método gráfico', 'Graphical method'),
  ol(L(r"Fem una <strong>taula de valors</strong> per a cada equació (dos o tres punts).", r"Hacemos una <strong>tabla de valores</strong> para cada ecuación (dos o tres puntos).", r"Make a <strong>table of values</strong> for each equation (two or three points)."),
     L(r"Representem les <strong>dues rectes</strong> en els mateixos eixos.", r"Representamos las <strong>dos rectas</strong> en los mismos ejes.", r"Draw the <strong>two lines</strong> on the same axes."),
     L(r"El <strong>punt de tall</strong> de les rectes és la solució del sistema. La comprovem en les dues equacions.", r"El <strong>punto de corte</strong> de las rectas es la solución del sistema. La comprobamos en las dos ecuaciones.", r"The <strong>crossing point</strong> of the lines is the solution. Check it in both equations."))
  + D(SY('x+y=5', '2x-y=1') + r"\qquad\Rightarrow\qquad " + SY('y=5-x', 'y=2x-1'))
  + '<div class="tv2">' + tvc('x+y=5', [0, 1, 5], 't0') + tvc('2x-y=1', [0, 1, 2], 't1') + '</div>'
  + figs(svg_graph([(1, 1, 5), (2, -1, 1)], [(0, 5, 'pt p0', None), (1, 4, 'pt p0', None), (5, 0, 'pt p0', None), (0, -1, 'pt p1', None), (1, 1, 'pt p1', None), (2, 3, 'cut', '(2, 3)')], R=6))
  + P(r"Les rectes es tallen en \((2,\,3)\). Comprovació: \(2+3=5\) ✓ i \(4-3=1\) ✓. Solució: \(x=2,\ y=3\).", r"Las rectas se cortan en \((2,\,3)\). Comprobación: \(2+3=5\) ✓ y \(4-3=1\) ✓. Solución: \(x=2,\ y=3\).", r"The lines cross at \((2,\,3)\). Check: \(2+3=5\) ✓ and \(4-3=1\) ✓. Solution: \(x=2,\ y=3\).")
  + note(r"El mètode gràfic ajuda a <strong>entendre</strong> què és la solució, però només és exacte si el punt de tall té coordenades fàcils de llegir. Si la solució és, per exemple, \(x=\frac{7}{3}\), el dibuix només en dona una aproximació: aleshores cal un mètode algebraic.",
         r"El método gráfico ayuda a <strong>entender</strong> qué es la solución, pero solo es exacto si el punto de corte tiene coordenadas fáciles de leer. Si la solución es, por ejemplo, \(x=\frac{7}{3}\), el dibujo solo da una aproximación: entonces hace falta un método algebraico.",
         r"The graphical method helps you <strong>understand</strong> what the solution is, but it's only exact when the crossing point is easy to read. If the solution is, say, \(x=\frac{7}{3}\), the drawing only gives an approximation: then you need an algebraic method.", '⚠'))
cs('x+y=5', '2x-y=1', (2, 3))
s6 += grafw('w-graf', 'x+y=5', '2x-y=1', [('x+y=5', '2x-y=1'), ('x-y=1', 'x+y=7'), ('2x+y=1', 'x-y=5'), ('y=2x-3', '3x+2y=8'), ('x+y=3', 'x-y=0'), ('y=x+2', 'y=-2x-4')])
s6 += drill('gra', 'Entrena: llig la solució en la gràfica', 'Entrena: lee la solución en la gráfica', 'Train: read the solution from the graph')
s6 += levels(
 [prob(L(r"Resol gràficament \(" + SY('x-y=1', 'x+y=7') + r"\).", r"Resuelve gráficamente \(" + SY('x-y=1', 'x+y=7') + r"\).", r"Solve graphically \(" + SY('x-y=1', 'x+y=7') + r"\)."),
       '<div class="tv2">' + tvc('x-y=1', [0, 1, 4], 't0') + tvc('x+y=7', [0, 3, 7], 't1') + '</div>',
       figs(svg_graph([(1, -1, 1), (1, 1, 7)], [(4, 3, 'cut', '(4, 3)')], R=8)),
       P(r"Les rectes es tallen en \((4,\,3)\): \(x=4,\ y=3\). Comprovació: \(4-3=1\) ✓, \(4+3=7\) ✓.", r"Las rectas se cortan en \((4,\,3)\): \(x=4,\ y=3\). Comprobación: \(4-3=1\) ✓, \(4+3=7\) ✓.", r"The lines cross at \((4,\,3)\): \(x=4,\ y=3\). Check: \(4-3=1\) ✓, \(4+3=7\) ✓."))],
 [prob(L(r"Resol gràficament \(" + SY('2x+y=1', 'x-y=5') + r"\).", r"Resuelve gráficamente \(" + SY('2x+y=1', 'x-y=5') + r"\).", r"Solve graphically \(" + SY('2x+y=1', 'x-y=5') + r"\)."),
       '<div class="tv2">' + tvc('2x+y=1', [-1, 0, 2], 't0') + tvc('x-y=5', [0, 2, 5], 't1') + '</div>',
       figs(svg_graph([(2, 1, 1), (1, -1, 5)], [(2, -3, 'cut', '(2, −3)')], R=6)),
       P(r"Punt de tall: \((2,\,-3)\). Comprovació: \(4-3=1\) ✓, \(2+3=5\) ✓.", r"Punto de corte: \((2,\,-3)\). Comprobación: \(4-3=1\) ✓, \(2+3=5\) ✓.", r"Crossing point: \((2,\,-3)\). Check: \(4-3=1\) ✓, \(2+3=5\) ✓."))],
 [prob(L(r"Representa \(" + SY('x+y=3', 'x-y=0') + r"\). Pots llegir la solució exacta en el dibuix? Calcula-la per reducció.", r"Representa \(" + SY('x+y=3', 'x-y=0') + r"\). ¿Puedes leer la solución exacta en el dibujo? Calcúlala por reducción.", r"Draw \(" + SY('x+y=3', 'x-y=0') + r"\). Can you read the exact solution from the drawing? Find it by elimination."),
       figs(svg_graph([(1, 1, 3), (1, -1, 0)], [(1.5, 1.5, 'cut', None)], R=5)),
       P(r"Les rectes es tallen entre 1 i 2 en els dos eixos: el dibuix només dona una aproximació, \((1{,}5;\ 1{,}5)\) més o menys. Sumant les equacions:", r"Las rectas se cortan entre 1 y 2 en los dos ejes: el dibujo solo da una aproximación, \((1{,}5;\ 1{,}5)\) más o menos. Sumando las ecuaciones:", r"The lines cross between 1 and 2 on both axes: the drawing only gives an estimate, about \((1.5,\ 1.5)\). Adding the equations:"),
       D(r"2x=3\ \Rightarrow\ x=\frac32,\qquad y=x=\frac32"))])
cs('x-y=1', 'x+y=7', (4, 3)); cs('2x+y=1', 'x-y=5', (2, -3)); cs('x+y=3', 'x-y=0', ('3/2', '3/2'))
s6 += practice([
  ('★', L(r"Resol gràficament: a) \(" + SY('x+y=4', 'x-y=2') + r"\) b) \(" + SY('y=2x', 'x+y=6') + r"\)", r"Resuelve gráficamente: a) \(" + SY('x+y=4', 'x-y=2') + r"\) b) \(" + SY('y=2x', 'x+y=6') + r"\)", r"Solve graphically: a) \(" + SY('x+y=4', 'x-y=2') + r"\) b) \(" + SY('y=2x', 'x+y=6') + r"\)")),
  ('★★', L(r"c) \(" + SY('2x-y=4', 'x+2y=-3') + r"\)", r"c) \(" + SY('2x-y=4', 'x+2y=-3') + r"\)", r"c) \(" + SY('2x-y=4', 'x+2y=-3') + r"\)")),
  ('★★★', L(r"d) \(" + SY('3x+y=2', 'x-2y=10') + r"\)", r"d) \(" + SY('3x+y=2', 'x-2y=10') + r"\)", r"d) \(" + SY('3x+y=2', 'x-2y=10') + r"\)"))],
  P(r"a) \((3,\,1)\); b) \((2,\,4)\); c) \((1,\,-2)\); d) \((2,\,-4)\). Pots comprovar-ho amb el giny d'aquest apartat.", r"a) \((3,\,1)\); b) \((2,\,4)\); c) \((1,\,-2)\); d) \((2,\,-4)\). Puedes comprobarlo con la herramienta de este apartado.", r"a) \((3,\,1)\); b) \((2,\,4)\); c) \((1,\,-2)\); d) \((2,\,-4)\). You can check them with this section's tool."))
cs('x+y=4', 'x-y=2', (3, 1)); cs('y=2x', 'x+y=6', (2, 4)); cs('2x-y=4', 'x+2y=-3', (1, -2)); cs('3x+y=2', 'x-2y=10', (2, -4))

# =====================================================================
# 6.7 Classificació dels sistemes
# =====================================================================
s7 = box('def', L('Tipus de sistemes segons el nombre de solucions', 'Tipos de sistemas según el número de soluciones', 'Types of system by number of solutions'),
  P(r"Dues rectes en el pla només poden estar en tres posicions. Per això un sistema de dues equacions lineals pot tindre <strong>una solució</strong>, <strong>infinites</strong> o <strong>cap</strong>:",
    r"Dos rectas en el plano solo pueden estar en tres posiciones. Por eso un sistema de dos ecuaciones lineales puede tener <strong>una solución</strong>, <strong>infinitas</strong> o <strong>ninguna</strong>:",
    r"Two lines in the plane can only be in three positions. So a system of two linear equations has <strong>one solution</strong>, <strong>infinitely many</strong> or <strong>none</strong>:")
  + figs(svg_graph([(1, 1, 3), (1, -1, -1)], [(1, 2, 'cut', None)], R=4, cap=L('Secants: una solució', 'Secantes: una solución', 'Intersecting: one solution')),
         svg_graph([(1, 2, 2, 0), (2, 4, 4, 1, True)], [], R=4, cap=L('Coincidents: infinites', 'Coincidentes: infinitas', 'Coincident: infinitely many')),
         svg_graph([(1, -1, -2), (1, -1, 2)], [], R=4, cap=L('Paral·leles: cap solució', 'Paralelas: ninguna solución', 'Parallel: no solution')))
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Sistema', 'Sistema', 'System') + '</th><th>' + L('Solucions', 'Soluciones', 'Solutions') + '</th><th>' + L('Rectes', 'Rectas', 'Lines') + '</th><th>' + L('Exemple', 'Ejemplo', 'Example') + '</th></tr></thead><tbody>'
  + f'<tr><td class="l"><strong>{L("Compatible determinat (SCD)", "Compatible determinado (SCD)", "Consistent, independent")}</strong></td><td>{L("Una", "Una", "One")}</td><td>{L("Secants", "Secantes", "Intersecting")}</td><td>\\({SY("x+y=3", "x-y=-1")}\\)</td></tr>'
  + f'<tr><td class="l"><strong>{L("Compatible indeterminat (SCI)", "Compatible indeterminado (SCI)", "Consistent, dependent")}</strong></td><td>{L("Infinites", "Infinitas", "Infinitely many")}</td><td>{L("Coincidents", "Coincidentes", "Coincident")}</td><td>\\({SY("x+2y=2", "2x+4y=4")}\\)</td></tr>'
  + f'<tr><td class="l"><strong>{L("Incompatible (SI)", "Incompatible (SI)", "Inconsistent")}</strong></td><td>{L("Cap", "Ninguna", "None")}</td><td>{L("Paral·leles", "Paralelas", "Parallel")}</td><td>\\({SY("x-y=-2", "x-y=2")}\\)</td></tr>'
  + '</tbody></table></div>')
cs('x+y=3', 'x-y=-1', (1, 2)); cs('x+2y=2', '2x+4y=4', 'SCI'); cs('x-y=-2', 'x-y=2', 'SI')
s7 += box('prop', L('Com ho detectem en resoldre?', '¿Cómo lo detectamos al resolver?', 'How do we spot it while solving?'),
  P(r"Si en aplicar un mètode algebraic <strong>desapareixen les dues incògnites</strong>, el sistema no és compatible determinat:", r"Si al aplicar un método algebraico <strong>desaparecen las dos incógnitas</strong>, el sistema no es compatible determinado:", r"If <strong>both unknowns disappear</strong> while applying an algebraic method, the system doesn't have exactly one solution:")
  + ul(L(r"Si arribem a una igualtat <strong>certa</strong>, com \(0=0\) o \(0x=0\): <strong>compatible indeterminat</strong> (infinites solucions).", r"Si llegamos a una igualdad <strong>cierta</strong>, como \(0=0\) o \(0x=0\): <strong>compatible indeterminado</strong> (infinitas soluciones).", r"If you reach a <strong>true</strong> statement, like \(0=0\) or \(0x=0\): <strong>infinitely many solutions</strong>."),
       L(r"Si arribem a una igualtat <strong>impossible</strong>, com \(0=5\) o \(0x=-3\): <strong>incompatible</strong> (cap solució).", r"Si llegamos a una igualdad <strong>imposible</strong>, como \(0=5\) o \(0x=-3\): <strong>incompatible</strong> (ninguna solución).", r"If you reach an <strong>impossible</strong> statement, like \(0=5\) or \(0x=-3\): <strong>no solution</strong>."))
  + D(SY('x+2y=3', '2x+4y=6') + r"\ \xrightarrow{(\cdot(-2))\text{ i sumem}}\ 0=0\qquad\qquad " + SY('x+2y=3', '2x+4y=5') + r"\ \xrightarrow{(\cdot(-2))\text{ i sumem}}\ 0=-1").replace(r'\text{ i sumem}', Lt(' i sumem', ' y sumamos', ' and add'))
  + P(r"En el primer cas, les solucions són tots els punts de la recta \(x+2y=3\): \((3,\,0),\ (1,\,1),\ (-1,\,2)\ldots\) En el segon, no n'hi ha cap.", r"En el primer caso, las soluciones son todos los puntos de la recta \(x+2y=3\): \((3,\,0),\ (1,\,1),\ (-1,\,2)\ldots\) En el segundo, no hay ninguna.", r"In the first case, the solutions are all the points of the line \(x+2y=3\): \((3,\,0),\ (1,\,1),\ (-1,\,2)\ldots\) In the second, there are none."))
cs('x+2y=3', '2x+4y=6', 'SCI'); cs('x+2y=3', '2x+4y=5', 'SI'); ok('x+2y=3', 3, 0); ok('x+2y=3', 1, 1); ok('x+2y=3', -1, 2)
s7 += box('prop', L('Classificació sense resoldre: comparem els coeficients', 'Clasificación sin resolver: comparamos los coeficientes', 'Classifying without solving: compare the coefficients'),
  P(r"En el sistema \(" + SY("ax+by=c", "a'x+b'y=c'") + r"\) comparem els quocients dels coeficients:", r"En el sistema \(" + SY("ax+by=c", "a'x+b'y=c'") + r"\) comparamos los cocientes de los coeficientes:", r"In the system \(" + SY("ax+by=c", "a'x+b'y=c'") + r"\) compare the ratios of the coefficients:")
  + ul(L(r"\(\dfrac{a}{a'}\neq\dfrac{b}{b'}\)\(\ \Rightarrow\ \) <strong>compatible determinat</strong> (rectes secants).", r"\(\dfrac{a}{a'}\neq\dfrac{b}{b'}\)\(\ \Rightarrow\ \) <strong>compatible determinado</strong> (rectas secantes).", r"\(\dfrac{a}{a'}\neq\dfrac{b}{b'}\)\(\ \Rightarrow\ \) <strong>one solution</strong> (intersecting lines)."),
       L(r"\(\dfrac{a}{a'}=\dfrac{b}{b'}=\dfrac{c}{c'}\)\(\ \Rightarrow\ \) <strong>compatible indeterminat</strong>: una equació és l'altra multiplicada per un nombre (rectes coincidents).", r"\(\dfrac{a}{a'}=\dfrac{b}{b'}=\dfrac{c}{c'}\)\(\ \Rightarrow\ \) <strong>compatible indeterminado</strong>: una ecuación es la otra multiplicada por un número (rectas coincidentes).", r"\(\dfrac{a}{a'}=\dfrac{b}{b'}=\dfrac{c}{c'}\)\(\ \Rightarrow\ \) <strong>infinitely many</strong>: one equation is the other times a number (coincident lines)."),
       L(r"\(\dfrac{a}{a'}=\dfrac{b}{b'}\neq\dfrac{c}{c'}\)\(\ \Rightarrow\ \) <strong>incompatible</strong> (rectes paral·leles).", r"\(\dfrac{a}{a'}=\dfrac{b}{b'}\neq\dfrac{c}{c'}\)\(\ \Rightarrow\ \) <strong>incompatible</strong> (rectas paralelas).", r"\(\dfrac{a}{a'}=\dfrac{b}{b'}\neq\dfrac{c}{c'}\)\(\ \Rightarrow\ \) <strong>no solution</strong> (parallel lines)."))
  + D(r"\begin{cases}2x-y=3\\4x-2y=6\end{cases}:\ \ \frac24=\frac{-1}{-2}=\frac36\ \Rightarrow\ \text{SCI}\qquad\qquad \begin{cases}2x-y=3\\4x-2y=1\end{cases}:\ \ \frac24=\frac{-1}{-2}\neq\frac31\ \Rightarrow\ \text{SI}")
  + grafw('w-graf2', 'x+2y=2', '2x+4y=4', [('x+y=3', 'x-y=-1'), ('x+2y=2', '2x+4y=4'), ('x-y=-2', 'x-y=2'), ('2x-y=3', '4x-2y=6'), ('2x-y=3', '4x-2y=1'), ('3x+y=2', '6x+2y=1')], ratio=True)
  + drill('cls', 'Entrena: classifica el sistema', 'Entrena: clasifica el sistema', 'Train: classify the system', opts=True))
cs('2x-y=3', '4x-2y=6', 'SCI'); cs('2x-y=3', '4x-2y=1', 'SI'); cs('3x+y=2', '6x+2y=1', 'SI')
s7 += levels(
 [prob(L(r"Classifica sense resoldre: a) \(" + SY('2x-y=3', '4x-2y=6') + r"\) b) \(" + SY('x+y=2', 'x+y=5') + r"\) c) \(" + SY('x+y=4', 'x-y=2') + r"\)", r"Clasifica sin resolver: a) \(" + SY('2x-y=3', '4x-2y=6') + r"\) b) \(" + SY('x+y=2', 'x+y=5') + r"\) c) \(" + SY('x+y=4', 'x-y=2') + r"\)", r"Classify without solving: a) \(" + SY('2x-y=3', '4x-2y=6') + r"\) b) \(" + SY('x+y=2', 'x+y=5') + r"\) c) \(" + SY('x+y=4', 'x-y=2') + r"\)"),
       D(r"\text{a)}\ \frac24=\frac{-1}{-2}=\frac36:\ \text{SCI}\qquad \text{b)}\ \frac11=\frac11\neq\frac25:\ \text{SI}\qquad \text{c)}\ \frac11\neq\frac{1}{-1}:\ \text{SCD}"),
       P(r"En a) la segona equació és la primera multiplicada per 2; en b) \(x+y\) no pot valdre alhora 2 i 5.", r"En a) la segunda ecuación es la primera multiplicada por 2; en b) \(x+y\) no puede valer a la vez 2 y 5.", r"In a) the second equation is the first times 2; in b) \(x+y\) can't be 2 and 5 at once."))],
 [prob(L(r"Resol i classifica \(" + SY('3x-6y=9', '-x+2y=-3') + r"\).", r"Resuelve y clasifica \(" + SY('3x-6y=9', '-x+2y=-3') + r"\).", r"Solve and classify \(" + SY('3x-6y=9', '-x+2y=-3') + r"\)."),
       P(r"Multipliquem la segona per 3 i sumem:", r"Multiplicamos la segunda por 3 y sumamos:", r"Multiply the second by 3 and add:"),
       D(r"\begin{array}{rrcr}3x&-6y&=&9\\-3x&+6y&=&-9\\\hline &0&=&0\end{array}"),
       P(r"És <strong>compatible indeterminat</strong>: totes les solucions de \(x-2y=3\), és a dir, \(x=3+2y\). Per exemple, \((3,\,0)\), \((5,\,1)\), \((1,\,-1)\).", r"Es <strong>compatible indeterminado</strong>: todas las soluciones de \(x-2y=3\), es decir, \(x=3+2y\). Por ejemplo, \((3,\,0)\), \((5,\,1)\), \((1,\,-1)\).", r"It has <strong>infinitely many solutions</strong>: all the solutions of \(x-2y=3\), that is, \(x=3+2y\). For example, \((3,\,0)\), \((5,\,1)\), \((1,\,-1)\)."))],
 [prob(L(r"Per a quin valor de \(k\) el sistema \(" + SY('2x+ky=5', 'x+3y=2') + r"\) és incompatible? Com és per als altres valors?", r"¿Para qué valor de \(k\) el sistema \(" + SY('2x+ky=5', 'x+3y=2') + r"\) es incompatible? ¿Cómo es para los otros valores?", r"For which \(k\) is the system \(" + SY('2x+ky=5', 'x+3y=2') + r"\) inconsistent? What about other values?"),
       D(r"\frac21=\frac k3\ \Rightarrow\ k=6;\qquad \text{%s}\ \ \frac{c}{c'}=\frac52\neq2" % Lt('i a més', 'y además', 'and also')),
       P(r"Si \(k=6\) les rectes són paral·leles: <strong>incompatible</strong>. Si \(k\neq6\), els quocients de la \(x\) i la \(y\) són diferents: <strong>compatible determinat</strong>. Mai no pot ser indeterminat.", r"Si \(k=6\) las rectas son paralelas: <strong>incompatible</strong>. Si \(k\neq6\), los cocientes de la \(x\) y la \(y\) son distintos: <strong>compatible determinado</strong>. Nunca puede ser indeterminado.", r"If \(k=6\) the lines are parallel: <strong>no solution</strong>. If \(k\neq6\), the \(x\) and \(y\) ratios differ: <strong>one solution</strong>. It can never have infinitely many."))])
cs('x+y=2', 'x+y=5', 'SI'); cs('x+y=4', 'x-y=2', (3, 1)); cs('3x-6y=9', '-x+2y=-3', 'SCI'); ok('x-2y=3', 5, 1); ok('x-2y=3', 1, -1)
cs('2x+6y=5', 'x+3y=2', 'SI'); cs('2x+5y=5', 'x+3y=2', (5, -1))
s7 += practice([
  ('★', L(r"Classifica: a) \(" + SY('x-3y=2', '2x-6y=4') + r"\) b) \(" + SY('x+y=1', '2x+y=1') + r"\) c) \(" + SY('3x+y=4', '6x+2y=5') + r"\)", r"Clasifica: a) \(" + SY('x-3y=2', '2x-6y=4') + r"\) b) \(" + SY('x+y=1', '2x+y=1') + r"\) c) \(" + SY('3x+y=4', '6x+2y=5') + r"\)", r"Classify: a) \(" + SY('x-3y=2', '2x-6y=4') + r"\) b) \(" + SY('x+y=1', '2x+y=1') + r"\) c) \(" + SY('3x+y=4', '6x+2y=5') + r"\)")),
  ('★★', L(r"d) Escriu una equació que forme amb \(x+2y=4\) un sistema incompatible, una altra que en forme un d'indeterminat i una altra que en forme un de determinat.", r"d) Escribe una ecuación que forme con \(x+2y=4\) un sistema incompatible, otra que forme uno indeterminado y otra que forme uno determinado.", r"d) Write an equation that forms an inconsistent system with \(x+2y=4\), another forming a dependent one and another forming one with a single solution.")),
  ('★★★', L(r"e) Troba \(m\) perquè \(" + SY('mx+4y=6', '3x+2y=3') + r"\) tinga infinites solucions.", r"e) Halla \(m\) para que \(" + SY('mx+4y=6', '3x+2y=3') + r"\) tenga infinitas soluciones.", r"e) Find \(m\) so that \(" + SY('mx+4y=6', '3x+2y=3') + r"\) has infinitely many solutions."))],
  D(r"\text{a)}\ \text{SCI}\ \left(\tfrac12=\tfrac{-3}{-6}=\tfrac24\right)\qquad \text{b)}\ \text{SCD}\ (x=0,\ y=1)\qquad \text{c)}\ \text{SI}\ \left(\tfrac36=\tfrac12\neq\tfrac45\right)")
  + P(r"d) Per exemple: \(x+2y=7\) (SI), \(2x+4y=8\) (SCI) i \(x-y=1\) (SCD). e) \(\frac m3=\frac42=\frac63=2\Rightarrow m=6\).", r"d) Por ejemplo: \(x+2y=7\) (SI), \(2x+4y=8\) (SCI) y \(x-y=1\) (SCD). e) \(\frac m3=\frac42=\frac63=2\Rightarrow m=6\).", r"d) For example: \(x+2y=7\) (none), \(2x+4y=8\) (infinitely many) and \(x-y=1\) (one). e) \(\frac m3=\frac42=\frac63=2\Rightarrow m=6\)."))
cs('x-3y=2', '2x-6y=4', 'SCI'); cs('x+y=1', '2x+y=1', (0, 1)); cs('3x+y=4', '6x+2y=5', 'SI'); cs('x+2y=4', 'x+2y=7', 'SI'); cs('x+2y=4', '2x+4y=8', 'SCI'); cs('x+2y=4', 'x-y=1', (2, 1)); cs('6x+4y=6', '3x+2y=3', 'SCI')

# =====================================================================
# 6.8 Sistemes amb parèntesis i denominadors. Quin mètode triem?
# =====================================================================
s8 = box('prop', L('Primer, la forma reduïda', 'Primero, la forma reducida', 'First, standard form'),
  P(r"Si les equacions tenen parèntesis o denominadors, primer les transformem en equacions de la forma \(ax+by=c\), igual que fèiem amb les equacions de primer grau: traiem denominadors (multiplicant pel m.c.m.), traiem parèntesis, transposem i reduïm. Si tots els coeficients tenen un divisor comú, simplifiquem.",
    r"Si las ecuaciones tienen paréntesis o denominadores, primero las transformamos en ecuaciones de la forma \(ax+by=c\), igual que hacíamos con las ecuaciones de primer grado: quitamos denominadores (multiplicando por el m.c.m.), quitamos paréntesis, transponemos y reducimos. Si todos los coeficientes tienen un divisor común, simplificamos.",
    r"If the equations have brackets or fractions, first turn them into equations of the form \(ax+by=c\), just as with linear equations: clear fractions (multiply by the LCM), remove brackets, rearrange and simplify. If all the coefficients share a factor, divide it out.")
  + D(SY(r'2(x+1)-y=3(y-1)+5', r'\dfrac{x+2}{3}+\dfrac{y-1}{2}=\dfrac52'))
  + D(r"\text{1a: }2x+2-y=3y-3+5\ \Rightarrow\ 2x-4y=0\ \Rightarrow\ x-2y=0")
  + D(r"\text{2a: }\cdot6:\ 2(x+2)+3(y-1)=15\ \Rightarrow\ 2x+4+3y-3=15\ \Rightarrow\ 2x+3y=14")
  + D(SY('x-2y=0', '2x+3y=14') + r"\qquad x=2y\ \Rightarrow\ 4y+3y=14\ \Rightarrow\ y=2,\ \ x=4"))
same('2(x+1)-y=3(y-1)+5', '2x-4y=0'); same('6*((x+2)/3+(y-1)/2)=15', '2x+3y=14'); cs('2(x+1)-y=3(y-1)+5', '(x+2)/3+(y-1)/2=5/2', (4, 2))
s8 += box('prop', L('Quin mètode és el més adequat?', '¿Qué método es el más adecuado?', 'Which method is best?'),
  '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Mètode', 'Método', 'Method') + '</th><th>' + L('Quan convé', 'Cuándo conviene', 'When to use it') + '</th><th>' + L('Exemple', 'Ejemplo', 'Example') + '</th></tr></thead><tbody>'
  + f'<tr><td class="l"><strong>{L("Substitució", "Sustitución", "Substitution")}</strong></td><td class="l">{L("Una incògnita té coeficient 1 o −1, o ja està aïllada.", "Una incógnita tiene coeficiente 1 o −1, o ya está despejada.", "One unknown has coefficient 1 or −1, or is already isolated.")}</td><td>\\({SY("y=2x-3", "3x+2y=8")}\\)</td></tr>'
  + f'<tr><td class="l"><strong>{L("Igualació", "Igualación", "Equalisation")}</strong></td><td class="l">{L("La mateixa incògnita està aïllada (o és fàcil d’aïllar) en les dues.", "La misma incógnita está despejada (o es fácil de despejar) en las dos.", "The same unknown is isolated (or easy to isolate) in both.")}</td><td>\\({SY("x=2y+1", "x=7-y")}\\)</td></tr>'
  + f'<tr><td class="l"><strong>{L("Reducció", "Reducción", "Elimination")}</strong></td><td class="l">{L("Els coeficients d’una incògnita són iguals, oposats o múltiples; o no hi ha cap coeficient 1.", "Los coeficientes de una incógnita son iguales, opuestos o múltiplos; o no hay ningún coeficiente 1.", "One unknown has equal, opposite or multiple coefficients; or no coefficient is 1.")}</td><td>\\({SY("3x+2y=8", "5x-2y=8")}\\)</td></tr>'
  + f'<tr><td class="l"><strong>{L("Gràfic", "Gráfico", "Graphical")}</strong></td><td class="l">{L("Per a visualitzar el sistema i saber de quin tipus és. Només és exacte si la solució és entera.", "Para visualizar el sistema y saber de qué tipo es. Solo es exacto si la solución es entera.", "To visualise the system and its type. Only exact if the solution is a whole number.")}</td><td>\\({SY("x+y=5", "2x-y=1")}\\)</td></tr>'
  + '</tbody></table></div>'
  + note(r"Qualsevol mètode algebraic dona la mateixa solució: triar bé només fa que els càlculs siguen més curts. Tria'n un i, si vols, comprova la solució amb un altre.", r"Cualquier método algebraico da la misma solución: elegir bien solo hace que los cálculos sean más cortos. Elige uno y, si quieres, comprueba la solución con otro.", r"Any algebraic method gives the same solution: choosing well just makes the working shorter. Pick one and, if you like, check with another.")
  + solver('w-all', None, L('Resol qualsevol sistema', 'Resuelve cualquier sistema', 'Solve any system'), '2(x+1)-y=3(y-1)+5', '(x+2)/3+(y-1)/2=5/2',
           [('2(x+1)-y=3(y-1)+5', '(x+2)/3+(y-1)/2=5/2'), ('x/2+y/3=4', 'x/4-y/6=0'), ('3(x-1)+y=5', 'x+2(y-1)=4'), ('(x+1)/3-(y-2)/4=1', '2(x-y)=x-7'), ('0,5x+y=4', '0,3x-0,1y=0,3'), ('x+y=3', '2(x+y)=6')])
  + drill('mix', 'Entrena: sistemes amb parèntesis i denominadors', 'Entrena: sistemas con paréntesis y denominadores', 'Train: systems with brackets and fractions'))
cs('y=2x-3', '3x+2y=8', (2, 1)); cs('x=2y+1', 'x=7-y', (5, 2)); cs('x/2+y=4', '3x/10-y/10=3/10', (2, 3))
s8 += levels(
 [prob(L(r"Resol \(" + SY('3(x-1)+y=5', 'x+2(y-1)=4') + r"\).", r"Resuelve \(" + SY('3(x-1)+y=5', 'x+2(y-1)=4') + r"\).", r"Solve \(" + SY('3(x-1)+y=5', 'x+2(y-1)=4') + r"\)."),
       D(r"3x-3+y=5\ \Rightarrow\ 3x+y=8\qquad\quad x+2y-2=4\ \Rightarrow\ x+2y=6"),
       D(r"y=8-3x\ \Rightarrow\ x+2(8-3x)=6\ \Rightarrow\ -5x=-10\ \Rightarrow\ x=2,\quad y=8-6=2\qquad " + BX(2, 2)))],
 [prob(L(r"Resol \(" + SY(r'\dfrac x2+\dfrac y3=4', r'\dfrac x4-\dfrac y6=0') + r"\).", r"Resuelve \(" + SY(r'\dfrac x2+\dfrac y3=4', r'\dfrac x4-\dfrac y6=0') + r"\).", r"Solve \(" + SY(r'\dfrac x2+\dfrac y3=4', r'\dfrac x4-\dfrac y6=0') + r"\)."),
       D(r"\cdot6:\ 3x+2y=24\qquad\quad \cdot12:\ 3x-2y=0"),
       P(r"Els coeficients de la \(y\) són oposats: reducció.", r"Los coeficientes de la \(y\) son opuestos: reducción.", r"The \(y\) coefficients are opposite: elimination."),
       D(r"6x=24\ \Rightarrow\ x=4,\qquad 12+2y=24\ \Rightarrow\ y=6\qquad " + BX(4, 6)))],
 [prob(L(r"Resol \(" + SY(r'\dfrac{x+1}{3}-\dfrac{y-2}{4}=1', r'2(x-y)=x-7') + r"\).", r"Resuelve \(" + SY(r'\dfrac{x+1}{3}-\dfrac{y-2}{4}=1', r'2(x-y)=x-7') + r"\).", r"Solve \(" + SY(r'\dfrac{x+1}{3}-\dfrac{y-2}{4}=1', r'2(x-y)=x-7') + r"\)."),
       D(r"\cdot12:\ 4(x+1)-3(y-2)=12\ \Rightarrow\ 4x+4-3y+6=12\ \Rightarrow\ 4x-3y=2"),
       D(r"2x-2y=x-7\ \Rightarrow\ x-2y=-7\ \Rightarrow\ x=2y-7"),
       D(r"4(2y-7)-3y=2\ \Rightarrow\ 8y-28-3y=2\ \Rightarrow\ 5y=30\ \Rightarrow\ y=6,\quad x=12-7=5\qquad " + BX(5, 6)))])
same('3(x-1)+y=5', '3x+y=8'); same('x+2(y-1)=4', 'x+2y=6'); cs('3(x-1)+y=5', 'x+2(y-1)=4', (2, 2))
same('6*(x/2+y/3)=24', '3x+2y=24'); same('12*(x/4-y/6)=0', '3x-2y=0'); cs('x/2+y/3=4', 'x/4-y/6=0', (4, 6))
same('12*((x+1)/3-(y-2)/4)=12', '4x-3y=2'); same('2(x-y)=x-7', 'x-2y=-7'); cs('(x+1)/3-(y-2)/4=1', '2(x-y)=x-7', (5, 6))
s8 += practice([
  ('★', L(r"a) \(" + SY('2(x+y)-3x=1', 'x-(y-4)=5') + r"\)", r"a) \(" + SY('2(x+y)-3x=1', 'x-(y-4)=5') + r"\)", r"a) \(" + SY('2(x+y)-3x=1', 'x-(y-4)=5') + r"\)")),
  ('★★', L(r"b) \(" + SY(r'\dfrac x3+\dfrac y2=3', r'\dfrac x2-\dfrac y4=\dfrac12') + r"\)", r"b) \(" + SY(r'\dfrac x3+\dfrac y2=3', r'\dfrac x2-\dfrac y4=\dfrac12') + r"\)", r"b) \(" + SY(r'\dfrac x3+\dfrac y2=3', r'\dfrac x2-\dfrac y4=\dfrac12') + r"\)")),
  ('★★★', L(r"c) \(" + SY(r'\dfrac{x-1}{2}+y=4', r'x-\dfrac{y+1}{3}=4') + r"\)", r"c) \(" + SY(r'\dfrac{x-1}{2}+y=4', r'x-\dfrac{y+1}{3}=4') + r"\)", r"c) \(" + SY(r'\dfrac{x-1}{2}+y=4', r'x-\dfrac{y+1}{3}=4') + r"\)"))],
  D(r"\text{a)}\ \begin{cases}-x+2y=1\\x-y=1\end{cases}\Rightarrow y=2,\ x=3\qquad \text{b)}\ \begin{cases}2x+3y=18\\2x-y=2\end{cases}\Rightarrow 4y=16\Rightarrow y=4,\ x=3")
  + D(r"\text{c)}\ \begin{cases}x+2y=9\\3x-y=13\end{cases}\Rightarrow y=3x-13\Rightarrow 7x=35\Rightarrow x=5,\ y=2"))
same('2(x+y)-3x=1', '-x+2y=1'); same('x-(y-4)=5', 'x-y=1'); cs('2(x+y)-3x=1', 'x-(y-4)=5', (3, 2))
same('6*(x/3+y/2)=18', '2x+3y=18'); same('4*(x/2-y/4)=2', '2x-y=2'); cs('x/3+y/2=3', 'x/2-y/4=1/2', (3, 4))
same('2*((x-1)/2+y)=8', 'x+2y=9'); same('3*(x-(y+1)/3)=12', '3x-y=13'); cs('(x-1)/2+y=4', 'x-(y+1)/3=4', (5, 2))

# =====================================================================
# 6.9 Problemes amb sistemes d'equacions
# =====================================================================
s9 = box('prop', L('Com resolem un problema amb un sistema', 'Cómo resolvemos un problema con un sistema', 'How to solve a word problem with a system'),
  ol(L(r"<strong>Llegim i entenem</strong> l'enunciat: quines dades tenim i què ens pregunten.", r"<strong>Leemos y entendemos</strong> el enunciado: qué datos tenemos y qué nos preguntan.", r"<strong>Read and understand</strong> the problem: what you know and what you're asked."),
     L(r"<strong>Triem les dues incògnites</strong> i escrivim clarament què representen \(x\) i \(y\).", r"<strong>Elegimos las dos incógnitas</strong> y escribimos claramente qué representan \(x\) e \(y\).", r"<strong>Choose the two unknowns</strong> and write down clearly what \(x\) and \(y\) stand for."),
     L(r"<strong>Plantegem el sistema</strong>: busquem <strong>dues relacions</strong> entre les incògnites a l'enunciat, una per a cada equació.", r"<strong>Planteamos el sistema</strong>: buscamos <strong>dos relaciones</strong> entre las incógnitas en el enunciado, una para cada ecuación.", r"<strong>Set up the system</strong>: find <strong>two relationships</strong> between the unknowns in the problem, one for each equation."),
     L(r"<strong>Resolem</strong> el sistema pel mètode més adequat.", r"<strong>Resolvemos</strong> el sistema por el método más adecuado.", r"<strong>Solve</strong> the system with the most suitable method."),
     L(r"<strong>Comprovem</strong> la solució en l'enunciat (no sols en les equacions) i <strong>responem</strong> amb una frase.", r"<strong>Comprobamos</strong> la solución en el enunciado (no solo en las ecuaciones) y <strong>respondemos</strong> con una frase.", r"<strong>Check</strong> the solution against the problem (not just the equations) and <strong>answer</strong> in a sentence.")))
TR9 = [("La suma de dos nombres és 20", "La suma de dos números es 20", "Two numbers add up to 20", r"x+y=20"),
       ("La seua diferència és 4", "Su diferencia es 4", "Their difference is 4", r"x-y=4"),
       ("Un nombre és el triple de l'altre", "Un número es el triple del otro", "One number is three times the other", r"x=3y"),
       ("Gallines (\\(x\\)) i conills (\\(y\\)): 30 caps i 84 potes", "Gallinas (\\(x\\)) y conejos (\\(y\\)): 30 cabezas y 84 patas", "Hens (\\(x\\)) and rabbits (\\(y\\)): 30 heads and 84 legs", r"x+y=30,\ \ 2x+4y=84"),
       ("\\(x\\) entrades de 8 € i \\(y\\) de 5 €: 750 € en total", "\\(x\\) entradas de 8 € e \\(y\\) de 5 €: 750 € en total", "\\(x\\) tickets at €8 and \\(y\\) at €5: €750 in all", r"8x+5y=750"),
       ("D'ací a 10 anys el pare tindrà el doble d'edat que el fill", "Dentro de 10 años el padre tendrá el doble de edad que el hijo", "In 10 years the father will be twice as old as his son", r"x+10=2(y+10)"),
       ("Nombre de dues xifres: desenes \\(x\\), unitats \\(y\\)", "Número de dos cifras: decenas \\(x\\), unidades \\(y\\)", "Two-digit number: tens \\(x\\), units \\(y\\)", r"10x+y")]
s9 += box('prop', L('Traduccions útils', 'Traducciones útiles', 'Useful translations'),
  '<div class="tbl-wrap"><table class="data narrow"><thead><tr><th>' + L('Enunciat', 'Enunciado', 'In words') + '</th><th>' + L('Equació', 'Ecuación', 'Equation') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td class="l">{L(va, es, en)}</td><td>\\({e}\\)</td></tr>' for va, es, en, e in TR9) + '</tbody></table></div>'
  + drill('prob', 'Entrena: planteja i resol', 'Entrena: plantea y resuelve', 'Train: set up and solve'))
s9 += levels(
 [prob(L(r"La suma de dos nombres és 45 i la seua diferència, 7. Quins són?", r"La suma de dos números es 45 y su diferencia, 7. ¿Cuáles son?", r"Two numbers add up to 45 and their difference is 7. What are they?"),
       P(r"\(x\) = nombre major, \(y\) = nombre menor.", r"\(x\) = número mayor, \(y\) = número menor.", r"\(x\) = larger number, \(y\) = smaller number."),
       D(SY('x+y=45', 'x-y=7') + r"\ \xrightarrow{\text{%s}}\ 2x=52\ \Rightarrow\ x=26,\quad y=45-26=19" % Lt('sumem', 'sumamos', 'add')),
       P(r"Els nombres són <strong>26 i 19</strong>: \(26+19=45\) i \(26-19=7\) ✓", r"Los números son <strong>26 y 19</strong>: \(26+19=45\) y \(26-19=7\) ✓", r"The numbers are <strong>26 and 19</strong>: \(26+19=45\) and \(26-19=7\) ✓")),
  prob(L(r"En una granja hi ha gallines i conills. Hi ha 35 caps i 94 potes. Quants animals hi ha de cada tipus?", r"En una granja hay gallinas y conejos. Hay 35 cabezas y 94 patas. ¿Cuántos animales hay de cada tipo?", r"A farm has hens and rabbits: 35 heads and 94 legs. How many of each are there?"),
       P(r"\(x\) = gallines, \(y\) = conills. Cada animal té un cap; les gallines tenen 2 potes i els conills, 4.", r"\(x\) = gallinas, \(y\) = conejos. Cada animal tiene una cabeza; las gallinas tienen 2 patas y los conejos, 4.", r"\(x\) = hens, \(y\) = rabbits. Each animal has one head; hens have 2 legs and rabbits 4."),
       D(SY('x+y=35', '2x+4y=94') + r"\ \xrightarrow{(\cdot(-2))}\ \begin{array}{rrcr}-2x&-2y&=&-70\\2x&+4y&=&94\\\hline&2y&=&24\end{array}\ \Rightarrow\ y=12,\ \ x=23"),
       P(r"Hi ha <strong>23 gallines i 12 conills</strong>: \(46+48=94\) potes ✓", r"Hay <strong>23 gallinas y 12 conejos</strong>: \(46+48=94\) patas ✓", r"There are <strong>23 hens and 12 rabbits</strong>: \(46+48=94\) legs ✓"))],
 [prob(L(r"Les entrades d'un teatre costen 8 € per als adults i 5 € per als xiquets. Un dia hi van entrar 120 persones i es van recaptar 750 €. Quants adults i quants xiquets hi van anar?", r"Las entradas de un teatro cuestan 8 € para los adultos y 5 € para los niños. Un día entraron 120 personas y se recaudaron 750 €. ¿Cuántos adultos y cuántos niños fueron?", r"Theatre tickets cost €8 for adults and €5 for children. One day 120 people went in and €750 was taken. How many adults and how many children went?"),
       P(r"\(x\) = adults, \(y\) = xiquets.", r"\(x\) = adultos, \(y\) = niños.", r"\(x\) = adults, \(y\) = children."),
       D(SY('x+y=120', '8x+5y=750') + r"\qquad y=120-x\ \Rightarrow\ 8x+5(120-x)=750\ \Rightarrow\ 3x=150\ \Rightarrow\ x=50,\ \ y=70"),
       P(r"Hi van anar <strong>50 adults i 70 xiquets</strong>: \(400+350=750\) € ✓", r"Fueron <strong>50 adultos y 70 niños</strong>: \(400+350=750\) € ✓", r"<strong>50 adults and 70 children</strong> went: \(400+350=750\) € ✓")),
  prob(L(r"Un pare té el triple d'edat que el seu fill. D'ací a 10 anys només en tindrà el doble. Quants anys tenen ara?", r"Un padre tiene el triple de edad que su hijo. Dentro de 10 años solo tendrá el doble. ¿Cuántos años tienen ahora?", r"A father is three times as old as his son. In 10 years he'll only be twice as old. How old are they now?"),
       P(r"\(x\) = edat del pare, \(y\) = edat del fill (ara).", r"\(x\) = edad del padre, \(y\) = edad del hijo (ahora).", r"\(x\) = father's age, \(y\) = son's age (now)."),
       D(SY('x=3y', 'x+10=2(y+10)') + r"\qquad 3y+10=2y+20\ \Rightarrow\ y=10,\ \ x=30"),
       P(r"El pare té <strong>30 anys</strong> i el fill <strong>10</strong>. D'ací a 10 anys: 40 i 20 ✓", r"El padre tiene <strong>30 años</strong> y el hijo <strong>10</strong>. Dentro de 10 años: 40 y 20 ✓", r"The father is <strong>30</strong> and the son <strong>10</strong>. In 10 years: 40 and 20 ✓"))],
 [prob(L(r"Volem 50 kg de cafè a 9,60 €/kg barrejant un cafè de 12 €/kg amb un altre de 8 €/kg. Quants quilos de cada tipus hi hem de posar?", r"Queremos 50 kg de café a 9,60 €/kg mezclando un café de 12 €/kg con otro de 8 €/kg. ¿Cuántos kilos de cada tipo tenemos que poner?", r"We want 50 kg of coffee at €9.60/kg by mixing coffee at €12/kg with coffee at €8/kg. How many kilos of each do we need?"),
       P(r"\(x\) = kg de 12 €, \(y\) = kg de 8 €. El preu de la mescla és \(9{,}60\cdot50=480\) €.", r"\(x\) = kg de 12 €, \(y\) = kg de 8 €. El precio de la mezcla es \(9{,}60\cdot50=480\) €.", r"\(x\) = kg at €12, \(y\) = kg at €8. The mixture costs \(9.60\cdot50=480\) €."),
       D(SY('x+y=50', '12x+8y=480') + r"\ \xrightarrow{(\cdot(-8))}\ 4x=80\ \Rightarrow\ x=20,\ \ y=30"),
       P(r"Hem de posar <strong>20 kg del cafè de 12 €</strong> i <strong>30 kg del de 8 €</strong>: \(240+240=480\) € ✓", r"Tenemos que poner <strong>20 kg del café de 12 €</strong> y <strong>30 kg del de 8 €</strong>: \(240+240=480\) € ✓", r"We need <strong>20 kg of the €12 coffee</strong> and <strong>30 kg of the €8 one</strong>: \(240+240=480\) € ✓")),
  prob(L(r"Les xifres d'un nombre de dues xifres sumen 9. Si les intercanviem, el nombre augmenta en 27. Quin és el nombre?", r"Las cifras de un número de dos cifras suman 9. Si las intercambiamos, el número aumenta en 27. ¿Cuál es el número?", r"The digits of a two-digit number add up to 9. Swapping them increases the number by 27. What is the number?"),
       P(r"\(x\) = xifra de les desenes, \(y\) = xifra de les unitats. El nombre val \(10x+y\), i el nombre amb les xifres intercanviades, \(10y+x\).", r"\(x\) = cifra de las decenas, \(y\) = cifra de las unidades. El número vale \(10x+y\), y el número con las cifras intercambiadas, \(10y+x\).", r"\(x\) = tens digit, \(y\) = units digit. The number is \(10x+y\), and with the digits swapped it's \(10y+x\)."),
       D(SY('x+y=9', '10y+x=10x+y+27') + r"\ \Rightarrow\ " + SY('x+y=9', '-9x+9y=27') + r"\ \Rightarrow\ " + SY('x+y=9', '-x+y=3')),
       D(r"2y=12\ \Rightarrow\ y=6,\ \ x=3"),
       P(r"El nombre és el <strong>36</strong>: \(3+6=9\) i \(63-36=27\) ✓", r"El número es el <strong>36</strong>: \(3+6=9\) y \(63-36=27\) ✓", r"The number is <strong>36</strong>: \(3+6=9\) and \(63-36=27\) ✓"))])
cs('x+y=45', 'x-y=7', (26, 19)); cs('x+y=35', '2x+4y=94', (23, 12)); cs('x+y=120', '8x+5y=750', (50, 70)); cs('x=3y', 'x+10=2(y+10)', (30, 10))
cs('x+y=50', '12x+8y=480', (20, 30)); cs('x+y=9', '10y+x=10x+y+27', (3, 6)); same('10y+x=10x+y+27', '-9x+9y=27')
s9 += practice([
  ('★', L(r"a) Dos nombres sumen 30 i un és el quàdruple de l'altre. Quins són? b) En una guardiola hi ha 25 monedes d'1 € i de 2 €, que sumen 38 €. Quantes n'hi ha de cada?", r"a) Dos números suman 30 y uno es el cuádruple del otro. ¿Cuáles son? b) En una hucha hay 25 monedas de 1 € y de 2 €, que suman 38 €. ¿Cuántas hay de cada?", r"a) Two numbers add up to 30 and one is four times the other. What are they? b) A money box holds 25 €1 and €2 coins worth €38. How many of each?")),
  ('★★', L(r"c) Tres quaderns i dos bolígrafs costen 11 €; dos quaderns i tres bolígrafs, 9 €. Quant costa cada cosa? d) La base d'un rectangle fa 4 cm més que l'altura i el perímetre és 36 cm. Quines dimensions té?", r"c) Tres cuadernos y dos bolígrafos cuestan 11 €; dos cuadernos y tres bolígrafos, 9 €. ¿Cuánto cuesta cada cosa? d) La base de un rectángulo mide 4 cm más que la altura y el perímetro es 36 cm. ¿Qué dimensiones tiene?", r"c) Three notebooks and two pens cost €11; two notebooks and three pens, €9. How much is each? d) A rectangle's base is 4 cm longer than its height and its perimeter is 36 cm. What are its dimensions?")),
  ('★★★', L(r"e) Un test té 20 preguntes. Cada encert suma 3 punts i cada errada en resta 1. Si l'Anna les ha contestat totes i ha tret 40 punts, quantes n'ha encertat?", r"e) Un test tiene 20 preguntas. Cada acierto suma 3 puntos y cada fallo resta 1. Si Ana las ha contestado todas y ha sacado 40 puntos, ¿cuántas ha acertado?", r"e) A test has 20 questions. Each right answer scores 3 points and each wrong one loses 1. If Anna answered them all and scored 40, how many did she get right?"))],
  D(r"\text{a)}\ \begin{cases}x+y=30\\x=4y\end{cases}\Rightarrow y=6,\ x=24\qquad \text{b)}\ \begin{cases}x+y=25\\x+2y=38\end{cases}\Rightarrow y=13,\ x=12")
  + D(r"\text{c)}\ \begin{cases}3q+2b=11\\2q+3b=9\end{cases}\Rightarrow q=3\text{ €},\ b=1\text{ €}\qquad \text{d)}\ \begin{cases}x=y+4\\2x+2y=36\end{cases}\Rightarrow y=7,\ x=11")
  + D(r"\text{e)}\ \begin{cases}x+y=20\\3x-y=40\end{cases}\Rightarrow 4x=60\Rightarrow x=15\ \text{%s},\ y=5" % Lt('encerts', 'aciertos', 'right')))
cs('x+y=30', 'x=4y', (24, 6)); cs('x+y=25', 'x+2y=38', (12, 13)); cs('3x+2y=11', '2x+3y=9', (3, 1)); cs('x=y+4', '2x+2y=36', (11, 7)); cs('x+y=20', '3x-y=40', (15, 5))

# ============================================================ muntatge
SECS = [
  (L('Equacions lineals amb dues incògnites', 'Ecuaciones lineales con dos incógnitas', 'Linear equations in two unknowns'), s1),
  (L("Sistemes de dues equacions amb dues incògnites", 'Sistemas de dos ecuaciones con dos incógnitas', 'Systems of two equations in two unknowns'), s2),
  (L('Mètode de substitució', 'Método de sustitución', 'Substitution method'), s3),
  (L("Mètode d'igualació", 'Método de igualación', 'Equalisation method'), s4),
  (L('Mètode de reducció', 'Método de reducción', 'Elimination method'), s5),
  (L('Mètode gràfic', 'Método gráfico', 'Graphical method'), s6),
  (L('Classificació dels sistemes', 'Clasificación de los sistemas', 'Classifying systems'), s7),
  (L('Sistemes amb parèntesis i denominadors', 'Sistemas con paréntesis y denominadores', 'Systems with brackets and fractions'), s8),
  (L("Problemes amb sistemes d'equacions", 'Problemas con sistemas de ecuaciones', 'Word problems with systems'), s9),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Sistemes d'equacions · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 6 (Sistemes d\'equacions) de 3r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "{x,y}";')
assert "Sistemes d'equacions · FentMates" in head and 'content: "{x,y}"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
assert 'NSEC = %d' % NS in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">6.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../3eso.html">{L("3r ESO", "3º ESO", "3rd ESO (Year 9)")}</a> / {L("Unitat 6", "Unidad 6", "Unit 6")}</span>
    <span class="spacer"></span>
    <div class="lang-switch" role="group" aria-label="Idioma / Language">
      <button type="button" data-setlang="va">VA</button><button type="button" data-setlang="es">ES</button><button type="button" data-setlang="en">EN</button>
    </div>
    <button class="icon-btn" type="button" id="theme-btn" aria-label="Mode clar / fosc"></button>
  </div>
  <div class="progress" id="progress"></div>
</header>

<section class="hero">
  <div class="in">
    <span class="kicker">{L("Apunts de teoria · 3r ESO · Matemàtiques", "Apuntes de teoría · 3º ESO · Matemáticas", "Theory notes · 3rd ESO · Mathematics")}</span>
    <h1><span class="u">{L("Unitat 6", "Unidad 6", "Unit 6")}</span> · {L("Sistemes d'equacions", "Sistemas de ecuaciones", "Simultaneous equations")}</h1>
    <p>{L("Equacions lineals amb dues incògnites, sistemes de dues equacions amb dues incògnites, mètodes de substitució, igualació, reducció i gràfic, classificació dels sistemes segons el nombre de solucions i problemes amb sistemes: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Ecuaciones lineales con dos incógnitas, sistemas de dos ecuaciones con dos incógnitas, métodos de sustitución, igualación, reducción y gráfico, clasificación de los sistemas según el número de soluciones y problemas con sistemas: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Linear equations in two unknowns, systems of two equations in two unknowns, the substitution, equalisation, elimination and graphical methods, classifying systems by their number of solutions and word problems: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
    <div class="chips"><span>{L(f"{NS} apartats", f"{NS} apartados", f"{NS} sections")}</span><span>{L(f"{ntools} eines interactives", f"{ntools} herramientas interactivas", f"{ntools} interactive tools")}</span><span>{L("Problemes per nivells ★☆☆ → ★★★", "Problemas por niveles ★☆☆ → ★★★", "Problems by level ★☆☆ → ★★★")}</span><span>{L("Autoavaluació final", "Autoevaluación final", "Final self-check")}</span></div>
  </div>
</section>

<div class="layout">
  <nav class="toc" aria-label="Índex">
    <details open id="toc-d">
      <summary>{L("Índex", "Índice", "Contents")}</summary>
      <ol id="toc-list">
{toc}        <li><a href="#quiz"><span class="n">?</span>{L("Autoavaluació", "Autoevaluación", "Self-check")}</a></li>
      </ol>
      <div class="meter"><i id="meter"></i></div>
      <div class="meter-l"><span id="meter-n">0</span>/{NS} {L("apartats estudiats", "apartados estudiados", "sections studied")}</div>
    </details>
  </nav>

<article>
{''.join(sec(i, t, b) for i, (t, b) in enumerate(SECS, 1))}
<!-- ======================= QUIZ ======================= -->
<section class="unit quiz-sec" id="quiz">
  <div class="sec-head"><span class="num">?</span><h2>{L("Autoavaluació", "Autoevaluación", "Self-check")}</h2></div>
  {P("Respon i comprova a l'instant si ho has entés. Les preguntes van de més fàcils a més difícils.", "Responde y comprueba al instante si lo has entendido. Las preguntas van de más fáciles a más difíciles.", "Answer and instantly check whether you've understood. The questions go from easier to harder.")}
  <div class="quiz" id="quiz-box"></div>
  <div class="score" id="quiz-score"></div>
  <button class="btn" type="button" id="quiz-reset">↺ {L("Torna a començar", "Volver a empezar", "Start again")}</button>
</section>

</article>
</div>

<footer class="foot">
  <p>{L("Apunts de teoria · Unitat 6: Sistemes d'equacions · 3r ESO", "Apuntes de teoría · Unidad 6: Sistemas de ecuaciones · 3º ESO", "Theory notes · Unit 6: Simultaneous equations · 3rd ESO")}</p>
  <p><a href="../../index.html">FentMates</a> · {L("Fet amb ♥ per a l'alumnat", "Hecho con ♥ para el alumnado", "Made with ♥ for students")}</p>
</footer>
<button class="icon-btn to-top" type="button" id="to-top" aria-label="↑">↑</button>

<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
{js}</script>
</body>
</html>
'''
html = head + '\n' + css + '\n' + wide + '\n</style>\n</head>\n' + body
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(html)
print('ok', OUT, len(html.split('\n')), 'lines,', ntools, 'tools')

sys.path.insert(0, os.path.dirname(HERE))
import relabel
print('\n'.join(relabel.fix_file(OUT)))

# FentMates: enllaça el tema comú (logo i colors del bloc) només a aquesta pàgina; aplica.py sencer
# reescriuria la versió de totes les altres pàgines de materials/.
import importlib.util as _ilu
_d = os.path.dirname(HERE)
while os.path.basename(_d) != "_eines":
    _d = os.path.dirname(_d)
_sp = _ilu.spec_from_file_location("aplica", os.path.join(_d, "tema", "aplica.py"))
_tema = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_tema)
_tema.VERSION = "20261030a"
_tema.aplica_fitxer(OUT)
