  /* ======================= ginys nous de 4t ESO A, unitat 6 ======================= */

  /* ---------- 6.7 lectura d'un gràfic amb context ---------- */
  function wRead() {
    var w = byId("w-read"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), sl = $(w, "t"), cur = 0;
    var C = [
      { name: function () { return t3("Excursió", "Excursión", "Hike"); }, P: [[0, 0], [2, 8], [3, 8], [4, 10], [6, 0]], v: { x0: -.4, x1: 6.6, y0: -1.2, y1: 12, sy: 2, xs: 1 },
        xu: "h", yu: "km", st: .05,
        xv: function () { return t3("temps", "tiempo", "time"); }, yv: function () { return t3("distància a casa", "distancia a casa", "distance from home"); },
        up: function (r) { return t3("S'allunya de casa a ", "Se aleja de casa a ", "Moving away from home at ") + r + " km/h"; },
        eq: function (y) { return t3("Està parat (descansa) a ", "Está parado (descansa) a ", "Stopped (resting) at ") + y + t3(" km de casa", " km de casa", " km from home"); },
        dn: function (r) { return t3("Torna cap a casa a ", "Vuelve hacia casa a ", "Heading back home at ") + r + " km/h"; } },
      { name: function () { return t3("Dipòsit", "Depósito", "Water tank"); }, P: [[0, 0], [10, 200], [15, 200], [25, 0]], v: { x0: -1.5, x1: 27, y0: -25, y1: 240, sy: 40, xs: 5 },
        xu: "min", yu: "L", st: .25,
        xv: function () { return t3("temps", "tiempo", "time"); }, yv: function () { return t3("volum d'aigua", "volumen de agua", "volume of water"); },
        up: function (r) { return t3("S'omple a ", "Se llena a ", "Filling at ") + r + " L/min"; },
        eq: function (y) { return t3("Ni s'omple ni es buida: té ", "Ni se llena ni se vacía: tiene ", "Neither filling nor emptying: it holds ") + y + " L"; },
        dn: function (r) { return t3("Es buida a ", "Se vacía a ", "Emptying at ") + r + " L/min"; } },
      { name: function () { return t3("Temperatura", "Temperatura", "Temperature"); }, P: [[0, 6], [6, 2], [15, 14], [24, 6]], v: { x0: -1, x1: 25, y0: -1, y1: 16, sy: 2, xs: 3 },
        xu: "h", yu: "°C", st: .25,
        xv: function () { return t3("hora", "hora", "time of day"); }, yv: function () { return t3("temperatura", "temperatura", "temperature"); },
        up: function (r) { return t3("La temperatura puja ", "La temperatura sube ", "Temperature rising ") + r + t3(" °C cada hora", " °C cada hora", " °C per hour"); },
        eq: function (y) { return t3("La temperatura es manté a ", "La temperatura se mantiene a ", "Temperature steady at ") + y + " °C"; },
        dn: function (r) { return t3("La temperatura baixa ", "La temperatura baja ", "Temperature falling ") + r + t3(" °C cada hora", " °C cada hora", " °C per hour"); } }
    ];
    presetBtns($(w, "pre"), function () { return C.map(function (c) { return c.name(); }); }, function (i) {
      cur = i; var P = C[i].P; sl.min = P[0][0]; sl.max = P[P.length - 1][0]; sl.step = C[i].st; sl.value = (P[1][0] + P[2][0]) / 2; draw();
    }, 0);
    sl.addEventListener("input", draw);
    function val(P, t) {
      for (var i = 0; i < P.length - 1; i++) if (t <= P[i + 1][0] + 1e-9) return { i: i, y: P[i][1] + (P[i + 1][1] - P[i][1]) * (t - P[i][0]) / (P[i + 1][0] - P[i][0]) };
      return { i: P.length - 2, y: P[P.length - 1][1] };
    }
    function draw() {
      var c = C[cur], P = c.P, t = +sl.value, v = c.v;
      var G = gview({ x0: v.x0, x1: v.x1, y0: v.y0, y1: v.y1, sy: v.sy, W: 360, H: 250, pl: 34, xt: ticks(0, v.x1, v.xs) }), h = G.g + G.open, i;
      var s = val(P, t), k = s.i;
      for (i = 0; i < P.length - 1; i++) h += seg(G, P[i][0], P[i][1], P[i + 1][0], P[i + 1][1], i === k ? BL : AC, i === k ? 4 : 2.6);
      h += '<line class="gd" x1="' + f1(G.X(t)) + '" y1="' + f1(G.Y(0)) + '" x2="' + f1(G.X(t)) + '" y2="' + f1(G.Y(s.y)) + '"/>';
      h += '<line class="gd" x1="' + f1(G.X(0)) + '" y1="' + f1(G.Y(s.y)) + '" x2="' + f1(G.X(t)) + '" y2="' + f1(G.Y(s.y)) + '"/>';
      P.forEach(function (p) { h += gdot(G, p[0], p[1], AC, 3.5); });
      h += gdot(G, t, s.y, BL, 6);
      svg.innerHTML = h + G.close;
      var a = P[k], b = P[k + 1], r = (b[1] - a[1]) / (b[0] - a[0]), ph;
      if (r > 0) ph = '<strong class="sp">' + t3("Creixent", "Creciente", "Increasing") + "</strong>" + small(c.up(decS(r)));
      else if (r < 0) ph = '<strong class="sm">' + t3("Decreixent", "Decreciente", "Decreasing") + "</strong>" + small(c.dn(decS(-r)));
      else ph = "<strong>" + t3("Constant", "Constante", "Constant") + "</strong>" + small(c.eq(decS(a[1])));
      var ys = P.map(function (p) { return p[1]; }), mx = Math.max.apply(null, ys), mn = Math.min.apply(null, ys), xm = P[ys.indexOf(mx)][0];
      var plateau = P.filter(function (p) { return p[1] === mx; }).map(function (p) { return p[0]; });
      info.innerHTML = kv([
        [t3("Variables", "Variables", "Variables"), "x: " + c.xv() + " (" + c.xu + ")<br>y: " + c.yv() + " (" + c.yu + ")"],
        [t3("Punt", "Punto", "Point"), tex("x=" + dT(t, 2)) + " " + c.xu + " ⇒ " + tex("y=" + dT(s.y, 2)) + " " + c.yu],
        [t3("Tram", "Tramo", "Stretch"), tex("(" + a[0] + ",\\," + b[0] + ")") + ": " + ph],
        [t3("Domini i recorregut", "Dominio y recorrido", "Domain and range"), tex("D=[" + P[0][0] + ",\\," + P[P.length - 1][0] + "]") + ", " + tex("R=[" + mn + ",\\," + mx + "]")],
        [t3("Màxim", "Máximo", "Maximum"), plateau.length > 1 ? mx + " " + c.yu + t3(" entre ", " entre ", " between ") + plateau[0] + t3(" i ", " y ", " and ") + plateau[plateau.length - 1] + " " + c.xu : tex("(" + xm + ",\\," + mx + ")")]
      ]);
    }
    onLang(draw);
  }

  /* ---------- 6.8 construcció d'una funció a partir d'un enunciat ---------- */
  function wBuild() {
    var w = byId("w-build"); if (!w) return;
    var svg = w.querySelector("svg.tg-svg"), info = w.querySelector(".info"), cur = 0;
    var S1 = $(w, "p1"), S2 = $(w, "p2"), L2 = $(w, "g2");
    var C = [
      { name: function () { return "Taxi"; }, p: [[1, 5, .5, 3], [.5, 2, .1, 1.2]],
        lab: function () { return [t3("baixada de bandera (€)", "bajada de bandera (€)", "fixed fee (€)"), t3("preu per km (€)", "precio por km (€)", "price per km (€)")]; },
        txt: function (a, b) { return t3("Una carrera de taxi costa ", "Una carrera de taxi cuesta ", "A taxi ride costs ") + eur(a) + t3(" € fixos més ", " € fijos más ", " € fixed plus ") + eur(b) + t3(" € per cada km recorregut.", " € por cada km recorrido.", " € per km travelled."); },
        vars: function () { return [t3("x: km recorreguts", "x: km recorridos", "x: km travelled"), t3("y: preu (€)", "y: precio (€)", "y: price (€)")]; },
        f: function (a, b, x) { return a + b * x; }, xs: [0, 5, 10, 15, 20], dom: function () { return [0, 20]; },
        F: function (a, b) { return "y=" + dT(a) + "+" + dT(b) + "x"; }, D: function () { return "[0,\\,+\\infty)"; },
        note: function (a, b) { return t3("És una funció lineal: el preu puja ", "Es una función lineal: el precio sube ", "It is a linear function: the price rises ") + eur(b) + t3(" € per cada km. La gràfica és una recta que talla l'eix Y en ", " € por cada km. La gráfica es una recta que corta el eje Y en ", " € per km. Its graph is a line meeting the y-axis at ") + decS(a) + " €."; },
        view: function (a, b) { var m = a + 20 * b; return { x0: -1.5, x1: 21, y0: -m * .08, y1: m * 1.12, xs: 5 }; } },
      { name: function () { return t3("Dipòsit", "Depósito", "Tank"); }, p: [[100, 500, 50, 300], [5, 50, 5, 20]],
        lab: function () { return [t3("volum inicial (L)", "volumen inicial (L)", "initial volume (L)"), t3("es buida (L/min)", "se vacía (L/min)", "drains (L/min)")]; },
        txt: function (a, b) { return t3("Un dipòsit té ", "Un depósito tiene ", "A tank holds ") + a + t3(" L d'aigua i es buida a raó de ", " L de agua y se vacía a razón de ", " L of water and drains at ") + b + " L/min."; },
        vars: function () { return [t3("x: temps (min)", "x: tiempo (min)", "x: time (min)"), t3("y: litres que queden", "y: litros que quedan", "y: litres left")]; },
        f: function (a, b, x) { return x < -1e-9 || x > a / b + 1e-9 ? NaN : a - b * x; },
        xs: null, dom: function (a, b) { return [0, a / b]; },
        F: function (a, b) { return "y=" + a + "-" + b + "x"; }, D: function (a, b) { return "\\left[0,\\," + niceT(snap(a / b)) + "\\right]"; },
        note: function (a, b) { return t3("Es buida del tot quan ", "Se vacía del todo cuando ", "It is empty when ") + tex(a + "-" + b + "x=0\\Rightarrow x=" + niceT(snap(a / b))) + t3(" min: per això el domini acaba ací. La recta baixa (pendent negatiu).", " min: por eso el dominio acaba aquí. La recta baja (pendiente negativa).", " min, so the domain ends there. The line falls (negative slope)."); },
        view: function (a, b) { var T = a / b; return { x0: -T * .08, x1: T * 1.12, y0: -a * .08, y1: a * 1.12, xs: T > 30 ? 10 : T > 12 ? 5 : T > 6 ? 2 : 1 }; } },
      { name: function () { return t3("Rectangle", "Rectángulo", "Rectangle"); }, p: [[8, 40, 4, 20]],
        lab: function () { return [t3("perímetre (m)", "perímetro (m)", "perimeter (m)")]; },
        txt: function (a) { return t3("Amb ", "Con ", "With ") + a + t3(" m de tanca volem fer un corral rectangular. Si un costat mesura x m, l'altre mesura ", " m de valla queremos hacer un corral rectangular. Si un lado mide x m, el otro mide ", " m of fencing we make a rectangular pen. If one side is x m, the other is ") + tex(niceT(a / 2) + "-x") + " m."; },
        vars: function () { return [t3("x: un costat (m)", "x: un lado (m)", "x: one side (m)"), t3("y: àrea (m²)", "y: área (m²)", "y: area (m²)")]; },
        f: function (a, b, x) { return x <= 1e-9 || x >= a / 2 - 1e-9 ? NaN : x * (a / 2 - x); },
        xs: null, dom: function (a) { return [0, a / 2]; },
        F: function (a) { return "y=x\\,(" + niceT(a / 2) + "-x)=" + niceT(a / 2) + "x-x^2"; }, D: function (a) { return "(0,\\," + niceT(a / 2) + ")"; },
        note: function (a) { return t3("No és lineal: la gràfica és una paràbola. L'àrea màxima és ", "No es lineal: la gráfica es una parábola. El área máxima es ", "Not linear: the graph is a parabola. The largest area is ") + tex(niceT(snap(a * a / 16)) + "\\ \\text{m}^2") + t3(", quan el corral és un quadrat de costat ", ", cuando el corral es un cuadrado de lado ", ", when the pen is a square of side ") + tex(niceT(snap(a / 4))) + " m."; },
        view: function (a) { var m = a * a / 16; return { x0: -a * .04, x1: a * .56, y0: -m * .1, y1: m * 1.18, xs: a > 24 ? 4 : 2 }; } },
      { name: function () { return t3("Repartiment", "Reparto", "Sharing"); }, p: [[60, 600, 60, 120]],
        lab: function () { return [t3("premi (€)", "premio (€)", "prize (€)")]; },
        txt: function (a) { return t3("Un premi de ", "Un premio de ", "A prize of ") + a + t3(" € es reparteix a parts iguals entre x persones.", " € se reparte a partes iguales entre x personas.", " € is shared equally among x people."); },
        vars: function () { return [t3("x: nombre de persones", "x: número de personas", "x: number of people"), t3("y: € per persona", "y: € por persona", "y: € per person")]; },
        f: function (a, b, x) { return a / x; }, xs: [1, 2, 3, 4, 5, 6], disc: true, dom: function () { return [1, 10]; },
        F: function (a) { return "y=\\dfrac{" + a + "}{x}"; }, D: function () { return "\\{1,\\,2,\\,3,\\,4,\\,\\ldots\\}"; },
        note: function () { return t3("Proporcionalitat inversa: si el nombre de persones es duplica, cadascú en rep la meitat. Com que x només pot ser un nombre natural, els punts <strong>no s'uneixen</strong>.", "Proporcionalidad inversa: si el número de personas se duplica, cada uno recibe la mitad. Como x solo puede ser un número natural, los puntos <strong>no se unen</strong>.", "Inverse proportion: doubling the number of people halves each share. Since x can only be a whole number, the points are <strong>not joined</strong>."); },
        view: function (a) { return { x0: -.6, x1: 10.8, y0: -a * .08, y1: a * 1.12, xs: 1 }; } }
    ];
    presetBtns($(w, "pre"), function () { return C.map(function (c) { return c.name(); }); }, function (i) {
      cur = i; var c = C[i];
      [S1, S2].forEach(function (S, k) { var p = c.p[k]; if (!p) return; S.min = p[0]; S.max = p[1]; S.step = p[2]; S.value = p[3]; });
      L2.style.display = c.p[1] ? "" : "none"; draw();
    }, 0);
    S1.addEventListener("input", draw); S2.addEventListener("input", draw);
    function eur(v) { var t = v.toFixed(2); return lang === "en" ? t : t.replace(".", ","); }
    function niceStep(m) { var e = Math.pow(10, Math.floor(Math.log10(m / 4))), r = m / 4 / e; return (r < 1.5 ? 1 : r < 3.5 ? 2 : r < 7.5 ? 5 : 10) * e; }
    function draw() {
      var c = C[cur], a = +S1.value, b = c.p[1] ? +S2.value : 0, labs = c.lab();
      $(w, "l1").innerHTML = labs[0]; $(w, "v1").innerHTML = decS(a); if (c.p[1]) { $(w, "l2").innerHTML = labs[1]; $(w, "v2").innerHTML = decS(b); }
      var v = c.view(a, b), sy = niceStep(v.y1), G = gview({ x0: v.x0, x1: v.x1, y0: v.y0, y1: v.y1, sy: sy, W: 360, H: 250, pl: 36, xt: ticks(0, v.x1, v.xs) }), h = G.g + G.open;
      var d = c.dom(a, b), f = function (x) { return c.f(a, b, x); };
      var xs = c.xs || [0, 1, 2, 3, 4].map(function (k) { return snap(d[0] + (d[1] - d[0]) * k / 4); });
      if (cur === 2) xs = [1, 2, 3, 4].map(function (k) { return snap(a / 2 * k / 5); });
      if (c.disc) { for (var n = 1; n <= 10; n++) h += gdot(G, n, f(n), AC, 4.5); }
      else {
        h += curve(G, f, AC, { a: d[0], b: d[1], n: 400 });
        if (cur === 0) h += gdot(G, 0, a, AC, 4.5);
        if (cur === 1) h += gdot(G, 0, a, AC, 4.5) + gdot(G, d[1], 0, AC, 4.5);
        if (cur === 2) h += odot(G, 0, 0, AC) + odot(G, a / 2, 0, AC) + gdot(G, a / 4, a * a / 16, GR, 5.5);
      }
      xs.forEach(function (x) { var y = f(x); if (isFinite(y)) h += gdot(G, x, y, BL, 4); });
      svg.innerHTML = h + G.close;
      var tb = '<div class="tbl-wrap"><table class="data tr"><tr><th>x</th>' + xs.map(function (x) { return "<td>" + decS(x) + "</td>"; }).join("") + "</tr><tr><th>y</th>" +
        xs.map(function (x) { var y = f(x); return "<td>" + (isFinite(y) ? decS(y) : "—") + "</td>"; }).join("") + "</tr></table></div>";
      var vv = c.vars();
      info.innerHTML = kv([
        [t3("Enunciat", "Enunciado", "Problem"), c.txt(a, b)],
        [t3("Variables", "Variables", "Variables"), vv[0] + "<br>" + vv[1]],
        [t3("Taula", "Tabla", "Table"), tb],
        [t3("Fórmula", "Fórmula", "Formula"), "<strong>" + tex(c.F(a, b)) + "</strong>"],
        [t3("Domini", "Dominio", "Domain"), tex(c.D(a, b))],
        [t3("Observa", "Observa", "Notice"), c.note(a, b)]
      ]);
    }
    onLang(draw);
  }
