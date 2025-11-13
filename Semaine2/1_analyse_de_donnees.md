---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d6aea3002ca0fafcee45e60068a142d4", "grade": false, "grade_id": "cell-6a641665ea50c56d", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}}

# Analyse de données sur la biodiversité des parcs nationaux américains

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d2b7e15c2a4b66f4f5432f246bd1d10f", "grade": false, "grade_id": "cell-6a641665ea50c56e", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}}

## Introduction

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "aa9f0d065b674118d65f8b10f2869aa3", "grade": false, "grade_id": "cell-6a641665ea50c56f", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}}

L'objectif de ce TP est d'étudier la biodiversité au sein de parcs nationaux. Pour cela nous utiliserons des données d'observations de plusieurs espèces dans différents lieux.

En science des données vous devrez préparer les données, les analyser (statistiquement) et produire des figures pertinentes dans l'objectif de répondre à différentes questions.

:::{admonition} Sources

Les fichiers `Observations.csv` et `Species_info.csv` sont issus
originellement d'un projet de
[Kaggle](https://www.kaggle.com/code/karthikbhandary2/biodiversity-analysis/notebook).

Remarques: les données pour ce projet sont inventées bien
qu'*inspirées* par des données réelles.

:::

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5eff63e9b178106b2b3103aefd274965", "grade": false, "grade_id": "cell-6ad4374b3e1cc45d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Objectifs du projet

Vous êtes deux analystes de la biodiversité pour le service des parcs nationaux. Le service veut assurer la survie des espèces en péril et maintenir le niveau de biodiversité au sein de leurs parcs. Par conséquent, vos principaux objectifs seront de comprendre les caractéristiques des espèces et leur état de conservation, ainsi que ces espèces et leurs relations avec les parcs nationaux. Quelques questions qui se posent :

-   Quel animal est le plus répandu ? Quel parc possède le plus d'espèces ?
-   Quelle est la répartition des statuts de conservation des espèces ?
-   Certains types d'espèces sont-ils plus susceptibles d'être menacés ?

### Chargement des données

Ce TP contient deux ensembles de données. Le premier fichier CSV (*comma separated values*) contient des informations sur chaque espèce et un autre contient des observations d'espèces avec des emplacements de parc. Ces données seront utilisées pour répondre aux questions ci-dessus.

### Analyse des données

Des statistiques descriptives et des techniques de visualisation des données seront utilisées pour mieux comprendre les données. L'inférence statistique sera également utilisée pour tester si les valeurs observées sont statistiquement significatives. Certaines des mesures clés qui seront calculées incluent :

1.  distributions,
2.  comptage,
3.  relation entre les espèces,
4.  état de conservation des espèces.

### Évaluation et conclusion

Enfin, nous reviendrons aux questions posées. A-t-on pu répondre à toutes les questions? Peut-on aller plus loin? Nous réfléchirons aux limites et nous verrons si l'une des analyses aurait pu être effectuée à l'aide de méthodes différentes.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8b6f3d4436c1a1179eed971bf7b3c498", "grade": false, "grade_id": "cell-e7f5611c49adea51", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Chargement des données

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: a9f6f810d06d66d8d4bf22dc3f15a11d
  grade: false
  grade_id: cell-c1bfa68a968d0c01
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "43e687d383113b8663936192861a8bb6", "grade": false, "grade_id": "cell-e7f5611c49adea52", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Chargez les fichiers `media/species_info.csv` et
`media/observations.csv` sous forme de tables (*data frames*) appelées
`species` et `observations` respectivement.

**Indication:** La fonction `.head()` permet d'avoir un apercu du
contenu de chaque table.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: d405d413540b91ed5abd5aa99346bdfa
  grade: false
  grade_id: cell-867461a5b5ba53e2
  locked: false
  schema_version: 3
  solution: true
  task: false
---
species = pd.read_csv("media/species_info.csv", sep=",")

species.head()
```

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: cd64e94d6bc7a5fa41beac1b71b27f07
  grade: false
  grade_id: cell-48c4226568856ec4
  locked: false
  schema_version: 3
  solution: true
  task: false
---
observations = pd.read_csv("media/observations.csv", sep=",")

observations.head()
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 3082227b6de8573028b1fadc2275ddbb
  grade: true
  grade_id: cell-4cabc03db76dbe7a
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert isinstance(observations, pd.DataFrame)
assert isinstance(species, pd.DataFrame)
assert observations.shape == (23296, 3)
assert species.shape == (5824, 4)
assert (observations.isna()).any(axis=None)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "68a89bd7b8d8acd023d6881845ecdc47", "grade": false, "grade_id": "cell-33d2c44e29b0dadb", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Caractéristiques des jeux de données

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "215d71d694739dbda4bcbc81f0292309", "grade": false, "grade_id": "cell-33d2c44e29b0dada", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Quelles sont les dimensions des jeux de données?

:::{admonition} Consigne

Vous utiliserez la cellule de code ci-dessous pour mener les calculs
dont vous aurez besoin, puis vous rédigerez votre réponse dans la
cellule de texte qui suit, sous forme de phrase complète explicitant
les nombres de lignes et de colonnes.

Vous procéderez de même dans tout le reste du TP.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 36ecd4e0d574d0693bb568b6ea22bc58
  grade: true
  grade_id: cell-a9e1b8d3f6fe6b04
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
---
species.info()
observations.info()
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "52c31ef63659a7f1b763ffa2e6fc57e5", "grade": true, "grade_id": "cell-3af14f238a7ea5d1", "locked": false, "points": 2, "schema_version": 3, "solution": true, "task": false}}

Les dimensions de la table `species` sont de $5824$ lignes pour $4$ colonnes (category, scientific_name, common_names, conservation_status).
Les dimensions de la table `observations` sont de $23296$ lignes pour $3$ colonnes (scientific_name, park_name, observations).

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "251cd1220f13ff55293c50f782c5d106", "grade": false, "grade_id": "cell-65b6bfd5b959b473", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Jeu de données `species`

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ea1152541d875ae2e94fb8330baf6f9a", "grade": false, "grade_id": "cell-65b6bfd5b959b474", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Il est temps d'explorer un peu plus en profondeur la table
`species`.
1.  Répondez aux questions suivantes :
    - Combien y a-t-il d'espèces différentes?
    - Ce nombre est-il égal aux nombre de lignes? Pourquoi?
    - Proposez des hypothèses permettant d'expliquer cette observation.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 230c0e7decd8c74f4700cbec51fe325e
  grade: true
  grade_id: cell-8e409954360e88d1
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
---
len(species.groupby("scientific_name"))
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d2bac3f627d4434e8affc7d52da6e9a9", "grade": true, "grade_id": "cell-035e76b795b14676", "locked": false, "points": 4, "schema_version": 3, "solution": true, "task": false}}

Au total, il y a $5541$ espèces différentes dans notre jeu de données.
Le nombre d'espèces qui est de $5541$ n'est donc pas égal au nombre de colonnes qui est de $5824$. Cela est sûrement dû au fait qu'il peut y avoir des doublons parmi notre jeu de données. En effet, la méthode _groupby( )_ enlève les doublons. 
Ces doublons peuvent alors probablement être expliqués par le fait qu'il peut y avoir une espèce qui appartient à plusieurs catégories différentes, une espèce qui possèdent des noms communs différents ou l'état de conservation d'une espèce (le fait qu'elle soit en voie d'extinction ou non par exemple).

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2de815c5c2494860a6a0e707ca39618f", "grade": false, "grade_id": "cell-8d27ed348b4a754f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

2.  Calculez dans la variable `ncat` le nombre de catégories présentes
    dans la table. À quoi cette colonne correspond-t-elle?

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 76ba4a6ac42e6dfe979435d57839ffd4
  grade: false
  grade_id: cell-5513563a0941f609
  locked: false
  schema_version: 3
  solution: true
  task: false
---
ncat = len(species.groupby("category"))
ncat
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bbfcd461acde3ab870ea089e37436adb", "grade": true, "grade_id": "cell-56c4d364a6c3ddfa", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

Le nombre de catégories présentes dans la table `species` est de $7$. Cette colonne correspond à la classe de l'animal qu'il soit par exemple un mammifère, un oiseau ou encore un reptile.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 15d18068b2c191ddb736748047fdf519
  grade: true
  grade_id: cell-18fc7ac0ca95a6a6
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert ncat**2+32 == 81
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "64c978b805f5b83d4457537478791870", "grade": false, "grade_id": "cell-ecbf69c48c0617bf", "locked": true, "schema_version": 3, "solution": false, "task": false}}

3.  Calculez dans l'objet `species_cat` le nombre d'espèces par
    catégorie. Vous utiliserez la méthode `groupby` vue en
    cours. Faites un barplot pour représenter ce résultat. Quelle
    catégorie a le plus d'espèces? Est-ce surprenant?

:::{admonition} Remarque

Les Vascular Plant correspondent aux
[Trachéophytes](https://fr.wikipedia.org/wiki/Tracheophyta) et
regroupent les plantes à fleurs
[Angiospermes](https://fr.wikipedia.org/wiki/Angiosperme). Les
Nonvascular plant correspondent aux [plantes
non-vasculaires](https://fr.wikipedia.org/wiki/Plante_non_vasculaire)*

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: e76d82cce290c26425e632d6c599e88b
  grade: true
  grade_id: cell-248b4d376d7716c4
  locked: false
  points: 3
  schema_version: 3
  solution: true
  task: false
---
species_cat = species.groupby("category").count()["scientific_name"]
species_cat.plot(kind='bar')
plt.xlabel("Catégorie")
plt.ylabel("Nombre d'espèces")
plt.title("Nombre d'espèces différentes au sein d'une même catégorie")
species_cat
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 2124fe9d122afd98ec9b40bf6705956d
  grade: true
  grade_id: cell-42a30a9eee9814c4
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert isinstance(species_cat, pd.Series)
assert species_cat.size == 7
assert species_cat['Bird']>20
```

+++ {"deletable": false, "editable": true, "nbgrader": {"cell_type": "markdown", "checksum": "908b5734068425caa817500a174c11c6", "grade": true, "grade_id": "cell-0d83f9d55e19a5c7", "locked": false, "points": 1, "schema_version": 3, "solution": true, "task": false}, "slideshow": {"slide_type": ""}}

La catégorie ayant le plus d'espèces est celle des **Vascular Plant** avec un total de $4470$. Le jeu de données concernant la biodiversité au sein de parcs nationaux, il n'est pas si surprenant que la catégorie la plus représentée soit celle des Vascular Plant.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fce5709c10a7ed60ef3a3af083bf0b76", "grade": false, "grade_id": "cell-d8c24200712072c6", "locked": true, "schema_version": 3, "solution": false, "task": false}}

4.   Créer la variable `species_status`qui contient les différents
    statuts possibles de ces espèces. Dans un paragraphe de texte,
    décrivez chacune de ces catégories. A votre avis, que signifie une
    valeur `nan`?

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 45c49e1d4227a5c1e51d91257f303abd
  grade: false
  grade_id: cell-7c7a5b388b6a587e
  locked: false
  schema_version: 3
  solution: true
  task: false
---
species_status = species["conservation_status"].unique()
species_status
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: f6665d54889d592bc7a3577df605fb00
  grade: true
  grade_id: cell-1cde562156519625
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
import hashlib
assert hashlib.md5(species_status[1].encode("utf-8")).hexdigest() == '5b98e09fa16ca9ffb8a4e6481fab1ef7'
assert hashlib.md5(species_status[2].encode("utf-8")).hexdigest() == 'e8ffc938d2592b28a666523cc1c80a5a'
assert hashlib.md5(species_status[3].encode("utf-8")).hexdigest() == '667cebca285ad56866f34c25309d99f3'
assert hashlib.md5(species_status[4].encode("utf-8")).hexdigest() == 'dd283e78058345d5e2ad72b7c7769579'
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f5112434eb167090dcb3b5fd4e6fc647", "grade": true, "grade_id": "cell-4ca50000b3bce35a", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

Les différents status possibles pour ces espèces sont :
- **'Species of concern'** pour des espèces qui sont particulièrement vulnérables mais qui ne remplissent pas les critères d'une espèce en danger ou menacés.
- **'Endangered'** pour des espèces en voie de disparition.
- **'Threatened'** pour des espèces susceptibles d'être menacées d'extinction dans un avenir prévisible
- **'In recovery'** pour des espèces précedemment en danger ou menacés au point qu'elles ne nécessitent plus d'aucune mesure de protection
- **'nan'** signifie que ces espèces n'ont aucun statut de conservation en particulier. Cela est peut être dû au fait qu'elles ne sont pas menacées ou en danger d'extinction.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "95797af20b64887b6d9ccbd37af22d5d", "grade": false, "grade_id": "cell-2ecf922e2d9a9904", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Jeu de données `observations`

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "01da75a8df6d137323341f62c84e98a8", "grade": false, "grade_id": "cell-2ecf922e2d9a9905", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On passe à l'observation de l'autre table, `observations`.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: bf6221893b64a382f769759b49ee3545
  grade: false
  grade_id: cell-a393a50850f08b68
  locked: true
  schema_version: 3
  solution: false
  task: false
---
observations.describe(include="all")
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "18eea5a46640f6211766e87b7a019c9e", "grade": false, "grade_id": "cell-a1af70876ffbc084", "locked": true, "schema_version": 3, "solution": false, "task": false}}

