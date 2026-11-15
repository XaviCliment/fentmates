# Versió en castellà de genera.py. Genera t7-fitxa-exercicis-es.tex i t7-fitxa-solucions-es.tex
# (1r ESO, Unitat 7: Geometria bàsica del pla — punts, rectes, angles i polígons; sense àrees ni perímetres)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Els càlculs amb angles es fan en segons (sx/dms) i les asserts CHK comproven cada resultat escrit.
import os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- comprovacions ----------
NCHK = [0]
def CHK(cond, *info):
    NCHK[0] += 1
    assert cond, info
def sx(d, m=0, s=0): return d * 3600 + m * 60 + s
def dms(t): return t // 3600, t % 3600 // 60, t % 60
def A(t):
    """angle (en segons) en TeX: 12^\\circ\\,30'\\,15''"""
    d, m, s = dms(t); out = []
    if d or (not m and not s): out.append(r'%d^\circ' % d)
    if m: out.append(r"%d'" % m)
    if s: out.append(r"%d''" % s)
    return r'\,'.join(out)
def eqA(t, txt):
    """comprova que el text en forma complexa correspon a t segons"""
    m = re.fullmatch(r"(?:(\d+)\^\\circ)?(?:\\,)?(?:(\d+)')?(?:\\,)?(?:(\d+)'')?", txt)
    CHK(m is not None, txt)
    d, mi, s = (int(g) if g else 0 for g in m.groups())
    CHK(mi < 60 and s < 60 and sx(d, mi, s) == t, txt, dms(t))
    return txt
def diag(n): return n * (n - 3) // 2
def S(n): return (n - 2) * 180

# ---------- figures (TikZ) ----------
ST = {'': 'thick', 'gf': 'fill=teal!12,draw=teal,thick', 'hl': 'accent,very thick', 'd': 'dashed,muted', 'af': 'fill=accent!30,draw=accent', 'af2': 'fill=teal!30,draw=teal', 'thin': 'muted'}
def P_(p): return '(%.3f,%.3f)' % (float(p[0]), float(p[1]))
def pol(C, r, a): return (C[0] + r * math.cos(math.radians(a)), C[1] + r * math.sin(math.radians(a)))
def reg(n, r=1, rot=None):
    rot = -90 - 180 / n if rot is None else rot
    return [pol((0, 0), r, rot + 360 * k / n) for k in range(n)]
