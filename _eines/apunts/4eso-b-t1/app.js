(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-4eso-b-u1-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top" }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  function t3(va, es, en) { return lang === "es" ? es : lang === "en" ? en : va; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }
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
  var COL = { a: "#3b82f6", b: "#f97316", r: "#e11d48", k: "#16a34a" };

  /* ---------- nombres ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function decS(x, k) { var s = String(+x.toFixed(k == null ? 2 : k)); if (s === "-0") s = "0"; return lang === "en" ? s : s.replace(".", ","); }
  function dT(x, k) { return decS(x, k).replace(",", "{,}"); }
  function frac(x) { if (!isFinite(x)) return null; for (var d = 1; d <= 12; d++) { var n = Math.round(x * d); if (Math.abs(n / d - x) < 1e-9) return [n, d]; } return null; }
  // nombre en TeX: enter, fracció (denominador ≤ 12) o decimal
  function nT(x) {
    if (x === Infinity) return "+\\infty"; if (x === -Infinity) return "-\\infty";
    var f = frac(x);
    if (f) return f[1] === 1 ? String(f[0]) : (f[0] < 0 ? "-" : "") + "\\frac{" + Math.abs(f[0]) + "}{" + f[1] + "}";
    return dT(x, 3);
  }
  // el mateix, en text pla per a l'SVG
  function nS(x) { var f = frac(x); if (f && f[1] !== 1) return (f[0] < 0 ? "−" : "") + Math.abs(f[0]) + "/" + f[1]; return decS(x, 2).replace("-", "−"); }
  function parseNum(s) {
    s = s.replace(/−/g, "-").replace(/\s/g, "").replace(",", ".").toLowerCase();
    if (/^\+?(inf|∞)$/.test(s)) return Infinity;
    if (/^-(inf|∞)$/.test(s)) return -Infinity;
    var m = s.match(/^(-?\d+(?:\.\d+)?)\/(\d+(?:\.\d+)?)$/); if (m && +m[2] !== 0) return +m[1] / +m[2];
    if (/^[-+]?\d+(\.\d+)?$/.test(s)) return +s;
    return NaN;
  }

  /* ---------- intervals: {a, ac, b, bc}; un conjunt és una llista ordenada d'intervals disjunts ---------- */
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
  function cap2(I, J) {
    return { a: Math.max(I.a, J.a), ac: I.a > J.a ? I.ac : J.a > I.a ? J.ac : I.ac && J.ac,
      b: Math.min(I.b, J.b), bc: I.b < J.b ? I.bc : J.b < I.b ? J.bc : I.bc && J.bc };
  }
  function cap(S, T) { var r = []; S.forEach(function (I) { T.forEach(function (J) { r.push(cap2(I, J)); }); }); return norm(r); }
  function cup(S, T) { return norm(S.concat(T)); }
  function compl(S) {
    var r = [], a = -Infinity, ac = false;
    norm(S).forEach(function (I) { r.push({ a: a, ac: ac, b: I.a, bc: !I.ac }); a = I.b; ac = !I.bc; });
    r.push({ a: a, ac: ac, b: Infinity, bc: false }); return norm(r);
  }
  function minus(S, T) { return cap(S, compl(T)); }
  function parseIv(s) {
    var m = s.trim().replace(/−/g, "-").match(/^([\[\(\]])\s*([^,;]+?)\s*[,;]\s*([^,;]+?)\s*([\]\)\[])$/);
    if (!m) return null;
    var a = parseNum(m[2]), b = parseNum(m[3]);
    if (isNaN(a) || isNaN(b)) return null;
    return { a: a, ac: m[1] === "[", b: b, bc: m[4] === "]" };
  }
  function ivT(I) { return I.a === I.b ? "\\{" + nT(I.a) + "\\}" : (I.ac ? "[" : "(") + nT(I.a) + ",\\," + nT(I.b) + (I.bc ? "]" : ")"); }
  function setT(S) { S = norm(S); return S.length ? S.map(ivT).join("\\cup ") : "\\varnothing"; }

  /* ---------- recta real en SVG ---------- */
  function range(sets) {
    var p = [];
    sets.forEach(function (S) { S.forEach(function (I) { if (isFinite(I.a)) p.push(I.a); if (isFinite(I.b)) p.push(I.b); }); });
    if (!p.length) p = [0];
    var lo = Math.floor(Math.min.apply(null, p)) - 1, hi = Math.ceil(Math.max.apply(null, p)) + 1;
    if (hi - lo < 8) { var c = (hi + lo) / 2; lo = Math.floor(c - 4); hi = Math.ceil(c + 4); }
    return [lo, hi];
  }
  // rows: [{S, c (color), l (etiqueta)}]; W ample del viewBox
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
  // ample del viewBox segons l'ample real de l'SVG: al mòbil els números de la recta es llegeixen igual de bé
  function svgW(svg) { var w = svg.getBoundingClientRect().width; return w ? Math.max(300, Math.min(600, Math.round(w))) : 600; }
  var resizeT; window.addEventListener("resize", function () { clearTimeout(resizeT); resizeT = setTimeout(function () { refreshers.forEach(function (fn) { fn(); }); }, 150); });

  /* ---------- 1.1 classificador ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  function wCls() {
    var w = document.getElementById("w-cls"); if (!w) return;
    var POOL = [
      ["\\sqrt5", "I", q3("No és un quadrat perfecte: té infinites xifres decimals no periòdiques.", "No es un cuadrado perfecto: tiene infinitas cifras decimales no periódicas.", "It isn't a perfect square: infinitely many non-repeating decimals.")],
      ["-3", "Z", q3("És un enter negatiu.", "Es un entero negativo.", "It's a negative integer.")],
      ["\\dfrac{24}{6}", "N", q3("$\\frac{24}{6}=4$, un natural.", "$\\frac{24}{6}=4$, un natural.", "$\\frac{24}{6}=4$, a natural number.")],
      ["[2{,}45|2.45]", "Q", q3("Decimal exacte: $\\frac{245}{100}=\\frac{49}{20}$.", "Decimal exacto: $\\frac{245}{100}=\\frac{49}{20}$.", "Terminating decimal: $\\frac{245}{100}=\\frac{49}{20}$.")],
      ["\\pi", "I", q3("Infinites xifres decimals sense període.", "Infinitas cifras decimales sin periodo.", "Infinitely many digits with no repeating block.")],
      ["\\dfrac{5}{12}", "Q", q3("És una fracció no entera.", "Es una fracción no entera.", "A fraction that isn't a whole number.")],
      ["0", "N", q3("El 0 el considerem natural.", "El 0 lo consideramos natural.", "We count 0 as a natural number.")],
      ["-\\sqrt{16}", "Z", q3("$-\\sqrt{16}=-4$.")],
      ["[2{,}3\\widehat{45}|2.3\\widehat{45}]", "Q", q3("Decimal periòdic: té fracció generatriu.", "Decimal periódico: tiene fracción generatriz.", "Repeating decimal: it has a generating fraction.")],
      ["\\sqrt[3]{-8}", "Z", q3("$\\sqrt[3]{-8}=-2$, perquè $(-2)^3=-8$.", "$\\sqrt[3]{-8}=-2$, porque $(-2)^3=-8$.", "$\\sqrt[3]{-8}=-2$, because $(-2)^3=-8$.")],
      ["\\dfrac{1+\\sqrt5}{2}", "I", q3("És el nombre d'or $\\phi$: conté $\\sqrt5$.", "Es el número de oro $\\phi$: contiene $\\sqrt5$.", "It's the golden ratio $\\phi$: it contains $\\sqrt5$.")],
      ["[0{,}1010010001\\ldots|0.1010010001\\ldots]", "I", q3("Infinites xifres i cap bloc no es repeteix.", "Infinitas cifras y ningún bloque se repite.", "Infinitely many digits and no block repeats.")],
      ["\\sqrt{\\tfrac94}", "Q", q3("$\\sqrt{9/4}=\\frac32$.")],
      ["\\sqrt2\\cdot\\sqrt8", "N", q3("$\\sqrt{16}=4$: el producte de dos irracionals pot ser racional!", "$\\sqrt{16}=4$: ¡el producto de dos irracionales puede ser racional!", "$\\sqrt{16}=4$: the product of two irrationals can be rational!")],
      ["\\sqrt2+\\sqrt8", "I", q3("$\\sqrt2+2\\sqrt2=3\\sqrt2$, irracional.", "$\\sqrt2+2\\sqrt2=3\\sqrt2$, irracional.", "$\\sqrt2+2\\sqrt2=3\\sqrt2$, irrational.")],
      ["-\\dfrac{18}{3}", "Z", q3("$-\\frac{18}{3}=-6$.")],
      ["e", "I", q3("El nombre $e\\approx2{,}718\\ldots$ és irracional.", "El número $e\\approx2{,}718\\ldots$ es irracional.", "The number $e\\approx2.718\\ldots$ is irrational.")],
      ["[1{,}\\widehat9|1.\\widehat9]", "N", q3("Curiositat: $1{,}\\widehat9=\\frac{19-1}{9}=2$.", "Curiosidad: $1{,}\\widehat9=\\frac{19-1}{9}=2$.", "Fun fact: $1.\\widehat9=\\frac{19-1}{9}=2$.")],
      ["\\dfrac{22}{7}", "Q", q3("És una aproximació de $\\pi$, però és una fracció.", "Es una aproximación de $\\pi$, pero es una fracción.", "It approximates $\\pi$, but it is a fraction.")]
    ];
    var SETS = ["N", "Z", "Q", "I"], SYM = { N: "\\mathbb N", Z: "\\mathbb Z", Q: "\\mathbb Q", I: "\\mathbb I" };
    var order = [], idx = -1, pick = null, ok = 0, tot = 0;
    function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function loc(s) { return s.replace(/\[([^|\]]*)\|([^\]]*)\]/g, function (_, c, p) { return lang === "en" ? p : c; }); }
    function rt(s) { return s.replace(/\$([^$]+)\$/g, function (_, m) { return tex(m); }); }
    var btns = $(w, "btns"), sets = $(w, "sets"), fb = $(w, "fb");
    SETS.forEach(function (k) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn"; b.dataset.k = k; b.innerHTML = tex(SYM[k]);
      b.addEventListener("click", function () { if (pick) return; pick = k; tot++; if (k === order[idx][1]) ok++; draw(); });
      btns.appendChild(b);
    });
    sets.innerHTML = '<span class="nm">' + tex("\\mathbb R") + '</span>' +
      '<div class="set" data-s="Q"><span class="nm">' + tex("\\mathbb Q") + '</span><div class="set" data-s="Z"><span class="nm">' + tex("\\mathbb Z") + '</span>' +
      '<div class="set" data-s="N"><span class="nm">' + tex("\\mathbb N") + '</span><div class="ex">' + ["0", "1", "7", "12"].map(function (x) { return tex(x); }).join("") + "</div></div>" +
      '<div class="ex">' + ["-3", "-14", "-18"].map(function (x) { return tex(x); }).join("") + "</div></div>" +
      '<div class="ex">' + ["\\tfrac23", "-\\tfrac15", "\\tfrac{7}{4}"].map(function (x) { return tex(x); }).join("") + "</div></div>" +
      '<div class="set" data-s="I"><span class="nm">' + tex("\\mathbb I") + '</span><div class="ex">' + ["\\pi", "\\sqrt2", "\\sqrt[3]5", "\\phi"].map(function (x) { return tex(x); }).join("") + "</div></div>";
    function next() {
      if (idx >= order.length - 1) { order = shuffle(POOL.slice()); idx = -1; }
      idx++; pick = null; draw();
    }
    function draw() {
      var it = order[idx];
      $(w, "num").innerHTML = tex(loc(it[0]), true);
      [].forEach.call(btns.children, function (b) {
        b.classList.toggle("right", !!pick && b.dataset.k === it[1]);
        b.classList.toggle("wrong", !!pick && b.dataset.k === pick && pick !== it[1]);
      });
      [].forEach.call(sets.querySelectorAll(".set"), function (s) { s.classList.toggle("on", !!pick && s.dataset.s === it[1]); });
      fb.innerHTML = pick ? "<strong>" + (pick === it[1] ? "✓ " + u("right") : "✗ " + t3("El menor conjunt és ", "El menor conjunto es ", "The smallest set is ") + tex(SYM[it[1]]) + ".") + "</strong> " + rt(it[2][lang]) : t3("Quin és el menor conjunt?", "¿Cuál es el menor conjunto?", "Which is the smallest set?");
      $(w, "next").textContent = t3("Un altre nombre", "Otro número", "Another number") + " →";
      $(w, "score").textContent = tot ? u("score") + ": " + ok + " / " + tot : "";
    }
    $(w, "next").addEventListener("click", next);
    order = shuffle(POOL.slice()); idx = 0;
    onLang(draw);
  }

  /* ---------- 1.1 fracció generatriu ---------- */
  function wGen() {
    var w = document.getElementById("w-gen"); if (!w) return;
    var info = w.querySelector(".info");
    function draw() {
      var E = $(w, "e").value.trim().replace("−", "-"), A = $(w, "a").value.trim(), P = $(w, "p").value.trim();
      [["e", /^-?\d{1,6}$/.test(E)], ["a", /^\d{0,5}$/.test(A)], ["p", /^\d{0,5}$/.test(P)]].forEach(function (c) { $(w, c[0]).classList.toggle("bad", !c[1]); });
      if (!/^-?\d{1,6}$/.test(E) || !/^\d{0,5}$/.test(A) || !/^\d{0,5}$/.test(P)) { info.innerHTML = t3("Escriu només xifres (la part entera pot ser negativa).", "Escribe solo cifras (la parte entera puede ser negativa).", "Type digits only (the whole part may be negative)."); return; }
      var neg = E.charAt(0) === "-", e = E.replace("-", ""), s = neg ? "-" : "", sep = lang === "en" ? "." : "{,}";
      var shown = s + e + (A || P ? sep : "") + A + (P ? "\\widehat{" + P + "}" : ""), num, den, line;
      if (!P) { num = +(e + A); den = Math.pow(10, A.length); line = "\\dfrac{" + (e + A).replace(/^0+(?=\d)/, "") + "}{" + den + "}"; }
      else {
        var full = +(e + A + P), part = +(e + A); num = full - part; den = +(new Array(P.length + 1).join("9") + new Array(A.length + 1).join("0"));
        line = "\\dfrac{" + full + "-" + part + "}{" + den + "}=\\dfrac{" + num + "}{" + den + "}";
      }
      var g = gcd(num, den) || 1, n2 = num / g, d2 = den / g, fin = d2 === 1 ? s + n2 : s + "\\dfrac{" + n2 + "}{" + d2 + "}";
      var kind = !P ? t3("decimal exacte", "decimal exacto", "terminating decimal") : A ? t3("periòdic mixt", "periódico mixto", "eventually repeating") : t3("periòdic pur", "periódico puro", "purely repeating");
      var expr = !A && !P ? shown : shown + "=" + s + line + (g > 1 ? "=" + fin : "");
      info.innerHTML = kv([[t3("Tipus", "Tipo", "Type"), !A && !P ? t3("nombre enter", "número entero", "whole number") : kind], [t3("Fracció", "Fracción", "Fraction"), tex(expr)]]);
    }
    ["e", "a", "p"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 1.4 valor absolut ---------- */
  function wAbs() {
    var w = document.getElementById("w-abs"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info");
    function draw() {
      var x = +$(w, "x").value; $(w, "xv").textContent = decS(x, 1).replace("-", "−");
      var W = svgW(svg), L = 22, R = W - 22, lo = -9, hi = 9, y = 50, stp = W < 450 ? 2 : 1;
      svg.setAttribute("viewBox", "0 0 " + W + " 90");
      function X(v) { return L + (v - lo) / (hi - lo) * (R - L); }
      var g = '<line class="ax" x1="' + L + '" x2="' + R + '" y1="' + y + '" y2="' + y + '"/>';
      for (var v = -8; v <= 8; v++) g += '<line class="tk" x1="' + X(v) + '" x2="' + X(v) + '" y1="' + (y - 4) + '" y2="' + (y + 4) + '"/>' + (v % stp ? "" : '<text x="' + X(v) + '" y="' + (y + 20) + '" text-anchor="middle">' + String(v).replace("-", "−") + "</text>");
      g += '<line x1="' + X(0) + '" x2="' + X(x) + '" y1="' + y + '" y2="' + y + '" stroke="' + COL.r + '" stroke-width="5"/>';
      g += '<path d="M' + X(0) + " " + (y - 14) + " V" + (y - 20) + " H" + X(x) + " V" + (y - 14) + '" fill="none" stroke="' + COL.r + '" stroke-width="1.5"/>';
      g += '<text class="lb" x="' + (X(0) + X(x)) / 2 + '" y="' + (y - 26) + '" text-anchor="middle">|x| = ' + decS(Math.abs(x), 1) + "</text>";
      g += '<circle cx="' + X(x) + '" cy="' + y + '" r="6.5" fill="' + COL.a + '"/><circle cx="' + X(0) + '" cy="' + y + '" r="4" fill="var(--text)"/>';
      svg.innerHTML = g;
      var xs = nT(x);
      info.innerHTML = tex(x >= 0 ? "x=" + xs + "\\ge0\\ \\Rightarrow\\ |x|=x=" + xs : "x=" + xs + "\\lt0\\ \\Rightarrow\\ |x|=-x=-(" + xs + ")=" + nT(-x));
    }
    $(w, "x").addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 1.4 entorns i desigualtats ---------- */
  function wEnt() {
    var w = document.getElementById("w-ent"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), op = 0;
    var OPS = ["\\lt", "\\le", "\\gt", "\\ge"];
    presetBtns($(w, "ops"), function () { return OPS.map(function (s) { return tex("|x-a|" + s + " r"); }); }, function (i) { op = i; draw(); }, 0);
    function draw() {
      var a = +$(w, "a").value, r = +$(w, "r").value;
      $(w, "av").textContent = decS(a, 1).replace("-", "−"); $(w, "rv").textContent = decS(r, 1);
      var inside = op < 2, closedInner = op === 1 || op === 2, I = [{ a: a - r, ac: closedInner, b: a + r, bc: closedInner }];
      var W = svgW(svg), S = inside ? I : compl(I), res = nline([{ S: S, c: COL.r }], { range: [-10, 10], W: W });
      res.svg += '<line x1="' + res.X(a) + '" x2="' + res.X(a) + '" y1="16" y2="40" stroke="var(--text)" stroke-width="1.5" stroke-dasharray="3 3"/><circle cx="' + res.X(a) + '" cy="28" r="3.5" fill="var(--text)"/><text class="lb" x="' + res.X(a) + '" y="12" text-anchor="middle">a</text>';
      paint(svg, res, W);
      var xa = a === 0 ? "x" : a > 0 ? "x-" + nT(a) : "x+" + nT(-a), s = OPS[op], o = t3("o", "o", "or");
      var ineq = inside ? nT(a - r) + s + " x" + s + " " + nT(a + r) : "x" + (op === 2 ? "\\lt " : "\\le ") + nT(a - r) + "\\ \\ \\text{" + o + "}\\ \\ x" + s + " " + nT(a + r);
      var rows = [[t3("Desigualtat", "Desigualdad", "Inequality"), tex("|" + xa + "|" + s + " " + nT(r))], [t3("Equival a", "Equivale a", "Same as"), tex(ineq)], [t3("Solució", "Solución", "Solution"), tex("x\\in " + setT(S))]];
      if (op === 0) rows.push(["", t3("És l'entorn ", "Es el entorno ", "It's the neighbourhood ") + tex("B(" + nT(a) + ";\\," + nT(r) + ")") + "."]);
      if (op === 1) rows.push(["", t3("És l'entorn tancat ", "Es el entorno cerrado ", "It's the closed neighbourhood ") + tex("B[" + nT(a) + ";\\," + nT(r) + "]") + "."]);
      if (op > 1) rows.push(["", t3("Són els punts que estan a distància ", "Son los puntos que están a distancia ", "These are the points at distance ") + (op === 2 ? t3("més gran que ", "mayor que ", "greater than ") : t3("més gran o igual que ", "mayor o igual que ", "at least ")) + tex(nT(r)) + t3(" del centre.", " del centro.", " from the centre.")]);
      info.innerHTML = kv(rows);
    }
    ["a", "r"].forEach(function (k) { $(w, k).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 1.2 dibuixos petits de la taula: només els extrems a i b, el tros marcat damunt de la recta ---------- */
  function wMini() {
    document.querySelectorAll("svg.nl-mini[data-iv]").forEach(function (s) {
      var I = parseIv(s.dataset.iv), y = 14, xa = 64, xb = 136, L = 10, R = 186, c = COL.r;
      var x1 = isFinite(I.a) ? xa : L + 4, x2 = isFinite(I.b) ? xb : R - 4;
      // si l'interval és una semirecta, el seu extrem va al centre
      if (!isFinite(I.a) && isFinite(I.b)) x2 = 100;
      if (isFinite(I.a) && !isFinite(I.b)) x1 = 100;
      var g = '<line class="ax" x1="' + L + '" x2="' + R + '" y1="' + y + '" y2="' + y + '"/><path d="M' + (R + 6) + " " + y + ' l-8 -4 v8 z" fill="var(--muted)"/>';
      g += '<line x1="' + x1 + '" x2="' + x2 + '" y1="' + y + '" y2="' + y + '" stroke="' + c + '" stroke-width="4"/>';
      if (!isFinite(I.a)) g += '<path d="M' + (x1 - 6) + " " + y + ' l9 -6 v12 z" fill="' + c + '"/>';
      if (!isFinite(I.b)) g += '<path d="M' + (x2 + 6) + " " + y + ' l-9 -6 v12 z" fill="' + c + '"/>';
      [[I.a, I.ac, x1, "a"], [I.b, I.bc, x2, "b"]].forEach(function (e) {
        if (!isFinite(e[0])) return;
        g += '<circle cx="' + e[2] + '" cy="' + y + '" r="4.5" stroke="' + c + '" stroke-width="2"' + (e[1] ? ' fill="' + c + '"' : ' class="op"') + "/>";
        g += '<text class="ab" x="' + e[2] + '" y="' + (y + 17) + '" text-anchor="middle">' + e[3] + "</text>";
      });
      s.setAttribute("viewBox", "0 0 200 34"); s.innerHTML = g;
    });
  }

  /* ---------- 1.2 constructor d'intervals ---------- */
  function wIb() {
    var w = document.getElementById("w-ib"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), inp = $(w, "in");
    var PRE = ["(-3, 1]", "[4, +inf)", "(-inf, 7/2)", "[-1, 5]", "(-inf, 0]"];
    presetBtns($(w, "pre"), function () { return PRE; }, function (i) { inp.value = PRE[i]; draw(); });
    function name(I) {
      var fa = isFinite(I.a), fb = isFinite(I.b);
      if (!fa && !fb) return t3("Tota la recta real", "Toda la recta real", "The whole number line");
      if (!fa) return t3("Semirecta negativa", "Semirrecta negativa", "Ray to the left") + (I.bc ? t3(" (tancada)", " (cerrada)", " (closed)") : t3(" (oberta)", " (abierta)", " (open)"));
      if (!fb) return t3("Semirecta positiva", "Semirrecta positiva", "Ray to the right") + (I.ac ? t3(" (tancada)", " (cerrada)", " (closed)") : t3(" (oberta)", " (abierta)", " (open)"));
      if (I.ac && I.bc) return t3("Interval tancat", "Intervalo cerrado", "Closed interval");
      if (!I.ac && !I.bc) return t3("Interval obert", "Intervalo abierto", "Open interval");
      return I.ac ? t3("Interval obert per la dreta", "Intervalo abierto por la derecha", "Half-open interval (open on the right)") : t3("Interval obert per l'esquerra", "Intervalo abierto por la izquierda", "Half-open interval (open on the left)");
    }
    function draw() {
      var I = parseIv(inp.value);
      inp.classList.toggle("bad", !I);
      if (!I) { svg.innerHTML = ""; info.innerHTML = t3("No entenc l'interval. Escriu-lo així: ", "No entiendo el intervalo. Escríbelo así: ", "I can't read that interval. Write it like this: ") + "<code>[-2, 5)</code>, <code>(3, +inf)</code>."; return; }
      if (isEmpty(I)) { svg.innerHTML = ""; info.innerHTML = t3("L'extrem esquerre ha de ser menor que el dret: és el conjunt buit ", "El extremo izquierdo tiene que ser menor que el derecho: es el conjunto vacío ", "The left endpoint must be smaller than the right one: it's the empty set ") + tex("\\varnothing") + "."; return; }
      var W = svgW(svg); paint(svg, nline([{ S: [I], c: COL.r }], { W: W }), W);
      var fa = isFinite(I.a), fb = isFinite(I.b), d = (fa ? nT(I.a) + (I.ac ? "\\le " : "\\lt ") : "") + "x" + (fb ? (I.bc ? "\\le " : "\\lt ") + nT(I.b) : "");
      info.innerHTML = kv([[t3("Tipus", "Tipo", "Type"), name(I)], [t3("Interval", "Intervalo", "Interval"), tex(ivT(I))], [t3("Desigualtat", "Desigualdad", "Inequality"), tex(!fa && !fb ? "x\\in\\mathbb R" : "\\{x\\in\\mathbb R : " + d + "\\}")]]);
    }
    inp.addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 1.3 operacions amb intervals ---------- */
  function wOps() {
    var w = document.getElementById("w-ops"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info");
    function draw() {
      var A = parseIv($(w, "A").value), B = parseIv($(w, "B").value);
      $(w, "A").classList.toggle("bad", !A); $(w, "B").classList.toggle("bad", !B);
      if (!A || !B) { svg.innerHTML = ""; info.innerHTML = t3("Revisa ", "Revisa ", "Check ") + (A ? "B" : "A") + t3(": escriu-lo com ", ": escríbelo como ", ": write it like ") + "<code>[1, 3)</code>, <code>(-inf, 2]</code> " + t3("o", "o", "or") + " <code>]2, 5[</code>."; return; }
      var SA = norm([A]), SB = norm([B]);
      var R = [["A∪B", "A\\cup B", cup(SA, SB)], ["A∩B", "A\\cap B", cap(SA, SB)]];
      var rg = range([SA, SB]);
      var W = svgW(svg);
      paint(svg, nline([{ S: SA, c: COL.a, l: "A" }, { S: SB, c: COL.b, l: "B" }].concat(R.map(function (x) { return { S: x[2], c: COL.r, l: x[0] }; })), { range: rg, W: W }), W);
      info.innerHTML = kv(R.map(function (x) { return [tex(x[1]), tex(setT(x[2]))]; }));
    }
    ["A", "B"].forEach(function (k) { $(w, k).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 1.6 simplificació de radicals ---------- */
  function wSimp() {
    var w = document.getElementById("w-simp"); if (!w) return;
    var info = w.querySelector(".info");
    function draw() {
      var a = Math.round(+$(w, "a").value), m = Math.round(+$(w, "m").value), n = Math.round(+$(w, "n").value);
      var ok = { a: a >= 2 && a <= 99, m: m >= 1 && m <= 60, n: n >= 2 && n <= 60 };
      ["a", "m", "n"].forEach(function (k) { $(w, k).classList.toggle("bad", !ok[k]); });
      if (!ok.a || !ok.m || !ok.n) { info.innerHTML = t3("Tria una base entre 2 i 99, un exponent entre 1 i 60 i un índex entre 2 i 60.", "Elige una base entre 2 y 99, un exponente entre 1 y 60 y un índice entre 2 y 60.", "Choose a base from 2 to 99, an exponent from 1 to 60 and an index from 2 to 60."); return; }
      function rad(nn, mm) { var r = mm === 1 ? String(a) : a + "^{" + mm + "}"; return nn === 1 ? r : nn === 2 ? "\\sqrt{" + r + "}" : "\\sqrt[" + nn + "]{" + r + "}"; }
      var g = gcd(m, n), m2 = m / g, n2 = n / g, rows = [];
      rows.push([t3("Radical", "Radical", "Radical"), tex(rad(n, m))]);
      rows.push([t3("Potència", "Potencia", "Power"), tex(a + "^{\\frac{" + m + "}{" + n + "}}" + (g > 1 ? "=" + a + (n2 === 1 ? "^{" + m2 + "}" : "^{\\frac{" + m2 + "}{" + n2 + "}}") : ""))]);
      rows.push([t3("m.c.d.", "m.c.d.", "HCF"), tex("\\text{m.c.d.}(" + m + "," + n + ")=" + g)]);
      var res = rad(n, m) + (g > 1 ? "=" + rad(n2, m2) : "");
      if (n2 === 1) res += "=" + (Math.pow(a, m2) <= 1e9 ? Math.pow(a, m2) : a + "^{" + m2 + "}");
      var note = g === 1 ? t3("L'índex i l'exponent no tenen divisors comuns: el radical ja és irreductible.", "El índice y el exponente no tienen divisores comunes: el radical ya es irreducible.", "The index and the exponent have no common factor: the radical is already in its simplest form.")
        : n2 === 1 ? t3("L'índex divideix l'exponent: l'arrel és exacta.", "El índice divide al exponente: la raíz es exacta.", "The index divides the exponent: the root is exact.")
        : t3("Dividim l'índex i l'exponent entre ", "Dividimos el índice y el exponente entre ", "Divide the index and the exponent by ") + g + ".";
      if (m2 >= n2 && n2 > 1) note += " " + t3("Encara es poden extraure factors (mira l'eina de més avall).", "Todavía se pueden extraer factores (mira la herramienta de más abajo).", "You can still take factors out (see the tool further down).");
      rows.push([t3("Simplificat", "Simplificado", "Simplified"), tex(res) + "<br><small>" + note + "</small>"]);
      info.innerHTML = kv(rows);
    }
    ["a", "m", "n"].forEach(function (k) { $(w, k).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 1.6 extracció de factors ---------- */
  function wExt() {
    var w = document.getElementById("w-ext"); if (!w) return;
    var info = w.querySelector(".info");
    function factor(n) { var f = [], p, e; for (p = 2; p * p <= n; p++) { e = 0; while (n % p === 0) { n /= p; e++; } if (e) f.push([p, e]); } if (n > 1) f.push([n, 1]); return f; }
    function draw() {
      var n = Math.round(+$(w, "n").value), N = Math.round(+$(w, "N").value), okN = n >= 2 && n <= 9, okR = N >= 1 && N <= 99999999;
      $(w, "n").classList.toggle("bad", !okN); $(w, "N").classList.toggle("bad", !okR);
      if (!okN || !okR) { info.innerHTML = t3("Tria un índex entre 2 i 9 i un radicand natural fins a 99 999 999.", "Elige un índice entre 2 y 9 y un radicando natural hasta 99 999 999.", "Choose an index from 2 to 9 and a whole-number radicand up to 99 999 999."); return; }
      var f = factor(N), idx = n === 2 ? "" : "[" + n + "]";
      function pw(p, e) { return e === 1 ? String(p) : p + "^{" + e + "}"; }
      var fact = f.length ? f.map(function (x) { return pw(x[0], x[1]); }).join("\\cdot ") : "1", outF = [], inF = [], split = [], outV = 1, inV = 1;
      f.forEach(function (x) {
        var q = Math.floor(x[1] / n), r = x[1] % n;
        if (q) outF.push(pw(x[0], q)); if (r) inF.push(pw(x[0], r));
        outV *= Math.pow(x[0], q); inV *= Math.pow(x[0], r);
        split.push(x[1] + "=" + q + "\\cdot" + n + "+" + r);
      });
      var res = outF.join("\\cdot ") + (inV > 1 ? "\\sqrt" + idx + "{" + inF.join("\\cdot ") + "}" : "") || "1";
      if (outF.length > 1 || (outF.length && inF.length > 1)) res += "=" + (outV > 1 ? outV : "") + (inV > 1 ? "\\sqrt" + idx + "{" + inV + "}" : "");
      var note = inV === 1 ? t3("És una arrel exacta.", "Es una raíz exacta.", "It's an exact root.") : outV === 1 ? t3("Cap exponent no arriba a l'índex: no se'n pot extraure res.", "Ningún exponente llega al índice: no se puede extraer nada.", "No exponent reaches the index: nothing comes out.") : "";
      info.innerHTML = kv([[t3("Factoritzem", "Factorizamos", "Factorise"), tex("\\sqrt" + idx + "{" + N + "}=\\sqrt" + idx + "{" + fact + "}")],
        [t3("Exponents entre l'índex", "Exponentes entre el índice", "Exponents ÷ index"), tex(split.join(",\\;\\;") || "-")],
        [t3("Resultat", "Resultado", "Result"), tex("\\sqrt" + idx + "{" + N + "}=" + res) + (note ? "<br><small>" + note + "</small>" : "")]]);
    }
    ["n", "N"].forEach(function (k) { $(w, k).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 1.7 racionalització de k / (p + q·√c) ---------- */
  function wRac() {
    var w = document.getElementById("w-rac"); if (!w) return;
    var info = w.querySelector(".info");
    // part quadrada de c: c = s²·r
    function sq(c) { var s = 1, r = c; for (var d = 2; d * d <= r; d++) while (r % (d * d) === 0) { r /= d * d; s *= d; } return [s, r]; }
    // a + b√r en TeX
    function lin(a, b, r) {
      var t = "";
      if (a) t = String(a);
      if (b) { var bt = (Math.abs(b) === 1 ? "" : Math.abs(b)) + "\\sqrt{" + r + "}"; t += (b < 0 ? "-" : t ? "+" : "") + bt; }
      return t || "0";
    }
    function fr(num, den) { // num: TeX, den enter > 0
      return den === 1 ? num : "\\dfrac{" + num + "}{" + den + "}";
    }
    function draw() {
      var k = Math.round(+$(w, "k").value), p = Math.round(+$(w, "p").value), q = Math.round(+$(w, "q").value), c = Math.round(+$(w, "c").value);
      var ok = { k: k !== 0 && Math.abs(k) <= 99, p: Math.abs(p) <= 20, q: q !== 0 && Math.abs(q) <= 20, c: c >= 2 && c <= 99 };
      ["k", "p", "q", "c"].forEach(function (x) { $(w, x).classList.toggle("bad", !ok[x]); });
      if (!ok.k || !ok.p || !ok.q || !ok.c) { info.innerHTML = t3("Tria \\(k\\neq0\\), \\(q\\neq0\\) i \\(c\\) natural entre 2 i 99.", "Elige \\(k\\neq0\\), \\(q\\neq0\\) y \\(c\\) natural entre 2 y 99.", "Choose \\(k\\neq0\\), \\(q\\neq0\\) and a whole number \\(c\\) from 2 to 99.").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }); return; }
      var S = sq(c), s = S[0], r = S[1], rows = [];
      var den0 = lin(p, q, c), start = "\\dfrac{" + k + "}{" + den0 + "}";
      rows.push([t3("Fracció", "Fracción", "Fraction"), tex(start)]);
      if (r === 1) {
        var v = p + q * s, g0 = gcd(k, v) || 1, sg = (k / v < 0 ? "-" : "");
        rows.push(["", t3("Com que ", "Como ", "Since ") + tex("\\sqrt{" + c + "}=" + s) + t3(", no hi ha cap arrel: ", ", no hay ninguna raíz: ", ", there is no root at all: ") + tex(start + "=" + (v === 0 ? "\\text{?}" : sg + fr(String(Math.abs(k / g0)), Math.abs(v / g0))))]);
        if (v === 0) rows[1][1] = t3("El denominador val 0: la fracció no existeix.", "El denominador vale 0: la fracción no existe.", "The denominator is 0: the fraction doesn't exist.");
        info.innerHTML = kv(rows); return;
      }
      var Q = q * s; // denominador = p + Q√r
      if (s > 1) rows.push([t3("Extraiem factors", "Extraemos factores", "Take factors out"), tex("\\sqrt{" + c + "}=" + s + "\\sqrt{" + r + "}\\ \\Rightarrow\\ " + start + "=\\dfrac{" + k + "}{" + lin(p, Q, r) + "}")]);
      var numA, numB, D, mult;
      if (p === 0) { mult = "\\sqrt{" + r + "}"; numA = 0; numB = k; D = Q * r;
        rows.push([t3("Multipliquem per", "Multiplicamos por", "Multiply by"), tex(mult) + " " + t3("(dalt i baix)", "(arriba y abajo)", "(top and bottom)")]);
        rows.push([t3("Queda", "Queda", "We get"), tex("\\dfrac{" + k + "\\sqrt{" + r + "}}{" + lin(0, Q, r) + "\\cdot\\sqrt{" + r + "}}=\\dfrac{" + lin(0, k, r) + "}{" + D + "}")]);
      } else {
        mult = lin(p, -Q, r); numA = k * p; numB = -k * Q; D = p * p - Q * Q * r;
        rows.push([t3("Conjugat", "Conjugado", "Conjugate"), tex(mult)]);
        rows.push([t3("Denominador", "Denominador", "Denominator"), tex("(" + lin(p, Q, r) + ")(" + mult + ")=" + (p < 0 ? "(" + p + ")" : p) + "^2-(" + lin(0, Math.abs(Q), r) + ")^2=" + (p * p) + "-" + (Q * Q * r) + "=" + D)]);
        rows.push([t3("Numerador", "Numerador", "Numerator"), tex(k + "(" + mult + ")=" + lin(numA, numB, r))]);
      }
      if (D === 0) { info.innerHTML = kv(rows.concat([["", t3("El denominador val 0.", "El denominador vale 0.", "The denominator is 0.")]])); return; }
      if (D < 0) { D = -D; numA = -numA; numB = -numB; }
      var g = gcd(gcd(numA, numB), D) || 1; numA /= g; numB /= g; D /= g;
      rows.push([t3("Resultat", "Resultado", "Result"), "<strong>" + tex(start + "=" + fr(lin(numA, numB, r), D)) + "</strong>"]);
      info.innerHTML = kv(rows);
    }
    ["k", "p", "q", "c"].forEach(function (x) { $(w, x).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- 1.8 explorador de logaritmes ---------- */
  function wLog() {
    var w = document.getElementById("w-log"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), bi = 2;
    var B = [{ v: 2, t: "2", l: "\\log_2" }, { v: 3, t: "3", l: "\\log_3" }, { v: 10, t: "10", l: "\\log" }, { v: Math.E, t: "e", l: "\\ln" }, { v: 0.5, t: "\\tfrac12", l: "\\log_{1/2}" }];
    presetBtns($(w, "base"), function () { return B.map(function (b) { return tex("a=" + b.t); }); }, function (i) { bi = i; draw(); }, 2);
    function draw() {
      var b = B[bi], c = +$(w, "c").value, val = Math.pow(b.v, c);
      $(w, "cv").textContent = decS(c, 2).replace("-", "−");
      var exact = Math.abs(val - Math.round(val)) < 1e-9 || !!frac(val), vt = exact ? nT(val) : (lang === "en" ? val.toPrecision(4) : val.toPrecision(4).replace(".", "{,}")), eq = exact ? "=" : "\\approx ";
      var rows = [[t3("Potència", "Potencia", "Power"), tex(b.t + "^{" + nT(c) + "}" + eq + vt)], [t3("Logaritme", "Logaritmo", "Logarithm"), tex(b.l + "\\," + vt + eq + nT(c))]];
      rows.push(["", "<small>" + (b.v < 1 ? t3("Amb base menor que 1 la funció és decreixent: els nombres majors que 1 tenen logaritme negatiu.", "Con base menor que 1 la función es decreciente: los números mayores que 1 tienen logaritmo negativo.", "With a base below 1 the function decreases: numbers greater than 1 have a negative logarithm.") :
        c < 0 ? t3("Si \\(0\\lt b\\lt 1\\) el logaritme és negatiu (amb base major que 1).", "Si \\(0\\lt b\\lt 1\\) el logaritmo es negativo (con base mayor que 1).", "If \\(0\\lt b\\lt 1\\) the logarithm is negative (base greater than 1).").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }) :
        t3("Els nombres majors que 1 tenen logaritme positiu (amb base major que 1).", "Los números mayores que 1 tienen logaritmo positivo (con base mayor que 1).", "Numbers greater than 1 have a positive logarithm (base greater than 1).")) + (val > 16 ? " " + t3("El punt queda fora de la gràfica.", "El punto queda fuera de la gráfica.", "The point is off the graph.") : "") + "</small>"]);
      info.innerHTML = kv(rows);
      var x0 = 34, y0 = 130, sx = (360 - 50) / 16, sy = 26, g = "";
      function X(x) { return x0 + x * sx; } function Y(y) { return y0 - y * sy; }
      for (var v = -4; v <= 4; v++) if (v) g += '<line class="g" x1="' + x0 + '" x2="352" y1="' + Y(v) + '" y2="' + Y(v) + '"/>';
      for (v = 2; v <= 16; v += 2) g += '<line class="g" x1="' + X(v) + '" x2="' + X(v) + '" y1="16" y2="248"/>';
      g += '<line class="ax" x1="' + (x0 - 6) + '" x2="354" y1="' + y0 + '" y2="' + y0 + '"/><line class="ax" x1="' + x0 + '" x2="' + x0 + '" y1="10" y2="252"/>';
      [4, 8, 12, 16].forEach(function (v) { g += '<text x="' + X(v) + '" y="' + (y0 + 14) + '" text-anchor="middle">' + v + "</text>"; });
      [-4, -2, 2, 4].forEach(function (v) { g += '<text x="' + (x0 - 6) + '" y="' + (Y(v) + 3) + '" text-anchor="end">' + String(v).replace("-", "−") + "</text>"; });
      var d = ""; for (var i = 1; i <= 400; i++) { var x = i * 16 / 400, yv = Math.log(x) / Math.log(b.v); if (yv < -4.6 || yv > 4.6) continue; d += (d ? "L" : "M") + X(x).toFixed(1) + " " + Y(yv).toFixed(1); }
      g += '<path d="' + d + '" fill="none" stroke="' + COL.a + '" stroke-width="2.6"/>';
      if (val <= 16) g += '<line x1="' + X(val) + '" x2="' + X(val) + '" y1="' + y0 + '" y2="' + Y(c) + '" stroke="' + COL.b + '" stroke-dasharray="3 3" stroke-width="1.5"/><line x1="' + x0 + '" x2="' + X(val) + '" y1="' + Y(c) + '" y2="' + Y(c) + '" stroke="' + COL.b + '" stroke-dasharray="3 3" stroke-width="1.5"/><circle cx="' + X(val) + '" cy="' + Y(c) + '" r="5.5" fill="' + COL.b + '"/>';
      g += '<text class="lb" x="348" y="26" text-anchor="end">y = ' + (b.t === "10" ? "log x" : b.t === "e" ? "ln x" : "log" + (b.v === 0.5 ? "₁/₂" : b.v === 2 ? "₂" : "₃") + " x") + "</text>";
      svg.innerHTML = g;
    }
    $(w, "c").addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 1.8 canvi de base ---------- */
  function wCb() {
    var w = document.getElementById("w-cb"); if (!w) return;
    var info = w.querySelector(".info");
    function d4(x) { return dT(x, 4); }
    function draw() {
      var a = parseNum($(w, "a").value), b = parseNum($(w, "b").value);
      var okA = isFinite(a) && a > 0 && a !== 1, okB = isFinite(b) && b > 0;
      $(w, "a").classList.toggle("bad", !okA); $(w, "b").classList.toggle("bad", !okB);
      if (!okA || !okB) { info.innerHTML = (!okA ? t3("La base ha de ser positiva i diferent d'1. ", "La base tiene que ser positiva y distinta de 1. ", "The base must be positive and not equal to 1. ") : "") + (!okB ? t3("El nombre ha de ser positiu: el logaritme d'un nombre negatiu o de 0 no existeix.", "El número tiene que ser positivo: el logaritmo de un número negativo o de 0 no existe.", "The number must be positive: the logarithm of a negative number or of 0 doesn't exist.") : ""); return; }
      var at = nT(a), bt = nT(b), v = Math.log(b) / Math.log(a), exact = Math.abs(v - Math.round(v * 12) / 12) < 1e-9;
      var vt = exact ? nT(Math.round(v * 12) / 12) : dT(v, 4), eq = exact ? "=" : "\\approx ";
      info.innerHTML = kv([
        [t3("Amb log", "Con log", "With log"), tex("\\log_{" + at + "}" + bt + "=\\dfrac{\\log " + bt + "}{\\log " + at + "}\\approx\\dfrac{" + d4(Math.log10(b)) + "}{" + d4(Math.log10(a)) + "}")],
        [t3("Amb ln", "Con ln", "With ln"), tex("\\log_{" + at + "}" + bt + "=\\dfrac{\\ln " + bt + "}{\\ln " + at + "}\\approx\\dfrac{" + d4(Math.log(b)) + "}{" + d4(Math.log(a)) + "}")],
        [t3("Resultat", "Resultado", "Result"), "<strong>" + tex("\\log_{" + at + "}" + bt + eq + vt) + "</strong>"],
        [t3("Comprovació", "Comprobación", "Check"), tex(at + "^{" + vt + "}" + (exact ? "=" : "\\approx ") + bt) + "<br><small>" + t3("Les dues maneres donen el mateix: el quocient no depén de la base que fem servir.", "Las dos maneras dan lo mismo: el cociente no depende de la base que usemos.", "Both ways give the same answer: the quotient doesn't depend on the base we use.") + "</small>"]
      ]);
    }
    ["a", "b"].forEach(function (k) { $(w, k).addEventListener("input", draw); });
    onLang(draw);
  }

  /* ---------- autoavaluació ---------- */
  var QUIZ = [
    { q: q3("Quin és el menor conjunt al qual pertany $-\\sqrt{16}$?", "¿Cuál es el menor conjunto al que pertenece $-\\sqrt{16}$?", "What is the smallest set $-\\sqrt{16}$ belongs to?"),
      o: [q3("$\\mathbb N$"), q3("$\\mathbb Z$"), q3("$\\mathbb I$")], a: 1, e: q3("$-\\sqrt{16}=-4$, un enter negatiu.", "$-\\sqrt{16}=-4$, un entero negativo.", "$-\\sqrt{16}=-4$, a negative integer.") },
    { q: q3("Quin d'aquests nombres és irracional?", "¿Cuál de estos números es irracional?", "Which of these numbers is irrational?"),
      o: [q3("$\\sqrt{25}$"), q3("$1{,}\\widehat{3}$", "$1{,}\\widehat{3}$", "$1.\\widehat{3}$"), q3("$\\sqrt{8}$")], a: 2, e: q3("8 no és un quadrat perfecte. En canvi, $\\sqrt{25}=5$ i $1{,}\\widehat3=\\frac43$.", "8 no es un cuadrado perfecto. En cambio, $\\sqrt{25}=5$ y $1{,}\\widehat3=\\frac43$.", "8 isn't a perfect square. On the other hand, $\\sqrt{25}=5$ and $1.\\widehat3=\\frac43$.") },
    { q: q3("Els nombres que compleixen $-2\\lt x\\le 5$ formen l'interval…", "Los números que cumplen $-2\\lt x\\le 5$ forman el intervalo…", "The numbers with $-2\\lt x\\le 5$ form the interval…"),
      o: [q3("$[-2,5)$"), q3("$(-2,5]$"), q3("$(-2,5)$")], a: 1, e: q3("El $-2$ no hi és (parèntesi) i el 5 sí (claudàtor).", "El $-2$ no está (paréntesis) y el 5 sí (corchete).", "$-2$ is not included (round bracket) and 5 is (square bracket).") },
    { q: q3("«$x$ és com a màxim 3» s'escriu…", "«$x$ es como máximo 3» se escribe…", "\"$x$ is at most 3\" is written…"),
      o: [q3("$(-\\infty,3]$"), q3("$(-\\infty,3)$"), q3("$[3,+\\infty)$")], a: 0, e: q3("$x\\le3$: semirecta tancada en el 3.", "$x\\le3$: semirrecta cerrada en el 3.", "$x\\le3$: a ray closed at 3.") },
    { q: q3("$[0,3)\\cap(2,5]=$"), o: [q3("$(2,3)$"), q3("$[0,5]$"), q3("$[2,3]$")], a: 0, e: q3("Els nombres comuns estan entre 2 i 3, i cap dels dos extrems no és dels dos intervals alhora.", "Los números comunes están entre 2 y 3, y ninguno de los dos extremos es de los dos intervalos a la vez.", "The common numbers lie between 2 and 3, and neither endpoint is in both intervals.") },
    { q: q3("$(-\\infty,1]\\cup(0,4)=$"), o: [q3("$(0,1]$"), q3("$(-\\infty,4)$"), q3("$\\mathbb R$")], a: 1, e: q3("Ajuntant-les, tot està pintat fins al 4 (no inclòs).", "Juntándolas, todo está pintado hasta el 4 (no incluido).", "Putting them together, everything is shaded up to 4 (not included).") },
    { q: q3("El conjunt solució de $|x-1|\\le2$ és…", "El conjunto solución de $|x-1|\\le2$ es…", "The solution set of $|x-1|\\le2$ is…"),
      o: [q3("$(-1,3)$"), q3("$[-1,3]$"), q3("$(-\\infty,-1]\\cup[3,+\\infty)$")], a: 1, e: q3("$-2\\le x-1\\le2\\Rightarrow-1\\le x\\le3$.") },
    { q: q3("$|x|\\ge4$ equival a…", "$|x|\\ge4$ equivale a…", "$|x|\\ge4$ means…"),
      o: [q3("$[-4,4]$"), q3("$(-\\infty,-4]\\cup[4,+\\infty)$"), q3("$[4,+\\infty)$")], a: 1, e: q3("Són els nombres a distància 4 o més del zero, a tots dos costats.", "Son los números a distancia 4 o más del cero, a ambos lados.", "They're the numbers at distance 4 or more from zero, on both sides.") },
    { q: q3("$-2^4=$"), o: [q3("$16$"), q3("$-16$"), q3("$-8$")], a: 1, e: q3("L'exponent només afecta el 2: $-(2^4)=-16$.", "El exponente solo afecta al 2: $-(2^4)=-16$.", "The exponent only applies to the 2: $-(2^4)=-16$.") },
    { q: q3("$\\left(\\dfrac23\\right)^{-2}=$"), o: [q3("$-\\dfrac49$"), q3("$\\dfrac94$"), q3("$\\dfrac49$")], a: 1, e: q3("$\\left(\\frac32\\right)^2=\\frac94$: un exponent negatiu inverteix la fracció.", "$\\left(\\frac32\\right)^2=\\frac94$: un exponente negativo invierte la fracción.", "$\\left(\\frac32\\right)^2=\\frac94$: a negative exponent flips the fraction.") },
    { q: q3("Quantes arrels reals té $\\sqrt[4]{-16}$?", "¿Cuántas raíces reales tiene $\\sqrt[4]{-16}$?", "How many real roots does $\\sqrt[4]{-16}$ have?"),
      o: [q3("Cap", "Ninguna", "None"), q3("Una", "Una", "One"), q3("Dues", "Dos", "Two")], a: 0, e: q3("Índex parell i radicand negatiu: cap nombre real elevat a 4 és negatiu.", "Índice par y radicando negativo: ningún número real elevado a 4 es negativo.", "Even index, negative radicand: no real number to the 4th power is negative.") },
    { q: q3("$\\sqrt[5]{a^3}$ en forma de potència és…", "$\\sqrt[5]{a^3}$ en forma de potencia es…", "$\\sqrt[5]{a^3}$ as a power is…"),
      o: [q3("$a^{\\frac53}$"), q3("$a^{\\frac35}$"), q3("$a^{15}$")], a: 1, e: q3("L'exponent va al numerador i l'índex al denominador.", "El exponente va al numerador y el índice al denominador.", "The exponent goes on top and the index underneath.") },
    { q: q3("Simplificat, $\\sqrt[6]{27}=$", "Simplificado, $\\sqrt[6]{27}=$", "Simplified, $\\sqrt[6]{27}=$"),
      o: [q3("$\\sqrt3$"), q3("$\\sqrt[3]{3}$"), q3("$3$")], a: 0, e: q3("$\\sqrt[6]{3^3}=\\sqrt[2]{3^1}$: dividim índex i exponent entre 3.", "$\\sqrt[6]{3^3}=\\sqrt[2]{3^1}$: dividimos índice y exponente entre 3.", "$\\sqrt[6]{3^3}=\\sqrt[2]{3^1}$: divide the index and the exponent by 3.") },
    { q: q3("$\\sqrt8+\\sqrt{18}=$"), o: [q3("$\\sqrt{26}$"), q3("$5\\sqrt2$"), q3("$6\\sqrt2$")], a: 1, e: q3("$2\\sqrt2+3\\sqrt2=5\\sqrt2$. L'arrel no es reparteix en sumes.", "$2\\sqrt2+3\\sqrt2=5\\sqrt2$. La raíz no se reparte en sumas.", "$2\\sqrt2+3\\sqrt2=5\\sqrt2$. A root doesn't split over a sum.") },
    { q: q3("$\\sqrt2\\cdot\\sqrt[3]{2}=$"), o: [q3("$\\sqrt[5]{2}$"), q3("$\\sqrt[6]{4}$"), q3("$\\sqrt[6]{32}$")], a: 2, e: q3("$2^{\\frac12+\\frac13}=2^{\\frac56}=\\sqrt[6]{2^5}$.") },
    { q: q3("$\\dfrac{6}{\\sqrt3}=$"), o: [q3("$2\\sqrt3$"), q3("$3\\sqrt2$"), q3("$\\dfrac{\\sqrt3}{2}$")], a: 0, e: q3("$\\dfrac{6\\sqrt3}{3}=2\\sqrt3$.") },
    { q: q3("$\\dfrac{2}{\\sqrt5-\\sqrt3}=$"), o: [q3("$\\sqrt5+\\sqrt3$"), q3("$\\sqrt5-\\sqrt3$"), q3("$2(\\sqrt5+\\sqrt3)$")], a: 0, e: q3("Pel conjugat: $\\dfrac{2(\\sqrt5+\\sqrt3)}{5-3}=\\sqrt5+\\sqrt3$.", "Por el conjugado: $\\dfrac{2(\\sqrt5+\\sqrt3)}{5-3}=\\sqrt5+\\sqrt3$.", "Using the conjugate: $\\dfrac{2(\\sqrt5+\\sqrt3)}{5-3}=\\sqrt5+\\sqrt3$.") },
    { q: q3("$\\log_2 32=$"), o: [q3("$16$"), q3("$5$"), q3("$\\dfrac15$")], a: 1, e: q3("$2^5=32$.") },
    { q: q3("$\\log_7 1+\\log_7 7=$"), o: [q3("$1$"), q3("$7$"), q3("$0$")], a: 0, e: q3("$\\log_a1=0$ i $\\log_aa=1$.", "$\\log_a1=0$ y $\\log_aa=1$.", "$\\log_a1=0$ and $\\log_aa=1$.") },
    { q: q3("$\\log20+\\log5=$"), o: [q3("$\\log25$"), q3("$2$"), q3("$100$")], a: 1, e: q3("$\\log(20\\cdot5)=\\log100=2$.") },
    { q: q3("Amb la calculadora, $\\log_3 10$ es calcula com…", "Con la calculadora, $\\log_3 10$ se calcula como…", "On a calculator, $\\log_3 10$ is worked out as…"),
      o: [q3("$\\dfrac{\\log3}{\\log10}$"), q3("$\\dfrac{\\log10}{\\log3}$"), q3("$\\log10-\\log3$")], a: 1, e: q3("Canvi de base: $\\dfrac{\\log 10}{\\log3}=\\dfrac{1}{\\log3}\\approx2{,}096$.", "Cambio de base: $\\dfrac{\\log 10}{\\log3}=\\dfrac{1}{\\log3}\\approx2{,}096$.", "Change of base: $\\dfrac{\\log 10}{\\log3}=\\dfrac{1}{\\log3}\\approx2.096$.") }
  ];

  /*@@GENERIC@@*/
  var TITLES = { va: "Nombres reals · FentMates", es: "Números reales · FentMates", en: "Real numbers · FentMates" };
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
    var all = [wChrome, wSteps, wNav, wCls, wGen, wMini, wIb, wOps, wAbs, wEnt, wSimp, wExt, wRac, wLog, wCb, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM1 = { norm: norm, cap: cap, cup: cup, minus: minus, parseIv: parseIv, setT: setT };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
