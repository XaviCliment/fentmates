/*@@CORE@@*/
  /* =====================================================================
     Unitat 4: problemes mètrics. Tots els càlculs es fan amb fraccions exactes (F, Fr, vdot…, del nucli de la unitat 3) i
     les distàncies i els angles es guarden al quadrat (d², cos²) com a fraccions, de manera que sempre es poden escriure
     exactes amb arrels simplificades.
     ===================================================================== */
  function kv(rows) { return '<div class="kv">' + rows.map(function (r) { return r[0] === "" ? '<span class="full">' + r[1] + "</span>" : "<span>" + r[0] + "</span><span>" + r[1] + "</span>"; }).join("") + "</div>"; }
  function cdot(c) { return '<i class="tag-c" style="background:' + c + '"></i>'; }
  function mt(s) { return s.replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }); }
  function isSqI(n) { n = Math.abs(n); var r = Math.round(Math.sqrt(n)); return r * r === n; }
  function exact(f) { f = F(f); return isSqI(f.n) && isSqI(f.d); }
  function sqrtFrT(f) { // √f simplificat i racionalitzat (f ≥ 0 fracció)
    f = F(f); if (f.n === 0) return "0";
    var s = surd(f.n * f.d), c = Fr(s.a, f.d);
    if (s.b === 1) return fT(c);
    var top = (c.n === 1 ? "" : c.n) + "\\sqrt{" + s.b + "}";
    return c.d === 1 ? top : "\\frac{" + top + "}{" + c.d + "}";
  }
  function distT(f2) { f2 = F(f2); return sqrtFrT(f2) + (exact(f2) ? "" : "\\approx " + dT(Math.sqrt(fVal(f2)))) + "\\ \\text{u}"; }
  function rtF(S) { S = F(S); return S.d === 1 && isSqI(S.n) ? String(Math.round(Math.sqrt(S.n))) : "\\sqrt{" + fT(S) + "}"; }
  function degS(a) {
    if (Math.abs(a - Math.round(a)) < 1e-7) return Math.round(a) + "^\\circ";
    return dmsT(a) + "\\approx " + degT(a);
  }
  function abs(f) { f = F(f); return Fr(Math.abs(f.n), f.d); }
  function nOf(c) { return c.slice(0, 3); }
  function planeT(c) { return poly([[c[0], "x"], [c[1], "y"], [c[2], "z"], [c[3], ""]]) + "=0"; }
  function evalT(c, P) { var s = []; for (var i = 0; i < 3; i++) if (F(c[i]).n) s.push(fP(c[i]) + "\\cdot" + fP(P[i])); if (F(c[3]).n) s.push(fP(c[3])); return s.join("+") || "0"; }
  function sqsT(v) { return v.map(function (x) { return fP(x) + "^2"; }).join("+"); }
  function sym2(Q, P) { return vsub(vmul(Q, 2), P); } // simètric de P respecte de Q
  function lineT(P, d, t) { return "(x,y,z)=" + vT(P) + "+" + (t || "\\lambda") + vT(d); }
  function primDir(v) { var w = prim(v); if ((w[0] || w[1] || w[2]) < 0) w = w.map(function (x) { return -x; }); return w; }

  /* ---------- angles ---------- */
  function angLL(d, e) { var p = vdot(d, e), c2 = fDiv(fMul(p, p), fMul(vdot(d, d), vdot(e, e))); return { p: p, c2: c2, a: deg(Math.acos(Math.min(1, Math.sqrt(fVal(c2))))) }; }
  // kind 0: dues rectes (cos amb els directors); 1: recta i pla (sin amb d i n); 2: dos plans (cos amb els normals)
  function angRows(d, e, kind) {
    var A = angLL(d, e), L1 = ["\\vec d_r", "\\vec d", "\\vec n_1"][kind], L2 = ["\\vec d_s", "\\vec n", "\\vec n_2"][kind], fn = kind === 1 ? "\\sin" : "\\cos";
    var a = kind === 1 ? 90 - A.a : A.a, rows = [[tex(L1 + "\\cdot" + L2), tex(dotT(d, e))],
      [t3("Angle", "Ángulo", "Angle"), tex(fn + "\\alpha=\\dfrac{|" + L1 + "\\cdot" + L2 + "|}{|" + L1 + "|\\,|" + L2 + "|}=\\dfrac{" + fT(abs(A.p)) + "}{" + rtF(vdot(d, d)) + "\\cdot" + rtF(vdot(e, e)) + "}=" + sqrtFrT(A.c2))],
      ["", tex("\\alpha=" + (kind === 1 ? "\\arcsin " : "\\arccos ") + sqrtFrT(A.c2) + "=" + degS(a))]];
    var z = F(A.p).n === 0, one = F(A.c2).n === F(A.c2).d, note = "";
    if (kind === 0) note = z ? t3("Les rectes són perpendiculars (es tallen o s'encreuen).", "Las rectas son perpendiculares (se cortan o se cruzan).", "The lines are perpendicular (they meet or are skew).") : one ? t3("Directors proporcionals: rectes paral·leles o coincidents.", "Directores proporcionales: rectas paralelas o coincidentes.", "Proportional directions: parallel or coincident lines.") : "";
    if (kind === 1) note = z ? t3("La recta és paral·lela al pla o hi està continguda: l'angle és 0°.", "La recta es paralela al plano o está contenida en él: el ángulo es 0°.", "The line is parallel to the plane or lies in it: the angle is 0°.") : one ? t3("La recta és perpendicular al pla.", "La recta es perpendicular al plano.", "The line is perpendicular to the plane.") : "";
    if (kind === 2) note = z ? t3("Els plans són perpendiculars.", "Los planos son perpendiculares.", "The planes are perpendicular.") : one ? t3("Normals proporcionals: plans paral·lels o coincidents.", "Normales proporcionales: planos paralelos o coincidentes.", "Proportional normals: parallel or coincident planes.") : "";
    if (note) rows.push(["", "<strong>" + note + "</strong>"]);
    return { rows: rows, a: a };
  }

  /* ---------- distàncies i projeccions ---------- */
  function dPPl(P, c) { var n = nOf(c), v = evalPlane(c, P), S = vdot(n, n), t = fDiv(fMul(-1, v), S); return { v: v, S: S, d2: fDiv(fMul(v, v), S), t: t, Q: vadd(P, vmul(n, t)) }; }
  function dPL(P, A, d) { var AP = vsub(P, A), cr = vcross(AP, d), dd = vdot(d, d), t = fDiv(vdot(AP, d), dd); return { AP: AP, cr: cr, dd: dd, d2: fDiv(vdot(cr, cr), dd), t: t, Q: vadd(A, vmul(d, t)) }; }
  function LL(P, d, Q, e) {
    var w = vsub(Q, P), r1 = rank([d, e]), r2 = rank([d, e, w]), o = { w: w, pos: r1 === 1 ? (r2 === 1 ? 0 : 1) : (r2 === 2 ? 2 : 3), d2: Fr(0) };
    if (o.pos === 1) { var D = dPL(Q, P, d); o.D = D; o.d2 = D.d2; o.X = D.Q; o.Y = Q; }
    if (o.pos >= 2) {
      var dd = vdot(d, d), ee = vdot(e, e), de = vdot(d, e), wd = vdot(w, d), we = vdot(w, e), det = fSub(fMul(de, de), fMul(dd, ee));
      o.la = fDiv(fAdd(fMul(-1, fMul(wd, ee)), fMul(de, we)), det); o.mu = fDiv(fSub(fMul(dd, we), fMul(de, wd)), det);
      o.X = vadd(P, vmul(d, o.la)); o.Y = vadd(Q, vmul(e, o.mu));
      o.n = vcross(d, e); o.m = det3(w, d, e); o.d2 = fDiv(fMul(o.m, o.m), vdot(o.n, o.n));
    }
    return o;
  }
  function LPl(P, d, c) {
    var n = nOf(c), nd = vdot(n, d), v = evalPlane(c, P), o = { nd: nd, v: v, pos: F(nd).n ? 0 : F(v).n ? 1 : 2 };
    if (o.pos === 0) { o.t = fDiv(fMul(-1, v), nd); o.X = vadd(P, vmul(d, o.t)); }
    return o;
  }
  function PlPl(c1, c2) {
    var n1 = nOf(c1), n2 = nOf(c2);
    if (!vzero(vcross(n1, n2))) return { pos: 2 };
    var j = [0, 1, 2].filter(function (i) { return F(n2[i]).n !== 0; })[0], k = fDiv(n2[j], n1[j]), D2 = fDiv(c2[3], k), diff = fSub(c1[3], D2);
    return { pos: F(diff).n ? 1 : 0, k: k, D2: D2, diff: diff, d2: fDiv(fMul(diff, diff), vdot(n1, n1)) };
  }
  function symLinePl(A, d, c) { // simètrica de la recta (A, d) respecte del pla c
    var lp = LPl(A, d, c);
    if (lp.pos === 2) return { pos: 2, P: A, d: primDir(d) };
    if (lp.pos === 1) { var A1 = sym2(dPPl(A, c).Q, A); return { pos: 1, P: A1, d: primDir(d), A1: A1 }; }
    var B = vzero(vsub(A, lp.X)) ? vadd(A, d) : A, B1 = sym2(dPPl(B, c).Q, B);
    return { pos: 0, X: lp.X, B: B, B1: B1, P: lp.X, d: primDir(vsub(B1, lp.X)) };
  }
  function med(A, B) { var n = vsub(B, A), M = vmul(vadd(A, B), Fr(1, 2)); return { n: n, M: M, pl: planeEq(n, fMul(-1, vdot(n, M))) }; }
  function bis(c1, c2) {
    var S1 = vdot(nOf(c1), nOf(c1)), S2 = vdot(nOf(c2), nOf(c2)), q2 = fDiv(S2, S1), o = { S1: S1, S2: S2 };
    if (exact(q2)) {
      var q = Fr(Math.round(Math.sqrt(q2.n)), Math.round(Math.sqrt(q2.d)));
      o.ex = [1, -1].map(function (s) { var c = [0, 1, 2, 3].map(function (i) { return fSub(fMul(q, c1[i]), fMul(s, c2[i])); }); return vzero(c.slice(0, 3)) ? null : planeEq(c.slice(0, 3), c[3]); });
    }
    var r1 = Math.sqrt(fVal(S1)), r2 = Math.sqrt(fVal(S2));
    o.num = [1, -1].map(function (s) { return [0, 1, 2, 3].map(function (i) { return fVal(c1[i]) * r2 - s * fVal(c2[i]) * r1; }); });
    return o;
  }
  function tetra(A, B, C, D) {
    var u = vsub(B, A), v = vsub(C, A), w = vsub(D, A), cr = vcross(u, v), m = det3(u, v, w);
    return { u: u, v: v, w: w, cr: cr, m: m, area2: fDiv(vdot(cr, cr), 4), V: fDiv(abs(m), 6), h2: vzero(cr) ? null : fDiv(fMul(m, m), vdot(cr, cr)) };
  }

  /* ---------- files d'informació reutilitzables (ginys i laboratori) ---------- */
  var POSLL = function () { return [t3("Coincidents", "Coincidentes", "Coincident"), t3("Paral·leles", "Paralelas", "Parallel"), t3("Secants", "Secantes", "Intersecting"), t3("S'encreuen", "Se cruzan", "Skew")]; };
  function rowsPPl(P, c, name) {
    var o = dPPl(P, c), nm = name || "\\pi";
    var rows = [[tex("d(P," + nm + ")"), tex("\\dfrac{|" + evalT(c, P) + "|}{\\sqrt{" + sqsT(nOf(c)) + "}}=\\dfrac{" + fT(abs(o.v)) + "}{" + rtF(o.S) + "}=" + distT(o.d2))]];
    if (F(o.v).n === 0) rows.push(["", "<strong>" + t3("El punt és del pla: la distància és 0.", "El punto está en el plano: la distancia es 0.", "The point lies on the plane: the distance is 0.") + "</strong>"]);
    else {
      rows.push([t3("Recta per P ⊥ al pla", "Recta por P ⊥ al plano", "Line through P ⊥ plane"), tex(lineT(P, nOf(c), "t"))]);
      rows.push([t3("Tall amb el pla", "Corte con el plano", "Meets the plane"), tex(poly([[o.v, ""], [o.S, "t"]]) + "=0\\Rightarrow t=" + fT(o.t))]);
      rows.push([cdot(COL.p) + t3("Projecció", "Proyección", "Projection"), tex("Q=" + vT(o.Q))]);
    }
    return { rows: rows, o: o };
  }
  function rowsPL(P, A, d) {
    var o = dPL(P, A, d), rows = [[tex("\\overrightarrow{AP}"), tex(vT(o.AP))], [tex("\\overrightarrow{AP}\\times\\vec d"), tex(vT(o.cr))],
      [tex("d(P,r)"), tex("\\dfrac{|\\overrightarrow{AP}\\times\\vec d|}{|\\vec d|}=\\dfrac{" + rtF(vdot(o.cr, o.cr)) + "}{" + rtF(o.dd) + "}=" + distT(o.d2))]];
    if (vzero(o.cr)) rows.push(["", "<strong>" + t3("El punt és de la recta: la distància és 0.", "El punto está en la recta: la distancia es 0.", "The point lies on the line: the distance is 0.") + "</strong>"]);
    else {
      rows.push([t3("Peu de la perpendicular", "Pie de la perpendicular", "Foot of the perpendicular"), tex("\\overrightarrow{QP}\\cdot\\vec d=0\\Rightarrow\\lambda=\\dfrac{\\overrightarrow{AP}\\cdot\\vec d}{|\\vec d|^2}=" + fT(o.t))]);
      rows.push([cdot(COL.p) + t3("Projecció", "Proyección", "Projection"), tex("Q=" + vT(o.Q))]);
    }
    return { rows: rows, o: o };
  }
  function rowsLL(P, d, Q, e) {
    var o = LL(P, d, Q, e), rows = [[t3("Posició", "Posición", "Position"), "<strong>" + POSLL()[o.pos] + "</strong>"]];
    if (o.pos === 0) rows.push([tex("d(r,s)"), tex("0")]);
    if (o.pos === 1) {
      rows.push([tex("d(r,s)=d(Q,r)"), tex("\\dfrac{|\\overrightarrow{PQ}\\times\\vec d_r|}{|\\vec d_r|}=\\dfrac{" + rtF(vdot(o.D.cr, o.D.cr)) + "}{" + rtF(o.D.dd) + "}=" + distT(o.d2))]);
      rows.push([cdot(COL.p) + t3("Peu des de Q", "Pie desde Q", "Foot from Q"), tex(vT(o.X))]);
    }
    if (o.pos >= 2) {
      rows.push([tex("[\\overrightarrow{PQ},\\vec d_r,\\vec d_s]"), tex(detT(o.w, d, e))]);
      if (o.pos === 3) rows.push([tex("d(r,s)"), tex("\\dfrac{|[\\overrightarrow{PQ},\\vec d_r,\\vec d_s]|}{|\\vec d_r\\times\\vec d_s|}=\\dfrac{" + fT(abs(o.m)) + "}{|" + vT(o.n) + "|}=\\dfrac{" + fT(abs(o.m)) + "}{" + rtF(vdot(o.n, o.n)) + "}=" + distT(o.d2))]);
      else rows.push([tex("d(r,s)"), tex("0") + " " + t3("(es tallen)", "(se cortan)", "(they meet)")]);
      rows.push([t3("Perpendicular comuna", "Perpendicular común", "Common perpendicular"), tex("\\overrightarrow{XY}\\perp\\vec d_r,\\ \\overrightarrow{XY}\\perp\\vec d_s\\Rightarrow\\lambda=" + fT(o.la) + ",\\ \\mu=" + fT(o.mu))]);
      rows.push([cdot(COL.p) + t3("Peus", "Pies", "Feet"), tex("X=" + vT(o.X) + (o.pos === 3 ? ",\\ \\ Y=" + vT(o.Y) : "\\ " + "(=Y)"))]);
      if (o.pos === 3) rows.push([t3("Recta perpendicular comuna", "Recta perpendicular común", "Common perpendicular line"), tex(lineT(o.X, primDir(o.n), "t"))]);
    }
    return { rows: rows, o: o };
  }
  function rowsLPl(P, d, c, nm) {
    nm = nm || "\\pi";
    var o = LPl(P, d, c), rows = [[tex("\\vec n\\cdot\\vec d"), tex(dotT(nOf(c), d))]];
    rows.push([t3("Posició", "Posición", "Position"), "<strong>" + [t3("Secants", "Secantes", "Intersecting"), t3("Paral·lels", "Paralelos", "Parallel"), t3("La recta és continguda en el pla", "La recta está contenida en el plano", "The line lies in the plane")][o.pos] + "</strong>"]);
    if (o.pos === 0) rows.push([cdot(COL.p) + t3("Punt de tall", "Punto de corte", "Intersection"), tex("\\lambda=" + fT(o.t) + "\\Rightarrow " + vT(o.X)) + " · " + tex("d(r," + nm + ")=0")]);
    if (o.pos === 1) { var D = dPPl(P, c); rows.push([tex("d(r," + nm + ")=d(P," + nm + ")"), tex("\\dfrac{|" + evalT(c, P) + "|}{" + rtF(D.S) + "}=" + distT(D.d2))]); }
    if (o.pos === 2) rows.push([tex("d(r," + nm + ")"), tex("0")]);
    return { rows: rows, o: o };
  }
  function rowsPlPl(c1, c2) {
    var o = PlPl(c1, c2), rows = [];
    if (o.pos === 2) { rows.push([t3("Posició", "Posición", "Position"), "<strong>" + t3("Secants", "Secantes", "Intersecting") + "</strong> · " + tex("d(\\pi_1,\\pi_2)=0")]); return { rows: rows, o: o }; }
    rows.push([t3("Posició", "Posición", "Position"), "<strong>" + (o.pos ? t3("Paral·lels", "Paralelos", "Parallel") : t3("Coincidents", "Coincidentes", "Coincident")) + "</strong>"]);
    if (F(o.k).n !== F(o.k).d) rows.push([t3("Mateix normal", "Mismo normal", "Same normal"), tex("\\pi_2:" + planeT(nOf(c1).concat([o.D2])))]);
    rows.push([tex("d(\\pi_1,\\pi_2)"), tex("\\dfrac{|D_1-D_2|}{|\\vec n|}=\\dfrac{|" + fT(c1[3]) + "-" + fP(o.D2) + "|}{" + rtF(vdot(nOf(c1), nOf(c1))) + "}=" + distT(o.d2))]);
    return { rows: rows, o: o };
  }

  /* ---------- muntatge dels ginys ---------- */
  // ginys amb diversos modes: cada mode té les seues caselles (es tornen a crear en canviar de mode)
  function setupModes(id, labels, modes, draw) {
    var w = document.getElementById(id); if (!w) return null;
    var fig = $(w, "fig"), box = $(w, "in"), g = { w: w, info: w.querySelector(".info"), mode: 0 };
    g.redraw = s3mount(fig, function () { return g.scene || { items: [] }; });
    function build(i) { g.mode = i; box.innerHTML = ""; g.f = fields(box, modes[i](), function () { draw(); }); draw(); }
    var bs = presetBtns($(w, "modes"), labels, build); bs[0].classList.add("on");
    g.f = fields(box, modes[0](), function () { draw(); });
    return g;
  }
  function noPlane(c) { return vzero(nOf(c)); }
  var MSG = {
    pl: function () { return t3("Si A = B = C = 0, no és un pla.", "Si A = B = C = 0, no es un plano.", "If A = B = C = 0 it is not a plane."); },
    d: function () { return t3("Un vector director no pot ser nul.", "Un vector director no puede ser nulo.", "A direction vector cannot be zero."); }
  };
  function segP(a, b, col, dash) { return { seg: [vnum(a), vnum(b)], stroke: col || COL.p, w: 2.2, dash: dash === undefined ? "5 4" : dash }; }
  function lineI(P, d, col, lab) { return { line: [vnum(P), vnum(d)], stroke: col, w: 2.4, label: lab }; }

  /* ---------- 4.1 angle entre dues rectes ---------- */
  function wArr() {
    var g = setupW("w-arr", [{ k: "P", vals: [1, 0, -1], fmt: ptF("P") }, { k: "dr", vals: [1, 2, 2], fmt: veF("\\vec d_r") }, { k: "Q", vals: [0, 1, 1], fmt: ptF("Q") }, { k: "ds", vals: [2, -1, 2], fmt: veF("\\vec d_s") }], draw); if (!g) return;
    function draw() {
      var P = g.f.v.P, Q = g.f.v.Q, d = g.f.v.dr, e = g.f.v.ds, items = [dot3(P, "P", COL.r), dot3(Q, "Q", COL.s)];
      if (vzero(d) || vzero(e)) { bad(g, MSG.d()); scene(g, items, [P, Q]); return; }
      var A = angRows(d, e, 0), o = LL(P, d, Q, e), rows = A.rows.concat([[t3("Posició", "Posición", "Position"), POSLL()[o.pos]]]);
      items.unshift(lineI(P, d, COL.r, "r"), lineI(Q, e, COL.s, "s"), arrow3(P, d, COL.r), arrow3(Q, e, COL.s));
      if (o.pos === 2) items.push(dot3(vnum(o.X), "X", COL.p));
      scene(g, items, [P, Q]);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 4.2 angle entre recta i pla i entre dos plans ---------- */
  function wArp() {
    var g = setupW("w-arp", [{ k: "P", vals: [1, 0, 2], fmt: ptF("P") }, { k: "d", vals: [2, 1, 2], fmt: veF("\\vec d") }, { k: "p1", vals: [1, 2, 2, -3], fmt: plF("\\pi_1") }, { k: "p2", vals: [1, 1, 0, 0], fmt: plF("\\pi_2") }], draw); if (!g) return;
    function draw() {
      var P = g.f.v.P, d = g.f.v.d, c1 = g.f.v.p1, c2 = g.f.v.p2, items = [dot3(P, "P", COL.r)];
      if (vzero(d)) { bad(g, MSG.d()); scene(g, items, [P]); return; }
      if (noPlane(c1) || noPlane(c2)) { bad(g, MSG.pl()); scene(g, items, [P]); return; }
      var A = angRows(d, nOf(c1), 1), B = angRows(nOf(c1), nOf(c2), 2);
      var rows = [["", "<b>" + t3("Recta ", "Recta ", "Line ") + tex("r") + t3(" i pla ", " y plano ", " and plane ") + tex("\\pi_1") + "</b>"]].concat(A.rows,
        [["", "<b>" + t3("Plans ", "Planos ", "Planes ") + tex("\\pi_1") + t3(" i ", " y ", " and ") + tex("\\pi_2") + "</b>"]], B.rows);
      items.unshift(pl(0, nOf(c1), c1[3]), pl(2, nOf(c2), c2[3]), lineI(P, d, COL.s, "r"));
      var lp = LPl(P, d, c1); if (lp.pos === 0) items.push(dot3(vnum(lp.X), "X", COL.p));
      scene(g, items, [P]);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 4.3 distància d'un punt a un pla ---------- */
  function wDpp() {
    var g = setupW("w-dpp", [{ k: "P", vals: [5, 1, 6], fmt: ptF("P") }, { k: "pi", vals: [2, -1, 2, -3], fmt: plF("\\pi") }], draw); if (!g) return;
    function draw() {
      var P = g.f.v.P, c = g.f.v.pi, items = [dot3(P, "P", COL.r)];
      if (noPlane(c)) { bad(g, MSG.pl()); scene(g, items, [P]); return; }
      var R = rowsPPl(P, c);
      items.unshift(pl(2, nOf(c), c[3]));
      if (F(R.o.v).n) { items.push(segP(P, R.o.Q), dot3(vnum(R.o.Q), "Q", COL.p)); R.rows.push([t3("Comprovació", "Comprobación", "Check"), tex("|\\overrightarrow{PQ}|=" + sqrtFrT(vdot(vsub(R.o.Q, P), vsub(R.o.Q, P))))]); }
      scene(g, items, [P, vnum(R.o.Q)]);
      g.info.innerHTML = kv(R.rows);
    }
    onLang(draw);
  }

  /* ---------- 4.4 distància d'un punt a una recta ---------- */
  function wDpr() {
    var g = setupW("w-dpr", [{ k: "P", vals: [6, 4, 4], fmt: ptF("P") }, { k: "A", vals: [2, 1, 0], fmt: ptF("A") }, { k: "d", vals: [1, 2, 2], fmt: veF("\\vec d") }], draw); if (!g) return;
    function draw() {
      var P = g.f.v.P, A = g.f.v.A, d = g.f.v.d, items = [dot3(P, "P", COL.s), dot3(A, "A", COL.r)];
      if (vzero(d)) { bad(g, MSG.d()); scene(g, items, [P, A]); return; }
      var R = rowsPL(P, A, d);
      items.unshift(lineI(A, d, COL.r, "r"), arrow3(A, d, COL.r));
      if (!vzero(R.o.cr)) items.push(segP(P, R.o.Q), dot3(vnum(R.o.Q), "Q", COL.p));
      scene(g, items, [P, A, vnum(R.o.Q)]);
      g.info.innerHTML = kv(R.rows);
    }
    onLang(draw);
  }

  /* ---------- 4.5 distància entre dues rectes ---------- */
  function wDrr() {
    var g = setupW("w-drr", [{ k: "P", vals: [2, -1, 3], fmt: ptF("P") }, { k: "dr", vals: [1, -2, 2], fmt: veF("\\vec d_r") }, { k: "Q", vals: [1, 4, 4], fmt: ptF("Q") }, { k: "ds", vals: [2, -1, -2], fmt: veF("\\vec d_s") }], draw); if (!g) return;
    var PR = [{ P: [2, -1, 3], dr: [1, -2, 2], Q: [1, 4, 4], ds: [2, -1, -2] }, { P: [1, 0, -1], dr: [1, 2, 2], Q: [3, 1, 0], ds: [2, 4, 4] }, { P: [1, 0, 0], dr: [1, 1, 0], Q: [2, 1, 3], ds: [0, 0, 1] }];
    presetBtns($(g.w, "presets"), function () { return [t3("S'encreuen", "Se cruzan", "Skew"), t3("Paral·leles", "Paralelas", "Parallel"), t3("Secants", "Secantes", "Intersecting")]; }, function (i) { g.f.set(PR[i]); });
    function draw() {
      var P = g.f.v.P, Q = g.f.v.Q, d = g.f.v.dr, e = g.f.v.ds, items = [dot3(P, "P", COL.r), dot3(Q, "Q", COL.s)];
      if (vzero(d) || vzero(e)) { bad(g, MSG.d()); scene(g, items, [P, Q]); return; }
      var R = rowsLL(P, d, Q, e), o = R.o, pts = [P, Q];
      items.unshift(lineI(P, d, COL.r, "r"), lineI(Q, e, COL.s, "s"));
      if (o.X) { items.push(dot3(vnum(o.X), "X", COL.p)); pts.push(vnum(o.X)); }
      if (o.pos === 3 || o.pos === 1) { items.push(segP(o.X, o.Y, COL.p, false), dot3(vnum(o.Y), "Y", COL.p)); pts.push(vnum(o.Y)); }
      scene(g, items, pts);
      g.info.innerHTML = kv(R.rows);
    }
    onLang(draw);
  }

  /* ---------- 4.6 distància entre recta i pla i entre dos plans ---------- */
  function wDpl() {
    var g = setupW("w-dpl", [{ k: "P", vals: [0, 1, -1], fmt: ptF("P") }, { k: "d", vals: [3, -1, 2], fmt: veF("\\vec d") }, { k: "p1", vals: [1, 1, -1, -3], fmt: plF("\\pi_1") }, { k: "p2", vals: [2, 2, -2, 5], fmt: plF("\\pi_2") }], draw); if (!g) return;
    function draw() {
      var P = g.f.v.P, d = g.f.v.d, c1 = g.f.v.p1, c2 = g.f.v.p2, items = [dot3(P, "P", COL.r)];
      if (vzero(d)) { bad(g, MSG.d()); scene(g, items, [P]); return; }
      if (noPlane(c1) || noPlane(c2)) { bad(g, MSG.pl()); scene(g, items, [P]); return; }
      var A = rowsLPl(P, d, c1, "\\pi_1"), B = rowsPlPl(c1, c2);
      var rows = [["", "<b>" + t3("Recta ", "Recta ", "Line ") + tex("r") + t3(" i pla ", " y plano ", " and plane ") + tex("\\pi_1") + "</b>"]].concat(A.rows,
        [["", "<b>" + t3("Plans ", "Planos ", "Planes ") + tex("\\pi_1") + t3(" i ", " y ", " and ") + tex("\\pi_2") + "</b>"]], B.rows);
      items.unshift(pl(0, nOf(c1), c1[3]), pl(2, nOf(c2), c2[3]), lineI(P, d, COL.s, "r"));
      if (A.o.pos === 1) { var D = dPPl(P, c1); items.push(segP(P, D.Q), dot3(vnum(D.Q), "Q", COL.p)); }
      if (A.o.pos === 0) items.push(dot3(vnum(A.o.X), "X", COL.p));
      scene(g, items, [P]);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 4.7 simètric respecte d'una recta ---------- */
  function rowsSymL(P, A, d) {
    var o = dPL(P, A, d), P1 = sym2(o.Q, P), c = planeEq(d, fMul(-1, vdot(d, P)));
    var rows = [[t3("Pla per P ⊥ a r", "Plano por P ⊥ a r", "Plane through P ⊥ r"), tex("\\pi:" + c.t)],
      [t3("Tall amb r", "Corte con r", "Meets r"), tex("\\lambda=" + fT(o.t) + "\\Rightarrow M=" + vT(o.Q))],
      [cdot(COL.k) + t3("Simètric", "Simétrico", "Reflection"), tex("P'=2M-P=" + vT(P1))]];
    return { rows: rows, o: o, P1: P1 };
  }
  function wSr() {
    var g = setupW("w-sr", [{ k: "P", vals: [4, -3, 0], fmt: ptF("P") }, { k: "A", vals: [-2, 0, 1], fmt: ptF("A") }, { k: "d", vals: [0, -1, -1], fmt: veF("\\vec d") }], draw); if (!g) return;
    function draw() {
      var P = g.f.v.P, A = g.f.v.A, d = g.f.v.d, items = [dot3(P, "P", COL.s)];
      if (vzero(d)) { bad(g, MSG.d()); scene(g, items, [P, A]); return; }
      var R = rowsSymL(P, A, d);
      items.unshift(lineI(A, d, COL.r, "r"));
      items.push(segP(P, R.P1, COL.p), dot3(vnum(R.o.Q), "M", COL.p), dot3(vnum(R.P1), "P'", COL.k));
      scene(g, items, [P, A, vnum(R.P1)]);
      g.info.innerHTML = kv(R.rows);
    }
    onLang(draw);
  }

  /* ---------- 4.8 simètric respecte d'un pla (d'un punt i d'una recta) ---------- */
  function rowsSymP(P, c) {
    var o = dPPl(P, c), P1 = sym2(o.Q, P);
    return { rows: [[t3("Recta per P ⊥ a π", "Recta por P ⊥ a π", "Line through P ⊥ π"), tex(lineT(P, nOf(c), "t"))],
      [t3("Tall amb π", "Corte con π", "Meets π"), tex(poly([[o.v, ""], [o.S, "t"]]) + "=0\\Rightarrow t=" + fT(o.t) + "\\Rightarrow M=" + vT(o.Q))],
      [cdot(COL.k) + t3("Simètric", "Simétrico", "Reflection"), tex("P'=2M-P=" + vT(P1))]], o: o, P1: P1 };
  }
  function rowsSymLine(A, d, c) {
    var s = symLinePl(A, d, c), rows = [];
    if (s.pos === 2) rows.push(["", "<strong>" + t3("La recta és continguda en el pla: la simètrica és ella mateixa.", "La recta está contenida en el plano: la simétrica es ella misma.", "The line lies in the plane: its reflection is itself.") + "</strong>"]);
    if (s.pos === 1) {
      rows.push([t3("Posició", "Posición", "Position"), t3("paral·lela al pla: la simètrica té el mateix director", "paralela al plano: la simétrica tiene el mismo director", "parallel to the plane: the reflection has the same direction")]);
      rows.push([t3("Simètric de A", "Simétrico de A", "Reflection of A"), tex("A'=" + vT(s.A1))]);
    }
    if (s.pos === 0) {
      rows.push([t3("Punt de tall (fix)", "Punto de corte (fijo)", "Intersection (fixed)"), tex("X=" + vT(s.X))]);
      rows.push([t3("Un altre punt", "Otro punto", "Another point"), tex("B=" + vT(s.B) + "\\ \\to\\ B'=" + vT(s.B1))]);
    }
    rows.push([cdot(COL.k) + t3("Recta simètrica", "Recta simétrica", "Reflected line"), tex("r':" + lineT(s.P, s.d))]);
    return { rows: rows, s: s };
  }
  function wSp() {
    var g = setupW("w-sp", [{ k: "P", vals: [3, 4, 2], fmt: ptF("P") }, { k: "pi", vals: [1, 1, 1, -6], fmt: plF("\\pi") }, { k: "A", vals: [2, 1, 0], fmt: ptF("A") }, { k: "d", vals: [1, 0, 0], fmt: veF("\\vec d") }], draw); if (!g) return;
    function draw() {
      var P = g.f.v.P, c = g.f.v.pi, A = g.f.v.A, d = g.f.v.d, items = [dot3(P, "P", COL.s)];
      if (noPlane(c)) { bad(g, MSG.pl()); scene(g, items, [P]); return; }
      if (vzero(d)) { bad(g, MSG.d()); scene(g, items, [P]); return; }
      var R = rowsSymP(P, c), S = rowsSymLine(A, d, c);
      var rows = [["", "<b>" + t3("Simètric del punt ", "Simétrico del punto ", "Reflection of the point ") + tex("P") + "</b>"]].concat(R.rows, [["", "<b>" + t3("Simètrica de la recta ", "Simétrica de la recta ", "Reflection of the line ") + tex("r") + "</b>"]], S.rows);
      items.unshift(pl(2, nOf(c), c[3]), lineI(A, d, COL.r, "r"), lineI(S.s.P, S.s.d, COL.k, "r'"));
      items.push(segP(P, R.P1, COL.p), dot3(vnum(R.o.Q), "M", COL.p), dot3(vnum(R.P1), "P'", COL.k));
      if (S.s.pos === 0) items.push(dot3(vnum(S.s.X), "X", COL.p));
      scene(g, items, [P, vnum(R.P1), A]);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 4.9 àrees i volums ---------- */
  function wVol() {
    var g = setupW("w-vol", [{ k: "A", vals: [1, 1, 1], fmt: ptF("A") }, { k: "B", vals: [3, 1, 1], fmt: ptF("B") }, { k: "C", vals: [1, 4, 1], fmt: ptF("C") }, { k: "D", vals: [2, 3, 5], fmt: ptF("D") }], draw); if (!g) return;
    function draw() {
      var A = g.f.v.A, B = g.f.v.B, C = g.f.v.C, D = g.f.v.D, T = tetra(A, B, C, D), items = [], pts = [A, B, C, D];
      var rows = [[t3("Vectors", "Vectores", "Vectors"), tex("\\overrightarrow{AB}=" + vT(T.u) + ",\\ \\overrightarrow{AC}=" + vT(T.v) + ",\\ \\overrightarrow{AD}=" + vT(T.w))],
        [tex("\\overrightarrow{AB}\\times\\overrightarrow{AC}"), tex(vT(T.cr))]];
      if (vzero(T.cr)) { rows.push(["", "<strong>" + t3("A, B i C estan alineats: no formen cap triangle.", "A, B y C están alineados: no forman ningún triángulo.", "A, B and C are collinear: they do not form a triangle.") + "</strong>"]); }
      else {
        rows.push([t3("Àrea del paral·lelogram", "Área del paralelogramo", "Parallelogram area"), tex("|\\overrightarrow{AB}\\times\\overrightarrow{AC}|=" + rtF(vdot(T.cr, T.cr)) + (exact(vdot(T.cr, T.cr)) ? "" : "=" + sqrtFrT(vdot(T.cr, T.cr))) + "\\ \\text{u}^2")]);
        rows.push([t3("Àrea del triangle", "Área del triángulo", "Triangle area"), tex("S=\\tfrac12|\\overrightarrow{AB}\\times\\overrightarrow{AC}|=" + sqrtFrT(T.area2) + (exact(T.area2) ? "" : "\\approx " + dT(Math.sqrt(fVal(T.area2)))) + "\\ \\text{u}^2")]);
        rows.push([tex("[\\overrightarrow{AB},\\overrightarrow{AC},\\overrightarrow{AD}]"), tex(detT(T.u, T.v, T.w))]);
        if (F(T.m).n === 0) rows.push(["", "<strong>" + t3("Els quatre punts són coplanaris: no hi ha tetraedre.", "Los cuatro puntos son coplanarios: no hay tetraedro.", "The four points are coplanar: there is no tetrahedron.") + "</strong>"]);
        else {
          rows.push([t3("Volum del tetraedre", "Volumen del tetraedro", "Tetrahedron volume"), tex("V=\\tfrac16|[\\overrightarrow{AB},\\overrightarrow{AC},\\overrightarrow{AD}]|=" + fT(T.V) + "\\ \\text{u}^3")]);
          rows.push([t3("Volum del paral·lelepípede", "Volumen del paralelepípedo", "Parallelepiped volume"), tex(fT(abs(T.m)) + "\\ \\text{u}^3")]);
          rows.push([t3("Altura des de D", "Altura desde D", "Height from D"), tex("h=\\dfrac{3V}{S}=d(D,\\pi_{ABC})=" + distT(T.h2))]);
          var c = planeEq(T.cr, fMul(-1, vdot(T.cr, A))), H = dPPl(D, c.c);
          rows.push([cdot(COL.p) + t3("Peu de l'altura", "Pie de la altura", "Foot of the height"), tex(vT(H.Q))]);
          items.push(segP(D, H.Q), dot3(vnum(H.Q), "H", COL.p)); pts.push(vnum(H.Q));
        }
      }
      [[A, B, C], [A, B, D], [A, C, D], [B, C, D]].forEach(function (f, i) { items.unshift({ poly: f, fill: i ? COL.k : COL.u, stroke: i ? COL.k : COL.u, op: i ? 0.1 : 0.25 }); });
      items.push(dot3(A, "A"), dot3(B, "B"), dot3(C, "C"), dot3(D, "D", COL.s));
      scene(g, items, pts);
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 4.10 llocs geomètrics ---------- */
  function circle3(C, n, R) { // circumferència de centre C, radi R, en el pla de normal n (numèric)
    var nn = Math.sqrt(n[0] * n[0] + n[1] * n[1] + n[2] * n[2]), u = n.map(function (x) { return x / nn; });
    var a = Math.abs(u[0]) < 0.9 ? [0, -u[2], u[1]] : [-u[2], 0, u[0]], la = Math.hypot(a[0], a[1], a[2]); a = a.map(function (x) { return x / la; });
    var b = [u[1] * a[2] - u[2] * a[1], u[2] * a[0] - u[0] * a[2], u[0] * a[1] - u[1] * a[0]], P = [];
    for (var i = 0; i < 48; i++) { var t = i / 48 * 2 * Math.PI; P.push([0, 1, 2].map(function (k) { return C[k] + R * (Math.cos(t) * a[k] + Math.sin(t) * b[k]); })); }
    return P;
  }
  function sphereI(C, R) { return [[1, 0, 0], [0, 1, 0], [0, 0, 1]].map(function (n) { return { poly: circle3(C, n, R), fill: COL.p, stroke: COL.p, op: 0.06, w: 1.2 }; }); }
  function rowsMed(A, B) {
    var o = med(A, B);
    return { o: o, rows: [[tex("\\overrightarrow{AB}"), tex(vT(o.n))], [t3("Punt mig", "Punto medio", "Midpoint"), tex("M=" + vT(o.M))],
      [t3("Condició", "Condición", "Condition"), tex("d(X,A)=d(X,B)\\iff\\overrightarrow{AB}\\cdot\\overrightarrow{MX}=0")],
      [cdot(PCOL[2][1]) + t3("Pla mediador", "Plano mediador", "Perpendicular bisector plane"), tex(o.pl.t)]] };
  }
  function rowsBis(c1, c2) {
    var o = bis(c1, c2), rows = [[t3("Condició", "Condición", "Condition"), tex("\\dfrac{|" + planeT(c1).slice(0, -2) + "|}{" + rtF(o.S1) + "}=\\dfrac{|" + planeT(c2).slice(0, -2) + "|}{" + rtF(o.S2) + "}")]];
    if (PlPl(c1, c2).pos !== 2) rows.push(["", "<strong>" + t3("Els plans són paral·lels: el lloc és un sol pla, paral·lel a tots dos i a mitja distància.", "Los planos son paralelos: el lugar es un solo plano, paralelo a ambos y a media distancia.", "The planes are parallel: the locus is a single plane, parallel to both and halfway between them.") + "</strong>"]);
    if (o.ex) o.ex.forEach(function (p, i) { if (p) rows.push([cdot(i ? PCOL[1][1] : COL.k) + t3("Bisector ", "Bisector ", "Bisector ") + (i + 1), tex(p.t)]); });
    else rows.push([t3("Bisectors", "Bisectores", "Bisectors"), tex(sqT(fVal(o.S2)) + "\\,(" + planeT(c1).slice(0, -2) + ")\\mp" + sqT(fVal(o.S1)) + "\\,(" + planeT(c2).slice(0, -2) + ")=0")]);
    return { rows: rows, o: o };
  }
  function rowsSph(C, R, c) {
    var D = dPPl(C, c), R2 = Fr(R * R), diff = fSub(R2, D.d2), rows = [[t3("Esfera", "Esfera", "Sphere"), tex("(x" + (C[0] ? (C[0] < 0 ? "+" : "-") + Math.abs(C[0]) : "") + ")^2+(y" + (C[1] ? (C[1] < 0 ? "+" : "-") + Math.abs(C[1]) : "") + ")^2+(z" + (C[2] ? (C[2] < 0 ? "+" : "-") + Math.abs(C[2]) : "") + ")^2=" + R * R)],
      [tex("d(C,\\pi)"), tex("\\dfrac{|" + evalT(c, C) + "|}{" + rtF(D.S) + "}=" + distT(D.d2))]];
    var k = F(diff).n > 0 ? 0 : F(diff).n === 0 ? 1 : 2;
    rows.push([t3("Posició", "Posición", "Position"), "<strong>" + [t3("Secant: talla l'esfera en una circumferència", "Secante: corta la esfera en una circunferencia", "Intersecting: it cuts the sphere in a circle"), t3("Tangent: un sol punt comú", "Tangente: un solo punto común", "Tangent: one common point"), t3("Exterior: no la talla", "Exterior: no la corta", "Exterior: it misses the sphere")][k] + "</strong>"]);
    if (k === 0) rows.push([cdot(COL.k) + t3("Circumferència", "Circunferencia", "Circle"), tex(t3("\\text{centre }", "\\text{centro }", "\\text{centre }") + vT(D.Q) + ",\\ \\rho=\\sqrt{R^2-d^2}=" + sqrtFrT(diff))]);
    if (k === 1) rows.push([cdot(COL.k) + t3("Punt de tangència", "Punto de tangencia", "Point of tangency"), tex(vT(D.Q))]);
    return { rows: rows, D: D, k: k, diff: diff };
  }
  function wLloc() {
    var MODES = [function () { return [{ k: "A", vals: [1, 2, 3], fmt: ptF("A") }, { k: "B", vals: [-3, -2, 3], fmt: ptF("B") }]; },
      function () { return [{ k: "p1", vals: [1, 2, 2, -1], fmt: plF("\\pi_1") }, { k: "p2", vals: [2, -1, 2, 3], fmt: plF("\\pi_2") }]; },
      function () { return [{ k: "C", vals: [1, 2, -1], fmt: ptF("C") }, { k: "R", vals: [3], fmt: [tex("R="), ""] }, { k: "pi", vals: [2, -1, 2, 8], fmt: plF("\\pi") }]; }];
    var g = setupModes("w-lloc", function () { return [t3("Pla mediador", "Plano mediador", "Bisector plane"), t3("Plans bisectors", "Planos bisectores", "Angle-bisector planes"), t3("Esfera i pla", "Esfera y plano", "Sphere and plane")]; }, MODES, draw); if (!g) return;
    function draw() {
      var v = g.f.v, items = [], pts = [], rows;
      if (g.mode === 0) {
        if (vzero(vsub(v.B, v.A))) { bad(g, t3("A i B han de ser diferents.", "A y B tienen que ser distintos.", "A and B must be different.")); g.scene = { items: [], w: 340, h: 300 }; g.redraw(); return; }
        var M = rowsMed(v.A, v.B); rows = M.rows;
        items.push(pl(2, vnum(M.o.n), -fVal(vdot(M.o.n, M.o.M))), segP(v.A, v.B, "var(--muted)", "3 3"), dot3(v.A, "A", COL.r), dot3(v.B, "B", COL.s), dot3(vnum(M.o.M), "M", COL.p)); pts = [v.A, v.B];
      } else if (g.mode === 1) {
        if (noPlane(v.p1) || noPlane(v.p2)) { bad(g, MSG.pl()); g.scene = { items: [], w: 340, h: 300 }; g.redraw(); return; }
        var B = rowsBis(v.p1, v.p2); rows = B.rows;
        items.push(pl(0, nOf(v.p1), v.p1[3]), pl(1, nOf(v.p2), v.p2[3]));
        var par = PlPl(v.p1, v.p2).pos !== 2;
        B.o.num.forEach(function (c, i) { if (Math.hypot(c[0], c[1], c[2]) > 1e-9 && !(par && i === 0 && B.o.ex && !B.o.ex[0])) items.push({ plane: c, fill: COL.k, stroke: COL.k, op: 0.3 }); });
      } else {
        var R = v.R[0];
        if (R <= 0) { bad(g, t3("El radi ha de ser positiu.", "El radio tiene que ser positivo.", "The radius must be positive.")); g.scene = { items: [], w: 340, h: 300 }; g.redraw(); return; }
        if (noPlane(v.pi)) { bad(g, MSG.pl()); g.scene = { items: [], w: 340, h: 300 }; g.redraw(); return; }
        var S = rowsSph(v.C, R, v.pi); rows = S.rows;
        items = sphereI(v.C, R).concat([pl(2, nOf(v.pi), v.pi[3]), dot3(v.C, "C", COL.p)]);
        if (S.k === 0) items.push({ poly: circle3(vnum(S.D.Q), nOf(v.pi), Math.sqrt(fVal(S.diff))), fill: "none", stroke: COL.k, w: 2.6, op: 0 });
        if (S.k < 2) items.push(segP(v.C, S.D.Q), dot3(vnum(S.D.Q), "Q", COL.k));
        pts = [v.C.map(function (x) { return Math.abs(x) + R; })];
      }
      g.scene = { items: items, L: Lof(pts, 3), w: 340, h: 300 }; g.redraw();
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- laboratori mètric ---------- */
  function wLab() {
    var D = { P: [5, 1, 6], A: [2, 1, 0], d: [1, 2, 2], Q: [1, 4, 4], e: [2, -1, -2], p1: [2, -1, 2, -3], p2: [1, 1, 1, -6] };
    function G(k, name, kind) { return { k: k, vals: D[k].slice(), fmt: kind === "p" ? ptF(name) : kind === "v" ? veF(name) : plF(name) }; }
    var MODES = [function () { return [G("P", "P", "p"), G("A", "A", "p"), G("d", "\\vec d", "v")]; },
      function () { return [G("P", "P", "p"), G("p1", "\\pi", "pl")]; },
      function () { return [G("A", "P", "p"), G("d", "\\vec d_r", "v"), G("Q", "Q", "p"), G("e", "\\vec d_s", "v")]; },
      function () { return [G("A", "P", "p"), G("d", "\\vec d", "v"), G("p1", "\\pi", "pl")]; },
      function () { return [G("p1", "\\pi_1", "pl"), G("p2", "\\pi_2", "pl")]; }];
    var g = setupModes("w-lab", function () { return [t3("Punt i recta", "Punto y recta", "Point and line"), t3("Punt i pla", "Punto y plano", "Point and plane"), t3("Dues rectes", "Dos rectas", "Two lines"), t3("Recta i pla", "Recta y plano", "Line and plane"), t3("Dos plans", "Dos planos", "Two planes")]; }, MODES, draw); if (!g) return;
    function head(s) { return ["", "<b>" + s + "</b>"]; }
    function draw() {
      var v = g.f.v, items = [], pts = [], rows = [], m = g.mode, X;
      function stop(msg) { bad(g, msg); g.scene = { items: [], w: 340, h: 300 }; g.redraw(); }
      if (m === 0) {
        if (vzero(v.d)) return stop(MSG.d());
        X = rowsPL(v.P, v.A, v.d); var S = rowsSymL(v.P, v.A, v.d);
        rows = [head(t3("Distància", "Distancia", "Distance"))].concat(X.rows, [head(t3("Simètric de P respecte de r", "Simétrico de P respecto de r", "Reflection of P in r"))], S.rows.slice(2));
        items = [lineI(v.A, v.d, COL.r, "r"), dot3(v.P, "P", COL.s), dot3(v.A, "A", COL.r), segP(v.P, S.P1), dot3(vnum(S.o.Q), "Q", COL.p), dot3(vnum(S.P1), "P'", COL.k)]; pts = [v.P, v.A, vnum(S.P1)];
      } else if (m === 1) {
        if (noPlane(v.p1)) return stop(MSG.pl());
        X = rowsPPl(v.P, v.p1); var T = rowsSymP(v.P, v.p1);
        rows = [head(t3("Distància i projecció", "Distancia y proyección", "Distance and projection"))].concat(X.rows, [head(t3("Simètric de P respecte de π", "Simétrico de P respecto de π", "Reflection of P in π"))], T.rows.slice(2));
        items = [pl(2, nOf(v.p1), v.p1[3]), dot3(v.P, "P", COL.s), segP(v.P, T.P1), dot3(vnum(T.o.Q), "Q", COL.p), dot3(vnum(T.P1), "P'", COL.k)]; pts = [v.P, vnum(T.P1)];
      } else if (m === 2) {
        if (vzero(v.d) || vzero(v.e)) return stop(MSG.d());
        X = rowsLL(v.A, v.d, v.Q, v.e);
        rows = [head(t3("Angle", "Ángulo", "Angle"))].concat(angRows(v.d, v.e, 0).rows, [head(t3("Posició i distància", "Posición y distancia", "Position and distance"))], X.rows);
        items = [lineI(v.A, v.d, COL.r, "r"), lineI(v.Q, v.e, COL.s, "s"), dot3(v.A, "P", COL.r), dot3(v.Q, "Q", COL.s)]; pts = [v.A, v.Q];
        if (X.o.X) { items.push(dot3(vnum(X.o.X), "X", COL.p)); if (X.o.pos % 2) items.push(segP(X.o.X, X.o.Y, COL.p, false), dot3(vnum(X.o.Y), "Y", COL.p)); }
      } else if (m === 3) {
        if (vzero(v.d)) return stop(MSG.d());
        if (noPlane(v.p1)) return stop(MSG.pl());
        X = rowsLPl(v.A, v.d, v.p1); var U = rowsSymLine(v.A, v.d, v.p1);
        rows = [head(t3("Angle", "Ángulo", "Angle"))].concat(angRows(v.d, nOf(v.p1), 1).rows, [head(t3("Posició i distància", "Posición y distancia", "Position and distance"))], X.rows,
          [head(t3("Recta simètrica respecte de π", "Recta simétrica respecto de π", "Line reflected in π"))], U.rows);
        items = [pl(2, nOf(v.p1), v.p1[3]), lineI(v.A, v.d, COL.r, "r"), lineI(U.s.P, U.s.d, COL.k, "r'"), dot3(v.A, "P", COL.r)]; pts = [v.A];
        if (X.o.pos === 0) items.push(dot3(vnum(X.o.X), "X", COL.p));
      } else {
        if (noPlane(v.p1) || noPlane(v.p2)) return stop(MSG.pl());
        X = rowsPlPl(v.p1, v.p2);
        rows = [head(t3("Angle", "Ángulo", "Angle"))].concat(angRows(nOf(v.p1), nOf(v.p2), 2).rows, [head(t3("Posició i distància", "Posición y distancia", "Position and distance"))], X.rows,
          [head(t3("Plans bisectors", "Planos bisectores", "Angle-bisector planes"))], rowsBis(v.p1, v.p2).rows.slice(1));
        items = [pl(0, nOf(v.p1), v.p1[3]), pl(2, nOf(v.p2), v.p2[3])];
      }
      g.scene = { items: items, L: Lof(pts, 3), w: 340, h: 300 }; g.redraw();
      g.info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("L'angle entre dues rectes sempre està entre…", "El ángulo entre dos rectas siempre está entre…", "The angle between two lines is always between…"),
      o: [q3("$0^\\circ$ i $90^\\circ$", "$0^\\circ$ y $90^\\circ$", "$0^\\circ$ and $90^\\circ$"), q3("$0^\\circ$ i $180^\\circ$", "$0^\\circ$ y $180^\\circ$", "$0^\\circ$ and $180^\\circ$"), q3("$-90^\\circ$ i $90^\\circ$", "$-90^\\circ$ y $90^\\circ$", "$-90^\\circ$ and $90^\\circ$")], a: 0,
      e: q3("Per això posem el valor absolut: $\\cos\\alpha=\\frac{|\\vec d_r\\cdot\\vec d_s|}{|\\vec d_r||\\vec d_s|}\\ge0$.", "Por eso ponemos el valor absoluto: $\\cos\\alpha=\\frac{|\\vec d_r\\cdot\\vec d_s|}{|\\vec d_r||\\vec d_s|}\\ge0$.", "That is why we take the absolute value: $\\cos\\alpha=\\frac{|\\vec d_r\\cdot\\vec d_s|}{|\\vec d_r||\\vec d_s|}\\ge0$.") },
    { q: q3("Per a l'angle entre una recta i un pla fem servir…", "Para el ángulo entre una recta y un plano usamos…", "For the angle between a line and a plane we use…"),
      o: [q3("el cosinus entre $\\vec d$ i $\\vec n$", "el coseno entre $\\vec d$ y $\\vec n$", "the cosine between $\\vec d$ and $\\vec n$"), q3("el sinus: $\\sin\\alpha=\\frac{|\\vec d\\cdot\\vec n|}{|\\vec d||\\vec n|}$", "el seno: $\\sin\\alpha=\\frac{|\\vec d\\cdot\\vec n|}{|\\vec d||\\vec n|}$", "the sine: $\\sin\\alpha=\\frac{|\\vec d\\cdot\\vec n|}{|\\vec d||\\vec n|}$"), q3("el producte vectorial", "el producto vectorial", "the cross product")], a: 1,
      e: q3("L'angle entre $\\vec d$ i $\\vec n$ és el complementari de l'angle entre la recta i el pla.", "El ángulo entre $\\vec d$ y $\\vec n$ es el complementario del ángulo entre la recta y el plano.", "The angle between $\\vec d$ and $\\vec n$ is the complement of the angle between the line and the plane.") },
    { q: q3("Els plans $x+y=1$ i $x-y+3z=0$ són…", "Los planos $x+y=1$ y $x-y+3z=0$ son…", "The planes $x+y=1$ and $x-y+3z=0$ are…"),
      o: [q3("paral·lels", "paralelos", "parallel"), q3("perpendiculars", "perpendiculares", "perpendicular"), q3("secants a $45^\\circ$", "secantes a $45^\\circ$", "at $45^\\circ$")], a: 1, e: q3("$\\vec n_1\\cdot\\vec n_2=1-1+0=0$.") },
    { q: q3("La distància de $P(1,1,1)$ al pla $2x-y+2z+4=0$ és…", "La distancia de $P(1,1,1)$ al plano $2x-y+2z+4=0$ es…", "The distance from $P(1,1,1)$ to the plane $2x-y+2z+4=0$ is…"),
      o: [q3("$\\frac73$"), q3("$7$"), q3("$\\frac{7}{\\sqrt5}$")], a: 0, e: q3("$\\frac{|2-1+2+4|}{\\sqrt{4+1+4}}=\\frac73$.") },
    { q: q3("La distància d'un punt $P$ a una recta $r$ (punt $A$, director $\\vec d$) és…", "La distancia de un punto $P$ a una recta $r$ (punto $A$, director $\\vec d$) es…", "The distance from a point $P$ to a line $r$ (point $A$, direction $\\vec d$) is…"),
      o: [q3("$\\frac{|\\overrightarrow{AP}\\cdot\\vec d|}{|\\vec d|}$"), q3("$\\frac{|\\overrightarrow{AP}\\times\\vec d|}{|\\vec d|}$"), q3("$|\\overrightarrow{AP}\\times\\vec d|$")], a: 1, e: q3("És l'altura del paral·lelogram de costats $\\overrightarrow{AP}$ i $\\vec d$: àrea entre base.", "Es la altura del paralelogramo de lados $\\overrightarrow{AP}$ y $\\vec d$: área entre base.", "It is the height of the parallelogram with sides $\\overrightarrow{AP}$ and $\\vec d$: area over base.") },
    { q: q3("Si dues rectes es tallen, la distància entre elles és…", "Si dos rectas se cortan, la distancia entre ellas es…", "If two lines meet, the distance between them is…"),
      o: [q3("0"), q3("la distància entre els punts $P$ i $Q$", "la distancia entre los puntos $P$ y $Q$", "the distance between the points $P$ and $Q$"), q3("no es pot calcular", "no se puede calcular", "impossible to compute")], a: 0, e: q3("Tenen un punt comú; de fet, el producte mixt $[\\overrightarrow{PQ},\\vec d_r,\\vec d_s]$ és 0.", "Tienen un punto común; de hecho, el producto mixto $[\\overrightarrow{PQ},\\vec d_r,\\vec d_s]$ es 0.", "They share a point; indeed the triple product $[\\overrightarrow{PQ},\\vec d_r,\\vec d_s]$ is 0.") },
    { q: q3("Per a la distància entre dues rectes que s'encreuen, el numerador de la fórmula és…", "Para la distancia entre dos rectas que se cruzan, el numerador de la fórmula es…", "For the distance between two skew lines, the numerator of the formula is…"),
      o: [q3("$|\\vec d_r\\times\\vec d_s|$"), q3("$|[\\overrightarrow{PQ},\\vec d_r,\\vec d_s]|$"), q3("$|\\overrightarrow{PQ}|$")], a: 1, e: q3("$d=\\frac{|[\\overrightarrow{PQ},\\vec d_r,\\vec d_s]|}{|\\vec d_r\\times\\vec d_s|}$: volum del paral·lelepípede entre l'àrea de la base.", "$d=\\frac{|[\\overrightarrow{PQ},\\vec d_r,\\vec d_s]|}{|\\vec d_r\\times\\vec d_s|}$: volumen del paralelepípedo entre el área de la base.", "$d=\\frac{|[\\overrightarrow{PQ},\\vec d_r,\\vec d_s]|}{|\\vec d_r\\times\\vec d_s|}$: parallelepiped volume over base area.") },
    { q: q3("La distància entre els plans $x+2y-2z=1$ i $x+2y-2z=7$ és…", "La distancia entre los planos $x+2y-2z=1$ y $x+2y-2z=7$ es…", "The distance between the planes $x+2y-2z=1$ and $x+2y-2z=7$ is…"),
      o: [q3("$6$"), q3("$2$"), q3("$\\frac83$")], a: 1, e: q3("$\\frac{|7-1|}{\\sqrt{1+4+4}}=\\frac63=2$.") },
    { q: q3("Si una recta talla un pla, la distància entre ells és…", "Si una recta corta a un plano, la distancia entre ellos es…", "If a line cuts a plane, the distance between them is…"),
      o: [q3("0"), q3("$d(P,\\pi)$ per a qualsevol $P$ de la recta", "$d(P,\\pi)$ para cualquier $P$ de la recta", "$d(P,\\pi)$ for any $P$ on the line"), q3("l'angle que formen", "el ángulo que forman", "the angle between them")], a: 0, e: q3("Només té sentit calcular $d(P,\\pi)$ quan la recta és paral·lela al pla.", "Solo tiene sentido calcular $d(P,\\pi)$ cuando la recta es paralela al plano.", "Computing $d(P,\\pi)$ only makes sense when the line is parallel to the plane.") },
    { q: q3("El simètric de $P(1,2,3)$ respecte del pla $z=0$ és…", "El simétrico de $P(1,2,3)$ respecto del plano $z=0$ es…", "The reflection of $P(1,2,3)$ in the plane $z=0$ is…"),
      o: [q3("$(1,2,0)$"), q3("$(-1,-2,3)$"), q3("$(1,2,-3)$")], a: 2, e: q3("La projecció és $M(1,2,0)$ i $P'=2M-P=(1,2,-3)$.", "La proyección es $M(1,2,0)$ y $P'=2M-P=(1,2,-3)$.", "The projection is $M(1,2,0)$ and $P'=2M-P=(1,2,-3)$.") },
    { q: q3("Per a trobar el simètric de $P$ respecte d'una recta $r$, el primer pas és…", "Para hallar el simétrico de $P$ respecto de una recta $r$, el primer paso es…", "To reflect $P$ in a line $r$, the first step is…"),
      o: [q3("el pla per $P$ perpendicular a $r$", "el plano por $P$ perpendicular a $r$", "the plane through $P$ perpendicular to $r$"), q3("la recta per $P$ paral·lela a $r$", "la recta por $P$ paralela a $r$", "the line through $P$ parallel to $r$"), q3("el pla que conté $r$ i $P$", "el plano que contiene $r$ y $P$", "the plane containing $r$ and $P$")], a: 0, e: q3("Aquest pla talla $r$ en la projecció $M$, i aleshores $P'=2M-P$.", "Este plano corta a $r$ en la proyección $M$, y entonces $P'=2M-P$.", "That plane meets $r$ at the projection $M$, and then $P'=2M-P$.") },
    { q: q3("El volum del tetraedre de vèrtexs $O$, $(2,0,0)$, $(0,3,0)$ i $(0,0,4)$ és…", "El volumen del tetraedro de vértices $O$, $(2,0,0)$, $(0,3,0)$ y $(0,0,4)$ es…", "The volume of the tetrahedron with vertices $O$, $(2,0,0)$, $(0,3,0)$ and $(0,0,4)$ is…"),
      o: [q3("$24$"), q3("$4$"), q3("$12$")], a: 1, e: q3("$V=\\frac16|2\\cdot3\\cdot4|=4$.") },
    { q: q3("El lloc geomètric dels punts que equidisten de $A$ i $B$ és…", "El lugar geométrico de los puntos que equidistan de $A$ y $B$ es…", "The locus of points equidistant from $A$ and $B$ is…"),
      o: [q3("la recta $AB$", "la recta $AB$", "the line $AB$"), q3("el pla mediador del segment $AB$", "el plano mediador del segmento $AB$", "the perpendicular bisector plane of $AB$"), q3("una esfera de diàmetre $AB$", "una esfera de diámetro $AB$", "a sphere with diameter $AB$")], a: 1, e: q3("És el pla perpendicular a $\\overrightarrow{AB}$ que passa pel punt mig.", "Es el plano perpendicular a $\\overrightarrow{AB}$ que pasa por el punto medio.", "It is the plane perpendicular to $\\overrightarrow{AB}$ through the midpoint.") },
    { q: q3("Els punts que equidisten de dos plans secants formen…", "Los puntos que equidistan de dos planos secantes forman…", "The points equidistant from two intersecting planes form…"),
      o: [q3("un pla", "un plano", "one plane"), q3("dos plans perpendiculars (els bisectors)", "dos planos perpendiculares (los bisectores)", "two perpendicular planes (the bisectors)"), q3("una recta", "una recta", "a line")], a: 1, e: q3("Igualem $\\frac{|\\pi_1|}{|\\vec n_1|}=\\frac{|\\pi_2|}{|\\vec n_2|}$: els dos signes donen dos plans.", "Igualamos $\\frac{|\\pi_1|}{|\\vec n_1|}=\\frac{|\\pi_2|}{|\\vec n_2|}$: los dos signos dan dos planos.", "Set $\\frac{|\\pi_1|}{|\\vec n_1|}=\\frac{|\\pi_2|}{|\\vec n_2|}$: the two signs give two planes.") },
    { q: q3("El pla $2x+y-2z=9$ i l'esfera de centre $O$ i radi $3$…", "El plano $2x+y-2z=9$ y la esfera de centro $O$ y radio $3$…", "The plane $2x+y-2z=9$ and the sphere with centre $O$ and radius $3$…"),
      o: [q3("es tallen en una circumferència", "se cortan en una circunferencia", "meet in a circle"), q3("són tangents", "son tangentes", "are tangent"), q3("no es tallen", "no se cortan", "do not meet")], a: 1, e: q3("$d(O,\\pi)=\\frac{9}{3}=3=R$: tangents.", "$d(O,\\pi)=\\frac{9}{3}=3=R$: tangentes.", "$d(O,\\pi)=\\frac{9}{3}=3=R$: tangent.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Problemes mètrics · FentMates", es: "Problemas métricos · FentMates", en: "Metric problems · FentMates" };
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
      document.querySelectorAll(".widget .wt, .widget label, .widget .legend, .widget > p, #lab .bh, #lab .bb > p").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wArr, wArp, wDpp, wDpr, wDrr, wDpl, wSr, wSp, wVol, wLloc, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM4 = { Fr: Fr, sqrtFrT: sqrtFrT, angLL: angLL, dPPl: dPPl, dPL: dPL, LL: LL, LPl: LPl, PlPl: PlPl, symLinePl: symLinePl, med: med, bis: bis, tetra: tetra, fVal: fVal, vT: vT };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
