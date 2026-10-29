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

A `1eso-t1`, `1eso-t2`, `1eso-t3`, `1eso-t4`, `1batx-mi-t5`, `2batx-ccss-t1`, `2batx-ccss-t5`, `2batx-ccss-t6`, `2batx-ccss-t7`, `2batx-ccss-t8`, `2batx-ccss-t9` i `2batx-ccss-t10` la fitxa i les solucions es generen totes dues des de `genera.py` (una sola llista d'exercicis):
edita-la, executa `python3 genera.py` i després compila els dos `.tex`.
Copia els PDF resultants a `materials/<curs>/` i enllaça'ls a `materials.js` (les solucions, amb `hidden: true`
si encara no han de ser visibles). Els fitxers auxiliars de LaTeX (`.aux`, `.log`, `.pdf`…) no es pugen al repositori.

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

Els apunts de 1r Batx MI de la unitat 5 (Geometria analítica en el pla, carpeta `1batx-mi-t5`) reaprofiten l'estil de les
unitats 4 i 9 de 2n Batx CCSS. Els ginys dibuixen un pla cartesià amb punts que es poden arrossegar (vectors, rectes, angles,
distàncies i el laboratori del triangle) i calculen amb fraccions exactes. A `materials.js` la unitat porta `num: "5"`, el número
dels apunts del departament (les unitats 1-4 encara no hi són). La fitxa (`_eines/fonts-latex/1batx-mi-t5/genera.py`) comprova
totes les solucions amb fraccions i en dibuixa algunes figures:

```
python3 _eines/apunts/1batx-mi-t5/build.py
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
