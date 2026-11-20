(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1batx-ccss-u2-alg-done";

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

  /* ---------- 2.1 operacions amb polinomis ---------- */
  function wPop() {
    var w = byId("w-pop"); if (!w) return;
    var info = w.querySelector(".info");
    function draw() {
      var P = parsePoly($(w, "p").value), Q = parsePoly($(w, "q").value), a = parseFr($(w, "a").value);
      $(w, "p").classList.toggle("bad", !P); $(w, "q").classList.toggle("bad", !Q); $(w, "a").classList.toggle("bad", !a);
      if (!P || !Q) { info.innerHTML = u("badP"); return; }
      function dg(p) { var d = pDeg(p); return d === -Infinity ? "—" : d; }
      var rows = [
        [t3("Suma", "Suma", "Sum"), tex("P+Q=" + pTex(pAdd(P, Q)))],
        [t3("Resta", "Resta", "Difference"), tex("P-Q=" + pTex(pSub(P, Q)))],
        [t3("Producte", "Producto", "Product"), tex("P\\cdot Q=" + pTex(pMul(P, Q)))],
        [t3("Graus", "Grados", "Degrees"), tex("\\text{gr}\\,P=" + dg(P) + ",\\ \\text{gr}\\,Q=" + dg(Q) + ",\\ \\text{gr}(P\\cdot Q)=" + dg(pMul(P, Q)))]
      ];
      if (a) rows.push([t3("Valor numèric", "Valor numérico", "Value"), tex("P(" + frT(a) + ")=" + frT(pEval(P, a)) + ",\\quad Q(" + frT(a) + ")=" + frT(pEval(Q, a)))]);
      info.innerHTML = kv(rows);
    }
    ["p", "q", "a"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
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

  /* ---------- 2.1 divisió entera ---------- */
  function wDiv() {
    var w = byId("w-div"); if (!w) return;
    var box = $(w, "tbl"), info = w.querySelector(".info"), st = null, D, d, res;
    var PRE = [["2x^4-3x^3+x-5", "x^2-x+2"], ["3x^3+2x^2+x-5", "3x^2+2"], ["x^3-1", "x-1"], ["6x^4-x^2+3x", "2x^2+1"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex("(" + pTex(parsePoly(p[0])) + "):(" + pTex(parsePoly(p[1])) + ")"); }); }, function (i) { $(w, "D").value = PRE[i][0]; $(w, "d").value = PRE[i][1]; read(); });
    function rowCells(p, n) {
      var out = [], first = true;
      for (var e = n; e >= 0; e--) { var c = p[e]; if (c && !c.zero()) { out.push(tex(monT(c, e, "x", first))); first = false; } else out.push(""); }
      return out;
    }
    function read() {
      D = parsePoly($(w, "D").value); d = parsePoly($(w, "d").value);
      var okD = !!D, okd = !!d && pDeg(d) >= 1;
      $(w, "D").classList.toggle("bad", !okD); $(w, "d").classList.toggle("bad", !okd);
      res = okD && okd ? pDivide(D, d) : null;
      st.reset(res ? Math.min(1, res.steps.length) : 0);
    }
    function show(k) {
      if (!res) { box.innerHTML = ""; info.innerHTML = D && d && pDeg(d) < 1 ? t3("El divisor ha de tindre grau 1 o més.", "El divisor tiene que tener grado 1 o más.", "The divisor must have degree 1 or more.") : u("badP"); return; }
      var n = Math.max(pDeg(D), 0), h = '<table class="ldiv"><tr>' + rowCells(D, n).map(function (c) { return "<td>" + c + "</td>"; }).join("") + '<td class="dv">' + tex(pTex(d)) + "</td></tr>";
      var qT = k ? pTex(res.steps[k - 1].q) : "";
      for (var i = 0; i < k; i++) {
        var s = res.steps[i];
        h += '<tr class="sub">' + rowCells(pScale(s.prod, FM1), n).map(function (c) { return "<td>" + c + "</td>"; }).join("") + (i === 0 ? '<td class="dq">' + tex(qT) + "</td>" : "<td class=\"dl\"></td>") + "</tr>";
        h += '<tr class="rem">' + rowCells(s.r, n).map(function (c) { return "<td>" + c + "</td>"; }).join("") + "<td class=\"dl\"></td></tr>";
      }
      if (!k) h += "<tr>" + rowCells([F0], n).map(function () { return "<td></td>"; }).join("") + '<td class="dq"></td></tr>';
      box.innerHTML = h + "</table>";
      var rows = [];
      if (k) {
        var s2 = res.steps[k - 1], prev = k === 1 ? pTrim(D) : res.steps[k - 2].r, mt = monT(s2.t, s2.e, "x", true);
        rows.push([t3("Pas ", "Paso ", "Step ") + k, tex("\\dfrac{" + monT(prev[prev.length - 1], prev.length - 1, "x", true) + "}{" + monT(d[d.length - 1], pDeg(d), "x", true) + "}=" + mt) + " " + t3("i restem", "y restamos", "and subtract") + " " + tex("(" + mt + ")\\cdot(" + pTex(d) + ")")]);
      }
      if (k === res.steps.length) {
        rows.push([t3("Quocient", "Cociente", "Quotient"), tex("c(x)=" + pTex(res.q))], [t3("Residu", "Resto", "Remainder"), tex("r(x)=" + pTex(res.r)) + (pDeg(res.r) === -Infinity ? " — " + t3("divisió exacta", "división exacta", "exact division") : "")]);
        rows.push([t3("Comprovació", "Comprobación", "Check"), tex("(" + pTex(d) + ")(" + pTex(res.q) + ")" + (pDeg(res.r) === -Infinity ? "" : "+(" + pTex(res.r) + ")") + "=" + pTex(pAdd(pMul(d, res.q), res.r))) + " " + ok(true)]);
      }
      if (!res.steps.length) rows.push(["", t3("El grau del dividend és menor que el del divisor: el quocient és 0.", "El grado del dividendo es menor que el del divisor: el cociente es 0.", "The dividend has lower degree than the divisor: the quotient is 0.")]);
      info.innerHTML = kv(rows);
    }
    st = stepper(w, function () { return res ? res.steps.length : 0; }, show);
    ["D", "d"].forEach(function (r) { $(w, r).addEventListener("input", read); });
    read(); onLang(function () { st.upd(); });
  }

  /* ---------- 2.2 Ruffini ---------- */
  function wRuf() {
    var w = byId("w-ruf"); if (!w) return;
    var box = $(w, "tbl"), info = w.querySelector(".info"), st, P, dv, a, R;
    var PRE = [["2x^4-7x^2+3x-1", "x+2"], ["6x^3-x^2+4x-3", "2x-1"], ["x^5-3x^2+7", "x+1"], ["x^3-2x^2-5x+6", "x-1"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex("(" + pTex(parsePoly(p[0])) + "):(" + pTex(parsePoly(p[1])) + ")"); }); }, function (i) { $(w, "p").value = PRE[i][0]; $(w, "d").value = PRE[i][1]; read(); });
    function read() {
      P = parsePoly($(w, "p").value); dv = parsePoly($(w, "d").value);
      var okd = dv && pDeg(dv) === 1;
      $(w, "p").classList.toggle("bad", !P || pDeg(P) < 1); $(w, "d").classList.toggle("bad", !okd);
      R = null;
      if (P && pDeg(P) >= 1 && okd) { a = dv[0].neg().div(dv[1]); R = ruffini(P, a); }
      st.reset(R ? 1 : 0);
    }
    function show(k) {
      if (!R) { box.innerHTML = ""; info.innerHTML = t3("Escriu un polinomi i un divisor de grau 1, com <code>x+2</code> o <code>2x-1</code>.", "Escribe un polinomio y un divisor de grado 1, como <code>x+2</code> o <code>2x-1</code>.", "Type a polynomial and a degree-1 divisor, such as <code>x+2</code> or <code>2x-1</code>."); return; }
      box.innerHTML = rufHtml(R, a, k);
      var rows = [], b1 = dv[1];
      rows.push([t3("Coeficients", "Coeficientes", "Coefficients"), t3("ordenats, amb 0 en els termes que falten", "ordenados, con 0 en los términos que faltan", "in order, with 0 for missing terms")]);
      rows.push([t3("Nombre", "Número", "Number"), tex(pTex(dv) + (b1.eq(F1) ? "=x-" + frP(a) : "=" + frT(b1) + "\\left(x-" + frP(a) + "\\right)") + "\\ \\Rightarrow\\ a=" + frT(a))]);
      if (k > 1 && k <= R.c.length) rows.push([t3("Pas ", "Paso ", "Step ") + k, tex(frP(R.res[k - 2]) + "\\cdot" + frP(a) + "=" + frT(R.prod[k - 1]) + ",\\quad " + frT(R.c[k - 1]) + (R.prod[k - 1].sgn() < 0 ? "" : "+") + frT(R.prod[k - 1]) + "=" + frT(R.res[k - 1]))]);
      if (k === R.c.length) {
        var q = R.q, extra = "";
        if (!b1.eq(F1)) { extra = "<br><small>" + t3("Com que el divisor és ", "Como el divisor es ", "Since the divisor is ") + tex(frT(b1) + "\\left(x-" + frP(a) + "\\right)") + t3(", el quocient obtingut es divideix entre ", ", el cociente obtenido se divide entre ", ", the quotient we get is divided by ") + tex(frT(b1)) + t3("; el residu no canvia.", "; el resto no cambia.", "; the remainder stays the same.") + "</small>"; q = pScale(q, F1.div(b1)); }
        rows.push([t3("Quocient", "Cociente", "Quotient"), tex("c(x)=" + pTex(q)) + extra]);
        rows.push([t3("Residu", "Resto", "Remainder"), tex("r=" + frT(R.r))]);
        rows.push([t3("Teorema del residu", "Teorema del resto", "Remainder theorem"), tex("P(" + frT(a) + ")=" + frT(pEval(P, a))) + " " + ok(true) + (R.r.zero() ? " " + t3("És una arrel: la divisió és exacta.", "Es una raíz: la división es exacta.", "It's a root: the division is exact.") : "")]);
      }
      info.innerHTML = kv(rows);
    }
    st = stepper(w, function () { return R ? R.c.length : 0; }, show);
    ["p", "d"].forEach(function (r) { $(w, r).addEventListener("input", read); });
    read(); onLang(function () { st.upd(); });
  }

  /* ---------- 2.3 factorització pas a pas ---------- */
  function facStepsHtml(P, F) {
    var h = "";
    if (F.k) h += "<h4>" + t3("Factor comú", "Factor común", "Common factor") + "</h4>" + tex(pTex(P) + "=" + (F.k === 1 ? "x" : "x^{" + F.k + "}") + "\\left(" + pTex(F.afterK) + "\\right)");
    if (F.cands) {
      var c = F.cands.slice(0, 10).map(function (x) { return "\\pm" + x; }).join(",\\,") + (F.cands.length > 10 ? ",\\ldots" : "");
      h += "<h4>" + t3("Possibles arrels", "Posibles raíces", "Candidate roots") + "</h4>" + t3("Divisors del terme independent: ", "Divisores del término independiente: ", "Divisors of the constant term: ") + tex(c) +
        (F.candsQ && F.candsQ.length > 1 ? " " + t3("(i les fraccions ", "(y las fracciones ", "(and the fractions ") + tex("\\tfrac pq") + t3(", amb ", ", con ", ", with ") + tex("q") + t3(" divisor del coeficient principal)", " divisor del coeficiente principal)", " a divisor of the leading coefficient)") : "");
    }
    F.steps.forEach(function (s) {
      if (s.type === "ruf") h += "<h4>Ruffini " + t3("amb ", "con ", "with ") + tex("x=" + frT(s.a)) + "</h4>" + rufHtml(s.R, s.a) + t3("Residu 0: ", "Resto 0: ", "Remainder 0: ") + tex("x=" + frT(s.a)) + t3(" és arrel i queda ", " es raíz y queda ", " is a root, leaving ") + tex(pTex(s.R.q));
      if (s.type === "quad") {
        var Q = s.Q, a = s.P[2], b = s.P[1], c2 = s.P[0];
        h += "<h4>" + t3("Equació de segon grau", "Ecuación de segundo grado", "Quadratic equation") + "</h4>" + tex(pTex(s.P) + "=0:\\ \\ \\Delta=" + frT(Q.D)) + " ";
        if (Q.kind === "none") h += t3("negatiu: no té arrels reals, és irreductible.", "negativo: no tiene raíces reales, es irreducible.", "negative: no real roots, it is irreducible.");
        else h += "<br>" + tex(quadFormulaT(a, b, c2, Q) + "\\Rightarrow " + Q.roots.map(function (r) { return "x=" + r.tex; }).join(",\\ ")) + (Q.kind === "double" ? " (" + multName(2) + ")" : "");
      }
      if (s.type === "biq") h += "<h4>" + t3("Biquadrat", "Bicuadrado", "Biquadratic") + "</h4>" + tex("t=x^2:\\ " + pTex([s.P[0], s.P[2], s.P[4]], "t") + "=0\\Rightarrow " + (s.Q.roots.length ? s.Q.roots.map(function (r) { return "t=" + r.tex; }).join(",\\ ") : "\\text{" + t3("cap solució", "ninguna solución", "no solution") + "}"));
    });
    if (F.approx.length) h += "<p><small>" + t3("No té arrels racionals; les arrels reals que queden són irracionals (aproximades).", "No tiene raíces racionales; las raíces reales que quedan son irracionales (aproximadas).", "No rational roots left; the remaining real roots are irrational (approximate).") + "</small></p>";
    return h;
  }
  function wFac() {
    var w = byId("w-fac"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg");
    var PRE = ["x^4-x^3-7x^2+x+6", "2x^4+x^3-5x^2+2x", "x^3-3x^2+3x-1", "x^4-5x^2+4", "x^3-2x^2-2x", "x^4+x^2-6"];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(pTex(parsePoly(p))); }); }, function (i) { $(w, "p").value = PRE[i]; draw(); });
    function draw() {
      var P = parsePoly($(w, "p").value), good = P && pDeg(P) >= 1 && pDeg(P) <= 8;
      $(w, "p").classList.toggle("bad", !good);
      if (!good) { info.innerHTML = u("badP") + " " + t3("(grau entre 1 i 8)", "(grado entre 1 y 8)", "(degree 1 to 8)"); svg.innerHTML = ""; return; }
      var F = factorPoly(P);
      info.innerHTML = facStepsHtml(P, F) + "<h4>" + t3("Resultat", "Resultado", "Result") + "</h4>" + tex("P(x)=" + facTex(F)) + "<br>" + t3("Arrels: ", "Raíces: ", "Roots: ") + rootsList(F);
      var G = gview(polyView(P, F.roots)), C = clipSvg(svg, G), g = G.g + C.open + curve(G, function (x) { return pEvalN(P, x); }, COL.a);
      F.roots.forEach(function (r) { g += dot(G, r.v, 0, r.m > 1 ? COL.v : COL.r); });
      svg.setAttribute("viewBox", "0 0 " + G.W + " " + G.H); svg.innerHTML = g + C.close;
    }
    $(w, "p").addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 2.4 simplificació de fraccions algebraiques ---------- */
  function wFrs() {
    var w = byId("w-frs"); if (!w) return;
    var info = w.querySelector(".info");
    var PRE = [["x^3-4x", "x^3-4x^2+4x"], ["2x^2-8", "x^3+x^2-2x"], ["x^4-2x^3-3x^2", "x^4-9x^2"], ["x^3-3x^2+3x-1", "x^3-2x^2+x"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex("\\frac{" + pTex(parsePoly(p[0])) + "}{" + pTex(parsePoly(p[1])) + "}"); }); }, function (i) { $(w, "n").value = PRE[i][0]; $(w, "d").value = PRE[i][1]; draw(); });
    function clone(F) { return { c: F.c, k: F.k, lin: F.lin.map(function (x) { return { r: x.r, m: x.m }; }), irr: F.irr.map(function (Q) { return { roots: Q.roots, m: Q.m, D: Q.D }; }), rest: F.rest.map(function (R) { return { P: R.P, m: R.m, key: R.key }; }) }; }
    function draw() {
      var N = parsePoly($(w, "n").value), D = parsePoly($(w, "d").value);
      var gN = N && pDeg(N) >= 0 && pDeg(N) <= 8, gD = D && pDeg(D) >= 1 && pDeg(D) <= 8;
      $(w, "n").classList.toggle("bad", !gN); $(w, "d").classList.toggle("bad", !gD);
      if (!gN || !gD) { info.innerHTML = u("badP") + " " + t3("(el denominador ha de tindre grau 1 o més)", "(el denominador tiene que tener grado 1 o más)", "(the denominator must have degree 1 or more)"); return; }
      if (pDeg(N) === -Infinity) { info.innerHTML = tex("\\dfrac{0}{" + pTex(D) + "}=0"); return; }
      var fn = pDeg(N) >= 1 ? factorPoly(N) : { c: N[0], k: 0, lin: [], irr: [], rest: [], roots: [] }, fd = factorPoly(D), a = clone(fn), b = clone(fd), common = [];
      var mk = Math.min(a.k, b.k); if (mk) { a.k -= mk; b.k -= mk; common.push(mk === 1 ? "x" : "x^{" + mk + "}"); }
      a.lin.forEach(function (L) { b.lin.forEach(function (M) { if (L.r.eq(M.r)) { var m = Math.min(L.m, M.m); if (m) { L.m -= m; M.m -= m; common.push("(" + linT(L.r) + ")" + (m > 1 ? "^{" + m + "}" : "")); } } }); });
      a.irr.forEach(function (Q) { b.irr.forEach(function (S) { if (Q.D.eq(S.D) && Math.abs(Q.roots[0].v - S.roots[0].v) < 1e-12) { var m = Math.min(Q.m, S.m); Q.m -= m; S.m -= m; if (m) common.push("\\ldots"); } }); });
      a.rest.forEach(function (R) { b.rest.forEach(function (S) { if (R.key === S.key) { var m = Math.min(R.m, S.m); R.m -= m; S.m -= m; if (m) common.push("(" + pTex(R.P) + ")"); } }); });
      var c = fn.c.div(fd.c), na = facParts(a), nb = facParts(b);
      var top = (na.length ? (c.n === 1 ? "" : c.n === -1 ? "-" : String(c.n)) + na.join("") : String(c.n)), bot = (c.d === 1 ? "" : String(c.d)) + nb.join("");
      var resT = bot === "" ? top : "\\dfrac{" + top + "}{" + bot + "}";
      var excl = fd.roots.filter(function (r) { return !r.ap; }).map(function (r) { return r.tex; });
      info.innerHTML = kv([
        [t3("Factoritzem", "Factorizamos", "Factorise"), tex("\\dfrac{" + facTex(fn) + "}{" + facTex(fd) + "}")],
        [t3("Factors comuns", "Factores comunes", "Common factors"), common.length ? tex(common.join(",\\ ")) : t3("cap: la fracció ja és irreductible", "ninguno: la fracción ya es irreducible", "none: the fraction is already in lowest terms")],
        [t3("Simplificada", "Simplificada", "Simplified"), tex(resT)],
        [t3("Té sentit si", "Tiene sentido si", "Defined for"), excl.length ? tex("x\\neq " + excl.join(",\\ x\\neq ")) + "<br><small>" + t3("Compte: els valors que anul·len el denominador original continuen exclosos encara que el factor s'haja simplificat.", "Cuidado: los valores que anulan el denominador original siguen excluidos aunque el factor se haya simplificado.", "Careful: values that make the original denominator zero stay excluded even after cancelling.") + "</small>" : tex("x\\in\\mathbb R")]
      ]);
    }
    ["n", "d"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 2.5 equacions de primer grau amb parèntesis i denominadors ---------- */
  // cada terme és k·(p·x+q)/d, amb k fraccionari (amb signe), p i q enters i d natural
  function wLin() {
    var w = byId("w-lin"); if (!w) return;
    var info = w.querySelector(".info"), eqBox = $(w, "eq"), st = null, E = null, R = null;
    function T(k, p, q, d) { return { k: new Fr(k), p: p, q: q, d: d }; }
    var PRE = [
      [[T(1, 1, -1, 2), T(-1, 1, 2, 3)], [T(1, 0, 1, 1)]],
      [[T(3, 1, -2, 1), T(-2, 1, 1, 1)], [T(1, 0, 4, 1)]],
      [[T(1, 2, -3, 4), T(1, 1, 0, 2), T(-1, 3, -1, 5)], [T(1, 2, -1, 1)]],
      [[T(2, 1, 1, 3), T(-1, 1, -2, 2)], [T(1, 1, 0, 6), T(1, 0, 1, 1)]],
      [[T(3, 1, -2, 1), T(-2, 1, 1, 1)], [T(1, 1, -8, 1)]]
    ];
    function lcm(a, b) { return a / gcd(a, b) * b; }
    function tt(t, K, dd) { // {neg, tex} del terme amb coeficient K i denominador dd
      var neg = K.sgn() < 0, a = K.abs(), num;
      if (t.p === 0) { var v = a.mul(Math.abs(t.q)); neg = neg !== (t.q < 0); num = frT(v); return { neg: neg, tex: dd > 1 ? "\\dfrac{" + num + "}{" + dd + "}" : num, zero: t.q === 0 }; }
      if (t.q === 0) { var c = a.mul(Math.abs(t.p)); neg = neg !== (t.p < 0); num = (c.eq(F1) ? "" : frT(c)) + "x"; return { neg: neg, tex: dd > 1 ? "\\dfrac{" + num + "}{" + dd + "}" : num }; }
      var inn = pTex([new Fr(t.q), new Fr(t.p)]);
      if (dd > 1) return { neg: neg, tex: "\\dfrac{" + (a.eq(F1) ? inn : frT(a) + "(" + inn + ")") + "}{" + dd + "}" };
      return { neg: neg, tex: a.eq(F1) ? (neg ? "(" + inn + ")" : inn) : frT(a) + "(" + inn + ")" };
    }
    function join(list) {
      var s = "";
      list.forEach(function (r, i) { s += (r.neg ? "-" : i ? "+" : "") + r.tex; });
      return s || "0";
    }
    function side(terms, mult) { return join(terms.map(function (t) { return mult ? tt(t, t.k.mul(new Fr(mult / t.d)), 1) : tt(t, t.k, t.d); })); }
    function lin(t, mult) { var K = t.k.mul(new Fr(mult / t.d)); return [K.mul(t.q), K.mul(t.p)]; }
    function expSide(terms, mult) {
      var s = "";
      terms.forEach(function (t, i) { var e = pTex(lin(t, mult)); if (e === "0") return; s += (s && e.charAt(0) !== "-" ? "+" : "") + e; });
      return s || "0";
    }
    function sum(terms, mult) { return terms.reduce(function (acc, t) { return pAdd(acc, lin(t, mult)); }, [F0]); }
    function solve(e) {
      var M = e[0].concat(e[1]).reduce(function (m, t) { return lcm(m, t.d); }, 1);
      var L = sum(e[0], M), Rr = sum(e[1], M), A = L[1] || F0, B = L[0] || F0, C = Rr[1] || F0, D = Rr[0] || F0;
      var a = A.sub(C), b = D.sub(B);
      return { M: M, L: L, R: Rr, a: a, b: b, kind: !a.zero() ? "one" : b.zero() ? "all" : "none", x: a.zero() ? null : b.div(a) };
    }
    function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
    function nz(a, b) { var v = 0; while (!v) v = rnd(a, b); return v; }
    function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
    function random() {
      for (var tries = 0; tries < 300; tries++) {
        var Ds = [1, 2, 3, 4, 5, 6], terms = [[], []];
        terms[0].push(T(pick([1, 1, 2, 3]), nz(1, 3), nz(-6, 6), pick(Ds)));
        terms[0].push(T(pick([1, -1, 2, -2, -3]), nz(1, 3), nz(-6, 6), pick(Ds)));
        terms[1].push(Math.random() < 0.5 ? T(1, nz(1, 2), rnd(-6, 6), pick([1, 1, 2, 3, 6])) : T(pick([1, 2, -1]), 1, nz(-5, 5), pick(Ds)));
        if (Math.random() < 0.5) terms[1].push(T(1, 0, nz(-6, 6), pick([1, 1, 2, 3])));
        var all = terms[0].concat(terms[1]);
        if (!all.some(function (t) { return t.d > 1; })) continue;
        if (all.some(function (t) { return t.p === 0 && t.q === 0; })) continue;
        if (all.some(function (t) { return t.d > 1 && gcd(t.k.n * (t.p ? 1 : t.q), t.d) > 1; })) continue;
        if (all.some(function (t) { return t.p && t.q && gcd(t.p, t.q) > 1; })) continue;
        var s = solve(terms);
        if (s.kind !== "one" || s.x.d > 12 || Math.abs(s.x.n) > 60 || s.M > 30) continue;
        return terms;
      }
      return PRE[0];
    }
    function eqT(e) { return side(e[0]) + "=" + side(e[1]); }
    function nSteps() { return R ? (R.M > 1 ? 4 : 3) : 0; }
    function set(e) { E = e; R = solve(E); st.reset(1); }
    var bs = presetBtns($(w, "pre"), function () { return PRE.map(function (e) { return tex(eqT(e)); }); }, function (i) { set(PRE[i]); }, 0);
    $(w, "rnd").addEventListener("click", function () { bs.forEach(function (b) { b.classList.remove("on"); }); set(random()); });
    function show(k) {
      eqBox.innerHTML = tex(eqT(E), true);
      var rows = [], i = 1, M = R.M;
      if (M > 1) {
        rows.push([t3("Pas ", "Paso ", "Step ") + i++ + ": " + t3("m.c.m. dels denominadors", "m.c.m. de los denominadores", "LCM of the denominators"),
          tex("\\text{m.c.m.}=" + M) + ". " + t3("Multipliquem cada terme per " + M + " i simplifiquem:", "Multiplicamos cada término por " + M + " y simplificamos:", "Multiply every term by " + M + " and simplify:") + "<br>" + tex(side(E[0], M) + "=" + side(E[1], M))]);
      }
      if (k >= i) rows.push([t3("Pas ", "Paso ", "Step ") + i + ": " + t3("traiem els parèntesis i reduïm", "quitamos los paréntesis y reducimos", "remove brackets and simplify"),
        tex(expSide(E[0], M) + "=" + expSide(E[1], M)) + "<br>" + tex(pTex(R.L) + "=" + pTex(R.R))]);
      i++;
      if (k >= i) rows.push([t3("Pas ", "Paso ", "Step ") + i + ": " + t3("termes amb x a un membre i nombres a l'altre", "términos con x a un miembro y números al otro", "x terms on one side, numbers on the other"),
        tex((R.a.zero() ? "0\\cdot x" : pTex([F0, R.a])) + "=" + frT(R.b))]);
      i++;
      if (k >= i) {
        var sol;
        if (R.kind === "one") {
          var chk = function (s) { return s.reduce(function (acc, t) { return acc.add(t.k.mul(new Fr(t.p).mul(R.x).add(t.q)).div(t.d)); }, F0); };
          var nu = R.a.sgn() < 0 ? R.b.neg() : R.b, de = R.a.abs(), fT = nu.d === 1 && de.d === 1 && !de.eq(F1) && de.n !== R.x.d ? "x=\\dfrac{" + frT(nu) + "}{" + frT(de) + "}\\Rightarrow " : "";
          sol = tex(fT + "x=" + frT(R.x), true) +
            "<small>" + t3("Comprovació: els dos membres valen ", "Comprobación: los dos miembros valen ", "Check: both sides equal ") + tex(frT(chk(E[0]))) + " " + ok(chk(E[0]).eq(chk(E[1]))) + "</small>";
        } else if (R.kind === "none") sol = tex("0\\cdot x=" + frT(R.b)) + ": " + t3("cap nombre ho compleix, l'equació <strong>no té solució</strong> (és incompatible).", "ningún número lo cumple, la ecuación <strong>no tiene solución</strong> (es incompatible).", "no number satisfies it: the equation <strong>has no solution</strong>.");
        else sol = tex("0\\cdot x=0") + ": " + t3("es compleix per a tot nombre real, és una <strong>identitat</strong> (infinites solucions).", "se cumple para todo número real, es una <strong>identidad</strong> (infinitas soluciones).", "true for every real number: it is an <strong>identity</strong> (infinitely many solutions).");
        rows.push([t3("Solució", "Solución", "Solution"), sol]);
      }
      info.innerHTML = kv(rows.slice(0, k));
    }
    E = PRE[0]; R = solve(E);
    st = stepper(w, nSteps, show);
    onLang(function () { $(w, "rnd").textContent = "🎲 " + t3("Nova equació", "Nueva ecuación", "New equation"); st.upd(); });
  }

  /* ---------- 2.5 segon grau i biquadrades ---------- */
  function wQuad() {
    var w = byId("w-quad"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg"), mode = 0;
    presetBtns($(w, "mode"), function () { return [tex("ax^2+bx+c=0"), tex("ax^4+bx^2+c=0")]; }, function (i) { mode = i; draw(); }, 0);
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

  /* ---------- 2.6 equacions amb radicals: solucions estranyes ---------- */
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

  /* ---------- 2.8 exponencials amb canvi de variable ---------- */
  function wExp() {
    var w = byId("w-exp"); if (!w) return;
    var info = w.querySelector(".info"), bi = 0, BASES = [2, 3, 5, 10];
    var bb = presetBtns($(w, "base"), function () { return BASES.map(function (b) { return tex("a=" + b); }); }, function (i) { bi = i; draw(); }, 0);
    var PRE = [[0, 1, -6, 8], [1, 1, 5, -24], [0, 1, -3, -4], [2, 1, -6, 5]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (P) { return tex(eqT(BASES[P[0]], P[1], P[2], P[3])); }); }, function (i) {
      var P = PRE[i]; bi = P[0]; bb.forEach(function (b, j) { b.classList.toggle("on", j === bi); }); $(w, "k").value = P[1]; $(w, "m").value = P[2]; $(w, "n").value = P[3]; draw();
    });
    function eqT(a, k, m, n) { return (k === 1 ? "" : k === -1 ? "-" : k) + (a * a) + "^{x}" + (m ? (m > 0 ? "+" : "-") + (Math.abs(m) === 1 ? "" : Math.abs(m) + "\\cdot ") + a + "^{x}" : "") + (n ? (n > 0 ? "+" : "") + n : "") + "=0"; }
    function logExact(a, t) { // t = a^j amb j enter?
      for (var j = -6; j <= 12; j++) { var v = j >= 0 ? new Fr(Math.pow(a, j)) : new Fr(1, Math.pow(a, -j)); if (v.eq(t)) return j; }
      return null;
    }
    function draw() {
      var a = BASES[bi], k = Math.round(+$(w, "k").value), m = Math.round(+$(w, "m").value), n = Math.round(+$(w, "n").value);
      var bad = !isFinite(k) || !isFinite(m) || !isFinite(n) || k === 0;
      ["k", "m", "n"].forEach(function (r) { $(w, r).classList.toggle("bad", bad); });
      if (bad) { info.innerHTML = t3("Escriu tres nombres enters (el primer, diferent de 0).", "Escribe tres números enteros (el primero, distinto de 0).", "Type three whole numbers (the first one non-zero)."); return; }
      var rows = [[t3("Equació", "Ecuación", "Equation"), tex(eqT(a, k, m, n))],
        [t3("Observa", "Observa", "Notice"), tex((a * a) + "^{x}=(" + a + "^2)^{x}=(" + a + "^{x})^2")],
        [t3("Canvi", "Cambio", "Substitution"), tex("t=" + a + "^{x}:\\ " + pTex([new Fr(n), new Fr(m), new Fr(k)], "t") + "=0")]];
      var Q = quadRoots(new Fr(k), new Fr(m), new Fr(n)), out = [];
      if (Q.kind === "none") rows.push([tex("t"), t3("Δ < 0: cap solució.", "Δ < 0: ninguna solución.", "Δ < 0: no solution.")]);
      else {
        rows.push([tex("t"), tex(Q.roots.map(function (r) { return "t=" + r.tex; }).join(",\\quad "))]);
        Q.roots.forEach(function (r) {
          if (r.v <= 1e-12) { out.push(tex(a + "^{x}=" + r.tex) + ": " + t3("impossible, una potència de base positiva sempre és positiva", "imposible, una potencia de base positiva siempre es positiva", "impossible, a power of a positive base is always positive") + " " + ok(false)); return; }
          var j = r.fr ? logExact(a, r.fr) : null;
          if (j != null) out.push(tex(a + "^{x}=" + r.tex + "=" + a + "^{" + j + "}\\Rightarrow x=" + j) + " " + ok(true));
          else out.push(tex(a + "^{x}=" + r.tex + "\\Rightarrow x=" + (a === 10 ? "\\log\\left(" + r.tex + "\\right)" : "\\dfrac{\\log\\left(" + r.tex + "\\right)}{\\log " + a + "}") + "\\approx " + dT(Math.log(r.v) / Math.log(a), 4)) + " " + ok(true));
        });
        rows.push([t3("Desfem el canvi", "Deshacemos el cambio", "Undo the substitution"), out.join("<br>")]);
      }
      info.innerHTML = kv(rows);
    }
    ["k", "m", "n"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- autoavaluació ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("Quin és el grau de $P(x)\\cdot Q(x)$ si $P$ té grau 3 i $Q$ té grau 2?", "¿Cuál es el grado de $P(x)\\cdot Q(x)$ si $P$ tiene grado 3 y $Q$ tiene grado 2?", "What is the degree of $P(x)\\cdot Q(x)$ if $P$ has degree 3 and $Q$ has degree 2?"),
      o: [q3("$6$"), q3("$5$"), q3("$3$")], a: 1, e: q3("Els graus se sumen: $3+2=5$.", "Los grados se suman: $3+2=5$.", "Degrees add up: $3+2=5$.") },
    { q: q3("$(2x-3)^2=$"), o: [q3("$4x^2-9$"), q3("$4x^2-12x+9$"), q3("$4x^2-6x+9$")], a: 1, e: q3("$(a-b)^2=a^2-2ab+b^2$: $4x^2-2\\cdot2x\\cdot3+9$.") },
    { q: q3("El residu de $(x^3-2x+5):(x+2)$ és…", "El resto de $(x^3-2x+5):(x+2)$ es…", "The remainder of $(x^3-2x+5):(x+2)$ is…"),
      o: [q3("$1$"), q3("$9$"), q3("$-1$")], a: 0, e: q3("Pel teorema del residu: $P(-2)=-8+4+5=1$.", "Por el teorema del resto: $P(-2)=-8+4+5=1$.", "By the remainder theorem: $P(-2)=-8+4+5=1$.") },
    { q: q3("Quin d'aquests nombres <strong>no</strong> pot ser una arrel entera de $x^3+2x^2-5x-6$?", "¿Cuál de estos números <strong>no</strong> puede ser una raíz entera de $x^3+2x^2-5x-6$?", "Which of these numbers <strong>cannot</strong> be an integer root of $x^3+2x^2-5x-6$?"),
      o: [q3("$-3$"), q3("$4$"), q3("$2$")], a: 1, e: q3("Les arrels enteres són divisors de $-6$, i 4 no ho és.", "Las raíces enteras son divisores de $-6$, y 4 no lo es.", "Integer roots divide $-6$, and 4 doesn't.") },
    { q: q3("$\\dfrac{x^2-9}{x^2+3x}=$"), o: [q3("$\\dfrac{x-3}{x}$"), q3("$\\dfrac{-9}{3x}$"), q3("$x-3$")], a: 0, e: q3("$\\dfrac{(x+3)(x-3)}{x(x+3)}$: només se simplifiquen factors.", "$\\dfrac{(x+3)(x-3)}{x(x+3)}$: solo se simplifican factores.", "$\\dfrac{(x+3)(x-3)}{x(x+3)}$: only factors cancel.") },
    { q: q3("$\\dfrac{x-1}{2}-\\dfrac{x+2}{3}=1\\Rightarrow x=$"), o: [q3("$13$"), q3("$5$"), q3("$11$")], a: 0,
      e: q3("Per 6: $3(x-1)-2(x+2)=6\\Rightarrow3x-3-2x-4=6\\Rightarrow x=13$. Compte: el signe $-$ afecta tot el numerador.", "Por 6: $3(x-1)-2(x+2)=6\\Rightarrow3x-3-2x-4=6\\Rightarrow x=13$. Cuidado: el signo $-$ afecta a todo el numerador.", "Times 6: $3(x-1)-2(x+2)=6\\Rightarrow3x-3-2x-4=6\\Rightarrow x=13$. Careful: the $-$ sign applies to the whole numerator.") },
    { q: q3("Quantes solucions té $3(x-2)-2(x+1)=x-8$?", "¿Cuántas soluciones tiene $3(x-2)-2(x+1)=x-8$?", "How many solutions does $3(x-2)-2(x+1)=x-8$ have?"),
      o: [q3("Cap", "Ninguna", "None"), q3("Una", "Una", "One"), q3("Infinites", "Infinitas", "Infinitely many")], a: 2,
      e: q3("$x-8=x-8\\Rightarrow0\\cdot x=0$: és una identitat.", "$x-8=x-8\\Rightarrow0\\cdot x=0$: es una identidad.", "$x-8=x-8\\Rightarrow0\\cdot x=0$: it is an identity.") },
    { q: q3("Quantes solucions reals té $x^4-5x^2-36=0$?", "¿Cuántas soluciones reales tiene $x^4-5x^2-36=0$?", "How many real solutions does $x^4-5x^2-36=0$ have?"),
      o: [q3("$4$"), q3("$2$"), q3("$0$")], a: 1, e: q3("$t=9$ o $t=-4$: només $x^2=9$ dona solucions, $x=\\pm3$.", "$t=9$ o $t=-4$: solo $x^2=9$ da soluciones, $x=\\pm3$.", "$t=9$ or $t=-4$: only $x^2=9$ gives solutions, $x=\\pm3$.") },
    { q: q3("En resoldre $\\dfrac{x}{x-2}=\\dfrac{2}{x-2}$ obtenim $x=2$. Per tant…", "Al resolver $\\dfrac{x}{x-2}=\\dfrac{2}{x-2}$ obtenemos $x=2$. Por tanto…", "Solving $\\dfrac{x}{x-2}=\\dfrac{2}{x-2}$ gives $x=2$. So…"),
      o: [q3("la solució és $x=2$", "la solución es $x=2$", "the solution is $x=2$"), q3("no té solució", "no tiene solución", "it has no solution"), q3("té infinites solucions", "tiene infinitas soluciones", "it has infinitely many")], a: 1, e: q3("$x=2$ anul·la el denominador: es descarta.", "$x=2$ anula el denominador: se descarta.", "$x=2$ makes the denominator zero, so it is rejected.") },
    { q: q3("En elevar al quadrat $\\sqrt{x+4}=x-2$ obtenim $x=0$ i $x=5$. Quines són solucions?", "Al elevar al cuadrado $\\sqrt{x+4}=x-2$ obtenemos $x=0$ y $x=5$. ¿Cuáles son soluciones?", "Squaring $\\sqrt{x+4}=x-2$ gives $x=0$ and $x=5$. Which are solutions?"),
      o: [q3("Totes dues", "Las dos", "Both"), q3("Només $x=5$", "Solo $x=5$", "Only $x=5$"), q3("Només $x=0$", "Solo $x=0$", "Only $x=0$")], a: 1, e: q3("$x=0$: $\\sqrt4=2\\neq-2$, és una solució estranya.", "$x=0$: $\\sqrt4=2\\neq-2$, es una solución extraña.", "$x=0$: $\\sqrt4=2\\neq-2$, an extraneous solution.") },
    { q: q3("$3^{x+1}+3^{x}=36\\Rightarrow x=$"), o: [q3("$2$"), q3("$3$"), q3("$\\tfrac32$")], a: 0, e: q3("$3^x(3+1)=36\\Rightarrow3^x=9\\Rightarrow x=2$.") },
    { q: q3("$\\log x+\\log(x-3)=1$ té com a solució…", "$\\log x+\\log(x-3)=1$ tiene como solución…", "The solution of $\\log x+\\log(x-3)=1$ is…"),
      o: [q3("$x=5$ i $x=-2$", "$x=5$ y $x=-2$", "$x=5$ and $x=-2$"), q3("$x=5$"), q3("$x=-2$")], a: 1, e: q3("$x(x-3)=10$; $x=-2$ no val perquè $\\log(-2)$ no existeix.", "$x(x-3)=10$; $x=-2$ no vale porque $\\log(-2)$ no existe.", "$x(x-3)=10$; $x=-2$ fails because $\\log(-2)$ doesn't exist.") }
  ];

  /*@@GENERIC@@*/
  var TITLES = { va: "Àlgebra · FentMates", es: "Álgebra · FentMates", en: "Algebra · FentMates" };
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
    var all = [wChrome, wSteps, wNav, wPop, wDiv, wRuf, wFac, wFrs, wLin, wQuad, wRad, wExp, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM2 = { parsePoly: parsePoly, factorPoly: factorPoly, facTex: facTex, pTex: pTex, quadRoots: quadRoots, Fr: Fr };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
