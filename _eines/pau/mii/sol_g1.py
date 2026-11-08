# Solucions 1-40 del recull de geometria. S'executa dins de sol_geo.py.
# ruff: noqa
import math

O = V(0, 0, 0)
U = r"\ \text{u}"
U2 = r"\ \text{u}^2"
U3 = r"\ \text{u}^3"


def sq(x2):
    """√x2 i aproximació si no és exacta"""
    return rq(x2) + ("" if isq(x2) else r"\approx " + ap(math.sqrt(float(x2))))


def lineq(p1, p2, name="r", p=L):
    P, d, k = line_pl(p1, p2)
    pn = {"r": "R", "s": "S", "r'": "R'", "l": "L"}.get(name, "P")
    return P, d, (line_pl_tex(p1, p2, P, d, k, pn) + r" $$%s:\ %s$$" % (name, par_tex(P, d, p)))


def plane3x(A, B, C, nA="A", nB="B", nC="C", name=r"\pi"):
    u, v = sub(B, A), sub(C, A)
    cx, n = crossx(u, v)
    pl = pl_pn(A, n)
    ck(pl.has(B) and pl.has(C))
    t = (r"$\overrightarrow{%s%s}=%s$, $\overrightarrow{%s%s}=%s$. Vector normal: $$\vec n=\overrightarrow{%s%s}\times\overrightarrow{%s%s}=%s$$"
         r"Imposem que passe per $%s$: $\ %s:\ %s$."
         % (nA, nB, pv(u), nA, nC, pv(v), nA, nB, nA, nC, cx, nA, name, pl.tex()))
    return pl, t


# ---------------- 1. Juny 1999 ----------------
p1 = Pl((1, 2, 1), 4)
p2, t2 = plane3x(V(1, 1, 1), V(1, 2, 3), V(2, 0, 0))
ck(p2 == Pl((1, 2, -1), -2))
P, d, tl = lineq(p1, p2)
td, d2 = dpr_x(O, P, d, "O", "R")
ck(d2 == F(46, 5))
sol(1, steps(
    ap_("Pla $\\pi_2$.") + t2.replace(r"\pi:", r"\pi_2:").replace("A", "A").replace("$\\overrightarrow{AB}", "Amb $A(1,1,1)$, $B(1,2,3)$, $C(2,0,0)$: $\\overrightarrow{AB}", 1),
    ap_("Recta $r=\\pi_1\\cap\\pi_2$.") + tl,
    ap_("Distància de l'origen a $r$.") + td,
) + res(r"$\pi_2:x+2y-z-2=0$ i $d(O,r)=%s\ \text{u}$." % sq(d2)))

# ---------------- 2. Juny 1999 ----------------
A, B, C, D = V(1, 0, 2), V(0, 1, 3), V(0, 3, 0), V(1, 2, 1)
d1, e1 = sub(B, A), sub(D, C)
m = det3(sub(C, A), d1, e1)
ck(not par(d1, e1) and m != 0)
td, d2 = dll_x(A, d1, C, e1, "A", "C", "1", "2")
td = td.replace(r"d(A,C)", r"d(r_1,r_2)")
sol(2, steps(
    ap_("Vectors directors.") + r"$\vec d_1=\overrightarrow{AB}=%s$, $\vec d_2=\overrightarrow{CD}=%s$: no són proporcionals, així que les rectes no són paral·leles." % (pv(d1), pv(e1)),
    ap_("Posició relativa.") + r"$\overrightarrow{AC}=%s$ i $$[\overrightarrow{AC},\vec d_1,\vec d_2]=%s\neq0$$ Els tres vectors no són coplanaris: les rectes <strong>es creuen</strong>." % (pv(sub(C, A)), detx(sub(C, A), d1, e1)),
    ap_("Distància.") + td.replace(r"\vec d_1\times\vec d_2", r"\vec d_1\times\vec d_2"),
) + res(r"Es creuen i $d(r_1,r_2)=%s\ \text{u}$." % sq(d2)))

# ---------------- 3. Setembre 1999 ----------------
for a in (F(3), F(-2), F(1, 2)):
    ck(d2_ll(V(0, 0, 0), V(0, 1, 0), V(0, 0, 5), V(a, 7, 0)) == 25)
ck(d2_pl(V(0, 0, 5), V(0, 0, 0), V(0, 1, 0)) == 25)
sol(3, steps(
    ap_("Elements de les rectes.") + r"$r_1$: punt $A(0,0,0)$, $\vec d_1=\overrightarrow{AB}=(0,1,0)$. $\ r_2$: punt $C(0,0,5)$, $\vec d_2=\overrightarrow{CD}=(a,7,0)$.",
    ap_("Cas $a\\neq0$.") + r"Els directors no són proporcionals. $\overrightarrow{AC}=(0,0,5)$ i $$[\overrightarrow{AC},\vec d_1,\vec d_2]=\begin{vmatrix}0&0&5\\ 0&1&0\\ a&7&0\end{vmatrix}=5(0-a)=-5a\neq0$$ Les rectes es creuen. $\vec d_1\times\vec d_2=\begin{vmatrix}\vec i&\vec j&\vec k\\ 0&1&0\\ a&7&0\end{vmatrix}=(0,0,-a)$, de mòdul $|a|$: $$d(r_1,r_2)=\frac{|-5a|}{|a|}=5\ \text{u}$$",
    ap_("Cas $a=0$.") + r"$\vec d_2=(0,7,0)\parallel\vec d_1$ i $C\notin r_1$: rectes paral·leles. $d(r_1,r_2)=d(C,r_1)=\dfrac{|\overrightarrow{AC}\times\vec d_1|}{|\vec d_1|}=\dfrac{|(-5,0,0)|}{1}=5$ u.",
    ap_("Interpretació.") + r"La distància no depèn de $a$: $r_1$ està continguda en el pla $z=0$ i $r_2$ en el pla $z=5$ (tots dos directors tenen tercera component nul·la). Són dos plans paral·lels a distància 5, i la perpendicular comuna és vertical, així que dues rectes qualssevol situades en aquests plans disten 5. El paràmetre $a$ només gira $r_2$ dins del pla $z=5$.",
) + res(r"$d(r_1,r_2)=5$ u per a qualsevol $a$ (les rectes estan en els plans paral·lels $z=0$ i $z=5$)."))

# ---------------- 4. Setembre 1999 ----------------
A, B, C, E = V(8, 0, 0), V(0, 8, 0), V(0, 0, 8), V(8, 8, 8)
D = sub(add(A, C), B)
w = sub(E, A)
Fp, G, H = add(B, w), add(C, w), add(D, w)
vol = abs(det3(sub(B, A), sub(D, A), w))
ck(D == V(8, -8, 8) and vol == 1024)
sol(4, steps(
    ap_("Quart vèrtex de la base.") + r"$ABCD$ és un paral·lelogram: $\overrightarrow{AD}=\overrightarrow{BC}\Rightarrow D=A+C-B=%s$." % pv(D),
    ap_("Base superior.") + r"Les arestes laterals són paral·leles i iguals a $\overrightarrow{AE}=%s$: $$F=B+\overrightarrow{AE}=%s,\quad G=C+\overrightarrow{AE}=%s,\quad H=D+\overrightarrow{AE}=%s$$" % (pv(w), pv(Fp), pv(G), pv(H)),
    ap_("Volum.") + r"És el valor absolut del producte mixt de tres arestes que ixen d'un vèrtex: $\overrightarrow{AB}=%s$, $\overrightarrow{AD}=%s$, $\overrightarrow{AE}=%s$: $$[\overrightarrow{AB},\overrightarrow{AD},\overrightarrow{AE}]=%s$$" % (pv(sub(B, A)), pv(sub(D, A)), pv(w), detx(sub(B, A), sub(D, A), w)),
) + res(r"$V=1024\ \text{u}^3$; $D%s$, $F%s$, $G%s$, $H%s$." % (pv(D), pv(Fp), pv(G), pv(H))))

