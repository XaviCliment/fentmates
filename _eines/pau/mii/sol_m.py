# Solucions dels exercicis de matrius i determinants (M). S'executa dins de sol_mii.py.
# ruff: noqa

# ---------------- Juny 1999 (1) ----------------
A = M([2, 0, 1], [1, 3, 0], [5, 1, 3]); B = M([1, 1], [2, 1], [0, 3])
ih, Ai = inv_html(A); X = mul(Ai, B); assert mul(A, X) == B
sol("M", "Juny 1999", 1, steps(
    r"<strong>Apartat a).</strong> $A$ és quadrada; si és invertible, $AX=B\Rightarrow X=A^{-1}B$ (de dimensió $3\times2$)." + ih,
    r"$$X=A^{-1}B=%s%s=%s$$ Comprovació: $AX=%s=B$ ✓." % (nice(Ai), tx(B), nice(X), tx(mul(A, X))),
    r"<strong>Apartat b).</strong> Ara $A$ és $3\times2$ i $B$ és $3\times3$, així que $X$ hauria de ser $2\times3$. $A$ no és quadrada i no té inversa: plantegem el sistema per columnes. Per a la primera columna $\begin{pmatrix}a\\b\end{pmatrix}$ de $X$: $$\begin{pmatrix}1&1\\2&1\\0&3\end{pmatrix}\begin{pmatrix}a\\b\end{pmatrix}=\begin{pmatrix}2\\1\\5\end{pmatrix}\iff%s$$ De les dues primeres, $a=-1$, $b=3$; però llavors $3b=9\neq5$. El sistema és incompatible, així que <strong>no existeix</strong> cap matriu $X$." % sysm("a+b&=2", "2a+b&=1", "3b&=5"),
) + res(r"a) $X=%s$. &nbsp; b) No existeix." % nice(X)))

# ---------------- Juny 2000 (1) ----------------
A = M([0, 1, 2], [0, 0, 3], [0, 0, 0]); A2 = mul(A, A); A3 = mul(A2, A)
assert A3 == sc(0, I(3))
sol("M", "Juny 2000", 1, steps(
    r"<strong>Potències.</strong> $$A^2=%s%s=%s$$ $$A^3=A^2\cdot A=%s%s=%s$$" % (tx(A), tx(A), tx(A2), tx(A2), tx(A), tx(A3)),
    r"<strong>A partir d'ací.</strong> $A^4=A^3A=O\cdot A=O$ i $A^5=A^4A=O$, on $O$ és la matriu nul·la.",
    r"<strong>Cas general.</strong> Per a $n>5$, $A^n=A^3\cdot A^{n-3}=O\cdot A^{n-3}=O$. (Diem que $A$ és <em>nilpotent</em>.)",
) + res(r"$A^2=%s$, $A^3=A^4=A^5=O$ i $A^n=O$ per a tot $n\geq3$." % tx(A2)))

# ---------------- Juny 2001 (1) ----------------
A = M([1, 0, 0], [4, 2, 0], [6, 5, 3]); Bv = M([3], [7], [2]); Cv = M([4], [8], [9])
R = sub(Cv, Bv); X = mul(inv(A), R); assert add(mul(A, X), Bv) == Cv
sol("M", "Juny 2001", 1, steps(
    r"<strong>Aïllem.</strong> $$AX+B=C\Rightarrow AX=C-B=%s$$" % tx(R),
    r"<strong>Resolem.</strong> Com que $A$ és triangular ($|A|=1\cdot2\cdot3=6\neq0$), el sistema $AX=C-B$ es resol de dalt cap avall: $$%s\Rightarrow x=1,\quad y=\frac{1-4}{2}=-\frac32,\quad z=\frac{7-6+\frac{15}{2}}{3}=\frac{17}{6}$$" % sysm("x&=1", "4x+2y&=1", "6x+5y+3z&=7"),
    r"<strong>Comprovació.</strong> $AX+B=%s+%s=%s=C$ ✓." % (tx(mul(A, X)), tx(Bv), tx(Cv)),
) + res(r"$X=%s$" % tx(X)))
assert X == M([1], [Fr(-3, 2)], [Fr(17, 6)])

# ---------------- Juny 2002 (1) ----------------
A1 = M([1, 1, 1], [1, 1, -1], [3, 5, 5]); B1 = M([2, 1, 1], [1, 1, -1], [2, 1, -1])
assert det(A1) == 4 and det(B1) == -2 and det(mul(A1, B1)) == -8
sol("M", "Juny 2002", 1, steps(
    r"<strong>Apartat a).</strong> Desenvolupem per la fila (o columna) on hi ha les incògnites: $$|A|=x\begin{vmatrix}1&-1\\5&5\end{vmatrix}-y\begin{vmatrix}1&-1\\3&5\end{vmatrix}+z\begin{vmatrix}1&1\\3&5\end{vmatrix}=10x-8y+2z$$ $$|B|=-x\begin{vmatrix}1&-1\\2&-1\end{vmatrix}+y\begin{vmatrix}2&1\\2&-1\end{vmatrix}-z\begin{vmatrix}2&1\\1&-1\end{vmatrix}=-x-4y+3z$$ (per a $|B|$ hem desenvolupat per la segona columna).",
    r"<strong>Apartat b).</strong> Per a $x=y=z=1$: $|A|=10-8+2=4$ i $|B|=-1-4+3=-2$. Pel determinant d'un producte, $|A\cdot B|=|A|\cdot|B|=-8$.",
    r"<strong>Apartat c).</strong> Cap de les dues té inversa si $|A|=0$ i $|B|=0$: $$%s$$ De la primera, $z=4y-5x$; substituint en la segona: $-x-4y+12y-15x=0\Rightarrow y=2x$, i llavors $z=3x$. Per tant $(x,y,z)=(t,2t,3t)$, $t\in\mathbb{R}$." % sysm("5x-4y+z&=0", "-x-4y+3z&=0"),
) + res(r"a) $|A|=10x-8y+2z$, $|B|=-x-4y+3z$. &nbsp; b) $|AB|=-8$. &nbsp; c) $(x,y,z)=(t,2t,3t)$, $t\in\mathbb{R}$."))

# ---------------- Juny 2002 (2) ----------------
M0 = M([4, 3, 0], [2, 1, 2], [0, 0, -1]); ih, Mi = inv_html(M0, "M(0)")
Mf = lambda t: M([4, 3, t], [2, 1, 2], [t, t, -1])
assert [det(Mf(t)) for t in (8, 4, 3)] == [50, 10, 5]
sol("M", "Juny 2002", 2, steps(
    r"<strong>Apartat a).</strong> $$|M(\lambda)|=4(-1-2\lambda)-3(-2-2\lambda)+\lambda(2\lambda-\lambda)=\lambda^2-2\lambda+2=(\lambda-1)^2+1$$ Com que $(\lambda-1)^2\geq0$, $|M(\lambda)|\geq1>0$ per a tot $\lambda$: $M(\lambda)$ sempre té inversa.",
    r"<strong>Apartat b).</strong>" + ih,
    r"<strong>Apartat c).</strong> $|A|=|M(8)|=64-16+2=50$, $|B|=|M(4)|=16-8+2=10$, $|C|=|M(3)|=9-6+2=5$. Com que $|P^{-1}|=\frac1{|P|}$ i el determinant del producte és el producte de determinants: $$|A\,B^{-1}\,C^{-1}|=\frac{|A|}{|B|\,|C|}=\frac{50}{10\cdot5}=1$$",
) + res(r"a) $|M(\lambda)|=\lambda^2-2\lambda+2>0$. &nbsp; b) $M(0)^{-1}=%s$. &nbsp; c) $1$." % nice(Mi)))

# ---------------- Setembre 2002 (1) ----------------
A = M([5, 8], [9, 4]); B = M([1, 1, -1], [2, -3, 2]); C = M([2, -1], [-3, 2], [1, 4]); D = M([3, 7], [1, 2])
BC = mul(B, C); Mm = sub(A, sc(2, BC)); ih, Di = inv_html(D, "D")
X = mul(Di, Mm); Y = mul(Mm, Di); assert mul(D, X) == Mm and mul(Y, D) == Mm
sol("M", "Setembre 2002", 1, steps(
    r"<strong>Apartat a).</strong> $$BC=%s%s=%s;\qquad M=A-2BC=%s-%s=%s$$" % (tx(B), tx(C), tx(BC), tx(A), tx(sc(2, BC)), tx(Mm)),
    r"<strong>Apartat b).</strong>" + ih,
    r"<strong>Apartat c).</strong> $DX=M\Rightarrow X=D^{-1}M$ (per l'esquerra) i $YD=M\Rightarrow Y=MD^{-1}$ (per la dreta): $$X=%s%s=%s,\qquad Y=%s%s=%s$$" % (tx(Di), tx(Mm), tx(X), tx(Mm), tx(Di), tx(Y)),
) + res(r"a) $M=%s$. &nbsp; b) $D^{-1}=%s$. &nbsp; c) $X=%s$, $Y=%s$." % (tx(Mm), tx(Di), tx(X), tx(Y))))

# ---------------- Juny 2003 (1) ----------------
B = M([1, 0, 1], [0, 1, 1], [0, 0, 1]); C = M([1, -1, 0], [-1, 1, 1], [1, 1, 1])
X = sc(Fr(1, 5), add(sc(2, B), C)); Y = sc(Fr(1, 5), sub(B, sc(2, C)))
assert add(sc(2, X), Y) == B and sub(X, sc(2, Y)) == C
BCm = mul(B, C)
sol("M", "Juny 2003", 1, steps(
    r"<strong>Apartat a).</strong> Resolem com un sistema lineal (les matrius se sumen i es multipliquen per nombres com si foren incògnites): multipliquem la primera equació per 2 i hi sumem la segona: $$4X+2Y+X-2Y=2B+C\Rightarrow X=\tfrac15(2B+C)$$ i de la primera, $Y=B-2X=\tfrac15(B-2C)$.",
    r"$$X=\tfrac15\left[%s+%s\right]=%s,\qquad Y=\tfrac15\left[%s-%s\right]=%s$$" % (tx(sc(2, B)), tx(C), nice(X), tx(B), tx(sc(2, C)), nice(Y)),
    r"<strong>Apartat b).</strong> Traiem factor comú $(2X+Y)$ per l'esquerra: $$(2X+Y)X-(2X+Y)(2Y)=(2X+Y)(X-2Y)=B\cdot C=%s%s=%s$$" % (tx(B), tx(C), tx(BCm)),
) + res(r"a) $X=%s$, $Y=%s$. &nbsp; b) $BC=%s$." % (nice(X), nice(Y), tx(BCm))))
assert sub(mul(add(sc(2, X), Y), X), mul(add(sc(2, X), Y), sc(2, Y))) == BCm

