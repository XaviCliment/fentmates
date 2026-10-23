# Solucions dels exercicis de sistemes (S). S'executa dins de sol_mii.py.
# ruff: noqa
L = r"\lambda"

# ---------------- Juny 1997 (1) ----------------
sol("S", "Juny 1997", 1, steps(
    dsc([[L, "1", "0"], [L, "0", "1"], [L, "2", "1"]], r"\lambda\begin{vmatrix}0&1\\2&1\end{vmatrix}-\lambda\begin{vmatrix}1&0\\2&1\end{vmatrix}+\lambda\begin{vmatrix}1&0\\0&1\end{vmatrix}=-2\lambda-\lambda+\lambda=-2\lambda", ["0"]),
    cdcase(["0"]) + r" Per Cramer: $$x=\frac{\begin{vmatrix}1&1&0\\1&0&1\\1&2&1\end{vmatrix}}{-2\lambda}=\frac{-2}{-2\lambda}=\frac1\lambda,\qquad y=\frac{\begin{vmatrix}\lambda&1&0\\\lambda&1&1\\\lambda&1&1\end{vmatrix}}{-2\lambda}=0,\qquad z=\frac{\begin{vmatrix}\lambda&1&1\\\lambda&0&1\\\lambda&2&1\end{vmatrix}}{-2\lambda}=0$$ (en $|A_y|$ hi ha dues files iguals; en $|A_z|$ la primera i la tercera columna són proporcionals).",
    crit(L, "0", [[0, 1, 0, 1], [0, 0, 1, 1], [0, 2, 1, 1]]),
    "<strong>Conclusió.</strong> El sistema no és compatible indeterminat per a cap valor de $\\lambda$, així que no hi ha cap cas d'aquest tipus per resoldre.",
) + res(r"Si $\lambda\neq0$: compatible determinat, $(x,y,z)=\left(\frac1\lambda,0,0\right)$. Si $\lambda=0$: incompatible. No hi ha cap valor que el faça compatible indeterminat."))

# ---------------- Juny 1997 (2) ----------------
A = M([2, 3], [1, -1]); ih, Ai = inv_html(A)
assert mul(A, [[Fr(1, 5)], [Fr(1, 5)]]) == [[1], [0]] and mul(A, [[Fr(3, 5)], [Fr(-2, 5)]]) == [[0], [1]]
sol("S", "Juny 1997", 2, steps(
    "<strong>Primer sistema.</strong> De $x-y=0$ tenim $y=x$; substituint, $2x+3x=1\\Rightarrow x=\\frac15$. Solució: $x=y=\\frac15$.",
    "<strong>Segon sistema.</strong> De $x-y=1$ tenim $x=1+y$; substituint, $2+2y+3y=0\\Rightarrow y=-\\frac25$, $x=\\frac35$.",
    "<strong>Inversa de la matriu de coeficients.</strong>" + ih,
    r"<strong>Relació.</strong> Les solucions són les columnes de $A^{-1}$. És lògic: els sistemes són $AX=\begin{pmatrix}1\\0\end{pmatrix}$ i $AX=\begin{pmatrix}0\\1\end{pmatrix}$, i per tant $X=A^{-1}\begin{pmatrix}1\\0\end{pmatrix}$ (primera columna de $A^{-1}$) i $X=A^{-1}\begin{pmatrix}0\\1\end{pmatrix}$ (segona columna).",
) + res(r"$\left(\frac15,\frac15\right)$ i $\left(\frac35,-\frac25\right)$, que són la 1a i la 2a columna de $A^{-1}=%s$." % nice(Ai)))

# ---------------- Setembre 1997 (1) ----------------
A = M([2, 1], [1, -1]); ih, Ai = inv_html(A)
assert Ai == M([Fr(1, 3), Fr(1, 3)], [Fr(1, 3), Fr(-2, 3)])
sol("S", "Setembre 1997", 1, steps(
    "<strong>Primer sistema.</strong> $y=x$ i $2x+x=1\\Rightarrow x=y=\\frac13$.",
    "<strong>Segon sistema.</strong> $x=1+y$ i $2+2y+y=0\\Rightarrow y=-\\frac23$, $x=\\frac13$.",
    "<strong>Forma matricial.</strong> Els tres sistemes són $AX=B$ amb $A=" + tx(A) + r"$. Com que $|A|=-3\neq0$, $X=A^{-1}B$:" + ih,
    r"<strong>Relació.</strong> $$\begin{pmatrix}x\\y\end{pmatrix}=A^{-1}\begin{pmatrix}a\\b\end{pmatrix}=a\begin{pmatrix}1/3\\1/3\end{pmatrix}+b\begin{pmatrix}1/3\\-2/3\end{pmatrix}$$ És a dir, la solució del sistema general és $a$ vegades la solució del primer sistema més $b$ vegades la del segon (que són les columnes de $A^{-1}$).",
    r"<strong>Comprovació.</strong> $x=\frac{a+b}3$, $y=\frac{a-2b}3$: $2x+y=\frac{2a+2b+a-2b}3=a$ ✓ i $x-y=\frac{3b}3=b$ ✓.",
) + res(r"$\left(\frac13,\frac13\right)$, $\left(\frac13,-\frac23\right)$ i, en general, $(x,y)=a\left(\frac13,\frac13\right)+b\left(\frac13,-\frac23\right)=\left(\frac{a+b}3,\frac{a-2b}3\right)$."))

# ---------------- Setembre 1997 (2) ----------------
sol("S", "Setembre 1997", 2, steps(
    dsc([["1", "-1", L], ["1", L, "-1"], ["0", "1", L]], r"(\lambda^2+1)+(\lambda-0)+\lambda(1-0)=\lambda^2+2\lambda+1=(\lambda+1)^2", ["-1"]),
    cdcase(["-1"]),
    r"<strong>Cas $\lambda=-1$.</strong> $$A^*=\left(\begin{array}{ccc|c}1&-1&-1&-1\\1&-1&-1&-1\\0&1&-1&-1\end{array}\right)$$ Les dues primeres files són iguals. El menor $\begin{vmatrix}1&-1\\0&1\end{vmatrix}=1\neq0$, així que $%s(A)=2$, i com que $A^*$ només té dues files diferents, $%s(A^*)=2$. Sistema %s." % (RG, RG, CI),
) + res(r"Si $\lambda\neq-1$: compatible determinat. Si $\lambda=-1$: compatible indeterminat ($\operatorname{rg}A=\operatorname{rg}A^*=2$). No és incompatible per a cap valor."))

# ---------------- Juny 1998 (1) ----------------
h, s_ = G([[1, 1, 1, 3], [2, -1, 0, 1], [-1, 2, 1, 2]])
sol("S", "Juny 1998", 1, steps(
    "<strong>Resolem per Gauss.</strong>" + h,
    "<strong>Comparem amb el sistema de dues equacions.</strong> Observem que la tercera equació és la primera menys la segona: $(x+y+z)-(2x-y)=-x+2y+z$ i $3-1=2$. Per tant la tercera equació no aporta cap condició nova i els dos sistemes tenen <strong>les mateixes solucions</strong> (els dos tenen rang 2 i són equivalents).",
) + res(r"Compatible indeterminat: $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. Sí que té les mateixes solucions que el sistema de dues equacions, perquè $E_3=E_1-E_2$." % tuple(s_)))

# ---------------- Juny 1998 (2) ----------------
A = M([1, -1], [1, 1]); ih, Ai = inv_html(A)
X = mul(Ai, M([2], [3])); assert X == M([Fr(5, 2)], [Fr(1, 2)])
sol("S", "Juny 1998", 2, steps(
    "<strong>Apartat a) Inversa.</strong> La matriu de coeficients és $A=" + tx(A) + "$." + ih,
    r"<strong>Resolem.</strong> $$AX=\begin{pmatrix}2\\3\end{pmatrix}\Rightarrow X=A^{-1}\begin{pmatrix}2\\3\end{pmatrix}=%s\begin{pmatrix}2\\3\end{pmatrix}=%s$$" % (nice(Ai), tx(X)),
    r"<strong>Apartat b).</strong> Traiem $A$ factor comú per l'esquerra: $$A^2+7A=I\Rightarrow A(A+7I)=I$$ Per definició d'inversa (i també $(A+7I)A=A^2+7A=I$), $A$ és invertible i $A^{-1}=A+7I$.",
) + res(r"a) $A^{-1}=%s$, $x=\frac52$, $y=\frac12$. &nbsp; b) $A^{-1}=A+7I$." % nice(Ai)))

# ---------------- Setembre 1998 (1) ----------------
h, s_ = G([[1, 1, 1, 0], [2, 1, 3, 0], [1, 0, 2, 0]])
sol("S", "Setembre 1998", 1, steps(
    "<strong>Sistema homogeni.</strong> Sempre té la solució trivial $(0,0,0)$. Té altres solucions si i només si és compatible indeterminat, és a dir, si $|A|=0$.",
    dsc([["1", "1", "1"], ["2", "1", "3"], ["1", "0", "a"]], "(a-0)-(2a-3)+(0-1)=2-a", ["2"], "a"),
    "<strong>Cas $a=2$.</strong>" + h,
    "<strong>Interpretació.</strong> Els tres plans passen per l'origen (són homogenis) i, com que el rang és 2 i cap parell de plans és paral·lel, es tallen en una mateixa <strong>recta</strong> que passa per l'origen (formen un feix de plans).",
) + res(r"$a=2$. Solucions: $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$: la recta comuna als tres plans." % tuple(s_)))

# ---------------- Setembre 1998 (2) ----------------
P = M([-3, -6, 4], [Fr(9, 2), 8, Fr(-11, 2)], [-1, -1, 1]); A = M([5, 4, 2], [2, 2, 3], [7, 6, 6])
assert mul(P, A) == I(3)
X = mul(P, M([2], [3], [5])); assert mul(A, X) == M([2], [3], [5])
sol("S", "Setembre 1998", 2, steps(
    r"<strong>Producte.</strong> $$%s\cdot%s=%s=I$$ Per tant, la primera matriu és la inversa de la segona: $P=A^{-1}$." % (mt([["-3", "-6", "4"], [r"\frac92", "8", r"-\frac{11}2"], ["-1", "-1", "1"]]), tx(A), tx(I(3))),
    r"<strong>Resolem el sistema.</strong> La matriu de coeficients és precisament $A$, així que $$AX=\begin{pmatrix}2\\3\\5\end{pmatrix}\Rightarrow X=A^{-1}\begin{pmatrix}2\\3\\5\end{pmatrix}=P\begin{pmatrix}2\\3\\5\end{pmatrix}=%s$$" % tx(X),
) + res(r"El producte és $I$; la solució és $x=%s,\ y=%s,\ z=%s$." % tuple(ft(r[0]) for r in X)))

# ---------------- Juny 1999 (1) ----------------
sol("S", "Juny 1999", 1, steps(
    dsc([["1", "2", "1"], ["1", "3", "2"], ["1", "m", "3"]], "(9-2m)-2(3-2)+(m-3)=4-m", ["4"], "m"),
    cdcase(["4"], "m") + r" (La solució és $(1,0,2)$ per a tot $m\neq4$: $1+0+2=3$, $1+0+4=5$, $1+0+6=7$ ✓.)",
    crit("m", "4", [[1, 2, 1, 3], [1, 3, 2, 5], [1, 4, 3, 7]]),
    "<strong>No hi ha cap valor incompatible.</strong> Si $m\\neq4$ és compatible determinat i si $m=4$ és compatible indeterminat, així que sempre té solució.",
) + res(r"Per a $m=4$ té infinites solucions: $(x,y,z)=(-1+t,\ 2-t,\ t)$. Per a $m\neq4$ té la solució única $(1,0,2)$; mai és incompatible."))

