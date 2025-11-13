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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "78560d6c76c41ce785423ed075900b5d", "grade": false, "grade_id": "cell-3876f910a24fe8ac", "locked": true, "schema_version": 3, "solution": false}}

# Quelques bonnes pratiques pour les documents exécutables

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8d0c9e1fad260f1b08060dceeb1242f1", "grade": false, "grade_id": "cell-3876f910a24fe8ad", "locked": true, "schema_version": 3, "solution": false}}

## Introduction

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b54852e2ef47c0a9c6c68ec1bba9273b", "grade": false, "grade_id": "cell-3876f910a24fe8ab", "locked": true, "schema_version": 3, "solution": false}}

Lors de la création d'un **document exécutable** -- tel que le rapport
d'analyse de données que nous allons explorer aujourd'hui -- le but
est de rendre le document aussi lisible que possible, en mettant en
évidence **ce qui** est calculé et en faisant abstraction des
**détails techniques** de **comment** il est calculé.

Avec les feuilles Jupyter, cela est généralement réalisé en
développant une collection d'utilitaires dans des **fichiers de code**
séparés. De la sorte, les détails techniques de ces utilitaires ne
polluent pas la lecture du document. Ils n'en restent pas moins
immédiatement accessibles pour étude plus approfondie: le lecteur peut
à tout moment utiliser l'*introspection* (en utilisant `?` après la
fonction, voir les exemples ci-dessous) pour consulter rapidement la
documentation et le code des utilitaires.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "54ea728e695953d333f49b32ab73ad58", "grade": false, "grade_id": "cell-3876f910a24fe8a7", "locked": true, "schema_version": 3, "solution": false}}

Des utilitaires pour l'ensemble du cours sont fournis dans le module
Python `intro_science_donnees` préinstallé sur le système. En outre, des
utilitaires dédiés au devoir en cours sont fournis dans le module
<a href="utilities.py">utilities.py</a> présent dans le dossier du devoir.

Certains de ces utilitaires sont
incomplets : vous serez invité à les compléter au fur et à mesure de
votre progression. Nous ne nous attendons pas à ce que vous soyez dès
maintenant en capacité de tous les réécrire vous-même; cependant, vous
devriez certainement les consulter et essayer de les comprendre.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8f039a74d016445d61def24e140fd995", "grade": false, "grade_id": "cell-3876f910a24fe8a8", "locked": true, "schema_version": 3, "solution": false}}

Rendre les données disponibles pour l'analyse peut également
nécessiter un certain soin. En général, c'est un sujet à part entière;
voir par exemple les [principes
FAIR](https://en.wikipedia.org/wiki/FAIR_data) (Findable, Accessible,
Interoperable, Reproducible) de la Science Ouverte. À l'échelle de
l'analyse que nous allons mener dans ce cours, la principale
préoccupation est de rendre les données facilement accessibles depuis
les feuilles Jupyter sans les dupliquer partout - et en particulier
dans vos espaces en salle de TP, sur JupyterHub et sur GitLab -- pour
économiser de l'espace de stockage. Aussi, les jeux de données sont
ils préinstallés avec la pile logicielle du cours.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bfec21b879770275b4888a5b862644ea", "grade": false, "grade_id": "cell-3876f910a24fe8a9", "locked": true, "schema_version": 3, "solution": false}}

## En pratique

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4dbf9003867699553b95cc8b21d89ffc", "grade": false, "grade_id": "cell-3876f910a24fe8aa", "locked": true, "schema_version": 3, "solution": false}}

Les commandes suivantes configurent Jupyter pour recharger
automatiquement les modules comme `utilities.py` chaque fois qu'ils
sont modifiés; ainsi il ne sera pas nécessaire de redémarrer le noyau
à tout bout de champ.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 7d49236810557fb2cdde6248fa11f168
  grade: false
  grade_id: cell-d230a57693ce2447
  locked: true
  schema_version: 3
  solution: false
  task: false
