(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-3eso-u7-done", NSEC = 8;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc",
      bad: "No entenc la fórmula. Escriu-la amb la x, per exemple: x^2-3x+1, 2x+5, 12/x o sqrt(x+4).",
      badx: "Escriu un valor de x (un nombre).", num: "Escriu un nombre (pots fer servir coma decimal o una fracció com 5/2).",
      pair: "Escriu el punt com (2, −3) o bé 2; −3.", sol: "Solució:" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro",
      bad: "No entiendo la fórmula. Escríbela con la x, por ejemplo: x^2-3x+1, 2x+5, 12/x o sqrt(x+4).",
      badx: "Escribe un valor de x (un número).", num: "Escribe un número (puedes usar coma decimal o una fracción como 5/2).",
      pair: "Escribe el punto como (2, −3) o bien 2; −3.", sol: "Solución:" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Score", right: "Correct!", wrong: "Not correct.", theme: "Switch between light and dark mode",
      bad: "I can't read the formula. Write it in x, for example: x^2-3x+1, 2x+5, 12/x or sqrt(x+4).",
      badx: "Type a value of x (a number).", num: "Type a number (decimals or a fraction like 5/2 are fine).",
      pair: "Type the point as (2, −3) or 2; −3.", sol: "Solution:" }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  function T(o) { return o[lang] || o.va; }
  function L3(va, es, en) { return { va: va, es: es, en: en }; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return k in o ? o[k] : m; }); }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var MACROS = { "\\dc": "\\htmlClass{dc}{{,}}", "\\tri": "\\htmlClass{lva}{\\text{#1}}\\htmlClass{les}{\\text{#2}}\\htmlClass{len}{\\text{#3}}" };
  var KOPT = { throwOnError: false, strict: "ignore", macros: MACROS, trust: function (c) { return c.command === "\\htmlClass"; } };
  function tex(s, display) {
    try { return window.katex.renderToString(display ? s : "\\displaystyle " + s, { throwOnError: false, strict: "ignore", displayMode: !!display, macros: MACROS, trust: KOPT.trust }); } catch (e) { return s; }
  }
  function rtex(s) { return s.replace(/\$([^$]+)\$/g, function (_, m) { return tex(m); }); }
  function segBind(w, cb) {
    var bs = w.querySelectorAll(".seg button");
    bs.forEach(function (b) { b.addEventListener("click", function () { bs.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); cb(b.dataset.k); }); });
  }
  function warn(s) { return '<span class="warn">' + s + "</span>"; }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function rnz(a, b) { var k; do { k = rint(a, b); } while (k === 0); return k; }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = rint(0, i), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function inputs(w) { var o = {}; w.querySelectorAll(".tin[data-k]").forEach(function (i) { o[i.dataset.k] = i; }); return o; }
  function quickBind(w, cb) { w.querySelectorAll(".quick button[data-b]").forEach(function (b) { b.addEventListener("click", function () { cb(b.dataset.b.split("|"), b); }); }); }
  function rows2html(rows) { return rows.map(function (x) { return '<div class="hrow">' + x + "</div>"; }).join(""); }

  /* ---------- nombres ---------- */
  var INF = Infinity;
  function near(a, b) { return Math.abs(a - b) < 1e-9; }
  /* nombre en TeX amb coma decimal (com a molt 3 decimals) */
  function nf(v) {
    if (v === INF) return "+\\infty"; if (v === -INF) return "-\\infty";
    var r = Math.round(v * 1000) / 1000; if (near(r, 0)) r = 0;
    return String(r).replace(".", "\\dc ");
  }
  function nfp(v) { return v < 0 ? "(" + nf(v) + ")" : nf(v); }
  /* nombre escrit per l'alumne: "−3", "2,5", "5/2" */
  function numIn(raw) {
    var s = String(raw).replace(/[−–]/g, "-").replace(/\s+/g, "").replace(",", ".");
    var m = s.match(/^(-?\d+(?:\.\d+)?)(?:\/(\d+(?:\.\d+)?))?$/);
    if (!m) return null;
    var v = parseFloat(m[1]); if (m[2]) { if (+m[2] === 0) return null; v /= parseFloat(m[2]); }
    return v;
  }
  function pairIn(raw) {
    var s = String(raw).replace(/[−–]/g, "-").replace(/[()\s]/g, "");
    var parts = s.indexOf(";") >= 0 ? s.split(";") : s.split(/,(?!\d)/);
    if (parts.length !== 2) { var m = s.match(/^(-?\d+),(-?\d+)$/); if (m) parts = [m[1], m[2]]; else return null; }
    var a = numIn(parts[0]), b = numIn(parts[1]);
    return a === null || b === null ? null : [a, b];
  }

  /* ---------- expressions: lectura, valor i TeX ---------- */
  function lex(s) {
    s = s.replace(/[−–]/g, "-").replace(/[·×]/g, "*").replace(/÷/g, "/").replace(/²/g, "^2").replace(/³/g, "^3").replace(/\s+/g, "").toLowerCase();
    var out = [], i = 0, m;
    while (i < s.length) {
      var r = s.slice(i);
      if ((m = r.match(/^\d+(?:[.,]\d+)?/))) { out.push({ t: "n", v: parseFloat(m[0].replace(",", ".")), s: m[0] }); i += m[0].length; }
      else if ((m = r.match(/^(sqrt|arrel|raiz|raíz|√)/))) { out.push({ t: "f" }); i += m[0].length; }
      else if (r[0] === "x") { out.push({ t: "x" }); i++; }
      else if ("+-*/^()".indexOf(r[0]) >= 0) { out.push({ t: r[0] }); i++; }
      else return null;
    }
    return out;
  }
  function parseExpr(raw) {
    var tk = lex(raw); if (!tk || !tk.length) return null;
    var i = 0;
    function peek() { return tk[i] ? tk[i].t : null; }
    function expr() {
      var a = term();
      while (peek() === "+" || peek() === "-") { var op = tk[i++].t; a = { t: op, a: a, b: term() }; }
      return a;
    }
    function term() {
      var a = unary();
      for (;;) {
        var p = peek();
        if (p === "*" || p === "/") { i++; a = { t: p, a: a, b: unary() }; }
        else if (p === "n" || p === "x" || p === "(" || p === "f") a = { t: "*", a: a, b: power(), imp: true };
        else return a;
      }
    }
    function unary() { if (peek() === "-") { i++; return { t: "neg", a: unary() }; } if (peek() === "+") { i++; return unary(); } return power(); }
    function power() { var a = atom(); if (peek() === "^") { i++; a = { t: "^", a: a, b: unary() }; } return a; }
    function atom() {
      var k = tk[i++]; if (!k) throw 0;
      if (k.t === "n") return { t: "n", v: k.v };
      if (k.t === "x") return { t: "x" };
      if (k.t === "(") { var e = expr(); if (peek() !== ")") throw 0; i++; return { t: "()", a: e }; }
      if (k.t === "f") { var b = power(); return { t: "sqrt", a: b.t === "()" ? b.a : b }; }
      throw 0;
    }
    try { var e = expr(); return i === tk.length ? e : null; } catch (err) { return null; }
  }
  function ev(e, x) {
    switch (e.t) {
      case "n": return e.v; case "x": return x; case "()": return ev(e.a, x); case "neg": return -ev(e.a, x);
      case "+": return ev(e.a, x) + ev(e.b, x); case "-": return ev(e.a, x) - ev(e.b, x);
      case "*": return ev(e.a, x) * ev(e.b, x);
      case "/": var d = ev(e.b, x); return Math.abs(d) < 1e-12 ? NaN : ev(e.a, x) / d;
      case "^": return Math.pow(ev(e.a, x), ev(e.b, x));
      case "sqrt": var r = ev(e.a, x); return r < -1e-12 ? NaN : Math.sqrt(Math.max(r, 0));
    }
    return NaN;
  }
  /* TeX; amb sub !== undefined, la x es canvia pel valor (entre parèntesis si és negatiu) */
  function etex(e, sub) {
    function leaf(n) { return n.t === "n" || n.t === "x" || n.t === "()" || n.t === "sqrt"; }
    function startsNum(n) { while (n.t === "*" || n.t === "^" || n.t === "/") n = n.a; return n.t === "n" || (n.t === "x" && sub !== undefined); }
    switch (e.t) {
      case "n": return nf(e.v);
      case "x": return sub === undefined ? "x" : nfp(sub);
      case "()": return "\\left(" + etex(e.a, sub) + "\\right)";
      case "neg": return "-" + (e.a.t === "+" || e.a.t === "-" ? "(" + etex(e.a, sub) + ")" : etex(e.a, sub));
      case "+": return etex(e.a, sub) + "+" + etex(e.b, sub);
      case "-": return etex(e.a, sub) + "-" + (e.b.t === "+" || e.b.t === "-" ? "(" + etex(e.b, sub) + ")" : etex(e.b, sub));
      case "*":
        var A = etex(e.a, sub), B = etex(e.b, sub);
        if (e.a.t === "+" || e.a.t === "-") A = "(" + A + ")";
        if (e.b.t === "+" || e.b.t === "-" || e.b.t === "neg") B = "(" + B + ")";
        return A + (e.imp && !startsNum(e.b) ? "" : "\\cdot ") + B;
      case "/": return "\\dfrac{" + etex(e.a.t === "()" ? e.a.a : e.a, sub) + "}{" + etex(e.b.t === "()" ? e.b.a : e.b, sub) + "}";
      case "^":
        var base = etex(e.a, sub);
        if (!leaf(e.a) || (e.a.t === "x" && sub !== undefined && sub < 0) || (e.a.t === "n" && e.a.v < 0)) base = "(" + base.replace(/^\(|\)$/g, "") + ")";
        return base + "^{" + etex(e.b.t === "()" ? e.b.a : e.b, sub) + "}";
      case "sqrt": return "\\sqrt{" + etex(e.a, sub) + "}";
    }
    return "";
  }
  /* termes del nivell superior: a + b − c -> [{s:1,e:a},{s:1,e:b},{s:-1,e:c}] */
  function topTerms(e, s, out) {
    out = out || []; s = s || 1;
    if (e.t === "+") { topTerms(e.a, s, out); topTerms(e.b, s, out); }
    else if (e.t === "-") { topTerms(e.a, s, out); topTerms(e.b, -s, out); }
    else out.push({ s: s, e: e });
    return out;
  }
  /* passos per a calcular f(a) */
  function imageSteps(e, a) {
    var v = ev(e, a), rows = [];
    var s1 = "f(" + nf(a) + ")=" + etex(e, a);
    var ts = topTerms(e);
    if (ts.length > 1 && ts.every(function (t) { return isFinite(ev(t.e, a)); })) {
      var mid = ts.map(function (t, i) { var tv = t.s * ev(t.e, a); return (i === 0 ? nf(tv) : (tv < 0 ? "-" + nf(-tv) : "+" + nf(tv))); }).join("");
      if (mid !== nf(v)) s1 += "=" + mid;
    } else if (e.t === "/" && isFinite(v)) {
      var nu = ev(e.a, a), de = ev(e.b, a);
      if (!near(de, 0)) s1 += "=\\dfrac{" + nf(nu) + "}{" + nf(de) + "}";
    } else if (e.t === "sqrt" && isFinite(v)) s1 += "=\\sqrt{" + nf(ev(e.a, a)) + "}";
    rows.push(s1 + (isFinite(v) ? "=\\boxed{" + nf(v) + "}" : ""));
    return { v: v, rows: rows };
  }

  /* ---------- funcions poligonals: el mateix estudi que pl.py ---------- */
  /* F(["c", [[0,1],[2,3]], "o"], ...) amb pts opcional */
  function PL(pieces, pts) { return { p: pieces.map(function (q) { return { l: q[0], v: q[1].map(function (P) { return [P[0], P[1]]; }), r: q[2] }; }), pts: (pts || []).map(function (P) { return [P[0], P[1]]; }) }; }
  function slope(P, Q) { return (Q[1] - P[1]) / (Q[0] - P[0]); }
  function sgn(v) { return near(v, 0) ? 0 : v > 0 ? 1 : -1; }
  function peq(P, Q) { return near(P[0], Q[0]) && near(P[1], Q[1]); }
  function hasPt(pts, P) { for (var i = 0; i < pts.length; i++) if (peq(pts[i], P)) return i; return -1; }
  function norm(f) {
    var ps = f.p.map(function (p) { return { l: p.l, v: p.v.slice(), r: p.r }; }), pts = f.pts.slice(), i, k, changed = true;
    ps.sort(function (a, b) { return a.v[0][0] - b.v[0][0]; });
    while (changed) {
      changed = false;
      for (i = 0; i < ps.length - 1; i++) {
        var A = ps[i], B = ps[i + 1];
        if (A.r !== "a" && B.l !== "a" && peq(A.v[A.v.length - 1], B.v[0])) {
          var P = B.v[0], ip = hasPt(pts, P);
          if (A.r === "c" || B.l === "c" || ip >= 0) {
            if (ip >= 0) pts.splice(ip, 1);
            ps[i] = { l: A.l, v: A.v.concat(B.v.slice(1)), r: B.r }; ps.splice(i + 1, 1); changed = true; break;
          }
        }
      }
    }
    ps.forEach(function (p) {
      if (p.l === "o" && (k = hasPt(pts, p.v[0])) >= 0) { pts.splice(k, 1); p.l = "c"; }
      if (p.r === "o" && (k = hasPt(pts, p.v[p.v.length - 1])) >= 0) { pts.splice(k, 1); p.r = "c"; }
      var v = p.v; i = 1;
      while (i < v.length - 1) { if (near(slope(v[i - 1], v[i]), slope(v[i], v[i + 1]))) v.splice(i, 1); else i++; }
    });
    return { p: ps, pts: pts };
  }
  function union(iv) {
    iv = iv.slice().sort(function (a, b) { return a[0] - b[0] || (a[2] ? 0 : 1) - (b[2] ? 0 : 1); });
    var out = [];
    iv.forEach(function (I) {
      var L = out[out.length - 1];
      if (L && (I[0] < L[1] - 1e-9 || (near(I[0], L[1]) && (L[3] || I[2])))) {
        if (I[1] > L[1] + 1e-9) { L[1] = I[1]; L[3] = I[3]; } else if (near(I[1], L[1])) L[3] = L[3] || I[3];
        return;
      }
      out.push(I.slice());
    });
    return out;
  }
  function value(f, x) {
    for (var j = 0; j < f.p.length; j++) {
      var p = f.p[j], v = p.v, n = v.length;
      for (var i = 0; i < n - 1; i++) {
        var P = v[i], Q = v[i + 1], inP = i > 0 || p.l !== "o", inQ = i < n - 2 || p.r !== "o";
        if ((x > P[0] + 1e-9 && x < Q[0] - 1e-9) || (near(x, P[0]) && inP) || (near(x, Q[0]) && inQ)) return P[1] + slope(P, Q) * (x - P[0]);
      }
      if (n === 1 && near(x, v[0][0])) return v[0][1];
      if (p.l === "a" && x < v[0][0]) return v[0][1] + slope(v[0], v[1]) * (x - v[0][0]);
      if (p.r === "a" && x > v[n - 1][0]) return v[n - 1][1] + slope(v[n - 2], v[n - 1]) * (x - v[n - 1][0]);
    }
    for (j = 0; j < f.pts.length; j++) if (near(f.pts[j][0], x)) return f.pts[j][1];
    return null;
  }
  function domain(f) {
    var iv = f.p.map(function (p) { return [p.l === "a" ? -INF : p.v[0][0], p.r === "a" ? INF : p.v[p.v.length - 1][0], p.l === "c", p.r === "c"]; });
    f.pts.forEach(function (P) { iv.push([P[0], P[0], true, true]); });
    return union(iv);
  }
  function rng(f) {
    var iv = [];
    f.p.forEach(function (p) {
      var v = p.v, n = v.length, s, y0;
      if (n === 1) { iv.push([v[0][1], v[0][1], true, true]); return; }
      for (var i = 0; i < n - 1; i++) {
        var P = v[i], Q = v[i + 1], inP = i > 0 || p.l !== "o", inQ = i < n - 2 || p.r !== "o";
        if (near(P[1], Q[1])) iv.push([P[1], P[1], true, true]);
        else if (P[1] < Q[1]) iv.push([P[1], Q[1], inP, inQ]); else iv.push([Q[1], P[1], inQ, inP]);
      }
      if (p.l === "a") { s = sgn(slope(v[0], v[1])); y0 = v[0][1]; iv.push(s > 0 ? [-INF, y0, false, true] : s < 0 ? [y0, INF, true, false] : [y0, y0, true, true]); }
      if (p.r === "a") { s = sgn(slope(v[n - 2], v[n - 1])); y0 = v[n - 1][1]; iv.push(s > 0 ? [y0, INF, true, false] : s < 0 ? [-INF, y0, false, true] : [y0, y0, true, true]); }
    });
    f.pts.forEach(function (P) { iv.push([P[1], P[1], true, true]); });
    return union(iv);
  }
  function segsOf(p) {
    var v = p.v, n = v.length, segs = [];
    if (n < 2) return segs;
    if (p.l === "a") segs.push([-INF, v[0][0], sgn(slope(v[0], v[1]))]);
    for (var i = 0; i < n - 1; i++) segs.push([v[i][0], v[i + 1][0], sgn(slope(v[i], v[i + 1]))]);
    if (p.r === "a") segs.push([v[n - 1][0], INF, sgn(slope(v[n - 2], v[n - 1]))]);
    return segs;
  }
  function mono(f) {
    var out = { "+": [], "-": [], "0": [] };
    f.p.forEach(function (p) {
      var segs = segsOf(p); if (!segs.length) return;
      var run = segs[0].slice();
      segs.slice(1).concat([[null, null, null]]).forEach(function (s) {
        if (s[2] === run[2]) { run[1] = s[1]; return; }
        out[run[2] > 0 ? "+" : run[2] < 0 ? "-" : "0"].push([run[0], run[1], false, false]);
        run = s.slice();
      });
    });
    return out;
  }
  function extrema(f) {
    var mx = [], mn = [];
    f.p.forEach(function (p) {
      var v = p.v, n = v.length;
      for (var i = 0; i < n; i++) {
        if ((i === 0 && p.l !== "a") || (i === n - 1 && p.r !== "a") || n < 2) continue;
        var sl = sgn(i > 0 ? slope(v[i - 1], v[i]) : slope(v[0], v[1])), sr = sgn(i < n - 1 ? slope(v[i], v[i + 1]) : slope(v[n - 2], v[n - 1]));
        if (sl > 0 && sr < 0) mx.push(v[i]);
        if (sl < 0 && sr > 0) mn.push(v[i]);
      }
    });
    return { max: mx, min: mn };
  }
  function absolute(f, R) {
    function where(y) {
      var xs = [];
      f.p.forEach(function (p) { var n = p.v.length; p.v.forEach(function (P, i) { var inc = (i > 0 && i < n - 1) || (i === 0 && p.l !== "o") || (i === n - 1 && p.r !== "o"); if (inc && near(P[1], y) && xs.indexOf(P[0]) < 0) xs.push(P[0]); }); });
      f.pts.forEach(function (P) { if (near(P[1], y) && xs.indexOf(P[0]) < 0) xs.push(P[0]); });
      return xs.sort(function (a, b) { return a - b; });
    }
    var hi = R[R.length - 1], lo = R[0];
    return { M: hi[1] !== INF && hi[3] ? [hi[1], where(hi[1])] : null, m: lo[0] !== -INF && lo[2] ? [lo[0], where(lo[0])] : null };
  }
  function disc(f) {
    var out = [], ps = f.p, xs = [];
    function add(x) { if (!xs.some(function (t) { return near(t, x); })) xs.push(x); }
    ps.forEach(function (p) { if (p.l !== "a") add(p.v[0][0]); if (p.r !== "a") add(p.v[p.v.length - 1][0]); });
    f.pts.forEach(function (P) { add(P[0]); });
    xs.sort(function (a, b) { return a - b; }).forEach(function (x) {
      var left = ps.filter(function (p) { return p.r !== "a" && p.v.length > 1 && near(p.v[p.v.length - 1][0], x); }).map(function (p) { return p.v[p.v.length - 1][1]; });
      var right = ps.filter(function (p) { return p.l !== "a" && p.v.length > 1 && near(p.v[0][0], x); }).map(function (p) { return p.v[0][1]; });
      var inside = ps.some(function (p) { return (p.l === "a" || p.v[0][0] < x - 1e-9) && (p.r === "a" || p.v[p.v.length - 1][0] > x + 1e-9); });
      var val = value(f, x), isPt = f.pts.some(function (P) { return near(P[0], x); });
      if (inside) { if (val !== null && isPt) out.push([x, "forat"]); return; }
      if (left.length && right.length) out.push([x, near(left[0], right[0]) ? "forat" : "salt"]);
      else if ((left.length || right.length) && val !== null && !ps.some(function (p) { return (near(p.v[p.v.length - 1][0], x) && p.r === "c") || (near(p.v[0][0], x) && p.l === "c"); })) out.push([x, "forat"]);
      else if (!left.length && !right.length && val !== null) out.push([x, "aillat"]);
    });
    return out;
  }
  function study(f0) {
    var f = norm(f0), R = rng(f), e = extrema(f), A = absolute(f, R);
    return { f: f, dom: domain(f), rec: R, mono: mono(f), max: e.max, min: e.min, amax: A.M, amin: A.m, disc: disc(f) };
  }
  /* intervals en TeX */
  function ivtex(I) { if (near(I[0], I[1])) return "\\{" + nf(I[0]) + "\\}"; return (I[2] ? "[" : "(") + nf(I[0]) + ",\\," + nf(I[1]) + (I[3] ? "]" : ")"); }
  function settex(iv) {
    if (!iv.length) return "\\varnothing";
    if (iv.length === 1 && iv[0][0] === -INF && iv[0][1] === INF) return "\\mathbb{R}";
    if (iv.length === 2 && iv[0][0] === -INF && iv[1][1] === INF && near(iv[0][1], iv[1][0]) && !iv[0][3] && !iv[1][2]) return "\\mathbb{R}-\\{" + nf(iv[0][1]) + "\\}";
    var parts = [], pend = [];
    iv.concat([null]).forEach(function (I) {
      if (I && near(I[0], I[1])) { pend.push(nf(I[0])); return; }
      if (pend.length) { parts.push("\\{" + pend.join(",\\,") + "\\}"); pend = []; }
      if (I) parts.push(ivtex(I));
    });
    return parts.join("\\cup ");
  }
  function pt(P) { return "(" + nf(P[0]) + ",\\," + nf(P[1]) + ")"; }

  /* ---------- gràfiques SVG ---------- */
  /* o: { xr:[x0,x1], yr:[y0,y1], W, H, pls:[{f, cls, mono}], curves:[{pts:[[x,y]...], cls}], fn:[{e, cls}], dots:[], bars:{dom, rec}, vl, xl, yl, xs, ys } */
  function plot(o) {
    var x0 = o.xr[0], x1 = o.xr[1], y0 = o.yr[0], y1 = o.yr[1], W = o.W || 340, H = o.H || Math.round(W * (y1 - y0) / (x1 - x0));
    if (H > 380 && !o.H) { H = 380; }
    function sx(x) { return +((x - x0) / (x1 - x0) * W).toFixed(1); }
    function sy(y) { return +(H - (y - y0) / (y1 - y0) * H).toFixed(1); }
    var g = "", k, xs = o.xs || (x1 - x0 > 24 ? 5 : x1 - x0 > 14 ? 2 : 1), ys = o.ys || (y1 - y0 > 24 ? 5 : y1 - y0 > 14 ? 2 : 1);
    for (k = Math.ceil(x0); k <= x1; k++) if (o.gx ? k % o.gx === 0 : true) g += '<line class="grid" x1="' + sx(k) + '" y1="0" x2="' + sx(k) + '" y2="' + H + '"/>';
    for (k = Math.ceil(y0); k <= y1; k++) if (o.gy ? k % o.gy === 0 : true) g += '<line class="grid" x1="0" y1="' + sy(k) + '" x2="' + W + '" y2="' + sy(k) + '"/>';
    var ax = Math.min(Math.max(0, y0), y1), ay = Math.min(Math.max(0, x0), x1);
    g += '<line class="ax" x1="0" y1="' + sy(ax) + '" x2="' + W + '" y2="' + sy(ax) + '"/><line class="ax" x1="' + sx(ay) + '" y1="0" x2="' + sx(ay) + '" y2="' + H + '"/>';
    for (k = Math.ceil(x0 / xs) * xs; k < x1; k += xs) if (k && k > x0) g += '<text class="tk" x="' + sx(k) + '" y="' + (sy(ax) + 13) + '" text-anchor="middle">' + String(k).replace("-", "−") + "</text>";
    for (k = Math.ceil(y0 / ys) * ys; k < y1; k += ys) if (k && k > y0) g += '<text class="tk" x="' + (sx(ay) - 5) + '" y="' + (sy(k) + 4) + '" text-anchor="end">' + String(k).replace("-", "−") + "</text>";
    if (ay === 0 && ax === 0 && x0 < 0 && y0 < 0) g += '<text class="tk" x="' + (sx(0) - 5) + '" y="' + (sy(0) + 13) + '" text-anchor="end">0</text>';
    g += '<text class="tk ax-l" x="' + (W - 6) + '" y="' + (sy(ax) - 6) + '" text-anchor="end">' + (o.xl || "x") + '</text><text class="tk ax-l" x="' + (sx(ay) + 6) + '" y="12">' + (o.yl || "y") + "</text>";
    /* barres de domini i recorregut */
    function bar(iv, cls, horiz) {
      iv.forEach(function (I) {
        var a = Math.max(I[0], horiz ? x0 : y0), b = Math.min(I[1], horiz ? x1 : y1);
        if (horiz) g += '<line class="bar ' + cls + '" x1="' + sx(a) + '" y1="' + sy(ax) + '" x2="' + sx(b) + '" y2="' + sy(ax) + '"/>';
        else g += '<line class="bar ' + cls + '" x1="' + sx(ay) + '" y1="' + sy(a) + '" x2="' + sx(ay) + '" y2="' + sy(b) + '"/>';
        [[I[0], I[2]], [I[1], I[3]]].forEach(function (E) {
          if (!isFinite(E[0])) return;
          var cx = horiz ? sx(E[0]) : sx(ay), cy = horiz ? sy(ax) : sy(E[0]);
          g += '<circle class="bd ' + cls + (E[1] ? "" : " op") + '" cx="' + cx + '" cy="' + cy + '" r="4.5"/>';
        });
      });
    }
    if (o.bars && o.bars.dom) bar(o.bars.dom, "bdom", true);
    if (o.bars && o.bars.rec) bar(o.bars.rec, "brec", false);
    if (o.bands) o.bands.forEach(function (B) { var a = Math.max(B[0], x0), b = Math.min(B[1], x1); g += '<rect class="band ' + B[2] + '" x="' + sx(a) + '" y="0" width="' + (sx(b) - sx(a)) + '" height="' + H + '"/>'; });
    if (o.vguides) o.vguides.forEach(function (x) { g += '<line class="guide" x1="' + sx(x) + '" y1="0" x2="' + sx(x) + '" y2="' + H + '"/>'; });
    /* corbes donades per punts (ja mostrejades) */
    (o.curves || []).forEach(function (c) {
      var d = "", pen = false;
      c.pts.forEach(function (P) {
        if (!P || !isFinite(P[1]) || P[1] > y1 + (y1 - y0) || P[1] < y0 - (y1 - y0)) { pen = false; return; }
        d += (pen ? "L" : "M") + sx(P[0]) + " " + sy(P[1]); pen = true;
      });
      g += '<path class="cv ' + (c.cls || "c0") + '" d="' + d + '"/>';
    });
    /* funcions donades per fórmula */
    (o.fn || []).forEach(function (F) {
      var d = "", pen = false, prev = null, n = 400, a = F.from == null ? x0 : Math.max(F.from, x0), b = F.to == null ? x1 : Math.min(F.to, x1);
      for (var i = 0; i <= n; i++) {
        var x = a + (b - a) * i / n, y = ev(F.e, x);
        if (!isFinite(y) || (prev !== null && Math.abs(y - prev) > 3 * (y1 - y0))) { pen = false; prev = isFinite(y) ? y : null; if (!isFinite(y)) continue; }
        var yy = Math.max(y0 - 2 * (y1 - y0), Math.min(y1 + 2 * (y1 - y0), y));
        d += (pen ? "L" : "M") + sx(x) + " " + sy(yy); pen = true; prev = y;
      }
      g += '<path class="cv ' + (F.cls || "c0") + '" d="' + d + '"/>';
    });
    /* funcions poligonals */
    (o.pls || []).forEach(function (F) {
      var f = F.f, cls = F.cls || "c0";
      function seg(P, Q, s) { g += '<line class="cv ' + (F.mono ? (s > 0 ? "up" : s < 0 ? "down" : "flat") : cls) + '" x1="' + sx(P[0]) + '" y1="' + sy(P[1]) + '" x2="' + sx(Q[0]) + '" y2="' + sy(Q[1]) + '"/>'; }
      function ray(P, Q, back) {
        /* semirecta des de P en la direcció de P->Q (back: cap a l'esquerra) fins a la vora */
        var m = slope(P, Q), dx = back ? -1 : 1, t = 1e9;
        var X = back ? x0 : x1; t = Math.min(t, (X - P[0]) * dx);
        if (Math.abs(m) > 1e-12) { var Y = (m * dx > 0) ? y1 : y0; t = Math.min(t, (Y - P[1]) / (m * dx)); }
        t = Math.max(t - 0.15, 0.1);
        var E = [P[0] + dx * t, P[1] + m * dx * t]; seg(P, E, sgn(m));
        var ang = Math.atan2(-(sy(E[1]) - sy(P[1])), sx(E[0]) - sx(P[0])), ex = sx(E[0]), ey = sy(E[1]), L = 9;
        g += '<path class="ah ' + (F.mono ? (sgn(m) > 0 ? "up" : sgn(m) < 0 ? "down" : "flat") : cls) + '" d="M' + (ex + Math.cos(ang) * 3).toFixed(1) + " " + (ey - Math.sin(ang) * 3).toFixed(1) + "L" + (ex - Math.cos(ang - 0.45) * L).toFixed(1) + " " + (ey + Math.sin(ang - 0.45) * L).toFixed(1) + "L" + (ex - Math.cos(ang + 0.45) * L).toFixed(1) + " " + (ey + Math.sin(ang + 0.45) * L).toFixed(1) + 'Z"/>';
      }
      f.p.forEach(function (p) {
        var v = p.v, n = v.length;
        for (var i = 0; i < n - 1; i++) seg(v[i], v[i + 1], sgn(slope(v[i], v[i + 1])));
        if (p.l === "a") ray(v[0], v[1], true);
        if (p.r === "a") ray(v[n - 1], v[n - 2], false);
      });
      f.p.forEach(function (p) {
        var v = p.v, n = v.length;
        if (p.l !== "a") g += '<circle class="ep ' + cls + (p.l === "o" ? " op" : "") + '" cx="' + sx(v[0][0]) + '" cy="' + sy(v[0][1]) + '" r="4.5"/>';
        if (p.r !== "a" && n > 1) g += '<circle class="ep ' + cls + (p.r === "o" ? " op" : "") + '" cx="' + sx(v[n - 1][0]) + '" cy="' + sy(v[n - 1][1]) + '" r="4.5"/>';
      });
      f.pts.forEach(function (P) { g += '<circle class="ep ' + cls + '" cx="' + sx(P[0]) + '" cy="' + sy(P[1]) + '" r="4.5"/>'; });
    });
    if (o.vl != null) g += '<line class="vl" x1="' + sx(o.vl) + '" y1="0" x2="' + sx(o.vl) + '" y2="' + H + '"/>';
    (o.dots || []).forEach(function (P) {
      g += '<circle class="' + (P.cls || "cut") + '" cx="' + sx(P.x) + '" cy="' + sy(P.y) + '" r="' + (P.r || 6) + '"/>';
      if (P.lab) g += '<text class="plab" x="' + (sx(P.x) + (P.dx || 8)) + '" y="' + (sy(P.y) + (P.dy || -8)) + '"' + (P.anchor ? ' text-anchor="' + P.anchor + '"' : "") + ">" + P.lab + "</text>";
    });
    return '<svg class="sgraf' + (o.small ? " small" : "") + '" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="gràfica">' + g + "</svg>";
  }
  /* finestra que conté una funció poligonal */
  function winOf(f, pad) {
    var xs = [], ys = [];
    pad = pad == null ? 1 : pad;
    f.p.forEach(function (p) { p.v.forEach(function (P) { xs.push(P[0]); ys.push(P[1]); }); });
    f.pts.forEach(function (P) { xs.push(P[0]); ys.push(P[1]); });
    var a = Math.min.apply(null, xs), b = Math.max.apply(null, xs), c = Math.min.apply(null, ys), d = Math.max.apply(null, ys);
    a = Math.min(a, 0) - pad; b = Math.max(b, 0) + pad; c = Math.min(c, 0) - pad; d = Math.max(d, 0) + pad;
    if (f.p.some(function (p) { return p.l === "a"; })) a -= 1;
    if (f.p.some(function (p) { return p.r === "a"; })) b += 1;
    return { xr: [a, b], yr: [c, d] };
  }

  /* ---------- funcions de mostra ---------- */
  var SETS = {
    dom: [
      { n: "A", f: PL([["c", [[-4, 1], [-1, 4], [2, -2], [5, 3]], "c"]]) },
      { n: "B", f: PL([["o", [[-3, -2], [0, 2], [4, 2]], "c"]]) },
      { n: "C", f: PL([["a", [[-2, -3], [1, 3]], "o"], ["c", [[3, 1], [6, -1]], "a"]]) },
      { n: "D", f: PL([["c", [[-5, 4], [-2, 1]], "o"], ["c", [[-2, -1], [2, 3]], "c"]], [[5, 2]]) },
      { n: "E", f: PL([["a", [[-3, 4], [0, 1], [3, 4]], "a"]]) }
    ],
    mono: [
      { n: "A", f: PL([["c", [[-5, -1], [-2, 3], [1, -2], [4, 2], [6, 2]], "c"]]) },
      { n: "B", f: PL([["a", [[-3, -2], [-1, 2], [2, 2], [4, -1]], "a"]]) },
      { n: "C", f: PL([["c", [[-4, 4], [0, 0], [3, 0]], "o"], ["c", [[3, 2], [6, 5]], "c"]]) },
      { n: "D", f: PL([["a", [[-4, 0], [-1, 3], [2, -3], [5, 1]], "a"]]) }
    ],
    ext: [
      { n: "A", f: PL([["c", [[-5, 2], [-3, 5], [0, -1], [3, 3], [5, 1]], "c"]]) },
      { n: "B", f: PL([["a", [[-3, 1], [-1, -3], [2, 4], [4, 0]], "a"]]) },
      { n: "C", f: PL([["c", [[-4, -2], [-1, 4], [1, 2], [3, 4], [6, -3]], "c"]]) },
      { n: "D", f: PL([["o", [[-4, 3], [-1, -2], [2, 3]], "o"]]) }
    ],
    cont: [
      { n: "A", f: PL([["c", [[-5, 1], [-1, 3]], "c"], ["o", [[-1, -1], [3, 3]], "c"]]) },
      { n: "B", f: PL([["c", [[-4, -1], [1, 4]], "o"], ["o", [[1, 4], [5, 0]], "c"]], [[1, 1]]) },
      { n: "C", f: PL([["c", [[-4, 1], [0, 1]], "o"], ["c", [[0, 2], [3, 2]], "o"], ["c", [[3, 3], [6, 3]], "c"]]) },
      { n: "D", f: PL([["c", [[-5, -2], [-2, 1], [1, -2], [4, 4]], "c"]]) }
    ],
    all: [
      { n: "A", f: PL([["c", [[-6, 0], [-3, 4], [0, 1]], "c"], ["o", [[0, -2], [3, 2], [6, 2]], "c"]]) },
      { n: "B", f: PL([["a", [[-4, 3], [-1, -2], [2, 2], [5, -1]], "c"]]) },
      { n: "C", f: PL([["o", [[-5, 2], [-2, -3], [0, -1]], "c"], ["o", [[2, 4], [4, 1], [6, 3]], "c"]]) }
    ]
  };
  /* funció poligonal aleatòria: contínua (cont=false) o amb una discontinuïtat */
  function randPL(opt) {
    opt = opt || {};
    for (var tries = 0; tries < 200; tries++) {
      var n = rint(3, opt.long ? 5 : 4), x = rint(-6, -3), v = [[x, rint(-4, 4)]], dir = pick([1, -1]);
      for (var i = 1; i < n; i++) {
        x += rint(2, 3);
        var y = v[i - 1][1] + dir * rint(2, 5);
        if (opt.flat && i === n - 1 && rint(0, 2) === 0) y = v[i - 1][1];
        if (y > 5 || y < -5) { y = Math.max(-5, Math.min(5, y)); if (y === v[i - 1][1]) y -= dir; }
        v.push([x, y]); dir = -dir;
      }
      if (x > 7) continue;
      var l = opt.arrows && rint(0, 2) === 0 ? "a" : pick(["c", "c", "o"]), r = opt.arrows && rint(0, 2) === 0 ? "a" : pick(["c", "c", "o"]);
      var f;
      if (opt.jump) {
        var k = rint(1, v.length - 2), J = v[k], kind = pick(["salt", "salt", "forat", "punt"]), A = v.slice(0, k + 1), B = v.slice(k);
        if (kind === "salt") {
          var d = rnz(-3, 3), B2 = B.map(function (P) { return [P[0], P[1] + d]; });
          if (B2.some(function (P) { return Math.abs(P[1]) > 6; })) continue;
          var closedLeft = rint(0, 1) === 0;
          f = PL([[l, A, closedLeft ? "c" : "o"], [closedLeft ? "o" : "c", B2, r]]);
        } else if (kind === "forat") f = PL([[l, A, "o"], ["o", B, r]]);
        else { var py = J[1] + pick([-3, -2, 2, 3]); if (Math.abs(py) > 6) continue; f = PL([[l, A, "o"], ["o", B, r]], [[J[0], py]]); }
      } else f = PL([[l, v, r]]);
      var s = study(f);
      if (opt.need && !opt.need(s)) continue;
      return f;
    }
    return PL([["c", [[-4, 1], [-1, 4], [2, -2], [5, 3]], "c"]]);
  }

  /* ---------- textos de l'estudi ---------- */
  var TXT = {
    dom: L3("Domini", "Dominio", "Domain"), rec: L3("Recorregut", "Recorrido", "Range"),
    up: L3("Creixent", "Creciente", "Increasing"), down: L3("Decreixent", "Decreciente", "Decreasing"), flat: L3("Constant", "Constante", "Constant"),
    rmax: L3("Màxim relatiu", "Máximo relativo", "Local maximum"), rmin: L3("Mínim relatiu", "Mínimo relativo", "Local minimum"),
    amax: L3("Màxim absolut", "Máximo absoluto", "Absolute maximum"), amin: L3("Mínim absolut", "Mínimo absoluto", "Absolute minimum"),
    none: L3("no en té", "no tiene", "none"), cont: L3("Continuïtat", "Continuidad", "Continuity"),
    isc: L3("és contínua: es pot dibuixar sense alçar el llapis.", "es continua: se puede dibujar sin levantar el lápiz.", "it is continuous: you can draw it without lifting your pencil."),
    salt: L3("salt", "salto", "jump"), forat: L3("li falta un punt o el té desplaçat", "le falta un punto o lo tiene desplazado", "a point is missing or moved"), aillat: L3("punt aïllat", "punto aislado", "isolated point"),
    at: L3("en", "en", "at")
  };
  function extList(L) { return L.length ? L.map(function (P) { return tex(pt(P)); }).join(", ") : T(TXT.none); }
  function absTxt(A) { return A ? tex(nf(A[0])) + " (" + T(L3("en", "en", "at")) + " " + A[1].map(function (x) { return tex("x=" + nf(x)); }).join(", ") + ")" : T(TXT.none); }
  function discTxt(D) {
    if (!D.length) return T(TXT.isc);
    return T(L3("és discontínua en ", "es discontinua en ", "it is discontinuous at ")) + D.map(function (d) { return tex("x=" + nf(d[0])) + " (" + T(TXT[d[1]]) + ")"; }).join(", ") + ".";
  }
  function studyRows(s, mode) {
    var r = [];
    if (mode === "dom" || mode === "all") {
      r.push('<span class="key kd"></span><b>' + T(TXT.dom) + ":</b> " + tex("\\mathrm{Dom}\\,f=" + settex(s.dom)));
      r.push('<span class="key kr"></span><b>' + T(TXT.rec) + ":</b> " + tex("\\mathrm{Rec}\\,f=" + settex(s.rec)));
    }
    if (mode === "mono" || mode === "all") {
      r.push('<span class="key ku"></span><b>' + T(TXT.up) + ":</b> " + tex(settex(s.mono["+"])));
      r.push('<span class="key kw"></span><b>' + T(TXT.down) + ":</b> " + tex(settex(s.mono["-"])));
      if (s.mono["0"].length) r.push('<span class="key kf"></span><b>' + T(TXT.flat) + ":</b> " + tex(settex(s.mono["0"])));
    }
    if (mode === "ext" || mode === "all") {
      r.push("▲ <b>" + T(TXT.rmax) + ":</b> " + extList(s.max) + " &nbsp; ▼ <b>" + T(TXT.rmin) + ":</b> " + extList(s.min));
      r.push("<b>" + T(TXT.amax) + ":</b> " + absTxt(s.amax) + " &nbsp; <b>" + T(TXT.amin) + ":</b> " + absTxt(s.amin));
    }
    if (mode === "cont" || mode === "all") r.push("<b>" + T(TXT.cont) + ":</b> " + T(L3("la funció ", "la función ", "the function ")) + discTxt(s.disc));
    return r;
  }
  function studyPlot(s, f, mode, small) {
    var w = winOf(f), o = { xr: w.xr, yr: w.yr, pls: [{ f: f, mono: mode === "mono" }], small: small, dots: [] };
    if (mode === "dom") o.bars = { dom: s.dom, rec: s.rec };
    if (mode === "ext" || mode === "all") {
      s.max.forEach(function (P) { o.dots.push({ x: P[0], y: P[1], cls: "mx", r: 6, lab: "Màx".replace("Màx", T(L3("Màx", "Máx", "Max"))) }); });
      s.min.forEach(function (P) { o.dots.push({ x: P[0], y: P[1], cls: "mn", r: 6, lab: T(L3("mín", "mín", "min")), dy: 16 }); });
    }
    if (mode === "cont" || mode === "all") o.vguides = s.disc.map(function (d) { return d[0]; });
    return plot(o);
  }

  /* ---------- giny: estudi d'una gràfica ---------- */
  function wAnal(w) {
    var mode = w.dataset.mode, set = SETS[w.dataset.set || mode], cur = set[0].f, out = w.querySelector(".gout"), info = w.querySelector(".info");
    var bs = w.querySelectorAll(".seg button");
    function paint() {
      var s = study(cur);
      out.innerHTML = studyPlot(s, s.f, mode) + '<div class="gcol">' + studyRows(s, mode).map(function (r) { return "<p>" + r + "</p>"; }).join("") + "</div>";
      info.innerHTML = "";
    }
    bs.forEach(function (b) {
      b.addEventListener("click", function () {
        bs.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        if (b.dataset.k === "rnd") cur = randPL({ arrows: mode === "dom" || mode === "all", jump: mode === "cont" ? rint(0, 3) > 0 : mode === "dom" || mode === "all" ? rint(0, 1) === 1 : false, flat: mode === "mono", long: true, need: mode === "ext" ? function (s) { return s.max.length + s.min.length >= 2; } : null });
        else cur = set[+b.dataset.k].f;
        paint();
      });
    });
    onLang(paint);
  }

  /* ---------- giny: la recta vertical ---------- */
  function circlePts(r, cx, cy) { var a = []; for (var i = 0; i <= 240; i++) { var t = i / 240 * 2 * Math.PI; a.push([cx + r * Math.cos(t), cy + r * Math.sin(t)]); } return a; }
  function sidePara() { var a = []; for (var i = 0; i <= 200; i++) { var y = -4.5 + 9 * i / 200; a.push([y * y / 2 - 3, y]); } return a; }
  function cubicPts() { var a = []; for (var i = 0; i <= 200; i++) { var x = -5 + 10 * i / 200; a.push([x, x * x * x / 20 - x]); } return a; }
  function plPts(f) { var a = []; f.p.forEach(function (p, j) { if (j) a.push(null); p.v.forEach(function (P) { a.push(P); }); }); return a; }
  var VCURVES = [
    { n: L3("Paràbola", "Parábola", "Parabola"), pts: (function () { var a = []; for (var i = 0; i <= 200; i++) { var x = -4 + 8 * i / 200; a.push([x, x * x / 2 - 3]); } return a; })(), f: true },
    { n: L3("Circumferència", "Circunferencia", "Circle"), pts: circlePts(4, 0, 0), f: false },
    { n: L3("Paràbola tombada", "Parábola tumbada", "Sideways parabola"), pts: sidePara(), f: false },
    { n: L3("Corba en S", "Curva en S", "S-curve"), pts: cubicPts(), f: true },
    { n: L3("Ziga-zaga", "Zigzag", "Zigzag"), pts: [[-5, -3], [-1, 3], [-3, -1], [3, 4], [5, -2]], f: false },
    { n: L3("Poligonal", "Poligonal", "Broken line"), pts: [[-5, 2], [-2, -3], [1, 1], [4, -1], [5, 3]], f: true }
  ];
  function vHits(pts, x) {
    var ys = [];
    for (var i = 0; i < pts.length - 1; i++) {
      var P = pts[i], Q = pts[i + 1]; if (!P || !Q) continue;
      if ((x - P[0]) * (x - Q[0]) <= 0 && !near(P[0], Q[0])) {
        var y = P[1] + (Q[1] - P[1]) * (x - P[0]) / (Q[0] - P[0]);
        if (!ys.some(function (t) { return Math.abs(t - y) < 0.05; })) ys.push(y);
      }
    }
    return ys;
  }
  function wVline() {
    var w = document.getElementById("w-vline"); if (!w) return;
    var out = w.querySelector(".gout"), info = w.querySelector(".info"), sl = w.querySelector('input[type="range"]'), cur = VCURVES[0];
    function paint() {
      var x = +sl.value, ys = vHits(cur.pts, x);
      out.innerHTML = plot({ xr: [-6, 6], yr: [-6, 6], curves: [{ pts: cur.pts, cls: "c0" }], vl: x, dots: ys.map(function (y) { return { x: x, y: y, cls: ys.length > 1 ? "bad" : "cut", r: 6 }; }) });
      var msg = fill(T(L3("La recta vertical {x} talla la gràfica en <b>{n}</b> punt(s).", "La recta vertical {x} corta la gráfica en <b>{n}</b> punto(s).", "The vertical line {x} meets the graph at <b>{n}</b> point(s).")), { x: tex("x=" + nf(x)), n: ys.length });
      if (ys.length > 1) msg += " " + fill(T(L3("Per a aquest valor de {x} hi ha {n} valors de {y}: <b>no és una funció</b>.", "Para este valor de {x} hay {n} valores de {y}: <b>no es una función</b>.", "This value of {x} has {n} values of {y}: <b>it is not a function</b>.")), { x: tex("x"), y: tex("y"), n: ys.length });
      else msg += " " + T(cur.f ? L3("Mou la recta: mai no la talla en més d'un punt, així que <b>és una funció</b>.", "Mueve la recta: nunca la corta en más de un punto, así que <b>es una función</b>.", "Move the line: it never meets the graph more than once, so <b>it is a function</b>.")
        : L3("Mou la recta i busca un lloc on la talle en dos punts…", "Mueve la recta y busca un lugar donde la corte en dos puntos…", "Move the line and look for a place where it meets the graph twice…"));
      info.innerHTML = msg;
    }
    sl.addEventListener("input", paint);
    var bs = w.querySelectorAll(".seg button");
    bs.forEach(function (b) { b.addEventListener("click", function () { bs.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); cur = VCURVES[+b.dataset.k]; paint(); }); });
    onLang(function () { bs.forEach(function (b) { b.textContent = T(VCURVES[+b.dataset.k].n); }); paint(); });
  }

  /* ---------- giny: màquina de funcions (imatge) ---------- */
  function wMachine() {
    var w = document.getElementById("w-machine"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = ""; out.innerHTML = "";
      var e = parseExpr(I.f.value); if (!e) { info.innerHTML = warn(u("bad")); return; }
      var a = numIn(I.x.value); if (a === null) { info.innerHTML = warn(u("badx")); return; }
      var r = imageSteps(e, a), rows = [tex("f(x)=" + etex(e))];
      rows.push(tex(r.rows[0]));
      out.innerHTML = rows2html(rows);
      info.innerHTML = isFinite(r.v) ? fill(T(L3("La <b>imatge</b> de {a} és {v}: el punt {p} és de la gràfica. Diem també que {a} és una <b>antiimatge</b> de {v}.", "La <b>imagen</b> de {a} es {v}: el punto {p} es de la gráfica. Decimos también que {a} es una <b>antiimagen</b> de {v}.", "The <b>image</b> of {a} is {v}: the point {p} is on the graph. We also say {a} is a <b>preimage</b> of {v}.")), { a: tex(nf(a)), v: tex(nf(r.v)), p: tex(pt([a, r.v])) })
        : warn(fill(T(L3("{a} no té imatge: l'operació no es pot fer (divisió entre 0 o arrel d'un nombre negatiu). {a} no és del domini.", "{a} no tiene imagen: la operación no se puede hacer (división entre 0 o raíz de un número negativo). {a} no es del dominio.", "{a} has no image: the operation can't be done (division by 0 or square root of a negative). {a} is not in the domain.")), { a: tex("x=" + nf(a)) }));
    }
    [I.f, I.x].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.f.value = v[0]; I.x.value = v[1]; paint(); });
    onLang(paint);
  }

  /* ---------- giny: taula de valors i gràfica ---------- */
  function wPlot() {
    var w = document.getElementById("w-plot"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = ""; out.innerHTML = "";
      var e = parseExpr(I.f.value); if (!e) { info.innerHTML = warn(u("bad")); return; }
      var a = numIn(I.a.value), b = numIn(I.b.value);
      if (a === null || b === null || b <= a || b - a > 20) { info.innerHTML = warn(T(L3("Tria un interval de x vàlid (com a molt 20 unitats): per exemple, de −3 a 3.", "Elige un intervalo de x válido (como mucho 20 unidades): por ejemplo, de −3 a 3.", "Choose a valid x range (at most 20 units): for example, from −3 to 3."))); return; }
      var xs = [], st = b - a > 10 ? 2 : 1; for (var x = Math.ceil(a); x <= b; x += st) xs.push(x);
      var ys = xs.map(function (x) { return ev(e, x); }), ok = ys.filter(isFinite);
      var lo = Math.min.apply(null, ok.concat([0])), hi = Math.max.apply(null, ok.concat([0]));
      if (hi - lo > 40) { var mid = ok.length ? ok[Math.floor(ok.length / 2)] : 0; lo = Math.max(lo, mid - 20); hi = Math.min(hi, mid + 20); }
      var tbl = '<table class="data tv"><tbody><tr><th>' + tex("x") + "</th>" + xs.map(function (x) { return "<td>" + tex(nf(x)) + "</td>"; }).join("") + "</tr><tr><th>" + tex("f(x)") + "</th>" + ys.map(function (y) { return "<td>" + (isFinite(y) ? tex(nf(y)) : "—") + "</td>"; }).join("") + "</tr></tbody></table>";
      var R = { xr: [Math.min(a, 0) - 1, Math.max(b, 0) + 1], yr: [Math.floor(lo) - 1, Math.ceil(hi) + 1] };
      out.innerHTML = '<div class="gcol"><p>' + tex("f(x)=" + etex(e)) + '</p><div class="tbl-wrap">' + tbl + "</div></div>"
        + plot({ xr: R.xr, yr: R.yr, fn: [{ e: e, from: a, to: b }], dots: xs.map(function (x, i) { return isFinite(ys[i]) && ys[i] >= R.yr[0] && ys[i] <= R.yr[1] ? { x: x, y: ys[i], cls: "pt p0", r: 4 } : null; }).filter(Boolean) });
      var f0 = ev(e, 0), msg = [];
      if (0 >= a && 0 <= b && isFinite(f0)) msg.push(fill(T(L3("Talla l'eix {Y} en {p}.", "Corta el eje {Y} en {p}.", "It crosses the {Y} axis at {p}.")), { Y: tex("Y"), p: tex(pt([0, f0])) }));
      var zs = [];
      for (var k = 0; k <= 2000; k++) { var x1 = a + (b - a) * k / 2000, x2 = a + (b - a) * (k + 1) / 2000, y1 = ev(e, x1), y2 = ev(e, x2); if (isFinite(y1) && Math.abs(y1) < 1e-9) { if (!zs.some(function (z) { return near(z, x1); })) zs.push(x1); } else if (k < 2000 && isFinite(y1) && isFinite(y2) && y1 * y2 < 0 && Math.abs(y1 - y2) < (hi - lo + 1)) { var lo2 = x1, hi2 = x2; for (var it = 0; it < 50; it++) { var m = (lo2 + hi2) / 2; if (ev(e, lo2) * ev(e, m) <= 0) hi2 = m; else lo2 = m; } var z = Math.round(lo2 * 1000) / 1000; if (!zs.some(function (t) { return Math.abs(t - z) < 1e-3; })) zs.push(z); } }
      if (zs.length) msg.push(fill(T(L3("Talla l'eix {X} en {p}.", "Corta el eje {X} en {p}.", "It crosses the {X} axis at {p}.")), { X: tex("X"), p: zs.map(function (z) { return tex(pt([z, 0])); }).join(", ") }));
      else msg.push(fill(T(L3("En aquest interval no talla l'eix {X}.", "En este intervalo no corta el eje {X}.", "It doesn't cross the {X} axis in this range.")), { X: tex("X") }));
      info.innerHTML = "💡 " + msg.join(" ");
    }
    [I.f, I.a, I.b].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.f.value = v[0]; I.a.value = v[1]; I.b.value = v[2]; paint(); });
    onLang(paint);
  }

  /* ---------- giny: llegir una gràfica (situacions) ---------- */
  var STORIES = [
    { n: L3("Excursió", "Excursión", "Hike"), xl: "t (h)", yl: "d (km)", xr: [-0.5, 8.5], yr: [-1, 13], H: 260,
      f: PL([["c", [[0, 0], [2, 8], [3, 8], [4, 12], [5, 12], [8, 0]], "c"]]),
      seg: function (P, Q) { var m = slope(P, Q); return m > 0 ? L3("s'allunya de casa a " + nf(m) + " km/h", "se aleja de casa a " + nf(m) + " km/h", "walking away from home at " + nf(m) + " km/h") : m < 0 ? L3("torna cap a casa a " + nf(-m) + " km/h", "vuelve hacia casa a " + nf(-m) + " km/h", "heading back home at " + nf(-m) + " km/h") : L3("està parat (descansa)", "está parado (descansa)", "stopped (resting)"); },
      say: function (x, y) { return fill(T(L3("Han passat {x} h i està a {y} km de casa.", "Han pasado {x} h y está a {y} km de casa.", "{x} h have passed and they are {y} km from home.")), { x: tex(nf(x)), y: tex(nf(y)) }); } },
    { n: L3("Temperatura", "Temperatura", "Temperature"), xl: "h", yl: "T (°C)", xr: [-1, 25], yr: [-4, 22], H: 260, xs: 2, ys: 2,
      f: PL([["c", [[0, 6], [6, 2], [14, 18], [18, 14], [24, 8]], "c"]]),
      seg: function (P, Q) { var m = slope(P, Q); return m > 0 ? L3("la temperatura puja", "la temperatura sube", "the temperature is rising") : m < 0 ? L3("la temperatura baixa", "la temperatura baja", "the temperature is falling") : L3("la temperatura no canvia", "la temperatura no cambia", "the temperature stays the same"); },
      say: function (x, y) { return fill(T(L3("A les {x} h hi ha {y} °C.", "A las {x} h hay {y} °C.", "At {x}:00 it is {y} °C.")), { x: tex(nf(x)), y: tex(nf(y)) }); } },
    { n: L3("Dipòsit d'aigua", "Depósito de agua", "Water tank"), xl: "t (min)", yl: "V (L)", xr: [-2, 42], yr: [-20, 220], H: 260, xs: 5, ys: 50, gx: 5, gy: 25,
      f: PL([["c", [[0, 50], [10, 200], [25, 200], [40, 0]], "c"]]),
      seg: function (P, Q) { var m = slope(P, Q); return m > 0 ? L3("s'omple a " + nf(m) + " L/min", "se llena a " + nf(m) + " L/min", "filling at " + nf(m) + " L/min") : m < 0 ? L3("es buida a " + nf(-m) + " L/min", "se vacía a " + nf(-m) + " L/min", "emptying at " + nf(-m) + " L/min") : L3("està ple: ni entra ni ix aigua", "está lleno: ni entra ni sale agua", "it is full: no water in or out"); },
      say: function (x, y) { return fill(T(L3("Al minut {x} hi ha {y} litres.", "En el minuto {x} hay {y} litros.", "At minute {x} there are {y} litres.")), { x: tex(nf(x)), y: tex(nf(y)) }); } }
  ];
  function wRead() {
    var w = document.getElementById("w-read"); if (!w) return;
    var out = w.querySelector(".gout"), info = w.querySelector(".info"), sl = w.querySelector('input[type="range"]'), cur = STORIES[0];
    function paint() {
      var v = cur.f.p[0].v, x0 = v[0][0], x1 = v[v.length - 1][0], x = x0 + (x1 - x0) * sl.value / 100;
      x = Math.round(x * 4) / 4;
      var y = value(cur.f, x), seg = null;
      for (var i = 0; i < v.length - 1; i++) if (x >= v[i][0] && x < v[i + 1][0]) seg = [v[i], v[i + 1]];
      if (!seg) seg = [v[v.length - 2], v[v.length - 1]];
      out.innerHTML = plot({ xr: cur.xr, yr: cur.yr, H: cur.H, W: 360, xl: cur.xl, yl: cur.yl, xs: cur.xs, ys: cur.ys, gx: cur.gx, gy: cur.gy, pls: [{ f: cur.f }], vl: x, dots: [{ x: x, y: y, cls: "cut", r: 6 }] });
      info.innerHTML = cur.say(x, y) + " " + T(L3("En aquest tram ", "En este tramo ", "On this stretch ")) + T(cur.seg(seg[0], seg[1])) + ".";
    }
    sl.addEventListener("input", paint);
    var bs = w.querySelectorAll(".seg button");
    bs.forEach(function (b) { b.addEventListener("click", function () { bs.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); cur = STORIES[+b.dataset.k]; paint(); }); });
    onLang(function () { bs.forEach(function (b) { b.textContent = T(STORIES[+b.dataset.k].n); }); paint(); });
  }

  /* ---------- entrenadors ---------- */
  function polyS(c) {
    /* coeficients [c0, c1, c2] -> text de fórmula i arbre */
    var s = "";
    [[c[2], "x^2"], [c[1], "x"], [c[0], ""]].forEach(function (t) {
      var a = t[0]; if (!a) return;
      var abs = Math.abs(a), body = t[1] ? (abs === 1 ? "" : abs) + t[1] : String(abs);
      s += (a < 0 ? "-" : s ? "+" : "") + body;
    });
    return s || "0";
  }
  function ivOpts(right, wrongs) {
    /* opcions úniques en TeX: la correcta + distractors */
    var all = [right], seen = {}; seen[right] = 1;
    wrongs.forEach(function (w) { if (w && !seen[w] && all.length < 4) { seen[w] = 1; all.push(w); } });
    var order = shuffle(all.map(function (_, i) { return i; }));
    return { opts: order.map(function (i) { return { va: "$" + all[i] + "$" }; }), ans: order.indexOf(0) };
  }
  function flipClose(iv) { return iv.map(function (I) { return [I[0], I[1], isFinite(I[0]) ? !I[2] : false, isFinite(I[1]) ? !I[3] : false]; }); }
  var GEN = {
    isf: function () {
      var c = rint(0, 1) ? pick(VCURVES) : null, pts, isF;
      if (c) { pts = c.pts; isF = c.f; }
      else {
        isF = rint(0, 1) === 1;
        var v = [[rint(-5, -3), rint(-4, 4)]];
        for (var i = 0; i < 4; i++) { var P = v[v.length - 1]; v.push([P[0] + rint(1, 3), Math.max(-5, Math.min(5, P[1] + rnz(-4, 4)))]); }
        if (!isF) { var k = rint(1, 3); v.splice(k + 1, 0, [v[k][0] - rint(1, 2), v[k][1] + rnz(-3, 3)]); v.splice(k + 2, 0, [v[k + 1][0] + rint(2, 3), v[k + 1][1] + rnz(-3, 3)]); }
        pts = v; isF = !v.some(function (P, j) { return j && P[0] <= v[j - 1][0]; });
      }
      return { opts: [L3("Sí, és funció", "Sí, es función", "Yes, it's a function"), L3("No és funció", "No es función", "Not a function")], ans: isF ? 0 : 1,
        q: function () { return T(L3("Aquesta gràfica, és d'una funció?", "¿Esta gráfica es de una función?", "Is this the graph of a function?")) + plot({ xr: [-6, 6], yr: [-6, 6], curves: [{ pts: pts, cls: "c0" }], small: true }); },
        s: function () { return isF ? T(L3("Cap recta vertical no la talla en més d'un punt: a cada {x} li correspon una única {y}.", "Ninguna recta vertical la corta en más de un punto: a cada {x} le corresponde una única {y}.", "No vertical line meets it more than once: each {x} has a single {y}.")).replace("{x}", tex("x")).replace("{y}", tex("y")) : T(L3("Hi ha rectes verticals que la tallen en més d'un punt: alguna {x} té més d'una {y}.", "Hay rectas verticales que la cortan en más de un punto: alguna {x} tiene más de una {y}.", "Some vertical lines meet it more than once: some {x} has more than one {y}.")).replace("{x}", tex("x")).replace("{y}", tex("y")); } };
    },
    img: function () {
      var c = rint(0, 2) ? [rint(-6, 6), rnz(-5, 5), rnz(-3, 3)] : [rint(-9, 9), rnz(-6, 6), 0], a = rint(-4, 4), e = parseExpr(polyS(c)), v = ev(e, a);
      return { num: v, q: function () { return fill(T(L3("Si {f}, calcula {a}.", "Si {f}, calcula {a}.", "If {f}, work out {a}.")), { f: "$f(x)=" + etex(e) + "$", a: "$f(" + nf(a) + ")$" }); }, s: function () { return tex(imageSteps(e, a).rows[0]); } };
    },
    anti: function () {
      var m = rnz(-5, 5), b = rint(-9, 9), x0 = rint(-6, 6), k = m * x0 + b, e = parseExpr(polyS([b, m, 0]));
      return { num: x0, q: function () { return fill(T(L3("Si {f}, quin valor de {x} té imatge {k}?", "Si {f}, ¿qué valor de {x} tiene imagen {k}?", "If {f}, which value of {x} has image {k}?")), { f: "$f(x)=" + etex(e) + "$", x: "$x$", k: "$" + k + "$" }); },
        s: function () { return tex(etex(e) + "=" + k + "\\Rightarrow " + (m === 1 ? "" : m === -1 ? "-" : m) + "x=" + (k - b) + "\\Rightarrow \\boxed{x=" + x0 + "}"); } };
    },
    read: function () {
      var f = randPL({}), v = f.p[0].v, cand = [];
      for (var x = v[0][0]; x <= v[v.length - 1][0]; x++) { var y = value(f, x); if (y !== null && near(y, Math.round(y))) cand.push([x, y]); }
      var P = pick(cand);
      return { num: P[1], q: function () { return fill(T(L3("Mira la gràfica de la funció {f}. Quant val {a}?", "Mira la gráfica de la función {f}. ¿Cuánto vale {a}?", "Look at the graph of {f}. What is {a}?")), { f: "$f$", a: "$f(" + nf(P[0]) + ")$" }) + plot({ xr: [-7, 8], yr: [-6, 6], pls: [{ f: f }], small: true }); },
        s: function () { return fill(T(L3("Busquem {x} en l'eix horitzontal, pugem (o baixem) fins a la gràfica i llegim l'altura: {r}.", "Buscamos {x} en el eje horizontal, subimos (o bajamos) hasta la gráfica y leemos la altura: {r}.", "Find {x} on the horizontal axis, go up (or down) to the graph and read the height: {r}.")), { x: tex("x=" + nf(P[0])), r: tex("f(" + nf(P[0]) + ")=" + nf(P[1])) }); } };
    },
    dom: function () {
      var f = randPL({ arrows: true, jump: rint(0, 1) === 1 }), s = study(f), askDom = rint(0, 1) === 0, R = askDom ? s.dom : s.rec, O = askDom ? s.rec : s.dom;
      var o = ivOpts(settex(R), [settex(flipClose(R)), settex(O), settex([[-INF, INF, false, false]]), settex(flipClose(O))]);
      return { opts: o.opts, ans: o.ans,
        q: function () { return T(askDom ? L3("Quin és el <b>domini</b> d'aquesta funció?", "¿Cuál es el <b>dominio</b> de esta función?", "What is the <b>domain</b> of this function?") : L3("Quin és el <b>recorregut</b> d'aquesta funció?", "¿Cuál es el <b>recorrido</b> de esta función?", "What is the <b>range</b> of this function?")) + studyPlot(s, s.f, "none", true); },
        s: function () { return T(askDom ? L3("Mirem quines {x} tenen imatge (eix horitzontal):", "Miramos qué {x} tienen imagen (eje horizontal):", "See which {x} values have an image (horizontal axis):") : L3("Mirem quins valors de {y} pren la funció (eix vertical):", "Miramos qué valores de {y} toma la función (eje vertical):", "See which {y} values the function takes (vertical axis):")).replace("{x}", tex("x")).replace("{y}", tex("y")) + " " + tex((askDom ? "\\mathrm{Dom}\\,f=" : "\\mathrm{Rec}\\,f=") + settex(R)) + plot({ xr: winOf(s.f).xr, yr: winOf(s.f).yr, pls: [{ f: s.f }], bars: askDom ? { dom: s.dom } : { rec: s.rec }, small: true }); } };
    },
    domf: function () {
      var t = rint(0, 4), k = rnz(-6, 6), a = rnz(-5, 5), b = rint(-9, 9), e, R, W;
      function nk(s) { return s.replace(/\+-/g, "-").replace(/--/g, "+"); }
      if (t === 0) { e = nk(polyS([b, a, rnz(-3, 3)])); R = "\\mathbb{R}"; W = ["\\mathbb{R}-\\{0\\}", "[0,\\,+\\infty)", "\\mathbb{R}-\\{" + nf(b) + "\\}"]; }
      else if (t === 1) { e = nk(rnz(1, 9) + "/(x-" + k + ")"); R = "\\mathbb{R}-\\{" + nf(k) + "\\}"; W = ["\\mathbb{R}-\\{" + nf(-k) + "\\}", "\\mathbb{R}", "(" + nf(k) + ",\\,+\\infty)"]; }
      else if (t === 2) { e = nk("sqrt(x-" + k + ")"); R = "[" + nf(k) + ",\\,+\\infty)"; W = ["(" + nf(k) + ",\\,+\\infty)", "[" + nf(-k) + ",\\,+\\infty)", "(-\\infty,\\," + nf(k) + "]"]; }
      else if (t === 3) { e = nk("sqrt(" + k + "-x)"); R = "(-\\infty,\\," + nf(k) + "]"; W = ["[" + nf(k) + ",\\,+\\infty)", "(-\\infty,\\," + nf(k) + ")", "\\mathbb{R}-\\{" + nf(k) + "\\}"]; }
      else { var m = rint(1, 5); e = nk(rnz(1, 9) + "/(x^2-" + m * m + ")"); R = "\\mathbb{R}-\\{-" + m + ",\\," + m + "\\}"; W = ["\\mathbb{R}-\\{" + m + "\\}", "\\mathbb{R}-\\{" + m * m + "\\}", "\\mathbb{R}"]; }
      var E = parseExpr(e), o = ivOpts(R, W);
      var why = [L3("És un polinomi: sempre es pot calcular.", "Es un polinomio: siempre se puede calcular.", "It's a polynomial: it can always be worked out."),
        L3("El denominador no pot valdre 0: {c}.", "El denominador no puede valer 0: {c}.", "The denominator can't be 0: {c}."),
        L3("El radicand ha de ser positiu o zero: {c}.", "El radicando tiene que ser positivo o cero: {c}.", "The number under the root must be positive or zero: {c}."),
        L3("El radicand ha de ser positiu o zero: {c}.", "El radicando tiene que ser positivo o cero: {c}.", "The number under the root must be positive or zero: {c}."),
        L3("El denominador no pot valdre 0: {c}.", "El denominador no puede valer 0: {c}.", "The denominator can't be 0: {c}.")][t];
      var cond = t === 0 ? "" : t === 1 ? "x-" + nfp(k) + "\\neq0\\Rightarrow x\\neq" + nf(k) : t === 2 ? "x-" + nfp(k) + "\\ge0\\Rightarrow x\\ge" + nf(k) : t === 3 ? nf(k) + "-x\\ge0\\Rightarrow x\\le" + nf(k) : "";
      if (t === 4) { var mm = +R.match(/,\\,(\d+)\\\}/)[1]; cond = "x^2\\neq" + mm * mm + "\\Rightarrow x\\neq\\pm" + mm; }
      cond = cond.replace(/-\(-(\d+)\)/g, "+$1");
      return { opts: o.opts, ans: o.ans, q: function () { return fill(T(L3("Quin és el domini de {f}?", "¿Cuál es el dominio de {f}?", "What is the domain of {f}?")), { f: "$f(x)=" + etex(E) + "$" }); },
        s: function () { return T(why).replace("{c}", tex(cond)) + " " + tex("\\mathrm{Dom}\\,f=" + R); } };
    },
    mono: function () {
      var f = randPL({ long: true, flat: rint(0, 2) === 0 }), s = study(f), up = rint(0, 1) === 0, R = s.mono[up ? "+" : "-"], O = s.mono[up ? "-" : "+"];
      if (!R.length) return GEN.mono();
      var yv = R.map(function (I) { var a = value(s.f, I[0]), b = value(s.f, I[1]); return [Math.min(a, b), Math.max(a, b), false, false]; });
      var o = ivOpts(settex(R), [settex(O), settex(R.map(function (I) { return [I[0], I[1], true, true]; })), settex(union(yv))]);
      return { opts: o.opts, ans: o.ans,
        q: function () { return T(up ? L3("En quins intervals és <b>creixent</b> aquesta funció?", "¿En qué intervalos es <b>creciente</b> esta función?", "On which intervals is this function <b>increasing</b>?") : L3("En quins intervals és <b>decreixent</b> aquesta funció?", "¿En qué intervalos es <b>decreciente</b> esta función?", "On which intervals is this function <b>decreasing</b>?")) + plot({ xr: [-7, 8], yr: [-6, 6], pls: [{ f: s.f }], small: true }); },
        s: function () { return T(L3("Llegim d'esquerra a dreta i donem els intervals de {x} (oberts):", "Leemos de izquierda a derecha y damos los intervalos de {x} (abiertos):", "Read from left to right and give the {x}-intervals (open):")).replace("{x}", tex("x")) + " " + tex(settex(R)) + plot({ xr: [-7, 8], yr: [-6, 6], pls: [{ f: s.f, mono: true }], small: true }); } };
    },
    ext: function () {
      var f = randPL({ long: true, need: function (s) { return s.max.length + s.min.length >= 1; } }), s = study(f), isMax = s.max.length && (s.min.length === 0 || rint(0, 1) === 0), L = isMax ? s.max : s.min;
      var P = L[0], multi = L.length > 1;
      return { pair: L, q: function () { return T(isMax ? (multi ? L3("Escriu un dels <b>màxims relatius</b> d'aquesta funció.", "Escribe uno de los <b>máximos relativos</b> de esta función.", "Write one of the <b>local maxima</b> of this function.") : L3("Escriu el punt on hi ha el <b>màxim relatiu</b> d'aquesta funció.", "Escribe el punto donde está el <b>máximo relativo</b> de esta función.", "Write the point where this function has its <b>local maximum</b>."))
          : (multi ? L3("Escriu un dels <b>mínims relatius</b> d'aquesta funció.", "Escribe uno de los <b>mínimos relativos</b> de esta función.", "Write one of the <b>local minima</b> of this function.") : L3("Escriu el punt on hi ha el <b>mínim relatiu</b> d'aquesta funció.", "Escribe el punto donde está el <b>mínimo relativo</b> de esta función.", "Write the point where this function has its <b>local minimum</b>."))) + plot({ xr: [-7, 8], yr: [-6, 6], pls: [{ f: s.f }], small: true }); },
        s: function () { return T(isMax ? L3("Passa de creixent a decreixent en", "Pasa de creciente a decreciente en", "It changes from increasing to decreasing at") : L3("Passa de decreixent a creixent en", "Pasa de decreciente a creciente en", "It changes from decreasing to increasing at")) + " " + L.map(function (Q) { return tex(pt(Q)); }).join(", ") + "." + studyPlot(s, s.f, "ext", true); } };
    },
    cont: function () {
      var f = randPL({ jump: rint(0, 3) > 0 }), s = study(f), D = s.disc, xs = [];
      s.f.p.forEach(function (p) { p.v.forEach(function (P, i) { if (i > 0 && i < p.v.length - 1 || (i === 0 && s.f.p.indexOf(p) > 0)) xs.push(P[0]); }); });
      var right = D.length ? T(L3("Discontínua en ", "Discontinua en ", "Discontinuous at ")) + "$x=" + nf(D[0][0]) + "$" : T(L3("Contínua", "Continua", "Continuous"));
      var wr = [D.length ? T(L3("Contínua", "Continua", "Continuous")) : null];
      xs.filter(function (x) { return !D.length || !near(x, D[0][0]); }).slice(0, 3).forEach(function (x) { wr.push(T(L3("Discontínua en ", "Discontinua en ", "Discontinuous at ")) + "$x=" + nf(x) + "$"); });
      var all = [right].concat(wr.filter(Boolean).filter(function (t, i, a) { return a.indexOf(t) === i && t !== right; }).slice(0, 2)), order = shuffle(all.map(function (_, i) { return i; }));
      return { opts: order.map(function (i) { return { va: all[i] }; }), ans: order.indexOf(0),
        q: function () { return T(L3("Com és aquesta funció?", "¿Cómo es esta función?", "What can you say about this function?")) + plot({ xr: [-7, 8], yr: [-6, 6], pls: [{ f: f }], small: true }); },
        s: function () { return T(L3("La funció ", "La función ", "The function ")) + discTxt(D); } };
    },
    prob: function () {
      var t = rint(0, 2), b, m, k, ask = rint(0, 1), e, ctx;
      if (t === 0) { b = pick([2, 2.5, 3, 3.5]); m = pick([0.5, 1, 1.5, 2]); ctx = L3("Un taxi cobra {b} € per pujar-hi i {m} € per cada km.", "Un taxi cobra {b} € por subir y {m} € por cada km.", "A taxi charges €{b} to get in and €{m} per km."); }
      else if (t === 1) { b = pick([5, 8, 10, 12]); m = pick([0.1, 0.2, 0.5]); ctx = L3("Una tarifa de mòbil costa {b} € al mes més {m} € per cada minut de trucada.", "Una tarifa de móvil cuesta {b} € al mes más {m} € por cada minuto de llamada.", "A phone plan costs €{b} a month plus €{m} per call minute."); }
      else { b = pick([20, 30, 40]); m = pick([2, 3, 4, 5]); ctx = L3("Un gimnàs cobra {b} € de matrícula i {m} € per cada sessió.", "Un gimnasio cobra {b} € de matrícula y {m} € por cada sesión.", "A gym charges a €{b} joining fee and €{m} per session."); }
      k = t === 1 ? pick([20, 30, 40, 50, 60]) : rint(3, 15);
      var cost = Math.round((b + m * k) * 100) / 100, unit = [L3("km", "km", "km"), L3("minuts", "minutos", "minutes"), L3("sessions", "sesiones", "sessions")][t];
      var fx = "f(x)=" + nf(b) + "+" + nf(m) + "x";
      return { num: ask ? k : cost,
        q: function () { var c = fill(T(ctx), { b: nf(b).replace("\\dc ", ","), m: nf(m).replace("\\dc ", ",") }); return c + " " + (ask ? fill(T(L3("Si has pagat {c} €, quants {u} has fet servir?", "Si has pagado {c} €, ¿cuántos {u} has usado?", "If you paid €{c}, how many {u} did you use?")), { c: nf(cost).replace("\\dc ", ","), u: T(unit) }) : fill(T(L3("Quant costen {k} {u}? (en €)", "¿Cuánto cuestan {k} {u}? (en €)", "How much do {k} {u} cost? (in €)")), { k: k, u: T(unit) })); },
        s: function () { return tex(fx) + " → " + (ask ? tex(nf(b) + "+" + nf(m) + "x=" + nf(cost) + "\\Rightarrow " + nf(m) + "x=" + nf(cost - b) + "\\Rightarrow \\boxed{x=" + k + "}") : tex("f(" + k + ")=" + nf(b) + "+" + nf(m) + "\\cdot" + k + "=\\boxed{" + nf(cost) + "}")); } };
    }
  };
  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, res = 0, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore"), ob = w.querySelector(".dopts");
    function paint() {
      dq.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (ob) {
        ob.innerHTML = "";
        q.opts.forEach(function (o, j) {
          var b = document.createElement("button"); b.type = "button"; b.className = "btn"; b.innerHTML = rtex(T(o));
          if (done) { b.disabled = true; if (j === q.ans) b.classList.add("right"); else if (j === res.pick) b.classList.add("wrong"); }
          b.addEventListener("click", function () { check(j); }); ob.appendChild(b);
        });
      }
      if (done) info.innerHTML = (res.good ? '<span class="ok">✓ ' + u("right") + "</span>" : '<span class="ko">✗ ' + u("wrong") + "</span>") + '<div class="dsol">' + u("sol") + " " + q.s() + "</div>";
    }
    function check(j) {
      if (done) return;
      var good;
      if (q.opts) good = j === q.ans;
      else if (q.pair) {
        var p = pairIn(inp.value); if (!p) { info.innerHTML = warn(u("pair")); return; }
        good = q.pair.some(function (P) { return near(P[0], p[0]) && near(P[1], p[1]); });
      } else {
        var v = numIn(inp.value); if (v === null) { info.innerHTML = warn(u("num")); return; }
        good = Math.abs(v - q.num) < 1e-6;
      }
      done = true; tot++; res = { good: good, pick: j }; if (good) ok++;
      paint();
    }
    function fresh() { q = GEN[kind](); done = false; if (inp) inp.value = ""; info.innerHTML = ""; paint(); }
    var cb = w.querySelector('[data-a="check"]'); if (cb) cb.addEventListener("click", function () { check(); });
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); if (inp) inp.focus(); });
    if (inp) inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    onLang(paint);
  }
  window.FM7 = { parseExpr: parseExpr, ev: ev, etex: etex, imageSteps: imageSteps, PL: PL, study: study, settex: settex, value: value, randPL: randPL, GEN: GEN, SETS: SETS, numIn: numIn, pairIn: pairIn };

  /* ---------- qüestionari ---------- */
  var QUIZ = [
/*QUIZ*/
  ];

  var answers = {};
  function wQuiz() {
    var box = document.getElementById("quiz-box"), score = document.getElementById("quiz-score");
    if (!box) return;
    function render() {
      box.innerHTML = ""; var ok = 0, done = 0;
      QUIZ.forEach(function (q, i) {
        var d = document.createElement("div"); d.className = "q";
        d.innerHTML = '<p class="qt">' + (i + 1) + ". " + rtex(q.q[lang]) + '</p><div class="opts"></div><div class="fb"></div>';
        var opts = d.querySelector(".opts"), fb = d.querySelector(".fb");
        q.o.forEach(function (o, j) {
          var b = document.createElement("button"); b.type = "button"; b.innerHTML = rtex(o[lang] || o.va);
          if (answers[i] != null) {
            b.disabled = true;
            if (j === q.a) b.classList.add("right"); else if (j === answers[i]) b.classList.add("wrong");
          }
          b.addEventListener("click", function () { answers[i] = j; render(); });
          opts.appendChild(b);
        });
        if (answers[i] != null) { done++; if (answers[i] === q.a) ok++; fb.innerHTML = "<strong>" + (answers[i] === q.a ? "✓ " + u("right") : "✗ " + u("wrong")) + "</strong> " + rtex(q.e[lang]); }
        box.appendChild(d);
      });
      score.textContent = done ? u("score") + ": " + ok + " / " + QUIZ.length : "";
    }
    document.getElementById("quiz-reset").addEventListener("click", function () { answers = {}; render(); });
    onLang(render);
  }

  /* ---------- passos ---------- */
  function wSteps() {
    document.querySelectorAll(".steps").forEach(function (s) {
      var steps = [].slice.call(s.children).filter(function (c) { return c.classList.contains("step"); });
      if (steps.length < 2) return;
      s.classList.add("js");
      var shown = 1, ctl = document.createElement("div"); ctl.className = "steps-ctl";
      var bn = document.createElement("button"), ba = document.createElement("button"), cnt = document.createElement("span");
      bn.type = ba.type = "button"; bn.className = "btn primary"; ba.className = "btn"; cnt.className = "step-count";
      ctl.appendChild(bn); ctl.appendChild(ba); ctl.appendChild(cnt); s.after(ctl);
      function upd() {
        steps.forEach(function (st, i) { st.classList.toggle("hidden", i >= shown); });
        bn.textContent = u("next") + " →"; bn.disabled = shown >= steps.length;
        ba.textContent = shown >= steps.length ? u("reset") : u("all");
        cnt.textContent = u("step") + " " + shown + " " + u("of") + " " + steps.length;
      }
      bn.addEventListener("click", function () { if (shown < steps.length) { shown++; upd(); steps[shown - 1].scrollIntoView({ block: "nearest", behavior: "smooth" }); } });
      ba.addEventListener("click", function () { shown = shown >= steps.length ? 1 : steps.length; upd(); });
      onLang(upd);
    });
  }

  /* ---------- índex, progrés i seccions estudiades ---------- */
  function wNav() {
    var links = [].slice.call(document.querySelectorAll("#toc-list a")), secs = links.map(function (a) { return document.querySelector(a.getAttribute("href")); });
    var bar = document.getElementById("progress"), top = document.getElementById("to-top");
    function onScroll() {
      var h = document.documentElement, max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? h.scrollTop / max * 100 : 0) + "%";
      top.classList.toggle("show", h.scrollTop > 800);
      var y = window.scrollY + 140, idx = 0;
      secs.forEach(function (s, i) { if (s && s.offsetTop <= y) idx = i; });
      links.forEach(function (a, i) { a.classList.toggle("active", i === idx); });
    }
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
    top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
    var done = {}; try { done = JSON.parse(store(UNIT_KEY) || "{}") || {}; } catch (e) {}
    var heads = document.querySelectorAll("section.unit[id^='s'] .sec-head");
    heads.forEach(function (hd) {
      var id = hd.parentNode.id, b = document.createElement("button"); b.type = "button"; b.className = "done-btn";
      function upd() { b.setAttribute("aria-pressed", String(!!done[id])); b.textContent = (done[id] ? "✓ " + u("studied") : "○ " + u("mark")); }
      b.addEventListener("click", function () { done[id] = !done[id]; store(UNIT_KEY, JSON.stringify(done)); upd(); meter(); });
      hd.appendChild(b); onLang(upd);
    });
    function meter() {
      var n = 0; links.forEach(function (a) { var id = a.getAttribute("href").slice(1); a.classList.toggle("done", !!done[id]); if (done[id]) n++; });
      document.getElementById("meter").style.width = (n / NSEC * 100) + "%"; document.getElementById("meter-n").textContent = n;
    }
    meter();
    var d = document.getElementById("toc-d");
    var mq = window.matchMedia("(max-width: 960px)");
    d.open = !mq.matches;
    if (mq.addEventListener) mq.addEventListener("change", function () { d.open = !mq.matches; });
    links.forEach(function (a) { a.addEventListener("click", function () { if (window.matchMedia("(max-width: 960px)").matches) d.open = false; }); });
  }

  /* ---------- idioma i tema ---------- */
  var ICON = {
    moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
  };
  function curTheme() { var t = root.getAttribute("data-theme"); return t || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"); }
  function wChrome() {
    var tb = document.getElementById("theme-btn");
    function paintTheme() { tb.innerHTML = curTheme() === "dark" ? ICON.sun : ICON.moon; tb.setAttribute("aria-label", u("theme")); }
    tb.addEventListener("click", function () { var n = curTheme() === "dark" ? "light" : "dark"; root.setAttribute("data-theme", n); store("theme", n); paintTheme(); });
    var btns = document.querySelectorAll("[data-setlang]");
    function paintLang() { btns.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.setlang === lang)); }); }
    btns.forEach(function (b) { b.addEventListener("click", function () { setLang(b.dataset.setlang); }); });
    onLang(function () { paintTheme(); paintLang(); });
  }

  var TITLES = { va: "Funcions · FentMates", es: "Funciones · FentMates", en: "Functions · FentMates" };
  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l; root.setAttribute("data-lang", l); root.lang = HTML_LANG[l]; document.title = TITLES[l]; store("lang", l);
    try { var url = new URL(location.href); if (url.searchParams.has("lang")) { url.searchParams.set("lang", l); history.replaceState(null, "", url); } } catch (e) {}
    refreshers.forEach(function (fn) { fn(); });
  }

  function init() {
    document.title = TITLES[lang];
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, {
        delimiters: [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }],
        ignoredClasses: ["widget"], throwOnError: false, strict: "ignore", macros: KOPT.macros, trust: KOPT.trust
      });
    }
    wChrome(); wSteps(); wNav();
    wVline(); wMachine(); wPlot(); wRead(); document.querySelectorAll(".w-anal").forEach(wAnal);
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
