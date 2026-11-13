(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1batx-mi-u7-done";

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
    return S.ivs.map(function (v) { return v.a === v.b ? "\\left\\{" + niceT(v.a) + "\\right\\}" : (v.ac ? "\\left[" : "\\left]") + e(v.a) + ",\\," + e(v.b) + (v.bc ? "\\right]" : "\\right["); }).join("\\cup ");
  }
  function sgnT(v) { return !v ? "" : (v > 0 ? "+" : "-") + numT(Math.abs(v)); }
  function fnField(w, onChange) {
    var inp = $(w, "f"), ast = parseF(inp.value);
    inp.addEventListener("input", function () { var a = parseF(inp.value); inp.classList.toggle("bad", !a); if (a) { ast = a; onChange(); } });
    return { get: function () { return ast; }, set: function (s) { inp.value = s; inp.classList.remove("bad"); ast = parseF(s); onChange(); } };
  }
  function presetsOf(w, list, field, role) { presetBtns($(w, role || "pre"), function () { return list.map(function (s) { return tex(toT(parseF(s))); }); }, function (i) { field.set(list[i]); }, 0); }

  /* ---------- 6.1 prova de la recta vertical ---------- */
  function wVert() {
    var w = byId("w-vert"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), sl = $(w, "x"), cur = 0;
    function sq(v) { return v < 0 ? NaN : Math.sqrt(v); }
    var R = [
      { t: "y=x^2-2", fun: true, br: [function (x) { return x * x - 2; }] },
      { t: "y=\\frac{x^3}{4}-x", fun: true, br: [function (x) { return x * x * x / 4 - x; }] },
      { t: "x^2+y^2=9", fun: false, br: [function (x) { return sq(9 - x * x); }, function (x) { return -sq(9 - x * x); }] },
      { t: "x=y^2-2", fun: false, br: [function (x) { return sq(x + 2); }, function (x) { return -sq(x + 2); }] }
    ];
    presetBtns($(w, "pre"), function () { return R.map(function (r) { return tex(r.t); }); }, function (i) { cur = i; draw(); }, 0);
    sl.addEventListener("input", draw);
    function draw() {
      var x = +sl.value, r = R[cur], G = plane(-5, 5, -4, 4), h = G.g + G.open;
      r.br.forEach(function (f) { h += curve(G, f, AC, { n: 1500 }); });
      h += seg(G, x, -4, x, 4, BL, 2);
      var ys = []; r.br.forEach(function (f) { var y = f(x); if (isFinite(y) && !ys.some(function (v) { return Math.abs(v - y) < 1e-6; })) ys.push(y); });
      ys.forEach(function (y) { h += gdot(G, x, y, BL); });
      svg.innerHTML = h + G.close;
      info.innerHTML = kv([
        [t3("Relació", "Relación", "Relation"), tex(r.t)],
        ["\\(x\\)".replace(/\\\(|\\\)/g, ""), tex("x=" + dT(x, 1))],
        [t3("Talls amb la vertical", "Cortes con la vertical", "Hits on the vertical"), "<strong>" + ys.length + "</strong>" + (ys.length ? " " + tex("y=" + ys.map(function (v) { return dT(v, 2); }).join(",\\ ")) : "")],
        [t3("Veredicte", "Veredicto", "Verdict"), r.fun ? "<strong class=\"sp\">" + t3("És una funció", "Es una función", "It is a function") + "</strong>" + small(t3("Cap recta vertical talla la gràfica més d'una vegada.", "Ninguna recta vertical corta la gráfica más de una vez.", "No vertical line meets the graph more than once.")) : "<strong class=\"sm\">" + t3("No és una funció", "No es una función", "Not a function") + "</strong>" + small(t3("Hi ha valors de x amb dues imatges.", "Hay valores de x con dos imágenes.", "Some values of x have two images."))]
      ]);
    }
    onLang(draw);
  }

  /* ---------- 6.2 domini analític ---------- */
  function wDom() {
    var w = byId("w-dom"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info");
    var fld = fnField(w, draw);
    presetsOf(w, ["3x+4", "(2x-1)/(x^2-4)", "sqrt(x^2+x-2)", "cbrt(x-7)", "2^(x+5)", "log2(6x+4)", "sqrt(x)/(x-3)"], fld);
    var NM = { ne: "\\neq", ge: "\\geq", gt: "\\gt" };
    function why(c) { return c.k === "ne" ? t3("El denominador no pot valdre 0", "El denominador no puede valer 0", "The denominator cannot be 0") : c.k === "ge" ? t3("El radicand d'índex parell ha de ser positiu o 0", "El radicando de índice par debe ser positivo o 0", "An even-index radicand must be positive or 0") : t3("L'argument del logaritme ha de ser positiu", "El argumento del logaritmo debe ser positivo", "A logarithm's argument must be positive"); }
    function draw() {
      var A = fld.get(), C = consOf(A, []), S = solveSet(C), G = plane(-8, 8, -6, 6, 2), h = G.g + G.open;
      h += curve(G, function (x) { return ev(A, x); }, AC, { n: 1600 });
      var rows = [["\\(f\\)".replace(/\\\(|\\\)/g, ""), tex("f(x)=" + toT(A))]];
      if (!S) rows.push([t3("Domini", "Dominio", "Domain"), t3("Té funcions trigonomètriques: el domini d'aquestes funcions es veu a la unitat 7 (apartat 7.7).", "Tiene funciones trigonométricas: el dominio de estas funciones se ve en la unidad 7 (apartado 7.7).", "It has trigonometric functions: their domain is covered in unit 7 (section 7.7).")]);
      else {
        if (!C.length) rows.push([t3("Condicions", "Condiciones", "Conditions"), t3("Cap: no hi ha denominadors amb x, ni arrels d'índex parell, ni logaritmes.", "Ninguna: no hay denominadores con x, ni raíces de índice par, ni logaritmos.", "None: no denominators containing x, even roots or logarithms.")]);
        C.forEach(function (c, i) { var one = solveSet([c]); rows.push([t3("Condició ", "Condición ", "Condition ") + (i + 1), tex(toT(c.g) + NM[c.k] + "0") + small(why(c)) + "<br>" + tex("\\Rightarrow\\ " + setT(one))]); });
        rows.push(["<strong>" + t3("Domini", "Dominio", "Domain") + "</strong>", "<strong>" + tex("D(f)=" + setT(S)) + "</strong>"]);
        S.ivs.forEach(function (v) {
          var a = Math.max(v.a, -8), b = Math.min(v.b, 8); if (a > 8 || b < -8) return;
          h += seg(G, a, 0, b, 0, BL, 5);
          if (v.a >= -8 && isFinite(v.a)) h += v.ac ? gdot(G, v.a, 0, BL) : odot(G, v.a, 0, BL);
          if (v.b <= 8 && isFinite(v.b) && v.b !== v.a) h += v.bc ? gdot(G, v.b, 0, BL) : odot(G, v.b, 0, BL);
        });
      }
      svg.innerHTML = h + G.close; info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 6.3 punts de tall ---------- */
  function wCut() {
    var w = byId("w-cut"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info");
    var fld = fnField(w, draw);
    presetsOf(w, ["x^2-x-6", "x^3-4x", "(x-2)/(x+1)", "sqrt(x+4)-1", "2^x-4", "x^2+1"], fld);
    function draw() {
      var A = fld.get(), f = function (x) { return ev(A, x); }, G = plane(-8, 8, -8, 8, 2), h = G.g + G.open + curve(G, f, AC, { n: 1600 });
      var y0 = f(0), rts = rootsF(f, hasTrig(A) ? -8 : -40, hasTrig(A) ? 8 : 40), rows = [["", tex("f(x)=" + toT(A))]];
      if (isFinite(y0)) { rows.push([t3("Eix OY", "Eje OY", "y-axis"), tex("x=0\\Rightarrow y=f(0)=" + niceT(snap(y0))) + "<br>" + t3("Talla en ", "Corta en ", "Meets it at ") + tex("(0,\\ " + niceT(snap(y0)) + ")")]); h += gdot(G, 0, y0, GR); }
      else rows.push([t3("Eix OY", "Eje OY", "y-axis"), t3("No el talla: x = 0 no és del domini.", "No lo corta: x = 0 no es del dominio.", "It doesn't: x = 0 isn't in the domain.")]);
      if (rts.length) { rows.push([t3("Eix OX", "Eje OX", "x-axis"), tex("y=0\\Rightarrow f(x)=0\\Rightarrow x=" + rts.map(niceT).join(",\\ x=")) + "<br>" + t3("Talla en ", "Corta en ", "Meets it at ") + rts.map(function (r) { return tex("(" + niceT(r) + ",\\ 0)"); }).join(", ")]); rts.forEach(function (r) { h += gdot(G, r, 0, BL); }); }
      else rows.push([t3("Eix OX", "Eje OX", "x-axis"), t3("No el talla: l'equació f(x) = 0 no té solució.", "No lo corta: la ecuación f(x) = 0 no tiene solución.", "It doesn't: f(x) = 0 has no solution.")]);
      svg.innerHTML = h + G.close; info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 6.4 monotonia amb punts arrossegables ---------- */
  function wMono() {
    var w = byId("w-mono"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), P0 = [12, 15, 13, 6, 10, 20, 15, 18, 10, 12, 7], P = P0.map(function (y, i) { return { x: i, y: y }; }), G;
    function view() { return gview({ x0: -.5, x1: 10.5, y0: 0, y1: 22, sy: 2, W: 360, H: 260, xt: ticks(0, 10, 1) }); }
    G = view();
    dragger(svg, function () { return G; }, function () { return P; }, function (i, d) { var y = Math.max(0, Math.min(22, Math.round(d.y))); if (P[i].y !== y) { P[i].y = y; draw(); } });
    $(w, "reset").addEventListener("click", function () { P0.forEach(function (y, i) { P[i].y = y; }); draw(); });
    function iv(a, b) { return "\\left]" + a + ",\\," + b + "\\right["; }
    function draw() {
      var h = G.g + G.open, i, sg = [];
      for (i = 0; i < 10; i++) { var d = P[i + 1].y - P[i].y; sg.push(d > 0 ? 1 : d < 0 ? -1 : 0); h += seg(G, i, P[i].y, i + 1, P[i + 1].y, sg[i] > 0 ? GR : sg[i] < 0 ? "#dc2626" : MU, 3); }
      var groups = { 1: [], "-1": [], 0: [] }, st = 0;
      for (i = 1; i <= 10; i++) if (i === 10 || sg[i] !== sg[st]) { groups[sg[st]].push(iv(st, i)); st = i; }
      var mx = Math.max.apply(null, P.map(function (p) { return p.y; })), mn = Math.min.apply(null, P.map(function (p) { return p.y; })), maxs = [], mins = [];
      for (i = 0; i <= 10; i++) {
        var l = i > 0 ? sg[i - 1] : null, r = i < 10 ? sg[i] : null, p = P[i], isM = l > 0 && r < 0, ism = l < 0 && r > 0, ext = i === 0 || i === 10;
        if (isM || (ext && p.y === mx && mx > mn)) maxs.push({ p: p, abs: p.y === mx });
        if (ism || (ext && p.y === mn && mx > mn)) mins.push({ p: p, abs: p.y === mn });
      }
      function lst(L) { return L.length ? L.map(function (m) { return tex("(" + m.p.x + ",\\," + m.p.y + ")") + (m.abs ? " <strong>" + t3("absolut", "absoluto", "absolute") + "</strong>" : ""); }).join("; ") : "—"; }
      P.forEach(function (p) { h += '<circle class="halo" cx="' + f1(G.X(p.x)) + '" cy="' + f1(G.Y(p.y)) + '" r="14"/>'; h += '<circle class="pt drag" cx="' + f1(G.X(p.x)) + '" cy="' + f1(G.Y(p.y)) + '" r="6" style="fill:' + AC + '"/>'; });
      maxs.concat(mins).forEach(function (m) { h += gtext(G, m.p.x, m.p.y, m.abs ? "★" : "", "#b45309", 0, -10); });
      svg.innerHTML = h + G.close;
      function join(a) { return a.length ? tex(a.join("\\cup ")) : "—"; }
      info.innerHTML = kv([
        ['<i class="tag-c" style="background:' + GR + '"></i>' + t3("Creixent", "Creciente", "Increasing"), join(groups[1])],
        ['<i class="tag-c" style="background:#dc2626"></i>' + t3("Decreixent", "Decreciente", "Decreasing"), join(groups[-1])],
        ['<i class="tag-c" style="background:' + MU + '"></i>' + t3("Constant", "Constante", "Constant"), join(groups[0])],
        [t3("Màxims", "Máximos", "Maxima"), lst(maxs)],
        [t3("Mínims", "Mínimos", "Minima"), lst(mins)]
      ]);
    }
    onLang(draw);
  }

  /* ---------- 6.5 tipus de discontinuïtat ---------- */
  function wDisc() {
    var w = byId("w-disc"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), S = {}, c = 2;
    ["L", "R", "V"].forEach(function (k) { S[k] = $(w, k); S[k].addEventListener("input", draw); });
    ["Li", "Ri", "Ve"].forEach(function (k) { S[k] = $(w, k); S[k].addEventListener("change", draw); });
    var PR = [[1, 1, 1, false, false, true], [1, 1, 1, false, false, false], [1, 1, 3, false, false, true], [3, 1, 3, false, false, true], [1, 1, 1, true, false, true], [1, 1, 1, true, true, false]];
    presetBtns($(w, "pre"), function () { return [t3("Contínua", "Continua", "Continuous"), t3("Evitable (forat)", "Evitable (agujero)", "Removable (hole)"), t3("Evitable (punt fora)", "Evitable (punto fuera)", "Removable (point off)"), t3("Salt finit", "Salto finito", "Finite jump"), t3("Salt infinit", "Salto infinito", "Infinite jump"), t3("Asimptòtica", "Asintótica", "Asymptotic")]; }, function (i) {
      var p = PR[i]; S.L.value = p[0]; S.R.value = p[1]; S.V.value = p[2]; S.Li.checked = p[3]; S.Ri.checked = p[4]; S.Ve.checked = p[5]; draw();
    }, 0);
    function draw() {
      var L = +S.L.value, R = +S.R.value, V = +S.V.value, Li = S.Li.checked, Ri = S.Ri.checked, Ve = S.Ve.checked;
      $(w, "Lv").innerHTML = Li ? "∞" : dT(L, 1); $(w, "Rv").innerHTML = Ri ? "∞" : dT(R, 1); $(w, "Vv").innerHTML = Ve ? dT(V, 1) : "—";
      var G = plane(-3, 7, -4, 6), h = G.g + G.open + vdash(G, c);
      var fl = Li ? function (x) { return L + 1 / (c - x); } : function (x) { return L + .25 * (x - c) + .35 * Math.sin((x - c) * 1.6); };
      var fr = Ri ? function (x) { return R + 1 / (x - c); } : function (x) { return R + .35 * (x - c) - .3 * Math.sin((x - c) * 1.4); };
      h += curve(G, fl, AC, { a: -3, b: c - .002, n: 800 }) + curve(G, fr, AC, { a: c + .002, b: 7, n: 800 });
      if (!Li) h += odot(G, c, L, AC); if (!Ri) h += odot(G, c, R, AC);
      if (Ve) h += gdot(G, c, V, AC);
      var kind, col = "sm", ex;
      if (Li && Ri) { kind = t3("Discontinuïtat asimptòtica", "Discontinuidad asintótica", "Asymptotic discontinuity"); ex = t3("La funció tendeix a infinit pels dos costats: hi ha una asímptota vertical.", "La función tiende a infinito por los dos lados: hay una asíntota vertical.", "The function tends to infinity on both sides: there is a vertical asymptote."); }
      else if (Li || Ri) { kind = t3("Discontinuïtat de salt infinit", "Discontinuidad de salto infinito", "Infinite-jump discontinuity"); ex = t3("Per un costat la funció tendeix a infinit i per l'altre s'acosta a un valor finit.", "Por un lado la función tiende a infinito y por el otro se acerca a un valor finito.", "On one side the function tends to infinity; on the other it approaches a finite value."); }
      else if (L !== R) { kind = t3("Discontinuïtat de salt finit", "Discontinuidad de salto finito", "Finite-jump discontinuity"); ex = t3("Els dos trossos arriben a altures diferents. El salt és ", "Los dos trozos llegan a alturas diferentes. El salto es ", "The two pieces reach different heights. The jump is ") + tex("|" + dT(L, 1) + "-" + (R < 0 ? "(" + dT(R, 1) + ")" : dT(R, 1)) + "|=" + dT(Math.abs(L - R), 1)) + "."; }
      else if (Ve && V === L) { kind = t3("Contínua en x = 2", "Continua en x = 2", "Continuous at x = 2"); col = "sp"; ex = t3("Els dos trossos arriben a la mateixa altura i el punt és justament allí: es dibuixa sense alçar el llapis.", "Los dos trozos llegan a la misma altura y el punto está justo allí: se dibuja sin levantar el lápiz.", "Both pieces reach the same height and the point is right there: you can draw it without lifting your pen."); }
      else { kind = t3("Discontinuïtat evitable", "Discontinuidad evitable", "Removable discontinuity"); ex = (Ve ? t3("El punt està fora de lloc.", "El punto está fuera de lugar.", "The point is out of place.") : t3("Falta el punt.", "Falta el punto.", "The point is missing.")) + " " + t3("N'hi hauria prou amb definir ", "Bastaría con definir ", "It would be enough to define ") + tex("f(2)=" + dT(L, 1)) + "."; }
      svg.innerHTML = h + G.close;
      info.innerHTML = kv([[t3("Per l'esquerra", "Por la izquierda", "From the left"), Li ? tex("+\\infty") : tex(dT(L, 1))], [t3("Per la dreta", "Por la derecha", "From the right"), Ri ? tex("+\\infty") : tex(dT(R, 1))], [tex("f(2)"), Ve ? tex(dT(V, 1)) : t3("no existeix", "no existe", "undefined")], [t3("Tipus", "Tipo", "Type"), '<strong class="' + col + '">' + kind + "</strong>" + small(ex)]]);
    }
    onLang(draw);
  }

  /* ---------- 6.6 simetries i període ---------- */
  function wSym() {
    var w = byId("w-sym"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), sl = $(w, "a");
    var fld = fnField(w, draw); sl.addEventListener("input", draw);
    presetsOf(w, ["x^2+1", "x^2/(x^4-1)", "x^3+x", "x/(x^2+3)", "x^2+x", "abs(x)-2"], fld);
    function draw() {
      var A = fld.get(), f = function (x) { return ev(A, x); }, a = +sl.value, G = plane(-6, 6, -6, 6, 2), h = G.g + G.open + curve(G, f, AC, { n: 1600 });
      var even = true, odd = true, n = 0, i;
      for (i = 1; i <= 80; i++) { var x = .137 * i, p = f(x), q = f(-x); if (isFinite(p) !== isFinite(q)) { even = odd = false; break; } if (!isFinite(p)) continue; n++; if (Math.abs(q - p) > 1e-7 * Math.max(1, Math.abs(p))) even = false; if (Math.abs(q + p) > 1e-7 * Math.max(1, Math.abs(p))) odd = false; }
      if (!n) even = odd = false;
      var nx = { t: "neg", a: { t: "x" } }, sb = sub(A, nx), P = polyOf(sb), fa = f(a), fb = f(-a);
      if (isFinite(fa)) h += gdot(G, a, fa, BL) + gtext(G, a, fa, "P", BL, 0, -10);
      if (isFinite(fb)) h += gdot(G, -a, fb, OR) + gtext(G, -a, fb, "Q", OR, 0, -10);
      svg.innerHTML = h + G.close;
      var verdict = even && odd ? t3("Parella i senar (és la funció zero)", "Par e impar (es la función cero)", "Both even and odd (the zero function)") : even ? t3("Parella: simètrica respecte de l'eix OY", "Par: simétrica respecto del eje OY", "Even: symmetric about the y-axis") : odd ? t3("Senar: simètrica respecte de l'origen", "Impar: simétrica respecto del origen", "Odd: symmetric about the origin") : t3("Ni parella ni senar", "Ni par ni impar", "Neither even nor odd");
      info.innerHTML = kv([
        ["", tex("f(x)=" + toT(A))],
        [tex("f(-x)"), tex(P ? polyT(P) : toT(sb))],
        ["P", isFinite(fa) ? tex("f(" + dT(a, 1) + ")=" + dT(fa, 2)) : "—"],
        ["Q", isFinite(fb) ? tex("f(" + dT(-a, 1) + ")=" + dT(fb, 2)) : "—"],
        [t3("Conclusió", "Conclusión", "Conclusion"), "<strong>" + verdict + "</strong>"]
      ]);
    }
    onLang(draw);
  }
  function wPer() {
    var w = byId("w-per"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), sl = $(w, "T"), cur = 0;
    function saw(x) { var t = ((x % 2) + 2) % 2; return t < 1 ? 2 * t - 1 : 3 - 2 * t; }
    function ecg(x) { var t = ((x % 3) + 3) % 3; return t < .4 ? .3 * Math.sin(t / .4 * Math.PI) : t > 1 && t < 1.15 ? -.4 * (t - 1) / .15 : t >= 1.15 && t < 1.3 ? -.4 + 2.9 * (t - 1.15) / .15 : t >= 1.3 && t < 1.5 ? 2.5 - 3.2 * (t - 1.3) / .2 : t >= 1.5 && t < 1.6 ? -.7 + .7 * (t - 1.5) / .1 : t > 2 && t < 2.6 ? .55 * Math.sin((t - 2) / .6 * Math.PI) : 0; }
    var FN = [{ f: Math.cos, T: 2 * Math.PI, n: "y=\\cos x", tt: "2\\pi", y0: -2.5, y1: 3 }, { f: saw, T: 2, n: t3 ? "\\text{zig-zag}" : "", tt: "2", y0: -2.5, y1: 3 }, { f: ecg, T: 3, n: "\\text{ECG}", tt: "3", y0: -1.5, y1: 3.5 }];
    presetBtns($(w, "pre"), function () { return [tex("\\cos x"), "zig-zag", t3("Electrocardiograma", "Electrocardiograma", "ECG")]; }, function (i) { cur = i; draw(); }, 0);
    sl.addEventListener("input", draw);
    function draw() {
      var o = FN[cur], T = +sl.value, G = gview({ x0: -1, x1: 13, y0: o.y0, y1: o.y1, sy: 1, W: 360, H: 220, xt: ticks(0, 13, 1) }), ok = true, i;
      for (i = 0; i < 400; i++) { var x = i * .0371; if (Math.abs(o.f(x + T) - o.f(x)) > 1e-6) { ok = false; break; } }
      var h = G.g + G.open + curve(G, o.f, AC, { n: 1500 }) + curve(G, function (x) { return o.f(x - T); }, BL, { n: 1500, dash: "6 5", w: 2 });
      h += vdash(G, 0) + vdash(G, T) + seg(G, 0, o.y1 - .35, T, o.y1 - .35, ok ? GR : "#dc2626", 3.5);
      svg.innerHTML = h + G.close;
      $(w, "Tv").innerHTML = dT(T, 2);
      info.innerHTML = kv([[t3("Desplaçament", "Desplazamiento", "Shift"), tex("T=" + dT(T, 2))], [t3("Coincideix?", "¿Coincide?", "Do they match?"), ok ? "<strong class=\"sp\">" + t3("Sí: f(x + T) = f(x) per a tot x", "Sí: f(x + T) = f(x) para todo x", "Yes: f(x + T) = f(x) for all x") + "</strong>" : "<strong class=\"sm\">" + t3("No", "No", "No") + "</strong>"], [t3("Període de la funció", "Periodo de la función", "Period of the function"), tex("T=" + o.tt)]]);
    }
    onLang(draw);
  }

  /* ---------- 6.7 translacions ---------- */
  function wTr() {
    var w = byId("w-tr"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), sh = $(w, "h"), sk = $(w, "k"), cur = 0;
    function P(s) { return "\\left(" + s + "\\right)"; }
    function iv(a, b, ca, cb) { return (ca ? "\\left[" : "\\left]") + a + ",\\," + b + (cb ? "\\right]" : "\\right["); }
    var B = [
      { t: "x^2", e: function (u, h) { return (h ? P(u) : u) + "^2"; }, f: function (x) { return x * x; }, p: [0, 0], pn: function () { return t3("Vèrtex", "Vértice", "Vertex"); },
        D: function () { return "\\mathbb R"; }, R: function (h, k) { return iv(numT(k), "+\\infty", true, false); } },
      { t: "|x|", e: function (u) { return "\\left|" + u + "\\right|"; }, f: Math.abs, p: [0, 0], pn: function () { return t3("Vèrtex", "Vértice", "Vertex"); },
        D: function () { return "\\mathbb R"; }, R: function (h, k) { return iv(numT(k), "+\\infty", true, false); } },
      { t: "\\sqrt x", e: function (u) { return "\\sqrt{" + u + "}"; }, f: function (x) { return x < 0 ? NaN : Math.sqrt(x); }, p: [0, 0], pn: function () { return t3("Punt inicial", "Punto inicial", "Starting point"); },
        D: function (h) { return iv(numT(h), "+\\infty", true, false); }, R: function (h, k) { return iv(numT(k), "+\\infty", true, false); } },
      { t: "\\dfrac1x", e: function (u) { return "\\dfrac{1}{" + u + "}"; }, f: function (x) { return Math.abs(x) < 1e-9 ? NaN : 1 / x; }, p: null, as: [0, 0],
        D: function (h) { return "\\mathbb R-\\{" + numT(h) + "\\}"; }, R: function (h, k) { return "\\mathbb R-\\{" + numT(k) + "\\}"; } },
      { t: "x^3", e: function (u, h) { return (h ? P(u) : u) + "^3"; }, f: function (x) { return x * x * x; }, p: [0, 0], pn: function () { return t3("Punt (0, 0)", "Punto (0, 0)", "Point (0, 0)"); },
        D: function () { return "\\mathbb R"; }, R: function () { return "\\mathbb R"; } },
      { t: "2^x", e: function (u) { return "2^{" + u + "}"; }, f: function (x) { return Math.pow(2, x); }, p: [0, 1], ah: 0, pn: function () { return t3("Punt (0, 1)", "Punto (0, 1)", "Point (0, 1)"); },
        D: function () { return "\\mathbb R"; }, R: function (h, k) { return iv(numT(k), "+\\infty", false, false); } }
    ];
    presetBtns($(w, "pre"), function () { return B.map(function (b) { return tex("y=" + b.t); }); }, function (i) { cur = i; draw(); }, 0);
    sh.addEventListener("input", draw); sk.addEventListener("input", draw);
    function mv(v, pos, neg) { return !v ? t3("cap", "ninguna", "none") : numT(Math.abs(v)) + " " + (v > 0 ? pos : neg); }
    function draw() {
      var b = B[cur], h = +sh.value, k = +sk.value, G = plane(-7, 7, -6, 7, 1), H = G.g + G.open;
      $(w, "hv").innerHTML = numT(h); $(w, "kv").innerHTML = numT(k);
      var g = function (x) { return b.f(x - h) + k; }, inner = h ? "x" + sgnT(-h) : "x";
      if (b.as) H += vdash(G, h) + hdash(G, k);
      if (b.ah != null) H += hdash(G, k);
      H += curve(G, b.f, MU, { dash: "5 5", w: 1.8, n: 1500 }) + curve(G, g, AC, { n: 1500 });
      var rows = [["", tex("y=" + b.e(inner, h) + sgnT(k))],
        [t3("Horitzontal", "Horizontal", "Horizontal"), mv(h, t3("cap a la dreta", "hacia la derecha", "to the right"), t3("cap a l'esquerra", "hacia la izquierda", "to the left"))],
        [t3("Vertical", "Vertical", "Vertical"), mv(k, t3("cap amunt", "hacia arriba", "up"), t3("cap avall", "hacia abajo", "down"))]];
      if (b.p) {
        var q = [b.p[0] + h, b.p[1] + k];
        H += '<line class="gd" x1="' + f1(G.X(b.p[0])) + '" y1="' + f1(G.Y(b.p[1])) + '" x2="' + f1(G.X(q[0])) + '" y2="' + f1(G.Y(q[1])) + '"/>' + gdot(G, b.p[0], b.p[1], MU) + gdot(G, q[0], q[1], BL);
        rows.push([b.pn(), tex("(" + b.p[0] + ",\\," + b.p[1] + ")\\to(" + numT(q[0]) + ",\\," + numT(q[1]) + ")")]);
      }
      if (b.as) rows.push([t3("Asímptotes", "Asíntotas", "Asymptotes"), tex("x=" + numT(h) + ",\\ \\ y=" + numT(k))]);
      if (b.ah != null) rows.push([t3("Asímptota", "Asíntota", "Asymptote"), tex("y=" + numT(k))]);
      rows.push([t3("Domini", "Dominio", "Domain"), tex(b.D(h))], [t3("Recorregut", "Recorrido", "Range"), tex(b.R(h, k))]);
      svg.innerHTML = H + G.close; info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 6.8 composició ---------- */
  function wComp() {
    var w = byId("w-comp"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), fi = $(w, "ff"), gi = $(w, "gf"), xi = $(w, "x0"), f = parseF(fi.value), g = parseF(gi.value);
    function chg() { var a = parseF(fi.value), b = parseF(gi.value); fi.classList.toggle("bad", !a); gi.classList.toggle("bad", !b); if (a) f = a; if (b) g = b; draw(); }
    fi.addEventListener("input", chg); gi.addEventListener("input", chg); xi.addEventListener("input", draw);
    var PR = [["x^2-1", "3x/(x-1)"], ["x^2-1", "sqrt(x+1)"], ["x^2-1", "x^2-1"], ["2x+1", "x^3"]];
    presetBtns($(w, "pre"), function () { return PR.map(function (p) { return tex("f=" + toT(parseF(p[0])) + ",\\ g=" + toT(parseF(p[1]))); }); }, function (i) { fi.value = PR[i][0]; gi.value = PR[i][1]; chg(); }, 0);
    function comp(a, b) { var s = sub(a, b), p = polyOf(s), t = toT(s); return p ? (polyT(p) === t ? t : t + "=" + polyT(p)) : t; }
    function draw() {
      var fg = sub(f, g), gf = sub(g, f), x0 = +xi.value, G = plane(-6, 6, -6, 8, 2), h = G.g + G.open, g0 = ev(g, x0), v = ev(f, g0), S = solveSet(consOf(fg, []));
      h += curve(G, function (x) { return ev(gf, x); }, BL, { n: 1500, w: 2 }) + curve(G, function (x) { return ev(fg, x); }, AC, { n: 1500 });
      if (isFinite(v)) h += gdot(G, x0, v, AC);
      svg.innerHTML = h + G.close; $(w, "x0v").innerHTML = dT(x0, 1);
      var X0 = dT(x0, 1);
      info.innerHTML = kv([
        ['<i class="tag-c" style="background:' + AC + '"></i>' + tex("(f\\circ g)(x)"), tex("f(g(x))=" + comp(f, g))],
        ['<i class="tag-c" style="background:' + BL + '"></i>' + tex("(g\\circ f)(x)"), tex("g(f(x))=" + comp(g, f))],
        [t3("Pas a pas", "Paso a paso", "Step by step"), isFinite(g0) ? tex("g(" + X0 + ")=" + dT(g0, 3)) + (isFinite(v) ? "<br>" + tex("f(" + dT(g0, 3) + ")=" + dT(v, 3)) : "<br>" + t3("f no existeix en aquest valor", "f no existe en ese valor", "f is undefined there")) : t3("g no existeix en aquest valor", "g no existe en ese valor", "g is undefined there")],
        [tex("D(f\\circ g)"), S ? tex(setT(S)) : "—"]
      ]);
    }
    onLang(draw);
  }

  /* ---------- 6.9 inversa ---------- */
  function wInv() {
    var w = byId("w-inv"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), sl = $(w, "t"), cur = 0;
    var PR = [
      { n: "f(x)=3x-1", f: function (x) { return 3 * x - 1; }, g: function (x) { return (x + 1) / 3; }, a: -2, b: 3, st: ["y=3x-1", "x=3y-1", "y=\\dfrac{x+1}{3}"], r: "f^{-1}(x)=\\dfrac{x+1}{3}" },
      { n: "f(x)=2^x+1", f: function (x) { return Math.pow(2, x) + 1; }, g: function (x) { return x > 1 ? Math.log2(x - 1) : NaN; }, a: -3, b: 2.8, st: ["y=2^x+1", "x=2^y+1", "2^y=x-1\\Rightarrow y=\\log_2(x-1)"], r: "f^{-1}(x)=\\log_2(x-1)" },
      { n: "f(x)=3x^2+2,\\ x\\ge0", f: function (x) { return x < 0 ? NaN : 3 * x * x + 2; }, g: function (x) { return x < 2 ? NaN : Math.sqrt((x - 2) / 3); }, a: 0, b: 1.7, st: ["y=3x^2+2", "x=3y^2+2", "y^2=\\dfrac{x-2}{3}\\Rightarrow y=\\sqrt{\\dfrac{x-2}{3}}"], r: "f^{-1}(x)=\\sqrt{\\dfrac{x-2}{3}}" },
      { n: "g(x)=\\dfrac{3}{x-1}", f: function (x) { return Math.abs(x - 1) < 1e-9 ? NaN : 3 / (x - 1); }, g: function (x) { return Math.abs(x) < 1e-9 ? NaN : 1 + 3 / x; }, a: 1.5, b: 6, st: ["y=\\dfrac{3}{x-1}", "x=\\dfrac{3}{y-1}", "y-1=\\dfrac3x\\Rightarrow y=1+\\dfrac3x"], r: "g^{-1}(x)=\\dfrac{x+3}{x}" }
    ];
    presetBtns($(w, "pre"), function () { return PR.map(function (p) { return tex(p.n); }); }, function (i) { cur = i; sl.value = 50; draw(); }, 0);
    sl.addEventListener("input", draw);
    function draw() {
      var o = PR[cur], t = o.a + (o.b - o.a) * (+sl.value) / 100, y = o.f(t), G = plane(-4, 7, -4, 7, 1, 320, 320), h = G.g + G.open;
      h += curve(G, function (x) { return x; }, MU, { dash: "6 5", w: 1.6, n: 20 }) + curve(G, o.f, AC, { n: 1200 }) + curve(G, o.g, GR, { n: 1200 });
      h += '<line class="gd" x1="' + f1(G.X(t)) + '" y1="' + f1(G.Y(y)) + '" x2="' + f1(G.X(y)) + '" y2="' + f1(G.Y(t)) + '"/>' + gdot(G, t, y, AC) + gdot(G, y, t, GR);
      svg.innerHTML = h + G.close;
      info.innerHTML = kv([
        ["", tex(o.n)],
        [t3("1) Canviem f(x) per y", "1) Cambiamos f(x) por y", "1) Replace f(x) with y"), tex(o.st[0])],
        [t3("2) Intercanviem x i y", "2) Intercambiamos x e y", "2) Swap x and y"), tex(o.st[1])],
        [t3("3) Aïllem y", "3) Despejamos y", "3) Solve for y"), tex(o.st[2])],
        [t3("4) Inversa", "4) Inversa", "4) Inverse"), "<strong>" + tex(o.r) + "</strong>"],
        [t3("Punts simètrics", "Puntos simétricos", "Mirror points"), tex("(" + dT(t, 2) + ",\\ " + dT(y, 2) + ")\\leftrightarrow(" + dT(y, 2) + ",\\ " + dT(t, 2) + ")")]
      ]);
    }
    onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("Quin és el domini de $f(x)=\\dfrac{2x-1}{x^2-9}$?", "¿Cuál es el dominio de $f(x)=\\dfrac{2x-1}{x^2-9}$?", "What is the domain of $f(x)=\\dfrac{2x-1}{x^2-9}$?"),
      o: [q3("$\\mathbb R$"), q3("$\\mathbb R-\\{-3,3\\}$"), q3("$\\mathbb R-\\{\\frac12\\}$")], a: 1, e: q3("El denominador s'anul·la en $x=\\pm3$.", "El denominador se anula en $x=\\pm3$.", "The denominator vanishes at $x=\\pm3$.") },
    { q: q3("El domini de $f(x)=\\log_2(x-3)$ és…", "El dominio de $f(x)=\\log_2(x-3)$ es…", "The domain of $f(x)=\\log_2(x-3)$ is…"),
      o: [q3("$[3,+\\infty[$"), q3("$]3,+\\infty[$"), q3("$\\mathbb R$")], a: 1, e: q3("L'argument ha de ser estrictament positiu: $x-3\\gt0$.", "El argumento debe ser estrictamente positivo: $x-3\\gt0$.", "The argument must be strictly positive: $x-3\\gt0$.") },
    { q: q3("On talla $f(x)=x^2-5x+6$ l'eix $OY$?", "¿Dónde corta $f(x)=x^2-5x+6$ el eje $OY$?", "Where does $f(x)=x^2-5x+6$ meet the $y$-axis?"),
      o: [q3("$(0,6)$"), q3("$(6,0)$"), q3("$(2,0)$ i $(3,0)$", "$(2,0)$ y $(3,0)$", "$(2,0)$ and $(3,0)$")], a: 0, e: q3("Fem $x=0$: $f(0)=6$.", "Hacemos $x=0$: $f(0)=6$.", "Set $x=0$: $f(0)=6$.") },
    { q: q3("En un mínim, la funció passa de ser…", "En un mínimo, la función pasa de ser…", "At a minimum the function goes from being…"),
      o: [q3("creixent a decreixent", "creciente a decreciente", "increasing to decreasing"), q3("decreixent a creixent", "decreciente a creciente", "decreasing to increasing"), q3("contínua a discontínua", "continua a discontinua", "continuous to discontinuous")], a: 1, e: q3("La gràfica baixa, arriba al punt més baix de la zona i torna a pujar.", "La gráfica baja, llega al punto más bajo de la zona y vuelve a subir.", "The graph falls, reaches the lowest point nearby and rises again.") },
    { q: q3("Si els dos trossos arriben a la mateixa altura, però falta el punt, la discontinuïtat és…", "Si los dos trozos llegan a la misma altura, pero falta el punto, la discontinuidad es…", "If both pieces reach the same height but the point is missing, the discontinuity is…"),
      o: [q3("evitable", "evitable", "removable"), q3("de salt finit", "de salto finito", "a finite jump"), q3("asimptòtica", "asintótica", "asymptotic")], a: 0, e: q3("Es podria evitar definint la funció en aquest punt.", "Se podría evitar definiendo la función en ese punto.", "It could be removed by defining the function at that point.") },
    { q: q3("La funció $f(x)=x^3-x$ és…", "La función $f(x)=x^3-x$ es…", "The function $f(x)=x^3-x$ is…"),
      o: [q3("parella", "par", "even"), q3("senar", "impar", "odd"), q3("ni parella ni senar", "ni par ni impar", "neither")], a: 1, e: q3("$f(-x)=-x^3+x=-f(x)$.") },
    { q: q3("La gràfica de $y=f(x-3)$ s'obté desplaçant la de $y=f(x)$…", "La gráfica de $y=f(x-3)$ se obtiene desplazando la de $y=f(x)$…", "The graph of $y=f(x-3)$ is the graph of $y=f(x)$ moved…"),
      o: [q3("3 unitats cap a la dreta", "3 unidades hacia la derecha", "3 units to the right"), q3("3 unitats cap a l'esquerra", "3 unidades hacia la izquierda", "3 units to the left"), q3("3 unitats cap avall", "3 unidades hacia abajo", "3 units down")], a: 0, e: q3("El que valia $f$ en $a$ ara ho val en $a+3$: la gràfica va cap a la dreta (signe contrari al que es veu).", "Lo que valía $f$ en $a$ ahora lo vale en $a+3$: la gráfica va hacia la derecha (signo contrario al que se ve).", "What $f$ took at $a$ now happens at $a+3$: the graph moves right (opposite to the sign you see).") },
    { q: q3("Si $f$ té un mínim en $(1,2)$, la funció $y=f(x)+4$ el té en…", "Si $f$ tiene un mínimo en $(1,2)$, la función $y=f(x)+4$ lo tiene en…", "If $f$ has a minimum at $(1,2)$, $y=f(x)+4$ has it at…"),
      o: [q3("$(1,6)$"), q3("$(5,2)$"), q3("$(1,-2)$")], a: 0, e: q3("Sumar 4 puja tota la gràfica 4 unitats; la $x$ no canvia.", "Sumar 4 sube toda la gráfica 4 unidades; la $x$ no cambia.", "Adding 4 lifts the whole graph 4 units; $x$ stays the same.") },
    { q: q3("$y=(x+2)^2-1$ és la paràbola $y=x^2$ desplaçada…", "$y=(x+2)^2-1$ es la parábola $y=x^2$ desplazada…", "$y=(x+2)^2-1$ is $y=x^2$ moved…"),
      o: [q3("2 a la dreta i 1 avall", "2 a la derecha y 1 abajo", "2 right and 1 down"), q3("2 a l'esquerra i 1 avall", "2 a la izquierda y 1 abajo", "2 left and 1 down"), q3("2 a l'esquerra i 1 amunt", "2 a la izquierda y 1 arriba", "2 left and 1 up")], a: 1, e: q3("$x+2=x-(-2)$: 2 cap a l'esquerra; $-1$: 1 cap avall. El vèrtex és $(-2,-1)$.", "$x+2=x-(-2)$: 2 hacia la izquierda; $-1$: 1 hacia abajo. El vértice es $(-2,-1)$.", "$x+2=x-(-2)$: 2 left; $-1$: 1 down. The vertex is $(-2,-1)$.") },
    { q: q3("Si $f(x)=x^2$ i $g(x)=x+1$, $(f\\circ g)(x)$ és…", "Si $f(x)=x^2$ y $g(x)=x+1$, $(f\\circ g)(x)$ es…", "If $f(x)=x^2$ and $g(x)=x+1$, $(f\\circ g)(x)$ is…"),
      o: [q3("$x^2+1$"), q3("$(x+1)^2$"), q3("$x^3+x^2$")], a: 1, e: q3("$f(g(x))=f(x+1)=(x+1)^2$.") },
    { q: q3("La inversa de $f(x)=2x+6$ és…", "La inversa de $f(x)=2x+6$ es…", "The inverse of $f(x)=2x+6$ is…"),
      o: [q3("$\\frac{1}{2x+6}$"), q3("$\\frac{x-6}{2}$"), q3("$-2x-6$")], a: 1, e: q3("$x=2y+6\\Rightarrow y=\\frac{x-6}{2}$.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Estudi de funcions · FentMates", es: "Estudio de funciones · FentMates", en: "Studying functions · FentMates" };
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
    var all = [wChrome, wSteps, wNav, wVert, wDom, wCut, wMono, wDisc, wSym, wPer, wTr, wComp, wInv, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM7 = { parseF: parseF, ev: ev, toT: toT, consOf: consOf, solveSet: solveSet, setT: setT, rootsF: rootsF, niceT: niceT, polyOf: polyOf, polyT: polyT, sub: sub };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
