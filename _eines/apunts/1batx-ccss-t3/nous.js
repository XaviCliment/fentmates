  /* =====================================================================
     Ginys nous de 1r Batx CCSS, unitat 3 (build.py els posa al lloc del marcador NOUS)
     ===================================================================== */

  /* ---------- lector d'expressions: polinomis amb parèntesis, producte i divisió per un nombre ---------- */
  function parseExpr(s) {
    if (s == null) return null;
    s = String(s).replace(/[−–]/g, "-").replace(/\s+/g, "").replace(/[·×]/g, "*").replace(/²/g, "^2").replace(/³/g, "^3").replace(/⁴/g, "^4")
      .replace(/,/g, ".").replace(/X/g, "x").replace(/:/g, "/");
    if (!s) return null;
    var i = 0;
    function pk() { return s.charAt(i); }
    function expr() {
      var p = unary(); if (!p) return null;
      while (pk() === "+" || pk() === "-") { var o = s.charAt(i++), q = unary(); if (!q) return null; p = o === "+" ? pAdd(p, q) : pSub(p, q); }
      return p;
    }
    function unary() {
      if (pk() === "-") { i++; var p = unary(); return p ? pScale(p, FM1) : null; }
      if (pk() === "+") { i++; return unary(); }
      return term();
    }
    function term() {
      var p = power(); if (!p) return null;
      for (;;) {
        var c = pk(), q;
        if (c === "*") { i++; q = power(); if (!q) return null; p = pMul(p, q); }
        else if (c === "/") { i++; q = power(); if (!q || pDeg(q) !== 0) return null; p = pScale(p, F1.div(q[0])); }
        else if (c === "(" || c === "x" || /[0-9.]/.test(c)) { q = power(); if (!q) return null; p = pMul(p, q); }
        else return p;
      }
    }
    function power() {
      var b = atom(); if (!b) return null;
      if (pk() !== "^") return b;
      i++; var m = s.slice(i).match(/^\d{1,2}/); if (!m || +m[0] > 8) return null; i += m[0].length;
      var r = [F1]; for (var k = 0; k < +m[0]; k++) r = pMul(r, b); return r;
    }
    function atom() {
      var c = pk();
      if (c === "(") { i++; var p = expr(); if (!p || pk() !== ")") return null; i++; return p; }
      if (c === "x") { i++; return [F0, F1]; }
      var m = s.slice(i).match(/^\d+(?:\.\d+)?/);
      if (m) { i += m[0].length; var f = parseFr(m[0]); return f ? [f] : null; }
      return null;
    }
    try { var p = expr(); return p && i === s.length ? pTrim(p) : null; } catch (e) { return null; }
  }
  function parseAny(s) { return parseExpr(s) || parsePoly(s); }
  var FLIP = { "<": ">", "<=": ">=", ">": "<", ">=": "<=" };
  function parseIneq(s) {
    s = String(s || "").replace(/≤|=</g, "<=").replace(/≥|=>/g, ">=");
    var m = s.match(/<=|>=|<|>/g); if (!m || m.length !== 1) return null;
    var op = m[0], k = s.indexOf(op), L = parseAny(s.slice(0, k)), R = parseAny(s.slice(k + op.length));
    return L && R ? { L: L, R: R, op: op } : null;
  }
  function holds(v, op) { var e = 1e-9; return op === "<" ? v < -e : op === "<=" ? v <= e : op === ">" ? v > e : v >= -e; }
  // solució de P(x) op 0 com a llista d'intervals {a, ac, b, bc}
  function solvePoly(P, op) {
    P = pTrim(P);
    var all = [{ a: -Infinity, ac: false, b: Infinity, bc: false }];
    if (pDeg(P) < 1) return { S: holds(pDeg(P) === -Infinity ? 0 : P[0].val(), op) ? all : [], pts: [] };
    var F = factorPoly(P), pts = [];
    F.roots.forEach(function (r) { if (!pts.some(function (q) { return Math.abs(q.v - r.v) < 1e-9; })) pts.push({ v: r.v, t: r.tex.replace("\\approx ", "") }); });
    pts.sort(function (a, b) { return a.v - b.v; });
    var S = [], i;
    for (i = 0; i <= pts.length; i++) {
      var a = i ? pts[i - 1].v : -Infinity, b = i < pts.length ? pts[i].v : Infinity;
      var mid = !isFinite(a) && !isFinite(b) ? 0 : !isFinite(a) ? b - 1 : !isFinite(b) ? a + 1 : (a + b) / 2;
      if (holds(pEvalN(P, mid), op)) S.push({ a: a, ac: false, b: b, bc: false });
      if (i < pts.length && holds(0, op)) S.push({ a: pts[i].v, ac: true, b: pts[i].v, bc: true });
    }
    return { S: norm(S), pts: pts, F: F };
  }
  function inter2(I, J) {
    var a, ac, b, bc;
    if (I.a > J.a) { a = I.a; ac = I.ac; } else if (J.a > I.a) { a = J.a; ac = J.ac; } else { a = I.a; ac = I.ac && J.ac; }
    if (I.b < J.b) { b = I.b; bc = I.bc; } else if (J.b < I.b) { b = J.b; bc = J.bc; } else { b = I.b; bc = I.bc && J.bc; }
    return { a: a, ac: ac, b: b, bc: bc };
  }
  function interS(S, T) { var out = []; S.forEach(function (I) { T.forEach(function (J) { var K = inter2(I, J); if (!isEmpty(K)) out.push(K); }); }); return norm(out); }
  function labOf(pts) { return function (v) { var p = pts.filter(function (q) { return Math.abs(q.v - v) < 1e-9; })[0]; return p ? p.t : nT(v); }; }
  function ineqT(I) { return pTex(I.L) + OPT[I.op] + pTex(I.R); }
  function rayS(c, op) { // x op c
    return op.charAt(0) === "<" ? [{ a: -Infinity, ac: false, b: c, bc: op === "<=" }] : [{ a: c, ac: op === ">=", b: Infinity, bc: false }];
  }

  /* ---------- 3.1 sistemes lineals 2x2 amb parèntesis i denominadors ---------- */
  // expressió lineal en x i y: [terme independent, coef. de x, coef. de y]
  function parseLin(s) {
    if (s == null) return null;
    s = String(s).replace(/[−–]/g, "-").replace(/\s+/g, "").replace(/[·×]/g, "*").replace(/,/g, ".").replace(/X/g, "x").replace(/Y/g, "y").replace(/:/g, "/");
    if (!s) return null;
    var i = 0;
    function pk() { return s.charAt(i); }
    function isC(p) { return p[1].zero() && p[2].zero(); }
    function add(p, q, k) { return [p[0].add(q[0].mul(k)), p[1].add(q[1].mul(k)), p[2].add(q[2].mul(k))]; }
    function sc(p, k) { return [p[0].mul(k), p[1].mul(k), p[2].mul(k)]; }
    function mul(p, q) { if (isC(p)) return sc(q, p[0]); if (isC(q)) return sc(p, q[0]); return null; }
    function expr() {
      var p = unary(); if (!p) return null;
      while (pk() === "+" || pk() === "-") { var o = s.charAt(i++), q = unary(); if (!q) return null; p = add(p, q, o === "+" ? F1 : FM1); }
      return p;
    }
    function unary() {
      if (pk() === "-") { i++; var p = unary(); return p ? sc(p, FM1) : null; }
      if (pk() === "+") { i++; return unary(); }
      return term();
    }
    function term() {
      var p = atom(); if (!p) return null;
      for (;;) {
        var c = pk(), q;
        if (c === "*") { i++; q = atom(); if (!q) return null; p = mul(p, q); if (!p) return null; }
        else if (c === "/") { i++; q = atom(); if (!q || !isC(q) || q[0].zero()) return null; p = sc(p, F1.div(q[0])); }
        else if (c === "(" || c === "x" || c === "y" || /[0-9.]/.test(c)) { q = atom(); if (!q) return null; p = mul(p, q); if (!p) return null; }
        else return p;
      }
    }
    function atom() {
      var c = pk();
      if (c === "(") { i++; var p = expr(); if (!p || pk() !== ")") return null; i++; return p; }
      if (c === "x") { i++; return [F0, F1, F0]; }
      if (c === "y") { i++; return [F0, F0, F1]; }
      var m = s.slice(i).match(/^\d+(?:\.\d+)?/);
      if (m) { i += m[0].length; var f = parseFr(m[0]); return f ? [f, F0, F0] : null; }
      return null;
    }
    try { var p = expr(); return p && i === s.length ? p : null; } catch (e) { return null; }
  }
  // equació lineal → {a, b, c} enters amb a x + b y = c (sense denominadors)
  function parseEq2(s) {
    var k = String(s || "").split("=");
    if (k.length !== 2) return null;
    var L = parseLin(k[0]), R = parseLin(k[1]); if (!L || !R) return null;
    var a = L[1].sub(R[1]), b = L[2].sub(R[2]), c = R[0].sub(L[0]);
    if (a.zero() && b.zero()) return null;
    var M = 1; [a, b, c].forEach(function (f) { M = M / gcd(M, f.d) * f.d; });
    var den = 1; L.concat(R).forEach(function (f) { den = den / gcd(den, f.d) * f.d; });
    a = a.mul(new Fr(M)); b = b.mul(new Fr(M)); c = c.mul(new Fr(M));
    // no simplifiquem per un factor comú: així es veu si les dues equacions són proporcionals
    var g = a.sgn() < 0 || (a.zero() && b.sgn() < 0) ? FM1 : F1;
    return { a: a.mul(g), b: b.mul(g), c: c.mul(g), mcm: den };
  }
  function eqT(E) {
    var s = ""; if (!E.a.zero()) s += monT(E.a, 1, "x", true); if (!E.b.zero()) s += monT(E.b, 1, "y", s === "");
    return s + "=" + frT(E.c);
  }
  function trm(c, v, val, first) { // terme c·v, o c·(valor) si v ja és coneguda
    if (c.zero()) return "";
    if (val == null) return monT(c, 1, v, first);
    var t = (c.eq(F1) ? "" : c.eq(FM1) ? "-" : frT(c) + "\\cdot") + frP(val);
    return (first || t.charAt(0) === "-" ? "" : "+") + t;
  }
  function wSis2() {
    var w = byId("w-sis2"); if (!w) return;
    var i1 = $(w, "e1"), i2 = $(w, "e2"), info = w.querySelector(".info"), svg = w.querySelector("svg"), st, res;
    var PRE = [["3(x-1) - 2(y+1) = 1", "2(x+y) - (x-3) = 13"], ["x/2 + y/3 = 4", "(x+2)/3 - (y-2)/4 = 1"], ["2x - y = 3", "4x - 2y = 6"], ["2(x-y) = 3", "x - y = 1"]];
    presetBtns($(w, "pre"), function () { return [t3("Amb parèntesis", "Con paréntesis", "With brackets"), t3("Amb denominadors", "Con denominadores", "With denominators"), t3("Infinites solucions", "Infinitas soluciones", "Infinitely many"), t3("Sense solució", "Sin solución", "No solution")]; },
      function (k) { i1.value = PRE[k][0]; i2.value = PRE[k][1]; read(); }, 0);
    function solve(E1, E2) {
      var D = E1.a.mul(E2.b).sub(E2.a.mul(E1.b)), r = { E1: E1, E2: E2, D: D }, v, p1, p2;
      if (!E1.b.zero() && !E2.b.zero()) { v = "y"; p1 = E1.b; p2 = E2.b; }
      else if (!E1.a.zero() && !E2.a.zero()) { v = "x"; p1 = E1.a; p2 = E2.a; }
      if (v) {
        var g = gcd(p1.n, p2.n) || 1, k1 = new Fr(p2.n / g), k2 = new Fr(p1.n / g);
        if (k1.sgn() < 0) { k1 = k1.neg(); k2 = k2.neg(); }
        var w2 = v === "y" ? "x" : "y", R = (v === "y" ? E1.a.mul(k1).sub(E2.a.mul(k2)) : E1.b.mul(k1).sub(E2.b.mul(k2))), S = E1.c.mul(k1).sub(E2.c.mul(k2));
        r.el = { v: v, w: w2, k1: k1, k2: k2, R: R, S: S };
      }
      // si no es pot eliminar cap incògnita, cada equació en té només una i D no és 0
      if (D.zero()) r.kind = r.el.S.zero() ? "SCI" : "SI";
      else {
        r.kind = "SCD";
        r.x = E1.c.mul(E2.b).sub(E2.c.mul(E1.b)).div(D); r.y = E1.a.mul(E2.c).sub(E2.a.mul(E1.c)).div(D);
      }
      return r;
    }
    function read() {
      var E1 = parseEq2(i1.value), E2 = parseEq2(i2.value);
      i1.classList.toggle("bad", !E1); i2.classList.toggle("bad", !E2);
      res = E1 && E2 ? solve(E1, E2) : null;
      st.reset(1);
    }
    function rt2(s) { return s.replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }); }
    function show(k) {
      if (!res) {
        info.innerHTML = t3("Escriu dues equacions de primer grau amb \\(x\\) i \\(y\\), per exemple <code>3(x-1) - 2(y+1) = 1</code> o <code>x/2 + y/3 = 4</code>.",
          "Escribe dos ecuaciones de primer grado con \\(x\\) e \\(y\\), por ejemplo <code>3(x-1) - 2(y+1) = 1</code> o <code>x/2 + y/3 = 4</code>.",
          "Type two linear equations in \\(x\\) and \\(y\\), for example <code>3(x-1) - 2(y+1) = 1</code> or <code>x/2 + y/3 = 4</code>.").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); });
        svg.innerHTML = ""; return;
      }
      var r = res, L = function (i) { return u("step") + " " + i; }, rows = [];
      var mc = [r.E1.mcm, r.E2.mcm].map(function (m, i) { return m > 1 ? "\\(E_" + (i + 1) + "\\): m.c.m. = " + m : ""; }).filter(Boolean).join("; ");
      rows.push([L(1), t3("Traiem parèntesis i denominadors i deixem cada equació en la forma \\(ax+by=c\\)", "Quitamos paréntesis y denominadores y dejamos cada ecuación en la forma \\(ax+by=c\\)", "Remove brackets and denominators and write each equation as \\(ax+by=c\\)") +
        (mc ? " (" + t3("multipliquem per", "multiplicamos por", "multiply by") + " " + mc.replace(/m\.c\.m\./g, t3("m.c.m.", "m.c.m.", "LCM")) + ")" : "") + ":<br>" + tex("\\begin{cases}" + eqT(r.E1) + "\\\\ " + eqT(r.E2) + "\\end{cases}")]);
      rows[0][1] = rt2(rows[0][1]);
      if (k >= 2) {
        if (r.el) {
          var e = r.el, op = e.k2.sgn() > 0 ? "-" : "+", k2a = e.k2.abs();
          var comb = (e.k1.eq(F1) ? "" : frT(e.k1)) + "E_1" + op + (k2a.eq(F1) ? "" : frT(k2a)) + "E_2";
          rows.push([L(2), rt2(t3("Reducció: eliminem la \\(" + e.v + "\\) fent ", "Reducción: eliminamos la \\(" + e.v + "\\) haciendo ", "Elimination: remove \\(" + e.v + "\\) by computing ")) + tex(comb) + "<br>" + tex((e.R.zero() ? "0" + e.w : monT(e.R, 1, e.w, true)) + "=" + frT(e.S))]);
        } else rows.push([L(2), t3("Cada equació té una sola incògnita: les aïllem directament.", "Cada ecuación tiene una sola incógnita: las despejamos directamente.", "Each equation has a single unknown: solve them directly.")]);
      }
      if (k >= 3) {
        if (r.kind === "SCD") {
          var txt;
          if (r.el) {
            var e2 = r.el, wv = e2.w === "x" ? r.x : r.y, vv = e2.v === "x" ? r.x : r.y, Eu = (e2.v === "y" ? !r.E1.b.zero() : !r.E1.a.zero()) ? r.E1 : r.E2, n = Eu === r.E1 ? "1" : "2";
            var lhs = trm(Eu.a, "x", e2.w === "x" ? wv : null, true); lhs += trm(Eu.b, "y", e2.w === "y" ? wv : null, lhs === "");
            txt = tex(e2.w + "=" + frT(wv)) + ". " + t3("Substituïm en ", "Sustituimos en ", "Substitute into ") + tex("E_" + n) + ":" + "<br>" +
              tex(lhs + "=" + frT(Eu.c) + "\\ \\Rightarrow\\ " + e2.v + "=" + frT(vv));
          } else txt = tex("x=" + frT(r.x) + ",\\quad y=" + frT(r.y));
          rows.push([L(3), txt]);
        } else if (r.kind === "SCI") rows.push([L(3), t3("Queda \\(0=0\\): les dues equacions són equivalents (proporcionals).", "Queda \\(0=0\\): las dos ecuaciones son equivalentes (proporcionales).", "We get \\(0=0\\): both equations are equivalent (proportional).").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); })]);
        else rows.push([L(3), t3("Queda una igualtat impossible, ", "Queda una igualdad imposible, ", "We get an impossible equality, ") + tex("0=" + frT(r.el.S)) + t3(": les equacions es contradiuen.", ": las ecuaciones se contradicen.", ": the equations contradict each other.")]);
      }
      if (k >= 4) {
        var B = { SCD: '<span class="badge ok">SCD</span> ' + t3("una única solució: les rectes es tallen en un punt", "una única solución: las rectas se cortan en un punto", "one solution: the lines cross at one point"),
          SCI: '<span class="badge ev">SCI</span> ' + t3("infinites solucions: les rectes són coincidents", "infinitas soluciones: las rectas son coincidentes", "infinitely many solutions: the lines coincide"),
          SI: '<span class="badge as">SI</span> ' + t3("cap solució: les rectes són paral·leles", "ninguna solución: las rectas son paralelas", "no solution: the lines are parallel") };
        rows.push([t3("Classificació", "Clasificación", "Type"), B[r.kind]]);
        if (r.kind === "SCD") rows.push([t3("Solució", "Solución", "Solution"), tex("(x,y)=\\left(" + frT(r.x) + ",\\ " + frT(r.y) + "\\right)")]);
        if (r.kind === "SCI") {
          var E = r.E1, sol = !E.b.zero() ? "\\left(\\lambda,\\ " + pTex([E.c.div(E.b), E.a.neg().div(E.b)], "\\lambda") + "\\right)" : "\\left(" + frT(E.c.div(E.a)) + ",\\ \\lambda\\right)";
          rows.push([t3("Solució", "Solución", "Solution"), tex("(x,y)=" + sol + ",\\ \\lambda\\in\\mathbb R")]);
        }
      }
      info.innerHTML = kv(rows);
      draw(k);
    }
    function draw(k) {
      var cx = 0, cy = 0;
      if (res.kind === "SCD") { cx = res.x.val(); cy = res.y.val(); }
      var R = Math.max(6, Math.ceil(Math.max(Math.abs(cx), Math.abs(cy)) + 3)), G = gview({ x0: -R, x1: R, y0: -R, y1: R, W: 320, H: 320 }), Cl = clipSvg(svg, G), g = G.g + Cl.open;
      [[res.E1, COL.a], [res.E2, COL.b]].forEach(function (p, i) {
        var E = p[0], dash = res.kind === "SCI" && i ? "7 6" : null;
        if (!E.b.zero()) g += curve(G, function (x) { return (E.c.val() - E.a.val() * x) / E.b.val(); }, p[1], { dash: dash, w: dash ? 3.4 : 2.6 });
        else { var x0 = E.c.val() / E.a.val(); g += '<line x1="' + G.X(x0) + '" x2="' + G.X(x0) + '" y1="' + G.Y(-R) + '" y2="' + G.Y(R) + '" stroke="' + p[1] + '" stroke-width="2.6"' + (dash ? ' stroke-dasharray="' + dash + '"' : "") + "/>"; }
      });
      if (res.kind === "SCD" && k >= 4) g += dot(G, cx, cy, COL.r);
      svg.setAttribute("viewBox", "0 0 " + G.W + " " + G.H); svg.innerHTML = g + Cl.close;
    }
    [i1, i2].forEach(function (e) { e.addEventListener("input", read); });
    st = stepper(w, function () { return res ? 4 : 0; }, show);
    read(); onLang(function () { st.upd(); });
  }

  /* ---------- 3.2 mètode de Gauss ---------- */
  function wGauss() {
    var w = byId("w-gauss"); if (!w) return;
    var grid = $(w, "grid"), out = $(w, "steps"), info = w.querySelector(".info"), ins = [], st, res;
    var PRE = [[[1, 1, 1, 6], [2, -1, 1, 3], [1, 2, -1, 2]], [[1, -1, 1, 1], [2, 1, -1, 5], [1, 2, -2, 4]], [[1, -1, 1, 1], [2, 1, -1, 5], [1, 2, -2, 5]], [[1, 1, 1, 10], [8, 6, 4, 56], [1, 1, -1, 0]]];
    for (var i = 0; i < 3; i++) for (var j = 0; j < 4; j++) {
      var inp = document.createElement("input"); inp.className = "tin s" + (j === 3 ? " rhs" : ""); inp.inputMode = "decimal"; inp.autocomplete = "off"; inp.value = PRE[0][i][j];
      inp.setAttribute("aria-label", (j < 3 ? "xyz"[j] : "=") + " (" + (i + 1) + ")");
      inp.addEventListener("input", read); grid.appendChild(inp); ins.push(inp);
    }
    presetBtns($(w, "pre"), function () { return [t3("Exemple SCD", "Ejemplo SCD", "Example (unique)"), t3("Exemple SCI", "Ejemplo SCI", "Example (infinite)"), t3("Exemple SI", "Ejemplo SI", "Example (none)"), t3("Problema de les entrades", "Problema de las entradas", "Tickets problem")]; }, function (k) {
      PRE[k].forEach(function (r, i) { r.forEach(function (v, j) { ins[i * 4 + j].value = v; }); }); read();
    });
    function mT(M, piv) {
      return "\\left(\\begin{array}{rrr|r}" + M.map(function (r) { return r.map(frT).join("&"); }).join("\\\\") + "\\end{array}\\right)";
    }
    function opT(i, k, al, be) { // F_i -> al F_i - be F_k
      var s = "F_" + (i + 1) + "\\to " + (al.eq(F1) ? "" : frT(al)) + "F_" + (i + 1);
      var b = be.neg(); s += (b.sgn() > 0 ? "+" : "-") + (b.abs().eq(F1) ? "" : frT(b.abs())) + "F_" + (k + 1);
      return s;
    }
    function solve(M0) {
      var M = M0.map(function (r) { return r.slice(); }), steps = [{ M: M.map(function (r) { return r.slice(); }), ops: [] }], r = 0, pivots = [];
      for (var c = 0; c < 3 && r < 3; c++) {
        var p = -1; for (var i = r; i < 3; i++) if (!M[i][c].zero()) { p = i; break; }
        if (p < 0) continue;
        var ops = [];
        if (p !== r) { var t = M[p]; M[p] = M[r]; M[r] = t; ops.push("F_" + (r + 1) + "\\leftrightarrow F_" + (p + 1)); }
        for (i = r + 1; i < 3; i++) {
          if (M[i][c].zero()) continue;
          var pv = M[r][c], q = M[i][c], al, be;
          if (pv.d === 1 && q.d === 1) { var g = gcd(pv.n, q.n); al = new Fr(pv.n / g); be = new Fr(q.n / g); if (al.sgn() < 0) { al = al.neg(); be = be.neg(); } }
          else { al = F1; be = q.div(pv); }
          for (var j = 0; j < 4; j++) M[i][j] = M[i][j].mul(al).sub(M[r][j].mul(be));
          ops.push(opT(i, r, al, be));
        }
        pivots.push(c);
        if (ops.length) steps.push({ M: M.map(function (x) { return x.slice(); }), ops: ops });
        r++;
      }
      var incompatible = M.some(function (row) { return row[0].zero() && row[1].zero() && row[2].zero() && !row[3].zero(); });
      var rank = M.filter(function (row) { return !(row[0].zero() && row[1].zero() && row[2].zero()); }).length;
      var kind = incompatible ? "SI" : rank === 3 ? "SCD" : "SCI", sol = null;
      if (!incompatible) {
        // forma reduïda per a escriure la solució
        var E = M.map(function (x) { return x.slice(); }), pr = 0, pc = [];
        for (c = 0; c < 3 && pr < 3; c++) {
          var pp = -1; for (i = pr; i < 3; i++) if (!E[i][c].zero()) { pp = i; break; }
          if (pp < 0) continue;
          var tt = E[pp]; E[pp] = E[pr]; E[pr] = tt;
          var inv = F1.div(E[pr][c]); for (j = 0; j < 4; j++) E[pr][j] = E[pr][j].mul(inv);
          for (i = 0; i < 3; i++) if (i !== pr && !E[i][c].zero()) { var f = E[i][c]; for (j = 0; j < 4; j++) E[i][j] = E[i][j].sub(E[pr][j].mul(f)); }
          pc.push(c); pr++;
        }
        var free = [0, 1, 2].filter(function (c2) { return pc.indexOf(c2) < 0; }), names = ["\\lambda", "\\mu", "\\nu"], expr = [];
        free.forEach(function (c2, k2) { expr[c2] = names[k2]; });
        pc.forEach(function (c2, k2) {
          var s = frT(E[k2][3]), first = E[k2][3].zero();
          if (first) s = "";
          free.forEach(function (fc, k3) {
            var co = E[k2][fc].neg(); if (co.zero()) return;
            s += (co.sgn() < 0 ? "-" : s ? "+" : "") + (co.abs().eq(F1) ? "" : frT(co.abs())) + names[k3];
          });
          expr[c2] = s || "0";
        });
        sol = { expr: expr, free: free.length, names: names };
      }
      return { steps: steps, kind: kind, sol: sol, rank: rank, M: M };
    }
    function read() {
      var M = [], good = true;
      for (var i = 0; i < 3; i++) { M.push([]); for (var j = 0; j < 4; j++) { var f = parseFr(ins[i * 4 + j].value || "0"); ins[i * 4 + j].classList.toggle("bad", !f); if (!f) good = false; M[i].push(f || F0); } }
      res = good ? solve(M) : null;
      st.reset(1);
    }
    function show(k) {
      if (!res) { out.innerHTML = ""; info.innerHTML = t3("Escriu nombres enters, decimals o fraccions.", "Escribe números enteros, decimales o fracciones.", "Type whole numbers, decimals or fractions."); return; }
      var h = "";
      res.steps.slice(0, k).forEach(function (s, i) {
        h += '<div class="gstep">' + (i ? tex("\\xrightarrow[" + (s.ops[1] || "") + (s.ops[2] ? "\\\\ " + s.ops[2] : "") + "]{" + s.ops[0] + "}") : "") + tex(mT(s.M), false) + "</div>";
      });
      out.innerHTML = h;
      if (k < res.steps.length) { info.innerHTML = '<span class="step-count">' + t3("Fem zeros davall de la diagonal…", "Hacemos ceros debajo de la diagonal…", "Making zeros below the diagonal…") + "</span>"; return; }
      var last = res.M[2], rows = [];
      var le = ""; ["x", "y", "z"].forEach(function (v, i) { if (!last[i].zero()) le += monT(last[i], 1, v, le === ""); });
      rows.push([t3("Última equació", "Última ecuación", "Last equation"), tex((le || "0") + "=" + frT(last[3]))]);
      var badge = { SCD: '<span class="badge ok">SCD</span> ' + t3("Compatible determinat: una única solució", "Compatible determinado: una única solución", "Consistent, independent: exactly one solution"),
        SCI: '<span class="badge ev">SCI</span> ' + t3("Compatible indeterminat: infinites solucions", "Compatible indeterminado: infinitas soluciones", "Consistent, dependent: infinitely many solutions"),
        SI: '<span class="badge as">SI</span> ' + t3("Incompatible: cap solució (apareix ", "Incompatible: ninguna solución (aparece ", "Inconsistent: no solution (we get ") + tex("0=" + frT(res.M.filter(function (r) { return r[0].zero() && r[1].zero() && r[2].zero() && !r[3].zero(); })[0] ? res.M.filter(function (r) { return r[0].zero() && r[1].zero() && r[2].zero() && !r[3].zero(); })[0][3] : F0)) + ")" };
      rows.push([t3("Classificació", "Clasificación", "Type"), badge[res.kind]]);
      if (res.sol) rows.push([t3("Solució", "Solución", "Solution"), tex("(x,y,z)=\\left(" + res.sol.expr.join(",\\ ") + "\\right)" + (res.sol.free ? ",\\ \\ " + res.sol.names.slice(0, res.sol.free).join(",") + "\\in\\mathbb R" : ""))]);
      info.innerHTML = kv(rows);
    }
    st = stepper(w, function () { return res ? res.steps.length : 0; }, show);
    read(); onLang(function () { st.upd(); });
  }

  /* ---------- 3.3 recta i circumferència ---------- */
  function wNl() {
    var w = byId("w-nl"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg");
    function draw() {
      var R2 = +$(w, "r").value, m = +$(w, "m").value, n = +$(w, "n").value;
      $(w, "rv").textContent = R2; $(w, "mv").textContent = decS(m, 1).replace("-", "−"); $(w, "nv").textContent = decS(n, 1).replace("-", "−");
      var M = toFr(m), N = toFr(n), RR = new Fr(R2), rows = [];
      rows.push([t3("Sistema", "Sistema", "System"), tex("\\begin{cases}x^2+y^2=" + R2 + "\\\\ y=" + pTex([N, M]) + "\\end{cases}")]);
      var a = F1.add(M.mul(M)), b = M.mul(N).mul(2), c = N.mul(N).sub(RR);
      rows.push([t3("Substituïm", "Sustituimos", "Substitute"), tex("x^2+\\left(" + pTex([N, M]) + "\\right)^2=" + R2 + "\\ \\Rightarrow\\ " + pTex([c, b, a]) + "=0")]);
      var Q = quadRoots(a, b, c), pts = [];
      rows.push(["Δ", tex("\\Delta=" + frT(Q.D)) + " → " + (Q.kind === "none" ? t3("cap punt de tall", "ningún punto de corte", "no intersection") : Q.kind === "double" ? t3("un punt: la recta és tangent", "un punto: la recta es tangente", "one point: the line is tangent") : t3("dos punts de tall", "dos puntos de corte", "two intersection points"))]);
      Q.roots.forEach(function (r) {
        var yT;
        if (r.fr) yT = frT(M.mul(r.fr).add(N));
        else { var A2 = M.mul(r.A).add(N), B2 = M.abs().mul(r.B), s2 = M.sgn() < 0 ? -r.s : r.s; yT = M.zero() ? frT(N) : irrT(A2, B2, r.m, s2); }
        pts.push({ x: r.v, y: m * r.v + n, t: "\\left(" + r.tex + ",\\ " + yT + "\\right)" });
      });
      if (pts.length) rows.push([t3("Solucions", "Soluciones", "Solutions"), tex(pts.map(function (p) { return p.t; }).join(",\\ "))]);
      info.innerHTML = kv(rows);
      var G = gview({ x0: -7, x1: 7, y0: -7, y1: 7, W: 320, H: 320, sx: 1, sy: 1 }), Cl = clipSvg(svg, G), r0 = Math.sqrt(R2);
      var g = G.g + Cl.open + '<circle cx="' + G.X(0) + '" cy="' + G.Y(0) + '" r="' + (G.X(r0) - G.X(0)) + '" fill="none" stroke="' + COL.a + '" stroke-width="2.6"/>' + curve(G, function (x) { return m * x + n; }, COL.b);
      pts.forEach(function (p) { g += dot(G, p.x, p.y, COL.r); });
      svg.setAttribute("viewBox", "0 0 " + G.W + " " + G.H); svg.innerHTML = g + Cl.close;
    }
    ["r", "m", "n"].forEach(function (k) { $(w, k).addEventListener("input", draw); });
    onLang(draw);
  }



  /* ---------- 3.4 inequacions de primer grau pas a pas ---------- */
  function wLin() {
    var w = byId("w-lin"); if (!w) return;
    var inp = $(w, "in"), info = w.querySelector(".info"), svg = w.querySelector("svg.nl-svg"), st, res;
    var PRE = [["3x-5 <= x+7", "3x-5\\le x+7"], ["2(x-1) > 5x+4", "2(x-1)\\gt 5x+4"], ["(x+1)/2 - x/3 >= 1", "\\frac{x+1}{2}-\\frac{x}{3}\\ge 1"],
      ["4-x < 2(3-x)", "4-x\\lt 2(3-x)"], ["2(x+1) >= 2x-3", "2(x+1)\\ge 2x-3"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(p[1]); }); }, function (k) { inp.value = PRE[k][0]; read(); });
    function read() {
      var I = parseIneq(inp.value);
      res = null;
      if (I && pDeg(I.L) <= 1 && pDeg(I.R) <= 1) {
        // denominadors: multipliquem els dos membres pel m.c.m. (positiu)
        var M = 1; I.L.concat(I.R).forEach(function (c) { M = M / gcd(M, c.d) * c.d; });
        if (M > 1) { I.L = pScale(I.L, new Fr(M)); I.R = pScale(I.R, new Fr(M)); I.mcm = M; }
        var A = (I.L[1] || F0).sub(I.R[1] || F0), B = (I.R[0] || F0).sub(I.L[0] || F0);
        res = { I: I, A: A, B: B };
        if (!A.zero()) { res.c = B.div(A); res.op2 = A.sgn() < 0 ? FLIP[I.op] : I.op; res.S = rayS(res.c.val(), res.op2); }
        else { res.ok = holds(-B.val(), I.op); res.S = res.ok ? [{ a: -Infinity, ac: false, b: Infinity, bc: false }] : []; }
      }
      inp.classList.toggle("bad", !res);
      st.reset(1);
    }
    function show(k) {
      if (!res) {
        info.innerHTML = t3("Escriu una inequació de primer grau, per exemple <code>2(x-1) &gt; 5x+4</code> o <code>(x+1)/2 - x/3 &gt;= 1</code>.",
          "Escribe una inecuación de primer grado, por ejemplo <code>2(x-1) &gt; 5x+4</code> o <code>(x+1)/2 - x/3 &gt;= 1</code>.",
          "Type a linear inequality, for example <code>2(x-1) &gt; 5x+4</code> or <code>(x+1)/2 - x/3 &gt;= 1</code>.");
        svg.innerHTML = ""; return;
      }
      var r = res, op = r.I.op, L = function (i) { return u("step") + " " + i; }, rows = [];
      rows.push([L(1), t3("Traiem parèntesis i denominadors i reduïm cada membre:", "Quitamos paréntesis y denominadores y reducimos cada miembro:", "Remove brackets and denominators and simplify each side:") +
        (r.I.mcm ? " " + t3("multipliquem per m.c.m. = ", "multiplicamos por m.c.m. = ", "multiply by LCM = ") + r.I.mcm + "," : "") + "<br>" + tex(ineqT(r.I))]);
      if (k >= 2) rows.push([L(2), t3("Passem els termes amb \\(x\\) a l'esquerra i els nombres a la dreta (canviant-los de signe):", "Pasamos los términos con \\(x\\) a la izquierda y los números a la derecha (cambiándolos de signo):", "Move the \\(x\\) terms to the left and the numbers to the right (changing their sign):").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }) +
        "<br>" + tex((r.A.zero() ? "0x" : pTex([F0, r.A])) + OPT[op] + frT(r.B))]);
      if (k >= 3) {
        if (r.A.zero()) rows.push([L(3), t3("No queda cap \\(x\\): ", "No queda ninguna \\(x\\): ", "No \\(x\\) is left: ").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }) + tex("0" + OPT[op] + frT(r.B)) + " " + ok(r.ok) + " " +
          (r.ok ? t3("és cert per a qualsevol valor de x.", "es cierto para cualquier valor de x.", "is true for every value of x.") : t3("no és cert mai.", "no es cierto nunca.", "is never true."))]);
        else if (r.A.eq(F1)) rows.push([L(3), t3("La \\(x\\) ja està aïllada.", "La \\(x\\) ya está despejada.", "\\(x\\) is already isolated.").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); })]);
        else rows.push([L(3), (r.A.sgn() < 0 ? "<strong>" + t3("Dividim entre ", "Dividimos entre ", "Divide by ") + tex(frT(r.A)) + t3(", que és negatiu: la desigualtat canvia de sentit.", ", que es negativo: la desigualdad cambia de sentido.", ", which is negative: the inequality is reversed.") + "</strong>"
          : t3("Dividim entre ", "Dividimos entre ", "Divide by ") + tex(frT(r.A)) + t3(", que és positiu: la desigualtat no canvia.", ", que es positivo: la desigualdad no cambia.", ", which is positive: the inequality stays the same.")) + "<br>" + tex("x" + OPT[r.op2] + frT(r.c))]);
      }
      if (k >= 4) rows.push([t3("Solució", "Solución", "Solution"), tex(r.A.zero() ? (r.ok ? "x\\in\\mathbb R" : "\\text{" + t3("no té solució", "no tiene solución", "no solution") + "}") : "x\\in " + setTL(r.S, function (v) { return frT(r.c); }))]);
      info.innerHTML = kv(rows);
      var W = svgW(svg);
      if (k >= 4) paint(svg, nline([{ S: r.S, c: COL.r }], { W: W, range: r.A.zero() ? [-5, 5] : range([[{ a: r.c.val(), b: r.c.val() }]]) }), W);
      else svg.innerHTML = "";
    }
    inp.addEventListener("input", read);
    st = stepper(w, function () { return res ? 4 : 0; }, show);
    read(); onLang(function () { st.upd(); });
  }

  /* ---------- 3.6 sistemes d'inequacions amb una incògnita ---------- */
  function wSys1() {
    var w = byId("w-sys1"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg.nl-svg"), box = $(w, "rows"), R = [], CS = [COL.a, COL.b, COL.v];
    for (var i = 0; i < 3; i++) {
      var row = document.createElement("div"); row.className = "hrow";
      var cb = document.createElement("input"); cb.type = "checkbox"; cb.checked = i < 2;
      var d = document.createElement("i"); d.className = "dot"; d.style.background = CS[i];
      var t = document.createElement("input"); t.className = "tin w"; t.autocomplete = "off"; t.spellcheck = false; t.style.maxWidth = "230px";
      row.appendChild(cb); row.appendChild(d); row.appendChild(t); box.appendChild(row); R.push({ cb: cb, t: t });
      cb.addEventListener("change", draw); t.addEventListener("input", draw);
    }
    var PRE = [["3x-2 <= x+4", "2x+1 > -3", ""], ["x^2-x-6 <= 0", "x-1 > 0", ""], ["x-2 > 0", "x+1 < 0", ""], ["2(x-3) < x+1", "x^2 >= 4", "x >= 0"]];
    function set(k) { PRE[k].forEach(function (s, i) { R[i].t.value = s; R[i].cb.checked = !!s; }); }
    set(0);
    presetBtns($(w, "pre"), function () { return PRE.map(function (_, i) { return t3("Exemple ", "Ejemplo ", "Example ") + (i + 1); }); }, function (k) { set(k); draw(); }, 0);
    function draw() {
      var rows = [], kvs = [], pts = [], S = null, bad = false;
      R.forEach(function (r, i) {
        r.t.parentNode.classList.toggle("off", !r.cb.checked);
        if (!r.cb.checked) { r.t.classList.remove("bad"); return; }
        var I = parseIneq(r.t.value), ok2 = I && pDeg(pSub(I.L, I.R)) <= 6;
        r.t.classList.toggle("bad", !ok2);
        if (!ok2) { bad = true; return; }
        var sol = solvePoly(pSub(I.L, I.R), I.op);
        pts = pts.concat(sol.pts);
        rows.push({ S: sol.S, c: CS[i], l: "(" + (i + 1) + ")" });
        kvs.push(['<i class="dot" style="background:' + CS[i] + '"></i>' + tex(ineqT(I)), tex("x\\in " + setTL(sol.S, labOf(sol.pts)))]);
        S = S ? interS(S, sol.S) : sol.S;
      });
      var W = svgW(svg);
      if (bad || !rows.length) {
        info.innerHTML = bad ? t3("Revisa les inequacions marcades en roig (exemple: <code>x^2-x-6 &lt;= 0</code>).", "Revisa las inecuaciones marcadas en rojo (ejemplo: <code>x^2-x-6 &lt;= 0</code>).", "Check the inequalities marked in red (example: <code>x^2-x-6 &lt;= 0</code>).")
          : t3("Activa alguna inequació.", "Activa alguna inecuación.", "Turn on an inequality.");
        svg.innerHTML = ""; return;
      }
      kvs.push(["<strong>" + t3("Solució del sistema", "Solución del sistema", "Solution of the system") + "</strong>", S.length ? tex("x\\in " + setTL(S, labOf(pts))) : t3("no té solució (la intersecció és buida)", "no tiene solución (la intersección es vacía)", "no solution (the intersection is empty)")]);
      info.innerHTML = kv(kvs);
      rows.push({ S: S, c: COL.r, l: "S" });
      var all = rows.map(function (r) { return r.S; }).concat([pts.map(function (p) { return { a: p.v, b: p.v }; })]);
      paint(svg, nline(rows, { W: W, range: range(all) }), W);
    }
    onLang(draw);
  }

  /* ---------- 3.9 programació lineal ---------- */
  function wPl() {
    var w = byId("w-pl"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg"), rowsBox = $(w, "rows"), R = [], st, res;
    var OPS = ["<=", ">=", "<", ">"], SYM = { "<": "<", "<=": "≤", ">": ">", ">=": "≥" }, CS = [COL.a, COL.b, COL.v, "#0891b2", "#a16207"];
    var goal = $(w, "goal"), ip = $(w, "p"), iq = $(w, "q");
    function mk(v) { var x = document.createElement("input"); x.className = "tin s"; x.inputMode = "decimal"; x.autocomplete = "off"; x.value = v; return x; }
    function txt(t) { var s = document.createElement("span"); s.textContent = t; return s; }
    for (var i = 0; i < 5; i++) {
      var row = document.createElement("div"); row.className = "hrow";
      var cb = document.createElement("input"); cb.type = "checkbox";
      var ia = mk("1"), ib = mk("1"), ic = mk("0"), sel = document.createElement("select");
      OPS.forEach(function (o) { sel.add(new Option(SYM[o], o)); });
      var dotc = document.createElement("i"); dotc.className = "dot"; dotc.style.background = CS[i];
      [cb, dotc, ia, txt("x +"), ib, txt("y"), sel, ic].forEach(function (e) { row.appendChild(e); });
      rowsBox.appendChild(row); R.push({ cb: cb, a: ia, b: ib, op: sel, c: ic });
      [cb, ia, ib, sel, ic].forEach(function (e) { e.addEventListener("input", read); e.addEventListener("change", read); });
    }
    [ip, iq].forEach(function (e) { e.addEventListener("input", read); });
    goal.addEventListener("change", read);
    var PRE = [
      { g: "max", p: 30, q: 40, c: [[1, 2, "<=", 16], [1, 1, "<=", 10], [1, 0, ">=", 0], [0, 1, ">=", 0]] },
      { g: "min", p: 3, q: 2, c: [[1, 2, ">=", 8], [2, 1, ">=", 10], [1, 0, ">=", 0], [0, 1, ">=", 0]] },
      { g: "max", p: 1, q: 1, c: [[1, 2, "<=", 16], [1, 1, "<=", 10], [1, 0, ">=", 0], [0, 1, ">=", 0]] },
      { g: "max", p: 1, q: 1, c: [[1, 2, ">=", 8], [2, 1, ">=", 10], [1, 0, ">=", 0], [0, 1, ">=", 0]] }
    ];
    function set(k) {
      var P = PRE[k]; goal.value = P.g; ip.value = P.p; iq.value = P.q;
      R.forEach(function (r, i) { var c = P.c[i]; r.cb.checked = !!c; if (c) { r.a.value = c[0]; r.b.value = c[1]; r.op.value = c[2]; r.c.value = c[3]; } });
    }
    function goalOpts() { goal.innerHTML = ""; goal.add(new Option(t3("Maximitzar", "Maximizar", "Maximise"), "max")); goal.add(new Option(t3("Minimitzar", "Minimizar", "Minimise"), "min")); }
    goalOpts(); set(0);
    presetBtns($(w, "pre"), function () { return [t3("Joguets (màxim)", "Juguetes (máximo)", "Toys (maximum)"), t3("Pinso (mínim)", "Pienso (mínimo)", "Feed (minimum)"), t3("Infinites solucions", "Infinitas soluciones", "Infinitely many solutions"), t3("Sense òptim", "Sin óptimo", "No optimum")]; },
      function (k) { set(k); read(); }, 0);
    function read() {
      var cons = [], bad = false;
      R.forEach(function (r, i) {
        var a = parseFr(r.a.value || "0"), b = parseFr(r.b.value || "0"), c = parseFr(r.c.value || "0");
        [r.a, r.b, r.c].forEach(function (e) { e.classList.toggle("bad", r.cb.checked && !parseFr(e.value || "0")); });
        r.a.parentNode.classList.toggle("off", !r.cb.checked);
        if (!r.cb.checked) return;
        if (!a || !b || !c || (a.zero() && b.zero())) { bad = true; return; }
        cons.push({ a: a.val(), b: b.val(), c: c.val(), op: r.op.value, col: CS[i] });
      });
      var p = parseFr(ip.value || "0"), q = parseFr(iq.value || "0");
      ip.classList.toggle("bad", !p); iq.classList.toggle("bad", !q);
      res = null;
      if (!bad && p && q && cons.length) {
        var BIG = 1e6, PB = region(cons, [-BIG, BIG, -BIG, BIG]);
        var F = function (pt) { return p.val() * pt[0] + q.val() * pt[1]; }, mx = goal.value === "max";
        var V = PB.filter(function (pt) { return Math.abs(pt[0]) < BIG / 2 && Math.abs(pt[1]) < BIG / 2; });
        res = { cons: cons, P: PB, V: V, F: F, p: p, q: q, mx: mx, empty: PB.length < 3, bounded: V.length === PB.length };
        if (!res.empty && V.length) {
          var vals = V.map(F), best = mx ? Math.max.apply(null, vals) : Math.min.apply(null, vals);
          var far = PB.filter(function (pt) { return V.indexOf(pt) < 0; }).map(F);
          var tol = 1e-6 * Math.max(1, Math.abs(best));
          res.noOpt = far.some(function (v) { return mx ? v > best + tol : v < best - tol; });
          res.best = best; res.vals = vals;
          res.opt = V.filter(function (pt, i) { return Math.abs(vals[i] - best) <= tol; });
        } else if (!res.empty) res.noOpt = true;
      }
      st.reset(1);
    }
    function pT(pt) { return "(" + nT(pt[0]) + ",\\," + nT(pt[1]) + ")"; }
    function fT() { return pTex([F0, res.p]).replace(/^0$/, "") + (res.q.zero() ? "" : monT(res.q, 1, "y", res.p.zero())); }
    function draw(k) {
      var xs = [0], ys = [0];
      if (res) res.V.forEach(function (pt) { xs.push(pt[0]); ys.push(pt[1]); });
      if (res) res.cons.forEach(function (c) { if (Math.abs(c.a) > 1e-12) xs.push(c.c / c.a); if (Math.abs(c.b) > 1e-12) ys.push(c.c / c.b); });
      var x1 = Math.max.apply(null, xs), y1 = Math.max.apply(null, ys), x0 = Math.min.apply(null, xs), y0 = Math.min.apply(null, ys);
      var ext = res && !res.bounded ? 1.45 : 1.18, m = Math.max(x1 - x0, y1 - y0, 4);
      var V = [x0 - m * 0.1, x0 + m * ext, y0 - m * 0.1, y0 + m * ext];
      var G = gview({ x0: V[0], x1: V[1], y0: V[2], y1: V[3], W: 340, H: 340 }), Cl = clipSvg(svg, G), g = G.g + Cl.open;
      if (res) {
        if (!res.empty) g += halfFill(G, region(res.cons, V));
        res.cons.forEach(function (c) { g += halfLine(G, c, V, c.col); });
        if (k >= 4 && res.best != null && !res.noOpt) g += halfLine(G, { a: res.p.val(), b: res.q.val(), c: res.best, op: "<" }, V, COL.k);
        if (k >= 2) res.V.forEach(function (pt) {
          var isO = k >= 4 && !res.noOpt && res.opt.indexOf(pt) >= 0;
          g += dot(G, pt[0], pt[1], isO ? COL.k : "var(--text)", isO ? 6.5 : 4);
          g += '<text x="' + (G.X(pt[0]) + 6) + '" y="' + (G.Y(pt[1]) - 6) + '" style="fill:var(--text);font-size:10.5px">(' + nS(pt[0]) + ", " + nS(pt[1]) + ")</text>";
        });
      }
      svg.setAttribute("viewBox", "0 0 " + G.W + " " + G.H); svg.innerHTML = g + Cl.close;
    }
    function show(k) {
      if (!res) { info.innerHTML = t3("Revisa la funció objectiu i les restriccions (a i b no poden ser tots dos 0).", "Revisa la función objetivo y las restricciones (a y b no pueden ser ambos 0).", "Check the objective function and the constraints (a and b can't both be 0)."); draw(0); return; }
      var L = function (i) { return u("step") + " " + i; }, rows = [];
      rows.push([L(1), t3("Dibuixem les restriccions: la <strong>regió factible</strong> és la part comuna de tots els semiplans.", "Dibujamos las restricciones: la <strong>región factible</strong> es la parte común de todos los semiplanos.", "Draw the constraints: the <strong>feasible region</strong> is the part shared by all the half-planes.") +
        (res.empty ? "<br>" + t3("No hi ha cap punt que complisca totes les restriccions: el problema no té solució.", "No hay ningún punto que cumpla todas las restricciones: el problema no tiene solución.", "No point satisfies all the constraints: the problem has no solution.") : "<br>" + (res.bounded ? t3("Regió fitada.", "Región acotada.", "Bounded region.") : t3("Regió no fitada.", "Región no acotada.", "Unbounded region.")))]);
      if (k >= 2 && !res.empty) rows.push([L(2), t3("Vèrtexs (talls de les rectes frontera): ", "Vértices (cortes de las rectas frontera): ", "Vertices (where the boundary lines cross): ") + tex(res.V.map(pT).join(",\\ "))]);
      if (k >= 3 && !res.empty) rows.push([L(3), t3("Valor de ", "Valor de ", "Value of ") + tex("F(x,y)=" + fT()) + t3(" en cada vèrtex:", " en cada vértice:", " at each vertex:") + "<br>" +
        res.V.map(function (pt, i) { return tex("F" + pT(pt) + "=" + nT(res.vals[i])); }).join("<br>")]);
      if (k >= 4 && !res.empty) {
        var txt2;
        if (res.noOpt) txt2 = res.mx ? t3("La regió no és fitada i \\(F\\) hi pren valors tan grans com vulguem: <strong>no hi ha màxim</strong>.", "La región no es acotada y \\(F\\) toma valores tan grandes como queramos: <strong>no hay máximo</strong>.", "The region is unbounded and \\(F\\) takes values as large as we like: <strong>there is no maximum</strong>.")
          : t3("La regió no és fitada i \\(F\\) hi pren valors tan menuts com vulguem: <strong>no hi ha mínim</strong>.", "La región no es acotada y \\(F\\) toma valores tan pequeños como queramos: <strong>no hay mínimo</strong>.", "The region is unbounded and \\(F\\) takes values as small as we like: <strong>there is no minimum</strong>.");
        else if (res.opt.length > 1) txt2 = (res.mx ? t3("El màxim", "El máximo", "The maximum") : t3("El mínim", "El mínimo", "The minimum")) + " " + tex("F=" + nT(res.best)) + t3(" s'assoleix en dos vèrtexs: <strong>infinites solucions</strong>, tots els punts del segment que va de ", " se alcanza en dos vértices: <strong>infinitas soluciones</strong>, todos los puntos del segmento que va de ", " is reached at two vertices: <strong>infinitely many solutions</strong>, every point of the segment from ") + tex(pT(res.opt[0])) + t3(" a ", " a ", " to ") + tex(pT(res.opt[1])) + ".";
        else txt2 = (res.mx ? t3("Màxim", "Máximo", "Maximum") : t3("Mínim", "Mínimo", "Minimum")) + ": " + tex("F" + pT(res.opt[0]) + "=" + nT(res.best)) + ". " + t3("La recta de nivell que passa per l'òptim (verda) deixa tota la regió a un costat.", "La recta de nivel que pasa por el óptimo (verde) deja toda la región a un lado.", "The level line through the optimum (green) leaves the whole region on one side.");
        rows.push([t3("Solució", "Solución", "Solution"), txt2.replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); })]);
      }
      info.innerHTML = kv(rows);
      draw(k);
    }
    st = stepper(w, function () { return res ? (res.empty ? 1 : 4) : 0; }, show);
    read();
    onLang(function () { var g = goal.value; goalOpts(); goal.value = g; st.upd(); });
  }

  /* ---------- autoavaluació ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("El sistema $\\begin{cases}x+y=2\\\\ 2x+2y=5\\end{cases}$ és…", "El sistema $\\begin{cases}x+y=2\\\\ 2x+2y=5\\end{cases}$ es…", "The system $\\begin{cases}x+y=2\\\\ 2x+2y=5\\end{cases}$ is…"),
      o: [q3("compatible determinat", "compatible determinado", "consistent with one solution"), q3("compatible indeterminat", "compatible indeterminado", "consistent with infinitely many"), q3("incompatible", "incompatible", "inconsistent")], a: 2, e: q3("Si multipliquem la primera per 2 queda $2x+2y=4$, que contradiu $2x+2y=5$: les rectes són paral·leles.", "Si multiplicamos la primera por 2 queda $2x+2y=4$, que contradice $2x+2y=5$: las rectas son paralelas.", "Multiplying the first by 2 gives $2x+2y=4$, which contradicts $2x+2y=5$: the lines are parallel.") },
    { q: q3("Per a traure denominadors de $\\frac x2+\\frac y3=4$ multipliquem els dos membres per…", "Para quitar denominadores de $\\frac x2+\\frac y3=4$ multiplicamos los dos miembros por…", "To clear the denominators of $\\frac x2+\\frac y3=4$ we multiply both sides by…"),
      o: [q3("$5$"), q3("$6$"), q3("$12$")], a: 1, e: q3("El m.c.m. de 2 i 3 és 6: queda $3x+2y=24$.", "El m.c.m. de 2 y 3 es 6: queda $3x+2y=24$.", "The LCM of 2 and 3 is 6: we get $3x+2y=24$.") },
    { q: q3("En aplicar Gauss, l'última fila queda $\\left(0\\ \\ 0\\ \\ 0\\,|\\,0\\right)$ i les altres dues no s'anul·len. El sistema és…", "Al aplicar Gauss, la última fila queda $\\left(0\\ \\ 0\\ \\ 0\\,|\\,0\\right)$ y las otras dos no se anulan. El sistema es…", "Applying Gauss, the last row becomes $\\left(0\\ \\ 0\\ \\ 0\\,|\\,0\\right)$ and the other two do not vanish. The system is…"),
      o: [q3("SCD"), q3("SCI"), q3("SI")], a: 1, e: q3("L'última equació és $0=0$: sobra, i una incògnita passa a ser un paràmetre.", "La última ecuación es $0=0$: sobra, y una incógnita pasa a ser un parámetro.", "The last equation is $0=0$: it drops out and one unknown becomes a parameter.") },
    { q: q3("Quines són les solucions de $\\begin{cases}x+y=5\\\\ xy=6\\end{cases}$?", "¿Cuáles son las soluciones de $\\begin{cases}x+y=5\\\\ xy=6\\end{cases}$?", "What are the solutions of $\\begin{cases}x+y=5\\\\ xy=6\\end{cases}$?"),
      o: [q3("Només $(2,3)$", "Solo $(2,3)$", "Only $(2,3)$"), q3("$(2,3)$ i $(3,2)$", "$(2,3)$ y $(3,2)$", "$(2,3)$ and $(3,2)$"), q3("No en té", "No tiene", "None")], a: 1, e: q3("$y=5-x\\Rightarrow x(5-x)=6\\Rightarrow x^2-5x+6=0$: $x=2$ o $x=3$.", "$y=5-x\\Rightarrow x(5-x)=6\\Rightarrow x^2-5x+6=0$: $x=2$ o $x=3$.", "$y=5-x\\Rightarrow x(5-x)=6\\Rightarrow x^2-5x+6=0$: $x=2$ or $x=3$.") },
    { q: q3("Si dividim els dos membres de $-3x\\lt12$ entre $-3$, obtenim…", "Si dividimos los dos miembros de $-3x\\lt12$ entre $-3$, obtenemos…", "Dividing both sides of $-3x\\lt12$ by $-3$ gives…"),
      o: [q3("$x\\lt-4$"), q3("$x\\gt-4$"), q3("$x\\gt4$")], a: 1, e: q3("En dividir per un nombre negatiu, la desigualtat canvia de sentit.", "Al dividir por un número negativo, la desigualdad cambia de sentido.", "Dividing by a negative number reverses the inequality.") },
    { q: q3("La solució de $2x+1\\ge7$ és…", "La solución de $2x+1\\ge7$ es…", "The solution of $2x+1\\ge7$ is…"),
      o: [q3("$(3,+\\infty)$"), q3("$[3,+\\infty)$"), q3("$(-\\infty,3]$")], a: 1, e: q3("$2x\\ge6\\Rightarrow x\\ge3$; el 3 s'inclou perquè hi ha $\\ge$.", "$2x\\ge6\\Rightarrow x\\ge3$; el 3 se incluye porque hay $\\ge$.", "$2x\\ge6\\Rightarrow x\\ge3$; 3 is included because of $\\ge$.") },
    { q: q3("La inequació $2(x+1)\\gt2x+5$…", "La inecuación $2(x+1)\\gt2x+5$…", "The inequality $2(x+1)\\gt2x+5$…"),
      o: [q3("té per solució $\\mathbb R$", "tiene por solución $\\mathbb R$", "has solution $\\mathbb R$"), q3("no té solució", "no tiene solución", "has no solution"), q3("té per solució $x\\gt\\frac32$", "tiene por solución $x\\gt\\frac32$", "has solution $x\\gt\\frac32$")], a: 1, e: q3("Queda $2\\gt5$, que és fals per a qualsevol $x$.", "Queda $2\\gt5$, que es falso para cualquier $x$.", "It becomes $2\\gt5$, false for every $x$.") },
    { q: q3("La solució de $x^2-9\\lt0$ és…", "La solución de $x^2-9\\lt0$ es…", "The solution of $x^2-9\\lt0$ is…"),
      o: [q3("$(-3,3)$"), q3("$(-\\infty,-3)\\cup(3,+\\infty)$"), q3("$(-\\infty,3)$")], a: 0, e: q3("La paràbola $y=x^2-9$ és negativa entre les arrels $-3$ i $3$.", "La parábola $y=x^2-9$ es negativa entre las raíces $-3$ y $3$.", "The parabola $y=x^2-9$ is negative between the roots $-3$ and $3$.") },
    { q: q3("La inequació $x^2+4\\gt0$…", "La inecuación $x^2+4\\gt0$…", "The inequality $x^2+4\\gt0$…"),
      o: [q3("no té solució", "no tiene solución", "has no solution"), q3("es compleix per a tot $x\\in\\mathbb R$", "se cumple para todo $x\\in\\mathbb R$", "holds for every $x\\in\\mathbb R$"), q3("té per solució $(-2,2)$", "tiene por solución $(-2,2)$", "has solution $(-2,2)$")], a: 1, e: q3("$x^2+4$ no té arrels reals i sempre és positiu.", "$x^2+4$ no tiene raíces reales y siempre es positivo.", "$x^2+4$ has no real roots and is always positive.") },
    { q: q3("Quina és la solució de $(x-1)^2\\le0$?", "¿Cuál es la solución de $(x-1)^2\\le0$?", "What is the solution of $(x-1)^2\\le0$?"),
      o: [q3("$\\{1\\}$"), q3("$\\varnothing$"), q3("$\\mathbb R$")], a: 0, e: q3("Un quadrat mai no és negatiu; només val 0 si $x=1$.", "Un cuadrado nunca es negativo; solo vale 0 si $x=1$.", "A square is never negative; it is 0 only when $x=1$.") },
    { q: q3("En la taula de signes de $x(x-2)(x+3)$, quin signe té el producte en $(0,2)$?", "En la tabla de signos de $x(x-2)(x+3)$, ¿qué signo tiene el producto en $(0,2)$?", "In the sign table of $x(x-2)(x+3)$, what sign does the product have on $(0,2)$?"),
      o: [q3("$+$"), q3("$-$")], a: 1, e: q3("Per exemple, amb $x=1$: $1\\cdot(-1)\\cdot4=-4\\lt0$.", "Por ejemplo, con $x=1$: $1\\cdot(-1)\\cdot4=-4\\lt0$.", "For example, with $x=1$: $1\\cdot(-1)\\cdot4=-4\\lt0$.") },
    { q: q3("La solució del sistema $x\\gt-1,\\ x\\le4$ és…", "La solución del sistema $x\\gt-1,\\ x\\le4$ es…", "The solution of the system $x\\gt-1,\\ x\\le4$ is…"),
      o: [q3("$[-1,4]$"), q3("$(-1,4]$"), q3("$(-\\infty,4]$")], a: 1, e: q3("És la intersecció de $(-1,+\\infty)$ i $(-\\infty,4]$.", "Es la intersección de $(-1,+\\infty)$ y $(-\\infty,4]$.", "It is the intersection of $(-1,+\\infty)$ and $(-\\infty,4]$.") },
    { q: q3("El punt $(0,0)$ és solució de $3x-2y\\gt6$?", "¿El punto $(0,0)$ es solución de $3x-2y\\gt6$?", "Is $(0,0)$ a solution of $3x-2y\\gt6$?"),
      o: [q3("Sí", "Sí", "Yes"), q3("No: la solució és el semiplà que no conté l'origen", "No: la solución es el semiplano que no contiene el origen", "No: the solution is the half-plane not containing the origin")], a: 1, e: q3("$0\\gt6$ és fals.", "$0\\gt6$ es falso.", "$0\\gt6$ is false.") },
    { q: q3("Com es dibuixa la recta frontera de $x+y\\lt5$?", "¿Cómo se dibuja la recta frontera de $x+y\\lt5$?", "How is the boundary line of $x+y\\lt5$ drawn?"),
      o: [q3("Contínua", "Continua", "Solid"), q3("Discontínua", "Discontinua", "Dashed")], a: 1, e: q3("Amb $\\lt$ o $\\gt$ els punts de la recta no són solució.", "Con $\\lt$ o $\\gt$ los puntos de la recta no son solución.", "With $\\lt$ or $\\gt$ the points on the line are not solutions.") },
    { q: q3("Les restriccions $x\\ge0,\\ y\\ge0$ indiquen que la regió és…", "Las restricciones $x\\ge0,\\ y\\ge0$ indican que la región está…", "The constraints $x\\ge0,\\ y\\ge0$ mean the region lies…"),
      o: [q3("al primer quadrant", "en el primer cuadrante", "in the first quadrant"), q3("al tercer quadrant", "en el tercer cuadrante", "in the third quadrant"), q3("sobre l'eix $x$", "sobre el eje $x$", "on the $x$-axis")], a: 0, e: q3("Les dues coordenades han de ser positives o zero.", "Las dos coordenadas tienen que ser positivas o cero.", "Both coordinates must be positive or zero.") },
    { q: q3("En un problema de programació lineal amb regió fitada, l'òptim s'assoleix…", "En un problema de programación lineal con región acotada, el óptimo se alcanza…", "In a linear programming problem with a bounded region, the optimum is reached…"),
      o: [q3("en el centre de la regió", "en el centro de la región", "at the centre of the region"), q3("en un vèrtex (o en un costat sencer)", "en un vértice (o en un lado entero)", "at a vertex (or along a whole edge)"), q3("sempre en l'origen", "siempre en el origen", "always at the origin")], a: 1, e: q3("És el teorema fonamental: n'hi ha prou amb avaluar $F$ en els vèrtexs.", "Es el teorema fundamental: basta con evaluar $F$ en los vértices.", "This is the fundamental theorem: evaluating $F$ at the vertices is enough.") },
    { q: q3("Els vèrtexs d'una regió són $(0,0)$, $(4,0)$, $(2,3)$ i $(0,4)$. Quin és el màxim de $F=2x+y$?", "Los vértices de una región son $(0,0)$, $(4,0)$, $(2,3)$ y $(0,4)$. ¿Cuál es el máximo de $F=2x+y$?", "A region has vertices $(0,0)$, $(4,0)$, $(2,3)$ and $(0,4)$. What is the maximum of $F=2x+y$?"),
      o: [q3("$7$, en $(2,3)$", "$7$, en $(2,3)$", "$7$, at $(2,3)$"), q3("$8$, en $(4,0)$", "$8$, en $(4,0)$", "$8$, at $(4,0)$"), q3("$4$, en $(0,4)$", "$4$, en $(0,4)$", "$4$, at $(0,4)$")], a: 1, e: q3("$F(0,0)=0,\\ F(4,0)=8,\\ F(2,3)=7,\\ F(0,4)=4$.") },
    { q: q3("Si dos vèrtexs donen el mateix valor màxim de $F$, el problema…", "Si dos vértices dan el mismo valor máximo de $F$, el problema…", "If two vertices give the same maximum value of $F$, the problem…"),
      o: [q3("no té solució", "no tiene solución", "has no solution"), q3("té infinites solucions (el segment que els uneix)", "tiene infinitas soluciones (el segmento que los une)", "has infinitely many solutions (the segment joining them)"), q3("té exactament dues solucions", "tiene exactamente dos soluciones", "has exactly two solutions")], a: 1, e: q3("Tots els punts del costat que uneix els dos vèrtexs donen el mateix valor.", "Todos los puntos del lado que une los dos vértices dan el mismo valor.", "Every point on the edge joining the two vertices gives the same value.") }
  ];
