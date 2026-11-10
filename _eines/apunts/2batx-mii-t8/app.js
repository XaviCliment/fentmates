(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2batx-mii-u8-done";

  /* ---------- textos de la interfície (els de la unitat 7 i els propis) ---------- */
  var UI = /*@@UI7@@*/;
  var UI8 = {
    va: { dom: "Domini", posOn: "\\(f(x)\\gt0\\) (gràfica per damunt de l'eix OX) en", negOn: "\\(f(x)\\lt0\\) (gràfica per davall de l'eix OX) en", sgnF: "signe de \\(f\\)",
      fmx: "Comprovació numèrica", cen: "Simètrica respecte del punt", cenWhy: "on es tallen les asímptotes: \\(f(a+h)+f(a-h)=2b\\)",
      pUp: "la gràfica s'hi acosta per damunt", pDn: "la gràfica s'hi acosta per davall", pOsc: "la gràfica talla l'asímptota infinites vegades",
      side: "Costat", mL: "\\(m=\\lim\\frac{f(x)}{x}\\)", nL: "\\(n=\\lim\\,(f(x)-mx)\\)", concl: "Conclusió",
      brY: "branca parabòlica en la direcció de l'eix OY", brX: "branca parabòlica en la direcció de l'eix OX", brM: "branca parabòlica en la direcció de la recta", divi: "Divisió de polinomis:",
      quot: "El quocient és l'asímptota obliqua (el residu dividit pel denominador tendeix a 0).", quotH: "El quocient és constant: és l'asímptota horitzontal.", quotN: "El quocient té grau ≥ 2: no hi ha asímptota obliqua (branca parabòlica).",
      trN: ["f(x) + k", "f(x − k)", "k · f(x)", "f(k · x)", "−f(x)", "f(−x)", "|f(x)|", "f(|x|)", "1 / f(x)"],
      trD: ["Translació vertical de \\(k\\) unitats (cap amunt si \\(k\\gt0\\)).", "Translació horitzontal de \\(k\\) unitats (cap a la dreta si \\(k\\gt0\\)).", "Dilatació vertical de raó \\(k\\) (si \\(k\\lt0\\), també una simetria respecte de l'eix OX).",
        "Contracció horitzontal de raó \\(k\\): els punts \\((a,b)\\) passen a \\(\\left(\\frac ak,b\\right)\\).", "Simetria respecte de l'eix OX.", "Simetria respecte de l'eix OY.", "La part negativa es reflecteix cap amunt (simetria respecte de OX només on \\(f\\lt0\\)).",
        "Es dibuixa la part de \\(x\\geq0\\) i se'n fa la simètrica respecte de OY (la funció resultant és parella).", "On \\(f\\to0\\) hi ha asímptotes verticals; on \\(f\\to\\pm\\infty\\), \\(1/f\\to0\\); els màxims de \\(f\\) passen a ser mínims de \\(1/f\\) (i al revés)."],
      kLab: "k", base: "funció inicial", trans: "transformada",
      shF: "f", shD: "f′", shD2: "f″", fromD: "Com es llig: on \\(f'\\gt0\\) (gràfica de \\(f'\\) per damunt de OX) la funció \\(f\\) creix; on \\(f'\\) talla OX canviant de signe, \\(f\\) té un extrem; on \\(f'\\) té un extrem, \\(f\\) té un punt d'inflexió.",
      pDom: ["√(x² − 4x)", "ln((x+1)/(x−2))", "√(4 − x²)/ln x", "1/√(x² − 1)", "∛(x+1)/(x² − 4)", "tan 2x", "1/(2 cos x − 1)", "arcsin(2x − 1)", "√(eˣ − 2)"],
      pSign: ["x³ − 4x", "(x² − 1)/(x − 2)", "x²(x − 3)", "x ln x", "(2x+1)/(x² + x)", "sin 2x", "e^(−x)(x² − 1)"],
      pSym: ["x³/(x² − 4)", "x² e^(−x²)", "x sin x", "(3x² + 2)/(x − 2)", "ln|x|·x", "sin x + cos x", "1/(x² − 4x + 5)"],
      pAsy: ["(2x − 1)/√(x² − x − 2)", "eˣ/(x³ − x)", "e^(−x)/(x + 1)", "x² e^(1 − x)", "ln(x + 2)/(3x + 4)", "(x³ − 4x − 1)/(x² − 4)", "x²/(2 − e^(−x))", "(eˣ + x)/(eˣ − x)"],
      pObl: ["x²/(x − 2)", "(x³ + 4)/x²", "(2x³ − x² + x + 3)/(x² + 2)", "√(x² + 2x)", "x e^(1/x)", "(4x⁴ − x² + 1)/x", "x + ln(x² + 1)", "x − 2 arctan x"],
      pTr: ["x²", "eˣ", "ln x", "1/x", "sin x", "√x", "x³ − 3x"],
      pDer: ["x³ − 3x", "x e^(−x)", "x²/(x − 1)", "ln(x² + 1)", "x + 2 sin x", "x⁴ − 4x³"],
      pR1: ["(x³ − 4x − 1)/(x² − 4)", "(x² − x + 2)/x", "(4x⁴ − x² + 1)/x", "(2x² + 6)/(x − 1)", "(x² − 1)/(x² − 4x + 3)", "x⁵ − 5x³"],
      pR2: ["√(x² − 4x)", "x √(4 − x²)", "(2x − 1)/√(x² − x − 2)", "x^(2/3)(x − 5)", "√(x² + 2x)", "x/√(x² + 1)"],
      pR3: ["e^(−2x)(x² − 3x + 3/2)", "ln x/(x² − 3x + 2)", "(eˣ + x)/(eˣ − x)", "x²/(2 − e^(−x))", "1/x + ln x", "x² e^(1 − x)"],
      pR4: ["sin 2x − 2 sin x", "x − 2 sin x", "sin x / x", "cos x/(1 + sin x)", "2 cos x + cos 2x", "e^(sin x)"],
      pLab: ["x³ − 3x", "x²/(x − 2)", "x e^(−x²)", "ln(x)/x", "√(x² − 1)", "x + 2 cos x", "|x² − 4|", "x^(2/3)(x − 5)"] },
    es: { dom: "Dominio", posOn: "\\(f(x)\\gt0\\) (gráfica por encima del eje OX) en", negOn: "\\(f(x)\\lt0\\) (gráfica por debajo del eje OX) en", sgnF: "signo de \\(f\\)",
      fmx: "Comprobación numérica", cen: "Simétrica respecto del punto", cenWhy: "donde se cortan las asíntotas: \\(f(a+h)+f(a-h)=2b\\)",
      pUp: "la gráfica se acerca por encima", pDn: "la gráfica se acerca por debajo", pOsc: "la gráfica corta la asíntota infinitas veces",
      side: "Lado", mL: "\\(m=\\lim\\frac{f(x)}{x}\\)", nL: "\\(n=\\lim\\,(f(x)-mx)\\)", concl: "Conclusión",
      brY: "rama parabólica en la dirección del eje OY", brX: "rama parabólica en la dirección del eje OX", brM: "rama parabólica en la dirección de la recta", divi: "División de polinomios:",
      quot: "El cociente es la asíntota oblicua (el resto dividido entre el denominador tiende a 0).", quotH: "El cociente es constante: es la asíntota horizontal.", quotN: "El cociente tiene grado ≥ 2: no hay asíntota oblicua (rama parabólica).",
      trN: ["f(x) + k", "f(x − k)", "k · f(x)", "f(k · x)", "−f(x)", "f(−x)", "|f(x)|", "f(|x|)", "1 / f(x)"],
      trD: ["Traslación vertical de \\(k\\) unidades (hacia arriba si \\(k\\gt0\\)).", "Traslación horizontal de \\(k\\) unidades (hacia la derecha si \\(k\\gt0\\)).", "Dilatación vertical de razón \\(k\\) (si \\(k\\lt0\\), también una simetría respecto del eje OX).",
        "Contracción horizontal de razón \\(k\\): los puntos \\((a,b)\\) pasan a \\(\\left(\\frac ak,b\\right)\\).", "Simetría respecto del eje OX.", "Simetría respecto del eje OY.", "La parte negativa se refleja hacia arriba (simetría respecto de OX solo donde \\(f\\lt0\\)).",
        "Se dibuja la parte de \\(x\\geq0\\) y se hace su simétrica respecto de OY (la función resultante es par).", "Donde \\(f\\to0\\) hay asíntotas verticales; donde \\(f\\to\\pm\\infty\\), \\(1/f\\to0\\); los máximos de \\(f\\) pasan a ser mínimos de \\(1/f\\) (y al revés)."],
      kLab: "k", base: "función inicial", trans: "transformada",
      shF: "f", shD: "f′", shD2: "f″", fromD: "Cómo se lee: donde \\(f'\\gt0\\) (gráfica de \\(f'\\) por encima de OX) la función \\(f\\) crece; donde \\(f'\\) corta OX cambiando de signo, \\(f\\) tiene un extremo; donde \\(f'\\) tiene un extremo, \\(f\\) tiene un punto de inflexión.",
      pDom: ["√(x² − 4x)", "ln((x+1)/(x−2))", "√(4 − x²)/ln x", "1/√(x² − 1)", "∛(x+1)/(x² − 4)", "tg 2x", "1/(2 cos x − 1)", "arcsen(2x − 1)", "√(eˣ − 2)"],
      pSign: ["x³ − 4x", "(x² − 1)/(x − 2)", "x²(x − 3)", "x ln x", "(2x+1)/(x² + x)", "sen 2x", "e^(−x)(x² − 1)"],
      pSym: ["x³/(x² − 4)", "x² e^(−x²)", "x sen x", "(3x² + 2)/(x − 2)", "ln|x|·x", "sen x + cos x", "1/(x² − 4x + 5)"],
      pAsy: ["(2x − 1)/√(x² − x − 2)", "eˣ/(x³ − x)", "e^(−x)/(x + 1)", "x² e^(1 − x)", "ln(x + 2)/(3x + 4)", "(x³ − 4x − 1)/(x² − 4)", "x²/(2 − e^(−x))", "(eˣ + x)/(eˣ − x)"],
      pObl: ["x²/(x − 2)", "(x³ + 4)/x²", "(2x³ − x² + x + 3)/(x² + 2)", "√(x² + 2x)", "x e^(1/x)", "(4x⁴ − x² + 1)/x", "x + ln(x² + 1)", "x − 2 arctg x"],
      pTr: ["x²", "eˣ", "ln x", "1/x", "sen x", "√x", "x³ − 3x"],
      pDer: ["x³ − 3x", "x e^(−x)", "x²/(x − 1)", "ln(x² + 1)", "x + 2 sen x", "x⁴ − 4x³"],
      pR1: ["(x³ − 4x − 1)/(x² − 4)", "(x² − x + 2)/x", "(4x⁴ − x² + 1)/x", "(2x² + 6)/(x − 1)", "(x² − 1)/(x² − 4x + 3)", "x⁵ − 5x³"],
      pR2: ["√(x² − 4x)", "x √(4 − x²)", "(2x − 1)/√(x² − x − 2)", "x^(2/3)(x − 5)", "√(x² + 2x)", "x/√(x² + 1)"],
      pR3: ["e^(−2x)(x² − 3x + 3/2)", "ln x/(x² − 3x + 2)", "(eˣ + x)/(eˣ − x)", "x²/(2 − e^(−x))", "1/x + ln x", "x² e^(1 − x)"],
      pR4: ["sen 2x − 2 sen x", "x − 2 sen x", "sen x / x", "cos x/(1 + sen x)", "2 cos x + cos 2x", "e^(sen x)"],
      pLab: ["x³ − 3x", "x²/(x − 2)", "x e^(−x²)", "ln(x)/x", "√(x² − 1)", "x + 2 cos x", "|x² − 4|", "x^(2/3)(x − 5)"] },
    en: { dom: "Domain", posOn: "\\(f(x)\\gt0\\) (graph above the x-axis) on", negOn: "\\(f(x)\\lt0\\) (graph below the x-axis) on", sgnF: "sign of \\(f\\)",
      fmx: "Numerical check", cen: "Symmetric about the point", cenWhy: "where the asymptotes meet: \\(f(a+h)+f(a-h)=2b\\)",
      pUp: "the graph approaches it from above", pDn: "the graph approaches it from below", pOsc: "the graph crosses the asymptote infinitely many times",
      side: "Side", mL: "\\(m=\\lim\\frac{f(x)}{x}\\)", nL: "\\(n=\\lim\\,(f(x)-mx)\\)", concl: "Conclusion",
      brY: "parabolic branch in the direction of the y-axis", brX: "parabolic branch in the direction of the x-axis", brM: "parabolic branch in the direction of the line", divi: "Polynomial division:",
      quot: "The quotient is the oblique asymptote (the remainder over the denominator tends to 0).", quotH: "The quotient is constant: it is the horizontal asymptote.", quotN: "The quotient has degree ≥ 2: there is no oblique asymptote (parabolic branch).",
      trN: ["f(x) + k", "f(x − k)", "k · f(x)", "f(k · x)", "−f(x)", "f(−x)", "|f(x)|", "f(|x|)", "1 / f(x)"],
      trD: ["Vertical shift of \\(k\\) units (up if \\(k\\gt0\\)).", "Horizontal shift of \\(k\\) units (to the right if \\(k\\gt0\\)).", "Vertical stretch by a factor \\(k\\) (if \\(k\\lt0\\), also a reflection in the x-axis).",
        "Horizontal compression by a factor \\(k\\): the points \\((a,b)\\) move to \\(\\left(\\frac ak,b\\right)\\).", "Reflection in the x-axis.", "Reflection in the y-axis.", "The negative part is reflected upwards (in the x-axis, only where \\(f\\lt0\\)).",
        "Draw the part with \\(x\\geq0\\) and reflect it in the y-axis (the result is even).", "Where \\(f\\to0\\) there are vertical asymptotes; where \\(f\\to\\pm\\infty\\), \\(1/f\\to0\\); maxima of \\(f\\) become minima of \\(1/f\\) (and vice versa)."],
      kLab: "k", base: "original function", trans: "transformed",
      shF: "f", shD: "f′", shD2: "f″", fromD: "How to read it: where \\(f'\\gt0\\) (graph of \\(f'\\) above the x-axis) \\(f\\) increases; where \\(f'\\) crosses the x-axis changing sign, \\(f\\) has an extremum; where \\(f'\\) has an extremum, \\(f\\) has an inflection point.",
      pDom: ["√(x² − 4x)", "ln((x+1)/(x−2))", "√(4 − x²)/ln x", "1/√(x² − 1)", "∛(x+1)/(x² − 4)", "tan 2x", "1/(2 cos x − 1)", "arcsin(2x − 1)", "√(eˣ − 2)"],
      pSign: ["x³ − 4x", "(x² − 1)/(x − 2)", "x²(x − 3)", "x ln x", "(2x+1)/(x² + x)", "sin 2x", "e^(−x)(x² − 1)"],
      pSym: ["x³/(x² − 4)", "x² e^(−x²)", "x sin x", "(3x² + 2)/(x − 2)", "ln|x|·x", "sin x + cos x", "1/(x² − 4x + 5)"],
      pAsy: ["(2x − 1)/√(x² − x − 2)", "eˣ/(x³ − x)", "e^(−x)/(x + 1)", "x² e^(1 − x)", "ln(x + 2)/(3x + 4)", "(x³ − 4x − 1)/(x² − 4)", "x²/(2 − e^(−x))", "(eˣ + x)/(eˣ − x)"],
      pObl: ["x²/(x − 2)", "(x³ + 4)/x²", "(2x³ − x² + x + 3)/(x² + 2)", "√(x² + 2x)", "x e^(1/x)", "(4x⁴ − x² + 1)/x", "x + ln(x² + 1)", "x − 2 arctan x"],
      pTr: ["x²", "eˣ", "ln x", "1/x", "sin x", "√x", "x³ − 3x"],
      pDer: ["x³ − 3x", "x e^(−x)", "x²/(x − 1)", "ln(x² + 1)", "x + 2 sin x", "x⁴ − 4x³"],
      pR1: ["(x³ − 4x − 1)/(x² − 4)", "(x² − x + 2)/x", "(4x⁴ − x² + 1)/x", "(2x² + 6)/(x − 1)", "(x² − 1)/(x² − 4x + 3)", "x⁵ − 5x³"],
      pR2: ["√(x² − 4x)", "x √(4 − x²)", "(2x − 1)/√(x² − x − 2)", "x^(2/3)(x − 5)", "√(x² + 2x)", "x/√(x² + 1)"],
      pR3: ["e^(−2x)(x² − 3x + 3/2)", "ln x/(x² − 3x + 2)", "(eˣ + x)/(eˣ − x)", "x²/(2 − e^(−x))", "1/x + ln x", "x² e^(1 − x)"],
      pR4: ["sin 2x − 2 sin x", "x − 2 sin x", "sin x / x", "cos x/(1 + sin x)", "2 cos x + cos 2x", "e^(sin x)"],
      pLab: ["x³ − 3x", "x²/(x − 2)", "x e^(−x²)", "ln(x)/x", "√(x² − 1)", "x + 2 cos x", "|x² − 4|", "x^(2/3)(x − 5)"] }
  };
  LANGS.forEach(function (l) { Object.keys(UI8[l]).forEach(function (k) { UI[l][k] = UI8[l][k]; }); });
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { var v = (UI[lang] || UI.va)[k]; return v === undefined ? UI.va[k] : v; }
  function t3(va, es, en) { return lang === "es" ? es : lang === "en" ? en : va; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }
  // text amb fórmules \( \) (els textos de UI)
  function rt(s) { return String(s).replace(/\\\((.*?)\\\)/g, function (m, f) { return tex(f); }); }

  /*@@CORE@@*/
  /*@@DERIV@@*/
  /*@@STUDY@@*/
  /*@@STUDYFIG@@*/
  /*@@MONO@@*/
  /*@@WSTUDY@@*/

  /* ---------- eines comunes de la unitat 8 ---------- */
  function setupF(n) {
    var f = compile(n), C = condsOf(n), T = periodOf(f, n);
    var dens = C.den.map(compile).concat(C.tn.map(function (a) { return compile(Fn("cos", a)); }));
    var Dm = T ? domainOf(f, dens, 0, T) : domainOf(f, dens);
    return { n: n, f: f, T: T, Dm: Dm };
  }
  function viewDom(R) {
    if (R.T) { var v = [-0.25 * R.T, 1.75 * R.T]; return v.concat(autoY([R.f], v[0], v[1])); }
    var xs = [];
    R.Dm.iv.forEach(function (o) { if (!o.aInf && Math.abs(o.a) < XL) xs.push(o.a); if (!o.bInf && Math.abs(o.b) < XL) xs.push(o.b); });
    R.Dm.ex.forEach(function (p) { if (Math.abs(p) < XL) xs.push(p); });
    return viewOf(R.f, xs, [], [-6, 6]);
  }
  function domEnds(R, view) {
    var p = [];
    R.Dm.iv.forEach(function (o) {
      [[o.aInf, o.a, o.ai], [o.bInf, o.b, o.bi]].forEach(function (q) { if (!q[0] && !(R.T && (o.cut || 0)) && q[2]) p.push({ x: q[1], y: R.f(q[1]) }); });
    });
    return p.filter(function (q) { return q.x >= view[0] && q.x <= view[1]; });
  }

  /* ---------- 8.1 domini ---------- */
  function wDom() {
    var w = document.getElementById("w-dom"); if (!w) return;
    var PRE = [["sqrt(x^2-4x)"], ["ln((x+1)/(x-2))"], ["sqrt(4-x^2)/ln(x)"], ["1/sqrt(x^2-1)"], ["(x+1)^(1/3)/(x^2-4)"], ["tan(2x)"], ["1/(2cos(x)-1)"], ["arcsin(2x-1)"], ["sqrt(e^x-2)"]];
    var I = fnInput(w, PRE, "pDom", draw), svg = w.querySelector("svg"), info = w.querySelector(".info");
    function draw() {
      var n = readF(w, I.fi); if (!n) return;
      var R = setupF(n), view = viewDom(R), dt = domTex(R.Dm, R.T);
      info.innerHTML = "<p>" + tex("f(x)=" + texD(n)) + "</p><p><strong>" + u("dom") + ":</strong> " + (R.Dm.iv.length ? tex("\\mathrm{Dom}\\,f=" + dt) + (R.T && dt !== "\\mathbb R" && !/k/.test(dt) ? " (" + u("inPer") + ")" : "") + (R.T && /k/.test(dt) ? " " + rt(u("andK")) : "") : u("empty")) + "</p>" + domWhy(n, R.T) + (R.T ? "<p>" + u("per") + " " + tex("T=" + piTex(R.T)) + ".</p>" : "");
      plot(svg, { v: view, band: domBands(R.Dm), curves: [{ f: R.f }], pts: domEnds(R, view) });
    }
    onLang(draw);
  }

  /* ---------- 8.2 talls i signe ---------- */
  function sgnTable(Q, inf) {
    var r0 = ["<th>" + tex("x") + "</th>"], r1 = ["<th>" + tex("f(x)") + "</th>"], r2 = ["<th></th>"], last = Q.seg.length - 1;
    Q.seg.forEach(function (sg, j) {
      r0.push("<td>" + tex(intTex(sg.a, sg.b, inf && j === 0, inf && j === last)) + "</td>");
      if (sg.s === 0) { r1.push('<td class="nd">∄</td>'); r2.push('<td class="nd">' + u("noDom") + "</td>"); }
      else { r1.push('<td class="' + (sg.s > 0 ? "p" : "m") + '">' + (sg.s > 0 ? "+" : "−") + "</td>"); r2.push('<td class="nd">' + (sg.s > 0 ? "⬆ OX" : "⬇ OX") + "</td>"); }
      var e = Q.ev[j]; if (!e) return;
      r0.push('<td class="pt">' + tex(nn(e.x)) + "</td>"); r1.push('<td class="pt">' + (e.k === "z" ? "0" : "∄") + "</td>"); r2.push('<td class="pt"></td>');
    });
    return '<div class="tbl-wrap"><table class="data sm sgn">' + [r0, r1, r2].map(function (r) { return "<tr>" + r.join("") + "</tr>"; }).join("") + "</table></div>";
  }
  function wSign() {
    var w = document.getElementById("w-sign"); if (!w) return;
    var PRE = [["x^3-4x"], ["(x^2-1)/(x-2)"], ["x^2*(x-3)"], ["x*ln(x)"], ["(2x+1)/(x^2+x)"], ["sin(2x)"], ["e^(-x)*(x^2-1)"]];
    var I = fnInput(w, PRE, "pSign", draw), svg = w.querySelector("svg"), info = w.querySelector(".info"), tb = w.querySelector(".vtbl");
    function draw() {
      var n = readF(w, I.fi); if (!n) { tb.innerHTML = ""; return; }
      var R = setupF(n), inf = !R.T, Q = R.T ? crit(R.f, R.f, 0, R.T, { noJump: true }) : crit(R.f, R.f, -XL, XL, { noJump: true });
      if (!R.T && Q.ev.length > 24) { Q = crit(R.f, R.f, -8, 8, { noJump: true }); inf = false; }
      var C = cutsOf(R.f, R.Dm, R.T), K = runsOf(Q, inf), view = viewDom(R);
      info.innerHTML = "<p>" + tex("f(x)=" + texD(n)) + "</p>" + cutsHtml(C) + "<p><strong>" + rt(u("posOn")) + "</strong> " + (K.up.length ? tex(K.up.join("\\cup ")) : "—") + "<br><strong>" + rt(u("negOn")) + "</strong> " + (K.dn.length ? tex(K.dn.join("\\cup ")) : "—") + (R.T ? "<br>(" + u("inPer") + " " + tex("[0," + piTex(R.T) + "]") + ")" : "") + "</p>";
      tb.innerHTML = sgnTable(Q, inf);
      var curves = Q.seg.filter(function (g) { return g.s !== 0; }).map(function (g) { return { f: R.f, a: g.a, b: g.b, col: g.s > 0 ? "var(--ok)" : "var(--bad)" }; });
      if (R.T) curves = [-1, 0, 1].reduce(function (L, k) { return L.concat(curves.map(function (c) { return { f: R.f, a: c.a + k * R.T, b: c.b + k * R.T, col: c.col }; })); }, []);
      plot(svg, { v: view, band: domBands(R.Dm), curves: curves, pts: cutPts(C, view) });
    }
    onLang(draw);
  }

  /* ---------- 8.3 simetries i periodicitat ---------- */
  function centerOf(f, A) {
    if (A.T || A.av.length !== 1) return null;
    var a = A.av[0].x, L = A.side[-1], R = A.side[1], b;
    if (L.k === "o" && R.k === "o" && Math.abs(L.m - R.m) + Math.abs(L.n - R.n) < 1e-9) b = L.m * a + L.n;
    else if (L.k === "h" && R.k === "h" && Math.abs(L.y - R.y) < 1e-9) b = L.y;
    else return null;
    var ok = [0.37, 0.9, 1.7, 2.6, 4.1].every(function (h) { var p = f(a + h), q = f(a - h); return isFinite(p) && isFinite(q) && Math.abs(p + q - 2 * b) < 1e-7 * (1 + Math.abs(p) + Math.abs(q)); });
    return ok && (Math.abs(a) > 1e-9 || Math.abs(b) > 1e-9) ? { a: snap(a), b: snap(b) } : null;
  }
  function wSym() {
    var w = document.getElementById("w-sym"); if (!w) return;
    var PRE = [["x^3/(x^2-4)"], ["x^2*e^(-x^2)"], ["x*sin(x)"], ["(3x^2+2)/(x-2)"], ["x*ln(abs(x))"], ["sin(x)+cos(x)"], ["1/(x^2-4x+5)"]];
    var I = fnInput(w, PRE, "pSym", draw), svg = w.querySelector("svg"), info = w.querySelector(".info");
    function draw() {
      var n = readF(w, I.fi); if (!n) return;
      var R = setupF(n), f = R.f, s = symOf(f), A = asyOf(f, R.Dm, R.T), c = centerOf(f, A), view = viewDom(R);
      var h = "<p>" + tex("f(x)=" + texD(n)) + "</p><p><strong>" + symTxt(s) + "</strong>" + (s === "even" ? " — " + tex("f(-x)=f(x)") : s === "odd" ? " — " + tex("f(-x)=-f(x)") : "") + ".";
      if (c) h += "<br>" + u("cen") + " " + tex("(" + nn(c.a) + "," + nn(c.b) + ")") + ", " + rt(u("cenWhy"));
      h += "<br>" + (R.T ? u("per") + " " + tex("T=" + piTex(R.T)) + ": " + tex("f(x+" + piTex(R.T) + ")=f(x)") : u("notPer")) + "</p>";
      var rows = [1, 2, 3].map(function (x) { var a = f(x), b = f(-x); return "<tr><td>" + tex(String(x)) + "</td><td>" + (isFinite(a) ? tex(nnA(a)) : "∄") + "</td><td>" + (isFinite(b) ? tex(nnA(b)) : "∄") + "</td></tr>"; }).join("");
      h += "<p><strong>" + u("fmx") + "</strong></p><div class=\"tbl-wrap\"><table class=\"data sm\"><tr><th>" + tex("x") + "</th><th>" + tex("f(x)") + "</th><th>" + tex("f(-x)") + "</th></tr>" + rows + "</table></div>";
      info.innerHTML = h;
      var cfg = { v: view, band: domBands(R.Dm), curves: [{ f: function (x) { return f(-x); }, col: "var(--r3)" }, { f: f }] };
      if (c) { cfg.mark = [{ x: c.a, y: c.b, col: "var(--plus)" }]; Object.assign(cfg, asyPlot(A, view)); }
      plot(svg, cfg);
    }
    onLang(draw);
  }

  /* ---------- 8.4 asímptotes i posició relativa ---------- */
  function posOf(f, s, g) {
    var v = [30, 100, 300, 1000, 3000].map(function (X) { var y = f(s * X) - g(s * X); return isFinite(y) ? sgn(y) : 0; }).filter(function (k) { return k !== 0; });
    if (!v.length) return "";
    var a = v[v.length - 1], b = v[v.length - 2];
    if (b !== undefined && a !== b) return u("pOsc");
    return a > 0 ? u("pUp") : u("pDn");
  }
  function posHtml(f, A) {
    if (A.T) return "";
    var L = [];
    [-1, 1].forEach(function (s) {
      var o = A.side[s];
      if (o.k === "h") L.push((s < 0 ? u("toL") : u("toR")) + ", " + tex("y=" + nn(o.y)) + ": " + posOf(f, s, function () { return o.y; }));
      if (o.k === "o") L.push((s < 0 ? u("toL") : u("toR")) + ", " + tex(lineT(o.m, 0, o.n)) + ": " + posOf(f, s, function (x) { return o.m * x + o.n; }));
    });
    return L.length ? "<p>" + L.join("<br>") + "</p>" : "";
  }
  function wAsy() {
    var w = document.getElementById("w-asy"); if (!w) return;
    var PRE = [["(2x-1)/sqrt(x^2-x-2)"], ["e^x/(x^3-x)"], ["e^(-x)/(x+1)"], ["x^2*e^(1-x)"], ["ln(x+2)/(3x+4)"], ["(x^3-4x-1)/(x^2-4)"], ["x^2/(2-e^(-x))"], ["(e^x+x)/(e^x-x)"]];
    var I = fnInput(w, PRE, "pAsy", draw), svg = w.querySelector("svg"), info = w.querySelector(".info");
    function draw() {
      var n = readF(w, I.fi); if (!n) return;
      var R = setupF(n), A = asyOf(R.f, R.Dm, R.T), view = viewDom(R);
      var ys = []; [-1, 1].forEach(function (s) { if (A.side[s].k === "h") ys.push(A.side[s].y); });
      if (!R.T) view = viewOf(R.f, A.av.map(function (q) { return q.x; }).concat(R.Dm.iv.reduce(function (L, o) { if (!o.aInf) L.push(o.a); if (!o.bInf) L.push(o.b); return L; }, [])), ys, [-6, 6]);
      info.innerHTML = "<p>" + tex("f(x)=" + texD(n)) + "</p><p>" + tex("\\mathrm{Dom}\\,f=" + domTex(R.Dm, R.T)) + "</p>" + asyHtml(A, polyQ(n)) + posHtml(R.f, A);
      var cfg = { v: view, band: domBands(R.Dm), curves: [{ f: R.f }] };
      Object.assign(cfg, asyPlot(A, view));
      plot(svg, cfg);
    }
    onLang(draw);
  }

  /* ---------- 8.5 asímptotes obliqües i branques parabòliques ---------- */
  function pDivide(P, Q) {
    P = pTrim(P); Q = pTrim(Q);
    var q = [], r = P.slice(), dq = Q.length - 1;
    for (var i = 0; i <= Math.max(0, r.length - 1 - dq); i++) q.push(new Fr(0));
    while (pTrim(r).length - 1 >= dq && !(pTrim(r).length === 1 && r[0].zero())) {
      r = pTrim(r);
      var k = r.length - 1 - dq, c = r[r.length - 1].div(Q[dq]);
      q[k] = c;
      var sub = []; for (var j = 0; j < k; j++) sub.push(new Fr(0)); sub = sub.concat(Q.map(function (a) { return a.mul(c); }));
      r = pAdd(r, sub, -1);
      if (dq === 0) break;
    }
    return { q: pTrim(q), r: pTrim(r) };
  }
  function ratParts(n) {
    n = strip0(n);
    if (n.t !== "/") return null;
    try { var P = pTrim(polyOf(n.a)), Q = pTrim(polyOf(n.b)); return Q.length > 1 ? { P: P, Q: Q } : null; } catch (e) { return null; }
  }
  function sideObl(f, s) {
    var L = limSide(f, s * Infinity, s), M = null, N = null, k;
    if (L.k === "num") { L.v = snap(Math.abs(L.v) < 1e-5 ? 0 : L.v); k = { t: "h", y: L.v }; }
    else if (L.k !== "inf") k = { t: "none" };
    else {
      M = limSide(function (x) { return f(x) / x; }, s * Infinity, s);
      if (M.k === "inf") k = { t: "brY" };
      else if (M.k === "num" && Math.abs(M.v) < 1e-6) k = { t: "brX" };
      else if (M.k === "num") {
        var m = snap(M.v); if (Math.abs(m - Math.round(m)) < 1e-5) m = Math.round(m); M.v = m;
        N = limSide(function (x) { return f(x) - m * x; }, s * Infinity, s);
        if (N.k === "num") N.v = snap(Math.abs(N.v) < 1e-5 ? 0 : N.v);
        k = N.k === "num" ? { t: "o", m: m, n: N.v } : { t: "brM", m: m };
      } else k = { t: "none" };
    }
    return { L: L, M: M, N: N, k: k };
  }
  function oblTx(k) {
    if (k.t === "h") return u("ah") + " " + tex("y=" + nn(k.y));
    if (k.t === "o") return u("ao") + " " + tex(lineT(k.m, 0, k.n));
    if (k.t === "brY") return u("brY");
    if (k.t === "brX") return u("brX");
    if (k.t === "brM") return u("brM") + " " + tex("y=" + (Math.abs(k.m - 1) < 1e-12 ? "" : Math.abs(k.m + 1) < 1e-12 ? "-" : nn(k.m)) + "x");
    return u("noAsy");
  }
  function wObl() {
    var w = document.getElementById("w-obl"); if (!w) return;
    var PRE = [["x^2/(x-2)"], ["(x^3+4)/x^2"], ["(2x^3-x^2+x+3)/(x^2+2)"], ["sqrt(x^2+2x)"], ["x*e^(1/x)"], ["(4x^4-x^2+1)/x"], ["x+ln(x^2+1)"], ["x-2arctan(x)"]];
    var I = fnInput(w, PRE, "pObl", draw), svg = w.querySelector("svg"), info = w.querySelector(".info");
    function draw() {
      var n = readF(w, I.fi); if (!n) return;
      var R = setupF(n), f = R.f, h = "<p>" + tex("f(x)=" + texD(n)) + "</p>";
      if (R.T) { info.innerHTML = h + "<p>" + u("perAsy") + "</p>"; plot(svg, { v: viewDom(R), curves: [{ f: f }] }); return; }
      var rp = ratParts(n);
      if (rp) {
        var dv = pDivide(rp.P, rp.Q), dq = pDeg(dv.q);
        h += "<p><strong>" + u("divi") + "</strong> " + tex("\\dfrac{" + pTex(rp.P) + "}{" + pTex(rp.Q) + "}=" + pTex(dv.q) + (pTrim(dv.r).length === 1 && dv.r[0].zero() ? "" : "+\\dfrac{" + pTex(dv.r) + "}{" + pTex(rp.Q) + "}")) + "<br>" + (dq === 1 ? u("quot") : dq === 0 ? u("quotH") : u("quotN")) + "</p>";
      }
      var rows = [], oa = [], ha = [];
      [-1, 1].forEach(function (s) {
        var P = Dm0(R, s);
        if (!P) { rows.push("<tr><td>" + tex(s < 0 ? "x\\to-\\infty" : "x\\to+\\infty") + '</td><td colspan="3">' + u("notTo") + "</td></tr>"); return; }
        var O = sideObl(f, s);
        if (O.k.t === "o") oa.push({ m: O.k.m, n: O.k.n }); if (O.k.t === "h") ha.push(O.k.y);
        rows.push("<tr><td>" + tex(s < 0 ? "x\\to-\\infty" : "x\\to+\\infty") + "</td><td>" + tex("f\\to " + limTx(O.L)) + "</td><td>" + (O.M ? tex("m=" + limTx(O.M)) : "—") + (O.N ? "<br>" + tex("n=" + limTx(O.N)) : "") + "</td><td>" + oblTx(O.k) + "</td></tr>");
      });
      h += '<div class="tbl-wrap"><table class="data sm"><tr><th>' + u("side") + "</th><th>" + tex("\\lim f(x)") + "</th><th>" + rt(u("mL")) + "<br>" + rt(u("nL")) + "</th><th>" + u("concl") + "</th></tr>" + rows.join("") + "</table></div>";
      info.innerHTML = h;
      var A = asyOf(f, R.Dm, 0), view = viewOf(f, A.av.map(function (q) { return q.x; }), [], [-8, 8]);
      if (view[1] - view[0] < 14) { var c = (view[0] + view[1]) / 2; view[0] = c - 7; view[1] = c + 7; view = view.slice(0, 2).concat(autoY([f], view[0], view[1])); }
      plot(svg, { v: view, band: domBands(R.Dm), curves: [{ f: f }], va: A.av.map(function (q) { return q.x; }), oa: oa, ha: ha });
    }
    onLang(draw);
  }
  function limTx(r) { return r.k === "inf" && !r.s ? "\\infty" : r.k === "two" ? "\\nexists" : r.k === "num" ? nn(Math.abs(r.v) < 1e-8 ? 0 : r.v) : limTex(r); }
  function Dm0(R, s) { var P = R.Dm.iv[s < 0 ? 0 : R.Dm.iv.length - 1]; return P && (s < 0 ? P.aInf : P.bInf) ? P : null; }

  /* ---------- 8.11 transformacions de gràfiques ---------- */
  function wTr() {
    var w = document.getElementById("w-tr"); if (!w) return;
    var PRE = ["x^2", "e^x", "ln(x)", "1/x", "sin(x)", "sqrt(x)", "x^3-3x"];
    var fi = $(w, "f"), kr = $(w, "k"), kv = $(w, "kv"), box = $(w, "tr"), svg = w.querySelector("svg"), info = w.querySelector(".info"), mode = 0, bts = [];
    presetBtns($(w, "presets"), PRE.length, "pTr", function (i) { fi.value = PRE[i]; draw(); });
    for (var i = 0; i < 9; i++) (function (i) { var b = document.createElement("button"); b.type = "button"; b.className = "btn"; b.addEventListener("click", function () { mode = i; draw(); }); box.appendChild(b); bts.push(b); })(i);
    fi.addEventListener("input", draw); kr.addEventListener("input", draw);
    function draw() {
      bts.forEach(function (b, i) { b.textContent = u("trN")[i]; b.classList.toggle("primary", i === mode); });
      var n = readF(w, fi); if (!n) return;
      var f = compile(n), k = +kr.value; kv.textContent = numTxt(k);
      var G = [function (x) { return f(x) + k; }, function (x) { return f(x - k); }, function (x) { return k * f(x); }, function (x) { return f(k * x); }, function (x) { return -f(x); }, function (x) { return f(-x); },
        function (x) { return Math.abs(f(x)); }, function (x) { return f(Math.abs(x)); }, function (x) { var y = f(x); return Math.abs(y) < 1e-12 ? NaN : 1 / y; }][mode];
      var ks = numTex(k), ft = texD(n), gT = ["f(x)" + (k < 0 ? "-" + numTex(-k) : "+" + ks), "f\\left(x" + (k < 0 ? "+" + numTex(-k) : "-" + ks) + "\\right)", ks + "\\cdot f(x)", "f\\left(" + ks + "x\\right)", "-f(x)", "f(-x)", "\\left|f(x)\\right|", "f\\left(|x|\\right)", "\\dfrac{1}{f(x)}"][mode];
      var useK = mode < 4;
      kr.parentNode.style.display = useK ? "" : "none";
      info.innerHTML = "<p>" + tex("f(x)=" + ft) + "</p><p>" + tex("g(x)=" + gT) + "</p><p>" + rt(u("trD")[mode]) + "</p><div class=\"legend\"><span><i style=\"background:var(--muted)\"></i>" + u("base") + " \\(f\\)</span><span><i style=\"background:var(--accent)\"></i>" + u("trans") + " \\(g\\)</span></div>";
      info.querySelectorAll(".legend span").forEach(function (s) { s.innerHTML = rt(s.innerHTML); });
      var v = [-6, 6]; v = v.concat(autoY([f, G], v[0], v[1]));
      plot(svg, { v: v, curves: [{ f: f, col: "var(--muted)" }, { f: G, col: "var(--accent)" }] });
    }
    onLang(draw);
  }

  /* ---------- 8.12 f, f′ i f″ ---------- */
  function wDer() {
    var w = document.getElementById("w-der"); if (!w) return;
    var PRE = [["x^3-3x"], ["x*e^(-x)"], ["x^2/(x-1)"], ["ln(x^2+1)"], ["x+2sin(x)"], ["x^4-4x^3"]];
    var I = fnInput(w, PRE, "pDer", draw), svg = w.querySelector("svg"), info = w.querySelector(".info"), cb = [$(w, "c0"), $(w, "c1"), $(w, "c2")];
    cb.forEach(function (c) { c.addEventListener("change", draw); });
    function draw() {
      var n = readF(w, I.fi); if (!n) return;
      var S; try { S = studyWin(n); } catch (e) { info.textContent = u("noDiff"); return; }
      var h = "<p>" + tex("f(x)=" + texD(n)) + "</p>";
      if (S.dn) h += "<p>" + tex("f'(x)=" + texD(S.dn)) + "</p>";
      if (S.d2n) h += "<p>" + tex("f''(x)=" + texD(S.d2n)) + "</p>";
      info.innerHTML = h + monoHtml(S, S.inf) + curvHtml(S, S.inf) + '<p class="hint">' + rt(u("fromD")) + "</p>";
      var v = autoView(S, [-5, 5]), curves = [], fs = [];
      if (cb[2].checked) { curves.push({ f: S.d2, col: "var(--r3)" }); fs.push(S.d2); }
      if (cb[1].checked) { curves.push({ f: S.df, col: "var(--accent-2)" }); fs.push(S.df); }
      if (cb[0].checked) { curves.push({ f: S.f, col: "var(--accent)" }); fs.push(S.f); }
      if (fs.length) { var yy = autoY(fs, v[0], v[1]); v = [v[0], v[1], yy[0], yy[1]]; }
      var mk = cb[0].checked ? extMarks(S).concat(inflPts(S)) : [];
      if (S.P) mk = periodic(mk, S.P, v);
      plot(svg, { v: v, curves: curves, mark: mk });
    }
    onLang(draw);
  }

  function wStudies() {
    wStudy("w-r1", ["(x^3-4x-1)/(x^2-4)", "(x^2-x+2)/x", "(4x^4-x^2+1)/x", "(2x^2+6)/(x-1)", "(x^2-1)/(x^2-4x+3)", "x^5-5x^3"], "pR1");
    wStudy("w-r2", ["sqrt(x^2-4x)", "x*sqrt(4-x^2)", "(2x-1)/sqrt(x^2-x-2)", "x^(2/3)*(x-5)", "sqrt(x^2+2x)", "x/sqrt(x^2+1)"], "pR2");
    wStudy("w-r3", ["e^(-2x)*(x^2-3x+3/2)", "ln(x)/(x^2-3x+2)", "(e^x+x)/(e^x-x)", "x^2/(2-e^(-x))", "1/x+ln(x)", "x^2*e^(1-x)"], "pR3");
    wStudy("w-r4", ["sin(2x)-2sin(x)", "x-2sin(x)", "sin(x)/x", "cos(x)/(1+sin(x))", "2cos(x)+cos(2x)", "e^(sin(x))"], "pR4");
    wStudy("w-lab", ["x^3-3x", "x^2/(x-2)", "x*e^(-x^2)", "ln(x)/x", "sqrt(x^2-1)", "x+2cos(x)", "abs(x^2-4)", "x^(2/3)*(x-5)"], "pLab");
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("El domini de $f(x)=\\sqrt{\\dfrac{x+1}{x-2}}$ és…", "El dominio de $f(x)=\\sqrt{\\dfrac{x+1}{x-2}}$ es…", "The domain of $f(x)=\\sqrt{\\dfrac{x+1}{x-2}}$ is…"),
      o: [q3("$(-\\infty,-1]\\cup(2,+\\infty)$"), q3("$[-1,2)$"), q3("$\\mathbb R-\\{2\\}$")], a: 0, e: q3("Cal $\\frac{x+1}{x-2}\\geq0$ i $x\\neq2$: signes $+$, $-$, $+$; el $-1$ hi entra (val 0) però el 2 no.", "Hace falta $\\frac{x+1}{x-2}\\geq0$ y $x\\neq2$: signos $+$, $-$, $+$; el $-1$ entra (vale 0) pero el 2 no.", "We need $\\frac{x+1}{x-2}\\geq0$ and $x\\neq2$: signs $+$, $-$, $+$; $-1$ is included (value 0) but 2 is not.") },
    { q: q3("El domini de $f(x)=\\sqrt[3]{x-5}$ és…", "El dominio de $f(x)=\\sqrt[3]{x-5}$ es…", "The domain of $f(x)=\\sqrt[3]{x-5}$ is…"),
      o: [q3("$[5,+\\infty)$"), q3("$\\mathbb R$"), q3("$(5,+\\infty)$")], a: 1, e: q3("Les arrels d'índex senar existeixen per a qualsevol radicand.", "Las raíces de índice impar existen para cualquier radicando.", "Odd roots exist for any radicand.") },
    { q: q3("Si $f(-x)=-f(x)$ per a tot $x$ del domini, la gràfica és simètrica respecte…", "Si $f(-x)=-f(x)$ para todo $x$ del dominio, la gráfica es simétrica respecto…", "If $f(-x)=-f(x)$ for every $x$ in the domain, the graph is symmetric about…"),
      o: [q3("de l'eix OY", "del eje OY", "the y-axis"), q3("de l'origen", "del origen", "the origin"), q3("de l'eix OX", "del eje OX", "the x-axis")], a: 1, e: q3("És una funció senar: $(x,y)$ i $(-x,-y)$ són de la gràfica.", "Es una función impar: $(x,y)$ y $(-x,-y)$ son de la gráfica.", "It is an odd function: $(x,y)$ and $(-x,-y)$ are on the graph.") },
    { q: q3("Quantes asímptotes horitzontals pot tindre, com a molt, una funció?", "¿Cuántas asíntotas horizontales puede tener, como mucho, una función?", "At most how many horizontal asymptotes can a function have?"),
      o: [q3("Una"), q3("Dues (una en $-\\infty$ i una en $+\\infty$)", "Dos (una en $-\\infty$ y una en $+\\infty$)", "Two (one at $-\\infty$ and one at $+\\infty$)"), q3("Infinites", "Infinitas", "Infinitely many")], a: 1, e: q3("Per exemple, $f(x)=\\frac{2x-1}{\\sqrt{x^2-x-2}}$ té $y=-2$ en $-\\infty$ i $y=2$ en $+\\infty$.", "Por ejemplo, $f(x)=\\frac{2x-1}{\\sqrt{x^2-x-2}}$ tiene $y=-2$ en $-\\infty$ e $y=2$ en $+\\infty$.", "For example, $f(x)=\\frac{2x-1}{\\sqrt{x^2-x-2}}$ has $y=-2$ at $-\\infty$ and $y=2$ at $+\\infty$.") },
    { q: q3("Una funció pot tallar la seua asímptota horitzontal?", "¿Una función puede cortar a su asíntota horizontal?", "Can a function cross its horizontal asymptote?"),
      o: [q3("No, mai", "No, nunca", "No, never"), q3("Sí, fins i tot infinites vegades", "Sí, incluso infinitas veces", "Yes, even infinitely many times"), q3("Només si és parella", "Solo si es par", "Only if it is even")], a: 1, e: q3("$f(x)=\\frac{\\sin x}{x}$ té l'asímptota $y=0$ i la talla en tots els $x=k\\pi$. El que no pot tallar mai és una asímptota vertical.", "$f(x)=\\frac{\\sin x}{x}$ tiene la asíntota $y=0$ y la corta en todos los $x=k\\pi$. Lo que no puede cortar nunca es una asíntota vertical.", "$f(x)=\\frac{\\sin x}{x}$ has the asymptote $y=0$ and crosses it at every $x=k\\pi$. What it can never cross is a vertical asymptote.") },
    { q: q3("L'asímptota obliqua de $f(x)=\\sqrt{x^2+2x}$ quan $x\\to+\\infty$ és…", "La asíntota oblicua de $f(x)=\\sqrt{x^2+2x}$ cuando $x\\to+\\infty$ es…", "The oblique asymptote of $f(x)=\\sqrt{x^2+2x}$ as $x\\to+\\infty$ is…"),
      o: [q3("$y=x$"), q3("$y=x+1$"), q3("$y=x+2$")], a: 1, e: q3("$m=1$, $n=\\lim(\\sqrt{x^2+2x}-x)=\\lim\\frac{2x}{\\sqrt{x^2+2x}+x}=1$. Quan $x\\to-\\infty$ és $y=-x-1$.", "$m=1$, $n=\\lim(\\sqrt{x^2+2x}-x)=\\lim\\frac{2x}{\\sqrt{x^2+2x}+x}=1$. Cuando $x\\to-\\infty$ es $y=-x-1$.", "$m=1$, $n=\\lim(\\sqrt{x^2+2x}-x)=\\lim\\frac{2x}{\\sqrt{x^2+2x}+x}=1$. As $x\\to-\\infty$ it is $y=-x-1$.") },
    { q: q3("Si $\\lim_{x\\to+\\infty}f(x)=+\\infty$ i $\\lim_{x\\to+\\infty}\\frac{f(x)}{x}=0$ (com $\\ln x$ o $\\sqrt x$), hi ha…", "Si $\\lim_{x\\to+\\infty}f(x)=+\\infty$ y $\\lim_{x\\to+\\infty}\\frac{f(x)}{x}=0$ (como $\\ln x$ o $\\sqrt x$), hay…", "If $\\lim_{x\\to+\\infty}f(x)=+\\infty$ and $\\lim_{x\\to+\\infty}\\frac{f(x)}{x}=0$ (like $\\ln x$ or $\\sqrt x$), there is…"),
      o: [q3("una asímptota obliqua $y=0$", "una asíntota oblicua $y=0$", "an oblique asymptote $y=0$"), q3("una branca parabòlica en la direcció de OX", "una rama parabólica en la dirección de OX", "a parabolic branch in the direction of the x-axis"), q3("una asímptota horitzontal", "una asíntota horizontal", "a horizontal asymptote")], a: 1, e: q3("Creix cap a l'infinit, però cada vegada més «tombada».", "Crece hacia el infinito, pero cada vez más «tumbada».", "It grows without bound, but flatter and flatter.") },
    { q: q3("$f(x)=\\dfrac{x^2-1}{x^2-4x+3}$ en $x=1$ té…", "$f(x)=\\dfrac{x^2-1}{x^2-4x+3}$ en $x=1$ tiene…", "$f(x)=\\dfrac{x^2-1}{x^2-4x+3}$ at $x=1$ has…"),
      o: [q3("una asímptota vertical", "una asíntota vertical", "a vertical asymptote"), q3("una discontinuïtat evitable (un forat)", "una discontinuidad evitable (un agujero)", "a removable discontinuity (a hole)"), q3("un punt de tall amb OX", "un punto de corte con OX", "an x-intercept")], a: 1, e: q3("$\\frac{(x-1)(x+1)}{(x-1)(x-3)}=\\frac{x+1}{x-3}\\to-1$: el punt $(1,-1)$ no és de la gràfica. L'asímptota vertical és $x=3$.", "$\\frac{(x-1)(x+1)}{(x-1)(x-3)}=\\frac{x+1}{x-3}\\to-1$: el punto $(1,-1)$ no es de la gráfica. La asíntota vertical es $x=3$.", "$\\frac{(x-1)(x+1)}{(x-1)(x-3)}=\\frac{x+1}{x-3}\\to-1$: the point $(1,-1)$ is not on the graph. The vertical asymptote is $x=3$.") },
    { q: q3("En $x=0$, $f(x)=x^{2/3}(x-5)$ té…", "En $x=0$, $f(x)=x^{2/3}(x-5)$ tiene…", "At $x=0$, $f(x)=x^{2/3}(x-5)$ has…"),
      o: [q3("un màxim amb tangent horitzontal", "un máximo con tangente horizontal", "a maximum with a horizontal tangent"), q3("un màxim en un punt de retrocés (no derivable)", "un máximo en un punto de retroceso (no derivable)", "a maximum at a cusp (not differentiable)"), q3("un punt d'inflexió", "un punto de inflexión", "an inflection point")], a: 1, e: q3("$f'(x)=\\frac{5(x-2)}{3\\sqrt[3]x}$: no existeix en 0 i hi passa de $+$ a $-$.", "$f'(x)=\\frac{5(x-2)}{3\\sqrt[3]x}$: no existe en 0 y pasa de $+$ a $-$.", "$f'(x)=\\frac{5(x-2)}{3\\sqrt[3]x}$: it does not exist at 0 and changes from $+$ to $-$.") },
    { q: q3("El període de $f(x)=\\sin(2x)-2\\sin x$ és…", "El periodo de $f(x)=\\sin(2x)-2\\sin x$ es…", "The period of $f(x)=\\sin(2x)-2\\sin x$ is…"),
      o: [q3("$\\pi$"), q3("$2\\pi$"), q3("$4\\pi$")], a: 1, e: q3("$\\sin 2x$ té període $\\pi$ i $\\sin x$, $2\\pi$: el període comú és el mínim comú múltiple, $2\\pi$.", "$\\sin 2x$ tiene periodo $\\pi$ y $\\sin x$, $2\\pi$: el periodo común es el mínimo común múltiplo, $2\\pi$.", "$\\sin 2x$ has period $\\pi$ and $\\sin x$ has $2\\pi$: the common period is their lcm, $2\\pi$.") },
    { q: q3("La gràfica de $y=|f(x)|$ s'obté de la de $f$…", "La gráfica de $y=|f(x)|$ se obtiene de la de $f$…", "The graph of $y=|f(x)|$ is obtained from that of $f$…"),
      o: [q3("reflectint la part de $x\\lt0$", "reflejando la parte de $x\\lt0$", "by reflecting the part with $x\\lt0$"), q3("reflectint cap amunt la part que queda per davall de OX", "reflejando hacia arriba la parte que queda por debajo de OX", "by reflecting upwards the part below the x-axis"), q3("traslladant-la cap amunt", "trasladándola hacia arriba", "by shifting it up")], a: 1, e: q3("On $f\\lt0$, $|f|=-f$; on $f\\geq0$ no canvia. En els talls amb OX solen aparéixer punts angulosos.", "Donde $f\\lt0$, $|f|=-f$; donde $f\\geq0$ no cambia. En los cortes con OX suelen aparecer puntos angulosos.", "Where $f\\lt0$, $|f|=-f$; where $f\\geq0$ nothing changes. Corners usually appear at the x-intercepts.") },
    { q: q3("Si la gràfica de $f'$ talla l'eix OX en $x=2$ passant de positiva a negativa, $f$ té en $x=2$…", "Si la gráfica de $f'$ corta el eje OX en $x=2$ pasando de positiva a negativa, $f$ tiene en $x=2$…", "If the graph of $f'$ crosses the x-axis at $x=2$ going from positive to negative, $f$ has at $x=2$…"),
      o: [q3("un mínim relatiu", "un mínimo relativo", "a relative minimum"), q3("un màxim relatiu", "un máximo relativo", "a relative maximum"), q3("un punt d'inflexió", "un punto de inflexión", "an inflection point")], a: 1, e: q3("$f$ passa de créixer a decréixer.", "$f$ pasa de crecer a decrecer.", "$f$ goes from increasing to decreasing.") },
    { q: q3("Si la gràfica de $f'$ té un mínim en $x=1$, la funció $f$ té en $x=1$…", "Si la gráfica de $f'$ tiene un mínimo en $x=1$, la función $f$ tiene en $x=1$…", "If the graph of $f'$ has a minimum at $x=1$, the function $f$ has at $x=1$…"),
      o: [q3("un mínim", "un mínimo", "a minimum"), q3("un punt d'inflexió", "un punto de inflexión", "an inflection point"), q3("una asímptota", "una asíntota", "an asymptote")], a: 1, e: q3("En un extrem de $f'$ s'anul·la $f''$ i canvia de signe: canvia la curvatura de $f$.", "En un extremo de $f'$ se anula $f''$ y cambia de signo: cambia la curvatura de $f$.", "At an extremum of $f'$, $f''$ vanishes and changes sign: the concavity of $f$ changes.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Representació gràfica de funcions · FentMates", es: "Representación gráfica de funciones · FentMates", en: "Graphing functions · FentMates" };
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
      document.querySelectorAll(".widget .wt, .widget label, .widget .ttl, .widget .legend, .lab label, .lab .legend").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wStudyFigs, wDom, wSign, wSym, wAsy, wObl, wMono, wCurv, wTr, wDer, wStudies, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM8 = { parse: parse, compile: compile, fullStudy: fullStudy, setupF: setupF, asyOf: asyOf, sideObl: sideObl, pDivide: pDivide, nn: nn };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