# ---------------- Setembre 2003 (1) ----------------
A = M([0, 0, 3], [1, 0, -1], [5, 1, -1]); Bp = M([0, 1, 0], [1, 0, 0], [0, 0, 1])
ih, Ai = inv_html(A, "A"); X = sub(mul(Ai, Bp), Bp); assert sub(Bp, mul(A, X)) == mul(A, Bp)
sol("M", "Setembre 2003", 1, steps(
    r"<strong>Apartat a) Determinant.</strong> $$|A|=\begin{vmatrix}0&m&3\\1&0&-1\\5&1&-(m+1)\end{vmatrix}=-m\left[-(m+1)+5\right]+3(1-0)=m^2-4m+3=(m-1)(m-3)$$ $A$ és invertible si i només si $m\neq1$ i $m\neq3$.",
    r"<strong>Inversa en general.</strong> Calculem els adjunts: $$\mathrm{Adj}(A)=\begin{pmatrix}1&m-4&1\\m^2+m+3&-15&5m\\-m&3&-m\end{pmatrix}\ \Rightarrow\ A^{-1}=\frac{1}{(m-1)(m-3)}\begin{pmatrix}1&m^2+m+3&-m\\m-4&-15&3\\1&5m&-m\end{pmatrix}$$",
    r"<strong>Apartat b) Aïllem $X$.</strong> $$B-AX=AB\Rightarrow AX=B-AB\Rightarrow X=A^{-1}B-B$$",
    r"<strong>Per a $m=0$.</strong> $$A^{-1}=\frac13\begin{pmatrix}1&3&0\\-4&-15&3\\1&0&0\end{pmatrix}=%s$$ $$X=A^{-1}B-B=%s-%s=%s$$" % (nice(Ai), nice(mul(Ai, Bp)), tx(Bp), nice(X)),
    r"<strong>Comprovació.</strong> $B-AX=%s=AB$ ✓." % tx(sub(Bp, mul(A, X))),
) + res(r"a) $m\neq1,3$; $A^{-1}=\frac{1}{(m-1)(m-3)}\begin{pmatrix}1&m^2+m+3&-m\\m-4&-15&3\\1&5m&-m\end{pmatrix}$. &nbsp; b) $X=%s$." % nice(X)))
assert Ai == sc(Fr(1, 3), M([1, 3, 0], [-4, -15, 3], [1, 0, 0]))

# ---------------- Setembre 2003 (2) ----------------
P = M([1, 2], [2, 3]); Q = M([2, 0], [0, 3]); ih, Pi = inv_html(P, "P")
X = mul(P, Q, Pi); X2 = mul(X, X); assert mul(Pi, X, P) == Q and X2 == mul(P, mul(Q, Q), Pi)
sol("M", "Setembre 2003", 2, steps(
    r"<strong>Apartat a).</strong>" + ih,
    r"<strong>Apartat b).</strong> Multipliquem per $P$ per l'esquerra i per $P^{-1}$ per la dreta: $$P^{-1}XP=Q\Rightarrow X=PQP^{-1}=%s%s%s=%s$$" % (tx(P), tx(Q), tx(Pi), tx(X)),
    r"<strong>Apartat c).</strong> $$(PQP^{-1})^2=PQ\,\underbrace{P^{-1}P}_{I}\,QP^{-1}=PQ^2P^{-1}=%s%s%s=%s$$ (és el mateix que $X^2$)." % (tx(P), tx(mul(Q, Q)), tx(Pi), tx(X2)),
) + res(r"a) $P^{-1}=%s$. &nbsp; b) $X=%s$. &nbsp; c) $%s$." % (tx(Pi), tx(X), tx(X2))))

# ---------------- Juny 2004 (1) ----------------
sol("M", "Juny 2004", 1, steps(
    r"<strong>Propietat.</strong> Si $B$ és d'ordre 3, $|2B|=2^3|B|=8|B|$. Per tant $8|B|=160\Rightarrow|B|=20$.",
    r"<strong>Calculem $|B|$.</strong> Restem la primera fila a la tercera (no canvia el determinant) i desenvolupem per la tercera fila: $$|B|=\begin{vmatrix}x&3&1\\x+1&4&2\\0&-1-x^2&0\end{vmatrix}=-(-1-x^2)\begin{vmatrix}x&1\\x+1&2\end{vmatrix}=(1+x^2)(2x-x-1)=(x^2+1)(x-1)$$",
    r"<strong>Resolem.</strong> $$(x^2+1)(x-1)=20\Rightarrow x^3-x^2+x-21=0\Rightarrow(x-3)(x^2+2x+7)=0$$ El factor $x^2+2x+7$ no té arrels reals (discriminant $4-28<0$), així que l'única solució és $x=3$.",
    r"<strong>Comprovació.</strong> $(9+1)(3-1)=20$ ✓.",
) + res(r"$x=3$"))

# ---------------- Setembre 2004 (1) ----------------
sol("M", "Setembre 2004", 1, steps(
    r"<strong>Plantegem.</strong> $$AX=\begin{pmatrix}x+2z&y+2t\\3x+4z&3y+4t\end{pmatrix},\qquad XA=\begin{pmatrix}x+3y&2x+4y\\z+3t&2z+4t\end{pmatrix}$$",
    r"<strong>Igualem element a element.</strong> $$%s\ \Rightarrow\ %s$$" % (sysm("x+2z&=x+3y", "y+2t&=2x+4y", "3x+4z&=z+3t", "3y+4t&=2z+4t"), sysm("2z&=3y", "2t&=2x+3y", "t&=x+z", "3y&=2z")),
    r"<strong>Resolem.</strong> De la primera, $z=\frac32y$; de la tercera, $t=x+\frac32y$ (i la segona i la quarta es compleixen automàticament). Hi ha dos paràmetres lliures, $x$ i $y$.",
) + res(r"$X=\begin{pmatrix}x&y\\\frac32y&x+\frac32y\end{pmatrix}$ amb $x,y\in\mathbb{R}$ (és a dir, $z=\frac32y$, $t=x+\frac32y$)."))
for x_, y_ in ((1, 0), (0, 2), (3, -4)):
    X = M([x_, y_], [Fr(3, 2) * y_, x_ + Fr(3, 2) * y_]); A = M([1, 2], [3, 4]); assert mul(A, X) == mul(X, A)

# ---------------- Setembre 2004 (2) ----------------
A = M([-1, -1, 2], [3, -5, 6], [1, -1, 0]); Bm = mul(A, add(A, sc(4, I(3))))
assert det(A) == -8 and Bm == sc(-4, I(3)) and inv(A) == sub(sc(Fr(-1, 4), A), I(3)) and mul(A, A) == sub(sc(-4, A), sc(4, I(3)))
sol("M", "Setembre 2004", 2, steps(
    r"<strong>Apartat a).</strong> $$|A|=-1(0+6)+1(0-6)+2(-3+5)=-8\neq0$$ Per tant $A^{-1}$ existeix, i $|A^{-1}|=\frac1{|A|}=-\frac18$.",
    r"<strong>Apartat b).</strong> $$A+4I=%s,\qquad B=A(A+4I)=%s%s=%s=-4I$$" % (tx(add(A, sc(4, I(3)))), tx(A), tx(add(A, sc(4, I(3)))), tx(Bm)),
    r"<strong>Apartat c).</strong> De $A(A+4I)=-4I$: $$A\cdot\left[-\tfrac14(A+4I)\right]=I\Rightarrow A^{-1}=-\tfrac14A-I\quad\Rightarrow\quad x=-\tfrac14,\ y=-1$$ I com que $A^2+4A=-4I$: $$A^2=-4A-4I\quad\Rightarrow\quad z=-4,\ t=-4$$",
) + res(r"a) $|A^{-1}|=-\frac18$. &nbsp; b) $B=-4I$. &nbsp; c) $x=-\frac14$, $y=-1$, $z=-4$, $t=-4$."))

# ---------------- Juny 2005 (1) ----------------
A = M([2, -5], [-1, 3]); B = M([-18, 0], [11, 1]); C = M([-17, -30], [10, 18])
ih, Ai = inv_html(A); U = sub(sc(3, C), B); V = sub(sc(2, C), B); X = mul(Ai, U); Y = mul(Ai, V)
assert sub(sc(2, mul(A, X)), sc(3, mul(A, Y))) == B and sub(mul(A, X), mul(A, Y)) == C
sol("M", "Juny 2005", 1, steps(
    r"<strong>Canvi de variables.</strong> Anomenem $U=AX$ i $V=AY$: $$%s$$ De la segona, $U=C+V$; substituint, $2C+2V-3V=B\Rightarrow V=2C-B$, i $U=3C-B$." % sysm("2U-3V&=B", "U-V&=C"),
    r"$$U=3C-B=%s,\qquad V=2C-B=%s$$" % (tx(U), tx(V)),
    r"<strong>Inversa de $A$.</strong>" + ih,
    r"<strong>Calculem $X$ i $Y$.</strong> $$X=A^{-1}U=%s%s=%s,\qquad Y=A^{-1}V=%s%s=%s$$" % (tx(Ai), tx(U), tx(X), tx(Ai), tx(V), tx(Y)),
) + res(r"$x_1=%s,\ x_2=%s,\ x_3=%s,\ x_4=%s$; $\ y_1=%s,\ y_2=%s,\ y_3=%s,\ y_4=%s$." % tuple(ft(v) for v in [X[0][0], X[0][1], X[1][0], X[1][1], Y[0][0], Y[0][1], Y[1][0], Y[1][1]])))

# ---------------- Setembre 2005 (1) ----------------
A = M([1], [2], [3]); B = M([7], [2], [-2]); C = M([0, 0, 0], [0, 1, 0], [0, 0, 1]); D = M([0], [2], [2]); E = M([2], [5], [3])
K = add(mul(A, T(B)), C); AtD = mul(T(A), D)[0][0]; R = sc(AtD, E)
ih, Ki = inv_html(K, "K"); X = mul(Ki, R); assert mul(K, X) == R
sol("M", "Setembre 2005", 1, steps(
    r"<strong>Primer membre.</strong> $$AB^t=%s\begin{pmatrix}7&2&-2\end{pmatrix}=%s,\qquad K=AB^t+C=%s$$" % (tx(A), tx(mul(A, T(B))), tx(K)),
    r"<strong>Segon membre.</strong> $A^tD=\begin{pmatrix}1&2&3\end{pmatrix}%s=0+4+6=10$ (és una matriu $1\times1$, un nombre), així que $(A^tD)E=10E=%s$." % (tx(D), tx(R)),
    r"<strong>Resolem $KX=10E$.</strong>" + ih + r"$$X=K^{-1}\cdot10E=%s%s=%s$$" % (nice(Ki), tx(R), nice(X)),
) + res(r"$X=%s$" % nice(X)))

# ---------------- Juny 2006 (1) ----------------
A = M([2, 2, 1], [-1, -1, -1], [2, 4, 3]); Tm = M([2, 4, 1], [-1, -3, -1], [1, 2, 1])
ih, Ti = inv_html(Tm, "T"); B = mul(Tm, A, Ti); assert mul(Ti, B, Tm) == A and det(B) == det(A)
sol("M", "Juny 2006", 1, steps(
    r"<strong>Apartat a).</strong>" + ih,
    r"<strong>Apartat b).</strong> Pel determinant d'un producte, $|A|=|T^{-1}|\,|B|\,|T|=\frac{1}{|T|}|B||T|=|B|$. I $$|A|=2(-3+4)-2(-3+2)+1(-4+2)=2+2-2=%s$$ Per tant $|B|=%s$." % (ft(det(A)), ft(det(A))),
    r"<strong>Apartat c).</strong> Aïllem $B$ multiplicant per $T$ per l'esquerra i per $T^{-1}$ per la dreta: $$A=T^{-1}BT\Rightarrow B=TAT^{-1}$$ $$TA=%s%s=%s,\qquad B=%s%s=%s$$" % (tx(Tm), tx(A), tx(mul(Tm, A)), tx(mul(Tm, A)), tx(Ti), tx(B)),
) + res(r"a) $T^{-1}=%s$. &nbsp; b) $|B|=%s$. &nbsp; c) $B=%s$." % (tx(Ti), ft(det(A)), tx(B))))

