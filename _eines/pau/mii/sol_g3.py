# Solucions 81-116 del recull de geometria. S'executa dins de sol_geo.py (després de sol_g1.py i sol_g2.py).
# ruff: noqa

# ---------------- 81. Juny 2019 ----------------
R, dr, tl = lineq(Pl((1, -1, 0), 3), Pl((2, 0, -1), 3))
S, ds = V(0, 0, 2), V(1, 1, 2)
ck(par(dr, ds) and not par(sub(S, R), dr))
pl = pl_pn(S, cross(ds, sub(R, S)))
ck(pl == Pl((5, 1, -3), 6) and pl.has(R))
P0 = V(0, -1, 2)
t, X = proj_line(P0, R, dr)
sol(81, steps(
    ap_("Rectes.") + tl + r" $s$: $S(0,0,2)$, $\vec d_s=(1,1,2)$. Els directors són iguals i $S\notin r$: les rectes són <strong>paral·leles</strong>.",
    ap_("a)") + r"El pla conté $\vec d=(1,1,2)$ i $\overrightarrow{SR}=%s$: $\ \vec n=\vec d\times\overrightarrow{SR}=%s$, per $S$: $\ %s$." % (pv(sub(R, S)), crossx(ds, sub(R, S))[0], pl.tex()),
    ap_("b)") + r"Busquem el peu $X$ de la perpendicular des de $P$: $X=%s$ amb $\overrightarrow{PX}\cdot\vec d=0$, que dona $\lambda=%s$ i $X%s$. La recta és $PX$: $\ (x,y,z)=(0,-1,2)+\mu%s$." % (gp(R, dr), nm(t), pv(X), pv(prim(sub(X, P0)))),
    ap_("c)") + r"$s\subset\pi$ si $\vec n\cdot\vec d_s=1-2+2a=0\Rightarrow a=\frac12$, i $S(0,0,2)\in\pi$: $2a=b\Rightarrow b=1$.",
) + res(r"a) $%s$; b) $(0,-1,2)+\mu%s$; c) $a=\frac12$, $b=1$." % (pl.tex(), pv(prim(sub(X, P0))))))

# ---------------- 82. Juny 2019 ----------------
A, B, C = V(20, 0, 0), V(0, 15, 0), V(0, 0, 9)
tg, c2, g = ang_x(sub(B, A), sub(C, A), "vv", r"\overrightarrow{AB}", r"\overrightarrow{AC}")
vol = abs(det3(A, B, C)) / 6
ck(vol == 450 and c2 == F(256, 481))
sol(82, steps(
    ap_("a)") + r"$|\vec n|=\sqrt{81+144+400}=25$. Plans $9x+12y+20z+D=0$ amb $\dfrac{|D+180|}{25}=4\Rightarrow D=-180\pm100$.",
    ap_("b)") + r"$A(20,0,0)$, $B(0,15,0)$, $C(0,0,9)$. $\overrightarrow{AB}=(-20,15,0)$, $\overrightarrow{AC}=(-20,0,9)$: $$%s\Rightarrow\alpha\approx%s$$" % (tg, gr(g)),
    ap_("c)") + r"$V=\dfrac16|[\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC}]|=\dfrac{20\cdot15\cdot9}{6}=450$ u³.",
) + res(r"a) $9x+12y+20z-80=0$ i $9x+12y+20z-280=0$; b) $\cos\alpha=\frac{16}{\sqrt{481}}$, $\alpha\approx%s$; c) $450$ u³." % gr(g)))

# ---------------- 83. Juliol 2019 ----------------
pl = Pl((2, 1, 2), -8)
P0 = V(10, 0, 10)
tdp, dd2 = dpl_x(P0, pl)
A, B, C = V(4, 0, 0), V(0, 8, 0), V(0, 0, 4)
cx, c = crossx(sub(B, A), sub(C, A))
vol = abs(det3(sub(B, A), sub(C, A), sub(P0, A))) / 6
ck(dd2 == F(1024, 9) and n2(c) == 2304 and vol == F(256, 3))
sol(83, steps(
    ap_("a)") + "$" + tdp + "$",
    ap_("b)") + r"$A(4,0,0)$, $B(0,8,0)$, $C(0,0,4)$: $\ \overrightarrow{AB}\times\overrightarrow{AC}=%s$, de mòdul $48$: $\ S=24$ u²." % cx,
    ap_("c)") + r"$V=\dfrac13\,S\,d(P,\pi)=\dfrac13\cdot24\cdot\dfrac{32}{3}=\dfrac{256}{3}$ u³ (també amb el producte mixt: $\frac16\left|%s\right|$)." % detx(sub(B, A), sub(C, A), sub(P0, A)),
) + res(r"a) $\frac{32}{3}$ u; b) $24$ u²; c) $\frac{256}{3}$ u³."))

# ---------------- 84. Juliol 2019 ----------------
ck(Pl((1, 2, 3), -6).has(V(6, 0, 0)) and dot(V(1, 2, 3), V(-1, -4, 3)) == 0)
sol(84, steps(
    ap_("a)") + r"$r$: $R(\alpha,0,0)$, $\vec d=(-1,-4,\beta)$; $\vec n=(1,2,3)$. $\ \vec d\cdot\vec n=-1-8+3\beta=3\beta-9$. Si $\beta\neq3$: la recta i el pla es tallen en un punt. Si $\beta=3$: $R\in\pi\iff\alpha=6$. Per tant: $\beta=3$, $\alpha=6$: recta continguda; $\beta=3$, $\alpha\neq6$: paral·lels.",
    ap_("b)") + r"Per a $\alpha=6$, $\beta=3$ la recta està continguda en el pla: $d(r,\pi)=0$.",
    ap_("c)") + r"No talla $\pi$ si és paral·lel: mateix normal i per l'origen: $\ x+2y+3z=0$.",
) + res(r"a) $\beta\neq3$: secants; $\beta=3,\alpha\neq6$: paral·lels; $\beta=3,\alpha=6$: continguda; b) $0$; c) $x+2y+3z=0$."))

