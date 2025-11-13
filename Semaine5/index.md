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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f6c8728c41191e222c533bab4bd2e89f", "grade": false, "grade_id": "cell-4911a792a82448d7", "locked": true, "schema_version": 3, "solution": false}, "slideshow": {"slide_type": ""}, "tags": []}

# Semaine 5

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3ca7dfc802742b9d6913cad7ec8ed74c", "grade": false, "grade_id": "cell-4911a792a82448d8", "locked": true, "schema_version": 3, "solution": false}, "slideshow": {"slide_type": ""}, "tags": []}

## Consignes

Avant mardi 27 février à 23h59:
- Relire les [diapos du cours 5](CM5.md)
- Rendu final du mini-projet 1. Vous devrez avoir déposé votre version
  finale du dossier `Semaine4` sur GitLab.
- Préparer les données pour le Projet 2.

+++ {"editable": true, "slideshow": {"slide_type": ""}, "tags": []}

## Travail à faire pendant les vacances

**Choix du jeu de données pour le projet 2 et préparation des données**: il consistera typiquement d'images ou photographies que vous aurez prises vous-même ou que vous aurez collectées sur internet. Les vacances sont l'occasion de prendre ces dites photos.
Quelques consignes:
- Les photos doivent toutes être au même format (paysage ou portrait). Le plus simple c'est qu'elles soient toutes prises par **le même téléphone portable**.

+++ {"editable": true, "slideshow": {"slide_type": ""}, "tags": []}

## TP: fin du mini-projet 1

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d698730c61d74678f94b191c7006a511", "grade": false, "grade_id": "cell-4911a792a82448d9", "locked": true, "schema_version": 3, "solution": false}, "slideshow": {"slide_type": ""}, "tags": []}

La semaine précédente, vous avez appliqué le schéma VI-MÉ-RÉ-BAR --
[VI]sualisation, [MÉ]trique, [Ré]férence, [BAR]res d'erreur -- pour la
classification de votre propre jeu de données. Vous avez :

- Fait quelques essais avec un des jeux de données fournis
- Déroulé l'analyse de données avec des attributs simples (par exemple
  rougeur et élongation) ainsi qu'un premier classifieur, afin
  d'obtenir votre référence: sans chercher à optimiser, quelle
  performance de classification obtient-on?
- Implémenté d'autres attributs et déroulé à nouveau l'analyse pour
  obtenir une meilleure performance.

### Objectifs

L'objectif de cette deuxième semaine de mini-projet est de mettre en
application le [cours de cette semaine](CM5.md) en explorant d'autres
classificateurs. Vous pouvez au choix:

- Implémenter l'un des classificateurs décrits dans le cours:
  - OneR(**)
  - KNN: k-plus proches voisins (*)
  - Arbre de décision (*)
  - Fenêtre de Parzen (*)
  - Perceptron (**)
- Essayer plusieurs autres [classificateurs fournis par Scikit-Learn](https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html) comme par exemple:
  - Autre méthode de noyau (****)
  - Perceptron multi-couche (****)

+++ {"deletable": false, "editable": true, "slideshow": {"slide_type": ""}, "tags": []}

### Au travail!


- [ ] Vérifiez votre inscription en binôme dans le [document
    partagé](https://codimd.math.cnrs.fr/3f98v4-YT4CN2ktM6_g5lw?both). La procédure pour le partage du TP est détaillée en [Semaine2](../Semaine2/index.md).
- [ ] Révisez les [bonnes pratiques](../Semaine3/1_bonnes_pratiques.md)
      vues en semaine 3.
- [ ] Partez à la découverte des [classificateurs](../Semaine4/5_classificateurs.md).
- [ ] Reprenez votre analyse de la semaine dernière dans la feuille
      [analyse de donnees](../Semaine4/4_analyse_de_donnees.md) avec vos propres
      classificateurs.

:::{seealso}

Pour en savoir plus et pour des suggestions sur comment travailler en
binôme, veuillez vous référer à la 
[page web](https://nicolas.thiery.name/Enseignement/IntroScienceDonnees/ComputerLab/travailBinome.html).

:::



### Barême indicatif /20

* 1_tableaux.md : 1,5 points 
* 2_images.md : 2 points 
* 3_features.md : 1 point
* 4_analyse_de_données.md : 10 points 
* 5_classificateur.md : 4 points (+ 3 points bonus pour le OneR)
* index (semaine 4) : 1,5 points
