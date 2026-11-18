(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-4eso-a-u11-done", NSEC = 7;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc",
      bad: "No entenc la fórmula. Escriu-la amb la x, per exemple: x^2-3x+1, 2x+5, 12/x o sqrt(x+4).",
      badx: "Escriu un valor de x (un nombre).", num: "Escriu un nombre (pots fer servir coma decimal o una fracció com 5/2).",
      pair: "Escriu el punt com (2, −3) o bé 2; −3.", sol: "Solució:" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro",
      bad: "No entiendo la fórmula. Escríbela con la x, por ejemplo: x^2-3x+1, 2x+5, 12/x o sqrt(x+4).",
      badx: "Escribe un valor de x (un número).", num: "Escribe un número (puedes usar coma decimal o una fracción como 5/2).",
      pair: "Escribe el punto como (2, −3) o bien 2; −3.", sol: "Solución:" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Score", right: "Correct!", wrong: "Not correct.", theme: "Switch between light and dark mode",
      bad: "I can't read the formula. Write it in x, for example: x^2-3x+1, 2x+5, 12/x or sqrt(x+4).",
      badx: "Type a value of x (a number).", num: "Type a number (decimals or a fraction like 5/2 are fine).",
      pair: "Type the point as (2, −3) or 2; −3.", sol: "Solution:" }
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
  function warn(s) { return '<span class="warn">' + s + "</span>"; }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function rnz(a, b) { var k; do { k = rint(a, b); } while (k === 0); return k; }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = rint(0, i), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function inputs(w) { var o = {}; w.querySelectorAll(".tin[data-k]").forEach(function (i) { o[i.dataset.k] = i; }); return o; }
  function quickBind(w, cb) { w.querySelectorAll(".quick button[data-b]").forEach(function (b) { b.addEventListener("click", function () { cb(b.dataset.b.split("|"), b); }); }); }
  function rows2html(rows) { return rows.map(function (x) { return '<div class="hrow">' + x + "</div>"; }).join(""); }

  /* ---------- nombres ---------- */
  var INF = Infinity;
  function near(a, b) { return Math.abs(a - b) < 1e-9; }
  /* nombre en TeX amb coma decimal (com a molt 3 decimals) */
  function nf(v) {
    if (v === INF) return "+\\infty"; if (v === -INF) return "-\\infty";
    var r = Math.round(v * 1000) / 1000; if (near(r, 0)) r = 0;
    return String(r).replace(".", "\\dc ");
  }
  function nfp(v) { return v < 0 ? "(" + nf(v) + ")" : nf(v); }
  /* nombre escrit per l'alumne: "−3", "2,5", "5/2" */
  function numIn(raw) {
    var s = String(raw).replace(/[−–]/g, "-").replace(/\s+/g, "").replace(",", ".");
    var m = s.match(/^(-?\d+(?:\.\d+)?)(?:\/(\d+(?:\.\d+)?))?$/);
    if (!m) return null;
    var v = parseFloat(m[1]); if (m[2]) { if (+m[2] === 0) return null; v /= parseFloat(m[2]); }
    return v;
  }
  function pairIn(raw) {
    var s = String(raw).replace(/[−–]/g, "-").replace(/[()\s]/g, "");
    var parts = s.indexOf(";") >= 0 ? s.split(";") : s.split(/,(?!\d)/);
    if (parts.length !== 2) { var m = s.match(/^(-?\d+),(-?\d+)$/); if (m) parts = [m[1], m[2]]; else return null; }
    var a = numIn(parts[0]), b = numIn(parts[1]);
    return a === null || b === null ? null : [a, b];
  }


  /* ======================================================================
     unitat 9: perímetres i àrees. Teorema de Pitàgores
     ====================================================================== */
  function isInt(v) { return Math.abs(v - Math.round(v)) < 1e-9; }
  /* nombre amb fins a 4 decimals (per als quadrats: 1,4² = 1,96) */
  function n4(v) { var r = Math.round(v * 10000) / 10000; if (near(r, 0)) r = 0; return String(r).replace(".", "\\dc "); }
  function d2(v) { return (Math.round(v * 100) / 100).toFixed(2).replace(".", "\\dc "); }
  /* "= 5" si és exacte, "≈ 8,60" si no */
  function ap(v) { return isInt(v) ? "=" + nf(Math.round(v)) : "\\approx " + d2(v); }
  function rt(v) { return "\\sqrt{" + n4(v) + "}" + ap(Math.sqrt(v)); }
  function lab(v) { var s = String(Math.round(v * 100) / 100); return lang === "en" ? s : s.replace(".", ","); }
  function pol(C, r, a) { return [C[0] + r * Math.cos(a * Math.PI / 180), C[1] + r * Math.sin(a * Math.PI / 180)]; }
  function mid(A, B, f) { f = f == null ? 0.5 : f; return [A[0] + (B[0] - A[0]) * f, A[1] + (B[1] - A[1]) * f]; }
  /* punt mitjà de AB desplaçat d cap a l'esquerra (mirant d'A a B) */
  function off(A, B, d) { var M = mid(A, B), dx = B[0] - A[0], dy = B[1] - A[1], n = Math.hypot(dx, dy); return [M[0] - dy / n * d, M[1] + dx / n * d]; }
  var PI = Math.PI;
  function tolOf(v, pi) { return pi ? Math.max(0.011, 0.0006 * Math.abs(v)) : 0.011; }

  /* ---------- lectura dels controls ---------- */
  function sliders(w) { var o = {}; w.querySelectorAll('input[type="range"]').forEach(function (i) { o[i.dataset.k] = i; }); return o; }
  function showRv(w, k, name, v) { var e = w.querySelector("." + k + "v"); if (e) e.innerHTML = tex(name + "=" + nf(v)); }
  function showRange(w, k, on) { var i = w.querySelector('input[data-k="' + k + '"]'); if (i) i.closest("label").style.display = on ? "" : "none"; }
  function gcol(rows) { return '<div class="gcol">' + rows.map(function (r) { return "<p>" + r + "</p>"; }).join("") + "</div>"; }

  /* ======================================================================
     Unitat 11 (4t ESO A): probabilitat (a partir de les unitats 11 de 2n ESO i 12 de 3r ESO)
     ====================================================================== */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; }
  /* fracció irreductible en TeX */
  function ft(n, d) { var g = gcd(n, d); n /= g; d /= g; return d === 1 ? String(n) : "\\frac{" + n + "}{" + d + "}"; }
  /* n/d i, si es pot, simplificada */
  function fs(n, d) { var g = gcd(n, d); return "\\frac{" + n + "}{" + d + "}" + (g > 1 && d !== 0 ? "=" + ft(n, d) : ""); }
  function dcm(v, k) { k = k == null ? 2 : k; var s = (Math.round(v * Math.pow(10, k)) / Math.pow(10, k)).toFixed(k); return s.replace(".", "\\dc "); }
  /* decimal sense zeros sobrers: 0,35 · 0,5 */
  function dz(v) { var r = Math.round(v * 10000) / 10000; return String(r).replace(".", "\\dc "); }
  function setTex(a) { return a.length ? "\\{" + a.join(",\\,") + "\\}" : "\\varnothing"; }
  function range(a, b) { var o = []; for (var i = a; i <= b; i++) o.push(i); return o; }
  function isPrime(n) { if (n < 2) return false; for (var i = 2; i * i <= n; i++) if (n % i === 0) return false; return true; }
  function probQ(n, d) { return { num: n / d, tol: 0.0051 }; }
  /* "= 0,25" si el decimal és exacte amb 2 xifres, "≈ 0,33" si no; res si la fracció és entera */
  function apx(n, d) { var v = n / d; if (Math.abs(v - Math.round(v)) < 1e-9) return ""; return Math.abs(v * 100 - Math.round(v * 100)) < 1e-9 ? "=" + dz(Math.round(v * 100) / 100) : "\\approx " + dcm(v); }
  function ansTxt(n, d) { return tex(fs(n, d) + apx(n, d)); }

  /* grup de botons (un sol actiu) que es redibuixa en canviar d'idioma */
  function segGroup(box, items, cur, cb) {
    function paint() {
      if (typeof items === "function") return paintL(items());
      paintL(items);
    }
    function paintL(items) {
      box.innerHTML = "";
      items.forEach(function (it) {
        var b = document.createElement("button"); b.type = "button"; b.innerHTML = rtex(T(it.t)); b.setAttribute("aria-pressed", String(it.k === cur));
        b.addEventListener("click", function () { cur = it.k; paint(); cb(cur); }); box.appendChild(b);
      });
    }
    onLang(paint);
    return { set: function (k) { cur = k; paint(); }, get: function () { return cur; }, repaint: paint };
  }

  /* ---------- figures ---------- */
  var BALLC = { R: "ball-r", B: "ball-b", V: "ball-g", G: "ball-y", N: "ball-k" };
  function ballSvg(c, r) { r = r || 9; return '<svg width="' + (2 * r + 4) + '" height="' + (2 * r + 4) + '" viewBox="0 0 ' + (2 * r + 4) + " " + (2 * r + 4) + '"><circle class="ball ' + BALLC[c] + '" cx="' + (r + 2) + '" cy="' + (r + 2) + '" r="' + r + '"/></svg>'; }
  function bagSvg(spec, per) {
    var n = spec.length; if (!n) return "";
    per = per || (n > 20 ? 8 : n > 12 ? 6 : 5);
    /* costats rectes i cantonades de baix arredonides: cada bola queda a 6 px (o més) de la vora (com bag() de comu.py) */
    var cols = Math.min(per, n), rows = Math.ceil(n / cols), W = 44 + (cols - 1) * 26, Hb = 36 + (rows - 1) * 26 + 19, H = Hb + 4, o = "";
    o += '<path class="bagp" d="M6 20 L6 ' + (Hb - 16) + " Q6 " + Hb + " 22 " + Hb + " L" + (W - 22) + " " + Hb + " Q" + (W - 6) + " " + Hb + " " + (W - 6) + " " + (Hb - 16) + " L" + (W - 6) + ' 20 Z"/><path class="bagt" d="M2 20 H' + (W - 2) + '"/>';
    for (var i = 0; i < n; i++) { var r = Math.floor(i / cols), k = i % cols; o += '<circle class="ball ' + BALLC[spec[i]] + '" cx="' + (22 + k * 26) + '" cy="' + (36 + r * 26) + '" r="10"/>'; }
    return '<svg class="bag" viewBox="0 0 ' + W + " " + H + '" style="max-width:' + W + 'px" role="img" aria-label="bossa">' + o + "</svg>";
  }
  function bagSpec(c) { var s = ""; ["R", "B", "V", "G"].forEach(function (k) { for (var i = 0; i < (c[k] || 0); i++) s += k; }); return s; }
  /* diagrama d'arbre: kids = [{lab, ball, p, kids, end, hit}] */
  function treeSvg(kids, o) {
    o = o || {}; var W = o.W || 360, rowh = o.rowh || 36, depth = 0, cnt = 0, out = "", txt = "";
    (function dep(ks, d) { depth = Math.max(depth, d); ks.forEach(function (k) { if (k.kids) dep(k.kids, d + 1); }); })(kids, 1);
    var cw = (W - (o.leafw || 150)) / depth;
    function place(ks, d) {
      return ks.map(function (k) {
        if (k.kids && k.kids.length) { var ch = place(k.kids, d + 1), y = ch.reduce(function (s, c) { return s + c.y; }, 0) / ch.length; return { k: k, y: y, d: d, ch: ch }; }
        var y0 = 16 + cnt * rowh; cnt++; return { k: k, y: y0, d: d, ch: [] };
      });
    }
    var top = place(kids, 1), H = 32 + (cnt - 1) * rowh, ry = top.reduce(function (s, c) { return s + c.y; }, 0) / top.length;
    function X(d) { return 14 + d * cw; }
    function draw(pos, px, py) {
      pos.forEach(function (p) {
        var x = X(p.d), k = p.k;
        out += '<line class="tl' + (k.on ? " on" : "") + '" x1="' + (px + 9).toFixed(1) + '" y1="' + py.toFixed(1) + '" x2="' + (x - 12).toFixed(1) + '" y2="' + p.y.toFixed(1) + '"/>';
        if (k.p) txt += '<text class="tp" x="' + ((px + x - 3) / 2).toFixed(1) + '" y="' + ((py + p.y) / 2 + (p.y > py + 1 ? 13 : -5)).toFixed(1) + '" text-anchor="middle">' + k.p + "</text>";
        if (k.ball) out += '<circle class="ball ' + BALLC[k.ball] + '" cx="' + x.toFixed(1) + '" cy="' + p.y.toFixed(1) + '" r="9"/>';
        txt += '<text class="tn' + (k.ball ? " on" : "") + '" x="' + x.toFixed(1) + '" y="' + (p.y + 4.5).toFixed(1) + '" text-anchor="middle">' + k.lab + "</text>";
        if (p.ch.length) draw(p.ch, x, p.y);
        else if (k.end) txt += '<text class="te' + (k.hit ? " hit" : "") + '" x="' + (x + 18).toFixed(1) + '" y="' + (p.y + 4.5).toFixed(1) + '">' + k.end + "</text>";
      });
    }
    out += '<circle class="troot" cx="' + (X(0) - 4) + '" cy="' + ry.toFixed(1) + '" r="3.5"/>';
    draw(top, X(0) - 13, ry);
    return '<svg class="ptree" viewBox="0 0 ' + W + " " + H + '" style="max-width:' + W + 'px" role="img" aria-label="arbre">' + out + txt + "</svg>";
  }
  function fstr(n, d) { var g = gcd(n, d); n /= g; d /= g; return d === 1 ? String(n) : n + "/" + d; }
  /* arbre de dues extraccions (r roges, b blaves); ev("RB") -> favorable */
  function bagTree(r, b, rep, ev) {
    var n = r + b, kids = [], terms = [], sn = 0, sd = 1, rows = [];
    [["R", r], ["B", b]].forEach(function (a) {
      if (!a[1]) return;
      var ch = [];
      [["R", r], ["B", b]].forEach(function (c) {
        var num = rep ? c[1] : c[1] - (a[0] === c[0] ? 1 : 0), den = rep ? n : n - 1;
        if (num <= 0) return;
        var pn = a[1] * num, pd = n * den, hit = ev ? ev(a[0] + c[0]) : false;
        if (hit) { terms.push({ t: "\\frac{" + a[1] + "}{" + n + "}\\cdot\\frac{" + num + "}{" + den + "}", n: pn, d: pd }); sn = sn * pd + pn * sd; sd = sd * pd; var g = gcd(sn, sd); sn /= g; sd /= g; }
        ch.push({ lab: c[0], ball: c[0], p: num + "/" + den, end: a[0] + c[0] + ": " + fstr(pn, pd), hit: hit, on: hit });
      });
      kids.push({ lab: a[0], ball: a[0], p: a[1] + "/" + n, kids: ch, on: ch.some(function (c) { return c.hit; }) });
    });
    return { kids: kids, terms: terms, n: sn, d: sd };
  }
  /* taula de doble entrada dels dos daus */
  var DOPS = { s: function (a, b) { return a + b; }, d: function (a, b) { return Math.abs(a - b); }, p: function (a, b) { return a * b; } };
  function diceHtml(op, hit, last) {
    var sym = { s: "+", d: "−", p: "×" }[op], h = '<tr><th class="corner">' + sym + "</th>";
    for (var b = 1; b <= 6; b++) h += "<th>" + b + "</th>";
    h += "</tr>"; var body = "";
    for (var a = 1; a <= 6; a++) {
      body += "<tr><th>" + a + "</th>";
      for (b = 1; b <= 6; b++) { var c = []; if (hit(a, b)) c.push("hit"); if (last && last[0] === a && last[1] === b) c.push("last"); body += "<td" + (c.length ? ' class="' + c.join(" ") + '"' : "") + ">" + DOPS[op](a, b) + "</td>"; }
      body += "</tr>";
    }
    return '<div class="tbl-wrap"><table class="dgrid"><thead>' + h + "</thead><tbody>" + body + "</tbody></table></div>";
  }
  function chipsHtml(E, A, B, R, cls) {
    return '<div class="chips-e ' + (cls || "") + '">' + E.map(function (e) {
      var c = "el" + (A && A.indexOf(e) >= 0 ? " a" : "") + (B && B.indexOf(e) >= 0 ? " b" : "") + (R && R.indexOf(e) >= 0 ? " r" : "") + (R && R.indexOf(e) < 0 ? " dim" : "");
      return '<span class="' + c + '">' + e + "</span>";
    }).join("") + "</div>";
  }

  /* ---------- 11.1 experiments ---------- */
  var EXP = {
    mon: { t: L3("Una moneda", "Una moneda", "A coin"), E: ["C", "X"] },
    dau: { t: L3("Un dau", "Un dado", "A die"), E: range(1, 6) },
    m2: { t: L3("Dues monedes", "Dos monedas", "Two coins"), E: ["CC", "CX", "XC", "XX"] },
    m3: { t: L3("Tres monedes", "Tres monedas", "Three coins"), E: ["CCC", "CCX", "CXC", "CXX", "XCC", "XCX", "XXC", "XXX"] },
    md: { t: L3("Moneda i dau", "Moneda y dado", "Coin and die"), E: ["C1", "C2", "C3", "C4", "C5", "C6", "X1", "X2", "X3", "X4", "X5", "X6"] },
    bos: { t: L3("Bossa: 3 roges i 2 blaves", "Bolsa: 3 rojas y 2 azules", "Bag: 3 red and 2 blue"), E: ["R", "B"], bag: "RRRBB" }
  };
  function wEsp() {
    var w = document.getElementById("w-esp"); if (!w) return;
    var out = w.querySelector(".esp-out"), cur = "dau", hist = [], last = null;
    function draw() {
      var X = EXP[cur], E = X.E;
      if (X.bag) { var bb = X.bag[rint(0, X.bag.length - 1)]; return bb; }
      return E[rint(0, E.length - 1)];
    }
    function paint() {
      var X = EXP[cur], cnt = {};
      hist.forEach(function (h) { cnt[h] = (cnt[h] || 0) + 1; });
      var rows = [T(L3("Espai mostral:", "Espacio muestral:", "Sample space:")) + " " + tex("E=" + setTex(X.E.map(String))) + " · " + fill(T(L3("{n} resultats", "{n} resultados", "{n} outcomes")), { n: X.E.length })];
      if (X.bag) rows.push(bagSvg(X.bag) + " " + T(L3("Només hi ha dos resultats, però no són igual de probables: hi ha més boles roges.", "Solo hay dos resultados, pero no son igual de probables: hay más bolas rojas.", "There are only two outcomes, but they aren't equally likely: there are more red balls.")));
      var html = rows.map(function (r) { return "<p>" + r + "</p>"; }).join("");
      html += '<div class="chips-e">' + X.E.map(function (e) { e = String(e); return '<span class="el' + (e === String(last) ? " now" : "") + '">' + e + (cnt[e] ? " <small>×" + cnt[e] + "</small>" : "") + "</span>"; }).join("") + "</div>";
      if (last !== null) html += "<p>" + T(L3("Resultat:", "Resultado:", "Result:")) + ' <span class="big-r">' + (X.bag ? ballSvg(last, 11) + " " : "") + last + "</span> · " + fill(T(L3("Has fet l'experiment {n} vegades.", "Has hecho el experimento {n} veces.", "You've done the experiment {n} times.")), { n: hist.length }) + "</p>";
      if (hist.length > 1) html += '<p class="hist">' + hist.slice(-40).join(" · ") + "</p>";
      out.innerHTML = html;
    }
    segGroup(w.querySelector(".sg-x"), Object.keys(EXP).map(function (k) { return { k: k, t: EXP[k].t }; }), cur, function (k) { cur = k; hist = []; last = null; paint(); });
    w.querySelector('[data-a="go"]').addEventListener("click", function () { last = String(draw()); hist.push(last); paint(); });
    w.querySelector('[data-a="clr"]').addEventListener("click", function () { hist = []; last = null; paint(); });
    onLang(paint);
  }

  /* ---------- 11.2 operacions amb esdeveniments ---------- */
  var UNIV = { d: { t: L3("Dau (1–6)", "Dado (1–6)", "Die (1–6)"), n: 6, lo: 4, hi: 4 }, b: { t: L3("Bombo (1–20)", "Bombo (1–20)", "Drum (1–20)"), n: 20, lo: 8, hi: 12 } };
  function evList(U) {
    return [
      { k: "par", t: L3("parell", "par", "even"), f: function (x) { return x % 2 === 0; } },
      { k: "sen", t: L3("senar", "impar", "odd"), f: function (x) { return x % 2 === 1; } },
      { k: "m3", t: L3("múltiple de 3", "múltiplo de 3", "multiple of 3"), f: function (x) { return x % 3 === 0; } },
      { k: "m4", t: L3("múltiple de 4", "múltiplo de 4", "multiple of 4"), f: function (x) { return x % 4 === 0; } },
      { k: "pri", t: L3("primer", "primo", "prime"), f: isPrime },
      { k: "lo", t: L3("menor que " + U.lo, "menor que " + U.lo, "less than " + U.lo), f: function (x) { return x < U.lo; } },
      { k: "hi", t: L3("major que " + U.hi, "mayor que " + U.hi, "greater than " + U.hi), f: function (x) { return x > U.hi; } }
    ];
  }
  function opsOf(E, A, B) {
    var inA = function (x) { return A.indexOf(x) >= 0; }, inB = function (x) { return B.indexOf(x) >= 0; };
    return {
      U: E.filter(function (x) { return inA(x) || inB(x); }), I: E.filter(function (x) { return inA(x) && inB(x); }),
      nA: E.filter(function (x) { return !inA(x); }), nB: E.filter(function (x) { return !inB(x); }),
      AnB: E.filter(function (x) { return inA(x) && !inB(x); }), nU: E.filter(function (x) { return !inA(x) && !inB(x); })
    };
  }
  function wOps() {
    var w = document.getElementById("w-ops"); if (!w) return;
    var out = w.querySelector(".ops-out"), u = "d", a = "par", b = "m3", sa, sb;
    function evs() { return evList(UNIV[u]); }
    function paint() {
      var U = UNIV[u], E = range(1, U.n), L = evs();
      var fa = L.filter(function (e) { return e.k === a; })[0], fb = L.filter(function (e) { return e.k === b; })[0];
      var A = E.filter(fa.f), B = E.filter(fb.f), o = opsOf(E, A, B);
      var row = function (lab, s, R) { return '<div class="hrow">' + tex(lab + "=" + setTex(s)) + chipsHtml(E, A, B, R) + "</div>"; };
      out.innerHTML = chipsHtml(E, A, B) + '<div class="hrow">' + tex("A=" + setTex(A)) + " · " + rtex(T(fa.t)) + "<br>" + tex("B=" + setTex(B)) + " · " + rtex(T(fb.t)) + "</div>"
        + row("A\\cup B", o.U, o.U) + row("A\\cap B", o.I, o.I) + row("\\overline{A}", o.nA, o.nA) + row("\\overline{B}", o.nB, o.nB)
        + '<div class="hrow">' + (o.I.length ? "🔗 " + T(L3("<strong>Compatibles</strong>: poden ocórrer alhora.", "<strong>Compatibles</strong>: pueden ocurrir a la vez.", "<strong>Compatible</strong>: they can happen together."))
          : "⛔ " + T(L3("<strong>Incompatibles</strong>: ", "<strong>Incompatibles</strong>: ", "<strong>Mutually exclusive</strong>: ")) + tex("A\\cap B=\\varnothing") + (o.U.length === E.length ? " " + T(L3("i, a més, són <strong>contraris</strong>.", "y, además, son <strong>contrarios</strong>.", "and they are also <strong>complementary</strong>.")) : "")) + "</div>";
    }
    var items = function () { return evs().map(function (e) { return { k: e.k, t: e.t }; }); };
    segGroup(w.querySelector(".sg-u"), Object.keys(UNIV).map(function (k) { return { k: k, t: UNIV[k].t }; }), u, function (k) { u = k; sa.repaint(); sb.repaint(); paint(); });
    sa = segGroup(w.querySelector(".sg-a"), items, a, function (k) { a = k; paint(); });
    sb = segGroup(w.querySelector(".sg-b"), items, b, function (k) { b = k; paint(); });
    onLang(paint);
  }

  /* ---------- 11.3 propietats ---------- */
  function vennSvg(a, b, c, show) {
    var o = '<rect class="fr" x="4" y="4" width="292" height="172" rx="10"/><text x="16" y="24">E</text>';
    o += '<circle class="ca" cx="115" cy="92" r="66"/><circle class="cb" cx="185" cy="92" r="66"/>';
    o += '<text class="l" x="70" y="40" text-anchor="middle">A</text><text class="l" x="230" y="40" text-anchor="middle">B</text>';
    if (show) {
      o += '<text x="88" y="97" text-anchor="middle">' + lab(a - c) + '</text><text x="150" y="97" text-anchor="middle">' + lab(c) + "</text>";
      o += '<text x="212" y="97" text-anchor="middle">' + lab(b - c) + '</text><text x="268" y="166" text-anchor="middle">' + lab(1 - a - b + c) + "</text>";
    }
    return '<svg class="venn" viewBox="0 0 300 180" role="img" aria-label="Venn">' + o + "</svg>";
  }
  function wProp() {
    var w = document.getElementById("w-prop"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var a = +I.a.value, b = +I.b.value, c = +I.c.value, r = function (v) { return Math.round(v * 100) / 100; };
      showRv(w, "a", "P(A)", a); showRv(w, "b", "P(B)", b); showRv(w, "c", "P(A\\cap B)", c);
      var bad = c > Math.min(a, b) + 1e-9 ? T(L3("La intersecció no pot ser més probable que A o que B: ", "La intersección no puede ser más probable que A o que B: ", "The intersection can't be more likely than A or B: ")) + tex("A\\cap B\\subset A,\\ A\\cap B\\subset B")
        : a + b - c > 1 + 1e-9 ? fill(T(L3("Impossible: ens eixiria {u}, i una probabilitat no pot passar d'1.", "Imposible: nos saldría {u}, y una probabilidad no puede pasar de 1.", "Impossible: we'd get {u}, and a probability can't exceed 1.")), { u: tex("P(A\\cup B)=" + dz(r(a + b - c))) }) : null;
      if (bad) { out.innerHTML = vennSvg(a, b, c, false) + gcol(['<span class="warn-b">⚠️ ' + bad + "</span>"]); return; }
      out.innerHTML = vennSvg(a, b, c, true) + gcol([
        tex("P(\\overline{A})=1-" + dz(a) + "=" + dz(r(1 - a))) + " · " + tex("P(\\overline{B})=" + dz(r(1 - b))),
        tex("P(A\\cup B)=" + dz(a) + "+" + dz(b) + "-" + dz(c) + "=" + dz(r(a + b - c))),
        T(L3("Només A:", "Solo A:", "Only A:")) + " " + tex("P(A\\cap\\overline{B})=" + dz(a) + "-" + dz(c) + "=" + dz(r(a - c))),
        T(L3("Cap dels dos:", "Ninguno de los dos:", "Neither:")) + " " + tex("P(\\overline{A\\cup B})=" + dz(r(1 - a - b + c))),
        c === 0 ? "⛔ " + T(L3("Són incompatibles: la unió és la suma.", "Son incompatibles: la unión es la suma.", "They are mutually exclusive: the union is the sum.")) : "🔗 " + T(L3("Són compatibles: cal restar la intersecció.", "Son compatibles: hay que restar la intersección.", "They are compatible: subtract the intersection."))]);
    }
    [I.a, I.b, I.c].forEach(function (s) { s.addEventListener("input", paint); });
    quickBind(w, function (v) { I.a.value = v[0]; I.b.value = v[1]; I.c.value = v[2]; paint(); });
    onLang(paint);
  }

  /* ---------- 12.4 bossa (Laplace) ---------- */

  /* ---------- 11.4 bossa (Laplace) ---------- */
  var CNAME = { R: L3("roja", "roja", "red"), B: L3("blava", "azul", "blue"), V: L3("verda", "verde", "green"), G: L3("groga", "amarilla", "yellow") };
  function wBag() {
    var w = document.getElementById("w-bag"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), ev = "R", drawn = w.querySelector(".drawn"), tally = {}, nd = 0;
    var EVS = [{ k: "R", t: L3("roja", "roja", "red") }, { k: "B", t: L3("blava", "azul", "blue") }, { k: "V", t: L3("verda", "verde", "green") }, { k: "G", t: L3("groga", "amarilla", "yellow") },
      { k: "nR", t: L3("no roja", "no roja", "not red") }, { k: "RB", t: L3("roja o blava", "roja o azul", "red or blue") }];
    function cnts() { return { R: +I.r.value, B: +I.b.value, V: +I.v.value, G: +I.g.value }; }
    function fav(c) { return ev === "nR" ? c.B + c.V + c.G : ev === "RB" ? c.R + c.B : c[ev]; }
    function paint() {
      var c = cnts(), n = c.R + c.B + c.V + c.G;
      showRv(w, "r", "R", c.R); showRv(w, "b", "B", c.B); showRv(w, "v", "V", c.V); showRv(w, "g", "G", c.G);
      if (!n) { out.innerHTML = warn(T(L3("La bossa és buida!", "¡La bolsa está vacía!", "The bag is empty!"))); return; }
      var f = fav(c), name = T(EVS.filter(function (e) { return e.k === ev; })[0].t), g = gcd(f, n);
      var rows = [fill(T(L3("Casos possibles: {n} boles. Casos favorables a «{e}»: {f}.", "Casos posibles: {n} bolas. Casos favorables a «{e}»: {f}.", "Possible outcomes: {n} balls. Favourable to “{e}”: {f}.")), { n: n, e: name, f: f }),
        '<span class="big">' + tex("P(\\text{" + name + "})=" + fs(f, n) + apx(f, n) + (apx(f, n).charAt(0) === "\\" ? "\\approx " : "=") + dz(Math.round(f / n * 1000) / 10) + "\\,\\%") + "</span>"];
      if (f === 0) rows.push("🚫 " + T(L3("És un esdeveniment impossible.", "Es un suceso imposible.", "It's an impossible event.")));
      if (f === n) rows.push("✅ " + T(L3("És un esdeveniment segur.", "Es un suceso seguro.", "It's a certain event.")));
      out.innerHTML = bagSvg(bagSpec(c)) + gcol(rows);
    }
    function resetT() { tally = {}; nd = 0; drawn.innerHTML = ""; }
    [I.r, I.b, I.v, I.g].forEach(function (s) { s.addEventListener("input", function () { resetT(); paint(); }); });
    segGroup(w.querySelector(".sg-e"), EVS, ev, function (k) { ev = k; paint(); });
    w.querySelector('[data-a="draw"]').addEventListener("click", function () {
      var s = bagSpec(cnts()); if (!s) return;
      var x = s[rint(0, s.length - 1)]; tally[x] = (tally[x] || 0) + 1; nd++;
      drawn.innerHTML = ballSvg(x, 10) + " " + T(CNAME[x]) + " · " + Object.keys(tally).map(function (k) { return k + ": " + tally[k]; }).join(", ") + " (" + nd + ")";
    });
    onLang(paint);
  }

  /* ---------- 11.3 llei dels grans nombres ---------- */
  var SIM = {
    mon: { t: L3("Moneda: cara", "Moneda: cara", "Coin: heads"), p: 0.5, reg: true, pt: "\\frac12" },
    dau: { t: L3("Dau: traure un 6", "Dado: sacar un 6", "Die: roll a 6"), p: 1 / 6, reg: true, pt: "\\frac16\\approx0\\dc 167" },
    xin: { t: L3("Xinxeta: punta amunt", "Chincheta: punta arriba", "Drawing pin: point up"), p: 0.62, reg: false, pt: "0\\dc 62" },
    tru: { t: L3("Dau trucat: traure un 6", "Dado trucado: sacar un 6", "Loaded die: roll a 6"), p: 0.3, reg: false, pt: "0\\dc 3" }
  };
  function wLgn() {
    var w = document.getElementById("w-lgn"); if (!w) return;
    var out = w.querySelector(".gout"), cur = "mon", n = 0, f = 0, pts = [];
    function run(k) { var p = SIM[cur].p; for (var i = 0; i < k; i++) { n++; if (Math.random() < p) f++; pts.push(f / n); } paint(); }
    function chart() {
      var Wd = 440, H = 220, l = 40, r = 12, t = 12, bt = 28, N = Math.max(n, 10), o = "";
      var X = function (i) { return l + (i / N) * (Wd - l - r); }, Y = function (h) { return t + (1 - h) * (H - t - bt); };
      [0, 0.25, 0.5, 0.75, 1].forEach(function (h) { o += '<line class="grid" x1="' + l + '" x2="' + (Wd - r) + '" y1="' + Y(h) + '" y2="' + Y(h) + '"/><text class="tk" x="' + (l - 6) + '" y="' + (Y(h) + 3) + '" text-anchor="end">' + lab(h) + "</text>"; });
      o += '<line class="ax" x1="' + l + '" x2="' + (Wd - r) + '" y1="' + Y(0) + '" y2="' + Y(0) + '"/><text class="tk" x="' + (Wd - r) + '" y="' + (H - 8) + '" text-anchor="end">n = ' + N + '</text><text class="tk" x="' + l + '" y="' + (H - 8) + '">0</text>';
      o += '<line class="pv" x1="' + l + '" x2="' + (Wd - r) + '" y1="' + Y(SIM[cur].p) + '" y2="' + Y(SIM[cur].p) + '"/>';
      if (pts.length) {
        var step = Math.max(1, Math.floor(pts.length / 500)), d = "";
        for (var i = 0; i < pts.length; i += step) d += (d ? "L" : "M") + X(i + 1).toFixed(1) + " " + Y(pts[i]).toFixed(1);
        d += "L" + X(pts.length).toFixed(1) + " " + Y(pts[pts.length - 1]).toFixed(1);
        o += '<path class="cv" d="' + d + '"/>';
      }
      return '<svg class="lgn" viewBox="0 0 ' + Wd + " " + H + '" role="img" aria-label="freqüència relativa">' + o + "</svg>";
    }
    function paint() {
      var S = SIM[cur], rows = [];
      rows.push(fill(T(L3("Repeticions: {n} · vegades que ocorre: {f}", "Repeticiones: {n} · veces que ocurre: {f}", "Trials: {n} · times it happens: {f}")), { n: n, f: f }));
      if (n) rows.push('<span class="big">' + tex("h=\\frac{" + f + "}{" + n + "}\\approx " + dcm(f / n, 3)) + "</span>");
      rows.push((S.reg ? "📐 " + T(L3("Experiment regular: per Laplace,", "Experimento regular: por Laplace,", "Regular experiment: by Laplace,")) : "🔬 " + T(L3("Experiment irregular: no podem usar Laplace. La probabilitat (línia discontínua) només la coneixem experimentant:", "Experimento irregular: no podemos usar Laplace. La probabilidad (línea discontinua) solo la conocemos experimentando:", "Irregular experiment: we can't use Laplace. We only know the probability (dashed line) by experimenting:"))) + " " + tex("P=" + S.pt));
      if (n >= 1000) rows.push("✅ " + T(L3("Amb tantes repeticions, la freqüència relativa ja és molt a prop de la probabilitat.", "Con tantas repeticiones, la frecuencia relativa ya está muy cerca de la probabilidad.", "With so many trials, the relative frequency is already very close to the probability.")));
      else if (n > 0 && n < 50) rows.push("💡 " + T(L3("Amb poques repeticions, la freqüència relativa salta molt. Prova amb +1000.", "Con pocas repeticiones, la frecuencia relativa salta mucho. Prueba con +1000.", "With few trials, the relative frequency jumps around a lot. Try +1000.")));
      out.innerHTML = chart() + gcol(rows);
    }
    segGroup(w.querySelector(".sg-x"), Object.keys(SIM).map(function (k) { return { k: k, t: SIM[k].t }; }), cur, function (k) { cur = k; n = f = 0; pts = []; paint(); });
    w.querySelectorAll("[data-n]").forEach(function (b) { b.addEventListener("click", function () { if (n < 50000) run(+b.dataset.n); }); });
    w.querySelector('[data-a="clr"]').addEventListener("click", function () { n = f = 0; pts = []; paint(); });
    onLang(paint);
  }

  /* ---------- 11.4 dos daus ---------- */
  var DOPN = { s: L3("suma", "suma", "sum"), d: L3("diferència", "diferencia", "difference"), p: L3("producte", "producto", "product") };
  var DRANGE = { s: [2, 12], d: [0, 5], p: [1, 36] };
  function relF(rel, k) { return rel === "eq" ? function (v) { return v === k; } : rel === "le" ? function (v) { return v <= k; } : function (v) { return v >= k; }; }
  var RELT = { eq: "=", le: "\\le", ge: "\\ge" };
  function wDice2() {
    var w = document.getElementById("w-dice2"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), op = "s", rel = "eq", last = null, drawn = w.querySelector(".drawn");
    function setRange() { var R = DRANGE[op]; I.k.min = R[0]; I.k.max = R[1]; if (+I.k.value < R[0] || +I.k.value > R[1]) I.k.value = op === "s" ? 7 : op === "d" ? 1 : 12; }
    function paint() {
      var k = +I.k.value, f = relF(rel, k), cnt = 0, name = T(DOPN[op]);
      showRv(w, "k", "k", k);
      for (var a = 1; a <= 6; a++) for (var b = 1; b <= 6; b++) if (f(DOPS[op](a, b))) cnt++;
      var rows = [fill(T(L3("Caselles marcades: {c} de 36.", "Casillas marcadas: {c} de 36.", "Highlighted cells: {c} of 36.")), { c: cnt }),
        '<span class="big">' + tex("P(\\text{" + name + "}" + RELT[rel] + k + ")=" + (cnt ? fs(cnt, 36) + apx(cnt, 36) : "0")) + "</span>"];
      if (op === "d") rows.push("💡 " + T(L3("La diferència és sempre el nombre gran menys el petit.", "La diferencia es siempre el número mayor menos el menor.", "The difference is always the larger number minus the smaller.")));
      if (last) { var v = DOPS[op](last[0], last[1]); drawn.innerHTML = "🎲 " + last[0] + " · " + last[1] + " → " + name + " " + v + " " + (f(v) ? "✅" : "❌"); } else drawn.innerHTML = "";
      out.innerHTML = diceHtml(op, function (a, b) { return f(DOPS[op](a, b)); }, last) + gcol(rows);
    }
    segGroup(w.querySelector(".sg-o"), [{ k: "s", t: L3("Suma", "Suma", "Sum") }, { k: "d", t: L3("Diferència", "Diferencia", "Difference") }, { k: "p", t: L3("Producte", "Producto", "Product") }], op, function (k) { op = k; setRange(); paint(); });
    segGroup(w.querySelector(".sg-r"), [{ k: "eq", t: L3("$=k$", "$=k$", "$=k$") }, { k: "le", t: L3("$\\le k$", "$\\le k$", "$\\le k$") }, { k: "ge", t: L3("$\\ge k$", "$\\ge k$", "$\\ge k$") }], rel, function (k) { rel = k; paint(); });
    I.k.addEventListener("input", paint);
    w.querySelector('[data-a="roll"]').addEventListener("click", function () { last = [rint(1, 6), rint(1, 6)]; paint(); });
    setRange(); onLang(paint);
  }

  /* ---------- 11.6 arbre de dues extraccions ---------- */
  var TEV = {
    RR: { t: L3("dues roges", "dos rojas", "two red"), f: function (s) { return s === "RR"; } },
    BB: { t: L3("dues blaves", "dos azules", "two blue"), f: function (s) { return s === "BB"; } },
    mx: { t: L3("una de cada color", "una de cada color", "one of each colour"), f: function (s) { return s[0] !== s[1]; } },
    al: { t: L3("almenys una roja", "al menos una roja", "at least one red"), f: function (s) { return s.indexOf("R") >= 0; } },
    s2: { t: L3("la segona és roja", "la segunda es roja", "the second is red"), f: function (s) { return s[1] === "R"; } }
  };
  function treeSum(t) {
    if (!t.terms.length) return "P=0";
    var s = "P=" + t.terms.map(function (x) { return x.t; }).join("+");
    if (t.terms.length > 1) s += "=" + t.terms.map(function (x) { return ft(x.n, x.d); }).join("+");
    return s + "=" + ft(t.n, t.d) + apx(t.n, t.d);
  }
  function wTree() {
    var w = document.getElementById("w-tree"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), rep = "sense", ev = "RR";
    function paint() {
      var r = +I.r.value, b = +I.b.value, t = bagTree(r, b, rep === "amb", TEV[ev].f);
      showRv(w, "r", "R", r); showRv(w, "b", "B", b);
      out.innerHTML = bagSvg(bagSpec({ R: r, B: b })) + treeSvg(t.kids, { W: 380, leafw: 130 }) + gcol([
        fill(T(L3("Esdeveniment: «{e}». Sumem els camins marcats.", "Suceso: «{e}». Sumamos los caminos marcados.", "Event: “{e}”. Add the highlighted paths.")), { e: T(TEV[ev].t) }),
        '<span class="big">' + tex(treeSum(t)) + "</span>",
        rep === "amb" ? "🔁 " + T(L3("Amb reemplaçament: la segona extracció té les mateixes probabilitats que la primera.", "Con reemplazamiento: la segunda extracción tiene las mismas probabilidades que la primera.", "With replacement: the second draw has the same probabilities as the first."))
          : "➖ " + T(L3("Sense reemplaçament: en la segona extracció queda una bola menys. Les experiències són dependents.", "Sin reemplazamiento: en la segunda extracción queda una bola menos. Las experiencias son dependientes.", "Without replacement: there's one ball fewer for the second draw. The draws are dependent.")) + (r > 1 ? " " + tex("P(R_2/R_1)=\\frac{" + (r - 1) + "}{" + (r + b - 1) + "}") : "")]);
    }
    [I.r, I.b].forEach(function (s) { s.addEventListener("input", paint); });
    segGroup(w.querySelector(".sg-m"), [{ k: "amb", t: L3("Amb reemplaçament", "Con reemplazamiento", "With replacement") }, { k: "sense", t: L3("Sense reemplaçament", "Sin reemplazamiento", "Without replacement") }], rep, function (k) { rep = k; paint(); });
    segGroup(w.querySelector(".sg-e"), Object.keys(TEV).map(function (k) { return { k: k, t: TEV[k].t }; }), ev, function (k) { ev = k; paint(); });
    onLang(paint);
  }



  /* ---------- 11.5 experiències independents ---------- */
  var NA_ = "Ā", NB_ = "B̄";
  var EVI = {
    AB: { t: L3("A i B", "A y B", "A and B"), f: function (s) { return s === "AB"; } },
    no: { t: L3("cap dels dos", "ninguno de los dos", "neither"), f: function (s) { return s === "ab"; } },
    al: { t: L3("almenys un", "al menos uno", "at least one"), f: function (s) { return s !== "ab"; } },
    one: { t: L3("exactament un", "exactamente uno", "exactly one"), f: function (s) { return s === "Ab" || s === "aB"; } }
  };
  function r2_(v) { return Math.round(v * 10000) / 10000; }
  function wInd() {
    var w = document.getElementById("w-ind"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), ev = "AB";
    function paint() {
      var a = +I.a.value, b = +I.b.value, na = r2_(1 - a), nb = r2_(1 - b), f = EVI[ev].f;
      showRv(w, "a", "P(A)", a); showRv(w, "b", "P(B)", b);
      var P = { AB: r2_(a * b), Ab: r2_(a * nb), aB: r2_(na * b), ab: r2_(na * nb) }, tot = 0, terms = [];
      var lab_ = lab;
      function lf(k, l, p) { var h = f(k); if (h) { tot += P[k]; terms.push(dz(P[k])); } return { lab: l, p: lab_(p), end: lab_(P[k]), hit: h, on: h }; }
      var c1 = [lf("AB", "B", b), lf("Ab", NB_, nb)], c2 = [lf("aB", "B", b), lf("ab", NB_, nb)];
      var kids = [{ lab: "A", p: lab_(a), kids: c1, on: c1.some(function (c) { return c.hit; }) }, { lab: NA_, p: lab_(na), kids: c2, on: c2.some(function (c) { return c.hit; }) }];
      tot = r2_(tot);
      var rows = [
        fill(T(L3("Esdeveniment: «{e}». Sumem els camins marcats:", "Suceso: «{e}». Sumamos los caminos marcados:", "Event: “{e}”. Add the highlighted paths:")), { e: T(EVI[ev].t) }),
        '<span class="big">' + tex("P=" + terms.join("+") + (terms.length > 1 ? "=" + dz(tot) : "")) + "</span>",
        tex("P(A\\cap B)=P(A)\\cdot P(B)=" + dz(a) + "\\cdot" + dz(b) + "=" + dz(P.AB))
      ];
      if (ev === "al") rows.push("💡 " + T(L3("Més ràpid amb el contrari:", "Más rápido con el contrario:", "Quicker with the complement:")) + " " + tex("1-P(\\overline{A}\\cap\\overline{B})=1-" + dz(na) + "\\cdot" + dz(nb) + "=" + dz(r2_(1 - P.ab))));
      out.innerHTML = treeSvg(kids, { W: 330, leafw: 70 }) + gcol(rows);
    }
    [I.a, I.b].forEach(function (s) { s.addEventListener("input", paint); });
    quickBind(w, function (v) { I.a.value = v[0]; I.b.value = v[1]; paint(); });
    segGroup(w.querySelector(".sg-e"), Object.keys(EVI).map(function (k) { return { k: k, t: EVI[k].t }; }), ev, function (k) { ev = k; paint(); });
    onLang(paint);
  }

  /* ---------- 11.6 dues urnes ---------- */
  var USEL = {
    m: { t: L3("Moneda: cara → I", "Moneda: cara → I", "Coin: heads → I"), n: 1, d: 2 },
    d: { t: L3("Dau: 1 o 2 → I", "Dado: 1 o 2 → I", "Die: 1 or 2 → I"), n: 1, d: 3 },
    s: { t: L3("Dau: 6 → I", "Dado: 6 → I", "Die: 6 → I"), n: 1, d: 6 }
  };
  function fadd(a, b) { var n = a[0] * b[1] + b[0] * a[1], d = a[1] * b[1], g = gcd(n, d); return [n / g, d / g]; }
  function urnTree(sel, r1, b1, r2, b2, ev) {
    var S = USEL[sel], pI = [S.n, S.d], pII = [S.d - S.n, S.d], n1 = r1 + b1, n2 = r2 + b2, terms = [], sum = [0, 1], kids = [];
    [["I", pI, r1, b1, n1], ["II", pII, r2, b2, n2]].forEach(function (u) {
      var ch = [];
      [["R", u[2]], ["B", u[3]]].forEach(function (c) {
        if (!c[1]) return;
        var pn = u[1][0] * c[1], pd = u[1][1] * u[4], hit = ev(u[0], c[0]);
        if (hit) { terms.push({ t: "\\frac{" + u[1][0] + "}{" + u[1][1] + "}\\cdot\\frac{" + c[1] + "}{" + u[4] + "}", n: pn, d: pd }); sum = fadd(sum, [pn, pd]); }
        ch.push({ lab: c[0], ball: c[0], p: c[1] + "/" + u[4], end: u[0] + "," + c[0] + ": " + fstr(pn, pd), hit: hit, on: hit });
      });
      kids.push({ lab: u[0], p: fstr(u[1][0], u[1][1]), kids: ch, on: ch.some(function (c) { return c.hit; }) });
    });
    return { kids: kids, terms: terms, n: sum[0], d: sum[1] };
  }
  var UEV = {
    R: { t: L3("roja", "roja", "red"), f: function (u, c) { return c === "R"; } },
    B: { t: L3("blava", "azul", "blue"), f: function (u, c) { return c === "B"; } },
    IR: { t: L3("urna I i roja", "urna I y roja", "urn I and red"), f: function (u, c) { return u === "I" && c === "R"; } },
    IIB: { t: L3("urna II i blava", "urna II y azul", "urn II and blue"), f: function (u, c) { return u === "II" && c === "B"; } }
  };
  function wUrn() {
    var w = document.getElementById("w-urn"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), sel = "m", ev = "R";
    function paint() {
      var r1 = +I.r1.value, b1 = +I.b1.value, r2 = +I.r2.value, b2 = +I.b2.value;
      showRv(w, "r1", "R_I", r1); showRv(w, "b1", "B_I", b1); showRv(w, "r2", "R_{II}", r2); showRv(w, "b2", "B_{II}", b2);
      if (!(r1 + b1) || !(r2 + b2)) { out.innerHTML = gcol([warn(T(L3("Cada urna ha de tindre alguna bola.", "Cada urna debe tener alguna bola.", "Each urn must have at least one ball.")))]); return; }
      var t = urnTree(sel, r1, b1, r2, b2, UEV[ev].f);
      out.innerHTML = '<div class="figs"><figure>' + bagSvg(bagSpec({ R: r1, B: b1 })) + "<figcaption>" + T(L3("Urna I", "Urna I", "Urn I")) + '</figcaption></figure><figure>' + bagSvg(bagSpec({ R: r2, B: b2 })) + "<figcaption>" + T(L3("Urna II", "Urna II", "Urn II")) + "</figcaption></figure></div>"
        + treeSvg(t.kids, { W: 380, leafw: 120 }) + gcol([
          fill(T(L3("Esdeveniment: «{e}». Sumem els camins marcats.", "Suceso: «{e}». Sumamos los caminos marcados.", "Event: “{e}”. Add the highlighted paths.")), { e: T(UEV[ev].t) }),
          '<span class="big">' + tex(treeSum(t)) + "</span>",
          "🔎 " + T(L3("Les branques de la segona etapa són probabilitats condicionades: depenen de la urna triada.", "Las ramas de la segunda etapa son probabilidades condicionadas: dependen de la urna elegida.", "The second-stage branches are conditional probabilities: they depend on the urn chosen.")) + " " + tex("P(R/I)=" + ft(r1, r1 + b1) + ",\\ P(R/II)=" + ft(r2, r2 + b2))]);
    }
    [I.r1, I.b1, I.r2, I.b2].forEach(function (s) { s.addEventListener("input", paint); });
    segGroup(w.querySelector(".sg-s"), Object.keys(USEL).map(function (k) { return { k: k, t: USEL[k].t }; }), sel, function (k) { sel = k; paint(); });
    segGroup(w.querySelector(".sg-e"), Object.keys(UEV).map(function (k) { return { k: k, t: UEV[k].t }; }), ev, function (k) { ev = k; paint(); });
    onLang(paint);
  }

  /* ---------- 11.7 taula de contingència ---------- */
  var CTB = {
    ull: { t: L3("Ulleres", "Gafas", "Glasses"), M: [[6, 10], [4, 10]],
      rh: [L3("Xiques", "Chicas", "Girls"), L3("Xics", "Chicos", "Boys")], ch: [L3("Ulleres", "Gafas", "Glasses"), L3("Sense ulleres", "Sin gafas", "No glasses")],
      rs: [L3("xica", "chica", "girl"), L3("xic", "chico", "boy")], cs: [L3("ulleres", "gafas", "glasses"), L3("sense ulleres", "sin gafas", "no glasses")],
      who: L3("En una classe, comptem qui porta ulleres.", "En una clase, contamos quién lleva gafas.", "In a class, we count who wears glasses.") },
    esp: { t: L3("Esport", "Deporte", "Sport"), M: [[18, 12], [9, 21]],
      rh: [L3("3r ESO", "3º ESO", "Year 9"), L3("4t ESO", "4º ESO", "Year 10")], ch: [L3("Fa esport", "Hace deporte", "Does sport"), L3("No en fa", "No hace", "Doesn't")],
      rs: [L3("de 3r", "de 3º", "in Year 9"), L3("de 4t", "de 4º", "in Year 10")], cs: [L3("fa esport", "hace deporte", "does sport"), L3("no fa esport", "no hace deporte", "no sport")],
      who: L3("Preguntem a l'alumnat de 3r i 4t d'ESO si fa esport fora de l'institut.", "Preguntamos al alumnado de 3º y 4º de ESO si hace deporte fuera del instituto.", "We ask Year 9 and Year 10 students whether they do sport outside school.") },
    vac: { t: L3("Vacuna", "Vacuna", "Vaccine"), M: [[12, 228], [48, 112]],
      rh: [L3("Vacunats", "Vacunados", "Vaccinated"), L3("No vacunats", "No vacunados", "Not vaccinated")], ch: [L3("Grip", "Gripe", "Flu"), L3("Sense grip", "Sin gripe", "No flu")],
      rs: [L3("vacunat", "vacunado", "vaccinated"), L3("no vacunat", "no vacunado", "not vaccinated")], cs: [L3("té la grip", "tiene la gripe", "has flu"), L3("no té la grip", "no tiene la gripe", "has no flu")],
      who: L3("En una empresa de 400 treballadors, comptem qui s'ha vacunat i qui ha tingut la grip aquest hivern.", "En una empresa de 400 trabajadores, contamos quién se ha vacunado y quién ha tenido la gripe este invierno.", "In a company with 400 workers, we count who was vaccinated and who had flu this winter.") },
    bic: { t: L3("Bicicleta", "Bicicleta", "Bike"), M: [[50, 70], [40, 40]],
      rh: [L3("Dones", "Mujeres", "Women"), L3("Homes", "Hombres", "Men")], ch: [L3("Bici", "Bici", "Bike"), L3("No bici", "No bici", "No bike")],
      rs: [L3("dona", "mujer", "woman"), L3("home", "hombre", "man")], cs: [L3("bici", "bici", "bike"), L3("no bici", "no bici", "no bike")],
      who: L3("En una enquesta, preguntem a la gent d'un poble si va a treballar amb bicicleta.", "En una encuesta, preguntamos a la gente de un pueblo si va a trabajar en bicicleta.", "In a survey, we ask people in a village whether they cycle to work.") }
  };
  /* esdeveniments d'una taula 2×2: cel·les favorables i, si n'hi ha, la fila que ja sabem (given) */
  function ctEvents(C) {
    var r0 = T(C.rs[0]), r1 = T(C.rs[1]), c0 = T(C.cs[0]), c1 = T(C.cs[1]), y = T(L3(" i ", " y ", " and ")), o = T(L3(" o ", " o ", " or ")), sab = T(L3("{a}, sabent que és {b}", "{a}, sabiendo que es {b}", "{a}, given {b}"));
    return [
      { k: "r0", t: r0, cells: [[0, 0], [0, 1]] },
      { k: "c0", t: c0, cells: [[0, 0], [1, 0]] },
      { k: "and", t: r0 + y + c0, cells: [[0, 0]] },
      { k: "or", t: r0 + o + c0, cells: [[0, 0], [0, 1], [1, 0]] },
      { k: "c1", t: c1, cells: [[0, 1], [1, 1]] },
      { k: "r1c1", t: r1 + y + c1, cells: [[1, 1]] },
      { k: "cond", t: fill(sab, { a: c0, b: r1 }), cells: [[1, 0]], given: 1 },
      { k: "cond0", t: fill(sab, { a: c0, b: r0 }), cells: [[0, 0]], given: 0 },
      { k: "condc", t: fill(T(L3("{a}, entre els de «{b}»", "{a}, entre los de «{b}»", "{a}, among those with “{b}”")), { a: r0, b: c0 }), cells: [[0, 0]], givenc: 0 }
    ];
  }
  function ctEv(C, k) { return ctEvents(C).filter(function (e) { return e.k === k; })[0]; }
  function ctCount(M, e) {
    var f = e.cells.reduce(function (s, c) { return s + M[c[0]][c[1]]; }, 0);
    var n = e.given != null ? M[e.given][0] + M[e.given][1] : e.givenc != null ? M[0][e.givenc] + M[1][e.givenc] : M[0][0] + M[0][1] + M[1][0] + M[1][1];
    return { f: f, n: n };
  }
  function ctOut(e, i, j) { return (e.given != null && i !== e.given) || (e.givenc != null && j !== e.givenc); }
  function ctHit(e, i, j) { return e.cells.some(function (c) { return c[0] === i && c[1] === j; }); }
  /* taula estàtica (entrenador i solucions): hide = [i, j] amaga una casella */
  function ctStatic(C, M, e, hide, show) {
    var h = '<tr><th class="corner"></th>' + C.ch.map(function (c) { return "<th>" + T(c) + "</th>"; }).join("") + '<th class="tot">Total</th></tr>', b = "";
    for (var i = 0; i < 2; i++) {
      b += "<tr><th>" + T(C.rh[i]) + "</th>";
      for (var j = 0; j < 2; j++) {
        var hd = hide && hide[0] === i && hide[1] === j && !show, cl = [];
        if (e && show && ctHit(e, i, j)) cl.push("hit");
        if (e && show && ctOut(e, i, j)) cl.push("out");
        b += "<td" + (cl.length ? ' class="' + cl.join(" ") + '"' : "") + ">" + (hd ? '<span class="miss">?</span>' : M[i][j]) + "</td>";
      }
      b += '<td class="tot">' + (M[i][0] + M[i][1]) + "</td></tr>";
    }
    b += '<tr><th class="tot">Total</th><td class="tot">' + (M[0][0] + M[1][0]) + '</td><td class="tot">' + (M[0][1] + M[1][1]) + '</td><td class="tot">' + (M[0][0] + M[0][1] + M[1][0] + M[1][1]) + "</td></tr>";
    return '<div class="tbl-wrap"><table class="ctab"><thead>' + h + "</thead><tbody>" + b + "</tbody></table></div>";
  }
  function wCont() {
    var w = document.getElementById("w-cont"); if (!w) return;
    var box = w.querySelector(".ct-box"), out = w.querySelector(".gout"), cur = "ull", ev = "and", M = CTB.ull.M.map(function (r) { return r.slice(); }), sg;
    function build() {
      var C = CTB[cur], h = '<tr><th class="corner"></th>' + C.ch.map(function (c) { return "<th>" + T(c) + "</th>"; }).join("") + '<th class="tot">Total</th></tr>', b = "";
      for (var i = 0; i < 2; i++) {
        b += "<tr><th>" + T(C.rh[i]) + "</th>";
        for (var j = 0; j < 2; j++) b += '<td data-c="' + i + j + '"><input class="tin s" type="text" inputmode="numeric" autocomplete="off" data-i="' + i + '" data-j="' + j + '" value="' + M[i][j] + '" aria-label="' + T(C.rh[i]) + " · " + T(C.ch[j]) + '"></td>';
        b += '<td class="tot" data-c="' + i + 't"></td></tr>';
      }
      b += '<tr><th class="tot">Total</th><td class="tot" data-c="t0"></td><td class="tot" data-c="t1"></td><td class="tot" data-c="tt"></td></tr>';
      box.innerHTML = '<p class="ct-who">' + T(C.who) + " " + T(L3("Pots canviar els nombres de les caselles.", "Puedes cambiar los números de las casillas.", "You can change the numbers in the cells.")) + '</p><div class="tbl-wrap"><table class="ctab ct-w"><thead>' + h + "</thead><tbody>" + b + "</tbody></table></div>";
      box.querySelectorAll("input").forEach(function (inp) {
        inp.addEventListener("input", function () {
          var v = parseInt(String(inp.value).replace(/\D/g, ""), 10);
          M[+inp.dataset.i][+inp.dataset.j] = isNaN(v) ? 0 : Math.min(v, 9999); paint();
        });
      });
      paint();
    }
    function paint() {
      var C = CTB[cur], e = ctEv(C, ev), q = function (c) { return box.querySelector('[data-c="' + c + '"]'); };
      q("0t").textContent = M[0][0] + M[0][1]; q("1t").textContent = M[1][0] + M[1][1];
      q("t0").textContent = M[0][0] + M[1][0]; q("t1").textContent = M[0][1] + M[1][1]; q("tt").textContent = M[0][0] + M[0][1] + M[1][0] + M[1][1];
      for (var i = 0; i < 2; i++) for (var j = 0; j < 2; j++) { var td = q("" + i + j); td.classList.toggle("hit", ctHit(e, i, j)); td.classList.toggle("out", ctOut(e, i, j)); }
      var c = ctCount(M, e), rows = [];
      if (!c.n) { out.innerHTML = gcol([warn(T(L3("No hi ha cap cas possible: la taula (o la fila) està buida.", "No hay ningún caso posible: la tabla (o la fila) está vacía.", "There are no possible outcomes: the table (or the row) is empty.")))]); return; }
      rows.push(fill(T(L3("Casos possibles: {n} ({w}). Casos favorables a «{e}»: {f} (caselles marcades).", "Casos posibles: {n} ({w}). Casos favorables a «{e}»: {f} (casillas marcadas).", "Possible outcomes: {n} ({w}). Favourable to “{e}”: {f} (highlighted cells).")),
        { n: c.n, f: c.f, e: e.t, w: e.given != null ? fill(T(L3("només la fila «{r}»", "solo la fila «{r}»", "only the “{r}” row")), { r: T(C.rh[e.given]) }) : e.givenc != null ? fill(T(L3("només la columna «{r}»", "solo la columna «{r}»", "only the “{r}” column")), { r: T(C.ch[e.givenc]) }) : T(L3("el total de la taula", "el total de la tabla", "the table total")) }));
      rows.push('<span class="big">' + tex("P=" + (c.f ? fs(c.f, c.n) + apx(c.f, c.n) : "0")) + "</span>");
      if (e.k === "or") rows.push("💡 " + T(L3("Sumem les tres caselles on hi ha alguna de les dues coses. Si sumàrem el total de la fila i el de la columna, la casella comuna la comptaríem dues vegades:", "Sumamos las tres casillas donde hay alguna de las dos cosas. Si sumáramos el total de la fila y el de la columna, la casilla común la contaríamos dos veces:", "Add the three cells with at least one of the two. If we added the row total and the column total, we'd count the shared cell twice:")) + " " + tex((M[0][0] + M[0][1]) + "+" + (M[0][0] + M[1][0]) + "-" + M[0][0] + "=" + c.f));
      if (e.given != null || e.givenc != null) {
        var Nt = M[0][0] + M[0][1] + M[1][0] + M[1][1];
        rows.push("🔎 " + T(L3("És una probabilitat condicionada: com que ja sabem una cosa de la persona triada, els casos possibles són només els d'aquella fila o columna.", "Es una probabilidad condicionada: como ya sabemos algo de la persona elegida, los casos posibles son solo los de esa fila o columna.", "It's a conditional probability: since we already know something about the person chosen, the possible outcomes are only those in that row or column.")));
        if (Nt && c.f) rows.push(T(L3("També:", "También:", "Also:")) + " " + tex("P(A/B)=\\frac{P(A\\cap B)}{P(B)}=\\frac{" + c.f + "/" + Nt + "}{" + c.n + "/" + Nt + "}=" + ft(c.f, c.n)));
      }
      out.innerHTML = gcol(rows);
    }
    segGroup(w.querySelector(".sg-c"), Object.keys(CTB).map(function (k) { return { k: k, t: CTB[k].t }; }), cur, function (k) { cur = k; M = CTB[k].M.map(function (r) { return r.slice(); }); build(); sg.repaint(); });
    sg = segGroup(w.querySelector(".sg-e"), function () { return ctEvents(CTB[cur]).map(function (e) { return { k: e.k, t: L3(e.t, e.t, e.t) }; }); }, ev, function (k) { ev = k; paint(); });
    onLang(build);
  }

  /* ---------- entrenadors ---------- */
  function optsTxt(right, wrongs) {
    var all = [right].concat(wrongs), order = shuffle(all.map(function (_, i) { return i; }));
    return { opts: order.map(function (i) { return all[i]; }), ans: order.indexOf(0) };
  }
  function ret(o, q, s) { o.q = q; o.s = s; return o; }

  var DET = [
    [L3("Llançar un dau i anotar el resultat", "Lanzar un dado y anotar el resultado", "Rolling a die and noting the result"), 0],
    [L3("Traure una carta d'una baralla sense mirar", "Sacar una carta de una baraja sin mirar", "Drawing a card from a pack without looking"), 0],
    [L3("El número guanyador de la loteria de Nadal", "El número ganador de la lotería de Navidad", "The winning number in the Christmas lottery"), 0],
    [L3("Girar una ruleta i mirar en quin color es para", "Girar una ruleta y mirar en qué color se para", "Spinning a wheel and seeing which colour it stops on"), 0],
    [L3("Llançar una xinxeta i mirar com cau", "Lanzar una chincheta y mirar cómo cae", "Tossing a drawing pin and seeing how it lands"), 0],
    [L3("Triar a l'atzar un alumne de la classe", "Elegir al azar un alumno de la clase", "Picking a student from the class at random"), 0],
    [L3("El temps que farà d'ací a un mes", "El tiempo que hará dentro de un mes", "The weather a month from now"), 0],
    [L3("Traure una bola d'una bossa amb boles de colors sense mirar", "Sacar una bola de una bolsa con bolas de colores sin mirar", "Taking a ball from a bag of coloured balls without looking"), 0],
    [L3("El resultat d'un partit de futbol de la setmana que ve", "El resultado de un partido de fútbol de la semana que viene", "The result of next week's football match"), 0],
    [L3("Quantes persones pujaran a l'autobús en la pròxima parada", "Cuántas personas subirán al autobús en la próxima parada", "How many people will get on the bus at the next stop"), 0],
    [L3("Llançar dues monedes i comptar les cares", "Lanzar dos monedas y contar las caras", "Tossing two coins and counting the heads"), 0],
    [L3("Calcular l'àrea d'un rectangle de 3 cm per 4 cm", "Calcular el área de un rectángulo de 3 cm por 4 cm", "Working out the area of a 3 cm by 4 cm rectangle"), 1],
    [L3("Deixar caure una pedra i mirar si cau a terra", "Dejar caer una piedra y mirar si cae al suelo", "Dropping a stone and seeing whether it falls to the ground"), 1],
    [L3("El preu de 5 llibretes a 2 € cadascuna", "El precio de 5 libretas a 2 € cada una", "The price of 5 notebooks at €2 each"), 1],
    [L3("La temperatura a què bull l'aigua al nivell de la mar", "La temperatura a la que hierve el agua al nivel del mar", "The temperature at which water boils at sea level"), 1],
    [L3("Comptar quantes cares té un cub", "Contar cuántas caras tiene un cubo", "Counting how many faces a cube has"), 1],
    [L3("Saber quin dia de la setmana serà demà", "Saber qué día de la semana será mañana", "Knowing what day of the week it will be tomorrow"), 1],
    [L3("Convertir 3 km en metres", "Convertir 3 km en metros", "Converting 3 km into metres"), 1],
    [L3("Fer la multiplicació 17 · 3", "Hacer la multiplicación 17 · 3", "Working out 17 · 3"), 1],
    [L3("Posar un glaçó al sol a 30 °C i mirar si es fon", "Poner un cubito de hielo al sol a 30 °C y mirar si se funde", "Leaving an ice cube in the sun at 30 °C and seeing whether it melts"), 1]
  ];
  var DETO = [L3("Aleatori", "Aleatorio", "Random"), L3("Determinista", "Determinista", "Deterministic")];
  var KINDS = [L3("Segur", "Seguro", "Certain"), L3("Impossible", "Imposible", "Impossible"), L3("Elemental", "Elemental", "Elementary"), L3("Compost", "Compuesto", "Compound")];
  var CTX = {
    d: { n: 6, t: L3("Llancem un dau.", "Lanzamos un dado.", "We roll a die.") },
    r: { n: 8, t: L3("Girem una ruleta de 8 sectors iguals numerats de l'1 al 8.", "Giramos una ruleta de 8 sectores iguales numerados del 1 al 8.", "We spin a wheel with 8 equal sectors numbered 1 to 8.") },
    b: { n: 10, t: L3("Traiem una bola d'una urna amb boles numerades de l'1 al 10.", "Sacamos una bola de una urna con bolas numeradas del 1 al 10.", "We draw a ball from an urn with balls numbered 1 to 10.") }
  };
  var GEN = {
    det: function () {
      var d = pick(DET);
      return ret({ opts: DETO, ans: d[1] }, function () { return fill(T(L3("«{e}». Quin tipus d'experiment és?", "«{e}». ¿Qué tipo de experimento es?", "“{e}”. What kind of experiment is it?")), { e: T(d[0]) }); },
        function () { return "<strong>" + T(DETO[d[1]]) + "</strong>: " + T(d[1] ? L3("en les mateixes condicions, el resultat és sempre el mateix; el podem saber abans de fer-lo.", "en las mismas condiciones, el resultado es siempre el mismo; lo podemos saber antes de hacerlo.", "under the same conditions the result is always the same; we can know it beforehand.") : L3("no podem saber el resultat abans de fer-lo, encara que coneguem tots els resultats possibles.", "no podemos saber el resultado antes de hacerlo, aunque conozcamos todos los resultados posibles.", "we can't know the result beforehand, even if we know all the possible results.")); });
    },
    cont: function () {
      var key = pick(Object.keys(CTB)), C = CTB[key], M, k, c, hide = null, guard = 0;
      do {
        M = [[rint(2, 20), rint(2, 20)], [rint(2, 20), rint(2, 20)]]; k = pick(["r0", "c0", "and", "or", "c1", "r1c1", "cond", "cond0", "condc"]); c = ctCount(M, ctEv(C, k));
      } while ((c.f === 0 || c.f === c.n) && ++guard < 50);
      if (rint(0, 2) === 0) hide = [rint(0, 1), rint(0, 1)];
      return ret(probQ(c.f, c.n), function () {
        var e = ctEv(C, k);
        return T(C.who) + " " + fill(T(L3("Triem una persona a l'atzar. Quina és la probabilitat de «{e}»?", "Elegimos una persona al azar. ¿Cuál es la probabilidad de «{e}»?", "We pick a person at random. What is the probability of “{e}”?")), { e: e.t })
          + (hide ? " " + T(L3("(Primer, troba la casella que falta.)", "(Primero, encuentra la casilla que falta.)", "(First, find the missing cell.)")) : "") + ctStatic(C, M, e, hide, false);
      }, function () {
        var e = ctEv(C, k), s = ctStatic(C, M, e, hide, true);
        if (hide) s += fill(T(L3("Casella que falta: {t} − {o} = {v}. ", "Casilla que falta: {t} − {o} = {v}. ", "Missing cell: {t} − {o} = {v}. ")), { t: M[hide[0]][0] + M[hide[0]][1], o: M[hide[0]][1 - hide[1]], v: M[hide[0]][hide[1]] });
        return s + fill(T(L3("{f} casos favorables de {n} possibles: ", "{f} casos favorables de {n} posibles: ", "{f} favourable out of {n} possible: ")), { f: c.f, n: c.n }) + ansTxt(c.f, c.n);
      });
    },
    tipus: function () {
      var c = CTX[pick(["d", "r", "b"])], N = c.n, k = rint(0, 3), e, E = range(1, N);
      var C = [
        [function () { var m = N + rint(1, 3); return { t: L3("traure un nombre menor que " + m, "sacar un número menor que " + m, "get a number less than " + m), s: E }; },
         function () { return { t: L3("traure un nombre més gran que 0", "sacar un número mayor que 0", "get a number greater than 0"), s: E }; },
         function () { return { t: L3("traure un nombre parell o senar", "sacar un número par o impar", "get an even or an odd number"), s: E }; }],
        [function () { var m = N + rint(1, 4); return { t: L3("traure un " + m, "sacar un " + m, "get a " + m), s: [] }; },
         function () { return { t: L3("traure un nombre més gran que " + N, "sacar un número mayor que " + N, "get a number greater than " + N), s: [] }; },
         function () { return { t: L3("traure un nombre parell i senar alhora", "sacar un número par e impar a la vez", "get a number that's both even and odd"), s: [] }; }],
        [function () { var m = rint(1, N); return { t: L3("traure un " + m, "sacar un " + m, "get a " + m), s: [m] }; },
         function () { return { t: L3("traure un nombre parell i primer", "sacar un número par y primo", "get an even prime number"), s: [2] }; },
         function () { return { t: L3("traure un nombre més gran que " + (N - 1), "sacar un número mayor que " + (N - 1), "get a number greater than " + (N - 1)), s: [N] }; }],
        [function () { return { t: L3("traure un nombre parell", "sacar un número par", "get an even number"), s: E.filter(function (x) { return x % 2 === 0; }) }; },
         function () { return { t: L3("traure un múltiple de 3", "sacar un múltiplo de 3", "get a multiple of 3"), s: E.filter(function (x) { return x % 3 === 0; }) }; },
         function () { var m = rint(3, N - 1); return { t: L3("traure un nombre menor que " + m, "sacar un número menor que " + m, "get a number less than " + m), s: range(1, m - 1) }; },
         function () { return { t: L3("traure un nombre primer", "sacar un número primo", "get a prime number"), s: E.filter(isPrime) }; }]
      ];
      e = pick(C[k])();
      return ret({ opts: KINDS, ans: k }, function () { return T(c.t) + " " + fill(T(L3("Quin tipus d'esdeveniment és «{e}»?", "¿Qué tipo de suceso es «{e}»?", "What kind of event is “{e}”?")), { e: T(e.t) }); },
        function () { return tex("E=" + setTex(E) + "\\qquad " + setTex(e.s)) + " → <strong>" + T(KINDS[k]) + "</strong>"; });
    },
    ops: function () {
      var U = pick([UNIV.d, UNIV.b, { n: 12, lo: 5, hi: 8, t: L3("1–12", "1–12", "1–12") }]), E = range(1, U.n), L = evList(U), A, B, ea, eb, o, k, sets, right, wr, guard = 0;
      do {
        ea = pick(L); eb = pick(L); A = E.filter(ea.f); B = E.filter(eb.f); o = opsOf(E, A, B);
        k = pick(["U", "I", "nA", "nB"]);
        right = o[k]; sets = [o.U, o.I, o.nA, o.nB, o.AnB, o.nU, A, B].filter(function (s) { return s.join() !== right.join(); });
        var seen = {}; wr = []; sets.forEach(function (s) { if (!seen[s.join()]) { seen[s.join()] = 1; wr.push(s); } });
      } while ((ea === eb || wr.length < 3 || !A.length || !B.length || A.length === E.length || B.length === E.length) && ++guard < 200);
      var sym = { U: "A\\cup B", I: "A\\cap B", nA: "\\overline{A}", nB: "\\overline{B}" }[k];
      var w3 = shuffle(wr).slice(0, 3).map(function (s) { var t = "$" + setTex(s) + "$"; return { va: t, es: t, en: t }; }), rt = "$" + setTex(right) + "$";
      var oo = optsTxt({ va: rt, es: rt, en: rt }, w3);
      var ctx = U.n === 6 ? CTX.d.t : U.n === 20 ? L3("Traiem una bola d'un bombo amb boles de l'1 al 20.", "Sacamos una bola de un bombo con bolas del 1 al 20.", "We draw a ball from a drum with balls 1 to 20.") : L3("Traiem una carta d'entre 12 cartes numerades de l'1 al 12.", "Sacamos una carta de entre 12 cartas numeradas del 1 al 12.", "We draw a card from 12 cards numbered 1 to 12.");
      return ret({ opts: oo.opts, ans: oo.ans }, function () { return T(ctx) + " " + fill(T(L3("Siguen A = «{a}» i B = «{b}». Quin és {o}?", "Sean A = «{a}» y B = «{b}». ¿Cuál es {o}?", "Let A = “{a}” and B = “{b}”. What is {o}?")), { a: T(ea.t), b: T(eb.t), o: "$" + sym + "$" }); },
        function () { return tex("A=" + setTex(A) + ",\\ B=" + setTex(B) + "\\ \\Rightarrow\\ " + sym + "=" + setTex(right)); });
    },
    prop: function () {
      var t = rint(0, 4), h = function () { return rint(1, 19) * 5 / 100; }, a, b, c, r2 = function (v) { return Math.round(v * 100) / 100; };
      if (t === 0) { a = rint(1, 99) / 100; return ret({ num: r2(1 - a), tol: 0.001 }, function () { return fill(T(L3("Si $P(A)={a}$, quant val $P(\\overline{A})$?", "Si $P(A)={a}$, ¿cuánto vale $P(\\overline{A})$?", "If $P(A)={a}$, what is $P(\\overline{A})$?")), { a: dz(a) }); }, function () { return tex("P(\\overline{A})=1-" + dz(a) + "=" + dz(r2(1 - a))); }); }
      if (t === 1) {
        do { a = h(); b = h(); c = rint(1, 8) * 5 / 100; } while (c >= Math.min(a, b) || a + b - c > 1);
        return ret({ num: r2(a + b - c), tol: 0.001 }, function () { return fill(T(L3("$P(A)={a}$, $P(B)={b}$ i $P(A\\cap B)={c}$. Calcula $P(A\\cup B)$.", "$P(A)={a}$, $P(B)={b}$ y $P(A\\cap B)={c}$. Calcula $P(A\\cup B)$.", "$P(A)={a}$, $P(B)={b}$ and $P(A\\cap B)={c}$. Find $P(A\\cup B)$.")), { a: dz(a), b: dz(b), c: dz(c) }); },
          function () { return tex("P(A\\cup B)=" + dz(a) + "+" + dz(b) + "-" + dz(c) + "=" + dz(r2(a + b - c))); });
      }
      if (t === 2) {
        do { a = h(); b = h(); c = rint(1, 8) * 5 / 100; } while (c >= Math.min(a, b) || a + b - c > 1);
        var u = r2(a + b - c);
        return ret({ num: c, tol: 0.001 }, function () { return fill(T(L3("$P(A)={a}$, $P(B)={b}$ i $P(A\\cup B)={u}$. Calcula $P(A\\cap B)$.", "$P(A)={a}$, $P(B)={b}$ y $P(A\\cup B)={u}$. Calcula $P(A\\cap B)$.", "$P(A)={a}$, $P(B)={b}$ and $P(A\\cup B)={u}$. Find $P(A\\cap B)$.")), { a: dz(a), b: dz(b), u: dz(u) }); },
          function () { return tex("P(A\\cap B)=" + dz(a) + "+" + dz(b) + "-" + dz(u) + "=" + dz(c)); });
      }
      if (t === 3) {
        do { a = h(); b = h(); } while (a + b > 1);
        return ret({ num: r2(a + b), tol: 0.001 }, function () { return fill(T(L3("$A$ i $B$ són incompatibles, amb $P(A)={a}$ i $P(B)={b}$. Calcula $P(A\\cup B)$.", "$A$ y $B$ son incompatibles, con $P(A)={a}$ y $P(B)={b}$. Calcula $P(A\\cup B)$.", "$A$ and $B$ are mutually exclusive, with $P(A)={a}$ and $P(B)={b}$. Find $P(A\\cup B)$.")), { a: dz(a), b: dz(b) }); },
          function () { return tex("P(A\\cup B)=" + dz(a) + "+" + dz(b) + "=" + dz(r2(a + b))); });
      }
      var ps; do { ps = [0, 0, 0, 0, 0].map(function () { return rint(1, 3) * 5 / 100; }); } while (ps.reduce(function (s, v) { return s + v; }, 0) > 0.9);
      var p6 = r2(1 - ps.reduce(function (s, v) { return s + v; }, 0));
      return ret({ num: p6, tol: 0.001 }, function () { return fill(T(L3("Un dau està trucat. $P(1)$, $P(2)$, $P(3)$, $P(4)$ i $P(5)$ valen {l}. Quant val $P(6)$?", "Un dado está trucado. $P(1)$, $P(2)$, $P(3)$, $P(4)$ y $P(5)$ valen {l}. ¿Cuánto vale $P(6)$?", "A die is loaded. $P(1)$, $P(2)$, $P(3)$, $P(4)$ and $P(5)$ are {l}. What is $P(6)$?")), { l: "$" + ps.map(dz).join(";\\ ") + "$" }); },
        function () { return tex("P(6)=1-(" + ps.map(dz).join("+") + ")=" + dz(p6)); });
    },
    /* experiències compostes independents: regla del producte i contrari */
    ind: function () {
      var t = rint(0, 2);
      if (t === 0) {
        var C = pick([
          { w: L3("La probabilitat que ploga dissabte és {p} i la que ploga diumenge, {q} (els dos dies són independents).", "La probabilidad de que llueva el sábado es {p} y la de que llueva el domingo, {q} (los dos días son independientes).", "The probability of rain on Saturday is {p} and on Sunday {q} (the two days are independent)."),
            e: { AB: L3("plou els dos dies", "llueve los dos días", "it rains both days"), no: L3("no plou cap dia", "no llueve ningún día", "it rains on neither day"), al: L3("plou almenys un dia", "llueve al menos un día", "it rains on at least one day"), one: L3("plou exactament un dia", "llueve exactamente un día", "it rains on exactly one day") } },
          { w: L3("L'Anna encerta la diana amb probabilitat {p} i el Biel, amb probabilitat {q}. Disparen una vegada cadascun.", "Ana acierta la diana con probabilidad {p} y Biel, con probabilidad {q}. Disparan una vez cada uno.", "Anna hits the target with probability {p} and Biel with probability {q}. Each shoots once."),
            e: { AB: L3("encerten tots dos", "aciertan los dos", "both hit"), no: L3("no encerta cap", "no acierta ninguno", "neither hits"), al: L3("la diana rep almenys un impacte", "la diana recibe al menos un impacto", "the target is hit at least once"), one: L3("només encerta un dels dos", "solo acierta uno de los dos", "only one of them hits") } },
          { w: L3("Un aparell té dues peces independents. La primera falla amb probabilitat {p} i la segona, amb probabilitat {q}.", "Un aparato tiene dos piezas independientes. La primera falla con probabilidad {p} y la segunda, con probabilidad {q}.", "A device has two independent parts. The first fails with probability {p} and the second with probability {q}."),
            e: { AB: L3("fallen les dues", "fallan las dos", "both fail"), no: L3("no en falla cap", "no falla ninguna", "neither fails"), al: L3("en falla almenys una", "falla al menos una", "at least one fails"), one: L3("en falla exactament una", "falla exactamente una", "exactly one fails") } }]);
        var p = rint(1, 9) / 10, q = rint(1, 9) / 10, k = pick(["AB", "no", "al", "one"]), np = r2_(1 - p), nq = r2_(1 - q);
        var v = k === "AB" ? p * q : k === "no" ? np * nq : k === "al" ? 1 - np * nq : p * nq + np * q; v = r2_(v);
        return ret({ num: v, tol: 0.0051 }, function () { return fill(T(C.w), { p: "$" + dz(p) + "$", q: "$" + dz(q) + "$" }) + " " + fill(T(L3("Quina és la probabilitat que {e}?", "¿Cuál es la probabilidad de que {e}?", "What is the probability that {e}?")), { e: T(C.e[k]) }); },
          function () {
            return tex(k === "AB" ? dz(p) + "\\cdot" + dz(q) + "=" + dz(v) : k === "no" ? "(1-" + dz(p) + ")\\cdot(1-" + dz(q) + ")=" + dz(np) + "\\cdot" + dz(nq) + "=" + dz(v)
              : k === "al" ? "1-" + dz(np) + "\\cdot" + dz(nq) + "=1-" + dz(r2_(np * nq)) + "=" + dz(v) : dz(p) + "\\cdot" + dz(nq) + "+" + dz(np) + "\\cdot" + dz(q) + "=" + dz(v));
          });
      }
      if (t === 1) {
        var n = rint(2, 3), s = rint(0, 1);
        var num = s ? Math.pow(6, n) - Math.pow(5, n) : 1, den = Math.pow(6, n);
        return ret(probQ(num, den), function () { return fill(T(s ? L3("Llancem {n} daus. Quina és la probabilitat de traure almenys un 6?", "Lanzamos {n} dados. ¿Cuál es la probabilidad de sacar al menos un 6?", "We roll {n} dice. What is the probability of getting at least one 6?") : L3("Llancem {n} daus. Quina és la probabilitat que tots siguen 6?", "Lanzamos {n} dados. ¿Cuál es la probabilidad de que todos sean 6?", "We roll {n} dice. What is the probability that they're all 6s?")), { n: n }); },
          function () { return s ? tex("1-P(\\text{" + T(L3("cap 6", "ningún 6", "no 6")) + "})=1-\\left(\\frac56\\right)^" + n + "=1-\\frac{" + Math.pow(5, n) + "}{" + den + "}=" + ft(num, den) + apx(num, den)) : tex("\\left(\\frac16\\right)^" + n + "=" + ft(num, den) + apx(num, den)); });
      }
      var m = rint(2, 4), o = pick([2, 3, 4]), z = rint(0, 2), nm, dn;
      if (z === 0) { nm = 1; dn = Math.pow(o, m); }
      else if (z === 1) { nm = Math.pow(o - 1, m); dn = Math.pow(o, m); }
      else { nm = Math.pow(o, m) - Math.pow(o - 1, m); dn = Math.pow(o, m); }
      return ret(probQ(nm, dn), function () { return fill(T(L3("Un test té {m} preguntes amb {o} opcions cadascuna (només una correcta). Contestem a l'atzar. Quina és la probabilitat {e}?", "Un test tiene {m} preguntas con {o} opciones cada una (solo una correcta). Contestamos al azar. ¿Cuál es la probabilidad {e}?", "A test has {m} questions with {o} options each (only one correct). We answer at random. What is the probability {e}?")),
        { m: m, o: o, e: T([L3("d'encertar-les totes", "de acertarlas todas", "of getting them all right"), L3("de no encertar-ne cap", "de no acertar ninguna", "of getting none right"), L3("d'encertar-ne almenys una", "de acertar al menos una", "of getting at least one right")][z]) }); },
        function () { var b = "\\left(\\frac{" + (z === 0 ? 1 : o - 1) + "}{" + o + "}\\right)^" + m; return tex((z === 2 ? "1-\\left(\\frac{" + (o - 1) + "}{" + o + "}\\right)^" + m : b) + "=" + ft(nm, dn) + apx(nm, dn)); });
    },
    /* experiències dependents: extraccions sense reemplaçament i probabilitat condicionada */
    dep: function () {
      var t = rint(0, 2);
      if (t === 0) {
        var r = rint(3, 7), b = rint(2, 6), n = r + b, col = rint(0, 1), k = col ? b : r;
        return ret(probQ(k * (k - 1) * (k - 2), n * (n - 1) * (n - 2)), function () { return fill(T(L3("En una bossa hi ha {r} boles roges i {b} de blaves. En traiem tres sense reemplaçament. Quina és la probabilitat que les tres siguen {c}?", "En una bolsa hay {r} bolas rojas y {b} azules. Sacamos tres sin reemplazamiento. ¿Cuál es la probabilidad de que las tres sean {c}?", "A bag has {r} red and {b} blue balls. We draw three without replacement. What is the probability that all three are {c}?")), { r: r, b: b, c: T(col ? L3("blaves", "azules", "blue") : L3("roges", "rojas", "red")) }); },
          function () { return tex("\\frac{" + k + "}{" + n + "}\\cdot\\frac{" + (k - 1) + "}{" + (n - 1) + "}\\cdot\\frac{" + (k - 2) + "}{" + (n - 2) + "}=" + ft(k * (k - 1) * (k - 2), n * (n - 1) * (n - 2)) + apx(k * (k - 1) * (k - 2), n * (n - 1) * (n - 2))); });
      }
      if (t === 1) {
        var r1 = rint(2, 8), b1 = rint(2, 8), n1 = r1 + b1, first = pick(["R", "B"]), sec = pick(["R", "B"]);
        var f = (sec === "R" ? r1 : b1) - (first === sec ? 1 : 0);
        var cn = { R: L3("roja", "roja", "red"), B: L3("blava", "azul", "blue") };
        return ret(probQ(f, n1 - 1), function () { return fill(T(L3("En una bossa hi ha {r} boles roges i {b} de blaves. Traiem una bola, és {x} i no la tornem. Quina és la probabilitat que la segona siga {y}?", "En una bolsa hay {r} bolas rojas y {b} azules. Sacamos una bola, es {x} y no la devolvemos. ¿Cuál es la probabilidad de que la segunda sea {y}?", "A bag has {r} red and {b} blue balls. We draw a ball, it's {x}, and we don't put it back. What is the probability that the second one is {y}?")), { r: r1, b: b1, x: T(cn[first]), y: T(cn[sec]) }); },
          function () { return T(L3("Queden ", "Quedan ", "There are ")) + (n1 - 1) + T(L3(" boles, de les quals ", " bolas, de las cuales ", " balls left, of which ")) + f + " " + T(cn[sec]) + ": " + tex("P(" + sec + "_2/" + first + "_1)=" + fs(f, n1 - 1) + apx(f, n1 - 1)); });
      }
      var K = pick([
        { t: L3("dos oros", "dos oros", "two coins cards"), a: 10, b: 9 }, { t: L3("dos asos", "dos ases", "two aces"), a: 4, b: 3 }, { t: L3("dues figures", "dos figuras", "two face cards"), a: 12, b: 11 },
        { t: L3("primer un as i després un rei", "primero un as y después un rey", "first an ace and then a king"), a: 4, b: 4 }, { t: L3("dues cartes de copes", "dos cartas de copas", "two cups cards"), a: 10, b: 9 }]);
      return ret(probQ(K.a * K.b, 40 * 39), function () { return fill(T(L3("Traiem dues cartes d'una baralla espanyola de 40 cartes, sense reemplaçament. Quina és la probabilitat de traure {e}?", "Sacamos dos cartas de una baraja española de 40 cartas, sin reemplazamiento. ¿Cuál es la probabilidad de sacar {e}?", "We draw two cards from a 40-card Spanish pack without replacement. What is the probability of getting {e}?")), { e: T(K.t) }); },
        function () { return tex("\\frac{" + K.a + "}{40}\\cdot\\frac{" + K.b + "}{39}=\\frac{" + K.a * K.b + "}{1560}=" + ft(K.a * K.b, 1560) + apx(K.a * K.b, 1560)); });
    },
    /* dues urnes: probabilitat total sumant camins */
    urn: function () {
      var sel = pick(Object.keys(USEL)), r1 = rint(1, 6), b1 = rint(1, 6), r2 = rint(1, 6), b2 = rint(1, 6), ek = pick(["R", "R", "B", "IR"]), tr = urnTree(sel, r1, b1, r2, b2, UEV[ek].f);
      var how = { m: L3("Llancem una moneda: si ix cara traiem una bola de la urna I, i si ix creu, de la urna II.", "Lanzamos una moneda: si sale cara sacamos una bola de la urna I, y si sale cruz, de la urna II.", "We toss a coin: heads, we draw from urn I; tails, from urn II."),
        d: L3("Llancem un dau: si ix 1 o 2 traiem una bola de la urna I, i si no, de la urna II.", "Lanzamos un dado: si sale 1 o 2 sacamos una bola de la urna I, y si no, de la urna II.", "We roll a die: 1 or 2, we draw from urn I; otherwise, from urn II."),
        s: L3("Llancem un dau: si ix 6 traiem una bola de la urna I, i si no, de la urna II.", "Lanzamos un dado: si sale 6 sacamos una bola de la urna I, y si no, de la urna II.", "We roll a die: 6, we draw from urn I; otherwise, from urn II.") };
      return ret(probQ(tr.n, tr.d), function () { return fill(T(L3("La urna I té {a} boles roges i {b} de blaves; la urna II, {c} de roges i {d} de blaves.", "La urna I tiene {a} bolas rojas y {b} azules; la urna II, {c} rojas y {d} azules.", "Urn I has {a} red and {b} blue balls; urn II, {c} red and {d} blue.")), { a: r1, b: b1, c: r2, d: b2 }) + " " + T(how[sel]) + " " + fill(T(L3("Quina és la probabilitat de «{e}»?", "¿Cuál es la probabilidad de «{e}»?", "What is the probability of “{e}”?")), { e: T(UEV[ek].t) }); },
        function () { return treeSvg(tr.kids, { W: 360, leafw: 110 }) + tex(treeSum(tr)); });
    },
    /* les probabilitats dels resultats elementals sumen 1 i se sumen per a un esdeveniment compost */
    falta: function () {
      var t = rint(0, 2), r2 = function (v) { return Math.round(v * 100) / 100; }, ps, tot;
      if (t === 1) {
        var C = [L3("roig", "rojo", "red"), L3("blau", "azul", "blue"), L3("verd", "verde", "green"), L3("groc", "amarillo", "yellow")];
        do { ps = [0, 0, 0].map(function () { return rint(1, 6) * 5 / 100; }); tot = ps[0] + ps[1] + ps[2]; } while (tot > 0.9);
        var pg = r2(1 - tot);
        return ret({ num: pg, tol: 0.001 }, function () { return fill(T(L3("Una ruleta té sectors roig, blau, verd i groc. $P(\\text{roig})={a}$, $P(\\text{blau})={b}$ i $P(\\text{verd})={c}$. Quina és la probabilitat que isca groc?", "Una ruleta tiene sectores rojo, azul, verde y amarillo. $P(\\text{rojo})={a}$, $P(\\text{azul})={b}$ y $P(\\text{verde})={c}$. ¿Cuál es la probabilidad de que salga amarillo?", "A spinner has red, blue, green and yellow sectors. $P(\\text{red})={a}$, $P(\\text{blue})={b}$ and $P(\\text{green})={c}$. What is the probability of yellow?")), { a: dz(ps[0]), b: dz(ps[1]), c: dz(ps[2]) }); },
          function () { return T(L3("Els quatre colors sumen 1:", "Los cuatro colores suman 1:", "The four colours add up to 1:")) + " " + tex("1-(" + ps.map(dz).join("+") + ")=" + dz(pg)); });
      }
      do { ps = [0, 0, 0, 0, 0].map(function () { return rint(1, 3) * 5 / 100; }); tot = ps.reduce(function (s, v) { return s + v; }, 0); } while (tot > 0.9);
      var p6 = r2(1 - tot), all = ps.concat([p6]);
      if (t === 0) return ret({ num: p6, tol: 0.001 }, function () { return fill(T(L3("Un dau està trucat. $P(1)$, $P(2)$, $P(3)$, $P(4)$ i $P(5)$ valen {l}. Quant val $P(6)$?", "Un dado está trucado. $P(1)$, $P(2)$, $P(3)$, $P(4)$ y $P(5)$ valen {l}. ¿Cuánto vale $P(6)$?", "A die is loaded. $P(1)$, $P(2)$, $P(3)$, $P(4)$ and $P(5)$ are {l}. What is $P(6)$?")), { l: "$" + ps.map(dz).join(";\\ ") + "$" }); },
        function () { return tex("P(6)=1-(" + ps.map(dz).join("+") + ")=" + dz(p6)); });
      var E = pick([{ t: L3("parell", "par", "even"), s: [2, 4, 6] }, { t: L3("senar", "impar", "odd"), s: [1, 3, 5] }, { t: L3("més gran que 3", "mayor que 3", "greater than 3"), s: [4, 5, 6] }, { t: L3("menor que 3", "menor que 3", "less than 3"), s: [1, 2] }]);
      var v = r2(E.s.reduce(function (s, k) { return s + all[k - 1]; }, 0));
      return ret({ num: v, tol: 0.001 }, function () { return fill(T(L3("Un dau està trucat i les probabilitats de l'1 al 6 són {l}. Quina és la probabilitat de traure un nombre {e}?", "Un dado está trucado y las probabilidades del 1 al 6 son {l}. ¿Cuál es la probabilidad de sacar un número {e}?", "A die is loaded and the probabilities of 1 to 6 are {l}. What is the probability of rolling a number that is {e}?")), { l: "$" + all.map(dz).join(";\\ ") + "$", e: T(E.t) }); },
        function () { return tex(E.s.map(function (k) { return "P(" + k + ")"; }).join("+") + "=" + E.s.map(function (k) { return dz(all[k - 1]); }).join("+") + "=" + dz(v)); });
    },
    lap: function () {
      var t = rint(0, 3);
      if (t === 0) {
        var c = { R: rint(1, 8), B: rint(1, 8), V: rint(0, 6) }, n = c.R + c.B + c.V, col = pick(["R", "B", "V"].filter(function (k) { return c[k]; })), neg = rint(0, 2) === 0, f = neg ? n - c[col] : c[col];
        return ret(probQ(f, n), function () { return fill(T(L3("En una bossa hi ha {r} boles roges, {b} de blaves i {v} de verdes. Traiem una bola a l'atzar. Quina és la probabilitat que {n}siga {c}?", "En una bolsa hay {r} bolas rojas, {b} azules y {v} verdes. Sacamos una bola al azar. ¿Cuál es la probabilidad de que {n}sea {c}?", "A bag has {r} red, {b} blue and {v} green balls. We draw one at random. What is the probability that it {n} {c}?")), { r: c.R, b: c.B, v: c.V, n: neg ? T(L3("no ", "no ", "isn't")) : (lang === "en" ? "is" : ""), c: T(CNAME[col]) }) + bagSvg(bagSpec(c)); },
          function () { return ansTxt(f, n); });
      }
      if (t === 1) {
        var C = pick([
          { t: L3("traure un nombre parell", "sacar un número par", "get an even number"), f: function (x) { return x % 2 === 0; } },
          { t: L3("traure un múltiple de 3", "sacar un múltiplo de 3", "get a multiple of 3"), f: function (x) { return x % 3 === 0; } },
          { t: L3("traure un nombre primer", "sacar un número primo", "get a prime number"), f: isPrime },
          { t: L3("traure un múltiple de 4", "sacar un múltiplo de 4", "get a multiple of 4"), f: function (x) { return x % 4 === 0; } }]), N = pick([6, 8, 10, 12, 20]);
        var fv = range(1, N).filter(C.f).length;
        return ret(probQ(fv, N), function () { return fill(T(L3("Girem una ruleta de {n} sectors iguals numerats de l'1 al {n}. Quina és la probabilitat de {e}?", "Giramos una ruleta de {n} sectores iguales numerados del 1 al {n}. ¿Cuál es la probabilidad de {e}?", "We spin a wheel with {n} equal sectors numbered 1 to {n}. What is the probability to {e}?")), { n: N, e: T(C.t) }); },
          function () { return tex(setTex(range(1, N).filter(C.f))) + ": " + ansTxt(fv, N); });
      }
      if (t === 2) {
        var K = pick([
          { t: L3("un oro", "un oro", "a coins card"), f: 10 }, { t: L3("una figura (sota, cavall o rei)", "una figura (sota, caballo o rey)", "a face card (jack, knight or king)"), f: 12 }, { t: L3("un as", "un as", "an ace"), f: 4 },
          { t: L3("el rei d'espases", "el rey de espadas", "the king of swords"), f: 1 }, { t: L3("una carta que no siga de bastos", "una carta que no sea de bastos", "a card that isn't clubs"), f: 30 },
          { t: L3("un as o un rei", "un as o un rey", "an ace or a king"), f: 8 }, { t: L3("una copa o una figura", "una copa o una figura", "a cups card or a face card"), f: 19 }]);
        return ret(probQ(K.f, 40), function () { return fill(T(L3("Traiem una carta d'una baralla espanyola de 40 cartes. Quina és la probabilitat que siga {e}?", "Sacamos una carta de una baraja española de 40 cartas. ¿Cuál es la probabilidad de que sea {e}?", "We draw a card from a 40-card Spanish pack. What is the probability that it's {e}?")), { e: T(K.t) }); },
          function () { return ansTxt(K.f, 40); });
      }
      var Wd = pick(["MATEMATIQUES", "PROBABILITAT", "ESDEVENIMENT", "ALEATORI", "LAPLACE"]), lt = pick(Wd.split("").filter(function (x, i, a) { return a.indexOf(x) === i; }));
      var voc = rint(0, 1), fw = voc ? Wd.split("").filter(function (x) { return "AEIOU".indexOf(x) >= 0; }).length : Wd.split("").filter(function (x) { return x === lt; }).length;
      return ret(probQ(fw, Wd.length), function () { return fill(T(L3("Escrivim cada lletra de la paraula {w} en una targeta i en traiem una a l'atzar. Quina és la probabilitat que siga {e}?", "Escribimos cada letra de la palabra {w} en una tarjeta y sacamos una al azar. ¿Cuál es la probabilidad de que sea {e}?", "We write each letter of the word {w} on a card and draw one at random. What is the probability that it's {e}?")), { w: "<strong>" + Wd + "</strong>", e: voc ? T(L3("una vocal", "una vocal", "a vowel")) : T(L3("la lletra ", "la letra ", "the letter ")) + lt }); },
        function () { return fill(T(L3("{n} lletres: ", "{n} letras: ", "{n} letters: ")), { n: Wd.length }) + ansTxt(fw, Wd.length); });
    },
    freq: function () {
      var t = rint(0, 2);
      if (t === 0) {
        var n = pick([20, 25, 40, 50, 80, 100, 200, 250, 400, 500]), f = rint(Math.round(n * 0.1), Math.round(n * 0.9)), X = pick([L3("una xinxeta ha caigut amb la punta cap amunt", "una chincheta ha caído con la punta hacia arriba", "a drawing pin landed point up"), L3("un tap de suro ha caigut dret", "un tapón de corcho ha caído de pie", "a cork landed upright"), L3("una jugadora ha encertat el tir", "una jugadora ha acertado el tiro", "a player scored the shot")]);
        return ret({ num: f / n, tol: 0.0051 }, function () { return fill(T(L3("En {n} intents, {x} {f} vegades. Quina és la freqüència relativa?", "En {n} intentos, {x} {f} veces. ¿Cuál es la frecuencia relativa?", "In {n} trials, {x} {f} times. What is the relative frequency?")), { n: n, x: T(X), f: f }); },
          function () { return tex("h=\\frac{" + f + "}{" + n + "}" + (Math.abs(f / n * 100 - Math.round(f / n * 100)) < 1e-9 ? "=" : "\\approx ") + dz(Math.round(f / n * 100) / 100)); });
      }
      if (t === 1) {
        var pr = pick([[1, 6, L3("traure un 6 amb un dau", "sacar un 6 con un dado", "rolling a 6 on a die"), 6], [1, 2, L3("traure cara amb una moneda", "sacar cara con una moneda", "getting heads on a coin"), 2], [1, 4, L3("traure oros d'una baralla espanyola", "sacar oros de una baraja española", "drawing a coins card from a Spanish pack"), 4], [62, 100, L3("que una xinxeta caiga amb la punta cap amunt (P ≈ 0,62)", "que una chincheta caiga con la punta hacia arriba (P ≈ 0,62)", "a drawing pin landing point up (P ≈ 0.62)"), 50]]);
        var N = pr[3] * rint(5, 60);
        return ret({ num: N * pr[0] / pr[1], tol: 0.51 }, function () { return fill(T(L3("Repetim {n} vegades l'experiment de {e}. Quantes vegades esperem, aproximadament, que ocórrega?", "Repetimos {n} veces el experimento de {e}. ¿Cuántas veces esperamos, aproximadamente, que ocurra?", "We repeat {e} {n} times. About how many times do we expect it to happen?")), { n: N, e: T(pr[2]) }); },
          function () { return tex(N + "\\cdot" + (pr[1] === 100 ? "0\\dc 62" : "\\frac{" + pr[0] + "}{" + pr[1] + "}") + "=" + nf(N * pr[0] / pr[1])); });
      }
      var Nb = pick([10, 20, 25]), x = rint(1, Nb - 1), ne = 500, k = Math.round(ne * x / Nb + rint(-8, 8)), est = Math.round(Nb * k / ne);
      return ret({ num: Nb * k / ne, tol: 0.51 }, function () { return fill(T(L3("En una bossa hi ha {N} boles, unes blanques i altres negres. Traiem una bola, n'anotem el color i la tornem. Després de {n} extraccions n'han eixit {k} de negres. Quantes boles negres deu haver-hi? (arrodoneix a les unitats)", "En una bolsa hay {N} bolas, unas blancas y otras negras. Sacamos una bola, anotamos su color y la devolvemos. Después de {n} extracciones han salido {k} negras. ¿Cuántas bolas negras debe de haber? (redondea a las unidades)", "A bag has {N} balls, some white and some black. We draw a ball, note its colour and put it back. After {n} draws, {k} have been black. How many black balls are there likely to be? (round to a whole number)")), { N: Nb, n: ne, k: k }); },
        function () { return tex("h=\\frac{" + k + "}{" + ne + "}=" + dz(k / ne) + "\\qquad " + Nb + "\\cdot" + dz(k / ne) + "=" + dz(Nb * k / ne) + "\\approx " + est); });
    },
    dice: function () {
      var op = pick(["s", "s", "d", "p"]), rel = pick(["eq", "eq", "le", "ge"]), R = DRANGE[op], k, cnt, f;
      do { k = rint(R[0], R[1]); f = relF(rel, k); cnt = 0; for (var a = 1; a <= 6; a++) for (var b = 1; b <= 6; b++) if (f(DOPS[op](a, b))) cnt++; } while (cnt === 0 || cnt === 36);
      var rw = { eq: L3("siga", "sea", "is"), le: L3("siga menor o igual que", "sea menor o igual que", "is at most"), ge: L3("siga major o igual que", "sea mayor o igual que", "is at least") };
      return ret(probQ(cnt, 36), function () { return fill(T(L3("Llancem dos daus. Quina és la probabilitat que la {o} dels punts {r} {k}?", "Lanzamos dos dados. ¿Cuál es la probabilidad de que la {o} de los puntos {r} {k}?", "We roll two dice. What is the probability that the {o} of the scores {r} {k}?")), { o: T(DOPN[op]), r: T(rw[rel]), k: k }); },
        function () { return diceHtml(op, function (a, b) { return f(DOPS[op](a, b)); }) + ansTxt(cnt, 36); });
    },
    tree: function () {
      var r, b, rep, ek, t;
      do { r = rint(1, 6); b = rint(1, 6); rep = rint(0, 1) === 1; ek = pick(Object.keys(TEV)); t = bagTree(r, b, rep, TEV[ek].f); } while (t.n === 0);
      return ret(probQ(t.n, t.d), function () { return fill(T(L3("En una bossa hi ha {r} boles roges i {b} de blaves. En traiem dues {m}. Quina és la probabilitat de traure {e}?", "En una bolsa hay {r} bolas rojas y {b} azules. Sacamos dos {m}. ¿Cuál es la probabilidad de sacar {e}?", "A bag has {r} red and {b} blue balls. We draw two {m}. What is the probability of getting {e}?")), { r: r, b: b, m: rep ? T(L3("amb reemplaçament", "con reemplazamiento", "with replacement")) : T(L3("sense reemplaçament", "sin reemplazamiento", "without replacement")), e: T(TEV[ek].t) }); },
        function () { return treeSvg(t.kids, { W: 360, leafw: 120 }) + tex(treeSum(t)); });
    }
  };

  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, res = 0, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore"), ob = w.querySelector(".dopts");
    function paint() {
      dq.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (ob) {
        ob.innerHTML = "";
        q.opts.forEach(function (o, j) {
          var b = document.createElement("button"); b.type = "button"; b.className = "btn"; b.innerHTML = rtex(T(o));
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
        var v = numIn(String(inp.value).replace("%", "")); if (v === null) { info.innerHTML = warn(u("num")); return; }
        if (/%/.test(inp.value)) v /= 100;
        good = Math.abs(v - q.num) <= (q.tol || 1e-6);
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
  window.FM411 = { GEN: GEN, bagTree: bagTree, urnTree: urnTree, treeSum: treeSum, ctEvents: ctEvents, ctCount: ctCount, CTB: CTB, DET: DET, DOPS: DOPS, numIn: numIn, ft: ft, opsOf: opsOf };

  /* ---------- qüestionari ---------- */
  var QUIZ = [
/*QUIZ*/
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

  var TITLES = { va: "Probabilitat · FentMates", es: "Probabilidad · FentMates", en: "Probability · FentMates" };
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
    wEsp(); wOps(); wProp(); wBag(); wLgn(); wDice2(); wInd(); wTree(); wUrn(); wCont();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
