# Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex
# (1r ESO, Unitat 8: Àrees i perímetres — unitats de mesura, polígons, circumferència, cercle, figures compostes i teorema de Pitàgores)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Els càlculs amb π es fan amb π ≈ 3,14 (P3). Les comprovacions N() i CHK verifiquen cada resultat escrit.
import os, re, math
from decimal import Decimal as Dm
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- comprovacions ----------
NCHK = [0]
def CHK(cond, *info):
    NCHK[0] += 1
    assert cond, info
P3 = Dm('3.14')
def d(x): return x if isinstance(x, Dm) else Dm(str(x))
def N(v, txt, dec=None):
    """v: valor calculat; txt: el que escrivim («3,14», «35\\,000»). dec: decimals de l'arrodoniment (None = exacte)"""
    w = Dm(txt.replace('\\,', '').replace('{,}', '.').replace(',', '.'))
    v = d(v)
    CHK(v == w if dec is None else abs(v - w) <= Dm('0.5') * Dm(10) ** -dec, v, txt)
    return txt
def cellper(cs):
    S = set(cs)
    return sum(1 for x, y in cs for e in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + e[0], y + e[1]) not in S)
def shoelace(V): return abs(sum(V[i][0] * V[(i + 1) % len(V)][1] - V[(i + 1) % len(V)][0] * V[i][1] for i in range(len(V)))) / 2

# ---------- figures (TikZ) ----------
ST = {'': 'thick', 'gf': 'fill=teal!12,draw=teal,thick', 'sh': 'fill=accent!22,draw=accent,thick', 'sht': 'fill=accent,fill opacity=0.22,draw=accent,thick', 'tl': 'fill=accent!8,draw=accent!60', 'hole': 'fill=white,draw=teal,thick',
      'lawn': 'fill=green!18,draw=green!50!black,thick', 'd': 'dashed,muted', 'hl': 'accent,very thick', 'gc': 'draw=teal,thick', 'grid': 'muted!80,line width=0.5pt,step=1', 'frame': 'thick,muted'}
def P_(p): return '(%.3f,%.3f)' % (float(p[0]), float(p[1]))
def pol(C, r, a): return (C[0] + r * math.cos(math.radians(a)), C[1] + r * math.sin(math.radians(a)))
def reg(n, r=1, rot=None):
    rot = -90 - 180 / n if rot is None else rot
    return [pol((0, 0), r, rot + 360 * k / n) for k in range(n)]
def mid(A, B): return ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
def tz(items, s=0.5):
    o = [r'\begin{tikzpicture}[x=%scm,y=%scm,baseline=(current bounding box.center),line join=round,line cap=round]' % (s, s)]
    for it in items:
        k = it[0]
        if k == 'poly': o.append(r'\draw[%s] %s -- cycle;' % (ST[it[2]], ' -- '.join(P_(p) for p in it[1])))
        elif k == 'seg': o.append(r'\draw[%s] %s -- %s;' % (ST[it[3] if len(it) > 3 else ''], P_(it[1]), P_(it[2])))
        elif k == 'grid': o.append(r'\draw[%s] %s grid %s;' % (ST['grid'], P_(it[1]), P_(it[2])))
        elif k == 'cells':
            for x, y in it[1]: o.append(r'\fill[teal!25] (%d,%d) rectangle (%d,%d);' % (x, y, x + 1, y + 1))
        elif k == 'circ': o.append(r'\draw[%s] %s circle (%s);' % (ST[it[3] if len(it) > 3 else 'gc'], P_(it[1]), it[2]))
        elif k == 'sect':
            C, r, a0, a1 = it[1], it[2], it[3], it[4]
            o.append(r'\draw[%s] %s -- %s arc[start angle=%s,end angle=%s,radius=%s] -- cycle;' % (ST[it[5] if len(it) > 5 else 'sh'], P_(C), P_(pol(C, r, a0)), a0, a1, r))
        elif k == 'arc':
            C, r, a0, a1 = it[1], it[2], it[3], it[4]
            o.append(r'\draw[%s] %s arc[start angle=%s,end angle=%s,radius=%s];' % (ST[it[5] if len(it) > 5 else ''], P_(pol(C, r, a0)), a0, a1, r))
        elif k == 'ra':
            V, A_, B = it[1], it[2], it[3]; q = 0.22 / s
            def u(Pp):
                dx, dy = Pp[0] - V[0], Pp[1] - V[1]; n = math.hypot(dx, dy); return dx / n * q, dy / n * q
            ua, ub = u(A_), u(B)
            o.append(r'\draw[thin] %s -- %s -- %s;' % (P_((V[0] + ua[0], V[1] + ua[1])), P_((V[0] + ua[0] + ub[0], V[1] + ua[1] + ub[1])), P_((V[0] + ub[0], V[1] + ub[1]))))
        elif k == 'lab': o.append(r'\node[font=\small,%s] at %s {%s};' % (it[3] if len(it) > 3 else 'inner sep=1pt', P_(it[1]), it[2]))
        elif k == 'dot': o.append(r'\fill %s circle (1.5pt);' % P_(it[1]))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def cellfig(cs, w, h, s=0.55): return tz([('cells', cs), ('grid', (0, 0), (w, h))] + bound(cs), s)
def bound(cs):
    S = set(cs); it = []
    for x, y in cs:
        if (x, y - 1) not in S: it.append(('seg', (x, y), (x + 1, y), ''))
        if (x, y + 1) not in S: it.append(('seg', (x, y + 1), (x + 1, y + 1), ''))
        if (x - 1, y) not in S: it.append(('seg', (x, y), (x, y + 1), ''))
        if (x + 1, y) not in S: it.append(('seg', (x + 1, y), (x + 1, y + 1), ''))
    return it
def center(t): return r'\par\smallskip\begin{center}' + t + r'\end{center}'

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Perímetre i àrea. Unitats de mesura
# =====================================================================
C1 = [[(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)], [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (0, 1)], [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]]
R1 = [(6, 10), (7, 16), (5, 12)]
for c, (a, p) in zip(C1, R1): CHK(len(c) == a and cellper(c) == p, c)
F1 = [cellfig(C1[0], 3, 2), cellfig(C1[1], 4, 3), cellfig(C1[2], 3, 3)]
for v, t in [(Dm('4.7') * 1000, '4700'), (Dm(380) / 100, '3,8'), (Dm(25) / 10, '2,5'), (Dm(9) * 100, '900'), (Dm(1250) / 1000, '1,25')]: N(v, t)
for v, t in [(Dm('3.2') * 100, '320'), (Dm(45) / 10, '4,5'), (Dm('0.8') * 100, '80'), (Dm(760) / 1000, '0,76')]: N(v, t)
for v, t in [(Dm(5) * 100, '500'), (Dm('2.4') * 100, '240'), (Dm(35000) / 10000, '3,5'), (Dm('0.7') * 10000, '7000'), (Dm(8) * 100, '800')]: N(v, t)
for v, t in [(Dm('3.5') * 10000, '35\\,000'), (Dm(4500) / 10000, '0,45'), (Dm(12) * 100, '1200'), (Dm('0.25') * 100, '25')]: N(v, t)
CHK(sorted([50000, 40000, 52000, 48000]) == [40000, 48000, 50000, 52000])
N(Dm('2.4') * 10000 * 18, '432\\,000')
CHK([a * (10 - a) for a in range(1, 6)] == [9, 16, 21, 24, 25])
S_.append(("Perímetre i àrea. Unitats de mesura", [
 (1, r"Cada quadret fa 1\,cm de costat. Calcula l'àrea i el perímetre de cada figura:" + tasks(3, F1)
     + recorda(r"El \textbf{perímetre} és la longitud del contorn (cm, m…) i l'\textbf{àrea} és la superfície que ocupa la figura (cm$^2$, m$^2$…). En una quadrícula, l'àrea és el nombre de quadrets i el perímetre, el nombre de costats de quadret del contorn."),
     tasks(3, [r"$A=\res{%d\text{ cm}^2}$, $P=\res{%d\text{ cm}}$" % ap for ap in R1])),
 (1, r"Expressa en metres:" + tasks(5, [r"4,7\,km", r"380\,cm", r"25\,dm", r"9\,hm", r"1250\,mm"])
     + recorda(r"Les unitats de longitud van de 10 en 10: km, hm, dam, m, dm, cm, mm. Per a passar a una unitat més menuda multipliquem i per a passar a una més gran dividim."),
     tasks(5, [r"$\res{4700\text{ m}}$", r"$\res{3,8\text{ m}}$", r"$\res{2,5\text{ m}}$", r"$\res{900\text{ m}}$", r"$\res{1,25\text{ m}}$"])),
 (1, r"Fes els canvis d'unitats:" + tasks(4, [r"3,2\,m a cm", r"45\,mm a cm", r"0,8\,km a dam", r"760\,dm a hm"]),
     tasks(4, [r"$\res{320\text{ cm}}$", r"$\res{4,5\text{ cm}}$", r"$\res{80\text{ dam}}$", r"$\res{0,76\text{ hm}}$"])),
 (1, r"Fes els canvis d'unitats de superfície:" + tasks(3, [r"5\,dm$^2$ a cm$^2$", r"2,4\,m$^2$ a dm$^2$", r"35\,000\,cm$^2$ a m$^2$", r"0,7\,hm$^2$ a m$^2$", r"8\,km$^2$ a hm$^2$"])
     + recorda(r"Les unitats de superfície van de 100 en 100: \ $1\text{ m}^2=100\text{ dm}^2=10\,000\text{ cm}^2$."),
     tasks(3, [r"$\res{500\text{ cm}^2}$", r"$\res{240\text{ dm}^2}$", r"$\res{3,5\text{ m}^2}$", r"$\res{7000\text{ m}^2}$", r"$\res{800\text{ hm}^2}$"])),
 (2, r"Fes els canvis amb unitats agràries ($1\text{ ha}=1\text{ hm}^2$, \ $1\text{ a}=1\text{ dam}^2$):" + tasks(4, [r"3,5\,ha a m$^2$", r"4500\,m$^2$ a ha", r"12\,a a m$^2$", r"0,25\,km$^2$ a ha"]),
     tasks(4, [r"$\res{35\,000\text{ m}^2}$", r"$\res{0,45\text{ ha}}$", r"$\res{1200\text{ m}^2}$", r"$\res{25\text{ ha}}$"])),
 (2, r"Ordena de menor a major: \ $0,05\text{ km}^2$, \ $4\text{ ha}$, \ $520\text{ dam}^2$, \ $48\,000\text{ m}^2$.",
     r"Ho passem tot a m$^2$: $50\,000$, $40\,000$, $52\,000$ i $48\,000$. \ \rest{$4\text{ ha}<48\,000\text{ m}^2<0,05\text{ km}^2<520\text{ dam}^2$}"),
 (2, r"Una finca de 2,4\,ha es ven a 18\,€ el metre quadrat. Quant costa?",
     r"$2,4\text{ ha}=24\,000\text{ m}^2$; \ $24\,000\cdot18=\res{432\,000\text{ €}}$"),
 (3, r"Volem fer rectangles de 20\,cm de perímetre amb costats que siguen nombres naturals. Escriu-los tots i calcula'n l'àrea. Quin té l'àrea més gran?",
     r"La base i l'altura sumen 10: \ $1\times9$ ($A=9$), $2\times8$ ($A=16$), $3\times7$ ($A=21$), $4\times6$ ($A=24$) i $5\times5$ ($A=25$). L'àrea més gran és la del \rest{quadrat de 5\,cm}: $25\text{ cm}^2$."),
]))

