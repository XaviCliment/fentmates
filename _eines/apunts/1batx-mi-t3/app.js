(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1batx-mi-u3-sistemes-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt",
      badP: "No entenc el polinomi. Escriu-lo així: <code>2x^3-x+5</code> o <code>x^4/4</code> → <code>1/4x^4</code>." },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba",
      badP: "No entiendo el polinomio. Escríbelo así: <code>2x^3-x+5</code> o <code>x^4/4</code> → <code>1/4x^4</code>." },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top",
      badP: "I can't read that polynomial. Write it like this: <code>2x^3-x+5</code> or <code>x^4/4</code> → <code>1/4x^4</code>." }
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
  var COL = { a: "#3b82f6", b: "#f97316", r: "#e11d48", k: "#16a34a", v: "#7c3aed" };
  function ok(b) { return b ? '<span class="msg-ok">✓</span>' : '<span class="msg-bad">✗</span>'; }

  /* ---------- nombres ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function decS(x, k) { var s = String(+x.toFixed(k == null ? 2 : k)); if (s === "-0") s = "0"; return lang === "en" ? s : s.replace(".", ","); }
  function dT(x, k) { return decS(x, k).replace(",", "{,}"); }
  function frac(x) { if (!isFinite(x)) return null; for (var d = 1; d <= 12; d++) { var n = Math.round(x * d); if (Math.abs(n / d - x) < 1e-9) return [n, d]; } return null; }
  function nT(x) {
    if (x === Infinity) return "+\\infty"; if (x === -Infinity) return "-\\infty";
    var f = frac(x);
    if (f) return f[1] === 1 ? String(f[0]) : (f[0] < 0 ? "-" : "") + "\\frac{" + Math.abs(f[0]) + "}{" + f[1] + "}";
    return dT(x, 3);
  }
  function nS(x) { var f = frac(x); if (f && f[1] !== 1) return (f[0] < 0 ? "−" : "") + Math.abs(f[0]) + "/" + f[1]; return decS(x, 2).replace("-", "−"); }

  /* ---------- fraccions exactes ---------- */
  function Fr(n, d) {
    if (d === undefined) d = 1;
    if (d === 0) throw new Error("div0");
    if (d < 0) { n = -n; d = -d; }
    var g = gcd(n, d) || 1; this.n = n / g; this.d = d / g; if (this.n === 0) this.d = 1;
  }
  function fr(x) { return x instanceof Fr ? x : toFr(x); }
  Fr.prototype.add = function (o) { o = fr(o); return new Fr(this.n * o.d + o.n * this.d, this.d * o.d); };
  Fr.prototype.sub = function (o) { o = fr(o); return new Fr(this.n * o.d - o.n * this.d, this.d * o.d); };
  Fr.prototype.mul = function (o) { o = fr(o); return new Fr(this.n * o.n, this.d * o.d); };
  Fr.prototype.div = function (o) { o = fr(o); return new Fr(this.n * o.d, this.d * o.n); };
  Fr.prototype.neg = function () { return new Fr(-this.n, this.d); };
  Fr.prototype.abs = function () { return new Fr(Math.abs(this.n), this.d); };
  Fr.prototype.zero = function () { return this.n === 0; };
  Fr.prototype.eq = function (o) { o = fr(o); return this.n === o.n && this.d === o.d; };
  Fr.prototype.sgn = function () { return this.n > 0 ? 1 : this.n < 0 ? -1 : 0; };
  Fr.prototype.val = function () { return this.n / this.d; };
  var F0 = new Fr(0), F1 = new Fr(1), FM1 = new Fr(-1);
  function toFr(x) { if (Number.isInteger(x)) return new Fr(x); return new Fr(Math.round(x * 10000), 10000); }
  function frT(f) { f = fr(f); return f.d === 1 ? String(f.n) : (f.n < 0 ? "-" : "") + "\\frac{" + Math.abs(f.n) + "}{" + f.d + "}"; }
  function frP(f) { f = fr(f); return f.sgn() < 0 ? "\\left(" + frT(f) + "\\right)" : frT(f); }
  function parseFr(s) {
    s = String(s).trim().replace(/[−–]/g, "-").replace(/,/g, ".").replace(/\s/g, "");
    var m = s.match(/^([+-]?)(\d+(?:\.\d+)?)(?:\/(\d+(?:\.\d+)?))?$/);
    if (!m) return null;
    function dec(t) { var i = t.indexOf("."); return i < 0 ? new Fr(+t) : new Fr(+t.replace(".", ""), Math.pow(10, t.length - i - 1)); }
    var v = dec(m[2]);
    if (m[3]) { var q = dec(m[3]); if (q.zero()) return null; v = v.div(q); }
    return m[1] === "-" ? v.neg() : v;
  }
  function isq(n) { if (n < 0) return null; var r = Math.round(Math.sqrt(n)); return r * r === n ? r : null; }
  function sqrtFr(f) { var a = isq(f.n), b = isq(f.d); return a != null && b != null ? new Fr(a, b) : null; }
  function simpSqrt(N) { var k = 1, m = N; for (var f = 2; f * f <= m; f++) while (m % (f * f) === 0) { m /= f * f; k *= f; } return [k, m]; }

  /* ---------- polinomis: llista de coeficients (Fr), de grau 0 cap amunt ---------- */
  function pTrim(p) { p = p.slice(); while (p.length > 1 && p[p.length - 1].zero()) p.pop(); return p.length ? p : [F0]; }
  function pDeg(p) { p = pTrim(p); return p.length === 1 && p[0].zero() ? -Infinity : p.length - 1; }
  function pAdd(a, b) { var r = []; for (var i = 0; i < Math.max(a.length, b.length); i++) r.push((a[i] || F0).add(b[i] || F0)); return pTrim(r); }
  function pScale(a, k) { return pTrim(a.map(function (c) { return c.mul(k); })); }
  function pSub(a, b) { return pAdd(a, pScale(b, FM1)); }
  function pMul(a, b) {
    var r = [];
    for (var i = 0; i < a.length; i++) for (var j = 0; j < b.length; j++) r[i + j] = (r[i + j] || F0).add(a[i].mul(b[j]));
    return pTrim(r);
  }
  function pDivide(D, d) {
    var dd = pDeg(d), q = [F0], r = pTrim(D), steps = [];
    while (pDeg(r) >= dd) {
      var e = pDeg(r) - dd, t = r[r.length - 1].div(d[dd]), mono = [];
      for (var i = 0; i < e; i++) mono.push(F0);
      mono.push(t);
      var prod = pMul(mono, d);
      q = pAdd(q, mono); r = pSub(r, prod);
      steps.push({ t: t, e: e, prod: prod, r: r, q: q });
    }
    return { q: q, r: r, steps: steps };
  }
  function pEval(p, x) { var v = F0; for (var i = p.length - 1; i >= 0; i--) v = v.mul(x).add(p[i]); return v; }
  function pEvalN(p, x) { var v = 0; for (var i = p.length - 1; i >= 0; i--) v = v * x + p[i].val(); return v; }
  function monT(c, e, v, first) {
    var s = c.sgn() < 0 ? "-" : (first ? "" : "+"), a = c.abs();
    var vp = e === 0 ? "" : e === 1 ? v : v + "^{" + e + "}";
    return s + ((e > 0 && a.eq(F1)) ? "" : frT(a)) + vp;
  }
  function pTex(p, v) { v = v || "x"; p = pTrim(p); var out = ""; for (var i = p.length - 1; i >= 0; i--) if (!p[i].zero()) out += monT(p[i], i, v, out === ""); return out || "0"; }
  function parsePoly(s) {
    if (s == null) return null;
    s = String(s).replace(/[−–]/g, "-").replace(/\s+/g, "").replace(/[·*]/g, "").replace(/²/g, "^2").replace(/³/g, "^3").replace(/⁴/g, "^4")
      .replace(/⁵/g, "^5").replace(/⁶/g, "^6").replace(/,/g, ".").replace(/X/g, "x");
    if (!s) return null;
    var terms = s.replace(/-/g, "+-").split("+"), p = [F0], n = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i]; if (t === "") continue;
      var m = t.match(/^(-?)(\d+(?:\.\d+)?(?:\/\d+(?:\.\d+)?)?)?(x(?:\^(\d{1,2}))?)?$/);
      if (!m || (!m[2] && !m[3])) return null;
      var c = m[2] ? parseFr(m[2]) : F1; if (!c) return null; if (m[1]) c = c.neg();
      var e = m[3] ? (m[4] ? +m[4] : 1) : 0; if (e > 12) return null;
      while (p.length <= e) p.push(F0);
      p[e] = p[e].add(c); n++;
    }
    return n ? pTrim(p) : null;
  }
  function divisors(n) {
    n = Math.abs(n); if (n === 0) return [1]; if (n > 1e7) return null;
    var r = []; for (var i = 1; i * i <= n; i++) if (n % i === 0) { r.push(i); if (i * i !== n) r.push(n / i); }
    return r.sort(function (a, b) { return a - b; });
  }
  // versió amb coeficients enters primers i coeficient principal positiu: p = k·P
  function intForm(p) {
    var L = 1; p.forEach(function (c) { L = L / gcd(L, c.d) * c.d; });
    var q = p.map(function (c) { return c.mul(L); }), g = 0;
    q.forEach(function (c) { g = gcd(g, c.n); });
    if (q[q.length - 1].n < 0) g = -g;
    return { P: q.map(function (c) { return c.div(g); }), k: new Fr(g, L) };
  }

  /* ---------- equació de segon grau exacta ---------- */
  function rRat(f) { return { v: f.val(), tex: frT(f), fr: f }; }
  function bsqT(B, m) { return B.eq(F1) ? "\\sqrt{" + m + "}" : B.d === 1 ? B.n + "\\sqrt{" + m + "}" : "\\frac{" + (B.n === 1 ? "" : B.n) + "\\sqrt{" + m + "}}{" + B.d + "}"; }
  function irrT(A, B, m, s) {
    var L = A.d / gcd(A.d, B.d) * B.d, pa = A.mul(L).n, kb = B.mul(L).n;
    var top = (pa ? pa : "") + (s < 0 ? "-" : pa ? "+" : "") + (kb === 1 ? "" : kb) + "\\sqrt{" + m + "}";
    return L === 1 ? top : "\\frac{" + top + "}{" + L + "}";
  }
  function rIrr(A, B, m, s) { return { v: A.val() + s * B.val() * Math.sqrt(m), tex: irrT(A, B, m, s), A: A, B: B, m: m, s: s }; }
  function quadRoots(a, b, c) {
    var D = b.mul(b).sub(new Fr(4).mul(a).mul(c)), res = { D: D, roots: [] };
    if (D.sgn() < 0) { res.kind = "none"; return res; }
    var A = b.neg().div(a.mul(2));
    if (D.zero()) { res.kind = "double"; res.roots = [rRat(A)]; return res; }
    var sq = sqrtFr(D);
    if (sq) {
      res.kind = "rat";
      res.roots = [rRat(b.neg().sub(sq).div(a.mul(2))), rRat(b.neg().add(sq).div(a.mul(2)))].sort(function (p, q) { return p.v - q.v; });
      return res;
    }
    var s = simpSqrt(D.n * D.d), B = new Fr(s[0], D.d).div(a.mul(2)).abs();
    res.kind = "irr"; res.sq = s; res.roots = [rIrr(A, B, s[1], -1), rIrr(A, B, s[1], 1)];
    return res;
  }
  function quadFormulaT(a, b, c, Q) {
    var D = Q.D, sD = "\\sqrt{" + frT(D) + "}";
    var s = "x=\\dfrac{" + (b.zero() ? "" : frT(b.neg())) + "\\pm" + sD + "}{" + frT(a.mul(2)) + "}";
    if (Q.kind === "rat") s += "=\\dfrac{" + (b.zero() ? "" : frT(b.neg())) + "\\pm" + frT(sqrtFr(D)) + "}{" + frT(a.mul(2)) + "}";
    return s;
  }

  /* ---------- gràfiques cartesianes ---------- */
  function niceStep(r) { var raw = r / 8, e = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / e; return e * (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10); }
  function gview(o) {
    var W = o.W || 360, H = o.H || 280, pl = 28, pr = 12, pt = 12, pb = 22;
    function X(x) { return pl + (x - o.x0) / (o.x1 - o.x0) * (W - pl - pr); }
    function Y(y) { return H - pb - (y - o.y0) / (o.y1 - o.y0) * (H - pt - pb); }
    var g = "", sx = o.sx || niceStep(o.x1 - o.x0), sy = o.sy || niceStep(o.y1 - o.y0), v;
    for (v = Math.ceil(o.x0 / sx) * sx; v <= o.x1 + 1e-9; v += sx) g += '<line class="g" x1="' + X(v) + '" x2="' + X(v) + '" y1="' + Y(o.y0) + '" y2="' + Y(o.y1) + '"/>';
    for (v = Math.ceil(o.y0 / sy) * sy; v <= o.y1 + 1e-9; v += sy) g += '<line class="g" x1="' + X(o.x0) + '" x2="' + X(o.x1) + '" y1="' + Y(v) + '" y2="' + Y(v) + '"/>';
    var ay = Math.max(o.y0, Math.min(o.y1, 0)), ax = Math.max(o.x0, Math.min(o.x1, 0));
    g += '<line class="ax" x1="' + X(o.x0) + '" x2="' + X(o.x1) + '" y1="' + Y(ay) + '" y2="' + Y(ay) + '"/><line class="ax" x1="' + X(ax) + '" x2="' + X(ax) + '" y1="' + Y(o.y0) + '" y2="' + Y(o.y1) + '"/>';
    function lb(t) { return String(+t.toFixed(6)).replace("-", "−").replace(".", lang === "en" ? "." : ","); }
    for (v = Math.ceil(o.x0 / sx) * sx; v <= o.x1 + 1e-9; v += sx) if (Math.abs(v) > 1e-9) g += '<text x="' + X(v) + '" y="' + (Y(ay) + 13) + '" text-anchor="middle">' + lb(v) + "</text>";
    for (v = Math.ceil(o.y0 / sy) * sy; v <= o.y1 + 1e-9; v += sy) if (Math.abs(v) > 1e-9) g += '<text x="' + (X(ax) - 4) + '" y="' + (Y(v) + 3.5) + '" text-anchor="end">' + lb(v) + "</text>";
    return { g: g, X: X, Y: Y, W: W, H: H, o: o };
  }
  function curve(G, f, color, opts) {
    opts = opts || {};
    var o = G.o, a = opts.a == null ? o.x0 : Math.max(o.x0, opts.a), b = opts.b == null ? o.x1 : Math.min(o.x1, opts.b), N = 400, d = "", pen = false, M = (o.y1 - o.y0) * 3;
    for (var i = 0; i <= N; i++) {
      var x = a + (b - a) * i / N, y = f(x);
      if (!isFinite(y) || y > o.y1 + M || y < o.y0 - M) { pen = false; continue; }
      y = Math.max(o.y0 - (o.y1 - o.y0), Math.min(o.y1 + (o.y1 - o.y0), y));
      d += (pen ? "L" : "M") + G.X(x).toFixed(1) + " " + G.Y(y).toFixed(1); pen = true;
    }
    return '<path d="' + d + '" fill="none" stroke="' + color + '" stroke-width="' + (opts.w || 2.6) + '"' + (opts.dash ? ' stroke-dasharray="' + opts.dash + '"' : "") + ' stroke-linejoin="round"/>';
  }
  function dot(G, x, y, color, r) { return '<circle cx="' + G.X(x) + '" cy="' + G.Y(y) + '" r="' + (r || 5.5) + '" fill="' + color + '" stroke="var(--bg)" stroke-width="1.5"/>'; }
  function clipSvg(svg, G) {
    var id = "cl" + Math.random().toString(36).slice(2, 8), o = G.o;
    return { open: '<defs><clipPath id="' + id + '"><rect x="' + G.X(o.x0) + '" y="' + G.Y(o.y1) + '" width="' + (G.X(o.x1) - G.X(o.x0)) + '" height="' + (G.Y(o.y0) - G.Y(o.y1)) + '"/></clipPath></defs><g clip-path="url(#' + id + ')">', close: "</g>" };
  }
  function polyView(p, roots) {
    var xs = roots.map(function (r) { return r.v; }).filter(isFinite);
    var x0 = Math.min(-3, Math.floor(Math.min.apply(null, xs.concat([0])) - 1.5)), x1 = Math.max(3, Math.ceil(Math.max.apply(null, xs.concat([0])) + 1.5));
    var ys = [], ym, i, r0 = Math.min.apply(null, xs.concat([0])), r1 = Math.max.apply(null, xs.concat([0]));
    if (r1 - r0 > 0.5) { for (i = 0; i <= 200; i++) ys.push(Math.abs(pEvalN(p, r0 - 0.4 + (r1 - r0 + 0.8) * i / 200))); ym = Math.max(2, Math.max.apply(null, ys) * 1.25); }
    else { for (i = 0; i <= 200; i++) ys.push(Math.abs(pEvalN(p, x0 + (x1 - x0) * i / 200))); ys.sort(function (a, b) { return a - b; }); ym = Math.max(2, ys[Math.floor(ys.length * 0.5)] * 1.3); }
    var e = Math.pow(10, Math.floor(Math.log10(ym))); ym = Math.ceil(ym / e) * e;
    return { x0: x0, x1: x1, y0: -ym, y1: ym };
  }

  /* ---------- controls de passos per als ginys ---------- */
  function stepper(w, getN, onShow) {
    var shown = 1, nb = $(w, "next"), ab = $(w, "all"), cnt = $(w, "cnt");
    function upd() {
      var n = getN(); if (shown > n) shown = n; if (shown < 0) shown = 0;
      nb.textContent = u("next") + " →"; nb.disabled = shown >= n;
      ab.textContent = shown >= n ? u("reset") : u("all");
      cnt.textContent = n ? u("step") + " " + shown + " " + u("of") + " " + n : "";
      onShow(shown);
    }
    nb.addEventListener("click", function () { shown++; upd(); });
    ab.addEventListener("click", function () { shown = shown >= getN() ? Math.min(1, getN()) : getN(); upd(); });
    return { upd: upd, reset: function (v) { shown = v == null ? 1 : v; upd(); } };
  }

  /* ---------- 3.3 rectes reals una sobre l'altra ---------- */
  // cada interval és [a, a inclòs, b, b inclòs]
  var INF = Infinity, STACKS = {
    a: { range: [-4, 5], rows: [{ l: "2x − 1 &lt; 5", S: [[-INF, 0, 3, 0]] }, { l: "x² − 4 ≥ 0", S: [[-INF, 0, -2, 1], [2, 1, INF, 0]] }], sol: [[-INF, 0, -2, 1], [2, 1, 3, 0]] },
    b: { range: [-3, 4], rows: [{ l: "x − 2 &gt; 0", S: [[2, 0, INF, 0]] }, { l: "x + 1 &lt; 0", S: [[-INF, 0, -1, 0]] }], sol: [] }
  };
  function svgW(svg) { var w = svg.getBoundingClientRect().width; return w ? Math.max(300, Math.min(600, Math.round(w))) : 600; }
  function nstack(d, showSol, W) {
    var L = 92, R = W - 24, rowH = 36, top = 8, lo = d.range[0], hi = d.range[1];
    var rows = d.rows.map(function (r, i) { return { l: r.l, S: r.S, c: [COL.a, COL.b][i] }; });
    if (showSol) rows.push({ l: t3("Solució", "Solución", "Solution"), S: d.sol, c: COL.r, sol: true });
    function X(v) { return L + (Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo) * (R - L); }
    var ay = top + rows.length * rowH + 8, H = ay + 26, g = "", marks = {};
    if (showSol) d.sol.forEach(function (I) { g += '<rect x="' + X(I[0]) + '" y="' + top + '" width="' + (X(I[2]) - X(I[0])) + '" height="' + (ay - top) + '" fill="' + COL.r + '" fill-opacity=".12"/>'; });
    d.rows.forEach(function (r) { r.S.forEach(function (I) { [I[0], I[2]].forEach(function (v) { if (isFinite(v)) marks[v] = 1; }); }); });
    Object.keys(marks).forEach(function (v) { g += '<line class="gd" x1="' + X(+v) + '" x2="' + X(+v) + '" y1="' + top + '" y2="' + ay + '"/>'; });
    rows.forEach(function (r, i) {
      var y = top + i * rowH + 18;
      g += '<text class="lb" x="6" y="' + (y + 4) + '">' + r.l + "</text>";
      g += '<line class="gl" x1="' + L + '" x2="' + R + '" y1="' + y + '" y2="' + y + '"/>';
      if (r.sol && !r.S.length) g += '<text class="lb" x="' + (L + R) / 2 + '" y="' + (y - 5) + '" text-anchor="middle">∅</text>';
      r.S.forEach(function (I) {
        var x1 = X(I[0]), x2 = X(I[2]);
        g += '<line x1="' + x1 + '" x2="' + x2 + '" y1="' + y + '" y2="' + y + '" stroke="' + r.c + '" stroke-width="5"/>';
        if (I[0] === -INF) g += '<path d="M' + (L - 9) + " " + y + ' l11 -7 v14 z" fill="' + r.c + '"/>';
        if (I[2] === INF) g += '<path d="M' + (R + 9) + " " + y + ' l-11 -7 v14 z" fill="' + r.c + '"/>';
        [[I[0], I[1], x1], [I[2], I[3], x2]].forEach(function (e) {
          if (isFinite(e[0])) g += '<circle cx="' + e[2] + '" cy="' + y + '" r="5.5" stroke="' + r.c + '" stroke-width="2.2"' + (e[1] ? ' fill="' + r.c + '"' : ' class="op"') + "/>";
        });
      });
    });
    g += '<line class="ax" x1="' + (L - 6) + '" x2="' + (R + 12) + '" y1="' + ay + '" y2="' + ay + '"/><path d="M' + (R + 16) + " " + ay + ' l-8 -4 v8 z" fill="var(--muted)"/>';
    for (var v = lo; v <= hi; v++) g += '<line class="tk" x1="' + X(v) + '" x2="' + X(v) + '" y1="' + (ay - 5) + '" y2="' + (ay + 5) + '"/><text x="' + X(v) + '" y="' + (ay + 18) + '" text-anchor="middle">' + String(v).replace("-", "−") + "</text>";
    return { svg: g, H: H };
  }
  function wStacks() {
    document.querySelectorAll("svg[data-stack]").forEach(function (svg) {
      var d = STACKS[svg.getAttribute("data-stack")], sol = svg.getAttribute("data-sol") === "1", last = 0;
      function draw(force) { var W = svgW(svg); if (W === last && !force) return; last = W; var r = nstack(d, sol, W); svg.setAttribute("viewBox", "0 0 " + W + " " + r.H); svg.innerHTML = r.svg; }
      onLang(function () { draw(true); });
      // els passos amagats no tenen amplària: es torna a dibuixar quan apareixen o canvia la pantalla
      if (window.ResizeObserver) new ResizeObserver(function () { draw(false); }).observe(svg);
    });
  }

  /* ---------- 3.1 mètode de Gauss ---------- */
  function wGauss() {
    var w = byId("w-gauss"); if (!w) return;
    var grid = $(w, "grid"), out = $(w, "steps"), info = w.querySelector(".info"), ins = [], st, res;
    var PRE = [[[1, 1, 1, 6], [2, -1, 1, 3], [1, 2, -1, 2]], [[1, -1, 1, 1], [2, 1, -1, 5], [1, 2, -2, 4]], [[1, -1, 1, 1], [2, 1, -1, 5], [1, 2, -2, 5]], [[2, 1, 1, 5], [2, -1, 3, 3], [3, 2, 1, 8]]];
    for (var i = 0; i < 3; i++) for (var j = 0; j < 4; j++) {
      var inp = document.createElement("input"); inp.className = "tin s" + (j === 3 ? " rhs" : ""); inp.inputMode = "decimal"; inp.autocomplete = "off"; inp.value = PRE[0][i][j];
      inp.setAttribute("aria-label", (j < 3 ? "xyz"[j] : "=") + " (" + (i + 1) + ")");
      inp.addEventListener("input", read); grid.appendChild(inp); ins.push(inp);
    }
    presetBtns($(w, "pre"), function () { return [t3("Exemple SCD", "Ejemplo SCD", "Example (unique)"), t3("Exemple SCI", "Ejemplo SCI", "Example (infinite)"), t3("Exemple SI", "Ejemplo SI", "Example (none)"), t3("Exercici 2c", "Ejercicio 2c", "Exercise 2c")]; }, function (k) {
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

  /* ---------- 3.2 recta i circumferència ---------- */
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


  /* ---------- 3.5 semiplans i sistemes ---------- */
  var OPT = { "<": "\\lt ", "<=": "\\le ", ">": "\\gt ", ">=": "\\ge " };
  function clipHalf(P, A, B, C, s) {
    var out = [], n = P.length; if (!n) return out;
    function val(p) { return s * (A * p[0] + B * p[1] - C); }
    for (var i = 0; i < n; i++) {
      var p = P[i], q = P[(i + 1) % n], vp = val(p), vq = val(q);
      if (vp <= 1e-9) out.push(p);
      if ((vp < -1e-9 && vq > 1e-9) || (vp > 1e-9 && vq < -1e-9)) { var t = vp / (vp - vq); out.push([p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])]); }
    }
    var r = []; out.forEach(function (p) { if (!r.length || Math.abs(r[r.length - 1][0] - p[0]) + Math.abs(r[r.length - 1][1] - p[1]) > 1e-7) r.push(p); });
    while (r.length > 1 && Math.abs(r[0][0] - r[r.length - 1][0]) + Math.abs(r[0][1] - r[r.length - 1][1]) < 1e-7) r.pop();
    return r;
  }
  function region(cons, b) {
    var P = [[b[0], b[2]], [b[1], b[2]], [b[1], b[3]], [b[0], b[3]]];
    cons.forEach(function (c) { P = clipHalf(P, c.a, c.b, c.c, c.op.charAt(0) === "<" ? 1 : -1); });
    return P;
  }
  function consT(c) {
    var s = pTex([F0, toFr(c.a)]).replace(/^0$/, ""), y = c.b ? monT(toFr(c.b), 1, "y", !s) : "";
    return (s + y || "0") + OPT[c.op] + nT(c.c);
  }
  function wHalf() {
    var w = byId("w-half"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg"), rowsBox = $(w, "rows"), R = [];
    var OPS = ["<", "<=", ">", ">="], SYM = { "<": "<", "<=": "≤", ">": ">", ">=": "≥" };
    for (var i = 0; i < 4; i++) {
      var row = document.createElement("div"); row.className = "hrow";
      var cb = document.createElement("input"); cb.type = "checkbox"; cb.checked = true;
      var ia = mk("1"), ib = mk("1"), ic = mk("4"), sel = document.createElement("select");
      OPS.forEach(function (o) { sel.add(new Option(SYM[o], o)); });
      var dotc = document.createElement("i"); dotc.className = "dot"; dotc.style.background = [COL.a, COL.b, COL.v, COL.k][i];
      [cb, dotc, ia, txt("x +"), ib, txt("y"), sel, ic].forEach(function (e) { row.appendChild(e); });
      rowsBox.appendChild(row); R.push({ cb: cb, a: ia, b: ib, op: sel, c: ic });
      [cb, ia, ib, sel, ic].forEach(function (e) { e.addEventListener("input", draw); e.addEventListener("change", draw); });
    }
    function mk(v) { var x = document.createElement("input"); x.className = "tin s"; x.inputMode = "decimal"; x.autocomplete = "off"; x.value = v; return x; }
    function txt(t) { var s = document.createElement("span"); s.textContent = t; return s; }
    var PRE = [
      [[1, 1, "<=", 4], [-1, 1, ">=", -2], [1, 0, ">=", 0], [0, 1, ">=", 0]],
      [[2, 1, "<", 4], [-1, 1, ">=", 0], null, null],
      [[1, 1, "<=", 6], [-1, 2, "<=", 0], [1, 0, ">=", 0], null],
      [[0, 1, ">=", 3], [0, 1, "<=", 5], [1, 0, "<=", 6], [1, 0, ">=", 4]]
    ];
    function applyPre(k) { PRE[k].forEach(function (c, i) { R[i].cb.checked = !!c; if (c) { R[i].a.value = c[0]; R[i].b.value = c[1]; R[i].op.value = c[2]; R[i].c.value = c[3]; } }); }
    applyPre(0);
    presetBtns($(w, "pre"), function () { return [t3("Exemple dels apunts", "Ejemplo de los apuntes", "Notes example"), "8 b)", "8 d)", "8 f)"]; }, function (k) { applyPre(k); draw(); }, 0);
    function draw() {
      var cons = [], bad = false;
      R.forEach(function (r, i) {
        var a = parseFr(r.a.value || "0"), b = parseFr(r.b.value || "0"), c = parseFr(r.c.value || "0");
        [r.a, r.b, r.c].forEach(function (e) { e.classList.toggle("bad", r.cb.checked && !parseFr(e.value || "0")); });
        r.a.parentNode.classList.toggle("off", !r.cb.checked);
        if (!r.cb.checked) return;
        if (!a || !b || !c || (a.zero() && b.zero())) { bad = true; return; }
        cons.push({ a: a.val(), b: b.val(), c: c.val(), op: r.op.value, col: [COL.a, COL.b, COL.v, COL.k][i] });
      });
      var V = [-3, 9, -3, 9], G = gview({ x0: V[0], x1: V[1], y0: V[2], y1: V[3], W: 340, H: 340, sx: 1, sy: 1 }), Cl = clipSvg(svg, G), g = G.g + Cl.open;
      var P = region(cons, V);
      if (P.length >= 3) g += '<path d="M' + P.map(function (p) { return G.X(p[0]).toFixed(1) + " " + G.Y(p[1]).toFixed(1); }).join("L") + 'Z" fill="' + COL.r + '" fill-opacity=".22"/>';
      cons.forEach(function (c) {
        var pts = Math.abs(c.b) > 1e-12 ? [[V[0] - 1, (c.c - c.a * (V[0] - 1)) / c.b], [V[1] + 1, (c.c - c.a * (V[1] + 1)) / c.b]] : [[c.c / c.a, V[2] - 1], [c.c / c.a, V[3] + 1]];
        g += '<line x1="' + G.X(pts[0][0]) + '" y1="' + G.Y(pts[0][1]) + '" x2="' + G.X(pts[1][0]) + '" y2="' + G.Y(pts[1][1]) + '" stroke="' + c.col + '" stroke-width="2.4"' + (c.op.length === 1 ? ' stroke-dasharray="7 5"' : "") + "/>";
      });
      var BIG = 1e6, PB = region(cons, [-BIG, BIG, -BIG, BIG]), verts = PB.filter(function (p) { return Math.abs(p[0]) < BIG / 2 && Math.abs(p[1]) < BIG / 2; });
      verts.forEach(function (p) { g += dot(G, p[0], p[1], "var(--text)", 4); });
      svg.setAttribute("viewBox", "0 0 " + G.W + " " + G.H); svg.innerHTML = g + Cl.close;
      if (bad) { info.innerHTML = t3("Revisa els coeficients (a i b no poden ser tots dos 0).", "Revisa los coeficientes (a y b no pueden ser ambos 0).", "Check the coefficients (a and b can't both be 0)."); return; }
      var rows = cons.map(function (c) {
        var tp = Math.abs(c.c) > 1e-12 ? [0, 0] : Math.abs(c.a) > 1e-12 ? [1, 0] : [0, 1], v = c.a * tp[0] + c.b * tp[1];
        var holds = { "<": v < c.c, "<=": v <= c.c, ">": v > c.c, ">=": v >= c.c }[c.op];
        return ['<i class="dot" style="background:' + c.col + '"></i>' + tex(consT(c)), t3("recta ", "recta ", "line ") + (c.op.length === 1 ? t3("discontínua", "discontinua", "dashed") : t3("contínua", "continua", "solid")) + "; " + tex("(" + tp.join(",") + "):\\ " + nT(v) + OPT[c.op] + nT(c.c)) + " " + ok(holds) + " → " + (holds ? t3("semiplà del punt", "semiplano del punto", "the point's side") : t3("l'altre semiplà", "el otro semiplano", "the other side"))];
      });
      if (!cons.length) rows.push(["", t3("Activa alguna inequació.", "Activa alguna inecuación.", "Turn on an inequality.")]);
      else if (PB.length < 3) rows.push([t3("Solució", "Solución", "Solution"), t3("No hi ha cap punt que complisca totes les inequacions.", "No hay ningún punto que cumpla todas las inecuaciones.", "No point satisfies all the inequalities.")]);
      else {
        var bounded = verts.length === PB.length;
        rows.push([t3("Regió", "Región", "Region"), bounded ? t3("fitada (un polígon)", "acotada (un polígono)", "bounded (a polygon)") : t3("no fitada", "no acotada", "unbounded")]);
        if (verts.length) rows.push([t3("Vèrtexs", "Vértices", "Vertices"), tex(verts.map(function (p) { return "(" + nT(p[0]) + ",\\," + nT(p[1]) + ")"; }).join(",\\ "))]);
      }
      info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 3.4 i 3.5: figures dels exemples ---------- */
  function halfLine(G, c, V, col) {
    var pts = Math.abs(c.b) > 1e-12 ? [[V[0] - 1, (c.c - c.a * (V[0] - 1)) / c.b], [V[1] + 1, (c.c - c.a * (V[1] + 1)) / c.b]] : [[c.c / c.a, V[2] - 1], [c.c / c.a, V[3] + 1]];
    return '<line x1="' + G.X(pts[0][0]) + '" y1="' + G.Y(pts[0][1]) + '" x2="' + G.X(pts[1][0]) + '" y2="' + G.Y(pts[1][1]) + '" stroke="' + col + '" stroke-width="2.4"' + (c.op.length === 1 ? ' stroke-dasharray="7 5"' : "") + "/>";
  }
  function halfFill(G, P) { return P.length >= 3 ? '<path d="M' + P.map(function (p) { return G.X(p[0]).toFixed(1) + " " + G.Y(p[1]).toFixed(1); }).join("L") + 'Z" fill="' + COL.r + '" fill-opacity=".22"/>' : ""; }
  function wFigs() {
    var OP = { lt: "<", le: "<=", gt: ">", ge: ">=" }, CS = [COL.a, COL.b, COL.v, COL.k];
    document.querySelectorAll("svg[data-half]").forEach(function (svg) {
      var V = svg.getAttribute("data-view").split(",").map(Number);
      var cons = svg.getAttribute("data-half").split(";").map(function (s) { var p = s.split(","); return { a: +p[0], b: +p[1], op: OP[p[2]], c: +p[3] }; });
      var G = gview({ x0: V[0], x1: V[1], y0: V[2], y1: V[3], W: 320, H: 320, sx: 1, sy: 1 }), Cl = clipSvg(svg, G), g = G.g + Cl.open + halfFill(G, region(cons, V));
      cons.forEach(function (c, i) { g += halfLine(G, c, V, CS[i % 4]); });
      var pt = svg.getAttribute("data-pt");
      if (pt) { var q = pt.split(",").map(Number); g += dot(G, q[0], q[1], q[2] ? COL.k : COL.r, 6); }
      svg.setAttribute("viewBox", "0 0 320 320"); svg.innerHTML = g + Cl.close;
    });
  }

  /* ---------- 3.4 inequació amb dues incògnites pas a pas ---------- */
  function wSemi() {
    var w = byId("w-semi"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg"), ia = $(w, "a"), ib = $(w, "b"), ic = $(w, "c"), sel = $(w, "op"), st, res;
    var SYM = { "<": "<", "<=": "≤", ">": ">", ">=": "≥" };
    Object.keys(SYM).forEach(function (o) { sel.add(new Option(SYM[o], o)); });
    var PRE = [[3, 4, "<=", 12], [-3, 4, ">=", 4], [2, 1, "<", 2], [1, -1, ">", -2]];
    function set(p) { ia.value = p[0]; ib.value = p[1]; sel.value = p[2]; ic.value = p[3]; }
    set(PRE[0]);
    presetBtns($(w, "pre"), function () { return ["a", "b", "c", "d"].map(function (l) { return t3("Exercici 7", "Ejercicio 7", "Exercise 7") + l; }); }, function (k) { set(PRE[k]); read(); }, 0);
    function calc(a, b, c, op) {
      var P, x0;
      if (b.zero()) { x0 = c.div(a); P = [[x0, F0], [x0, F1]]; }
      else if (a.zero()) { x0 = c.div(b); P = [[F0, x0], [F1, x0]]; }
      else if (c.zero()) P = [[F0, F0], [b, a.neg()]];
      else P = [[c.div(a), F0], [F0, c.div(b)]];
      var t = !c.zero() ? [0, 0] : !a.zero() ? [1, 0] : [0, 1], v = a.val() * t[0] + b.val() * t[1], cv = c.val();
      return { a: a, b: b, c: c, op: op, P: P, t: t, v: v, holds: { "<": v < cv, "<=": v <= cv, ">": v > cv, ">=": v >= cv }[op] };
    }
    function read() {
      var a = parseFr(ia.value || "0"), b = parseFr(ib.value || "0"), c = parseFr(ic.value || "0");
      ia.classList.toggle("bad", !a); ib.classList.toggle("bad", !b); ic.classList.toggle("bad", !c);
      res = a && b && c && !(a.zero() && b.zero()) ? calc(a, b, c, sel.value) : null;
      st.reset(1);
    }
    function draw(k) {
      var m = 6;
      if (res) res.P.forEach(function (p) { m = Math.max(m, Math.ceil(Math.abs(p[0].val())) + 1, Math.ceil(Math.abs(p[1].val())) + 1); });
      var V = [-m, m, -m, m], fine = m <= 8, G = gview({ x0: -m, x1: m, y0: -m, y1: m, W: 340, H: 340, sx: fine ? 1 : undefined, sy: fine ? 1 : undefined }), Cl = clipSvg(svg, G), g = G.g + Cl.open;
      if (res) {
        var c = { a: res.a.val(), b: res.b.val(), c: res.c.val(), op: res.op };
        if (k >= 4) g += halfFill(G, region([c], V));
        if (k >= 2) {
          g += halfLine(G, c, V, COL.a);
          res.P.forEach(function (p) { var x = p[0].val(), y = p[1].val(); var lb = y === 0 && x !== 0 ? ' x="' + G.X(x) + '" y="' + (G.Y(y) + 24) + '" text-anchor="middle"' : ' x="' + (G.X(x) + 7) + '" y="' + (G.Y(y) - 7) + '"';
            g += dot(G, x, y, "var(--text)", 4) + "<text" + lb + ' style="fill:var(--text)">(' + nS(x) + ", " + nS(y) + ")</text>"; });
        }
        if (k >= 3) g += dot(G, res.t[0], res.t[1], res.holds ? COL.k : COL.r, 6);
      }
      svg.setAttribute("viewBox", "0 0 " + G.W + " " + G.H); svg.innerHTML = g + Cl.close;
    }
    function ptT(p) { return "(" + frT(p[0]) + ",\\," + frT(p[1]) + ")"; }
    function subT() {
      return [[res.a, res.t[0]], [res.b, res.t[1]]].filter(function (e) { return !e[0].zero(); }).map(function (e) { return (e[0].sgn() < 0 ? "(" + frT(e[0]) + ")" : frT(e[0])) + "\\cdot " + e[1]; }).join("+");
    }
    function show(k) {
      if (!res) { info.innerHTML = t3("Revisa els coeficients (a i b no poden ser tots dos 0).", "Revisa los coeficientes (a y b no pueden ser ambos 0).", "Check the coefficients (a and b can't both be 0)."); draw(0); return; }
      var c = { a: res.a.val(), b: res.b.val(), c: res.c.val(), op: res.op }, solid = res.op.length === 2, L = function (i) { return u("step") + " " + i; };
      var rows = [[L(1), t3("Recta frontera: canviem la desigualtat per un igual.", "Recta frontera: cambiamos la desigualdad por un igual.", "Boundary line: replace the inequality sign with an equals sign.") + "<br>" + tex(consT({ a: c.a, b: c.b, c: c.c, op: "<=" }).replace("\\le ", "="))]];
      if (k >= 2) rows.push([L(2), t3("Dos punts de la recta: ", "Dos puntos de la recta: ", "Two points on the line: ") + tex(ptT(res.P[0])) + t3(" i ", " y ", " and ") + tex(ptT(res.P[1])) + ".<br>" +
        (solid ? t3("Recta contínua: la desigualtat inclou l'igual, els punts de la recta són solució.", "Recta continua: la desigualdad incluye el igual, los puntos de la recta son solución.", "Solid line: the inequality includes equality, so points on the line are solutions.")
          : t3("Recta discontínua: la desigualtat és estricta, els punts de la recta no són solució.", "Recta discontinua: la desigualdad es estricta, los puntos de la recta no son solución.", "Dashed line: the inequality is strict, so points on the line are not solutions."))]);
      if (k >= 3) rows.push([L(3), t3("Punt de prova ", "Punto de prueba ", "Test point ") + tex("(" + res.t.join(",\\,") + ")") + ":<br>" + tex(subT() + "=" + nT(res.v) + OPT[res.op] + nT(c.c)) + " " + ok(res.holds)]);
      if (k >= 4) rows.push([L(4), res.holds ? t3("El punt compleix la inequació: la solució és el semiplà que el conté.", "El punto cumple la inecuación: la solución es el semiplano que lo contiene.", "The point satisfies the inequality: the solution is the half-plane containing it.")
        : t3("El punt no compleix la inequació: la solució és el semiplà que no el conté.", "El punto no cumple la inecuación: la solución es el semiplano que no lo contiene.", "The point does not satisfy the inequality: the solution is the half-plane not containing it.")]);
      info.innerHTML = kv(rows);
      draw(k);
    }
    [ia, ib, ic].forEach(function (e) { e.addEventListener("input", read); });
    sel.addEventListener("change", read);
    st = stepper(w, function () { return res ? 4 : 0; }, show);
    read(); onLang(function () { st.upd(); });
  }

  /* ---------- autoavaluació ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("En aplicar Gauss, l'última fila queda $\\left(0\\ \\ 0\\ \\ 0\\,|\\,3\\right)$. El sistema és…", "Al aplicar Gauss, la última fila queda $\\left(0\\ \\ 0\\ \\ 0\\,|\\,3\\right)$. El sistema es…", "After Gauss, the last row is $\\left(0\\ \\ 0\\ \\ 0\\,|\\,3\\right)$. The system is…"),
      o: [q3("SCD"), q3("SCI"), q3("SI")], a: 2, e: q3("L'equació $0=3$ és impossible: incompatible.", "La ecuación $0=3$ es imposible: incompatible.", "The equation $0=3$ is impossible: inconsistent.") },
    { q: q3("Un sistema amb infinites solucions és…", "Un sistema con infinitas soluciones es…", "A system with infinitely many solutions is…"),
      o: [q3("SCD"), q3("SCI"), q3("SI")], a: 1, e: q3("Compatible indeterminat: les solucions depenen d'un paràmetre.", "Compatible indeterminado: las soluciones dependen de un parámetro.", "Consistent and dependent: the solutions depend on a parameter.") },
    { q: q3("El sistema $x+y=0,\\ xy=1$…", "El sistema $x+y=0,\\ xy=1$…", "The system $x+y=0,\\ xy=1$…"),
      o: [q3("té dues solucions reals", "tiene dos soluciones reales", "has two real solutions"), q3("té una solució real", "tiene una solución real", "has one real solution"), q3("no té solució real", "no tiene solución real", "has no real solution")], a: 2, e: q3("Substituint $y=-x$: $-x^2=1$, que no té solució real.", "Sustituyendo $y=-x$: $-x^2=1$, que no tiene solución real.", "Substituting $y=-x$: $-x^2=1$, which has no real solution.") },
    { q: q3("La solució del sistema $x\\gt1,\\ x\\le4$ és…", "La solución del sistema $x\\gt1,\\ x\\le4$ es…", "The solution of the system $x\\gt1,\\ x\\le4$ is…"),
      o: [q3("$[1,4]$"), q3("$(1,4]$"), q3("$(-\\infty,4]$")], a: 1, e: q3("És la intersecció de $(1,+\\infty)$ i $(-\\infty,4]$.", "Es la intersección de $(1,+\\infty)$ y $(-\\infty,4]$.", "It is the intersection of $(1,+\\infty)$ and $(-\\infty,4]$.") },
    { q: q3("El punt $(0,0)$ compleix $2x-y\\gt3$?", "¿El punto $(0,0)$ cumple $2x-y\\gt3$?", "Does $(0,0)$ satisfy $2x-y\\gt3$?"),
      o: [q3("Sí", "Sí", "Yes"), q3("No: la solució és el semiplà que no conté l'origen", "No: la solución es el semiplano que no contiene el origen", "No: the solution is the half-plane not containing the origin")], a: 1, e: q3("$0\\gt3$ és fals.", "$0\\gt3$ es falso.", "$0\\gt3$ is false.") },
    { q: q3("Com es dibuixa la recta frontera de $3x+y\\le6$?", "¿Cómo se dibuja la recta frontera de $3x+y\\le6$?", "How do you draw the boundary line of $3x+y\\le6$?"),
      o: [q3("Contínua", "Continua", "Solid"), q3("Discontínua", "Discontinua", "Dashed")], a: 0, e: q3("Amb $\\le$ o $\\ge$ els punts de la recta formen part de la solució.", "Con $\\le$ o $\\ge$ los puntos de la recta forman parte de la solución.", "With $\\le$ or $\\ge$ the points on the line are part of the solution.") },
    { q: q3("Tenim 10 monedes d'1 € i de 2 € que sumen 13 €. Quantes en són de 2 €?", "Tenemos 10 monedas de 1 € y de 2 € que suman 13 €. ¿Cuántas son de 2 €?", "We have 10 coins of €1 and €2 adding up to €13. How many are €2 coins?"),
      o: [q3("$3$"), q3("$5$"), q3("$7$")], a: 0, e: q3("$x+y=10,\\ x+2y=13$: restant, $y=3$.", "$x+y=10,\\ x+2y=13$: restando, $y=3$.", "$x+y=10,\\ x+2y=13$: subtracting, $y=3$.") }
  ];

  /*@@GENERIC@@*/
  var TITLES = { va: "Sistemes d'equacions i inequacions · FentMates", es: "Sistemas de ecuaciones e inecuaciones · FentMates", en: "Systems of equations and inequalities · FentMates" };
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
    var all = [wChrome, wSteps, wNav, wStacks, wFigs, wGauss, wNl, wSemi, wHalf, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
