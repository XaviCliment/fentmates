(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-4eso-a-u5-done";

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


  /* ---------- 5.8 rectes reals una sobre l'altra ---------- */
  // cada interval és [a, a inclòs, b, b inclòs]
  var INF = Infinity, STACKS = {
    a: { range: [-4, 5], rows: [{ l: "2x − 1 &lt; 5", S: [[-INF, 0, 3, 0]] }, { l: "x + 3 ≥ 1", S: [[-2, 1, INF, 0]] }], sol: [[-2, 1, 3, 0]] },
    c: { range: [-4, 5], rows: [{ l: "x² − 4 ≥ 0", S: [[-INF, 0, -2, 1], [2, 1, INF, 0]] }, { l: "2x − 1 &lt; 5", S: [[-INF, 0, 3, 0]] }], sol: [[-INF, 0, -2, 1], [2, 1, 3, 0]] },
    b: { range: [-3, 4], rows: [{ l: "x − 2 &gt; 0", S: [[2, 0, INF, 0]] }, { l: "x + 1 &lt; 0", S: [[-INF, 0, -1, 0]] }], sol: [] }
  };
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

  /* ---------- 5.4 recta i circumferència ---------- */
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


  /* ---------- recta frontera (mètode gràfic) ---------- */
  function halfLine(G, c, V, col) {
    var pts = Math.abs(c.b) > 1e-12 ? [[V[0] - 1, (c.c - c.a * (V[0] - 1)) / c.b], [V[1] + 1, (c.c - c.a * (V[1] + 1)) / c.b]] : [[c.c / c.a, V[2] - 1], [c.c / c.a, V[3] + 1]];
    return '<line x1="' + G.X(pts[0][0]) + '" y1="' + G.Y(pts[0][1]) + '" x2="' + G.X(pts[1][0]) + '" y2="' + G.Y(pts[1][1]) + '" stroke="' + col + '" stroke-width="2.4"' + (c.op.length === 1 ? ' stroke-dasharray="7 5"' : "") + "/>";
  }
  function halfFill(G, P) { return P.length >= 3 ? '<path d="M' + P.map(function (p) { return G.X(p[0]).toFixed(1) + " " + G.Y(p[1]).toFixed(1); }).join("L") + 'Z" fill="' + COL.r + '" fill-opacity=".22"/>' : ""; }

  /* ---------- 5.1 i 5.2 sistemes lineals 2x2: a1x+b1y=c1, a2x+b2y=c2 ---------- */
  var SYS_PRE = [[2, 1, 7, 1, -1, 2], [1, 2, 8, 3, -1, 3], [3, 2, 7, 5, -3, 18], [1, -1, 1, 2, -2, 5], [1, 1, 3, 2, 2, 6]];
  function sysRead(w) {
    var k = ["a1", "b1", "c1", "a2", "b2", "c2"], v = {}, good = true;
    k.forEach(function (r) { var f = parseFr($(w, r).value || "0"); $(w, r).classList.toggle("bad", !f); if (!f) good = false; v[r] = f; });
    if (good && ((v.a1.zero() && v.b1.zero()) || (v.a2.zero() && v.b2.zero()))) good = false;
    return good ? v : null;
  }
  function sysPre(w, onPick) {
    presetBtns($(w, "pre"), function () { var e = t3("Exemple", "Ejemplo", "Example"); return [e + " 1", e + " 2", e + " 3", "SI", "SCI"]; },
      function (i) { var P = SYS_PRE[i]; ["a1", "b1", "c1", "a2", "b2", "c2"].forEach(function (r, j) { $(w, r).value = P[j]; }); onPick(); });
  }
  function eqT(a, b, c) { var s = a.zero() ? "" : monT(a, 1, "x", true); s += b.zero() ? "" : monT(b, 1, "y", !s); return (s || "0") + "=" + frT(c); }
  function sysT(v) { return "\\begin{cases}" + eqT(v.a1, v.b1, v.c1) + "\\\\ " + eqT(v.a2, v.b2, v.c2) + "\\end{cases}"; }
  function sysSolve(v) {
    var D = v.a1.mul(v.b2).sub(v.a2.mul(v.b1));
    if (!D.zero()) { var x = v.c1.mul(v.b2).sub(v.c2.mul(v.b1)).div(D), y = v.a1.mul(v.c2).sub(v.a2.mul(v.c1)).div(D); return { kind: "SCD", x: x, y: y }; }
    // rectes paral·leles o coincidents: les equacions són proporcionals?
    var same = v.a1.mul(v.c2).sub(v.a2.mul(v.c1)).zero() && v.b1.mul(v.c2).sub(v.b2.mul(v.c1)).zero();
    return { kind: same ? "SCI" : "SI" };
  }
  function kindT(S) {
    return S.kind === "SCD" ? t3("<strong>Sistema compatible determinat</strong>: una única solució", "<strong>Sistema compatible determinado</strong>: una única solución", "<strong>Consistent and independent</strong>: exactly one solution")
      : S.kind === "SCI" ? t3("<strong>Sistema compatible indeterminat</strong>: infinites solucions", "<strong>Sistema compatible indeterminado</strong>: infinitas soluciones", "<strong>Consistent and dependent</strong>: infinitely many solutions")
      : t3("<strong>Sistema incompatible</strong>: cap solució", "<strong>Sistema incompatible</strong>: ninguna solución", "<strong>Inconsistent</strong>: no solution");
  }
  // dos punts d'una recta ax+by=c (per a la taula de valors)
  function twoPts(a, b, c) {
    if (b.zero()) { var x0 = c.div(a); return [[x0, F0], [x0, F1]]; }
    var xs = [F0, F1, new Fr(2), FM1, new Fr(-2), new Fr(3)], P = [];
    xs.forEach(function (x) { var y = c.sub(a.mul(x)).div(b); if (P.length < 2 && y.d === 1) P.push([x, y]); });
    if (P.length < 2) P = [[F0, c.div(b)], [F1, c.sub(a).div(b)]];
    return P;
  }
  function wGr() {
    var w = byId("w-gr"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg");
    sysPre(w, draw);
    function draw() {
      var v = sysRead(w), V = [-6, 6, -6, 6], G = gview({ x0: V[0], x1: V[1], y0: V[2], y1: V[3], W: 320, H: 320, sx: 1, sy: 1 }), Cl = clipSvg(svg, G), g = G.g + Cl.open;
      if (!v) { info.innerHTML = t3("Escriu nombres en totes les caselles (en cada equació, \\(a\\) i \\(b\\) no poden ser tots dos 0).", "Escribe números en todas las casillas (en cada ecuación, \\(a\\) y \\(b\\) no pueden ser ambos 0).", "Type numbers in every box (in each equation, \\(a\\) and \\(b\\) can't both be 0).").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }); svg.innerHTML = G.g; return; }
      var L = [{ a: v.a1.val(), b: v.b1.val(), c: v.c1.val(), op: "<=", col: COL.a }, { a: v.a2.val(), b: v.b2.val(), c: v.c2.val(), op: "<=", col: COL.b }];
      L.forEach(function (c) { g += halfLine(G, c, V, c.col); });
      var S = sysSolve(v), rows = [[t3("Sistema", "Sistema", "System"), tex(sysT(v))]];
      [[v.a1, v.b1, v.c1, COL.a], [v.a2, v.b2, v.c2, COL.b]].forEach(function (e, i) {
        var P = twoPts(e[0], e[1], e[2]);
        rows.push(['<i class="dot" style="background:' + e[3] + '"></i>' + t3("Recta ", "Recta ", "Line ") + (i + 1), t3("passa per ", "pasa por ", "goes through ") + tex("(" + frT(P[0][0]) + ",\\," + frT(P[0][1]) + ")") + t3(" i ", " y ", " and ") + tex("(" + frT(P[1][0]) + ",\\," + frT(P[1][1]) + ")")]);
        P.forEach(function (p) { g += dot(G, p[0].val(), p[1].val(), e[3], 3.5); });
      });
      if (S.kind === "SCD") { g += dot(G, S.x.val(), S.y.val(), COL.r, 6.5); rows.push([t3("Tall", "Corte", "Crossing"), t3("Les rectes es tallen en ", "Las rectas se cortan en ", "The lines cross at ") + "<strong>" + tex("(" + frT(S.x) + ",\\," + frT(S.y) + ")") + "</strong>"]); }
      else rows.push([t3("Posició", "Posición", "Position"), S.kind === "SI" ? t3("Les rectes són paral·leles: no es tallen.", "Las rectas son paralelas: no se cortan.", "The lines are parallel: they never meet.") : t3("Les rectes són coincidents: totes dues són la mateixa recta.", "Las rectas son coincidentes: las dos son la misma recta.", "The lines coincide: they are the same line.")]);
      rows.push(["", kindT(S)]);
      info.innerHTML = kv(rows);
      svg.setAttribute("viewBox", "0 0 " + G.W + " " + G.H); svg.innerHTML = g + Cl.close;
    }
    ["a1", "b1", "c1", "a2", "b2", "c2"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }
  function linV(p, q, v) { return pTex([p, q], v); } // p + q·v
  function subst(p, q, sv) { var t = p.zero() ? "" : frT(p); if (!q.zero()) t += (q.sgn() < 0 ? "-" : t ? "+" : "") + (q.abs().eq(F1) ? "" : frT(q.abs()) + "\\cdot ") + frP(sv); return t || "0"; }
  function par(t) { return /[+-]/.test(t.replace(/^-/, "")) ? "\\left(" + t + "\\right)" : t; }
  // passos de la resolució d'un sistema 2x2 (met: 0 substitució, 1 igualació, 2 reducció); afig les files a rows
  function metRows(v, met, rows) {
    var S = sysSolve(v), st = function (i) { return u("step") + " " + i; };
    // variables: E = [{a,b,c}] amb a coef. de x i b coef. de y
    var E = [{ a: v.a1, b: v.b1, c: v.c1 }, { a: v.a2, b: v.b2, c: v.c2 }];
    if (S.kind !== "SCD") {
      rows.push([t3("Resultat", "Resultado", "Result"), (S.kind === "SI" ? t3("En operar arribem a una igualtat impossible, com ", "Al operar llegamos a una igualdad imposible, como ", "Working it through gives an impossible equality, such as ") + tex("0=k\\neq0") : t3("En operar arribem a ", "Al operar llegamos a ", "Working it through gives ") + tex("0=0") + t3(": les dues equacions diuen el mateix.", ": las dos ecuaciones dicen lo mismo.", ": both equations say the same thing.")) + "<br>" + kindT(S)]);
      return rows;
    }
    var x = S.x, y = S.y;
    if (met === 0) {
      // aïllem la incògnita amb coeficient ±1 si n'hi ha
      var ch = null;
      [[0, "y"], [0, "x"], [1, "y"], [1, "x"]].forEach(function (c) { var co = c[1] === "x" ? E[c[0]].a : E[c[0]].b; if (!ch && co.abs().eq(F1)) ch = c; });
      if (!ch) ch = !E[0].b.zero() ? [0, "y"] : [0, "x"];
      var i = ch[0], j = 1 - i, vu = ch[1], vw = vu === "x" ? "y" : "x", cu = vu === "x" ? E[i].a : E[i].b, cw = vu === "x" ? E[i].b : E[i].a;
      var p = E[i].c.div(cu), q = cw.neg().div(cu), ex = linV(p, q, vw);
      rows.push([st(1), t3("Aïllem ", "Despejamos ", "Solve for ") + tex(vu) + t3(" en la ", " en la ", " in equation ") + (i + 1) + t3("a equació:", "ª ecuación:", ":") + "<br>" + tex(vu + "=" + ex)]);
      var cu2 = vu === "x" ? E[j].a : E[j].b, cw2 = vu === "x" ? E[j].b : E[j].a;
      var tU = cu2.zero() ? "" : (cu2.abs().eq(F1) ? "" : frT(cu2.abs())) + par(ex), tW = cw2.zero() ? "" : monT(cw2.abs(), 1, vw, true), sU = cu2.sgn() < 0 ? "-" : "+", sW = cw2.sgn() < 0 ? "-" : "+";
      var parts = vu === "x" ? [[sU, tU], [sW, tW]] : [[sW, tW], [sU, tU]], left = "";
      parts.forEach(function (q) { if (q[1]) left += (left ? q[0] : q[0] === "-" ? "-" : "") + q[1]; });
      var k1 = cw2.add(cu2.mul(q)), k0 = E[j].c.sub(cu2.mul(p)), sol = vw === "x" ? x : y, other = vu === "x" ? x : y;
      rows.push([st(2), t3("Substituïm en la ", "Sustituimos en la ", "Substitute into equation ") + (j + 1) + t3("a:", "ª:", ":") + "<br>" + tex(left + "=" + frT(E[j].c))]);
      rows.push([st(3), t3("Resolem l'equació de primer grau:", "Resolvemos la ecuación de primer grado:", "Solve the linear equation:") + "<br>" + tex(monT(k1, 1, vw, true) + "=" + frT(k0) + "\\Rightarrow " + vw + "=" + frT(sol))]);
      rows.push([st(4), t3("Calculem ", "Calculamos ", "Work out ") + tex(vu) + ":<br>" + tex(vu + "=" + subst(p, q, sol) + "=" + frT(other))]);
    } else if (met === 1) {
      var vu2 = !E[0].b.zero() && !E[1].b.zero() ? "y" : "x", vw2 = vu2 === "x" ? "y" : "x", P = [];
      E.forEach(function (e) { var cu = vu2 === "x" ? e.a : e.b, cw = vu2 === "x" ? e.b : e.a; P.push([e.c.div(cu), cw.neg().div(cu)]); });
      rows.push([st(1), t3("Aïllem ", "Despejamos ", "Solve both equations for ") + tex(vu2) + t3(" de les dues equacions:", " de las dos ecuaciones:", ":") + "<br>" + tex(vu2 + "=" + linV(P[0][0], P[0][1], vw2) + ",\\qquad " + vu2 + "=" + linV(P[1][0], P[1][1], vw2))]);
      rows.push([st(2), t3("Igualem les dues expressions:", "Igualamos las dos expresiones:", "Set the two expressions equal:") + "<br>" + tex(linV(P[0][0], P[0][1], vw2) + "=" + linV(P[1][0], P[1][1], vw2))]);
      var sol2 = vw2 === "x" ? x : y, oth2 = vu2 === "x" ? x : y;
      rows.push([st(3), tex(monT(P[0][1].sub(P[1][1]), 1, vw2, true) + "=" + frT(P[1][0].sub(P[0][0])) + "\\Rightarrow " + vw2 + "=" + frT(sol2))]);
      rows.push([st(4), t3("Substituïm en qualsevol de les dues:", "Sustituimos en cualquiera de las dos:", "Substitute into either one:") + "<br>" + tex(vu2 + "=" + frT(oth2))]);
    } else {
      // eliminem y (o x si cal) multiplicant per nombres que igualen els coeficients
      var el = !E[0].b.zero() && !E[1].b.zero() ? "y" : "x", kp = el === "y" ? "x" : "y";
      var c1 = el === "y" ? E[0].b : E[0].a, c2 = el === "y" ? E[1].b : E[1].a, m1, m2;
      if (c1.d === 1 && c2.d === 1) { var g = gcd(c1.n, c2.n) || 1, Lc = Math.abs(c1.n * c2.n) / g; m1 = new Fr(Lc / c1.n); m2 = new Fr(Lc / c2.n); } else { m1 = c2; m2 = c1; }
      function sc(e, m) { return { a: e.a.mul(m), b: e.b.mul(m), c: e.c.mul(m) }; }
      var A = sc(E[0], m1), B = sc(E[1], m2);
      rows.push([st(1), t3("Multipliquem perquè ", "Multiplicamos para que ", "Multiply so that ") + tex(el) + t3(" tinga el mateix coeficient a les dues equacions:", " tenga el mismo coeficiente en las dos ecuaciones:", " has the same coefficient in both equations:") + "<br>" +
        tex((m1.eq(F1) ? "" : "(" + frT(m1) + ")\\cdot E_1:\\ ") + eqT(A.a, A.b, A.c) + "\\qquad " + (m2.eq(F1) ? "" : "(" + frT(m2) + ")\\cdot E_2:\\ ") + eqT(B.a, B.b, B.c))]);
      var R = { a: A.a.sub(B.a), b: A.b.sub(B.b), c: A.c.sub(B.c) };
      rows.push([st(2), t3("Restem les equacions i ", "Restamos las ecuaciones y ", "Subtract the equations and ") + tex(el) + t3(" desapareix:", " desaparece:", " disappears:") + "<br>" + tex(eqT(R.a, R.b, R.c))]);
      var sol3 = kp === "x" ? x : y, oth3 = el === "x" ? x : y;
      rows.push([st(3), tex(kp + "=" + frT(sol3))]);
      rows.push([st(4), t3("Substituïm en una equació inicial i trobem ", "Sustituimos en una ecuación inicial y hallamos ", "Substitute into an original equation to find ") + tex(el) + ":<br>" + tex(el + "=" + frT(oth3))]);
    }
    rows.push([t3("Solució", "Solución", "Solution"), "<strong>" + tex("x=" + frT(x) + ",\\ \\ y=" + frT(y)) + "</strong> " + ok(true) + "<br><small>" + t3("Els tres mètodes donen la mateixa solució; tria el que faça els càlculs més senzills.", "Los tres métodos dan la misma solución; elige el que haga los cálculos más sencillos.", "All three methods give the same solution; pick whichever makes the working simplest.") + "</small>"]);
    return rows;
  }
  function wMet() {
    var w = byId("w-met"); if (!w) return;
    var info = w.querySelector(".info"), met = 0;
    presetBtns($(w, "met"), function () { return [t3("Substitució", "Sustitución", "Substitution"), t3("Igualació", "Igualación", "Equalisation"), t3("Reducció", "Reducción", "Elimination")]; }, function (i) { met = i; draw(); }, 0);
    sysPre(w, draw);
    function draw() {
      var v = sysRead(w);
      if (!v) { info.innerHTML = t3("Escriu nombres en totes les caselles.", "Escribe números en todas las casillas.", "Type numbers in every box."); return; }
      info.innerHTML = kv(metRows(v, met, [[t3("Sistema", "Sistema", "System"), tex(sysT(v))]]));
    }
    ["a1", "b1", "c1", "a2", "b2", "c2"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 5.8 sistemes d'inequacions de primer grau amb una incògnita ---------- */
  function wSys1() {
    var w = byId("w-sys1"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg"), last = 0, data = null;
    var PRE = [[2, -1, "<", 5, 1, 2, ">=", -1], [1, -2, ">", 0, 1, 1, "<", 0], [3, 0, "<=", 6, -1, 4, "<", 7], [1, 0, ">=", -2, 2, 1, "<=", 9]];
    var SY = { "<": "<", "<=": "≤", ">": ">", ">=": "≥" }, TX = { "<": "\\lt ", "<=": "\\le ", ">": "\\gt ", ">=": "\\ge " }, FL = { "<": ">", "<=": ">=", ">": "<", ">=": "<=" };
    ["op1", "op2"].forEach(function (r) { Object.keys(SY).forEach(function (o) { $(w, r).add(new Option(SY[o], o)); }); });
    function set(P) { ["a1", "b1", "op1", "c1", "a2", "b2", "op2", "c2"].forEach(function (r, i) { $(w, r).value = P[i]; }); }
    set(PRE[0]);
    presetBtns($(w, "pre"), function () { return PRE.map(function (P) { return tex("\\begin{cases}" + pTex([new Fr(P[1]), new Fr(P[0])]) + TX[P[2]] + P[3] + "\\\\ " + pTex([new Fr(P[5]), new Fr(P[4])]) + TX[P[6]] + P[7] + "\\end{cases}"); }); }, function (i) { set(PRE[i]); draw(); }, 0);
    function solve1(a, b, op, c) { // ax + b op c
      var rhs = c.sub(b);
      if (a.zero()) { var v = 0, cv = rhs.val(), h = { "<": v < cv, "<=": v <= cv, ">": v > cv, ">=": v >= cv }[op]; return { S: h ? [[-INF, 0, INF, 0]] : [], t: tex("0" + TX[op] + frT(rhs)) + ": " + (h ? t3("sempre", "siempre", "always") : t3("mai", "nunca", "never")) }; }
      var r = rhs.div(a), o = a.sgn() < 0 ? FL[op] : op, cl = o.length === 2 ? 1 : 0, rv = r.val();
      return { S: o.charAt(0) === "<" ? [[-INF, 0, rv, cl]] : [[rv, cl, INF, 0]], t: tex(monT(a, 1, "x", true) + TX[op] + frT(rhs) + (a.eq(F1) ? "" : "\\Rightarrow x" + TX[o] + frT(r))) + (a.sgn() < 0 ? " <small>(" + t3("canvia el sentit", "cambia el sentido", "reversed") + ")</small>" : ""), r: r };
    }
    function capI(A, B) {
      if (!A.length || !B.length) return [];
      var I = A[0], J = B[0], lo = Math.max(I[0], J[0]), hi = Math.min(I[2], J[2]);
      var lc = I[0] > J[0] ? I[1] : J[0] > I[0] ? J[1] : I[1] && J[1], hc = I[2] < J[2] ? I[3] : J[2] < I[2] ? J[3] : I[3] && J[3];
      if (lo > hi || (lo === hi && !(lc && hc))) return [];
      return [[lo, lc, hi, hc]];
    }
    function ivT(S) { if (!S.length) return "\\varnothing"; var I = S[0]; if (I[0] === -INF && I[2] === INF) return "\\mathbb R"; return (I[1] ? "[" : "(") + (I[0] === -INF ? "-\\infty" : nT(I[0])) + ",\\," + (I[2] === INF ? "+\\infty" : nT(I[2])) + (I[3] ? "]" : ")"); }
    function lab(a, b, op, c) { return (pTex([b, a]).replace(/\{|\}/g, "").replace(/\^/g, "").replace(/-/g, " − ").replace(/\+/g, " + ").replace(/^ − /, "−")) + " " + { "<": "&lt;", "<=": "≤", ">": "&gt;", ">=": "≥" }[op] + " " + frT(c).replace("-", "−").replace(/\\frac\{(\d+)\}\{(\d+)\}/, "$1/$2"); }
    function paintS(force) { if (!data) return; var W = svgW(svg); if (W === last && !force) return; last = W; var r = nstack(data, true, W); svg.setAttribute("viewBox", "0 0 " + W + " " + r.H); svg.innerHTML = r.svg; }
    function draw() {
      var v = {}, good = true;
      ["a1", "b1", "c1", "a2", "b2", "c2"].forEach(function (r) { var f = parseFr($(w, r).value || "0"); $(w, r).classList.toggle("bad", !f); if (!f) good = false; v[r] = f; });
      if (!good) { info.innerHTML = t3("Escriu nombres en totes les caselles.", "Escribe números en todas las casillas.", "Type numbers in every box."); svg.innerHTML = ""; data = null; return; }
      var o1 = $(w, "op1").value, o2 = $(w, "op2").value, s1 = solve1(v.a1, v.b1, o1, v.c1), s2 = solve1(v.a2, v.b2, o2, v.c2), sol = capI(s1.S, s2.S);
      var pts = [0]; [s1, s2].forEach(function (s) { s.S.forEach(function (I) { if (isFinite(I[0])) pts.push(I[0]); if (isFinite(I[2])) pts.push(I[2]); }); });
      var lo = Math.floor(Math.min.apply(null, pts)) - 2, hi = Math.ceil(Math.max.apply(null, pts)) + 2; if (hi - lo < 7) { hi = lo + 7; }
      data = { range: [lo, hi], rows: [{ l: lab(v.a1, v.b1, o1, v.c1), S: s1.S }, { l: lab(v.a2, v.b2, o2, v.c2), S: s2.S }], sol: sol };
      info.innerHTML = kv([['<i class="dot" style="background:' + COL.a + '"></i>1', s1.t + " → " + tex(ivT(s1.S))], ['<i class="dot" style="background:' + COL.b + '"></i>2', s2.t + " → " + tex(ivT(s2.S))],
        [t3("Solució", "Solución", "Solution"), "<strong>" + tex(ivT(s1.S) + "\\cap " + ivT(s2.S) + "=" + ivT(sol)) + "</strong>" + (sol.length ? "" : "<br><small>" + t3("No tenen cap punt en comú: el sistema no té solució.", "No tienen ningún punto en común: el sistema no tiene solución.", "They share no point: the system has no solution.") + "</small>")]]);
      paintS(true);
    }
    ["a1", "b1", "c1", "a2", "b2", "c2", "op1", "op2"].forEach(function (r) { $(w, r).addEventListener("input", draw); $(w, r).addEventListener("change", draw); });
    if (window.ResizeObserver) new ResizeObserver(function () { paintS(false); }).observe(svg);
    onLang(draw);
  }

  /* ---------- 5.7 taula de signes ---------- */
  function wSign() {
    var w = byId("w-sign"); if (!w) return;
    var info = w.querySelector(".info"), tbl = $(w, "tbl"), svg = w.querySelector("svg.nl-svg"), op = 3;
    var OPS = ["\\lt", "\\le", "\\gt", "\\ge"];
    presetBtns($(w, "ops"), function () { return OPS.map(function (s) { return tex(s + " 0"); }); }, function (i) { op = i; draw(); }, 3);
    var PRE = [["x^2-5x+6", "1"], ["x^2-4", "1"], ["x^2-3x", "1"], ["-x^2+x+2", "1"], ["x^2+2x+1", "1"], ["x^2+1", "1"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(p[1] === "1" ? pTex(parsePoly(p[0])) : "\\frac{" + pTex(parsePoly(p[0])) + "}{" + pTex(parsePoly(p[1])) + "}"); }); }, function (i) { $(w, "n").value = PRE[i][0]; $(w, "d").value = PRE[i][1]; draw(); });
    function rowsOf(F, den) {
      var R = [];
      if (F.isConst) return R;
      if (F.k) R.push({ t: F.k === 1 ? "x" : "x^{" + F.k + "}", f: function (x) { return Math.pow(x, F.k); }, z: [0], den: den });
      F.lin.forEach(function (L) { var r = L.r.val(), q = L.r.d; R.push({ t: (L.r.zero() ? "x" : linT(L.r)) + (L.m > 1 ? "" : ""), tt: "(" + linT(L.r) + ")" + (L.m > 1 ? "^{" + L.m + "}" : ""), f: function (x) { return Math.pow(q * x - q * r, L.m); }, z: [r], den: den }); });
      F.irr.forEach(function (Q) { Q.roots.forEach(function (x) { var v = x.v; R.push({ tt: "\\left(" + irrFacT(x) + "\\right)" + (Q.m > 1 ? "^{" + Q.m + "}" : ""), f: function (y) { return Math.pow(y - v, Q.m); }, z: [v], den: den, irr: x }); }); });
      F.rest.forEach(function (Rs) { R.push({ tt: "(" + pTex(Rs.P) + ")" + (Rs.m > 1 ? "^{" + Rs.m + "}" : ""), f: function (x) { return Math.pow(pEvalN(Rs.P, x), Rs.m); }, z: [], den: den }); });
      return R;
    }
    function draw() {
      var N = parsePoly($(w, "n").value), D = parsePoly($(w, "d").value || "1");
      var gN = N && pDeg(N) >= 0 && pDeg(N) <= 8, gD = D && pDeg(D) >= 0 && pDeg(D) <= 8;
      $(w, "n").classList.toggle("bad", !gN); $(w, "d").classList.toggle("bad", !gD);
      if (!gN || !gD) { info.innerHTML = u("badP"); tbl.innerHTML = ""; svg.innerHTML = ""; return; }
      var fN = pDeg(N) >= 1 ? factorPoly(N) : { isConst: true, c: N[0], roots: [] }, fD = pDeg(D) >= 1 ? factorPoly(D) : { isConst: true, c: D[0], roots: [] };
      var rows = rowsOf(fN, false).concat(rowsOf(fD, true)), c = fN.c.div(fD.c);
      if (c.sgn() < 0) rows.unshift({ tt: frT(c), f: function () { return -1; }, z: [], den: false });
      rows.forEach(function (r) { if (!r.tt) r.tt = r.t; });
      var pts = [];
      function addPt(v, t, den) { var p = pts.filter(function (q) { return Math.abs(q.v - v) < 1e-9; })[0]; if (!p) { p = { v: v, t: t, num: false, den: false }; pts.push(p); } if (den) p.den = true; else p.num = true; }
      fN.roots.forEach(function (r) { addPt(r.v, r.tex, false); }); fD.roots.forEach(function (r) { addPt(r.v, r.tex, true); });
      pts.sort(function (a, b) { return a.v - b.v; });
      var rest = rows.filter(function (r) { return !r.z.length && r.tt !== frT(c); });
      // columnes: intervals i punts
      var cols = [], i;
      for (i = 0; i <= pts.length; i++) {
        var a = i ? pts[i - 1].v : -Infinity, b = i < pts.length ? pts[i].v : Infinity, mid = !isFinite(a) && !isFinite(b) ? 0 : !isFinite(a) ? b - 1 : !isFinite(b) ? a + 1 : (a + b) / 2;
        cols.push({ iv: true, a: a, b: b, mid: mid, ta: i ? pts[i - 1].t : "-\\infty", tb: i < pts.length ? pts[i].t : "+\\infty" });
        if (i < pts.length) cols.push({ iv: false, p: pts[i] });
      }
      function sg(v) { return v > 0 ? '<span class="sp">+</span>' : v < 0 ? '<span class="sm">−</span>' : "0"; }
      var head = "<tr><th></th>" + cols.map(function (c2) { return "<th>" + tex(c2.iv ? "(" + c2.ta + ",\\," + c2.tb + ")" : c2.p.t) + "</th>"; }).join("") + "</tr>";
      var body = rows.map(function (r) {
        return "<tr><td>" + tex(r.tt) + (r.den ? " <small>(" + t3("den.", "den.", "den.") + ")</small>" : "") + "</td>" + cols.map(function (c2) {
          if (c2.iv) return "<td>" + sg(r.f(c2.mid)) + "</td>";
          return "<td>" + (r.z.some(function (z) { return Math.abs(z - c2.p.v) < 1e-9; }) ? "0" : "") + "</td>";
        }).join("") + "</tr>";
      }).join("");
      var fval = function (x) { return pEvalN(N, x) / pEvalN(D, x); };
      var resRow = '<tr class="tot"><td>' + tex(pDeg(D) >= 1 ? "\\frac{P}{Q}" : "P(x)") + "</td>" + cols.map(function (c2) {
        if (c2.iv) return "<td>" + sg(fval(c2.mid)) + "</td>";
        return "<td>" + (c2.p.den ? "∄" : "0") + "</td>";
      }).join("") + "</tr>";
      tbl.innerHTML = '<div class="tbl-wrap"><table class="data sm sgn">' + head + body + resRow + "</table></div>";
      var want = op >= 2 ? 1 : -1, incl = op === 1 || op === 3, S = [];
      cols.forEach(function (c2) {
        if (c2.iv) { if (Math.sign(fval(c2.mid)) === want) S.push({ a: c2.a, ac: false, b: c2.b, bc: false }); }
        else if (incl && c2.p.num && !c2.p.den) S.push({ a: c2.p.v, ac: true, b: c2.p.v, bc: true });
      });
      S = norm(S);
      function lab(v) { var p = pts.filter(function (q) { return Math.abs(q.v - v) < 1e-9; })[0]; return p ? p.t.replace("\\approx ", "") : nT(v); }
      var W = svgW(svg); paint(svg, nline([{ S: S, c: COL.r }], { W: W, range: range([S.length ? S : [{ a: 0, b: 0 }]].concat([pts.map(function (p) { return { a: p.v, b: p.v }; })])) }), W);
      var ineq = (pDeg(D) >= 1 ? "\\dfrac{" + pTex(N) + "}{" + pTex(D) + "}" : pTex(N)) + OPS[op] + " 0";
      var notes = [];
      if (rest.length) notes.push(t3("Els factors sense arrels reals (com ", "Los factores sin raíces reales (como ", "Factors with no real roots (like ") + tex(rest[0].tt) + t3(") tenen sempre el mateix signe.", ") tienen siempre el mismo signo.", ") always keep the same sign."));
      if (pts.some(function (p) { return p.den; })) notes.push(t3("Les arrels del denominador no s'inclouen mai.", "Las raíces del denominador no se incluyen nunca.", "Roots of the denominator are never included."));
      info.innerHTML = kv([[t3("Inequació", "Inecuación", "Inequality"), tex(ineq)],
        [t3("Factoritzem", "Factorizamos", "Factorise"), tex(pDeg(D) >= 1 ? "\\dfrac{" + facTex(fN) + "}{" + facTex(fD) + "}" : facTex(fN))],
        [t3("Solució", "Solución", "Solution"), tex("x\\in " + setTL(S, lab))]].concat(notes.length ? [["", "<small>" + notes.join(" ") + "</small>"]] : []));
    }
    ["n", "d"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }


  /* ---------- 5.6 inequacions de primer grau: ax + b (op) cx + d ---------- */
  function wLin() {
    var w = byId("w-lin"); if (!w) return;
    var info = w.querySelector(".info"), svg = w.querySelector("svg"), op = 1;
    var OPS = ["\\lt", "\\le", "\\gt", "\\ge"], FLIP = [2, 3, 0, 1];
    presetBtns($(w, "ops"), function () { return OPS.map(function (s) { return tex(s); }); }, function (i) { op = i; draw(); }, 1);
    var PRE = [[3, -2, 1, 4, 1], [-2, 1, 0, 7, 0], [5, 3, 2, -6, 3], [1, 4, 1, 1, 2]];
    var bs = presetBtns($(w, "pre"), function () { return PRE.map(function (P) { return tex(lin(new Fr(P[0]), new Fr(P[1])) + OPS[P[4]] + lin(new Fr(P[2]), new Fr(P[3]))); }); },
      function (i) { var P = PRE[i]; ["a", "b", "c", "d"].forEach(function (k, j) { $(w, k).value = P[j]; }); op = P[4]; draw(); });
    function lin(a, b) { return pTex([b, a]); }
    function draw() {
      var a = parseFr($(w, "a").value), b = parseFr($(w, "b").value), c = parseFr($(w, "c").value), d = parseFr($(w, "d").value);
      ["a", "b", "c", "d"].forEach(function (k) { $(w, k).classList.toggle("bad", !parseFr($(w, k).value)); });
      [].forEach.call($(w, "ops").children, function (btn, i) { btn.classList.toggle("on", i === op); });
      if (!a || !b || !c || !d) { info.innerHTML = t3("Escriu quatre nombres (enters, decimals o fraccions).", "Escribe cuatro números (enteros, decimales o fracciones).", "Type four numbers (whole, decimal or fractions)."); svg.innerHTML = ""; return; }
      var s = OPS[op], A = a.sub(c), B = d.sub(b), rows = [], S;
      rows.push([t3("Inequació", "Inecuación", "Inequality"), tex(lin(a, b) + s + " " + lin(c, d))]);
      if (!(c.zero() && b.zero()) && !A.zero()) rows.push([t3("Agrupem", "Agrupamos", "Collect terms"), tex(lin(A, F0) + s + " " + frT(B))]);
      if (A.zero()) {
        var holds = op === 0 ? 0 < B.val() : op === 1 ? 0 <= B.val() : op === 2 ? 0 > B.val() : 0 >= B.val();
        rows.push(["", tex("0" + s + " " + frT(B)) + ": " + (holds ? t3("es compleix sempre", "se cumple siempre", "always true") : t3("no es compleix mai", "no se cumple nunca", "never true"))]);
        S = holds ? [{ a: -Infinity, ac: false, b: Infinity, bc: false }] : [];
      } else {
        var r = B.div(A), o2 = A.sgn() < 0 ? FLIP[op] : op;
        rows.push([t3("Aïllem", "Aislamos", "Isolate"), tex("x" + OPS[o2] + " \\dfrac{" + frT(B) + "}{" + frT(A) + "}=" + frT(r)) + (A.sgn() < 0 ? "<br><small><strong>" + t3("Hem dividit per un nombre negatiu: la desigualtat canvia de sentit.", "Hemos dividido por un número negativo: la desigualdad cambia de sentido.", "We divided by a negative number: the inequality is reversed.") + "</strong></small>" : "")]);
        var rv = r.val(), cl = o2 === 1 || o2 === 3;
        S = o2 <= 1 ? [{ a: -Infinity, ac: false, b: rv, bc: cl }] : [{ a: rv, ac: cl, b: Infinity, bc: false }];
      }
      rows.push([t3("Solució", "Solución", "Solution"), "<strong>" + tex("x\\in " + setTL(S)) + "</strong>"]);
      info.innerHTML = kv(rows);
      var W = svgW(svg); paint(svg, nline([{ S: S, c: COL.r }], { W: W }), W);
    }
    ["a", "b", "c", "d"].forEach(function (k) { $(w, k).addEventListener("input", draw); });
    onLang(draw);
  }



  /* ---------- autoavaluació ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  /*@@NOUS@@*/
  /*@@QUIZ@@*/

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
    var all = [wChrome, wSteps, wNav, wStacks, wGr, wMet, wSred, wNl, wPsys, wLin, wIneq, wSign, wSys1, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM2 = { parsePoly: parsePoly, factorPoly: factorPoly, facTex: facTex, pTex: pTex, quadRoots: quadRoots, Fr: Fr };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