# ---------------- 5. Juny 2000 ----------------
ck(d2_ppl(V(4, 0, 0), Pl((1, -1, 1), -2)) == F(4, 3))
sol(5, steps(
    ap_("a)") + r"$\vec n_1=(1,1,1)$ i $\vec n_2=(1,1,-1)$ no són proporcionals ($\frac11=\frac11\neq\frac1{-1}$): els plans <strong>no són paral·lels</strong>, es tallen en una recta.",
    ap_("b)") + r"$\vec n_1=\vec n_2=(1,-1,1)$ però els termes independents són diferents ($4\neq2$): els plans són <strong>paral·lels</strong>.",
    ap_("Distància en el cas b).") + r"Amb el mateix vector normal, $\pi_1:x-y+z-4=0$ i $\pi_2:x-y+z-2=0$: $$d(\pi_1,\pi_2)=\frac{|D_1-D_2|}{|\vec n|}=\frac{|-4-(-2)|}{\sqrt{1+1+1}}=\frac{2}{\sqrt3}=%s\ \text{u}$$ (També: prenem $P(4,0,0)\in\pi_1$ i calculem $d(P,\pi_2)$.)" % sq(F(4, 3)),
) + res(r"a) Secants (no paral·lels). b) Paral·lels, a distància $\frac{2\sqrt3}{3}\approx1{,}15$ u."))

# ---------------- 6. Juny 2000 ----------------
A, B = (F(3), F(4)), (F(4), F(3))
C = (F(7), F(7))
ck((C[0] - 3) ** 2 + (C[1] - 4) ** 2 == 25 and (C[0] - 4) ** 2 + (C[1] - 3) ** 2 == 25)
sol(6, steps(
    ap_("Condicions.") + r"Siga $C(x,y)$. $|\overrightarrow{AC}|=5$ i $|\overrightarrow{BC}|=5$: $$(x-3)^2+(y-4)^2=25,\qquad (x-4)^2+(y-3)^2=25$$",
    ap_("Restem les equacions.") + r"$(x-3)^2-(x-4)^2+(y-4)^2-(y-3)^2=0\Rightarrow(2x-7)-(2y-7)=0\Rightarrow y=x$ (és la mediatriu de $AB$: $C$ equidista de $A$ i $B$).",
    ap_("Substituïm.") + r"$(x-3)^2+(x-4)^2=25\Rightarrow 2x^2-14x=0\Rightarrow x=0$ o $x=7$. Com que les coordenades de $C$ han de ser positives, $C(7,7)$.",
    ap_("Vèrtex $D$.") + r"En el paral·lelogram $ABCD$, $\overrightarrow{AD}=\overrightarrow{BC}$: $D=A+C-B=(3+7-4,\ 4+7-3)=(6,8)$.",
) + res(r"$C(7,7)$ i $D(6,8)$."))

# ---------------- 7. Setembre 2000 ----------------
A, B, C, D = V(2, 4, 0), V(6, 2, 0), V(0, 0, 7), V(3, 2, 0)
d1, e1 = prim(sub(B, A)), sub(D, C)
ck(det3(sub(C, A), d1, e1) != 0)
td, d2 = dll_x(A, d1, C, e1, "A", "C", "1", "2")
sol(7, steps(
    ap_("Directors.") + r"$\overrightarrow{AB}=%s$, així que prenem $\vec d_1=%s$; $\ \vec d_2=\overrightarrow{CD}=%s$. No són proporcionals." % (pv(sub(B, A)), pv(d1), pv(e1)),
    ap_("Les rectes es creuen") + r"si el producte mixt és no nul, i la distància és el volum del paral·lelepípede dividit per l'àrea de la base: " + td.replace("d(A,C)", "d(r_1,r_2)"),
) + res(r"$d(r_1,r_2)=%s$ u." % sq(d2)))

# ---------------- 8. Setembre 2000 ----------------
pl, tp = plane3x(V(0, 0, 0), V(0, 2, 4), V(4, 0, 2), "O", "A", "B")
ck(pl == Pl((1, 4, -2), 0))
td, d2 = dpl_x(V(0, 0, 7), pl)
sol(8, steps(
    ap_("Mètode.") + r"Calculem l'equació general del pla $Ax+By+Cz+D=0$ amb un punt i dos vectors (el producte vectorial dona el vector normal) i després apliquem la fórmula $d(P,\pi)=\dfrac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}$.",
    ap_("Pla.") + r"Amb $O(0,0,0)$, $A(0,2,4)$, $B(4,0,2)$: " + tp,
    ap_("Distància.") + "$" + td + "$",
) + res(r"$\pi:x+4y-2z=0$ i $d=%s$ u." % sq(d2)))

# ---------------- 9. Juny 2001 ----------------
A, B, C, E = V(1, 1, 1), V(2, 1, 1), V(2, 4, 1), V(1, 2, 7)
D = sub(add(A, C), B)
cx, c = crossx(sub(B, A), sub(D, A))
area = n2(c)
vol = abs(det3(sub(B, A), sub(D, A), sub(E, A)))
ck(area == 9 and vol == 18)
sol(9, steps(
    ap_("Arestes que ixen de $A$.") + r"$D=A+C-B=%s$, $\ \overrightarrow{AB}=%s$, $\overrightarrow{AD}=\overrightarrow{BC}=%s$, $\overrightarrow{AE}=%s$." % (pv(D), pv(sub(B, A)), pv(sub(D, A)), pv(sub(E, A))),
    ap_("Àrea de la base.") + r"$$\overrightarrow{AB}\times\overrightarrow{AD}=%s\ \Rightarrow\ S=|(0,0,3)|=3\ \text{u}^2$$" % cx,
    ap_("Volum.") + r"$$V=|[\overrightarrow{AB},\overrightarrow{AD},\overrightarrow{AE}]|=\left|%s\right|=18\ \text{u}^3$$" % detx(sub(B, A), sub(D, A), sub(E, A)),
    ap_("Distància entre les bases.") + r"És l'altura del paral·lelepípede: $h=\dfrac{V}{S}=\dfrac{18}{3}=6$ u. (Ho confirma que les bases estan en els plans $z=1$ i $z=7$.)",
) + res(r"Àrea de la base $3$ u², volum $18$ u³ i distància entre les bases $6$ u."))

# ---------------- 10. Juny 2001 ----------------
Op, A, B, C = V(0, 0, 0), V(1, 1, 1), V(0, 5, 0), V(10, 5, 0)
dr, ds = sub(A, Op), sub(C, B)
mx = det3(sub(B, Op), dr, ds)
cx, c = crossx(dr, ds)
d2 = mx ** 2 / n2(c)
ck(abs(mx) == 50 and n2(c) == 200 and d2 == F(25, 2))
sol(10, steps(
    ap_("Comprovacions.") + r"$O$ i $A$ compleixen $x=y=z$. $B$ i $C$ compleixen $y=5$, $z=0$. Per tant $r$ té director $\overrightarrow{OA}=(1,1,1)$ i $r'$ té director $\overrightarrow{BC}=(10,0,0)$.",
    ap_("Producte mixt i producte vectorial.") + r"$$[\overrightarrow{OA},\overrightarrow{BC},\overrightarrow{OB}]=%s,\qquad \overrightarrow{OA}\times\overrightarrow{BC}=%s$$ amb $|\overrightarrow{OA}\times\overrightarrow{BC}|=\sqrt{200}=10\sqrt2$. Com que el producte mixt no és 0, les rectes es creuen." % (detx(dr, ds, sub(B, Op)), cx),
    ap_("Distància i relació.") + r"El valor absolut del producte mixt és el volum del paral·lelepípede d'arestes $\overrightarrow{OA}$, $\overrightarrow{BC}$, $\overrightarrow{OB}$; el mòdul del producte vectorial és l'àrea de la base (el paral·lelogram de costats $\overrightarrow{OA}$, $\overrightarrow{BC}$, paral·lel a les dues rectes), i l'altura sobre aquesta base és justament la distància entre les rectes: $$d(r,r')=\frac{|[\overrightarrow{OA},\overrightarrow{BC},\overrightarrow{OB}]|}{|\overrightarrow{OA}\times\overrightarrow{BC}|}=\frac{50}{10\sqrt2}=\frac{5\sqrt2}{2}\approx3{,}54\ \text{u}$$",
) + res(r"$d(r,r')=\dfrac{5\sqrt2}{2}$ u $=\dfrac{\text{volum}}{\text{àrea de la base}}$."))

