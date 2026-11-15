(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-4eso-b-u6-done";

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

  /* ---------- expressions i equacions ---------- */
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
  // Ax+By+C=0 amb coeficients enters, primitius i el primer positiu
  function gen(A, B, C) {
    A = F(A); B = F(B); C = F(C);
    var L = lcm(lcm(A.d, B.d), C.d), a = A.n * L / A.d, b = B.n * L / B.d, c = C.n * L / C.d, g = gcd(gcd(a, b), c) || 1;
    a /= g; b /= g; c /= g;
    if (a < 0 || (a === 0 && b < 0)) { a = -a; b = -b; c = -c; }
    return { A: a, B: b, C: c, t: poly([[a, "x"], [b, "y"], [c, ""]]) + "=0" };
  }
  // recta per P amb vector director d (enters o fraccions)
  function lineDir(P, d) { return gen(d[1], fMul(-1, d[0]), fSub(fMul(d[0], P[1]), fMul(d[1], P[0]))); }
  function lineNormal(P, n) { return gen(n[0], n[1], fMul(-1, fAdd(fMul(n[0], P[0]), fMul(n[1], P[1])))); }
  function inter(r, s) { // punt de tall de dues rectes generals (null si són paral·leles)
    var det = r.A * s.B - s.A * r.B;
    if (!det) return null;
    return [Fr(r.B * s.C - s.B * r.C, det), Fr(s.A * r.C - r.A * s.C, det)];
  }
  function onLine(r, P) { return fAdd(fAdd(fMul(r.A, P[0]), fMul(r.B, P[1])), r.C).n === 0; }
  function prim(v) { var g = gcd(v[0], v[1]) || 1; return [v[0] / g, v[1] / g]; }

  /* ---------- pla cartesià amb punts arrossegables ---------- */
  var COL = { u: "#3b82f6", v: "#f97316", w: "#16a34a", r: "#3b82f6", s: "#e11d48", p: "#8b5cf6", k: "#0f9488" };
  function Plane(svg, o) {
    o = o || {};
    var r = o.r || 8, S = 360, pad = 16, k = (S - 2 * pad) / (2 * r), lim = o.lim || r;
    var P = { r: r, pts: o.pts || {}, ok: o.ok, onChange: null };
    function X(x) { return pad + (x + r) * k; }
    function Y(y) { return pad + (r - y) * k; }
    function f(x) { return Math.round(x * 10) / 10; }
    function L(x1, y1, x2, y2, cls, st) { return '<line x1="' + f(x1) + '" y1="' + f(y1) + '" x2="' + f(x2) + '" y2="' + f(y2) + '" class="' + cls + '"' + (st ? ' style="' + st + '"' : "") + "/>"; }
    var base = "", i;
    for (i = -r; i <= r; i++) base += L(X(i), Y(-r), X(i), Y(r), "g") + L(X(-r), Y(i), X(r), Y(i), "g");
    base += L(X(-r), Y(0), X(r) + 4, Y(0), "ax") + L(X(0), Y(-r), X(0), Y(r) - 4, "ax");
    for (i = -r + 2; i < r; i += 2) if (i) base += '<text x="' + X(i) + '" y="' + (Y(0) + 13) + '" text-anchor="middle">' + (i < 0 ? "−" + -i : i) + "</text>" +
      '<text x="' + (X(0) - 5) + '" y="' + (Y(i) + 3.5) + '" text-anchor="end">' + (i < 0 ? "−" + -i : i) + "</text>";
    P.X = X; P.Y = Y;
    function num(p) { return [fVal(p[0]), fVal(p[1])]; }
    P.seg = function (p, q, col, cls) { p = num(p); q = num(q); return L(X(p[0]), Y(p[1]), X(q[0]), Y(q[1]), cls || "ln", col ? "stroke:" + col : ""); };
    P.arrow = function (p, q, col, lbl, cls) {
      p = num(p); q = num(q);
      var x1 = X(p[0]), y1 = Y(p[1]), x2 = X(q[0]), y2 = Y(q[1]), dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy);
      if (len < 3) return "";
      var ux = dx / len, uy = dy / len, h = Math.min(11, len * 0.6), w = h * 0.45, bx = x2 - ux * h, by = y2 - uy * h, s = "";
      s += L(x1, y1, bx + ux, by + uy, "vec" + (cls ? " " + cls : ""), "stroke:" + col);
      s += '<path d="M' + f(x2) + " " + f(y2) + "L" + f(bx - uy * w) + " " + f(by + ux * w) + "L" + f(bx + uy * w) + " " + f(by - ux * w) + 'Z" style="fill:' + col + '"/>';
      if (lbl) s += P.text([(p[0] + q[0]) / 2, (p[1] + q[1]) / 2], lbl, -uy * 13, ux * 13 * -1 + 4, true, col);
      return s;
    };
    P.text = function (p, s, dx, dy, it, col) {
      p = num(p);
      return '<text x="' + f(X(p[0]) + (dx || 0)) + '" y="' + f(Y(p[1]) + (dy || 0)) + '" text-anchor="middle" class="lb' + (it ? " it" : "") + '"' + (col ? ' style="fill:' + col + '"' : "") + ">" + s + "</text>";
    };
    P.dot = function (p, col, id, lbl, pos) {
      var q = num(p), x = X(q[0]), y = Y(q[1]), s = "";
      if (id) s += '<circle class="halo" data-id="' + id + '" cx="' + f(x) + '" cy="' + f(y) + '" r="17"/>';
      s += '<circle class="pt' + (id ? " drag" : "") + '"' + (id ? ' data-id="' + id + '"' : "") + ' cx="' + f(x) + '" cy="' + f(y) + '" r="' + (id ? 6.5 : 4.5) + '" style="fill:' + col + '"/>';
      if (lbl) { pos = pos || [12, -10]; s += '<text x="' + f(x + pos[0]) + '" y="' + f(y + pos[1]) + '" text-anchor="middle" class="lb it">' + lbl + "</text>"; }
      return s;
    };
    // recta per p amb direcció d, retallada al requadre
    P.line = function (p, d, col, cls) {
      p = num(p); d = num(d);
      var t0 = -1e9, t1 = 1e9, ok = true;
      [[d[0], p[0]], [d[1], p[1]]].forEach(function (c) {
        if (Math.abs(c[0]) < 1e-12) { if (c[1] < -r || c[1] > r) ok = false; return; }
        var a = (-r - c[1]) / c[0], b = (r - c[1]) / c[0];
        t0 = Math.max(t0, Math.min(a, b)); t1 = Math.min(t1, Math.max(a, b));
      });
      if (!ok || t0 >= t1) return "";
      return L(X(p[0] + t0 * d[0]), Y(p[1] + t0 * d[1]), X(p[0] + t1 * d[0]), Y(p[1] + t1 * d[1]), "ln" + (cls ? " " + cls : ""), "stroke:" + col);
    };
    P.gline = function (g, col, cls) { // recta Ax+By+C=0
      var p = g.B ? [Fr(0), Fr(-g.C, g.B)] : [Fr(-g.C, g.A), Fr(0)];
      return P.line(p, [-g.B, g.A], col, cls);
    };
    // arc d'angle al voltant de c, des de l'angle a0 fins a a1 (radians, sentit antihorari)
    P.arc = function (c, a0, a1, rad, col, lbl) {
      c = num(c);
      var x = X(c[0]), y = Y(c[1]), sweep = a1 - a0;
      while (sweep < 0) sweep += 2 * Math.PI;
      var xa = x + rad * Math.cos(a0), ya = y - rad * Math.sin(a0), xb = x + rad * Math.cos(a0 + sweep), yb = y - rad * Math.sin(a0 + sweep);
      var s = '<path class="arc" style="stroke:' + col + '" d="M' + f(xa) + " " + f(ya) + "A" + rad + " " + rad + " 0 " + (sweep > Math.PI ? 1 : 0) + " 0 " + f(xb) + " " + f(yb) + '"/>';
      if (lbl) { var m = a0 + sweep / 2; s += '<text x="' + f(x + (rad + 12) * Math.cos(m)) + '" y="' + f(y - (rad + 12) * Math.sin(m) + 4) + '" text-anchor="middle" class="lb it" style="fill:' + col + '">' + lbl + "</text>"; }
      return s;
    };
    P.draw = function (h) { svg.innerHTML = base + h; };
    var drag = null;
    function toW(e) {
      var m = svg.getScreenCTM(); if (!m) return null;
      var pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
      var q = pt.matrixTransform(m.inverse());
      return [Math.max(-lim, Math.min(lim, Math.round((q.x - pad) / k - r))), Math.max(-lim, Math.min(lim, Math.round(r - (q.y - pad) / k)))];
    }
    svg.addEventListener("pointerdown", function (e) {
      var t = e.target.closest ? e.target.closest("[data-id]") : null;
      if (!t) return;
      drag = t.getAttribute("data-id"); svg.classList.add("dragging");
      try { svg.setPointerCapture(e.pointerId); } catch (_) {}
      e.preventDefault();
    });
    svg.addEventListener("pointermove", function (e) {
      if (!drag) return;
      var w = toW(e), c = P.pts[drag];
      if (!w || (c && c[0] === w[0] && c[1] === w[1])) return;
      if (P.ok && !P.ok(drag, w)) return;
      P.pts[drag] = w;
      if (P.onChange) P.onChange(drag);
    });
    function up() { drag = null; svg.classList.remove("dragging"); }
    svg.addEventListener("pointerup", up); svg.addEventListener("pointercancel", up);
    return P;
  }
  function sub(p, q) { return [fSub(p[0], q[0]), fSub(p[1], q[1])]; }
  function dv(p, q) { return [p[0] - q[0], p[1] - q[1]]; } // components enteres de q→p (punts enters)
  function diff(id, pts) { return function (k, w) { return !Object.keys(pts).some(function (j) { return j !== k && pts[j][0] === w[0] && pts[j][1] === w[1]; }); }; }
  function setup(id, pts, opt) {
    var w = document.getElementById(id); if (!w) return null;
    opt = opt || {}; opt.pts = pts;
    var P = Plane(w.querySelector("svg.gp-svg"), opt);
    if (!opt.ok && opt.distinct !== false) P.ok = diff(id, pts);
    return { w: w, P: P, info: w.querySelector(".info") };
  }
  function kv(rows) { return '<div class="kv">' + rows.map(function (r) { return "<span>" + r[0] + "</span><span>" + r[1] + "</span>"; }).join("") + "</div>"; }
  function cdot(c) { return '<i class="tag-c" style="background:' + c + '"></i>'; }

  /* ---------- 6.1 vectors ---------- */
  function wVec() {
    var g = setup("w-vec", { A: [-1, 3], B: [3, 0] }); if (!g) return;
    var P = g.P, pt = P.pts;
    function draw() {
      var A = pt.A, B = pt.B, v = [B[0] - A[0], B[1] - A[1]], m2 = v[0] * v[0] + v[1] * v[1], O = [0, 0];
      var h = P.seg(A, [B[0], A[1]], COL.v, "gd") + P.seg([B[0], A[1]], B, COL.w, "gd");
      if (v[0]) h += P.text([(A[0] + B[0]) / 2, A[1]], String(v[0]).replace("-", "−"), 0, v[1] > 0 ? 14 : -6, false, COL.v);
      if (v[1]) h += P.text([B[0], (A[1] + B[1]) / 2], String(v[1]).replace("-", "−"), v[0] >= 0 ? 12 : -12, 4, false, COL.w);
      if (A[0] || A[1]) h += P.arrow(O, v, COL.p, "", "d");
      h += P.arrow(A, B, COL.u) + P.dot(A, "var(--text)", "A", "A", [-12, -8]) + P.dot(B, COL.u, "B", "B");
      P.draw(h);
      g.info.innerHTML = kv([
        [tex("A,\\ B"), tex("A" + cT(A) + ",\\ B" + cT(B))],
        [cdot(COL.u) + t3("Components", "Componentes", "Components"), tex("\\overrightarrow{AB}=(" + B[0] + "-" + fP(A[0]) + ",\\," + B[1] + "-" + fP(A[1]) + ")=" + cT(v))],
        [t3("Mòdul", "Módulo", "Magnitude"), tex("|\\overrightarrow{AB}|=\\sqrt{" + fP(v[0]) + "^2+" + fP(v[1]) + "^2}=\\sqrt{" + m2 + "}" + (surd(m2).a > 1 ? "=" + sqT(m2) : "") + sqApprox(m2))],
        ["", "<small>" + t3("El mòdul és la hipotenusa d'un triangle rectangle de catets |", "El módulo es la hipotenusa de un triángulo rectángulo de catetos |", "The magnitude is the hypotenuse of a right triangle with legs |") + v[0] + "| " + t3("i", "y", "and") + " |" + v[1] + "|.</small>"],
        [t3("Oposat", "Opuesto", "Opposite"), tex("\\overrightarrow{BA}=" + cT([-v[0], -v[1]]))],
        [cdot(COL.p) + t3("Equipol·lent", "Equipolente", "Equivalent"), (A[0] || A[1] ? t3("La fletxa discontínua té origen en ", "La flecha discontinua tiene origen en ", "The dashed arrow starts at ") + tex("O(0,0)") + t3(" i extrem en ", " y extremo en ", " and ends at ") + tex(cT(v)) + t3(": les mateixes components, el mateix vector lliure.", ": las mismas componentes, el mismo vector libre.", ": same components, same free vector.")
          : t3("Ara l'origen és ", "Ahora el origen es ", "Now the initial point is ") + tex("O") + t3(": l'extrem té les mateixes coordenades que el vector.", ": el extremo tiene las mismas coordenadas que el vector.", ": the terminal point has the same coordinates as the vector."))]
      ]);
    }
    P.onChange = draw; onLang(draw);
  }

  /* ---------- 6.4 aplicacions: distància i punt mig, simètric, alineació, paral·lelogram ---------- */
  function wApp() {
    var g = setup("w-app", { A: [-4, -2], B: [1, 1], C: [3, 5] }); if (!g) return;
    var P = g.P, pt = P.pts, mode = 0;
    presetBtns($(g.w, "mode"), function () { return [t3("Distància i punt mig", "Distancia y punto medio", "Distance and midpoint"), t3("Punt simètric", "Punto simétrico", "Symmetric point"), t3("Punts alineats?", "¿Puntos alineados?", "Collinear?"), t3("Paral·lelogram", "Paralelogramo", "Parallelogram")]; },
      function (i) { mode = i; draw(); })[0].classList.add("on");
    function draw() {
      var A = pt.A, B = pt.B, C = pt.C, h = "", rows = [], AB = dv(B, A), m2 = AB[0] * AB[0] + AB[1] * AB[1];
      if (mode === 0) {
        var M = [Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2)];
        h += P.seg(A, B, "var(--text)") + P.dot(M, COL.v, null, "M", [12, 16]);
        h += P.dot(A, COL.r, "A", "A", [-12, -8]) + P.dot(B, COL.r, "B", "B");
        rows.push([tex("\\overrightarrow{AB}"), tex(cT(AB))]);
        rows.push([t3("Distància", "Distancia", "Distance"), tex("d(A,B)=\\sqrt{" + fP(AB[0]) + "^2+" + fP(AB[1]) + "^2}=\\sqrt{" + m2 + "}" + (surd(m2).a > 1 ? "=" + sqT(m2) : "") + sqApprox(m2))]);
        rows.push([cdot(COL.v) + t3("Punt mig", "Punto medio", "Midpoint"), tex("M=\\left(\\frac{" + A[0] + "+" + fP(B[0]) + "}{2},\\frac{" + A[1] + "+" + fP(B[1]) + "}{2}\\right)=" + cT(M))]);
      } else if (mode === 1) {
        var S = [2 * B[0] - A[0], 2 * B[1] - A[1]], inside = Math.abs(S[0]) <= 8 && Math.abs(S[1]) <= 8;
        h += P.arrow(A, B, COL.u, "") + (inside ? P.arrow(B, S, COL.u, "", "d") + P.dot(S, COL.p, null, "A'", [12, -10]) : "");
        h += P.dot(A, COL.r, "A", "A", [-12, -8]) + P.dot(B, "var(--text)", "B", "M");
        rows.push([t3("Centre de simetria", "Centro de simetría", "Centre of symmetry"), tex("M" + cT(B))]);
        rows.push([tex("\\overrightarrow{AM}"), tex(cT(AB))]);
        rows.push([cdot(COL.p) + t3("Simètric", "Simétrico", "Symmetric"), tex("A'=A+2\\,\\overrightarrow{AM}=" + cT(A) + "+" + cT([2 * AB[0], 2 * AB[1]]) + "=" + cT(S))]);
        rows.push(["", "<small>" + t3("M és el punt mig de A i A'.", "M es el punto medio de A y A'.", "M is the midpoint of A and A'.") + (inside ? "" : " " + t3("(A' queda fora del dibuix.)", "(A' queda fuera del dibujo.)", "(A' is off the grid.)")) + "</small>"]);
      } else if (mode === 2) {
        var AC = dv(C, A), cr = AB[0] * AC[1] - AB[1] * AC[0];
        h += cr === 0 ? P.line(A, AB, COL.w) : P.seg(A, B, COL.u) + P.seg(A, C, COL.v) + P.seg(B, C, "var(--muted)", "gd");
        h += P.dot(A, COL.r, "A", "A", [-12, -8]) + P.dot(B, COL.r, "B", "B") + P.dot(C, COL.r, "C", "C");
        rows.push([cdot(COL.u) + tex("\\overrightarrow{AB}"), tex(cT(AB))]);
        rows.push([cdot(COL.v) + tex("\\overrightarrow{AC}"), tex(cT(AC))]);
        rows.push([t3("Proporcionals?", "¿Proporcionales?", "Proportional?"), tex(AB[0] + "\\cdot" + fP(AC[1]) + (cr ? "\\neq" : "=") + fP(AB[1]) + "\\cdot" + fP(AC[0]))]);
        rows.push([t3("Conclusió", "Conclusión", "Conclusion"), cr === 0 ? '<span class="chk ok">' + t3("Alineats", "Alineados", "Collinear") + "</span>" : '<span class="chk no">' + t3("No alineats: formen un triangle", "No alineados: forman un triángulo", "Not collinear: they form a triangle") + "</span>"]);
      } else {
        var BC = dv(C, B), D = [A[0] + BC[0], A[1] + BC[1]], d = AB[0] * BC[0] + AB[1] * BC[1], l1 = m2, l2 = BC[0] * BC[0] + BC[1] * BC[1];
        var degen = AB[0] * BC[1] - AB[1] * BC[0] === 0, inD = Math.abs(D[0]) <= 8 && Math.abs(D[1]) <= 8;
        if (!degen && inD) h += '<path class="tri" d="M' + P.X(A[0]) + " " + P.Y(A[1]) + "L" + P.X(B[0]) + " " + P.Y(B[1]) + "L" + P.X(C[0]) + " " + P.Y(C[1]) + "L" + P.X(D[0]) + " " + P.Y(D[1]) + 'Z"/>';
        h += P.arrow(B, C, COL.v, "") + (inD ? P.arrow(A, D, COL.v, "", "d") + P.dot(D, COL.p, null, "D", [12, -10]) : "");
        h += P.dot(A, COL.r, "A", "A", [-12, -8]) + P.dot(B, COL.r, "B", "B") + P.dot(C, COL.r, "C", "C");
        rows.push([cdot(COL.v) + tex("\\overrightarrow{BC}=\\overrightarrow{AD}"), tex(cT(BC))]);
        rows.push([cdot(COL.p) + t3("Quart vèrtex", "Cuarto vértice", "Fourth vertex"), tex("D=A+\\overrightarrow{BC}=" + cT(D)) + (inD ? "" : " <small>" + t3("(fora del dibuix)", "(fuera del dibujo)", "(off the grid)") + "</small>")]);
        if (degen) rows.push(["", '<p class="msg-bad">' + t3("A, B i C estan alineats: no hi ha paral·lelogram.", "A, B y C están alineados: no hay paralelogramo.", "A, B and C are collinear: no parallelogram.") + "</p>"]);
        else {
          rows.push([t3("Costats", "Lados", "Sides"), tex("|\\overrightarrow{AB}|=" + sqT(l1) + ",\\ |\\overrightarrow{BC}|=" + sqT(l2))]);
          rows.push([tex("\\overrightarrow{AB}\\cdot\\overrightarrow{BC}"), tex(AB[0] + "\\cdot" + fP(BC[0]) + "+" + fP(AB[1]) + "\\cdot" + fP(BC[1]) + "=" + d)]);
          var kind = d === 0 && l1 === l2 ? t3("És un quadrat.", "Es un cuadrado.", "It's a square.") : d === 0 ? t3("És un rectangle (costats perpendiculars).", "Es un rectángulo (lados perpendiculares).", "It's a rectangle (perpendicular sides).") : l1 === l2 ? t3("És un rombe (costats iguals).", "Es un rombo (lados iguales).", "It's a rhombus (equal sides).") : t3("És un paral·lelogram qualsevol.", "Es un paralelogramo cualquiera.", "It's a general parallelogram.");
          rows.push([t3("Tipus", "Tipo", "Type"), '<span class="chk ok">' + kind + "</span>"]);
        }
      }
      P.draw(h);
      g.info.innerHTML = kv(rows);
    }
    P.onChange = draw; onLang(draw);
  }

  /* ---------- 6.2 operacions ---------- */
  function wOps() {
    var g = setup("w-ops", { U: [3, 1], V: [1, 3] }, { lim: 5, ok: function (k, w) { return w[0] || w[1]; } }); if (!g) return;
    var P = g.P, pt = P.pts, mode = 0, kIn = $(g.w, "k"), kv_ = $(g.w, "kv");
    presetBtns($(g.w, "ops"), function () { return [tex("\\vec u+\\vec v"), tex("\\vec u-\\vec v"), tex("k\\,\\vec u"), tex("k\\,\\vec u+\\vec v")]; }, function (i) { mode = i; draw(); })[0].classList.add("on");
    kIn.addEventListener("input", draw);
    function draw() {
      var U = pt.U, V = pt.V, O = [0, 0], k = Fr(Math.round(parseFloat(kIn.value) * 2), 2), kU = [fMul(k, U[0]), fMul(k, U[1])], R, h = "", calc;
      kv_.textContent = decS(fVal(k), 1);
      g.w.querySelector(".wctl").style.opacity = mode >= 2 ? 1 : 0.4;
      if (mode === 0) {
        R = [U[0] + V[0], U[1] + V[1]];
        h += P.arrow(U, R, COL.v, "", "d") + P.arrow(V, R, COL.u, "", "d");
        calc = "\\vec u+\\vec v=" + cT(U) + "+" + cT(V) + "=(" + U[0] + "+" + fP(V[0]) + ",\\," + U[1] + "+" + fP(V[1]) + ")=" + cT(R);
      } else if (mode === 1) {
        R = [U[0] - V[0], U[1] - V[1]];
        h += P.arrow(V, U, COL.w, "", "d");
        calc = "\\vec u-\\vec v=" + cT(U) + "-" + cT(V) + "=(" + U[0] + "-" + fP(V[0]) + ",\\," + U[1] + "-" + fP(V[1]) + ")=" + cT(R);
      } else if (mode === 2) {
        R = kU;
        calc = fT(k) + "\\,\\vec u=" + fT(k) + "\\cdot" + cT(U) + "=" + cT(R);
      } else {
        R = [fAdd(kU[0], V[0]), fAdd(kU[1], V[1])];
        h += P.arrow(O, kU, COL.u, "", "d") + P.arrow(kU, R, COL.v, "", "d");
        calc = fT(k) + "\\,\\vec u+\\vec v=" + cT(kU) + "+" + cT(V) + "=" + cT(R);
      }
      h += P.arrow(O, R, COL.w, mode === 2 ? "k u" : "") + P.arrow(O, U, COL.u, "u") + P.arrow(O, V, COL.v, "v");
      h += P.dot(U, COL.u, "U") + P.dot(V, COL.v, "V");
      P.draw(h);
      var r2 = fAdd(fMul(R[0], R[0]), fMul(R[1], R[1])), rows = [
        [cdot(COL.u) + tex("\\vec u"), tex(cT(U))], [cdot(COL.v) + tex("\\vec v"), tex(cT(V))],
        [cdot(COL.w) + t3("Resultat", "Resultado", "Result"), tex(calc)],
        [t3("Mòdul", "Módulo", "Magnitude"), tex("|\\cdot|=" + (r2.d === 1 ? "\\sqrt{" + r2.n + "}" + (surd(r2.n).a > 1 ? "=" + sqT(r2.n) : "") : "\\sqrt{" + fT(r2) + "}") + "\\approx " + dT(Math.sqrt(fVal(r2))))]
      ];
      if (mode === 2) rows.push(["", "<small>" + (k.n > 0 ? t3("k > 0: mateix sentit que u, ", "k > 0: mismo sentido que u, ", "k > 0: same sense as u, ") : k.n < 0 ? t3("k < 0: sentit contrari a u, ", "k < 0: sentido contrario a u, ", "k < 0: opposite sense to u, ") : t3("k = 0: vector nul. ", "k = 0: vector nulo. ", "k = 0: zero vector. ")) + (k.n ? t3("mòdul multiplicat per |k| = ", "módulo multiplicado por |k| = ", "length multiplied by |k| = ") + decS(Math.abs(fVal(k)), 1) : "") + "</small>"]);
      if (mode === 0) rows.push(["", "<small>" + t3("Regla del paral·lelogram: la suma és la diagonal.", "Regla del paralelogramo: la suma es la diagonal.", "Parallelogram rule: the sum is the diagonal.") + "</small>"]);
      if (mode === 1) rows.push(["", "<small>" + t3("La resta va de la punta de v a la punta de u (línia discontínua).", "La resta va de la punta de v a la punta de u (línea discontinua).", "The difference goes from the tip of v to the tip of u (dashed).") + "</small>"]);
      var cr = U[0] * V[1] - U[1] * V[0];
      rows.push([t3("Paral·lels?", "¿Paralelos?", "Parallel?"), tex("u_1v_2-u_2v_1=" + U[0] + "\\cdot" + fP(V[1]) + "-" + fP(U[1]) + "\\cdot" + fP(V[0]) + "=" + cr) + " " + (cr ? t3("→ no", "→ no", "→ no") : t3("→ sí", "→ sí", "→ yes"))]);
      g.info.innerHTML = kv(rows);
    }
    P.onChange = draw; onLang(draw);
  }

  /* ---------- 6.3 producte escalar ---------- */
  function wDot() {
    var g = setup("w-dot", { U: [4, 2], V: [-1, 2] }, { lim: 7, ok: function (k, w) { return w[0] || w[1]; } }); if (!g) return;
    var P = g.P, pt = P.pts;
    function draw() {
      var U = pt.U, V = pt.V, O = [0, 0], d = U[0] * V[0] + U[1] * V[1], cr = U[0] * V[1] - U[1] * V[0], nu = U[0] * U[0] + U[1] * U[1], nv = V[0] * V[0] + V[1] * V[1];
      var a = deg(Math.acos(Math.max(-1, Math.min(1, d / Math.sqrt(nu * nv)))));
      var a0 = Math.atan2(U[1], U[0]), a1 = Math.atan2(V[1], V[0]), sw = a1 - a0;
      while (sw <= -Math.PI) sw += 2 * Math.PI; while (sw > Math.PI) sw -= 2 * Math.PI;
      var h = P.line(O, U, "var(--muted)", "d");
      if (cr) h += sw >= 0 ? P.arc(O, a0, a1, 26, COL.p, "α") : P.arc(O, a1, a0, 26, COL.p, "α");
      h += P.arrow(O, [-U[1], U[0]], COL.w, "", "d") + P.arrow(O, U, COL.u, "u") + P.arrow(O, V, COL.v, "v") + P.dot(U, COL.u, "U") + P.dot(V, COL.v, "V");
      P.draw(h);
      var kind = cr === 0 ? '<span class="chk ok">' + t3("paral·lels", "paralelos", "parallel") + " " + (d > 0 ? t3("(mateix sentit)", "(mismo sentido)", "(same sense)") : t3("(sentit contrari)", "(sentido contrario)", "(opposite sense)")) + "</span>"
        : d > 0 ? '<span class="chk ok">' + t3("angle agut", "ángulo agudo", "acute angle") + "</span>" : d < 0 ? '<span class="chk no">' + t3("angle obtús", "ángulo obtuso", "obtuse angle") + "</span>" : '<span class="chk ok">' + t3("perpendiculars!", "¡perpendiculares!", "perpendicular!") + "</span>";
      g.info.innerHTML = kv([
        [cdot(COL.u) + tex("\\vec u"), tex(cT(U) + ",\\ |\\vec u|=" + sqT(nu) + sqApprox(nu))],
        [cdot(COL.v) + tex("\\vec v"), tex(cT(V) + ",\\ |\\vec v|=" + sqT(nv) + sqApprox(nv))],
        [tex("\\vec u\\cdot\\vec v"), tex(U[0] + "\\cdot" + fP(V[0]) + "+" + fP(U[1]) + "\\cdot" + fP(V[1]) + "=" + d)],
        [t3("Angle", "Ángulo", "Angle"), tex("\\alpha\\approx" + degT(a)) + " " + kind],
        [t3("Paral·lels?", "¿Paralelos?", "Parallel?"), tex(U[0] + "\\cdot" + fP(V[1]) + (cr ? "\\neq" : "=") + fP(U[1]) + "\\cdot" + fP(V[0]))],
        [cdot(COL.w) + t3("Perpendicular a u", "Perpendicular a u", "Perpendicular to u"), tex(cT([-U[1], U[0]])) + " <small>" + t3("(intercanviem i canviem un signe)", "(intercambiamos y cambiamos un signo)", "(swap and change one sign)") + "</small>"]
      ]);
    }
    P.onChange = draw; onLang(draw);
  }

  /* ---------- 6.5 el paràmetre ---------- */
  function wParam() {
    var g = setup("w-param", { P: [-2, -1], Q: [0, 2] }); if (!g) return;
    var P = g.P, pt = P.pts, lIn = $(g.w, "l"), lv = $(g.w, "lv");
    lIn.addEventListener("input", draw);
    function draw() {
      var A = pt.P, v = dv(pt.Q, A), l = Fr(Math.round(parseFloat(lIn.value) * 2), 2), X = [fAdd(A[0], fMul(l, v[0])), fAdd(A[1], fMul(l, v[1]))];
      lv.textContent = decS(fVal(l), 1);
      var inside = Math.abs(fVal(X[0])) <= 8 && Math.abs(fVal(X[1])) <= 8;
      var h = P.line(A, v, COL.r) + (inside ? P.arrow(A, X, COL.p, "", "d") + P.dot(X, COL.p, null, "X", [12, -10]) : "") + P.arrow(A, pt.Q, COL.v, "v");
      h += P.dot(A, "var(--text)", "P", "P", [-12, -8]) + P.dot(pt.Q, COL.v, "Q");
      P.draw(h);
      var L = "\\lambda";
      g.info.innerHTML = kv([
        [t3("Punt", "Punto", "Point"), tex("P" + cT(A))], [cdot(COL.v) + t3("Director", "Director", "Direction"), tex("\\vec v=" + cT(v))],
        [t3("Vectorial", "Vectorial", "Vector"), tex("(x,y)=" + cT(A) + "+" + L + cT(v))],
        [cdot(COL.p) + tex(L + "=" + fT(l)), tex("X=" + cT(A) + "+" + fP(l) + "\\cdot" + cT(v) + "=" + cT(X)) + (inside ? "" : " <small>" + t3("(fora del dibuix)", "(fuera del dibujo)", "(off the grid)") + "</small>")],
        ["", "<small>" + (l.n > 0 ? t3("λ > 0: X està en el sentit de v.", "λ > 0: X está en el sentido de v.", "λ > 0: X lies in the sense of v.") : l.n < 0 ? t3("λ < 0: X està en sentit contrari a v.", "λ < 0: X está en sentido contrario a v.", "λ < 0: X lies opposite to v.") : t3("λ = 0: X és el punt P.", "λ = 0: X es el punto P.", "λ = 0: X is the point P.")) + "</small>"]
      ]);
    }
    P.onChange = draw; onLang(draw);
  }

  /* ---------- 6.6 pendent ---------- */
  function wSlope() {
    var g = setup("w-slope", { A: [-4, -2], B: [2, 2] }); if (!g) return;
    var P = g.P, pt = P.pts;
    function draw() {
      var A = pt.A, B = pt.B, v = dv(B, A), h = P.line(A, v, COL.r);
      if (v[0]) {
        var m = Fr(v[1], v[0]), n = fSub(A[1], fMul(m, A[0]));
        h += P.seg(A, [B[0], A[1]], COL.v, "ln") + P.seg([B[0], A[1]], B, COL.w, "ln");
        h += P.text([(A[0] + B[0]) / 2, A[1]], "Δx = " + String(v[0]).replace("-", "−"), 0, v[1] > 0 ? 15 : -7, false, COL.v);
        h += P.text([B[0], (A[1] + B[1]) / 2], "Δy = " + String(v[1]).replace("-", "−"), v[0] >= 0 ? 32 : -32, 4, false, COL.w);
        if (Math.abs(fVal(n)) <= 8) h += P.dot([0, n], "var(--muted)", null, "n", [-12, 4]);
        h += P.dot(A, "var(--text)", "A", "A", [-12, -8]) + P.dot(B, "var(--text)", "B", "B");
        P.draw(h);
        var desc = m.n > 0 ? t3("creixent: puja ", "creciente: sube ", "increasing: rises ") + tex(fT(m)) + t3(" per cada unitat cap a la dreta", " por cada unidad hacia la derecha", " for each unit to the right")
          : m.n < 0 ? t3("decreixent: baixa ", "decreciente: baja ", "decreasing: falls ") + tex(fT(Fr(-m.n, m.d))) + t3(" per cada unitat cap a la dreta", " por cada unidad hacia la derecha", " for each unit to the right") : t3("horitzontal", "horizontal", "horizontal");
        g.info.innerHTML = kv([
          [t3("Punts", "Puntos", "Points"), tex("A" + cT(A) + ",\\ B" + cT(B))],
          [t3("Pendent", "Pendiente", "Slope"), tex("m=\\dfrac{\\Delta y}{\\Delta x}=\\dfrac{" + B[1] + "-" + fP(A[1]) + "}{" + B[0] + "-" + fP(A[0]) + "}=\\dfrac{" + v[1] + "}{" + v[0] + "}" + (v[0] === 1 ? "" : "=" + fT(m)))],
          ["", "<small>" + t3("Recta ", "Recta ", "Line ") + desc + ".</small>"],
          [t3("Vector director", "Vector director", "Direction vector"), tex(cT(v) + "\\parallel(1,\\," + fT(m) + ")")],
          [t3("Punt-pendent", "Punto-pendiente", "Point-slope"), tex(poly([[1, "y"], [-A[1], ""]]) + "=" + (m.n === 0 ? "0" : (m.n === m.d ? "" : m.n === -m.d ? "-" : fT(m)) + "(" + poly([[1, "x"], [-A[0], ""]]) + ")"))],
          [t3("Explícita", "Explícita", "Slope-intercept"), tex("y=" + poly([[m, "x"], [n, ""]])) + " <small>" + t3("ordenada en l'origen ", "ordenada en el origen ", "y-intercept ") + tex("n=" + fT(n)) + "</small>"]
        ]);
      } else {
        h += P.dot(A, "var(--text)", "A", "A", [-12, -8]) + P.dot(B, "var(--text)", "B", "B");
        P.draw(h);
        g.info.innerHTML = kv([[t3("Punts", "Puntos", "Points"), tex("A" + cT(A) + ",\\ B" + cT(B))], [t3("Pendent", "Pendiente", "Slope"), tex("\\Delta x=0") + ": " + t3("recta vertical, no té pendent", "recta vertical, no tiene pendiente", "vertical line, no slope")], [t3("Equació", "Ecuación", "Equation"), tex("x=" + A[0])]]);
      }
    }
    P.onChange = draw; onLang(draw);
  }

  /* ---------- 6.6 totes les equacions de la recta ---------- */
  function eqForms(Pp, d) {
    var a = Pp[0], b = Pp[1], u1 = d[0], u2 = d[1], G = lineDir(Pp, d), o = [], L = "\\lambda";
    o.push([t3("Vectorial", "Vectorial", "Vector"), "(x,y)=" + cT(Pp) + "+" + L + cT(d)]);
    o.push([t3("Paramètriques", "Paramétricas", "Parametric"), "\\left\\{\\begin{array}{l}x=" + poly([[a, ""], [u1, L]]) + "\\\\ y=" + poly([[b, ""], [u2, L]]) + "\\end{array}\\right."]);
    if (fVal(u1) !== 0 && fVal(u2) !== 0) o.push([t3("Contínua", "Continua", "Continuous"), "\\dfrac{" + poly([[1, "x"], [fMul(-1, a), ""]]) + "}{" + fT(u1) + "}=\\dfrac{" + poly([[1, "y"], [fMul(-1, b), ""]]) + "}{" + fT(u2) + "}"]);
    else o.push([t3("Contínua", "Continua", "Continuous"), "\\text{" + t3("no es pot escriure (component 0)", "no se puede escribir (componente 0)", "can't be written (a zero component)") + "}"]);
    if (fVal(u1) !== 0) {
      var m = fDiv(u2, u1), n = fSub(b, fMul(m, a));
      o.push([t3("Punt-pendent", "Punto-pendiente", "Point-slope"), poly([[1, "y"], [fMul(-1, b), ""]]) + "=" + (m.n === 0 ? "0" : (m.n === m.d ? "" : m.n === -m.d ? "-" : fT(m)) + "(" + poly([[1, "x"], [fMul(-1, a), ""]]) + ")") + "\\quad(m=" + fT(m) + ")"]);
      o.push([t3("Explícita", "Explícita", "Slope-intercept"), "y=" + poly([[m, "x"], [n, ""]])]);
    } else {
      o.push([t3("Explícita", "Explícita", "Slope-intercept"), "\\text{" + t3("recta vertical: no té pendent", "recta vertical: no tiene pendiente", "vertical line: no slope") + "}"]);
    }
    o.push([t3("General", "General", "General"), G.t + "\\quad\\vec n=(" + G.A + "," + G.B + ")"]);
    return { list: o, G: G };
  }
  function wEq() {
    var g = setup("w-eq", { P: [2, 1], Q: [5, 3], R: [-4, -3] }); if (!g) return;
    var P = g.P, pt = P.pts;
    function draw() {
      var A = pt.P, d = [pt.Q[0] - A[0], pt.Q[1] - A[1]], e = eqForms(A, d), G = e.G, R = pt.R, val = G.A * R[0] + G.B * R[1] + G.C;
      var nrm = [G.A, G.B], sc = 3 / Math.hypot(G.A, G.B);
      var h = P.line(A, d, COL.r) + P.arrow(A, [A[0] + nrm[0] * sc, A[1] + nrm[1] * sc], COL.p, "n", "d") + P.arrow(A, pt.Q, COL.v, "v");
      h += P.dot(A, "var(--text)", "P", "P", [-12, -8]) + P.dot(pt.Q, COL.v, "Q", "", [0, 0]) + P.dot(R, val ? COL.s : COL.w, "R", "Q", [12, -10]);
      P.draw(h);
      g.info.innerHTML = kv([[t3("Punt", "Punto", "Point"), tex("P" + cT(A))], [cdot(COL.v) + t3("Director", "Director", "Direction"), tex("\\vec v=" + cT(d) + (gcd(d[0], d[1]) > 1 ? "\\parallel" + cT(prim(d)) : ""))]]) +
        '<div class="eqs">' + e.list.map(function (x) { return "<div><b>" + x[0] + "</b>" + tex(x[1]) + "</div>"; }).join("") + "</div>" +
        kv([[cdot(val ? COL.s : COL.w) + tex("Q" + cT(R)), tex(G.A + "\\cdot" + fP(R[0]) + (G.B < 0 ? "-" : "+") + Math.abs(G.B) + "\\cdot" + fP(R[1]) + (G.C < 0 ? "-" : "+") + Math.abs(G.C) + "=" + val) + " " +
          (val ? '<span class="chk no">' + tex("Q\\notin r") + "</span>" : '<span class="chk ok">' + tex("Q\\in r") + "</span>")]]);
    }
    P.onChange = draw; onLang(draw);
  }

  /* ---------- 6.7 posicions relatives ---------- */
  function coefRow(box, name, col, vals, onIn) {
    box.innerHTML = '<span class="coef">' + cdot(col) + "<i>" + name + "</i>:&nbsp;" +
      '<input class="tin s" inputmode="numeric" value="' + vals[0] + '"> <i>x</i> + <input class="tin s" inputmode="numeric" value="' + vals[1] + '"> <i>y</i> + <input class="tin s" inputmode="numeric" value="' + vals[2] + '"> = 0</span>';
    var ins = [].slice.call(box.querySelectorAll("input"));
    ins.forEach(function (i) { i.addEventListener("input", onIn); });
    return {
      get: function () {
        var v = ins.map(function (i) { var s = i.value.trim().replace("−", "-"), ok = /^[-+]?\d{1,3}$/.test(s); i.classList.toggle("bad", !ok); return ok ? parseInt(s, 10) : null; });
        return v.indexOf(null) >= 0 || (!v[0] && !v[1]) ? null : v;
      },
      set: function (v) { ins.forEach(function (i, k) { i.value = v[k]; i.classList.remove("bad"); }); }
    };
  }
  function ratio(a, b) { return b ? fT(Fr(a, b)) : (a ? "\\tfrac{" + a + "}{0}" : "\\tfrac{0}{0}"); }
  function wPos() {
    var w = document.getElementById("w-pos"); if (!w) return;
    var P = Plane(w.querySelector("svg.gp-svg"), {}), info = w.querySelector(".info");
    var PRE = [[[3, 4, -5], [1, -3, -6]], [[1, -2, 4], [-2, 4, 4]], [[1, -2, 4], [-2, 4, -8]], [[2, -1, 1], [1, 2, -7]], [[0, 1, -3], [1, 0, 2]]];
    var r1 = coefRow($(w, "r1"), "r", COL.r, PRE[0][0], draw), r2 = coefRow($(w, "r2"), "s", COL.s, PRE[0][1], draw);
    presetBtns($(w, "presets"), function () { return [t3("Secants", "Secantes", "Intersecting"), t3("Paral·leles", "Paralelas", "Parallel"), t3("Coincidents", "Coincidentes", "Coincident"), t3("Perpendiculars", "Perpendiculares", "Perpendicular"), t3("Paral·leles als eixos", "Paralelas a los ejes", "Parallel to the axes")]; },
      function (i) { r1.set(PRE[i][0]); r2.set(PRE[i][1]); draw(); })[0].classList.add("on");
    function draw() {
      var a = r1.get(), b = r2.get();
      if (!a || !b) { info.innerHTML = '<p class="msg-bad">' + t3("Escriu coeficients enters (A i B no poden ser tots dos 0).", "Escribe coeficientes enteros (A y B no pueden ser los dos 0).", "Type whole-number coefficients (A and B can't both be 0).") + "</p>"; P.draw(""); return; }
      var R = { A: a[0], B: a[1], C: a[2] }, S = { A: b[0], B: b[1], C: b[2] }, X = inter(R, S), h = P.gline(R, COL.r) + P.gline(S, COL.s, X ? "" : "d");
      var rows = [[t3("Quocients", "Cocientes", "Ratios"), tex("\\frac{A}{A'}=" + ratio(a[0], b[0]) + ",\\ \\ \\frac{B}{B'}=" + ratio(a[1], b[1]) + ",\\ \\ \\frac{C}{C'}=" + ratio(a[2], b[2]))]];
      var dot = a[0] * b[0] + a[1] * b[1];
      if (X) {
        h += P.dot(X, "var(--text)", null, "", [0, 0]);
        rows.push([t3("Posició", "Posición", "Position"), '<span class="chk ok">' + t3("Secants", "Secantes", "Intersecting") + "</span>" + (dot === 0 ? " " + t3("i perpendiculars", "y perpendiculares", "and perpendicular") + " " + tex("(\\vec n_r\\cdot\\vec n_s=0)") : "")]);
        rows.push([t3("Punt de tall", "Punto de corte", "Intersection"), tex(cT(X))]);
        rows.push(["", "<small>" + t3("Solució del sistema (compatible determinat).", "Solución del sistema (compatible determinado).", "Solution of the system (one solution).") + "</small>"]);
      } else {
        var coin = a[0] * b[2] === b[0] * a[2] && a[1] * b[2] === b[1] * a[2];
        rows.push([t3("Posició", "Posición", "Position"), coin ? '<span class="chk ok">' + t3("Coincidents", "Coincidentes", "Coincident") + "</span> " + tex("r\\equiv s")
          : '<span class="chk no">' + t3("Paral·leles", "Paralelas", "Parallel") + "</span> " + tex("r\\parallel s")]);
        rows.push(["", "<small>" + (coin ? t3("Els tres coeficients són proporcionals: és la mateixa recta (infinites solucions).", "Los tres coeficientes son proporcionales: es la misma recta (infinitas soluciones).", "All three coefficients are proportional: it's the same line (infinitely many solutions).")
          : t3("A i B són proporcionals però C no: el sistema és incompatible.", "A y B son proporcionales pero C no: el sistema es incompatible.", "A and B are proportional but C isn't: the system has no solution.")) + "</small>"]);
      }
      P.draw(h);
      info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 6.8 paral·lela i perpendicular ---------- */
  function wPar() {
    var g = setup("w-par", { A: [-6, -2], B: [4, 3], P: [-3, 5] }); if (!g) return;
    var P = g.P, pt = P.pts;
    function draw() {
      var d = sub(pt.B, pt.A), R = lineDir(pt.A, d), Pp = pt.P, par = lineNormal(Pp, [R.A, R.B]), per = lineNormal(Pp, [R.B, -R.A]), H = inter(R, per);
      var h = P.gline(R, COL.r) + P.gline(par, COL.w, "d") + P.gline(per, COL.v);
      if (H) h += P.dot(H, COL.v, null, "", [0, 0]);
      h += P.dot(pt.A, COL.r, "A", "A", [-12, -8]) + P.dot(pt.B, COL.r, "B", "B") + P.dot(Pp, "var(--text)", "P", "P");
      P.draw(h);
      var m = R.B ? fT(Fr(-R.A, R.B)) : null;
      g.info.innerHTML = kv([
        [cdot(COL.r) + "r", tex(R.t)],
        ["", "<small>" + tex("\\vec n_r=(" + R.A + "," + R.B + "),\\ \\vec u_r=(" + -R.B + "," + R.A + ")" + (m !== null ? ",\\ m_r=" + m : "")) + "</small>"],
        [cdot(COL.w) + t3("Paral·lela per P", "Paralela por P", "Parallel through P"), tex(par.t)],
        ["", "<small>" + tex(poly([[R.A, "x"], [R.B, "y"]]) + "+K=0,\\ \\ K=" + par.C) + "</small>"],
        [cdot(COL.v) + t3("Perpendicular per P", "Perpendicular por P", "Perpendicular through P"), tex(per.t)],
        ["", "<small>" + t3("El vector normal de r és un vector director de la perpendicular", "El vector normal de r es un vector director de la perpendicular", "The normal vector of r is a direction vector of the perpendicular") + (m !== null && R.A ? "; " + tex("m'=-\\dfrac{1}{m_r}=" + fT(Fr(R.B, R.A))) : "") + ".</small>"],
        [t3("Peu de la perpendicular", "Pie de la perpendicular", "Foot of the perpendicular"), H ? tex(cT(H)) : "—"]
      ]);
    }
    P.onChange = draw; onLang(draw);
  }

  /* ---------- 6.8 mediatriu ---------- */
  function wMed() {
    var g = setup("w-med", { A: [-4, 3], B: [4, -1], X: [3, 6] }); if (!g) return;
    var P = g.P, pt = P.pts;
    function draw() {
      var A = pt.A, B = pt.B, X = pt.X, AB = dv(B, A), M = [Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2)], med = lineNormal(M, AB);
      var dA = Math.pow(X[0] - A[0], 2) + Math.pow(X[1] - A[1], 2), dB = Math.pow(X[0] - B[0], 2) + Math.pow(X[1] - B[1], 2), on = dA === dB;
      var h = P.seg(A, B, "var(--text)") + P.gline(med, COL.p) + P.seg(X, A, on ? COL.w : COL.u, "gd") + P.seg(X, B, on ? COL.w : COL.v, "gd");
      h += P.dot(M, COL.p, null, "M", [12, 16]) + P.dot(A, COL.r, "A", "A", [-12, -8]) + P.dot(B, COL.r, "B", "B") + P.dot(X, on ? COL.w : "var(--text)", "X", "X");
      P.draw(h);
      g.info.innerHTML = kv([
        [t3("Punt mig", "Punto medio", "Midpoint"), tex("M=" + cT(M))],
        [t3("Vector normal", "Vector normal", "Normal vector"), tex("\\overrightarrow{AB}=" + cT(AB) + (gcd(AB[0], AB[1]) > 1 ? "\\parallel" + cT(prim(AB)) : ""))],
        [cdot(COL.p) + t3("Mediatriu", "Mediatriz", "Bisector"), tex(med.t)],
        [tex("X" + cT(X)), tex("d(X,A)=\\sqrt{" + dA + "}" + sqApprox(dA) + ",\\ d(X,B)=\\sqrt{" + dB + "}" + sqApprox(dB))],
        ["", on ? '<span class="chk ok">' + t3("X és de la mediatriu: equidista de A i B", "X está en la mediatriz: equidista de A y B", "X is on the bisector: equidistant from A and B") + "</span>" : "<small>" + t3("Porta X a la recta lila: les dues distàncies seran iguals.", "Lleva X a la recta lila: las dos distancias serán iguales.", "Move X onto the purple line: both distances will match.") + "</small>"]
      ]);
    }
    P.onChange = draw; onLang(draw);
  }
  /* ---------- laboratori del triangle ---------- */
  function wLab() {
    var w = document.getElementById("w-lab"); if (!w) return;
    var pts = { A: [-5, -3], B: [6, -2], C: [1, 6] }, P = Plane(w.querySelector("svg.gp-svg"), { pts: pts }), out = $(w, "out"), kind = 0, ins = {};
    P.ok = diff("w-lab", pts);
    var box = $(w, "pts");
    ["A", "B", "C"].forEach(function (k) {
      var s = document.createElement("span"); s.className = "ptin";
      s.innerHTML = "<i>" + k + "</i>(" + '<input class="tin s" inputmode="numeric">' + "," + '<input class="tin s" inputmode="numeric">' + ")";
      box.appendChild(s);
      ins[k] = [].slice.call(s.querySelectorAll("input"));
      ins[k].forEach(function (inp, j) {
        inp.addEventListener("input", function () {
          var v = inp.value.trim().replace("−", "-"), ok = /^-?\d{1,2}$/.test(v) && Math.abs(+v) <= 8;
          inp.classList.toggle("bad", !ok);
          if (ok) { var c = pts[k].slice(); c[j] = +v; if (P.ok(k, c)) { pts[k] = c; draw(true); } else inp.classList.add("bad"); }
        });
      });
    });
    presetBtns($(w, "kind"), function () { return [t3("Només el triangle", "Solo el triángulo", "Triangle only"), t3("Mitjanes i baricentre", "Medianas y baricentro", "Medians and centroid"), t3("Altures i ortocentre", "Alturas y ortocentro", "Altitudes and orthocentre"), t3("Mediatrius i circumcentre", "Mediatrices y circuncentro", "Perpendicular bisectors and circumcentre")]; },
      function (i) { kind = i; draw(); })[0].classList.add("on");
    function ang(p, q, s) { var a = sub(q, p).map(fVal), b = sub(s, p).map(fVal); return deg(Math.acos((a[0] * b[0] + a[1] * b[1]) / Math.hypot(a[0], a[1]) / Math.hypot(b[0], b[1]))); }
    function d2(p, q) { return Math.pow(p[0] - q[0], 2) + Math.pow(p[1] - q[1], 2); }
    function draw(fromInput) {
      var A = pts.A, B = pts.B, C = pts.C;
      if (fromInput !== true) ["A", "B", "C"].forEach(function (k) { ins[k].forEach(function (inp, j) { inp.value = pts[k][j]; inp.classList.remove("bad"); }); });
      var det = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0]);
      var tri = '<path class="tri" d="M' + P.X(A[0]) + " " + P.Y(A[1]) + "L" + P.X(B[0]) + " " + P.Y(B[1]) + "L" + P.X(C[0]) + " " + P.Y(C[1]) + 'Z"/>', h = tri, rows = [];
      if (!det) {
        P.draw(h + P.dot(A, COL.r, "A", "A") + P.dot(B, COL.r, "B", "B") + P.dot(C, COL.r, "C", "C"));
        out.innerHTML = '<p class="msg-bad">' + t3("Els tres punts estan alineats: no formen un triangle.", "Los tres puntos están alineados: no forman un triángulo.", "The three points are collinear: they don't form a triangle.") + "</p>";
        return;
      }
      var c2 = d2(A, B), a2 = d2(B, C), b2 = d2(C, A), aA = ang(A, B, C), aB = ang(B, C, A), aC = 180 - aA - aB;
      var sides = [[lineDir(A, sub(B, A)), "AB"], [lineDir(B, sub(C, B)), "BC"], [lineDir(C, sub(A, C)), "CA"]];
      var dots = [(B[0] - A[0]) * (C[0] - A[0]) + (B[1] - A[1]) * (C[1] - A[1]), (A[0] - B[0]) * (C[0] - B[0]) + (A[1] - B[1]) * (C[1] - B[1]), (A[0] - C[0]) * (B[0] - C[0]) + (A[1] - C[1]) * (B[1] - C[1])];
      var tA = dots.some(function (x) { return x === 0; }) ? t3("rectangle", "rectángulo", "right-angled") : dots.some(function (x) { return x < 0; }) ? t3("obtusangle", "obtusángulo", "obtuse") : t3("acutangle", "acutángulo", "acute");
      var tS = a2 === b2 && b2 === c2 ? t3("equilàter", "equilátero", "equilateral") : a2 === b2 || b2 === c2 || a2 === c2 ? t3("isòsceles", "isósceles", "isosceles") : t3("escalè", "escaleno", "scalene");
      rows.push([t3("Vectors", "Vectores", "Vectors"), tex("\\overrightarrow{AB}=" + cT(sub(B, A)) + ",\\ \\overrightarrow{BC}=" + cT(sub(C, B)) + ",\\ \\overrightarrow{CA}=" + cT(sub(A, C)))]);
      rows.push([t3("Costats", "Lados", "Sides"), tex("c=|AB|=" + sqT(c2) + sqApprox(c2) + "\\\\ a=|BC|=" + sqT(a2) + sqApprox(a2) + "\\\\ b=|CA|=" + sqT(b2) + sqApprox(b2))]);
      rows.push([t3("Tipus", "Tipo", "Type"), t3("Triangle ", "Triángulo ", "") + tS + ", " + tA + (lang === "en" ? " triangle" : "")]);
      rows.push([t3("Perímetre", "Perímetro", "Perimeter"), tex("\\approx " + dT(Math.sqrt(a2) + Math.sqrt(b2) + Math.sqrt(c2)) + "\\ \\text{u}")]);
      rows.push([t3("Àrea", "Área", "Area"), tex(fT(Fr(Math.abs(det), 2)) + "\\ \\text{u}^2")]);
      rows.push([t3("Rectes dels costats", "Rectas de los lados", "Side lines"), tex(sides.map(function (s) { return s[1] + ":\\ " + s[0].t; }).join("\\\\ "))]);
      var L3 = [], X = null, nm = "", col = COL.v;
      if (kind === 1) {
        L3 = [[A, [fDiv(B[0] + C[0], 2), fDiv(B[1] + C[1], 2)]], [B, [fDiv(C[0] + A[0], 2), fDiv(C[1] + A[1], 2)]], [C, [fDiv(A[0] + B[0], 2), fDiv(A[1] + B[1], 2)]]].map(function (q) { return lineDir(q[0], sub(q[1], q[0])); });
        X = [Fr(A[0] + B[0] + C[0], 3), Fr(A[1] + B[1] + C[1], 3)]; nm = "G"; col = COL.w;
      } else if (kind === 2) {
        L3 = [lineNormal(A, sub(C, B)), lineNormal(B, sub(A, C)), lineNormal(C, sub(B, A))]; X = inter(L3[0], L3[1]); nm = "H"; col = COL.v;
      } else if (kind === 3) {
        L3 = [[A, B], [B, C], [C, A]].map(function (q) { return lineNormal([fDiv(q[0][0] + q[1][0], 2), fDiv(q[0][1] + q[1][1], 2)], sub(q[1], q[0])); }); X = inter(L3[0], L3[1]); nm = "O"; col = COL.p;
      }
      L3.forEach(function (l) { h += P.gline(l, col, "d"); });
      if (kind === 3 && X) {
        var rpx = Math.hypot(fVal(X[0]) - A[0], fVal(X[1]) - A[1]) * (P.X(1) - P.X(0));
        h += '<circle cx="' + P.X(fVal(X[0])) + '" cy="' + P.Y(fVal(X[1])) + '" r="' + rpx.toFixed(1) + '" class="arc" style="stroke:' + col + ';stroke-dasharray:2 4"/>';
      }
      if (X) h += P.dot(X, col, null, nm, [12, -10]);
      h += P.dot(A, COL.r, "A", "A", [-12, -8]) + P.dot(B, COL.r, "B", "B") + P.dot(C, COL.r, "C", "C");
      P.draw(h);
      if (kind) {
        var names = [[t3("Mitjanes", "Medianas", "Medians"), t3("Baricentre", "Baricentro", "Centroid")], [t3("Altures", "Alturas", "Altitudes"), t3("Ortocentre", "Ortocentro", "Orthocentre")], [t3("Mediatrius", "Mediatrices", "Perpendicular bisectors"), t3("Circumcentre", "Circuncentro", "Circumcentre")]][kind - 1];
        rows.push([cdot(col) + names[0], tex(L3.map(function (l) { return l.t; }).join("\\\\ "))]);
        rows.push([cdot(col) + names[1], tex(nm + cT(X)) + (kind === 3 ? "<br><small>" + t3("Radi de la circumferència circumscrita: ", "Radio de la circunferencia circunscrita: ", "Circumradius: ") + tex("R\\approx " + dT(Math.hypot(fVal(X[0]) - A[0], fVal(X[1]) - A[1]))) + "</small>" : kind === 1 ? "<br><small>" + tex("G=\\left(\\frac{a_1+b_1+c_1}{3},\\frac{a_2+b_2+c_2}{3}\\right)") + "</small>" : "")]);
      }
      out.innerHTML = kv(rows);
    }
    P.onChange = draw; onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("Si $A(2,-1)$ i $B(-1,3)$, el vector $\\overrightarrow{AB}$ és…", "Si $A(2,-1)$ y $B(-1,3)$, el vector $\\overrightarrow{AB}$ es…", "If $A(2,-1)$ and $B(-1,3)$, the vector $\\overrightarrow{AB}$ is…"),
      o: [q3("$(3,-4)$"), q3("$(-3,4)$"), q3("$(1,2)$")], a: 1, e: q3("Extrem menys origen: $(-1-2,\\ 3-(-1))=(-3,4)$.", "Extremo menos origen: $(-1-2,\\ 3-(-1))=(-3,4)$.", "Terminal minus initial point: $(-1-2,\\ 3-(-1))=(-3,4)$.") },
    { q: q3("El mòdul de $\\vec v=(-6,8)$ és…", "El módulo de $\\vec v=(-6,8)$ es…", "The magnitude of $\\vec v=(-6,8)$ is…"),
      o: [q3("$2$"), q3("$14$"), q3("$10$")], a: 2, e: q3("$\\sqrt{36+64}=\\sqrt{100}=10$.") },
    { q: q3("El vector $\\vec v=(3,-2)$ té l'origen en $P(1,4)$. El seu extrem és…", "El vector $\\vec v=(3,-2)$ tiene el origen en $P(1,4)$. Su extremo es…", "The vector $\\vec v=(3,-2)$ starts at $P(1,4)$. Its terminal point is…"),
      o: [q3("$(4,2)$"), q3("$(-2,6)$"), q3("$(2,-6)$")], a: 0, e: q3("Extrem $=P+\\vec v=(1+3,\\ 4-2)=(4,2)$.", "Extremo $=P+\\vec v=(1+3,\\ 4-2)=(4,2)$.", "Terminal point $=P+\\vec v=(1+3,\\ 4-2)=(4,2)$.") },
    { q: q3("Si $\\vec u=(1,-2)$ i $\\vec v=(3,1)$, el vector $2\\vec u-\\vec v$ és…", "Si $\\vec u=(1,-2)$ y $\\vec v=(3,1)$, el vector $2\\vec u-\\vec v$ es…", "If $\\vec u=(1,-2)$ and $\\vec v=(3,1)$, the vector $2\\vec u-\\vec v$ is…"),
      o: [q3("$(5,-3)$"), q3("$(-1,-5)$"), q3("$(-1,-3)$")], a: 1, e: q3("$(2,-4)-(3,1)=(-1,-5)$.") },
    { q: q3("Els vectors $\\vec u=(4,-6)$ i $\\vec v=(3,2)$ són…", "Los vectores $\\vec u=(4,-6)$ y $\\vec v=(3,2)$ son…", "The vectors $\\vec u=(4,-6)$ and $\\vec v=(3,2)$ are…"),
      o: [q3("paral·lels", "paralelos", "parallel"), q3("perpendiculars", "perpendiculares", "perpendicular"), q3("ni una cosa ni l'altra", "ni una cosa ni la otra", "neither")], a: 1, e: q3("$\\vec u\\cdot\\vec v=12-12=0$.") },
    { q: q3("Un vector perpendicular a $(5,-2)$ és…", "Un vector perpendicular a $(5,-2)$ es…", "A vector perpendicular to $(5,-2)$ is…"),
      o: [q3("$(-5,2)$"), q3("$(2,-5)$"), q3("$(2,5)$")], a: 2, e: q3("Intercanviem les components i canviem un signe: $(2,5)$. Comprovació: $10-10=0$.", "Intercambiamos las componentes y cambiamos un signo: $(2,5)$. Comprobación: $10-10=0$.", "Swap the components and change one sign: $(2,5)$. Check: $10-10=0$.") },
    { q: q3("El punt mig de $A(-2,5)$ i $B(6,1)$ és…", "El punto medio de $A(-2,5)$ y $B(6,1)$ es…", "The midpoint of $A(-2,5)$ and $B(6,1)$ is…"),
      o: [q3("$(2,3)$"), q3("$(4,6)$"), q3("$(4,-2)$")], a: 0, e: q3("$\\left(\\frac{-2+6}{2},\\frac{5+1}{2}\\right)=(2,3)$.") },
    { q: q3("La distància entre $A(1,1)$ i $B(4,5)$ és…", "La distancia entre $A(1,1)$ y $B(4,5)$ es…", "The distance between $A(1,1)$ and $B(4,5)$ is…"),
      o: [q3("$7$"), q3("$5$"), q3("$\\sqrt7$")], a: 1, e: q3("$\\overrightarrow{AB}=(3,4)$, $\\sqrt{9+16}=5$.") },
    { q: q3("Els punts $A(0,1)$, $B(2,5)$ i $C(3,7)$…", "Los puntos $A(0,1)$, $B(2,5)$ y $C(3,7)$…", "The points $A(0,1)$, $B(2,5)$ and $C(3,7)$…"),
      o: [q3("estan alineats", "están alineados", "are collinear"), q3("formen un triangle", "forman un triángulo", "form a triangle")], a: 0, e: q3("$\\overrightarrow{AB}=(2,4)$ i $\\overrightarrow{AC}=(3,6)$ són proporcionals: $\\frac23=\\frac46$.", "$\\overrightarrow{AB}=(2,4)$ y $\\overrightarrow{AC}=(3,6)$ son proporcionales: $\\frac23=\\frac46$.", "$\\overrightarrow{AB}=(2,4)$ and $\\overrightarrow{AC}=(3,6)$ are proportional: $\\frac23=\\frac46$.") },
    { q: q3("Un punt i un vector director de $\\dfrac{x+3}{2}=\\dfrac{y-1}{-5}$ són…", "Un punto y un vector director de $\\dfrac{x+3}{2}=\\dfrac{y-1}{-5}$ son…", "A point and a direction vector of $\\dfrac{x+3}{2}=\\dfrac{y-1}{-5}$ are…"),
      o: [q3("$(3,-1)$ i $(2,-5)$", "$(3,-1)$ y $(2,-5)$", "$(3,-1)$ and $(2,-5)$"), q3("$(-3,1)$ i $(2,-5)$", "$(-3,1)$ y $(2,-5)$", "$(-3,1)$ and $(2,-5)$"), q3("$(-3,1)$ i $(-5,2)$", "$(-3,1)$ y $(-5,2)$", "$(-3,1)$ and $(-5,2)$")], a: 1, e: q3("$x-(-3)$ i $y-1$: el punt és $(-3,1)$; els denominadors formen el vector $(2,-5)$.", "$x-(-3)$ e $y-1$: el punto es $(-3,1)$; los denominadores forman el vector $(2,-5)$.", "$x-(-3)$ and $y-1$: the point is $(-3,1)$; the denominators give the vector $(2,-5)$.") },
    { q: q3("El pendent de la recta que passa per $(1,2)$ i $(3,8)$ és…", "La pendiente de la recta que pasa por $(1,2)$ y $(3,8)$ es…", "The slope of the line through $(1,2)$ and $(3,8)$ is…"),
      o: [q3("$3$"), q3("$\\frac13$"), q3("$5$")], a: 0, e: q3("$m=\\frac{8-2}{3-1}=\\frac62=3$.") },
    { q: q3("Un vector director de la recta $3x-2y+5=0$ és…", "Un vector director de la recta $3x-2y+5=0$ es…", "A direction vector of the line $3x-2y+5=0$ is…"),
      o: [q3("$(3,-2)$"), q3("$(2,3)$"), q3("$(-2,3)$")], a: 1, e: q3("$(A,B)=(3,-2)$ és el vector normal; un director és $(-B,A)=(2,3)$.", "$(A,B)=(3,-2)$ es el vector normal; un director es $(-B,A)=(2,3)$.", "$(A,B)=(3,-2)$ is the normal vector; a direction vector is $(-B,A)=(2,3)$.") },
    { q: q3("L'ordenada en l'origen de $2x+y-6=0$ és…", "La ordenada en el origen de $2x+y-6=0$ es…", "The $y$-intercept of $2x+y-6=0$ is…"),
      o: [q3("$-6$"), q3("$3$"), q3("$6$")], a: 2, e: q3("Aïllant, $y=-2x+6$: $n=6$.", "Despejando, $y=-2x+6$: $n=6$.", "Solving, $y=-2x+6$: $n=6$.") },
    { q: q3("El punt $(2,-1)$ és de la recta $x+3y+1=0$?", "¿El punto $(2,-1)$ está en la recta $x+3y+1=0$?", "Is the point $(2,-1)$ on the line $x+3y+1=0$?"),
      o: [q3("Sí", "Sí", "Yes"), q3("No")], a: 0, e: q3("$2+3\\cdot(-1)+1=0$ ✓") },
    { q: q3("Les rectes $2x-y+3=0$ i $-4x+2y+1=0$ són…", "Las rectas $2x-y+3=0$ y $-4x+2y+1=0$ son…", "The lines $2x-y+3=0$ and $-4x+2y+1=0$ are…"),
      o: [q3("secants", "secantes", "intersecting"), q3("paral·leles", "paralelas", "parallel"), q3("coincidents", "coincidentes", "coincident")], a: 1, e: q3("$\\frac{2}{-4}=\\frac{-1}{2}\\neq\\frac31$.") },
    { q: q3("La recta perpendicular a $y=2x+1$ que passa per l'origen és…", "La recta perpendicular a $y=2x+1$ que pasa por el origen es…", "The line perpendicular to $y=2x+1$ through the origin is…"),
      o: [q3("$y=-2x$"), q3("$y=\\frac12x$"), q3("$y=-\\frac12x$")], a: 2, e: q3("$m'=-\\frac{1}{m}=-\\frac12$, i passa per $(0,0)$.", "$m'=-\\frac{1}{m}=-\\frac12$, y pasa por $(0,0)$.", "$m'=-\\frac{1}{m}=-\\frac12$, through $(0,0)$.") },
    { q: q3("Una recta paral·lela a $x-4y+2=0$ és…", "Una recta paralela a $x-4y+2=0$ es…", "A line parallel to $x-4y+2=0$ is…"),
      o: [q3("$4x+y-7=0$"), q3("$x-4y-7=0$"), q3("$x+4y+2=0$")], a: 1, e: q3("Només canvia el terme independent: $x-4y+K=0$.", "Solo cambia el término independiente: $x-4y+K=0$.", "Only the constant term changes: $x-4y+K=0$.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Vectors i rectes · FentMates", es: "Vectores y rectas · FentMates", en: "Vectors and lines · FentMates" };
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
      document.querySelectorAll(".widget .wt, .widget label, .widget .legend, .widget > p").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wVec, wOps, wDot, wApp, wParam, wSlope, wEq, wPos, wPar, wMed, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM46 = { Fr: Fr, gen: gen, lineDir: lineDir, lineNormal: lineNormal, inter: inter, eqForms: eqForms };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