---
%load_ext autoreload
%autoreload 2
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "cb9f3b29dd7e8b5c26bb3e48bc5c7a41", "grade": false, "grade_id": "cell-571249fbcd43aec5", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Importons les fonctions `load_images` et `image_grid` du module `intro_science_donnees` et toutes les fonctions du module <a href="utilities.py">utilities.py</a> :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: ff0e15137ef78f039425e96019ca67f1
  grade: false
  grade_id: cell-bf9fd3310da94f48
  locked: true
  schema_version: 3
  solution: false
  task: false
---
from intro_science_donnees import *
from utilities import *
# Configuration intégration dans Jupyter
%matplotlib inline
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "293004f2a84560d830afa342bd0fe6d7", "grade": false, "grade_id": "cell-f82f534024dda6ec", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous pouvons maintenant utiliser l'introspection pour consulter, par
exemple, la documentation de `load_images`:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 43b37328830eb7347e795e51a92b7ed1
  grade: false
  grade_id: cell-abb04be0a4eb6e79
  locked: true
  schema_version: 3
  solution: false
  task: false
---
load_images?
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7338db6c8e5d589aeef42fdc089e0af5", "grade": false, "grade_id": "cell-f73f7746ecbf6699", "locked": true, "schema_version": 3, "solution": false, "task": false}}

voire pour étudier son code:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: c2c473f85cb92cf5b7c81250b1813024
  grade: false
  grade_id: cell-abb04be0a4eb6e80
  locked: true
  schema_version: 3
  solution: false
  task: false
---
load_images??
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d0689e1f2ad47c6ee67b97420dd501c2", "grade": false, "grade_id": "cell-096011a115f5d432", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Les jeux de données pour ce TP (et le projet 1) sont disponibles dans
le dossier suivant :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 90cb27439e31b8021d49d0d9a8f78674
  grade: false
  grade_id: cell-befee52b24f8481e
  locked: true
  schema_version: 3
  solution: false
  task: false
---
from intro_science_donnees import data
data.dir
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2d76e950e35240540630d0e6b148a0c2", "grade": false, "grade_id": "cell-26520376f6d56641", "locked": true, "schema_version": 3, "solution": false, "task": false}}

La liste des jeux de données disponibles peut s'obtenir ainsi :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 01e51b271b073e662abe32b6851db5b1
  grade: false
  grade_id: cell-1d13fa491f705b15
  locked: true
  schema_version: 3
  solution: false
  task: false
---
!ls {data.dir}
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a310b3feaf1a30957f1e8024be62d160", "grade": false, "grade_id": "cell-9f1c3ed8cbe8ba1d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Quelques explications: vous aurez reconnu la commande `ls` du shell,
et ce n'est pas un accident: lorsqu'une cellule commence par un `!`,
la commande est interprétée avec le shell au lieu de Python. Qui plus
est, un nom de variable Python apparaissant entre accolade dans la
commande shell, comme `{data.dir}` ci-dessus, est substitué par sa
valeur.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f20357f6272d058a44e7ecf588a1438b", "grade": false, "grade_id": "cell-4c11aaff08edefde", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Aujourd'hui nous nous intéressons au jeu de données
`ApplesAndBananasSimple` :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 81cc72d6e998531c087b02b88eb2761b
  grade: false
  grade_id: cell-18adc7a00f068617
  locked: true
  schema_version: 3
  solution: false
  task: false
---
import os.path
dataset_dir = os.path.join(data.dir, 'ApplesAndBananasSimple')
dataset_dir
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2ec17d4bb53251e19eba2a5537142fc0", "grade": false, "grade_id": "cell-63c7a97b588426e2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Il consiste en une collection d'images :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: db2cea0282a59f6f349f99bb358e6a67
  grade: false
  grade_id: cell-cc22fec0abbc0fe5
  locked: true
  schema_version: 3
  solution: false
  task: false
---
! ls {dataset_dir}
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9d6a22f9682309096940a7bf4926d642", "grade": false, "grade_id": "cell-d28985fb031c1550", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Chargez toutes ces images dans une variable `images` et
affichez les.  
**Indication :** consultez la documentation de `load_images` et de
`image_grid`.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 1089f76d4c93c07ca0a79e200c25a6fa
  grade: false
  grade_id: cell-64d11a9c5b549a05
  locked: false
  schema_version: 3
  solution: true
  task: false
