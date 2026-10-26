(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2batx-u6-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt", pc: "si", rest: "en la resta",
      bad: "No entenc l'expressió: revisa-la.", aBad: "Escriu nombres per als extrems de l'interval (a < b).", noDiff: "Aquesta expressió no la sé derivar amb les regles de la unitat.",
      point: "Punt de tangència", slope: "Pendent", tline: "Recta tangent", nline: "Recta normal", horiz: "la tangent és horitzontal, així que la normal és vertical",
      perp: "Comprovació: són perpendiculars", noF: "La funció no existeix en aquest punt.", noD: "La funció no és derivable en aquest punt.",
      noPts: "cap punt de la finestra té tangent amb aquest pendent", inc: "creixent", dec: "decreixent", flat: "tangent horitzontal",
      test: "Valor de prova", noDom: "fora del domini", mx: "màx", mn: "mín", incOn: "Creixent en", decOn: "Decreixent en",
      crit: "Punts crítics", noCrit: "No hi ha cap punt on f′(x) = 0.", maxR: "Màxim relatiu", minR: "Mínim relatiu", noExt: "no és extrem",
      c1: "Canvi de signe de f′", c2: "Segona derivada", undec: "no decideix", type: "Conclusió", cand: "Candidat", endp: "extrem de l'interval", critp: "punt crític",
      absMax: "Màxim absolut", absMin: "Mínim absolut", notCont: "Compte: la funció no és contínua en tot l'interval, així que potser no té extrems absoluts.",
      goUp: "f′ > 0: si augmentes la variable, la funció puja.", goDn: "f′ < 0: si augmentes la variable, la funció baixa.", found: "Has trobat l'òptim!",
      optMax: "El màxim s'assoleix en", optMin: "El mínim s'assoleix en", many: "Hi ha molts punts crítics: mostrem l'estudi en la finestra",
      inR: "Estudi en ℝ", inI: "Estudi en l'interval",
      pTan: ["x² − 4x + 5", "x·eˣ", "ln(x² − 3)", "x³ − 3x + 1", "(x+1)/(x−1)"], pPar: ["x³ − 3x + 1 ∥ y = 9x", "x³ − 3x² ∥ y = 9x", "Tangent horitzontal", "eˣ"],
      pNorm: ["x² − 4x + 5", "√x", "x³ − 3x", "2/x", "ln x"], pMono: ["Polinomi", "x²/(x − 1)", "x·e⁻ˣ", "x³", "x − ln x"],
      pExt: ["Polinomi", "x⁴ − 2x²", "x⁴ − 4x³", "x²/(x − 1)", "x + 4/x", "x·eˣ"], pAbs: ["Exemple 1", "Exemple 2", "x·e⁻ˣ", "Contaminant"],
      pOpt: ["Llepolies", "Benefici per tona", "Cost mitjà", "Contaminació"], pBuild: ["Piscina", "Caixa", "Camp vora el riu", "Agència de viatges"],
      pLab: ["Polinomi", "Racional", "Exponencial", "Logaritme", "x/(x² + 1)", "x⁴ − 4x³", "En [0, 5]"] },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba", pc: "si", rest: "en el resto",
      bad: "No entiendo la expresión: revísala.", aBad: "Escribe números para los extremos del intervalo (a < b).", noDiff: "Esta expresión no la sé derivar con las reglas de la unidad.",
      point: "Punto de tangencia", slope: "Pendiente", tline: "Recta tangente", nline: "Recta normal", horiz: "la tangente es horizontal, así que la normal es vertical",
      perp: "Comprobación: son perpendiculares", noF: "La función no existe en este punto.", noD: "La función no es derivable en este punto.",
      noPts: "ningún punto de la ventana tiene tangente con esta pendiente", inc: "creciente", dec: "decreciente", flat: "tangente horizontal",
      test: "Valor de prueba", noDom: "fuera del dominio", mx: "máx", mn: "mín", incOn: "Creciente en", decOn: "Decreciente en",
      crit: "Puntos críticos", noCrit: "No hay ningún punto donde f′(x) = 0.", maxR: "Máximo relativo", minR: "Mínimo relativo", noExt: "no es extremo",
      c1: "Cambio de signo de f′", c2: "Segunda derivada", undec: "no decide", type: "Conclusión", cand: "Candidato", endp: "extremo del intervalo", critp: "punto crítico",
      absMax: "Máximo absoluto", absMin: "Mínimo absoluto", notCont: "Cuidado: la función no es continua en todo el intervalo, así que quizá no tenga extremos absolutos.",
      goUp: "f′ > 0: si aumentas la variable, la función sube.", goDn: "f′ < 0: si aumentas la variable, la función baja.", found: "¡Has encontrado el óptimo!",
      optMax: "El máximo se alcanza en", optMin: "El mínimo se alcanza en", many: "Hay muchos puntos críticos: mostramos el estudio en la ventana",
      inR: "Estudio en ℝ", inI: "Estudio en el intervalo",
      pTan: ["x² − 4x + 5", "x·eˣ", "ln(x² − 3)", "x³ − 3x + 1", "(x+1)/(x−1)"], pPar: ["x³ − 3x + 1 ∥ y = 9x", "x³ − 3x² ∥ y = 9x", "Tangente horizontal", "eˣ"],
      pNorm: ["x² − 4x + 5", "√x", "x³ − 3x", "2/x", "ln x"], pMono: ["Polinomio", "x²/(x − 1)", "x·e⁻ˣ", "x³", "x − ln x"],
      pExt: ["Polinomio", "x⁴ − 2x²", "x⁴ − 4x³", "x²/(x − 1)", "x + 4/x", "x·eˣ"], pAbs: ["Ejemplo 1", "Ejemplo 2", "x·e⁻ˣ", "Contaminante"],
      pOpt: ["Golosinas", "Beneficio por tonelada", "Coste medio", "Contaminación"], pBuild: ["Piscina", "Caja", "Campo junto al río", "Agencia de viajes"],
      pLab: ["Polinomio", "Racional", "Exponencial", "Logaritmo", "x/(x² + 1)", "x⁴ − 4x³", "En [0, 5]"] },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top", pc: "if", rest: "otherwise",
      bad: "I can't read that expression: check it.", aBad: "Type numbers for the ends of the interval (a < b).", noDiff: "I can't differentiate this with the rules of the unit.",
      point: "Point of tangency", slope: "Slope", tline: "Tangent line", nline: "Normal line", horiz: "the tangent is horizontal, so the normal is vertical",
      perp: "Check: they are perpendicular", noF: "The function does not exist at this point.", noD: "The function is not differentiable at this point.",
      noPts: "no point in the window has a tangent with this slope", inc: "increasing", dec: "decreasing", flat: "horizontal tangent",
      test: "Test value", noDom: "outside the domain", mx: "max", mn: "min", incOn: "Increasing on", decOn: "Decreasing on",
      crit: "Critical points", noCrit: "There is no point where f′(x) = 0.", maxR: "Relative maximum", minR: "Relative minimum", noExt: "not an extremum",
      c1: "Sign change of f′", c2: "Second derivative", undec: "inconclusive", type: "Conclusion", cand: "Candidate", endp: "endpoint", critp: "critical point",
      absMax: "Absolute maximum", absMin: "Absolute minimum", notCont: "Careful: the function is not continuous on the whole interval, so it may have no absolute extrema.",
      goUp: "f′ > 0: if you increase the variable, the function goes up.", goDn: "f′ < 0: if you increase the variable, the function goes down.", found: "You found the optimum!",
      optMax: "The maximum is reached at", optMin: "The minimum is reached at", many: "There are many critical points: the study is shown for the window",
      inR: "Study on ℝ", inI: "Study on the interval",
      pTan: ["x² − 4x + 5", "x·eˣ", "ln(x² − 3)", "x³ − 3x + 1", "(x+1)/(x−1)"], pPar: ["x³ − 3x + 1 ∥ y = 9x", "x³ − 3x² ∥ y = 9x", "Horizontal tangent", "eˣ"],
      pNorm: ["x² − 4x + 5", "√x", "x³ − 3x", "2/x", "ln x"], pMono: ["Polynomial", "x²/(x − 1)", "x·e⁻ˣ", "x³", "x − ln x"],
      pExt: ["Polynomial", "x⁴ − 2x²", "x⁴ − 4x³", "x²/(x − 1)", "x + 4/x", "x·eˣ"], pAbs: ["Example 1", "Example 2", "x·e⁻ˣ", "Pollutant"],
      pOpt: ["Sweets", "Profit per tonne", "Average cost", "Pollution"], pBuild: ["Swimming pool", "Box", "Field by the river", "Travel agency"],
      pLab: ["Polynomial", "Rational", "Exponential", "Logarithm", "x/(x² + 1)", "x⁴ − 4x³", "On [0, 5]"] }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  function t3(va, es, en) { return lang === "es" ? es : lang === "en" ? en : va; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }

  /*@@CORE@@*/
  /*@@DERIV@@*/
  /* ---------- nombres i rectes ---------- */
  function F(s) { return compile(parse(s)); }
  var RATIO = (H - MT - MB) / (W - ML - MR); // per a vistes amb la mateixa escala en els dos eixos
  function sgn(v) { return v > 0 ? 1 : v < 0 ? -1 : 0; }
  function snap(x) { if (Math.abs(x) < 1e-9) return 0; var q = fracOf(x, 12); return q ? q.n / q.d : x; }
  // valor exacte si és senzill; si no, arrodonit
  function nn(v) { var s = niceTex(v); return s.indexOf("\\approx") === 0 ? numTex(+v.toFixed(4)) : s; }
  function eqv(l, v) { var s = niceTex(v); return s.indexOf("\\approx") === 0 ? l + s : l + "=" + s; }
  function r2(v) { return numTex(+v.toFixed(2)); }
  // y − f(a) = m(x − a)
  function ptSl(m, a, fa) {
    var yl = Math.abs(fa) < 1e-12 ? "y" : "y" + (fa > 0 ? "-" : "+") + nn(Math.abs(fa));
    if (Math.abs(m) < 1e-12) return yl + "=0";
    var xr = Math.abs(a) < 1e-12 ? "x" : "\\left(x" + (a > 0 ? "-" : "+") + nn(Math.abs(a)) + "\\right)";
    return yl + "=" + (Math.abs(m - 1) < 1e-12 ? "" : Math.abs(m + 1) < 1e-12 ? "-" : nn(m)) + xr;
  }
  // y = mx + n
  function lineT(m, a, fa) {
    if (Math.abs(m) < 1e-12) return "y=" + nn(fa);
    var b0 = fa - m * a;
    return "y=" + (Math.abs(m - 1) < 1e-12 ? "" : Math.abs(m + 1) < 1e-12 ? "-" : nn(m)) + "x" + (Math.abs(b0) < 1e-9 ? "" : (b0 > 0 ? "+" : "-") + nn(Math.abs(b0)));
  }
  // tros de recta de la mateixa llargària en pantalla, siga quin siga el pendent
  function segAt(m, a, fa, v, col, k) {
    var len = (v[1] - v[0]) * (k || 0.16), r = (v[1] - v[0]) / (v[3] - v[2]) * RATIO, dx = len / Math.sqrt(1 + m * m * r * r);
    return { f: lineF(m, a, fa), a: a - dx, b: a + dx, col: col };
  }

  /* ---------- arrels, punts crítics i taula de signes (numèricament) ---------- */
  function roots(g, x0, x1, N) {
    N = N || 4000;
    var h = (x1 - x0) / N, xs = [], gs = [], out = [], i, it, m;
    for (i = 0; i <= N; i++) { xs.push(x0 + i * h); gs.push(g(xs[i])); }
    function push(r) {
      if (!(r >= x0 - 1e-12 && r <= x1 + 1e-12) || !isFinite(g(r))) return;
      r = snap(r);
      for (var k = 0; k < out.length; k++) if (Math.abs(out[k] - r) < 1e-6 * (1 + Math.abs(r))) return;
      out.push(r);
    }
    for (i = 0; i < N; i++) {
      var a = gs[i], b = gs[i + 1];
      if (!isFinite(a) || !isFinite(b)) continue;
      if (a === 0) { push(xs[i]); continue; }
      if (a * b < 0) {
        var p = xs[i], q = xs[i + 1], gp = a;
        for (it = 0; it < 80; it++) { m = (p + q) / 2; var gm = g(m); if (!isFinite(gm)) break; if (sgn(gm) === sgn(gp)) { p = m; gp = gm; } else q = m; }
        var r = (p + q) / 2;
        if (Math.abs(g(r)) < 1e-6 * (1 + Math.abs(a) + Math.abs(b))) push(r); // si no, és un pol
      } else if (i > 0 && isFinite(gs[i - 1]) && a * gs[i - 1] > 0 && Math.abs(a) <= Math.abs(gs[i - 1]) && Math.abs(a) <= Math.abs(b)) {
        // arrel doble (sense canvi de signe): mínim local de |g|
        var lo = xs[i - 1], hi = xs[i + 1];
        for (it = 0; it < 100; it++) { var m1 = lo + (hi - lo) / 3, m2 = hi - (hi - lo) / 3; if (Math.abs(g(m1)) < Math.abs(g(m2))) hi = m2; else lo = m1; }
        var rr = (lo + hi) / 2;
        if (Math.abs(g(rr)) < 1e-9) push(rr);
      }
    }
    return out.sort(function (p, q) { return p - q; });
  }
  // ev: punts on f' = 0 ("z"), on f no existeix ("h") o on comença o acaba el domini ("e"); seg: signe de f' entre ells
  function crit(f, df, x0, x1) {
    var N = 6000, h = (x1 - x0) / N, ev = [], X = [], OK = [], i, it, m;
    function ok(x) { return isFinite(f(x)) && isFinite(df(x)); }
    function add(x, k) { x = snap(x); for (var j = 0; j < ev.length; j++) if (Math.abs(ev[j].x - x) < 1e-6 * (1 + Math.abs(x))) return; ev.push({ x: x, k: k }); }
    for (i = 0; i <= N; i++) { X.push(x0 + i * h); OK.push(ok(X[i])); }
    for (i = 0; i < N; i++) {
      var p = X[i], q = X[i + 1];
      if (OK[i] !== OK[i + 1]) {
        if (OK[i] && i + 2 <= N && OK[i + 2]) { add(q, "h"); continue; }  // un sol punt fora del domini
        if (!OK[i] && i >= 1 && OK[i - 1]) continue;
        var lo = p, hi = q;
        for (it = 0; it < 60; it++) { m = (lo + hi) / 2; if (ok(m) === OK[i]) lo = m; else hi = m; }
        add((lo + hi) / 2, "e");
        continue;
      }
      if (!OK[i]) continue;
      var d1 = df(p), d2 = df(q), s1 = sgn(d1), s2 = sgn(d2), fp = f(p), dv = f(q) - fp, a, b;
      if (s1 === s2 && s1 !== 0 && dv * s1 < 0 && Math.abs(dv) > 1e-9 * (1 + Math.abs(fp))) {
        // f' no canvia de signe però f «salta» en sentit contrari: hi ha una asímptota entremig
        a = p; b = q;
        for (it = 0; it < 60; it++) { m = (a + b) / 2; var fm = f(m); if (!isFinite(fm)) { a = b = m; break; } if ((fm - f(a)) * s1 < 0) b = m; else a = m; }
        add((a + b) / 2, "h");
      } else if (s1 * s2 < 0) {
        a = p; b = q; var ga = d1;
        for (it = 0; it < 80; it++) { m = (a + b) / 2; var gm = df(m); if (!isFinite(gm)) break; if (sgn(gm) === sgn(ga)) { a = m; ga = gm; } else b = m; }
        var r = (a + b) / 2;
        if (!(Math.abs(df(r)) < 1e-6 * (1 + Math.abs(d1) + Math.abs(d2)))) add(r, "h");
      }
    }
    roots(df, x0, x1, N).forEach(function (r) { if (isFinite(f(r))) add(r, "z"); });
    ev.sort(function (p, q) { return p.x - q.x; });
    var bs = [x0].concat(ev.map(function (e) { return e.x; })).concat([x1]), seg = [];
    for (i = 0; i + 1 < bs.length; i++) {
      var A = bs[i], Bb = bs[i + 1], t = null;
      [0.5, 0.25, 0.75, 0.1, 0.9].some(function (k) { var x = A + (Bb - A) * k; if (ok(x) && df(x) !== 0) { t = x; return true; } return false; });
      seg.push({ a: A, b: Bb, s: t === null ? 0 : sgn(df(t)), t: t });
    }
    return { ev: ev, seg: seg };
  }
  // estudi complet: derivades, punts crítics i classificació
  function studyF(n, x0, x1) {
    var f = compile(n), dn = D(n), df = compile(dn), S = crit(f, df, x0, x1);
    S.f = f; S.n = n; S.dn = dn; S.df = df; S.x0 = x0; S.x1 = x1;
    try { S.d2n = D(dn); S.d2 = compile(S.d2n); } catch (e) { S.d2 = null; }
    S.ev.forEach(function (e, j) {
      e.y = f(e.x);
      if (e.k !== "z") return;
      var l = S.seg[j].s, r = S.seg[j + 1].s;
      e.t1 = l > 0 && r < 0 ? "max" : l < 0 && r > 0 ? "min" : "none";
      if (S.d2) { var v2 = S.d2(e.x); e.v2 = v2; e.t2 = !isFinite(v2) ? "?" : v2 < -1e-9 ? "max" : v2 > 1e-9 ? "min" : "undec"; }
    });
    return S;
  }
  function intTex(a, b, aInf, bInf) { return "(" + (aInf ? "-\\infty" : nn(a)) + "," + (bInf ? "+\\infty" : nn(b)) + ")"; }
  // un valor de prova «bonic» dins de l'interval
  function testPt(S, g, aInf, bInf) {
    var a = g.a, b = g.b, c;
    if (aInf && bInf) c = 0;
    else if (aInf) c = Math.ceil(b) - 1;
    else if (bInf) c = Math.floor(a) + 1;
    else {
      c = Math.round((a + b) / 2);
      if (!(c > a && c < b)) { c = Math.floor(a) + 1; if (!(c < b)) c = +((a + b) / 2).toFixed(2); }
      if (!(c > a && c < b)) c = (a + b) / 2;
    }
    var v = S.df(c);
    return isFinite(S.f(c)) && isFinite(v) && sgn(v) === g.s ? c : g.t;
  }
  function signTable(S, inf) {
    var r0 = ["<th>" + tex("x") + "</th>"], r1 = ["<th>" + u("test") + "</th>"], r2s = ["<th>" + tex("f'(x)") + "</th>"], r3 = ["<th>" + tex("f(x)") + "</th>"], last = S.seg.length - 1;
    S.seg.forEach(function (g, j) {
      var aInf = inf && j === 0, bInf = inf && j === last;
      r0.push("<td>" + tex(intTex(g.a, g.b, aInf, bInf)) + "</td>");
      if (g.s === 0) { r1.push('<td class="nd">—</td>'); r2s.push('<td class="nd">∄</td>'); r3.push('<td class="nd">' + u("noDom") + "</td>"); }
      else {
        var t = testPt(S, g, aInf, bInf);
        r1.push("<td>" + tex("f'(" + nn(t) + ")" + (g.s > 0 ? "\\gt0" : "\\lt0")) + "</td>");
        r2s.push('<td class="' + (g.s > 0 ? "p" : "m") + '">' + (g.s > 0 ? "+" : "−") + "</td>");
        r3.push('<td class="ar ' + (g.s > 0 ? "p" : "m") + '">' + (g.s > 0 ? "↗" : "↘") + "</td>");
      }
      var e = S.ev[j]; if (!e) return;
      r0.push('<td class="pt">' + tex(nn(e.x)) + "</td>"); r1.push('<td class="pt"></td>');
      r2s.push('<td class="pt">' + (e.k === "z" ? "0" : "∄") + "</td>");
      r3.push('<td class="pt">' + (e.k === "z" ? (e.t1 === "max" ? u("mx") : e.t1 === "min" ? u("mn") : "—") : e.k === "h" || !isFinite(e.y) ? "∄" : "") + "</td>");
    });
    return '<div class="tbl-wrap"><table class="data sm sgn">' + [r0, r1, r2s, r3].map(function (r) { return "<tr>" + r.join("") + "</tr>"; }).join("") + "</table></div>";
  }
  // intervals de creixement i decreixement (ajuntant els trams separats per un punt crític que no és extrem)
  function monoHtml(S, inf) {
    var runs = [], cur = null, last = S.seg.length - 1;
    S.seg.forEach(function (g, j) {
      var prev = S.ev[j - 1];
      if (cur && g.s === cur.s && prev && prev.k === "z") cur.b = j; else { cur = { s: g.s, a: j, b: j }; runs.push(cur); }
    });
    function iv(r) { return intTex(S.seg[r.a].a, S.seg[r.b].b, inf && r.a === 0, inf && r.b === last); }
    var up = runs.filter(function (r) { return r.s > 0; }).map(iv), dn = runs.filter(function (r) { return r.s < 0; }).map(iv);
    return "<p><strong>" + u("incOn") + "</strong> " + (up.length ? tex(up.join("\\cup ")) : "—") + "<br><strong>" + u("decOn") + "</strong> " + (dn.length ? tex(dn.join("\\cup ")) : "—") + "</p>";
  }
  function ptTex(x, y) { return "(" + nn(x) + "," + nn(y) + ")"; }
  function extHtml(S) {
    var z = S.ev.filter(function (e) { return e.k === "z"; });
    if (!z.length) return "<p>" + u("noCrit") + "</p>";
    return "<p>" + z.map(function (e) {
      return e.t1 === "max" ? '<span class="badge ok">' + u("maxR") + "</span> " + tex(ptTex(e.x, e.y)) : e.t1 === "min" ? '<span class="badge as">' + u("minR") + "</span> " + tex(ptTex(e.x, e.y)) : tex("x=" + nn(e.x)) + ": " + u("noExt");
    }).join("<br>") + "</p>";
  }
  // gràfica pintada de verd (creix) i roig (decreix)
  function monoCurves(S) {
    return S.seg.filter(function (g) { return g.s !== 0; }).map(function (g) { return { f: S.f, a: g.a, b: g.b, col: g.s > 0 ? "var(--ok)" : "var(--bad)" }; });
  }
  function extMarks(S) {
    return S.ev.filter(function (e) { return e.k === "z" && e.t1 !== "none"; }).map(function (e) { return { x: e.x, y: e.y, col: e.t1 === "max" ? "var(--ok)" : "var(--bad)" }; });
  }
  // finestra que mostra tots els punts crítics
  function autoView(S, def) {
    var xs = S.ev.map(function (e) { return e.x; });
    var x0 = xs.length ? Math.min.apply(null, xs) - 3 : def[0], x1 = xs.length ? Math.max.apply(null, xs) + 3 : def[1];
    if (x1 - x0 < 6) { var c = (x0 + x1) / 2; x0 = c - 3; x1 = c + 3; }
    var yy = autoY([S.f], x0, x1);
    S.ev.forEach(function (e) { if (isFinite(e.y)) { yy[0] = Math.min(yy[0], e.y - 1); yy[1] = Math.max(yy[1], e.y + 1); } });
    return [x0, x1, yy[0], yy[1]];
  }

  /* ---------- figures estàtiques ---------- */
  var FIGS = {
    tan: function () {
      var f = F("x^2/2+1");
      return { v: [-1, 4, -0.5, 7], curves: [{ f: f }, { f: lineF(1, 1, 1.5), col: "var(--accent-2)" }], pts: [{ x: 1, y: 1.5 }], guides: [{ x: 1, y: 1.5 }],
        labels: [{ x: 0.85, y: 2.2, t: "P(a, f(a))", anchor: "end" }, { x: 3.2, y: 3.1, t: t3("m = f′(a)", "m = f′(a)", "m = f′(a)"), anchor: "start" }] };
    },
    tn: function () {
      var f = F("x^2/4+1"), c = 2.4, hh = 8 * RATIO / 2;
      return { v: [-2, 6, c - hh, c + hh], curves: [{ f: f }, { f: lineF(1, 2, 2), col: "var(--accent-2)" }, { f: lineF(-1, 2, 2), col: "var(--r3)" }], pts: [{ x: 2, y: 2 }],
        labels: [{ x: 4.4, y: 3.6, t: t3("tangent", "tangente", "tangent"), anchor: "start" }, { x: -0.2, y: 4.6, t: "normal", anchor: "start" }, { x: 2.25, y: 1.55, t: "P", anchor: "start" }] };
    },
    mono: function () {
      var f = F("x^3-3x");
      return { v: [-2.6, 2.6, -4, 4], curves: [{ f: f, b: -1, col: "var(--ok)" }, { f: f, a: -1, b: 1, col: "var(--bad)" }, { f: f, a: 1, col: "var(--ok)" }],
        labels: [{ x: -2, y: 3, t: "f′ > 0 ↗" }, { x: 0, y: 3, t: "f′ < 0 ↘" }, { x: 2, y: 3, t: "f′ > 0 ↗" }] };
    },
    ext: function () {
      var f = F("x^3-3x");
      return { v: [-2.6, 2.6, -4, 4], curves: [{ f: f }, { f: function () { return 2; }, a: -1.8, b: -0.2, col: "var(--accent-2)" }, { f: function () { return -2; }, a: 0.2, b: 1.8, col: "var(--accent-2)" }],
        mark: [{ x: -1, y: 2, col: "var(--ok)" }, { x: 1, y: -2, col: "var(--bad)" }],
        labels: [{ x: -1, y: 2.7, t: t3("màxim relatiu", "máximo relativo", "relative max") }, { x: 1, y: -2.9, t: t3("mínim relatiu", "mínimo relativo", "relative min") }] };
    },
    x3: function () {
      return { v: [-2, 2, -3, 3], curves: [{ f: F("x^3") }, { f: function () { return 0; }, a: -1, b: 1, col: "var(--accent-2)" }], pts: [{ x: 0, y: 0 }],
        labels: [{ x: 0.15, y: -0.8, t: t3("f′(0) = 0, però no és extrem", "f′(0) = 0, pero no es extremo", "f′(0) = 0, but no extremum"), anchor: "start" }] };
    },
    absf: function () {
      var f = F("x^3-6x^2+9x+2");
      return { v: [-0.6, 5.8, -2, 25], curves: [{ f: f, col: "var(--border)" }, { f: f, a: 0, b: 5 }], guides: [{ x: 0 }, { x: 5 }],
        pts: [{ x: 1, y: 6 }], mark: [{ x: 5, y: 22, col: "var(--ok)" }, { x: 0, y: 2, col: "var(--bad)" }, { x: 3, y: 2, col: "var(--bad)" }],
        labels: [{ x: 1, y: 8.2, t: t3("màx. relatiu", "máx. relativo", "relative max") }, { x: 4.8, y: 23.2, t: t3("màx. absolut", "máx. absoluto", "absolute max"), anchor: "end" }, { x: 3, y: -0.4, t: t3("mín. absolut", "mín. absoluto", "absolute min") }] };
    }
  };
  function wFigs() {
    document.querySelectorAll("[data-g]").forEach(function (el) {
      var mk = FIGS[el.getAttribute("data-g")]; if (!mk) return;
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("class", "lp-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Gràfica");
      el.appendChild(svg);
      onLang(function () { plot(svg, mk()); });
    });
  }

  /* ---------- widgets: recta tangent i recta normal ---------- */
  function wTN(id, normal) {
    var w = document.getElementById(id); if (!w) return;
    var PRE = normal ? [
      { e: "x^2-4x+5", a: 3, r: [-1, 5], v: [-2, 7, 2.6] }, { e: "sqrt(x)", a: 4, r: [0.5, 8], v: [-1, 9, 1.5] }, { e: "x^3-3x", a: 1, r: [-2, 2], v: [-3.5, 3.5, 0] },
      { e: "2/x", a: 2, r: [0.4, 5], v: [-1, 6, 1.5] }, { e: "ln(x)", a: 1, r: [0.2, 6], v: [-1, 7, 0] }
    ] : [
      { e: "x^2-4x+5", a: 3, r: [-0.5, 5.5], v: [-1, 6, -1, 10] }, { e: "x*e^x", a: 0, r: [-3.5, 1.5], v: [-4, 2, -1.5, 5] }, { e: "ln(x^2-3)", a: 2, r: [1.8, 4.8], v: [-5, 5, -4, 3] },
      { e: "x^3-3x+1", a: 2, r: [-2.5, 2.5], v: [-3, 3, -6, 8] }, { e: "(x+1)/(x-1)", a: 2, r: [1.2, 4.8], v: [-3, 5, -6, 8] }
    ];
    // la normal només es veu perpendicular si els dos eixos tenen la mateixa escala
    if (normal) PRE.forEach(function (P) { var hh = (P.v[1] - P.v[0]) * RATIO / 2; P.v = [P.v[0], P.v[1], P.v[2] - hh, P.v[2] + hh]; });
    var st = 0, fi = $(w, "f"), ra = $(w, "a"), svg = w.querySelector("svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, normal ? "pNorm" : "pTan", function (i) { st = i; fi.value = PRE[i].e; setup(); });
    fi.addEventListener("input", function () { if (st >= 0) { ra.min = -5; ra.max = 5; } st = -1; draw(); });
    ra.addEventListener("input", draw);
    function setup() { var P = PRE[st]; ra.min = P.r[0]; ra.max = P.r[1]; ra.step = 0.1; ra.value = P.a; draw(); }
    function draw() {
      var n, f, dn, df;
      try { n = parse(fi.value); f = compile(n); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
      try { dn = D(n); df = compile(dn); } catch (e) { info.textContent = u("noDiff"); return; }
      var a = +ra.value, fa = f(a), m = df(a), at = nn(a), v;
      $(w, "av").textContent = numTxt(a);
      if (st >= 0) v = PRE[st].v;
      else if (normal) { var yc = isFinite(fa) ? fa : 0; v = [a - 4, a + 4, yc - 4 * RATIO, yc + 4 * RATIO]; }
      else { var yy = autoY([f], a - 4, a + 4); v = [a - 4, a + 4, yy[0], yy[1]]; }
      var h = "<p>" + tex("f(x)=" + T(n)) + "</p>";
      if (!isFinite(fa) || !isFinite(m)) {
        info.innerHTML = h + "<p>" + (isFinite(fa) ? u("noD") : u("noF")) + "</p>";
        plot(svg, { v: v, curves: [{ f: f }], guides: [{ x: a }] }); return;
      }
      h += "<p>① " + u("point") + ": " + tex(eqv("f(" + at + ")", fa) + "\\ \\Rightarrow\\ P" + ptTex(a, fa)) + "</p>";
      h += "<p>② " + u("slope") + ": " + tex("f'(x)=" + texD(dn)) + "<br>" + tex(eqv("m=f'(" + at + ")", m)) + "</p>";
      h += "<p>③ " + u("tline") + ": " + tex(ptSl(m, a, fa) + "\\ \\Rightarrow\\ " + lineT(m, a, fa)) + "</p>";
      var curves = [{ f: f }, { f: lineF(m, a, fa), col: "var(--accent-2)" }], va = [];
      if (normal) {
        if (Math.abs(m) < 1e-9) { h += "<p>④ " + u("nline") + ": " + tex("x=" + at) + " (" + u("horiz") + ")</p>"; va.push(a); }
        else {
          var mn = -1 / m;
          h += "<p>④ " + u("nline") + ": " + tex(eqv("m_n=-\\dfrac{1}{f'(" + at + ")}", mn)) + "<br>" + tex(ptSl(mn, a, fa) + "\\ \\Rightarrow\\ " + lineT(mn, a, fa)) + "</p>";
          h += '<p style="color:var(--muted)">' + u("perp") + ": " + tex("m\\cdot m_n=" + nn(m) + "\\cdot\\left(" + nn(mn) + "\\right)=-1") + "</p>";
          curves.push({ f: lineF(mn, a, fa), col: "var(--r3)" });
        }
      }
      info.innerHTML = h;
      plot(svg, { v: v, curves: curves, va: va, pts: [{ x: a, y: fa }] });
    }
    onLang(setup);
  }

  /* ---------- widget: tangents amb un pendent donat ---------- */
  function wPar() {
    var w = document.getElementById("w-par"); if (!w) return;
    var PRE = [{ e: "x^3-3x+1", m: 9, v: [-3, 3, -20, 22] }, { e: "x^3-3x^2", m: 9, v: [-2, 4.2, -25, 25] }, { e: "x^2-6x+1", m: 0, v: [-1, 7, -10, 8] }, { e: "e^x", m: 1, v: [-3, 3, -1, 8] }];
    var st = 0, fi = $(w, "f"), rm = $(w, "m"), svg = w.querySelector("svg"), info = w.querySelector(".info");
    rm.min = -10; rm.max = 15; rm.step = 0.5; rm.value = PRE[0].m;
    presetBtns($(w, "presets"), PRE.length, "pPar", function (i) { st = i; fi.value = PRE[i].e; rm.value = PRE[i].m; draw(); });
    fi.addEventListener("input", function () { st = -1; draw(); });
    rm.addEventListener("input", draw);
    function draw() {
      var n, f, dn, df, m = +rm.value;
      $(w, "mv").textContent = numTxt(m);
      try { n = parse(fi.value); f = compile(n); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
      try { dn = D(n); df = compile(dn); } catch (e) { info.textContent = u("noDiff"); return; }
      var v = st >= 0 ? PRE[st].v : (function () { var yy = autoY([f], -5, 5); return [-5, 5, yy[0], yy[1]]; })();
      var xs = roots(function (x) { return df(x) - m; }, v[0], v[1]).filter(function (x) { return isFinite(f(x)); });
      var h = "<p>" + tex("f(x)=" + T(n) + ",\\quad f'(x)=" + texD(dn)) + "</p><p>" + tex("f'(x)=" + nn(m)) + " ⇒ " + (xs.length ? tex("x=" + xs.map(nn).join(",\\ x=")) : u("noPts")) + "</p>";
      var curves = [{ f: f }, { f: function (x) { return m * x; }, col: "var(--plus)" }], pts = [];
      xs.forEach(function (x) {
        var fx = f(x);
        h += "<p>" + tex("P" + ptTex(x, fx) + ":\\ " + ptSl(m, x, fx) + "\\ \\Rightarrow\\ " + lineT(m, x, fx)) + "</p>";
        curves.push({ f: lineF(m, x, fx), col: "var(--accent-2)" }); pts.push({ x: x, y: fx });
      });
      info.innerHTML = h;
      plot(svg, { v: v, curves: curves, pts: pts });
    }
    onLang(draw);
  }

  /* ---------- widget: monotonia ---------- */
  function wMono() {
    var w = document.getElementById("w-mono"); if (!w) return;
    var PRE = [{ e: "x^3-3x^2-9x+1", v: [-3.5, 5.5, -30, 12], a: -2 }, { e: "x^2/(x-1)", v: [-3, 5, -8, 10], a: 0.5 }, { e: "x*e^(-x)", v: [-1, 6, -3, 0.8], a: 0 },
      { e: "x^3", v: [-2, 2, -4, 4], a: -1 }, { e: "x-ln(x)", v: [-0.5, 5, -0.5, 4], a: 0.5 }];
    var st = 0, fi = $(w, "f"), ra = $(w, "a"), svg = w.querySelector("svg"), info = w.querySelector(".info"), tb = $(w, "tbl"), S = null, view = null;
    presetBtns($(w, "presets"), PRE.length, "pMono", function (i) { st = i; fi.value = PRE[i].e; setup(); });
    fi.addEventListener("input", function () { st = -1; setup(); });
    ra.addEventListener("input", draw);
    function setup() {
      try { S = studyF(parse(fi.value), -40, 40); fi.classList.remove("bad"); }
      catch (e) { S = null; fi.classList.toggle("bad", !(e instanceof NoDiff)); info.textContent = e instanceof NoDiff ? u("noDiff") : u("bad"); tb.innerHTML = ""; return; }
      view = st >= 0 ? PRE[st].v : autoView(S, [-6, 6]);
      var span = view[1] - view[0];
      ra.min = view[0] + span * 0.04; ra.max = view[1] - span * 0.04; ra.step = 0.05; ra.value = st >= 0 ? PRE[st].a : (view[0] + view[1]) / 2;
      tb.innerHTML = signTable(S, true) + monoHtml(S, true);
      draw();
    }
    function draw() {
      if (!S) return;
      var a = +ra.value, fa = S.f(a), m = S.df(a);
      $(w, "av").textContent = numTxt(a);
      var h = "<p>" + tex("f(x)=" + T(S.n)) + "<br>" + tex("f'(x)=" + texD(S.dn)) + "</p>", curves = monoCurves(S), pts = [];
      if (isFinite(fa) && isFinite(m)) {
        var s = Math.abs(m) < 0.02 ? 0 : sgn(m);
        h += "<p>" + tex("f'(" + numTex(+a.toFixed(2)) + ")=" + numTex(+m.toFixed(3))) + " " + (s > 0 ? "\\(\\gt0\\)" : s < 0 ? "\\(\\lt0\\)" : "≈ 0") + "</p>";
        h += "<p>" + (s > 0 ? '<span class="badge ok">↗ ' + u("inc") + "</span>" : s < 0 ? '<span class="badge as">↘ ' + u("dec") + "</span>" : '<span class="badge ev">→ ' + u("flat") + "</span>") + "</p>";
        curves.push(segAt(m, a, fa, view, "var(--accent-2)")); pts.push({ x: a, y: fa });
      } else h += "<p>" + u("noF") + "</p>";
      info.innerHTML = h.replace(/\\\((.*?)\\\)/g, function (_, x) { return tex(x); });
      plot(svg, { v: view, curves: curves, pts: pts, guides: [{ x: a }] });
    }
    onLang(setup);
  }

  /* ---------- widget: màxims i mínims ---------- */
  function critRows(S) {
    var z = S.ev.filter(function (e) { return e.k === "z"; });
    if (!z.length) return "<p>" + u("noCrit") + "</p>";
    var T1 = { max: u("maxR"), min: u("minR"), none: u("noExt") };
    var h = '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + tex("x") + "</th><th>" + tex("f(x)") + "</th><th>" + u("c2") + "</th><th>" + u("c1") + "</th><th>" + u("type") + "</th></tr></thead><tbody>";
    z.forEach(function (e) {
      var j = S.ev.indexOf(e), l = S.seg[j].s, r = S.seg[j + 1].s, sg = function (s) { return s > 0 ? "+" : s < 0 ? "-" : "\\nexists"; };
      var c2 = e.t2 === undefined || e.t2 === "?" ? "—" : tex(eqv("f''(" + nn(e.x) + ")", e.v2) + (e.t2 === "max" ? "\\lt0" : e.t2 === "min" ? "\\gt0" : "")) + (e.t2 === "undec" ? " (" + u("undec") + ")" : "");
      var cls = e.t1 === "max" ? "v-mx" : e.t1 === "min" ? "v-mn" : "";
      h += "<tr><td>" + tex(nn(e.x)) + "</td><td>" + tex(nn(e.y)) + "</td><td>" + c2 + "</td><td>" + tex(sg(l) + "\\ \\to\\ " + sg(r)) + "</td><td" + (cls ? ' class="' + cls + '"' : "") + ">" + T1[e.t1] + (e.t1 !== "none" ? " " + tex(ptTex(e.x, e.y)) : "") + "</td></tr>";
    });
    return h + "</tbody></table></div>";
  }
  function wExt() {
    var w = document.getElementById("w-ext"); if (!w) return;
    var PRE = [{ e: "x^3-3x^2-9x+1", v: [-3.5, 5.5, -30, 12] }, { e: "x^4-2x^2", v: [-2.2, 2.2, -1.5, 3] }, { e: "x^4-4x^3", v: [-1.5, 4.5, -32, 12] },
      { e: "x^2/(x-1)", v: [-3, 5, -8, 10] }, { e: "x+4/x", v: [-7, 7, -10, 10] }, { e: "x*e^x", v: [-5, 1.2, -0.8, 2.5] }];
    var st = 0, fi = $(w, "f"), svg = w.querySelector("svg"), info = w.querySelector(".info"), tb = $(w, "tbl");
    presetBtns($(w, "presets"), PRE.length, "pExt", function (i) { st = i; fi.value = PRE[i].e; draw(); });
    fi.addEventListener("input", function () { st = -1; draw(); });
    function draw() {
      var S;
      try { S = studyF(parse(fi.value), -40, 40); fi.classList.remove("bad"); }
      catch (e) { fi.classList.toggle("bad", !(e instanceof NoDiff)); info.textContent = e instanceof NoDiff ? u("noDiff") : u("bad"); tb.innerHTML = ""; return; }
      var z = S.ev.filter(function (e) { return e.k === "z"; });
      var h = "<p>" + tex("f(x)=" + T(S.n)) + "</p><p>" + tex("f'(x)=" + texD(S.dn)) + "</p>";
      h += "<p>" + u("crit") + ": " + (z.length ? tex("f'(x)=0\\ \\Rightarrow\\ x=" + z.map(function (e) { return nn(e.x); }).join(",\\ x=")) : u("noCrit")) + "</p>";
      if (S.d2) h += "<p>" + tex("f''(x)=" + texD(S.d2n)) + "</p>";
      info.innerHTML = h + extHtml(S);
      tb.innerHTML = critRows(S);
      var v = st >= 0 ? PRE[st].v : autoView(S, [-6, 6]);
      plot(svg, { v: v, curves: [{ f: S.f }], mark: extMarks(S), pts: z.filter(function (e) { return e.t1 === "none"; }).map(function (e) { return { x: e.x, y: e.y }; }) });
    }
    onLang(draw);
  }

  /* ---------- extrems absoluts en [a, b] ---------- */
  function absStudy(n, a, b) {
    var S = studyF(n, a, b), f = S.f, c = [{ x: a, k: "e" }];
    S.ev.forEach(function (e) { if (e.k === "z" && e.x > a + 1e-9 && e.x < b - 1e-9) c.push({ x: e.x, k: "z" }); });
    c.push({ x: b, k: "e" });
    c.forEach(function (q) { q.y = f(q.x); });
    var ys = c.map(function (q) { return q.y; }).filter(isFinite), M = Math.max.apply(null, ys), m = Math.min.apply(null, ys);
    c.forEach(function (q) { q.max = isFinite(q.y) && Math.abs(q.y - M) < 1e-9 * (1 + Math.abs(M)); q.min = isFinite(q.y) && Math.abs(q.y - m) < 1e-9 * (1 + Math.abs(m)); });
    var cont = !S.ev.some(function (e) { return e.k !== "z"; }) && c.every(function (q) { return isFinite(q.y); });
    return { S: S, c: c, M: M, m: m, cont: cont };
  }
  function absHtml(A) {
    var h = '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + u("cand") + "</th><th></th><th>" + tex("f(x)") + "</th></tr></thead><tbody>";
    A.c.forEach(function (q) {
      var cls = q.max ? ' class="v-mx"' : q.min ? ' class="v-mn"' : "";
      h += "<tr><td>" + tex("x=" + nn(q.x)) + "</td><td>" + (q.k === "e" ? u("endp") : u("critp")) + "</td><td" + cls + ">" + tex(isFinite(q.y) ? nn(q.y) : "\\nexists") + "</td></tr>";
    });
    h += "</tbody></table></div>";
    function at(k) { return A.c.filter(function (q) { return q[k]; }).map(function (q) { return nn(q.x); }).join(",\\ x="); }
    h += "<p>" + '<span class="badge ok">' + u("absMax") + "</span> " + tex(nn(A.M) + "\\ \\text{" + t3("en", "en", "at") + " } x=" + at("max")) + "<br>" +
      '<span class="badge as">' + u("absMin") + "</span> " + tex(nn(A.m) + "\\ \\text{" + t3("en", "en", "at") + " } x=" + at("min")) + "</p>";
    if (!A.cont) h += '<p class="msg-bad">' + u("notCont") + "</p>";
    return h;
  }
  function absMarks(A) {
    var mk = [];
    A.c.forEach(function (q) { if (q.max) mk.push({ x: q.x, y: q.y, col: "var(--ok)" }); else if (q.min) mk.push({ x: q.x, y: q.y, col: "var(--bad)" }); });
    return mk;
  }
  function wAbs() {
    var w = document.getElementById("w-abs"); if (!w) return;
    var PRE = [{ e: "x^3-6x^2+9x+2", r: [-0.5, 5.5], a: 0, b: 5, v: [-0.8, 5.8, -6, 38] }, { e: "x^3-3x^2-9x+1", r: [-3, 5], a: -2, b: 4, v: [-3.3, 5.3, -30, 10] },
      { e: "x*e^(-x)", r: [-0.5, 5], a: 0, b: 3, v: [-0.7, 5.2, -1, 0.6] }, { e: "-x^3+9x^2-15x+40", r: [-1, 7], a: 0, b: 6, v: [-1.3, 7.3, 0, 75] }];
    var st = 0, ra = $(w, "a"), rb = $(w, "b"), svg = w.querySelector("svg"), fn = $(w, "fn"), info = w.querySelector(".cands");
    presetBtns($(w, "presets"), PRE.length, "pAbs", function (i) { st = i; setup(); });
    ra.addEventListener("input", function () { if (+ra.value > +rb.value - 0.2) ra.value = +rb.value - 0.2; draw(); });
    rb.addEventListener("input", function () { if (+rb.value < +ra.value + 0.2) rb.value = +ra.value + 0.2; draw(); });
    function setup() { var P = PRE[st]; [ra, rb].forEach(function (r) { r.min = P.r[0]; r.max = P.r[1]; r.step = 0.1; }); ra.value = P.a; rb.value = P.b; draw(); }
    function draw() {
      var P = PRE[st], n = parse(P.e), a = +ra.value, b = +rb.value, A = absStudy(n, a, b), f = A.S.f;
      $(w, "av").textContent = numTxt(a); $(w, "bv").textContent = numTxt(b);
      fn.innerHTML = tex("f(x)=" + T(n) + "\\ \\text{" + t3("en", "en", "on") + " }[" + nn(a) + "," + nn(b) + "]") + "<br>" + tex("f'(x)=" + texD(A.S.dn));
      info.innerHTML = absHtml(A);
      plot(svg, { v: P.v, curves: [{ f: f, col: "var(--border)" }, { f: f, a: a, b: b }], guides: [{ x: a }, { x: b }], pts: A.c.map(function (q) { return { x: q.x, y: q.y }; }), mark: absMarks(A) });
    }
    onLang(setup);
  }

  /* ---------- widget: optimització amb la funció donada ---------- */
  function optOf(f, df, dom, kind) {
    var c = [dom[0], dom[1]].concat(roots(df, dom[0], dom[1]).filter(function (x) { return x > dom[0] && x < dom[1]; }));
    var best = null;
    c.forEach(function (x) { var y = f(x); if (isFinite(y) && (best === null || (kind === "max" ? y > best.y : y < best.y))) best = { x: x, y: y }; });
    return best;
  }
  function wOpt() {
    var w = document.getElementById("w-opt"); if (!w) return;
    var PRE = [
      { e: "-0.1x^2+2.5x-10", dt: "-0.2x+2.5", fn: "B", vr: "x", dom: [0, 25], step: 0.1, x: 5, k: "max", v: [-1, 26, -11, 7.5],
        d: function () { return t3("x: tones venudes; B(x): benefici en milions d'€.", "x: toneladas vendidas; B(x): beneficio en millones de €.", "x: tonnes sold; B(x): profit in millions of €."); } },
      { e: "-0.1x+2.5-10/x", dt: "-0.1+\\dfrac{10}{x^2}", fn: "g", vr: "x", dom: [1, 25], step: 0.1, x: 3, k: "max", v: [0, 26, -8, 1.5],
        d: function () { return t3("x: tones; g(x) = B(x)/x: benefici per tona (milions d'€).", "x: toneladas; g(x) = B(x)/x: beneficio por tonelada (millones de €).", "x: tonnes; g(x) = B(x)/x: profit per tonne (millions of €)."); } },
      { e: "x+10+400/x", dt: "1-\\dfrac{400}{x^2}", fn: "CM", vr: "x", dom: [5, 80], step: 0.5, x: 50, k: "min", v: [0, 82, 0, 110],
        d: function () { return t3("x: unitats fabricades; CM(x): cost mitjà per unitat (€).", "x: unidades fabricadas; CM(x): coste medio por unidad (€).", "x: units made; CM(x): average cost per unit (€)."); } },
      { e: "t^3-15t^2+63t+40", dt: "3t^2-30t+63", fn: "C", vr: "t", dom: [0, 8], step: 0.05, x: 6, k: "max", v: [-0.5, 8.5, 0, 140],
        d: function () { return t3("t: hores (de 0 a 8); C(t): nivell de contaminació.", "t: horas (de 0 a 8); C(t): nivel de contaminación.", "t: hours (0 to 8); C(t): pollution level."); } }
    ];
    var st = 0, rx = $(w, "x"), svg = w.querySelector("svg"), fn = $(w, "fn"), out = w.querySelector(".opt-out"), P, f, dn, df, best;
    presetBtns($(w, "presets"), PRE.length, "pOpt", function (i) { st = i; setup(); });
    rx.addEventListener("input", draw);
    $(w, "show").addEventListener("click", function () { rx.value = best.x; draw(); });
    function setup() {
      P = PRE[st]; var n = parse(P.e); f = compile(n); dn = D(n); df = compile(dn); best = optOf(f, df, P.dom, P.k);
      rx.min = P.dom[0]; rx.max = P.dom[1]; rx.step = P.step; rx.value = P.x;
      draw();
    }
    function draw() {
      var x = +rx.value, y = f(x), m = df(x), V = P.vr, nm = P.fn + "(" + V + ")";
      $(w, "xn").innerHTML = tex(V + "="); $(w, "xv").textContent = numTxt(x);
      fn.innerHTML = "<p>" + tex(nm + "=" + T(P.e) + ",\\quad " + V + "\\in[" + nn(P.dom[0]) + "," + nn(P.dom[1]) + "]") + "<br>" + tex(P.fn + "'(" + V + ")=" + (lang === "en" ? P.dt : P.dt.replace(/(\d)\.(\d)/g, "$1{,}$2"))) + "</p><p style=\"color:var(--muted)\">" + P.d() + "</p>";
      var s = Math.abs(m) < 1e-3 * (1 + Math.abs(y)) ? 0 : sgn(m);
      var h = "<p>" + tex(P.fn + "(" + r2(x) + ")=" + r2(y) + ",\\quad " + P.fn + "'(" + r2(x) + ")=" + numTex(+m.toFixed(3))) + "</p><p>" + (s > 0 ? u("goUp") : s < 0 ? u("goDn") : "→ " + u("flat")) + "</p>";
      if (Math.abs(x - best.x) < P.step * 0.6) h += '<p class="msg-ok">✓ ' + u("found") + " " + u(P.k === "max" ? "optMax" : "optMin") + " " + tex(V + "=" + numTex(+best.x.toFixed(4))) + ": " + tex(P.fn + "(" + numTex(+best.x.toFixed(4)) + ")=" + numTex(+best.y.toFixed(4))) + "</p>";
      out.innerHTML = h;
      plot(svg, { v: P.v, curves: [{ f: f, a: P.dom[0], b: P.dom[1] }, segAt(m, x, y, P.v, "var(--accent-2)", 0.12)], pts: [{ x: x, y: y }], guides: [{ x: x, y: y }] });
    }
    onLang(setup);
  }

  /* ---------- widget: construïm la funció (dibuix + gràfica) ---------- */
  function P2(x, y) { return { x: +x.toFixed(1), y: +y.toFixed(1) }; }
  function ln2(p, q, cls) { return '<line class="' + cls + '" x1="' + p.x + '" y1="' + p.y + '" x2="' + q.x + '" y2="' + q.y + '"/>'; }
  function poly(ps, cls) { return '<polygon class="' + cls + '" points="' + ps.map(function (p) { return p.x + "," + p.y; }).join(" ") + '"/>'; }
  function txt(x, y, s, anchor, cls) { return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="' + (anchor || "middle") + '"' + (cls ? ' class="' + cls + '"' : "") + ">" + s + "</text>"; }
  // prisma obert per dalt (perspectiva cavallera): amplària w, fondària d, altura h
  function prism(ox, oy, wd, dp, ht, s, labs) {
    var k = 0.45, c = Math.cos(Math.PI / 6) * k, si = Math.sin(Math.PI / 6) * k;
    function P(u0, v0, z0) { return P2(ox + (u0 + z0 * c) * s, oy - (v0 + z0 * si) * s); }
    var A = P(0, 0, 0), Bq = P(wd, 0, 0), C = P(wd, ht, 0), Dq = P(0, ht, 0), A2 = P(0, 0, dp), B2 = P(wd, 0, dp), C2 = P(wd, ht, dp), D2 = P(0, ht, dp);
    var g = poly([A, Bq, C, Dq], "wt") + poly([Bq, B2, C2, C], "wt") + poly([Dq, C, C2, D2], "top");
    g += ln2(A, A2, "ed hid") + ln2(A2, B2, "ed hid") + ln2(A2, D2, "ed hid");
    g += poly([A, Bq, C, Dq], "ed") + ln2(Bq, B2, "ed") + ln2(B2, C2, "ed") + ln2(C, C2, "ed") + ln2(Dq, D2, "ed") + ln2(D2, C2, "ed");
    g += txt((A.x + Bq.x) / 2, A.y + 18, labs[0]) + txt((Bq.x + B2.x) / 2 + 8, (Bq.y + B2.y) / 2 + 12, labs[1], "start") + txt(A.x - 8, (A.y + Dq.y) / 2 + 4, labs[2], "end");
    return g;
  }
  var BUILD = [
    { e: "x^2+128/x", fn: "S", dom: [1.5, 8], step: 0.05, x: 2, v: [0, 8.5, 0, 110], kind: "min",
      head: function () { return tex("x^2y=32\\Rightarrow y=\\dfrac{32}{x^2}") + "&emsp;" + tex("S=x^2+4xy\\Rightarrow S(x)=x^2+\\dfrac{128}{x}"); },
      draw: function (x) {
        var y = 32 / (x * x), c = Math.cos(Math.PI / 6) * 0.45, si = Math.sin(Math.PI / 6) * 0.45, s = Math.min(300 / (x + x * c), 220 / (y + x * si));
        var ox = (420 - (x + x * c) * s) / 2, oy = 300 - (300 - (y + x * si) * s) / 2;
        return prism(ox, oy, x, x, y, s, ["x = " + numTxt(+x.toFixed(2)) + " m", "x", "y = " + numTxt(+y.toFixed(2)) + " m"]);
      },
      info: function (x) { var y = 32 / (x * x); return tex("x=" + r2(x) + "\\text{ m},\\quad y=\\dfrac{32}{x^2}=" + r2(y) + "\\text{ m},\\quad S=" + r2(x * x + 128 / x) + "\\text{ m}^2"); },
      unit: "\\text{ m}^2" },
    { e: "x(12-2x)^2", fn: "V", dom: [0.2, 5.8], step: 0.05, x: 1, v: [0, 6, 0, 140], kind: "max",
      head: function () { return tex(t3("\\text{base: }(12-2x)^2,\\ \\text{altura: }x", "\\text{base: }(12-2x)^2,\\ \\text{altura: }x", "\\text{base: }(12-2x)^2,\\ \\text{height: }x")) + "&emsp;" + tex("V(x)=x\\,(12-2x)^2"); },
      draw: function (x) {
        var s = 16, ox = 16, oy = 50, L = 12, g = "", b = L - 2 * x;
        g += '<rect class="sheet" x="' + ox + '" y="' + oy + '" width="' + L * s + '" height="' + L * s + '"/>';
        [[0, 0], [L - x, 0], [0, L - x], [L - x, L - x]].forEach(function (q) { g += '<rect class="cut" x="' + (ox + q[0] * s) + '" y="' + (oy + q[1] * s) + '" width="' + x * s + '" height="' + x * s + '"/>'; });
        g += '<rect class="fold" x="' + (ox + x * s) + '" y="' + (oy + x * s) + '" width="' + b * s + '" height="' + b * s + '"/>';
        g += txt(ox + x * s / 2, oy - 6, "x") + txt(ox + L * s / 2, oy + L * s + 18, "12 cm") + txt(ox + L * s / 2, oy + (L - x) * s - 6, "12 − 2x", "middle", "sm");
        // la caixa, a la dreta, sempre a la mida més gran que hi cap
        var c = Math.cos(Math.PI / 6) * 0.45, si = Math.sin(Math.PI / 6) * 0.45, sb = Math.min(160 / (b * (1 + c)), 170 / (x + b * si));
        g += prism(236 + (172 - b * (1 + c) * sb) / 2, 160 + (x + b * si) * sb / 2, b, b, x, sb, [numTxt(+b.toFixed(2)), numTxt(+b.toFixed(2)), "x = " + numTxt(+x.toFixed(2))]);
        return g;
      },
      info: function (x) { var b = 12 - 2 * x; return tex("x=" + r2(x) + "\\text{ cm},\\quad 12-2x=" + r2(b) + "\\text{ cm},\\quad V=" + r2(x * b * b) + "\\text{ cm}^3"); },
      unit: "\\text{ cm}^3" },
    { e: "x(400-2x)", fn: "A", dom: [5, 195], step: 1, x: 40, v: [0, 200, 0, 22000], kind: "max",
      head: function () { return tex("2x+y=400\\Rightarrow y=400-2x") + "&emsp;" + tex("A(x)=x\\,(400-2x)"); },
      draw: function (x) {
        var y = 400 - 2 * x, s = 0.95, L = (420 - y * s) / 2, R = L + y * s, top = 62, bot = top + x * s, g = "";
        g += '<rect class="river" x="6" y="18" width="408" height="' + (top - 18) + '"/>' + txt(210, 46, t3("riu", "río", "river"), "middle", "sm");
        g += '<rect class="area" x="' + L.toFixed(1) + '" y="' + top + '" width="' + (y * s).toFixed(1) + '" height="' + (x * s).toFixed(1) + '"/>';
        g += '<polyline class="fence" points="' + L.toFixed(1) + "," + top + " " + L.toFixed(1) + "," + bot.toFixed(1) + " " + R.toFixed(1) + "," + bot.toFixed(1) + " " + R.toFixed(1) + "," + top + '"/>';
        g += txt(L - 8, (top + bot) / 2 + 4, "x = " + numTxt(x), "end") + txt((L + R) / 2, bot + 20, "y = " + numTxt(y));
        return g;
      },
      info: function (x) { var y = 400 - 2 * x; return tex("x=" + r2(x) + "\\text{ m},\\quad y=400-2x=" + r2(y) + "\\text{ m},\\quad A=" + r2(x * y) + "\\text{ m}^2"); },
      unit: "\\text{ m}^2" },
    { e: "(30+x)(600-10x)", fn: "I", dom: [0, 40], step: 1, x: 5, v: [-1, 41, 0, 23000], kind: "max",
      head: function () { return tex(t3("\\text{persones: }30+x,\\ \\text{preu: }600-10x", "\\text{personas: }30+x,\\ \\text{precio: }600-10x", "\\text{people: }30+x,\\ \\text{price: }600-10x")) + "&emsp;" + tex("I(x)=(30+x)(600-10x)"); },
      draw: function (x) {
        var np = 30 + x, pr = 600 - 10 * x, sx = 4.8, sy = 0.36, ox = 70, oy = 262, g = "";
        g += ln2(P2(ox, oy), P2(ox + 345, oy), "axl") + ln2(P2(ox, oy), P2(ox, 20), "axl");
        g += '<rect class="area" x="' + ox + '" y="' + (oy - pr * sy).toFixed(1) + '" width="' + (np * sx).toFixed(1) + '" height="' + (pr * sy).toFixed(1) + '"/>';
        g += txt(ox + np * sx / 2, oy + 20, t3("persones: ", "personas: ", "people: ") + np) + txt(ox - 8, oy - pr * sy / 2, pr + " €", "end");
        g += txt(ox + np * sx / 2, oy - pr * sy / 2 + 5, "I = " + numTxt(np * pr) + " €");
        return g;
      },
      info: function (x) { return tex("x=" + x + ",\\quad " + t3("\\text{persones}", "\\text{personas}", "\\text{people}") + "=" + (30 + x) + ",\\quad " + t3("\\text{preu}", "\\text{precio}", "\\text{price}") + "=" + (600 - 10 * x) + "\\text{ €},\\quad I=" + numTex((30 + x) * (600 - 10 * x)) + "\\text{ €}"); },
      unit: "\\text{ €}" }
  ];
  function wBuild() {
    var w = document.getElementById("w-build"); if (!w) return;
    var st = 0, rx = $(w, "x"), dr = $(w, "draw"), gr = $(w, "graph"), fn = $(w, "fn"), out = w.querySelector(".opt-out"), P, f, df, best;
    presetBtns($(w, "presets"), BUILD.length, "pBuild", function (i) { st = i; setup(); });
    rx.addEventListener("input", draw);
    $(w, "show").addEventListener("click", function () { rx.value = best.x; draw(); });
    function setup() {
      P = BUILD[st]; var n = parse(P.e); f = compile(n); df = compile(D(n)); best = optOf(f, df, P.dom, P.kind);
      rx.min = P.dom[0]; rx.max = P.dom[1]; rx.step = P.step; rx.value = P.x;
      draw();
    }
    function draw() {
      var x = +rx.value, y = f(x);
      $(w, "xv").textContent = numTxt(x);
      fn.innerHTML = P.head();
      dr.setAttribute("viewBox", "0 0 420 300"); dr.innerHTML = P.draw(x);
      var h = "<p>" + P.info(x) + "</p>";
      if (Math.abs(x - best.x) < P.step * 0.6) h += '<p class="msg-ok">✓ ' + u("found") + " " + u(P.kind === "max" ? "optMax" : "optMin") + " " + tex("x=" + nn(best.x)) + ": " + tex(P.fn + "(" + nn(best.x) + ")=" + nn(best.y) + P.unit) + "</p>";
      out.innerHTML = h;
      plot(gr, { v: P.v, curves: [{ f: f, a: P.dom[0], b: P.dom[1] }], pts: [{ x: x, y: y }], guides: [{ x: x, y: y }] });
    }
    onLang(setup);
  }

  /* ---------- estudi complet d'una funció ---------- */
  function wLab() {
    var w = document.getElementById("w-lab"); if (!w) return;
    var PRE = [["x^3-3x^2-9x+1", "", ""], ["x^2/(x-1)", "", ""], ["(x^2-3)*e^x", "", ""], ["x-ln(x)", "", ""], ["x/(x^2+1)", "", ""], ["x^4-4x^3", "", ""], ["x^3-6x^2+9x+2", "0", "5"]];
    var fi = $(w, "f"), ai = $(w, "a"), bi = $(w, "b"), svg = w.querySelector("svg"), out = $(w, "out"), tb = $(w, "tbl");
    presetBtns($(w, "presets"), PRE.length, "pLab", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; bi.value = PRE[i][2]; draw(); });
    [fi, ai, bi].forEach(function (i) { i.addEventListener("input", draw); });
    function draw() {
      var n, a = null, b = null, iv = ai.value.trim() !== "" || bi.value.trim() !== "";
      try { n = parse(fi.value); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); out.textContent = u("bad"); tb.innerHTML = ""; return; }
      if (iv) {
        a = parseFr(ai.value); b = parseFr(bi.value);
        var okI = a && b && a.val() < b.val();
        ai.classList.toggle("bad", !okI); bi.classList.toggle("bad", !okI);
        if (!okI) { out.textContent = u("aBad"); tb.innerHTML = ""; return; }
        a = a.val(); b = b.val();
      } else { ai.classList.remove("bad"); bi.classList.remove("bad"); }
      var S, inf = !iv, note = "";
      try { S = studyF(n, iv ? a : -40, iv ? b : 40); } catch (e) { out.textContent = e instanceof NoDiff ? u("noDiff") : u("bad"); tb.innerHTML = ""; return; }
      if (!iv && S.ev.length > 12) { S = studyF(n, -8, 8); inf = false; note = '<p class="msg-bad">' + u("many") + " " + tex("[-8,8]") + ".</p>"; }
      var z = S.ev.filter(function (e) { return e.k === "z"; });
      var h = "<p>" + tex("f(x)=" + T(n)) + "</p><p>" + tex("f'(x)=" + texD(S.dn)) + "</p>";
      if (S.d2) h += "<p>" + tex("f''(x)=" + texD(S.d2n)) + "</p>";
      h += "<p>" + u("crit") + ": " + (z.length ? tex("x=" + z.map(function (e) { return nn(e.x); }).join(",\\ x=")) : u("noCrit")) + "</p>";
      h += note + monoHtml(S, inf) + extHtml(S);
      var A = null;
      if (iv) { A = absStudy(n, a, b); h += absHtml(A); }
      out.innerHTML = h;
      tb.innerHTML = "<p><strong>" + (iv ? u("inI") + " " + tex("[" + nn(a) + "," + nn(b) + "]") : u("inR")) + "</strong></p>" + signTable(S, inf) + (z.length ? critRows(S) : "");
      var v;
      if (iv) {
        var pad = (b - a) * 0.1, yy = autoY([S.f], a, b), ys = A.c.map(function (q) { return q.y; }).filter(isFinite), dy = (Math.max.apply(null, ys) - Math.min.apply(null, ys)) * 0.08 + 0.5;
        v = [a - pad, b + pad, Math.min(yy[0], Math.min.apply(null, ys) - dy), Math.max(yy[1], Math.max.apply(null, ys) + dy)];
      }
      else v = autoView(S, [-6, 6]);
      plot(svg, { v: v, curves: [{ f: S.f, col: "var(--border)" }].concat(monoCurves(S)), mark: iv ? absMarks(A) : extMarks(S), guides: iv ? [{ x: a }, { x: b }] : [] });
    }
    onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("La recta tangent a $f(x)=x^2$ en $x=1$ és…", "La recta tangente a $f(x)=x^2$ en $x=1$ es…", "The tangent line to $f(x)=x^2$ at $x=1$ is…"),
      o: [q3("$y=2x-1$"), q3("$y=2x+1$"), q3("$y=x$")], a: 0, e: q3("$f(1)=1$, $f'(1)=2$: $\\ y-1=2(x-1)\\Rightarrow y=2x-1$.") },
    { q: q3("Si $f'(a)=2$, el pendent de la recta normal en $x=a$ és…", "Si $f'(a)=2$, la pendiente de la recta normal en $x=a$ es…", "If $f'(a)=2$, the slope of the normal line at $x=a$ is…"),
      o: [q3("$2$"), q3("$-2$"), q3("$-\\frac12$")], a: 2, e: q3("$m_n=-\\frac{1}{f'(a)}=-\\frac12$ (perquè $m_t\\cdot m_n=-1$).", "$m_n=-\\frac{1}{f'(a)}=-\\frac12$ (porque $m_t\\cdot m_n=-1$).", "$m_n=-\\frac{1}{f'(a)}=-\\frac12$ (since $m_t\\cdot m_n=-1$).") },
    { q: q3("Si $f'(x)\\gt0$ en tot l'interval $(a,b)$, aleshores $f$ en $(a,b)$ és…", "Si $f'(x)\\gt0$ en todo el intervalo $(a,b)$, entonces $f$ en $(a,b)$ es…", "If $f'(x)\\gt0$ on the whole interval $(a,b)$, then on $(a,b)$ $f$ is…"),
      o: [q3("creixent", "creciente", "increasing"), q3("decreixent", "decreciente", "decreasing"), q3("constant", "constante", "constant")], a: 0,
      e: q3("El pendent de les tangents és positiu: la funció puja.", "La pendiente de las tangentes es positiva: la función sube.", "The tangents have positive slope: the function goes up.") },
    { q: q3("$f(x)=x^3-3x$ és decreixent en…", "$f(x)=x^3-3x$ es decreciente en…", "$f(x)=x^3-3x$ is decreasing on…"),
      o: [q3("$(-\\infty,-1)$"), q3("$(-1,1)$"), q3("$(1,+\\infty)$")], a: 1, e: q3("$f'(x)=3(x+1)(x-1)\\lt0$ entre $-1$ i $1$.", "$f'(x)=3(x+1)(x-1)\\lt0$ entre $-1$ y $1$.", "$f'(x)=3(x+1)(x-1)\\lt0$ between $-1$ and $1$.") },
    { q: q3("Si $f'(a)=0$ i $f''(a)\\lt0$, en $x=a$ hi ha…", "Si $f'(a)=0$ y $f''(a)\\lt0$, en $x=a$ hay…", "If $f'(a)=0$ and $f''(a)\\lt0$, at $x=a$ there is…"),
      o: [q3("un mínim relatiu", "un mínimo relativo", "a relative minimum"), q3("un màxim relatiu", "un máximo relativo", "a relative maximum"), q3("res: cal estudiar la monotonia", "nada: hay que estudiar la monotonía", "nothing: we must study monotonicity")], a: 1,
      e: q3("$f''(a)\\lt0$: la corba és còncava cap avall (∩), és un màxim.", "$f''(a)\\lt0$: la curva es cóncava hacia abajo (∩), es un máximo.", "$f''(a)\\lt0$: the curve bends downwards (∩), so it is a maximum.") },
    { q: q3("$f(x)=x^3$ compleix $f'(0)=0$. En $x=0$…", "$f(x)=x^3$ cumple $f'(0)=0$. En $x=0$…", "$f(x)=x^3$ has $f'(0)=0$. At $x=0$…"),
      o: [q3("té un màxim", "tiene un máximo", "it has a maximum"), q3("té un mínim", "tiene un mínimo", "it has a minimum"), q3("no té cap extrem", "no tiene ningún extremo", "it has no extremum")], a: 2,
      e: q3("$f'(x)=3x^2\\geq0$ no canvia de signe: és creixent abans i després de 0.", "$f'(x)=3x^2\\geq0$ no cambia de signo: es creciente antes y después de 0.", "$f'(x)=3x^2\\geq0$ does not change sign: it increases on both sides of 0.") },
    { q: q3("El mínim relatiu de $f(x)=x^2-6x+10$ és el punt…", "El mínimo relativo de $f(x)=x^2-6x+10$ es el punto…", "The relative minimum of $f(x)=x^2-6x+10$ is the point…"),
      o: [q3("$(3,1)$"), q3("$(3,0)$"), q3("$(-3,37)$")], a: 0, e: q3("$f'(x)=2x-6=0\\Rightarrow x=3$, $f''=2\\gt0$; $\\ f(3)=9-18+10=1$.") },
    { q: q3("Per trobar el màxim absolut d'una funció contínua en $[a,b]$ comparem els valors de $f$…", "Para encontrar el máximo absoluto de una función continua en $[a,b]$ comparamos los valores de $f$…", "To find the absolute maximum of a continuous function on $[a,b]$ we compare the values of $f$…"),
      o: [q3("només en els punts on $f'(x)=0$", "solo en los puntos donde $f'(x)=0$", "only at the points where $f'(x)=0$"), q3("en els punts crítics de dins i en els extrems $a$ i $b$", "en los puntos críticos de dentro y en los extremos $a$ y $b$", "at the critical points inside and at the endpoints $a$ and $b$"), q3("només en $a$ i $b$", "solo en $a$ y $b$", "only at $a$ and $b$")], a: 1,
      e: q3("El màxim absolut pot estar en un extrem de l'interval.", "El máximo absoluto puede estar en un extremo del intervalo.", "The absolute maximum may be at an endpoint.") },
    { q: q3("De tots els rectangles de perímetre 20, el d'àrea màxima té els costats…", "De todos los rectángulos de perímetro 20, el de área máxima tiene los lados…", "Of all rectangles with perimeter 20, the one with the largest area has sides…"),
      o: [q3("$4$ i $6$", "$4$ y $6$", "$4$ and $6$"), q3("$5$ i $5$", "$5$ y $5$", "$5$ and $5$"), q3("$2$ i $8$", "$2$ y $8$", "$2$ and $8$")], a: 1, e: q3("$y=10-x$, $A(x)=10x-x^2$, $A'=10-2x=0\\Rightarrow x=5$: és un quadrat.", "$y=10-x$, $A(x)=10x-x^2$, $A'=10-2x=0\\Rightarrow x=5$: es un cuadrado.", "$y=10-x$, $A(x)=10x-x^2$, $A'=10-2x=0\\Rightarrow x=5$: it is a square.") },
    { q: q3("En un problema d'optimització amb dues variables, el primer pas és…", "En un problema de optimización con dos variables, el primer paso es…", "In an optimisation problem with two variables, the first step is…"),
      o: [q3("derivar i igualar a zero", "derivar e igualar a cero", "differentiate and set equal to zero"), q3("buscar l'equació que relaciona les variables i aïllar-ne una", "buscar la ecuación que relaciona las variables y despejar una", "find the equation linking the variables and solve for one"), q3("fer la segona derivada", "hacer la segunda derivada", "compute the second derivative")], a: 1,
      e: q3("Primer necessitem una funció d'una sola variable: per això fem servir la condició que lliga les dues variables.", "Primero necesitamos una función de una sola variable: para eso usamos la condición que liga las dos variables.", "First we need a function of a single variable: that is what the constraint linking the two variables is for.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Aplicacions de la derivada · FentMates", es: "Aplicaciones de la derivada · FentMates", en: "Applications of the derivative · FentMates" };
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
      document.querySelectorAll(".widget .wt, .widget label, .widget .ttl, .widget .legend, #w-lab label, #w-lab .legend").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wFigs, function wTan() { wTN("w-tan", false); }, wPar, function wNorm() { wTN("w-norm", true); }, wMono, wExt, wAbs, wOpt, wBuild, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM6 = { parse: parse, D: D, texD: texD, compile: compile, studyF: studyF, roots: roots };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