# ---------------- 11. Setembre 2001 ----------------
for Dk in (71, -85):
    ck(abs(Dk + 7) == 78)
sol(11, steps(
    ap_("Plans paral·lels a $\\pi$.") + r"Tenen el mateix vector normal: $12x+3y-4z+D=0$. Escrivim $\pi:12x+3y-4z-7=0$ i $|\vec n|=\sqrt{144+9+16}=13$.",
    ap_("Condició de distància.") + r"$$\frac{|D-(-7)|}{13}=6\ \Rightarrow\ |D+7|=78\ \Rightarrow\ D=71\ \text{ o }\ D=-85$$",
) + res(r"$12x+3y-4z+71=0$ i $12x+3y-4z-85=0$."))

# ---------------- 12. Setembre 2001 ----------------
ck(Pl((1, 1, 1), -3).has(V(1, 1, 1)) and Pl((1, 0, -1), 0).has(V(1, 1, 1)))
sol(12, steps(
    r"<em>Nota: a l'enunciat del recull apareix $\pi_1:x+y+x=3$; és una errata de $\pi_1:x+y+z=3$.</em>",
    ap_("Rectes en el pla $z=0$.") + r"$$\pi_1\cap\pi_4:\begin{cases}x+y=3\\ z=0\end{cases}\equiv(3-\lambda,\lambda,0),\qquad \pi_2\cap\pi_4:\begin{cases}x=0\\ z=0\end{cases}\ (\text{eix }Y),\qquad \pi_3\cap\pi_4:\begin{cases}y=0\\ z=0\end{cases}\ (\text{eix }X)$$",
    ap_("Vèrtexs del tetraedre.") + r"Tallant els plans de tres en tres: $\pi_2\cap\pi_3\cap\pi_4=O(0,0,0)$, $\ \pi_1\cap\pi_3\cap\pi_4=A(3,0,0)$, $\ \pi_1\cap\pi_2\cap\pi_4=B(0,3,0)$ i $\pi_1\cap\pi_2\cap\pi_3$: $x=z$, $y=z$, $3z=3$, $V(1,1,1)$.",
    ap_("Àrea de la cara del pla $z=0$.") + r"És el triangle rectangle $OAB$: $S=\dfrac{|\overrightarrow{OA}\times\overrightarrow{OB}|}{2}=\dfrac{|(0,0,9)|}{2}=\dfrac92$ u².",
    ap_("Altura.") + r"És la distància del vèrtex oposat $V(1,1,1)$ al pla $\pi_4:z=0$: $h=\dfrac{|1|}{\sqrt{0+0+1}}=1$ u. (Volum: $\frac13\cdot\frac92\cdot1=\frac32$ u³.)",
) + res(r"Rectes $\{x+y=3,z=0\}$, eix $Y$ i eix $X$; àrea de la base $\frac92$ u² i altura $1$ u."))

# ---------------- 13. Juny 2002 ----------------
A, B = V(1, -2, 3), V(0, 2, 1)
d = sub(B, A)
Mm = mid(A, B)
med = pl_pn(Mm, d)
ck(med == Pl((2, -8, 4), -9))
ck(d2_pp(V(0, 0, 0), A) != 0)
P, dd, tl = lineq(Pl((0, 2, -1), 0), med, "s")
td, d2 = dpr_x(O, P, dd, "O", "S", "s")
sol(13, steps(
    ap_("a)") + r"$\overrightarrow{AB}=%s$: $\ r:\ %s$." % (pv(d), par_tex(A, d)),
    ap_("b) Pla mediador.") + r"Els punts que equidisten de $A$ i $B$ formen el pla perpendicular a $AB$ pel punt mitjà $M=%s$: $$-1\left(x-\tfrac12\right)+4y-2(z-2)=0\ \Rightarrow\ \pi:\ %s$$" % (pvt(Mm), med.tex()),
    ap_("c) Recta $s$.") + tl,
    ap_("Distància a l'origen.") + td,
) + res(r"a) $%s$; b) $\pi:%s$; c) $d=%s$ u." % (par_tex(A, d), med.tex(), sq(d2))))

# ---------------- 14. Juny 2002 ----------------
P0 = V(3, -1, 4)
p1, p2 = Pl((2, 1, -1), 5), Pl((4, 4, -1), 9)
R, d, tl = lineq(p1, p2)
td, d2 = dpr_x(P0, R, d, "P", "R")
tp, plb = pencil_x(p1, p2, P0)
ck(plb == Pl((2, -11, -7), 11))
sol(14, steps(
    ap_("a) Recta $r$.") + tl,
    ap_("Distància de $P$ a $r$.") + td,
    ap_("b) Pla per $r$ i $P$.") + tp,
) + res(r"a) $d(P,r)=%s$ u; b) $%s$." % (sq(d2), plb.tex())))

# ---------------- 15. Setembre 2002 ----------------
p1, p2 = Pl((1, 1, 0), -6), Pl((2, 4, 4), 2)
P, d, tl = lineq(p1, p2)
for lam in (4, -4):
    ck(F(dot(V(1, 1, 0), V(2, 4, lam))) ** 2 / (2 * (20 + lam ** 2)) == F(1, 2))
sol(15, steps(
    ap_("a) $\\lambda=4$.") + r"$\pi_2:2x+4y+4z+2=0\equiv x+2y+2z+1=0$. " + tl,
    ap_("b) Angle de $45^\\circ$.") + r"$\vec n_1=(1,1,0)$, $\vec n_2=(2,4,\lambda)$: $$\cos45^\circ=\frac{|\vec n_1\cdot\vec n_2|}{|\vec n_1||\vec n_2|}\ \Rightarrow\ \frac{\sqrt2}{2}=\frac{6}{\sqrt2\,\sqrt{20+\lambda^2}}\ \Rightarrow\ \sqrt{20+\lambda^2}=6\ \Rightarrow\ \lambda^2=16$$",
) + res(r"a) $%s$; b) $\lambda=4$ o $\lambda=-4$." % par_tex(P, d)))

# ---------------- 16. Setembre 2002 ----------------
pl = Pl((8, -4, 1), -3)
P0 = V(1, -3, 7)
q1, q2 = Pl((1, 2, 0), 5), Pl((1, 0, -8), 55)
ck(q1.has(P0) and q2.has(P0) and par(cross(q1.n, q2.n), pl.n))
td, d2 = dpl_x(P0, pl)
ck(d2 == F(64, 9))
sol(16, steps(
    ap_("a) Recta perpendicular.") + r"Té per director el vector normal $\vec n=(8,-4,1)$: $\ \dfrac{x-1}{8}=\dfrac{y+3}{-4}=\dfrac{z-7}{1}$. Igualant les fraccions dos a dos: $-4(x-1)=8(y+3)$ i $x-1=8(z-7)$: $$\begin{cases}x+2y+5=0\\ x-8z+55=0\end{cases}$$",
    ap_("b)") + "$" + td + "$",
    ap_("c)") + r"Plans $8x-4y+z+D=0$ amb $\dfrac{|D-(-3)|}{\sqrt{81}}=3\Rightarrow|D+3|=27\Rightarrow D=24$ o $D=-30$.",
) + res(r"a) $\{x+2y+5=0,\ x-8z+55=0\}$; b) $\frac83$ u; c) $8x-4y+z+24=0$ i $8x-4y+z-30=0$."))

