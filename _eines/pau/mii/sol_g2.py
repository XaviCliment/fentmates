# Solucions 41-80 del recull de geometria. S'executa dins de sol_geo.py (després de sol_g1.py).
# ruff: noqa


def angv(u, v, nu, nv):
    """angle entre dos vectors (amb signe), explicat"""
    t, c2, g = ang_x(u, v, "vv", nu, nv)
    return t, g


# ---------------- 41. Juny 2009 ----------------
A, B, C = V(4, 0, 0), V(0, 1, 0), V(0, 0, -2)
cx, c = crossx(sub(B, A), sub(C, A))
ar2 = n2(c) / 4
ck(ar2 == 21)
ab, ac, bc = n2(sub(B, A)), n2(sub(C, A)), n2(sub(C, B))
per = math.sqrt(ab) + math.sqrt(ac) + math.sqrt(bc)
tA, gA = angv(sub(B, A), sub(C, A), r"\overrightarrow{AB}", r"\overrightarrow{AC}")
tB, gB = angv(sub(A, B), sub(C, B), r"\overrightarrow{BA}", r"\overrightarrow{BC}")
tC, gC = angv(sub(A, C), sub(B, C), r"\overrightarrow{CA}", r"\overrightarrow{CB}")
ck(abs(gA + gB + gC - 180) < 1e-9)
sol(41, steps(
    ap_("Vèrtexs.") + r"Amb $y=z=0$: $x=4$, $A(4,0,0)$; amb $x=z=0$: $B(0,1,0)$; amb $x=y=0$: $-2z=4$, $C(0,0,-2)$.",
    ap_("a) Àrea.") + r"$\overrightarrow{AB}=%s$, $\overrightarrow{AC}=%s$: $\ \overrightarrow{AB}\times\overrightarrow{AC}=%s$. $$S=\frac{\sqrt{84}}{2}=\sqrt{21}\approx4{,}58\ \text{u}^2$$" % (pv(sub(B, A)), pv(sub(C, A)), cx),
    ap_("b) Perímetre.") + r"$|AB|=\sqrt{17}$, $|AC|=\sqrt{20}=2\sqrt5$, $|BC|=|(0,-1,-2)|=\sqrt5$: $\ p=\sqrt{17}+3\sqrt5\approx%s$ u." % ap(per),
    ap_("c) Angles.") + r"Amb el producte escalar dels vectors que ixen de cada vèrtex: $$%s\Rightarrow\hat A\approx%s$$ $$%s\Rightarrow\hat B\approx%s$$ $$%s\Rightarrow\hat C\approx%s$$ (sumen $180^\circ$ ✓)." % (tA, gr(gA), tB, gr(gB), tC, gr(gC)),
) + res(r"a) $\sqrt{21}$ u²; b) $\sqrt{17}+3\sqrt5\approx%s$ u; c) $\hat A\approx%s$, $\hat B\approx%s$, $\hat C\approx%s$." % (ap(per), gr(gA), gr(gB), gr(gC))))

# ---------------- 42. Juny 2009 ----------------
P0 = V(0, 0, 12)
pls = []
for t in (4, 8):
    Q = V(4, 4, t)
    pl = pl_pn(P0, Q)
    ck(pl.has(Q))
    pls.append(pl)
ck(pls[0] == Pl((1, 1, 1), -12) and pls[1] == Pl((1, 1, 2), -24))
sol(42, steps(
    ap_("a)") + r"El vector normal de $z=0$ és $(0,0,1)$: la recta és $(x,y,z)=(4,4,0)+\lambda(0,0,1)$, és a dir, $\begin{cases}x=4\\ y=4\end{cases}$.",
    ap_("b)") + r"Els punts de la recta $x=y=4$ són $Q(4,4,t)$. El pla és perpendicular a $OQ$, així que el seu vector normal és $\overrightarrow{OQ}=(4,4,t)$. Com que passa per $P$ i per $Q$, el vector $\overrightarrow{PQ}=(4,4,t-12)$ és del pla i ha de ser perpendicular al normal: $$\overrightarrow{OQ}\cdot\overrightarrow{PQ}=16+16+t(t-12)=0\Rightarrow t^2-12t+32=0\Rightarrow t=4\ \text{o}\ t=8$$",
    ap_("Plans.") + r"$t=4$: $Q(4,4,4)$, normal $(1,1,1)$ per $P$: $%s$. $\ t=8$: $Q(4,4,8)$, normal $(1,1,2)$ per $P$: $%s$." % (pls[0].tex(), pls[1].tex()),
) + res(r"a) $x=4,\ y=4$; b) dues solucions: $%s$ (amb $Q(4,4,4)$) o $%s$ (amb $Q(4,4,8)$)." % (pls[0].tex(), pls[1].tex())))

# ---------------- 43. Setembre 2009 ----------------
P0, Q = V(3, -1, 4), V(1, 0, -1)
pl = Pl((1, -2, 2), 5)
q1, q2 = Pl((2, 1, 0), -5), Pl((0, 1, 1), -3)
ck(q1.has(P0) and q2.has(P0) and dot(q1.n, pl.n) == 0 and dot(q2.n, pl.n) == 0)
pp = pl_pn(P0, cross(sub(Q, P0), pl.n))
ck(pp.has(Q) and pp == Pl((8, 1, -3), -11))
sol(43, steps(
    ap_("a)") + r"Director $\vec n=(1,-2,2)$: $\ r:\ \dfrac{x-3}{1}=\dfrac{y+1}{-2}=\dfrac{z-4}{2}$, és a dir, $%s$." % par_tex(P0, pl.n),
    ap_("b)") + r"Un pla perpendicular a $\pi$ conté la direcció $\vec n$; si a més passa per $P$, conté tota la recta $r$. Per tant, n'hi ha infinits: són els plans del feix d'eix $r$. De la forma contínua: $-2(x-3)=y+1$ i $2(y+1)=-2(z-4)$, és a dir, $r:\begin{cases}2x+y-5=0\\ y+z-3=0\end{cases}$, i els plans són $$(2x+y-5)+\mu(y+z-3)=0,\ \mu\in\mathbb{R}\quad(\text{i també }y+z-3=0)$$",
    ap_("c)") + r"$\overrightarrow{PQ}=(-2,1,-5)$ i $\vec n=(1,-2,2)$ són del pla: $$\vec n'=\overrightarrow{PQ}\times\vec n=%s$$ Per $P$: $\ \pi':%s$." % (crossx(sub(Q, P0), pl.n)[0], pp.tex()),
) + res(r"a) $%s$; b) el feix $(2x+y-5)+\mu(y+z-3)=0$; c) $%s$." % (par_tex(P0, pl.n), pp.tex())))

# ---------------- 44. Setembre 2009 ----------------
A, B, C = V(4, 0, 0), V(0, 6, 0), V(0, 0, 3)
pl = Pl((3, 2, 4), -12)
ck(all(pl.has(X) for X in (A, B, C)))
tA, gA = angv(sub(B, A), sub(C, A), r"\overrightarrow{AB}", r"\overrightarrow{AC}")
tB, gB = angv(sub(A, B), sub(C, B), r"\overrightarrow{BA}", r"\overrightarrow{BC}")
tC, gC = angv(sub(A, C), sub(B, C), r"\overrightarrow{CA}", r"\overrightarrow{CB}")
ck(abs(gA + gB + gC - 180) < 1e-9)
sol(44, steps(
    ap_("a)") + r"Plans $3x+2y+4z+D=0$ amb $\dfrac{|D+12|}{\sqrt{9+4+16}}=5\Rightarrow|D+12|=5\sqrt{29}\Rightarrow D=-12\pm5\sqrt{29}$.",
    ap_("b)") + r"$A(4,0,0)$, $B(0,6,0)$, $C(0,0,3)$.",
    ap_("c)") + r"$$%s\Rightarrow\hat A\approx%s$$ $$%s\Rightarrow\hat B\approx%s$$ $$%s\Rightarrow\hat C\approx%s$$" % (tA, gr(gA), tB, gr(gB), tC, gr(gC)),
) + res(r"a) $3x+2y+4z-12+5\sqrt{29}=0$ i $3x+2y+4z-12-5\sqrt{29}=0$; b) $A(4,0,0)$, $B(0,6,0)$, $C(0,0,3)$; c) $\hat A\approx%s$, $\hat B\approx%s$, $\hat C\approx%s$." % (gr(gA), gr(gB), gr(gC))))