# ---------------- 85. Juliol 2020 ----------------
R, dr = V(1, -1, 0), V(1, 1, -1)
P0 = V(1, 0, 0)
Q1 = V(2, 1, 1)
pl = pl_pn(P0, cross(sub(Q1, P0), dr))
ck(pl == Pl((1, -1, 0), -1) and pl.has(Q1))
pp = pl_pn(P0, dr)
tdp, dd2 = dpl_x(Q1, pp, "Q")
ck(dd2 == F(1, 3))
sol(85, steps(
    ap_("a)") + r"$\overrightarrow{PQ}=(1,1,\alpha)\parallel\vec d=(1,1,-1)\iff\alpha=-1$. (I $P\notin r$: $\frac{1-1}{1}=0\neq\frac{0+1}{1}$, així que són paral·leles i no coincidents.)",
    ap_("b)") + r"$\alpha=1$: $\overrightarrow{PQ}=(1,1,1)$; $\ \vec n=\overrightarrow{PQ}\times\vec d=%s\parallel(1,-1,0)$: $\ x-y-1=0$." % crossx(sub(Q1, P0), dr)[0],
    ap_("c)") + r"Pla per $P$ perpendicular a $r$: $\ %s$. $\ %s$." % (pp.tex(), tdp),
) + res(r"a) $\alpha=-1$; b) $x-y-1=0$; c) $\frac{\sqrt3}{3}$ u."))

# ---------------- 86. Juliol 2020 ----------------
pi_ = Pl((2, 1, -1), -5)
A, B = V(1, 2, -1), V(2, 1, 0)
pa_ = pl_pn(A, cross(sub(B, A), pi_.n))
ck(pa_ == Pl((0, 1, 1), -1) and pa_.has(B))
q1, q2 = Pl((1, -2, 0), 3), Pl((0, 1, 1), -1)
ck(q1.has(A) and q2.has(A) and par(cross(q1.n, q2.n), pi_.n))
td, dd2 = dpr_x(B, A, pi_.n, "B", "A")
sol(86, steps(
    ap_("a)") + r"Conté $\overrightarrow{AB}=(1,-1,1)$ i $\vec n_\pi=(2,1,-1)$: $\ \vec n=%s\parallel(0,1,1)$, per $A$: $\ y+z-1=0$." % crossx(sub(B, A), pi_.n)[0],
    ap_("b)") + r"$r:\ %s$. De $\dfrac{x-1}{2}=\dfrac{y-2}{1}=\dfrac{z+1}{-1}$: $\ x-2y+3=0$ i $y+z-1=0$, així que $r:\begin{cases}x-2y+3=0\\ y+z-1=0\end{cases}$." % par_tex(A, pi_.n),
    ap_("c)") + td,
) + res(r"a) $y+z-1=0$; b) $%s$, $r=\{x-2y+3=0\}\cap\{y+z-1=0\}$; c) $%s$ u." % (par_tex(A, pi_.n), sq(dd2))))

# ---------------- 87. Setembre 2020 ----------------
p1, p2 = Pl((1, 1, 0), -1), Pl((1, -1, 1), -1)
P0 = V(1, -1, 0)
d = prim(cross(p1.n, p2.n))
ck(d == V(1, -1, -2))
t1, d21 = dpl_x(P0, p1, "r", r"\pi")
t2, d22 = dpl_x(P0, p2, "r", r"\pi'")
S, ds, tl = lineq(p1, p2, "s")
t, X = proj_line(P0, S, ds)
ck(d21 == F(1, 2) and d22 == F(1, 3))
sol(87, steps(
    ap_("a)") + r"És paral·lela als dos plans: $\vec d=\vec n\times\vec n'=%s$. $\ r:\ %s$." % (crossx(p1.n, p2.n)[0], par_tex(P0, d)),
    ap_("b)") + r"Com que $r$ és paral·lela a cada pla, la distància és la de $P$: $\ %s$; $\ %s$." % (t1, t2),
    ap_("c) Recta $s=\\pi\\cap\\pi'$.") + tl + r" Peu de la perpendicular des de $P$: $X=%s$ amb $\overrightarrow{PX}\cdot\vec d=0$: $\lambda=%s$, $X%s$. Recta: $\ (x,y,z)=(1,-1,0)+\mu%s$." % (gp(S, ds), nm(t), pvt(X), pv(prim(sub(X, P0)))),
) + res(r"a) $%s$; b) $\frac{\sqrt2}{2}$ u i $\frac{\sqrt3}{3}$ u; c) $(1,-1,0)+\mu%s$." % (par_tex(P0, d), pv(prim(sub(X, P0))))))

# ---------------- 88. Setembre 2020 ----------------
R, dr = V(1, 2, 0), V(0, 1, 2)
S, ds = V(-1, 0, -2), V(-2, -1, 1)
m = det3(sub(S, R), dr, ds)
ck(m != 0)
tdl, dl2 = dll_x(R, dr, S, ds, "R", "S")
dt = prim(cross(V(2, -1, 0), V(0, 1, -1)))
tg, c2, g = ang_x(dr, dt, "rr", r"\vec d_r", r"\vec d_t")
ck(dt == V(1, 2, 2) and c2 == F(4, 5))
sol(88, steps(
    ap_("a)") + r"$\vec n=(3,a,-1)$, $\vec d_r=(0,1,2)$: $\vec n\cdot\vec d_r=a-2=0\Rightarrow a=2$. Però $R(1,2,0)$ dona $3+2a+1=8\neq0$: la recta és paral·lela al pla, no continguda. <strong>No hi ha cap valor</strong> de $a$.",
    ap_("b)") + r"$s$: $S(-1,0,-2)$, $\vec d_s=(-2,-1,1)$. " + tdl,
    ap_("c)") + r"$\vec d_t=(2,-1,0)\times(0,1,-1)=(1,2,2)$. $$%s$$" % tg,
) + res(r"a) Cap; b) $%s$ u; c) $\cos\alpha=\frac{2\sqrt5}{5}$." % sq(dl2)))

# ---------------- 89. Juny 2021 ----------------
sol(89, steps(
    ap_("a)") + r"$$|A|=\begin{vmatrix}1&1&1\\ 2&1&a\\ 1&a&1\end{vmatrix}=(1-a^2)-(2-a)+(2a-1)=-a^2+3a-2=-(a-1)(a-2)$$ Si $a\neq1,2$: $\operatorname{rg}A=\operatorname{rg}A^*=3$, els tres plans es tallen en <strong>un punt</strong>.",
    ap_("Cas $a=1$.") + r"$\pi_1:x+y+z=0$, $\pi_2:2x+y+z=1$, $\pi_3:x+y+z=1$. $\pi_1$ i $\pi_3$ tenen el mateix normal i diferent terme independent: són <strong>paral·lels</strong>, i $\pi_2$ els talla tots dos ($\operatorname{rg}A=2$, $\operatorname{rg}A^*=3$).",
    ap_("Cas $a=2$.") + r"$\pi_1:x+y+z=1$, $\pi_2:2x+y+2z=2$, $\pi_3:x+2y+z=1$. $E_3=3E_1-E_2$ (també en el terme independent): $\operatorname{rg}A=\operatorname{rg}A^*=2$ i cap parell és paral·lel: els tres plans es tallen en <strong>una recta</strong> (formen un feix).",
    ap_("b)") + r"Per a $a=1$, $\pi_1\parallel\pi_3$: no hi ha recta de tall.",
    ap_("c)") + r"Per a $a=2$: restant $\pi_2-\pi_1$: $x+z=1$, i aleshores $y=0$. Recta: $(x,y,z)=(1,0,0)+\lambda(1,0,-1)$ (que és la recta comuna als tres plans).",
) + res(r"a) $a\neq1,2$: un punt; $a=1$: $\pi_1\parallel\pi_3$ tallats per $\pi_2$; $a=2$: feix (es tallen en una recta); b) no existeix; c) $(1+\lambda,\,0,\,-\lambda)$."))
for a in (F(0), F(3), F(-1)):
    ck(-(a - 1) * (a - 2) == det3(V(1, 1, 1), V(2, 1, a), V(1, a, 1)))
