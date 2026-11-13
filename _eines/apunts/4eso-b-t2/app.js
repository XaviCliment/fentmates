(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-4eso-b-u2-done";

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

  /* ---------- intervals (com a la unitat 1) ---------- */
  function isEmpty(I) { return I.a > I.b || (I.a === I.b && !(I.ac && I.bc)); }
  function norm(list) {
    var L = list.filter(function (I) { return !isEmpty(I); }).map(function (I) { return { a: I.a, ac: isFinite(I.a) && I.ac, b: I.b, bc: isFinite(I.b) && I.bc }; })
      .sort(function (p, q) { return p.a - q.a || (q.ac - p.ac); });
    var out = [];
    L.forEach(function (I) {
      var c = out[out.length - 1];
      if (c && (I.a < c.b || (I.a === c.b && (c.bc || I.ac)))) {
        if (I.b > c.b) { c.b = I.b; c.bc = I.bc; } else if (I.b === c.b) c.bc = c.bc || I.bc;
      } else out.push(I);
    });
    return out;
  }
  function setTL(S, lab) {
    S = norm(S); lab = lab || nT;
    function L(v) { return v === Infinity ? "+\\infty" : v === -Infinity ? "-\\infty" : lab(v); }
    if (!S.length) return "\\varnothing";
    if (S.length === 1 && S[0].a === -Infinity && S[0].b === Infinity) return "\\mathbb R";
    return S.map(function (I) { return I.a === I.b ? "\\{" + L(I.a) + "\\}" : (I.ac ? "[" : "(") + L(I.a) + ",\\," + L(I.b) + (I.bc ? "]" : ")"); }).join("\\cup ");
  }
  function range(sets) {
    var p = [];
    sets.forEach(function (S) { S.forEach(function (I) { if (isFinite(I.a)) p.push(I.a); if (isFinite(I.b)) p.push(I.b); }); });
    if (!p.length) p = [0];
    var lo = Math.floor(Math.min.apply(null, p)) - 1, hi = Math.ceil(Math.max.apply(null, p)) + 1;
    if (hi - lo < 8) { var c = (hi + lo) / 2; lo = Math.floor(c - 4); hi = Math.ceil(c + 4); }
    return [lo, hi];
  }
  function nline(rows, o) {
    o = o || {};
    var W = o.W || 600, lab = rows.some(function (r) { return r.l; }), L = lab ? 58 : 20, R = W - 22, rowH = o.rowH || 34, top = 14;
    var rg = o.range || range(rows.map(function (r) { return r.S; })), lo = rg[0], hi = rg[1];
    function X(v) { return L + (Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo) * (R - L); }
    var H = top + rows.length * rowH + 30, g = "";
    rows.forEach(function (r, i) {
      var y = top + i * rowH + 14;
      if (r.l) g += '<text class="lb" x="6" y="' + (y + 4) + '">' + r.l + "</text>";
      g += '<line class="gl" x1="' + L + '" x2="' + R + '" y1="' + y + '" y2="' + y + '"/>';
      norm(r.S).forEach(function (I) {
        var x1 = X(I.a), x2 = X(I.b);
        if (I.a !== I.b) g += '<line x1="' + x1 + '" x2="' + x2 + '" y1="' + y + '" y2="' + y + '" stroke="' + r.c + '" stroke-width="5"/>';
        if (I.a === -Infinity) g += '<path d="M' + (L - 9) + " " + y + ' l11 -7 v14 z" fill="' + r.c + '"/>';
        if (I.b === Infinity) g += '<path d="M' + (R + 9) + " " + y + ' l-11 -7 v14 z" fill="' + r.c + '"/>';
        [[I.a, I.ac, x1], [I.b, I.bc, x2]].forEach(function (e, k) {
          if (!isFinite(e[0]) || (k === 1 && I.a === I.b)) return;
          g += '<circle cx="' + e[2] + '" cy="' + y + '" r="5.5" stroke="' + r.c + '" stroke-width="2.2"' + (e[1] ? ' fill="' + r.c + '"' : ' class="op"') + "/>";
          if (!Number.isInteger(e[0])) g += '<text x="' + e[2] + '" y="' + (y - 10) + '" text-anchor="middle">' + nS(e[0]) + "</text>";
        });
      });
    });
    var ay = H - 22, px = (R - L) / (hi - lo), step = [1, 2, 5, 10].filter(function (s) { return s * px >= 24; })[0] || 10;
    g += '<line class="ax" x1="' + (L - 6) + '" x2="' + (R + 12) + '" y1="' + ay + '" y2="' + ay + '"/><path d="M' + (R + 16) + " " + ay + ' l-8 -4 v8 z" fill="var(--muted)"/>';
    for (var v = Math.ceil(lo / step) * step; v <= hi; v += step)
      g += '<line class="tk" x1="' + X(v) + '" x2="' + X(v) + '" y1="' + (ay - 5) + '" y2="' + (ay + 5) + '"/><text x="' + X(v) + '" y="' + (ay + 18) + '" text-anchor="middle">' + String(v).replace("-", "−") + "</text>";
    return { svg: g, H: H, X: X };
  }
  function paint(svg, res, W) { svg.setAttribute("viewBox", "0 0 " + (W || 600) + " " + res.H); svg.innerHTML = res.svg; }
  function svgW(svg) { var w = svg.getBoundingClientRect().width; return w ? Math.max(300, Math.min(600, Math.round(w))) : 600; }
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

  /* ---------- 2.2 operacions amb polinomis ---------- */
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

  /* ---------- 2.2 divisió entera ---------- */
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

  /* ---------- 2.5 factorització pas a pas ---------- */
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

  /* ---------- 2.7 simplificació de fraccions algebraiques ---------- */
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
      function strip(t) { var m = t.match(/^\(([^()]*)\)$/); return m ? m[1] : t; }
      top = strip(top); bot = strip(bot);
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

  /* ---------- factorització com a llista de factors amb coeficients enters: P = c · Π f.P^f.m ---------- */
  function facList(P) {
    P = pTrim(P);
    if (pDeg(P) < 1) return { c: P[0], fs: [] };
    var F = factorPoly(P), c = F.c, fs = [];
    function add(poly, m) { var key = pTex(poly), f = fs.filter(function (x) { return x.key === key; })[0]; if (f) f.m += m; else fs.push({ P: poly, m: m, key: key }); }
    if (F.k) add([F0, F1], F.k);
    F.lin.forEach(function (L) { if (L.m) add([new Fr(-L.r.n), new Fr(L.r.d)], L.m); });
    F.irr.forEach(function (Q) {
      if (!Q.m) return;
      var r = Q.roots[0], I = intForm([r.A.mul(r.A).sub(r.B.mul(r.B).mul(new Fr(r.m))), r.A.mul(new Fr(-2)), F1]);
      for (var i = 0; i < Q.m; i++) c = c.mul(I.k);
      add(I.P, Q.m);
    });
    F.rest.forEach(function (R) { if (R.m) add(R.P, R.m); });
    return { c: c, fs: fs };
  }
  function facT(poly) { return pDeg(poly) === 1 && poly[0].zero() && poly[1].eq(F1) ? "x" : "(" + pTex(poly) + ")"; }
  function listT(L, wrap) {
    var act = L.fs.filter(function (f) { return f.m > 0; }).sort(function (a, b) { return (b.key === "x") - (a.key === "x"); });
    if (act.length === 1 && act[0].m === 1 && (L.c.eq(F1) || L.c.eq(FM1))) return (L.c.eq(FM1) ? "-(" + pTex(act[0].P) + ")" : wrap ? facT(act[0].P) : pTex(act[0].P));
    var parts = act.map(function (f) { return facT(f.P) + (f.m > 1 ? "^{" + f.m + "}" : ""); });
    if (!parts.length) return frT(L.c);
    return (L.c.eq(F1) ? "" : L.c.eq(FM1) ? "-" : frT(L.c)) + parts.join("");
  }
  // (a)(b) sense parèntesis sobrers ni factors 1
  function parT(p) { var t = pTex(p), n = p.filter(function (c) { return !c.zero(); }).length; return n > 1 ? "(" + t + ")" : t; }
  function mulT(a, b) {
    if (pDeg(b) === 0 && b[0].eq(F1)) return parT(a);
    if (pDeg(a) === 0 && a[0].eq(F1)) return parT(b);
    if (pDeg(a) === 0) return pTex(a) + (pDeg(b) === 0 ? "\cdot " + pTex(b) : parT(b));
    return parT(a) + (pDeg(b) === 0 ? "\cdot " + pTex(b) : parT(b));
  }
  function listPoly(L) { var p = [L.c]; L.fs.forEach(function (f) { for (var i = 0; i < f.m; i++) p = pMul(p, f.P); }); return pTrim(p); }
  function findF(L, key) { return L.fs.filter(function (f) { return f.key === key && f.m > 0; })[0]; }
  function mcdMcm(A, B) {
    var seen = {}, all = [], mcd = [], mcm = [];
    A.fs.concat(B.fs).forEach(function (f) { if (f.m > 0 && !seen[f.key]) { seen[f.key] = 1; all.push(f); } });
    all.forEach(function (f) {
      var a = findF(A, f.key), b = findF(B, f.key), ma = a ? a.m : 0, mb = b ? b.m : 0;
      if (Math.min(ma, mb) > 0) mcd.push({ P: f.P, m: Math.min(ma, mb), key: f.key });
      mcm.push({ P: f.P, m: Math.max(ma, mb), key: f.key });
    });
    var ints = A.c.d === 1 && B.c.d === 1, g = ints ? gcd(A.c.n, B.c.n) || 1 : 1, l = ints ? Math.abs(A.c.n * B.c.n) / g : 1;
    return { mcd: { c: new Fr(g), fs: mcd }, mcm: { c: new Fr(l), fs: mcm }, ints: ints };
  }
  // simplifica N/D: cancel·la els factors comuns
  function simpFrac(N, D) {
    if (pDeg(N) === -Infinity) return { tex: "0", N: [F0], D: [F1] };
    var A = facList(N), B = facList(D), a = { c: F1, fs: [] }, b = { c: F1, fs: [] };
    A.fs.forEach(function (f) { var g = findF(B, f.key), m = f.m - (g ? Math.min(f.m, g.m) : 0); if (m > 0) a.fs.push({ P: f.P, m: m, key: f.key }); });
    B.fs.forEach(function (f) { var g = findF(A, f.key), m = f.m - (g ? Math.min(f.m, g.m) : 0); if (m > 0) b.fs.push({ P: f.P, m: m, key: f.key }); });
    var c = A.c.div(B.c), neg = c.sgn() < 0, cn = new Fr(Math.abs(c.n)), cd = new Fr(c.d);
    a.c = cn; b.c = cd;
    var top = listT(a), bot = b.fs.length || !cd.eq(F1) ? listT(b) : "";
    var tx = (neg ? "-" : "") + (bot ? "\\dfrac{" + top + "}{" + bot + "}" : top);
    var Np = listPoly(a), Dp = listPoly(b), ex = (neg ? "-" : "") + (bot ? "\\dfrac{" + pTex(Np) + "}{" + pTex(Dp) + "}" : pTex(Np));
    return { tex: tx, ex: ex, N: neg ? pScale(Np, FM1) : Np, D: Dp };
  }
  function exclT(polys) {
    var r = [];
    polys.forEach(function (p) { if (pDeg(p) >= 1) factorPoly(p).roots.forEach(function (x) { if (!x.ap && r.indexOf(x.tex) < 0) r.push(x.tex); }); });
    return r.length ? tex("x\\neq " + r.join(",\\ x\\neq ")) : tex("x\\in\\mathbb R");
  }
  function frPar(a) { return a.sgn() < 0 || a.d !== 1 ? "\\left(" + frT(a) + "\\right)" : frT(a); }
  function subT(P, a) {
    var A = frPar(a), out = "";
    for (var i = P.length - 1; i >= 0; i--) {
      var c = P[i]; if (c.zero()) continue;
      var s = c.sgn() < 0 ? "-" : (out ? "+" : ""), ac = c.abs(), pw = i === 0 ? "" : i === 1 ? A : A + "^{" + i + "}";
      out += s + (i === 0 ? frT(ac) : ac.eq(F1) ? "" : frT(ac) + "\\cdot ") + pw;
    }
    return out || "0";
  }

  /* ---------- 2.3 valor numèric i teorema del residu ---------- */
  function wRes() {
    var w = byId("w-res"); if (!w) return;
    var info = w.querySelector(".info");
    var PRE = [["x^3-2x+5", "-2"], ["x^4-3x^2+2x-1", "1"], ["2x^3-5x^2+x+2", "2"], ["x^5-1", "-1"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex("P(x)=" + pTex(parsePoly(p[0])) + ",\\ a=" + p[1]); }); }, function (i) { $(w, "p").value = PRE[i][0]; $(w, "a").value = PRE[i][1]; draw(); });
    function draw() {
      var P = parsePoly($(w, "p").value), a = parseFr($(w, "a").value), good = P && pDeg(P) >= 1;
      $(w, "p").classList.toggle("bad", !good); $(w, "a").classList.toggle("bad", !a);
      if (!good || !a) { info.innerHTML = good ? t3("Escriu un nombre per a \\(a\\) (enter, decimal o fracció).", "Escribe un número para \\(a\\) (entero, decimal o fracción).", "Type a number for \\(a\\) (whole, decimal or fraction).").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }) : u("badP"); return; }
      var R = ruffini(P, a), v = pEval(P, a), dv = a.zero() ? "x" : "x" + (a.sgn() < 0 ? "+" + frT(a.neg()) : "-" + frT(a));
      var rows = [
        [t3("Valor numèric", "Valor numérico", "Value"), tex("P(" + frT(a) + ")=" + subT(P, a) + "=" + frT(v))],
        ["Ruffini", rufHtml(R, a) + t3("Dividim ", "Dividimos ", "Divide ") + tex("P(x):(" + dv + ")") + t3(": el residu és ", ": el resto es ", ": the remainder is ") + tex("r=" + frT(R.r))],
        [t3("Teorema del residu", "Teorema del resto", "Remainder theorem"), "<strong>" + tex("r=P(" + frT(a) + ")=" + frT(v)) + "</strong> " + ok(R.r.eq(v))]
      ];
      if (v.zero()) rows.push(["", t3("Com que el residu és 0, ", "Como el resto es 0, ", "Since the remainder is 0, ") + tex("x=" + frT(a)) + t3(" és una <strong>arrel</strong> de ", " es una <strong>raíz</strong> de ", " is a <strong>root</strong> of ") + tex("P") + t3(" i ", " y ", " and ") + tex("(" + dv + ")") + t3(" n'és un factor: ", " es un factor: ", " is a factor: ") + tex("P(x)=(" + dv + ")(" + pTex(R.q) + ")")]);
      else rows.push(["", "<small>" + t3("Els dos camins donen el mateix nombre. Amb Ruffini és més ràpid si el polinomi té molts termes o el grau és alt.", "Los dos caminos dan el mismo número. Con Ruffini es más rápido si el polinomio tiene muchos términos o el grado es alto.", "Both ways give the same number. Ruffini is quicker when the polynomial has many terms or a high degree.") + "</small>"]);
      info.innerHTML = kv(rows);
    }
    ["p", "a"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 2.4 cerca d'arrels enteres ---------- */
  function wArr() {
    var w = byId("w-arr"); if (!w) return;
    var info = w.querySelector(".info");
    var PRE = ["x^3-2x^2-5x+6", "x^3+x^2-4x-4", "x^4-5x^2+4", "x^3-3x+2", "x^3+x+1", "2x^3-3x^2-3x+2"];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(pTex(parsePoly(p))); }); }, function (i) { $(w, "p").value = PRE[i]; draw(); });
    function draw() {
      var P0 = parsePoly($(w, "p").value), good = P0 && pDeg(P0) >= 1 && pDeg(P0) <= 8;
      $(w, "p").classList.toggle("bad", !good);
      if (!good) { info.innerHTML = u("badP"); return; }
      var I = intForm(P0), P = I.P, k = 0, rows = [], h = "";
      while (P[k].zero()) k++;
      if (k) rows.push([t3("Factor comú", "Factor común", "Common factor"), tex(pTex(P) + "=" + (k === 1 ? "x" : "x^{" + k + "}") + "\\left(" + pTex(P.slice(k)) + "\\right)") + " → " + tex("x=0") + t3(" és arrel", " es raíz", " is a root")]);
      var Q = P.slice(k), a0 = Q[0].n, ds = divisors(a0);
      if (!ds || ds.length > 16) { info.innerHTML = kv(rows.concat([["", t3("El terme independent té massa divisors per a provar-los tots ací.", "El término independiente tiene demasiados divisores para probarlos todos aquí.", "The constant term has too many divisors to try them all here.")]])); return; }
      if (pDeg(Q) < 1) { info.innerHTML = kv(rows); return; }
      var cands = []; ds.forEach(function (d) { cands.push(d, -d); });
      var roots = [];
      h = '<div class="tbl-wrap"><table class="data cand"><thead><tr><th>' + tex("x") + "</th>" + cands.map(function (c) { return "<th>" + tex(String(c)) + "</th>"; }).join("") + "</tr></thead><tbody><tr><td>" + tex("P(x)") + "</td>";
      cands.forEach(function (c) { var v = pEval(Q, new Fr(c)); if (v.zero()) roots.push(c); h += "<td" + (v.zero() ? ' class="yes"' : "") + ">" + tex(frT(v)) + "</td>"; });
      h += "</tr></tbody></table></div>";
      rows.push([t3("Candidats", "Candidatos", "Candidates"), t3("divisors del terme independent ", "divisores del término independiente ", "divisors of the constant term ") + tex(String(a0)) + ": " + tex(cands.map(String).join(",\\ "))]);
      if (k) h = "<p><small>" + t3("Busquem les arrels de ", "Buscamos las raíces de ", "We look for the roots of ") + tex(pTex(Q)) + "</small></p>" + h;
      var lead = Q[Q.length - 1].n, all = (k ? ["0"] : []).concat(roots.map(String));
      rows.push([t3("Arrels enteres", "Raíces enteras", "Integer roots"), all.length ? tex(all.map(function (r) { return "x=" + r; }).join(",\\ ")) : t3("cap", "ninguna", "none")]);
      var note = Math.abs(lead) !== 1 ? t3("Com que el coeficient principal no és ±1, també hi pot haver arrels fraccionàries ", "Como el coeficiente principal no es ±1, también puede haber raíces fraccionarias ", "Since the leading coefficient isn't ±1, there may also be fractional roots ") + tex("\\tfrac pq") + t3(" (\\(q\\) divisor de ", " (\\(q\\) divisor de ", " (\\(q\\) dividing ").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }) + tex(String(lead)) + ")." :
        t3("Comprovar cada candidat calculant ", "Comprobar cada candidato calculando ", "Checking each candidate by working out ") + tex("P(a)") + t3(" és el mateix que fer Ruffini i mirar el residu.", " es lo mismo que hacer Ruffini y mirar el resto.", " is the same as running Ruffini and looking at the remainder.");
      rows.push(["", "<small>" + note + " " + t3("Un polinomi de grau ", "Un polinomio de grado ", "A polynomial of degree ") + pDeg(P) + t3(" té, com a màxim, ", " tiene, como máximo, ", " has at most ") + pDeg(P) + t3(" arrels.", " raíces.", " roots.") + "</small>"]);
      info.innerHTML = h + kv(rows);
    }
    $(w, "p").addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 2.6 m.c.d. i m.c.m. de polinomis ---------- */
  function wMcm() {
    var w = byId("w-mcm"); if (!w) return;
    var info = w.querySelector(".info");
    var PRE = [["x^2-1", "x^2+2x+1"], ["x^3-4x", "x^2-4x+4"], ["2x^2-2", "3x^2-3x"], ["x^3-x^2", "x^4-x^2"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(pTex(parsePoly(p[0])) + ",\\ " + pTex(parsePoly(p[1]))); }); }, function (i) { $(w, "p").value = PRE[i][0]; $(w, "q").value = PRE[i][1]; draw(); });
    function draw() {
      var P = parsePoly($(w, "p").value), Q = parsePoly($(w, "q").value), gP = P && pDeg(P) >= 1 && pDeg(P) <= 8, gQ = Q && pDeg(Q) >= 1 && pDeg(Q) <= 8;
      $(w, "p").classList.toggle("bad", !gP); $(w, "q").classList.toggle("bad", !gQ);
      if (!gP || !gQ) { info.innerHTML = u("badP") + " " + t3("(grau entre 1 i 8)", "(grado entre 1 y 8)", "(degree 1 to 8)"); return; }
      var A = facList(P), B = facList(Q), M = mcdMcm(A, B);
      info.innerHTML = kv([
        [t3("Factoritzem", "Factorizamos", "Factorise"), tex("P(x)=" + listT(A)) + "<br>" + tex("Q(x)=" + listT(B))],
        [t3("m.c.d.", "m.c.d.", "GCD"), "<strong>" + tex("\\text{m.c.d.}(P,Q)=" + listT(M.mcd)) + "</strong><br><small>" + t3("factors comuns elevats al menor exponent", "factores comunes elevados al menor exponente", "common factors to the lowest power") + "</small>"],
        [t3("m.c.m.", "m.c.m.", "LCM"), "<strong>" + tex("\\text{m.c.m.}(P,Q)=" + listT(M.mcm)) + "</strong><br><small>" + t3("factors comuns i no comuns elevats al major exponent", "factores comunes y no comunes elevados al mayor exponente", "common and non-common factors to the highest power") + "</small>"],
        ["", "<small>" + (M.mcd.fs.length ? "" : t3("No tenen cap factor comú: són primers entre si. ", "No tienen ningún factor común: son primos entre sí. ", "They share no factor: they are coprime. ")) + t3("Els nombres que multipliquen (el m.c.d. i el m.c.m. dels coeficients) es posen per costum, però no canvien quins són els divisors.", "Los números que multiplican (el m.c.d. y el m.c.m. de los coeficientes) se ponen por costumbre, pero no cambian cuáles son los divisores.", "The numbers in front (the GCD and LCM of the coefficients) are included by convention but don't change which polynomials divide.") + "</small>"]
      ]);
    }
    ["p", "q"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 2.7 operacions amb fraccions algebraiques ---------- */
  function wFop() {
    var w = byId("w-fop"); if (!w) return;
    var info = w.querySelector(".info"), sel = $(w, "op");
    var PRE = [["x", "x-1", "+", "2", "x^2-1"], ["3", "x+2", "-", "1", "x"], ["x^2-9", "x^2+2x", "*", "x+2", "x-3"], ["2x-4", "x^2", "/", "x^2-4", "x"]];
    var OPT = { "+": "+", "-": "-", "*": "\\cdot", "/": ":" };
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex("\\frac{" + pTex(parsePoly(p[0])) + "}{" + pTex(parsePoly(p[1])) + "}" + OPT[p[2]] + "\\frac{" + pTex(parsePoly(p[3])) + "}{" + pTex(parsePoly(p[4])) + "}"); }); },
      function (i) { var p = PRE[i]; $(w, "n1").value = p[0]; $(w, "d1").value = p[1]; sel.value = p[2]; $(w, "n2").value = p[3]; $(w, "d2").value = p[4]; draw(); });
    function draw() {
      var n1 = parsePoly($(w, "n1").value), d1 = parsePoly($(w, "d1").value), n2 = parsePoly($(w, "n2").value), d2 = parsePoly($(w, "d2").value), op = sel.value;
      var g = { n1: n1 && pDeg(n1) <= 6, d1: d1 && pDeg(d1) >= 0 && pDeg(d1) <= 6 && !(pDeg(d1) === 0 && d1[0].zero()), n2: n2 && pDeg(n2) <= 6, d2: d2 && pDeg(d2) >= 0 && pDeg(d2) <= 6 && !(pDeg(d2) === 0 && d2[0].zero()) };
      if (op === "/" && n2 && pDeg(n2) === -Infinity) g.n2 = false;
      ["n1", "d1", "n2", "d2"].forEach(function (k) { $(w, k).classList.toggle("bad", !g[k]); });
      if (!g.n1 || !g.d1 || !g.n2 || !g.d2) { info.innerHTML = u("badP") + " " + t3("(grau fins a 6; els denominadors no poden ser 0)", "(grado hasta 6; los denominadores no pueden ser 0)", "(degree up to 6; denominators can't be 0)"); return; }
      var F1T = "\\dfrac{" + pTex(n1) + "}{" + pTex(d1) + "}", F2T = "\\dfrac{" + pTex(n2) + "}{" + pTex(d2) + "}", rows = [[t3("Operació", "Operación", "Operation"), tex(F1T + OPT[op] + F2T)]], N, D, excl = [d1, d2];
      var A1 = facList(d1), A2 = facList(d2);
      if (op === "+" || op === "-") {
        var M = mcdMcm(A1, A2).mcm, Mp = listPoly(M), f1 = pDivide(Mp, d1).q, f2 = pDivide(Mp, d2).q;
        var dT = [[d1, A1], [d2, A2]].filter(function (x) { return listT(x[1]) !== pTex(x[0]); }).map(function (x) { return pTex(x[0]) + "=" + listT(x[1]); });
        if (dT.length) rows.push([t3("Factoritzem", "Factorizamos", "Factorise"), tex(dT.join(",\\quad "))]);
        rows.push([t3("m.c.m.", "m.c.m.", "LCM"), tex(listT(M))]);
        var p1 = pMul(n1, f1), p2 = pMul(n2, f2);
        N = op === "+" ? pAdd(p1, p2) : pSub(p1, p2); D = Mp;
        rows.push([t3("Comú denominador", "Común denominador", "Common denominator"), tex("\\dfrac{" + mulT(n1, f1) + op + mulT(n2, f2) + "}{" + listT(M) + "}")]);
        rows.push([t3("Numerador", "Numerador", "Numerator"), tex((function () { var l = op === "-" ? pTex(p1) + "-" + parT(p2) : pTex(p1) + (p2[p2.length - 1].sgn() < 0 ? "" : "+") + pTex(p2); return l === pTex(N) ? l : l + "=" + pTex(N); })())]);
      } else {
        var B1 = facList(n1.length && pDeg(n1) >= 0 ? n1 : [F0]), B2 = facList(n2);
        if (op === "*") { N = pMul(n1, n2); D = pMul(d1, d2);
          rows.push([t3("Multipliquem", "Multiplicamos", "Multiply"), tex("\\dfrac{" + (pDeg(n1) === -Infinity ? "0" : listT(B1, true)) + "\\cdot " + listT(B2, true) + "}{" + listT(A1, true) + "\\cdot " + listT(A2, true) + "}") + "<br><small>" + t3("Factoritzem abans de multiplicar: així es veu què se simplifica.", "Factorizamos antes de multiplicar: así se ve qué se simplifica.", "Factorise before multiplying: then you see what cancels.") + "</small>"]);
        } else { N = pMul(n1, d2); D = pMul(d1, n2); excl.push(n2);
          rows.push([t3("Multipliquem en creu", "Multiplicamos en cruz", "Cross-multiply"), tex("\\dfrac{" + (pDeg(n1) === -Infinity ? "0" : listT(B1, true)) + "\\cdot " + listT(A2, true) + "}{" + listT(A1, true) + "\\cdot " + listT(B2, true) + "}")]);
        }
      }
      var S = simpFrac(N, D);
      rows.push([t3("Resultat", "Resultado", "Result"), "<strong>" + tex(S.tex) + "</strong>" + (S.ex !== S.tex ? "<br>" + tex("=" + S.ex) : "")]);
      rows.push([t3("Té sentit si", "Tiene sentido si", "Defined for"), exclT(excl)]);
      info.innerHTML = kv(rows);
    }
    ["n1", "d1", "n2", "d2"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    sel.addEventListener("change", draw);
    onLang(draw);
  }

  /* ---------- autoavaluació ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("Quin és el grau de $P(x)=3x^2-5x^4+x-7$?", "¿Cuál es el grado de $P(x)=3x^2-5x^4+x-7$?", "What is the degree of $P(x)=3x^2-5x^4+x-7$?"),
      o: [q3("$2$"), q3("$4$"), q3("$3$")], a: 1, e: q3("El terme de grau més alt és $-5x^4$.", "El término de mayor grado es $-5x^4$.", "The highest-degree term is $-5x^4$.") },
    { q: q3("El terme independent de $P(x)=2x^3-x+6$ és…", "El término independiente de $P(x)=2x^3-x+6$ es…", "The constant term of $P(x)=2x^3-x+6$ is…"),
      o: [q3("$2$"), q3("$-1$"), q3("$6$")], a: 2, e: q3("És el terme sense $x$.", "Es el término sin $x$.", "It's the term with no $x$.") },
    { q: q3("Quin és el grau de $P(x)\\cdot Q(x)$ si $P$ té grau 3 i $Q$ té grau 2?", "¿Cuál es el grado de $P(x)\\cdot Q(x)$ si $P$ tiene grado 3 y $Q$ tiene grado 2?", "What is the degree of $P(x)\\cdot Q(x)$ if $P$ has degree 3 and $Q$ has degree 2?"),
      o: [q3("$6$"), q3("$5$"), q3("$3$")], a: 1, e: q3("Els graus se sumen: $3+2=5$.", "Los grados se suman: $3+2=5$.", "Degrees add up: $3+2=5$.") },
    { q: q3("$(2x-3)^2=$"), o: [q3("$4x^2-9$"), q3("$4x^2-12x+9$"), q3("$4x^2-6x+9$")], a: 1, e: q3("$(a-b)^2=a^2-2ab+b^2$: $4x^2-2\\cdot2x\\cdot3+9$.") },
    { q: q3("Si $P(x)=x^3-2x+5$, $P(-2)=$"), o: [q3("$1$"), q3("$9$"), q3("$-7$")], a: 0, e: q3("$(-2)^3-2(-2)+5=-8+4+5=1$.") },
    { q: q3("El residu de $(x^3-2x+5):(x+2)$ és…", "El resto de $(x^3-2x+5):(x+2)$ es…", "The remainder of $(x^3-2x+5):(x+2)$ is…"),
      o: [q3("$1$"), q3("$9$"), q3("$-1$")], a: 0, e: q3("Pel teorema del residu, és $P(-2)=1$.", "Por el teorema del resto, es $P(-2)=1$.", "By the remainder theorem, it's $P(-2)=1$.") },
    { q: q3("Si $P(3)=0$, aleshores…", "Si $P(3)=0$, entonces…", "If $P(3)=0$, then…"),
      o: [q3("$P(x)$ és divisible per $x+3$", "$P(x)$ es divisible por $x+3$", "$P(x)$ is divisible by $x+3$"), q3("$P(x)$ és divisible per $x-3$", "$P(x)$ es divisible por $x-3$", "$P(x)$ is divisible by $x-3$"), q3("el terme independent és 3", "el término independiente es 3", "the constant term is 3")],
      a: 1, e: q3("$x=3$ és una arrel, i $(x-3)$ és un factor.", "$x=3$ es una raíz, y $(x-3)$ es un factor.", "$x=3$ is a root, so $(x-3)$ is a factor.") },
    { q: q3("Quin d'aquests nombres <strong>no</strong> pot ser una arrel entera de $x^3+2x^2-5x-6$?", "¿Cuál de estos números <strong>no</strong> puede ser una raíz entera de $x^3+2x^2-5x-6$?", "Which of these numbers <strong>can't</strong> be an integer root of $x^3+2x^2-5x-6$?"),
      o: [q3("$-3$"), q3("$4$"), q3("$2$")], a: 1, e: q3("Les arrels enteres són divisors de $-6$, i 4 no ho és.", "Las raíces enteras son divisores de $-6$, y 4 no lo es.", "Integer roots divide $-6$, and 4 doesn't.") },
    { q: q3("$x^3-4x$ factoritzat és…", "$x^3-4x$ factorizado es…", "$x^3-4x$ factorised is…"),
      o: [q3("$x(x-2)^2$"), q3("$x(x+2)(x-2)$"), q3("$(x-2)(x^2+2x)$")], a: 1, e: q3("Factor comú i diferència de quadrats: $x(x^2-4)=x(x+2)(x-2)$.", "Factor común y diferencia de cuadrados: $x(x^2-4)=x(x+2)(x-2)$.", "Common factor and difference of squares: $x(x^2-4)=x(x+2)(x-2)$.") },
    { q: q3("$\\text{m.c.d.}\\left(x^2-1,\\ x^2+2x+1\\right)=$"), o: [q3("$x+1$"), q3("$(x+1)^2(x-1)$"), q3("$1$")], a: 0, e: q3("$(x+1)(x-1)$ i $(x+1)^2$: l'únic factor comú és $x+1$, amb el menor exponent.", "$(x+1)(x-1)$ y $(x+1)^2$: el único factor común es $x+1$, con el menor exponente.", "$(x+1)(x-1)$ and $(x+1)^2$: the only common factor is $x+1$, to the lowest power.") },
    { q: q3("$\\text{m.c.m.}\\left(x^2-1,\\ x^2+2x+1\\right)=$"), o: [q3("$(x+1)(x-1)$"), q3("$(x+1)^2(x-1)$"), q3("$(x+1)^3(x-1)$")], a: 1, e: q3("Tots els factors amb el major exponent: $(x+1)^2(x-1)$.", "Todos los factores con el mayor exponente: $(x+1)^2(x-1)$.", "Every factor to the highest power: $(x+1)^2(x-1)$.") },
    { q: q3("$\\dfrac{x^2-9}{x^2+3x}=$"), o: [q3("$\\dfrac{x-3}{x}$"), q3("$\\dfrac{-9}{3x}$"), q3("$x-3$")], a: 0, e: q3("$\\dfrac{(x+3)(x-3)}{x(x+3)}$: només se simplifiquen factors.", "$\\dfrac{(x+3)(x-3)}{x(x+3)}$: solo se simplifican factores.", "$\\dfrac{(x+3)(x-3)}{x(x+3)}$: only factors cancel.") },
    { q: q3("$\\dfrac{1}{x}+\\dfrac{1}{x+1}=$"), o: [q3("$\\dfrac{2}{2x+1}$"), q3("$\\dfrac{2x+1}{x(x+1)}$"), q3("$\\dfrac{2}{x(x+1)}$")], a: 1, e: q3("Comú denominador $x(x+1)$: $\\dfrac{(x+1)+x}{x(x+1)}$.", "Común denominador $x(x+1)$: $\\dfrac{(x+1)+x}{x(x+1)}$.", "Common denominator $x(x+1)$: $\\dfrac{(x+1)+x}{x(x+1)}$.") },
    { q: q3("$\\dfrac{x}{x-2}:\\dfrac{x^2}{x-2}=$"), o: [q3("$\\dfrac1x$"), q3("$x$"), q3("$\\dfrac{x^3}{(x-2)^2}$")], a: 0, e: q3("$\\dfrac{x(x-2)}{(x-2)x^2}=\\dfrac1x$.") }
  ];

  /*@@GENERIC@@*/
  var TITLES = { va: "Polinomis i fraccions algebraiques · FentMates", es: "Polinomios y fracciones algebraicas · FentMates", en: "Polynomials and algebraic fractions · FentMates" };
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
    var all = [wChrome, wSteps, wNav, wPop, wDiv, wRuf, wRes, wArr, wFac, wMcm, wFrs, wFop, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM2 = { parsePoly: parsePoly, factorPoly: factorPoly, facTex: facTex, pTex: pTex, quadRoots: quadRoots, Fr: Fr, facList: facList, pMul: pMul };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
