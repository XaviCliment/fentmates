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

La versió en castellà de cada guia és a `_eines/casio/guies_es.py` (mateixa estructura, textos traduïts); el mateix
`build_casio.py` genera les dues versions (`casio-…-es.html`). Si canvies una guia, canvia-la als dos fitxers.

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

Totes les fitxes d'exercicis i de solucions tenen versió en castellà (tots els cursos; només el model d'examen
de la unitat 2 de 3r ESO no en té): la font és
el mateix nom acabat en `-es.tex` (p. ex. `t1-fitxa-exercicis-es.tex`) i el PDF es copia a
`materials/<curs>/` acabat en `-es.pdf`. A les unitats que es generen amb `genera.py` (totes menys 3r ESO 1–3), la versió en
castellà té el seu propi `genera-es.py` (mateixos exercicis i càlculs, amb els textos traduïts, i el preàmbul en
castellà el fa `comu/castella.py`): executa `python3 genera-es.py` i compila els dos `-es.tex`. Si canvies un
exercici a `genera.py`, fes el mateix canvi a `genera-es.py`. Usen `\usepackage[spanish,es-minimal,es-noshorthands]{babel}` i
les metadades del PDF van dins de `\AtBeginDocument{\hypersetup{...}}` (amb «º» a les opcions de
`hyperref` no compila). `castella.py` també fa que el sinus s'escriga «sen» (i l'arcsinus, «arcsen»). Per a cursos que no són 3r ESO,
passa `curs='1eso'`, `'4eso-b'`, `'1batx-mi'`, `'2batx-ccss'` o `'2batx-mii'` a `preambul()` i fes servir `assignatura(curs)`
(4t ESO B: `eso4b.build(..., lang='es')`). El curs s'escriu «3º ESO»: al text, `3\textsuperscript{o} ESO` (el caràcter «º» de
Fira Sans porta un guió baix). A `materials.js`, l'`url` porta els dos fitxers i la web mostra el de l'idioma triat
(en anglés, el valencià):

```js
url: { va: "materials/3eso/t1-fitxa-exercicis.pdf", es: "materials/3eso/t1-fitxa-exercicis-es.pdf" }
```

Si canvies una fitxa que té versió en castellà, recorda canviar també el `-es.tex`.

### Versió en castellà de les pàgines PAU

Les pàgines `materials/2batx-*/pau-….html` tenen una versió `pau-…-es.html`, que fa
`_eines/pau/castella/tradueix.py` a partir de la valenciana amb un diccionari de frases
(`_eines/pau/castella/<curs>-<pàgina>.json`; les fórmules de cada frase hi apareixen com a ⟨1⟩, ⟨2⟩…).
Després de tornar a generar una pàgina PAU en valencià:

```
python3 _eines/pau/castella/tradueix.py materials/2batx-ccss/pau-u1-matrius.html --falten
```

escriu a `<curs>-<pàgina>.falten.json` les frases noves que encara no tenen traducció: tradueix-les, afig-les al
`.json` del diccionari i torna a executar l'ordre sense `--falten` (o `--totes` per a totes les pàgines).

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