# =====================================================================
# 2. Perímetre dels polígons
# =====================================================================
N(Dm('7.5') + 9 + 11, '27,5'); N(4 * Dm('8.5'), '34'); N(2 * 15 + 2 * 9, '48'); N(4 * Dm('6.3'), '25,2')
N(5 * 7, '35'); N(6 * Dm('4.5'), '27'); N(8 * Dm('3.2'), '25,6'); N(10 * 12, '120')
PV11 = [(0, 0), (5, 0), (5, 3), (2, 5.5), (0, 3)]
N(Dm(5) + 3 + 4 + Dm('3.5') + 3, '18,5')
N(Dm(46) / 4, '11,5'); N(Dm(51) / 6, '8,5'); N(Dm('13.5') / 3, '4,5')
N((64 - 2 * 20) / 2, '12'); N(3 * (2 * 120 + 2 * 85), '1230'); N(1230 * Dm('0.35'), '430,5')
CHK(96 / 8 == 12 and 2 * 36 + 2 * 12 == 96 and 40 / 5 == 8 and 8 + 16 + 16 == 40)
F11 = tz([('poly', PV11, 'gf'), ('lab', (2.5, 0), '5 cm', 'below'), ('lab', (5, 1.5), '3 cm', 'right'), ('lab', (3.5, 4.25), '4 cm', 'above right'), ('lab', (1, 4.25), '3,5 cm', 'above left'), ('lab', (0, 1.5), '3 cm', 'left')], 0.45)
S_.append(("Perímetre dels polígons", [
 (1, r"Calcula el perímetre de:" + tasks(2, [r"un triangle de costats 7,5\,cm, 9\,cm i 11\,cm", r"un quadrat de 8,5\,cm de costat", r"un rectangle de 15\,m × 9\,m", r"un rombe de 6,3\,cm de costat"])
     + recorda(r"El perímetre d'un polígon és la suma dels seus costats. Quadrat: $P=4\cdot l$. \ Rectangle: $P=2\cdot b+2\cdot h$. \ Polígon regular de $n$ costats: $P=n\cdot l$."),
     tasks(2, [r"$\res{27,5\text{ cm}}$", r"$4\cdot8,5=\res{34\text{ cm}}$", r"$2\cdot15+2\cdot9=\res{48\text{ m}}$", r"$4\cdot6,3=\res{25,2\text{ cm}}$"])),
 (1, r"Calcula el perímetre d'aquests polígons regulars:" + tasks(2, [r"pentàgon de 7\,cm de costat", r"hexàgon de 4,5\,cm de costat", r"octàgon de 3,2\,cm de costat", r"decàgon de 12\,mm de costat"]),
     tasks(2, [r"$5\cdot7=\res{35\text{ cm}}$", r"$6\cdot4,5=\res{27\text{ cm}}$", r"$8\cdot3,2=\res{25,6\text{ cm}}$", r"$10\cdot12=\res{120\text{ mm}}$"])),
 (1, r"Calcula el perímetre d'aquest polígon:" + center(F11),
     r"$P=5+3+4+3,5+3=\res{18,5\text{ cm}}$"),
 (2, r"Calcula el costat de:" + tasks(1, [r"un quadrat de 46\,cm de perímetre", r"un hexàgon regular de 51\,cm de perímetre", r"un triangle equilàter de 13,5\,m de perímetre"]),
     tasks(3, [r"$46:4=\res{11,5\text{ cm}}$", r"$51:6=\res{8,5\text{ cm}}$", r"$13,5:3=\res{4,5\text{ m}}$"])),
 (2, r"Un rectangle té 64\,cm de perímetre i la base fa 20\,cm. Quant fa l'altura?",
     r"Les dues bases fan $40$\,cm; queden $64-40=24$\,cm per a les dues altures: \ $h=24:2=\res{12\text{ cm}}$."),
 (2, r"Volem tancar un camp rectangular de 120\,m × 85\,m amb tres fils de filferro. Quants metres de filferro calen? Quant costaran si el metre val 0,35\,€?",
     r"$P=2\cdot120+2\cdot85=410$\,m. \ Amb tres fils: $3\cdot410=\res{1230\text{ m}}$. \ Preu: $1230\cdot0,35=\res{430,50\text{ €}}$."),
 (3, r"La base d'un rectangle fa el triple que l'altura i el perímetre fa 96\,cm. Quant fan la base i l'altura?",
     r"El perímetre equival a $3+1+3+1=8$ altures: $h=96:8=\res{12\text{ cm}}$ i $b=3\cdot12=\res{36\text{ cm}}$."),
 (3, r"Cadascun dels dos costats iguals d'un triangle isòsceles fa el doble que la base. Si el perímetre és de 40\,cm, quant fa cada costat?",
     r"El perímetre equival a $1+2+2=5$ bases: base $=40:5=\res{8\text{ cm}}$ i els costats iguals, \res{16\text{ cm}} cadascun."),
]))