ck(Pl((1, 1, 1), -1).has(V(2, 0, -1)) and Pl((2, 1, 2), -2).has(V(2, 0, -1)) and Pl((1, 2, 1), -1).has(V(2, 0, -1)))

# ---------------- 90. Juny 2021 ----------------
P0 = V(1, 2, 3)
pl = Pl((3, 2, 1), 4)
tdp, dd2 = dpl_x(P0, pl)
t, Mf = proj_pl(P0, pl)
Ps = sym(P0, Mf)
pp = pl_pn(Ps, pl.n)
ck(dd2 == 14 and Ps == V(-5, -2, 1) and pp == Pl((3, 2, 1), 18))
sol(90, steps(
    ap_("a)") + "$" + tdp + "$",
    ap_("b)") + r"Recta perpendicular per $P$: $(1+3\lambda,2+2\lambda,3+\lambda)$. En $\pi$: $14+14\lambda=0\Rightarrow\lambda=-1$, $M(-2,0,2)$. $\ P'=2M-P=(-5,-2,1)$.",
    ap_("c)") + r"$3x+2y+z+D=0$ per $P'$: $-15-4+1+D=0\Rightarrow D=18$: $\ 3x+2y+z+18=0$.",
) + res(r"a) $\sqrt{14}$ u; b) $P'(-5,-2,1)$; c) $3x+2y+z+18=0$."))

# ---------------- 91. Juliol 2021 ----------------
R, dr, tl = lineq(Pl((1, 1, 0), -1), Pl((2, 0, -1), -1))
S, ds = V(1, 0, 0), V(1, -1, 2)
ck(dr == V(1, -1, 2) and pos_ll(R, dr, S, ds) == "paral·leles")
ck(R[0] + 3 * R[1] + R[2] == 2)
ck(Pl((1, 3, 1), -2).has(R) and dot(V(1, 3, 1), dr) == 0)
A, B, C, P0 = V(2, 0, 0), V(0, 1, 0), V(0, 0, 2), V(2, 2, 2)
vol = abs(det3(sub(B, A), sub(C, A), sub(P0, A))) / 6
ck(vol == 2)
sol(91, steps(
    ap_("a)") + tl + r" $s$: $S(1,0,0)$, $\vec d_s=(1,-1,2)$, proporcional a $\vec d_r$. $S$ no és de $r$ ($2\cdot1-0-1=1\neq0$): les rectes són <strong>paral·leles</strong>.",
    ap_("b)") + r"$\vec n=(1,m,1)$: $\vec n\cdot\vec d_r=1-m+2=3-m=0\Rightarrow m=3$. A més, el punt $R%s$ de $r$ ha de ser del pla: $%s+%s\cdot m+%s=2$, que es compleix amb $m=3$. Per tant, $m=3$." % (pv(R), nm(R[0]), pr_(R[1]), pr_(R[2])),
    ap_("c)") + r"$m=2$: $x+2y+z=2$: $A(2,0,0)$, $B(0,1,0)$, $C(0,0,2)$. $$V=\frac16\left|%s\right|=2\ \text{u}^3$$" % detx(sub(B, A), sub(C, A), sub(P0, A)),
) + res(r"a) Paral·leles; b) $m=3$; c) $A(2,0,0)$, $B(0,1,0)$, $C(0,0,2)$, $V=2$ u³."))

# ---------------- 92. Juliol 2021 ----------------
P0, Q = V(1, 1, 0), V(2, -1, 1)
R1 = V(1, 3, -1)
pl, tp = plane3x(P0, Q, R1, "P", "Q", "R")
ck(pl == Pl((0, 1, 2), -1))
d = sub(Q, P0)
td, dd2 = dpr_x(R1, P0, d, "R", "P", "s")
sol(92, steps(
    ap_("a)") + tp + r" $d(O,\pi)=\dfrac{|-1|}{\sqrt5}=\dfrac{\sqrt5}{5}$ u.",
    ap_("b)") + r"$\vec d=\overrightarrow{PQ}=(1,-2,1)$: $\ r:\ %s$. Com que $r\parallel s$, $d(r,s)=d(R,s)$: " % par_tex(R1, d) + td,
    ap_("c)") + r"Alineats si $\overrightarrow{PR}=(\alpha-1,2,-1)\parallel(1,-2,1)$: $\alpha-1=-1\Rightarrow\alpha=0$. Recta: $(x,y,z)=(1,1,0)+\lambda(1,-2,1)$.",
) + res(r"a) $y+2z-1=0$, $\frac{\sqrt5}{5}$ u; b) $%s$, $d=%s$ u; c) $\alpha=0$, $(1,1,0)+\lambda(1,-2,1)$." % (par_tex(R1, d), sq(dd2))))

