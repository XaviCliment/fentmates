# Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex
# (1r ESO, Unitat 7: Geometria bàsica del pla — punts, rectes, angles i polígons; sense àrees ni perímetres)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Els càlculs amb angles es fan en segons (sx/dms) i les asserts CHK comproven cada resultat escrit.
import os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))

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
S_.append(("Punts, rectes, semirectes i segments", [
 (1, r"Observa la figura i respon:\par\smallskip\begin{center}" + F1 + r"\end{center}" + tasks(1, [r"Quins punts són de la recta $r$? Quin punt no hi és?", r"Escriu tots els segments que tenen els extrems en dos dels punts $A$, $B$ i $C$.", r"Quantes semirectes de la recta $r$ tenen l'origen en $B$?"])
     + recorda(r"La \textbf{recta} no té principi ni final; la \textbf{semirecta} té origen però no té final; el \textbf{segment} té dos extrems i es pot mesurar. Per dos punts passa una única recta."),
     tasks(1, [r"$A$, $B$ i $C$ són de la recta $r$ (estan \rest{alineats}); $D$ \rest{no} hi és.", r"\rest{$\overline{AB}$, $\overline{AC}$ i $\overline{BC}$} (3 segments).", r"\rest{Dues}: una cap a $A$ i una altra cap a $C$."])),
 (1, r"Digues si cada figura és una recta, una semirecta o un segment:" + tasks(3, F2),
     tasks(3, [r"\rest{Recta} (dues fletxes)", r"\rest{Segment} (dos extrems)", r"\rest{Semirecta} (una fletxa)"])),
 (1, r"Respon:" + tasks(1, [r"El segment $\overline{AB}$ mesura 7\,cm i $M$ és el seu punt mitjà. Quant mesura $\overline{AM}$?", r"$M$ és el punt mitjà de $\overline{PQ}$ i $\overline{PM}$ fa 4,2\,cm. Quant mesura $\overline{PQ}$?"]),
     tasks(1, [r"$7:2=\res{3,5\text{ cm}}$", r"$2\cdot4,2=\res{8,4\text{ cm}}$"])),
 (2, r"Sobre una recta marquem quatre punts. Quants segments determinen? I si en marquem sis?",
     r"Amb 4 punts: $3+2+1=\res{6}$ segments. Amb 6 punts: $5+4+3+2+1=\res{15}$ segments."),
 (2, r"Els punts $A$, $B$ i $C$ estan sobre una recta, en aquest ordre. $\overline{AB}=5$\,cm i $\overline{BC}=3$\,cm. Quant mesura $\overline{AC}$? I si $C$ estiguera entre $A$ i $B$ (amb $\overline{BC}=3$\,cm)?",
     r"En el primer cas, $\overline{AC}=5+3=\res{8\text{ cm}}$. En el segon, $\overline{AC}=5-3=\res{2\text{ cm}}$."),
 (3, r"Dibuixem punts de manera que no n'hi ha tres d'alineats. Quantes rectes podem traçar que passen per dos d'ells si hi ha 4 punts? I 5? I 7?",
     r"De cada punt ixen tantes rectes com punts queden, i cada recta es compta dues vegades: \ $\frac{4\cdot3}{2}=\res{6}$, \ $\frac{5\cdot4}{2}=\res{10}$, \ $\frac{7\cdot6}{2}=\res{21}$."),
]))

# =====================================================================
# 2. Posicions relatives de rectes. Mediatriu
# =====================================================================
F7 = tz([('ln', (-0.4, 0), (6.4, 0), '', 'b'), ('ln', (-0.4, 1.6), (6.4, 1.6), '', 'b'), ('ln', (1.5, -0.9), (1.5, 2.6), '', 'b'), ('ln', (2.8, -0.9), (6.2, 2.6), '', 'b'), ('ra', (1.5, 0), (2.5, 0), (1.5, 1)),
         ('lab', (6.4, 0), '$r$', 'right'), ('lab', (6.4, 1.6), '$s$', 'right'), ('lab', (1.5, 2.6), '$t$', 'above'), ('lab', (6.2, 2.6), '$u$', 'above')], 0.6)
