(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-3eso-u5-done", NSEC = 7;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc",
      bad: "No entenc l'equació. Ha de tindre un signe = i una sola lletra: exemple 3(x-2)=x+4.",
      set: "Escriu les solucions separades per punt i coma (3; -2) o «cap» si no en té.", num: "Escriu un nombre.", sol: "Solució:" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro",
      bad: "No entiendo la ecuación. Debe tener un signo = y una sola letra: ejemplo 3(x-2)=x+4.",
      set: "Escribe las soluciones separadas por punto y coma (3; -2) o «ninguna» si no tiene.", num: "Escribe un número.", sol: "Solución:" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Score", right: "Correct!", wrong: "Not correct.", theme: "Switch between light and dark mode",
      bad: "I can't read that equation. It needs an = sign and a single letter: e.g. 3(x-2)=x+4.",
      set: "Type the solutions separated by semicolons (3; -2), or “none” if there are none.", num: "Type a number.", sol: "Solution:" }
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
  function readEq(raw) {
    var s = clean(raw), k = s.split("=");
    if (k.length !== 2 || !k[0] || !k[1]) return null;
    var Lp = parse(k[0]), Rp = parse(k[1]);
    if (!Lp || !Rp || negExp(Lp) || negExp(Rp)) return null;
    var vs = pvars(padd(Lp, Rp)); if (vs.length > 1) return null;
    return { ls: k[0], rs: k[1], L: Lp, R: Rp, v: vs[0] || "x" };
  }
  function cof(p, v, k) { var key = mkey(VE(v, k)); return p[key] ? p[key].c : rat(0); }
  function sumT(arr, v, k) { return arr.length ? arr.map(function (c, i) { return ttex(mono(c, VE(v, k)), i === 0); }).join("") : "0"; }
  function lin(A, v) { return A.n ? ttex(mono(A, VE(v, 1)), true) : "0" + v; }

  /* ---------- pas 1: denominadors i parèntesis ---------- */
  function prepare(E) {
    var rows = [], both = E.ls + "=" + E.rs, re = /\/(\d+)/g, mm, m = 1;
    while ((mm = re.exec(both))) m = lcm(m, parseInt(mm[1], 10));
    [E.L, E.R].forEach(function (p) { for (var k in p) m = lcm(m, p[k].c.d); });
    rows.push(tex(texRaw(E.ls) + "=" + texRaw(E.rs), true));
    var Lp = E.L, Rp = E.R;
    if (m > 1) {
      Lp = pscale(Lp, rat(m)); Rp = pscale(Rp, rat(m));
      var ml = mulSide(E.ls, m), mr = mulSide(E.rs, m);
      rows.push(fill(T(L3("Eliminem els denominadors: multipliquem <b>tots</b> els termes dels dos membres pel {m} (dividim el m.c.m. entre cada denominador i el resultat multiplica el numerador).", "Eliminamos los denominadores: multiplicamos <b>todos</b> los términos de los dos miembros por el {m} (dividimos el m.c.m. entre cada denominador y el resultado multiplica al numerador).", "Clear the denominators: multiply <b>every</b> term on both sides by the {m} (divide the LCM by each denominator and multiply the numerator by the result).")), { m: tex("\\text{m.c.m.}=" + m) })
        + tex(ml && mr ? ml + "=" + mr : ptex(Lp) + "=" + ptex(Rp), true));
      if (ml && mr && /[(]/.test(ml + mr)) rows.push(T(L3("Traiem parèntesis i reduïm cada membre:", "Quitamos paréntesis y reducimos cada miembro:", "Remove brackets and simplify each side:")) + tex(ptex(Lp) + "=" + ptex(Rp), true));
      else if (ml && mr && ml + "=" + mr !== ptex(Lp) + "=" + ptex(Rp)) rows.push(T(L3("Reduïm cada membre:", "Reducimos cada miembro:", "Simplify each side:")) + tex(ptex(Lp) + "=" + ptex(Rp), true));
    } else {
      var tl = topTerms(E.ls), tr = topTerms(E.rs);
      if (/[()\[\]{}]/.test(both) || !tl || !tr || tl.length !== Math.max(1, terms(E.L).length) || tr.length !== Math.max(1, terms(E.R).length))
        rows.push(T(L3("Traiem parèntesis i reduïm cada membre:", "Quitamos paréntesis y reducimos cada miembro:", "Remove brackets and simplify each side:")) + tex(ptex(Lp) + "=" + ptex(Rp), true));
    }
    return { rows: rows, L: Lp, R: Rp, v: E.v };
  }
  /* tot al primer membre, coeficient principal positiu i simplificat */
  function toStd(pre, rows) {
    var P = psub(pre.L, pre.R);
    if (!isZero(pre.R)) rows.push(T(L3("Passem tots els termes al primer membre i reduïm:", "Pasamos todos los términos al primer miembro y reducimos:", "Move every term to the left and simplify:")) + tex(ptex(P) + "=0", true));
    var a = coeffs(P).a;
    if (a[a.length - 1].n < 0) { P = pneg(P); rows.push(T(L3("Multipliquem per −1 (canviem tots els signes) perquè el primer coeficient siga positiu:", "Multiplicamos por −1 (cambiamos todos los signos) para que el primer coeficiente sea positivo:", "Multiply by −1 (change every sign) so the leading coefficient is positive:")) + tex(ptex(P) + "=0", true)); }
    var g = 0; for (var k in P) g = gcd(g, P[k].c.n);
    if (g > 1) { P = pscale(P, rat(1, g)); rows.push(fill(T(L3("Simplifiquem: dividim tots els termes entre {g}:", "Simplificamos: dividimos todos los términos entre {g}:", "Simplify: divide every term by {g}:")), { g: g }) + tex(ptex(P) + "=0", true)); }
    return P;
  }

  /* ---------- primer grau ---------- */
  function linSolve(pre, E, rows) {
    var v = pre.v, a1 = cof(pre.L, v, 1), b1 = cof(pre.L, v, 0), a2 = cof(pre.R, v, 1), b2 = cof(pre.R, v, 0);
    var A = rsub(a1, a2), B = rsub(b2, b1);
    if (a2.n || b1.n) {
      var xs = [], ns = [];
      if (a1.n) xs.push(a1); if (a2.n) xs.push(rneg(a2)); if (b2.n) ns.push(b2); if (b1.n) ns.push(rneg(b1));
      rows.push(fill(T(L3("Transposem: els termes amb {v} al primer membre i els nombres al segon (el que suma passa restant i el que resta passa sumant):", "Transponemos: los términos con {v} al primer miembro y los números al segundo (lo que suma pasa restando y lo que resta pasa sumando):", "Rearrange: {v} terms on the left and numbers on the right (what is added moves across subtracted, and vice versa):")), { v: tex(v) }) + tex(sumT(xs, v, 1) + "=" + sumT(ns, v, 0), true));
      rows.push(T(L3("Reduïm:", "Reducimos:", "Simplify:")) + " " + tex(lin(A, v) + "=" + nt(B)));
    }
    if (!A.n) {
      rows.push(B.n ? fill(T(L3("Cap nombre multiplicat per 0 dona {b}: l'equació <b>no té solució</b>.", "Ningún número multiplicado por 0 da {b}: la ecuación <b>no tiene solución</b>.", "No number times 0 gives {b}: the equation has <b>no solution</b>.")), { b: tex(nt(B)) })
        : T(L3("Qualsevol nombre multiplicat per 0 dona 0: <b>infinites solucions</b> (és una identitat).", "Cualquier número multiplicado por 0 da 0: <b>infinitas soluciones</b> (es una identidad).", "Any number times 0 gives 0: <b>infinitely many solutions</b> (it's an identity).")));
      return B.n ? { sols: [] } : { all: true };
    }
    var s = rdiv(B, A);
    if (!(A.n === 1 && A.d === 1)) rows.push(fill(T(L3("Aïllem la {v}: el {a} que multiplica passa dividint.", "Despejamos la {v}: el {a} que multiplica pasa dividiendo.", "Isolate {v}: the {a} multiplying moves across dividing.")), { v: tex(v), a: tex(nt(A)) }) + tex(v + "=\\frac{" + nt(B) + "}{" + nt(A) + "}" + (A.n > 0 && B.d === 1 && gcd(B.n, A.n) === 1 ? "" : "=" + nt(s)), true));
    var o = {}; o[v] = s;
    rows.push(T(L3("Comprovació:", "Comprobación:", "Check:")) + " " + tex(substRaw(E.ls, v, s) + "=" + nt(evalAt(E.L, o))) + " ; " + tex(substRaw(E.rs, v, s) + "=" + nt(evalAt(E.R, o))) + " ✓");
    return { sols: [{ r: s }] };
  }

  /* ---------- segon grau: A, B, C enters ---------- */
  function sqrtSplit(n) { var k = 1, m = n; for (var f = 2; f * f <= m; f++) while (m % (f * f) === 0) { m /= f * f; k *= f; } return [k, m]; }
  function ip(n) { return n < 0 ? "(" + n + ")" : String(n); }
  function quad(A, B, C, v, rows) {
    var P2 = fromC([rat(C), rat(B), rat(A)], v);
    if (A < 0) { A = -A; B = -B; C = -C; P2 = pneg(P2); rows.push(T(L3("Canviem tots els signes perquè a siga positiu:", "Cambiamos todos los signos para que a sea positivo:", "Change every sign so that a is positive:")) + tex(ptex(P2) + "=0", true)); }
    if (B === 0 && C === 0) { rows.push(tex(ptex(P2) + "=0\\ \\Rightarrow\\ " + v + "^2=0\\ \\Rightarrow\\ " + v + "=0", true)); return [{ r: rat(0), dbl: true }]; }
    if (B === 0) {
      var q = rat(-C, A);
      rows.push(fill(T(L3("És <b>incompleta</b> (b = 0): aïllem {x2} i fem l'arrel quadrada (dues arrels: positiva i negativa).", "Es <b>incompleta</b> (b = 0): despejamos {x2} y hacemos la raíz cuadrada (dos raíces: positiva y negativa).", "It's <b>incomplete</b> (b = 0): isolate {x2} and take the square root (two roots: positive and negative).")), { x2: tex(v + "^2") })
        + tex(A === 1 ? v + "^2=" + nt(q) : A + v + "^2=" + (-C) + "\\ \\Rightarrow\\ " + v + "^2=" + (gcd(C, A) === 1 ? "" : "\\frac{" + (-C) + "}{" + A + "}=") + nt(q), true));
      if (q.n < 0) { rows.push(T(L3("Cap nombre al quadrat dona un resultat negatiu: <b>no té solució</b>.", "Ningún número al cuadrado da un resultado negativo: <b>no tiene solución</b>.", "No square is negative: <b>no solution</b>."))); return []; }
      var sp = sqrtSplit(q.n * q.d), k = rat(sp[0], q.d);
      if (sp[1] === 1) { rows.push(tex(v + "=\\pm\\sqrt{" + nt(q) + "}=\\pm" + nt(k), true)); return [{ r: k }, { r: rneg(k) }]; }
      var rt = "\\frac{" + (k.n === 1 ? "" : k.n) + "\\sqrt{" + sp[1] + "}}{" + k.d + "}";
      if (k.d === 1) rt = (k.n === 1 ? "" : k.n) + "\\sqrt{" + sp[1] + "}";
      rows.push(tex(v + "=\\pm\\sqrt{" + nt(q) + "}" + (rt === "\\sqrt{" + nt(q) + "}" ? "" : "=\\pm" + rt) + "\\approx\\pm" + dec(Math.sqrt(q.n / q.d)), true));
      return [{ t: rt, val: Math.sqrt(q.n / q.d) }, { t: "-" + rt, val: -Math.sqrt(q.n / q.d) }];
    }
    if (C === 0) {
      var L1 = fromC([rat(B), rat(A)], v), r0 = rat(-B, A);
      rows.push(fill(T(L3("És <b>incompleta</b> (c = 0): traiem factor comú {v} i igualem cada factor a 0.", "Es <b>incompleta</b> (c = 0): sacamos factor común {v} e igualamos cada factor a 0.", "It's <b>incomplete</b> (c = 0): take out the common factor {v} and set each factor to 0.")), { v: tex(v) })
        + tex(v + "\\,(" + ptex(L1) + ")=0\\ \\Rightarrow\\ \\begin{cases}" + v + "=0\\\\ " + ptex(L1) + "=0\\ \\Rightarrow\\ " + v + "=" + nt(r0) + "\\end{cases}", true));
      return [{ r: rat(0) }, { r: r0 }];
    }
    rows.push(fill(T(L3("És <b>completa</b>: {abc}. Apliquem la fórmula:", "Es <b>completa</b>: {abc}. Aplicamos la fórmula:", "It's <b>complete</b>: {abc}. Use the formula:")), { abc: tex("a=" + A + ",\\ b=" + B + ",\\ c=" + C) }));
    var D = B * B - 4 * A * C, den = 2 * A;
    rows.push(tex(v + "=\\frac{-b\\pm\\sqrt{b^2-4ac}}{2a}=\\frac{-" + ip(B) + "\\pm\\sqrt{" + ip(B) + "^2-4\\cdot" + ip(A) + "\\cdot" + ip(C) + "}}{2\\cdot" + ip(A) + "}=\\frac{" + (-B) + "\\pm\\sqrt{" + D + "}}{" + den + "}", true));
    rows.push(fill(T(L3("Discriminant: {d}", "Discriminante: {d}", "Discriminant: {d}")), { d: tex("\\Delta=" + D + (D > 0 ? ">0" : D < 0 ? "<0" : "")) }) + " → "
      + (D > 0 ? T(L3("dues solucions.", "dos soluciones.", "two solutions.")) : D === 0 ? T(L3("una solució (doble).", "una solución (doble).", "one (double) solution.")) : T(L3("l'arrel d'un nombre negatiu no existeix: <b>no té solució</b>.", "la raíz de un número negativo no existe: <b>no tiene solución</b>.", "a negative number has no square root: <b>no solution</b>."))));
    if (D < 0) return [];
    if (D === 0) { var rr = rat(-B, den); rows.push(tex(v + "=\\frac{" + (-B) + "}{" + den + "}" + (rr.d === den && rr.n === -B ? "" : "=" + nt(rr)), true)); return [{ r: rr, dbl: true }]; }
    var s = isqrt(D);
    if (s >= 0) {
      var r1 = rat(-B + s, den), r2 = rat(-B - s, den);
      function one(n, r) { return "\\frac{" + n + "}{" + den + "}" + (r.d === den && r.n === n ? "" : "=" + nt(r)); }
      rows.push(tex(v + "=\\frac{" + (-B) + "\\pm" + s + "}{" + den + "}\\ \\Rightarrow\\ \\begin{cases}" + v + "_1=" + one(-B + s, r1) + "\\\\ " + v + "_2=" + one(-B - s, r2) + "\\end{cases}", true));
      return [{ r: r1 }, { r: r2 }];
    }
    var ks = sqrtSplit(D), k2 = ks[0], m = ks[1], g = gcd(gcd(Math.abs(B), k2), den);
    var line = v + "=\\frac{" + (-B) + "\\pm\\sqrt{" + D + "}}{" + den + "}";
    var fin = "\\frac{" + (-B) + "\\pm" + (k2 === 1 ? "" : k2) + "\\sqrt{" + m + "}}{" + den + "}";
    if (k2 > 1) line += "=" + fin;
    if (g > 1) { var nm = (-B / g) + "\\pm" + (k2 / g === 1 ? "" : k2 / g) + "\\sqrt{" + m + "}"; fin = den / g === 1 ? nm : "\\frac{" + nm + "}{" + den / g + "}"; line += "=" + fin; }
    var x1 = (-B + Math.sqrt(D)) / den, x2 = (-B - Math.sqrt(D)) / den;
    rows.push(tex(line, true));
    rows.push(T(L3("Com que el discriminant no és un quadrat perfecte, les solucions són <b>irracionals</b>:", "Como el discriminante no es un cuadrado perfecto, las soluciones son <b>irracionales</b>:", "Since the discriminant isn't a perfect square, the solutions are <b>irrational</b>:")) + " " + tex(v + "_1\\approx " + dec(x1) + ",\\quad " + v + "_2\\approx " + dec(x2)));
    return [{ t: fin.replace("\\pm", "+"), val: x1 }, { t: fin.replace("\\pm", "-"), val: x2 }];
  }
  /* coeficients racionals -> enters (multiplicant pel m.c.m.) */
  function intC(a) { var m = 1; a.forEach(function (c) { m = lcm(m, c.d); }); return { m: m, a: a.map(function (c) { return c.n * (m / c.d); }) }; }

  /* ---------- grau 3 o 4: Ruffini ---------- */
  function ruffini(a, r) { var n = a.length - 1, b = [], mid = []; var acc = rat(0); for (var k = n; k >= 0; k--) { var m = k === n ? null : rmul(acc, r); var s = m ? radd(a[k], m) : a[k]; mid.push(m); b.push(s); acc = s; } return { mid: mid, b: b }; }
  function divisors(n) { n = Math.abs(n); var d = []; for (var i = 1; i <= n; i++) if (n % i === 0) d.push(i); return d; }
  function rufTable(a, r) {
    var n = a.length - 1, R = ruffini(a, r), k, h = '<div class="tbl-wrap"><table class="ruf"><tbody><tr><td class="ra"></td>';
    for (k = n; k >= 0; k--) h += "<td" + (k === 0 ? ' class="rl"' : "") + ">" + tex(nt(a[k])) + "</td>";
    h += '</tr><tr><td class="ra">' + tex(nt(r)) + "</td>";
    for (k = 0; k <= n; k++) h += '<td class="m' + (k === n ? " rl" : "") + '">' + (k > 0 ? tex(nt(R.mid[k])) : "") + "</td>";
    h += '</tr><tr class="rb"><td class="ra"></td>';
    for (k = 0; k <= n; k++) h += '<td class="' + (k === n ? "rl rr" : "") + '">' + tex(nt(R.b[k])) + "</td>";
    return h + "</tr></tbody></table></div>";
  }
  var ORBE = "\\ \\tri{o bé}{o bien}{or}\\ ";
  function polySolve(P, v, rows) {
    var a = coeffs(P).a, sols = [];
    while (a.length - 1 > 2) {
      var n = a.length - 1;
      if (!a[0].n) {
        var Q = fromC(a.slice(1), v);
        rows.push(fill(T(L3("No hi ha terme independent: traiem factor comú {v}.", "No hay término independiente: sacamos factor común {v}.", "There's no constant term: take out the common factor {v}.")), { v: tex(v) })
          + tex(v + "\\,(" + ptex(Q) + ")=0\\ \\Rightarrow\\ " + v + "=0" + ORBE + ptex(Q) + "=0", true));
        sols.push({ r: rat(0) }); a = a.slice(1); continue;
      }
      var I = intC(a); if (I.m > 1) { a = I.a.map(function (c) { return rat(c); }); rows.push(fill(T(L3("Multipliquem per {m} per a treballar amb coeficients enters:", "Multiplicamos por {m} para trabajar con coeficientes enteros:", "Multiply by {m} to work with whole-number coefficients:")), { m: I.m }) + tex(ptex(fromC(a, v)) + "=0", true)); }
      var c0 = a[0].n, lead = Math.abs(a[n].n), ds = divisors(c0), cands = [];
      ds.forEach(function (d) { cands.push(rat(d), rat(-d)); });
      if (lead > 1) divisors(lead).forEach(function (q) { if (q > 1) ds.forEach(function (p) { if (gcd(p, q) === 1) cands.push(rat(p, q), rat(-p, q)); }); });
      var Pp = fromC(a, v), tried = [], root = null;
      for (var i = 0; i < cands.length && !root; i++) {
        var o = {}; o[v] = cands[i]; var val = evalAt(Pp, o);
        tried.push(tex("P(" + nt(cands[i]) + ")=" + nt(val)));
        if (!val.n) root = cands[i];
      }
      rows.push(fill(T(L3("Busquem una solució entre els divisors del terme independent, {c}: {ds}.", "Buscamos una solución entre los divisores del término independiente, {c}: {ds}.", "Look for a solution among the divisors of the constant term, {c}: {ds}.")), { c: tex(nt(a[0])), ds: tex(ds.map(function (d) { return "\\pm" + d; }).join(",\\ ")) })
        + (lead > 1 ? " " + fill(T(L3("Com que el primer coeficient és {l}, també podem provar fraccions {pq} amb {q} divisor de {l}.", "Como el primer coeficiente es {l}, también podemos probar fracciones {pq} con {q} divisor de {l}.", "Since the leading coefficient is {l}, we can also try fractions {pq} with {q} a divisor of {l}.")), { l: lead, pq: tex("\\pm\\frac{p}{q}"), q: tex("q") }) : ""));
      if (!root) {
        rows.push(tried.join(", ") + " " + warn(T(L3("Cap d'aquests valors és solució: aquesta equació no es pot resoldre amb Ruffini (no té solucions racionals).", "Ninguno de estos valores es solución: esta ecuación no se puede resolver con Ruffini (no tiene soluciones racionales).", "None of these values is a solution: this equation can't be solved with Ruffini's rule (it has no rational solutions)."))));
        return { sols: sols, stuck: true };
      }
      rows.push(T(L3("Provem:", "Probamos:", "Try:")) + " " + tried.join(", ") + " ✓");
      var R = ruffini(a, root), q = R.b.slice(0, n).reverse(), Qp = fromC(q, v), bin = fromC([rneg(root), rat(1)], v);
      rows.push(fill(T(L3("Dividim per Ruffini entre {b}:", "Dividimos por Ruffini entre {b}:", "Divide by {b} with Ruffini's rule:")), { b: tex(ptex(bin)) }) + rufTable(a, root)
        + tex("(" + ptex(bin) + ")(" + ptex(Qp) + ")=0\\ \\Rightarrow\\ " + v + "=" + nt(root) + ORBE + ptex(Qp) + "=0", true));
      sols.push({ r: root }); a = q;
    }
    if (a.length - 1 === 2) {
      rows.push(fill(T(L3("Resolem l'equació de segon grau que queda, {e}:", "Resolvemos la ecuación de segundo grado que queda, {e}:", "Solve the quadratic that's left, {e}:")), { e: tex(ptex(fromC(a, v)) + "=0") }));
      var J = intC(a); sols = sols.concat(quad(J.a[2], J.a[1], J.a[0], v, rows));
    } else if (a.length - 1 === 1) sols.push({ r: rdiv(rneg(a[0]), a[1]) });
    return { sols: sols };
  }
  /* llista final de solucions (amb les dobles marcades) */
  function solsTex(sols, v) {
    var u2 = [];
    sols.forEach(function (s) {
      var f = u2.filter(function (x) { return s.r && x.r ? req(s.r, x.r) : (s.t && x.t === s.t); })[0];
      if (f) f.n++; else u2.push({ r: s.r, t: s.t, val: s.val, n: s.dbl ? 2 : 1 });
    });
    u2.sort(function (p, q) { return (p.r ? p.r.n / p.r.d : p.val) - (q.r ? q.r.n / q.r.d : q.val); });
    return u2.map(function (s) { return v + "=" + (s.r ? nt(s.r) : s.t) + (s.n === 2 ? "\\ (\\tri{doble}{doble}{double})" : s.n === 3 ? "\\ (\\tri{triple}{triple}{triple})" : ""); }).join(",\\quad ");
  }
  /* resol qualsevol equació polinòmica (fins a grau 4) */
  function solveAny(E) {
    var pre = prepare(E), rows = pre.rows, v = pre.v, diff = psub(pre.L, pre.R), deg = pdeg(diff), res;
    if (isZero(diff)) {
      rows.push(T(L3("Els dos membres són iguals: és una <b>identitat</b> i qualsevol nombre n'és solució.", "Los dos miembros son iguales: es una <b>identidad</b> y cualquier número es solución.", "Both sides are the same: it's an <b>identity</b> and every number is a solution.")));
      return { rows: rows, all: true, deg: 0 };
    }
    if (deg <= 1) { res = linSolve(pre, E, rows); return { rows: rows, sols: res.sols, all: res.all, deg: 1 }; }
    if (deg > 4) { rows.push(warn(T(L3("Aquesta eina resol equacions fins a grau 4.", "Esta herramienta resuelve ecuaciones hasta grado 4.", "This tool solves equations up to degree 4.")))); return { rows: rows, deg: deg }; }
    var P = toStd(pre, rows), sols;
    if (deg === 2) { var a = coeffs(P).a.map(function (c) { return c.n; }); sols = quad(a[2], a[1], a[0], v, rows); }
    else { var r = polySolve(P, v, rows); sols = r.sols; if (r.stuck) return { rows: rows, deg: deg, stuck: true }; }
    rows.push((sols.length ? T(L3("Solucions:", "Soluciones:", "Solutions:")) + " " + tex("\\boxed{" + solsTex(sols, v) + "}") : T(L3("L'equació <b>no té solució</b>.", "La ecuación <b>no tiene solución</b>.", "The equation has <b>no solution</b>."))));
    return { rows: rows, sols: sols, deg: deg };
  }
  function solverWidget(id, want) {
    var w = document.getElementById(id); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      var E = readEq(I.e.value); info.innerHTML = "";
      if (!E) { out.innerHTML = ""; info.innerHTML = warn(u("bad")); return; }
      var R = solveAny(E);
      out.innerHTML = rows2html(R.rows);
      if (want && R.deg && R.deg !== want && !R.all) info.innerHTML = "💡 " + fill(T(L3("Un cop reduïda, aquesta equació és de grau {d}.", "Una vez reducida, esta ecuación es de grado {d}.", "Once simplified, this equation has degree {d}.")), { d: R.deg });
    }
    I.e.addEventListener("input", paint);
    quickBind(w, function (v) { I.e.value = v[0]; paint(); });
    onLang(paint);
  }

  /* ---------- giny: és solució? ---------- */
  function wCheck() {
    var w = document.getElementById("w-check"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      var E = readEq(I.e.value), q = parse(clean(I.x.value)); info.innerHTML = "";
      if (!E) { out.innerHTML = ""; info.innerHTML = warn(u("bad")); return; }
      if (!q || !isConst(q)) { out.innerHTML = ""; info.innerHTML = warn(u("num")); return; }
      var r = cval(q), v = E.v, o = {}; o[v] = r;
      var vl = evalAt(E.L, o), vr = evalAt(E.R, o), ok = req(vl, vr), diff = psub(E.L, E.R), rows = [];
      rows.push(fill(T(L3("Substituïm {x} en cada membre:", "Sustituimos {x} en cada miembro:", "Substitute {x} into each side:")), { x: tex(v + "=" + nt(r)) }));
      rows.push(T(L3("1r membre:", "1.er miembro:", "Left side:")) + " " + tex(substRaw(E.ls, v, r) + "=" + nt(vl)));
      rows.push(T(L3("2n membre:", "2.º miembro:", "Right side:")) + " " + tex(substRaw(E.rs, v, r) + "=" + nt(vr)));
      rows.push(ok ? '<span class="ok">✓ ' + fill(T(L3("Els dos membres valen el mateix: {x} <b>és solució</b>.", "Los dos miembros valen lo mismo: {x} <b>es solución</b>.", "Both sides are equal: {x} <b>is a solution</b>.")), { x: tex(v + "=" + nt(r)) }) + "</span>"
        : '<span class="ko">✗ ' + fill(T(L3("{a}: {x} <b>no és solució</b>.", "{a}: {x} <b>no es solución</b>.", "{a}: {x} <b>isn't a solution</b>.")), { a: tex(nt(vl) + "\\neq" + nt(vr)), x: tex(v + "=" + nt(r)) }) + "</span>");
      out.innerHTML = rows2html(rows);
      info.innerHTML = isZero(diff) ? "💡 " + T(L3("A més, els dos membres són iguals un cop operats: és una <b>identitat</b>, i qualsevol valor és solució.", "Además, los dos miembros son iguales una vez operados: es una <b>identidad</b>, y cualquier valor es solución.", "What's more, both sides are the same once worked out: it's an <b>identity</b>, so every value is a solution."))
        : "💡 " + fill(T(L3("És una equació de grau {d} (un cop reduïda).", "Es una ecuación de grado {d} (una vez reducida).", "It's an equation of degree {d} (once simplified).")), { d: pdeg(diff) });
    }
    [I.e, I.x].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.e.value = v[0]; I.x.value = v[1]; paint(); });
    onLang(paint);
  }

  /* ---------- giny: discriminant i paràbola ---------- */
  function wDisc() {
    var w = document.getElementById("w-disc"); if (!w) return;
    var rs = {}; w.querySelectorAll('input[type="range"]').forEach(function (r) { rs[r.dataset.k] = r; });
    var eq = w.querySelector(".disc-eq"), svg = w.querySelector(".parab"), info = w.querySelector(".info");
    var W = 340, H = 260, X0 = -7, X1 = 7, Y0 = -10, Y1 = 10;
    function sx(x) { return (x - X0) / (X1 - X0) * W; }
    function sy(y) { return H - (y - Y0) / (Y1 - Y0) * H; }
    function paint() {
      var a = +rs.a.value, b = +rs.b.value, c = +rs.c.value;
      w.querySelectorAll(".rv").forEach(function (s) { s.textContent = rs[s.dataset.v].value; });
      var g = "", k;
      for (k = X0; k <= X1; k++) g += '<line class="grid" x1="' + sx(k) + '" y1="0" x2="' + sx(k) + '" y2="' + H + '"/>';
      for (k = Y0; k <= Y1; k += 2) g += '<line class="grid" x1="0" y1="' + sy(k) + '" x2="' + W + '" y2="' + sy(k) + '"/>';
      g += '<line class="ax" x1="0" y1="' + sy(0) + '" x2="' + W + '" y2="' + sy(0) + '"/><line class="ax" x1="' + sx(0) + '" y1="0" x2="' + sx(0) + '" y2="' + H + '"/>';
      for (k = X0 + 1; k < X1; k++) if (k) g += '<text class="tk" x="' + sx(k) + '" y="' + (sy(0) + 13) + '" text-anchor="middle">' + k + "</text>";
      var d = "", pen = false;
      for (var x = X0; x <= X1 + 1e-9; x += 0.05) {
        var y = a * x * x + b * x + c;
        if (y < Y0 - 2 || y > Y1 + 2) { pen = false; continue; }
        d += (pen ? "L" : "M") + sx(x).toFixed(1) + " " + sy(y).toFixed(1); pen = true;
      }
      g += '<path class="curve" d="' + d + '"/>';
      var P2 = fromC([rat(c), rat(b), rat(a)], "x"), D = b * b - 4 * a * c, roots = [], msg;
      if (a === 0) {
        eq.innerHTML = tex(ptex(P2) + "=0");
        info.innerHTML = warn(T(L3("Si a = 0 no és una equació de segon grau (la gràfica és una recta).", "Si a = 0 no es una ecuación de segundo grado (la gráfica es una recta).", "If a = 0 it isn't a quadratic (the graph is a straight line).")));
        if (b) roots.push(-c / b);
      } else {
        if (D > 0) roots = [(-b - Math.sqrt(D)) / (2 * a), (-b + Math.sqrt(D)) / (2 * a)]; else if (D === 0) roots = [-b / (2 * a)];
        msg = D > 0 ? T(L3("<b>dues solucions</b>: la paràbola talla l'eix X en dos punts.", "<b>dos soluciones</b>: la parábola corta al eje X en dos puntos.", "<b>two solutions</b>: the parabola crosses the x-axis twice.")) : D === 0 ? T(L3("<b>una solució</b> (doble): la paràbola toca l'eix X en un sol punt, el vèrtex.", "<b>una solución</b> (doble): la parábola toca el eje X en un solo punto, el vértice.", "<b>one (double) solution</b>: the parabola just touches the x-axis at its vertex.")) : T(L3("<b>cap solució</b>: la paràbola no talla l'eix X.", "<b>ninguna solución</b>: la parábola no corta al eje X.", "<b>no solution</b>: the parabola doesn't meet the x-axis."));
        eq.innerHTML = tex(ptex(P2) + "=0") + "<br>" + tex("\\Delta=" + ip(b) + "^2-4\\cdot" + ip(a) + "\\cdot" + ip(c) + "=" + D) + " → " + msg;
        info.innerHTML = roots.length ? T(L3("Solucions: ", "Soluciones: ", "Solutions: ")) + roots.map(function (r) { return tex("x\\approx " + dec(r)); }).join(", ") : "";
      }
      roots.forEach(function (r) { if (r >= X0 && r <= X1) g += '<circle class="root" cx="' + sx(r) + '" cy="' + sy(0) + '" r="5"/>'; });
      svg.innerHTML = g;
    }
    Object.keys(rs).forEach(function (k) { rs[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  function pm(n) { return n < 0 ? "-" + (-n) : "+" + n; }
  function linStr(a, b) { var s = a ? (a === 1 ? "x" : a === -1 ? "-x" : a + "x") : ""; return b ? s + (s ? pm(b) : String(b)) : (s || "0"); }
  function polyS(asc) { return ptex(fromC(asc.map(function (c) { return rat(c); }), "x")); }
  function eqItem(s, ans) {
    return { set: true, str: s, ans: ans.map(function (r) { return typeof r === "number" ? rat(r) : r; }),
      q: function () { return T(L3("Resol:", "Resuelve:", "Solve:")) + " $" + texRaw(s) + "$"; },
      s: function () { return rows2html(solveAny(readEq(s)).rows.slice(1)); } };
  }
  var PROBS = [
    function () { var x = rint(5, 60), S = 3 * x + 3; return { ans: x, d: { S: S }, q: L3("La suma de tres nombres consecutius és {S}. Quin és el menor?", "La suma de tres números consecutivos es {S}. ¿Cuál es el menor?", "Three consecutive numbers add up to {S}. What is the smallest?"), e: "x+(x+1)+(x+2)=" + S + "\\ \\Rightarrow\\ 3x+3=" + S + "\\ \\Rightarrow\\ x=" + x }; },
    function () { var k = rint(2, 15), m = rint(2, 15), x = k + m; return { ans: x, d: { k: k, m: m }, q: L3("Si al triple d'un nombre li restem {k}, obtenim el mateix que si al seu doble li sumem {m}. Quin és el nombre?", "Si al triple de un número le restamos {k}, obtenemos lo mismo que si a su doble le sumamos {m}. ¿Cuál es el número?", "Three times a number minus {k} equals twice the number plus {m}. What is the number?"), e: "3x-" + k + "=2x+" + m + "\\ \\Rightarrow\\ x=" + x }; },
    function () { var F = rint(4, 14), y = rint(2, 20), M = 2 * F + y; return { ans: y, d: { M: M, F: F }, q: L3("Una mare té {M} anys i la seua filla {F}. D'ací a quants anys la mare tindrà el doble d'edat que la filla?", "Una madre tiene {M} años y su hija {F}. ¿Dentro de cuántos años la madre tendrá el doble de edad que la hija?", "A mother is {M} and her daughter is {F}. In how many years will the mother be twice as old as her daughter?"), e: M + "+x=2(" + F + "+x)\\ \\Rightarrow\\ " + M + "+x=" + 2 * F + "+2x\\ \\Rightarrow\\ x=" + y }; },
    function () { var h = rint(3, 20), d = rint(2, 9), P = 4 * h + 2 * d; return { ans: h, d: { d: d, P: P }, q: L3("La base d'un rectangle fa {d} cm més que l'altura i el perímetre és {P} cm. Quant fa l'altura (en cm)?", "La base de un rectángulo mide {d} cm más que la altura y el perímetro es {P} cm. ¿Cuánto mide la altura (en cm)?", "A rectangle's base is {d} cm longer than its height and its perimeter is {P} cm. How tall is it (in cm)?"), e: "2x+2(x+" + d + ")=" + P + "\\ \\Rightarrow\\ 4x+" + 2 * d + "=" + P + "\\ \\Rightarrow\\ x=" + h }; },
    function () { var x = rint(3, 12), N = x * x - 2 * x; return { ans: x, d: { N: N }, q: L3("El quadrat d'un nombre positiu menys el seu doble és {N}. Quin és el nombre?", "El cuadrado de un número positivo menos su doble es {N}. ¿Cuál es el número?", "The square of a positive number minus twice the number is {N}. What is the number?"), e: "x^2-2x-" + N + "=0\\ \\Rightarrow\\ x=\\frac{2\\pm" + (2 * x - 2) + "}{2}\\ \\Rightarrow\\ x=" + x + "\\ (" + (2 - x) + "\\ \\tri{no val}{no vale}{not valid})" }; },
    function () { var H = rint(10, 40), g = rint(1, H - 1), P = 2 * g + 4 * (H - g); return { ans: g, d: { H: H, P: P }, q: L3("En una granja hi ha gallines i conills: en total, {H} caps i {P} potes. Quantes gallines hi ha?", "En una granja hay gallinas y conejos: en total, {H} cabezas y {P} patas. ¿Cuántas gallinas hay?", "A farm has hens and rabbits: {H} heads and {P} legs in all. How many hens are there?"), e: "2x+4(" + H + "-x)=" + P + "\\ \\Rightarrow\\ " + (4 * H) + "-2x=" + P + "\\ \\Rightarrow\\ x=" + g }; },
    function () { var k = rint(1, 9), x = 6 * k, S = 11 * k; return { ans: x, d: { S: S }, q: L3("Un nombre més la seua meitat més la seua tercera part fan {S}. Quin és el nombre?", "Un número más su mitad más su tercera parte suman {S}. ¿Cuál es el número?", "A number plus half of it plus a third of it makes {S}. What is the number?"), e: "x+\\frac{x}{2}+\\frac{x}{3}=" + S + "\\ \\xrightarrow{\\cdot6}\\ 11x=" + 6 * S + "\\ \\Rightarrow\\ x=" + x }; }
  ];
  var GEN = {
    lin1: function () {
      var x0 = rnz(-9, 9), a1, a2; do { a1 = rnz(-6, 9); a2 = rint(-5, 6); } while (a1 === a2);
      var b1 = rint(-12, 12), b2 = (a1 - a2) * x0 + b1;
      return eqItem(linStr(a1, b1) + "=" + linStr(a2, b2), [x0]);
    },
    lin2: function () {
      var t = rint(0, 2), x0 = rnz(-8, 8), s, q, w;
      if (t === 0) {
        var p = rint(2, 5), r = rint(2, 4), a2 = rint(-3, 4); q = rnz(-6, 6); w = rnz(-6, 6);
        if (p - r === a2) a2++;
        s = p + "(x" + pm(q) + ")-" + r + "(x" + pm(w) + ")=" + linStr(a2, p * (x0 + q) - r * (x0 + w) - a2 * x0);
      } else if (t === 1) {
        var ds = pick([[2, 3], [3, 4], [2, 5], [4, 6], [3, 6], [2, 4], [3, 5]]), d1 = ds[0], d2 = ds[1];
        q = rnz(-5, 5); q -= mod(x0 + q, d1); w = rnz(-5, 5); w -= mod(x0 + w, d2);
        var n1 = q ? "(x" + pm(q) + ")" : "x", n2 = w ? "(x" + pm(w) + ")" : "x";
        s = n1 + "/" + d1 + "-" + n2 + "/" + d2 + "=" + ((x0 + q) / d1 - (x0 + w) / d2);
      } else {
        var e1 = rint(2, 5), e2; do { e2 = rint(2, 6); } while (e2 === e1);
        x0 = lcm(e1, e2) * rnz(-3, 4);
        s = "x/" + e1 + "+x/" + e2 + "=" + (x0 / e1 + x0 / e2);
      }
      return eqItem(s, [x0]);
    },
    inc: function () {
      var t = rint(0, 4), a = rint(1, 4), r;
      if (t === 0) { r = rint(1, 9); return eqItem(polyS([-a * r * r, 0, a]) + "=0", [r, -r]); }
      if (t === 1) { r = rnz(-9, 9); return eqItem(polyS([0, -a * r, a]) + "=0", [0, r]); }
      if (t === 2) { return eqItem(polyS([rint(1, 20), 0, a]) + "=0", []); }
      if (t === 3) { r = rint(1, 8); return eqItem((a === 1 ? "" : a) + "x^2=" + a * r * r, [r, -r]); }
      var p = rint(2, 5), q; do { q = rint(1, 7); } while (gcd(p, q) !== 1);
      return eqItem(polyS([-q * q, 0, p * p]) + "=0", [rat(q, p), rat(-q, p)]);
    },
    q2: function () {
      var co, ans;
      if (rint(0, 3) === 0) { var p = pick([1, 3, 5, -1, -3, -5]), r2; do { r2 = rnz(-6, 6); } while (p + 2 * r2 === 0); co = [p * r2, -(p + 2 * r2), 2]; ans = [rat(p, 2), rat(r2)]; }
      else { var a = pick([1, 1, 1, 2, 3, -1]), r1 = rnz(-7, 7), r3; do { r3 = rnz(-7, 7); } while (r1 + r3 === 0); co = [a * r1 * r3, -a * (r1 + r3), a]; ans = r1 === r3 ? [r1] : [r1, r3]; }
      var s = rint(0, 2) === 0 ? polyS([0, co[1], co[2]]) + "=" + (-co[0]) : polyS(co) + "=0";
      return eqItem(s, ans);
    },
    disc: function () {
      var a, b, c;
      if (rint(0, 2) === 0) { a = rint(1, 3); var r = rnz(-4, 4); b = -2 * a * r; c = a * r * r; }
      else do { a = rnz(-3, 3); b = rint(-7, 7); c = rnz(-8, 8); } while (b === 0);
      var D = b * b - 4 * a * c, n = D > 0 ? 2 : D === 0 ? 1 : 0, e = polyS([c, b, a]) + "=0";
      return { num: true, ans: rat(n), q: function () { return T(L3("Quantes solucions té", "¿Cuántas soluciones tiene", "How many solutions has")) + " $" + e + "$?"; },
        s: function () { return tex("\\Delta=" + ip(b) + "^2-4\\cdot" + ip(a) + "\\cdot" + ip(c) + "=" + D) + " → " + n + " " + T(n === 1 ? L3("solució", "solución", "solution") : L3("solucions", "soluciones", "solutions")) + "."; } };
    },
    cub: function () {
      var rs = rint(0, 3) === 0 ? [0, rnz(-5, 5), rnz(-5, 5)] : [rnz(-3, 3), rnz(-4, 4), rnz(-4, 4)], P = pconst(rat(1));
      rs.forEach(function (r) { P = pmul(P, fromC([rat(-r), rat(1)], "x")); });
      return eqItem(ptex(P) + "=0", rs);
    },
    prob: function () {
      var p = pick(PROBS)();
      return { num: true, ans: rat(p.ans), q: function () { return fill(T(p.q), p.d); }, s: function () { return tex(p.e) + " → <b>" + p.ans + "</b>"; } };
    }
  };
  /* llista de solucions escrita per l'alumne */
  function parseSet(raw) {
    var s = raw.toLowerCase().replace(/[−–]/g, "-").replace(/\+\/-|\+-/g, "±").replace(/[a-z][\d₁₂₃]?\s*=/g, "").trim();
    if (/^(cap|ninguna|ninguno|none|no|∅|sense solució|sin solución|no solution|no té solució|no tiene solución)\.?$/.test(s)) return [];
    var parts = s.indexOf(";") >= 0 ? s.split(";") : s.split(/\s+(?:i|y|and|o|or)\s+|,\s+|,(?=[-+±])/);
    var out = [];
    for (var i = 0; i < parts.length; i++) {
      var p = clean(parts[i]); if (!p) continue;
      var pmf = p[0] === "±"; if (pmf) p = p.slice(1);
      var e = parse(p); if (!e || !isConst(e)) return null;
      out.push(cval(e)); if (pmf) out.push(rneg(cval(e)));
    }
    return out;
  }
  function uniq(a) { var o = []; a.forEach(function (r) { if (!o.some(function (s) { return req(s, r); })) o.push(r); }); return o; }
  function sameSet(a, b) { a = uniq(a); b = uniq(b); return a.length === b.length && a.every(function (r) { return b.some(function (s) { return req(r, s); }); }); }
  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, res = 0, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore");
    function paint() {
      dq.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (done) info.innerHTML = (res ? '<span class="ok">✓ ' + u("right") + "</span>" : '<span class="ko">✗ ' + u("wrong") + "</span>") + '<div class="dsol">' + u("sol") + " " + q.s() + "</div>";
    }
    function check() {
      if (done) return;
      var raw = inp.value.trim(), good;
      if (!raw) { info.innerHTML = warn(q.num ? u("num") : u("set")); return; }
      if (q.set) { var got = parseSet(raw); if (!got) { info.innerHTML = warn(u("set")); return; } good = sameSet(got, q.ans); }
      else { var p = parse(clean(raw).replace(/^[a-z]=/i, "")); if (!p || !isConst(p)) { info.innerHTML = warn(u("num")); return; } good = req(cval(p), q.ans); }
      done = true; tot++; res = good; if (good) ok++;
      paint();
    }
    function fresh() { q = GEN[kind](); done = false; inp.value = ""; info.innerHTML = ""; paint(); }
    w.querySelector('[data-a="check"]').addEventListener("click", check);
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); inp.focus(); });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    onLang(paint);
  }
  window.FM5 = { parse: parse, ptex: ptex, readEq: readEq, solveAny: solveAny, texRaw: texRaw, mulSide: mulSide, parseSet: parseSet, sameSet: sameSet, GEN: GEN, nt: nt };

  /* ---------- qüestionari ---------- */
  var QUIZ = [
    { q: { va: "Quina d'aquestes igualtats és una identitat?", es: "¿Cuál de estas igualdades es una identidad?", en: "Which of these equalities is an identity?" },
      o: [{ va: "$2x+1=7$" }, { va: "$3(x+1)=3x+3$" }, { va: "$x^2=4$" }, { va: "$x+1=x$" }], a: 1,
      e: { va: "En operar, $3(x+1)=3x+3$: els dos membres són iguals per a qualsevol valor de $x$.", es: "Al operar, $3(x+1)=3x+3$: los dos miembros son iguales para cualquier valor de $x$.", en: "Working it out, $3(x+1)=3x+3$: both sides are equal for every value of $x$." } },
    { q: { va: "Quin d'aquests nombres és solució de $x^2+x=2$?", es: "¿Cuál de estos números es solución de $x^2+x=2$?", en: "Which of these numbers is a solution of $x^2+x=2$?" },
      o: [{ va: "$2$" }, { va: "$-2$" }, { va: "$0$" }, { va: "$3$" }], a: 1,
      e: { va: "$(-2)^2+(-2)=4-2=2$ ✓. Amb $x=2$ dona 6, amb 0 dona 0 i amb 3 dona 12.", es: "$(-2)^2+(-2)=4-2=2$ ✓. Con $x=2$ da 6, con 0 da 0 y con 3 da 12.", en: "$(-2)^2+(-2)=4-2=2$ ✓. $x=2$ gives 6, 0 gives 0 and 3 gives 12." } },
    { q: { va: "Quin grau té l'equació $x(x+3)=x^2-6$?", es: "¿Qué grado tiene la ecuación $x(x+3)=x^2-6$?", en: "What degree is the equation $x(x+3)=x^2-6$?" },
      o: [{ va: "$2$" }, { va: "$1$" }, { va: "$3$" }, { va: "$0$" }], a: 1,
      e: { va: "$x^2+3x=x^2-6\\Rightarrow 3x=-6$: els $x^2$ es cancel·len i queda de grau 1.", es: "$x^2+3x=x^2-6\\Rightarrow 3x=-6$: los $x^2$ se cancelan y queda de grado 1.", en: "$x^2+3x=x^2-6\\Rightarrow 3x=-6$: the $x^2$ terms cancel, leaving degree 1." } },
    { q: { va: "En $3x-5=10$, en transposar el $-5$ queda…", es: "En $3x-5=10$, al transponer el $-5$ queda…", en: "In $3x-5=10$, moving the $-5$ across gives…" },
      o: [{ va: "$3x=5$" }, { va: "$3x=15$" }, { va: "$3x=-15$" }, { va: "$x=10+5-3$" }], a: 1,
      e: { va: "El que resta passa sumant: $3x=10+5=15$.", es: "Lo que resta pasa sumando: $3x=10+5=15$.", en: "What is subtracted moves across added: $3x=10+5=15$." } },
    { q: { va: "Si $-4x=12$, aleshores…", es: "Si $-4x=12$, entonces…", en: "If $-4x=12$, then…" },
      o: [{ va: "$x=3$" }, { va: "$x=-3$" }, { va: "$x=16$" }, { va: "$x=8$" }], a: 1,
      e: { va: "El $-4$ multiplica, passa dividint amb el seu signe: $x=\\frac{12}{-4}=-3$.", es: "El $-4$ multiplica, pasa dividiendo con su signo: $x=\\frac{12}{-4}=-3$.", en: "The $-4$ multiplies, so it moves across dividing, sign included: $x=\\frac{12}{-4}=-3$." } },
    { q: { va: "La solució de $2(x-3)-(x+1)=0$ és…", es: "La solución de $2(x-3)-(x+1)=0$ es…", en: "The solution of $2(x-3)-(x+1)=0$ is…" },
      o: [{ va: "$x=5$" }, { va: "$x=7$" }, { va: "$x=-7$" }, { va: "$x=4$" }], a: 1,
      e: { va: "$2x-6-x-1=0\\Rightarrow x-7=0\\Rightarrow x=7$. Compte: el $-$ canvia el signe de $x$ i de $1$.", es: "$2x-6-x-1=0\\Rightarrow x-7=0\\Rightarrow x=7$. Ojo: el $-$ cambia el signo de $x$ y de $1$.", en: "$2x-6-x-1=0\\Rightarrow x-7=0\\Rightarrow x=7$. Careful: the $-$ changes the sign of both $x$ and $1$." } },
    { q: { va: "En multiplicar $\\frac{x+1}{2}-\\frac{x-1}{3}=1$ per 6 obtenim…", es: "Al multiplicar $\\frac{x+1}{2}-\\frac{x-1}{3}=1$ por 6 obtenemos…", en: "Multiplying $\\frac{x+1}{2}-\\frac{x-1}{3}=1$ by 6 gives…" },
      o: [{ va: "$3(x+1)-2(x-1)=1$" }, { va: "$3(x+1)-2(x-1)=6$" }, { va: "$3x+1-2x-1=6$" }, { va: "$3(x+1)-2x-1=6$" }], a: 1,
      e: { va: "Tots els termes es multipliquen per 6 (també el 1 del segon membre) i els numeradors van entre parèntesis.", es: "Todos los términos se multiplican por 6 (también el 1 del segundo miembro) y los numeradores van entre paréntesis.", en: "Every term is multiplied by 6 (including the 1 on the right) and the numerators go in brackets." } },
    { q: { va: "L'equació $2(x+1)=2x+3$…", es: "La ecuación $2(x+1)=2x+3$…", en: "The equation $2(x+1)=2x+3$…" },
      o: [{ va: "no té solució", es: "no tiene solución", en: "has no solution" }, { va: "té infinites solucions", es: "tiene infinitas soluciones", en: "has infinitely many solutions" }, { va: "té la solució $x=1$", es: "tiene la solución $x=1$", en: "has the solution $x=1$" }, { va: "té la solució $x=0$", es: "tiene la solución $x=0$", en: "has the solution $x=0$" }], a: 0,
      e: { va: "$2x+2=2x+3\\Rightarrow 0x=1$: cap nombre multiplicat per 0 dona 1.", es: "$2x+2=2x+3\\Rightarrow 0x=1$: ningún número multiplicado por 0 da 1.", en: "$2x+2=2x+3\\Rightarrow 0x=1$: no number times 0 gives 1." } },
    { q: { va: "Les solucions de $x^2-16=0$ són…", es: "Las soluciones de $x^2-16=0$ son…", en: "The solutions of $x^2-16=0$ are…" },
      o: [{ va: "$x=4$" }, { va: "$x=\\pm4$" }, { va: "$x=\\pm8$" }, { va: "$x=8$" }], a: 1,
      e: { va: "$x^2=16\\Rightarrow x=\\pm\\sqrt{16}=\\pm4$. No oblides l'arrel negativa: $(-4)^2=16$.", es: "$x^2=16\\Rightarrow x=\\pm\\sqrt{16}=\\pm4$. No olvides la raíz negativa: $(-4)^2=16$.", en: "$x^2=16\\Rightarrow x=\\pm\\sqrt{16}=\\pm4$. Don't forget the negative root: $(-4)^2=16$." } },
    { q: { va: "Les solucions de $3x^2=6x$ són…", es: "Las soluciones de $3x^2=6x$ son…", en: "The solutions of $3x^2=6x$ are…" },
      o: [{ va: "$x=2$" }, { va: "$x=0$ i $x=2$", es: "$x=0$ y $x=2$", en: "$x=0$ and $x=2$" }, { va: "$x=\\pm2$" }, { va: "$x=0$" }], a: 1,
      e: { va: "$3x^2-6x=0\\Rightarrow 3x(x-2)=0$. Si dividim entre $x$ perdem la solució $x=0$.", es: "$3x^2-6x=0\\Rightarrow 3x(x-2)=0$. Si dividimos entre $x$ perdemos la solución $x=0$.", en: "$3x^2-6x=0\\Rightarrow 3x(x-2)=0$. Dividing by $x$ would lose the solution $x=0$." } },
    { q: { va: "Quant val el discriminant de $2x^2-x-3=0$?", es: "¿Cuánto vale el discriminante de $2x^2-x-3=0$?", en: "What is the discriminant of $2x^2-x-3=0$?" },
      o: [{ va: "$-23$" }, { va: "$25$" }, { va: "$-25$" }, { va: "$7$" }], a: 1,
      e: { va: "$\\Delta=b^2-4ac=(-1)^2-4\\cdot2\\cdot(-3)=1+24=25$.", es: "$\\Delta=b^2-4ac=(-1)^2-4\\cdot2\\cdot(-3)=1+24=25$.", en: "$\\Delta=b^2-4ac=(-1)^2-4\\cdot2\\cdot(-3)=1+24=25$." } },
    { q: { va: "L'equació $x^2+2x+5=0$…", es: "La ecuación $x^2+2x+5=0$…", en: "The equation $x^2+2x+5=0$…" },
      o: [{ va: "té dues solucions", es: "tiene dos soluciones", en: "has two solutions" }, { va: "té una solució doble", es: "tiene una solución doble", en: "has a double solution" }, { va: "no té solució", es: "no tiene solución", en: "has no solution" }], a: 2,
      e: { va: "$\\Delta=4-20=-16<0$: l'arrel d'un nombre negatiu no existeix.", es: "$\\Delta=4-20=-16<0$: la raíz de un número negativo no existe.", en: "$\\Delta=4-20=-16<0$: a negative number has no square root." } },
    { q: { va: "Les solucions de $x^2-x-6=0$ són…", es: "Las soluciones de $x^2-x-6=0$ son…", en: "The solutions of $x^2-x-6=0$ are…" },
      o: [{ va: "$3$ i $-2$", es: "$3$ y $-2$", en: "$3$ and $-2$" }, { va: "$-3$ i $2$", es: "$-3$ y $2$", en: "$-3$ and $2$" }, { va: "$6$ i $-1$", es: "$6$ y $-1$", en: "$6$ and $-1$" }, { va: "$1$ i $-6$", es: "$1$ y $-6$", en: "$1$ and $-6$" }], a: 0,
      e: { va: "$x=\\frac{1\\pm\\sqrt{1+24}}{2}=\\frac{1\\pm5}{2}$: $3$ i $-2$.", es: "$x=\\frac{1\\pm\\sqrt{1+24}}{2}=\\frac{1\\pm5}{2}$: $3$ y $-2$.", en: "$x=\\frac{1\\pm\\sqrt{1+24}}{2}=\\frac{1\\pm5}{2}$: $3$ and $-2$." } },
    { q: { va: "Per a resoldre $x^3-4x^2+x+6=0$ amb Ruffini, quins valors provem?", es: "Para resolver $x^3-4x^2+x+6=0$ con Ruffini, ¿qué valores probamos?", en: "To solve $x^3-4x^2+x+6=0$ with Ruffini, which values do we try?" },
      o: [{ va: "Els divisors de 4", es: "Los divisores de 4", en: "The divisors of 4" }, { va: "Els divisors de 6 (positius i negatius)", es: "Los divisores de 6 (positivos y negativos)", en: "The divisors of 6 (positive and negative)" }, { va: "Qualsevol nombre enter", es: "Cualquier número entero", en: "Any whole number" }, { va: "Només l'1", es: "Solo el 1", en: "Only 1" }], a: 1,
      e: { va: "Les solucions enteres són divisors del terme independent, 6. Ací són $-1,\\ 2$ i $3$.", es: "Las soluciones enteras son divisores del término independiente, 6. Aquí son $-1,\\ 2$ y $3$.", en: "Whole-number solutions divide the constant term, 6. Here they are $-1,\\ 2$ and $3$." } },
    { q: { va: "Les solucions de $x(x-2)(x+5)=0$ són…", es: "Las soluciones de $x(x-2)(x+5)=0$ son…", en: "The solutions of $x(x-2)(x+5)=0$ are…" },
      o: [{ va: "$2$ i $-5$", es: "$2$ y $-5$", en: "$2$ and $-5$" }, { va: "$0,\\ 2$ i $-5$", es: "$0,\\ 2$ y $-5$", en: "$0,\\ 2$ and $-5$" }, { va: "$0,\\ -2$ i $5$", es: "$0,\\ -2$ y $5$", en: "$0,\\ -2$ and $5$" }, { va: "$2$ i $5$", es: "$2$ y $5$", en: "$2$ and $5$" }], a: 1,
      e: { va: "Un producte val 0 si algun factor val 0: $x=0$, $x-2=0$ o $x+5=0$.", es: "Un producto vale 0 si algún factor vale 0: $x=0$, $x-2=0$ o $x+5=0$.", en: "A product is 0 if one factor is 0: $x=0$, $x-2=0$ or $x+5=0$." } },
    { q: { va: "«El doble d'un nombre més 5 és 17». L'equació és…", es: "«El doble de un número más 5 es 17». La ecuación es…", en: "“Twice a number plus 5 is 17”. The equation is…" },
      o: [{ va: "$2(x+5)=17$" }, { va: "$2x+5=17$" }, { va: "$x+10=17$" }, { va: "$2+x+5=17$" }], a: 1,
      e: { va: "Primer el doble, $2x$, i després sumem 5: $2x+5=17\\Rightarrow x=6$.", es: "Primero el doble, $2x$, y después sumamos 5: $2x+5=17\\Rightarrow x=6$.", en: "First double it, $2x$, then add 5: $2x+5=17\\Rightarrow x=6$." } },
    { q: { va: "Un rectangle té costats $x$ i $x+2$ i àrea 48. Quina equació el resol?", es: "Un rectángulo tiene lados $x$ y $x+2$ y área 48. ¿Qué ecuación lo resuelve?", en: "A rectangle has sides $x$ and $x+2$ and area 48. Which equation solves it?" },
      o: [{ va: "$2x+2(x+2)=48$" }, { va: "$x(x+2)=48$" }, { va: "$x+x+2=48$" }, { va: "$x^2+2=48$" }], a: 1,
      e: { va: "Àrea = base · altura: $x(x+2)=48\\Rightarrow x^2+2x-48=0\\Rightarrow x=6$ (el $-8$ no val): 6 × 8.", es: "Área = base · altura: $x(x+2)=48\\Rightarrow x^2+2x-48=0\\Rightarrow x=6$ (el $-8$ no vale): 6 × 8.", en: "Area = base · height: $x(x+2)=48\\Rightarrow x^2+2x-48=0\\Rightarrow x=6$ ($-8$ isn't valid): 6 × 8." } }
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

  var TITLES = { va: "Equacions · FentMates", es: "Ecuaciones · FentMates", en: "Equations · FentMates" };
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
    wCheck(); solverWidget("w-lin", 1); wDisc(); solverWidget("w-q2", 2); solverWidget("w-cub", 0);
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
