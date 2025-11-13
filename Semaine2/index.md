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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6981034dc6d705bef616168113b708f1", "grade": false, "grade_id": "cell-4911a792a82448d7", "locked": true, "schema_version": 3, "solution": false}}

# Semaine 2: premières analyses de données

## Cours

- Cours: [analyses de données](CM2.md)

## TP: votre première analyse de donnée

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1c5a8f4aecb10d2374433e04b7ff4b33", "grade": false, "grade_id": "cell-c35449a5f3f139fa", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Objectif

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f1e112254a250696e99ea50b0bc4562a", "grade": false, "grade_id": "cell-8ed723df6051a8b4", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Dans ce TP, vous allez réaliser en binôme votre première **analyse de
données**, pour répondre à des questions autour de la
biodiversité. Pour cela, vous vous appuierez sur de la **visualisation
de données** et des **tests statistiques simples**, à l'aide des
bibliothèques `Pandas`, `Numpy`, `Matplotlib` et `Seaborn`.

Suivant les bonnes pratiques pour la **Science Ouverte** et la
**Reproductibilité**, cette analyse sera documentée par un **rapport
d'analyse de données exécutable**: un document narratif détaillant
l'analyse, spécifiant pas-à-pas les traitements effectués, accompagné
de tous les artefacts requis pour reproduire les traitements: données,
code, dépendances logicielles.

Pour cette première analyse, nous vous fournissons la trame du
rapport. Votre travail sera de lire cette trame en détail, en
complétant au fur et à mesure les éléments manquants pour pouvoir
l'exécuter de bout en bout et en interpréter les résultats.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "89f59b38b7dfbe2274a42f49bcb8d69e", "grade": false, "grade_id": "cell-8dc4f3263114eb81", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Travail en binôme

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e719bd8612c68701c432d3f8e664e1ed", "grade": false, "grade_id": "cell-90c83ff3e456dff1", "locked": true, "schema_version": 3, "solution": false, "task": false}}

La procédure suivante vous facilitera la collaboration et nous
permettra de connaître les binômes, pour corriger et attribuer les
notes.

1.  Vérifiez votre inscription en binôme dans le [document
    partagé](https://codimd.math.cnrs.fr/3f98v4-YT4CN2ktM6_g5lw?both).
    Inscrivez-vous aussi si vous n'avez pas encore de binôme!

2.  Si vous ne l'avez pas déjà fait, téléchargez le devoir `Semaine2`.

3.  Déposez le devoir `Semaine2`. Vous noterez que l'interface du
    tableau de bord a légèrement changé: vous n'aurez à donner votre
    groupe que la première fois où vous déposerez.

Par défaut, lorsque vous déposez un devoir, il n’est accessible qu’à
vous et à l’équipe enseignante.

4.  Donnez accès à votre devoir à votre binôme, en utilisant l'action
    «Partage avec» du tableau de bord et en spécifiant son identifiant
    `prénom.nom`.

Votre enseignant ou enseignante corrigera votre TP sur la base de l'un
de vos deux dépôts.

5.  Avec votre binôme, choisissez lequel de vos deux dépôts sera le
    ***dépôt principal*** à corriger par l'équipe
    enseignante. Appelons A et B les deux membres de votre binôme, de
    sorte que A soit le propriétaire du dépôt principal.

6.  Membre B : depuis le tableau de bord utilisez l'action «Définir le
    dépôt principal» en spécifiant l'identifiant `prénom.nom` de A.

7.  Tous les membres : vérifiez le résultat de la manœuvre: après
    avoir relancé le tableau de bord, les identifiants `prénom.nom` de
    A et de B doivent apparaître pour le devoir, avec des liens vers
    leurs dépôts respectifs, et une étoile pour marquer le dépôt
    principal.


:::{attention}

Nous ne consulterons que le devoir de A : à charge pour vous de vous
assurer que celui-ci contient bien l'intégralité du travail du binôme!

:::

:::{seealso}

Pour en savoir plus et pour des suggestions sur comment travailler en
binôme, veuillez vous référer à la 
[page web](https://nicolas.thiery.name/Enseignement/IntroScienceDonnees/ComputerLab/travailBinome.html).

:::

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "620ca6629835f0dfdfb947f8d0b120e1", "grade": false, "grade_id": "cell-fe3106d721569081", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Consignes

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "38bdc313a899a0ee860b77bd634cc7cc", "grade": false, "grade_id": "cell-f9e10475f1a086eb", "locked": true, "schema_version": 3, "solution": false, "task": false}}

- Faites la feuille [1_analyse_de_donnees.md](1_analyse_de_donnees.md)
  et suivez les instructions.

Bon TP!

**Avant mardi 30 janvier à 23h59**:

- Relisez les diapos du cours 2.
- Finissez le TP et déposez le sur GitLab; il sera noté à la fois automatiquement et par vos enseignantes et enseignants (15 points)
