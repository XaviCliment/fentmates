(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1eso-u3-done", NSEC = 8;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", write: "Escriu un nombre enter (per exemple, −7).",
      ctx: {
        temp: { p: "{n} °C sobre zero", n: "{n} °C baix zero", z: "0 °C: ni fa calor ni fred… de gel!", zero: "0 °C", up: "més calor", down: "més fred" },
        floor: { p: "planta {n}", n: "soterrani {n}", z: "planta baixa", zero: "planta baixa", up: "plantes", down: "soterranis" },
        alt: { p: "{n} m d'altitud (sobre el nivell de la mar)", n: "{n} m de profunditat (sota el nivell de la mar)", z: "al nivell de la mar", zero: "nivell de la mar", up: "altitud", down: "profunditat" },
        money: { p: "tinc {n} €", n: "dec {n} €", z: "ni tinc ni dec res", zero: "0 €", up: "diners", down: "deutes" },
        year: { p: "any {n} d. C.", n: "any {n} a. C.", z: "", zero: "naixement de Crist", up: "després de Crist", down: "abans de Crist" } },
      cxBad: "Escriu un enter entre −9999 i 9999.", cxRef: "El 0 és la <b>referència</b>: {z}. Els positius estan per damunt i els negatius, per davall.", cxYear0: "Compte: no hi ha cap «any 0»! De l'any 1 a. C. es passa directament a l'any 1 d. C.",
      cxSay: "Ho diem així:", cxNum: "Ho escrivim així:",
      lnBad: "Escriu entre 1 i 15 enters separats per comes (entre −1000 i 1000).", lnAsc: "De menor a major:", lnDesc: "De major a menor:", lnRight: "Com més a la dreta en la recta, més gran és el nombre.",
      lnCmp: "{a} està més a la {s} que {b}, per tant", lnL: "esquerra", lnR: "dreta", lnEq: "Són el mateix nombre.", lnRep: "(Els nombres repetits només es dibuixen una vegada.)",
      abBad: "Escriu un enter entre −1000 i 1000.", abDist: "{a} està a <b>{d}</b> unitats del 0: el seu valor absolut és {d}.", abOp: "L'oposat de {a} és <b>{o}</b>: està a la mateixa distància del 0, però a l'altre costat.",
      abZero: "El 0 és l'únic nombre que és igual al seu oposat i que té valor absolut 0.", abPair: "Entre {a} i {o} hi ha {t} unitats (el doble de {d}).",
      adBad: "Escriu enters entre −200 i 200.", adSub: "Restar és sumar l'oposat:", adSame: "Tenen el <b>mateix signe</b>: sumem {x} + {y} = {s} i posem el signe comú ({g}).",
      adDiff: "Tenen <b>signes diferents</b>: restem {x} − {y} = {s} i posem el signe del que té major valor absolut ({g}).", adZero: "Són oposats: la suma és 0.", adZ: "Sumar 0 no canvia res.",
      adMove: "Partim de {a} i ens movem {m} unitats cap a la {s}.", sgP: "+", sgN: "−",
      prBad: "Escriu termes com 3, −5, (+7), −(−4)… separats per + o −.", prRule: "Traiem els parèntesis amb la regla dels signes:", prGroup: "Agrupem positius i negatius:", prOnly: "No hi ha parèntesis: ja podem operar.",
      sgBad: "Escriu enters entre −1000 i 1000.", sgDiv0: "No es pot dividir entre 0.", sgInex: "{a} : {b} no és exacta: el resultat no és un nombre enter.", sgZero: "Si un dels factors és 0, el producte és 0 (no té signe).",
      sgSame: "Signes <b>iguals</b> → resultat <b>positiu</b>.", sgDiff: "Signes <b>diferents</b> → resultat <b>negatiu</b>.", sgAbs: "Primer operem els valors absoluts: {x} {o} {y} = {r}.",
      hParse: "No entenc l'expressió. Usa xifres, + − · : i parèntesis ( ) [ ].", hDiv: "{a} : {b} no és exacta: el resultat no seria enter.", hDiv0: "No es pot dividir entre 0.", hBig: "El resultat és massa gran.",
      kinds: { opp: "Signe davant del parèntesi", mul: "Multiplicació", div: "Divisió", add: "Suma", sub: "Resta" }, inPar: "dins del parèntesi", result: "Resultat:", already: "Ja és un nombre: no hi ha res a calcular.",
      elBad: "Escriu un enter de partida i una llista de canvis com +5, −3, +2 (com a molt 20).", elStart: "Partida", elEnd: "Final", elVar: "Variació total: {v}.", elMax: "El valor més alt ha sigut {M} i el més baix, {m}.",
      elSay: "Al final:", elUnit: { floor: "", temp: " °C", money: " €" },
      dMin: "Quin és el més <b>xicotet</b> d'aquests nombres?", dMax: "Quin és el més <b>gran</b> d'aquests nombres?", dOpp: "Dos nombres oposats estan a {d} unitats l'un de l'altre. Quin és el negatiu?", dCalc: "Calcula:", dMiss: "Quin nombre falta?" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", write: "Escribe un número entero (por ejemplo, −7).",
      ctx: {
        temp: { p: "{n} °C sobre cero", n: "{n} °C bajo cero", z: "0 °C: ¡ni calor ni frío… de hielo!", zero: "0 °C", up: "más calor", down: "más frío" },
        floor: { p: "planta {n}", n: "sótano {n}", z: "planta baja", zero: "planta baja", up: "plantas", down: "sótanos" },
        alt: { p: "{n} m de altitud (sobre el nivel del mar)", n: "{n} m de profundidad (bajo el nivel del mar)", z: "al nivel del mar", zero: "nivel del mar", up: "altitud", down: "profundidad" },
        money: { p: "tengo {n} €", n: "debo {n} €", z: "ni tengo ni debo nada", zero: "0 €", up: "dinero", down: "deudas" },
        year: { p: "año {n} d. C.", n: "año {n} a. C.", z: "", zero: "nacimiento de Cristo", up: "después de Cristo", down: "antes de Cristo" } },
      cxBad: "Escribe un entero entre −9999 y 9999.", cxRef: "El 0 es la <b>referencia</b>: {z}. Los positivos están por encima y los negativos, por debajo.", cxYear0: "¡Cuidado: no existe el «año 0»! Del año 1 a. C. se pasa directamente al año 1 d. C.",
      cxSay: "Lo decimos así:", cxNum: "Lo escribimos así:",
      lnBad: "Escribe entre 1 y 15 enteros separados por comas (entre −1000 y 1000).", lnAsc: "De menor a mayor:", lnDesc: "De mayor a menor:", lnRight: "Cuanto más a la derecha en la recta, mayor es el número.",
      lnCmp: "{a} está más a la {s} que {b}, por tanto", lnL: "izquierda", lnR: "derecha", lnEq: "Son el mismo número.", lnRep: "(Los números repetidos solo se dibujan una vez.)",
      abBad: "Escribe un entero entre −1000 y 1000.", abDist: "{a} está a <b>{d}</b> unidades del 0: su valor absoluto es {d}.", abOp: "El opuesto de {a} es <b>{o}</b>: está a la misma distancia del 0, pero al otro lado.",
      abZero: "El 0 es el único número que es igual a su opuesto y que tiene valor absoluto 0.", abPair: "Entre {a} y {o} hay {t} unidades (el doble de {d}).",
      adBad: "Escribe enteros entre −200 y 200.", adSub: "Restar es sumar el opuesto:", adSame: "Tienen el <b>mismo signo</b>: sumamos {x} + {y} = {s} y ponemos el signo común ({g}).",
      adDiff: "Tienen <b>signos distintos</b>: restamos {x} − {y} = {s} y ponemos el signo del que tiene mayor valor absoluto ({g}).", adZero: "Son opuestos: la suma es 0.", adZ: "Sumar 0 no cambia nada.",
      adMove: "Partimos de {a} y nos movemos {m} unidades hacia la {s}.", sgP: "+", sgN: "−",
      prBad: "Escribe términos como 3, −5, (+7), −(−4)… separados por + o −.", prRule: "Quitamos los paréntesis con la regla de los signos:", prGroup: "Agrupamos positivos y negativos:", prOnly: "No hay paréntesis: ya podemos operar.",
      sgBad: "Escribe enteros entre −1000 y 1000.", sgDiv0: "No se puede dividir entre 0.", sgInex: "{a} : {b} no es exacta: el resultado no es un número entero.", sgZero: "Si uno de los factores es 0, el producto es 0 (no tiene signo).",
      sgSame: "Signos <b>iguales</b> → resultado <b>positivo</b>.", sgDiff: "Signos <b>distintos</b> → resultado <b>negativo</b>.", sgAbs: "Primero operamos los valores absolutos: {x} {o} {y} = {r}.",
      hParse: "No entiendo la expresión. Usa cifras, + − · : y paréntesis ( ) [ ].", hDiv: "{a} : {b} no es exacta: el resultado no sería entero.", hDiv0: "No se puede dividir entre 0.", hBig: "El resultado es demasiado grande.",
      kinds: { opp: "Signo delante del paréntesis", mul: "Multiplicación", div: "División", add: "Suma", sub: "Resta" }, inPar: "dentro del paréntesis", result: "Resultado:", already: "Ya es un número: no hay nada que calcular.",
      elBad: "Escribe un entero de partida y una lista de cambios como +5, −3, +2 (como mucho 20).", elStart: "Salida", elEnd: "Final", elVar: "Variación total: {v}.", elMax: "El valor más alto ha sido {M} y el más bajo, {m}.",
      elSay: "Al final:", elUnit: { floor: "", temp: " °C", money: " €" },
      dMin: "¿Cuál es el <b>menor</b> de estos números?", dMax: "¿Cuál es el <b>mayor</b> de estos números?", dOpp: "Dos números opuestos están a {d} unidades el uno del otro. ¿Cuál es el negativo?", dCalc: "Calcula:", dMiss: "¿Qué número falta?" },
    en: { next: "Next step", all: "Show all", reset: "Hide steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Toggle light and dark mode", write: "Type an integer (for example, −7).",
      ctx: {
        temp: { p: "{n} °C above zero", n: "{n} °C below zero", z: "0 °C: freezing point!", zero: "0 °C", up: "warmer", down: "colder" },
        floor: { p: "floor {n}", n: "basement {n}", z: "ground floor", zero: "ground floor", up: "floors", down: "basements" },
        alt: { p: "{n} m above sea level", n: "{n} m below sea level", z: "at sea level", zero: "sea level", up: "height", down: "depth" },
        money: { p: "I have €{n}", n: "I owe €{n}", z: "I have nothing and owe nothing", zero: "€0", up: "money", down: "debts" },
        year: { p: "year {n} AD", n: "year {n} BC", z: "", zero: "birth of Christ", up: "AD", down: "BC" } },
      cxBad: "Type an integer from −9999 to 9999.", cxRef: "0 is the <b>reference point</b>: {z}. Positives are above it and negatives below it.", cxYear0: "Careful: there is no “year 0”! Year 1 BC is followed directly by year 1 AD.",
      cxSay: "We say:", cxNum: "We write:",
      lnBad: "Type from 1 to 15 integers separated by commas (between −1000 and 1000).", lnAsc: "From smallest to largest:", lnDesc: "From largest to smallest:", lnRight: "The further right on the number line, the bigger the number.",
      lnCmp: "{a} is further {s} than {b}, so", lnL: "left", lnR: "right", lnEq: "They are the same number.", lnRep: "(Repeated numbers are drawn only once.)",
      abBad: "Type an integer from −1000 to 1000.", abDist: "{a} is <b>{d}</b> units away from 0: its absolute value is {d}.", abOp: "The opposite of {a} is <b>{o}</b>: it's the same distance from 0, but on the other side.",
      abZero: "0 is the only number that equals its opposite and has absolute value 0.", abPair: "There are {t} units between {a} and {o} (twice {d}).",
      adBad: "Type integers from −200 to 200.", adSub: "Subtracting is adding the opposite:", adSame: "They have the <b>same sign</b>: add {x} + {y} = {s} and keep the common sign ({g}).",
      adDiff: "They have <b>different signs</b>: subtract {x} − {y} = {s} and take the sign of the one with the larger absolute value ({g}).", adZero: "They are opposites: the sum is 0.", adZ: "Adding 0 changes nothing.",
      adMove: "Start at {a} and move {m} units to the {s}.", sgP: "+", sgN: "−",
      prBad: "Type terms like 3, −5, (+7), −(−4)… joined by + or −.", prRule: "Remove the brackets using the sign rule:", prGroup: "Group positives and negatives:", prOnly: "There are no brackets: we can work it out directly.",
      sgBad: "Type integers from −1000 to 1000.", sgDiv0: "You can't divide by 0.", sgInex: "{a} : {b} is not exact: the result is not an integer.", sgZero: "If one factor is 0, the product is 0 (which has no sign).",
      sgSame: "<b>Same</b> signs → <b>positive</b> result.", sgDiff: "<b>Different</b> signs → <b>negative</b> result.", sgAbs: "First work with the absolute values: {x} {o} {y} = {r}.",
      hParse: "I can't read that expression. Use digits, + − · : and brackets ( ) [ ].", hDiv: "{a} : {b} is not exact: the result wouldn't be an integer.", hDiv0: "You can't divide by 0.", hBig: "The result is too big.",
      kinds: { opp: "Sign before brackets", mul: "Multiplication", div: "Division", add: "Addition", sub: "Subtraction" }, inPar: "inside the brackets", result: "Result:", already: "It's already a number: nothing to work out.",
      elBad: "Type a starting integer and a list of changes like +5, −3, +2 (at most 20).", elStart: "Start", elEnd: "End", elVar: "Total change: {v}.", elMax: "The highest value was {M} and the lowest, {m}.",
      elSay: "At the end:", elUnit: { floor: "", temp: " °C", money: " €" },
      dMin: "Which is the <b>smallest</b> of these numbers?", dMax: "Which is the <b>largest</b> of these numbers?", dOpp: "Two opposite numbers are {d} units apart. Which is the negative one?", dCalc: "Work out:", dMiss: "Which number is missing?" }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var MACROS = { "\\dc": "\\htmlClass{dc}{{,}}", "\\tri": "\\htmlClass{lva}{\\text{#1}}\\htmlClass{les}{\\text{#2}}\\htmlClass{len}{\\text{#3}}" };
  var KOPT = { throwOnError: false, strict: "ignore", macros: MACROS, trust: function (c) { return c.command === "\\htmlClass"; } };
  function tex(s, display) {
    try { return window.katex.renderToString(s, { throwOnError: false, strict: "ignore", displayMode: !!display, macros: MACROS, trust: KOPT.trust }); } catch (e) { return s; }
  }
  function rtex(s) { return s.replace(/\$([^$]+)\$/g, function (_, m) { return tex(m); }); }
  function segBind(w, cb) {
    var bs = w.querySelectorAll(".seg button");
    bs.forEach(function (b) { b.addEventListener("click", function () { bs.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); cb(b.dataset.k); }); });
  }
  function segVal(w) { var b = w.querySelector('.seg button[aria-pressed="true"]'); return b ? b.dataset.k : null; }
  function segSet(w, k) { w.querySelectorAll(".seg button").forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.k === k)); }); }

  /* ---------- nombres i format ---------- */
  function norm(s) { return String(s).replace(/[−–—]/g, "-").replace(/[×xX*]/g, "·").replace(/[\/÷]/g, ":").replace(/[\s  ]/g, ""); }
  function pint(s) {
    s = norm(s);
    if (!/^[+-]?\d{1,9}$/.test(s)) return NaN;
    return parseInt(s, 10);
  }
  function fcore(x, th) {
    if (!isFinite(x)) return "—";
    var s = String(Math.round(Math.abs(x)));
    if (s.length > 4) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, th);
    return s;
  }
  function fh(x) { return (x < 0 ? "−" : "") + fcore(x, " "); }          // HTML: −7
  function fs(x) { return (x > 0 ? "+" : "") + fh(x); }                    // HTML amb signe: +7, −7
  function ft(x) { return (x < 0 ? "-" : "") + fcore(x, "\\,"); }          // TeX: -7
  function fp(x) { return x < 0 ? "(" + ft(x) + ")" : ft(x); }             // TeX amb parèntesi si és negatiu
  function fps(x) { return "(" + (x > 0 ? "+" : "") + ft(x) + ")"; }       // TeX: (+7), (-7)
  function warn(k) { return '<span class="warn">' + u(k) + "</span>"; }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function rnz(a, b) { var x; do { x = rint(a, b); } while (!x); return x; }
  function hint(s) { return '<div class="hint">' + s + "</div>"; }
  function sgnW(x) { return x > 0 ? "+" : "−"; }
  function readInt(w, k, max) { var el = w.querySelector('[data-k="' + k + '"]'), x = pint(el.value); return isNaN(x) || Math.abs(x) > max ? null : x; }
  function readList(s, maxN, maxV) {
    var p = norm(s).split(/[,;]+/).filter(function (x) { return x !== ""; });
    if (!p.length || p.length > maxN) return null;
    var v = p.map(pint);
    return v.every(function (x) { return !isNaN(x) && Math.abs(x) <= maxV; }) ? v : null;
  }
  function quickFill(w, keys, render) {
    w.querySelectorAll(".quick button[data-b]").forEach(function (b) {
      b.addEventListener("click", function () {
        var p = b.dataset.b.split("|");
        keys.forEach(function (k, i) { var el = w.querySelector('[data-k="' + k + '"]'); if (el && p[i] != null) el.value = p[i]; });
        render();
      });
    });
  }

  /* ---------- recta numèrica en SVG ---------- */
  var STEPS = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 5000];
  function axis(lo, hi, Y, opt) {
    opt = opt || {};
    var st = 1;
    for (var i = 0; i < STEPS.length; i++) { st = STEPS[i]; if ((hi - lo) / st <= (opt.max || 20)) break; }
    lo = Math.floor(lo / st) * st; hi = Math.ceil(hi / st) * st;
    var X0 = 34, X1 = 586, x = function (v) { return X0 + (v - lo) / (hi - lo) * (X1 - X0); };
    var s = '<line class="sv-ax" x1="' + (X0 - 22) + '" y1="' + Y + '" x2="' + (X1 + 22) + '" y2="' + Y + '"/>' +
      '<path class="sv-ax" fill="none" d="M' + (X1 + 14) + " " + (Y - 6) + " L" + (X1 + 24) + " " + Y + " L" + (X1 + 14) + " " + (Y + 6) + '"/>' +
      '<path class="sv-ax" fill="none" d="M' + (X0 - 14) + " " + (Y - 6) + " L" + (X0 - 24) + " " + Y + " L" + (X0 - 14) + " " + (Y + 6) + '"/>';
    for (var v = lo; v <= hi; v += st) {
      s += '<line class="sv-ax" x1="' + x(v) + '" y1="' + (Y - 6) + '" x2="' + x(v) + '" y2="' + (Y + 6) + '"/>';
      if (!opt.noLab) s += '<text class="' + (v ? "sv-t" : "sv-tb") + '" x="' + x(v) + '" y="' + (Y + 24) + '" text-anchor="middle">' + fh(v) + "</text>";
    }
    return { x: x, s: s, lo: lo, hi: hi, st: st };
  }
  function head(x, y, dir, cls) { return '<path class="' + cls + '" d="M' + x + " " + y + " l" + (-9 * dir) + " -5 l0 10 z" + '"/>'; }
  function svgWrap(h, s, lab) { return '<svg viewBox="0 0 620 ' + h + '" role="img" aria-label="' + lab + '">' + s + "</svg>"; }

  /* ---------- giny: enters en context ---------- */
  function wCtx() {
    var w = document.getElementById("w-ctx"); if (!w) return;
    var V = w.querySelector('[data-k="v"]'), ch = w.querySelector(".chart"), info = w.querySelector(".info");
    function render() {
      var c = segVal(w) || "temp", v = pint(V.value), C = u("ctx")[c];
      if (isNaN(v) || Math.abs(v) > 9999) { ch.innerHTML = ""; info.innerHTML = warn("cxBad"); return; }
      var R = 5; while (R < Math.abs(v) * 1.15) R = R < 10 ? 10 : R * (String(R).charAt(0) === "2" ? 2.5 : 2);
      var H = 280, T = 20, B = 260, y = function (t) { return T + (R - t) / (2 * R) * (B - T); }, s = "";
      s += '<rect class="cx-up" x="150" y="' + T + '" width="120" height="' + (y(0) - T) + '" rx="6"/><rect class="cx-dn" x="150" y="' + y(0) + '" width="120" height="' + (B - y(0)) + '" rx="6"/>';
      for (var k = -5; k <= 5; k++) { var t = R * k / 5; s += '<line class="sv-ax" x1="142" y1="' + y(t) + '" x2="150" y2="' + y(t) + '"/><text class="' + (k ? "sv-t" : "sv-tb") + '" x="136" y="' + (y(t) + 4) + '" text-anchor="end">' + fs(t).replace("+0", "0") + "</text>"; }
      s += '<line class="cx-zero" x1="144" y1="' + y(0) + '" x2="300" y2="' + y(0) + '"/><text class="sv-tb" x="306" y="' + (y(0) + 5) + '">' + C.zero + "</text>";
      s += '<text class="sv-t" x="306" y="' + (T + 14) + '">▲ ' + C.up + '</text><text class="sv-t" x="306" y="' + (B - 4) + '">▼ ' + C.down + "</text>";
      if (v) s += '<rect class="' + (v > 0 ? "cx-bp" : "cx-bn") + '" x="190" y="' + Math.min(y(0), y(v)) + '" width="40" height="' + Math.abs(y(v) - y(0)) + '"/>';
      s += '<line class="cx-mk" x1="176" y1="' + y(v) + '" x2="244" y2="' + y(v) + '"/><text class="cx-lab" x="252" y="' + (y(v) + (v > 0 ? -6 : 18)) + '">' + fs(v).replace("+0", "0") + "</text>";
      ch.innerHTML = '<svg viewBox="0 0 620 ' + H + '" role="img" aria-label="escala">' + s + "</svg>";
      var say = v > 0 ? fill(C.p, { n: fh(v) }) : v < 0 ? fill(C.n, { n: fh(-v) }) : C.z;
      var h = c === "year" && !v ? warn("cxYear0") : "<div>" + u("cxSay") + " <b>" + say + "</b></div><div>" + u("cxNum") + " " + tex((v > 0 ? "+" : "") + ft(v), true) + "</div>";
      info.innerHTML = h + hint(fill(u("cxRef"), { z: C.zero }));
    }
    V.addEventListener("input", render);
    segBind(w, render);
    w.querySelectorAll(".quick button[data-b]").forEach(function (b) { b.addEventListener("click", function () { var p = b.dataset.b.split("|"); segSet(w, p[0]); V.value = p[1]; render(); }); });
    onLang(render);
  }

  /* ---------- giny: recta numèrica i ordre ---------- */
  function lineSVG(vals, hl) {
    var mn = Math.min.apply(null, vals.concat([0])), mx = Math.max.apply(null, vals.concat([0]));
    var A = axis(mn - 1, mx + 1, 52), s = A.s, last = [-99, -99], uniq = vals.filter(function (x, i) { return vals.indexOf(x) === i; }).sort(function (a, b) { return a - b; });
    uniq.forEach(function (v) {
      var X = A.x(v), row = X - last[0] < 30 ? (X - last[1] < 30 ? 0 : 1) : 0;
      if (row === 0) last[0] = X; else last[1] = X;
      var ly = row ? 92 : 22;
      s += '<line class="ln-st" x1="' + X + '" y1="' + (row ? 58 : 46) + '" x2="' + X + '" y2="' + (row ? 80 : 28) + '"/>';
      s += '<circle class="' + (hl && hl.indexOf(v) >= 0 ? "ln-hl" : v < 0 ? "ln-n" : v > 0 ? "ln-p" : "ln-z") + '" cx="' + X + '" cy="52" r="6.5"/><text class="ln-lab" x="' + X + '" y="' + (ly + 4) + '" text-anchor="middle">' + fh(v) + "</text>";
    });
    return svgWrap(104, s.replace(/<text class="sv-t[b]?" [^>]*>[^<]*<\/text>/g, function (m) { return m.replace(/y="(\d+)"/, 'y="$1" opacity=".55"'); }), "recta");
  }
  function wLine() {
    var w = document.getElementById("w-line"); if (!w) return;
    var I = w.querySelector('[data-k="v"]'), ch = w.querySelector(".chart"), info = w.querySelector(".info");
    function render() {
      var v = readList(I.value, 15, 1000), up = segVal(w) !== "desc";
      if (!v) { ch.innerHTML = ""; info.innerHTML = warn("lnBad"); return; }
      ch.innerHTML = lineSVG(v);
      var o = v.slice().sort(function (a, b) { return up ? a - b : b - a; });
      var h = "<div><b>" + u(up ? "lnAsc" : "lnDesc") + "</b></div>" + tex(o.map(function (x, i) { return (i ? (x === o[i - 1] ? "=" : up ? "<" : ">") : "") + ft(x); }).join(""), true);
      if (v.length === 2) {
        var a = v[0], b = v[1];
        h += a === b ? hint(u("lnEq")) : "<div>" + fill(u("lnCmp"), { a: fh(a), b: fh(b), s: u(a > b ? "lnR" : "lnL") }) + " " + tex(ft(a) + (a > b ? ">" : "<") + ft(b)) + "</div>";
      }
      if (o.some(function (x, i) { return i && x === o[i - 1]; })) h += hint(u("lnRep"));
      info.innerHTML = h + hint(u("lnRight"));
    }
    I.addEventListener("input", render);
    segBind(w, render);
    quickFill(w, ["v"], render);
    onLang(render);
  }

  /* ---------- giny: valor absolut i oposat ---------- */
  function wAbs() {
    var w = document.getElementById("w-abs"); if (!w) return;
    var A = w.querySelector('[data-k="a"]'), ch = w.querySelector(".chart"), info = w.querySelector(".info");
    function render() {
      var a = pint(A.value);
      if (isNaN(a) || Math.abs(a) > 1000) { ch.innerHTML = ""; info.innerHTML = warn("abBad"); return; }
      var d = Math.abs(a), R = Math.max(5, d + 1), X = axis(-R, R, 70), s = X.s, x0 = X.x(0);
      if (d) {
        [a, -a].forEach(function (v, i) {
          var xv = X.x(v), cls = i ? "ab-op" : "ab-a";
          s += '<path class="' + cls + '" fill="none" d="M' + x0 + " 64 Q " + (x0 + xv) / 2 + " 4 " + xv + ' 64"/>';
          s += '<text class="ab-t ' + cls + 't" x="' + (x0 + xv) / 2 + '" y="28" text-anchor="middle">' + fh(d) + "</text>";
          s += '<circle class="' + (i ? "ln-op" : "ln-hl") + '" cx="' + xv + '" cy="70" r="7"/>';
        });
      } else s += '<circle class="ln-hl" cx="' + x0 + '" cy="70" r="7"/>';
      ch.innerHTML = svgWrap(104, s, "valor absolut");
      var o = { a: fh(a), d: fh(d), o: fh(-a), t: fh(2 * d) };
      info.innerHTML = tex("|" + ft(a) + "|=" + ft(d) + "\\qquad \\text{op}" + "(" + ft(a) + ")=" + ft(-a), true) +
        "<div>" + fill(u("abDist"), o) + "</div>" + (d ? "<div>" + fill(u("abOp"), o) + "</div>" + hint(fill(u("abPair"), o)) : hint(u("abZero")));
    }
    A.addEventListener("input", render);
    quickFill(w, ["a"], render);
    onLang(render);
  }

  /* ---------- giny: suma i resta en la recta ---------- */
  function sumRule(x, y) {
    var r = x + y, o = { x: fh(Math.abs(x)), y: fh(Math.abs(y)), s: "", g: "" };
    if (!y || !x) return u("adZ");
    if (!r) return u("adZero");
    if ((x > 0) === (y > 0)) { o.s = fh(Math.abs(r)); o.g = sgnW(x); return fill(u("adSame"), o); }
    var big = Math.abs(x) >= Math.abs(y) ? x : y; o.x = fh(Math.max(Math.abs(x), Math.abs(y))); o.y = fh(Math.min(Math.abs(x), Math.abs(y))); o.s = fh(Math.abs(r)); o.g = sgnW(big);
    return fill(u("adDiff"), o);
  }
  function wAdd() {
    var w = document.getElementById("w-add"); if (!w) return;
    var ch = w.querySelector(".chart"), info = w.querySelector(".info");
    function render() {
      var a = readInt(w, "a", 200), b = readInt(w, "b", 200), op = segVal(w) || "+";
      if (a == null || b == null) { ch.innerHTML = ""; info.innerHTML = warn("adBad"); return; }
      var c = op === "+" ? b : -b, r = a + c, X = axis(Math.min(0, a, r) - 1, Math.max(0, a, r) + 1, 70), s = X.s, xa = X.x(a), xr = X.x(r);
      if (c) {
        var dir = c > 0 ? 1 : -1;
        s += '<path class="ad-arr" fill="none" d="M' + xa + " 62 Q " + (xa + xr) / 2 + " 6 " + (xr - 4 * dir) + ' 58"/>' + head(xr, 60, dir, "ad-hd");
        s += '<text class="ad-t" x="' + (xa + xr) / 2 + '" y="24" text-anchor="middle">' + fs(c) + "</text>";
      }
      s += '<circle class="ln-z" cx="' + xa + '" cy="70" r="6.5"/><circle class="ln-hl" cx="' + xr + '" cy="70" r="7"/>';
      ch.innerHTML = svgWrap(104, s, "suma");
      var h = tex(ft(a) + op + fp(b) + "=" + (op === "-" ? ft(a) + "+" + fp(c) + "=" : "") + "\\boxed{" + ft(r) + "}", true);
      if (op === "-") h += hint(u("adSub") + " " + tex("-" + fp(b) + "=+" + fp(c)));
      h += "<div>" + sumRule(a, c) + "</div>";
      if (c) h += hint(fill(u("adMove"), { a: fh(a), m: fh(Math.abs(c)), s: u(c > 0 ? "lnR" : "lnL") }));
      info.innerHTML = h;
    }
    w.querySelectorAll(".tin").forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, render);
    w.querySelectorAll(".quick button[data-b]").forEach(function (bt) { bt.addEventListener("click", function () { var p = bt.dataset.b.split("|"); w.querySelector('[data-k="a"]').value = p[0]; segSet(w, p[1]); w.querySelector('[data-k="b"]').value = p[2]; render(); }); });
    onLang(render);
  }

  /* ---------- parèntesis en sumes i restes ---------- */
  function parTerms(s) {
    s = norm(s);
    var t = [], m;
    while (s.length) {
      if ((m = s.match(/^([+-]?)\(([+-]?)(\d{1,6})\)/))) t.push({ o: m[1] || "+", i: m[2] || "+", n: +m[3], p: true, ou: !!m[1], iu: !!m[2] });
      else if ((m = s.match(/^([+-]?)(\d{1,6})/))) t.push({ o: m[1] || "+", i: "+", n: +m[2], p: false, ou: !!m[1] });
      else return null;
      if (t.length > 1 && !t[t.length - 1].ou) return null;
      s = s.slice(m[0].length);
    }
    if (!t.length || t.length > 12) return null;
    t.forEach(function (x) { x.s = x.o === x.i ? 1 : -1; x.v = x.s * x.n; });
    return t;
  }
  function termTex(x, first) {
    var o = first && x.o === "+" && !x.ou ? "" : x.o;
    return o + (x.p ? "(" + (x.iu ? x.i : "") + ft(x.n) + ")" : ft(x.n));
  }
  function flatTex(t) { return t.map(function (x, i) { return (x.v < 0 ? "-" : i ? "+" : "") + ft(x.n); }).join(""); }
  function parSteps(t) {
    var P = 0, N = 0, out = [];
    t.forEach(function (x) { if (x.v > 0) P += x.v; else N -= x.v; });
    var has = t.some(function (x) { return x.p; });
    out.push(t.map(function (x, i) { return termTex(x, !i); }).join("") + (has ? "=" + flatTex(t) : ""));
    if (t.length > 2 && P && N) out.push("=" + ft(P) + "-" + ft(N));
    out.push("=\\boxed{" + ft(P - N) + "}");
    return { tex: out.join(""), P: P, N: N, has: has };
  }
  function wPar() {
    var w = document.getElementById("w-par"); if (!w) return;
    var inp = w.querySelector(".tin"), out = w.querySelector(".pchips"), info = w.querySelector(".info");
    function render() {
      var t = parTerms(inp.value);
      if (!t) { out.innerHTML = ""; info.innerHTML = warn("prBad"); return; }
      var r = parSteps(t);
      out.innerHTML = r.has ? '<span class="ql">' + u("prRule") + "</span>" + t.filter(function (x) { return x.p; }).map(function (x) {
        return '<span class="pch ' + (x.s > 0 ? "p" : "n") + '">' + tex(x.o + "(" + x.i + ft(x.n) + ")\\ \\to\\ " + (x.s > 0 ? "+" : "-") + ft(x.n)) + '<small>' + x.o + " ( " + x.i + " → " + (x.s > 0 ? "+" : "−") + "</small></span>";
      }).join("") : '<span class="ql">' + u("prOnly") + "</span>";
      var g = r.P && r.N && t.length > 2 ? hint(u("prGroup") + " " + tex("(" + t.filter(function (x) { return x.v > 0; }).map(function (x) { return ft(x.n); }).join("+") + ")-(" + t.filter(function (x) { return x.v < 0; }).map(function (x) { return ft(x.n); }).join("+") + ")=" + ft(r.P) + "-" + ft(r.N))) : "";
      info.innerHTML = tex(r.tex, true) + g;
    }
    inp.addEventListener("input", render);
    w.querySelectorAll(".quick button[data-e]").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.e; render(); }); });
    onLang(render);
  }

  /* ---------- giny: regla dels signes ---------- */
  function wSign() {
    var w = document.getElementById("w-sign"); if (!w) return;
    var tb = w.querySelector(".sgtab"), info = w.querySelector(".info");
    function render() {
      var a = readInt(w, "a", 1000), b = readInt(w, "b", 1000), op = segVal(w) || "·";
      tb.querySelectorAll("td").forEach(function (td) { td.classList.remove("on"); });
      tb.querySelector(".sop").textContent = op;
      if (a == null || b == null) { info.innerHTML = warn("sgBad"); return; }
      var sym = op === "·" ? "\\cdot " : ":";
      if (op === ":" && !b) { info.innerHTML = warn("sgDiv0"); return; }
      if (op === ":" && a % b) { info.innerHTML = tex(fp(a) + ":" + fp(b), true) + '<span class="warn">' + fill(u("sgInex"), { a: fh(a), b: fh(b) }) + "</span>"; return; }
      var r = op === "·" ? a * b : a / b;
      if (a && b) tb.querySelector('td[data-c="' + (a > 0 ? "p" : "n") + (b > 0 ? "p" : "n") + '"]').classList.add("on");
      var h = tex(fps(a) + sym + fps(b) + "=" + (a && b ? (r > 0 ? "+" : "-") + "(" + ft(Math.abs(a)) + sym + ft(Math.abs(b)) + ")=" : "") + "\\boxed{" + ft(r) + "}", true);
      if (!a || !b) h += hint(op === "·" || !a ? u("sgZero") : "");
      else h += "<div>" + fill(u("sgAbs"), { x: fh(Math.abs(a)), y: fh(Math.abs(b)), o: op, r: fh(Math.abs(r)) }) + "</div><div>" + u((a > 0) === (b > 0) ? "sgSame" : "sgDiff") + "</div>";
      info.innerHTML = h;
    }
    w.querySelectorAll(".tin").forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, render);
    w.querySelectorAll(".quick button[data-b]").forEach(function (bt) { bt.addEventListener("click", function () { var p = bt.dataset.b.split("|"); w.querySelector('[data-k="a"]').value = p[0]; segSet(w, p[1]); w.querySelector('[data-k="b"]').value = p[2]; render(); }); });
    onLang(render);
  }

  /* ---------- operacions combinades pas a pas (amb enters) ---------- */
  function tokenize(s) {
    s = norm(s).replace(/\{/g, "[").replace(/\}/g, "]");
    var t = [], i = 0;
    while (i < s.length) {
      var c = s.charAt(i);
      if (/\d/.test(c)) { var m = s.slice(i).match(/^\d+/)[0]; if (m.length > 9) return null; t.push({ k: "n", v: parseInt(m, 10) }); i += m.length; continue; }
      if ("+-·:()[]".indexOf(c) >= 0) { t.push({ k: c }); i++; continue; }
      return null;
    }
    return t;
  }
  function parseExpr(s) {
    var t = tokenize(s), i = 0;
    if (!t || !t.length) return null;
    function peek() { return t[i] && t[i].k; }
    function expr() { var a = term(); while (peek() === "+" || peek() === "-") { var op = t[i++].k; a = { t: "b", op: op, l: a, r: term() }; } return a; }
    function term() {
      var a = un();
      for (;;) {
        var p = peek();
        if (p === "·" || p === ":") { i++; a = { t: "b", op: p, l: a, r: un() }; }
        else if (p === "(" || p === "[") a = { t: "b", op: "·", l: a, r: prim() };
        else return a;
      }
    }
    /* un signe davant d'un nombre forma un enter; davant d'un parèntesi és «l'oposat de» */
    function un() {
      var p = peek();
      if (p === "+" || p === "-") {
        i++;
        if (peek() === "n") { var v = t[i++].v; return { t: "n", v: p === "-" ? -v : v }; }
        var e = un();
        return p === "-" ? { t: "u", e: e } : e;
      }
      return prim();
    }
    function prim() {
      var p = peek();
      if (p === "n") return { t: "n", v: t[i++].v };
      if (p === "(" || p === "[") { i++; var e = expr(), cl = p === "(" ? ")" : "]"; if (peek() !== cl) throw 0; i++; return e.t === "n" ? e : { t: "p", k: p, e: e }; }
      throw 0;
    }
    try { var r = expr(); return i === t.length ? r : null; } catch (e) { return null; }
  }
  function isN(x) { return x.t === "n"; }
  function first(x, pr) {
    if (x.t === "b") return first(x.l, pr) || (pr(x) ? x : null) || first(x.r, pr);
    if (x.t === "u") return first(x.e, pr) || (pr(x) ? x : null);
    return pr(x) ? x : null;
  }
  function grp(x) { return x.t === "p" && !isN(x.e); }
  /* ordre: parèntesis (de dins cap a fora) → signe davant del parèntesi → · i : → + i − (sempre d'esquerra a dreta) */
  function target(x, inG) {
    var g = first(x, grp);
    if (g) return target(g.e, true);
    var y = first(x, function (z) { return z.t === "u" && isN(z.e); }) ||
      first(x, function (z) { return z.t === "b" && (z.op === "·" || z.op === ":") && isN(z.l) && isN(z.r); }) ||
      first(x, function (z) { return z.t === "b" && (z.op === "+" || z.op === "-") && isN(z.l) && isN(z.r); });
    return y ? { n: y, g: !!inG } : null;
  }
  function applyOp(y) {
    if (y.t === "u") return { v: -y.e.v, k: "opp" };
    var a = y.l.v, b = y.r.v;
    if (y.op === "+") return { v: a + b, k: "add" };
    if (y.op === "-") return { v: a - b, k: "sub" };
    if (y.op === "·") return { v: a * b, k: "mul" };
    return !b ? { err: u("hDiv0") } : a % b ? { err: fill(u("hDiv"), { a: fh(a), b: fh(b) }) } : { v: a / b, k: "div" };
  }
  function repl(x, tg, nv) {
    if (x === tg) return nv;
    if (x.t === "b") return { t: "b", op: x.op, l: repl(x.l, tg, nv), r: repl(x.r, tg, nv) };
    if (x.t === "p") { var e = repl(x.e, tg, nv); return isN(e) ? e : { t: "p", k: x.k, e: e }; }
    if (x.t === "u") return { t: "u", e: repl(x.e, tg, nv) };
    return x;
  }
  /* lead: el terme va al principi (de tota l'expressió o d'un parèntesi), i un negatiu no necessita parèntesi */
  function tx(x, tg, val, lead) {
    var s;
    if (x.t === "n") s = x.v < 0 && !lead ? "(" + ft(x.v) + ")" : ft(x.v);
    else if (x.t === "p") s = x.k === "(" ? "\\left(" + tx(x.e, tg, val, true) + "\\right)" : "\\left[" + tx(x.e, tg, val, true) + "\\right]";
    else if (x.t === "u") s = "-" + (isN(x.e) ? "(" + ft(x.e.v) + ")" : tx(x.e, tg, val, false));
    else s = tx(x.l, tg, val, lead) + { "+": "+", "-": "-", "·": "\\cdot ", ":": ":" }[x.op] + tx(x.r, tg, val, false);
    if (x === tg) s = "\\underbrace{\\htmlClass{hl}{" + s + "}}_{\\htmlClass{hlv}{" + ft(val) + "}}";
    return s;
  }
  function run(s) {
    var tree = parseExpr(s), rows = [];
    if (!tree) return { err: u("hParse"), rows: rows };
    for (var guard = 0; guard < 80; guard++) {
      var tg = target(tree);
      if (!tg) break;
      var r = applyOp(tg.n);
      if (!r.err && Math.abs(r.v) > 1e12) r = { err: u("hBig") };
      if (r.err) return { err: r.err, rows: rows, last: tx(tree, null, 0, true) };
      rows.push({ t: tx(tree, tg.n, r.v, true), k: r.k, g: tg.g });
      tree = repl(tree, tg.n, { t: "n", v: r.v });
    }
    return { ok: true, v: tree.v, rows: rows, src: s };
  }
  function rowsHTML(res) {
    return res.rows.map(function (r, i) {
      return '<div class="hrow"><span class="hk">' + (i + 1) + " · " + u("kinds")[r.k] + (r.g ? " <small>(" + u("inPar") + ")</small>" : "") + "</span>" + tex(r.t) + "</div>";
    });
  }
  function wHier(w) {
    var inp = w.querySelector(".tin"), box = w.querySelector(".hsteps"), info = w.querySelector(".info"), shown = 1;
    var bn = w.querySelector('[data-a="next"]'), ba = w.querySelector('[data-a="all"]'), cnt = w.querySelector(".step-count"), ctl = w.querySelector(".steps-ctl");
    function render() {
      var res = run(inp.value), rows = rowsHTML(res), n = rows.length;
      if (shown > n) shown = Math.max(1, n);
      var end = res.ok && (n === 0 || shown >= n);
      box.innerHTML = rows.map(function (h, i) { return i < shown ? h : ""; }).join("");
      ctl.hidden = n < 2;
      bn.textContent = u("next") + " →"; bn.disabled = shown >= n;
      ba.textContent = shown >= n ? u("reset") : u("all");
      cnt.textContent = u("step") + " " + Math.min(shown, n) + " " + u("of") + " " + n;
      if (!res.ok) info.innerHTML = (res.last ? tex(res.last) + "<br>" : "") + '<span class="warn">' + res.err + "</span>";
      else if (n === 0) info.innerHTML = '<span class="hint">' + u("already") + "</span>";
      else info.innerHTML = end ? "<b>" + u("result") + "</b> " + tex("\\boxed{" + ft(res.v) + "}") : "";
    }
    inp.addEventListener("input", function () { shown = 1; render(); });
    bn.addEventListener("click", function () { shown++; render(); });
    ba.addEventListener("click", function () { var n = run(inp.value).rows.length; shown = shown >= n ? 1 : n; render(); });
    w.querySelectorAll(".quick button[data-e]").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.e; shown = 1; render(); }); });
    w.querySelectorAll(".quick button[data-ins]").forEach(function (b) {
      b.addEventListener("click", function () {
        var a = inp.selectionStart == null ? inp.value.length : inp.selectionStart, z = inp.selectionEnd == null ? a : inp.selectionEnd;
        inp.value = inp.value.slice(0, a) + b.dataset.ins + inp.value.slice(z);
        inp.focus(); inp.setSelectionRange(a + b.dataset.ins.length, a + b.dataset.ins.length); shown = 1; render();
      });
    });
    onLang(render);
  }

  /* ---------- giny: ascensor, temperatures i comptes ---------- */
  function wElev() {
    var w = document.getElementById("w-elev"); if (!w) return;
    var ch = w.querySelector(".chart"), info = w.querySelector(".info");
    function say(c, v) { var C = u("ctx")[c]; return v > 0 ? fill(C.p, { n: fh(v) }) : v < 0 ? fill(C.n, { n: fh(-v) }) : C.z; }
    function render() {
      var c = segVal(w) || "floor", s0 = readInt(w, "s", 9999), mv = readList(w.querySelector('[data-k="m"]').value, 20, 9999);
      if (s0 == null || !mv) { ch.innerHTML = ""; info.innerHTML = warn("elBad"); return; }
      var vals = [s0]; mv.forEach(function (d) { vals.push(vals[vals.length - 1] + d); });
      var n = vals.length, mn = Math.min.apply(null, vals.concat([0])), mx = Math.max.apply(null, vals.concat([0]));
      if (mx === mn) mx = mn + 1;
      var L = 56, Rr = 600, T = 18, B = 222, X = function (i) { return L + i * (Rr - L) / (n - 1 || 1); }, Y = function (v) { return T + (mx - v) / (mx - mn) * (B - T); };
      var st = 1; for (var q = 0; q < STEPS.length; q++) { st = STEPS[q]; if ((mx - mn) / st <= 8) break; }
      var s = "";
      for (var g = Math.ceil(mn / st) * st; g <= mx; g += st) s += '<line class="' + (g ? "sv-grid" : "el-zero") + '" x1="' + L + '" y1="' + Y(g) + '" x2="' + Rr + '" y2="' + Y(g) + '"/><text class="' + (g ? "sv-t" : "sv-tb") + '" x="' + (L - 8) + '" y="' + (Y(g) + 4) + '" text-anchor="end">' + fh(g) + "</text>";
      var d = "M" + X(0) + " " + Y(vals[0]);
      for (var i = 1; i < n; i++) d += " L" + X(i) + " " + Y(vals[i - 1]) + " L" + X(i) + " " + Y(vals[i]);
      s += '<path class="el-path" fill="none" d="' + d + '"/>';
      for (var j = 0; j < n; j++) {
        s += '<circle class="' + (j === n - 1 ? "ln-hl" : vals[j] < 0 ? "ln-n" : vals[j] > 0 ? "ln-p" : "ln-z") + '" cx="' + X(j) + '" cy="' + Y(vals[j]) + '" r="' + (j === n - 1 ? 7 : 5) + '"/>';
        if (j) s += '<text class="el-d ' + (mv[j - 1] > 0 ? "up" : "dn") + '" x="' + (X(j) - (X(j) - X(j - 1)) / 2) + '" y="' + (Y(vals[j - 1]) + (mv[j - 1] > 0 ? 16 : -7)) + '" text-anchor="middle">' + fs(mv[j - 1]) + "</text>";
      }
      s += '<text class="sv-t" x="' + X(0) + '" y="' + (B + 24) + '" text-anchor="middle">' + u("elStart") + '</text><text class="sv-t" x="' + X(n - 1) + '" y="' + (B + 24) + '" text-anchor="end">' + u("elEnd") + "</text>";
      ch.innerHTML = '<svg viewBox="0 0 620 252" role="img" aria-label="gràfic">' + s + "</svg>";
      var f = vals[n - 1], un = u("elUnit")[c];
      info.innerHTML = tex(ft(s0) + mv.map(function (x) { return (x >= 0 ? "+" : "") + ft(x); }).join("") + "=\\boxed{" + ft(f) + "}", true) +
        "<div>" + u("elSay") + " <b>" + say(c, f) + "</b></div>" +
        hint(fill(u("elVar"), { v: fs(f - s0) + un }) + " " + fill(u("elMax"), { M: fh(Math.max.apply(null, vals)) + un, m: fh(Math.min.apply(null, vals)) + un }));
    }
    w.querySelectorAll(".tin").forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, render);
    w.querySelectorAll(".quick button[data-b]").forEach(function (bt) { bt.addEventListener("click", function () { var p = bt.dataset.b.split("|"); segSet(w, p[0]); w.querySelector('[data-k="s"]').value = p[1]; w.querySelector('[data-k="m"]').value = p[2]; render(); }); });
    onLang(render);
  }

  /* ---------- entrenadors ---------- */
  function stepsTex(e) { var r = run(e); return r.rows.map(function (x) { return tex(x.t, true); }).join("") + tex("\\boxed{" + ft(r.v) + "}", true); }
  var GEN = {
    ord: function () {
      var v = [];
      while (v.length < rint(5, 7)) { var x = rint(-25, 25); if (v.indexOf(x) < 0) v.push(x); }
      var mx = Math.random() < .5, o = v.slice().sort(function (a, b) { return a - b; }), ans = mx ? o[o.length - 1] : o[0];
      return { ans: ans, q: function () { return u(mx ? "dMax" : "dMin") + " $" + v.map(ft).join(",\\ \\ ") + "$"; },
        s: function () { return lineSVG(v, [ans]) + tex(o.map(ft).join("<"), true); } };
    },
    abs: function () {
      var a = rnz(-30, 30), f = rint(0, 5), e, ans;
      if (f === 0) { e = "|" + ft(a) + "|"; ans = Math.abs(a); }
      else if (f === 1) { e = "\\text{op}(" + ft(a) + ")"; ans = -a; }
      else if (f === 2) { e = "\\text{op}(\\text{op}(" + ft(a) + "))"; ans = a; }
      else if (f === 3) { e = "|\\text{op}(" + ft(a) + ")|"; ans = Math.abs(a); }
      else if (f === 4) { e = "\\text{op}(|" + ft(a) + "|)"; ans = -Math.abs(a); }
      else { var d = 2 * rint(2, 40); return { ans: -d / 2, q: function () { return fill(u("dOpp"), { d: d }); }, s: function () { return tex(ft(d) + ":2=" + ft(d / 2) + "\\ \\to\\ " + ft(-d / 2) + "\\text{ i }" + ft(d / 2) + "\\ \\to\\ \\boxed{" + ft(-d / 2) + "}", true); } }; }
      return { ans: ans, q: function () { return u("dCalc") + " $" + e + "$"; }, s: function () { return tex(e + "=\\boxed{" + ft(ans) + "}", true); } };
    },
    add: function () {
      var a = rnz(-15, 15), b = rnz(-15, 15), k = rint(0, 2), t;
      if (k === 0) t = ft(a) + (b > 0 ? "+" : "-") + ft(Math.abs(b));
      else if (k === 1) t = fps(a) + pick(["+", "-"]) + fps(b);
      else { var c = rnz(-12, 12); t = ft(a) + (b > 0 ? "+" : "-") + ft(Math.abs(b)) + (c > 0 ? "+" : "-") + ft(Math.abs(c)); }
      var e = t.replace(/\\,/g, ""), r = run(e);
      return { ans: r.v, q: function () { return u("dCalc") + " $" + t + "$"; }, s: function () { var p = parTerms(e); return tex(p ? parSteps(p).tex : t + "=\\boxed{" + ft(r.v) + "}", true); } };
    },
    par: function () {
      var n = rint(3, 5), t = [];
      for (var i = 0; i < n; i++) {
        var o = i ? pick(["+", "-"]) : pick(["", "", "-"]), x = rint(1, 15);
        t.push(Math.random() < .7 ? o + "(" + pick(["+", "-"]) + x + ")" : o + x);
      }
      var e = t.join(""), p = parTerms(e);
      return { ans: parSteps(p).P - parSteps(p).N, q: function () { return u("dCalc") + " $" + p.map(function (x, i) { return termTex(x, !i); }).join("") + "$"; }, s: function () { return tex(parSteps(p).tex, true); } };
    },
    mul: function () {
      var k = rint(0, 3), a = rnz(-12, 12), b = rnz(-12, 12);
      if (k === 0) return { ans: a * b, q: function () { return u("dCalc") + " $" + fps(a) + "\\cdot " + fps(b) + "$"; }, s: function () { return tex(fps(a) + "\\cdot " + fps(b) + "=\\boxed{" + ft(a * b) + "}", true); } };
      if (k === 1) return { ans: a, q: function () { return u("dCalc") + " $" + fps(a * b) + ":" + fps(b) + "$"; }, s: function () { return tex(fps(a * b) + ":" + fps(b) + "=\\boxed{" + ft(a) + "}", true); } };
      if (k === 2) { var c = rnz(-6, 6); a = rnz(-6, 6); b = rnz(-6, 6); return { ans: a * b * c, q: function () { return u("dCalc") + " $" + fps(a) + "\\cdot " + fps(b) + "\\cdot " + fps(c) + "$"; }, s: function () { return tex(fps(a) + "\\cdot " + fps(b) + "\\cdot " + fps(c) + "=" + fp(a * b) + "\\cdot " + fps(c) + "=\\boxed{" + ft(a * b * c) + "}", true); } }; }
      return { ans: b, q: function () { return u("dMiss") + " $" + fps(a) + "\\cdot (\\ \\square\\ )=" + ft(a * b) + "$"; }, s: function () { return tex(ft(a * b) + ":" + fps(a) + "=\\boxed{" + ft(b) + "}", true); } };
    },
    comb: function () {
      function r() { return rnz(-9, 9); }
      for (;;) {
        var a = r(), b = r(), c = r(), d = r(), k = rint(0, 5), e;
        if (k === 0) e = fps(a) + "·" + fps(b) + "+" + fps(c) + "·" + fps(d);
        else if (k === 1) e = ft(a * 3) + "-" + fps(b) + "·" + fps(c);
        else if (k === 2) e = "(" + ft(a) + (b > 0 ? "+" : "-") + ft(Math.abs(b)) + ")·" + fps(c);
        else if (k === 3) e = fps(a * b) + ":" + fps(b) + "-" + fps(c) + "·" + fps(d);
        else if (k === 4) e = ft(a) + "-[" + ft(b) + "-(" + ft(c) + (d > 0 ? "+" : "-") + ft(Math.abs(d)) + ")]";
        else e = ft(a * 2) + "+" + fps(b) + "·[" + ft(c) + (d > 0 ? "+" : "-") + ft(Math.abs(d)) + "]";
        var res = run(e);
        if (!res.ok || Math.abs(res.v) > 150) continue;
        return { ans: res.v, q: function () { return u("dCalc") + " $" + tx(parseExpr(e), null, 0, true) + "$"; }, s: function () { return stepsTex(e); } };
      }
    }
  };
  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, good = false, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore");
    function paint() {
      dq.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (done) info.innerHTML = (good ? '<span class="ok">✓ ' + u("right") + "</span>" : '<span class="ko">✗ ' + u("wrong") + "</span>") + '<div class="dsol">' + q.s() + "</div>";
    }
    function check() {
      if (done) return;
      var v = pint(inp.value);
      if (isNaN(v)) { info.innerHTML = warn("write"); return; }
      done = true; tot++; good = v === q.ans; if (good) ok++;
      paint();
    }
    function fresh() { q = GEN[kind](); done = false; inp.value = ""; info.innerHTML = ""; paint(); }
    w.querySelector('[data-a="check"]').addEventListener("click", check);
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); inp.focus(); });
    w.querySelector('[data-a="neg"]').addEventListener("click", function () { var v = inp.value.trim(); inp.value = /^[−-]/.test(v) ? v.slice(1) : "−" + v; inp.focus(); });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    onLang(paint);
  }

  /* ---------- qüestionari ---------- */
  var QUIZ = [
    { q: { va: "«El cotxe està aparcat al tercer soterrani.» Quin enter ho representa?", es: "«El coche está aparcado en el tercer sótano.» ¿Qué entero lo representa?", en: "“The car is parked on the third basement level.” Which integer represents it?" },
      o: [{ va: "$+3$" }, { va: "$-3$" }, { va: "$3$" }, { va: "$-30$" }], a: 1,
      e: { va: "Per davall de la planta baixa (0) fem servir negatius: tercer soterrani $=-3$.", es: "Por debajo de la planta baja (0) usamos negativos: tercer sótano $=-3$.", en: "Below the ground floor (0) we use negatives: third basement $=-3$." } },
    { q: { va: "Quin d'aquests nombres <b>no</b> és un nombre natural?", es: "¿Cuál de estos números <b>no</b> es un número natural?", en: "Which of these is <b>not</b> a natural number?" },
      o: [{ va: "$0$" }, { va: "$+12$" }, { va: "$-1$" }, { va: "$100$" }], a: 2,
      e: { va: "Els naturals són $0, 1, 2, 3\\ldots$ (els enters positius i el zero). El $-1$ és enter, però no natural.", es: "Los naturales son $0, 1, 2, 3\\ldots$ (los enteros positivos y el cero). El $-1$ es entero, pero no natural.", en: "The natural numbers are $0, 1, 2, 3\\ldots$ (the positive integers and zero). $-1$ is an integer, but not a natural number." } },
    { q: { va: "Quina comparació és <b>correcta</b>?", es: "¿Qué comparación es <b>correcta</b>?", en: "Which comparison is <b>correct</b>?" },
      o: [{ va: "$-8>-3$" }, { va: "$-3<-8$" }, { va: "$-3>-8$" }, { va: "$0<-3$" }], a: 2,
      e: { va: "En la recta, $-3$ està més a la dreta que $-8$ (més a prop del 0): $-3>-8$.", es: "En la recta, $-3$ está más a la derecha que $-8$ (más cerca del 0): $-3>-8$.", en: "On the number line, $-3$ is to the right of $-8$ (closer to 0): $-3>-8$." } },
    { q: { va: "Ordenats de menor a major, $\\ 2,\\ -5,\\ 0,\\ -1\\ $ queden…", es: "Ordenados de menor a mayor, $\\ 2,\\ -5,\\ 0,\\ -1\\ $ quedan…", en: "From smallest to largest, $\\ 2,\\ -5,\\ 0,\\ -1\\ $ are…" },
      o: [{ va: "$0<-1<2<-5$" }, { va: "$-1<-5<0<2$" }, { va: "$-5<-1<0<2$" }, { va: "$2<0<-1<-5$" }], a: 2,
      e: { va: "Primer els negatius (el més allunyat del 0 és el menor), després el 0 i després els positius.", es: "Primero los negativos (el más alejado del 0 es el menor), después el 0 y después los positivos.", en: "First the negatives (the furthest from 0 is the smallest), then 0, then the positives." } },
    { q: { va: "$|-9|=$", es: "$|-9|=$", en: "$|-9|=$" }, o: [{ va: "$-9$" }, { va: "$9$" }, { va: "$0$" }, { va: "$\\pm9$" }], a: 1,
      e: { va: "El valor absolut és una distància: mai no és negatiu. $-9$ està a 9 unitats del 0.", es: "El valor absoluto es una distancia: nunca es negativo. $-9$ está a 9 unidades del 0.", en: "Absolute value is a distance: it is never negative. $-9$ is 9 units from 0." } },
    { q: { va: "$\\text{op}(\\text{op}(-4))=$", es: "$\\text{op}(\\text{op}(-4))=$", en: "$\\text{op}(\\text{op}(-4))=$" }, o: [{ va: "$4$" }, { va: "$-4$" }, { va: "$0$" }, { va: "$8$" }], a: 1,
      e: { va: "$\\text{op}(-4)=4$ i $\\text{op}(4)=-4$. Canviar el signe dues vegades ens torna al nombre inicial.", es: "$\\text{op}(-4)=4$ y $\\text{op}(4)=-4$. Cambiar el signo dos veces nos devuelve al número inicial.", en: "$\\text{op}(-4)=4$ and $\\text{op}(4)=-4$. Changing the sign twice gives back the starting number." } },
    { q: { va: "Dos nombres oposats estan a 14 unitats l'un de l'altre. Quins són?", es: "Dos números opuestos están a 14 unidades el uno del otro. ¿Cuáles son?", en: "Two opposite numbers are 14 units apart. Which are they?" },
      o: [{ va: "$14$ i $-14$", es: "$14$ y $-14$", en: "$14$ and $-14$" }, { va: "$0$ i $14$", es: "$0$ y $14$", en: "$0$ and $14$" }, { va: "$7$ i $-7$", es: "$7$ y $-7$", en: "$7$ and $-7$" }, { va: "$-7$ i $-14$", es: "$-7$ y $-14$", en: "$-7$ and $-14$" }], a: 2,
      e: { va: "Cadascun està a la meitat de la distància del 0: $14:2=7$.", es: "Cada uno está a la mitad de la distancia del 0: $14:2=7$.", en: "Each is half the distance from 0: $14:2=7$." } },
    { q: { va: "$-7+4=$", es: "$-7+4=$", en: "$-7+4=$" }, o: [{ va: "$-11$" }, { va: "$3$" }, { va: "$-3$" }, { va: "$11$" }], a: 2,
      e: { va: "Signes diferents: restem $7-4=3$ i posem el signe del 7 (negatiu). Si dec 7 € i en pague 4, encara en dec 3.", es: "Signos distintos: restamos $7-4=3$ y ponemos el signo del 7 (negativo). Si debo 7 € y pago 4, aún debo 3.", en: "Different signs: subtract $7-4=3$ and keep the sign of 7 (negative). If I owe €7 and pay €4, I still owe €3." } },
    { q: { va: "$-5-6=$", es: "$-5-6=$", en: "$-5-6=$" }, o: [{ va: "$-1$" }, { va: "$1$" }, { va: "$11$" }, { va: "$-11$" }], a: 3,
      e: { va: "Mateix signe: sumem $5+6=11$ i posem el signe comú: $-11$.", es: "Mismo signo: sumamos $5+6=11$ y ponemos el signo común: $-11$.", en: "Same sign: add $5+6=11$ and keep the common sign: $-11$." } },
    { q: { va: "$4-(-6)=$", es: "$4-(-6)=$", en: "$4-(-6)=$" }, o: [{ va: "$-2$" }, { va: "$10$" }, { va: "$2$" }, { va: "$-10$" }], a: 1,
      e: { va: "$-(-\\ \\to\\ +$: $\\ 4-(-6)=4+6=10$.", es: "$-(-\\ \\to\\ +$: $\\ 4-(-6)=4+6=10$.", en: "$-(-\\ \\to\\ +$: $\\ 4-(-6)=4+6=10$." } },
    { q: { va: "$-(+3)+(-2)-(-8)=$", es: "$-(+3)+(-2)-(-8)=$", en: "$-(+3)+(-2)-(-8)=$" }, o: [{ va: "$3$" }, { va: "$-13$" }, { va: "$-3$" }, { va: "$13$" }], a: 0,
      e: { va: "$-3-2+8=8-5=3$.", es: "$-3-2+8=8-5=3$.", en: "$-3-2+8=8-5=3$." } },
    { q: { va: "$10-(2-7)=$", es: "$10-(2-7)=$", en: "$10-(2-7)=$" }, o: [{ va: "$5$" }, { va: "$15$" }, { va: "$1$" }, { va: "$-15$" }], a: 1,
      e: { va: "Primer el parèntesi: $2-7=-5$. Després, $10-(-5)=10+5=15$.", es: "Primero el paréntesis: $2-7=-5$. Después, $10-(-5)=10+5=15$.", en: "Brackets first: $2-7=-5$. Then $10-(-5)=10+5=15$." } },
    { q: { va: "$(-6)\\cdot(-4)=$", es: "$(-6)\\cdot(-4)=$", en: "$(-6)\\cdot(-4)=$" }, o: [{ va: "$-24$" }, { va: "$-10$" }, { va: "$24$" }, { va: "$10$" }], a: 2,
      e: { va: "Menys per menys és més: $6\\cdot4=24$ amb signe $+$.", es: "Menos por menos es más: $6\\cdot4=24$ con signo $+$.", en: "Minus times minus is plus: $6\\cdot4=24$ with a $+$ sign." } },
    { q: { va: "$(+42):(-7)=$", es: "$(+42):(-7)=$", en: "$(+42):(-7)=$" }, o: [{ va: "$6$" }, { va: "$-6$" }, { va: "$35$" }, { va: "$-35$" }], a: 1,
      e: { va: "Signes diferents: resultat negatiu. $42:7=6\\ \\to\\ -6$.", es: "Signos distintos: resultado negativo. $42:7=6\\ \\to\\ -6$.", en: "Different signs: negative result. $42:7=6\\ \\to\\ -6$." } },
    { q: { va: "El signe de $(-2)\\cdot(-3)\\cdot(-1)\\cdot(+5)$ és…", es: "El signo de $(-2)\\cdot(-3)\\cdot(-1)\\cdot(+5)$ es…", en: "The sign of $(-2)\\cdot(-3)\\cdot(-1)\\cdot(+5)$ is…" },
      o: [{ va: "positiu", es: "positivo", en: "positive" }, { va: "negatiu", es: "negativo", en: "negative" }, { va: "depén de l'ordre", es: "depende del orden", en: "it depends on the order" }, { va: "no en té", es: "no tiene", en: "it has none" }], a: 1,
      e: { va: "Hi ha tres factors negatius (un nombre senar): el resultat és negatiu, $-30$.", es: "Hay tres factores negativos (un número impar): el resultado es negativo, $-30$.", en: "There are three negative factors (an odd number): the result is negative, $-30$." } },
    { q: { va: "$-3+4\\cdot(-2)=$", es: "$-3+4\\cdot(-2)=$", en: "$-3+4\\cdot(-2)=$" }, o: [{ va: "$-2$" }, { va: "$-11$" }, { va: "$5$" }, { va: "$-5$" }], a: 1,
      e: { va: "Primer la multiplicació: $4\\cdot(-2)=-8$. Després, $-3-8=-11$. (Si sumes primer, $1\\cdot(-2)=-2$, és un error típic!)", es: "Primero la multiplicación: $4\\cdot(-2)=-8$. Después, $-3-8=-11$. (Si sumas primero, $1\\cdot(-2)=-2$, ¡es un error típico!)", en: "Multiplication first: $4\\cdot(-2)=-8$. Then $-3-8=-11$. (Adding first, $1\\cdot(-2)=-2$, is a common mistake!)" } },
    { q: { va: "A les 7 h fa $-4$ °C i a les 14 h, $9$ °C. Quants graus ha pujat la temperatura?", es: "A las 7 h hace $-4$ °C y a las 14 h, $9$ °C. ¿Cuántos grados ha subido la temperatura?", en: "At 7 am it's $-4$ °C and at 2 pm it's $9$ °C. How many degrees has the temperature risen?" },
      o: [{ va: "$5$ °C" }, { va: "$13$ °C" }, { va: "$-13$ °C" }, { va: "$9$ °C" }], a: 1,
      e: { va: "Final menys inicial: $9-(-4)=9+4=13$ °C.", es: "Final menos inicial: $9-(-4)=9+4=13$ °C.", en: "Final minus initial: $9-(-4)=9+4=13$ °C." } },
    { q: { va: "Arquimedes va nàixer l'any 287 a. C. i va morir l'any 212 a. C. Quants anys va viure?", es: "Arquímedes nació el año 287 a. C. y murió el año 212 a. C. ¿Cuántos años vivió?", en: "Archimedes was born in 287 BC and died in 212 BC. How many years did he live?" },
      o: [{ va: "$499$" }, { va: "$75$" }, { va: "$-75$" }, { va: "$212$" }], a: 1,
      e: { va: "$-212-(-287)=-212+287=75$ anys.", es: "$-212-(-287)=-212+287=75$ años.", en: "$-212-(-287)=-212+287=75$ years." } }
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

  var TITLES = { va: "Nombres enters · FentMates", es: "Números enteros · FentMates", en: "Integers · FentMates" };
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
    wCtx(); wLine(); wAbs(); wAdd(); wPar(); wSign(); wElev();
    document.querySelectorAll(".w-hier").forEach(wHier);
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
