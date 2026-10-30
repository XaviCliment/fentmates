(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-3eso-u4-done", NSEC = 10;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc",
      write: "Escriu una expressió com 3x^2-5x+1 (el producte es pot escriure amb * o ·, o sense signe).", bad: "No entenc l'expressió. Revisa-la: exemple 3x^2-5x+1.",
      noParen: "Escriu el resultat desenvolupat, sense parèntesis.", num: "Escriu un nombre.", sol: "Solució:" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro",
      write: "Escribe una expresión como 3x^2-5x+1 (el producto se puede escribir con * o ·, o sin signo).", bad: "No entiendo la expresión. Revísala: ejemplo 3x^2-5x+1.",
      noParen: "Escribe el resultado desarrollado, sin paréntesis.", num: "Escribe un número.", sol: "Solución:" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Score", right: "Correct!", wrong: "Not correct.", theme: "Switch between light and dark mode",
      write: "Type an expression like 3x^2-5x+1 (multiply with * or ·, or with no sign).", bad: "I can't read that expression. Check it: e.g. 3x^2-5x+1.",
      noParen: "Write the expanded result, with no brackets.", num: "Type a number.", sol: "Solution:" }
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
  function segVal(w) { var b = w.querySelector('.seg button[aria-pressed="true"]'); return b ? b.dataset.k : null; }
  function warn(s) { return '<span class="warn">' + s + "</span>"; }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function rnz(a, b) { var k; do { k = rint(a, b); } while (k === 0); return k; }
  function hint(s) { return '<div class="hint">' + s + "</div>"; }
  function inputs(w) { var o = {}; w.querySelectorAll(".tin[data-k]").forEach(function (i) { o[i.dataset.k] = i; }); return o; }
  function quickBind(w, cb) { w.querySelectorAll(".quick button[data-b]").forEach(function (b) { b.addEventListener("click", function () { cb(b.dataset.b.split("|")); }); }); }

  /* ---------- racionals ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function rat(n, d) { if (d === undefined) d = 1; if (d < 0) { n = -n; d = -d; } var g = gcd(n, d) || 1; return { n: n / g, d: d / g }; }
  function radd(a, b) { return rat(a.n * b.d + b.n * a.d, a.d * b.d); }
  function rsub(a, b) { return rat(a.n * b.d - b.n * a.d, a.d * b.d); }
  function rmul(a, b) { return rat(a.n * b.n, a.d * b.d); }
  function rdiv(a, b) { return rat(a.n * b.d, a.d * b.n); }
  function rneg(a) { return { n: -a.n, d: a.d }; }
  function req(a, b) { return a.n === b.n && a.d === b.d; }
  function rpow(a, k) { var r = rat(1); for (var i = 0; i < k; i++) r = rmul(r, a); return r; }
  /* nombre en TeX: enter o fracció, amb signe */
  function nt(r) { return r.d === 1 ? String(r.n) : (r.n < 0 ? "-" : "") + "\\frac{" + Math.abs(r.n) + "}{" + r.d + "}"; }
  function ntp(r) { return r.n < 0 ? "(" + nt(r) + ")" : nt(r); }

  /* ---------- polinomis: { clau: { c: racional, e: { x: 2, y: 1 } } } ---------- */
  function mkey(e) { return Object.keys(e).filter(function (v) { return e[v]; }).sort().map(function (v) { return v + e[v]; }).join(" "); }
  function pconst(r) { var p = {}; if (r.n) p[""] = { c: r, e: {} }; return p; }
  function pvar(v) { var e = {}; e[v] = 1; var p = {}; p[mkey(e)] = { c: rat(1), e: e }; return p; }
  function pterm(c, e) { var p = {}; if (c.n) p[mkey(e)] = { c: c, e: e }; return p; }
  function padd(a, b) {
    var p = {}, k;
    for (k in a) p[k] = { c: a[k].c, e: a[k].e };
    for (k in b) { if (p[k]) p[k] = { c: radd(p[k].c, b[k].c), e: p[k].e }; else p[k] = { c: b[k].c, e: b[k].e }; if (!p[k].c.n) delete p[k]; }
    return p;
  }
  function pscale(a, r) { var p = {}; if (!r.n) return p; for (var k in a) p[k] = { c: rmul(a[k].c, r), e: a[k].e }; return p; }
  function pneg(a) { return pscale(a, rat(-1)); }
  function psub(a, b) { return padd(a, pneg(b)); }
  function emul(e1, e2, s) { var e = {}, v; for (v in e1) e[v] = (e[v] || 0) + e1[v]; for (v in e2) e[v] = (e[v] || 0) + s * e2[v]; for (v in e) if (!e[v]) delete e[v]; return e; }
  function pmul(a, b) { var p = {}; for (var i in a) for (var j in b) p = padd(p, pterm(rmul(a[i].c, b[j].c), emul(a[i].e, b[j].e, 1))); return p; }
  function ppow(a, n) { var p = pconst(rat(1)); for (var i = 0; i < n; i++) p = pmul(p, a); return p; }
  function tdeg(e) { var s = 0; for (var v in e) s += e[v]; return s; }
  function isZero(p) { return Object.keys(p).length === 0; }
  function peq(a, b) { return isZero(psub(a, b)); }
  function cmpE(a, b) {
    var d = tdeg(b.e) - tdeg(a.e); if (d) return d;
    var vs = Object.keys(a.e).concat(Object.keys(b.e)).sort();
    for (var i = 0; i < vs.length; i++) { var x = (b.e[vs[i]] || 0) - (a.e[vs[i]] || 0); if (x) return x; }
    return 0;
  }
  function terms(p) { return Object.keys(p).map(function (k) { return p[k]; }).sort(cmpE); }
  function pdeg(p) { var d = -Infinity; for (var k in p) d = Math.max(d, tdeg(p[k].e)); return d; }
  function pvars(p) { var s = {}; for (var k in p) for (var v in p[k].e) s[v] = 1; return Object.keys(s).sort(); }
  function isConst(p) { return isZero(p) || (Object.keys(p).length === 1 && p[""] !== undefined); }
  function cval(p) { return p[""] ? p[""].c : rat(0); }
  function negExp(p) { for (var k in p) for (var v in p[k].e) if (p[k].e[v] < 0) return true; return false; }
  /* TeX */
  function etex(e) { return Object.keys(e).sort().map(function (v) { return e[v] === 1 ? v : v + "^{" + e[v] + "}"; }).join(""); }
  function ttex(t, first) {
    var lit = etex(t.e), c = t.c, neg = c.n < 0, a = { n: Math.abs(c.n), d: c.d }, s;
    if (!lit) s = nt(a); else if (a.n === 1 && a.d === 1) s = lit; else s = nt(a) + lit;
    return (neg ? (first ? "-" : "-") : (first ? "" : "+")) + s;
  }
  function ptex(p) { var ts = terms(p); if (!ts.length) return "0"; return ts.map(function (t, i) { return ttex(t, i === 0); }).join(""); }
  function ptexp(p) { return Object.keys(p).length > 1 ? "(" + ptex(p) + ")" : (terms(p)[0] && terms(p)[0].c.n < 0 ? "(" + ptex(p) + ")" : ptex(p)); }
  function mono(c, e) { return terms(pterm(c, e))[0]; }
  /* exponents {v: k} (buit si k = 0) */
  function VE(v, k) { var e = {}; if (k) e[v] = k; return e; }

  /* ---------- analitzador d'expressions ---------- */
  function lex(s) {
    s = s.replace(/[−–]/g, "-").replace(/[·×]/g, "*").replace(/²/g, "^2").replace(/³/g, "^3").replace(/⁴/g, "^4").replace(/\s+/g, "");
    var out = [], i = 0, m;
    while (i < s.length) {
      var ch = s[i];
      if ((m = /^\d+(?:[.,]\d+)?/.exec(s.slice(i)))) {
        var str = m[0].replace(",", "."), parts = str.split("."), r;
        if (parts.length === 2) r = rat(parseInt(parts[0] + parts[1], 10), Math.pow(10, parts[1].length)); else r = rat(parseInt(str, 10));
        out.push({ t: "n", v: r }); i += m[0].length;
      } else if (/[a-z]/i.test(ch)) { out.push({ t: "v", v: ch.toLowerCase() }); i++; }
      else if ("+-*/:^()".indexOf(ch) >= 0) { out.push({ t: ch === ":" ? "/" : ch }); i++; }
      else if (ch === "[" || ch === "{") { out.push({ t: "(" }); i++; }
      else if (ch === "]" || ch === "}") { out.push({ t: ")" }); i++; }
      else return null;
    }
    return out;
  }
  function parse(s) {
    var tk = lex(s), i = 0;
    if (!tk || !tk.length) return null;
    function peek() { return tk[i] ? tk[i].t : null; }
    function expr() {
      var p = term();
      while (peek() === "+" || peek() === "-") { var o = tk[i++].t, q = term(); p = o === "+" ? padd(p, q) : psub(p, q); }
      return p;
    }
    function term() {
      var p = factor();
      for (;;) {
        var t = peek();
        if (t === "*") { i++; p = pmul(p, factor()); }
        else if (t === "/") {
          i++; var q = factor(), ts = terms(q);
          if (ts.length !== 1) throw "div";
          var inv = {}; for (var v in ts[0].e) inv[v] = -ts[0].e[v];
          p = pmul(p, pterm(rdiv(rat(1), ts[0].c), inv));
        }
        else if (t === "n" || t === "v" || t === "(") p = pmul(p, factor());
        else return p;
      }
    }
    function factor() {
      if (peek() === "-") { i++; return pneg(factor()); }
      if (peek() === "+") { i++; return factor(); }
      var b = base();
      while (peek() === "^") {
        i++; var neg = false;
        if (peek() === "-") { neg = true; i++; }
        if (peek() !== "n" || tk[i].v.d !== 1 || tk[i].v.n > 12) throw "exp";
        var k = tk[i++].v.n;
        if (neg) { var ts = terms(b); if (ts.length !== 1) throw "exp"; var e = {}; for (var v in ts[0].e) e[v] = -k * ts[0].e[v]; b = pterm(rpow(rdiv(rat(1), ts[0].c), k), e); }
        else b = ppow(b, k);
      }
      return b;
    }
    function base() {
      var t = tk[i];
      if (!t) throw "end";
      if (t.t === "n") { i++; return pconst(t.v); }
      if (t.t === "v") { i++; return pvar(t.v); }
      if (t.t === "(") { i++; var p = expr(); if (peek() !== ")") throw "par"; i++; return p; }
      throw "tok";
    }
    try { var p = expr(); if (i !== tk.length) return null; return p; } catch (e) { return null; }
  }
  /* polinomi en una variable -> coeficients [c0, c1, …] */
  function coeffs(p) {
    var vs = pvars(p); if (vs.length > 1 || negExp(p)) return null;
    var v = vs[0] || "x", n = Math.max(0, pdeg(p)), a = [];
    for (var k = 0; k <= n; k++) a.push(rat(0));
    for (var key in p) a[p[key].e[v] || 0] = p[key].c;
    return { v: v, a: a };
  }
  function fromC(a, v) { var p = {}; a.forEach(function (c, k) { var e = {}; if (k) e[v] = k; p = padd(p, pterm(c, e)); }); return p; }
  function evalAt(p, vals) { var s = rat(0); for (var k in p) { var t = p[k].c; for (var v in p[k].e) t = rmul(t, rpow(vals[v], p[k].e[v])); s = radd(s, t); } return s; }
  /* substitució mostrada: 3x^2-5x+1 amb x=-2 -> 3(-2)^2-5(-2)+1 */
  function substTex(p, vals) {
    return terms(p).map(function (t, i) {
      var a = { n: Math.abs(t.c.n), d: t.c.d }, vs = Object.keys(t.e).sort(), parts = [];
      vs.forEach(function (v) { var x = vals[v], b = x.n < 0 || x.d !== 1 ? "(" + nt(x) + ")" : nt(x); parts.push(t.e[v] === 1 ? b : b + "^{" + t.e[v] + "}"); });
      var s = (a.n === 1 && a.d === 1 && parts.length ? "" : nt(a) + (parts.length ? "\\cdot " : "")) + parts.join("\\cdot ");
      return (t.c.n < 0 ? "-" : i ? "+" : "") + s;
    }).join("");
  }

  /* ---------- giny: monomis (coeficient, part literal, grau) ---------- */
  function wMono() {
    var w = document.getElementById("w-mono"); if (!w) return;
    var inp = w.querySelector(".tin"), out = w.querySelector(".cards"), info = w.querySelector(".info");
    function paint() {
      var p = parse(inp.value), ts;
      out.innerHTML = ""; info.innerHTML = "";
      if (!p) { info.innerHTML = warn(u("bad")); return; }
      ts = terms(p);
      if (ts.length !== 1) { info.innerHTML = warn(fill(T(L3("No és un monomi: després d'operar té {n} termes, és a dir, és un polinomi.", "No es un monomio: después de operar tiene {n} términos, es decir, es un polinomio.", "It isn't a monomial: after simplifying it has {n} terms, so it's a polynomial.")), { n: ts.length })); return; }
      if (negExp(p)) { info.innerHTML = warn(T(L3("No és un monomi: una variable té exponent negatiu (està dividint).", "No es un monomio: una variable tiene exponente negativo (está dividiendo).", "It isn't a monomial: a variable has a negative exponent (it is dividing)."))); return; }
      var t = ts[0], vs = Object.keys(t.e).sort(), g = tdeg(t.e);
      function card(h, b) { return '<div class="card"><h4>' + h + "</h4><div>" + b + "</div></div>"; }
      out.innerHTML = card(T(L3("Monomi", "Monomio", "Monomial")), tex(ttex(t, true)))
        + card(T(L3("Coeficient", "Coeficiente", "Coefficient")), tex(nt(t.c)))
        + card(T(L3("Part literal", "Parte literal", "Variable part")), vs.length ? tex(etex(t.e)) : "—")
        + card(T(L3("Grau", "Grado", "Degree")), tex(vs.length ? vs.map(function (v) { return String(t.e[v]); }).join("+") + (vs.length > 1 ? "=" + g : "") : "0"));
      var s = vs.length ? T(L3("Grau respecte de cada variable: ", "Grado respecto de cada variable: ", "Degree in each variable: ")) + vs.map(function (v) { return tex(v + ":\\ " + t.e[v]); }).join(", ") + "."
        : T(L3("És un nombre sense part literal: un monomi de grau 0.", "Es un número sin parte literal: un monomio de grado 0.", "It's a number with no variable part: a monomial of degree 0."));
      if (vs.length && t.c.n === 1 && t.c.d === 1) s += " " + T(L3("Quan no s'escriu el coeficient, val 1.", "Cuando no se escribe el coeficiente, vale 1.", "When no coefficient is written, it is 1."));
      if (vs.length && t.c.n === -1 && t.c.d === 1) s += " " + T(L3("El signe − tot sol vol dir coeficient −1.", "El signo − solo quiere decir coeficiente −1.", "A lone − sign means coefficient −1."));
      info.innerHTML = s;
    }
    inp.addEventListener("input", paint);
    quickBind(w, function (v) { inp.value = v[0]; paint(); });
    onLang(paint);
  }

  /* ---------- giny: operacions amb monomis ---------- */
  function wMonOps() {
    var w = document.getElementById("w-monops"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), op = segVal(w) || "*";
    function paint() {
      out.innerHTML = ""; info.innerHTML = "";
      var a = parse(I.a.value), b = parse(I.b.value);
      if (!a || !b || Object.keys(a).length !== 1 || Object.keys(b).length !== 1 || negExp(a) || negExp(b)) { info.innerHTML = warn(T(L3("Escriu dos monomis, per exemple 6x^3y i -2xy.", "Escribe dos monomios, por ejemplo 6x^3y y -2xy.", "Type two monomials, for example 6x^3y and -2xy."))); return; }
      var A = terms(a)[0], B = terms(b)[0], s = [], ta = ttex(A, true), tb = ttex(B, true), tbp = B.c.n < 0 ? "(" + tb + ")" : tb;
      if (op === "+" || op === "-") {
        var head = "(" + ta + ")" + (op === "+" ? "+" : "-") + "(" + tb + ")";
        if (mkey(A.e) === mkey(B.e)) {
          var c = op === "+" ? radd(A.c, B.c) : rsub(A.c, B.c), lit = etex(A.e);
          s.push(T(L3("Són <b>semblants</b> (mateixa part literal " + tex(lit || "\\text{—}") + "): sumem o restem els coeficients i deixem la mateixa part literal.", "Son <b>semejantes</b> (misma parte literal " + tex(lit || "\\text{—}") + "): sumamos o restamos los coeficientes y dejamos la misma parte literal.", "They are <b>like terms</b> (same variable part " + tex(lit || "\\text{—}") + "): add or subtract the coefficients and keep the same variable part.")));
          s.push(tex(head + "=(" + nt(A.c) + (op === "+" ? "+" : "-") + ntp(B.c) + ")" + lit + "=\\boxed{" + ptex(pterm(c, A.e)) + "}", true));
        } else {
          var r = op === "+" ? padd(a, b) : psub(a, b);
          s.push(T(L3("<b>No són semblants</b> (tenen parts literals diferents): no es poden reduir a un sol monomi. El resultat és un polinomi:", "<b>No son semejantes</b> (tienen partes literales distintas): no se pueden reducir a un solo monomio. El resultado es un polinomio:", "<b>They aren't like terms</b> (different variable parts): they can't be combined into one monomial. The result is a polynomial:")));
          s.push(tex(head + "=\\boxed{" + ptex(r) + "}", true));
        }
      } else if (op === "*") {
        var e = emul(A.e, B.e, 1), vs = Object.keys(e).sort();
        s.push(T(L3("Multipliquem els coeficients i, per a cada variable, <b>sumem els exponents</b> (\\(x^m\\cdot x^n=x^{m+n}\\)).", "Multiplicamos los coeficientes y, para cada variable, <b>sumamos los exponentes</b> (\\(x^m\\cdot x^n=x^{m+n}\\)).", "Multiply the coefficients and, for each variable, <b>add the exponents</b> (\\(x^m\\cdot x^n=x^{m+n}\\)).")).replace(/\\\((.+?)\\\)/g, function (_, m) { return tex(m); }));
        var ex = vs.map(function (v) { var p1 = A.e[v] || 0, p2 = B.e[v] || 0; return p1 && p2 ? v + "^{" + p1 + "+" + p2 + "}" : v + (e[v] === 1 ? "" : "^{" + e[v] + "}"); }).join("");
        s.push(tex("(" + ta + ")\\cdot " + tbp + "=(" + nt(A.c) + "\\cdot " + ntp(B.c) + ")\\," + ex + "=\\boxed{" + ttex(mono(rmul(A.c, B.c), e), true) + "}", true));
      } else {
        var q = emul(A.e, B.e, -1), vq = Object.keys(emul(A.e, B.e, 1)).sort(), neg = vq.some(function (v) { return (q[v] || 0) < 0; });
        s.push(T(L3("Dividim els coeficients i, per a cada variable, <b>restem els exponents</b> (\\(x^m:x^n=x^{m-n}\\)).", "Dividimos los coeficientes y, para cada variable, <b>restamos los exponentes</b> (\\(x^m:x^n=x^{m-n}\\)).", "Divide the coefficients and, for each variable, <b>subtract the exponents</b> (\\(x^m:x^n=x^{m-n}\\)).")).replace(/\\\((.+?)\\\)/g, function (_, m) { return tex(m); }));
        var exq = vq.map(function (v) { var p1 = A.e[v] || 0, p2 = B.e[v] || 0; return v + "^{" + p1 + "-" + p2 + "}"; }).join("");
        var c2 = rdiv(A.c, B.c);
        if (neg) {
          s.push(tex("(" + ta + "):" + tbp + "=" + nt(c2) + "\\," + exq, true));
          s.push(warn(T(L3("Algun exponent queda negatiu: el divisor té més grau en alguna variable. El quocient <b>no és un monomi</b> (és una fracció algebraica).", "Algún exponente queda negativo: el divisor tiene más grado en alguna variable. El cociente <b>no es un monomio</b> (es una fracción algebraica).", "An exponent comes out negative: the divisor has a higher degree in some variable. The quotient <b>isn't a monomial</b> (it's an algebraic fraction)."))));
        } else {
          var qt = vq.map(function (v) { return (q[v] || 0) === 0 ? v + "^{0}=1" : ""; }).filter(Boolean);
          s.push(tex("(" + ta + "):" + tbp + "=" + nt(c2) + "\\," + exq + "=\\boxed{" + ttex(mono(c2, q), true) + "}", true));
          if (qt.length) s.push(T(L3("Recorda que \\(x^0=1\\): la variable desapareix.", "Recuerda que \\(x^0=1\\): la variable desaparece.", "Remember \\(x^0=1\\): the variable disappears.")).replace(/\\\((.+?)\\\)/g, function (_, m) { return tex(m); }));
        }
      }
      out.innerHTML = s.map(function (x) { return '<div class="hrow">' + x + "</div>"; }).join("");
    }
    [I.a, I.b].forEach(function (x) { x.addEventListener("input", paint); });
    segBind(w, function (k) { op = k; paint(); });
    quickBind(w, function (v) { I.a.value = v[0]; I.b.value = v[1]; op = v[2]; w.querySelectorAll(".seg button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.k === op)); }); paint(); });
    onLang(paint);
  }

  /* ---------- giny: valor numèric ---------- */
  function wVal() {
    var w = document.getElementById("w-val"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      out.innerHTML = ""; info.innerHTML = "";
      var p = parse(I.p.value), vals = {}, ok = true;
      if (!p || negExp(p)) { info.innerHTML = warn(u("bad")); return; }
      ["x", "y"].forEach(function (v) { var q = parse(I[v].value); if (q && isConst(q)) vals[v] = cval(q); else if (pvars(p).indexOf(v) >= 0) ok = false; });
      var extra = pvars(p).filter(function (v) { return v !== "x" && v !== "y"; });
      if (extra.length) { info.innerHTML = warn(T(L3("Usa només les variables x i y.", "Usa solo las variables x e y.", "Only use the variables x and y."))); return; }
      if (!ok) { info.innerHTML = warn(u("num")); return; }
      var r = evalAt(p, vals), vs = pvars(p);
      out.innerHTML = '<div class="hrow">' + tex(ptex(p), true) + "</div>"
        + '<div class="hrow">' + T(L3("Substituïm", "Sustituimos", "Substitute")) + " " + vs.map(function (v) { return tex(v + "=" + nt(vals[v])); }).join(", ") + " " + T(L3("(posa els negatius entre parèntesis!):", "(¡pon los negativos entre paréntesis!):", "(put negatives in brackets!):")) + "</div>"
        + '<div class="hrow">' + tex(substTex(p, vals) + "=" + terms(p).map(function (t, i) { var v = evalAt(pterm(t.c, t.e), vals); return (i && v.n >= 0 ? "+" : "") + nt(v); }).join("") + "=\\boxed{" + nt(r) + "}", true) + "</div>";
    }
    Object.keys(I).forEach(function (k) { I[k].addEventListener("input", paint); });
    quickBind(w, function (v) { I.p.value = v[0]; I.x.value = v[1]; I.y.value = v[2] || "0"; paint(); });
    onLang(paint);
  }

  /* ---------- giny: anàlisi d'un polinomi ---------- */
  function wPoly() {
    var w = document.getElementById("w-poly"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".cards"), extra = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      out.innerHTML = extra.innerHTML = info.innerHTML = "";
      var p = parse(I.p.value);
      if (!p || negExp(p)) { info.innerHTML = warn(u("bad")); return; }
      var C = coeffs(p);
      if (!C) { info.innerHTML = warn(T(L3("Aquest giny treballa amb polinomis d'una sola variable.", "Este widget trabaja con polinomios de una sola variable.", "This tool works with polynomials in one variable."))); return; }
      var v = C.v, a = C.a, n = a.length - 1, ts = terms(p);
      function card(h, b) { return '<div class="card"><h4>' + h + "</h4><div>" + b + "</div></div>"; }
      if (isZero(p)) { info.innerHTML = T(L3("És el polinomi zero.", "Es el polinomio cero.", "It's the zero polynomial.")); return; }
      var miss = []; for (var k = n; k >= 0; k--) if (!a[k].n) miss.push(k);
      out.innerHTML = card(T(L3("Ordenat", "Ordenado", "In order")), tex("P(" + v + ")=" + ptex(p)))
        + card(T(L3("Grau", "Grado", "Degree")), tex(String(n)))
        + card(T(L3("Nombre de termes", "Número de términos", "Number of terms")), tex(String(ts.length)) + " " + (["", T(L3("(monomi)", "(monomio)", "(monomial)")), T(L3("(binomi)", "(binomio)", "(binomial)")), T(L3("(trinomi)", "(trinomio)", "(trinomial)"))][ts.length] || ""))
        + card(T(L3("Coeficient principal", "Coeficiente principal", "Leading coefficient")), tex(nt(a[n])))
        + card(T(L3("Terme independent", "Término independiente", "Constant term")), tex(nt(a[0])))
        + card(T(L3("Complet?", "¿Completo?", "Complete?")), miss.length ? T(L3("No", "No", "No")) : T(L3("Sí", "Sí", "Yes")));
      var rows = '<div class="tbl-wrap"><table class="data ptab"><thead><tr><th>' + T(L3("Terme", "Término", "Term")) + "</th>";
      for (k = n; k >= 0; k--) rows += "<th>" + tex(k ? (k === 1 ? v : v + "^{" + k + "}") : "\\text{" + T(L3("indep.", "indep.", "const.")) + "}") + "</th>";
      rows += "</tr></thead><tbody><tr><th>" + T(L3("Coeficient", "Coeficiente", "Coefficient")) + "</th>";
      for (k = n; k >= 0; k--) rows += '<td class="' + (a[k].n ? "" : "z") + '">' + tex(nt(a[k])) + "</td>";
      rows += "</tr></tbody></table></div>";
      var s = rows;
      if (miss.length) s += '<div class="hrow">' + T(L3("Falten els termes de grau ", "Faltan los términos de grado ", "Missing the terms of degree ")) + miss.join(", ") + ". " + T(L3("Per a dividir (o fer Ruffini) l'escrivim complet, amb zeros:", "Para dividir (o hacer Ruffini) lo escribimos completo, con ceros:", "To divide (or use Ruffini) write it complete, with zeros:")) + " " + tex(a.map(function (c, k) { return { c: c, k: k }; }).reverse().map(function (o, i) { var t = (o.c.n ? nt({ n: Math.abs(o.c.n), d: o.c.d }) : "0"); if (o.k && t === "1") t = ""; return (i ? (o.c.n < 0 ? "-" : "+") : (o.c.n < 0 ? "-" : "")) + t + (o.k ? (o.k === 1 ? v : v + "^{" + o.k + "}") : (t === "" ? "1" : "")); }).join("")) + "</div>";
      var xv = parse(I.a.value);
      if (xv && isConst(xv)) { var vals = {}; vals[v] = cval(xv); s += '<div class="hrow">' + T(L3("Valor numèric:", "Valor numérico:", "Value:")) + " " + tex("P(" + nt(cval(xv)) + ")=" + substTex(p, vals) + "=\\boxed{" + nt(evalAt(p, vals)) + "}") + "</div>"; }
      extra.innerHTML = s;
    }
    Object.keys(I).forEach(function (k) { I[k].addEventListener("input", paint); });
    quickBind(w, function (v) { I.p.value = v[0]; I.a.value = v[1]; paint(); });
    onLang(paint);
  }

  /* ---------- taula de columnes per graus (sumes i restes) ---------- */
  function colRow(p, v, n, lead) {
    var C = coeffs(p), a = C ? C.a : [], cells = "";
    for (var k = n; k >= 0; k--) {
      var c = a[k];
      if (!c || !c.n) { cells += "<td></td>"; continue; }
      cells += "<td>" + tex(ttex(mono(c, VE(v, k)), false)) + "</td>";
    }
    return "<tr><th>" + lead + "</th>" + cells + "</tr>";
  }
  function wAddSub() {
    var w = document.getElementById("w-addsub"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), op = "+";
    function paint() {
      out.innerHTML = info.innerHTML = "";
      var P = parse(I.p.value), Q = parse(I.q.value);
      if (!P || !Q || negExp(P) || negExp(Q)) { info.innerHTML = warn(u("bad")); return; }
      var vs = pvars(padd(P, Q)), R = op === "+" ? padd(P, Q) : psub(P, Q), s = "";
      s += '<div class="hrow">' + tex("(" + ptex(P) + ")" + op.replace("-", "-") + "(" + ptex(Q) + ")", true) + "</div>";
      if (op === "-") s += '<div class="hrow">' + T(L3("Restar és sumar l'oposat: canviem el signe de <b>tots</b> els termes de Q.", "Restar es sumar el opuesto: cambiamos el signo de <b>todos</b> los términos de Q.", "Subtracting means adding the opposite: change the sign of <b>every</b> term of Q.")) + " " + tex("-Q=" + ptex(pneg(Q))) + "</div>";
      if (vs.length <= 1) {
        var v = vs[0] || "x", n = Math.max(0, pdeg(P), pdeg(Q));
        var tb = '<div class="tbl-wrap"><table class="data coltab"><tbody>' + colRow(P, v, n, tex("P")) + colRow(op === "+" ? Q : pneg(Q), v, n, tex(op === "+" ? "+Q" : "-Q")) + colRow(R, v, n, tex(op === "+" ? "P+Q" : "P-Q")).replace("<tr>", '<tr class="tot">') + "</tbody></table></div>";
        s += '<div class="hrow">' + T(L3("Col·loquem els termes semblants en columna (un grau en cada columna) i sumem:", "Colocamos los términos semejantes en columna (un grado en cada columna) y sumamos:", "Line up like terms in columns (one degree per column) and add:")) + "</div>" + tb;
      } else s += '<div class="hrow">' + T(L3("Agrupem els termes semblants:", "Agrupamos los términos semejantes:", "Group the like terms:")) + "</div>";
      s += '<div class="hrow">' + tex((op === "+" ? "P+Q" : "P-Q") + "=\\boxed{" + ptex(R) + "}", true) + "</div>";
      out.innerHTML = s;
    }
    [I.p, I.q].forEach(function (x) { x.addEventListener("input", paint); });
    segBind(w, function (k) { op = k; paint(); });
    quickBind(w, function (v) { I.p.value = v[0]; I.q.value = v[1]; paint(); });
    onLang(paint);
  }

  /* ---------- giny: producte de polinomis (taula) ---------- */
  function wMul() {
    var w = document.getElementById("w-mul"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      out.innerHTML = info.innerHTML = "";
      var P = parse(I.p.value), Q = parse(I.q.value);
      if (!P || !Q || negExp(P) || negExp(Q) || isZero(P) || isZero(Q)) { info.innerHTML = warn(u("bad")); return; }
      var tp = terms(P), tq = terms(Q), prods = [], cols = ["var(--r1)", "var(--r2)", "var(--r3)", "var(--r4)", "var(--plus)", "var(--minus)"];
      var tb = '<div class="tbl-wrap"><table class="data multab"><thead><tr><th>' + tex("\\cdot") + "</th>" + tq.map(function (t, j) { return "<th>" + tex(ttex(t, true)) + "</th>"; }).join("") + "</tr></thead><tbody>";
      var keys = {};
      tp.forEach(function (a) {
        tb += "<tr><th>" + tex(ttex(a, true)) + "</th>";
        tq.forEach(function (b) {
          var m = mono(rmul(a.c, b.c), emul(a.e, b.e, 1)), k = mkey(m.e);
          if (!(k in keys)) keys[k] = Object.keys(keys).length;
          prods.push(m);
          tb += '<td style="color:' + cols[keys[k] % cols.length] + '">' + tex(ttex(m, true)) + "</td>";
        });
        tb += "</tr>";
      });
      tb += "</tbody></table></div>";
      var R = pmul(P, Q);
      var s = '<div class="hrow">' + tex("(" + ptex(P) + ")\\cdot(" + ptex(Q) + ")", true) + "</div>"
        + '<div class="hrow">' + T(L3("Multipliquem <b>cada terme</b> del primer per <b>cada terme</b> del segon (propietat distributiva). Els termes semblants tenen el mateix color:", "Multiplicamos <b>cada término</b> del primero por <b>cada término</b> del segundo (propiedad distributiva). Los términos semejantes tienen el mismo color:", "Multiply <b>each term</b> of the first by <b>each term</b> of the second (distributive law). Like terms share a colour:")) + "</div>" + tb
        + '<div class="hrow">' + tex("=" + prods.map(function (m, i) { return ttex(m, i === 0); }).join(""), true) + "</div>"
        + '<div class="hrow">' + T(L3("Reduïm els termes semblants:", "Reducimos los términos semejantes:", "Collect like terms:")) + " " + tex("\\boxed{" + ptex(R) + "}") + "</div>";
      out.innerHTML = s;
    }
    [I.p, I.q].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.p.value = v[0]; I.q.value = v[1]; paint(); });
    onLang(paint);
  }

  /* ---------- arrel quadrada d'un monomi (per a reconéixer identitats) ---------- */
  function isqrt(n) { var r = Math.round(Math.sqrt(n)); return r * r === n ? r : -1; }
  function msqrt(t) {
    if (t.c.n <= 0) return null;
    var a = isqrt(t.c.n), b = isqrt(t.c.d); if (a < 0 || b < 0) return null;
    var e = {}; for (var v in t.e) { if (t.e[v] % 2) return null; e[v] = t.e[v] / 2; }
    return mono(rat(a, b), e);
  }
  function mtex(t) { return ttex(t, true); }
  function mtexp(t) { var s = mtex(t); return (t.c.n !== 1 || t.c.d !== 1) && Object.keys(t.e).length || t.c.n < 0 ? "(" + s + ")" : s; }
  /* reconeix a^2+2ab+b^2, a^2-2ab+b^2 o a^2-b^2; retorna text TeX o null */
  function idOf(p) {
    var ts = terms(p);
    if (ts.length === 2) {
      var pos = ts.filter(function (t) { return t.c.n > 0; }), ng = ts.filter(function (t) { return t.c.n < 0; });
      if (pos.length !== 1 || ng.length !== 1) return null;
      var A = msqrt(pos[0]), B = msqrt(mono(rneg(ng[0].c), ng[0].e));
      if (!A || !B) return null;
      return { kind: "dif", A: A, B: B, f: "(" + mtex(A) + "+" + mtex(B) + ")(" + mtex(A) + "-" + mtex(B) + ")" };
    }
    if (ts.length === 3) {
      for (var i = 0; i < 3; i++) for (var j = i + 1; j < 3; j++) {
        var k = 3 - i - j, A2 = msqrt(ts[i]), B2 = msqrt(ts[j]);
        if (!A2 || !B2) continue;
        var dbl = pscale(pmul(pterm(A2.c, A2.e), pterm(B2.c, B2.e)), rat(2)), mid = pterm(ts[k].c, ts[k].e);
        if (peq(dbl, mid)) return { kind: "sq+", A: A2, B: B2, f: "(" + mtex(A2) + "+" + mtex(B2) + ")^{2}" };
        if (peq(pneg(dbl), mid)) return { kind: "sq-", A: A2, B: B2, f: "(" + mtex(A2) + "-" + mtex(B2) + ")^{2}" };
      }
    }
    return null;
  }

  /* ---------- giny: identitats notables ---------- */
  function wId() {
    var w = document.getElementById("w-id"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), kind = "sq+";
    function paint() {
      out.innerHTML = info.innerHTML = "";
      var a = parse(I.a.value), b = parse(I.b.value);
      if (!a || !b || Object.keys(a).length !== 1 || Object.keys(b).length !== 1 || negExp(a) || negExp(b)) { info.innerHTML = warn(T(L3("Escriu dos monomis, per exemple 3x i 2.", "Escribe dos monomios, por ejemplo 3x y 2.", "Type two monomials, for example 3x and 2."))); return; }
      var A = terms(a)[0], B = terms(b)[0], ta = mtex(A), tb = mtex(B), pa = mtexp(A), pb = mtexp(B);
      var A2 = pmul(a, a), B2 = pmul(b, b), AB2 = pscale(pmul(a, b), rat(2)), s = [], ca = "\\color{#ff7a50}", cb = "\\color{#2bb3a3}";
      if (kind === "sq+") {
        s.push(tex("(\\textcolor{#ff7a50}{a}+\\textcolor{#2bb3a3}{b})^2=\\textcolor{#ff7a50}{a}^2+2\\textcolor{#ff7a50}{a}\\textcolor{#2bb3a3}{b}+\\textcolor{#2bb3a3}{b}^2", true));
        s.push(tex("(" + "{" + ca + ta + "}+{" + cb + tb + "})^2={" + ca + pa + "}^2+2\\cdot{" + ca + pa + "}\\cdot{" + cb + pb + "}+{" + cb + pb + "}^2", true));
        s.push(tex("=\\boxed{" + ptex(padd(padd(A2, AB2), B2)) + "}", true));
      } else if (kind === "sq-") {
        s.push(tex("(\\textcolor{#ff7a50}{a}-\\textcolor{#2bb3a3}{b})^2=\\textcolor{#ff7a50}{a}^2-2\\textcolor{#ff7a50}{a}\\textcolor{#2bb3a3}{b}+\\textcolor{#2bb3a3}{b}^2", true));
        s.push(tex("(" + "{" + ca + ta + "}-{" + cb + tb + "})^2={" + ca + pa + "}^2-2\\cdot{" + ca + pa + "}\\cdot{" + cb + pb + "}+{" + cb + pb + "}^2", true));
        s.push(tex("=\\boxed{" + ptex(padd(psub(A2, AB2), B2)) + "}", true));
      } else {
        s.push(tex("(\\textcolor{#ff7a50}{a}+\\textcolor{#2bb3a3}{b})(\\textcolor{#ff7a50}{a}-\\textcolor{#2bb3a3}{b})=\\textcolor{#ff7a50}{a}^2-\\textcolor{#2bb3a3}{b}^2", true));
        s.push(tex("({" + ca + ta + "}+{" + cb + tb + "})({" + ca + ta + "}-{" + cb + tb + "})={" + ca + pa + "}^2-{" + cb + pb + "}^2", true));
        s.push(tex("=\\boxed{" + ptex(psub(A2, B2)) + "}", true));
      }
      out.innerHTML = s.map(function (x) { return '<div class="hrow">' + x + "</div>"; }).join("");
      if (kind !== "dif") info.innerHTML = "⚠ " + T(L3("Error típic: " + tex("(" + ta + (kind === "sq+" ? "+" : "-") + tb + ")^2\\neq " + ptex(padd(A2, B2))) + ". No oblides el doble producte!", "Error típico: " + tex("(" + ta + (kind === "sq+" ? "+" : "-") + tb + ")^2\\neq " + ptex(padd(A2, B2))) + ". ¡No olvides el doble producto!", "Common mistake: " + tex("(" + ta + (kind === "sq+" ? "+" : "-") + tb + ")^2\\neq " + ptex(padd(A2, B2))) + ". Don't forget the middle term!"));
      else info.innerHTML = T(L3("Suma per diferència és igual a <b>diferència de quadrats</b>: els termes del mig s'anul·len.", "Suma por diferencia es igual a <b>diferencia de cuadrados</b>: los términos del medio se anulan.", "Sum times difference equals the <b>difference of two squares</b>: the middle terms cancel."));
    }
    [I.a, I.b].forEach(function (x) { x.addEventListener("input", paint); });
    segBind(w, function (k) { kind = k; paint(); });
    quickBind(w, function (v) { I.a.value = v[0]; I.b.value = v[1]; kind = v[2]; w.querySelectorAll(".seg button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.k === kind)); }); paint(); });
    onLang(paint);
  }

  /* ---------- factor comú ---------- */
  function commonFactor(p) {
    var ts = terms(p); if (!ts.length) return null;
    var g = 0, ints = ts.every(function (t) { return t.c.d === 1; });
    ts.forEach(function (t) { g = gcd(g, t.c.n); });
    if (!ints) g = 1;
    var e = {}, vs = pvars(p);
    vs.forEach(function (v) { var m = Infinity; ts.forEach(function (t) { m = Math.min(m, t.e[v] || 0); }); if (m > 0) e[v] = m; });
    return mono(rat(g || 1), e);
  }
  function wFc() {
    var w = document.getElementById("w-fc"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      out.innerHTML = info.innerHTML = "";
      var p = parse(I.p.value);
      if (!p || negExp(p) || isZero(p)) { info.innerHTML = warn(u("bad")); return; }
      var ts = terms(p);
      if (ts.length < 2) { info.innerHTML = warn(T(L3("Escriu un polinomi amb dos o més termes.", "Escribe un polinomio con dos o más términos.", "Type a polynomial with two or more terms."))); return; }
      var F = commonFactor(p), vs = Object.keys(F.e).sort(), s = [];
      var ints = ts.every(function (t) { return t.c.d === 1; });
      s.push(T(L3("Termes:", "Términos:", "Terms:")) + " " + ts.map(function (t) { return tex(mtex(t)); }).join(", "));
      if (ints) s.push(T(L3("Part numèrica: el MCD dels coeficients és", "Parte numérica: el MCD de los coeficientes es", "Number part: the gcd of the coefficients is")) + " " + tex("\\text{" + T(L3("MCD", "MCD", "gcd")) + "}(" + ts.map(function (t) { return Math.abs(t.c.n); }).join(",") + ")=" + F.c.n) + ".");
      s.push(T(L3("Part literal: agafem les variables que estan en <b>tots</b> els termes, amb el <b>menor</b> exponent:", "Parte literal: tomamos las variables que están en <b>todos</b> los términos, con el <b>menor</b> exponente:", "Variable part: take the variables that appear in <b>every</b> term, with the <b>lowest</b> exponent:")) + " " + (vs.length ? tex(etex(F.e)) : T(L3("cap", "ninguna", "none"))) + ".");
      var Fp = pterm(F.c, F.e), isOne = F.c.n === 1 && F.c.d === 1 && !vs.length;
      if (isOne) { s.push(warn(T(L3("No hi ha cap factor comú (diferent de 1).", "No hay ningún factor común (distinto de 1).", "There's no common factor (other than 1).")))); }
      else {
        var inner = {}; ts.forEach(function (t) { inner = padd(inner, pterm(rdiv(t.c, F.c), emul(t.e, F.e, -1))); });
        s.push(T(L3("Factor comú:", "Factor común:", "Common factor:")) + " " + tex("\\boxed{" + mtex(F) + "}") + ". " + T(L3("Dividim cada terme entre el factor comú:", "Dividimos cada término entre el factor común:", "Divide each term by the common factor:")) + " " + ts.map(function (t) { return tex("\\frac{" + mtex(t) + "}{" + mtex(F) + "}=" + mtex(mono(rdiv(t.c, F.c), emul(t.e, F.e, -1)))); }).join(",\\ "));
        s.push(tex(ptex(p) + "=\\boxed{" + mtex(F) + "\\,(" + ptex(inner) + ")}", true));
        s.push(T(L3("Comprovació: si multipliquem, tornem a obtindre el polinomi inicial.", "Comprobación: si multiplicamos, volvemos a obtener el polinomio inicial.", "Check: multiplying back gives the original polynomial.")));
        p = inner;
      }
      var id = idOf(p);
      if (id) s.push("✨ " + T(L3("A més, ", "Además, ", "What's more, ")) + tex(ptex(p)) + " " + (id.kind === "dif" ? T(L3("és una diferència de quadrats:", "es una diferencia de cuadrados:", "is a difference of two squares:")) : T(L3("és el quadrat d'un binomi:", "es el cuadrado de un binomio:", "is a perfect square:"))) + " " + tex(ptex(p) + "=" + id.f) + (isOne ? "" : ". " + T(L3("Factorització completa:", "Factorización completa:", "Fully factorised:")) + " " + tex("\\boxed{" + mtex(F) + "\\," + id.f + "}")));
      out.innerHTML = s.map(function (x) { return '<div class="hrow">' + x + "</div>"; }).join("");
    }
    I.p.addEventListener("input", paint);
    quickBind(w, function (v) { I.p.value = v[0]; paint(); });
    onLang(paint);
  }

  /* ---------- divisió de polinomis ---------- */
  function divide(A, B) {
    var a = A.a.slice(), b = B.a, n = a.length - 1, m = b.length - 1, q = [], steps = [];
    for (var k = 0; k <= n - m; k++) q.push(rat(0));
    var r = a.slice();
    function deg(x) { for (var i = x.length - 1; i >= 0; i--) if (x[i].n) return i; return -Infinity; }
    while (deg(r) >= m) {
      var d = deg(r), c = rdiv(r[d], b[m]), s = d - m, sub = [];
      q[s] = c;
      for (var i = 0; i < a.length; i++) sub.push(rat(0));
      for (i = 0; i <= m; i++) sub[i + s] = rneg(rmul(c, b[i]));
      var nr = r.map(function (x, i) { return radd(x, sub[i]); });
      steps.push({ c: c, s: s, sub: sub, r: nr, top: d });
      r = nr;
    }
    return { q: q, r: r, steps: steps };
  }
  function cellT(c, k, v, first) { return !c || !c.n ? "" : tex(ttex(mono(c, VE(v, k)), first)); }
  function wDiv() {
    var w = document.getElementById("w-div"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".ldiv-out"), res = w.querySelector(".hsteps"), info = w.querySelector(".info");
    var bn = w.querySelector('[data-a="next"]'), ba = w.querySelector('[data-a="all"]'), cnt = w.querySelector(".step-count"), shown = 0, D = null;
    function compute() {
      D = null; info.innerHTML = "";
      var P = parse(I.p.value), Q = parse(I.q.value);
      if (!P || !Q || negExp(P) || negExp(Q)) { info.innerHTML = warn(u("bad")); return; }
      var vs = pvars(padd(P, Q));
      if (vs.length > 1) { info.innerHTML = warn(T(L3("Els dos polinomis han de tindre la mateixa (i única) variable.", "Los dos polinomios deben tener la misma (y única) variable.", "Both polynomials must use the same single variable."))); return; }
      var v = vs[0] || "x", A = coeffs(P), B = coeffs(Q);
      if (isZero(Q) || pdeg(Q) < 1) { info.innerHTML = warn(T(L3("El divisor ha de tindre grau 1 o més.", "El divisor debe tener grado 1 o más.", "The divisor must have degree 1 or more."))); return; }
      if (pdeg(P) < pdeg(Q)) { info.innerHTML = warn(T(L3("El grau del dividend ha de ser major o igual que el del divisor.", "El grado del dividendo debe ser mayor o igual que el del divisor.", "The dividend's degree must be at least the divisor's."))); return; }
      D = { v: v, A: A.a, B: B.a, P: P, Q: Q, res: divide(A, B) };
      shown = 0;
    }
    function paint() {
      if (!D) { out.innerHTML = res.innerHTML = ""; bn.disabled = ba.disabled = true; cnt.textContent = ""; return; }
      var v = D.v, n = D.A.length - 1, st = D.res.steps, N = st.length, k, html = '<div class="tbl-wrap"><table class="ldiv"><tbody>';
      function row(arr, cls, from, to) {
        var r = '<tr class="' + (cls || "") + '">';
        for (var i = n; i >= 0; i--) r += "<td>" + (i <= from && i >= to ? cellT(arr[i], i, v, !cls && i === n) : "") + "</td>";
        return r;
      }
      /* fila 0: dividend | divisor */
      html += row(D.A, "", n, 0) + '<td class="dv">' + tex(ptex(D.Q)) + "</td></tr>";
      var qcur = []; for (k = 0; k < D.res.q.length; k++) qcur.push(rat(0));
      for (k = 0; k < Math.min(shown, N); k++) qcur[st[k].s] = st[k].c;
      var qtex = shown ? ptex(fromC(qcur, v)) : "";
      for (k = 0; k < Math.min(shown, N); k++) {
        var s = st[k], low = s.s;
        html += row(s.sub, "sub", s.top, low) + (k === 0 ? '<td class="qt">' + tex(qtex) + "</td>" : "<td></td>") + "</tr>";
        html += row(s.r, "rem", s.top - 1, 0) + "<td></td></tr>";
      }
      if (!shown) html += '<tr><td colspan="' + (n + 1) + '"></td><td class="qt">&nbsp;</td></tr>';
      html += "</tbody></table></div>";
      out.innerHTML = html;
      var cur = shown ? st[shown - 1] : null, msg = "";
      if (shown && shown <= N) {
        var lt = mono(shown === 1 ? D.A[cur.top] : st[shown - 2].r[cur.top], VE(v, cur.top));
        var lb = mono(D.B[D.B.length - 1], VE(v, D.B.length - 1));
        var qt = mono(cur.c, VE(v, cur.s));
        msg = fill(T(L3("Pas {k}: dividim el primer terme, {a}, entre el primer terme del divisor, {b}: dona {q}. Multipliquem {q} pel divisor, ho escrivim <b>canviat de signe</b> davall i sumem.", "Paso {k}: dividimos el primer término, {a}, entre el primer término del divisor, {b}: da {q}. Multiplicamos {q} por el divisor, lo escribimos <b>cambiado de signo</b> debajo y sumamos.", "Step {k}: divide the first term, {a}, by the divisor's first term, {b}: that gives {q}. Multiply {q} by the divisor, write it underneath <b>with the signs changed</b> and add.")),
          { k: shown, a: tex(mtex(lt)), b: tex(mtex(lb)), q: tex(mtex(qt)) });
      }
      if (shown >= N) {
        var Qp = fromC(D.res.q, v), Rp = fromC(D.res.r, v);
        msg += (msg ? "<br>" : "") + T(L3("El grau del residu és menor que el del divisor: hem acabat.", "El grado del resto es menor que el del divisor: hemos terminado.", "The remainder's degree is lower than the divisor's: we're done."));
        res.innerHTML = '<div class="hrow">' + T(L3("Quocient", "Cociente", "Quotient")) + " " + tex("C(" + v + ")=\\boxed{" + ptex(Qp) + "}") + " &nbsp; " + T(L3("Residu", "Resto", "Remainder")) + " " + tex("R(" + v + ")=\\boxed{" + ptex(Rp) + "}") + "</div>"
          + '<div class="hrow">' + T(L3("Comprovació (prova de la divisió):", "Comprobación (prueba de la división):", "Check:")) + " " + tex("D=d\\cdot C+R") + ": " + tex("(" + ptex(D.Q) + ")(" + ptex(Qp) + ")" + (isZero(Rp) ? "" : "+" + ptexp(Rp)) + "=" + ptex(padd(pmul(D.Q, Qp), Rp))) + " ✓" + (isZero(Rp) ? " " + T(L3("La divisió és <b>exacta</b>.", "La división es <b>exacta</b>.", "The division is <b>exact</b>.")) : "") + "</div>";
      } else res.innerHTML = "";
      info.innerHTML = msg;
      bn.textContent = u("next") + " →"; bn.disabled = shown >= N;
      ba.textContent = shown >= N ? u("reset") : u("all"); ba.disabled = false;
      cnt.textContent = u("step") + " " + shown + " " + u("of") + " " + N;
    }
    [I.p, I.q].forEach(function (x) { x.addEventListener("input", function () { compute(); paint(); }); });
    bn.addEventListener("click", function () { if (D && shown < D.res.steps.length) { shown++; paint(); } });
    ba.addEventListener("click", function () { if (!D) return; shown = shown >= D.res.steps.length ? 0 : D.res.steps.length; paint(); });
    quickBind(w, function (v) { I.p.value = v[0]; I.q.value = v[1]; compute(); paint(); });
    compute(); onLang(paint);
  }

  /* ---------- regla de Ruffini ---------- */
  function ruffini(a, r) { var n = a.length - 1, b = [], mid = []; var acc = rat(0); for (var k = n; k >= 0; k--) { var m = k === n ? null : rmul(acc, r); var s = m ? radd(a[k], m) : a[k]; mid.push(m); b.push(s); acc = s; } return { mid: mid, b: b }; }
  function wRuf() {
    var w = document.getElementById("w-ruf"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".ruf-out"), res = w.querySelector(".hsteps"), info = w.querySelector(".info");
    var bn = w.querySelector('[data-a="next"]'), ba = w.querySelector('[data-a="all"]'), cnt = w.querySelector(".step-count"), shown = 0, D = null;
    function compute() {
      D = null;
      var P = parse(I.p.value), Q = parse(I.q.value);
      if (!P || !Q || negExp(P) || negExp(Q)) return;
      var vs = pvars(padd(P, Q)); if (vs.length > 1) return;
      var v = vs[0] || "x", A = coeffs(P), B = coeffs(Q);
      if (!B || B.a.length !== 2 || !req(B.a[1], rat(1)) || pdeg(P) < 1) { D = { bad: 1 }; return; }
      var r = rneg(B.a[0]);
      D = { v: v, a: A.a, r: r, P: P, Q: Q, R: ruffini(A.a, r) };
      shown = 0;
    }
    function paint() {
      info.innerHTML = "";
      if (!D || D.bad) { out.innerHTML = res.innerHTML = ""; bn.disabled = ba.disabled = true; cnt.textContent = ""; info.innerHTML = warn(!D ? u("bad") : T(L3("Amb Ruffini només dividim entre binomis de la forma x − a (per exemple x − 3 o x + 2).", "Con Ruffini solo dividimos entre binomios de la forma x − a (por ejemplo x − 3 o x + 2).", "Ruffini's rule only divides by binomials of the form x − a (e.g. x − 3 or x + 2)."))); return; }
      var a = D.a, n = a.length - 1, N = n + 1, R = D.R, k;
      var h = '<div class="tbl-wrap"><table class="ruf"><tbody><tr><td class="ra"></td>';
      for (k = n; k >= 0; k--) h += "<td" + (k === 0 ? ' class="rl"' : "") + ">" + tex(nt(a[k])) + "</td>";
      h += '</tr><tr><td class="ra">' + tex(nt(D.r)) + "</td>";
      for (k = 0; k <= n; k++) h += '<td class="m' + (k === n ? " rl" : "") + '">' + (k > 0 && k < shown ? tex(nt(R.mid[k])) : "") + "</td>";
      h += '</tr><tr class="rb"><td class="ra"></td>';
      for (k = 0; k <= n; k++) h += '<td class="' + (k === n ? "rl rr" : "") + (k === shown - 1 ? " now" : "") + '">' + (k < shown ? tex(nt(R.b[k])) : "") + "</td>";
      h += "</tr></tbody></table></div>";
      out.innerHTML = h;
      var msg = "";
      if (shown === 0) msg = fill(T(L3("Escrivim els coeficients del dividend <b>ordenat i complet</b> (zeros on falten termes) i, a l'esquerra, {a} (el divisor és {d}).", "Escribimos los coeficientes del dividendo <b>ordenado y completo</b> (ceros donde faltan términos) y, a la izquierda, {a} (el divisor es {d}).", "Write the coefficients of the dividend <b>in order and complete</b> (zeros for missing terms) and, on the left, {a} (the divisor is {d}).")), { a: tex("a=" + nt(D.r)), d: tex(ptex(D.Q)) });
      else if (shown === 1) msg = T(L3("Baixem el primer coeficient.", "Bajamos el primer coeficiente.", "Bring down the first coefficient."));
      else msg = fill(T(L3("Multipliquem {b} per {a}: {m}. Ho escrivim davall de {c} i sumem: {s}.", "Multiplicamos {b} por {a}: {m}. Lo escribimos debajo de {c} y sumamos: {s}.", "Multiply {b} by {a}: {m}. Write it under {c} and add: {s}.")),
        { b: tex(nt(R.b[shown - 2])), a: tex(nt(D.r)), m: tex(nt(R.mid[shown - 1])), c: tex(nt(a[n - shown + 1])), s: tex(nt(a[n - shown + 1]) + "+" + ntp(R.mid[shown - 1]) + "=" + nt(R.b[shown - 1])) });
      info.innerHTML = msg;
      if (shown >= N) {
        var q = R.b.slice(0, n).reverse(), Qp = fromC(q, D.v), rem = R.b[n];
        res.innerHTML = '<div class="hrow">' + T(L3("L'últim nombre és el <b>residu</b>; els altres són els coeficients del <b>quocient</b>, que té un grau menys:", "El último número es el <b>resto</b>; los demás son los coeficientes del <b>cociente</b>, que tiene un grado menos:", "The last number is the <b>remainder</b>; the others are the coefficients of the <b>quotient</b>, one degree lower:")) + "</div>"
          + '<div class="hrow">' + tex("C(" + D.v + ")=\\boxed{" + ptex(Qp) + "}\\qquad R=\\boxed{" + nt(rem) + "}", true) + "</div>"
          + '<div class="hrow">' + T(L3("Teorema del residu:", "Teorema del resto:", "Remainder theorem:")) + " " + tex("P(" + nt(D.r) + ")=" + nt(rem)) + ". " + (rem.n ? T(L3("Com que el residu no és 0, " + tex(ptex(D.Q)) + " no és un factor de P.", "Como el resto no es 0, " + tex(ptex(D.Q)) + " no es un factor de P.", "Since the remainder isn't 0, " + tex(ptex(D.Q)) + " isn't a factor of P."))
            : T(L3("La divisió és <b>exacta</b>: ", "La división es <b>exacta</b>: ", "The division is <b>exact</b>: ")) + tex(ptex(D.P) + "=(" + ptex(D.Q) + ")(" + ptex(Qp) + ")") + T(L3(", i " + tex(D.v + "=" + nt(D.r)) + " és una <b>arrel</b> de P.", ", y " + tex(D.v + "=" + nt(D.r)) + " es una <b>raíz</b> de P.", ", and " + tex(D.v + "=" + nt(D.r)) + " is a <b>root</b> of P."))) + "</div>";
      } else res.innerHTML = "";
      bn.textContent = u("next") + " →"; bn.disabled = shown >= N; ba.disabled = false;
      ba.textContent = shown >= N ? u("reset") : u("all");
      cnt.textContent = u("step") + " " + shown + " " + u("of") + " " + N;
    }
    [I.p, I.q].forEach(function (x) { x.addEventListener("input", function () { compute(); paint(); }); });
    bn.addEventListener("click", function () { if (D && !D.bad && shown < D.a.length) { shown++; paint(); } });
    ba.addEventListener("click", function () { if (!D || D.bad) return; shown = shown >= D.a.length ? 0 : D.a.length; paint(); });
    quickBind(w, function (v) { I.p.value = v[0]; I.q.value = v[1]; compute(); paint(); });
    compute(); onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  function rpoly(deg, lo, hi, full) { var a = []; for (var k = 0; k <= deg; k++) a.push(rat(k === deg ? rnz(lo, hi) : (full || Math.random() < .75 ? rint(lo, hi) : 0))); return fromC(a, "x"); }
  function X(k) { return VE("x", k); }
  var LANGQ = [
    [L3("El doble d'un nombre més {a}", "El doble de un número más {a}", "Twice a number plus {a}"), "2x+{a}"],
    [L3("El triple d'un nombre menys {a}", "El triple de un número menos {a}", "Three times a number minus {a}"), "3x-{a}"],
    [L3("La meitat d'un nombre més {a}", "La mitad de un número más {a}", "Half a number plus {a}"), "x/2+{a}"],
    [L3("El quadrat d'un nombre menys {a}", "El cuadrado de un número menos {a}", "The square of a number minus {a}"), "x^2-{a}"],
    [L3("El quadrat de la suma d'un nombre i {a}", "El cuadrado de la suma de un número y {a}", "The square of the sum of a number and {a}"), "(x+{a})^2"],
    [L3("La suma d'un nombre i el seu consecutiu", "La suma de un número y su consecutivo", "The sum of a number and the next number"), "2x+1"],
    [L3("El producte d'un nombre pel seu consecutiu", "El producto de un número por su consecutivo", "A number times the next number"), "x(x+1)"],
    [L3("Un nombre menys la seua tercera part", "Un número menos su tercera parte", "A number minus a third of it"), "x-x/3"],
    [L3("{a} vegades un nombre més el seu quadrat", "{a} veces un número más su cuadrado", "{a} times a number plus its square"), "{a}x+x^2"],
    [L3("El perímetre d'un rectangle de base x i altura {a} unitats més llarga", "El perímetro de un rectángulo de base x y altura {a} unidades más larga", "The perimeter of a rectangle with base x and a height {a} units longer"), "2x+2(x+{a})"],
    [L3("L'àrea d'un quadrat de costat x + {a}", "El área de un cuadrado de lado x + {a}", "The area of a square with side x + {a}"), "(x+{a})^2"],
    [L3("L'edat d'una persona d'ací a {a} anys, si ara en té x", "La edad de una persona dentro de {a} años, si ahora tiene x", "Someone's age in {a} years' time if they are x now"), "x+{a}"],
    [L3("El preu de {a} entrades de x euros amb un descompte de 5 euros en total", "El precio de {a} entradas de x euros con un descuento de 5 euros en total", "The price of {a} tickets at x euros each with a 5-euro discount in total"), "{a}x-5"]
  ];
  var GEN = {
    lang: function () { var t = pick(LANGQ), a = rint(2, 9), e = t[1].replace(/\{a\}/g, a); return { paren: true, ans: parse(e), q: function () { return T(L3("Escriu en llenguatge algebraic (usa x):", "Escribe en lenguaje algebraico (usa x):", "Write in algebra (use x):")) + " <b>" + fill(T(t[0]), { a: a }) + "</b>"; }, s: function () { return tex(texOf(e)) + (e.indexOf("(") >= 0 || /x\/|x-x/.test(e) ? " " + tex("=" + ptex(parse(e))) : ""); } }; },
    val: function () {
      var p = rpoly(rint(2, 3), -5, 5), x = rnz(-3, 3), vals = { x: rat(x) };
      return { num: true, ans: evalAt(p, vals), q: function () { return fill(T(L3("Calcula el valor numèric de $P(x)={p}$ per a $x={x}$:", "Calcula el valor numérico de $P(x)={p}$ para $x={x}$:", "Find the value of $P(x)={p}$ when $x={x}$:")), { p: ptex(p), x: x }); }, s: function () { return tex("P(" + x + ")=" + substTex(p, vals) + "=" + nt(evalAt(p, vals))); } };
    },
    mono: function () {
      var op = pick(["+", "-", "*", ":"]), vs = pick([["x"], ["x"], ["x", "y"], ["a", "b"]]), e1 = {}, e2 = {};
      vs.forEach(function (v) { e1[v] = rint(1, 4); e2[v] = rint(op === ":" ? 0 : 1, op === ":" ? e1[v] : 3); if (!e2[v]) delete e2[v]; });
      if (op === "+" || op === "-") e2 = e1;
      var A = mono(rat(rnz(-9, 9)), e1), B = mono(rat(rnz(-9, 9)), e2);
      if (op === ":") { var k = rnz(-5, 5); B = mono(rat(rnz(-4, 4)), e2); A = mono(rmul(B.c, rat(k)), e1); }
      var a = pterm(A.c, A.e), b = pterm(B.c, B.e), ans = op === "+" ? padd(a, b) : op === "-" ? psub(a, b) : op === "*" ? pmul(a, b) : pterm(rdiv(A.c, B.c), emul(A.e, B.e, -1));
      var qt = "(" + mtex(A) + ")" + (op === "*" ? "\\cdot" : op) + "(" + mtex(B) + ")";
      return { ans: ans, q: function () { return T(L3("Opera:", "Opera:", "Work out:")) + " $" + qt + "$"; }, s: function () { return tex(qt + "=" + ptex(ans)); } };
    },
    addsub: function () {
      var P = rpoly(rint(2, 3), -7, 7), Q = rpoly(rint(1, 3), -7, 7), op = pick(["+", "-"]), ans = op === "+" ? padd(P, Q) : psub(P, Q);
      var qt = "(" + ptex(P) + ")" + op + "(" + ptex(Q) + ")";
      return { ans: ans, paren: false, q: function () { return T(L3("Calcula:", "Calcula:", "Work out:")) + " $" + qt + "$"; }, s: function () { return tex(qt + "=" + ptex(ans)); } };
    },
    mul: function () {
      var t = rint(0, 2), P, Q;
      if (t === 0) { P = pterm(rat(rnz(-5, 5)), X(rint(1, 2))); do { Q = rpoly(rint(2, 3), -5, 5); } while (terms(Q).length < 2); }
      else if (t === 1) { P = fromC([rat(rnz(-5, 5)), rat(rnz(1, 3))], "x"); Q = fromC([rat(rnz(-5, 5)), rat(rnz(-3, 3))], "x"); }
      else { P = fromC([rat(rnz(-4, 4)), rat(rnz(-3, 3))], "x"); Q = rpoly(2, -4, 4, true); }
      var ans = pmul(P, Q), qt = ptexp(P) + "\\cdot(" + ptex(Q) + ")";
      if (t === 0) qt = ptex(P) + "\\cdot(" + ptex(Q) + ")";
      return { ans: ans, q: function () { return T(L3("Multiplica:", "Multiplica:", "Multiply:")) + " $" + qt + "$"; }, s: function () { return tex(qt + "=" + ptex(ans)); } };
    },
    id: function () {
      var k = pick(["sq+", "sq-", "dif"]), A = mono(rat(rint(1, 5)), X(rint(1, 2))), B = mono(rat(rint(1, 7)), {});
      if (Math.random() < .25) { A = mono(rat(rint(1, 3)), X(1)); B = mono(rat(rint(1, 3)), { y: 1 }); }
      var a = pterm(A.c, A.e), b = pterm(B.c, B.e), ans, qt;
      if (k === "sq+") { ans = ppow(padd(a, b), 2); qt = "(" + mtex(A) + "+" + mtex(B) + ")^2"; }
      else if (k === "sq-") { ans = ppow(psub(a, b), 2); qt = "(" + mtex(A) + "-" + mtex(B) + ")^2"; }
      else { ans = psub(pmul(a, a), pmul(b, b)); qt = "(" + mtex(A) + "+" + mtex(B) + ")(" + mtex(A) + "-" + mtex(B) + ")"; }
      return { ans: ans, q: function () { return T(L3("Desenvolupa amb les identitats notables:", "Desarrolla con las identidades notables:", "Expand using the special products:")) + " $" + qt + "$"; }, s: function () { return tex(qt + "=" + ptex(ans)); } };
    },
    fc: function () {
      var F = mono(rat(rint(1, 6)), pick([X(1), X(2), {}, X(1), { x: 1, y: 1 }])), G;
      do { G = rpoly(rint(1, 3), -6, 6); } while (terms(G).length < 2 || !(commonFactor(G).c.n === 1 && !Object.keys(commonFactor(G).e).length));
      if (F.c.n === 1 && !Object.keys(F.e).length) F = mono(rat(rint(2, 6)), X(1));
      var P = pmul(pterm(F.c, F.e), G), ans = pterm(F.c, F.e);
      return { ans: ans, sign: true, q: function () { return fill(T(L3("Quin és el factor comú (màxim) de $P={p}$? Escriu només el factor.", "¿Cuál es el factor común (máximo) de $P={p}$? Escribe solo el factor.", "What is the (greatest) common factor of $P={p}$? Type just the factor.")), { p: ptex(P) }); }, s: function () { return tex(ptex(P) + "=" + mtex(F) + "\\,(" + ptex(G) + ")"); } };
    },
    ruf: function () {
      var a = rnz(-3, 3), P = rpoly(3, -5, 5), vals = { x: rat(a) }, rem = evalAt(P, vals), d = a < 0 ? "x+" + (-a) : "x-" + a;
      return { num: true, ans: rem, q: function () { return fill(T(L3("Quin és el residu de dividir $P(x)={p}$ entre ${d}$?", "¿Cuál es el resto de dividir $P(x)={p}$ entre ${d}$?", "What is the remainder when $P(x)={p}$ is divided by ${d}$?")), { p: ptex(P), d: d }); }, s: function () { var R = ruffini(coeffs(P).a, rat(a)); return "Ruffini: " + tex(R.b.map(nt).join("\\quad")) + " → " + tex("R=" + nt(rem)) + ". " + T(L3("També", "También", "Also")) + " " + tex("P(" + a + ")=" + nt(rem)) + "."; } };
    }
  };
  /* expressió escrita per l'alumne → TeX (sense simplificar) */
  function texOf(e) { return e.replace(/\*/g, "\\cdot ").replace(/x\/(\d)/g, "\\frac{x}{$1}").replace(/\^(\d)/g, "^{$1}"); }
  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, res = 0, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore");
    function paint() {
      dq.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (done) info.innerHTML = (res ? '<span class="ok">✓ ' + u("right") + "</span>" : '<span class="ko">✗ ' + u("wrong") + "</span>") + '<div class="dsol">' + u("sol") + " " + q.s() + "</div>";
    }
    function check() {
      if (done) return;
      var raw = inp.value.trim(), p = parse(raw), good;
      if (!raw || !p) { info.innerHTML = warn(q.num ? u("num") : u("write")); return; }
      if (q.num) { if (!isConst(p)) { info.innerHTML = warn(u("num")); return; } good = req(cval(p), q.ans); }
      else {
        if (!q.paren && /[()\[\]]/.test(raw)) { info.innerHTML = warn(u("noParen")); return; }
        good = peq(p, q.ans) || (q.sign && peq(p, pneg(q.ans)));
      }
      done = true; tot++; res = good; if (good) ok++;
      paint();
    }
    function fresh() { q = GEN[kind](); done = false; inp.value = ""; info.innerHTML = ""; paint(); }
    w.querySelector('[data-a="check"]').addEventListener("click", check);
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); inp.focus(); });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    onLang(paint);
  }
  window.FM34 = { parse: parse, ptex: ptex, peq: peq, divide: divide, coeffs: coeffs, ruffini: ruffini, idOf: idOf, commonFactor: commonFactor, GEN: GEN, terms: terms };

  /* ---------- qüestionari ---------- */
  var QUIZ = [
    { q: { va: "«El triple d'un nombre menys 4» s'escriu…", es: "«El triple de un número menos 4» se escribe…", en: "“Three times a number minus 4” is written…" },
      o: [{ va: "$3(x-4)$" }, { va: "$3x-4$" }, { va: "$x^3-4$" }, { va: "$4-3x$" }], a: 1,
      e: { va: "Primer multipliquem el nombre per 3 i després restem 4: $3x-4$. En canvi, $3(x-4)$ seria «el triple de la diferència».", es: "Primero multiplicamos el número por 3 y después restamos 4: $3x-4$. En cambio, $3(x-4)$ sería «el triple de la diferencia».", en: "First multiply the number by 3, then subtract 4: $3x-4$. $3(x-4)$ would be “three times the difference”." } },
    { q: { va: "Quin és el grau del monomi $-7x^3y^2$?", es: "¿Cuál es el grado del monomio $-7x^3y^2$?", en: "What is the degree of the monomial $-7x^3y^2$?" },
      o: [{ va: "$3$" }, { va: "$5$" }, { va: "$-7$" }, { va: "$6$" }], a: 1,
      e: { va: "El grau és la suma dels exponents de la part literal: $3+2=5$. El coeficient ($-7$) no hi compta.", es: "El grado es la suma de los exponentes de la parte literal: $3+2=5$. El coeficiente ($-7$) no cuenta.", en: "The degree is the sum of the exponents: $3+2=5$. The coefficient ($-7$) doesn't count." } },
    { q: { va: "Quin d'aquests monomis és semblant a $4ab^2$?", es: "¿Cuál de estos monomios es semejante a $4ab^2$?", en: "Which of these is a like term of $4ab^2$?" },
      o: [{ va: "$4a^2b$" }, { va: "$-ab^2$" }, { va: "$4ab$" }, { va: "$4b^2$" }], a: 1,
      e: { va: "Són semblants si tenen <b>la mateixa part literal</b> ($ab^2$); el coeficient pot ser diferent.", es: "Son semejantes si tienen <b>la misma parte literal</b> ($ab^2$); el coeficiente puede ser distinto.", en: "Like terms have <b>the same variable part</b> ($ab^2$); the coefficient can differ." } },
    { q: { va: "$5x^2+3x^2=$", es: "$5x^2+3x^2=$", en: "$5x^2+3x^2=$" },
      o: [{ va: "$8x^4$" }, { va: "$15x^2$" }, { va: "$8x^2$" }, { va: "$8x$" }], a: 2,
      e: { va: "Sumem els coeficients i deixem la mateixa part literal: $(5+3)x^2=8x^2$. Els exponents <b>no</b> se sumen!", es: "Sumamos los coeficientes y dejamos la misma parte literal: $(5+3)x^2=8x^2$. ¡Los exponentes <b>no</b> se suman!", en: "Add the coefficients and keep the variable part: $(5+3)x^2=8x^2$. The exponents are <b>not</b> added!" } },
    { q: { va: "$(-3x^2y)\\cdot(4xy^3)=$", es: "$(-3x^2y)\\cdot(4xy^3)=$", en: "$(-3x^2y)\\cdot(4xy^3)=$" },
      o: [{ va: "$-12x^3y^4$" }, { va: "$x^3y^4$" }, { va: "$-12x^2y^3$" }, { va: "$12x^3y^4$" }], a: 0,
      e: { va: "$(-3)\\cdot4=-12$ i sumem exponents: $x^{2+1}y^{1+3}=x^3y^4$.", es: "$(-3)\\cdot4=-12$ y sumamos exponentes: $x^{2+1}y^{1+3}=x^3y^4$.", en: "$(-3)\\cdot4=-12$ and add exponents: $x^{2+1}y^{1+3}=x^3y^4$." } },
    { q: { va: "$12x^5:(-4x^2)=$", es: "$12x^5:(-4x^2)=$", en: "$12x^5:(-4x^2)=$" },
      o: [{ va: "$-3x^7$" }, { va: "$3x^3$" }, { va: "$-3x^3$" }, { va: "$-8x^3$" }], a: 2,
      e: { va: "$12:(-4)=-3$ i restem exponents: $x^{5-2}=x^3$.", es: "$12:(-4)=-3$ y restamos exponentes: $x^{5-2}=x^3$.", en: "$12:(-4)=-3$ and subtract exponents: $x^{5-2}=x^3$." } },
    { q: { va: "Quin és el grau i el terme independent de $P(x)=2x^3-x^5+7$?", es: "¿Cuál es el grado y el término independiente de $P(x)=2x^3-x^5+7$?", en: "What are the degree and the constant term of $P(x)=2x^3-x^5+7$?" },
      o: [{ va: "Grau 3, t. i. 7", es: "Grado 3, t. i. 7", en: "Degree 3, constant 7" }, { va: "Grau 5, t. i. 7", es: "Grado 5, t. i. 7", en: "Degree 5, constant 7" }, { va: "Grau 5, t. i. 2", es: "Grado 5, t. i. 2", en: "Degree 5, constant 2" }, { va: "Grau 8, t. i. 7", es: "Grado 8, t. i. 7", en: "Degree 8, constant 7" }], a: 1,
      e: { va: "Ordenat: $-x^5+2x^3+7$. El grau és el del terme de grau més alt (5), encara que no siga el primer escrit.", es: "Ordenado: $-x^5+2x^3+7$. El grado es el del término de mayor grado (5), aunque no sea el primero escrito.", en: "In order: $-x^5+2x^3+7$. The degree is the highest one (5), even if that term isn't written first." } },
    { q: { va: "Si $P(x)=x^2-3x+1$, quant val $P(-2)$?", es: "Si $P(x)=x^2-3x+1$, ¿cuánto vale $P(-2)$?", en: "If $P(x)=x^2-3x+1$, what is $P(-2)$?" },
      o: [{ va: "$-1$" }, { va: "$11$" }, { va: "$3$" }, { va: "$-9$" }], a: 1,
      e: { va: "$(-2)^2-3\\cdot(-2)+1=4+6+1=11$. Posa sempre els negatius entre parèntesis.", es: "$(-2)^2-3\\cdot(-2)+1=4+6+1=11$. Pon siempre los negativos entre paréntesis.", en: "$(-2)^2-3\\cdot(-2)+1=4+6+1=11$. Always put negatives in brackets." } },
    { q: { va: "$(3x^2-x+5)-(x^2-4x+2)=$", es: "$(3x^2-x+5)-(x^2-4x+2)=$", en: "$(3x^2-x+5)-(x^2-4x+2)=$" },
      o: [{ va: "$2x^2-5x+3$" }, { va: "$2x^2+3x+3$" }, { va: "$2x^2-5x+7$" }, { va: "$4x^2-5x+7$" }], a: 1,
      e: { va: "Canviem el signe de tots els termes del segon: $3x^2-x+5-x^2+4x-2=2x^2+3x+3$.", es: "Cambiamos el signo de todos los términos del segundo: $3x^2-x+5-x^2+4x-2=2x^2+3x+3$.", en: "Change the sign of every term of the second: $3x^2-x+5-x^2+4x-2=2x^2+3x+3$." } },
    { q: { va: "$(x+2)(x-5)=$", es: "$(x+2)(x-5)=$", en: "$(x+2)(x-5)=$" },
      o: [{ va: "$x^2-10$" }, { va: "$x^2-3x-10$" }, { va: "$x^2+3x-10$" }, { va: "$x^2-7x-10$" }], a: 1,
      e: { va: "$x^2-5x+2x-10=x^2-3x-10$.", es: "$x^2-5x+2x-10=x^2-3x-10$.", en: "$x^2-5x+2x-10=x^2-3x-10$." } },
    { q: { va: "$(x+3)^2=$", es: "$(x+3)^2=$", en: "$(x+3)^2=$" },
      o: [{ va: "$x^2+9$" }, { va: "$x^2+6x+9$" }, { va: "$x^2+3x+9$" }, { va: "$2x+6$" }], a: 1,
      e: { va: "Quadrat del primer, més el doble del primer pel segon, més el quadrat del segon: $x^2+2\\cdot x\\cdot3+9$.", es: "Cuadrado del primero, más el doble del primero por el segundo, más el cuadrado del segundo: $x^2+2\\cdot x\\cdot3+9$.", en: "First squared, plus twice first times second, plus second squared: $x^2+2\\cdot x\\cdot3+9$." } },
    { q: { va: "$(2x-1)^2=$", es: "$(2x-1)^2=$", en: "$(2x-1)^2=$" },
      o: [{ va: "$4x^2-1$" }, { va: "$4x^2-4x+1$" }, { va: "$2x^2-4x+1$" }, { va: "$4x^2-2x+1$" }], a: 1,
      e: { va: "$(2x)^2-2\\cdot2x\\cdot1+1^2=4x^2-4x+1$. Compte: $(2x)^2=4x^2$, no $2x^2$.", es: "$(2x)^2-2\\cdot2x\\cdot1+1^2=4x^2-4x+1$. Ojo: $(2x)^2=4x^2$, no $2x^2$.", en: "$(2x)^2-2\\cdot2x\\cdot1+1^2=4x^2-4x+1$. Careful: $(2x)^2=4x^2$, not $2x^2$." } },
    { q: { va: "$x^2-49$ és igual a…", es: "$x^2-49$ es igual a…", en: "$x^2-49$ equals…" },
      o: [{ va: "$(x-7)^2$" }, { va: "$(x+7)(x-7)$" }, { va: "$(x-49)(x+1)$" }, { va: "$(x+7)^2$" }], a: 1,
      e: { va: "És una diferència de quadrats: $a^2-b^2=(a+b)(a-b)$ amb $a=x$, $b=7$.", es: "Es una diferencia de cuadrados: $a^2-b^2=(a+b)(a-b)$ con $a=x$, $b=7$.", en: "It's a difference of two squares: $a^2-b^2=(a+b)(a-b)$ with $a=x$, $b=7$." } },
    { q: { va: "Traient factor comú, $6x^3-9x^2=$", es: "Sacando factor común, $6x^3-9x^2=$", en: "Taking out the common factor, $6x^3-9x^2=$" },
      o: [{ va: "$3x(2x^2-3x)$" }, { va: "$3x^2(2x-3)$" }, { va: "$x^2(6x-9)$" }, { va: "$3x^2(2x-9)$" }], a: 1,
      e: { va: "MCD$(6,9)=3$ i la $x$ amb el menor exponent, $x^2$. Les altres opcions o no són el factor comú <b>màxim</b> o són incorrectes.", es: "MCD$(6,9)=3$ y la $x$ con el menor exponente, $x^2$. Las otras opciones o no son el factor común <b>máximo</b> o son incorrectas.", en: "gcd$(6,9)=3$ and $x$ with the lowest exponent, $x^2$. The other options either aren't the <b>greatest</b> common factor or are wrong." } },
    { q: { va: "En una divisió de polinomis, el residu ha de tindre…", es: "En una división de polinomios, el resto debe tener…", en: "In polynomial division, the remainder must have…" },
      o: [{ va: "el mateix grau que el divisor", es: "el mismo grado que el divisor", en: "the same degree as the divisor" }, { va: "grau menor que el divisor", es: "grado menor que el divisor", en: "a lower degree than the divisor" }, { va: "grau 0 sempre", es: "grado 0 siempre", en: "degree 0, always" }, { va: "grau major que el quocient", es: "grado mayor que el cociente", en: "a higher degree than the quotient" }], a: 1,
      e: { va: "Seguim dividint mentre es puga: parem quan el grau del residu és menor que el del divisor. I es compleix $D=d\\cdot C+R$.", es: "Seguimos dividiendo mientras se pueda: paramos cuando el grado del resto es menor que el del divisor. Y se cumple $D=d\\cdot C+R$.", en: "Keep dividing while possible: stop when the remainder's degree is lower than the divisor's. And $D=d\\cdot C+R$." } },
    { q: { va: "Per a dividir $x^3-2x+5$ entre $x-3$ amb Ruffini, quins coeficients escrivim?", es: "Para dividir $x^3-2x+5$ entre $x-3$ con Ruffini, ¿qué coeficientes escribimos?", en: "To divide $x^3-2x+5$ by $x-3$ with Ruffini, which coefficients do we write?" },
      o: [{ va: "$1\\quad -2\\quad 5$ i a l'esquerra $-3$", es: "$1\\quad -2\\quad 5$ y a la izquierda $-3$", en: "$1\\quad -2\\quad 5$ and $-3$ on the left" }, { va: "$1\\quad 0\\quad -2\\quad 5$ i a l'esquerra $3$", es: "$1\\quad 0\\quad -2\\quad 5$ y a la izquierda $3$", en: "$1\\quad 0\\quad -2\\quad 5$ and $3$ on the left" }, { va: "$1\\quad 0\\quad -2\\quad 5$ i a l'esquerra $-3$", es: "$1\\quad 0\\quad -2\\quad 5$ y a la izquierda $-3$", en: "$1\\quad 0\\quad -2\\quad 5$ and $-3$ on the left" }], a: 1,
      e: { va: "El polinomi ha d'estar <b>complet</b> (falta $x^2$: hi posem 0) i, si el divisor és $x-a$, a l'esquerra va $a=3$.", es: "El polinomio debe estar <b>completo</b> (falta $x^2$: ponemos 0) y, si el divisor es $x-a$, a la izquierda va $a=3$.", en: "The polynomial must be <b>complete</b> (no $x^2$: write 0) and, if the divisor is $x-a$, $a=3$ goes on the left." } },
    { q: { va: "Amb Ruffini obtenim la fila $2\\quad 1\\quad -3\\quad \\big|\\ 4$. Quin és el quocient i el residu?", es: "Con Ruffini obtenemos la fila $2\\quad 1\\quad -3\\quad \\big|\\ 4$. ¿Cuál es el cociente y el resto?", en: "Ruffini gives the bottom row $2\\quad 1\\quad -3\\quad \\big|\\ 4$. What are the quotient and remainder?" },
      o: [{ va: "$C=2x^3+x^2-3x$, $R=4$" }, { va: "$C=2x^2+x-3$, $R=4$" }, { va: "$C=2x^2+x-3+4$, $R=0$" }, { va: "$C=x^2-3x+4$, $R=2$" }], a: 1,
      e: { va: "L'últim nombre és el residu i la resta són els coeficients del quocient, que té <b>un grau menys</b> que el dividend.", es: "El último número es el resto y los demás son los coeficientes del cociente, que tiene <b>un grado menos</b> que el dividendo.", en: "The last number is the remainder; the rest are the coefficients of the quotient, which is <b>one degree lower</b> than the dividend." } }
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

  var TITLES = { va: "Polinomis · FentMates", es: "Polinomios · FentMates", en: "Polynomials · FentMates" };
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
    wMono(); wMonOps(); wVal(); wPoly(); wAddSub(); wMul(); wId(); wFc(); wDiv(); wRuf();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
