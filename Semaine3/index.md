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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a2be6ae351d0a4afa69bdd4cbce8841e", "grade": false, "grade_id": "cell-4911a792a82448d7", "locked": true, "schema_version": 3, "solution": false}}

# Semaine 3: première classification automatique par apprentissage statistique

+++

## Consignes

Avant le mardi 6 février 23h59:
- [x] Déposez le TP n°3 (rendu noté)
- [x] Relisez les [diapos du cours 3 : Classification automatique par apprentissage statistique: VI-ME-RÉ-BAR](CM3.md)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e75a1131e3789fc97a1c12fcf29ea1b4", "grade": false, "grade_id": "cell-7b516d0f999cf0c7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## TP: classification automatique d'images de pommes et bananes

### Objectif

La **classification automatique** d'images par **apprentissage
statistique** sera le fil directeur des semaines à venir. Nous allons
commencer en douceur cette semaine, en reproduisant une analyse de
données préexistante dont l'objet est de classer des photographies
très simples de pommes et de bananes. Ce sera l'occasion de vous
familiariser avec le schéma **VI-ME-RÉ-BAR** -- [VI]sualisation,
[ME]sure, [RÉ]férence, [BAR]res d'erreur. Ce sera aussi l'occasion
de mettre en œuvre quelques **bonnes pratiques** pour la rédaction de
**documents exécutables reproductibles**.

En semaine 4 et 5 (mini projet 1), vous traiterez d'autres jeux de
données, en abordant l'**extraction d'attributs** et l'**utilisation
d'autres classificateurs**. Ce sera aussi l'occasion d'aborder le
traitement d'images.

Les semaines suivantes nous approfondirons le sujet pour vous amener
au projet final où vous classerez automatiquement des images de votre
cru.

<!--

### Consignes

Vous documenterez au fur et à mesure votre analyse de données dans le
document exécutable [analyse de données](2_analyse_de_donnees.md), en
suivant la trame fournie. Gardez notamment une trace des
expérimentations intermédiaires («nous avons essayé telle combinaison
d'attributs; voici les résultats et la performance obtenue»).

Votre travail devra être déposé avant le lundi 14 février 22h et sera
noté par correction automatique sur 5 points.

!-->

+++

### Au travail!

- [x] Relisez si nécessaire les
    [instructions](https://nicolas.thiery.name/Enseignement/IntroScienceDonnees/Devoirs/Semaine1/index.html#telechargement-depot-et-correction-des-tps)
    pour le téléchargement et le dépôt des TPs.
- [x] Téléchargez le sujet de TP `Semaine3`.
- [x] Ouvrez la feuille [index](index.md) pour retrouver ces consignes.
- [x] Consultez la section « Rapport » en fin de feuille.
- [x] Partez à la découverte des [bonnes pratiques](1_bonnes_pratiques.md).
- [x] Effectuez votre [analyse de donnees](2_analyse_de_donnees.md), en
    suivant la trame et les instructions fournies.
- [x] Choisissez le [jeu de données](3_jeux_de_donnees.md) que vous
	analyserez lors du mini projet 1 (Semaines 4 & 5)
- [x] Inscrivez vous avec votre binome pour le projet 1 dans le [document partagé](https://codimd.math.cnrs.fr/3f98v4-YT4CN2ktM6_g5lw?both).

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b5a7570f87720458cf29eee80aa46b1a", "grade": false, "grade_id": "cell-4911a792a82448dE", "locked": true, "schema_version": 3, "solution": false}}

### Rapport

Cette feuille joue aussi le rôle de mini-rapport qui vous permettra à
vous et votre enseignant d'évaluer rapidement votre avancement sur ce
TP.

Au fur et à mesure du TP, vous cocherez ci-dessus les actions que vous
aurez effectuées; pour cela, double-cliquez sur la cellule pour
l'éditer, et remplacez `- [ ]` par `- [x]`. Vous prendrez aussi des
notes ci-dessous. Enfin, vous consulterez la section « Revue de code »
ci-dessous pour vérifier la qualité de votre code.

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6563f058f4e26554f094663c22bb3f3c", "grade": true, "grade_id": "cell-4911a792a82448dF", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

Utilisation de la feuille de bonnes pratiques afin d'importer les données dans la feuille 2 pour leur analyse.

Mon cerveau est capable de dissocier les bananes des pommes grâce à leur forme tout d'abord puis ensuite d'une manière minoritaire grâce à leur couleur. Voyons comment nous pouvons traduire cela à l'aide de statistiques.

(solutions!=predictions).sum() Cette ligne de code renvoie un entier, le nombre d'éléments qui sont différents dans les deux Séries solutions et predictions. Elle utilise la vectorisation de Pandas et permet d'éviter d'implémenter une boucle.
On a donc (solutions!=predictions).sum())/len(solutions) = $\frac{e}{n}$ car $n =$ len(solutions).

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "db64aca779ecc9f6030d7442c300f254", "grade": false, "grade_id": "cell-4911a792a82448dG", "locked": true, "schema_version": 3, "solution": false, "task": false}}

#### Revue du code

##### Affichage du code des principales fonctions

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 20e2db344f56b0ad20c7361e2f23c8b5
  grade: false
  grade_id: cell-006fb180e6a86e73
  locked: true
  schema_version: 3
  solution: false
  task: false
---
from intro_science_donnees import show_source
from utilities import *
# Feuille 2_analyses_donnees.md
show_source(error_rate)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "abdfb5a24c36ae9a2cd982e3bcd4dba8", "grade": false, "grade_id": "cell-d21a1d7d40d56302", "locked": true, "schema_version": 3, "solution": false, "task": false}}

##### Conventions de codage

L'outil `flake8` permet de vérifier que votre code respecte les
conventions de codage usuelles de Python, telles que définies
notamment par le document [PEP
8](https://www.python.org/dev/peps/pep-0008/). Si la cellule suivante
affiche des avertissements, suivez les indications données pour
peaufiner votre code.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: af09a7ad3797f2e5dc5ec66e98ee34e2
  grade: true
  grade_id: cell-ce5cf24a9e83ff0e
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
from intro_science_donnees import code_checker
code_checker("flake8 utilities.py")
```

```{code-cell} ipython3

```
