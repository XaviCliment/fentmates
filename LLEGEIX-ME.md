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
