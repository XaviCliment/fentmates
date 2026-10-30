(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-3eso-u6-done", NSEC = 9;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc",
      bad: "No entenc alguna equació. Cada una ha de tindre un signe = i ser de primer grau en x i y: exemple 2x+3y=7.",
      bad1: "No entenc l'equació. Ha de tindre un signe = i ser de primer grau en x i y: exemple 2x+3y=7.",
      pair: "Escriu la solució com x = 3, y = −2 (o bé 3; −2).", num: "Escriu un nombre.", sol: "Solució:" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro",
      bad: "No entiendo alguna ecuación. Cada una debe tener un signo = y ser de primer grado en x e y: ejemplo 2x+3y=7.",
      bad1: "No entiendo la ecuación. Debe tener un signo = y ser de primer grado en x e y: ejemplo 2x+3y=7.",
      pair: "Escribe la solución como x = 3, y = −2 (o bien 3; −2).", num: "Escribe un número.", sol: "Solución:" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Score", right: "Correct!", wrong: "Not correct.", theme: "Switch between light and dark mode",
      bad: "I can't read one of the equations. Each needs an = sign and must be first degree in x and y: e.g. 2x+3y=7.",
      bad1: "I can't read that equation. It needs an = sign and must be first degree in x and y: e.g. 2x+3y=7.",
      pair: "Type the solution as x = 3, y = −2 (or 3; −2).", num: "Type a number.", sol: "Solution:" }
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


  function isqrt(n) { var r = Math.round(Math.sqrt(n)); return r * r === n ? r : -1; }
  function lcm(a, b) { return a / gcd(a, b) * b; }
  function mod(a, n) { return ((a % n) + n) % n; }
  function rows2html(rows) { return rows.map(function (x) { return '<div class="hrow">' + x + "</div>"; }).join(""); }
  function dec(x) { return (Math.round(x * 100) / 100).toFixed(2).replace(".", "\\dc "); }

  /* ---------- equacions: lectura del text ---------- */
  function clean(s) { return s.replace(/[−–]/g, "-").replace(/[·×]/g, "*").replace(/\s+/g, "").replace(/\^\{(\d+)\}/g, "^$1"); }
  var OPEN = "([{", CLOSE = ")]}";
  /* termes del nivell superior: "(x+1)/2-(x-2)/3" -> [{sg:"+",t:"(x+1)/2"}, {sg:"-",t:"(x-2)/3"}] */
  function topTerms(s) {
    var out = [], d = 0, cur = "", sg = "+";
    for (var i = 0; i < s.length; i++) {
      var c = s[i];
      if (OPEN.indexOf(c) >= 0) d++; else if (CLOSE.indexOf(c) >= 0) d--;
      if ((c === "+" || c === "-") && d === 0 && !(i > 0 && /[\^*\/:]/.test(s[i - 1]))) {
        if (cur) out.push({ sg: sg, t: cur }); else if (i > 0) return null;
        sg = c; cur = "";
      } else cur += c;
    }
    if (cur) out.push({ sg: sg, t: cur });
    return out;
  }
  function hasTop(s) { var t = topTerms(s); return !t || t.length > 1 || (t[0] && t[0].sg === "-"); }
  function lastSlash(t) { var d = 0; for (var i = t.length - 1; i >= 0; i--) { var c = t[i]; if (CLOSE.indexOf(c) >= 0) d++; else if (OPEN.indexOf(c) >= 0) d--; else if ((c === "/" || c === ":") && d === 0) return i; } return -1; }
  function wrapped(s) { if (OPEN.indexOf(s[0]) < 0) return false; var d = 0; for (var i = 0; i < s.length; i++) { if (OPEN.indexOf(s[i]) >= 0) d++; else if (CLOSE.indexOf(s[i]) >= 0) d--; if (d === 0 && i < s.length - 1) return false; } return true; }
  function tTex(s) { return s.replace(/\[/g, "(").replace(/\]/g, ")").replace(/\*/g, "\\cdot ").replace(/\^(\d+)/g, "^{$1}").replace(/(\d)[.,](\d)/g, "$1\\dc $2"); }
  /* fracció i numerador d'un terme: "(x+1)/2" -> {num:"(x+1)", den:2} */
  function fracOf(t) { var i = lastSlash(t); if (i < 0) return { num: t, den: 1 }; var d = t.slice(i + 1); return /^\d+$/.test(d) ? { num: t.slice(0, i), den: parseInt(d, 10) } : null; }
  function joinT(parts) { return parts.map(function (p, i) { return (p.sg === "-" ? "-" : i ? "+" : "") + p.x; }).join(""); }
  /* expressió escrita -> TeX amb fraccions */
  function texRaw(s) {
    var ts = topTerms(s); if (!ts) return tTex(s);
    return joinT(ts.map(function (p) {
      var f = fracOf(p.t), x;
      if (f && f.den > 1) x = "\\frac{" + tTex(wrapped(f.num) ? f.num.slice(1, -1) : f.num) + "}{" + f.den + "}";
      else x = tTex(p.t);
      return { sg: p.sg, x: x };
    }));
  }
  /* cada terme multiplicat pel m.c.m.: "(x+1)/2-(x-2)/3", 6 -> "3(x+1)-2(x-2)" */
  function mulSide(s, m) {
    var ts = topTerms(s); if (!ts) return null;
    var parts = [];
    for (var i = 0; i < ts.length; i++) {
      var f = fracOf(ts[i].t); if (!f || m % f.den) return null;
      var k = m / f.den, num = f.num, x;
      if (/^\d+([.,]\d+)?$/.test(num)) { var p = parse(num); if (!p) return null; x = nt(rmul(cval(p), rat(k))); }
      else {
        var body = hasTop(num) && !wrapped(num) ? "(" + num + ")" : num;
        x = k === 1 ? tTex(body) : (/^\d/.test(body) ? k + "\\cdot " : k) + tTex(body);
      }
      parts.push({ sg: ts[i].sg, x: x });
    }
    return joinT(parts);
  }
  /* substitució en l'expressió escrita: "3x+1", x=-2 -> "3·(-2)+1" */
  function substRaw(s, v, r) {
    var V = r.n < 0 || r.d !== 1 ? "(" + nt(r) + ")" : nt(r);
    var out = "";
    for (var i = 0; i < s.length; i++) {
      if (s[i].toLowerCase() === v) { out += (i > 0 && /[\d)\]}a-z]/i.test(s[i - 1]) ? "\\cdot " : "") + V + (i + 1 < s.length && /[\d(a-z]/i.test(s[i + 1]) ? "\\cdot " : ""); }
      else out += s[i];
    }
    return texRaw(out);
  }
  function cof(p, v, k) { var key = mkey(VE(v, k)); return p[key] ? p[key].c : rat(0); }

  /* ---------- sistemes: lectura i forma reduïda ax + by = c ---------- */
  function readLin(raw) {
    var s = clean(raw), k = s.split("=");
    if (k.length !== 2 || !k[0] || !k[1]) return null;
    var Lp = parse(k[0]), Rp = parse(k[1]);
    if (!Lp || !Rp || negExp(Lp) || negExp(Rp)) return null;
    var P = psub(Lp, Rp), vs = pvars(P);
    if (!vs.length || pdeg(P) > 1 || vs.some(function (v) { return v !== "x" && v !== "y"; })) return null;
    var m = /^([xy])$/.exec(k[0]);
    return { ls: k[0], rs: k[1], L: Lp, R: Rp, iso: m && !/[xy]/.test(k[1].replace(m[1] === "x" ? /y/g : /x/g, "")) ? m[1] : null };
  }
  function other(v) { return v === "x" ? "y" : "x"; }
  function co(e, v) { return v === "x" ? e.a : e.b; }
  function lp(a, b) { return padd(pterm(a, VE("x", 1)), pterm(b, VE("y", 1))); }
  function ltex(e) { return ptex(lp(e.a, e.b)) + "=" + nt(e.c); }
  function rawTex(E) { return texRaw(E.ls) + "=" + texRaw(E.rs); }
  function sysTex(a, b) { return "\\begin{cases}" + a + "\\\\[2pt]" + b + "\\end{cases}"; }
  function sc(e, r) { return { a: rmul(e.a, r), b: rmul(e.b, r), c: rmul(e.c, r) }; }
  function ordn(i) { return T([L3("primera", "primera", "first"), L3("segona", "segunda", "second")][i]); }
  function arrow(s) { return '<span class="arr">→</span> ' + s; }
  /* forma reduïda d'una equació (amb els passos, si cal) */
  function prep2(E, rows, i, quiet) {
    var both = E.ls + "=" + E.rs, re = /\/(\d+)/g, mm, m = 1, Lp = E.L, Rp = E.R, last = rawTex(E), r = [];
    while ((mm = re.exec(both))) m = lcm(m, parseInt(mm[1], 10));
    if (m > 1) {
      Lp = pscale(Lp, rat(m)); Rp = pscale(Rp, rat(m));
      var ml = mulSide(E.ls, m), mr = mulSide(E.rs, m);
      last = ml && mr ? ml + "=" + mr : ptex(Lp) + "=" + ptex(Rp);
      r.push(fill(T(L3("Traiem denominadors: multipliquem tots els termes pel m.c.m., {m}:", "Quitamos denominadores: multiplicamos todos los términos por el m.c.m., {m}:", "Clear denominators: multiply every term by the LCM, {m}:")), { m: m }) + " " + tex(last));
      if (/[(]/.test(last)) { last = ptex(Lp) + "=" + ptex(Rp); r.push(T(L3("Traiem parèntesis:", "Quitamos paréntesis:", "Remove brackets:")) + " " + tex(last)); }
    } else if (/[()\[\]{}]/.test(both)) { last = ptex(Lp) + "=" + ptex(Rp); r.push(T(L3("Traiem parèntesis:", "Quitamos paréntesis:", "Remove brackets:")) + " " + tex(last)); }
    var P = psub(Lp, Rp), e = { a: cof(P, "x", 1), b: cof(P, "y", 1), c: rneg(cval(P)) };
    if (ltex(e) !== last && !(quiet && E.iso && !r.length)) r.push(T(L3("Passem les incògnites al primer membre i els nombres al segon, i reduïm:", "Pasamos las incógnitas al primer miembro y los números al segundo, y reducimos:", "Move the unknowns to the left and the numbers to the right, and simplify:")) + " " + tex(ltex(e)));
    var d = lcm(lcm(e.a.d, e.b.d), e.c.d);
    if (d > 1) { e = sc(e, rat(d)); r.push(fill(T(L3("Multipliquem per {d} per a tindre coeficients enters:", "Multiplicamos por {d} para tener coeficientes enteros:", "Multiply by {d} to get whole-number coefficients:")), { d: d }) + " " + tex(ltex(e))); }
    var g = gcd(gcd(e.a.n, e.b.n), e.c.n);
    if (g > 1) { e = sc(e, rat(1, g)); r.push(fill(T(L3("Simplifiquem: dividim entre {g}:", "Simplificamos: dividimos entre {g}:", "Simplify: divide by {g}:")), { g: g }) + " " + tex(ltex(e))); }
    if (r.length) { rows.push("<b>" + fill(T(L3("Arreglem la {n} equació", "Arreglamos la {n} ecuación", "Tidy up the {n} equation")), { n: ordn(i) }) + "</b> " + tex(rawTex(E))); r.forEach(function (x) { rows.push(arrow(x)); }); }
    return e;
  }

  /* ---------- expressions aïllades: v = (N0 + N1·w) / den ---------- */
  function iso(e, v) {
    var k = co(e, v), h = co(e, other(v)), N0 = e.c, N1 = rneg(h), den = k;
    if (den.n < 0) { N0 = rneg(N0); N1 = rneg(N1); den = rneg(den); }
    var g = gcd(gcd(N0.n, N1.n), den.n) || 1;
    return { v: v, w: other(v), k: k, h: h, N0: rat(N0.n / g), N1: rat(N1.n / g), den: den.n / g };
  }
  function wt(c, w, first) { return ttex(mono(c, VE(w, 1)), first); }
  /* numerador: primer el terme positiu (7 − 2x, 2x − 1) */
  function numTex(N0, N1, w) {
    if (!N1.n) return nt(N0);
    if (!N0.n) return wt(N1, w, true);
    return N1.n > 0 ? wt(N1, w, true) + ttex(mono(N0, {}), false) : nt(N0) + wt(N1, w, false);
  }
  function numTerms(N0, N1, w, k) {
    var a = mono(rmul(N0, k), {}), b = mono(rmul(N1, k), VE(w, 1)), out = N1.n > 0 ? [b, a] : [a, b];
    return out.filter(function (t) { return t && t.c.n; });
  }
  function isoTex(I) { var n = numTex(I.N0, I.N1, I.w); return I.den === 1 ? n : "\\frac{" + n + "}{" + I.den + "}"; }
  function isoVal(I, val) { return rdiv(radd(I.N0, rmul(I.N1, val)), rat(I.den)); }
  /* com hem aïllat: 2y = 7 − 3x ⇒ y = (7 − 3x)/2 */
  function isoShow(e, I) {
    var s = "";
    if (!(I.k.n === 1 && I.k.d === 1)) s = wt(I.k, I.v, true) + "=" + numTex(e.c, rneg(I.h), I.w) + "\\ \\Rightarrow\\ ";
    return s + I.v + "=" + isoTex(I);
  }
  /* k·(expressió), amb el signe */
  function kTimes(k, body, first) {
    var a = Math.abs(k.n) === 1 && k.d === 1 ? "" : nt({ n: Math.abs(k.n), d: k.d }) + (/^\\frac/.test(body) ? "\\cdot " : "");
    return (k.n < 0 ? "-" : first ? "" : "+") + a + body;
  }
  /* k·valor: 3·(−2) */
  function kVal(k, val, first) {
    var a = Math.abs(k.n) === 1 && k.d === 1 ? ntp(val) : nt({ n: Math.abs(k.n), d: k.d }) + "\\cdot " + ntp(val);
    return (k.n < 0 ? "-" : first ? "" : "+") + a;
  }
  function joinTerms(ts) { return ts.length ? ts.map(function (t, i) { return ttex(t, i === 0); }).join("") : "0"; }
  /* A·w = B ⇒ w = B/A */
  function isolateTex(A, B, w) {
    if (A.n === 1 && A.d === 1) return "";
    var s = rdiv(B, A);
    return "\\ \\Rightarrow\\ " + w + "=\\frac{" + nt(B) + "}{" + nt(A) + "}" + (A.n > 0 && A.d === 1 && B.d === 1 && gcd(B.n, A.n) === 1 ? "" : "=" + nt(s));
  }
  function sol(o) { return "x=" + nt(o.x) + ",\\ \\ y=" + nt(o.y); }

  /* ---------- casos especials: 0·w = B ---------- */
  function special(B, e1, rows) {
    if (B.n) {
      rows.push('<span class="ko">' + fill(T(L3("Cap valor multiplicat per 0 dona {b}: el sistema <b>no té solució</b>. És un <b>sistema incompatible</b> (les dues rectes són paral·leles).", "Ningún valor multiplicado por 0 da {b}: el sistema <b>no tiene solución</b>. Es un <b>sistema incompatible</b> (las dos rectas son paralelas).", "No value times 0 gives {b}: the system has <b>no solution</b>. It's an <b>inconsistent system</b> (the two lines are parallel).")), { b: tex(nt(B)) }) + "</span>");
      return { kind: "si" };
    }
    var v = e1.b.n ? "y" : "x", I = iso(e1, v);
    rows.push('<span class="ok">' + fill(T(L3("Qualsevol valor compleix la igualtat: el sistema té <b>infinites solucions</b>. És un <b>sistema compatible indeterminat</b> (les dues equacions són la mateixa recta). Les solucions són tots els parells amb {s}.", "Cualquier valor cumple la igualdad: el sistema tiene <b>infinitas soluciones</b>. Es un <b>sistema compatible indeterminado</b> (las dos ecuaciones son la misma recta). Las soluciones son todos los pares con {s}.", "Every value satisfies it: the system has <b>infinitely many solutions</b>. It's a <b>dependent system</b> (both equations are the same line). The solutions are all pairs with {s}.")), { s: tex(v + "=" + isoTex(I)) }) + "</span>");
    return { kind: "sci" };
  }

  /* ---------- substitució ---------- */
  function score(k) { return Math.abs(k.n / k.d) + (k.n < 0 ? 0.1 : 0) + (k.d > 1 ? 50 : 0); }
  function pickIso(es, both) {
    var best = null;
    es.forEach(function (e, i) {
      ["x", "y"].forEach(function (v) {
        var k = co(e, v); if (!k.n) return;
        if (both && !co(es[1 - i], v).n) return;
        var s = score(k) + (es[i].isoVar === v ? -1 : 0);
        if (!best || s < best.s) best = { i: i, v: v, s: s };
      });
    });
    return best;
  }
  /* equació després de substituir v per l'expressió aïllada */
  function substEq(o, I) {
    var kv = co(o, I.v), kw = co(o, I.w), tw = kw.n ? wt(kw, I.w, true) : "", body = I.den === 1 ? "(" + numTex(I.N0, I.N1, I.w) + ")" : isoTex(I);
    var tv = kTimes(kv, body, !tw);
    return (I.v === "y" ? tw + tv : kTimes(kv, body, true) + (kw.n ? wt(kw, I.w, false) : "")) + "=" + nt(o.c);
  }
  /* resol k_w·w + k_v·(N0 + N1 w)/den = c: retorna la cadena i A, B */
  function solveSubst(o, I) {
    var kv = co(o, I.v), kw = co(o, I.w), den = rat(I.den), ch = [substEq(o, I)];
    var tW = kw.n ? mono(rmul(kw, den), VE(I.w, 1)) : null;
    if (I.den > 1) {
      var tw = tW ? ttex(tW, true) : "", body = "(" + numTex(I.N0, I.N1, I.w) + ")";
      ch.push((I.v === "y" ? tw + kTimes(kv, body, !tw) : kTimes(kv, body, true) + (tW ? ttex(tW, false) : "")) + "=" + nt(rmul(o.c, den)));
    }
    var tn = numTerms(I.N0, I.N1, I.w, kv), ts = I.v === "y" ? (tW ? [tW] : []).concat(tn) : tn.concat(tW ? [tW] : []);
    var exp = joinTerms(ts) + "=" + nt(rmul(o.c, den));
    if (exp !== ch[ch.length - 1]) ch.push(exp);
    var A = radd(rmul(kw, den), rmul(kv, I.N1)), B = rsub(rmul(o.c, den), rmul(kv, I.N0));
    var red = (A.n ? wt(A, I.w, true) : "0" + I.w) + "=" + nt(B);
    if (red !== ch[ch.length - 1]) ch.push(red);
    return { ch: ch, A: A, B: B };
  }
  function backShow(I, val) {
    if (!I.N1.n) return null;
    var n = I.N1.n > 0 ? kVal(I.N1, val, true) + (I.N0.n ? ttex(mono(I.N0, {}), false) : "") : (I.N0.n ? nt(I.N0) + kVal(I.N1, val, false) : kVal(I.N1, val, true));
    return I.v + "=" + (I.den === 1 ? n : "\\frac{" + n + "}{" + I.den + "}") + "=" + nt(isoVal(I, val));
  }
  function mSub(e1, e2, rows) {
    var es = [e1, e2], P = pickIso(es), e = es[P.i], o = es[1 - P.i], I = iso(e, P.v);
    var easy = Math.abs(I.k.n) === 1 && I.k.d === 1;
    rows.push("<b>1.</b> " + fill(T(easy ? L3("Aïllem la {v} de la {n} equació (té coeficient {k}: és la més fàcil d'aïllar):", "Despejamos la {v} de la {n} ecuación (tiene coeficiente {k}: es la más fácil de despejar):", "Isolate {v} in the {n} equation (its coefficient is {k}: the easiest to isolate):")
      : L3("Aïllem la {v} de la {n} equació:", "Despejamos la {v} de la {n} ecuación:", "Isolate {v} in the {n} equation:")), { v: tex(I.v), n: ordn(P.i), k: tex(nt(I.k)) }) + tex(isoShow(e, I), true));
    var S = solveSubst(o, I);
    rows.push("<b>2.</b> " + fill(T(L3("Substituïm aquesta expressió en lloc de la {v} en l'altra equació:", "Sustituimos esta expresión en lugar de la {v} en la otra ecuación:", "Substitute this expression for {v} in the other equation:")), { v: tex(I.v) }) + tex(S.ch[0], true));
    var ch = S.ch.slice(1);
    rows.push("<b>3.</b> " + fill(T(L3("Resolem l'equació, que només té la incògnita {w}:", "Resolvemos la ecuación, que solo tiene la incógnita {w}:", "Solve the equation, which only has the unknown {w}:")), { w: tex(I.w) })
      + tex((ch.length ? ch.join("\\ \\Rightarrow\\ ") : S.ch[0]) + (S.A.n ? isolateTex(S.A, S.B, I.w) : ""), true));
    if (!S.A.n) return special(S.B, e1, rows);
    var val = rdiv(S.B, S.A), vv = isoVal(I, val), b = backShow(I, val);
    rows.push("<b>4.</b> " + (b ? fill(T(L3("Substituïm {w} en l'expressió aïllada per a trobar la {v}:", "Sustituimos {w} en la expresión despejada para hallar la {v}:", "Substitute {w} into the isolated expression to find {v}:")), { w: tex(I.w + "=" + nt(val)), v: tex(I.v) }) + tex(b, true)
      : fill(T(L3("La {v} ja la sabíem: {s}.", "La {v} ya la sabíamos: {s}.", "We already knew {v}: {s}.")), { v: tex(I.v), s: tex(I.v + "=" + nt(vv)) })));
    var r = { kind: "scd" }; r[I.w] = val; r[I.v] = vv; return r;
  }

  /* ---------- igualació ---------- */
  function mIgu(e1, e2, rows) {
    var P = pickIso([e1, e2], true), v = P.v, I1 = iso(e1, v), I2 = iso(e2, v), w = I1.w;
    rows.push("<b>1.</b> " + fill(T(L3("Aïllem la mateixa incògnita, la {v}, de les dues equacions:", "Despejamos la misma incógnita, la {v}, de las dos ecuaciones:", "Isolate the same unknown, {v}, in both equations:")), { v: tex(v) })
      + tex(isoShow(e1, I1), true) + tex(isoShow(e2, I2), true));
    rows.push("<b>2.</b> " + fill(T(L3("Igualem les dues expressions (les dues valen el mateix, la {v}):", "Igualamos las dos expresiones (las dos valen lo mismo, la {v}):", "Set the two expressions equal (both equal {v}):")), { v: tex(v) }) + tex(isoTex(I1) + "=" + isoTex(I2), true));
    var m = lcm(I1.den, I2.den), k1 = rat(m / I1.den), k2 = rat(m / I2.den), ch = [];
    if (m > 1) {
      var s1 = k1.n === 1 ? numTex(I1.N0, I1.N1, w) : kTimes(k1, "(" + numTex(I1.N0, I1.N1, w) + ")", true);
      var s2 = k2.n === 1 ? numTex(I2.N0, I2.N1, w) : kTimes(k2, "(" + numTex(I2.N0, I2.N1, w) + ")", true);
      ch.push(s1 + "=" + s2);
      var x1 = joinTerms(numTerms(I1.N0, I1.N1, w, k1)) + "=" + joinTerms(numTerms(I2.N0, I2.N1, w, k2));
      if (x1 !== ch[0]) ch.push(x1);
    }
    var A = rsub(rmul(I1.N1, k1), rmul(I2.N1, k2)), B = rsub(rmul(I2.N0, k2), rmul(I1.N0, k1));
    ch.push((A.n ? wt(A, w, true) : "0" + w) + "=" + nt(B));
    rows.push("<b>3.</b> " + (m > 1 ? fill(T(L3("Resolem l'equació (primer traiem denominadors multiplicant per {m}):", "Resolvemos la ecuación (primero quitamos denominadores multiplicando por {m}):", "Solve the equation (first clear denominators by multiplying by {m}):")), { m: m })
      : T(L3("Resolem l'equació: passem les {w} a un membre i els nombres a l'altre:", "Resolvemos la ecuación: pasamos las {w} a un miembro y los números al otro:", "Solve the equation: {w} terms on one side, numbers on the other:")).replace("{w}", tex(w)))
      + tex(ch.join("\\ \\Rightarrow\\ ") + (A.n ? isolateTex(A, B, w) : ""), true));
    if (!A.n) return special(B, e1, rows);
    var val = rdiv(B, A), b = backShow(I1, val);
    rows.push("<b>4.</b> " + (b ? fill(T(L3("Substituïm {w} en la primera expressió:", "Sustituimos {w} en la primera expresión:", "Substitute {w} into the first expression:")), { w: tex(w + "=" + nt(val)) }) + tex(b, true)
      : fill(T(L3("De la primera expressió: {s}.", "De la primera expresión: {s}.", "From the first expression: {s}.")), { s: tex(v + "=" + nt(isoVal(I1, val))) })));
    var r = { kind: "scd" }; r[w] = val; r[v] = isoVal(I1, val); return r;
  }

  /* ---------- reducció ---------- */
  function pickRed(e1, e2) {
    var best = null;
    ["y", "x"].forEach(function (v) {
      var c1 = co(e1, v), c2 = co(e2, v); if (!c1.n || !c2.n) return;
      var l = lcm(Math.abs(c1.n), Math.abs(c2.n)), m1 = l / Math.abs(c1.n), m2 = l / Math.abs(c2.n);
      if ((c1.n > 0) === (c2.n > 0)) { if (m1 === 1 && m2 !== 1) m1 = -m1; else m2 = -m2; }
      var s = Math.abs(m1) + Math.abs(m2) + (m1 < 0 ? 0.5 : 0);
      if (!best || s < best.s) best = { v: v, m1: rat(m1), m2: rat(m2), s: s };
    });
    return best;
  }
  function arrRow(e, hideV) {
    var tx = e.a.n && hideV !== "x" ? wt(e.a, "x", true) : "", ty = e.b.n && hideV !== "y" ? wt(e.b, "y", !tx) : "";
    if (hideV === "both") return "&0&=&" + nt(e.c);
    return (hideV === "x" ? "" : tx) + "&" + (hideV === "y" ? "" : ty) + "&=&" + nt(e.c);
  }
  function mRed(e1, e2, rows) {
    var P = pickRed(e1, e2), v = P.v, w = other(v), f1 = sc(e1, P.m1), f2 = sc(e2, P.m2);
    var sum = { a: radd(f1.a, f2.a), b: radd(f1.b, f2.b), c: radd(f1.c, f2.c) }, A = co(sum, w), B = sum.c;
    var one = function (m) { return m.n === 1 && m.d === 1; };
    var msg = one(P.m1) && one(P.m2) ? T(L3("Els coeficients de la {v} ja són oposats: sumem directament les dues equacions.", "Los coeficientes de la {v} ya son opuestos: sumamos directamente las dos ecuaciones.", "The {v} coefficients are already opposite: just add the two equations."))
      : one(P.m1) ? fill(T(L3("Per a eliminar la {v}, multipliquem la segona equació per {m2}: així els coeficients de la {v} són oposats. Després sumem.", "Para eliminar la {v}, multiplicamos la segunda ecuación por {m2}: así los coeficientes de la {v} son opuestos. Después sumamos.", "To eliminate {v}, multiply the second equation by {m2}: now the {v} coefficients are opposite. Then add.")), { m2: tex(nt(P.m2)) })
      : one(P.m2) ? fill(T(L3("Per a eliminar la {v}, multipliquem la primera equació per {m1}: així els coeficients de la {v} són oposats. Després sumem.", "Para eliminar la {v}, multiplicamos la primera ecuación por {m1}: así los coeficientes de la {v} son opuestos. Después sumamos.", "To eliminate {v}, multiply the first equation by {m1}: now the {v} coefficients are opposite. Then add.")), { m1: tex(nt(P.m1)) })
      : fill(T(L3("Per a eliminar la {v}, multipliquem la primera equació per {m1} i la segona per {m2}: així els coeficients de la {v} són oposats. Després sumem.", "Para eliminar la {v}, multiplicamos la primera ecuación por {m1} y la segunda por {m2}: así los coeficientes de la {v} son opuestos. Después sumamos.", "To eliminate {v}, multiply the first equation by {m1} and the second by {m2}: now the {v} coefficients are opposite. Then add.")), { m1: tex(nt(P.m1)), m2: tex(nt(P.m2)) });
    var lab = function (m) { return one(m) ? "" : "\\scriptstyle(\\cdot" + ntp(m) + ")"; };
    var arr = "\\begin{array}{lrrcr}" + lab(P.m1) + "&" + arrRow(f1) + "\\\\" + lab(P.m2) + "&" + arrRow(f2) + "\\\\\\hline" + "&" + arrRow(sum, A.n ? v : "both") + "\\end{array}";
    rows.push("<b>1.</b> " + msg.replace(/\{v\}/g, tex(v)) + tex(arr, true));
    if (!A.n) {
      rows.push("<b>2.</b> " + fill(T(L3("En sumar s'han eliminat les dues incògnites i queda {e}.", "Al sumar se han eliminado las dos incógnitas y queda {e}.", "Adding has eliminated both unknowns, leaving {e}.")), { e: tex("0=" + nt(B)) }));
      return special(B, e1, rows);
    }
    var val = rdiv(B, A);
    rows.push("<b>2.</b> " + fill(T(L3("Resolem l'equació que queda:", "Resolvemos la ecuación que queda:", "Solve the equation that is left:")), {}) + tex(wt(A, w, true) + "=" + nt(B) + isolateTex(A, B, w), true));
    var i = score(co(e1, v)) <= score(co(e2, v)) ? 0 : 1, e = [e1, e2][i], kv = co(e, v), kw = co(e, w);
    var lhs = v === "y" ? (kw.n ? kVal(kw, val, true) : "") + (kw.n ? wt(kv, v, false) : wt(kv, v, true)) : wt(kv, v, true) + (kw.n ? kVal(kw, val, false) : "");
    var rhs = rsub(e.c, rmul(kw, val)), ch = [lhs + "=" + nt(e.c)];
    if (kw.n) ch.push(wt(kv, v, true) + "=" + nt(e.c) + (rmul(kw, val).n ? ttex(mono(rneg(rmul(kw, val)), {}), false) : "") + (rmul(kw, val).n ? "=" + nt(rhs) : ""));
    rows.push("<b>3.</b> " + fill(T(L3("Substituïm {w} en la {n} equació per a trobar la {v}:", "Sustituimos {w} en la {n} ecuación para hallar la {v}:", "Substitute {w} into the {n} equation to find {v}:")), { w: tex(w + "=" + nt(val)), n: ordn(i), v: tex(v) })
      + tex(ch.join("\\ \\Rightarrow\\ ") + isolateTex(kv, rhs, v), true));
    var r = { kind: "scd" }; r[w] = val; r[v] = rdiv(rhs, kv); return r;
  }

  /* ---------- resolució completa ---------- */
  function classify(e1, e2) {
    var det = rsub(rmul(e1.a, e2.b), rmul(e2.a, e1.b));
    if (det.n) return "scd";
    return !rsub(rmul(e1.a, e2.c), rmul(e2.a, e1.c)).n && !rsub(rmul(e1.b, e2.c), rmul(e2.b, e1.c)).n ? "sci" : "si";
  }
  function autoMethod(e1, e2) {
    if (e1.isoVar && e2.isoVar && e1.isoVar === e2.isoVar) return "igu";
    var p = pickIso([e1, e2]); if (p && p.s < 1.5) return "sub";
    return "red";
  }
  function checkRow(E1, E2, o) {
    return T(L3("Comprovació:", "Comprobación:", "Check:")) + " " + [E1, E2].map(function (E) {
      var vl = evalAt(E.L, o), vr = evalAt(E.R, o), rc = isConst(E.R);
      return tex(substRaw2(E.ls, o) + "=" + nt(vl) + (rc ? "" : ";\\ \\ " + substRaw2(E.rs, o) + "=" + nt(vr))) + (req(vl, vr) ? " ✓" : " ✗");
    }).join(" &nbsp;&nbsp; ");
  }
  /* substitució en l'expressió escrita: "2x+y", x=3, y=-1 -> "2·3+(-1)" */
  function substRaw2(s, o) {
    var out = "";
    for (var i = 0; i < s.length; i++) {
      var c = s[i].toLowerCase(), r = (c === "x" || c === "y") ? o[c] : null;
      if (r) { var V = r.n < 0 || r.d !== 1 ? "(" + nt(r) + ")" : nt(r); out += (i > 0 && /[\d)\]}a-z]/i.test(s[i - 1]) ? "\\cdot " : "") + V + (i + 1 < s.length && /[\d(a-z]/i.test(s[i + 1]) ? "\\cdot " : ""); }
      else out += s[i];
    }
    return texRaw(out);
  }
  function solveSys(E1, E2, method) {
    var rows = [], quiet = method !== "red", e1 = prep2(E1, rows, 0, quiet), e2 = prep2(E2, rows, 1, quiet), R;
    e1.isoVar = E1.iso; e2.isoVar = E2.iso;
    if (!method) {
      method = autoMethod(e1, e2);
      if (method === "red") { rows = []; e1 = prep2(E1, rows, 0, false); e2 = prep2(E2, rows, 1, false); e1.isoVar = E1.iso; e2.isoVar = E2.iso; }
    }
    if (rows.length) rows.push(T(L3("El sistema en forma reduïda és:", "El sistema en forma reducida es:", "In standard form the system is:")) + tex(sysTex(ltex(e1), ltex(e2)), true));
    var noY = !e1.b.n && !e2.b.n, noX = !e1.a.n && !e2.a.n;
    if (noX || noY) {
      var k = classify(e1, e2), v = noY ? "x" : "y";
      rows.push(fill(T(L3("Cap de les dues equacions té la {v}: la {v} pot valdre qualsevol cosa.", "Ninguna de las dos ecuaciones tiene la {v}: la {v} puede valer cualquier cosa.", "Neither equation contains {v}: {v} can take any value.")), { v: tex(noY ? "y" : "x") }));
      rows.push(k === "si" ? '<span class="ko">' + T(L3("Les dues equacions es contradiuen: <b>sistema incompatible</b>.", "Las dos ecuaciones se contradicen: <b>sistema incompatible</b>.", "The two equations contradict each other: <b>inconsistent system</b>.")) + "</span>"
        : '<span class="ok">' + T(L3("<b>Sistema compatible indeterminat</b>: infinites solucions.", "<b>Sistema compatible indeterminado</b>: infinitas soluciones.", "<b>Dependent system</b>: infinitely many solutions.")) + "</span>");
      return { rows: rows, kind: k, e: [e1, e2], method: method };
    }
    if ((!e1.a.n && !e2.b.n) || (!e1.b.n && !e2.a.n)) {
      var ex = e1.a.n ? e1 : e2, ey = e1.b.n ? e1 : e2;
      R = { kind: "scd", x: rdiv(ex.c, ex.a), y: rdiv(ey.c, ey.b) };
      rows.push(T(L3("Cada equació només té una incògnita: les resolem per separat.", "Cada ecuación solo tiene una incógnita: las resolvemos por separado.", "Each equation has only one unknown: solve them separately.")) + tex(ltex(ex) + isolateTex(ex.a, ex.c, "x") + "\\qquad " + ltex(ey) + isolateTex(ey.b, ey.c, "y"), true));
    } else R = method === "sub" ? mSub(e1, e2, rows) : method === "igu" ? mIgu(e1, e2, rows) : mRed(e1, e2, rows);
    if (R.kind === "scd") {
      rows.push('<span class="ok">' + T(L3("Solució (sistema compatible determinat):", "Solución (sistema compatible determinado):", "Solution (one solution):")) + "</span> " + tex("\\boxed{" + sol(R) + "}"));
      rows.push(checkRow(E1, E2, R));
    }
    R.rows = rows; R.e = [e1, e2]; R.method = method;
    return R;
  }

  /* ---------- gràfiques ---------- */
  function fv(r) { return r.n / r.d; }
  function graphSvg(lines, pts, R, small) {
    R = R || 8; var W = 320, H = 320, g = "", k;
    function sx(x) { return ((x + R) / (2 * R) * W).toFixed(1); }
    function sy(y) { return (H - (y + R) / (2 * R) * H).toFixed(1); }
    for (k = -R; k <= R; k++) g += '<line class="grid" x1="' + sx(k) + '" y1="0" x2="' + sx(k) + '" y2="' + H + '"/><line class="grid" x1="0" y1="' + sy(k) + '" x2="' + W + '" y2="' + sy(k) + '"/>';
    g += '<line class="ax" x1="0" y1="' + sy(0) + '" x2="' + W + '" y2="' + sy(0) + '"/><line class="ax" x1="' + sx(0) + '" y1="0" x2="' + sx(0) + '" y2="' + H + '"/>';
    var st = R > 6 ? 2 : 1;
    for (k = -R + st; k < R; k += st) if (k) g += '<text class="tk" x="' + sx(k) + '" y="' + (+sy(0) + 13) + '" text-anchor="middle">' + k + '</text><text class="tk" x="' + (+sx(0) - 5) + '" y="' + (+sy(k) + 4) + '" text-anchor="end">' + k + "</text>";
    g += '<text class="tk ax-l" x="' + (W - 6) + '" y="' + (+sy(0) - 6) + '" text-anchor="end">x</text><text class="tk ax-l" x="' + (+sx(0) + 6) + '" y="12">y</text>';
    lines.forEach(function (L, i) {
      var a = fv(L.a), b = fv(L.b), c = fv(L.c), X = R + 1, p;
      p = Math.abs(b) > 1e-12 ? [-X, (c + a * X) / b, X, (c - a * X) / b] : [c / a, -X, c / a, X];
      g += '<line class="ln ln' + (L.cls == null ? i : L.cls) + (L.dash ? " dash" : "") + '" x1="' + sx(p[0]) + '" y1="' + sy(p[1]) + '" x2="' + sx(p[2]) + '" y2="' + sy(p[3]) + '"/>';
    });
    (pts || []).forEach(function (p) {
      if (Math.abs(p.x) > R || Math.abs(p.y) > R) return;
      g += '<circle class="' + (p.cls || "pt") + '" cx="' + sx(p.x) + '" cy="' + sy(p.y) + '" r="' + (p.r || 5) + '"/>';
      if (p.lab) g += '<text class="plab" x="' + (+sx(p.x) + 8) + '" y="' + (+sy(p.y) - 8) + '">' + p.lab + "</text>";
    });
    return '<svg class="sgraf' + (small ? " small" : "") + '" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="gràfica">' + g + "</svg>";
  }
  /* taula de valors amb x que donen y entera, si n'hi ha */
  function tvals(e, n) {
    var out = [], k;
    if (!e.b.n) { var x0 = rdiv(e.c, e.a); [-1, 0, 1, 2, 3].slice(0, n).forEach(function (y) { out.push({ x: x0, y: rat(y) }); }); return out; }
    var c = [0]; for (k = 1; k <= 8; k++) c.push(k, -k);
    c.forEach(function (x) { if (out.length < n) { var y = rdiv(rsub(e.c, rmul(e.a, rat(x))), e.b); if (y.d === 1 && Math.abs(y.n) <= 8) out.push({ x: rat(x), y: y }); } });
    if (out.length < 2) { out = []; [-1, 0, 1, 2, 3].slice(0, n).forEach(function (x) { out.push({ x: rat(x), y: rdiv(rsub(e.c, rmul(e.a, rat(x))), e.b) }); }); }
    return out.sort(function (p, q) { return fv(p.x) - fv(q.x) || fv(p.y) - fv(q.y); });
  }
  function tvTable(ps, cls) {
    return '<table class="data tv' + (cls ? " " + cls : "") + '"><tbody><tr><th>' + tex("x") + "</th>" + ps.map(function (p) { return "<td>" + tex(nt(p.x)) + "</td>"; }).join("") + "</tr><tr><th>" + tex("y") + "</th>" + ps.map(function (p) { return "<td>" + tex(nt(p.y)) + "</td>"; }).join("") + "</tr></tbody></table>";
  }
  function yOf(e) { return e.b.n ? "y=" + isoTex(iso(e, "y")) : "x=" + nt(rdiv(e.c, e.a)); }

  /* ---------- giny: taula de valors i recta ---------- */
  function wLine() {
    var w = document.getElementById("w-line"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      var E = readLin(I.e.value); info.innerHTML = "";
      if (!E) { out.innerHTML = ""; info.innerHTML = warn(u("bad1")); return; }
      var rows = [], e = prep2(E, rows, 0, true), ps = tvals(e, 5);
      var pts = ps.map(function (p) { return { x: fv(p.x), y: fv(p.y) }; });
      out.innerHTML = '<div class="gcol">' + (e.b.n ? "<p>" + fill(T(L3("Aïllem la {y} i donem valors a la {x}:", "Despejamos la {y} y damos valores a la {x}:", "Isolate {y} and give values to {x}:")), { y: tex("y"), x: tex("x") }) + " " + tex(yOf(e)) + "</p>"
        : "<p>" + fill(T(L3("No hi ha {y}: {e}, i la {y} pot valdre qualsevol cosa (recta vertical).", "No hay {y}: {e}, y la {y} puede valer cualquier cosa (recta vertical).", "There's no {y}: {e}, and {y} can be anything (a vertical line).")), { y: tex("y"), e: tex(yOf(e)) }) + "</p>")
        + '<div class="tbl-wrap">' + tvTable(ps) + "</div></div>" + graphSvg([e], pts, 8);
      var p = ps[0];
      info.innerHTML = "💡 " + fill(T(L3("Cada columna de la taula és una solució de l'equació, per exemple {p}. Totes les solucions formen una recta: n'hi ha <b>infinites</b>.", "Cada columna de la tabla es una solución de la ecuación, por ejemplo {p}. Todas las soluciones forman una recta: hay <b>infinitas</b>.", "Each column of the table is a solution, for example {p}. All the solutions form a line: there are <b>infinitely many</b>.")), { p: tex("(" + nt(p.x) + ",\\," + nt(p.y) + ")") });
    }
    I.e.addEventListener("input", paint);
    quickBind(w, function (v) { I.e.value = v[0]; paint(); });
    onLang(paint);
  }

  /* ---------- giny: és solució del sistema? ---------- */
  function wPair() {
    var w = document.getElementById("w-pair"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      var E1 = readLin(I.e1.value), E2 = readLin(I.e2.value), px = parse(clean(I.x.value)), py = parse(clean(I.y.value)); info.innerHTML = "";
      if (!E1 || !E2) { out.innerHTML = ""; info.innerHTML = warn(u("bad")); return; }
      if (!px || !py || !isConst(px) || !isConst(py)) { out.innerHTML = ""; info.innerHTML = warn(u("num")); return; }
      var o = { x: cval(px), y: cval(py) }, rows = [], good = 0;
      rows.push(tex(sysTex(rawTex(E1), rawTex(E2)), true));
      [E1, E2].forEach(function (E, i) {
        var vl = evalAt(E.L, o), vr = evalAt(E.R, o), ok = req(vl, vr); if (ok) good++;
        rows.push(fill(T(L3("{n} equació:", "{n} ecuación:", "{n} equation:")), { n: ordn(i).charAt(0).toUpperCase() + ordn(i).slice(1) }) + " " + tex(substRaw2(E.ls, o) + "=" + nt(vl)) + (isConst(E.R) ? "" : " ; " + tex(substRaw2(E.rs, o) + "=" + nt(vr))) + (ok ? ' <span class="ok">✓</span>' : ' <span class="ko">✗ ' + tex(nt(vl) + "\\neq" + nt(vr)) + "</span>"));
      });
      var p = tex("(" + nt(o.x) + ",\\," + nt(o.y) + ")");
      rows.push(good === 2 ? '<span class="ok">✓ ' + fill(T(L3("Compleix les dues equacions: {p} <b>és solució del sistema</b>.", "Cumple las dos ecuaciones: {p} <b>es solución del sistema</b>.", "It satisfies both equations: {p} <b>is a solution of the system</b>.")), { p: p }) + "</span>"
        : '<span class="ko">✗ ' + fill(T(good ? L3("Només compleix una de les equacions: {p} <b>no és solució del sistema</b>.", "Solo cumple una de las ecuaciones: {p} <b>no es solución del sistema</b>.", "It only satisfies one equation: {p} <b>is not a solution of the system</b>.") : L3("No compleix cap equació: {p} <b>no és solució</b>.", "No cumple ninguna ecuación: {p} <b>no es solución</b>.", "It satisfies neither equation: {p} <b>is not a solution</b>.")), { p: p }) + "</span>");
      out.innerHTML = rows2html(rows);
    }
    [I.e1, I.e2, I.x, I.y].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.e1.value = v[0]; I.e2.value = v[1]; I.x.value = v[2]; I.y.value = v[3]; paint(); });
    onLang(paint);
  }

  /* ---------- ginys: resolució pas a pas ---------- */
  var MNAME = { sub: L3("substitució", "sustitución", "substitution"), igu: L3("igualació", "igualación", "equalisation"), red: L3("reducció", "reducción", "elimination") };
  function solverWidget(w) {
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), fixed = w.dataset.m;
    function paint() {
      var E1 = readLin(I.e1.value), E2 = readLin(I.e2.value); info.innerHTML = "";
      if (!E1 || !E2) { out.innerHTML = ""; info.innerHTML = warn(u("bad")); return; }
      var m = fixed || segVal(w) || null, R = solveSys(E1, E2, m === "auto" ? null : m);
      out.innerHTML = rows2html([tex(sysTex(rawTex(E1), rawTex(E2)), true)].concat(R.rows));
      if (!fixed && (m === "auto" || !m)) info.innerHTML = "💡 " + fill(T(L3("Mètode triat: <b>{m}</b>.", "Método elegido: <b>{m}</b>.", "Method chosen: <b>{m}</b>.")), { m: T(MNAME[R.method]) });
    }
    [I.e1, I.e2].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.e1.value = v[0]; I.e2.value = v[1]; paint(); });
    if (!fixed) segBind(w, paint);
    onLang(paint);
  }

  /* ---------- giny: mètode gràfic i classificació ---------- */
  function ratioTex(e1, e2) {
    function q(p, r) { return r.n ? "\\frac{" + nt(p) + "}{" + nt(r) + "}" : (p.n ? "\\frac{" + nt(p) + "}{0}" : "\\frac{0}{0}"); }
    return "\\frac{a}{a'}=" + q(e1.a, e2.a) + ",\\quad \\frac{b}{b'}=" + q(e1.b, e2.b) + ",\\quad \\frac{c}{c'}=" + q(e1.c, e2.c);
  }
  var KIND = {
    scd: L3("<b>Rectes secants</b>: es tallen en un punt. <b>Sistema compatible determinat</b> (una solució).", "<b>Rectas secantes</b>: se cortan en un punto. <b>Sistema compatible determinado</b> (una solución).", "<b>Intersecting lines</b>: they cross at one point. <b>One solution</b> (independent system)."),
    sci: L3("<b>Rectes coincidents</b>: són la mateixa recta. <b>Sistema compatible indeterminat</b> (infinites solucions).", "<b>Rectas coincidentes</b>: son la misma recta. <b>Sistema compatible indeterminado</b> (infinitas soluciones).", "<b>Coincident lines</b>: they are the same line. <b>Infinitely many solutions</b> (dependent system)."),
    si: L3("<b>Rectes paral·leles</b>: no es tallen mai. <b>Sistema incompatible</b> (cap solució).", "<b>Rectas paralelas</b>: no se cortan nunca. <b>Sistema incompatible</b> (ninguna solución).", "<b>Parallel lines</b>: they never meet. <b>No solution</b> (inconsistent system).")
  };
  function wGraf(w) {
    var I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), ratio = w.hasAttribute("data-ratio");
    function paint() {
      var E1 = readLin(I.e1.value), E2 = readLin(I.e2.value); info.innerHTML = "";
      if (!E1 || !E2) { out.innerHTML = ""; info.innerHTML = warn(u("bad")); return; }
      var tmp = [], e1 = prep2(E1, tmp, 0, true), e2 = prep2(E2, tmp, 1, true), k = classify(e1, e2), pts = [], s = null;
      var p1 = tvals(e1, 3), p2 = tvals(e2, 3);
      p1.forEach(function (p) { pts.push({ x: fv(p.x), y: fv(p.y), cls: "pt p0", r: 4 }); });
      p2.forEach(function (p) { pts.push({ x: fv(p.x), y: fv(p.y), cls: "pt p1", r: 4 }); });
      if (k === "scd") {
        var det = rsub(rmul(e1.a, e2.b), rmul(e2.a, e1.b));
        s = { x: rdiv(rsub(rmul(e1.c, e2.b), rmul(e2.c, e1.b)), det), y: rdiv(rsub(rmul(e1.a, e2.c), rmul(e2.a, e1.c)), det) };
        pts.push({ x: fv(s.x), y: fv(s.y), cls: "cut", r: 7, lab: "(" + nt(s.x).replace(/\\frac\{(\d+)\}\{(\d+)\}/, "$1/$2") + ", " + nt(s.y).replace(/\\frac\{(\d+)\}\{(\d+)\}/, "$1/$2") + ")" });
      }
      var lines = [{ a: e1.a, b: e1.b, c: e1.c }, { a: e2.a, b: e2.b, c: e2.c, dash: k === "sci" }];
      out.innerHTML = '<div class="gcol"><p><span class="key k0"></span>' + tex(rawTex(E1)) + (E1.iso || !e1.b.n ? "" : " &nbsp;→&nbsp; " + tex(yOf(e1))) + '</p><div class="tbl-wrap">' + tvTable(p1, "t0") + "</div>"
        + '<p><span class="key k1"></span>' + tex(rawTex(E2)) + (E2.iso || !e2.b.n ? "" : " &nbsp;→&nbsp; " + tex(yOf(e2))) + '</p><div class="tbl-wrap">' + tvTable(p2, "t1") + "</div></div>" + graphSvg(lines, pts, 8);
      var msg = T(KIND[k]);
      if (s) {
        var whole = s.x.d === 1 && s.y.d === 1, inR = Math.abs(fv(s.x)) <= 8 && Math.abs(fv(s.y)) <= 8;
        msg += " " + (whole && inR ? fill(T(L3("El punt de tall és la solució: {s}.", "El punto de corte es la solución: {s}.", "The crossing point is the solution: {s}.")), { s: tex(sol(s)) })
          : !inR ? fill(T(L3("El punt de tall queda fora del dibuix: {s}.", "El punto de corte queda fuera del dibujo: {s}.", "The crossing point is off the grid: {s}.")), { s: tex(sol(s)) })
          : fill(T(L3("El punt de tall no té coordenades enteres: en el dibuix només el podem llegir de manera aproximada. Amb un mètode algebraic obtenim {s}.", "El punto de corte no tiene coordenadas enteras: en el dibujo solo lo podemos leer de forma aproximada. Con un método algebraico obtenemos {s}.", "The crossing point doesn't have whole-number coordinates: we can only read it approximately. An algebraic method gives {s}.")), { s: tex(sol(s)) }));
      }
      if (ratio) msg += '<br><span class="ratio">' + T(L3("Coeficients:", "Coeficientes:", "Coefficients:")) + " " + tex(ratioTex(e1, e2)) + "</span>";
      info.innerHTML = msg;
    }
    [I.e1, I.e2].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.e1.value = v[0]; I.e2.value = v[1]; paint(); });
    onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  function term(a, v, first) { return a ? (a < 0 ? "-" : first ? "" : "+") + (Math.abs(a) === 1 ? "" : Math.abs(a)) + v : ""; }
  function linS(a, b, c) { var s = term(a, "x", true); return s + term(b, "y", !s) + "=" + c; }
  /* x aïllada: ax + by = c amb a = ±1 -> "x=c/a-(b/a)y" */
  function isoS(a, b, c) { var k = -b / a, d = c / a, s = term(k, "y", true); return "x=" + (s ? s + (d ? (d > 0 ? "+" : "") + d : "") : d); }
  function pairItem(s1, s2, x0, y0, method) {
    return { pair: true, ans: { x: rat(x0), y: rat(y0) },
      q: function () { return (method ? fill(T(L3("Resol pel mètode de {m}:", "Resuelve por el método de {m}:", "Solve by {m}:")), { m: T(MNAME[method]) }) : T(L3("Resol el sistema:", "Resuelve el sistema:", "Solve the system:"))) + " $" + sysTex(texRaw(s1.split("=")[0]) + "=" + texRaw(s1.split("=")[1]), texRaw(s2.split("=")[0]) + "=" + texRaw(s2.split("=")[1])) + "$"; },
      s: function () { return rows2html(solveSys(readLin(s1), readLin(s2), method).rows); } };
  }
  function rsys(kind) {
    var x0 = rint(-6, 6), y0 = rint(-6, 6), a1, b1, a2, b2;
    do {
      if (kind === "sub") { a1 = rnz(-5, 5); b1 = pick([1, 1, -1]); a2 = rnz(-5, 5); b2 = rnz(-5, 5); if (rint(0, 1)) { var t = a1; a1 = b1; b1 = t; } }
      else if (kind === "igu") { a1 = pick([1, 1, -1]); a2 = pick([1, 1, 2, -1]); b1 = rnz(-5, 5); b2 = rnz(-5, 5); }
      else { a1 = rnz(-7, 7); b1 = rnz(-7, 7); a2 = rnz(-7, 7); b2 = rnz(-7, 7); if (Math.abs(a1) + Math.abs(b1) < 5 || Math.abs(a2) + Math.abs(b2) < 5) a1 = 0; }
    } while (!a1 || a1 * b2 - a2 * b1 === 0);
    var c1 = a1 * x0 + b1 * y0, c2 = a2 * x0 + b2 * y0, s1 = linS(a1, b1, c1), s2 = linS(a2, b2, c2);
    if (kind === "igu" && Math.abs(a2) === 1 && rint(0, 1)) { s1 = isoS(a1, b1, c1); s2 = isoS(a2, b2, c2); }
    return pairItem(s1, s2, x0, y0, kind);
  }
  function mixSys() {
    var u0 = rnz(-3, 3), v0 = rnz(-3, 3), d1 = pick([2, 3, 4]), d2 = pick([2, 3, 5]), p = rnz(-4, 4), a = rint(2, 4), b = rnz(-3, 3);
    while (d2 === d1) d2 = pick([2, 3, 5]);
    var x0 = d1 * u0, y0 = d2 * v0;
    var s1 = a + "(x" + (p > 0 ? "+" : "") + p + ")" + term(b, "y", false) + "=" + (a * (x0 + p) + b * y0);
    var s2 = "x/" + d1 + (rint(0, 1) ? "+" : "-") + "y/" + d2, sg = s2.indexOf("-y") >= 0 ? -1 : 1;
    s2 += "=" + (u0 + sg * v0);
    var e1 = { a: a, b: b }, e2 = { a: d2, b: sg * d1 };
    if (e1.a * e2.b - e2.a * e1.b === 0) return mixSys();
    return pairItem(s1, s2, x0, y0, null);
  }
  var PROBS = [
    function () { var y = rint(3, 40), x = y + rint(2, 30); return { ans: [x, y], d: { S: x + y, D: x - y }, q: L3("Dos nombres sumen {S} i la seua diferència és {D}. Quins són? (Escriu: el major; el menor)", "Dos números suman {S} y su diferencia es {D}. ¿Cuáles son? (Escribe: el mayor; el menor)", "Two numbers add up to {S} and their difference is {D}. What are they? (Type: larger; smaller)"), e: "\\begin{cases}x+y=" + (x + y) + "\\\\x-y=" + (x - y) + "\\end{cases}\\Rightarrow 2x=" + 2 * x + "\\Rightarrow x=" + x + ",\\ y=" + y }; },
    function () { var g = rint(5, 30), c = rint(3, 25); return { ans: [g, c], d: { H: g + c, P: 2 * g + 4 * c }, q: L3("En una granja hi ha gallines i conills: {H} caps i {P} potes. Quants n'hi ha de cada? (gallines; conills)", "En una granja hay gallinas y conejos: {H} cabezas y {P} patas. ¿Cuántos hay de cada? (gallinas; conejos)", "A farm has hens and rabbits: {H} heads and {P} legs. How many of each? (hens; rabbits)"), e: "\\begin{cases}x+y=" + (g + c) + "\\\\2x+4y=" + (2 * g + 4 * c) + "\\end{cases}\\Rightarrow x=" + g + ",\\ y=" + c }; },
    function () { var x = rint(4, 25), y = rint(4, 25); return { ans: [x, y], d: { N: x + y, V: x + 2 * y }, q: L3("En una guardiola hi ha {N} monedes d'1 € i de 2 € que sumen {V} €. Quantes n'hi ha de cada? (d'1 €; de 2 €)", "En una hucha hay {N} monedas de 1 € y de 2 € que suman {V} €. ¿Cuántas hay de cada? (de 1 €; de 2 €)", "A money box holds {N} €1 and €2 coins worth €{V} in all. How many of each? (€1; €2)"), e: "\\begin{cases}x+y=" + (x + y) + "\\\\x+2y=" + (x + 2 * y) + "\\end{cases}\\Rightarrow y=" + y + ",\\ x=" + x }; },
    function () { var a = rint(10, 60), n = rint(10, 60), pa = pick([6, 7, 8, 9]), pn = pick([3, 4, 5]); return { ans: [a, n], d: { N: a + n, M: pa * a + pn * n, pa: pa, pn: pn }, q: L3("L'entrada d'un museu costa {pa} € per als adults i {pn} € per als xiquets. Han entrat {N} persones i s'han recaptat {M} €. Quants adults i quants xiquets hi han entrat? (adults; xiquets)", "La entrada de un museo cuesta {pa} € para los adultos y {pn} € para los niños. Han entrado {N} personas y se han recaudado {M} €. ¿Cuántos adultos y cuántos niños han entrado? (adultos; niños)", "Museum tickets cost €{pa} for adults and €{pn} for children. {N} people went in and €{M} was taken. How many adults and how many children? (adults; children)"), e: "\\begin{cases}x+y=" + (a + n) + "\\\\" + pa + "x+" + pn + "y=" + (pa * a + pn * n) + "\\end{cases}\\Rightarrow x=" + a + ",\\ y=" + n }; },
    function () { var f = rint(3, 12), k = pick([3, 4]), p = k * f, t = p - 2 * f; return { ans: [p, f], d: { k: [0, 0, "doble", "triple", "quàdruple"][k], kes: [0, 0, "doble", "triple", "cuádruple"][k], ken: [0, 0, "twice", "three times", "four times"][k], t: t }, q: L3("L'edat d'una mare és el {k} de la del seu fill i d'ací a {t} anys serà el doble. Quants anys tenen ara? (mare; fill)", "La edad de una madre es el {kes} de la de su hijo y dentro de {t} años será el doble. ¿Cuántos años tienen ahora? (madre; hijo)", "A mother is {ken} as old as her son, and in {t} years she'll be twice as old. How old are they now? (mother; son)"), e: "\\begin{cases}x=" + k + "y\\\\x+" + t + "=2(y+" + t + ")\\end{cases}\\Rightarrow " + k + "y+" + t + "=2y+" + 2 * t + "\\Rightarrow y=" + f + ",\\ x=" + p }; },
    function () { var h = rint(3, 15), d = rint(1, 9), b = h + d; return { ans: [b, h], d: { P: 2 * (b + h), d: d }, q: L3("La base d'un rectangle fa {d} cm més que l'altura i el perímetre és {P} cm. Quant fan la base i l'altura? (base; altura)", "La base de un rectángulo mide {d} cm más que la altura y el perímetro es {P} cm. ¿Cuánto miden la base y la altura? (base; altura)", "A rectangle's base is {d} cm longer than its height and its perimeter is {P} cm. Find the base and height. (base; height)"), e: "\\begin{cases}2x+2y=" + 2 * (b + h) + "\\\\x=y+" + d + "\\end{cases}\\Rightarrow 4y+" + 2 * d + "=" + 2 * (b + h) + "\\Rightarrow y=" + h + ",\\ x=" + b }; },
    function () { var n = pick([20, 25, 30]), x = rint(Math.ceil(n / 2), n - 1), y = n - x, p = pick([2, 3, 4]); return { ans: [x, y], d: { n: n, p: p, S: p * x - y }, q: L3("Un test té {n} preguntes, totes contestades. Cada encert suma {p} punts i cada errada en resta 1. Si has tret {S} punts, quantes n'has encertat i quantes n'has errat? (encerts; errades)", "Un test tiene {n} preguntas, todas contestadas. Cada acierto suma {p} puntos y cada fallo resta 1. Si has sacado {S} puntos, ¿cuántas has acertado y cuántas has fallado? (aciertos; fallos)", "A test has {n} questions, all answered. Each right answer scores {p} points and each wrong one loses 1. If you scored {S}, how many were right and how many wrong? (right; wrong)"), e: "\\begin{cases}x+y=" + n + "\\\\" + p + "x-y=" + (p * x - y) + "\\end{cases}\\Rightarrow " + (p + 1) + "x=" + (p * x - y + n) + "\\Rightarrow x=" + x + ",\\ y=" + y }; }
  ];
  var CLS = [L3("Compatible determinat (una solució)", "Compatible determinado (una solución)", "One solution"), L3("Compatible indeterminat (infinites)", "Compatible indeterminado (infinitas)", "Infinitely many solutions"), L3("Incompatible (cap solució)", "Incompatible (ninguna solución)", "No solution")];
  var GEN = {
    pair: function () {
      var x0 = rint(-5, 5), y0 = rint(-5, 5), a1, b1, a2, b2;
      do { a1 = rnz(-4, 4); b1 = rnz(-4, 4); a2 = rnz(-4, 4); b2 = rnz(-4, 4); } while (a1 * b2 === a2 * b1);
      var s1 = linS(a1, b1, a1 * x0 + b1 * y0), s2 = linS(a2, b2, a2 * x0 + b2 * y0), t = rint(0, 2), px = x0, py = y0;
      if (t === 1) { if (rint(0, 1)) px += rnz(-2, 2); else py += rnz(-2, 2); }
      if (t === 2) { var k = rnz(-2, 2); px = x0 + b1 * k; py = y0 - a1 * k; }
      var o = { x: rat(px), y: rat(py) }, E1 = readLin(s1), E2 = readLin(s2), ok = req(evalAt(E1.L, o), evalAt(E1.R, o)) && req(evalAt(E2.L, o), evalAt(E2.R, o));
      return { opts: [L3("Sí", "Sí", "Yes"), L3("No", "No", "No")], ans: ok ? 0 : 1,
        q: function () { return fill(T(L3("És {p} solució d'aquest sistema?", "¿Es {p} solución de este sistema?", "Is {p} a solution of this system?")), { p: "$(" + px + ",\\," + py + ")$" }) + " $" + sysTex(texRaw(s1.split("=")[0]) + "=" + s1.split("=")[1], texRaw(s2.split("=")[0]) + "=" + s2.split("=")[1]) + "$"; },
        s: function () { return [E1, E2].map(function (E) { var vl = evalAt(E.L, o); return tex(substRaw2(E.ls, o) + "=" + nt(vl)) + (req(vl, evalAt(E.R, o)) ? " ✓" : " ✗"); }).join(" &nbsp; ") + " → " + (ok ? T(L3("<b>sí</b> que és solució.", "<b>sí</b> es solución.", "it <b>is</b> a solution.")) : T(L3("<b>no</b> és solució.", "<b>no</b> es solución.", "it is <b>not</b> a solution."))); } };
    },
    sub: function () { return rsys("sub"); },
    igu: function () { return rsys("igu"); },
    red: function () { return rsys("red"); },
    mix: mixSys,
    gra: function () {
      var x0 = rint(-5, 5), y0 = rint(-5, 5), a1, b1, a2, b2;
      do { a1 = rint(-3, 3); b1 = rint(-2, 2); a2 = rint(-3, 3); b2 = rint(-2, 2); } while (!b1 || !b2 || a1 * b2 === a2 * b1 || (!a1 && !a2));
      var e1 = { a: rat(a1), b: rat(b1), c: rat(a1 * x0 + b1 * y0) }, e2 = { a: rat(a2), b: rat(b2), c: rat(a2 * x0 + b2 * y0) };
      return { pair: true, ans: { x: rat(x0), y: rat(y0) },
        q: function () { return T(L3("Quina és la solució del sistema que representen aquestes dues rectes?", "¿Cuál es la solución del sistema que representan estas dos rectas?", "What is the solution of the system shown by these two lines?")) + graphSvg([e1, e2], [], 7, true); },
        s: function () { return tex(sysTex(ltex(e1), ltex(e2))) + " → " + T(L3("les rectes es tallen en", "las rectas se cortan en", "the lines cross at")) + " " + tex("(" + x0 + ",\\," + y0 + ")") + ": " + tex("\\boxed{x=" + x0 + ",\\ y=" + y0 + "}"); } };
    },
    cls: function () {
      var t = rint(0, 2), a, b, c, k = pick([2, 3, -1, -2]), a2, b2, c2;
      do { a = rnz(-5, 5); b = rnz(-5, 5); } while (gcd(a, b) !== 1);
      c = rint(-9, 9);
      if (t === 0) { do { a2 = rnz(-5, 5); b2 = rnz(-5, 5); } while (a * b2 === a2 * b); c2 = rint(-9, 9); }
      else { a2 = k * a; b2 = k * b; c2 = t === 1 ? k * c : k * c + rnz(-4, 4); }
      var e1 = { a: rat(a), b: rat(b), c: rat(c) }, e2 = { a: rat(a2), b: rat(b2), c: rat(c2) };
      return { opts: CLS, ans: t,
        q: function () { return T(L3("Com és aquest sistema?", "¿Cómo es este sistema?", "What kind of system is this?")) + " $" + sysTex(ltex(e1), ltex(e2)) + "$"; },
        s: function () { return tex(ratioTex(e1, e2)) + " → " + T(t === 0 ? L3("els quocients de la x i la y són diferents: rectes secants.", "los cocientes de la x y la y son distintos: rectas secantes.", "the x and y ratios differ: intersecting lines.") : t === 1 ? L3("els tres quocients són iguals: rectes coincidents.", "los tres cocientes son iguales: rectas coincidentes.", "all three ratios are equal: coincident lines.") : L3("els quocients de la x i la y són iguals, però el dels termes independents és diferent: rectes paral·leles.", "los cocientes de la x y la y son iguales, pero el de los términos independientes es distinto: rectas paralelas.", "the x and y ratios are equal but the constants' ratio is different: parallel lines.")) + " <b>" + T(CLS[t]) + "</b>."; } };
    },
    prob: function () {
      var p = pick(PROBS)();
      return { pair: true, ans: { x: rat(p.ans[0]), y: rat(p.ans[1]) }, q: function () { return fill(T(p.q), p.d); }, s: function () { return tex(p.e) + " → <b>" + p.ans[0] + "; " + p.ans[1] + "</b>"; } };
    }
  };
  /* parell escrit per l'alumne: "x=3, y=-2", "(3,-2)", "3; -2" */
  function parsePair(raw) {
    var s = raw.toLowerCase().replace(/[−–]/g, "-").replace(/[()]/g, " ").trim(), o = {}, m, re = /([xy])\s*=\s*([^;,=xy]+)/g;
    if (/[xy]\s*=/.test(s)) { while ((m = re.exec(s))) { var p = parse(clean(m[2])); if (!p || !isConst(p)) return null; o[m[1]] = cval(p); } return o.x && o.y ? o : null; }
    var parts = s.indexOf(";") >= 0 ? s.split(";") : s.split(/,(?!\d)|\s+(?:i|y|and)\s+|,\s+/);
    parts = parts.map(function (t) { return t.trim(); }).filter(Boolean);
    if (parts.length !== 2) return null;
    var a = parse(clean(parts[0])), b = parse(clean(parts[1]));
    if (!a || !b || !isConst(a) || !isConst(b)) return null;
    return { x: cval(a), y: cval(b) };
  }
  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, res = 0, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore"), ob = w.querySelector(".dopts");
    function paint() {
      dq.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (ob) {
        ob.innerHTML = "";
        q.opts.forEach(function (o, j) {
          var b = document.createElement("button"); b.type = "button"; b.className = "btn"; b.innerHTML = T(o);
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
      else {
        var raw = inp.value.trim(); if (!raw) { info.innerHTML = warn(u("pair")); return; }
        var p = parsePair(raw); if (!p) { info.innerHTML = warn(u("pair")); return; }
        good = req(p.x, q.ans.x) && req(p.y, q.ans.y);
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
  window.FM6 = { parse: parse, readLin: readLin, solveSys: solveSys, classify: classify, parsePair: parsePair, GEN: GEN, nt: nt, ltex: ltex, prep2: prep2 };

  /* ---------- qüestionari ---------- */
  var QUIZ = [
    { q: { va: "Quin d'aquests parells és solució de $x+2y=7$?", es: "¿Cuál de estos pares es solución de $x+2y=7$?", en: "Which of these pairs is a solution of $x+2y=7$?" },
      o: [{ va: "$(3,\\,1)$" }, { va: "$(1,\\,3)$" }, { va: "$(2,\\,3)$" }, { va: "$(7,\\,1)$" }], a: 1,
      e: { va: "$1+2\\cdot3=7$ ✓. Amb $(3,1)$ dona 5, amb $(2,3)$ dona 8 i amb $(7,1)$ dona 9.", es: "$1+2\\cdot3=7$ ✓. Con $(3,1)$ da 5, con $(2,3)$ da 8 y con $(7,1)$ da 9.", en: "$1+2\\cdot3=7$ ✓. $(3,1)$ gives 5, $(2,3)$ gives 8 and $(7,1)$ gives 9." } },
    { q: { va: "Quantes solucions té una equació lineal amb dues incògnites, com $2x-y=3$?", es: "¿Cuántas soluciones tiene una ecuación lineal con dos incógnitas, como $2x-y=3$?", en: "How many solutions does a linear equation in two unknowns, like $2x-y=3$, have?" },
      o: [{ va: "Una", es: "Una", en: "One" }, { va: "Dues", es: "Dos", en: "Two" }, { va: "Infinites", es: "Infinitas", en: "Infinitely many" }, { va: "Cap", es: "Ninguna", en: "None" }], a: 2,
      e: { va: "Per a cada valor de $x$ hi ha un valor de $y$: $(0,-3),\\ (1,-1),\\ (2,1)\\ldots$ Totes formen una recta.", es: "Para cada valor de $x$ hay un valor de $y$: $(0,-3),\\ (1,-1),\\ (2,1)\\ldots$ Todas forman una recta.", en: "Every value of $x$ gives a value of $y$: $(0,-3),\\ (1,-1),\\ (2,1)\\ldots$ Together they form a line." } },
    { q: { va: "És $(2,\\,1)$ solució del sistema $x+y=3$, $\\ x-y=1$?", es: "¿Es $(2,\\,1)$ solución del sistema $x+y=3$, $\\ x-y=1$?", en: "Is $(2,\\,1)$ a solution of the system $x+y=3$, $\\ x-y=1$?" },
      o: [{ va: "Sí, compleix les dues equacions", es: "Sí, cumple las dos ecuaciones", en: "Yes, it satisfies both equations" }, { va: "No, només compleix la primera", es: "No, solo cumple la primera", en: "No, it only satisfies the first" }, { va: "No, no en compleix cap", es: "No, no cumple ninguna", en: "No, it satisfies neither" }], a: 0,
      e: { va: "$2+1=3$ ✓ i $2-1=1$ ✓: compleix les dues alhora.", es: "$2+1=3$ ✓ y $2-1=1$ ✓: cumple las dos a la vez.", en: "$2+1=3$ ✓ and $2-1=1$ ✓: it satisfies both at once." } },
    { q: { va: "En el sistema $y=2x-1$, $\\ 3x+y=9$, si substituïm la $y$ en la segona equació obtenim…", es: "En el sistema $y=2x-1$, $\\ 3x+y=9$, si sustituimos la $y$ en la segunda ecuación obtenemos…", en: "In the system $y=2x-1$, $\\ 3x+y=9$, substituting $y$ into the second equation gives…" },
      o: [{ va: "$3x+2x=9$" }, { va: "$3x+(2x-1)=9$" }, { va: "$3(2x-1)+y=9$" }, { va: "$2x-1=9$" }], a: 1,
      e: { va: "Posem $2x-1$ en lloc de la $y$: $3x+2x-1=9\\Rightarrow 5x=10\\Rightarrow x=2$, i $y=3$.", es: "Ponemos $2x-1$ en lugar de la $y$: $3x+2x-1=9\\Rightarrow 5x=10\\Rightarrow x=2$, e $y=3$.", en: "Put $2x-1$ in place of $y$: $3x+2x-1=9\\Rightarrow 5x=10\\Rightarrow x=2$, and $y=3$." } },
    { q: { va: "En substituir $y=5-x$ en $2x-3y=5$, quina equació és correcta?", es: "Al sustituir $y=5-x$ en $2x-3y=5$, ¿qué ecuación es correcta?", en: "Substituting $y=5-x$ into $2x-3y=5$, which equation is right?" },
      o: [{ va: "$2x-15-3x=5$" }, { va: "$2x-15+3x=5$" }, { va: "$2x-3\\cdot5-x=5$" }, { va: "$2x+15-3x=5$" }], a: 1,
      e: { va: "$-3(5-x)=-15+3x$: el $-3$ multiplica els dos termes del parèntesi. Queda $5x=20$, $x=4$, $y=1$.", es: "$-3(5-x)=-15+3x$: el $-3$ multiplica los dos términos del paréntesis. Queda $5x=20$, $x=4$, $y=1$.", en: "$-3(5-x)=-15+3x$: the $-3$ multiplies both terms in the bracket. That gives $5x=20$, $x=4$, $y=1$." } },
    { q: { va: "Quin mètode és el més còmode per a $x=2y+1$, $\\ x=5-y$?", es: "¿Qué método es el más cómodo para $x=2y+1$, $\\ x=5-y$?", en: "Which method is easiest for $x=2y+1$, $\\ x=5-y$?" },
      o: [{ va: "Reducció", es: "Reducción", en: "Elimination" }, { va: "Igualació", es: "Igualación", en: "Equalisation" }, { va: "Gràfic", es: "Gráfico", en: "Graphical" }], a: 1,
      e: { va: "La $x$ ja està aïllada en les dues: igualem $2y+1=5-y\\Rightarrow y=\\frac43$.", es: "La $x$ ya está despejada en las dos: igualamos $2y+1=5-y\\Rightarrow y=\\frac43$.", en: "$x$ is already isolated in both: set $2y+1=5-y\\Rightarrow y=\\frac43$." } },
    { q: { va: "Per a eliminar la $y$ en $2x+3y=8$, $\\ 5x-y=3$ per reducció, multipliquem la segona equació per…", es: "Para eliminar la $y$ en $2x+3y=8$, $\\ 5x-y=3$ por reducción, multiplicamos la segunda ecuación por…", en: "To eliminate $y$ in $2x+3y=8$, $\\ 5x-y=3$, we multiply the second equation by…" },
      o: [{ va: "$-3$" }, { va: "$3$" }, { va: "$2$" }, { va: "$5$" }], a: 1,
      e: { va: "Queda $15x-3y=9$; sumant: $17x=17$, $x=1$ i $y=2$.", es: "Queda $15x-3y=9$; sumando: $17x=17$, $x=1$ e $y=2$.", en: "That gives $15x-3y=9$; adding: $17x=17$, $x=1$ and $y=2$." } },
    { q: { va: "En sumar $\\ 3x+2y=8\\ $ i $\\ 5x-2y=8$ obtenim…", es: "Al sumar $\\ 3x+2y=8\\ $ y $\\ 5x-2y=8$ obtenemos…", en: "Adding $\\ 3x+2y=8\\ $ and $\\ 5x-2y=8$ gives…" },
      o: [{ va: "$8x=16$" }, { va: "$8x+4y=16$" }, { va: "$-2x=0$" }, { va: "$8x=0$" }], a: 0,
      e: { va: "Els termes $2y$ i $-2y$ s'anul·len: $8x=16\\Rightarrow x=2$, i aleshores $y=1$.", es: "Los términos $2y$ y $-2y$ se anulan: $8x=16\\Rightarrow x=2$, y entonces $y=1$.", en: "$2y$ and $-2y$ cancel: $8x=16\\Rightarrow x=2$, and then $y=1$." } },
    { q: { va: "Les rectes de les dues equacions d'un sistema es tallen en el punt $(3,\\,-1)$. La solució és…", es: "Las rectas de las dos ecuaciones de un sistema se cortan en el punto $(3,\\,-1)$. La solución es…", en: "The lines of a system's two equations cross at $(3,\\,-1)$. The solution is…" },
      o: [{ va: "$x=-1,\\ y=3$" }, { va: "$x=3,\\ y=-1$" }, { va: "$x=3,\\ y=1$" }, { va: "No en té", es: "No tiene", en: "There is none" }], a: 1,
      e: { va: "El primer nombre del punt és la $x$ i el segon, la $y$.", es: "El primer número del punto es la $x$ y el segundo, la $y$.", en: "The first number of the point is $x$ and the second is $y$." } },
    { q: { va: "Si les dues rectes d'un sistema són paral·leles, el sistema…", es: "Si las dos rectas de un sistema son paralelas, el sistema…", en: "If a system's two lines are parallel, the system…" },
      o: [{ va: "té una solució", es: "tiene una solución", en: "has one solution" }, { va: "té infinites solucions", es: "tiene infinitas soluciones", en: "has infinitely many solutions" }, { va: "no té solució", es: "no tiene solución", en: "has no solution" }], a: 2,
      e: { va: "Dues rectes paral·leles no es tallen mai: <b>sistema incompatible</b>.", es: "Dos rectas paralelas no se cortan nunca: <b>sistema incompatible</b>.", en: "Two parallel lines never meet: <b>no solution</b> (inconsistent)." } },
    { q: { va: "Com és el sistema $x+y=3$, $\\ 2x+2y=6$?", es: "¿Cómo es el sistema $x+y=3$, $\\ 2x+2y=6$?", en: "What kind of system is $x+y=3$, $\\ 2x+2y=6$?" },
      o: [{ va: "Compatible determinat", es: "Compatible determinado", en: "One solution" }, { va: "Compatible indeterminat", es: "Compatible indeterminado", en: "Infinitely many solutions" }, { va: "Incompatible", es: "Incompatible", en: "No solution" }], a: 1,
      e: { va: "La segona és la primera multiplicada per 2: són la mateixa recta. $\\frac12=\\frac12=\\frac36$.", es: "La segunda es la primera multiplicada por 2: son la misma recta. $\\frac12=\\frac12=\\frac36$.", en: "The second is the first times 2: they're the same line. $\\frac12=\\frac12=\\frac36$." } },
    { q: { va: "Com és el sistema $2x-y=1$, $\\ 4x-2y=5$?", es: "¿Cómo es el sistema $2x-y=1$, $\\ 4x-2y=5$?", en: "What kind of system is $2x-y=1$, $\\ 4x-2y=5$?" },
      o: [{ va: "Compatible determinat", es: "Compatible determinado", en: "One solution" }, { va: "Compatible indeterminat", es: "Compatible indeterminado", en: "Infinitely many solutions" }, { va: "Incompatible", es: "Incompatible", en: "No solution" }], a: 2,
      e: { va: "$\\frac24=\\frac{-1}{-2}\\neq\\frac15$: rectes paral·leles, cap solució.", es: "$\\frac24=\\frac{-1}{-2}\\neq\\frac15$: rectas paralelas, ninguna solución.", en: "$\\frac24=\\frac{-1}{-2}\\neq\\frac15$: parallel lines, no solution." } },
    { q: { va: "Resolent un sistema arribem a $0x=7$. El sistema…", es: "Resolviendo un sistema llegamos a $0x=7$. El sistema…", en: "Solving a system we reach $0x=7$. The system…" },
      o: [{ va: "té la solució $x=7$", es: "tiene la solución $x=7$", en: "has the solution $x=7$" }, { va: "té infinites solucions", es: "tiene infinitas soluciones", en: "has infinitely many solutions" }, { va: "no té solució", es: "no tiene solución", en: "has no solution" }], a: 2,
      e: { va: "Cap nombre multiplicat per 0 dona 7: és incompatible. (Si arribàrem a $0x=0$, seria compatible indeterminat.)", es: "Ningún número multiplicado por 0 da 7: es incompatible. (Si llegáramos a $0x=0$, sería compatible indeterminado.)", en: "No number times 0 gives 7: no solution. (If we reached $0x=0$, there would be infinitely many.)" } },
    { q: { va: "Quin és el primer pas per a resoldre $\\frac{x}{2}+\\frac{y}{3}=2$, $\\ x-y=-1$?", es: "¿Cuál es el primer paso para resolver $\\frac{x}{2}+\\frac{y}{3}=2$, $\\ x-y=-1$?", en: "What's the first step to solve $\\frac{x}{2}+\\frac{y}{3}=2$, $\\ x-y=-1$?" },
      o: [{ va: "Multiplicar la primera per 6", es: "Multiplicar la primera por 6", en: "Multiply the first by 6" }, { va: "Sumar les dues equacions", es: "Sumar las dos ecuaciones", en: "Add the two equations" }, { va: "Multiplicar la primera per 5", es: "Multiplicar la primera por 5", en: "Multiply the first by 5" }], a: 0,
      e: { va: "Traiem denominadors amb el m.c.m.(2, 3) = 6: $3x+2y=12$. Després, per exemple, substitució: $x=2,\\ y=3$.", es: "Quitamos denominadores con el m.c.m.(2, 3) = 6: $3x+2y=12$. Después, por ejemplo, sustitución: $x=2,\\ y=3$.", en: "Clear denominators with LCM(2, 3) = 6: $3x+2y=12$. Then, say, substitution: $x=2,\\ y=3$." } },
    { q: { va: "«Dos nombres sumen 20 i la seua diferència és 4». El sistema és…", es: "«Dos números suman 20 y su diferencia es 4». El sistema es…", en: "“Two numbers add up to 20 and their difference is 4”. The system is…" },
      o: [{ va: "$x+y=20,\\ \\ xy=4$" }, { va: "$x+y=20,\\ \\ x-y=4$" }, { va: "$x+y=4,\\ \\ x-y=20$" }, { va: "$x-y=20,\\ \\ x=4y$" }], a: 1,
      e: { va: "Sumant les dues: $2x=24$, $x=12$ i $y=8$.", es: "Sumando las dos: $2x=24$, $x=12$ e $y=8$.", en: "Adding them: $2x=24$, $x=12$ and $y=8$." } },
    { q: { va: "En un corral hi ha 10 animals, entre gallines i conills, i 28 potes. Quantes gallines hi ha?", es: "En un corral hay 10 animales, entre gallinas y conejos, y 28 patas. ¿Cuántas gallinas hay?", en: "A pen holds 10 animals, hens and rabbits, with 28 legs. How many hens are there?" },
      o: [{ va: "4" }, { va: "6" }, { va: "5" }, { va: "7" }], a: 1,
      e: { va: "$x+y=10,\\ 2x+4y=28\\Rightarrow x=6$ gallines i $y=4$ conills ($12+16=28$ ✓).", es: "$x+y=10,\\ 2x+4y=28\\Rightarrow x=6$ gallinas e $y=4$ conejos ($12+16=28$ ✓).", en: "$x+y=10,\\ 2x+4y=28\\Rightarrow x=6$ hens and $y=4$ rabbits ($12+16=28$ ✓)." } }
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

  var TITLES = { va: "Sistemes d'equacions · FentMates", es: "Sistemas de ecuaciones · FentMates", en: "Simultaneous equations · FentMates" };
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
    wLine(); wPair(); document.querySelectorAll(".w-solve").forEach(solverWidget); document.querySelectorAll(".w-graf").forEach(wGraf);
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
