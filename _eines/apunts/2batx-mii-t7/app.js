(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2batx-mii-u7-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt",
      der: "derivable", nder: "no derivable", ang: "punt anguló", vt: "tangent vertical", cusp: "punt de retrocés", ncont: "no contínua",
      bad: "No entenc l'expressió: revisa-la.", aBad: "Escriu un nombre per al punt.", noDiff: "Aquesta expressió no la sé derivar amb les regles de la unitat.",
      sum: "Derivada d'una suma o resta: derivem terme a terme.", kf: "Constant per una funció: la constant es queda multiplicant.", fk: "Funció dividida per una constant: derivem el numerador.",
      prod: "Derivada d'un producte:", quo: "Derivada d'un quocient:", powx: "Derivada d'una potència de x:", neg: "Canvi de signe:", cst: "És una constant: la derivada és 0.",
      chain: "Funció composta: regla de la cadena.", outer: "funció de fora", inner: "funció de dins", elem: "Derivada d'una funció elemental (taula):", res: "Resultat",
      logd: "Derivació logarítmica: hi ha x a la base i a l'exponent.",
      tline: "Recta tangent", nline: "Recta normal", noF: "La funció no està definida en aquest punt.", noD: "La funció no és derivable en aquest punt.",
      horT: "La tangent és horitzontal i la normal és vertical:", onC: "El punt és de la corba: només hi ha la tangent en aquest punt.", tFrom: "Tangents que passen per",
      genT: "Tangent en un punt genèric \\((a,f(a))\\): \\(y-f(a)=f'(a)(x-a)\\). Imposem que passe pel punt i resolem l'equació en \\(a\\):", noTan: "Cap recta tangent a la gràfica (en la finestra) passa per aquest punt.", tAt: "Punt de tangència",
      hopT: "Indeterminació: apliquem L'Hôpital (derivem el numerador i el denominador per separat).", notInd: "Ja no és indeterminat:", simpl: "Simplifiquem:",
      osc: "El límit del quocient de les derivades no existeix: la regla de L'Hôpital no hi diu res. Cal un altre camí.", many: "Després de 5 aplicacions encara és indeterminat: convé simplificar abans o usar infinitèsims.",
      check: "Comprovació numèrica", aErr: "Punt: un nombre, inf o -inf. Per a un límit lateral, afig + o − al final (0+).", sideDiff: "Els límits laterals són diferents: el límit no existeix.", hopRes: "Resultat",
      type: "Tipus", trans: "Transformació", logT: "Prenem logaritmes: si \\(L=\\lim f^{\\,g}\\), aleshores \\(\\ln L=\\lim g\\cdot\\ln f\\).", backE: "Desfem el logaritme:",
      test: "Prova", incOn: "Creixent en", decOn: "Decreixent en", noCrit: "No té punts crítics.", maxR: "Màxim relatiu", minR: "Mínim relatiu", noExt: "no és extrem (la derivada no canvia de signe)",
      mx: "màx.", mn: "mín.", noDom: "fora del domini", crit: "Punts crítics", d2t: "Segona derivada en el punt", ndPt: "\\(f\\) no hi és derivable",
      cvx: "Convexa \\(\\cup\\) en", ccv: "Còncava \\(\\cap\\) en", infl: "Punt d'inflexió", noInfl: "No té punts d'inflexió.", ip: "P.I.", noInf: "no és d'inflexió (no canvia la curvatura)",
      tanAt: "Tangent en", above: "la corba queda per damunt de la tangent", below: "la corba queda per davall de la tangent", cross: "la tangent travessa la corba",
      fVals: "Valors en el punt", kindPt: "Conclusió",
      hyp: "Hipòtesis", hypC: "\\(f\\) contínua en \\([a,b]\\)", hypD: "\\(f\\) derivable en \\((a,b)\\)", hypE: "\\(f(a)=f(b)\\)", thR: "Tesi: existeix \\(c\\in(a,b)\\) amb \\(f'(c)=0\\)",
      thL: "Tesi: existeix \\(c\\in(a,b)\\) amb \\(f'(c)=\\dfrac{f(b)-f(a)}{b-a}\\)", cFound: "Valors de \\(c\\)", hypFail: "No es compleixen totes les hipòtesis: el teorema no assegura res.", noC: "No hi ha cap \\(c\\) a l'interval.",
      ivBad: "Escriu un interval amb a < b.", rolleM: "Rolle", lagM: "Valor mitjà", slope: "pendent de la secant",
      cand: "Candidats", ends: "extrem de l'interval", critIn: "punt crític", ndIn: "punt no derivable", absMax: "Màxim absolut", absMin: "Mínim absolut", value: "Valor",
      found: "Has trobat", optMax: "el màxim:", optMin: "el mínim:", show: "Mostra l'òptim",
      sNames: ["Domini", "Simetria i periodicitat", "Talls amb els eixos", "Asímptotes", "Monotonia i extrems", "Curvatura i inflexió", "Gràfica"],
      even: "Funció parella: simètrica respecte de l'eix OY", odd: "Funció senar: simètrica respecte de l'origen", noSym: "No és parella ni senar", symNoDom: "el domini no és simètric",
      per: "És periòdica de període", notPer: "No és periòdica.", perStudy: "Com que és periòdica, l'estudiem en un període:", cutX: "Eix OX", cutY: "Eix OY", noCutX: "no talla l'eix OX", noCutY: "no talla l'eix OY (0 no és del domini)",
      av: "Asímptotes verticals", noAV: "no en té", ah: "asímptota horitzontal", ao: "asímptota obliqua", noAsy: "no té asímptota horitzontal ni obliqua", branch: "branca parabòlica",
      notTo: "la funció no hi arriba (el domini està fitat per aquest costat)", toL: "quan x → −∞", toR: "quan x → +∞", poly: "Els polinomis no tenen asímptotes.", perAsy: "Com que és periòdica, no té asímptotes horitzontals ni obliqües.",
      den: "Denominador", denZ: "s'anul·la en", denNo: "no s'anul·la mai", lnArg: "Argument del logaritme", lnPos: "ha de ser positiu", sqArg: "Radicand", sqPos: "ha de ser ≥ 0", tanArg: "La tangent no existeix on", noCond: "Cap restricció.", empty: "El domini és buit.",
      andK: "amb \\(k\\in\\mathbb Z\\)", inPer: "en un període",
      pTn: ["x³ − 3x", "√(x² + 5)", "e^(2x)", "ln(x² − 3)", "sin x + cos x", "(2x²+2x−2)/(3x²+3)"], pTp: ["x² des de (1, −3)", "x²/4+4x+4 des de (0, 0)", "x³ des de (2, 0)", "eˣ des de (0, 0)", "1/x des de (0, 1)"],
      pHop: ["(eˣ−1−x)/x²", "(x − sin x)/x³", "ln x / x", "x²/eˣ", "(tan x − x)/(x − sin x)", "PAU Castella-la Manxa", "PAU Castella i Lleó", "(x + sin x)/x"],
      pInd: ["0·∞: x ln x", "∞·0: x(e^(1/x)−1)", "∞−∞: 1/x − 1/(eˣ−1)", "∞−∞: 1/ln x − 1/(x−1)", "1^∞: (1+x−sin x)^(1/x³)", "1^∞: (eˣ+x³)^(1/x)", "∞⁰: x^(1/x)", "0⁰: x^x", "0⁰: x^(sin x)"],
      pMono: ["x³ − 3x", "x e^(1−x²)", "x/ln x", "(x+1)/(x²+1)", "x + 2 cos x", "|x² − 4|", "x^(2/3)(x−5)"], pCurv: ["x³ − 3x²", "eˣ(x²−5x+6)", "x − ln(x²+1)", "(x−1)²/x²", "x + sin x", "∛x", "x⁴"],
      pChk: ["x³ − 3x² + 2 en 0", "x³ − 3x² + 2 en 1", "x³ en 0", "x⁴ en 0", "x⁵ − 5x⁴ en 4"],
      pRolle: ["x² − 4x + 3 en [0, 4]", "x³ − x en [−1, 1]", "1 − ∛x² en [−1, 1]", "(1 − x²)·tan x en [0, 1]", "x³ en [0, 2]", "ln x en [1, e]", "√(1 − x²) en [0, 1]", "x ln(x²+1) en [1, 2]"],
      pAbs: ["PAU València 2026", "PAU Madrid 2025", "PAU Astúries 2025", "PAU Múrcia 2018", "x eˣ en [−3, 1]", "sin x + cos x en [0, 2π]"],
      pOpt: ["Finestra (València 2023)", "Porta (València 2023)", "Caixa (València 2024)", "Espill (València 2021)", "Cables (València 2017)", "Triatló (Múrcia 2022)", "Rectangle en un triangle (València 2020)"],
      pR1: ["x⁴ − 2x²", "x³/(1 − x²)", "(x+1)/(x²+1)", "x³/(1+x)²", "(x²+3)/(x²−4)"], pR2: ["x/√(x² − 1)", "x e^(−2x²)", "2 ln x / x", "x²e^(−x)", "√(x² − 4x)"], pR3: ["2 sin x + sin 2x", "x + sin x", "cos(πx/9) + 2", "sin² x", "tan x", "e^(sin x)"],
      pLab: ["x³ − 3x", "x²/(x−2)", "x e^(−x²)", "ln(x)/x", "√(x² − 1)", "x + 2 cos x", "|x² − 4|"] },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba",
      der: "derivable", nder: "no derivable", ang: "punto anguloso", vt: "tangente vertical", cusp: "punto de retroceso", ncont: "no continua",
      bad: "No entiendo la expresión: revísala.", aBad: "Escribe un número para el punto.", noDiff: "Esta expresión no la sé derivar con las reglas de la unidad.",
      sum: "Derivada de una suma o resta: derivamos término a término.", kf: "Constante por una función: la constante se queda multiplicando.", fk: "Función dividida por una constante: derivamos el numerador.",
      prod: "Derivada de un producto:", quo: "Derivada de un cociente:", powx: "Derivada de una potencia de x:", neg: "Cambio de signo:", cst: "Es una constante: la derivada es 0.",
      chain: "Función compuesta: regla de la cadena.", outer: "función de fuera", inner: "función de dentro", elem: "Derivada de una función elemental (tabla):", res: "Resultado",
      logd: "Derivación logarítmica: hay x en la base y en el exponente.",
      tline: "Recta tangente", nline: "Recta normal", noF: "La función no está definida en este punto.", noD: "La función no es derivable en este punto.",
      horT: "La tangente es horizontal y la normal es vertical:", onC: "El punto es de la curva: solo está la tangente en este punto.", tFrom: "Tangentes que pasan por",
      genT: "Tangente en un punto genérico \\((a,f(a))\\): \\(y-f(a)=f'(a)(x-a)\\). Imponemos que pase por el punto y resolvemos la ecuación en \\(a\\):", noTan: "Ninguna recta tangente a la gráfica (en la ventana) pasa por este punto.", tAt: "Punto de tangencia",
      hopT: "Indeterminación: aplicamos L'Hôpital (derivamos el numerador y el denominador por separado).", notInd: "Ya no es indeterminado:", simpl: "Simplificamos:",
      osc: "El límite del cociente de las derivadas no existe: la regla de L'Hôpital no dice nada. Hay que buscar otro camino.", many: "Después de 5 aplicaciones sigue siendo indeterminado: conviene simplificar antes o usar infinitésimos.",
      check: "Comprobación numérica", aErr: "Punto: un número, inf o -inf. Para un límite lateral, añade + o − al final (0+).", sideDiff: "Los límites laterales son distintos: el límite no existe.", hopRes: "Resultado",
      type: "Tipo", trans: "Transformación", logT: "Tomamos logaritmos: si \\(L=\\lim f^{\\,g}\\), entonces \\(\\ln L=\\lim g\\cdot\\ln f\\).", backE: "Deshacemos el logaritmo:",
      test: "Prueba", incOn: "Creciente en", decOn: "Decreciente en", noCrit: "No tiene puntos críticos.", maxR: "Máximo relativo", minR: "Mínimo relativo", noExt: "no es extremo (la derivada no cambia de signo)",
      mx: "máx.", mn: "mín.", noDom: "fuera del dominio", crit: "Puntos críticos", d2t: "Segunda derivada en el punto", ndPt: "\\(f\\) no es derivable",
      cvx: "Convexa \\(\\cup\\) en", ccv: "Cóncava \\(\\cap\\) en", infl: "Punto de inflexión", noInfl: "No tiene puntos de inflexión.", ip: "P.I.", noInf: "no es de inflexión (no cambia la curvatura)",
      tanAt: "Tangente en", above: "la curva queda por encima de la tangente", below: "la curva queda por debajo de la tangente", cross: "la tangente atraviesa la curva",
      fVals: "Valores en el punto", kindPt: "Conclusión",
      hyp: "Hipótesis", hypC: "\\(f\\) continua en \\([a,b]\\)", hypD: "\\(f\\) derivable en \\((a,b)\\)", hypE: "\\(f(a)=f(b)\\)", thR: "Tesis: existe \\(c\\in(a,b)\\) con \\(f'(c)=0\\)",
      thL: "Tesis: existe \\(c\\in(a,b)\\) con \\(f'(c)=\\dfrac{f(b)-f(a)}{b-a}\\)", cFound: "Valores de \\(c\\)", hypFail: "No se cumplen todas las hipótesis: el teorema no asegura nada.", noC: "No hay ningún \\(c\\) en el intervalo.",
      ivBad: "Escribe un intervalo con a < b.", rolleM: "Rolle", lagM: "Valor medio", slope: "pendiente de la secante",
      cand: "Candidatos", ends: "extremo del intervalo", critIn: "punto crítico", ndIn: "punto no derivable", absMax: "Máximo absoluto", absMin: "Mínimo absoluto", value: "Valor",
      found: "Has encontrado", optMax: "el máximo:", optMin: "el mínimo:", show: "Mostrar el óptimo",
      sNames: ["Dominio", "Simetría y periodicidad", "Cortes con los ejes", "Asíntotas", "Monotonía y extremos", "Curvatura e inflexión", "Gráfica"],
      even: "Función par: simétrica respecto del eje OY", odd: "Función impar: simétrica respecto del origen", noSym: "No es par ni impar", symNoDom: "el dominio no es simétrico",
      per: "Es periódica de periodo", notPer: "No es periódica.", perStudy: "Como es periódica, la estudiamos en un periodo:", cutX: "Eje OX", cutY: "Eje OY", noCutX: "no corta el eje OX", noCutY: "no corta el eje OY (0 no es del dominio)",
      av: "Asíntotas verticales", noAV: "no tiene", ah: "asíntota horizontal", ao: "asíntota oblicua", noAsy: "no tiene asíntota horizontal ni oblicua", branch: "rama parabólica",
      notTo: "la función no llega (el dominio está acotado por este lado)", toL: "cuando x → −∞", toR: "cuando x → +∞", poly: "Los polinomios no tienen asíntotas.", perAsy: "Como es periódica, no tiene asíntotas horizontales ni oblicuas.",
      den: "Denominador", denZ: "se anula en", denNo: "no se anula nunca", lnArg: "Argumento del logaritmo", lnPos: "debe ser positivo", sqArg: "Radicando", sqPos: "debe ser ≥ 0", tanArg: "La tangente no existe donde", noCond: "Ninguna restricción.", empty: "El dominio es vacío.",
      andK: "con \\(k\\in\\mathbb Z\\)", inPer: "en un periodo",
      pTn: ["x³ − 3x", "√(x² + 5)", "e^(2x)", "ln(x² − 3)", "sen x + cos x", "(2x²+2x−2)/(3x²+3)"], pTp: ["x² desde (1, −3)", "x²/4+4x+4 desde (0, 0)", "x³ desde (2, 0)", "eˣ desde (0, 0)", "1/x desde (0, 1)"],
      pHop: ["(eˣ−1−x)/x²", "(x − sen x)/x³", "ln x / x", "x²/eˣ", "(tg x − x)/(x − sen x)", "PAU Castilla-La Mancha", "PAU Castilla y León", "(x + sen x)/x"],
      pInd: ["0·∞: x ln x", "∞·0: x(e^(1/x)−1)", "∞−∞: 1/x − 1/(eˣ−1)", "∞−∞: 1/ln x − 1/(x−1)", "1^∞: (1+x−sen x)^(1/x³)", "1^∞: (eˣ+x³)^(1/x)", "∞⁰: x^(1/x)", "0⁰: x^x", "0⁰: x^(sen x)"],
      pMono: ["x³ − 3x", "x e^(1−x²)", "x/ln x", "(x+1)/(x²+1)", "x + 2 cos x", "|x² − 4|", "x^(2/3)(x−5)"], pCurv: ["x³ − 3x²", "eˣ(x²−5x+6)", "x − ln(x²+1)", "(x−1)²/x²", "x + sen x", "∛x", "x⁴"],
      pChk: ["x³ − 3x² + 2 en 0", "x³ − 3x² + 2 en 1", "x³ en 0", "x⁴ en 0", "x⁵ − 5x⁴ en 4"],
      pRolle: ["x² − 4x + 3 en [0, 4]", "x³ − x en [−1, 1]", "1 − ∛x² en [−1, 1]", "(1 − x²)·tg x en [0, 1]", "x³ en [0, 2]", "ln x en [1, e]", "√(1 − x²) en [0, 1]", "x ln(x²+1) en [1, 2]"],
      pAbs: ["PAU Valencia 2026", "PAU Madrid 2025", "PAU Asturias 2025", "PAU Murcia 2018", "x eˣ en [−3, 1]", "sen x + cos x en [0, 2π]"],
      pOpt: ["Ventana (Valencia 2023)", "Puerta (Valencia 2023)", "Caja (Valencia 2024)", "Espejo (Valencia 2021)", "Cables (Valencia 2017)", "Triatlón (Murcia 2022)", "Rectángulo en un triángulo (Valencia 2020)"],
      pR1: ["x⁴ − 2x²", "x³/(1 − x²)", "(x+1)/(x²+1)", "x³/(1+x)²", "(x²+3)/(x²−4)"], pR2: ["x/√(x² − 1)", "x e^(−2x²)", "2 ln x / x", "x²e^(−x)", "√(x² − 4x)"], pR3: ["2 sen x + sen 2x", "x + sen x", "cos(πx/9) + 2", "sen² x", "tg x", "e^(sen x)"],
      pLab: ["x³ − 3x", "x²/(x−2)", "x e^(−x²)", "ln(x)/x", "√(x² − 1)", "x + 2 cos x", "|x² − 4|"] },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top",
      der: "differentiable", nder: "not differentiable", ang: "corner point", vt: "vertical tangent", cusp: "cusp", ncont: "not continuous",
      bad: "I can't read that expression: check it.", aBad: "Type a number for the point.", noDiff: "I can't differentiate this with the rules of the unit.",
      sum: "Derivative of a sum or difference: differentiate term by term.", kf: "Constant times a function: the constant stays as a factor.", fk: "Function divided by a constant: differentiate the numerator.",
      prod: "Product rule:", quo: "Quotient rule:", powx: "Power rule:", neg: "Change of sign:", cst: "It is a constant: the derivative is 0.",
      chain: "Composite function: chain rule.", outer: "outer function", inner: "inner function", elem: "Derivative of an elementary function (table):", res: "Result",
      logd: "Logarithmic differentiation: x appears in both the base and the exponent.",
      tline: "Tangent line", nline: "Normal line", noF: "The function is not defined at this point.", noD: "The function is not differentiable at this point.",
      horT: "The tangent is horizontal and the normal is vertical:", onC: "The point lies on the curve: there is only the tangent at that point.", tFrom: "Tangents through",
      genT: "Tangent at a generic point \\((a,f(a))\\): \\(y-f(a)=f'(a)(x-a)\\). Make it pass through the point and solve the equation for \\(a\\):", noTan: "No tangent line to the graph (in the window) passes through this point.", tAt: "Point of tangency",
      hopT: "Indeterminate form: apply L'Hôpital's rule (differentiate the numerator and the denominator separately).", notInd: "No longer indeterminate:", simpl: "Simplify:",
      osc: "The limit of the quotient of the derivatives does not exist: L'Hôpital's rule says nothing here. We need another method.", many: "After 5 applications it is still indeterminate: simplify first or use equivalent infinitesimals.",
      check: "Numerical check", aErr: "Point: a number, inf or -inf. For a one-sided limit, add + or − at the end (0+).", sideDiff: "The one-sided limits are different: the limit does not exist.", hopRes: "Result",
      type: "Type", trans: "Rewrite", logT: "Take logarithms: if \\(L=\\lim f^{\\,g}\\), then \\(\\ln L=\\lim g\\cdot\\ln f\\).", backE: "Undo the logarithm:",
      test: "Test", incOn: "Increasing on", decOn: "Decreasing on", noCrit: "It has no critical points.", maxR: "Relative maximum", minR: "Relative minimum", noExt: "is not an extremum (the derivative does not change sign)",
      mx: "max", mn: "min", noDom: "outside the domain", crit: "Critical points", d2t: "Second derivative at the point", ndPt: "\\(f\\) is not differentiable there",
      cvx: "Convex \\(\\cup\\) on", ccv: "Concave \\(\\cap\\) on", infl: "Inflection point", noInfl: "It has no inflection points.", ip: "I.P.", noInf: "is not an inflection point (the concavity does not change)",
      tanAt: "Tangent at", above: "the curve lies above the tangent", below: "the curve lies below the tangent", cross: "the tangent crosses the curve",
      fVals: "Values at the point", kindPt: "Conclusion",
      hyp: "Hypotheses", hypC: "\\(f\\) continuous on \\([a,b]\\)", hypD: "\\(f\\) differentiable on \\((a,b)\\)", hypE: "\\(f(a)=f(b)\\)", thR: "Conclusion: there is \\(c\\in(a,b)\\) with \\(f'(c)=0\\)",
      thL: "Conclusion: there is \\(c\\in(a,b)\\) with \\(f'(c)=\\dfrac{f(b)-f(a)}{b-a}\\)", cFound: "Values of \\(c\\)", hypFail: "Not all the hypotheses hold: the theorem guarantees nothing.", noC: "There is no \\(c\\) in the interval.",
      ivBad: "Type an interval with a < b.", rolleM: "Rolle", lagM: "Mean value", slope: "slope of the secant",
      cand: "Candidates", ends: "endpoint", critIn: "critical point", ndIn: "non-differentiable point", absMax: "Absolute maximum", absMin: "Absolute minimum", value: "Value",
      found: "You found", optMax: "the maximum:", optMin: "the minimum:", show: "Show the optimum",
      sNames: ["Domain", "Symmetry and periodicity", "Intercepts", "Asymptotes", "Monotonicity and extrema", "Concavity and inflection", "Graph"],
      even: "Even function: symmetric about the y-axis", odd: "Odd function: symmetric about the origin", noSym: "Neither even nor odd", symNoDom: "the domain is not symmetric",
      per: "It is periodic with period", notPer: "It is not periodic.", perStudy: "Since it is periodic, we study it over one period:", cutX: "x-axis", cutY: "y-axis", noCutX: "it does not cross the x-axis", noCutY: "it does not cross the y-axis (0 is not in the domain)",
      av: "Vertical asymptotes", noAV: "none", ah: "horizontal asymptote", ao: "oblique asymptote", noAsy: "no horizontal or oblique asymptote", branch: "parabolic branch",
      notTo: "the function does not get there (the domain is bounded on this side)", toL: "as x → −∞", toR: "as x → +∞", poly: "Polynomials have no asymptotes.", perAsy: "Since it is periodic, it has no horizontal or oblique asymptotes.",
      den: "Denominator", denZ: "vanishes at", denNo: "never vanishes", lnArg: "Argument of the logarithm", lnPos: "must be positive", sqArg: "Radicand", sqPos: "must be ≥ 0", tanArg: "The tangent does not exist where", noCond: "No restrictions.", empty: "The domain is empty.",
      andK: "with \\(k\\in\\mathbb Z\\)", inPer: "over one period",
      pTn: ["x³ − 3x", "√(x² + 5)", "e^(2x)", "ln(x² − 3)", "sin x + cos x", "(2x²+2x−2)/(3x²+3)"], pTp: ["x² from (1, −3)", "x²/4+4x+4 from (0, 0)", "x³ from (2, 0)", "eˣ from (0, 0)", "1/x from (0, 1)"],
      pHop: ["(eˣ−1−x)/x²", "(x − sin x)/x³", "ln x / x", "x²/eˣ", "(tan x − x)/(x − sin x)", "PAU Castile-La Mancha", "PAU Castile and León", "(x + sin x)/x"],
      pInd: ["0·∞: x ln x", "∞·0: x(e^(1/x)−1)", "∞−∞: 1/x − 1/(eˣ−1)", "∞−∞: 1/ln x − 1/(x−1)", "1^∞: (1+x−sin x)^(1/x³)", "1^∞: (eˣ+x³)^(1/x)", "∞⁰: x^(1/x)", "0⁰: x^x", "0⁰: x^(sin x)"],
      pMono: ["x³ − 3x", "x e^(1−x²)", "x/ln x", "(x+1)/(x²+1)", "x + 2 cos x", "|x² − 4|", "x^(2/3)(x−5)"], pCurv: ["x³ − 3x²", "eˣ(x²−5x+6)", "x − ln(x²+1)", "(x−1)²/x²", "x + sin x", "∛x", "x⁴"],
      pChk: ["x³ − 3x² + 2 at 0", "x³ − 3x² + 2 at 1", "x³ at 0", "x⁴ at 0", "x⁵ − 5x⁴ at 4"],
      pRolle: ["x² − 4x + 3 on [0, 4]", "x³ − x on [−1, 1]", "1 − ∛x² on [−1, 1]", "(1 − x²)·tan x on [0, 1]", "x³ on [0, 2]", "ln x on [1, e]", "√(1 − x²) on [0, 1]", "x ln(x²+1) on [1, 2]"],
      pAbs: ["PAU Valencia 2026", "PAU Madrid 2025", "PAU Asturias 2025", "PAU Murcia 2018", "x eˣ on [−3, 1]", "sin x + cos x on [0, 2π]"],
      pOpt: ["Window (Valencia 2023)", "Door (Valencia 2023)", "Box (Valencia 2024)", "Mirror (Valencia 2021)", "Cables (Valencia 2017)", "Triathlon (Murcia 2022)", "Rectangle in a triangle (Valencia 2020)"],
      pR1: ["x⁴ − 2x²", "x³/(1 − x²)", "(x+1)/(x²+1)", "x³/(1+x)²", "(x²+3)/(x²−4)"], pR2: ["x/√(x² − 1)", "x e^(−2x²)", "2 ln x / x", "x²e^(−x)", "√(x² − 4x)"], pR3: ["2 sin x + sin 2x", "x + sin x", "cos(πx/9) + 2", "sin² x", "tan x", "e^(sin x)"],
      pLab: ["x³ − 3x", "x²/(x−2)", "x e^(−x²)", "ln(x)/x", "√(x² − 1)", "x + 2 cos x", "|x² − 4|"] }
  };
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
  /* ---------- nombres i rectes ---------- */
  function F(s) { return compile(parse(s)); }
  var RATIO = (H - MT - MB) / (W - ML - MR); // per a vistes amb la mateixa escala en els dos eixos
  function sgn(v) { return v > 0 ? 1 : v < 0 ? -1 : 0; }
  function snap(x) {
    if (Math.abs(x) < 1e-9) return 0;
    var q = fracOf(x, 12); if (q) return q.n / q.d;
    var k = x / Math.PI * 12, r = Math.round(k);
    return Math.abs(k - r) < 1e-7 ? r * Math.PI / 12 : x;
  }
  function gcdI(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; }
  // a + b√c (a, b racionals senzills): com les arrels de les equacions de segon grau
  var QC = [2, 3, 5, 6, 7, 10, 11, 13, 15, 17, 21];
  function quadTex(v) {
    for (var i = 0; i < QC.length; i++) {
      var c = QC[i], s = Math.sqrt(c);
      for (var d = 1; d <= 6; d++) for (var m = 1; m <= 12; m++) for (var sg = 1; sg >= -1; sg -= 2) {
        var bn = sg * m; if (gcdI(bn, d) !== 1) continue;
        var A = fracOf(v - bn / d * s, 12);
        if (!A || Math.abs(A.val() + bn / d * s - v) > 1e-9 * (1 + Math.abs(v))) continue;
        var den = A.d * d / gcdI(A.d, d), an = A.n * den / A.d, bb = bn * den / d;
        var sq = (Math.abs(bb) === 1 ? "" : Math.abs(bb)) + "\\sqrt{" + c + "}";
        var top = (an ? an + (bb > 0 ? "+" : "-") : (bb > 0 ? "" : "-")) + sq;
        return den === 1 ? top : (an === 0 && bb < 0 ? "-\\frac{" + sq + "}{" + den + "}" : "\\frac{" + top + "}{" + den + "}");
      }
    }
    return null;
  }
  // valor exacte si és senzill (fraccions, π, √, e, ln); si no, arrodonit
  function nn(v) {
    if (!isFinite(v)) return numTex(v);
    if (Math.abs(v) < 1e-12) return "0";
    var p = piTex(v); if (p.indexOf("\\pi") >= 0) return p;
    var s = niceTex(v); if (s.indexOf("\\approx") !== 0) return s;
    var q = fracOf(Math.exp(v), 12); if (q && q.n > 0 && !(q.n === 1 && q.d === 1)) return "\\ln" + (q.d === 1 ? " " + q.n : "\\frac{" + q.n + "}{" + q.d + "}");
    q = quadTex(v); if (q) return q;
    return numTex(+v.toFixed(4));
  }
  function nnA(v) { var s = nn(v); return /[\\]/.test(s) && !/^-?\d+$/.test(s) && s.indexOf("\\approx") < 0 && Math.abs(v) > 1e-9 && !/^-?\\frac\{\d+\}\{\d+\}$/.test(s) ? s + "\\approx" + numTex(+v.toFixed(3)) : s; }
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
  // derivades simbòliques i, si no es pot (valor absolut), numèriques
  function numD(g, h) { h = h || 1e-6; return function (x) { var a = g(x - h), b = g(x + h); return isFinite(a) && isFinite(b) ? (b - a) / (2 * h) : NaN; }; }
  function numD2(g) { var h = 1e-3; return function (x) { var a = g(x - h), b = g(x), c = g(x + h); return isFinite(a) && isFinite(b) && isFinite(c) ? (a - 2 * b + c) / (h * h) : NaN; }; }
  function derivs(n) {
    var R = { f: compile(n), dn: null, d2n: null };
    try { R.dn = D(n); R.df = compile(R.dn); } catch (e) { if (!(e instanceof NoDiff)) throw e; R.df = numD(R.f); }
    try { if (R.dn) { R.d2n = D(R.dn); R.d2 = compile(R.d2n); } else R.d2 = numD2(R.f); } catch (e) { if (!(e instanceof NoDiff)) throw e; R.d2 = numD2(R.f); }
    return R;
  }

  /* ---------- arrels, punts crítics i taules de signes (numèricament) ---------- */
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
      if (a === 0) { var l0 = i > 0 ? gs[i - 1] : NaN, r0 = gs[i + 1]; if ((l0 !== 0 && r0 !== 0) || l0 * r0 < 0) push(xs[i]); continue; }
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
  // ev: punts on g = 0 ("z"), on f o g no existeixen ("h") o on comença o acaba el domini ("e"); seg: signe de g entre ells
  function crit(f, g, x0, x1, opt) {
    opt = opt || {};
    var N = 6000, h = (x1 - x0) / N, ev = [], X = [], OK = [], i, it, m;
    function ok(x) { return isFinite(f(x)) && isFinite(g(x)); }
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
      var d1 = g(p), d2 = g(q), s1 = sgn(d1), s2 = sgn(d2), fp = f(p), dv = f(q) - fp, a, b;
      if (!opt.noJump && s1 === s2 && s1 !== 0 && dv * s1 < 0 && Math.abs(dv) > 1e-9 * (1 + Math.abs(fp))) {
        // f' no canvia de signe però f «salta» en sentit contrari: hi ha una asímptota entremig
        a = p; b = q;
        for (it = 0; it < 60; it++) { m = (a + b) / 2; var fm = f(m); if (!isFinite(fm)) { a = b = m; break; } if ((fm - f(a)) * s1 < 0) b = m; else a = m; }
        add((a + b) / 2, "h");
      } else if (s1 * s2 < 0) {
        a = p; b = q; var ga = d1;
        for (it = 0; it < 80; it++) { m = (a + b) / 2; var gm = g(m); if (!isFinite(gm)) break; if (sgn(gm) === sgn(ga)) { a = m; ga = gm; } else b = m; }
        var r = (a + b) / 2;
        if (!(Math.abs(g(r)) < 1e-6 * (1 + Math.abs(d1) + Math.abs(d2)))) add(r, "h");
      }
    }
    var tol = 1e-9 * (1 + Math.abs(x0) + Math.abs(x1));
    roots(g, x0, x1, N).forEach(function (r) { if (isFinite(f(r)) && r > x0 + tol && r < x1 - tol) add(r, "z"); });
    (opt.extra || []).forEach(function (r) { if (r > x0 && r < x1) add(r, "h"); });
    ev.sort(function (p, q) { return p.x - q.x; });
    var bs = [x0].concat(ev.map(function (e) { return e.x; })).concat([x1]), seg = [];
    for (i = 0; i + 1 < bs.length; i++) {
      var A = bs[i], Bb = bs[i + 1], t = null;
      [0.5, 0.25, 0.75, 0.1, 0.9].some(function (k) { var x = A + (Bb - A) * k; if (ok(x) && g(x) !== 0) { t = x; return true; } return false; });
      seg.push({ a: A, b: Bb, s: t === null ? 0 : sgn(g(t)), t: t });
    }
    return { ev: ev, seg: seg };
  }
  // f té una punxa en x? (derivades laterals numèriques diferents)
  function kink(f, x) { var hh = 1e-4, fx = f(x), dl = (fx - f(x - hh)) / hh, dr = (f(x + hh) - fx) / hh; return isFinite(dl) && isFinite(dr) && Math.abs(dl - dr) > 1e-2 * (1 + Math.abs(dl) + Math.abs(dr)); }
  // estudi complet: derivades, punts crítics, classificació i curvatura
  function fy(f, x) { var y = f(x); return Math.abs(y) < 1e10 ? y : NaN; }
  function studyF(n, x0, x1, P) {
    var R = derivs(n), f = R.f, S = crit(f, R.df, x0, x1);
    S.f = f; S.n = n; S.dn = R.dn; S.df = R.df; S.d2n = R.d2n; S.d2 = R.d2; S.x0 = x0; S.x1 = x1; S.P = P || 0;
    function cls(Q, j, x) { var l = Q.seg[j].s, r = Q.seg[j + 1].s; return [l, r]; }
    S.ev.forEach(function (e, j) {
      e.y = fy(f, e.x);
      if (e.k === "z" && kink(f, e.x)) e.k = "h";
      if (!isFinite(e.y) || e.k === "e") { e.t1 = "none"; return; }
      var lr = cls(S, j);
      e.t1 = lr[0] > 0 && lr[1] < 0 ? "max" : lr[0] < 0 && lr[1] > 0 ? "min" : "none";
      if (e.k === "z" && S.d2) { var v2 = S.d2(e.x); e.v2 = v2; e.t2 = !isFinite(v2) ? "?" : v2 < -1e-7 ? "max" : v2 > 1e-7 ? "min" : "undec"; }
    });
    var holes = S.ev.filter(function (e) { return !isFinite(e.y); }).map(function (e) { return e.x; });
    var C = crit(f, R.d2, x0, x1, { noJump: true, extra: holes });
    C.ev.forEach(function (e, j) {
      e.y = fy(f, e.x); var lr = cls(C, j); e.inf = isFinite(e.y) && e.k !== "e" && lr[0] * lr[1] < 0;
      // en un punt anguló no hi ha tangent: no l'anomenem punt d'inflexió
      S.ev.forEach(function (q) { if (q.k === "h" && isFinite(q.y) && Math.abs(q.x - e.x) < 1e-2 && kink(f, q.x)) { e.x = q.x; e.y = q.y; e.inf = false; e.k = "h"; C.seg[j].b = q.x; C.seg[j + 1].a = q.x; } });
    });
    S.C = C;
    // funcions periòdiques: el punt inicial del període també pot ser crític o d'inflexió
    if (P) {
      var e0 = { x: x0, y: f(x0) }, l = S.seg[S.seg.length - 1].s, r = S.seg[0].s;
      if (isFinite(e0.y) && Math.abs(R.df(x0)) < 1e-7) { e0.t1 = l > 0 && r < 0 ? "max" : l < 0 && r > 0 ? "min" : "none"; e0.k = "z"; S.edge = e0; }
      var c0 = { x: x0, y: e0.y }, cl = C.seg[C.seg.length - 1].s, cr = C.seg[0].s;
      if (isFinite(c0.y) && Math.abs(R.d2(x0)) < 1e-7 && cl * cr < 0) { c0.inf = true; C.edge = c0; }
    }
    return S;
  }
  function intTex(a, b, aInf, bInf) { return "(" + (aInf ? "-\\infty" : nn(a)) + "," + (bInf ? "+\\infty" : nn(b)) + ")"; }
  // un valor de prova «bonic» dins de l'interval
  function testPt(f, g, sg, aInf, bInf) {
    var a = sg.a, b = sg.b, c;
    if (aInf && bInf) c = 0;
    else if (aInf) c = Math.ceil(b) - 1;
    else if (bInf) c = Math.floor(a) + 1;
    else {
      c = Math.round((a + b) / 2);
      if (!(c > a && c < b)) { c = Math.floor(a) + 1; if (!(c < b)) c = +((a + b) / 2).toFixed(2); }
      if (!(c > a && c < b)) c = (a + b) / 2;
    }
    var v = g(c);
    return isFinite(f(c)) && isFinite(v) && sgn(v) === sg.s ? c : sg.t;
  }
  // taula de signes de f' (two = false) o de f'' (two = true)
  function signTable(S, inf, two) {
    var Q = two ? S.C : S, g = two ? S.d2 : S.df, gl = two ? "f''" : "f'", last = Q.seg.length - 1;
    var r0 = ["<th>" + tex("x") + "</th>"], r1 = ["<th>" + u("test") + "</th>"], r2s = ["<th>" + tex(gl + "(x)") + "</th>"], r3 = ["<th>" + tex("f(x)") + "</th>"];
    Q.seg.forEach(function (sg, j) {
      var aInf = inf && j === 0, bInf = inf && j === last;
      r0.push("<td>" + tex(intTex(sg.a, sg.b, aInf, bInf)) + "</td>");
      if (sg.s === 0) { r1.push('<td class="nd">—</td>'); r2s.push('<td class="nd">∄</td>'); r3.push('<td class="nd">' + u("noDom") + "</td>"); }
      else {
        var t = testPt(S.f, g, sg, aInf, bInf);
        r1.push("<td>" + tex(gl + "(" + nn(t) + ")" + (sg.s > 0 ? "\\gt0" : "\\lt0")) + "</td>");
        r2s.push('<td class="' + (sg.s > 0 ? "p" : "m") + '">' + (sg.s > 0 ? "+" : "−") + "</td>");
        r3.push('<td class="ar ' + (sg.s > 0 ? "p" : "m") + '">' + (two ? (sg.s > 0 ? "∪" : "∩") : (sg.s > 0 ? "↗" : "↘")) + "</td>");
      }
      var e = Q.ev[j]; if (!e) return;
      r0.push('<td class="pt">' + tex(nn(e.x)) + "</td>"); r1.push('<td class="pt"></td>');
      r2s.push('<td class="pt">' + (e.k === "z" ? "0" : "∄") + "</td>");
      var lab = two ? (e.inf ? u("ip") : !isFinite(e.y) ? "∄" : "—") : (e.t1 === "max" ? u("mx") : e.t1 === "min" ? u("mn") : !isFinite(e.y) ? "∄" : "—");
      r3.push('<td class="pt">' + lab + "</td>");
    });
    return '<div class="tbl-wrap"><table class="data sm sgn">' + [r0, r1, r2s, r3].map(function (r) { return "<tr>" + r.join("") + "</tr>"; }).join("") + "</table></div>";
  }
  // intervals (ajuntant els trams separats per un punt on g = 0 sense canvi de signe)
  function runsOf(Q, inf) {
    var runs = [], cur = null, last = Q.seg.length - 1;
    Q.seg.forEach(function (g, j) {
      var prev = Q.ev[j - 1];
      if (cur && g.s === cur.s && prev && prev.k === "z") cur.b = j; else { cur = { s: g.s, a: j, b: j }; runs.push(cur); }
    });
    function iv(r) { return intTex(Q.seg[r.a].a, Q.seg[r.b].b, inf && r.a === 0, inf && r.b === last); }
    return { up: runs.filter(function (r) { return r.s > 0; }).map(iv), dn: runs.filter(function (r) { return r.s < 0; }).map(iv) };
  }
  function monoHtml(S, inf) { var R = runsOf(S, inf); return "<p><strong>" + u("incOn") + "</strong> " + (R.up.length ? tex(R.up.join("\\cup ")) : "—") + "<br><strong>" + u("decOn") + "</strong> " + (R.dn.length ? tex(R.dn.join("\\cup ")) : "—") + "</p>"; }
  function curvHtml(S, inf) { var R = runsOf(S.C, inf); return "<p><strong>" + rt(u("cvx")) + "</strong> " + (R.up.length ? tex(R.up.join("\\cup ")) : "—") + "<br><strong>" + rt(u("ccv")) + "</strong> " + (R.dn.length ? tex(R.dn.join("\\cup ")) : "—") + "</p>"; }
  function ptTex(x, y) { return "(" + nn(x) + "," + nn(y) + ")"; }
  // k·T escrit com 2kπ, kπ, 18k…
  function kT(T) { var c = T / Math.PI, n = Math.round(c); if (Math.abs(c - n) < 1e-9) return (n === 1 ? "" : n) + "k\\pi"; if (Math.abs(T - Math.round(T)) < 1e-9) return Math.round(T) + "k"; return "k\\," + piTex(T); }
  function pk(x, T) { return Math.abs(x) < 1e-12 ? kT(T) : nn(x) + "+" + kT(T); }
  function perK(S) { return S.P ? "+" + kT(S.P) : ""; }
  function extHtml(S, d2) {
    var z = S.ev.filter(function (e) { return (e.k === "z" || (e.k === "h" && isFinite(e.y))) && isFinite(e.y); });
    if (S.edge) z = [S.edge].concat(z);
    if (!z.length) return "<p>" + u("noCrit") + "</p>";
    return "<p>" + z.map(function (e) {
      var w = d2 && e.k === "z" && e.v2 !== undefined ? " &nbsp;(" + tex("f''(" + nn(e.x) + ")" + (e.t2 === "max" ? "\\lt0" : e.t2 === "min" ? "\\gt0" : "=0")) + ")" : "";
      var nd = e.k === "h" ? " — " + rt(u("ndPt")) : "";
      var X = S.P ? "x=" + pk(e.x, S.P) : null;
      return e.t1 === "max" ? '<span class="badge ok">' + u("maxR") + "</span> " + tex(ptTex(e.x, e.y)) + (X ? " " + tex("(" + X + ")") : "") + w + nd
        : e.t1 === "min" ? '<span class="badge as">' + u("minR") + "</span> " + tex(ptTex(e.x, e.y)) + (X ? " " + tex("(" + X + ")") : "") + w + nd
        : tex("x=" + nn(e.x)) + ": " + u("noExt") + nd;
    }).join("<br>") + "</p>";
  }
  function inflHtml(S) {
    var z = S.C.ev.filter(function (e) { return e.inf; });
    if (S.C.edge) z = [S.C.edge].concat(z);
    var no = S.C.ev.filter(function (e) { return e.k === "z" && !e.inf && isFinite(e.y); });
    if (!z.length && !no.length) return "<p>" + u("noInfl") + "</p>";
    var h = z.map(function (e) { return '<span class="badge ev">' + u("infl") + "</span> " + tex(ptTex(e.x, e.y)) + (S.P ? " " + tex("(x=" + pk(e.x, S.P) + ")") : ""); });
    no.forEach(function (e) { h.push(tex("x=" + nn(e.x)) + ": " + u("noInf")); });
    if (!z.length) h.unshift(u("noInfl"));
    return "<p>" + h.join("<br>") + "</p>";
  }
  // gràfica pintada de verd (creix) i roig (decreix)
  function monoCurves(S) { return S.seg.filter(function (g) { return g.s !== 0; }).map(function (g) { return { f: S.f, a: g.a, b: g.b, col: g.s > 0 ? "var(--ok)" : "var(--bad)" }; }); }
  function curvCurves(S) { return S.C.seg.filter(function (g) { return g.s !== 0; }).map(function (g) { return { f: S.f, a: g.a, b: g.b, col: g.s > 0 ? "var(--accent-2)" : "var(--r3)" }; }); }
  function extMarks(S) {
    var L = S.ev.filter(function (e) { return e.t1 === "max" || e.t1 === "min"; });
    if (S.edge && S.edge.t1 !== "none") L = L.concat([S.edge, { x: S.x1, y: S.f(S.x1), t1: S.edge.t1 }]);
    return L.map(function (e) { return { x: e.x, y: e.y, col: e.t1 === "max" ? "var(--ok)" : "var(--bad)" }; });
  }
  function inflPts(S) {
    var L = S.C.ev.filter(function (e) { return e.inf; });
    if (S.C.edge) L = L.concat([S.C.edge, { x: S.x1, y: S.f(S.x1) }]);
    return L.map(function (e) { return { x: e.x, y: e.y, col: "var(--plus)" }; });
  }
  // finestra que mostra tots els punts crítics
  function autoView(S, def) {
    var xs = S.ev.concat(S.C.ev).map(function (e) { return e.x; });
    var x0 = xs.length ? Math.min.apply(null, xs) - 2.5 : def[0], x1 = xs.length ? Math.max.apply(null, xs) + 2.5 : def[1];
    if (x1 - x0 < 6) { var c = (x0 + x1) / 2; x0 = c - 3; x1 = c + 3; }
    if (S.P) { x0 = S.x0 - 0.15 * S.P; x1 = S.x1 + 0.15 * S.P; }
    var yy = autoY([S.f], x0, x1);
    S.ev.forEach(function (e) { if (isFinite(e.y)) { yy[0] = Math.min(yy[0], e.y - 1); yy[1] = Math.max(yy[1], e.y + 1); } });
    return [x0, x1, yy[0], yy[1]];
  }

  /* ---------- domini, periodicitat, simetria i asímptotes ---------- */
  var XL = 40; // finestra d'estudi: [−40, 40]
  // denominadors, arguments de logaritmes, d'arrels i de tangents de l'expressió
  function condsOf(n, out) {
    out = out || { den: [], ln: [], sq: [], tn: [] };
    if (!n || typeof n !== "object") return out;
    if (n.t === "/") out.den.push(n.b);
    if (n.t === "f" && (n.n === "ln" || n.n === "log")) out.ln.push(n.a);
    if (n.t === "f" && n.n === "sqrt") out.sq.push(n.a);
    if (n.t === "f" && n.n === "tan") out.tn.push(n.a);
    if (n.t === "^" && cst(n.b) && cst(n.b).n < 0) out.den.push(n.a);
    if (n.a) condsOf(n.a, out);
    if (n.b) condsOf(n.b, out);
    return out;
  }
  function hasTrig(n) { if (!n || typeof n !== "object") return false; if (n.t === "f" && /^(sin|cos|tan)$/.test(n.n)) return true; return hasTrig(n.a) || hasTrig(n.b); }
  var PER = [Math.PI / 2, 2, 2 * Math.PI / 3, 3, Math.PI, 4, 4 * Math.PI / 3, 2 * Math.PI, 8, 3 * Math.PI, 12, 4 * Math.PI, 18, 24].sort(function (a, b) { return a - b; });
  var PX = [0.123, 0.77, 1.31, 2.05, 2.9, 3.7, 4.42, 5.3, 6.6];
  function periodOf(f, n) {
    if (!hasTrig(n)) return 0;
    for (var i = 0; i < PER.length; i++) {
      var T = PER[i], any = false, ok = PX.every(function (x) {
        var a = f(x), b = f(x + T), c = f(x - 2 * T);
        if (isFinite(a) !== isFinite(b) || isFinite(a) !== isFinite(c)) return false;
        if (!isFinite(a)) return true;
        any = true;
        return Math.abs(a - b) < 1e-9 * (1 + Math.abs(a)) && Math.abs(a - c) < 1e-9 * (1 + Math.abs(a));
      });
      if (ok && any) return T;
    }
    return 0;
  }
  // dom: {iv:[{a,b,aInf,bInf,ai,bi}], ex:[punts exclosos dins dels intervals]}; en [A, B] si és periòdica (sense infinits)
  function domainOf(f, dens, A, B) {
    var per = A !== undefined; A = per ? A : -XL; B = per ? B : XL;
    var N = 8000, h = (B - A) / N, X = [], OK = [], i, runs = [], cur = null, holes = [];
    for (i = 0; i <= N; i++) { X.push(A + i * h); OK.push(isFinite(f(X[i]))); }
    for (i = 1; i < N; i++) if (!OK[i] && OK[i - 1] && OK[i + 1]) { OK[i] = true; holes.push(snap(X[i])); }
    for (i = 0; i <= N; i++) { if (OK[i]) { if (!cur) { cur = { i0: i }; runs.push(cur); } cur.i1 = i; } else cur = null; }
    function edge(xIn, xOut) {
      for (var it = 0; it < 80; it++) { var m = (xIn + xOut) / 2; if (isFinite(f(m))) xIn = m; else xOut = m; }
      return snap((xIn + xOut) / 2);
    }
    function far(s) { return [1e2, 1e3, 1e6].some(function (v) { return !isNaN(f(s * v)); }); }
    var iv = [];
    runs.forEach(function (r) {
      if (r.i1 - r.i0 < 2) return;
      var o = { aInf: false, bInf: false };
      if (r.i0 > 0) o.a = edge(X[r.i0], X[r.i0 - 1]); else if (per) { o.a = A; o.cut = 1; } else if (far(-1)) o.aInf = true; else o.a = edge(X[0], -1e2);
      if (r.i1 < N) o.b = edge(X[r.i1], X[r.i1 + 1]); else if (per) { o.b = B; o.cut = (o.cut || 0) + 2; } else if (far(1)) o.bInf = true; else o.b = edge(X[N], 1e2);
      o.ai = !o.aInf && isFinite(f(o.a)); o.bi = !o.bInf && isFinite(f(o.b));
      iv.push(o);
    });
    var ex = [];
    function inside(p) { return iv.some(function (o) { return (o.aInf || p > o.a + 1e-9) && (o.bInf || p < o.b - 1e-9); }); }
    function addEx(p) { if (!inside(p)) return; for (var k = 0; k < ex.length; k++) if (Math.abs(ex[k] - p) < 1e-6 * (1 + Math.abs(p))) return; ex.push(p); }
    (dens || []).forEach(function (g) { roots(g, A, B).forEach(addEx); });
    holes.forEach(addEx);
    ex.sort(function (p, q) { return p - q; });
    return { iv: iv, ex: ex, per: per, A: A, B: B };
  }
  function inDom(Dm, x) {
    if (Dm.ex.some(function (p) { return Math.abs(p - x) < 1e-9; })) return false;
    return Dm.iv.some(function (o) { return (o.aInf || x > o.a || (o.ai && x === o.a)) && (o.bInf || x < o.b || (o.bi && x === o.b)); });
  }
  function domParts(Dm) {
    var out = [];
    Dm.iv.forEach(function (o) {
      var pts = Dm.ex.filter(function (p) { return (o.aInf || p > o.a) && (o.bInf || p < o.b); });
      var bs = [o.aInf ? -Infinity : o.a].concat(pts).concat([o.bInf ? Infinity : o.b]);
      for (var k = 0; k + 1 < bs.length; k++) out.push({ a: bs[k], b: bs[k + 1], ai: k === 0 && o.ai, bi: k + 2 === bs.length && o.bi });
    });
    return out;
  }
  function domTex(Dm, T) {
    if (!Dm.iv.length) return "\\varnothing";
    if (Dm.per) {
      // tot el període menys uns punts: ℝ − {p + kT}
      var whole = Dm.iv.length === 1 && Dm.iv[0].cut === 3 || (Dm.iv.length === 2 && Dm.iv[0].cut === 1 && Dm.iv[1].cut === 2 && Math.abs(Dm.iv[0].b - Dm.iv[1].a) < 1e-6);
      if (whole) {
        var pts = Dm.ex.slice(); if (Dm.iv.length === 2) pts.push(Dm.iv[0].b);
        pts = pts.filter(function (p) { return p < Dm.A + T - 1e-9; }).sort(function (p, q) { return p - q; });
        return pts.length ? "\\mathbb R-\\left\\{" + pts.map(function (p) { return pk(p, T); }).join(",\\ ") + "\\right\\}" : "\\mathbb R";
      }
    }
    if (Dm.iv.length === 1 && Dm.iv[0].aInf && Dm.iv[0].bInf) return Dm.ex.length ? "\\mathbb R-\\{" + Dm.ex.map(nn).join(",\\,") + "\\}" : "\\mathbb R";
    return domParts(Dm).map(function (p) {
      return (p.ai ? "[" : "(") + (isFinite(p.a) ? nn(p.a) : "-\\infty") + "," + (isFinite(p.b) ? nn(p.b) : "+\\infty") + (p.bi ? "]" : ")");
    }).join("\\cup ");
  }
  function domBands(Dm) {
    var out = [], P = Dm.iv;
    if (!P.length) return [{ a: -1e9, b: 1e9 }];
    if (Dm.per) return []; // es repetiria en cada període: no ombregem
    if (!P[0].aInf) out.push({ a: -1e9, b: P[0].a });
    for (var k = 0; k + 1 < P.length; k++) out.push({ a: P[k].b, b: P[k + 1].a });
    if (!P[P.length - 1].bInf) out.push({ a: P[P.length - 1].b, b: 1e9 });
    return out;
  }
  function zerosOf(g, A, B) {
    A = A === undefined ? -XL : A; B = B === undefined ? XL : B;
    var r = roots(g, A, B);
    domainOf(g, []).iv.forEach(function (o) {
      [o.aInf || !o.ai ? NaN : o.a, o.bInf || !o.bi ? NaN : o.b].forEach(function (p) {
        if (isFinite(p) && p >= A && p <= B && Math.abs(g(p)) < 1e-7 && !r.some(function (q) { return Math.abs(q - p) < 1e-6 * (1 + Math.abs(p)); })) r.push(p);
      });
    });
    return r.sort(function (p, q) { return p - q; });
  }
  function signSet(g, test) { return domTex(domainOf(function (x) { var v = g(x); return test(v) ? 1 : NaN; }, [])); }
  function domWhy(n, T) {
    var C = condsOf(n), h = [], A = T ? 0 : -XL, B = T ? T : XL;
    function lst(r) { return r.length > 6 ? r.slice(0, 6).map(nn).join(",\\ x=") + ",\\ \\ldots" : r.map(nn).join(",\\ x="); }
    C.den.forEach(function (d) {
      if (strip(d).t === "n" || strip(d).t === "c") return;
      var r = zerosOf(compile(d), A, B);
      h.push("<li>" + u("den") + " " + tex(T_(d)) + ": " + (r.length ? u("denZ") + " " + tex("x=" + lst(r)) + (T ? " (" + u("inPer") + ")" : "") : u("denNo")) + "</li>");
    });
    C.tn.forEach(function (a) { h.push("<li>" + u("tanArg") + " " + tex("\\cos\\left(" + T_(a) + "\\right)=0") + "</li>"); });
    if (!T) C.ln.forEach(function (a) { h.push("<li>" + u("lnArg") + " " + u("lnPos") + ": " + tex(T_(a) + "\\gt0\\ \\Leftrightarrow\\ x\\in " + signSet(compile(a), function (v) { return v > 1e-12; })) + "</li>"); });
    if (!T) C.sq.forEach(function (a) { h.push("<li>" + u("sqArg") + " " + u("sqPos") + ": " + tex(T_(a) + "\\geq0\\ \\Leftrightarrow\\ x\\in " + signSet(compile(a), function (v) { return v > -1e-12; })) + "</li>"); });
    return h.length ? "<ul>" + h.join("") + "</ul>" : "<p>" + u("noCond") + "</p>";
  }
  function T_(n) { return texD(n); }
  var SYM_X = [0.37, 0.81, 1.23, 1.9, 2.71, 3.3, 4.6, 6.1, 7.7, 11.3];
  function symOf(f) {
    var ev = true, od = true, any = false;
    for (var i = 0; i < SYM_X.length; i++) {
      var x = SYM_X[i], a = f(x), b = f(-x);
      if (isFinite(a) !== isFinite(b)) return "dom";
      if (!isFinite(a)) continue;
      any = true;
      var tol = 1e-9 * (1 + Math.abs(a));
      if (Math.abs(a - b) > tol) ev = false;
      if (Math.abs(a + b) > tol) od = false;
    }
    if (!any) return "none";
    return ev ? "even" : od ? "odd" : "none";
  }
  function symTxt(s) { return s === "even" ? u("even") : s === "odd" ? u("odd") : s === "dom" ? u("noSym") + " (" + u("symNoDom") + ")" : u("noSym"); }
  function cutsOf(f, Dm, T) {
    var y0 = inDom(Dm, 0) || (T && isFinite(f(0))) ? f(0) : NaN;
    var xs = (T ? zerosOf(f, 0, T - 1e-9) : zerosOf(f)).filter(function (x) { return (T || inDom(Dm, x)) && Math.abs(f(x)) < 1e-7; });
    return { oy: isFinite(y0) ? (Math.abs(y0) < 1e-12 ? 0 : y0) : null, ox: xs, T: T };
  }
  function cutsHtml(C) {
    var k = C.T ? "+" + kT(C.T) : "";
    return "<p><strong>" + u("cutX") + ":</strong> " + (C.ox.length ? tex("f(x)=0\\ \\Rightarrow\\ " + (C.T ? C.ox.map(function (x) { return "x=" + pk(x, C.T); }).join(",\\ ") : C.ox.map(function (x) { return "(" + nn(x) + ",0)"; }).join(",\\ "))) + (C.T ? " " + rt(u("andK")) : "") : u("noCutX")) +
      "<br><strong>" + u("cutY") + ":</strong> " + (C.oy !== null ? tex("x=0\\ \\Rightarrow\\ f(0)=" + nn(C.oy) + "\\ \\Rightarrow\\ (0," + nn(C.oy) + ")") : u("noCutY")) + "</p>";
  }
  function cutPts(C, view) {
    var p = [];
    C.ox.forEach(function (x) { if (C.T) { for (var k = -3; k <= 3; k++) { var z = x + k * C.T; if (z >= view[0] && z <= view[1]) p.push({ x: z, y: 0, col: "var(--accent-2)" }); } } else p.push({ x: x, y: 0, col: "var(--accent-2)" }); });
    if (C.oy !== null) p.push({ x: 0, y: C.oy, col: "var(--accent-2)" });
    return p;
  }
  function polyQ(n) { try { polyOf(n); return true; } catch (e) { return false; } }
  // asímptotes: verticals (límits laterals) i, en cada costat, horitzontal / obliqua / cap
  function asyOf(f, Dm, T) {
    var cand = [];
    function add(c) { if (!cand.some(function (p) { return Math.abs(p - c) < 1e-7; })) cand.push(c); }
    Dm.iv.forEach(function (o) { if (!o.aInf && !(o.cut & 1)) add(o.a); if (!o.bInf && !(o.cut & 2)) add(o.b); });
    Dm.ex.forEach(add);
    if (T && Dm.iv.length === 2 && Dm.iv[0].cut === 1) add(Dm.iv[0].b);
    cand.sort(function (p, q) { return p - q; });
    var av = [];
    cand.forEach(function (c) {
      var L = isFinite(f(c - 1e-6)) ? limSide(f, c, -1) : null, R = isFinite(f(c + 1e-6)) ? limSide(f, c, 1) : null;
      if ((L && L.k === "inf") || (R && R.k === "inf")) av.push({ x: c, L: L, R: R });
    });
    var side = {};
    [-1, 1].forEach(function (s) {
      if (T) { side[s] = { k: "per" }; return; }
      var P = Dm.iv[s < 0 ? 0 : Dm.iv.length - 1];
      if (!P || !(s < 0 ? P.aInf : P.bInf)) { side[s] = { k: "no" }; return; }
      var L = limSide(f, s * Infinity, s);
      if (L.k === "num") { side[s] = { k: "h", y: snap(Math.abs(L.v) < 1e-5 ? 0 : L.v) }; return; }
      if (L.k !== "inf") { side[s] = { k: "none" }; return; }
      var M = limSide(function (x) { return f(x) / x; }, s * Infinity, s);
      if (M.k === "num" && Math.abs(M.v) > 1e-6) {
        var m = snap(M.v), Nn = limSide(function (x) { return f(x) - m * x; }, s * Infinity, s);
        if (Nn.k === "num") { side[s] = { k: "o", m: m, n: snap(Math.abs(Nn.v) < 1e-5 ? 0 : Nn.v) }; return; }
      }
      side[s] = { k: "p" };
    });
    return { av: av, side: side, T: T };
  }
  function sideTx(o) {
    if (o.k === "h") return u("ah") + " " + tex("y=" + nn(o.y));
    if (o.k === "o") return u("ao") + " " + tex(lineT(o.m, 0, o.n));
    if (o.k === "no") return u("notTo");
    return u("noAsy") + (o.k === "p" ? " (" + u("branch") + ")" : "");
  }
  function avHtml(A) {
    if (!A.av.length) return u("noAV");
    var k = A.T ? "+" + kT(A.T) : "";
    return A.av.map(function (q) {
      var l = [];
      if (q.L) l.push(tex("\\lim_{x\\to " + nn(q.x) + "^-}f(x)=" + limTex(q.L)));
      if (q.R) l.push(tex("\\lim_{x\\to " + nn(q.x) + "^+}f(x)=" + limTex(q.R)));
      return tex("x=" + (A.T ? pk(q.x, A.T) : nn(q.x))) + " &nbsp;(" + l.join(",&ensp;") + ")";
    }).join("<br>") + (A.T ? "<br>" + rt(u("andK")) : "");
  }
  function asyHtml(A, poly) {
    if (poly) return "<p>" + u("poly") + "</p>";
    var h = "<p><strong>" + u("av") + ":</strong> " + avHtml(A) + "</p><p>";
    if (A.T) return h + u("perAsy") + "</p>";
    var sL = A.side[-1], sR = A.side[1], same = sL.k === sR.k && (sL.k === "h" ? Math.abs(sL.y - sR.y) < 1e-9 : sL.k === "o" ? Math.abs(sL.m - sR.m) + Math.abs(sL.n - sR.n) < 1e-9 : true);
    var up = function (s) { return s.replace(/^./, function (c) { return c.toUpperCase(); }); };
    h += same ? up(sideTx(sL)) + " (" + u("toL") + " " + t3("i", "y", "and") + " " + u("toR").replace(/^(quan|cuando|as) /, "") + ")" : up(u("toL")) + ": " + sideTx(sL) + "<br>" + up(u("toR")) + ": " + sideTx(sR);
    return h + "</p>";
  }
  function asyPlot(A, view) {
    var ha = [], oa = [], va = [];
    [-1, 1].forEach(function (s) {
      var o = A.side[s];
      if (o.k === "h" && ha.indexOf(o.y) < 0) ha.push(o.y);
      if (o.k === "o" && !oa.some(function (q) { return q.m === o.m && q.n === o.n; })) oa.push({ m: o.m, n: o.n });
    });
    A.av.forEach(function (q) { if (A.T) { for (var k = -4; k <= 4; k++) { var z = q.x + k * A.T; if (z > view[0] && z < view[1]) va.push(z); } } else va.push(q.x); });
    return { va: va, ha: ha, oa: oa };
  }
  function viewOf(f, xs, ys, def) {
    xs = xs.filter(isFinite); ys = ys.filter(isFinite);
    var x0 = xs.length ? Math.min.apply(null, xs) - 3 : def[0], x1 = xs.length ? Math.max.apply(null, xs) + 3 : def[1];
    if (x1 - x0 < 8) { var c = (x0 + x1) / 2; x0 = c - 4; x1 = c + 4; }
    var yy = autoY([f], x0, x1);
    if (ys.length) {
      var lo = Math.min.apply(null, ys), hi = Math.max.apply(null, ys), sp = Math.max(hi - lo, 2);
      yy = [Math.min(Math.max(yy[0], lo - 2.5 * sp), lo - 0.8 * sp), Math.max(Math.min(yy[1], hi + 2.5 * sp), hi + 0.8 * sp)];
    }
    return [x0, x1, yy[0], yy[1]];
  }
  // estudi complet: domini, simetria, periodicitat, talls, asímptotes, monotonia, extrems i curvatura
  function fullStudy(n) {
    var f = compile(n), C = condsOf(n), T = periodOf(f, n);
    var dens = C.den.map(compile).concat(C.tn.map(function (a) { return compile(Fn("cos", a)); }));
    var Dm = T ? domainOf(f, dens, 0, T) : domainOf(f, dens);
    var R = { n: n, f: f, Dm: Dm, T: T, poly: polyQ(n) };
    R.cuts = cutsOf(f, Dm, T); R.sym = symOf(f); R.A = asyOf(f, Dm, T);
    if (T) { R.S = studyF(n, 0, T, T); R.inf = false; }
    else { R.S = studyF(n, -XL, XL); R.inf = true; if (R.S.ev.length + R.S.C.ev.length > 18) { R.S = studyF(n, -8, 8); R.inf = false; } }
    if (T) { R.view = [-0.25 * T, 1.75 * T]; var yy = autoY([f], R.view[0], R.view[1]); R.view = R.view.concat(yy); return R; }
    var xs = R.cuts.ox.concat(R.A.av.map(function (q) { return q.x; })), ys = [];
    if (R.cuts.oy !== null) { xs.push(0); ys.push(R.cuts.oy); }
    Dm.iv.forEach(function (o) { if (!o.aInf && Math.abs(o.a) < XL) xs.push(o.a); if (!o.bInf && Math.abs(o.b) < XL) xs.push(o.b); });
    R.S.ev.forEach(function (e) { if (e.t1 === "max" || e.t1 === "min") { xs.push(e.x); ys.push(e.y); } });
    R.S.C.ev.forEach(function (e) { if (e.inf) { xs.push(e.x); ys.push(e.y); } });
    [-1, 1].forEach(function (s) { if (R.A.side[s].k === "h") ys.push(R.A.side[s].y); });
    R.view = viewOf(f, xs, ys, [-6, 6]);
    return R;
  }

  /* ---------- figures estàtiques ---------- */
  var FIGS = {
    mono: function () {
      var f = F("x^3/3-x^2-3x+4"), df = F("x^2-2x-3");
      return { v: [-3.2, 5.2, -6, 8], curves: [{ f: f, b: -1, col: "var(--ok)" }, { f: f, a: -1, b: 3, col: "var(--bad)" }, { f: f, a: 3, col: "var(--ok)" }, segAt(df(-2), -2, f(-2), [-3.2, 5.2, -6, 8], "var(--accent-2)"), segAt(df(1), 1, f(1), [-3.2, 5.2, -6, 8], "var(--accent-2)"), segAt(0, -1, f(-1), [-3.2, 5.2, -6, 8], "var(--accent-2)"), segAt(0, 3, f(3), [-3.2, 5.2, -6, 8], "var(--accent-2)")],
        mark: [{ x: -1, y: f(-1), col: "var(--ok)" }, { x: 3, y: f(3), col: "var(--bad)" }], labels: [{ x: -1, y: f(-1) + 1.1, t: "f′ = 0" }, { x: 3, y: f(3) - 1, t: "f′ = 0" }, { x: -2.5, y: 4.6, t: "f′ > 0", anchor: "start" }, { x: 1.6, y: 3.2, t: "f′ < 0", anchor: "start" }] };
    },
    cvx: function () {
      var f = F("x^2/2"), v = [-2.6, 2.6, -1, 3];
      return { v: v, curves: [{ f: f, col: "var(--accent-2)" }, segAt(-1, -1, 0.5, v, "var(--muted)", 0.3), segAt(1.5, 1.5, 1.125, v, "var(--muted)", 0.3)], pts: [{ x: -1, y: 0.5 }, { x: 1.5, y: 1.125 }], labels: [{ x: 0, y: 2.5, t: "f″ > 0  ∪" }] };
    },
    ccv: function () {
      var f = F("-x^2/2+2"), v = [-2.6, 2.6, -1, 3];
      return { v: v, curves: [{ f: f, col: "var(--r3)" }, segAt(1, -1, 1.5, v, "var(--muted)", 0.3), segAt(-1.5, 1.5, 0.875, v, "var(--muted)", 0.3)], pts: [{ x: -1, y: 1.5 }, { x: 1.5, y: 0.875 }], labels: [{ x: 0, y: 2.6, t: "f″ < 0  ∩" }] };
    },
    infl: function () {
      var f = F("x^3/3-x"), v = [-2.6, 2.6, -2, 2];
      return { v: v, curves: [{ f: f, b: 0, col: "var(--r3)" }, { f: f, a: 0, col: "var(--accent-2)" }, { f: lineF(-1, 0, 0), col: "var(--muted)", a: -1.6, b: 1.6 }], pts: [{ x: 0, y: 0, col: "var(--plus)" }], labels: [{ x: -1.8, y: 1.5, t: "∩" }, { x: 1.8, y: -1.4, t: "∪" }, { x: 0.15, y: 0.35, t: "P.I.", anchor: "start" }] };
    },
    rolle: function () {
      var f = F("-(x-1)(x-5)/2+1"), v = [0, 6, -0.5, 4];
      return { v: v, curves: [{ f: f, a: 1, b: 5 }, { f: function () { return 1; }, col: "var(--r3)", a: 1, b: 5 }, { f: function () { return 3; }, col: "var(--accent-2)", a: 1.8, b: 4.2 }], pts: [{ x: 1, y: 1 }, { x: 5, y: 1 }, { x: 3, y: 3, col: "var(--accent-2)" }], guides: [{ x: 3 }],
        labels: [{ x: 1, y: 0.55, t: "a" }, { x: 5, y: 0.55, t: "b" }, { x: 3.15, y: 0.2, t: "c", anchor: "start" }, { x: 3, y: 3.4, t: "f′(c) = 0" }] };
    },
    lag: function () {
      var f = F("x^3/6-x/2+1"), a = -1, b = 2.5, m = (f(b) - f(a)) / (b - a), c = Math.sqrt((m + 0.5) * 2), v = [-1.6, 3, -0.5, 3.5];
      return { v: v, curves: [{ f: f, a: a, b: b }, { f: lineF(m, a, f(a)), col: "var(--r3)", a: a, b: b }, { f: lineF(m, c, f(c)), col: "var(--accent-2)", a: c - 1.3, b: c + 1.3 }], pts: [{ x: a, y: f(a) }, { x: b, y: f(b) }, { x: c, y: f(c), col: "var(--accent-2)" }], guides: [{ x: c }],
        labels: [{ x: a, y: f(a) - 0.4, t: "a" }, { x: b + 0.1, y: f(b) - 0.3, t: "b", anchor: "start" }, { x: c + 0.1, y: -0.25, t: "c", anchor: "start" }] };
    },
    absx: function () {
      var f = F("x^3-6x^2+9x+1"), v = [-0.6, 4.6, -1.5, 6];
      return { v: v, curves: [{ f: f, a: -0.3, b: 4.2 }], pts: [{ x: -0.3, y: f(-0.3), col: "var(--bad)" }, { x: 4.2, y: f(4.2), col: "var(--ok)" }], mark: [{ x: 1, y: 5, col: "var(--ok)" }, { x: 3, y: 1, col: "var(--bad)" }], guides: [{ x: -0.3 }, { x: 4.2 }],
        labels: [{ x: 1, y: 5.5, t: "màx. rel." }, { x: 3, y: 0.4, t: "mín. rel." }, { x: 4.2, y: 5.6, t: "màx. abs.", anchor: "end" }, { x: -0.2, y: -1.1, t: "mín. abs.", anchor: "start" }] };
    },
    pw: function () {
      var P = pwMake({ p: ["x^2+4x+3", "3e^(-x)"], c: [0], inc: ["L"] }), v = [-4.5, 4.5, -1.6, 4], dr = pwDraw(P, v);
      return { v: v, curves: dr.curves, pts: dr.pts.concat([{ x: 0, y: 3 }, { x: -1, y: 0, col: "var(--accent-2)" }, { x: -3, y: 0, col: "var(--accent-2)" }]), mark: [{ x: -2, y: -1, col: "var(--bad)" }, { x: 0, y: 3, col: "var(--ok)" }], ha: [0] };
    }
  };
  function wFigs() {
    document.querySelectorAll("[data-g]").forEach(function (el) {
      var mk = FIGS[el.getAttribute("data-g")]; if (!mk) return;
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("class", "lp-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Gràfica");
      el.appendChild(svg);
      var cfg = mk();
      onLang(function () { plot(svg, cfg); });
    });
  }
  // gràfiques estàtiques generades amb l'estudi complet (exemples resolts)
  function wStudyFigs() {
    document.querySelectorAll("[data-sf]").forEach(function (el) {
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("class", "lp-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Gràfica");
      el.appendChild(svg);
      var v = el.getAttribute("data-v"), R = fullStudy(parse(el.getAttribute("data-sf")));
      if (v) R.view = v.split(",").map(Number);
      onLang(function () { plot(svg, finalCfg(R)); });
    });
  }
  function finalCfg(R) {
    var cfg = { v: R.view, band: domBands(R.Dm), pts: cutPts(R.cuts, R.view), mark: extMarks(R.S).concat(inflPts(R.S).map(function (p) { return { x: p.x, y: p.y, col: "var(--plus)" }; })) };
    Object.assign(cfg, asyPlot(R.A, R.view));
    cfg.curves = R.T ? [{ f: R.f }] : monoCurves(R.S);
    if (R.T) cfg.mark = periodic(cfg.mark, R.T, R.view);
    return cfg;
  }
  function periodic(L, T, view) {
    var out = [];
    L.forEach(function (p) { for (var k = -3; k <= 3; k++) { var x = p.x + k * T; if (x >= view[0] - 1e-9 && x <= view[1] + 1e-9 && !out.some(function (q) { return Math.abs(q.x - x) < 1e-6; })) out.push({ x: x, y: p.y, col: p.col }); } });
    return out;
  }

  /* ---------- ginys amb una funció escrita ---------- */
  function fnInput(w, PRE, key, draw, two) {
    var fi = $(w, "f"), ai = $(w, "a");
    presetBtns($(w, "presets"), PRE.length, key, function (i) { fi.value = PRE[i][0]; if (ai && PRE[i][1] !== undefined) ai.value = PRE[i][1]; draw(); });
    fi.addEventListener("input", draw); if (ai) ai.addEventListener("input", draw);
    return { fi: fi, ai: ai };
  }
  function readF(w, fi) {
    try { var n = strip0(parse(fi.value)); fi.classList.remove("bad"); return n; } catch (e) { fi.classList.add("bad"); w.querySelector(".info").textContent = u("bad"); return null; }
  }
  // punt d'un límit: nombre, ±inf, i un + o − al final per als laterals
  function readPt(s) {
    s = String(s).trim().replace(/−/g, "-").replace(/∞/g, "inf").replace(/\s+/g, "");
    if (/^\+?inf(inity)?$/i.test(s)) return { a: Infinity, s: 0, t: "+\\infty" };
    if (/^-inf(inity)?$/i.test(s)) return { a: -Infinity, s: 0, t: "-\\infty" };
    var side = 0, m = s.match(/^(.*\S)([+-])$/);
    if (m && m[1].length) { side = m[2] === "+" ? 1 : -1; s = m[1]; }
    var v = readNum(s); if (!isFinite(v)) return null;
    return { a: v, s: side, t: nn(v) + (side > 0 ? "^+" : side < 0 ? "^-" : "") };
  }

  /* ---------- 7.1 tangent i normal ---------- */
  function wTn() {
    var w = document.getElementById("w-tn"); if (!w) return;
    var PRE = [["x^3-3x", "2"], ["sqrt(x^2+5)", "-2"], ["e^(2x)", "0"], ["ln(x^2-3)", "2"], ["sin(x)+cos(x)", "pi/4"], ["(2x^2+2x-2)/(3x^2+3)", "1"]];
    var I = fnInput(w, PRE, "pTn", draw), svg = w.querySelector("svg"), info = w.querySelector(".info");
    function draw() {
      var n = readF(w, I.fi); if (!n) return;
      var a = readNum(I.ai.value); I.ai.classList.toggle("bad", !isFinite(a)); if (!isFinite(a)) { info.textContent = u("aBad"); return; }
      var f = compile(n), dn, df;
      try { dn = D(n); df = compile(dn); } catch (e) { info.textContent = u("noDiff"); return; }
      var fa = f(a), m = df(a), at = nn(a), h = "<p>" + tex("f(x)=" + texD(n)) + "</p><p>" + tex("f'(x)=" + texD(dn)) + "</p>";
      var v0 = [a - 4, a + 4], yy = autoY([f], v0[0], v0[1]);
      if (isFinite(fa)) { yy = [Math.min(yy[0], fa - 2), Math.max(yy[1], fa + 2)]; if (yy[1] - yy[0] > 30) yy = [fa - 12, fa + 12]; }
      var v = v0.concat(yy), cfg = { v: v, curves: [{ f: f }], pts: [] };
      if (!isFinite(fa)) h += '<p class="msg-bad">' + u("noF") + "</p>";
      else if (!isFinite(m)) h += '<p class="msg-bad">' + u("noD") + "</p>";
      else {
        h += "<p>" + tex("f(" + at + ")=" + nn(fa) + ",\\qquad f'(" + at + ")=" + nn(m)) + "</p>";
        h += "<p><strong>" + u("tline") + ":</strong> " + tex(ptSl(m, a, fa) + "\\ \\Rightarrow\\ " + lineT(m, a, fa)) + "</p>";
        cfg.curves.push({ f: lineF(m, a, fa), col: "var(--accent-2)" });
        if (Math.abs(m) < 1e-12) { h += "<p>" + u("horT") + " " + tex("x=" + at) + "</p>"; cfg.segs = [{ l: [[a, v[2], a, v[3]]], col: "var(--r3)" }]; }
        else {
          var mn = -1 / m;
          h += "<p><strong>" + u("nline") + ":</strong> " + tex("m_n=-\\dfrac{1}{" + nn(m) + "}=" + nn(mn) + "\\ \\Rightarrow\\ " + ptSl(mn, a, fa) + "\\ \\Rightarrow\\ " + lineT(mn, a, fa)) + "</p>";
          cfg.curves.push({ f: lineF(mn, a, fa), col: "var(--r3)" });
        }
        cfg.pts.push({ x: a, y: fa });
      }
      info.innerHTML = h;
      plot(svg, cfg);
    }
    onLang(draw);
  }
  // tangents des d'un punt exterior
  function wTp() {
    var w = document.getElementById("w-tp"); if (!w) return;
    var PRE = [["x^2", "1", "-3"], ["x^2/4+4x+4", "0", "0"], ["x^3", "2", "0"], ["e^x", "0", "0"], ["1/x", "0", "1"]];
    var fi = $(w, "f"), pi = $(w, "p"), qi = $(w, "q"), svg = w.querySelector("svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pTp", function (i) { fi.value = PRE[i][0]; pi.value = PRE[i][1]; qi.value = PRE[i][2]; draw(); });
    [fi, pi, qi].forEach(function (e) { e.addEventListener("input", draw); });
    function draw() {
      var n = readF(w, fi); if (!n) return;
      var p = readNum(pi.value), q = readNum(qi.value);
      pi.classList.toggle("bad", !isFinite(p)); qi.classList.toggle("bad", !isFinite(q)); if (!isFinite(p) || !isFinite(q)) { info.textContent = u("aBad"); return; }
      var f = compile(n), dn; try { dn = D(n); } catch (e) { info.textContent = u("noDiff"); return; }
      var df = compile(dn), P = "(" + nn(p) + "," + nn(q) + ")";
      var g = function (a) { return f(a) + df(a) * (p - a) - q; };
      var as = roots(g, p - 12, p + 12, 6000).filter(function (a) { return isFinite(f(a)) && isFinite(df(a)); });
      var h = "<p>" + tex("f(x)=" + texD(n) + ",\\qquad f'(x)=" + texD(dn)) + "</p>";
      h += "<p>" + rt(u("genT")) + "</p><p>" + tex(nn(q) + "-f(a)=f'(a)\\left(" + nn(p) + "-a\\right)") + "</p>";
      var on = Math.abs(f(p) - q) < 1e-9 * (1 + Math.abs(q));
      if (on) h += "<p>" + u("onC") + "</p>";
      var cfg = { curves: [{ f: f }], pts: [{ x: p, y: q, col: "var(--r3)" }] }, xs = [p], ys = [q];
      if (!as.length) h += '<p class="msg-bad">' + u("noTan") + "</p>";
      else {
        h += "<p>" + tex("a=" + as.map(nn).join(",\\ a=")) + "</p><ul>";
        as.forEach(function (a, k) {
          var fa = f(a), m = df(a);
          h += "<li>" + u("tAt") + " " + tex(ptTex(a, fa)) + ": " + tex(lineT(m, a, fa)) + "</li>";
          cfg.curves.push({ f: lineF(m, a, fa), col: k % 2 ? "var(--r3)" : "var(--accent-2)" }); cfg.pts.push({ x: a, y: fa }); xs.push(a); ys.push(fa);
        });
        h += "</ul>";
      }
      info.innerHTML = h;
      var x0 = Math.min.apply(null, xs) - 2.5, x1 = Math.max.apply(null, xs) + 2.5, y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys), yy = autoY([f], x0, x1);
      cfg.v = [x0, x1, Math.min(y0 - 2, Math.max(yy[0], y0 - 10)), Math.max(y1 + 2, Math.min(yy[1], y1 + 10))];
      plot(svg, cfg);
    }
    onLang(draw);
  }

  /* ---------- 7.2 i 7.3 regla de L'Hôpital ---------- */
  function limAt(g, P) {
    if (!isFinite(P.a)) return limSide(g, P.a, P.a > 0 ? 1 : -1);
    if (P.s) return contSide(g, P.a, P.s);
    var L = contSide(g, P.a, -1), R = contSide(g, P.a, 1);
    if (sameLim(L, R)) return L;
    if (L.k === "inf" && R.k === "inf") return { k: "inf", s: 0, L: L, R: R };
    return { k: "two", L: L, R: R };
  }
  function kindOf(r) { return r.k === "num" ? (Math.abs(r.v) < 1e-8 ? "0" : "k") : r.k === "inf" ? "inf" : "?"; }
  function limTx(r) { return r.k === "inf" && !r.s ? "\\infty" : r.k === "two" ? "\\nexists" : r.k === "num" ? nn(Math.abs(r.v) < 1e-8 ? 0 : r.v) : limTex(r); }
  // aplica L'Hôpital tantes vegades com calga (fins a 5); torna les línies en TeX i el resultat
  function hopital(N0, D0, P) {
    var lines = [], N = N0, Dd = D0, at = "\\lim_{x\\to " + P.t + "}", res = null, note = "";
    for (var k = 0; k <= 5; k++) {
      var fN = compile(N), fD = compile(Dd), LN = limAt(fN, P), LD = limAt(fD, P), kN = kindOf(LN), kD = kindOf(LD);
      // la primera línia escriu el límit; les següents continuen la cadena d'igualtats
      var q = k === 0 ? at + "\\dfrac{" + texD(N) + "}{" + texD(Dd) + "}" : "";
      var ind = (kN === "0" && kD === "0") ? "\\left[\\dfrac{0}{0}\\right]" : (kN === "inf" && kD === "inf") ? "\\left[\\dfrac{\\infty}{\\infty}\\right]" : null;
      if (ind && k === 5) { lines.push({ t: "=" + ind }); note = u("many"); break; }
      if (ind) {
        var dN = D(N), dD = D(Dd), Q = simp(B("/", dN, dD));
        lines.push({ t: q + "=" + ind, hop: true });
        lines.push({ t: "\\overset{\\text{L'H}}{=}" + at + "\\dfrac{" + texD(dN) + "}{" + texD(dD) + "}", sub: true });
        var Qs = strip0(Q);
        if (Qs.t !== "/" || texD(Qs.a) !== texD(dN) || texD(Qs.b) !== texD(dD)) lines.push({ t: "=" + at + (Qs.t === "/" ? "\\dfrac{" + texD(Qs.a) + "}{" + texD(Qs.b) + "}" : (Qs.t === "+" || Qs.t === "-" ? "\\left(" + texD(Q) + "\\right)" : texD(Q))), sub: true, simp: true });
        if (Qs.t === "/") { N = Qs.a; Dd = Qs.b; }
        else { N = Q; Dd = ONE; }
        continue;
      }
      // ja no és indeterminat: calculem el límit del quocient
      var fq = function (x) { return fN(x) / fD(x); }, L = limAt(fq, P);
      if (k > 0) lines.push({ t: "=" + limTx(L), end: true });
      else lines.push({ t: q + "=" + limTx(L), end: true, noInd: true });
      res = L;
      if (L.k === "osc" || L.k === "none") note = u("osc");
      if (L.k === "two" || (L.k === "inf" && !L.s)) { note = u("sideDiff"); lines[lines.length - 1].t += "\\quad\\left(\\lim_{x\\to " + P.t + "^-}=" + limTex(L.L) + ",\\ \\lim_{x\\to " + P.t + "^+}=" + limTex(L.R) + "\\right)"; }
      break;
    }
    return { lines: lines, res: res, note: note };
  }
  function hopHtml(H) {
    var h = "";
    H.lines.forEach(function (l) {
      if (l.hop) h += "<p>" + tex(l.t) + "<br><span class=\"hint\">" + u("hopT") + "</span></p>";
      else if (l.simp) h += "<p><span class=\"hint\">" + u("simpl") + "</span> " + tex(l.t) + "</p>";
      else if (l.noInd) h += "<p><span class=\"hint\">" + u("notInd") + "</span><br>" + tex(l.t) + "</p>";
      else h += "<p>" + tex(l.t) + "</p>";
    });
    if (H.note) h += '<p class="msg-bad">' + H.note + "</p>";
    return h;
  }
  function numTable(g, P, label) {
    var rows = "", xs = [];
    if (!isFinite(P.a)) [10, 100, 1000, 1e4].forEach(function (k) { xs.push(P.a > 0 ? k : -k); });
    else { [1e-1, 1e-2, 1e-3, 1e-4].forEach(function (k) { if (P.s >= 0) xs.push(P.a + k); }); if (P.s <= 0) [1e-1, 1e-2, 1e-3, 1e-4].forEach(function (k) { xs.push(P.a - k); }); }
    xs.forEach(function (x) { var y = g(x); rows += "<tr><td>" + tex(numTex(+x.toPrecision(6))) + "</td><td>" + tex(isFinite(y) ? numTex(+y.toPrecision(6)) : "\\nexists") + "</td></tr>"; });
    return '<p class="hint">' + u("check") + ":</p>" + '<table class="data sm"><thead><tr><th>' + tex("x") + "</th><th>" + tex(label) + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
  }
  function wHop() {
    var w = document.getElementById("w-hop"); if (!w) return;
    var PRE = [["e^x-1-x", "x^2", "0"], ["x-sin(x)", "x^3", "0"], ["ln(x)", "x", "inf"], ["x^2", "e^x", "inf"], ["tan(x)-x", "x-sin(x)", "0"], ["x^3+3x^2-4", "x^3+5x^2+8x+4", "-2"], ["e^x-x-cos(3x)", "sin(x)^2", "0"], ["x+sin(x)", "x", "inf"]];
    var ni = $(w, "n"), di = $(w, "d"), ai = $(w, "a"), out = $(w, "out"), tb = w.querySelector(".vtbl");
    presetBtns($(w, "presets"), PRE.length, "pHop", function (i) { ni.value = PRE[i][0]; di.value = PRE[i][1]; ai.value = PRE[i][2]; draw(); });
    [ni, di, ai].forEach(function (e) { e.addEventListener("input", draw); });
    function draw() {
      var N, Dd, P = readPt(ai.value);
      try { N = strip0(parse(ni.value)); ni.classList.remove("bad"); } catch (e) { ni.classList.add("bad"); out.textContent = u("bad"); return; }
      try { Dd = strip0(parse(di.value)); di.classList.remove("bad"); } catch (e) { di.classList.add("bad"); out.textContent = u("bad"); return; }
      ai.classList.toggle("bad", !P); if (!P) { out.textContent = u("aErr"); return; }
      var H; try { H = hopital(N, Dd, P); } catch (e) { out.textContent = u("noDiff"); return; }
      out.innerHTML = hopHtml(H);
      var fN = compile(N), fD = compile(Dd);
      tb.innerHTML = numTable(function (x) { return fN(x) / fD(x); }, P, "\\dfrac{" + texD(N) + "}{" + texD(Dd) + "}");
    }
    onLang(draw);
  }
  // altres indeterminacions: transformació i L'Hôpital
  var IND = [
    { e: "x*ln(x)", a: "0+", ty: "0\\cdot\\infty", tr: "x\\ln x=\\dfrac{\\ln x}{\\;1/x\\;}", n: "ln(x)", d: "1/x" },
    { e: "x*(e^(1/x)-1)", a: "inf", ty: "\\infty\\cdot0", tr: "x\\left(e^{1/x}-1\\right)=\\dfrac{e^{1/x}-1}{\\;1/x\\;}", n: "e^(1/x)-1", d: "1/x" },
    { e: "1/x-1/(e^x-1)", a: "0", ty: "\\infty-\\infty", tr: "\\dfrac1x-\\dfrac{1}{e^x-1}=\\dfrac{e^x-1-x}{x\\left(e^x-1\\right)}", n: "e^x-1-x", d: "x*e^x-x" },
    { e: "1/ln(x)-1/(x-1)", a: "1", ty: "\\infty-\\infty", tr: "\\dfrac{1}{\\ln x}-\\dfrac{1}{x-1}=\\dfrac{x-1-\\ln x}{(x-1)\\ln x}", n: "x-1-ln(x)", d: "(x-1)*ln(x)" },
    { e: "(1+x-sin(x))^(1/x^3)", a: "0+", ty: "1^{\\infty}", tr: "\\ln L=\\lim\\dfrac{1}{x^3}\\ln\\left(1+x-\\sin x\\right)=\\lim\\dfrac{\\ln\\left(1+x-\\sin x\\right)}{x^3}", n: "ln(1+x-sin(x))", d: "x^3", ex: true },
    { e: "(e^x+x^3)^(1/x)", a: "0", ty: "1^{\\infty}", tr: "\\ln L=\\lim\\dfrac{\\ln\\left(e^x+x^3\\right)}{x}", n: "ln(e^x+x^3)", d: "x", ex: true },
    { e: "x^(1/x)", a: "inf", ty: "\\infty^{0}", tr: "\\ln L=\\lim\\dfrac1x\\ln x=\\lim\\dfrac{\\ln x}{x}", n: "ln(x)", d: "x", ex: true },
    { e: "x^x", a: "0+", ty: "0^{0}", tr: "\\ln L=\\lim x\\ln x=\\lim\\dfrac{\\ln x}{1/x}", n: "ln(x)", d: "1/x", ex: true },
    { e: "x^(sin(x))", a: "0+", ty: "0^{0}", tr: "\\ln L=\\lim\\,\\sin x\\cdot\\ln x=\\lim\\dfrac{\\ln x}{1/\\sin x}", n: "ln(x)", d: "1/sin(x)", ex: true }
  ];
  function wInd() {
    var w = document.getElementById("w-ind"); if (!w) return;
    var st = 0, out = $(w, "out"), tb = w.querySelector(".vtbl");
    presetBtns($(w, "presets"), IND.length, "pInd", function (i) { st = i; draw(); });
    function draw() {
      var I = IND[st], P = readPt(I.a), e = parse(I.e), at = "\\lim_{x\\to " + P.t + "}";
      var h = "<p>" + tex((I.ex ? "L=" : "") + at + texD(e)) + "</p><p><strong>" + u("type") + ":</strong> " + tex("\\left[" + I.ty + "\\right]") + "</p>";
      if (I.ex) h += "<p>" + rt(u("logT")) + "</p>";
      h += "<p><strong>" + u("trans") + ":</strong> " + tex(I.tr) + "</p>";
      var H = hopital(strip0(parse(I.n)), strip0(parse(I.d)), P);
      h += hopHtml(H);
      if (H.res && H.res.k === "num") {
        var v = Math.abs(H.res.v) < 1e-8 ? 0 : H.res.v;
        h += "<p><strong>" + u("hopRes") + ":</strong> " + (I.ex ? u("backE") + " " + tex("\\ln L=" + nn(v) + "\\ \\Rightarrow\\ L=e^{" + nn(v) + "}" + (Math.abs(v) < 1e-12 ? "=1" : Math.abs(v - 1) < 1e-12 ? "=e" : "")) : tex(at + texD(e) + "=" + nn(v))) + "</p>";
      }
      out.innerHTML = h;
      var g = compile(e); tb.innerHTML = numTable(g, P, texD(e));
    }
    onLang(draw);
  }

  /* ---------- 7.4 monotonia i extrems ---------- */
  function studyWin(n) {
    var f = compile(n), T = periodOf(f, n), S;
    if (T) return studyF(n, 0, T, T);
    S = studyF(n, -XL, XL); S.inf = true;
    if (S.ev.length + S.C.ev.length > 18) { S = studyF(n, -8, 8); S.inf = false; }
    return S;
  }
  function perNote(S) { return S.P ? "<p>" + u("per") + " " + tex("T=" + piTex(S.P)) + ". " + u("perStudy") + " " + tex("[0," + piTex(S.P) + "]") + "</p>" : ""; }
  function wMono() {
    var w = document.getElementById("w-mono"); if (!w) return;
    var PRE = [["x^3-3x"], ["x*e^(1-x^2)"], ["x/ln(x)"], ["(x+1)/(x^2+1)"], ["x+2cos(x)"], ["abs(x^2-4)"], ["x^(2/3)*(x-5)"]];
    var I = fnInput(w, PRE, "pMono", draw), svg = w.querySelector("svg"), info = w.querySelector(".info"), tb = w.querySelector(".vtbl");
    function draw() {
      var n = readF(w, I.fi); if (!n) { tb.innerHTML = ""; return; }
      var S; try { S = studyWin(n); } catch (e) { info.textContent = u("noDiff"); return; }
      var h = "<p>" + tex("f(x)=" + texD(n)) + "</p>" + perNote(S);
      if (S.dn) h += "<p>" + tex("f'(x)=" + texD(S.dn)) + "</p>";
      h += monoHtml(S, S.inf) + extHtml(S, true);
      info.innerHTML = h; tb.innerHTML = signTable(S, S.inf);
      plot(svg, { v: autoView(S, [-5, 5]), curves: monoCurves(S), mark: S.P ? periodic(extMarks(S), S.P, autoView(S, [-5, 5])) : extMarks(S) });
    }
    onLang(draw);
  }
  /* ---------- 7.5 curvatura ---------- */
  function wCurv() {
    var w = document.getElementById("w-curv"); if (!w) return;
    var PRE = [["x^3-3x^2"], ["e^x*(x^2-5x+6)"], ["x-ln(x^2+1)"], ["(x-1)^2/x^2"], ["x+sin(x)"], ["x^(1/3)"], ["x^4"]];
    var I = fnInput(w, PRE, "pCurv", draw), svg = w.querySelector("svg"), info = w.querySelector(".info"), tb = w.querySelector(".vtbl"), rx = $(w, "x"), S = null, v = null;
    rx.addEventListener("input", paint);
    function draw() {
      var n = readF(w, I.fi); if (!n) { tb.innerHTML = ""; return; }
      try { S = studyWin(n); } catch (e) { S = null; info.textContent = u("noDiff"); return; }
      var h = "<p>" + tex("f(x)=" + texD(n)) + "</p>" + perNote(S);
      if (S.d2n) h += "<p>" + tex("f''(x)=" + texD(S.d2n)) + "</p>";
      h += curvHtml(S, S.inf) + inflHtml(S);
      info.innerHTML = h; tb.innerHTML = signTable(S, S.inf, true);
      v = autoView(S, [-5, 5]); rx.min = v[0] + 0.05 * (v[1] - v[0]); rx.max = v[1] - 0.05 * (v[1] - v[0]); rx.step = (v[1] - v[0]) / 400;
      var ip = S.C.ev.filter(function (e) { return e.inf; });
      rx.value = ip.length ? ip[0].x + 0.6 : (v[0] + v[1]) / 2 + 0.7;
      paint();
    }
    function paint() {
      if (!S) return;
      var x = +rx.value, fx = S.f(x), m = S.df(x), cfg = { v: v, curves: curvCurves(S), pts: inflPts(S) };
      var t = $(w, "tt");
      if (isFinite(fx) && isFinite(m)) {
        cfg.curves.push({ f: lineF(m, x, fx), col: "var(--muted)" }); cfg.pts.push({ x: x, y: fx, col: "var(--text)" });
        var d2 = S.d2(x), k = Math.abs(d2) < 1e-6 ? "cross" : d2 > 0 ? "above" : "below";
        t.innerHTML = u("tanAt") + " " + tex("x=" + numTex(+x.toFixed(2))) + ": " + tex("f''=" + numTex(+d2.toPrecision(3))) + " → " + u(k);
      } else t.textContent = "";
      if (S.P) cfg.pts = periodic(cfg.pts.slice(0, -1), S.P, v).concat(cfg.pts.slice(-1));
      plot(svg, cfg);
    }
    onLang(draw);
  }
  /* ---------- 7.6 comprovació de condicions en un punt ---------- */
  function wChk() {
    var w = document.getElementById("w-chk"); if (!w) return;
    var PRE = [["x^3-3x^2+2", "0"], ["x^3-3x^2+2", "1"], ["x^3", "0"], ["x^4", "0"], ["x^5-5x^4", "4"]];
    var I = fnInput(w, PRE, "pChk", draw), info = w.querySelector(".info");
    function draw() {
      var n = readF(w, I.fi); if (!n) return;
      var a = readNum(I.ai.value); I.ai.classList.toggle("bad", !isFinite(a)); if (!isFinite(a)) { info.textContent = u("aBad"); return; }
      var ds = [n], k, at = nn(a);
      try { for (k = 0; k < 5; k++) ds.push(D(ds[k])); } catch (e) { info.textContent = u("noDiff"); return; }
      var vals = ds.map(function (d) { return compile(d)(a); }), names = ["f", "f'", "f''", "f'''", "f^{(4)}", "f^{(5)}"], rows = "";
      vals.forEach(function (v, i) { rows += "<tr><td>" + tex(names[i] + "(x)=" + texD(ds[i])) + "</td><td>" + tex(names[i] + "(" + at + ")=" + (isFinite(v) ? nn(Math.abs(v) < 1e-10 ? 0 : v) : "\\nexists")) + "</td></tr>"; });
      var c;
      if (!isFinite(vals[0])) c = u("noF");
      else if (Math.abs(vals[1]) > 1e-9) c = Math.abs(vals[2]) < 1e-9 ? t3("\\(f'(a)\\neq0\\): no és un punt crític. Com que \\(f''(a)=0\\), cal mirar si \\(f''\\) canvia de signe (seria un punt d'inflexió).", "\\(f'(a)\\neq0\\): no es un punto crítico. Como \\(f''(a)=0\\), hay que mirar si \\(f''\\) cambia de signo (sería un punto de inflexión).", "\\(f'(a)\\neq0\\): not a critical point. Since \\(f''(a)=0\\), check whether \\(f''\\) changes sign (it would be an inflection point).") : t3("\\(f'(a)\\neq0\\): no és un punt crític; la funció és " + (vals[1] > 0 ? "creixent" : "decreixent") + " i " + (vals[2] > 0 ? "convexa" : "còncava") + " en el punt.", "\\(f'(a)\\neq0\\): no es un punto crítico; la función es " + (vals[1] > 0 ? "creciente" : "decreciente") + " y " + (vals[2] > 0 ? "convexa" : "cóncava") + " en el punto.", "\\(f'(a)\\neq0\\): not a critical point; the function is " + (vals[1] > 0 ? "increasing" : "decreasing") + " and " + (vals[2] > 0 ? "convex" : "concave") + " at the point.");
      else {
        // primera derivada no nul·la a partir de la segona
        for (k = 2; k < vals.length && Math.abs(vals[k]) < 1e-9; k++);
        if (k >= vals.length) c = "?";
        else if (k % 2 === 0) c = t3("La primera derivada no nul·la és la d'ordre " + k + " (parell): és un <strong>" + (vals[k] > 0 ? "mínim" : "màxim") + " relatiu</strong>.", "La primera derivada no nula es la de orden " + k + " (par): es un <strong>" + (vals[k] > 0 ? "mínimo" : "máximo") + " relativo</strong>.", "The first non-zero derivative has order " + k + " (even): it is a <strong>relative " + (vals[k] > 0 ? "minimum" : "maximum") + "</strong>.");
        else c = t3("La primera derivada no nul·la és la d'ordre " + k + " (senar): és un <strong>punt d'inflexió amb tangent horitzontal</strong>.", "La primera derivada no nula es la de orden " + k + " (impar): es un <strong>punto de inflexión con tangente horizontal</strong>.", "The first non-zero derivative has order " + k + " (odd): it is an <strong>inflection point with a horizontal tangent</strong>.");
      }
      info.innerHTML = '<table class="data sm kv-tbl"><tbody>' + rows + "</tbody></table><p><strong>" + u("kindPt") + ":</strong> " + rt(c) + "</p>";
    }
    onLang(draw);
  }
  /* ---------- 7.7 teoremes de Rolle i del valor mitjà ---------- */
  function wRolle() {
    var w = document.getElementById("w-rolle"); if (!w) return;
    var PRE = [["x^2-4x+3", "0", "4"], ["x^3-x", "-1", "1"], ["1-x^(2/3)", "-1", "1"], ["(1-x^2)*tan(x)", "0", "1"], ["x^3", "0", "2"], ["ln(x)", "1", "e"], ["sqrt(1-x^2)", "0", "1"], ["x*ln(x^2+1)", "1", "2"]];
    var fi = $(w, "f"), ai = $(w, "a"), bi = $(w, "b"), svg = w.querySelector("svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pRolle", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; bi.value = PRE[i][2]; draw(); });
    [fi, ai, bi].forEach(function (e) { e.addEventListener("input", draw); });
    function ck(b) { return b ? '<span class="msg-ok">✓</span>' : '<span class="msg-bad">✗</span>'; }
    function draw() {
      var n = readF(w, fi); if (!n) return;
      var a = readNum(ai.value), b = readNum(bi.value);
      if (!(isFinite(a) && isFinite(b) && a < b)) { info.textContent = u("ivBad"); return; }
      var R = derivs(n), f = R.f, df = R.df, N = 800, cont = true, der = true, i, x;
      for (i = 0; i <= N; i++) {
        x = a + (b - a) * i / N; var y = f(x);
        if (!isFinite(y)) { cont = false; break; }
        if (i > 0) { var y0 = f(x - (b - a) / N); if (Math.abs(y - y0) > 0.25 * (1 + Math.abs(y))) { var mid = f(x - (b - a) / (2 * N)); if (!(Math.abs(mid - y0) < 0.6 * Math.abs(y - y0) + 1e-9)) { cont = false; break; } } }
      }
      for (i = 1; i < N; i++) { x = a + (b - a) * i / N; if (!isFinite(df(x)) || Math.abs(df(x)) > 1e6) { der = false; break; } }
      if (der) { var S0 = crit(f, df, a + 1e-9, b - 1e-9); S0.ev.forEach(function (e) { if (e.k === "h" || kink(f, e.x)) der = false; }); }
      var fa = f(a), fb = f(b), m = (fb - fa) / (b - a), eq = Math.abs(fb - fa) < 1e-9 * (1 + Math.abs(fa)), A = nn(a), Bt = nn(b);
      var h = "<p>" + tex("f(x)=" + texD(n) + "\\quad\\text{en}\\quad[" + A + "," + Bt + "]") + "</p>";
      if (R.dn) h += "<p>" + tex("f'(x)=" + texD(R.dn)) + "</p>";
      h += "<p><strong>" + u("hyp") + ":</strong><br>" + ck(cont) + " " + rt(u("hypC")) + "<br>" + ck(der) + " " + rt(u("hypD")) + "<br>" + ck(eq) + " " + rt(u("hypE")) + ": " + tex("f(" + A + ")=" + nn(fa) + ",\\ f(" + Bt + ")=" + nn(fb)) + "</p>";
      var mode = eq ? "R" : "L", cs = roots(function (t) { return df(t) - m; }, a + 1e-9 * (b - a), b - 1e-9 * (b - a), 4000).filter(function (t) { return t > a && t < b; });
      h += "<p><strong>" + (mode === "R" ? u("rolleM") : u("lagM")) + "</strong> — " + rt(mode === "R" ? u("thR") : u("thL")) + (mode === "L" ? ": " + tex("\\dfrac{" + nn(fb) + "-" + (fa < 0 ? "\\left(" + nn(fa) + "\\right)" : nn(fa)) + "}{" + Bt + "-" + (a < 0 ? "\\left(" + A + "\\right)" : A) + "}=" + nnA(m)) : "") + "</p>";
      if (!(cont && der)) h += '<p class="msg-bad">' + u("hypFail") + "</p>";
      h += "<p>" + rt(u("cFound")) + ": " + (cs.length ? tex("c=" + cs.map(nnA).join(",\\ c=")) : rt(u("noC"))) + "</p>";
      info.innerHTML = h;
      var pad = (b - a) * 0.25, yy = autoY([f], a - pad, b + pad), cfg = { v: [a - pad, b + pad, yy[0], yy[1]], curves: [{ f: f, a: a, b: b }, { f: f, b: a, col: "var(--muted)" }, { f: f, a: b, col: "var(--muted)" }, { f: lineF(m, a, fa), a: a, b: b, col: "var(--r3)" }], pts: [{ x: a, y: fa }, { x: b, y: fb }], guides: [] };
      cs.forEach(function (c) { var fc = f(c), L = (b - a) * 0.3; cfg.curves.push({ f: lineF(m, c, fc), a: c - L, b: c + L, col: "var(--accent-2)" }); cfg.pts.push({ x: c, y: fc, col: "var(--accent-2)" }); cfg.guides.push({ x: c }); });
      plot(svg, cfg);
    }
    onLang(draw);
  }
  /* ---------- 7.8 extrems absoluts en [a, b] ---------- */
  function wAbs() {
    var w = document.getElementById("w-abs"); if (!w) return;
    var PRE = [["10x^3/3-x^4/4+6", "0", "12"], ["cos(pi*x/9)+2", "0", "12"], ["2cos(x+pi/2)+10", "0", "4"], ["x*sqrt(18-x^2)", "-4", "4"], ["x*e^x", "-3", "1"], ["sin(x)+cos(x)", "0", "2pi"]];
    var fi = $(w, "f"), ai = $(w, "a"), bi = $(w, "b"), svg = w.querySelector("svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pAbs", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; bi.value = PRE[i][2]; draw(); });
    [fi, ai, bi].forEach(function (e) { e.addEventListener("input", draw); });
    function draw() {
      var n = readF(w, fi); if (!n) return;
      var a = readNum(ai.value), b = readNum(bi.value);
      if (!(isFinite(a) && isFinite(b) && a < b)) { info.textContent = u("ivBad"); return; }
      var S = studyF(n, a, b), f = S.f, C = [{ x: a, k: "ends" }];
      S.ev.forEach(function (e) { if (isFinite(e.y) && e.x > a + 1e-9 && e.x < b - 1e-9) C.push({ x: e.x, k: e.k === "z" ? "critIn" : "ndIn" }); });
      C.push({ x: b, k: "ends" });
      C.forEach(function (c) { c.y = f(c.x); });
      var ok = C.filter(function (c) { return isFinite(c.y); }), mx = ok.reduce(function (p, q) { return q.y > p.y + 1e-12 ? q : p; }, ok[0]), mn = ok.reduce(function (p, q) { return q.y < p.y - 1e-12 ? q : p; }, ok[0]);
      var h = "<p>" + tex("f(x)=" + texD(n) + "\\quad\\text{en}\\quad[" + nn(a) + "," + nn(b) + "]") + "</p>";
      if (S.dn) h += "<p>" + tex("f'(x)=" + texD(S.dn)) + "</p>";
      h += '<table class="data sm"><thead><tr><th>' + u("cand") + "</th><th>" + tex("x") + "</th><th>" + tex("f(x)") + "</th></tr></thead><tbody>";
      C.forEach(function (c) { var cl = Math.abs(c.y - mx.y) < 1e-9 * (1 + Math.abs(mx.y)) ? ' class="v-mx"' : Math.abs(c.y - mn.y) < 1e-9 * (1 + Math.abs(mn.y)) ? ' class="v-mn"' : ""; h += "<tr><td>" + u(c.k) + "</td><td>" + tex(nn(c.x)) + "</td><td" + cl + ">" + tex(isFinite(c.y) ? nnA(c.y) : "\\nexists") + "</td></tr>"; });
      h += "</tbody></table>";
      h += '<p><span class="badge ok">' + u("absMax") + "</span> " + tex(ptTex(mx.x, mx.y)) + "<br>" + '<span class="badge as">' + u("absMin") + "</span> " + tex(ptTex(mn.x, mn.y)) + "</p>";
      info.innerHTML = h;
      var pad = (b - a) * 0.08, yy = autoY([f], a, b);
      plot(svg, { v: [a - pad, b + pad, Math.min(yy[0], mn.y - 0.1 * (mx.y - mn.y + 1)), Math.max(yy[1], mx.y + 0.1 * (mx.y - mn.y + 1))], curves: [{ f: f, a: a, b: b }], guides: [{ x: a }, { x: b }], mark: [{ x: mx.x, y: mx.y, col: "var(--ok)" }, { x: mn.x, y: mn.y, col: "var(--bad)" }] });
    }
    onLang(draw);
  }

  /* ---------- 7.9 optimització: construïm la funció (dibuix + gràfica) ---------- */
  function P2(x, y) { return { x: +x.toFixed(1), y: +y.toFixed(1) }; }
  function ln2(p, q, cls) { return '<line class="' + cls + '" x1="' + p.x + '" y1="' + p.y + '" x2="' + q.x + '" y2="' + q.y + '"/>'; }
  function poly(ps, cls) { return '<polygon class="' + cls + '" points="' + ps.map(function (p) { return p.x + "," + p.y; }).join(" ") + '"/>'; }
  function pline(ps, cls) { return '<polyline class="' + cls + '" points="' + ps.map(function (p) { return p.x + "," + p.y; }).join(" ") + '"/>'; }
  function txt(x, y, s, anchor, cls) { return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="' + (anchor || "middle") + '"' + (cls ? ' class="' + cls + '"' : "") + ">" + s + "</text>"; }
  function dot(p, cls) { return '<circle class="' + (cls || "dt") + '" cx="' + p.x + '" cy="' + p.y + '" r="4.5"/>'; }
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
  function nt2(v) { return numTxt(+v.toFixed(2)); }
  var BUILD = [
    { e: "10x-(1/2+pi/8)*x^2", fn: "A", dom: [0.2, 7.6], step: 0.02, x: 2, v: [0, 8, 0, 32], kind: "max",
      head: function () { return tex("x+2y+\\dfrac{\\pi x}{2}=20\\Rightarrow y=10-\\dfrac x2-\\dfrac{\\pi x}{4}") + "<br>" + tex("A(x)=xy+\\dfrac{\\pi x^2}{8}=10x-\\left(\\dfrac12+\\dfrac{\\pi}{8}\\right)x^2"); },
      draw: function (x) {
        var y = 10 - x / 2 - Math.PI * x / 4, s = 24, cx = 210, by = 268, L = P2(cx - x * s / 2, by), R = P2(cx + x * s / 2, by), tl = P2(cx - x * s / 2, by - y * s), tr = P2(cx + x * s / 2, by - y * s), r = x * s / 2;
        var g = '<path class="area" d="M' + L.x + "," + L.y + " L" + tl.x + "," + tl.y + " A" + r.toFixed(1) + "," + r.toFixed(1) + " 0 0 1 " + tr.x + "," + tr.y + " L" + R.x + "," + R.y + ' Z"/>';
        g += ln2(tl, tr, "fold") + txt(cx, by + 20, "x = " + nt2(x), "middle") + txt(L.x - 6, (by + tl.y) / 2 + 4, "y = " + nt2(y), "end") + txt(cx, tl.y - r / 2 + 5, "r = x/2", "middle", "sm");
        return g;
      },
      info: function (x) { var y = 10 - x / 2 - Math.PI * x / 4; return tex("x=" + r2(x) + "\\text{ m},\\ y=" + r2(y) + "\\text{ m},\\ A=" + r2(10 * x - (0.5 + Math.PI / 8) * x * x) + "\\text{ m}^2"); }, unit: "\\text{ m}^2" },
    { e: "2x(12-x^2)", fn: "A", dom: [0.05, 3.45], step: 0.01, x: 1, v: [0, 3.6, 0, 36], kind: "max",
      head: function () { return tex(t3("\\text{base }2x,\\ \\text{altura }12-x^2", "\\text{base }2x,\\ \\text{altura }12-x^2", "\\text{base }2x,\\ \\text{height }12-x^2")) + "&emsp;" + tex("A(x)=2x\\left(12-x^2\\right)"); },
      draw: function (x) {
        var sx = 52, sy = 21, ox = 210, oy = 280, pts = [], t;
        for (t = -Math.sqrt(12); t <= Math.sqrt(12) + 1e-9; t += 0.05) pts.push(P2(ox + t * sx, oy - (12 - t * t) * sy));
        pts.push(P2(ox + Math.sqrt(12) * sx, oy));
        var h = 12 - x * x, g = '<rect class="sheet" x="' + (ox - 3.7 * sx).toFixed(1) + '" y="' + (oy - 12.8 * sy).toFixed(1) + '" width="' + (7.4 * sx).toFixed(1) + '" height="' + (12.8 * sy).toFixed(1) + '"/>';
        g += '<polygon class="top" points="' + pts.map(function (p) { return p.x + "," + p.y; }).join(" ") + '"/>' + pline(pts, "ed");
        g += '<rect class="area" x="' + (ox - x * sx).toFixed(1) + '" y="' + (oy - h * sy).toFixed(1) + '" width="' + (2 * x * sx).toFixed(1) + '" height="' + (h * sy).toFixed(1) + '"/>';
        g += ln2(P2(ox - 3.9 * sx, oy), P2(ox + 3.9 * sx, oy), "axl") + txt(ox, oy + 16, "2x = " + nt2(2 * x)) + txt(ox - x * sx - 6, oy - h * sy / 2, nt2(h), "end") + txt(ox + 2.6 * sx, oy - 9.5 * sy, "y = 12 − x²", "middle", "sm");
        return g;
      },
      info: function (x) { return tex("x=" + r2(x) + ",\\ " + t3("\\text{base}", "\\text{base}", "\\text{base}") + "=" + r2(2 * x) + "\\text{ m},\\ " + t3("\\text{altura}", "\\text{altura}", "\\text{height}") + "=" + r2(12 - x * x) + "\\text{ m},\\ A=" + r2(2 * x * (12 - x * x)) + "\\text{ m}^2"); }, unit: "\\text{ m}^2" },
    { e: "x(16-2x)(10-2x)", fn: "V", dom: [0.1, 4.9], step: 0.02, x: 1, v: [0, 5, 0, 160], kind: "max",
      head: function () { return tex("V(x)=x\\,(16-2x)(10-2x)"); },
      draw: function (x) {
        var s = 10.5, ox = 26, oy = 76, Lw = 16, Lh = 10, g = "";
        g += '<rect class="sheet" x="' + ox + '" y="' + oy + '" width="' + Lw * s + '" height="' + Lh * s + '"/>';
        [[0, 0], [Lw - x, 0], [0, Lh - x], [Lw - x, Lh - x]].forEach(function (q) { g += '<rect class="cut" x="' + (ox + q[0] * s).toFixed(1) + '" y="' + (oy + q[1] * s).toFixed(1) + '" width="' + (x * s).toFixed(1) + '" height="' + (x * s).toFixed(1) + '"/>'; });
        g += '<rect class="fold" x="' + (ox + x * s).toFixed(1) + '" y="' + (oy + x * s).toFixed(1) + '" width="' + ((Lw - 2 * x) * s).toFixed(1) + '" height="' + ((Lh - 2 * x) * s).toFixed(1) + '"/>';
        g += txt(ox + x * s / 2, oy - 6, "x") + txt(ox + Lw * s / 2, oy + Lh * s + 18, "16 cm") + txt(ox - 4, oy + Lh * s / 2, "10", "end");
        var bw = Lw - 2 * x, bd = Lh - 2 * x, c = Math.cos(Math.PI / 6) * 0.45, si = Math.sin(Math.PI / 6) * 0.45, sb = Math.min(170 / (bw + bd * c), 180 / (x + bd * si));
        g += prism(222 + (180 - (bw + bd * c) * sb) / 2, 170 + (x + bd * si) * sb / 2, bw, bd, x, sb, [nt2(bw), nt2(bd), nt2(x)]);
        return g;
      },
      info: function (x) { return tex("x=" + r2(x) + "\\text{ cm},\\ " + r2(16 - 2 * x) + "\\times" + r2(10 - 2 * x) + "\\times" + r2(x) + ",\\ V=" + r2(x * (16 - 2 * x) * (10 - 2 * x)) + "\\text{ cm}^3"); }, unit: "\\text{ cm}^3" },
    { e: "-5/4*x^2+60x+3200", fn: "A", dom: [0, 32], step: 0.1, x: 8, v: [-1, 33, 3000, 4000], kind: "max",
      head: function () { return tex("y=40-\\dfrac{5}{4}x") + "&emsp;" + tex("A(x)=(80-x)(80-y)=-\\dfrac54x^2+60x+3200"); },
      draw: function (x) {
        var s = 3.2, ox = 60, oy = 284, y = 40 - 1.25 * x, Pq = function (a, b) { return P2(ox + a * s, oy - b * s); }, g = "";
        g += poly([Pq(32, 0), Pq(80, 0), Pq(80, 80), Pq(0, 80), Pq(0, 40)], "sheet") + poly([Pq(0, 0), Pq(32, 0), Pq(0, 40)], "cut");
        g += poly([Pq(x, y), Pq(80, y), Pq(80, 80), Pq(x, 80)], "area") + dot(Pq(x, y));
        g += txt(ox + 16 * s, oy + 16, "32") + txt(ox - 6, oy - 20 * s, "40", "end") + txt(ox + x * s + 6, oy - y * s + 16, "(x, y)", "start", "sm");
        g += txt(ox + (x + 80) / 2 * s, oy - 82 * s - 2 + 4, "80 − x = " + nt2(80 - x), "middle") + txt(ox + 80 * s + 6, oy - (y + 80) / 2 * s, nt2(80 - y), "start");
        return g;
      },
      info: function (x) { var y = 40 - 1.25 * x; return tex("x=" + r2(x) + ",\\ y=" + r2(y) + ",\\ " + r2(80 - x) + "\\times" + r2(80 - y) + ",\\ A=" + r2((80 - x) * (80 - y)) + "\\text{ cm}^2"); }, unit: "\\text{ cm}^2" },
    { e: "10sqrt(x^2+36)+5(18-x)", fn: "C", dom: [0, 18], step: 0.05, x: 9, v: [-0.5, 18.5, 120, 200], kind: "min",
      head: function () { return tex("\\overline{MP}=\\sqrt{x^2+36},\\ \\overline{PN}=18-x") + "<br>" + tex("C(x)=10\\sqrt{x^2+36}+5(18-x)"); },
      draw: function (x) {
        var s = 20, ox = 30, oy = 200, Pq = function (a, b) { return P2(ox + a * s, oy - b * s); }, g = "";
        g += '<rect class="river" x="6" y="' + (oy - 6 * s) + '" width="408" height="' + 6 * s + '"/>' + txt(380, oy - 3 * s + 4, t3("carrer", "calle", "street"), "middle", "sm");
        g += ln2(P2(6, oy), P2(414, oy), "axl") + ln2(P2(6, oy - 6 * s), P2(414, oy - 6 * s), "axl");
        g += '<line class="fence" x1="' + Pq(0, 6).x + '" y1="' + Pq(0, 6).y + '" x2="' + Pq(x, 0).x + '" y2="' + Pq(x, 0).y + '"/>' + ln2(Pq(x, 0), Pq(18, 0), "ed");
        g += dot(Pq(0, 6)) + dot(Pq(x, 0)) + dot(Pq(18, 0));
        g += txt(Pq(0, 6).x, Pq(0, 6).y - 10, "M") + txt(Pq(x, 0).x, oy + 18, "P (x = " + nt2(x) + ")") + txt(Pq(18, 0).x, oy + 18, "N") + txt(Pq(x / 2, 3).x + 10, Pq(x / 2, 3).y, "10 €/m", "start", "sm") + txt(Pq((x + 18) / 2, 0).x, oy - 8, "5 €/m", "middle", "sm");
        return g;
      },
      info: function (x) { return tex("x=" + r2(x) + "\\text{ m},\\ C=" + r2(10 * Math.sqrt(x * x + 36) + 5 * (18 - x)) + "\\text{ €}"); }, unit: "\\text{ €}" },
    { e: "sqrt(x^2+4)/4+(10-x)/12", fn: "t", dom: [0, 10], step: 0.02, x: 4, v: [-0.3, 10.3, 1.2, 2.8], kind: "min",
      head: function () { return tex("t(x)=\\dfrac{\\sqrt{x^2+4}}{4}+\\dfrac{10-x}{12}") + "&emsp;" + tex(t3("(\\text{nedant a 4 km/h, corrent a 12 km/h})", "(\\text{nadando a 4 km/h, corriendo a 12 km/h})", "(\\text{swimming at 4 km/h, running at 12 km/h})")); },
      draw: function (x) {
        var s = 34, ox = 40, oy = 110, Pq = function (a, b) { return P2(ox + a * s, oy - b * s); }, g = "";
        g += '<rect class="river" x="6" y="' + oy + '" width="408" height="' + 2 * s + '"/>' + ln2(P2(6, oy), P2(414, oy), "axl") + ln2(P2(6, oy + 2 * s), P2(414, oy + 2 * s), "axl");
        g += '<line class="fence" x1="' + Pq(0, -2).x + '" y1="' + Pq(0, -2).y + '" x2="' + Pq(x, 0).x + '" y2="' + Pq(x, 0).y + '"/>' + '<line class="fence" style="stroke:var(--ok)" x1="' + Pq(x, 0).x + '" y1="' + oy + '" x2="' + Pq(10, 0).x + '" y2="' + oy + '"/>';
        g += dot(Pq(0, -2)) + dot(Pq(0, 0)) + dot(Pq(x, 0)) + dot(Pq(10, 0));
        g += txt(Pq(0, -2).x - 8, Pq(0, -2).y + 4, "A", "end") + txt(Pq(0, 0).x, oy - 10, "C") + txt(Pq(x, 0).x, oy - 10, "D") + txt(Pq(10, 0).x, oy - 10, "B") + txt(Pq(x / 2, 0).x, oy - 26, "x = " + nt2(x), "middle", "sm") + txt(ox - 8, oy + s + 4, "2 km", "end", "sm") + txt(Pq(5, 0).x, oy + 2 * s + 34, "CB = 10 km", "middle", "sm");
        return g;
      },
      info: function (x) { var t = Math.sqrt(x * x + 4) / 4 + (10 - x) / 12; return tex("x=" + r2(x) + "\\text{ km},\\ t=" + numTex(+t.toFixed(4)) + "\\text{ h}\\approx" + Math.floor(t) + "\\text{ h }" + Math.round((t - Math.floor(t)) * 60) + "\\text{ min}"); }, unit: "\\text{ h}" },
    { e: "24x-24/5*x^2", fn: "A", dom: [0.05, 4.95], step: 0.01, x: 1, v: [0, 5, 0, 35], kind: "max",
      head: function () { return tex("\\overline{AC}:\\ y=12-\\dfrac{12}{5}x") + "&emsp;" + tex("A(x)=2x\\left(12-\\dfrac{12}{5}x\\right)"); },
      draw: function (x) {
        var s = 21, ox = 210, oy = 270, Pq = function (a, b) { return P2(ox + a * s, oy - b * s); }, h = 12 - 12 * x / 5, g = "";
        g += poly([Pq(-5, 0), Pq(5, 0), Pq(0, 12)], "top") + poly([Pq(-5, 0), Pq(5, 0), Pq(0, 12)], "ed");
        g += poly([Pq(-x, 0), Pq(x, 0), Pq(x, h), Pq(-x, h)], "area");
        g += txt(Pq(0, 12).x, Pq(0, 12).y - 6, "A(0, 12)") + txt(Pq(-5, 0).x, oy + 16, "B(−5, 0)") + txt(Pq(5, 0).x, oy + 16, "C(5, 0)") + txt(ox, oy + 16, "2x = " + nt2(2 * x), "middle", "sm") + txt(Pq(x, h / 2).x + 6, Pq(x, h / 2).y, nt2(h), "start");
        return g;
      },
      info: function (x) { var h = 12 - 12 * x / 5; return tex("x=" + r2(x) + ",\\ " + r2(2 * x) + "\\times" + r2(h) + ",\\ A=" + r2(2 * x * h) + "\\text{ u}^2"); }, unit: "\\text{ u}^2" }
  ];
  function optOf(f, df, dom, kind) {
    var c = [dom[0], dom[1]].concat(roots(df, dom[0], dom[1]));
    var best = null;
    c.forEach(function (x) { var y = f(x); if (!isFinite(y)) return; if (!best || (kind === "max" ? y > best.y : y < best.y)) best = { x: x, y: y }; });
    return best;
  }
  function wOpt() {
    var w = document.getElementById("w-opt"); if (!w) return;
    var st = 0, rx = $(w, "x"), dr = $(w, "draw"), gr = $(w, "graph"), fn = $(w, "fn"), out = w.querySelector(".opt-out"), P, f, df, dn, best;
    presetBtns($(w, "presets"), BUILD.length, "pOpt", function (i) { st = i; setup(); });
    rx.addEventListener("input", draw);
    $(w, "show").addEventListener("click", function () { rx.value = best.x; draw(); });
    function setup() {
      P = BUILD[st]; var n = parse(P.e); f = compile(n); dn = D(n); df = compile(dn); best = optOf(f, df, P.dom, P.kind);
      rx.min = P.dom[0]; rx.max = P.dom[1]; rx.step = P.step; rx.value = P.x;
      $(w, "show").textContent = u("show");
      draw();
    }
    function draw() {
      var x = +rx.value, y = f(x);
      $(w, "xv").textContent = numTxt(x);
      fn.innerHTML = P.head() + "<br>" + tex(P.fn + "'(x)=" + texD(dn));
      dr.setAttribute("viewBox", "0 0 420 300"); dr.innerHTML = P.draw(x);
      var h = "<p>" + P.info(x) + "</p>";
      if (Math.abs(x - best.x) < P.step * 0.6) h += '<p class="msg-ok">✓ ' + u("found") + " " + u(P.kind === "max" ? "optMax" : "optMin") + " " + tex("x=" + nnA(best.x)) + ": " + tex(P.fn + "=" + nnA(best.y) + P.unit) + "</p>";
      out.innerHTML = h;
      plot(gr, { v: P.v, curves: [{ f: f, a: P.dom[0], b: P.dom[1] }], pts: [{ x: x, y: y }], guides: [{ x: x, y: y }] });
    }
    onLang(setup);
  }

  /* ---------- estudi complet pas a pas (7.10–7.12 i calculadora) ---------- */
  var NSTEP = 7;
  function wStudy(id, PRE, key) {
    var w = document.getElementById(id); if (!w) return;
    var fi = $(w, "f"), out = $(w, "out"), tb = $(w, "tbl"), svg = w.querySelector("svg.lp-svg"), bn = $(w, "nx"), ba = $(w, "al"), cnt = $(w, "cnt"), R = null, shown = 1;
    presetBtns($(w, "presets"), PRE.length, key, function (i) { fi.value = PRE[i]; setup(); });
    fi.addEventListener("input", setup);
    bn.addEventListener("click", function () { if (shown < NSTEP) { shown++; draw(); } });
    ba.addEventListener("click", function () { shown = shown >= NSTEP ? 1 : NSTEP; draw(); });
    function setup() {
      shown = 1;
      try { R = fullStudy(strip0(parse(fi.value))); fi.classList.remove("bad"); }
      catch (e) { R = null; fi.classList.add("bad"); out.textContent = e instanceof NoDiff ? u("noDiff") : u("bad"); tb.innerHTML = ""; return; }
      draw();
    }
    function row(i, html) { return '<div class="rs' + (i === shown - 1 ? " now" : "") + '"><h4>' + (i + 1) + ". " + u("sNames")[i] + "</h4>" + html + "</div>"; }
    function draw() {
      if (!R) return;
      var names = u("sNames"), rows = [], S = R.S, T = R.T;
      rows.push(row(0, (R.Dm.iv.length ? tex("\\mathrm{Dom}\\,f=" + domTex(R.Dm, T)) + (T && !/k/.test(domTex(R.Dm, T)) && domTex(R.Dm, T) !== "\\mathbb R" ? " (" + u("inPer") + ")" : "") : u("empty")) + '<div class="why">' + domWhy(R.n, T) + "</div>"));
      if (shown > 1) rows.push(row(1, "<p>" + symTxt(R.sym) + (R.sym === "even" ? " — " + tex("f(-x)=f(x)") : R.sym === "odd" ? " — " + tex("f(-x)=-f(x)") : "") + ".<br>" + (T ? u("per") + " " + tex("T=" + piTex(T)) + ": " + tex("f(x+" + piTex(T) + ")=f(x)") + ". " + u("perStudy") + " " + tex("[0," + piTex(T) + "]") : u("notPer")) + "</p>"));
      if (shown > 2) rows.push(row(2, cutsHtml(R.cuts)));
      if (shown > 3) rows.push(row(3, asyHtml(R.A, R.poly)));
      if (shown > 4) rows.push(row(4, (S.dn ? "<p>" + tex("f'(x)=" + texD(S.dn)) + "</p>" : "") + monoHtml(S, R.inf) + extHtml(S)));
      if (shown > 5) rows.push(row(5, (S.d2n ? "<p>" + tex("f''(x)=" + texD(S.d2n)) + "</p>" : "") + curvHtml(S, R.inf) + inflHtml(S)));
      if (shown > 6) rows.push(row(6, "✓"));
      out.innerHTML = "<p>" + tex("f(x)=" + texD(R.n)) + "</p>" + rows.join("");
      tb.innerHTML = (shown > 4 ? signTable(S, R.inf) : "") + (shown > 5 ? signTable(S, R.inf, true) : "");
      bn.textContent = u("next") + " →"; bn.disabled = shown >= NSTEP;
      ba.textContent = shown >= NSTEP ? u("reset") : u("all");
      cnt.textContent = u("step") + " " + shown + " " + u("of") + " " + NSTEP + " · " + names[shown - 1];
      var cfg = { v: R.view, band: domBands(R.Dm), curves: [], pts: [], mark: [] };
      if (shown > 2) cfg.pts = cutPts(R.cuts, R.view);
      if (shown > 3) Object.assign(cfg, asyPlot(R.A, R.view));
      if (shown > 4) cfg.mark = extMarks(S);
      if (shown > 5) cfg.mark = cfg.mark.concat(inflPts(S).map(function (p) { return { x: p.x, y: p.y, col: "var(--plus)" }; }));
      if (T) cfg.mark = periodic(cfg.mark, T, R.view);
      if (shown > 6) cfg.curves = T ? [{ f: R.f }] : monoCurves(S);
      plot(svg, cfg);
    }
    onLang(setup);
  }
  function wStudies() {
    wStudy("w-r1", ["x^4-2x^2", "x^3/(1-x^2)", "(x+1)/(x^2+1)", "x^3/(1+x)^2", "(x^2+3)/(x^2-4)"], "pR1");
    wStudy("w-r2", ["x/sqrt(x^2-1)", "x*e^(-2x^2)", "2ln(x)/x", "x^2*e^(-x)", "sqrt(x^2-4x)"], "pR2");
    wStudy("w-r3", ["2sin(x)+sin(2x)", "x+sin(x)", "cos(pi*x/9)+2", "sin(x)^2", "tan(x)", "e^(sin(x))"], "pR3");
    wStudy("w-lab", ["x^3-3x", "x^2/(x-2)", "x*e^(-x^2)", "ln(x)/x", "sqrt(x^2-1)", "x+2cos(x)", "abs(x^2-4)"], "pLab");
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("$\\displaystyle\\lim_{x\\to0}\\frac{1-\\cos x}{x^2}$ val…", "$\\displaystyle\\lim_{x\\to0}\\frac{1-\\cos x}{x^2}$ vale…", "$\\displaystyle\\lim_{x\\to0}\\frac{1-\\cos x}{x^2}$ equals…"),
      o: [q3("$0$"), q3("$\\frac12$"), q3("$1$")], a: 1, e: q3("$\\left[\\frac00\\right]$: L'Hôpital dues vegades, $\\frac{\\sin x}{2x}\\to\\frac{\\cos x}{2}\\to\\frac12$.", "$\\left[\\frac00\\right]$: L'Hôpital dos veces, $\\frac{\\sin x}{2x}\\to\\frac{\\cos x}{2}\\to\\frac12$.", "$\\left[\\frac00\\right]$: L'Hôpital twice, $\\frac{\\sin x}{2x}\\to\\frac{\\cos x}{2}\\to\\frac12$.") },
    { q: q3("En aplicar L'Hôpital a $\\dfrac{f}{g}$, derivem…", "Al aplicar L'Hôpital a $\\dfrac{f}{g}$, derivamos…", "When applying L'Hôpital to $\\dfrac{f}{g}$, we differentiate…"),
      o: [q3("el quocient amb la regla del quocient", "el cociente con la regla del cociente", "the quotient with the quotient rule"), q3("el numerador i el denominador per separat", "el numerador y el denominador por separado", "the numerator and the denominator separately"), q3("només el numerador", "solo el numerador", "only the numerator")], a: 1,
      e: q3("$\\lim\\frac fg=\\lim\\frac{f'}{g'}$, sempre que siga $\\left[\\frac00\\right]$ o $\\left[\\frac\\infty\\infty\\right]$.", "$\\lim\\frac fg=\\lim\\frac{f'}{g'}$, siempre que sea $\\left[\\frac00\\right]$ o $\\left[\\frac\\infty\\infty\\right]$.", "$\\lim\\frac fg=\\lim\\frac{f'}{g'}$, provided it is $\\left[\\frac00\\right]$ or $\\left[\\frac\\infty\\infty\\right]$.") },
    { q: q3("$\\displaystyle\\lim_{x\\to0^+}x\\ln x$ és del tipus… i val…", "$\\displaystyle\\lim_{x\\to0^+}x\\ln x$ es del tipo… y vale…", "$\\displaystyle\\lim_{x\\to0^+}x\\ln x$ is of type… and equals…"),
      o: [q3("$0\\cdot\\infty$; val $0$", "$0\\cdot\\infty$; vale $0$", "$0\\cdot\\infty$; it is $0$"), q3("$0\\cdot\\infty$; val $-\\infty$", "$0\\cdot\\infty$; vale $-\\infty$", "$0\\cdot\\infty$; it is $-\\infty$"), q3("no és indeterminat", "no es indeterminado", "it is not indeterminate")], a: 0,
      e: q3("$x\\ln x=\\frac{\\ln x}{1/x}\\to\\frac{1/x}{-1/x^2}=-x\\to0$.") },
    { q: q3("$\\displaystyle\\lim_{x\\to0}(1+2x)^{1/x}$ val…", "$\\displaystyle\\lim_{x\\to0}(1+2x)^{1/x}$ vale…", "$\\displaystyle\\lim_{x\\to0}(1+2x)^{1/x}$ equals…"),
      o: [q3("$1$"), q3("$e$"), q3("$e^2$")], a: 2, e: q3("$\\left[1^\\infty\\right]$: $\\ln L=\\lim\\frac{\\ln(1+2x)}{x}=\\lim\\frac{2/(1+2x)}{1}=2$.") },
    { q: q3("Si $f'(a)=0$ i $f''(a)\\lt0$, en $x=a$ hi ha…", "Si $f'(a)=0$ y $f''(a)\\lt0$, en $x=a$ hay…", "If $f'(a)=0$ and $f''(a)\\lt0$, at $x=a$ there is…"),
      o: [q3("un mínim relatiu", "un mínimo relativo", "a relative minimum"), q3("un màxim relatiu", "un máximo relativo", "a relative maximum"), q3("un punt d'inflexió", "un punto de inflexión", "an inflection point")], a: 1,
      e: q3("La funció és còncava $\\cap$ al voltant del punt crític: és un màxim.", "La función es cóncava $\\cap$ alrededor del punto crítico: es un máximo.", "The function is concave $\\cap$ around the critical point: it is a maximum.") },
    { q: q3("$f(x)=x^3$ en $x=0$ té…", "$f(x)=x^3$ en $x=0$ tiene…", "$f(x)=x^3$ at $x=0$ has…"),
      o: [q3("un mínim", "un mínimo", "a minimum"), q3("un punt d'inflexió amb tangent horitzontal", "un punto de inflexión con tangente horizontal", "an inflection point with a horizontal tangent"), q3("un màxim", "un máximo", "a maximum")], a: 1,
      e: q3("$f'(0)=f''(0)=0$ i $f'''(0)=6\\neq0$ (ordre senar).", "$f'(0)=f''(0)=0$ y $f'''(0)=6\\neq0$ (orden impar).", "$f'(0)=f''(0)=0$ and $f'''(0)=6\\neq0$ (odd order).") },
    { q: q3("Si $f''(x)\\gt0$ en un interval, la gràfica hi és…", "Si $f''(x)\\gt0$ en un intervalo, la gráfica es…", "If $f''(x)\\gt0$ on an interval, the graph there is…"),
      o: [q3("convexa $\\cup$ (per damunt de les tangents)", "convexa $\\cup$ (por encima de las tangentes)", "convex $\\cup$ (above its tangents)"), q3("còncava $\\cap$", "cóncava $\\cap$", "concave $\\cap$"), q3("creixent", "creciente", "increasing")], a: 0,
      e: q3("$f''\\gt0$: $f'$ creix i la corba queda per damunt de les tangents. (Alguns llibres l'anomenen «còncava cap amunt».)", "$f''\\gt0$: $f'$ crece y la curva queda por encima de las tangentes. (Algunos libros la llaman «cóncava hacia arriba».)", "$f''\\gt0$: $f'$ increases and the curve lies above its tangents (also called «concave up»).") },
    { q: q3("Es pot aplicar el teorema de Rolle a $f(x)=|x|$ en $[-1,1]$?", "¿Se puede aplicar el teorema de Rolle a $f(x)=|x|$ en $[-1,1]$?", "Can Rolle's theorem be applied to $f(x)=|x|$ on $[-1,1]$?"),
      o: [q3("Sí, i $c=0$", "Sí, y $c=0$", "Yes, with $c=0$"), q3("No: no és derivable en $x=0$", "No: no es derivable en $x=0$", "No: it is not differentiable at $x=0$"), q3("No: $f(-1)\\neq f(1)$", "No: $f(-1)\\neq f(1)$", "No: $f(-1)\\neq f(1)$")], a: 1,
      e: q3("És contínua i $f(-1)=f(1)$, però té un punt anguló en 0; de fet, $f'$ no s'anul·la mai.", "Es continua y $f(-1)=f(1)$, pero tiene un punto anguloso en 0; de hecho, $f'$ no se anula nunca.", "It is continuous and $f(-1)=f(1)$, but it has a corner at 0; in fact $f'$ never vanishes.") },
    { q: q3("El valor $c$ del teorema del valor mitjà per a $f(x)=x^2$ en $[0,2]$ és…", "El valor $c$ del teorema del valor medio para $f(x)=x^2$ en $[0,2]$ es…", "The value $c$ of the mean value theorem for $f(x)=x^2$ on $[0,2]$ is…"),
      o: [q3("$c=1$"), q3("$c=\\sqrt2$"), q3("$c=2$")], a: 0, e: q3("$\\frac{f(2)-f(0)}{2}=2=f'(c)=2c\\Rightarrow c=1$.") },
    { q: q3("Per a trobar els extrems absoluts d'una funció contínua en $[a,b]$, comparem els valors de $f$…", "Para hallar los extremos absolutos de una función continua en $[a,b]$, comparamos los valores de $f$…", "To find the absolute extrema of a continuous function on $[a,b]$, we compare the values of $f$…"),
      o: [q3("només en els punts crítics", "solo en los puntos críticos", "only at the critical points"), q3("en $a$, en $b$, en els punts crítics i en els no derivables", "en $a$, en $b$, en los puntos críticos y en los no derivables", "at $a$, at $b$, at the critical points and at the non-differentiable points"), q3("només en $a$ i en $b$", "solo en $a$ y en $b$", "only at $a$ and $b$")], a: 1,
      e: q3("Pel teorema de Weierstrass existeixen, i només poden estar en aquests candidats.", "Por el teorema de Weierstrass existen, y solo pueden estar en esos candidatos.", "By the extreme value theorem they exist, and they can only be at those candidates.") },
    { q: q3("L'asímptota obliqua de $f(x)=\\dfrac{x^2+1}{x}$ és…", "La asíntota oblicua de $f(x)=\\dfrac{x^2+1}{x}$ es…", "The oblique asymptote of $f(x)=\\dfrac{x^2+1}{x}$ is…"),
      o: [q3("$y=x$"), q3("$y=x+1$"), q3("$y=1$")], a: 0, e: q3("$f(x)=x+\\frac1x$: $m=1$, $n=\\lim(f(x)-x)=0$.") },
    { q: q3("El període de $f(x)=\\sin(2x)+\\cos(2x)$ és…", "El periodo de $f(x)=\\sin(2x)+\\cos(2x)$ es…", "The period of $f(x)=\\sin(2x)+\\cos(2x)$ is…"),
      o: [q3("$2\\pi$"), q3("$\\pi$"), q3("$\\frac\\pi2$")], a: 1, e: q3("$\\sin(2(x+\\pi))=\\sin(2x+2\\pi)=\\sin 2x$: n'hi ha prou d'estudiar-la en $[0,\\pi]$.", "$\\sin(2(x+\\pi))=\\sin(2x+2\\pi)=\\sin 2x$: basta con estudiarla en $[0,\\pi]$.", "$\\sin(2(x+\\pi))=\\sin(2x+2\\pi)=\\sin 2x$: it is enough to study it on $[0,\\pi]$.") },
    { q: q3("Una caixa sense tapa de base quadrada té volum $32$. La superfície que cal minimitzar és…", "Una caja sin tapa de base cuadrada tiene volumen $32$. La superficie que hay que minimizar es…", "An open box with a square base has volume $32$. The surface to be minimised is…"),
      o: [q3("$S(x)=2x^2+\\dfrac{128}{x}$"), q3("$S(x)=x^2+\\dfrac{128}{x}$"), q3("$S(x)=x^2+\\dfrac{32}{x}$")], a: 1, e: q3("$x^2y=32$; base $x^2$ i quatre cares laterals $4xy=\\frac{128}{x}$.", "$x^2y=32$; base $x^2$ y cuatro caras laterales $4xy=\\frac{128}{x}$.", "$x^2y=32$; base $x^2$ and four sides $4xy=\\frac{128}{x}$.") }
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
      document.querySelectorAll(".widget .wt, .widget label, .widget .ttl, .widget .legend, .lab label, .lab .legend").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wFigs, wStudyFigs, wTn, wTp, wHop, wInd, wMono, wCurv, wChk, wRolle, wAbs, wOpt, wStudies, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM7 = { parse: parse, D: D, texD: texD, compile: compile, fullStudy: fullStudy, studyF: studyF, hopital: hopital, readPt: readPt, nn: nn };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
