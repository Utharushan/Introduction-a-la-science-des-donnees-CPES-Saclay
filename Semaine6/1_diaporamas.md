---
jupytext:
  notebook_metadata_filter: rise
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
rise:
  auto_select: first
  autolaunch: false
  centered: false
  controls: false
  enable_chalkboard: true
  height: 100%
  margin: 0
  maxScale: 1
  minScale: 1
  scroll: true
  slideNumber: true
  start_slideshow_at: selected
  transition: none
  width: 90%
---

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ea5cac756cb589df60b23ae76971fabe", "grade": false, "grade_id": "cell-4911a792a82448d7", "locked": true, "schema_version": 3, "solution": false}, "slideshow": {"slide_type": "slide"}, "tags": []}

# Diaporamas interactifs avec Jupyter

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ec54c9a6cd0a9a982bce820e333f4ad8", "grade": false, "grade_id": "cell-8b77acf5d2044f9d", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": "fragment"}, "tags": []}

Dans cette feuille de travail, vous allez apprendre à 
produire des diaporamas interactifs pour vos présentations orales.

C'est ce que nous utilisons pour les notes de cours et ce que vous
pourrez utiliser pour la soutenance du projet final.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ccf218652d65165989db2c2b9b8f8df8", "grade": false, "grade_id": "cell-e55a0f76366ee6ec", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": "slide"}, "tags": []}

## Utiliser un diaporama

Cette feuille de travail est en fait un diaporama!

- Ouvrez la feuille en tant que Notebook (en haut à droite de la feuille).
- Activez le diaporama en cliquant sur <kbd>Affichage</kbd> > <kbd>Activer la palette de commandes</kbd> > <kbd>Start Deck</kbd> dans la barre d'outils.
- Parcourir l'ensemble du diaporama en explorant les fontionalités suivantes:
  - Naviguez avec les touches <kbd>Espace</kbd>, <kbd>Maj</kbd>-<kbd>Espace</kbd> ou les flèches en bas à droite pour changer de page.
    <!--
      - Consultez la documentation en cliquant sur le bouton <i class="fa fa-question" style="color: #727272;"></i>.
      - Suivez la documentation pour afficher la vue d'ensemble du diaporama (*overview*) puis revenir.
      - Suivez la documentation pour cacher puis afficher à nouveau les boutons.
    !-->
  - Utilisez <kbd>Control</kbd>-<kbd>+</kbd> et <kbd>Control</kbd>-<kbd>-</kbd> pour ajuster la taille des fontes.
  - Exécutez les cellules de code (sans avancer à la cellule suivante) avec les boutons <kbd>Control</kbd>-<kbd>Entrée</kbd>
  - Quittez le diaporama en appuyant sur le bouton orange («Exit Deck») entre les flèches en bas à droite.
<!--
  - Cliquez sur l'icône <i class="fa fa-pencil-square" style="color: #727272;"></i> pour lancer le tableau noir.
  - Cliquez sur l'icône <i class="fa fa-pencil" style="color: #727272;"></i> pour dessiner sur les diapos.
  - Cliquez sur l'icône <i class="fa fa-times-circle" style="color: #727272;"></i> pour quitter le tableau noir ou les diapos.
!-->
- Ouvrez les [notes de cours](CM6.md) comme un diaporama.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fa1d0e8aa3ee42ed01cbfe95dabd482c", "grade": false, "grade_id": "cell-f3f6ad1e405c3005", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": "slide"}, "tags": []}

## Éditer un diaporama
- Quittez le plein écran.
- Dans le barre de droite, cliquez sur l'icône <i class="fa fa-gears" style="color: #727272;"></i> pour ouvrir l'inspecteur de propriétés et les *Common Tools. Le menu déroulant «Slide Type» permet de définir le rôle de la cellule actuellement sélectionnée. Cette année vous utiliserez:
  - Diapositive (*Slide*): commence une nouvelle diapo.
  - Extrait (*-*): la cellule se rajoute à la diapo en cours.
  - Sauter (*Skip*): la cellule n'apparaît pas dans les diapos.
- Utilisez le bac à sable ci-dessous pour explorer les différents rôles et leur effet.

- On ne recommande pas l'utilisation de *Note*, *Subslide* et *Fragment* qui ont un comportement instable en 2024.

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

## Bac à sable
La suite de cette feuille contient une succession de cellules sans signification pour vous
servir de bac à sable. Vous pouvez en rajouter de nouvelles à votre convenance. 

Vous ne comprenez pas les textes? Pour savoir pourquoi, consultez
l'article [Lorem Ipsum](https://fr.wikipedia.org/wiki/Lorem_ipsum).

+++ {"editable": false, "slideshow": {"slide_type": "slide"}, "tags": []}

## Bla bla bla
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
---
39 + 1
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
---
40 + 1
```

+++ {"editable": true, "slideshow": {"slide_type": ""}, "tags": []}

Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a450835e317da9d6a9e379c8d30621d9", "grade": false, "grade_id": "cell-ca0131f59521fce9", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

## The end of the universe

Vous êtes venus jusqu'ici? Bravo! Affectez 42 à la variable `ultime` pour marquer un point :-)

Ouvrez ensuite la feuille [arcimboldo](2_arcimboldo.md), après avoir mis à jour votre rapport.

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 1515e38b3a3d35aa5656b7a094cc813b
  grade: false
  grade_id: cell-0fcaec8b81d7a78b
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
ultime = 42
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: f6f1ce00c13dab615d2679e1c80a7a61
  grade: true
  grade_id: cell-963f3a9626ae1519
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
assert ultime == 42
```
