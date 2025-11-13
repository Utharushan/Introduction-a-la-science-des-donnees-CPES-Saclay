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

+++ {"deletable": false, "editable": true, "nbgrader": {"cell_type": "markdown", "checksum": "668abcfabdc00f52d9c410b2392bff5f", "grade": false, "grade_id": "cell-9a7c1f7d80af137e", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

# Semaine 6

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "14ebb063add718d31a02eb637d024633", "grade": false, "grade_id": "cell-d97fff24c56a912b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Consignes

+++

Avant mardi 5 mars 23h59:
- [x] Relire les diapos du cours 6.
- [x] Finir le TP et le déposer sur GitLab (5 points)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e4445d6e4137ab89418f1bf64b3e0e4c", "grade": false, "grade_id": "cell-2c5576020df94493", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Support de cours

- [Diapos](CM6.md)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "222a059c28130aaba6795304c996d9d8", "grade": false, "grade_id": "cell-d5eab73cdc508877", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## TP

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3995315430c98a2a38dc89e06b22fc8a", "grade": false, "grade_id": "cell-b0c265fdc2363814", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Objectif

L'objectif de cette semaine est de rajouter à votre escarcelle
quelques outils de manipulation d'images en vue du deuxième projet:
ainsi, vous pourrez y traiter des jeux d'images plus complexes. Nous
verrons par exemple, lorsque l'image n'est pas bien cadrée, comment en
extraire la portion pertinente. Nous verrons aussi comment réaliser
des diaporamas simples avec Jupyter, en vue de votre soutenance de
projet.

N'oubliez pas d'appliquer les bonnes pratiques pour
[gérer vos devoirs](Nicolas.thiery.name/Enseignement/IntroScienceDonnees/ComputerLab/)
et [rédiger vos feuilles Jupyter](../Semaine3/1_bonnes_pratiques.md)!

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d8afefb67984b373277863a0c620d91f", "grade": false, "grade_id": "cell-229300fb372ae6d5", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Rapport

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "db44c1d27234caea97047c1b1a2e4900", "grade": false, "grade_id": "cell-ceddc6281cff411f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Au fur et à mesure du TP, vous cocherez ci-dessus les actions que vous
aurez effectuées; pour cela, double-cliquez sur la cellule pour
l'éditer, et remplacez `- [ ]` par `- [x]`. Vous prendrez aussi des
notes ci-dessous. Enfin, vous consulterez la section « Revue de code »
ci-dessous pour vérifier la qualité de votre code.

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b25e7560a2f116e66b38685c9039a7ce", "grade": true, "grade_id": "cell-25746e7990738300", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

#### En quelques mots, qu'avez-vous appris?

J'ai appris à manipuler des images, par exemple, lorsque l’image n’est pas bien cadrée, comment en extraire la portion pertinente. J'ai également appris à réaliser des diaporamas simples avec Jupyter.

#### Quelles difficultés avez vous éventuellement rencontrées?

J'ai trouvé que le calcul du barycentre et le fait de trouver les bonnes coordonnées pour le cropping n'étaient pas évident.

#### Qu'avez vous aimé ou moins aimé dans ce TP?

Le TP était assez guidé donc je n'ai pas été trop perdu.

#### Notes libres

+++

### Consignes

+++

% TODO: à supprimer en 2024-2025
- [x] (seulement si vous travaillez sur myDocker) Exécutez **une fois** la commande suivante qui corrige la configuration de votre terminal

```{code-cell} ipython3
! cp --no-clobber /etc/skel/.* ~/
```

- [x] Revenez sur le tableau de bord et téléchargez le devoir «Exercices». Pour le moment, vous trouverez quelques
      exercices sur les tableaux `numpy`. Ce dossier sera enrichi au fur et à
      mesure du semestre de nouveaux exercices. Ceux-ci seront à travailler
      chez-vous. Pour aujourd'hui, explorez les exercices proposés
      pendant cinq minutes.
- [x] Ouvrez la feuille [diaporamas](1_diaporamas.md) et suivez les
      instructions.
- [x] Ouvrez la feuille [arcimboldo](2_arcimboldo.md) et suivez les instructions.
- [x] Au fur et à mesure, vous mettrez à jour votre rapport ci-dessus.
- [x] Vous ferez la revue de code avec Flake8.

Bon TP!

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3cdeab84509ec542214d2b5022e65b4d", "grade": false, "grade_id": "cell-4911a792a82448dG", "locked": true, "schema_version": 3, "solution": false, "task": false}}

#### Revue du code

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f5be6a8e0307679bd09f7e9a8661ccb2", "grade": false, "grade_id": "cell-4911a792a82448dH", "locked": true, "schema_version": 3, "solution": false, "task": false}}

##### Affichage du code des principales fonctions

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 0b7f382020931cebd9159552dab83cff
  grade: false
  grade_id: cell-006fb180e6a86e73
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
---
from intro_science_donnees import show_source
from utilities import *
show_source(yellowness_filter)
show_source(color_correlation_filter)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1c0f01ca7b436223b24fc71e1f74ba08", "grade": false, "grade_id": "cell-d21a1d7d40d56302", "locked": true, "schema_version": 3, "solution": false, "task": false}}

##### Conventions de codage

L'outil `flake8` permet de vérifier que votre code respecte les
conventions de codage usuelles de Python, telles que définies
notamment par le document [PEP
8](https://www.python.org/dev/peps/pep-0008/). Si la cellule suivante
affiche des avertissements, suivez les indications affichées pour
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