# ---------------- Setembre 2006 (1) ----------------
A2 = M([2, 1, 0], [-1, 0, -1], [-1, -1, 2]); A3 = M([1, 0, 2], [-2, -1, 0], [2, 2, -3])
ih, A3i = inv_html(A3, "(A^3)"); Ainv = mul(A2, A3i)
X = mul(M([1, 2, 3]), Ainv)
Areal = inv(Ainv); assert mul(Areal, Areal) == A2 and mul(Areal, Areal, Areal) == A3
assert mul(X, A3) == mul(M([1, 2, 3]), A2)
sol("M", "Setembre 2006", 1, steps(
    r"<strong>Apartat a).</strong>" + ih,
    r"<strong>Apartat b).</strong> Multipliquem per $(A^3)^{-1}$ per la dreta: $$XA^3=BA^2\Rightarrow X=BA^2(A^3)^{-1}=BA^2A^{-3}=BA^{-1}$$ Calculem $A^{-1}=A^2(A^3)^{-1}$ (les potències de $A$ commuten): $$A^{-1}=%s%s=%s$$ $$X=BA^{-1}=\begin{pmatrix}1&2&3\end{pmatrix}%s=%s$$" % (tx(A2), nice(A3i), tx(Ainv), tx(Ainv), tx(X)),
    r"<strong>Apartat c).</strong> Com hem vist, $A^{-1}=A^2\cdot(A^3)^{-1}$, ja que $A^2\cdot(A^3)^{-1}\cdot A=A^2\cdot A\cdot(A^3)^{-1}=A^3(A^3)^{-1}=I$.",
) + res(r"a) $|A^3|=%s$, $(A^3)^{-1}=%s$. &nbsp; b) $X=%s$. &nbsp; c) $A^{-1}=%s$." % (ft(det(A3)), tx(A3i), tx(X), tx(Ainv))))

# ---------------- Juny 2007 (1) ----------------
assert det(M([3, 7, 12], [2, 3, 6], [3, 2, 6])) == 0
for x_ in (0, 1, 5):
    assert det(sc(3, M([x_ + 2, 4, 6], [2 * x_ + 3, 3, 6], [4 * x_ + 4, 2, 6]))) == 162 * x_
sol("M", "Juny 2007", 1, steps(
    r"<strong>Apartat a) Determinant de $B(x)$.</strong> Traiem el factor 6 de la tercera columna i restem la primera fila a la segona i a la tercera: $$|B(x)|=6\begin{vmatrix}x+2&4&1\\2x+3&3&1\\4x+4&2&1\end{vmatrix}=6\begin{vmatrix}x+2&4&1\\x+1&-1&0\\3x+2&-2&0\end{vmatrix}=6\begin{vmatrix}x+1&-1\\3x+2&-2\end{vmatrix}=6\left[-2x-2+3x+2\right]=6x$$",
    r"<strong>Determinant de $3B(x)$.</strong> Com que és d'ordre 3, $|3B(x)|=3^3|B(x)|=27\cdot6x=162x$. Per tant $162x=162\iff x=1$.",
    r"<strong>Apartat b).</strong> Observem que la tercera columna és la suma de $\begin{pmatrix}5\\3\\4\end{pmatrix}$ i la segona: $C_3=\begin{pmatrix}5\\3\\4\end{pmatrix}+C_2$. Separem la primera columna, $C_1=y\begin{pmatrix}3\\2\\3\end{pmatrix}+\begin{pmatrix}5\\3\\4\end{pmatrix}$: $$|C(y)|=y\begin{vmatrix}3&7&12\\2&3&6\\3&2&6\end{vmatrix}+\begin{vmatrix}5&7&12\\3&3&6\\4&2&6\end{vmatrix}$$ El segon determinant és 0 perquè $C_3=C_1+C_2$. El primer val $3(18-12)-7(12-18)+12(4-9)=18+42-60=0$. Per tant $|C(y)|=0$ per a tot $y$ i $C(y)$ mai no té inversa.",
) + res(r"a) $|3B(x)|=162x$; $x=1$. &nbsp; b) $|C(y)|=0$ per a tot $y$."))

# ---------------- Setembre 2007 (1) ----------------
sol("M", "Setembre 2007", 1, steps(
    r"<strong>Apartat a).</strong> $AX=\alpha X\iff(A-\alpha I)X=0$, un sistema homogeni que només té la solució $X=0$ si $|A-\alpha I|\neq0$: $$|A-\alpha I|=\begin{vmatrix}6-\alpha&4\\-1&1-\alpha\end{vmatrix}=(6-\alpha)(1-\alpha)+4=\alpha^2-7\alpha+10=(\alpha-2)(\alpha-5)$$ Per tant, la solució nul·la és l'única si $\alpha\neq2$ i $\alpha\neq5$.",
    r"<strong>Apartat b).</strong> Per a $\alpha=2$: $$(A-2I)X=\begin{pmatrix}4&4\\-1&-1\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}0\\0\end{pmatrix}\iff x+y=0$$ Les solucions són $x=t$, $y=-t$.",
) + res(r"a) $\alpha\neq2,5$. &nbsp; b) $X=\begin{pmatrix}t\\-t\end{pmatrix}$, $t\in\mathbb{R}$."))
A = M([6, 4], [-1, 1]); assert mul(A, M([1], [-1])) == M([2], [-2])

# ---------------- Juny 2008 (1) ----------------
A = M([17, 29], [-10, -17]); A2 = mul(A, A); A3 = mul(A2, A)
assert A2 == sc(-1, I(2)) and pw(add(I(2), A), 3) == add(sc(-2, I(2)), sc(2, A))
sol("M", "Juny 2008", 1, steps(
    r"<strong>Apartat a).</strong> $$A^2=%s%s=%s=-I,\qquad A^3=A^2A=-A=%s$$" % (tx(A), tx(A), tx(A2), tx(A3)),
    r"<strong>Apartat b).</strong> Com que $I$ i $A$ commuten, podem desenvolupar el cub com el d'un binomi: $$(I+A)^3=I+3A+3A^2+A^3=I+3A-3I-A=-2I+2A$$ Per tant $\alpha=-2$ i $\beta=2$.",
) + res(r"a) $A^2=-I$, $A^3=-A=%s$. &nbsp; b) $\alpha=-2$, $\beta=2$." % tx(A3)))

# ---------------- Setembre 2008 (1) ----------------
sol("M", "Setembre 2008", 1, steps(
    r"<strong>Apartat a).</strong> $AX=0X=0$ és un sistema homogeni amb $|A|=4+2=6\neq0$: només té la solució $X=\begin{pmatrix}0\\0\end{pmatrix}$.",
    r"<strong>Apartat b).</strong> $AX=3X\iff(A-3I)X=0$: $$\begin{pmatrix}-2&-1\\2&1\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}0\\0\end{pmatrix}\iff y=-2x$$ (les dues equacions són proporcionals, $|A-3I|=0$). Solucions: $X=\begin{pmatrix}t\\-2t\end{pmatrix}$.",
    r"<strong>Apartat c).</strong> $AX=2X\iff(A-2I)X=0$: $$\begin{pmatrix}-1&-1\\2&2\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}0\\0\end{pmatrix}\iff y=-x$$ Solucions: $X=\begin{pmatrix}t\\-t\end{pmatrix}$.",
) + res(r"a) $X=\begin{pmatrix}0\\0\end{pmatrix}$. &nbsp; b) $X=\begin{pmatrix}t\\-2t\end{pmatrix}$. &nbsp; c) $X=\begin{pmatrix}t\\-t\end{pmatrix}$, $t\in\mathbb{R}$."))
A = M([1, -1], [2, 4]); assert mul(A, M([1], [-2])) == M([3], [-6]) and mul(A, M([1], [-1])) == M([2], [-2])

# ---------------- Juny 2009 (1) ----------------
A = M([3, 6, 0], [0, 3, 2], [0, 0, 1]); B = M([18, 48, 12], [0, 18, 12], [0, 0, 6])
ih, Ai = inv_html(A); A2 = mul(A, A)
assert add(add(sc(3, I(3)), sc(2, A)), A2) == B
sol("M", "Juny 2009", 1, steps(
    r"<strong>Apartat a).</strong> $A$ és triangular, $|A|=3\cdot3\cdot1=9\neq0$." + ih,
    r"<strong>Apartat b).</strong> Per a una matriu d'ordre 3, $|3A^{-1}|=3^3|A^{-1}|=\frac{27}{|A|}=\frac{27}{9}=3$.",
    r"<strong>Apartat c).</strong> $$A^2=%s,\qquad xI+yA+zA^2=\begin{pmatrix}x+3y+9z&6y+36z&12z\\0&x+3y+9z&2y+8z\\0&0&x+y+z\end{pmatrix}=%s$$ Igualant: $12z=12\Rightarrow z=1$; $2y+8z=12\Rightarrow y=2$; $x+y+z=6\Rightarrow x=3$. Es comprova que $6y+36z=48$ ✓ i $x+3y+9z=18$ ✓." % (tx(A2), tx(B)),
) + res(r"a) $A^{-1}=%s$. &nbsp; b) $|3A^{-1}|=3$. &nbsp; c) $x=3,\ y=2,\ z=1$." % nice(Ai)))

# ---------------- Setembre 2009 (1) ----------------
for a_ in (6, -6):
    assert det(M([1, 2, a_ - 2], [4, 3, 2], [a_, a_, -6])) == 66
sol("M", "Setembre 2009", 1, steps(
    r"<strong>Apartat a).</strong> Desenvolupem per la primera fila: $$|A(\alpha)|=1(-18-2\alpha)-2(-24-2\alpha)+(\alpha-2)(4\alpha-3\alpha)=-18-2\alpha+48+4\alpha+\alpha^2-2\alpha=\alpha^2+30$$",
    r"<strong>Apartat b).</strong> $|A(\alpha)|=\alpha^2+30\geq30>0$, així que sempre hi ha inversa, i $|A(\alpha)^{-1}|=\frac{1}{\alpha^2+30}$. Imposem: $$\frac{1}{\alpha^2+30}=\frac1{66}\iff\alpha^2=36\iff\alpha=\pm6$$",
) + res(r"a) $|A(\alpha)|=\alpha^2+30$. &nbsp; b) $\alpha=6$ o $\alpha=-6$."))

# ---------------- Juny 2010 (1) ----------------
A = M([2, 1, 1], [2, 3, 2], [-3, -3, -2]); AmI = sub(A, I(3)); Am2 = sub(A, sc(2, I(3)))
assert mul(AmI, AmI) == sc(0, I(3)) and mul(A, Am2) == sc(-1, I(3)) and det(AmI) == 0
sol("M", "Juny 2010", 1, steps(
    r"<strong>Apartat a).</strong> $$A-I=%s,\qquad (A-I)^2=%s%s=%s=O$$ $$A-2I=%s,\qquad A(A-2I)=%s%s=%s=-I$$" % (tx(AmI), tx(AmI), tx(AmI), tx(mul(AmI, AmI)), tx(Am2), tx(A), tx(Am2), tx(mul(A, Am2))),
    r"<strong>Apartat b.1).</strong> De $A(A-2I)=-I$ resulta $A\cdot\left[-(A-2I)\right]=I$ i $\left[-(A-2I)\right]A=I$ (les dues matrius commuten). Per tant $A$ és invertible amb $A^{-1}=-(A-2I)$, i $A-2I$ és invertible amb $(A-2I)^{-1}=-A$. (També: $|A|\cdot|A-2I|=|-I|=-1\neq0$, així que cap dels dos determinants és 0.)",
    r"<strong>Apartat b.2).</strong> De $(A-I)^2=O$, $|A-I|^2=|O|=0$, és a dir, $|A-I|=0$: $A-I$ no té inversa.",
    r"<strong>Apartat c).</strong> Hem vist que $A^{-1}=-(A-2I)$, per tant $\lambda=-1$.",
) + res(r"a) $(A-I)^2=O$, $A(A-2I)=-I$. &nbsp; b) $A^{-1}=2I-A$, $(A-2I)^{-1}=-A$; $|A-I|=0$. &nbsp; c) $\lambda=-1$."))

# ---------------- Setembre 2010 (1) ----------------
for x_ in (0, 6):
    assert det(M([x_ + 2, 4, 3], [x_ + 2, 6, 2], [x_ + 3, 8, 2])) == 2 * x_ - 6
for y_ in (0, 7):
    assert det(M([y_ + 1, 4, 3], [y_ + 2, 6, 2], [y_ + 3, 8, 1])) == 0