# ---------------- 45. Juny 2010 ----------------
R, dr, tl = lineq(Pl((5, 1, -1), -4), Pl((2, -2, -1), 5))
S, ds, tl2 = lineq(Pl((1, -1, 0), 5), Pl((0, 0, 1), -4), "s", M_)
m = det3(sub(S, R), dr, ds)
ck(m != 0 and not par(dr, ds))
tdl, dl2 = dll_x(R, dr, S, ds, "R", "S")
n = cross(dr, ds)
Dm = -(dot(n, R) + dot(n, S)) / 2
pm = Pl(n, Dm)
ck(d2_ppl(R, pm) == d2_ppl(S, pm) and dot(pm.n, dr) == 0 and dot(pm.n, ds) == 0)
sol(45, steps(
    ap_("Recta $r$.") + tl,
    ap_("Recta $s$.") + tl2,
    ap_("a)") + r"Els directors no són proporcionals i $$[\overrightarrow{RS},\vec d_r,\vec d_s]=%s\neq0$$ Les rectes es creuen." % detx(sub(S, R), dr, ds),
    ap_("b)") + tdl,
    ap_("c)") + r"El pla és paral·lel a les dues rectes: $\vec n=\vec d_r\times\vec d_s=%s$, $\ %s+D=0$. Equidista de les rectes si equidista de $R$ i de $S$, és a dir, si està a mig camí entre el pla paral·lel que conté $r$ ($D_r=-\vec n\cdot R=%s$) i el que conté $s$ ($D_s=-\vec n\cdot S=%s$): $D=\dfrac{D_r+D_s}{2}=%s$." % (pv(n), lin(n), nm(-dot(n, R)), nm(-dot(n, S)), nm(Dm)),
) + res(r"a) S'encreuen; b) $d=%s$ u; c) $\pi:%s$." % (sq(dl2), pm.tex())))

# ---------------- 46. Juny 2010 ----------------
P0, d = V(0, 3, -1), V(2, -1, 1)
A = V(0, 1, 0)
td, d2 = dpr_x(A, P0, d, "A", "P")
tg, c2, g = ang_x(sub(A, P0), d, "rr", r"\overrightarrow{PA}", r"\vec d")
t, Q = meet_lp(P0, d, Pl((0, 0, 1), 0))
ck(Q == V(2, 2, 0))
gp_ = dot(sub(A, P0), sub(Q, P0))
gq_ = dot(sub(A, Q), sub(P0, Q))
ck(gp_ == gq_ and n2(sub(Q, P0)) == n2(sub(P0, Q)))
sol(46, steps(
    ap_("a)") + td,
    ap_("b)") + r"$\overrightarrow{PA}=%s$: $$%s\Rightarrow\alpha\approx%s$$" % (pv(sub(A, P0)), tg, gr(g)),
    ap_("c)") + r"$(2\lambda,\,3-\lambda,\,-1+\lambda)$ amb $z=0$: $\lambda=1$, $Q(2,2,0)$. $$\cos\hat P=\frac{\overrightarrow{PA}\cdot\overrightarrow{PQ}}{|\overrightarrow{PA}||\overrightarrow{PQ}|}=\frac{(0,-2,1)\cdot(2,-1,1)}{\sqrt5\sqrt6}=\frac{3}{\sqrt{30}},\qquad \cos\hat Q=\frac{\overrightarrow{QA}\cdot\overrightarrow{QP}}{|\overrightarrow{QA}||\overrightarrow{QP}|}=\frac{(-2,-1,0)\cdot(-2,1,-1)}{\sqrt5\sqrt6}=\frac{3}{\sqrt{30}}$$ Els angles en $P$ i $Q$ són iguals (el triangle és isòsceles: $|AP|=|AQ|=\sqrt5$).",
) + res(r"a) $%s$ u; b) $\alpha\approx%s$; c) $\cos\hat P=\cos\hat Q=\frac{3}{\sqrt{30}}$, $\hat P=\hat Q\approx%s$." % (sq(d2), gr(g), gr(g))))

# ---------------- 47. Setembre 2010 ----------------
pl, tp = plane3x(V(0, 0, 0), V(6, -3, 0), V(3, 0, 1), "O", "A", "B")
ck(pl == Pl((1, 2, -3), 0))
P0 = V(8, 7, -2)
t, Q = meet_lp(P0, pl.n, pl)
ck(Q == V(6, 3, 4))
sol(47, steps(
    ap_("a)") + tp,
    ap_("b)") + r"Director $\vec n=(1,2,-3)$: $\ r:\ %s$." % par_tex(P0, pl.n),
    ap_("c)") + r"El punt del pla més pròxim a $P$ és el peu de la perpendicular, és a dir, $Q=r\cap\pi$: $(8+\lambda)+2(7+2\lambda)-3(-2-3\lambda)=0\Rightarrow28+14\lambda=0\Rightarrow\lambda=-2$, $Q(6,3,4)$. (Per a qualsevol altre $X\in\pi$, pel teorema de Pitàgores $|PX|^2=|PQ|^2+|QX|^2>|PQ|^2$.)",
) + res(r"a) $x+2y-3z=0$; b) $%s$; c) $Q(6,3,4)$." % par_tex(P0, pl.n)))

# ---------------- 48. Setembre 2010 ----------------
R, dr, S, ds = V(4, 4, 4), V(3, 2, 1), V(0, 0, 0), V(1, 2, 3)
tt, uu, Pp = meet_ll(R, dr, S, ds)
tg, c2, g = ang_x(dr, ds, "rr", r"\vec d_r", r"\vec d_s")
ck(Pp == V(1, 2, 3) and c2 == F(25, 49))
pl = pl_pn(Pp, cross(dr, ds))
ck(pl == Pl((1, -2, 1), 0))
sol(48, steps(
    ap_("a)") + r"$r$: $R(4,4,4)$, $\vec d_r=(3,2,1)$; $\ s$: $O(0,0,0)$, $\vec d_s=(1,2,3)$. Igualem $(4+3\lambda,4+2\lambda,4+\lambda)=(\mu,2\mu,3\mu)$: de les dues primeres, $\lambda=-1$, $\mu=1$, i la tercera es compleix ($3=3$): $P(1,2,3)$.",
    ap_("b)") + "$$" + tg + r"\Rightarrow\alpha\approx%s$$" % gr(g),
    ap_("c)") + r"$\vec n=\vec d_r\times\vec d_s=%s\parallel(1,-2,1)$, per l'origen: $\ x-2y+z=0$." % crossx(dr, ds)[0],
) + res(r"a) $P(1,2,3)$; b) $\cos\alpha=\frac57$, $\alpha\approx%s$; c) $x-2y+z=0$." % gr(g)))

# ---------------- 49. Juny 2011 ----------------
R, dr, tl = lineq(Pl((1, 0, 1), -2), Pl((2, -1, 1), 0))
S, ds, tl2 = lineq(Pl((2, -1, 0), -3), Pl((1, -1, -1), -2), "s", M_)
pos = pos_ll(R, dr, S, ds)
m = det3(sub(S, R), dr, ds)
pl = pl_pn(R, cross(dr, ds))
ck(pl.has(pt_on(R, dr, 1)) and dot(pl.n, ds) == 0)
sol(49, steps(
    ap_("a) Recta $r$.") + tl,
    ap_("Recta $s$.") + tl2,
    ap_("b)") + r"Directors no proporcionals; $$[\overrightarrow{RS},\vec d_r,\vec d_s]=%s$$" % detx(sub(S, R), dr, ds) + (r"Les rectes <strong>s'encreuen</strong>." if m != 0 else r"Les rectes <strong>es tallen</strong>."),
    ap_("c)") + r"Passa per $R$ i té per normal $\vec d_r\times\vec d_s=%s$: $\ %s$." % (crossx(dr, ds)[0], pl.tex()),
) + res(r"a) $R%s$, $\vec d_r=%s$; $S%s$, $\vec d_s=%s$; b) %s; c) $%s$." % (pv(R), pv(dr), pv(S), pv(ds), pos, pl.tex())))