def tz(items, s=0.5):
    o = [r'\begin{tikzpicture}[x=%scm,y=%scm,baseline=(current bounding box.center),line join=round,line cap=round]' % (s, s)]
    for it in items:
        k = it[0]
        if k == 'poly': o.append(r'\draw[%s] %s -- cycle;' % (ST[it[2]], ' -- '.join(P_(p) for p in it[1])))
        elif k == 'seg': o.append(r'\draw[%s] %s -- %s;' % (ST[it[3] if len(it) > 3 else ''], P_(it[1]), P_(it[2])))
        elif k == 'ln':
            ends = it[4] if len(it) > 4 else 'b'
            arr = {'b': 'latex-latex', 'e': '-latex', '': '-'}[ends]
            o.append(r'\draw[%s,%s] %s -- %s;' % (ST[it[3] if len(it) > 3 else ''], arr, P_(it[1]), P_(it[2])))
        elif k == 'ra':
            V, A_, B = it[1], it[2], it[3]; q = 0.22 / s
            def u(Pp):
                dx, dy = Pp[0] - V[0], Pp[1] - V[1]; n = math.hypot(dx, dy); return dx / n * q, dy / n * q
            ua, ub = u(A_), u(B)
            o.append(r'\draw[thin] %s -- %s -- %s;' % (P_((V[0] + ua[0], V[1] + ua[1])), P_((V[0] + ua[0] + ub[0], V[1] + ua[1] + ub[1])), P_((V[0] + ub[0], V[1] + ub[1]))))
        elif k == 'tick':
            A_, B, n = it[1], it[2], it[3]; dx, dy = B[0] - A_[0], B[1] - A_[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; M = ((A_[0] + B[0]) / 2, (A_[1] + B[1]) / 2)
            h = 0.12 / s
            for j in range(n):
                of = (j - (n - 1) / 2) * 0.09 / s; C = (M[0] + of * ux, M[1] + of * uy)
                o.append(r'\draw[thick] %s -- %s;' % (P_((C[0] - h * uy, C[1] + h * ux)), P_((C[0] + h * uy, C[1] - h * ux))))
        elif k == 'sect':
            C, r, a0, a1 = it[1], it[2], it[3], it[4]
            o.append(r'\draw[%s] %s -- %s arc[start angle=%s,end angle=%s,radius=%s] -- cycle;' % (ST[it[5] if len(it) > 5 else 'af'], P_(C), P_(pol(C, r, a0)), a0, a1, r))
        elif k == 'lab': o.append(r'\node[font=\small,%s] at %s {%s};' % (it[3] if len(it) > 3 else 'inner sep=1pt', P_(it[1]), it[2]))
        elif k == 'dot': o.append(r'\fill %s circle (1.5pt);' % P_(it[1]))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def angfig(a, a0=0, r=1.8, R=0.5, lab=None):
    it = []
    if a == 90: it.append(('poly', [(0, 0), pol((0, 0), 0.4, a0), pol(pol((0, 0), 0.4, a0), 0.4, a0 + 90), pol((0, 0), 0.4, a0 + 90)], 'af'))
    else: it.append(('sect', (0, 0), R, a0, a0 + a, 'af'))
    it += [('ln', (0, 0), pol((0, 0), r, a0), '', 'e'), ('ln', (0, 0), pol((0, 0), r, a0 + a), '', 'e'), ('dot', (0, 0))]
    if lab: it.append(('lab', pol((0, 0), R + 0.45, a0 + a / 2), lab))
    return it
def parfig(a, given=None, nums=True, s=0.85):
    """paral·leles y=0 i y=1,8 tallades per una secant amb angle a; angles numerats 1-8"""
    h = 1.8; X1 = h / math.tan(math.radians(a)); P1, P2 = (0, 0), (X1, h)
    it = [('ln', (-2.2, 0), (2.2 + X1, 0), '', 'b'), ('ln', (-2.2, h), (2.2 + X1, h), '', 'b'), ('ln', pol(P1, 1.3, 180 + a), pol(P2, 1.3, a), '', 'b'),
          ('lab', (-2.2, h), '$r$', 'above'), ('lab', (-2.2, 0), '$s$', 'above')]
    for P, off in ((P1, 0), (P2, 4)):
        for k, (a0, a1) in enumerate([(0, a), (a, 180), (180, 180 + a), (180 + a, 360)]):
            n = off + k + 1
            if given and n == given[0]: it.append(('sect', P, 0.45, a0, a1, 'af')); it.append(('lab', pol(P, 0.95, (a0 + a1) / 2), given[1]))
            elif nums: it.append(('lab', pol(P, 0.62, (a0 + a1) / 2), r'\scriptsize %d' % n))
    return tz(it, s)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Punts, rectes, semirectes i segments
# =====================================================================
F1 = tz([('ln', (-0.5, 0), (7.5, 0), '', 'b'), ('lab', (7.3, 0), '$r$', 'below')] + [x for i, t in enumerate('ABC') for x in (('dot', (1 + 2.5 * i, 0)), ('lab', (1 + 2.5 * i, 0), '$%s$' % t, 'above'))]
        + [('dot', (4.6, 1.5)), ('lab', (4.6, 1.5), '$D$', 'above')], 0.6)
F2 = [tz([('ln', (0, 0), (3, 0.6), '', 'b'), ('dot', (1, 0.2)), ('dot', (2, 0.4))], 0.6), tz([('ln', (0, 0), (3, 0.6), '', ''), ('dot', (0, 0)), ('dot', (3, 0.6))], 0.6), tz([('ln', (0, 0), (3, 0.6), '', 'e'), ('dot', (0, 0))], 0.6)]
CHK(4 * 3 // 2 == 6 and 6 * 5 // 2 == 15 and 5 + 3 == 8 and 5 - 3 == 2 and 4 * 3 // 2 == 6 and 5 * 4 // 2 == 10 and 7 * 6 // 2 == 21)
S_.append(("Puntos, rectas, semirrectas y segmentos", [
 (1, r"Observa la figura y responde:\par\smallskip\begin{center}" + F1 + r"\end{center}" + tasks(1, [r"¿Qué puntos son de la recta $r$? ¿Qué punto no está en ella?", r"Escribe todos los segmentos que tienen los extremos en dos de los puntos $A$, $B$ y $C$.", r"¿Cuántas semirrectas de la recta $r$ tienen el origen en $B$?"])
     + recorda(r"La \textbf{recta} no tiene principio ni final; la \textbf{semirrecta} tiene origen pero no tiene final; el \textbf{segmento} tiene dos extremos y se puede medir. Por dos puntos pasa una única recta."),
     tasks(1, [r"$A$, $B$ y $C$ son de la recta $r$ (están \rest{alineados}); $D$ \rest{no} está en ella.", r"\rest{$\overline{AB}$, $\overline{AC}$ y $\overline{BC}$} (3 segmentos).", r"\rest{Dos}: una hacia $A$ y otra hacia $C$."])),
 (1, r"Di si cada figura es una recta, una semirrecta o un segmento:" + tasks(3, F2),
     tasks(3, [r"\rest{Recta} (dos flechas)", r"\rest{Segmento} (dos extremos)", r"\rest{Semirrecta} (una flecha)"])),
 (1, r"Responde:" + tasks(1, [r"El segmento $\overline{AB}$ mide 7\,cm y $M$ es su punto medio. ¿Cuánto mide $\overline{AM}$?", r"$M$ es el punto medio de $\overline{PQ}$ y $\overline{PM}$ mide 4,2\,cm. ¿Cuánto mide $\overline{PQ}$?"]),
     tasks(1, [r"$7:2=\res{3,5\text{ cm}}$", r"$2\cdot4,2=\res{8,4\text{ cm}}$"])),
 (2, r"Sobre una recta marcamos cuatro puntos. ¿Cuántos segmentos determinan? ¿Y si marcamos seis?",
     r"Con 4 puntos: $3+2+1=\res{6}$ segmentos. Con 6 puntos: $5+4+3+2+1=\res{15}$ segmentos."),
 (2, r"Los puntos $A$, $B$ y $C$ están sobre una recta, en este orden. $\overline{AB}=5$\,cm y $\overline{BC}=3$\,cm. ¿Cuánto mide $\overline{AC}$? ¿Y si $C$ estuviera entre $A$ y $B$ (con $\overline{BC}=3$\,cm)?",
     r"En el primer caso, $\overline{AC}=5+3=\res{8\text{ cm}}$. En el segundo, $\overline{AC}=5-3=\res{2\text{ cm}}$."),
 (3, r"Dibujamos puntos de manera que no haya tres alineados. ¿Cuántas rectas podemos trazar que pasen por dos de ellos si hay 4 puntos? ¿Y 5? ¿Y 7?",
     r"De cada punto salen tantas rectas como puntos quedan, y cada recta se cuenta dos veces: \ $\frac{4\cdot3}{2}=\res{6}$, \ $\frac{5\cdot4}{2}=\res{10}$, \ $\frac{7\cdot6}{2}=\res{21}$."),
]))

# =====================================================================
# 2. Posicions relatives de rectes. Mediatriu
# =====================================================================
F7 = tz([('ln', (-0.4, 0), (6.4, 0), '', 'b'), ('ln', (-0.4, 1.6), (6.4, 1.6), '', 'b'), ('ln', (1.5, -0.9), (1.5, 2.6), '', 'b'), ('ln', (2.8, -0.9), (6.2, 2.6), '', 'b'), ('ra', (1.5, 0), (2.5, 0), (1.5, 1)),
         ('lab', (6.4, 0), '$r$', 'right'), ('lab', (6.4, 1.6), '$s$', 'right'), ('lab', (1.5, 2.6), '$t$', 'above'), ('lab', (6.2, 2.6), '$u$', 'above')], 0.6)
S_.append(("Posiciones relativas de rectas. Mediatriz", [
 (1, r"Las rectas $r$ y $s$ son paralelas. Di cómo son:\par\smallskip\begin{center}" + F7 + r"\end{center}" + tasks(4, [r"$r$ y $s$", r"$r$ y $t$", r"$s$ y $t$", r"$r$ y $u$"])
     + recorda(r"Dos rectas son \textbf{secantes} si se cortan en un punto, \textbf{paralelas} si no se cortan nunca y \textbf{perpendiculares} si se cortan formando cuatro ángulos rectos ($r\perp s$)."),
     tasks(4, [r"\rest{paralelas}", r"\rest{perpendiculares}", r"\rest{perpendiculares}", r"\rest{secantes}"])),
 (1, r"Di si son paralelas, secantes o perpendiculares:" + tasks(2, [r"Dos lados opuestos de una hoja de papel.", r"Dos lados de una hoja que forman una esquina.", r"Las agujas de un reloj a las 9 en punto.", r"Las agujas de un reloj a las 10 en punto."]),
     tasks(2, [r"\rest{Paralelas}", r"\rest{Perpendiculares}", r"\rest{Perpendiculares} (ángulo de $90^\circ$)", r"\rest{Secantes} (ángulo de $60^\circ$)"])),
 (1, r"Dibuja un segmento $\overline{AB}$ de 6\,cm y traza su mediatriz con regla y compás. ¿A qué distancia de $A$ corta el segmento?",
     r"Con el compás abierto más de 3\,cm, traza arcos desde $A$ y desde $B$ que se corten por encima y por debajo del segmento; la recta que une los dos puntos de corte es la mediatriz. Corta el segmento en el punto medio, a \rest{3\,cm} de $A$, y es perpendicular al segmento."),
 (2, r"Di si es cierto o falso:" + tasks(1, [r"Dos rectas perpendiculares son siempre secantes.", r"Dos rectas secantes son siempre perpendiculares.", r"Si $r\parallel s$ y $s\parallel t$, entonces $r\parallel t$.", r"Si $r\perp s$ y $s\perp t$, entonces $r\perp t$."]),
     tasks(1, [r"\rest{Cierto}: se cortan en un punto.", r"\rest{Falso}: solo si forman ángulos rectos.", r"\rest{Cierto}.", r"\rest{Falso}: $r$ y $t$ son paralelas."])),
 (2, r"El punto $P$ está sobre la mediatriz del segmento $\overline{AB}$, que mide 8\,cm, y la distancia de $P$ a $A$ es 5\,cm. ¿Cuánto mide $\overline{PB}$? ¿A qué distancia de $A$ está el punto medio $M$?",
     r"Los puntos de la mediatriz equidistan de los extremos: $\overline{PB}=\res{5\text{ cm}}$. \ $\overline{AM}=8:2=\res{4\text{ cm}}$."),
 (3, r"Dos casas, $A$ y $B$, están al mismo lado de un camino recto. ¿Dónde se tiene que poner una fuente, junto al camino, para que esté a la misma distancia de las dos casas? Explica cómo la encontrarías.",
     r"Los puntos que equidistan de $A$ y $B$ son los de la \rest{mediatriz de $\overline{AB}$}. La fuente tiene que estar en el \rest{punto donde la mediatriz corta el camino}."),
]))

# =====================================================================
# 3. Angles
# =====================================================================
F14 = [tz(angfig(a, a0, r=3.0, R=0.6), 0.8) for a, a0 in ((40, 10), (90, 0), (140, 0), (230, 0))]
CHK([3 * 30, 4 * 30, 5 * 30, 6 * 30, 3 * 30, 1 * 30] == [90, 120, 150, 180, 90, 30])
CHK([10 * 6, 25 * 6, 60 * 6, 45 * 6] == [60, 150, 360, 270] and 136 // 2 == 68 and 2 * 43 == 86 and 360 - 125 == 235 and 360 // 5 == 72 and 360 // 8 == 45 and 180 // 15 == 12)
S_.append(("Ángulos: elementos, medida y clasificación", [
 (1, r"Clasifica estos ángulos (nulo, agudo, recto, obtuso, llano, cóncavo o completo):" + tasks(4, [r"$25^\circ$", r"$90^\circ$", r"$100^\circ$", r"$180^\circ$", r"$270^\circ$", r"$360^\circ$", r"$179^\circ$", r"$89^\circ$"])
     + recorda(r"Agudo: menos de $90^\circ$. Recto: $90^\circ$. Obtuso: entre $90^\circ$ y $180^\circ$. Llano: $180^\circ$. Cóncavo: más de $180^\circ$. Completo: $360^\circ$."),
     tasks(4, [r"\rest{agudo}", r"\rest{recto}", r"\rest{obtuso}", r"\rest{llano}", r"\rest{cóncavo}", r"\rest{completo}", r"\rest{obtuso}", r"\rest{agudo}"])),
 (1, r"Clasifica cada ángulo y mídelo con el transportador:" + tasks(2, F14),
     tasks(4, [r"\rest{agudo} ($40^\circ$)", r"\rest{recto} ($90^\circ$)", r"\rest{obtuso} ($140^\circ$)", r"\rest{cóncavo} ($230^\circ$)"])),
 (1, r"¿Qué ángulo (convexo) forman las agujas de un reloj a las horas en punto siguientes?" + tasks(6, [r"3 h", r"4 h", r"5 h", r"6 h", r"9 h", r"11 h"]),
     r"Entre dos números de la esfera hay $360^\circ:12=30^\circ$." + tasks(6, [r"$\res{90^\circ}$", r"$\res{120^\circ}$", r"$\res{150^\circ}$", r"$\res{180^\circ}$", r"$\res{90^\circ}$", r"$\res{30^\circ}$"])),
 (2, r"¿Cuántos grados gira la aguja de los minutos en estos tiempos?" + tasks(4, [r"10 min", r"25 min", r"1 hora", r"tres cuartos de hora"]),
     r"Cada minuto gira $360^\circ:60=6^\circ$." + tasks(4, [r"$\res{60^\circ}$", r"$\res{150^\circ}$", r"$\res{360^\circ}$", r"$45\cdot6=\res{270^\circ}$"])),
 (2, r"Responde:" + tasks(1, [r"¿Qué ángulos forma la bisectriz de un ángulo de $136^\circ$ con cada uno de los lados?", r"La bisectriz de un ángulo forma con uno de los lados un ángulo de $43^\circ$. ¿Cuánto mide el ángulo?"]),
     tasks(1, [r"$136^\circ:2=\res{68^\circ}$ cada uno.", r"$2\cdot43^\circ=\res{86^\circ}$ (agudo)."])),
 (2, r"Dos semirrectas con el mismo origen forman un ángulo convexo de $125^\circ$. ¿Cuánto mide el ángulo cóncavo que forman?",
     r"Entre los dos forman una vuelta completa: $360^\circ-125^\circ=\res{235^\circ}$."),
 (3, r"Responde:" + tasks(1, [r"Dividimos un ángulo completo en 5 ángulos iguales. ¿Cuánto mide cada uno? ¿Y si lo dividimos en 8?", r"¿Cuántas veces cabe un ángulo de $15^\circ$ en un ángulo llano?"]),
     tasks(1, [r"$360^\circ:5=\res{72^\circ}$; \ $360^\circ:8=\res{45^\circ}$.", r"$180:15=\res{12}$ veces."])),
]))

# =====================================================================
# 4. El sistema sexagesimal
# =====================================================================
E20 = [(2, 0, 0), (0, 15, 0), (1, 20, 0), (3, 5, 40), (10, 10, 10), (0, 45, 30)]
R20 = [7200, 900, 4800, 11140, 36610, 2730]
for e, r in zip(E20, R20): CHK(sx(*e) == r, e)
E21 = [(5, 0), (2, 30), (12, 45), (180, 0)]; R21 = [300, 150, 765, 10800]
for e, r in zip(E21, R21): CHK(e[0] * 60 + e[1] == r)
E22 = [("150'", 150 * 60, r"2^\circ\,30'"), ("4000''", 4000, r"1^\circ\,6'\,40''"), ("7385''", 7385, r"2^\circ\,3'\,5''"), ("10\,000''", 10000, r"2^\circ\,46'\,40''"), ("1000'", 60000, r"16^\circ\,40'"), ("86\,400''", 86400, r"24^\circ")]
for _, t, w in E22: eqA(t, w)
E23 = [("12,5", sx(12, 30), r"12^\circ\,30'"), ("30,25", sx(30, 15), r"30^\circ\,15'"), ("8,75", sx(8, 45), r"8^\circ\,45'"), ("0,1", sx(0, 6), r"6'")]
for v, t, w in E23: CHK(abs(float(v.replace(',', '.')) * 3600 - t) < 1e-6); eqA(t, w)
OP = [  # (enunciat, resultat en segons, resultat escrit)
 (r"23^\circ\,45'+18^\circ\,30'", sx(23, 45) + sx(18, 30), r"42^\circ\,15'"),
 (r"45^\circ\,36'\,50''+27^\circ\,48'\,25''", sx(45, 36, 50) + sx(27, 48, 25), r"73^\circ\,25'\,15''"),
 (r"120^\circ\,15'\,40''+59^\circ\,44'\,20''", sx(120, 15, 40) + sx(59, 44, 20), r"180^\circ"),
 (r"75^\circ\,40'-32^\circ\,15'", sx(75, 40) - sx(32, 15), r"43^\circ\,25'"),
 (r"60^\circ\,20'\,15''-25^\circ\,45'\,30''", sx(60, 20, 15) - sx(25, 45, 30), r"34^\circ\,34'\,45''"),
 (r"180^\circ-97^\circ\,34'\,18''", sx(180) - sx(97, 34, 18), r"82^\circ\,25'\,42''"),
 (r"(12^\circ\,20')\cdot3", sx(12, 20) * 3, r"37^\circ"),
 (r"(25^\circ\,15'\,40'')\cdot4", sx(25, 15, 40) * 4, r"101^\circ\,2'\,40''"),
 (r"(8^\circ\,45'\,50'')\cdot6", sx(8, 45, 50) * 6, r"52^\circ\,35'"),
 (r"(75^\circ\,36'):4", sx(75, 36) // 4, r"18^\circ\,54'"),
 (r"(100^\circ\,20'\,30''):5", sx(100, 20, 30) // 5, r"20^\circ\,4'\,6''"),
 (r"(47^\circ\,13'):3", sx(47, 13) // 3, r"15^\circ\,44'\,20''")]
for _, t, w in OP: eqA(t, w)
CHK(sx(75, 36) % 4 == 0 and sx(100, 20, 30) % 5 == 0 and sx(47, 13) % 3 == 0)
CHK(360 * 3600 // 24 == sx(15) and sx(15) // 60 == sx(0, 15) and sx(0, 15) // 60 == 15)
def ops(a, b): return tasks(3, [r"$%s$" % e for e, _, _ in OP[a:b]]), tasks(2, [r"$%s=\res{%s}$" % (e, w) for e, _, w in OP[a:b]])
S_.append(("Medida de ángulos: el sistema sexagesimal", [
 (1, r"Expresa en segundos:" + tasks(3, [r"$%s$" % A(sx(*e)) if e != (0, 45, 30) else r"$45'\,30''$" for e in E20])
     + recorda(r"$1^\circ=60'$, \ $1'=60''$, \ $1^\circ=3600''$. Para pasar a una unidad más pequeña multiplicamos; para pasar a una unidad más grande dividimos entre 60."),
     tasks(3, [r"$\res{%d''}$" % r for r in R20])),
 (1, r"Expresa en minutos:" + tasks(4, [r"$5^\circ$", r"$2^\circ\,30'$", r"$12^\circ\,45'$", r"$180^\circ$"]),
     tasks(4, [r"$\res{%d'}$" % r if r < 10000 else r"$\res{10\,800'}$" for r in R21])),
 (1, r"Pasa a forma compleja (grados, minutos y segundos):" + tasks(3, [r"$%s$" % e for e, _, _ in E22]),
     r"Dividimos entre 60 tantas veces como haga falta: por ejemplo, $4000'':60=66'$ y sobran $40''$; $66':60=1^\circ$ y sobran $6'$." + tasks(3, [r"$\res{%s}$" % w for _, _, w in E22])),
 (2, r"Expresa en grados y minutos:" + tasks(4, [r"$%s^\circ$" % v for v, _, _ in E23]),
     r"La parte decimal de los grados se multiplica por 60: $0,5^\circ=30'$, \ $0,25^\circ=15'$, \ $0,75^\circ=45'$, \ $0,1^\circ=6'$." + tasks(4, [r"$\res{%s}$" % w for _, _, w in E23])),
 (2, r"Calcula:" + ops(0, 3)[0], ops(0, 3)[1]),
 (2, r"Calcula:" + ops(3, 6)[0], r"Cuando no se puede restar, convertimos $1^\circ$ en $60'$ o $1'$ en $60''$." + ops(3, 6)[1]),
 (2, r"Calcula:" + ops(6, 9)[0], ops(6, 9)[1]),
 (3, r"Calcula y comprueba el resultado multiplicando:" + ops(9, 12)[0],
     ops(9, 12)[1] + r"Comprobación del primero: $(18^\circ\,54')\cdot4=72^\circ\,216'=75^\circ\,36'$ \checkmark"),
 (3, r"La Tierra da una vuelta completa sobre sí misma en 24 horas. ¿Cuántos grados gira en 1 hora? ¿Y en 1 minuto? ¿Y en 1 segundo?",
     r"En 1 hora: $360^\circ:24=\res{15^\circ}$. En 1 minuto: $15^\circ:60=900':60=\res{15'}$. En 1 segundo: $15':60=900'':60=\res{15''}$."),
]))
CHK(sx(18, 54) * 4 == sx(72, 216) == sx(75, 36))

# =====================================================================
# 5. Relacions entre angles
# =====================================================================
F31 = tz([('sect', (0, 0), 0.5, 30, 65, 'af'), ('ln', pol((0, 0), 2, 210), pol((0, 0), 2, 30), '', 'b'), ('ln', pol((0, 0), 2, 245), pol((0, 0), 2, 65), '', 'b'), ('dot', (0, 0)),
          ('lab', pol((0, 0), 0.95, 47), r'$35^\circ$'), ('lab', pol((0, 0), 0.75, 147), '$a$'), ('lab', pol((0, 0), 0.75, 227), '$b$'), ('lab', pol((0, 0), 0.75, 327), '$c$')], 0.6)
CT = [(sx(30), sx(60)), (sx(47), sx(43)), (sx(89), sx(1)), (sx(15, 30), sx(74, 30))]
for a, c in CT: CHK(a + c == sx(90))
ST_ = [(sx(45), sx(135)), (sx(120), sx(60)), (sx(179), sx(1)), (sx(92, 15, 40), sx(87, 44, 20))]
for a, c in ST_: CHK(a + c == sx(180))
CHK(sx(90) - sx(37, 25, 48) == sx(52, 34, 12) and sx(180) - sx(37, 25, 48) == sx(142, 34, 12))
CHK(35 + 55 == 90 and 55 - 35 == 20 and 36 + 144 == 180 and 144 == 4 * 36 and 3 * 20 + 10 == 70)
S_.append(("Relaciones entre ángulos", [
 (1, r"Calcula el complementario de cada ángulo:" + tasks(4, [r"$%s$" % A(a) for a, _ in CT])
     + recorda(r"Dos ángulos son \textbf{complementarios} si suman $90^\circ$ y \textbf{suplementarios} si suman $180^\circ$. Los ángulos \textbf{opuestos por el vértice} son iguales y los \textbf{adyacentes} suman $180^\circ$."),
     tasks(4, [r"$\res{%s}$" % eqA(c, A(c)) for _, c in CT])),
 (1, r"Calcula el suplementario de cada ángulo:" + tasks(4, [r"$%s$" % A(a) for a, _ in ST_]),
     tasks(4, [r"$\res{%s}$" % eqA(c, A(c)) for _, c in ST_])),
 (1, r"Dos rectas se cortan y uno de los ángulos mide $35^\circ$. Calcula los ángulos $a$, $b$ y $c$ y explica cómo los has encontrado.\par\smallskip\begin{center}" + F31 + r"\end{center}",
     r"$a$ y $c$ son adyacentes al ángulo de $35^\circ$: $a=c=180^\circ-35^\circ=\res{145^\circ}$. \ $b$ es opuesto por el vértice al ángulo de $35^\circ$: $b=\res{35^\circ}$."),
 (2, r"Las rectas $r$ y $s$ son paralelas y el ángulo 1 mide $58^\circ$. Calcula el resto de ángulos numerados.\par\smallskip\begin{center}" + parfig(58) + r"\end{center}",
     r"El ángulo 3 es opuesto por el vértice al 1 y los ángulos 5 y 7 son correspondientes al 1 y al 3: \ $\hat3=\hat5=\hat7=\res{58^\circ}$. \ Los ángulos 2, 4, 6 y 8 son suplementarios del 1: \ $180^\circ-58^\circ=\res{122^\circ}$."),
 (2, r"Di si es cierto o falso:" + tasks(1, [r"Dos ángulos agudos pueden ser suplementarios.", r"El suplementario de un ángulo agudo es obtuso.", r"Dos ángulos adyacentes siempre son suplementarios.", r"Un ángulo obtuso tiene complementario."]),
     tasks(1, [r"\rest{Falso}: dos ángulos agudos suman menos de $180^\circ$.", r"\rest{Cierto}: $180^\circ$ menos un ángulo agudo da más de $90^\circ$.", r"\rest{Cierto}.", r"\rest{Falso}: ya pasa de $90^\circ$."])),
 (2, r"Calcula el complementario y el suplementario del ángulo $37^\circ\,25'\,48''$.",
     r"$89^\circ\,59'\,60''-37^\circ\,25'\,48''=\res{52^\circ\,34'\,12''}$ \qquad $179^\circ\,59'\,60''-37^\circ\,25'\,48''=\res{142^\circ\,34'\,12''}$"),
 (3, r"Dos ángulos son complementarios y uno de ellos mide $20^\circ$ más que el otro. ¿Cuánto mide cada uno?",
     r"$x+(x+20)=90\ \Rightarrow\ 2x=70\ \Rightarrow\ x=35$. \ Los ángulos miden \rest{$35^\circ$ y $55^\circ$}."),
 (3, r"El suplementario de un ángulo es el cuádruple del ángulo. ¿Cuánto mide el ángulo?",
     r"$x+4x=180\ \Rightarrow\ 5x=180\ \Rightarrow\ x=\res{36^\circ}$ (el suplementario mide $144^\circ=4\cdot36^\circ$)."),
 (3, r"Dos rectas paralelas cortadas por una secante forman dos ángulos alternos internos que miden $3x+10^\circ$ y $70^\circ$. ¿Cuánto vale $x$?",
     r"Los ángulos alternos internos son iguales: $3x+10=70\ \Rightarrow\ 3x=60\ \Rightarrow\ x=\res{20^\circ}$."),
]))

# =====================================================================
# 6. Polígons: elements i classificació
# =====================================================================
CONC = [(0, 0), (2.4, 0), (2.4, 2), (1.2, 0.9), (0, 2)]
IRR = [(0, 0), (2.4, 0.3), (2.0, 1.9), (0.3, 1.5)]
F39 = [tz([('poly', reg(5, 1.1), 'gf')], 0.6), tz([('poly', CONC, 'gf')], 0.6), tz([('poly', [(0, 0), (2.8, 0), (2.8, 1.6), (0, 1.6)], 'gf')], 0.6), tz([('poly', IRR, 'gf')], 0.6)]
NOMS = {3: 'triángulo', 4: 'cuadrilátero', 5: 'pentágono', 6: 'hexágono', 7: 'heptágono', 8: 'octógono', 9: 'eneágono', 10: 'decágono', 11: 'endecágono', 12: 'dodecágono'}
CHK([diag(n) for n in (4, 5, 8, 10)] == [2, 5, 20, 35] and diag(7) == 14 and diag(9) == 27 and diag(12) == 54 and diag(3) == 0)
S_.append(("Polígonos: elementos y clasificación", [
 (1, r"Escribe el nombre del polígono que tiene:" + tasks(3, [r"5 lados", r"8 lados", r"6 lados", r"10 lados", r"7 lados", r"12 lados"]),
     tasks(3, [r"\rest{%s}" % NOMS[n] for n in (5, 8, 6, 10, 7, 12)])),
 (1, r"Para cada polígono, di cuántos lados tiene, si es convexo o cóncavo y si es regular o irregular:" + tasks(4, F39)
     + recorda(r"Un polígono es \textbf{cóncavo} si tiene algún ángulo interior de más de $180^\circ$, y \textbf{regular} si tiene todos los lados \emph{y} todos los ángulos iguales."),
     tasks(2, [r"5 lados, \rest{convexo} y \rest{regular}", r"5 lados, \rest{cóncavo} e \rest{irregular}", r"4 lados, \rest{convexo} e \rest{irregular} (rectángulo)", r"4 lados, \rest{convexo} e \rest{irregular}"])),
 (1, r"¿Cuántas diagonales salen de cada vértice y cuántas tiene en total?" + tasks(4, [r"cuadrilátero", r"pentágono", r"octógono", r"decágono"]),
     r"De cada vértice salen $n-3$ diagonales; en total, $\dfrac{n\cdot(n-3)}{2}$." + tasks(4, [r"1 y \res{2}", r"2 y \res{5}", r"5 y \res{20}", r"7 y \res{35}"])),
 (2, r"Di si es cierto o falso:" + tasks(1, [r"Un polígono regular tiene todos los lados iguales.", r"Un rombo (4 lados iguales) es un polígono regular.", r"Un polígono cóncavo tiene algún ángulo interior de más de $180^\circ$.", r"Un triángulo tiene 3 diagonales."]),
     tasks(1, [r"\rest{Cierto} (y también todos los ángulos iguales).", r"\rest{Falso}: sus ángulos no son todos iguales.", r"\rest{Cierto}.", r"\rest{Falso}: no tiene ninguna ($\frac{3\cdot0}{2}=0$)."])),
 (2, r"¿Qué polígono tiene 14 diagonales? ¿Y cuál tiene 27?",
     r"Buscamos $n$ con $n\cdot(n-3)=28$: \ $7\cdot4=28$ \ $\Rightarrow$ \rest{heptágono}. \ Con $n\cdot(n-3)=54$: \ $9\cdot6=54$ \ $\Rightarrow$ \rest{eneágono}."),
 (3, r"De cada vértice de un polígono salen 9 diagonales. ¿Cuántos lados tiene? ¿Cuántas diagonales tiene en total?",
     r"$n-3=9\ \Rightarrow\ n=\res{12}$ (dodecágono). \ En total: $\dfrac{12\cdot9}{2}=\res{54}$ diagonales."),
]))

# =====================================================================
# 7. Triangles
# =====================================================================
T45 = [(40, 60), (90, 35), (120, 25), (45, 45)]
CHK([180 - a - b for a, b in T45] == [80, 55, 35, 90])
CHK(3 + 4 > 5 and not 2 + 3 > 6 and 5 + 5 > 9 and not 4 + 4 > 8)
CHK((180 - 50) // 2 == 65 and 180 - 2 * 72 == 36 and (180 - 90) // 2 == 45)
CHK(sx(90) - sx(27, 35) == sx(62, 25))
CHK(3 * 45 + 45 == 180 and [45, 60, 75] == [45, 45 + 15, 45 + 30])
CHK(len([c for c in range(1, 30) if c < 5 + 12 and 12 < 5 + c]) == 9 and min(c for c in range(1, 30) if 12 < 5 + c) == 8 and max(c for c in range(1, 30) if c < 17) == 16)
CHK(180 - 130 == 50 and 180 - 60 - 50 == 70)
S_.append(("Triángulos", [
 (1, r"Clasifica según los lados los triángulos que tienen estas medidas (en cm):" + tasks(4, [r"5, 5, 5", r"4, 7, 7", r"3, 5, 6", r"8, 8, 3"])
     + recorda(r"Según los lados: \textbf{equilátero} (3 iguales), \textbf{isósceles} (2 iguales), \textbf{escaleno} (ninguno igual). Según los ángulos: \textbf{acutángulo}, \textbf{rectángulo} u \textbf{obtusángulo}. Los tres ángulos suman $180^\circ$."),
     tasks(4, [r"\rest{equilátero}", r"\rest{isósceles}", r"\rest{escaleno}", r"\rest{isósceles}"])),
 (1, r"Dos ángulos de un triángulo miden lo que se indica. Calcula el tercero y clasifica el triángulo según los ángulos:" + tasks(4, [r"$%d^\circ$ y $%d^\circ$" % t for t in T45]),
     tasks(2, [r"$180^\circ-100^\circ=\res{80^\circ}$, \rest{acutángulo}", r"$180^\circ-125^\circ=\res{55^\circ}$, \rest{rectángulo}", r"$180^\circ-145^\circ=\res{35^\circ}$, \rest{obtusángulo}", r"$180^\circ-90^\circ=\res{90^\circ}$, \rest{rectángulo} (e isósceles)"])),
 (1, r"¿Se puede construir un triángulo con segmentos de estas longitudes (en cm)?" + tasks(4, [r"3, 4, 5", r"2, 3, 6", r"5, 5, 9", r"4, 4, 8"]),
     r"El lado más largo tiene que ser menor que la suma de los otros dos." + tasks(4, [r"$5<7$: \rest{sí}", r"$6>5$: \rest{no}", r"$9<10$: \rest{sí}", r"$8=8$: \rest{no}"])),
 (2, r"Calcula:" + tasks(1, [r"Los ángulos de la base de un triángulo isósceles en el que el ángulo desigual mide $50^\circ$.", r"El ángulo desigual de un triángulo isósceles en el que cada ángulo de la base mide $72^\circ$.", r"Los ángulos agudos de un triángulo rectángulo isósceles."]),
     tasks(1, [r"$(180^\circ-50^\circ):2=\res{65^\circ}$ cada uno.", r"$180^\circ-2\cdot72^\circ=\res{36^\circ}$.", r"$(180^\circ-90^\circ):2=\res{45^\circ}$ cada uno."])),
 (2, r"¿Puede existir un triángulo que sea…" + tasks(2, [r"rectángulo e isósceles?", r"obtusángulo y equilátero?", r"acutángulo y escaleno?", r"rectángulo y equilátero?"]),
     tasks(2, [r"\rest{Sí}: ángulos de $90^\circ$, $45^\circ$ y $45^\circ$.", r"\rest{No}: los ángulos de un equilátero miden $60^\circ$.", r"\rest{Sí}: por ejemplo, $50^\circ$, $60^\circ$ y $70^\circ$.", r"\rest{No}: los ángulos de un equilátero miden $60^\circ$."])),
 (2, r"Un ángulo agudo de un triángulo rectángulo mide $27^\circ\,35'$. ¿Cuánto mide el otro ángulo agudo?",
     r"Los dos ángulos agudos suman $90^\circ$: \ $89^\circ\,60'-27^\circ\,35'=\res{62^\circ\,25'}$."),
 (2, r"¿Qué punto notable de un triángulo es…" + tasks(1, [r"el centro de la circunferencia que pasa por los tres vértices?", r"el punto donde se cortan las tres alturas?", r"el centro de gravedad del triángulo?", r"el punto que está a la misma distancia de los tres lados?"]),
     tasks(1, [r"El \rest{circuncentro} (corte de las mediatrices).", r"El \rest{ortocentro}.", r"El \rest{baricentro} (corte de las medianas).", r"El \rest{incentro} (corte de las bisectrices)."])),
 (3, r"Los ángulos de un triángulo miden $x$, $x+15^\circ$ y $x+30^\circ$. Calcúlalos y clasifica el triángulo.",
     r"$x+(x+15)+(x+30)=180\ \Rightarrow\ 3x+45=180\ \Rightarrow\ x=45$. \ Ángulos: \rest{$45^\circ$, $60^\circ$ y $75^\circ$}: \rest{acutángulo} y escaleno."),
 (3, r"Dos lados de un triángulo miden 5\,cm y 12\,cm. ¿Qué longitudes (en centímetros enteros) puede tener el tercer lado?",
     r"El tercer lado debe ser menor que $5+12=17$ y mayor que $12-5=7$: \ \rest{8, 9, 10, …, 16\,cm} (9 posibilidades)."),
 (3, r"Prolongamos un lado de un triángulo y, en uno de los vértices, el ángulo adyacente al interior que se forma fuera del triángulo mide $130^\circ$. Otro ángulo del triángulo mide $60^\circ$. Calcula los tres ángulos del triángulo.",
     r"El ángulo interior de ese vértice mide $180^\circ-130^\circ=50^\circ$. \ El tercero: $180^\circ-60^\circ-50^\circ=70^\circ$. \ Ángulos: \rest{$50^\circ$, $60^\circ$ y $70^\circ$}."),
]))

# =====================================================================
# 8. Quadrilàters
# =====================================================================
def qfig(V, ra=(), ticks=()):
    it = [('poly', V, 'gf')]
    for i in ra: it.append(('ra', V[i], V[i - 1], V[(i + 1) % 4]))
    for i, n in ticks: it.append(('tick', V[i], V[(i + 1) % 4], n))
    return tz(it, 0.5)
F54 = [qfig([(0, 0), (2, 0), (2, 2), (0, 2)], ra=(0, 1, 2, 3), ticks=[(0, 1), (1, 1), (2, 1), (3, 1)]), qfig([(0, 0), (1.6, -1.1), (3.2, 0), (1.6, 1.1)], ticks=[(0, 1), (1, 1), (2, 1), (3, 1)]),
       qfig([(0, 0), (3.4, 0), (2.5, 1.7), (0.9, 1.7)], ticks=[(1, 1), (3, 1)]), qfig([(0, 0), (3, 0), (3, 1.7), (0, 1.7)], ra=(0, 1, 2, 3), ticks=[(0, 1), (1, 2), (2, 1), (3, 2)]),
       qfig([(0, 0), (2.6, 0), (3.5, 1.6), (0.9, 1.6)], ticks=[(0, 1), (1, 2), (2, 1), (3, 2)]), qfig([(0, 0), (3.2, 0), (2.0, 1.8), (0, 1.8)], ra=(0, 3))]
CHK(360 - 90 - 90 - 100 == 80 and 360 - 75 - 105 - 75 == 105 and 360 - 120 - 60 - 95 == 85)
CHK(180 - 54 == 126 and 180 - 112 == 68 and 180 - 63 == 117)
CHK(10 * 36 == 360 and [36, 72, 108, 144] == [36 * k for k in (1, 2, 3, 4)] and 45 + 135 == 180 and 135 == 3 * 45)
S_.append(("Cuadriláteros", [
 (1, r"Escribe el nombre de cada cuadrilátero (las marcas indican lados iguales):" + tasks(3, F54)
     + recorda(r"\textbf{Paralelogramos} (lados opuestos paralelos): cuadrado, rectángulo, rombo y romboide. \textbf{Trapecios} (solo dos lados paralelos): rectángulo, isósceles y escaleno. \textbf{Trapezoides}: ningún lado paralelo."),
     tasks(3, [r"\rest{cuadrado}", r"\rest{rombo}", r"\rest{trapecio isósceles}", r"\rest{rectángulo}", r"\rest{romboide}", r"\rest{trapecio rectángulo}"])),
 (1, r"Tres ángulos de un cuadrilátero miden lo que se indica. Calcula el cuarto:" + tasks(3, [r"$90^\circ$, $90^\circ$, $100^\circ$", r"$75^\circ$, $105^\circ$, $75^\circ$", r"$120^\circ$, $60^\circ$, $95^\circ$"])
     + recorda(r"Los cuatro ángulos de un cuadrilátero suman $360^\circ$."),
     tasks(3, [r"$\res{80^\circ}$", r"$\res{105^\circ}$", r"$\res{85^\circ}$"])),
 (1, r"¿Qué paralelogramos tienen…" + tasks(2, [r"las diagonales iguales?", r"las diagonales perpendiculares?", r"los cuatro ángulos rectos?", r"los cuatro lados iguales?"]),
     tasks(2, [r"\rest{cuadrado y rectángulo}", r"\rest{cuadrado y rombo}", r"\rest{cuadrado y rectángulo}", r"\rest{cuadrado y rombo}"])),
 (2, r"Calcula los ángulos que faltan:" + tasks(1, [r"Un rombo con un ángulo de $54^\circ$.", r"Un romboide con un ángulo de $112^\circ$.", r"Un trapecio rectángulo con un ángulo agudo de $63^\circ$."]),
     tasks(1, [r"$\res{54^\circ,\ 126^\circ,\ 54^\circ,\ 126^\circ}$ (ángulos opuestos iguales; consecutivos suplementarios)", r"$\res{112^\circ,\ 68^\circ,\ 112^\circ,\ 68^\circ}$", r"$\res{90^\circ,\ 90^\circ,\ 63^\circ,\ 117^\circ}$ ($180^\circ-63^\circ=117^\circ$)"])),
 (2, r"Di si es cierto o falso:" + tasks(1, [r"Todo cuadrado es un rectángulo.", r"Todo rombo es un cuadrado.", r"Todo rectángulo es un paralelogramo.", r"Un trapecio puede tener tres ángulos rectos."]),
     tasks(1, [r"\rest{Cierto}: tiene los cuatro ángulos rectos.", r"\rest{Falso}: el rombo no tiene por qué tener ángulos rectos.", r"\rest{Cierto}.", r"\rest{Falso}: si tiene tres, el cuarto también mide $90^\circ$ y sería un rectángulo."])),
 (3, r"Responde:" + tasks(1, [r"Los ángulos de un cuadrilátero miden $x$, $2x$, $3x$ y $4x$. ¿Cuánto mide cada uno?", r"En un romboide, un ángulo es el triple de su consecutivo. ¿Cuánto miden los cuatro ángulos?"]),
     tasks(1, [r"$10x=360\ \Rightarrow\ x=36$: \ \rest{$36^\circ$, $72^\circ$, $108^\circ$ y $144^\circ$}.", r"Dos ángulos consecutivos suman $180^\circ$: $x+3x=180\Rightarrow x=45$. \ \rest{$45^\circ$, $135^\circ$, $45^\circ$ y $135^\circ$}."])),
]))

# =====================================================================
# 9. Angles dels polígons. Polígons regulars
# =====================================================================
R62 = [3, 4, 5, 6, 8, 10]
CHK([S(n) for n in (5, 6, 8, 10, 12)] == [540, 720, 1080, 1440, 1800])
CHK([(S(n) // n, 360 // n) for n in R62] == [(60, 120), (90, 90), (108, 72), (120, 60), (135, 45), (144, 36)] and all(S(n) % n == 0 for n in R62))
CHK(360 // 24 == 15 and S(15) // 15 == 156 and 180 - 160 == 20 and 360 // 20 == 18 and S(18) // 18 == 160 and 2340 // 180 + 2 == 15 and S(15) == 2340)
CHK(360 % 80 != 0 and 360 // 30 == 12 and 135 + 135 + 90 == 360 and 3 * 108 == 324 and 4 * 108 == 432)
S_.append(("Ángulos de los polígonos. Polígonos regulares", [
 (1, r"¿Cuánto suman los ángulos interiores de cada polígono?" + tasks(5, [r"pentágono", r"hexágono", r"octógono", r"decágono", r"dodecágono"])
     + recorda(r"Los ángulos de un polígono de $n$ lados suman $(n-2)\cdot180^\circ$. En un polígono regular, cada ángulo interior mide $\dfrac{(n-2)\cdot180^\circ}{n}$ y el ángulo central mide $\dfrac{360^\circ}{n}$."),
     tasks(5, [r"$\res{%d^\circ}$" % S(n) for n in (5, 6, 8, 10, 12)])),
 (1, r"Calcula el ángulo interior y el ángulo central de estos polígonos regulares:" + tasks(3, [r"triángulo equilátero", r"cuadrado", r"pentágono", r"hexágono", r"octógono", r"decágono"]),
     tasks(3, [r"$\res{%d^\circ}$ y $\res{%d^\circ}$" % (S(n) // n, 360 // n) for n in R62])),
 (2, r"El ángulo central de un polígono regular mide $24^\circ$. ¿Cuántos lados tiene? ¿Cuánto mide cada ángulo interior?",
     r"$n=360:24=\res{15}$ lados. \ Ángulo interior: $180^\circ-24^\circ=\res{156^\circ}$ \ (o bien $\frac{13\cdot180^\circ}{15}=156^\circ$)."),
 (2, r"Cada ángulo interior de un polígono regular mide $160^\circ$. ¿Cuántos lados tiene?",
     r"Ángulo central: $180^\circ-160^\circ=20^\circ$; \ $n=360:20=\res{18}$ lados."),
 (2, r"Los ángulos interiores de un polígono suman $2340^\circ$. ¿Cuántos lados tiene?",
     r"$(n-2)\cdot180=2340\ \Rightarrow\ n-2=13\ \Rightarrow\ n=\res{15}$ lados."),
 (3, r"¿Puede haber un polígono regular con ángulos interiores de $100^\circ$? ¿Y de $150^\circ$?",
     r"Con $100^\circ$, el ángulo central mediría $80^\circ$ y $360:80=4,5$ no es un número natural: \rest{no}. \ Con $150^\circ$: $360:30=12$: \rest{sí}, el dodecágono regular."),
 (3, r"¿Con cuáles de estos polígonos regulares se puede cubrir el suelo sin dejar huecos: triángulos, cuadrados, pentágonos, hexágonos u octógonos? ¿Y combinando octógonos y cuadrados?",
     r"Los ángulos que se encuentran en un vértice tienen que sumar $360^\circ$: \rest{triángulos} ($6\cdot60^\circ$), \rest{cuadrados} ($4\cdot90^\circ$) y \rest{hexágonos} ($3\cdot120^\circ$). Con pentágonos no ($3\cdot108^\circ=324^\circ$) ni con octógonos solos. Combinándolos, \rest{sí}: dos octógonos y un cuadrado, $135^\circ+135^\circ+90^\circ=360^\circ$."),
 (3, r"Unimos el centro de un hexágono regular con los seis vértices. ¿Qué tipo de triángulos se obtienen? Razónalo con los ángulos.",
     r"Cada ángulo central mide $360^\circ:6=60^\circ$. Los dos radios son iguales, así que los otros dos ángulos son iguales: $(180^\circ-60^\circ):2=60^\circ$. Los seis triángulos son \rest{equiláteros}."),
]))
CHK((180 - 60) // 2 == 60)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''
TIT = "Geometría básica del plano"

def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 7: %s' % (t, TIT), capcalera='%s · Unidad 7' % t,
                 pdfkeywords='punto, recta, semirrecta, segmento, rectas perpendiculares, mediatriz, ángulos, bisectriz, sistema sexagesimal, complementarios, suplementarios, polígonos, diagonales, triángulos, cuadriláteros, polígonos regulares',
                 curs='1eso')
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1eso') + '{' + ('Soluciones de la ficha · Unidad 7' if sol else 'Ficha de ejercicios · Unidad 7') + '}{' + TIT + '}\n')
    if not sol:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás una calculadora de ángulos en el sistema sexagesimal y herramientas para explorar rectas, ángulos, triángulos y polígonos."
             if sol else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Ten a mano la regla, el compás y el transportador de ángulos, y haz un dibujo siempre que te ayude.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't7-fitxa-solucions-es.tex' if sol else 't7-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios,', NCHK[0], 'comprobaciones')