1.   À partir de la commande ci-dessus répondez aux questions suivantes :

    - Décrivez le contenu de la colonne `observations`.
    - Combien y a-t-il de données manquantes dans la table `observations`?
    - Combien d'espèces ont été vues au Yosemite?

**Rappel:** utilisez systématiquement des phrases complètes.

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "36cb000f1e594f89894e262ada1ae603", "grade": true, "grade_id": "cell-a5b1befcc2103d06", "locked": false, "points": 3, "schema_version": 3, "solution": true, "task": false}}

La colonne `observations` contient le nombre d'observations qui ont été faites au sein de parcs nationaux, leur moyenne, leur écart-type, leurs extremums et enfin leurs quartiles.
Il y a $17$ données manquantes dans le tableau mais cela est normal comme elle correspondent à des moyennes ou des écarts-types de données qui ne sont pas des nombres.
Au total, $5824$ espèces ont été vues au Yosemite.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5b2e098dd3fe761690fd526439b92058", "grade": false, "grade_id": "cell-b312eba78f698844", "locked": true, "schema_version": 3, "solution": false, "task": false}}

2.  Indiquez dans `npark` le nombre de parcs étudiés. Où se
    situent-ils (faites une recherche internet)?

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 8e2195043c79311b7c372135a4914bed
  grade: false
  grade_id: cell-c8ad74a1e0672681
  locked: false
  schema_version: 3
  solution: true
  task: false