# ---------------- 93. Juny 2022 ----------------
R, dr = V(-1, 2, 0), V(1, -3, 1)
S, ds = V(4, -3, 0), V(-5, 4, 1)
m = det3(sub(S, R), dr, ds)
pos = pos_ll(R, dr, S, ds)
q1 = pl_pn(O, cross(dr, R))
q2 = pl_pn(O, cross(ds, S))
L_, dl, tl = lineq(q1, q2, "l")
ck(L_ == O or q1.has(O))
ck(not par(dl, dr) and not par(dl, ds))
sol(93, steps(
    ap_("Rectes.") + r"Amb $z=\lambda$: $r:(x,y,z)=(-1,2,0)+\lambda(1,-3,1)$, $\ s:(x,y,z)=(4,-3,0)+\mu(-5,4,1)$.",
    ap_("a)") + r"Directors no proporcionals. $$[\overrightarrow{RS},\vec d_r,\vec d_s]=%s$$" % detx(sub(S, R), dr, ds) + (r"Les rectes <strong>s'encreuen</strong>." if m != 0 else r"Les rectes <strong>es tallen</strong>."),
    ap_("b)") + r"La recta $l$ està en el pla que conté $O$ i $r$, i en el que conté $O$ i $s$. Pla $(O,r)$: $\vec n_1=\vec d_r\times\overrightarrow{OR}=%s$: $\ %s$. Pla $(O,s)$: $\vec n_2=\vec d_s\times\overrightarrow{OS}=%s$: $\ %s$. $$\vec d_l=\vec n_1\times\vec n_2=%s$$ $l:(x,y,z)=\lambda%s$ (no és paral·lela ni a $r$ ni a $s$, així que les talla totes dues)." % (crossx(dr, R)[0], q1.tex(), crossx(ds, S)[0], q2.tex(), crossx(q1.n, q2.n)[0], pv(dl)),
) + res(r"a) %s; b) $l:(x,y,z)=\lambda%s$." % ("S'encreuen" if m != 0 else "Es tallen", pv(dl))))

# ---------------- 94. Juny 2022 ----------------
p1 = Pl((2, -1, -1), 4)
n2v = cross(V(1, 1, 1), V(0, 1, -1))
p2 = pl_pn(V(-1, 1, 0), n2v)
ck(p2 == Pl((2, -1, -1), 3))
P0 = V(1, 0, 0)
t, Mf = proj_pl(P0, p1)
Ps = sym(P0, Mf)
ck(Ps == V(-3, 2, 2))
t, X = meet_lp(V(1, 0, 2), V(1, 2, -1), p1)
ck(X == V(-3, -8, 6))
sol(94, steps(
    ap_("a)") + r"$\vec n_2=(1,1,1)\times(0,1,-1)=%s$, i per $(-1,1,0)$: $\ \pi_2:2x-y-z+3=0$. Té el mateix normal que $\pi_1$ i diferent terme independent: <strong>paral·lels</strong>." % pv(n2v),
    ap_("b)") + r"$(1+2\lambda,-\lambda,-\lambda)$ en $\pi_1$: $6+6\lambda=0\Rightarrow\lambda=-1$, $M(-1,1,1)$. $\ P'=2M-P=(-3,2,2)$.",
    ap_("c)") + r"$(1+\lambda,2\lambda,2-\lambda)$: $2+2\lambda-2\lambda-2+\lambda+4=0\Rightarrow\lambda=-4$: $(-3,-8,6)$.",
) + res(r"a) Paral·lels; b) $P'(-3,2,2)$; c) $(-3,-8,6)$."))

# ---------------- 95. Juliol 2022 ----------------
A, B = V(2, 0, 0), V(0, 1, 0)
S, ds = V(1, 1, 0), V(2, 3, 1)
dr = sub(B, A)
pl = pl_pn(S, cross(ds, dr))
ck(pl == Pl((1, 2, -8), -3))
td, dd2 = dpr_x(A, S, ds, "A", "S", "s")
sol(95, steps(
    ap_("a)") + r"$\overrightarrow{AB}=(-2,1,0)$: $\ r:\ %s$." % par_tex(A, dr),
    ap_("b)") + r"$\vec n=\vec d_s\times\vec d_r=%s$, per $S(1,1,0)$: $\ %s$." % (crossx(ds, dr)[0], pl.tex()),
    ap_("c)") + td,
) + res(r"a) $%s$; b) $%s$; c) $%s$ u." % (par_tex(A, dr), pl.tex(), sq(dd2))))

# ---------------- 96. Juliol 2022 ----------------
A, B = V(2, 1, -2), V(3, 2, 3)
pl = Pl((2, 2, 1), -3)
t, C = proj_pl(B, pl)
ck(C == V(F(7, 9), F(-2, 9), F(17, 9)))
cx, c = crossx(sub(B, A), sub(C, A))
ar2 = n2(c) / 4
sol(96, steps(
    ap_("a)") + r"$(3+2\lambda,2+2\lambda,3+\lambda)$ en $\pi$: $13+9\lambda=3\Rightarrow\lambda=-\frac{10}{9}$: $C%s$." % pvt(C),
    ap_("b)") + r"$\overrightarrow{AB}=%s$, $\overrightarrow{AC}=%s$: $\ \overrightarrow{AB}\times\overrightarrow{AC}=%s$. $\ S=\dfrac12|\overrightarrow{AB}\times\overrightarrow{AC}|=%s$ u²." % (pv(sub(B, A)), pvt(sub(C, A)), pvt(c), sq(ar2)),
) + res(r"a) $C%s$; b) $%s$ u²." % (pvt(C), sq(ar2))))

# ---------------- 97. Juny 2023 ----------------
R, dr, tl = lineq(Pl((1, -1, 0), -1), Pl((1, 2, 1), 0))
ck(dr == V(1, 1, -3))
pl = pl_pn(V(0, 0, 3), dr)
ck(pl == Pl((1, 1, -3), 9))
sol(97, steps(
    ap_("Recta $r$.") + tl,
    ap_("a)") + r"$\overrightarrow{PQ}=(2,2,a-3)\parallel(1,1,-3)\iff a-3=-6\iff a=-3$. ($P$ no és de $r$: $0-0\neq1$, així que són paral·leles i no coincidents.)",
    ap_("b)") + r"Normal $(1,1,-3)$ per $P$: $x+y-3z+9=0$.",
) + res(r"a) $a=-3$; b) $x+y-3z+9=0$."))

# ---------------- 98. Juny 2023 ----------------
p1, p2 = Pl((5, 1, 7), -16), Pl((9, -1, 7), -12)
Q = V(2, 6, 0)
P0 = V(0, 5, 2)
ck(p1.has(Q) and p2.has(Q))
dr = prim(cross(p1.n, p2.n))
ds = sub(Q, P0)
tg, c2, g = ang_x(dr, ds, "rr", r"\vec d_r", r"\vec d_s")
t, X = proj_line(P0, Q, dr)
ck(X == V(1, 4, 1) and c2 == F(2, 3))
sol(98, steps(
    ap_("a)") + r"$Q$: $10+6=16$ ✓ i $18-6=12$ ✓. $\overrightarrow{PQ}=(2,1,-2)$: $\ s:\ %s$." % par_tex(P0, ds, M_),
    ap_("b)") + r"$\vec d_r=(5,1,7)\times(9,-1,7)=%s\parallel(1,2,-1)$. $$%s\Rightarrow\alpha\approx%s$$" % (pv(cross(p1.n, p2.n)), tg, gr(g)),
    ap_("c)") + r"$r:(2+\lambda,6+2\lambda,-\lambda)$. La projecció $X$ compleix $\overrightarrow{PX}\cdot\vec d_r=0$: $\overrightarrow{PX}=(2+\lambda,1+2\lambda,-2-\lambda)$, $\ (2+\lambda)+2(1+2\lambda)+(2+\lambda)=6+6\lambda=0\Rightarrow\lambda=-1$: $X(1,4,1)$.",
) + res(r"a) $%s$; b) $\cos\alpha=\frac{\sqrt6}{3}$, $\alpha\approx%s$; c) $(1,4,1)$." % (par_tex(P0, ds, M_), gr(g))))

