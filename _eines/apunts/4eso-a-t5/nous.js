  /* ======================= ginys nous de 4t ESO A, unitat 5 ======================= */

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
      .replace(/[\[{]/g, "(").replace(/[\]}]/g, ")").replace(/X/g, "x").replace(/Y/g, "y").replace(/\s+/g, "");
    var out = [], i = 0, m;
    while (i < s.length) {
      var c = s.charAt(i);
      if ((m = /^\d+(?:[.,]\d+)?/.exec(s.slice(i)))) { out.push({ t: "n", s: m[0] }); i += m[0].length; }
      else if (c === "x" || c === "y") { out.push({ t: c }); i++; }
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

  /* ---------- analitzador d'expressions lineals en x i y: { x, y, c } (Fr) i t (TeX tal com s'ha escrit) ---------- */
  function lnK(c) { return { x: F0, y: F0, c: c }; }
  function lnAdd(a, b, s) { return { x: a.x.add(b.x.mul(s)), y: a.y.add(b.y.mul(s)), c: a.c.add(b.c.mul(s)) }; }
  function lnScale(a, k) { return { x: a.x.mul(k), y: a.y.mul(k), c: a.c.mul(k) }; }
  function lnIsK(a) { return a.x.zero() && a.y.zero(); }
  function lnMul(a, b) { if (lnIsK(a)) return lnScale(b, a.c); if (lnIsK(b)) return lnScale(a, b.c); throw new Error("nolin"); }
  function parseLinSide(s, info) {
    var tk = lexE(s), i = 0;
    if (!tk || !tk.length) return null;
    function pk() { return tk[i] ? tk[i].t : null; }
    function strip(nd) { return nd.par ? nd.inner : nd.t; }
    function expr() {
      var a = term();
      while (pk() === "+" || pk() === "-") { var o = tk[i++].t, b = term(); a = { v: lnAdd(a.v, b.v, o === "-" ? FM1 : F1), t: a.t + o + b.t }; }
      return a;
    }
    function term() {
      var a = unary();
      for (;;) {
        var p = pk();
        if (p === "*" || p === "/") {
          i++; var b = unary();
          if (p === "*") a = { v: lnMul(a.v, b.v), t: a.t + "\\cdot " + b.t };
          else {
            if (!lnIsK(b.v)) throw new Error("nolin");
            var c = b.v.c; if (c.zero()) throw new Error("div0");
            if (c.d === 1) info.m = ilcm(info.m, Math.abs(c.n));
            a = { v: lnScale(a.v, F1.div(c)), t: "\\dfrac{" + strip(a) + "}{" + strip(b) + "}" };
          }
        } else if (p === "x" || p === "y" || p === "(" || p === "n") {
          var b2 = unary(), sep = /\d$/.test(a.t) && /^\d/.test(b2.t) ? "\\cdot " : "";
          a = { v: lnMul(a.v, b2.v), t: a.t + sep + b2.t };
        } else return a;
      }
    }
    function unary() {
      if (pk() === "-") { i++; var a = unary(); return { v: lnScale(a.v, FM1), t: "-" + a.t }; }
      if (pk() === "+") { i++; return unary(); }
      return atom();
    }
    function atom() {
      var q = tk[i++]; if (!q) throw new Error("end");
      if (q.t === "n") return { v: lnK(numFr(q.s)), t: q.s.replace(/[.,]/, lang === "en" ? "." : "{,}") };
      if (q.t === "x") return { v: { x: F1, y: F0, c: F0 }, t: "x" };
      if (q.t === "y") return { v: { x: F0, y: F1, c: F0 }, t: "y" };
      if (q.t === "(") { var e = expr(); if (pk() !== ")") throw new Error("par"); i++; return { v: e.v, t: "\\left(" + e.t + "\\right)", par: true, inner: e.t }; }
      throw new Error("tok");
    }
    try { var r = expr(); if (i < tk.length) return null; return r; } catch (e) { return null; }
  }
  // equació lineal → forma ax+by=c amb coeficients enters
  function parseLinEq(s) {
    var parts = String(s || "").split("="); if (parts.length !== 2) return null;
    var info = { m: 1 }, L = parseLinSide(parts[0], info), R = parseLinSide(parts[1], info);
    if (!L || !R) return null;
    var D = lnAdd(L.v, R.v, FM1), k = info.m;   // D = 0, és a dir, D.x·x + D.y·y + D.c = 0
    [D.x, D.y, D.c].forEach(function (c) { k = ilcm(k, c.d); });
    var a = D.x.mul(k), b = D.y.mul(k), c = D.c.neg().mul(k), g = gcd(gcd(a.n, b.n), c.n) || 1;
    if (a.sgn() < 0 || (a.zero() && b.sgn() < 0)) g = -g;
    return { t: L.t + "=" + R.t, k: k, m: info.m, a: a.div(new Fr(g)), b: b.div(new Fr(g)), c: c.div(new Fr(g)), g: Math.abs(g), k0: { a: a, b: b, c: c } };
  }

  /* ---------- 5.3 sistemes amb parèntesis i denominadors ---------- */
  var SRED_PRE = [["(x+1)/2+y/3=2", "2(x-y)=x-3"], ["3(x-1)+y=6", "x-2(y+1)=-6"], ["x/3+y/2=4", "x/2-y/4=2"], ["(x-1)/2+(y+1)/3=2", "2(x+y)-(x-3)=10"], ["x/5-y/2=0", "(x+1)/3+(y-2)/4=2"]];
  function wSred() {
    var w = byId("w-sred"); if (!w) return;
    var info = w.querySelector(".info"), met = -1, mb;
    mb = presetBtns($(w, "met"), function () { return [t3("Substitució", "Sustitución", "Substitution"), t3("Igualació", "Igualación", "Equalisation"), t3("Reducció", "Reducción", "Elimination")]; }, function (i) { met = i; draw(); });
    presetBtns($(w, "pre"), function () { return SRED_PRE.map(function (P) { var A = parseLinEq(P[0]), B = parseLinEq(P[1]); return tex("\\begin{cases}" + A.t + "\\\\ " + B.t + "\\end{cases}"); }); },
      function (i) { $(w, "e1").value = SRED_PRE[i][0]; $(w, "e2").value = SRED_PRE[i][1]; met = -1; draw(); });
    function draw() {
      var E = [parseLinEq($(w, "e1").value), parseLinEq($(w, "e2").value)];
      $(w, "e1").classList.toggle("bad", !E[0]); $(w, "e2").classList.toggle("bad", !E[1]);
      if (!E[0] || !E[1] || (E[0].a.zero() && E[0].b.zero()) || (E[1].a.zero() && E[1].b.zero())) {
        info.innerHTML = t3("Escriu dues equacions de primer grau amb <code>x</code> i <code>y</code>, per exemple <code>(x+1)/2+y/3=2</code> i <code>2(x-y)=x-3</code>. Fes servir <code>/</code> per a les fraccions.", "Escribe dos ecuaciones de primer grado con <code>x</code> e <code>y</code>, por ejemplo <code>(x+1)/2+y/3=2</code> y <code>2(x-y)=x-3</code>. Usa <code>/</code> para las fracciones.", "Type two linear equations in <code>x</code> and <code>y</code>, e.g. <code>(x+1)/2+y/3=2</code> and <code>2(x-y)=x-3</code>. Use <code>/</code> for fractions."); return;
      }
      var rows = [[t3("Sistema", "Sistema", "System"), tex("\\begin{cases}" + E[0].t + "\\\\ " + E[1].t + "\\end{cases}")]];
      E.forEach(function (e, i) {
        var lab = t3("Equació ", "Ecuación ", "Equation ") + (i + 1), how;
        if (e.m > 1) how = t3("Multipliquem per m.c.m. = ", "Multiplicamos por m.c.m. = ", "Multiply by the LCM = ") + e.k + t3(", traiem parèntesis i reduïm:", ", quitamos paréntesis y reducimos:", ", expand and simplify:");
        else if (e.k > 1) how = t3("Multipliquem per ", "Multiplicamos por ", "Multiply by ") + e.k + t3(" i reduïm:", " y reducimos:", " and simplify:");
        else how = t3("Traiem parèntesis i passem les incògnites a l'esquerra:", "Quitamos paréntesis y pasamos las incógnitas a la izquierda:", "Expand and move the unknowns to the left:");
        var txt = how + "<br>" + tex(eqT(e.k0.a, e.k0.b, e.k0.c)), dv = e.k0.a.zero() ? e.k0.b.div(e.b) : e.k0.a.div(e.a);
        if (!dv.eq(F1)) txt += " → " + tex(eqT(e.a, e.b, e.c)) + " <small>(" + (dv.eq(FM1) ? "·(−1)" : "÷" + frT(dv).replace("-", "−")) + ")</small>";
        rows.push([lab, txt]);
      });
      var v = { a1: E[0].a, b1: E[0].b, c1: E[0].c, a2: E[1].a, b2: E[1].b, c2: E[1].c };
      var m = met;
      if (m < 0) { m = [v.a1, v.b1, v.a2, v.b2].some(function (c) { return c.abs().eq(F1); }) ? 0 : 2; mb.forEach(function (b, j) { b.classList.toggle("on", j === m); }); }
      rows.push([t3("Sistema equivalent", "Sistema equivalente", "Equivalent system"), tex(sysT(v)) + " <small>(" + [t3("per substitució", "por sustitución", "by substitution"), t3("per igualació", "por igualación", "by equalisation"), t3("per reducció", "por reducción", "by elimination")][m] + ")</small>"]);
      info.innerHTML = kv(metRows(v, m, rows));
    }
    ["e1", "e2"].forEach(function (r) { $(w, r).addEventListener("input", function () { draw(); }); });
    onLang(draw);
  }

  /* ---------- 5.6 i 5.7 resolutor d'inequacions (primer i segon grau) ---------- */
  var IN_PRE = {
    "w-in1": ["3(x-2)+1<x+5", "2-(x+4)>=3x+6", "(x+1)/2-(x-3)/3<=1", "x/4-(2x-1)/6>x/3+1", "2(x+3)>2x+1"],
    "w-in2": ["x^2-5x+6<0", "x^2-9>=0", "x^2+3x<=0", "-x^2+2x+3>0", "(x-1)^2>=x+5", "x^2+2x+5<0"]
  };
  var IOP = { "<": "\\lt ", "<=": "\\le ", ">": "\\gt ", ">=": "\\ge " }, IFL = { "<": ">", "<=": ">=", ">": "<", ">=": "<=" };
  function splitIneq(s) {
    s = String(s || "").replace(/≤|=</g, "<=").replace(/≥|=>/g, ">=");
    var m = /^([^<>=]+)(<=|>=|<|>)([^<>=]+)$/.exec(s.replace(/\s+/g, ""));
    return m ? { l: m[1], op: m[2], r: m[3] } : null;
  }
  function ineqHolds(v, op) { return op === "<" ? v < 0 : op === "<=" ? v <= 0 : op === ">" ? v > 0 : v >= 0; }
  function wIneq() { Object.keys(IN_PRE).forEach(function (id) { ineqW(byId(id), IN_PRE[id]); }); }
  function ineqW(w, PRE) {
    if (!w) return;
    var info = w.querySelector(".info"), inp = $(w, "e"), svg = w.querySelector("svg");
    function show(s) { var q = splitIneq(s), I = { dens: [], m: 1 }, L = q && parseSide(q.l, I), R = q && parseSide(q.r, I); return L && R ? tex(L.t + IOP[q.op] + R.t) : s; }
    presetBtns($(w, "pre"), function () { return PRE.map(show); }, function (i) { inp.value = PRE[i]; draw(); });
    function draw() {
      var q = splitIneq(inp.value), I = { dens: [], m: 1 }, L = q && parseSide(q.l, I), R = q && parseSide(q.r, I);
      var good = L && R && !I.dens.length && pIsConst(L.rf.d) && pIsConst(R.rf.d);
      inp.classList.toggle("bad", !good);
      if (!good) { info.innerHTML = t3("Escriu una inequació amb un dels signes <code>&lt;</code>, <code>&lt;=</code>, <code>&gt;</code> o <code>&gt;=</code>, per exemple <code>(x+1)/2-3(x-2)&lt;x</code>. La x no pot estar al denominador.", "Escribe una inecuación con uno de los signos <code>&lt;</code>, <code>&lt;=</code>, <code>&gt;</code> o <code>&gt;=</code>, por ejemplo <code>(x+1)/2-3(x-2)&lt;x</code>. La x no puede estar en el denominador.", "Type an inequality with one of <code>&lt;</code>, <code>&lt;=</code>, <code>&gt;</code> or <code>&gt;=</code>, e.g. <code>(x+1)/2-3(x-2)&lt;x</code>. x can't be in a denominator."); svg.innerHTML = ""; return; }
      var op = q.op, Lp = L.rf.n, Rp = R.rf.n, rows = [[t3("Inequació", "Inecuación", "Inequality"), tex(L.t + IOP[op] + R.t)]];
      var k = ilcm(ilcm(coefLcm(Lp), coefLcm(Rp)), I.m);
      Lp = pScale(Lp, new Fr(k)); Rp = pScale(Rp, new Fr(k));
      var same = (pTex(Lp) + IOP[op] + pTex(Rp)).replace(/\s/g, "") === (L.t + IOP[op] + R.t).replace(/\s/g, "");
      if (!same) rows.push([k > 1 ? t3("Multipliquem per ", "Multiplicamos por ", "Multiply by ") + k : t3("Traiem parèntesis", "Quitamos paréntesis", "Expand"), tex(pTex(Lp) + IOP[op] + pTex(Rp)) + (k > 1 ? "<br><small>" + t3("És positiu: el sentit de la desigualtat no canvia.", "Es positivo: el sentido de la desigualdad no cambia.", "It's positive: the inequality keeps its direction.") + "</small>" : "")]);
      var P = pSub(Lp, Rp), d = pDeg(P), S, lab = nT;
      if (d > 2) { rows.push(["", t3("Aquest resolutor només fa inequacions de primer i de segon grau.", "Este resolutor solo hace inecuaciones de primer y de segundo grado.", "This solver only handles linear and quadratic inequalities.")]); info.innerHTML = kv(rows); svg.innerHTML = ""; return; }
      if (d <= 0) {
        var c0 = d < 0 ? 0 : P[0].val(), h = ineqHolds(c0, op);
        rows.push([t3("Ho passem tot a un membre", "Lo pasamos todo a un miembro", "Move everything to one side"), tex(frT(d < 0 ? F0 : P[0]) + IOP[op] + "0") + ": " + (h ? t3("es compleix sempre", "se cumple siempre", "always true") : t3("no es compleix mai", "no se cumple nunca", "never true"))]);
        S = h ? [{ a: -Infinity, ac: false, b: Infinity, bc: false }] : [];
      } else if (d === 1) {
        var a = P[1], b = P[0], r = b.neg().div(a), o = a.sgn() < 0 ? IFL[op] : op, cl = o.length === 2;
        rows.push([t3("Agrupem", "Agrupamos", "Collect terms"), tex(pTex([F0, a]) + IOP[op] + frT(b.neg()))]);
        if (!a.eq(F1)) rows.push([t3("Aïllem la x", "Despejamos la x", "Isolate x"), tex("x" + IOP[o] + (a.eq(F1) ? "" : "\\dfrac{" + frT(b.neg()) + "}{" + frT(a) + "}=") + frT(r)) + (a.sgn() < 0 ? "<br><small><strong>" + t3("Hem dividit per un nombre negatiu: la desigualtat canvia de sentit.", "Hemos dividido por un número negativo: la desigualdad cambia de sentido.", "We divided by a negative number: the inequality is reversed.") + "</strong></small>" : "")]);
        S = o.charAt(0) === "<" ? [{ a: -Infinity, ac: false, b: r.val(), bc: cl }] : [{ a: r.val(), ac: cl, b: Infinity, bc: false }];
      } else {
        if (pDeg(Rp) >= 0) rows.push([t3("Ho passem tot a un membre", "Lo pasamos todo a un miembro", "Move everything to one side"), tex(pTex(P) + IOP[op] + "0")]);
        if (P[2].sgn() < 0) { P = pScale(P, FM1); op = IFL[op]; rows.push([t3("Multipliquem per −1", "Multiplicamos por −1", "Multiply by −1"), tex(pTex(P) + IOP[op] + "0") + " <small>(" + t3("la desigualtat canvia de sentit", "la desigualdad cambia de sentido", "the inequality is reversed") + ")</small>"]); }
        var Iq = intForm(P); if (Iq.k.d === 1 && Iq.k.n > 1) { P = Iq.P; rows.push([t3("Simplifiquem", "Simplificamos", "Simplify") + " (÷" + Iq.k.n + ")", tex(pTex(P) + IOP[op] + "0")]); }
        var Q = quadRoots(P[2], P[1], P[0]), rts = Q.roots;
        rows.push([t3("Arrels", "Raíces", "Roots"), tex(pTex(P) + "=0") + ": " + (Q.kind === "none" ? tex("\\Delta=" + frT(Q.D) + "\\lt 0") + ", " + t3("no en té", "no tiene", "none") : rts.map(function (x) { return tex("x=" + x.tex); }).join(", ") + (Q.kind === "double" ? " (" + t3("doble", "doble", "double") + ")" : ""))]);
        lab = function (v) { var m = rts.filter(function (x) { return Math.abs(x.v - v) < 1e-9; })[0]; return m ? m.tex : nT(v); };
        var cuts = rts.map(function (x) { return x.v; }), tests = [], i;
        if (!cuts.length) tests = [0];
        else {
          tests.push(Math.ceil(cuts[0]) - 1);
          for (i = 0; i + 1 < cuts.length; i++) { var mi = Math.floor(cuts[i]) + 1; tests.push(mi < cuts[i + 1] ? mi : (cuts[i] + cuts[i + 1]) / 2); }
          tests.push(Math.floor(cuts[cuts.length - 1]) + 1);
        }
        rows.push([t3("Signe en cada interval", "Signo en cada intervalo", "Sign on each interval"), tests.map(function (t) { var v = pEvalN(P, t); return tex("P(" + nT(t) + ")=" + nT(v) + (v > 0 ? "\\gt 0" : "\\lt 0")); }).join(", ")]);
        S = [];
        var ends = [-Infinity].concat(cuts, [Infinity]);
        for (i = 0; i < ends.length - 1; i++) if (ineqHolds(pEvalN(P, tests[i]), op)) S.push({ a: ends[i], ac: false, b: ends[i + 1], bc: false });
        if (op.length === 2) cuts.forEach(function (c) { S.push({ a: c, ac: true, b: c, bc: true }); });
        S = norm(S);
        if (cuts.length) rows.push(["", "<small>" + (op.length === 2 ? t3("Les arrels s'inclouen (hi ha igual).", "Las raíces se incluyen (hay igual).", "The roots are included (there's an equals sign).") : t3("Les arrels no s'inclouen (desigualtat estricta).", "Las raíces no se incluyen (desigualdad estricta).", "The roots are not included (strict inequality).")) + "</small>"]);
      }
      rows.push([t3("Solució", "Solución", "Solution"), "<strong>" + tex("x\\in " + setTL(S, lab)) + "</strong>"]);
      info.innerHTML = kv(rows);
      var W = svgW(svg); paint(svg, nline([{ S: S, c: COL.r }], { W: W }), W);
    }
    inp.addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 5.5 entrenador de problemes amb sistemes ---------- */
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(L) { return L[Math.floor(Math.random() * L.length)]; }
  function cs(a, b) { return "\\begin{cases}" + a + "\\\\ " + b + "\\end{cases}"; }
  var PSYS1 = [
    function () { var x = rnd(8, 40), y = rnd(5, 30), N = x + y, W = 4 * x + 2 * y; return { a: [x, y], n: function () { return [t3("cotxes", "coches", "cars"), t3("motos", "motos", "motorbikes")]; },
      q: function () { return t3("En un aparcament hi ha " + N + " vehicles entre cotxes i motos, i en total " + W + " rodes. Quants cotxes i quantes motos hi ha?", "En un aparcamiento hay " + N + " vehículos entre coches y motos, y en total " + W + " ruedas. ¿Cuántos coches y cuántas motos hay?", "A car park holds " + N + " vehicles, cars and motorbikes, with " + W + " wheels in total. How many cars and how many motorbikes are there?"); },
      s: function () { return [tex("x=") + t3(" cotxes, ", " coches, ", " cars, ") + tex("y=") + t3(" motos", " motos", " motorbikes"), tex(cs("x+y=" + N, "4x+2y=" + W)), t3("Restem a la 2a el doble de la 1a: ", "Restamos a la 2ª el doble de la 1ª: ", "Subtract twice the 1st from the 2nd: ") + tex("2x=" + (W - 2 * N) + "\\Rightarrow x=" + x + ",\\ y=" + y), t3("Hi ha " + x + " cotxes i " + y + " motos.", "Hay " + x + " coches y " + y + " motos.", "There are " + x + " cars and " + y + " motorbikes.")]; } }; },
    function () { var p = rnd(6, 15), q = rnd(2, p - 2), A = rnd(2, 5), B = rnd(1, 4), C = rnd(1, 4), D = rnd(2, 5); if (A * D === B * C) D++; var T1 = A * p + B * q, T2 = C * p + D * q; return { a: [p, q], n: function () { return [t3("adult (€)", "adulto (€)", "adult (€)"), t3("infant (€)", "niño (€)", "child (€)")]; },
      q: function () { return t3(A + " entrades d'adult i " + B + " d'infant costen " + T1 + " €, i " + C + " d'adult i " + D + " d'infant, " + T2 + " €. Quant costa cada entrada?", A + " entradas de adulto y " + B + " de niño cuestan " + T1 + " €, y " + C + " de adulto y " + D + " de niño, " + T2 + " €. ¿Cuánto cuesta cada entrada?", A + " adult tickets and " + B + " child tickets cost " + T1 + " €, and " + C + " adult and " + D + " child tickets cost " + T2 + " €. How much is each ticket?"); },
      s: function () { return [tex("x=") + t3(" preu adult, ", " precio adulto, ", " adult price, ") + tex("y=") + t3(" preu infant", " precio niño", " child price"), tex(cs(A + "x+" + B + "y=" + T1, C + "x+" + D + "y=" + T2)), t3("Per reducció: ", "Por reducción: ", "By elimination: ") + tex("x=" + p + ",\\ y=" + q), t3("L'entrada d'adult costa " + p + " € i la d'infant, " + q + " €.", "La entrada de adulto cuesta " + p + " € y la de niño, " + q + " €.", "An adult ticket costs " + p + " € and a child ticket " + q + " €.")]; } }; },
    function () { var y = rnd(4, 14), d = rnd(2, 12), k = pick([2, 3]), x = k * (y + d) - d; return { a: [x, y], n: function () { return [t3("pare (anys)", "padre (años)", "father (years)"), t3("fill (anys)", "hijo (años)", "son (years)")]; },
      q: function () { return t3("Un pare té " + (x - y) + " anys més que el seu fill. D'ací a " + d + " anys, l'edat del pare serà " + (k === 2 ? "el doble" : "el triple") + " de la del fill. Quants anys té cadascun?", "Un padre tiene " + (x - y) + " años más que su hijo. Dentro de " + d + " años, la edad del padre será " + (k === 2 ? "el doble" : "el triple") + " de la del hijo. ¿Cuántos años tiene cada uno?", "A father is " + (x - y) + " years older than his son. In " + d + " years the father will be " + (k === 2 ? "twice" : "three times") + " as old as the son. How old is each?"); },
      s: function () { return [tex("x=") + t3(" edat del pare, ", " edad del padre, ", " father's age, ") + tex("y=") + t3(" edat del fill", " edad del hijo", " son's age"), tex(cs("x-y=" + (x - y), "x+" + d + "=" + k + "(y+" + d + ")")), t3("Substituïm ", "Sustituimos ", "Substitute ") + tex("x=y+" + (x - y)) + ": " + tex("y+" + (x - y + d) + "=" + k + "y+" + k * d + "\\Rightarrow y=" + y + ",\\ x=" + x), t3("El pare té " + x + " anys i el fill, " + y + ".", "El padre tiene " + x + " años y el hijo, " + y + ".", "The father is " + x + " and the son " + y + ".")]; } }; },
    function () { var x = rnd(5, 30), y = rnd(5, 30), N = x + y, T = x + 2 * y; return { a: [x, y], n: function () { return [t3("monedes d'1 €", "monedas de 1 €", "1 € coins"), t3("monedes de 2 €", "monedas de 2 €", "2 € coins")]; },
      q: function () { return t3("Tinc " + N + " monedes d'1 € i de 2 €, que fan " + T + " €. Quantes en tinc de cada classe?", "Tengo " + N + " monedas de 1 € y de 2 €, que suman " + T + " €. ¿Cuántas tengo de cada clase?", "I have " + N + " coins of 1 € and 2 €, worth " + T + " € in total. How many of each do I have?"); },
      s: function () { return [tex("x=") + t3(" monedes d'1 €, ", " monedas de 1 €, ", " 1 € coins, ") + tex("y=") + t3(" monedes de 2 €", " monedas de 2 €", " 2 € coins"), tex(cs("x+y=" + N, "x+2y=" + T)), t3("Restant: ", "Restando: ", "Subtracting: ") + tex("y=" + y + ",\\ x=" + x), t3("Tinc " + x + " monedes d'1 € i " + y + " de 2 €.", "Tengo " + x + " monedas de 1 € y " + y + " de 2 €.", "I have " + x + " 1 € coins and " + y + " 2 € coins.")]; } }; },
    function () { var y = rnd(3, 20), x = y + rnd(1, 15), S = x + y, D = x - y; return { a: [x, y], n: function () { return [t3("major", "mayor", "larger"), t3("menor", "menor", "smaller")]; },
      q: function () { return t3("Dos nombres sumen " + S + " i es diferencien en " + D + ". Quins són?", "Dos números suman " + S + " y se diferencian en " + D + ". ¿Cuáles son?", "Two numbers add up to " + S + " and differ by " + D + ". What are they?"); },
      s: function () { return [tex(cs("x+y=" + S, "x-y=" + D)), t3("Sumant: ", "Sumando: ", "Adding: ") + tex("2x=" + (S + D) + "\\Rightarrow x=" + x + ",\\ y=" + y), t3("Són " + x + " i " + y + ".", "Son " + x + " y " + y + ".", "They are " + x + " and " + y + ".")]; } }; }
  ];
  var PSYS2 = [
    function () { var y = rnd(2, 12), x = y + rnd(1, 9), P = 2 * (x + y), A = x * y; return { a: [x, y], n: function () { return [t3("llarg (cm)", "largo (cm)", "length (cm)"), t3("ample (cm)", "ancho (cm)", "width (cm)")]; },
      q: function () { return t3("Un rectangle té " + P + " cm de perímetre i " + A + " cm² d'àrea. Quant fan el llarg i l'ample?", "Un rectángulo tiene " + P + " cm de perímetro y " + A + " cm² de área. ¿Cuánto miden el largo y el ancho?", "A rectangle has a perimeter of " + P + " cm and an area of " + A + " cm². How long and how wide is it?"); },
      s: function () { var S = x + y; return [tex(cs("2x+2y=" + P, "xy=" + A)) + " → " + tex("y=" + S + "-x"), tex("x(" + S + "-x)=" + A + "\\Rightarrow x^2-" + S + "x+" + A + "=0\\Rightarrow x=" + x + ",\\ x=" + y), t3("El rectangle fa " + x + " cm de llarg i " + y + " cm d'ample.", "El rectángulo mide " + x + " cm de largo y " + y + " cm de ancho.", "The rectangle is " + x + " cm long and " + y + " cm wide.")]; } }; },
    function () { var y = rnd(2, 12), x = y + rnd(1, 9), S = x + y, Pd = x * y; return { a: [x, y], n: function () { return [t3("major", "mayor", "larger"), t3("menor", "menor", "smaller")]; },
      q: function () { return t3("Dos nombres naturals sumen " + S + " i el seu producte és " + Pd + ". Quins són?", "Dos números naturales suman " + S + " y su producto es " + Pd + ". ¿Cuáles son?", "Two natural numbers add up to " + S + " and multiply to " + Pd + ". What are they?"); },
      s: function () { return [tex(cs("x+y=" + S, "xy=" + Pd)) + " → " + tex("y=" + S + "-x"), tex("x^2-" + S + "x+" + Pd + "=0\\Rightarrow x=" + x + ",\\ x=" + y), t3("Són " + x + " i " + y + ".", "Son " + x + " y " + y + ".", "They are " + x + " and " + y + ".")]; } }; },
    function () { var y = rnd(2, 10), d = rnd(1, 6), x = y + d, Q = x * x + y * y; return { a: [x, y], n: function () { return [t3("major", "mayor", "larger"), t3("menor", "menor", "smaller")]; },
      q: function () { return t3("Dos nombres naturals es diferencien en " + d + " i la suma dels seus quadrats és " + Q + ". Quins són?", "Dos números naturales se diferencian en " + d + " y la suma de sus cuadrados es " + Q + ". ¿Cuáles son?", "Two natural numbers differ by " + d + " and the sum of their squares is " + Q + ". What are they?"); },
      s: function () { var c = (d * d - Q) / 2; return [tex(cs("x-y=" + d, "x^2+y^2=" + Q)) + " → " + tex("x=y+" + d), tex("(y+" + d + ")^2+y^2=" + Q + "\\Rightarrow y^2+" + (d === 1 ? "" : d) + "y" + c + "=0\\Rightarrow y=" + y + ",\\ y=" + (-x)), t3("Com que són naturals: " + x + " i " + y + ".", "Como son naturales: " + x + " y " + y + ".", "Since they're natural numbers: " + x + " and " + y + ".")]; } }; },
    function () { var T = pick([[3, 4, 5], [6, 8, 10], [5, 12, 13], [9, 12, 15], [8, 15, 17], [12, 16, 20]]), x = T[1], y = T[0], A = x * y; return { a: [x, y], n: function () { return [t3("llarg (cm)", "largo (cm)", "length (cm)"), t3("ample (cm)", "ancho (cm)", "width (cm)")]; },
      q: function () { return t3("La diagonal d'un rectangle fa " + T[2] + " cm i l'àrea, " + A + " cm². Quant fan el llarg i l'ample?", "La diagonal de un rectángulo mide " + T[2] + " cm y el área, " + A + " cm². ¿Cuánto miden el largo y el ancho?", "A rectangle's diagonal is " + T[2] + " cm and its area " + A + " cm². How long and how wide is it?"); },
      s: function () { return [tex(cs("x^2+y^2=" + T[2] * T[2], "xy=" + A)) + " → " + tex("y=\\dfrac{" + A + "}{x}"), tex("x^2+\\dfrac{" + A * A + "}{x^2}=" + T[2] * T[2] + "\\Rightarrow x^4-" + T[2] * T[2] + "x^2+" + A * A + "=0\\Rightarrow x^2=" + x * x + ",\\ x^2=" + y * y), t3("Fa " + x + " cm de llarg i " + y + " cm d'ample.", "Mide " + x + " cm de largo y " + y + " cm de ancho.", "It is " + x + " cm long and " + y + " cm wide.")]; } }; }
  ];
  function wPsys() { psysW(byId("w-psys1"), PSYS1); psysW(byId("w-psys2"), PSYS2); }
  function psysW(w, GEN) {
    if (!w) return;
    var P, shown = false, last = -1, qEl = $(w, "q"), in1 = $(w, "a1"), in2 = $(w, "a2"), fb = $(w, "fb"), sol = $(w, "sol");
    function nw() { var i; do { i = Math.floor(Math.random() * GEN.length); } while (GEN.length > 1 && i === last); last = i; P = GEN[i](); in1.value = ""; in2.value = ""; fb.innerHTML = ""; shown = false; draw(); }
    function draw() {
      qEl.innerHTML = P.q(); var n = P.n(); $(w, "l1").textContent = n[0] + ":"; $(w, "l2").textContent = n[1] + ":";
      sol.innerHTML = shown ? "<ol>" + P.s().map(function (l) { return "<li>" + l + "</li>"; }).join("") + "</ol>" : "";
    }
    function check() {
      var v1 = parseFr(in1.value), v2 = parseFr(in2.value);
      if (!v1 || !v2) { fb.innerHTML = '<span class="msg-bad">' + t3("Escriu els dos nombres.", "Escribe los dos números.", "Type both numbers.") + "</span>"; return; }
      var good = Math.abs(v1.val() - P.a[0]) < 1e-6 && Math.abs(v2.val() - P.a[1]) < 1e-6;
      fb.innerHTML = good ? '<span class="msg-ok">✓ ' + u("right") + "</span>" : '<span class="msg-bad">✗ ' + u("wrong") + " " + t3("Torna-ho a provar o mira la resolució.", "Vuelve a intentarlo o mira la resolución.", "Try again or look at the solution.") + "</span>";
    }
    $(w, "chk").addEventListener("click", check);
    [in1, in2].forEach(function (e) { e.addEventListener("keydown", function (ev) { if (ev.key === "Enter") check(); }); });
    $(w, "new").addEventListener("click", nw);
    $(w, "show").addEventListener("click", function () { shown = !shown; draw(); });
    nw();
    onLang(function () { if (P) { draw(); if (fb.innerHTML) check(); } });
  }
