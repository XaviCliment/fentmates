(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-4eso-a-u4-done";

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

  /* ---------- Ruffini ---------- */
  function ruffini(p, a) {
    var c = pTrim(p).slice().reverse(), prod = [null], res = [c[0]];
    for (var i = 1; i < c.length; i++) { var m = res[i - 1].mul(a); prod.push(m); res.push(c[i].add(m)); }
    return { c: c, prod: prod, res: res, q: pTrim(res.slice(0, -1).reverse()), r: res[res.length - 1] };
  }
  function rufHtml(R, a, upto) {
    var n = R.c.length; if (upto == null) upto = n;
    function cell(f, cls) { return "<td" + (cls ? ' class="' + cls + '"' : "") + ">" + (f ? tex(frT(f)) : "") + "</td>"; }
    var h = '<table class="rf">';
    h += "<tr><td></td>" + R.c.map(function (f, i) { return cell(f, i === n - 1 ? "rl" : ""); }).join("") + "</tr>";
    h += "<tr><td>" + tex(frT(a)) + "</td>" + R.prod.map(function (f, i) { return cell(i < upto ? f : null, i === n - 1 ? "rl" : ""); }).join("") + "</tr>";
    h += "<tr><td></td>" + R.res.map(function (f, i) { return cell(i < upto ? f : null, i === n - 1 ? "rl rr" : ""); }).join("") + "</tr></table>";
    return h;
  }

  /* ---------- factorització ---------- */
  function numRoots(p) {
    var an = Math.abs(p[p.length - 1].val()), B = 1;
    p.forEach(function (c, i) { if (i < p.length - 1) B = Math.max(B, 1 + Math.abs(c.val()) / an); });
    var out = [], N = 4000, x0 = -B, f0 = pEvalN(p, x0);
    for (var i = 1; i <= N; i++) {
      var x1 = -B + 2 * B * i / N, f1 = pEvalN(p, x1);
      if (f0 === 0) out.push(x0);
      else if (f0 * f1 < 0) { var a = x0, b = x1, fa = f0; for (var k = 0; k < 60; k++) { var m = (a + b) / 2, fm = pEvalN(p, m); if (fa * fm <= 0) b = m; else { a = m; fa = fm; } } out.push((a + b) / 2); }
      x0 = x1; f0 = f1;
    }
    return out;
  }
  function linT(r) { // factor lineal amb coeficients enters que té l'arrel r
    if (r.zero()) return "x";
    var q = r.d === 1 ? "" : String(r.d);
    return q + "x" + (r.n > 0 ? "-" + r.n : "+" + (-r.n));
  }
  function irrFacT(rt) { var A = rt.A; return "x" + (A.zero() ? "" : A.sgn() > 0 ? "-" + frT(A) : "+" + frT(A.neg())) + (rt.s > 0 ? "-" : "+") + bsqT(rt.B, rt.m); }
  function factorPoly(p0) {
    var p = pTrim(p0), out = { steps: [], lin: [], irr: [], rest: [], k: 0, approx: [] };
    if (pDeg(p) < 1) { out.c = p[0]; out.isConst = true; return out; }
    var k = 0; while (p[k].zero()) k++;
    out.k = k; p = p.slice(k); out.afterK = p;
    var lead = p[p.length - 1], prodLead = F1;
    function addLin(r, m) {
      var L = out.lin.filter(function (x) { return x.r.eq(r); })[0];
      if (L) L.m += m; else { out.lin.push({ r: r, m: m }); }
      prodLead = prodLead.mul(new Fr(Math.pow(r.d, m)));
    }
    function addRest(P, m) {
      var I = intForm(P), key = pTex(I.P), R = out.rest.filter(function (x) { return x.key === key; })[0];
      if (R) R.m += m; else out.rest.push({ P: I.P, m: m, key: key });
      for (var i = 0; i < m; i++) prodLead = prodLead.mul(I.P[I.P.length - 1]);
    }
    var cur = p;
    if (pDeg(cur) > 2) {
      var I = intForm(cur), dp = divisors(I.P[0].n), dq = divisors(I.P[I.P.length - 1].n), cands = [];
      if (dp && dq) {
        dq.forEach(function (q) { dp.forEach(function (pp) { [pp, -pp].forEach(function (s) { var f = new Fr(s, q); if (!cands.some(function (c) { return c.eq(f); })) cands.push(f); }); }); });
        out.cands = dp; out.candsQ = dq;
        for (var i = 0; i < cands.length && pDeg(cur) > 2; i++) {
          var r = cands[i], m = 0;
          while (pDeg(cur) > 2 && pEval(cur, r).zero()) { var R = ruffini(cur, r); out.steps.push({ type: "ruf", R: R, a: r, P: cur }); cur = R.q; m++; }
          if (m) addLin(r, m);
        }
      }
    }
    var d = pDeg(cur);
    if (d === 1) addLin(cur[0].neg().div(cur[1]), 1);
    else if (d === 2) {
      var Q = quadRoots(cur[2], cur[1], cur[0]);
      out.steps.push({ type: "quad", P: cur, Q: Q });
      if (Q.kind === "double") addLin(Q.roots[0].fr, 2);
      else if (Q.kind === "rat") Q.roots.forEach(function (x) { addLin(x.fr, 1); });
      else if (Q.kind === "irr") { Q.m = 1; out.irr.push(Q); }
      else addRest(cur, 1);
    } else if (d === 4 && cur[1].zero() && cur[3].zero()) {
      var T = quadRoots(cur[4], cur[2], cur[0]);
      out.steps.push({ type: "biq", P: cur, Q: T });
      if (T.kind === "rat" || T.kind === "double") {
        T.roots.forEach(function (t) {
          var mm = T.kind === "double" ? 2 : 1, tf = t.fr;
          if (tf.sgn() < 0 || tf.zero()) addRest([tf.neg(), F0, F1], mm);
          else { var Qx = quadRoots(F1, F0, tf.neg()); Qx.m = mm; out.irr.push(Qx); }
        });
      } else { addRest(cur, 1); numRoots(cur).forEach(function (x) { out.approx.push(x); }); }
    } else if (d >= 3) { addRest(cur, 1); numRoots(cur).forEach(function (x) { out.approx.push(x); }); }
    out.c = lead.div(prodLead);
    out.roots = [];
    if (k) out.roots.push({ v: 0, tex: "0", m: k });
    out.lin.forEach(function (L) { out.roots.push({ v: L.r.val(), tex: frT(L.r), m: L.m }); });
    out.irr.forEach(function (Q) { Q.roots.forEach(function (x) { out.roots.push({ v: x.v, tex: x.tex, m: Q.m, irr: x }); }); });
    out.approx.forEach(function (x) { out.roots.push({ v: x, tex: "\\approx " + dT(x, 3), m: 1, ap: true }); });
    out.roots.sort(function (a, b) { return a.v - b.v; });
    return out;
  }
  function facParts(F) {
    var parts = [];
    if (F.k) parts.push(F.k === 1 ? "x" : "x^{" + F.k + "}");
    F.lin.forEach(function (L) { if (L.m > 0) parts.push((L.r.zero() ? "x" : "(" + linT(L.r) + ")") + (L.m > 1 ? "^{" + L.m + "}" : "")); });
    F.irr.forEach(function (Q) { if (Q.m > 0) Q.roots.forEach(function (x) { parts.push("\\left(" + irrFacT(x) + "\\right)" + (Q.m > 1 ? "^{" + Q.m + "}" : "")); }); });
    F.rest.forEach(function (R) { if (R.m > 0) parts.push("(" + pTex(R.P) + ")" + (R.m > 1 ? "^{" + R.m + "}" : "")); });
    return parts;
  }
  function facTex(F, c) {
    if (c === undefined) c = F.c;
    var parts = facParts(F);
    if (!parts.length) return frT(c);
    if (parts.length === 1 && F.rest.length === 1 && F.rest[0].m === 1 && !F.k && c.eq(F1)) return pTex(F.rest[0].P);
    return (c.eq(F1) ? "" : c.eq(FM1) ? "-" : frT(c)) + parts.join("");
  }
  function multName(m) { return m === 2 ? t3("doble", "doble", "double") : m === 3 ? t3("triple", "triple", "triple") : m > 3 ? t3("de multiplicitat ", "de multiplicidad ", "multiplicity ") + m : ""; }
  function rootsList(F) {
    if (!F.roots.length) return t3("cap arrel real", "ninguna raíz real", "no real roots");
    return F.roots.map(function (r) { return tex("x=" + (r.ap ? "" : "") + r.tex) + (r.m > 1 ? " (" + multName(r.m) + ")" : ""); }).join(", ");
  }

  var resizeT; window.addEventListener("resize", function () { clearTimeout(resizeT); resizeT = setTimeout(function () { refreshers.forEach(function (fn) { fn(); }); }, 150); });

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

  /* ---------- 4.3 segon grau (gràfica) ---------- */
  function wQuad() { quadW(byId("w-quad"), 0); }
  function quadW(w, mode) {
    if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg");
    if ($(w, "mode")) presetBtns($(w, "mode"), function () { return [tex("ax^2+bx+c=0"), tex("ax^4+bx^2+c=0")]; }, function (i) { mode = i; draw(); }, mode);
    function draw() {
      var a = +$(w, "a").value, b = +$(w, "b").value, c = +$(w, "c").value;
      ["a", "b", "c"].forEach(function (k) { $(w, k + "v").textContent = decS(+$(w, k).value, 1).replace("-", "−"); });
      var A = toFr(a), B = toFr(b), C = toFr(c), e1 = mode ? 4 : 2, e2 = mode ? 2 : 1, eq = [C], rows = [];
      for (var i = 1; i <= e1; i++) eq.push(i === e1 ? A : i === e2 ? B : F0);
      var G = gview({ x0: -6, x1: 6, y0: -8, y1: 8 }), Cl = clipSvg(svg, G), g = G.g + Cl.open + curve(G, function (x) { return a * Math.pow(x, e1) + b * Math.pow(x, e2) + c; }, COL.a);
      if (A.zero()) { info.innerHTML = t3("Amb a = 0 l'equació ja no és de segon grau (ni biquadrada).", "Con a = 0 la ecuación ya no es de segundo grado (ni bicuadrada).", "With a = 0 the equation is no longer quadratic (or biquadratic)."); svg.innerHTML = g + Cl.close; return; }
      var Q = quadRoots(A, B, C), sols = [];
      rows.push([t3("Equació", "Ecuación", "Equation"), tex(pTex(eq) + "=0")]);
      if (mode) rows.push([t3("Canvi", "Cambio", "Substitution"), tex("t=x^2:\\ " + pTex([C, B, A], "t") + "=0")]);
      var v = mode ? "t" : "x";
      rows.push(["Δ", tex("\\Delta=b^2-4ac=" + frP(B) + "^2-4\\cdot" + frP(A) + "\\cdot" + frP(C) + "=" + frT(Q.D))]);
      if (Q.kind === "none") rows.push([t3("Solucions", "Soluciones", "Solutions"), t3("Δ < 0: cap solució real", "Δ < 0: ninguna solución real", "Δ < 0: no real solution") + (mode ? t3(" en t, i per tant cap en x.", " en t, y por tanto ninguna en x.", " in t, so none in x.") : ".")]);
      else rows.push([mode ? tex("t") : t3("Solucions", "Soluciones", "Solutions"), tex(Q.roots.map(function (r) { return v + "=" + r.tex; }).join(",\\quad ")) + (Q.kind === "double" ? " (" + t3("Δ = 0: solució doble", "Δ = 0: solución doble", "Δ = 0: double root") + ")" : "")]);
      if (!mode) {
        sols = Q.roots.map(function (r) { return r.v; });
        if (Q.kind !== "none") rows.push([t3("Suma i producte", "Suma y producto", "Sum and product"), tex("x_1+x_2=-\\tfrac ba=" + frT(B.neg().div(A)) + ",\\quad x_1\\cdot x_2=\\tfrac ca=" + frT(C.div(A)))]);
      } else {
        var xs = [];
        Q.roots.forEach(function (r) {
          if (r.v < -1e-12) xs.push(tex("t=" + r.tex) + ": " + t3("negatiu, no dona solucions", "negativo, no da soluciones", "negative, no solutions"));
          else if (Math.abs(r.v) < 1e-12) { xs.push(tex("x^2=0\\Rightarrow x=0")); sols.push(0); }
          else {
            var tx = r.fr ? (sqrtFr(r.fr) ? frT(sqrtFr(r.fr)) : bsqT(new Fr(simpSqrt(r.fr.n * r.fr.d)[0], r.fr.d), simpSqrt(r.fr.n * r.fr.d)[1])) : "\\sqrt{" + r.tex + "}";
            xs.push(tex("x^2=" + r.tex + "\\Rightarrow x=\\pm" + tx)); sols.push(Math.sqrt(r.v), -Math.sqrt(r.v));
          }
        });
        if (xs.length) rows.push([tex("x"), xs.join("<br>")]);
        rows.push([t3("Total", "Total", "Total"), sols.length + " " + t3("solucions reals", "soluciones reales", "real solutions")]);
      }
      sols.forEach(function (x) { g += dot(G, x, 0, COL.r); });
      info.innerHTML = kv(rows);
      svg.setAttribute("viewBox", "0 0 " + G.W + " " + G.H); svg.innerHTML = g + Cl.close;
    }
    ["a", "b", "c"].forEach(function (k) { $(w, k).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 4.8 equacions amb radicals: solucions estranyes ---------- */
  function wRad() {
    var w = byId("w-rad"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg");
    var PRE = [[1, 1, 1, -5], [1, 4, 1, -2], [2, -3, -1, 1], [1, 7, 1, 1]];
    function setv(P) { ["p", "q", "m", "n"].forEach(function (k, i) { $(w, k).value = P[i]; }); draw(); }
    presetBtns($(w, "pre"), function () {
      return [tex("x-\\sqrt{x+1}=5"), tex("\\sqrt{x+4}=x-2"), tex("-\\sqrt{2x-3}+1=x"), tex("\\sqrt{x+7}=x+1")];
    }, function (i) { setv(PRE[i]); });
    function lin(m, n) { return pTex([n, m]); }
    function draw() {
      var p = +$(w, "p").value, q = +$(w, "q").value, m = +$(w, "m").value, n = +$(w, "n").value;
      ["p", "q", "m", "n"].forEach(function (k) { $(w, k + "v").textContent = decS(+$(w, k).value, 1).replace("-", "−"); });
      var P = toFr(p), Qq = toFr(q), M = toFr(m), N = toFr(n), rows = [];
      var inside = lin(P, Qq), right = lin(M, N);
      rows.push([t3("Equació", "Ecuación", "Equation"), tex("\\sqrt{" + inside + "}=" + right)]);
      rows.push([t3("Elevem al quadrat", "Elevamos al cuadrado", "Square both sides"), tex(inside + "=\\left(" + right + "\\right)^2")]);
      var eq = [N.mul(N).sub(Qq), M.mul(N).mul(2).sub(P), M.mul(M)], cands = [];
      if (M.zero()) {
        rows.push(["", tex(pTex([N.mul(N).sub(Qq), P.neg()]) + "=0")]);
        cands.push(rRat(N.mul(N).sub(Qq).div(P)));
      } else {
        rows.push(["", tex(pTex(eq) + "=0")]);
        var Q = quadRoots(eq[2], eq[1], eq[0]);
        if (Q.kind === "none") rows.push(["", t3("Δ < 0: l'equació elevada al quadrat no té solució, i l'original tampoc.", "Δ < 0: la ecuación elevada al cuadrado no tiene solución, y la original tampoco.", "Δ < 0: the squared equation has no solution, so neither does the original.")]);
        cands = Q.roots;
      }
      var G = gview({ x0: -8, x1: 12, y0: -6, y1: 8 }), Cl = clipSvg(svg, G), x0 = -q / p;
      var g = G.g + Cl.open + curve(G, function (x) { return Math.sqrt(p * x + q); }, COL.a, { a: x0 }) + curve(G, function (x) { return -Math.sqrt(p * x + q); }, COL.a, { a: x0, dash: "5 5", w: 2 }) + curve(G, function (x) { return m * x + n; }, COL.b);
      var chk = [];
      cands.forEach(function (r) {
        var x = r.v, lhs = Math.sqrt(Math.max(0, p * x + q)), rhs = m * x + n, good = rhs >= -1e-9 && p * x + q >= -1e-9;
        chk.push(tex("x=" + r.tex) + ": " + (r.fr ? tex("\\sqrt{" + frT(P.mul(r.fr).add(Qq)) + "}" + (good ? "=" : "\\neq ") + frT(M.mul(r.fr).add(N))) + " " : "") + ok(good) + " " + (good ? t3("és solució", "es solución", "is a solution") : t3("solució estranya", "solución extraña", "extraneous solution")));
        g += dot(G, x, rhs, good ? COL.k : COL.r);
      });
      if (chk.length) rows.push([t3("Comprovació", "Comprobación", "Check"), chk.join("<br>")]);
      rows.push(["", "<small>" + t3("Els punts verds són solucions. Els rojos són de la branca discontínua ", "Los puntos verdes son soluciones. Los rojos son de la rama discontinua ", "Green points are solutions. Red ones lie on the dashed branch ") + tex("y=-\\sqrt{" + inside + "}") + t3(": apareixen en elevar al quadrat.", ": aparecen al elevar al cuadrado.", ": they appear when we square.") + "</small>"]);
      info.innerHTML = kv(rows);
      svg.setAttribute("viewBox", "0 0 " + G.W + " " + G.H); svg.innerHTML = g + Cl.close;
    }
    ["p", "q", "m", "n"].forEach(function (k) { $(w, k).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 4.6 equacions factoritzades: (…)(…)(…) = 0 ---------- */
  function parseProd(s) {
    s = String(s).replace(/[−–]/g, "-").replace(/\s+/g, "").replace(/[·*]/g, "").replace(/=0$/, "");
    var out = [], k = F1, i = 0;
    var m0 = s.match(/^(-?\d+(?:\/\d+)?)(?=[(x])/); if (m0) { k = parseFr(m0[1]); i = m0[0].length; }
    else if (s.charAt(0) === "-" && /[(x]/.test(s.charAt(1))) { k = FM1; i = 1; }
    while (i < s.length) {
      var P, rest = s.slice(i), m;
      if (s.charAt(i) === "(") {
        var dep = 0, j = i;
        for (; j < s.length; j++) { if (s.charAt(j) === "(") dep++; else if (s.charAt(j) === ")") { dep--; if (!dep) break; } }
        if (j >= s.length) return null;
        P = parsePoly(s.slice(i + 1, j)); if (!P) return null; i = j + 1;
      } else if ((m = rest.match(/^x/))) { P = [F0, F1]; i += 1; }
      else return null;
      var e = 1, me = s.slice(i).match(/^\^(\d)/); if (me) { e = +me[1]; i += me[0].length; }
      out.push({ P: P, m: e });
    }
    return out.length ? { k: k, fs: out } : null;
  }
  function wFeq() {
    var w = byId("w-feq"); if (!w) return;
    var info = w.querySelector(".info");
    var PRE = ["(x-2)(x+3)(2x-1)", "x^2(x-4)", "(x^2-9)(x+1)", "3x(x^2+1)(x-5)", "(x^2-5x+6)(x^2-2)", "(x+1)^2(x^2-4x)"];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(p.replace(/\^(\d)/g, "^{$1}") + "=0"); }); }, function (i) { $(w, "p").value = PRE[i]; draw(); });
    function draw() {
      var R = parseProd($(w, "p").value), good = R && R.fs.every(function (f) { return pDeg(f.P) >= 0 && pDeg(f.P) <= 6; });
      $(w, "p").classList.toggle("bad", !good);
      if (!good) { info.innerHTML = t3("Escriu un producte de factors entre parèntesis, per exemple <code>(x-2)(x+3)x^2</code>.", "Escribe un producto de factores entre paréntesis, por ejemplo <code>(x-2)(x+3)x^2</code>.", "Type a product of bracketed factors, for example <code>(x-2)(x+3)x^2</code>."); return; }
      var rows = [], sols = [];
      function addSol(v, t) { if (!sols.some(function (q) { return Math.abs(q.v - v) < 1e-9; })) sols.push({ v: v, t: t }); }
      var eqT = (R.k.eq(F1) ? "" : R.k.eq(FM1) ? "-" : frT(R.k)) + R.fs.map(function (f) { var t = pTex(f.P), one = f.P.filter(function (c) { return !c.zero(); }).length === 1; return (one && pDeg(f.P) <= 1 ? t : "(" + t + ")") + (f.m > 1 ? "^{" + f.m + "}" : ""); }).join("");
      rows.push([t3("Equació", "Ecuación", "Equation"), tex(eqT + "=0")]);
      rows.push(["", "<small>" + t3("Un producte és 0 si i només si algun dels factors és 0. Igualem cada factor a 0:", "Un producto es 0 si y solo si alguno de los factores es 0. Igualamos cada factor a 0:", "A product is 0 exactly when one of its factors is 0. Set each factor equal to 0:") + "</small>"]);
      R.fs.forEach(function (f) {
        var P = f.P, d = pDeg(P), base = (f.m > 1 ? "(" + pTex(P) + ")^{" + f.m + "}=0\\Rightarrow " : "") + pTex(P) + "=0", res;
        if (d === -Infinity) res = tex("0=0") + ": " + t3("qualsevol nombre", "cualquier número", "every number");
        else if (d === 0) res = tex(pTex(P) + "\\neq0") + ": " + t3("no dona solucions", "no da soluciones", "gives no solutions");
        else if (d === 1) { var r = P[0].neg().div(P[1]); res = tex(base + "\\Rightarrow x=" + frT(r)); addSol(r.val(), frT(r)); }
        else if (d === 2) {
          var Q = quadRoots(P[2], P[1], P[0]);
          if (Q.kind === "none") res = tex(base) + ": " + t3("Δ < 0, cap solució real", "Δ < 0, ninguna solución real", "Δ < 0, no real solution");
          else { res = tex(base + "\\Rightarrow " + Q.roots.map(function (x) { return "x=" + x.tex; }).join(",\\ ")); Q.roots.forEach(function (x) { addSol(x.v, x.tex); }); }
        } else {
          var F = factorPoly(P);
          res = tex(base + "\\Rightarrow " + facTex(F) + "=0") + (F.roots.length ? "<br>" + tex(F.roots.map(function (x) { return "x=" + x.tex; }).join(",\\ ")) : " " + t3("(cap solució real)", "(ninguna solución real)", "(no real solution)"));
          F.roots.forEach(function (x) { addSol(x.v, x.tex); });
        }
        if (f.m > 1 && d >= 1) res += " (" + multName(f.m) + ")";
        rows.push(["", res]);
      });
      sols.sort(function (a, b) { return a.v - b.v; });
      rows.push([t3("Solucions", "Soluciones", "Solutions"), "<strong>" + (sols.length ? tex(sols.map(function (x) { return "x=" + x.t; }).join(",\\quad ")) : t3("no té solucions reals", "no tiene soluciones reales", "no real solutions")) + "</strong>"]);
      info.innerHTML = kv(rows);
    }
    $(w, "p").addEventListener("input", draw); onLang(draw);
  }

  /* ---------- autoavaluació ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  /*@@NOUS@@*/
  /*@@QUIZ@@*/

  /*@@GENERIC@@*/
  var TITLES = { va: "Equacions · FentMates", es: "Ecuaciones · FentMates", en: "Equations · FentMates" };
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
    var all = [wChrome, wSteps, wNav, wQuad, wFeq, wRad, wSolve, wProb, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM2 = { parsePoly: parsePoly, factorPoly: factorPoly, facTex: facTex, pTex: pTex, quadRoots: quadRoots, Fr: Fr };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