Els apunts de 2n ESO de la unitat 1 (Nombres naturals i enters, carpeta `2eso-t1`) funcionen com els de 1r ESO. Tenen 10
apartats (1.1-1.10), i `app.js` ajunta els ginys de les unitats 2 (divisibilitat, mcm i MCD) i 3 (enters) de 1r ESO. A més, hi afig
el giny de potències d'enters, el de l'arrel quadrada (exacta o entera) i una calculadora pas a pas que també accepta `^` i `√`.
A `materials.js` la unitat és la primera targeta de 2n ESO (bloc d'aritmètica). La fitxa (`_eines/fonts-latex/2eso-t1/`) té 51
exercicis en 10 seccions. Excepcionalment, els exercicis de les dues llengües són a un sol fitxer, `exercicis.py`, que també
calcula i comprova les solucions; `genera.py` (valencià) i `genera-es.py` (castellà) només escriuen els `.tex`:

```
python3 _eines/apunts/2eso-t1/build.py
cd _eines/fonts-latex/2eso-t1 && python3 genera.py && python3 genera-es.py
pdflatex t1-fitxa-exercicis.tex && pdflatex t1-fitxa-solucions.tex && pdflatex t1-fitxa-exercicis-es.tex && pdflatex t1-fitxa-solucions-es.tex
```

Compte: en acabar, `build.py` executa `_eines/tema/aplica.py`, que pot posar una versió antiga del tema a altres pàgines de `materials/`.
Desfés aquests canvis abans de fer el commit (`git checkout` de les pàgines que no són de la unitat).

La unitat 3 de 2n ESO (Introducció a l'àlgebra. Polinomis, carpeta `2eso-t3`) té 8 apartats (3.1-3.8): l'àlgebra i el llenguatge
algebraic, monomis, operacions amb monomis (també potències i operacions combinades), polinomis, suma i resta, producte, identitats
notables i factor comú (sense divisió de polinomis). El contingut és a `alg.py` (3.1-3.3) i `pol.py` (3.4-3.8), amb comprovacions
sympy (`chk`), i `app.js` és el de la unitat 4 de 3r ESO amb la potència d'un monomi al giny d'operacions, entrenadors nous
(reduir termes semblants, potències i operacions combinades de monomis) i un qüestionari propi. A `materials.js` és del bloc
d'àlgebra. La fitxa (`_eines/fonts-latex/2eso-t3/genera.py`, 63 exercicis en 8 seccions) calcula amb sympy els resultats i en
comprova els escrits a mà; com a la unitat 2, `genera-es.py` només executa `genera.py` en castellà:

```
python3 _eines/apunts/2eso-t3/build.py
cd _eines/fonts-latex/2eso-t3 && python3 genera.py && python3 genera-es.py
pdflatex t3-fitxa-exercicis.tex && pdflatex t3-fitxa-solucions.tex && pdflatex t3-fitxa-exercicis-es.tex && pdflatex t3-fitxa-solucions-es.tex
```

La unitat 4 de 2n ESO (Equacions de 1r i 2n grau, carpeta `2eso-t4`) té 9 apartats (4.1-4.9): elements i solucions, primer grau,
parèntesis, denominadors, problemes de primer grau, segon grau incompletes i completes, el discriminant i problemes de segon
grau. El contingut és a `eq1.py` (4.1-4.5) i `eq2.py` (4.6-4.9), amb comprovacions sympy (`ce`), i `app.js` és el de la unitat 5
de 3r ESO sense Ruffini, amb entrenadors nous (parèntesis, denominadors i problemes de segon grau) i un qüestionari propi. A
`materials.js` és del bloc d'àlgebra. La fitxa (`_eines/fonts-latex/2eso-t4/genera.py`, 70 exercicis en 9 seccions) resol les
equacions pas a pas amb el resolutor de la fitxa de 3r (`sol`) i ho comprova tot amb sympy; `genera-es.py` l'executa en castellà:

```
python3 _eines/apunts/2eso-t4/build.py
cd _eines/fonts-latex/2eso-t4 && python3 genera.py && python3 genera-es.py
pdflatex t4-fitxa-exercicis.tex && pdflatex t4-fitxa-solucions.tex && pdflatex t4-fitxa-exercicis-es.tex && pdflatex t4-fitxa-solucions-es.tex
```

La unitat 5 de 2n ESO (Sistemes d'equacions, carpeta `2eso-t5`) té 7 apartats (5.1-5.7): equacions de primer grau amb dues
incògnites, què és i què representa un sistema, substitució, igualació, reducció (amb «Quin mètode triem?»), mètode gràfic (amb
quantes solucions pot tindre un sistema, sense els noms SCD/SCI/SI) i problemes. El contingut és a `sis1.py` (5.1-5.3) i `sis2.py`
(5.4-5.7), amb comprovacions sympy (`cs`, `ok`, `same`), i `app.js` és el de la unitat 6 de 3r ESO amb els entrenadors nous «troba
la y» (`val`) i «quin és el sistema?» (`tra`) i un qüestionari propi. A `materials.js` és del bloc d'àlgebra. La fitxa
(`_eines/fonts-latex/2eso-t5/genera.py`, 53 exercicis en 7 seccions) resol els sistemes pas a pas amb els resolutors de la fitxa
de 3r (`m_sub`, `m_igu`, `m_red`) i ho comprova tot amb sympy; `genera-es.py` l'executa en castellà:

```
python3 _eines/apunts/2eso-t5/build.py
cd _eines/fonts-latex/2eso-t5 && python3 genera.py && python3 genera-es.py
pdflatex t5-fitxa-exercicis.tex && pdflatex t5-fitxa-solucions.tex && pdflatex t5-fitxa-exercicis-es.tex && pdflatex t5-fitxa-solucions-es.tex
```

La unitat 6 de 2n ESO (Proporcionalitat i percentatges, carpeta `2eso-t6`) té 8 apartats (6.1-6.8): raons i proporcions,
magnituds directament i inversament proporcionals (reducció a la unitat, taula i regla de tres), proporcionalitat composta,
repartiments directament i inversament proporcionals, percentatges, càlcul del tant per cent i del total, i augments i
disminucions percentuals (índex de variació, quantitat inicial i variacions encadenades). El contingut és a `prop1.py` (6.1-6.5)
i `prop2.py` (6.6-6.8), amb comprovacions `ck`; `comu.py` és el de la unitat 5 de 1r ESO. `app.js` és el de la unitat 5 de 1r
ESO sense els ginys de decimals, amb el repartidor i el solucionador de proporcionalitat composta de 3r ESO (funció `M3`, amb
els seus propis formats numèrics), dues calculadores de percentatges (classe `w-pctc`), entrenadors nous i un qüestionari
propi. A `materials.js` és del bloc d'aritmètica. La fitxa (`_eines/fonts-latex/2eso-t6/genera.py`, 57 exercicis en 8
seccions) comprova tots els resultats amb fraccions i decimals exactes; `genera-es.py` l'executa en castellà:

```
python3 _eines/apunts/2eso-t6/build.py
cd _eines/fonts-latex/2eso-t6 && python3 genera.py && python3 genera-es.py
pdflatex t6-fitxa-exercicis.tex && pdflatex t6-fitxa-solucions.tex && pdflatex t6-fitxa-exercicis-es.tex && pdflatex t6-fitxa-solucions-es.tex
```

La unitat 7 de 2n ESO (Teorema de Pitàgores. Perímetres i àrees, carpeta `2eso-t7`) és l'adaptació de la unitat 9 de 3r
(`3eso-t9`) sense la distància entre dos punts del pla i amb un apartat nou de problemes amb enunciat. Té 9 apartats (7.1-7.9):
el teorema de Pitàgores (càlcul d'un costat i ternes), el recíproc (és rectangle un triangle?), aplicacions en figures planes,
perímetres i àrees de triangles i quadrilàters, polígons regulars, longitud de la circumferència i arcs, àrea del cercle i figures
circulars, figures compostes i problemes amb enunciat (estratègia, perímetre o àrea?, entrenador `prob` nou). El contingut és a
`p12.py`, `p34.py`, `p56.py`, `p78.py` i `p9.py`, amb `ck()`; `app.js` (`window.FM27`) i `extra.css` són els de 3r. La fitxa
(`_eines/fonts-latex/2eso-t7/genera.py`, 81 exercicis en 9 seccions) és la de 3r adaptada, amb la secció 9 nova; com la de 3r, la
versió en castellà és un fitxer a part (`genera-es.py`), i un canvi s'ha de fer en tots dos:

```
python3 _eines/apunts/2eso-t7/build.py
cd _eines/fonts-latex/2eso-t7 && python3 genera.py && python3 genera-es.py
pdflatex t7-fitxa-exercicis.tex && pdflatex t7-fitxa-solucions.tex && pdflatex t7-fitxa-exercicis-es.tex && pdflatex t7-fitxa-solucions-es.tex
```

La unitat 8 de 2n ESO (Semblança. Teorema de Tales, carpeta `2eso-t8`) és l'adaptació de la unitat 10 de 3r (`3eso-t10`), amb
els apartats reordenats i sense el mitjà proporcional ni la raó dels volums. Té 5 apartats (8.1-8.5): figures semblants (raó de
semblança, perímetres i àrees), plànols, mapes i maquetes (escales numèrica i gràfica), el teorema de Tales (proporcions i divisió
d'un segment), aplicació a la semblança de triangles (posició de Tales i criteris) i problemes (ombres, mirall, fanal, rampa, riu).
El contingut és a `s123.py` i `s45.py`, amb `ck()`; `app.js` (`window.FM28`), `comu.py`, `fig8.py` i `extra.css` són els de 3r, i
`quiz.js` és nou. A `materials.js` és del bloc de geometria (il·lustració `tales`). La fitxa (`_eines/fonts-latex/2eso-t8/genera.py`,
56 exercicis en 5 seccions, bilingüe amb `T()`) dibuixa les figures en TikZ amb el `tz()` de la fitxa de 3r; `genera-es.py`
l'executa en castellà:

```
python3 _eines/apunts/2eso-t8/build.py
cd _eines/fonts-latex/2eso-t8 && python3 genera.py && python3 genera-es.py
pdflatex t8-fitxa-exercicis.tex && pdflatex t8-fitxa-solucions.tex && pdflatex t8-fitxa-exercicis-es.tex && pdflatex t8-fitxa-solucions-es.tex
```

La unitat 9 de 2n ESO (Cossos geomètrics. Àrees i volums, carpeta `2eso-t9`) és l'adaptació de la unitat 11 de 3r
(`3eso-t11`) sense troncs de piràmide i de con ni la Terra i les coordenades geogràfiques. Té 8 apartats (9.1-9.8): poliedres,
fórmula d'Euler i poliedres regulars, prismes, piràmides, cossos de revolució (cilindre i con), l'esfera, volum de prismes i
cilindres (amb unitats i Cavalieri), volum de piràmides, cons i esferes, i cossos compostos i problemes. La teoria, les figures 3D
(`solids.py`, `fig11.py`) i els ginys (`app.js`, `window.FM29`) són els de 3r; els problemes resolts, la «Practica» de cada apartat i
part del qüestionari són nous, i cada resultat es comprova amb `ck()`. A `materials.js` és del bloc de geometria. La fitxa
(`_eines/fonts-latex/2eso-t9/genera.py`, 63 exercicis en 8 seccions, bilingüe amb `T()`) dibuixa els cossos en TikZ amb el `tz()`
de la fitxa de 3r; `genera-es.py` l'executa en castellà:

```
python3 _eines/apunts/2eso-t9/build.py
cd _eines/fonts-latex/2eso-t9 && python3 genera.py && python3 genera-es.py
pdflatex t9-fitxa-exercicis.tex && pdflatex t9-fitxa-solucions.tex && pdflatex t9-fitxa-exercicis-es.tex && pdflatex t9-fitxa-solucions-es.tex
```

La unitat 10 de 2n ESO (Funcions, carpeta `2eso-t10`) està feta a partir de la unitat 9 de 1r (`1eso-t9`). Té 8 apartats
(10.1-10.8): concepte de funció (variables, maneres de donar una funció i prova de la recta vertical), funcions donades per taules
de valors (unir o no els punts, valors intermedis i fórmula a partir de la taula), funcions donades per la seua equació (taula,
gràfic, punts del gràfic i càlcul de la $x$), funció de proporcionalitat $y=mx$, pendent d'una recta, funcions lineals $y=mx+n$,
funcions constants $y=k$ (rectes horitzontals i verticals, funcions constants a trossos) i interpretació de gràfics i problemes. El
contingut és a `s12.py`, `s345.py`, `s67.py` i `s8.py` (aquest, fet a partir dels apartats 9.4 i 9.7 de 1r), amb `comu.py` i `ck()`.
`app.js` (`window.FM210`) és el de 1r amb el lector d'expressions de 3r (`3eso-t7`) i ginys nous (recta vertical, gràfic d'una
equació, pendent entre dos punts, rectes horitzontals i verticals) i entrenadors nous; `quiz.js` és nou. A `materials.js` és del
bloc d'anàlisi (il·lustració `grafiques`). La fitxa (`_eines/fonts-latex/2eso-t10/genera.py`, 59 exercicis en 8 seccions,
bilingüe amb `T()`) dibuixa els gràfics amb el `tp()` de la fitxa de 1r; `genera-es.py` l'executa en castellà:

```
python3 _eines/apunts/2eso-t10/build.py
cd _eines/fonts-latex/2eso-t10 && python3 genera.py && python3 genera-es.py
pdflatex t10-fitxa-exercicis.tex && pdflatex t10-fitxa-solucions.tex && pdflatex t10-fitxa-exercicis-es.tex && pdflatex t10-fitxa-solucions-es.tex
```

La unitat 11 de 2n ESO (Atzar i probabilitat, carpeta `2eso-t11`) és l'adaptació de la unitat 12 de 3r (`3eso-t12`), sense
operacions amb esdeveniments ni les fórmules del contrari i de la unió. Té 5 apartats (11.1-11.5): experiments aleatoris i
deterministes (amb el llenguatge de l'atzar i l'entrenador nou `det`), espai mostral i esdeveniments, probabilitat d'un esdeveniment
(freqüències, llei dels grans nombres i propietats), la llei de Laplace (experiments regulars i irregulars) i estratègies de càlcul:
diagrames d'arbre (també amb i sense reemplaçament), la taula de doble entrada dels dos daus i la taula de contingència (giny
`w-cont` amb caselles editables i entrenador `cont`, nous). El contingut és a `s12.py`, `s3.py`, `s4.py` i `s5.py`, amb `ck()` i
fraccions exactes; `app.js` (`window.FM211`), `comu.py` (amb `ctab()` per a les taules de contingència) i `extra.css` són els de 3r
ampliats, i `quiz.js` és nou. A `materials.js` és la unitat amb `num: "11"` (es va publicar abans que la 10), del bloc de probabilitat. La
fitxa (`_eines/fonts-latex/2eso-t11/genera.py`, 54 exercicis en 5 seccions, bilingüe amb `T()`) reaprofita part dels exercicis de 3r
i en comprova totes les probabilitats amb fraccions; `genera-es.py` l'executa en castellà:

```
python3 _eines/apunts/2eso-t11/build.py
cd _eines/fonts-latex/2eso-t11 && python3 genera.py && python3 genera-es.py
pdflatex t11-fitxa-exercicis.tex && pdflatex t11-fitxa-solucions.tex && pdflatex t11-fitxa-exercicis-es.tex && pdflatex t11-fitxa-solucions-es.tex
```

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

Els apunts de 1r Batx MI de la unitat 8 (Límits i continuïtat, carpeta `1batx-mi-t8`) parteixen d'una còpia dels de la unitat 4 de
2n Batx CCSS (`contingut-1.html` i `app.js`, copiats el 13/11/2026; els fitxers de CCSS no es toquen) adaptada a l'estructura dels
apunts del departament: 10 apartats (8.1-8.10), amb la indeterminació 1^∞ en un punt (8.6), el mètode general de l'asímptota obliqua
(m i n amb límits) i les branques parabòliques (8.10). `build.py` funciona com el de la unitat 6 (extra.css de les unitats 4 i 9 de
CCSS + el propi). La fitxa (`_eines/fonts-latex/1batx-mi-t8/genera.py`) té 36 exercicis en 8 seccions, amb els exercicis proposats
als apunts del departament; `C()` estima numèricament cada límit de les solucions (també els laterals) i `EQ()` comprova les
divisions i factoritzacions:

```
python3 _eines/apunts/1batx-mi-t8/build.py
cd _eines/fonts-latex/1batx-mi-t8 && python3 genera.py && pdflatex t8-fitxa-exercicis.tex && pdflatex t8-fitxa-solucions.tex
```

Els apunts de 1r Batx MI de la unitat 9 (Derivades i aplicacions, carpeta `1batx-mi-t9`) ajunten els apunts de les unitats 5, 6 i
7 de 2n Batx CCSS seguint els apunts del departament: 9 apartats (9.1-9.9), amb la representació gràfica de funcions (9.8) just
abans dels problemes d'optimització (9.9). `contingut-2.html` i `app.js` són còpies fetes el 13/11/2026 (els fitxers de CCSS no
es toquen): `app.js` té el nucli comú (nucli de la unitat 4 + derivació simbòlica de la 5 + estudi de la 6) i tres mòduls
(`M5`, `M6`, `M7`), cadascun amb els seus textos (`UI`), figures i ginys; els textos del nucli són la unió dels tres. Els
laboratoris es diuen `w-lab5` (calculadora de derivades) i `w-lab7` (estudi complet, dins de 9.8). La fitxa
(`_eines/fonts-latex/1batx-mi-t9/genera.py`) té 36 exercicis en 8 seccions (9 d'estudi i representació gràfica, 6 de racionals); `comprova.py` verifica amb sympy cada derivada,
valor, punt crític i signe:

```
python3 _eines/apunts/1batx-mi-t9/build.py
cd _eines/fonts-latex/1batx-mi-t9 && python3 genera.py && pdflatex t9-fitxa-exercicis.tex && pdflatex t9-fitxa-solucions.tex
```

Els apunts de 1r Batx MI de la unitat 10 (Estadística, carpeta `1batx-mi-t10`) són nous: 9 apartats, 10.1-10.3 repàs
d'estadística unidimensional (taules, centralització i posició, dispersió) i 10.4-10.9 estadística bidimensional (taules de
doble entrada, núvol de punts, variàncies i covariància, correlació lineal, recta de regressió amb estimacions; els altres tipus de relació només amb exemples de
núvols). `app.js` té el seu propi codi (`uniStats`, `biStats`, `cloud` per als núvols en SVG, `cloudR` genera núvols amb una r
exacta; l'opció `reg` hi dibuixa la recta de regressió) i 9 ginys. La fitxa (`_eines/fonts-latex/1batx-mi-t10/genera.py`) té 34 exercicis en 9 seccions; tots els resultats es
calculen amb `Fraction` (`uni`, `bi`, `dbl`) i es formaten amb `d()`, i els núvols es dibuixen amb TikZ (`nuvol`):

```
python3 _eines/apunts/1batx-mi-t10/build.py
cd _eines/fonts-latex/1batx-mi-t10 && python3 genera.py && pdflatex t10-fitxa-exercicis.tex && pdflatex t10-fitxa-solucions.tex
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

## 1r Batx CCSS (Matemàtiques Aplicades a les CCSS I)

A `materials.js` el curs porta `cards: true`, `byBlock: true` i `sections: true`, com la resta de cursos; a `fm-materials.js`, la
unitat 1 és del bloc d'aritmètica, la 2 i la 3, del d'àlgebra, i de la 4 a la 6, del d'anàlisi (la resta, de moment, `all`).
Les fitxes usen `\fmcurs{1batx-ccss}` i, en castellà, `curs='1batx-ccss'` a `castella.py` («Matemáticas CCSS»).

- **Unitat 1 (Nombres reals, `1batx-ccss-t1`)**: parteix de la unitat 1 de 1r Batx MI (mateix `app.js`, mateixos ginys i el mateix
  `build.py`), reorganitzada en 8 apartats (1.1-1.8): nombres reals ($\mathbb N$, $\mathbb Z$, $\mathbb Q$, $\mathbb I$ i fracció generatriu),
  intervals i semirectes, valor absolut (equacions i desigualtats; sense el nom d'entorn), unió i intersecció (`w-ops` ja no fa
  diferències), radicals (forma exponencial i simplificació, índex comú, extracció i introducció de factors, i suma, resta, producte,
  quocient i potència), racionalització, logaritmes i propietats dels logaritmes. Ginys nous a `app.js`: `w-rad` (radical ↔ potència,
  simplificació i extracció), `w-ic` (reducció a índex comú, comparació, producte i quocient) i `w-lp` (propietats dels logaritmes amb
  nombres), i el qüestionari (16 preguntes). La fitxa (`_eines/fonts-latex/1batx-ccss-t1/genera.py`, 51 exercicis en 9 seccions, la
  darrera de problemes de context) és bilingüe amb `T(va, es)` com la de la unitat 3; els intervals i les desigualtats amb valor absolut
  es calculen amb fraccions exactes (`absI`) i les solucions de radicals i logaritmes es comproven numèricament (`cn`).

```
python3 _eines/apunts/1batx-ccss-t1/build.py
cd _eines/fonts-latex/1batx-ccss-t1 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
```

- **Unitat 2 (Àlgebra, `1batx-ccss-t2`)**: parteix de la unitat 2 de 1r Batx MI (mateix `build.py` i ginys), sense les inequacions (que
  són a la unitat 3) ni l'apartat de problemes, en 9 apartats (2.1-2.9): polinomis i operacions, Ruffini i teorema del residu,
  factorització, fraccions algebraiques (amb operacions combinades), equacions polinòmiques (primer grau amb parèntesis i denominadors,
  segon grau, biquadrades i grau superior), amb radicals, racionals, exponencials i logarítmiques. Giny nou a `app.js`: `w-lin` (equació
  de primer grau pas a pas: m.c.m., parèntesis, transposició i solució, amb casos sense solució i identitat, i equacions aleatòries);
  s'han tret `w-sign` i `w-tap`. Qüestionari de 12 preguntes. La fitxa (`_eines/fonts-latex/1batx-ccss-t2/genera.py`, 62 exercicis en
  10 seccions, la darrera de problemes de context) és bilingüe amb `T(va, es)`; sympy calcula o comprova totes les solucions.
  `fm-materials.js`: les unitats 2 i 3 són d'àlgebra.

```
python3 _eines/apunts/1batx-ccss-t2/build.py
cd _eines/fonts-latex/1batx-ccss-t2 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
```

- **Unitat 3 (Sistemes d'equacions i inequacions, `1batx-ccss-t3`, pàgina `t3-sistemes-inequacions.html`)**: 9 apartats (3.1-3.9):
  sistemes d'equacions lineals 2x2 (classificació SCD/SCI/SI i interpretació gràfica, mètodes, equacions amb parèntesis i denominadors),
  mètode de Gauss (sistemes esglaonats, classificació i un problema), sistemes no lineals (substitució i reducció), inequacions de primer
  grau (regles, parèntesis, denominadors, casos $\mathbb R$ i $\varnothing$, problemes), de segon grau i de grau superior (estudi del signe,
  paràbola, $\Delta\lt0$, arrels dobles, Ruffini), sistemes amb una incògnita, inequacions i sistemes amb dues incògnites i programació lineal
  (teorema fonamental, problemes de màxim i de mínim, infinites solucions i sense òptim). Els apartats 3.1-3.3 es van afegir el 20/11/2026
  davant dels sis que hi havia (la pàgina abans es deia `t3-inequacions.html` i la unitat, «Inequacions i sistemes d'inequacions»; la clau
  de progrés és ara `fm-1batx-ccss-u3-sistemes-done`). `app.js` ajunta el nucli de la unitat 2 de 1r Batx MI (polinomis, factorització,
  intervals, recta real i taula de signes `w-sign`, ara només amb polinomis) i els ginys de rectes apilades (`STACKS`), semiplans (`w-semi`)
  i regions (`w-half`) de la unitat 3 de 1r Batx MI; `wFigs` accepta `data-step` per al pas de la quadrícula. Els ginys nous són a `nous.js`
  (al lloc de `/*@@NOUS@@*/`): sistemes 2x2 pas a pas per reducció amb les dues rectes (`w-sis2`, amb el lector `parseLin`/`parseEq2`, que
  no simplifica per un factor comú perquè es vegen les equacions proporcionals), Gauss pas a pas (`w-gauss`) i recta-circumferència
  (`w-nl`) copiats de la unitat 3 de 1r Batx MI, un lector d'expressions amb parèntesis (`parseExpr`), inequacions de primer grau pas a
  pas (`w-lin`), sistemes d'inequacions amb una incògnita escrites amb text (`w-sys1`, `solvePoly`, `interS`) i el resolutor de
  programació lineal pas a pas (`w-pl`: regió, vèrtexs, valors de $F$, òptim i recta de nivell; detecta infinites solucions i problemes
  sense òptim), i el qüestionari (18 preguntes). La fitxa (`_eines/fonts-latex/1batx-ccss-t3/genera.py`, 51 exercicis en 10 seccions) és
  bilingüe amb `T(va, es)` (`genera-es.py` l'executa amb `FM_LANG=es`); sympy resol els sistemes d'equacions (`s2`, `gsol`, `nlsol`; `red`
  comprova les formes reduïdes), resol cada inequació i sistema i `iq()` la compara amb la solució esperada, `regck` comprova els vèrtexs
  de les regions i `pl()`, els vèrtexs, els valors de $F$ i l'òptim dels problemes de programació lineal (també que l'òptim existeix quan la
  regió no és fitada), que es dibuixen amb la recta de nivell en verd.

```
python3 _eines/apunts/1batx-ccss-t3/build.py
cd _eines/fonts-latex/1batx-ccss-t3 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
```

- **Unitat 4 (Estudi de funcions, `1batx-ccss-t4`, pàgina `t4-estudi-funcions.html`)**: el mateix contingut que la unitat 6 de 1r Batx MI
  (`1batx-mi-t6`: apunts, ginys, `fig.py` i fitxa de 30 exercicis), copiat i renumerat com a unitat 4 (apartats 4.1-4.9). Canvis respecte
  de MI: curs i capçaleres, la clau de progrés (`fm-1batx-ccss-u4-funcions-done`), les referències a «la unitat 7» (ara «la unitat
  següent») i el missatge de la calculadora de dominis amb funcions trigonomètriques. `genera.py` i `genera-es.py` són dos fitxers
  separats, com a MI; si canvies un exercici, canvia'l als dos (i, si cal, també a `1batx-mi-t6`).

```
python3 _eines/apunts/1batx-ccss-t4/build.py
cd _eines/fonts-latex/1batx-ccss-t4 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
```

- **Unitat 5 (Funcions elementals, `1batx-ccss-t5`, pàgina `t5-funcions-elementals.html`)**: el mateix contingut que la unitat 7 de
  1r Batx MI (`1batx-mi-t7`) **sense les funcions trigonomètriques**: fora l'apartat 7.7 (teoria, giny `w-trig` i pregunta del
  qüestionari sobre la tangent) i la secció de trigonomètriques de la fitxa (2 exercicis). Queden 8 apartats (5.1-5.8: lineals,
  quadràtiques i cúbiques, racionals, radicals, exponencials, logarítmiques, a trossos i valor absolut, i problemes de màxims i
  mínims) i 33 exercicis en 7 seccions. `build.py` i els `genera*.py` agafen `fig.py` de `1batx-ccss-t4`; les referències a la
  unitat d'estudi de funcions apunten a la unitat 4 (apartats 4.7 i 4.9). Clau de progrés `fm-1batx-ccss-u5-elementals-done`.
- **Unitat 6 (Límits i continuïtat, `1batx-ccss-t6`, pàgina `t6-limits-continuitat.html`)**: el mateix contingut que la unitat 8 de
  1r Batx MI (`1batx-mi-t8`: apunts, ginys i fitxa de 36 exercicis), renumerat com a unitat 6 (apartats 6.1-6.10), amb el curs i les
  capçaleres de CCSS i la clau de progrés `fm-1batx-ccss-u6-limits-done`. Si canvies un exercici, canvia'l a `genera.py` i a
  `genera-es.py` (i, si cal, també a `1batx-mi-t8`).
- **Unitat 7 (Derivades i aplicacions, `1batx-ccss-t7`, pàgina `t7-derivades.html`)**: parteix de la unitat 9 de 1r Batx MI
  (`1batx-mi-t9`), renumerada (apartats 7.1-7.9), **sense funcions trigonomètriques** (taules de derivades, exemples, exercicis,
  ginys `w-fd` i `w-chain` i calculadora) i amb l'apartat 7.9 d'optimització refet: o bé la funció és coneguda i cal estudiar-ne
  el creixement i el decreixement, o bé cal construir una funció de benefici, ingressos o costos (contextos empresarials i socials;
  sense problemes geomètrics). El giny `w-build` té els casos «Benefici = I − C», «Cafeteria», «Agència de viatges» i «Bosses».
  La fitxa té 39 exercicis en 8 seccions (les 9 de representació gràfica, com a MI; 10 d'optimització) i `comprova.py` en verifica
  amb sympy 211 resultats. Clau de progrés `fm-1batx-ccss-u7-derivades-done`.
- **Unitat 8 (Distribucions bidimensionals, `1batx-ccss-t8`, pàgina `t8-distribucions-bidimensionals.html`)**: parteix de la part
  bidimensional de la unitat 10 de 1r Batx MI (`1batx-mi-t10`, apartats 10.4-10.9), **sense l'estadística unidimensional** i
  reorganitzada en 6 apartats: 8.1 distribucions bidimensionals i taules de freqüències (taula simple, doble entrada, freqüències
  relatives, distribucions condicionades i dades agrupades en intervals), 8.2 núvol de punts, 8.3 correlació i regressió (dependència
  funcional, estadística i independència; relacions no lineals; correlació i causalitat), 8.4 correlació lineal i covariància, 8.5
  coeficient de correlació (propietats, només mesura la relació lineal, valors atípics) i 8.6 rectes de regressió (les dues rectes,
  coeficients de regressió, $m_{yx}\cdot m_{xy}=r^2$, quina és quina, fiabilitat). Exemple conductor nou: publicitat i vendes.
  `app.js` afig a la de MI la segona recta (opció `reg2` de `cloud`, en verd discontinu), el giny `w-reg` amb les dues rectes i les
  dues estimacions, `w-two` (l'angle entre les rectes segons $r$) i `w-lines` (de dues rectes escrites amb text al centre de gravetat,
  quina és quina i $r$; `parseLine`, `linesInfo`), i un qüestionari de 19 preguntes. La fitxa (`genera.py`, bilingüe amb `T(va, es)`;
  `genera-es.py` l'executa amb `FM_LANG=es`) té 35 exercicis en 6 seccions; tots els resultats es calculen amb `Fraction` i per a cada
  recta es comprova que passa per $(\bar x,\bar y)$, que fa mínima la suma de quadrats i que $m_{yx}\cdot m_{xy}=r^2$.
  Clau de progrés `fm-1batx-ccss-u8-bidimensionals-done`.
- **Unitat 9 (Combinatòria i probabilitat, `1batx-ccss-t9`, pàgina `t9-combinatoria-probabilitat.html`)**: 14 apartats. 9.1-9.4
  (tècniques de recompte i combinatòria) parteixen dels 9.1-9.3 de 4t ESO B (`4eso-b-t9`) i hi afigen el principi de la suma, les
  permutacions amb repetició i circulars, les propietats dels nombres combinatoris (Stifel, triangle de Tartaglia, suma d'una fila) i
  el binomi de Newton. 9.5-9.14 són els apartats 10.1-10.10 de 2n Batx MII (`2batx-mii-t10`, terminologia «succés»), sense les
  variables aleatòries ni la binomial: 9.8 (Laplace) remet a la combinatòria de 9.1-9.4, 9.12 és «successos dependents i
  independents» i 9.13 «experiències compostes», amb un quadre nou d'experiències independents i dependents. `app.js` és el de MII
  sense `wBin` ni `wNmin`, amb els ginys de recompte de 4t ESO B (`w-comb`, `w-mult`, `w-llista`, `w-tipus`; `w-tipus` amb
  permutacions amb repetició) i un qüestionari de 22 preguntes. La fitxa (`genera.py`, bilingüe amb `T(va, es)`; `genera-es.py`
  l'executa amb `FM_LANG=es`) té 49 exercicis en 7 seccions i 149 comprovacions (recomptes amb `math.comb`/`math.perm` o enumerant
  els casos amb `itertools`, probabilitats amb `Fraction`). Clau de progrés `fm-1batx-ccss-u9-probabilitat-done`.
- **Unitat 10 (Distribucions de probabilitat, `1batx-ccss-t10`, pàgina `t10-distribucions-probabilitat.html`)**: 9 apartats.
  Parteix de la unitat 10 de 2n Batx CCSS (`2batx-ccss-t10`): 10.3-10.4 i 10.6-10.9 són els seus 10.2-10.3 i 10.5-10.8 (binomial,
  taula de la binomial, normal, normal típica i taula, tipificació, aproximació de la binomial a la normal), sense la insistència
  en la PAU. Són nous 10.1 (variables aleatòries discretes i contínues, paral·lelisme amb l'estadística), 10.2 (funció de
  probabilitat i de distribució, mitjana i desviació típica, jocs justos; giny `w-disc`) i 10.5 (funció de densitat sense
  integrals, amb àrees de rectangles, triangles i trapezis, i distribució uniforme; giny `w-dens`). `build.py` calcula les taules
  de la binomial i de la normal $N(0,1)$ com a 2n. `app.js` és el de 2n amb `wDisc`, `wDens` i un qüestionari de 18 preguntes.
  La fitxa (`genera.py`, bilingüe amb `T(va, es)`; `genera-es.py` l'executa amb `FM_LANG=es`) té 42 exercicis en 6 seccions (12 de
  la PAU d'altres comunitats, els mateixos que a la fitxa de 2n) i 98 comprovacions: discretes amb `Fraction`, normal com a la PAU
  (z arredonit a dues decimals i taula a quatre decimals). Clau de progrés `fm-1batx-ccss-u10-distribucions-done`.

```
python3 _eines/apunts/1batx-ccss-t5/build.py
python3 _eines/apunts/1batx-ccss-t6/build.py
python3 _eines/apunts/1batx-ccss-t7/build.py
python3 _eines/apunts/1batx-ccss-t8/build.py
python3 _eines/apunts/1batx-ccss-t9/build.py
python3 _eines/apunts/1batx-ccss-t10/build.py
cd _eines/fonts-latex/1batx-ccss-t5 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
cd _eines/fonts-latex/1batx-ccss-t6 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
cd _eines/fonts-latex/1batx-ccss-t7 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
cd _eines/fonts-latex/1batx-ccss-t8 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
cd _eines/fonts-latex/1batx-ccss-t9 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
cd _eines/fonts-latex/1batx-ccss-t10 && python3 genera.py && python3 genera-es.py  # i pdflatex (dues vegades) dels quatre .tex
```

## 4t ESO Matemàtiques A

Matemàtiques A és l'opció més aplicada de 4t (alumnat que farà cicles formatius). Els apunts són a `_eines/apunts/4eso-a-tN`
i les fitxes, a `_eines/fonts-latex/4eso-a-tN` (capçalera «Matemàtiques A · 4t ESO», `\fmcurs{4eso-a}` i, en castellà,
`curs='4eso-a'` a `castella.py`). A `fm-materials.js`, les unitats 1 i 2 són del bloc d'aritmètica, les 3-5, del d'àlgebra, les 6 i 7, del d'anàlisi, la 8, del de geometria i les 9-11, del d'estadística i probabilitat.

- **Unitat 1 (Nombres naturals, enters i fraccionaris, `4eso-a-t1`)**: 11 apartats (1.1-1.11): naturals i divisió entera, potències,
  arrels i operacions combinades amb naturals, enters i valor absolut, operacions combinades amb enters, fraccions equivalents
  (simplificació i amplificació), operacions, operacions combinades i problemes amb fraccions, potències amb base entera i racional
  propietats de les potències i potències d'exponent zero i negatiu. El contingut és a `nat.py` (1.1-1.4), `fra4.py` (1.5-1.8),
  `pot4.py` (1.9-1.10) i `neg4.py` (1.11), i les ajudes a
  `eines4a.py`. `fra4.py` **importa** els apartats 2.5, 2.7, 2.8, 2.10 i 2.11 de 2n ESO (`_eines/apunts/2eso-t2/fra.py` i `pot.py`) i
  hi afig problemes d'aplicació: si es canvien allà, també canvien ací. `app.js` té dues parts: la 1 és l'`app.js` de 2eso-t2
  (fraccions, índex, idioma i qüestionari) i la 2, el de 2eso-t1 reduït als ginys d'enters (els que porten la classe `wz`), que
  segueix l'idioma de la part 1; hi ha un entrenador nou d'operacions combinades amb naturals (`natc`). El qüestionari és a `quiz.js`.
  La fitxa té 62 exercicis en 10 seccions (nivell pujat per a acostar-lo al del llibre de text; la 10, potències d'exponent negatiu, correspon a l'apartat 1.11); com a 2eso-t1, `exercicis.py` té les dues llengües i calcula i comprova les solucions
  (les fraccions s'escriuen entre claus, `{3/4}`; exponents negatius `2^-3`, valor absolut `abs(…)` i fraccions compostes `⟦num¦den⟧`); `genera.py` i `genera-es.py` només escriuen els `.tex`.

```
python3 _eines/apunts/4eso-a-t1/build.py
cd _eines/fonts-latex/4eso-a-t1 && python3 genera.py && python3 genera-es.py
pdflatex t1-fitxa-exercicis.tex && pdflatex t1-fitxa-solucions.tex && pdflatex t1-fitxa-exercicis-es.tex && pdflatex t1-fitxa-solucions-es.tex
```

- **Unitat 2 (Nombres reals, `4eso-a-t2`)**: adaptació a Matemàtiques A dels apunts de la unitat 1 de 4t ESO B (mateix `build.py`,
  `app.js` i `extra.css`, sense valor absolut ni logaritmes i amb més exemples resolts). 7 apartats (2.1-2.7): classificació dels nombres
  i fracció generatriu, intervals i semirectes, operacions amb intervals, arrels i radicals (pas a potència i a l'inrevés), radicals
  equivalents (simplificació, índex comú, extracció i introducció de factors), operacions amb radicals i racionalització. El contingut és a
  `contingut-1..4.html` (convencions ⟪va‖es‖en⟫) i el qüestionari, a `quiz.js` (`build.py` el posa al lloc de `/*@@QUIZ@@*/`). Hi ha
  8 ginys; el de suma i resta de radicals (`w-sum`, a 2.6) és nou. La fitxa (`_eines/fonts-latex/4eso-a-t2/genera.py`, 57 exercicis en
  11 seccions) fa servir les eines de `comu/eso4b.py` amb `build(..., curs='4eso-a')`; és bilingüe amb `T(va, es)` i `genera-es.py`
  l'executa en castellà. Els intervals es calculen amb aritmètica exacta i els radicals es comproven amb sympy (`eq`).

```
python3 _eines/apunts/4eso-a-t2/build.py
cd _eines/fonts-latex/4eso-a-t2 && python3 genera.py && python3 genera-es.py
pdflatex t2-fitxa-exercicis.tex && pdflatex t2-fitxa-solucions.tex && pdflatex t2-fitxa-exercicis-es.tex && pdflatex t2-fitxa-solucions-es.tex
```

- **Unitat 3 (Polinomis, `4eso-a-t3`)**: adaptació a Matemàtiques A dels apunts de la unitat 2 de 4t ESO B (mateix `build.py`, `app.js` i
  `extra.css`, sense binomi de Newton, m.c.d./m.c.m. ni operacions amb fraccions algebraiques, i amb més exemples resolts). 9 apartats (3.1-3.9): monomis
  (operacions i valor numèric), polinomis i valor numèric, suma i resta, producte (per un monomi i de polinomis) i identitats notables,
  divisió, regla de Ruffini (i valor numèric amb Ruffini), arrels, factorització (factor comú, identitats notables, segon grau i Ruffini) i, com a aplicació, simplificació de fraccions
  algebraiques (ginys `w-frs`, portat de `4eso-b-t2/app.js`).
  El contingut és a `contingut-1..4.html`; els ginys nous (operacions amb monomis `w-mon`, taula de valors `w-vn`, identitats notables
  `w-id` i factor comú + identitat notable `w-fci`) són a `nous.js`, que `build.py` posa al lloc de `/*@@NOUS@@*/`, i el qüestionari
  (24 preguntes) a `quiz.js`. La fitxa (`_eines/fonts-latex/4eso-a-t3/genera.py`, 62 exercicis en 13 seccions) calcula totes les solucions
  amb sympy (`pt`, `fac`, `rft` per a les taules de Ruffini, `dv`); és bilingüe amb `T(va, es)` i `genera-es.py` l'executa en castellà.

```
python3 _eines/apunts/4eso-a-t3/build.py
cd _eines/fonts-latex/4eso-a-t3 && python3 genera.py && python3 genera-es.py
pdflatex t3-fitxa-exercicis.tex && pdflatex t3-fitxa-solucions.tex && pdflatex t3-fitxa-exercicis-es.tex && pdflatex t3-fitxa-solucions-es.tex
```

- **Unitat 4 (Equacions, `4eso-a-t4`)**: adaptació a Matemàtiques A dels apunts de la unitat 3 de 4t ESO B (mateix `app.js` i `extra.css`,
  sense biquadrades, Ruffini, exponencials, logarítmiques ni inequacions; `build.py` com el de la unitat 3). 8 apartats (4.1-4.8): primer grau
  (parèntesis, denominadors i casos sense solució o amb infinites), problemes de primer grau, segon grau completes i incompletes (discriminant),
  segon grau amb parèntesis i denominadors, problemes de segon grau, equacions factoritzades, racionals (valors prohibits) i amb radicals (un
  radical, o dos sense més termes). Els ginys de 4t B que es queden són la gràfica de segon grau (`w-quad`), les factoritzades (`w-feq`) i els
  radicals (`w-rad`); els nous són a `nous.js`: un resolutor pas a pas d'equacions escrites amb parèntesis, `/` i `^` (`parseEqn`, fraccions de
  polinomis exactes; m.c.m., valors prohibits, forma reduïda, incompletes, fórmula i comprovació), amb tres instàncies (`w-eq1`, `w-eq2`,
  `w-eqr`), i un entrenador de problemes amb nombres aleatoris (`w-prob1` de primer grau i `w-prob2` de segon). El qüestionari (22 preguntes) és
  a `quiz.js`. La fitxa (`_eines/fonts-latex/4eso-a-t4/genera.py`, 51 exercicis en 10 seccions) escriu cada equació una sola vegada en la
  mateixa notació que el resolutor (`Q()` en fa el TeX i l'expressió de sympy) i en calcula les solucions (`lin`, `qd`, `rac`); `chk()`
  comprova també les escrites a mà (en els radicals, descarta les que donen l'arrel d'un negatiu). És bilingüe amb `T(va, es)`.

```
python3 _eines/apunts/4eso-a-t4/build.py
cd _eines/fonts-latex/4eso-a-t4 && python3 genera.py && python3 genera-es.py
pdflatex t4-fitxa-exercicis.tex && pdflatex t4-fitxa-solucions.tex && pdflatex t4-fitxa-exercicis-es.tex && pdflatex t4-fitxa-solucions-es.tex
```

- **Unitat 5 (Sistemes d'equacions i inequacions, `4eso-a-t5`)**: adaptació a Matemàtiques A dels apunts de la unitat 4 de 4t ESO B (mateix
  `build.py` que la unitat 4), sense inequacions amb dues incògnites i amb les inequacions de la unitat 3 de 4t ESO B. 8 apartats (5.1-5.8): mètode
  gràfic (equacions amb dues incògnites, classificació), substitució, igualació i reducció (amb «Quin mètode triem?»), sistemes amb parèntesis i
  denominadors, no lineals, problemes, inequacions de primer grau, de segon grau i sistemes d'inequacions. `app.js` ajunta el motor de 4eso-b-t3
  (polinomis, intervals, gràfiques) i els ginys de 4eso-b-t4 (`w-gr`, `w-met`, `w-nl`, `w-sys1`; els passos de `w-met` són a `metRows`) i de
  4eso-b-t3 (`w-lin`, i `w-sign` només de segon grau). Els nous són a `nous.js`: el resolutor de sistemes amb parèntesis i denominadors (`w-sred`,
  `parseLinEq`), el resolutor d'inequacions de primer i segon grau escrites amb text (`w-in1`, `w-in2`, amb `parseSide` de la unitat 4) i
  l'entrenador de problemes amb sistemes lineals i no lineals (`w-psys1`, `w-psys2`, dues respostes). Qüestionari de 22 preguntes a `quiz.js`.
  La fitxa (`_eines/fonts-latex/4eso-a-t5/genera.py`, 45 exercicis en 9 seccions) escriu cada sistema o inequació una sola vegada (`Q()` en fa
  el TeX i l'expressió de sympy, també amb `y` i amb `<`, `<=`, `>`, `>=`); sympy en calcula la forma reduïda i les solucions (`lsr`, `iq`,
  `iqs`) i comprova les escrites a mà (`ls`, `kind`, `nls`, `chk`). Bilingüe amb `T(va, es)`. Compte: amb `icomma`, els punts s'escriuen
  `(2,\,3)` (si no, `2,3` es llig com un decimal).

```
python3 _eines/apunts/4eso-a-t5/build.py
cd _eines/fonts-latex/4eso-a-t5 && python3 genera.py && python3 genera-es.py
pdflatex t5-fitxa-exercicis.tex && pdflatex t5-fitxa-solucions.tex && pdflatex t5-fitxa-exercicis-es.tex && pdflatex t5-fitxa-solucions-es.tex
```

- **Unitat 6 (Funcions. Característiques, `4eso-a-t6`)**: adaptació a Matemàtiques A dels apunts de la unitat 7 de 4t ESO B (mateix `app.js`
  i `extra.css`, sense simetries ni funció inversa; els dominis, només de polinòmiques, racionals i arrels quadrades de radicand de primer grau).
  8 apartats (6.1-6.8): concepte de funció (variables, formes d'expressar-la, unir o no els punts, imatges i antiimatges), domini i recorregut,
  punts de tall, continuïtat i tipus de discontinuïtats (amb l'exemple d'un aparcament que cobra per hores), creixement i decreixement amb
  màxims i mínims, periodicitat, interpretació de gràfics (excursió, temperatura) i construcció de funcions a partir d'un enunciat (taxi,
  corral, comparació d'ofertes). Les figures són les de `4eso-b-t7/fig.py` més les pròpies de `fig6.py`. Els ginys de 4t B que es queden són
  la recta vertical, la calculadora de dominis, els talls, les discontinuïtats, la monotonia i el període; els nous, a `nous.js`: lectura d'un
  gràfic amb context (`w-read`: excursió, dipòsit i temperatura, amb el ritme de cada tram) i construcció d'una funció a partir d'un enunciat
  (`w-build`: taxi, dipòsit que es buida, corral de perímetre fix i repartiment, amb taula, fórmula, domini i gràfica). Qüestionari de 22
  preguntes a `quiz.js`. La fitxa (`_eines/fonts-latex/4eso-a-t6/genera.py`, 50 exercicis en 8 seccions) parteix de la de 4eso-b-t7; sympy
  comprova talls i solucions, `ckdom` cada domini i `ok()`/`lin()` les dades dels problemes i dels gràfics. Bilingüe amb `T(va, es)`
  (`genera-es.py` l'executa amb `FM_LANG=es`).

```
python3 _eines/apunts/4eso-a-t6/build.py
cd _eines/fonts-latex/4eso-a-t6 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
```

- **Unitat 7 (Funcions elementals, `4eso-a-t7`)**: adaptació a Matemàtiques A dels apunts de la unitat 8 de 4t ESO B (mateix `app.js`
  i `extra.css`), amb menys profunditat, sense funcions a trossos, valor absolut ni logaritmes, i amb les funcions radicals. 9 apartats
  (7.1-7.9): funcions lineals (proporcionalitat directa, afí i constant), equació punt-pendent (pendent per dos punts, rectes paral·leles,
  punts alineats), funció quadràtica (forma, vèrtex, eix, talls, casos incomplets), representació de funcions quadràtiques (sis passos),
  funcions radicals ($\sqrt x$ i les seues translacions), proporcionalitat inversa ($y=k/x$), translacions de la hipèrbola
  ($y=k/x\pm a$, $y=k/(x\pm a)$), funcions exponencials ($a^x$ i $C\cdot a^t$ amb percentatges) i problemes amb funcions. Les figures
  són les de `4eso-b-t7/fig.py` més les pròpies de `fig7.py`. Els ginys de 4t B que es queden són la recta per dos punts, el laboratori
  de paràboles i els laboratoris de radicals i d'hipèrboles (`wTrans`); els nous, a `nous.js`: tipus de rectes amb m i n
  (`w-types`), paràbola pas a pas (`w-qstep`), rectangle d'àrea k de la hipèrbola (`w-inv`), creixement i decreixement exponencial
  (`w-grow`) i comparació de dues tarifes lineals (`w-cmp`). Qüestionari de 23 preguntes a `quiz.js`. La fitxa
  (`_eines/fonts-latex/4eso-a-t7/genera.py`, 55 exercicis en 9 seccions) parteix de la de 4eso-b-t8; sympy comprova talls, vèrtexs i
  solucions i `ok()` les dades dels problemes (49 comprovacions). Bilingüe amb `T(va, es)` (`genera-es.py` l'executa amb `FM_LANG=es`).

```
python3 _eines/apunts/4eso-a-t7/build.py
cd _eines/fonts-latex/4eso-a-t7 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
```

- **Unitat 8 (Semblança. Aplicacions, `4eso-a-t8`)**: adaptació a Matemàtiques A dels apunts de la unitat 8 de 2n ESO (`2eso-t8`, que ja
  venien dels de 3r, `3eso-t10`), amb el mateix `build.py`, `comu.py`, `extra.css` i `app.js` (`window.FM48`). 7 apartats (8.1-8.7): figures
  semblants (amb els volums de cossos semblants, giny `w-k` i entrenador `k23` de 3r), plànols, mapes i maquetes (amb els volums d'una maqueta),
  el teorema de Tales, semblança de triangles (posició de Tales i criteris), aplicació: distància a un punt inaccessible (mètode dels triangles en
  posició de Tales i dels triangles oposats pel vèrtex), semblança de triangles rectangles (criteris, ombres, mirall i l'altura sobre la hipotenusa
  amb els teoremes de l'altura i del catet) i problemes de semblança. El contingut és a `s123.py` (8.1-8.3, el de 2n amb els volums), `s4.py`,
  `s5.py` i `s67.py` (8.6-8.7; les ombres, el mirall i el fanal són els de 2n), amb `ck()`; `fig8.py` hi afig `inacc_tales()`, `inacc_cross()` i
  `alt_fig()`. Els ginys nous són l'amplària d'un riu (`w-inacc`, amb els dos mètodes) i l'altura i els catets d'un triangle rectangle
  (`w-alt`), i els entrenadors nous, `inacc`, `rect` i `mix` (problemes variats). Qüestionari de 22 preguntes a `quiz.js`. A `materials.js`
  és del bloc de geometria (il·lustració `tales`). La fitxa (`_eines/fonts-latex/4eso-a-t8/genera.py`, 76 exercicis en 7 seccions, bilingüe
  amb `T()`) és la de 2n amb exercicis de volums i de maquetes i amb les seccions noves 5 (distància inaccessible; s'hi passa el riu de
  l'antiga secció de problemes) i 6 (triangles rectangles); dins de cada secció, els exercicis s'ordenen per estrelles. `genera-es.py`
  l'executa en castellà:

```
python3 _eines/apunts/4eso-a-t8/build.py
cd _eines/fonts-latex/4eso-a-t8 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
```

- **Unitat 9 (Estadística Unidimensional, `4eso-a-t9`)**: adaptació a Matemàtiques A dels apunts de la unitat 10 de 1r ESO (`1eso-t10`), amb el mateix
  `build.py`, `comu.py`, `extra.css` i `app.js` (`window.FM49`). 8 apartats (9.1-9.8): població, mostra i variables (amb el mostreig aleatori,
  sistemàtic i estratificat), taules de freqüències amb dades aïllades ($f_i$, $F_i$, $h_i$, percentatges), taules amb dades agrupades (marca de
  classe i com es fan els intervals amb la regla de l'arrel), gràfics estadístics (barres, polígons, histogrames, sectors i pictogrames),
  paràmetres de centralització (també amb taules i amb dades agrupades: interval modal i interval medià), de dispersió (rang, desviació mitjana,
  variància, desviació típica i coeficient de variació), de posició (quartils i percentils, amb el criteri de la mediana: posició $k\cdot N/100$; si
  és entera, la mitjana d'eixa dada i la següent) i el diagrama de caixes (amb els valors atípics com a ampliació). El contingut és a `s123.py`
  (9.1-9.3, fet a partir del 10.1-10.3 de 1r), `s4.py` (10.4 i 10.5 de 1r), `s5.py` (10.6, 10.7 i 10.9 de 1r, amb les dades agrupades), `s6.py` i
  `s78.py` (nous); `comu.py` hi afig `var`, `pctl`, `five`, `ckr` (comprovació arrodonida) i el diagrama de caixes en SVG (`caixes`). Els ginys nous
  són agrupar dades en intervals (`w-grp`), la variància pas a pas amb una taula (`w-var`), els quartils i percentils (`w-quart`) i els diagrames
  de caixes de dos grups (`w-box`); `w-disp` ara també dona $\sigma$ i el $CV$. Entrenadors nous: `interval`, `marca`, `var`, `cv`, `quart`, `perc`,
  `boxread` i `boxpct`. Qüestionari de 25 preguntes a `quiz.js` (10 de 1r i 15 noves). A `materials.js` és del bloc d'estadística i probabilitat
  (il·lustració `estadistica`). La fitxa (`_eines/fonts-latex/4eso-a-t9/genera.py`, 54 exercicis en 8 seccions, bilingüe amb `T()`) calcula
  tots els resultats amb fraccions (`EQ`) o arrodonits (`AP`) i dibuixa barres, histogrames, sectors i caixes en TikZ (`tbar`, `thist`, `tpie`,
  `tbox`). `genera-es.py` l'executa en castellà:

```
python3 _eines/apunts/4eso-a-t9/build.py
cd _eines/fonts-latex/4eso-a-t9 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
```

- **Unitat 10 (Estadística bidimensional, `4eso-a-t10`)**: apunts nous amb la mateixa estructura que els de la unitat 9 (`build.py`,
  `comu.py`, `app.js`; l'`extra.css` s'afegeix després del de `4eso-a-t9`). 6 apartats (10.1-10.6): distribucions bidimensionals (parelles,
  taules simples i de doble entrada, relació funcional, estadística o cap), núvol de punts i centre de gravetat, correlació (sentit, força,
  lineal o no, correlació i causalitat), coeficient de correlació (covariància i $r$ amb una taula), recta de regressió (a ull i amb
  $y-\bar y=\frac{\sigma_{xy}}{\sigma_x^2}(x-\bar x)$) i estimacions (interpolació, extrapolació i fiabilitat). El contingut és a `s12.py`, `s3.py`,
  `s4.py` i `s56.py`; `comu.py` hi afig `bi()`, `rl()` i els núvols en SVG (`nuvol`, `nuvolR` per a núvols amb una $r$ exacta), i `app.js` en té
  una còpia (`cloud`, `cloudR`). Ginys: taula de doble entrada (`w-dbl`), núvol amb el centre de gravetat (`w-cloud`), el núvol segons $r$
  (`w-slide`), $r$ pas a pas (`w-cov`), endevina $r$ (`w-guess`), recta a ull amb la suma dels quadrats dels errors (`w-eye`), recta de
  regressió (`w-reg`) i estimacions amb la fiabilitat (`w-est`). Entrenadors `rel`, `cg`, `tipus`, `sentit`, `cov`, `rcalc`, `rint`, `recta`, `est` i
  `fiab`; qüestionari de 20 preguntes a `quiz.js`. A `materials.js` és del bloc d'estadística i probabilitat (il·lustració nova `regressio`).
  La fitxa (`_eines/fonts-latex/4eso-a-t10/genera.py`, 41 exercicis en 6 seccions, bilingüe amb `T()`) escriu els càlculs de $r$ i de la recta
  pas a pas a partir de les dades (`passos_r`, `passos_recta`) i dibuixa els núvols en TikZ (`nuvol`, `gen`):

```
python3 _eines/apunts/4eso-a-t10/build.py
cd _eines/fonts-latex/4eso-a-t10 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
```

- **Unitat 11 (Probabilitat, `4eso-a-t11`)**: feta a partir dels apunts de probabilitat de 2n ESO (`2eso-t11`, d'on venen `comu.py`,
  `extra.css` i la base d'`app.js`) i de 3r ESO (`3eso-t12`: operacions amb esdeveniments i propietats). 7 apartats (11.1-11.7):
  experiments (aleatoris i deterministes, espai mostral i experiments compostos), esdeveniments (tipus, unió, intersecció, contrari i
  incompatibles), probabilitat d'un esdeveniment (freqüències, llei dels grans nombres i propietats amb el contrari i la unió),
  càlcul de probabilitats (Laplace i la taula dels dos daus), experiències compostes (independents, regla del producte i «almenys un»
  amb el contrari), experiències dependents i probabilitat condicionada ($P(B/A)$, $P(A\cap B)=P(A)\cdot P(B/A)$ i dues urnes) i
  taules de contingència (condicionades a una fila o a una columna, de percentatges a la taula i a l'arbre, independència). El
  contingut és a `s12.py`, `s3.py`, `s4.py`, `s5.py`, `s6.py` i `s7.py`, amb fraccions exactes (`ck()`); molts problemes resolts són
  els de 2n i 3r. `app.js` (`window.FM411`) afig a l'app de 2n els ginys `w-ops` i `w-prop` de 3r i els nous `w-ind` (dues experiències
  independents) i `w-urn` (dues urnes); la taula de contingència (`w-cont`) té condicionades per files i per columnes i un context nou
  (vacuna). Entrenadors `det`, `tipus`, `ops`, `freq`, `falta`, `prop`, `lap`, `dice`, `ind`, `tree`, `dep`, `urn` i `cont`; qüestionari de
  20 preguntes a `quiz.js`. A `materials.js` és del bloc d'estadística i probabilitat (il·lustració `probabilitat`). La fitxa
  (`_eines/fonts-latex/4eso-a-t11/genera.py`, 56 exercicis en 7 seccions, bilingüe amb `T()`) parteix de la de 2n: els seus exercicis
  es guarden a `OLD` i es reparteixen amb `O(secció, número)`, i s'hi afigen els d'operacions, propietats, independència, probabilitat
  condicionada i taules a partir de percentatges; `apartats()` posa en línies independents (entorn `tasks` d'una columna) els
  apartats a), b)… que el text escriu en línia, tant als enunciats com a les solucions:

```
python3 _eines/apunts/4eso-a-t11/build.py
cd _eines/fonts-latex/4eso-a-t11 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
```

## 4t ESO Matemàtiques B

Els apunts de 4t ESO B parteixen dels de 1r Batx MI, simplificats (carpetes `_eines/apunts/4eso-b-tN`). Funcionen igual: el
contingut és a `contingut-*.html` (convencions ⟪va‖es‖en⟫), els ginys a `app.js`, l'estil propi a `extra.css`, i `build.py`
genera `materials/4eso-b/tN-….html`. A `fm-materials.js`, la unitat 1 de 4t ESO B és del bloc d'aritmètica, les unitats 2-4,
del d'àlgebra, i la 5, del de geometria.

Les fitxes (`_eines/fonts-latex/4eso-b-tN/genera.py`) mostren les estrelles de dificultat (com les d'ESO) i comparteixen les
eines de `_eines/fonts-latex/comu/eso4b.py`: `tasks`, intervals i recta real (`P`, `cup`, `cap`, `RI`, `recta`), `ck` per a
resultats exactes, `eq` per a comprovar amb sympy (numèricament) cada resultat escrit a mà, i `build`, que escriu la fitxa i
les solucions. `tasks(..., gap='12pt')` separa més les files d'apartats amb fraccions o sistemes.

- **Unitat 1 (Nombres reals, `4eso-b-t1`)**: 8 apartats (classificació dels nombres, intervals i semirectes, unió i
  intersecció, valor absolut, potències, radicals, racionalització i logaritmes) i 11 ginys; el valor absolut i els entorns
  (`w-abs`, `w-ent`) són els de 1r Batx MI, i hi ha tres ginys nous (simplificació de radicals `w-simp`, racionalització `w-rac`
  i canvi de base `w-cb`). Els apartats 1.6-1.7 són a `contingut-2b.html`. La fitxa té 36 exercicis: els 1-17 són els de la
  fitxa del departament («Fitxa 1 (1a Av.)»), amb la mateixa numeració, i les seccions 8-10 són d'ampliació per al Batxillerat
  (racionalització i sumes de radicals del departament, i exercicis nous de generatrius, intervals, valor absolut, potències,
  radicals, logaritmes i problemes).

```
python3 _eines/apunts/4eso-b-t1/build.py
cd _eines/fonts-latex/4eso-b-t1 && python3 genera.py && pdflatex t1-fitxa-exercicis.tex && pdflatex t1-fitxa-solucions.tex
```

- **Unitat 2 (Polinomis i fraccions algebraiques, `4eso-b-t2`)**: parteix dels apartats 2.1-2.4 de 1r Batx MI (`app.js` en
  conserva el motor de polinomis amb fraccions exactes: `parsePoly`, `pDivide`, `ruffini`, `factorPoly`). 7 apartats i 10 ginys;
  els nous són el binomi de Newton (`w-newton`, a 2.2), el teorema del residu (`w-res`), la cerca d'arrels enteres (`w-arr`),
  el m.c.d. i el m.c.m. (`w-mcm`) i les operacions amb fraccions algebraiques (`w-fop`), que fan servir `facList`, `mcdMcm` i
  `simpFrac`. La fitxa té 35 exercicis en 13 seccions: recull els de les fitxes del departament (Polinomis 1 i 2, Potències de
  binomis, Exercici 71 pàg. 68, Simplificació, Multiplicacions i divisions, Sumes i restes i Fitxa de fraccions algebraiques),
  ordenats per temes, i alguns de propis (arrels, m.c.d. i m.c.m., problemes). sympy calcula totes les solucions (`pt`, `ML`, `FT`).

```
python3 _eines/apunts/4eso-b-t2/build.py
cd _eines/fonts-latex/4eso-b-t2 && python3 genera.py && pdflatex t2-fitxa-exercicis.tex && pdflatex t2-fitxa-solucions.tex
```

- **Unitat 3 (Equacions i inequacions, `4eso-b-t3`)**: parteix dels apartats 2.5-2.10 de 1r Batx MI, separats en 10 apartats
  (segon grau, biquadrades, grau major que 2, factoritzades, amb fraccions, amb radicals, exponencials, logarítmiques,
  inequacions de primer grau i de segon grau o superior). 8 ginys: el de segon grau té dues instàncies (`w-quad` i `w-biq`,
  amb `quadW`), i són nous el de les equacions factoritzades (`w-feq`, amb `parseProd`) i el de les inequacions de primer
  grau (`w-lin`). La fitxa té 41 exercicis en 11 seccions (inclou equacions de segon grau i biquadrades amb
  parèntesis i denominadors; `red()` n'escriu la forma reduïda i `sols()` les solucions); `sol()` resol cada equació amb sympy (i, si sympy no pot, comprova
  les solucions i fa un escombratge numèric) i `ineq()` resol cada inequació i la compara amb l'interval escrit.

```
python3 _eines/apunts/4eso-b-t3/build.py
cd _eines/fonts-latex/4eso-b-t3 && python3 genera.py && pdflatex t3-fitxa-exercicis.tex && pdflatex t3-fitxa-solucions.tex
```

- **Unitat 4 (Sistemes d'equacions i inequacions, `4eso-b-t4`)**: parteix de la unitat 3 de 1r Batx MI. Els apartats 4.5-4.7
  (inequacions) en són còpia (`contingut-3.html`, amb el giny nou `w-sys1` de sistemes d'inequacions de primer grau); els de
  sistemes lineals 2x2 (4.1 mètode gràfic, `w-gr`; 4.2 substitució, igualació i reducció pas a pas, `w-met`), no lineals i
  problemes són nous. Sense el mètode de Gauss. La fitxa té 31 exercicis en 7 seccions (cada mètode amb sistemes amb denominadors i
  parèntesis, i sistemes no lineals amb arrels; `sis()` separa més les files dels sistemes amb fraccions); sympy resol i classifica cada sistema
  (`ls`, `kind`, `nls`) i els sistemes d'inequacions (`ineqs`), i `vx` comprova els vèrtexs de cada regió. Les figures del pla
  són a `_eines/fonts-latex/comu/regions.py` (còpia de les funcions de la fitxa de 1r Batx MI unitat 3).

```
python3 _eines/apunts/4eso-b-t4/build.py
cd _eines/fonts-latex/4eso-b-t4 && python3 genera.py && pdflatex t4-fitxa-exercicis.tex && pdflatex t4-fitxa-solucions.tex
```

- **Unitat 5 (Trigonometria, `4eso-b-t5`)**: parteix dels apartats 5.1-5.5 de 1r Batx MI, simplificats i reordenats en 8
  apartats seguint les fitxes del departament (graus i radians, raons d'un angle agut, raons de 30°, 45° i 60°, relacions
  fonamentals, triangles rectangles, problemes, angles qualssevol i reducció al primer quadrant), sense teoremes del sinus i
  del cosinus ni raons recíproques. `app.js` conserva sis ginys de 1r Batx MI (`w-rad`, `w-rt`, `w-rect`, `w-circ`, `w-find`
  i `w-red`) i n'afegeix dos: si hi ha un angle amb dues raons donades (`w-chk`, amb `chkPair`, exacte amb arrels o amb
  decimals) i la doble observació (`w-dob`, amb `dob`, al mateix costat o a costats oposats); `window.FM45` els exposa per a
  provar-los. A `fm-materials.js` la unitat 5 és del bloc de geometria. La fitxa té 64 exercicis en 8 seccions: recull els
  de les fitxes del departament (Trigonometria, Trigonometria II i III, exercicis d'entrega i del llibre) i n'afegeix de nous;
  `ap()` i `eq()` comproven cada resultat i les figures són TikZ.

```
python3 _eines/apunts/4eso-b-t5/build.py
cd _eines/fonts-latex/4eso-b-t5 && python3 genera.py && pdflatex t5-fitxa-exercicis.tex && pdflatex t5-fitxa-solucions.tex
```

- **Unitat 7 (Estudi de funcions, `4eso-b-t7`)**: parteix de la unitat 6 de 1r Batx MI, sense translacions ni composició i amb
  els dominis només de funcions polinòmiques, racionals i radicals. 9 apartats (concepte, imatges i antiimatges; domini i
  recorregut; talls; creixement i extrems; continuïtat; simetries; periodicitat; funció inversa; estudi complet d'una gràfica)
  i 8 ginys. Els intervals s'escriuen com a la resta de 4t, `(a,b)`. `fig.py` (figures fixes dels apunts i de les fitxes de les
  unitats 7 i 8) és en aquesta carpeta. La fitxa (bilingüe, com la de la unitat 6) té 40 exercicis en 9 seccions; sympy
  comprova talls, simetries i inverses i `ckdom` comprova numèricament cada domini.
- **Unitat 8 (Funcions elementals, `4eso-b-t8`)**: parteix de la unitat 7 de 1r Batx MI, sense cúbiques, radicals,
  trigonomètriques ni quocients de polinomis. 8 apartats (lineals, quadràtiques, proporcionalitat inversa, a trossos, valor
  absolut, exponencials, logarítmiques i problemes amb funcions) i 8 ginys. «Lineal» és y = mx + n, com a 3r d'ESO. La fitxa
  (bilingüe) té 45 exercicis en 8 seccions: tots els de la fitxa del departament («Fitxa 5: Funcions 2», marcats amb `(D)` al
  codi) i d'altres de nous, amb una secció de problemes. A `fm-materials.js`, les unitats 7 i 8 són del bloc d'anàlisi.

```
python3 _eines/apunts/4eso-b-t7/build.py && python3 _eines/apunts/4eso-b-t8/build.py
cd _eines/fonts-latex/4eso-b-t7 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
cd _eines/fonts-latex/4eso-b-t8 && python3 genera.py && python3 genera-es.py   # i pdflatex (dues vegades) dels quatre .tex
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
