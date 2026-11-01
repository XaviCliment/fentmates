(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1eso-u6-done", NSEC = 9;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc",
      bad: "No entenc l'equació. Ha de tindre un signe = i una sola lletra: exemple 3(x-2)=x+4.", badE: "No entenc l'expressió. Exemple: 3(x+2)-x.",
      num: "Escriu un nombre (pot ser negatiu o una fracció, com 3/2).", yn: "Respon «sí» o «no».", onlyX: "Fes servir només la lletra x.",
      notRed: "És equivalent, però encara no està reduïda: agrupa els termes semblants i trau els parèntesis.", sol: "Solució:" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro",
      bad: "No entiendo la ecuación. Debe tener un signo = y una sola letra: ejemplo 3(x-2)=x+4.", badE: "No entiendo la expresión. Ejemplo: 3(x+2)-x.",
      num: "Escribe un número (puede ser negativo o una fracción, como 3/2).", yn: "Responde «sí» o «no».", onlyX: "Usa solo la letra x.",
      notRed: "Es equivalente, pero todavía no está reducida: agrupa los términos semejantes y quita los paréntesis.", sol: "Solución:" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Score", right: "Correct!", wrong: "Not correct.", theme: "Switch between light and dark mode",
      bad: "I can't read that equation. It needs an = sign and a single letter: e.g. 3(x-2)=x+4.", badE: "I can't read that expression. Example: 3(x+2)-x.",
      num: "Type a number (it can be negative or a fraction, like 3/2).", yn: "Answer “yes” or “no”.", onlyX: "Use only the letter x.",
      notRed: "It's equivalent, but not simplified yet: collect the like terms and remove the brackets.", sol: "Solution:" }
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

  /* ---------- ajudes de la unitat 6 ---------- */
  function sg(n) { return n < 0 ? "-" : "+"; }
  /* fracció amb només 2 i 5 al denominador -> decimal amb coma */
  function decOf(r) {
    var d = r.d, k = 0; while (d % 2 === 0) { d /= 2; k++; } while (d % 5 === 0) { d /= 5; k++; }
    if (d !== 1 || k > 6) return null;
    var s = (Math.abs(r.n) / r.d).toFixed(k).replace(/0+$/, "").replace(/\.$/, "");
    return (r.n < 0 ? "-" : "") + s.replace(".", "\\dc ");
  }
  function ntd(r) { var d = r.d === 1 ? null : decOf(r); return d ? d : nt(r); }
  /* expressió llegida pel text; null si no s'entén */
  function readE(raw) { var s = clean(raw || ""); if (!s || /=/.test(s)) return null; var p = parse(s); return p ? { s: s, p: p } : null; }
  /* termes del nivell superior amb el seu polinomi (amb signe) */
  function termPolys(s) {
    var ts = topTerms(s); if (!ts) return null;
    var out = [];
    for (var i = 0; i < ts.length; i++) { var q = parse(ts[i].t); if (!q) return null; out.push({ sg: ts[i].sg, t: ts[i].t, p: ts[i].sg === "-" ? pneg(q) : q }); }
    return out;
  }
  /* està escrita de manera reduïda? (sense parèntesis ni productes i sense termes semblants repetits) */
  function isReduced(raw, p) {
    var s = clean(raw); if (/[()\[\]{}*:]/.test(s)) return false;
    var tp = termPolys(s); if (!tp) return false;
    var n = Object.keys(p).length, seen = {};
    for (var i = 0; i < tp.length; i++) {
      var ks = Object.keys(tp[i].p); if (ks.length > 1) return false;
      if (ks.length === 1) { if (seen[ks[0]]) return false; seen[ks[0]] = 1; }
      if (/^\d+(?:[.,]\d+)?\/\d+$/.test(tp[i].t) || /^\d+[.,]?\d*\^/.test(tp[i].t)) return false;
    }
    return tp.length === Math.max(n, 1);
  }
  /* substitució de diverses lletres en el text: "2a-b", {a:5,b:-2} -> "2*5-(-2)" */
  function substAll(s, vals) {
    var out = "";
    for (var i = 0; i < s.length; i++) {
      var c = s[i].toLowerCase();
      if (/[a-z]/.test(c) && vals[c]) {
        var r = vals[c], V = r.d !== 1 ? "(" + (r.n < 0 ? "-" : "") + Math.abs(r.n) + "/" + r.d + ")" : r.n < 0 ? "(" + r.n + ")" : String(r.n);
        var dv = r.d !== 1 && decOf(r); if (dv) V = (r.n < 0 ? "(" : "") + dv.replace("\\dc ", ".") + (r.n < 0 ? ")" : "");
        out += (i > 0 && /[\d)\]}a-z.]/i.test(s[i - 1]) ? "*" : "") + V + (i + 1 < s.length && /[\d(\[{a-z]/i.test(s[i + 1]) ? "*" : "");
      } else out += s[i];
    }
    return out;
  }
  /* valor numèric pas a pas */
  function valRows(s, p, vals) {
    var rows = [], sub = substAll(s, vals), res = evalAt(p, vals);
    rows.push(T(L3("Substituïm:", "Sustituimos:", "Substitute:")) + tex(texRaw(sub), true));
    var tp = termPolys(s);
    if (tp && tp.length > 1) {
      var parts = tp.map(function (t, i) { var v = evalAt(t.p, vals); return (v.n < 0 ? "-" : i ? "+" : "") + ntd({ n: Math.abs(v.n), d: v.d }); });
      rows.push(T(L3("Calculem cada terme (primer potències i productes):", "Calculamos cada término (primero potencias y productos):", "Work out each term (powers and products first):")) + tex(parts.join("") + "=\\boxed{" + ntd(res) + "}", true));
    } else rows.push(T(L3("Calculem:", "Calculamos:", "Work it out:")) + tex(texRaw(sub) + "=\\boxed{" + ntd(res) + "}", true));
    return rows;
  }
  function solve1(E) {
    var pre = prepare(E), rows = pre.rows, diff = psub(pre.L, pre.R), deg = pdeg(diff), v = pre.v;
    if (isZero(diff)) { rows.push(T(L3("Els dos membres són iguals: és una <b>identitat</b> i qualsevol nombre n'és solució.", "Los dos miembros son iguales: es una <b>identidad</b> y cualquier número es solución.", "Both sides are the same: it's an <b>identity</b> and every number is a solution."))); return { rows: rows, all: true, deg: 0 }; }
    if (deg > 1) { rows.push(warn(fill(T(L3("Un cop reduïda, aquesta equació és de grau {d}: no és de primer grau.", "Una vez reducida, esta ecuación es de grado {d}: no es de primer grado.", "Once simplified, this equation has degree {d}: it isn't first degree.")), { d: deg }))); return { rows: rows, deg: deg }; }
    var r = linSolve(pre, E, rows);
    if (r.sols && r.sols.length) rows.push(u("sol") + " " + tex("\\boxed{" + v + "=" + ntd(r.sols[0].r) + "}"));
    return { rows: rows, sols: r.sols, all: r.all, deg: 1 };
  }

  /* ---------- 6.1 sèries amb escuradents ---------- */
  function patEdges(kind, n) {
    var E = {}, list = [], s = 34;
    function add(x1, y1, x2, y2) {
      var k1 = Math.round(x1) + "," + Math.round(y1), k2 = Math.round(x2) + "," + Math.round(y2), k = k1 < k2 ? k1 + "|" + k2 : k2 + "|" + k1;
      if (!E[k]) { E[k] = 1; list.push([x1, y1, x2, y2, k]); }
    }
    for (var i = 0; i < n; i++) {
      if (kind === "q") { var x = i * s; add(x, 0, x, s); add(x, 0, x + s, 0); add(x, s, x + s, s); add(x + s, 0, x + s, s); }
      else if (kind === "t") {
        var h = s * 0.866, j = Math.floor(i / 2);
        if (i % 2 === 0) { add(j * s, h, j * s + s, h); add(j * s, h, j * s + s / 2, 0); add(j * s + s / 2, 0, j * s + s, h); }
        else { add(j * s + s / 2, 0, j * s + 1.5 * s, 0); add(j * s + s / 2, 0, j * s + s, h); add(j * s + s, h, j * s + 1.5 * s, 0); }
      } else {
        var r = s * 0.62, w = r * 1.732, cx = r * 0.866 + i * w, cy = r, P = [];
        for (var k = 0; k < 6; k++) { var a = Math.PI / 6 + k * Math.PI / 3; P.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
        for (k = 0; k < 6; k++) add(P[k][0], P[k][1], P[(k + 1) % 6][0], P[(k + 1) % 6][1]);
      }
    }
    return list;
  }
  var PAT = { q: { m: 3, b: 1 }, t: { m: 2, b: 1 }, h: { m: 5, b: 1 } };
  function wPat() {
    var w = document.getElementById("w-pat"); if (!w) return;
    var rg = w.querySelector('input[type="range"]'), rv = w.querySelector(".rv"), vis = w.querySelector(".fvis"), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), kind = "q";
    function paint() {
      var n = +rg.value, all = patEdges(kind, n), prev = {}, P = PAT[kind];
      patEdges(kind, n - 1).forEach(function (e) { prev[e[4]] = 1; });
      rv.textContent = n;
      var xs = [], ys = []; all.forEach(function (e) { xs.push(e[0], e[2]); ys.push(e[1], e[3]); });
      var X0 = Math.min.apply(null, xs) - 8, Y0 = Math.min.apply(null, ys) - 8, W = Math.max.apply(null, xs) - X0 + 8, H = Math.max.apply(null, ys) - Y0 + 8;
      var g = all.map(function (e) { var nw = !prev[e[4]] && n > 1; return '<line class="stk' + (nw ? " nw" : "") + '" x1="' + e[0].toFixed(1) + '" y1="' + e[1].toFixed(1) + '" x2="' + e[2].toFixed(1) + '" y2="' + e[3].toFixed(1) + '"/><circle class="stk-h" cx="' + e[0].toFixed(1) + '" cy="' + e[1].toFixed(1) + '" r="3.3"/>'; }).join("");
      vis.innerHTML = '<svg viewBox="' + X0.toFixed(1) + " " + Y0.toFixed(1) + " " + W.toFixed(1) + " " + H.toFixed(1) + '" style="width:' + Math.min(560, W * 1.6).toFixed(0) + 'px">' + g + "</svg>";
      var name = T({ q: L3("quadrats", "cuadrados", "squares"), t: L3("triangles", "triángulos", "triangles"), h: L3("hexàgons", "hexágonos", "hexagons") }[kind]);
      var head = "<tr><th>n</th>" + [1, 2, 3, 4, 5].map(function (k) { return "<td>" + k + "</td>"; }).join("") + "<td>…</td><td>n</td></tr>";
      var row = "<tr><th>" + T(L3("Escuradents", "Palillos", "Sticks")) + "</th>" + [1, 2, 3, 4, 5].map(function (k) { return "<td" + (k === n ? ' class="hl"' : "") + ">" + patEdges(kind, k).length + "</td>"; }).join("") + "<td>…</td><td>" + tex(P.m + "n+" + P.b) + "</td></tr>";
      out.innerHTML = '<div class="tbl-wrap"><table class="data ptab"><tbody>' + head + row + "</tbody></table></div>"
        + rows2html([fill(T(L3("Amb {n} {f} fan falta {c} escuradents. Cada figura nova n'afegix {m} (en color).", "Con {n} {f} hacen falta {c} palillos. Cada figura nueva añade {m} (en color).", "{n} {f} need {c} matchsticks. Each new shape adds {m} (in colour).")), { n: n, f: name, c: all.length, m: P.m })
          + tex(P.m + "n+" + P.b + "\\ \\to\\ " + P.m + "\\cdot" + n + "+" + P.b + "=" + (P.m * n + P.b), true)]);
      info.innerHTML = "💡 " + fill(T(L3("Amb la fórmula podem calcular-ho sense dibuixar: per a 100 {f}, {m}·100 + {b} = {r} escuradents.", "Con la fórmula podemos calcularlo sin dibujar: para 100 {f}, {m}·100 + {b} = {r} palillos.", "With the formula we can work it out without drawing: 100 {f} need {m}·100 + {b} = {r} matchsticks.")), { f: name, m: P.m, b: P.b, r: P.m * 100 + P.b });
    }
    segBind(w, function (k) { kind = k; paint(); });
    rg.addEventListener("input", paint);
    onLang(paint);
  }

  /* ---------- 6.2 valor numèric ---------- */
  function readVals(raw) {
    var o = {}, ok = true;
    raw.split(";").forEach(function (part) {
      part = clean(part); if (!part) return;
      var m = /^([a-z])=(.+)$/i.exec(part); if (!m) { ok = false; return; }
      var q = parse(m[2]); if (!q || !isConst(q)) { ok = false; return; }
      o[m[1].toLowerCase()] = cval(q);
    });
    return ok ? o : null;
  }
  function wVal() {
    var w = document.getElementById("w-val"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), tab = w.querySelector(".vtab"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = ""; tab.innerHTML = "";
      var R = readE(I.e.value), vals = readVals(I.v.value);
      if (!R) { out.innerHTML = ""; info.innerHTML = warn(u("badE")); return; }
      if (negExp(R.p)) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Aquesta eina no admet lletres dividint.", "Esta herramienta no admite letras dividiendo.", "This tool doesn't accept letters in a denominator."))); return; }
      var vs = pvars(R.p);
      if (!vals) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Escriu els valors així: x=-3 (o a=5; b=-2).", "Escribe los valores así: x=-3 (o a=5; b=-2).", "Type the values like this: x=-3 (or a=5; b=-2)."))); return; }
      var miss = vs.filter(function (v) { return !vals[v]; });
      if (miss.length) { out.innerHTML = ""; info.innerHTML = warn(fill(T(L3("Falta el valor de {v}.", "Falta el valor de {v}.", "The value of {v} is missing.")), { v: miss.join(", ") })); return; }
      var rows = [tex(texRaw(R.s), true)].concat(valRows(R.s, R.p, vals));
      out.innerHTML = rows2html(rows);
      if (vs.length === 1) {
        var v = vs[0], xs = [-2, -1, 0, 1, 2, 3, 4], o = {};
        tab.innerHTML = '<p class="hint-s">' + fill(T(L3("Taula de valors de l'expressió per a diversos valors de {v}:", "Tabla de valores de la expresión para varios valores de {v}:", "Table of values of the expression for several values of {v}:")), { v: v }) + '</p><div class="tbl-wrap"><table class="data ptab"><tbody><tr><th>' + tex(v) + "</th>"
          + xs.map(function (k) { return "<td>" + k + "</td>"; }).join("") + "</tr><tr><th>" + T(L3("Valor", "Valor", "Value")) + "</th>"
          + xs.map(function (k) { o[v] = rat(k); return "<td" + (req(vals[v], rat(k)) ? ' class="hl"' : "") + ">" + tex(ntd(evalAt(R.p, o))) + "</td>"; }).join("") + "</tr></tbody></table></div>";
      }
      if (vs.length && vs.some(function (k) { return vals[k].n < 0; })) info.innerHTML = "💡 " + T(L3("Hem posat els nombres negatius entre parèntesis.", "Hemos puesto los números negativos entre paréntesis.", "We put the negative numbers in brackets."));
    }
    [I.e, I.v].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (b) { I.e.value = b[0]; I.v.value = b[1]; paint(); });
    onLang(paint);
  }

  /* ---------- 6.3 monomis i polinomis ---------- */
  function litT(e) { var s = etex(e); return s || "\\text{—}"; }
  function wMono() {
    var w = document.getElementById("w-mono"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = "";
      var R = readE(I.e.value);
      if (!R) { out.innerHTML = ""; info.innerHTML = warn(u("badE")); return; }
      if (negExp(R.p)) { out.innerHTML = rows2html([tex(texRaw(R.s), true)]); info.innerHTML = warn(T(L3("Hi ha una lletra dividint: <b>no és un monomi</b> (ni un polinomi).", "Hay una letra dividiendo: <b>no es un monomio</b> (ni un polinomio).", "There's a letter in a denominator: <b>it isn't a monomial</b> (or a polynomial)."))); return; }
      var ts = terms(R.p), tp = termPolys(R.s), rows = [tex(texRaw(R.s), true)];
      if (tp && (tp.length !== ts.length || /[()*]/.test(R.s))) rows.push(T(L3("Operant i reduint queda:", "Operando y reduciendo queda:", "Working it out and simplifying gives:")) + tex(ptex(R.p), true));
      var head = "<tr><th>" + T(L3("Terme", "Término", "Term")) + "</th><th>" + T(L3("Coeficient", "Coeficiente", "Coefficient")) + "</th><th>" + T(L3("Part literal", "Parte literal", "Literal part")) + "</th><th>" + T(L3("Grau", "Grado", "Degree")) + "</th></tr>";
      var body = ts.map(function (t) { return "<tr><td>" + tex(ttex(t, true)) + "</td><td>" + tex(nt(t.c)) + "</td><td>" + tex(litT(t.e)) + "</td><td>" + tdeg(t.e) + "</td></tr>"; }).join("");
      rows.push('<div class="tbl-wrap"><table class="data ptab"><thead>' + head + "</thead><tbody>" + body + "</tbody></table></div>");
      if (ts.length <= 1) {
        var t = ts[0] || { c: rat(0), e: {} };
        rows.push('<span class="ok">' + fill(T(L3("És un <b>monomi</b>: coeficient {c}, part literal {l}, grau {g}.", "Es un <b>monomio</b>: coeficiente {c}, parte literal {l}, grado {g}.", "It's a <b>monomial</b>: coefficient {c}, literal part {l}, degree {g}.")), { c: tex(nt(t.c)), l: tex(litT(t.e)), g: tdeg(t.e) }) + "</span>");
      } else {
        var nm = ts.length === 2 ? T(L3("binomi", "binomio", "binomial")) : ts.length === 3 ? T(L3("trinomi", "trinomio", "trinomial")) : T(L3("polinomi", "polinomio", "polynomial"));
        rows.push('<span class="ok">' + fill(T(L3("És un <b>{n}</b> ({k} termes) de grau {g}. Terme independent: {i}.", "Es un <b>{n}</b> ({k} términos) de grado {g}. Término independiente: {i}.", "It's a <b>{n}</b> ({k} terms) of degree {g}. Constant term: {i}.")), { n: nm, k: ts.length, g: pdeg(R.p), i: tex(nt(cval(R.p))) }) + "</span>");
      }
      out.innerHTML = rows2html(rows);
    }
    I.e.addEventListener("input", paint);
    quickBind(w, function (b) { I.e.value = b[0]; paint(); });
    onLang(paint);
  }

  /* ---------- 6.4 fitxes algebraiques ---------- */
  function tileSpan(k, s, cls) { return '<span class="tile k' + k + (s < 0 ? " neg" : "") + (cls ? " " + cls : "") + '">' + (k === 2 ? "x²" : k === 1 ? "x" : "") + "</span>"; }
  function wTiles() {
    var w = document.getElementById("w-tiles"); if (!w) return;
    var I = inputs(w), vis = w.querySelector(".fvis"), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = ""; vis.innerHTML = ""; out.innerHTML = "";
      var R = readE(I.e.value);
      if (!R) { info.innerHTML = warn(u("badE")); return; }
      var vs = pvars(R.p), tp = termPolys(R.s);
      if (vs.some(function (v) { return v !== "x"; }) || negExp(R.p) || pdeg(R.p) > 2 || !tp) { info.innerHTML = warn(T(L3("Les fitxes només funcionen amb la lletra x i fins a x².", "Las fichas solo funcionan con la letra x y hasta x².", "The tiles only work with the letter x, up to x²."))); return; }
      var cnt = [[0, 0], [0, 0], [0, 0]], items = [], bad = false;
      tp.forEach(function (t) {
        [2, 1, 0].forEach(function (k) {
          var c = cof(t.p, "x", k); if (!c.n) return;
          if (c.d !== 1 || Math.abs(c.n) > 12) { bad = true; return; }
          items.push({ k: k, c: c.n }); cnt[k][c.n > 0 ? 0 : 1] += Math.abs(c.n);
        });
      });
      if (bad || cnt.some(function (p) { return p[0] + p[1] > 16; })) { info.innerHTML = warn(T(L3("Fes servir coeficients enters petits (com a molt 16 fitxes de cada tipus).", "Usa coeficientes enteros pequeños (como mucho 16 fichas de cada tipo).", "Use small whole-number coefficients (at most 16 tiles of each kind)."))); return; }
      var before = items.map(function (it) { var s = ""; for (var j = 0; j < Math.abs(it.c); j++) s += tileSpan(it.k, it.c); return '<span class="tg">' + s + "</span>"; }).join("");
      var grouped = "", after = "";
      [2, 1, 0].forEach(function (k) {
        var p = cnt[k][0], n = cnt[k][1], z = Math.min(p, n); if (!p && !n) return;
        var s = "";
        for (var j = 0; j < p; j++) s += tileSpan(k, 1, j < z ? "zp" : "");
        for (j = 0; j < n; j++) s += tileSpan(k, -1, j < z ? "zp" : "");
        grouped += '<span class="tg">' + s + "</span>";
        var r = p - n; s = ""; for (j = 0; j < Math.abs(r); j++) s += tileSpan(k, r); if (s) after += '<span class="tg">' + s + "</span>";
      });
      vis.innerHTML = '<div class="trow"><span class="tl">' + T(L3("Expressió", "Expresión", "Expression")) + "</span>" + before + '</div><div class="trow"><span class="tl">' + T(L3("Agrupem", "Agrupamos", "Group")) + "</span>" + grouped + '</div><div class="trow"><span class="tl">' + T(L3("Resultat", "Resultado", "Result")) + "</span>" + (after || '<span class="t0">0</span>') + "</div>"
        + '<p class="hint-s"><span class="tile k1 mini"></span> = x &nbsp; <span class="tile k0 mini"></span> = 1 &nbsp; <span class="tile k1 neg mini"></span> = −x &nbsp; <span class="tile k0 neg mini"></span> = −1 &nbsp; ' + T(L3("Les fitxes ratllades formen parelles que s'anul·len.", "Las fichas tachadas forman parejas que se anulan.", "Crossed-out tiles form pairs that cancel out.")) + "</p>";
      var groups = [2, 1, 0].map(function (k) {
        var cs = items.filter(function (it) { return it.k === k; }); if (!cs.length) return null;
        var s = cs.map(function (it, i) { return ttex(mono(rat(it.c), VE("x", k)), i === 0); }).join("");
        return { s: s, n: cs.length };
      }).filter(Boolean);
      var gtex = groups.map(function (g, i) { return g.n > 1 ? (i ? "+" : "") + "(" + g.s + ")" : (i && g.s[0] !== "-" ? "+" : "") + g.s; }).join("");
      out.innerHTML = rows2html([tex(texRaw(R.s), true), T(L3("Agrupem els termes semblants:", "Agrupamos los términos semejantes:", "Group the like terms:")) + tex(gtex + "=\\boxed{" + ptex(R.p) + "}", true)]);
    }
    I.e.addEventListener("input", paint);
    quickBind(w, function (b) { I.e.value = b[0]; paint(); });
    onLang(paint);
  }

  /* ---------- 6.4 reducció pas a pas ---------- */
  function joinMonos(list) { return list.length ? list.map(function (t, i) { return ttex(t, i === 0); }).join("") : "0"; }
  function wRed() {
    var w = document.getElementById("w-red"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = "";
      var R = readE(I.e.value), tp = R && termPolys(R.s);
      if (!R || !tp) { out.innerHTML = ""; info.innerHTML = warn(u("badE")); return; }
      if (negExp(R.p)) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Aquesta eina no admet lletres dividint.", "Esta herramienta no admite letras dividiendo.", "This tool doesn't accept letters in a denominator."))); return; }
      var rows = [tex(texRaw(R.s), true)], monos = [];
      tp.forEach(function (t) { terms(t.p).forEach(function (m) { monos.push(m); }); });
      var expanded = tp.some(function (t) { return /[()\[\]{}*]/.test(t.t) || terms(t.p).length !== 1; });
      if (expanded) rows.push(T(L3("Traiem parèntesis i fem els productes (compte amb els signes):", "Quitamos paréntesis y hacemos los productos (cuidado con los signos):", "Remove brackets and multiply out (watch the signs):")) + tex(joinMonos(monos), true));
      var groups = {}, order = [];
      monos.forEach(function (m) { var k = mkey(m.e); if (!groups[k]) { groups[k] = []; order.push(m); } groups[k].push(m); });
      order.sort(cmpE);
      var rep = order.some(function (m) { return groups[mkey(m.e)].length > 1; });
      if (rep) {
        var g = order.map(function (m, i) { var l = groups[mkey(m.e)]; return l.length > 1 ? (i ? "+" : "") + "(" + joinMonos(l) + ")" : (i ? ttex(l[0], false) : ttex(l[0], true)); }).join("");
        rows.push(T(L3("Agrupem els termes semblants:", "Agrupamos los términos semejantes:", "Group the like terms:")) + tex(g, true));
      }
      rows.push(T(L3("Resultat:", "Resultado:", "Result:")) + " " + tex("\\boxed{" + ptex(R.p) + "}"));
      out.innerHTML = rows2html(rows);
      if (!expanded && !rep) info.innerHTML = "💡 " + T(L3("Ja està reduïda: no hi ha parèntesis ni termes semblants.", "Ya está reducida: no hay paréntesis ni términos semejantes.", "It's already simplified: no brackets and no like terms."));
    }
    I.e.addEventListener("input", paint);
    quickBind(w, function (b) { I.e.value = b[0]; paint(); });
    onLang(paint);
  }

  /* ---------- 6.6 la balança ---------- */
  function sideT(a, b) { var s = a ? (a === 1 ? "x" : a + "x") : ""; if (b) s += (a ? "+" : "") + b; return s || "0"; }
  function subSide(a, b, x) { var s = a ? (a === 1 ? "" : a + "\\cdot ") + x : ""; if (b) s += (a ? "+" : "") + b; return s || "0"; }
  function balEq(S) { return sideT(S[0], S[1]) + "=" + sideT(S[2], S[3]); }
  function panSvg(cx, a, b) {
    var items = [], g = "", per = 6, Y = 196;
    for (var i = 0; i < a; i++) items.push("x"); for (i = 0; i < b; i++) items.push("1");
    items.forEach(function (it, j) {
      var row = Math.floor(j / per), col = j % per, inRow = Math.min(per, items.length - row * per), x = cx - inRow * 14 + col * 28 + 14, y = Y - 15 - row * 28;
      g += it === "x" ? '<rect class="bx" x="' + (x - 12) + '" y="' + (y - 12) + '" width="24" height="24" rx="4"/><text class="bxt" x="' + x + '" y="' + (y + 5) + '" text-anchor="middle">x</text>'
        : '<circle class="bu" cx="' + x + '" cy="' + y + '" r="10"/><text class="but" x="' + x + '" y="' + (y + 4) + '" text-anchor="middle">1</text>';
    });
    return '<path class="bpan" d="M' + (cx - 92) + " " + Y + " Q" + cx + " " + (Y + 22) + " " + (cx + 92) + " " + Y + ' Z"/><path class="bstr" d="M' + cx + " 30 L" + (cx - 88) + " " + Y + " M" + cx + " 30 L" + (cx + 88) + " " + Y + '"/>' + g;
  }
  function wBal() {
    var w = document.getElementById("w-bal"); if (!w) return;
    var vis = w.querySelector(".fvis"), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), bk = w.querySelector(".bal-k");
    var B = {}; w.querySelectorAll(".bal-ops button").forEach(function (b) { B[b.dataset.op] = b; });
    var S0 = [3, 2, 1, 8], S = S0.slice(), hist = [];
    function divK() { if (!S[1] && !S[2] && S[0] > 1 && S[3] % S[0] === 0) return S[0]; if (!S[0] && !S[3] && S[2] > 1 && S[1] % S[2] === 0) return S[2]; return 0; }
    function solved() { return (S[0] === 1 && !S[1] && !S[2]) || (S[2] === 1 && !S[3] && !S[0]); }
    function paint() {
      var x = (S0[3] - S0[1]) / (S0[0] - S0[2]);
      vis.innerHTML = '<svg viewBox="0 0 520 250" style="width:520px"><path class="bfoot" d="M260 30 L232 244 H288 Z"/><path class="bbeam" d="M70 30 H450"/><circle class="bpiv" cx="260" cy="30" r="7"/>'
        + panSvg(130, S[0], S[1]) + panSvg(390, S[2], S[3]) + "</svg>";
      var rows = [tex(balEq(S0), true)].concat(hist);
      out.innerHTML = rows2html(rows);
      var k = divK(); bk.textContent = k || "n";
      B.u.disabled = !(S[1] && S[3]) || solved(); B.x.disabled = !(S[0] && S[2]) || solved(); B.d.disabled = !k;
      if (solved()) info.innerHTML = '<span class="ok">✓ ' + fill(T(L3("Ja hem aïllat la x: {s}. Comprovació en l'equació inicial: {c}.", "Ya hemos despejado la x: {s}. Comprobación en la ecuación inicial: {c}.", "We've isolated x: {s}. Check in the original equation: {c}.")), { s: tex("x=" + x), c: tex(subSide(S0[0], S0[1], x) + "=" + (S0[0] * x + S0[1])) + " ; " + tex(subSide(S0[2], S0[3], x) + "=" + (S0[2] * x + S0[3])) + " ✓" }) + "</span>";
      else info.innerHTML = "💡 " + T(L3("Fes el mateix als dos plats perquè la balança continue equilibrada. Objectiu: deixar una sola x en un plat i només unitats en l'altre.", "Haz lo mismo en los dos platos para que la balanza siga equilibrada. Objetivo: dejar una sola x en un plato y solo unidades en el otro.", "Do the same to both pans so the scale stays balanced. Goal: one x alone in one pan and only units in the other."));
    }
    function op(o) {
      var lab;
      if (o === "u" && S[1] && S[3]) { S[1]--; S[3]--; lab = T(L3("Traiem 1 unitat de cada plat:", "Quitamos 1 unidad de cada plato:", "Take 1 unit from each pan:")); }
      else if (o === "x" && S[0] && S[2]) { S[0]--; S[2]--; lab = T(L3("Traiem una x de cada plat:", "Quitamos una x de cada plato:", "Take one x from each pan:")); }
      else if (o === "d") { var k = divK(); if (!k) return; if (S[0]) { S[0] = 1; S[3] /= k; } else { S[2] = 1; S[1] /= k; } lab = fill(T(L3("Repartim cada plat en {k} parts iguals i ens quedem amb una:", "Repartimos cada plato en {k} partes iguales y nos quedamos con una:", "Split each pan into {k} equal parts and keep one:")), { k: k }); }
      else return;
      hist.push(lab + tex(balEq(S), true)); paint();
    }
    function load(s) { S0 = s.slice(); S = s.slice(); hist = []; paint(); }
    function rnd() {
      var x, a, c, b, d;
      do { x = rint(1, 5); a = rint(1, 5); c = rint(0, a - 1); b = rint(0, 7); d = (a - c) * x + b; } while (a + b > 14 || c + d > 14 || (a === 1 && !c && !b));
      var s = [a, b, c, d];
      load(Math.random() < .3 ? [c, d, a, b] : s);
    }
    ["u", "x", "d"].forEach(function (o) { B[o].addEventListener("click", function () { op(o); }); });
    B.r.addEventListener("click", function () { load(S0); });
    B.n.addEventListener("click", rnd);
    quickBind(w, function (b) { load(b.map(Number)); });
    onLang(paint);
  }

  /* ---------- 6.5 és solució? ---------- */
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
      if (isZero(diff)) info.innerHTML = "💡 " + T(L3("A més, els dos membres són iguals un cop operats: és una <b>identitat</b>, i qualsevol valor és solució.", "Además, los dos miembros son iguales una vez operados: es una <b>identidad</b>, y cualquier valor es solución.", "What's more, both sides are the same once worked out: it's an <b>identity</b>, so every value is a solution."));
    }
    [I.e, I.x].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.e.value = v[0]; I.x.value = v[1]; paint(); });
    onLang(paint);
  }

  /* ---------- 6.6-6.8 resolutor ---------- */
  function solverWidget(id) {
    var w = document.getElementById(id); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    function paint() {
      var E = readEq(I.e.value); info.innerHTML = "";
      if (!E) { out.innerHTML = ""; info.innerHTML = warn(u("bad")); return; }
      out.innerHTML = rows2html(solve1(E).rows);
    }
    I.e.addEventListener("input", paint);
    quickBind(w, function (v) { I.e.value = v[0]; paint(); });
    onLang(paint);
  }

  /* ---------- 6.9 planteja i resol ---------- */
  var PLAN = {
    c: { p: 84, q: "", pl: L3("Suma", "Suma", "Sum"), ql: null,
      st: L3("La suma de tres nombres consecutius és {p}. Quins són?", "La suma de tres números consecutivos es {p}. ¿Cuáles son?", "Three consecutive numbers add up to {p}. What are they?"),
      x: L3("el menor dels tres nombres; els altres són x + 1 i x + 2", "el menor de los tres números; los otros son x + 1 y x + 2", "the smallest number; the others are x + 1 and x + 2"),
      eq: function (p) { return "x+(x+1)+(x+2)=" + p; },
      ok: function (s) { return s.d === 1; },
      ans: function (s) { return fill(T(L3("Els nombres són {a}, {b} i {c}.", "Los números son {a}, {b} y {c}.", "The numbers are {a}, {b} and {c}.")), { a: s.n, b: s.n + 1, c: s.n + 2 }); },
      ko: L3("La solució no és un nombre enter: no hi ha tres nombres consecutius que sumen això (la suma ha de ser múltiple de 3).", "La solución no es un número entero: no hay tres números consecutivos que sumen eso (la suma tiene que ser múltiplo de 3).", "The solution isn't a whole number: no three consecutive numbers add up to that (the sum must be a multiple of 3).") },
    e: { p: 38, q: 8, pl: L3("Mare", "Madre", "Mother"), ql: L3("Fill", "Hijo", "Son"),
      st: L3("Una mare té {p} anys i el seu fill, {q}. D'ací a quants anys la mare tindrà el doble d'edat que el fill?", "Una madre tiene {p} años y su hijo, {q}. ¿Dentro de cuántos años la madre tendrá el doble de edad que el hijo?", "A mother is {p} and her son is {q}. In how many years will the mother be twice as old as her son?"),
      x: L3("els anys que han de passar; la mare tindrà {p} + x anys i el fill, {q} + x", "los años que tienen que pasar; la madre tendrá {p} + x años y el hijo, {q} + x", "the number of years; the mother will be {p} + x and the son {q} + x"),
      eq: function (p, q) { return p + "+x=2(" + q + "+x)"; },
      ok: function (s, p, q) { return s.d === 1 && q + s.n >= 0; },
      ans: function (s, p, q) {
        return s.n > 0 ? fill(T(L3("D'ací a {x} anys (la mare en tindrà {m} i el fill {f}).", "Dentro de {x} años (la madre tendrá {m} y el hijo {f}).", "In {x} years (the mother will be {m} and the son {f}).")), { x: s.n, m: p + s.n, f: q + s.n })
          : s.n === 0 ? T(L3("Ara mateix ja té el doble.", "Ahora mismo ya tiene el doble.", "She is already twice as old right now."))
          : fill(T(L3("La solució és negativa: no passarà, però <b>fa {x} anys</b> sí que tenia el doble ({m} i {f}).", "La solución es negativa: no pasará, pero <b>hace {x} años</b> sí que tenía el doble ({m} y {f}).", "The solution is negative: it won't happen, but <b>{x} years ago</b> she was twice as old ({m} and {f}).")), { x: -s.n, m: p + s.n, f: q + s.n });
      },
      ko: L3("Amb aquestes edats no té sentit (el fill tindria una edat negativa).", "Con estas edades no tiene sentido (el hijo tendría una edad negativa).", "With these ages it doesn't make sense (the son would have a negative age).") },
    r: { p: 54, q: 3, pl: L3("Perímetre", "Perímetro", "Perimeter"), ql: L3("Diferència", "Diferencia", "Difference"),
      st: L3("El perímetre d'un rectangle és {p} cm i la base fa {q} cm més que l'altura. Quant mesura cada costat?", "El perímetro de un rectángulo es {p} cm y la base mide {q} cm más que la altura. ¿Cuánto mide cada lado?", "A rectangle has a perimeter of {p} cm and its base is {q} cm longer than its height. How long is each side?"),
      x: L3("l'altura; la base és x + {q}", "la altura; la base es x + {q}", "the height; the base is x + {q}"),
      eq: function (p, q) { return "2x+2(x+" + q + ")=" + p; },
      ok: function (s) { return s.n > 0; },
      ans: function (s, p, q) { return fill(T(L3("Altura {h} cm i base {b} cm.", "Altura {h} cm y base {b} cm.", "Height {h} cm and base {b} cm.")), { h: tex(ntd(s)), b: tex(ntd(radd(s, rat(q)))) }); },
      ko: L3("L'altura no pot ser zero ni negativa: amb aquestes dades no hi ha cap rectangle.", "La altura no puede ser cero ni negativa: con estos datos no hay ningún rectángulo.", "The height can't be zero or negative: no rectangle fits these numbers.") },
    d: { p: 130, q: 20, pl: L3("Total (€)", "Total (€)", "Total (€)"), ql: L3("Diferència (€)", "Diferencia (€)", "Difference (€)"),
      st: L3("Repartim {p} € entre dues persones de manera que una rep {q} € més que l'altra. Quant rep cadascuna?", "Repartimos {p} € entre dos personas de forma que una recibe {q} € más que la otra. ¿Cuánto recibe cada una?", "We share {p} € between two people so that one gets {q} € more than the other. How much does each get?"),
      x: L3("el que rep la que en rep menys; l'altra rep x + {q}", "lo que recibe la que recibe menos; la otra recibe x + {q}", "the smaller share; the other gets x + {q}"),
      eq: function (p, q) { return "x+(x+" + q + ")=" + p; },
      ok: function (s) { return s.n > 0; },
      ans: function (s, p, q) { return fill(T(L3("Una rep {a} € i l'altra {b} €.", "Una recibe {a} € y la otra {b} €.", "One gets {a} € and the other {b} €.")), { a: tex(ntd(s)), b: tex(ntd(radd(s, rat(q)))) }); },
      ko: L3("Amb aquestes dades una de les parts seria zero o negativa.", "Con estos datos una de las partes sería cero o negativa.", "With these numbers one of the shares would be zero or negative.") }
  };
  function wPlan() {
    var w = document.getElementById("w-plan"); if (!w) return;
    var I = inputs(w), pq = w.querySelector(".pq"), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), kind = "c";
    var lp = w.querySelector('.pl[data-p="p"]'), lq = w.querySelector('.pl[data-p="q"]');
    function load(k) { kind = k; I.p.value = PLAN[k].p; I.q.value = PLAN[k].q; paint(); }
    function paint() {
      var K = PLAN[kind], p = parseInt(I.p.value, 10), q = parseInt(I.q.value, 10);
      lp.textContent = T(K.pl); lq.textContent = K.ql ? T(K.ql) : ""; I.q.parentNode.style.display = K.ql ? "" : "none";
      info.innerHTML = "";
      if (!(p > 0 && p < 10000) || (K.ql && !(q >= 0 && q < 10000))) { pq.innerHTML = ""; out.innerHTML = ""; info.innerHTML = warn(T(L3("Escriu nombres naturals (menors que 10 000).", "Escribe números naturales (menores que 10 000).", "Type whole numbers (less than 10,000)."))); return; }
      pq.innerHTML = "<strong>" + fill(T(K.st), { p: p, q: q }) + "</strong>";
      var eq = K.eq(p, q), E = readEq(eq), R = solve1(E), rows = [];
      rows.push(T(L3("1. Incògnita:", "1. Incógnita:", "1. Unknown:")) + " " + tex("x") + " = " + fill(T(K.x), { p: p, q: q }) + ".");
      rows.push(T(L3("2. Plantegem l'equació:", "2. Planteamos la ecuación:", "2. Set up the equation:")) + tex(texRaw(E.ls) + "=" + texRaw(E.rs), true));
      rows.push(T(L3("3. La resolem:", "3. La resolvemos:", "3. Solve it:")) + '<div class="sub-steps">' + rows2html(R.rows.slice(1)) + "</div>");
      var s = R.sols && R.sols[0] && R.sols[0].r;
      if (s && K.ok(s, p, q)) rows.push('<span class="ok">' + T(L3("4. Resposta:", "4. Respuesta:", "4. Answer:")) + " " + K.ans(s, p, q) + "</span>");
      else rows.push('<span class="ko">' + T(L3("4. Revisem si té sentit:", "4. Revisamos si tiene sentido:", "4. Does it make sense?")) + " " + T(K.ko) + "</span>");
      out.innerHTML = rows2html(rows);
    }
    segBind(w, load);
    [I.p, I.q].forEach(function (x) { x.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  var TRAD = [
    [L3("El doble d'un nombre més {a}", "El doble de un número más {a}", "Twice a number plus {a}"), "2x+{a}"],
    [L3("El triple d'un nombre menys {a}", "El triple de un número menos {a}", "Three times a number minus {a}"), "3x-{a}"],
    [L3("La meitat d'un nombre més {a}", "La mitad de un número más {a}", "Half a number plus {a}"), "x/2+{a}"],
    [L3("El doble de la suma d'un nombre i {a}", "El doble de la suma de un número y {a}", "Twice the sum of a number and {a}"), "2(x+{a})"],
    [L3("El quadrat d'un nombre menys {a}", "El cuadrado de un número menos {a}", "The square of a number minus {a}"), "x^2-{a}"],
    [L3("Un nombre més el seu triple", "Un número más su triple", "A number plus three times the number"), "x+3x"],
    [L3("La tercera part d'un nombre menys {a}", "La tercera parte de un número menos {a}", "A third of a number minus {a}"), "x/3-{a}"],
    [L3("{a} menys el doble d'un nombre", "{a} menos el doble de un número", "{a} minus twice a number"), "{a}-2x"],
    [L3("El quàdruple de la diferència entre un nombre i {a}", "El cuádruple de la diferencia entre un número y {a}", "Four times the difference between a number and {a}"), "4(x-{a})"],
    [L3("La suma d'un nombre i el seu consecutiu", "La suma de un número y su consecutivo", "The sum of a number and the next number"), "x+(x+1)"],
    [L3("El quíntuple d'un nombre més la seua meitat", "El quíntuple de un número más su mitad", "Five times a number plus half of it"), "5x+x/2"],
    [L3("L'edat d'una persona d'ací a {a} anys, si ara en té x", "La edad de una persona dentro de {a} años, si ahora tiene x", "A person's age in {a} years' time, if they are x now"), "x+{a}"],
    [L3("El doble d'un nombre menys el seu quadrat", "El doble de un número menos su cuadrado", "Twice a number minus its square"), "2x-x^2"]
  ];
  function rawOf(list) { return list.map(function (t, i) { var c = t[0], k = t[1], s = Math.abs(c) === 1 && k ? "" : String(Math.abs(c)); return (c < 0 ? "-" : i ? "+" : "") + s + (k === 2 ? "x^2" : k === 1 ? "x" : ""); }).join(""); }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = rint(0, i), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function eqDrill(raw) {
    var E = readEq(raw), R = solve1(E);
    return { t: "num", ans: R.sols[0].r, q: function () { return T(L3("Resol:", "Resuelve:", "Solve:")) + " $" + texRaw(E.ls) + "=" + texRaw(E.rs) + "$"; }, s: function () { return rows2html(solve1(E).rows); } };
  }
  function linR(a, b) { return rawOf([[a, 1], [b, 0]].filter(function (t) { return t[0]; })) || "0"; }
  var KW = { 2: L3("doble", "doble", "twice"), 3: L3("triple", "triple", "three times"), 4: L3("quàdruple", "cuádruple", "four times"), 5: L3("quíntuple", "quíntuple", "five times") };
  var GEN = {
    trad: function () {
      var t = pick(TRAD), a = rint(2, 9), raw = t[1].replace(/\{a\}/g, a);
      return { t: "expr", vars: ["x"], ans: parse(raw), q: function () { return fill(T(t[0]), { a: a }) + "."; }, s: function () { return tex("\\boxed{" + texRaw(raw) + "}", true) + (!isReduced(raw, parse(raw)) ? hint(T(L3("També és correcte escriure-ho reduït:", "También es correcto escribirlo reducido:", "Writing it simplified is also correct:")) + " " + tex(ptex(parse(raw)))) : ""); } };
    },
    val: function () {
      var f = rint(0, 3), a = rnz(-6, 6), b = rnz(-9, 9), raw;
      if (f === 0) raw = linR(a, b); else if (f === 1) raw = rawOf([[pick([1, 1, 2, 3, -1]), 2], [b, 0]]); else if (f === 2) raw = (a === 1 ? "" : a === -1 ? "-" : a) + "(x" + (b < 0 ? b : "+" + b) + ")"; else raw = rawOf([[1, 2], [a, 1]]);
      var p = parse(raw), x = rint(-4, 5), o = { x: rat(x) };
      return { t: "num", ans: evalAt(p, o), q: function () { return fill(T(L3("Calcula el valor numèric de {e} per a {x}.", "Calcula el valor numérico de {e} para {x}.", "Evaluate {e} for {x}.")), { e: "$" + texRaw(raw) + "$", x: "$x=" + x + "$" }); }, s: function () { return rows2html(valRows(raw, p, o)); } };
    },
    mono: function () {
      var L = shuffle(["x", "y", "z", "a", "b"]).slice(0, rint(1, 3)).sort(), e = {}, c = rnz(-9, 9);
      L.forEach(function (v) { e[v] = pick([1, 1, 2, 3, 4]); });
      var m = mono(rat(c), e), g = tdeg(e), ask = Math.random() < .5 ? "g" : "c";
      return { t: "num", ans: ask === "g" ? rat(g) : rat(c), q: function () { return fill(T(ask === "g" ? L3("Quin és el grau del monomi {m}?", "¿Cuál es el grado del monomio {m}?", "What is the degree of the monomial {m}?") : L3("Quin és el coeficient del monomi {m}?", "¿Cuál es el coeficiente del monomio {m}?", "What is the coefficient of the monomial {m}?")), { m: "$" + ttex(m, true) + "$" }); },
        s: function () { return tex(ask === "g" ? "\\text{" + T(L3("grau", "grado", "degree")) + "}=" + L.map(function (v) { return e[v]; }).join("+") + "=\\boxed{" + g + "}" : "\\text{" + T(L3("coeficient", "coeficiente", "coefficient")) + "}=\\boxed{" + c + "}", true) + (ask === "c" && Math.abs(c) === 1 ? hint(T(L3("Quan el coeficient és 1 o −1, no s'escriu el 1.", "Cuando el coeficiente es 1 o −1, no se escribe el 1.", "When the coefficient is 1 or −1, the 1 isn't written."))) : ""); } };
    },
    red: function () {
      var list, sq = Math.random() < .3;
      do {
        list = [[rnz(-7, 9), 1], [rnz(-7, 7), 1], [rnz(-9, 9), 0], [rnz(-9, 9), 0]];
        if (Math.random() < .4) list.push([rnz(-5, 5), 1]);
        if (sq) list.push([rnz(-4, 4), 2], [rnz(-4, 4), 2]);
        shuffle(list);
      } while (list[0][0] < 0 && Math.random() < .7);
      var raw = rawOf(list), p = parse(raw);
      return { t: "expr", red: true, vars: ["x"], ans: p, q: function () { return T(L3("Redueix:", "Reduce:", "Simplify:")) + " $" + texRaw(raw) + "$"; },
        s: function () { var ks = [2, 1, 0].map(function (k) { var l = list.filter(function (t) { return t[1] === k; }); return l.length ? (l.length > 1 ? "(" + texRaw(rawOf(l)) + ")" : texRaw(rawOf(l))) : null; }).filter(Boolean); return tex(ks.join("+").replace(/\+-/g, "-") + "=\\boxed{" + ptex(p) + "}", true); } };
    },
    mul: function () {
      var f = rint(0, 4), a = rnz(-6, 6), b = rnz(-7, 7), c = rnz(-5, 5), raw;
      if (f === 0) raw = (a < 0 ? "(" + a + "x)" : a + "x") + "*" + (c < 0 ? "(" + c + "x)" : c + "x");
      else if (f === 1) raw = a + "(x" + (b < 0 ? b : "+" + b) + ")";
      else if (f === 2) raw = "-(" + linR(rnz(1, 6), b) + ")";
      else if (f === 3) raw = Math.abs(a) + "(" + linR(rnz(1, 5), b) + ")" + (c < 0 ? c : "+" + c) + "x";
      else raw = Math.abs(a) + "(x" + (b < 0 ? b : "+" + b) + ")" + (c < 0 ? "-" + (-c) : "+" + c) + "(x" + (a < 0 ? "-" : "+") + rint(1, 6) + ")";
      var p = parse(raw);
      return { t: "expr", red: true, vars: ["x"], ans: p, q: function () { return T(L3("Calcula i redueix:", "Calcula y reduce:", "Work out and simplify:")) + " $" + texRaw(raw) + "$"; },
        s: function () { var tp = termPolys(clean(raw)), m = []; tp.forEach(function (t) { terms(t.p).forEach(function (x) { m.push(x); }); }); var ex = joinMonos(m), rd = ptex(p); return tex(texRaw(raw) + "=" + (ex !== rd ? ex + "=" : "") + "\\boxed{" + rd + "}", true); } };
    },
    sol: function () {
      var s = rint(-4, 6), a = rnz(-5, 6), c, b = rnz(-9, 9);
      do { c = rnz(-4, 4); } while (c === a);
      var d = (a - c) * s + b, raw = linR(a, b) + "=" + linR(c, d), E = readEq(raw), tr = s + (Math.random() < .5 ? 0 : pick([-2, -1, 1, 2])), o = { x: rat(tr) };
      var vl = evalAt(E.L, o), vr = evalAt(E.R, o), yes = req(vl, vr);
      return { t: "yn", ans: yes, q: function () { return fill(T(L3("És {x} solució de {e}?", "¿Es {x} solución de {e}?", "Is {x} a solution of {e}?")), { x: "$x=" + tr + "$", e: "$" + texRaw(E.ls) + "=" + texRaw(E.rs) + "$" }); },
        s: function () { return tex(substRaw(E.ls, "x", rat(tr)) + "=" + nt(vl) + "\\qquad " + substRaw(E.rs, "x", rat(tr)) + "=" + nt(vr), true) + hint(yes ? T(L3("Els dos membres valen el mateix: sí que és solució.", "Los dos miembros valen lo mismo: sí es solución.", "Both sides are equal: it is a solution.")) : T(L3("Els membres donen resultats diferents: no és solució.", "Los miembros dan resultados distintos: no es solución.", "The sides give different results: it isn't a solution."))); } };
    },
    eq1: function () {
      var s = rint(-6, 9), f = rint(0, 4), a = rnz(-6, 7), b = rnz(-9, 9), c, raw;
      if (f === 0) raw = "x" + (b < 0 ? b : "+" + b) + "=" + (s + b);
      else if (f === 1) { a = rnz(-9, 9); if (a === 1) a = 2; raw = (a === -1 ? "-" : a) + "x=" + a * s; }
      else if (f === 2) { var k = rint(2, 6); s = k * rint(-3, 5); raw = "x/" + k + "=" + s / k; }
      else if (f === 3) { if (a === 1) a = 3; raw = linR(a, b) + "=" + (a * s + b); }
      else { do { c = rnz(-5, 6); } while (c === a); raw = linR(a, b) + "=" + linR(c, (a - c) * s + b); }
      return eqDrill(raw);
    },
    eq2: function () {
      var s = rint(-4, 8), k = rnz(-5, 6), b = rnz(-7, 7), m = rnz(-4, 4), e = rnz(-6, 6), two = Math.random() < .5, c, raw, L;
      if (k === 1) k = 2;
      L = (k === -1 ? "-" : k) + "(x" + (b < 0 ? b : "+" + b) + ")";
      var lv = k * (s + b);
      if (two) { L += (m < 0 ? "-" + (-m) : "+" + m) + "(x" + (e < 0 ? e : "+" + e) + ")"; lv += m * (s + e); }
      var A = k + (two ? m : 0);
      do { c = rnz(-4, 5); } while (c === A);
      raw = L + "=" + linR(c, lv - c * s);
      return eqDrill(raw);
    },
    eq3: function () {
      var f = rint(0, 3), a = pick([2, 3, 4, 5, 6]), b, s, raw;
      if (f === 0) { s = a * rint(-3, 6); var p = rnz(-6, 6); raw = "x/" + a + (p < 0 ? p : "+" + p) + "=" + (s / a + p); }
      else if (f === 1) { var pr = pick([[2, 3], [2, 4], [2, 6], [3, 6], [3, 4], [4, 6], [2, 5]]); if (Math.random() < .5) pr.reverse(); a = pr[0]; b = pr[1]; var M = lcm(a, b); s = M * rint(1, M > 10 ? 2 : 3); raw = "x/" + a + (Math.random() < .5 ? "+x/" + b + "=" + (s / a + s / b) : "-x/" + b + "=" + (s / a - s / b)); }
      else if (f === 2) { var p2 = rnz(-5, 5); s = a * rint(-2, 6) - p2; raw = "(x" + (p2 < 0 ? p2 : "+" + p2) + ")/" + a + "=" + (s + p2) / a; }
      else { do { b = pick([2, 3, 4, 5]); } while (b === a); var q1 = rnz(-4, 4), q2 = rnz(-4, 4), t; for (t = 0; t < 200; t++) { s = rint(-10, 20); if ((s + q1) % a === 0 && (s + q2) % b === 0) break; } if (t === 200) return GEN.eq3(); raw = "(x" + (q1 < 0 ? q1 : "+" + q1) + ")/" + a + "-(x" + (q2 < 0 ? q2 : "+" + q2) + ")/" + b + "=" + ((s + q1) / a - (s + q2) / b); }
      return eqDrill(raw);
    },
    prob: function () {
      var f = rint(0, 4), x, raw, st;
      if (f === 0) { var k = rint(2, 5), a = rnz(-15, 20); x = rint(2, 20); raw = k + "x" + (a < 0 ? a : "+" + a) + "=" + (k * x + a); st = fill(T(a > 0 ? L3("Si al {k} d'un nombre li sumem {a}, obtenim {r}. Quin és el nombre?", "Si al {k} de un número le sumamos {a}, obtenemos {r}. ¿Cuál es el número?", "If we add {a} to {k} a number, we get {r}. What is the number?") : L3("Si al {k} d'un nombre li restem {a}, obtenim {r}. Quin és el nombre?", "Si al {k} de un número le restamos {a}, obtenemos {r}. ¿Cuál es el número?", "If we subtract {a} from {k} a number, we get {r}. What is the number?")), { k: T(KW[k]), a: Math.abs(a), r: k * x + a }); }
      else if (f === 1) { var n = rint(2, 3); x = rint(5, 60); var S = n === 2 ? 2 * x + 1 : 3 * x + 3; raw = n === 2 ? "x+(x+1)=" + S : "x+(x+1)+(x+2)=" + S; st = fill(T(L3("La suma de {n} nombres consecutius és {s}. Quin és el menor?", "La suma de {n} números consecutivos es {s}. ¿Cuál es el menor?", "{n} consecutive numbers add up to {s}. What is the smallest?")), { n: n === 2 ? T(L3("dos", "dos", "Two")) : T(L3("tres", "tres", "Three")), s: S }); }
      else if (f === 2) { var k2 = rint(2, 3), C = rint(3, 12); x = rint(1, 12); var Mo = k2 * (C + x) - x; if (Mo > 55 || Mo - C < 18) return GEN.prob(); raw = Mo + "+x=" + k2 + "(" + C + "+x)"; st = fill(T(L3("Un pare té {m} anys i la seua filla, {c}. D'ací a quants anys l'edat del pare serà el {k} que la de la filla?", "Un padre tiene {m} años y su hija, {c}. ¿Dentro de cuántos años la edad del padre será el {k} que la de la hija?", "A father is {m} and his daughter is {c}. In how many years will he be {k} as old as her?")), { m: Mo, c: C, k: k2 === 2 ? T(L3("doble", "doble", "twice")) : T(L3("triple", "triple", "three times")) }); }
      else if (f === 3) { var D = rint(1, 9) * 5; x = rint(4, 40) * 5; var Tt = 2 * x + D; raw = "x+(x+" + D + ")=" + Tt; st = fill(T(L3("Repartim {t} € entre dues germanes de manera que la major rep {d} € més que la menor. Quant rep la menor?", "Repartimos {t} € entre dos hermanas de forma que la mayor recibe {d} € más que la menor. ¿Cuánto recibe la menor?", "We share {t} € between two sisters so the older one gets {d} € more than the younger one. How much does the younger one get?")), { t: Tt, d: D }); }
      else { var q = rint(1, 9); x = rint(2, 20); var P = 4 * x + 2 * q; raw = "2x+2(x+" + q + ")=" + P; st = fill(T(L3("El perímetre d'un rectangle és {p} cm i la base fa {q} cm més que l'altura. Quant fa l'altura (en cm)?", "El perímetro de un rectángulo es {p} cm y la base mide {q} cm más que la altura. ¿Cuánto mide la altura (en cm)?", "A rectangle has a perimeter of {p} cm and its base is {q} cm longer than its height. How long is the height (in cm)?")), { p: P, q: q }); }
      var E = readEq(raw);
      return { t: "num", ans: rat(x), q: function () { return st; }, s: function () { return T(L3("Equació:", "Ecuación:", "Equation:")) + " " + tex(texRaw(E.ls) + "=" + texRaw(E.rs)) + rows2html(solve1(E).rows.slice(1)); } };
    }
  };
  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, res = 0, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore");
    function paint() {
      dq.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (done) info.innerHTML = (res === 1 ? '<span class="ok">✓ ' + u("right") + "</span>" : '<span class="ko">✗ ' + u(res === 2 ? "notRed" : "wrong") + "</span>") + '<div class="dsol">' + u("sol") + " " + q.s() + "</div>";
    }
    function check() {
      if (done) return;
      var raw = inp.value.trim(), good;
      if (!raw) { info.innerHTML = warn(q.t === "yn" ? u("yn") : q.t === "num" ? u("num") : u("badE")); return; }
      if (q.t === "yn") {
        var a = raw.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z]/g, "");
        var yes = ["si", "s", "yes", "y"].indexOf(a) >= 0, no = ["no", "n"].indexOf(a) >= 0;
        if (!yes && !no) { info.innerHTML = warn(u("yn")); return; }
        good = yes === q.ans ? 1 : 0;
      } else if (q.t === "num") {
        var p = parse(clean(raw).replace(/^[a-z]=/i, ""));
        if (!p || !isConst(p)) { info.innerHTML = warn(u("num")); return; }
        good = req(cval(p), q.ans) ? 1 : 0;
      } else {
        var e = readE(raw);
        if (!e) { info.innerHTML = warn(u("badE")); return; }
        if (q.vars && pvars(e.p).some(function (v) { return q.vars.indexOf(v) < 0; })) { info.innerHTML = warn(u("onlyX")); return; }
        good = peq(e.p, q.ans) ? 1 : 0;
        if (good && q.red && !isReduced(raw, e.p)) good = 2;
      }
      done = true; tot++; res = good; if (good === 1) ok++;
      paint();
    }
    function fresh() { q = GEN[kind](); done = false; inp.value = ""; info.innerHTML = ""; paint(); }
    w.querySelector('[data-a="check"]').addEventListener("click", check);
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); inp.focus(); });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    onLang(paint);
  }

  /* ---------- qüestionari ---------- */
  var QUIZ = [
    { q: { va: "Com s'escriu «el triple d'un nombre menys 5»?", es: "¿Cómo se escribe «el triple de un número menos 5»?", en: "How do you write “three times a number minus 5”?" },
      o: [{ va: "$3(x-5)$" }, { va: "$3x-5$" }, { va: "$x^3-5$" }, { va: "$5-3x$" }], a: 1,
      e: { va: "Primer multipliquem per 3 i després restem 5: $3x-5$. $3(x-5)$ seria «el triple de la diferència».", es: "Primero multiplicamos por 3 y después restamos 5: $3x-5$. $3(x-5)$ sería «el triple de la diferencia».", en: "Multiply by 3 first, then subtract 5: $3x-5$. $3(x-5)$ would be “three times the difference”." } },
    { q: { va: "Si $x$ és un nombre, quin és el seu consecutiu?", es: "Si $x$ es un número, ¿cuál es su consecutivo?", en: "If $x$ is a number, what is the next number?" },
      o: [{ va: "$2x$" }, { va: "$x+1$" }, { va: "$x-1$" }, { va: "$x^2$" }], a: 1,
      e: { va: "El consecutiu és el següent: una unitat més, $x+1$.", es: "El consecutivo es el siguiente: una unidad más, $x+1$.", en: "The next number is one more: $x+1$." } },
    { q: { va: "Quin és el valor numèric de $2x^2-3$ per a $x=-2$?", es: "¿Cuál es el valor numérico de $2x^2-3$ para $x=-2$?", en: "What is the value of $2x^2-3$ when $x=-2$?" },
      o: [{ va: "$-11$" }, { va: "$5$" }, { va: "$13$" }, { va: "$-7$" }], a: 1,
      e: { va: "$2\\cdot(-2)^2-3=2\\cdot4-3=5$. El quadrat d'un negatiu és positiu.", es: "$2\\cdot(-2)^2-3=2\\cdot4-3=5$. El cuadrado de un negativo es positivo.", en: "$2\\cdot(-2)^2-3=2\\cdot4-3=5$. The square of a negative is positive." } },
    { q: { va: "Quin és el grau del monomi $-4x^2y^3$?", es: "¿Cuál es el grado del monomio $-4x^2y^3$?", en: "What is the degree of the monomial $-4x^2y^3$?" },
      o: [{ va: "$3$" }, { va: "$-4$" }, { va: "$5$" }, { va: "$6$" }], a: 2,
      e: { va: "Sumem els exponents de les lletres: $2+3=5$.", es: "Sumamos los exponentes de las letras: $2+3=5$.", en: "Add the exponents of the letters: $2+3=5$." } },
    { q: { va: "Quin monomi és semblant a $5ab^2$?", es: "¿Qué monomio es semejante a $5ab^2$?", en: "Which monomial is a like term of $5ab^2$?" },
      o: [{ va: "$5a^2b$" }, { va: "$-ab^2$" }, { va: "$5ab$" }, { va: "$5a^2b^2$" }], a: 1,
      e: { va: "Ha de tindre la mateixa part literal, $ab^2$. El coeficient pot ser diferent.", es: "Tiene que tener la misma parte literal, $ab^2$. El coeficiente puede ser distinto.", en: "It must have the same literal part, $ab^2$. The coefficient can differ." } },
    { q: { va: "$7x-2x+x=$", es: "$7x-2x+x=$", en: "$7x-2x+x=$" },
      o: [{ va: "$5x$" }, { va: "$6x$" }, { va: "$4x$" }, { va: "$6x^3$" }], a: 1,
      e: { va: "Sumem els coeficients: $7-2+1=6$. Recorda que $x=1x$.", es: "Sumamos los coeficientes: $7-2+1=6$. Recuerda que $x=1x$.", en: "Add the coefficients: $7-2+1=6$. Remember $x=1x$." } },
    { q: { va: "Es pot reduir $4x+3$?", es: "¿Se puede reducir $4x+3$?", en: "Can $4x+3$ be simplified?" },
      o: [{ va: "Sí, és $7x$", es: "Sí, es $7x$", en: "Yes, it's $7x$" }, { va: "Sí, és $7$", es: "Sí, es $7$", en: "Yes, it's $7$" }, { va: "No, no són semblants", es: "No, no son semejantes", en: "No, they aren't like terms" }], a: 2,
      e: { va: "$4x$ i $3$ no són semblants: la suma es deixa indicada.", es: "$4x$ y $3$ no son semejantes: la suma se deja indicada.", en: "$4x$ and $3$ aren't like terms: the sum stays as it is." } },
    { q: { va: "$3x\\cdot4x=$", es: "$3x\\cdot4x=$", en: "$3x\\cdot4x=$" },
      o: [{ va: "$7x$" }, { va: "$12x$" }, { va: "$12x^2$" }, { va: "$7x^2$" }], a: 2,
      e: { va: "Multipliquem coeficients ($3\\cdot4=12$) i lletres ($x\\cdot x=x^2$).", es: "Multiplicamos coeficientes ($3\\cdot4=12$) y letras ($x\\cdot x=x^2$).", en: "Multiply the coefficients ($3\\cdot4=12$) and the letters ($x\\cdot x=x^2$)." } },
    { q: { va: "$-2(x-3)=$", es: "$-2(x-3)=$", en: "$-2(x-3)=$" },
      o: [{ va: "$-2x-6$" }, { va: "$-2x+6$" }, { va: "$-2x-3$" }, { va: "$2x+6$" }], a: 1,
      e: { va: "Multipliquem $-2$ per cada terme: $-2\\cdot x=-2x$ i $(-2)\\cdot(-3)=+6$.", es: "Multiplicamos $-2$ por cada término: $-2\\cdot x=-2x$ y $(-2)\\cdot(-3)=+6$.", en: "Multiply each term by $-2$: $-2\\cdot x=-2x$ and $(-2)\\cdot(-3)=+6$." } },
    { q: { va: "Quin d'aquests nombres és la solució de $4x-1=2x+7$?", es: "¿Cuál de estos números es la solución de $4x-1=2x+7$?", en: "Which of these numbers solves $4x-1=2x+7$?" },
      o: [{ va: "$3$" }, { va: "$4$" }, { va: "$1$" }, { va: "$-4$" }], a: 1,
      e: { va: "$4\\cdot4-1=15$ i $2\\cdot4+7=15$ ✓.", es: "$4\\cdot4-1=15$ y $2\\cdot4+7=15$ ✓.", en: "$4\\cdot4-1=15$ and $2\\cdot4+7=15$ ✓." } },
    { q: { va: "En $x+8=3$, en transposar el 8 queda…", es: "En $x+8=3$, al transponer el 8 queda…", en: "In $x+8=3$, moving the 8 across gives…" },
      o: [{ va: "$x=3+8$" }, { va: "$x=3-8$" }, { va: "$x=\\frac{3}{8}$" }, { va: "$x=8-3$" }], a: 1,
      e: { va: "El que suma passa restant: $x=3-8=-5$.", es: "Lo que suma pasa restando: $x=3-8=-5$.", en: "What is added moves across subtracted: $x=3-8=-5$." } },
    { q: { va: "Si $-3x=12$, aleshores…", es: "Si $-3x=12$, entonces…", en: "If $-3x=12$, then…" },
      o: [{ va: "$x=4$" }, { va: "$x=-4$" }, { va: "$x=15$" }, { va: "$x=9$" }], a: 1,
      e: { va: "El $-3$ multiplica: passa dividint amb el seu signe, $x=\\frac{12}{-3}=-4$.", es: "El $-3$ multiplica: pasa dividiendo con su signo, $x=\\frac{12}{-3}=-4$.", en: "The $-3$ multiplies: it moves across dividing, sign included, $x=\\frac{12}{-3}=-4$." } },
    { q: { va: "Quina és la solució de $2(x+1)=x+5$?", es: "¿Cuál es la solución de $2(x+1)=x+5$?", en: "What is the solution of $2(x+1)=x+5$?" },
      o: [{ va: "$x=4$" }, { va: "$x=3$" }, { va: "$x=6$" }, { va: "$x=2$" }], a: 1,
      e: { va: "$2x+2=x+5\\Rightarrow 2x-x=5-2\\Rightarrow x=3$.", es: "$2x+2=x+5\\Rightarrow 2x-x=5-2\\Rightarrow x=3$.", en: "$2x+2=x+5\\Rightarrow 2x-x=5-2\\Rightarrow x=3$." } },
    { q: { va: "En $\\frac{x}{3}+1=5$, si multipliquem tots els termes per 3 queda…", es: "En $\\frac{x}{3}+1=5$, si multiplicamos todos los términos por 3 queda…", en: "In $\\frac{x}{3}+1=5$, multiplying every term by 3 gives…" },
      o: [{ va: "$x+1=15$" }, { va: "$x+3=15$" }, { va: "$x+3=5$" }, { va: "$3x+3=15$" }], a: 1,
      e: { va: "Tots els termes es multipliquen per 3, també el 1: $x+3=15$, i $x=12$.", es: "Todos los términos se multiplican por 3, también el 1: $x+3=15$, y $x=12$.", en: "Every term is multiplied by 3, including the 1: $x+3=15$, so $x=12$." } },
    { q: { va: "La suma de dos nombres consecutius és 35. Quina equació ho expressa?", es: "La suma de dos números consecutivos es 35. ¿Qué ecuación lo expresa?", en: "Two consecutive numbers add up to 35. Which equation says this?" },
      o: [{ va: "$2x=35$" }, { va: "$x+(x+1)=35$" }, { va: "$x+1=35$" }, { va: "$x+2x=35$" }], a: 1,
      e: { va: "Si el menor és $x$, el següent és $x+1$: $2x+1=35$, $x=17$. Els nombres són 17 i 18.", es: "Si el menor es $x$, el siguiente es $x+1$: $2x+1=35$, $x=17$. Los números son 17 y 18.", en: "If the smaller is $x$, the next is $x+1$: $2x+1=35$, $x=17$. The numbers are 17 and 18." } },
    { q: { va: "Un pare té 40 anys i el seu fill, 10. D'ací a quants anys el pare tindrà el triple d'edat que el fill?", es: "Un padre tiene 40 años y su hijo, 10. ¿Dentro de cuántos años el padre tendrá el triple de edad que el hijo?", en: "A father is 40 and his son is 10. In how many years will the father be three times as old as his son?" },
      o: [{ va: "$10$" }, { va: "$5$" }, { va: "$20$" }, { va: "$3$" }], a: 1,
      e: { va: "$40+x=3(10+x)\\Rightarrow 40+x=30+3x\\Rightarrow 10=2x\\Rightarrow x=5$. Tindran 45 i 15 anys.", es: "$40+x=3(10+x)\\Rightarrow 40+x=30+3x\\Rightarrow 10=2x\\Rightarrow x=5$. Tendrán 45 y 15 años.", en: "$40+x=3(10+x)\\Rightarrow 40+x=30+3x\\Rightarrow 10=2x\\Rightarrow x=5$. They'll be 45 and 15." } }
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

  var TITLES = { va: "Introducció a l'àlgebra. Equacions de 1r grau · FentMates", es: "Introducción al álgebra. Ecuaciones de 1.er grado · FentMates", en: "Introduction to algebra. First-degree equations · FentMates" };
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
    wPat(); wVal(); wMono(); wTiles(); wRed(); wCheck(); wBal(); solverWidget("w-solve1"); solverWidget("w-solve2"); solverWidget("w-solve3"); wPlan();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
    window.FM16 = { parse: parse, ptex: ptex, readEq: readEq, solve1: solve1, texRaw: texRaw, isReduced: isReduced, valRows: valRows, patEdges: patEdges, GEN: GEN, nt: nt, req: req, peq: peq, evalAt: evalAt, rat: rat };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