# ---------------- 50. Juny 2011 ----------------
R, dr, S, ds = V(0, 1, 3), V(1, -1, 0), V(1, 0, 3), V(1, 1, 1)
tt, uu, X = meet_ll(R, dr, S, ds)
pl = pl_pn(X, cross(dr, ds))
ck(X == V(1, 0, 3) and pl == Pl((1, 1, -2), 5))
sol(50, steps(
    ap_("a)") + r"$\vec d_r=(1,-1,0)$; $s$ en forma contínua és $\dfrac{x-1}{1}=\dfrac{y}{1}=\dfrac{z-3}{1}$: $\vec d_s=(1,1,1)$.",
    ap_("b)") + r"Normal $(1,-1,0)$ pel punt $(0,1,3)$: $x-y+D=0$, $-1+D=0$: $\ x-y+1=0$.",
    ap_("c)") + r"Punt de $s$: $(1+\mu,\mu,3+\mu)$. Igualant amb $(\lambda,1-\lambda,3)$: $\mu=0$, $\lambda=1$: el punt de tall és $(1,0,3)$. Pla: $\vec n=\vec d_r\times\vec d_s=%s$, és a dir $(1,1,-2)$: $\ \pi:%s$." % (crossx(dr, ds)[0], pl.tex()),
) + res(r"a) $(1,-1,0)$ i $(1,1,1)$; b) $x-y+1=0$; c) $(1,0,3)$ i $%s$." % pl.tex()))

# ---------------- 51. Setembre 2011 ----------------
R, dr = V(3, -1, 2), V(1, 2, 1)
ds = cross(V(1, 2, 0), V(0, 3, -1))
s1, s2 = Pl((1, 2, 0), -1), Pl((0, 3, -1), 5)
ck(s1.has(R) and s2.has(R))
pl = pl_pn(R, cross(dr, ds))
ck(pl == Pl((1, -1, 1), -6))
pp = pl_pn(V(1, 2, 1), dr)
sol(51, steps(
    ap_("a)") + r"$\vec d_s=(1,2,0)\times(0,3,-1)=%s$ no és proporcional a $\vec d_r$, així que les rectes són coplanàries si i només si es tallen. Substituïm el punt genèric de $r$, $(3+\lambda,-1+2\lambda,2+\lambda)$, en la primera equació de $s$: $3+\lambda-2+4\lambda-1=5\lambda=0\Rightarrow\lambda=0$. L'únic candidat és $(3,-1,2)$; en la segona: $-3-2+2+\alpha=0\Rightarrow\alpha=3$." % pv(ds),
    ap_("b)") + r"Per a $\alpha=3$ es tallen en $(3,-1,2)$. $\vec n=\vec d_r\times\vec d_s=%s\parallel(1,-1,1)$: $\ %s$." % (crossx(dr, ds)[0], pl.tex()),
    ap_("c)") + r"Normal $\vec d_r=(1,2,1)$ pel punt $(1,2,1)$: $\ %s$." % pp.tex(),
) + res(r"a) $\alpha=3$; b) $%s$; c) $%s$." % (pl.tex(), pp.tex())))

# ---------------- 52. Setembre 2011 ----------------
dr = V(4, 1, 1)


def pa(al):
    al = F(al)
    return Pl((2 + 2 * al, 1, al), -2 - 6 * al)


ck(pa(F(1, 4)).has(V(1, 1, 0)) and pa(F(1, 4)) == Pl((10, 4, 1), -14))
ck(dot(pa(-1).n, dr) == 0 and not pa(-1).has(O) and pa(-1) == Pl((0, 1, -1), 4))
ck(par(pa(1).n, dr) and pa(1) == Pl((4, 1, 1), -8))
sol(52, steps(
    ap_("Recta $r$.") + r"$x=4y$, $z=y$: $(x,y,z)=\lambda(4,1,1)$, director $\vec d=(4,1,1)$. El pla té normal $\vec n_\alpha=(2+2\alpha,\,1,\,\alpha)$.",
    ap_("a)") + r"$(2+2\alpha)+1+0-2-6\alpha=0\Rightarrow1-4\alpha=0\Rightarrow\alpha=\frac14$: $\frac52x+y+\frac14z-\frac72=0$, és a dir, $10x+4y+z-14=0$.",
    ap_("b)") + r"Paral·lel a $r$: $\vec n_\alpha\cdot\vec d=4(2+2\alpha)+1+\alpha=9+9\alpha=0\Rightarrow\alpha=-1$: $\ y-z+4=0$ (l'origen, que és de $r$, no hi és: és paral·lel, no la conté).",
    ap_("c)") + r"Perpendicular a $r$: $\vec n_\alpha\parallel\vec d$: $\dfrac{2+2\alpha}{4}=\dfrac11=\dfrac{\alpha}{1}\Rightarrow\alpha=1$ (i $2+2\cdot1=4$ ✓): $\ 4x+y+z-8=0$.",
) + res(r"a) $10x+4y+z-14=0$; b) $y-z+4=0$; c) $4x+y+z-8=0$."))

# ---------------- 53. Juny 2012 ----------------
R1, d1, R2, d2v = V(1, 0, 2), V(2, 1, -1), V(-1, 1, -1), V(0, 1, -2)
tt, uu, X = meet_ll(R1, d1, R2, d2v)
pl = pl_pn(X, cross(d1, d2v))
ck(X == V(-1, -1, 3) and pl == Pl((1, -4, -2), 3))
td, dd2 = dpr_x(V(0, 0, 1), R2, d2v, "A", "R_2", "r_2")
sol(53, steps(
    ap_("a)") + r"$1+2\alpha=-1\Rightarrow\alpha=-1$; aleshores $y=-1=1+\beta\Rightarrow\beta=-2$ i $z$: $2-(-1)=3$ i $-1-2(-2)=3$ ✓. Punt de tall $(-1,-1,3)$.",
    ap_("b)") + r"$\vec n=\vec d_1\times\vec d_2=%s$, pel punt $(-1,-1,3)$: $\ %s$." % (crossx(d1, d2v)[0], pl.tex()),
    ap_("c)") + r"Amb $A(0,0,1)$ i $R_2(-1,1,-1)\in r_2$: " + td,
) + res(r"a) $(-1,-1,3)$; b) $%s$; c) $%s$ u." % (pl.tex(), sq(dd2))))

# ---------------- 54. Juny 2012 ----------------
R, dr, tl = lineq(Pl((1, -2, -2), -1), Pl((1, 5, -1), 0))
ck(dr == V(12, -1, 7))
pval = 2 * R[0] + R[1] + F(-23, 7) * R[2]
ck(pval == F(9, 7))
sol(54, steps(
    ap_("Recta $r$.") + tl,
    ap_("Condició.") + r"$\vec n=(2,1,n)$: $\ \vec n\cdot\vec d=24-1+7n=23+7n$.",
    ap_("a)") + r"Es tallen en un punt si $\vec n\cdot\vec d\neq0$: $\ n\neq-\frac{23}{7}$ (per a qualsevol $p$).",
    ap_("b)") + r"Si $n=-\frac{23}{7}$, la recta és paral·lela o continguda. Està continguda si $R%s\in\pi$: $%s=p\Rightarrow p=\frac97$." % (pv(R), r"2\cdot(%s)+%s-\frac{23}{7}\cdot(%s)" % (nm(R[0]), nm(R[1]), nm(R[2]))),
    ap_("c)") + r"No el talla (paral·lela) si $n=-\frac{23}{7}$ i $p\neq\frac97$.",
) + res(r"a) $n\neq-\frac{23}{7}$; b) $n=-\frac{23}{7}$, $p=\frac97$; c) $n=-\frac{23}{7}$ i $p\neq\frac97$."))