# ---------------- 17. Juny 2003 ----------------
A, B = V(3, 6, 7), V(7, 8, 3)
dr = prim(sub(B, A))
p1, p2 = Pl((1, -4, -1), 10), Pl((3, -4, 1), 2)
P, ds, tl = lineq(p1, p2, "r'", M_)
ck(par(dr, ds) and not p1.has(A))
td, d2 = dpr_x(A, P, ds, "A", "R'", "r'")
ab = n2(sub(B, A))
ar2 = ab * d2 / 4
ck(ab == 36)
sol(17, steps(
    ap_("a) Recta $r$.") + r"$\overrightarrow{AB}=%s$, director $\vec d_r=%s$: $\ r:\ %s$." % (pv(sub(B, A)), pv(dr), par_tex(A, dr)),
    ap_("Recta $r'$.") + tl,
    ap_("Posició relativa.") + r"$\vec d_r=\vec d_{r'}=%s$ i $A%s$ no és de $r'$ ($%s\neq-10$): les rectes són <strong>paral·leles</strong>." % (pv(dr), pv(A), nm(p1.ev(A) - 10)),
    ap_("b) Distància.") + r"Com que són paral·leles, $d(r,r')=d(A,r')$: " + td.replace("d(A,r')", "d"),
    ap_("c) Àrea.") + r"Qualsevol $C\in r'$ està a distància $d$ de la recta $AB$, així que l'altura del triangle sobre la base $AB$ és sempre $d$: $$S=\frac{|AB|\cdot d}{2}=\frac{6\cdot %s}{2}=%s\ \text{u}^2$$ (no depèn del punt $C$ triat)." % (rq(d2), sq(ar2)),
) + res(r"Paral·leles; $d=%s$ u; àrea $%s$ u² per a qualsevol $C\in r'$." % (sq(d2), sq(ar2))))

# ---------------- 18. Juny 2003 ----------------
R1, R2 = V(2, 2, 4), V(-1, 2, 1)
dr = prim(sub(R2, R1))
pl, tp = plane3x(V(1, 0, 1), V(1, -1, 0), V(3, 0, 0), "A", "B", "C")
ck(pl == Pl((1, -2, 2), -3))
t, Pp = meet_lp(R1, dr, pl)
ta, s2, g = ang_x(dr, pl.n, "rp", r"\vec d", r"\vec n")
ck(s2 == F(1, 2))
ST = []
for k in (12, -12):
    tt = (F(k) - pl.ev(R1)) / dot(pl.n, dr)
    X = pt_on(R1, dr, tt)
    ck(d2_ppl(X, pl) == 16)
    ST.append(X)
sol(18, steps(
    ap_("Elements.") + r"$r$: punt $R(2,2,4)$ i director $\vec d=%s$ (proporcional a $(-3,0,-3)$). Pla: " % pv(dr) + tp,
    ap_("a)") + r"$\vec d\cdot\vec n=%s\neq0$: la recta no és paral·lela al pla (el talla en un punt)." % nm(dot(dr, pl.n)),
    ap_("b) Punt de tall.") + r"$(2+\lambda,\ 2,\ 4+\lambda)$ en $\pi$: $%s=0\Rightarrow\lambda=%s$, $P%s$." % (lin([3], ["\\lambda"], 3), nm(t), pv(Pp)),
    ap_("Angle.") + "$$" + ta + r"\Rightarrow\alpha=45^\circ$$",
    ap_("c)") + r"Un punt de $r$ és $X(2+\lambda,2,4+\lambda)$ i $d(X,\pi)=\dfrac{|3+3\lambda|}{3}=|1+\lambda|=4\Rightarrow\lambda=3$ o $\lambda=-5$.",
) + res(r"b) $P%s$, $\alpha=45^\circ$; c) $S%s$ i $T%s$." % (pv(Pp), pv(ST[0]), pv(ST[1]))))

# ---------------- 19. Setembre 2003 ----------------
P0 = V(3, 2, 3)
p1, p2 = Pl((1, 3, -4), 0), Pl((1, 2, -2), -1)
R, d, tl = lineq(p1, p2)
ck(R == V(3, -1, 0) and d == V(2, -2, -1))
td, d2 = dpr_x(P0, R, d, "P", "R")
ck(d2 == 9)
MN = []
for tt in (1, -3):
    X = pt_on(R, d, tt)
    ck(d2_pp(X, P0) == 45)
    MN.append(X)
mn2 = d2_pp(MN[0], MN[1])
ck(mn2 == 144)
sol(19, steps(
    ap_("Recta $r$.") + tl,
    ap_("a)") + td,
    ap_("b)") + r"Busquem $X=%s$ amb $|\overrightarrow{PX}|^2=5d^2=45$: $\overrightarrow{PX}=(2\lambda,\,-3-2\lambda,\,-3-\lambda)$ i $$4\lambda^2+(3+2\lambda)^2+(3+\lambda)^2=45\Rightarrow9\lambda^2+18\lambda-27=0\Rightarrow\lambda^2+2\lambda-3=0$$ $\lambda=1$ o $\lambda=-3$." % gp(R, d),
    ap_("c)") + r"$M$ i $N$ són de $r$, així que l'altura des de $P$ és $d=3$: $|MN|=\sqrt{%s}=12$ i $S=\dfrac{12\cdot3}{2}=18$ u²." % nm(mn2),
) + res(r"a) $d=3$ u; b) $M%s$, $N%s$; c) $18$ u²." % (pv(MN[0]), pv(MN[1]))))

# ---------------- 20. Setembre 2003 ----------------
pa, ta = plane3x(V(0, 2, 1), V(3, -1, 1), V(1, -1, 5), "A", "B", "C")
pb, tb = plane3x(V(3, 0, 2), V(2, 1, 1), V(5, 4, -2), "D", "E", "G", r"\pi'")
P, d, tl = lineq(pa, pb)
tg, c2, g = ang_x(pa.n, pb.n, "pp", r"\vec n", r"\vec n'")
nperp = cross(d, pa.n)
pc = pl_pn(P, nperp)
ck(pc.has(pt_on(P, d, 1)) and dot(pc.n, pa.n) == 0)
sol(20, steps(
    ap_("Pla $\\pi$.") + ta,
    ap_("Pla $\\pi'$.") + tb,
    ap_("a) Recta $r$.") + tl,
    ap_("b) Angle.") + "$$" + tg + r"\Rightarrow\alpha=%s$$" % gr(g),
    ap_("c)") + r"El pla conté $r$ i és perpendicular a $\pi$, així que conté les direccions $\vec d$ i $\vec n=%s$: $$\vec n''=\vec d\times\vec n=%s$$ i passa per $P%s$: $\ %s$." % (pv(pa.n), crossx(d, pa.n)[0], pv(P), pc.tex()),
) + res(r"a) $%s$; b) $\alpha\approx%s$; c) $%s$." % (par_tex(P, d), gr(g), pc.tex())))

# ---------------- 21. Juny 2004 ----------------
p1, p2 = Pl((1, 1, 1), 5), Pl((1, -3, -1), -3)
S, ds, tl = lineq(p1, p2, "s", M_)
R, dr = V(2, 1, 0), V(2, 3, 2)
pos = pos_ll(R, dr, S, ds)
m = det3(sub(S, R), dr, ds)
pl = pl_pn(S, cross(ds, dr))
ck(pl.has(pt_on(S, ds, 1)) and dot(pl.n, dr) == 0 and not pl.has(R))
sol(21, steps(
    ap_("Recta $s$.") + tl,
    ap_("a) Posició.") + r"$r$: $R(2,1,0)$, $\vec d_r=(2,3,2)$. Els directors no són proporcionals. $\overrightarrow{SR}$ amb $S%s$: $\overrightarrow{SR}=%s$ i $$[\overrightarrow{SR},\vec d_r,\vec d_s]=%s$$" % (pv(S), pv(sub(R, S)), detx(sub(R, S), dr, ds)) + (r"Com que és diferent de zero, les rectes <strong>es creuen</strong>." if m != 0 else r"Com que és zero, les rectes <strong>es tallen</strong>."),
    ap_("b)") + r"El pla conté $s$ i és paral·lel a $r$: passa per $S%s$ i té per normal $\vec d_s\times\vec d_r=%s$: $\ %s$." % (pv(S), crossx(ds, dr)[0], pl.tex()),
) + res(r"a) Les rectes %s; b) $%s$." % (pos, pl.tex())))