# ---------------- Setembre 1999 (1) ----------------
A = M([3, 1], [11, 4]); ih, Ai = inv_html(A)
assert Ai == M([4, -1], [-11, 3])
sol("S", "Setembre 1999", 1, steps(
    r"<strong>Forma matricial.</strong> $$%s\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}1\\0\end{pmatrix}\qquad\text{i}\qquad %s\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}0\\1\end{pmatrix}$$" % (tx(A), tx(A)),
    "<strong>Primer sistema.</strong> De $3x+y=1$, $y=1-3x$; $11x+4-12x=0\\Rightarrow x=4$, $y=-11$.",
    "<strong>Segon sistema.</strong> De $3x+y=0$, $y=-3x$; $11x-12x=1\\Rightarrow x=-1$, $y=3$.",
    "<strong>Inversa.</strong>" + ih,
    r"<strong>Relació.</strong> Les solucions són les columnes de $A^{-1}$, perquè $X=A^{-1}\begin{pmatrix}1\\0\end{pmatrix}$ és la primera columna de $A^{-1}$ i $X=A^{-1}\begin{pmatrix}0\\1\end{pmatrix}$ és la segona.",
) + res(r"$(4,-11)$ i $(-1,3)$, que són les columnes de $A^{-1}=%s$." % tx(Ai)))

# ---------------- Setembre 1999 (2) ----------------
h, s_ = G([[1, 1, 2, 3], [1, 2, 9, 5], [2, 1, -3, 4]])
sol("S", "Setembre 1999", 2, steps(
    dsc([["1", "1", "2"], ["1", "2", L], ["2", "1", "-3"]], r"(-6-\lambda)-(-3-2\lambda)+2(1-4)=\lambda-9", ["9"]),
    r"Si $\lambda\neq9$ el sistema és compatible determinat (solució única), així que infinites solucions només és possible per a $\lambda=9$.",
    crit(L, "9", [[1, 1, 2, 3], [1, 2, 9, 5], [2, 1, -3, 4]]),
    "<strong>Interpretació geomètrica.</strong> Els tres plans són distints i no paral·lels, i tenen en comú tota una <strong>recta</strong>: es tallen en una recta (feix de plans).",
) + res(r"$\lambda=9$; solucions $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$: els tres plans es tallen en una recta." % tuple(s_)))

# ---------------- Juny 2000 (1) ----------------
sol("S", "Juny 2000", 1, steps(
    dsc([["1", "1", "1"], ["1", "2", "3"], ["3", "4", L]], r"(2\lambda-12)-(\lambda-9)+(4-6)=\lambda-5", ["5"]),
    cdcase(["5"]),
    crit(L, "5", [[1, 1, 1, 1], [1, 2, 3, 3], [3, 4, 5, 5]]),
) + res(r"Solució única si $\lambda\neq5$; infinites solucions si $\lambda=5$ (en aquest cas, $(x,y,z)=(-1+t,\ 2-2t,\ t)$)."))