S_.append(("Posicions relatives de rectes. Mediatriu", [
 (1, r"Les rectes $r$ i $s$ són paral·leles. Digues com són:\par\smallskip\begin{center}" + F7 + r"\end{center}" + tasks(4, [r"$r$ i $s$", r"$r$ i $t$", r"$s$ i $t$", r"$r$ i $u$"])
     + recorda(r"Dues rectes són \textbf{secants} si es tallen en un punt, \textbf{paral·leles} si no es tallen mai i \textbf{perpendiculars} si es tallen formant quatre angles rectes ($r\perp s$)."),
     tasks(4, [r"\rest{paral·leles}", r"\rest{perpendiculars}", r"\rest{perpendiculars}", r"\rest{secants}"])),
 (1, r"Digues si són paral·leles, secants o perpendiculars:" + tasks(2, [r"Dos costats oposats d'un full de paper.", r"Dos costats d'un full que formen una cantonada.", r"Les agulles d'un rellotge a les 9 en punt.", r"Les agulles d'un rellotge a les 10 en punt."]),
     tasks(2, [r"\rest{Paral·leles}", r"\rest{Perpendiculars}", r"\rest{Perpendiculars} (angle de $90^\circ$)", r"\rest{Secants} (angle de $60^\circ$)"])),
 (1, r"Dibuixa un segment $\overline{AB}$ de 6\,cm i traça'n la mediatriu amb regle i compàs. A quina distància d'$A$ talla el segment?",
     r"Amb el compàs obert més de 3\,cm, traça arcs des d'$A$ i des de $B$ que es tallen per damunt i per davall del segment; la recta que unix els dos punts de tall és la mediatriu. Talla el segment en el punt mitjà, a \rest{3\,cm} d'$A$, i és perpendicular al segment."),
 (2, r"Digues si és cert o fals:" + tasks(1, [r"Dues rectes perpendiculars són sempre secants.", r"Dues rectes secants són sempre perpendiculars.", r"Si $r\parallel s$ i $s\parallel t$, aleshores $r\parallel t$.", r"Si $r\perp s$ i $s\perp t$, aleshores $r\perp t$."]),
     tasks(1, [r"\rest{Cert}: es tallen en un punt.", r"\rest{Fals}: només si formen angles rectes.", r"\rest{Cert}.", r"\rest{Fals}: $r$ i $t$ són paral·leles."])),
 (2, r"El punt $P$ està sobre la mediatriu del segment $\overline{AB}$, que mesura 8\,cm, i la distància de $P$ a $A$ és 5\,cm. Quant mesura $\overline{PB}$? A quina distància de $A$ està el punt mitjà $M$?",
     r"Els punts de la mediatriu equidisten dels extrems: $\overline{PB}=\res{5\text{ cm}}$. \ $\overline{AM}=8:2=\res{4\text{ cm}}$."),
 (3, r"Dues cases, $A$ i $B$, estan a la mateixa banda d'un camí recte. On s'ha de posar una font, vora el camí, perquè estiga a la mateixa distància de les dues cases? Explica com la trobaries.",
     r"Els punts que equidisten de $A$ i $B$ són els de la \rest{mediatriu de $\overline{AB}$}. La font ha d'estar en el \rest{punt on la mediatriu talla el camí}."),
]))