---
npark = len(observations["park_name"].dropna().unique())
park = observations["park_name"].dropna().unique()
npark, park
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: a94adf736341de5ba4fdcc64c10a610d
  grade: true
  grade_id: cell-ad9440d5f3e79eee
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert npark**2+93 == 109
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ef7b983269ed1413ddad62a5ed22736b", "grade": true, "grade_id": "cell-09589dc8f6717a02", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

Le nombre de parcs étudiés est donc de $4$, il s'agit de :
- **'Great Smoky Mountains'** qui se situe aux États-Unis, dans les États du Tennessee et de la Caroline du Nord.
- **'Yosemite'** qui se situe dans les montagnes de Sierra Nevada, dans l'est de l'État de Californie.
- **'Redwood'** qui se situe aux États-Unis, sur la côte nord de la Californie, entre les localités d'Eureka et de Crescent City.
- **'Yellowstone'** qui se situe  à cheval sur trois États : au nord-ouest du Wyoming (pour 96 % de sa surface) et, marginalement, au sud-est de l'Idaho (en bordure de la forêt nationale de Caribou-Targhee) et au sud-ouest du Montana (adjacent à la forêt nationale de Gallatin).

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "aa78d8c571028a699fd2a62e1f7c71c3", "grade": false, "grade_id": "cell-fa922f17285fd65e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