# ---------------- 99. Juny 2024 ----------------
R, dr = V(1, -1, -2), V(2, 3, -1)
mm = F(5, 3)
pp = Pl((3, -mm, 1), 0)
pp = pl_pn(R, pp.n)
ck(pp == Pl((9, -5, 3), -8) and dot(pp.n, dr) == 0)
for m in (F(0), F(2), F(-1)):
    ck(d2_ppl(R, Pl((3, -m, 1), -1)) == m ** 2 / (10 + m ** 2))
sol(99, steps(
    ap_("a)") + r"$\vec n=(3,-m,1)$, $\vec d=(2,3,-1)$: $\vec n\cdot\vec d=6-3m-1=5-3m=0\Rightarrow m=\frac53$. $R(1,-1,-2)\in\pi\iff3+m-2=1\iff m=0$. Com que totes dues condicions no es compleixen alhora, per a $m=\frac53$ la recta és paral·lela i <strong>no hi ha cap valor</strong> de $m$ per al qual $\pi$ continga $r$.",
    ap_("b)") + r"Amb $m=\frac53$, els plans paral·lels a $\pi$ són $3x-\frac53y+z+D=0$, és a dir, $9x-5y+3z+D'=0$. Per $R$: $9+5-6+D'=0\Rightarrow D'=-8$: $\ 9x-5y+3z-8=0$.",
    ap_("c)") + r"$P$ és el punt $R$ de la recta: $$d(P,\pi)=\frac{|3+m-2-1|}{\sqrt{9+m^2+1}}=\frac{|m|}{\sqrt{m^2+10}}$$",
) + res(r"a) $m=\frac53$; cap valor; b) $9x-5y+3z-8=0$; c) $\dfrac{|m|}{\sqrt{m^2+10}}$."))

# ---------------- 100. Juny 2024 ----------------
P0, Q, R = V(2, 1, 3), V(1, 3, 1), V(4, 7, 6)
d = sub(Q, P0)
pl = pl_pn(P0, cross(d, sub(R, P0)))
ck(pl == Pl((18, -1, -10), -5) and pl.has(Q) and pl.has(R))
t1, Pq = proj_line(P0, R, d)
t2, Qq = proj_line(Q, R, d)
ck(Pq == V(F(40, 9), F(55, 9), F(62, 9)) and Qq == V(F(31, 9), F(73, 9), F(44, 9)))
ck(d2_pp(Pq, Qq) == n2(d) and dot(sub(Pq, P0), d) == 0)
sol(100, steps(
    ap_("a)") + r"El costat oposat a $PQ$ és paral·lel a $PQ$: $\vec d=\overrightarrow{PQ}=(-1,2,-2)$. $\ r:\ %s$." % par_tex(R, d),
    ap_("b)") + r"Conté $\overrightarrow{PQ}$ i $\overrightarrow{PR}=(2,6,3)$: $\ \vec n=%s$, per $P$: $\ %s$." % (crossx(d, sub(R, P0))[0], pl.tex()),
    ap_("c)") + r"Els altres vèrtexs són els peus de les perpendiculars des de $P$ i $Q$ a $r$. Per a $X=R+\lambda\vec d$: $\lambda=\dfrac{\overrightarrow{RP}\cdot\vec d}{|\vec d|^2}=\dfrac{-4}{9}$ i $\lambda=\dfrac{\overrightarrow{RQ}\cdot\vec d}{|\vec d|^2}=\dfrac59$. Vèrtexs: $P'%s$ (consecutiu a $P$) i $Q'%s$ (consecutiu a $Q$). Comprovació: $|P'Q'|=|PQ|=3$." % (pvt(Pq), pvt(Qq)),
) + res(r"a) $%s$; b) $%s$; c) $\left(\frac{40}{9},\frac{55}{9},\frac{62}{9}\right)$ i $\left(\frac{31}{9},\frac{73}{9},\frac{44}{9}\right)$." % (par_tex(R, d), pl.tex())))

# ---------------- 101. Juliol 2024 ----------------
R, dr = V(1, 2, 1), V(1, 1, 2)
S, ds = V(3, 3, -1), V(-2, -1, 2)
tt, uu, X = meet_ll(R, dr, S, ds)
dp = cross(dr, ds)
sol(101, steps(
    ap_("a)") + r"$r:%s$, $\ s:%s$. Igualant: $1+\lambda=3-2\mu$, $2+\lambda=3-\mu$: $\mu=%s$, $\lambda=%s$; tercera: $1+2\lambda=%s$ i $-1+2\mu=%s$ ✓. Es tallen en $P%s$." % (gp(R, dr), gp(S, ds, M_), nm(uu), nm(tt), nm(1 + 2 * tt), nm(-1 + 2 * uu), pv(X)),
    ap_("b)") + r"Director $\vec d_r\times\vec d_s=%s$: $\ (x,y,z)=%s+\lambda%s$." % (crossx(dr, ds)[0], pv(X), pv(dp)),
) + res(r"a) $P%s$; b) $(x,y,z)=%s+\lambda%s$." % (pv(X), pv(X), pv(dp))))

# ---------------- 102. Juliol 2024 ----------------
for dd in (F(12), F(-6), F(1)):
    A, B, C = V(dd / 6, 0, 0), V(0, dd / 4, 0), V(0, 0, -dd / 3)
    ck(Pl((6, 4, -3), -dd).has(A) and Pl((6, 4, -3), -dd).has(C))
    v2, g = ang(sub(B, A), sub(C, A), absval=False)
    ck(v2 == F(4, 65) and dot(sub(B, A), sub(C, A)) > 0)
