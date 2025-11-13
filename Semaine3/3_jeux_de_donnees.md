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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "18c7334b328263f50028a0ed2c57f0b7", "grade": false, "grade_id": "cell-86380fd084769e80", "locked": true, "schema_version": 3, "solution": false, "task": false}}

# Jeux de données disponibles pour le projet 1

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "223d805a84ad990418805d7560debe26", "grade": false, "grade_id": "cell-c2fd6036df8ecb11", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Dans cette feuille, vous allez parcourir les jeux de données
disponibles et choisir celui que vous étudierez en Semaine 4
et 5 pour le mini projet.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 24c27ee8aa197ea9bbd0cd7403842ade
  grade: false
  grade_id: cell-638b8591a86d2f35
  locked: true
  schema_version: 3
  solution: false
  task: false
---
%matplotlib inline
%load_ext autoreload
%autoreload 2
import os
from utilities import *
from intro_science_donnees import data, load_images, image_grid
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: d05ae432ec7d927e7bb629830f56a341
  grade: false
  grade_id: cell-603f0e005a71785c
  locked: true
  schema_version: 3
  solution: false
  task: false
---
! ls {data.dir}
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bbff11ed347d80e42d362ba51096a613", "grade": false, "grade_id": "cell-65a29118d123c634", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Poules et canards

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 1fbba1528e04cb1bf06a608ca603264a
  grade: false
  grade_id: cell-4bd1153d315503ef
  locked: true
  schema_version: 3
  solution: false
  task: false
---
dataset_dir = os.path.join(data.dir, 'Farm')
images = load_images(dataset_dir, "*.jpeg")
image_grid(images, titles=images.index)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "745c260321fc496c732f9834592822a7", "grade": false, "grade_id": "cell-8ae6e1c8034faf85", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Paumes et dos de mains

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: c6216c71d2e8e5eae2de7046ca6eb35f
  grade: false
  grade_id: cell-aa92e20b30d4829d
  locked: true
  schema_version: 3
  solution: false
  task: false
---
dataset_dir = os.path.join(data.dir, 'Hands')
images = load_images(dataset_dir, "*.jpeg")
image_grid(images, titles=images.index)
```

+++ {"deletable": false, "editable": false, "heading_collapsed": true, "nbgrader": {"cell_type": "markdown", "checksum": "73d1d29e516e4547a8779f1d3549e8ed", "grade": false, "grade_id": "cell-933228e1040c967b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Smileys gais et tristes

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: c995abf2fa9813c40b6387cde9bfc7c5
  grade: false
  grade_id: cell-3c651c729aa65f4f
  locked: true
  schema_version: 3
  solution: false
  task: false
---
dataset_dir = os.path.join(data.dir, 'Smiley')
images = load_images(dataset_dir, "*.png")
image_grid(images, titles=images.index)
```

+++ {"deletable": false, "editable": false, "heading_collapsed": true, "nbgrader": {"cell_type": "markdown", "checksum": "8f0a67d037c13bb12ef0a66d795eebc3", "grade": false, "grade_id": "cell-15a0b989b1cd4c5b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Zéros et uns manuscrits

*Indications*: jeu de données très simple à classifier mais attention, c'est en noir et blanc donc certains attributs comme la redness ne peuvent pas etre calculés sur ce jeu de données

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: c807ec2807eef81b367168f8a0537387
  grade: false
  grade_id: cell-0e86999691136d40
  locked: true
  schema_version: 3
  solution: false
  task: false
---
dataset_dir = os.path.join(data.dir, 'ZeroOne')
images = load_images(dataset_dir, "*.png")
image_grid(images, titles=images.index)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "daf4a5c24b94d86a068163a71b966a5e", "grade": false, "grade_id": "cell-78ed854e0e4200ba", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Choix du jeu de données

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f729f32800d4456283fd558a3f31823a", "grade": false, "grade_id": "cell-78ed854e0e4200bb", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Choisissez l'un des jeux de données ci-dessus pour
votre projet. Chargez les images correspondantes dans `images` et
affichez les:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 333cf13ac01b2026e3defab409c8a14e
  grade: false
  grade_id: cell-e732417891788d51
  locked: false
  schema_version: 3
  solution: true
  task: false
---
dataset_dir = os.path.join(data.dir, 'ZeroOne')
images = load_images(dataset_dir, "*.png")
image_grid(images, titles=images.index)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 393908f8f06c63d2a3ae481447e7f0da
  grade: true
  grade_id: cell-2389de956025bb38
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert isinstance(images, pd.Series)
assert len(images) == 20
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0f753034fd6593bdc86dac221ffc2007", "grade": false, "grade_id": "cell-af6191373559b6be", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Bravo, vous avez terminé la dernière feuille du TP.

Mettez à jour votre rapport et déposez votre travail.