sol("M", "Setembre 2010", 1, steps(
    r"<strong>Apartat a).</strong> Restem la primera fila a la segona i a la tercera: $$|A(x)|=\begin{vmatrix}x+2&4&3\\0&2&-1\\1&4&-1\end{vmatrix}=(x+2)(-2+4)-4(0+1)+3(0-2)=2x-6$$ $2x-6=6\iff x=6$.",
    r"<strong>Apartat b).</strong> $A(x)$ és d'ordre 3, així que $|2A(x)|=2^3|A(x)|=8(2x-6)=16x-48$. Per al valor $x=6$ de l'apartat anterior, $|2A(6)|=8\cdot6=48$.",
    r"<strong>Apartat c).</strong> Restem la primera fila a la segona i a la tercera: $$|B(y)|=\begin{vmatrix}y+1&4&3\\1&2&-1\\2&4&-2\end{vmatrix}=0$$ perquè la tercera fila és el doble de la segona. Com que $|B(y)|=0$ per a tot $y$, $B(y)$ no té inversa.",
) + res(r"a) $x=6$. &nbsp; b) $|2A(x)|=8|A(x)|=16x-48$ (val 48 per a $x=6$). &nbsp; c) $|B(y)|=0$ sempre."))

# ---------------- Juny 2011 (1) ----------------
A = M([-1, 0, 1], [0, 1, 0], [2, 1, 0]); ih, Ai = inv_html(A)
assert mul(A, Ai) == I(3) and mul(Ai, A) == I(3)
sol("M", "Juny 2011", 1, steps(
    r"<strong>Apartat a).</strong> Desenvolupem per la segona fila: $$|A|=m\begin{vmatrix}-1&1\\2&m^2-1\end{vmatrix}=m\left(-m^2+1-2\right)=-m(m^2+1)$$ Com que $m^2+1>0$, $|A|=0\iff m=0$. Si $m\neq0$, $\operatorname{rg}(A)=3$. Si $m=0$, $A=\begin{pmatrix}-1&0&1\\0&0&0\\2&1&-1\end{pmatrix}$ i $\begin{vmatrix}-1&0\\2&1\end{vmatrix}=-1\neq0$, així que $\operatorname{rg}(A)=2$.",
    r"<strong>Apartat b).</strong> Per a $m=1$, $|A|=-1\cdot2=-2\neq0$, així que $A$ és invertible.",
    r"<strong>Apartat c).</strong> Passos: (1) calculem $|A|$; (2) la matriu d'adjunts; (3) la transposem; (4) dividim per $|A|$." + ih + r"Comprovació: $AA^{-1}=%s\cdot%s=I$ i $A^{-1}A=I$ ✓." % (tx(A), nice(Ai)),
) + res(r"a) $\operatorname{rg}A=3$ si $m\neq0$; $\operatorname{rg}A=2$ si $m=0$. &nbsp; b) $|A|=-2\neq0$. &nbsp; c) $A^{-1}=%s$." % nice(Ai)))

# ---------------- Setembre 2011 (1) ----------------
A = M([0, -2], [1, 3]); B3 = sub(A, sc(3, I(2))); ih, B3i = inv_html(B3, "B")
A2 = mul(A, A); assert sub(A2, sc(3, A)) == sc(-2, I(2))
sol("M", "Setembre 2011", 1, steps(
    r"<strong>Apartat a).</strong> $$|A-kI|=\begin{vmatrix}-k&-2\\1&3-k\end{vmatrix}=-k(3-k)+2=k^2-3k+2=(k-1)(k-2)$$ $B$ té inversa si $k\neq1$ i $k\neq2$.",
    r"<strong>Apartat b) $k=3$.</strong> $B=%s$." % tx(B3) + ih,
    r"<strong>Apartat c).</strong> $$A^2=%s,\qquad \alpha A^2+\beta A=\begin{pmatrix}-2\alpha&-6\alpha-2\beta\\3\alpha+\beta&7\alpha+3\beta\end{pmatrix}=\begin{pmatrix}-2&0\\0&-2\end{pmatrix}$$ De $-2\alpha=-2$, $\alpha=1$; de $3\alpha+\beta=0$, $\beta=-3$; i es comprova $7-9=-2$ ✓ i $-6+6=0$ ✓." % tx(A2),
    r"<strong>Apartat d).</strong> Fent servir $M^2=M$ (i que $I$ commuta amb tot): $$P^2=(I-M)^2=I-2M+M^2=I-2M+M=I-M=P$$ $$MP=M(I-M)=M-M^2=O,\qquad PM=(I-M)M=M-M^2=O$$ Per tant $MP=PM$ (les dues són la matriu nul·la).",
) + res(r"a) $k\neq1,2$. &nbsp; b) $B^{-1}=%s$. &nbsp; c) $\alpha=1$, $\beta=-3$. &nbsp; d) Comprovat." % tx(B3i)))

# ---------------- Setembre 2011 (2) ----------------
Mm = M([1, 2, 1], [2, 1, 1], [2, 1, -1]); assert det(Mm) == 6
sol("M", "Setembre 2011", 2, steps(
    r"<strong>Determinant de $M$.</strong> $$|M|=1(-1-1)-2(-2-2)+1(2-2)=-2+8=6$$",
    r"<strong>Apartat a).</strong> Si multipliquem una matriu d'ordre $n$ per un nombre $k$, el determinant queda multiplicat per $k^n$ (cada fila aporta un factor $k$): $$\left|\tfrac12T\right|=\left(\tfrac12\right)^3|T|=\frac{\sqrt2}{8}$$",
    r"<strong>Apartat b).</strong> El determinant d'un producte és el producte de determinants: $|M^4|=|M|^4=6^4=1296$.",
    r"<strong>Apartat c).</strong> $$|TM^3T^{-1}|=|T|\,|M|^3\,|T^{-1}|=|T|\,|M|^3\,\frac{1}{|T|}=|M|^3=216$$ (fent servir $|T^{-1}|=\frac1{|T|}$).",
) + res(r"a) $\frac{\sqrt2}8$. &nbsp; b) $1296$. &nbsp; c) $216$."))

# ---------------- Juny 2012 (1) ----------------
sol("M", "Juny 2012", 1, steps(
    r"<strong>Apartat a).</strong> És el sistema $%s$. Resolem per Gauss:" % sysm("x+2z&=1", "x+y+3z&=3", "x-y+z&=-1") + G([[1, 0, 2, 1], [1, 1, 3, 3], [1, -1, 1, -1]])[0],
    r"<strong>Apartat b).</strong> Prenent determinants a $B^2=B$: $|B|^2=|B|\Rightarrow|B|(|B|-1)=0$. Com que $B$ té inversa, $|B|\neq0$, i per tant $|B|=1$. (De fet, multiplicant $B^2=B$ per $B^{-1}$ resulta $B=I$.)",
    r"<strong>Apartat c).</strong> L'equació és $A^2=9I$, amb $I$ d'ordre 4. Prenent determinants: $$|A|^2=|9I|=9^4\,|I|=6561\Rightarrow|A|=\pm81$$ Com que $|A|>0$, $|A|=81$.",
) + res(r"a) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; b) $|B|=1$. &nbsp; c) $|A|=81$." % tuple(G([[1, 0, 2, 1], [1, 1, 3, 3], [1, -1, 1, -1]])[1])))

# ---------------- Setembre 2012 (1) ----------------
A = M([1, -1], [1, 1]); assert mul(A, A) == sub(sc(2, A), sc(2, I(2)))
sol("M", "Setembre 2012", 1, steps(
    r"<strong>Apartat a).</strong> $$A^2=%s,\qquad aA+bU=\begin{pmatrix}a+b&-a\\a&a+b\end{pmatrix}$$ Igualant: $-a=-2\Rightarrow a=2$ i $a+b=0\Rightarrow b=-2$." % tx(mul(A, A)),
    r"<strong>Apartat b).</strong> $$B^2=-7B+U\Rightarrow B^2+7B=U\Rightarrow B(B+7U)=U$$ i també $(B+7U)B=U$. Per tant $B$ té inversa i $B^{-1}=B+7U$: $p=1$, $q=7$.",
    r"<strong>Apartat c).</strong> $$B^3=B\cdot B^2=B(-7B+U)=-7B^2+B=-7(-7B+U)+B=50B-7U$$ Per tant $x=50$, $y=-7$.",
) + res(r"a) $a=2$, $b=-2$. &nbsp; b) $p=1$, $q=7$. &nbsp; c) $x=50$, $y=-7$."))

# ---------------- Juny 2013 (1) ----------------
A = M([-2, 0, 0], [1, 1, 0], [4, 2, -2]); B = M([2, 1, 2], [0, -1, 5], [0, 0, 2]); S = add(A, B)
assert det(A) == 4 and det(B) == -4 and det(S) == 24
sol("M", "Juny 2013", 1, steps(
    r"<strong>Determinants bàsics.</strong> $A$ i $B$ són triangulars: $|A|=(-2)\cdot1\cdot(-2)=4$, $|B|=2\cdot(-1)\cdot2=-4$. $$A+B=%s,\qquad |A+B|=0-1(0-20)+2(2-0)=24$$" % tx(S),
    r"<strong>Apartat a).</strong> $|A+B|=24$ i, com que són matrius d'ordre 3, $$\left|\tfrac12(A+B)^{-1}\right|=\left(\tfrac12\right)^3\frac{1}{|A+B|}=\frac18\cdot\frac1{24}=\frac1{192}$$",
    r"<strong>Apartat b).</strong> $$|(A+B)^{-1}A|=\frac{|A|}{|A+B|}=\frac4{24}=\frac16,\qquad |A^{-1}(A+B)|=\frac{|A+B|}{|A|}=\frac{24}4=6$$",
    r"<strong>Apartat c).</strong> $$|2ABA^{-1}|=2^3|A|\,|B|\,\frac1{|A|}=8|B|=-32,\qquad |A^3B^{-1}|=\frac{|A|^3}{|B|}=\frac{64}{-4}=-16$$",
) + res(r"a) $24$ i $\frac1{192}$. &nbsp; b) $\frac16$ i $6$. &nbsp; c) $-32$ i $-16$."))

# ---------------- Juliol 2013 (1) ----------------
A = M([1, 0, 0], [0, -4, 10], [0, -3, 7]); A2 = mul(A, A)
assert add(sub(A2, sc(3, A)), sc(2, I(3))) == sc(0, I(3)) and pw(A, 3) == sub(sc(7, A), sc(6, I(3)))
sol("M", "Juliol 2013", 1, steps(
    r"<strong>Apartat a).</strong> Fent servir la propietat associativa i que $AB=BA$: $$A^2B^2=A\,(AB)\,B=A\,(BA)\,B=(AB)(AB)=(AB)^2$$",
    r"<strong>Apartat b).</strong> $$A^2=%s,\qquad A^2-3A+2I=%s-%s+%s=O\ ✓$$ Si $A^2-3A+2I=O$, aleshores $A^2-3A=-2I$, és a dir, $A(A-3I)=-2I$ i $$A\cdot\left[-\tfrac12(A-3I)\right]=I$$ (i igual multiplicant per l'altre costat). Per tant $A$ té inversa: $A^{-1}=-\frac12(A-3I)=\frac12(3I-A)$." % (tx(A2), tx(A2), tx(sc(3, A)), tx(sc(2, I(3)))),
    r"<strong>Apartat c).</strong> $A^2=3A-2I$, així que $$A^3=A\cdot A^2=3A^2-2A=3(3A-2I)-2A=7A-6I$$ Per tant $\alpha=7$, $\beta=-6$.",
) + res(r"a) Demostrat. &nbsp; b) Es compleix; $A^{-1}=\frac12(3I-A)$. &nbsp; c) $\alpha=7$, $\beta=-6$."))