# ---------------- 22. Juny 2004 ----------------
R, dr = V(1, 0, 0), V(1, 2, 3)
P0 = V(1, 1, 1)
q1 = pl_pn(P0, (1, -2, -1))
q2 = pl_pn(R, cross(dr, sub(P0, R)))
ck(q1 == Pl((1, -2, -1), 2) and q2 == Pl((1, 1, -1), -1) and q2.has(P0))
X, d, tl = lineq(q1, q2, "s")
sol(22, steps(
    ap_("a)") + r"Paral·lel a $\pi$: $x-2y-z+D=0$; per $P$: $1-2-1+D=0\Rightarrow D=2$. $\ \pi_1:%s$." % q1.tex(),
    ap_("b)") + r"$r$ passa per $R(1,0,0)$ amb director $\vec d=(1,2,3)$, i $\overrightarrow{RP}=(0,1,1)$: $$\vec n_2=\vec d\times\overrightarrow{RP}=%s$$ $\pi_2:%s$ (passa per $R$ i per $P$)." % (crossx(dr, sub(P0, R))[0], q2.tex()),
    ap_("c) Recta intersecció.") + tl,
) + res(r"a) $%s$; b) $%s$; c) $%s$." % (q1.tex(), q2.tex(), par_tex(X, d))))

# ---------------- 23. Setembre 2004 ----------------
P0 = V(-2, 4, -3)
R, dr = V(1, 2, 0), V(1, -2, 1)
pl = pl_pn(P0, dr)
ck(pl == Pl((1, -2, 1), 13))
t, Mf = meet_lp(R, dr, pl)
td, d2 = dpr_x(P0, R, dr, "P", "R")
ck(d2 == d2_pp(P0, Mf))
sol(23, steps(
    ap_("a)") + r"El director de $r$ és normal al pla: $x-2y+z+D=0$; per $P$: $-2-8-3+D=0\Rightarrow D=13$. $\ \pi:%s$." % pl.tex(),
    ap_("b)") + td + r" (També: el pla anterior talla $r$ en el peu de la perpendicular $M%s$, i $d=|\overrightarrow{PM}|$.)" % pv(Mf),
) + res(r"a) $%s$; b) $%s$ u." % (pl.tex(), sq(d2))))

# ---------------- 24. Setembre 2004 ----------------
A, B, C, D = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1), V(2, 1, 2)
cx, c = crossx(sub(C, B), sub(D, B))
ar2 = n2(c) / 4
vol = abs(det3(sub(B, A), sub(C, A), sub(D, A))) / 6
plb = pl_pn(B, c)
td, d2 = dpl_x(A, plb, "A", r"\pi")
ck(d2 == (3 * vol) ** 2 / ar2)
sol(24, steps(
    ap_("a)") + r"$\overrightarrow{BC}=%s$, $\overrightarrow{BD}=%s$: $\ \overrightarrow{BC}\times\overrightarrow{BD}=%s$. $$S=\frac{|\overrightarrow{BC}\times\overrightarrow{BD}|}{2}=\frac{%s}{2}=%s\ \text{u}^2$$" % (pv(sub(C, B)), pv(sub(D, B)), cx, sqv(n2(c)), sq(ar2)),
    ap_("b)") + r"$$V=\frac16\left|[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}]\right|=\frac16\left|%s\right|=%s\ \text{u}^3$$" % (detx(sub(B, A), sub(C, A), sub(D, A)), nm(vol)),
    ap_("c)") + r"Pla $BCD$: normal $%s$ i passa per $B$: $\ \pi:%s$. $$%s$$ (o bé $h=\dfrac{3V}{S}$)." % (pv(c), plb.tex(), td),
) + res(r"a) $%s$ u²; b) $%s$ u³; c) $%s$ u." % (sq(ar2), nm(vol), sq(d2))))

# ---------------- 25. Juny 2005 ----------------
for mm in (F(2), F(-1, 3)):
    A_, B_, C_ = V(1, 6 * mm, 6 * mm), V(2, 8 * mm, 4 * mm), V(3, 9 * mm, 3 * mm)
    pl = Pl((0, 1, 1), -12 * mm)
    ck(pl.has(A_) and pl.has(B_) and pl.has(C_))
    ck(cross(sub(B_, A_), sub(C_, A_)) == V(0, -mm, -mm))
sol(25, steps(
    ap_("a)") + r"$u$: $x=1$, $y=z$; en $\pi$: $2z=12m\Rightarrow z=6m$: $A(1,6m,6m)$. $\ v$: $x=2$, $y=2z$; $3z=12m$: $B(2,8m,4m)$. $\ w$: $x=3$, $y=3z$; $4z=12m$: $C(3,9m,3m)$.",
    ap_("b)") + r"$\overrightarrow{AB}=(1,2m,-2m)$, $\overrightarrow{AC}=(2,3m,-3m)$: $$\overrightarrow{AB}\times\overrightarrow{AC}=\begin{vmatrix}\vec i&\vec j&\vec k\\ 1&2m&-2m\\ 2&3m&-3m\end{vmatrix}=(0,\,-m,\,-m)$$ $$S=\frac{\sqrt{m^2+m^2}}{2}=\frac{\sqrt2\,|m|}{2}=1\Rightarrow|m|=\sqrt2$$",
) + res(r"a) $A(1,6m,6m)$, $B(2,8m,4m)$, $C(3,9m,3m)$; b) $m=\sqrt2$ o $m=-\sqrt2$."))

# ---------------- 26. Juny 2005 ----------------
Q = V(-7, 2, -3)
pls = []
for tt in (-3, -4):
    H = V(tt, 4, 1)
    pl = pl_pn(H, H)
    ck(pl.has(Q))
    ck(proj_pl(O, pl)[1] == H)
    pls.append(pl)
sol(26, steps(
    ap_("Idea.") + r"Si $H$ és la projecció de l'origen sobre un d'aquests plans, el vector $\overrightarrow{OH}$ és perpendicular al pla. Així, el pla passa per $H$ i per $Q(-7,2,-3)$, i $\overrightarrow{OH}\perp\overrightarrow{HQ}$.",
    ap_("Condició.") + r"$H=(t,4,1)$ (punt de la recta). $\overrightarrow{OH}\cdot\overrightarrow{HQ}=0$: $$(t,4,1)\cdot(-7-t,\,-2,\,-4)=-7t-t^2-8-4=0\Rightarrow t^2+7t+12=0\Rightarrow t=-3\ \text{o}\ t=-4$$",
    ap_("Plans.") + r"$t=-3$: $H(-3,4,1)$, normal $(-3,4,1)$: $-3x+4y+z-26=0$, és a dir, $%s$. $\ t=-4$: $H(-4,4,1)$: $-4x+4y+z-33=0$, és a dir, $%s$. (Tots dos passen per $Q$ ✓.)" % (pls[0].tex(), pls[1].tex()),
) + res(r"$%s$ i $%s$." % (pls[0].tex(), pls[1].tex())))

