(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-4eso-a-u7-done";

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
  function byId(id) { return document.getElementById(id); }
  function presetBtns(box, labels, onPick, first) {
    var bs = [];
    labels().forEach(function (_, i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { bs.forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on"); onPick(i); });
      box.appendChild(b); bs.push(b);
    });
    if (first != null && bs[first]) bs[first].classList.add("on");
    onLang(function () { var L = labels(); bs.forEach(function (b, i) { b.innerHTML = L[i]; }); });
    return bs;
  }
  function kv(rows) { return '<div class="kv">' + rows.map(function (r) { return "<span>" + r[0] + "</span><span>" + r[1] + "</span>"; }).join("") + "</div>"; }
  function rt(s) { return s.replace(/\$([^$]+)\$/g, function (_, m) { return tex(m); }); }
  function small(s) { return "<br><small>" + s + "</small>"; }
  var COL = { cos: "#3b82f6", sin: "#f97316", tan: "#16a34a", ang: "#7c3aed", r: "#e11d48" };
  function cdot(c) { return '<i class="tag-c" style="background:' + c + '"></i>'; }

  /* ---------- nombres ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function lcm(a, b) { return a / gcd(a, b) * b; }
  function decS(x, k) { var s = String(+x.toFixed(k == null ? 2 : k)); if (s === "-0") s = "0"; return lang === "en" ? s : s.replace(".", ","); }
  function dT(x, k) { return decS(x, k).replace(",", "{,}"); }
  function apx(x, k) { var e = Math.abs(x - +x.toFixed(k == null ? 4 : k)) > 1e-10; return (e ? "\\approx " : "=") + dT(x, k == null ? 4 : k); }
  function Fr(n, d) { if (d === undefined) d = 1; if (d < 0) { n = -n; d = -d; } var g = gcd(n, d) || 1; return { n: n / g, d: d / g }; }
  function F(x) { return typeof x === "number" ? Fr(x) : x; }
  function fAdd(a, b) { a = F(a); b = F(b); return Fr(a.n * b.d + b.n * a.d, a.d * b.d); }
  function fSub(a, b) { a = F(a); b = F(b); return Fr(a.n * b.d - b.n * a.d, a.d * b.d); }
  function fMul(a, b) { a = F(a); b = F(b); return Fr(a.n * b.n, a.d * b.d); }
  function fDiv(a, b) { a = F(a); b = F(b); return Fr(a.n * b.d, a.d * b.n); }
  function fVal(a) { a = F(a); return a.n / a.d; }
  function fT(f) { f = F(f); return f.d === 1 ? String(f.n) : (f.n < 0 ? "-" : "") + "\\frac{" + Math.abs(f.n) + "}{" + f.d + "}"; }

  function svgPt(svg, e) {
    var m = svg.getScreenCTM(); if (!m) return null;
    var pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
    return pt.matrixTransform(m.inverse());
  }
  function f1(x) { return Math.round(x * 10) / 10; }
  /* ---------- gràfiques cartesianes ---------- */
  function gview(o) {
    var W = o.W || 360, H = o.H || 260, pl = o.pl || 30, pr = 10, pt = 10, pb = 22;
    function X(x) { return pl + (x - o.x0) / (o.x1 - o.x0) * (W - pl - pr); }
    function Y(y) { return H - pb - (y - o.y0) / (o.y1 - o.y0) * (H - pt - pb); }
    var g = "", v;
    (o.xt || []).forEach(function (t) { g += '<line class="g" x1="' + f1(X(t[0])) + '" x2="' + f1(X(t[0])) + '" y1="' + Y(o.y0) + '" y2="' + Y(o.y1) + '"/>'; });
    for (v = Math.ceil(o.y0 / o.sy) * o.sy; v <= o.y1 + 1e-9; v += o.sy) g += '<line class="g" x1="' + X(o.x0) + '" x2="' + X(o.x1) + '" y1="' + f1(Y(v)) + '" y2="' + f1(Y(v)) + '"/>';
    var ay = Math.max(o.y0, Math.min(o.y1, 0)), ax = Math.max(o.x0, Math.min(o.x1, 0));
    g += '<line class="ax" x1="' + X(o.x0) + '" x2="' + X(o.x1) + '" y1="' + f1(Y(ay)) + '" y2="' + f1(Y(ay)) + '"/><line class="ax" x1="' + f1(X(ax)) + '" x2="' + f1(X(ax)) + '" y1="' + Y(o.y0) + '" y2="' + Y(o.y1) + '"/>';
    (o.xt || []).forEach(function (t) { if (t[1]) g += '<text x="' + f1(X(t[0])) + '" y="' + f1(Math.min(H - 4, Y(ay) + 13)) + '" text-anchor="middle">' + t[1] + "</text>"; });
    for (v = Math.ceil(o.y0 / o.sy) * o.sy; v <= o.y1 + 1e-9; v += o.sy) if (Math.abs(v) > 1e-9) g += '<text x="' + f1(X(ax) - 4) + '" y="' + f1(Y(v) + 3.5) + '" text-anchor="end">' + String(+v.toFixed(3)).replace("-", "−").replace(".", lang === "en" ? "." : ",") + "</text>";
    var id = "cl" + Math.random().toString(36).slice(2, 8);
    var clip = '<defs><clipPath id="' + id + '"><rect x="' + X(o.x0) + '" y="' + Y(o.y1) + '" width="' + (X(o.x1) - X(o.x0)) + '" height="' + (Y(o.y0) - Y(o.y1)) + '"/></clipPath></defs>';
    return { g: g + clip, X: X, Y: Y, o: o, open: '<g clip-path="url(#' + id + ')">', close: "</g>" };
  }
  // corba de f; es talla on la funció salta (asímptotes)
  function curve(G, f, color, opts) {
    opts = opts || {};
    var o = G.o, a = opts.a == null ? o.x0 : opts.a, b = opts.b == null ? o.x1 : opts.b, N = opts.n || 600, d = "", pen = false, M = (o.y1 - o.y0), py = null;
    for (var i = 0; i <= N; i++) {
      var x = a + (b - a) * i / N, y = f(x);
      if (!isFinite(y) || Math.abs(y) > 1e6) { pen = false; py = null; continue; }
      if (py != null && Math.abs(y - py) > M * 1.5) pen = false;
      py = y; y = Math.max(o.y0 - M, Math.min(o.y1 + M, y));
      d += (pen ? "L" : "M") + G.X(x).toFixed(1) + " " + G.Y(y).toFixed(1); pen = true;
    }
    return '<path class="cv" d="' + d + '" style="stroke:' + color + (opts.w ? ";stroke-width:" + opts.w : "") + '"' + (opts.dash ? ' stroke-dasharray="' + opts.dash + '"' : "") + "/>";
  }
  function gdot(G, x, y, col, r) { return '<circle class="pt" cx="' + f1(G.X(x)) + '" cy="' + f1(G.Y(y)) + '" r="' + (r || 5) + '" style="fill:' + col + '"/>'; }
  /* ---------- més ajudes de gràfiques ---------- */
  function odot(G, x, y, col) { return '<circle cx="' + f1(G.X(x)) + '" cy="' + f1(G.Y(y)) + '" r="5" style="fill:var(--bg);stroke:' + col + ';stroke-width:2.2"/>'; }
  function vdash(G, x) { return '<line class="gd" x1="' + f1(G.X(x)) + '" x2="' + f1(G.X(x)) + '" y1="' + G.Y(G.o.y0) + '" y2="' + G.Y(G.o.y1) + '"/>'; }
  function hdash(G, y) { return '<line class="gd" x1="' + G.X(G.o.x0) + '" x2="' + G.X(G.o.x1) + '" y1="' + f1(G.Y(y)) + '" y2="' + f1(G.Y(y)) + '"/>'; }
  function seg(G, a, b, c, d, col, w) { return '<line x1="' + f1(G.X(a)) + '" y1="' + f1(G.Y(b)) + '" x2="' + f1(G.X(c)) + '" y2="' + f1(G.Y(d)) + '" style="stroke:' + col + ";stroke-width:" + (w || 2.6) + ';stroke-linecap:round"/>'; }
  function gtext(G, x, y, s, col, dx, dy) { return '<text class="lb" x="' + f1(G.X(x) + (dx || 0)) + '" y="' + f1(G.Y(y) + (dy || 0)) + '" text-anchor="middle"' + (col ? ' style="fill:' + col + '"' : "") + ">" + s + "</text>"; }
  function ticks(a, b, s) { var o = [], v; for (v = Math.ceil(a / s) * s; v <= b + 1e-9; v += s) o.push([v, Math.abs(v) < 1e-9 ? "" : String(+v.toFixed(3)).replace("-", "−")]); return o; }
  function plane(x0, x1, y0, y1, s, W, H) { return gview({ x0: x0, x1: x1, y0: y0, y1: y1, sy: s || 1, W: W || 360, H: H || 260, xt: ticks(x0, x1, s || 1) }); }
  var AC = "var(--accent)", BL = "#3b82f6", GR = "#16a34a", VI = "#7c3aed", OR = "#f97316", MU = "var(--muted)";
  // arrossegament de punts d'una gràfica: getG() retorna la vista actual i pts() la llista de punts [{x,y}]
  function dragger(svg, getG, pts, onMove) {
    var act = -1;
    function data(e) {
      var q = svgPt(svg, e); if (!q) return null;
      var G = getG(), o = G.o, W = o.W || 360, H = o.H || 260, pl = o.pl || 30;
      return { x: o.x0 + (q.x - pl) / (W - pl - 10) * (o.x1 - o.x0), y: o.y0 + (H - 22 - q.y) / (H - 32) * (o.y1 - o.y0), px: q.x, py: q.y };
    }
    svg.addEventListener("pointerdown", function (e) {
      var d = data(e); if (!d) return;
      var G = getG(), best = -1, bd = 26;
      pts().forEach(function (p, i) { var k = Math.hypot(G.X(p.x) - d.px, G.Y(p.y) - d.py); if (k < bd) { bd = k; best = i; } });
      if (best < 0) return;
      act = best; svg.classList.add("dragging"); try { svg.setPointerCapture(e.pointerId); } catch (_) {} e.preventDefault();
    });
    svg.addEventListener("pointermove", function (e) { if (act >= 0) { var d = data(e); if (d) onMove(act, d); } });
    function up() { act = -1; svg.classList.remove("dragging"); }
    svg.addEventListener("pointerup", up); svg.addEventListener("pointercancel", up);
  }

  /* ---------- expressions: analitzador, avaluació, LaTeX ---------- */
  function parseF(src) {
    var s = String(src).toLowerCase().replace(/\s+/g, "").replace(/[·×]/g, "*").replace(/[−–]/g, "-").replace(/√/g, "sqrt").replace(/π/g, "pi").replace(/,/g, ".").replace(/²/g, "^2").replace(/³/g, "^3").replace(/tg/g, "tan").replace(/sen/g, "sin");
    if (!s) return null;
    var i = 0, m;
    function peek() { return s[i]; }
    function fail() { throw new Error("sintaxi"); }
    function expr() { var a = term(); while (peek() === "+" || peek() === "-") { var o = s[i++]; a = { t: o, a: a, b: term() }; } return a; }
    function starts() { var c = peek(); return c !== undefined && /[0-9.a-z(]/.test(c); }
    function term() { var a = unary(); for (;;) { var c = peek(); if (c === "*" || c === "/") { i++; a = { t: c, a: a, b: unary() }; } else if (starts()) a = { t: "*", a: a, b: power() }; else return a; } }
    function unary() { if (peek() === "-") { i++; return { t: "neg", a: unary() }; } if (peek() === "+") { i++; return unary(); } return power(); }
    function power() { var a = atom(); if (peek() === "^") { i++; return { t: "^", a: a, b: unary() }; } return a; }
    function call(n, extra) { var a; if (peek() === "(") { i++; a = expr(); if (s[i++] !== ")") fail(); } else a = power(); var o = { t: "f", n: n, a: a }; if (extra) o.base = extra; return o; }
    function atom() {
      var c = peek(), r = s.slice(i);
      if (c === "(") { i++; var a = expr(); if (s[i++] !== ")") fail(); return a; }
      if (c === "|") { i++; var b = expr(); if (s[i++] !== "|") fail(); return { t: "f", n: "abs", a: b }; }
      if ((m = r.match(/^(\d+\.?\d*|\.\d+)/))) { i += m[0].length; return { t: "n", v: +m[0] }; }
      if ((m = r.match(/^(sqrt|cbrt|abs|exp|sin|cos|tan|ln)/))) { i += m[0].length; return call(m[0]); }
      if ((m = r.match(/^log_?(\d+\.?\d*)?/))) { i += m[0].length; return call("log", m[1] ? +m[1] : 10); }
      if (r.indexOf("pi") === 0) { i += 2; return { t: "c", s: "\\pi", v: Math.PI }; }
      if (c === "x") { i++; return { t: "x" }; }
      if (c === "e") { i++; return { t: "c", s: "e", v: Math.E }; }
      fail();
    }
    try { var ast = expr(); return i === s.length ? ast : null; } catch (e) { return null; }
  }
  function powE(b, e) { if (b === 0 && e < 0) return NaN; if (b < 0 && Math.abs(e - Math.round(e)) > 1e-12) return NaN; return Math.pow(b, e); }
  function ev(n, x) {
    switch (n.t) {
      case "n": case "c": return n.v;
      case "x": return x;
      case "+": return ev(n.a, x) + ev(n.b, x);
      case "-": return ev(n.a, x) - ev(n.b, x);
      case "*": return ev(n.a, x) * ev(n.b, x);
      case "/": var d = ev(n.b, x); return Math.abs(d) < 1e-11 ? NaN : ev(n.a, x) / d;
      case "^": return powE(ev(n.a, x), ev(n.b, x));
      case "neg": return -ev(n.a, x);
    }
    var v = ev(n.a, x);
    switch (n.n) {
      case "sqrt": return v < -1e-10 ? NaN : Math.sqrt(Math.max(v, 0));
      case "cbrt": return Math.cbrt(v);
      case "abs": return Math.abs(v);
      case "exp": return Math.exp(v);
      case "ln": return v <= 1e-12 ? NaN : Math.log(v);
      case "log": return v <= 1e-12 ? NaN : Math.log(v) / Math.log(n.base);
      case "sin": return Math.sin(v);
      case "cos": return Math.cos(v);
      case "tan": return Math.abs(Math.cos(v)) < 1e-9 ? NaN : Math.tan(v);
    }
    return NaN;
  }
  function hasX(n) { return n.t === "x" || (n.a && hasX(n.a)) || (n.b && hasX(n.b)) || false; }
  function hasTrig(n) { return (n.t === "f" && /sin|cos|tan/.test(n.n) && hasX(n.a)) || (n.a && hasTrig(n.a)) || (n.b && hasTrig(n.b)) || false; }
  function sub(n, r) { if (n.t === "x") return r; var o = {}; for (var k in n) o[k] = n[k]; if (n.a) o.a = sub(n.a, r); if (n.b) o.b = sub(n.b, r); return o; }
  function prec(n) { return n.t === "+" || n.t === "-" ? 1 : n.t === "*" || n.t === "/" || n.t === "neg" ? 2 : n.t === "^" ? 3 : 4; }
  function numT(v) { return Number.isInteger(v) ? String(v) : String(+v.toFixed(4)).replace(".", lang === "en" ? "." : "{,}"); }
  function toT(n) {
    function P(c, p) { var s = toT(c); return prec(c) < p ? "\\left(" + s + "\\right)" : s; }
    switch (n.t) {
      case "n": return numT(n.v);
      case "c": return n.s;
      case "x": return "x";
      case "+": return n.b.t === "neg" ? toT(n.a) + "-" + P(n.b.a, 2) : toT(n.a) + "+" + toT(n.b);
      case "-": return toT(n.a) + "-" + P(n.b, 2);
      case "neg": return "-" + P(n.a, 2);
      case "/": return "\\dfrac{" + toT(n.a) + "}{" + toT(n.b) + "}";
      case "*": var lhs = P(n.a, 2), rhs = P(n.b, 2), imp = n.a.t === "n" && n.b.t !== "n" && !/^\d/.test(rhs); return lhs + (imp ? "" : "\\cdot ") + rhs;
      case "^": var bs = (n.a.t === "f" && n.a.n !== "abs" && n.a.n !== "sqrt") || prec(n.a) <= 3 ? "\\left(" + toT(n.a) + "\\right)" : toT(n.a); return bs + "^{" + toT(n.b) + "}";
    }
    var a = toT(n.a), br = "\\left(" + a + "\\right)";
    switch (n.n) {
      case "sqrt": return "\\sqrt{" + a + "}";
      case "cbrt": return "\\sqrt[3]{" + a + "}";
      case "abs": return "\\left|" + a + "\\right|";
      case "exp": return "e^{" + a + "}";
      case "ln": return "\\ln" + br;
      case "log": return "\\log" + (n.base === 10 ? "" : "_{" + numT(n.base) + "}") + br;
      default: return "\\" + n.n + br;
    }
  }
  // polinomis amb coeficients exactes (per a simplificar les composicions)
  function polyOf(n) {
    function add(a, b, s) { var o = [], i; for (i = 0; i < Math.max(a.length, b.length); i++) o.push(fAdd(a[i] || Fr(0), fMul(b[i] || Fr(0), s))); return o; }
    function mul(a, b) { var o = [], i, j; for (i = 0; i < a.length + b.length - 1; i++) o.push(Fr(0)); for (i = 0; i < a.length; i++) for (j = 0; j < b.length; j++) o[i + j] = fAdd(o[i + j], fMul(a[i], b[j])); return o; }
    var a, b;
    switch (n.t) {
      case "n": if (Number.isInteger(n.v)) return [Fr(n.v)]; var d = 1; while (d < 10000 && !Number.isInteger(+(n.v * d).toFixed(9))) d *= 10; return [Fr(Math.round(n.v * d), d)];
      case "x": return [Fr(0), Fr(1)];
      case "neg": a = polyOf(n.a); return a && a.map(function (c) { return fMul(c, -1); });
      case "+": case "-": a = polyOf(n.a); b = polyOf(n.b); return a && b && add(a, b, n.t === "+" ? 1 : -1);
      case "*": a = polyOf(n.a); b = polyOf(n.b); return a && b && mul(a, b);
      case "/": a = polyOf(n.a); b = polyOf(n.b); if (!a || !b || b.length > 1 || !b[0].n) return null; return a.map(function (c) { return fDiv(c, b[0]); });
      case "^": if (hasX(n.b)) return null; var e = ev(n.b, 0); if (!Number.isInteger(e) || e < 0 || e > 8) return null; a = polyOf(n.a); if (!a) return null; var r = [Fr(1)]; while (e--) r = mul(r, a); return r;
    }
    return null;
  }
  function polyT(c) {
    var s = "", i;
    for (i = c.length - 1; i >= 0; i--) {
      var v = F(c[i]); if (!v.n) continue;
      var ab = fT(Fr(Math.abs(v.n), v.d)), mono = i === 0 ? ab : (ab === "1" ? "" : ab) + "x" + (i > 1 ? "^{" + i + "}" : "");
      s += (v.n < 0 ? "-" : s ? "+" : "") + mono;
    }
    return s || "0";
  }
  function snap(r) { for (var d = 1; d <= 24; d++) { var n = Math.round(r * d); if (Math.abs(r - n / d) < 1e-7) return n / d; } return r; }
  function rootsF(f, A, B) {
    var N = Math.round((B - A) * 60), h = (B - A) / N, out = [], i, xs = [], vs = [];
    function add(r) { r = snap(r); if (!out.some(function (o) { return Math.abs(o - r) < 1e-5; })) out.push(r); }
    for (i = 0; i <= N; i++) { xs.push(A + i * h); vs.push(f(xs[i])); }
    for (i = 0; i <= N; i++) {
      if (isFinite(vs[i]) && Math.abs(vs[i]) < 1e-12) add(xs[i]);
      if (i && isFinite(vs[i]) && isFinite(vs[i - 1]) && vs[i] * vs[i - 1] < 0) {
        var lo = xs[i - 1], hi = xs[i], fl = vs[i - 1];
        for (var k = 0; k < 70; k++) { var m = (lo + hi) / 2, fm = f(m); if (!isFinite(fm)) break; if (fl * fm <= 0) hi = m; else { lo = m; fl = fm; } }
        var rr = (lo + hi) / 2; if (Math.abs(f(rr)) < 1e-6) add(rr);
      }
      if (i > 0 && i < N && isFinite(vs[i]) && isFinite(vs[i - 1]) && isFinite(vs[i + 1]) && Math.abs(vs[i]) <= Math.abs(vs[i - 1]) && Math.abs(vs[i]) <= Math.abs(vs[i + 1]) && Math.abs(vs[i]) < .05) {
        var a = xs[i - 1], b = xs[i + 1];
        for (var j = 0; j < 90; j++) { var m1 = a + (b - a) / 3, m2 = b - (b - a) / 3; if (Math.abs(f(m1)) < Math.abs(f(m2))) b = m2; else a = m1; }
        var mm = (a + b) / 2; if (Math.abs(f(mm)) < 1e-9) add(mm);
      }
    }
    return out.sort(function (p, q) { return p - q; });
  }
  function consOf(n, o) {
    if (n.a) consOf(n.a, o); if (n.b) consOf(n.b, o);
    if (n.t === "/" && hasX(n.b)) o.push({ k: "ne", g: n.b });
    if (n.t === "^" && hasX(n.a)) {
      if (hasX(n.b)) o.push({ k: "gt", g: n.a });
      else { var e = ev(n.b, 0); if (Number.isInteger(e)) { if (e < 0) o.push({ k: "ne", g: n.a }); } else o.push({ k: e < 0 ? "gt" : "ge", g: n.a }); }
    }
    if (n.t === "f" && hasX(n.a)) {
      if (n.n === "sqrt") o.push({ k: "ge", g: n.a });
      if (n.n === "ln" || n.n === "log") o.push({ k: "gt", g: n.a });
      if (n.n === "tan") o.push({ k: "ne", g: { t: "f", n: "cos", a: n.a } });
    }
    return o;
  }
  function solveSet(C) {
    if (C.some(function (c) { return hasTrig(c.g); })) return null;
    var pts = [];
    C.forEach(function (c) { rootsF(function (x) { return ev(c.g, x); }, -60, 60).forEach(function (r) { if (!pts.some(function (p) { return Math.abs(p - r) < 1e-5; })) pts.push(r); }); });
    pts.sort(function (a, b) { return a - b; });
    function ok(x) { return C.every(function (c) { var v = ev(c.g, x); if (!isFinite(v)) return false; var z = Math.abs(v) < 1e-8; return c.k === "ne" ? !z : c.k === "ge" ? (z || v > 0) : (!z && v > 0); }); }
    var xs = [-Infinity].concat(pts, [Infinity]), res = [], j;
    for (j = 0; j < xs.length - 1; j++) {
      var a = xs[j], b = xs[j + 1], m = !isFinite(a) && !isFinite(b) ? 0 : !isFinite(a) ? b - 1 : !isFinite(b) ? a + 1 : (a + b) / 2;
      if (!ok(m)) { if (isFinite(b) && ok(b) && !ok(isFinite(xs[j + 2]) ? (b + xs[j + 2]) / 2 : b + 1)) res.push({ a: b, b: b, ac: true, bc: true }); continue; }
      var ac = isFinite(a) && ok(a), bc = isFinite(b) && ok(b), last = res[res.length - 1];
      if (last && last.b === a && last.bc) { last.b = b; last.bc = bc; } else res.push({ a: a, b: b, ac: ac, bc: bc });
    }
    return { ivs: res, ok: ok, pts: pts };
  }
  function niceT(r) {
    if (Math.abs(r) < 1e-9) return "0";
    var d, n, p, k;
    for (d = 1; d <= 24; d++) { n = Math.round(r * d); if (Math.abs(r - n / d) < 1e-7) return fT(Fr(n, d)); }
    for (d = 1; d <= 12; d++) for (k = 0; k <= 60; k++) {
      p = k % 2 ? (k + 1) / 2 : -k / 2;
      var t = r * d - p, q = t * t, qn = Math.round(q);
      if (qn >= 2 && qn <= 500 && Math.abs(q - qn) < 1e-6 && surd(qn).b > 1) {
        var sd = surd(qn), rd = (sd.a > 1 ? sd.a : "") + "\\sqrt{" + sd.b + "}", top = (p ? p + (t < 0 ? "-" : "+") : t < 0 ? "-" : "") + rd;
        return d === 1 ? top : "\\dfrac{" + top + "}{" + d + "}";
      }
    }
    return dT(r, 3);
  }
  function setT(S) {
    if (!S.ivs.length) return "\\varnothing";
    function e(v) { return v === Infinity ? "+\\infty" : v === -Infinity ? "-\\infty" : niceT(v); }
    if (S.ivs[0].a === -Infinity && S.ivs[S.ivs.length - 1].b === Infinity && S.ivs.every(function (v, i) { return i === 0 || v.a === S.ivs[i - 1].b; })) {
      if (S.ivs.length === 1) return "\\mathbb{R}";
      return "\\mathbb{R}-\\left\\{" + S.ivs.slice(1).map(function (v) { return niceT(v.a); }).join(",\\,") + "\\right\\}";
    }
    return S.ivs.map(function (v) { return v.a === v.b ? "\\left\\{" + niceT(v.a) + "\\right\\}" : (v.ac ? "[" : "(") + e(v.a) + ",\\," + e(v.b) + (v.bc ? "]" : ")"); }).join("\\cup ");
  }
  function sgnT(v) { return !v ? "" : (v > 0 ? "+" : "-") + numT(Math.abs(v)); }
  function fnField(w, onChange) {
    var inp = $(w, "f"), ast = parseF(inp.value);
    inp.addEventListener("input", function () { var a = parseF(inp.value); inp.classList.toggle("bad", !a); if (a) { ast = a; onChange(); } });
    return { get: function () { return ast; }, set: function (s) { inp.value = s; inp.classList.remove("bad"); ast = parseF(s); onChange(); } };
  }
  function presetsOf(w, list, field, role) { presetBtns($(w, role || "pre"), function () { return list.map(function (s) { return tex(toT(parseF(s))); }); }, function (i) { field.set(list[i]); }, 0); }

  /* ---------- 7.2 recta per dos punts (de 4t ESO B, 8.1) ---------- */
  function wLin() {
    var w = byId("w-lin"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), P = [{ x: 1, y: 3 }, { x: 3, y: 7 }];
    var G = plane(-6, 6, -6, 8, 1);
    dragger(svg, function () { return G; }, function () { return P; }, function (i, d) { var x = Math.max(-6, Math.min(6, Math.round(d.x))), y = Math.max(-6, Math.min(8, Math.round(d.y))); if (P[i].x !== x || P[i].y !== y) { P[i].x = x; P[i].y = y; draw(); } });
    function draw() {
      var A = P[0], B = P[1], h = G.g + G.open, dx = B.x - A.x, dy = B.y - A.y, rows = [["A", tex("(" + A.x + ",\\," + A.y + ")")], ["B", tex("(" + B.x + ",\\," + B.y + ")")]];
      if (!dx) {
        h += vdash(G, A.x);
        rows.push([t3("Recta", "Recta", "Line"), tex(dy ? "x=" + A.x : "\\text{A = B}") + small(t3("Una recta vertical no és una funció: el pendent no existeix.", "Una recta vertical no es una función: la pendiente no existe.", "A vertical line isn't a function: the slope doesn't exist."))]);
      } else {
        var m = Fr(dy, dx), n = fSub(A.y, fMul(m, A.x)), mv = fVal(m), nv = fVal(n);
        h += curve(G, function (x) { return mv * x + nv; }, AC, { n: 20 }) + '<line class="gd" x1="' + f1(G.X(A.x)) + '" y1="' + f1(G.Y(A.y)) + '" x2="' + f1(G.X(B.x)) + '" y2="' + f1(G.Y(A.y)) + '"/><line class="gd" x1="' + f1(G.X(B.x)) + '" y1="' + f1(G.Y(A.y)) + '" x2="' + f1(G.X(B.x)) + '" y2="' + f1(G.Y(B.y)) + '"/>';
        var pp = "y=" + A.y + (m.n ? (m.n > 0 ? "+" : "-") + (Math.abs(fVal(m)) === 1 ? "" : fT(Fr(Math.abs(m.n), m.d))) + "\\left(x" + sgnT(-A.x) + "\\right)" : "");
        rows.push([t3("Pendent", "Pendiente", "Slope"), tex("m=\\dfrac{" + B.y + (A.y < 0 ? "+" + -A.y : "-" + A.y) + "}{" + B.x + (A.x < 0 ? "+" + -A.x : "-" + A.x) + "}=" + fT(m))]);
        rows.push([t3("Punt-pendent", "Punto-pendiente", "Point-slope"), tex(pp)]);
        rows.push([t3("Explícita", "Explícita", "Slope-intercept"), "<strong>" + tex("y=" + polyT([n, m])) + "</strong>"]);
        rows.push([t3("Tipus", "Tipo", "Type"), !m.n ? t3("Constant", "Constante", "Constant") : !n.n ? t3("De proporcionalitat directa, ", "De proporcionalidad directa, ", "Direct proportion, ") + (m.n > 0 ? t3("creixent", "creciente", "increasing") : t3("decreixent", "decreciente", "decreasing")) : t3("Lineal, ", "Lineal, ", "Linear, ") + (m.n > 0 ? t3("creixent", "creciente", "increasing") : t3("decreixent", "decreciente", "decreasing"))]);
      }
      P.forEach(function (p, i) { h += '<circle class="halo" cx="' + f1(G.X(p.x)) + '" cy="' + f1(G.Y(p.y)) + '" r="16"/><circle class="pt drag" cx="' + f1(G.X(p.x)) + '" cy="' + f1(G.Y(p.y)) + '" r="7" style="fill:' + BL + '"/>' + gtext(G, p.x, p.y, "AB"[i], BL, 12, -8); });
      svg.innerHTML = h + G.close; info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 7.3 quadràtica (de 4t ESO B, 8.2) ---------- */
  function wQuad() {
    var w = byId("w-quad"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), S = {};
    ["a", "b", "c"].forEach(function (k) { S[k] = $(w, k); S[k].addEventListener("input", draw); });
    function draw() {
      var a = +S.a.value, b = +S.b.value, c = +S.c.value; if (!a) { a = .5; S.a.value = .5; }
      ["a", "b", "c"].forEach(function (k) { $(w, k + "v").innerHTML = dT(+S[k].value, 1); });
      var af = Fr(Math.round(a * 2), 2), vx = fDiv(-b, fMul(2, af)), vy = fAdd(fAdd(fMul(af, fMul(vx, vx)), fMul(b, vx)), c), xv = fVal(vx), yv = fVal(vy), D = b * b - 4 * a * c;
      var G = plane(-8, 8, -8, 8, 2), f = function (x) { return a * x * x + b * x + c; }, h = G.g + G.open + vdash(G, xv) + curve(G, f, GR, { n: 500 });
      var rts = D > 1e-9 ? [(-b - Math.sqrt(D)) / (2 * a), (-b + Math.sqrt(D)) / (2 * a)].sort(function (p, q) { return p - q; }) : Math.abs(D) <= 1e-9 ? [-b / (2 * a)] : [];
      h += gdot(G, 0, c, GR); rts.forEach(function (r) { h += gdot(G, r, 0, BL); }); h += gdot(G, xv, yv, VI);
      svg.innerHTML = h + G.close;
      info.innerHTML = kv([
        ["", tex("f(x)=" + polyT([Fr(c), Fr(b), af]))],
        [t3("Forma", "Forma", "Shape"), a > 0 ? t3("Branques cap amunt ∪ (a > 0): el vèrtex és el mínim", "Ramas hacia arriba ∪ (a > 0): el vértice es el mínimo", "Arms up ∪ (a > 0): the vertex is the minimum") : t3("Branques cap avall ∩ (a < 0): el vèrtex és el màxim", "Ramas hacia abajo ∩ (a < 0): el vértice es el máximo", "Arms down ∩ (a < 0): the vertex is the maximum")],
        [t3("Vèrtex", "Vértice", "Vertex"), tex("V_x=\\dfrac{-b}{2a}=" + fT(vx) + ",\\ \\ V_y=f(V_x)=" + fT(vy))],
        [t3("Eix de simetria", "Eje de simetría", "Axis"), tex("x=" + fT(vx))],
        [t3("Tall eix OY", "Corte eje OY", "y-intercept"), tex("(0,\\ " + dT(c, 1) + ")")],
        [t3("Talls eix OX", "Cortes eje OX", "x-intercepts"), rts.length ? rts.map(function (r) { return tex("(" + niceT(snap(r)) + ",\\ 0)"); }).join(", ") : t3("No en té (Δ < 0)", "No tiene (Δ < 0)", "None (Δ < 0)")],
        [t3("Recorregut", "Recorrido", "Range"), tex(a > 0 ? "[" + fT(vy) + ",\\,+\\infty)" : "(-\\infty,\\," + fT(vy) + "]")]
      ]);
    }
    onLang(draw);
  }
  /* ---------- 7.5 i 7.7 laboratoris de radicals i hipèrboles (de 4t ESO B, 8.3) ---------- */
  var BASES = [{ v: 1 / 3, t: "\\frac13" }, { v: .5, t: "\\frac12" }, { v: 2, t: "2" }, { v: 3, t: "3" }, { v: Math.E, t: "e" }, { v: 10, t: "10" }];
  function wTrans(id, kind) {
    var w = byId(id); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), ctl = [].slice.call(w.querySelectorAll("[data-role]")).filter(function (e) { return e.tagName === "INPUT"; }), v = {};
    ctl.forEach(function (e) { e.addEventListener(e.type === "checkbox" ? "change" : "input", draw); });
    function inc() { return t3("Creixent", "Creciente", "Increasing"); } function dec() { return t3("Decreixent", "Decreciente", "Decreasing"); }
    var IR = "\\mathbb R", MO = t3("Monotonia", "Monotonía", "Monotonicity"), DO = t3("Domini", "Dominio", "Domain"), RE = t3("Recorregut", "Recorrido", "Range");
    function draw() {
      IR = "\\mathbb R"; MO = t3("Monotonia", "Monotonía", "Monotonicity"); DO = t3("Domini", "Dominio", "Domain"); RE = t3("Recorregut", "Recorrido", "Range");
      ctl.forEach(function (e) { var r = e.getAttribute("data-role"); v[r] = e.type === "checkbox" ? e.checked : +e.value; var o = $(w, r + "v"); if (o) o.innerHTML = kind !== "rad" && r === "a" ? tex(BASES[v.a].t) : numT(v[r]); });
      var G = plane(-8, 8, -8, 8, 2), h = G.g + G.open, f, base, rows, h0 = v.h, v0 = v.v, ref;
      var xh = function (s) { return "x" + sgnT(s); };
      if (kind === "rac") {
        if (!v.k) { v.k = 1; $(w, "k").value = 1; $(w, "kv").innerHTML = "1"; }
        f = function (x) { return Math.abs(x - h0) < 1e-9 ? NaN : v.k / (x - h0) + v0; }; base = function (x) { return x ? v.k / x : NaN; };
        h += vdash(G, h0) + hdash(G, v0);
        rows = [["", tex("y=\\dfrac{" + v.k + "}{" + xh(-h0) + "}" + sgnT(v0))], [t3("Asímptota vertical", "Asíntota vertical", "Vertical asymptote"), tex("x=" + h0)], [t3("Asímptota horitzontal", "Asíntota horizontal", "Horizontal asymptote"), tex("y=" + v0)], [DO, tex(IR + "-\\{" + h0 + "\\}")], [RE, tex(IR + "-\\{" + v0 + "\\}")], [MO, (v.k > 0 ? dec() : inc()) + t3(" a cada branca", " en cada rama", " on each branch")]];
      } else if (kind === "rad") {
        var sx = v.sx ? -1 : 1, sy = v.sy ? -1 : 1;
        f = function (x) { var u = sy * (x - h0); return u < -1e-9 ? NaN : sx * Math.sqrt(Math.max(u, 0)) + v0; }; base = function (x) { return x < 0 ? NaN : Math.sqrt(x); };
        ref = [h0, v0];
        rows = [["", tex("y=" + (sx < 0 ? "-" : "") + "\\sqrt{" + (sy < 0 ? "-x" : "x") + sgnT(-sy * h0) + "}" + sgnT(v0))], [t3("Punt inicial", "Punto inicial", "Starting point"), tex("(" + h0 + ",\\ " + v0 + ")")], [DO, tex(sy > 0 ? "[" + h0 + ",\\,+\\infty)" : "(-\\infty,\\," + h0 + "]")], [RE, tex(sx > 0 ? "[" + v0 + ",\\,+\\infty)" : "(-\\infty,\\," + v0 + "]")], [MO, sx * sy > 0 ? inc() : dec()]];
      } else if (kind === "exp") {
        var a = BASES[v.a], s = v.s ? -1 : 1, bt = a.v < 1 ? "\\left(" + a.t + "\\right)" : a.t;
        f = function (x) { return s * Math.pow(a.v, x + h0) + v0; }; base = function (x) { return Math.pow(a.v, x); };
        h += hdash(G, v0); ref = [-h0, s + v0];
        rows = [["", tex("y=" + (s < 0 ? "-" : "") + bt + "^{" + xh(h0) + "}" + sgnT(v0))], [t3("Asímptota horitzontal", "Asíntota horizontal", "Horizontal asymptote"), tex("y=" + v0)], [t3("Punt de referència", "Punto de referencia", "Reference point"), tex("(" + -h0 + ",\\ " + (s + v0) + ")")], [DO, tex(IR)], [RE, tex(s > 0 ? "(" + v0 + ",\\,+\\infty)" : "(-\\infty,\\," + v0 + ")")], [MO, s * (a.v > 1 ? 1 : -1) > 0 ? inc() : dec()]];
      } else {
        var b = BASES[v.a], sg = v.s ? -1 : 1;
        f = function (x) { return x + h0 <= 1e-9 ? NaN : sg * Math.log(x + h0) / Math.log(b.v) + v0; }; base = function (x) { return x <= 0 ? NaN : Math.log(x) / Math.log(b.v); };
        h += vdash(G, -h0); ref = [1 - h0, v0];
        var nm = b.v === Math.E ? "\\ln" : b.v === 10 ? "\\log" : "\\log_{" + b.t + "}";
        rows = [["", tex("y=" + (sg < 0 ? "-" : "") + nm + "\\left(" + xh(h0) + "\\right)" + sgnT(v0))], [t3("Asímptota vertical", "Asíntota vertical", "Vertical asymptote"), tex("x=" + -h0)], [t3("Punt de referència", "Punto de referencia", "Reference point"), tex("(" + (1 - h0) + ",\\ " + v0 + ")")], [DO, tex("(" + -h0 + ",\\,+\\infty)")], [RE, tex(IR)], [MO, sg * (b.v > 1 ? 1 : -1) > 0 ? inc() : dec()]];
      }
      h += curve(G, base, MU, { dash: "5 5", w: 1.8, n: 1500 }) + curve(G, f, AC, { n: 1800 });
      if (ref) h += gdot(G, ref[0], ref[1], BL);
      svg.innerHTML = h + G.close;
      info.innerHTML = kv(rows);
    }
    onLang(draw);
  }
  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  /*@@NOUS@@*/
  /*@@QUIZ@@*/
  /*@@GENERIC@@*/
  var TITLES = { va: "Funcions elementals · FentMates", es: "Funciones elementales · FentMates", en: "Elementary functions · FentMates" };
  function piTicks(x0, x1, step) {
    var out = [], k;
    for (k = Math.ceil(x0 / (Math.PI * step) - 1e-9); k * Math.PI * step <= x1 + 1e-9; k++) {
      var f = Fr(k * Math.round(step * 4), 4), s = f.n === 0 ? "" : (f.n < 0 ? "−" : "") + (Math.abs(f.n) === 1 ? "" : Math.abs(f.n)) + "π" + (f.d > 1 ? "/" + f.d : "");
      out.push([k * Math.PI * step, s]);
    }
    return out;
  }
  function piT(f) {
    f = F(f); if (f.n === 0) return "0";
    var top = (Math.abs(f.n) === 1 ? "" : Math.abs(f.n)) + "\\pi";
    return (f.n < 0 ? "-" : "") + (f.d === 1 ? top : "\\frac{" + top + "}{" + f.d + "}");
  }
  function surd(n) { var a = 1, b = n, i; for (i = 2; i * i <= b; i++) while (b % (i * i) === 0) { b /= i * i; a *= i; } return { a: a, b: b }; }
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
    var all = [wChrome, wSteps, wNav, wTypes, wLin, wQuad, wQStep, wInv, wGrow, wCmp, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    [["w-rad", "rad"], ["w-rac", "rac"]].forEach(function (p) { try { wTrans(p[0], p[1]); } catch (e) { if (window.console) console.error(p[0], e); } });
    window.FM47A = { parseF: parseF, ev: ev, toT: toT, consOf: consOf, solveSet: solveSet, setT: setT, rootsF: rootsF, niceT: niceT, polyOf: polyOf, polyT: polyT, sub: sub };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
