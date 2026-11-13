(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1batx-mi-u9-derivades-done";

  // Els textos (UI) es completen després de carregar els mòduls: el nucli comú fa servir u(), amb els textos de tots tres.
  var UI = { va: {}, es: {}, en: {} };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  function t3(va, es, en) { return lang === "es" ? es : lang === "en" ? en : va; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }

  /* ===================== nucli comú (unitat 4 de CCSS) + derivació simbòlica (unitat 5) + estudi (unitat 6) ===================== */
  /* ---------- fraccions exactes ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; }
  function Fr(n, d) { if (d === undefined) d = 1; if (d < 0) { n = -n; d = -d; } var g = gcd(n, d); this.n = n / g; this.d = d / g; }
  Fr.prototype.add = function (o) { return new Fr(this.n * o.d + o.n * this.d, this.d * o.d); };
  Fr.prototype.sub = function (o) { return new Fr(this.n * o.d - o.n * this.d, this.d * o.d); };
  Fr.prototype.mul = function (o) { return new Fr(this.n * o.n, this.d * o.d); };
  Fr.prototype.div = function (o) { return new Fr(this.n * o.d, this.d * o.n); };
  Fr.prototype.zero = function () { return this.n === 0; };
  Fr.prototype.val = function () { return this.n / this.d; };
  Fr.prototype.tex = function () { if (this.d === 1) return String(this.n); return (this.n < 0 ? "-" : "") + "\\frac{" + Math.abs(this.n) + "}{" + this.d + "}"; };
  Fr.prototype.txt = function () { return (this.d === 1 ? String(this.n) : this.n + "/" + this.d).replace(/-/g, "−"); };
  function decFr(s) { var p = s.split("."), k = p[1] ? p[1].length : 0, f = Math.pow(10, k); return new Fr(Math.round(parseFloat(s) * f), f); }
  function parseFr(s) {
    s = String(s).trim().replace(/,/g, ".").replace(/−/g, "-");
    var m = s.match(/^(-?\d*\.?\d+)(?:\/(-?\d*\.?\d+))?$/);
    if (!m) return null;
    var a = decFr(m[1]); if (!m[2]) return a;
    var b = decFr(m[2]); return b.zero() ? null : a.div(b);
  }

  /* ---------- nombres ---------- */
  function decTex(s) { return lang === "en" ? s : s.replace(".", "{,}"); }
  function numTex(v) {
    if (v !== v) return "\\nexists";
    if (v === Infinity) return "+\\infty";
    if (v === -Infinity) return "-\\infty";
    if (v === 0) return "0";
    var a = Math.abs(v);
    if (a >= 1e6 || a < 1e-4) {
      var e = Math.floor(Math.log10(a)), m = +(v / Math.pow(10, e)).toFixed(3);
      if (Math.abs(m) >= 10) { m = +(m / 10).toFixed(3); e++; }
      return decTex(String(m)) + "\\cdot10^{" + e + "}";
    }
    return decTex(String(+v.toPrecision(7)));
  }
  function numTxt(v) {
    if (v !== v) return "∄";
    if (v === Infinity) return "+∞";
    if (v === -Infinity) return "−∞";
    var s = String(+v.toPrecision(6));
    if (/e/.test(s)) s = v.toExponential(3);
    return (lang === "en" ? s : s.replace(".", ",")).replace(/^-/, "−");
  }
  // reconeix fraccions senzilles i potències de e
  function fracOf(v, maxD) {
    for (var d = 1; d <= maxD; d++) { var n = Math.round(v * d); if (Math.abs(n / d - v) < 1e-7 * Math.max(1, Math.abs(v))) return new Fr(n, d); }
    return null;
  }
  function niceTex(v) {
    if (v !== v || !isFinite(v)) return numTex(v);
    if (Math.abs(v) < 5e-7) return "0";
    var f = fracOf(v, 60);
    var sv = String(+v.toFixed(6));
    if (f && (f.d <= 12 || !/^-?\d+\.\d{1,3}$/.test(sv))) return f.tex();
    if (f) return decTex(sv);
    if (v > 0) { var r = fracOf(Math.log(v), 6); if (r && Math.abs(r.n) <= 40) return r.n === 1 && r.d === 1 ? "e" : "e^{" + r.tex() + "}"; }
    var q = fracOf(v * v, 60);
    if (q && q.d === 1) return (v < 0 ? "-" : "") + "\\sqrt{" + q.n + "}";
    return "\\approx" + decTex(String(+v.toPrecision(6)));
  }

  /* ---------- lectura d'expressions ---------- */
  var NAMES = ["arcsin", "arccos", "arctan", "sqrt", "exp", "abs", "log", "sin", "cos", "tan", "ln", "pi", "x", "t", "a", "b", "e"];
  var FUNCS = { sqrt: 1, exp: 1, abs: 1, log: 1, sin: 1, cos: 1, tan: 1, arcsin: 1, arccos: 1, arctan: 1, ln: 1 };
  function tokenize(src) {
    var s = String(src).replace(/\s+/g, "").replace(/,/g, ".").replace(/[−–]/g, "-").replace(/[·×]/g, "*").replace(/\*\*/g, "^").replace(/√/g, "sqrt").replace(/²/g, "^2").replace(/³/g, "^3").replace(/π/g, "pi").toLowerCase();
    var out = [], i = 0, m;
    while (i < s.length) {
      var r = s.slice(i);
      if ((m = r.match(/^(\d+\.?\d*|\.\d+)/))) { out.push({ k: "n", v: m[1] }); i += m[1].length; continue; }
      if (/^[a-z]/.test(r)) {
        var hit = null;
        for (var j = 0; j < NAMES.length; j++) if (r.indexOf(NAMES[j]) === 0) { hit = NAMES[j]; break; }
        if (!hit) throw new Error("name");
        out.push({ k: FUNCS[hit] ? "f" : "v", v: hit }); i += hit.length; continue;
      }
      if ("+-*/^()".indexOf(r[0]) >= 0) { out.push({ k: r[0] }); i++; continue; }
      throw new Error("char");
    }
    return out;
  }
  function parse(src) {
    var T = tokenize(src), p = 0;
    if (!T.length) throw new Error("empty");
    function peek() { return T[p] || { k: "end" }; }
    function eat(k) { if (peek().k !== k) throw new Error("expected " + k); p++; }
    function expr() {
      var a = term();
      while (peek().k === "+" || peek().k === "-") { var o = T[p++].k; a = { t: o, a: a, b: term() }; }
      return a;
    }
    function term() {
      var a = unary();
      for (;;) {
        var k = peek().k;
        if (k === "*" || k === "/") { p++; a = { t: k, a: a, b: unary() }; }
        else if (k === "n" || k === "v" || k === "f" || k === "(") a = { t: "*", a: a, b: power(), imp: true };
        else return a;
      }
    }
    function unary() {
      if (peek().k === "-") { p++; return { t: "neg", a: unary() }; }
      if (peek().k === "+") { p++; return unary(); }
      return power();
    }
    function power() {
      var a = atom();
      if (peek().k === "^") { p++; return { t: "^", a: a, b: unary() }; }
      return a;
    }
    function atom() {
      var k = peek();
      if (k.k === "n") { p++; return { t: "n", v: parseFloat(k.v), s: k.v }; }
      if (k.k === "v") { p++; return k.v === "e" || k.v === "pi" ? { t: "c", n: k.v } : { t: "v", n: k.v }; }
      if (k.k === "f") { p++; var arg = peek().k === "(" ? atom() : power(); return { t: "f", n: k.v, a: arg }; }
      if (k.k === "(") { p++; var e = expr(); eat(")"); return { t: "()", a: e }; }
      throw new Error("atom");
    }
    var r = expr();
    if (p < T.length) throw new Error("trailing");
    return r;
  }
  function strip(n) { while (n.t === "()") n = n.a; return n; }
  var FN = { sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, log: function (v) { return v > 0 ? Math.log10(v) : NaN; }, ln: function (v) { return v > 0 ? Math.log(v) : NaN; }, sin: Math.sin, cos: Math.cos, tan: Math.tan, arcsin: Math.asin, arccos: Math.acos, arctan: Math.atan };
  function compile(ast) {
    function ev(n, x, env) {
      switch (n.t) {
        case "n": return n.v;
        case "c": return n.n === "e" ? Math.E : Math.PI;
        case "v": return n.n === "x" || n.n === "t" ? x : (env && env[n.n] !== undefined ? env[n.n] : NaN);
        case "()": return ev(n.a, x, env);
        case "neg": return -ev(n.a, x, env);
        case "+": return ev(n.a, x, env) + ev(n.b, x, env);
        case "-": return ev(n.a, x, env) - ev(n.b, x, env);
        case "*": return ev(n.a, x, env) * ev(n.b, x, env);
        case "/": return ev(n.a, x, env) / ev(n.b, x, env);
        case "^": {
          var b = ev(n.a, x, env), e = ev(n.b, x, env);
          if (b < 0 && e !== Math.round(e)) { var q = fracOf(e, 9); if (q && q.d % 2 === 1) return (q.n % 2 ? -1 : 1) * Math.pow(-b, e); }
          return Math.pow(b, e);
        }
        case "f": return FN[n.n](ev(n.a, x, env));
      }
      return NaN;
    }
    return function (x, env) { var v = ev(ast, x, env); return v === v ? v : NaN; };
  }
  function fnOf(src) { var a = parse(src); return compile(a); }

  // TeX d'una expressió
  var PREC = { "+": 1, "-": 1, "*": 2, "/": 2, neg: 2, "^": 4 };
  function texA(n) {
    switch (n.t) {
      case "n": return decTex(n.s);
      case "c": return n.n === "e" ? "e" : "\\pi";
      case "v": return n.n;
      case "()": return texA(strip(n.a));
      case "neg": { var a = strip(n.a); var s = texA(a); return "-" + ((a.t === "+" || a.t === "-" || a.t === "neg") ? "\\left(" + s + "\\right)" : s); }
      case "+": return texA(n.a) + "+" + texA(n.b);
      case "-": { var b = strip(n.b); var sb = texA(b); return texA(n.a) + "-" + ((b.t === "+" || b.t === "-" || b.t === "neg") ? "\\left(" + sb + "\\right)" : sb); }
      case "*": {
        var l = strip(n.a), r = strip(n.b), tl = texA(l), tr = texA(r);
        if (l.t === "+" || l.t === "-") tl = "\\left(" + tl + "\\right)";
        if (r.t === "+" || r.t === "-" || r.t === "neg") tr = "\\left(" + tr + "\\right)";
        var dot = (r.t === "n" || (r.t === "^" && strip(r.a).t === "n") || (l.t === "n" && r.t === "n")) ? "\\cdot " : (/^[0-9{]/.test(tr) ? "\\cdot " : "\\,");
        if (l.t === "n" && (r.t === "v" || r.t === "f" || r.t === "c" || (r.t === "^" && strip(r.a).t !== "n") || r.t === "()" )) dot = "";
        if (n.imp && dot === "\\,") dot = "";
        return tl + dot + tr;
      }
      case "/": return "\\dfrac{" + texA(strip(n.a)) + "}{" + texA(strip(n.b)) + "}";
      case "^": {
        var base = strip(n.a), tb = texA(base);
        if (base.t !== "n" && base.t !== "v" && base.t !== "c") tb = "\\left(" + tb + "\\right)";
        return tb + "^{" + texA(strip(n.b)) + "}";
      }
      case "f": {
        var arg = texA(strip(n.a));
        if (n.n === "sqrt") return "\\sqrt{" + arg + "}";
        if (n.n === "abs") return "\\left|" + arg + "\\right|";
        if (n.n === "exp") return "e^{" + arg + "}";
        return "\\" + (n.n === "ln" ? "ln" : n.n) + "\\left(" + arg + "\\right)";
      }
    }
    return "?";
  }
  function texOf(src) { try { return texA(strip(parse(src))); } catch (e) { return "?"; } }

  /* ---------- polinomis amb coeficients fraccionaris ---------- */
  function pTrim(p) { p = p.slice(); while (p.length > 1 && p[p.length - 1].zero()) p.pop(); return p; }
  function pAdd(p, q, s) { var r = []; for (var i = 0; i < Math.max(p.length, q.length); i++) { var a = p[i] || new Fr(0), b = q[i] || new Fr(0); r.push(s < 0 ? a.sub(b) : a.add(b)); } return pTrim(r); }
  function pMul(p, q) { var r = []; for (var i = 0; i < p.length + q.length - 1; i++) r.push(new Fr(0)); p.forEach(function (a, i) { q.forEach(function (b, j) { r[i + j] = r[i + j].add(a.mul(b)); }); }); return pTrim(r); }
  function polyOf(n) {
    switch (n.t) {
      case "n": return [decFr(n.s)];
      case "v": if (n.n === "x") return [new Fr(0), new Fr(1)]; throw new Error("var");
      case "()": return polyOf(n.a);
      case "neg": return polyOf(n.a).map(function (c) { return new Fr(-c.n, c.d); });
      case "+": return pAdd(polyOf(n.a), polyOf(n.b), 1);
      case "-": return pAdd(polyOf(n.a), polyOf(n.b), -1);
      case "*": return pMul(polyOf(n.a), polyOf(n.b));
      case "/": { var d = pTrim(polyOf(n.b)); if (d.length > 1 || d[0].zero()) throw new Error("div"); return polyOf(n.a).map(function (c) { return c.div(d[0]); }); }
      case "^": {
        var e = strip(n.b); if (e.t !== "n" || !/^\d+$/.test(e.s) || +e.s > 20) throw new Error("pow");
        var b = polyOf(n.a), r = [new Fr(1)]; for (var i = 0; i < +e.s; i++) r = pMul(r, b); return r;
      }
    }
    throw new Error("poly");
  }
  function polyParse(src) { return pTrim(polyOf(parse(src))); }
  function pDeg(p) { return pTrim(p).length - 1; }
  function pEval(p, a) { var r = new Fr(0); for (var i = p.length - 1; i >= 0; i--) r = r.mul(a).add(p[i]); return r; }
  function monoTex(c, k, first) {
    if (c.zero()) return "";
    var neg = c.n < 0, ab = new Fr(Math.abs(c.n), c.d), cs = (k > 0 && ab.n === 1 && ab.d === 1) ? "" : ab.tex();
    var xs = k === 0 ? "" : k === 1 ? "x" : "x^{" + k + "}";
    return (neg ? "-" : first ? "" : "+") + cs + xs;
  }
  function pTex(p) {
    var s = "", first = true;
    for (var k = p.length - 1; k >= 0; k--) { var m = monoTex(p[k], k, first); if (m) { s += m; first = false; } }
    return s || "0";
  }
  function ruffini(p, a) { // p: coeficients de grau 0..n; divideix per (x − a)
    var c = p.slice().reverse(), row = [null], res = [c[0]];
    for (var i = 1; i < c.length; i++) { var m = res[i - 1].mul(a); row.push(m); res.push(c[i].add(m)); }
    var r = res.pop();
    return { q: res.slice().reverse(), r: r, top: c, mid: row, bot: res.concat([r]) };
  }
  function ruffHtml(R, a) {
    function td(x, cls) { return "<td" + (cls ? ' class="' + cls + '"' : "") + ">" + (x ? x.txt() : "") + "</td>"; }
    var t = "<tr><td></td>" + R.top.map(function (x) { return td(x); }).join("") + "</tr>";
    t += "<tr>" + td(a) + R.mid.map(function (x) { return td(x); }).join("") + "</tr>";
    t += "<tr><td></td>" + R.bot.map(function (x, i) { return td(x, i === R.bot.length - 1 ? "rz" : ""); }).join("") + "</tr>";
    return '<table class="rf">' + t + "</table>";
  }

  /* ---------- estimació numèrica de límits ---------- */
  // side: -1 (esquerra) o +1 (dreta); a pot ser ±Infinity
  function samples(f, a, side) {
    var out = [];
    for (var k = 1; k <= 8; k++) {
      var x = isFinite(a) ? a + side * Math.pow(10, -k) : (a > 0 ? 1 : -1) * Math.pow(10, k);
      out.push({ x: x, y: f(x) });
    }
    if (isFinite(a)) return out;
    // si les exponencials desborden aviat, anem doblant x fins on es pot calcular
    var ok = 0; while (ok < out.length && isFinite(out[ok].y)) ok++;
    if (ok >= 5) return out;
    var d = [];
    for (var x2 = 10; x2 < 1e9; x2 *= 2) {
      var y = f((a > 0 ? 1 : -1) * x2); d.push({ x: x2, y: y });
      if (!isFinite(y)) { if (y !== y) d.pop(); break; }
    }
    return d.length >= 5 ? d : out;
  }
  function analyse(S) {
    var v = S.map(function (s) { return s.y; });
    var tail = v.slice(4);
    if (tail.every(function (y) { return y !== y; })) return { k: "none" };
    var last = v[v.length - 1];
    if (last === Infinity || last === -Infinity) return { k: "inf", s: last > 0 ? 1 : -1 };
    var fin = v.filter(function (y) { return isFinite(y); });
    if (fin.length < 5) return { k: "none" };
    var w = fin.slice(-5), d = [];
    for (var i = 1; i < w.length; i++) d.push(w[i] - w[i - 1]);
    var sameSign = d.every(function (x) { return x > 0; }) || d.every(function (x) { return x < 0; });
    var notShrinking = Math.abs(d[3]) >= 0.5 * Math.abs(d[2]) && Math.abs(d[2]) >= 0.5 * Math.abs(d[1]);
    if (sameSign && notShrinking && Math.abs(d[3]) > 1e-9 * (1 + Math.abs(w[4]))) return { k: "inf", s: d[3] > 0 ? 1 : -1 };
    var best = null;
    for (var j = 2; j < fin.length; j++) {
      var dd = Math.abs(fin[j] - fin[j - 1]);
      if (best === null || dd < best.d) best = { d: dd, v: fin[j] };
    }
    if (best.d <= 1e-5 * Math.max(1, Math.abs(best.v))) return { k: "num", v: best.v };
    var shrink = Math.abs(d[3]) < 0.6 * Math.abs(d[2]) && Math.abs(d[2]) < 0.6 * Math.abs(d[1]);
    if (shrink) return { k: "num", v: w[4], approx: true };
    return { k: "osc" };
  }
  function limSide(f, a, side) { return analyse(samples(f, a, side)); }
  function limVal(r) { return r.k === "num" ? (Math.abs(r.v) < 5e-7 ? 0 : r.v) : r.k === "inf" ? r.s * Infinity : NaN; }
  function limTex(r) {
    if (r.k === "num") return niceTex(r.v);
    if (r.k === "inf") return r.s > 0 ? "+\\infty" : "-\\infty";
    return "\\nexists";
  }
  function sameLim(p, q) {
    if (p.k === "num" && q.k === "num") return Math.abs(p.v - q.v) <= 1e-5 * Math.max(1, Math.abs(p.v));
    return p.k === "inf" && q.k === "inf" && p.s === q.s;
  }
  // valor exacte quan es pot (polinomis, etc.), si no, estimació
  function sideAt(f, c, side) {
    var y = f(c);
    if (isFinite(y)) { var y2 = f(c + side * 1e-7); if (isFinite(y2) && Math.abs(y2 - y) < 1e-4 * (1 + Math.abs(y))) return { k: "num", v: y }; }
    return limSide(f, c, side);
  }
  // tipus de discontinuïtat a partir dels laterals i f(a)
  function classify(L, R, fa) {
    var fin = function (r) { return r.k === "num"; };
    if (fin(L) && fin(R) && sameLim(L, R)) return (fa === fa && isFinite(fa) && Math.abs(fa - L.v) <= 1e-5 * Math.max(1, Math.abs(fa))) ? "ok" : "ev";
    if (fin(L) && fin(R)) return "sf";
    var iL = L.k === "inf", iR = R.k === "inf";
    if (iL && iR) return "as";
    if ((iL && fin(R)) || (iR && fin(L))) return "si";
    if (fin(L) || fin(R)) return "si";
    return "as";
  }
  var BADGE = { ok: ["ok", "cont"], ev: ["ev", "ev"], sf: ["sf", "sf"], si: ["si", "si"], as: ["as", "as"] };
  function badge(c) { return '<span class="badge ' + BADGE[c][0] + '">' + u(BADGE[c][1]) + "</span>"; }

  /* ---------- dibuix de gràfiques ---------- */
  var W = 420, H = 300, ML = 30, MR = 10, MT = 10, MB = 22;
  var COLS = ["var(--accent)", "var(--accent-2)", "var(--r3)", "var(--plus)", "var(--r4)"];
  function niceStep(r) { var e = Math.pow(10, Math.floor(Math.log10(r / 6))), m = r / 6 / e; return e * (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10); }
  function numLab(x) { var s = String(+x.toFixed(6)); return (lang === "en" ? s : s.replace(".", ",")).replace("-", "−"); }
  var clipN = 0;
  /* cfg: {v:[x0,x1,y0,y1], curves:[{f,a,b,col}], va:[], ha:[], pts:[{x,y,o,col}], guides:[{x,y}], mark:[{x,y,col}], ticks:[{x,t}]} */
  function plot(svg, cfg) {
    var v = cfg.v, x0 = v[0], x1 = v[1], y0 = v[2], y1 = v[3];
    var sx = (W - ML - MR) / (x1 - x0), sy = (H - MT - MB) / (y1 - y0);
    function X(x) { return +(ML + (x - x0) * sx).toFixed(2); }
    function Y(y) { return +(H - MB - (y - y0) * sy).toFixed(2); }
    var g = "", id = "lc" + (++clipN);
    g += '<defs><clipPath id="' + id + '"><rect x="' + ML + '" y="' + MT + '" width="' + (W - ML - MR) + '" height="' + (H - MT - MB) + '"/></clipPath></defs>';
    var st = niceStep(x1 - x0), sty = niceStep(y1 - y0), t;
    for (t = Math.ceil(x0 / st) * st; t <= x1 + 1e-9; t += st) g += '<line class="g" x1="' + X(t) + '" y1="' + MT + '" x2="' + X(t) + '" y2="' + (H - MB) + '"/>';
    for (t = Math.ceil(y0 / sty) * sty; t <= y1 + 1e-9; t += sty) g += '<line class="g" x1="' + ML + '" y1="' + Y(t) + '" x2="' + (W - MR) + '" y2="' + Y(t) + '"/>';
    var ay = Math.min(Math.max(0, y0), y1), ax = Math.min(Math.max(0, x0), x1);
    g += '<line class="ax" x1="' + ML + '" y1="' + Y(ay) + '" x2="' + (W - MR) + '" y2="' + Y(ay) + '"/><line class="ax" x1="' + X(ax) + '" y1="' + MT + '" x2="' + X(ax) + '" y2="' + (H - MB) + '"/>';
    for (t = Math.ceil(x0 / st) * st; t <= x1 + 1e-9; t += st) if (Math.abs(t) > 1e-9) g += '<text x="' + X(t) + '" y="' + (H - 6) + '" text-anchor="middle">' + numLab(t) + "</text>";
    for (t = Math.ceil(y0 / sty) * sty; t <= y1 + 1e-9; t += sty) if (Math.abs(t) > 1e-9) g += '<text x="' + (ML - 4) + '" y="' + (Y(t) + 3.5) + '" text-anchor="end">' + numLab(t) + "</text>";
    var body = "";
    (cfg.band || []).forEach(function (q) { var a = Math.max(q.a, x0), b = Math.min(q.b, x1); if (b > a) body += '<rect class="' + (q.cls || "nodom") + '" x="' + X(a) + '" y="' + MT + '" width="' + (X(b) - X(a)).toFixed(2) + '" height="' + (H - MT - MB) + '"/>'; });
    (cfg.ha || []).forEach(function (y) { body += '<line class="asy" x1="' + ML + '" y1="' + Y(y) + '" x2="' + (W - MR) + '" y2="' + Y(y) + '"/>'; });
    (cfg.va || []).forEach(function (x) { body += '<line class="asy" x1="' + X(x) + '" y1="' + MT + '" x2="' + X(x) + '" y2="' + (H - MB) + '"/>'; });
    (cfg.oa || []).forEach(function (q) { body += '<line class="asy" x1="' + X(x0) + '" y1="' + Y(q.m * x0 + q.n) + '" x2="' + X(x1) + '" y2="' + Y(q.m * x1 + q.n) + '"/>'; });
    (cfg.guides || []).forEach(function (q) {
      if (q.x !== undefined) body += '<line class="gd" x1="' + X(q.x) + '" y1="' + MT + '" x2="' + X(q.x) + '" y2="' + (H - MB) + '"/>';
      if (q.y !== undefined && isFinite(q.y)) body += '<line class="gd" x1="' + ML + '" y1="' + Y(q.y) + '" x2="' + (W - MR) + '" y2="' + Y(q.y) + '"/>';
    });
    var lim = (y1 - y0) * 4;
    (cfg.curves || []).forEach(function (c, ci) {
      var a = Math.max(c.a === undefined ? -Infinity : c.a, x0), b = Math.min(c.b === undefined ? Infinity : c.b, x1);
      if (!(b > a)) return;
      var N = 700, d = "", pen = false, prevY = null, eps = (b - a) * 1e-6;
      for (var i = 0; i <= N; i++) {
        var x = a + (b - a) * i / N;
        if (i === 0) x += eps; if (i === N) x -= eps;
        var y = c.f(x);
        if (!isFinite(y) || y < y0 - lim || y > y1 + lim) { pen = false; prevY = null; continue; }
        if (prevY !== null && Math.abs(y - prevY) > (y1 - y0) * 1.5) pen = false;
        d += (pen ? "L" : "M") + X(x) + "," + Y(y); pen = true; prevY = y;
      }
      body += '<path class="cv" d="' + d + '" style="stroke:' + (c.col || COLS[ci % COLS.length]) + '"/>';
    });
    (cfg.mark || []).forEach(function (q) {
      if (q.x < x0 || q.x > x1 || !isFinite(q.y) || q.y < y0 || q.y > y1) return;
      body += '<circle class="mk" cx="' + X(q.x) + '" cy="' + Y(q.y) + '" r="6" style="fill:' + (q.col || "var(--text)") + '"/>';
    });
    (cfg.pts || []).forEach(function (q) {
      if (!isFinite(q.y) || q.y < y0 - 1e-9 || q.y > y1 + 1e-9) return;
      var col = q.col || COLS[0];
      body += q.o ? '<circle class="open" cx="' + X(q.x) + '" cy="' + Y(q.y) + '" r="4.5" style="stroke:' + col + '"/>'
        : '<circle cx="' + X(q.x) + '" cy="' + Y(q.y) + '" r="4.5" style="fill:' + col + '"/>';
    });
    (cfg.labels || []).forEach(function (q) { body += '<text class="vl" x="' + X(q.x) + '" y="' + Y(q.y) + '" text-anchor="' + (q.anchor || "middle") + '">' + q.t + "</text>"; });
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    svg.innerHTML = g + '<g clip-path="url(#' + id + ')">' + body + "</g>";
  }

  /* ---------- funcions a trossos ---------- */
  // def: {p:[expr...], c:[talls], inc:["L"|"R"], dom:[lo,hi], din:[bool,bool], at:{x:valor}}
  function pwMake(def, env) {
    var fs = def.p.map(function (e) { return compile(parse(e)); });
    var c = def.c || [], inc = def.inc || c.map(function () { return "R"; });
    var dom = def.dom || [-Infinity, Infinity], din = def.din || [true, true];
    function idx(x) {
      for (var k = 0; k < c.length; k++) { if (x < c[k]) return k; if (x === c[k]) return inc[k] === "L" ? k : k + 1; }
      return c.length;
    }
    function inDom(x) { return (x > dom[0] || (x === dom[0] && din[0])) && (x < dom[1] || (x === dom[1] && din[1])); }
    function f(x) {
      if (!inDom(x)) return NaN;
      if (def.at && def.at[x] !== undefined) return def.at[x];
      return fs[idx(x)](x, env);
    }
    function piece(i) { return function (x) { return fs[i](x, env); }; }
    function bounds(i) { return [i === 0 ? dom[0] : c[i - 1], i === c.length ? dom[1] : c[i]]; }
    return { f: f, fs: fs, piece: piece, bounds: bounds, c: c, inc: inc, dom: dom, din: din, n: fs.length, env: env };
  }
  // corbes i punts (plens/buits) per al dibuix
  function pwDraw(P, view, cols) {
    var curves = [], pts = [];
    for (var i = 0; i < P.n; i++) { var B = P.bounds(i); curves.push({ f: P.piece(i), a: B[0], b: B[1], col: (cols || [])[i] || COLS[0] }); }
    P.c.forEach(function (c, k) {
      var L = sideAt(P.piece(k), c, -1), R = sideAt(P.piece(k + 1), c, 1), fc = P.f(c);
      var col = COLS[0];
      if (L.k === "num" && R.k === "num" && sameLim(L, R) && Math.abs(fc - L.v) < 1e-6 * (1 + Math.abs(fc))) return;
      if (isFinite(fc)) pts.push({ x: c, y: fc, col: col });
      if (L.k === "num" && !(isFinite(fc) && Math.abs(fc - L.v) < 1e-9 * (1 + Math.abs(fc)))) pts.push({ x: c, y: L.v, o: true, col: col });
      if (R.k === "num" && !(isFinite(fc) && Math.abs(fc - R.v) < 1e-9 * (1 + Math.abs(fc)))) pts.push({ x: c, y: R.v, o: true, col: col });
    });
    [0, 1].forEach(function (s) {
      var x = P.dom[s]; if (!isFinite(x) || x < view[0] || x > view[1]) return;
      var y = P.piece(s ? P.n - 1 : 0)(x);
      if (isFinite(y)) pts.push({ x: x, y: y, o: !P.din[s] });
    });
    return { curves: curves, pts: pts };
  }
  function condTex(lo, loIn, hi, hiIn) {
    var L = isFinite(lo), R = isFinite(hi);
    if (L && R) return numTex(lo) + (loIn ? "\\leq " : "\\lt ") + "x" + (hiIn ? "\\leq " : "\\lt ") + numTex(hi);
    if (L) return "x" + (loIn ? "\\geq " : "\\gt ") + numTex(lo);
    if (R) return "x" + (hiIn ? "\\leq " : "\\lt ") + numTex(hi);
    return "x\\in\\mathbb R";
  }
  function pwTex(def, name) {
    var c = def.c || [], inc = def.inc || c.map(function () { return "R"; }), dom = def.dom || [-Infinity, Infinity], din = def.din || [true, true];
    var rows = def.p.map(function (e, i) {
      var lo = i === 0 ? dom[0] : c[i - 1], hi = i === c.length ? dom[1] : c[i];
      var loIn = i === 0 ? din[0] : inc[i - 1] === "R", hiIn = i === c.length ? din[1] : inc[i] === "L";
      return texOf(e) + "&\\text{" + u("pc") + " }" + condTex(lo, loIn, hi, hiIn);
    });
    return (name || "f(x)") + "=\\begin{cases}" + rows.join("\\\\[3pt]") + "\\end{cases}";
  }
  function autoY(fs, x0, x1, pad) {
    var ys = [];
    fs.forEach(function (f) { for (var i = 0; i <= 200; i++) { var y = f(x0 + (x1 - x0) * i / 200); if (isFinite(y)) ys.push(y); } });
    if (!ys.length) return [-5, 5];
    ys.sort(function (a, b) { return a - b; });
    var lo = ys[Math.floor(ys.length * 0.04)], hi = ys[Math.ceil(ys.length * 0.96) - 1];
    if (hi - lo < 1e-9) { lo -= 1; hi += 1; }
    var m = (hi - lo) * (pad || 0.15);
    return [Math.min(lo - m, -0.5), Math.max(hi + m, 0.5)];
  }

  /* ---------- derivació simbòlica ---------- */
  function strip0(n) { while (n.t === "()") n = n.a; return n; }
  function num(v) { return v < 0 ? { t: "neg", a: num(-v) } : { t: "n", v: v, s: String(v) }; }
  var ZERO = num(0), ONE = num(1);
  function frNode(f) {
    if (f.n < 0) return { t: "neg", a: frNode(new Fr(-f.n, f.d)) };
    if (f.d > 1 && /^10*$/.test(String(f.d))) return num(+(f.n / f.d).toFixed(String(f.d).length - 1)); // decimals de l'enunciat
    return f.d === 1 ? num(f.n) : { t: "/", a: num(f.n), b: num(f.d) };
  }
  // valor racional d'una expressió constant (o null)
  function cst(n) {
    n = strip0(n);
    switch (n.t) {
      case "n": return decFr(n.s);
      case "neg": { var a = cst(n.a); return a && new Fr(-a.n, a.d); }
      case "+": case "-": case "*": case "/": {
        var p = cst(n.a), q = cst(n.b); if (!p || !q) return null;
        if (n.t === "+") return p.add(q); if (n.t === "-") return p.sub(q); if (n.t === "*") return p.mul(q);
        return q.zero() ? null : p.div(q);
      }
      case "^": {
        var b = cst(n.a), e = cst(n.b); if (!b || !e || e.d !== 1 || Math.abs(e.n) > 12) return null;
        if (b.zero() && e.n <= 0) return null;
        var r = new Fr(1); for (var i = 0; i < Math.abs(e.n); i++) r = r.mul(b);
        return e.n < 0 ? new Fr(1).div(r) : r;
      }
    }
    return null;
  }
  function isN(n, v) { var c = cst(n); return !!c && c.n === v && c.d === 1; }
  function indep(n) {
    if (!n || typeof n !== "object") return true;
    if (n.t === "v") return n.n !== "x" && n.n !== "t";
    return indep(n.a) && indep(n.b);
  }
  function B(t, a, b) { return { t: t, a: a, b: b }; }
  function Fn(name, a) { return { t: "f", n: name, a: a }; }
  function simp(n) {
    n = strip0(n);
    if (n.t === "n" || n.t === "v" || n.t === "c") return n;
    if (n.t === "f") return Fn(n.n, simp(n.a));
    var a = n.a ? simp(n.a) : null, b = n.b ? simp(n.b) : null;
    var m = { t: n.t, a: a, b: b };
    if (n.t !== "neg" && a && b && cst(a) && cst(b) && (n.t !== "^" || cst(m))) { var c = cst(m); if (c) return frNode(c); }
    switch (n.t) {
      case "neg":
        if (a.t === "neg") return a.a;
        if (isN(a, 0)) return ZERO;
        return { t: "neg", a: a };
      case "+":
        if (isN(a, 0)) return b; if (isN(b, 0)) return a;
        if (b.t === "neg") return simp(B("-", a, b.a));
        if (a.t === "neg") return simp(B("-", b, a.a));
        return m;
      case "-":
        if (isN(b, 0)) return a; if (isN(a, 0)) return simp({ t: "neg", a: b });
        if (b.t === "neg") return simp(B("+", a, b.a));
        return m;
      case "*": case "/":
        if (isN(a, 0)) return ZERO;
        if (n.t === "*" && isN(b, 0)) return ZERO;
        return prodNorm(m);
      case "^":
        if (isN(b, 0)) return ONE; if (isN(b, 1)) return a; if (isN(a, 1)) return ONE;
        var e = cst(b);
        if (e && e.n === 1 && e.d === 2) return Fn("sqrt", a);
        if (e && e.n < 0) return simp(B("/", ONE, B("^", a, frNode(new Fr(-e.n, e.d)))));
        if (a.t === "^" && cst(a.b) && e) return simp(B("^", a.a, frNode(cst(a.b).mul(e))));
        if (a.t === "f" && a.n === "sqrt" && e) return simp(B("^", a.a, frNode(e.mul(new Fr(1, 2)))));
        return m;
    }
    return m;
  }
  // productes i quocients: ajuntem constants i potències de la mateixa base i simplifiquem factors comuns
  function mkPow(b, k) {
    if (k.n === k.d) return b;
    if (k.n === 1 && k.d === 2) return Fn("sqrt", b);
    return B("^", b, frNode(k));
  }
  function rank(b) { b = strip0(b); return b.t === "v" ? 0 : (b.t === "+" || b.t === "-") ? 1 : b.t === "f" ? 3 : 2; }
  function prodNorm(n) {
    var c = new Fr(1), fs = [];
    (function col(m, e) {
      m = strip0(m);
      if (m.t === "*") { col(m.a, e); col(m.b, e); return; }
      if (m.t === "/") { col(m.a, e); col(m.b, -e); return; }
      if (m.t === "neg") { c = new Fr(-c.n, c.d); col(m.a, e); return; }
      var k = cst(m);
      if (k) { c = e > 0 ? c.mul(k) : c.div(k); return; }
      var base = m, ex = new Fr(e);
      if (m.t === "^" && cst(m.b)) { base = strip0(m.a); ex = cst(m.b).mul(new Fr(e)); }
      var key = texD(base), hit = null;
      fs.forEach(function (f) { if (f.key === key) hit = f; });
      if (hit) hit.k = hit.k.add(ex); else fs.push({ key: key, b: base, k: ex });
    })(n, 1);
    if (c.zero()) return ZERO;
    fs = fs.filter(function (f) { return !f.k.zero(); });
    fs.sort(function (p, q) { return rank(p.b) - rank(q.b); });
    function build(list, k0) {
      var out = k0 === 1 ? null : num(k0);
      list.forEach(function (f) { out = out ? B("*", out, f) : f; });
      return out || ONE;
    }
    var up = fs.filter(function (f) { return f.k.n > 0; }).map(function (f) { return mkPow(f.b, f.k); });
    var dn = fs.filter(function (f) { return f.k.n < 0; }).map(function (f) { return mkPow(f.b, new Fr(-f.k.n, f.k.d)); });
    var r = build(up, Math.abs(c.n));
    if (dn.length || c.d !== 1) r = B("/", r, build(dn, c.d));
    return c.n < 0 ? { t: "neg", a: r } : r;
  }
  // si una expressió és un polinomi de grau petit, l'escrivim desenvolupat i ordenat
  function polyNode(p) {
    var out = null;
    for (var k = p.length - 1; k >= 0; k--) {
      var c = p[k]; if (c.zero()) continue;
      var ab = new Fr(Math.abs(c.n), c.d), xk = k === 0 ? null : k === 1 ? { t: "v", n: "x" } : B("^", { t: "v", n: "x" }, num(k));
      var t = !xk ? frNode(ab) : (ab.n === 1 && ab.d === 1 ? xk : (ab.d === 1 ? B("*", num(ab.n), xk) : B("/", B("*", num(ab.n), xk), num(ab.d))));
      out = !out ? (c.n < 0 ? { t: "neg", a: t } : t) : B(c.n < 0 ? "-" : "+", out, t);
    }
    return out || ZERO;
  }
  function polyTry(n) {
    try { var p = pTrim(polyOf(n)); if (p.length <= 7 && p.filter(function (c) { return !c.zero(); }).length <= 6) return polyNode(p); } catch (e) {}
    return null;
  }
  function tidy(n) {
    // només desenvolupem sumes (un producte com 6x(x²+2)² es queda factoritzat)
    n = strip0(n);
    var sum = function (m) { m = strip0(m); return m.t === "+" || m.t === "-"; };
    if (sum(n)) { var p = polyTry(n); if (p) return p; }
    if (n.t === "neg") return { t: "neg", a: tidy(n.a) };
    if (n.t === "/" && sum(n.a)) { var q = polyTry(n.a); if (q) return simp(B("/", q, n.b)); }
    return n;
  }
  function NoDiff() { this.name = "NoDiff"; }
  function d(n) {
    n = strip0(n);
    if (indep(n)) return ZERO;
    switch (n.t) {
      case "v": return ONE;
      case "neg": return { t: "neg", a: d(n.a) };
      case "+": case "-": return B(n.t, d(n.a), d(n.b));
      case "*":
        if (indep(n.a)) return B("*", n.a, d(n.b));
        if (indep(n.b)) return B("*", n.b, d(n.a));
        return B("+", B("*", d(n.a), n.b), B("*", n.a, d(n.b)));
      case "/":
        if (indep(n.b)) return B("/", d(n.a), n.b);
        return B("/", B("-", B("*", d(n.a), n.b), B("*", n.a, d(n.b))), B("^", n.b, num(2)));
      case "^": {
        var b = strip0(n.a), e = strip0(n.b);
        if (indep(e)) return B("*", B("*", e, B("^", b, B("-", e, ONE))), d(b));
        if (indep(b)) return b.t === "c" && b.n === "e" ? B("*", B("^", b, e), d(e)) : B("*", B("*", B("^", b, e), Fn("ln", b)), d(e));
        throw new NoDiff();
      }
      case "f": {
        var g = n.a, dg = d(g);
        switch (n.n) {
          case "sqrt": return B("/", dg, B("*", num(2), Fn("sqrt", g)));
          case "exp": return B("*", Fn("exp", g), dg);
          case "ln": return B("/", dg, g);
          case "log": return B("/", dg, B("*", g, Fn("ln", num(10))));
          case "sin": return B("*", Fn("cos", g), dg);
          case "cos": return { t: "neg", a: B("*", Fn("sin", g), dg) };
          case "tan": return B("/", dg, B("^", Fn("cos", g), num(2)));
          case "arcsin": return B("/", dg, Fn("sqrt", B("-", ONE, B("^", g, num(2)))));
          case "arccos": return { t: "neg", a: B("/", dg, Fn("sqrt", B("-", ONE, B("^", g, num(2))))) };
          case "arctan": return B("/", dg, B("+", ONE, B("^", g, num(2))));
        }
        throw new NoDiff();
      }
    }
    throw new NoDiff();
  }
  function D(n) { return tidy(simp(d(n))); }

  // TeX més polit que el de la unitat 4: sin x, cos² x, exponents amb \frac
  var FNAME = { sin: "\\sin", cos: "\\cos", tan: "\\tan", arcsin: "\\arcsin", arccos: "\\arccos", arctan: "\\arctan", ln: "\\ln", log: "\\log" };
  function simpleArg(n) { n = strip0(n); return n.t === "v" || n.t === "n" || n.t === "c" || (n.t === "*" && strip0(n.a).t === "n" && strip0(n.b).t === "v"); }
  function texD(n, inExp) {
    n = strip0(n);
    function wrapSum(m) { m = strip0(m); var s = texD(m, inExp); return (m.t === "+" || m.t === "-" || m.t === "neg") ? "\\left(" + s + "\\right)" : s; }
    switch (n.t) {
      case "n": return decTex(n.s);
      case "c": return n.n === "e" ? "e" : "\\pi";
      case "v": return n.n;
      case "neg": return "-" + wrapSum(n.a);
      case "+": return texD(n.a, inExp) + "+" + texD(n.b, inExp);
      case "-": return texD(n.a, inExp) + "-" + wrapSum(n.b);
      case "*": {
        var l = strip0(n.a), r = strip0(n.b), tl = texD(l, inExp), tr = texD(r, inExp);
        if (l.t === "+" || l.t === "-") tl = "\\left(" + tl + "\\right)";
        if (r.t === "+" || r.t === "-" || r.t === "neg") tr = "\\left(" + tr + "\\right)";
        var dot = (/^[0-9]/.test(tr) || r.t === "n" || r.t === "/" || (r.t === "^" && strip0(r.a).t === "n")) ? "\\cdot " : l.t === "n" ? "" : "\\,";
        return tl + dot + tr;
      }
      case "/": return (inExp ? "\\frac{" : "\\dfrac{") + texD(n.a, inExp) + "}{" + texD(n.b, inExp) + "}";
      case "^": {
        var base = strip0(n.a), ex = texD(n.b, true), q = cst(n.b);
        if (q && q.d > 1 && q.n > 0 && !(base.t === "c")) return "\\sqrt" + (q.d === 2 ? "" : "[" + q.d + "]") + "{" + (q.n === 1 ? texD(base) : texD(B("^", base, num(q.n)))) + "}";
        if (base.t === "f" && FNAME[base.n] && base.n !== "ln" && base.n !== "log") return FNAME[base.n] + "^{" + ex + "}" + (simpleArg(base.a) ? " " + texD(base.a) : "\\left(" + texD(base.a) + "\\right)");
        var tb = texD(base, inExp);
        if (base.t !== "n" && base.t !== "v" && base.t !== "c") tb = "\\left(" + tb + "\\right)";
        return tb + "^{" + ex + "}";
      }
      case "f": {
        var arg = texD(n.a, inExp);
        if (n.n === "sqrt") return "\\sqrt{" + arg + "}";
        if (n.n === "abs") return "\\left|" + arg + "\\right|";
        if (n.n === "exp") return "e^{" + texD(n.a, true) + "}";
        return FNAME[n.n] + (simpleArg(n.a) ? " " + arg : "\\left(" + arg + "\\right)");
      }
    }
    return "?";
  }
  function T(src) { return texD(typeof src === "string" ? parse(src) : src); }
  function dOf(src) { return D(parse(src)); }

  // explicació pas a pas de la primera regla que cal aplicar
  var OUTER = {
    sqrt: "\\left[\\sqrt{g}\\right]'=\\dfrac{g'}{2\\sqrt{g}}", exp: "\\left[e^{g}\\right]'=e^{g}\\cdot g'", ln: "\\left[\\ln g\\right]'=\\dfrac{g'}{g}",
    log: "\\left[\\log g\\right]'=\\dfrac{g'}{g\\cdot\\ln 10}", sin: "\\left[\\sin g\\right]'=\\cos g\\cdot g'", cos: "\\left[\\cos g\\right]'=-\\sin g\\cdot g'",
    tan: "\\left[\\tan g\\right]'=\\dfrac{g'}{\\cos^2 g}", arcsin: "\\left[\\arcsin g\\right]'=\\dfrac{g'}{\\sqrt{1-g^2}}", arccos: "\\left[\\arccos g\\right]'=\\dfrac{-g'}{\\sqrt{1-g^2}}",
    arctan: "\\left[\\arctan g\\right]'=\\dfrac{g'}{1+g^2}"
  };
  var ELEM = {
    sqrt: "\\left(\\sqrt{x}\\right)'=\\dfrac{1}{2\\sqrt{x}}", exp: "\\left(e^{x}\\right)'=e^{x}", ln: "\\left(\\ln x\\right)'=\\dfrac1x", log: "\\left(\\log x\\right)'=\\dfrac{1}{x\\ln 10}",
    sin: "(\\sin x)'=\\cos x", cos: "(\\cos x)'=-\\sin x", tan: "(\\tan x)'=1+\\tan^2x=\\dfrac{1}{\\cos^2x}", arcsin: "(\\arcsin x)'=\\dfrac{1}{\\sqrt{1-x^2}}",
    arccos: "(\\arccos x)'=\\dfrac{-1}{\\sqrt{1-x^2}}", arctan: "(\\arctan x)'=\\dfrac{1}{1+x^2}"
  };
  function li(s) { return "<li>" + s + "</li>"; }
  function explain(src) {
    var n = strip0(parse(src)), res = D(n), fx = "f(x)=" + T(n), out = [];
    var gx = function (g) { g = strip0(g); return "g(x)=" + T(g) + ",\\quad g'(x)=" + T(D(g)); };
    if (indep(n)) out.push(u("cst"));
    else switch (n.t) {
      case "+": case "-": {
        var terms = [], st = [[n, 1]];
        while (st.length) { var p = st.pop(), q = strip0(p[0]); if (q.t === "+" || q.t === "-") { st.push([q.b, q.t === "-" ? -1 : 1]); st.push([q.a, 1]); } else terms.push(q); }
        out.push(u("sum") + "<ul>" + terms.map(function (t) { return li(tex("\\left(" + T(t) + "\\right)'=" + T(D(t)))); }).join("") + "</ul>");
        break;
      }
      case "neg": out.push(u("neg") + " " + tex("\\left(-g\\right)'=-g'") + ", " + tex(gx(n.a))); break;
      case "*":
        if (indep(n.a) || indep(n.b)) {
          var k = indep(n.a) ? n.a : n.b, g = indep(n.a) ? n.b : n.a;
          out.push(u("kf") + " " + tex("(k\\cdot g)'=k\\cdot g'") + "<br>" + tex("k=" + T(k) + ",\\quad " + gx(g)));
        } else {
          out.push(u("prod") + " " + tex("(u\\cdot v)'=u'\\cdot v+u\\cdot v'") + "<br>" + tex("u=" + T(n.a) + ",\\quad u'=" + T(D(n.a))) + "<br>" + tex("v=" + T(n.b) + ",\\quad v'=" + T(D(n.b))) +
            "<br>" + tex("f'(x)=" + texD(B("+", B("*", D(n.a), n.b), B("*", n.a, D(n.b))))));
        }
        break;
      case "/":
        if (indep(n.b)) { out.push(u("fk") + " " + tex("\\left(\\dfrac{g}{k}\\right)'=\\dfrac{g'}{k}") + "<br>" + tex("k=" + T(n.b) + ",\\quad " + gx(n.a))); break; }
        out.push(u("quo") + " " + tex("\\left(\\dfrac uv\\right)'=\\dfrac{u'\\cdot v-u\\cdot v'}{v^2}") + "<br>" + tex("u=" + T(n.a) + ",\\quad u'=" + T(D(n.a))) + "<br>" + tex("v=" + T(n.b) + ",\\quad v'=" + T(D(n.b))) +
          "<br>" + tex("f'(x)=\\dfrac{" + texD(B("-", B("*", D(n.a), n.b), B("*", n.a, D(n.b)))) + "}{" + texD(B("^", n.b, num(2))) + "}"));
        break;
      case "^": {
        var b = strip0(n.a), e = strip0(n.b);
        if (indep(e) && b.t === "v") out.push(u("powx") + " " + tex("(x^n)'=n\\,x^{n-1}") + ",\\ " + tex("n=" + texD(e, true)));
        else if (indep(e)) out.push(u("chain") + " " + tex("\\left[g^n\\right]'=n\\,g^{n-1}\\cdot g'") + "<br>" + tex("n=" + texD(e, true) + ",\\quad " + gx(b)));
        else if (b.t === "c" && b.n === "e") out.push((strip0(e).t === "v" ? u("elem") + " " + tex("(e^x)'=e^x") : u("chain") + " " + tex("\\left[e^{g}\\right]'=e^{g}\\cdot g'") + "<br>" + tex(gx(e))));
        else if (indep(b)) out.push((strip0(e).t === "v" ? u("elem") + " " + tex("(a^x)'=a^x\\cdot\\ln a") : u("chain") + " " + tex("\\left[a^{g}\\right]'=a^{g}\\cdot g'\\cdot\\ln a") + "<br>" + tex("a=" + T(b) + ",\\quad " + gx(e))));
        break;
      }
      case "f":
        if (n.n === "abs") throw new NoDiff();
        if (strip0(n.a).t === "v") out.push(u("elem") + " " + tex(ELEM[n.n]));
        else out.push(u("chain") + " " + tex(OUTER[n.n]) + "<br>" + u("inner") + ": " + tex(gx(n.a)));
        break;
    }
    return { html: "<p>" + tex(fx) + "</p>" + out.map(function (s) { return "<p>" + s + "</p>"; }).join("") + "<p><strong>" + u("res") + ":</strong> " + tex("f'(x)=" + texD(res)) + "</p>", d: res };
  }

  // valor numèric amb format
  function nt(v) { return niceTex(v); }
  function badgeD(k) {
    var C = { der: "ok", nder: "as", ang: "sf", vt: "si", ncont: "as" };
    return '<span class="badge ' + C[k] + '">' + u(k) + "</span>";
  }
  function lineTex(m, a, fa) { var b0 = fa - m * a; return "y=" + (Math.abs(m) < 1e-12 ? nt(fa) : (m === 1 ? "" : m === -1 ? "-" : nt(m)) + "x" + (Math.abs(b0) < 1e-12 ? "" : (b0 > 0 ? "+" : "") + nt(b0))); }
  // key: nom d'un text de UI o funció que torna les etiquetes (cada mòdul hi passa les seues: vegeu els presetBtns dels mòduls)
  function presetBtnsS(box, n, key, onPick) {
    var lab = typeof key === "function" ? key : function () { return u(key); };
    var bs = [];
    for (var i = 0; i < n; i++) (function (i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { onPick(i); }); box.appendChild(b); bs.push(b);
    })(i);
    onLang(function () { var L = lab() || []; bs.forEach(function (b, i) { b.textContent = L[i] != null ? L[i] : String(i + 1); }); });
    return bs;
  }
  function presetBtns(box, n, key, onPick) { return presetBtnsS(box, n, key, onPick); }
  function lineF(m, a, fa) { return function (x) { return fa + m * (x - a); }; }
  // límit lateral d'una expressió contínua en a: el seu valor (sideAt falla amb arrels com ∛x, que s'acosten molt a poc a poc)
  function contSide(g, a, side) {
    var y = g(a);
    if (isFinite(y) && Math.abs(g(a + side * 1e-12) - y) < 1e-3 * (1 + Math.abs(y))) return { k: "num", v: y };
    return sideAt(g, a, side);
  }
  // amb decimals a l'enunciat, escrivim els resultats amb decimals
  function limFmt(r, dec) { return dec && r.k === "num" ? numTex(+r.v.toFixed(6)) : limTex(r); }
  // derivades laterals a partir del quocient incremental
  function sideDer(f, a, side) { var fa = f(a); return limSide(function (x) { return (f(x) - fa) / (x - a); }, a, side); }
  // classificació de la derivabilitat en a
  function derClass(L, R, fa, dL, dR) {
    if (classify(L, R, fa) !== "ok") return "ncont";
    if (dL.k === "num" && dR.k === "num") return sameLim(dL, dR) ? "der" : "ang";
    if (dL.k === "inf" && dR.k === "inf" && dL.s === dR.s) return "vt";
    return dL.k === "inf" || dR.k === "inf" ? (dL.k === "inf" && dR.k === "inf" ? "nder" : "nder") : "nder";
  }

  /* ---------- nombres i rectes ---------- */
  function F(s) { return compile(parse(s)); }
  var RATIO = (H - MT - MB) / (W - ML - MR); // per a vistes amb la mateixa escala en els dos eixos
  function sgn(v) { return v > 0 ? 1 : v < 0 ? -1 : 0; }
  function snap(x) { if (Math.abs(x) < 1e-9) return 0; var q = fracOf(x, 12); return q ? q.n / q.d : x; }
  // valor exacte si és senzill; si no, arrodonit
  function nn(v) { var s = niceTex(v); return s.indexOf("\\approx") === 0 ? numTex(+v.toFixed(4)) : s; }
  function eqv(l, v) { var s = niceTex(v); return s.indexOf("\\approx") === 0 ? l + s : l + "=" + s; }
  function r2(v) { return numTex(+v.toFixed(2)); }
  // y − f(a) = m(x − a)
  function ptSl(m, a, fa) {
    var yl = Math.abs(fa) < 1e-12 ? "y" : "y" + (fa > 0 ? "-" : "+") + nn(Math.abs(fa));
    if (Math.abs(m) < 1e-12) return yl + "=0";
    var xr = Math.abs(a) < 1e-12 ? "x" : "\\left(x" + (a > 0 ? "-" : "+") + nn(Math.abs(a)) + "\\right)";
    return yl + "=" + (Math.abs(m - 1) < 1e-12 ? "" : Math.abs(m + 1) < 1e-12 ? "-" : nn(m)) + xr;
  }
  // y = mx + n
  function lineT(m, a, fa) {
    if (Math.abs(m) < 1e-12) return "y=" + nn(fa);
    var b0 = fa - m * a;
    return "y=" + (Math.abs(m - 1) < 1e-12 ? "" : Math.abs(m + 1) < 1e-12 ? "-" : nn(m)) + "x" + (Math.abs(b0) < 1e-9 ? "" : (b0 > 0 ? "+" : "-") + nn(Math.abs(b0)));
  }
  // tros de recta de la mateixa llargària en pantalla, siga quin siga el pendent
  function segAt(m, a, fa, v, col, k) {
    var len = (v[1] - v[0]) * (k || 0.16), r = (v[1] - v[0]) / (v[3] - v[2]) * RATIO, dx = len / Math.sqrt(1 + m * m * r * r);
    return { f: lineF(m, a, fa), a: a - dx, b: a + dx, col: col };
  }

  /* ---------- arrels, punts crítics i taula de signes (numèricament) ---------- */
  function roots(g, x0, x1, N) {
    N = N || 4000;
    var h = (x1 - x0) / N, xs = [], gs = [], out = [], i, it, m;
    for (i = 0; i <= N; i++) { xs.push(x0 + i * h); gs.push(g(xs[i])); }
    function push(r) {
      if (!(r >= x0 - 1e-12 && r <= x1 + 1e-12) || !isFinite(g(r))) return;
      r = snap(r);
      for (var k = 0; k < out.length; k++) if (Math.abs(out[k] - r) < 1e-6 * (1 + Math.abs(r))) return;
      out.push(r);
    }
    for (i = 0; i < N; i++) {
      var a = gs[i], b = gs[i + 1];
      if (!isFinite(a) || !isFinite(b)) continue;
      if (a === 0) { push(xs[i]); continue; }
      if (a * b < 0) {
        var p = xs[i], q = xs[i + 1], gp = a;
        for (it = 0; it < 80; it++) { m = (p + q) / 2; var gm = g(m); if (!isFinite(gm)) break; if (sgn(gm) === sgn(gp)) { p = m; gp = gm; } else q = m; }
        var r = (p + q) / 2;
        if (Math.abs(g(r)) < 1e-6 * (1 + Math.abs(a) + Math.abs(b))) push(r); // si no, és un pol
      } else if (i > 0 && isFinite(gs[i - 1]) && a * gs[i - 1] > 0 && Math.abs(a) <= Math.abs(gs[i - 1]) && Math.abs(a) <= Math.abs(b)) {
        // arrel doble (sense canvi de signe): mínim local de |g|
        var lo = xs[i - 1], hi = xs[i + 1];
        for (it = 0; it < 100; it++) { var m1 = lo + (hi - lo) / 3, m2 = hi - (hi - lo) / 3; if (Math.abs(g(m1)) < Math.abs(g(m2))) hi = m2; else lo = m1; }
        var rr = (lo + hi) / 2;
        if (Math.abs(g(rr)) < 1e-9) push(rr);
      }
    }
    return out.sort(function (p, q) { return p - q; });
  }
  // ev: punts on f' = 0 ("z"), on f no existeix ("h") o on comença o acaba el domini ("e"); seg: signe de f' entre ells
  function crit(f, df, x0, x1) {
    var N = 6000, h = (x1 - x0) / N, ev = [], X = [], OK = [], i, it, m;
    function ok(x) { return isFinite(f(x)) && isFinite(df(x)); }
    function add(x, k) { x = snap(x); for (var j = 0; j < ev.length; j++) if (Math.abs(ev[j].x - x) < 1e-6 * (1 + Math.abs(x))) return; ev.push({ x: x, k: k }); }
    for (i = 0; i <= N; i++) { X.push(x0 + i * h); OK.push(ok(X[i])); }
    for (i = 0; i < N; i++) {
      var p = X[i], q = X[i + 1];
      if (OK[i] !== OK[i + 1]) {
        if (OK[i] && i + 2 <= N && OK[i + 2]) { add(q, "h"); continue; }  // un sol punt fora del domini
        if (!OK[i] && i >= 1 && OK[i - 1]) continue;
        var lo = p, hi = q;
        for (it = 0; it < 60; it++) { m = (lo + hi) / 2; if (ok(m) === OK[i]) lo = m; else hi = m; }
        add((lo + hi) / 2, "e");
        continue;
      }
      if (!OK[i]) continue;
      var d1 = df(p), d2 = df(q), s1 = sgn(d1), s2 = sgn(d2), fp = f(p), dv = f(q) - fp, a, b;
      if (s1 === s2 && s1 !== 0 && dv * s1 < 0 && Math.abs(dv) > 1e-9 * (1 + Math.abs(fp))) {
        // f' no canvia de signe però f «salta» en sentit contrari: hi ha una asímptota entremig
        a = p; b = q;
        for (it = 0; it < 60; it++) { m = (a + b) / 2; var fm = f(m); if (!isFinite(fm)) { a = b = m; break; } if ((fm - f(a)) * s1 < 0) b = m; else a = m; }
        add((a + b) / 2, "h");
      } else if (s1 * s2 < 0) {
        a = p; b = q; var ga = d1;
        for (it = 0; it < 80; it++) { m = (a + b) / 2; var gm = df(m); if (!isFinite(gm)) break; if (sgn(gm) === sgn(ga)) { a = m; ga = gm; } else b = m; }
        var r = (a + b) / 2;
        if (!(Math.abs(df(r)) < 1e-6 * (1 + Math.abs(d1) + Math.abs(d2)))) add(r, "h");
      }
    }
    roots(df, x0, x1, N).forEach(function (r) { if (isFinite(f(r))) add(r, "z"); });
    ev.sort(function (p, q) { return p.x - q.x; });
    var bs = [x0].concat(ev.map(function (e) { return e.x; })).concat([x1]), seg = [];
    for (i = 0; i + 1 < bs.length; i++) {
      var A = bs[i], Bb = bs[i + 1], t = null;
      [0.5, 0.25, 0.75, 0.1, 0.9].some(function (k) { var x = A + (Bb - A) * k; if (ok(x) && df(x) !== 0) { t = x; return true; } return false; });
      seg.push({ a: A, b: Bb, s: t === null ? 0 : sgn(df(t)), t: t });
    }
    return { ev: ev, seg: seg };
  }
  // estudi complet: derivades, punts crítics i classificació
  function studyF(n, x0, x1) {
    var f = compile(n), dn = D(n), df = compile(dn), S = crit(f, df, x0, x1);
    S.f = f; S.n = n; S.dn = dn; S.df = df; S.x0 = x0; S.x1 = x1;
    try { S.d2n = D(dn); S.d2 = compile(S.d2n); } catch (e) { S.d2 = null; }
    S.ev.forEach(function (e, j) {
      e.y = f(e.x);
      if (e.k !== "z") return;
      var l = S.seg[j].s, r = S.seg[j + 1].s;
      e.t1 = l > 0 && r < 0 ? "max" : l < 0 && r > 0 ? "min" : "none";
      if (S.d2) { var v2 = S.d2(e.x); e.v2 = v2; e.t2 = !isFinite(v2) ? "?" : v2 < -1e-9 ? "max" : v2 > 1e-9 ? "min" : "undec"; }
    });
    return S;
  }
  function intTex(a, b, aInf, bInf) { return "(" + (aInf ? "-\\infty" : nn(a)) + "," + (bInf ? "+\\infty" : nn(b)) + ")"; }
  // un valor de prova «bonic» dins de l'interval
  function testPt(S, g, aInf, bInf) {
    var a = g.a, b = g.b, c;
    if (aInf && bInf) c = 0;
    else if (aInf) c = Math.ceil(b) - 1;
    else if (bInf) c = Math.floor(a) + 1;
    else {
      c = Math.round((a + b) / 2);
      if (!(c > a && c < b)) { c = Math.floor(a) + 1; if (!(c < b)) c = +((a + b) / 2).toFixed(2); }
      if (!(c > a && c < b)) c = (a + b) / 2;
    }
    var v = S.df(c);
    return isFinite(S.f(c)) && isFinite(v) && sgn(v) === g.s ? c : g.t;
  }
  function signTable(S, inf) {
    var r0 = ["<th>" + tex("x") + "</th>"], r1 = ["<th>" + u("test") + "</th>"], r2s = ["<th>" + tex("f'(x)") + "</th>"], r3 = ["<th>" + tex("f(x)") + "</th>"], last = S.seg.length - 1;
    S.seg.forEach(function (g, j) {
      var aInf = inf && j === 0, bInf = inf && j === last;
      r0.push("<td>" + tex(intTex(g.a, g.b, aInf, bInf)) + "</td>");
      if (g.s === 0) { r1.push('<td class="nd">—</td>'); r2s.push('<td class="nd">∄</td>'); r3.push('<td class="nd">' + u("noDom") + "</td>"); }
      else {
        var t = testPt(S, g, aInf, bInf);
        r1.push("<td>" + tex("f'(" + nn(t) + ")" + (g.s > 0 ? "\\gt0" : "\\lt0")) + "</td>");
        r2s.push('<td class="' + (g.s > 0 ? "p" : "m") + '">' + (g.s > 0 ? "+" : "−") + "</td>");
        r3.push('<td class="ar ' + (g.s > 0 ? "p" : "m") + '">' + (g.s > 0 ? "↗" : "↘") + "</td>");
      }
      var e = S.ev[j]; if (!e) return;
      r0.push('<td class="pt">' + tex(nn(e.x)) + "</td>"); r1.push('<td class="pt"></td>');
      r2s.push('<td class="pt">' + (e.k === "z" ? "0" : "∄") + "</td>");
      r3.push('<td class="pt">' + (e.k === "z" ? (e.t1 === "max" ? u("mx") : e.t1 === "min" ? u("mn") : "—") : e.k === "h" || !isFinite(e.y) ? "∄" : "") + "</td>");
    });
    return '<div class="tbl-wrap"><table class="data sm sgn">' + [r0, r1, r2s, r3].map(function (r) { return "<tr>" + r.join("") + "</tr>"; }).join("") + "</table></div>";
  }
  // intervals de creixement i decreixement (ajuntant els trams separats per un punt crític que no és extrem)
  function monoHtml(S, inf) {
    var runs = [], cur = null, last = S.seg.length - 1;
    S.seg.forEach(function (g, j) {
      var prev = S.ev[j - 1];
      if (cur && g.s === cur.s && prev && prev.k === "z") cur.b = j; else { cur = { s: g.s, a: j, b: j }; runs.push(cur); }
    });
    function iv(r) { return intTex(S.seg[r.a].a, S.seg[r.b].b, inf && r.a === 0, inf && r.b === last); }
    var up = runs.filter(function (r) { return r.s > 0; }).map(iv), dn = runs.filter(function (r) { return r.s < 0; }).map(iv);
    return "<p><strong>" + u("incOn") + "</strong> " + (up.length ? tex(up.join("\\cup ")) : "—") + "<br><strong>" + u("decOn") + "</strong> " + (dn.length ? tex(dn.join("\\cup ")) : "—") + "</p>";
  }
  function ptTex(x, y) { return "(" + nn(x) + "," + nn(y) + ")"; }
  function extHtml(S) {
    var z = S.ev.filter(function (e) { return e.k === "z"; });
    if (!z.length) return "<p>" + u("noCrit") + "</p>";
    return "<p>" + z.map(function (e) {
      return e.t1 === "max" ? '<span class="badge ok">' + u("maxR") + "</span> " + tex(ptTex(e.x, e.y)) : e.t1 === "min" ? '<span class="badge as">' + u("minR") + "</span> " + tex(ptTex(e.x, e.y)) : tex("x=" + nn(e.x)) + ": " + u("noExt");
    }).join("<br>") + "</p>";
  }
  // gràfica pintada de verd (creix) i roig (decreix)
  function monoCurves(S) {
    return S.seg.filter(function (g) { return g.s !== 0; }).map(function (g) { return { f: S.f, a: g.a, b: g.b, col: g.s > 0 ? "var(--ok)" : "var(--bad)" }; });
  }
  function extMarks(S) {
    return S.ev.filter(function (e) { return e.k === "z" && e.t1 !== "none"; }).map(function (e) { return { x: e.x, y: e.y, col: e.t1 === "max" ? "var(--ok)" : "var(--bad)" }; });
  }
  // finestra que mostra tots els punts crítics
  function autoView(S, def) {
    var xs = S.ev.map(function (e) { return e.x; });
    var x0 = xs.length ? Math.min.apply(null, xs) - 3 : def[0], x1 = xs.length ? Math.max.apply(null, xs) + 3 : def[1];
    if (x1 - x0 < 6) { var c = (x0 + x1) / 2; x0 = c - 3; x1 = c + 3; }
    var yy = autoY([S.f], x0, x1);
    S.ev.forEach(function (e) { if (isFinite(e.y)) { yy[0] = Math.min(yy[0], e.y - 1); yy[1] = Math.max(yy[1], e.y + 1); } });
    return [x0, x1, yy[0], yy[1]];
  }

  /* ===================== mòdul de la unitat 5 de 2n Batx CCSS ===================== */
  var M5 = (function () {
    function presetBtns(box, n, key, onPick) { return presetBtnsS(box, n, typeof key === "function" ? key : function () { return u(key); }, onPick); }
    /* ---------- textos de la interfície ---------- */
    var UI = {
      va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
        score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt",
        cont: "contínua", ev: "evitable", sf: "salt finit", si: "salt infinit", as: "asimptòtica", pc: "si", rest: "en la resta", interval: "Interval",
        der: "derivable", nder: "no derivable", ang: "punt anguló", vt: "tangent vertical", ncont: "no contínua",
        bad: "No entenc l'expressió: revisa-la.", aBad: "Escriu un nombre per al punt.", noDiff: "Aquesta expressió no la sé derivar amb les regles de la unitat (valor absolut, o x a la base i a l'exponent alhora).",
        tvm: "Taxa de variació mitjana", slope: "pendent de la recta secant", tang: "recta tangent", sec: "recta secant", exact: "Valor exacte (amb les regles de derivació)",
        est: "Estimació numèrica", left: "per l'esquerra", right2: "per la dreta", noLim: "Els dos quocients no s'acosten al mateix valor: no existeix la derivada.",
        quot: "quocient incremental", trap: "Compte! El producte de les derivades no és la derivada del producte:",
        sum: "Derivada d'una suma o resta: derivem terme a terme.", kf: "Constant per una funció: la constant es queda multiplicant.", fk: "Funció dividida per una constant: derivem el numerador.",
        prod: "Derivada d'un producte:", quo: "Derivada d'un quocient:", powx: "Derivada d'una potència de x:", neg: "Canvi de signe:", cst: "És una constant: la derivada és 0.",
        chain: "Funció composta: regla de la cadena.", outer: "funció de fora", inner: "funció de dins", elem: "Derivada d'una funció elemental (taula):", res: "Resultat",
        pointA: "En el punt", tline: "Recta tangent", isCD: "Contínua i derivable!", isC: "Contínua, però no derivable en", notC: "Encara no és contínua", almost: "Pràcticament contínua i derivable (diferències < 0,01): l'exacte és",
        wantC: "Contínua!", dl: "derivada per l'esquerra", dr: "derivada per la dreta", junction: "Punts on canvia l'expressió", pieceDer: "Derivem tros per tros (sense l'igual en els punts de canvi):",
        chkPieces: "Comprova també que cada tros siga derivable en el seu interval obert.", derAll: "La funció és derivable en tot el seu domini.", derExc: "La funció és derivable excepte en", andW: "i",
        zoomTip: "Fes zoom: si és derivable, la corba s'acaba confonent amb una recta.", fpoint: "Si \\(f\\) no és contínua en \\(a\\), no és derivable.",
        pTvm: ["Benefici B(x)", "Població 2^x", "x³/3 − x"], pSec: ["x²", "√x", "x³ − 3x", "eˣ", "1/x"], pQuot: ["x² − 3x", "3/x", "√x", "PAU Navarra", "|x − 1|"],
        pRules: ["x² i x³", "x i eˣ", "Quocient", "ln x i x²"], pChain: ["(x²+1)⁵", "√(3x−1)", "e^(x²−x)", "ln(x²+1)", "sin 3x", "ln((x−1)/(x+1))", "PAU Andalusia", "arctan x²", "2^(3x)", "cos² x"],
        pZoom: ["x² en 1", "|x − 1| en 1", "∛x en 0", "Punt anguló", "Salt", "Unió suau"], pPwd: ["Exemple resum", "PAU Andalusia 2024", "PAU Andalusia v(t)", "PAU Navarra 2024", "PAU Andalusia 2021", "PAU Andalusia 2025", "PAU COVID"],
        pPar: ["PAU Andalusia 2022", "PAU Andalusia 2020", "PAU Balears 2022", "Exemple", "PAU Aragó 2022"], pLab: ["Polinomi", "Producte", "Quocient", "Cadena", "Arrel", "Logaritme"] },
      es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
        score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba",
        cont: "continua", ev: "evitable", sf: "salto finito", si: "salto infinito", as: "asintótica", pc: "si", rest: "en el resto", interval: "Intervalo",
        der: "derivable", nder: "no derivable", ang: "punto anguloso", vt: "tangente vertical", ncont: "no continua",
        bad: "No entiendo la expresión: revísala.", aBad: "Escribe un número para el punto.", noDiff: "Esta expresión no la sé derivar con las reglas de la unidad (valor absoluto, o x en la base y en el exponente a la vez).",
        tvm: "Tasa de variación media", slope: "pendiente de la recta secante", tang: "recta tangente", sec: "recta secante", exact: "Valor exacto (con las reglas de derivación)",
        est: "Estimación numérica", left: "por la izquierda", right2: "por la derecha", noLim: "Los dos cocientes no se acercan al mismo valor: no existe la derivada.",
        quot: "cociente incremental", trap: "¡Cuidado! El producto de las derivadas no es la derivada del producto:",
        sum: "Derivada de una suma o resta: derivamos término a término.", kf: "Constante por una función: la constante se queda multiplicando.", fk: "Función dividida por una constante: derivamos el numerador.",
        prod: "Derivada de un producto:", quo: "Derivada de un cociente:", powx: "Derivada de una potencia de x:", neg: "Cambio de signo:", cst: "Es una constante: la derivada es 0.",
        chain: "Función compuesta: regla de la cadena.", outer: "función de fuera", inner: "función de dentro", elem: "Derivada de una función elemental (tabla):", res: "Resultado",
        pointA: "En el punto", tline: "Recta tangente", isCD: "¡Continua y derivable!", isC: "Continua, pero no derivable en", notC: "Todavía no es continua", almost: "Prácticamente continua y derivable (diferencias < 0,01): el exacto es",
        wantC: "¡Continua!", dl: "derivada por la izquierda", dr: "derivada por la derecha", junction: "Puntos donde cambia la expresión", pieceDer: "Derivamos trozo a trozo (sin el igual en los puntos de cambio):",
        chkPieces: "Comprueba también que cada trozo sea derivable en su intervalo abierto.", derAll: "La función es derivable en todo su dominio.", derExc: "La función es derivable excepto en", andW: "y",
        zoomTip: "Haz zoom: si es derivable, la curva acaba confundiéndose con una recta.", fpoint: "Si \\(f\\) no es continua en \\(a\\), no es derivable.",
        pTvm: ["Beneficio B(x)", "Población 2^x", "x³/3 − x"], pSec: ["x²", "√x", "x³ − 3x", "eˣ", "1/x"], pQuot: ["x² − 3x", "3/x", "√x", "PAU Navarra", "|x − 1|"],
        pRules: ["x² y x³", "x y eˣ", "Cociente", "ln x y x²"], pChain: ["(x²+1)⁵", "√(3x−1)", "e^(x²−x)", "ln(x²+1)", "sen 3x", "ln((x−1)/(x+1))", "PAU Andalucía", "arctg x²", "2^(3x)", "cos² x"],
        pZoom: ["x² en 1", "|x − 1| en 1", "∛x en 0", "Punto anguloso", "Salto", "Unión suave"], pPwd: ["Ejemplo resumen", "PAU Andalucía 2024", "PAU Andalucía v(t)", "PAU Navarra 2024", "PAU Andalucía 2021", "PAU Andalucía 2025", "PAU COVID"],
        pPar: ["PAU Andalucía 2022", "PAU Andalucía 2020", "PAU Baleares 2022", "Ejemplo", "PAU Aragón 2022"], pLab: ["Polinomio", "Producto", "Cociente", "Cadena", "Raíz", "Logaritmo"] },
      en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
        score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top",
        cont: "continuous", ev: "removable", sf: "finite jump", si: "infinite jump", as: "asymptotic", pc: "if", rest: "otherwise", interval: "Interval",
        der: "differentiable", nder: "not differentiable", ang: "corner point", vt: "vertical tangent", ncont: "not continuous",
        bad: "I can't read that expression: check it.", aBad: "Type a number for the point.", noDiff: "I can't differentiate this with the rules of the unit (absolute value, or x both in the base and in the exponent).",
        tvm: "Average rate of change", slope: "slope of the secant line", tang: "tangent line", sec: "secant line", exact: "Exact value (with the differentiation rules)",
        est: "Numerical estimate", left: "from the left", right2: "from the right", noLim: "The two quotients do not approach the same value: the derivative does not exist.",
        quot: "difference quotient", trap: "Careful! The product of the derivatives is not the derivative of the product:",
        sum: "Derivative of a sum or difference: differentiate term by term.", kf: "Constant times a function: the constant stays as a factor.", fk: "Function divided by a constant: differentiate the numerator.",
        prod: "Product rule:", quo: "Quotient rule:", powx: "Power rule:", neg: "Change of sign:", cst: "It is a constant: the derivative is 0.",
        chain: "Composite function: chain rule.", outer: "outer function", inner: "inner function", elem: "Derivative of an elementary function (table):", res: "Result",
        pointA: "At the point", tline: "Tangent line", isCD: "Continuous and differentiable!", isC: "Continuous, but not differentiable at", notC: "Not continuous yet", almost: "Practically continuous and differentiable (differences < 0.01): the exact value is",
        wantC: "Continuous!", dl: "left-hand derivative", dr: "right-hand derivative", junction: "Points where the formula changes", pieceDer: "Differentiate piece by piece (no equals sign at the break points):",
        chkPieces: "Also check that each piece is differentiable on its open interval.", derAll: "The function is differentiable on its whole domain.", derExc: "The function is differentiable except at", andW: "and",
        zoomTip: "Zoom in: if it is differentiable, the curve ends up looking like a straight line.", fpoint: "If \\(f\\) is not continuous at \\(a\\), it is not differentiable.",
        pTvm: ["Profit B(x)", "Population 2^x", "x³/3 − x"], pSec: ["x²", "√x", "x³ − 3x", "eˣ", "1/x"], pQuot: ["x² − 3x", "3/x", "√x", "PAU Navarre", "|x − 1|"],
        pRules: ["x² and x³", "x and eˣ", "Quotient", "ln x and x²"], pChain: ["(x²+1)⁵", "√(3x−1)", "e^(x²−x)", "ln(x²+1)", "sin 3x", "ln((x−1)/(x+1))", "PAU Andalusia", "arctan x²", "2^(3x)", "cos² x"],
        pZoom: ["x² at 1", "|x − 1| at 1", "∛x at 0", "Corner point", "Jump", "Smooth join"], pPwd: ["Summary example", "PAU Andalusia 2024", "PAU Andalusia v(t)", "PAU Navarre 2024", "PAU Andalusia 2021", "PAU Andalusia 2025", "PAU COVID"],
        pPar: ["PAU Andalusia 2022", "PAU Andalusia 2020", "PAU Balearic Is. 2022", "Example", "PAU Aragon 2022"], pLab: ["Polynomial", "Product", "Quotient", "Chain", "Root", "Logarithm"] }
    };
    function u(k) { return (UI[lang] || UI.va)[k]; }


    /* ---------- figures estàtiques ---------- */
    function F(s) { return compile(parse(s)); }
    var FIGS = {
      tvm: function () {
        var f = F("-x^2+10x"), m = (f(3) - f(1)) / 2;
        return { v: [-0.5, 7, -2, 28], curves: [{ f: f }, { f: lineF(m, 1, f(1)), col: "var(--accent-2)" }], pts: [{ x: 1, y: f(1) }, { x: 3, y: f(3) }], guides: [{ x: 1, y: f(1) }, { x: 3, y: f(3) }],
          labels: [{ x: 1, y: -1.4, t: "a" }, { x: 3, y: -1.4, t: "b" }, { x: 4.3, y: 26, t: "f(b) − f(a)", anchor: "start" }] };
      },
      tan: function () {
        var f = F("x^2/2+1");
        return { v: [-1, 4, -0.5, 7], curves: [{ f: f }, { f: lineF(1, 1, 1.5), col: "var(--accent-2)" }, { f: lineF(2.5, 1, 1.5), col: "var(--r3)" }, { f: lineF(1.6, 1, 1.5), col: "var(--r3)" }],
          pts: [{ x: 1, y: 1.5 }, { x: 4, y: 9 }, { x: 2.2, y: f(2.2), col: "var(--r3)" }], labels: [{ x: 0.9, y: 2.2, t: "P", anchor: "end" }, { x: 3.4, y: 3.6, t: "tangent", anchor: "start" }] };
      },
      abs: function () { return { v: [-3, 3, -1, 3], curves: [{ f: F("abs(x)") }, { f: lineF(-1, 0, 0), col: "var(--accent-2)", b: 0 }, { f: lineF(1, 0, 0), col: "var(--r3)", a: 0 }], pts: [{ x: 0, y: 0 }] }; },
      cbrt: function () { return { v: [-3, 3, -2, 2], curves: [{ f: F("x^(1/3)") }], guides: [{ x: 0 }], pts: [{ x: 0, y: 0 }] }; },
      jump: function () { return { v: [-1, 4, -1, 5], curves: [{ f: F("x+1"), b: 1 }, { f: F("x+2"), a: 1 }], pts: [{ x: 1, y: 2 }, { x: 1, y: 3, o: true }] }; },
      res: function () {
        var P = pwMake({ p: ["x+1", "x^2-1"], c: [2], inc: ["R"] }), v = [-1, 3.6, -1, 10], dr = pwDraw(P, v);
        return { v: v, curves: dr.curves.concat([{ f: lineF(1, 2, 3), col: "var(--accent-2)", a: 1, b: 2 }, { f: lineF(4, 2, 3), col: "var(--r3)", a: 2, b: 3 }]), pts: [{ x: 2, y: 3 }] };
      }
    };
    function wFigs() {
      document.querySelectorAll("[data-g]").forEach(function (el) {
        var mk = FIGS[el.getAttribute("data-g")]; if (!mk) return;
        var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("class", "lp-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Gràfica");
        el.appendChild(svg);
        var cfg = mk();
        onLang(function () { plot(svg, cfg); });
      });
    }

    /* ---------- widget: taxa de variació mitjana ---------- */
    function wTvm() {
      var w = document.getElementById("w-tvm"); if (!w) return;
      var PRE = [{ e: "-x^2+10x", v: [-0.5, 10.5, -3, 28], a: 1, b: 3 }, { e: "2^x", v: [-1, 5, -1, 24], a: 1, b: 3 }, { e: "x^3/3-x", v: [-3, 3, -4, 4], a: -1, b: 2 }];
      var st = 0, svg = w.querySelector("svg"), ra = $(w, "a"), rb = $(w, "b"), info = w.querySelector(".info");
      presetBtns($(w, "presets"), PRE.length, "pTvm", function (i) { st = i; setup(); });
      [ra, rb].forEach(function (r) { r.addEventListener("input", draw); });
      function setup() { var P = PRE[st]; [ra, rb].forEach(function (r) { r.min = P.v[0]; r.max = P.v[1]; r.step = 0.1; }); ra.value = P.a; rb.value = P.b; draw(); }
      function draw() {
        var P = PRE[st], f = F(P.e), a = +ra.value, b = +rb.value;
        $(w, "av").textContent = numTxt(a); $(w, "bv").textContent = numTxt(b);
        var fa = f(a), fb = f(b), curves = [{ f: f }], h;
        h = "<p>" + tex("f(x)=" + T(P.e)) + "</p>";
        if (Math.abs(b - a) < 1e-9) h += "<p>" + tex("a=b") + "</p>";
        else {
          var m = (fb - fa) / (b - a);
          h += "<p>" + tex("\\text{TVM}[" + numTex(Math.min(a, b)) + "," + numTex(Math.max(a, b)) + "]=\\dfrac{f(" + numTex(b) + ")-f(" + numTex(a) + ")}{" + numTex(b) + "-" + (a < 0 ? "(" + numTex(a) + ")" : numTex(a)) + "}=\\dfrac{" + numTex(+fb.toFixed(4)) + "-" + (fa < 0 ? "(" + numTex(+fa.toFixed(4)) + ")" : numTex(+fa.toFixed(4))) + "}{" + numTex(+(b - a).toFixed(4)) + "}=" + numTex(+m.toFixed(4))) + "</p>";
          h += "<p>" + u("tvm") + " = " + u("slope") + ".</p>";
          curves.push({ f: lineF(m, a, fa), col: "var(--accent-2)" });
        }
        info.innerHTML = h;
        plot(svg, { v: P.v, curves: curves, pts: [{ x: a, y: fa }, { x: b, y: fb, col: COLS[1] }], guides: [{ x: a, y: fa }, { x: b, y: fb }] });
      }
      onLang(setup);
    }

    /* ---------- widget: de la secant a la tangent ---------- */
    function wSec() {
      var w = document.getElementById("w-sec"); if (!w) return;
      var PRE = [{ e: "x^2", a: 1, v: [-1.5, 3.4, -1, 8] }, { e: "sqrt(x)", a: 4, v: [-0.5, 8.5, -0.5, 3.5] }, { e: "x^3-3x", a: 1.5, v: [-2.5, 3.6, -4, 8] }, { e: "e^x", a: 0, v: [-2.5, 2.5, -1, 7] }, { e: "1/x", a: 1, v: [0, 3.5, -0.5, 4], hm: -0.8 }];
      var st = 0, svg = w.querySelector("svg"), rh = $(w, "h"), tb = w.querySelector(".vtbl"), info = w.querySelector(".info");
      presetBtns($(w, "presets"), PRE.length, "pSec", function (i) { st = i; setup(); });
      rh.addEventListener("input", draw);
      function setup() { var P = PRE[st]; rh.min = P.hm || -2; rh.max = 2; rh.step = 0.01; rh.value = 1.5; draw(); }
      function draw() {
        var P = PRE[st], f = F(P.e), a = P.a, h = +rh.value, fa = f(a), m0 = compile(dOf(P.e))(a);
        if (Math.abs(h) < 0.005) h = 0;
        $(w, "hv").textContent = numTxt(h);
        var rows = "";
        [1, 0.1, 0.01, 0.001, -0.001, -0.01, -0.1].forEach(function (k) { if (a + k <= 0 && P.e.indexOf("sqrt") >= 0) return; rows += "<tr><td>" + tex(numTex(k)) + "</td><td>" + tex(numTex(+((f(a + k) - fa) / k).toFixed(6))) + "</td></tr>"; });
        tb.innerHTML = '<table class="data sm"><thead><tr><th>' + tex("h") + "</th><th>" + tex("\\dfrac{f(" + numTex(a) + "+h)-f(" + numTex(a) + ")}{h}") + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
        var curves = [{ f: f }, { f: lineF(m0, a, fa), col: "var(--accent-2)" }], pts = [{ x: a, y: fa }], H = "<p>" + tex("f(x)=" + T(P.e)) + "</p>";
        if (h !== 0) {
          var ms = (f(a + h) - fa) / h;
          curves.push({ f: lineF(ms, a, fa), col: "var(--r3)" }); pts.push({ x: a + h, y: f(a + h), col: "var(--r3)" });
          H += "<p>" + u("slope") + ": " + tex("\\dfrac{f(" + numTex(a) + "+h)-f(" + numTex(a) + ")}{h}=" + numTex(+ms.toFixed(5))) + "</p>";
        }
        H += "<p><strong>" + tex("f'(" + numTex(a) + ")=\\lim_{h\\to0}\\dfrac{f(" + numTex(a) + "+h)-f(" + numTex(a) + ")}{h}=" + nt(m0)) + "</strong></p>";
        H += "<p>" + u("tline") + ": " + tex(lineTex(m0, a, fa)) + "</p>";
        info.innerHTML = H;
        plot(svg, { v: P.v, curves: curves, pts: pts, guides: [{ x: a }] });
      }
      onLang(setup);
    }

    /* ---------- widget: derivada per definició (quocient incremental) ---------- */
    function wQuot() {
      var w = document.getElementById("w-quot"); if (!w) return;
      var PRE = [["x^2-3x", "2"], ["3/x", "1"], ["sqrt(x)", "4"], ["-x^2+4x+3", "1"], ["abs(x-1)", "1"]];
      var fi = $(w, "f"), ai = $(w, "a"), tb = w.querySelector(".vtbl"), info = w.querySelector(".info");
      presetBtns($(w, "presets"), PRE.length, "pQuot", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; draw(); });
      [fi, ai].forEach(function (i) { i.addEventListener("input", draw); });
      function draw() {
        var f, a = parseFr(ai.value);
        try { f = fnOf(fi.value); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
        if (!a) { ai.classList.add("bad"); info.textContent = u("aBad"); return; } ai.classList.remove("bad"); a = a.val();
        var fa = f(a), q = function (x) { return (f(x) - fa) / (x - a); }, rows = "";
        for (var k = 1; k <= 6; k++) { var h = Math.pow(10, -k); rows += "<tr><td>" + tex(numTex(h)) + "</td><td>" + tex(numTex(+q(a - h).toPrecision(7))) + "</td><td>" + tex(numTex(+q(a + h).toPrecision(7))) + "</td></tr>"; }
        tb.innerHTML = '<table class="data sm"><thead><tr><th>' + tex("h") + "</th><th>" + tex("\\dfrac{f(a-h)-f(a)}{-h}") + "</th><th>" + tex("\\dfrac{f(a+h)-f(a)}{h}") + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
        var L = limSide(q, a, -1), R = limSide(q, a, 1), at = numTex(a);
        var H = "<p>" + tex("f(x)=" + T(fi.value) + ",\\quad a=" + at) + "</p><p>" + u("est") + ": " + tex("\\lim_{h\\to0^-}=" + limTex(L) + ",\\quad\\lim_{h\\to0^+}=" + limTex(R)) + "</p>";
        H += "<p><strong>" + (sameLim(L, R) && L.k === "num" ? tex("f'(" + at + ")=" + limTex(L)) : u("noLim")) + "</strong></p>";
        try { var dd = dOf(fi.value), v = compile(dd)(a); H += '<p style="color:var(--muted)">' + u("exact") + ": " + tex("f'(x)=" + texD(dd) + "\\ \\Rightarrow\\ f'(" + at + ")=" + (isFinite(v) ? nt(v) : "\\nexists")) + "</p>"; } catch (e) {}
        info.innerHTML = H;
      }
      onLang(draw);
    }

    /* ---------- widget: propietats (suma, producte, quocient) ---------- */
    function wRules() {
      var w = document.getElementById("w-rules"); if (!w) return;
      var PRE = [["x^2", "x^3", "1"], ["x", "e^x", "0"], ["x^2+1", "x-1", "2"], ["ln(x)", "x^2", "1"]];
      var iu = $(w, "u"), iv = $(w, "v"), ix = $(w, "x0"), info = w.querySelector(".info");
      presetBtns($(w, "presets"), PRE.length, "pRules", function (i) { iu.value = PRE[i][0]; iv.value = PRE[i][1]; ix.value = PRE[i][2]; draw(); });
      [iu, iv, ix].forEach(function (i) { i.addEventListener("input", draw); });
      function draw() {
        var U, V, x0 = parseFr(ix.value);
        try { U = strip0(parse(iu.value)); iu.classList.remove("bad"); } catch (e) { iu.classList.add("bad"); info.textContent = u("bad"); return; }
        try { V = strip0(parse(iv.value)); iv.classList.remove("bad"); } catch (e) { iv.classList.add("bad"); info.textContent = u("bad"); return; }
        if (!x0) { ix.classList.add("bad"); info.textContent = u("aBad"); return; } ix.classList.remove("bad"); x0 = x0.val();
        var dU, dV; try { dU = D(U); dV = D(V); } catch (e) { info.textContent = u("noDiff"); return; }
        var ev = function (n) { return compile(n)(x0); }, xt = numTex(x0);
        var sumD = simp(B("+", dU, dV)), prD = simp(B("+", B("*", dU, V), B("*", U, dV))), quD = simp(B("/", B("-", B("*", dU, V), B("*", U, dV)), B("^", V, num(2))));
        var rows = [
          ["u'", texD(dU), ev(dU)], ["v'", texD(dV), ev(dV)],
          ["(u+v)'=u'+v'", texD(sumD), ev(sumD)],
          ["(u\\cdot v)'=u'v+uv'", texD(B("+", B("*", dU, V), B("*", U, dV))) + "=" + texD(prD), ev(prD)],
          ["\\left(\\dfrac uv\\right)'=\\dfrac{u'v-uv'}{v^2}", texD(quD), ev(quD)]
        ];
        var h = '<div class="tbl-wrap"><table class="data sm"><thead><tr><th></th><th></th><th>' + tex("x=" + xt) + "</th></tr></thead><tbody>";
        rows.forEach(function (r) { h += "<tr><td>" + tex(r[0]) + "</td><td>" + tex(r[1]) + "</td><td>" + tex(isFinite(r[2]) ? nt(r[2]) : "\\nexists") + "</td></tr>"; });
        h += "</tbody></table></div>";
        var a1 = ev(prD), a2 = ev(dU) * ev(dV);
        h += "<p>" + u("trap") + " " + tex("(u\\cdot v)'(" + xt + ")=" + nt(a1) + (Math.abs(a1 - a2) < 1e-9 ? "=" : "\\neq") + nt(a2) + "=u'(" + xt + ")\\cdot v'(" + xt + ")") + "</p>";
        info.innerHTML = h;
      }
      onLang(draw);
    }

    /* ---------- widget: f i f' ---------- */
    function wFd() {
      var w = document.getElementById("w-fd"); if (!w) return;
      var L = [
        { e: "x^2", v: [-3, 3, -1, 6], r: [-2.5, 2.5] }, { e: "x^3", v: [-2, 2, -5, 5], r: [-1.6, 1.6] }, { e: "sqrt(x)", v: [-0.5, 6, -0.5, 3], r: [0.1, 5.5] },
        { e: "1/x", v: [-4, 4, -4, 4], r: [0.3, 3.5] }, { e: "e^x", v: [-3, 2.5, -0.5, 8], r: [-2.5, 2] }, { e: "2^x", v: [-3, 3, -0.5, 7], r: [-2.5, 2.5] },
        { e: "ln(x)", v: [-0.5, 6, -3, 2.5], r: [0.2, 5.5] }, { e: "sin(x)", v: [-6.5, 6.5, -1.6, 1.6], r: [-6, 6] }, { e: "cos(x)", v: [-6.5, 6.5, -1.6, 1.6], r: [-6, 6] },
        { e: "tan(x)", v: [-1.5, 1.5, -5, 5], r: [-1.2, 1.2] }, { e: "arctan(x)", v: [-5, 5, -2, 2], r: [-4.5, 4.5] }
      ];
      var sel = $(w, "fn"), ra = $(w, "a"), sf = $(w, "pf"), sd = $(w, "pd"), info = w.querySelector(".info");
      L.forEach(function (o, i) { sel.add(new Option("f(x) = " + o.e.replace("sqrt(x)", "√x").replace("^x", "ˣ").replace("x^2", "x²").replace("x^3", "x³"), i)); });
      sel.addEventListener("change", setup); ra.addEventListener("input", draw);
      function setup() { var P = L[+sel.value]; ra.min = P.r[0]; ra.max = P.r[1]; ra.step = 0.01; ra.value = (P.r[0] + P.r[1]) / 2 + (P.r[1] - P.r[0]) / 5; draw(); }
      function draw() {
        var P = L[+sel.value], f = F(P.e), dn = dOf(P.e), df = compile(dn), a = +ra.value, fa = f(a), m = df(a);
        $(w, "av").textContent = numTxt(+a.toFixed(2));
        var yd = autoY([df], P.v[0], P.v[1]);
        if (P.e === "tan(x)") yd = [-0.5, 12];
        info.innerHTML = "<p>" + tex("f(x)=" + T(P.e) + "\\qquad f'(x)=" + texD(dn)) + "</p><p>" + tex("f'(" + numTex(+a.toFixed(2)) + ")=" + numTex(+m.toFixed(4))) + " = " + u("tang") + " (" + u("slope").split(" ")[0] + ")</p>";
        plot(sf, { v: P.v, curves: [{ f: f }, { f: lineF(m, a, fa), col: "var(--accent-2)" }], pts: [{ x: a, y: fa }], guides: [{ x: a }] });
        plot(sd, { v: [P.v[0], P.v[1], yd[0], yd[1]], curves: [{ f: df, col: "var(--accent-2)" }], pts: [{ x: a, y: m, col: "var(--accent-2)" }], guides: [{ x: a, y: m }] });
      }
      onLang(setup);
    }

    /* ---------- widget: regla de la cadena pas a pas ---------- */
    function wChain() {
      var w = document.getElementById("w-chain"); if (!w) return;
      var PRE = ["(x^2+1)^5", "sqrt(3x-1)", "e^(x^2-x)", "ln(x^2+1)", "sin(3x)", "ln((x-1)/(x+1))", "(x^2+2)^3*e^(-2x)", "arctan(x^2)", "2^(3x)", "cos(x)^2"];
      var fi = $(w, "f"), info = w.querySelector(".info");
      presetBtns($(w, "presets"), PRE.length, "pChain", function (i) { fi.value = PRE[i]; draw(); });
      fi.addEventListener("input", draw);
      function draw() {
        try { parse(fi.value); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
        try { info.innerHTML = explain(fi.value).html; } catch (e) { info.textContent = u("noDiff"); }
      }
      onLang(draw);
    }

    /* ---------- widget: zoom i derivades laterals ---------- */
    function wZoom() {
      var w = document.getElementById("w-zoom"); if (!w) return;
      var PRE = [
        { d: { p: ["x^2"] }, a: 1, v: [-1, 3, -1, 5] }, { d: { p: ["abs(x-1)"] }, a: 1, v: [-1, 3, -0.5, 2] }, { d: { p: ["x^(1/3)"] }, a: 0, v: [-2, 2, -1.6, 1.6] },
        { d: { p: ["x+1", "x^2-1"], c: [2], inc: ["R"] }, a: 2, v: [0, 4, -0.5, 9] }, { d: { p: ["2^(x+1)", "x^2-2x"], c: [0], inc: ["R"] }, a: 0, v: [-2, 2.5, -1.5, 3.5] },
        { d: { p: ["x^2-8x+60", "-x^2+32x-140"], c: [10], inc: ["L"] }, a: 10, v: [4, 16, 40, 120] }
      ];
      var st = 0, svg = w.querySelector("svg"), rz = $(w, "z"), info = w.querySelector(".info");
      presetBtns($(w, "presets"), PRE.length, "pZoom", function (i) { st = i; rz.value = 0; draw(); });
      rz.addEventListener("input", draw);
      function draw() {
        var P = PRE[st], M = pwMake(P.d), f = M.f, a = P.a, fa = f(a), z = Math.pow(10, +rz.value);
        $(w, "zv").textContent = "×" + numTxt(+z.toPrecision(3));
        var L = contSide(M.piece(0), a, -1), R = contSide(M.piece(M.c.length ? 1 : 0), a, 1);
        var dL = sideDer(f, a, -1), dR = sideDer(f, a, 1), k = derClass(L, R, fa, dL, dR);
        var ft = M.n > 1 ? pwTex(P.d) : "f(x)=" + T(P.d.p[0]);
        var h = "<p>" + tex(ft) + "</p>";
        h += "<p>" + tex("\\lim_{x\\to" + numTex(a) + "^-}f(x)=" + limTex(L) + ",\\quad \\lim_{x\\to" + numTex(a) + "^+}f(x)=" + limTex(R) + ",\\quad f(" + numTex(a) + ")=" + nt(fa)) + "</p>";
        if (k !== "ncont") h += "<p>" + tex("f'(" + numTex(a) + "^-)=" + limTex(dL) + ",\\quad f'(" + numTex(a) + "^+)=" + limTex(dR)) + "</p>";
        h += "<p>" + badgeD(k) + (k === "der" ? " " + tex("f'(" + numTex(a) + ")=" + limTex(dL)) : k === "ncont" ? " " + u("fpoint").replace(/\\\(|\\\)/g, "") : "") + "</p>";
        info.innerHTML = h;
        var cx = a, cy = isFinite(fa) ? fa : (P.v[2] + P.v[3]) / 2, hx = (P.v[1] - P.v[0]) / 2 / z, hy = (P.v[3] - P.v[2]) / 2 / z;
        var v = z > 1.01 ? [cx - hx, cx + hx, cy - hy, cy + hy] : P.v, dr = pwDraw(M, v), curves = dr.curves.slice();
        if (k !== "ncont") {
          if (dL.k === "num") curves.push({ f: lineF(dL.v, a, fa), col: "var(--accent-2)", b: a });
          if (dR.k === "num") curves.push({ f: lineF(dR.v, a, fa), col: "var(--r3)", a: a });
        }
        plot(svg, { v: v, curves: curves, pts: dr.pts.concat(isFinite(fa) ? [{ x: a, y: fa }] : []), guides: k === "vt" ? [{ x: a }] : [] });
      }
      onLang(draw);
    }

    /* ---------- estudi de la derivabilitat d'una funció a trossos ---------- */
    function dPieces(def) { return def.p.map(function (e) { try { return compile(dOf(e)); } catch (x) { return null; } }); }
    function studyD(def, env) {
      var P = pwMake(def, env), DP = dPieces(def), out = [];
      P.c.forEach(function (c, k) {
        var inside = (c > P.dom[0] || (c === P.dom[0] && P.din[0])) && (c < P.dom[1] || (c === P.dom[1] && P.din[1]));
        if (!inside) return;
        var L = contSide(P.piece(k), c, -1), R = contSide(P.piece(k + 1), c, 1), fa = P.f(c), cl = classify(L, R, fa), dL = { k: "none" }, dR = { k: "none" };
        if (cl === "ok") {
          dL = DP[k] ? contSide(function (x) { return DP[k](x, env); }, c, -1) : sideDer(P.f, c, -1);
          dR = DP[k + 1] ? contSide(function (x) { return DP[k + 1](x, env); }, c, 1) : sideDer(P.f, c, 1);
        }
        out.push({ x: c, L: L, R: R, fa: fa, cl: cl, dL: dL, dR: dR, k: derClass(L, R, fa, dL, dR) });
      });
      return { P: P, cuts: out };
    }
    function dpwTex(def) {
      var c = def.c || [], dom = def.dom || [-Infinity, Infinity];
      var rows = def.p.map(function (e, i) {
        var lo = i === 0 ? dom[0] : c[i - 1], hi = i === c.length ? dom[1] : c[i], dt;
        try { dt = texD(dOf(e)); } catch (x) { dt = "?"; }
        return dt + "&\\text{" + u("pc") + " }" + condTex(lo, false, hi, false);
      });
      return "f'(x)=\\begin{cases}" + rows.join("\\\\[3pt]") + "\\end{cases}";
    }
    function tangentBits(S, view) {
      // segments de la mateixa llargària en pantalla, siga quin siga el pendent
      var curves = [], len = (view[1] - view[0]) * 0.12, r = (view[1] - view[0]) / (view[3] - view[2]) * 0.7;
      function dx(m) { return len / Math.sqrt(1 + m * m * r * r); }
      S.cuts.forEach(function (q) {
        if (q.cl !== "ok") return;
        if (q.dL.k === "num") curves.push({ f: lineF(q.dL.v, q.x, q.fa), col: "var(--accent-2)", a: q.x - dx(q.dL.v), b: q.x });
        if (q.dR.k === "num") curves.push({ f: lineF(q.dR.v, q.x, q.fa), col: "var(--r3)", a: q.x, b: q.x + dx(q.dR.v) });
      });
      return curves;
    }
    var PWD = {
      res: { d: { p: ["x+1", "x^2-1"], c: [2], inc: ["R"] }, v: [-1, 4, -1, 12] },
      and24: { d: { p: ["-x^2+4x+3", "2x-5"], c: [4], inc: ["R"] }, v: [-1, 7, -2, 9] },
      vt: { d: { p: ["x^2-8x+60", "-x^2+32x-140"], c: [10], inc: ["L"], dom: [0, 24] }, v: [-1, 25, 0, 120] },
      nav24: { d: { p: ["-x^2-4x", "4-x", "x^2-6x+8"], c: [-1, 1], inc: ["R", "R"] }, v: [-5, 6, -3, 9] },
      and21: { d: { p: ["2^(x+1)", "x^2-2x"], c: [0], inc: ["R"] }, v: [-3, 3.5, -2, 4] },
      sup25: { d: { p: ["10+5x/2", "x^2+1", "10-5x/2"], c: [-2, 2], inc: ["L", "R"] }, v: [-5, 5, -1, 10] },
      covid: { d: { p: ["-x^2+2x-0.3", "0.1x-0.12", "-0.5x^2+8.3x-28.62"], c: [1.8, 5], inc: ["L", "L"], dom: [0.2, 10] }, v: [0, 10.5, -1, 6.5] }
    };
    function wPwd() {
      var w = document.getElementById("w-pwd"); if (!w) return;
      var KEYS = ["res", "and24", "vt", "nav24", "and21", "sup25", "covid"];
      var box = $(w, "pcs"), svg = w.querySelector("svg"), info = w.querySelector(".info"), def = null, cur = null, view = null, rows = [];
      presetBtns($(w, "presets"), KEYS.length, "pPwd", function (i) { cur = null; load(PWD[KEYS[i]].d, PWD[KEYS[i]].v); });
      function inp(v, cls) { var i = document.createElement("input"); i.type = "text"; i.className = "tin " + cls; i.value = v; i.autocomplete = "off"; i.spellcheck = false; i.addEventListener("input", read); return i; }
      function sel(v) { var s = document.createElement("select"); s.add(new Option("<", "R")); s.add(new Option("≤", "L")); s.value = v; s.addEventListener("change", read); return s; }
      function load(d, v) {
        def = { p: d.p.slice(), c: (d.c || []).slice(), dom: (d.dom || [-Infinity, Infinity]).slice(), din: (d.din || [true, true]).slice() };
        def.inc = (d.inc || def.c.map(function () { return "R"; })).slice();
        view = v; box.innerHTML = ""; rows = [];
        def.p.forEach(function (e, i) {
          var r = document.createElement("div"); r.className = "pc";
          var dot = document.createElement("span"); dot.className = "dot"; dot.style.background = COLS[0];
          var ie = inp(e, "w"); r.appendChild(dot); r.appendChild(ie);
          var o = { e: ie };
          if (i < def.c.length) { r.appendChild(document.createTextNode(u("pc") + " x ")); o.s = sel(def.inc[i]); o.c = inp(numTxt(def.c[i]), "s"); r.appendChild(o.s); r.appendChild(o.c); }
          else r.appendChild(document.createTextNode(u("rest")));
          box.appendChild(r); rows.push(o);
        });
        read();
      }
      function read() {
        var bad = false;
        var d = { p: [], c: [], inc: [], dom: def.dom, din: def.din };
        rows.forEach(function (o) {
          try { parse(o.e.value); o.e.classList.remove("bad"); } catch (e) { o.e.classList.add("bad"); bad = true; }
          d.p.push(o.e.value);
          if (o.c) { var v = parseFr(o.c.value); o.c.classList.toggle("bad", !v); if (!v) bad = true; d.c.push(v ? v.val() : 0); d.inc.push(o.s.value); }
        });
        for (var k = 1; k < d.c.length; k++) if (!(d.c[k] > d.c[k - 1])) bad = true;
        if (bad) { info.textContent = u("bad"); return; }
        cur = d; draw(d);
      }
      function draw(d) {
        var S = studyD(d), dec = /\d\.\d/.test(d.p.join(" ")), h = "<p>" + tex(pwTex(d)) + "</p><p>" + u("pieceDer") + "</p><p>" + tex(dpwTex(d)) + "</p>";
        h += '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + tex("a") + "</th><th>" + tex("f(a)") + "</th><th>" + tex("\\lim\\limits_{x\\to a^-}") + "</th><th>" + tex("\\lim\\limits_{x\\to a^+}") + "</th><th>" + tex("f'(a^-)") + "</th><th>" + tex("f'(a^+)") + "</th><th></th></tr></thead><tbody>";
        S.cuts.forEach(function (q) {
          var cont = q.cl === "ok";
          h += "<tr><td>" + tex(numTex(q.x)) + "</td><td>" + tex(limFmt({ k: isFinite(q.fa) ? "num" : "none", v: q.fa }, dec)) + "</td><td>" + tex(limFmt(q.L, dec)) + "</td><td>" + tex(limFmt(q.R, dec)) + "</td><td>" + (cont ? tex(limFmt(q.dL, dec)) : "—") + "</td><td>" + (cont ? tex(limFmt(q.dR, dec)) : "—") + "</td><td>" + badgeD(q.k) + "</td></tr>";
        });
        h += "</tbody></table></div>";
        var bad = S.cuts.filter(function (q) { return q.k !== "der"; }).map(function (q) { return numTex(q.x); });
        h += "<p><strong>" + (bad.length ? u("derExc") + " " + tex("x=" + bad.join(",\\ x=")) + "." : u("derAll")) + "</strong> <span style=\"color:var(--muted)\">" + u("chkPieces") + "</span></p>";
        info.innerHTML = h;
        var dr = pwDraw(S.P, view);
        plot(svg, { v: view, curves: dr.curves.concat(tangentBits(S, view)), pts: dr.pts });
      }
      onLang(function () { load(cur || PWD.res.d, view || PWD.res.v); });
    }

    /* ---------- widget: paràmetres (contínua i derivable) ---------- */
    function wPard() {
      var w = document.getElementById("w-pard"); if (!w) return;
      var PRE = [
        { d: { p: ["6x-3", "a x^2+b x+2"], c: [1], inc: ["L"] }, tex: "f(x)=\\begin{cases}6x-3&\\SI x\\leq1\\\\ax^2+bx+2&\\SI x\\gt1\\end{cases}", a: [0, 8, 0.1, 2], b: [-8, 4, 0.1, 0], sol: "a=5,\\ b=-4", v: [-1, 3, -6, 14] },
        { d: { p: ["2+a/(x-1)", "a+b e^x"], c: [0], inc: ["R"] }, tex: "f(x)=\\begin{cases}2+\\dfrac{a}{x-1}&\\SI x\\lt0\\\\a+b\\,e^x&\\SI x\\geq0\\end{cases}", a: [-1, 4, 0.05, 1], b: [-4, 2, 0.05, 0], sol: "a=2,\\ b=-2", v: [-4, 2.5, -4, 5] },
        { d: { p: ["x^2-3x+2", "x^2+a x+2"], c: [0], inc: ["R"] }, tex: "f(x)=\\begin{cases}x^2-3x+2&\\SI x\\lt0\\\\x^2+ax+2&\\SI x\\geq0\\end{cases}", a: [-6, 4, 0.1, 1], sol: "a=-3", v: [-2, 4, -1, 9] },
        { d: { p: ["a x^2+3x", "b x-4"], c: [2], inc: ["L"] }, tex: "f(x)=\\begin{cases}ax^2+3x&\\SI x\\leq2\\\\bx-4&\\SI x\\gt2\\end{cases}", a: [-2, 4, 0.05, 0], b: [0, 12, 0.05, 5], sol: "a=1,\\ b=7", v: [-1, 4, -4, 18] },
        { d: { p: ["x^2+2sqrt(3)", "sqrt(a x+b)", "7/2-x/6"], c: [0, 3], inc: ["L", "L"] }, tex: "f(x)=\\begin{cases}x^2+2\\sqrt3&\\SI x\\leq0\\\\\\sqrt{ax+b}&\\SI 0\\lt x\\leq3\\\\\\dfrac72-\\dfrac x6&\\SI x\\gt3\\end{cases}", a: [-3, 3, 0.05, 0], b: [0, 20, 0.1, 8], sol: "a=-1,\\ b=12", v: [-3, 7, 0, 7], onlyC: true }
      ];
      var st = 0, svg = w.querySelector("svg"), fn = $(w, "fn"), out = $(w, "out"), ra = $(w, "a"), rb = $(w, "b"), av = $(w, "av"), bv = $(w, "bv");
      presetBtns($(w, "presets"), PRE.length, "pPar", function (i) { st = i; setup(); });
      [ra, rb].forEach(function (r) { r.addEventListener("input", draw); });
      function setup() {
        var P = PRE[st];
        ra.min = P.a[0]; ra.max = P.a[1]; ra.step = P.a[2]; ra.value = P.a[3];
        $(w, "sb").style.display = P.b ? "" : "none";
        if (P.b) { rb.min = P.b[0]; rb.max = P.b[1]; rb.step = P.b[2]; rb.value = P.b[3]; }
        draw();
      }
      function draw() {
        var P = PRE[st], env = { a: +ra.value, b: P.b ? +rb.value : 0 };
        av.textContent = numTxt(env.a); bv.textContent = numTxt(env.b);
        fn.innerHTML = tex(P.tex.replace(/\\SI /g, "\\text{" + u("pc") + " }"));
        var S = studyD(P.d, env), cont = S.cuts.every(function (q) { return q.cl === "ok"; }), der = S.cuts.every(function (q) { return q.k === "der"; });
        var near = S.cuts.every(function (q) {
          return q.L.k === "num" && q.R.k === "num" && Math.abs(q.L.v - q.R.v) < 0.01 && (P.onlyC || (q.dL.k === "num" && q.dR.k === "num" && Math.abs(q.dL.v - q.dR.v) < 0.01));
        });
        if (!S.cuts.every(function (q) { return q.cl === "ok"; })) near = near && S.cuts.every(function (q) { return q.L.k === "num" && q.R.k === "num" && Math.abs(q.L.v - q.R.v) < 0.01; });
        var h = S.cuts.map(function (q) {
          var xs = numTex(q.x), s = tex("x=" + xs + ":\\ \\lim_{x\\to" + xs + "^-}f=" + limTex(q.L) + ",\\ \\lim_{x\\to" + xs + "^+}f=" + limTex(q.R));
          if (q.cl === "ok") s += "<br>" + tex("\\phantom{x=" + xs + ":}\\ f'(" + xs + "^-)=" + limTex(q.dL) + ",\\ f'(" + xs + "^+)=" + limTex(q.dR));
          return "<div>" + s + " " + badgeD(q.k) + "</div>";
        }).join("");
        var ok = P.onlyC ? cont : cont && der, msg;
        if (ok) msg = "✓ " + (P.onlyC ? u("wantC") : u("isCD")) + " " + tex(P.sol);
        else if (near) msg = "≈ " + u("almost") + " " + tex(P.sol);
        else if (cont && !P.onlyC) msg = u("isC") + " " + tex("x=" + S.cuts.filter(function (q) { return q.k !== "der"; }).map(function (q) { return numTex(q.x); }).join(",\\ "));
        else msg = u("notC");
        h += '<p class="' + (ok || near ? "msg-ok" : "msg-bad") + '">' + msg + "</p>";
        out.innerHTML = h;
        var dr = pwDraw(S.P, P.v);
        plot(svg, { v: P.v, curves: dr.curves.concat(tangentBits(S, P.v)), pts: dr.pts });
      }
      onLang(setup);
    }

    /* ---------- calculadora de derivades ---------- */
    function wLab() {
      var w = document.getElementById("w-lab5"); if (!w) return;
      var PRE = [["x^3-6x^2+9x+1", "1"], ["x^2*e^x", "0"], ["(x^2+1)/(x-2)", "3"], ["(x^2+2)^3*e^(-2x)", "0"], ["sqrt(5+x^2)", "-2"], ["ln((x-1)/(x+1))", "2"]];
      var fi = $(w, "f"), ai = $(w, "a"), svg = w.querySelector("svg"), info = w.querySelector(".info"), sb = $(w, "steps");
      presetBtns($(w, "presets"), PRE.length, "pLab", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; draw(); });
      [fi, ai].forEach(function (i) { i.addEventListener("input", draw); });
      function draw() {
        var f, ex, a = parseFr(ai.value);
        try { f = fnOf(fi.value); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); sb.innerHTML = ""; info.textContent = u("bad"); return; }
        try { ex = explain(fi.value); } catch (e) { sb.innerHTML = ""; info.textContent = u("noDiff"); plot(svg, { v: [-5, 5, -5, 5], curves: [{ f: f }] }); return; }
        sb.innerHTML = ex.html;
        if (!a) { ai.classList.add("bad"); info.textContent = u("aBad"); return; } ai.classList.remove("bad"); a = a.val();
        var df = compile(ex.d), fa = f(a), m = df(a), at = numTex(a), h;
        if (!isFinite(fa)) h = "<p>" + tex("f(" + at + ")\\ \\nexists") + "</p>";
        else if (!isFinite(m)) h = "<p>" + tex("f(" + at + ")=" + nt(fa) + ",\\quad f'(" + at + ")\\ \\nexists") + "</p>";
        else h = "<p>" + tex("f(" + at + ")=" + nt(fa) + ",\\quad f'(" + at + ")=" + nt(m)) + "</p><p>" + u("tline") + ": " + tex("y-f(a)=f'(a)(x-a)\\ \\Rightarrow\\ " + lineTex(m, a, fa)) + "</p>";
        info.innerHTML = h;
        var x0 = a - 4, x1 = a + 4, yy = autoY([f], x0, x1), curves = [{ f: f }, { f: df, col: "var(--r3)" }];
        if (isFinite(fa) && yy[1] - yy[0] > 40) yy = [Math.max(yy[0], fa - 20), Math.min(yy[1], fa + 20)];
        if (isFinite(m) && isFinite(fa)) curves.push({ f: lineF(m, a, fa), col: "var(--accent-2)" });
        plot(svg, { v: [x0, x1, yy[0], yy[1]], curves: curves, pts: isFinite(fa) ? [{ x: a, y: fa }] : [], guides: [{ x: a }] });
      }
      onLang(draw);
    }

    /* ---------- qüestionari ---------- */
    function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
    var QUIZ = [
      { q: q3("La taxa de variació mitjana de $f(x)=x^2$ en l'interval $[1,3]$ és…", "La tasa de variación media de $f(x)=x^2$ en el intervalo $[1,3]$ es…", "The average rate of change of $f(x)=x^2$ on $[1,3]$ is…"),
        o: [q3("$8$"), q3("$4$"), q3("$2$")], a: 1, e: q3("$\\frac{f(3)-f(1)}{3-1}=\\frac{9-1}{2}=4$.") },
      { q: q3("Geomètricament, $f'(a)$ és…", "Geométricamente, $f'(a)$ es…", "Geometrically, $f'(a)$ is…"),
        o: [q3("el pendent de la recta tangent a la gràfica en $x=a$", "la pendiente de la recta tangente a la gráfica en $x=a$", "the slope of the tangent line to the graph at $x=a$"), q3("el valor de $f$ en $a$", "el valor de $f$ en $a$", "the value of $f$ at $a$"), q3("l'àrea sota la corba fins a $a$", "el área bajo la curva hasta $a$", "the area under the curve up to $a$")], a: 0,
        e: q3("$f'(a)=\\lim_{h\\to0}\\frac{f(a+h)-f(a)}{h}$ és el límit dels pendents de les secants.", "$f'(a)=\\lim_{h\\to0}\\frac{f(a+h)-f(a)}{h}$ es el límite de las pendientes de las secantes.", "$f'(a)=\\lim_{h\\to0}\\frac{f(a+h)-f(a)}{h}$ is the limit of the slopes of the secants.") },
      { q: q3("Per definició, si $f(x)=x^2+x$, el quocient $\\frac{f(1+h)-f(1)}{h}$ és…", "Por definición, si $f(x)=x^2+x$, el cociente $\\frac{f(1+h)-f(1)}{h}$ es…", "By definition, if $f(x)=x^2+x$, the quotient $\\frac{f(1+h)-f(1)}{h}$ is…"),
        o: [q3("$h+3$"), q3("$h+2$"), q3("$3$")], a: 0, e: q3("$f(1+h)-f(1)=(1+2h+h^2+1+h)-2=h^2+3h$; $\\ \\frac{h^2+3h}{h}=h+3\\to3=f'(1)$.") },
      { q: q3("La derivada de $f(x)=x^2\\cdot e^x$ és…", "La derivada de $f(x)=x^2\\cdot e^x$ es…", "The derivative of $f(x)=x^2\\cdot e^x$ is…"),
        o: [q3("$2x\\,e^x$"), q3("$(x^2+2x)\\,e^x$"), q3("$x^2e^x$")], a: 1, e: q3("$(u\\cdot v)'=u'v+uv'=2x\\,e^x+x^2e^x$. Recorda que $(uv)'\\neq u'v'$.", "$(u\\cdot v)'=u'v+uv'=2x\\,e^x+x^2e^x$. Recuerda que $(uv)'\\neq u'v'$.", "$(u\\cdot v)'=u'v+uv'=2x\\,e^x+x^2e^x$. Remember that $(uv)'\\neq u'v'$.") },
      { q: q3("La derivada de $f(x)=\\dfrac{x}{x+1}$ és…", "La derivada de $f(x)=\\dfrac{x}{x+1}$ es…", "The derivative of $f(x)=\\dfrac{x}{x+1}$ is…"),
        o: [q3("$\\dfrac{1}{(x+1)^2}$"), q3("$\\dfrac{2x+1}{(x+1)^2}$"), q3("$1$")], a: 0, e: q3("$\\frac{1\\cdot(x+1)-x\\cdot1}{(x+1)^2}=\\frac{1}{(x+1)^2}$.") },
      { q: q3("La derivada de $f(x)=\\sqrt{x}$ és…", "La derivada de $f(x)=\\sqrt{x}$ es…", "The derivative of $f(x)=\\sqrt{x}$ is…"),
        o: [q3("$\\dfrac{1}{2\\sqrt x}$"), q3("$2\\sqrt x$"), q3("$\\dfrac{1}{\\sqrt x}$")], a: 0, e: q3("$\\sqrt x=x^{1/2}\\Rightarrow\\frac12x^{-1/2}=\\frac{1}{2\\sqrt x}$.") },
      { q: q3("La derivada de $f(x)=e^{3x^2}$ és…", "La derivada de $f(x)=e^{3x^2}$ es…", "The derivative of $f(x)=e^{3x^2}$ is…"),
        o: [q3("$e^{3x^2}$"), q3("$6x\\,e^{3x^2}$"), q3("$3x^2e^{3x^2-1}$")], a: 1, e: q3("Regla de la cadena: $e^{g}\\cdot g'$ amb $g=3x^2$, $g'=6x$.", "Regla de la cadena: $e^{g}\\cdot g'$ con $g=3x^2$, $g'=6x$.", "Chain rule: $e^{g}\\cdot g'$ with $g=3x^2$, $g'=6x$.") },
      { q: q3("La derivada de $f(x)=\\ln(x^2+1)$ és…", "La derivada de $f(x)=\\ln(x^2+1)$ es…", "The derivative of $f(x)=\\ln(x^2+1)$ is…"),
        o: [q3("$\\dfrac{1}{x^2+1}$"), q3("$\\dfrac{2x}{x^2+1}$"), q3("$2x\\ln(x^2+1)$")], a: 1, e: q3("$[\\ln g]'=\\frac{g'}{g}$.") },
      { q: q3("Si una funció és contínua en $x=a$…", "Si una función es continua en $x=a$…", "If a function is continuous at $x=a$…"),
        o: [q3("segur que és derivable en $a$", "seguro que es derivable en $a$", "it is certainly differentiable at $a$"), q3("pot ser derivable o no", "puede ser derivable o no", "it may or may not be differentiable"), q3("segur que no és derivable en $a$", "seguro que no es derivable en $a$", "it is certainly not differentiable at $a$")], a: 1,
        e: q3("Derivable ⇒ contínua, però no al revés: $|x|$ és contínua en 0 i no és derivable (punt anguló).", "Derivable ⇒ continua, pero no al revés: $|x|$ es continua en 0 y no es derivable (punto anguloso).", "Differentiable ⇒ continuous, but not the other way round: $|x|$ is continuous at 0 but not differentiable (corner).") },
      { q: q3("$f(x)=\\begin{cases}x^2&x\\lt1\\\\2x-1&x\\geq1\\end{cases}$ en $x=1$ és…", "$f(x)=\\begin{cases}x^2&x\\lt1\\\\2x-1&x\\geq1\\end{cases}$ en $x=1$ es…", "$f(x)=\\begin{cases}x^2&x\\lt1\\\\2x-1&x\\geq1\\end{cases}$ at $x=1$ is…"),
        o: [q3("contínua i derivable", "continua y derivable", "continuous and differentiable"), q3("contínua però no derivable", "continua pero no derivable", "continuous but not differentiable"), q3("no contínua", "no continua", "not continuous")], a: 0,
        e: q3("Laterals: $1=1=f(1)$. Derivades: $f'(1^-)=2\\cdot1=2$ i $f'(1^+)=2$: coincideixen.", "Laterales: $1=1=f(1)$. Derivadas: $f'(1^-)=2\\cdot1=2$ y $f'(1^+)=2$: coinciden.", "One-sided limits: $1=1=f(1)$. Derivatives: $f'(1^-)=2\\cdot1=2$ and $f'(1^+)=2$: they agree.") }
    ];

    return { UI: UI, QUIZ: QUIZ, ws: [wFigs, wTvm, wSec, wQuot, wRules, wFd, wChain, wZoom, wPwd, wPard, wLab] };
  })();
  /* ===================== mòdul de la unitat 6 de 2n Batx CCSS ===================== */
  var M6 = (function () {
    function presetBtns(box, n, key, onPick) { return presetBtnsS(box, n, typeof key === "function" ? key : function () { return u(key); }, onPick); }
    /* ---------- textos de la interfície ---------- */
    var UI = {
      va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
        score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt", pc: "si", rest: "en la resta",
        bad: "No entenc l'expressió: revisa-la.", aBad: "Escriu nombres per als extrems de l'interval (a < b).", noDiff: "Aquesta expressió no la sé derivar amb les regles de la unitat.",
        point: "Punt de tangència", slope: "Pendent", tline: "Recta tangent", nline: "Recta normal", horiz: "la tangent és horitzontal, així que la normal és vertical",
        perp: "Comprovació: són perpendiculars", noF: "La funció no existeix en aquest punt.", noD: "La funció no és derivable en aquest punt.",
        noPts: "cap punt de la finestra té tangent amb aquest pendent", inc: "creixent", dec: "decreixent", flat: "tangent horitzontal",
        test: "Valor de prova", noDom: "fora del domini", mx: "màx", mn: "mín", incOn: "Creixent en", decOn: "Decreixent en",
        crit: "Punts crítics", noCrit: "No hi ha cap punt on f′(x) = 0.", maxR: "Màxim relatiu", minR: "Mínim relatiu", noExt: "no és extrem",
        c1: "Canvi de signe de f′", c2: "Segona derivada", undec: "no decideix", type: "Conclusió", cand: "Candidat", endp: "extrem de l'interval", critp: "punt crític",
        absMax: "Màxim absolut", absMin: "Mínim absolut", notCont: "Compte: la funció no és contínua en tot l'interval, així que potser no té extrems absoluts.",
        goUp: "f′ > 0: si augmentes la variable, la funció puja.", goDn: "f′ < 0: si augmentes la variable, la funció baixa.", found: "Has trobat l'òptim!",
        optMax: "El màxim s'assoleix en", optMin: "El mínim s'assoleix en", many: "Hi ha molts punts crítics: mostrem l'estudi en la finestra",
        inR: "Estudi en ℝ", inI: "Estudi en l'interval",
        pTan: ["x² − 4x + 5", "x·eˣ", "ln(x² − 3)", "x³ − 3x + 1", "(x+1)/(x−1)"], pPar: ["x³ − 3x + 1 ∥ y = 9x", "x³ − 3x² ∥ y = 9x", "Tangent horitzontal", "eˣ"],
        pNorm: ["x² − 4x + 5", "√x", "x³ − 3x", "2/x", "ln x"], pMono: ["Polinomi", "x²/(x − 1)", "x·e⁻ˣ", "x³", "x − ln x"],
        pExt: ["Polinomi", "x⁴ − 2x²", "x⁴ − 4x³", "x²/(x − 1)", "x + 4/x", "x·eˣ"], pAbs: ["Exemple 1", "Exemple 2", "x·e⁻ˣ", "Contaminant"],
        pOpt: ["Llepolies", "Benefici per tona", "Cost mitjà", "Contaminació"], pBuild: ["Piscina", "Caixa", "Camp vora el riu", "Agència de viatges"],
        pLab: ["Polinomi", "Racional", "Exponencial", "Logaritme", "x/(x² + 1)", "x⁴ − 4x³", "En [0, 5]"] },
      es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
        score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba", pc: "si", rest: "en el resto",
        bad: "No entiendo la expresión: revísala.", aBad: "Escribe números para los extremos del intervalo (a < b).", noDiff: "Esta expresión no la sé derivar con las reglas de la unidad.",
        point: "Punto de tangencia", slope: "Pendiente", tline: "Recta tangente", nline: "Recta normal", horiz: "la tangente es horizontal, así que la normal es vertical",
        perp: "Comprobación: son perpendiculares", noF: "La función no existe en este punto.", noD: "La función no es derivable en este punto.",
        noPts: "ningún punto de la ventana tiene tangente con esta pendiente", inc: "creciente", dec: "decreciente", flat: "tangente horizontal",
        test: "Valor de prueba", noDom: "fuera del dominio", mx: "máx", mn: "mín", incOn: "Creciente en", decOn: "Decreciente en",
        crit: "Puntos críticos", noCrit: "No hay ningún punto donde f′(x) = 0.", maxR: "Máximo relativo", minR: "Mínimo relativo", noExt: "no es extremo",
        c1: "Cambio de signo de f′", c2: "Segunda derivada", undec: "no decide", type: "Conclusión", cand: "Candidato", endp: "extremo del intervalo", critp: "punto crítico",
        absMax: "Máximo absoluto", absMin: "Mínimo absoluto", notCont: "Cuidado: la función no es continua en todo el intervalo, así que quizá no tenga extremos absolutos.",
        goUp: "f′ > 0: si aumentas la variable, la función sube.", goDn: "f′ < 0: si aumentas la variable, la función baja.", found: "¡Has encontrado el óptimo!",
        optMax: "El máximo se alcanza en", optMin: "El mínimo se alcanza en", many: "Hay muchos puntos críticos: mostramos el estudio en la ventana",
        inR: "Estudio en ℝ", inI: "Estudio en el intervalo",
        pTan: ["x² − 4x + 5", "x·eˣ", "ln(x² − 3)", "x³ − 3x + 1", "(x+1)/(x−1)"], pPar: ["x³ − 3x + 1 ∥ y = 9x", "x³ − 3x² ∥ y = 9x", "Tangente horizontal", "eˣ"],
        pNorm: ["x² − 4x + 5", "√x", "x³ − 3x", "2/x", "ln x"], pMono: ["Polinomio", "x²/(x − 1)", "x·e⁻ˣ", "x³", "x − ln x"],
        pExt: ["Polinomio", "x⁴ − 2x²", "x⁴ − 4x³", "x²/(x − 1)", "x + 4/x", "x·eˣ"], pAbs: ["Ejemplo 1", "Ejemplo 2", "x·e⁻ˣ", "Contaminante"],
        pOpt: ["Golosinas", "Beneficio por tonelada", "Coste medio", "Contaminación"], pBuild: ["Piscina", "Caja", "Campo junto al río", "Agencia de viajes"],
        pLab: ["Polinomio", "Racional", "Exponencial", "Logaritmo", "x/(x² + 1)", "x⁴ − 4x³", "En [0, 5]"] },
      en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
        score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top", pc: "if", rest: "otherwise",
        bad: "I can't read that expression: check it.", aBad: "Type numbers for the ends of the interval (a < b).", noDiff: "I can't differentiate this with the rules of the unit.",
        point: "Point of tangency", slope: "Slope", tline: "Tangent line", nline: "Normal line", horiz: "the tangent is horizontal, so the normal is vertical",
        perp: "Check: they are perpendicular", noF: "The function does not exist at this point.", noD: "The function is not differentiable at this point.",
        noPts: "no point in the window has a tangent with this slope", inc: "increasing", dec: "decreasing", flat: "horizontal tangent",
        test: "Test value", noDom: "outside the domain", mx: "max", mn: "min", incOn: "Increasing on", decOn: "Decreasing on",
        crit: "Critical points", noCrit: "There is no point where f′(x) = 0.", maxR: "Relative maximum", minR: "Relative minimum", noExt: "not an extremum",
        c1: "Sign change of f′", c2: "Second derivative", undec: "inconclusive", type: "Conclusion", cand: "Candidate", endp: "endpoint", critp: "critical point",
        absMax: "Absolute maximum", absMin: "Absolute minimum", notCont: "Careful: the function is not continuous on the whole interval, so it may have no absolute extrema.",
        goUp: "f′ > 0: if you increase the variable, the function goes up.", goDn: "f′ < 0: if you increase the variable, the function goes down.", found: "You found the optimum!",
        optMax: "The maximum is reached at", optMin: "The minimum is reached at", many: "There are many critical points: the study is shown for the window",
        inR: "Study on ℝ", inI: "Study on the interval",
        pTan: ["x² − 4x + 5", "x·eˣ", "ln(x² − 3)", "x³ − 3x + 1", "(x+1)/(x−1)"], pPar: ["x³ − 3x + 1 ∥ y = 9x", "x³ − 3x² ∥ y = 9x", "Horizontal tangent", "eˣ"],
        pNorm: ["x² − 4x + 5", "√x", "x³ − 3x", "2/x", "ln x"], pMono: ["Polynomial", "x²/(x − 1)", "x·e⁻ˣ", "x³", "x − ln x"],
        pExt: ["Polynomial", "x⁴ − 2x²", "x⁴ − 4x³", "x²/(x − 1)", "x + 4/x", "x·eˣ"], pAbs: ["Example 1", "Example 2", "x·e⁻ˣ", "Pollutant"],
        pOpt: ["Sweets", "Profit per tonne", "Average cost", "Pollution"], pBuild: ["Swimming pool", "Box", "Field by the river", "Travel agency"],
        pLab: ["Polynomial", "Rational", "Exponential", "Logarithm", "x/(x² + 1)", "x⁴ − 4x³", "On [0, 5]"] }
    };
    function u(k) { return (UI[lang] || UI.va)[k]; }
    function t3(va, es, en) { return lang === "es" ? es : lang === "en" ? en : va; }


    /* ---------- figures estàtiques ---------- */
    var FIGS = {
      tan6: function () {
        var f = F("x^2/2+1");
        return { v: [-1, 4, -0.5, 7], curves: [{ f: f }, { f: lineF(1, 1, 1.5), col: "var(--accent-2)" }], pts: [{ x: 1, y: 1.5 }], guides: [{ x: 1, y: 1.5 }],
          labels: [{ x: 0.85, y: 2.2, t: "P(a, f(a))", anchor: "end" }, { x: 3.2, y: 3.1, t: t3("m = f′(a)", "m = f′(a)", "m = f′(a)"), anchor: "start" }] };
      },
      tn: function () {
        var f = F("x^2/4+1"), c = 2.4, hh = 8 * RATIO / 2;
        return { v: [-2, 6, c - hh, c + hh], curves: [{ f: f }, { f: lineF(1, 2, 2), col: "var(--accent-2)" }, { f: lineF(-1, 2, 2), col: "var(--r3)" }], pts: [{ x: 2, y: 2 }],
          labels: [{ x: 4.4, y: 3.6, t: t3("tangent", "tangente", "tangent"), anchor: "start" }, { x: -0.2, y: 4.6, t: "normal", anchor: "start" }, { x: 2.25, y: 1.55, t: "P", anchor: "start" }] };
      },
      mono: function () {
        var f = F("x^3-3x");
        return { v: [-2.6, 2.6, -4, 4], curves: [{ f: f, b: -1, col: "var(--ok)" }, { f: f, a: -1, b: 1, col: "var(--bad)" }, { f: f, a: 1, col: "var(--ok)" }],
          labels: [{ x: -2, y: 3, t: "f′ > 0 ↗" }, { x: 0, y: 3, t: "f′ < 0 ↘" }, { x: 2, y: 3, t: "f′ > 0 ↗" }] };
      },
      ext: function () {
        var f = F("x^3-3x");
        return { v: [-2.6, 2.6, -4, 4], curves: [{ f: f }, { f: function () { return 2; }, a: -1.8, b: -0.2, col: "var(--accent-2)" }, { f: function () { return -2; }, a: 0.2, b: 1.8, col: "var(--accent-2)" }],
          mark: [{ x: -1, y: 2, col: "var(--ok)" }, { x: 1, y: -2, col: "var(--bad)" }],
          labels: [{ x: -1, y: 2.7, t: t3("màxim relatiu", "máximo relativo", "relative max") }, { x: 1, y: -2.9, t: t3("mínim relatiu", "mínimo relativo", "relative min") }] };
      },
      x3: function () {
        return { v: [-2, 2, -3, 3], curves: [{ f: F("x^3") }, { f: function () { return 0; }, a: -1, b: 1, col: "var(--accent-2)" }], pts: [{ x: 0, y: 0 }],
          labels: [{ x: 0.15, y: -0.8, t: t3("f′(0) = 0, però no és extrem", "f′(0) = 0, pero no es extremo", "f′(0) = 0, but no extremum"), anchor: "start" }] };
      },
      absf: function () {
        var f = F("x^3-6x^2+9x+2");
        return { v: [-0.6, 5.8, -2, 25], curves: [{ f: f, col: "var(--border)" }, { f: f, a: 0, b: 5 }], guides: [{ x: 0 }, { x: 5 }],
          pts: [{ x: 1, y: 6 }], mark: [{ x: 5, y: 22, col: "var(--ok)" }, { x: 0, y: 2, col: "var(--bad)" }, { x: 3, y: 2, col: "var(--bad)" }],
          labels: [{ x: 1, y: 8.2, t: t3("màx. relatiu", "máx. relativo", "relative max") }, { x: 4.8, y: 23.2, t: t3("màx. absolut", "máx. absoluto", "absolute max"), anchor: "end" }, { x: 3, y: -0.4, t: t3("mín. absolut", "mín. absoluto", "absolute min") }] };
      }
    };
    function wFigs() {
      document.querySelectorAll("[data-g]").forEach(function (el) {
        var mk = FIGS[el.getAttribute("data-g")]; if (!mk) return;
        var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("class", "lp-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Gràfica");
        el.appendChild(svg);
        onLang(function () { plot(svg, mk()); });
      });
    }

    /* ---------- widgets: recta tangent i recta normal ---------- */
    function wTN(id, normal) {
      var w = document.getElementById(id); if (!w) return;
      var PRE = normal ? [
        { e: "x^2-4x+5", a: 3, r: [-1, 5], v: [-2, 7, 2.6] }, { e: "sqrt(x)", a: 4, r: [0.5, 8], v: [-1, 9, 1.5] }, { e: "x^3-3x", a: 1, r: [-2, 2], v: [-3.5, 3.5, 0] },
        { e: "2/x", a: 2, r: [0.4, 5], v: [-1, 6, 1.5] }, { e: "ln(x)", a: 1, r: [0.2, 6], v: [-1, 7, 0] }
      ] : [
        { e: "x^2-4x+5", a: 3, r: [-0.5, 5.5], v: [-1, 6, -1, 10] }, { e: "x*e^x", a: 0, r: [-3.5, 1.5], v: [-4, 2, -1.5, 5] }, { e: "ln(x^2-3)", a: 2, r: [1.8, 4.8], v: [-5, 5, -4, 3] },
        { e: "x^3-3x+1", a: 2, r: [-2.5, 2.5], v: [-3, 3, -6, 8] }, { e: "(x+1)/(x-1)", a: 2, r: [1.2, 4.8], v: [-3, 5, -6, 8] }
      ];
      // la normal només es veu perpendicular si els dos eixos tenen la mateixa escala
      if (normal) PRE.forEach(function (P) { var hh = (P.v[1] - P.v[0]) * RATIO / 2; P.v = [P.v[0], P.v[1], P.v[2] - hh, P.v[2] + hh]; });
      var st = 0, fi = $(w, "f"), ra = $(w, "a"), svg = w.querySelector("svg"), info = w.querySelector(".info");
      presetBtns($(w, "presets"), PRE.length, normal ? "pNorm" : "pTan", function (i) { st = i; fi.value = PRE[i].e; setup(); });
      fi.addEventListener("input", function () { if (st >= 0) { ra.min = -5; ra.max = 5; } st = -1; draw(); });
      ra.addEventListener("input", draw);
      function setup() { var P = PRE[st]; ra.min = P.r[0]; ra.max = P.r[1]; ra.step = 0.1; ra.value = P.a; draw(); }
      function draw() {
        var n, f, dn, df;
        try { n = parse(fi.value); f = compile(n); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
        try { dn = D(n); df = compile(dn); } catch (e) { info.textContent = u("noDiff"); return; }
        var a = +ra.value, fa = f(a), m = df(a), at = nn(a), v;
        $(w, "av").textContent = numTxt(a);
        if (st >= 0) v = PRE[st].v;
        else if (normal) { var yc = isFinite(fa) ? fa : 0; v = [a - 4, a + 4, yc - 4 * RATIO, yc + 4 * RATIO]; }
        else { var yy = autoY([f], a - 4, a + 4); v = [a - 4, a + 4, yy[0], yy[1]]; }
        var h = "<p>" + tex("f(x)=" + T(n)) + "</p>";
        if (!isFinite(fa) || !isFinite(m)) {
          info.innerHTML = h + "<p>" + (isFinite(fa) ? u("noD") : u("noF")) + "</p>";
          plot(svg, { v: v, curves: [{ f: f }], guides: [{ x: a }] }); return;
        }
        h += "<p>① " + u("point") + ": " + tex(eqv("f(" + at + ")", fa) + "\\ \\Rightarrow\\ P" + ptTex(a, fa)) + "</p>";
        h += "<p>② " + u("slope") + ": " + tex("f'(x)=" + texD(dn)) + "<br>" + tex(eqv("m=f'(" + at + ")", m)) + "</p>";
        h += "<p>③ " + u("tline") + ": " + tex(ptSl(m, a, fa) + "\\ \\Rightarrow\\ " + lineT(m, a, fa)) + "</p>";
        var curves = [{ f: f }, { f: lineF(m, a, fa), col: "var(--accent-2)" }], va = [];
        if (normal) {
          if (Math.abs(m) < 1e-9) { h += "<p>④ " + u("nline") + ": " + tex("x=" + at) + " (" + u("horiz") + ")</p>"; va.push(a); }
          else {
            var mn = -1 / m;
            h += "<p>④ " + u("nline") + ": " + tex(eqv("m_n=-\\dfrac{1}{f'(" + at + ")}", mn)) + "<br>" + tex(ptSl(mn, a, fa) + "\\ \\Rightarrow\\ " + lineT(mn, a, fa)) + "</p>";
            h += '<p style="color:var(--muted)">' + u("perp") + ": " + tex("m\\cdot m_n=" + nn(m) + "\\cdot\\left(" + nn(mn) + "\\right)=-1") + "</p>";
            curves.push({ f: lineF(mn, a, fa), col: "var(--r3)" });
          }
        }
        info.innerHTML = h;
        plot(svg, { v: v, curves: curves, va: va, pts: [{ x: a, y: fa }] });
      }
      onLang(setup);
    }

    /* ---------- widget: tangents amb un pendent donat ---------- */
    function wPar() {
      var w = document.getElementById("w-par"); if (!w) return;
      var PRE = [{ e: "x^3-3x+1", m: 9, v: [-3, 3, -20, 22] }, { e: "x^3-3x^2", m: 9, v: [-2, 4.2, -25, 25] }, { e: "x^2-6x+1", m: 0, v: [-1, 7, -10, 8] }, { e: "e^x", m: 1, v: [-3, 3, -1, 8] }];
      var st = 0, fi = $(w, "f"), rm = $(w, "m"), svg = w.querySelector("svg"), info = w.querySelector(".info");
      rm.min = -10; rm.max = 15; rm.step = 0.5; rm.value = PRE[0].m;
      presetBtns($(w, "presets"), PRE.length, "pPar", function (i) { st = i; fi.value = PRE[i].e; rm.value = PRE[i].m; draw(); });
      fi.addEventListener("input", function () { st = -1; draw(); });
      rm.addEventListener("input", draw);
      function draw() {
        var n, f, dn, df, m = +rm.value;
        $(w, "mv").textContent = numTxt(m);
        try { n = parse(fi.value); f = compile(n); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
        try { dn = D(n); df = compile(dn); } catch (e) { info.textContent = u("noDiff"); return; }
        var v = st >= 0 ? PRE[st].v : (function () { var yy = autoY([f], -5, 5); return [-5, 5, yy[0], yy[1]]; })();
        var xs = roots(function (x) { return df(x) - m; }, v[0], v[1]).filter(function (x) { return isFinite(f(x)); });
        var h = "<p>" + tex("f(x)=" + T(n) + ",\\quad f'(x)=" + texD(dn)) + "</p><p>" + tex("f'(x)=" + nn(m)) + " ⇒ " + (xs.length ? tex("x=" + xs.map(nn).join(",\\ x=")) : u("noPts")) + "</p>";
        var curves = [{ f: f }, { f: function (x) { return m * x; }, col: "var(--plus)" }], pts = [];
        xs.forEach(function (x) {
          var fx = f(x);
          h += "<p>" + tex("P" + ptTex(x, fx) + ":\\ " + ptSl(m, x, fx) + "\\ \\Rightarrow\\ " + lineT(m, x, fx)) + "</p>";
          curves.push({ f: lineF(m, x, fx), col: "var(--accent-2)" }); pts.push({ x: x, y: fx });
        });
        info.innerHTML = h;
        plot(svg, { v: v, curves: curves, pts: pts });
      }
      onLang(draw);
    }

    /* ---------- widget: monotonia ---------- */
    function wMono() {
      var w = document.getElementById("w-mono"); if (!w) return;
      var PRE = [{ e: "x^3-3x^2-9x+1", v: [-3.5, 5.5, -30, 12], a: -2 }, { e: "x^2/(x-1)", v: [-3, 5, -8, 10], a: 0.5 }, { e: "x*e^(-x)", v: [-1, 6, -3, 0.8], a: 0 },
        { e: "x^3", v: [-2, 2, -4, 4], a: -1 }, { e: "x-ln(x)", v: [-0.5, 5, -0.5, 4], a: 0.5 }];
      var st = 0, fi = $(w, "f"), ra = $(w, "a"), svg = w.querySelector("svg"), info = w.querySelector(".info"), tb = $(w, "tbl"), S = null, view = null;
      presetBtns($(w, "presets"), PRE.length, "pMono", function (i) { st = i; fi.value = PRE[i].e; setup(); });
      fi.addEventListener("input", function () { st = -1; setup(); });
      ra.addEventListener("input", draw);
      function setup() {
        try { S = studyF(parse(fi.value), -40, 40); fi.classList.remove("bad"); }
        catch (e) { S = null; fi.classList.toggle("bad", !(e instanceof NoDiff)); info.textContent = e instanceof NoDiff ? u("noDiff") : u("bad"); tb.innerHTML = ""; return; }
        view = st >= 0 ? PRE[st].v : autoView(S, [-6, 6]);
        var span = view[1] - view[0];
        ra.min = view[0] + span * 0.04; ra.max = view[1] - span * 0.04; ra.step = 0.05; ra.value = st >= 0 ? PRE[st].a : (view[0] + view[1]) / 2;
        tb.innerHTML = signTable(S, true) + monoHtml(S, true);
        draw();
      }
      function draw() {
        if (!S) return;
        var a = +ra.value, fa = S.f(a), m = S.df(a);
        $(w, "av").textContent = numTxt(a);
        var h = "<p>" + tex("f(x)=" + T(S.n)) + "<br>" + tex("f'(x)=" + texD(S.dn)) + "</p>", curves = monoCurves(S), pts = [];
        if (isFinite(fa) && isFinite(m)) {
          var s = Math.abs(m) < 0.02 ? 0 : sgn(m);
          h += "<p>" + tex("f'(" + numTex(+a.toFixed(2)) + ")=" + numTex(+m.toFixed(3))) + " " + (s > 0 ? "\\(\\gt0\\)" : s < 0 ? "\\(\\lt0\\)" : "≈ 0") + "</p>";
          h += "<p>" + (s > 0 ? '<span class="badge ok">↗ ' + u("inc") + "</span>" : s < 0 ? '<span class="badge as">↘ ' + u("dec") + "</span>" : '<span class="badge ev">→ ' + u("flat") + "</span>") + "</p>";
          curves.push(segAt(m, a, fa, view, "var(--accent-2)")); pts.push({ x: a, y: fa });
        } else h += "<p>" + u("noF") + "</p>";
        info.innerHTML = h.replace(/\\\((.*?)\\\)/g, function (_, x) { return tex(x); });
        plot(svg, { v: view, curves: curves, pts: pts, guides: [{ x: a }] });
      }
      onLang(setup);
    }

    /* ---------- widget: màxims i mínims ---------- */
    function critRows(S) {
      var z = S.ev.filter(function (e) { return e.k === "z"; });
      if (!z.length) return "<p>" + u("noCrit") + "</p>";
      var T1 = { max: u("maxR"), min: u("minR"), none: u("noExt") };
      var h = '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + tex("x") + "</th><th>" + tex("f(x)") + "</th><th>" + u("c2") + "</th><th>" + u("c1") + "</th><th>" + u("type") + "</th></tr></thead><tbody>";
      z.forEach(function (e) {
        var j = S.ev.indexOf(e), l = S.seg[j].s, r = S.seg[j + 1].s, sg = function (s) { return s > 0 ? "+" : s < 0 ? "-" : "\\nexists"; };
        var c2 = e.t2 === undefined || e.t2 === "?" ? "—" : tex(eqv("f''(" + nn(e.x) + ")", e.v2) + (e.t2 === "max" ? "\\lt0" : e.t2 === "min" ? "\\gt0" : "")) + (e.t2 === "undec" ? " (" + u("undec") + ")" : "");
        var cls = e.t1 === "max" ? "v-mx" : e.t1 === "min" ? "v-mn" : "";
        h += "<tr><td>" + tex(nn(e.x)) + "</td><td>" + tex(nn(e.y)) + "</td><td>" + c2 + "</td><td>" + tex(sg(l) + "\\ \\to\\ " + sg(r)) + "</td><td" + (cls ? ' class="' + cls + '"' : "") + ">" + T1[e.t1] + (e.t1 !== "none" ? " " + tex(ptTex(e.x, e.y)) : "") + "</td></tr>";
      });
      return h + "</tbody></table></div>";
    }
    function wExt() {
      var w = document.getElementById("w-ext"); if (!w) return;
      var PRE = [{ e: "x^3-3x^2-9x+1", v: [-3.5, 5.5, -30, 12] }, { e: "x^4-2x^2", v: [-2.2, 2.2, -1.5, 3] }, { e: "x^4-4x^3", v: [-1.5, 4.5, -32, 12] },
        { e: "x^2/(x-1)", v: [-3, 5, -8, 10] }, { e: "x+4/x", v: [-7, 7, -10, 10] }, { e: "x*e^x", v: [-5, 1.2, -0.8, 2.5] }];
      var st = 0, fi = $(w, "f"), svg = w.querySelector("svg"), info = w.querySelector(".info"), tb = $(w, "tbl");
      presetBtns($(w, "presets"), PRE.length, "pExt", function (i) { st = i; fi.value = PRE[i].e; draw(); });
      fi.addEventListener("input", function () { st = -1; draw(); });
      function draw() {
        var S;
        try { S = studyF(parse(fi.value), -40, 40); fi.classList.remove("bad"); }
        catch (e) { fi.classList.toggle("bad", !(e instanceof NoDiff)); info.textContent = e instanceof NoDiff ? u("noDiff") : u("bad"); tb.innerHTML = ""; return; }
        var z = S.ev.filter(function (e) { return e.k === "z"; });
        var h = "<p>" + tex("f(x)=" + T(S.n)) + "</p><p>" + tex("f'(x)=" + texD(S.dn)) + "</p>";
        h += "<p>" + u("crit") + ": " + (z.length ? tex("f'(x)=0\\ \\Rightarrow\\ x=" + z.map(function (e) { return nn(e.x); }).join(",\\ x=")) : u("noCrit")) + "</p>";
        if (S.d2) h += "<p>" + tex("f''(x)=" + texD(S.d2n)) + "</p>";
        info.innerHTML = h + extHtml(S);
        tb.innerHTML = critRows(S);
        var v = st >= 0 ? PRE[st].v : autoView(S, [-6, 6]);
        plot(svg, { v: v, curves: [{ f: S.f }], mark: extMarks(S), pts: z.filter(function (e) { return e.t1 === "none"; }).map(function (e) { return { x: e.x, y: e.y }; }) });
      }
      onLang(draw);
    }

    /* ---------- extrems absoluts en [a, b] ---------- */
    function absStudy(n, a, b) {
      var S = studyF(n, a, b), f = S.f, c = [{ x: a, k: "e" }];
      S.ev.forEach(function (e) { if (e.k === "z" && e.x > a + 1e-9 && e.x < b - 1e-9) c.push({ x: e.x, k: "z" }); });
      c.push({ x: b, k: "e" });
      c.forEach(function (q) { q.y = f(q.x); });
      var ys = c.map(function (q) { return q.y; }).filter(isFinite), M = Math.max.apply(null, ys), m = Math.min.apply(null, ys);
      c.forEach(function (q) { q.max = isFinite(q.y) && Math.abs(q.y - M) < 1e-9 * (1 + Math.abs(M)); q.min = isFinite(q.y) && Math.abs(q.y - m) < 1e-9 * (1 + Math.abs(m)); });
      var cont = !S.ev.some(function (e) { return e.k !== "z"; }) && c.every(function (q) { return isFinite(q.y); });
      return { S: S, c: c, M: M, m: m, cont: cont };
    }
    function absHtml(A) {
      var h = '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + u("cand") + "</th><th></th><th>" + tex("f(x)") + "</th></tr></thead><tbody>";
      A.c.forEach(function (q) {
        var cls = q.max ? ' class="v-mx"' : q.min ? ' class="v-mn"' : "";
        h += "<tr><td>" + tex("x=" + nn(q.x)) + "</td><td>" + (q.k === "e" ? u("endp") : u("critp")) + "</td><td" + cls + ">" + tex(isFinite(q.y) ? nn(q.y) : "\\nexists") + "</td></tr>";
      });
      h += "</tbody></table></div>";
      function at(k) { return A.c.filter(function (q) { return q[k]; }).map(function (q) { return nn(q.x); }).join(",\\ x="); }
      h += "<p>" + '<span class="badge ok">' + u("absMax") + "</span> " + tex(nn(A.M) + "\\ \\text{" + t3("en", "en", "at") + " } x=" + at("max")) + "<br>" +
        '<span class="badge as">' + u("absMin") + "</span> " + tex(nn(A.m) + "\\ \\text{" + t3("en", "en", "at") + " } x=" + at("min")) + "</p>";
      if (!A.cont) h += '<p class="msg-bad">' + u("notCont") + "</p>";
      return h;
    }
    function absMarks(A) {
      var mk = [];
      A.c.forEach(function (q) { if (q.max) mk.push({ x: q.x, y: q.y, col: "var(--ok)" }); else if (q.min) mk.push({ x: q.x, y: q.y, col: "var(--bad)" }); });
      return mk;
    }
    function wAbs() {
      var w = document.getElementById("w-abs"); if (!w) return;
      var PRE = [{ e: "x^3-6x^2+9x+2", r: [-0.5, 5.5], a: 0, b: 5, v: [-0.8, 5.8, -6, 38] }, { e: "x^3-3x^2-9x+1", r: [-3, 5], a: -2, b: 4, v: [-3.3, 5.3, -30, 10] },
        { e: "x*e^(-x)", r: [-0.5, 5], a: 0, b: 3, v: [-0.7, 5.2, -1, 0.6] }, { e: "-x^3+9x^2-15x+40", r: [-1, 7], a: 0, b: 6, v: [-1.3, 7.3, 0, 75] }];
      var st = 0, ra = $(w, "a"), rb = $(w, "b"), svg = w.querySelector("svg"), fn = $(w, "fn"), info = w.querySelector(".cands");
      presetBtns($(w, "presets"), PRE.length, "pAbs", function (i) { st = i; setup(); });
      ra.addEventListener("input", function () { if (+ra.value > +rb.value - 0.2) ra.value = +rb.value - 0.2; draw(); });
      rb.addEventListener("input", function () { if (+rb.value < +ra.value + 0.2) rb.value = +ra.value + 0.2; draw(); });
      function setup() { var P = PRE[st]; [ra, rb].forEach(function (r) { r.min = P.r[0]; r.max = P.r[1]; r.step = 0.1; }); ra.value = P.a; rb.value = P.b; draw(); }
      function draw() {
        var P = PRE[st], n = parse(P.e), a = +ra.value, b = +rb.value, A = absStudy(n, a, b), f = A.S.f;
        $(w, "av").textContent = numTxt(a); $(w, "bv").textContent = numTxt(b);
        fn.innerHTML = tex("f(x)=" + T(n) + "\\ \\text{" + t3("en", "en", "on") + " }[" + nn(a) + "," + nn(b) + "]") + "<br>" + tex("f'(x)=" + texD(A.S.dn));
        info.innerHTML = absHtml(A);
        plot(svg, { v: P.v, curves: [{ f: f, col: "var(--border)" }, { f: f, a: a, b: b }], guides: [{ x: a }, { x: b }], pts: A.c.map(function (q) { return { x: q.x, y: q.y }; }), mark: absMarks(A) });
      }
      onLang(setup);
    }

    /* ---------- widget: optimització amb la funció donada ---------- */
    function optOf(f, df, dom, kind) {
      var c = [dom[0], dom[1]].concat(roots(df, dom[0], dom[1]).filter(function (x) { return x > dom[0] && x < dom[1]; }));
      var best = null;
      c.forEach(function (x) { var y = f(x); if (isFinite(y) && (best === null || (kind === "max" ? y > best.y : y < best.y))) best = { x: x, y: y }; });
      return best;
    }
    function wOpt() {
      var w = document.getElementById("w-opt"); if (!w) return;
      var PRE = [
        { e: "-0.1x^2+2.5x-10", dt: "-0.2x+2.5", fn: "B", vr: "x", dom: [0, 25], step: 0.1, x: 5, k: "max", v: [-1, 26, -11, 7.5],
          d: function () { return t3("x: tones venudes; B(x): benefici en milions d'€.", "x: toneladas vendidas; B(x): beneficio en millones de €.", "x: tonnes sold; B(x): profit in millions of €."); } },
        { e: "-0.1x+2.5-10/x", dt: "-0.1+\\dfrac{10}{x^2}", fn: "g", vr: "x", dom: [1, 25], step: 0.1, x: 3, k: "max", v: [0, 26, -8, 1.5],
          d: function () { return t3("x: tones; g(x) = B(x)/x: benefici per tona (milions d'€).", "x: toneladas; g(x) = B(x)/x: beneficio por tonelada (millones de €).", "x: tonnes; g(x) = B(x)/x: profit per tonne (millions of €)."); } },
        { e: "x+10+400/x", dt: "1-\\dfrac{400}{x^2}", fn: "CM", vr: "x", dom: [5, 80], step: 0.5, x: 50, k: "min", v: [0, 82, 0, 110],
          d: function () { return t3("x: unitats fabricades; CM(x): cost mitjà per unitat (€).", "x: unidades fabricadas; CM(x): coste medio por unidad (€).", "x: units made; CM(x): average cost per unit (€)."); } },
        { e: "t^3-15t^2+63t+40", dt: "3t^2-30t+63", fn: "C", vr: "t", dom: [0, 8], step: 0.05, x: 6, k: "max", v: [-0.5, 8.5, 0, 140],
          d: function () { return t3("t: hores (de 0 a 8); C(t): nivell de contaminació.", "t: horas (de 0 a 8); C(t): nivel de contaminación.", "t: hours (0 to 8); C(t): pollution level."); } }
      ];
      var st = 0, rx = $(w, "x"), svg = w.querySelector("svg"), fn = $(w, "fn"), out = w.querySelector(".opt-out"), P, f, dn, df, best;
      presetBtns($(w, "presets"), PRE.length, "pOpt", function (i) { st = i; setup(); });
      rx.addEventListener("input", draw);
      $(w, "show").addEventListener("click", function () { rx.value = best.x; draw(); });
      function setup() {
        P = PRE[st]; var n = parse(P.e); f = compile(n); dn = D(n); df = compile(dn); best = optOf(f, df, P.dom, P.k);
        rx.min = P.dom[0]; rx.max = P.dom[1]; rx.step = P.step; rx.value = P.x;
        draw();
      }
      function draw() {
        var x = +rx.value, y = f(x), m = df(x), V = P.vr, nm = P.fn + "(" + V + ")";
        $(w, "xn").innerHTML = tex(V + "="); $(w, "xv").textContent = numTxt(x);
        fn.innerHTML = "<p>" + tex(nm + "=" + T(P.e) + ",\\quad " + V + "\\in[" + nn(P.dom[0]) + "," + nn(P.dom[1]) + "]") + "<br>" + tex(P.fn + "'(" + V + ")=" + (lang === "en" ? P.dt : P.dt.replace(/(\d)\.(\d)/g, "$1{,}$2"))) + "</p><p style=\"color:var(--muted)\">" + P.d() + "</p>";
        var s = Math.abs(m) < 1e-3 * (1 + Math.abs(y)) ? 0 : sgn(m);
        var h = "<p>" + tex(P.fn + "(" + r2(x) + ")=" + r2(y) + ",\\quad " + P.fn + "'(" + r2(x) + ")=" + numTex(+m.toFixed(3))) + "</p><p>" + (s > 0 ? u("goUp") : s < 0 ? u("goDn") : "→ " + u("flat")) + "</p>";
        if (Math.abs(x - best.x) < P.step * 0.6) h += '<p class="msg-ok">✓ ' + u("found") + " " + u(P.k === "max" ? "optMax" : "optMin") + " " + tex(V + "=" + numTex(+best.x.toFixed(4))) + ": " + tex(P.fn + "(" + numTex(+best.x.toFixed(4)) + ")=" + numTex(+best.y.toFixed(4))) + "</p>";
        out.innerHTML = h;
        plot(svg, { v: P.v, curves: [{ f: f, a: P.dom[0], b: P.dom[1] }, segAt(m, x, y, P.v, "var(--accent-2)", 0.12)], pts: [{ x: x, y: y }], guides: [{ x: x, y: y }] });
      }
      onLang(setup);
    }

    /* ---------- widget: construïm la funció (dibuix + gràfica) ---------- */
    function P2(x, y) { return { x: +x.toFixed(1), y: +y.toFixed(1) }; }
    function ln2(p, q, cls) { return '<line class="' + cls + '" x1="' + p.x + '" y1="' + p.y + '" x2="' + q.x + '" y2="' + q.y + '"/>'; }
    function poly(ps, cls) { return '<polygon class="' + cls + '" points="' + ps.map(function (p) { return p.x + "," + p.y; }).join(" ") + '"/>'; }
    function txt(x, y, s, anchor, cls) { return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="' + (anchor || "middle") + '"' + (cls ? ' class="' + cls + '"' : "") + ">" + s + "</text>"; }
    // prisma obert per dalt (perspectiva cavallera): amplària w, fondària d, altura h
    function prism(ox, oy, wd, dp, ht, s, labs) {
      var k = 0.45, c = Math.cos(Math.PI / 6) * k, si = Math.sin(Math.PI / 6) * k;
      function P(u0, v0, z0) { return P2(ox + (u0 + z0 * c) * s, oy - (v0 + z0 * si) * s); }
      var A = P(0, 0, 0), Bq = P(wd, 0, 0), C = P(wd, ht, 0), Dq = P(0, ht, 0), A2 = P(0, 0, dp), B2 = P(wd, 0, dp), C2 = P(wd, ht, dp), D2 = P(0, ht, dp);
      var g = poly([A, Bq, C, Dq], "wt") + poly([Bq, B2, C2, C], "wt") + poly([Dq, C, C2, D2], "top");
      g += ln2(A, A2, "ed hid") + ln2(A2, B2, "ed hid") + ln2(A2, D2, "ed hid");
      g += poly([A, Bq, C, Dq], "ed") + ln2(Bq, B2, "ed") + ln2(B2, C2, "ed") + ln2(C, C2, "ed") + ln2(Dq, D2, "ed") + ln2(D2, C2, "ed");
      g += txt((A.x + Bq.x) / 2, A.y + 18, labs[0]) + txt((Bq.x + B2.x) / 2 + 8, (Bq.y + B2.y) / 2 + 12, labs[1], "start") + txt(A.x - 8, (A.y + Dq.y) / 2 + 4, labs[2], "end");
      return g;
    }
    var BUILD = [
      { e: "x^2+128/x", fn: "S", dom: [1.5, 8], step: 0.05, x: 2, v: [0, 8.5, 0, 110], kind: "min",
        head: function () { return tex("x^2y=32\\Rightarrow y=\\dfrac{32}{x^2}") + "&emsp;" + tex("S=x^2+4xy\\Rightarrow S(x)=x^2+\\dfrac{128}{x}"); },
        draw: function (x) {
          var y = 32 / (x * x), c = Math.cos(Math.PI / 6) * 0.45, si = Math.sin(Math.PI / 6) * 0.45, s = Math.min(300 / (x + x * c), 220 / (y + x * si));
          var ox = (420 - (x + x * c) * s) / 2, oy = 300 - (300 - (y + x * si) * s) / 2;
          return prism(ox, oy, x, x, y, s, ["x = " + numTxt(+x.toFixed(2)) + " m", "x", "y = " + numTxt(+y.toFixed(2)) + " m"]);
        },
        info: function (x) { var y = 32 / (x * x); return tex("x=" + r2(x) + "\\text{ m},\\quad y=\\dfrac{32}{x^2}=" + r2(y) + "\\text{ m},\\quad S=" + r2(x * x + 128 / x) + "\\text{ m}^2"); },
        unit: "\\text{ m}^2" },
      { e: "x(12-2x)^2", fn: "V", dom: [0.2, 5.8], step: 0.05, x: 1, v: [0, 6, 0, 140], kind: "max",
        head: function () { return tex(t3("\\text{base: }(12-2x)^2,\\ \\text{altura: }x", "\\text{base: }(12-2x)^2,\\ \\text{altura: }x", "\\text{base: }(12-2x)^2,\\ \\text{height: }x")) + "&emsp;" + tex("V(x)=x\\,(12-2x)^2"); },
        draw: function (x) {
          var s = 16, ox = 16, oy = 50, L = 12, g = "", b = L - 2 * x;
          g += '<rect class="sheet" x="' + ox + '" y="' + oy + '" width="' + L * s + '" height="' + L * s + '"/>';
          [[0, 0], [L - x, 0], [0, L - x], [L - x, L - x]].forEach(function (q) { g += '<rect class="cut" x="' + (ox + q[0] * s) + '" y="' + (oy + q[1] * s) + '" width="' + x * s + '" height="' + x * s + '"/>'; });
          g += '<rect class="fold" x="' + (ox + x * s) + '" y="' + (oy + x * s) + '" width="' + b * s + '" height="' + b * s + '"/>';
          g += txt(ox + x * s / 2, oy - 6, "x") + txt(ox + L * s / 2, oy + L * s + 18, "12 cm") + txt(ox + L * s / 2, oy + (L - x) * s - 6, "12 − 2x", "middle", "sm");
          // la caixa, a la dreta, sempre a la mida més gran que hi cap
          var c = Math.cos(Math.PI / 6) * 0.45, si = Math.sin(Math.PI / 6) * 0.45, sb = Math.min(160 / (b * (1 + c)), 170 / (x + b * si));
          g += prism(236 + (172 - b * (1 + c) * sb) / 2, 160 + (x + b * si) * sb / 2, b, b, x, sb, [numTxt(+b.toFixed(2)), numTxt(+b.toFixed(2)), "x = " + numTxt(+x.toFixed(2))]);
          return g;
        },
        info: function (x) { var b = 12 - 2 * x; return tex("x=" + r2(x) + "\\text{ cm},\\quad 12-2x=" + r2(b) + "\\text{ cm},\\quad V=" + r2(x * b * b) + "\\text{ cm}^3"); },
        unit: "\\text{ cm}^3" },
      { e: "x(400-2x)", fn: "A", dom: [5, 195], step: 1, x: 40, v: [0, 200, 0, 22000], kind: "max",
        head: function () { return tex("2x+y=400\\Rightarrow y=400-2x") + "&emsp;" + tex("A(x)=x\\,(400-2x)"); },
        draw: function (x) {
          var y = 400 - 2 * x, s = 0.95, L = (420 - y * s) / 2, R = L + y * s, top = 62, bot = top + x * s, g = "";
          g += '<rect class="river" x="6" y="18" width="408" height="' + (top - 18) + '"/>' + txt(210, 46, t3("riu", "río", "river"), "middle", "sm");
          g += '<rect class="area" x="' + L.toFixed(1) + '" y="' + top + '" width="' + (y * s).toFixed(1) + '" height="' + (x * s).toFixed(1) + '"/>';
          g += '<polyline class="fence" points="' + L.toFixed(1) + "," + top + " " + L.toFixed(1) + "," + bot.toFixed(1) + " " + R.toFixed(1) + "," + bot.toFixed(1) + " " + R.toFixed(1) + "," + top + '"/>';
          g += txt(L - 8, (top + bot) / 2 + 4, "x = " + numTxt(x), "end") + txt((L + R) / 2, bot + 20, "y = " + numTxt(y));
          return g;
        },
        info: function (x) { var y = 400 - 2 * x; return tex("x=" + r2(x) + "\\text{ m},\\quad y=400-2x=" + r2(y) + "\\text{ m},\\quad A=" + r2(x * y) + "\\text{ m}^2"); },
        unit: "\\text{ m}^2" },
      { e: "(30+x)(600-10x)", fn: "I", dom: [0, 40], step: 1, x: 5, v: [-1, 41, 0, 23000], kind: "max",
        head: function () { return tex(t3("\\text{persones: }30+x,\\ \\text{preu: }600-10x", "\\text{personas: }30+x,\\ \\text{precio: }600-10x", "\\text{people: }30+x,\\ \\text{price: }600-10x")) + "&emsp;" + tex("I(x)=(30+x)(600-10x)"); },
        draw: function (x) {
          var np = 30 + x, pr = 600 - 10 * x, sx = 4.8, sy = 0.36, ox = 70, oy = 262, g = "";
          g += ln2(P2(ox, oy), P2(ox + 345, oy), "axl") + ln2(P2(ox, oy), P2(ox, 20), "axl");
          g += '<rect class="area" x="' + ox + '" y="' + (oy - pr * sy).toFixed(1) + '" width="' + (np * sx).toFixed(1) + '" height="' + (pr * sy).toFixed(1) + '"/>';
          g += txt(ox + np * sx / 2, oy + 20, t3("persones: ", "personas: ", "people: ") + np) + txt(ox - 8, oy - pr * sy / 2, pr + " €", "end");
          g += txt(ox + np * sx / 2, oy - pr * sy / 2 + 5, "I = " + numTxt(np * pr) + " €");
          return g;
        },
        info: function (x) { return tex("x=" + x + ",\\quad " + t3("\\text{persones}", "\\text{personas}", "\\text{people}") + "=" + (30 + x) + ",\\quad " + t3("\\text{preu}", "\\text{precio}", "\\text{price}") + "=" + (600 - 10 * x) + "\\text{ €},\\quad I=" + numTex((30 + x) * (600 - 10 * x)) + "\\text{ €}"); },
        unit: "\\text{ €}" }
    ];
    function wBuild() {
      var w = document.getElementById("w-build"); if (!w) return;
      var st = 0, rx = $(w, "x"), dr = $(w, "draw"), gr = $(w, "graph"), fn = $(w, "fn"), out = w.querySelector(".opt-out"), P, f, df, best;
      presetBtns($(w, "presets"), BUILD.length, "pBuild", function (i) { st = i; setup(); });
      rx.addEventListener("input", draw);
      $(w, "show").addEventListener("click", function () { rx.value = best.x; draw(); });
      function setup() {
        P = BUILD[st]; var n = parse(P.e); f = compile(n); df = compile(D(n)); best = optOf(f, df, P.dom, P.kind);
        rx.min = P.dom[0]; rx.max = P.dom[1]; rx.step = P.step; rx.value = P.x;
        draw();
      }
      function draw() {
        var x = +rx.value, y = f(x);
        $(w, "xv").textContent = numTxt(x);
        fn.innerHTML = P.head();
        dr.setAttribute("viewBox", "0 0 420 300"); dr.innerHTML = P.draw(x);
        var h = "<p>" + P.info(x) + "</p>";
        if (Math.abs(x - best.x) < P.step * 0.6) h += '<p class="msg-ok">✓ ' + u("found") + " " + u(P.kind === "max" ? "optMax" : "optMin") + " " + tex("x=" + nn(best.x)) + ": " + tex(P.fn + "(" + nn(best.x) + ")=" + nn(best.y) + P.unit) + "</p>";
        out.innerHTML = h;
        plot(gr, { v: P.v, curves: [{ f: f, a: P.dom[0], b: P.dom[1] }], pts: [{ x: x, y: y }], guides: [{ x: x, y: y }] });
      }
      onLang(setup);
    }

    /* ---------- estudi complet d'una funció ---------- */
    function wLab() {
      var w = document.getElementById("w-lab6"); if (!w) return;
      var PRE = [["x^3-3x^2-9x+1", "", ""], ["x^2/(x-1)", "", ""], ["(x^2-3)*e^x", "", ""], ["x-ln(x)", "", ""], ["x/(x^2+1)", "", ""], ["x^4-4x^3", "", ""], ["x^3-6x^2+9x+2", "0", "5"]];
      var fi = $(w, "f"), ai = $(w, "a"), bi = $(w, "b"), svg = w.querySelector("svg"), out = $(w, "out"), tb = $(w, "tbl");
      presetBtns($(w, "presets"), PRE.length, "pLab", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; bi.value = PRE[i][2]; draw(); });
      [fi, ai, bi].forEach(function (i) { i.addEventListener("input", draw); });
      function draw() {
        var n, a = null, b = null, iv = ai.value.trim() !== "" || bi.value.trim() !== "";
        try { n = parse(fi.value); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); out.textContent = u("bad"); tb.innerHTML = ""; return; }
        if (iv) {
          a = parseFr(ai.value); b = parseFr(bi.value);
          var okI = a && b && a.val() < b.val();
          ai.classList.toggle("bad", !okI); bi.classList.toggle("bad", !okI);
          if (!okI) { out.textContent = u("aBad"); tb.innerHTML = ""; return; }
          a = a.val(); b = b.val();
        } else { ai.classList.remove("bad"); bi.classList.remove("bad"); }
        var S, inf = !iv, note = "";
        try { S = studyF(n, iv ? a : -40, iv ? b : 40); } catch (e) { out.textContent = e instanceof NoDiff ? u("noDiff") : u("bad"); tb.innerHTML = ""; return; }
        if (!iv && S.ev.length > 12) { S = studyF(n, -8, 8); inf = false; note = '<p class="msg-bad">' + u("many") + " " + tex("[-8,8]") + ".</p>"; }
        var z = S.ev.filter(function (e) { return e.k === "z"; });
        var h = "<p>" + tex("f(x)=" + T(n)) + "</p><p>" + tex("f'(x)=" + texD(S.dn)) + "</p>";
        if (S.d2) h += "<p>" + tex("f''(x)=" + texD(S.d2n)) + "</p>";
        h += "<p>" + u("crit") + ": " + (z.length ? tex("x=" + z.map(function (e) { return nn(e.x); }).join(",\\ x=")) : u("noCrit")) + "</p>";
        h += note + monoHtml(S, inf) + extHtml(S);
        var A = null;
        if (iv) { A = absStudy(n, a, b); h += absHtml(A); }
        out.innerHTML = h;
        tb.innerHTML = "<p><strong>" + (iv ? u("inI") + " " + tex("[" + nn(a) + "," + nn(b) + "]") : u("inR")) + "</strong></p>" + signTable(S, inf) + (z.length ? critRows(S) : "");
        var v;
        if (iv) {
          var pad = (b - a) * 0.1, yy = autoY([S.f], a, b), ys = A.c.map(function (q) { return q.y; }).filter(isFinite), dy = (Math.max.apply(null, ys) - Math.min.apply(null, ys)) * 0.08 + 0.5;
          v = [a - pad, b + pad, Math.min(yy[0], Math.min.apply(null, ys) - dy), Math.max(yy[1], Math.max.apply(null, ys) + dy)];
        }
        else v = autoView(S, [-6, 6]);
        plot(svg, { v: v, curves: [{ f: S.f, col: "var(--border)" }].concat(monoCurves(S)), mark: iv ? absMarks(A) : extMarks(S), guides: iv ? [{ x: a }, { x: b }] : [] });
      }
      onLang(draw);
    }

    /* ---------- qüestionari ---------- */
    function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
    var QUIZ = [
      { q: q3("La recta tangent a $f(x)=x^2$ en $x=1$ és…", "La recta tangente a $f(x)=x^2$ en $x=1$ es…", "The tangent line to $f(x)=x^2$ at $x=1$ is…"),
        o: [q3("$y=2x-1$"), q3("$y=2x+1$"), q3("$y=x$")], a: 0, e: q3("$f(1)=1$, $f'(1)=2$: $\\ y-1=2(x-1)\\Rightarrow y=2x-1$.") },
      { q: q3("Si $f'(a)=2$, el pendent de la recta normal en $x=a$ és…", "Si $f'(a)=2$, la pendiente de la recta normal en $x=a$ es…", "If $f'(a)=2$, the slope of the normal line at $x=a$ is…"),
        o: [q3("$2$"), q3("$-2$"), q3("$-\\frac12$")], a: 2, e: q3("$m_n=-\\frac{1}{f'(a)}=-\\frac12$ (perquè $m_t\\cdot m_n=-1$).", "$m_n=-\\frac{1}{f'(a)}=-\\frac12$ (porque $m_t\\cdot m_n=-1$).", "$m_n=-\\frac{1}{f'(a)}=-\\frac12$ (since $m_t\\cdot m_n=-1$).") },
      { q: q3("Si $f'(x)\\gt0$ en tot l'interval $(a,b)$, aleshores $f$ en $(a,b)$ és…", "Si $f'(x)\\gt0$ en todo el intervalo $(a,b)$, entonces $f$ en $(a,b)$ es…", "If $f'(x)\\gt0$ on the whole interval $(a,b)$, then on $(a,b)$ $f$ is…"),
        o: [q3("creixent", "creciente", "increasing"), q3("decreixent", "decreciente", "decreasing"), q3("constant", "constante", "constant")], a: 0,
        e: q3("El pendent de les tangents és positiu: la funció puja.", "La pendiente de las tangentes es positiva: la función sube.", "The tangents have positive slope: the function goes up.") },
      { q: q3("$f(x)=x^3-3x$ és decreixent en…", "$f(x)=x^3-3x$ es decreciente en…", "$f(x)=x^3-3x$ is decreasing on…"),
        o: [q3("$(-\\infty,-1)$"), q3("$(-1,1)$"), q3("$(1,+\\infty)$")], a: 1, e: q3("$f'(x)=3(x+1)(x-1)\\lt0$ entre $-1$ i $1$.", "$f'(x)=3(x+1)(x-1)\\lt0$ entre $-1$ y $1$.", "$f'(x)=3(x+1)(x-1)\\lt0$ between $-1$ and $1$.") },
      { q: q3("Si $f'(a)=0$ i $f''(a)\\lt0$, en $x=a$ hi ha…", "Si $f'(a)=0$ y $f''(a)\\lt0$, en $x=a$ hay…", "If $f'(a)=0$ and $f''(a)\\lt0$, at $x=a$ there is…"),
        o: [q3("un mínim relatiu", "un mínimo relativo", "a relative minimum"), q3("un màxim relatiu", "un máximo relativo", "a relative maximum"), q3("res: cal estudiar la monotonia", "nada: hay que estudiar la monotonía", "nothing: we must study monotonicity")], a: 1,
        e: q3("$f''(a)\\lt0$: la corba és còncava cap avall (∩), és un màxim.", "$f''(a)\\lt0$: la curva es cóncava hacia abajo (∩), es un máximo.", "$f''(a)\\lt0$: the curve bends downwards (∩), so it is a maximum.") },
      { q: q3("$f(x)=x^3$ compleix $f'(0)=0$. En $x=0$…", "$f(x)=x^3$ cumple $f'(0)=0$. En $x=0$…", "$f(x)=x^3$ has $f'(0)=0$. At $x=0$…"),
        o: [q3("té un màxim", "tiene un máximo", "it has a maximum"), q3("té un mínim", "tiene un mínimo", "it has a minimum"), q3("no té cap extrem", "no tiene ningún extremo", "it has no extremum")], a: 2,
        e: q3("$f'(x)=3x^2\\geq0$ no canvia de signe: és creixent abans i després de 0.", "$f'(x)=3x^2\\geq0$ no cambia de signo: es creciente antes y después de 0.", "$f'(x)=3x^2\\geq0$ does not change sign: it increases on both sides of 0.") },
      { q: q3("El mínim relatiu de $f(x)=x^2-6x+10$ és el punt…", "El mínimo relativo de $f(x)=x^2-6x+10$ es el punto…", "The relative minimum of $f(x)=x^2-6x+10$ is the point…"),
        o: [q3("$(3,1)$"), q3("$(3,0)$"), q3("$(-3,37)$")], a: 0, e: q3("$f'(x)=2x-6=0\\Rightarrow x=3$, $f''=2\\gt0$; $\\ f(3)=9-18+10=1$.") },
      { q: q3("Per trobar el màxim absolut d'una funció contínua en $[a,b]$ comparem els valors de $f$…", "Para encontrar el máximo absoluto de una función continua en $[a,b]$ comparamos los valores de $f$…", "To find the absolute maximum of a continuous function on $[a,b]$ we compare the values of $f$…"),
        o: [q3("només en els punts on $f'(x)=0$", "solo en los puntos donde $f'(x)=0$", "only at the points where $f'(x)=0$"), q3("en els punts crítics de dins i en els extrems $a$ i $b$", "en los puntos críticos de dentro y en los extremos $a$ y $b$", "at the critical points inside and at the endpoints $a$ and $b$"), q3("només en $a$ i $b$", "solo en $a$ y $b$", "only at $a$ and $b$")], a: 1,
        e: q3("El màxim absolut pot estar en un extrem de l'interval.", "El máximo absoluto puede estar en un extremo del intervalo.", "The absolute maximum may be at an endpoint.") },
      { q: q3("De tots els rectangles de perímetre 20, el d'àrea màxima té els costats…", "De todos los rectángulos de perímetro 20, el de área máxima tiene los lados…", "Of all rectangles with perimeter 20, the one with the largest area has sides…"),
        o: [q3("$4$ i $6$", "$4$ y $6$", "$4$ and $6$"), q3("$5$ i $5$", "$5$ y $5$", "$5$ and $5$"), q3("$2$ i $8$", "$2$ y $8$", "$2$ and $8$")], a: 1, e: q3("$y=10-x$, $A(x)=10x-x^2$, $A'=10-2x=0\\Rightarrow x=5$: és un quadrat.", "$y=10-x$, $A(x)=10x-x^2$, $A'=10-2x=0\\Rightarrow x=5$: es un cuadrado.", "$y=10-x$, $A(x)=10x-x^2$, $A'=10-2x=0\\Rightarrow x=5$: it is a square.") },
      { q: q3("En un problema d'optimització amb dues variables, el primer pas és…", "En un problema de optimización con dos variables, el primer paso es…", "In an optimisation problem with two variables, the first step is…"),
        o: [q3("derivar i igualar a zero", "derivar e igualar a cero", "differentiate and set equal to zero"), q3("buscar l'equació que relaciona les variables i aïllar-ne una", "buscar la ecuación que relaciona las variables y despejar una", "find the equation linking the variables and solve for one"), q3("fer la segona derivada", "hacer la segunda derivada", "compute the second derivative")], a: 1,
        e: q3("Primer necessitem una funció d'una sola variable: per això fem servir la condició que lliga les dues variables.", "Primero necesitamos una función de una sola variable: para eso usamos la condición que liga las dos variables.", "First we need a function of a single variable: that is what the constraint linking the two variables is for.") }
    ];

    return { UI: UI, QUIZ: QUIZ, ws: [wFigs, function wTan() { wTN("w-tan", false); }, wPar, function wNorm() { wTN("w-norm", true); }, wMono, wExt, wAbs, wOpt, wBuild, wLab] };
  })();
  /* ===================== mòdul de la unitat 7 de 2n Batx CCSS ===================== */
  var M7 = (function () {
    function presetBtns(box, n, key, onPick) { return presetBtnsS(box, n, typeof key === "function" ? key : function () { return u(key); }, onPick); }
    /* ---------- textos de la interfície ---------- */
    var UI = {
      va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
        score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt", pc: "si", rest: "en la resta",
        bad: "No entenc l'expressió: revisa-la.", noDiff: "Aquesta expressió no la sé derivar amb les regles de la unitat.",
        test: "Valor de prova", noDom: "fora del domini", mx: "màx", mn: "mín", incOn: "Creixent en", decOn: "Decreixent en",
        noCrit: "No hi ha cap punt on f′(x) = 0.", maxR: "Màxim relatiu", minR: "Mínim relatiu", noExt: "no és extrem", inc: "creixent", dec: "decreixent",
        cont: "contínua", ev: "evitable", sf: "salt finit", si: "salt infinit", as: "asimptòtica",
        dom: "Domini", den: "Denominador", denZ: "s'anul·la en", denNo: "no s'anul·la mai", lnArg: "Argument del logaritme", lnPos: "ha de ser positiu",
        sqArg: "Dins de l'arrel", sqPos: "no pot ser negatiu", empty: "La funció no existeix per a cap x de la finestra.", noCond: "No hi ha denominadors ni logaritmes: cap restricció.",
        cutX: "Talls amb l'eix OX", cutY: "Tall amb l'eix OY", noCutX: "no talla l'eix OX", noCutY: "no talla l'eix OY (x = 0 no és del domini)",
        sym: "Simetria", even: "parella: simètrica respecte de l'eix OY", odd: "senar: simètrica respecte de l'origen", noSym: "ni parella ni senar", symNoDom: "el domini no és simètric",
        av: "Asímptotes verticals", noAV: "no en té", ah: "Asímptota horitzontal", ao: "Asímptota obliqua", noAsy: "ni horitzontal ni obliqua", branch: "branca parabòlica",
        toL: "quan x → −∞", toR: "quan x → +∞", notTo: "el domini no hi arriba", poly: "És una funció polinòmica: no té asímptotes.",
        quo: "Quocient", rem: "Residu", divide: "Dividim", mult: "multipliquem", subt: "restem",
        dLt: "grau P < grau Q ⇒ asímptota horitzontal y = 0", dEq: "grau P = grau Q ⇒ asímptota horitzontal (quocient dels coeficients principals)",
        dP1: "grau P = grau Q + 1 ⇒ asímptota obliqua: el quocient C(x)", dBig: "grau P > grau Q + 1 ⇒ ni horitzontal ni obliqua (branca parabòlica)",
        above: "la funció queda per damunt de l'asímptota", below: "la funció queda per davall de l'asímptota", notPoly: "Escriu dos polinomis (el denominador no pot ser constant 0).",
        mono: "Monotonia", ext: "Extrems relatius", none: "cap", value: "Valor",
        sNames: ["Domini", "Punts de tall", "Simetria", "Asímptotes", "Monotonia i extrems", "Gràfica"],
        many: "Hi ha molts punts crítics: mostrem l'estudi en la finestra", piece: "Tros", atCut: "En", contAll: "És contínua en tot el domini.",
        latL: "límit per l'esquerra", latR: "límit per la dreta", val: "valor", noExtPw: "No té extrems relatius.",
        pDom: ["Polinòmica", "(x + 1)/(x² − 4)", "1/(x² + 1)", "e^(1/x)", "ln(x − 3)", "ln(x² − 4)", "x / ln x", "√(6 − 2x)", "√(x² − 9)", "x/√(4 − x²)"],
        pCut: ["x³ − 4x", "x² − 2x − 3", "(x² − 1)/(x + 2)", "eˣ − 2", "ln(x + 1)", "x²·eˣ", "√(x² − 4)", "√(x + 3) − x − 1"],
        pSym: ["x⁴ − 3x²", "x³ − 3x", "x/(x² + 1)", "x²/(x² − 1)", "e^(−x²)", "eˣ", "x² + x", "√(9 − x²)", "x·√(x² + 1)", "√(x + 2)"],
        pAsy: ["(2x + 1)/(x − 3)", "x/(x² − 1)", "3x²/(x² + 1)", "2 − e⁻ˣ", "ln(x + 2)", "(x² + 1)/x"],
        pObl: ["(x² + 3)/(x − 1)", "x²/(x + 1)", "(2x² − x + 1)/x", "x³/(x² − 1)", "(x³ + 1)/x", "(3x² + 1)/(x² − 4)"],
        pMx: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "x·eˣ", "ln x / x"],
        pEl: ["a·eˣ⁻ʰ + k", "a·(1/2)ˣ⁻ʰ + k", "a·ln(x − h) + k"],
        pPw: ["Exemple resolt", "Amb un salt", "Exponencial i logaritme", "Racional i recta"],
        pLab: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "(2x − 1)/(x + 1)", "x·eˣ", "eˣ/x", "ln x / x"] },
      es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
        score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba", pc: "si", rest: "en el resto",
        bad: "No entiendo la expresión: revísala.", noDiff: "Esta expresión no la sé derivar con las reglas de la unidad.",
        test: "Valor de prueba", noDom: "fuera del dominio", mx: "máx", mn: "mín", incOn: "Creciente en", decOn: "Decreciente en",
        noCrit: "No hay ningún punto donde f′(x) = 0.", maxR: "Máximo relativo", minR: "Mínimo relativo", noExt: "no es extremo", inc: "creciente", dec: "decreciente",
        cont: "continua", ev: "evitable", sf: "salto finito", si: "salto infinito", as: "asintótica",
        dom: "Dominio", den: "Denominador", denZ: "se anula en", denNo: "no se anula nunca", lnArg: "Argumento del logaritmo", lnPos: "tiene que ser positivo",
        sqArg: "Dentro de la raíz", sqPos: "no puede ser negativo", empty: "La función no existe para ninguna x de la ventana.", noCond: "No hay denominadores ni logaritmos: ninguna restricción.",
        cutX: "Cortes con el eje OX", cutY: "Corte con el eje OY", noCutX: "no corta el eje OX", noCutY: "no corta el eje OY (x = 0 no es del dominio)",
        sym: "Simetría", even: "par: simétrica respecto del eje OY", odd: "impar: simétrica respecto del origen", noSym: "ni par ni impar", symNoDom: "el dominio no es simétrico",
        av: "Asíntotas verticales", noAV: "no tiene", ah: "Asíntota horizontal", ao: "Asíntota oblicua", noAsy: "ni horizontal ni oblicua", branch: "rama parabólica",
        toL: "cuando x → −∞", toR: "cuando x → +∞", notTo: "el dominio no llega", poly: "Es una función polinómica: no tiene asíntotas.",
        quo: "Cociente", rem: "Resto", divide: "Dividimos", mult: "multiplicamos", subt: "restamos",
        dLt: "grado P < grado Q ⇒ asíntota horizontal y = 0", dEq: "grado P = grado Q ⇒ asíntota horizontal (cociente de los coeficientes principales)",
        dP1: "grado P = grado Q + 1 ⇒ asíntota oblicua: el cociente C(x)", dBig: "grado P > grado Q + 1 ⇒ ni horizontal ni oblicua (rama parabólica)",
        above: "la función queda por encima de la asíntota", below: "la función queda por debajo de la asíntota", notPoly: "Escribe dos polinomios (el denominador no puede ser constante 0).",
        mono: "Monotonía", ext: "Extremos relativos", none: "ninguno", value: "Valor",
        sNames: ["Dominio", "Puntos de corte", "Simetría", "Asíntotas", "Monotonía y extremos", "Gráfica"],
        many: "Hay muchos puntos críticos: mostramos el estudio en la ventana", piece: "Trozo", atCut: "En", contAll: "Es continua en todo el dominio.",
        latL: "límite por la izquierda", latR: "límite por la derecha", val: "valor", noExtPw: "No tiene extremos relativos.",
        pDom: ["Polinómica", "(x + 1)/(x² − 4)", "1/(x² + 1)", "e^(1/x)", "ln(x − 3)", "ln(x² − 4)", "x / ln x", "√(6 − 2x)", "√(x² − 9)", "x/√(4 − x²)"],
        pCut: ["x³ − 4x", "x² − 2x − 3", "(x² − 1)/(x + 2)", "eˣ − 2", "ln(x + 1)", "x²·eˣ", "√(x² − 4)", "√(x + 3) − x − 1"],
        pSym: ["x⁴ − 3x²", "x³ − 3x", "x/(x² + 1)", "x²/(x² − 1)", "e^(−x²)", "eˣ", "x² + x", "√(9 − x²)", "x·√(x² + 1)", "√(x + 2)"],
        pAsy: ["(2x + 1)/(x − 3)", "x/(x² − 1)", "3x²/(x² + 1)", "2 − e⁻ˣ", "ln(x + 2)", "(x² + 1)/x"],
        pObl: ["(x² + 3)/(x − 1)", "x²/(x + 1)", "(2x² − x + 1)/x", "x³/(x² − 1)", "(x³ + 1)/x", "(3x² + 1)/(x² − 4)"],
        pMx: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "x·eˣ", "ln x / x"],
        pEl: ["a·eˣ⁻ʰ + k", "a·(1/2)ˣ⁻ʰ + k", "a·ln(x − h) + k"],
        pPw: ["Ejemplo resuelto", "Con un salto", "Exponencial y logaritmo", "Racional y recta"],
        pLab: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "(2x − 1)/(x + 1)", "x·eˣ", "eˣ/x", "ln x / x"] },
      en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
        score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top", pc: "if", rest: "otherwise",
        bad: "I can't read that expression: check it.", noDiff: "I can't differentiate this with the rules of the unit.",
        test: "Test value", noDom: "outside the domain", mx: "max", mn: "min", incOn: "Increasing on", decOn: "Decreasing on",
        noCrit: "There is no point where f′(x) = 0.", maxR: "Relative maximum", minR: "Relative minimum", noExt: "not an extremum", inc: "increasing", dec: "decreasing",
        cont: "continuous", ev: "removable", sf: "finite jump", si: "infinite jump", as: "asymptotic",
        dom: "Domain", den: "Denominator", denZ: "is zero at", denNo: "is never zero", lnArg: "Argument of the logarithm", lnPos: "must be positive",
        sqArg: "Inside the root", sqPos: "cannot be negative", empty: "The function does not exist for any x in the window.", noCond: "No denominators or logarithms: no restrictions.",
        cutX: "x-intercepts", cutY: "y-intercept", noCutX: "it does not cross the x-axis", noCutY: "it does not cross the y-axis (x = 0 is not in the domain)",
        sym: "Symmetry", even: "even: symmetric about the y-axis", odd: "odd: symmetric about the origin", noSym: "neither even nor odd", symNoDom: "the domain is not symmetric",
        av: "Vertical asymptotes", noAV: "none", ah: "Horizontal asymptote", ao: "Oblique asymptote", noAsy: "neither horizontal nor oblique", branch: "parabolic branch",
        toL: "as x → −∞", toR: "as x → +∞", notTo: "the domain does not reach it", poly: "It is a polynomial: it has no asymptotes.",
        quo: "Quotient", rem: "Remainder", divide: "Divide", mult: "multiply", subt: "subtract",
        dLt: "deg P < deg Q ⇒ horizontal asymptote y = 0", dEq: "deg P = deg Q ⇒ horizontal asymptote (ratio of the leading coefficients)",
        dP1: "deg P = deg Q + 1 ⇒ oblique asymptote: the quotient C(x)", dBig: "deg P > deg Q + 1 ⇒ neither horizontal nor oblique (parabolic branch)",
        above: "the function lies above the asymptote", below: "the function lies below the asymptote", notPoly: "Type two polynomials (the denominator cannot be the constant 0).",
        mono: "Monotonicity", ext: "Relative extrema", none: "none", value: "Value",
        sNames: ["Domain", "Intercepts", "Symmetry", "Asymptotes", "Monotonicity and extrema", "Graph"],
        many: "There are many critical points: the study is shown for the window", piece: "Piece", atCut: "At", contAll: "It is continuous on its whole domain.",
        latL: "left-hand limit", latR: "right-hand limit", val: "value", noExtPw: "It has no relative extrema.",
        pDom: ["Polynomial", "(x + 1)/(x² − 4)", "1/(x² + 1)", "e^(1/x)", "ln(x − 3)", "ln(x² − 4)", "x / ln x", "√(6 − 2x)", "√(x² − 9)", "x/√(4 − x²)"],
        pCut: ["x³ − 4x", "x² − 2x − 3", "(x² − 1)/(x + 2)", "eˣ − 2", "ln(x + 1)", "x²·eˣ", "√(x² − 4)", "√(x + 3) − x − 1"],
        pSym: ["x⁴ − 3x²", "x³ − 3x", "x/(x² + 1)", "x²/(x² − 1)", "e^(−x²)", "eˣ", "x² + x", "√(9 − x²)", "x·√(x² + 1)", "√(x + 2)"],
        pAsy: ["(2x + 1)/(x − 3)", "x/(x² − 1)", "3x²/(x² + 1)", "2 − e⁻ˣ", "ln(x + 2)", "(x² + 1)/x"],
        pObl: ["(x² + 3)/(x − 1)", "x²/(x + 1)", "(2x² − x + 1)/x", "x³/(x² − 1)", "(x³ + 1)/x", "(3x² + 1)/(x² − 4)"],
        pMx: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "x·eˣ", "ln x / x"],
        pEl: ["a·eˣ⁻ʰ + k", "a·(1/2)ˣ⁻ʰ + k", "a·ln(x − h) + k"],
        pPw: ["Worked example", "With a jump", "Exponential and log", "Rational and line"],
        pLab: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "(2x − 1)/(x + 1)", "x·eˣ", "eˣ/x", "ln x / x"] }
    };
    function u(k) { return (UI[lang] || UI.va)[k]; }
    function t3(va, es, en) { return lang === "es" ? es : lang === "en" ? en : va; }


    /* ---------- domini (numèricament, amb l'ajuda de l'expressió) ---------- */
    var XL = 40; // finestra d'estudi: [−40, 40]
    // denominadors, arguments de logaritmes i d'arrels de l'expressió
    function condsOf(n, out) {
      out = out || { den: [], ln: [], sq: [] };
      if (!n || typeof n !== "object") return out;
      if (n.t === "/") out.den.push(n.b);
      if (n.t === "f" && (n.n === "ln" || n.n === "log")) out.ln.push(n.a);
      if (n.t === "f" && n.n === "sqrt") out.sq.push(n.a);
      if (n.a) condsOf(n.a, out);
      if (n.b) condsOf(n.b, out);
      return out;
    }
    // dom: {iv:[{a,b,aInf,bInf,ai,bi}], ex:[punts exclosos dins dels intervals]}
    function domainOf(f, dens) {
      var N = 8000, h = 2 * XL / N, X = [], OK = [], i, runs = [], cur = null, holes = [];
      for (i = 0; i <= N; i++) { X.push(-XL + i * h); OK.push(isFinite(f(X[i]))); }
      // un sol punt fora (un forat) no talla el tram: és un punt exclòs
      for (i = 1; i < N; i++) if (!OK[i] && OK[i - 1] && OK[i + 1]) { OK[i] = true; holes.push(snap(X[i])); }
      for (i = 0; i <= N; i++) { if (OK[i]) { if (!cur) { cur = { i0: i }; runs.push(cur); } cur.i1 = i; } else cur = null; }
      function edge(xIn, xOut) {
        for (var it = 0; it < 80; it++) { var m = (xIn + xOut) / 2; if (isFinite(f(m))) xIn = m; else xOut = m; }
        return snap((xIn + xOut) / 2);
      }
      function far(s) { return [1e2, 1e3, 1e6].some(function (v) { return !isNaN(f(s * v)); }); }
      var iv = [];
      runs.forEach(function (r) {
        if (r.i1 - r.i0 < 2) return;
        var o = { aInf: false, bInf: false };
        if (r.i0 > 0) o.a = edge(X[r.i0], X[r.i0 - 1]); else if (far(-1)) o.aInf = true; else o.a = edge(X[0], -1e2);
        if (r.i1 < N) o.b = edge(X[r.i1], X[r.i1 + 1]); else if (far(1)) o.bInf = true; else o.b = edge(X[N], 1e2);
        o.ai = !o.aInf && isFinite(f(o.a)); o.bi = !o.bInf && isFinite(f(o.b));
        iv.push(o);
      });
      var ex = [];
      function inside(p) { return iv.some(function (o) { return (o.aInf || p > o.a + 1e-9) && (o.bInf || p < o.b - 1e-9); }); }
      function addEx(p) { if (!inside(p)) return; for (var k = 0; k < ex.length; k++) if (Math.abs(ex[k] - p) < 1e-6 * (1 + Math.abs(p))) return; ex.push(p); }
      (dens || []).forEach(function (g) { roots(g, -XL, XL).forEach(addEx); });
      holes.forEach(addEx);
      ex.sort(function (p, q) { return p - q; });
      return { iv: iv, ex: ex };
    }
    function inDom(Dm, x) {
      if (Dm.ex.some(function (p) { return Math.abs(p - x) < 1e-9; })) return false;
      return Dm.iv.some(function (o) { return (o.aInf || x > o.a || (o.ai && x === o.a)) && (o.bInf || x < o.b || (o.bi && x === o.b)); });
    }
    // trams del domini (separats pels punts exclosos)
    function domParts(Dm) {
      var out = [];
      Dm.iv.forEach(function (o) {
        var pts = Dm.ex.filter(function (p) { return (o.aInf || p > o.a) && (o.bInf || p < o.b); });
        var bs = [o.aInf ? -Infinity : o.a].concat(pts).concat([o.bInf ? Infinity : o.b]);
        for (var k = 0; k + 1 < bs.length; k++) out.push({ a: bs[k], b: bs[k + 1], ai: k === 0 && o.ai, bi: k + 2 === bs.length && o.bi });
      });
      return out;
    }
    function domTex(Dm) {
      if (!Dm.iv.length) return "\\varnothing";
      if (Dm.iv.length === 1 && Dm.iv[0].aInf && Dm.iv[0].bInf) return Dm.ex.length ? "\\mathbb R-\\{" + Dm.ex.map(nn).join(",\\,") + "\\}" : "\\mathbb R";
      return domParts(Dm).map(function (p) {
        return (p.ai ? "[" : "(") + (isFinite(p.a) ? nn(p.a) : "-\\infty") + "," + (isFinite(p.b) ? nn(p.b) : "+\\infty") + (p.bi ? "]" : ")");
      }).join("\\cup ");
    }
    // zones que no són del domini (per a ombrejar-les)
    function domBands(Dm) {
      var out = [], P = Dm.iv;
      if (!P.length) return [{ a: -1e9, b: 1e9 }];
      if (!P[0].aInf) out.push({ a: -1e9, b: P[0].a });
      for (var k = 0; k + 1 < P.length; k++) out.push({ a: P[k].b, b: P[k + 1].a });
      if (!P[P.length - 1].bInf) out.push({ a: P[P.length - 1].b, b: 1e9 });
      return out;
    }
    // zeros de g, també els de la vora del domini (com en sqrt(x^2-4) per a x=±2), on roots() no veu canvi de signe
    function zerosOf(g) {
      var r = roots(g, -XL, XL);
      domainOf(g, []).iv.forEach(function (o) {
        [o.aInf || !o.ai ? NaN : o.a, o.bInf || !o.bi ? NaN : o.b].forEach(function (p) {
          if (isFinite(p) && Math.abs(g(p)) < 1e-7 && !r.some(function (q) { return Math.abs(q - p) < 1e-6 * (1 + Math.abs(p)); })) r.push(p);
        });
      });
      return r.sort(function (p, q) { return p - q; });
    }
    // explicació: on s'anul·len els denominadors i on són positius els arguments dels logaritmes
    function signSet(g, test) {
      return domTex(domainOf(function (x) { var v = g(x); return test(v) ? 1 : NaN; }, []));
    }
    function domWhy(n) {
      var C = condsOf(n), h = [];
      C.den.forEach(function (d) {
        var g = compile(d), r = zerosOf(g);
        if (strip(d).t === "n" || strip(d).t === "c") return;
        h.push("<li>" + u("den") + " " + tex(T(d)) + ": " + (r.length ? u("denZ") + " " + tex("x=" + r.map(nn).join(",\\ x=")) : u("denNo")) + "</li>");
      });
      C.ln.forEach(function (a) {
        var g = compile(a);
        h.push("<li>" + u("lnArg") + " " + u("lnPos") + ": " + tex(T(a) + "\\gt0\\ \\Leftrightarrow\\ x\\in " + signSet(g, function (v) { return v > 1e-12; })) + "</li>");
      });
      C.sq.forEach(function (a) {
        var g = compile(a);
        h.push("<li>" + u("sqArg") + " " + u("sqPos") + ": " + tex(T(a) + "\\geq0\\ \\Leftrightarrow\\ x\\in " + signSet(g, function (v) { return v > -1e-12; })) + "</li>");
      });
      return h.length ? "<ul>" + h.join("") + "</ul>" : "<p>" + u("noCond") + "</p>";
    }

    /* ---------- punts de tall, simetria i asímptotes ---------- */
    function cutsOf(f, Dm) {
      var y0 = inDom(Dm, 0) ? f(0) : NaN;
      var xs = zerosOf(f).filter(function (x) { return inDom(Dm, x) && Math.abs(f(x)) < 1e-7; });
      return { oy: isFinite(y0) ? (Math.abs(y0) < 1e-12 ? 0 : y0) : null, ox: xs };
    }
    function cutsHtml(C) {
      return "<p><strong>" + u("cutX") + ":</strong> " + (C.ox.length ? tex("f(x)=0\\ \\Rightarrow\\ " + C.ox.map(function (x) { return "(" + nn(x) + ",0)"; }).join(",\\ ")) : u("noCutX")) +
        "<br><strong>" + u("cutY") + ":</strong> " + (C.oy !== null ? tex("x=0\\ \\Rightarrow\\ f(0)=" + nn(C.oy) + "\\ \\Rightarrow\\ (0," + nn(C.oy) + ")") : u("noCutY")) + "</p>";
    }
    function cutPts(C) {
      var p = C.ox.map(function (x) { return { x: x, y: 0, col: "var(--accent-2)" }; });
      if (C.oy !== null) p.push({ x: 0, y: C.oy, col: "var(--accent-2)" });
      return p;
    }
    var SYM_X = [0.37, 0.81, 1.23, 1.9, 2.71, 3.3, 4.6, 6.1, 7.7, 11.3];
    function symOf(f) {
      var ev = true, od = true, any = false;
      for (var i = 0; i < SYM_X.length; i++) {
        var x = SYM_X[i], a = f(x), b = f(-x);
        if (isFinite(a) !== isFinite(b)) return "dom";
        if (!isFinite(a)) continue;
        any = true;
        var tol = 1e-9 * (1 + Math.abs(a));
        if (Math.abs(a - b) > tol) ev = false;
        if (Math.abs(a + b) > tol) od = false;
      }
      if (!any) return "none";
      return ev ? "even" : od ? "odd" : "none";
    }
    function symTxt(s) { return s === "even" ? u("even") : s === "odd" ? u("odd") : s === "dom" ? u("noSym") + " (" + u("symNoDom") + ")" : u("noSym"); }
    // fracció exacta P/Q, si ho és
    function ratOf(n) {
      try { return { P: pTrim(polyOf(n)), Q: [new Fr(1)] }; } catch (e) {}
      n = strip(n);
      if (n.t !== "/") return null;
      try { var P = pTrim(polyOf(n.a)), Q = pTrim(polyOf(n.b)); if (pDeg(Q) === 0 && Q[0].zero()) return null; return { P: P, Q: Q }; } catch (e) { return null; }
    }
    // divisió de polinomis (coeficients de grau 0..n), amb els passos
    function pDiv(P, Q) {
      var r = pTrim(P), dq = pDeg(Q), lq = Q[dq], q = [new Fr(0)], steps = [];
      function isZ(p) { return pDeg(p) === 0 && p[0].zero(); }
      while (!isZ(r) && pDeg(r) >= dq) {
        var k = pDeg(r) - dq, c = r[pDeg(r)].div(lq), mono = [];
        for (var j = 0; j < k; j++) mono.push(new Fr(0));
        mono.push(c);
        while (q.length <= k) q.push(new Fr(0));
        q[k] = c;
        var sub = pMul(mono, Q), nr = pAdd(r, sub, -1);
        if (pDeg(nr) >= pDeg(r) && !isZ(nr)) nr = pTrim(nr.slice(0, pDeg(r))); // el terme principal s'anul·la sempre
        steps.push({ r: r, m: mono, s: sub, n: nr });
        r = nr;
      }
      return { q: pTrim(q), r: r, steps: steps };
    }
    function pFn(p) { return function (x) { var v = 0; for (var i = p.length - 1; i >= 0; i--) v = v * x + p[i].val(); return v; }; }
    // asímptotes: verticals (límits laterals) i, en cada costat, horitzontal / obliqua / cap
    function asyOf(f, Dm, n, rat0) {
      var cand = [];
      function add(c) { if (!cand.some(function (p) { return Math.abs(p - c) < 1e-7; })) cand.push(c); }
      Dm.iv.forEach(function (o) { if (!o.aInf) add(o.a); if (!o.bInf) add(o.b); });
      Dm.ex.forEach(add);
      cand.sort(function (p, q) { return p - q; });
      var av = [];
      cand.forEach(function (c) {
        var L = isFinite(f(c - 1e-6)) ? limSide(f, c, -1) : null, R = isFinite(f(c + 1e-6)) ? limSide(f, c, 1) : null;
        if ((L && L.k === "inf") || (R && R.k === "inf")) av.push({ x: c, L: L, R: R });
      });
      var rat = rat0 || (n ? ratOf(n) : null), side = {};
      [-1, 1].forEach(function (s) {
        var P = Dm.iv[s < 0 ? 0 : Dm.iv.length - 1];
        if (!P || !(s < 0 ? P.aInf : P.bInf)) { side[s] = { k: "no" }; return; }
        if (rat) {
          var dP = pDeg(rat.P), dQ = pDeg(rat.Q);
          if (dQ === 0) { side[s] = { k: "p" }; return; }
          if (dP < dQ) { side[s] = { k: "h", y: 0 }; return; }
          if (dP === dQ) { side[s] = { k: "h", y: rat.P[dP].div(rat.Q[dQ]).val() }; return; }
          if (dP === dQ + 1) { var Dv = pDiv(rat.P, rat.Q); side[s] = { k: "o", m: Dv.q[1].val(), n: Dv.q[0].val() }; return; }
          side[s] = { k: "p" }; return;
        }
        var L = limSide(f, s * Infinity, s);
        if (L.k === "num") { side[s] = { k: "h", y: snap(Math.abs(L.v) < 1e-5 ? 0 : L.v) }; return; }
        if (L.k !== "inf") { side[s] = { k: "none" }; return; }
        var M = limSide(function (x) { return f(x) / x; }, s * Infinity, s);
        if (M.k === "num" && Math.abs(M.v) > 1e-6) {
          var m = snap(M.v), Nn = limSide(function (x) { return f(x) - m * x; }, s * Infinity, s);
          if (Nn.k === "num") { side[s] = { k: "o", m: m, n: snap(Math.abs(Nn.v) < 1e-5 ? 0 : Nn.v) }; return; }
        }
        side[s] = { k: "p" };
      });
      return { av: av, side: side, rat: rat };
    }
    function lineTx(m, b) { return lineT(m, 0, b); }
    function sideTx(o) {
      if (o.k === "h") return u("ah") + " " + tex("y=" + nn(o.y));
      if (o.k === "o") return u("ao") + " " + tex(lineTx(o.m, o.n));
      if (o.k === "no") return u("notTo");
      return u("noAsy") + (o.k === "p" ? " (" + u("branch") + ")" : "");
    }
    function avHtml(A) {
      if (!A.av.length) return u("noAV");
      return A.av.map(function (q) {
        var l = [];
        if (q.L) l.push(tex("\\lim_{x\\to " + nn(q.x) + "^-}f(x)=" + limTex(q.L)));
        if (q.R) l.push(tex("\\lim_{x\\to " + nn(q.x) + "^+}f(x)=" + limTex(q.R)));
        return tex("x=" + nn(q.x)) + " &nbsp;(" + l.join(",&ensp;") + ")";
      }).join("<br>");
    }
    function asyHtml(A, poly) {
      if (poly) return "<p>" + u("poly") + "</p>";
      var sL = A.side[-1], sR = A.side[1], same = sL.k === sR.k && (sL.k === "h" ? Math.abs(sL.y - sR.y) < 1e-9 : sL.k === "o" ? Math.abs(sL.m - sR.m) + Math.abs(sL.n - sR.n) < 1e-9 : true);
      var h = "<p><strong>" + u("av") + ":</strong> " + avHtml(A) + "</p><p>";
      h += same ? sideTx(sL) + " (" + u("toL") + " " + t3("i", "y", "and") + " " + u("toR").replace(/^(quan|cuando|as) /, "") + ")" : u("toL").replace(/^./, function (c) { return c.toUpperCase(); }) + ": " + sideTx(sL) + "<br>" + u("toR").replace(/^./, function (c) { return c.toUpperCase(); }) + ": " + sideTx(sR);
      return h + "</p>";
    }
    function asyPlot(A) {
      var ha = [], oa = [];
      [-1, 1].forEach(function (s) {
        var o = A.side[s];
        if (o.k === "h" && ha.indexOf(o.y) < 0) ha.push(o.y);
        if (o.k === "o" && !oa.some(function (q) { return q.m === o.m && q.n === o.n; })) oa.push({ m: o.m, n: o.n });
      });
      return { va: A.av.map(function (q) { return q.x; }), ha: ha, oa: oa };
    }
    // finestra que mostra els elements importants
    function viewOf(f, xs, ys, def) {
      xs = xs.filter(isFinite); ys = ys.filter(isFinite);
      var x0 = xs.length ? Math.min.apply(null, xs) - 3 : def[0], x1 = xs.length ? Math.max.apply(null, xs) + 3 : def[1];
      if (x1 - x0 < 8) { var c = (x0 + x1) / 2; x0 = c - 4; x1 = c + 4; }
      var yy = autoY([f], x0, x1);
      if (ys.length) {
        // els punts destacats han de cabre bé, però sense que les asímptotes verticals aplanen la corba
        var lo = Math.min.apply(null, ys), hi = Math.max.apply(null, ys), sp = Math.max(hi - lo, 2);
        yy = [Math.min(Math.max(yy[0], lo - 2.5 * sp), lo - 0.8 * sp), Math.max(Math.min(yy[1], hi + 2.5 * sp), hi + 0.8 * sp)];
      }
      return [x0, x1, yy[0], yy[1]];
    }

    /* ---------- estudi complet ---------- */
    function fullStudy(n) {
      var f = compile(n), C = condsOf(n), Dm = domainOf(f, C.den.map(compile));
      var R = { n: n, f: f, Dm: Dm, poly: false };
      try { polyOf(n); R.poly = true; } catch (e) {}
      R.cuts = cutsOf(f, Dm); R.sym = symOf(f); R.A = asyOf(f, Dm, n);
      try { R.S = studyF(n, -XL, XL); R.inf = true; if (R.S.ev.length > 14) { R.S = studyF(n, -8, 8); R.inf = false; } } catch (e) { if (!(e instanceof NoDiff)) throw e; R.S = null; }
      var xs = R.cuts.ox.concat(R.A.av.map(function (q) { return q.x; })), ys = [];
      if (R.cuts.oy !== null) { xs.push(0); ys.push(R.cuts.oy); }
      Dm.iv.forEach(function (o) { if (!o.aInf && Math.abs(o.a) < XL) xs.push(o.a); if (!o.bInf && Math.abs(o.b) < XL) xs.push(o.b); });
      if (R.S) R.S.ev.forEach(function (e) { if (e.k === "z" && e.t1 !== "none") { xs.push(e.x); ys.push(e.y); } });
      [-1, 1].forEach(function (s) { if (R.A.side[s].k === "h") ys.push(R.A.side[s].y); });
      R.view = viewOf(f, xs, ys, [-6, 6]);
      return R;
    }

    /* ---------- figures estàtiques ---------- */
    var PWF = {
      ex: { p: ["x+3", "x^2+1", "2/x"], c: [-1, 1] },
      jump: { p: ["x^2", "4-x"], c: [1] },
      el: { p: ["e^x", "ln(x+1)+1"], c: [0] },
      rat: { p: ["1/(x+2)", "x/2+1/2"], c: [0] }
    };
    var FIGS = {
      par: function () {
        var f = F("x^4/8-x^2+2.5"), a = 1.7, ya = f(a);
        return { v: [-3, 3, -0.5, 4], curves: [{ f: f }, { f: function () { return ya; }, a: -a, b: a, col: "var(--accent-2)" }], pts: [{ x: -a, y: ya }, { x: a, y: ya }], guides: [{ x: 0 }],
          labels: [{ x: -a, y: ya + 0.45, t: "(−a, f(a))" }, { x: a, y: ya + 0.45, t: "(a, f(a))" }] };
      },
      sen: function () {
        var f = F("x^3/3-x"), a = 2.1, ya = f(a);
        return { v: [-3, 3, -2.5, 2.5], curves: [{ f: f }, { f: lineF(ya / a, 0, 0), a: -a, b: a, col: "var(--accent-2)" }], pts: [{ x: -a, y: -ya }, { x: a, y: ya }, { x: 0, y: 0, col: "var(--accent-2)" }],
          labels: [{ x: a - 0.1, y: ya + 0.35, t: "(a, f(a))", anchor: "end" }, { x: -a + 0.1, y: -ya - 0.55, t: "(−a, −f(a))", anchor: "start" }] };
      },
      asV: function () {
        return { v: [-3, 7, -4, 6], curves: [{ f: F("1/(x-2)+1") }], va: [2], ha: [1],
          labels: [{ x: 2.15, y: 5.3, t: "x = 2", anchor: "start" }, { x: -2.8, y: 1.35, t: "y = 1", anchor: "start" }] };
      },
      asO: function () {
        return { v: [-7, 9, -12, 16], curves: [{ f: F("(x^2+3)/(x-1)") }], va: [1], oa: [{ m: 1, n: 1 }],
          labels: [{ x: 1.3, y: 14.5, t: "x = 1", anchor: "start" }, { x: 8.6, y: 7.5, t: "y = x + 1", anchor: "end" }] };
      },
      expo: function () {
        return { v: [-4, 4, -1, 5], curves: [{ f: F("e^x") }, { f: F("(1/2)^x"), col: "var(--r3)" }], ha: [0], pts: [{ x: 0, y: 1, col: "var(--text)" }],
          labels: [{ x: 1.75, y: 4.5, t: "y = eˣ", anchor: "end" }, { x: -2.4, y: 4.5, t: "y = (1/2)ˣ", anchor: "start" }] };
      },
      loga: function () {
        return { v: [-1, 7, -3.5, 3.5], curves: [{ f: F("ln(x)") }, { f: F("-ln(x)/ln(2)"), col: "var(--r3)" }], va: [0], pts: [{ x: 1, y: 0, col: "var(--text)" }],
          labels: [{ x: 6.8, y: 2.3, t: "y = ln x", anchor: "end" }, { x: 6.8, y: -2.3, t: "y = log₁/₂ x", anchor: "end" }] };
      },
      ex1: function () {
        return { v: [-1, 4.5, -2, 6], curves: [{ f: F("x^3-6x^2+9x") }], pts: [{ x: 0, y: 0, col: "var(--accent-2)" }, { x: 3, y: 0, col: "var(--accent-2)" }],
          mark: [{ x: 1, y: 4, col: "var(--ok)" }, { x: 3, y: 0, col: "var(--bad)" }], labels: [{ x: 1, y: 4.7, t: "(1, 4)" }, { x: 3.2, y: -0.8, t: "(3, 0)" }] };
      },
      ex2: function () {
        var r = Math.SQRT2;
        return { v: [-2.2, 2.2, -1.6, 3], curves: [{ f: F("x^4-2x^2") }], pts: [{ x: -r, y: 0, col: "var(--accent-2)" }, { x: r, y: 0, col: "var(--accent-2)" }],
          mark: [{ x: 0, y: 0, col: "var(--ok)" }, { x: -1, y: -1, col: "var(--bad)" }, { x: 1, y: -1, col: "var(--bad)" }],
          labels: [{ x: -1, y: -1.45, t: "(−1, −1)" }, { x: 1, y: -1.45, t: "(1, −1)" }, { x: 0, y: 0.35, t: "(0, 0)" }] };
      },
      ex3: function () {
        return { v: [-6, 6, -5, 6], curves: [{ f: F("x^2/(x^2-4)") }], va: [-2, 2], ha: [1], mark: [{ x: 0, y: 0, col: "var(--ok)" }],
          labels: [{ x: -5.8, y: 1.45, t: "y = 1", anchor: "start" }, { x: -2.15, y: 5.3, t: "x = −2", anchor: "end" }, { x: 2.15, y: 5.3, t: "x = 2", anchor: "start" }] };
      },
      ex4: function () {
        return { v: [-7, 9, -12, 16], curves: [{ f: F("(x^2+3)/(x-1)") }], va: [1], oa: [{ m: 1, n: 1 }], pts: [{ x: 0, y: -3, col: "var(--accent-2)" }],
          mark: [{ x: -1, y: -2, col: "var(--ok)" }, { x: 3, y: 6, col: "var(--bad)" }], labels: [{ x: -1.3, y: -0.6, t: "(−1, −2)", anchor: "end" }, { x: 3.4, y: 4.4, t: "(3, 6)", anchor: "start" }, { x: 8.6, y: 7.5, t: "y = x + 1", anchor: "end" }] };
      },
      ex5: function () {
        return { v: [-6, 1.5, -1, 3], curves: [{ f: F("x*e^x") }], ha: [0], pts: [{ x: 0, y: 0, col: "var(--accent-2)" }], mark: [{ x: -1, y: -1 / Math.E, col: "var(--bad)" }],
          labels: [{ x: -1, y: -0.75, t: "(−1, −1/e)" }] };
      },
      ex6: function () {
        return { v: [-0.5, 12, -2, 1], curves: [{ f: F("ln(x)/x") }], va: [0], ha: [0], pts: [{ x: 1, y: 0, col: "var(--accent-2)" }], mark: [{ x: Math.E, y: 1 / Math.E, col: "var(--ok)" }],
          labels: [{ x: Math.E, y: 0.62, t: "(e, 1/e)" }] };
      },
      ex7: function () {
        var P = pwMake(PWF.ex), v = [-5, 6, -1, 4], d = pwDraw(P, v);
        return { v: v, curves: d.curves, pts: d.pts, ha: [0], mark: [{ x: -1, y: 2, col: "var(--ok)" }, { x: 0, y: 1, col: "var(--bad)" }, { x: 1, y: 2, col: "var(--ok)" }],
          labels: [{ x: -1, y: 2.5, t: "(−1, 2)" }, { x: 0, y: 0.45, t: "(0, 1)" }, { x: 1.2, y: 2.5, t: "(1, 2)", anchor: "start" }] };
      }
    };
    function wFigs() {
      document.querySelectorAll("[data-g]").forEach(function (el) {
        var mk = FIGS[el.getAttribute("data-g")]; if (!mk) return;
        var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("class", "lp-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Gràfica");
        el.appendChild(svg);
        onLang(function () { plot(svg, mk()); });
      });
    }

    /* ---------- ginys amb una funció escrita ---------- */
    // esquelet comú: botons d'exemples, camp f(x) i redibuix en canviar
    function fnWidget(id, PRE, key, draw) {
      var w = document.getElementById(id); if (!w) return;
      var fi = $(w, "f"), st = 0;
      presetBtns($(w, "presets"), PRE.length, key, function (i) { st = i; fi.value = PRE[i]; go(); });
      fi.addEventListener("input", function () { st = -1; go(); });
      function go() {
        var n;
        try { n = parse(fi.value); compile(n)(1); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); w.querySelector(".info").textContent = u("bad"); return; }
        draw(w, n, st);
      }
      onLang(go);
    }
    function wDom() {
      fnWidget("w-dom", ["x^3-2x", "(x+1)/(x^2-4)", "1/(x^2+1)", "e^(1/x)", "ln(x-3)", "ln(x^2-4)", "x/ln(x)", "sqrt(6-2x)", "sqrt(x^2-9)", "x/sqrt(4-x^2)"], "pDom", function (w, n) {
        var f = compile(n), Dm = domainOf(f, condsOf(n).den.map(compile)), v = viewOf(f, Dm.ex.concat(Dm.iv.map(function (o) { return o.aInf ? NaN : o.a; })).concat(Dm.iv.map(function (o) { return o.bInf ? NaN : o.b; })), [], [-6, 6]);
        w.querySelector(".info").innerHTML = "<p>" + tex("f(x)=" + T(n)) + "</p>" + domWhy(n) + "<p><strong>" + u("dom") + ":</strong> " + (Dm.iv.length ? tex("\\mathrm{Dom}\\,f=" + domTex(Dm)) : u("empty")) + "</p>";
        plot(w.querySelector("svg.lp-svg"), { v: v, band: domBands(Dm), curves: [{ f: f }], va: Dm.ex.filter(function (p) { return !isFinite(f(p - 1e-6)) || Math.abs(f(p - 1e-6)) > 1e4; }), pts: Dm.iv.reduce(function (a, o) {
          if (!o.aInf && isFinite(f(o.a))) a.push({ x: o.a, y: f(o.a) }); if (!o.bInf && isFinite(f(o.b))) a.push({ x: o.b, y: f(o.b) }); return a; }, []) });
      });
    }
    function wCut() {
      fnWidget("w-cut", ["x^3-4x", "x^2-2x-3", "(x^2-1)/(x+2)", "e^x-2", "ln(x+1)", "x^2*e^x", "sqrt(x^2-4)", "sqrt(x+3)-x-1"], "pCut", function (w, n) {
        var f = compile(n), Dm = domainOf(f, condsOf(n).den.map(compile)), C = cutsOf(f, Dm);
        var xs = C.ox.slice(), ys = [0]; if (C.oy !== null) { xs.push(0); ys.push(C.oy); }
        w.querySelector(".info").innerHTML = "<p>" + tex("f(x)=" + T(n)) + "</p>" + cutsHtml(C);
        plot(w.querySelector("svg.lp-svg"), { v: viewOf(f, xs, ys, [-5, 5]), band: domBands(Dm), curves: [{ f: f }], pts: cutPts(C),
          labels: cutPts(C).map(function (p) { return { x: p.x, y: p.y, t: "(" + numTxt(+p.x.toFixed(3)) + ", " + numTxt(+p.y.toFixed(3)) + ")", anchor: "start" }; }) });
      });
    }
    function wSym() {
      fnWidget("w-sym", ["x^4-3x^2", "x^3-3x", "x/(x^2+1)", "x^2/(x^2-1)", "e^(-x^2)", "e^x", "x^2+x", "sqrt(9-x^2)", "x*sqrt(x^2+1)", "sqrt(x+2)"], "pSym", function (w, n) {
        var f = compile(n), s = symOf(f), rows = "";
        [1, 2, 3].forEach(function (x) {
          var a = f(x), b = f(-x);
          rows += "<tr><td>" + tex(String(x)) + "</td><td>" + tex(isFinite(a) ? nn(a) : "\\nexists") + "</td><td>" + tex(isFinite(b) ? nn(b) : "\\nexists") + "</td><td>" + tex(isFinite(a) ? nn(-a) : "\\nexists") + "</td></tr>";
        });
        var cls = s === "even" ? "ok" : s === "odd" ? "ev" : "as";
        w.querySelector(".info").innerHTML = "<p>" + tex("f(x)=" + T(n)) + "</p>" +
          '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + tex("x") + "</th><th>" + tex("f(x)") + "</th><th>" + tex("f(-x)") + "</th><th>" + tex("-f(x)") + "</th></tr></thead><tbody>" + rows + "</tbody></table></div>" +
          "<p>" + (s === "even" ? tex("f(-x)=f(x)") : s === "odd" ? tex("f(-x)=-f(x)") : "") + ' <span class="badge ' + cls + '">' + symTxt(s) + "</span></p>";
        var v = viewOf(f, [-3, 3], [], [-5, 5]);
        plot(w.querySelector("svg.lp-svg"), { v: v, curves: [{ f: function (x) { return s === "odd" ? -f(-x) : f(-x); }, col: "var(--r3)" }, { f: f }], guides: s === "even" ? [{ x: 0 }] : [],
          pts: s === "odd" ? [{ x: 0, y: 0, col: "var(--accent-2)" }] : [] });
      });
    }
    function wAsy() {
      fnWidget("w-asy", ["(2x+1)/(x-3)", "x/(x^2-1)", "3x^2/(x^2+1)", "2-e^(-x)", "ln(x+2)", "(x^2+1)/x"], "pAsy", function (w, n) {
        var f = compile(n), Dm = domainOf(f, condsOf(n).den.map(compile)), A = asyOf(f, Dm, n), poly = !!(A.rat && pDeg(A.rat.Q) === 0), P = asyPlot(A);
        var ys = P.ha.slice();
        w.querySelector(".info").innerHTML = "<p>" + tex("f(x)=" + T(n)) + "</p>" + asyHtml(A, poly);
        plot(w.querySelector("svg.lp-svg"), Object.assign({ v: viewOf(f, P.va, ys, [-6, 6]), curves: [{ f: f }] }, P));
      });
    }
    function wMx() {
      fnWidget("w-mx", ["x^3-6x^2+9x", "x^4-2x^2", "x^2/(x^2-4)", "(x^2+3)/(x-1)", "x*e^x", "ln(x)/x"], "pMx", function (w, n) {
        var info = w.querySelector(".info"), tb = $(w, "tbl"), R;
        try { R = fullStudy(n); } catch (e) { info.textContent = u("bad"); tb.innerHTML = ""; return; }
        if (!R.S) { info.textContent = u("noDiff"); tb.innerHTML = ""; return; }
        info.innerHTML = "<p>" + tex("f(x)=" + T(n)) + "<br>" + tex("f'(x)=" + texD(R.S.dn)) + "</p>" + monoHtml(R.S, R.inf) + extHtml(R.S);
        tb.innerHTML = signTable(R.S, R.inf);
        plot(w.querySelector("svg.lp-svg"), Object.assign({ v: R.view, curves: monoCurves(R.S), mark: extMarks(R.S) }, asyPlot(R.A)));
      });
    }

    /* ---------- asímptota obliqua pel mètode del quocient ---------- */
    function wObl() {
      var w = document.getElementById("w-obl"); if (!w) return;
      var PRE = [["x^2+3", "x-1"], ["x^2", "x+1"], ["2x^2-x+1", "x"], ["x^3", "x^2-1"], ["x^3+1", "x"], ["3x^2+1", "x^2-4"]];
      var pi = $(w, "p"), qi = $(w, "q"), info = w.querySelector(".info"), dv = $(w, "div"), svg = w.querySelector("svg.lp-svg");
      presetBtns($(w, "presets"), PRE.length, "pObl", function (i) { pi.value = PRE[i][0]; qi.value = PRE[i][1]; draw(); });
      [pi, qi].forEach(function (el) { el.addEventListener("input", draw); });
      function draw() {
        var P, Q;
        try { P = pTrim(polyOf(parse(pi.value))); Q = pTrim(polyOf(parse(qi.value))); if (pDeg(Q) === 0 && Q[0].zero()) throw 0; pi.classList.remove("bad"); qi.classList.remove("bad"); }
        catch (e) { pi.classList.add("bad"); qi.classList.add("bad"); info.textContent = u("notPoly"); dv.innerHTML = ""; return; }
        var Dv = pDiv(P, Q), dP = pDeg(P), dQ = pDeg(Q), Pf = pFn(P), Qf = pFn(Q), f = function (x) { return Pf(x) / Qf(x); };
        var Dm = domainOf(f, [Qf]), A = asyOf(f, Dm, null, { P: P, Q: Q });
        var h = "<p>" + tex("f(x)=\\dfrac{" + pTex(P) + "}{" + pTex(Q) + "}") + "</p>";
        // passos de la divisió
        var s = "";
        Dv.steps.forEach(function (st, i) {
          var lead = [], k = pDeg(st.r); for (var j = 0; j < k; j++) lead.push(new Fr(0)); lead.push(st.r[k]);
          s += "<li>" + u("divide") + " " + tex("\\dfrac{" + pTex(lead) + "}{" + monoTex(Q[dQ], dQ, true) + "}=" + pTex(st.m)) + "; " + u("mult") + " " + tex(pTex(st.m) + "\\cdot\\left(" + pTex(Q) + "\\right)=" + pTex(st.s)) +
            "; " + u("subt") + ": " + tex("\\left(" + pTex(st.r) + "\\right)-\\left(" + pTex(st.s) + "\\right)=" + pTex(st.n)) + "</li>";
        });
        dv.innerHTML = (s ? "<ol>" + s + "</ol>" : "") + "<p>" + u("quo") + " " + tex("C(x)=" + pTex(Dv.q)) + ", &nbsp;" + u("rem") + " " + tex("R(x)=" + pTex(Dv.r)) + "<br>" +
          tex("f(x)=" + pTex(Dv.q) + (pDeg(Dv.r) === 0 && Dv.r[0].zero() ? "" : "+\\dfrac{" + pTex(Dv.r) + "}{" + pTex(Q) + "}")) + "</p>";
        var cas = dP < dQ ? "dLt" : dP === dQ ? "dEq" : dP === dQ + 1 ? "dP1" : "dBig";
        h += '<p class="verdict">' + u(cas).replace("C(x)", "") + (cas === "dEq" ? ": " + tex("y=\\dfrac{" + P[dP].tex() + "}{" + Q[dQ].tex() + "}=" + P[dP].div(Q[dQ]).tex()) : cas === "dP1" ? " " + tex("y=" + pTex(Dv.q)) : "") + "</p>";
        h += "<p><strong>" + u("av") + ":</strong> " + avHtml(A) + "</p>";
        var o = A.side[1];
        if (o.k === "o" || o.k === "h") {
          var g = o.k === "o" ? function (x) { return o.m * x + o.n; } : function () { return o.y; }, rows = "";
          [-1000, -100, -10, 10, 100, 1000].forEach(function (x) { var d = f(x) - g(x); rows += "<tr><td>" + tex(String(x)) + "</td><td>" + tex(numTex(+d.toPrecision(4))) + "</td></tr>"; });
          var yl = o.k === "o" ? lineTx(o.m, o.n).slice(2) : nn(o.y);
          h += '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + tex("x") + "</th><th>" + tex("f(x)-\\left(" + yl + "\\right)") + "</th></tr></thead><tbody>" + rows + "</tbody></table></div>";
          var dl = f(-1000) - g(-1000), dr = f(1000) - g(1000);
          if (Math.abs(dl) > 1e-12 || Math.abs(dr) > 1e-12) h += "<p>" + u("toL").replace(/^./, function (c) { return c.toUpperCase(); }) + ": " + (dl > 0 ? u("above") : u("below")) + ".<br>" + u("toR").replace(/^./, function (c) { return c.toUpperCase(); }) + ": " + (dr > 0 ? u("above") : u("below")) + ".</p>";
        }
        info.innerHTML = h;
        var Pp = asyPlot(A);
        plot(svg, Object.assign({ v: viewOf(f, Pp.va, Pp.ha, [-6, 6]), curves: [{ f: f }] }, Pp));
      }
      onLang(draw);
    }

    /* ---------- famílies exponencials i logarítmiques ---------- */
    function wEl() {
      var w = document.getElementById("w-el"); if (!w) return;
      var ty = 0, ra = $(w, "a"), rh = $(w, "h"), rk = $(w, "k"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
      [ra, rh, rk].forEach(function (r) { r.min = -3; r.max = 3; r.step = 0.5; r.addEventListener("input", draw); });
      ra.value = 1; rh.value = 0; rk.value = 0;
      presetBtns($(w, "presets"), 3, "pEl", function (i) { ty = i; ra.value = 1; rh.value = 0; rk.value = i === 2 ? 0 : -1; draw(); });
      function sh(h) { return h === 0 ? "x" : h > 0 ? "x-" + nn(h) : "x+" + nn(-h); }
      function co(a) { return a === 1 ? "" : a === -1 ? "-" : nn(a) + "\\,"; }
      function kk(k) { return k === 0 ? "" : (k > 0 ? "+" : "-") + nn(Math.abs(k)); }
      function draw() {
        var a = +ra.value, h = +rh.value, k = +rk.value;
        if (a === 0) { a = 0.5; ra.value = 0.5; }
        $(w, "av").textContent = numTxt(a); $(w, "hv").textContent = numTxt(h); $(w, "kv").textContent = numTxt(k);
        var b = ty === 0 ? Math.E : 0.5, lb = Math.log(b), f, ft, H = "", cfg = { v: [-6, 6, -5, 5] }, pts = [];
        if (ty < 2) {
          f = function (x) { return a * Math.pow(b, x - h) + k; };
          ft = "f(x)=" + co(a) + (ty === 0 ? "e^{" + sh(h) + "}" : "\\left(\\tfrac12\\right)^{" + sh(h) + "}") + kk(k);
          var r = -k / a;
          H += "<p><strong>" + u("dom") + ":</strong> " + tex("\\mathbb R") + "</p>";
          H += "<p><strong>" + u("ah") + ":</strong> " + tex("y=" + nn(k)) + " " + (lb > 0 ? u("toL") : u("toR")) + "<br><strong>" + u("av") + ":</strong> " + u("noAV") + "</p>";
          H += "<p><strong>" + u("cutY") + ":</strong> " + tex("(0," + nn(f(0)) + ")") + "<br><strong>" + u("cutX") + ":</strong> " +
            (r > 0 ? tex((ty === 0 ? "e^{" + sh(h) + "}" : "\\left(\\tfrac12\\right)^{" + sh(h) + "}") + "=" + nn(r) + "\\ \\Rightarrow\\ x=" + nn(h + Math.log(r) / lb)) : u("noCutX")) + "</p>";
          H += "<p><strong>" + u("mono") + ":</strong> " + (a * lb > 0 ? u("inc") : u("dec")) + " " + t3("en", "en", "on") + " " + tex("\\mathbb R") + "</p>";
          cfg.ha = [k]; pts.push({ x: 0, y: f(0) }); if (r > 0) pts.push({ x: h + Math.log(r) / lb, y: 0 });
        } else {
          f = function (x) { return x > h ? a * Math.log(x - h) + k : NaN; };
          ft = "f(x)=" + co(a) + "\\ln(" + sh(h) + ")" + kk(k);
          var x0 = h + Math.exp(-k / a);
          H += "<p><strong>" + u("dom") + ":</strong> " + tex(sh(h) + "\\gt0\\ \\Rightarrow\\ (" + nn(h) + ",+\\infty)") + "</p>";
          H += "<p><strong>" + u("av") + ":</strong> " + tex("x=" + nn(h)) + " &nbsp;(" + tex("\\lim_{x\\to " + nn(h) + "^+}f(x)=" + (a > 0 ? "-\\infty" : "+\\infty")) + ")<br><strong>" + u("ah") + ":</strong> " + u("noAV") + "</p>";
          H += "<p><strong>" + u("cutX") + ":</strong> " + tex("\\ln(" + sh(h) + ")=" + nn(-k / a) + "\\ \\Rightarrow\\ x=" + nn(x0)) + "<br><strong>" + u("cutY") + ":</strong> " + (h < 0 ? tex("(0," + nn(f(0)) + ")") : u("noCutY")) + "</p>";
          H += "<p><strong>" + u("mono") + ":</strong> " + (a > 0 ? u("inc") : u("dec")) + " " + t3("en", "en", "on") + " " + tex("(" + nn(h) + ",+\\infty)") + "</p>";
          cfg.va = [h]; cfg.band = [{ a: -10, b: h }]; pts.push({ x: x0, y: 0 }); if (h < 0) pts.push({ x: 0, y: f(0) });
        }
        info.innerHTML = "<p>" + tex(ft) + "</p>" + H;
        cfg.curves = [{ f: f }]; cfg.pts = pts.map(function (p) { p.col = "var(--accent-2)"; return p; });
        plot(svg, cfg);
      }
      onLang(draw);
    }

    /* ---------- funcions a trossos ---------- */
    function pwStudy(def) {
      var P = pwMake(def), segs = [], av = [], ha = {};
      for (var i = 0; i < P.n; i++) {
        var B = P.bounds(i), lo = Math.max(B[0], -XL), hi = Math.min(B[1], XL); if (!(hi > lo)) continue;
        var n = parse(def.p[i]), fi = compile(n), S = null;
        try { S = crit(fi, compile(D(n)), lo, hi); } catch (e) { S = null; }
        if (S) S.seg.forEach(function (g) { segs.push({ a: g.a, b: g.b, s: g.s }); });
        condsOf(n).den.forEach(function (d) {
          roots(compile(d), lo, hi).forEach(function (r) { if (r > B[0] && r < B[1] && limSide(fi, r, 1).k === "inf") av.push(r); });
        });
        if (i === 0 && !isFinite(B[0])) { var L = limSide(fi, -Infinity, -1); if (L.k === "num") ha[-1] = snap(Math.abs(L.v) < 1e-5 ? 0 : L.v); }
        if (i === P.n - 1 && !isFinite(B[1])) { var R = limSide(fi, Infinity, 1); if (R.k === "num") ha[1] = snap(Math.abs(R.v) < 1e-5 ? 0 : R.v); }
      }
      // ajuntem els trams amb el mateix signe i busquem els extrems (també en els punts de tall, si hi és contínua)
      var runs = [];
      segs.forEach(function (g) {
        var r = runs[runs.length - 1];
        if (r && r.s === g.s && Math.abs(r.b - g.a) < 1e-9 && g.s !== 0 && isFinite(P.f(g.a)) && Math.abs(P.f(g.a) - P.f(g.a - 1e-7)) < 1e-4 && Math.abs(P.f(g.a) - P.f(g.a + 1e-7)) < 1e-4) r.b = g.b;
        else runs.push({ a: g.a, b: g.b, s: g.s });
      });
      var ext = [];
      for (var j = 0; j + 1 < runs.length; j++) {
        var x = runs[j].b, y = P.f(x);
        if (!isFinite(y) || Math.abs(x - runs[j + 1].a) > 1e-9) continue;
        if (Math.abs(P.f(x - 1e-7) - y) > 1e-4 || Math.abs(P.f(x + 1e-7) - y) > 1e-4) continue;
        if (runs[j].s > 0 && runs[j + 1].s < 0) ext.push({ x: snap(x), y: y, t: "max" });
        if (runs[j].s < 0 && runs[j + 1].s > 0) ext.push({ x: snap(x), y: y, t: "min" });
      }
      return { P: P, runs: runs, ext: ext, av: av, ha: ha };
    }
    function wPw() {
      var w = document.getElementById("w-pw"); if (!w) return;
      var PRE = [PWF.ex, PWF.jump, PWF.el, PWF.rat];
      var ins = ["p1", "c1", "p2", "c2", "p3"].map(function (r) { return $(w, r); }), info = w.querySelector(".info"), svg = w.querySelector("svg.lp-svg");
      presetBtns($(w, "presets"), PRE.length, "pPw", function (i) {
        var d = PRE[i]; ins[0].value = d.p[0]; ins[1].value = numTxt(d.c[0]).replace("−", "-"); ins[2].value = d.p[1];
        ins[3].value = d.c[1] !== undefined ? numTxt(d.c[1]).replace("−", "-") : ""; ins[4].value = d.p[2] || ""; draw();
      });
      ins.forEach(function (el) { el.addEventListener("input", draw); });
      function draw() {
        var def = { p: [ins[0].value, ins[2].value], c: [] }, okAll = true;
        ins.forEach(function (el) { el.classList.remove("bad"); });
        var c1 = parseFr(ins[1].value);
        if (!c1) { ins[1].classList.add("bad"); okAll = false; } else def.c.push(c1.val());
        if (ins[4].value.trim() !== "" || ins[3].value.trim() !== "") {
          var c2 = parseFr(ins[3].value);
          if (!c2 || (c1 && c2.val() <= c1.val())) { ins[3].classList.add("bad"); okAll = false; } else { def.c.push(c2.val()); def.p.push(ins[4].value); }
        }
        [0, 2, 4].forEach(function (k, i) { if (i < def.p.length) { try { parse(ins[k].value); } catch (e) { ins[k].classList.add("bad"); okAll = false; } } });
        if (!okAll) { info.textContent = u("bad"); return; }
        var Z;
        try { Z = pwStudy(def); } catch (e) { info.textContent = u("bad"); return; }
        var P = Z.P, h = "<p>" + tex(pwTex(def)) + "</p>", allC = true;
        P.c.forEach(function (c, k) {
          var L = sideAt(P.piece(k), c, -1), R = sideAt(P.piece(k + 1), c, 1), fc = P.f(c), cl = classify(L, R, fc);
          if (cl !== "ok") allC = false;
          h += "<p>" + u("atCut") + " " + tex("x=" + nn(c)) + ": " + tex("\\lim_{x\\to " + nn(c) + "^-}f(x)=" + limTex(L) + ",\\ \\lim_{x\\to " + nn(c) + "^+}f(x)=" + limTex(R) + ",\\ f(" + nn(c) + ")=" + nn(fc)) + " " + badge(cl) + "</p>";
        });
        if (allC && !Z.av.length) h += '<p class="msg-ok">' + u("contAll") + "</p>";
        if (Z.av.length) h += "<p><strong>" + u("av") + ":</strong> " + tex(Z.av.map(function (x) { return "x=" + nn(x); }).join(",\\ ")) + "</p>";
        if (Z.ha[-1] !== undefined) h += "<p><strong>" + u("ah") + ":</strong> " + tex("y=" + nn(Z.ha[-1])) + " " + u("toL") + "</p>";
        if (Z.ha[1] !== undefined) h += "<p><strong>" + u("ah") + ":</strong> " + tex("y=" + nn(Z.ha[1])) + " " + u("toR") + "</p>";
        var last = Z.runs.length - 1;
        function iv(r, j) { return intTex(r.a, r.b, j === 0 && r.a <= -XL + 1e-9, j === last && r.b >= XL - 1e-9); }
        var up = [], dn = [];
        Z.runs.forEach(function (r, j) { if (r.s > 0) up.push(iv(r, j)); if (r.s < 0) dn.push(iv(r, j)); });
        h += "<p><strong>" + u("incOn") + "</strong> " + (up.length ? tex(up.join("\\cup ")) : "—") + "<br><strong>" + u("decOn") + "</strong> " + (dn.length ? tex(dn.join("\\cup ")) : "—") + "</p>";
        h += "<p>" + (Z.ext.length ? Z.ext.map(function (e) { return '<span class="badge ' + (e.t === "max" ? "ok" : "as") + '">' + u(e.t === "max" ? "maxR" : "minR") + "</span> " + tex(ptTex(e.x, e.y)); }).join("<br>") : u("noExtPw")) + "</p>";
        info.innerHTML = h;
        var xs = P.c.concat(Z.av).concat(Z.ext.map(function (e) { return e.x; })), x0 = Math.min.apply(null, xs) - 4, x1 = Math.max.apply(null, xs) + 4;
        var yy = autoY([P.f], x0, x1);
        var v = [x0, x1, yy[0], yy[1]], d = pwDraw(P, v);
        var ha = []; if (Z.ha[-1] !== undefined) ha.push(Z.ha[-1]); if (Z.ha[1] !== undefined && ha.indexOf(Z.ha[1]) < 0) ha.push(Z.ha[1]);
        plot(svg, { v: v, curves: d.curves, pts: d.pts, va: Z.av, ha: ha, mark: Z.ext.map(function (e) { return { x: e.x, y: e.y, col: e.t === "max" ? "var(--ok)" : "var(--bad)" }; }) });
      }
      onLang(function () { if (!ins[0].value) { ins[0].value = PRE[0].p[0]; ins[1].value = "-1"; ins[2].value = PRE[0].p[1]; ins[3].value = "1"; ins[4].value = PRE[0].p[2]; } draw(); });
    }

    /* ---------- estudi complet pas a pas ---------- */
    function wLab() {
      var w = document.getElementById("w-lab7"); if (!w) return;
      var PRE = ["x^3-6x^2+9x", "x^4-2x^2", "x^2/(x^2-4)", "(x^2+3)/(x-1)", "(2x-1)/(x+1)", "x*e^x", "e^x/x", "ln(x)/x"];
      var fi = $(w, "f"), out = $(w, "out"), tb = $(w, "tbl"), svg = w.querySelector("svg.lp-svg"), bn = $(w, "nx"), ba = $(w, "al"), cnt = $(w, "cnt"), R = null, shown = 1;
      presetBtns($(w, "presets"), PRE.length, "pLab", function (i) { fi.value = PRE[i]; setup(); });
      fi.addEventListener("input", setup);
      bn.addEventListener("click", function () { if (shown < 6) { shown++; draw(); } });
      ba.addEventListener("click", function () { shown = shown >= 6 ? 1 : 6; draw(); });
      function setup() {
        shown = 1;
        try { R = fullStudy(parse(fi.value)); fi.classList.remove("bad"); }
        catch (e) { R = null; fi.classList.add("bad"); out.textContent = u("bad"); tb.innerHTML = ""; return; }
        draw();
      }
      function row(i, html) { return '<div class="rs' + (i === shown - 1 ? " now" : "") + '"><h4>' + (i + 1) + ". " + u("sNames")[i] + "</h4>" + html + "</div>"; }
      function draw() {
        if (!R) return;
        var names = u("sNames"), rows = [], S = R.S;
        rows.push(row(0, (R.Dm.iv.length ? tex("\\mathrm{Dom}\\,f=" + domTex(R.Dm)) : u("empty")) + '<div class="why">' + domWhy(R.n) + "</div>"));
        if (shown > 1) rows.push(row(1, cutsHtml(R.cuts)));
        if (shown > 2) rows.push(row(2, symTxt(R.sym) + (R.sym === "even" ? " — " + tex("f(-x)=f(x)") : R.sym === "odd" ? " — " + tex("f(-x)=-f(x)") : "")));
        if (shown > 3) rows.push(row(3, asyHtml(R.A, R.poly)));
        if (shown > 4) rows.push(row(4, S ? "<p>" + tex("f'(x)=" + texD(S.dn)) + "</p>" + monoHtml(S, R.inf) + extHtml(S) : u("noDiff")));
        if (shown > 5) rows.push(row(5, "✓"));
        out.innerHTML = "<p>" + tex("f(x)=" + T(R.n)) + "</p>" + rows.join("");
        tb.innerHTML = shown > 4 && S ? signTable(S, R.inf) : "";
        bn.textContent = u("next") + " →"; bn.disabled = shown >= 6;
        ba.textContent = shown >= 6 ? u("reset") : u("all");
        cnt.textContent = u("step") + " " + shown + " " + u("of") + " 6 · " + names[shown - 1];
        var cfg = { v: R.view, band: domBands(R.Dm), curves: [], pts: [] };
        if (shown > 1) cfg.pts = cutPts(R.cuts);
        if (shown > 3) Object.assign(cfg, asyPlot(R.A));
        if (shown > 4 && S) cfg.mark = extMarks(S);
        if (shown > 5) cfg.curves = S ? monoCurves(S) : [{ f: R.f }];
        plot(svg, cfg);
      }
      onLang(setup);
    }

    /* ---------- qüestionari ---------- */
    function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
    var QUIZ = [
      { q: q3("El domini de $f(x)=\\dfrac{x+1}{x^2-9}$ és…", "El dominio de $f(x)=\\dfrac{x+1}{x^2-9}$ es…", "The domain of $f(x)=\\dfrac{x+1}{x^2-9}$ is…"),
        o: [q3("$\\mathbb R$"), q3("$\\mathbb R-\\{-3,3\\}$"), q3("$\\mathbb R-\\{-1\\}$")], a: 1, e: q3("El denominador s'anul·la en $x^2=9\\Rightarrow x=\\pm3$.", "El denominador se anula en $x^2=9\\Rightarrow x=\\pm3$.", "The denominator is zero when $x^2=9\\Rightarrow x=\\pm3$.") },
      { q: q3("El domini de $f(x)=\\ln(x-2)$ és…", "El dominio de $f(x)=\\ln(x-2)$ es…", "The domain of $f(x)=\\ln(x-2)$ is…"),
        o: [q3("$[2,+\\infty)$"), q3("$(2,+\\infty)$"), q3("$\\mathbb R-\\{2\\}$")], a: 1, e: q3("L'argument del logaritme ha de ser positiu: $x-2\\gt0$.", "El argumento del logaritmo tiene que ser positivo: $x-2\\gt0$.", "The argument of the logarithm must be positive: $x-2\\gt0$.") },
      { q: q3("Els punts de tall de $f(x)=x^2-4x$ amb l'eix OX són…", "Los puntos de corte de $f(x)=x^2-4x$ con el eje OX son…", "The x-intercepts of $f(x)=x^2-4x$ are…"),
        o: [q3("$(0,0)$ i $(4,0)$", "$(0,0)$ y $(4,0)$", "$(0,0)$ and $(4,0)$"), q3("$(0,0)$ i $(-4,0)$", "$(0,0)$ y $(-4,0)$", "$(0,0)$ and $(-4,0)$"), q3("$(0,-4)$")], a: 0, e: q3("$x^2-4x=x(x-4)=0\\Rightarrow x=0,\\ x=4$.") },
      { q: q3("Si $f(-x)=-f(x)$ per a tot $x$ del domini, la funció és…", "Si $f(-x)=-f(x)$ para todo $x$ del dominio, la función es…", "If $f(-x)=-f(x)$ for every $x$ in the domain, the function is…"),
        o: [q3("parella: simètrica respecte de l'eix OY", "par: simétrica respecto del eje OY", "even: symmetric about the y-axis"), q3("senar: simètrica respecte de l'origen", "impar: simétrica respecto del origen", "odd: symmetric about the origin"), q3("periòdica", "periódica", "periodic")], a: 1,
        e: q3("Per exemple, $f(x)=x^3-3x$.", "Por ejemplo, $f(x)=x^3-3x$.", "For example, $f(x)=x^3-3x$.") },
      { q: q3("$f(x)=x^4-3x^2+1$ és…", "$f(x)=x^4-3x^2+1$ es…", "$f(x)=x^4-3x^2+1$ is…"),
        o: [q3("parella", "par", "even"), q3("senar", "impar", "odd"), q3("ni parella ni senar", "ni par ni impar", "neither")], a: 0, e: q3("Només hi ha potències parelles de $x$: $f(-x)=f(x)$.", "Solo hay potencias pares de $x$: $f(-x)=f(x)$.", "Only even powers of $x$ appear: $f(-x)=f(x)$.") },
      { q: q3("Les asímptotes de $f(x)=\\dfrac{2x+1}{x-3}$ són…", "Las asíntotas de $f(x)=\\dfrac{2x+1}{x-3}$ son…", "The asymptotes of $f(x)=\\dfrac{2x+1}{x-3}$ are…"),
        o: [q3("$x=3$ i $y=2$", "$x=3$ y $y=2$", "$x=3$ and $y=2$"), q3("$x=-3$ i $y=2$", "$x=-3$ y $y=2$", "$x=-3$ and $y=2$"), q3("$x=3$ i $y=0$", "$x=3$ y $y=0$", "$x=3$ and $y=0$")], a: 0,
        e: q3("El denominador s'anul·la en $x=3$; els graus són iguals: $y=\\frac21=2$.", "El denominador se anula en $x=3$; los grados son iguales: $y=\\frac21=2$.", "The denominator is zero at $x=3$; equal degrees: $y=\\frac21=2$.") },
      { q: q3("Una funció racional $\\frac{P(x)}{Q(x)}$ té asímptota obliqua quan…", "Una función racional $\\frac{P(x)}{Q(x)}$ tiene asíntota oblicua cuando…", "A rational function $\\frac{P(x)}{Q(x)}$ has an oblique asymptote when…"),
        o: [q3("grau $P$ = grau $Q$", "grado $P$ = grado $Q$", "deg $P$ = deg $Q$"), q3("grau $P$ = grau $Q$ + 1", "grado $P$ = grado $Q$ + 1", "deg $P$ = deg $Q$ + 1"), q3("grau $P$ < grau $Q$", "grado $P$ < grado $Q$", "deg $P$ < deg $Q$")], a: 1,
        e: q3("Aleshores el quocient de la divisió és de grau 1: $y=mx+n$.", "Entonces el cociente de la división es de grado 1: $y=mx+n$.", "Then the quotient of the division has degree 1: $y=mx+n$.") },
      { q: q3("L'asímptota obliqua de $f(x)=\\dfrac{x^2+3}{x-1}$ és…", "La asíntota oblicua de $f(x)=\\dfrac{x^2+3}{x-1}$ es…", "The oblique asymptote of $f(x)=\\dfrac{x^2+3}{x-1}$ is…"),
        o: [q3("$y=x$"), q3("$y=x+1$"), q3("$y=x-1$")], a: 1, e: q3("$x^2+3=(x-1)(x+1)+4$: el quocient és $x+1$.", "$x^2+3=(x-1)(x+1)+4$: el cociente es $x+1$.", "$x^2+3=(x-1)(x+1)+4$: the quotient is $x+1$.") },
      { q: q3("La funció $f(x)=e^x+2$ té…", "La función $f(x)=e^x+2$ tiene…", "The function $f(x)=e^x+2$ has…"),
        o: [q3("asímptota horitzontal $y=2$ quan $x\\to-\\infty$", "asíntota horizontal $y=2$ cuando $x\\to-\\infty$", "horizontal asymptote $y=2$ as $x\\to-\\infty$"), q3("asímptota vertical $x=2$", "asíntota vertical $x=2$", "vertical asymptote $x=2$"), q3("asímptota horitzontal $y=2$ quan $x\\to+\\infty$", "asíntota horizontal $y=2$ cuando $x\\to+\\infty$", "horizontal asymptote $y=2$ as $x\\to+\\infty$")], a: 0,
        e: q3("$\\lim_{x\\to-\\infty}e^x=0$, així que $f(x)\\to2$.", "$\\lim_{x\\to-\\infty}e^x=0$, así que $f(x)\\to2$.", "$\\lim_{x\\to-\\infty}e^x=0$, so $f(x)\\to2$.") },
      { q: q3("La funció $f(x)=\\ln x$ té una asímptota…", "La función $f(x)=\\ln x$ tiene una asíntota…", "The function $f(x)=\\ln x$ has an asymptote…"),
        o: [q3("vertical $x=0$", "vertical $x=0$", "vertical, $x=0$"), q3("horitzontal $y=0$", "horizontal $y=0$", "horizontal, $y=0$"), q3("vertical $x=1$", "vertical $x=1$", "vertical, $x=1$")], a: 0,
        e: q3("$\\lim_{x\\to0^+}\\ln x=-\\infty$.") },
      { q: q3("Una funció polinòmica…", "Una función polinómica…", "A polynomial function…"),
        o: [q3("sempre té asímptota horitzontal", "siempre tiene asíntota horizontal", "always has a horizontal asymptote"), q3("no té asímptotes", "no tiene asíntotas", "has no asymptotes"), q3("té asímptotes verticals on s'anul·la", "tiene asíntotas verticales donde se anula", "has vertical asymptotes at its zeros")], a: 1,
        e: q3("Té domini $\\mathbb R$ i als extrems tendeix a $\\pm\\infty$ (si no és constant ni de grau 1).", "Tiene dominio $\\mathbb R$ y en los extremos tiende a $\\pm\\infty$ (si no es constante ni de grado 1).", "Its domain is $\\mathbb R$ and it tends to $\\pm\\infty$ at both ends (unless it is constant or of degree 1).") },
      { q: q3("En una funció a trossos, els punts que cal estudiar sempre a banda són…", "En una función a trozos, los puntos que hay que estudiar siempre aparte son…", "In a piecewise function, the points that must always be studied separately are…"),
        o: [q3("els punts on canvia la definició", "los puntos donde cambia la definición", "the points where the definition changes"), q3("els talls amb OY", "los cortes con OY", "the y-intercepts"), q3("els enters", "los enteros", "the integers")], a: 0,
        e: q3("Allà pot haver-hi salts o punts angulosos, i també màxims o mínims.", "Allí puede haber saltos o puntos angulosos, y también máximos o mínimos.", "There may be jumps or corners there, and also maxima or minima.") }
    ];

    return { UI: UI, QUIZ: QUIZ, ws: [wFigs, wDom, wCut, wSym, wAsy, wObl, wMx, wEl, wPw, wLab] };
  })();

  LANGS.forEach(function (l) { [M5, M6, M7].forEach(function (M) { var src = M.UI[l] || {}; Object.keys(src).forEach(function (k) { if (!(k in UI[l])) UI[l][k] = src[k]; }); }); });
  // qüestionari: les preguntes de derivabilitat (unitat 5 de CCSS) es descarten; de la unitat 7, simetria, asímptotes i polinomis
  var QUIZ = M5.QUIZ.slice(0, 8).concat(M6.QUIZ, [M7.QUIZ[3], M7.QUIZ[5], M7.QUIZ[10]]);
  /*@@GENERIC@@*/
  var TITLES = { va: "Derivades i aplicacions · FentMates", es: "Derivadas y aplicaciones · FentMates", en: "Derivatives and applications · FentMates" };
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
      document.querySelectorAll(".widget .wt, .widget label, .widget .ttl, .widget .legend, .lab label, .lab .legend").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav].concat(M5.ws, M6.ws, M7.ws, [wQuiz]);
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM19 = { parse: parse, D: D, texD: texD, compile: compile, M: [M5, M6, M7], UI: UI };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
