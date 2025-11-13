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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f4fb5e4d189ee37bad5f15c104bac2c3", "grade": false, "grade_id": "cell-883bbb5e1919ca1e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

# Analyse de données

Dans cette feuille, nous allons mener une première analyse sur des
données, afin d'obtenir une référence. Nous utiliserons d'abord les
données brutes (représentation en pixel), puis nous extrairons
automatiquement des attributs par Analyse en Composantes Principales.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5505231ef795dc8e2187a9d01fe6baa9", "grade": false, "grade_id": "cell-e15fdd0116a9b9e2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Import des librairies

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "37fab34064691bf8b1ca6806420171df", "grade": false, "grade_id": "cell-406ad2a159064cfa", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On commence par importer les librairies dont nous aurons besoin. Comme
d'habitude, nous utiliserons un fichier `utilities.py` où nous vous
fournissons quelques fonctions et que vous complèterez au fur et à
mesure du projet:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 8b6606817a987853e15d8e7508ef2992
  grade: false
  grade_id: cell-76e64ee7bcb96bb5
  locked: true
  schema_version: 3
  solution: false
  task: false
---
# Automatically reload code when changes are made
%load_ext autoreload
%autoreload 2
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
%matplotlib inline
from scipy import signal
import seaborn as sns

from intro_science_donnees import *
from utilities import *
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "204b7ee1b8c3572854ba896251950281", "grade": false, "grade_id": "cell-6ec03d05a4e1c693", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Chargement des images

En commentant la ligne 1 ou la ligne 2, vous choisirez ici sur quel
jeu de données vous travaillerez: les pommes et les bananes ou le
vôtre.

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
---
import pandas as pd
import sklearn
import numpy as np
import matplotlib.image as mpimg

dataset_dir = 'data'
images_a = load_images(dataset_dir, f"a*.{'jpeg'}")
images_b = load_images(dataset_dir, f"b*.{'jpeg'}")
images = pd.concat([images_a, images_b])
image_grid(images, titles=images.index)

def resize_image(img):
    return img.resize((100, 100))

images_resized = images.apply(resize_image)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "485636a5878bed6bf15e7e30c606e5ea", "grade": false, "grade_id": "cell-efcac6252de311fd", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous allons aborder des jeux de données **plus grands** que
les précédents, en nombre et en résolution des images; il faut donc
être **un peu prudent** et parfois **patient**. Par exemple, le jeu de
données des pommes et bananes contient plusieurs centaines
d'images. Cela prendrait du temps pour les afficher et les traiter
toutes dans cette feuille Jupyter. Aussi, ci-dessus, utilisons nous le
glob `?[012]?.png` pour ne charger que les images dont le nom fait
moins de trois caractères et dont le deuxième caractère est 0, 1, ou 2.

De même, dans les exemples suivants, nous n'afficherons que les
premières et dernières images :

```{code-cell} ipython3
head = images.head()
image_grid(head, titles=head.index)
```

```{code-cell} ipython3
tail = images.tail()
image_grid(tail, titles=tail.index)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0bfbf808941821dfe7d71ff7cc0c9a78", "grade": false, "grade_id": "cell-e723e3fb5001bd97", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Redimensionner et recadrer

Comme vu au TP6, il est généralement nécessaire de redimensionner et/ou de recadrer les
images. Lors du premier projet, nous avons utilisé des images
recadrées pour se simplifier la tâche. Si l'objet d'intérêt est petit
au milieu de l'image, il est préférable d'éliminer une partie de
l'arrière-plan pour faciliter la suite de l'analyse. De même, si
l'image a une résolution élevée, on peut la réduire pour accélérer les
calculs sans pour autant détériorer les performances. Dans l'ensemble,
les images ne doivent pas dépasser 100x100 pixels.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "664e54b2ebe12127b7f003c7b9f13d25", "grade": false, "grade_id": "cell-1f5b70462bf6e53f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Dans les cellules suivantes, on recadre et redimensionne les images en
32x32 pixels. Aucun effort particulier n'est fait pour centrer l'image
sur le fruit. Vous pourrez faire mieux ensuite, dans la fiche sur le
[prétraitement](3_extraction_d_attributs.md).

Dans utilities, finissez la fonction crop_image en appliquant crop à l'image.

```{code-cell} ipython3
lst_effected = images_resized.iloc[:10].apply(lambda img: crop_image(img, (30, 20, 70, 60)))
lst_healthy = images_resized.iloc[10:].apply(lambda img: crop_image(img, (30, 20, 70, 60)))

images_cropped = pd.concat([lst_effected, lst_healthy])

image_grid(images_cropped)
```

```{code-cell} ipython3
image_grid(images_cropped.head())
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "658d05d7ba30f63d0eea685c3446d37f", "grade": false, "grade_id": "cell-1848d8ac9dce2aa3", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 3: Représentation en pixels