3.  Indiquez dans `speciesMax` le nom scientifique de l'espèce la plus
    observée. Quel est son nom dans le langage courant?

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 24db69ae408f05f1c9d3b9046ad4eea4
  grade: false
  grade_id: cell-3d211c55f2065e25
  locked: false
  schema_version: 3
  solution: true
  task: false
---
speciesMax = observations.groupby('scientific_name')["observations"].sum()
speciesMax[speciesMax == max(speciesMax)]
speciesMax = 'Streptopelia decaocto'
nomCourant = species["common_names"][species["scientific_name"]=='Streptopelia decaocto']
nomCourant = 'Eurasian Collared-Dove'
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: e035c20ef8cc1b0ca080fb9ff31d8555
  grade: true
  grade_id: cell-03dc827892b56b10
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert hashlib.md5(speciesMax.encode("utf-8")).hexdigest() == 'eb0f1d26ae3ad8053d8291c2c24ad349'
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "c5ee626604f6ea8ad58bc427465509e1", "grade": true, "grade_id": "cell-629835ce3100c1ba", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

Le nom scientifique de l'espèce la plus observée est **'Streptopelia decaocto'** et son nom dans le langage courant est **'Eurasian Collared-Dove'**.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1e5442b712e07b333a002dccff305b86", "grade": false, "grade_id": "cell-aeea34fbde0ece03", "locked": true, "schema_version": 3, "solution": false, "task": false}}