# ---------------- 55. Setembre 2012 ----------------
R, dr, tl = lineq(Pl((1, 1, -1), -1), Pl((1, -1, -1), 0))
ck(dr == V(1, 0, 1))
ck(R[2] == 0)
plp = Pl((1, 0, -1), 0)
ck(not plp.has(R))
dd2 = d2_ppl(R, plp)
ck(dd2 == F(1, 8))
sol(55, steps(
    ap_("a)") + tl,
    ap_("b)") + r"$\vec n=(1,0,m)$. Perpendiculars si $\vec n\parallel\vec d=(1,0,1)$: $m=1$.",
    ap_("c)") + r"Paral·lels si $\vec n\cdot\vec d=1+m=0$: $m=-1$, i $R%s$ no és de $\pi:x-z=0$ ($%s\neq0$), així que no la conté." % (pvt(R), tn(plp.ev(R))),
    ap_("d)") + r"$d(r,\pi)=d(R,\pi)=\dfrac{|%s-0|}{\sqrt{1+1}}=%s\approx%s$ u." % (tn(R[0]), rq(dd2), ap(math.sqrt(float(dd2)))),
) + res(r"a) $(1,0,1)$; b) $m=1$; c) $m=-1$; d) $\frac{\sqrt2}{4}$ u."))

# ---------------- 56. Setembre 2012 ----------------
pi_, si_ = Pl((2, -1, 1), -3), Pl((1, -1, 1), -2)
R, dr, tl = lineq(pi_, si_)
ck(dr == V(0, 1, 1) and 3 * R[0] - R[1] + R[2] == 4)
tp, pb = pencil_x(pi_, si_, V(2, 1, 3), r"\pi", r"\sigma")
ck(pb == Pl((1, 1, -1), 0))
tau = Pl((3, -1, 1), -4)
ck(tau.has(R) and tau.has(pt_on(R, dr, 1)))
sol(56, steps(
    ap_("a)") + tl + r" Restant les equacions s'obté directament $x=1$; contínua: $\ x=1,\ \dfrac{y-%s}{%s}=\dfrac{z-%s}{%s}$." % (nm(R[1]), nm(dr[1]), nm(R[2]), nm(dr[2])),
    ap_("b)") + tp,
    ap_("c)") + r"$\tau$ conté $r$ si $\vec n_\tau\cdot\vec d=0$ i $R\in\tau$: $(3,-1,-a)\cdot%s=%s=0\Rightarrow a=-1$; $\ R%s\in\tau$: $3\cdot%s-%s+%s=b\Rightarrow b=4$." % (pv(dr), "-1-a", pv(R), pr_(R[0]), pr_(R[1]), pr_(R[2])),
) + res(r"a) $R%s$, $\vec d=%s$; b) $x+y-z=0$; c) $a=-1$, $b=4$." % (pv(R), pv(dr))))

# ---------------- 57. Juny 2013 ----------------
A, B, C = V(1, 0, 1), V(2, 1, 0), V(0, 2, 3)
cx, c = crossx(A, B)
vol = abs(det3(A, B, C)) / 6
pl = pl_pn(O, c)
tdc, dc2 = dpl_x(C, pl, "C")
Cm = mid(O, C)
tdm, dm2 = dpl_x(Cm, pl, "C'")
ck(vol == F(7, 6) and dm2 * 4 == dc2)
sol(57, steps(
    ap_("a)") + r"$\overrightarrow{OA}\times\overrightarrow{OB}=%s$: $\ S=\dfrac{\sqrt6}{2}\approx1{,}22$ u². $$V=\frac16|[\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC}]|=\frac16\left|%s\right|=\frac76\ \text{u}^3$$" % (cx, detx(A, B, C)),
    ap_("b)") + r"Pla $OAB$: normal $(-1,2,1)$ per l'origen: $\ %s$. $$%s$$" % (pl.tex(), tdc),
    ap_("c)") + r"$C'=%s$: $$%s$$ És la meitat de l'anterior, com era d'esperar: $O$ és del pla i $C'$ és el punt mitjà de $OC$." % (pvt(Cm), tdm),
) + res(r"a) $\frac{\sqrt6}{2}$ u² i $\frac76$ u³; b) $%s$ u; c) $%s$ u." % (sq(dc2), sq(dm2))))

# ---------------- 58. Juny 2013 ----------------
A, B, C, P0 = V(1, 0, 1), V(2, -1, 0), V(0, 1, 1), V(0, -3, 2)
tdl, dl2 = dpr_x(P0, A, sub(B, A), "P", "A", "AB")
pl, tp = plane3x(A, B, C)
tdp, dp2 = dpl_x(P0, pl)
sol(58, steps(
    ap_("a)") + r"$\overrightarrow{AP}=%s$: $\ d(P,A)=%s$ u." % (pv(sub(P0, A)), sq(n2(sub(P0, A)))),
    ap_("b)") + r"Recta $AB$: punt $A$, $\vec d=\overrightarrow{AB}=%s$. " % pv(sub(B, A)) + tdl,
    ap_("c)") + tp + "$$" + tdp + "$$",
) + res(r"a) $\sqrt{11}$ u; b) $%s$ u; c) $%s$ u." % (sq(dl2), sq(dp2))))

# ---------------- 59. Juliol 2013 ----------------
R1, d1, R2, d2v = V(1, 0, 2), V(2, 1, -1), V(-1, 1, -1), V(0, 1, -2)
tt, uu, X = meet_ll(R1, d1, R2, d2v)
pl = pl_pn(X, cross(d1, d2v))
Pp, Qp = V(-1, 0, 1), V(0, 1, 2)
cx, c = crossx(sub(Qp, Pp), sub(X, Pp))
ar2 = n2(c) / 4
ck(ar2 == F(14, 4))
sol(59, steps(
    ap_("a)") + r"Aïllem el paràmetre: $\alpha=y$, i aleshores $x=1+2y$, $z=2-y$: $\ r_1:\begin{cases}x-2y-1=0\\ y+z-2=0\end{cases}$.",
    ap_("b)") + r"Les rectes es tallen en $R(-1,-1,3)$ ($\alpha=-1$, $\beta=-2$) i no són paral·leles, per tant són coplanàries. $\vec n=\vec d_1\times\vec d_2=%s$: $\ \pi:%s$." % (crossx(d1, d2v)[0], pl.tex()),
    ap_("c)") + r"$\overrightarrow{PQ}=%s$, $\overrightarrow{PR}=%s$: $\ \overrightarrow{PQ}\times\overrightarrow{PR}=%s$. $\ S=\dfrac{\sqrt{14}}{2}\approx1{,}87$ u²." % (pv(sub(Qp, Pp)), pv(sub(X, Pp)), cx),
) + res(r"a) $x-2y-1=0,\ y+z-2=0$; b) $%s$; c) $\frac{\sqrt{14}}{2}$ u²." % pl.tex()))

