(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2batx-mii-u3-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top" }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  function t3(va, es, en) { return lang === "es" ? es : lang === "en" ? en : va; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }
  function presetBtns(box, labels, onPick) {
    var bs = [];
    labels().forEach(function (_, i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { bs.forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on"); onPick(i); });
      box.appendChild(b); bs.push(b);
    });
    onLang(function () { var L = labels(); bs.forEach(function (b, i) { b.innerHTML = L[i]; }); });
    return bs;
  }

  /* ---------- fraccions exactes ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function Fr(n, d) { if (d === undefined) d = 1; if (d < 0) { n = -n; d = -d; } var g = gcd(n, d) || 1; return { n: n / g, d: d / g }; }
  function F(x) { return typeof x === "number" ? Fr(x) : x; }
  function fAdd(a, b) { a = F(a); b = F(b); return Fr(a.n * b.d + b.n * a.d, a.d * b.d); }
  function fSub(a, b) { a = F(a); b = F(b); return Fr(a.n * b.d - b.n * a.d, a.d * b.d); }
  function fMul(a, b) { a = F(a); b = F(b); return Fr(a.n * b.n, a.d * b.d); }
  function fDiv(a, b) { a = F(a); b = F(b); return Fr(a.n * b.d, a.d * b.n); }
  function fVal(a) { a = F(a); return a.n / a.d; }
  function fT(f) { f = F(f); return f.d === 1 ? String(f.n) : (f.n < 0 ? "-" : "") + "\\frac{" + Math.abs(f.n) + "}{" + f.d + "}"; }
  function fP(f) { f = F(f); return f.n < 0 ? "(" + fT(f) + ")" : fT(f); } // entre parèntesis si és negatiu
  function cT(p) { return "(" + fT(p[0]) + ",\\," + fT(p[1]) + ")"; }
  function lcm(a, b) { return a / gcd(a, b) * b; }

  /* ---------- nombres decimals, arrels i angles ---------- */
  function decS(x, k) { var s = String(+x.toFixed(k == null ? 2 : k)); if (s === "-0") s = "0"; return lang === "en" ? s : s.replace(".", ","); }
  function dT(x, k) { return decS(x, k).replace(",", "{,}"); }
  // n = a²·b amb b lliure de quadrats
  function surd(n) { var a = 1, b = n, i; for (i = 2; i * i <= b; i++) while (b % (i * i) === 0) { b /= i * i; a *= i; } return { a: a, b: b }; }
  function sqT(n) { if (n === 0) return "0"; var s = surd(n); return s.b === 1 ? String(s.a) : (s.a === 1 ? "" : s.a) + "\\sqrt{" + s.b + "}"; }
  // num / √S, racionalitzat i simplificat
  function divRootT(num, S) {
    var s = surd(S), f = Fr(num, s.a * (s.b === 1 ? 1 : s.b));
    if (s.b === 1) return fT(f);
    var top = (Math.abs(f.n) === 1 ? "" : Math.abs(f.n)) + "\\sqrt{" + s.b + "}";
    return (f.n < 0 ? "-" : "") + (f.d === 1 ? top : "\\frac{" + top + "}{" + f.d + "}");
  }
  function sqApprox(n) { var s = surd(n); return s.b === 1 ? "" : "\\approx " + dT(Math.sqrt(n)); }
  function degT(x) { return dT(x, 2) + "^\\circ"; }
  function dmsT(x) {
    var s = Math.round(x * 3600), d = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), q = s % 60;
    return d + "^\\circ" + (m || q ? m + "'" : "") + (q ? q + "''" : "");
  }
  function deg(r) { return r * 180 / Math.PI; }

  /*@@3D@@*/
  var COL = { u: "#3b82f6", v: "#f97316", w: "#16a34a", r: "#3b82f6", s: "#e11d48", p: "#8b5cf6", k: "#0f9488" };

  /* ---------- vectors amb fraccions exactes ---------- */
  function vsub(a, b) { return [0, 1, 2].map(function (i) { return fSub(a[i], b[i]); }); }
  function vadd(a, b) { return [0, 1, 2].map(function (i) { return fAdd(a[i], b[i]); }); }
  function vmul(a, k) { return a.map(function (x) { return fMul(x, k); }); }
  function vdot(a, b) { return fAdd(fAdd(fMul(a[0], b[0]), fMul(a[1], b[1])), fMul(a[2], b[2])); }
  function vcross(a, b) { return [fSub(fMul(a[1], b[2]), fMul(a[2], b[1])), fSub(fMul(a[2], b[0]), fMul(a[0], b[2])), fSub(fMul(a[0], b[1]), fMul(a[1], b[0]))]; }
  function vzero(a) { return a.every(function (x) { return F(x).n === 0; }); }
  function vnum(a) { return a.map(fVal); }
  function vT(a) { return "(" + a.map(fT).join(",\\,") + ")"; }
  function det3(a, b, c) { return vdot(a, vcross(b, c)); }
  function rt(s) { return surd(s).b === 1 ? sqT(s) : "\\sqrt{" + s + "}"; }
  // terms = [[coeficient, "x"], …] -> 3x-\frac{1}{2}y+4 (sense els termes nuls)
  function poly(terms) {
    var s = "";
    terms.forEach(function (t) {
      var c = F(t[0]); if (c.n === 0) return;
      var neg = c.n < 0, a = Fr(Math.abs(c.n), c.d), body = t[1] && a.n === 1 && a.d === 1 ? t[1] : fT(a) + t[1];
      s += (s ? (neg ? "-" : "+") : (neg ? "-" : "")) + body;
    });
    return s || "0";
  }
  function m2(a) { return fVal(vdot(a, a)); } // |a|² (enter si a és enter)
  // desenvolupament d'un determinant 3×3 d'enters per la primera fila
  function detT(a, b, c) {
    a = vnum(a); b = vnum(b); c = vnum(c);
    var m = [b[1] * c[2] - b[2] * c[1], b[0] * c[2] - b[2] * c[0], b[0] * c[1] - b[1] * c[0]];
    return "\\begin{vmatrix}" + [a, b, c].map(function (r) { return r.join("&"); }).join("\\\\") + "\\end{vmatrix}=" +
      a[0] + "\\cdot" + fP(m[0]) + "-" + fP(a[1]) + "\\cdot" + fP(m[1]) + "+" + fP(a[2]) + "\\cdot" + fP(m[2]) + "=" + (a[0] * m[0] - a[1] * m[1] + a[2] * m[2]);
  }
  function dotT(a, b) { return a.map(function (x, i) { return fP(x) + "\\cdot" + fP(b[i]); }).join("+") + "=" + fT(vdot(a, b)); }
  function modT(a) { var s = m2(a); return "\\sqrt{" + a.map(function (x) { return fP(x) + "^2"; }).join("+") + "}=" + (Math.round(Math.sqrt(s)) ** 2 === s ? sqT(s) : "\\sqrt{" + s + "}" + (surd(s).a > 1 ? "=" + sqT(s) : "") + sqApprox(s)); }
  function prim(v) { // enters primitius (per a vectors directors i normals)
    var L = v.reduce(function (s, x) { return lcm(s, F(x).d); }, 1), w = v.map(function (x) { x = F(x); return x.n * L / x.d; });
    var g = w.reduce(function (s, x) { return gcd(s, x); }, 0) || 1;
    return w.map(function (x) { return x / g; });
  }
  // rang d'una llista de files (fraccions)
  function rank(rows) {
    var M = rows.map(function (r) { return r.map(F); }), rk = 0, nc = M[0].length;
    for (var c = 0; c < nc && rk < M.length; c++) {
      var p = -1; for (var i = rk; i < M.length; i++) if (M[i][c].n !== 0) { p = i; break; }
      if (p < 0) continue;
      var t = M[p]; M[p] = M[rk]; M[rk] = t;
      for (i = 0; i < M.length; i++) if (i !== rk && M[i][c].n !== 0) {
        var f = fDiv(M[i][c], M[rk][c]);
        M[i] = M[i].map(function (x, j) { return fSub(x, fMul(f, M[rk][j])); });
      }
      rk++;
    }
    return rk;
  }
  // pla a·x+b·y+c·z+d=0 amb enters primitius i el primer coeficient no nul positiu
  function planeEq(n, d) {
    var w = prim(n.concat([d])), s = w[0] || w[1] || w[2];
    if (s < 0) w = w.map(function (x) { return -x; });
    return { c: w, t: poly([[w[0], "x"], [w[1], "y"], [w[2], "z"], [w[3], ""]]) + "=0" };
  }
  function evalPlane(c, P) { return fAdd(vdot(c.slice(0, 3), P), c[3]); }
  function termT(v, p) { p = F(p); return p.n === 0 ? v : v + (p.n < 0 ? "+" + fT(Fr(-p.n, p.d)) : "-" + fT(p)); }

  /* ---------- caselles de coordenades (enters de −9 a 9) ---------- */
  // groups: [{ k: "A", vals: [..], fmt: [html abans de la 1a casella, entre caselles…, després de l'última] }]
  function fields(box, groups, onChange) {
    var st = {};
    groups.forEach(function (g) {
      var s = document.createElement("span"); s.className = "ptin"; g.ins = [];
      st[g.k] = g.vals.slice();
      g.fmt.forEach(function (h, i) {
        if (h) { var sp = document.createElement("span"); sp.innerHTML = h; s.appendChild(sp); }
        if (i < g.vals.length) {
          var inp = document.createElement("input"); inp.className = "tin s"; inp.autocomplete = "off"; inp.value = g.vals[i];
          inp.setAttribute("aria-label", g.k + " " + (i + 1));
          (function (j) {
            inp.addEventListener("input", function () {
              var v = inp.value.trim().replace("−", "-"), ok = /^-?\d$/.test(v);
              inp.classList.toggle("bad", !ok);
              if (ok) { st[g.k][j] = +v; onChange(); }
            });
          })(i);
          s.appendChild(inp); g.ins.push(inp);
        }
      });
      box.appendChild(s);
    });
    return {
      v: st,
      set: function (vals) {
        groups.forEach(function (g) { st[g.k] = vals[g.k].slice(); g.ins.forEach(function (inp, j) { inp.value = vals[g.k][j]; inp.classList.remove("bad"); }); });
        onChange();
      }
    };
  }
  function ptF(name) { return [tex(name) + "(", ",", ",", ")"]; }
  function veF(name) { return [tex(name) + "=(", ",", ",", ")"]; }
  function plF(name, rhs) { return [tex(name + ":"), tex("x+"), tex("y+"), tex("z") + (rhs ? tex("=") : tex("+")), rhs ? "" : tex("=0")]; }

  /* ---------- dibuixos ---------- */
  function arrow3(p, v, col, label) { return { seg: [p, [p[0] + v[0], p[1] + v[1], p[2] + v[2]]], stroke: col, w: 2.6, arrow: true, label: label }; }
  function pl(i, n, d) { return { plane: n.concat([d]), fill: PCOL[i][0], stroke: PCOL[i][1] }; }
  function dot3(p, label, col) { return { pt: p, label: label, fill: col }; }
  function drop(p) { return { seg: [p, [p[0], p[1], 0]], stroke: "var(--muted)", w: 1, dash: "3 3" }; } // perpendicular al pla XY
  function Lof(pts, min) { var m = min || 3; pts.forEach(function (p) { p.forEach(function (x) { m = Math.max(m, Math.abs(x)); }); }); return Math.ceil(m); }
  function setupW(id, groups, draw) {
    var w = document.getElementById(id); if (!w) return null;
    var fig = $(w, "fig"), info = w.querySelector(".info"), g = { w: w, info: info };
    g.redraw = s3mount(fig, function () { return g.scene || { items: [] }; });
    g.f = fields($(w, "in"), groups, function () { draw(); });
    return g;
  }
  function bad(g, msg) { g.info.innerHTML = '<p class="msg-bad">' + msg + "</p>"; }
  function scene(g, items, pts, extra) { var o = { items: items, L: Lof(pts), w: 340, h: 300 }; for (var k in extra || {}) o[k] = extra[k]; g.scene = o; g.redraw(); }

  /* ---------- 3.1 vectors ---------- */
  function wVec() {
    var g = setupW("w-vec", [{ k: "A", vals: [2, -1, 3], fmt: ptF("A") }, { k: "B", vals: [5, 1, -3], fmt: ptF("B") }], draw); if (!g) return;
    function draw() {
      var A = g.f.v.A, B = g.f.v.B, v = vsub(B, A).map(fVal), s = m2(v), M = vmul(vadd(A, B), Fr(1, 2));
      scene(g, [drop(A), drop(B), arrow3(A, v, COL.u), dot3(A, "A"), dot3(B, "B", COL.u), dot3(vnum(M), "M", COL.p)], [A, B]);
      var rows = [[t3("Components", "Componentes", "Components"), tex("\\overrightarrow{AB}=(" + B.map(function (b, i) { return b + "-" + fP(A[i]); }).join(",\\,") + ")=" + vT(v))]];
      if (!s) { rows.push(["", t3("És el vector nul: \\(A=B\\).", "Es el vector nulo: \\(A=B\\).", "It is the zero vector: \\(A=B\\).").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); })]); g.info.innerHTML = kv(rows); return; }
      var r = Math.round(Math.sqrt(s)), unit = r * r === s ? vT(v.map(function (x) { return Fr(x, r); })) : "\\left(" + v.map(function (x) { return divRootT(x, s); }).join(",\\,") + "\\right)";
      rows.push([t3("Mòdul", "Módulo", "Magnitude"), tex("|\\overrightarrow{AB}|=" + modT(v))]);
      rows.push([t3("Unitari", "Unitario", "Unit vector"), tex("\\dfrac{\\overrightarrow{AB}}{|\\overrightarrow{AB}|}=" + unit)]);
      rows.push([t3("Oposat", "Opuesto", "Opposite"), tex("\\overrightarrow{BA}=" + vT(v.map(function (x) { return -x; })))]);
      rows.push([t3("Punt mig", "Punto medio", "Midpoint"), cdot(COL.p) + tex("M" + vT(M))]);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 3.2 aplicacions ---------- */
  function wPts() {
    var g = setupW("w-pts", [{ k: "A", vals: [1, 2, -1], fmt: ptF("A") }, { k: "B", vals: [3, 1, 1], fmt: ptF("B") }, { k: "C", vals: [2, -2, 3], fmt: ptF("C") }], draw); if (!g) return;
    function draw() {
      var A = g.f.v.A, B = g.f.v.B, C = g.f.v.C, ab = vsub(B, A), ac = vsub(C, A), al = vzero(vcross(ab, ac));
      var M = vmul(vadd(A, B), Fr(1, 2)), A2 = vsub(vmul(B, 2), A), G = vmul(vadd(vadd(A, B), C), Fr(1, 3)), D = vsub(vadd(A, C), B);
      var rows = [[t3("Vectors", "Vectores", "Vectors"), tex("\\overrightarrow{AB}=" + vT(ab) + ",\\ \\ \\overrightarrow{AC}=" + vT(ac))]], k = null;
      if (!vzero(ab)) { var i = ab.findIndex(function (x) { return F(x).n !== 0; }); k = fDiv(ac[i], ab[i]); if (!vzero(vsub(ac, vmul(ab, k)))) k = null; }
      rows.push([t3("Alineats?", "¿Alineados?", "Collinear?"), al
        ? (k ? tex("\\overrightarrow{AC}=" + fT(k) + "\\,\\overrightarrow{AB}") + " " : "") + "<strong>" + t3("Sí: els vectors són proporcionals.", "Sí: los vectores son proporcionales.", "Yes: the vectors are proportional.") + "</strong>"
        : t3("No: ", "No: ", "No: ") + tex("\\overrightarrow{AB}") + t3(" i ", " y ", " and ") + tex("\\overrightarrow{AC}") + t3(" no són proporcionals.", " no son proporcionales.", " are not proportional.")]);
      rows.push([cdot(COL.p) + t3("Punt mig de ", "Punto medio de ", "Midpoint of ") + tex("AB"), tex("M=\\dfrac{A+B}{2}=" + vT(M))]);
      rows.push([cdot(COL.k) + t3("Simètric de ", "Simétrico de ", "Reflection of ") + tex("A") + t3(" resp. ", " resp. ", " in ") + tex("B"), tex("A'=2B-A=" + vT(A2))]);
      var items = [drop(A), drop(B), drop(C)], pts = [A, B, C];
      if (!al) {
        rows.push([cdot(COL.s) + t3("Baricentre", "Baricentro", "Centroid"), tex("G=\\dfrac{A+B+C}{3}=" + vT(G))]);
        rows.push([cdot(COL.w) + t3("Paral·lelogram", "Paralelogramo", "Parallelogram") + " " + tex("ABCD"), tex("D=A+C-B=" + vT(D))]);
        items.push({ poly: [A, B, C], fill: COL.u, stroke: COL.u, op: 0.18 }, { poly: [A, B, C, vnum(D)], fill: "none", stroke: COL.w, op: 0, w: 1.4 }, dot3(vnum(G), "G", COL.s), dot3(vnum(D), "D", COL.w));
        pts.push(vnum(D));
      } else items.push({ seg: [A, C], stroke: COL.u, w: 2 }, { seg: [A, B], stroke: COL.u, w: 2 });
      items.push(dot3(A, "A"), dot3(B, "B"), dot3(C, "C"), dot3(vnum(M), "M", COL.p), dot3(vnum(A2), "A′", COL.k));
      pts.push(vnum(A2));
      scene(g, items, pts);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 3.3 dependència lineal ---------- */
  function combo(a, b, c) { // c = x·a + y·b (a, b independents)
    var n = vcross(a, b), nn = vdot(n, n);
    return [fDiv(vdot(vcross(c, b), n), nn), fDiv(vdot(vcross(a, c), n), nn)];
  }
  function combT(x, y, a, b) { return poly([[x, a], [y, b]]); }
  function wDep() {
    var N = ["\\vec u", "\\vec v", "\\vec w"];
    var g = setupW("w-dep", [{ k: "u", vals: [1, 2, -1], fmt: veF(N[0]) }, { k: "v", vals: [0, 1, 3], fmt: veF(N[1]) }, { k: "w", vals: [2, 5, 1], fmt: veF(N[2]) }], draw); if (!g) return;
    var P = [{ u: [1, 0, 1], v: [2, 1, 0], w: [0, 1, 3] }, { u: [1, 2, -1], v: [0, 1, 3], w: [2, 5, 1] }, { u: [1, 2, -1], v: [2, 4, -2], w: [-1, -2, 1] }];
    presetBtns($(g.w, "presets"), function () { return [t3("Una base", "Una base", "A basis"), t3("Coplanaris", "Coplanarios", "Coplanar"), t3("Paral·lels", "Paralelos", "Parallel")]; }, function (i) { g.f.set(P[i]); });
    function draw() {
      var V = [g.f.v.u, g.f.v.v, g.f.v.w], d = det3(V[0], V[1], V[2]), rk = rank(V);
      var rows = [[t3("Determinant", "Determinante", "Determinant"), tex(detT(V[0], V[1], V[2]))], [t3("Rang", "Rango", "Rank"), tex("\\mathrm{rg}(\\vec u,\\vec v,\\vec w)=" + rk)]];
      var items = [arrow3([0, 0, 0], V[0], COL.u, "u"), arrow3([0, 0, 0], V[1], COL.v, "v"), arrow3([0, 0, 0], V[2], COL.w, "w")];
      if (rk === 3) rows.push(["", "<strong>" + t3("Són linealment independents: formen una base.", "Son linealmente independientes: forman una base.", "They are linearly independent: they form a basis.") + "</strong>"]);
      else if (rk === 2) {
        var pr = [[0, 1, 2], [0, 2, 1], [1, 2, 0]].find(function (q) { return !vzero(vcross(V[q[0]], V[q[1]])); }), c = combo(V[pr[0]], V[pr[1]], V[pr[2]]);
        rows.push(["", "<strong>" + t3("Són coplanaris (linealment dependents): no formen base.", "Son coplanarios (linealmente dependientes): no forman base.", "They are coplanar (linearly dependent): not a basis.") + "</strong>"]);
        rows.push([t3("Combinació", "Combinación", "Combination"), tex(N[pr[2]] + "=" + combT(c[0], c[1], N[pr[0]], N[pr[1]]))]);
        items.unshift({ plane: vnum(vcross(V[pr[0]], V[pr[1]])).concat([0]), fill: PCOL[2][0], stroke: PCOL[2][1], op: 0.3 });
      } else rows.push(["", "<strong>" + (rk ? t3("Els tres vectors són paral·lels (rang 1).", "Los tres vectores son paralelos (rango 1).", "All three vectors are parallel (rank 1).") : t3("Tots són nuls.", "Todos son nulos.", "They are all zero.")) + "</strong>"]);
      scene(g, items, V.concat([[0, 0, 0]]));
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 3.4 producte escalar ---------- */
  function wDot() {
    var g = setupW("w-dot", [{ k: "u", vals: [2, -1, 3], fmt: veF("\\vec u") }, { k: "v", vals: [1, 4, -2], fmt: veF("\\vec v") }], draw); if (!g) return;
    function draw() {
      var U = g.f.v.u, V = g.f.v.v, d = fVal(vdot(U, V)), su = m2(U), sv = m2(V), O = [0, 0, 0];
      var items = [arrow3(O, U, COL.u, "u"), arrow3(O, V, COL.v, "v")], rows = [[tex("\\vec u\\cdot\\vec v"), tex(dotT(U, V))]];
      if (!su || !sv) { scene(g, items, [U, V]); rows.push(["", t3("Algun vector és nul: no hi ha angle.", "Algún vector es nulo: no hay ángulo.", "One of the vectors is zero: no angle.")]); g.info.innerHTML = kv(rows); return; }
      var pj = vmul(V, Fr(d, sv)), a = deg(Math.acos(Math.max(-1, Math.min(1, d / Math.sqrt(su * sv)))));
      items.push({ seg: [U, vnum(pj)], stroke: "var(--muted)", w: 1.2, dash: "4 4" }, arrow3(O, vnum(pj), COL.w));
      rows.push([t3("Mòduls", "Módulos", "Magnitudes"), tex("|\\vec u|=" + rt(su) + ",\\ \\ |\\vec v|=" + rt(sv))]);
      rows.push([t3("Angle", "Ángulo", "Angle"), tex("\\cos\\alpha=\\dfrac{" + d + "}{" + rt(su) + "\\cdot " + rt(sv) + "}=" + divRootT(d, su * sv) + (surd(su * sv).b === 1 ? "" : "\\approx " + dT(d / Math.sqrt(su * sv), 4))) + "<br>" +
        tex("\\alpha" + (Math.abs(a - Math.round(a)) < 1e-9 ? "=" : "\\approx ") + dmsT(a)) + " · " + (d > 0 ? t3("agut", "agudo", "acute") : d < 0 ? t3("obtús", "obtuso", "obtuse") : "<strong>" + t3("recte: són perpendiculars", "recto: son perpendiculares", "right angle: perpendicular") + "</strong>")]);
      rows.push([cdot(COL.w) + t3("Projecció", "Proyección", "Projection"), tex("\\dfrac{\\vec u\\cdot\\vec v}{|\\vec v|}=" + divRootT(d, sv)) + "<br>" + tex("\\dfrac{\\vec u\\cdot\\vec v}{|\\vec v|^2}\\,\\vec v=" + fT(Fr(d, sv)) + "\\,\\vec v=" + vT(pj))]);
      scene(g, items, [U, V, vnum(pj)]);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 3.5 producte vectorial ---------- */
  function wCross() {
    var g = setupW("w-cross", [{ k: "u", vals: [1, 2, -1], fmt: veF("\\vec u") }, { k: "v", vals: [3, 0, 2], fmt: veF("\\vec v") }], draw); if (!g) return;
    function m22(a, b, c, d) { return "\\begin{vmatrix}" + a + "&" + b + "\\\\" + c + "&" + d + "\\end{vmatrix}"; }
    function draw() {
      var U = g.f.v.u, V = g.f.v.v, n = vnum(vcross(U, V)), O = [0, 0, 0], s = m2(n);
      var rows = [[tex("\\vec u\\times\\vec v"), tex("\\begin{vmatrix}\\vec i&\\vec j&\\vec k\\\\" + U.join("&") + "\\\\" + V.join("&") + "\\end{vmatrix}")], ["",
        tex("=\\left(" + m22(U[1], U[2], V[1], V[2]) + ",\\,-" + m22(U[0], U[2], V[0], V[2]) + ",\\," + m22(U[0], U[1], V[0], V[1]) + "\\right)=" + vT(n))]];
      var items = [{ poly: [O, U, vnum(vadd(U, V)), V], fill: COL.p, stroke: COL.p, op: 0.18 }, arrow3(O, U, COL.u, "u"), arrow3(O, V, COL.v, "v")];
      if (!s) {
        rows.push(["", "<strong>" + t3("És el vector nul: ", "Es el vector nulo: ", "It is the zero vector: ") + tex("\\vec u\\parallel\\vec v") + t3(" (o algun és nul) i l'àrea és 0.", " (o alguno es nulo) y el área es 0.", " (or one is zero) and the area is 0.") + "</strong>"]);
        scene(g, items, [U, V]); g.info.innerHTML = kv(rows); return;
      }
      rows.push([t3("Comprovació", "Comprobación", "Check"), tex("(\\vec u\\times\\vec v)\\cdot\\vec u=" + fT(vdot(n, U)) + ",\\ \\ (\\vec u\\times\\vec v)\\cdot\\vec v=" + fT(vdot(n, V)))]);
      rows.push([cdot(COL.p) + t3("Àrea paral·lelogram", "Área paralelogramo", "Parallelogram area"), tex("|\\vec u\\times\\vec v|=" + modT(n))]);
      rows.push([t3("Àrea triangle", "Área triángulo", "Triangle area"), tex("\\dfrac{|\\vec u\\times\\vec v|}{2}=" + (Math.round(Math.sqrt(s)) ** 2 === s ? fT(Fr(Math.round(Math.sqrt(s)), 2)) : "\\dfrac{" + sqT(s) + "}{2}\\approx " + dT(Math.sqrt(s) / 2)))]);
      // si u×v és molt llarg, el dibuixem a escala perquè no s'encongisca la resta del dibuix
      var big = Math.max(Math.sqrt(m2(U)), Math.sqrt(m2(V)), 2) * 1.3, k = Math.min(1, big / Math.sqrt(s)), nd = n.map(function (x) { return x * k; });
      items.push(arrow3(O, nd, COL.w, "u×v"));
      scene(g, items, [U, V, vnum(vadd(U, V)), nd]);
      g.info.innerHTML = kv(rows) + (k < 1 ? '<p class="note" style="margin-top:6px">' + t3("El vector verd està dibuixat més curt (no a escala).", "El vector verde está dibujado más corto (no a escala).", "The green vector is drawn shorter (not to scale).") + "</p>" : "");
    }
    onLang(draw);
  }

  /* ---------- 3.6 producte mixt ---------- */
  function wMix() {
    var shape = 0;
    var g = setupW("w-mix", [{ k: "u", vals: [1, 0, 2], fmt: veF("\\vec u") }, { k: "v", vals: [2, 1, 0], fmt: veF("\\vec v") }, { k: "w", vals: [0, 3, 1], fmt: veF("\\vec w") }], draw); if (!g) return;
    presetBtns($(g.w, "shape"), function () { return [t3("Paral·lelepípede", "Paralelepípedo", "Parallelepiped"), t3("Tetraedre", "Tetraedro", "Tetrahedron")]; }, function (i) { shape = i; draw(); })[0].classList.add("on");
    function draw() {
      var U = g.f.v.u, V = g.f.v.v, W = g.f.v.w, d = fVal(det3(U, V, W)), O = [0, 0, 0], items = [];
      var rows = [[tex("[\\vec u,\\vec v,\\vec w]"), tex(detT(U, V, W))]];
      if (shape === 0) {
        var uv = vnum(vadd(U, V)), uw = vnum(vadd(U, W)), vw = vnum(vadd(V, W)), uvw = vnum(vadd(vadd(U, V), W));
        [[O, U, uv, V], [W, uw, uvw, vw], [O, U, uw, W], [V, uv, uvw, vw], [O, V, vw, W], [U, uv, uvw, uw]].forEach(function (f) { items.push({ poly: f, fill: COL.p, stroke: COL.p, op: 0.1 }); });
      } else[[O, U, V], [O, U, W], [O, V, W], [U, V, W]].forEach(function (f) { items.push({ poly: f, fill: COL.k, stroke: COL.k, op: 0.14 }); });
      items.push(arrow3(O, U, COL.u, "u"), arrow3(O, V, COL.v, "v"), arrow3(O, W, COL.w, "w"));
      if (!d) rows.push(["", "<strong>" + t3("El producte mixt és 0: els vectors són coplanaris i el volum és 0.", "El producto mixto es 0: los vectores son coplanarios y el volumen es 0.", "The triple product is 0: the vectors are coplanar and the volume is 0.") + "</strong>"]);
      else {
        rows.push([cdot(COL.p) + t3("Paral·lelepípede", "Paralelepípedo", "Parallelepiped"), tex("V=|" + d + "|=" + Math.abs(d) + "\\ u^3")]);
        rows.push([cdot(COL.k) + t3("Tetraedre", "Tetraedro", "Tetrahedron"), tex("V=\\dfrac{|" + d + "|}{6}=" + fT(Fr(Math.abs(d), 6)) + "\\ u^3")]);
      }
      scene(g, items, [U, V, W, vnum(vadd(vadd(U, V), W))]);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 3.7 equacions de la recta ---------- */
  function lineEqs(P, d) {
    var par = ["x", "y", "z"].map(function (c, i) { return c + "=" + poly([[P[i], ""], [d[i], "\\lambda"]]); });
    var cont = ["x", "y", "z"].map(function (c, i) { return "\\dfrac{" + termT(c, P[i]) + "}{" + fT(d[i]) + "}"; }).join("=");
    // implícites: dues de les tres igualtats creuades amb normals no paral·leles
    var E = [[0, 1], [1, 2], [0, 2]].map(function (q) { var n = [0, 0, 0]; n[q[0]] = d[q[1]]; n[q[1]] = fMul(-1, d[q[0]]); return n; });
    var pick = [[0, 1], [0, 2], [1, 2]].find(function (q) { return !vzero(vcross(E[q[0]], E[q[1]])); });
    var imp = pick.map(function (i) { return planeEq(E[i], fMul(-1, vdot(E[i], P))).t; });
    return { vec: "(x,y,z)=" + vT(P) + "+\\lambda" + vT(d), par: "\\begin{cases}" + par.join("\\\\") + "\\end{cases}", cont: cont, imp: "\\begin{cases}" + imp.join("\\\\") + "\\end{cases}" };
  }
  function eqList(list) { return '<div class="eqs">' + list.map(function (x) { return "<div><b>" + x[0] + "</b>" + tex(x[1]) + "</div>"; }).join("") + "</div>"; }
  function wLine() {
    var g = setupW("w-line", [{ k: "P", vals: [1, -2, 3], fmt: ptF("P") }, { k: "d", vals: [2, 1, -1], fmt: veF("\\vec d") }], draw); if (!g) return;
    function draw() {
      var P = g.f.v.P, d = g.f.v.d;
      if (vzero(d)) { bad(g, t3("El vector director no pot ser nul.", "El vector director no puede ser nulo.", "The direction vector cannot be zero.")); scene(g, [dot3(P, "P")], [P]); return; }
      var e = lineEqs(P, d);
      scene(g, [{ line: [P, d], stroke: COL.r, w: 2.4, label: "r" }, drop(P), arrow3(P, d, COL.v, "d"), dot3(P, "P")], [P, vnum(vadd(P, d))]);
      g.info.innerHTML = eqList([[t3("Vectorial", "Vectorial", "Vector"), e.vec], [t3("Paramètriques", "Paramétricas", "Parametric"), e.par], [t3("Contínua", "Continua", "Symmetric"), e.cont], [t3("Implícites", "Implícitas", "Implicit"), e.imp]]) +
        '<p class="note" style="margin-top:6px">' + t3("Un altre punt de la recta (amb λ = 1): ", "Otro punto de la recta (con λ = 1): ", "Another point on the line (λ = 1): ") + tex(vT(vadd(P, d))) + "</p>";
    }
    onLang(draw);
  }

  /* ---------- 3.8 equacions del pla ---------- */
  function wPlane() {
    var g = setupW("w-plane", [{ k: "A", vals: [1, 0, 0], fmt: ptF("A") }, { k: "B", vals: [0, 2, 0], fmt: ptF("B") }, { k: "C", vals: [0, 0, 3], fmt: ptF("C") }], draw); if (!g) return;
    function draw() {
      var A = g.f.v.A, B = g.f.v.B, C = g.f.v.C, u = vsub(B, A), v = vsub(C, A), n = vcross(u, v), items = [drop(A), drop(B), drop(C)];
      if (vzero(n)) {
        bad(g, t3("Els tres punts estan alineats (o repetits): no determinen un pla.", "Los tres puntos están alineados (o repetidos): no determinan un plano.", "The three points are collinear (or repeated): they don't determine a plane."));
        scene(g, items.concat([dot3(A, "A"), dot3(B, "B"), dot3(C, "C")]), [A, B, C]); return;
      }
      var p = planeEq(n, fMul(-1, vdot(n, A))), c = p.c;
      var par = ["x", "y", "z"].map(function (k, i) { return k + "=" + poly([[A[i], ""], [u[i], "\\lambda"], [v[i], "\\mu"]]); });
      var list = [[t3("Vectors directors", "Vectores directores", "Direction vectors"), "\\overrightarrow{AB}=" + vT(u) + ",\\ \\ \\overrightarrow{AC}=" + vT(v)],
        [t3("Vector normal", "Vector normal", "Normal vector"), "\\vec n=\\overrightarrow{AB}\\times\\overrightarrow{AC}=" + vT(n) + (prim(n).join() !== vnum(n).join() ? "\\parallel" + vT(prim(n)) : "")],
        [t3("Vectorial", "Vectorial", "Vector"), "(x,y,z)=" + vT(A) + "+\\lambda" + vT(u) + "+\\mu" + vT(v)],
        [t3("Paramètriques", "Paramétricas", "Parametric"), "\\begin{cases}" + par.join("\\\\") + "\\end{cases}"],
        [t3("General", "General", "General"), p.t]];
      if (c.every(function (x) { return x !== 0; })) list.push([t3("Segmentària", "Segmentaria", "Intercept form"), ["x", "y", "z"].map(function (k, i) { var q = Fr(-c[3], c[i]); return q.n === 1 && q.d === 1 ? k : q.d === 1 && q.n > 0 ? "\\dfrac{" + k + "}{" + q.n + "}" : "\\dfrac{" + k + "}{" + fT(q) + "}"; }).join("+") + "=1"]);
      var nd = vnum(prim(n)), k = 1.6 / Math.sqrt(m2(nd));
      items.unshift({ plane: c.slice(0, 3).concat([c[3]]), fill: PCOL[2][0], stroke: PCOL[2][1], op: 0.4 });
      items.push(arrow3(A, vnum(u), COL.u), arrow3(A, vnum(v), COL.v), arrow3(A, nd.map(function (x) { return x * k; }), COL.w, "n"), dot3(A, "A"), dot3(B, "B"), dot3(C, "C"));
      scene(g, items, [A, B, C]);
      g.info.innerHTML = eqList(list);
    }
    onLang(draw);
  }

  /* ---------- 3.9 dues rectes ---------- */
  function wRR() {
    var g = setupW("w-rr", [{ k: "P", vals: [1, 0, -1], fmt: ptF("P") }, { k: "dr", vals: [1, 2, 1], fmt: veF("\\vec d_r") }, { k: "Q", vals: [1, 3, -2], fmt: ptF("Q") }, { k: "ds", vals: [1, -1, 2], fmt: veF("\\vec d_s") }], draw); if (!g) return;
    var PR = [{ P: [1, 0, -2], dr: [2, -1, 3], Q: [3, -1, 1], ds: [4, -2, 6] }, { P: [1, 0, 0], dr: [1, 1, 1], Q: [0, 2, 1], ds: [2, 2, 2] },
      { P: [1, 0, -1], dr: [1, 2, 1], Q: [1, 3, -2], ds: [1, -1, 2] }, { P: [1, 0, 2], dr: [1, -1, 2], Q: [2, 1, 0], ds: [2, 1, -1] }];
    presetBtns($(g.w, "presets"), function () { return [t3("Coincidents", "Coincidentes", "Coincident"), t3("Paral·leles", "Paralelas", "Parallel"), t3("Secants", "Secantes", "Intersecting"), t3("S'encreuen", "Se cruzan", "Skew")]; }, function (i) { g.f.set(PR[i]); });
    function draw() {
      var P = g.f.v.P, Q = g.f.v.Q, dr = g.f.v.dr, ds = g.f.v.ds, pq = vsub(Q, P);
      var items = [dot3(P, "P", COL.r), dot3(Q, "Q", COL.s)];
      if (vzero(dr) || vzero(ds)) { bad(g, t3("Els vectors directors no poden ser nuls.", "Los vectores directores no pueden ser nulos.", "Direction vectors cannot be zero.")); scene(g, items, [P, Q]); return; }
      items.unshift({ line: [P, dr], stroke: COL.r, w: 2.4, label: "r" }, { line: [Q, ds], stroke: COL.s, w: 2.4, label: "s" });
      var r1 = rank([dr, ds]), r2 = rank([dr, ds, pq]), pos = r1 === 1 ? (r2 === 1 ? 0 : 1) : (r2 === 2 ? 2 : 3);
      var rows = [[tex("\\overrightarrow{PQ}"), tex(vT(pq))], [t3("Rangs", "Rangos", "Ranks"), tex("\\mathrm{rg}(\\vec d_r,\\vec d_s)=" + r1 + ",\\ \\ \\mathrm{rg}(\\vec d_r,\\vec d_s,\\overrightarrow{PQ})=" + r2)]];
      if (r1 === 2) rows.push([t3("Determinant", "Determinante", "Determinant"), tex(detT(dr, ds, pq))]);
      rows.push([t3("Posició", "Posición", "Position"), "<strong>" + [t3("Coincidents", "Coincidentes", "Coincident"), t3("Paral·leles", "Paralelas", "Parallel"), t3("Secants", "Secantes", "Intersecting"), t3("S'encreuen", "Se cruzan", "Skew")][pos] + "</strong>"]);
      var pts = [P, Q];
      if (pos === 2) {
        var n = vcross(dr, ds), nn = vdot(n, n), la = fDiv(vdot(vcross(pq, ds), n), nn), mu = fDiv(vdot(vcross(pq, dr), n), nn), X = vadd(P, vmul(dr, la));
        rows.push([cdot(COL.p) + t3("Punt de tall", "Punto de corte", "Common point"), tex("\\lambda=" + fT(la) + ",\\ \\mu=" + fT(mu) + "\\ \\Rightarrow\\ " + vT(X))]);
        items.push(dot3(vnum(X), "X", COL.p)); pts.push(vnum(X));
      }
      scene(g, items, pts);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 3.9 recta i pla ---------- */
  function wRP() {
    var g = setupW("w-rp", [{ k: "P", vals: [1, 0, 2], fmt: ptF("P") }, { k: "d", vals: [2, 1, -1], fmt: veF("\\vec d") }, { k: "pi", vals: [1, 1, 1, -6], fmt: plF("\\pi") }], draw); if (!g) return;
    var PR = [{ P: [1, 0, 2], d: [2, 1, -1], pi: [1, 1, 1, -6] }, { P: [0, 1, 0], d: [1, 1, 2], pi: [2, -4, 1, -1] }, { P: [1, 1, 0], d: [1, -1, 0], pi: [1, 1, 1, -2] }];
    presetBtns($(g.w, "presets"), function () { return [t3("Secants", "Secantes", "Intersecting"), t3("Paral·lels", "Paralelos", "Parallel"), t3("Continguda", "Contenida", "Contained")]; }, function (i) { g.f.set(PR[i]); });
    function draw() {
      var P = g.f.v.P, d = g.f.v.d, c = g.f.v.pi, n = c.slice(0, 3), items = [dot3(P, "P", COL.r)];
      if (vzero(n)) { bad(g, t3("Si A = B = C = 0, no és un pla.", "Si A = B = C = 0, no es un plano.", "If A = B = C = 0 it is not a plane.")); scene(g, items, [P]); return; }
      if (vzero(d)) { bad(g, t3("El vector director no pot ser nul.", "El vector director no puede ser nulo.", "The direction vector cannot be zero.")); scene(g, items, [P]); return; }
      items.unshift(pl(2, n, c[3]), { line: [P, d], stroke: COL.r, w: 2.4, label: "r" });
      var nd = fVal(vdot(n, d)), vP = fVal(evalPlane(c, P)), pos = nd ? 0 : vP ? 1 : 2;
      var rows = [[tex("\\vec n\\cdot\\vec d"), tex(vT(n) + "\\cdot" + vT(d) + "=" + nd)]];
      if (!nd) rows.push([tex("P\\in\\pi\\,?"), tex(n.map(function (x, i) { return fP(x) + "\\cdot" + fP(P[i]); }).join("+") + "+" + fP(c[3]) + "=" + vP + (vP ? "\\neq0" : ""))]);
      rows.push([t3("Posició", "Posición", "Position"), "<strong>" + [t3("Secants", "Secantes", "Intersecting"), t3("Paral·lels", "Paralelos", "Parallel"), t3("La recta és continguda en el pla", "La recta está contenida en el plano", "The line lies in the plane")][pos] + "</strong>"]);
      var pts = [P];
      if (pos === 0) {
        var la = Fr(-vP, nd), X = vadd(P, vmul(d, la));
        rows.push([t3("Substituïm", "Sustituimos", "Substitute"), tex(poly([[vP, ""], [nd, "\\lambda"]]) + "=0\\Rightarrow\\lambda=" + fT(la))]);
        rows.push([cdot(COL.p) + t3("Punt de tall", "Punto de corte", "Intersection"), tex(vT(X))]);
        items.push(dot3(vnum(X), "X", COL.p)); pts.push(vnum(X));
      }
      scene(g, items, pts);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 3.10 / laboratori: tres plans ---------- */
  function propRows(a, b) { return rank([a, b]) < 2; }
  function solve3(E) { // E: files [A,B,C,D] de Ax+By+Cz=D, amb rg M = rg M* = 3
    var M = E.map(function (r) { return r.slice(0, 3); }), D = det3(M[0], M[1], M[2]);
    return [0, 1, 2].map(function (j) { var K = M.map(function (r, i) { var q = r.slice(); q[j] = E[i][3]; return q; }); return fDiv(det3(K[0], K[1], K[2]), D); });
  }
  function lineOf(E) { // recta comuna (rg 2): punt i director a partir de dues files independents
    var pr = [[0, 1], [0, 2], [1, 2]].find(function (q) { return !vzero(vcross(E[q[0]].slice(0, 3), E[q[1]].slice(0, 3))); });
    var a = E[pr[0]], b = E[pr[1]], d = vcross(a.slice(0, 3), b.slice(0, 3)), j = [0, 1, 2].find(function (k) { return F(d[k]).n !== 0; });
    var o = [0, 1, 2].filter(function (k) { return k !== j; }), det = fSub(fMul(a[o[0]], b[o[1]]), fMul(a[o[1]], b[o[0]])), X = [0, 0, 0];
    X[o[0]] = fDiv(fSub(fMul(a[3], b[o[1]]), fMul(a[o[1]], b[3])), det); X[o[1]] = fDiv(fSub(fMul(a[o[0]], b[3]), fMul(a[3], b[o[0]])), det); X[j] = Fr(0);
    d = prim(d); if ((d[0] || d[1] || d[2]) < 0) d = d.map(function (x) { return -x; });
    return { P: X, d: d };
  }
  function classify3(E) {
    var M = E.map(function (r) { return r.slice(0, 3); }), rM = rank(M), rA = rank(E), pM = false, pA = false;
    [[0, 1], [0, 2], [1, 2]].forEach(function (q) { if (propRows(M[q[0]], M[q[1]])) pM = true; if (propRows(E[q[0]], E[q[1]])) pA = true; });
    var k = rM === 3 ? 0 : rM === 2 ? (rA === 3 ? (pM ? 2 : 1) : (pA ? 4 : 3)) : rA === 2 ? (pA ? 6 : 5) : 7;
    return { rM: rM, rA: rA, k: k };
  }
  var P3 = function () { return [t3("Secants en un punt", "Secantes en un punto", "Meeting at one point"), t3("Secants dos a dos (prisma)", "Secantes dos a dos (prisma)", "Intersecting in pairs (prism)"), t3("Dos paral·lels tallats pel tercer", "Dos paralelos cortados por el tercero", "Two parallel planes cut by the third"),
    t3("Secants en una recta", "Secantes en una recta", "Meeting in a line"), t3("Dos coincidents i el tercer secant", "Dos coincidentes y el tercero secante", "Two coincident, the third cutting them"), t3("Tres plans paral·lels", "Tres planos paralelos", "Three parallel planes"),
    t3("Dos coincidents i el tercer paral·lel", "Dos coincidentes y el tercero paralelo", "Two coincident, the third parallel"), t3("Tres plans coincidents", "Tres planos coincidentes", "Three coincident planes")]; };
  function wLab() {
    var g = setupW("w-lab", [{ k: "p1", vals: [1, 1, 1, 1], fmt: plF("\\pi_1", true) }, { k: "p2", vals: [1, -1, 2, 0], fmt: plF("\\pi_2", true) }, { k: "p3", vals: [2, 0, 3, 5], fmt: plF("\\pi_3", true) }], draw); if (!g) return;
    var PR = [[[1, 1, 1, 1], [1, -1, 0, 0], [0, 1, -1, 0]], [[1, 1, 1, 1], [1, -1, 2, 0], [2, 0, 3, 5]], [[1, 2, -1, 1], [2, 4, -2, 5], [1, -1, 1, 0]], [[1, 1, 1, 1], [1, -1, 2, 0], [2, 0, 3, 1]],
      [[1, 1, 1, 1], [2, 2, 2, 2], [1, -1, 0, 0]], [[1, 1, 1, -2], [1, 1, 1, 0], [1, 1, 1, 2]], [[1, 1, 1, 0], [2, 2, 2, 0], [1, 1, 1, 3]], [[1, -1, 2, 1], [2, -2, 4, 2], [-1, 1, -2, -1]]];
    presetBtns($(g.w, "presets"), function () { return P3().map(function (s, i) { return (i + 1) + ". " + s; }); }, function (i) { g.f.set({ p1: PR[i][0], p2: PR[i][1], p3: PR[i][2] }); });
    function draw() {
      var E = [g.f.v.p1, g.f.v.p2, g.f.v.p3], out = $(g.w, "out");
      if (E.some(function (r) { return vzero(r.slice(0, 3)); })) { out.innerHTML = '<p class="msg-bad">' + t3("Algun pla té A = B = C = 0: no és un pla.", "Algún plano tiene A = B = C = 0: no es un plano.", "Some plane has A = B = C = 0: it is not a plane.") + "</p>"; g.scene = { items: [], w: 340, h: 300 }; g.redraw(); return; }
      var c = classify3(E), M = E.map(function (r) { return r.slice(0, 3); }), items = E.map(function (r, i) { return pl(i, r.slice(0, 3), -r[3]); }), pts = [];
      var rows = [[tex("M^*"), tex("\\left(\\begin{array}{ccc|c}" + E.map(function (r) { return r.join("&"); }).join("\\\\") + "\\end{array}\\right)")],
        [t3("Determinant", "Determinante", "Determinant"), tex("|M|=" + fT(det3(M[0], M[1], M[2])))], [t3("Rangs", "Rangos", "Ranks"), tex("\\mathrm{rg}\\,M=" + c.rM + ",\\ \\ \\mathrm{rg}\\,M^*=" + c.rA)],
        [t3("Posició", "Posición", "Position"), "<strong>" + P3()[c.k] + "</strong>"]];
      if (c.k === 0) { var X = solve3(E); rows.push([cdot(COL.p) + t3("Punt comú", "Punto común", "Common point"), tex(vT(X))]); items.push(dot3(vnum(X), "X", COL.p)); pts.push(vnum(X)); }
      if (c.k === 3 || c.k === 4) { var Ln = lineOf(E); rows.push([cdot(COL.p) + t3("Recta comuna", "Recta común", "Common line"), tex("(x,y,z)=" + vT(Ln.P) + "+\\lambda" + vT(Ln.d))]); items.push({ line: [vnum(Ln.P), Ln.d], stroke: COL.p, w: 3.2 }); }
      if (c.k === 7) rows.push(["", t3("Tots els punts del pla són comuns (SCI amb 2 paràmetres).", "Todos los puntos del plano son comunes (SCI con 2 parámetros).", "Every point of the plane is common (2 free parameters).")]);
      if ([1, 2, 5, 6].indexOf(c.k) >= 0) rows.push(["", t3("No hi ha cap punt comú als tres plans (sistema incompatible).", "No hay ningún punto común a los tres planos (sistema incompatible).", "No point is common to all three planes (no solution).")]);
      g.scene = { items: items, L: Lof(pts, 3), w: 340, h: 300 }; g.redraw();
      out.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 3.11 feix de plans ---------- */
  function wFeix() {
    var g = setupW("w-feix", [{ k: "p1", vals: [1, 1, -1, -2], fmt: plF("\\pi_1") }, { k: "p2", vals: [2, -1, 1, -1], fmt: plF("\\pi_2") }, { k: "P", vals: [1, 2, 3], fmt: ptF("P") }], draw); if (!g) return;
    var lam = Fr(1), sl = $(g.w, "lam"), lv = $(g.w, "lv"), fit = $(g.w, "fit"), target = null;
    sl.addEventListener("input", function () { lam = Fr(Math.round(+sl.value * 4), 4); draw(); });
    fit.addEventListener("click", function () { if (target) { lam = target; sl.value = fVal(target); draw(); } });
    onLang(function () { fit.textContent = t3("Pla que passa per P", "Plano que pasa por P", "Plane through P"); });
    function draw() {
      var a = g.f.v.p1, b = g.f.v.p2, P = g.f.v.P, n1 = a.slice(0, 3), n2 = b.slice(0, 3);
      lv.innerHTML = tex(fT(lam));
      if (vzero(n1) || vzero(n2) || vzero(vcross(n1, n2))) {
        target = null; fit.disabled = true;
        bad(g, t3("Els plans \\(\\pi_1\\) i \\(\\pi_2\\) han de ser secants (no paral·lels) per a determinar una recta.", "Los planos \\(\\pi_1\\) y \\(\\pi_2\\) tienen que ser secantes (no paralelos) para determinar una recta.", "The planes \\(\\pi_1\\) and \\(\\pi_2\\) must intersect (not be parallel) to determine a line.").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }));
        g.scene = { items: [], w: 340, h: 300 }; g.redraw(); return;
      }
      var L = lineOf([a.slice(0, 3).concat([-a[3]]), b.slice(0, 3).concat([-b[3]]), a.slice(0, 3).concat([-a[3]])]);
      var c = [0, 1, 2, 3].map(function (i) { return fAdd(a[i], fMul(lam, b[i])); }), cur = vzero(c.slice(0, 3)) ? null : planeEq(c.slice(0, 3), c[3]);
      var v1 = fVal(evalPlane(a, P)), v2 = fVal(evalPlane(b, P)), rows = [];
      rows.push([t3("Recta", "Recta", "Line") + " " + tex("r"), tex("(x,y,z)=" + vT(L.P) + "+t" + vT(L.d))]);
      rows.push([t3("Feix", "Haz", "Pencil"), tex("(" + poly([[a[0], "x"], [a[1], "y"], [a[2], "z"], [a[3], ""]]) + ")+\\lambda(" + poly([[b[0], "x"], [b[1], "y"], [b[2], "z"], [b[3], ""]]) + ")=0")]);
      rows.push([cdot(PCOL[2][1]) + tex("\\lambda=" + fT(lam)), cur ? tex(cur.t) : t3("(no és un pla)", "(no es un plano)", "(not a plane)")]);
      var msg;
      if (!v1 && !v2) { target = null; msg = t3("P és de la recta r: tots els plans del feix hi passen.", "P está en la recta r: todos los planos del haz pasan por él.", "P lies on r: every plane in the pencil passes through it."); }
      else if (!v2) { target = null; msg = t3("Cap valor de λ: el pla que passa per P és el mateix π₂ (el que perdem en escriure π₁ + λπ₂).", "Ningún valor de λ: el plano que pasa por P es el propio π₂ (el que perdemos al escribir π₁ + λπ₂).", "No value of λ works: the plane through P is π₂ itself (the one lost when writing π₁ + λπ₂)."); }
      else { target = Fr(-v1, v2); var tp = vzero(vadd(a.slice(0, 3), vmul(b.slice(0, 3), target))) ? null : planeEq(vadd(a.slice(0, 3), vmul(b.slice(0, 3), target)), fAdd(a[3], fMul(target, b[3]))); msg = tex(poly([[v1, ""], [v2, "\\lambda"]]) + "=0\\Rightarrow\\lambda=" + fT(target)) + (tp ? "<br>" + tex(tp.t) : ""); }
      fit.disabled = !target;
      rows.push([t3("Pla per ", "Plano por ", "Plane through ") + tex("P"), msg]);
      var items = [];
      if (cur) items.push({ plane: vnum(c.slice(0, 3)).concat([fVal(c[3])]), fill: PCOL[2][0], stroke: PCOL[2][1], op: 0.45 });
      items.push({ line: [vnum(L.P), L.d], stroke: COL.s, w: 3, label: "r" }, drop(P), dot3(P, "P", COL.p));
      g.scene = { items: items, L: Lof([P, vnum(L.P)], 3), w: 340, h: 300 }; g.redraw();
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  // una fila amb l'etiqueta buida ocupa tot l'ample (per a fórmules llargues i missatges)
  function kv(rows) { return '<div class="kv">' + rows.map(function (r) { return r[0] === "" ? '<span class="full">' + r[1] + "</span>" : "<span>" + r[0] + "</span><span>" + r[1] + "</span>"; }).join("") + "</div>"; }
  function cdot(c) { return '<i class="tag-c" style="background:' + c + '"></i>'; }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("El mòdul de $\\vec v=(2,-3,6)$ és…", "El módulo de $\\vec v=(2,-3,6)$ es…", "The magnitude of $\\vec v=(2,-3,6)$ is…"),
      o: [q3("$7$"), q3("$5$"), q3("$\\sqrt{11}$")], a: 0, e: q3("$\\sqrt{4+9+36}=\\sqrt{49}=7$.") },
    { q: q3("El simètric de $A(1,2,3)$ respecte de $M(2,2,2)$ és…", "El simétrico de $A(1,2,3)$ respecto de $M(2,2,2)$ es…", "The reflection of $A(1,2,3)$ in $M(2,2,2)$ is…"),
      o: [q3("$(3,2,1)$"), q3("$\\left(\\frac32,2,\\frac52\\right)$"), q3("$(1,0,-1)$")], a: 0, e: q3("$A'=2M-A=(4-1,\\,4-2,\\,4-3)=(3,2,1)$.") },
    { q: q3("Tres vectors de l'espai formen una base si…", "Tres vectores del espacio forman una base si…", "Three vectors in space form a basis if…"),
      o: [q3("el seu determinant és 0", "su determinante es 0", "their determinant is 0"), q3("el seu determinant no és 0", "su determinante no es 0", "their determinant is not 0"), q3("cap d'ells és nul", "ninguno de ellos es nulo", "none of them is zero")], a: 1, e: q3("Determinant no nul $\\iff$ rang 3 $\\iff$ linealment independents.", "Determinante no nulo $\\iff$ rango 3 $\\iff$ linealmente independientes.", "Nonzero determinant $\\iff$ rank 3 $\\iff$ linearly independent.") },
    { q: q3("Si $\\vec u\\cdot\\vec v=0$ (i cap és nul), els vectors són…", "Si $\\vec u\\cdot\\vec v=0$ (y ninguno es nulo), los vectores son…", "If $\\vec u\\cdot\\vec v=0$ (neither zero), the vectors are…"),
      o: [q3("paral·lels", "paralelos", "parallel"), q3("perpendiculars", "perpendiculares", "perpendicular"), q3("coplanaris", "coplanarios", "coplanar")], a: 1, e: q3("$\\cos\\alpha=0\\Rightarrow\\alpha=90^\\circ$.") },
    { q: q3("El resultat de $\\vec u\\times\\vec v$ és…", "El resultado de $\\vec u\\times\\vec v$ es…", "The result of $\\vec u\\times\\vec v$ is…"),
      o: [q3("un nombre", "un número", "a number"), q3("un vector paral·lel a $\\vec u$", "un vector paralelo a $\\vec u$", "a vector parallel to $\\vec u$"), q3("un vector perpendicular a $\\vec u$ i a $\\vec v$", "un vector perpendicular a $\\vec u$ y a $\\vec v$", "a vector perpendicular to $\\vec u$ and $\\vec v$")], a: 2, e: q3("El producte escalar dona un nombre; el vectorial, un vector perpendicular a tots dos.", "El producto escalar da un número; el vectorial, un vector perpendicular a ambos.", "The dot product gives a number; the cross product, a vector perpendicular to both.") },
    { q: q3("$(1,0,0)\\times(0,1,0)$ és…", "$(1,0,0)\\times(0,1,0)$ es…", "$(1,0,0)\\times(0,1,0)$ is…"),
      o: [q3("$(0,0,1)$"), q3("$(0,0,-1)$"), q3("$0$")], a: 0, e: q3("$\\vec i\\times\\vec j=\\vec k$ (i $\\vec j\\times\\vec i=-\\vec k$).", "$\\vec i\\times\\vec j=\\vec k$ (y $\\vec j\\times\\vec i=-\\vec k$).", "$\\vec i\\times\\vec j=\\vec k$ (and $\\vec j\\times\\vec i=-\\vec k$).") },
    { q: q3("L'àrea del triangle $ABC$ és…", "El área del triángulo $ABC$ es…", "The area of triangle $ABC$ is…"),
      o: [q3("$|\\overrightarrow{AB}\\times\\overrightarrow{AC}|$"), q3("$\\frac12|\\overrightarrow{AB}\\times\\overrightarrow{AC}|$"), q3("$\\frac12|\\overrightarrow{AB}\\cdot\\overrightarrow{AC}|$")], a: 1, e: q3("El mòdul del producte vectorial és l'àrea del paral·lelogram; el triangle n'és la meitat.", "El módulo del producto vectorial es el área del paralelogramo; el triángulo es la mitad.", "The magnitude of the cross product is the parallelogram's area; the triangle is half of it.") },
    { q: q3("Si $[\\vec u,\\vec v,\\vec w]=-12$, el volum del tetraedre que determinen és…", "Si $[\\vec u,\\vec v,\\vec w]=-12$, el volumen del tetraedro que determinan es…", "If $[\\vec u,\\vec v,\\vec w]=-12$, the volume of the tetrahedron they span is…"),
      o: [q3("$-2$"), q3("$12$"), q3("$2$")], a: 2, e: q3("$V=\\frac{|-12|}{6}=2$: el volum sempre és positiu.", "$V=\\frac{|-12|}{6}=2$: el volumen siempre es positivo.", "$V=\\frac{|-12|}{6}=2$: a volume is always positive.") },
    { q: q3("Un vector director de $\\frac{x-1}{2}=\\frac{y+3}{-1}=\\frac{z}{4}$ és…", "Un vector director de $\\frac{x-1}{2}=\\frac{y+3}{-1}=\\frac{z}{4}$ es…", "A direction vector of $\\frac{x-1}{2}=\\frac{y+3}{-1}=\\frac{z}{4}$ is…"),
      o: [q3("$(1,-3,0)$"), q3("$(2,-1,4)$"), q3("$(-1,3,0)$")], a: 1, e: q3("Els denominadors: $(2,-1,4)$. El punt és $(1,-3,0)$.", "Los denominadores: $(2,-1,4)$. El punto es $(1,-3,0)$.", "The denominators: $(2,-1,4)$. The point is $(1,-3,0)$.") },
    { q: q3("Un vector normal del pla $3x-y+2z=5$ és…", "Un vector normal del plano $3x-y+2z=5$ es…", "A normal vector of the plane $3x-y+2z=5$ is…"),
      o: [q3("$(3,-1,2)$"), q3("$(1,3,0)$"), q3("$(3,-1,5)$")], a: 0, e: q3("Els coeficients de $x$, $y$, $z$: $\\vec n=(3,-1,2)$.", "Los coeficientes de $x$, $y$, $z$: $\\vec n=(3,-1,2)$.", "The coefficients of $x$, $y$, $z$: $\\vec n=(3,-1,2)$.") },
    { q: q3("Dues rectes amb directors no proporcionals i $[\\vec d_r,\\vec d_s,\\overrightarrow{PQ}]\\neq0$…", "Dos rectas con directores no proporcionales y $[\\vec d_r,\\vec d_s,\\overrightarrow{PQ}]\\neq0$…", "Two lines with non-proportional directions and $[\\vec d_r,\\vec d_s,\\overrightarrow{PQ}]\\neq0$…"),
      o: [q3("es tallen", "se cortan", "intersect"), q3("són paral·leles", "son paralelas", "are parallel"), q3("s'encreuen", "se cruzan", "are skew")], a: 2, e: q3("Rangs 2 i 3: no són coplanàries, s'encreuen.", "Rangos 2 y 3: no son coplanarias, se cruzan.", "Ranks 2 and 3: not coplanar, so skew.") },
    { q: q3("Si $\\vec n\\cdot\\vec d=0$, la recta i el pla…", "Si $\\vec n\\cdot\\vec d=0$, la recta y el plano…", "If $\\vec n\\cdot\\vec d=0$, the line and the plane…"),
      o: [q3("es tallen en un punt", "se cortan en un punto", "meet at one point"), q3("són paral·lels o la recta és continguda en el pla", "son paralelos o la recta está contenida en el plano", "are parallel or the line lies in the plane"), q3("són perpendiculars", "son perpendiculares", "are perpendicular")], a: 1, e: q3("El director és perpendicular al normal: cal mirar si un punt de la recta és del pla.", "El director es perpendicular al normal: hay que mirar si un punto de la recta está en el plano.", "The direction is perpendicular to the normal: check whether a point of the line lies on the plane.") },
    { q: q3("Tres plans amb $\\mathrm{rg}\\,M=2$, $\\mathrm{rg}\\,M^*=3$ i cap parell paral·lel…", "Tres planos con $\\mathrm{rg}\\,M=2$, $\\mathrm{rg}\\,M^*=3$ y ningún par paralelo…", "Three planes with $\\mathrm{rg}\\,M=2$, $\\mathrm{rg}\\,M^*=3$ and no two parallel…"),
      o: [q3("es tallen en una recta", "se cortan en una recta", "meet in a line"), q3("formen un prisma (secants dos a dos)", "forman un prisma (secantes dos a dos)", "form a prism (intersect in pairs)"), q3("es tallen en un punt", "se cortan en un punto", "meet at one point")], a: 1, e: q3("Sistema incompatible sense plans paral·lels: cada parell es talla en una recta i les tres rectes són paral·leles.", "Sistema incompatible sin planos paralelos: cada par se corta en una recta y las tres rectas son paralelas.", "No solution and no parallel planes: each pair meets in a line and the three lines are parallel.") },
    { q: q3("El pla del feix $(x+y-1)+\\lambda(z-2)=0$ que passa per l'origen té…", "El plano del haz $(x+y-1)+\\lambda(z-2)=0$ que pasa por el origen tiene…", "The plane of the pencil $(x+y-1)+\\lambda(z-2)=0$ through the origin has…"),
      o: [q3("$\\lambda=\\frac12$"), q3("$\\lambda=-\\frac12$"), q3("$\\lambda=2$")], a: 1, e: q3("$-1-2\\lambda=0\\Rightarrow\\lambda=-\\frac12$.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Vectors, rectes i plans · FentMates", es: "Vectores, rectas y planos · FentMates", en: "Vectors, lines and planes · FentMates" };
  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l; root.setAttribute("data-lang", l); root.lang = HTML_LANG[l]; document.title = TITLES[l]; store("lang", l);
    try { var url = new URL(location.href); if (url.searchParams.has("lang")) { url.searchParams.set("lang", l); history.replaceState(null, "", url); } } catch (e) {}
    refreshers.forEach(function (fn) { fn(); });
  }

  function init() {
    document.title = TITLES[lang];
    var Dl = [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }];
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, { delimiters: Dl, ignoredClasses: ["widget", "lab"], throwOnError: false });
      document.querySelectorAll(".widget .wt, .widget label, .widget .legend, .widget > p, #lab .bh, #w-lab > p").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wVec, wPts, wDep, wDot, wCross, wMix, wLine, wPlane, wRR, wRP, wFeix, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM3 = { Fr: Fr, det3: det3, rank: rank, classify3: classify3, solve3: solve3, lineOf: lineOf, lineEqs: lineEqs, planeEq: planeEq };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
