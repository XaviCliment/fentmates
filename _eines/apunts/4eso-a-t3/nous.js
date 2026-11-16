  /* ======================= ginys nous de 4t ESO A, unitat 3 ======================= */
  function mPoly(m) { var p = []; for (var i = 0; i < m.e; i++) p.push(F0); p.push(m.c); return pTrim(p); }
  function parseMon(s) {
    var p = parsePoly(s); if (!p) return null;
    var nz = 0, e = 0; p.forEach(function (c, i) { if (!c.zero()) { nz++; e = i; } });
    return nz === 1 ? { c: p[e], e: e } : null;
  }
  function mT(m) { return m.c.zero() ? "0" : monT(m.c, m.e, "x", true); }
  function mP(m) { return (m.c.sgn() < 0 || (m.e > 0 && !m.c.eq(F1)) || m.c.d !== 1) ? "\\left(" + mT(m) + "\\right)" : mT(m); }
  function xp(e) { return e === 0 ? "" : e === 1 ? "x" : "x^{" + e + "}"; }

  /* ---------- 3.1 operacions amb monomis ---------- */
  function monOps(A, B) {
    var r = { sem: A.e === B.e, prod: { c: A.c.mul(B.c), e: A.e + B.e }, quoOk: A.e >= B.e && !B.c.zero(), pow: { c: A.c.mul(A.c), e: 2 * A.e } };
    if (r.sem) { r.sum = { c: A.c.add(B.c), e: A.e }; r.dif = { c: A.c.sub(B.c), e: A.e }; }
    if (r.quoOk) r.quo = { c: A.c.div(B.c), e: A.e - B.e };
    return r;
  }
  function wMon() {
    var w = byId("w-mon"); if (!w) return;
    var info = w.querySelector(".info");
    var PRE = [["6x^3", "-2x^3"], ["12x^5", "4x^2"], ["-3x^2", "5x"], ["1/2x^4", "3x"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(mT(parseMon(p[0])) + ",\\ " + mT(parseMon(p[1]))); }); }, function (i) { $(w, "a").value = PRE[i][0]; $(w, "b").value = PRE[i][1]; draw(); });
    function draw() {
      var A = parseMon($(w, "a").value), B = parseMon($(w, "b").value);
      $(w, "a").classList.toggle("bad", !A); $(w, "b").classList.toggle("bad", !B);
      if (!A || !B) { info.innerHTML = t3("Escriu dos monomis en \\(x\\), per exemple <code>-3x^2</code> o <code>1/2x</code>.", "Escribe dos monomios en \\(x\\), por ejemplo <code>-3x^2</code> o <code>1/2x</code>.", "Type two monomials in \\(x\\), e.g. <code>-3x^2</code> or <code>1/2x</code>.").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }); return; }
      var R = monOps(A, B), a = mT(A), b = mT(B), rows = [];
      rows.push([t3("Graus", "Grados", "Degrees"), tex("\\text{gr}(" + a + ")=" + A.e + ",\\quad \\text{gr}(" + b + ")=" + B.e)]);
      if (R.sem) {
        rows.push([t3("Semblants?", "¿Semejantes?", "Like terms?"), t3("Sí: tenen la mateixa part literal ", "Sí: tienen la misma parte literal ", "Yes: same literal part ") + tex(xp(A.e) || "1") + " " + ok(true)]);
        rows.push([t3("Suma", "Suma", "Sum"), tex(a + "+" + mP(B) + "=(" + frT(A.c) + "+" + frP(B.c) + ")" + xp(A.e) + "=" + mT(R.sum))]);
        rows.push([t3("Resta", "Resta", "Difference"), tex(a + "-" + mP(B) + "=(" + frT(A.c) + "-" + frP(B.c) + ")" + xp(A.e) + "=" + mT(R.dif))]);
      } else {
        rows.push([t3("Semblants?", "¿Semejantes?", "Like terms?"), t3("No: les parts literals són diferents. ", "No: las partes literales son distintas. ", "No: the literal parts differ. ") + ok(false)]);
        rows.push([t3("Suma i resta", "Suma y resta", "Sum and difference"), tex(pTex(pAdd(mPoly(A), mPoly(B)))) + t3(" i ", " y ", " and ") + tex(pTex(pSub(mPoly(A), mPoly(B)))) + "<br><small>" + t3("No es poden reduir: el resultat és un polinomi.", "No se pueden reducir: el resultado es un polinomio.", "They can't be combined: the result is a polynomial.") + "</small>"]);
      }
      rows.push([t3("Producte", "Producto", "Product"), tex(mP(A) + "\\cdot " + mP(B) + "=(" + frT(A.c) + "\\cdot " + frP(B.c) + ")\\," + (A.e + B.e ? "x^{" + A.e + "+" + B.e + "}" : "") + "=" + mT(R.prod))]);
      if (R.quoOk) rows.push([t3("Quocient", "Cociente", "Quotient"), tex(mP(A) + ":" + mP(B) + "=(" + frT(A.c) + ":" + frP(B.c) + ")\\," + (A.e ? "x^{" + A.e + "-" + B.e + "}" : "") + "=" + mT(R.quo))]);
      else rows.push([t3("Quocient", "Cociente", "Quotient"), t3("L'exponent del divisor és més gran: el quocient no és un monomi.", "El exponente del divisor es mayor: el cociente no es un monomio.", "The divisor has the higher exponent: the quotient isn't a monomial.")]);
      rows.push([t3("Quadrat", "Cuadrado", "Square"), tex(mP(A) + "^2=" + frP(A.c) + "^2\\," + (A.e ? "x^{" + A.e + "\\cdot 2}" : "") + "=" + mT(R.pow))]);
      info.innerHTML = kv(rows);
    }
    ["a", "b"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 3.2 taula de valors numèrics ---------- */
  function wVn() {
    var w = byId("w-vn"); if (!w) return;
    var info = w.querySelector(".info");
    var PRE = [["x^2-3x+2", "-2, -1, 0, 1, 2"], ["2x^3-x+4", "-1, 0, 1, 2"], ["x^4-5x^2+4", "-2, -1, 0, 1, 2"], ["1/2x^2+x", "-2, 0, 2, 4"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(pTex(parsePoly(p[0]))); }); }, function (i) { $(w, "p").value = PRE[i][0]; $(w, "v").value = PRE[i][1]; draw(); });
    function draw() {
      var P = parsePoly($(w, "p").value), vs = $(w, "v").value.split(/[;]|,\s+|\s+/).filter(Boolean).map(parseFr);
      var good = P && vs.length && vs.length <= 8 && vs.every(Boolean);
      $(w, "p").classList.toggle("bad", !P); $(w, "v").classList.toggle("bad", !(vs.length && vs.every(Boolean)));
      if (!P) { info.innerHTML = u("badP"); return; }
      if (!good) { info.innerHTML = t3("Escriu fins a 8 valors de \\(x\\) separats per espais o per «, », per exemple <code>-1, 0, 2</code>.", "Escribe hasta 8 valores de \\(x\\) separados por espacios o por «, », por ejemplo <code>-1, 0, 2</code>.", "Type up to 8 values of \\(x\\) separated by spaces or \", \", e.g. <code>-1, 0, 2</code>.").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }); return; }
      var h = '<div class="tbl-wrap"><table class="data cand"><thead><tr><th>' + tex("x") + "</th>" + vs.map(function (a) { return "<th>" + tex(frT(a)) + "</th>"; }).join("") + "</tr></thead><tbody><tr><td>" + tex("P(x)") + "</td>";
      var zs = [];
      vs.forEach(function (a) { var v = pEval(P, a); if (v.zero()) zs.push(frT(a)); h += "<td" + (v.zero() ? ' class="yes"' : "") + ">" + tex(frT(v)) + "</td>"; });
      h += "</tr></tbody></table></div>";
      var rows = vs.map(function (a) { return [tex("x=" + frT(a)), tex("P(" + frT(a) + ")=" + subT(P, a) + "=" + frT(pEval(P, a)))]; });
      if (zs.length) rows.push(["", "<small>" + t3("En verd, els valors que fan \\(P(x)=0\\): són <strong>arrels</strong> del polinomi (ho veurem a l'apartat 3.7).", "En verde, los valores que hacen \\(P(x)=0\\): son <strong>raíces</strong> del polinomio (lo veremos en el apartado 3.7).", "In green, the values that make \\(P(x)=0\\): they are <strong>roots</strong> of the polynomial (see section 3.7).").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }) + "</small>"]);
      info.innerHTML = h + kv(rows);
    }
    ["p", "v"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 3.4 identitats notables ---------- */
  function idDev(A, B) {
    var a = mPoly(A), b = mPoly(B);
    return { sq: pMul(pAdd(a, b), pAdd(a, b)), sqm: pMul(pSub(a, b), pSub(a, b)), dif: pMul(pAdd(a, b), pSub(a, b)),
      a2: { c: A.c.mul(A.c), e: 2 * A.e }, b2: { c: B.c.mul(B.c), e: 2 * B.e }, ab2: { c: A.c.mul(B.c).mul(new Fr(2)), e: A.e + B.e } };
  }
  function wId() {
    var w = byId("w-id"); if (!w) return;
    var info = w.querySelector(".info");
    var PRE = [["x", "3"], ["2x", "5"], ["3x^2", "1"], ["x", "1/2"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex("a=" + mT(parseMon(p[0])) + ",\\ b=" + mT(parseMon(p[1]))); }); }, function (i) { $(w, "a").value = PRE[i][0]; $(w, "b").value = PRE[i][1]; draw(); });
    function draw() {
      var A = parseMon($(w, "a").value), B = parseMon($(w, "b").value);
      $(w, "a").classList.toggle("bad", !A); $(w, "b").classList.toggle("bad", !B);
      if (!A || !B || A.c.sgn() < 0 || B.c.sgn() < 0) { info.innerHTML = t3("Escriu dos monomis positius, per exemple \\(a=\\) <code>2x</code> i \\(b=\\) <code>5</code>.", "Escribe dos monomios positivos, por ejemplo \\(a=\\) <code>2x</code> y \\(b=\\) <code>5</code>.", "Type two positive monomials, e.g. \\(a=\\) <code>2x</code> and \\(b=\\) <code>5</code>.").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }); return; }
      var D = idDev(A, B), a = mT(A), b = mT(B), pa = mP(A), pb = mP(B);
      var two = "2\\cdot " + pa + "\\cdot " + pb;
      info.innerHTML = kv([
        [t3("Quadrat d'una suma", "Cuadrado de una suma", "Square of a sum"), tex("(" + a + "+" + b + ")^2=" + pa + "^2+" + two + "+" + pb + "^2") + "<br>" + tex("=" + mT(D.a2) + "+" + mT(D.ab2) + "+" + mT(D.b2) + "=") + " <strong>" + tex(pTex(D.sq)) + "</strong>"],
        [t3("Quadrat d'una diferència", "Cuadrado de una diferencia", "Square of a difference"), tex("(" + a + "-" + b + ")^2=" + pa + "^2-" + two + "+" + pb + "^2") + "<br>" + tex("=" + mT(D.a2) + "-" + mT(D.ab2) + "+" + mT(D.b2) + "=") + " <strong>" + tex(pTex(D.sqm)) + "</strong>"],
        [t3("Suma per diferència", "Suma por diferencia", "Sum times difference"), tex("(" + a + "+" + b + ")(" + a + "-" + b + ")=" + pa + "^2-" + pb + "^2=") + " <strong>" + tex(pTex(D.dif)) + "</strong>"],
        ["", "<small>" + t3("Error típic: \\((a+b)^2\\neq a^2+b^2\\). Falta el doble producte \\(2ab\\).", "Error típico: \\((a+b)^2\\neq a^2+b^2\\). Falta el doble producto \\(2ab\\).", "Common mistake: \\((a+b)^2\\neq a^2+b^2\\). The middle term \\(2ab\\) is missing.").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }) + "</small>"]
      ]);
    }
    ["a", "b"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 3.8 factor comú i identitats notables ---------- */
  function fciSteps(P0) {
    var P = pTrim(P0), k = 0, g = 0, allInt = P.every(function (c) { return c.d === 1; });
    while (k < P.length - 1 && P[k].zero()) k++;
    if (allInt) P.forEach(function (c) { g = gcd(g, c.n); }); else g = 1;
    if (!g) g = 1;
    if (P[P.length - 1].sgn() < 0 && allInt) g = -g;
    var Q = pTrim(P.slice(k).map(function (c) { return c.div(new Fr(g)); }));
    var out = { g: g, k: k, Q: Q, kind: null, fac: null };
    var nz = []; Q.forEach(function (c, i) { if (!c.zero()) nz.push(i); });
    var n = pDeg(Q);
    function sqrtM(c, e) { var r = sqrtFr(c); return r && e % 2 === 0 ? { c: r, e: e / 2 } : null; }
    if (nz.length === 2 && nz[0] === 0 && n % 2 === 0 && Q[n].sgn() > 0 && Q[0].sgn() < 0) {
      var A = sqrtM(Q[n], n), B = sqrtM(Q[0].neg(), 0);
      if (A && B) {
        out.kind = "dif"; out.A = A; out.B = B; out.fac = "(" + mT(A) + "+" + mT(B) + ")(" + mT(A) + "-" + mT(B) + ")";
        var A1 = sqrtM(A.c, A.e), B1 = sqrtM(B.c, 0);   // x^4-16 = (x^2+4)(x^2-4) = (x^2+4)(x+2)(x-2)
        if (A1 && B1) { out.again = "(" + mT(A) + "+" + mT(B) + ")(" + mT(A1) + "+" + mT(B1) + ")(" + mT(A1) + "-" + mT(B1) + ")"; out.fac2 = out.fac; out.fac = out.again; }
      }
    }
    if (nz.length === 3 && nz[0] === 0 && n % 2 === 0 && nz[1] === n / 2 && Q[n].sgn() > 0 && Q[0].sgn() > 0) {
      var A2 = sqrtM(Q[n], n), B2 = sqrtM(Q[0], 0);
      if (A2 && B2) {
        var mid = A2.c.mul(B2.c).mul(new Fr(2));
        if (Q[n / 2].eq(mid)) { out.kind = "sq"; out.A = A2; out.B = B2; out.fac = "(" + mT(A2) + "+" + mT(B2) + ")^2"; }
        else if (Q[n / 2].eq(mid.neg())) { out.kind = "sqm"; out.A = A2; out.B = B2; out.fac = "(" + mT(A2) + "-" + mT(B2) + ")^2"; }
        else { out.kind = "no3"; out.mid = mid; }
      }
    }
    var pre = (g === 1 ? "" : g === -1 ? "-" : String(g)) + xp(k);
    out.pre = pre;
    var one = pDeg(Q) === 0 && Q[0].eq(F1);
    out.total = out.fac ? pre + out.fac : one ? pre : (pre ? pre + "\\left(" + pTex(Q) + "\\right)" : pTex(Q));
    return out;
  }
  function wFci() {
    var w = byId("w-fci"); if (!w) return;
    var info = w.querySelector(".info");
    var PRE = ["6x^3-9x^2+3x", "x^2-25", "4x^2+12x+9", "2x^3-8x", "3x^4-6x^3+3x^2", "x^2+5x+6"];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(pTex(parsePoly(p))); }); }, function (i) { $(w, "p").value = PRE[i]; draw(); });
    function draw() {
      var P = parsePoly($(w, "p").value), good = P && pDeg(P) >= 1;
      $(w, "p").classList.toggle("bad", !good);
      if (!good) { info.innerHTML = u("badP"); return; }
      var S = fciSteps(P), rows = [], Q = S.Q;
      if (S.pre) rows.push(["1. " + t3("Factor comú", "Factor común", "Common factor"), tex(pTex(P) + "=" + S.pre + "\\left(" + pTex(Q) + "\\right)") + "<br><small>" + t3("Traiem ", "Sacamos ", "We take out ") + tex(S.pre) + (Math.abs(S.g) > 1 ? t3(" (el m.c.d. dels coeficients", " (el m.c.d. de los coeficientes", " (the GCD of the coefficients") + (S.k ? t3(" i la menor potència de ", " y la menor potencia de ", " and the lowest power of ") + tex("x") : "") + ")" : S.k ? t3(" (la menor potència de ", " (la menor potencia de ", " (the lowest power of ") + tex("x") + ")" : "") + ".</small>"]);
      else rows.push(["1. " + t3("Factor comú", "Factor común", "Common factor"), t3("No n'hi ha.", "No hay.", "There isn't one.")]);
      var lab = "2. " + t3("Identitat notable", "Identidad notable", "Special product");
      if (S.kind === "dif") rows.push([lab, t3("Diferència de quadrats: ", "Diferencia de cuadrados: ", "Difference of squares: ") + tex(pTex(Q) + "=" + mP(S.A) + "^2-" + mP(S.B) + "^2=" + (S.fac2 || S.fac)) + " " + ok(true) +
        (S.fac2 ? "<br>" + t3("El segon factor també és una diferència de quadrats: ", "El segundo factor también es una diferencia de cuadrados: ", "The second factor is also a difference of squares: ") + tex("=" + S.fac) : "")]);
      else if (S.kind === "sq" || S.kind === "sqm") {
        var sg = S.kind === "sq" ? "+" : "-";
        rows.push([lab, t3(S.kind === "sq" ? "Quadrat d'una suma: " : "Quadrat d'una diferència: ", S.kind === "sq" ? "Cuadrado de una suma: " : "Cuadrado de una diferencia: ", S.kind === "sq" ? "Square of a sum: " : "Square of a difference: ") +
          tex(pTex(Q) + "=" + mP(S.A) + "^2" + sg + "2\\cdot " + mP(S.A) + "\\cdot " + mP(S.B) + "+" + mP(S.B) + "^2=" + S.fac) + " " + ok(true)]);
      } else if (S.kind === "no3") rows.push([lab, t3("El primer i l'últim terme són quadrats, però el terme del mig hauria de ser ", "El primero y el último término son cuadrados, pero el término del medio tendría que ser ", "The first and last terms are squares, but the middle term would have to be ") + tex("\\pm" + mT({ c: S.mid, e: pDeg(Q) / 2 })) + ": " + t3("no és un quadrat perfecte. Prova amb Ruffini o amb l'equació de segon grau.", "no es un cuadrado perfecto. Prueba con Ruffini o con la ecuación de segundo grado.", "it isn't a perfect square. Try Ruffini or the quadratic formula.")]);
      else rows.push([lab, pDeg(Q) <= 1 ? t3("El que queda és de grau 1: ja no es pot descompondre més.", "Lo que queda es de grado 1: ya no se puede descomponer más.", "What's left has degree 1: it can't be split further.") : t3("No és cap identitat notable. Prova amb Ruffini (més avall) o, si és de grau 2, amb l'equació de segon grau.", "No es ninguna identidad notable. Prueba con Ruffini (más abajo) o, si es de grado 2, con la ecuación de segundo grado.", "It isn't a special product. Try Ruffini (below) or, for degree 2, the quadratic formula.")]);
      rows.push([t3("Resultat", "Resultado", "Result"), "<strong>" + tex(pTex(P) + "=" + S.total) + "</strong>"]);
      info.innerHTML = kv(rows);
    }
    $(w, "p").addEventListener("input", draw); onLang(draw);
  }