# ---------------- Setembre 2000 (1) ----------------
h, s_ = G([[2, 2, -2, 0], [4, 2, 2, 0], [3, 2, 0, 0]])
sol("S", "Setembre 2000", 1, steps(
    "<strong>Sistema homogeni.</strong> Té infinites solucions si i només si $|A|=0$.",
    dsc([["1", "1", "-1"], ["2", "1", "1"], [L, "1", "0"]], r"(0-1)-(0-\lambda)-(2-\lambda)=2\lambda-3", [r"\frac32"]),
    r"<strong>Cas $\lambda=\frac32$.</strong> Multipliquem la tercera equació per 2 per evitar fraccions: $3x+2y=0$." + G([[1, 1, -1, 0], [2, 1, 1, 0], [3, 2, 0, 0]])[0],
    "<strong>Interpretació.</strong> Els tres plans passen per l'origen i són distints, però $|A|=0$: tenen en comú una <strong>recta</strong> que passa per l'origen. Per això hi ha infinites solucions.",
) + res(r"$\lambda=\frac32$; $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[1, 1, -1, 0], [2, 1, 1, 0], [3, 2, 0, 0]])[1])))

# ---------------- Setembre 2000 (2) ----------------
sol("S", "Setembre 2000", 2, steps(
    dsc([["1", "1", "1"], ["1", "-3", "0"], ["-1", "0", "3"]], "(-9-0)-(3-0)+(0-3)=-15", []),
    cdcase([]) + r" Per Cramer:$$x=\frac{\begin{vmatrix}3+\lambda&1&1\\-2&-3&0\\2&0&3\end{vmatrix}}{-15}=\frac{-9\lambda-15}{-15}=\frac{3\lambda+5}5$$ $$y=\frac{\begin{vmatrix}1&3+\lambda&1\\1&-2&0\\-1&2&3\end{vmatrix}}{-15}=\frac{-3\lambda-15}{-15}=\frac{\lambda+5}5,\qquad z=\frac{\begin{vmatrix}1&1&3+\lambda\\1&-3&-2\\-1&0&2\end{vmatrix}}{-15}=\frac{-3\lambda-15}{-15}=\frac{\lambda+5}5$$",
    r"<strong>Relació amb $\pi_2\cap\pi_3$.</strong> Els plans $\pi_2$ i $\pi_3$ no són paral·lels, així que es tallen en una recta $r$. Cada solució compleix $\pi_2$ i $\pi_3$ (es pot comprovar: $x-3y=\frac{3\lambda+5-3\lambda-15}5=-2$ i $-x+3z=\frac{-3\lambda-5+3\lambda+15}5=2$), així que és un punt de $r$: és el punt on el pla $\pi_1:x+y+z=3+\lambda$ talla $r$. Quan $\lambda$ recorre $\mathbb{R}$, les solucions recorren <strong>tota la recta</strong> $r$: $$r:\ (x,y,z)=(1,1,1)+\tfrac{\lambda}{5}(3,1,1)$$",
) + res(r"$x=\frac{3\lambda+5}5,\ y=z=\frac{\lambda+5}5$. El conjunt de totes aquestes solucions és la recta intersecció de $\pi_2$ i $\pi_3$."))

# ---------------- Juny 2001 (1) ----------------
A = M([2, 3], [4, 2]); ih, Ai = inv_html(A)
X = mul(Ai, M([8], [8])); assert X == M([1], [2])
sol("S", "Juny 2001", 1, steps(
    "<strong>Apartat a) Inversa.</strong>" + ih,
    r"<strong>Resolem.</strong> $$X=A^{-1}\begin{pmatrix}8\\8\end{pmatrix}=%s\begin{pmatrix}8\\8\end{pmatrix}=%s$$" % (nice(Ai), tx(X)),
    r"<strong>Apartat b).</strong> $$A^2+A=I\Rightarrow A(A+I)=I$$ i també $(A+I)A=A^2+A=I$. Per tant $A$ és invertible i $A^{-1}=A+I$.",
) + res(r"a) $x=1,\ y=2$. &nbsp; b) $A^{-1}=A+I$."))

# ---------------- Setembre 2001 (1) ----------------
h, s_ = G([[1, 1, 1, 1], [1, 2, 3, 4], [3, 5, 7, 9]])
sol("S", "Setembre 2001", 1, steps(
    dsc([["1", "1", "1"], ["1", "2", "3"], ["3", "5", "m"]], "(2m-15)-(m-9)+(5-6)=m-7", ["7"], "m"),
    r"Si $m\neq7$ és compatible determinat; per tant, només pot ser indeterminat per a $m=7$.",
    crit("m", "7", [[1, 1, 1, 1], [1, 2, 3, 4], [3, 5, 7, 9]]),
    "<strong>Interpretació.</strong> Cada equació és un pla. Per a $m=7$ els tres plans són distints i es tallen en una <strong>recta</strong> (la tercera equació és $E_3=2E_1+E_2$: el tercer pla és del feix determinat pels altres dos).",
) + res(r"$m=7$; $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$: tres plans que es tallen en una recta." % tuple(s_)))

# ---------------- Setembre 2001 (2) ----------------
sol("S", "Setembre 2001", 2, steps(
    dsc([["1", "1", "1"], ["1", "2", "1"], ["3", "5", "m"]], "(2m-5)-(m-3)+(5-6)=m-3", ["3"], "m"),
    cdcase(["3"], "m") + r" Per Cramer: $$x=\frac{\begin{vmatrix}2&1&1\\3&2&1\\8&5&m\end{vmatrix}}{m-3}=\frac{m-3}{m-3}=1,\quad y=\frac{\begin{vmatrix}1&2&1\\1&3&1\\3&8&m\end{vmatrix}}{m-3}=\frac{m-3}{m-3}=1,\quad z=\frac{\begin{vmatrix}1&1&2\\1&2&3\\3&5&8\end{vmatrix}}{m-3}=0$$",
    crit("m", "3", [[1, 1, 1, 2], [1, 2, 1, 3], [3, 5, 3, 8]]),
) + res(r"Té solució única si i només si $m\neq3$, i aquesta és sempre $(x,y,z)=(1,1,0)$. (Per a $m=3$ té infinites solucions.)"))

# ---------------- Setembre 2002 (1) ----------------
sol("S", "Setembre 2002", 1, steps(
    dsc([["1", "1", "1"], ["2", "3", "5"], ["3", "5", r"\lambda^2"]], r"(3\lambda^2-25)-(2\lambda^2-15)+(10-9)=\lambda^2-9", ["3", "-3"]),
    cdcase(["3", "-3"]),
    crit(L, "3", [[1, 1, 1, 3], [2, 3, 5, 2], [3, 5, 9, 1]]),
    crit(L, "-3", [[1, 1, 1, -3], [2, 3, 5, 2], [3, 5, 9, 1]]),
    r"<strong>Apartat c).</strong> Un vector de $S$ és $(7+2t,\,-4-3t,\,t)$. És ortogonal a $(1,1,2)$ si el producte escalar és 0: $$(7+2t)+(-4-3t)+2t=3+t=0\Rightarrow t=-3$$ El vector és $(1,5,-3)$.",
) + res(r"a) CD si $\lambda\neq\pm3$; CI si $\lambda=3$; incompatible si $\lambda=-3$. &nbsp; b) $S=\{(7+2t,\,-4-3t,\,t):t\in\mathbb{R}\}$. &nbsp; c) $(1,5,-3)$."))
assert G([[1, 1, 1, 3], [2, 3, 5, 2], [3, 5, 9, 1]])[1] == ["7+2t", "-4-3t", "t"]

# ---------------- Juny 2003 (1) ----------------
sol("S", "Juny 2003", 1, steps(
    dsc([[L, "0", "2"], ["0", L, "-1"], ["1", "3", "1"]], r"\lambda(\lambda+3)-0+2(0-\lambda)=\lambda^2+\lambda=\lambda(\lambda+1)", ["0", "-1"]),
    cdcase(["0", "-1"]) + r" Per Cramer: $$x=\frac{\begin{vmatrix}0&0&2\\\lambda&\lambda&-1\\5&3&1\end{vmatrix}}{\lambda(\lambda+1)}=\frac{-4\lambda}{\lambda(\lambda+1)}=\frac{-4}{\lambda+1},\quad y=\frac{\begin{vmatrix}\lambda&0&2\\0&\lambda&-1\\1&5&1\end{vmatrix}}{\lambda(\lambda+1)}=\frac{\lambda(\lambda+3)}{\lambda(\lambda+1)}=\frac{\lambda+3}{\lambda+1}$$ $$z=\frac{\begin{vmatrix}\lambda&0&0\\0&\lambda&\lambda\\1&3&5\end{vmatrix}}{\lambda(\lambda+1)}=\frac{2\lambda^2}{\lambda(\lambda+1)}=\frac{2\lambda}{\lambda+1}$$",
    crit(L, "0", [[0, 0, 2, 0], [0, 0, -1, 0], [1, 3, 1, 5]], "x,y,z"),
    crit(L, "-1", [[-1, 0, 2, 0], [0, -1, -1, -1], [1, 3, 1, 5]]),
) + res(r"CD si $\lambda\neq0,-1$, amb $(x,y,z)=\left(\frac{-4}{\lambda+1},\frac{\lambda+3}{\lambda+1},\frac{2\lambda}{\lambda+1}\right)$. CI si $\lambda=0$: $(5-3t,\ t,\ 0)$. Incompatible si $\lambda=-1$."))

# ---------------- Juny 2004 (1) ----------------
sol("S", "Juny 2004", 1, steps(
    dsc([["1", "-1", "1"], [L, "2", "-1"], ["2", L, "-2"]], r"(-4+\lambda)+(-2\lambda+2)+(\lambda^2-4)=\lambda^2-\lambda-6=(\lambda-3)(\lambda+2)", ["3", "-2"]),
    cdcase(["3", "-2"]) + r" Per Cramer: $$x=\frac{\begin{vmatrix}\lambda&-1&1\\3\lambda&2&-1\\6&\lambda&-2\end{vmatrix}}{(\lambda-3)(\lambda+2)}=\frac{2(\lambda-3)(2\lambda+1)}{(\lambda-3)(\lambda+2)}=\frac{2(2\lambda+1)}{\lambda+2}$$ $$y=\frac{\begin{vmatrix}1&\lambda&1\\\lambda&3\lambda&-1\\2&6&-2\end{vmatrix}}{(\lambda-3)(\lambda+2)}=\frac{2(\lambda-3)(\lambda-1)}{(\lambda-3)(\lambda+2)}=\frac{2(\lambda-1)}{\lambda+2},\qquad z=\frac{\begin{vmatrix}1&-1&\lambda\\\lambda&2&3\lambda\\2&\lambda&6\end{vmatrix}}{(\lambda-3)(\lambda+2)}=\frac{(\lambda-3)(\lambda-2)(\lambda+2)}{(\lambda-3)(\lambda+2)}=\lambda-2$$",
    crit(L, "3", [[1, -1, 1, 3], [3, 2, -1, 9], [2, 3, -2, 6]]),
    crit(L, "-2", [[1, -1, 1, -2], [-2, 2, -1, -6], [2, -2, -2, 6]]),
) + res(r"a) CD si $\lambda\neq3,-2$; CI si $\lambda=3$; incompatible si $\lambda=-2$. &nbsp; b) $\left(\frac{2(2\lambda+1)}{\lambda+2},\frac{2(\lambda-1)}{\lambda+2},\lambda-2\right)$. &nbsp; c) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[1, -1, 1, 3], [3, 2, -1, 9], [2, 3, -2, 6]])[1])))

AL = r"\alpha"

# ---------------- Juny 2005 (1) ----------------
sol("S", "Juny 2005", 1, steps(
    dsc([["1", AL, r"\alpha^2"], ["1", AL, AL], ["1", r"\alpha^2", r"\alpha^2"]], r"\begin{vmatrix}1&\alpha&\alpha^2\\0&0&\alpha-\alpha^2\\0&\alpha^2-\alpha&0\end{vmatrix}=-(\alpha-\alpha^2)(\alpha^2-\alpha)=\alpha^2(\alpha-1)^2", ["0", "1"], AL)
    + " (hem restat la primera fila a la segona i a la tercera).",
    cdcase(["0", "1"], AL) + r" Per Cramer, amb $|A|=\alpha^2(\alpha-1)^2$: $$x=\frac{\begin{vmatrix}1&\alpha&\alpha^2\\\alpha&\alpha&\alpha\\\alpha^2&\alpha^2&\alpha^2\end{vmatrix}}{|A|}=0\ (\text{2a i 3a files proporcionals}),\qquad y=\frac{\begin{vmatrix}1&1&\alpha^2\\1&\alpha&\alpha\\1&\alpha^2&\alpha^2\end{vmatrix}}{|A|}=\frac{\alpha(\alpha-1)^2(\alpha+1)}{\alpha^2(\alpha-1)^2}=\frac{\alpha+1}{\alpha}$$ $$z=\frac{\begin{vmatrix}1&\alpha&1\\1&\alpha&\alpha\\1&\alpha^2&\alpha^2\end{vmatrix}}{|A|}=\frac{-\alpha(\alpha-1)^2}{\alpha^2(\alpha-1)^2}=-\frac1\alpha$$",
    crit(AL, "0", [[1, 0, 0, 1], [1, 0, 0, 0], [1, 0, 0, 0]]),
    crit(AL, "1", [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]),
) + res(r"Si $\alpha\neq0,1$: CD, $(x,y,z)=\left(0,\frac{\alpha+1}\alpha,-\frac1\alpha\right)$. Si $\alpha=0$: incompatible. Si $\alpha=1$: CI, $(x,y,z)=(1-t-s,\ t,\ s)$."))

# ---------------- Setembre 2005 (1) ----------------
h, s_ = G([[6, 3, 2, 470], [3, 4, 6, 370], [1, 3, 2, 160]])
assert s_ == [62, 22, 16]
sol("S", "Setembre 2005", 1, steps(
    "<strong>Incògnites.</strong> $x$, $y$, $z$ = percentatge (%) de Migato, Catomeal i Comecat en la mescla.",
    r"<strong>Plantegem el sistema.</strong> Un quilo de mescla conté $\frac{x}{100}$ kg de Migato, etc. Igualant els grams de carn, peix i verdura: $$%s\ \Rightarrow\ %s$$ (hem multiplicat per $\frac{100}{100}$ cada equació; observeu que sumant-les queda $10(x+y+z)=1000$, és a dir, $x+y+z=100$, com ha de ser)." % (sysm(r"600\tfrac{x}{100}+300\tfrac{y}{100}+200\tfrac{z}{100}&=470", r"300\tfrac{x}{100}+400\tfrac{y}{100}+600\tfrac{z}{100}&=370", r"100\tfrac{x}{100}+300\tfrac{y}{100}+200\tfrac{z}{100}&=160"), sysm("6x+3y+2z&=470", "3x+4y+6z&=370", "x+3y+2z&=160")),
    "<strong>Resolem per Gauss.</strong>" + h,
) + res("62 % de Migato, 22 % de Catomeal i 16 % de Comecat."))

# ---------------- Juny 2006 (1) ----------------
sol("S", "Juny 2006", 1, steps(
    dsc([["1", "2", "-3"], ["2", "6", "-11"], ["1", "-2", "7"]], "(42-22)-2(14+11)-3(-4-6)=20-50+30=0", [], AL).replace("$|A|\\neq0$ per a qualsevol valor del paràmetre.", r"$|A|=0$ per a tot $\alpha$; com que $\begin{vmatrix}1&2\\2&6\end{vmatrix}=2\neq0$, $\operatorname{rg}(A)=2$."),
    r"<strong>Rang de $A^*$.</strong> Orlem el menor anterior amb la columna de termes independents: $$\begin{vmatrix}1&2&\alpha\\2&6&2\\1&-2&1\end{vmatrix}=(6+4)-2(2-2)+\alpha(-4-6)=10-10\alpha=-10(\alpha-1)$$ Si $\alpha\neq1$, $\operatorname{rg}(A^*)=3\neq\operatorname{rg}(A)$: incompatible. Si $\alpha=1$, $\operatorname{rg}(A^*)=2$: compatible (indeterminat). Per tant, és compatible només per a $\alpha=1$.",
    crit(AL, "1", [[1, 2, -3, 1], [2, 6, -11, 2], [1, -2, 7, 1]]),
    r"<strong>Posició relativa dels plans.</strong> Els vectors normals $(1,2,-3)$, $(2,6,-11)$, $(1,-2,7)$ no són proporcionals dos a dos, així que no hi ha plans paral·lels ni coincidents. <ul><li>Si $\alpha=1$ ($\operatorname{rg}A=\operatorname{rg}A^*=2$): els tres plans es tallen en una <strong>recta</strong> (feix de plans).</li><li>Si $\alpha\neq1$ ($\operatorname{rg}A=2$, $\operatorname{rg}A^*=3$): es tallen <strong>dos a dos en tres rectes paral·leles</strong> (formen un prisma triangular) i no tenen cap punt comú.</li></ul>",
) + res(r"a) $\alpha=1$. &nbsp; b) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; c) $\alpha=1$: recta comuna; $\alpha\neq1$: prisma triangular." % tuple(G([[1, 2, -3, 1], [2, 6, -11, 2], [1, -2, 7, 1]])[1])))

# ---------------- Setembre 2006 (1) ----------------
sol("S", "Setembre 2006", 1, steps(
    "<strong>Sistema homogeni.</strong> Sempre és compatible. Només admet la solució trivial si és compatible determinat, és a dir, si $|A|\\neq0$.",
    dsc([[r"\lambda+2", "-1", "1"], ["3", r"\lambda+6", "-3"], ["5", "5", r"\lambda-2"]], r"(\lambda+2)\left[(\lambda+6)(\lambda-2)+15\right]+\left[3(\lambda-2)+15\right]+\left[15-5(\lambda+6)\right]=\lambda^3+6\lambda^2+9\lambda=\lambda(\lambda+3)^2", ["0", "-3"]),
    r"<strong>Apartat a).</strong> Només la solució $(0,0,0)$ si $\lambda\neq0$ i $\lambda\neq-3$.",
    crit(L, "0", [[2, -1, 1, 0], [3, 6, -3, 0], [5, 5, -2, 0]]),
    crit(L, "-3", [[-1, -1, 1, 0], [3, 3, -3, 0], [5, 5, -5, 0]]),
    r"<strong>Apartat c).</strong> Per a $\lambda=-3$ les tres equacions són $-x-y+z=0$, $3x+3y-3z=0$ i $5x+5y-5z=0$: totes són proporcionals a $x+y-z=0$. Els tres plans són <strong>coincidents</strong> (és el mateix pla, que passa per l'origen).",
) + res(r"a) $\lambda\neq0,-3$. &nbsp; b) $\lambda=0$: $(x,y,z)=(%s,\ %s,\ %s)$; $\lambda=-3$: $(x,y,z)=(%s,\ %s,\ %s)$. &nbsp; c) Tres plans coincidents." % tuple(G([[2, -1, 1, 0], [3, 6, -3, 0], [5, 5, -2, 0]])[1] + G([[-1, -1, 1, 0], [3, 3, -3, 0], [5, 5, -5, 0]])[1])))

# ---------------- Juny 2007 (1) ----------------
sol("S", "Juny 2007", 1, steps(
    dsc([["1", AL, "1"], ["3", "5", "1"], [AL, "1", "1"]], r"(5-1)-\alpha(3-\alpha)+(3-5\alpha)=\alpha^2-8\alpha+7=(\alpha-1)(\alpha-7)", ["1", "7"], AL),
    cdcase(["1", "7"], AL) + r" (Es comprova que la solució és $(0,0,9)$.)",
    crit(AL, "1", [[1, 1, 1, 9], [3, 5, 1, 9], [1, 1, 1, 9]]),
    crit(AL, "7", [[1, 7, 1, 9], [3, 5, 1, 9], [7, 1, 1, 9]]),
    "<strong>Conclusió.</strong> En tots els casos $\\operatorname{rg}(A)=\\operatorname{rg}(A^*)$: el sistema és sempre compatible, i és indeterminat per a $\\alpha=1$ i $\\alpha=7$.",
) + res(r"a) Sempre compatible; indeterminat per a $\alpha=1$ i $\alpha=7$. &nbsp; b) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[1, 7, 1, 9], [3, 5, 1, 9], [7, 1, 1, 9]])[1])))

# ---------------- Setembre 2007 (1) ----------------
sol("S", "Setembre 2007", 1, steps(
    dsc([["6", "3", "2"], ["3", "4", "6"], ["1", "3", "2"]], "6(8-18)-3(6-6)+2(9-4)=-60+10=-50", [], AL),
    cdcase([], AL),
    r"<strong>Apartat b) Cramer.</strong> $$x=\frac{\begin{vmatrix}5&3&2\\3&4&6\\\alpha&3&2\end{vmatrix}}{-50}=\frac{10\alpha-50}{-50}=\frac{5-\alpha}{5},\qquad y=\frac{\begin{vmatrix}6&5&2\\3&3&6\\1&\alpha&2\end{vmatrix}}{-50}=\frac{30-30\alpha}{-50}=\frac{3(\alpha-1)}{5}$$ $$z=\frac{\begin{vmatrix}6&3&5\\3&4&3\\1&3&\alpha\end{vmatrix}}{-50}=\frac{15\alpha-20}{-50}=\frac{4-3\alpha}{10}$$",
    r"<strong>Apartat c).</strong> $$x+y+z=\frac{10-2\alpha+6\alpha-6+4-3\alpha}{10}=\frac{\alpha+8}{10}=1\Rightarrow\alpha=2$$ (La solució és llavors $\left(\frac35,\frac35,-\frac15\right)$.)",
) + res(r"a) $|A|=-50\neq0$ sempre. &nbsp; b) $\left(\frac{5-\alpha}5,\frac{3(\alpha-1)}5,\frac{4-3\alpha}{10}\right)$. &nbsp; c) $\alpha=2$."))
for al_ in (0, 2, 7):
    X = mul(inv(M([6, 3, 2], [3, 4, 6], [1, 3, 2])), M([5], [3], [al_]))
    assert X == M([Fr(5 - al_, 5)], [Fr(3 * (al_ - 1), 5)], [Fr(4 - 3 * al_, 10)])

# ---------------- Juny 2008 (1) ----------------
sol("S", "Juny 2008", 1, steps(
    dsc([[AL, "1", "1"], ["1", AL, "1"], ["1", "1", AL]], r"\alpha^3-3\alpha+2=(\alpha-1)^2(\alpha+2)", ["1", "-2"], AL),
    cdcase(["1", "-2"], AL),
    crit(AL, "1", [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]),
    crit(AL, "-2", [[-2, 1, 1, 1], [1, -2, 1, 1], [1, 1, -2, 1]]),
    r"<strong>Apartat b).</strong> El sistema és simètric en $x,y,z$, així que la solució única compleix $x=y=z$: $\alpha x+x+x=1\Rightarrow x=\frac1{\alpha+2}$. (També surt per Cramer: $|A_x|=|A_y|=|A_z|=(\alpha-1)^2$.)",
    r"<strong>Apartat c).</strong> $\alpha=0$ és un cas compatible determinat: $x=y=z=\frac12$.",
) + res(r"a) CD si $\alpha\neq1,-2$; CI si $\alpha=1$; incompatible si $\alpha=-2$. &nbsp; b) $x=y=z=\frac1{\alpha+2}$. &nbsp; c) $\left(\frac12,\frac12,\frac12\right)$."))

# ---------------- Setembre 2008 (1) ----------------
sol("S", "Setembre 2008", 1, steps(
    dsc([["1", "1", "1"], ["2", "-1", "1"], ["3", AL, "2"]], r"(-2-\alpha)-(4-3)+(2\alpha+3)=\alpha", ["0"], AL),
    cdcase(["0"], AL) + r" Per Cramer: $x=\frac{-6\alpha}{\alpha}=-6$, $y=\frac{-2\alpha}{\alpha}=-2$, $z=\frac{\alpha(\alpha+11)}{\alpha}=\alpha+11$.",
    crit(AL, "0", [[1, 1, 1, 3], [2, -1, 1, 1], [3, 0, 2, 4]]),
    "<strong>Conclusió.</strong> Per a $\\alpha\\neq0$ és CD i per a $\\alpha=0$ és CI: és compatible per a tot $\\alpha$, i indeterminat només si $\\alpha=0$.",
) + res(r"a) Sempre compatible. &nbsp; b) $\alpha=0$. &nbsp; c) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[1, 1, 1, 3], [2, -1, 1, 1], [3, 0, 2, 4]])[1])))

# ---------------- Juny 2009 (1) ----------------
sol("S", "Juny 2009", 1, steps(
    dsc([[r"\alpha+3", "-4", "-2"], ["1", "-2", r"-(\alpha+2)"], ["2", r"\alpha-3", "-2"]], r"\alpha^3+2\alpha^2+\alpha=\alpha(\alpha+1)^2", ["0", "-1"], AL),
    crit(AL, "0", [[3, -4, -2, 4], [1, -2, -2, 2], [2, -3, -2, 4]]),
    cdcase(["0", "-1"], AL),
    crit(AL, "-1", [[2, -4, -2, 4], [1, -2, -1, 2], [2, -4, -2, 4]]),
) + res(r"a) Per a $\alpha=0$, $\operatorname{rg}A=2\neq\operatorname{rg}A^*=3$. &nbsp; b) $\alpha\neq0,-1$. &nbsp; c) $\alpha=-1$: $(x,y,z)=(%s,\ %s,\ %s)$." % tuple(G([[2, -4, -2, 4], [1, -2, -1, 2], [2, -4, -2, 4]])[1])))

# ---------------- Setembre 2009 (1) ----------------
sol("S", "Setembre 2009", 1, steps(
    "<strong>Sistema homogeni.</strong> Només admet la solució trivial si $|A|\\neq0$.",
    dsc([["1", "1", "1"], ["2", "3", "4"], ["5", "7", AL]], r"(3\alpha-28)-(2\alpha-20)+(14-15)=\alpha-9", ["9"], AL),
    r"<strong>Apartat a).</strong> Només $(0,0,0)$ si $\alpha\neq9$.",
    crit(AL, "9", [[1, 1, 1, 0], [2, 3, 4, 0], [5, 7, 9, 0]]),
) + res(r"a) $\alpha\neq9$. &nbsp; b) $\alpha=9$: $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[1, 1, 1, 0], [2, 3, 4, 0], [5, 7, 9, 0]])[1])))

# ---------------- Juny 2010 (1) ----------------
A = M([2, -1, 1], [3, 2, -2], [5, -2, 1])
assert mul(A, M([1], [2], [3])) == M([3], [1], [4]) and det(A) == -7
sol("S", "Juny 2010", 1, steps(
    r"<strong>Apartat a).</strong> Amb $a=0$, $b=-1$, $c=2$ el sistema és $$%s$$ La primera equació diu $-y+z=6$ i la tercera, dividint per 2, $-y+z=2$: són contradictòries. El sistema és %s." % (sysm("-y+z&=6", "3x+2y-4z&=0", "-2y+2z&=4"), SI),
    r"<strong>Apartat b).</strong> Substituïm $(x,y,z)=(1,2,3)$: $$%s\ \Rightarrow\ %s$$ És un sistema lineal en $a,b,c$; el resolem per Gauss:" % (sysm("2a+2b+3&=3c", "3-4b-6c&=a", "5a-4+3c&=-4b"), sysm("2a+2b-3c&=-3", "a+4b+6c&=3", "5a+4b+3c&=4")) + G([[2, 2, -3, -3], [1, 4, 6, 3], [5, 4, 3, 4]], "a,b,c")[0],
    r"<strong>Apartat c).</strong> Amb $a=1$, $b=-1$, $c=1$ la matriu de coeficients és $$A=%s,\qquad |A|=-7\neq0$$ Per tant el sistema és compatible determinat i la solució $(1,2,3)$ <strong>és única</strong>." % tx(A),
) + res(r"a) Equacions 1a i 3a contradictòries. &nbsp; b) $a=1,\ b=-1,\ c=1$. &nbsp; c) Sí, és única ($|A|=-7\neq0$)."))
assert G([[2, 2, -3, -3], [1, 4, 6, 3], [5, 4, 3, 4]], "a,b,c")[1] == [1, -1, 1]

# ---------------- Setembre 2010 (1) ----------------
sol("S", "Setembre 2010", 1, steps(
    dsc([[AL, r"\alpha^3", "1"], [AL, AL, "1"], [r"\alpha^3", AL, "1"]], r"\begin{vmatrix}\alpha&\alpha^3&1\\0&\alpha-\alpha^3&0\\\alpha^3-\alpha&\alpha-\alpha^3&0\end{vmatrix}=1\cdot\left[0-(\alpha-\alpha^3)(\alpha^3-\alpha)\right]=(\alpha^3-\alpha)^2=\alpha^2(\alpha-1)^2(\alpha+1)^2", ["0", "1", "-1"], AL)
    + " (hem restat la 1a fila a la 2a i a la 3a, i desenvolupat per la 3a columna).",
    r"<strong>Apartat a).</strong> " + cdcase(["0", "1", "-1"], AL) + r" (La solució és $(0,0,1)$.)",
    crit(AL, "0", [[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1]]),
    crit(AL, "1", [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]),
    crit(AL, "-1", [[-1, -1, 1, 1], [-1, -1, 1, 1], [-1, -1, 1, 1]]),
    r"<strong>Apartat b).</strong> En els tres casos les tres equacions són iguals: $\operatorname{rg}A=\operatorname{rg}A^*=1$ i el sistema és compatible indeterminat (amb dos paràmetres).",
) + res(r"a) CD si $\alpha\neq0,\pm1$. &nbsp; b) CI si $\alpha\in\{0,1,-1\}$. &nbsp; c) $\alpha=0$: $(t,s,1)$; $\alpha=1$: $(1-t-s,\,t,\,s)$; $\alpha=-1$: $(-1-t+s,\,t,\,s)$, amb $t,s\in\mathbb{R}$."))
assert G([[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1]])[1] == ["t", "s", "1"]
assert G([[-1, -1, 1, 1], [-1, -1, 1, 1], [-1, -1, 1, 1]])[1] == ["-1-t+s", "t", "s"]

# ---------------- Juny 2011 (1) ----------------
sol("S", "Juny 2011", 1, steps(
    crit("m", "2", [[1, 1, 1, 2], [2, 0, 3, 5], [1, 3, 0, 1]]).replace("<strong>Cas $m=2$.</strong>", "<strong>Apartat a) $m=2$.</strong>"),
    dsc([["1", "1", "1"], ["2", "0", "3"], ["1", "3", "m-2"]], "(0-9)-(2m-4-3)+(6-0)=-2m+4=-2(m-2)", ["2"], "m").replace("<strong>Determinant", "<strong>Apartat b) Determinant"),
    "Si $m\\neq2$, $|A|\\neq0$ i el sistema té solució única; si $m=2$ hem vist que en té infinites. Per tant: solució única $\\iff m\\neq2$.",
    r"<strong>Apartat c).</strong> Substituïm $(x,y,z)=\left(\frac32,-\frac12,0\right)$: $$x+y+z=1=m\Rightarrow m=1$$ Comprovem les altres equacions amb $m=1$: $2\cdot\frac32+0=3=2m+1$ ✓ i $\frac32-\frac32+0=0=m-1$ ✓.",
) + res(r"a) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; b) $m\neq2$. &nbsp; c) $m=1$." % tuple(G([[1, 1, 1, 2], [2, 0, 3, 5], [1, 3, 0, 1]])[1])))

# ---------------- Juny 2012 (1) ----------------
sol("S", "Juny 2012", 1, steps(
    crit(AL, "0", [[2, 0, 0, 5], [1, 1, 1, 1], [1, 2, 0, 1]]).replace("<strong>Cas", "<strong>Apartat a)"),
    crit(AL, "-1", [[2, 0, 1, 5], [1, 2, 1, 1], [1, 2, 1, 1]]).replace("<strong>Cas", "<strong>Apartat b)"),
    dsc([["2", "0", r"\alpha^2"], ["1", r"1-\alpha", "1"], ["1", "2", r"\alpha^2"]], r"2\left[(1-\alpha)\alpha^2-2\right]+\alpha^2\left[2-(1-\alpha)\right]=-\alpha^3+3\alpha^2-4=-(\alpha+1)(\alpha-2)^2", ["-1", "2"], AL).replace("<strong>Determinant", "<strong>Apartat c) Determinant"),
    r"Si $\alpha\neq-1,2$ el sistema és compatible determinat, i per a $\alpha=-1$ hem vist que és compatible indeterminat. Només cal estudiar $\alpha=2$:" + G([[2, 0, 4, 5], [1, -1, 1, 1], [1, 2, 4, 1]])[0],
) + res(r"a) $(x,y,z)=\left(\frac52,-\frac34,-\frac34\right)$. &nbsp; b) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; c) $\alpha=2$." % tuple(G([[2, 0, 1, 5], [1, 2, 1, 1], [1, 2, 1, 1]])[1])))
assert G([[2, 0, 0, 5], [1, 1, 1, 1], [1, 2, 0, 1]])[1] == [Fr(5, 2), Fr(-3, 4), Fr(-3, 4)]

# ---------------- Setembre 2012 (1) ----------------
sol("S", "Setembre 2012", 1, steps(
    dsc([["1", "-2", "-3"], ["3", "10", "-1"], ["1", "14", AL]], r"(10\alpha+14)+2(3\alpha+1)-3(42-10)=16\alpha-80=16(\alpha-5)", ["5"], AL),
    r"<strong>Apartat a).</strong> Per a $\alpha=0$, $|A|=-80\neq0$: el sistema homogeni és compatible determinat i la seua única solució és la trivial, $(0,0,0)$.",
    r"<strong>Apartat b).</strong> Un sistema homogeni té infinites solucions si i només si $|A|=0$, és a dir, $\alpha=5$.",
    crit(AL, "5", [[1, -2, -3, 0], [3, 10, -1, 0], [1, 14, 5, 0]]).replace("<strong>Cas", "<strong>Apartat c)"),
) + res(r"a) $(0,0,0)$. &nbsp; b) $\alpha=5$. &nbsp; c) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[1, -2, -3, 0], [3, 10, -1, 0], [1, 14, 5, 0]])[1])))

# ---------------- Juny 2013 (1) ----------------
sol("S", "Juny 2013", 1, steps(
    r"<strong>Rangs.</strong> Tenim 3 equacions i 2 incògnites. $A=\begin{pmatrix}2&5\\-1&-4\\2&1\end{pmatrix}$ té $\begin{vmatrix}2&5\\-1&-4\end{vmatrix}=-3\neq0$, així que $\operatorname{rg}(A)=2$. El sistema és compatible si i només si $\operatorname{rg}(A^*)=2$, és a dir, si $|A^*|=0$: $$|A^*|=\begin{vmatrix}2&5&a\\-1&-4&b\\2&1&c\end{vmatrix}=2(-4c-b)-5(-c-2b)+a(-1+8)=7a+8b-3c$$",
    r"<strong>Apartat a).</strong> Ha de complir-se $7a+8b-3c=0$ (i aleshores és compatible determinat, perquè $\operatorname{rg}=2=$ nombre d'incògnites).",
    r"<strong>Apartat b).</strong> $7(-1)+8\cdot2-3\cdot3=0$ ✓, és compatible. Resolem amb les dues primeres equacions: $$%s\ \Rightarrow\ x=-2-4y\ \Rightarrow\ 2(-2-4y)+5y=-1\Rightarrow y=-1,\ x=2$$ (comprovem la 3a: $2\cdot2-1=3$ ✓)." % sysm("2x+5y&=-1", "-x-4y&=2"),
    r"<strong>Apartat c).</strong> Si $a=c=-2b$: $7(-2b)+8b-3(-2b)=0$ ✓, sempre és compatible. $$%s\Rightarrow x=-b-4y\Rightarrow -2b-8y+5y=-2b\Rightarrow y=0,\ x=-b$$ (3a: $2(-b)+0=-2b=c$ ✓)." % sysm("2x+5y&=-2b", "-x-4y&=b"),
) + res(r"a) $7a+8b-3c=0$. &nbsp; b) $x=2,\ y=-1$. &nbsp; c) $x=-b,\ y=0$."))

# ---------------- Juliol 2013 (1) ----------------
sol("S", "Juliol 2013", 1, steps(
    dsc([[AL, "1", "1"], ["1", AL, "1"], ["3", "5", "1"]], r"\alpha(\alpha-5)-(1-3)+(5-3\alpha)=\alpha^2-8\alpha+7=(\alpha-1)(\alpha-7)", ["1", "7"], AL),
    crit(AL, "7", [[7, 1, 1, 1], [1, 7, 1, 1], [3, 5, 1, 1]]).replace("<strong>Cas", "<strong>Apartat a)"),
    crit(AL, "1", [[1, 1, 1, 1], [1, 1, 1, 1], [3, 5, 1, 1]]),
    r"<strong>Apartats b) i c).</strong> Per a $\alpha=1$ i $\alpha=7$ el sistema és compatible indeterminat. Per a $\alpha\neq1,7$, $|A|\neq0$ i és compatible determinat (la solució és $(0,0,1)$).",
) + res(r"a) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; b) $\alpha=1$ i $\alpha=7$. &nbsp; c) $\alpha\neq1,7$." % tuple(G([[7, 1, 1, 1], [1, 7, 1, 1], [3, 5, 1, 1]])[1])))

# ---------------- Juny 2014 (1) ----------------
sol("S", "Juny 2014", 1, steps(
    dsc([["1", "3", "2"], ["2", "4", "5"], ["1", "k^2", "3"]], r"(12-5k^2)-3(6-5)+2(2k^2-4)=1-k^2=-(k-1)(k+1)", ["1", "-1"], "k"),
    cdcase(["1", "-1"], "k"),
    crit("k", "1", [[1, 3, 2, -1], [2, 4, 5, -1], [1, 1, 3, 2]]),
    crit("k", "-1", [[1, 3, 2, -1], [2, 4, 5, -3], [1, 1, 3, -2]]),
    crit("k", "0", [[1, 3, 2, -1], [2, 4, 5, -2], [1, 0, 3, 0]]).replace("<strong>Cas $k=0$.</strong>", "<strong>Apartat c) $k=0$.</strong>"),
) + res(r"a) CD si $k\neq\pm1$; CI si $k=-1$; incompatible si $k=1$. &nbsp; b) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; c) $(x,y,z)=(%s,\ %s,\ %s)$." % tuple(G([[1, 3, 2, -1], [2, 4, 5, -3], [1, 1, 3, -2]])[1] + G([[1, 3, 2, -1], [2, 4, 5, -2], [1, 0, 3, 0]])[1])))

# ---------------- Juliol 2014 (1) ----------------
sol("S", "Juliol 2014", 1, steps(
    dsc([[r"1-\alpha", "2", "1"], ["1", "1", "-2"], ["1", "4", r"-(\alpha+1)"]], r"(1-\alpha)(7-\alpha)-2(1-\alpha)+3=\alpha^2-6\alpha+8=(\alpha-2)(\alpha-4)", ["2", "4"], AL),
    crit(AL, "4", [[-3, 2, 1, 4], [1, 1, -2, -4], [1, 4, -5, -8]]),
    crit(AL, "2", [[-1, 2, 1, 4], [1, 1, -2, -4], [1, 4, -3, -4]]),
    cdcase(["2", "4"], AL),
) + res(r"a) $\alpha=4$. &nbsp; b) $\alpha\neq2,4$. &nbsp; c) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[-1, 2, 1, 4], [1, 1, -2, -4], [1, 4, -3, -4]])[1])))

# ---------------- Juny 2015 (1) ----------------
sol("S", "Juny 2015", 1, steps(
    crit(AL, "1", [[0, 3, 4, 1], [1, 1, 0, 4], [2, 2, 0, 8]]).replace("<strong>Cas", "<strong>Apartat a)"),
    crit(AL, "2", [[-1, 5, 6, 2], [2, 2, 0, 6], [2, 3, 1, 9]]).replace("<strong>Cas", "<strong>Apartat b)"),
    dsc([[r"1-\alpha", r"2\alpha+1", r"2\alpha+2"], [AL, AL, "0"], ["2", r"\alpha+1", r"\alpha-1"]], r"-\alpha\left[(2\alpha+1)(\alpha-1)-(2\alpha+2)(\alpha+1)\right]+\alpha\left[(1-\alpha)(\alpha-1)-2(2\alpha+2)\right]=-\alpha^3+3\alpha^2-2\alpha=-\alpha(\alpha-1)(\alpha-2)", ["0", "1", "2"], AL).replace("<strong>Determinant", "<strong>Apartat c) Determinant") + " (hem desenvolupat per la segona fila).",
    cdcase(["0", "1", "2"], AL) + " Per als altres valors ja hem vist que per a $\\alpha=1$ és CI i per a $\\alpha=2$ incompatible (i per a $\\alpha=0$ tampoc és CD, perquè $|A|=0$).",
) + res(r"a) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; b) Incompatible. &nbsp; c) $\alpha\neq0,1,2$." % tuple(G([[0, 3, 4, 1], [1, 1, 0, 4], [2, 2, 0, 8]])[1])))

# ---------------- Juny 2016 (1) ----------------
sol("S", "Juny 2016", 1, steps(
    dsc([["a", "0", "-1"], ["2", "a", "1"], ["2", "0", "1"]], "a(a-0)-0+(-1)(0-2a)=a^2+2a=a(a+2)", ["0", "-2"], "a"),
    crit("a", "0", [[0, 0, -1, 0], [2, 0, 1, 1], [2, 0, 1, 2]]).replace("<strong>Cas", "<strong>Apartat a)"),
    crit("a", "-2", [[-2, 0, -1, -2], [2, -2, 1, 1], [2, 0, 1, 2]]).replace("<strong>Cas", "<strong>Apartat b)"),
    r"<strong>Apartat c) $a=-1$.</strong> $|A|=-1\neq0$: compatible determinat. Per Cramer, amb $|A|=a(a+2)$, $|A_x|=a(a+2)$, $|A_y|=-(a+2)$ i $|A_z|=0$: $x=1$, $y=-\frac1a$, $z=0$. Per a $a=-1$: $(x,y,z)=(1,1,0)$. Comprovació: $-1-0=-1$ ✓, $2-1+0=1$ ✓, $2+0=2$ ✓.",
) + res(r"a) $a=0$. &nbsp; b) $a=-2$: $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; c) $(1,1,0)$." % tuple(G([[-2, 0, -1, -2], [2, -2, 1, 1], [2, 0, 1, 2]])[1])))

# ---------------- Juliol 2016 (1) ----------------
sol("S", "Juliol 2016", 1, steps(
    crit(AL, "0", [[1, 1, 2, 2], [-3, 2, 3, -2], [2, 0, -5, -4]]).replace("<strong>Cas", "<strong>Apartat a)"),
    dsc([["1", "1", "2"], ["-3", "2", "3"], ["2", AL, "-5"]], r"(-10-3\alpha)-(15-6)+2(-3\alpha-4)=-9\alpha-27=-9(\alpha+3)", ["-3"], AL),
    crit(AL, "-3", [[1, 1, 2, 2], [-3, 2, 3, -2], [2, -3, -5, -4]]).replace("<strong>Cas", "<strong>Apartat b)"),
    "<strong>Apartat c).</strong> " + cdcase(["-3"], AL) + r" Per Cramer: $$x=\frac{\begin{vmatrix}2&1&2\\-2&2&3\\-4&\alpha&-5\end{vmatrix}}{-9(\alpha+3)}=\frac{-2(5\alpha+13)}{-9(\alpha+3)}=\frac{2(5\alpha+13)}{9(\alpha+3)},\qquad y=\frac{\begin{vmatrix}1&2&2\\-3&-2&3\\2&-4&-5\end{vmatrix}}{-9(\alpha+3)}=\frac{36}{-9(\alpha+3)}=\frac{-4}{\alpha+3}$$ $$z=\frac{\begin{vmatrix}1&1&2\\-3&2&-2\\2&\alpha&-4\end{vmatrix}}{-9(\alpha+3)}=\frac{-4(\alpha+8)}{-9(\alpha+3)}=\frac{4(\alpha+8)}{9(\alpha+3)}$$",
) + res(r"a) $\left(\frac{26}{27},-\frac43,\frac{32}{27}\right)$. &nbsp; b) $\alpha=-3$. &nbsp; c) $\alpha\neq-3$: $\left(\frac{2(5\alpha+13)}{9(\alpha+3)},\frac{-4}{\alpha+3},\frac{4(\alpha+8)}{9(\alpha+3)}\right)$."))
assert G([[1, 1, 2, 2], [-3, 2, 3, -2], [2, 0, -5, -4]])[1] == [Fr(26, 27), Fr(-4, 3), Fr(32, 27)]

# ---------------- Juny 2017 (1) ----------------
sol("S", "Juny 2017", 1, steps(
    crit("a", "2", [[-1, 2, 2, 2], [2, 2, -1, 2], [2, -1, 2, 2]]).replace("<strong>Cas", "<strong>Apartat a)"),
    dsc([["-1", "a", "2"], ["2", "a", "-1"], ["a", "-1", "2"]], "-(2a-1)-a(4+a)+2(-2-a^2)=-3a^2-6a-3=-3(a+1)^2", ["-1"], "a"),
    "<strong>Apartat b).</strong> " + cdcase(["-1"], "a"),
    crit("a", "-1", [[-1, -1, 2, -1], [2, -1, -1, 2], [-1, -1, 2, -1]]).replace("<strong>Cas", "<strong>Apartat c)"),
) + res(r"a) $\left(\frac23,\frac23,\frac23\right)$. &nbsp; b) $a\neq-1$. &nbsp; c) $a=-1$: $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[-1, -1, 2, -1], [2, -1, -1, 2], [-1, -1, 2, -1]])[1])))
assert G([[-1, 2, 2, 2], [2, 2, -1, 2], [2, -1, 2, 2]])[1] == [Fr(2, 3)] * 3

# ---------------- Juny 2018 (1) ----------------
sol("S", "Juny 2018", 1, steps(
    dsc([["0", "1", "-1"], ["-1", "0", "1"], ["-a", "1", "-1"]], "0-1\\cdot(1+a)+(-1)(-1)=-a", ["0"], "a"),
    "<strong>Apartat a).</strong> " + cdcase(["0"], "a"),
    crit("a", "3", [[0, 1, -1, -2], [-1, 0, 1, 5], [-3, 1, -1, 1]]).replace("<strong>Cas", "<strong>Apartat b)"),
    crit("a", "0", [[0, 1, -1, 1], [-1, 0, 1, 5], [0, 1, -1, 1]]).replace("<strong>Cas", "<strong>Apartat c)"),
) + res(r"a) $a\neq0$. &nbsp; b) $(-1,2,4)$. &nbsp; c) $a=0$: $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[0, 1, -1, 1], [-1, 0, 1, 5], [0, 1, -1, 1]])[1])))
assert G([[0, 1, -1, -2], [-1, 0, 1, 5], [-3, 1, -1, 1]])[1] == [-1, 2, 4]

# ---------------- Juliol 2018 (1) ----------------
sol("S", "Juliol 2018", 1, steps(
    dsc([["1", "1", "0"], ["0", "a-1", "1"], ["1", "a", "a-1"]], "1\\cdot[(a-1)^2-a]-1\\cdot(0-1)=a^2-3a+2=(a-1)(a-2)", ["1", "2"], "a"),
    cdcase(["1", "2"], "a"),
    crit("a", "2", [[1, 1, 0, 1], [0, 1, 1, 0], [1, 2, 1, 2]]),
    crit("a", "1", [[1, 1, 0, 1], [0, 0, 1, 0], [1, 1, 0, 1]]).replace("<strong>Cas", "<strong>Apartat b)"),
    r"<strong>Apartat c) $a=0$.</strong> $|A|=2\neq0$. Per Cramer: $$x=\frac{\begin{vmatrix}1&1&0\\0&-1&1\\0&0&-1\end{vmatrix}}{2}=\frac12,\quad y=\frac{\begin{vmatrix}1&1&0\\0&0&1\\1&0&-1\end{vmatrix}}{2}=\frac12,\quad z=\frac{\begin{vmatrix}1&1&1\\0&-1&0\\1&0&0\end{vmatrix}}{2}=\frac12$$",
) + res(r"a) Compatible si $a\neq2$ (CD si $a\neq1,2$; CI si $a=1$). &nbsp; b) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; c) $\left(\frac12,\frac12,\frac12\right)$." % tuple(G([[1, 1, 0, 1], [0, 0, 1, 0], [1, 1, 0, 1]])[1])))
assert mul(inv(M([1, 1, 0], [0, -1, 1], [1, 0, -1])), M([1], [0], [0])) == M([Fr(1, 2)], [Fr(1, 2)], [Fr(1, 2)])

# ---------------- Juny 2019 (1) ----------------
A1 = M([1, 0, 1], [-2, 2, 2], [-3, 0, 1]); assert det(A1) == 8
sol("S", "Juny 2019", 1, steps(
    r"<strong>Apartat a) Rang.</strong> $$|A|=\begin{vmatrix}1&0&a\\-2&a+1&2\\-3&a-1&a\end{vmatrix}=\left[a(a+1)-2(a-1)\right]+a\left[-2(a-1)+3(a+1)\right]=2a^2+4a+2=2(a+1)^2$$ Si $a\neq-1$, $|A|\neq0$ i $\operatorname{rg}(A)=3$. Si $a=-1$, $A=\begin{pmatrix}1&0&-1\\-2&0&2\\-3&-2&-1\end{pmatrix}$, $|A|=0$ i el menor de les files 1a i 3a i columnes 1a i 2a és $\begin{vmatrix}1&0\\-3&-2\end{vmatrix}=-2\neq0$, així que $\operatorname{rg}(A)=2$.",
    r"<strong>Determinant de $2A^{-1}$ per a $a=1$.</strong> $|A|=2\cdot2^2=8$. Com que $A$ és $3\times3$: $$|2A^{-1}|=2^3\,|A^{-1}|=\frac{8}{|A|}=\frac88=1$$",
    crit("a", "-1", [[1, 0, -1, -1], [-2, 0, 2, 2], [-3, -2, -1, 0]]).replace("<strong>Cas", "<strong>Apartat b)"),
    r"<strong>Apartat c).</strong> $$B^2=\tfrac13I-2B\Rightarrow B^2+2B=\tfrac13I\Rightarrow B(B+2I)=\tfrac13I\Rightarrow B\,(3B+6I)=I$$ i també $(3B+6I)B=I$. Per tant $B$ és invertible i $B^{-1}=3B+6I$.",
) + res(r"a) $\operatorname{rg}A=3$ si $a\neq-1$; $\operatorname{rg}A=2$ si $a=-1$; $|2A^{-1}|=1$. &nbsp; b) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; c) $m=3$, $n=6$." % tuple(G([[1, 0, -1, -1], [-2, 0, 2, 2], [-3, -2, -1, 0]])[1])))

# ---------------- Juny 2019 (2) ----------------
sol("S", "Juny 2019", 2, steps(
    r"<strong>Rang de $A$.</strong> $$|A|=\begin{vmatrix}1&1&1\\3&4&5\\7&9&11\end{vmatrix}=(44-45)-(33-35)+(27-28)=0,\qquad \begin{vmatrix}1&1\\3&4\end{vmatrix}=1\neq0$$ Per tant $\operatorname{rg}(A)=2$ per a tot $\alpha$.",
    r"<strong>Apartat a) Rang de $A^*$.</strong> Orlem el menor amb la columna de termes independents: $$\begin{vmatrix}1&1&4\\3&4&5\\7&9&\alpha\end{vmatrix}=(4\alpha-45)-(3\alpha-35)+4(27-28)=\alpha-14$$ Si $\alpha=14$: $\operatorname{rg}A=\operatorname{rg}A^*=2<3$, compatible (indeterminat). Si $\alpha\neq14$: $\operatorname{rg}A^*=3$, incompatible.",
    crit(AL, "14", [[1, 1, 1, 4], [3, 4, 5, 5], [7, 9, 11, 14]]).replace("<strong>Cas", "<strong>Apartat b)"),
    r"<strong>Apartat c).</strong> Si canviem 11 per $c\neq11$: $$\begin{vmatrix}1&1&1\\3&4&5\\7&9&c\end{vmatrix}=(4c-45)-(3c-35)+(27-28)=c-11\neq0$$ i el nou sistema és <strong>compatible determinat per a qualsevol valor de $\alpha$</strong>.",
) + res(r"a) Compatible si $\alpha=14$, incompatible si $\alpha\neq14$. &nbsp; b) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; c) Sempre compatible determinat." % tuple(G([[1, 1, 1, 4], [3, 4, 5, 5], [7, 9, 11, 14]])[1])))

# ---------------- Juliol 2019 (1) ----------------
sol("S", "Juliol 2019", 1, steps(
    dsc([["2", "0", "3"], ["1", "-2", "2"], ["3", "-1", "5"]], "2(-10+2)-0+3(-1+6)=-1", [], AL),
    "<strong>Apartat a).</strong> " + cdcase([], AL),
    crit(AL, "-1", [[2, 0, 3, -1], [1, -2, 2, 5], [3, -1, 5, 0]]).replace("<strong>Cas", "<strong>Apartat b)"),
    r"<strong>Apartat c).</strong> Resolem en general per Cramer ($|A|=-1$): $$x=\frac{\begin{vmatrix}\alpha&0&3\\5&-2&2\\\alpha+1&-1&5\end{vmatrix}}{-1}=2\alpha+9,\quad y=\frac{\begin{vmatrix}2&\alpha&3\\1&5&2\\3&\alpha+1&5\end{vmatrix}}{-1}=-4,\quad z=\frac{\begin{vmatrix}2&0&\alpha\\1&-2&5\\3&-1&\alpha+1\end{vmatrix}}{-1}=-\alpha-6$$ $$x+y+z=2\alpha+9-4-\alpha-6=\alpha-1=0\Rightarrow\alpha=1$$",
) + res(r"a) Per a tot $\alpha\in\mathbb{R}$. &nbsp; b) $(7,-4,-5)$. &nbsp; c) $\alpha=1$."))
for al_ in (-1, 1, 3):
    assert mul(inv(M([2, 0, 3], [1, -2, 2], [3, -1, 5])), M([al_], [5], [al_ + 1])) == M([2 * al_ + 9], [-4], [-al_ - 6])

# ---------------- Juliol 2020 (1) ----------------
sol("S", "Juliol 2020", 1, steps(
    dsc([["1", "1", "a"], ["1", "a", "1"], ["a", "1", "1"]], "(a-1)-(1-a)+a(1-a^2)=-a^3+3a-2=-(a-1)^2(a+2)", ["1", "-2"], "a"),
    cdcase(["1", "-2"], "a") + r" Per Cramer: $x=\frac{2(a-1)(a+2)}{-(a-1)^2(a+2)}=\frac{-2}{a-1}$, $\ y=z=\frac{-(a-1)(a+2)}{-(a-1)^2(a+2)}=\frac1{a-1}$.",
    crit("a", "1", [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, -2]]),
    crit("a", "-2", [[1, 1, -2, 1], [1, -2, 1, 1], [-2, 1, 1, -2]]).replace("<strong>Cas", "<strong>Apartat b)"),
    r"<strong>Apartat c) $a=0$.</strong> És un cas CD: $x=\frac{-2}{-1}=2$, $y=z=\frac1{-1}=-1$. Comprovació: $2-1=1$ ✓, $2-1=1$ ✓, $-1-1=-2$ ✓.",
) + res(r"a) CD si $a\neq1,-2$; CI si $a=-2$; incompatible si $a=1$. &nbsp; b) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; c) $(2,-1,-1)$." % tuple(G([[1, 1, -2, 1], [1, -2, 1, 1], [-2, 1, 1, -2]])[1])))

# ---------------- Setembre 2020 (1) ----------------
sol("S", "Setembre 2020", 1, steps(
    dsc([["1", "a", "2"], ["1", "-3", "a"], ["1", "1", "2"]], "(-6-a)-a(2-a)+2(1+3)=a^2-3a+2=(a-1)(a-2)", ["1", "2"], "a"),
    cdcase(["1", "2"], "a"),
    crit("a", "1", [[1, 1, 2, 3], [1, -3, 1, -2], [1, 1, 2, 1]]),
    crit("a", "2", [[1, 2, 2, 3], [1, -3, 2, -2], [1, 1, 2, 2]]),
    r"<strong>Apartat b) $a=0$.</strong> És CD. Per Cramer ($|A|=2$): $$x=\frac{\begin{vmatrix}3&0&2\\-2&-3&0\\0&1&2\end{vmatrix}}{2}=\frac{-22}{2}=-11,\quad y=\frac{\begin{vmatrix}1&3&2\\1&-2&0\\1&0&2\end{vmatrix}}{2}=\frac{-6}{2}=-3,\quad z=\frac{\begin{vmatrix}1&0&3\\1&-3&-2\\1&1&0\end{vmatrix}}{2}=\frac{14}{2}=7$$",
) + res(r"a) Compatible si $a\neq1$ (CD si $a\neq1,2$; CI si $a=2$). &nbsp; b) $(-11,-3,7)$. &nbsp; c) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[1, 2, 2, 3], [1, -3, 2, -2], [1, 1, 2, 2]])[1])))
assert mul(inv(M([1, 0, 2], [1, -3, 0], [1, 1, 2])), M([3], [-2], [0])) == M([-11], [-3], [7])

# ---------------- Setembre 2020 (2) ----------------
A = M([1, 2, 0], [0, 1, 0], [0, 2, 1]); ih, Ai = inv_html(A)
A2 = mul(A, A)
assert Ai == add(sub(A2, sc(3, A)), sc(3, I(3)))
assert sub(add(sub(pw(A, 3), sc(3, A2)), sc(3, A)), I(3)) == sc(0, I(3))
sol("S", "Setembre 2020", 2, steps(
    "<strong>Apartat a).</strong>" + ih,
    r"<strong>Apartat b).</strong> De $A^3-3A^2+3A-I=0$: $$A^3-3A^2+3A=I\Rightarrow A\,(A^2-3A+3I)=I\Rightarrow A^{-1}=A^2-3A+3I$$ Per tant $a=-3$ i $b=3$. Comprovació: $A^2=%s$ i $A^2-3A+3I=%s=A^{-1}$ ✓." % (tx(A2), tx(Ai)),
    r"<strong>Apartat c).</strong> El sistema $(A-\lambda I)X=0$ és homogeni; té infinites solucions si i només si $|A-\lambda I|=0$: $$|A-\lambda I|=\begin{vmatrix}1-\lambda&2&0\\0&1-\lambda&0\\0&2&1-\lambda\end{vmatrix}=(1-\lambda)^3=0\iff\lambda=1$$",
    r"<strong>Cas $\lambda=1$.</strong> $A-I=\begin{pmatrix}0&2&0\\0&0&0\\0&2&0\end{pmatrix}$: el sistema es redueix a $2y=0$. Per tant $y=0$ i $x$, $z$ són lliures: $(x,y,z)=(t,0,s)$, $t,s\in\mathbb{R}$.",
) + res(r"a) $A^{-1}=%s$. &nbsp; b) $a=-3$, $b=3$. &nbsp; c) $\lambda=1$: $(x,y,z)=(t,0,s)$." % tx(Ai)))

# ---------------- Juny 2021 (1) ----------------
sol("S", "Juny 2021", 1, steps(
    dsc([["1", "1", "a+1"], ["1", "a-1", "2"], ["2", "a", "1"]], "[(a-1)-2a]-(1-4)+(a+1)[a-2(a-1)]=4-a^2=-(a-2)(a+2)", ["2", "-2"], "a"),
    cdcase(["2", "-2"], "a") + r" Per Cramer: $$x=\frac{(a-2)(2a+3)}{-(a-2)(a+2)}=-\frac{2a+3}{a+2},\qquad y=\frac{-3(a-2)}{-(a-2)(a+2)}=\frac{3}{a+2},\qquad z=\frac{-4(a-2)}{-(a-2)(a+2)}=\frac{4}{a+2}$$",
    crit("a", "2", [[1, 1, 3, 2], [1, 1, 2, 1], [2, 2, 1, -1]]),
    crit("a", "-2", [[1, 1, -1, 2], [1, -3, 2, 1], [2, -2, 1, -1]]),
) + res(r"a) CD si $a\neq\pm2$; CI si $a=2$; incompatible si $a=-2$. &nbsp; b) Si $a\neq\pm2$: $\left(-\frac{2a+3}{a+2},\frac3{a+2},\frac4{a+2}\right)$; si $a=2$: $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[1, 1, 3, 2], [1, 1, 2, 1], [2, 2, 1, -1]])[1])))

# ---------------- Juliol 2021 (1) ----------------
sol("S", "Juliol 2021", 1, steps(
    dsc([["2", "-1", "1"], ["1", "1", "3"], ["5", "-4", "m"]], "2(m+12)+(m-15)+(-4-5)=3m", ["0"], "m"),
    cdcase(["0"], "m") + r" Per Cramer: $x=\frac{m(m+8)}{3m}=\frac{m+8}3$, $\ y=\frac{-m(m-10)}{3m}=\frac{10-m}3$, $\ z=\frac{-6m}{3m}=-2$.",
    crit("m", "0", [[2, -1, 1, 0], [1, 1, 3, 0], [5, -4, 0, 0]]),
    r"<strong>Apartat b) $m=1$.</strong> $x=\frac{9}{3}=3$, $y=\frac93=3$, $z=-2$. Comprovació: $6-3-2=1$ ✓, $3+3-6=0$ ✓, $15-12-2=1$ ✓.",
) + res(r"a) CD si $m\neq0$; CI si $m=0$ (mai incompatible). &nbsp; b) $(3,3,-2)$. &nbsp; c) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[2, -1, 1, 0], [1, 1, 3, 0], [5, -4, 0, 0]])[1])))

# ---------------- Juliol 2021 (2) ----------------
A0 = M([1, 2, 3], [-1, 0, 1], [1, -2, 3]); ih, Ai = inv_html(A0, "A")
C = sc(16, Ai); assert mul(A0, C) == sc(16, I(3))
B = mul(M([1], [-1], [2]), M([1, 2, 3]))
sol("S", "Juliol 2021", 2, steps(
    r"<strong>Apartat a).</strong> $$|A|=\begin{vmatrix}1&2&3\\-1&a&1\\1&a^2-2&3\end{vmatrix}=\left[3a-(a^2-2)\right]-2(-3-1)+3\left[-(a^2-2)-a\right]=16-4a^2=-4(a-2)(a+2)$$ Si $a\neq\pm2$, $\operatorname{rg}(A)=3$. Si $a=\pm2$, $|A|=0$ i com que $\begin{vmatrix}1&3\\-1&1\end{vmatrix}=4\neq0$, $\operatorname{rg}(A)=2$.",
    r"<strong>Apartat b).</strong> $AC=16I\Rightarrow C=16A^{-1}$. Per a $a=0$:" + ih + r"$$C=16A^{-1}=%s$$" % tx(C),
    r"<strong>Apartat c).</strong> $$B=\begin{pmatrix}1\\-1\\2\end{pmatrix}\begin{pmatrix}1&2&3\end{pmatrix}=%s$$ Totes les files són proporcionals a $(1,2,3)$ i $B\neq0$: $\operatorname{rg}(B)=1$. El sistema és $$BX=\begin{pmatrix}1\\-1\\2\end{pmatrix}(x+2y+3z)=\begin{pmatrix}1\\-1\\2\end{pmatrix}\iff x+2y+3z=1$$ Per tant $\operatorname{rg}(B^*)=1=\operatorname{rg}(B)<3$: el sistema <strong>té solució</strong> (infinites): $(x,y,z)=(1-2t-3s,\ t,\ s)$." % tx(B),
) + res(r"a) $\operatorname{rg}A=3$ si $a\neq\pm2$; $\operatorname{rg}A=2$ si $a=\pm2$. &nbsp; b) $C=%s$. &nbsp; c) $\operatorname{rg}B=1$; el sistema és compatible indeterminat." % tx(C)))

# ---------------- Juliol 2022 (1) ----------------
sol("S", "Juliol 2022", 1, steps(
    dsc([["a", "1", "0"], ["1", "0", "1"], ["1", "a", "a-1"]], "a(0-a)-[(a-1)-1]=-a^2-a+2=-(a-1)(a+2)", ["1", "-2"], "a"),
    cdcase(["1", "-2"], "a") + r" Per Cramer: $x=\frac{1-a}{-(a-1)(a+2)}=\frac1{a+2}$, $\ y=\frac{-2(a-1)}{-(a-1)(a+2)}=\frac2{a+2}$, $\ z=\frac{-(a-1)(a+1)}{-(a-1)(a+2)}=\frac{a+1}{a+2}$.",
    crit("a", "1", [[1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 0, 1]]),
    crit("a", "-2", [[-2, 1, 0, 1], [1, 0, 1, 1], [1, -2, -3, -2]]),
) + res(r"a) CD si $a\neq1,-2$; CI si $a=1$; incompatible si $a=-2$. &nbsp; b) Si $a\neq1,-2$: $\left(\frac1{a+2},\frac2{a+2},\frac{a+1}{a+2}\right)$; si $a=1$: $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 0, 1]])[1])))

# ---------------- Juny 2024 (1) ----------------
sol("S", "Juny 2024", 1, steps(
    dsc([["-1", "1", "1"], ["2", "m", "-1"], ["m-1", "3", "-1"]], "-(-m+3)-[-2+(m-1)]+[6-m(m-1)]=-m^2+m+6=-(m-3)(m+2)", ["3", "-2"], "m"),
    cdcase(["3", "-2"], "m"),
    crit("m", "3", [[-1, 1, 1, 3], [2, 3, -1, 9], [2, 3, -1, 9]]),
    crit("m", "-2", [[-1, 1, 1, -2], [2, -2, -1, -6], [-3, 3, -1, 4]]),
) + res(r"a) CD si $m\neq3,-2$; CI si $m=3$; incompatible si $m=-2$. &nbsp; b) $m=3$: $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$." % tuple(G([[-1, 1, 1, 3], [2, 3, -1, 9], [2, 3, -1, 9]])[1])))

# ---------------- Juny 2025 (1) ----------------
sol("S", "Juny 2025", 1, steps(
    dsc([["3", "-2", "-3"], ["2", "a", "-5"], ["1", "1", "2"]], "3(2a+5)+2(4+5)-3(2-a)=9a+27=9(a+3)", ["-3"], "a"),
    cdcase(["-3"], "a") + r" Per Cramer, $|A_x|=9(a+3)$, $|A_y|=0$ i $|A_z|=9(a+3)$, així que la solució és $(1,0,1)$ per a tot $a\neq-3$.",
    crit("a", "-3", [[3, -2, -3, 0], [2, -3, -5, -3], [1, 1, 2, 3]]).replace("<strong>Cas", "<strong>Apartat b)"),
    r"<strong>Apartat c) $a=0$.</strong> És un cas CD: $(x,y,z)=(1,0,1)$. Comprovació: $3-3=0$ ✓, $2-5=-3$ ✓, $1+2=3$ ✓.",
) + res(r"a) CD si $a\neq-3$; CI si $a=-3$ (mai incompatible). &nbsp; b) $(x,y,z)=(%s,\ %s,\ %s)$, $t\in\mathbb{R}$. &nbsp; c) $(1,0,1)$." % tuple(G([[3, -2, -3, 0], [2, -3, -5, -3], [1, 1, 2, 3]])[1])))
assert mul(inv(M([3, -2, -3], [2, 0, -5], [1, 1, 2])), M([0], [-3], [3])) == M([1], [0], [1])

# ---------------- Juny 2025 (2) ----------------
sol("S", "Juny 2025", 2, steps(
    dsc([["3", "4", AL], ["-2", "1", "1"], ["2", "-1", AL]], r"3(\alpha+1)-4(-2\alpha-2)+\alpha(2-2)=11\alpha+11=11(\alpha+1)", ["-1"], AL),
    cdcase(["-1"], AL),
    crit(AL, "-1", [[3, 4, -1, 30], [-2, 1, 1, 4], [2, -1, -1, 10]]),
    r"<strong>Apartat b).</strong> Per a $\alpha\neq-1$, per Cramer ($|A|=11(\alpha+1)$): $$x=\frac{\begin{vmatrix}30&4&\alpha\\4&1&1\\10&-1&\alpha\end{vmatrix}}{11(\alpha+1)}=\frac{70}{11(\alpha+1)},\quad y=\frac{\begin{vmatrix}3&30&\alpha\\-2&4&1\\2&10&\alpha\end{vmatrix}}{11(\alpha+1)}=\frac{2(22\alpha+15)}{11(\alpha+1)},\quad z=\frac{\begin{vmatrix}3&4&30\\-2&1&4\\2&-1&10\end{vmatrix}}{11(\alpha+1)}=\frac{154}{11(\alpha+1)}=\frac{14}{\alpha+1}$$ Com que són quantitats en kg, en el context del problema cal a més que siguen no negatives, cosa que passa si $\alpha>-1$ i $22\alpha+15\geq0$, és a dir, $\alpha\geq-\frac{15}{22}$.",
) + res(r"a) CD si $\alpha\neq-1$; incompatible si $\alpha=-1$. &nbsp; b) $x=\frac{70}{11(\alpha+1)}$, $y=\frac{2(22\alpha+15)}{11(\alpha+1)}$, $z=\frac{14}{\alpha+1}$ (kg)."))
for al_ in (0, 1, 3):
    assert mul(inv(M([3, 4, al_], [-2, 1, 1], [2, -1, al_])), M([30], [4], [10])) == M([Fr(70, 11 * (al_ + 1))], [Fr(2 * (22 * al_ + 15), 11 * (al_ + 1))], [Fr(14, al_ + 1)])

# ---------------- Juny 2025 (3) ----------------
sol("S", "Juny 2025", 3, steps(
    dsc([["1", "-a", "-1"], ["a", "-1", "1"], ["a", "1", "0"]], "(0-1)+a(0-a)-(a+a)=-a^2-2a-1=-(a+1)^2", ["-1"], "a"),
    cdcase(["-1"], "a"),
    crit("a", "-1", [[1, 1, -1, 1], [-1, -1, 1, -1], [-1, 1, 0, -1]]),
    r"<strong>Apartat b).</strong> Per a $a\neq-1$, per Cramer ($|A|=-(a+1)^2$): $$x=\frac{\begin{vmatrix}-a&-a&-1\\a&-1&1\\a&1&0\end{vmatrix}}{-(a+1)^2}=\frac{-a(a+1)}{-(a+1)^2}=\frac{a}{a+1},\quad y=\frac{\begin{vmatrix}1&-a&-1\\a&a&1\\a&a&0\end{vmatrix}}{-(a+1)^2}=\frac{a}{a+1},\quad z=\frac{\begin{vmatrix}1&-a&-a\\a&-1&a\\a&1&a\end{vmatrix}}{-(a+1)^2}=\frac{2a}{a+1}$$",
) + res(r"a) CD si $a\neq-1$; CI si $a=-1$. &nbsp; b) $\left(\frac{a}{a+1},\frac{a}{a+1},\frac{2a}{a+1}\right)$."))
for a_ in (0, 1, 2):
    assert mul(inv(M([1, -a_, -1], [a_, -1, 1], [a_, 1, 0])), M([-a_], [a_], [a_])) == M([Fr(a_, a_ + 1)], [Fr(a_, a_ + 1)], [Fr(2 * a_, a_ + 1)])

# ---------------- Juliol 2025 (1) ----------------
sol("S", "Juliol 2025", 1, steps(
    dsc([["3", "1", "2"], ["1+a", "2", "1"], ["a", "-1", "1"]], "3(2+1)-[(1+a)-a]+2[-(1+a)-2a]=9-1-2-6a=6-6a=-6(a-1)", ["1"], "a"),
    cdcase(["1"], "a"),
    crit("a", "1", [[3, 1, 2, 0], [2, 2, 1, 1], [1, -1, 1, 0]]),
    r"<strong>Apartat b).</strong> Per a $a\neq1$, per Cramer ($|A|=-6(a-1)$): $$x=\frac{\begin{vmatrix}1-a&1&2\\a&2&1\\1-a&-1&1\end{vmatrix}}{-6(a-1)}=\frac{-3a}{-6(a-1)}=\frac{a}{2(a-1)},\qquad y=\frac{\begin{vmatrix}3&1-a&2\\1+a&a&1\\a&1-a&1\end{vmatrix}}{-6(a-1)}=\frac{-4a^2+7a-2}{-6(a-1)}=\frac{4a^2-7a+2}{6(a-1)}$$ $$z=\frac{\begin{vmatrix}3&1&1-a\\1+a&2&a\\a&-1&1-a\end{vmatrix}}{-6(a-1)}=\frac{5a^2-5a+4}{-6(a-1)}=-\frac{5a^2-5a+4}{6(a-1)}$$",
) + res(r"a) CD si $a\neq1$; incompatible si $a=1$. &nbsp; b) $\left(\frac{a}{2(a-1)},\ \frac{4a^2-7a+2}{6(a-1)},\ -\frac{5a^2-5a+4}{6(a-1)}\right)$."))
for a_ in (0, 2, 3):
    assert mul(inv(M([3, 1, 2], [1 + a_, 2, 1], [a_, -1, 1])), M([1 - a_], [a_], [1 - a_])) == M([Fr(a_, 2 * (a_ - 1))], [Fr(4 * a_ * a_ - 7 * a_ + 2, 6 * (a_ - 1))], [Fr(-(5 * a_ * a_ - 5 * a_ + 4), 6 * (a_ - 1))])

# ---------------- Juny 2026 (1) ----------------
sol("S", "Juny 2026", 1, steps(
    r"<strong>El sistema.</strong> $Tv=u$ és $$%s$$" % sysm("2x+my&=4", "mx+2y&=4", "z&=-2"),
    dsc([["2", "m", "0"], ["m", "2", "0"], ["0", "0", "1"]], "1\\cdot(4-m^2)=-(m-2)(m+2)", ["2", "-2"], "m"),
    cdcase(["2", "-2"], "m"),
    crit("m", "2", [[2, 2, 0, 4], [2, 2, 0, 4], [0, 0, 1, -2]]),
    crit("m", "-2", [[2, -2, 0, 4], [-2, 2, 0, 4], [0, 0, 1, -2]]),
    crit("m", "-1", [[2, -1, 0, 4], [-1, 2, 0, 4], [0, 0, 1, -2]]).replace("<strong>Cas", "<strong>Apartat b)"),
    r"<strong>Apartat c).</strong> Per a $m=2$: $$|T-\alpha I|=\begin{vmatrix}2-\alpha&2&0\\2&2-\alpha&0\\0&0&1-\alpha\end{vmatrix}=(1-\alpha)\left[(2-\alpha)^2-4\right]=(1-\alpha)(\alpha^2-4\alpha)=-\alpha(\alpha-1)(\alpha-4)$$ S'anul·la per a $\alpha=0$, $\alpha=1$ i $\alpha=4$.",
) + res(r"a) CD si $m\neq\pm2$; CI si $m=2$; incompatible si $m=-2$. &nbsp; b) $v=(4,4,-2)$. &nbsp; c) $\alpha=0,\ 1,\ 4$."))
assert G([[2, -1, 0, 4], [-1, 2, 0, 4], [0, 0, 1, -2]])[1] == [4, 4, -2]

# ---------------- Juny 2026 extra (1) ----------------
sol("S", "Juny 2026 extra", 1, steps(
    dsc([[AL, "1", "-1"], ["1", AL, "1"], ["-1", "1", AL]], r"\alpha(\alpha^2-1)-(\alpha+1)-(1+\alpha)=\alpha^3-3\alpha-2=(\alpha-2)(\alpha+1)^2", ["2", "-1"], AL),
    cdcase(["2", "-1"], AL),
    crit(AL, "2", [[2, 1, -1, 0], [1, 2, 1, 1], [-1, 1, 2, 2]]),
    crit(AL, "-1", [[-1, 1, -1, 0], [1, -1, 1, 1], [-1, 1, -1, 2]]),
    r"<strong>Apartat b).</strong> És compatible només si $\alpha\neq2,-1$ (determinat). Per Cramer, amb $|A|=(\alpha-2)(\alpha+1)^2$: $$x=\frac{\begin{vmatrix}0&1&-1\\1&\alpha&1\\2&1&\alpha\end{vmatrix}}{|A|}=\frac{\alpha+1}{|A|}=\frac{1}{(\alpha-2)(\alpha+1)},\quad y=\frac{\begin{vmatrix}\alpha&0&-1\\1&1&1\\-1&2&\alpha\end{vmatrix}}{|A|}=\frac{(\alpha-3)(\alpha+1)}{|A|}=\frac{\alpha-3}{(\alpha-2)(\alpha+1)}$$ $$z=\frac{\begin{vmatrix}\alpha&1&0\\1&\alpha&1\\-1&1&2\end{vmatrix}}{|A|}=\frac{(\alpha+1)(2\alpha-3)}{|A|}=\frac{2\alpha-3}{(\alpha-2)(\alpha+1)}$$",
) + res(r"a) CD si $\alpha\neq2,-1$; incompatible si $\alpha=2$ o $\alpha=-1$. &nbsp; b) $\left(\frac{1}{(\alpha-2)(\alpha+1)},\frac{\alpha-3}{(\alpha-2)(\alpha+1)},\frac{2\alpha-3}{(\alpha-2)(\alpha+1)}\right)$."))
for al_ in (0, 1, 3):
    d_ = (al_ - 2) * (al_ + 1)
    assert mul(inv(M([al_, 1, -1], [1, al_, 1], [-1, 1, al_])), M([0], [1], [2])) == M([Fr(1, d_)], [Fr(al_ - 3, d_)], [Fr(2 * al_ - 3, d_)])

# ---------------- Juliol 2026 (1) ----------------
sol("S", "Juliol 2026", 1, steps(
    r"<strong>Plantegem el sistema.</strong> $$%s$$" % sysm("x+3y+z&=5", r"\alpha x+2z&=0", r"\alpha y-z&=0"),
    dsc([["1", "3", "1"], [AL, "0", "2"], ["0", AL, "-1"]], r"(0-2\alpha)-3(-\alpha-0)+\alpha^2=\alpha^2+\alpha=\alpha(\alpha+1)", ["0", "-1"], AL),
    cdcase(["0", "-1"], AL) + " (una única configuració d'equilibri).",
    crit(AL, "0", [[1, 3, 1, 5], [0, 0, 2, 0], [0, 0, -1, 0]]) + " (infinites configuracions d'equilibri)",
    crit(AL, "-1", [[1, 3, 1, 5], [-1, 0, 2, 0], [0, -1, -1, 0]]) + " (cap configuració d'equilibri)",
    r"<strong>Apartat b).</strong> Per a $\alpha\neq-1$ i $\alpha\neq0$, per Cramer ($|A|=\alpha(\alpha+1)$): $$x=\frac{\begin{vmatrix}5&3&1\\0&0&2\\0&\alpha&-1\end{vmatrix}}{\alpha(\alpha+1)}=\frac{-10\alpha}{\alpha(\alpha+1)}=\frac{-10}{\alpha+1},\quad y=\frac{\begin{vmatrix}1&5&1\\\alpha&0&2\\0&0&-1\end{vmatrix}}{\alpha(\alpha+1)}=\frac{5\alpha}{\alpha(\alpha+1)}=\frac{5}{\alpha+1},\quad z=\frac{\begin{vmatrix}1&3&5\\\alpha&0&0\\0&\alpha&0\end{vmatrix}}{\alpha(\alpha+1)}=\frac{5\alpha}{\alpha+1}$$ Per a $\alpha=0$ les solucions són les de dalt: $z=0$, $x=5-3t$, $y=t$.",
) + res(r"a) Solució única si $\alpha\neq0,-1$; infinites si $\alpha=0$; cap si $\alpha=-1$. &nbsp; b) $x=\frac{-10}{\alpha+1},\ y=\frac5{\alpha+1},\ z=\frac{5\alpha}{\alpha+1}$ (si $\alpha=0$: $(5-3t,\,t,\,0)$)."))
for al_ in (1, 2, -2):
    assert mul(inv(M([1, 3, 1], [al_, 0, 2], [0, al_, -1])), M([5], [0], [0])) == M([Fr(-10, al_ + 1)], [Fr(5, al_ + 1)], [Fr(5 * al_, al_ + 1)])

# ---------------- Juliol 2026 (2) ----------------
A = M([2, -1], [1, 1]); B = M([5, -2], [2, 3]); D = sub(A, B)
ih, Di = inv_html(D, "(A-B)")
X = mul(Di, M([1], [0])); assert mul(A, X) == add(mul(B, X), M([1], [0]))
assert det(A) == 3 and det(B) == 19
assert add(sc(-2, A), B) == I(2)
sol("S", "Juliol 2026", 2, steps(
    r"<strong>Apartat a).</strong> $$Ax=Bx+b\Rightarrow Ax-Bx=b\Rightarrow(A-B)x=b,\qquad A-B=%s$$" % tx(D) + ih + r"$$x=(A-B)^{-1}b=%s\begin{pmatrix}1\\0\end{pmatrix}=%s$$" % (nice(Di), nice(X)),
    r"<strong>Apartat b).</strong> $|A|=2+1=3$, $|B|=15+4=19$ i, com que les matrius són $2\times2$, $|2B|=2^2|B|=76$: $$\det\left(A^5(2B)^{-1}\right)=|A|^5\cdot\frac{1}{|2B|}=\frac{3^5}{76}=\frac{243}{76}$$",
    r"<strong>Apartat c).</strong> $$\alpha A+\beta B=\begin{pmatrix}2\alpha+5\beta&-\alpha-2\beta\\\alpha+2\beta&\alpha+3\beta\end{pmatrix}=\begin{pmatrix}1&0\\0&1\end{pmatrix}$$ De $\alpha+2\beta=0$, $\alpha=-2\beta$. Substituint en $2\alpha+5\beta=1$: $\beta=1$, $\alpha=-2$. Comprovem la 4a equació: $\alpha+3\beta=-2+3=1$ ✓.",
) + res(r"a) $x=\left(-\frac27,\frac17\right)$. &nbsp; b) $\frac{243}{76}$. &nbsp; c) $\alpha=-2$, $\beta=1$."))
assert X == M([Fr(-2, 7)], [Fr(1, 7)])
