  /* =====================================================================
     MII: GEOMETRIA A L'ESPAI (dibuixos 3D i ginys) I AFEGITS D'ANÀLISI
     ===================================================================== */
  var UI2 = {
    va: { vin: "Vectors", dep: "Linealment dependents (coplanaris)", indep: "Linealment independents", areaP: "Àrea paral·lelogram", areaT: "Àrea triangle", volT: "Volum tetraedre",
      noAng: "No hi ha angle: algun vector és nul.", rr: ["Coincidents", "Paral·leles", "Secants", "S'encreuen"], prop: "proporcionals", nprop: "no proporcionals",
      cut: "Punt de tall", dist: "Distància", pIn: "P és de s", pOut: "P no és de s", notPlane: "Algun pla té A = B = C = 0: no és un pla.",
      p3: ["Secants en un punt", "Secants dos a dos", "Dos paral·lels secants al tercer", "Secants en una recta", "Dos coincidents secants al tercer", "Paral·lels", "Dos coincidents paral·lels al tercer", "Coincidents"],
      p3s: ["Punt", "Prisma", "2 // + 1", "Recta", "2 ≡ + 1", "// // //", "2 ≡ // 1", "≡ ≡ ≡"], point: "Punt comú", onPlane: "P és del pla: Q = P = P′ i d = 0.",
      proj: "Projecció", sym: "Simètric", bnext: "Bisecció: següent pas", bdone: "Ja tenim l'arrel amb prou precisió", root: "Arrel", interval: "Interval", sign: "canvi de signe en" },
    es: { vin: "Vectores", dep: "Linealmente dependientes (coplanarios)", indep: "Linealmente independientes", areaP: "Área paralelogramo", areaT: "Área triángulo", volT: "Volumen tetraedro",
      noAng: "No hay ángulo: algún vector es nulo.", rr: ["Coincidentes", "Paralelas", "Secantes", "Se cruzan"], prop: "proporcionales", nprop: "no proporcionales",
      cut: "Punto de corte", dist: "Distancia", pIn: "P está en s", pOut: "P no está en s", notPlane: "Algún plano tiene A = B = C = 0: no es un plano.",
      p3: ["Secantes en un punto", "Secantes dos a dos", "Dos paralelos secantes al tercero", "Secantes en una recta", "Dos coincidentes secantes al tercero", "Paralelos", "Dos coincidentes paralelos al tercero", "Coincidentes"],
      p3s: ["Punto", "Prisma", "2 // + 1", "Recta", "2 ≡ + 1", "// // //", "2 ≡ // 1", "≡ ≡ ≡"], point: "Punto común", onPlane: "P está en el plano: Q = P = P′ y d = 0.",
      proj: "Proyección", sym: "Simétrico", bnext: "Bisección: siguiente paso", bdone: "Ya tenemos la raíz con suficiente precisión", root: "Raíz", interval: "Intervalo", sign: "cambio de signo en" },
    en: { vin: "Vectors", dep: "Linearly dependent (coplanar)", indep: "Linearly independent", areaP: "Parallelogram area", areaT: "Triangle area", volT: "Tetrahedron volume",
      noAng: "No angle: one of the vectors is zero.", rr: ["Coincident", "Parallel", "Intersecting", "Skew"], prop: "proportional", nprop: "not proportional",
      cut: "Intersection point", dist: "Distance", pIn: "P lies on s", pOut: "P is not on s", notPlane: "Some plane has A = B = C = 0: it is not a plane.",
      p3: ["Meeting at one point", "Intersecting in pairs (prism)", "Two parallel, cut by the third", "Meeting in a line", "Two coincident, cut by the third", "Parallel", "Two coincident, parallel to the third", "Coincident"],
      p3s: ["Point", "Prism", "2 // + 1", "Line", "2 ≡ + 1", "// // //", "2 ≡ // 1", "≡ ≡ ≡"], point: "Common point", onPlane: "P lies on the plane: Q = P = P′ and d = 0.",
      proj: "Projection", sym: "Reflection", bnext: "Bisection: next step", bdone: "The root is already accurate enough", root: "Root", interval: "Interval", sign: "sign change on" }
  };
  LANGS.forEach(function (l) { for (var k in UI2[l]) UI[l][k] = UI2[l][k]; });

  /* ---------- vectors amb fraccions exactes ---------- */
  var F0 = new Fr(0);
  function vsub(a, b) { return a.map(function (x, i) { return x.sub(b[i]); }); }
  function vadd(a, b) { return a.map(function (x, i) { return x.add(b[i]); }); }
  function vscale(a, k) { return a.map(function (x) { return x.mul(k); }); }
  function vdot(a, b) { return a.reduce(function (s, x, i) { return s.add(x.mul(b[i])); }, F0); }
  function vcross(a, b) { return [a[1].mul(b[2]).sub(a[2].mul(b[1])), a[2].mul(b[0]).sub(a[0].mul(b[2])), a[0].mul(b[1]).sub(a[1].mul(b[0]))]; }
  function vzero(a) { return a.every(function (x) { return x.zero(); }); }
  function vnum(a) { return a.map(function (x) { return x.n / x.d; }); }
  function vtex(a) { return "(" + a.map(function (x) { return x.tex(); }).join(",\\,") + ")"; }
  function tdec(x, d) { return dec(x, d).replace(",", "{,}"); }
  function ftex(x) { return x.n < 0 ? "(" + x.tex() + ")" : x.tex(); }
  /* arrel quadrada exacta d'una fracció no negativa: k·√m / d */
  function sqrtFr(x) {
    if (x.zero()) return { tex: "0", v: 0, exact: true };
    var N = x.n * x.d, D = x.d, k = 1, m = N;
    for (var p = 2; p * p <= m; p++) while (m % (p * p) === 0) { m /= p * p; k *= p; }
    var g = gcd(k, D); k /= g; D /= g;
    var top = m === 1 ? String(k) : (k === 1 ? "" : k) + "\\sqrt{" + m + "}";
    return { tex: D === 1 ? top : "\\frac{" + top + "}{" + D + "}", v: Math.sqrt(x.n / x.d), exact: m === 1 };
  }
  function vecInputs(box, groups) {
    box.innerHTML = ""; box.classList.add("vin");
    return groups.map(function (g) {
      var lab = document.createElement("label"), ins = [];
      lab.innerHTML = tex(g.name) + "<span>=(</span>";
      g.vals.forEach(function (v, i) {
        var inp = document.createElement("input"); inp.type = "text"; inp.inputMode = "decimal"; inp.autocomplete = "off"; inp.value = v;
        inp.setAttribute("aria-label", g.name.replace(/\\[a-z]+\s?|[{}]/g, "") + " " + (i + 1));
        lab.appendChild(inp); ins.push(inp);
        if (i < g.vals.length - 1) lab.appendChild(document.createTextNode(","));
      });
      lab.appendChild(document.createTextNode(")"));
      box.appendChild(lab); return ins;
    });
  }
  function readVec(ins) { var v = ins.map(function (x) { return parseFr(x.value); }); return v.every(Boolean) ? v : null; }
  function setVec(ins, vals) { ins.forEach(function (x, i) { x.value = String(vals[i]); }); }

  /* ---------- dibuixos 3D: projecció ortogonal amb gir (arrossegant) ---------- */
  var PCOL = [["#f48fb1", "#c2185b"], ["#ffe082", "#b8860b"], ["#90caf9", "#1565c0"]];
  function d3(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function x3(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function planePoly(n, d, L) { /* polígon de n·p + d = 0 dins del cub [-L, L]³ */
    var V = [], pts = [], i, j;
    for (i = 0; i < 8; i++) V.push([i & 1 ? L : -L, i & 2 ? L : -L, i & 4 ? L : -L]);
    var f = V.map(function (p) { return d3(n, p) + d; });
    for (i = 0; i < 8; i++) if (Math.abs(f[i]) < 1e-9) pts.push(V[i]);
    for (i = 0; i < 8; i++) for (j = i + 1; j < 8; j++) {
      var x = i ^ j; if (x !== 1 && x !== 2 && x !== 4) continue;
      if ((f[i] < -1e-9 && f[j] > 1e-9) || (f[i] > 1e-9 && f[j] < -1e-9)) { var t = f[i] / (f[i] - f[j]); pts.push([0, 1, 2].map(function (k) { return V[i][k] + t * (V[j][k] - V[i][k]); })); }
    }
    if (pts.length < 3) return null;
    var c = [0, 1, 2].map(function (k) { return pts.reduce(function (s, p) { return s + p[k]; }, 0) / pts.length; });
    var e1 = Math.abs(n[0]) < 0.9 ? x3(n, [1, 0, 0]) : x3(n, [0, 1, 0]), e2 = x3(n, e1);
    return pts.map(function (p) { var q = [p[0] - c[0], p[1] - c[1], p[2] - c[2]]; return { p: p, a: Math.atan2(d3(q, e2), d3(q, e1)) }; })
      .sort(function (a, b) { return a.a - b.a; }).map(function (o) { return o.p; });
  }
  function clipLine(p, v, L) { /* tros de la recta p + t·v dins del cub */
    var t0 = -1e9, t1 = 1e9;
    for (var k = 0; k < 3; k++) {
      if (Math.abs(v[k]) < 1e-12) { if (Math.abs(p[k]) > L) return null; continue; }
      var a = (-L - p[k]) / v[k], b = (L - p[k]) / v[k]; if (a > b) { var t = a; a = b; b = t; }
      t0 = Math.max(t0, a); t1 = Math.min(t1, b);
    }
    if (t0 > t1) return null;
    return [[p[0] + t0 * v[0], p[1] + t0 * v[1], p[2] + t0 * v[2]], [p[0] + t1 * v[0], p[1] + t1 * v[1], p[2] + t1 * v[2]]];
  }
  function scene3d(el, o) {
    var L = o.L || 2, yaw = (o.yaw == null ? 35 : o.yaw) * Math.PI / 180, pit = (o.pitch == null ? 22 : o.pitch) * Math.PI / 180;
    var R = [-Math.sin(yaw), Math.cos(yaw), 0], U = [-Math.sin(pit) * Math.cos(yaw), -Math.sin(pit) * Math.sin(yaw), Math.cos(pit)], D = [Math.cos(pit) * Math.cos(yaw), Math.cos(pit) * Math.sin(yaw), Math.sin(pit)];
    function pr(p) { return [d3(p, R), d3(p, U), d3(p, D)]; }
    var polys = [], segs = [], pts = [], txts = [], all = [];
    if (o.axes !== false) {
      [[1, 0, 0, "X"], [0, 1, 0, "Y"], [0, 0, 1, "Z"]].forEach(function (a) {
        var e = [a[0] * L * 1.15, a[1] * L * 1.15, a[2] * L * 1.15];
        segs.push({ a: [-e[0] * 0.87, -e[1] * 0.87, -e[2] * 0.87], b: [0, 0, 0], stroke: "var(--ax)", w: 1, dash: "3 3" });
        segs.push({ a: [0, 0, 0], b: e, stroke: "var(--ax)", w: 1.2, arrow: true });
        txts.push({ p: [e[0] * 1.08, e[1] * 1.08, e[2] * 1.08], s: a[3], cls: "lb" });
      });
    }
    (o.items || []).forEach(function (it) {
      if (it.plane) { var P = planePoly(it.plane.slice(0, 3), it.plane[3], L); if (P) polys.push({ pts: P, fill: it.fill || PCOL[0][0], stroke: it.stroke || PCOL[0][1], op: it.op == null ? 0.45 : it.op }); }
      else if (it.poly) polys.push({ pts: it.poly, fill: it.fill || "none", stroke: it.stroke || "var(--text)", op: it.op == null ? 0.3 : it.op, w: it.w });
      else if (it.line) { var E = clipLine(it.line[0], it.line[1], L * 1.15); if (E) segs.push({ a: E[0], b: E[1], stroke: it.stroke, w: it.w || 2, dash: it.dash }); if (it.label && E) txts.push({ p: E[1], s: it.label, cls: "lb", fill: it.stroke }); }
      else if (it.seg) { segs.push({ a: it.seg[0], b: it.seg[1], stroke: it.stroke, w: it.w || 2, dash: it.dash, arrow: it.arrow }); if (it.label) txts.push({ p: [0, 1, 2].map(function (k) { return (it.seg[0][k] + it.seg[1][k]) / 2; }), s: it.label, cls: "lb", fill: it.stroke, dx: it.dx, dy: it.dy }); }
      else if (it.pt) { pts.push({ p: it.pt, fill: it.fill }); if (it.label) txts.push({ p: it.pt, s: it.label, cls: "lb", dx: it.dx == null ? 6 : it.dx, dy: it.dy == null ? -6 : it.dy }); }
      else if (it.txt) txts.push({ p: it.txt, s: it.s, cls: it.cls || "", fill: it.fill });
    });
    polys.forEach(function (q) { q.pp = q.pts.map(pr); q.z = q.pp.reduce(function (s, p) { return s + p[2]; }, 0) / q.pp.length; all = all.concat(q.pp); });
    segs.forEach(function (q) { q.pa = pr(q.a); q.pb = pr(q.b); all.push(q.pa, q.pb); });
    pts.forEach(function (q) { q.pp = pr(q.p); all.push(q.pp); });
    txts.forEach(function (q) { q.pp = pr(q.p); });
    var W = o.w || 300, H = o.h || 250, pad = 14, cx, cy, sc;
    if (o.fit) {
      var x0 = Math.min.apply(null, all.map(function (p) { return p[0]; })), x1 = Math.max.apply(null, all.map(function (p) { return p[0]; }));
      var y0 = Math.min.apply(null, all.map(function (p) { return p[1]; })), y1 = Math.max.apply(null, all.map(function (p) { return p[1]; }));
      sc = Math.min((W - 2 * pad) / (x1 - x0 || 1), (H - 2 * pad) / (y1 - y0 || 1)); cx = (x0 + x1) / 2; cy = (y0 + y1) / 2;
    } else { sc = Math.min(W, H) / 2 / (L * 1.3); cx = 0; cy = 0; }
    function X(p) { return +(W / 2 + (p[0] - cx) * sc).toFixed(1); }
    function Y(p) { return +(H / 2 - (p[1] - cy) * sc).toFixed(1); }
    var id = "q" + Math.random().toString(36).slice(2, 8), s = [];
    s.push('<defs><marker id="' + id + '" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>');
    polys.sort(function (a, b) { return a.z - b.z; }).forEach(function (q) {
      s.push('<path d="' + q.pp.map(function (p, i) { return (i ? "L" : "M") + X(p) + " " + Y(p); }).join("") + 'Z" fill="' + q.fill + '" fill-opacity="' + q.op + '" stroke="' + q.stroke + '" stroke-width="' + (q.w || 1.1) + '" stroke-linejoin="round"/>');
    });
    segs.forEach(function (q) {
      s.push('<line x1="' + X(q.pa) + '" y1="' + Y(q.pa) + '" x2="' + X(q.pb) + '" y2="' + Y(q.pb) + '" stroke="' + (q.stroke || "var(--text)") + '" stroke-width="' + (q.w || 2) + '" stroke-linecap="round"' + (q.dash ? ' stroke-dasharray="' + (q.dash === true ? "5 4" : q.dash) + '"' : "") + (q.arrow ? ' marker-end="url(#' + id + ')"' : "") + "/>");
    });
    pts.forEach(function (q) { s.push('<circle cx="' + X(q.pp) + '" cy="' + Y(q.pp) + '" r="3.6" fill="' + (q.fill || "var(--text)") + '" stroke="var(--surface)" stroke-width="1"/>'); });
    txts.forEach(function (q) { s.push('<text class="' + q.cls + '" x="' + (X(q.pp) + (q.dx || 0)) + '" y="' + (Y(q.pp) + (q.dy || 0)) + '"' + (q.fill ? ' style="fill:' + q.fill + '"' : "") + ">" + q.s + "</text>"); });
    el.innerHTML = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-hidden="true">' + s.join("") + "</svg>";
  }
  /* escena girable: getScene() torna l'escena; el gir es conserva entre redibuixos */
  function s3mount(el, getScene) {
    var view = { yaw: 35, pitch: 22 }, drag = null;
    function draw() { var o = getScene(); o.yaw = view.yaw; o.pitch = view.pitch; scene3d(el, o); }
    el.addEventListener("pointerdown", function (e) { drag = [e.clientX, e.clientY]; try { el.setPointerCapture(e.pointerId); } catch (er) {} });
    el.addEventListener("pointermove", function (e) {
      if (!drag) return;
      view.yaw -= (e.clientX - drag[0]) * 0.6; view.pitch = Math.max(-85, Math.min(85, view.pitch + (e.clientY - drag[1]) * 0.6));
      drag = [e.clientX, e.clientY]; draw();
    });
    ["pointerup", "pointercancel"].forEach(function (t) { el.addEventListener(t, function () { drag = null; }); });
    return draw;
  }
  function arrow3(p, v, col, label, extra) { var it = { seg: [p, [p[0] + v[0], p[1] + v[1], p[2] + v[2]]], stroke: col, w: 2.4, arrow: true, label: label }; for (var k in extra || {}) it[k] = extra[k]; return it; }
  function pl(i, n, d) { return { plane: n.concat([d]), fill: PCOL[i][0], stroke: PCOL[i][1] }; }
  function sp(p) { /* punt del pla z = 0.25x - 0.2y (dibuix de coplanaris) */ return [p[0], p[1], 0.25 * p[0] - 0.2 * p[1]]; }

  var S3 = {
    cop: function () { var A = sp([1.5, -1]), B = sp([-1.5, -1.3]), C = sp([-1, 1.6]), D = sp([1.4, 1.5]);
      return { L: 2, axes: false, fit: true, h: 190, pitch: 40, items: [{ plane: [-0.25, 0.2, 1, 0], fill: "#cfd8dc", stroke: "#78909c", op: 0.6 },
        arrow3(A, vsubN(B, A), COL.blue), arrow3(A, vsubN(C, A), COL.blue), arrow3(A, vsubN(D, A), COL.blue),
        { pt: A, label: "A", fill: COL.blue }, { pt: B, label: "B", fill: COL.blue }, { pt: C, label: "C", fill: COL.blue }, { pt: D, label: "D", fill: COL.blue }] }; },
    ppd: function () { var a = [0, 2, 0], b = [1.4, 0.5, 0], e = [0.2, 0.3, 1.4], O = [0, 0, 0], it = [];
      var c = [O, a, vaddN(a, b), b], top = c.map(function (p) { return vaddN(p, e); });
      [c, top, [O, a, top[1], top[0]], [b, vaddN(a, b), top[2], top[3]], [O, b, top[3], top[0]], [a, vaddN(a, b), top[2], top[1]]].forEach(function (f) { it.push({ poly: f, fill: "#f06292", stroke: "#ad1457", op: 0.18 }); });
      it.push(arrow3(O, a, COL.red), arrow3(O, b, COL.red), arrow3(O, e, COL.red));
      it.push({ pt: O, label: "A", dx: -14, dy: 4 }, { pt: a, label: "B" }, { pt: b, label: "D", dx: -12, dy: 12 }, { pt: e, label: "E", dx: -14 });
      return { axes: false, fit: true, w: 200, h: 170, items: it }; },
    tet: function () { var A = [0, 0, 0], B = [0, 2, 0], C = [1.5, 0.9, 0], Dp = [0.5, 0.9, 1.7], it = [];
      [[A, B, C], [A, B, Dp], [A, C, Dp], [B, C, Dp]].forEach(function (f) { it.push({ poly: f, fill: "#9575cd", stroke: "#4527a0", op: 0.14 }); });
      it.push(arrow3(A, B, COL.red), arrow3(A, C, COL.red), arrow3(A, Dp, COL.red));
      it.push({ pt: A, label: "A", dx: -14, dy: 4 }, { pt: B, label: "B" }, { pt: C, label: "C", dx: -12, dy: 14 }, { pt: Dp, label: "D" });
      return { axes: false, fit: true, w: 200, h: 170, items: it }; },
    coord: function () { var L = 1.6;
      return { L: L, fit: true, h: 220, items: [{ poly: [[0, 0, 0], [L, 0, 0], [L, L, 0], [0, L, 0]], fill: "#7986cb", stroke: "#3949ab", op: 0.45 },
        { poly: [[0, 0, 0], [0, L, 0], [0, L, L], [0, 0, L]], fill: "#81c784", stroke: "#2e7d32", op: 0.45 },
        { poly: [[0, 0, 0], [L, 0, 0], [L, 0, L], [0, 0, L]], fill: "#e57373", stroke: "#c62828", op: 0.4 },
        { txt: [L * 0.55, L * 0.55, 0], s: "z = 0", fill: "#283593" }, { txt: [0, L * 0.45, L * 0.6], s: "x = 0", fill: "#1b5e20" }, { txt: [L * 0.7, 0, L * 0.65], s: "y = 0", fill: "#b71c1c" }] }; },
    symr: function () { var P = [1.2, -1.4, 0.6], Q = [0, 0, 0.2], P2 = [-1.2, 1.4, -0.2];
      return { L: 1.8, axes: false, fit: true, w: 220, h: 150, items: [{ line: [[0, 0, 0.2], [0.5, 0.45, 1]], stroke: "var(--text)", w: 1.6, label: "r" }, { seg: [P, P2], stroke: "#777", w: 1.4, dash: true },
        { pt: P, label: "P", fill: COL.blue }, { pt: Q, label: "Q", fill: COL.blue }, { pt: P2, label: "P′", fill: COL.blue }] }; },
    symp: function () { var P = [1.4, -1.6, 0.3], Q = [0, -0.1, 0.3], P2 = [-1.4, 1.4, 0.3];
      return { L: 1.4, axes: false, fit: true, w: 220, h: 150, items: [{ plane: [1, -0.95, 0, -0.1], fill: "#ffab91", stroke: "#e64a19", op: 0.6 }, { seg: [P, P2], stroke: "#777", w: 1.4, dash: true },
        { pt: P, label: "P", fill: COL.blue }, { pt: Q, label: "Q", fill: COL.blue }, { pt: P2, label: "P′", fill: COL.blue }, { txt: [0, 1.2, 1.2], s: "π", cls: "lb" }] }; },
    perp: function () { /* r: (t,0,-0.6)  s: (0,t,0.6)  t: eix OZ entre els peus */
      return { L: 1.6, axes: false, fit: true, h: 210, items: [{ line: [[0, 0, -0.6], [1, 0, 0]], stroke: COL.blue, label: "r" }, { line: [[0, 0, 0.6], [0, 1, 0]], stroke: COL.green, label: "s" },
        { line: [[0, 0, 0], [0, 0, 1]], stroke: "#999", w: 1, dash: true }, { seg: [[0, 0, -0.6], [0, 0, 0.6]], stroke: COL.red, w: 2.6, label: "t", dx: 6 },
        { pt: [0, 0, -0.6], fill: COL.red }, { pt: [0, 0, 0.6], fill: COL.red }, arrow3([0.9, 0.9, 0], [0, 0, 0.7], "#8064a1", "w", { w: 1.8 })] }; }
  };
  function vsubN(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function vaddN(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
  /* posició relativa de tres plans: exemples (Ax+By+Cz+D=0) i dibuix de cada cas */
  var P3 = [
    { eq: [[1, 1, 1, -3], [1, -1, 0, 0], [0, 1, -1, 0]], pic: [[[1, 0, 0], 0], [[0, 1, 0], 0], [[0, 0, 1], 0]] },
    { eq: [[1, 0, 0, -1], [0, 1, 0, -1], [1, 1, 0, 0]], pic: [0, 1, 2].map(function (k) { var a = Math.PI / 2 + k * 2 * Math.PI / 3; return [[Math.cos(a), Math.sin(a), 0], -0.55]; }) },
    { eq: [[0, 0, 1, -1], [0, 0, 1, 1], [1, 0, 0, 0]], pic: [[[0, 0, 1], -0.75], [[0, 0, 1], 0.75], [[1, 0, 0], 0]] },
    { eq: [[1, -1, 0, 0], [0, 1, -1, 0], [1, 0, -1, 0]], pic: [0, 1, 2].map(function (k) { var a = k * Math.PI / 3; return [[Math.cos(a), Math.sin(a), 0], 0]; }) },
    { eq: [[1, 1, 0, -1], [2, 2, 0, -2], [0, 0, 1, 0]], pic: [[[1, 0, 0], 0], [[1, 0, 0], 0], [[0, 0, 1], 0]] },
    { eq: [[0, 0, 1, -1], [0, 0, 1, 0], [0, 0, 1, 1]], pic: [[[0, 0, 1], -0.85], [[0, 0, 1], 0], [[0, 0, 1], 0.85]] },
    { eq: [[0, 0, 1, -1], [0, 0, 2, -2], [0, 0, 1, 1]], pic: [[[0, 0, 1], -0.5], [[0, 0, 1], -0.5], [[0, 0, 1], 0.6]] },
    { eq: [[1, 1, 1, -1], [2, 2, 2, -2], [-1, -1, -1, 1]], pic: [[[0, 0, 1], 0], [[0, 0, 1], 0], [[0, 0, 1], 0]] }
  ];
  P3.forEach(function (c, k) {
    S3["p3-" + k] = function () { return { L: 1.2, axes: false, w: 150, h: 120, items: c.pic.map(function (q, i) { return pl(i, q[0], q[1]); }) }; };
  });
  function drawS3() { $$("[data-s3]").forEach(function (el) { var f = S3[el.dataset.s3]; if (f) scene3d(el, f()); }); }

  /* figures 2D noves */
  function ellipse(cx, cy, rx, ry) { var p = []; for (var k = 0; k <= 48; k++) { var t = k / 48 * 2 * Math.PI; p.push([cx + rx * Math.cos(t), cy + ry * Math.sin(t)]); } return p; }
  function fRolle(x) { return -0.35 * (x - 0.6) * (x - 3.6) + 1; }
  PLOTS["g-proj"] = { x: [-0.4, 4.8], y: [-0.9, 2.7], grid: false, axes: false, h: 170, items: [
    { seg: [[0, 0], [4.4, 0]], stroke: "var(--text)", w: 1.8, arrow: true }, { seg: [[0, 0], [2.6, 2.2]], stroke: "var(--text)", w: 1.8, arrow: true },
    { seg: [[2.6, 2.2], [2.6, 0]], stroke: "#888", dash: true, w: 1.2 }, { seg: [[0, -0.35], [2.6, -0.35]], stroke: COL.blue, w: 2.2 },
    { txt: [4.45, 0.15], s: "u", cls: "lb" }, { txt: [2.45, 2.35], s: "v", cls: "lb" }, { txt: [0.55, 0.15], s: "α", cls: "lb" }, { txt: [0.7, -0.75], s: "Proj u v", fill: COL.blue }] };
  PLOTS["g-par"] = { x: [-0.5, 4.6], y: [-0.5, 2.2], grid: false, axes: false, h: 110, items: [
    { poly: [[0, 0], [3, 0], [4, 1.6], [1, 1.6]], fill: "#9e9e9e", op: 0.55, stroke: "#616161" }, { seg: [[0, 0], [3, 0]], stroke: "var(--text)", arrow: true }, { seg: [[0, 0], [1, 1.6]], stroke: "var(--text)", arrow: true },
    { pt: [0, 0], label: "A", dx: -12, dy: 4, fill: COL.blue, r: 3 }, { pt: [3, 0], label: "B", dy: 14, fill: COL.blue, r: 3 }, { pt: [1, 1.6], label: "C", fill: COL.blue, r: 3 }, { pt: [4, 1.6], label: "D", fill: COL.blue, r: 3 }] };
  PLOTS["g-tri"] = { x: [-0.5, 4.6], y: [-0.5, 2.2], grid: false, axes: false, h: 110, items: [
    { poly: [[0, 0], [3, 0], [1, 1.6]], fill: "#9e9e9e", op: 0.55, stroke: "#616161" }, { seg: [[3, 0], [4, 1.6]], stroke: "#999", w: 1, dash: true }, { seg: [[1, 1.6], [4, 1.6]], stroke: "#999", w: 1, dash: true },
    { seg: [[0, 0], [3, 0]], stroke: "var(--text)", arrow: true }, { seg: [[0, 0], [1, 1.6]], stroke: "var(--text)", arrow: true },
    { pt: [0, 0], label: "A", dx: -12, dy: 4, fill: COL.blue, r: 3 }, { pt: [3, 0], label: "B", dy: 14, fill: COL.blue, r: 3 }, { pt: [1, 1.6], label: "C", fill: COL.blue, r: 3 }] };
  PLOTS["g-sym"] = { x: [-0.3, 4.3], y: [-0.4, 1.2], grid: false, axes: false, h: 80, items: [
    { seg: [[0, 0.8], [4, 0.2]], stroke: "#777", dash: true, w: 1.4 }, { pt: [0, 0.8], label: "P", fill: COL.blue }, { pt: [2, 0.5], label: "Q", fill: COL.blue }, { pt: [4, 0.2], label: "P′", dx: -6, fill: COL.blue }] };
  PLOTS["a-rolle"] = { x: [-0.3, 4.3], y: [-0.4, 2.2], grid: false, ticks: false, h: 200, items: [
    { seg: [[0.6, 0], [0.6, 1]], stroke: "#999", dash: true, w: 1 }, { seg: [[3.6, 0], [3.6, 1]], stroke: "#999", dash: true, w: 1 }, { seg: [[2.1, 0], [2.1, fRolle(2.1)]], stroke: "#999", dash: true, w: 1 },
    { seg: [[0, 1], [4.2, 1]], stroke: "#bbb", dash: "2 4", w: 1 }, { fn: fRolle, from: 0.3, to: 3.9, stroke: COL.fn, w: 2.2 },
    { seg: [[1.3, fRolle(2.1)], [2.9, fRolle(2.1)]], stroke: COL.green, w: 2 }, { pt: [0.6, 1], fill: COL.fn, r: 3 }, { pt: [3.6, 1], fill: COL.fn, r: 3 }, { pt: [2.1, fRolle(2.1)], fill: COL.green, r: 3.4 },
    { txt: [0.6, -0.3], s: "a", cls: "lb", anchor: "middle" }, { txt: [2.1, -0.3], s: "c", cls: "lb", anchor: "middle" }, { txt: [3.6, -0.3], s: "b", cls: "lb", anchor: "middle" },
    { txt: [2.25, 2.03], s: "f′(c) = 0", fill: COL.green }, { txt: [3.65, 1.1], s: "f(a) = f(b)" }] };
  PLOTS["a-vol"] = { x: [-0.6, 4.9], y: [-2.6, 2.6], grid: false, ticks: false, h: 220, items: [
    { area: { f: Math.sqrt, g: function (x) { return -Math.sqrt(x); }, a: 0, b: 4, pos: "#90caf9", op: 0.35, n: 80 } },
    { fn: Math.sqrt, from: 0, to: 4, stroke: COL.fn, w: 2.2 }, { fn: function (x) { return -Math.sqrt(x); }, from: 0, to: 4, stroke: COL.fn, w: 1.4, dash: "4 3" },
    { poly: ellipse(4, 0, 0.32, 2), stroke: "#1565c0" }, { poly: ellipse(2, 0, 0.24, Math.SQRT2), stroke: "#1565c0", dash: true },
    { txt: [2.6, 1.85], s: "y = f(x)", fill: COL.fn }, { txt: [3.95, -0.35], s: "b", cls: "lb" }, { txt: [0.08, -0.35], s: "a", cls: "lb" }] };

  /* ---------- giny: calculadora de vectors ---------- */
  function wVec() {
    var w = $("#w-vec"); if (!w) return;
    var I = vecInputs($('[data-role="in"]', w), [{ name: "\\vec u", vals: [1, 1, 0] }, { name: "\\vec v", vals: [0, 1, 1] }, { name: "\\vec w", vals: [1, 0, 2] }]);
    var info = $(".info", w), cur = null;
    var draw = s3mount($('[data-role="plot"]', w), function () {
      if (!cur) return { items: [] };
      var u = vnum(cur[0]), v = vnum(cur[1]), x = vnum(cur[3]), ww = vnum(cur[2]);
      var m = Math.max(1, Math.max.apply(null, u.concat(v, ww, x).map(Math.abs)));
      return { L: m * 1.05, items: [{ poly: [[0, 0, 0], u, vaddN(u, v), v], fill: "#90caf9", stroke: "#64b5f6", op: 0.35 },
        arrow3([0, 0, 0], u, COL.blue, "u"), arrow3([0, 0, 0], v, COL.green, "v"), arrow3([0, 0, 0], ww, "#8064a1", "w"), arrow3([0, 0, 0], x, COL.red, "u×v", { dash: "6 3" })] };
    });
    function render() {
      var a = readVec(I[0]), b = readVec(I[1]), c = readVec(I[2]);
      if (!a || !b || !c) { info.textContent = u("bad"); return; }
      var x = vcross(a, b), dt = vdot(a, b), mix = vdot(a, vcross(b, c)), nu = vdot(a, a), nv = vdot(b, b), nx = vdot(x, x);
      cur = [a, b, c, x];
      var su = sqrtFr(nu), sv = sqrtFr(nv), sx = sqrtFr(nx), h = "";
      h += tex("|\\vec u|=" + su.tex + (su.exact ? "" : "\\approx " + tdec(su.v, 3)) + ",\\quad |\\vec v|=" + sv.tex + (sv.exact ? "" : "\\approx " + tdec(sv.v, 3))) + "<br>";
      h += tex("\\vec u+\\vec v=" + vtex(vadd(a, b)) + ",\\quad \\vec u-\\vec v=" + vtex(vsub(a, b))) + "<br>";
      h += tex("\\vec u\\cdot\\vec v=" + a.map(function (q, i) { return ftex(q) + "\\cdot " + ftex(b[i]); }).join("+") + "=" + dt.tex()) + "<br>";
      if (nu.zero() || nv.zero()) h += u("noAng") + "<br>";
      else { var cs = (dt.n / dt.d) / (su.v * sv.v); h += tex("\\alpha=\\arccos\\left(\\frac{" + dt.tex() + "}{" + su.tex + "\\cdot " + sv.tex + "}\\right)\\approx " + tdec(Math.acos(Math.max(-1, Math.min(1, cs))) * 180 / Math.PI, 2) + "^\\circ") + (dt.zero() ? " ⟂" : "") + "<br>"; }
      h += tex("\\color{" + COL.red + "}{\\vec u\\times\\vec v=" + vtex(x) + "}") + "<br>";
      h += u("areaP") + ": " + tex("|\\vec u\\times\\vec v|=" + sx.tex + (sx.exact ? "" : "\\approx " + tdec(sx.v, 3))) + " · " + u("areaT") + ": " + tex("\\approx " + tdec(sx.v / 2, 3)) + "<br>";
      h += tex("[\\vec u,\\vec v,\\vec w]=" + mix.tex()) + " ⇒ <strong>" + (mix.zero() ? u("dep") : u("indep")) + "</strong>";
      if (!mix.zero()) h += "<br>" + u("volT") + " (" + tex("\\vec u,\\vec v,\\vec w") + "): " + tex("\\frac{|" + mix.tex() + "|}{6}=" + new Fr(Math.abs(mix.n), mix.d * 6).tex());
      info.innerHTML = h; draw();
    }
    I.forEach(function (g) { g.forEach(function (x) { x.addEventListener("input", render); }); });
    onLang(render);
  }

  /* ---------- giny: posició relativa de dues rectes ---------- */
  var RR = [[[1, 0, 2], [1, 2, -1], [3, 4, 0], [-2, -4, 2]], [[1, 0, 2], [1, 2, -1], [0, 1, 0], [2, 4, -2]], [[1, 0, 2], [1, 2, -1], [1, 3, -1], [1, -1, 2]], [[1, 0, 2], [1, 2, -1], [0, 1, 0], [0, 1, 1]]];
  function wRR() {
    var w = $("#w-rr"); if (!w) return;
    var I = vecInputs($('[data-role="in"]', w), [{ name: "P", vals: RR[2][0] }, { name: "\\vec u", vals: RR[2][1] }, { name: "Q", vals: RR[2][2] }, { name: "\\vec v", vals: RR[2][3] }]);
    var info = $(".info", w), btns = $$(".seg button", w), cur = null;
    var draw = s3mount($('[data-role="plot"]', w), function () {
      if (!cur) return { items: [] };
      var P = vnum(cur.P), Q = vnum(cur.Q), m = Math.max(2, Math.max.apply(null, P.concat(Q).map(Math.abs)) * 1.2), it = [];
      it.push({ line: [P, vnum(cur.u)], stroke: COL.blue, label: "r", w: cur.k === 0 ? 4 : 2 }, { line: [Q, vnum(cur.v)], stroke: COL.green, label: "s", dash: cur.k === 0 ? "6 5" : false });
      it.push({ pt: P, label: "P", fill: COL.blue }, { pt: Q, label: "Q", fill: COL.green });
      if (cur.X) it.push({ pt: vnum(cur.X), fill: COL.red, label: "X" });
      return { L: m, items: it };
    });
    function render() {
      var P = readVec(I[0]), U = readVec(I[1]), Q = readVec(I[2]), V = readVec(I[3]);
      if (!P || !U || !Q || !V || vzero(U) || vzero(V)) { info.textContent = u("bad"); return; }
      var PQ = vsub(Q, P), par = vzero(vcross(U, V)), h = "", k, X = null;
      h += tex("\\vec u=" + vtex(U) + ",\\ \\vec v=" + vtex(V)) + " → " + (par ? u("prop") : u("nprop")) + "<br>";
      h += tex("\\overrightarrow{PQ}=" + vtex(PQ)) + "<br>";
      if (par) {
        var on = vzero(vcross(PQ, V)); k = on ? 0 : 1;
        h += (on ? u("pIn") : u("pOut")) + " (" + tex("\\overrightarrow{PQ}" + (on ? "\\parallel" : "\\nparallel") + "\\vec v") + ")";
        if (!on) { var num = vdot(vcross(PQ, V), vcross(PQ, V)), den = vdot(V, V), q = sqrtFr(num.div(den)); h += "<br>" + u("dist") + ": " + tex("d(r,s)=\\frac{|\\overrightarrow{PQ}\\times\\vec v|}{|\\vec v|}=" + q.tex + (q.exact ? "" : "\\approx " + tdec(q.v, 3))); }
      } else {
        var M = [PQ, U, V], dt = detFr(M); k = dt.zero() ? 2 : 3;
        h += tex("\\det(\\overrightarrow{PQ},\\vec u,\\vec v)=\\begin{vmatrix}" + M.map(function (r) { return r.map(function (x) { return x.tex(); }).join("&"); }).join("\\\\") + "\\end{vmatrix}=" + dt.tex());
        if (k === 2) {
          /* P + λu = Q + μv: resolem amb dues coordenades de determinant no nul */
          var pr = [[0, 1], [0, 2], [1, 2]].filter(function (p) { return !U[p[0]].mul(V[p[1]]).sub(U[p[1]].mul(V[p[0]])).zero(); })[0];
          var a = pr[0], b = pr[1], den2 = U[a].mul(V[b]).sub(U[b].mul(V[a])), lam = PQ[a].mul(V[b]).sub(PQ[b].mul(V[a])).div(den2);
          X = vadd(P, vscale(U, lam)); h += "<br>" + u("cut") + ": " + tex("\\lambda=" + lam.tex() + "\\Rightarrow X" + vtex(X));
        } else {
          var cx = vcross(U, V), q2 = sqrtFr(new Fr(dt.n * dt.n, dt.d * dt.d).div(vdot(cx, cx)));
          h += "<br>" + u("dist") + ": " + tex("d(r,s)=\\frac{|" + dt.tex() + "|}{|\\vec u\\times\\vec v|}=" + q2.tex + (q2.exact ? "" : "\\approx " + tdec(q2.v, 3)));
        }
      }
      h = '<p><span class="verdict">' + u("rr")[k] + "</span></p>" + h;
      info.innerHTML = h; cur = { P: P, Q: Q, u: U, v: V, k: k, X: X }; draw();
    }
    btns.forEach(function (b) { b.addEventListener("click", function () {
      var c = RR[+b.dataset.k]; I.forEach(function (g, i) { setVec(g, c[i]); });
      btns.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); render(); }); });
    I.forEach(function (g) { g.forEach(function (x) { x.addEventListener("input", function () { btns.forEach(function (b) { b.setAttribute("aria-pressed", "false"); }); render(); }); }); });
    onLang(render);
  }

  /* ---------- giny: posició relativa de tres plans ---------- */
  function classify3(E) {
    var A = E.map(function (r) { return r.slice(0, 3); }), rA = rankFr(A), rS = rankFr(E);
    function pair(rows, i, j) { return rankFr([rows[i], rows[j]]) === 1; }
    var P = [[0, 1], [0, 2], [1, 2]], anyPar = P.some(function (p) { return pair(A, p[0], p[1]); }), anyCoin = P.some(function (p) { return pair(E, p[0], p[1]); });
    var k = rA === 3 ? 0 : rA === 2 && rS === 3 ? (anyPar ? 2 : 1) : rA === 2 ? (anyCoin ? 4 : 3) : rS === 2 ? (anyCoin ? 6 : 5) : 7;
    return { k: k, rA: rA, rS: rS };
  }
  function w3P() {
    var w = $("#w-3p"); if (!w) return;
    var box = $('[data-role="in"]', w), info = $(".info", w), segEl = $('[data-role="cases"]', w), ins = [], cur = null;
    box.innerHTML = ""; box.style.gridTemplateColumns = "auto repeat(4, auto)";
    ["", "A", "B", "C", "D"].forEach(function (t) { var s = document.createElement("span"); s.className = "c"; s.innerHTML = t ? "<strong>" + t + "</strong>" : ""; box.appendChild(s); });
    ["\\pi", "\\pi'", "\\pi''"].forEach(function (nm, i) {
      var s = document.createElement("span"); s.className = "c"; s.innerHTML = tex(nm); box.appendChild(s); ins.push([]);
      for (var j = 0; j < 4; j++) { var inp = document.createElement("input"); inp.type = "text"; inp.inputMode = "decimal"; inp.autocomplete = "off"; inp.value = P3[0].eq[i][j]; inp.setAttribute("aria-label", nm.replace("\\", "") + " " + "ABCD"[j]); box.appendChild(inp); ins[i].push(inp); }
    });
    var btns = P3.map(function (c, k) { var b = document.createElement("button"); b.type = "button"; b.dataset.k = k; segEl.appendChild(b); return b; });
    var draw = s3mount($('[data-role="plot"]', w), function () {
      if (!cur) return { items: [] };
      return { L: 2.2, items: cur.E.map(function (r, i) { var n = vnum(r.slice(0, 3)), d = r[3].n / r[3].d; return pl(i, n, d); }).concat(cur.X ? [{ pt: cur.X, fill: COL.red }] : []) };
    });
    function render() {
      var E = ins.map(function (r) { return r.map(function (x) { return parseFr(x.value); }); });
      if (!E.every(function (r) { return r.every(Boolean); })) { info.textContent = u("bad"); return; }
      if (E.some(function (r) { return vzero(r.slice(0, 3)); })) { info.textContent = u("notPlane"); cur = null; draw(); return; }
      var c = classify3(E), g = u("rg"), X = null;
      var h = '<p><span class="verdict">' + u("p3")[c.k] + "</span></p>";
      h += tex("A^*=\\left(\\begin{array}{ccc|c}" + E.map(function (r) { return r.map(function (x) { return x.tex(); }).join("&"); }).join("\\\\") + "\\end{array}\\right)", true);
      h += "<p>" + tex("\\text{" + g + "}(A)=" + c.rA + ",\\quad\\text{" + g + "}(A^*)=" + c.rS) + "</p>";
      if (c.k === 0) {
        var A = E.map(function (r) { return r.slice(0, 3); }), b = E.map(function (r) { return F0.sub(r[3]); }), dA = detFr(A);
        var sol = [0, 1, 2].map(function (cc) { return detFr(A.map(function (r, i) { return r.map(function (x, j) { return j === cc ? b[i] : x; }); })).div(dA); });
        X = vnum(sol); h += "<p>" + u("point") + ": " + tex(vtex(sol)) + "</p>";
      }
      info.innerHTML = h; cur = { E: E, X: X }; draw();
    }
    function paintBtns() { btns.forEach(function (b, k) { b.textContent = u("p3s")[k]; b.title = u("p3")[k]; }); }
    btns.forEach(function (b) { b.addEventListener("click", function () {
      var c = P3[+b.dataset.k]; ins.forEach(function (r, i) { setVec(r, c.eq[i]); });
      btns.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); render(); }); });
    btns[0].setAttribute("aria-pressed", "true");
    ins.forEach(function (r) { r.forEach(function (x) { x.addEventListener("input", function () { btns.forEach(function (b) { b.setAttribute("aria-pressed", "false"); }); render(); }); }); });
    onLang(function () { paintBtns(); render(); });
  }

  /* ---------- giny: punt i pla (projecció, simètric i distància) ---------- */
  function wPP() {
    var w = $("#w-pp"); if (!w) return;
    var I = vecInputs($('[data-role="in"]', w), [{ name: "P", vals: [1, 2, 2] }, { name: "\\pi:(A,B,C,D)", vals: [2, 1, 2, -2] }]);
    var info = $(".info", w), cur = null;
    var draw = s3mount($('[data-role="plot"]', w), function () {
      if (!cur) return { items: [] };
      var P = vnum(cur.P), Q = vnum(cur.Q), S = vnum(cur.S), m = Math.max(2, Math.max.apply(null, P.concat(S).map(Math.abs)) * 1.15);
      return { L: m, items: [{ plane: vnum(cur.n).concat([cur.D.n / cur.D.d]), fill: "#ffab91", stroke: "#e64a19", op: 0.5 }, { seg: [P, S], stroke: "#777", w: 1.4, dash: true },
        { pt: P, label: "P", fill: COL.blue }, { pt: Q, label: "Q", fill: COL.red }, { pt: S, label: "P′", fill: COL.green }] };
    });
    function render() {
      var P = readVec(I[0]), pi = readVec(I[1]);
      if (!P || !pi || vzero(pi.slice(0, 3))) { info.textContent = u("bad"); return; }
      var n = pi.slice(0, 3), D = pi[3], num = vdot(n, P).add(D), nn = vdot(n, n), lam = F0.sub(num).div(nn);
      var Q = vadd(P, vscale(n, lam)), S = vadd(P, vscale(n, lam.mul(new Fr(2)))), h = "";
      if (num.zero()) h = "<p>" + u("onPlane") + "</p>";
      else {
        h += "<p>1) " + tex("r:\\ (x,y,z)=" + vtex(P) + "+\\lambda" + vtex(n)) + "</p>";
        h += "<p>2) " + tex(n.map(function (a, i) { return ftex(a) + "(" + P[i].tex() + (a.n < 0 ? "" : "+") + a.tex() + "\\lambda)"; }).join("+") + (D.n < 0 ? "" : "+") + D.tex() + "=0\\Rightarrow\\lambda=" + lam.tex()) + "</p>";
        h += "<p>" + u("proj") + ": " + tex("\\color{" + COL.red + "}{Q" + vtex(Q) + "}") + " · " + u("sym") + ": " + tex("\\color{" + COL.green + "}{P'" + vtex(S) + "}") + "</p>";
        var q = sqrtFr(new Fr(num.n * num.n, num.d * num.d).div(nn));
        h += "<p>" + u("dist") + ": " + tex("d(P,\\pi)=\\frac{|" + num.tex() + "|}{\\sqrt{" + nn.tex() + "}}=" + q.tex + (q.exact ? "" : "\\approx " + tdec(q.v, 3))) + "</p>";
      }
      info.innerHTML = h; cur = { P: P, Q: Q, S: S, n: n, D: D }; draw();
    }
    I.forEach(function (g) { g.forEach(function (x) { x.addEventListener("input", render); }); });
    onLang(render);
  }

  /* ---------- giny: bisecció (teorema de Bolzano) ---------- */
  function wBolz() {
    var w = $("#w-bolz"); if (!w) return;
    function f(x) { return x + Math.sin(x) - 2; }
    var el = $('[data-role="plot"]', w), info = $(".info", w), bn = $('[data-role="next"]', w), br = $('[data-role="reset"]', w), hist;
    function reset() { hist = [[0, Math.PI]]; render(); }
    function render() {
      var I = hist[hist.length - 1], a = I[0], b = I[1], m = (a + b) / 2;
      plot(el, { x: [-0.3, 3.5], y: [-2.4, 1.8], ticks: 1, items: [
        { poly: [[a, -2.4], [b, -2.4], [b, 1.8], [a, 1.8]], fill: "#9bba58", op: 0.22 }, { fn: f, stroke: COL.fn, w: 2.2 },
        { pt: [a, f(a)], fill: COL.red, r: 3.4 }, { pt: [b, f(b)], fill: COL.green, r: 3.4 }, { seg: [[m, 0], [m, f(m)]], stroke: "#888", dash: true, w: 1 },
        { txt: [b - a < 0.3 ? m : a, -2.25], s: b - a < 0.3 ? "[a, b]" : "a", cls: "lb", anchor: "middle" }].concat(b - a < 0.3 ? [] : [{ txt: [b, -2.25], s: "b", cls: "lb", anchor: "middle" }]) });
      var rows = hist.map(function (I, k) { var mm = (I[0] + I[1]) / 2; return "<tr" + (k === hist.length - 1 ? ' class="best"' : "") + "><td>" + k + "</td><td>[" + dec(I[0], 4) + ", " + dec(I[1], 4) + "]</td><td>f(" + dec(mm, 4) + ") = " + dec(f(mm), 4) + "</td></tr>"; });
      info.innerHTML = "<div>" + tex("f(x)=x+\\sin x-2") + " · " + u("sign") + " " + tex("[a,b]") + "</div><table class=\"vtab\"><tbody>" + rows.slice(-6).join("") + "</tbody></table>" +
        (b - a < 1e-3 ? "<p><strong>" + u("root") + " ≈ " + dec(m, 4) + "</strong></p>" : "");
      bn.textContent = b - a < 1e-3 ? u("bdone") : u("bnext") + " →"; bn.disabled = b - a < 1e-3;
    }
    bn.addEventListener("click", function () { var I = hist[hist.length - 1], m = (I[0] + I[1]) / 2; hist.push(f(I[0]) * f(m) <= 0 ? [I[0], m] : [m, I[1]]); render(); });
    br.addEventListener("click", reset);
    hist = [[0, Math.PI]]; onLang(render);
  }

  /* ---------- giny: comprovació numèrica de L'Hôpital ---------- */
  function wLhop() {
    var w = $("#w-lhop"); if (!w) return;
    var rng = $("input", w), out = $("output", w), info = $(".info", w);
    function render() {
      var n = +rng.value, x = Math.pow(10, -n); out.textContent = n;
      info.innerHTML = tex("x=10^{-" + n + "}:\\quad \\sin x\\cdot\\ln x\\approx " + tdec(Math.sin(x) * Math.log(x), 8) + "\\qquad x^{\\sin x}\\approx " + tdec(Math.pow(x, Math.sin(x)), 8));
    }
    rng.addEventListener("input", render); onLang(render);
  }

