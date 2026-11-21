(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1batx-ccss-u10-distribucions-done";

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
  function fillSelect(sel, items) {
    var v = sel.value; sel.innerHTML = "";
    items.forEach(function (it) { var o = document.createElement("option"); o.value = it[0]; o.textContent = it[1]; sel.appendChild(o); });
    if (v && items.some(function (it) { return String(it[0]) === v; })) sel.value = v;
  }

  /* ---------- nombres ---------- */
  function decS(x, k) { var s = String(+(+x).toFixed(k == null ? 4 : k)); return lang === "en" ? s : s.replace(".", ","); }
  function td(x, k) { return decS(x, k).replace(",", "{,}"); }
  function f4(x) { var s = (+x).toFixed(4); return lang === "en" ? s : s.replace(".", "{,}"); }
  function num(s) { s = String(s == null ? "" : s).trim().replace(",", "."); if (!s) return NaN; if (/%$/.test(s)) return parseFloat(s) / 100; if (s.indexOf("/") > 0) { var q = s.split("/"); return parseFloat(q[0]) / parseFloat(q[1]); } return /^-?\d*\.?\d+$/.test(s) ? parseFloat(s) : NaN; }
  function r2(z) { return Math.round(z * 100 + (z >= 0 ? 1e-9 : -1e-9)) / 100; }
  function comb(n, k) { if (k < 0 || k > n) return 0; k = Math.min(k, n - k); var c = 1; for (var i = 1; i <= k; i++) c = c * (n - k + i) / i; return Math.round(c); }
  function pmf(n, p, k) { if (k < 0 || k > n) return 0; return comb(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k); }

  /* ---------- taules de la binomial i de la normal (es llegeixen de la pàgina) ---------- */
  var NT = [], BT = {}, PJ = [];
  function readTables() {
    document.querySelectorAll("#tnorm tbody tr").forEach(function (tr) {
      NT[+tr.getAttribute("data-r")] = [].map.call(tr.querySelectorAll("td"), function (c) { return +c.textContent.replace(",", "."); });
    });
    PJ = [].map.call(document.querySelectorAll("#tbin thead tr:nth-child(2) th"), function (th) { var t = th.textContent.trim(); return { l: t, p: t === "1/3" ? 1 / 3 : +t.replace(",", ".") }; });
    document.querySelectorAll("#tbin tbody tr").forEach(function (tr) {
      var n = +tr.getAttribute("data-n"), x = +tr.getAttribute("data-x");
      (BT[n] = BT[n] || [])[x] = [].map.call(tr.querySelectorAll("td"), function (c) { return +c.textContent.replace(",", "."); });
    });
  }
  // P(Z <= z) amb la taula (z arredonit a dues decimals)
  function F(z) {
    z = r2(z);
    if (z < 0) return +(1 - F(-z)).toFixed(4);
    if (z >= 4) return 1;
    var r = Math.floor(z * 10 + 1e-9), c = Math.round(z * 100) - r * 10;
    return NT[r] ? NT[r][c] : 1;
  }
  function cell(z) { z = Math.abs(r2(z)); if (z >= 4) return null; var r = Math.floor(z * 10 + 1e-9); return [r, Math.round(z * 100) - r * 10]; }
  // valor de z de la taula més pròxim a una probabilitat p > 0,5
  function invF(p) {
    var best = null;
    for (var r = 0; r < 40; r++) for (var c = 0; c < 10; c++) {
      var d = Math.abs(NT[r][c] - p);
      if (!best || d < best.d - 1e-12) best = { d: d, r: r, c: c, v: NT[r][c], z: r / 10 + c / 100, tie: false };
      else if (Math.abs(d - best.d) < 1e-12 && NT[r][c] !== best.v) best.tie = { r: r, c: c, v: NT[r][c], z: r / 10 + c / 100 };
    }
    return best;
  }
  function zinv(p) {
    // z amb P(Z <= z) = p (pren el valor de la taula més pròxim; si n'hi ha dos d'igual de pròxims, la mitjana)
    var neg = p < 0.5, b = invF(neg ? 1 - p : p), z = b.tie ? (b.z + b.tie.z) / 2 : b.z;
    return { z: neg ? -z : z, b: b, neg: neg, pp: neg ? 1 - p : p };
  }

  /* ---------- dibuixos ---------- */
  function dens(x, m, s) { return Math.exp(-(x - m) * (x - m) / (2 * s * s)) / (s * Math.sqrt(2 * Math.PI)); }
  function vb(svg) { var v = svg.getAttribute("viewBox").split(" ").map(Number); return { W: v[2], H: v[3] }; }
  // corba normal amb regions ombrejades: o = {m, s, x0, x1, shade: [[a, b]], ticks: [...], cmp: true, ymax}
  function normPlot(svg, o) {
    var d = vb(svg), W = d.W, H = d.H, L = 14, R = W - 10, T = 10, B = H - 22;
    var x0 = o.x0, x1 = o.x1, ym = o.ymax || dens(o.m, o.m, o.s) * 1.08;
    if (o.cmp) ym = Math.max(ym, dens(0, 0, 1) * 1.08);
    function X(x) { return L + (R - L) * (x - x0) / (x1 - x0); }
    function Y(y) { return B - (B - T) * y / ym; }
    var h = '<line class="ax" x1="' + L + '" x2="' + R + '" y1="' + B + '" y2="' + B + '"/>';
    function path(m, s, a, b) { var pts = [], N = 160; for (var i = 0; i <= N; i++) { var x = a + (b - a) * i / N; pts.push(X(x).toFixed(1) + "," + Y(dens(x, m, s)).toFixed(1)); } return pts; }
    (o.shade || []).forEach(function (ab) {
      var a = Math.max(ab[0], x0), b = Math.min(ab[1], x1); if (!(b > a)) return;
      h += '<polygon class="area" points="' + X(a).toFixed(1) + "," + B + " " + path(o.m, o.s, a, b).join(" ") + " " + X(b).toFixed(1) + "," + B + '"/>';
    });
    if (o.cmp) h += '<polyline class="cv2" points="' + path(0, 1, x0, x1).join(" ") + '"/>';
    h += '<polyline class="cv" points="' + path(o.m, o.s, x0, x1).join(" ") + '"/>';
    (o.ticks || []).forEach(function (t) {
      if (t[0] < x0 || t[0] > x1) return;
      h += '<line class="ax" x1="' + X(t[0]) + '" x2="' + X(t[0]) + '" y1="' + B + '" y2="' + (B + 4) + '"/><text x="' + X(t[0]) + '" y="' + (B + 15) + '" text-anchor="middle"' + (t[2] ? ' class="vl"' : "") + ">" + t[1] + "</text>";
    });
    (o.lines || []).forEach(function (x) { if (x >= x0 && x <= x1) h += '<line x1="' + X(x) + '" x2="' + X(x) + '" y1="' + T + '" y2="' + B + '" style="stroke:var(--accent);stroke-width:1.4;stroke-dasharray:4 4"/>'; });
    if (o.label) h += '<text x="' + (W - 12) + '" y="' + (T + 12) + '" text-anchor="end" class="vl">' + o.label + "</text>";
    svg.innerHTML = h;
  }
  // barres de la binomial (i, opcionalment, la normal aproximada)
  function barsPlot(svg, n, p, sel, ov) {
    var d = vb(svg), W = d.W, H = d.H, L = 14, R = W - 10, T = 12, B = H - 22, ps = [], ym = 0, k;
    var m = n * p, s = Math.sqrt(n * p * (1 - p)), lo = 0, hi = n;
    if (n > 30) { lo = Math.max(0, Math.floor(m - 4.5 * s)); hi = Math.min(n, Math.ceil(m + 4.5 * s)); }
    for (k = lo; k <= hi; k++) { ps[k] = pmf(n, p, k); ym = Math.max(ym, ps[k]); }
    if (ov) ym = Math.max(ym, dens(m, m, s));
    ym *= 1.1;
    var x0 = lo - 0.6, x1 = hi + 0.6;
    function X(x) { return L + (R - L) * (x - x0) / (x1 - x0); }
    function Y(y) { return B - (B - T) * y / ym; }
    var h = '<line class="ax" x1="' + L + '" x2="' + R + '" y1="' + B + '" y2="' + B + '"/>', bw = Math.max(1, (X(1) - X(0)) * 0.8);
    if (ov && ov.shade) {
      var a = Math.max(ov.shade[0], x0), b = Math.min(ov.shade[1], x1), pts = [];
      if (b > a) { for (var i = 0; i <= 120; i++) { var x = a + (b - a) * i / 120; pts.push(X(x).toFixed(1) + "," + Y(dens(x, m, s)).toFixed(1)); }
        h += '<polygon class="area" points="' + X(a).toFixed(1) + "," + B + " " + pts.join(" ") + " " + X(b).toFixed(1) + "," + B + '"/>'; }
    }
    for (k = lo; k <= hi; k++) h += '<rect class="bar' + (sel(k) ? " on" : "") + '" x="' + (X(k) - bw / 2).toFixed(1) + '" y="' + Y(ps[k]).toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + (B - Y(ps[k])).toFixed(1) + '"' + (ov ? ' style="opacity:.75"' : "") + "/>";
    if (ov) { var q = []; for (var j = 0; j <= 200; j++) { var xx = x0 + (x1 - x0) * j / 200; q.push(X(xx).toFixed(1) + "," + Y(dens(xx, m, s)).toFixed(1)); } h += '<polyline class="cv" points="' + q.join(" ") + '"/>'; }
    var st = Math.max(1, Math.ceil((hi - lo) / 10));
    for (k = lo; k <= hi; k++) if ((k - lo) % st === 0) h += '<text x="' + X(k) + '" y="' + (B + 14) + '" text-anchor="middle">' + k + "</text>";
    svg.innerHTML = h;
  }

  /* ---------- figures estàtiques de la normal ---------- */
  function wFigs() {
    var Z = [-3.4, 3.4], t = function (x, l) { return [x, l, true]; };
    var FIG = {
      dens: function () { return { m: 0, s: 1, x0: -3.4, x1: 3.4, shade: [[-0.4, 1.3]], ticks: [t(-0.4, "a"), t(1.3, "b")], label: "y = f(x)" }; },
      le: function () { return { m: 0, s: 1, x0: Z[0], x1: Z[1], shade: [[-9, 0.8]], ticks: [t(0, "0"), t(0.8, "z")] }; },
      ge: function () { return { m: 0, s: 1, x0: Z[0], x1: Z[1], shade: [[0.8, 9]], ticks: [t(0, "0"), t(0.8, "z")] }; },
      neg: function () { return { m: 0, s: 1, x0: Z[0], x1: Z[1], shade: [[-9, -0.8]], ticks: [t(-0.8, "−z"), t(0, "0")] }; },
      ngt: function () { return { m: 0, s: 1, x0: Z[0], x1: Z[1], shade: [[-0.8, 9]], ticks: [t(-0.8, "−z"), t(0, "0")] }; },
      ab: function () { return { m: 0, s: 1, x0: Z[0], x1: Z[1], shade: [[-0.6, 1.4]], ticks: [t(-0.6, "a"), t(1.4, "b")] }; },
      sym: function () { return { m: 0, s: 1, x0: Z[0], x1: Z[1], shade: [[-1.2, 1.2]], ticks: [t(-1.2, "−z"), t(1.2, "z")] }; }
    };
    document.querySelectorAll("svg[data-nf]").forEach(function (svg) { var f = FIG[svg.getAttribute("data-nf")]; if (f) normPlot(svg, f()); });
  }

  /* ---------- càlculs amb la binomial ---------- */
  var BEV = [["eq", "P(X = k)"], ["le", "P(X ≤ k)"], ["lt", "P(X < k)"], ["ge", "P(X ≥ k)"], ["gt", "P(X > k)"], ["ab", "P(k ≤ X ≤ k₂)"]];
  function bset(ev, a, b) {
    return function (k) { return ev === "eq" ? k === a : ev === "le" ? k <= a : ev === "lt" ? k < a : ev === "ge" ? k >= a : ev === "gt" ? k > a : k >= a && k <= b; };
  }
  function bEvTex(ev, a, b) { return ev === "eq" ? "P(X=" + a + ")" : ev === "le" ? "P(X\\leq " + a + ")" : ev === "lt" ? "P(X\\lt " + a + ")" : ev === "ge" ? "P(X\\geq " + a + ")" : ev === "gt" ? "P(X\\gt " + a + ")" : "P(" + a + "\\leq X\\leq " + b + ")"; }
  function binCalc(n, p, ev, a, b) {
    var f = bset(ev, a, b), ks = [], co = [], k, P = 0, Pc = 0;
    for (k = 0; k <= n; k++) { var v = pmf(n, p, k); if (f(k)) { ks.push(k); P += v; } else { co.push(k); Pc += v; } }
    var pt = td(p, 4), qt = td(1 - p, 4), h = "<p>" + tex("X\\sim B(" + n + ";\\," + pt + ")") + "</p>";
    function term(k) { return "\\tbinom{" + n + "}{" + k + "}" + pt + "^{" + k + "}" + qt + "^{" + (n - k) + "}"; }
    var useC = co.length < ks.length && co.length <= 4;
    var set = useC ? co : ks;
    if (set.length === 1) h += "<p>" + tex((useC ? "1-P(X=" + set[0] + ")=1-" : "P(X=" + set[0] + ")=") + term(set[0])) + "</p>";
    if (set.length <= 6) {
      h += "<p>" + tex(bEvTex(ev, a, b) + "=" + (useC ? "1-[" : "") + set.map(function (k) { return "P(" + k + ")"; }).join("+") + (useC ? "]" : "")) + "</p>";
      if (set.length > 1) h += "<p>" + tex("=" + (useC ? "1-(" : "") + set.map(function (k) { return f4(pmf(n, p, k)); }).join("+") + (useC ? ")" : "")) + "</p>";
    } else h += "<p>" + t3("Cal sumar ", "Hay que sumar ", "We need to add ") + set.length + t3(" termes: és un bon cas per a l'aproximació normal (10.9).", " términos: es un buen caso para la aproximación normal (10.9).", " terms: a good case for the normal approximation (10.9).") + "</p>";
    h += '<p class="big-p">' + tex(bEvTex(ev, a, b) + "\\approx " + f4(P)) + "</p>";
    h += "<p style='font-size:.88rem;color:var(--muted)'>" + tex("\\mu=np=" + td(n * p, 3) + ",\\ \\ \\sigma=\\sqrt{npq}\\approx " + td(Math.sqrt(n * p * (1 - p)), 3)) + "</p>";
    return { P: P, h: h, f: f };
  }
  function inTable(n, p) {
    if (n < 2 || n > 9) return null;
    for (var j = 0; j < PJ.length; j++) { if (Math.abs(PJ[j].p - p) < 1e-9) return { j: j, sw: false }; if (Math.abs(PJ[j].p - (1 - p)) < 1e-9) return { j: j, sw: true }; }
    return null;
  }

  /* ---------- widget: variable aleatòria discreta ---------- */
  function wDisc() {
    var w = document.getElementById("w-disc"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), tb = $(w, "tbl"), ix = $(w, "x"), ip = $(w, "p");
    var PRE = [
      { x: "0 1 2 3", p: "1/8 3/8 3/8 1/8", l: function () { return t3("Tres monedes", "Tres monedas", "Three coins"); } },
      { x: "1 2 3 4 5 6", p: "1/6 1/6 1/6 1/6 1/6 1/6", l: function () { return t3("Un dau", "Un dado", "One die"); } },
      { x: "2 3 4 5 6 7 8 9 10 11 12", p: "1/36 2/36 3/36 4/36 5/36 6/36 5/36 4/36 3/36 2/36 1/36", l: function () { return t3("Suma de dos daus", "Suma de dos dados", "Sum of two dice"); } },
      { x: "28 4 -2", p: "1/36 6/36 29/36", l: function () { return t3("Joc de la fira", "Juego de la feria", "Fair game"); } }
    ];
    presetBtns($(w, "presets"), function () { return PRE.map(function (p) { return p.l(); }); }, function (i) { ix.value = PRE[i].x; ip.value = PRE[i].p; draw(); })[0].classList.add("on");
    [ix, ip].forEach(function (e) { e.addEventListener("input", draw); });
    function split(s) { return String(s).trim().split(/[\s;]+/).filter(function (t) { return t !== ""; }); }
    function draw() {
      var xs = split(ix.value).map(num), ps = split(ip.value).map(num), n = xs.length;
      if (!n || n !== ps.length || xs.some(isNaN) || ps.some(function (p) { return isNaN(p) || p < 0 || p > 1; }) || n > 15) {
        tb.innerHTML = ""; svg.innerHTML = "";
        info.innerHTML = "<p class='chk no'>" + t3("Escriu el mateix nombre de valors que de probabilitats (fins a 15), separats per espais. Les probabilitats han d'estar entre 0 i 1.", "Escribe el mismo número de valores que de probabilidades (hasta 15), separados por espacios. Las probabilidades tienen que estar entre 0 y 1.", "Type as many values as probabilities (up to 15), separated by spaces. Probabilities must be between 0 and 1.") + "</p>";
        return;
      }
      var S = ps.reduce(function (a, b) { return a + b; }, 0), mu = 0, m2 = 0, F = 0, rows = [[], [], [], [], []];
      xs.forEach(function (x, i) { F += ps[i]; mu += x * ps[i]; m2 += x * x * ps[i]; rows[0].push(td(x, 4)); rows[1].push(td(ps[i], 4)); rows[2].push(td(F, 4)); rows[3].push(td(x * ps[i], 4)); rows[4].push(td(x * x * ps[i], 4)); });
      var heads = ["x_i", "p_i", "F(x_i)", "x_i\\,p_i", "x_i^2\\,p_i"], sums = ["", td(S, 4), "", td(mu, 4), td(m2, 4)];
      tb.innerHTML = '<table class="data sm" style="margin:8px auto"><tbody>' + rows.map(function (r, k) {
        return "<tr><th>" + tex(heads[k]) + "</th>" + r.map(function (v) { return "<td>" + tex(v) + "</td>"; }).join("") + "<td><b>" + (sums[k] ? tex(sums[k]) : (k === 0 ? "Σ" : "")) + "</b></td></tr>";
      }).join("") + "</tbody></table>";
      if (Math.abs(S - 1) > 1e-6) {
        info.innerHTML = "<p class='chk no'>" + tex("\\sum p_i=" + td(S, 4) + "\\neq1") + ": " + t3("no és una funció de probabilitat.", "no es una función de probabilidad.", "this is not a probability function.") + "</p>";
      } else {
        var v = m2 - mu * mu; if (Math.abs(v) < 1e-12) v = 0;
        info.innerHTML = "<p>" + tex("\\sum p_i=1") + " ✓</p><p>" + tex("\\mu=\\sum x_ip_i=" + td(mu, 4)) + "</p><p>" + tex("\\sigma^2=\\sum x_i^2p_i-\\mu^2=" + td(m2, 4) + "-" + (mu < 0 ? "(" + td(mu, 4) + ")" : td(mu, 4)) + "^2\\approx " + td(v, 4)) + "</p><p class='big-p'>" + tex("\\sigma\\approx " + td(Math.sqrt(v), 4)) + "</p>";
      }
      // diagrama de barres
      var d = vb(svg), W = d.W, H = d.H, L = 30, R = W - 12, T = 14, B = H - 24, lo = Math.min.apply(null, xs), hi = Math.max.apply(null, xs), ym = Math.max.apply(null, ps) * 1.15 || 1;
      if (hi === lo) { lo -= 1; hi += 1; }
      var pad = (hi - lo) * 0.08 + 0.5;
      function X(x) { return L + (R - L) * (x - lo + pad) / (hi - lo + 2 * pad); }
      function Y(y) { return B - (B - T) * y / ym; }
      var h = '<line class="ax" x1="' + L + '" x2="' + R + '" y1="' + B + '" y2="' + B + '"/><line class="ax" x1="' + L + '" x2="' + L + '" y1="' + T + '" y2="' + B + '"/>';
      var bw = Math.max(3, Math.min(26, (R - L) / (n + 1) * 0.5));
      xs.forEach(function (x, i) { h += '<rect class="bar on" x="' + (X(x) - bw / 2).toFixed(1) + '" y="' + Y(ps[i]).toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + (B - Y(ps[i])).toFixed(1) + '"/><text x="' + X(x).toFixed(1) + '" y="' + (B + 14) + '" text-anchor="middle">' + decS(x, 2) + "</text>"; });
      if (Math.abs(S - 1) <= 1e-6) h += '<line x1="' + X(mu).toFixed(1) + '" x2="' + X(mu).toFixed(1) + '" y1="' + T + '" y2="' + B + '" style="stroke:var(--accent-2);stroke-width:1.6;stroke-dasharray:5 4"/><text class="vl" x="' + X(mu).toFixed(1) + '" y="' + (T + 2) + '" text-anchor="middle">μ</text>';
      h += '<text x="' + (L - 4) + '" y="' + (Y(ym / 1.15) + 4).toFixed(1) + '" text-anchor="end">' + decS(ym / 1.15, 3) + "</text>";
      svg.innerHTML = h;
    }
    onLang(draw);
  }

  /* ---------- widget: funcions de densitat (àrees geomètriques) ---------- */
  function wDens() {
    var w = document.getElementById("w-dens"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), kind = "U";
    var K = [["U", function () { return t3("Uniforme", "Uniforme", "Uniform"); }], ["T", function () { return t3("Triangular", "Triangular", "Triangular"); }], ["R", function () { return t3("Triangle creixent", "Triángulo creciente", "Rising triangle"); }]];
    var DEF = { U: ["0", "15", "5", "10"], T: ["0", "4", "1", "3"], R: ["0", "2", "1", "1.5"] };
    var bs = K.map(function (k) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { kind = k[0]; ["a", "b", "c", "d"].forEach(function (r, i) { $(w, r).value = DEF[kind][i]; }); lab(); draw(); });
      $(w, "kind").appendChild(b); return b;
    });
    function lab() { bs.forEach(function (b, i) { b.textContent = K[i][1](); b.classList.toggle("on", K[i][0] === kind); }); }
    ["a", "b", "c", "d"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    function draw() {
      var a = num($(w, "a").value), b = num($(w, "b").value), c = num($(w, "c").value), dd = num($(w, "d").value);
      if ([a, b, c, dd].some(isNaN) || !(b > a) || dd < c) { info.innerHTML = "<p class='chk no'>" + t3("Escriu a < b i c ≤ d.", "Escribe a < b y c ≤ d.", "Type a < b and c ≤ d.") + "</p>"; svg.innerHTML = ""; return; }
      var L = b - a, m = (a + b) / 2, hU = 1 / L, hT = 2 / L;
      function f(x) {
        if (x < a || x > b) return 0;
        if (kind === "U") return hU;
        if (kind === "R") return hT * (x - a) / L;
        return x <= m ? hT * (x - a) / (m - a) : hT * (b - x) / (b - m);
      }
      function Fx(x) {
        if (x <= a) return 0; if (x >= b) return 1;
        if (kind === "U") return (x - a) / L;
        if (kind === "R") return (x - a) * f(x) / 2;
        return x <= m ? (x - a) * f(x) / 2 : 1 - (b - x) * f(x) / 2;
      }
      var c1 = Math.max(c, a), d1 = Math.min(dd, b), P = Math.max(0, Fx(dd) - Fx(c)), h = "";
      var den = kind === "U" ? "f(x)=\\frac{1}{" + td(L, 4) + "}" : kind === "R" ? "f(x)=\\frac{2\\,(x-" + (a < 0 ? "(" + td(a, 4) + ")" : td(a, 4)) + ")}{" + td(L * L, 4) + "}" : "f(" + td(m, 4) + ")=\\frac{2}{" + td(L, 4) + "}=" + td(hT, 4);
      h += "<p>" + tex(den) + (kind === "T" ? " " + t3("(altura del triangle, perquè l'àrea siga 1)", "(altura del triángulo, para que el área sea 1)", "(triangle height, so that the area is 1)") : "") + "</p>";
      if (!(d1 > c1)) h += "<p>" + t3("L'interval no talla la zona on la densitat és positiva: l'àrea és 0.", "El intervalo no corta la zona donde la densidad es positiva: el área es 0.", "The interval misses the region where the density is positive: the area is 0.") + "</p>";
      else if (kind === "U") h += "<p>" + t3("Rectangle", "Rectángulo", "Rectangle") + ": " + tex("(" + td(d1, 4) + "-" + (c1 < 0 ? "(" + td(c1, 4) + ")" : td(c1, 4)) + ")\\cdot\\frac1{" + td(L, 4) + "}=" + td(P, 4)) + "</p>";
      else if (kind === "R" || (d1 <= m || c1 >= m)) h += "<p>" + (Math.abs(f(c1)) < 1e-12 || Math.abs(f(d1)) < 1e-12 ? t3("Triangle", "Triángulo", "Triangle") : t3("Trapezi", "Trapecio", "Trapezium")) + ": " + tex("\\frac{f(" + td(c1, 4) + ")+f(" + td(d1, 4) + ")}{2}\\cdot(" + td(d1, 4) + "-" + (c1 < 0 ? "(" + td(c1, 4) + ")" : td(c1, 4)) + ")=\\frac{" + td(f(c1), 4) + "+" + td(f(d1), 4) + "}{2}\\cdot" + td(d1 - c1, 4) + "=" + td(P, 4)) + "</p>";
      else h += "<p>" + t3("Amb la funció de distribució (àrees a l'esquerra):", "Con la función de distribución (áreas a la izquierda):", "With the distribution function (areas to the left):") + " " + tex("F(" + td(d1, 4) + ")-F(" + td(c1, 4) + ")=" + td(Fx(d1), 4) + "-" + td(Fx(c1), 4) + "=" + td(P, 4)) + "</p>";
      h += '<p class="big-p">' + tex("P(" + td(c, 4) + "\\leq X\\leq " + td(dd, 4) + ")=" + td(P, 4)) + "</p>";
      if (kind === "U") h += "<p style='font-size:.88rem;color:var(--muted)'>" + tex("\\mu=\\frac{a+b}{2}=" + td(m, 4)) + "</p>";
      info.innerHTML = h;
      // dibuix
      var g = vb(svg), W = g.W, H = g.H, Lx = 14, Rx = W - 10, T = 14, B = H - 24, x0 = a - 0.15 * L, x1 = b + 0.15 * L, ym = (kind === "U" ? hU : hT) * 1.2;
      function X(x) { return Lx + (Rx - Lx) * (x - x0) / (x1 - x0); }
      function Y(y) { return B - (B - T) * y / ym; }
      var pts = [], N = 200, i, x;
      for (i = 0; i <= N; i++) { x = x0 + (x1 - x0) * i / N; pts.push(X(x).toFixed(1) + "," + Y(f(x)).toFixed(1)); }
      var s = '<line class="ax" x1="' + Lx + '" x2="' + Rx + '" y1="' + B + '" y2="' + B + '"/>';
      if (d1 > c1) { var q = [X(c1).toFixed(1) + "," + B]; for (i = 0; i <= 80; i++) { x = c1 + (d1 - c1) * i / 80; q.push(X(x).toFixed(1) + "," + Y(f(x)).toFixed(1)); } q.push(X(d1).toFixed(1) + "," + B); s += '<polygon class="area" points="' + q.join(" ") + '"/>'; }
      s += '<polyline class="cv" points="' + pts.join(" ") + '"/>';
      [[a, "a"], [b, "b"], [c, "c"], [dd, "d"]].forEach(function (t) { if (t[0] >= x0 && t[0] <= x1) s += '<line class="ax" x1="' + X(t[0]) + '" x2="' + X(t[0]) + '" y1="' + B + '" y2="' + (B + 4) + '"/><text x="' + X(t[0]) + '" y="' + (B + 15) + '" text-anchor="middle"' + (t[1] === "c" || t[1] === "d" ? ' class="vl"' : "") + ">" + decS(t[0], 2) + "</text>"; });
      svg.innerHTML = s;
    }
    onLang(function () { lab(); draw(); });
  }

  /* ---------- widget: binomial ---------- */
  function wBin() {
    var w = document.getElementById("w-bin"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), ev = $(w, "ev");
    fillSelect(ev, BEV); ev.value = "eq";
    ["n", "p", "a", "b"].forEach(function (r) { $(w, r).addEventListener("input", draw); }); ev.addEventListener("change", draw);
    function draw() {
      var n = Math.round(num($(w, "n").value)), p = num($(w, "p").value), a = Math.round(num($(w, "a").value)), b = Math.round(num($(w, "b").value)), e = ev.value;
      $(w, "blab").style.display = e === "ab" ? "" : "none";
      if (!(n >= 1 && n <= 60) || !(p > 0 && p < 1) || isNaN(a) || (e === "ab" && isNaN(b))) { info.innerHTML = "<p class='chk no'>" + t3("Escriu 1 ≤ n ≤ 60 i 0 < p < 1.", "Escribe 1 ≤ n ≤ 60 y 0 < p < 1.", "Type 1 ≤ n ≤ 60 and 0 < p < 1.") + "</p>"; return; }
      var r = binCalc(n, p, e, a, b), tb = inTable(n, p);
      info.innerHTML = r.h + (tb ? "<p style='font-size:.88rem'>" + (tb.sw ? t3("Amb la taula: compta els fracassos, ", "Con la tabla: cuenta los fracasos, ", "With the table: count failures, ") + tex("B(" + n + ";\\," + td(1 - p, 4) + ")") : t3("També es pot fer amb la taula de la binomial (10.4).", "También se puede hacer con la tabla de la binomial (10.4).", "You can also use the binomial table (10.4).")) + "</p>" : "");
      barsPlot(svg, n, p, r.f);
    }
    onLang(function () { fillSelect(ev, BEV); draw(); });
  }

  /* ---------- widget: taula de la binomial ---------- */
  function wTbin() {
    var w = document.getElementById("w-tbin"); if (!w) return;
    var tbl = document.getElementById("tbin"), info = w.querySelector(".info"), sn = $(w, "n"), sp = $(w, "p"), se = $(w, "ev"), sk = $(w, "k"), wrap = $(w, "wrap");
    fillSelect(sn, [2, 3, 4, 5, 6, 7, 8, 9].map(function (n) { return [n, n]; })); sn.value = 8;
    var popts = PJ.map(function (o, j) { return ["t" + j, o.l]; }).concat(PJ.slice(0, 12).reverse().map(function (o, i) { var j = 11 - i; return ["c" + j, o.l === "1/3" ? "2/3" : decS(1 - o.p, 2)]; }));
    fillSelect(sp, popts); sp.value = "t4";
    var EV = [["eq", "P(X = k)"], ["le", "P(X ≤ k)"], ["ge", "P(X ≥ k)"]];
    fillSelect(se, EV); se.value = "le";
    function ks() { var n = +sn.value, v = sk.value; fillSelect(sk, Array.apply(null, Array(n + 1)).map(function (_, i) { return [i, i]; })); sk.value = v !== "" && +v <= n ? v : Math.min(2, n); }
    ks();
    [sn].forEach(function (s) { s.addEventListener("change", function () { ks(); draw(true); }); });
    [sp, se, sk].forEach(function (s) { s.addEventListener("change", function () { draw(true); }); });
    tbl.addEventListener("click", function (e) {
      var tdc = e.target.closest("td"); if (!tdc) return;
      var tr = tdc.parentNode, n = +tr.getAttribute("data-n"), x = +tr.getAttribute("data-x"), j = +tdc.getAttribute("data-j");
      sn.value = n; ks(); sp.value = "t" + j; se.value = "eq"; sk.value = x; draw(false);
    });
    function draw(scroll) {
      var n = +sn.value, pv = sp.value, j = +pv.slice(1), sw = pv[0] === "c", k = +sk.value, e = se.value, p = sw ? 1 - PJ[j].p : PJ[j].p;
      var pl = sw ? (PJ[j].l === "1/3" ? "2/3" : td(1 - PJ[j].p, 2)) : PJ[j].l.replace(",", "{,}");
      var ql = PJ[j].l.replace(",", "{,}");
      var f = e === "eq" ? function (x) { return x === k; } : e === "le" ? function (x) { return x <= k; } : function (x) { return x >= k; };
      var xs = []; for (var x = 0; x <= n; x++) if (f(x)) xs.push(x);
      var ys = xs.map(function (x) { return sw ? n - x : x; });
      var useC = ys.length > (n + 1) / 2 + 0.5;
      var cs = []; if (useC) for (var y = 0; y <= n; y++) if (ys.indexOf(y) < 0) cs.push(y);
      tbl.querySelectorAll("td").forEach(function (c) { c.classList.remove("on", "on2", "col"); });
      tbl.querySelectorAll("tr.row").forEach(function (r) { r.classList.remove("row"); });
      tbl.querySelectorAll("td[data-j='" + j + "']").forEach(function (c) { c.classList.add("col"); });
      var cells = [];
      (useC ? cs : ys).forEach(function (y) { var c = tbl.querySelector("tr[data-n='" + n + "'][data-x='" + y + "'] td[data-j='" + j + "']"); if (c) { c.classList.add(useC ? "on2" : "on"); cells.push(c); } });
      var evt = e === "eq" ? "P(X=" + k + ")" : e === "le" ? "P(X\\leq " + k + ")" : "P(X\\geq " + k + ")";
      var h = "<p>" + tex("X\\sim B(" + n + ";\\," + pl + ")") + "</p>";
      if (sw) {
        var ev2 = e === "eq" ? "P(Y=" + (n - k) + ")" : e === "le" ? "P(Y\\geq " + (n - k) + ")" : "P(Y\\leq " + (n - k) + ")";
        h += "<p>" + t3("La taula no té ", "La tabla no tiene ", "The table has no ") + tex("p=" + pl) + t3(": comptem els fracassos, ", ": contamos los fracasos, ", ": count failures, ") + tex("Y=" + n + "-X\\sim B(" + n + ";\\," + ql + ")") + ".</p><p>" + tex(evt + "=" + ev2) + "</p>";
      }
      var vals = (useC ? cs : ys).map(function (y) { return BT[n][y][j]; }), sum = vals.reduce(function (s, v) { return s + v; }, 0), P = useC ? 1 - sum : sum;
      var vy = sw ? "Y" : "X";
      if (useC) h += "<p>" + t3("Més curt amb el contrari:", "Más corto con el contrario:", "Shorter with the complement:") + " " + tex("1-[" + cs.map(function (y) { return "P(" + vy + "=" + y + ")"; }).join("+") + "]") + "</p>";
      h += "<p>" + tex("=" + (useC ? "1-(" : "") + vals.map(f4).join("+") + (useC ? ")" : "")) + "</p>";
      h += '<p class="big-p">' + tex(evt + "=" + f4(P)) + "</p>";
      h += "<p style='font-size:.85rem;color:var(--muted)'>" + t3("Caselles marcades en el bloc ", "Casillas marcadas en el bloque ", "Marked cells in block ") + "n = " + n + t3(", columna ", ", columna ", ", column ") + "p = " + PJ[j].l + ".</p>";
      info.innerHTML = h;
      if (scroll && cells[0]) { var top = cells[0].offsetTop - 60; wrap.scrollTo({ top: Math.max(0, top), behavior: "smooth" }); }
    }
    onLang(function () { draw(false); });
  }

  /* ---------- càlculs amb la normal ---------- */
  var NEV = function () {
    return [["le", "P(X ≤ a)"], ["ge", "P(X ≥ a)"], ["ab", "P(a ≤ X ≤ b)"], ["ile", t3("Invers: P(X ≤ k) = p", "Inverso: P(X ≤ k) = p", "Inverse: P(X ≤ k) = p")], ["ige", t3("Invers: P(X ≥ k) = p", "Inverso: P(X ≥ k) = p", "Inverse: P(X ≥ k) = p")]];
  };
  // passos per a X ~ N(m, s); torna {h, P, shade, z}
  function normCalc(m, s, ev, a, b) {
    var h = "<p>" + tex("X\\sim N(" + td(m, 4) + ";\\," + td(s, 4) + ")") + "</p>", P, shade, zs = [];
    function zt(x) { var z = (x - m) / s; zs.push(r2(z)); return "\\frac{" + td(x, 4) + "-" + td(m, 4) + "}{" + td(s, 4) + "}" + (Math.abs(z - r2(z)) > 1e-9 ? "\\approx " : "=") + td(r2(z), 2); }
    function Ft(z) { z = r2(z); return z >= 0 ? "P(Z\\leq " + td(z, 2) + ")=" + f4(F(z)) : "1-P(Z\\leq " + td(-z, 2) + ")=1-" + f4(F(-z)) + "=" + f4(F(z)); }
    if (ev === "le" || ev === "ge") {
      var z = (a - m) / s, zr = r2(z);
      h += "<p>" + tex("Z=" + zt(a)) + "</p>";
      if (ev === "le") { P = F(zr); h += "<p>" + tex("P(X\\leq " + td(a, 4) + ")=P(Z\\leq " + td(zr, 2) + ")") + "</p><p>" + tex("=" + Ft(zr)) + "</p>"; shade = [[-1e9, a]]; }
      else { P = 1 - F(zr); h += "<p>" + tex("P(X\\geq " + td(a, 4) + ")=P(Z\\geq " + td(zr, 2) + ")=1-P(Z\\leq " + td(zr, 2) + ")") + "</p><p>" + tex("=1-" + f4(F(zr)) + "=" + f4(P)) + "</p>"; shade = [[a, 1e9]]; }
    } else if (ev === "ab") {
      var za = r2((a - m) / s), zb = r2((b - m) / s);
      h += "<p>" + tex("z_1=" + zt(a) + ",\\quad z_2=" + zt(b)) + "</p>";
      P = F(zb) - F(za);
      h += "<p>" + tex("P(" + td(za, 2) + "\\leq Z\\leq " + td(zb, 2) + ")=P(Z\\leq " + td(zb, 2) + ")-P(Z\\leq " + td(za, 2) + ")") + "</p><p>" + tex("=" + f4(F(zb)) + "-" + f4(F(za)) + "=" + f4(P)) + "</p>";
      shade = [[a, b]];
    } else {
      var pp = ev === "ile" ? a : 1 - a, zi = zinv(pp), k = m + zi.z * s;
      if (ev === "ige") h += "<p>" + tex("P(X\\geq k)=" + td(a, 4) + "\\iff P(X\\leq k)=" + td(pp, 4)) + "</p>";
      if (zi.neg) h += "<p>" + t3("Com que ", "Como ", "Since ") + tex(td(pp, 4) + "\\lt0{,}5") + t3(", el valor de z és negatiu: busquem ", ", el valor de z es negativo: buscamos ", ", z is negative: look up ") + tex(td(zi.pp, 4)) + t3(" a la taula.", " en la tabla.", " in the table.") + "</p>";
      h += "<p>" + t3("Valor més pròxim a la taula: ", "Valor más próximo en la tabla: ", "Closest table value: ") + tex(f4(zi.b.v) + "\\to z=" + td(zi.b.z, 2)) + (zi.b.tie ? " " + t3("(empat amb ", "(empate con ", "(tie with ") + tex(f4(zi.b.tie.v) + "\\to" + td(zi.b.tie.z, 2)) + t3(": prenem la mitjana)", ": tomamos la media)", ": take the average)") : "") + "</p>";
      h += "<p>" + tex("\\frac{k-" + td(m, 4) + "}{" + td(s, 4) + "}=" + td(zi.z, 3) + "\\Rightarrow k=" + td(m, 4) + (zi.z < 0 ? "-" : "+") + td(Math.abs(zi.z), 3) + "\\cdot" + td(s, 4) + "\\approx " + td(k, 3)) + "</p>";
      P = k; shade = ev === "ile" ? [[-1e9, k]] : [[k, 1e9]];
      zs.push(Math.abs(r2(zi.z)));
      return { h: h + '<p class="big-p">' + tex("k\\approx " + td(k, 3)) + "</p>", P: k, shade: shade, zs: zs, inv: zi };
    }
    h += '<p class="big-p">' + tex("P\\approx " + f4(P)) + "</p>";
    return { h: h, P: P, shade: shade, zs: zs };
  }
  function markZ(zs, inv) {
    var t = document.getElementById("tnorm"); if (!t) return null;
    t.querySelectorAll("td").forEach(function (c) { c.classList.remove("on", "on2"); });
    var first = null;
    if (inv) {
      [inv.b, inv.b.tie].forEach(function (b) { if (!b) return; var c = t.querySelector("tr[data-r='" + b.r + "'] td[data-c='" + b.c + "']"); if (c) { c.classList.add("on"); first = first || c; } });
      return first;
    }
    zs.forEach(function (z, i) { var rc = cell(z); if (!rc) return; var c = t.querySelector("tr[data-r='" + rc[0] + "'] td[data-c='" + rc[1] + "']"); if (c) { c.classList.add(i ? "on2" : "on"); first = first || c; } });
    return first;
  }

  /* ---------- widget: campana de Gauss ---------- */
  function wNorm() {
    var w = document.getElementById("w-norm"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info");
    ["m", "s", "a", "b"].forEach(function (r) { $(w, r).addEventListener("input", draw); });
    presetBtns($(w, "presets"), function () { return ["μ ± σ", "μ ± 2σ", "μ ± 3σ"]; }, function (i) {
      var m = +$(w, "m").value, s = +$(w, "s").value; $(w, "a").value = decS(m - (i + 1) * s, 2).replace(",", "."); $(w, "b").value = decS(m + (i + 1) * s, 2).replace(",", "."); draw();
    });
    function draw() {
      var m = +$(w, "m").value, s = +$(w, "s").value, a = num($(w, "a").value), b = num($(w, "b").value);
      $(w, "mv").textContent = decS(m, 1); $(w, "sv").textContent = decS(s, 1);
      if (isNaN(a) || isNaN(b) || b < a) { info.innerHTML = "<p class='chk no'>" + t3("Escriu a ≤ b.", "Escribe a ≤ b.", "Type a ≤ b.") + "</p>"; return; }
      var r = normCalc(m, s, "ab", a, b);
      info.innerHTML = r.h;
      var ticks = [[m, "μ", true]]; [-2, -1, 1, 2].forEach(function (k) { ticks.push([m + k * s, (k > 0 ? "μ+" : "μ−") + (Math.abs(k) > 1 ? Math.abs(k) : "") + "σ"]); });
      normPlot(svg, { m: m, s: s, x0: -8, x1: 8, shade: r.shade, ticks: ticks, cmp: true, lines: [a, b], ymax: Math.max(dens(m, m, s), 0.42) * 1.08 });
    }
    onLang(draw);
  }

  /* ---------- widget: taula de la normal ---------- */
  function wTz() {
    var w = document.getElementById("w-tz"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), se = $(w, "ev"), wrap = $(w, "wrap"), tbl = document.getElementById("tnorm");
    function EV() { return [["le", "P(Z ≤ z)"], ["ge", "P(Z ≥ z)"], ["ab", "P(z ≤ Z ≤ z₂)"], ["sym", "P(−z ≤ Z ≤ z)"], ["ile", t3("Invers: P(Z ≤ k) = p", "Inverso: P(Z ≤ k) = p", "Inverse: P(Z ≤ k) = p")], ["ige", t3("Invers: P(Z ≥ k) = p", "Inverso: P(Z ≥ k) = p", "Inverse: P(Z ≥ k) = p")]]; }
    fillSelect(se, EV()); se.value = "le";
    var lastEv = "le";
    se.addEventListener("change", function () {
      var e = se.value, inv = e[0] === "i";
      if (inv !== (lastEv[0] === "i")) $(w, "a").value = inv ? "0.9" : "1.25";
      lastEv = e; draw(true);
    });
    ["a", "b"].forEach(function (r) { $(w, r).addEventListener("input", function () { draw(true); }); });
    tbl.addEventListener("click", function (e) {
      var c = e.target.closest("td"); if (!c) return;
      var z = +c.parentNode.getAttribute("data-r") / 10 + +c.getAttribute("data-c") / 100;
      se.value = "le"; lastEv = "le"; $(w, "a").value = z.toFixed(2); draw(false);
    });
    function draw(scroll) {
      var e = se.value, a = num($(w, "a").value), b = num($(w, "b").value);
      var inv = e[0] === "i";
      $(w, "lb").style.display = e === "ab" ? "" : "none";
      $(w, "la").firstChild.textContent = inv ? "p = " : "";
      if (isNaN(a) || (e === "ab" && isNaN(b)) || (inv && !(a > 0 && a < 1))) { info.innerHTML = "<p class='chk no'>" + t3("Revisa les dades.", "Revisa los datos.", "Check the data.") + "</p>"; return; }
      var h = "", shade, zs = [], ivr = null, P;
      if (e === "le" || e === "ge") {
        var zr = r2(a); zs = [Math.abs(zr)];
        if (e === "le") { P = F(zr); shade = [[-9, zr]]; h = zr >= 0 ? "<p>" + tex("P(Z\\leq " + td(zr, 2) + ")=" + f4(P)) + "</p>" : "<p>" + tex("P(Z\\leq " + td(zr, 2) + ")=1-P(Z\\leq " + td(-zr, 2) + ")=1-" + f4(F(-zr)) + "=" + f4(P)) + "</p>"; }
        else { P = 1 - F(zr); shade = [[zr, 9]]; h = zr >= 0 ? "<p>" + tex("P(Z\\geq " + td(zr, 2) + ")=1-P(Z\\leq " + td(zr, 2) + ")=1-" + f4(F(zr)) + "=" + f4(P)) + "</p>" : "<p>" + tex("P(Z\\geq " + td(zr, 2) + ")=P(Z\\leq " + td(-zr, 2) + ")=" + f4(P)) + "</p>"; }
      } else if (e === "ab") {
        var za = r2(Math.min(a, b)), zb = r2(Math.max(a, b)); zs = [Math.abs(zb), Math.abs(za)]; P = F(zb) - F(za); shade = [[za, zb]];
        h = "<p>" + tex("P(" + td(za, 2) + "\\leq Z\\leq " + td(zb, 2) + ")=P(Z\\leq " + td(zb, 2) + ")-P(Z\\leq " + td(za, 2) + ")") + "</p><p>" + tex("=" + f4(F(zb)) + "-" + f4(F(za)) + "=" + f4(P)) + "</p>";
      } else if (e === "sym") {
        var z = Math.abs(r2(a)); P = 2 * F(z) - 1; zs = [z]; shade = [[-z, z]];
        h = "<p>" + tex("P(-" + td(z, 2) + "\\leq Z\\leq " + td(z, 2) + ")=2P(Z\\leq " + td(z, 2) + ")-1") + "</p><p>" + tex("=2\\cdot" + f4(F(z)) + "-1=" + f4(P)) + "</p>";
      } else {
        var pp = e === "ile" ? a : 1 - a; ivr = zinv(pp);
        if (e === "ige") h += "<p>" + tex("P(Z\\geq k)=" + td(a, 4) + "\\iff P(Z\\leq k)=" + td(pp, 4)) + "</p>";
        if (ivr.neg) h += "<p>" + t3("Com que la probabilitat és menor que 0,5, k és negatiu. Per simetria busquem ", "Como la probabilidad es menor que 0,5, k es negativo. Por simetría buscamos ", "Since the probability is below 0.5, k is negative. By symmetry we look up ") + tex(td(ivr.pp, 4)) + ".</p>";
        h += "<p>" + t3("A la taula, el més pròxim és ", "En la tabla, el más próximo es ", "In the table, the closest is ") + tex(f4(ivr.b.v) + "\\to " + td(ivr.b.z, 2)) + (ivr.b.tie ? " " + t3("i ", "y ", "and ") + tex(f4(ivr.b.tie.v) + "\\to " + td(ivr.b.tie.z, 2)) + t3(" (igual de pròxims: prenem la mitjana)", " (igual de próximos: tomamos la media)", " (equally close: take the average)") : "") + "</p>";
        h += '<p class="big-p">' + tex("k\\approx " + td(ivr.z, 3)) + "</p>";
        shade = e === "ile" ? [[-9, ivr.z]] : [[ivr.z, 9]];
      }
      info.innerHTML = h;
      normPlot(svg, { m: 0, s: 1, x0: -3.6, x1: 3.6, shade: shade, ticks: [[-3, "−3"], [-2, "−2"], [-1, "−1"], [0, "0"], [1, "1"], [2, "2"], [3, "3"]] });
      var c = markZ(zs, ivr);
      if (scroll && c) wrap.scrollTo({ top: Math.max(0, c.offsetTop - 80), behavior: "smooth" });
    }
    onLang(function () { fillSelect(se, EV()); draw(false); });
  }

  /* ---------- widget: tipificació ---------- */
  function wTip() {
    var w = document.getElementById("w-tip"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), se = $(w, "ev");
    var PRE = [
      { m: "100", s: "14", e: "ab", a: "108", b: "116", l: function () { return t3("CI entre 108 i 116", "CI entre 108 y 116", "IQ between 108 and 116"); } },
      { m: "70", s: "15", e: "ge", a: "80", l: function () { return t3("Pes > 80 kg", "Peso > 80 kg", "Weight > 80 kg"); } },
      { m: "60", s: "10", e: "ile", a: "0.96", l: function () { return t3("Temps per al 96 %", "Tiempo para el 96 %", "Time for 96%"); } },
      { m: "250", s: "50", e: "ige", a: "0.4", l: function () { return t3("Truites: el 40 % millor", "Truchas: el 40 % mejor", "Trout: top 40%"); } }
    ];
    presetBtns($(w, "presets"), function () { return PRE.map(function (p) { return p.l(); }); }, function (i) {
      var p = PRE[i]; $(w, "m").value = p.m; $(w, "s").value = p.s; se.value = p.e; $(w, "a").value = p.a; if (p.b) $(w, "b").value = p.b; draw();
    })[0].classList.add("on");
    fillSelect(se, NEV()); se.value = "ab";
    ["m", "s", "a", "b"].forEach(function (r) { $(w, r).addEventListener("input", draw); }); se.addEventListener("change", draw);
    function draw() {
      var m = num($(w, "m").value), s = num($(w, "s").value), e = se.value, a = num($(w, "a").value), b = num($(w, "b").value);
      $(w, "lb").style.display = e === "ab" ? "" : "none";
      $(w, "la").firstChild.textContent = e[0] === "i" ? "p = " : "";
      if (isNaN(m) || !(s > 0) || isNaN(a) || (e === "ab" && isNaN(b)) || (e[0] === "i" && !(a > 0 && a < 1))) { info.innerHTML = "<p class='chk no'>" + t3("Revisa les dades.", "Revisa los datos.", "Check the data.") + "</p>"; return; }
      var r = normCalc(m, s, e, a, b);
      info.innerHTML = r.h;
      var ticks = [[m, td(m, 3).replace("{,}", ","), true]];
      if (e === "ab") { ticks.push([a, decS(a, 3)], [b, decS(b, 3)]); } else if (e[0] === "i") ticks.push([r.P, "k"]); else ticks.push([a, decS(a, 3)]);
      normPlot(svg, { m: m, s: s, x0: m - 3.8 * s, x1: m + 3.8 * s, shade: r.shade, ticks: ticks });
    }
    onLang(function () { fillSelect(se, NEV()); draw(); });
  }

  /* ---------- aproximació binomial-normal ---------- */
  function aproxCalc(n, p, ev, a, b) {
    var m = n * p, s = Math.sqrt(n * p * (1 - p)), lo, hi, h = "";
    if (ev === "eq") { lo = a - 0.5; hi = a + 0.5; } else if (ev === "le") { lo = -1e9; hi = a + 0.5; } else if (ev === "lt") { lo = -1e9; hi = a - 0.5; }
    else if (ev === "ge") { lo = a - 0.5; hi = 1e9; } else if (ev === "gt") { lo = a + 0.5; hi = 1e9; } else { lo = a - 0.5; hi = b + 0.5; }
    var ok = m >= 5 && n * (1 - p) >= 5;
    h += "<p>" + tex("np=" + td(m, 3) + ",\\ nq=" + td(n - m, 3)) + (ok ? " ✓" : " <span class='chk no'>" + t3("l'aproximació no és bona", "la aproximación no es buena", "the approximation is poor") + "</span>") + "</p>";
    h += "<p>" + tex("X'\\sim N(" + td(m, 3) + ";\\," + td(s, 4) + ")") + "</p>";
    var P, zl = r2((lo - m) / s), zh = r2((hi - m) / s), nt;
    function zf(x) { return "\\frac{" + td(x, 4) + "-" + td(m, 3) + "}{" + td(s, 4) + "}\\approx " + td(r2((x - m) / s), 2); }
    if (lo < -1e8) { P = F(zh); nt = "P(X'\\leq " + td(hi, 1) + ")=P(Z\\leq " + td(zh, 2) + ")"; h += "<p>" + tex("z=" + zf(hi)) + "</p>"; }
    else if (hi > 1e8) { P = 1 - F(zl); nt = "P(X'\\geq " + td(lo, 1) + ")=P(Z\\geq " + td(zl, 2) + ")"; h += "<p>" + tex("z=" + zf(lo)) + "</p>"; }
    else { P = F(zh) - F(zl); nt = "P(" + td(lo, 1) + "\\leq X'\\leq " + td(hi, 1) + ")=P(" + td(zl, 2) + "\\leq Z\\leq " + td(zh, 2) + ")"; h += "<p>" + tex("z_1=" + zf(lo) + ",\\ z_2=" + zf(hi)) + "</p>"; }
    h += "<p>" + tex(bEvTex(ev, a, b) + "\\approx " + nt) + "</p><p class='big-p'>" + tex("\\approx " + f4(P)) + "</p>";
    return { P: P, h: h, shade: [lo, hi], m: m, s: s };
  }
  function wAprox() {
    var w = document.getElementById("w-aprox"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), ev = $(w, "ev");
    fillSelect(ev, BEV); ev.value = "le";
    ["n", "p", "a", "b"].forEach(function (r) { $(w, r).addEventListener("input", draw); }); ev.addEventListener("change", draw);
    function draw() {
      var n = +$(w, "n").value, p = +$(w, "p").value, a = Math.round(num($(w, "a").value)), b = Math.round(num($(w, "b").value)), e = ev.value;
      $(w, "nv").textContent = n; $(w, "pv").textContent = decS(p, 2); $(w, "lb").style.display = e === "ab" ? "" : "none";
      if (isNaN(a) || (e === "ab" && isNaN(b))) return;
      var ex = 0, f = bset(e, a, b); for (var k = 0; k <= n; k++) if (f(k)) ex += pmf(n, p, k);
      var r = aproxCalc(n, p, e, a, b);
      info.innerHTML = "<p>" + tex("X\\sim B(" + n + ";\\," + td(p, 2) + ")") + "</p>" + r.h +
        "<p>" + t3("Valor exacte (binomial): ", "Valor exacto (binomial): ", "Exact value (binomial): ") + tex(f4(ex)) + " · " + t3("diferència: ", "diferencia: ", "difference: ") + tex(f4(Math.abs(ex - r.P))) + "</p>";
      barsPlot(svg, n, p, f, { shade: r.shade });
    }
    onLang(function () { fillSelect(ev, BEV); draw(); });
  }

  /* ---------- calculadora ---------- */
  function wLab() {
    var w = document.getElementById("w-lab"); if (!w) return;
    var svg = w.querySelector("svg"), out = $(w, "out"), ev = $(w, "ev"), dist = "B";
    var inp1 = $(w, "x1"), inp2 = $(w, "x2"), l1 = $(w, "l1"), l2 = $(w, "l2");
    var bs = ["B", "N"].map(function (d) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { dist = d; inp1.value = d === "B" ? "20" : "100"; inp2.value = d === "B" ? "0.3" : "15"; $(w, "a").value = d === "B" ? "5" : "110"; $(w, "b").value = d === "B" ? "8" : "130"; opts(); draw(); });
      $(w, "dist").appendChild(b); return b;
    });
    function opts() {
      bs[0].textContent = "Binomial"; bs[1].textContent = "Normal";
      bs.forEach(function (b, i) { b.classList.toggle("on", (i === 0) === (dist === "B")); });
      l1.innerHTML = tex(dist === "B" ? "n=" : "\\mu=") + " "; l1.appendChild(inp1);
      l2.innerHTML = tex(dist === "B" ? "p=" : "\\sigma=") + " "; l2.appendChild(inp2);
      fillSelect(ev, dist === "B" ? BEV : NEV());
    }
    ["a", "b"].forEach(function (r) { $(w, r).addEventListener("input", draw); }); [inp1, inp2].forEach(function (i) { i.addEventListener("input", draw); }); ev.addEventListener("change", draw);
    function draw() {
      var x1 = num(inp1.value), x2 = num(inp2.value), e = ev.value, a = num($(w, "a").value), b = num($(w, "b").value);
      $(w, "lb").style.display = e === "ab" ? "" : "none";
      if (dist === "B") {
        var n = Math.round(x1), p = x2;
        if (!(n >= 1 && n <= 2000) || !(p > 0 && p < 1) || isNaN(a) || (e === "ab" && isNaN(b))) { out.innerHTML = "<p class='chk no'>" + t3("Revisa les dades (1 ≤ n ≤ 2000, 0 < p < 1).", "Revisa los datos (1 ≤ n ≤ 2000, 0 < p < 1).", "Check the data (1 ≤ n ≤ 2000, 0 < p < 1).") + "</p>"; return; }
        a = Math.round(a); b = Math.round(b);
        var h = "";
        if (n <= 60) { var r = binCalc(n, p, e, a, b); h = r.h; }
        else { var ex = 0, f = bset(e, a, b); for (var k = 0; k <= n; k++) if (f(k)) ex += pmf(n, p, k); h = "<p>" + tex("X\\sim B(" + n + ";\\," + td(p, 4) + ")") + "</p><p>" + t3("Valor exacte (sumant amb ordinador): ", "Valor exacto (sumando con ordenador): ", "Exact value (computer sum): ") + tex(f4(ex)) + "</p>"; }
        if (n * p >= 5 && n * (1 - p) >= 5) { var ap = aproxCalc(n, p, e, a, b); h += "<h4>" + t3("Aproximació normal", "Aproximación normal", "Normal approximation") + "</h4>" + ap.h; barsPlot(svg, n, p, bset(e, a, b), { shade: ap.shade }); }
        else barsPlot(svg, n, p, bset(e, a, b));
        out.innerHTML = h;
      } else {
        var m = x1, s = x2;
        if (isNaN(m) || !(s > 0) || isNaN(a) || (e === "ab" && isNaN(b)) || (e[0] === "i" && !(a > 0 && a < 1))) { out.innerHTML = "<p class='chk no'>" + t3("Revisa les dades.", "Revisa los datos.", "Check the data.") + "</p>"; return; }
        var rn = normCalc(m, s, e, a, b);
        out.innerHTML = rn.h;
        normPlot(svg, { m: m, s: s, x0: m - 3.8 * s, x1: m + 3.8 * s, shade: rn.shade, ticks: [[m, "μ", true]] });
      }
    }
    onLang(function () { opts(); draw(); });
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("Quina d'aquestes variables aleatòries és contínua?", "¿Cuál de estas variables aleatorias es continua?", "Which of these random variables is continuous?"),
      o: [q3("El nombre de fills d'una família", "El número de hijos de una familia", "The number of children in a family"), q3("El temps d'espera en una cua", "El tiempo de espera en una cola", "The waiting time in a queue"), q3("La suma de dos daus", "La suma de dos dados", "The sum of two dice")], a: 1,
      e: q3("El temps és una mesura: pot prendre qualsevol valor d'un interval.", "El tiempo es una medida: puede tomar cualquier valor de un intervalo.", "Time is a measurement: it can take any value in an interval.") },
    { q: q3("$X$ pren els valors 0, 1 i 2 amb probabilitats $0{,}2$, $0{,}5$ i $k$. Quant val $k$?", "$X$ toma los valores 0, 1 y 2 con probabilidades $0{,}2$, $0{,}5$ y $k$. ¿Cuánto vale $k$?", "$X$ takes the values 0, 1 and 2 with probabilities $0.2$, $0.5$ and $k$. What is $k$?"),
      o: [q3("$0{,}3$", "$0{,}3$", "$0.3$"), q3("$0{,}7$", "$0{,}7$", "$0.7$"), q3("$2$")], a: 0, e: q3("Les probabilitats sumen 1: $k=1-0{,}7=0{,}3$.", "Las probabilidades suman 1: $k=1-0{,}7=0{,}3$.", "The probabilities add up to 1: $k=1-0.7=0.3$.") },
    { q: q3("Amb la variable anterior ($p_i=0{,}2;\\ 0{,}5;\\ 0{,}3$), la mitjana és…", "Con la variable anterior ($p_i=0{,}2;\\ 0{,}5;\\ 0{,}3$), la media es…", "With the previous variable ($p_i=0.2,\\ 0.5,\\ 0.3$), the mean is…"),
      o: [q3("$1$"), q3("$1{,}1$", "$1{,}1$", "$1.1$"), q3("$0{,}5$", "$0{,}5$", "$0.5$")], a: 1, e: q3("$\\mu=0\\cdot0{,}2+1\\cdot0{,}5+2\\cdot0{,}3=1{,}1$.", "$\\mu=0\\cdot0{,}2+1\\cdot0{,}5+2\\cdot0{,}3=1{,}1$.", "$\\mu=0\\cdot0.2+1\\cdot0.5+2\\cdot0.3=1.1$.") },
    { q: q3("Si $X$ és el guany d'un joc, el joc és just quan…", "Si $X$ es la ganancia de un juego, el juego es justo cuando…", "If $X$ is the gain in a game, the game is fair when…"),
      o: [q3("$\\mu=0$"), q3("$\\sigma=0$"), q3("$P(X\\gt0)=0{,}5$", "$P(X\\gt0)=0{,}5$", "$P(X\\gt0)=0.5$")], a: 0, e: q3("A la llarga, ni es guanya ni es perd: el guany esperat és 0.", "A la larga, ni se gana ni se pierde: la ganancia esperada es 0.", "In the long run you neither win nor lose: the expected gain is 0.") },
    { q: q3("Quina d'aquestes variables és binomial?", "¿Cuál de estas variables es binomial?", "Which of these variables is binomial?"),
      o: [q3("L'altura d'un alumne", "La altura de un alumno", "A student's height"), q3("El nombre de sisos en 10 llançaments d'un dau", "El número de seises en 10 lanzamientos de un dado", "The number of sixes in 10 rolls of a die"), q3("El nombre de boles roges en 3 extraccions sense reemplaçament d'una urna amb 5 boles", "El número de bolas rojas en 3 extracciones sin reemplazamiento de una urna con 5 bolas", "The number of red balls in 3 draws without replacement from an urn with 5 balls")], a: 1,
      e: q3("10 proves independents amb la mateixa $p=\\frac16$. L'altura és contínua i, sense reemplaçament, la $p$ canvia.", "10 pruebas independientes con la misma $p=\\frac16$. La altura es continua y, sin reemplazamiento, la $p$ cambia.", "10 independent trials with the same $p=\\frac16$. Height is continuous and, without replacement, $p$ changes.") },
    { q: q3("Si $X\\sim B(10;\\,0{,}3)$, la mitjana és…", "Si $X\\sim B(10;\\,0{,}3)$, la media es…", "If $X\\sim B(10;\\,0.3)$, the mean is…"),
      o: [q3("$3$"), q3("$0{,}3$", "$0{,}3$", "$0.3$"), q3("$2{,}1$", "$2{,}1$", "$2.1$")], a: 0, e: q3("$\\mu=np=10\\cdot0{,}3=3$.", "$\\mu=np=10\\cdot0{,}3=3$.", "$\\mu=np=10\\cdot0.3=3$.") },
    { q: q3("Amb la taula, si $X\\sim B(5;\\,0{,}20)$, $P(X=1)$ val…", "Con la tabla, si $X\\sim B(5;\\,0{,}20)$, $P(X=1)$ vale…", "Using the table, if $X\\sim B(5;\\,0.20)$, $P(X=1)$ is…"),
      o: [q3("$0{,}3277$", "$0{,}3277$", "$0.3277$"), q3("$0{,}4096$", "$0{,}4096$", "$0.4096$"), q3("$0{,}2$", "$0{,}2$", "$0.2$")], a: 1, e: q3("$\\binom51\\,0{,}2\\cdot0{,}8^4=0{,}4096$ (bloc $n=5$, fila $x=1$).", "$\\binom51\\,0{,}2\\cdot0{,}8^4=0{,}4096$ (bloque $n=5$, fila $x=1$).", "$\\binom51\\,0.2\\cdot0.8^4=0.4096$ (block $n=5$, row $x=1$).") },
    { q: q3("Si $X\\sim B(6;\\,0{,}8)$, per a fer servir la taula calculem $P(X=6)$ com…", "Si $X\\sim B(6;\\,0{,}8)$, para usar la tabla calculamos $P(X=6)$ como…", "If $X\\sim B(6;\\,0.8)$, to use the table we compute $P(X=6)$ as…"),
      o: [q3("$P(Y=6)$ amb $Y\\sim B(6;\\,0{,}2)$", "$P(Y=6)$ con $Y\\sim B(6;\\,0{,}2)$", "$P(Y=6)$ with $Y\\sim B(6;\\,0.2)$"), q3("$P(Y=0)$ amb $Y\\sim B(6;\\,0{,}2)$", "$P(Y=0)$ con $Y\\sim B(6;\\,0{,}2)$", "$P(Y=0)$ with $Y\\sim B(6;\\,0.2)$"), q3("$1-P(X=0)$")], a: 1,
      e: q3("6 èxits són 0 fracassos: $P(Y=0)=0{,}2621$.", "6 éxitos son 0 fracasos: $P(Y=0)=0{,}2621$.", "6 successes means 0 failures: $P(Y=0)=0.2621$.") },
    { q: q3("Si $X\\sim U(0,10)$ (uniforme), $P(X\\leq3)$ val…", "Si $X\\sim U(0,10)$ (uniforme), $P(X\\leq3)$ vale…", "If $X\\sim U(0,10)$ (uniform), $P(X\\leq3)$ is…"),
      o: [q3("$0{,}03$", "$0{,}03$", "$0.03$"), q3("$0{,}3$", "$0{,}3$", "$0.3$"), q3("$3$")], a: 1, e: q3("Rectangle de base 3 i altura $\\frac1{10}$: $\\frac3{10}$.", "Rectángulo de base 3 y altura $\\frac1{10}$: $\\frac3{10}$.", "Rectangle of base 3 and height $\\frac1{10}$: $\\frac3{10}$.") },
    { q: q3("$f(x)=k$ en $[0,5]$ (i 0 fora) és una funció de densitat si $k$ val…", "$f(x)=k$ en $[0,5]$ (y 0 fuera) es una función de densidad si $k$ vale…", "$f(x)=k$ on $[0,5]$ (and 0 elsewhere) is a density function if $k$ is…"),
      o: [q3("$5$"), q3("$1$"), q3("$0{,}2$", "$0{,}2$", "$0.2$")], a: 2, e: q3("L'àrea total ha de ser 1: $5k=1$.", "El área total tiene que ser 1: $5k=1$.", "The total area must be 1: $5k=1$.") },
    { q: q3("En una variable contínua, $P(X=5)$ és…", "En una variable continua, $P(X=5)$ es…", "For a continuous variable, $P(X=5)$ is…"),
      o: [q3("$0$"), q3("$f(5)$"), q3("$P(X\\leq5)$")], a: 0, e: q3("L'àrea d'una línia és 0.", "El área de una línea es 0.", "The area over a single point is 0.") },
    { q: q3("En una normal $N(\\mu,\\sigma)$, quin percentatge aproximat de valors hi ha entre $\\mu-2\\sigma$ i $\\mu+2\\sigma$?", "En una normal $N(\\mu,\\sigma)$, ¿qué porcentaje aproximado de valores hay entre $\\mu-2\\sigma$ y $\\mu+2\\sigma$?", "In a normal $N(\\mu,\\sigma)$, roughly what percentage of values lies between $\\mu-2\\sigma$ and $\\mu+2\\sigma$?"),
      o: [q3("68 %", "68 %", "68%"), q3("95 %", "95 %", "95%"), q3("99,7 %", "99,7 %", "99.7%")], a: 1, e: q3("Regla 68–95–99,7: $2\\cdot0{,}9772-1\\approx0{,}95$.", "Regla 68–95–99,7: $2\\cdot0{,}9772-1\\approx0{,}95$.", "68–95–99.7 rule: $2\\cdot0.9772-1\\approx0.95$.") },
    { q: q3("Si $Z\\sim N(0,1)$, $P(Z\\geq1)$ val…", "Si $Z\\sim N(0,1)$, $P(Z\\geq1)$ vale…", "If $Z\\sim N(0,1)$, $P(Z\\geq1)$ is…"),
      o: [q3("$0{,}8413$", "$0{,}8413$", "$0.8413$"), q3("$0{,}1587$", "$0{,}1587$", "$0.1587$"), q3("$0{,}3413$", "$0{,}3413$", "$0.3413$")], a: 1, e: q3("$1-P(Z\\leq1)=1-0{,}8413$.", "$1-P(Z\\leq1)=1-0{,}8413$.", "$1-P(Z\\leq1)=1-0.8413$.") },
    { q: q3("$P(Z\\leq-0{,}5)$ és igual a…", "$P(Z\\leq-0{,}5)$ es igual a…", "$P(Z\\leq-0.5)$ equals…"),
      o: [q3("$-P(Z\\leq0{,}5)$", "$-P(Z\\leq0{,}5)$", "$-P(Z\\leq0.5)$"), q3("$1-P(Z\\leq0{,}5)$", "$1-P(Z\\leq0{,}5)$", "$1-P(Z\\leq0.5)$"), q3("$P(Z\\leq0{,}5)-0{,}5$", "$P(Z\\leq0{,}5)-0{,}5$", "$P(Z\\leq0.5)-0.5$")], a: 1, e: q3("Per simetria: $1-0{,}6915=0{,}3085$.", "Por simetría: $1-0{,}6915=0{,}3085$.", "By symmetry: $1-0.6915=0.3085$.") },
    { q: q3("Si $X\\sim N(50,10)$, el valor tipificat de $x=65$ és…", "Si $X\\sim N(50,10)$, el valor tipificado de $x=65$ es…", "If $X\\sim N(50,10)$, the standardised value of $x=65$ is…"),
      o: [q3("$6{,}5$", "$6{,}5$", "$6.5$"), q3("$1{,}5$", "$1{,}5$", "$1.5$"), q3("$15$")], a: 1, e: q3("$z=\\frac{65-50}{10}=1{,}5$.", "$z=\\frac{65-50}{10}=1{,}5$.", "$z=\\frac{65-50}{10}=1.5$.") },
    { q: q3("Si $X\\sim N(100,15)$, quin valor deixa per davall el 90 % dels casos?", "Si $X\\sim N(100,15)$, ¿qué valor deja por debajo el 90 % de los casos?", "If $X\\sim N(100,15)$, which value has 90% of cases below it?"),
      o: [q3("$119{,}2$", "$119{,}2$", "$119.2$"), q3("$115$"), q3("$128$")], a: 0, e: q3("$z\\approx1{,}28$: $100+1{,}28\\cdot15=119{,}2$.", "$z\\approx1{,}28$: $100+1{,}28\\cdot15=119{,}2$.", "$z\\approx1.28$: $100+1.28\\cdot15=119.2$.") },
    { q: q3("Quina d'aquestes binomials es pot aproximar bé per una normal?", "¿Cuál de estas binomiales se puede aproximar bien por una normal?", "Which of these binomials can be well approximated by a normal?"),
      o: [q3("$B(100;\\,0{,}02)$", "$B(100;\\,0{,}02)$", "$B(100;\\,0.02)$"), q3("$B(8;\\,0{,}5)$", "$B(8;\\,0{,}5)$", "$B(8;\\,0.5)$"), q3("$B(50;\\,0{,}4)$", "$B(50;\\,0{,}4)$", "$B(50;\\,0.4)$")], a: 2,
      e: q3("Cal $np\\geq5$ i $nq\\geq5$: $50\\cdot0{,}4=20$ i $50\\cdot0{,}6=30$. En les altres, $np=2$ o $np=4$.", "Hace falta $np\\geq5$ y $nq\\geq5$: $50\\cdot0{,}4=20$ y $50\\cdot0{,}6=30$. En las otras, $np=2$ o $np=4$.", "We need $np\\geq5$ and $nq\\geq5$: $50\\cdot0.4=20$ and $50\\cdot0.6=30$. In the others, $np=2$ or $np=4$.") },
    { q: q3("Per a aproximar $P(X\\leq40)$ amb $X\\sim B(100;\\,0{,}5)$ calculem…", "Para aproximar $P(X\\leq40)$ con $X\\sim B(100;\\,0{,}5)$ calculamos…", "To approximate $P(X\\leq40)$ with $X\\sim B(100;\\,0.5)$ we compute…"),
      o: [q3("$P(X'\\leq39{,}5)$", "$P(X'\\leq39{,}5)$", "$P(X'\\leq39.5)$"), q3("$P(X'\\leq40{,}5)$", "$P(X'\\leq40{,}5)$", "$P(X'\\leq40.5)$"), q3("$P(X'\\leq40)$")], a: 1, e: q3("La barra del 40 va fins a 40,5. $X'\\sim N(50,5)$: $P(Z\\leq-1{,}9)=0{,}0287$.", "La barra del 40 va hasta 40,5. $X'\\sim N(50,5)$: $P(Z\\leq-1{,}9)=0{,}0287$.", "The bar for 40 extends to 40.5. $X'\\sim N(50,5)$: $P(Z\\leq-1.9)=0.0287$.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Distribucions de probabilitat · FentMates", es: "Distribuciones de probabilidad · FentMates", en: "Probability distributions · FentMates" };
  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l; root.setAttribute("data-lang", l); root.lang = HTML_LANG[l]; document.title = TITLES[l]; store("lang", l);
    try { var url = new URL(location.href); if (url.searchParams.has("lang")) { url.searchParams.set("lang", l); history.replaceState(null, "", url); } } catch (e) {}
    refreshers.forEach(function (fn) { fn(); });
  }

  function init() {
    document.title = TITLES[lang];
    readTables();
    var Dl = [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }];
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, { delimiters: Dl, ignoredClasses: ["widget", "lab"], throwOnError: false });
      document.querySelectorAll(".widget .wt, .widget label, .widget .legend, .widget > p, .lab .bh, .lab p, .lab label").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wFigs, wDisc, wBin, wTbin, wDens, wNorm, wTz, wTip, wAprox, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM10 = { wDisc: wDisc, wDens: wDens, F: F, zinv: zinv, pmf: pmf, BT: BT, normCalc: normCalc, aproxCalc: aproxCalc };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
