(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-3eso-u8-done", NSEC = 8;

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

  /* ======================================================================
     unitat 8: funció lineal i quadràtica
     ====================================================================== */
  /* nombre com a fracció si té denominador petit: 0.666… -> \frac{2}{3} */
  function qf(v) {
    if (!isFinite(v)) return nf(v);
    if (near(v, Math.round(v))) return nf(Math.round(v));
    for (var d = 2; d <= 30; d++) { var p = v * d; if (Math.abs(p - Math.round(p)) < 1e-7) { if (d === 2 || d === 4 || d === 5 || d === 10 || d === 20 || d === 25) return nf(v); return (v < 0 ? "-" : "") + "\\frac{" + Math.abs(Math.round(p)) + "}{" + d + "}"; } }
    return nf(v);
  }
  function qfp(v) { return v < 0 ? "(" + qf(v) + ")" : qf(v); }
  /* polinomi en TeX a partir de [[coef, "x^2"], [coef, "x"], [coef, ""]] */
  function polyT(ts) {
    var s = "";
    ts.forEach(function (t) {
      var c = t[0]; if (near(c, 0)) return;
      var a = Math.abs(c), body = t[1] ? (near(a, 1) ? "" : qf(a)) + t[1] : qf(a);
      s += (c < 0 ? "-" : s ? "+" : "") + body;
    });
    return s || "0";
  }
  function lineT(m, n) { return polyT([[m, "x"], [n, ""]]); }
  function quadT(a, b, c) { return polyT([[a, "x^2"], [b, "x"], [c, ""]]); }
  /* arbres d'expressió per a dibuixar amb plot() */
  function N(v) { return { t: "n", v: v }; }
  function linE(m, n) { return { t: "+", a: { t: "*", a: N(m), b: { t: "x" } }, b: N(n) }; }
  function quadE(a, b, c) { return { t: "+", a: { t: "+", a: { t: "*", a: N(a), b: { t: "^", a: { t: "x" }, b: N(2) } }, b: { t: "*", a: N(b), b: { t: "x" } } }, b: N(c) }; }
  /* lectura d'una fórmula lineal o quadràtica escrita per l'alumne ("y = 2x − 3") */
  function readF(raw) { return parseExpr(String(raw).replace(/^\s*[yf]\s*(\(\s*x\s*\))?\s*=/i, "")); }
  function coefs(e) {
    if (!e) return null;
    var c = ev(e, 0), p = ev(e, 1), q = ev(e, -1), a = (p + q) / 2 - c, b = (p - q) / 2;
    var ok = [2, -3, 0.5, 4.25].every(function (t) { var v = ev(e, t); return isFinite(v) && Math.abs(v - (a * t * t + b * t + c)) < 1e-7 * Math.max(1, Math.abs(v)); });
    return ok ? { a: near(a, 0) ? 0 : a, b: near(b, 0) ? 0 : b, c: near(c, 0) ? 0 : c } : null;
  }
  function trend(m) { return m > 0 ? L3("creixent", "creciente", "increasing") : m < 0 ? L3("decreixent", "decreciente", "decreasing") : L3("constant", "constante", "constant"); }
  /* finestra entera que conté uns punts */
  function winPts(ps, pad, minR) {
    var xs = ps.map(function (P) { return P[0]; }).concat([0]), ys = ps.map(function (P) { return P[1]; }).concat([0]);
    var a = Math.floor(Math.min.apply(null, xs)) - pad, b = Math.ceil(Math.max.apply(null, xs)) + pad, c = Math.floor(Math.min.apply(null, ys)) - pad, d = Math.ceil(Math.max.apply(null, ys)) + pad;
    if (b - a < minR) { var e = Math.ceil((minR - (b - a)) / 2); a -= e; b += e; }
    if (d - c < minR) { var f = Math.ceil((minR - (d - c)) / 2); c -= f; d += f; }
    return { xr: [a, b], yr: [c, d] };
  }
  function slopeTri(x0, y0, m, run) {
    run = run || 1;
    return [{ pts: [[x0, y0], [x0 + run, y0]], cls: "tri" }, { pts: [[x0 + run, y0], [x0 + run, y0 + m * run]], cls: "tri" }];
  }
  function segSet(w, cb) { var bs = w.querySelectorAll(".seg button"); bs.forEach(function (b) { b.addEventListener("click", function () { bs.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); cb(b.dataset.k, b); }); }); return bs; }

  /* ---------- giny: y = mx (+ n) amb lliscadors ---------- */
  function wLine(w) {
    var mode = w.dataset.mode, out = w.querySelector(".gout"), info = w.querySelector(".info");
    var sm = w.querySelector('input[data-k="m"]'), sn = w.querySelector('input[data-k="n"]');
    function paint() {
      var m = +sm.value, n = sn ? +sn.value : 0;
      w.querySelector(".mv").innerHTML = tex("m=" + nf(m)); if (sn) w.querySelector(".nv").innerHTML = tex("n=" + nf(n));
      var xs = [-2, -1, 0, 1, 2, 3], tb = '<table class="data tv"><tbody><tr><th>' + tex("x") + "</th>" + xs.map(function (x) { return "<td>" + tex(nf(x)) + "</td>"; }).join("") + "</tr><tr><th>" + tex("y") + "</th>" + xs.map(function (x) { return "<td>" + tex(nf(m * x + n)) + "</td>"; }).join("") + "</tr></tbody></table>";
      var dots = [{ x: 0, y: n, cls: "cut", r: 6, lab: mode === "prop" ? "O" : tex0("(0,\\," + nf(n) + ")") }];
      if (mode === "prop") dots.push({ x: 1, y: m, cls: "pt p0", r: 5, lab: "(1, " + nf(m).replace("\\dc ", ",").replace("-", "−") + ")" });
      out.innerHTML = '<div class="gcol"><p class="big">' + tex("y=" + lineT(m, n)) + '</p><div class="tbl-wrap">' + tb + "</div></div>"
        + plot({ xr: [-6, 6], yr: [-6, 6], fn: [{ e: linE(m, n) }], curves: near(m, 0) ? [] : slopeTri(0, n, m, 1), dots: dots });
      var t = mode === "prop"
        ? fill(T(L3("És una funció de proporcionalitat directa: la gràfica passa per l'origen {O}. Quan la {x} augmenta 1, la {y} augmenta {m} (triangle de color): la constant de proporcionalitat i el pendent valen {mm}. La funció és <b>{tr}</b>.",
            "Es una función de proporcionalidad directa: la gráfica pasa por el origen {O}. Cuando la {x} aumenta 1, la {y} aumenta {m} (triángulo de color): la constante de proporcionalidad y la pendiente valen {mm}. La función es <b>{tr}</b>.",
            "It is a direct proportion: the graph goes through the origin {O}. When {x} goes up by 1, {y} goes up by {m} (coloured triangle): the constant of proportionality and the slope are {mm}. The function is <b>{tr}</b>.")), { O: tex("(0,\\,0)"), x: tex("x"), y: tex("y"), m: tex(nf(m)), mm: tex("m=" + nf(m)), tr: T(trend(m)) })
        : fill(T(L3("Pendent {m}: la funció és <b>{tr}</b>. Ordenada en l'origen {n}: talla l'eix {Y} en {P}.", "Pendiente {m}: la función es <b>{tr}</b>. Ordenada en el origen {n}: corta el eje {Y} en {P}.", "Slope {m}: the function is <b>{tr}</b>. {Y}-intercept {n}: it crosses the {Y} axis at {P}.")), { m: tex("m=" + nf(m)), n: tex("n=" + nf(n)), tr: T(trend(m)), Y: tex("Y"), P: tex("(0,\\," + nf(n) + ")") })
          + (near(m, 0) ? " " + T(L3("Amb pendent 0 és una <b>funció constant</b>: una recta horitzontal.", "Con pendiente 0 es una <b>función constante</b>: una recta horizontal.", "With slope 0 it is a <b>constant function</b>: a horizontal line.")) : "")
          + (near(n, 0) && !near(m, 0) ? " " + T(L3("Amb {n} passa per l'origen: és de proporcionalitat directa.", "Con {n} pasa por el origen: es de proporcionalidad directa.", "With {n} it goes through the origin: it is a direct proportion.")).replace("{n}", tex("n=0")) : "");
      info.innerHTML = "💡 " + t;
    }
    [sm, sn].forEach(function (s) { if (s) s.addEventListener("input", paint); });
    quickBind(w, function (v) { sm.value = v[0]; if (sn) sn.value = v[1]; paint(); });
    onLang(paint);
  }
  /* etiqueta de text per a l'SVG (sense TeX) */
  function tex0(s) { return s.replace(/\\,/g, " ").replace(/\\dc /g, ",").replace(/-/g, "−"); }

  /* ---------- giny: recta que passa per dos punts ---------- */
  function lineSteps(P, Q) {
    var rows = [], dx = Q[0] - P[0], dy = Q[1] - P[1];
    if (near(dx, 0)) {
      if (near(dy, 0)) return { rows: [], bad: true };
      return { rows: [T(L3("Els dos punts tenen la mateixa abscissa: és la recta vertical ", "Los dos puntos tienen la misma abscisa: es la recta vertical ", "Both points have the same x: it is the vertical line ")) + tex("x=" + nf(P[0])) + T(L3(", que <b>no és una funció</b>.", ", que <b>no es una función</b>.", ", which is <b>not a function</b>."))], vert: true };
    }
    var m = dy / dx, n = P[1] - m * P[0];
    rows.push(tex("m=\\dfrac{y_2-y_1}{x_2-x_1}=\\dfrac{" + nf(Q[1]) + "-" + nfp(P[1]) + "}{" + nf(Q[0]) + "-" + nfp(P[0]) + "}=\\dfrac{" + nf(dy) + "}{" + nf(dx) + "}=" + qf(m)));
    rows.push(T(L3("Equació punt-pendent amb ", "Ecuación punto-pendiente con ", "Point-slope form with ")) + tex("(" + nf(P[0]) + ",\\," + nf(P[1]) + ")") + ": " + tex("y-" + nfp(P[1]) + "=" + qf(m) + "\\,(x-" + nfp(P[0]) + ")").replace(/-\((-[\d\\dc ]+)\)/g, function (_, a) { return "+" + a.slice(1); }));
    rows.push(T(L3("Aïllem la ", "Despejamos la ", "Solve for ")) + tex("y") + ": " + tex("\\boxed{y=" + lineT(m, n) + "}") + " " + T(L3("(pendent ", "(pendiente ", "(slope ")) + tex(qf(m)) + T(L3(", ordenada en l'origen ", ", ordenada en el origen ", ", intercept ")) + tex(qf(n)) + ")");
    return { rows: rows, m: m, n: n };
  }
  function wTwo() {
    var w = document.getElementById("w-two"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), g = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = ""; out.innerHTML = ""; g.innerHTML = "";
      var P = pairIn(I.p.value), Q = pairIn(I.q.value);
      if (!P || !Q) { info.innerHTML = warn(u("pair")); return; }
      var r = lineSteps(P, Q);
      if (r.bad) { info.innerHTML = warn(T(L3("Els dos punts són el mateix: per un sol punt passen infinites rectes.", "Los dos puntos son el mismo: por un solo punto pasan infinitas rectas.", "Both points are the same: infinitely many lines go through one point."))); return; }
      out.innerHTML = rows2html(r.rows);
      var W0 = winPts([P, Q], 2, 10), o = { xr: W0.xr, yr: W0.yr, dots: [{ x: P[0], y: P[1], cls: "pt p0", r: 5, lab: "P" }, { x: Q[0], y: Q[1], cls: "pt p1", r: 5, lab: "Q" }] };
      if (r.vert) o.vl = P[0]; else { o.fn = [{ e: linE(r.m, r.n) }]; o.curves = slopeTri(P[0], P[1], r.m, Q[0] - P[0]); }
      g.innerHTML = plot(o);
    }
    [I.p, I.q].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.p.value = v[0]; I.q.value = v[1]; paint(); });
    onLang(paint);
  }

  /* ---------- giny: aplicacions (situacions lineals) ---------- */
  var APL = [
    { n: L3("Taxi", "Taxi", "Taxi"), m: 1.2, b: 3, xr: [-1, 21], yr: [-3, 30], xmax: 20, xl: "km", yl: "€", xs: 2, ys: 5, f: "y=1{,}2x+3",
      say: function (x, y) { return fill(T(L3("Un trajecte de {x} km costa {y} €: 3 € de baixada de bandera més 1,20 € per km.", "Un trayecto de {x} km cuesta {y} €: 3 € de bajada de bandera más 1,20 € por km.", "A {x} km trip costs €{y}: €3 to get in plus €1.20 per km.")), { x: tex(nf(x)), y: tex(nf(y)) }); } },
    { n: L3("Temperatura", "Temperatura", "Temperature"), m: 1.8, b: 32, xr: [-22, 42], yr: [-20, 110], xmax: 40, xmin: -20, xl: "°C", yl: "°F", xs: 10, ys: 20, gx: 5, gy: 10, f: "F=1{,}8C+32",
      say: function (x, y) { return fill(T(L3("{x} °C són {y} °F. Cada grau Celsius equival a 1,8 graus Fahrenheit, i 0 °C són 32 °F.", "{x} °C son {y} °F. Cada grado Celsius equivale a 1,8 grados Fahrenheit, y 0 °C son 32 °F.", "{x} °C is {y} °F. Each Celsius degree is 1.8 Fahrenheit degrees, and 0 °C is 32 °F.")), { x: tex(nf(x)), y: tex(nf(y)) }); } },
    { n: L3("Dipòsit", "Depósito", "Tank"), m: -25, b: 500, xr: [-2, 22], yr: [-40, 560], xmax: 20, xl: "t (min)", yl: "V (L)", xs: 5, ys: 100, gx: 5, gy: 50, f: "V=500-25t",
      say: function (x, y) { return fill(T(L3("Al minut {x} queden {y} litres: es buida a 25 L/min (pendent negatiu) i als 20 minuts està buit.", "En el minuto {x} quedan {y} litros: se vacía a 25 L/min (pendiente negativa) y a los 20 minutos está vacío.", "At minute {x} there are {y} litres left: it drains at 25 L/min (negative slope) and is empty after 20 minutes.")), { x: tex(nf(x)), y: tex(nf(y)) }); } },
    { n: L3("Ciclista", "Ciclista", "Cyclist"), m: 18, b: 10, xr: [-0.5, 5.5], yr: [-10, 110], xmax: 5, xl: "t (h)", yl: "d (km)", xs: 1, ys: 20, gy: 10, step: 0.25, f: "d=10+18t",
      say: function (x, y) { return fill(T(L3("Ix a 10 km de casa i s'allunya a 18 km/h (velocitat constant): al cap de {x} h està a {y} km de casa.", "Sale a 10 km de casa y se aleja a 18 km/h (velocidad constante): al cabo de {x} h está a {y} km de casa.", "Starts 10 km from home and rides away at 18 km/h (constant speed): after {x} h they are {y} km from home.")), { x: tex(nf(x)), y: tex(nf(y)) }); } }
  ];
  function wApl() {
    var w = document.getElementById("w-apl"); if (!w) return;
    var out = w.querySelector(".gout"), info = w.querySelector(".info"), sl = w.querySelector('input[type="range"]'), cur = APL[0];
    function paint() {
      var x0 = cur.xmin || 0, x = x0 + (cur.xmax - x0) * sl.value / 100, st = cur.step || 1;
      x = Math.round(x / st) * st;
      var y = cur.m * x + cur.b;
      out.innerHTML = '<div class="gcol"><p class="big">' + tex(cur.f) + "</p><p>" + T(L3("Pendent", "Pendiente", "Slope")) + " " + tex(nf(cur.m)) + " · " + T(L3("ordenada en l'origen", "ordenada en el origen", "intercept")) + " " + tex(nf(cur.b)) + "</p></div>"
        + plot({ xr: cur.xr, yr: cur.yr, W: 360, H: 260, xl: cur.xl, yl: cur.yl, xs: cur.xs, ys: cur.ys, gx: cur.gx || 1, gy: cur.gy || 1, fn: [{ e: linE(cur.m, cur.b), from: x0, to: cur.xmax }], vl: x, dots: [{ x: x, y: y, cls: "cut", r: 6 }] });
      info.innerHTML = cur.say(x, y);
    }
    sl.addEventListener("input", paint);
    var bs = segSet(w, function (k) { cur = APL[+k]; paint(); });
    onLang(function () { bs.forEach(function (b) { b.textContent = T(APL[+b.dataset.k].n); }); paint(); });
  }

  /* ---------- giny: dues rectes ---------- */
  function cutSteps(m1, n1, m2, n2, name) {
    var rows = [], x = (n2 - n1) / (m1 - m2), y = m1 * x + n1;
    rows.push(T(L3("Igualem les dues expressions de la ", "Igualamos las dos expresiones de la ", "Set the two expressions for ")) + tex("y") + ": " + tex(lineT(m1, n1) + "=" + lineT(m2, n2)));
    rows.push(tex(polyT([[m1, "x"], [-m2, "x"]]) + "=" + polyT([[n2, ""], [-n1, ""]]) + "\\Rightarrow " + qf(m1 - m2) + "x=" + qf(n2 - n1) + "\\Rightarrow x=" + qf(x)).replace(/\\Rightarrow 1x=/, "\\Rightarrow x=").replace(/\\Rightarrow -1x=/, "\\Rightarrow -x="));
    rows.push(T(L3("Substituïm en la primera: ", "Sustituimos en la primera: ", "Substitute into the first: ")) + tex("y=" + polyT([[m1, "\\cdot" + qfp(x)]]).replace(/^(-?)\\cdot/, "$1") + (near(n1, 0) ? "" : (n1 < 0 ? "-" : "+") + qf(Math.abs(n1))) + "=" + qf(y)));
    rows.push(T(L3("Es tallen en el punt ", "Se cortan en el punto ", "They meet at the point ")) + tex("\\boxed{(" + qf(x) + ",\\," + qf(y) + ")}"));
    return { rows: rows, x: x, y: y };
  }
  function wPair() {
    var w = document.getElementById("w-pair"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), g = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = ""; out.innerHTML = ""; g.innerHTML = "";
      var A = coefs(readF(I.r.value)), B = coefs(readF(I.s.value));
      if (!A || !B || !near(A.a, 0) || !near(B.a, 0)) { info.innerHTML = warn(T(L3("Escriu dues funcions lineals, per exemple 2x−1 i −x+5.", "Escribe dos funciones lineales, por ejemplo 2x−1 y −x+5.", "Type two linear functions, for example 2x−1 and −x+5."))); return; }
      var m1 = A.b, n1 = A.c, m2 = B.b, n2 = B.c, rows = [tex("r:\\ y=" + lineT(m1, n1) + "\\qquad s:\\ y=" + lineT(m2, n2))], o = { xr: [-6, 6], yr: [-6, 6], fn: [{ e: linE(m1, n1) }, { e: linE(m2, n2), cls: "c1" }] }, msg;
      if (near(m1, m2)) {
        rows.push(fill(T(L3("Tenen el mateix pendent ({m}).", "Tienen la misma pendiente ({m}).", "They have the same slope ({m}).")), { m: tex("m=" + qf(m1)) }));
        msg = near(n1, n2) ? T(L3("També tenen la mateixa ordenada en l'origen: són <b>coincidents</b> (la mateixa recta, infinits punts comuns).", "También tienen la misma ordenada en el origen: son <b>coincidentes</b> (la misma recta, infinitos puntos comunes).", "They also have the same intercept: they are <b>coincident</b> (the same line, infinitely many common points)."))
          : T(L3("Les ordenades en l'origen són diferents: són <b>paral·leles</b> i no es tallen mai.", "Las ordenadas en el origen son distintas: son <b>paralelas</b> y no se cortan nunca.", "The intercepts are different: they are <b>parallel</b> and never meet."));
        if (near(n1, n2)) o.fn[1].cls = "c1 dash";
      } else {
        rows.push(fill(T(L3("Pendents diferents ({a} i {b}): són <b>secants</b>, es tallen en un punt.", "Pendientes distintas ({a} y {b}): son <b>secantes</b>, se cortan en un punto.", "Different slopes ({a} and {b}): they are <b>intersecting</b>, they meet at one point.")), { a: tex(qf(m1)), b: tex(qf(m2)) }));
        var c = cutSteps(m1, n1, m2, n2); rows = rows.concat(c.rows);
        var W0 = winPts([[c.x, c.y], [0, n1], [0, n2]], 2, 12); o.xr = W0.xr; o.yr = W0.yr;
        if (o.xr[1] - o.xr[0] > 40 || o.yr[1] - o.yr[0] > 60) { o.xr = [Math.min(-2, Math.floor(c.x) - 2), Math.max(2, Math.ceil(c.x) + 2)]; }
        o.dots = [{ x: c.x, y: c.y, cls: "cut", r: 6, lab: "(" + tex0(qf(c.x).indexOf("frac") >= 0 ? nf(c.x) : qf(c.x)) + ", " + tex0(qf(c.y).indexOf("frac") >= 0 ? nf(c.y) : qf(c.y)) + ")" }];
        msg = T(L3("El punt de tall és la solució del sistema format per les dues equacions.", "El punto de corte es la solución del sistema formado por las dos ecuaciones.", "The meeting point is the solution of the system formed by the two equations."));
      }
      out.innerHTML = rows2html(rows); g.innerHTML = plot(o); info.innerHTML = "💡 " + msg;
    }
    [I.r, I.s].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.r.value = v[0]; I.s.value = v[1]; paint(); });
    onLang(paint);
  }

  /* ---------- paràboles ---------- */
  function vtx(a, b, c) { var xv = -b / (2 * a); return [xv, a * xv * xv + b * xv + c]; }
  function quadWin(a, b, c, extra) {
    var V = vtx(a, b, c), ps = [V, [0, c]].concat(extra || []), x0 = Math.floor(Math.min(V[0] - 4, -1)), x1 = Math.ceil(Math.max(V[0] + 4, 1));
    var W0 = winPts(ps, 1, 8), y0 = W0.yr[0], y1 = W0.yr[1];
    x0 = Math.min(x0, W0.xr[0]); x1 = Math.max(x1, W0.xr[1]);
    if (a > 0) y1 = Math.max(y1, Math.min(Math.ceil(V[1]) + 9, y1 + 8)); else y0 = Math.min(y0, Math.max(Math.floor(V[1]) - 9, y0 - 8));
    return { xr: [x0, x1], yr: [y0, y1] };
  }
  function rootsQ(a, b, c) { var D = b * b - 4 * a * c; if (D < -1e-9) return { D: D, r: [] }; if (Math.abs(D) < 1e-9) return { D: 0, r: [-b / (2 * a)] }; var s = Math.sqrt(D); return { D: D, r: [(-b - s) / (2 * a), (-b + s) / (2 * a)].sort(function (p, q) { return p - q; }) }; }
  function rq(v) { var q = qf(v); return q.indexOf("frac") < 0 && !near(v * 1000, Math.round(v * 1000)) ? "\\approx " + nf(Math.round(v * 100) / 100) : q; }
  /* estudi complet d'una paràbola, pas a pas */
  function paraStudy(a, b, c) {
    var V = vtx(a, b, c), rows = [], R = rootsQ(a, b, c), D = R.D;
    rows.push("<b>1.</b> " + fill(T(L3("Com que {a}, les branques van cap <b>{d}</b> i el vèrtex és un <b>{t}</b>.", "Como {a}, las ramas van hacia <b>{d}</b> y el vértice es un <b>{t}</b>.", "Since {a}, the arms point <b>{d}</b> and the vertex is a <b>{t}</b>.")), { a: tex("a=" + qf(a) + (a > 0 ? ">0" : "<0")), d: T(a > 0 ? L3("dalt", "arriba", "up") : L3("baix", "abajo", "down")), t: T(a > 0 ? L3("mínim", "mínimo", "minimum") : L3("màxim", "máximo", "maximum")) }));
    rows.push("<b>2.</b> " + T(L3("Vèrtex: ", "Vértice: ", "Vertex: ")) + tex("x_v=\\dfrac{-b}{2a}=\\dfrac{" + qf(-b) + "}{2\\cdot" + qfp(a) + "}=" + qf(V[0])) + ", " + tex("y_v=" + (near(a, 1) ? "" : near(a, -1) ? "-" : qf(a) + "\\cdot") + qfp(V[0]) + "^2" + (near(b, 0) ? "" : (b < 0 ? "-" : "+") + qf(Math.abs(b)) + "\\cdot" + qfp(V[0])) + (near(c, 0) ? "" : (c < 0 ? "-" : "+") + qf(Math.abs(c))) + "=" + qf(V[1])) + " → " + tex("V=\\boxed{(" + qf(V[0]) + ",\\," + qf(V[1]) + ")}") + ". " + T(L3("Eix de simetria: ", "Eje de simetría: ", "Axis of symmetry: ")) + tex("x=" + qf(V[0])) + ".");
    rows.push("<b>3.</b> " + T(L3("Tall amb l'eix ", "Corte con el eje ", "Crossing the ")) + tex("Y") + T(L3(" (fem x = 0): ", " (hacemos x = 0): ", " axis (set x = 0): ")) + tex("(0,\\," + qf(c) + ")"));
    var r4 = "<b>4.</b> " + T(L3("Talls amb l'eix ", "Cortes con el eje ", "Crossing the ")) + tex("X") + T(L3(" (resolem ", " (resolvemos ", " axis (solve ")) + tex(quadT(a, b, c) + "=0") + "): ";
    if (near(b, 0) || near(c, 0)) r4 += T(L3("és una equació incompleta. ", "es una ecuación incompleta. ", "it's an incomplete equation. "));
    r4 += tex("\\Delta=b^2-4ac=" + qfp(b) + "^2-4\\cdot" + qfp(a) + "\\cdot" + qfp(c) + "=" + qf(D)) + ". ";
    if (!R.r.length) r4 += T(L3("Com que és negatiu, <b>no talla</b> l'eix ", "Como es negativo, <b>no corta</b> el eje ", "It's negative, so it <b>doesn't cross</b> the ")) + tex("X") + ".";
    else if (R.r.length === 1) r4 += T(L3("És zero: el toca només en el vèrtex, ", "Es cero: lo toca solo en el vértice, ", "It's zero: it only touches it at the vertex, ")) + tex("(" + qf(R.r[0]) + ",\\,0)") + ".";
    else r4 += tex("x=\\dfrac{" + qf(-b) + "\\pm\\sqrt{" + qf(D) + "}}{" + qf(2 * a) + "}" + (near(Math.sqrt(D), Math.round(Math.sqrt(D))) ? "=\\dfrac{" + qf(-b) + "\\pm" + Math.round(Math.sqrt(D)) + "}{" + qf(2 * a) + "}" : "")) + " → " + R.r.map(function (r) { return tex("(" + rq(r) + ",\\,0)"); }).join(T(L3(" i ", " y ", " and ")));
    rows.push(r4);
    var xs = [-2, -1, 0, 1, 2].map(function (k) { return V[0] + k; }), xsN = xs.every(function (t) { return near(t, Math.round(t)); }) ? xs : [-2, -1, 0, 1, 2].map(function (k) { return Math.round(V[0]) + k; });
    rows.push("<b>5.</b> " + T(L3("Taula de valors al voltant del vèrtex (els valors són simètrics):", "Tabla de valores alrededor del vértice (los valores son simétricos):", "Table of values around the vertex (values are symmetric):")) + '<div class="tbl-wrap"><table class="data tv"><tbody><tr><th>' + tex("x") + "</th>" + xsN.map(function (t) { return "<td>" + tex(qf(t)) + "</td>"; }).join("") + "</tr><tr><th>" + tex("y") + "</th>" + xsN.map(function (t) { return "<td>" + tex(qf(a * t * t + b * t + c)) + "</td>"; }).join("") + "</tr></tbody></table></div>");
    rows.push("<b>6.</b> " + (a > 0 ? fill(T(L3("Decreix en {d} i creix en {c}. Mínim en {V}.", "Decrece en {d} y crece en {c}. Mínimo en {V}.", "Decreasing on {d} and increasing on {c}. Minimum at {V}.")), { d: tex("(-\\infty,\\," + qf(V[0]) + ")"), c: tex("(" + qf(V[0]) + ",\\,+\\infty)"), V: tex("(" + qf(V[0]) + ",\\," + qf(V[1]) + ")") })
      : fill(T(L3("Creix en {c} i decreix en {d}. Màxim en {V}.", "Crece en {c} y decrece en {d}. Máximo en {V}.", "Increasing on {c} and decreasing on {d}. Maximum at {V}.")), { c: tex("(-\\infty,\\," + qf(V[0]) + ")"), d: tex("(" + qf(V[0]) + ",\\,+\\infty)"), V: tex("(" + qf(V[0]) + ",\\," + qf(V[1]) + ")") })));
    return { rows: rows, V: V, R: R, xs: xsN };
  }
  function paraPlot(a, b, c, opt) {
    opt = opt || {};
    var V = vtx(a, b, c), R = rootsQ(a, b, c), W0 = quadWin(a, b, c, R.r.map(function (r) { return [r, 0]; }));
    var o = { xr: W0.xr, yr: W0.yr, fn: [{ e: quadE(a, b, c) }], vguides: opt.axis === false ? [] : [V[0]], dots: [], small: opt.small };
    if (opt.ref) o.fn.unshift({ e: quadE(opt.ref, 0, 0), cls: "c1 dash" });
    o.dots.push({ x: V[0], y: V[1], cls: a > 0 ? "mn" : "mx", r: 6, lab: "V", dy: a > 0 ? 18 : -8 });
    if (opt.cuts !== false) { R.r.forEach(function (r) { o.dots.push({ x: r, y: 0, cls: "cut", r: 5 }); }); if (!near(V[0], 0)) o.dots.push({ x: 0, y: c, cls: "pt p1", r: 5 }); }
    (opt.pts || []).forEach(function (t) { o.dots.push({ x: t, y: a * t * t + b * t + c, cls: "pt p0", r: 4 }); });
    return plot(o);
  }
  /* giny: y = ax² */
  function wA() {
    var w = document.getElementById("w-a"); if (!w) return;
    var sa = w.querySelector('input[data-k="a"]'), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      var a = +sa.value; if (near(a, 0)) a = sa.value = 0.25;
      w.querySelector(".av").innerHTML = tex("a=" + nf(a));
      var xs = [-2, -1, 0, 1, 2], tb = '<table class="data tv"><tbody><tr><th>' + tex("x") + "</th>" + xs.map(function (x) { return "<td>" + tex(nf(x)) + "</td>"; }).join("") + "</tr><tr><th>" + tex("y") + "</th>" + xs.map(function (x) { return "<td>" + tex(nf(a * x * x)) + "</td>"; }).join("") + "</tr></tbody></table>";
      out.innerHTML = '<div class="gcol"><p class="big">' + tex("y=" + quadT(a, 0, 0)) + '</p><div class="tbl-wrap">' + tb + '</div><p class="hint-s"><span class="key k1"></span>' + tex("y=x^2") + "</p></div>"
        + plot({ xr: [-5, 5], yr: [-7, 7], fn: [{ e: quadE(1, 0, 0), cls: "c1 dash" }, { e: quadE(a, 0, 0) }], vguides: [0], dots: [{ x: 0, y: 0, cls: a > 0 ? "mn" : "mx", r: 6, lab: "V" }].concat(xs.map(function (x) { return { x: x, y: a * x * x, cls: "pt p0", r: 4 }; })) });
      var A = Math.abs(a);
      info.innerHTML = "💡 " + fill(T(L3("Vèrtex {V}, eix de simetria l'eix {Y}. Com que {a}, les branques van cap <b>{d}</b>. ", "Vértice {V}, eje de simetría el eje {Y}. Como {a}, las ramas van hacia <b>{d}</b>. ", "Vertex {V}, axis of symmetry the {Y} axis. Since {a}, the arms point <b>{d}</b>. ")), { V: tex("(0,\\,0)"), Y: tex("Y"), a: tex("a" + (a > 0 ? ">0" : "<0")), d: T(a > 0 ? L3("dalt", "arriba", "up") : L3("baix", "abajo", "down")) })
        + T(near(A, 1) ? L3("Té la mateixa obertura que y = x².", "Tiene la misma abertura que y = x².", "It has the same width as y = x².") : A > 1 ? L3("Com que |a| > 1, és <b>més estreta</b> que y = x².", "Como |a| > 1, es <b>más estrecha</b> que y = x².", "Since |a| > 1, it is <b>narrower</b> than y = x².") : L3("Com que |a| < 1, és <b>més ampla</b> que y = x².", "Como |a| < 1, es <b>más ancha</b> que y = x².", "Since |a| < 1, it is <b>wider</b> than y = x²."));
    }
    sa.addEventListener("input", paint);
    quickBind(w, function (v) { sa.value = v[0]; paint(); });
    onLang(paint);
  }
  /* giny: y = ax² + bx + c amb lliscadors */
  function wPara() {
    var w = document.getElementById("w-para"); if (!w) return;
    var S = {}, out = w.querySelector(".gout"), info = w.querySelector(".info");
    w.querySelectorAll('input[type="range"]').forEach(function (s) { S[s.dataset.k] = s; });
    function paint() {
      var a = +S.a.value, b = +S.b.value, c = +S.c.value; if (near(a, 0)) { a = 0.5; S.a.value = 0.5; }
      ["a", "b", "c"].forEach(function (k) { w.querySelector("." + k + "v").innerHTML = tex(k + "=" + nf(+S[k].value)); });
      var V = vtx(a, b, c), R = rootsQ(a, b, c);
      out.innerHTML = '<div class="gcol"><p class="big">' + tex("y=" + quadT(a, b, c)) + "</p><p>" + T(L3("Vèrtex", "Vértice", "Vertex")) + " " + tex("V=(" + qf(V[0]) + ",\\," + qf(V[1]) + ")") + "</p><p>" + T(L3("Eix", "Eje", "Axis")) + " " + tex("x=" + qf(V[0])) + "</p><p>" + T(L3("Tall amb Y", "Corte con Y", "Y-intercept")) + " " + tex("(0,\\," + qf(c) + ")") + "</p><p>"
        + T(L3("Talls amb X", "Cortes con X", "X-intercepts")) + " " + (R.r.length ? R.r.map(function (r) { return tex("(" + rq(r) + ",\\,0)"); }).join(", ") : T(L3("cap", "ninguno", "none"))) + "</p></div>"
        + paraPlot(a, b, c);
      info.innerHTML = "💡 " + T(L3("Mou els lliscadors: <b>a</b> canvia l'obertura i el sentit, <b>c</b> puja o baixa la paràbola (és el tall amb l'eix Y) i <b>b</b> la desplaça en diagonal.", "Mueve los deslizadores: <b>a</b> cambia la abertura y el sentido, <b>c</b> sube o baja la parábola (es el corte con el eje Y) y <b>b</b> la desplaza en diagonal.", "Move the sliders: <b>a</b> changes the width and direction, <b>c</b> moves the parabola up or down (it's the Y-intercept) and <b>b</b> shifts it diagonally."));
    }
    Object.keys(S).forEach(function (k) { S[k].addEventListener("input", paint); });
    onLang(paint);
  }
  /* giny: estudi d'una paràbola escrita per l'alumne */
  function wStudy() {
    var w = document.getElementById("w-pstudy"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), g = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = ""; out.innerHTML = ""; g.innerHTML = "";
      var C = coefs(readF(I.f.value));
      if (!C || near(C.a, 0)) { info.innerHTML = warn(T(L3("Escriu una funció quadràtica, per exemple x^2-4x+3 o -2x^2+8x.", "Escribe una función cuadrática, por ejemplo x^2-4x+3 o -2x^2+8x.", "Type a quadratic function, for example x^2-4x+3 or -2x^2+8x."))); return; }
      var s = paraStudy(C.a, C.b, C.c);
      out.innerHTML = rows2html([tex("y=" + quadT(C.a, C.b, C.c)) + " → " + tex("a=" + qf(C.a) + ",\\ b=" + qf(C.b) + ",\\ c=" + qf(C.c))].concat(s.rows));
      g.innerHTML = paraPlot(C.a, C.b, C.c, { pts: s.xs });
    }
    I.f.addEventListener("input", paint);
    quickBind(w, function (v) { I.f.value = v[0]; paint(); });
    onLang(paint);
  }
  /* giny: llançament vertical h(t) = v·t − 5t² */
  function wProj() {
    var w = document.getElementById("w-proj"); if (!w) return;
    var sv = w.querySelector('input[data-k="v"]'), sh = w.querySelector('input[data-k="h"]'), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      var v = +sv.value, h0 = +sh.value, a = -5, V = vtx(a, v, h0), R = rootsQ(a, v, h0), tf = R.r[R.r.length - 1];
      w.querySelector(".vv").innerHTML = tex("v_0=" + nf(v) + "\\ \\text{m/s}"); w.querySelector(".hv").innerHTML = tex("h_0=" + nf(h0) + "\\ \\text{m}");
      var top = Math.ceil(V[1] / 10) * 10 + 10, right = Math.ceil(tf) + 1;
      out.innerHTML = '<div class="gcol"><p class="big">' + tex("h(t)=" + polyT([[h0, ""], [v, "t"], [-5, "t^2"]])) + "</p><p>" + T(L3("Altura màxima", "Altura máxima", "Maximum height")) + ": " + tex(nf(Math.round(V[1] * 100) / 100) + "\\ \\text{m}") + " " + T(L3("als", "a los", "after")) + " " + tex(nf(Math.round(V[0] * 100) / 100) + "\\ \\text{s}") + "</p><p>" + T(L3("Arriba a terra", "Llega al suelo", "Hits the ground")) + ": " + tex("t\\approx " + nf(Math.round(tf * 100) / 100) + "\\ \\text{s}") + "</p></div>"
        + plot({ xr: [-0.5, right], yr: [-top / 12, top], W: 360, H: 260, xl: "t (s)", yl: "h (m)", xs: right > 10 ? 2 : 1, ys: top > 100 ? 20 : 10, gx: 1, gy: 10, fn: [{ e: quadE(a, v, h0), from: 0, to: tf }], vguides: [V[0]], dots: [{ x: V[0], y: V[1], cls: "mx", r: 6, lab: "V" }, { x: tf, y: 0, cls: "cut", r: 5 }] });
      info.innerHTML = "💡 " + fill(T(L3("El vèrtex {V} dona el temps i l'altura màxima. El domini amb sentit és {D}: abans de llançar-la i després de tocar a terra la fórmula no té sentit.", "El vértice {V} da el tiempo y la altura máxima. El dominio con sentido es {D}: antes de lanzarla y después de tocar el suelo la fórmula no tiene sentido.", "The vertex {V} gives the time and the maximum height. The meaningful domain is {D}: before the throw and after it lands the formula makes no sense.")), { V: tex("t_v=\\frac{-b}{2a}=\\frac{" + nf(-v) + "}{-10}=" + nf(Math.round(V[0] * 100) / 100)), D: tex("[0,\\," + nf(Math.round(tf * 100) / 100) + "]") });
    }
    [sv, sh].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  function optsTex(right, wrongs) {
    var all = [right], seen = {}; seen[right] = 1;
    wrongs.forEach(function (w) { if (w && !seen[w] && all.length < 4) { seen[w] = 1; all.push(w); } });
    var order = shuffle(all.map(function (_, i) { return i; }));
    return { opts: order.map(function (i) { return { va: "$" + all[i] + "$" }; }), ans: order.indexOf(0) };
  }
  function optsTxt(right, wrongs) {
    var all = [right].concat(wrongs), order = shuffle(all.map(function (_, i) { return i; }));
    return { opts: order.map(function (i) { return all[i]; }), ans: order.indexOf(0) };
  }
  var GEN = {
    propk: function () {
      var k = pick([2, 3, 4, -2, -3, 0.5, 1.5, -0.5, 2.5]), a = pick([2, 4, -2, 6, -4]), b = k * a;
      return { num: k, q: function () { return fill(T(L3("Una funció de proporcionalitat directa passa pel punt {P}. Quina és la constant de proporcionalitat (el pendent)?", "Una función de proporcionalidad directa pasa por el punto {P}. ¿Cuál es la constante de proporcionalidad (la pendiente)?", "A direct proportion goes through the point {P}. What is the constant of proportionality (the slope)?")), { P: "$(" + nf(a) + ",\\," + nf(b) + ")$" }); },
        s: function () { return tex("m=\\dfrac{y}{x}=\\dfrac{" + nf(b) + "}{" + nf(a) + "}=\\boxed{" + nf(k) + "}") + " → " + tex("y=" + lineT(k, 0)); } };
    },
    mn: function () {
      var m = pick([1, 2, 3, -1, -2, -3, 0.5, -0.5]), n = rint(-4, 4);
      if (near(m, 0.5) || near(m, -0.5)) n = 2 * Math.round(n / 2);
      var o = optsTex("y=" + lineT(m, n), ["y=" + lineT(-m, n), "y=" + lineT(m, -n), "y=" + lineT(n || 1, m), "y=" + lineT(1 / m, n)]);
      return { opts: o.opts, ans: o.ans,
        q: function () { return T(L3("Quina és l'equació d'aquesta recta?", "¿Cuál es la ecuación de esta recta?", "What is the equation of this line?")) + plot({ xr: [-6, 6], yr: [-6, 6], fn: [{ e: linE(m, n) }], small: true }); },
        s: function () { return fill(T(L3("Talla l'eix {Y} en {P}: {n}. Si avancem {r} cap a la dreta, puja (o baixa) {u}: {m}.", "Corta el eje {Y} en {P}: {n}. Si avanzamos {r} hacia la derecha, sube (o baja) {u}: {m}.", "It crosses the {Y} axis at {P}: {n}. Moving {r} to the right, it goes up (or down) {u}: {m}.")), { Y: tex("Y"), P: tex("(0,\\," + nf(n) + ")"), n: tex("n=" + nf(n)), r: tex(Number.isInteger(m) ? "1" : "2"), u: tex(Number.isInteger(m) ? nf(m) : nf(2 * m)), m: tex("m=" + nf(m)) })
          + plot({ xr: [-6, 6], yr: [-6, 6], fn: [{ e: linE(m, n) }], curves: slopeTri(0, n, m, Number.isInteger(m) ? 1 : 2), dots: [{ x: 0, y: n, cls: "cut", r: 6 }], small: true }); } };
    },
    slope: function () {
      var P, Q;
      do { P = [rint(-5, 5), rint(-6, 6)]; Q = [rint(-5, 5), rint(-6, 6)]; } while (P[0] === Q[0] || ![1, 2, 4].some(function (d) { return Number.isInteger((Q[1] - P[1]) * d / (Q[0] - P[0])); }));
      var m = (Q[1] - P[1]) / (Q[0] - P[0]);
      return { num: m, q: function () { return fill(T(L3("Calcula el pendent de la recta que passa per {P} i {Q}.", "Calcula la pendiente de la recta que pasa por {P} y {Q}.", "Work out the slope of the line through {P} and {Q}.")), { P: "$(" + nf(P[0]) + ",\\," + nf(P[1]) + ")$", Q: "$(" + nf(Q[0]) + ",\\," + nf(Q[1]) + ")$" }); },
        s: function () { return lineSteps(P, Q).rows[0]; } };
    },
    eq2: function () {
      var m = pick([1, 2, 3, -1, -2, -3, 0.5, -0.5, 4]), n = rint(-5, 5), a = rint(-3, 0), b = a + pick([2, 4]);
      var P = [a, m * a + n], Q = [b, m * b + n], r = lineSteps(P, Q);
      var o = optsTex("y=" + lineT(m, n), ["y=" + lineT(-m, n), "y=" + lineT(m, -n), "y=" + lineT(1 / m, n - 1), "y=" + lineT(m, P[1])]);
      return { opts: o.opts, ans: o.ans,
        q: function () { return fill(T(L3("Quina és l'equació de la recta que passa per {P} i {Q}?", "¿Cuál es la ecuación de la recta que pasa por {P} y {Q}?", "What is the equation of the line through {P} and {Q}?")), { P: "$(" + nf(P[0]) + ",\\," + nf(P[1]) + ")$", Q: "$(" + nf(Q[0]) + ",\\," + nf(Q[1]) + ")$" }); },
        s: function () { return r.rows.join("<br>"); } };
    },
    apl: function () {
      var t = rint(0, 3), b, m, k, ask = rint(0, 1), ctx, unit;
      if (t === 0) { b = pick([2, 2.5, 3, 3.5]); m = pick([0.5, 1, 1.5, 2]); ctx = L3("Un taxi cobra {b} € per pujar-hi i {m} € per cada km.", "Un taxi cobra {b} € por subir y {m} € por cada km.", "A taxi charges €{b} to get in and €{m} per km."); unit = L3("km", "km", "km"); }
      else if (t === 1) { b = pick([5, 8, 10, 12]); m = pick([0.1, 0.2, 0.5]); ctx = L3("Una tarifa de mòbil costa {b} € al mes més {m} € per cada minut de trucada.", "Una tarifa de móvil cuesta {b} € al mes más {m} € por cada minuto de llamada.", "A phone plan costs €{b} a month plus €{m} per call minute."); unit = L3("minuts", "minutos", "minutes"); }
      else if (t === 2) { b = pick([20, 30, 40]); m = pick([2, 3, 4, 5]); ctx = L3("Un gimnàs cobra {b} € de matrícula i {m} € per cada sessió.", "Un gimnasio cobra {b} € de matrícula y {m} € por cada sesión.", "A gym charges a €{b} joining fee and €{m} per session."); unit = L3("sessions", "sesiones", "sessions"); }
      else { b = pick([15, 20, 25, 30]); m = pick([2, 3, 4]); ctx = L3("Una vela fa {b} cm i, encesa, s'escurça {m} cm cada hora.", "Una vela mide {b} cm y, encendida, se acorta {m} cm cada hora.", "A candle is {b} cm tall and, when lit, gets {m} cm shorter every hour."); unit = L3("hores", "horas", "hours"); m = -m; }
      k = t === 1 ? pick([20, 30, 40, 50, 60]) : t === 3 ? rint(1, Math.floor(b / -m) - 1) : rint(3, 15);
      var val = Math.round((b + m * k) * 100) / 100;
      return { num: ask ? k : val,
        q: function () { var c = fill(T(ctx), { b: nf(b).replace("\\dc ", ","), m: nf(Math.abs(m)).replace("\\dc ", ",") }); return c + " " + (t === 3 ? (ask ? fill(T(L3("Quantes hores fa que està encesa si ara fa {c} cm?", "¿Cuántas horas lleva encendida si ahora mide {c} cm?", "How many hours has it been lit if it is now {c} cm tall?")), { c: nf(val).replace("\\dc ", ",") }) : fill(T(L3("Quant farà al cap de {k} hores? (en cm)", "¿Cuánto medirá al cabo de {k} horas? (en cm)", "How tall will it be after {k} hours? (in cm)")), { k: k }))
          : (ask ? fill(T(L3("Si has pagat {c} €, quants {u} has fet servir?", "Si has pagado {c} €, ¿cuántos {u} has usado?", "If you paid €{c}, how many {u} did you use?")), { c: nf(val).replace("\\dc ", ","), u: T(unit) }) : fill(T(L3("Quant costen {k} {u}? (en €)", "¿Cuánto cuestan {k} {u}? (en €)", "How much do {k} {u} cost? (in €)")), { k: k, u: T(unit) }))); },
        s: function () { var fx = "y=" + lineT(m, b); return tex(fx) + " → " + (ask ? tex(lineT(m, b) + "=" + nf(val) + "\\Rightarrow " + qf(m) + "x=" + nf(val - b) + "\\Rightarrow \\boxed{x=" + k + "}") : tex("y=" + nf(b) + (m < 0 ? "-" : "+") + nf(Math.abs(m)) + "\\cdot" + k + "=\\boxed{" + nf(val) + "}")); } };
    },
    pos: function () {
      var m1 = rnz(-3, 3), n1 = rint(-5, 5), t = rint(0, 2), m2, n2, k = rint(2, 3);
      if (t === 0) { m2 = m1; do { n2 = rint(-5, 5); } while (n2 === n1); }
      else if (t === 1) { m2 = m1; n2 = n1; }
      else { do { m2 = rnz(-3, 3); } while (m2 === m1); n2 = rint(-5, 5); }
      var form2 = t === 1 && rint(0, 1) ? k + "y=" + polyT([[k * m2, "x"], [k * n2, ""]]) : "y=" + lineT(m2, n2);
      var names = [L3("Paral·leles", "Paralelas", "Parallel"), L3("Coincidents", "Coincidentes", "Coincident"), L3("Secants", "Secantes", "Intersecting")];
      var o = optsTxt(names[t], names.filter(function (_, i) { return i !== t; }));
      return { opts: o.opts, ans: o.ans,
        q: function () { return fill(T(L3("Quina és la posició relativa de les rectes {r} i {s}?", "¿Cuál es la posición relativa de las rectas {r} y {s}?", "How are the lines {r} and {s} related?")), { r: "$y=" + lineT(m1, n1) + "$", s: "$" + form2 + "$" }); },
        s: function () { return (form2.charAt(0) !== "y" ? T(L3("Dividim la segona entre ", "Dividimos la segunda entre ", "Divide the second one by ")) + tex(String(k)) + ": " + tex("y=" + lineT(m2, n2)) + ". " : "") + [T(L3("Mateix pendent i ordenades en l'origen diferents: paral·leles.", "Misma pendiente y ordenadas en el origen distintas: paralelas.", "Same slope and different intercepts: parallel.")), T(L3("Mateix pendent i mateixa ordenada en l'origen: és la mateixa recta (coincidents).", "Misma pendiente y misma ordenada en el origen: es la misma recta (coincidentes).", "Same slope and same intercept: it's the same line (coincident).")), T(L3("Pendents diferents: secants (es tallen en un punt).", "Pendientes distintas: secantes (se cortan en un punto).", "Different slopes: intersecting (they meet at one point)."))][t]; } };
    },
    cut: function () {
      var X = rint(-4, 4), Y = rint(-5, 5), m1 = rnz(-3, 3), m2; do { m2 = rnz(-3, 3); } while (m2 === m1);
      var n1 = Y - m1 * X, n2 = Y - m2 * X;
      return { pair: [[X, Y]], q: function () { return fill(T(L3("En quin punt es tallen les rectes {r} i {s}?", "¿En qué punto se cortan las rectas {r} y {s}?", "Where do the lines {r} and {s} meet?")), { r: "$y=" + lineT(m1, n1) + "$", s: "$y=" + lineT(m2, n2) + "$" }); },
        s: function () { return cutSteps(m1, n1, m2, n2).rows.join("<br>"); } };
    },
    vert: function () {
      var a = pick([1, 1, -1, 2, -2, 3, 0.5]), xv = rint(-3, 3), yv = rint(-6, 6);
      if (near(a, 0.5)) xv = 2 * Math.round(xv / 2);
      var b = -2 * a * xv, c = a * xv * xv + yv;
      return { pair: [[xv, yv]], q: function () { return fill(T(L3("Calcula el vèrtex de la paràbola {f}.", "Calcula el vértice de la parábola {f}.", "Find the vertex of the parabola {f}.")), { f: "$y=" + quadT(a, b, c) + "$" }); },
        s: function () { return paraStudy(a, b, c).rows[1].replace("<b>2.</b> ", ""); } };
    },
    pgraph: function () {
      var a = pick([1, -1]), xv = rint(-3, 3), yv = rint(-4, 4), b = -2 * a * xv, c = a * xv * xv + yv;
      var o = optsTex("y=" + quadT(a, b, c), ["y=" + quadT(-a, -b, -c), "y=" + quadT(a, -b, c), "y=" + quadT(a, b, c + (c > 0 ? -2 : 2)), "y=" + quadT(-a, b, c)]);
      return { opts: o.opts, ans: o.ans,
        q: function () { return T(L3("Quina fórmula correspon a aquesta paràbola?", "¿Qué fórmula corresponde a esta parábola?", "Which formula matches this parabola?")) + plot({ xr: [-7, 7], yr: [-7, 7], fn: [{ e: quadE(a, b, c) }], small: true }); },
        s: function () { return fill(T(L3("Branques cap {d} ({a}), vèrtex {V} i talla l'eix {Y} en {C}: ", "Ramas hacia {d} ({a}), vértice {V} y corta el eje {Y} en {C}: ", "Arms pointing {d} ({a}), vertex {V} and {Y}-intercept {C}: ")), { d: T(a > 0 ? L3("dalt", "arriba", "up") : L3("baix", "abajo", "down")), a: tex("a" + (a > 0 ? ">0" : "<0")), V: tex("(" + nf(xv) + ",\\," + nf(yv) + ")"), Y: tex("Y"), C: tex("(0,\\," + nf(c) + ")") }) + tex("y=" + quadT(a, b, c)); } };
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
  window.FM8 = { parseExpr: parseExpr, ev: ev, coefs: coefs, qf: qf, lineT: lineT, quadT: quadT, lineSteps: lineSteps, cutSteps: cutSteps, paraStudy: paraStudy, rootsQ: rootsQ, vtx: vtx, GEN: GEN, numIn: numIn, pairIn: pairIn };

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

  var TITLES = { va: "Funció lineal i quadràtica · FentMates", es: "Función lineal y cuadrática · FentMates", en: "Linear and quadratic functions · FentMates" };
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
    document.querySelectorAll(".w-line").forEach(wLine); wTwo(); wApl(); wPair(); wA(); wPara(); wStudy(); wProj();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
