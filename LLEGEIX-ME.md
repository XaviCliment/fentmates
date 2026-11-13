# FentMates — guia ràpida

Web estàtica (HTML + CSS + JS), sense base de dades ni WordPress. Funciona directament a Hostinger.

## Estructura

```
index.html            Pàgina d'inici (banner, sobre mi, cursos)
3eso.html             Pàgina de 3r ESO
2batx-ccss.html       Pàgina de 2n Batxillerat CCSS
pau.html              Racó PAU (compte enrere, exàmens anteriors, consells)
reptes.html           Reptes de la setmana i curiositats
.htaccess             HTTPS obligatori + memòria cau (Hostinger)
assets/css/style.css  Estils (colors a l'inici del fitxer)
assets/js/i18n.js     Tots els textos en valencià, castellà i anglés
assets/js/materials.js  ★ Materials de cada curs + dades de contacte
assets/js/pau.js        ★ Data de la PAU i enllaços als exàmens
assets/js/reptes.js     ★ Reptes de la setmana i curiositats
assets/img/           Foto, banner, icona
materials/3eso/       Ací poses els PDF de 3r ESO
materials/2batx-ccss/ Ací poses els PDF de 2n Batx CCSS
```

## Afegir un material

1. Copia el PDF a `materials/3eso/` (p. ex. `t1-apunts.pdf`). Fes servir noms sense espais ni accents.
2. Obri `assets/js/materials.js` i, dins de la unitat corresponent, afig o edita una línia:

```js
{ type: "notes", title: { va: "Apunts de la unitat", es: "Apuntes de la unidad", en: "Unit notes" }, url: "materials/3eso/t1-apunts.pdf" },
```

Tipus: `notes` (apunts), `exercises`, `video`, `resource`, `exam`.
Si `url` és un enllaç de YouTube, el vídeo s'obri dins de la web.
Si `url` està buit, apareix com a "Pròximament".


## Fórmules (LaTeX)

Escriu-les entre `$...$` (en línia) o `$$...$$` (centrades). Als fitxers .js cal doblar
les barres: `$\\frac{1}{2}$`, `$\\sqrt{x}$`.

## Repte de la setmana

A `assets/js/reptes.js`, afig un bloc nou amb la data del dilluns. Pots deixar-ne
de programats: només es mostren quan arriba la seua data.

## Google Drive

Comparteix el PDF com a "Qualsevol persona amb l'enllaç" i enganxa l'enllaç a `url`.

## Pujar-ho a Hostinger

1. hPanel → **Webs** → **Administrador de fitxers** → carpeta `public_html`.
2. Puja-hi **tot el contingut** d'aquesta carpeta (no la carpeta mateixa), inclòs `.htaccess`.
   No cal pujar `Foto personal.JPG` ni `LLEGEIX-ME.md`.
3. Activa el certificat SSL gratuït a hPanel (Seguretat → SSL).

Quan afegisques contingut, només cal tornar a pujar el fitxer .js que hages canviat.

## Apunts interactius (HTML)

Els apunts interactius són pàgines HTML autònomes dins de `materials/` (p. ex.
`materials/2batx-ccss/t1-matrius-determinants.html`). Porten els tres idiomes
dins del mateix fitxer i recorden l'idioma i el tema triats a la web.

- Idioma directe per enllaç: afig `?lang=va`, `?lang=es` o `?lang=en` a l'URL.
- Mode incrustat (sense capçalera de la web ni peu): afig `?embed=1`. Dins d'un
  iframe s'activa sol.

### Posar-los a AULES (Moodle)

1. **Opció recomanada — iframe.** Afig un recurs *Pàgina* o una *Àrea de text i
   mitjans*, obri l'editor en mode HTML (`</>`) i enganxa:

   ```html
   <iframe src="https://EL-TEU-DOMINI/materials/2batx-ccss/t1-matrius-determinants.html?lang=va"
           style="width:100%;height:85vh;border:0;border-radius:12px" loading="lazy"
           title="Matrius i determinants"></iframe>
   ```

