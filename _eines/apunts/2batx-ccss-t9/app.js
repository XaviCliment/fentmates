(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2batx-u9-done";

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
  function presetBtns(box, labels, onPick) {
    var bs = [];
    labels().forEach(function (_, i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { bs.forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on"); onPick(i); });
      box.appendChild(b); bs.push(b);
    });
    onLang(function () { var L = labels(); bs.forEach(function (b, i) { b.innerHTML = L[i]; }); });
    return bs;
  }

  /* ---------- fraccions exactes ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function Fr(n, d) { if (d === undefined) d = 1; if (d < 0) { n = -n; d = -d; } var g = gcd(n, d) || 1; return { n: n / g, d: d / g }; }
  function fAdd(a, b) { return Fr(a.n * b.d + b.n * a.d, a.d * b.d); }
  function fSub(a, b) { return Fr(a.n * b.d - b.n * a.d, a.d * b.d); }
  function fMul(a, b) { return Fr(a.n * b.n, a.d * b.d); }
  function fDiv(a, b) { return Fr(a.n * b.d, a.d * b.n); }
  function fVal(a) { return a.n / a.d; }
  function fEq(a, b) { return a.n === b.n && a.d === b.d; }
  var F0 = Fr(0), F1 = Fr(1);
  function fSum(arr) { return arr.reduce(fAdd, F0); }
  function fromFloat(x) {
    if (!isFinite(x)) return null;
    var h1 = 1, h0 = 0, k1 = 0, k0 = 1, b = x, i;
    for (i = 0; i < 30; i++) {
      var a = Math.floor(b), h2 = a * h1 + h0, k2 = a * k1 + k0;
      if (k2 > 1e6) break;
      h0 = h1; h1 = h2; k0 = k1; k1 = k2;
      if (Math.abs(x - h1 / k1) < 1e-11) return Fr(h1, k1);
      b = 1 / (b - a); if (!isFinite(b)) break;
    }
    return Math.abs(x - h1 / k1) < 1e-11 ? Fr(h1, k1) : null;
  }
  // llig 0.35, 0,35, 35%, 7/20, 1/4
  function parseP(s) {
    s = String(s || "").trim().replace(/\s+/g, "").replace(/,/g, ".");
    if (!s) return null;
    function dec(t) {
      if (!/^-?\d*\.?\d+$/.test(t) && !/^-?\d+\.?$/.test(t)) return null;
      var k = (t.split(".")[1] || "").length;
      return Fr(Math.round(parseFloat(t) * Math.pow(10, k)), Math.pow(10, k));
    }
    if (/%$/.test(s)) { var p = dec(s.slice(0, -1)); return p ? Fr(p.n, p.d * 100) : null; }
    if (s.indexOf("/") >= 0) { var q = s.split("/"); if (q.length !== 2) return null; var a = dec(q[0]), b = dec(q[1]); return a && b && b.n ? fDiv(a, b) : null; }
    return dec(s);
  }
  function pow10(d) { var e = d; while (e % 2 === 0) e /= 2; while (e % 5 === 0) e /= 5; return e === 1 && d <= 1e6; }
  function decS(x, k) { var s = String(+x.toFixed(k == null ? 4 : k)); return lang === "en" ? s : s.replace(".", ","); }
  function texDec(x, k) { return decS(x, k).replace(",", "{,}"); }
  function texP(f) {
    var x = fVal(f);
    if (pow10(f.d)) return texDec(x, 6);
    if (f.d <= 5000) return (f.n < 0 ? "-" : "") + "\\frac{" + Math.abs(f.n) + "}{" + f.d + "}\\approx " + texDec(x);
    return "\\approx " + texDec(x);
  }
  function texPs(f) { return pow10(f.d) ? texDec(fVal(f), 6) : f.d <= 5000 ? "\\frac{" + f.n + "}{" + f.d + "}" : texDec(fVal(f)); }
  function txtP(f) { return pow10(f.d) ? decS(fVal(f), 4) : f.d <= 999 ? f.n + "/" + f.d : decS(fVal(f), 4); }

  /* ---------- sistemes lineals amb fraccions (regions del diagrama de Venn) ---------- */
  // rows: [{c: [Fr x n], r: Fr}] -> {st: "ok", x} | {st: "under", x, nul} | {st: "bad"}
  function solveLin(rows, n) {
    var M = rows.map(function (q) { return q.c.slice().concat([q.r]); }), piv = [], r = 0, i, j, k;
    for (j = 0; j < n && r < M.length; j++) {
      var p = -1; for (i = r; i < M.length; i++) if (M[i][j].n !== 0) { p = i; break; }
      if (p < 0) continue;
      var t = M[p]; M[p] = M[r]; M[r] = t;
      var pv = M[r][j]; for (k = 0; k <= n; k++) M[r][k] = fDiv(M[r][k], pv);
      for (i = 0; i < M.length; i++) if (i !== r && M[i][j].n !== 0) { var f = M[i][j]; for (k = 0; k <= n; k++) M[i][k] = fSub(M[i][k], fMul(f, M[r][k])); }
      piv.push(j); r++;
    }
    for (i = r; i < M.length; i++) if (M[i][n].n !== 0) return { st: "bad" };
    var x = []; for (j = 0; j < n; j++) x.push(F0);
    piv.forEach(function (c, i) { x[c] = M[i][n]; });
    if (piv.length === n) return { st: "ok", x: x };
    var free = []; for (j = 0; j < n; j++) if (piv.indexOf(j) < 0) free.push(j);
    var nul = free.map(function (fj) {
      var v = []; for (var jj = 0; jj < n; jj++) v.push(F0);
      v[fj] = F1; piv.forEach(function (c, i) { v[c] = fSub(F0, M[i][fj]); });
      return v;
    });
    return { st: "under", x: x, nul: nul };
  }

  /* ---------- quantitats sobre les quatre regions: [només A, A∩B, només B, cap] ---------- */
  var Q = [
    { k: "A", s: "P(A)", t: "P(A)", v: [1, 1, 0, 0] },
    { k: "B", s: "P(B)", t: "P(B)", v: [0, 1, 1, 0] },
    { k: "AB", s: "P(A ∩ B)", t: "P(A\\cap B)", v: [0, 1, 0, 0] },
    { k: "AuB", s: "P(A ∪ B)", t: "P(A\\cup B)", v: [1, 1, 1, 0] },
    { k: "nA", s: "P(Ā)", t: "P(\\overline{A})", v: [0, 0, 1, 1] },
    { k: "nB", s: "P(B̄)", t: "P(\\overline{B})", v: [1, 0, 0, 1] },
    { k: "AnB", s: "P(A ∩ B̄)", t: "P(A\\cap\\overline{B})", v: [1, 0, 0, 0] },
    { k: "nAB", s: "P(Ā ∩ B)", t: "P(\\overline{A}\\cap B)", v: [0, 0, 1, 0] },
    { k: "nAnB", s: "P(Ā ∩ B̄)", t: "P(\\overline{A}\\cap\\overline{B})", v: [0, 0, 0, 1] },
    { k: "nAunB", s: "P(Ā ∪ B̄)", t: "P(\\overline{A}\\cup\\overline{B})", v: [1, 0, 1, 1] },
    { k: "one", s: "", t: "", v: [1, 0, 1, 0] },
    { k: "A|B", s: "P(A | B)", t: "P(A\\,|\\,B)", v: [0, 1, 0, 0], w: [0, 1, 1, 0] },
    { k: "B|A", s: "P(B | A)", t: "P(B\\,|\\,A)", v: [0, 1, 0, 0], w: [1, 1, 0, 0] },
    { k: "A|nB", s: "P(A | B̄)", t: "P(A\\,|\\,\\overline{B})", v: [1, 0, 0, 0], w: [1, 0, 0, 1] },
    { k: "B|nA", s: "P(B | Ā)", t: "P(B\\,|\\,\\overline{A})", v: [0, 0, 1, 0], w: [0, 0, 1, 1] },
    { k: "nA|B", s: "P(Ā | B)", t: "P(\\overline{A}\\,|\\,B)", v: [0, 0, 1, 0], w: [0, 1, 1, 0] },
    { k: "nB|A", s: "P(B̄ | A)", t: "P(\\overline{B}\\,|\\,A)", v: [1, 0, 0, 0], w: [1, 1, 0, 0] },
    { k: "nA|nB", s: "P(Ā | B̄)", t: "P(\\overline{A}\\,|\\,\\overline{B})", v: [0, 0, 0, 1], w: [1, 0, 0, 1] },
    { k: "nB|nA", s: "P(B̄ | Ā)", t: "P(\\overline{B}\\,|\\,\\overline{A})", v: [0, 0, 0, 1], w: [0, 0, 1, 1] },
    { k: "ind", s: "", t: "", ind: true }
  ];
  var QK = {}; Q.forEach(function (q) { QK[q.k] = q; });
  function qS(q) { return q.k === "one" ? t3("P(només un)", "P(solo uno)", "P(exactly one)") : q.k === "ind" ? t3("A i B independents", "A y B independientes", "A and B independent") : q.s; }
  function qT(q) { return q.k === "one" ? "P(\\text{" + t3("només un", "solo uno", "exactly one") + "})" : q.t; }
  function dot(v, x) { return fSum(v.map(function (c, i) { return c ? x[i] : F0; })); }
  function qVal(q, x) { var a = dot(q.v, x); if (!q.w) return a; var b = dot(q.w, x); return b.n === 0 ? null : fDiv(a, b); }

  /* ---------- diagrama de Venn ---------- */
  var VID = 0;
  // o: {on: "123" (regions ombrejades: 1 només A, 2 A∩B, 3 només B, 0 cap), vals: {0:..}, disj, cond}
  function venn(svg, o) {
    var id = svg._vid || (svg._vid = "vn" + (++VID));
    var A = o.disj ? [100, 108, 60] : [128, 108, 72], B = o.disj ? [220, 108, 60] : [192, 108, 72];
    svg.setAttribute("viewBox", "0 0 320 210");
    svg._geo = { A: A, B: B };
    function c(p, extra) { return '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + p[2] + '" ' + (extra || "") + "/>"; }
    var on = o.on || "", h = "<defs>";
    h += '<mask id="' + id + 'mA"><rect x="0" y="0" width="320" height="210" fill="#fff"/>' + c(A, 'fill="#000"') + "</mask>";
    h += '<mask id="' + id + 'mB"><rect x="0" y="0" width="320" height="210" fill="#fff"/>' + c(B, 'fill="#000"') + "</mask>";
    h += '<mask id="' + id + 'mAB"><rect x="0" y="0" width="320" height="210" fill="#fff"/>' + c(A, 'fill="#000"') + c(B, 'fill="#000"') + "</mask>";
    h += '<clipPath id="' + id + 'cB">' + c(B) + "</clipPath></defs>";
    h += '<rect class="omega" x="10" y="10" width="300" height="190" rx="12"/>';
    function st(r) {
      if (o.cond) return r === "2" ? 'style="fill:var(--accent);fill-opacity:.6"' : r === "3" ? 'style="fill:var(--accent-2);fill-opacity:.35"' : "";
      return "";
    }
    function cls(r) { return 'class="reg' + (on.indexOf(r) >= 0 ? " on" : "") + '" ' + st(r); }
    h += '<rect x="10" y="10" width="300" height="190" rx="12" ' + cls("0") + ' mask="url(#' + id + 'mAB)"/>';
    h += c(A, cls("1") + ' mask="url(#' + id + 'mB)"');
    if (!o.disj) h += c(A, cls("2") + ' clip-path="url(#' + id + 'cB)"');
    h += c(B, cls("3") + ' mask="url(#' + id + 'mA)"');
    h += c(A, 'class="set"') + c(B, 'class="set"');
    h += '<text x="' + (A[0] - A[2] * 0.72) + '" y="' + (A[1] - A[2] * 0.78) + '" text-anchor="middle" style="font-size:16px;font-weight:700">A</text>';
    h += '<text x="' + (B[0] + B[2] * 0.72) + '" y="' + (B[1] - B[2] * 0.78) + '" text-anchor="middle" style="font-size:16px;font-weight:700">B</text>';
    h += '<text x="24" y="30" class="sm" style="font-size:14px">E</text>';
    if (o.vals) {
      var pos = o.disj ? { 1: [A[0], A[1] + 5], 3: [B[0], B[1] + 5], 0: [160, 190] } : { 1: [A[0] - 30, A[1] + 5], 2: [160, A[1] + 5], 3: [B[0] + 30, B[1] + 5], 0: [160, 194] };
      Object.keys(pos).forEach(function (r) { if (o.vals[r] != null) h += '<text x="' + pos[r][0] + '" y="' + pos[r][1] + '" text-anchor="middle" class="pb">' + o.vals[r] + "</text>"; });
    }
    svg.innerHTML = h;
  }
  // regió on s'ha fet clic
  function vennHit(svg, ev) {
    var pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
    var m = svg.getScreenCTM(); if (!m) return null;
    var p = pt.matrixTransform(m.inverse()), g = svg._geo;
    if (p.x < 10 || p.x > 310 || p.y < 10 || p.y > 200) return null;
    var inA = Math.hypot(p.x - g.A[0], p.y - g.A[1]) <= g.A[2], inB = Math.hypot(p.x - g.B[0], p.y - g.B[1]) <= g.B[2];
    return inA && inB ? "2" : inA ? "1" : inB ? "3" : "0";
  }
  function sortR(s) { return s.split("").sort().join(""); }
  // les 16 combinacions de regions i com s'escriuen
  function opName(s) {
    var N = {
      "": ["\\varnothing", t3("succés impossible", "suceso imposible", "impossible event")],
      "0": ["\\overline{A}\\cap\\overline{B}=\\overline{A\\cup B}", t3("no ocorre cap dels dos", "no ocurre ninguno de los dos", "neither occurs")],
      "1": ["A\\cap\\overline{B}=A-B", t3("ocorre A però no B (només A)", "ocurre A pero no B (solo A)", "A occurs but not B (only A)")],
      "2": ["A\\cap B", t3("ocorren A i B alhora", "ocurren A y B a la vez", "A and B both occur")],
      "3": ["\\overline{A}\\cap B=B-A", t3("ocorre B però no A (només B)", "ocurre B pero no A (solo B)", "B occurs but not A (only B)")],
      "01": ["\\overline{B}", t3("no ocorre B", "no ocurre B", "B does not occur")],
      "02": ["(A\\cap B)\\cup(\\overline{A}\\cap\\overline{B})", t3("ocorren tots dos o cap", "ocurren los dos o ninguno", "both or neither occur")],
      "03": ["\\overline{A}", t3("no ocorre A", "no ocurre A", "A does not occur")],
      "12": ["A", t3("ocorre A", "ocurre A", "A occurs")],
      "13": ["(A\\cap\\overline{B})\\cup(\\overline{A}\\cap B)", t3("ocorre només un dels dos", "ocurre solo uno de los dos", "exactly one occurs")],
      "23": ["B", t3("ocorre B", "ocurre B", "B occurs")],
      "012": ["A\\cup\\overline{B}", t3("ocorre A o no ocorre B", "ocurre A o no ocurre B", "A occurs or B does not")],
      "013": ["\\overline{A}\\cup\\overline{B}=\\overline{A\\cap B}", t3("no ocorren tots dos alhora (com a molt un)", "no ocurren los dos a la vez (como mucho uno)", "they do not both occur (at most one)")],
      "023": ["\\overline{A}\\cup B", t3("no ocorre A o ocorre B", "no ocurre A u ocurre B", "A does not occur or B occurs")],
      "123": ["A\\cup B", t3("ocorre almenys un dels dos", "ocurre al menos uno de los dos", "at least one occurs")],
      "0123": ["E", t3("succés segur", "suceso seguro", "certain event")]
    };
    return N[sortR(s)];
  }

  /* ---------- figures estàtiques ---------- */
  function wFigs() {
    document.querySelectorAll("[data-venn]").forEach(function (fig) {
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("class", "pr-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Venn");
      fig.insertBefore(svg, fig.firstChild);
      venn(svg, { on: fig.getAttribute("data-venn"), disj: !!fig.getAttribute("data-disj"), cond: !!fig.getAttribute("data-cond") });
    });
    document.querySelectorAll('[data-fig="tree"]').forEach(function (fig) {
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("class", "pr-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Arbre");
      fig.insertBefore(svg, fig.firstChild);
      onLang(function () { drawTree(svg, urnTree([3, 2, 0], 2, false), function () { return false; }); });
    });
  }

  /* ---------- widget: operacions amb successos ---------- */
  function wVenn() {
    var w = document.getElementById("w-venn"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), box = $(w, "ops");
    var OPS = ["123", "2", "03", "01", "1", "3", "0", "013", "13"], cur = "123";
    var bs = OPS.map(function (o) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { cur = o; draw(); }); box.appendChild(b); return b;
    });
    svg.addEventListener("click", function (ev) {
      var r = vennHit(svg, ev); if (r == null) return;
      cur = cur.indexOf(r) >= 0 ? cur.replace(r, "") : sortR(cur + r); draw();
    });
    function draw() {
      bs.forEach(function (b, i) { b.innerHTML = tex(opName(OPS[i])[0].split("=")[0]); b.classList.toggle("on", sortR(OPS[i]) === sortR(cur)); });
      venn(svg, { on: cur });
      var n = opName(cur);
      info.innerHTML = '<p class="big-p">' + tex(n[0]) + "</p><p>" + n[1] + ".</p>" +
        "<p style='color:var(--muted);font-size:.88rem'>" + t3("Fes clic a les regions del diagrama per afegir-les o llevar-les.", "Haz clic en las regiones del diagrama para añadirlas o quitarlas.", "Click the regions of the diagram to add or remove them.") + "</p>";
    }
    onLang(draw);
  }

  /* ---------- widget: llei dels grans nombres ---------- */
  function wFreq() {
    var w = document.getElementById("w-freq"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info");
    var EXP = [
      { p: Fr(1, 2), run: function () { return Math.random() < 0.5; }, l: function () { return t3("Moneda: cara", "Moneda: cara", "Coin: heads"); }, o: function (r) { return r ? t3("cara", "cara", "heads") : t3("creu", "cruz", "tails"); } },
      { p: Fr(1, 6), run: function () { return Math.floor(Math.random() * 6) + 1; }, ok: function (r) { return r === 6; }, l: function () { return t3("Dau: eixir un 6", "Dado: salir un 6", "Die: rolling a 6"); }, o: function (r) { return String(r); } },
      { p: Fr(1, 6), run: function () { return [Math.floor(Math.random() * 6) + 1, Math.floor(Math.random() * 6) + 1]; }, ok: function (r) { return r[0] + r[1] === 7; }, l: function () { return t3("Dos daus: suma 7", "Dos dados: suma 7", "Two dice: sum 7"); }, o: function (r) { return "(" + r[0] + ", " + r[1] + ")"; } },
      { p: Fr(11, 36), run: function () { return [Math.floor(Math.random() * 6) + 1, Math.floor(Math.random() * 6) + 1]; }, ok: function (r) { return r[0] === 6 || r[1] === 6; }, l: function () { return t3("Dos daus: almenys un 6", "Dos dados: al menos un 6", "Two dice: at least one 6"); }, o: function (r) { return "(" + r[0] + ", " + r[1] + ")"; } }
    ];
    var ei = 0, n = 0, nA = 0, hist = [], last = "";
    presetBtns($(w, "presets"), function () { return EXP.map(function (e) { return e.l(); }); }, function (i) { ei = i; clear(); })[0].classList.add("on");
    var RUN = [1, 10, 100, 1000];
    RUN.forEach(function (k) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn primary"; b.textContent = "+" + k;
      b.addEventListener("click", function () { go(k); }); $(w, "run").appendChild(b);
    });
    var rb = document.createElement("button"); rb.type = "button"; rb.className = "btn"; rb.textContent = "↺";
    rb.addEventListener("click", clear); $(w, "run").appendChild(rb);
    function clear() { n = 0; nA = 0; hist = []; last = ""; draw(); }
    function go(k) {
      var e = EXP[ei];
      for (var i = 0; i < k && n < 20000; i++) { var r = e.run(), ok = e.ok ? e.ok(r) : r; n++; if (ok) nA++; hist.push(nA / n); last = e.o(r); }
      draw();
    }
    function draw() {
      var e = EXP[ei], p = fVal(e.p), W = 340, H = 220, x0 = 40, x1 = 330, y0 = 190, y1 = 12;
      var N = Math.max(10, n), Y = function (v) { return y0 - (y0 - y1) * v; }, X = function (i) { return x0 + (x1 - x0) * i / N; };
      var h = "";
      [0, 0.25, 0.5, 0.75, 1].forEach(function (v) { h += '<line x1="' + x0 + '" x2="' + x1 + '" y1="' + Y(v) + '" y2="' + Y(v) + '" style="stroke:var(--border)"/><text x="' + (x0 - 6) + '" y="' + (Y(v) + 4) + '" text-anchor="end" class="sm">' + decS(v, 2) + "</text>"; });
      h += '<line x1="' + x0 + '" x2="' + x1 + '" y1="' + Y(p) + '" y2="' + Y(p) + '" style="stroke:var(--accent-2);stroke-width:2;stroke-dasharray:6 4"/>';
      if (hist.length) {
        var step = Math.max(1, Math.floor(hist.length / 400)), pts = [];
        for (var i = 0; i < hist.length; i += step) pts.push(X(i + 1).toFixed(1) + "," + Y(hist[i]).toFixed(1));
        pts.push(X(hist.length).toFixed(1) + "," + Y(hist[hist.length - 1]).toFixed(1));
        h += '<polyline points="' + pts.join(" ") + '" style="fill:none;stroke:var(--accent);stroke-width:2"/>';
      }
      h += '<text x="' + x1 + '" y="' + (H - 8) + '" text-anchor="end" class="sm">n = ' + n + "</text>";
      svg.innerHTML = h;
      var fr = n ? nA / n : 0;
      info.innerHTML = "<div class='kvs'><span>" + t3("Repeticions", "Repeticiones", "Trials") + "</span><b>" + n + "</b><span>" + t3("Vegades que ocorre", "Veces que ocurre", "Times it occurs") + "</span><b>" + nA + "</b>" +
        "<span>" + t3("Últim resultat", "Último resultado", "Last outcome") + "</span><b>" + (last || "—") + "</b></div>" +
        (n ? "<p>" + tex("f_r=\\dfrac{" + nA + "}{" + n + "}\\approx " + texDec(fr)) + "</p>" : "") + "<p>" + tex("P=" + texP(e.p)) + "</p>" +
        (n >= 1000 ? "<p class='chk ok'>" + t3("Diferència: ", "Diferencia: ", "Difference: ") + decS(Math.abs(fr - p), 4) + "</p>" : "<p style='color:var(--muted);font-size:.88rem'>" + t3("Prova amb +1000 unes quantes vegades.", "Prueba con +1000 unas cuantas veces.", "Try +1000 a few times.") + "</p>");
    }
    onLang(draw);
  }

  /* ---------- widget: Laplace amb dos daus ---------- */
  function wDice() {
    var w = document.getElementById("w-dice"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), box = $(w, "ops");
    var EV = [
      { f: function (a, b) { return a + b === 7; }, l: function () { return t3("Suma 7", "Suma 7", "Sum 7"); } },
      { f: function (a, b) { return a + b >= 10; }, l: function () { return t3("Suma ≥ 10", "Suma ≥ 10", "Sum ≥ 10"); } },
      { f: function (a, b) { return a === b; }, l: function () { return t3("Dobles", "Dobles", "Doubles"); } },
      { f: function (a, b) { return a === 6 || b === 6; }, l: function () { return t3("Almenys un 6", "Al menos un 6", "At least one 6"); } },
      { f: function (a, b) { return a * b % 2 === 0; }, l: function () { return t3("Producte parell", "Producto par", "Even product"); } },
      { f: function (a, b) { return Math.abs(a - b) === 1; }, l: function () { return t3("Diferència 1", "Diferencia 1", "Difference 1"); } },
      { f: function (a, b) { return a + b === 8 || a === b; }, l: function () { return t3("Suma 8 o dobles", "Suma 8 o dobles", "Sum 8 or doubles"); } }
    ];
    var cur = 0;
    var bs = presetBtns(box, function () { return EV.map(function (e) { return e.l(); }); }, function (i) { cur = i; draw(); });
    bs[0].classList.add("on");
    function draw() {
      var e = EV[cur], h = "", c = 40, x0 = 50, y0 = 50, k = 0, list = [];
      for (var i = 1; i <= 6; i++) {
        h += '<text x="' + (x0 + (i - 0.5) * c) + '" y="' + (y0 - 10) + '" text-anchor="middle" class="sm">' + i + "</text>";
        h += '<text x="' + (x0 - 12) + '" y="' + (y0 + (i - 0.5) * c + 4) + '" text-anchor="middle" class="sm">' + i + "</text>";
      }
      h += '<text x="' + (x0 + 3 * c) + '" y="18" text-anchor="middle" class="sm">' + t3("2n dau", "2.º dado", "2nd die") + "</text>";
      h += '<text x="14" y="' + (y0 + 3 * c) + '" text-anchor="middle" class="sm" transform="rotate(-90 14 ' + (y0 + 3 * c) + ')">' + t3("1r dau", "1.er dado", "1st die") + "</text>";
      for (var a = 1; a <= 6; a++) for (var b = 1; b <= 6; b++) {
        var on = e.f(a, b); if (on) { k++; list.push("(" + a + "," + b + ")"); }
        h += '<rect class="cell' + (on ? " on" : "") + '" x="' + (x0 + (b - 1) * c) + '" y="' + (y0 + (a - 1) * c) + '" width="' + c + '" height="' + c + '"/>';
        h += '<text x="' + (x0 + (b - 0.5) * c) + '" y="' + (y0 + (a - 0.5) * c + 4) + '" text-anchor="middle" class="sm">' + a + "," + b + "</text>";
      }
      svg.innerHTML = h;
      var p = Fr(k, 36);
      info.innerHTML = "<p><b>" + e.l() + "</b></p><p>" + t3("Casos favorables: ", "Casos favorables: ", "Favourable outcomes: ") + "<b>" + k + "</b> " + t3("de", "de", "out of") + " 36</p>" +
        "<p style='font-size:.85rem'>" + list.join(" ") + "</p><p class='big-p'>" + tex("P=\\dfrac{" + k + "}{36}" + (p.d !== 36 ? "=" + texPs(p) : "") + "\\approx " + texDec(fVal(p))) + "</p>";
    }
    onLang(draw);
  }

  /* ---------- widget: fórmules amb el Venn ---------- */
  function wProps() {
    var w = document.getElementById("w-props"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), ra = $(w, "a"), rb = $(w, "b"), ri = $(w, "i");
    [ra, rb, ri].forEach(function (r) { r.min = 0; r.max = 100; r.step = 1; r.className = "wide"; });
    ra.value = 60; rb.value = 50; ri.value = 40;
    [ra, rb, ri].forEach(function (r) { r.addEventListener("input", function () { fix(r); draw(); }); });
    function fix(src) {
      var a = +ra.value, b = +rb.value, i = +ri.value, lo = Math.max(0, a + b - 100), hi = Math.min(a, b);
      if (i < lo || i > hi) {
        if (src === ri) ri.value = Math.min(hi, Math.max(lo, i));
        else ri.value = Math.min(hi, Math.max(lo, i));
      }
    }
    function draw() {
      var a = Fr(+ra.value, 100), b = Fr(+rb.value, 100), i = Fr(+ri.value, 100);
      $(w, "av").textContent = decS(fVal(a), 2); $(w, "bv").textContent = decS(fVal(b), 2); $(w, "iv").textContent = decS(fVal(i), 2);
      var r1 = fSub(a, i), r3 = fSub(b, i), un = fAdd(r1, b), r0 = fSub(F1, un);
      venn(svg, { on: "", vals: { 1: decS(fVal(r1), 2), 2: decS(fVal(i), 2), 3: decS(fVal(r3), 2), 0: decS(fVal(r0), 2) } });
      function L(l, r) { return "<p>" + tex(l + "=" + r) + "</p>"; }
      var d = function (f) { return texDec(fVal(f), 2); };
      var h = "<h4>" + t3("Fórmules", "Fórmulas", "Formulas") + "</h4>";
      h += L("P(A\\cup B)", d(a) + "+" + d(b) + "-" + d(i) + "=" + d(un));
      h += L("P(\\overline{A})", "1-" + d(a) + "=" + d(fSub(F1, a)));
      h += L("P(A\\cap\\overline{B})", d(a) + "-" + d(i) + "=" + d(r1));
      h += L("P(\\overline{A}\\cap B)", d(b) + "-" + d(i) + "=" + d(r3));
      h += L("P(\\overline{A}\\cap\\overline{B})", "1-P(A\\cup B)=" + d(r0));
      h += L("P(\\overline{A}\\cup\\overline{B})", "1-P(A\\cap B)=" + d(fSub(F1, i)));
      h += L("P(\\text{" + t3("només un", "solo uno", "exactly one") + "})", d(un) + "-" + d(i) + "=" + d(fSub(un, i)));
      var ind = fEq(fMul(a, b), i);
      h += "<p>" + (i.n === 0 ? "<span class='chk ok'>" + t3("Incompatibles", "Incompatibles", "Mutually exclusive") + "</span> " : "") +
        "<span class='chk " + (ind ? "ok" : "no") + "'>" + tex("P(A)P(B)=" + texDec(fVal(fMul(a, b)), 4)) + " " + (ind ? "=" : "≠") + " " + tex("P(A\\cap B)") + "</span></p>";
      info.innerHTML = h;
    }
    onLang(draw);
  }

  /* ---------- widget: taula de contingència ---------- */
  // cel·les: 0 A∩B̄ (r1), 1 A∩B (r2), 2 Ā∩B (r3), 3 Ā∩B̄ (r0); marges: A, Ā, B, B̄, total
  var CELLS = [
    { k: "AB", v: [0, 1, 0, 0], r: 0, c: 0 }, { k: "AnB", v: [1, 0, 0, 0], r: 0, c: 1 }, { k: "A", v: [1, 1, 0, 0], r: 0, c: 2 },
    { k: "nAB", v: [0, 0, 1, 0], r: 1, c: 0 }, { k: "nAnB", v: [0, 0, 0, 1], r: 1, c: 1 }, { k: "nA", v: [0, 0, 1, 1], r: 1, c: 2 },
    { k: "B", v: [0, 1, 1, 0], r: 2, c: 0 }, { k: "nB", v: [1, 0, 0, 1], r: 2, c: 1 }, { k: "T", v: [1, 1, 1, 1], r: 2, c: 2 }
  ];
  function wTaula() {
    var w = document.getElementById("w-taula"); if (!w) return;
    var tbl = $(w, "tbl"), info = w.querySelector(".info"), opsBox = $(w, "ops");
    var PRE = [
      { d: { A: "50", B: "70", AB: "30", T: "100" }, n: function () { return t3("A = aprova Història, B = aprova Matemàtiques (%)", "A = aprueba Historia, B = aprueba Matemáticas (%)", "A = passes History, B = passes Maths (%)"); }, l: function () { return t3("Història i Mates", "Historia y Mates", "History and Maths"); } },
      { d: { A: "45", AB: "27", nAnB: "38.5", T: "100" }, n: function () { return t3("A = home, B = llig premsa esportiva (%)", "A = hombre, B = lee prensa deportiva (%)", "A = man, B = reads sports papers (%)"); }, l: function () { return t3("Homes i premsa", "Hombres y prensa", "Men and papers"); } },
      { d: { A: "12", B: "16", nAnB: "4", T: "24" }, n: function () { return t3("24 alumnes. A = aprova anglés, B = aprova matemàtiques", "24 alumnos. A = aprueba inglés, B = aprueba matemáticas", "24 students. A = passes English, B = passes Maths"); }, l: function () { return t3("Classe de 24", "Clase de 24", "Class of 24"); } },
      { d: { A: "90", B: "40", nAnB: "3", T: "100" }, n: function () { return t3("A = té vehicle, B = usa transport públic (%)", "A = tiene vehículo, B = usa transporte público (%)", "A = owns a vehicle, B = uses public transport (%)"); }, l: function () { return t3("Vehicle i transport", "Vehículo y transporte", "Vehicle and transport"); } }
    ];
    var inputs = {}, pi = 0, sel = 0, X = null;
    function build() {
      var h = "<thead><tr><th></th><th>B</th><th>B̄</th><th class='tot'>Total</th></tr></thead><tbody>";
      ["A", "Ā", "Total"].forEach(function (rl, r) {
        h += "<tr><th" + (r === 2 ? " class='tot'" : "") + ">" + rl + "</th>";
        CELLS.filter(function (c) { return c.r === r; }).forEach(function (c) { h += "<td data-k='" + c.k + "'><input class='tin' type='text' autocomplete='off' data-k='" + c.k + "'></td>"; });
        h += "</tr>";
      });
      tbl.innerHTML = h + "</tbody>";
      tbl.querySelectorAll("input").forEach(function (i) { inputs[i.dataset.k] = i; i.addEventListener("input", function () { i.dataset.user = i.value.trim() ? "1" : ""; solve(); }); });
    }
    function load(i) { pi = i; CELLS.forEach(function (c) { var v = PRE[i].d[c.k] || ""; inputs[c.k].value = v; inputs[c.k].dataset.user = v ? "1" : ""; }); solve(); }
    var OPS = ["AB", "AuB", "AnB", "nAB", "one", "nAnB", "A|B", "B|A", "A|nB", "B|nA"];
    var obs = OPS.map(function (k, i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { sel = i; show(); }); opsBox.appendChild(b); return b;
    });
    function solve() {
      var rows = [], bad = false;
      CELLS.forEach(function (c) {
        var inp = inputs[c.k];
        if (inp.dataset.user) { var v = parseP(inp.value); if (!v) { inp.classList.add("bad"); bad = true; return; } inp.classList.remove("bad"); rows.push({ c: c.v.map(function (x) { return Fr(x); }), r: v }); }
        else inp.classList.remove("bad");
      });
      X = null;
      if (!inputs.T.dataset.user) { msg(t3("Escriu el total (100 si són percentatges).", "Escribe el total (100 si son porcentajes).", "Type the total (100 for percentages).")); return; }
      if (bad) { msg(t3("Hi ha alguna dada que no entenc.", "Hay algún dato que no entiendo.", "I can't read one of the values.")); return; }
      var s = solveLin(rows, 4);
      if (s.st === "bad") { msg(t3("Les dades són contradictòries.", "Los datos son contradictorios.", "The data contradict each other.")); fill(null); return; }
      if (s.st === "under") { msg(t3("Encara falten dades: n'hi ha prou amb tres de ben triades (a més del total).", "Todavía faltan datos: bastan tres bien elegidos (además del total).", "More data needed: three well-chosen values (plus the total) are enough.")); fill(null); return; }
      if (s.x.some(function (f) { return f.n < 0; })) { msg(t3("Amb aquestes dades alguna cel·la seria negativa: són impossibles.", "Con estos datos alguna celda sería negativa: son imposibles.", "With these data some cell would be negative: they are impossible.")); fill(null); return; }
      X = s.x; fill(X); show();
    }
    function fill(x) {
      CELLS.forEach(function (c) { var inp = inputs[c.k]; if (!inp.dataset.user) inp.value = x ? txtN(dot(c.v, x)) : ""; inp.style.fontWeight = inp.dataset.user ? "700" : "400"; });
    }
    function txtN(f) { return pow10(f.d) ? decS(fVal(f), 4) : f.n + "/" + f.d; }
    function msg(m) { info.innerHTML = "<p>" + PRE[pi].n() + "</p><p class='chk no'>" + m + "</p>"; tbl.querySelectorAll("td").forEach(function (td) { td.classList.remove("on", "on2"); }); }
    function show() {
      obs.forEach(function (b, i) { b.innerHTML = tex(qT(QK[OPS[i]])); b.classList.toggle("on", i === sel); });
      if (!X) return;
      var q = QK[OPS[sel]], T = dot([1, 1, 1, 1], X), num = dot(q.v, X), den = q.w ? dot(q.w, X) : T;
      tbl.querySelectorAll("td").forEach(function (td) { td.classList.remove("on", "on2"); });
      var inner = { AB: 1, AnB: 0, nAB: 2, nAnB: 3 };
      Object.keys(inner).forEach(function (k) {
        var td = tbl.querySelector("td[data-k='" + k + "']");
        if (q.v[inner[k]]) td.classList.add("on"); else if (q.w && q.w[inner[k]]) td.classList.add("on2");
      });
      var h = "<p>" + PRE[pi].n() + "</p>";
      if (den.n === 0) { info.innerHTML = h + "<p>" + t3("La condició té probabilitat 0.", "La condición tiene probabilidad 0.", "The condition has probability 0.") + "</p>"; return; }
      var p = fDiv(num, den);
      h += "<p class='big-p'>" + tex(qT(q) + "=\\dfrac{" + txtN(num) + "}{" + txtN(den) + "}=" + texP(p)) + "</p>";
      h += "<p style='font-size:.88rem;color:var(--muted)'>" + (q.w ? t3("Cel·les grogues: el succés dins de la condició. Denominador: tota la condició (grogues + verdes).", "Celdas amarillas: el suceso dentro de la condición. Denominador: toda la condición (amarillas + verdes).", "Orange cells: the event within the condition. Denominator: the whole condition (orange + green).")
        : t3("Sumem les cel·les marcades i dividim pel total.", "Sumamos las celdas marcadas y dividimos entre el total.", "Add the marked cells and divide by the total.")) + "</p>";
      var pa = fDiv(dot([1, 1, 0, 0], X), T), pb = fDiv(dot([0, 1, 1, 0], X), T), pab = fDiv(X[1], T);
      var ind = fEq(fMul(pa, pb), pab);
      h += "<p><span class='chk " + (ind ? "ok" : "no") + "'>" + (ind ? t3("A i B són independents", "A y B son independientes", "A and B are independent") : t3("A i B són dependents", "A y B son dependientes", "A and B are dependent")) + "</span></p>";
      info.innerHTML = h;
    }
    build();
    presetBtns($(w, "presets"), function () { return PRE.map(function (p) { return p.l(); }); }, load)[0].classList.add("on");
    load(0);
    onLang(function () { if (X) show(); else solve(); });
  }

  /* ---------- widget: la condició redueix l'espai mostral ---------- */
  function wCond() {
    var w = document.getElementById("w-cond"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), se = $(w, "ev"), sc = $(w, "cd");
    var pop = [], i;
    for (i = 0; i < 45; i++) pop.push({ F: 1, B: 0 });
    for (i = 0; i < 15; i++) pop.push({ F: 1, B: 1 });
    for (i = 0; i < 25; i++) pop.push({ F: 0, B: 1 });
    for (i = 0; i < 15; i++) pop.push({ F: 0, B: 0 });
    var EV = [{ s: "F", f: function (p) { return p.F; } }, { s: "B", f: function (p) { return p.B; } }, { s: "F̄", f: function (p) { return !p.F; } }, { s: "B̄", f: function (p) { return !p.B; } }, { s: "F ∩ B", f: function (p) { return p.F && p.B; } }];
    var CD = [{ s: "E", f: function () { return true; } }].concat(EV);
    EV.forEach(function (e, k) { var o = document.createElement("option"); o.value = k; o.textContent = e.s; se.appendChild(o); });
    CD.forEach(function (e, k) { var o = document.createElement("option"); o.value = k; o.textContent = e.s; sc.appendChild(o); });
    se.value = 0; sc.value = 2;
    se.addEventListener("change", draw); sc.addEventListener("change", draw);
    function draw() {
      var e = EV[+se.value], c = CD[+sc.value], h = "", nC = 0, nEC = 0, nE = 0;
      pop.forEach(function (p, k) {
        var x = 22 + (k % 10) * 29, y = 18 + Math.floor(k / 10) * 21, inC = c.f(p), inE = e.f(p);
        if (inE) nE++;
        if (inC) nC++; if (inC && inE) nEC++;
        var fill = inC && inE ? "var(--accent)" : inC ? "var(--accent-2)" : "var(--surface)", op = inC ? 1 : 0.35;
        h += '<circle cx="' + x + '" cy="' + y + '" r="9" style="fill:' + fill + ';stroke:var(--border);opacity:' + op + '"/>';
        var lab = (p.F ? "F" : "") + (p.B ? "B" : "");
        if (lab) h += '<text x="' + x + '" y="' + (y + 3.5) + '" text-anchor="middle" style="font-size:8px;font-weight:700;fill:' + (inC ? "#fff" : "var(--muted)") + ';opacity:' + op + '">' + lab + "</text>";
      });
      svg.innerHTML = h;
      var et = e.s.replace("F̄", "\\overline{F}").replace("B̄", "\\overline{B}").replace("∩", "\\cap"), ct = c.s.replace("F̄", "\\overline{F}").replace("B̄", "\\overline{B}").replace("∩", "\\cap");
      var hh;
      if (+sc.value === 0) hh = "<p class='big-p'>" + tex("P(" + et + ")=\\dfrac{" + nE + "}{100}=" + texP(Fr(nE, 100))) + "</p><p>" + t3("Sense condició, l'espai mostral són els 100 alumnes.", "Sin condición, el espacio muestral son los 100 alumnos.", "With no condition, the sample space is all 100 students.") + "</p>";
      else {
        hh = "<p class='big-p'>" + tex("P(" + et + "\\,|\\," + ct + ")=\\dfrac{" + nEC + "}{" + nC + "}=" + texP(Fr(nEC, nC))) + "</p>";
        hh += "<p>" + t3("Només compten els ", "Solo cuentan los ", "Only the ") + nC + t3(" alumnes de la condició (en color); d'ells, ", " alumnos de la condición (en color); de ellos, ", " students in the condition (coloured) count; of them, ") + nEC + t3(" compleixen el succés.", " cumplen el suceso.", " satisfy the event.") + "</p>";
        hh += "<p>" + tex("\\dfrac{P(" + et + "\\cap " + ct + ")}{P(" + ct + ")}=\\dfrac{" + texDec(nEC / 100, 2) + "}{" + texDec(nC / 100, 2) + "}") + "</p>";
        hh += "<p style='color:var(--muted)'>" + t3("Sense la condició: ", "Sin la condición: ", "Without the condition: ") + tex("P(" + et + ")=" + texDec(nE / 100, 2)) + "</p>";
      }
      info.innerHTML = hh;
    }
    onLang(draw);
  }

  /* ---------- widget: independència al quadrat unitat ---------- */
  function wIndep() {
    var w = document.getElementById("w-indep"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), ra = $(w, "a"), rba = $(w, "ba"), rbn = $(w, "bn");
    [ra, rba, rbn].forEach(function (r) { r.min = 0.05; r.max = 0.95; r.step = 0.05; r.className = "wide"; r.addEventListener("input", draw); });
    ra.value = 0.4; rba.value = 0.6; rbn.value = 0.3;
    var bt = document.createElement("button"); bt.type = "button"; bt.className = "btn"; bt.style.marginTop = "6px";
    bt.addEventListener("click", function () { rbn.value = rba.value; draw(); });
    w.querySelector(".lw-wrap > div:last-child").appendChild(bt);
    function draw() {
      var a = +ra.value, ba = +rba.value, bn = +rbn.value, b = a * ba + (1 - a) * bn, ab = a * ba;
      $(w, "av").textContent = decS(a, 2); $(w, "bav").textContent = decS(ba, 2); $(w, "bnv").textContent = decS(bn, 2);
      bt.textContent = t3("Fes-los independents", "Hazlos independientes", "Make them independent");
      var x0 = 40, y0 = 15, S = 220, h = "";
      h += '<rect x="' + x0 + '" y="' + y0 + '" width="' + S + '" height="' + S + '" class="omega"/>';
      h += '<rect x="' + x0 + '" y="' + (y0 + S * (1 - ba)) + '" width="' + (S * a) + '" height="' + (S * ba) + '" style="fill:var(--yellow);opacity:.85"/>';
      h += '<rect x="' + (x0 + S * a) + '" y="' + (y0 + S * (1 - bn)) + '" width="' + (S * (1 - a)) + '" height="' + (S * bn) + '" style="fill:var(--accent-2);opacity:.55"/>';
      h += '<rect x="' + x0 + '" y="' + y0 + '" width="' + (S * a) + '" height="' + S + '" style="fill:none;stroke:var(--accent);stroke-width:3"/>';
      h += '<line x1="' + x0 + '" x2="' + (x0 + S) + '" y1="' + (y0 + S * (1 - b)) + '" y2="' + (y0 + S * (1 - b)) + '" style="stroke:var(--text);stroke-dasharray:5 4"/>';
      h += '<text x="' + (x0 + S * a / 2) + '" y="' + (y0 + S + 16) + '" text-anchor="middle">A</text><text x="' + (x0 + S * a + S * (1 - a) / 2) + '" y="' + (y0 + S + 16) + '" text-anchor="middle">Ā</text>';
      h += '<text x="' + (x0 - 6) + '" y="' + (y0 + S * (1 - b) + 4) + '" text-anchor="end" class="sm">P(B)</text>';
      h += '<text x="' + (x0 + S * a / 2) + '" y="' + (y0 + S * (1 - ba / 2) + 4) + '" text-anchor="middle" style="font-size:11px">A∩B</text>';
      svg.innerHTML = h;
      var ind = Math.abs(ba - bn) < 1e-9;
      info.innerHTML = "<p>" + tex("P(B)=" + texDec(a, 2) + "\\cdot" + texDec(ba, 2) + "+" + texDec(1 - a, 2) + "\\cdot" + texDec(bn, 2) + "=" + texDec(b)) + "</p>" +
        "<p>" + tex("P(A\\cap B)=P(A)\\,P(B\\,|\\,A)=" + texDec(ab)) + "</p><p>" + tex("P(A)\\cdot P(B)=" + texDec(a * b)) + "</p>" +
        "<p><span class='chk " + (ind ? "ok" : "no") + "'>" + (ind ? t3("Independents: saber que ha ocorregut A no canvia la probabilitat de B", "Independientes: saber que ha ocurrido A no cambia la probabilidad de B", "Independent: knowing A occurred does not change the probability of B") : t3("Dependents: ", "Dependientes: ", "Dependent: ") + tex("P(B\\,|\\,A)\\neq P(B)")) + "</span></p>" +
        "<p style='font-size:.88rem;color:var(--muted)'>" + t3("La línia discontínua és P(B). Són independents quan la regió groga i la verda arriben a la mateixa altura.", "La línea discontinua es P(B). Son independientes cuando la región amarilla y la verde llegan a la misma altura.", "The dashed line is P(B). They are independent when the yellow and green regions reach the same height.") + "</p>";
    }
    onLang(draw);
  }

  /* ---------- arbres ---------- */
  var BALL = ["#e2483d", "#2f6fd6", "#2e9e57"];
  // node: {p: Fr (branca), col (color de la bola) o lab (text), kids: []}
  function urnTree(cnt, nd, rep) {
    function rec(c, depth, seq) {
      var tot = c[0] + c[1] + c[2], node = { kids: [], seq: seq };
      if (depth === nd) return node;
      for (var k = 0; k < 3; k++) {
        if (!c[k]) continue;
        var nc = c.slice(); if (!rep) nc[k]--;
        var ch = rec(nc, depth + 1, seq.concat([k])); ch.p = Fr(c[k], tot); ch.col = k; ch.lab = c[k] + "/" + tot;
        node.kids.push(ch);
      }
      return node;
    }
    return rec(cnt, 0, []);
  }
  function leaves(t) { return t.kids.length ? [].concat.apply([], t.kids.map(leaves)) : [t]; }
  function depthOf(t) { return t.kids.length ? 1 + Math.max.apply(null, t.kids.map(depthOf)) : 0; }
  // dibuixa l'arbre; hl(fulla) diu si una fulla és favorable (true) o de la condició (2)
  function drawTree(svg, t, hl) {
    var L = leaves(t), D = depthOf(t), W = 340, H = Math.max(180, L.length * 26 + 16), step = (H - 16) / L.length, cw = (W - 30 - 92) / Math.max(1, D);
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    var h = "", li = 0;
    function lay(n, d, prod) {
      n.x = 16 + d * cw; n.prod = prod;
      if (!n.kids.length) { n.y = 12 + step / 2 + (li++) * step; return; }
      n.kids.forEach(function (k) { lay(k, d + 1, fMul(prod, k.p)); });
      n.y = (n.kids[0].y + n.kids[n.kids.length - 1].y) / 2;
    }
    lay(t, 0, F1);
    function on(n) { return n.kids.length ? n.kids.some(on) : !!hl(n); }
    function paint(n) {
      n.kids.forEach(function (k) {
        var o = on(k);
        h += '<line class="br' + (o ? " on" : "") + '" x1="' + (n.x + 7) + '" y1="' + n.y + '" x2="' + (k.x - 8) + '" y2="' + k.y + '"/>';
        var mx = n.x + 0.55 * (k.x - n.x), my = n.y + 0.55 * (k.y - n.y) + (k.y < n.y - 1 ? -6 : k.y > n.y + 1 ? 13 : -6);
        h += '<text x="' + mx + '" y="' + my + '" text-anchor="middle" class="sm" style="paint-order:stroke;stroke:var(--bg);stroke-width:3px">' + k.lab + "</text>";
        paint(k);
      });
      if (n.col != null) h += '<circle class="ball" cx="' + n.x + '" cy="' + n.y + '" r="7" style="fill:' + BALL[n.col] + '"/>';
      else if (n.name) h += '<text x="' + n.x + '" y="' + (n.y + 4) + '" text-anchor="middle" style="font-size:12px;font-weight:700">' + n.name + "</text>";
      else h += '<circle class="nd" cx="' + n.x + '" cy="' + n.y + '" r="5"/>';
      if (!n.kids.length && n !== t) {
        var v = hl(n);
        h += '<text x="' + (W - 8) + '" y="' + (n.y + 4) + '" text-anchor="end" class="' + (v ? "pb" : "sm") + '"' + (v === 2 ? ' style="fill:var(--accent)"' : "") + ">" + txtP(n.prod) + "</text>";
      }
    }
    paint(t);
    svg.innerHTML = h;
  }

  /* ---------- widget: extraccions d'una urna ---------- */
  function wUrna() {
    var w = document.getElementById("w-urna"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), se = $(w, "ev");
    var inp = [$(w, "nR"), $(w, "nB"), $(w, "nV")], rep = false, nd = 2, evKey = null;
    function seg(box, opts, get, set) {
      var bs = opts.map(function (o, i) {
        var b = document.createElement("button"); b.type = "button"; b.className = "btn";
        b.addEventListener("click", function () { set(i); paint(); draw(); }); box.appendChild(b); return b;
      });
      function paint() { var L = opts.map(function (o) { return o(); }); bs.forEach(function (b, i) { b.textContent = L[i]; b.classList.toggle("on", get() === i); }); }
      onLang(paint);
    }
    seg($(w, "rep"), [function () { return t3("Sense reemplaçament", "Sin reemplazamiento", "Without replacement"); }, function () { return t3("Amb reemplaçament", "Con reemplazamiento", "With replacement"); }], function () { return rep ? 1 : 0; }, function (i) { rep = i === 1; });
    seg($(w, "nd"), [function () { return t3("2 extraccions", "2 extracciones", "2 draws"); }, function () { return t3("3 extraccions", "3 extracciones", "3 draws"); }], function () { return nd - 2; }, function (i) { nd = i + 2; });
    inp.forEach(function (i) { i.addEventListener("input", draw); });
    se.addEventListener("change", function () { evKey = se.value; draw(); });
    function names() {
      return lang === "es" ? [["roja", "rojas"], ["azul", "azules"], ["verde", "verdes"]] : lang === "en" ? [["red", "red"], ["blue", "blue"], ["green", "green"]] : [["roja", "roges"], ["blava", "blaves"], ["verda", "verdes"]];
    }
    function events(cs) {
      var N = names(), E = [];
      cs.forEach(function (c) { E.push({ k: "all" + c, l: t3("Totes ", "Todas ", "All ") + N[c][1], f: function (s) { return s.every(function (x) { return x === c; }); } }); });
      E.push({ k: "same", l: t3("Totes del mateix color", "Todas del mismo color", "All the same colour"), f: function (s) { return s.every(function (x) { return x === s[0]; }); } });
      E.push({ k: "diff", l: t3("Totes de colors diferents", "Todas de colores distintos", "All different colours"), f: function (s) { return s.every(function (x, i) { return s.indexOf(x) === i; }); } });
      cs.forEach(function (c) { E.push({ k: "atl" + c, l: t3("Almenys una ", "Al menos una ", "At least one ") + N[c][0], f: function (s) { return s.indexOf(c) >= 0; } }); });
      cs.forEach(function (c) { E.push({ k: "none" + c, l: t3("Cap ", "Ninguna ", "No ") + N[c][0], f: function (s) { return s.indexOf(c) < 0; } }); });
      cs.forEach(function (c) { E.push({ k: "ex1" + c, l: t3("Exactament una ", "Exactamente una ", "Exactly one ") + N[c][0], f: function (s) { return s.filter(function (x) { return x === c; }).length === 1; } }); });
      cs.forEach(function (c) { E.push({ k: "sec" + c, l: t3("La 2a és ", "La 2.ª es ", "The 2nd is ") + N[c][0], f: function (s) { return s[1] === c; } }); });
      cs.forEach(function (c1) { cs.forEach(function (c2) {
        E.push({ k: "cd" + c1 + c2, l: t3("1a " + N[c1][0] + " sabent que la 2a és " + N[c2][0], "1.ª " + N[c1][0] + " sabiendo que la 2.ª es " + N[c2][0], "1st " + N[c1][0] + " given that the 2nd is " + N[c2][0]),
          f: function (s) { return s[0] === c1 && s[1] === c2; }, g: function (s) { return s[1] === c2; } });
      }); });
      return E;
    }
    function draw() {
      var cnt = inp.map(function (i) { var v = Math.round(+i.value); return isFinite(v) && v >= 0 ? Math.min(v, 12) : 0; });
      var tot = cnt[0] + cnt[1] + cnt[2];
      if (tot < 1 || (!rep && tot < nd)) { info.innerHTML = "<p class='chk no'>" + t3("Hi ha d'haver prou boles a l'urna.", "Tiene que haber suficientes bolas en la urna.", "There must be enough balls in the urn.") + "</p>"; svg.innerHTML = ""; return; }
      var cs = [0, 1, 2].filter(function (c) { return cnt[c] > 0; }), E = events(cs);
      se.innerHTML = ""; E.forEach(function (e) { var o = document.createElement("option"); o.value = e.k; o.textContent = e.l; se.appendChild(o); });
      if (!E.some(function (e) { return e.k === evKey; })) evKey = E[0].k;
      se.value = evKey;
      var e = E.filter(function (x) { return x.k === evKey; })[0], t = urnTree(cnt, nd, rep), L = leaves(t);
      var prod = function (n) { var p = F1, s = n.seq, c = cnt.slice(), T = tot; s.forEach(function (k) { p = fMul(p, Fr(c[k], T)); if (!rep) { c[k]--; T--; } }); return p; };
      drawTree(svg, t, function (n) { return e.f(n.seq) ? true : e.g && e.g(n.seq) ? 2 : false; });
      var fav = L.filter(function (n) { return e.f(n.seq); }), pf = fSum(fav.map(prod));
      var N = names(), h = "<p><b>" + e.l + "</b></p>";
      function path(n) { var c = cnt.slice(), T = tot; return n.seq.map(function (k) { var s = "\\tfrac{" + c[k] + "}{" + T + "}"; if (!rep) { c[k]--; T--; } return s; }).join("\\cdot "); }
      var terms = fav.map(path);
      if (!e.g) {
        h += "<p>" + tex("P=" + (terms.length ? (terms.length > 6 ? terms.slice(0, 5).join("+") + "+\\dots" : terms.join("+")) : "0") + "=" + texP(pf)) + "</p>";
        h += "<p style='font-size:.88rem;color:var(--muted)'>" + fav.length + t3(" camins favorables (en color). Es multiplica al llarg de cada camí i se sumen els camins.", " caminos favorables (en color). Se multiplica a lo largo de cada camino y se suman los caminos.", " favourable paths (coloured). Multiply along each path and add the paths.") + "</p>";
      } else {
        var cond = L.filter(function (n) { return e.g(n.seq); }), pc = fSum(cond.map(prod));
        h += "<p>" + tex("P(\\text{" + t3("2a", "2.ª", "2nd") + "})=" + texP(pc)) + "</p>";
        h += "<p>" + tex("P(\\text{" + t3("1a", "1.ª", "1st") + "}\\cap\\text{" + t3("2a", "2.ª", "2nd") + "})=" + texP(pf)) + "</p>";
        h += "<p class='big-p'>" + tex("P=\\dfrac{" + texPs(pf) + "}{" + texPs(pc) + "}=" + texP(fDiv(pf, pc))) + "</p>";
        h += "<p style='font-size:.88rem;color:var(--muted)'>" + t3("Bayes: camins favorables (blau-verd) dividit entre tots els camins de la condició (taronja + blau-verd).", "Bayes: caminos favorables (azul verdoso) dividido entre todos los caminos de la condición (naranja + azul verdoso).", "Bayes: favourable paths (teal) divided by all the paths in the condition (orange + teal).") + "</p>";
      }
      h += "<p style='font-size:.85rem'>" + (rep ? t3("Amb reemplaçament: la composició no canvia i les extraccions són independents.", "Con reemplazamiento: la composición no cambia y las extracciones son independientes.", "With replacement: the contents never change and the draws are independent.") : t3("Sense reemplaçament: cada extracció canvia la composició de l'urna.", "Sin reemplazamiento: cada extracción cambia la composición de la urna.", "Without replacement: every draw changes the urn's contents.")) + "</p>";
      info.innerHTML = h;
    }
    onLang(draw);
  }

  /* ---------- widget: probabilitat total i Bayes ---------- */
  function wBayes() {
    var w = document.getElementById("w-bayes"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), rowsBox = $(w, "rows");
    var PRE = [
      { r: [["A", "0.25", "0.01"], ["B", "0.30", "0.02"], ["C", "0.45", "0.03"]], l: function () { return t3("Correctors", "Correctores", "Examiners"); }, b: function () { return t3("error", "error", "error"); } },
      { r: [["M", "0.15", "0.92"], ["S", "0.85", "0.04"]], l: function () { return t3("Test mèdic", "Test médico", "Medical test"); }, b: function () { return t3("positiu", "positivo", "positive"); } },
      { r: [["A", "0.25", "0.15"], ["B", "0.40", "0.10"], ["C", "0.35", "0.12"]], l: function () { return t3("Patinets", "Patinetes", "Scooters"); }, b: function () { return t3("avaria", "avería", "breakdown"); } },
      { r: [["I", "1/2", "3/10"], ["II", "1/2", "4/10"]], l: function () { return t3("Dues urnes", "Dos urnas", "Two urns"); }, b: function () { return t3("roja", "roja", "red"); } }
    ];
    var pi = 0, rows = [];
    function load(i) {
      pi = i; rowsBox.innerHTML = ""; rows = [];
      PRE[i].r.forEach(function (r) { addRow(r); });
      draw();
    }
    function addRow(r) {
      var d = document.createElement("div"); d.className = "pc";
      d.innerHTML = '<input class="tin s" type="text" value="' + r[0] + '" style="width:3.4em"> <span>P = </span><input class="tin s" type="text" value="' + r[1] + '" style="width:4.6em"> <span>P(B | ·) = </span><input class="tin s" type="text" value="' + r[2] + '" style="width:4.6em">';
      var ins = d.querySelectorAll("input"); ins.forEach(function (x) { x.addEventListener("input", draw); });
      rowsBox.appendChild(d); rows.push(ins);
    }
    presetBtns($(w, "presets"), function () { return PRE.map(function (p) { return p.l(); }); }, load)[0].classList.add("on");
    function draw() {
      var data = [], bad = false;
      rows.forEach(function (ins) {
        var a = parseP(ins[1].value), b = parseP(ins[2].value);
        [1, 2].forEach(function (k) { var v = parseP(ins[k].value); ins[k].classList.toggle("bad", !v || fVal(v) < 0 || fVal(v) > 1); });
        if (!a || !b || fVal(a) < 0 || fVal(a) > 1 || fVal(b) < 0 || fVal(b) > 1) bad = true;
        data.push({ n: ins[0].value.trim() || "?", a: a, b: b });
      });
      if (bad) { info.innerHTML = "<p class='chk no'>" + t3("Revisa les probabilitats: han de ser nombres entre 0 i 1.", "Revisa las probabilidades: tienen que ser números entre 0 y 1.", "Check the probabilities: they must be numbers between 0 and 1.") + "</p>"; return; }
      var sa = fSum(data.map(function (d) { return d.a; }));
      var t = { kids: data.map(function (d) {
        return { p: d.a, lab: txtP(d.a), name: d.n, kids: [{ p: d.b, lab: txtP(d.b), name: "B", kids: [], fav: true }, { p: fSub(F1, d.b), lab: txtP(fSub(F1, d.b)), name: "B̄", kids: [] }] };
      }) };
      drawTree(svg, t, function (n) { return n.fav; });
      var terms = data.map(function (d) { return fMul(d.a, d.b); }), pb = fSum(terms), bn = PRE[pi].b();
      var h = "";
      if (!fEq(sa, F1)) h += "<p class='chk no'>" + t3("Compte: les probabilitats a priori sumen ", "Cuidado: las probabilidades a priori suman ", "Careful: the priors add up to ") + txtP(sa) + t3(", no 1.", ", no 1.", ", not 1.") + "</p>";
      h += "<h4>" + t3("Probabilitat total", "Probabilidad total", "Total probability") + " (B = " + bn + ")</h4>";
      h += "<p>" + tex("P(B)=" + data.map(function (d) { return texPs(d.a) + "\\cdot" + texPs(d.b); }).join("+") + "=" + texP(pb)) + "</p>";
      if (pb.n === 0) { info.innerHTML = h; return; }
      h += "<h4>Bayes</h4>";
      data.forEach(function (d, i) { h += "<p>" + tex("P(" + d.n + "\\,|\\,B)=\\dfrac{" + texPs(terms[i]) + "}{" + texPs(pb) + "}=" + texP(fDiv(terms[i], pb))) + "</p>"; });
      var best = 0; terms.forEach(function (x, i) { if (fVal(x) > fVal(terms[best])) best = i; });
      h += "<p style='font-size:.88rem;color:var(--muted)'>" + t3("Si ha ocorregut B, la causa més probable és ", "Si ha ocurrido B, la causa más probable es ", "If B has occurred, the most likely cause is ") + "<b>" + data[best].n + "</b>.</p>";
      info.innerHTML = h;
    }
    load(0);
    onLang(draw);
  }

  /* ---------- calculadora de dos successos ---------- */
  function wLab() {
    var w = document.getElementById("w-lab"); if (!w) return;
    var svg = w.querySelector("svg"), out = $(w, "out"), tbl = $(w, "tbl"), box = $(w, "rows");
    var PRE = [
      { r: [["A", "0.6"], ["B", "0.5"], ["AB", "0.4"]], l: function () { return t3("País Basc 2020", "País Vasco 2020", "Basque C. 2020"); } },
      { r: [["A", "0.3"], ["B|A", "0.4"], ["B|nA", "0.6"]], l: function () { return "Madrid 2019"; } },
      { r: [["A", "0.4"], ["B", "0.7"], ["B|A", "0.75"]], l: function () { return t3("Galícia 2020", "Galicia 2020", "Galicia 2020"); } },
      { r: [["AuB", "0.8"], ["nA", "0.5"], ["AB", "0.3"]], l: function () { return t3("Balears 2020", "Baleares 2020", "Balearic Is. 2020"); } },
      { r: [["A", "0.25"], ["B", "0.2"], ["ind", ""]], l: function () { return t3("Independents", "Independientes", "Independent"); } }
    ];
    var rows = [];
    for (var i = 0; i < 3; i++) (function () {
      var d = document.createElement("div"); d.className = "dat-row";
      var s = document.createElement("select"), inp = document.createElement("input");
      inp.className = "tin s"; inp.type = "text"; inp.autocomplete = "off"; inp.style.width = "5em";
      d.appendChild(s); d.appendChild(document.createTextNode(" = ")); d.appendChild(inp); box.appendChild(d);
      s.addEventListener("change", function () { inp.disabled = s.value === "ind"; calc(); }); inp.addEventListener("input", calc);
      rows.push({ s: s, i: inp });
    })();
    function opts() {
      rows.forEach(function (r) {
        var v = r.s.value; r.s.innerHTML = "";
        Q.forEach(function (q) { var o = document.createElement("option"); o.value = q.k; o.textContent = qS(q); r.s.appendChild(o); });
        if (v) r.s.value = v;
      });
    }
    function load(k) { PRE[k].r.forEach(function (p, i) { rows[i].s.value = p[0]; rows[i].i.value = p[1]; rows[i].i.disabled = p[0] === "ind"; }); calc(); }
    presetBtns($(w, "presets"), function () { return PRE.map(function (p) { return p.l(); }); }, load)[0].classList.add("on");
    function err(m) { out.innerHTML = "<p class='chk no'>" + m + "</p>"; tbl.innerHTML = ""; venn(svg, { on: "" }); }
    function calc() {
      var eqs = [{ c: [F1, F1, F1, F1], r: F1 }], ind = false, bad = false;
      rows.forEach(function (r) {
        var q = QK[r.s.value];
        if (q.ind) { ind = true; r.i.classList.remove("bad"); return; }
        var v = parseP(r.i.value);
        if (!v || fVal(v) < 0 || fVal(v) > 1) { r.i.classList.add("bad"); bad = true; return; }
        r.i.classList.remove("bad");
        if (!q.w) eqs.push({ c: q.v.map(function (x) { return Fr(x); }), r: v });
        else eqs.push({ c: q.v.map(function (x, k) { return fSub(Fr(x), fMul(v, Fr(q.w[k]))); }), r: F0 });
      });
      if (bad) return err(t3("Escriu probabilitats entre 0 i 1 (0.35, 35% o 7/20).", "Escribe probabilidades entre 0 y 1 (0.35, 35% o 7/20).", "Type probabilities between 0 and 1 (0.35, 35% or 7/20)."));
      var s = solveLin(eqs, 4), X = null;
      if (s.st === "bad") return err(t3("Les dades són contradictòries.", "Los datos son contradictorios.", "The data contradict each other."));
      if (s.st === "ok") {
        X = s.x;
        if (ind && !fEq(fMul(fAdd(X[0], X[1]), fAdd(X[1], X[2])), X[1])) return err(t3("Amb aquestes dades, A i B no poden ser independents.", "Con estos datos, A y B no pueden ser independientes.", "With these data, A and B cannot be independent."));
      } else if (ind && s.nul.length === 1) {
        // x = p + t·d; independència: (x0+x1)(x1+x2) = x1, equació de segon grau en t
        var p = s.x.map(fVal), d = s.nul[0].map(fVal);
        var pa = p[0] + p[1], da = d[0] + d[1], pb = p[1] + p[2], db = d[1] + d[2];
        var A2 = da * db, B2 = pa * db + pb * da - d[1], C2 = pa * pb - p[1], ts = [];
        if (Math.abs(A2) < 1e-12) { if (Math.abs(B2) > 1e-12) ts.push(-C2 / B2); }
        else { var disc = B2 * B2 - 4 * A2 * C2; if (disc >= -1e-12) { disc = Math.sqrt(Math.max(0, disc)); ts.push((-B2 + disc) / (2 * A2), (-B2 - disc) / (2 * A2)); } }
        var sols = ts.map(function (t) { return p.map(function (v, k) { return v + t * d[k]; }); }).filter(function (x) { return x.every(function (v) { return v > -1e-9 && v < 1 + 1e-9; }); });
        if (!sols.length) return err(t3("Amb aquestes dades, A i B no poden ser independents.", "Con estos datos, A y B no pueden ser independientes.", "With these data, A and B cannot be independent."));
        X = sols[0].map(function (v) { return fromFloat(v) || Fr(Math.round(v * 1e6), 1e6); });
      } else return err(t3("Falten dades: en calen tres d'independents.", "Faltan datos: se necesitan tres independientes.", "Not enough data: three independent ones are needed."));
      if (X.some(function (f) { return f.n < 0; })) return err(t3("Amb aquestes dades alguna regió tindria probabilitat negativa: són impossibles.", "Con estos datos alguna región tendría probabilidad negativa: son imposibles.", "With these data some region would have negative probability: they are impossible."));
      show(X);
    }
    function show(X) {
      venn(svg, { on: "", vals: { 1: txtP(X[0]), 2: txtP(X[1]), 3: txtP(X[2]), 0: txtP(X[3]) } });
      var g = function (v) { return txtP(dot(v, X)); };
      tbl.innerHTML = "<thead><tr><th></th><th>B</th><th>B̄</th><th class='tot'>Total</th></tr></thead><tbody>" +
        "<tr><th>A</th><td>" + txtP(X[1]) + "</td><td>" + txtP(X[0]) + "</td><td class='tot'>" + g([1, 1, 0, 0]) + "</td></tr>" +
        "<tr><th>Ā</th><td>" + txtP(X[2]) + "</td><td>" + txtP(X[3]) + "</td><td class='tot'>" + g([0, 0, 1, 1]) + "</td></tr>" +
        "<tr><th class='tot'>Total</th><td class='tot'>" + g([0, 1, 1, 0]) + "</td><td class='tot'>" + g([1, 0, 0, 1]) + "</td><td class='tot'>1</td></tr></tbody>";
      var h = "<h4>" + t3("Totes les probabilitats", "Todas las probabilidades", "All the probabilities") + "</h4>";
      Q.forEach(function (q) { if (q.ind) return; var v = qVal(q, X); h += "<div>" + tex(qT(q) + "=" + (v ? texP(v) : "\\text{—}")) + "</div>"; });
      var pa = dot([1, 1, 0, 0], X), pb = dot([0, 1, 1, 0], X), ind = fEq(fMul(pa, pb), X[1]);
      h += "<h4>" + t3("Relació entre A i B", "Relación entre A y B", "How A and B are related") + "</h4>";
      h += "<p>" + tex("P(A)\\cdot P(B)=" + texP(fMul(pa, pb)) + (ind ? "=" : "\\neq ") + "P(A\\cap B)") + "</p>";
      h += "<p><span class='chk " + (ind ? "ok" : "no") + "'>" + (ind ? t3("Independents", "Independientes", "Independent") : t3("Dependents", "Dependientes", "Dependent")) + "</span> ";
      h += "<span class='chk " + (X[1].n === 0 ? "ok" : "no") + "'>" + (X[1].n === 0 ? t3("Incompatibles", "Incompatibles", "Mutually exclusive") : t3("Compatibles", "Compatibles", "Compatible")) + "</span></p>";
      out.innerHTML = h;
    }
    onLang(function () { opts(); if (!rows[0].s.dataset.init) { rows[0].s.dataset.init = 1; load(0); } else calc(); });
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("En llançar dues monedes, l'espai mostral té…", "Al lanzar dos monedas, el espacio muestral tiene…", "When tossing two coins, the sample space has…"),
      o: [q3("3 elements", "3 elementos", "3 elements"), q3("4 elements", "4 elementos", "4 elements"), q3("2 elements", "2 elementos", "2 elements")], a: 1,
      e: q3("CC, C+, +C, ++ (cara-creu i creu-cara són resultats diferents).", "CC, C+, +C, ++ (cara-cruz y cruz-cara son resultados distintos).", "HH, HT, TH, TT (heads-tails and tails-heads are different outcomes).") },
    { q: q3("«No ocorre cap dels dos» és…", "«No ocurre ninguno de los dos» es…", "“Neither occurs” is…"),
      o: [q3("$\\overline{A}\\cup\\overline{B}$"), q3("$\\overline{A\\cap B}$"), q3("$\\overline{A}\\cap\\overline{B}$")], a: 2,
      e: q3("Ni A ni B: $\\overline{A}\\cap\\overline{B}=\\overline{A\\cup B}$ (De Morgan).", "Ni A ni B: $\\overline{A}\\cap\\overline{B}=\\overline{A\\cup B}$ (De Morgan).", "Not A and not B: $\\overline{A}\\cap\\overline{B}=\\overline{A\\cup B}$ (De Morgan).") },
    { q: q3("En llançar dos daus, $P(\\text{suma }=7)$ és…", "Al lanzar dos dados, $P(\\text{suma }=7)$ es…", "Rolling two dice, $P(\\text{sum }=7)$ is…"),
      o: [q3("$\\frac{1}{11}$"), q3("$\\frac16$"), q3("$\\frac{7}{36}$")], a: 1,
      e: q3("6 parelles favorables de 36 equiprobables. (Les 11 sumes no són equiprobables!)", "6 parejas favorables de 36 equiprobables. (¡Las 11 sumas no son equiprobables!)", "6 favourable pairs out of 36 equally likely ones. (The 11 sums are not equally likely!)") },
    { q: q3("Si $P(A)=0{,}5$, $P(B)=0{,}4$ i $P(A\\cap B)=0{,}1$, aleshores $P(A\\cup B)$ val…", "Si $P(A)=0{,}5$, $P(B)=0{,}4$ y $P(A\\cap B)=0{,}1$, entonces $P(A\\cup B)$ vale…", "If $P(A)=0.5$, $P(B)=0.4$ and $P(A\\cap B)=0.1$, then $P(A\\cup B)$ is…"),
      o: [q3("$0{,}9$", "$0{,}9$", "$0.9$"), q3("$0{,}8$", "$0{,}8$", "$0.8$"), q3("$0{,}02$", "$0{,}02$", "$0.02$")], a: 1, e: q3("$0{,}5+0{,}4-0{,}1=0{,}8$", "$0{,}5+0{,}4-0{,}1=0{,}8$", "$0.5+0.4-0.1=0.8$") },
    { q: q3("Si $P(A\\cup B)=0{,}85$, quant val $P(\\overline{A}\\cap\\overline{B})$?", "Si $P(A\\cup B)=0{,}85$, ¿cuánto vale $P(\\overline{A}\\cap\\overline{B})$?", "If $P(A\\cup B)=0.85$, what is $P(\\overline{A}\\cap\\overline{B})$?"),
      o: [q3("$0{,}15$", "$0{,}15$", "$0.15$"), q3("$0{,}85$", "$0{,}85$", "$0.85$"), q3("No es pot saber", "No se puede saber", "It can't be known")], a: 0,
      e: q3("De Morgan: $\\overline{A}\\cap\\overline{B}=\\overline{A\\cup B}$, així que $1-0{,}85=0{,}15$.", "De Morgan: $\\overline{A}\\cap\\overline{B}=\\overline{A\\cup B}$, así que $1-0{,}85=0{,}15$.", "De Morgan: $\\overline{A}\\cap\\overline{B}=\\overline{A\\cup B}$, so $1-0.85=0.15$.") },
    { q: q3("«El 30 % dels que fan esport són dones» és…", "«El 30 % de los que hacen deporte son mujeres» es…", "“30% of those who do sport are women” is…"),
      o: [q3("$P(D\\cap E)=0{,}3$"), q3("$P(D\\,|\\,E)=0{,}3$"), q3("$P(E\\,|\\,D)=0{,}3$")], a: 1,
      e: q3("«Dels que fan esport» és la condició: ens restringim a $E$.", "«De los que hacen deporte» es la condición: nos restringimos a $E$.", "“Of those who do sport” is the condition: we restrict to $E$.") },
    { q: q3("$P(A\\cap B)=0{,}2$ i $P(B)=0{,}5$. Aleshores $P(A\\,|\\,B)$ és…", "$P(A\\cap B)=0{,}2$ y $P(B)=0{,}5$. Entonces $P(A\\,|\\,B)$ es…", "$P(A\\cap B)=0.2$ and $P(B)=0.5$. Then $P(A\\,|\\,B)$ is…"),
      o: [q3("$0{,}1$", "$0{,}1$", "$0.1$"), q3("$0{,}4$", "$0{,}4$", "$0.4$"), q3("$0{,}7$", "$0{,}7$", "$0.7$")], a: 1, e: q3("$\\frac{0{,}2}{0{,}5}=0{,}4$", "$\\frac{0{,}2}{0{,}5}=0{,}4$", "$\\frac{0.2}{0.5}=0.4$") },
    { q: q3("$P(A)=0{,}5$, $P(B)=0{,}6$ i $P(A\\cap B)=0{,}3$. Els successos són…", "$P(A)=0{,}5$, $P(B)=0{,}6$ y $P(A\\cap B)=0{,}3$. Los sucesos son…", "$P(A)=0.5$, $P(B)=0.6$ and $P(A\\cap B)=0.3$. The events are…"),
      o: [q3("independents", "independientes", "independent"), q3("incompatibles", "incompatibles", "mutually exclusive"), q3("dependents", "dependientes", "dependent")], a: 0,
      e: q3("$0{,}5\\cdot0{,}6=0{,}3=P(A\\cap B)$.", "$0{,}5\\cdot0{,}6=0{,}3=P(A\\cap B)$.", "$0.5\\cdot0.6=0.3=P(A\\cap B)$.") },
    { q: q3("Dos successos incompatibles amb probabilitats positives…", "Dos sucesos incompatibles con probabilidades positivas…", "Two mutually exclusive events with positive probabilities…"),
      o: [q3("són sempre independents", "son siempre independientes", "are always independent"), q3("mai no són independents", "nunca son independientes", "are never independent"), q3("poden ser-ho o no", "pueden serlo o no", "may or may not be independent")], a: 1,
      e: q3("$P(A\\cap B)=0$, però $P(A)P(B)\\gt0$.", "$P(A\\cap B)=0$, pero $P(A)P(B)\\gt0$.", "$P(A\\cap B)=0$, but $P(A)P(B)\\gt0$.") },
    { q: q3("Una urna té 3 boles roges i 2 blaves. Traiem dues boles sense reemplaçament. $P(\\text{dues roges})$ és…", "Una urna tiene 3 bolas rojas y 2 azules. Sacamos dos bolas sin reemplazamiento. $P(\\text{dos rojas})$ es…", "An urn has 3 red and 2 blue balls. We draw two without replacement. $P(\\text{two red})$ is…"),
      o: [q3("$\\frac{9}{25}$"), q3("$\\frac{3}{10}$"), q3("$\\frac35$")], a: 1, e: q3("$\\frac35\\cdot\\frac24=\\frac{6}{20}=\\frac{3}{10}$. ($\\frac{9}{25}$ seria amb reemplaçament.)", "$\\frac35\\cdot\\frac24=\\frac{6}{20}=\\frac{3}{10}$. ($\\frac{9}{25}$ sería con reemplazamiento.)", "$\\frac35\\cdot\\frac24=\\frac{6}{20}=\\frac{3}{10}$. ($\\frac{9}{25}$ would be with replacement.)") },
    { q: q3("Una fàbrica A fa el 60 % de les peces (2 % defectuoses) i B el 40 % (5 % defectuoses). $P(\\text{defectuosa})$ és…", "Una fábrica A hace el 60 % de las piezas (2 % defectuosas) y B el 40 % (5 % defectuosas). $P(\\text{defectuosa})$ es…", "Factory A makes 60% of the parts (2% faulty) and B 40% (5% faulty). $P(\\text{faulty})$ is…"),
      o: [q3("$0{,}07$", "$0{,}07$", "$0.07$"), q3("$0{,}035$", "$0{,}035$", "$0.035$"), q3("$0{,}032$", "$0{,}032$", "$0.032$")], a: 2,
      e: q3("Probabilitat total: $0{,}6\\cdot0{,}02+0{,}4\\cdot0{,}05=0{,}012+0{,}02=0{,}032$.", "Probabilidad total: $0{,}6\\cdot0{,}02+0{,}4\\cdot0{,}05=0{,}012+0{,}02=0{,}032$.", "Total probability: $0.6\\cdot0.02+0.4\\cdot0.05=0.012+0.02=0.032$.") },
    { q: q3("Amb les dades anteriors, si una peça és defectuosa, la probabilitat que vinga de B és…", "Con los datos anteriores, si una pieza es defectuosa, la probabilidad de que venga de B es…", "With the same data, if a part is faulty, the probability it came from B is…"),
      o: [q3("$0{,}625$", "$0{,}625$", "$0.625$"), q3("$0{,}05$", "$0{,}05$", "$0.05$"), q3("$0{,}4$", "$0{,}4$", "$0.4$")], a: 0,
      e: q3("Bayes: $\\frac{0{,}02}{0{,}032}=0{,}625$.", "Bayes: $\\frac{0{,}02}{0{,}032}=0{,}625$.", "Bayes: $\\frac{0.02}{0.032}=0.625$.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Probabilitat · FentMates", es: "Probabilidad · FentMates", en: "Probability · FentMates" };
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
      document.querySelectorAll(".widget .wt, .widget label, .widget .legend, .widget > p, .widget .dat-row > span").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wFigs, wVenn, wFreq, wDice, wProps, wTaula, wCond, wIndep, wUrna, wBayes, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM9 = { parseP: parseP, solveLin: solveLin, Q: QK, qVal: qVal, Fr: Fr };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