# ---------------- Juny 2014 (1) ----------------
A = M([1, -1, 1], [0, 1, 1], [0, 0, 1]); Bc = M([-2], [1], [-1]); Cr = M([-1, 1, 3])
ih, Ai = inv_html(A); BC = mul(Bc, Cr); X = mul(Ai, BC); assert mul(A, X) == BC
sol("M", "Juny 2014", 1, steps(
    r"<strong>Apartat a).</strong>" + ih,
    r"<strong>Apartat b).</strong> $AX=BC\Rightarrow X=A^{-1}BC$. $$BC=%s\begin{pmatrix}-1&1&3\end{pmatrix}=%s,\qquad X=%s%s=%s$$" % (tx(Bc), tx(BC), tx(Ai), tx(BC), tx(X)),
    r"<strong>Apartat c).</strong> $M$ és d'ordre 2: $$|2M^3|=2^2|M|^3=4\cdot\frac18=\frac12$$",
) + res(r"a) $A^{-1}=%s$. &nbsp; b) $X=%s$. &nbsp; c) $\frac12$." % (tx(Ai), tx(X))))

# ---------------- Juliol 2014 (1) ----------------
S = M([2, -2, 1], [1, 1, 1], [-1, 3, 5]); ih, Si = inv_html(S, "S"); assert det(S) == 20
sol("M", "Juliol 2014", 1, steps(
    r"<strong>Apartat a).</strong>" + ih + r"Una matriu quadrada $S$ té inversa si i només si $|S|\neq0$ (perquè $S^{-1}=\frac{1}{|S|}\mathrm{Adj}(S)^t$; i si $S^{-1}$ existeix, $|S|\,|S^{-1}|=|I|=1$, de manera que $|S|\neq0$).",
    r"<strong>Apartat b).</strong> $T$ és d'ordre 3, $|T|=20$: $$\left|(4T^2)^{-1}\right|=\frac{1}{|4T^2|}=\frac{1}{4^3|T|^2}=\frac1{64\cdot400}=\frac1{25600}$$",
    r"<strong>Apartat c).</strong> Igualem els elements que no coincideixen: $$a^2-1=a+1\iff a^2-a-2=0\iff a=2\ \text{o}\ a=-1;\qquad a^2+4=4a\iff(a-2)^2=0\iff a=2$$ L'únic valor que compleix totes les igualtats és $a=2$.",
) + res(r"a) $|S|=20$, $S^{-1}=%s$. &nbsp; b) $\frac{1}{25600}$. &nbsp; c) $a=2$." % nice(Si)))

# ---------------- Juny 2015 (1) ----------------
A = M([1, -3], [2, 2]); B = M([1, 3], [2, -2]); ih, Ai = inv_html(A)
X = mul(B, Ai); Y = mul(Ai, B); assert mul(X, A) == B and mul(A, Y) == B
sol("M", "Juny 2015", 1, steps(
    r"<strong>Apartat a).</strong>" + ih,
    r"<strong>Apartat b).</strong> $XA=B\Rightarrow X=BA^{-1}$ i $AY=B\Rightarrow Y=A^{-1}B$: $$X=%s%s=%s,\qquad Y=%s%s=%s$$" % (tx(B), nice(Ai), nice(X), nice(Ai), tx(B), nice(Y)),
    r"<strong>Apartat c).</strong> Si $M^2=I$: $$M^3=M^2M=IM=M,\qquad M^7=(M^2)^3M=I^3M=M$$ Per tant $M^3=M^7$.",
) + res(r"a) $A^{-1}=%s$. &nbsp; b) $X=%s$, $Y=%s$. &nbsp; c) Les dues són iguals a $M$." % (nice(Ai), nice(X), nice(Y))))

# ---------------- Juliol 2015 (1) ----------------
Ax = M([-1, 1, -1], [0, 2, 3], [1, 1, 0])
assert mul(Ax, Ax) == M([0, 0, 4], [3, 7, 6], [-1, 3, 2])
sol("M", "Juliol 2015", 1, steps(
    r"<strong>Apartat a).</strong> Desenvolupem per la tercera fila: $$|B|=\begin{vmatrix}x&1&-1\\1&2&3\\0&1&0\end{vmatrix}=-1\cdot\begin{vmatrix}x&-1\\1&3\end{vmatrix}=-(3x+1)$$ $B$ té inversa si $x\neq-\frac13$.",
    r"<strong>Apartat b).</strong> $|A^3|=|A|^3=8^3=512$. A la segona matriu, la primera columna és la de $A$ multiplicada per 2 i la segona és la de $A$ multiplicada per 5: $$\begin{vmatrix}2x&5&-1\\2y&10&3\\2z&5&0\end{vmatrix}=2\cdot5\,|A|=80$$",
    r"<strong>Apartat c).</strong> $$A^2=\begin{pmatrix}x^2+y-z&x+1&3-x\\xy+2y+3z&y+7&6-y\\xz+y&z+2&3-z\end{pmatrix}=\begin{pmatrix}0&0&4\\3&7&6\\-1&3&2\end{pmatrix}$$ De la segona columna: $x+1=0$, $y+7=7$, $z+2=3$, és a dir, $x=-1$, $y=0$, $z=1$. Comprovem la resta: $1+0-1=0$ ✓, $3-(-1)=4$ ✓, $0+0+3=3$ ✓, $6-0=6$ ✓, $-1+0=-1$ ✓, $3-1=2$ ✓.",
) + res(r"a) $x\neq-\frac13$. &nbsp; b) $512$ i $80$. &nbsp; c) $x=-1$, $y=0$, $z=1$."))

# ---------------- Juny 2016 (1) ----------------
sol("M", "Juny 2016", 1, steps(
    r"<strong>Apartat a).</strong> $$A\cdot A^t=\begin{pmatrix}\sqrt5&0&0\\0&1&-2\\0&2&1\end{pmatrix}\begin{pmatrix}\sqrt5&0&0\\0&1&2\\0&-2&1\end{pmatrix}=\begin{pmatrix}5&0&0\\0&5&0\\0&0&5\end{pmatrix}=5I$$ Per tant $A\cdot\left(\tfrac15A^t\right)=I$, és a dir, $A^{-1}=5^{-1}A^t$.",
    r"<strong>Apartat b).</strong> Desenvolupem per la primera fila: $$|A-\lambda I|=\begin{vmatrix}\sqrt5-\lambda&0&0\\0&1-\lambda&-2\\0&2&1-\lambda\end{vmatrix}=(\sqrt5-\lambda)\left[(1-\lambda)^2+4\right]$$ El segon factor és sempre positiu, així que $|A-\lambda I|=0\iff\lambda=\sqrt5$. $A-\lambda I$ no és invertible només per a $\lambda=\sqrt5$.",
    r"<strong>Apartat c).</strong> $|B^{-1}|=\frac1{|B|}$ i $|B^t|=|B|$. Llavors $\frac1{|B|}=|B|\Rightarrow|B|^2=1\Rightarrow|B|=\pm1$, i com que és positiu, $|B|=1$.",
) + res(r"a) $AA^t=5I$. &nbsp; b) $\lambda=\sqrt5$. &nbsp; c) $|B|=1$."))

# ---------------- Juliol 2016 (1) ----------------
A = M([1, 1, -1], [1, 2, 1], [0, 1, 1]); B = M([0, 1, -1], [2, 1, 2], [1, 0, -1])
assert det(A) == -1 and det(B) == 5
ih, Ai = inv_html(A); S = add(A, B); ihs, Si = inv_html(S, "(A+B)"); X = sc(3, Si)
assert mul(S, X) == sc(3, I(3)) and inv(mul(inv(mul(B, A)), B)) == A
sol("M", "Juliol 2016", 1, steps(
    r"<strong>Determinants.</strong> $|A|=1(2-1)-1(1-0)-1(1-0)=-1$ i $|B|=0-1(-2-2)-1(0-1)=5$.",
    r"<strong>Apartat a).</strong> Totes són d'ordre 3: $$|A\cdot(2B^2)|=|A|\cdot2^3|B|^2=-1\cdot8\cdot25=-200$$ $$|A\cdot(2B^2)\cdot(3A)^{-1}|=\frac{-200}{|3A|}=\frac{-200}{27\cdot(-1)}=\frac{200}{27}$$",
    r"<strong>Apartat b).</strong>" + ih + r"Fent servir $(PQ)^{-1}=Q^{-1}P^{-1}$: $$\left((BA)^{-1}B\right)^{-1}=B^{-1}\left((BA)^{-1}\right)^{-1}=B^{-1}BA=A=%s$$" % tx(A),
    r"<strong>Apartat c).</strong> $AX+BX=3I\Rightarrow(A+B)X=3I\Rightarrow X=3(A+B)^{-1}$:" + ihs + r"$$X=3(A+B)^{-1}=%s$$" % tx(X),
) + res(r"a) $-200$ i $\frac{200}{27}$. &nbsp; b) $A^{-1}=%s$; $\left((BA)^{-1}B\right)^{-1}=A$. &nbsp; c) $X=%s$." % (tx(Ai), tx(X))))

# ---------------- Juny 2017 (1) ----------------
C = M([5, -4, 2], [2, -1, 1], [-4, 4, -1]); C2 = mul(C, C)
assert C2 == sub(sc(2, C), I(3)) and pw(C, 4) == sub(sc(4, C), sc(3, I(3)))
sol("M", "Juny 2017", 1, steps(
    r"<strong>Apartat a).</strong> $$C^2=%s,\qquad 2C-I=%s-%s=%s\ ✓$$ Llavors $$C^4=(C^2)^2=(2C-I)^2=4C^2-4C+I=4(2C-I)-4C+I=4C-3I=%s$$" % (tx(C2), tx(sc(2, C)), tx(I(3)), tx(sub(sc(2, C), I(3))), tx(pw(C, 4))),
    r"<strong>Apartat b).</strong> $A$ és d'ordre 4 i $|A|=-1$: $$\left|(3A^4)(4A^2)^{-1}\right|=\frac{3^4|A|^4}{4^4|A|^2}=\frac{81\cdot1}{256\cdot1}=\frac{81}{256}$$",
    r"<strong>Apartat c).</strong> Multipliquem $BB=B$ per $B^{-1}$: $B^{-1}BB=B^{-1}B\Rightarrow B=I$. L'única matriu és la identitat.",
) + res(r"a) $C^4=4C-3I=%s$. &nbsp; b) $\frac{81}{256}$. &nbsp; c) $B=I$." % tx(pw(C, 4))))

# ---------------- Juliol 2017 (1) ----------------
sol("M", "Juliol 2017", 1, steps(
    r"<strong>Apartat a).</strong> $$A^2=-A-I\Rightarrow A^2+A=-I\Rightarrow A(-A-I)=I$$ i també $(-A-I)A=I$. Per tant $A$ és invertible i $A^{-1}=-A-I$. A més: $$A^3=A\cdot A^2=A(-A-I)=-A^2-A=-(-A-I)-A=I$$",
    r"<strong>Apartat b).</strong> Prenent determinants a $2B^3=B$ (ordre 3): $$2^3|B|^3=|B|\Rightarrow|B|\left(8|B|^2-1\right)=0\Rightarrow|B|=0\ \text{o}\ |B|=\pm\frac{1}{2\sqrt2}=\pm\frac{\sqrt2}{4}$$",
    r"<strong>Apartat c).</strong> Si $B$ té inversa, $|B|\neq0$ i $|B|^2=\frac18$. Per tant $|B^2|=|B|^2=\frac18$. (També: multiplicant $2B^3=B$ per $B^{-1}$, $2B^2=I$ i $8|B^2|=1$.)",
) + res(r"a) $A^{-1}=-A-I$, $A^3=I$. &nbsp; b) $|B|\in\left\{0,\frac{\sqrt2}4,-\frac{\sqrt2}4\right\}$. &nbsp; c) $|B^2|=\frac18$."))