2. **Opció enllaç.** Recurs *URL* amb l'adreça de la pàgina (Visualització: *Incrusta* o *Obri*).
3. **Sense web.** Recurs *Fitxer* pujant directament el `.html` (funciona sol perquè
   les fórmules es carreguen des d'internet).

## Resum teòric (2n Batx CCSS)

`materials/2batx-ccss/resum-teoric.html` és el formulari-resum de tot el curs (trilingüe i
interactiu), amb llicència CC BY-NC-SA 4.0 (sense finalitats comercials). Apareix a la pàgina de 2n Batx CCSS com a secció
«Resum Teòric» abans de la Unitat 1: a `materials.js` porta `num: "★"`, i les unitats amb
`num` no compten en la numeració (la Unitat 1 continua sent la 1).

## Amagar un material (p. ex. solucions)

A `assets/js/materials.js`, afig `hidden: true` a la línia del material:

```js
{ type: "exercises", title: {...}, url: "materials/3eso/t2-fitxa-solucions.pdf", download: true, hidden: true }
```

Per tornar a mostrar-lo, esborra `, hidden: true` (o posa `hidden: false`).
El fitxer continua al servidor: qui conega l'adreça exacta el pot obrir.

## Cursos "Pròximament"

Un curs amb `units: []` a `materials.js` apareix com a "Pròximament".
Quan hi afegisques la primera unitat, el cercador i els filtres apareixen sols.

## Guies «Amb la calculadora» (Casio fx-991SP CW)

El contingut és a `_eines/casio/guies.py` (un bloc per unitat). Per canviar-lo o afegir una unitat nova,
edita aquest fitxer i torna a generar les pàgines des de la carpeta del web:

```
python3 _eines/casio/build_casio.py
```

Al text, `[[EXE]]` dibuixa una tecla, `<<Matriz>>` una opció de menú i `$...$` una fórmula.
Després enllaça la pàgina a `materials.js` amb `type: "calc"`.

## Fitxes d'exercicis en PDF (LaTeX)

Les fonts són a `_eines/fonts-latex/<curs-unitat>/` (per exemple `3eso-t3`, `1eso-t1`). Cada carpeta té la fitxa,
les solucions i els logos. Per a compilar-les cal tindre LaTeX instal·lat (MacTeX); des de la carpeta de la fitxa:

```
pdflatex t3-fitxa-exercicis.tex
pdflatex t3-fitxa-solucions.tex
```

A `1eso-t1`, `1eso-t2`, `1eso-t3`, `1eso-t4`, `1batx-mi-t4`, `2batx-ccss-t1`, `2batx-ccss-t5`, `2batx-ccss-t6`, `2batx-ccss-t7`, `2batx-ccss-t8`, `2batx-ccss-t9` i `2batx-ccss-t10` la fitxa i les solucions es generen totes dues des de `genera.py` (una sola llista d'exercicis):
edita-la, executa `python3 genera.py` i després compila els dos `.tex`.
Copia els PDF resultants a `materials/<curs>/` i enllaça'ls a `materials.js` (les solucions, amb `hidden: true`
si encara no han de ser visibles). Els fitxers auxiliars de LaTeX (`.aux`, `.log`, `.pdf`…) no es pugen al repositori.

### Versió en castellà de les fitxes

Algunes fitxes tenen versió en castellà (totes les de 3r ESO, unitats 1 a 12): la font és
el mateix nom acabat en `-es.tex` (p. ex. `t1-fitxa-exercicis-es.tex`) i el PDF es copia a
`materials/<curs>/` acabat en `-es.pdf`. A les unitats que es generen amb `genera.py` (de la 4 a la 12), la versió en
castellà té el seu propi `genera-es.py` (mateixos exercicis i càlculs, amb els textos traduïts, i el preàmbul en
castellà el fa `comu/castella.py`): executa `python3 genera-es.py` i compila els dos `-es.tex`. Si canvies un
exercici a `genera.py`, fes el mateix canvi a `genera-es.py`. Usen `\usepackage[spanish,es-minimal,es-noshorthands]{babel}` i
les metadades del PDF van dins de `\AtBeginDocument{\hypersetup{...}}` (amb «º» a les opcions de
`hyperref` no compila). El curs s'escriu «3º ESO»: al text, `3\textsuperscript{o} ESO` (el caràcter «º» de
Fira Sans porta un guió baix). A `materials.js`, l'`url` porta els dos fitxers i la web mostra el de l'idioma triat
(en anglés, el valencià):