4.  Mettez dans l'objet `parkMax` le nom du parc dans lequel on trouve
    le plus d'observations.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: c8c052c7eeccdf774a74759cf2792102
  grade: false
  grade_id: cell-b5754761e45f4156
  locked: false
  schema_version: 3
  solution: true
  task: false
---
park = observations.groupby('park_name')["observations"].sum()
parkMax = 'Yellowstone'
park
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 94f05228a7d1fdefe7297caf0d3d92cf
  grade: true
  grade_id: cell-d1d16aef256c4519
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert hashlib.md5(parkMax.encode("utf-8")).hexdigest() == '5702641a382396a92985fd8020739b63'
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "38b9bb5798ccb4f1542c220ec0bcfb87", "grade": false, "grade_id": "cell-2239335d40bf00dc", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Analyse des données

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5421763bb4240f69fea0e49017922996", "grade": false, "grade_id": "cell-2239335d40bf00dd", "locked": true, "schema_version": 3, "solution": false, "task": false}}

La première étape est de nettoyer et préparer les données.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "451273024316050ce6a38648c316c09b", "grade": false, "grade_id": "cell-5e82c6617c8b8e03", "locked": true, "schema_version": 3, "solution": false, "task": false}}

1.  Y a-t-il des valeurs manquantes dans la table `observations`?
    Supprimez les lignes avec des données manquantes et stockez le
    résultat dans `observations_cleaned`

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: e5b0cc86615b2c080c998464c74c452e
  grade: false
  grade_id: cell-cdbcc205f67fcc29
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
---
observations_cleaned = observations.dropna()
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: ef170be33bcff63bed13f4cf8c34b3f8
  grade: true
  grade_id: cell-08c0e8b6aa9253d0
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert observations_cleaned.shape == (23291, 3)
assert (observations_cleaned.notna()).all(axis=None)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "be6af578ade44ef905ad4f0cb49cb8e0", "grade": false, "grade_id": "cell-16c3c3af53c81683", "locked": true, "schema_version": 3, "solution": false, "task": false}}