# ---------------- 60. Juliol 2013 ----------------
R, dr, tl = lineq(Pl((1, -1, 1), 0), Pl((2, 1, 1), -1))
S, ds = V(1, 2, 0), V(1, 1, 1)
m = det3(sub(S, R), dr, ds)
ck(m != 0)
tdl, dl2 = dll_x(R, dr, S, ds, "R", "S")
cx, dt = crossx(dr, ds)
Pt = V(F(41, 57), F(-14, 57), 0)
sol(60, steps(
    ap_("a) Recta $r$.") + tl + r" Recta $s$: $S(1,2,0)$, $\vec d_s=(1,1,1)$.",
    ap_("b)") + r"Els directors no són proporcionals. " + tdl + r" Com que el producte mixt no és zero, les rectes s'encreuen.",
    ap_("c)") + r"La recta $t$ és perpendicular a les dues, així que el seu director és $\vec d_r\times\vec d_s=%s$: $$t:\ (x,y,z)=\left(\tfrac{41}{57},-\tfrac{14}{57},0\right)+\lambda%s$$" % (cx, pv(prim(dt))),
) + res(r"b) $d(r,s)=%s$ u; c) $t:(x,y,z)=\left(\frac{41}{57},-\frac{14}{57},0\right)+\lambda%s$." % (sq(dl2), pv(prim(dt)))))

# ---------------- 61. Juny 2014 ----------------
A = V(-1, 0, 2)
R, dr = V(1, 0, 2), V(2, 3, 1)
S, ds = V(-1, 1, 1), V(-2, 3, 1)
ppi = pl_pn(A, cross(dr, sub(A, R)))
psi = pl_pn(A, ds)
ck(ppi == Pl((0, 1, -3), 6) and ppi.has(R) and psi == Pl((2, -3, -1), 4))
Lp, dl, tl = lineq(ppi, psi, "l")
pos = pos_ll(S, ds, Lp, dl)
m = det3(sub(Lp, S), ds, dl)
if m != 0:
    tdl, dl2 = dll_x(S, ds, Lp, dl, "S", "L", "s", "l")
sol(61, steps(
    ap_("a)") + r"$\overrightarrow{RA}=(-2,0,0)$ amb $R(1,0,2)\in r$: $\ \vec n=\vec d_r\times\overrightarrow{RA}=%s$: $\ \pi:%s$." % (crossx(dr, sub(A, R))[0], ppi.tex()),
    ap_("b)") + r"Normal $\vec d_s=(-2,3,1)$ per $A$: $-2x+3y+z+D=0$, $2+2+D=0$: $\ \sigma:%s$." % psi.tex(),
    ap_("c)") + tl,
    ap_("Distància.") + (tdl if m != 0 else r"Es tallen: $d=0$."),
) + res(r"a) $%s$; b) $%s$; c) $\vec d_l=%s$, $d(s,l)=%s$ u." % (ppi.tex(), psi.tex(), pv(dl), sq(dl2) if m != 0 else "0")))

# ---------------- 62. Juny 2014 ----------------
A, B, C = V(1, 2, -2), V(0, -3, 1), V(-1, 0, 0)
pT, tT = plane3x(A, B, C, "A", "B", "C", r"\pi_T")
ck(pT == Pl((1, 1, 2), 1))
p1 = Pl((1, 1, 1), 1)
n2v = cross(V(-1, 1, 1), V(1, -2, 1))
p2 = pl_pn(V(1, 0, 0), n2v)
ck(p2 == Pl((3, 2, 1), -3))
tg, c2, g = ang_x(p1.n, n2v, "vv", r"\vec n_1", r"\vec n_2")
R, dr, tl = lineq(p1, p2)
sol(62, steps(
    r"<em>Nota: a l'enunciat del recull apareix $A(1,2-2)$; és $A(1,2,-2)$.</em>",
    ap_("a) Pla del triangle.") + tT + r" Els normals $(1,1,2)$ i $(1,1,1)$ no són proporcionals: els plans són <strong>secants</strong>.",
    ap_("b)") + r"$\vec n_1=(1,1,1)$. El pla $\pi_2$ passa per $(1,0,0)$ i té vectors $(-1,1,1)$ i $(1,-2,1)$: $\ \vec n_2=%s$. $$%s$$" % (crossx(V(-1, 1, 1), V(1, -2, 1))[0], tg),
    ap_("c)") + r"$\pi_2:%s$. " % p2.tex() + tl,
) + res(r"a) Secants; b) $\vec n_1=(1,1,1)$, $\vec n_2=(3,2,1)$, $\cos\alpha=\frac{\sqrt{42}}{7}\approx%s$; c) $%s$." % (ap(math.sqrt(42) / 7, 3), par_tex(R, dr))))

# ---------------- 63. Juliol 2014 ----------------
A, B = V(1, 5, 7), V(3, -1, -1)
d = prim(sub(B, A))
Mm = mid(A, B)
q1, q2 = pl_pn(A, d), pl_pn(Mm, d)
ck(q1 == Pl((1, -3, -4), 42) and q2 == Pl((1, -3, -4), 16))
Cp = V(1, 0, 1)
pts = []
for t in (1, 2):
    X = pt_on(A, d, t)
    ck(d2_pp(X, Cp) == 9)
    pts.append(X)
sol(63, steps(
    ap_("a)") + r"$\overrightarrow{AB}=(2,-6,-8)\parallel(1,-3,-4)$ és normal als dos plans. $\pi_1$ per $A$: $\ %s$. Punt mitjà $M(2,2,3)$: $\ \pi_2:%s$." % (q1.tex(), q2.tex()),
    ap_("b)") + r"Són paral·lels: $d(\pi_1,\pi_2)=\dfrac{|42-16|}{\sqrt{1+9+16}}=\dfrac{26}{\sqrt{26}}=\sqrt{26}\approx5{,}10$ u (és la meitat de $|AB|=2\sqrt{26}$).",
    ap_("c)") + r"$r:\ %s$. Si $X=(1+\lambda,5-3\lambda,7-4\lambda)$, $\ \overrightarrow{CX}=(\lambda,5-3\lambda,6-4\lambda)$ i $$|\overrightarrow{CX}|^2=26\lambda^2-78\lambda+61=9\Rightarrow\lambda^2-3\lambda+2=0\Rightarrow\lambda=1,\ \lambda=2$$" % par_tex(A, d),
) + res(r"a) $%s$ i $%s$; b) $\sqrt{26}$ u; c) $%s$ i $%s$." % (q1.tex(), q2.tex(), pv(pts[0]), pv(pts[1]))))

# ---------------- 64. Juliol 2014 ----------------
R, dr = V(0, 0, 10), V(1, 1, 0)
S, ds, tl = lineq(Pl((1, 1, 0), -8), Pl((1, 1, 1), -13), "s", M_)
m = det3(sub(S, R), dr, ds)
pl = pl_pn(S, cross(ds, dr))
ck(m != 0 and pl == Pl((0, 0, 1), -5))
tdl, dl2 = dll_x(R, dr, S, ds, "R", "S")
ck(dl2 == 25)
sol(64, steps(
    ap_("a)") + r"$r$: $x=y$, $z=10$: $R(0,0,10)$, $\vec d_r=(1,1,0)$. " + tl + r" Directors no proporcionals i $[\overrightarrow{RS},\vec d_r,\vec d_s]=%s\neq0$: <strong>s'encreuen</strong>." % detx(sub(S, R), dr, ds),
    ap_("b)") + r"Normal $\vec d_s\times\vec d_r=%s\parallel(0,0,1)$, per $S$: $\ z-5=0$." % crossx(ds, dr)[0],
    ap_("c)") + r"$r$ és paral·lela a aquest pla (està en el pla $z=10$), així que $d(r,s)=d(R,\ z=5)=|10-5|=5$ u. (Amb la fórmula: " + tdl + ")",
) + res(r"a) $(1,1,0)$ i $(1,-1,0)$; s'encreuen; b) $z=5$; c) $5$ u."))