# ---------------- 27. Setembre 2005 ----------------
u1, u2, u3 = V(2, 1, 0), V(1, -2, 0), V(0, 0, 1)
ck(dot(u1, u2) == 0 and dot(u1, u3) == 0 and dot(u2, u3) == 0)
Pv = V(12, 21, -11)
a_, b_, c_ = F(9), F(-6), F(-11)
ck(add(add(sc(a_, u1), sc(b_, u2)), sc(c_, u3)) == Pv)
E1, E2, E3 = sc(a_, u1), sc(b_, u2), sc(c_, u3)
verts = [E1, E2, E3, add(E1, E2), add(E1, E3), add(E2, E3)]
vol = abs(det3(E1, E2, E3))
ck(vol == 2970)
sol(27, steps(
    ap_("Les tres rectes.") + r"Totes passen per l'origen: $l$ és l'eix $Z$, $\vec u_l=(0,0,1)$; $m$: $x=2y$, $z=0$, $\vec u_m=(2,1,0)$; $n$: $y=-2x$, $z=0$, $\vec u_n=(1,-2,0)$. Són perpendiculars dos a dos ($\vec u_m\cdot\vec u_n=2-2=0$ i les dues són horitzontals). Per tant, l'origen $O$ és un vèrtex i les arestes que hi concorren estan sobre $l$, $m$ i $n$.",
    ap_("Vèrtex donat.") + r"El vèrtex $(12,21,-11)$ no està en cap cara que passe per $O$, així que és l'oposat a $O$: $$(12,21,-11)=a(2,1,0)+b(1,-2,0)+c(0,0,1)\Rightarrow\begin{cases}2a+b=12\\ a-2b=21\\ c=-11\end{cases}\Rightarrow a=9,\ b=-6,\ c=-11$$",
    ap_("a) Vèrtexs.") + r"Arestes des de $O$: $\vec e_1=9(2,1,0)=%s$, $\vec e_2=-6(1,-2,0)=%s$, $\vec e_3=%s$. Vèrtexs: $O(0,0,0)$, $%s$, $%s$, $%s$, $%s$, $%s$, $%s$ i $(12,21,-11)$." % tuple([pv(E1), pv(E2), pv(E3)] + [pv(v) for v in verts]),
    ap_("b) Volum.") + r"$|\vec e_1|=\sqrt{405}=9\sqrt5$, $|\vec e_2|=\sqrt{180}=6\sqrt5$, $|\vec e_3|=11$: $V=9\sqrt5\cdot6\sqrt5\cdot11=2970$ u³ (coincideix amb $|[\vec e_1,\vec e_2,\vec e_3]|$).",
) + res(r"Vèrtexs $O$, $(18,9,0)$, $(-6,12,0)$, $(0,0,-11)$, $(12,21,0)$, $(18,9,-11)$, $(-6,12,-11)$, $(12,21,-11)$; $V=2970$ u³."))

# ---------------- 28. Setembre 2005 ----------------
pa, pb = Pl((5, -1, -1), 0), Pl((1, 1, -1), 0)
P0 = V(9, 4, -1)
d = prim(cross(pa.n, pb.n))
pl = pl_pn(P0, d)
t, Mf = meet_lp(O, d, pl)
Ps = sym(P0, Mf)
ck(pl == Pl((1, 2, 3), -14) and Mf == V(1, 2, 3) and Ps == V(-7, 0, 7))
sol(28, steps(
    ap_("a)") + r"Si és perpendicular a $\pi$ i a $\sigma$, el seu vector normal és perpendicular a $\vec n_\pi$ i a $\vec n_\sigma$: $$\vec n_\pi\times\vec n_\sigma=%s\parallel(1,2,3)$$ Per $P$: $x+2y+3z+D=0$, $9+8-3+D=0\Rightarrow D=-14$: $\ %s$." % (crossx(pa.n, pb.n)[0], pl.tex()),
    ap_("b) Recta $r$.") + r"Els dos plans passen per l'origen i $\vec d_r=(1,2,3)$: $r:(x,y,z)=\lambda(1,2,3)$. El pla de l'apartat a) és perpendicular a $r$ i passa per $P$, així que talla $r$ en la projecció $M$ de $P$: $\lambda+4\lambda+9\lambda=14\Rightarrow\lambda=1$, $M(1,2,3)$.",
    ap_("Simètric.") + r"$M$ és el punt mitjà de $P$ i $P'$: $P'=2M-P=(2-9,\ 4-4,\ 6+1)=(-7,0,7)$.",
) + res(r"a) $x+2y+3z-14=0$; b) $P'(-7,0,7)$."))

# ---------------- 29. Juny 2006 ----------------
p1, p2 = Pl((1, 1, -1), -5), Pl((2, 1, -2), -2)
R, dr, tl = lineq(p1, p2)
Pp, Qp = V(3, 10, 5), V(5, 12, 6)
ds = sub(Qp, Pp)
tt, uu, H = meet_ll(R, dr, Pp, ds)
tg, c2, g = ang_x(dr, ds, "rr", r"\vec d_r", r"\vec d_s")
ck(c2 == F(1, 2))
cxv = cross(ds, dr)
ck(n2(cxv) == 9)
MN = [pt_on(H, dr, k) for k in (2, -2)]
for X in MN:
    ck(n2(cross(sub(Qp, Pp), sub(X, Pp))) / 4 == 9)
sol(29, steps(
    ap_("a) Recta $r$.") + tl + r" Recta $s$: $\vec d_s=\overrightarrow{PQ}=%s$, $\ s:\ %s$." % (pv(ds), par_tex(Pp, ds, M_)),
    ap_("b) Punt $H$.") + r"Igualem: $%s$. Resolent, $\lambda=%s$, $\mu=%s$: $H%s$." % (r"\begin{cases}%s=%s\\ %s=%s\\ %s=%s\end{cases}" % tuple(x for i in range(3) for x in (aff(R[i], dr[i]), aff(Pp[i], ds[i], M_))), nm(tt), nm(uu), pv(H)),
    ap_("Angle.") + "$$" + tg + r"\Rightarrow\alpha=45^\circ$$",
    ap_("c)") + r"$M$ i $N$ són de $r$ i $r$ talla $s$ en $H$. Si $M=H+k\,\vec d_r$, l'àrea és $$S=\frac{|\overrightarrow{PQ}\times\overrightarrow{PM}|}{2}=\frac{|k|\,|\overrightarrow{PQ}\times\vec d_r|}{2}=\frac{|k|\cdot|%s|}{2}=\frac{3|k|}{2}$$ (perquè $\overrightarrow{PQ}\times\overrightarrow{PH}=\vec 0$). $S=3\Rightarrow k=\pm2$." % pv(cxv),
) + res(r"a) $r:%s$, $s:%s$; b) $H%s$, $\alpha=45^\circ$; c) $M%s$, $N%s$." % (par_tex(R, dr), par_tex(Pp, ds, M_), pv(H), pv(MN[0]), pv(MN[1]))))

# ---------------- 30. Juny 2006 ----------------
A, B, C = V(4, -4, 9), V(2, 0, 5), V(4, 2, 6)
Lp, Mp, Np = V(1, 1, 4), V(0, 2, 3), V(3, 0, 5)
Mab = mid(A, B)
dd = d2_pp(C, Mab)
cx, c = crossx(sub(B, A), sub(C, A))
ck(dd == 18 and n2(c) == 324)
de, te = plane3x(A, B, C, "A", "B", "C", r"\delta")
de2, te2 = plane3x(Lp, Mp, Np, "L", "M", "N", r"\delta'")
ck(de == Pl((2, -1, -2), 6) and de2 == Pl((0, 1, 1), -5))
R, dr, tl = lineq(de, de2)
tg, c2, g = ang_x(de.n, de2.n, "pp", r"\vec n", r"\vec n'")
ck(c2 == F(1, 2))
sol(30, steps(
    ap_("a)") + r"Punt mitjà de $AB$: $%s$. $\ d=|(1,4,-1)|=\sqrt{18}=3\sqrt2$ u. Àrea: $$\overrightarrow{AB}\times\overrightarrow{AC}=%s,\qquad S=\frac{\sqrt{324}}{2}=9\ \text{u}^2$$" % (pv(Mab), cx),
    ap_("b) Pla $\\delta$.") + te,
    ap_("Pla $\\delta'$.") + te2,
    ap_("c) Recta $r$.") + tl,
    ap_("Angle.") + "$$" + tg + r"\Rightarrow\alpha=45^\circ$$",
) + res(r"a) $d=3\sqrt2$ u, $S=9$ u²; b) $\delta:%s$, $\delta':%s$; c) $r:%s$, $\alpha=45^\circ$." % (de.tex(), de2.tex(), par_tex(R, dr))))