---
images = load_images(dataset_dir, '*.png')
image_grid(images)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: ebe09d5fce18d401fff227b9e020abd1
  grade: true
  grade_id: cell-6d1f5ba575ac8265
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert isinstance(images, pd.Series)
assert len(images) == 20
assert images.index[0] == "a01.png"
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "753e8894bcc46e17979a4e1e70451d3c", "grade": false, "grade_id": "cell-71d5fd534593a041", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Rappelez-vous de la documentation : `images` est une série `Pandas`
indexé par les noms des images :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 6b1d5161cffe32d73d62c89e944e6d18
  grade: false
  grade_id: cell-21b845283df09413
  locked: true
  schema_version: 3
  solution: false
  task: false
---
images.index
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7efed6556adc9124c138c993a77d4b13", "grade": false, "grade_id": "cell-e0607854db13afb0", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Ainsi, vous pouvez récupérer une image individuelle soit par son nom,
soit par son numéro :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: de96aa498c97d662032fd1abaa954f61
  grade: false
  grade_id: cell-efa7b0ab9840d4b8
  locked: true
  schema_version: 3
  solution: false
  task: false
---
images['a03.png']
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: f8a9a76474f6317ab586b250c79bfd0d
  grade: false
  grade_id: cell-807f5ed20fd82f62
  locked: true
  schema_version: 3
  solution: false
  task: false
---
images.iloc[2]
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fdb4aba557fcfac4b5bb6c67663abfd0", "grade": false, "grade_id": "cell-d333e62c5bddb016", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Chargez maintenant dans la variable `bimages` les images dont le nom
commence par `b`. Affichez-les en utilisant leur nom de fichier comme
titre.  
**Indication** : si besoin, relisez les documentations !

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 185c48e671be65551730e93e99c35bee
  grade: false
  grade_id: cell-f54b13a2d97830c3
  locked: false
  schema_version: 3
  solution: true
  task: false
---
bimages = load_images(dataset_dir, 'b*.png')
image_grid(bimages)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 18018f37ca31de5c809f89dc87c42aef
  grade: true
  grade_id: cell-21b845283df09414
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert isinstance(bimages, pd.Series)
assert len(bimages) == 10
assert bimages.index[0] == "b01.png"
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a2e5f06c803c984fb80330d33b4272cd", "grade": false, "grade_id": "cell-58f6b655249dd9b7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Sections repliables

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "785f998ea14cba9b2827ace5f9720e0a", "grade": false, "grade_id": "cell-58f6b655249dd9b8", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Lors de la manipulation d'un long document comme un rapport, il
devient vite fastidieux de naviguer dans le document en faisant
défiler d'avant en arrière. L'extension Jupyter «Collapsible Headings»
permet de replier à volonté sections et sous-sections. Cette extension
est activée par défaut dans l'environnement du cours : cherchez le
triangle gris «<i class="fa fa-fw fa-caret-down" style="color: gray;"></i>»
ou «<i class="fa fa-fw fa-caret-right" style="color: gray;"></i>» à
gauche des titres de section et essayez de cliquer dessus.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e97e0b481f0538ac751ebf943598c851", "grade": false, "grade_id": "cell-66fa3a07cbc56b2a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Toutes les cellules ci-dessous (code ou texte) sont contenues dans une
section repliable.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 852562cb45d6f9e88f99c8e027376084
  grade: false
  grade_id: cell-bc5388ee9b241362
  locked: true
  schema_version: 3
  solution: false
  task: false
---
print("Hello")
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7d753540216688710e56fae3f1441d7d", "grade": false, "grade_id": "cell-58f6b655249dd9b6", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Conclusion

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d56662761dab8f74dc864f6ff72077ae", "grade": false, "grade_id": "cell-58f6b655249dd9ba", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Dans cette feuille, nous avons exploré quelques bonnes pratiques pour
la rédaction de documents exécutables. C'est un premier pas vers la
reproductibilité et la Science Ouverte!

Mettez à jour votre rapport dans la feuille `index.md` et déposez
votre travail sur GitLab (`submit`). Passez ensuite à la feuille
[analyse de données](2_analyse_de_donnees.md).

```{code-cell} ipython3

```