# ---------------- 65. Juny 2015 ----------------
P0 = V(2, 0, 1)
R, dr = V(0, 0, 0), V(2, -1, 0)
pl = pl_pn(P0, dr)
t, Q = meet_lp(R, dr, pl)
ck(pl == Pl((2, -1, 0), -4) and Q == V(F(8, 5), F(-4, 5), 0) and d2_pp(P0, Q) == F(9, 5))
sol(65, steps(
    ap_("a)") + r"$r$: $x=-2y$, $z=0$: $(x,y,z)=\lambda(2,-1,0)$. Pla amb normal $(2,-1,0)$ per $P$: $\ 2x-y-4=0$.",
    ap_("b)") + r"$4\lambda+\lambda-4=0\Rightarrow\lambda=\frac45$: $Q\left(\tfrac85,-\tfrac45,0\right)$.",
    ap_("c)") + r"$Q$ és el peu de la perpendicular des de $P$: $d(P,r)=|\overrightarrow{QP}|=\left|\left(\tfrac25,\tfrac45,1\right)\right|=\sqrt{\tfrac{45}{25}}=\dfrac{3\sqrt5}{5}$ u. Per a qualsevol altre $X\in r$, el triangle $PQX$ és rectangle en $Q$, i $|PX|^2=|PQ|^2+|QX|^2\ge|PQ|^2$: $|PX|\ge\frac{3\sqrt5}{5}$.",
) + res(r"a) $2x-y-4=0$; b) $Q\left(\frac85,-\frac45,0\right)$; c) $\frac{3\sqrt5}{5}$ u."))

# ---------------- 66. Juny 2015 ----------------
R, dr, tl = lineq(Pl((1, -1, 0), 3), Pl((2, 0, -1), 2))
S, ds, tl2 = lineq(Pl((0, 3, 0), 1), Pl((1, 0, -2), -3), "s", M_)
pl = pl_pn(R, cross(dr, ds))
ck(pl == Pl((1, 3, -2), -5) and dot(dr, ds) != 0)
sol(66, steps(
    ap_("Recta $r$.") + tl,
    ap_("Recta $s$.") + tl2,
    ap_("a)") + r"Per $R$ amb normal $\vec d_r\times\vec d_s=%s$: $\ %s$." % (crossx(dr, ds)[0], pl.tex()),
    ap_("b)") + r"El director de $t$ és perpendicular als dos: $(1,3,-2)$. $\ t:(x,y,z)=\lambda(1,3,-2)$.",
    ap_("c)") + r"Un pla perpendicular a $s$ té normal $\vec d_s$; per contindre $r$ caldria $\vec d_r\perp\vec d_s$. Però $\vec d_r\cdot\vec d_s=%s\neq0$: <strong>no existeix</strong>." % nm(dot(dr, ds)),
) + res(r"a) $%s$; b) $(x,y,z)=\lambda(1,3,-2)$; c) no existeix." % pl.tex()))

# ---------------- 67. Juliol 2015 ----------------
R, dr = V(-1, 1, 0), V(3, -1, 2)
S, ds = V(1, 0, 0), V(1, -1, 0)
P0 = V(0, 3, -2)
pl = pl_pn(R, cross(dr, ds))
ck(pl == Pl((1, 1, -1), 0))
dd2 = d2_ppl(S, pl)
ck(dd2 == d2_ll(R, dr, S, ds))
sol(67, steps(
    ap_("a)") + r"$\vec d_r=(3,-1,2)$: $\ \dfrac{x}{3}=\dfrac{y-3}{-1}=\dfrac{z+2}{2}$.",
    ap_("b)") + r"Per $R(-1,1,0)$ amb normal $\vec d_r\times\vec d_s=%s\parallel(1,1,-1)$: $\ x+y-z=0$." % crossx(dr, ds)[0],
    ap_("c)") + r"El pla anterior conté $r$ i és paral·lel a $s$, així que $d(r,s)=d(S,\pi)$ amb $S(1,0,0)$: $\ \dfrac{|1|}{\sqrt3}=\dfrac{\sqrt3}{3}\approx0{,}58$ u.",
) + res(r"a) $\frac{x}{3}=\frac{y-3}{-1}=\frac{z+2}{2}$; b) $x+y-z=0$; c) $\frac{\sqrt3}{3}$ u."))

# ---------------- 68. Juliol 2015 ----------------
S, ds = V(1, 2, 3), V(-2, 1, -1)
X = pt_on(S, ds, 1)
r1, r2 = Pl((2, -1, 0), 5), Pl((6, 0, -1), 8)
ck(r1.has(X) and r2.has(X) and not par(cross(r1.n, r2.n), ds))
pp = pl_pn(S, cross(ds, V(0, 0, 1)))
ck(pp == Pl((1, 2, 0), -5) and pp.has(V(1, 2, 4)))
sol(68, steps(
    ap_("a)") + r"$\vec d_r=(2,-1,0)\times(6,0,-1)=%s$, no proporcional a $\vec d_s=(-2,1,-1)$. Substituïm $s$ en les equacions de $r$: $2(1-2\alpha)-(2+\alpha)+5=5-5\alpha=0$ i $6(1-2\alpha)-(3-\alpha)+8=11-11\alpha=0$: totes dues donen $\alpha=1$. Les rectes <strong>es tallen</strong> en el punt $(-1,3,2)$." % pv(cross(r1.n, r2.n)),
    ap_("b)") + r"$\vec n=(2,0,m)$: $\vec n\cdot\vec d_s=-4-m=0\Rightarrow m=-4$. Com que $(1,2,3)\in s$ dona $2-12+1=-9\neq0$, la recta no està continguda: és paral·lela.",
    ap_("c)") + r"$S(1,2,3)$, $\overrightarrow{SP}=(0,0,1)$: $\ \vec n=\vec d_s\times\overrightarrow{SP}=%s$: $\ x+2y-5=0$." % crossx(ds, V(0, 0, 1))[0],
) + res(r"a) Es tallen en $(-1,3,2)$; b) $m=-4$; c) $x+2y-5=0$."))

# ---------------- 69. Juny 2016 ----------------
p1, p2 = Pl((1, -2, 1), 3), Pl((3, 1, -1), 1)
R, dr, tl = lineq(p1, p2)
S, ds = V(1, 0, -2), V(0, 2, 1)
pl = pl_pn(R, cross(dr, ds))
ck(dot(pl.n, ds) == 0 and pl.has(pt_on(R, dr, 1)))
m = det3(sub(S, R), dr, ds)
dd2 = d2_ppl(S, pl)
ck(dd2 == d2_ll(R, dr, S, ds))
tdp, _ = dpl_x(S, pl, "S")
sol(69, steps(
    ap_("Recta $r$.") + tl,
    ap_("a)") + r"$(x,y,z)=(0,1,0)+\lambda%s$." % pv(dr),
    ap_("b)") + r"Normal $\vec d_r\times\vec d_s=%s$, per $R$: $\ \pi:%s$." % (crossx(dr, ds)[0], pl.tex()),
    ap_("c)") + r"$s$ és paral·lela a $\pi$ (i $r\subset\pi$), així que $d(r,s)=d(S,\pi)$ amb $S(1,0,-2)$: $\ %s$." % tdp,
) + res(r"a) $(x,y,z)=(0,1,0)+\lambda%s$; b) $%s$; c) $%s$ u." % (pv(dr), pl.tex(), sq(dd2))))

# ---------------- 70. Juny 2016 ----------------
A, B, C = V(1, 0, 0), V(0, 2, 0), V(0, 0, 3)
sg, ts = plane3x(A, B, C, "A", "B", "C", r"\sigma")
ck(sg == Pl((6, 3, 2), -6))
cx, c = crossx(sub(B, A), sub(C, A))
P0 = V(2, 0, 0)
vol = abs(det3(sub(B, A), sub(C, A), sub(P0, A))) / 6
ck(vol == 1 and n2(c) == 49)
sol(70, steps(
    ap_("a)") + ts + r" Té el mateix vector normal que $\pi$ però diferent terme independent ($-6\neq-12$): els plans són <strong>paral·lels</strong>.",
    ap_("b)") + r"$|\overrightarrow{AB}\times\overrightarrow{AC}|=|(6,3,2)|=7$: $\ S=\frac72$ u².",
    ap_("c)") + r"Per exemple $P(2,0,0)\in\pi$. $$V=\frac16|[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AP}]|=\frac16\left|%s\right|=1\ \text{u}^3$$ Com que $\pi\parallel\sigma$, l'altura és la mateixa per a qualsevol $P\in\pi$ i el volum sempre val 1." % detx(sub(B, A), sub(C, A), sub(P0, A)),
) + res(r"a) $6x+3y+2z-6=0$, paral·lel a $\pi$; b) $\frac72$ u²; c) amb $P(2,0,0)$, $V=1$ u³."))

