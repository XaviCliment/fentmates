  /* ======================= ginys nous de 4t ESO A, unitat 4 ======================= */

  /* ---------- polinomis: m.c.d. i m.c.m. ---------- */
  function pMonic(p) { p = pTrim(p); var l = p[p.length - 1]; return l.zero() ? p : pScale(p, F1.div(l)); }
  function pGcd(a, b) {
    a = pTrim(a); b = pTrim(b);
    while (pDeg(b) >= 0) { var r = pDivide(a, b).r; a = b; b = r; }
    return pDeg(a) <= 0 ? [F1] : pMonic(a);
  }
  function pLcm(a, b) { var g = pGcd(a, b); return pMonic(pDivide(pMul(a, b), g).q); }
  function ilcm(a, b) { return a / gcd(a, b) * b; }
  function coefLcm(p) { var L = 1; p.forEach(function (c) { L = ilcm(L, c.d); }); return L; }
  function pIsConst(p) { return pDeg(p) <= 0; }
  function pEqP(a, b) { return pDeg(pSub(a, b)) < 0; }

  /* ---------- analitzador d'expressions racionals en x ---------- */
  // cada node: { n, d } (fracció de polinomis) i t (TeX tal com s'ha escrit)
  function lexE(s) {
    s = String(s).replace(/[−–]/g, "-").replace(/[·×]/g, "*").replace(/:/g, "/").replace(/²/g, "^2").replace(/³/g, "^3").replace(/⁴/g, "^4")
      .replace(/[\[{]/g, "(").replace(/[\]}]/g, ")").replace(/X/g, "x").replace(/\s+/g, "");
    var out = [], i = 0, m;
    while (i < s.length) {
      var c = s.charAt(i);
      if ((m = /^\d+(?:[.,]\d+)?/.exec(s.slice(i)))) { out.push({ t: "n", s: m[0] }); i += m[0].length; }
      else if (c === "x") { out.push({ t: "x" }); i++; }
      else if ("+-*/^()".indexOf(c) >= 0) { out.push({ t: c }); i++; }
      else return null;
    }
    return out;
  }
  function numFr(s) { s = s.replace(",", "."); var k = s.indexOf("."); return k < 0 ? new Fr(+s) : new Fr(+s.replace(".", ""), Math.pow(10, s.length - k - 1)); }
  function rfRed(r) {
    if (pDeg(r.d) >= 1) { var g = pGcd(r.n, r.d); if (pDeg(g) >= 1) { r = { n: pDivide(r.n, g).q, d: pDivide(r.d, g).q }; } }
    if (pIsConst(r.d)) { r = { n: pScale(r.n, F1.div(r.d[0])), d: [F1] }; }
    return r;
  }
  function rfAdd(a, b, s) {
    var nb = s < 0 ? pScale(b.n, FM1) : b.n;
    if (pEqP(a.d, b.d)) return rfRed({ n: pAdd(a.n, nb), d: a.d });
    return rfRed({ n: pAdd(pMul(a.n, b.d), pMul(nb, a.d)), d: pMul(a.d, b.d) });
  }
  function rfMul(a, b) { return rfRed({ n: pMul(a.n, b.n), d: pMul(a.d, b.d) }); }
  function rfDiv(a, b) { if (pDeg(b.n) < 0) throw new Error("div0"); return rfRed({ n: pMul(a.n, b.d), d: pMul(a.d, b.n) }); }
  function parseSide(s, info) {
    var tk = lexE(s), i = 0;
    if (!tk || !tk.length) return null;
    function pk() { return tk[i] ? tk[i].t : null; }
    function strip(nd) { return nd.par ? nd.inner : nd.t; }
    function expr() {
      var a = term();
      while (pk() === "+" || pk() === "-") {
        var o = tk[i++].t, b = term();
        a = { n: null, rf: rfAdd(a.rf, b.rf, o === "-" ? -1 : 1), t: a.t + o + b.t };
      }
      return a;
    }
    function term() {
      var a = unary();
      for (;;) {
        var p = pk();
        if (p === "*" || p === "/") {
          i++; var b = unary();
          if (p === "*") a = { rf: rfMul(a.rf, b.rf), t: a.t + "\\cdot " + b.t };
          else {
            if (pDeg(b.rf.n) >= 1 || pDeg(b.rf.d) >= 1) info.dens.push(b.rf.n);
            else { var c = b.rf.n[0]; if (c.zero()) throw new Error("div0"); info.m = ilcm(info.m, Math.abs(c.n)); }
            a = { rf: rfDiv(a.rf, b.rf), t: "\\dfrac{" + strip(a) + "}{" + strip(b) + "}" };
          }
        } else if (p === "x" || p === "(" || p === "n") {
          var b2 = unary(), sep = /\d$/.test(a.t) && /^\d/.test(b2.t) ? "\\cdot " : "";
          a = { rf: rfMul(a.rf, b2.rf), t: a.t + sep + b2.t };
        } else return a;
      }
    }
    function unary() {
      if (pk() === "-") { i++; var a = unary(); return { rf: { n: pScale(a.rf.n, FM1), d: a.rf.d }, t: "-" + a.t }; }
      if (pk() === "+") { i++; return unary(); }
      return power();
    }
    function power() {
      var a = atom();
      if (pk() === "^") {
        i++; var e = tk[i++]; if (!e || e.t !== "n" || /[.,]/.test(e.s) || +e.s > 6) throw new Error("exp");
        var r = { n: [F1], d: [F1] }; for (var k = 0; k < +e.s; k++) r = rfMul(r, a.rf);
        a = { rf: r, t: a.t + "^{" + e.s + "}" };
      }
      return a;
    }
    function atom() {
      var q = tk[i++]; if (!q) throw new Error("end");
      if (q.t === "n") return { rf: { n: [numFr(q.s)], d: [F1] }, t: q.s.replace(/[.,]/, lang === "en" ? "." : "{,}") };
      if (q.t === "x") return { rf: { n: [F0, F1], d: [F1] }, t: "x" };
      if (q.t === "(") { var e = expr(); if (pk() !== ")") throw new Error("par"); i++; return { rf: e.rf, t: "\\left(" + e.t + "\\right)", par: true, inner: e.t }; }
      throw new Error("tok");
    }
    try { var r = expr(); if (i < tk.length) return null; return r; } catch (e) { return null; }
  }
  function parseEqn(s) {
    s = String(s || ""); var parts = s.split("="); if (parts.length !== 2) return null;
    var info = { dens: [], m: 1 }, L = parseSide(parts[0], info), R = parseSide(parts[1], info);
    if (!L || !R) return null;
    return { L: L, R: R, dens: info.dens, m: info.m };
  }

  /* ---------- resolució d'una equació polinòmica P = 0, amb els passos ---------- */
  function solvePoly(P, rows) {
    var d = pDeg(P), out = { roots: [] }, S = t3("Solució", "Solución", "Solution"), SS = t3("Solucions", "Soluciones", "Solutions");
    function add(fr, tx) { out.roots.push({ v: fr.val ? fr.val() : fr, tex: tx }); }
    if (d === -Infinity) { out.all = true; rows.push(["", t3("La x desapareix i queda una igualtat certa: es compleix per a qualsevol x.", "La x desaparece y queda una igualdad cierta: se cumple para cualquier x.", "x disappears and a true equality is left: it holds for every x.")]); return out; }
    if (d === 0) { out.none = true; rows.push(["", t3("La x desapareix i queda una igualtat falsa: és impossible.", "La x desaparece y queda una igualdad falsa: es imposible.", "x disappears and a false equality is left: it's impossible.")]); return out; }
    if (d >= 2 && P[d].sgn() < 0) { P = pScale(P, FM1); rows.push([t3("Canviem el signe", "Cambiamos el signo", "Change the sign"), tex(pTex(P) + "=0")]); }
    var I = intForm(P);
    if (d >= 2 && !I.k.eq(F1) && I.k.d === 1 && I.k.n > 1) { P = I.P; rows.push([t3("Simplifiquem", "Simplificamos", "Simplify") + " (÷" + I.k.n + ")", tex(pTex(P) + "=0")]); }
    if (d === 1) {
      var a = P[1], b = P[0], r = b.neg().div(a);
      rows.push([t3("Aïllem la x", "Despejamos la x", "Isolate x"), tex(a.eq(F1) ? "x=" + frT(r) : pTex([F0, a]) + "=" + frT(b.neg()) + "\\Rightarrow x=\\dfrac{" + frT(b.neg()) + "}{" + frT(a) + "}=" + frT(r))]);
      add(r, frT(r));
    } else if (d === 2) {
      var A = P[2], B = P[1], C = P[0];
      if (B.zero() && C.zero()) { rows.push([t3("Incompleta", "Incompleta", "Incomplete"), tex(pTex([F0, F0, A]) + "=0\\Rightarrow x^2=0\\Rightarrow x=0") + " (" + t3("doble", "doble", "double") + ")"]); add(F0, "0"); }
      else if (C.zero()) {
        var r2 = B.neg().div(A), f = pTex([B, A]);
        rows.push([t3("Incompleta: factor comú", "Incompleta: factor común", "Incomplete: common factor"), tex("x\\left(" + f + "\\right)=0\\Rightarrow x=0,\\ \\ " + f + "=0\\Rightarrow x=" + frT(r2))]);
        add(F0, "0"); add(r2, frT(r2));
      } else if (B.zero()) {
        var q = C.neg().div(A), Q0 = quadRoots(A, F0, C);
        if (q.sgn() < 0) { rows.push([t3("Incompleta", "Incompleta", "Incomplete"), tex("x^2=" + frT(q)) + ": " + t3("un quadrat no pot ser negatiu", "un cuadrado no puede ser negativo", "a square can't be negative")]); out.none = true; }
        else { rows.push([t3("Incompleta", "Incompleta", "Incomplete"), tex("x^2=" + frT(q) + "\\Rightarrow x=\\pm\\sqrt{" + frT(q) + "}=\\pm" + Q0.roots[1].tex)]); Q0.roots.forEach(function (x) { add(x.v, x.tex); }); }
      } else {
        var Q = quadRoots(A, B, C);
        rows.push([t3("Discriminant", "Discriminante", "Discriminant"), tex("\\Delta=" + frP(B) + "^2-4\\cdot" + frP(A) + "\\cdot" + frP(C) + "=" + frT(Q.D)) + (Q.kind === "none" ? " " + t3("< 0", "< 0", "< 0") : "")]);
        if (Q.kind === "none") { rows.push(["", t3("Δ < 0: no té solucions reals", "Δ < 0: no tiene soluciones reales", "Δ < 0: no real solutions")]); out.none = true; }
        else if (Q.kind === "double") { rows.push([t3("Fórmula", "Fórmula", "Formula"), tex("x=\\dfrac{" + frT(B.neg()) + "}{" + frT(A.mul(2)) + "}=" + Q.roots[0].tex) + " (" + t3("doble", "doble", "double") + ")"]); add(Q.roots[0].v, Q.roots[0].tex); }
        else { rows.push([t3("Fórmula", "Fórmula", "Formula"), tex(quadFormulaT(A, B, C, Q) + "\\Rightarrow " + Q.roots.map(function (x) { return "x=" + x.tex; }).join(",\\ \\ "))]); Q.roots.forEach(function (x) { add(x.v, x.tex); }); }
      }
    } else {
      var F = factorPoly(P);
      rows.push([t3("Factoritzem", "Factorizamos", "Factorise"), tex(facTex(F) + "=0")]);
      F.roots.forEach(function (x) { add(x.v, x.tex); });
      if (!F.roots.length) out.none = true;
    }
    return out;
  }

  /* ---------- 4.1, 4.4 i 4.7 resolutor pas a pas ---------- */
  var SOLVE_PRE = {
    "w-eq1": ["2(x-3)-(x+4)=3x-20", "(x+1)/2-(x-2)/3=2", "(3x-1)/4-(x+2)/6=x/3-1/2", "2(x+3)/5-(x-1)/2=(1-x)/10", "3(x-1)-2x=x-3"],
    "w-eq2": ["(x+2)^2-4x=13", "(x-3)(x+3)=2(x^2-5)", "(2x-1)^2-(x+1)(x-1)=6", "x^2/3-x/2=3/2", "(x+3)(x-3)/4-(x-1)^2/2=-2"],
    "w-eqr": ["3/x+2=5", "1/x+1/(x+2)=3/4", "x/(x-1)+2/(x+1)=2/(x^2-1)", "x/(x-2)-2/(x-2)=3", "(x+1)/x-x/(x+1)=5/6"]
  };
  function wSolve() { Object.keys(SOLVE_PRE).forEach(function (id) { solveW(byId(id), SOLVE_PRE[id]); }); }
  function solveW(w, PRE) {
    if (!w) return;
    var info = w.querySelector(".info"), inp = $(w, "e");
    presetBtns($(w, "pre"), function () { var e = parseEqn; return PRE.map(function (p) { var q = e(p); return q ? tex(q.L.t + "=" + q.R.t) : p; }); }, function (i) { inp.value = PRE[i]; draw(); });
    function draw() {
      var Q = parseEqn(inp.value);
      inp.classList.toggle("bad", !Q);
      if (!Q) { info.innerHTML = t3("Escriu una equació amb un signe =, per exemple <code>(x+1)/2-3(x-2)=x</code>. Fes servir <code>/</code> per a les fraccions i <code>^</code> per a les potències.", "Escribe una ecuación con un signo =, por ejemplo <code>(x+1)/2-3(x-2)=x</code>. Usa <code>/</code> para las fracciones y <code>^</code> para las potencias.", "Type an equation with one = sign, e.g. <code>(x+1)/2-3(x-2)=x</code>. Use <code>/</code> for fractions and <code>^</code> for powers."); return; }
      var rows = [[t3("Equació", "Ecuación", "Equation"), tex(Q.L.t + "=" + Q.R.t)]], L = Q.L.rf, R = Q.R.rf, bad = [], M = [F1];
      if (Q.dens.length) {
        var seen = [];
        Q.dens.forEach(function (D) { var I = intForm(D).P; if (!seen.some(function (S) { return pEqP(S, I); })) seen.push(I); });
        seen.forEach(function (D) { factorPoly(D).roots.forEach(function (r) { if (!bad.some(function (b) { return Math.abs(b.v - r.v) < 1e-9; })) bad.push(r); }); M = pLcm(M, D); });
        bad.sort(function (a, b) { return a.v - b.v; });
        rows.push([t3("Valors prohibits", "Valores prohibidos", "Excluded values"), bad.length ? tex("x\\neq " + bad.map(function (b) { return b.tex; }).join(",\\ ")) + " <small>(" + t3("anul·len un denominador", "anulan un denominador", "they make a denominator zero") + ")</small>" : "—"]);
      }
      function times(S) { var q = pDivide(pMul(S.n, M), S.d); return pDeg(q.r) < 0 ? q.q : null; }
      var Lp = times(L), Rp = times(R);
      if (!Lp || !Rp) { M = pLcm(pLcm(M, L.d), R.d); Lp = times(L); Rp = times(R); }
      var k = ilcm(ilcm(coefLcm(Lp), coefLcm(Rp)), Q.dens.length ? 1 : Q.m);
      k = ilcm(k, coefLcm(M)); M = pScale(M, new Fr(k)); Lp = pScale(Lp, new Fr(k)); Rp = pScale(Rp, new Fr(k));
      var I = intForm(M); if (I.k.sgn() < 0) { M = pScale(M, FM1); Lp = pScale(Lp, FM1); Rp = pScale(Rp, FM1); }
      if (pDeg(M) >= 1 || !M[0].eq(F1)) {
        var Mt = pDeg(M) >= 1 ? facTex(factorPoly(M)) : frT(M[0]);
        rows.push([t3("m.c.m. dels denominadors", "m.c.m. de los denominadores", "LCM of the denominators"), tex(Mt)]);
        rows.push([t3("Multipliquem per", "Multiplicamos por", "Multiply by") + " " + tex(Mt) + t3(" i reduïm", " y reducimos", " and simplify"), tex(pTex(Lp) + "=" + pTex(Rp))]);
      } else rows.push([t3("Traiem parèntesis i reduïm", "Quitamos paréntesis y reducimos", "Expand and simplify"), tex(pTex(Lp) + "=" + pTex(Rp))]);
      var P = pSub(Lp, Rp);
      rows.push([t3("Ho passem tot a un membre", "Lo pasamos todo a un miembro", "Move everything to one side"), tex(pTex(P) + "=0") + (pDeg(P) >= 1 ? " <small>(" + t3("grau ", "grado ", "degree ") + pDeg(P) + ")</small>" : "")]);
      var res = solvePoly(P, rows), good = [];
      if (res.all) {
        rows.push([t3("Solucions", "Soluciones", "Solutions"), "<strong>" + (bad.length ? t3("qualsevol nombre excepte ", "cualquier número excepto ", "any number except ") + tex(bad.map(function (b) { return b.tex; }).join(",\\ ")) : t3("infinites solucions (qualsevol nombre)", "infinitas soluciones (cualquier número)", "infinitely many solutions (any number)")) + "</strong>"]);
        info.innerHTML = kv(rows); return;
      }
      if (bad.length && res.roots.length) {
        var ch = [];
        res.roots.forEach(function (r) {
          var no = bad.some(function (b) { return Math.abs(b.v - r.v) < 1e-9; });
          ch.push(tex("x=" + r.tex) + ": " + (no ? ok(false) + " " + t3("anul·la un denominador, es descarta", "anula un denominador, se descarta", "makes a denominator zero, rejected") : ok(true) + " " + t3("val", "vale", "valid")));
          if (!no) good.push(r);
        });
        rows.push([t3("Comprovació", "Comprobación", "Check"), ch.join("<br>")]);
      } else good = res.roots;
      rows.push([t3("Solució", "Solución", "Solution"), "<strong>" + (good.length ? tex(good.map(function (r) { return "x=" + r.tex; }).join(",\\quad ")) : t3("no té solució", "no tiene solución", "no solution")) + "</strong>"]);
      info.innerHTML = kv(rows);
    }
    inp.addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 4.2 i 4.5 entrenador de problemes ---------- */
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(L) { return L[Math.floor(Math.random() * L.length)]; }
  var PROB1 = [
    function () { var x = rnd(5, 40), S = 3 * x + 3; return { a: x,
      q: function () { return t3("La suma de tres nombres consecutius és " + S + ". Quins són? (escriu el menor)", "La suma de tres números consecutivos es " + S + ". ¿Cuáles son? (escribe el menor)", "Three consecutive numbers add up to " + S + ". What are they? (type the smallest)"); },
      s: function () { return [t3("Nombres: ", "Números: ", "Numbers: ") + tex("x,\\ x+1,\\ x+2"), tex("x+(x+1)+(x+2)=" + S + "\\Rightarrow 3x+3=" + S + "\\Rightarrow 3x=" + (S - 3) + "\\Rightarrow x=" + x), t3("Són ", "Son ", "They are ") + x + ", " + (x + 1) + t3(" i ", " y ", " and ") + (x + 2) + "."]; } }; },
    function () { var b = rnd(4, 15), x = rnd(2, 20), a = 2 * b + x; return { a: x,
      q: function () { return t3("Una mare té " + a + " anys i el seu fill, " + b + ". D'ací a quants anys l'edat de la mare serà el doble de la del fill?", "Una madre tiene " + a + " años y su hijo, " + b + ". ¿Dentro de cuántos años la edad de la madre será el doble de la del hijo?", "A mother is " + a + " and her son is " + b + ". In how many years will the mother be twice as old as her son?"); },
      s: function () { return [t3("D'ací a x anys: mare ", "Dentro de x años: madre ", "In x years: mother ") + tex(a + "+x") + t3(", fill ", ", hijo ", ", son ") + tex(b + "+x"), tex(a + "+x=2(" + b + "+x)\\Rightarrow " + a + "+x=" + 2 * b + "+2x\\Rightarrow x=" + x), t3("D'ací a ", "Dentro de ", "In ") + x + t3(" anys.", " años.", " years.")]; } }; },
    function () { var k = rnd(2, 9), x = rnd(4, 30), P = 4 * x + 2 * k; return { a: x,
      q: function () { return t3("El llarg d'un rectangle fa " + k + " cm més que l'ample i el perímetre és de " + P + " cm. Quant fa l'ample?", "El largo de un rectángulo mide " + k + " cm más que el ancho y el perímetro es de " + P + " cm. ¿Cuánto mide el ancho?", "A rectangle is " + k + " cm longer than it is wide and its perimeter is " + P + " cm. How wide is it?"); },
      s: function () { return [t3("Ample ", "Ancho ", "Width ") + tex("x") + t3(", llarg ", ", largo ", ", length ") + tex("x+" + k), tex("2x+2(x+" + k + ")=" + P + "\\Rightarrow 4x+" + 2 * k + "=" + P + "\\Rightarrow x=" + x), t3("L'ample fa ", "El ancho mide ", "The width is ") + x + " cm" + t3(" i el llarg, ", " y el largo, ", " and the length ") + (x + k) + " cm."]; } }; },
    function () { var f = pick([[3, 4], [2, 5], [4, 6], [3, 5]]), den = ilcm(f[0], f[1]), rest = den - den / f[0] - den / f[1], t = rnd(2, 10), x = den * t * 5, R = x * rest / den; return { a: x,
      q: function () { return t3("Gaste " + "1/" + f[0] + " dels meus diners en roba i 1/" + f[1] + " en llibres, i encara em queden " + R + " €. Quants diners tenia?", "Gasto 1/" + f[0] + " de mi dinero en ropa y 1/" + f[1] + " en libros, y todavía me quedan " + R + " €. ¿Cuánto dinero tenía?", "I spend 1/" + f[0] + " of my money on clothes and 1/" + f[1] + " on books, and I still have " + R + " € left. How much did I have?"); },
      s: function () { return [t3("Tenia ", "Tenía ", "I had ") + tex("x") + " €", tex("x-\\dfrac{x}{" + f[0] + "}-\\dfrac{x}{" + f[1] + "}=" + R + "\\ \\xrightarrow{\\cdot" + den + "}\\ " + den + "x-" + den / f[0] + "x-" + den / f[1] + "x=" + R * den), tex(rest + "x=" + R * den + "\\Rightarrow x=" + x), t3("Tenia ", "Tenía ", "I had ") + x + " €."]; } }; },
    function () { var n = rnd(2, 6), m = rnd(2, 6), d = pick([0.5, 1, 1.5, 2]), x = pick([0.5, 1, 1.5, 2, 2.5]), T = n * (x + d) + m * x; return { a: x,
      q: function () { return t3("He comprat " + n + " quaderns i " + m + " bolígrafs per " + decS(T) + " €. Un quadern costa " + decS(d) + " € més que un bolígraf. Quant costa un bolígraf?", "He comprado " + n + " cuadernos y " + m + " bolígrafos por " + decS(T) + " €. Un cuaderno cuesta " + decS(d) + " € más que un bolígrafo. ¿Cuánto cuesta un bolígrafo?", "I bought " + n + " notebooks and " + m + " pens for " + decS(T) + " €. A notebook costs " + decS(d) + " € more than a pen. How much is a pen?"); },
      s: function () { return [t3("Bolígraf ", "Bolígrafo ", "Pen ") + tex("x") + t3(", quadern ", ", cuaderno ", ", notebook ") + tex("x+" + dT(d)), tex(n + "(x+" + dT(d) + ")+" + m + "x=" + dT(T) + "\\Rightarrow " + (n + m) + "x=" + dT(T - n * d) + "\\Rightarrow x=" + dT(x)), t3("Un bolígraf costa ", "Un bolígrafo cuesta ", "A pen costs ") + decS(x) + " €."]; } }; }
  ];
  var PROB2 = [
    function () { var x = rnd(3, 15), k = rnd(1, 6), A = x * (x + k), D = k * k + 4 * A, s = Math.sqrt(D); return { a: x,
      q: function () { return t3("Un rectangle té una àrea de " + A + " m² i el llarg fa " + k + " m més que l'ample. Quant fa l'ample?", "Un rectángulo tiene un área de " + A + " m² y el largo mide " + k + " m más que el ancho. ¿Cuánto mide el ancho?", "A rectangle has an area of " + A + " m² and is " + k + " m longer than it is wide. How wide is it?"); },
      s: function () { return [t3("Ample ", "Ancho ", "Width ") + tex("x") + t3(", llarg ", ", largo ", ", length ") + tex("x+" + k), tex("x(x+" + k + ")=" + A + "\\Rightarrow x^2+" + (k === 1 ? "" : k) + "x-" + A + "=0"), tex("x=\\dfrac{-" + k + "\\pm\\sqrt{" + D + "}}{2}=\\dfrac{-" + k + "\\pm" + s + "}{2}\\Rightarrow x=" + x + ",\\ x=" + (-x - k)), t3("La negativa no val: l'ample fa ", "La negativa no vale: el ancho mide ", "The negative one is rejected: the width is ") + x + " m."]; } }; },
    function () { var x = rnd(4, 25), N = x * (x + 1); return { a: x,
      q: function () { return t3("El producte de dos nombres naturals consecutius és " + N + ". Quins són? (escriu el menor)", "El producto de dos números naturales consecutivos es " + N + ". ¿Cuáles son? (escribe el menor)", "The product of two consecutive natural numbers is " + N + ". What are they? (type the smaller)"); },
      s: function () { var D = 1 + 4 * N, s = Math.sqrt(D); return [tex("x(x+1)=" + N + "\\Rightarrow x^2+x-" + N + "=0"), tex("x=\\dfrac{-1\\pm\\sqrt{" + D + "}}{2}=\\dfrac{-1\\pm" + s + "}{2}\\Rightarrow x=" + x + ",\\ x=" + (-x - 1)), t3("Com que són naturals, són ", "Como son naturales, son ", "Since they're natural numbers, they are ") + x + t3(" i ", " y ", " and ") + (x + 1) + "."]; } }; },
    function () { var x = rnd(3, 20), N = x * x + (x + 1) * (x + 1); return { a: x,
      q: function () { return t3("La suma dels quadrats de dos nombres naturals consecutius és " + N + ". Quins són? (escriu el menor)", "La suma de los cuadrados de dos números naturales consecutivos es " + N + ". ¿Cuáles son? (escribe el menor)", "The squares of two consecutive natural numbers add up to " + N + ". What are they? (type the smaller)"); },
      s: function () { var c = (N - 1) / 2, D = 1 + 4 * c, s = Math.sqrt(D); return [tex("x^2+(x+1)^2=" + N + "\\Rightarrow 2x^2+2x+1=" + N + "\\Rightarrow x^2+x-" + c + "=0"), tex("x=\\dfrac{-1\\pm" + s + "}{2}\\Rightarrow x=" + x + ",\\ x=" + (-x - 1)), t3("Són ", "Son ", "They are ") + x + t3(" i ", " y ", " and ") + (x + 1) + "."]; } }; },
    function () { var T = pick([[3, 4, 5], [5, 12, 13], [8, 15, 17], [20, 21, 29], [7, 24, 25]]), t = T[2] > 20 ? 1 : rnd(1, 3), a = T[0] * t, b = T[1] * t, h = T[2] * t, k = b - a; return { a: a,
      q: function () { return t3("En un triangle rectangle, un catet fa " + k + " cm més que l'altre i la hipotenusa fa " + h + " cm. Quant fa el catet menor?", "En un triángulo rectángulo, un cateto mide " + k + " cm más que el otro y la hipotenusa mide " + h + " cm. ¿Cuánto mide el cateto menor?", "In a right triangle, one leg is " + k + " cm longer than the other and the hypotenuse is " + h + " cm. How long is the shorter leg?"); },
      s: function () { var c = (h * h - k * k) / 2, B = k, D = B * B + 4 * c, s = Math.sqrt(D); return [t3("Catets ", "Catetos ", "Legs ") + tex("x") + t3(" i ", " y ", " and ") + tex("x+" + k) + t3(" (Pitàgores)", " (Pitágoras)", " (Pythagoras)"), tex("x^2+(x+" + k + ")^2=" + h * h + "\\Rightarrow 2x^2+" + 2 * k + "x-" + (h * h - k * k) + "=0\\Rightarrow x^2+" + (k === 1 ? "" : k) + "x-" + c + "=0"), tex("x=\\dfrac{-" + k + "\\pm" + s + "}{2}\\Rightarrow x=" + a + ",\\ x=" + (-b)), t3("El catet menor fa ", "El cateto menor mide ", "The shorter leg is ") + a + " cm" + t3(" (i l'altre, ", " (y el otro, ", " (and the other, ") + b + " cm)."]; } }; },
    function () { var x = rnd(3, 12), m = pick([2, 3, 4, 5]), N = x * x - m * x; if (N <= 0) { x += m; N = x * x - m * x; } return { a: x,
      q: function () { return t3("Si al quadrat d'un nombre natural li restem " + m + " vegades el nombre, obtenim " + N + ". Quin és el nombre?", "Si al cuadrado de un número natural le restamos " + m + " veces el número, obtenemos " + N + ". ¿Cuál es el número?", "If we subtract " + m + " times a natural number from its square, we get " + N + ". What is the number?"); },
      s: function () { var D = m * m + 4 * N, s = Math.sqrt(D), o = m - x; return [tex("x^2-" + m + "x=" + N + "\\Rightarrow x^2-" + m + "x-" + N + "=0"), tex("x=\\dfrac{" + m + "\\pm\\sqrt{" + D + "}}{2}=\\dfrac{" + m + "\\pm" + s + "}{2}\\Rightarrow x=" + x + ",\\ x=" + o), t3("Ha de ser natural: ", "Tiene que ser natural: ", "It must be a natural number: ") + tex("x=" + x) + "."]; } }; }
  ];
  function wProb() { probW(byId("w-prob1"), PROB1); probW(byId("w-prob2"), PROB2); }
  function probW(w, GEN) {
    if (!w) return;
    var P, shown = false, last = -1, qEl = $(w, "q"), inp = $(w, "a"), fb = $(w, "fb"), sol = $(w, "sol");
    function nw() { var i; do { i = Math.floor(Math.random() * GEN.length); } while (GEN.length > 1 && i === last); last = i; P = GEN[i](); inp.value = ""; fb.innerHTML = ""; shown = false; draw(); }
    function draw() {
      qEl.innerHTML = P.q();
      sol.innerHTML = shown ? "<ol>" + P.s().map(function (l) { return "<li>" + l + "</li>"; }).join("") + "</ol>" : "";
    }
    function check() {
      var v = parseFr(inp.value);
      if (!v) { fb.innerHTML = '<span class="msg-bad">' + t3("Escriu un nombre.", "Escribe un número.", "Type a number.") + "</span>"; return; }
      var good = Math.abs(v.val() - P.a) < 1e-6;
      fb.innerHTML = good ? '<span class="msg-ok">✓ ' + u("right") + "</span>" : '<span class="msg-bad">✗ ' + u("wrong") + " " + t3("Torna-ho a provar o mira la resolució.", "Vuelve a intentarlo o mira la resolución.", "Try again or look at the solution.") + "</span>";
    }
    $(w, "chk").addEventListener("click", check);
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") check(); });
    $(w, "new").addEventListener("click", nw);
    $(w, "show").addEventListener("click", function () { shown = !shown; draw(); });
    nw();
    onLang(function () { if (P) { draw(); if (fb.innerHTML) check(); } });
  }