sol(102, steps(
    ap_("a)") + r"$d(O,\pi)=\dfrac{|-d|}{\sqrt{36+16+9}}=\dfrac{|d|}{\sqrt{61}}=1\Rightarrow d=\pm\sqrt{61}$.",
    ap_("b)") + r"$A\left(\tfrac d6,0,0\right)$, $B\left(0,\tfrac d4,0\right)$, $C\left(0,0,-\tfrac d3\right)$.",
    ap_("c)") + r"$\overrightarrow{AB}=d\left(-\tfrac16,\tfrac14,0\right)$, $\overrightarrow{AC}=d\left(-\tfrac16,0,-\tfrac13\right)$. El factor $d$ no canvia l'angle (es simplifica, ja que $d^2>0$); multipliquem per 12: $(-2,3,0)$ i $(-2,0,-4)$: $$\cos\alpha=\frac{4}{\sqrt{13}\,\sqrt{20}}=\frac{2}{\sqrt{65}}\Rightarrow\alpha\approx%s$$" % gr(deg(2 / math.sqrt(65))),
) + res(r"a) $d=\pm\sqrt{61}$; b) $A\left(\frac d6,0,0\right)$, $B\left(0,\frac d4,0\right)$, $C\left(0,0,-\frac d3\right)$; c) $\cos\alpha=\frac{2}{\sqrt{65}}$, $\alpha\approx%s$ (no depèn de $d$)." % gr(deg(2 / math.sqrt(65)))))

# ---------------- 103. Juny 2025 ----------------
R, dr = V(1, 0, 2), V(2, 1, -1)
S, ds, tl = lineq(Pl((1, 0, 0), 1), Pl((1, 2, 1), 0), "s", M_)
tt, uu, X = meet_ll(R, dr, S, ds)
pl = pl_pn(X, cross(dr, ds))
ck(X == V(-1, -1, 3) and pl == Pl((1, -4, -2), 3) and pl.has(V(1, 0, 2)))
sol(103, steps(
    ap_("a)") + r"Substituïm $r$ en $s$: $1+2\lambda=-1\Rightarrow\lambda=-1$, punt $(-1,-1,3)$; i $x+2y+z=-1-2+3=0$ ✓. Es tallen en $(-1,-1,3)$.",
    ap_("b)") + r"$\vec d_s=(1,0,0)\times(1,2,1)=(0,-1,2)$. $\ \vec n=\vec d_r\times\vec d_s=%s$: $\ %s$." % (crossx(dr, V(0, -1, 2))[0], pl.tex()),
    ap_("c)") + r"$d(P,\pi)=\dfrac{|1-0-4+3|}{\sqrt{21}}=0$: $P(1,0,2)$ és del pla (és el punt de $r$ per a $\lambda=0$).",
) + res(r"a) $(-1,-1,3)$; b) $%s$; c) $0$ ($P$ és del pla)." % pl.tex()))

# ---------------- 104. Juny 2025 ----------------
pl = Pl((3, -1, 2), -4)
P0, Q = V(-1, 0, 1), V(2, 1, 2)
pp = pl_pn(P0, cross(sub(Q, P0), pl.n))
ck(pp == Pl((1, -1, -2), 3) and pp.has(Q))
tdq, dq2 = dpl_x(Q, pl, "Q")
t, Mf = proj_pl(P0, pl)
Ps = sym(P0, Mf)
ck(Ps == V(F(8, 7), F(-5, 7), F(17, 7)))
sol(104, steps(
    ap_("a)") + r"Conté $\overrightarrow{PQ}=(3,1,1)$ i $\vec n_\pi=(3,-1,2)$: $\ \vec n=%s\parallel(1,-1,-2)$, per $P$: $\ %s$." % (crossx(sub(Q, P0), pl.n)[0], pp.tex()),
    ap_("b)") + "$" + tdq + "$",
    ap_("c)") + r"$(-1+3\lambda,-\lambda,1+2\lambda)$ en $\pi$: $-5+14\lambda=0\Rightarrow\lambda=\frac5{14}$, $M%s$. $\ P'=2M-P=%s$." % (pvt(Mf), pvt(Ps)),
) + res(r"a) $%s$; b) $%s$ u; c) $P'\left(\frac87,-\frac57,\frac{17}{7}\right)$." % (pp.tex(), sq(dq2))))

# ---------------- 105. Juny 2025 ----------------
R, dr, tl = lineq(Pl((2, 4, -1), 0), Pl((-1, 1, 5), -3))
p4 = Pl((2, 4, -1), 3)
ck(dot(p4.n, dr) == 0 and not p4.has(R))
p3 = Pl((2, 3, -1), 3)
Pp = V(F(9, 2), 5, -1)
t, Mf = proj_pl(Pp, p3)
Ps = sym(Pp, Mf)
ck(Ps == V(F(-7, 2), -7, 3))
for a in (F(0), F(2), F(-3)):
    ck(d2_ppl(V(3, 1, -2), Pl((2, a, -1), 3)) == (a + 11) ** 2 / (a * a + 5))
sol(105, steps(
    ap_("a)") + r"$$d=\frac{|6+a+2+3|}{\sqrt{4+a^2+1}}=\frac{|a+11|}{\sqrt{a^2+5}}$$",
    ap_("b)") + tl + r" Per a $a=4$, $\vec n=(2,4,-1)$ i $\vec n\cdot\vec d=%s=0$: $\sin\alpha=0$, l'angle és $0^\circ$. (La recta és paral·lela al pla: $R%s$ dona $%s\neq0$.)" % (nm(dot(p4.n, dr)), pv(R), nm(p4.ev(R))),
    ap_("c)") + r"$a=3$: $\pi:2x+3y-z+3=0$. $\left(\tfrac92+2\lambda,5+3\lambda,-1-\lambda\right)$ en $\pi$: $28+14\lambda=0\Rightarrow\lambda=-2$, $M\left(\tfrac12,-1,1\right)$. $\ P'=2M-P=\left(-\tfrac72,-7,3\right)$.",
) + res(r"a) $\frac{|a+11|}{\sqrt{a^2+5}}$; b) $0^\circ$ (paral·lels); c) $\left(-\frac72,-7,3\right)$."))

# ---------------- 106. Juny 2025 ----------------
ds = prim(cross(V(-1, 1, 1), V(1, 2, -1)))
ck(ds == V(1, 0, 1) and dot(V(2, 3, -2), ds) == 0)
sol(106, steps(
    ap_("a)") + r"$\vec d_s=(-1,1,1)\times(1,2,-1)=%s\parallel(1,0,1)$; $\vec d_r=(2,3,\alpha)$. Perpendiculars: $\vec d_r\cdot\vec d_s=2+\alpha=0\Rightarrow\alpha=-2$." % pv(cross(V(-1, 1, 1), V(1, 2, -1))),
    ap_("b)") + r"El punt de $r$ amb $z=0$ és $(-1,2,0)$ (paràmetre 0). Recta: $(x,y,z)=(-1,2,0)+\lambda(1,0,1)$.",
) + res(r"a) $\alpha=-2$; b) $(-1+\lambda,\,2,\,\lambda)$."))