Dans les cours précédents, nous avons extrait des attributs avec des
fonctions ad-hoc, comme la rougeur (*redness*) ou l'élongation. Les
attributs ad-hoc sont pratiques pour faciliter la visualisation des
données. On peut cependant obtenir d'assez bons résultats en partant
directement des données brutes -- ici les valeurs des pixels de nos
images recadrées -- et en extrayant automatiquement des attributs par
[décomposition en valeurs
singulières](https://fr.wikipedia.org/wiki/D%C3%A9composition_en_valeurs_singuli%C3%A8res),
à la base de la technique de
[PCA](https://fr.wikipedia.org/wiki/Analyse_en_composantes_principales). Cette
analyse, présentée ci-dessous est simple à mettre en œuvre et peut
donner une première base de résultats.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "47f120d96a7a472d391909c207397262", "grade": false, "grade_id": "cell-6c8ca7bdc9253abf", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Vous trouverez dans `utilities.py` une fonction appelée
`image_to_series` qui transforme une image en une série
unidimensionnelle contenant les valeurs de tous les pixels de
l'image.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: a612f0aa6892caed701c54e5dd4daeda
  grade: false
  grade_id: cell-f376c04452c0a2c4
  locked: true
  schema_version: 3
  solution: false
  task: false
---
show_source(image_to_series)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0e83ead61f956532a186be26eb65c700", "grade": false, "grade_id": "cell-6e9b1ee1992cc570", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Appliquez cette fonction à toutes les images, et affectez le résultat
à `df` qui est donc un tableau de données où chaque ligne correspond à
une image:

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 9bf5386ca097b2a2f0fc4e044a230b16
  grade: false
  grade_id: cell-e726f7c95a38b80b
  locked: false
  schema_version: 3
  solution: true
  task: false
---
series_list = []
for image_name, image in images_cropped.items():
    series = image_to_series(image)
    series_list.append(series)
df = pd.concat(series_list, axis=1).T

nouveaux_index = []
for i in range(1, 11):
    nouveaux_index.append(f'a{i:02d}')
for i in range(1, 11):
    nouveaux_index.append(f'b{i:02d}')
df.index = nouveaux_index
df
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1fa86d21f4c37f83ebdec7f8d1e77385", "grade": true, "grade_id": "cell-edf8fc36ed15faf7", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

:::{admonition} Exercice

Pouvez-vous expliquer le nombre de colonnes que nous obtenons?

Le nombre de colonnes dans le DataFrame correspond au nombre total de pixels dans chaque image. Chaque colonne représente la valeur d'un pixel dans l'image. Dans cet exemple spécifique, il y a 4800 colonnes, ce qui suggère que chaque image contient 4800 pixels. Chaque ligne du DataFrame représente une image individuelle, et les valeurs dans les colonnes décrivent l'intensité de couleur de chaque pixel dans cette image particulière.

:::

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d73722ce156f1c0772d4243329275cb4", "grade": false, "grade_id": "cell-bac63aa1dc5a364a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous rajoutons à notre tableau de données une colonne contenant
l'étiquette (*ground truth*) de chaque image; dans le jeu de données
fourni, ce sera 1 pour une pomme et -1 pour une banane:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 45dcbbd75dc72916ab9d2c5a71cb4e37
  grade: false
  grade_id: cell-ef9776de8892681b
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df['étiquette'] = df.index.map(lambda name: 1 if name[0] == 'a' else -1)
df
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fa065ab1fe95a6676465ae02e1785238", "grade": false, "grade_id": "cell-b521e08d53e6f7e5", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Affichez les statistiques descriptives de Pandas sur votre base de
données. Peut-on interpréter ces statistiques?

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: d9aecf0f1e72279e18e23c52f68f08c4
  grade: false
  grade_id: cell-265099e5a3fefb08
  locked: false
  schema_version: 3
  solution: true
  task: false
---
df.describe()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0b04fc60580d53165e039ab88751a746", "grade": false, "grade_id": "cell-a69bb602ef2221a4", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Sauvegarde intermédiaire

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fcfa65f265bc5005f0f6dfbd091e52c8", "grade": false, "grade_id": "cell-8cb1846130b9cfe2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous allons sauvegarder ces données brutes dans un fichier:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 75453876738eaeed631d6014965c9b42
  grade: false
  grade_id: cell-2359fca3d8d7ac9b
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df.to_csv('crop_data.csv')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d5ae3b6058d953cc4ef782c24b395b1b", "grade": false, "grade_id": "cell-c8e307c24e9822df", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Cela vous permettra par la suite de reprendre la feuille à partir
d'ici, sans avoir à reexécuter tous les traitements depuis le début. 

Vous serez amenée à faire d'autres sauvergades intermédiaires dans
votre projet.

:::{admonition} Exercice

Chargez la table `crop_data.csv` dans `df` avec la fonction `read_csv`
de pandas et en ajoutant l'option `index_col=0` pour correctement
afficher le nom des colonnes:

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 3dae637fece9096a9f6d2faa5bac651f
  grade: false
  grade_id: cell-59f5ff38837b92ad
  locked: false
  schema_version: 3
  solution: true
  task: false
---
df = pd.read_csv("crop_data.csv", index_col=0)
df
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f250aaad53cded5510907c2fdb7dea2f", "grade": false, "grade_id": "cell-4576e2c2723b724d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## [VI]sualisation des données brutes par carte thermique

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1b59c8053df96e34b00ee320edd5e87b", "grade": false, "grade_id": "cell-2a67648ea9c07906", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Les données de la représentation en pixels sont volumineuses; par
principe il faut tout de même essayer de les visualiser. On peut pour
cela utiliser une carte thermique avec `Seaborn`.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: f3c870bca4130ab9236929eb09f24dab
  grade: false
  grade_id: cell-057378ec5d717db0
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
plt.figure(figsize=(20,20))
sns.heatmap(df, cmap="YlGnBu");
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0678d196c74da7082fc94a1c44cba369", "grade": false, "grade_id": "cell-261308b1d940c89a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Comme vous le constatez, les données ne sont pas aléatoires: il y a
des corrélations entre les lignes. Cela reste cependant difficilement
exploitable visuellement.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e9bd0477a8e615162f0d26e969effa89", "grade": false, "grade_id": "cell-c103279002f68467", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 4: Performance de [RÉ]férence

À présent, vous allez appliquer la méthode des plus proches voisins
**sur la représentation en pixels pour avoir une performance de
référence.**

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b05aa5cae21bde67de907dc9050a38b0", "grade": false, "grade_id": "cell-c67679043304e3f1", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Déclarez le modèle `sklearn_model` comme un classifieur par plus
proche voisin (KNN) avec 3 voisins, depuis la librairie
`scikit-learn`.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 38faac5ad1c9b5c18d79867828f4bf82
  grade: true
  grade_id: cell-4794ca5ee133a97b
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
---
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import balanced_accuracy_score as sklearn_metric

sklearn_model = KNeighborsClassifier(n_neighbors=3)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ef09c7b736bf0b0a0d4a3949ec62e207", "grade": false, "grade_id": "cell-f5d1905f8f1e86bf", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Comme dans les séances précédentes, on calcule la performance et les
barres d'erreurs du classifieur par validation croisée (*cross
validate*), en divisant de multiples fois nos données en ensemble
d'entraînement et en ensemble de test.

:::{admonition} Exercice

Finissez de remplir la fonction `df_cross_validate` d'`utilities.py`
afin qu'elle automatise tout le processus. Il y a deux endroits (et 3
lignes) où il y a du code manquant. Consultez son code pour retrouver
les étapes:

:::

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 18a09476bc1299fb57649633a2d04405
  grade: false
  grade_id: cell-1b3c24803336e33f
  locked: true
  schema_version: 3
  solution: false
  task: false
---
show_source(df_cross_validate)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 156a4a7721cdf2f999902e582da677dc
  grade: false
  grade_id: cell-10d1cd02c980dc5b
  locked: true
  schema_version: 3
  solution: false
  task: false
---
p_tr, s_tr, p_te, s_te = df_cross_validate(df, sklearn_model, sklearn_metric, verbose=True)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "62ce352416dedeff46a2c6c49a6fb028", "grade": false, "grade_id": "cell-7a16870bc8b1d91d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On a obtenu cette performance en comparant nos images pixel à pixel
(distance euclidienne), sans aucun attribut.

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e1435be6b97869d1c7c4669d74a28eb3", "grade": true, "grade_id": "cell-2b68d19d35bceb2f", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

:::{admonition} Exercice

Est-ce que ce score vous semble particulièrement bon, mauvais et/ou étonnant?

:::

Le score de précision équilibrée (balanced accuracy score) obtenu pour l'ensemble d'entraînement est de 0.76 en moyenne avec un écart-type de 0.08, tandis que pour l'ensemble de test, il est de 0.65 en moyenne avec un écart-type de 0.10.

Ce résultat semble bon pour un apprentissage sans attribut avec le classificateur des 3-plus proches voisins.

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "98d16b6749f680ce12d3e8bc472b508d", "grade": true, "grade_id": "cell-c5a8e3d90bb35375", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

## Conclusion

Cette première feuille vous fait passer par le formatage de base des
données. Prenez ici quelques notes sur ce que vous avez appris,
observé, interprété.

Nous avons appris avec ardeur à recadrer nos images. De plus, nous avons également eu l'occasion de voir comment convertir une image en Series Pandas. Finalement, nous avons effectué une heatmap de corrélation sur l'ensemble des pixels de nos images.

Les feuilles suivantes aborderont d'autres aspects de l'analyse
(attributs, classifieur) en se basant sur des attributs que vous
calculerez. Vous pourrez comparer les méthodes et appliquer celle qui
vous semble la plus pertinente à votre jeu de données. Ouvrez la
feuille sur l'[extraction d'attributs](3_extraction_d_attributs.md).