# ---------------- 71. Juliol 2016 ----------------
A, B, C, D = V(0, 0, 1), V(1, 0, -1), V(0, 1, -2), V(1, 2, 0)
pl, tp = plane3x(A, B, C)
ck(pl == Pl((2, 3, 1), -1))
tdp, dd2 = dpl_x(D, pl, "D")
vol = abs(det3(sub(B, A), sub(C, A), sub(D, A))) / 6
ck(vol == F(7, 6))
sol(71, steps(
    ap_("a)") + tp,
    ap_("b)") + r"$D$: $2+6+0-1=7\neq0$, $D\notin\pi$: no són coplanaris (equivalentment, $[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}]\neq0$).",
    ap_("c)") + "$" + tdp + r"$. $$V=\frac16\left|%s\right|=\frac76\ \text{u}^3$$" % detx(sub(B, A), sub(C, A), sub(D, A)),
) + res(r"a) $2x+3y+z-1=0$; c) $d=\frac{\sqrt{14}}{2}$ u, $V=\frac76$ u³."))

# ---------------- 72. Juliol 2016 ----------------
ck(Pl((1, -2, 1), 0).has(V(1, 2, 3)) and dot(V(1, -2, 1), V(1, 1, 1)) == 0)
sgb = Pl((F(1, 2), -1, 1), 0)
ck(sgb.has(V(0, 1, 1)) and d2_ppl(V(1, 0, 1), sgb) == 1)
for a in (F(3), F(-1), F(1, 3)):
    b = (5 - 3 * a) / 2
    ps = Pl((a, b, 1), 0)
    ck(par(cross(V(1, 1, 1), ps.n), V(3, 2, -5)))
    X = V(1 / (1 - a), 0, -a / (1 - a))
    ck(Pl((1, 1, 1), -1).has(X) and ps.has(X))
sol(72, steps(
    ap_("a)") + r"Passa per $(1,2,3)$: $a+2b+3=0$. Perpendicular a $\pi$: $(a,b,1)\cdot(1,1,1)=a+b+1=0$. Restant: $b=-2$, $a=1$: $\ \sigma:x-2y+z=0$.",
    ap_("b)") + r"Passa per $(0,1,1)$: $b+1=0\Rightarrow b=-1$. $$d\big((1,0,1),\sigma\big)=\frac{|a+1|}{\sqrt{a^2+1+1}}=1\Rightarrow(a+1)^2=a^2+2\Rightarrow2a=1\Rightarrow a=\frac12$$",
    ap_("c)") + r"El director de $\pi\cap\sigma$ és perpendicular als dos normals. $(3,2,-5)\cdot(1,1,1)=0$ sempre, i $(3,2,-5)\cdot(a,b,1)=3a+2b-5=0$. A més, els plans no han de ser paral·lels: $(a,b)\neq(1,1)$. Hi ha infinites solucions: $$b=\frac{5-3a}{2},\quad a\neq1$$ Un punt de $r$: amb $y=0$, $x+z=1$ i $ax+z=0$ donen $x=\dfrac{1}{1-a}$, $z=\dfrac{-a}{1-a}$. Per exemple, per a $a=3$, $b=-2$: $\sigma:3x-2y+z=0$ i $r:(x,y,z)=\left(-\tfrac12,0,\tfrac32\right)+\lambda(3,2,-5)$.",
) + res(r"a) $a=1$, $b=-2$; b) $a=\frac12$, $b=-1$; c) tots els $(a,b)$ amb $3a+2b=5$, $a\neq1$; punt $\left(\frac{1}{1-a},0,\frac{-a}{1-a}\right)$."))

# ---------------- 73. Juny 2017 ----------------
P0 = V(1, 1, 1)
p1, p2 = Pl((1, 1, -1), 1), Pl((1, 2, -1), -1)
tp, pa_ = pencil_x(p1, p2, P0, r"\pi_1", r"\pi_2")
ck(pa_ == Pl((1, 3, -1), -3))
pi_ = Pl((1, 1, 1), -1)
tdp, dd2 = dpl_x(P0, pi_)
t, Hs = meet_lp(P0, pi_.n, pi_)
R, dr, tl = lineq(p1, p2)
sg = pl_pn(R, cross(dr, pi_.n))
ck(sg == Pl((1, 0, -1), 3) and dot(sg.n, pi_.n) == 0 and sg.has(pt_on(R, dr, 2)))
sol(73, steps(
    ap_("a)") + tp.replace("passe per $P$", "passe per $P(1,1,1)$"),
    ap_("b)") + r"$s$: director $(1,1,1)$: $\ (x,y,z)=(1,1,1)+\lambda(1,1,1)$. $\ %s$. Tall: $3(1+\lambda)=1\Rightarrow\lambda=-\frac23$: $\left(\tfrac13,\tfrac13,\tfrac13\right)$." % tdp,
    ap_("c)") + tl + r" $\sigma$ conté $r$ i la direcció $\vec n_\pi$: $\ \vec n_\sigma=\vec d\times\vec n_\pi=%s$, per $R$: $\ \sigma:%s$." % (crossx(dr, pi_.n)[0], sg.tex()),
) + res(r"a) $x+3y-z-3=0$; b) $s:(1+\lambda,1+\lambda,1+\lambda)$, $d=%s$ u, $\left(\frac13,\frac13,\frac13\right)$; c) $%s$." % (rq(dd2), sg.tex())))

# ---------------- 74. Juny 2017 ----------------
A, B, C = V(1, 1, 1), V(3, 0, 0), V(0, 3, 0)
pl, tp = plane3x(A, B, C)
ck(pl == Pl((1, 1, 1), -3))
t, H = meet_lp(O, pl.n, pl)
ck(H == A)
vol = abs(det3(A, B, C)) / 6
ck(vol == F(3, 2))
sol(74, steps(
    ap_("a)") + tp + r" Altura: $h_O:(x,y,z)=\lambda(1,1,1)$, és a dir, $x=y=z$.",
    ap_("b)") + r"$3\lambda=3\Rightarrow\lambda=1$: el peu de l'altura és $(1,1,1)$, que és precisament el vèrtex $A$ (l'aresta $OA$ és perpendicular a la cara $ABC$).",
    ap_("c)") + r"$S=\dfrac{|(3,3,3)|}{2}=\dfrac{3\sqrt3}{2}$ u². $\ V=\dfrac16\left|%s\right|=\dfrac32$ u³ (o $\frac13\cdot\frac{3\sqrt3}{2}\cdot|OA|=\frac13\cdot\frac{3\sqrt3}{2}\cdot\sqrt3=\frac32$)." % detx(A, B, C),
) + res(r"a) $x+y+z-3=0$, $h_O:x=y=z$; b) $(1,1,1)=A$; c) $\frac{3\sqrt3}{2}$ u², $\frac32$ u³."))

# ---------------- 75. Juliol 2017 ----------------
R, dr, tl = lineq(Pl((1, -2, -2), -1), Pl((1, 3, -1), -1))
ck(dr == V(8, -1, 5) and R == V(1, 0, 0))
sol(75, steps(
    ap_("Recta $r$.") + tl,
    ap_("Condició.") + r"$\vec n=(2,1,m)$: $\ \vec n\cdot\vec d=16-1+5m=15+5m$, que s'anul·la per a $m=-3$. A més, $R(1,0,0)\in\pi\iff2=n$.",
    ap_("a)") + r"Es tallen en un punt si $m\neq-3$ (i $n$ qualsevol).",
    ap_("b)") + r"No es tallen (paral·lels) si $m=-3$ i $n\neq2$.",
    ap_("c)") + r"La recta està continguda si $m=-3$ i $n=2$.",
) + res(r"a) $m\neq-3$; b) $m=-3$, $n\neq2$; c) $m=-3$, $n=2$."))