# ---------------- Juliol 2017 (2) ----------------
A = M([0, 0, -1], [0, 1, 0], [1, 0, 0]); ih, Ai = inv_html(A); A2 = mul(A, A)
assert pw(A, 4) == I(3) and pw(A, 7) == Ai and pw(A, 30) == A2 and pw(A, 100) == I(3)
sol("M", "Juliol 2017", 2, steps(
    r"<strong>Apartat a).</strong>" + ih,
    r"<strong>Apartat b).</strong> $$A^2=%s,\qquad A^4=(A^2)^2=%s=I$$" % (tx(A2), tx(mul(A2, A2))),
    r"<strong>Apartat c).</strong> Dividim l'exponent entre 4: $$A^7=A^4A^3=A^3=A^{-1}=%s$$ (perquè $A^3A=A^4=I$); $$A^{30}=(A^4)^7A^2=A^2=%s,\qquad A^{100}=(A^4)^{25}=I$$" % (tx(Ai), tx(A2)),
) + res(r"a) $A^{-1}=%s$. &nbsp; b) $A^4=I$. &nbsp; c) $A^7=%s$, $A^{30}=%s$, $A^{100}=I$." % (tx(Ai), tx(Ai), tx(A2))))

# ---------------- Juny 2018 (1) ----------------
sol("M", "Juny 2018", 1, steps(
    r"<strong>Apartat a).</strong> $$A^2+2A=3I\Rightarrow A(A+2I)=3I\Rightarrow A\cdot\tfrac13(A+2I)=I$$ Per tant $A^{-1}=\frac13A+\frac23I$: $a=\frac13$, $b=\frac23$.",
    r"<strong>Apartat b).</strong> $A^2=3I-2A$, així que $$A^4=(A^2)^2=(3I-2A)^2=9I-12A+4A^2=9I-12A+4(3I-2A)=21I-20A$$ Per tant $\alpha=-20$, $\beta=21$.",
    r"<strong>Apartat c).</strong> $B$ és d'ordre 3 i $|B|=2$: $$|2B^{-1}|=2^3\cdot\frac1{|B|}=\frac82=4$$",
) + res(r"a) $a=\frac13$, $b=\frac23$. &nbsp; b) $\alpha=-20$, $\beta=21$. &nbsp; c) $4$."))

# ---------------- Juliol 2018 (1) ----------------
Am = M([1, 0], [0, 0]); Bm = M([0, 0], [1, 1])
assert mul(Bm, Bm) == Bm and mul(Am, Bm) != Am and mul(Bm, Am) != Bm
sol("M", "Juliol 2018", 1, steps(
    r"<strong>Apartat a).</strong> Fent servir $AB=A$ i $BA=B$: $$A^2=A\cdot A=(AB)A=A(BA)=AB=A,\qquad B^2=B\cdot B=(BA)B=B(AB)=BA=B$$",
    r"<strong>Apartat b).</strong> $$B^2=\begin{pmatrix}a&0\\1&b\end{pmatrix}\begin{pmatrix}a&0\\1&b\end{pmatrix}=\begin{pmatrix}a^2&0\\a+b&b^2\end{pmatrix}=B\iff a^2=a,\ b^2=b,\ a+b=1$$ Les opcions són $(a,b)=(1,0)$ o $(0,1)$. A més, $AB=\begin{pmatrix}a&0\\0&0\end{pmatrix}\neq A\iff a\neq1$, i $BA=\begin{pmatrix}a&0\\1&0\end{pmatrix}\neq B\iff b\neq0$. Només serveix $a=0$, $b=1$.",
    r"<strong>Apartat c).</strong> En el primer, la primera columna està multiplicada per 2: $$\begin{vmatrix}2x&1&0\\2y&2&1\\2z&3&2\end{vmatrix}=2\cdot3=6$$ En el segon, separem la primera columna en suma: $$\begin{vmatrix}x+1&1&0\\y+3&2&1\\z+5&3&2\end{vmatrix}=\begin{vmatrix}x&1&0\\y&2&1\\z&3&2\end{vmatrix}+\begin{vmatrix}1&1&0\\3&2&1\\5&3&2\end{vmatrix}=3+0=3$$ El segon determinant és 0 perquè la primera columna és la suma de les altres dues.",
) + res(r"a) Demostrat. &nbsp; b) $a=0$, $b=1$. &nbsp; c) $6$ i $3$."))
assert det(M([1, 1, 0], [3, 2, 1], [5, 3, 2])) == 0

# ---------------- Juliol 2019 (1) ----------------
A = M([1, 4], [-1, 6]); assert mul(A, M([4], [1])) == M([8], [2]) and mul(A, M([1], [1])) == M([5], [5])
sol("M", "Juliol 2019", 1, steps(
    r"<strong>Apartat a).</strong> $AX=\alpha X\iff(A-\alpha I)X=0$, homogeni; té solució única (la nul·la) si $|A-\alpha I|\neq0$: $$|A-\alpha I|=\begin{vmatrix}1-\alpha&4\\-1&6-\alpha\end{vmatrix}=(1-\alpha)(6-\alpha)+4=\alpha^2-7\alpha+10=(\alpha-2)(\alpha-5)$$ Sols admet una solució si $\alpha\neq2$ i $\alpha\neq5$.",
    r"<strong>Apartat b).</strong> $$(A-5I)X=\begin{pmatrix}-4&4\\-1&1\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}0\\0\end{pmatrix}\iff x=y$$ Solucions: $X=\begin{pmatrix}t\\t\end{pmatrix}$, $t\in\mathbb{R}$.",
    r"<strong>Apartat c).</strong> $A\begin{pmatrix}4\\1\end{pmatrix}=\begin{pmatrix}4+4\\-4+6\end{pmatrix}=\begin{pmatrix}8\\2\end{pmatrix}=2\begin{pmatrix}4\\1\end{pmatrix}$ ✓. Anomenem $v=\begin{pmatrix}4\\1\end{pmatrix}$. Aplicant $A$ repetidament: $A^2v=A(2v)=2Av=2^2v$, i en general $A^nv=2^nv$. Per tant $A^{100}v=2^{100}v$.",
) + res(r"a) $\alpha\neq2,5$. &nbsp; b) $X=\begin{pmatrix}t\\t\end{pmatrix}$. &nbsp; c) $\beta=2^{100}$."))

# ---------------- Juliol 2020 (1) ----------------
for b_ in (0, 1, 3):
    A = M([1, 2], [b_, 0], [-1, 2]); B = M([-1, 0, 2], [-1, b_, -1])
    assert det(mul(A, B)) == 0 and det(mul(B, A)) == 12 - 2 * b_ * b_ and mul(T(A), A) == M([b_ * b_ + 2, 0], [0, 8])
sol("M", "Juliol 2020", 1, steps(
    r"<strong>Apartat a).</strong> $AB$ és $3\times3$, però $\operatorname{rg}(AB)\leq\operatorname{rg}(A)\leq2$ (A només té 2 columnes), així que $|AB|=0$ i <strong>$AB$ no té inversa per a cap $b$</strong>. En canvi, $BA$ és $2\times2$: $$BA=\begin{pmatrix}-1&0&2\\-1&b&-1\end{pmatrix}\begin{pmatrix}1&2\\b&0\\-1&2\end{pmatrix}=\begin{pmatrix}-3&2\\b^2&-4\end{pmatrix},\qquad |BA|=12-2b^2$$ $BA$ té inversa si $b^2\neq6$, és a dir, $b\neq\pm\sqrt6$.",
    r"<strong>Apartat b).</strong> $$A^TA=\begin{pmatrix}1&b&-1\\2&0&2\end{pmatrix}\begin{pmatrix}1&2\\b&0\\-1&2\end{pmatrix}=\begin{pmatrix}b^2+2&0\\0&8\end{pmatrix},\qquad |A^TA|=8(b^2+2)>0$$ Té inversa per a tot $b\in\mathbb{R}$.",
    r"<strong>Apartat c).</strong> És diagonal, així que la inversa s'obté invertint els elements de la diagonal: $$(A^TA)^{-1}=\begin{pmatrix}\frac1{b^2+2}&0\\0&\frac18\end{pmatrix}$$",
) + res(r"a) $AB$ mai; $BA$ si $b\neq\pm\sqrt6$. &nbsp; b) Per a tot $b$. &nbsp; c) $\begin{pmatrix}\frac1{b^2+2}&0\\0&\frac18\end{pmatrix}$."))

# ---------------- Juny 2021 (1) ----------------
A = M([-1, 2, 1], [0, 1, 0], [2, 1, 2]); ih, Ai = inv_html(A); assert mul(Ai, A) == I(3)
sol("M", "Juny 2021", 1, steps(
    r"<strong>Apartat a).</strong> Desenvolupem per la segona fila: $$|A|=m\begin{vmatrix}-1&m\\2&m^2+1\end{vmatrix}=m(-m^2-1-2m)=-m(m+1)^2$$ Si $m\neq0,-1$: $\operatorname{rg}(A)=3$. Si $m=0$: $A=\begin{pmatrix}-1&2&0\\0&0&0\\2&1&1\end{pmatrix}$, amb $\begin{vmatrix}-1&2\\2&1\end{vmatrix}=-5\neq0$: $\operatorname{rg}(A)=2$. Si $m=-1$: $A=\begin{pmatrix}-1&2&-1\\0&-1&0\\2&1&2\end{pmatrix}$, amb $\begin{vmatrix}-1&2\\0&-1\end{vmatrix}=1\neq0$: $\operatorname{rg}(A)=2$.",
    r"<strong>Apartat b).</strong> $A$ és invertible si $|A|\neq0$, és a dir, si $m\neq0$ i $m\neq-1$.",
    r"<strong>Apartat c).</strong> $XA=I\Rightarrow X=A^{-1}$. Per a $m=1$:" + ih,
) + res(r"a) $\operatorname{rg}A=3$ si $m\neq0,-1$; $\operatorname{rg}A=2$ si $m=0$ o $m=-1$. &nbsp; b) $m\neq0,-1$. &nbsp; c) $X=%s$." % nice(Ai)))

# ---------------- Juny 2022 (1) ----------------
A = M([1, 0, 1], [-1, 2, -1]); B = M([1, 1, 1], [0, 1, 0]); C = M([1, 1], [0, -1])
ABt = mul(A, T(B)); D = sub(C, ABt); ih, Di = inv_html(D, "(C-AB^t)")
assert ABt == sc(2, I(2)) and mul(C, Di) == add(mul(ABt, Di), I(2))
sol("M", "Juny 2022", 1, steps(
    r"<strong>Apartat a).</strong> $$AB^t=%s%s=%s=2I,\qquad C-AB^t=%s$$" % (tx(A), tx(T(B)), tx(ABt), tx(D)) + ih,
    r"<strong>Apartat b).</strong> $$CX=AB^tX+I\Rightarrow CX-AB^tX=I\Rightarrow(C-AB^t)X=I\Rightarrow X=(C-AB^t)^{-1}=%s$$" % nice(Di),
    r"<strong>Apartat c).</strong> Com que $AB^t=2I$ i $I^n=I$: $(AB^t)^n=(2I)^n=2^nI^n=2^nI$ per a tot $n\in\mathbb{N}$.",
) + res(r"a) $(C-AB^t)^{-1}=%s$. &nbsp; b) $X=%s$. &nbsp; c) $AB^t=2I$." % (nice(Di), nice(Di))))