# =====================================================================
# 3. Angles
# =====================================================================
F14 = [tz(angfig(a, a0, r=3.0, R=0.6), 0.8) for a, a0 in ((40, 10), (90, 0), (140, 0), (230, 0))]
CHK([3 * 30, 4 * 30, 5 * 30, 6 * 30, 3 * 30, 1 * 30] == [90, 120, 150, 180, 90, 30])
CHK([10 * 6, 25 * 6, 60 * 6, 45 * 6] == [60, 150, 360, 270] and 136 // 2 == 68 and 2 * 43 == 86 and 360 - 125 == 235 and 360 // 5 == 72 and 360 // 8 == 45 and 180 // 15 == 12)
S_.append(("Angles: elements, mesura i classificació", [
 (1, r"Classifica aquests angles (nul, agut, recte, obtús, pla, còncau o complet):" + tasks(4, [r"$25^\circ$", r"$90^\circ$", r"$100^\circ$", r"$180^\circ$", r"$270^\circ$", r"$360^\circ$", r"$179^\circ$", r"$89^\circ$"])
     + recorda(r"Agut: menys de $90^\circ$. Recte: $90^\circ$. Obtús: entre $90^\circ$ i $180^\circ$. Pla: $180^\circ$. Còncau: més de $180^\circ$. Complet: $360^\circ$."),
     tasks(4, [r"\rest{agut}", r"\rest{recte}", r"\rest{obtús}", r"\rest{pla}", r"\rest{còncau}", r"\rest{complet}", r"\rest{obtús}", r"\rest{agut}"])),
 (1, r"Classifica cada angle i mesura'l amb el transportador:" + tasks(2, F14),
     tasks(4, [r"\rest{agut} ($40^\circ$)", r"\rest{recte} ($90^\circ$)", r"\rest{obtús} ($140^\circ$)", r"\rest{còncau} ($230^\circ$)"])),
 (1, r"Quin angle (convex) formen les agulles d'un rellotge a les hores en punt següents?" + tasks(6, [r"3 h", r"4 h", r"5 h", r"6 h", r"9 h", r"11 h"]),
     r"Entre dos nombres de l'esfera hi ha $360^\circ:12=30^\circ$." + tasks(6, [r"$\res{90^\circ}$", r"$\res{120^\circ}$", r"$\res{150^\circ}$", r"$\res{180^\circ}$", r"$\res{90^\circ}$", r"$\res{30^\circ}$"])),
 (2, r"Quants graus gira l'agulla dels minuts en aquests temps?" + tasks(4, [r"10 min", r"25 min", r"1 hora", r"tres quarts d'hora"]),
     r"Cada minut gira $360^\circ:60=6^\circ$." + tasks(4, [r"$\res{60^\circ}$", r"$\res{150^\circ}$", r"$\res{360^\circ}$", r"$45\cdot6=\res{270^\circ}$"])),
 (2, r"Respon:" + tasks(1, [r"Quins angles forma la bisectriu d'un angle de $136^\circ$ amb cadascun dels costats?", r"La bisectriu d'un angle forma amb un dels costats un angle de $43^\circ$. Quant mesura l'angle?"]),
     tasks(1, [r"$136^\circ:2=\res{68^\circ}$ cadascun.", r"$2\cdot43^\circ=\res{86^\circ}$ (agut)."])),
 (2, r"Dues semirectes amb el mateix origen formen un angle convex de $125^\circ$. Quant mesura l'angle còncau que formen?",
     r"Entre els dos fan una volta completa: $360^\circ-125^\circ=\res{235^\circ}$."),
 (3, r"Respon:" + tasks(1, [r"Dividim un angle complet en 5 angles iguals. Quant mesura cadascun? I si el dividim en 8?", r"Quantes vegades cap un angle de $15^\circ$ en un angle pla?"]),
     tasks(1, [r"$360^\circ:5=\res{72^\circ}$; \ $360^\circ:8=\res{45^\circ}$.", r"$180:15=\res{12}$ vegades."])),
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
S_.append(("Mesura d'angles: el sistema sexagesimal", [
 (1, r"Expressa en segons:" + tasks(3, [r"$%s$" % A(sx(*e)) if e != (0, 45, 30) else r"$45'\,30''$" for e in E20])
     + recorda(r"$1^\circ=60'$, \ $1'=60''$, \ $1^\circ=3600''$. Per a passar a una unitat més menuda multipliquem; per a passar a una unitat més gran dividim entre 60."),
     tasks(3, [r"$\res{%d''}$" % r for r in R20])),
 (1, r"Expressa en minuts:" + tasks(4, [r"$5^\circ$", r"$2^\circ\,30'$", r"$12^\circ\,45'$", r"$180^\circ$"]),
     tasks(4, [r"$\res{%d'}$" % r if r < 10000 else r"$\res{10\,800'}$" for r in R21])),
 (1, r"Passa a forma complexa (graus, minuts i segons):" + tasks(3, [r"$%s$" % e for e, _, _ in E22]),
     r"Dividim entre 60 tantes vegades com calga: per exemple, $4000'':60=66'$ i sobren $40''$; $66':60=1^\circ$ i sobren $6'$." + tasks(3, [r"$\res{%s}$" % w for _, _, w in E22])),
 (2, r"Expressa en graus i minuts:" + tasks(4, [r"$%s^\circ$" % v for v, _, _ in E23]),
     r"La part decimal dels graus es multiplica per 60: $0,5^\circ=30'$, \ $0,25^\circ=15'$, \ $0,75^\circ=45'$, \ $0,1^\circ=6'$." + tasks(4, [r"$\res{%s}$" % w for _, _, w in E23])),
 (2, r"Calcula:" + ops(0, 3)[0], ops(0, 3)[1]),
 (2, r"Calcula:" + ops(3, 6)[0], r"Quan no es pot restar, convertim $1^\circ$ en $60'$ o $1'$ en $60''$." + ops(3, 6)[1]),
 (2, r"Calcula:" + ops(6, 9)[0], ops(6, 9)[1]),
 (3, r"Calcula i comprova el resultat multiplicant:" + ops(9, 12)[0],
     ops(9, 12)[1] + r"Comprovació del primer: $(18^\circ\,54')\cdot4=72^\circ\,216'=75^\circ\,36'$ \checkmark"),
 (3, r"La Terra fa una volta completa sobre ella mateixa en 24 hores. Quants graus gira en 1 hora? I en 1 minut? I en 1 segon?",
     r"En 1 hora: $360^\circ:24=\res{15^\circ}$. En 1 minut: $15^\circ:60=900':60=\res{15'}$. En 1 segon: $15':60=900'':60=\res{15''}$."),
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
S_.append(("Relacions entre angles", [
 (1, r"Calcula el complementari de cada angle:" + tasks(4, [r"$%s$" % A(a) for a, _ in CT])
     + recorda(r"Dos angles són \textbf{complementaris} si sumen $90^\circ$ i \textbf{suplementaris} si sumen $180^\circ$. Els angles \textbf{oposats pel vèrtex} són iguals i els \textbf{adjacents} sumen $180^\circ$."),
     tasks(4, [r"$\res{%s}$" % eqA(c, A(c)) for _, c in CT])),
 (1, r"Calcula el suplementari de cada angle:" + tasks(4, [r"$%s$" % A(a) for a, _ in ST_]),
     tasks(4, [r"$\res{%s}$" % eqA(c, A(c)) for _, c in ST_])),
 (1, r"Dues rectes es tallen i un dels angles fa $35^\circ$. Calcula els angles $a$, $b$ i $c$ i explica com els has trobat.\par\smallskip\begin{center}" + F31 + r"\end{center}",
     r"$a$ i $c$ són adjacents a l'angle de $35^\circ$: $a=c=180^\circ-35^\circ=\res{145^\circ}$. \ $b$ és oposat pel vèrtex a l'angle de $35^\circ$: $b=\res{35^\circ}$."),
 (2, r"Les rectes $r$ i $s$ són paral·leles i l'angle 1 fa $58^\circ$. Calcula la resta d'angles numerats.\par\smallskip\begin{center}" + parfig(58) + r"\end{center}",
     r"L'angle 3 és oposat pel vèrtex a l'1 i els angles 5 i 7 són corresponents a l'1 i al 3: \ $\hat3=\hat5=\hat7=\res{58^\circ}$. \ Els angles 2, 4, 6 i 8 són suplementaris de l'1: \ $180^\circ-58^\circ=\res{122^\circ}$."),
 (2, r"Digues si és cert o fals:" + tasks(1, [r"Dos angles aguts poden ser suplementaris.", r"El suplementari d'un angle agut és obtús.", r"Dos angles adjacents sempre són suplementaris.", r"Un angle obtús té complementari."]),
     tasks(1, [r"\rest{Fals}: dos angles aguts sumen menys de $180^\circ$.", r"\rest{Cert}: $180^\circ$ menys un angle agut fa més de $90^\circ$.", r"\rest{Cert}.", r"\rest{Fals}: ja passa de $90^\circ$."])),
 (2, r"Calcula el complementari i el suplementari de l'angle $37^\circ\,25'\,48''$.",
     r"$89^\circ\,59'\,60''-37^\circ\,25'\,48''=\res{52^\circ\,34'\,12''}$ \qquad $179^\circ\,59'\,60''-37^\circ\,25'\,48''=\res{142^\circ\,34'\,12''}$"),
 (3, r"Dos angles són complementaris i un d'ells mesura $20^\circ$ més que l'altre. Quant mesura cadascun?",
     r"$x+(x+20)=90\ \Rightarrow\ 2x=70\ \Rightarrow\ x=35$. \ Els angles mesuren \rest{$35^\circ$ i $55^\circ$}."),
 (3, r"El suplementari d'un angle és el quàdruple de l'angle. Quant mesura l'angle?",
     r"$x+4x=180\ \Rightarrow\ 5x=180\ \Rightarrow\ x=\res{36^\circ}$ (el suplementari fa $144^\circ=4\cdot36^\circ$)."),
 (3, r"Dues rectes paral·leles tallades per una secant formen dos angles alterns interns que mesuren $3x+10^\circ$ i $70^\circ$. Quant val $x$?",
     r"Els angles alterns interns són iguals: $3x+10=70\ \Rightarrow\ 3x=60\ \Rightarrow\ x=\res{20^\circ}$."),
]))

# =====================================================================
# 6. Polígons: elements i classificació
# =====================================================================
CONC = [(0, 0), (2.4, 0), (2.4, 2), (1.2, 0.9), (0, 2)]
IRR = [(0, 0), (2.4, 0.3), (2.0, 1.9), (0.3, 1.5)]
F39 = [tz([('poly', reg(5, 1.1), 'gf')], 0.6), tz([('poly', CONC, 'gf')], 0.6), tz([('poly', [(0, 0), (2.8, 0), (2.8, 1.6), (0, 1.6)], 'gf')], 0.6), tz([('poly', IRR, 'gf')], 0.6)]
NOMS = {3: 'triangle', 4: 'quadrilàter', 5: 'pentàgon', 6: 'hexàgon', 7: 'heptàgon', 8: 'octàgon', 9: 'enneàgon', 10: 'decàgon', 11: 'endecàgon', 12: 'dodecàgon'}
CHK([diag(n) for n in (4, 5, 8, 10)] == [2, 5, 20, 35] and diag(7) == 14 and diag(9) == 27 and diag(12) == 54 and diag(3) == 0)
S_.append(("Polígons: elements i classificació", [
 (1, r"Escriu el nom del polígon que té:" + tasks(3, [r"5 costats", r"8 costats", r"6 costats", r"10 costats", r"7 costats", r"12 costats"]),
     tasks(3, [r"\rest{%s}" % NOMS[n] for n in (5, 8, 6, 10, 7, 12)])),
 (1, r"Per a cada polígon, digues quants costats té, si és convex o còncau i si és regular o irregular:" + tasks(4, F39)
     + recorda(r"Un polígon és \textbf{còncau} si té algun angle interior de més de $180^\circ$, i \textbf{regular} si té tots els costats \emph{i} tots els angles iguals."),
     tasks(2, [r"5 costats, \rest{convex} i \rest{regular}", r"5 costats, \rest{còncau} i \rest{irregular}", r"4 costats, \rest{convex} i \rest{irregular} (rectangle)", r"4 costats, \rest{convex} i \rest{irregular}"])),
 (1, r"Quantes diagonals ixen de cada vèrtex i quantes en té en total?" + tasks(4, [r"quadrilàter", r"pentàgon", r"octàgon", r"decàgon"]),
     r"De cada vèrtex ixen $n-3$ diagonals; en total, $\dfrac{n\cdot(n-3)}{2}$." + tasks(4, [r"1 i \res{2}", r"2 i \res{5}", r"5 i \res{20}", r"7 i \res{35}"])),
 (2, r"Digues si és cert o fals:" + tasks(1, [r"Un polígon regular té tots els costats iguals.", r"Un rombe (4 costats iguals) és un polígon regular.", r"Un polígon còncau té algun angle interior de més de $180^\circ$.", r"Un triangle té 3 diagonals."]),
     tasks(1, [r"\rest{Cert} (i també tots els angles iguals).", r"\rest{Fals}: els seus angles no són tots iguals.", r"\rest{Cert}.", r"\rest{Fals}: no en té cap ($\frac{3\cdot0}{2}=0$)."])),
 (2, r"Quin polígon té 14 diagonals? I quin en té 27?",
     r"Busquem $n$ amb $n\cdot(n-3)=28$: \ $7\cdot4=28$ \ $\Rightarrow$ \rest{heptàgon}. \ Amb $n\cdot(n-3)=54$: \ $9\cdot6=54$ \ $\Rightarrow$ \rest{enneàgon}."),
 (3, r"De cada vèrtex d'un polígon ixen 9 diagonals. Quants costats té? Quantes diagonals té en total?",
     r"$n-3=9\ \Rightarrow\ n=\res{12}$ (dodecàgon). \ En total: $\dfrac{12\cdot9}{2}=\res{54}$ diagonals."),
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
S_.append(("Triangles", [
 (1, r"Classifica segons els costats els triangles que tenen aquestes mesures (en cm):" + tasks(4, [r"5, 5, 5", r"4, 7, 7", r"3, 5, 6", r"8, 8, 3"])
     + recorda(r"Segons els costats: \textbf{equilàter} (3 iguals), \textbf{isòsceles} (2 iguals), \textbf{escalé} (cap igual). Segons els angles: \textbf{acutangle}, \textbf{rectangle} o \textbf{obtusangle}. Els tres angles sumen $180^\circ$."),
     tasks(4, [r"\rest{equilàter}", r"\rest{isòsceles}", r"\rest{escalé}", r"\rest{isòsceles}"])),
 (1, r"Dos angles d'un triangle mesuren el que s'indica. Calcula el tercer i classifica el triangle segons els angles:" + tasks(4, [r"$%d^\circ$ i $%d^\circ$" % t for t in T45]),
     tasks(2, [r"$180^\circ-100^\circ=\res{80^\circ}$, \rest{acutangle}", r"$180^\circ-125^\circ=\res{55^\circ}$, \rest{rectangle}", r"$180^\circ-145^\circ=\res{35^\circ}$, \rest{obtusangle}", r"$180^\circ-90^\circ=\res{90^\circ}$, \rest{rectangle} (i isòsceles)"])),
 (1, r"Es pot construir un triangle amb segments d'aquestes longituds (en cm)?" + tasks(4, [r"3, 4, 5", r"2, 3, 6", r"5, 5, 9", r"4, 4, 8"]),
     r"El costat més llarg ha de ser més menut que la suma dels altres dos." + tasks(4, [r"$5<7$: \rest{sí}", r"$6>5$: \rest{no}", r"$9<10$: \rest{sí}", r"$8=8$: \rest{no}"])),
 (2, r"Calcula:" + tasks(1, [r"Els angles de la base d'un triangle isòsceles en què l'angle desigual fa $50^\circ$.", r"L'angle desigual d'un triangle isòsceles en què cada angle de la base fa $72^\circ$.", r"Els angles aguts d'un triangle rectangle isòsceles."]),
     tasks(1, [r"$(180^\circ-50^\circ):2=\res{65^\circ}$ cadascun.", r"$180^\circ-2\cdot72^\circ=\res{36^\circ}$.", r"$(180^\circ-90^\circ):2=\res{45^\circ}$ cadascun."])),
 (2, r"Pot existir un triangle que siga…" + tasks(2, [r"rectangle i isòsceles?", r"obtusangle i equilàter?", r"acutangle i escalé?", r"rectangle i equilàter?"]),
     tasks(2, [r"\rest{Sí}: angles de $90^\circ$, $45^\circ$ i $45^\circ$.", r"\rest{No}: els angles d'un equilàter fan $60^\circ$.", r"\rest{Sí}: per exemple, $50^\circ$, $60^\circ$ i $70^\circ$.", r"\rest{No}: els angles d'un equilàter fan $60^\circ$."])),
 (2, r"Un angle agut d'un triangle rectangle mesura $27^\circ\,35'$. Quant mesura l'altre angle agut?",
     r"Els dos angles aguts sumen $90^\circ$: \ $89^\circ\,60'-27^\circ\,35'=\res{62^\circ\,25'}$."),
 (2, r"Quin punt notable d'un triangle és…" + tasks(1, [r"el centre de la circumferència que passa pels tres vèrtexs?", r"el punt on es tallen les tres altures?", r"el centre de gravetat del triangle?", r"el punt que està a la mateixa distància dels tres costats?"]),
     tasks(1, [r"El \rest{circumcentre} (tall de les mediatrius).", r"L'\rest{ortocentre}.", r"El \rest{baricentre} (tall de les mitjanes).", r"L'\rest{incentre} (tall de les bisectrius)."])),
 (3, r"Els angles d'un triangle mesuren $x$, $x+15^\circ$ i $x+30^\circ$. Calcula'ls i classifica el triangle.",
     r"$x+(x+15)+(x+30)=180\ \Rightarrow\ 3x+45=180\ \Rightarrow\ x=45$. \ Angles: \rest{$45^\circ$, $60^\circ$ i $75^\circ$}: \rest{acutangle} i escalé."),
 (3, r"Dos costats d'un triangle mesuren 5\,cm i 12\,cm. Quines longituds (en centímetres sencers) pot tindre el tercer costat?",
     r"El tercer costat ha de ser més menut que $5+12=17$ i més gran que $12-5=7$: \ \rest{8, 9, 10, …, 16\,cm} (9 possibilitats)."),
 (3, r"Prolonguem un costat d'un triangle i, en un vèrtex, l'angle interior i l'angle adjacent que es forma fora del triangle fan $130^\circ$ (l'adjacent). Un altre angle del triangle fa $60^\circ$. Calcula els tres angles del triangle.",
     r"L'angle adjacent fa $180^\circ-130^\circ=50^\circ$. \ El tercer: $180^\circ-60^\circ-50^\circ=70^\circ$. \ Angles: \rest{$50^\circ$, $60^\circ$ i $70^\circ$}."),
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
S_.append(("Quadrilàters", [
 (1, r"Escriu el nom de cada quadrilàter (les marques indiquen costats iguals):" + tasks(3, F54)
     + recorda(r"\textbf{Paral·lelograms} (costats oposats paral·lels): quadrat, rectangle, rombe i romboide. \textbf{Trapezis} (només dos costats paral·lels): rectangle, isòsceles i escalé. \textbf{Trapezoides}: cap costat paral·lel."),
     tasks(3, [r"\rest{quadrat}", r"\rest{rombe}", r"\rest{trapezi isòsceles}", r"\rest{rectangle}", r"\rest{romboide}", r"\rest{trapezi rectangle}"])),
 (1, r"Tres angles d'un quadrilàter mesuren el que s'indica. Calcula el quart:" + tasks(3, [r"$90^\circ$, $90^\circ$, $100^\circ$", r"$75^\circ$, $105^\circ$, $75^\circ$", r"$120^\circ$, $60^\circ$, $95^\circ$"])
     + recorda(r"Els quatre angles d'un quadrilàter sumen $360^\circ$."),
     tasks(3, [r"$\res{80^\circ}$", r"$\res{105^\circ}$", r"$\res{85^\circ}$"])),
 (1, r"Quins paral·lelograms tenen…" + tasks(2, [r"les diagonals iguals?", r"les diagonals perpendiculars?", r"els quatre angles rectes?", r"els quatre costats iguals?"]),
     tasks(2, [r"\rest{quadrat i rectangle}", r"\rest{quadrat i rombe}", r"\rest{quadrat i rectangle}", r"\rest{quadrat i rombe}"])),
 (2, r"Calcula els angles que falten:" + tasks(1, [r"Un rombe amb un angle de $54^\circ$.", r"Un romboide amb un angle de $112^\circ$.", r"Un trapezi rectangle amb un angle agut de $63^\circ$."]),
     tasks(1, [r"$\res{54^\circ,\ 126^\circ,\ 54^\circ,\ 126^\circ}$ (angles oposats iguals; consecutius suplementaris)", r"$\res{112^\circ,\ 68^\circ,\ 112^\circ,\ 68^\circ}$", r"$\res{90^\circ,\ 90^\circ,\ 63^\circ,\ 117^\circ}$ ($180^\circ-63^\circ=117^\circ$)"])),
 (2, r"Digues si és cert o fals:" + tasks(1, [r"Tot quadrat és un rectangle.", r"Tot rombe és un quadrat.", r"Tot rectangle és un paral·lelogram.", r"Un trapezi pot tindre tres angles rectes."]),
     tasks(1, [r"\rest{Cert}: té els quatre angles rectes.", r"\rest{Fals}: el rombe no té per què tindre angles rectes.", r"\rest{Cert}.", r"\rest{Fals}: si en té tres, el quart també fa $90^\circ$ i seria un rectangle."])),
 (3, r"Respon:" + tasks(1, [r"Els angles d'un quadrilàter mesuren $x$, $2x$, $3x$ i $4x$. Quant mesura cadascun?", r"En un romboide, un angle és el triple del seu consecutiu. Quant mesuren els quatre angles?"]),
     tasks(1, [r"$10x=360\ \Rightarrow\ x=36$: \ \rest{$36^\circ$, $72^\circ$, $108^\circ$ i $144^\circ$}.", r"Dos angles consecutius sumen $180^\circ$: $x+3x=180\Rightarrow x=45$. \ \rest{$45^\circ$, $135^\circ$, $45^\circ$ i $135^\circ$}."])),
]))

# =====================================================================
# 9. Angles dels polígons. Polígons regulars
# =====================================================================
R62 = [3, 4, 5, 6, 8, 10]
CHK([S(n) for n in (5, 6, 8, 10, 12)] == [540, 720, 1080, 1440, 1800])
CHK([(S(n) // n, 360 // n) for n in R62] == [(60, 120), (90, 90), (108, 72), (120, 60), (135, 45), (144, 36)] and all(S(n) % n == 0 for n in R62))
CHK(360 // 24 == 15 and S(15) // 15 == 156 and 180 - 160 == 20 and 360 // 20 == 18 and S(18) // 18 == 160 and 2340 // 180 + 2 == 15 and S(15) == 2340)
CHK(360 % 80 != 0 and 360 // 30 == 12 and 135 + 135 + 90 == 360 and 3 * 108 == 324 and 4 * 108 == 432)
S_.append(("Angles dels polígons. Polígons regulars", [
 (1, r"Quant sumen els angles interiors de cada polígon?" + tasks(5, [r"pentàgon", r"hexàgon", r"octàgon", r"decàgon", r"dodecàgon"])
     + recorda(r"Els angles d'un polígon de $n$ costats sumen $(n-2)\cdot180^\circ$. En un polígon regular, cada angle interior fa $\dfrac{(n-2)\cdot180^\circ}{n}$ i l'angle central fa $\dfrac{360^\circ}{n}$."),
     tasks(5, [r"$\res{%d^\circ}$" % S(n) for n in (5, 6, 8, 10, 12)])),
 (1, r"Calcula l'angle interior i l'angle central d'aquests polígons regulars:" + tasks(3, [r"triangle equilàter", r"quadrat", r"pentàgon", r"hexàgon", r"octàgon", r"decàgon"]),
     tasks(3, [r"$\res{%d^\circ}$ i $\res{%d^\circ}$" % (S(n) // n, 360 // n) for n in R62])),
 (2, r"L'angle central d'un polígon regular mesura $24^\circ$. Quants costats té? Quant mesura cada angle interior?",
     r"$n=360:24=\res{15}$ costats. \ Angle interior: $180^\circ-24^\circ=\res{156^\circ}$ \ (o bé $\frac{13\cdot180^\circ}{15}=156^\circ$)."),
 (2, r"Cada angle interior d'un polígon regular mesura $160^\circ$. Quants costats té?",
     r"Angle central: $180^\circ-160^\circ=20^\circ$; \ $n=360:20=\res{18}$ costats."),
 (2, r"Els angles interiors d'un polígon sumen $2340^\circ$. Quants costats té?",
     r"$(n-2)\cdot180=2340\ \Rightarrow\ n-2=13\ \Rightarrow\ n=\res{15}$ costats."),
 (3, r"Pot haver-hi un polígon regular amb angles interiors de $100^\circ$? I de $150^\circ$?",
     r"Amb $100^\circ$, l'angle central faria $80^\circ$ i $360:80=4,5$ no és un nombre natural: \rest{no}. \ Amb $150^\circ$: $360:30=12$: \rest{sí}, el dodecàgon regular."),
 (3, r"Amb quins d'aquests polígons regulars es pot cobrir el terra sense deixar buits: triangles, quadrats, pentàgons, hexàgons o octàgons? I combinant octàgons i quadrats?",
     r"Els angles que es troben en un vèrtex han de sumar $360^\circ$: \rest{triangles} ($6\cdot60^\circ$), \rest{quadrats} ($4\cdot90^\circ$) i \rest{hexàgons} ($3\cdot120^\circ$). Amb pentàgons no ($3\cdot108^\circ=324^\circ$) ni amb octàgons sols. Combinant-los, \rest{sí}: dos octàgons i un quadrat, $135^\circ+135^\circ+90^\circ=360^\circ$."),
 (3, r"Unim el centre d'un hexàgon regular amb els sis vèrtexs. Quina mena de triangles s'obtenen? Raona-ho amb els angles.",
     r"Cada angle central fa $360^\circ:6=60^\circ$. Els dos radis són iguals, així que els altres dos angles són iguals: $(180^\circ-60^\circ):2=60^\circ$. Els sis triangles són \rest{equilàters}."),
]))
CHK((180 - 60) // 2 == 60)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
KW = 'pdfkeywords={punt, recta, semirecta, segment, rectes perpendiculars, mediatriu, angles, bisectriu, sistema sexagesimal, complementaris, suplementaris, polígons, diagonals, triangles, quadrilàters, polígons regulars}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 1r ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
TIT = "Geometria bàsica del pla"

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 7: %s. 1r d'ESO}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 7 · 1r d'ESO" % t)
    assert 'Unitat 7' in p and 'unitat 7' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{1r ESO}{''' + ('Solucions de la fitxa · Unitat 7' if sol else "Fitxa d'exercicis · Unitat 7") + r'''}{''' + TIT + r'''}
''')
    if not sol:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs una calculadora d'angles en el sistema sexagesimal i eines per a explorar rectes, angles, triangles i polígons."
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Tin a mà el regle, el compàs i el transportador d'angles, i fes un dibuix sempre que t'ajude.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't7-fitxa-solucions.tex' if sol else 't7-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis,', NCHK[0], 'comprovacions')