# =====================================================================
# 3. Àrea del quadrat i del rectangle
# =====================================================================
N(12 ** 2, '144'); N(4 * 12, '48'); N(15 * 8, '120'); N(2 * 15 + 2 * 8, '46'); N(Dm('7.5') * 4, '30'); N(2 * Dm('7.5') + 2 * 4, '23'); N(Dm('2.5') ** 2, '6,25'); N(4 * Dm('2.5'), '10')
N(Dm(84) / 12, '7'); N(2 * 12 + 2 * 7, '38'); N(11 ** 2, '121'); N(4 * 11, '44'); N((Dm(28) / 4) ** 2, '49')
N(Dm('5.4') * Dm('3.5'), '18,9'); N(Dm('18.9') * 24, '453,6')
N(6 * Dm('2.5') - Dm('1.5') * Dm('1.2'), '13,2'); CHK(math.ceil(13.2 / 5) == 3)
N((800 // 50) * (600 // 50), '192')
CHK(4 * 10 == 2 * 20 and 10 ** 2 == 4 * 5 ** 2)
CHK([(a, 36 // a, 2 * (a + 36 // a)) for a in (1, 2, 3, 4, 6)] == [(1, 36, 74), (2, 18, 40), (3, 12, 30), (4, 9, 26), (6, 6, 24)])
S_.append(("Àrea del quadrat i del rectangle", [
 (1, r"Calcula l'àrea i el perímetre de:" + tasks(2, [r"un quadrat de 12\,cm de costat", r"un rectangle de 15\,cm × 8\,cm", r"un rectangle de 7,5\,m × 4\,m", r"un quadrat de 2,5\,m de costat"])
     + recorda(r"Rectangle: $A=b\cdot h$. \ Quadrat: $A=l\cdot l=l^2$. Les dues mesures han d'estar en la mateixa unitat."),
     tasks(2, [r"$A=\res{144\text{ cm}^2}$, $P=\res{48\text{ cm}}$", r"$A=\res{120\text{ cm}^2}$, $P=\res{46\text{ cm}}$", r"$A=\res{30\text{ m}^2}$, $P=\res{23\text{ m}}$", r"$A=\res{6,25\text{ m}^2}$, $P=\res{10\text{ m}}$"])),
 (1, r"Un rectangle té 84\,cm$^2$ d'àrea i 12\,cm de base. Quant fan l'altura i el perímetre?",
     r"$h=84:12=\res{7\text{ cm}}$; \ $P=2\cdot12+2\cdot7=\res{38\text{ cm}}$"),
 (1, r"Respon:" + tasks(1, [r"Un quadrat té 121\,m$^2$ d'àrea. Quant fa el costat? I el perímetre?", r"Un quadrat té 28\,cm de perímetre. Quina és la seua àrea?"]),
     tasks(1, [r"$11^2=121\Rightarrow l=\res{11\text{ m}}$; \ $P=\res{44\text{ m}}$", r"$l=28:4=7$\,cm; \ $A=7^2=\res{49\text{ cm}^2}$"])),
 (2, r"Una habitació fa 5,4\,m × 3,5\,m. Quant costarà posar-hi parquet si el metre quadrat val 24\,€?",
     r"$A=5,4\cdot3,5=18,9\text{ m}^2$; \ $18,9\cdot24=\res{453,60\text{ €}}$"),
 (2, r"Volem pintar una paret de 6\,m × 2,5\,m que té una finestra d'1,5\,m × 1,2\,m. Un pot de pintura cobreix 5\,m$^2$. Quants pots hem de comprar?",
     r"$6\cdot2,5-1,5\cdot1,2=15-1,8=13,2\text{ m}^2$. \ $13,2:5=2,64$: cal comprar \rest{3 pots}."),
 (2, r"Quantes rajoles quadrades de 50\,cm de costat calen per a enrajolar un pati de 8\,m × 6\,m?",
     r"Caben $800:50=16$ rajoles al llarg i $600:50=12$ a l'ample: \ $16\cdot12=\res{192}$ rajoles."),
 (3, r"Un quadrat fa 5\,cm de costat. Si dupliquem el costat, què li passa al perímetre? I a l'àrea?",
     r"$P$: de 20\,cm a 40\,cm, \rest{es duplica}. \ $A$: de 25\,cm$^2$ a 100\,cm$^2$, \rest{es multiplica per 4}."),
 (3, r"Escriu tots els rectangles de costats naturals que tenen 36\,cm$^2$ d'àrea. Quin té el perímetre més menut?",
     r"$1\times36$ ($P=74$), $2\times18$ ($P=40$), $3\times12$ ($P=30$), $4\times9$ ($P=26$), $6\times6$ ($P=24$). El de perímetre més menut és el \rest{quadrat de 6\,cm}."),
]))

# =====================================================================
# 4. Àrea del romboide i del triangle
# =====================================================================
N(12 * 7, '84'); N(Dm('8.5') * 4, '34'); N(Dm(14 * 9) / 2, '63'); N(Dm(7 * 5) / 2, '17,5'); N(Dm('6.4') * Dm('3.5') / 2, '11,2')
F27 = [tz([('poly', [(0, 0), (6, 0), (2, 4)], 'gf'), ('seg', (2, 0), (2, 4), 'd'), ('ra', (2, 0), (3, 0), (2, 1)), ('lab', (3, 0), '6 cm', 'below'), ('lab', (2, 2), '4 cm', 'right')], 0.42),
       tz([('poly', [(0, 0), (8, 0), (0, 5)], 'gf'), ('ra', (0, 0), (1, 0), (0, 1)), ('lab', (4, 0), '8 cm', 'below'), ('lab', (0, 2.5), '5 cm', 'left')], 0.38),
       tz([('poly', [(0, 0), (4, 0), (6.5, 5)], 'gf'), ('seg', (4, 0), (6.5, 0), 'd'), ('seg', (6.5, 0), (6.5, 5), 'd'), ('ra', (6.5, 0), (5.5, 0), (6.5, 1)), ('lab', (2, 0), '4 cm', 'below'), ('lab', (6.5, 2.5), '5 cm', 'right')], 0.38)]
N(Dm(6 * 4) / 2, '12'); N(Dm(8 * 5) / 2, '20'); N(Dm(4 * 5) / 2, '10')
N(Dm(9 * 12) / 2, '54'); N(9 + 12 + 15, '36'); CHK(9 ** 2 + 12 ** 2 == 15 ** 2)
N(Dm(96) / 12, '8'); N(Dm(2 * 45) / 9, '10')
TG = [(0, 0), (8, 0), (3, 5)]; CHK(shoelace(TG) == 20)
F30 = tz([('grid', (0, 0), (8, 5)), ('poly', TG, 'sht')], 0.42)
N(Dm(14 * 12) / 2, '84'); N(Dm(2 * 84) / 15, '11,2')
S_.append(("Àrea del romboide i del triangle", [
 (1, r"Calcula l'àrea dels romboides:" + tasks(2, [r"base 12\,cm i altura 7\,cm", r"base 8,5\,m i altura 4\,m"])
     + recorda(r"Romboide: $A=b\cdot h$. \ Triangle: $A=\dfrac{b\cdot h}{2}$. L'altura sempre és perpendicular a la base."),
     tasks(2, [r"$12\cdot7=\res{84\text{ cm}^2}$", r"$8,5\cdot4=\res{34\text{ m}^2}$"])),
 (1, r"Calcula l'àrea dels triangles:" + tasks(3, [r"base 14\,cm i altura 9\,cm", r"base 7\,cm i altura 5\,cm", r"base 6,4\,m i altura 3,5\,m"]),
     tasks(3, [r"$\frac{14\cdot9}{2}=\res{63\text{ cm}^2}$", r"$\frac{7\cdot5}{2}=\res{17,5\text{ cm}^2}$", r"$\frac{6,4\cdot3,5}{2}=\res{11,2\text{ m}^2}$"])),
 (1, r"Calcula l'àrea de cada triangle:" + tasks(3, F27),
     tasks(1, [r"$\frac{6\cdot4}{2}=\res{12\text{ cm}^2}$", r"$\frac{8\cdot5}{2}=\res{20\text{ cm}^2}$", r"$\frac{4\cdot5}{2}=\res{10\text{ cm}^2}$ (l'altura cau fora)"])),
 (2, r"Els catets d'un triangle rectangle fan 9\,cm i 12\,cm, i la hipotenusa, 15\,cm. Calcula'n l'àrea i el perímetre.",
     r"Els catets fan de base i altura: \ $A=\frac{9\cdot12}{2}=\res{54\text{ cm}^2}$. \ $P=9+12+15=\res{36\text{ cm}}$."),
 (2, r"Respon:" + tasks(1, [r"Un romboide té 96\,cm$^2$ d'àrea i 12\,cm de base. Quant fa l'altura?", r"Un triangle té 45\,m$^2$ d'àrea i 9\,m d'altura. Quant fa la base?"]),
     tasks(1, [r"$h=96:12=\res{8\text{ cm}}$", r"$b\cdot9=90\Rightarrow b=\res{10\text{ m}}$"])),
 (2, r"Cada quadret de la quadrícula fa 1\,cm de costat. Calcula l'àrea del triangle." + center(F30),
     r"Base 8\,cm (sobre la línia de baix) i altura 5\,cm: \ $A=\frac{8\cdot5}{2}=\res{20\text{ cm}^2}$."),
 (3, r"Un triangle té els costats de 13\,cm, 14\,cm i 15\,cm, i l'altura sobre el costat de 14\,cm fa 12\,cm. Calcula'n l'àrea i l'altura sobre el costat de 15\,cm.",
     r"$A=\frac{14\cdot12}{2}=\res{84\text{ cm}^2}$. \ Amb base 15: $\frac{15\cdot h}{2}=84\Rightarrow 15\cdot h=168\Rightarrow h=\res{11,2\text{ cm}}$."),
 (3, r"Dibuixa dues rectes paral·leles separades 6\,cm i, sobre una d'elles, un segment de 10\,cm. Dibuixa tres triangles diferents que tinguen aquest segment de base i el tercer vèrtex sobre l'altra recta. Quina àrea té cadascun? Per què?",
     r"Tots tenen la mateixa base (10\,cm) i la mateixa altura (6\,cm, la distància entre les paral·leles): $A=\frac{10\cdot6}{2}=\res{30\text{ cm}^2}$ \rest{tots tres}."),
]))
CHK(10 * 6 / 2 == 30)

# =====================================================================
# 5. Àrea del rombe i del trapezi
# =====================================================================
N(Dm(16 * 10) / 2, '80'); N(Dm(9 * 6) / 2, '27'); N(Dm('7.5') * 4 / 2, '15')
N(Dm((12 + 8) * 5) / 2, '50'); N(Dm((9 + 4) * 6) / 2, '39'); N((Dm('10.5') + Dm('6.5')) * 4 / 2, '34')
N(Dm(52) / 4, '13'); N(Dm(24 * 10) / 2, '120'); CHK(12 ** 2 + 5 ** 2 == 13 ** 2)
N(Dm((18 + 10) * 3) / 2, '42'); N(18 + 10 + 5 + 5, '38'); CHK(4 ** 2 + 3 ** 2 == 5 ** 2)
N(Dm(2 * 60) / 15, '8'); N(Dm(2 * 72) / (14 + 10), '6')
N(Dm('1.2') * Dm('0.8') / 2, '0,48'); N(Dm('0.48') * 10000, '4800')
N(Dm((85 + 55) * 40) / 2, '2800'); N(Dm(2800) / 10000, '0,28'); N(2800 * 12, '33\\,600')
F36 = tz([('poly', [(0, 0), (18, 0), (14, 3), (4, 3)], 'gf'), ('seg', (4, 0), (4, 3), 'd'), ('ra', (4, 0), (5, 0), (4, 1)), ('lab', (9, 0), '18 cm', 'below'), ('lab', (9, 3), '10 cm', 'above'), ('lab', (4, 1.5), '3 cm', 'right'), ('lab', (16, 1.5), '5 cm', 'right')], 0.3)
S_.append(("Àrea del rombe i del trapezi", [
 (1, r"Calcula l'àrea dels rombes:" + tasks(3, [r"diagonals 16\,cm i 10\,cm", r"diagonals 9\,m i 6\,m", r"diagonals 7,5\,cm i 4\,cm"])
     + recorda(r"Rombe: $A=\dfrac{D\cdot d}{2}$. \ Trapezi: $A=\dfrac{(B+b)\cdot h}{2}$."),
     tasks(3, [r"$\frac{16\cdot10}{2}=\res{80\text{ cm}^2}$", r"$\frac{9\cdot6}{2}=\res{27\text{ m}^2}$", r"$\frac{7,5\cdot4}{2}=\res{15\text{ cm}^2}$"])),
 (1, r"Calcula l'àrea dels trapezis:" + tasks(2, [r"bases 12\,cm i 8\,cm, altura 5\,cm", r"bases 9\,m i 4\,m, altura 6\,m", r"bases 10,5\,cm i 6,5\,cm, altura 4\,cm"]),
     tasks(3, [r"$\frac{(12+8)\cdot5}{2}=\res{50\text{ cm}^2}$", r"$\frac{(9+4)\cdot6}{2}=\res{39\text{ m}^2}$", r"$\frac{17\cdot4}{2}=\res{34\text{ cm}^2}$"])),
 (2, r"Un rombe té 52\,cm de perímetre i les diagonals fan 24\,cm i 10\,cm. Quant fa el costat? Calcula'n l'àrea.",
     r"$l=52:4=\res{13\text{ cm}}$; \ $A=\frac{24\cdot10}{2}=\res{120\text{ cm}^2}$"),
 (2, r"Calcula l'àrea i el perímetre d'aquest trapezi isòsceles:" + center(F36),
     r"$A=\frac{(18+10)\cdot3}{2}=\res{42\text{ cm}^2}$; \ $P=18+10+5+5=\res{38\text{ cm}}$"),
 (2, r"Respon:" + tasks(1, [r"Un rombe té 60\,cm$^2$ d'àrea i la diagonal major fa 15\,cm. Quant fa la menor?", r"Un trapezi té 72\,m$^2$ d'àrea i les bases fan 14\,m i 10\,m. Quant fa l'altura?"]),
     tasks(1, [r"$15\cdot d=120\Rightarrow d=\res{8\text{ cm}}$", r"$(14+10)\cdot h=144\Rightarrow 24\cdot h=144\Rightarrow h=\res{6\text{ m}}$"])),
 (3, r"Un estel té forma de rombe, amb diagonals d'1,2\,m i 80\,cm. Quants m$^2$ de tela calen per a fer-lo? Expressa-ho també en cm$^2$.",
     r"$A=\frac{1,2\cdot0,8}{2}=\res{0,48\text{ m}^2}=\res{4800\text{ cm}^2}$"),
 (3, r"Una parcel·la té forma de trapezi, amb bases de 85\,m i 55\,m i 40\,m d'amplària (altura). Quantes hectàrees fa? Quant val si el metre quadrat es paga a 12\,€?",
     r"$A=\frac{(85+55)\cdot40}{2}=2800\text{ m}^2=\res{0,28\text{ ha}}$. \ Preu: $2800\cdot12=\res{33\,600\text{ €}}$."),
]))

# =====================================================================
# 6. Àrea dels polígons regulars i dels polígons qualssevol
# =====================================================================
N(5 * 10, '50'); N(50 * Dm('6.88') / 2, '172'); N(6 * 8, '48'); N(48 * Dm('6.93') / 2, '166,32')
N(Dm(40) / 8, '5'); N(40 * Dm('6.04') / 2, '120,8'); N(2 * Dm('93.6') / 36, '5,2')
for n, l, a in ((5, 10, 6.88), (6, 8, 6.93), (8, 5, 6.04), (6, 6, 5.2)): CHK(abs(l / (2 * math.tan(math.pi / n)) - a) < 0.006, n, l, a)
PG44 = [(0, 0), (6, 0), (6, 4), (3, 6), (0, 4)]; CHK(shoelace(PG44) == 30 and 6 * 4 + 6 * 2 / 2 == 30)
TG45 = [(0, 0), (7, 2), (3, 6)]; CHK(shoelace(TG45) == 18 and 42 - 7 - 8 - 9 == 18)
N(60 * Dm('8.66') / 2, '259,8'); N(Dm(250000) / Dm('259.8'), '962,28', 2); CHK(math.ceil(250000 / 259.8) == 963)
F44 = tz([('grid', (0, 0), (6, 6)), ('poly', PG44, 'sht')], 0.4)
F45 = tz([('grid', (0, 0), (7, 6)), ('poly', TG45, 'sht')], 0.4)
S_.append(("Àrea dels polígons regulars i dels polígons qualssevol", [
 (1, r"Un pentàgon regular té 10\,cm de costat i 6,88\,cm d'apotema. Calcula'n el perímetre i l'àrea."
     + recorda(r"Polígon regular: $A=\dfrac{P\cdot a}{2}$, on $P=n\cdot l$ és el perímetre i $a$ és l'apotema (el segment del centre al punt mitjà d'un costat)."),
     r"$P=5\cdot10=\res{50\text{ cm}}$; \ $A=\frac{50\cdot6,88}{2}=\res{172\text{ cm}^2}$"),
 (1, r"Un hexàgon regular té 8\,cm de costat i 6,93\,cm d'apotema. Calcula'n el perímetre i l'àrea.",
     r"$P=6\cdot8=\res{48\text{ cm}}$; \ $A=\frac{48\cdot6,93}{2}=\res{166,32\text{ cm}^2}$"),
 (2, r"Un octàgon regular té 40\,cm de perímetre i 6,04\,cm d'apotema. Quant fa el costat? I l'àrea?",
     r"$l=40:8=\res{5\text{ cm}}$; \ $A=\frac{40\cdot6,04}{2}=\res{120,8\text{ cm}^2}$"),
 (2, r"Un hexàgon regular té 36\,cm de perímetre i 93,6\,cm$^2$ d'àrea. Quant fa l'apotema?",
     r"$\frac{36\cdot a}{2}=93,6\Rightarrow 36\cdot a=187,2\Rightarrow a=\res{5,2\text{ cm}}$"),
 (2, r"Cada quadret fa 1\,cm de costat. Calcula l'àrea del polígon descomponent-lo en un rectangle i un triangle." + center(F44),
     r"Rectangle $6\times4$ i triangle de base 6 i altura 2: \ $24+\frac{6\cdot2}{2}=24+6=\res{30\text{ cm}^2}$"),
 (3, r"Cada quadret fa 1\,cm de costat. Calcula l'àrea del triangle completant-lo fins a un rectangle i restant els triangles que sobren." + center(F45),
     r"Rectangle $7\times6=42$. Triangles que sobren: $\frac{7\cdot2}{2}=7$, \ $\frac{4\cdot4}{2}=8$ \ i \ $\frac{3\cdot6}{2}=9$. \ $A=42-7-8-9=\res{18\text{ cm}^2}$"),
 (3, r"Volem enrajolar 25\,m$^2$ amb rajoles en forma d'hexàgon regular de 10\,cm de costat i 8,66\,cm d'apotema. Quantes rajoles calen, com a mínim?",
     r"Rajola: $A=\frac{60\cdot8,66}{2}=259,8\text{ cm}^2$. \ $25\text{ m}^2=250\,000\text{ cm}^2$; \ $250\,000:259,8\approx962,3$: calen \rest{963 rajoles}."),
]))

# =====================================================================
# 7. La circumferència i la seua longitud
# =====================================================================
N(2 * P3 * 4, '25,12'); N(2 * P3 * 9, '56,52'); N(P3 * 20, '62,8'); N(P3 * 7, '21,98')
N(Dm('31.4') / (2 * P3), '5'); N(Dm('75.36') / P3, '24')
N(P3 * 70, '219,8'); N(Dm(100000) / Dm('219.8'), '454,96', 2); CHK(math.ceil(100000 / 219.8) == 455)
N(2 * P3 * 8 * 90 / 360, '12,56'); N(2 * P3 * 12 * 60 / 360, '12,56'); N(2 * P3 * 6 * 150 / 360, '15,7')
N(P3 * 10 / 2 + 10, '25,7'); N(2 * P3 * 4 / 4 + 8, '14,28')
N(2 * P3 * 15 * 120 / 360, '31,4'); N(2 * P3 * 15, '94,2')
F48 = tz([('circ', (0, 0), 2), ('seg', (0, 0), pol((0, 0), 2, 130), ''), ('seg', pol((0, 0), 2, 200), pol((0, 0), 2, 20), ''), ('seg', pol((0, 0), 2, 250), pol((0, 0), 2, 320), ''),
          ('arc', (0, 0), 2, 40, 100, 'hl'), ('dot', (0, 0)), ('lab', (0.25, -0.3), '$O$'), ('lab', mid((0, 0), pol((0, 0), 2, 130)), '$a$', 'above right'),
          ('lab', mid(pol((0, 0), 2, 200), pol((0, 0), 2, 20)), '$b$', 'below right'), ('lab', mid(pol((0, 0), 2, 250), pol((0, 0), 2, 320)), '$c$', 'above'), ('lab', pol((0, 0), 2.35, 70), '$d$')], 0.75)
S_.append(("La circumferència i la seua longitud", [
 (1, r"Com s'anomenen els elements $a$, $b$, $c$ i $d$ de la figura?" + center(F48),
     tasks(4, [r"$a$: \rest{radi}", r"$b$: \rest{diàmetre}", r"$c$: \rest{corda}", r"$d$: \rest{arc}"])),
 (1, r"Calcula la longitud de les circumferències (fes servir $\pi\approx3,14$):" + tasks(4, [r"radi 4\,cm", r"radi 9\,m", r"diàmetre 20\,cm", r"diàmetre 7\,mm"])
     + recorda(r"La longitud de la circumferència és $L=\pi\cdot d=2\cdot\pi\cdot r$, amb $\pi\approx3,14$. Un arc de $n^\circ$ fa $L_{\text{arc}}=\dfrac{2\cdot\pi\cdot r\cdot n}{360}$."),
     tasks(2, [r"$2\cdot3,14\cdot4=\res{25,12\text{ cm}}$", r"$2\cdot3,14\cdot9=\res{56,52\text{ m}}$", r"$3,14\cdot20=\res{62,8\text{ cm}}$", r"$3,14\cdot7=\res{21,98\text{ mm}}$"])),
 (2, r"Respon:" + tasks(1, [r"Una circumferència fa 31,4\,cm de longitud. Quant fa el radi?", r"Una circumferència fa 75,36\,m de longitud. Quant fan el diàmetre i el radi?"]),
     tasks(1, [r"$d=31,4:3,14=10$\,cm; \ $r=\res{5\text{ cm}}$", r"$d=75,36:3,14=\res{24\text{ m}}$; \ $r=\res{12\text{ m}}$"])),
 (2, r"La roda d'una bicicleta fa 70\,cm de diàmetre. Quants centímetres avança en una volta? Quantes voltes ha de fer, aproximadament, per a recórrer 1\,km?",
     r"$L=3,14\cdot70=\res{219,8\text{ cm}}$. \ $1\text{ km}=100\,000\text{ cm}$; \ $100\,000:219,8\approx455$ \ \rest{unes 455 voltes}."),
 (2, r"Calcula la longitud dels arcs:" + tasks(3, [r"$90^\circ$ i radi 8\,cm", r"$60^\circ$ i radi 12\,cm", r"$150^\circ$ i radi 6\,cm"]),
     tasks(3, [r"$\frac{2\cdot3,14\cdot8\cdot90}{360}=\res{12,56\text{ cm}}$", r"$\frac{2\cdot3,14\cdot12\cdot60}{360}=\res{12,56\text{ cm}}$", r"$\frac{2\cdot3,14\cdot6\cdot150}{360}=\res{15,7\text{ cm}}$"])),
 (3, r"Calcula el perímetre de:" + tasks(2, [r"un semicercle de 10\,cm de diàmetre", r"un quart de cercle de 4\,cm de radi"]),
     tasks(2, [r"$\frac{3,14\cdot10}{2}+10=15,7+10=\res{25,7\text{ cm}}$", r"$\frac{2\cdot3,14\cdot4}{4}+4+4=6,28+8=\res{14,28\text{ cm}}$"])),
 (3, r"L'agulla dels minuts d'un rellotge fa 15\,cm. Quina distància recorre la punta en 20 minuts? I en una hora?",
     r"En 20 minuts gira $120^\circ$: \ $\frac{2\cdot3,14\cdot15\cdot120}{360}=\res{31,4\text{ cm}}$. \ En una hora: $2\cdot3,14\cdot15=\res{94,2\text{ cm}}$."),
]))

# =====================================================================
# 8. L'àrea del cercle i de les figures circulars
# =====================================================================
N(P3 * 36, '113,04'); N(P3 * Dm('6.25'), '19,625'); N(P3 * 49, '153,86'); N(P3 * 225, '706,5')
N(P3 * 100 / 2, '157'); N(P3 * 36 / 4, '28,26')
N(P3 * 64 * 45 / 360, '25,12'); N(P3 * 81 * 120 / 360, '84,78'); N(P3 * 16 * 270 / 360, '37,68')
N(P3 * (49 - 16), '103,62'); N(P3 * (100 - 36), '200,96')
N(Dm('78.5') / P3, '25'); N(Dm('18.84') / (2 * P3), '3'); N(P3 * 9, '28,26')
N(P3 * (36 - Dm('0.5625')), '111,27375'); N(P3 * (36 - Dm('0.5625')), '111,27', 2)
N(P3 * 256, '803,84'); N(2 * P3 * 121, '759,88')
F57 = tz([('circ', (0, 0), 2.1, 'sh'), ('circ', (0, 0), 1.2, 'hole'), ('dot', (0, 0)), ('seg', (0, 0), pol((0, 0), 2.1, 30), ''), ('seg', (0, 0), pol((0, 0), 1.2, 160), 'd'),
          ('lab', pol((0, 0), 1.65, 42), '$R$'), ('lab', pol((0, 0), 0.6, 178), '$r$')], 0.6)
S_.append(("L'àrea del cercle i de les figures circulars", [
 (1, r"Calcula l'àrea dels cercles ($\pi\approx3,14$):" + tasks(4, [r"radi 6\,cm", r"radi 2,5\,m", r"diàmetre 14\,cm", r"diàmetre 30\,cm"])
     + recorda(r"Cercle: $A=\pi\cdot r^2$. \ Sector circular de $n^\circ$: $A=\dfrac{\pi\cdot r^2\cdot n}{360}$. \ Corona circular: $A=\pi\cdot R^2-\pi\cdot r^2$. Si et donen el diàmetre, calcula primer el radi."),
     tasks(2, [r"$3,14\cdot36=\res{113,04\text{ cm}^2}$", r"$3,14\cdot6,25=\res{19,625\text{ m}^2}$", r"$3,14\cdot7^2=\res{153,86\text{ cm}^2}$", r"$3,14\cdot15^2=\res{706,5\text{ cm}^2}$"])),
 (2, r"Calcula l'àrea de:" + tasks(2, [r"un semicercle de 10\,cm de radi", r"un quart de cercle de 6\,cm de radi"]),
     tasks(2, [r"$\frac{3,14\cdot100}{2}=\res{157\text{ cm}^2}$", r"$\frac{3,14\cdot36}{4}=\res{28,26\text{ cm}^2}$"])),
 (2, r"Calcula l'àrea dels sectors circulars:" + tasks(3, [r"$45^\circ$ i radi 8\,cm", r"$120^\circ$ i radi 9\,cm", r"$270^\circ$ i radi 4\,cm"]),
     tasks(3, [r"$\frac{3,14\cdot64\cdot45}{360}=\res{25,12\text{ cm}^2}$", r"$\frac{3,14\cdot81\cdot120}{360}=\res{84,78\text{ cm}^2}$", r"$\frac{3,14\cdot16\cdot270}{360}=\res{37,68\text{ cm}^2}$"])),
 (2, r"Calcula l'àrea de la corona circular de la figura en cada cas:" + center(F57) + tasks(2, [r"$R=7$\,cm, \ $r=4$\,cm", r"$R=10$\,m, \ $r=6$\,m"]),
     tasks(2, [r"$3,14\cdot(49-16)=3,14\cdot33=\res{103,62\text{ cm}^2}$", r"$3,14\cdot(100-36)=3,14\cdot64=\res{200,96\text{ m}^2}$"])),
 (2, r"Respon:" + tasks(1, [r"Un cercle té 78,5\,cm$^2$ d'àrea. Quant fa el radi?", r"Una circumferència fa 18,84\,cm. Quina és l'àrea del cercle que tanca?"]),
     tasks(1, [r"$r^2=78,5:3,14=25\Rightarrow r=\res{5\text{ cm}}$", r"$r=18,84:6,28=3$\,cm; \ $A=3,14\cdot9=\res{28,26\text{ cm}^2}$"])),
 (3, r"Un CD fa 12\,cm de diàmetre i té un forat central d'1,5\,cm de diàmetre. Quina és la superfície del CD?",
     r"Corona de radis $R=6$\,cm i $r=0,75$\,cm: \ $3,14\cdot(36-0,5625)\approx\res{111,27\text{ cm}^2}$"),
 (3, r"Què té més superfície: una pizza de 32\,cm de diàmetre o dues pizzes de 22\,cm de diàmetre?",
     r"Gran: $3,14\cdot16^2=803,84\text{ cm}^2$. \ Dues menudes: $2\cdot3,14\cdot11^2=759,88\text{ cm}^2$. \ \rest{La pizza gran.}"),
]))

# =====================================================================
# 9. Figures compostes
# =====================================================================
FL = [(0, 0), (10, 0), (10, 4), (6, 4), (6, 7), (0, 7)]; CHK(shoelace(FL) == 58 and 70 - 12 == 58 and 10 + 4 + 4 + 3 + 6 + 7 == 34)
F61 = tz([('poly', FL, 'gf'), ('lab', (5, 0), '10 cm', 'below'), ('lab', (0, 3.5), '7 cm', 'left'), ('lab', (10, 2), '4 cm', 'right'), ('lab', (8, 4), '4 cm', 'above'), ('lab', (3, 7), '6 cm', 'above')], 0.32)
F62 = tz([('poly', [(0, 0), (8, 0), (8, 5), (0, 5)], 'gf'), ('poly', [(0, 5), (8, 5), (4, 8)], 'sh'), ('seg', (4, 5), (4, 8), 'd'), ('lab', (4, 0), '8 m', 'below'), ('lab', (8, 2.5), '5 m', 'right'), ('lab', (4, 6.5), '3 m', 'right')], 0.3)
N(8 * 5 + Dm(8 * 3) / 2, '52')
F63 = tz([('poly', [(0, 0), (6, 0), (6, 4), (0, 4)], 'sh'), ('sect', (6, 2), 2, -90, 90, 'sh'), ('seg', (6, 0), (6, 4), 'd'), ('lab', (3, 0), '6 cm', 'below'), ('lab', (0, 2), '4 cm', 'left')], 0.38)
N(24 + P3 * 4 / 2, '30,28'); N(6 + 6 + 4 + P3 * 2, '22,28')
F64 = tz([('poly', [(0, 0), (8, 0), (8, 8), (0, 8)], 'sh')] + [('sect', C, 4, a, a + 90, 'hole') for C, a in (((0, 0), 0), ((8, 0), 90), ((8, 8), 180), ((0, 8), 270))] + [('lab', (4, 0), '8 cm', 'below')], 0.28)
N(64 - P3 * 16, '13,76')
F65 = tz([('poly', [(-1.5, -1.5), (11.5, -1.5), (11.5, 7.5), (-1.5, 7.5)], 'sh'), ('poly', [(0, 0), (10, 0), (10, 6), (0, 6)], 'hole'), ('lab', (5, 3), '10 m × 6 m'), ('lab', (5, 6.75), '1,5 m')], 0.3)
N(13 * 9 - 60, '57')
N(80 * 50 + P3 * 625, '5962,5'); N(160 + P3 * 50, '317')
N(P3 * 9, '28,26'); N(P3 * (36 - 9), '84,78'); N(P3 * (81 - 36), '141,3')
F67 = tz([('circ', (0, 0), 2.7, 'sh'), ('circ', (0, 0), 1.8, 'hole'), ('circ', (0, 0), 1.8, 'tl'), ('circ', (0, 0), 0.9, 'sh'), ('dot', (0, 0)), ('seg', (0, 0), (2.7, 0), ''), ('lab', (0.45, 0), '3', 'above'), ('lab', (1.35, 0), '3', 'above'), ('lab', (2.25, 0), '3', 'above')], 0.55)
N(2 * (P3 * 36 / 4 - 18), '20,52')
F68 = tz([('poly', [(0, 0), (6, 0), (6, 6), (0, 6)], 'frame'), ('arc', (0, 0), 6, 0, 90, 'hl'), ('arc', (6, 6), 6, 180, 270, 'hl'), ('seg', (6, 0), (0, 6), 'd'), ('lab', (3, 0), '6 cm', 'below')], 0.38)
N(Dm('1.2') * Dm('1.5') + P3 * Dm('0.36') / 2, '2,3652'); N((Dm('1.8') + Dm('0.5652')) * 45, '106,434'); N((Dm('1.8') + Dm('0.5652')) * 45, '106,43', 2)
F69 = tz([('poly', [(0, 0), (1.2, 0), (1.2, 1.5), (0, 1.5)], 'gf'), ('sect', (0.6, 1.5), 0.6, 0, 180, 'gf'), ('seg', (0, 1.5), (1.2, 1.5), 'd'), ('lab', (0.6, 0), '1,2 m', 'below'), ('lab', (1.2, 0.75), '1,5 m', 'right')], 1.6)
S_.append(("Figures compostes", [
 (1, r"Calcula l'àrea i el perímetre d'aquesta figura:" + center(F61)
     + recorda(r"Per a l'àrea d'una figura composta, la \textbf{descomponem} en figures conegudes i sumem, o la \textbf{completem} i restem. El perímetre és només el contorn exterior."),
     r"Completem el rectangle $10\times7$ i restem el tros $4\times3$: \ $A=70-12=\res{58\text{ cm}^2}$. \ $P=10+4+4+3+6+7=\res{34\text{ cm}}$."),
 (1, r"Calcula l'àrea de la façana d'aquesta caseta:" + center(F62),
     r"$A=8\cdot5+\frac{8\cdot3}{2}=40+12=\res{52\text{ m}^2}$"),
 (2, r"Calcula l'àrea i el perímetre de la figura, formada per un rectangle i un semicercle ($\pi\approx3,14$):" + center(F63),
     r"Semicercle de radi 2\,cm: \ $A=6\cdot4+\frac{3,14\cdot2^2}{2}=24+6,28=\res{30,28\text{ cm}^2}$. \ $P=6+6+4+\frac{2\cdot3,14\cdot2}{2}=16+6,28=\res{22,28\text{ cm}}$"),
 (2, r"Calcula l'àrea de la zona acolorida (un quadrat de 8\,cm de costat sense quatre quarts de cercle de 4\,cm de radi):" + center(F64),
     r"Els quatre quarts formen un cercle sencer de radi 4\,cm: \ $A=8^2-3,14\cdot4^2=64-50,24=\res{13,76\text{ cm}^2}$"),
 (2, r"Al voltant d'una piscina de 10\,m × 6\,m es fa una vorera d'1,5\,m d'amplària. Quina és l'àrea de la vorera?" + center(F65),
     r"Rectangle exterior: $(10+3)\times(6+3)=13\cdot9=117\text{ m}^2$. \ $A=117-60=\res{57\text{ m}^2}$"),
 (2, r"Una pista està formada per un rectangle de 80\,m × 50\,m i dos semicercles de 50\,m de diàmetre als extrems. Calcula'n l'àrea i la longitud d'una volta.",
     r"Els dos semicercles fan un cercle de radi 25\,m: \ $A=80\cdot50+3,14\cdot25^2=4000+1962,5=\res{5962,5\text{ m}^2}$. \ $P=2\cdot80+3,14\cdot50=160+157=\res{317\text{ m}}$"),
 (3, r"Una diana té tres circumferències concèntriques de radis 3, 6 i 9\,cm. Calcula l'àrea de cada zona." + center(F67),
     r"Centre: $3,14\cdot9=\res{28,26\text{ cm}^2}$. \ Zona del mig: $3,14\cdot(36-9)=\res{84,78\text{ cm}^2}$. \ Zona de fora: $3,14\cdot(81-36)=\res{141,3\text{ cm}^2}$."),
 (3, r"Dins d'un quadrat de 6\,cm de costat es dibuixen dos quarts de circumferència amb centre en dos vèrtexs oposats. Calcula l'àrea de la fulla que queda entre els dos arcs." + center(F68),
     r"La diagonal divideix la fulla en dues meitats. Cada meitat és un quart de cercle menys un triangle: $\frac{3,14\cdot36}{4}-\frac{6\cdot6}{2}=28,26-18=10,26$. \ $A=2\cdot10,26=\res{20,52\text{ cm}^2}$"),
 (3, r"Una finestra està formada per un rectangle d'1,2\,m × 1,5\,m acabat per dalt amb un semicercle. Quant costa el vidre si el m$^2$ val 45\,€?" + center(F69),
     r"$A=1,2\cdot1,5+\frac{3,14\cdot0,6^2}{2}=1,8+0,5652=2,3652\text{ m}^2$. \ $2,3652\cdot45\approx\res{106,43\text{ €}}$"),
]))

# =====================================================================
# 10. El teorema de Pitàgores
# =====================================================================
def R2(x): return Dm(str(x)).sqrt()
F71 = tz([('poly', [(0, 0), (4, 0), (0, 3)], 'sh'), ('ra', (0, 0), (4, 0), (0, 3)), ('lab', (2, 0), '$x$', 'below'), ('lab', (0, 1.5), '$y$', 'left'), ('lab', (2, 1.5), '$z$', 'above right')], 0.45)
F72 = tz([('poly', [(0, 0), (5, 0), (1.8, 2.4)], 'sh'), ('ra', (1.8, 2.4), (0, 0), (5, 0)), ('lab', (2.5, 0), '$m$', 'below'), ('lab', (0.9, 1.2), '$n$', 'above left'), ('lab', (3.4, 1.2), '$p$', 'above right')], 0.45)
F73 = tz([('poly', [(0, 0), (0, 4), (3, 4)], 'sh'), ('ra', (0, 4), (0, 0), (3, 4)), ('lab', (0, 2), '$r$', 'left'), ('lab', (1.5, 4), '$s$', 'above'), ('lab', (1.5, 2), '$t$', 'below right')], 0.45)
for a, b, c in [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (6, 8, 10), (12, 5, 13), (15, 8, 17), (7, 24, 25)]: CHK(a * a + b * b == c * c, a, b, c)
N(R2(29), '5,39', 2); N(R2(52), '7,21', 2); N(R2(64 - 9), '7,42', 2); N(R2(100 - 49), '7,14', 2)
CHK(36 + 64 == 100 and 25 + 49 == 74 != 81 and 64 + 225 == 289 and 100 + 121 == 221 != 225)
N(Dm(25) - Dm('1.96'), '23,04'); N(R2('23.04'), '4,8')
N(R2(144 + 81), '15'); N(R2(36 + 64), '10'); N(R2(144 + 25), '13'); N(4 * 13, '52')
F79 = tz([('grid', (0, 0), (8, 10)), ('poly', [(1, 1), (7, 1), (7, 9)], 'sht'), ('ra', (7, 1), (1, 1), (7, 9)), ('dot', (1, 1)), ('dot', (7, 9)), ('lab', (1, 1), '$A$', 'below left'), ('lab', (7, 9), '$B$', 'above right')], 0.3)
F710 = tz([('seg', (-1, 0), (7, 0), ''), ('seg', (0, 0), (0, 12), 'hl'), ('seg', (0, 12), (5, 0), ''), ('ra', (0, 0), (5, 0), (0, 12)), ('lab', (0, 6), '12 m', 'left'), ('lab', (2.5, 0), '5 m', 'below'), ('lab', (2.5, 6), 'cable', 'right')], 0.17)
S_.append(("El teorema de Pitàgores", [
 (1, r"En cada triangle rectangle, digues quins costats són els catets i quin és la hipotenusa, i escriu la relació que dona el teorema de Pitàgores:" + center(F71 + r'\qquad\qquad ' + F72 + r'\qquad\qquad ' + F73)
     + recorda(r"En un triangle rectangle, els \textbf{catets} formen l'angle recte i la \textbf{hipotenusa} és el costat oposat, el més llarg. \textbf{Teorema de Pitàgores:} $c^2=a^2+b^2$."),
     tasks(1, [r"Catets $x$ i $y$; hipotenusa $z$: \ $\res{z^2=x^2+y^2}$", r"Catets $n$ i $p$; hipotenusa $m$: \ $\res{m^2=n^2+p^2}$", r"Catets $r$ i $s$; hipotenusa $t$: \ $\res{t^2=r^2+s^2}$"])),
 (1, r"Calcula la hipotenusa d'un triangle rectangle de catets:" + tasks(4, [r"3\,cm i 4\,cm", r"6\,m i 8\,m", r"5\,cm i 12\,cm", r"9\,dm i 12\,dm"])
     + recorda(r"Hipotenusa: $c=\sqrt{a^2+b^2}$ (sumem els quadrats i fem l'arrel). \ Catet: $b=\sqrt{c^2-a^2}$ (restem i fem l'arrel)."),
     tasks(2, [r"$\sqrt{9+16}=\sqrt{25}=\res{5\text{ cm}}$", r"$\sqrt{36+64}=\sqrt{100}=\res{10\text{ m}}$", r"$\sqrt{25+144}=\sqrt{169}=\res{13\text{ cm}}$", r"$\sqrt{81+144}=\sqrt{225}=\res{15\text{ dm}}$"])),
 (1, r"Calcula el catet que falta en cada triangle rectangle:" + tasks(2, [r"hipotenusa 10\,cm, catet 6\,cm", r"hipotenusa 13\,m, catet 12\,m", r"hipotenusa 17\,cm, catet 15\,cm", r"hipotenusa 25\,cm, catet 7\,cm"]),
     tasks(2, [r"$\sqrt{100-36}=\sqrt{64}=\res{8\text{ cm}}$", r"$\sqrt{169-144}=\sqrt{25}=\res{5\text{ m}}$", r"$\sqrt{289-225}=\sqrt{64}=\res{8\text{ cm}}$", r"$\sqrt{625-49}=\sqrt{576}=\res{24\text{ cm}}$"])),
 (2, r"Calcula el costat que falta i arrodoneix el resultat a les centèsimes:" + tasks(2, [r"catets 2\,cm i 5\,cm", r"catets 4\,cm i 6\,cm", r"hipotenusa 8\,cm, catet 3\,cm", r"hipotenusa 10\,cm, catet 7\,cm"]),
     tasks(2, [r"$c=\sqrt{4+25}=\sqrt{29}\approx\res{5,39\text{ cm}}$", r"$c=\sqrt{16+36}=\sqrt{52}\approx\res{7,21\text{ cm}}$", r"$b=\sqrt{64-9}=\sqrt{55}\approx\res{7,42\text{ cm}}$", r"$b=\sqrt{100-49}=\sqrt{51}\approx\res{7,14\text{ cm}}$"])),
 (2, r"Esbrina si són rectangles els triangles que tenen aquests costats:" + tasks(4, [r"6, 8 i 10\,cm", r"5, 7 i 9\,cm", r"8, 15 i 17\,cm", r"10, 11 i 15\,cm"])
     + recorda(r"Compara el quadrat del costat més llarg amb la suma dels quadrats dels altres dos. Si són iguals, el triangle és rectangle."),
     tasks(2, [r"$10^2=100$; \ $36+64=100$: \ \rest{sí}", r"$9^2=81$; \ $25+49=74$: \ \rest{no}", r"$17^2=289$; \ $64+225=289$: \ \rest{sí}", r"$15^2=225$; \ $100+121=221$: \ \rest{no}"])),
 (2, r"Una escala de 5\,m està recolzada en una paret, amb el peu a 1,4\,m de la paret. A quina altura arriba?",
     r"L'escala és la hipotenusa: \ $h=\sqrt{5^2-1,4^2}=\sqrt{25-1,96}=\sqrt{23,04}=\res{4,8\text{ m}}$"),
 (2, r"Un vaixell ix del port i navega 12\,km cap al nord i després 9\,km cap a l'est. A quina distància en línia recta està del port?",
     r"Els dos trajectes són els catets: \ $d=\sqrt{12^2+9^2}=\sqrt{144+81}=\sqrt{225}=\res{15\text{ km}}$"),
 (3, r"En la quadrícula, cada quadret fa 1\,cm de costat. Calcula la distància entre els punts $A$ i $B$." + center(F79),
     r"Triangle rectangle de catets 6\,cm i 8\,cm: \ $AB=\sqrt{36+64}=\sqrt{100}=\res{10\text{ cm}}$"),
 (3, r"Per a subjectar un pal de 12\,m d'alt es lliguen quatre cables des de la punta fins a terra, cadascun a 5\,m del peu del pal. Quants metres de cable calen?" + center(F710),
     r"Cada cable: $\sqrt{12^2+5^2}=\sqrt{169}=13$\,m. \ Quatre cables: $4\cdot13=\res{52\text{ m}}$"),
]))

# =====================================================================
# 11. Pitàgores per a calcular àrees i perímetres
# =====================================================================
N(R2(64 + 36), '10'); N(R2(576 + 49), '25'); N(R2(32), '5,66', 2)
N(R2(100 - 64), '6'); N(Dm(16 * 6) / 2, '48'); N(16 + 20, '36')
F82 = tz([('poly', [(-8, 0), (8, 0), (0, 6)], 'gf'), ('seg', (0, 0), (0, 6), 'd'), ('ra', (0, 0), (8, 0), (0, 6)), ('lab', (0, 0), '16 cm', 'below'), ('lab', (-4, 3), '10 cm', 'above left'), ('lab', (4, 3), '10 cm', 'above right'), ('lab', (0, 3), '$h$', 'right')], 0.2)
N(R2(81 + 144), '15'); N(4 * 15, '60'); N(Dm(18 * 24) / 2, '216')
N(R2(25 + 144), '13'); N(12 + 7 + 12 + 13, '44'); N(Dm(19 * 12) / 2, '114')
F84 = tz([('poly', [(0, 0), (12, 0), (7, 12), (0, 12)], 'gf'), ('seg', (7, 0), (7, 12), 'd'), ('ra', (0, 0), (12, 0), (0, 12)), ('ra', (7, 0), (12, 0), (7, 12)), ('lab', (6, 0), '12 cm', 'below'), ('lab', (3.5, 12), '7 cm', 'above'), ('lab', (0, 6), '12 cm', 'left'), ('lab', (9.5, 6), '$c$', 'right')], 0.17)
N(R2(100 - 36), '8'); N(Dm(20 * 8) / 2, '80'); N(16 + 4 + 20, '40')
N(R2(16 - 4), '3,46', 2); N(Dm(24) * Dm('3.46') / 2, '41,52')
F86 = tz([('poly', reg(6, 2), 'gf'), ('seg', (0, 0), mid(reg(6, 2)[0], reg(6, 2)[1]), 'd'), ('seg', (0, 0), reg(6, 2)[1], 'd'), ('ra', mid(reg(6, 2)[0], reg(6, 2)[1]), (0, 0), reg(6, 2)[1]), ('dot', (0, 0)), ('lab', mid(reg(6, 2)[0], reg(6, 2)[1]), '4 cm', 'below'), ('lab', (0, -0.85), '$a$', 'left')], 0.55)
N(R2(36 - 9), '5,20', 2); N(6 * Dm('5.2') / 2, '15,6')
N(P3 * 16, '50,24'); N(P3 * 16 - 32, '18,24')
F88 = tz([('circ', (0, 0), 4, 'sh'), ('poly', [(4, 0), (0, 4), (-4, 0), (0, -4)], 'hole'), ('seg', (-4, 0), (4, 0), 'd'), ('dot', (0, 0)), ('lab', (2, 0), '4 cm', 'above')], 0.32)
N(R2(16 + 9), '5'); N(8 + 5 + 5 + 5 + 5, '28'); N(8 * 5 + Dm(8 * 3) / 2, '52')
F89 = tz([('poly', [(0, 0), (8, 0), (8, 5), (0, 5)], 'gf'), ('poly', [(0, 5), (8, 5), (4, 8)], 'sh'), ('seg', (4, 5), (4, 8), 'd'), ('ra', (4, 5), (8, 5), (4, 8)), ('lab', (4, 0), '8 m', 'below'), ('lab', (8, 2.5), '5 m', 'right'), ('lab', (4, 6.5), '3 m', 'left')], 0.3)
S_.append(("Pitàgores per a calcular àrees i perímetres", [
 (1, r"Calcula la diagonal de:" + tasks(3, [r"un rectangle de 8\,cm × 6\,cm", r"un rectangle de 24\,m × 7\,m", r"un quadrat de 4\,cm de costat"])
     + recorda(r"Busca dins de la figura un \textbf{triangle rectangle} en què la mesura que et falta siga un costat i en conegues els altres dos. Aplica Pitàgores i després calcula l'àrea o el perímetre."),
     tasks(3, [r"$\sqrt{64+36}=\res{10\text{ cm}}$", r"$\sqrt{576+49}=\res{25\text{ m}}$", r"$\sqrt{16+16}=\sqrt{32}\approx\res{5,66\text{ cm}}$"])),
 (1, r"Calcula l'altura, l'àrea i el perímetre d'aquest triangle isòsceles:" + center(F82),
     r"L'altura parteix la base en dues meitats de 8\,cm: \ $h=\sqrt{10^2-8^2}=\sqrt{36}=\res{6\text{ cm}}$. \ $A=\frac{16\cdot6}{2}=\res{48\text{ cm}^2}$. \ $P=16+10+10=\res{36\text{ cm}}$"),
 (2, r"Les diagonals d'un rombe fan 18\,cm i 24\,cm. Calcula'n el costat, el perímetre i l'àrea.",
     r"Les semidiagonals fan 9 i 12\,cm: \ $l=\sqrt{81+144}=\sqrt{225}=\res{15\text{ cm}}$. \ $P=4\cdot15=\res{60\text{ cm}}$. \ $A=\frac{18\cdot24}{2}=\res{216\text{ cm}^2}$"),
 (2, r"Calcula el perímetre i l'àrea d'aquest trapezi rectangle:" + center(F84),
     r"Triangle de catets $12-7=5$ i 12: \ $c=\sqrt{25+144}=\sqrt{169}=13$\,cm. \ $P=12+7+12+13=\res{44\text{ cm}}$. \ $A=\frac{(12+7)\cdot12}{2}=\res{114\text{ cm}^2}$"),
 (2, r"Un trapezi isòsceles té les bases de 16\,cm i 4\,cm i els costats iguals de 10\,cm. Calcula'n l'altura, l'àrea i el perímetre.",
     r"A cada costat sobren $(16-4):2=6$\,cm: \ $h=\sqrt{100-36}=\res{8\text{ cm}}$. \ $A=\frac{(16+4)\cdot8}{2}=\res{80\text{ cm}^2}$. \ $P=16+4+10+10=\res{40\text{ cm}}$"),
 (2, r"Calcula l'apotema i l'àrea d'un hexàgon regular de 4\,cm de costat." + center(F86),
     r"El radi és igual al costat (4\,cm): \ $a=\sqrt{4^2-2^2}=\sqrt{12}\approx\res{3,46\text{ cm}}$. \ $P=6\cdot4=24$\,cm; \ $A=\frac{24\cdot3,46}{2}=\res{41,52\text{ cm}^2}$"),
 (3, r"Un triangle equilàter té 18\,cm de perímetre. Calcula'n l'altura i l'àrea.",
     r"Costat: $18:3=6$\,cm. \ $h=\sqrt{6^2-3^2}=\sqrt{27}\approx\res{5,20\text{ cm}}$. \ $A=\frac{6\cdot5,2}{2}=\res{15,6\text{ cm}^2}$"),
 (3, r"Un quadrat té els quatre vèrtexs sobre una circumferència de 4\,cm de radi. Calcula l'àrea de la zona acolorida ($\pi\approx3,14$)." + center(F88),
     r"La diagonal del quadrat és un diàmetre (8\,cm): \ $l^2+l^2=64\Rightarrow l^2=32$, que és l'àrea del quadrat. \ $A=3,14\cdot4^2-32=50,24-32=\res{18,24\text{ cm}^2}$"),
 (3, r"Calcula el perímetre i l'àrea de la façana d'aquesta caseta, amb una teulada en forma de triangle isòsceles:" + center(F89),
     r"Cada costat de la teulada: $\sqrt{4^2+3^2}=\sqrt{25}=5$\,m. \ $P=8+5+5+5+5=\res{28\text{ m}}$. \ $A=8\cdot5+\frac{8\cdot3}{2}=\res{52\text{ m}^2}$"),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
KW = 'pdfkeywords={perímetre, àrea, unitats de longitud, unitats de superfície, hectàrea, quadrat, rectangle, romboide, triangle, rombe, trapezi, polígons regulars, apotema, circumferència, nombre pi, cercle, sector circular, corona circular, figures compostes, teorema de Pitàgores, catets, hipotenusa}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 1r ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
TIT = "Àrees i perímetres"

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 8: %s. 1r d'ESO}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 8 · 1r d'ESO" % t)
    assert 'Unitat 8' in p and 'unitat 8' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{1r ESO}{''' + ('Solucions de la fitxa · Unitat 8' if sol else "Fitxa d'exercicis · Unitat 8") + r'''}{''' + TIT + r'''}
''')
    if not sol:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs eines per a canviar d'unitats i per a explorar les àrees i els perímetres de totes les figures."
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i escriu sempre les unitats (cm, cm$^2$…). Quan hi haja cercles o circumferències, fes servir $\pi\approx3,14$. Si una arrel no és exacta, arrodoneix-la a les centèsimes.") + r'''
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
    name = 't8-fitxa-solucions.tex' if sol else 't8-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis,', NCHK[0], 'comprovacions')