# ---------------- Juny 2022 (2) ----------------
A = M([2, 0, 1], [-4, 4, 1], [0, 4, 1]); ih, Ai = inv_html(A)
assert det(M([1, 0, 0], [-2, 1, 1], [0, 2, 1])) == -1
sol("M", "Juny 2022", 2, steps(
    r"<strong>Apartat a).</strong> $$|A|=m(m^2-2m)+(m-1)(-4m^2)=-3m^3+2m^2=-m^2(3m-2)$$ Si $m\neq0$ i $m\neq\frac23$: $\operatorname{rg}(A)=3$. Si $m=0$: $A=\begin{pmatrix}0&0&-1\\0&0&1\\0&0&1\end{pmatrix}$, totes les files proporcionals: $\operatorname{rg}(A)=1$. Si $m=\frac23$: $A=\begin{pmatrix}\frac23&0&-\frac13\\-\frac43&\frac49&1\\0&\frac43&1\end{pmatrix}$ i $\begin{vmatrix}\frac23&0\\-\frac43&\frac49\end{vmatrix}=\frac{8}{27}\neq0$: $\operatorname{rg}(A)=2$.",
    r"<strong>Apartat b) $m=2$.</strong> $A=%s$." % tx(A) + ih,
    r"<strong>Apartat c).</strong> $|2A|=2^3|A|=-8\Rightarrow|A|=-1$: $$-3m^3+2m^2=-1\Rightarrow3m^3-2m^2-1=0\Rightarrow(m-1)(3m^2+m+1)=0$$ El factor de segon grau no té arrels reals (discriminant $1-12<0$), així que $m=1$.",
) + res(r"a) $\operatorname{rg}A=3$ si $m\neq0,\frac23$; $2$ si $m=\frac23$; $1$ si $m=0$. &nbsp; b) $A^{-1}=%s$. &nbsp; c) $m=1$." % nice(Ai)))

# ---------------- Juliol 2022 (1) ----------------
A = M([1, 1], [0, 1]); assert inv(A) == M([1, -1], [0, 1]) and pw(A, 3) == M([1, 3], [0, 1]) and pw(A, 4) == M([1, 4], [0, 1])
sol("M", "Juliol 2022", 1, steps(
    r"<strong>Apartat a).</strong> Si $A^{-1}=\begin{pmatrix}1&-1\\0&1\end{pmatrix}$, llavors $A$ és la inversa d'aquesta matriu: $$A=\begin{pmatrix}1&-1\\0&1\end{pmatrix}^{-1}=\begin{pmatrix}1&1\\0&1\end{pmatrix}$$ Igualant: $a+b=1$ i $a-b=1$, d'on $a=1$, $b=0$.",
    r"<strong>Apartat b).</strong> $$A^2=\begin{pmatrix}1&2\\0&1\end{pmatrix},\qquad A^3=A^2A=\begin{pmatrix}1&3\\0&1\end{pmatrix},\qquad A^4=A^3A=\begin{pmatrix}1&4\\0&1\end{pmatrix}$$",
    r"<strong>Apartat c).</strong> $|A|=(a+b)(a-b)=a^2-b^2\neq0$, així que $A$ és invertible i $$\det(A^{-50})=\frac{1}{|A|^{50}}=\frac{1}{(a^2-b^2)^{50}}$$",
) + res(r"a) $a=1$, $b=0$. &nbsp; b) $A^3=\begin{pmatrix}1&3\\0&1\end{pmatrix}$, $A^4=\begin{pmatrix}1&4\\0&1\end{pmatrix}$. &nbsp; c) $(a^2-b^2)^{-50}$."))

# ---------------- Juny 2023 (1) ----------------
for m_ in (0, 1, 2, -3):
    A = M([1, 2, 0], [0, m_, 1], [0, 3, 0]); X = M([3 * m_ - 6], [-m_], [m_ * m_ + 3])
    assert det(A) == -3 and mul(A, A, X) == M([m_], [0], [9])
sol("M", "Juny 2023", 1, steps(
    r"<strong>Apartat a).</strong> Desenvolupem per la primera columna: $|A|=1\cdot\begin{vmatrix}m&1\\3&0\end{vmatrix}=-3\neq0$ per a tot $m$. Per tant $|A^2|=|A|^2=9\neq0$: $A^2$ sempre és invertible i l'equació $A^2X=B$ té <strong>sempre una única solució</strong>, $X=(A^2)^{-1}B$.",
    r"<strong>Apartat b).</strong> Escrivim $A^2X=A(AX)$ i anomenem $Y=AX$. Primer resolem $AY=B$: $$%s\Rightarrow y_2=3,\ y_1=m-6,\ y_3=-3m$$ Ara resolem $AX=Y$: $$%s\Rightarrow x_2=-m,\ x_1=m-6+2m=3m-6,\ x_3=3+m^2$$" % (sysm("y_1+2y_2&=m", "my_2+y_3&=0", "3y_2&=9"), sysm("x_1+2x_2&=m-6", "mx_2+x_3&=3", "3x_2&=-3m")),
) + res(r"a) Sempre té solució (única). &nbsp; b) $X=\begin{pmatrix}3m-6\\-m\\m^2+3\end{pmatrix}$."))

# ---------------- Juny 2023 (2) ----------------
A = M([1, 0, 1], [0, 1, 1]); B = M([1, 1, 1], [2, -1, 0]); P = add(mul(A, T(B)), I(2)); ih, Pi = inv_html(P, "(AB^t+I)")
sol("M", "Juny 2023", 2, steps(
    r"<strong>Apartat a).</strong> $A$ és $2\times3$ i $B^t$ és $3\times2$, així que $AB^t$ és $2\times2$ i $I$ és la identitat d'ordre 2: $$AB^t=%s%s=%s,\qquad AB^t+I=%s$$" % (tx(A), tx(T(B)), tx(mul(A, T(B))), tx(P)) + ih,
    r"<strong>Apartat b).</strong> $$C^2=\begin{pmatrix}0&\alpha\\-\alpha^2&0\end{pmatrix}\begin{pmatrix}0&\alpha\\-\alpha^2&0\end{pmatrix}=\begin{pmatrix}-\alpha^3&0\\0&-\alpha^3\end{pmatrix}=-\alpha^3I$$ $$C^{13}=(C^2)^6C=(-\alpha^3)^6I\,C=\alpha^{18}C=\begin{pmatrix}0&\alpha^{19}\\-\alpha^{20}&0\end{pmatrix}$$",
) + res(r"a) $(AB^t+I)^{-1}=%s$. &nbsp; b) $C^{13}=\alpha^{18}C$." % nice(Pi)))

# ---------------- Juny 2024 (1) ----------------
A = M([1, -2, -1], [0, -1, 0], [-1, 1, -1]); Bm = M([1, 0], [0, 1], [0, 0]); ih, Ai = inv_html(A); X = mul(Ai, Bm); assert mul(A, X) == Bm
A0 = M([1, 0, 0], [0, 0, 0], [0, 1, 0]); assert pw(A0, 5) == M([1, 0, 0], [0, 0, 0], [0, 0, 0])
sol("M", "Juny 2024", 1, steps(
    r"<strong>Apartat a).</strong> Desenvolupem per la segona fila: $$|A|=m\begin{vmatrix}1&m\\m&m\end{vmatrix}=m(m-m^2)=m^2(1-m)$$ Si $m\neq0,1$: $\operatorname{rg}(A)=3$. Si $m=0$: $A=\begin{pmatrix}1&0&0\\0&0&0\\0&1&0\end{pmatrix}$, amb $\begin{vmatrix}1&0\\0&1\end{vmatrix}=1\neq0$ (files 1 i 3, columnes 1 i 2): $\operatorname{rg}(A)=2$. Si $m=1$: $A=\begin{pmatrix}1&2&1\\0&1&0\\1&1&1\end{pmatrix}$, amb $\begin{vmatrix}1&2\\0&1\end{vmatrix}=1\neq0$: $\operatorname{rg}(A)=2$.",
    r"<strong>Apartat b) $m=-1$.</strong> $A=%s$, $|A|=2\neq0$, i $X=A^{-1}B$ (de dimensió $3\times2$):" % tx(A) + ih + r"$$X=A^{-1}B=%s%s=%s$$" % (nice(Ai), tx(Bm), nice(X)),
    r"<strong>Apartat c) $m=0$.</strong> $$A^2=%s,\qquad A^3=A^2A=%s=A^2$$ Per tant $A^n=A^2$ per a tot $n\geq2$, i $A^5=%s$." % (tx(mul(A0, A0)), tx(pw(A0, 3)), tx(pw(A0, 5))),
) + res(r"a) $\operatorname{rg}A=3$ si $m\neq0,1$; $2$ si $m=0$ o $m=1$. &nbsp; b) $X=%s$. &nbsp; c) $A^5=%s$." % (nice(X), tx(pw(A0, 5)))))

# ---------------- Juliol 2024 (1) ----------------
A = M([0, 0, 3], [0, Fr(1, 3), 1], [2, -1, -1]); ih, Ai = inv_html(A)
sol("M", "Juliol 2024", 1, steps(
    r"<strong>Apartat a).</strong> $$|A|=0-k\left(-k-2\right)+3\left(-k-\tfrac23\right)=k^2+2k-3k-2=k^2-k-2=(k-2)(k+1)$$ $A$ és invertible si $k\neq2$ i $k\neq-1$.",
    r"<strong>Apartat b) $k=0$.</strong> $|A|=-2\neq0$, així que existeix:" + ih,
    r"<strong>Apartat c).</strong> Siga $D=\begin{pmatrix}d_1&0&0\\0&d_2&0\\0&0&d_3\end{pmatrix}$. L'element $(i,j)$ de $AD$ és $a_{ij}d_j$ i el de $DA$ és $d_ia_{ij}$. Per tant cal $a_{ij}(d_j-d_i)=0$. Com que $a_{13}=3\neq0$, $d_1=d_3$; com que $a_{23}=1\neq0$, $d_2=d_3$. Així doncs $d_1=d_2=d_3$.",
) + res(r"a) $k\neq2,-1$. &nbsp; b) $A^{-1}=%s$. &nbsp; c) $D=dI=\begin{pmatrix}d&0&0\\0&d&0\\0&0&d\end{pmatrix}$, $d\in\mathbb{R}$." % nice(Ai)))
for d_ in ((1, 1, 1), (1, 2, 1)):
    D = M(*[[d_[i] if i == j else 0 for j in range(3)] for i in range(3)])
    assert (mul(A, D) == mul(D, A)) == (d_ == (1, 1, 1))

# ---------------- Juliol 2024 (2) ----------------
for a_ in (0, 1, 5):
    A = M([1, 0, 2], [3, 2, 1], [a_, 0, 3])
    assert det(A) == 6 - 4 * a_ and mul(A, A, M([3], [-2], [-1])) == M([6 * a_ - 5], [3 * a_ + 8], [10 * a_ - 9])
sol("M", "Juliol 2024", 2, steps(
    r"<strong>Apartat a).</strong> Desenvolupem per la segona columna: $$|A|=2\begin{vmatrix}1&2\\a&3\end{vmatrix}=2(3-2a)$$ L'equació $A^2X=B$ té solució única si $A^2$ és invertible, és a dir, si $|A^2|=|A|^2\neq0$: $a\neq\frac32$.",
    r"<strong>Apartat b).</strong> $B=A^2\begin{pmatrix}3\\-2\\-1\end{pmatrix}=A\left[A\begin{pmatrix}3\\-2\\-1\end{pmatrix}\right]$: $$A\begin{pmatrix}3\\-2\\-1\end{pmatrix}=\begin{pmatrix}3-2\\9-4-1\\3a-3\end{pmatrix}=\begin{pmatrix}1\\4\\3a-3\end{pmatrix},\qquad A\begin{pmatrix}1\\4\\3a-3\end{pmatrix}=\begin{pmatrix}1+6a-6\\3+8+3a-3\\a+9a-9\end{pmatrix}=\begin{pmatrix}6a-5\\3a+8\\10a-9\end{pmatrix}$$",
) + res(r"a) $a\neq\frac32$. &nbsp; b) $\alpha=6a-5$, $\beta=3a+8$, $\gamma=10a-9$."))

# ---------------- Juny 2025 (1) ----------------
for a_ in (Fr(2), Fr(3), Fr(-1, 2)):
    A = M([1, a_, 0], [0, a_, 0], [0, 0, 1 - a_])
    assert inv(A) == M([1, -1, 0], [0, 1 / a_, 0], [0, 0, 1 / (1 - a_)])