# ---------------- 31. Setembre 2006 ----------------
p1, p2 = Pl((2, -2, -1), -9), Pl((4, -1, 1), -42)
R, dr, tl = lineq(p1, p2)
S1, S2 = V(1, 3, -4), V(3, -5, -2)
ds = prim(sub(S2, S1))
m = det3(sub(S1, R), dr, ds)
ck(m != 0)
cx, dt = crossx(dr, ds)
lam, mu, X, Y = feet(R, dr, S1, ds)
sol(31, steps(
    ap_("a) Recta $r$.") + tl + r" Recta $s$: $\overrightarrow{S_1S_2}=%s$, director $\vec d_s=%s$: $\ s:\ %s$." % (pv(sub(S2, S1)), pv(ds), par_tex(S1, ds, M_)),
    ap_("b)") + r"Els directors no són proporcionals, i amb $R%s\in r$, $S_1%s\in s$: $$[\overrightarrow{RS_1},\vec d_r,\vec d_s]=%s\neq0$$ Les rectes <strong>s'encreuen</strong> (no són coplanàries)." % (pv(R), pv(S1), detx(sub(S1, R), dr, ds)),
    ap_("c) Perpendicular comuna.") + r"El seu director és perpendicular als dos: $$\vec d_t=\vec d_r\times\vec d_s=%s$$" % cx,
    ap_("Punt $P$.") + r"Com que $r$ i $s$ s'encreuen, no tenen cap punt comú; el que té sentit és el punt on la perpendicular comuna $t$ talla $r$ (i on talla $s$). Prenem $X=%s\in r$ i $Y=%s\in s$ i imposem $\overrightarrow{XY}\perp\vec d_r$ i $\overrightarrow{XY}\perp\vec d_s$: s'obté $\lambda=%s$, $\mu=%s$, és a dir, $P=X%s$ (en $r$) i $Y%s$ (en $s$)." % (gp(R, dr), gp(S1, ds, M_), nm(lam), nm(mu), pv(X), pv(Y)),
) + res(r"a) $r:%s$, $s:%s$; b) s'encreuen; c) $\vec d_t=%s$; $r$ i $s$ no es tallen: $t$ talla $r$ en $%s$ i $s$ en $%s$." % (par_tex(R, dr), par_tex(S1, ds, M_), pv(prim(dt)), pv(X), pv(Y))))

# ---------------- 32. Setembre 2006 ----------------
pl, tp = plane3x(V(11, 1, 2), V(5, 7, 5), V(7, -1, -2), "A", "B", "C")
p1, p2 = Pl((1, 1, 1), -15), Pl((2, -7, 2), -3)
R, dr, tl = lineq(p1, p2)
t, Pp = meet_lp(R, dr, pl)
tg, s2, g = ang_x(dr, pl.n, "rp", r"\vec d_r", r"\vec n")
MN = []
den = dot(pl.n, dr)
for k in (1, -1):
    target = k * 3 * F(math.isqrt(int(n2(pl.n)))) if isq(n2(pl.n)) else None
    assert target is not None
    tt = (target - pl.ev(R)) / den
    X = pt_on(R, dr, tt)
    ck(d2_ppl(X, pl) == 9)
    MN.append(X)
sol(32, steps(
    ap_("a) Recta $r$.") + tl,
    ap_("Pla $\\pi$.") + tp,
    ap_("b) Punt $P$.") + r"Substituïm $%s$ en $\pi$: $\lambda=%s$, $P%s$." % (gp(R, dr), nm(t), pv(Pp)),
    ap_("Angle.") + "$$" + tg + r"\Rightarrow\alpha\approx%s$$" % gr(g),
    ap_("c)") + r"Per a $X=%s$, $\ d(X,\pi)=\dfrac{|%s|}{%s}=3$. Resolent les dues possibilitats del valor absolut:" % (gp(R, dr), lin([dot(pl.n, dr)], [r"\lambda"], pl.ev(R)), rq(n2(pl.n))) + r" $M%s$ i $N%s$." % (pv(MN[0]), pv(MN[1])),
) + res(r"a) $r:%s$, $\pi:%s$; b) $P%s$, $\alpha\approx%s$; c) $M%s$, $N%s$." % (par_tex(R, dr), pl.tex(), pv(Pp), gr(g), pv(MN[0]), pv(MN[1]))))

# ---------------- 33. Juny 2007 ----------------
R, dr = V(1, F(1, 2), F(3, 2)), V(2, -3, 3)
S, ds = V(3, F(-3, 2), 1), V(-2, 1, 4)
tt, uu, Pp = meet_ll(R, dr, S, ds)
tg, c2, g = ang_x(dr, ds, "rr", r"\vec d_r", r"\vec d_s")
pl = pl_pn(Pp, cross(dr, ds))
ck(pl.has(R) and pl.has(S))
sol(33, steps(
    ap_("Forma contínua estàndard.") + r"Dividim per 2 els numeradors amb $2y$, $2z$: $$r:\frac{x-1}{2}=\frac{y-\frac12}{-3}=\frac{z-\frac32}{3},\qquad s:\frac{x-3}{-2}=\frac{y+\frac32}{1}=\frac{z-1}{4}$$ $r$: $R\left(1,\tfrac12,\tfrac32\right)$, $\vec d_r=(2,-3,3)$; $\ s$: $S\left(3,-\tfrac32,1\right)$, $\vec d_s=(-2,1,4)$.",
    ap_("a) Punt de tall.") + r"$%s=%s$: de les dues primeres components, $\lambda=%s$, $\mu=%s$ (la tercera es compleix): $P%s$." % (gp(R, dr), gp(S, ds, M_), nm(tt), nm(uu), pv(Pp)),
    ap_("b) Angle.") + "$$" + tg + r"\Rightarrow\alpha\approx%s$$" % gr(g),
    ap_("c) Pla.") + r"$\vec n=\vec d_r\times\vec d_s=%s$ i passa per $P$: $\ %s$." % (crossx(dr, ds)[0], pl.tex()),
) + res(r"a) $P%s$; b) $\vec d_r=(2,-3,3)$, $\vec d_s=(-2,1,4)$, $\alpha\approx%s$; c) $%s$." % (pv(Pp), gr(g), pl.tex())))

# ---------------- 34. Juny 2007 ----------------
Q = V(3, -1, 4)
R, dr = V(-2, 0, 1), V(3, -2, 4)
ds = V(1, -1, 1)
td, d2 = dpr_x(Q, R, dr, "Q", "R")
m = det3(sub(Q, R), dr, ds)
ck(m != 0 and not par(dr, ds))
tl2, dl2 = dll_x(R, dr, Q, ds, "R", "Q")
sol(34, steps(
    ap_("a)") + r"$r$: $R(-2,0,1)$, $\vec d_r=(3,-2,4)$. " + td,
    ap_("b)") + r"$s$: $Q(3,-1,4)$, $\vec d_s=(1,-1,1)$. Els directors no són proporcionals i $$[\overrightarrow{RQ},\vec d_r,\vec d_s]=%s\neq0$$ Les rectes s'encreuen: <strong>no es tallen</strong>." % detx(sub(Q, R), dr, ds),
    ap_("c)") + tl2,
) + res(r"a) $%s$ u; b) s'encreuen; c) $%s$ u." % (sq(d2), sq(dl2))))

