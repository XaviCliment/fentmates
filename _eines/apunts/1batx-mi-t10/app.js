(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1batx-mi-u10-estadistica-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { regL: "Recta de regressió de Y sobre X", est: "Estimació", estGood: "És una estimació fiable (|r| prop d'1 i x dins de les dades).", estMid: "L'estimació és poc precisa: la correlació només és moderada.", estBad: "No és fiable: la correlació és massa feble.", estOut: "Compte: x queda fora de l'interval de les dades (extrapolació), no és fiable.", pReg: ["Exemple resolt", "Preu i vendes", "Hores i notes", "Sense relació"], next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt",
      bad: "Revisa les dades: escriu nombres separats per espais o per punt i coma (per exemple 3 5 5 7 o 3:4; 5:2).", bad2: "Les dues llistes han de tindre el mateix nombre de valors (com a mínim 2).",
      val: "Valor", fi: "f<sub>i</sub>", Fi: "F<sub>i</sub>", hi: "h<sub>i</sub>", Hi: "H<sub>i</sub>", pct: "%", total: "Total",
      mean: "Mitjana", median: "Mediana", mode: "Moda", q1: "Primer quartil", q3: "Tercer quartil", range: "Rang", vari: "Variància", sd: "Desviació típica", cv: "Coeficient de variació",
      pairs: "parells", cov: "Covariància", r: "Coeficient de correlació", strong: "forta", moderate: "moderada", weak: "feble", none: "pràcticament nul·la",
      pos: "positiva (directa)", neg: "negativa (inversa)", corr: "Correlació", noCorr: "No hi ha correlació lineal", noVar: "Una de les variables no varia: r no està definit.",
      clickAdd: "Fes clic al gràfic per afegir un punt; clic sobre un punt per llevar-lo.", clear: "Esborra", points: "punts",
      guessQ: "Quin és el coeficient de correlació d'aquest núvol?", newCloud: "Un altre núvol", wasR: "El coeficient és", hits: "Encerts",
      margX: "Distribució marginal de X", margY: "Distribució marginal de Y", sums: "Sumes",
      pUni: ["Notes (20 alumnes)", "Valors repetits", "Dades soltes"], pPairs: ["Hores i notes", "Exemple resolt", "Correlació negativa", "Sense relació", "Parabòlica"], pCloud: ["Buit", "Creixent", "Decreixent", "Núvol rodó"] },
    es: { regL: "Recta de regresión de Y sobre X", est: "Estimación", estGood: "Es una estimación fiable (|r| cerca de 1 y x dentro de los datos).", estMid: "La estimación es poco precisa: la correlación solo es moderada.", estBad: "No es fiable: la correlación es demasiado débil.", estOut: "Cuidado: x queda fuera del intervalo de los datos (extrapolación), no es fiable.", pReg: ["Ejemplo resuelto", "Precio y ventas", "Horas y notas", "Sin relación"], next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba",
      bad: "Revisa los datos: escribe números separados por espacios o por punto y coma (por ejemplo 3 5 5 7 o 3:4; 5:2).", bad2: "Las dos listas deben tener el mismo número de valores (como mínimo 2).",
      val: "Valor", fi: "f<sub>i</sub>", Fi: "F<sub>i</sub>", hi: "h<sub>i</sub>", Hi: "H<sub>i</sub>", pct: "%", total: "Total",
      mean: "Media", median: "Mediana", mode: "Moda", q1: "Primer cuartil", q3: "Tercer cuartil", range: "Rango", vari: "Varianza", sd: "Desviación típica", cv: "Coeficiente de variación",
      pairs: "pares", cov: "Covarianza", r: "Coeficiente de correlación", strong: "fuerte", moderate: "moderada", weak: "débil", none: "prácticamente nula",
      pos: "positiva (directa)", neg: "negativa (inversa)", corr: "Correlación", noCorr: "No hay correlación lineal", noVar: "Una de las variables no varía: r no está definido.",
      clickAdd: "Haz clic en el gráfico para añadir un punto; clic sobre un punto para quitarlo.", clear: "Borrar", points: "puntos",
      guessQ: "¿Cuál es el coeficiente de correlación de esta nube?", newCloud: "Otra nube", wasR: "El coeficiente es", hits: "Aciertos",
      margX: "Distribución marginal de X", margY: "Distribución marginal de Y", sums: "Sumas",
      pUni: ["Notas (20 alumnos)", "Valores repetidos", "Datos sueltos"], pPairs: ["Horas y notas", "Ejemplo resuelto", "Correlación negativa", "Sin relación", "Parabólica"], pCloud: ["Vacío", "Creciente", "Decreciente", "Nube redonda"] },
    en: { regL: "Regression line of Y on X", est: "Estimate", estGood: "It is a reliable estimate (|r| close to 1 and x within the data).", estMid: "The estimate is not very precise: the correlation is only moderate.", estBad: "Not reliable: the correlation is too weak.", estOut: "Careful: x lies outside the range of the data (extrapolation), so it is not reliable.", pReg: ["Worked example", "Price and sales", "Hours and marks", "No relation"], next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Score", right: "Correct!", wrong: "Not correct.", theme: "Switch between light and dark mode", top: "Back to top",
      bad: "Check the data: type numbers separated by spaces or semicolons (for example 3 5 5 7 or 3:4; 5:2).", bad2: "Both lists must have the same number of values (at least 2).",
      val: "Value", fi: "f<sub>i</sub>", Fi: "F<sub>i</sub>", hi: "h<sub>i</sub>", Hi: "H<sub>i</sub>", pct: "%", total: "Total",
      mean: "Mean", median: "Median", mode: "Mode", q1: "First quartile", q3: "Third quartile", range: "Range", vari: "Variance", sd: "Standard deviation", cv: "Coefficient of variation",
      pairs: "pairs", cov: "Covariance", r: "Correlation coefficient", strong: "strong", moderate: "moderate", weak: "weak", none: "practically zero",
      pos: "positive (direct)", neg: "negative (inverse)", corr: "Correlation", noCorr: "There is no linear correlation", noVar: "One of the variables does not vary: r is undefined.",
      clickAdd: "Click on the chart to add a point; click on a point to remove it.", clear: "Clear", points: "points",
      guessQ: "What is the correlation coefficient of this cloud?", newCloud: "Another cloud", wasR: "The coefficient is", hits: "Hits",
      margX: "Marginal distribution of X", margY: "Marginal distribution of Y", sums: "Sums",
      pUni: ["Marks (20 students)", "Repeated values", "Raw data"], pPairs: ["Hours and marks", "Worked example", "Negative correlation", "No relation", "Parabolic"], pCloud: ["Empty", "Increasing", "Decreasing", "Round cloud"] }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }

  /* ---------- nombres ---------- */
  // fmt: arredoneix a d decimals, lleva zeros finals i usa la coma decimal (punt en anglés)
  function fmt(v, d) {
    if (!isFinite(v)) return "—";
    d = d == null ? 4 : d;
    var s = (Math.round(v * Math.pow(10, d)) / Math.pow(10, d)).toFixed(d).replace(/\.?0+$/, "");
    if (s === "-0") s = "0";
    return lang === "en" ? s : s.replace(".", "{,}");
  }
  function ft(v, d) { return fmt(v, d).replace("{,}", ","); } // per a text HTML (fora de KaTeX)
  function num(s) { s = String(s).trim().replace(",", "."); if (!/^[-+]?(\d+\.?\d*|\.\d+)$/.test(s)) return NaN; return parseFloat(s); }
  // llista: "3 5 5 7", "3; 5; 7" o amb freqüències "3:4; 5:2"
  function readList(s) {
    var toks = String(s).trim().split(/[\s;]+/).filter(Boolean), vals = [];
    for (var i = 0; i < toks.length; i++) {
      var p = toks[i].split(":");
      var v = num(p[0]), f = p.length > 1 ? num(p[1]) : 1;
      if (!isFinite(v) || !isFinite(f) || f < 0 || Math.round(f) !== f || p.length > 2) return null;
      for (var k = 0; k < f; k++) vals.push(v);
    }
    return vals.length ? vals : null;
  }
  function readNums(s) {
    var toks = String(s).trim().split(/[\s;]+/).filter(Boolean), out = [];
    for (var i = 0; i < toks.length; i++) { var v = num(toks[i]); if (!isFinite(v)) return null; out.push(v); }
    return out;
  }

  /* ---------- estadística ---------- */
  function freqTable(vals) {
    var m = {}; vals.forEach(function (v) { m[v] = (m[v] || 0) + 1; });
    var xs = Object.keys(m).map(Number).sort(function (a, b) { return a - b; }), N = vals.length, F = 0;
    return xs.map(function (x) { F += m[x]; return { x: x, f: m[x], F: F, h: m[x] / N, H: F / N }; });
  }
  // percentil a la manera dels apunts: el primer valor amb F_i ≥ k·N; si F_i = k·N exactament, la mitjana amb el següent
  function quant(T, N, k) {
    var pos = k * N;
    for (var i = 0; i < T.length; i++) {
      if (Math.abs(T[i].F - pos) < 1e-9 && i + 1 < T.length) return (T[i].x + T[i + 1].x) / 2;
      if (T[i].F > pos - 1e-9) return T[i].x;
    }
    return T[T.length - 1].x;
  }
  function uniStats(vals) {
    var T = freqTable(vals), N = vals.length, s = 0, s2 = 0;
    T.forEach(function (r) { s += r.x * r.f; s2 += r.x * r.x * r.f; });
    var mean = s / N, v = s2 / N - mean * mean; if (Math.abs(v) < 1e-12) v = 0;
    var fmax = Math.max.apply(null, T.map(function (r) { return r.f; }));
    return { T: T, N: N, s: s, s2: s2, mean: mean, v: v, sd: Math.sqrt(v), med: quant(T, N, 0.5), q1: quant(T, N, 0.25), q3: quant(T, N, 0.75),
      modes: T.filter(function (r) { return r.f === fmax; }).map(function (r) { return r.x; }), min: T[0].x, max: T[T.length - 1].x };
  }
  function biStats(x, y) {
    var N = x.length, sx = 0, sy = 0, sx2 = 0, sy2 = 0, sxy = 0;
    for (var i = 0; i < N; i++) { sx += x[i]; sy += y[i]; sx2 += x[i] * x[i]; sy2 += y[i] * y[i]; sxy += x[i] * y[i]; }
    var mx = sx / N, my = sy / N, vx = sx2 / N - mx * mx, vy = sy2 / N - my * my, c = sxy / N - mx * my;
    if (Math.abs(vx) < 1e-12) vx = 0; if (Math.abs(vy) < 1e-12) vy = 0;
    var r = vx > 0 && vy > 0 ? c / Math.sqrt(vx * vy) : NaN;
    return { N: N, sx: sx, sy: sy, sx2: sx2, sy2: sy2, sxy: sxy, mx: mx, my: my, vx: vx, vy: vy, c: c, r: Math.max(-1, Math.min(1, r)) };
  }
  function rWords(r) {
    if (!isFinite(r)) return u("noVar");
    var a = Math.abs(r), k = a >= 0.8 ? "strong" : a >= 0.5 ? "moderate" : a >= 0.2 ? "weak" : "none";
    if (k === "none") return u("noCorr") + " (" + u("corr").toLowerCase() + " " + u("none") + ")";
    return u("corr") + " " + u(r > 0 ? "pos" : "neg") + " " + u(k) + (a > 0.995 ? " (" + (lang === "en" ? "almost exact" : lang === "es" ? "casi exacta" : "gairebé exacta") + ")" : "");
  }

  /* ---------- núvol de punts (SVG) ---------- */
  var W = 340, H = 260, ML = 38, MR = 12, MT = 12, MB = 30;
  function nice(lo, hi) {
    if (hi - lo < 1e-9) { lo -= 1; hi += 1; }
    var span = hi - lo, step = Math.pow(10, Math.floor(Math.log10(span / 5)));
    [1, 2, 5, 10].some(function (k) { if (span / (step * k) <= 6) { step *= k; return true; } return false; });
    return { lo: Math.floor(lo / step) * step, hi: Math.ceil(hi / step) * step, step: step };
  }
  // opts: {xr:[a,b], yr:[a,b], means:true, axes:["X","Y"], hl: índex}
  function cloud(svg, pts, opts) {
    opts = opts || {};
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; });
    var ax = opts.xr ? { lo: opts.xr[0], hi: opts.xr[1], step: opts.xr[2] || nice(opts.xr[0], opts.xr[1]).step } : nice(Math.min.apply(null, xs.concat([0])), Math.max.apply(null, xs.concat([1])));
    var ay = opts.yr ? { lo: opts.yr[0], hi: opts.yr[1], step: opts.yr[2] || nice(opts.yr[0], opts.yr[1]).step } : nice(Math.min.apply(null, ys.concat([0])), Math.max.apply(null, ys.concat([1])));
    function X(v) { return ML + (v - ax.lo) / (ax.hi - ax.lo) * (W - ML - MR); }
    function Y(v) { return H - MB - (v - ay.lo) / (ay.hi - ay.lo) * (H - MT - MB); }
    var h = '<rect class="bg" x="' + ML + '" y="' + MT + '" width="' + (W - ML - MR) + '" height="' + (H - MT - MB) + '"/>', v;
    for (v = ax.lo; v <= ax.hi + 1e-9; v += ax.step) h += '<line class="grid" x1="' + X(v) + '" y1="' + MT + '" x2="' + X(v) + '" y2="' + (H - MB) + '"/><text class="tick" x="' + X(v) + '" y="' + (H - MB + 15) + '" text-anchor="middle">' + ft(v, 3) + "</text>";
    for (v = ay.lo; v <= ay.hi + 1e-9; v += ay.step) h += '<line class="grid" x1="' + ML + '" y1="' + Y(v) + '" x2="' + (W - MR) + '" y2="' + Y(v) + '"/><text class="tick" x="' + (ML - 5) + '" y="' + (Y(v) + 4) + '" text-anchor="end">' + ft(v, 3) + "</text>";
    h += '<line class="axis" x1="' + ML + '" y1="' + (H - MB) + '" x2="' + (W - MR) + '" y2="' + (H - MB) + '"/><line class="axis" x1="' + ML + '" y1="' + MT + '" x2="' + ML + '" y2="' + (H - MB) + '"/>';
    if (opts.axes) h += '<text class="tick lab" x="' + (W - MR) + '" y="' + (H - MB - 5) + '" text-anchor="end">' + opts.axes[0] + '</text><text class="tick lab" x="' + (ML + 5) + '" y="' + (MT + 11) + '">' + opts.axes[1] + "</text>";
    if (opts.means && pts.length > 1) {
      var st = biStats(xs, ys);
      h += '<line class="meanl" x1="' + X(st.mx) + '" y1="' + MT + '" x2="' + X(st.mx) + '" y2="' + (H - MB) + '"/><line class="meanl" x1="' + ML + '" y1="' + Y(st.my) + '" x2="' + (W - MR) + '" y2="' + Y(st.my) + '"/>';
      h += '<circle class="cg" cx="' + X(st.mx) + '" cy="' + Y(st.my) + '" r="5"/>';
    }
    if (opts.reg && pts.length > 1) {
      var R = biStats(xs, ys);
      if (R.vx > 0) {
        var m = R.c / R.vx, f = function (x) { return R.my + m * (x - R.mx); }, xa = ax.lo, xb = ax.hi;
        // retallem la recta a la finestra vertical
        if (m !== 0) { var x1 = R.mx + (ay.lo - R.my) / m, x2 = R.mx + (ay.hi - R.my) / m; xa = Math.max(xa, Math.min(x1, x2)); xb = Math.min(xb, Math.max(x1, x2)); }
        if (xb > xa) h += '<line class="regl" x1="' + X(xa) + '" y1="' + Y(f(xa)) + '" x2="' + X(xb) + '" y2="' + Y(f(xb)) + '"/>';
      }
    }
    if (opts.mark) h += '<circle class="est" cx="' + X(opts.mark[0]) + '" cy="' + Y(opts.mark[1]) + '" r="6"/>';
    pts.forEach(function (p, i) { h += '<circle class="pt' + (opts.hl === i ? " hl" : "") + '" data-i="' + i + '" cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="' + (opts.r || 4.5) + '"/>'; });
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    svg.innerHTML = h;
    return { X: X, Y: Y, ax: ax, ay: ay, inv: function (px, py) { return [ax.lo + (px - ML) / (W - ML - MR) * (ax.hi - ax.lo), ay.lo + (H - MB - py) / (H - MT - MB) * (ay.hi - ay.lo)]; } };
  }
  // generador pseudoaleatori amb llavor i núvols amb un r exacte
  function rng(seed) { var s = seed >>> 0 || 1; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
  function normals(n, rand) { var out = []; while (out.length < n) { var a = rand() || 1e-9, b = rand(); out.push(Math.sqrt(-2 * Math.log(a)) * Math.cos(2 * Math.PI * b)); } return out; }
  function std(a) { var n = a.length, m = a.reduce(function (s, v) { return s + v; }, 0) / n, s2 = a.reduce(function (s, v) { return s + (v - m) * (v - m); }, 0) / n; return a.map(function (v) { return (v - m) / Math.sqrt(s2); }); }
  function cloudR(n, r, seed) {
    var rand = rng(seed), z1 = std(normals(n, rand)), z2 = normals(n, rand);
    var d = z1.reduce(function (s, v, i) { return s + v * z2[i]; }, 0) / n; z2 = std(z2.map(function (v, i) { return v - d * z1[i]; }));
    return z1.map(function (a, i) { return [a, r * a + Math.sqrt(Math.max(0, 1 - r * r)) * z2[i]]; });
  }

  function presetBtns(box, n, key, onPick) {
    var bs = [];
    for (var i = 0; i < n; i++) (function (i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { onPick(i); }); box.appendChild(b); bs.push(b);
    })(i);
    onLang(function () { bs.forEach(function (b, i) { b.textContent = u(key)[i]; }); });
    return bs;
  }
  function table(head, rows, foot) {
    var h = '<div class="tbl-wrap"><table class="data sm st-tbl"><thead><tr>' + head.map(function (c) { return "<th>" + c + "</th>"; }).join("") + "</tr></thead><tbody>";
    rows.forEach(function (r) { h += "<tr>" + r.map(function (c) { return "<td>" + c + "</td>"; }).join("") + "</tr>"; });
    if (foot) h += '<tr class="tot">' + foot.map(function (c) { return "<td>" + c + "</td>"; }).join("") + "</tr>";
    return h + "</tbody></table></div>";
  }
  function K(s) { return tex(s); }

  /* ---------- 10.3 estadística unidimensional ---------- */
  var PRE_UNI = ["3:1; 4:2; 5:4; 6:5; 7:4; 8:3; 9:1", "2 3 3 4 4 4 5 5 6 8", "12,5 14 9,5 11 15 13 10,5 12"];
  function wUni() {
    var w = document.getElementById("w-uni"); if (!w) return;
    var inp = $(w, "d"), out = w.querySelector(".info"), tb = w.querySelector(".vtbl");
    presetBtns($(w, "presets"), PRE_UNI.length, "pUni", function (i) { inp.value = PRE_UNI[i]; draw(); });
    inp.addEventListener("input", draw);
    function draw() {
      var vals = readList(inp.value);
      if (!vals) { inp.classList.add("bad"); out.textContent = u("bad"); tb.innerHTML = ""; return; }
      inp.classList.remove("bad");
      var S = uniStats(vals), N = S.N;
      tb.innerHTML = table([K("x_i"), u("fi"), u("Fi"), u("hi"), u("Hi"), K("x_i\\,f_i"), K("x_i^2\\,f_i")],
        S.T.map(function (r) { return [ft(r.x, 3), r.f, r.F, ft(r.h, 3), ft(r.H, 3), ft(r.x * r.f, 3), ft(r.x * r.x * r.f, 3)]; }),
        [u("total"), N, "", "1", "", ft(S.s, 3), ft(S.s2, 3)]);
      var h = "<p>" + K("N=" + N) + " &nbsp; " + u("mean") + ": " + K("\\bar x=\\dfrac{" + fmt(S.s, 3) + "}{" + N + "}=" + fmt(S.mean)) + "</p>";
      h += "<p>" + u("median") + ": " + K("Me=" + fmt(S.med, 3)) + " &nbsp; " + u("mode") + ": " + K("Mo=" + S.modes.map(function (m) { return fmt(m, 3); }).join(",\\ ")) +
        " &nbsp; " + K("Q_1=" + fmt(S.q1, 3)) + ", " + K("Q_3=" + fmt(S.q3, 3)) + "</p>";
      h += "<p>" + u("range") + ": " + K(fmt(S.max, 3) + "-" + fmt(S.min, 3) + "=" + fmt(S.max - S.min, 3)) + "</p>";
      h += "<p>" + u("vari") + ": " + K("\\sigma^2=\\dfrac{" + fmt(S.s2, 3) + "}{" + N + "}-" + fmt(S.mean) + "^2=" + fmt(S.v)) + " &nbsp; " + u("sd") + ": " + K("\\sigma=" + fmt(S.sd)) + "</p>";
      if (S.mean !== 0) h += "<p>" + u("cv") + ": " + K("CV=\\dfrac{\\sigma}{\\bar x}=" + fmt(S.sd / Math.abs(S.mean)) + "\\ (" + fmt(100 * S.sd / Math.abs(S.mean), 2) + "\\,\\%)") + "</p>";
      out.innerHTML = h;
    }
    onLang(draw);
  }

  /* ---------- 10.4 taula de doble entrada ---------- */
  var PRE_PAIRS = [["1 2 2 3 4 4 5 6", "3 4 5 5 6 7 8 9"], ["1 2 3 4 5", "2 3 5 4 6"], ["1 2 3 4 5 6 7", "9 8 8 6 5 3 2"], ["1 2 3 4 5 6 7 8", "5 2 6 3 7 5 2 6"], ["-3 -2 -1 0 1 2 3", "9 4 1 0 1 4 9"]];
  function readPairs(w) {
    var x = readNums($(w, "x").value), y = readNums($(w, "y").value);
    var ok = x && y && x.length === y.length && x.length >= 2;
    $(w, "x").classList.toggle("bad", !x); $(w, "y").classList.toggle("bad", !y);
    return ok ? { x: x, y: y } : null;
  }
  function pairsPresets(w, draw) {
    presetBtns($(w, "presets"), PRE_PAIRS.length, "pPairs", function (i) { $(w, "x").value = PRE_PAIRS[i][0]; $(w, "y").value = PRE_PAIRS[i][1]; draw(); });
    $(w, "x").addEventListener("input", draw); $(w, "y").addEventListener("input", draw);
  }
  function wDbl() {
    var w = document.getElementById("w-dbl"); if (!w) return;
    var tb = w.querySelector(".vtbl"), out = w.querySelector(".info");
    pairsPresets(w, draw);
    function draw() {
      var P = readPairs(w);
      if (!P) { out.textContent = u("bad2"); tb.innerHTML = ""; return; }
      var xs = freqTable(P.x).map(function (r) { return r.x; }), ys = freqTable(P.y).map(function (r) { return r.x; });
      var M = {}; P.x.forEach(function (a, i) { var k = a + "|" + P.y[i]; M[k] = (M[k] || 0) + 1; });
      var head = ['<span class="dg">' + K("X") + "\\" + K("Y") + "</span>"].concat(ys.map(function (b) { return K(fmt(b, 3)); }), [K("f_{x}")]);
      var rows = xs.map(function (a) {
        var tot = 0, r = [K(fmt(a, 3))];
        ys.forEach(function (b) { var f = M[a + "|" + b] || 0; tot += f; r.push(f ? "<b>" + f + "</b>" : '<span class="z">0</span>'); });
        r.push(tot); return r;
      });
      var foot = [K("f_{y}")].concat(ys.map(function (b) { return P.y.filter(function (v) { return v === b; }).length; }), [P.x.length]);
      tb.innerHTML = table(head, rows, foot);
      out.innerHTML = "<p>" + u("margX") + ": " + K("\\bar x=" + fmt(biStats(P.x, P.y).mx)) + ". &nbsp; " + u("margY") + ": " + K("\\bar y=" + fmt(biStats(P.x, P.y).my)) + ".</p>";
    }
    onLang(draw);
  }

  /* ---------- 10.5 núvol de punts interactiu ---------- */
  var PRE_CLOUD = [[], [[1, 2], [2, 2.5], [3, 3.8], [4, 4.1], [5, 5.6], [6, 6.2], [7, 7.5]], [[1, 8], [2, 7.1], [3, 6.5], [4, 5.2], [5, 4.6], [6, 3.1], [7, 2.4]], [[2, 5], [3, 7], [4, 4], [5, 6.5], [6, 3.5], [4.5, 2.5], [3.5, 3], [5.5, 8]]];
  function wCloud() {
    var w = document.getElementById("w-cloud"); if (!w) return;
    var svg = w.querySelector("svg"), out = w.querySelector(".info"), pts = PRE_CLOUD[1].slice(), G = null;
    presetBtns($(w, "presets"), PRE_CLOUD.length, "pCloud", function (i) { pts = PRE_CLOUD[i].map(function (p) { return p.slice(); }); draw(); });
    svg.addEventListener("click", function (ev) {
      var t = ev.target;
      if (t.classList && t.classList.contains("pt")) { pts.splice(+t.getAttribute("data-i"), 1); draw(); return; }
      var r = svg.getBoundingClientRect(), px = (ev.clientX - r.left) * W / r.width, py = (ev.clientY - r.top) * H / r.height;
      if (px < ML || px > W - MR || py < MT || py > H - MB) return;
      var q = G.inv(px, py); pts.push([Math.round(q[0] * 10) / 10, Math.round(q[1] * 10) / 10]); draw();
    });
    function draw() {
      G = cloud(svg, pts, { xr: [0, 10, 1], yr: [0, 10, 1], means: true });
      var h = "<p>" + u("clickAdd") + "</p><p><b>" + pts.length + "</b> " + u("points");
      if (pts.length >= 2) {
        var S = biStats(pts.map(function (p) { return p[0]; }), pts.map(function (p) { return p[1]; }));
        h += ". " + K("(\\bar x,\\bar y)=(" + fmt(S.mx, 2) + ",\\ " + fmt(S.my, 2) + ")") + " &nbsp; " + K("\\sigma_{xy}=" + fmt(S.c, 3)) + " &nbsp; " + K("r=" + fmt(S.r, 3)) + "</p><p>" + rWords(S.r);
      }
      out.innerHTML = h + "</p>";
    }
    onLang(draw);
  }

  /* ---------- 10.6 taula per a la covariància ---------- */
  function covTable(P) {
    var S = biStats(P.x, P.y);
    var rows = P.x.map(function (a, i) { var b = P.y[i]; return [ft(a, 3), ft(b, 3), ft(a * a, 3), ft(b * b, 3), ft(a * b, 3)]; });
    return { S: S, html: table([K("x_i"), K("y_i"), K("x_i^2"), K("y_i^2"), K("x_i\\,y_i")], rows, [ft(S.sx, 3), ft(S.sy, 3), ft(S.sx2, 3), ft(S.sy2, 3), ft(S.sxy, 3)]) };
  }
  function covSteps(S) {
    var N = S.N;
    return "<p>" + K("\\bar x=\\dfrac{" + fmt(S.sx, 3) + "}{" + N + "}=" + fmt(S.mx) + "\\qquad\\bar y=\\dfrac{" + fmt(S.sy, 3) + "}{" + N + "}=" + fmt(S.my)) + "</p>" +
      "<p>" + K("\\sigma_x^2=\\dfrac{" + fmt(S.sx2, 3) + "}{" + N + "}-" + fmt(S.mx) + "^2=" + fmt(S.vx) + "\\qquad\\sigma_y^2=\\dfrac{" + fmt(S.sy2, 3) + "}{" + N + "}-" + fmt(S.my) + "^2=" + fmt(S.vy)) + "</p>" +
      "<p>" + K("\\sigma_x=" + fmt(Math.sqrt(S.vx)) + "\\qquad\\sigma_y=" + fmt(Math.sqrt(S.vy))) + "</p>" +
      "<p>" + u("cov") + ": " + K("\\sigma_{xy}=\\dfrac{" + fmt(S.sxy, 3) + "}{" + N + "}-" + fmt(S.mx) + "\\cdot" + fmt(S.my) + "=" + fmt(S.c)) + "</p>";
  }
  function wCov() {
    var w = document.getElementById("w-cov"); if (!w) return;
    var tb = w.querySelector(".vtbl"), out = w.querySelector(".info");
    pairsPresets(w, draw);
    function draw() {
      var P = readPairs(w);
      if (!P) { out.textContent = u("bad2"); tb.innerHTML = ""; return; }
      var T = covTable(P); tb.innerHTML = T.html; out.innerHTML = covSteps(T.S);
    }
    onLang(draw);
  }

  function regTex(S) {
    var m = S.c / S.vx, n = S.my - m * S.mx;
    return { m: m, n: n, tex: "y" + "=" + fmt(m, 4) + "x" + (n < 0 ? "-" + fmt(-n, 4) : "+" + fmt(n, 4)) };
  }
  function regSteps(S) {
    var R = regTex(S);
    function sh(v) { return v < 0 ? "+" + fmt(-v) : "-" + fmt(v); }
    return "<p>" + K("y" + sh(S.my) + "=\\dfrac{" + fmt(S.c) + "}{" + fmt(S.vx) + "}\\,(x" + sh(S.mx) + ")") + "</p><p>" + u("regL") + ": " + K(R.tex) + "</p>";
  }
  /* ---------- 10.8 recta de regressió ---------- */
  var PRE_REG = [["1 2 3 4 5", "2 3 5 4 6", "4,5"], ["2 3 4 5 6", "40 34 30 25 21", "4,5"], ["1 2 2 3 4 4 5 6", "3 4 5 5 6 7 8 9", "4,5"], ["1 2 3 4 5 6 7 8", "5 2 6 3 7 5 2 6", "4"]];
  function wReg() {
    var w = document.getElementById("w-reg"); if (!w) return;
    var out = w.querySelector(".info"), svg = w.querySelector("svg"), x0i = $(w, "x0");
    presetBtns($(w, "presets"), PRE_REG.length, "pReg", function (i) { $(w, "x").value = PRE_REG[i][0]; $(w, "y").value = PRE_REG[i][1]; x0i.value = PRE_REG[i][2]; draw(); });
    $(w, "x").addEventListener("input", draw); $(w, "y").addEventListener("input", draw); x0i.addEventListener("input", draw);
    function draw() {
      var P = readPairs(w);
      if (!P) { out.textContent = u("bad2"); svg.innerHTML = ""; return; }
      var S = biStats(P.x, P.y), pts = P.x.map(function (a, i) { return [a, P.y[i]]; });
      if (!(S.vx > 0)) { out.textContent = u("noVar"); svg.innerHTML = ""; return; }
      var R = regTex(S), x0 = num(x0i.value), h = regSteps(S) + "<p>" + K("r=" + fmt(S.r, 3)) + ": " + rWords(S.r) + "</p>", mark = null;
      x0i.classList.toggle("bad", !isFinite(x0));
      if (isFinite(x0)) {
        var y0 = R.m * x0 + R.n, mn = Math.min.apply(null, P.x), mx = Math.max.apply(null, P.x), span = mx - mn;
        h += "<p>" + u("est") + ": " + K("\\hat y(" + fmt(x0, 3) + ")=" + fmt(y0, 3)) + ". ";
        if (Math.abs(S.r) < 0.5) h += "<b>" + u("estBad") + "</b>";
        else if (x0 < mn - 0.15 * span || x0 > mx + 0.15 * span) h += "<b>" + u("estOut") + "</b>";
        else h += u(Math.abs(S.r) >= 0.8 ? "estGood" : "estMid");
        h += "</p>"; mark = [x0, y0];
      }
      cloud(svg, pts, { means: true, reg: true, mark: mark && isFinite(mark[1]) ? mark : null });
      out.innerHTML = h;
    }
    onLang(draw);
  }

  /* ---------- 10.7 r amb un control lliscant i endevina r ---------- */
  function wSlide() {
    var w = document.getElementById("w-slide"); if (!w) return;
    var svg = w.querySelector("svg"), sl = $(w, "r"), out = w.querySelector(".info"), lab = $(w, "rv");
    sl.addEventListener("input", draw);
    function draw() {
      var r = +sl.value, pts = cloudR(40, r, 7).map(function (p) { return [5 + 1.6 * p[0], 5 + 1.6 * p[1]]; });
      cloud(svg, pts, { xr: [0, 10, 1], yr: [0, 10, 1], means: true, r: 3.6 });
      lab.textContent = ft(r, 2);
      out.innerHTML = "<p>" + K("r=" + fmt(r, 2)) + ": " + rWords(r) + "</p>";
    }
    onLang(draw);
  }
  function wGuess() {
    var w = document.getElementById("w-guess"); if (!w) return;
    var svg = w.querySelector("svg"), box = $(w, "opts"), out = w.querySelector(".info"), nb = $(w, "new"), q = $(w, "q");
    var OPTS = [-0.95, -0.7, -0.3, 0, 0.3, 0.7, 0.95], seed = 11, cur = 0, ok = 0, tries = 0, answered = false;
    function fresh() { seed = (seed * 7 + 13) % 100000; cur = OPTS[seed % OPTS.length]; answered = false; draw(); }
    nb.addEventListener("click", fresh);
    function draw() {
      q.textContent = u("guessQ"); nb.textContent = u("newCloud");
      var pts = cloudR(30, cur, seed).map(function (p) { return [5 + 1.5 * p[0], 5 + 1.5 * p[1]]; });
      cloud(svg, pts, { xr: [0, 10, 1], yr: [0, 10, 1], r: 3.6 });
      box.innerHTML = "";
      OPTS.forEach(function (o) {
        var b = document.createElement("button"); b.type = "button"; b.className = "btn"; b.innerHTML = K("r=" + fmt(o, 2));
        if (answered) { b.disabled = true; if (o === cur) b.classList.add("ok-b"); }
        b.addEventListener("click", function () { if (answered) return; answered = true; tries++; if (o === cur) ok++; out.innerHTML = "<p><b>" + (o === cur ? "✓ " + u("right") : "✗ " + u("wrong")) + "</b> " + u("wasR") + " " + K(fmt(cur, 2)) + ". " + u("hits") + ": " + ok + " / " + tries + "</p>"; draw(); });
        box.appendChild(b);
      });
      if (!answered && !tries) out.innerHTML = "";
    }
    onLang(draw);
  }

  /* ---------- figures fixes: núvols dels exemples ---------- */
  function F(fn, n, a, b, noise, seed) { var rand = rng(seed), out = []; for (var i = 0; i < n; i++) { var x = a + (b - a) * (i + rand() * 0.8) / n; out.push([x, fn(x) + noise * (rand() * 2 - 1)]); } return out; }
  var FIGS = {
    reg1: function () { return { pts: [[1, 2], [2, 3], [3, 5], [4, 4], [5, 6]], o: { xr: [0, 6, 1], yr: [0, 7, 1], means: true, reg: true, axes: ["X", "Y"] } }; },
    cl1: function () { return { pts: [[1, 2], [2, 3], [3, 5], [4, 4], [5, 6]], o: { xr: [0, 6, 1], yr: [0, 7, 1], means: true, axes: ["X", "Y"] } }; },
    clHours: function () { return { pts: [[1, 3], [2, 4], [2, 5], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9]], o: { xr: [0, 7, 1], yr: [0, 10, 1], axes: ["h", "nota"] } }; },
    rp: function () { return { pts: cloudR(30, 0.92, 3).map(function (p) { return [5 + 1.5 * p[0], 5 + 1.5 * p[1]]; }), o: { xr: [0, 10, 2], yr: [0, 10, 2], r: 3.4 } }; },
    rn: function () { return { pts: cloudR(30, -0.85, 5).map(function (p) { return [5 + 1.5 * p[0], 5 + 1.5 * p[1]]; }), o: { xr: [0, 10, 2], yr: [0, 10, 2], r: 3.4 } }; },
    r0: function () { return { pts: cloudR(30, 0.02, 9).map(function (p) { return [5 + 1.5 * p[0], 5 + 1.5 * p[1]]; }), o: { xr: [0, 10, 2], yr: [0, 10, 2], r: 3.4 } }; },
    rw: function () { return { pts: cloudR(30, 0.45, 21).map(function (p) { return [5 + 1.5 * p[0], 5 + 1.5 * p[1]]; }), o: { xr: [0, 10, 2], yr: [0, 10, 2], r: 3.4 } }; },
    par: function () { return { pts: F(function (x) { return 9 - (x - 5) * (x - 5) * 0.35; }, 24, 0.2, 9.8, 0.6, 4), o: { xr: [0, 10, 2], yr: [0, 10, 2], r: 3.4 } }; },
    expo: function () { return { pts: F(function (x) { return 0.15 * Math.exp(0.42 * x); }, 24, 0.2, 9.8, 0.25, 8), o: { xr: [0, 10, 2], yr: [0, 10, 2], r: 3.4 } }; },
    sat: function () { return { pts: F(function (x) { return 9 * (1 - Math.exp(-0.5 * x)); }, 24, 0.2, 9.8, 0.4, 12), o: { xr: [0, 10, 2], yr: [0, 10, 2], r: 3.4 } }; },
    circ: function () { var o = []; for (var i = 0; i < 24; i++) { var a = i / 24 * 2 * Math.PI; o.push([5 + 3.6 * Math.cos(a), 5 + 3.6 * Math.sin(a)]); } return { pts: o, o: { xr: [0, 10, 2], yr: [0, 10, 2], r: 3.4 } }; },
    outl: function () { return { pts: [[1, 1.2], [1.5, 1], [2, 1.4], [1.2, 1.6], [1.8, 0.9], [2.2, 1.3], [1.4, 1.1], [9, 9]], o: { xr: [0, 10, 2], yr: [0, 10, 2], r: 3.6, hl: 7 } }; }
  };
  function wFigs() {
    document.querySelectorAll("[data-g]").forEach(function (el) {
      var mk = FIGS[el.getAttribute("data-g")]; if (!mk) return;
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("class", "st-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Núvol de punts");
      el.insertBefore(svg, el.firstChild);
      var cfg = mk();
      onLang(function () {
        cloud(svg, cfg.pts, cfg.o);
        var cap = el.querySelector(".rcap");
        if (cap) { var S = biStats(cfg.pts.map(function (p) { return p[0]; }), cfg.pts.map(function (p) { return p[1]; })); cap.innerHTML = K("r\\approx" + fmt(S.r, 2)); }
      });
    });
  }

  /* ---------- laboratori bidimensional ---------- */
  function wLab() {
    var w = document.getElementById("w-lab"); if (!w) return;
    var tb = w.querySelector(".vtbl"), out = w.querySelector(".info"), svg = w.querySelector("svg");
    pairsPresets(w, draw);
    function draw() {
      var P = readPairs(w);
      if (!P) { out.textContent = u("bad2"); tb.innerHTML = ""; svg.innerHTML = ""; return; }
      var T = covTable(P), S = T.S;
      tb.innerHTML = T.html;
      cloud(svg, P.x.map(function (a, i) { return [a, P.y[i]]; }), { means: true, reg: true });
      out.innerHTML = covSteps(S) + (S.vx > 0 ? regSteps(S) : "") + "<p>" + u("r") + ": " + K("r=\\dfrac{\\sigma_{xy}}{\\sigma_x\\,\\sigma_y}=\\dfrac{" + fmt(S.c) + "}{" + fmt(Math.sqrt(S.vx)) + "\\cdot" + fmt(Math.sqrt(S.vy)) + "}=" + fmt(S.r)) + "</p><p><b>" + rWords(S.r) + "</b></p>";
    }
    onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es || va, en: en || va }; }
  var QUIZ = [
    { q: q3("El nombre de germans d'un alumne és una variable…", "El número de hermanos de un alumno es una variable…", "The number of siblings of a student is a…"),
      o: [q3("quantitativa discreta", "cuantitativa discreta", "discrete quantitative variable"), q3("quantitativa contínua", "cuantitativa continua", "continuous quantitative variable"), q3("qualitativa", "cualitativa", "qualitative variable")], a: 0,
      e: q3("Pren valors numèrics aïllats (0, 1, 2…).", "Toma valores numéricos aislados (0, 1, 2…).", "It takes isolated numerical values (0, 1, 2…).") },
    { q: q3("La mitjana de 2, 4, 4, 5 i 10 és…", "La media de 2, 4, 4, 5 y 10 es…", "The mean of 2, 4, 4, 5 and 10 is…"),
      o: [q3("$4$"), q3("$5$"), q3("$4{,}5$", "$4{,}5$", "$4.5$")], a: 1, e: q3("$\\frac{25}{5}=5$. La mediana és 4.", "$\\frac{25}{5}=5$. La mediana es 4.", "$\\frac{25}{5}=5$. The median is 4.") },
    { q: q3("Si $\\sum x_i^2f_i=50$, $N=10$ i $\\bar x=2$, la variància és…", "Si $\\sum x_i^2f_i=50$, $N=10$ y $\\bar x=2$, la varianza es…", "If $\\sum x_i^2f_i=50$, $N=10$ and $\\bar x=2$, the variance is…"),
      o: [q3("$1$"), q3("$3$"), q3("$5$")], a: 0, e: q3("$\\sigma^2=\\frac{50}{10}-2^2=1$.") },
    { q: q3("Dos grups tenen $\\bar x=10,\\ \\sigma=2$ i $\\bar x=50,\\ \\sigma=5$. Quin és relativament més dispers?", "Dos grupos tienen $\\bar x=10,\\ \\sigma=2$ y $\\bar x=50,\\ \\sigma=5$. ¿Cuál es relativamente más disperso?", "Two groups have $\\bar x=10,\\ \\sigma=2$ and $\\bar x=50,\\ \\sigma=5$. Which is relatively more spread out?"),
      o: [q3("el primer", "el primero", "the first"), q3("el segon", "el segundo", "the second"), q3("igual", "igual", "the same")], a: 0,
      e: q3("$CV_1=0{,}2$ i $CV_2=0{,}1$: compara amb el coeficient de variació.", "$CV_1=0{,}2$ y $CV_2=0{,}1$: compara con el coeficiente de variación.", "$CV_1=0.2$ and $CV_2=0.1$: compare the coefficients of variation.") },
    { q: q3("En una taula de doble entrada, la suma d'una fila dona…", "En una tabla de doble entrada, la suma de una fila da…", "In a two-way table, the sum of a row gives…"),
      o: [q3("una freqüència marginal de X", "una frecuencia marginal de X", "a marginal frequency of X"), q3("la covariància", "la covarianza", "the covariance"), q3("el total N", "el total N", "the total N")], a: 0,
      e: q3("Les sumes de files i de columnes són les distribucions marginals.", "Las sumas de filas y de columnas son las distribuciones marginales.", "Row and column sums are the marginal distributions.") },
    { q: q3("El centre de gravetat d'un núvol de punts és…", "El centro de gravedad de una nube de puntos es…", "The centre of gravity of a scatter plot is…"),
      o: [q3("$(\\bar x,\\bar y)$"), q3("$(\\sigma_x,\\sigma_y)$"), q3("el punt més alt", "el punto más alto", "the highest point")], a: 0, e: q3("És el punt de les dues mitjanes.", "Es el punto de las dos medias.", "It is the point given by both means.") },
    { q: q3("Si $\\sum x_iy_i=69$, $N=5$, $\\bar x=3$ i $\\bar y=4$, la covariància és…", "Si $\\sum x_iy_i=69$, $N=5$, $\\bar x=3$ y $\\bar y=4$, la covarianza es…", "If $\\sum x_iy_i=69$, $N=5$, $\\bar x=3$ and $\\bar y=4$, the covariance is…"),
      o: [q3("$1{,}8$", "$1{,}8$", "$1.8$"), q3("$13{,}8$", "$13{,}8$", "$13.8$"), q3("$-1{,}8$", "$-1{,}8$", "$-1.8$")], a: 0, e: q3("$\\sigma_{xy}=\\frac{69}{5}-3\\cdot4=13{,}8-12=1{,}8$.", "$\\sigma_{xy}=\\frac{69}{5}-3\\cdot4=13{,}8-12=1{,}8$.", "$\\sigma_{xy}=\\frac{69}{5}-3\\cdot4=13.8-12=1.8$.") },
    { q: q3("Una covariància negativa indica que…", "Una covarianza negativa indica que…", "A negative covariance means that…"),
      o: [q3("quan una variable creix, l'altra tendeix a decréixer", "cuando una variable crece, la otra tiende a decrecer", "when one variable increases, the other tends to decrease"), q3("no hi ha cap relació", "no hay ninguna relación", "there is no relation"), q3("hi ha un error de càlcul", "hay un error de cálculo", "there is a calculation error")], a: 0,
      e: q3("La majoria de punts són als quadrants 2n i 4t respecte de $(\\bar x,\\bar y)$.", "La mayoría de puntos están en los cuadrantes 2º y 4º respecto de $(\\bar x,\\bar y)$.", "Most points lie in the 2nd and 4th quadrants around $(\\bar x,\\bar y)$.") },
    { q: q3("Quin d'aquests valors NO pot ser un coeficient de correlació?", "¿Cuál de estos valores NO puede ser un coeficiente de correlación?", "Which of these values CANNOT be a correlation coefficient?"),
      o: [q3("$-0{,}98$", "$-0{,}98$", "$-0.98$"), q3("$1{,}2$", "$1{,}2$", "$1.2$"), q3("$0$")], a: 1, e: q3("Sempre $-1\\leq r\\leq1$.") },
    { q: q3("Si $\\sigma_{xy}=1{,}8$ i $\\sigma_x=\\sigma_y=\\sqrt2$, aleshores $r$ val…", "Si $\\sigma_{xy}=1{,}8$ y $\\sigma_x=\\sigma_y=\\sqrt2$, entonces $r$ vale…", "If $\\sigma_{xy}=1.8$ and $\\sigma_x=\\sigma_y=\\sqrt2$, then $r$ equals…"),
      o: [q3("$0{,}9$", "$0{,}9$", "$0.9$"), q3("$1{,}8$", "$1{,}8$", "$1.8$"), q3("$1{,}27$", "$1{,}27$", "$1.27$")], a: 0, e: q3("$r=\\frac{1{,}8}{\\sqrt2\\cdot\\sqrt2}=\\frac{1{,}8}{2}=0{,}9$.", "$r=\\frac{1{,}8}{\\sqrt2\\cdot\\sqrt2}=\\frac{1{,}8}{2}=0{,}9$.", "$r=\\frac{1.8}{\\sqrt2\\cdot\\sqrt2}=\\frac{1.8}{2}=0.9$.") },
    { q: q3("$r=-0{,}93$ indica una correlació…", "$r=-0{,}93$ indica una correlación…", "$r=-0.93$ indicates a…"),
      o: [q3("negativa i forta", "negativa y fuerte", "strong negative correlation"), q3("negativa i feble", "negativa y débil", "weak negative correlation"), q3("positiva i forta", "positiva y fuerte", "strong positive correlation")], a: 0,
      e: q3("El signe diu el sentit i $|r|$ prop d'1, la força.", "El signo dice el sentido y $|r|$ cerca de 1, la fuerza.", "The sign gives the direction and $|r|$ close to 1, the strength.") },
    { q: q3("Si els punts formen una paràbola gairebé perfecta i simètrica, $r$ pot ser…", "Si los puntos forman una parábola casi perfecta y simétrica, $r$ puede ser…", "If the points form an almost perfect symmetric parabola, $r$ can be…"),
      o: [q3("pròxim a 0", "cercano a 0", "close to 0"), q3("pròxim a 1", "cercano a 1", "close to 1"), q3("pròxim a −1", "cercano a −1", "close to −1")], a: 0,
      e: q3("Hi ha una relació forta però no lineal: $r$ només mesura la relació lineal.", "Hay una relación fuerte pero no lineal: $r$ solo mide la relación lineal.", "There is a strong but non-linear relation: $r$ only measures linear relation.") },
    { q: q3("La recta de regressió de Y sobre X sempre passa pel punt…", "La recta de regresión de Y sobre X siempre pasa por el punto…", "The regression line of Y on X always passes through…"),
      o: [q3("$(\\bar x,\\bar y)$"), q3("$(0,0)$"), q3("$(\\sigma_x,\\sigma_y)$")], a: 0, e: q3("El centre de gravetat: $y-\\bar y=\\frac{\\sigma_{xy}}{\\sigma_x^2}(x-\\bar x)$.", "El centro de gravedad: $y-\\bar y=\\frac{\\sigma_{xy}}{\\sigma_x^2}(x-\\bar x)$.", "The centre of gravity: $y-\\bar y=\\frac{\\sigma_{xy}}{\\sigma_x^2}(x-\\bar x)$.") },
    { q: q3("Amb $\\bar x=3$, $\\bar y=4$, $\\sigma_x^2=2$ i $\\sigma_{xy}=1$, la recta de regressió de Y sobre X és…", "Con $\\bar x=3$, $\\bar y=4$, $\\sigma_x^2=2$ y $\\sigma_{xy}=1$, la recta de regresión de Y sobre X es…", "With $\\bar x=3$, $\\bar y=4$, $\\sigma_x^2=2$ and $\\sigma_{xy}=1$, the regression line of Y on X is…"),
      o: [q3("$y=0{,}5x+2{,}5$", "$y=0{,}5x+2{,}5$", "$y=0.5x+2.5$"), q3("$y=2x-2$"), q3("$y=0{,}5x+4$", "$y=0{,}5x+4$", "$y=0.5x+4$")], a: 0, e: q3("$y-4=\\frac12(x-3)\\Rightarrow y=0{,}5x+2{,}5$.", "$y-4=\\frac12(x-3)\\Rightarrow y=0{,}5x+2{,}5$.", "$y-4=\\frac12(x-3)\\Rightarrow y=0.5x+2.5$.") },
    { q: q3("Una estimació feta amb la recta de regressió és més fiable quan…", "Una estimación hecha con la recta de regresión es más fiable cuando…", "An estimate from the regression line is more reliable when…"),
      o: [q3("$|r|$ és prop d'1 i $x$ és dins de l'interval de les dades", "$|r|$ está cerca de 1 y $x$ está dentro del intervalo de los datos", "$|r|$ is close to 1 and $x$ is within the data range"), q3("$r$ és prop de 0", "$r$ está cerca de 0", "$r$ is close to 0"), q3("$x$ és molt lluny de les dades", "$x$ está muy lejos de los datos", "$x$ is far from the data")], a: 0,
      e: q3("La fiabilitat depén de $|r|$ i de no extrapolar.", "La fiabilidad depende de $|r|$ y de no extrapolar.", "Reliability depends on $|r|$ and on not extrapolating.") },
    { q: q3("Si entre dues variables $r=0{,}95$, podem dir que una és la causa de l'altra?", "Si entre dos variables $r=0{,}95$, ¿podemos decir que una es la causa de la otra?", "If two variables have $r=0.95$, can we say one causes the other?"),
      o: [q3("No necessàriament", "No necesariamente", "Not necessarily"), q3("Sí, sempre", "Sí, siempre", "Yes, always"), q3("Només si $r=1$", "Solo si $r=1$", "Only if $r=1$")], a: 0,
      e: q3("Correlació no vol dir causalitat: pot haver-hi una tercera variable que influïsca en les dues.", "Correlación no significa causalidad: puede haber una tercera variable que influya en las dos.", "Correlation does not imply causation: a third variable may influence both.") }
  ];

  /*@@GENERIC@@*/
  var TITLES = { va: "Estadística · FentMates", es: "Estadística · FentMates", en: "Statistics · FentMates" };
  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l; root.setAttribute("data-lang", l); root.lang = HTML_LANG[l]; document.title = TITLES[l]; store("lang", l);
    try { var url = new URL(location.href); if (url.searchParams.has("lang")) { url.searchParams.set("lang", l); history.replaceState(null, "", url); } } catch (e) {}
    refreshers.forEach(function (fn) { fn(); });
  }

  function init() {
    document.title = TITLES[lang];
    var D = [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }];
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, { delimiters: D, ignoredClasses: ["widget", "lab"], throwOnError: false });
      document.querySelectorAll(".widget .wt, .widget label, #w-lab label").forEach(function (el) { window.renderMathInElement(el, { delimiters: D, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wFigs, wUni, wDbl, wCloud, wCov, wReg, wSlide, wGuess, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM110b = { uniStats: uniStats, biStats: biStats, cloudR: cloudR, readList: readList };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