# ---------------- 107. Juliol 2025 ----------------
ck(F(dot(V(1, 2, 2), V(1, 0, 1))) ** 2 / (n2(V(1, 2, 2)) * 2) == F(1, 2))
for m in (F(0), F(3), F(-2)):
    X = V(6 - 1, F(-7, 2) + (1 - m) / 2, 1)
    ck(Pl((1, 2, m), 1).has(X) and Pl((1, 0, 1), -6).has(X))
sol(107, steps(
    ap_("a)") + r"$(1,2,m)\cdot(1,0,1)=1+m=0\Rightarrow m=-1$.",
    ap_("b)") + r"$$\frac{|1+m|}{\sqrt{5+m^2}\,\sqrt2}=\frac{\sqrt2}{2}\Rightarrow|1+m|=\sqrt{5+m^2}\Rightarrow1+2m=5\Rightarrow m=2$$",
    ap_("c)") + r"Els normals no són mai proporcionals, així que es tallen sempre. Amb $z=\lambda$: $x=6-\lambda$ i $2y=-1-x-m\lambda=-7+(1-m)\lambda$: $$x=6-\lambda,\quad y=-\frac72+\frac{1-m}{2}\lambda,\quad z=\lambda$$",
) + res(r"a) $m=-1$; b) $m=2$; c) $\left(6-\lambda,\ -\frac72+\frac{1-m}2\lambda,\ \lambda\right)$."))

# ---------------- 108. Juliol 2025 ----------------
pl = Pl((3, 1, -1), -2)
ck(pl.has(V(0, 1, -1)) and pl.has(V(1, 0, 1)))
Q = V(1, 1, 1)
t, Mf = proj_pl(Q, pl)
Qs = sym(Q, Mf)
ck(Qs == V(F(5, 11), F(9, 11), F(13, 11)))
sol(108, steps(
    ap_("a)") + r"$P$ és de $\pi$ ($0+1+1=2$ ✓), així que la recta $PQ$ hi està continguda si i només si $Q\in\pi$: $3+a-1=2\Rightarrow a=0$.",
    ap_("b)") + r"$Q(1,1,1)$: $(1+3\lambda,1+\lambda,1-\lambda)$ en $\pi$: $1+11\lambda=0\Rightarrow\lambda=-\frac1{11}$, $M%s$. $\ Q'=2M-Q=%s$." % (pvt(Mf), pvt(Qs)),
) + res(r"a) $a=0$; b) $\left(\frac5{11},\frac9{11},\frac{13}{11}\right)$."))

# ---------------- 109. Juliol 2025 ----------------
pl = Pl((2, 0, -1), -1)
dr = V(1, 2, 2)
pp = pl_pn(O, cross(dr, pl.n))
ck(pp == Pl((2, -5, 4), 0))
sol(109, steps(
    ap_("a)") + r"$r$: $y=2x$, $z=y$: $(x,y,z)=\lambda(1,2,2)$. Com que $\vec d_r$ no és paral·lel a $\vec n_\pi=(2,0,-1)$, el pla existeix i és únic: conté $\vec d_r$ i $\vec n_\pi$: $\ \vec n=%s$, per l'origen: $\ %s$." % (crossx(dr, pl.n)[0], pp.tex()),
    ap_("b)") + r"$2x-z+D=0$ amb $\dfrac{|0-2+D|}{\sqrt5}=2\Rightarrow D=2\pm2\sqrt5$.",
) + res(r"a) $2x-5y+4z=0$; b) $2x-z+2+2\sqrt5=0$ i $2x-z+2-2\sqrt5=0$."))

# ---------------- 110 i 116. Juliol 2025 / Juliol 2026 ----------------
A, B, C, D = V(0, 0, 0), V(10, 0, -20), V(0, 15, -30), V(1, 2, -1)
pi_ = Pl((2, 3, -1), 0)
ck(pi_.ev(B) == 40 and pi_.ev(C) == 75)
pabc, tabc = plane3x(A, B, C)
ck(pabc == Pl((2, 2, 1), 0))
t, Hd = proj_pl(D, pabc)
ck(Hd == V(F(-1, 9), F(8, 9), F(-14, 9)))
tdd, dd2 = dpl_x(D, pi_, "D")
ck(dd2 == F(81, 14))
s_a = ap_("Triangle i pla $\\pi$.") + r"$A$ és de $\pi$, però $B$: $20+0+20=40\neq0$ i $C$: $0+45+30=75\neq0$. El triangle <strong>no</strong> està en el pla $\pi$."
s_p = ap_("Projecció de $D$ sobre el pla $ABC$.") + tabc + r" Recta per $D$ perpendicular: $(1+2\lambda,2+2\lambda,-1+\lambda)$; en el pla: $5+9\lambda=0\Rightarrow\lambda=-\frac59$: $\left(-\tfrac19,\tfrac89,-\tfrac{14}{9}\right)$."
s_d = ap_("Distància de $D$ a $\\pi$.") + "$" + tdd + "$"
R_ = r"$ABC$ no és de $\pi$; projecció $\left(-\frac19,\frac89,-\frac{14}9\right)$; $d(D,\pi)=\frac{9\sqrt{14}}{14}$ u."
sol(110, steps(r"<em>Nota: a l'enunciat del recull apareix $D(1,2,,1)$; és $D(1,2,-1)$, com a l'exercici de juliol de 2026, que és el mateix.</em>", s_a, s_d, s_p) + res(R_))
sol(116, steps(s_a, s_p, s_d) + res(R_))

# ---------------- 111. Juny 2026 ----------------
R, dr = V(0, -1, 1), V(2, -1, 1)
for m in (F(0), F(1), F(-3), F(7)):
    t, X = meet_lp(R, dr, Pl((2, m, 1), -3))
    ck(X == V((2 * m + 4) / (5 - m), -7 / (5 - m), 7 / (5 - m)))
ck(not Pl((2, 5, 1), -3).has(R))
sol(111, steps(
    ap_("a)") + r"$\vec n=(2,m,1)\parallel\vec d=(2,-1,1)\iff m=-1$.",
    ap_("b)") + r"$\vec n\cdot\vec d=4-m+1=5-m=0\Rightarrow m=5$; i $R(0,-1,1)$: $0-5+1-3=-7\neq0$, no és del pla: paral·lels.",
    ap_("c)") + r"Per a $m\neq5$: $(2\lambda,-1-\lambda,1+\lambda)$ en $\pi$: $4\lambda-m-m\lambda+1+\lambda-3=0\Rightarrow(5-m)\lambda=m+2\Rightarrow\lambda=\dfrac{m+2}{5-m}$. $$P=\left(\frac{2m+4}{5-m},\ \frac{-7}{5-m},\ \frac{7}{5-m}\right)$$",
) + res(r"a) $m=-1$; b) $m=5$; c) per a $m\neq5$, $\left(\frac{2m+4}{5-m},\frac{-7}{5-m},\frac{7}{5-m}\right)$."))