2.  Dans la colonne `conservation_status` de la table `species`,
    remplacez les valeurs `NaN` par `No Intervention`. En effet, `NaN`
    signifie qu'il n'y a pas de spécification de conservation.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 049253136ca4b09bc8f9d38a2068e82d
  grade: false
  grade_id: cell-17dee0f233f349d3
  locked: false
  schema_version: 3
  solution: true
  task: false
---
species['conservation_status'] = species['conservation_status'].fillna('No Intervention')
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: bbeedb2dece41e6b14e6bb021899d2ca
  grade: true
  grade_id: cell-cafe9e81ddc3a8d9
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert (species.notna()).all(axis=None)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e9673fd5f775ac9395df337d15b17f95", "grade": false, "grade_id": "cell-417062c5e904254e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On calcule ensuite, sous la forme d'un tableau, le nombre d'espèces
pour chaque catégorie et chaque statut de conservation dans l'objet
`group_status`. Pour cela, on utilise *entre autres* les fonctions
`groupby()` et
[`unstack()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.unstack.html).

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 01a561f3f672a43a1e222ce40f61b1a0
  grade: false
  grade_id: cell-a5f0857ce456285d
  locked: true
  schema_version: 3
  solution: false
  task: false
---
group_status = species.groupby('category')['conservation_status'].value_counts().unstack()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2a088849fcf85e0b18294e9bdc57a9d3", "grade": false, "grade_id": "cell-9965320addb512f5", "locked": true, "schema_version": 3, "solution": false, "task": false}}

3.  ♣ Faites une figure pour représenter ces données sous forme de
    carte de chaleur (heatmap).

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 1062a91643d21970838e7a5573ccfc0b
  grade: false
  grade_id: cell-caf28f30ccf1d0a2
  locked: false
  schema_version: 3
  solution: true
  task: false
---
group_status.style.background_gradient(cmap='coolwarm', axis=None)

assert isinstance(group_status, pd.DataFrame)
assert group_status.shape == (7,5)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "66174c589018454e964fb94aa45d9518", "grade": false, "grade_id": "cell-8c36c732f4c67a98", "locked": true, "schema_version": 3, "solution": false, "task": false}}

4.  À quoi sert l'opération `unstack`?

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "82eb159e87fbee1276cbcc8e9a5d44a3", "grade": true, "grade_id": "cell-5f4bbe18f55d8e26", "locked": false, "points": 1, "schema_version": 3, "solution": true, "task": false}}

L'opération _unstack( )_ dans pandas permet de réorganiser un DataFrame en pivotant un niveau de hiérarchie des colonnes vers les index, rendant la structure des données plus accessible.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "30bd6b31e8ae0db60cdb165fd66478fc", "grade": false, "grade_id": "cell-335905fb91e7c7d4", "locked": true, "schema_version": 3, "solution": false, "task": false}}

5.  ♣ Dans la pratique, la plupart des espèces sont sans intervention,
    notamment pour les plantes. Refaites la figure en éliminant les
    espèces sans intervention. Gardez le nombre d'espèces par
    catégorie et par statut de conservation dans l'objet
    `group_status_conserv`.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: bc5425375456daec4516b716a6bcd100
  grade: false
  grade_id: cell-a6b086aba96f28b1
  locked: false
  schema_version: 3
  solution: true
  task: false
---
group_status_conserv = group_status.drop('No Intervention', axis = 1)
group_status_conserv.style.background_gradient(cmap='coolwarm', axis=None)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 8d86104500ea512d0c6e0ca180c11e19
  grade: true
  grade_id: cell-5103410b77ba6bb2
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert isinstance(group_status_conserv, pd.DataFrame)
assert group_status_conserv.shape == (7,4)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2c524f81fa84c798edefb8d13dd64458", "grade": false, "grade_id": "cell-b72dfe5082e963d5", "locked": true, "schema_version": 3, "solution": false, "task": false}}

6.  ♣ Faites une nouvelle figure à partir de `group_status_conserv` de
    type barplot avec l'option `stacked=True`.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: f82a6d04fe3ebdd561576352bc0a36f3
  grade: false
  grade_id: cell-94ac4fae78de88b4
  locked: false
  schema_version: 3
  solution: true
  task: false
---
group_status_conserv.plot.bar(stacked=True)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0982097dcfc20d6709f4e6c8aa219754", "grade": false, "grade_id": "cell-72d383ef1fc09d26", "locked": true, "schema_version": 3, "solution": false, "task": false}}

7.  A l'aide des analyses précédentes, répondez aux questions
    initiales en quelques phrases:

    - Quelle est la répartition des statuts de conservation des espèces?
    - Quel type d'être vivant est particulièrement en danger?

Commentez vos figures.

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "aaef064fe59059fd890c31afd3b511c8", "grade": true, "grade_id": "cell-32dc56440ea62824", "locked": false, "points": 4, "schema_version": 3, "solution": true, "task": false}}

Le statut de conservation des espèces est représenté par une grande majorité d'entre elles en tant que **'Species of Concern'** pour l'ensemble des catégories, suivie d'une répartition à peu près égale entre les espèces **'Threatened'** et **'Endangered'** pour les amphibiens, les poissons et les plantes vasculaires. En ce qui concerne les mammifères, une plus grande proportion d'espèces est classée comme **'Endangered'** plutôt que **'Threatened'**. En ce qui concerne les espèces **'In Recovery'**, elles sont présentes en proportions infimes chez les oiseaux et les mammifères, et absentes chez les autres catégories.

Le type d'être vivant le plus en danger semble être le mammifère, étant la catégorie qui compte le plus grand nombre d'espèces **'Endangered'** au total. Néanmoins, d'autres paramètres doivent être pris en compte. En effet, les oiseaux sont ceux qui présentent le plus grand nombre d'espèces classées comme **'Species of concern'** au total, et les poissons sont les seules espèces où une majorité est à la fois **'Endangered'** et **'Threatened'** par rapport à leurs statuts de conservation.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4af8484a09773b5ed8698dfcc5958dae", "grade": false, "grade_id": "cell-710ee6a737849476", "locked": true, "schema_version": 3, "solution": false, "task": false}}

#### Conservation

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "886462c83af8c1330143173983b09849", "grade": false, "grade_id": "cell-710ee6a737849477", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On passe maintenant à la question : quelles sont les espèces
plus susceptibles d'être suivies dans le cadre de la conservation?

-   Créez une nouvelle colonne `is_protected` qui vaut `False` pour
    toutes les espèces de statut `No Intervention` et `True` pour les
    autres.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 5f1e0d78909c3d904191b945da4522ab
  grade: false
  grade_id: cell-57e10ff3a863b08a
  locked: false
  schema_version: 3
  solution: true
  task: false
---
species.loc[species['conservation_status'] == 'No Intervention', 'is_protected'] = False
species.loc[species['conservation_status'] != 'No Intervention', 'is_protected'] = True
species    
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 1de62723abe34dd2c94cb44136766f34
  grade: true
  grade_id: cell-5d7e2ea1de145b45
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert species.shape == (5824, 5)
assert species['is_protected'].mean() < 0.033
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0a2b965cd699f7abb72256ddb72e7b56", "grade": false, "grade_id": "cell-a9dfe0ed57a1b03e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Pour chaque catégorie calculez la proportion d'espèces protégées et
mettez le resultat dans la variable `prop_cat`. Observez les
résultats.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: fc8416e3045bbf898b69778c0d2cff09
  grade: false
  grade_id: cell-d1863498f50a9e5e
  locked: false
  schema_version: 3
  solution: true
  task: false
---
prop_cat = (species.groupby("category").sum()['is_protected'])/(species.groupby("category").count()['is_protected'])
prop_cat.to_list()
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 1db3207d274c440f545ff446d3fa643a
  grade: true
  grade_id: cell-6cdcfc4eec90da41
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert prop_cat.mean() == 0.08455896094419532
assert prop_cat.max() == 0.17757009345794392
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f5f0b37403bd21246a41f26659470986", "grade": false, "grade_id": "cell-a08ac62e82d594db", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Évaluation

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "279454da0ed3e432fa5dc1568df54822", "grade": false, "grade_id": "cell-a08ac62e82d594dc", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous avons fini cette première partie de ce cours consacré aux
analyses de données, avec un accent mis sur la \[VI\]sualisation des
données. La semaine prochaine et jusqu'à fin du cours nous nous
concentrerons sur la classification d'image par apprentissage
statistiques, avec le schema d'analyse complet: VI-MÉ-BA-BAR.

Ce TP a permis d'analyser la composition en être vivants de quatre
parcs nationaux.

-  Répondez de facon succinte aux questions du début du TP:

      -   Quel animal est le plus répandu ? Quel parc possède le plus d'espèces ?
      -   Quelle est la répartition des statuts de conservation des espèces ?
      -   Certains types d'espèces sont-ils plus susceptibles d'être menacés ?

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "c929ab4ed24575ae3977d9adf9a00c72", "grade": true, "grade_id": "cell-4392623430a050aa", "locked": false, "points": 2, "schema_version": 3, "solution": true, "task": false}}

L'animal le plus répendu est le **'Eurasian Collared-Dove'**, le parc qui possède le plus d'espèce est le parc de **'Yellowstone'**.

Le statut de conservation des espèces est représenté par une grande majorité d'entre elles en tant que **'Species of Concern'** pour l'ensemble des catégories, suivie d'une répartition à peu près égale entre les espèces **'Threatened'** et **'Endangered'** pour les amphibiens, les poissons et les plantes vasculaires. En ce qui concerne les mammifères, une plus grande proportion d'espèces est classée comme **'Endangered'** plutôt que **'Threatened'**. En ce qui concerne les espèces **'In Recovery'**, elles sont présentes en proportions infimes chez les poissons et les mammifères, et absentes chez les autres catégories.

Certains types d'espèces sont plus susceptible d'être menacée, il s'agit de ceux qui ont le plus grand nombre de **'Species of Concern'**, c'est-à-dire les oiseaux principalement, mais aussi les plantes vasculaires et les mammifères.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3769fd2cfb961a6e61e3dcd7bba6287d", "grade": false, "grade_id": "cell-40da5b7e37b2d8cb", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}}

:::{admonition} Obtenez votre score

Bravo, vous avez fini le TP.

Depuis le tableau de bord :

1.  Déposez votre travail

2.  Vérifiez que votre binôme est bien configuré, et notamment que le
    dépôt principal, marqué par une étoile, est le bon. Au besoin,
    consultez la [page web](https://nicolas.thiery.name/Enseignement/IntroScienceDonnees/ComputerLab/travailBinome.html#indiquer-a-gitlab-que-vous-travaillez-en-binome)  
    **Rappel:** nous ne corrigerons que votre dépôt principal, tel que
    vous l'avez configuré!

3.  Consultez votre score.  
    **Rappel: ** le calcul du score peut prendre quelques
    minutes. Vous devez relancer le tableau de bord, ou consultez le
    dépôt pour le voir. Cliquez sur le badge avec le score pour avoir
    les détails et les commentaires. Les commentaires et donc le score
    total sera mis à jour seulement après correction par votre
    enseignant ou enseignante.

:::