# ---------------- 35. Setembre 2007 ----------------
pl = Pl((2, 1, 3), -1)
Q = V(2, 1, 3)
td, d2 = dpl_x(Q, pl, "Q")
P1, P2, P3 = V(F(1, 2), 0, 0), V(0, 1, 0), V(0, 0, F(1, 3))
cx, c = crossx(sub(P2, P1), sub(P3, P1))
ar2 = n2(c) / 4
vol = abs(det3(sub(P2, P1), sub(P3, P1), sub(Q, P1))) / 6
ck(vol ** 2 == ar2 * d2 / 9)
sol(35, steps(
    ap_("a)") + "$" + td + "$",
    ap_("b) Talls amb els eixos.") + r"$y=z=0$: $2x=1$, $P_1\left(\tfrac12,0,0\right)$; $\ P_2(0,1,0)$; $\ P_3\left(0,0,\tfrac13\right)$. $$\overrightarrow{P_1P_2}\times\overrightarrow{P_1P_3}=%s\ \Rightarrow\ S=\frac12\left|%s\right|=%s\ \text{u}^2$$" % (cx, pvt(c), sq(ar2)),
    ap_("c)") + r"$$V=\frac16|[\overrightarrow{P_1P_2},\overrightarrow{P_1P_3},\overrightarrow{P_1Q}]|=\frac16\left|%s\right|=%s\ \text{u}^3$$ (també $V=\frac13\,S\,d(Q,\pi)$)." % (detx(sub(P2, P1), sub(P3, P1), sub(Q, P1)), nm(vol)),
) + res(r"a) $%s$ u; b) $%s$ u²; c) $%s$ u³." % (sq(d2), sq(ar2), nm(vol))))

# ---------------- 36. Setembre 2007 ----------------
p1, p2 = Pl((1, 2, 1), 3), Pl((2, 1, -1), -6)
tg, c2, g = ang_x(p1.n, p2.n, "pp", r"\vec n_1", r"\vec n_2")
ck(c2 == F(1, 4))
R, dr, tl = lineq(p1, p2)
pb = Pl((1, 1, 0), -1)
ck(pb.has(R) and dot(pb.n, dr) == 0)
for nn in (p1.n, p2.n):
    ck(F(dot(pb.n, nn)) ** 2 / (n2(pb.n) * n2(nn)) == F(3, 4))
sol(36, steps(
    ap_("a)") + "$$" + tg + r"\Rightarrow\alpha=60^\circ$$",
    ap_("b)") + tl,
    ap_("c)") + r"$\vec n=(1,1,0)$. $$\cos(\pi,\pi_1)=\frac{|1+2+0|}{\sqrt2\,\sqrt6}=\frac{3}{\sqrt{12}}=\frac{\sqrt3}{2},\qquad \cos(\pi,\pi_2)=\frac{|2+1+0|}{\sqrt2\,\sqrt6}=\frac{\sqrt3}{2}$$ Tots dos angles valen $30^\circ=\alpha/2$. A més, $\pi$ conté la recta $r$: $R%s$ compleix $x+y-1=0$ i $\vec d_r\cdot\vec n=0$. Per tant, $\pi$ és el pla bisector." % pv(R),
) + res(r"a) $60^\circ$; b) $r:%s$; c) $\pi$ forma $30^\circ$ amb cada pla i conté $r$." % par_tex(R, dr)))

# ---------------- 37. Juny 2008 ----------------
A, B = V(2, 1, 1), V(1, 0, -1)
R, dr = V(5, 0, -2), V(1, 1, -2)
med = pl_pn(mid(A, B), sub(B, A))
t, C = meet_lp(R, dr, med)
ck(d2_pp(C, A) == d2_pp(C, B) and C == V(F(9, 2), F(-1, 2), -1))
cx, c = crossx(sub(B, A), sub(C, A))
ar2 = n2(c) / 4
sol(37, steps(
    ap_("a)") + r"$r$: $R(5,0,-2)$, $\vec d=(1,1,-2)$. Els punts que equidisten de $A$ i $B$ formen el pla mediador: normal $\overrightarrow{AB}=(-1,-1,-2)$ pel punt mitjà $\left(\tfrac32,\tfrac12,0\right)$: $\ %s$. Tallem amb $r$: $(5+\lambda)+\lambda+2(-2-2\lambda)-2=0\Rightarrow\lambda=%s$: $C%s$." % (med.tex(), nm(t), pvt(C)),
    ap_("b)") + r"$\overrightarrow{AB}=%s$, $\overrightarrow{AC}=%s$: $\ \overrightarrow{AB}\times\overrightarrow{AC}=%s$. $$S=\frac{|\overrightarrow{AB}\times\overrightarrow{AC}|}{2}=%s\ \text{u}^2$$" % (pv(sub(B, A)), pvt(sub(C, A)), pvt(c), sq(ar2)),
) + res(r"a) $C%s$; b) $S=%s$ u²." % (pvt(C), sq(ar2))))

# ---------------- 38. Juny 2008 ----------------
p1, p2 = Pl((0, 1, 1), 0), Pl((1, -2, 0), -1)
R, dr, tl = lineq(p1, p2)
S, ds = V(0, 1, 3), V(2, 1, -1)
ck(pos_ll(R, dr, S, ds) == "paral·leles")
td, dl2 = dpr_x(S, R, dr, "S", "R")
sol(38, steps(
    ap_("a) Recta $r$.") + tl + r" Recta $s$: $\dfrac{x}{2}=\dfrac{y-1}{1}=\dfrac{z-3}{-1}$, és a dir, $s:\ %s$." % par_tex(S, ds, M_),
    ap_("b)") + r"$\vec d_r=\vec d_s=%s$: les rectes són paral·leles o coincidents. $S(0,1,3)$ no és de $r$ ($y+z=4\neq0$), així que són <strong>paral·leles</strong> (i distintes)." % pv(dr),
    ap_("c)") + r"Com que són paral·leles, $d(r,s)=d(S,r)$: " + td.replace("d(S,r)", "d(r,s)"),
) + res(r"Les rectes són paral·leles; $d(r,s)=%s$ u." % sq(dl2)))

# ---------------- 39. Setembre 2008 ----------------
p1 = Pl((1, 1, 1), -3)
p2a = Pl((1, 1, -2), 0)
R, dr, tl = lineq(p1, p2a)
sol(39, steps(
    ap_("a)") + r"$\vec n_1\cdot\vec n_2=(1,1,1)\cdot(1,1,-\alpha)=2-\alpha=0\Rightarrow\alpha=2$. Per a $\alpha=2$, $\pi_2:x+y-2z=0$. " + tl,
    ap_("b)") + r"Paral·lels: $(1,1,-\alpha)\parallel(1,1,1)\Rightarrow-\alpha=1\Rightarrow\alpha=-1$, i aleshores $\pi_2:x+y+z=0$ (diferent de $\pi_1$). $$d(\pi_1,\pi_2)=\frac{|-3-0|}{\sqrt3}=\sqrt3\approx1{,}73\ \text{u}$$",
) + res(r"a) $\alpha=2$, $r:%s$; b) $\alpha=-1$, $d=\sqrt3$ u." % par_tex(R, dr)))

# ---------------- 40. Setembre 2008 ----------------
pl = Pl((1, 1, 1), -6)
t, Mf = meet_lp(O, V(1, 1, 1), pl)
Os = sym(O, Mf)
ck(Mf == V(2, 2, 2) and Os == V(4, 4, 4))
pc = pl_pn(O, cross(V(1, 0, 0), V(1, 1, 1)))
ck(pc == Pl((0, 1, -1), 0))
sol(40, steps(
    ap_("a)") + r"Director $\vec n=(1,1,1)$: $\ r:(x,y,z)=\lambda(1,1,1)$.",
    ap_("b)") + r"Tallem $r$ amb $\pi$: $3\lambda=6\Rightarrow\lambda=2$, $M(2,2,2)$ (projecció de $O$). El simètric compleix que $M$ és el punt mitjà: $O'=2M-O=(4,4,4)$.",
    ap_("c)") + r"Conté l'eix $X$ (punt $O$, director $(1,0,0)$) i la recta $r$ (director $(1,1,1)$): $$\vec n=(1,0,0)\times(1,1,1)=%s$$ i passa per $O$: $\ y-z=0$." % crossx(V(1, 0, 0), V(1, 1, 1))[0],
) + res(r"a) $(x,y,z)=\lambda(1,1,1)$; b) $O'(4,4,4)$; c) $y-z=0$."))