# ---------------- 76. Juliol 2017 ----------------
R = V(1, 0, 1)
t, X = meet_lp(R, V(4, 1, -1), Pl((2, -1, -1), 0))
ck(X == V(F(1, 2), F(-1, 8), F(9, 8)))
pb = Pl((2, -1, 4), 0)
ck(dot(pb.n, V(4, 4, -1)) == 0)
dd2 = d2_ppl(R, pb)
ck(dd2 == F(36, 21))
sol(76, steps(
    ap_("Recta.") + r"$r$: $R(1,0,1)$, $\vec d=(4,a,-1)$; $\ \vec n=(2,-1,b)$.",
    ap_("a)") + r"$a=1$, $b=-1$: $\pi:2x-y-z=0$. $(1+4\lambda,\lambda,1-\lambda)$: $2+8\lambda-\lambda-1+\lambda=0\Rightarrow\lambda=-\frac18$: $\left(\tfrac12,-\tfrac18,\tfrac98\right)$.",
    ap_("b)") + r"$a=b=4$: $\vec d\cdot\vec n=8-4-4=0$ i $R$: $2-0+4=6\neq0$: paral·lels. $d=\dfrac{6}{\sqrt{21}}=\dfrac{2\sqrt{21}}{7}\approx1{,}31$ u.",
    ap_("c)") + r"$\vec d\cdot\vec n=8-a-b$. Si $a+b\neq8$: es tallen en un punt. Si $a+b=8$: $R\in\pi\iff2+b=0\iff b=-2$ (i $a=10$): recta continguda. Si $a+b=8$ i $b\neq-2$: paral·lels.",
) + res(r"a) $\left(\frac12,-\frac18,\frac98\right)$; b) $\frac{2\sqrt{21}}{7}$ u; c) secants si $a+b\neq8$; continguda si $a=10$, $b=-2$; paral·lels si $a+b=8$, $b\neq-2$."))

# ---------------- 77. Juny 2018 ----------------
B, C = V(2, 3, 5), V(3, 5, 3)
A = V(-1, 2, F(5, 2))
ck(dot(sub(A, B), sub(C, B)) == 0)
A6 = V(-1, 2, 6)
cx, c = crossx(sub(B, A6), sub(C, A6))
pl = pl_pn(A6, c)
ck(pl == Pl((0, 1, 1), -8) and n2(c) == 50)
sol(77, steps(
    ap_("a)") + r"Si $AC$ és la hipotenusa, l'angle recte és en $B$: $\overrightarrow{BA}\cdot\overrightarrow{BC}=0$. $\overrightarrow{BA}=(-3,-1,\lambda-5)$, $\overrightarrow{BC}=(1,2,-2)$: $-3-2-2\lambda+10=0\Rightarrow\lambda=\frac52$.",
    ap_("b)") + r"$A(-1,2,6)$: $\overrightarrow{AB}=(3,1,-1)$, $\overrightarrow{AC}=(4,3,-3)$, $\ \overrightarrow{AB}\times\overrightarrow{AC}=%s$: $\ S=\dfrac{\sqrt{50}}{2}=\dfrac{5\sqrt2}{2}\approx3{,}54$ u²." % cx,
    ap_("c)") + r"Normal $(0,1,1)$ per $B$: $\ y+z-8=0$.",
) + res(r"a) $\lambda=\frac52$; b) $\frac{5\sqrt2}{2}$ u²; c) $y+z-8=0$."))

# ---------------- 78. Juny 2018 ----------------
A = V(5, 7, 3)
R, dr = V(3, -1, 0), V(-1, 3, 2)
t, X = proj_line(A, R, dr)
ck(X == V(1, 5, 4) and d2_pp(A, X) == 21)
pl = pl_pn(R, dr)
tdp, dd2 = dpl_x(V(1, 1, 1), pl, "B")
sol(78, steps(
    ap_("a)") + r"Busquem $X=(3-\lambda,-1+3\lambda,2\lambda)\in r$ amb $\overrightarrow{AX}\perp\vec d$: $\overrightarrow{AX}=(-2-\lambda,-8+3\lambda,-3+2\lambda)$, $\ \overrightarrow{AX}\cdot(-1,3,2)=14\lambda-28=0\Rightarrow\lambda=2$, $X(1,5,4)$. $\ s:(x,y,z)=(5,7,3)+\mu(-4,-2,1)$.",
    ap_("b)") + r"$d(A,r)=|\overrightarrow{AX}|=|(-4,-2,1)|=\sqrt{21}\approx4{,}58$ u.",
    ap_("c)") + r"$\pi$: normal $(-1,3,2)$ per $(3,-1,0)$: $-x+3y+2z+6=0$, és a dir, $%s$. $$%s$$" % (pl.tex(), tdp),
) + res(r"a) $s:(5,7,3)+\mu(-4,-2,1)$; b) $\sqrt{21}$ u; c) $%s$ u." % sq(dd2)))

# ---------------- 79. Juliol 2018 ----------------
A = V(1, 1, 1)
pi_ = Pl((1, -1, 1), -3)
pA = pl_pn(A, pi_.n)
t, X = meet_lp(V(0, 0, 0), V(2, 1, 0), pA)
ck(X == V(2, 1, 0) and dot(sub(X, A), pi_.n) == 0)
pb = pl_pn(A, cross(pi_.n, V(2, 1, 0)))
ck(pb == Pl((1, -2, -3), 4))
sol(79, steps(
    ap_("a)") + r"La recta és paral·lela a $\pi$ i passa per $A$, per tant està en el pla paral·lel a $\pi$ per $A$: $x-y+z-1=0$. Talla $s$, $(2\mu,\mu,0)$, on $2\mu-\mu-1=0$: $\mu=1$, $X(2,1,0)$. Recta $AX$: $\ (x,y,z)=(1,1,1)+\lambda(1,0,-1)$.",
    ap_("b)") + r"Conté les direccions $\vec n_\pi=(1,-1,1)$ i $\vec d_s=(2,1,0)$: $\ \vec n=%s$, per $A$: $\ %s$." % (crossx(pi_.n, V(2, 1, 0))[0], pb.tex()),
    ap_("c)") + r"La recta és $(5,3,1)+\mu(2,1,0)$. Amb $\mu=-1$ s'obté $(3,2,1)$: <strong>sí</strong> que hi està.",
) + res(r"a) $(1,1,1)+\lambda(1,0,-1)$; b) $%s$; c) sí ($\mu=-1$)." % pb.tex()))

# ---------------- 80. Juliol 2018 ----------------
R, dr, tl = lineq(Pl((1, 1, 0), -3), Pl((1, 4, -1), -8))
pl = pl_pn(V(5, 0, 1), cross(V(-1, 1, -1), dr))
ck(pl == Pl((1, 1, 0), -5) and dot(pl.n, dr) == 0)
dd2 = d2_ppl(R, pl)
ck(dd2 == 2)
sol(80, steps(
    ap_("a)") + tl,
    ap_("b)") + r"Vectors del pla: $(4,1,0)-(5,0,1)=(-1,1,-1)$ i $\vec d$: $\ \vec n=(-1,1,-1)\times\vec d=%s\parallel(1,1,0)$: $\ x+y-5=0$." % crossx(V(-1, 1, -1), dr)[0],
    ap_("c)") + r"$r$ és paral·lela a $\pi$: $d(r,\pi)=d(R,\pi)=\dfrac{|%s+%s-5|}{\sqrt2}=\sqrt2\approx1{,}41$ u." % (nm(R[0]), nm(R[1])),
) + res(r"a) $%s$; b) $x+y-5=0$; c) $\sqrt2$ u." % par_tex(R, dr)))