```js
url: { va: "materials/3eso/t1-fitxa-exercicis.pdf", es: "materials/3eso/t1-fitxa-exercicis-es.pdf" }
```

Si canvies una fitxa que té versió en castellà, recorda canviar també el `-es.tex`.

## Apunts interactius generats

Els apunts de 1r ESO es generen amb `_eines/apunts/1eso-tN/build.py` (contingut), `app.js` (ginys)
i `extra.css` (estil propi), una carpeta per unitat (`1eso-t1`, `1eso-t2`…). Des de la carpeta del web:

```
python3 _eines/apunts/1eso-t1/build.py
python3 _eines/apunts/1eso-t2/build.py
python3 _eines/apunts/1eso-t3/build.py
python3 _eines/apunts/1eso-t4/build.py
```

`_eines/apunts/relabel.py` fa que cada exercici dels quadres «Practica» comence per a) i ajusta les solucions.

Els de 2n Batx CCSS de les unitats 4, 5 i 6 funcionen igual, amb les carpetes `2batx-ccss-t4`, `2batx-ccss-t5` i
`2batx-ccss-t6` (la 6, Aplicacions de la derivada, reaprofita el codi de les unitats 4 i 5):

```
python3 _eines/apunts/2batx-ccss-t6/build.py
```

La unitat 7 (Representació gràfica de funcions, carpeta `2batx-ccss-t7`) reaprofita també l'estudi de la monotonia
de la unitat 6. A la fitxa, `genera.py` calcula i dibuixa ell mateix les gràfiques de les solucions:

```
python3 _eines/apunts/2batx-ccss-t7/build.py
```

La unitat 8 (Integrals, carpeta `2batx-ccss-t8`) només reaprofita el nucli de la unitat 4, al qual afegeix l'ombrejat
d'àrees a les gràfiques. Els ginys treballen amb polinomis de manera exacta (fraccions), com a la PAU de CCSS. A la fitxa,
`genera.py` comprova totes les integrals i àrees amb fraccions exactes i dibuixa els recintes de les solucions:

```
python3 _eines/apunts/2batx-ccss-t8/build.py
```

La unitat 9 (Probabilitat, carpeta `2batx-ccss-t9`) no necessita el nucli de gràfiques: els diagrames de Venn, els arbres,
la taula de contingència i la calculadora de dos successos (que resol les quatre regions del diagrama de Venn amb fraccions
exactes) són a `app.js`. El contingut està repartit en `contingut-1.html`, `contingut-2.html` i `contingut-3.html`, que
`build.py` ajunta per ordre. A la fitxa, `genera.py` calcula totes les probabilitats amb fraccions (o comptant l'espai
mostral) i les compara amb les solucions oficials dels exercicis de la PAU:

```
python3 _eines/apunts/2batx-ccss-t9/build.py
```

La unitat 10 (Distribució binomial i normal, carpeta `2batx-ccss-t10`) reaprofita l'estil de les unitats 4 i 9. `build.py`
calcula i insereix les taules de la binomial i de la normal $N(0,1)$ que s'adjunten a l'examen de la PAU valenciana (des del
curs 2025-26); els ginys llegeixen els valors d'aquestes taules, de manera que els resultats coincideixen amb la taula:

```
python3 _eines/apunts/2batx-ccss-t10/build.py
```

Els apunts de 1r Batx MI de la unitat 4 (Geometria analítica en el pla, carpeta `1batx-mi-t4`) reaprofiten l'estil de les
unitats 4 i 9 de 2n Batx CCSS. Els ginys dibuixen un pla cartesià amb punts que es poden arrossegar (vectors, rectes, angles,
distàncies i el laboratori del triangle) i calculen amb fraccions exactes. A `materials.js` la unitat porta `num: "4"`.
La fitxa (`_eines/fonts-latex/1batx-mi-t4/genera.py`) comprova
totes les solucions amb fraccions i en dibuixa algunes figures:

```
python3 _eines/apunts/1batx-mi-t4/build.py
```

Els apunts de 1r Batx MI de la unitat 1 (Nombres reals, carpeta `1batx-mi-t1`) funcionen com els de la unitat 4: el contingut és a
`contingut-*.html`, els ginys a `app.js` (classificador de nombres, fracció generatriu, valor absolut, entorns, constructor d'intervals,
operacions amb intervals, extracció de factors i explorador de logaritmes) i l'estil a `extra.css`. Les rectes reals s'adapten a
l'ample de la pantalla perquè es lligen bé al mòbil. A `materials.js` la unitat porta `num: "1"` i és del bloc d'aritmètica.
La fitxa (`_eines/fonts-latex/1batx-mi-t1/genera.py`) té els 42 exercicis de la fitxa del departament amb la mateixa numeració i
una secció 6 amb 12 exercicis nous; comprova amb fraccions exactes els decimals periòdics, les operacions i els intervals, i
dibuixa les rectes de les solucions:

```
python3 _eines/apunts/1batx-mi-t1/build.py
cd _eines/fonts-latex/1batx-mi-t1 && python3 genera.py && pdflatex t1-fitxa-exercicis.tex && pdflatex t1-fitxa-solucions.tex
```

Els apunts de 1r Batx MI de la unitat 2 (Àlgebra. Equacions i inequacions, carpeta `1batx-mi-t2`) tenen 11 apartats (2.1-2.11) i funcionen com els de la unitat 1.
Els ginys de `app.js` treballen amb fraccions exactes: operacions i divisió llarga de polinomis, Ruffini pas a pas (també amb divisors `ax+b`), factorització pas a pas,
simplificació de fraccions algebraiques, segon grau i biquadrades, solucions estranyes de les equacions amb radicals, exponencials amb canvi de variable, taula de signes
d'inequacions polinòmiques i racionals, i aixetes. A `materials.js` la unitat porta `num: "2"` i és del bloc d'àlgebra. La fitxa (`_eines/fonts-latex/1batx-mi-t2/genera.py`)
té 71 exercicis (1-62 de la fitxa del departament, i una secció 12 amb 9 de nous); sympy calcula o comprova totes les solucions (les de radicals, logaritmes i exponencials,
numèricament) i es dibuixen les taules de Ruffini i les rectes de les inequacions:

```
python3 _eines/apunts/1batx-mi-t2/build.py
cd _eines/fonts-latex/1batx-mi-t2 && python3 genera.py && pdflatex t2-fitxa-exercicis.tex && pdflatex t2-fitxa-solucions.tex
```