# ---------------- 112. Juny 2026 ----------------
ck(3 + 2 * F(13, 2) == 16)
sol(112, steps(
    ap_("Recta.") + r"El denominador 0 vol dir que $x$ no varia: $s:(x,y,z)=(1,1,1)+\lambda(0,1,-1)$.",
    ap_("a)") + r"Normal $(0,1,-1)$ per $(1,1,1)$: $\ y-z=0$.",
    ap_("b)") + r"$X=(1,1+\lambda,1-\lambda)$: $|OX|^2=1+(1+\lambda)^2+(1-\lambda)^2=3+2\lambda^2=16\Rightarrow\lambda=\pm\sqrt{\tfrac{13}{2}}=\pm\dfrac{\sqrt{26}}{2}$. Punts: $\left(1,\,1+\tfrac{\sqrt{26}}2,\,1-\tfrac{\sqrt{26}}2\right)$ i $\left(1,\,1-\tfrac{\sqrt{26}}2,\,1+\tfrac{\sqrt{26}}2\right)$.",
    ap_("c)") + r"$\cos\alpha=\dfrac{|(0,1,-1)\cdot(0,0,1)|}{\sqrt2\cdot1}=\dfrac{\sqrt2}{2}\Rightarrow\alpha=45^\circ$.",
) + res(r"a) $y-z=0$; b) $\left(1,1\pm\frac{\sqrt{26}}2,1\mp\frac{\sqrt{26}}2\right)$; c) $45^\circ$."))

# ---------------- 113. Juny 2026 extra ----------------
a = F(2, 3)
X = V(a - 1, 2 - a, 1)
ck(Pl((2, 1, 0), -a).has(X) and Pl((-1, 2, 2), -5).has(X) and Pl((1, 0, 1), -a).has(X))
ck(n2(X) == F(26, 9))
for aa in (F(0), F(1), F(2, 3), F(-4)):
    Rr, Ss = V(0, aa, 1), V(aa, (5 + aa) / 2, 0)
    ck(Pl((-1, 2, 2), -5).has(Ss) and Pl((1, 0, 1), -aa).has(Ss))
    ck((det3(sub(Ss, Rr), V(1, -2, 0), V(2, 3, -2)) == 0) == (aa == F(2, 3)))
sol(113, steps(
    ap_("Directors.") + r"$\vec d_r=(2,1,0)\times(0,0,1)=(1,-2,0)$, $\ \vec d_s=(-1,2,2)\times(1,0,1)=(2,3,-2)$: no són proporcionals, així que les rectes es tallen o s'encreuen.",
    ap_("a) i b)") + r"Es tallen si el sistema de les quatre equacions és compatible. De $z=1$ i $x+z=a$: $x=a-1$; de $2x+y=a$: $y=2-a$. En la tercera: $-(a-1)+2(2-a)+2=5\Rightarrow7-3a=5\Rightarrow a=\frac23$. Per tant: si $a=\frac23$ <strong>es tallen</strong>, i si $a\neq\frac23$ <strong>s'encreuen</strong>.",
    ap_("Punt de tall.") + r"$a=\frac23$: $P\left(-\tfrac13,\tfrac43,1\right)$.",
    ap_("c)") + r"$|OP|=\sqrt{\tfrac19+\tfrac{16}9+1}=\sqrt{\tfrac{26}{9}}=\dfrac{\sqrt{26}}{3}\approx1{,}70$ u.",
) + res(r"a) Es tallen si $a=\frac23$; s'encreuen si $a\neq\frac23$; b) $P\left(-\frac13,\frac43,1\right)$; c) $\frac{\sqrt{26}}{3}$ u."))

# ---------------- 114. Juny 2026 extra ----------------
pl = Pl((2, 1, 0), -3)
R, dr = V(1, -1, 1), V(1, -2, 0)
ck(dot(pl.n, dr) == 0 and not pl.has(R))
p1_ = pl_pn(R, cross(dr, pl.n))
p2_ = pl_pn(R, pl.n)
ck(p1_ == Pl((0, 0, 1), -1) and p2_ == Pl((2, 1, 0), -1))
sol(114, steps(
    ap_("a)") + r"$\vec n_1=\vec d_r\times\vec n_\pi=%s\parallel(0,0,1)$, per $R(1,-1,1)$: $\ \pi_1:z-1=0$." % crossx(dr, pl.n)[0],
    ap_("b)") + r"$\vec d_r\cdot\vec n_\pi=2-2=0$: $r$ és paral·lela a $\pi$ ($R$ no hi és: $2-1-3\neq0$), així que el pla existeix: $2x+y+D=0$ per $R$: $2-1+D=0$: $\ \pi_2:2x+y-1=0$.",
) + res(r"a) $z-1=0$; b) $2x+y-1=0$."))

# ---------------- 115. Juliol 2026 ----------------
A, B, v = V(0, -1, 0), V(1, 0, 1), V(2, -1, 1)
pl = pl_pn(A, v)
t, C = proj_pl(B, pl)
tdb, db2 = dpl_x(B, pl, "B")
ck(pl == Pl((2, -1, 1), -1) and C == V(F(1, 3), F(1, 3), F(2, 3)) and db2 == F(2, 3))
sol(115, steps(
    ap_("a)") + r"$2x-y+z+D=0$ per $A$: $1+D=0$: $\ \pi:2x-y+z-1=0$.",
    ap_("b)") + r"$(x,y,z)=(1,0,1)+\lambda(2,-1,1)$.",
    ap_("c)") + r"El punt més pròxim és el peu de la perpendicular: $2(1+2\lambda)+\lambda+(1+\lambda)-1=0\Rightarrow6\lambda+2=0\Rightarrow\lambda=-\frac13$: $C\left(\tfrac13,\tfrac13,\tfrac23\right)$.",
    ap_("d)") + "$" + tdb + r"$ (és $|\overrightarrow{BC}|$).",
) + res(r"a) $2x-y+z-1=0$; b) $(1+2\lambda,-\lambda,1+\lambda)$; c) $C\left(\frac13,\frac13,\frac23\right)$; d) $\frac{\sqrt6}{3}$ u."))
