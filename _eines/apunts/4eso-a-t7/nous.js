  /* ======================= ginys nous de 4t ESO A, unitat 7 ======================= */
  function niceStep(span, n) { var r = span / (n || 6), p = Math.pow(10, Math.floor(Math.log(r) / Math.LN10)), k = r / p; return (k <= 1 ? 1 : k <= 2 ? 2 : k <= 5 ? 5 : 10) * p; }
  function grp(v) { var s = decS(v, 2), i = s.search(/[.,]|$/), a = s.slice(0, i), b = s.slice(i), neg = a[0] === "-"; if (neg) a = a.slice(1); if (a.length > 3) a = a.replace(/\B(?=(\d{3})+(?!\d))/g, lang === "en" ? "," : "\\,"); return (neg ? "-" : "") + a + b; }

  /* ---------- 7.1 tipus de funcions lineals: y = mx + n ---------- */
  function wTypes() {
    var w = byId("w-types"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), S = {};
    ["m", "n"].forEach(function (k) { S[k] = $(w, k); S[k].addEventListener("input", draw); });
    function draw() {
      var m = +S.m.value, n = +S.n.value, mf = Fr(Math.round(m * 2), 2);
      $(w, "mv").innerHTML = dT(m, 1); $(w, "nv").innerHTML = numT(n);
      var G = plane(-6, 6, -6, 6, 1), h = G.g + G.open + curve(G, function (x) { return m * x + n; }, AC, { n: 20 });
      if (m) h += seg(G, 0, n, 1, n, OR, 2.2) + seg(G, 1, n, 1, n + m, GR, 2.2) + gtext(G, .5, n, "1", OR, 0, m > 0 ? 14 : -6) + gtext(G, 1, n + m / 2, dT(m, 1).replace("{,}", lang === "en" ? "." : ","), GR, 16, 4);
      h += gdot(G, 0, n, BL);
      if (m && Math.abs(-n / m) <= 6) h += gdot(G, -n / m, 0, VI);
      svg.innerHTML = h + G.close;
      var type, mono = m > 0 ? t3("creixent", "creciente", "increasing") : t3("decreixent", "decreciente", "decreasing");
      if (!m) type = "<strong>" + t3("Funció constant", "Función constante", "Constant function") + "</strong>" + small(t3("m = 0: recta horitzontal a altura ", "m = 0: recta horizontal a altura ", "m = 0: horizontal line at height ") + n);
      else if (!n) type = "<strong>" + t3("Proporcionalitat directa", "Proporcionalidad directa", "Direct proportion") + "</strong>" + small(t3("n = 0: passa per l'origen (0, 0); ", "n = 0: pasa por el origen (0, 0); ", "n = 0: goes through the origin (0, 0); ") + mono);
      else type = "<strong>" + t3("Funció afí", "Función afín", "Affine function") + "</strong>" + small(t3("m ≠ 0 i n ≠ 0; ", "m ≠ 0 y n ≠ 0; ", "m ≠ 0 and n ≠ 0; ") + mono);
      var tb = '<div class="tbl-wrap"><table class="data tr"><tr><th>' + tex("x") + "</th>" + [0, 1, 2, 3].map(function (x) { return "<td>" + tex(String(x)) + "</td>"; }).join("") + "</tr><tr><th>" + tex("y") + "</th>" + [0, 1, 2, 3].map(function (x) { return "<td>" + tex(fT(fAdd(fMul(mf, x), n))) + "</td>"; }).join("") + "</tr></table></div>";
      info.innerHTML = kv([
        ["", "<strong>" + tex("y=" + polyT([Fr(n), mf])) + "</strong>"],
        [t3("Tipus", "Tipo", "Type"), type],
        [t3("Pendent", "Pendiente", "Slope"), tex("m=" + fT(mf)) + small(m ? t3("Quan x augmenta 1, y ", "Cuando x aumenta 1, y ", "When x goes up by 1, y ") + (m > 0 ? t3("augmenta ", "aumenta ", "goes up by ") : t3("disminueix ", "disminuye ", "goes down by ")) + decS(Math.abs(m), 1) : t3("La y no canvia mai.", "La y no cambia nunca.", "y never changes."))],
        [t3("Ordenada en l'origen", "Ordenada en el origen", "y-intercept"), tex("n=" + n) + " → " + tex("(0,\\ " + n + ")")],
        [t3("Taula", "Tabla", "Table"), tb]
      ]);
    }
    onLang(draw);
  }

  /* ---------- 7.4 representació d'una paràbola pas a pas ---------- */
  function wQStep() {
    var w = byId("w-qstep"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), nx = $(w, "next"), rs = $(w, "reset"), cur = 0, st = 0, NST = 6;
    var PR = [[1, -4, 3], [-1, 2, 3], [1, 2, 2], [1, 0, -4], [-1, -4, -3]];
    presetBtns($(w, "pre"), function () { return PR.map(function (p) { return tex("y=" + polyT([Fr(p[2]), Fr(p[1]), Fr(p[0])])); }); }, function (i) { cur = i; st = 0; draw(); }, 0);
    nx.addEventListener("click", function () { if (st < NST) { st++; draw(); } });
    rs.addEventListener("click", function () { st = 0; draw(); });
    function draw() {
      var p = PR[cur], a = p[0], b = p[1], c = p[2], f = function (x) { return a * x * x + b * x + c; };
      var vx = Fr(-b, 2 * a), xv = fVal(vx), yv = f(xv), D = b * b - 4 * a * c, rts = D > 0 ? [(-b - Math.sqrt(D)) / (2 * a), (-b + Math.sqrt(D)) / (2 * a)].sort(function (u, v) { return u - v; }) : D === 0 ? [xv] : [];
      var G = plane(-7, 7, -6, 8, 1), h = G.g + G.open, rows = [["", "<strong>" + tex("f(x)=" + polyT([Fr(c), Fr(b), Fr(a)])) + "</strong>"]], msg = [];
      var up = a > 0, cup = up ? "∪" : "∩";
      if (st === 0) msg.push(t3("Prem «Següent pas» per a començar.", "Pulsa «Siguiente paso» para empezar.", "Press “Next step” to start."));
      if (st >= 1) rows.push([t3("1. Forma", "1. Forma", "1. Shape"), tex("a=" + a) + (up ? t3(" > 0: branques cap amunt ", " > 0: ramas hacia arriba ", " > 0: arms up ") : t3(" < 0: branques cap avall ", " < 0: ramas hacia abajo ", " < 0: arms down ")) + cup]);
      if (st >= 2) { h += vdash(G, xv) + gdot(G, xv, yv, VI, 6); rows.push([t3("2. Vèrtex i eix", "2. Vértice y eje", "2. Vertex and axis"), tex("V_x=\\dfrac{-b}{2a}=\\dfrac{" + (-b) + "}{" + 2 * a + "}=" + fT(vx) + ",\\ \\ V_y=f(" + fT(vx) + ")=" + niceT(yv)) + "<br>V" + tex("(" + fT(vx) + ",\\ " + niceT(yv) + ")") + ", " + t3("eix ", "eje ", "axis ") + tex("x=" + fT(vx))]); }
      if (st >= 3) {
        h += gdot(G, 0, c, GR);
        var sym = 2 * xv, txt = tex("f(0)=" + c) + " → " + tex("(0,\\ " + c + ")");
        if (Math.abs(sym) > 1e-9) { h += gdot(G, sym, c, GR); txt += "<br>" + t3("Simètric respecte de l'eix: ", "Simétrico respecto del eje: ", "Mirror point across the axis: ") + tex("(" + niceT(sym) + ",\\ " + c + ")"); }
        else txt += small(t3("El vèrtex és sobre l'eix OY.", "El vértice está sobre el eje OY.", "The vertex lies on the y-axis."));
        rows.push([t3("3. Tall amb OY", "3. Corte con OY", "3. y-intercept"), txt]);
      }
      if (st >= 4) {
        rts.forEach(function (r) { h += gdot(G, r, 0, BL); });
        rows.push([t3("4. Talls amb OX", "4. Cortes con OX", "4. x-intercepts"), tex(polyT([Fr(c), Fr(b), Fr(a)]) + "=0") + ": " + (rts.length ? tex("x=" + rts.map(function (r) { return niceT(snap(r)); }).join(",\\ x=")) : t3("Δ = " + D + " < 0, no en té", "Δ = " + D + " < 0, no tiene", "Δ = " + D + " < 0, none"))]);
      }
      if (st >= 5) {
        var xs = [xv - 2, xv - 1, xv, xv + 1, xv + 2];
        xs.forEach(function (x) { h += gdot(G, x, f(x), OR, 4); });
        rows.push([t3("5. Taula de valors", "5. Tabla de valores", "5. Table of values"), '<div class="tbl-wrap"><table class="data tr"><tr><th>' + tex("x") + "</th>" + xs.map(function (x) { return "<td>" + tex(niceT(x)) + "</td>"; }).join("") + "</tr><tr><th>" + tex("y") + "</th>" + xs.map(function (x) { return "<td>" + tex(niceT(f(x))) + "</td>"; }).join("") + "</tr></table></div>" + small(t3("Agafem valors a banda i banda del vèrtex: per simetria, les imatges es repeteixen.", "Tomamos valores a ambos lados del vértice: por simetría, las imágenes se repiten.", "Take values on both sides of the vertex: by symmetry, the images repeat."))]);
      }
      if (st >= 6) {
        h = h.replace(G.open, G.open + curve(G, f, AC, { n: 500 }));
        rows.push([t3("6. Gràfica", "6. Gráfica", "6. Graph"), t3("Unim els punts amb una corba suau i simètrica.", "Unimos los puntos con una curva suave y simétrica.", "Join the points with a smooth, symmetric curve.") + "<br>" + t3("Recorregut: ", "Recorrido: ", "Range: ") + tex(up ? "[" + niceT(yv) + ",\\,+\\infty)" : "(-\\infty,\\," + niceT(yv) + "]") + "<br>" + (up ? t3("Decreixent en ", "Decreciente en ", "Decreasing on ") + tex("(-\\infty,\\," + fT(vx) + ")") + t3(" i creixent en ", " y creciente en ", " and increasing on ") + tex("(" + fT(vx) + ",\\,+\\infty)") + t3("; mínim en V.", "; mínimo en V.", "; minimum at V.") : t3("Creixent en ", "Creciente en ", "Increasing on ") + tex("(-\\infty,\\," + fT(vx) + ")") + t3(" i decreixent en ", " y decreciente en ", " and decreasing on ") + tex("(" + fT(vx) + ",\\,+\\infty)") + t3("; màxim en V.", "; máximo en V.", "; maximum at V."))]);
      }
      if (msg.length) rows.push([t3("Pas", "Paso", "Step"), msg.join("")]);
      nx.disabled = st >= NST;
      svg.innerHTML = h + G.close; info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- 7.6 proporcionalitat inversa: x · y = k ---------- */
  function wInv() {
    var w = byId("w-inv"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), S = {};
    ["k", "x"].forEach(function (r) { S[r] = $(w, r); S[r].addEventListener("input", draw); });
    function draw() {
      var k = +S.k.value, x = +S.x.value;
      if (!k) { k = 1; S.k.value = 1; }
      if (!x) { x = .5; S.x.value = .5; }
      $(w, "kv").innerHTML = numT(k); $(w, "xv").innerHTML = dT(x, 1);
      var y = k / x, G = plane(-8, 8, -8, 8, 2), f = function (t) { return Math.abs(t) < 1e-9 ? NaN : k / t; };
      var rx = G.X(Math.min(0, x)), ry = G.Y(Math.max(0, y)), rw = Math.abs(G.X(x) - G.X(0)), rh = Math.abs(G.Y(y) - G.Y(0));
      var h = G.g + G.open + '<rect x="' + f1(rx) + '" y="' + f1(ry) + '" width="' + f1(rw) + '" height="' + f1(rh) + '" style="fill:' + BL + ';fill-opacity:.16;stroke:' + BL + ';stroke-width:1.5"/>' + curve(G, f, AC, { n: 1600 }) + gdot(G, x, y, BL, 6);
      svg.innerHTML = h + G.close;
      var xs = [1, 2, 3, 4, 6], tb = '<div class="tbl-wrap"><table class="data tr"><tr><th>' + tex("x") + "</th>" + xs.map(function (v) { return "<td>" + tex(String(v)) + "</td>"; }).join("") + "</tr><tr><th>" + tex("y") + "</th>" + xs.map(function (v) { return "<td>" + tex(fT(Fr(k, v))) + "</td>"; }).join("") + "</tr></table></div>";
      info.innerHTML = kv([
        ["", "<strong>" + tex("y=\\dfrac{" + k + "}{x}") + "</strong>"],
        [t3("Punt", "Punto", "Point"), tex("x=" + dT(x, 1) + "\\ \\Rightarrow\\ y=\\dfrac{" + k + "}{" + dT(x, 1) + "}" + apx(y, 2))],
        [t3("Producte", "Producto", "Product"), tex("x\\cdot y=" + dT(x, 1) + "\\cdot" + (y < 0 ? "\\left(" + dT(y, 2) + "\\right)" : dT(y, 2)) + (Math.abs(y * 100 - Math.round(y * 100)) > 1e-9 ? "\\approx " : "=") + k) + small(t3("El rectangle blau té sempre la mateixa àrea: ", "El rectángulo azul tiene siempre la misma área: ", "The blue rectangle always has the same area: ") + Math.abs(k))],
        [t3("Branques", "Ramas", "Branches"), k > 0 ? t3("1r i 3r quadrant; decreixent a cada branca", "1.er y 3.er cuadrante; decreciente en cada rama", "1st and 3rd quadrants; decreasing on each branch") : t3("2n i 4t quadrant; creixent a cada branca", "2.º y 4.º cuadrante; creciente en cada rama", "2nd and 4th quadrants; increasing on each branch")],
        [t3("Taula", "Tabla", "Table"), tb]
      ]);
    }
    onLang(draw);
  }

  /* ---------- 7.8 creixement i decreixement exponencial: y = C · a^t ---------- */
  function wGrow() {
    var w = byId("w-grow"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), S = {};
    ["C", "p"].forEach(function (r) { S[r] = $(w, r); S[r].addEventListener("input", draw); });
    function draw() {
      var C = +S.C.value, p = +S.p.value;
      if (!p) { p = 5; S.p.value = 5; }
      $(w, "Cv").innerHTML = numT(C); $(w, "pv").innerHTML = (p > 0 ? "+" : "") + p + " %";
      var a = 1 + p / 100, f = function (t) { return C * Math.pow(a, t); }, T = 8, top = Math.max(C, f(T)) * 1.12, sy = niceStep(top, 5);
      var G = gview({ x0: -.6, x1: T + .4, y0: -top * .08, y1: top, sy: sy, W: 360, H: 260, pl: 44, xt: ticks(0, T, 1) }), h = G.g + G.open + curve(G, f, AC, { a: 0, b: T, n: 300 });
      for (var t = 0; t <= T; t++) h += gdot(G, t, f(t), t ? BL : GR, 4);
      svg.innerHTML = h + G.close;
      var ts = [0, 1, 2, 3, 4, 5];
      var aT = dT(a, 2);
      info.innerHTML = kv([
        ["", "<strong>" + tex("y=" + C + "\\cdot" + aT + "^{\\,t}") + "</strong>"],
        [t3("Factor", "Factor", "Factor"), tex("a=1" + (p > 0 ? "+" : "-") + "\\dfrac{" + Math.abs(p) + "}{100}=" + aT) + small(p > 0 ? t3("Augmenta un ", "Aumenta un ", "Increases by ") + Math.abs(p) + t3(" % cada unitat de temps", " % cada unidad de tiempo", " % each time unit") : t3("Disminueix un ", "Disminuye un ", "Decreases by ") + Math.abs(p) + t3(" % cada unitat de temps", " % cada unidad de tiempo", " % each time unit"))],
        [t3("Tipus", "Tipo", "Type"), a > 1 ? '<strong class="sp">' + t3("Creixement exponencial", "Crecimiento exponencial", "Exponential growth") + "</strong>" + small(t3("a > 1: creix cada vegada més de pressa", "a > 1: crece cada vez más deprisa", "a > 1: grows faster and faster")) : '<strong class="sm">' + t3("Decreixement exponencial", "Decrecimiento exponencial", "Exponential decay") + "</strong>" + small(t3("0 < a < 1: decreix cada vegada més a poc a poc, sense arribar a 0", "0 < a < 1: decrece cada vez más despacio, sin llegar a 0", "0 < a < 1: decays more and more slowly, never reaching 0"))],
        [t3("Taula", "Tabla", "Table"), '<div class="tbl-wrap"><table class="data tr"><tr><th>' + tex("t") + "</th>" + ts.map(function (t) { return "<td>" + tex(String(t)) + "</td>"; }).join("") + "</tr><tr><th>" + tex("y") + "</th>" + ts.map(function (t) { return "<td>" + tex(grp(f(t))) + "</td>"; }).join("") + "</tr></table></div>" + small(t3("Cada valor és l'anterior multiplicat per ", "Cada valor es el anterior multiplicado por ", "Each value is the previous one times ") + decS(a, 2) + ".")]
      ]);
    }
    onLang(draw);
  }

  /* ---------- 7.9 comparació de dues tarifes lineals ---------- */
  function wCmp() {
    var w = byId("w-cmp"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), S = {};
    ["nA", "mA", "nB", "mB"].forEach(function (r) { S[r] = $(w, r); S[r].addEventListener("input", draw); });
    function draw() {
      var nA = +S.nA.value, mA = +S.mA.value, nB = +S.nB.value, mB = +S.mB.value, X1 = 20;
      ["nA", "mA", "nB", "mB"].forEach(function (r) { $(w, r + "v").innerHTML = dT(+S[r].value, 2) + " €"; });
      var A = function (x) { return nA + mA * x; }, B = function (x) { return nB + mB * x; }, top = Math.max(A(X1), B(X1), 10) * 1.1, sy = niceStep(top, 5);
      var G = gview({ x0: -1, x1: X1 + .5, y0: -top * .06, y1: top, sy: sy, W: 360, H: 260, pl: 38, xt: ticks(0, X1, 2) }), h = G.g + G.open;
      h += curve(G, A, OR, { a: 0, b: X1, n: 20 }) + curve(G, B, BL, { a: 0, b: X1, n: 20 }) + gtext(G, X1 - .6, A(X1 - .6), "A", OR, 0, -9) + gtext(G, X1 - .6, B(X1 - .6), "B", BL, 0, -9);
      var rows = [[cdot(OR) + "A", tex("A(x)=" + dT(mA, 2) + "x" + (nA ? "+" + dT(nA, 2) : ""))], [cdot(BL) + "B", tex("B(x)=" + dT(mB, 2) + "x" + (nB ? "+" + dT(nB, 2) : ""))]], msg;
      var cheap = function (x) { var d = A(x) - B(x); return Math.abs(d) < 1e-9 ? 0 : d < 0 ? "A" : "B"; };
      if (Math.abs(mA - mB) < 1e-9) {
        msg = Math.abs(nA - nB) < 1e-9 ? t3("Són la mateixa tarifa.", "Son la misma tarifa.", "They are the same tariff.") : t3("Rectes paral·leles (mateix preu per unitat): sempre convé ", "Rectas paralelas (mismo precio por unidad): siempre conviene ", "Parallel lines (same price per unit): always choose ") + (nA < nB ? "A" : "B") + ".";
      } else {
        var xs = (nB - nA) / (mA - mB), ys = A(xs);
        if (xs > 0 && xs <= X1) h += vdash(G, xs) + gdot(G, xs, ys, VI, 6);
        rows.push([t3("Costen igual", "Cuestan igual", "Same cost"), tex(dT(mA, 2) + "x" + (nA ? "+" + dT(nA, 2) : "") + "=" + dT(mB, 2) + "x" + (nB ? "+" + dT(nB, 2) : "") + "\\Rightarrow x" + apx(xs, 2)) + (xs > 0 ? " (" + tex(dT(ys, 2)) + " €)" : "")]);
        if (xs <= 0) msg = t3("Per a qualsevol x > 0 convé ", "Para cualquier x > 0 conviene ", "For every x > 0 choose ") + cheap(1) + ".";
        else msg = t3("Si x < ", "Si x < ", "If x < ") + decS(xs, 2) + t3(" convé ", " conviene ", " choose ") + "<strong>" + cheap(xs / 2) + "</strong>; " + t3("si x > ", "si x > ", "if x > ") + decS(xs, 2) + ", <strong>" + cheap(xs + 1) + "</strong>" + t3(" (la seua recta queda per davall).", " (su recta queda por debajo).", " (its line is lower).");
      }
      rows.push([t3("Quina convé?", "¿Cuál conviene?", "Which is cheaper?"), msg]);
      svg.innerHTML = h + G.close; info.innerHTML = kv(rows);
    }
    onLang(draw);
  }