Els apunts de 1r Batx MI de la unitat 3 (Sistemes d'equacions i inequacions, carpeta `1batx-mi-t3`) tenen 6 apartats (3.1-3.6) i funcionen com els de la unitat 2.
Els ginys de `app.js`: Gauss pas a pas (SCD, SCI i SI), recta i circumferència, inequació amb dues incògnites pas a pas, i semiplans i regions. Les rectes reals apilades dels exemples de 3.3 es defineixen a `STACKS` i les figures de 3.4 i 3.5, amb l'atribut `data-half` del contingut. A `materials.js` la unitat porta `num: "3"` i és del bloc d'àlgebra.
La fitxa (`_eines/fonts-latex/1batx-mi-t3/genera.py`) té 32 exercicis (1-28 de la fitxa del departament, i una secció 6 amb 4 de nous); sympy calcula o comprova totes les solucions
i es dibuixen les rectes de les inequacions i les regions:

```
python3 _eines/apunts/1batx-mi-t3/build.py
cd _eines/fonts-latex/1batx-mi-t3 && python3 genera.py && pdflatex t3-fitxa-exercicis.tex && pdflatex t3-fitxa-solucions.tex
```

Els apunts de 1r Batx MI de la unitat 5 (Trigonometria, carpeta `1batx-mi-t5`) ajunten en una sola unitat les dues parts dels apunts
del departament (Trigonometria 1 i 2): 13 apartats (5.1-5.13), del radian a les funcions trigonomètriques. Funcionen com els de la
unitat 2; a més, dins de les fórmules `{,}` és la coma decimal i en anglés es converteix sola en un punt. Els ginys de `app.js`:
radians, triangle rectangle, circumferència goniomètrica, raons a partir d'una (exactes amb arrels), reducció al primer quadrant,
triangles rectangles, laboratori del triangle (teoremes del sinus i del cosinus), resolució de triangles pas a pas (amb el cas ambigu),
fórmules de la suma amb valors exactes, comprovador d'identitats, equacions elementals, de la circumferència a la gràfica i
`y = A·f(Bx+C)+D`. A `materials.js` la unitat porta `num: "5"` i és del bloc de geometria. La fitxa
(`_eines/fonts-latex/1batx-mi-t5/genera.py`) té els exercicis de les dues fitxes del departament (1-41 i 42-60, en el mateix ordre)
i una secció 13 amb 13 exercicis nous; calcula tots els valors numèrics, compara les solucions exactes amb el valor numèric i
comprova que les equacions i els sistemes tenen exactament les solucions donades:

```
python3 _eines/apunts/1batx-mi-t5/build.py
cd _eines/fonts-latex/1batx-mi-t5 && python3 genera.py && pdflatex t5-fitxa-exercicis.tex && pdflatex t5-fitxa-solucions.tex
```

Els apunts de 1r Batx MI de la unitat 6 (Estudi de funcions, carpeta `1batx-mi-t6`) parteixen dels apunts «Funcions i
característiques» del departament (que allí eren la unitat 6) i tenen 9 apartats (6.1-6.9): concepte de funció, domini i
recorregut, talls, monotonia, continuïtat, simetries i periodicitat, transformacions (translacions), composició i inversa. Les
figures fixes de les unitats 6 i 7 es defineixen a `1batx-mi-t6/fig.py` (classe `Plot`, que dibuixa la mateixa gràfica en SVG per
als apunts i en TikZ per a les fitxes) i es posen al contingut amb el marcador `@@FIG:nom@@`. Els ginys de `app.js` tenen un
analitzador d'expressions propi: calculadora de dominis, talls, simetria, translacions, composició i inversa. La fitxa
(`_eines/fonts-latex/1batx-mi-t6/genera.py`) té 30 exercicis en 8 seccions; sympy comprova talls, composicions i inverses, i els
dominis es comproven numèricament. Els estudis complets de funcions aniran en una unitat posterior.

Els apunts de la unitat 7 (Funcions elementals, carpeta `1batx-mi-t7`) tenen 9 apartats (7.1-7.9): lineals i afins, quadràtiques i
cúbiques, racionals, radicals, exponencials, logarítmiques, trigonomètriques, a trossos i valor absolut, i problemes de màxims i
mínims amb funcions quadràtiques (vèrtex i extrems de l'interval, sense límits ni derivades). `build.py` agafa `fig.py` de la carpeta
de la unitat 6; `app.js` repeteix la part comuna (analitzador i gràfiques) de la unitat 6. La fitxa
(`_eines/fonts-latex/1batx-mi-t7/genera.py`) té 35 exercicis en 8 seccions, l'última amb problemes d'ingressos, costos, beneficis i
àrees; els màxims i mínims en un interval es comproven també amb una malla fina. Les dues unitats porten `num: "6"` i `num: "7"` a
`materials.js` i són del bloc d'anàlisi:

```
python3 _eines/apunts/1batx-mi-t6/build.py
python3 _eines/apunts/1batx-mi-t7/build.py
cd _eines/fonts-latex/1batx-mi-t6 && python3 genera.py && pdflatex t6-fitxa-exercicis.tex && pdflatex t6-fitxa-solucions.tex
cd _eines/fonts-latex/1batx-mi-t7 && python3 genera.py && pdflatex t7-fitxa-exercicis.tex && pdflatex t7-fitxa-solucions.tex
```

Les pàgines PAU de les unitats 9 (Probabilitat) i 10 (Binomial i normal) es generen des de `_eines/pau/pr/`: `pr.txt`
conté els enunciats del dossier de selectivitat valencià (`## R` probabilitat, `## B` binomial i normal), `keys.json`
els relaciona amb el número del dossier i `sol_u9a.py`, `sol_u9b.py` i `sol_u10.py`, les solucions (calculades i
comprovades). No toca les pàgines PAU de les unitats 1-3:

```
python3 _eines/pau/pr/build.py
```

Les pàgines PAU d'anàlisi (unitats 4 a 8) es generen des de `_eines/pau/an/`: `an.txt` conté els 118 enunciats del
dossier «Exercicis d'anàlisi de la selectivitat» en el mateix ordre (`## 6 | Juny 2001`: el número és la unitat on va
l'exercici, la més avançada que necessita). A `build.py`, `XL` indica els exercicis que també es mostren a les unitats 4 i 5
perquè algun apartat és d'aquestes unitats. Les solucions són a `sol_a.py`, `sol_b.py` i `sol_c.py` (números 1-40, 41-80 i
81-118): `anlib.py` fa els càlculs amb fraccions exactes, l'estudi complet de les funcions i les gràfiques en SVG:

```
python3 _eines/pau/an/build.py
```

## 2n Batx MII: unitat 7 (Aplicacions de la derivada)

Els apunts es generen amb `_eines/apunts/2batx-mii-t7/build.py` (contingut a `contingut-*.html`, ginys a `app.js`,
estil a `extra.css`). Reaprofita el nucli de la unitat 5 de MII i la derivació simbòlica de la unitat 6 de MII; l'estudi
numèric (domini, asímptotes, monotonia, curvatura i periodicitat de les trigonomètriques) està copiat i ampliat a `app.js`.
La fitxa i les solucions es generen amb `_eines/fonts-latex/2batx-mii-t7/genera.py` (sympy comprova totes les solucions i
dibuixa les gràfiques); els exercicis PAU són del recull de tota Espanya del curs 2026/27 (ebaumatematicas.com):

```
python3 _eines/apunts/2batx-mii-t7/build.py
cd _eines/fonts-latex/2batx-mii-t7 && python3 genera.py && pdflatex t7-fitxa-exercicis.tex && pdflatex t7-fitxa-solucions.tex
```

## 2n Batx MII: unitats 8 (Representació gràfica de funcions) i 9 (Integrals)

Segueixen l'estructura de les unitats 7 i 8 de CCSS, amb més dificultat i amb funcions radicals, trigonomètriques i a trossos.
Els apunts es generen amb `_eines/apunts/2batx-mii-t8/build.py` i `_eines/apunts/2batx-mii-t9/build.py` (contingut a
`contingut-*.html`, ginys a `app.js`, estil a `extra.css`). La unitat 8 reaprofita de l'`app.js` de la unitat 7 de MII els
textos de la interfície, l'estudi numèric (domini, asímptotes, monotonia, curvatura, periodicitat), els ginys de monotonia i
curvatura i l'estudi complet pas a pas; la unitat 9 n'agafa els nombres exactes i les arrels numèriques, i hi afegeix les àrees
ombrejades i els rectangles de Riemann de la unitat 8 de CCSS, la descomposició exacta en fraccions simples i els passos guiats
de canvi de variable i per parts. Les fitxes es generen amb els `genera.py` de `_eines/fonts-latex/2batx-mii-t8` i `-t9`
(sympy comprova totes les solucions; les gràfiques i els recintes es dibuixen amb TikZ), amb exercicis PAU del mateix recull
de tota Espanya (ebaumatematicas.com):

```
python3 _eines/apunts/2batx-mii-t8/build.py
python3 _eines/apunts/2batx-mii-t9/build.py
cd _eines/fonts-latex/2batx-mii-t8 && python3 genera.py && pdflatex t8-fitxa-exercicis.tex && pdflatex t8-fitxa-solucions.tex
cd _eines/fonts-latex/2batx-mii-t9 && python3 genera.py && pdflatex t9-fitxa-exercicis.tex && pdflatex t9-fitxa-solucions.tex
```

## Treballar des de casa i des de l'institut

El repositori de GitHub és la còpia de referència. Abans de començar, baixa els canvis (`git pull` o *Fetch/Pull*
a GitHub Desktop); en acabar, puja'ls (`git add -A`, `git commit -m "…"`, `git push`). No poses la carpeta dins de
OneDrive: la sincronització la fa GitHub. Les carpetes que comencen per `_` no es publiquen a fentmates.org.

### Des d'un ordinador amb Windows

- **Git:** GitHub Desktop (s'instal·la per a l'usuari, sense permisos d'administrador). Si no es pot instal·lar res,
  obri el repositori a github.com i prem la tecla `.` per a editar-lo al navegador.
- **Editor:** Visual Studio Code (també té versió per a l'usuari).
- **Python:** des de python.org o la Microsoft Store. A Windows l'ordre és `py` en lloc de `python3`:
  `py _eines/apunts/1eso-t1/build.py`
- **LaTeX:** MiKTeX (instal·la sol els paquets que falten la primera vegada que compiles). Sense instal·lar res,
  pots pujar la carpeta de la fitxa a Overleaf i compilar-la allà.
- **Vista prèvia:** obri `index.html` amb doble clic al navegador (les fórmules necessiten connexió a internet).
- El fitxer `.gitattributes` fa que els salts de línia siguen els mateixos a Mac i a Windows.

## Global d'Àlgebra (2n Batx CCSS)

Secció de repàs de les unitats 1 i 2, darrere de la Unitat 2. A `materials.js` porta `num: "★"` (com el Resum teòric, no compta com a unitat)
i `block: "algg"`, un blau més fosc que el de les unitats d'àlgebra (color a `BLOCKS` de `main.js` i de `fm-materials.js`).
Les dues pàgines es generen amb el mateix `build.py` dels models d'examen:

```
python3 _eines/examens/build.py _eines/examens/2batx-global-alg/pau.src.html materials/2batx-ccss/global-algebra-pau.html
python3 _eines/examens/build.py _eines/examens/2batx-global-alg/model1.src.html materials/2batx-ccss/global-algebra-prova-model1.html
```

`pau.src.html` té 19 exercicis de la PAU 2026 d'altres comunitats (de www.ebaumatematicas.com) amb les solucions i una
taula que indica en quins exercicis apareix cada contingut; `model1.src.html` és la prova global tipus PAU, i
`resum.src.html`, la presentació-resum (mapa conceptual i errors típics), amb l'estil de `materials/3eso/t2-resum-diapositives.html`
(es genera igual, cap a `materials/2batx-ccss/global-algebra-resum-diapositives.html`). Atenció: dins
d'un marcador `[[va||es||en]]` no es pot escriure `||` (per exemple `|M||N|`; cal posar `|M|\cdot|N|`).