A0 = M([1, 0, 0], [0, 0, 0], [0, 0, 1]); assert mul(A0, A0) == A0
sol("M", "Juny 2025", 1, steps(
    r"<strong>Apartat a).</strong> $$A^2=\begin{pmatrix}1&a&0\\0&a&0\\0&0&1-a\end{pmatrix}^2=\begin{pmatrix}1&a+a^2&0\\0&a^2&0\\0&0&(1-a)^2\end{pmatrix}$$ $A^2=A$ exigeix $a+a^2=a$, $a^2=a$ i $(1-a)^2=1-a$. De la primera, $a^2=0$, és a dir, $a=0$, que també compleix les altres dues. Per tant $a=0$.",
    r"<strong>Apartat b).</strong> $A$ és triangular: $|A|=1\cdot a\cdot(1-a)$. Existeix la inversa si $a\neq0$ i $a\neq1$. Calculem-la (per adjunts o resolent $AA^{-1}=I$): $$A^{-1}=\begin{pmatrix}1&-1&0\\0&\frac1a&0\\0&0&\frac1{1-a}\end{pmatrix}$$ Comprovació: $AA^{-1}=\begin{pmatrix}1&-1+a\cdot\frac1a&0\\0&1&0\\0&0&1\end{pmatrix}=I$ ✓.",
) + res(r"a) $a=0$. &nbsp; b) $a\neq0,1$; $A^{-1}=\begin{pmatrix}1&-1&0\\0&\frac1a&0\\0&0&\frac1{1-a}\end{pmatrix}$."))

# ---------------- Juny 2025 (2) ----------------
for m_ in (0, 1, 4):
    A = M([2, 3], [1, m_]); B = M([-1, 2], [1, 5]); C = M([0, -1], [5, m_ * m_])
    X = sc(Fr(1, 7), M([41 - 2 * m_, 15 * m_ + 29], [-m_ - 4, -3 * m_ - 10])); assert add(mul(B, X), mul(A, A)) == C
B = M([-1, 2], [1, 5]); ihB, Bi = inv_html(B, "B")
sol("M", "Juny 2025", 2, steps(
    r"<strong>Apartat a).</strong> $$AB=\begin{pmatrix}2&3\\1&m\end{pmatrix}\begin{pmatrix}-1&2\\1&5\end{pmatrix}=\begin{pmatrix}1&19\\m-1&5m+2\end{pmatrix},\qquad (AB)^t=\begin{pmatrix}1&m-1\\19&5m+2\end{pmatrix}$$",
    r"<strong>Apartat b).</strong> $|A|=2m-3$. Si $m\neq\frac32$: $$A^{-1}=\frac{1}{2m-3}\begin{pmatrix}m&-3\\-1&2\end{pmatrix}$$",
    r"<strong>Apartat c).</strong> $BX=C-A^2\Rightarrow X=B^{-1}(C-A^2)$. $$A^2=\begin{pmatrix}7&3m+6\\m+2&m^2+3\end{pmatrix},\qquad C-A^2=\begin{pmatrix}-7&-3m-7\\3-m&-3\end{pmatrix}$$" + ihB + r"$$X=-\frac17\begin{pmatrix}5&-2\\-1&-1\end{pmatrix}\begin{pmatrix}-7&-3m-7\\3-m&-3\end{pmatrix}=\frac17\begin{pmatrix}41-2m&15m+29\\-m-4&-3m-10\end{pmatrix}$$",
) + res(r"a) $AB=\begin{pmatrix}1&19\\m-1&5m+2\end{pmatrix}$. &nbsp; b) $A^{-1}=\frac{1}{2m-3}\begin{pmatrix}m&-3\\-1&2\end{pmatrix}$ ($m\neq\frac32$). &nbsp; c) $X=\frac17\begin{pmatrix}41-2m&15m+29\\-m-4&-3m-10\end{pmatrix}$."))

# ---------------- Juliol 2025 (1) ----------------
A = M([-2, 1], [3, -2]); B = M([1, 2], [0, -1]); C = M([3, -1], [-3, 3])
assert mul(B, B) == I(2) and det(A) == 1 and det(B) == -1 and add(A, C) == I(2)
assert inv(mul(inv(A), A)) == mul(A, inv(mul(B, B, A)))
sol("M", "Juliol 2025", 1, steps(
    r"<strong>Observació clau.</strong> $$B^2=\begin{pmatrix}1&2\\0&-1\end{pmatrix}\begin{pmatrix}1&2\\0&-1\end{pmatrix}=\begin{pmatrix}1&0\\0&1\end{pmatrix}=I$$",
    r"<strong>Apartat a).</strong> $$A(B^2A)^{-1}=A(IA)^{-1}=AA^{-1}=I$$ Per tant $(A^{-1}X)^{-1}=I\Rightarrow A^{-1}X=I\Rightarrow X=A=%s$." % tx(A),
    r"<strong>Apartat b).</strong> $|A|=4-3=1$, $|B|=-1$, i són d'ordre 2: $$|3A^5B|=3^2|A|^5|B|=9\cdot1\cdot(-1)=-9,\qquad |(3A^5B)^2|=(-9)^2=81$$",
    r"<strong>Apartat c).</strong> Com que $B^2=I$: $B^{100}=(B^2)^{50}=I$ i $B^{99}=B^{98}B=B$. A més, $A+C=%s=I$. L'equació queda $$aI+bB=I\iff\begin{pmatrix}a+b&2b\\0&a-b\end{pmatrix}=\begin{pmatrix}1&0\\0&1\end{pmatrix}\iff b=0,\ a=1$$" % tx(add(A, C)),
) + res(r"a) $X=A=%s$. &nbsp; b) $81$. &nbsp; c) $a=1$, $b=0$." % tx(A)))

# ---------------- Juliol 2025 (2) ----------------
A = M([Fr(1, 2), 1], [0, Fr(-1, 2)]); B = M([2, 1], [1, 1]); D = sub(sc(2, A), B); ih, Di = inv_html(D, "(2A-B)")
assert mul(A, A) == sc(Fr(1, 4), I(2)) and pw(A, 12) == sc(Fr(1, 4096), I(2))
assert mul(sc(2, A), Di) == add(mul(B, Di), I(2))
sol("M", "Juliol 2025", 2, steps(
    r"<strong>Apartat a).</strong> $$2AX=BX+I\Rightarrow(2A-B)X=I\Rightarrow X=(2A-B)^{-1},\qquad 2A-B=%s-%s=%s$$" % (tx(sc(2, A)), tx(B), tx(D)) + ih,
    r"<strong>Apartat b).</strong> $$A^2=\begin{pmatrix}\frac12&1\\0&-\frac12\end{pmatrix}\begin{pmatrix}\frac12&1\\0&-\frac12\end{pmatrix}=\begin{pmatrix}\frac14&0\\0&\frac14\end{pmatrix}=\tfrac14I$$ Llavors $4A^2+\alpha A-I=I+\alpha A-I=\alpha A=0$, i com que $A\neq0$, $\alpha=0$.",
    r"<strong>Apartat c).</strong> $$A^{12}=(A^2)^6=\left(\tfrac14\right)^6I=\frac{1}{4096}I$$",
) + res(r"a) $X=%s$. &nbsp; b) $\alpha=0$. &nbsp; c) $A^{12}=\frac{1}{4096}I$." % nice(Di)))

# ---------------- Juny 2026 (1) ----------------
P = M([1, 0], [0, 1], [1, 1]); Q = M([2, 1], [0, 2], [1, 0])
for a_ in (1, -1):
    for b_ in (1, -1):
        Bm = M([0, 0, a_], [0, 1, 0], [b_, 0, 0]); X = mul(T(Bm), sub(Q, P))
        assert mul(Bm, T(Bm)) == I(3) and add(mul(Bm, X), P) == Q and X == M([0, -b_], [0, 1], [a_, a_])
sol("M", "Juny 2026", 1, steps(
    r"<strong>Apartat a).</strong> $$AA^t=\begin{pmatrix}\cos\alpha&\sin\alpha\\-\sin\alpha&\cos\alpha\end{pmatrix}\begin{pmatrix}\cos\alpha&-\sin\alpha\\\sin\alpha&\cos\alpha\end{pmatrix}=\begin{pmatrix}\cos^2\alpha+\sin^2\alpha&0\\0&\sin^2\alpha+\cos^2\alpha\end{pmatrix}=I$$ Per tant $A^{-1}=A^t$ per a tot $\alpha$: $A$ és ortogonal.",
    r"<strong>Apartat b).</strong> $$BB^t=\begin{pmatrix}0&0&a\\0&1&0\\b&0&0\end{pmatrix}\begin{pmatrix}0&0&b\\0&1&0\\a&0&0\end{pmatrix}=\begin{pmatrix}a^2&0&0\\0&1&0\\0&0&b^2\end{pmatrix}=I\iff a^2=1,\ b^2=1$$ Per tant $a=\pm1$ i $b=\pm1$: hi ha <strong>4 matrius</strong> ortogonals d'aquesta forma.",
    r"<strong>Apartat c).</strong> $$BX=\begin{pmatrix}2&1\\0&2\\1&0\end{pmatrix}-\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix}=\begin{pmatrix}1&1\\0&1\\0&-1\end{pmatrix}\Rightarrow X=B^{-1}\begin{pmatrix}1&1\\0&1\\0&-1\end{pmatrix}=B^t\begin{pmatrix}1&1\\0&1\\0&-1\end{pmatrix}$$ $$X=\begin{pmatrix}0&0&b\\0&1&0\\a&0&0\end{pmatrix}\begin{pmatrix}1&1\\0&1\\0&-1\end{pmatrix}=\begin{pmatrix}0&-b\\0&1\\a&a\end{pmatrix}$$ amb $a,b\in\{1,-1\}$ els valors de la matriu $B$ triada.",
) + res(r"a) $AA^t=I$. &nbsp; b) $a=\pm1$, $b=\pm1$: 4 matrius. &nbsp; c) $X=\begin{pmatrix}0&-b\\0&1\\a&a\end{pmatrix}$."))

# ---------------- Juny 2026 extra (1) ----------------
for a_ in (1, -1):
    A = M([1 - a_, 1], [1, 1 + a_]); assert sub(mul(A, A), I(2)) == sc(2, A)
for a_ in (Fr(2), Fr(-3), Fr(1, 2)):
    A = M([1 - a_, 1], [1, 1 + a_]); assert det(A) == -a_ * a_ and inv(A) == sc(1 / (a_ * a_), M([-1 - a_, 1], [1, a_ - 1]))
sol("M", "Juny 2026 extra", 1, steps(
    r"<strong>Apartat a).</strong> $$A^2=\begin{pmatrix}(1-a)^2+1&2\\2&1+(1+a)^2\end{pmatrix},\qquad A^2-I=\begin{pmatrix}(1-a)^2&2\\2&(1+a)^2\end{pmatrix},\qquad 2A=\begin{pmatrix}2-2a&2\\2&2+2a\end{pmatrix}$$ Igualant: $(1-a)^2=2-2a\iff a^2-2a+1=2-2a\iff a^2=1$, i $(1+a)^2=2+2a\iff a^2=1$. El risc s'optimitza per a $a=1$ i $a=-1$.",
    r"<strong>Apartat b).</strong> $|A|=(1-a)(1+a)-1=-a^2$. Té inversa si $a\neq0$: $$A^{-1}=\frac{1}{-a^2}\begin{pmatrix}1+a&-1\\-1&1-a\end{pmatrix}=\frac{1}{a^2}\begin{pmatrix}-1-a&1\\1&a-1\end{pmatrix}$$",
) + res(r"a) $a=\pm1$. &nbsp; b) $a\neq0$; $A^{-1}=\frac{1}{a^2}\begin{pmatrix}-1-a&1\\1&a-1\end{pmatrix}$."))
