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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "21b6ea6ffa68c3859943b2ddc94f1c4a", "grade": false, "grade_id": "cell-3876f910a24fe8a7", "locked": true, "schema_version": 3, "solution": false}}

# VI-ME-RÉ-BAR sur des données «réelles»

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7c56405b92cf87eabb2d6dcecc9a9b74", "grade": false, "grade_id": "cell-8647bce9e2a5d173", "locked": true, "schema_version": 3, "solution": false}}

Aujourd'hui nous allons analyser un jeu de données qui comporte des
images de pommes et de bananes avec comme objectif de *classer
automatiquement* les images de pommes versus celles de bananes.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "114b2eb7aac993047184dea6844c2335", "grade": false, "grade_id": "cell-8647bce9e2a5d174", "locked": true, "schema_version": 3, "solution": false}}

## Import des bibliothèques

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: dfcd9c2929e441096890b2d59860930a
  grade: false
  grade_id: cell-106177762ff8d9b4
  locked: true
  schema_version: 3
  solution: false
  task: false
---
import os, re
from glob import glob as ls
import numpy as np                    # Matrix algebra library
import pandas as pd                   # Data table (DataFrame) library
import seaborn as sns; sns.set()      # Graphs and visualization library
from PIL import Image                 # Image processing library
import matplotlib.pyplot as plt       # Library to make graphs 
# Configuration intégration dans Jupyter
%matplotlib inline
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2d440aa55f6dd25dc09569722688d3ec", "grade": false, "grade_id": "cell-af66fb6952f8b345", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Import des utilitaires:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 40fe5b4b283beb6e7a074304050de52f
  grade: false
  grade_id: cell-106177762ff8d9b5
  locked: true
  schema_version: 3
  solution: false
  task: false
---
%load_ext autoreload
%autoreload 2

from utilities import *
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9b9d9f0a01aa1a8842eab61922ec3814", "grade": false, "grade_id": "cell-11d255d13abd4972", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 0: chargement du jeu de données

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d2796f6bae05d43d64331f365098ccbd", "grade": false, "grade_id": "cell-11d255d13abd4973", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice:** En vous inspirant de la [feuille de bonnes
pratiques](1_bonnes_pratiques.md), chargez les images du jeu de
données 'ApplesAndBananasSimple', dans la variable `images`, et
affichez les:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 1f810e82161c5efc64c2614548e9d750
  grade: false
  grade_id: cell-a7eef074d0ac872f
  locked: false
  schema_version: 3
  solution: true
  task: false
---
from intro_science_donnees import *
import os.path
dataset_dir = os.path.join(data.dir, 'ApplesAndBananasSimple')
images = load_images(dataset_dir, '*.png')
image_grid(images)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9ade8c23e6b081232764434426a2b305", "grade": false, "grade_id": "cell-d7d7ff6550223d3e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 1: prétraitement et [VI]sualisation

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f3050f9e60c36e84d759e77ccff7215b", "grade": false, "grade_id": "cell-eb2909432b6312ab", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Observez les images en détails. Êtes vous capable de différencier les
pommes des bananes ? Essayez d'imaginer comment votre cerveau réussi
un tel exercice !

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0b000ff83f56163e885d62acd7b169b8", "grade": false, "grade_id": "cell-1ad9ea64fc9cfd94", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Prétraitement

Les données sont très souvent prétraitées c'est-à-dire **résumées
selon différentes caractéristiques** : chaque élément du jeu de
données est décrit par un ensemble
d'[**attributs**](https://en.wikipedia.org/wiki/Feature_(machine_learning))
-- propriétés ou caractéristiques mesurables de cet élément ; pour un
animal, cela peut être sa taille, sa température corporelle, etc.

C'est également le cas dans notre jeu de données : une image est
décrite par la couleur de chacun de ses pixels. Cependant les pixels
sont trop nombreux pour nos besoins. Nous voulons à la place juste
quelques attributs résumant les propriétés du fruit dans l'image,
comme sa couleur ou sa forme moyenne: ce sont les données
prétraitées. Nous verrons la semaine prochaine comment **extraire ces
attributs** depuis les images.

Pour ce TP, une table contenant les données prétraitées vous est
fournie dans le fichier `attributs.csv` qu'il suffit donc de charger:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 5837adf0ba95dfd875107091e9210793
  grade: false
  grade_id: cell-a322f1aa4ab94e73
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df = pd.read_csv("attributs.csv", index_col=0)
df
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "648bc29eb1b1f89d9920df73ebd8e258", "grade": false, "grade_id": "cell-045dcd312be9ba57", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Cette table de données contient en colonne les attributs (*features*)
de nos images ainsi que leurs classes (*vérité terrain*, *ground
truth*): 1 si c'est une image de pomme et -1 si c'est une banane.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "affb0898bb769af9508e6ed5e0be3f02", "grade": false, "grade_id": "cell-aa604d5354811a16", "locked": true, "schema_version": 3, "solution": false, "task": false}}

<div class="alert alert-info">

Cette table est tout ce dont nous aurons besoin dans la suite. 
    
</div>

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6d13fd2d81bfd064329527e046178f46", "grade": false, "grade_id": "cell-85e26887a30112ac", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Visualisation

**Exercice:** Tout d'abord, extrayez quelques statistiques simples et
observez votre table avec la méthode `describe`:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 09d219254b852169f62d2d312f1e73a9
  grade: false
  grade_id: cell-fb6f78878deb1b59
  locked: false
  schema_version: 3
  solution: true
  task: false
---
df.describe()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "40a29f036184e3b4ce216ab1811995ea", "grade": false, "grade_id": "cell-d7facf4fac2c600c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous pouvons visualiser cette table sous forme de carte de chaleur
(*heat map*) aisément:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 4ad44ce0f09d340834bf66f2ce7898c8
  grade: false
  grade_id: cell-59b086b9a7351acb
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df.style.background_gradient(cmap='coolwarm')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9b66bfee7fd205a075d260e51f672678", "grade": false, "grade_id": "cell-6cc172376a6a1121", "locked": true, "schema_version": 3, "solution": false, "task": false}}

La carte de chaleur est appliquée à chaque colonne
indépendamment. Ainsi, nous visualisons la variation de chaque colonne
même si les valeurs sont dans des unités différentes ou avec des
ordres de grandeur différents, comme c'est le cas ici.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "67bf44a7d163d86637bf93d06cbc23bd", "grade": false, "grade_id": "cell-193e638c102d8d62", "locked": true, "schema_version": 3, "solution": false, "task": false}}

La prochaine étape est de calculer la corrélation entre les colonnes;
comme vu en cours, ces corrélations ne sont pas représentatives quand
les colonnes n'ont pas le même ordre de grandeur. Nous devons donc
**standardiser** chaque colonne de sorte à avoir la moyenne à $0$ et
l'écart-type à $1$.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e8d714798632819175d53a34792e95ce", "grade": false, "grade_id": "cell-fefe4d124f205c7d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice:** Standardisez la table : colonne par colonne, soustrayez
la moyenne puis divisez par l'écart-type; affectez le résultat à
`dfstd`. Comme la semaine dernière, pas besoin de boucle. Utilisez la
vectorisation!

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: ccf67125b462642861aab81ca88a20c8
  grade: false
  grade_id: cell-0c29581ba1da5a27
  locked: false
  schema_version: 3
  solution: true
  task: false
---
dfstd = df
dfstd['redness'] = (df['redness']-df['redness'].mean())/df['redness'].std()
dfstd['elongation'] = (df['elongation']-df['elongation'].mean())/df['elongation'].std()
df.describe()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5458d5e9862efff8285730df6d612d09", "grade": false, "grade_id": "cell-26178c2d52dee7fb", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Vérifiez que cette nouvelle table est effectivement standarisée à
l'aide des commandes suivantes (vérifiez que la moyenne est à 0 et
l'écart type à 1):

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 99bbc49667deeb8969cfdacb1f660cd5
  grade: false
  grade_id: cell-5a37f3af26472421
  locked: true
  schema_version: 3
  solution: false
  task: false
---
dfstd.describe()
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: a505ff0701fdc746c6e05d24008af201
  grade: true
  grade_id: cell-1334dd39d25778b2
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert dfstd.shape == df.shape
assert dfstd.index.equals(df.index)
assert dfstd.columns.equals(df.columns)
assert (abs(dfstd.mean()) < 0.01).all()
assert (abs(dfstd.std() - 1) < 0.1).all()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "c17528382c01e3ddd092a57276793615", "grade": false, "grade_id": "cell-d53234dfccf90ba6", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Mince, ce n'est pas exactement ce qu'on veut ! La valeur du fruit
correspond à une **étiquette** et pas à une **valeur**; on veut donc
garder les valeurs originelles -1 pour les bananes et 1 pour les
pommes.

Pour cela, le plus simple est de réaffecter la colonne d'origine:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 3e02aec7ec19e111d7d17a90a7375de5
  grade: false
  grade_id: cell-05f8cc17ab9a5c02
  locked: true
  schema_version: 3
  solution: false
  task: false
---
dfstd['class'] = df['class']
dfstd
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b316c422c9dcf7c87f66cddbb563c0a0", "grade": false, "grade_id": "cell-42a3abe8791a4315", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Observations

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4252e89827198d19bda0f6e972daacef", "grade": false, "grade_id": "cell-63ce671dbea4f35c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Regardez la carte de chaleur de la table standarisée;
elle devrait être identique à la précédente:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 6bd10c8406b70b27b69e1b9ddd7e50af
  grade: false
  grade_id: cell-ce7b2effecfa8a5d
  locked: false
  schema_version: 3
  solution: true
  task: false
---
dfstd.style.background_gradient(cmap='coolwarm')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e62a2dc1fe486e125bbb1781ea018a90", "grade": false, "grade_id": "cell-e5f384409c2d18ab", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :**

1.  Produisez une carte de chaleur de la matrice de corrélation.

    **Indication:** si nécessaire, consultez le TP de la semaine
    précédente.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 2ef96fc103a66cc7c64ed4d219ce1561
  grade: false
  grade_id: cell-5d6f2f8188882c92
  locked: false
  schema_version: 3
  solution: true
  task: false
---
dfstd_cor = dfstd.corr(numeric_only=True)
dfstd_cor.style.background_gradient(cmap='coolwarm', axis=None)
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ad45a239352e6c1062d68075511d09b8", "grade": true, "grade_id": "cell-42ea408841ec0159", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

2.  Quel(s) attribut(s) est (sont) correlé(s) au type de fruit ?
    Pouvez vous indiquer quel type de fruit est le «plus» rouge et lequel est
    le «plus» allongé ? Y a-t-il des exceptions ?
    
    L'élongation est fortement corrélée négativement à la classe du fruit et la rougeur est faiblement corrélée positivement à la classe du fruit.
    La pomme est le fruit le plus rouge et la banane est le fruit le plus élongué.
    Il y a des exceptions comme des bananes qui sont de couleur rouge.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fc51e55c746fb28a707d8375436a7409", "grade": false, "grade_id": "cell-30a2ce5f1e7c564b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Il existe quelques valeurs aberrantes (*outliers*), comme, par exemple
deux bananes rouges; on peut les identifier à l'aide d'une
visualisation en nuage de points (*scatter plot*), où chaque image est
positionnée en fonction des valeurs de ses attributs:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 78cb5f6efd2669cb165f9a521212ccb9
  grade: false
  grade_id: cell-3a943ea0d8fd622f
  locked: true
  schema_version: 3
  solution: false
  task: false
---
make_scatter_plot(dfstd, images, axis='square')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e8f318c74872af64a289e68c81a079b6", "grade": false, "grade_id": "cell-4be4c177b85c9ea7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On peut aussi visualiser le jeu de données à l'aide d'un pair plot. 

**Exercice :** En vous inspirant du TP de la semaine dernière,
utilisez `Seaborn` pour produire un pair plot. Utilisez l'option
`diag_kind` pour choisir une représentation en histogrammes sur la
diagonale et l'option `palette` pour prendre `Set2` comme palette de
couleurs:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: c1201c5115ada0394f7ccf9683d9bc54
  grade: false
  grade_id: cell-bd856139dbfc04d8
  locked: false
  schema_version: 3
  solution: true
  task: false
---
import seaborn as sns
sns.pairplot(dfstd, palette='Set2', diag_kind="hist")
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "599b276bc865de4c46320f4422e0811d", "grade": false, "grade_id": "cell-ea1ae3bf85efb5ac", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Remarque importante :** un seul attribut (la rougeur ou
l'élongation) est presque suffisant pour parfaitement séparer les
pommes des bananes.

+++ {"deletable": false, "editable": false, "heading_collapsed": true, "nbgrader": {"cell_type": "markdown", "checksum": "a8298dd2abec2be4d1e21ba163c12825", "grade": false, "grade_id": "cell-61f22f6356336879", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 2: [ME]sure de performance (*[ME]tric*)

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "74d0ba519a7091000ebd56cb2b7a31c1", "grade": false, "grade_id": "cell-61f22f635633687a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Mesurer les performances de ce problème de classification revient à
déterminer notre capacité à séparer les pommes des bananes (un
problème de classification).

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "c2ed65c73ab43f9def35137d29b2108e", "grade": false, "grade_id": "cell-566038093ef58836", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Partition (*split*) du jeu de données en ensemble d'entraînement (*training set*) et ensemble de test (*test set*)

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "431aed291130212ad986f14f34524c82", "grade": false, "grade_id": "cell-858740fbee6099c6", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Séparons d'abord les colonnes de notre table selon:

- `X`: les attributs permettant d'effectuer des prédictions
- `Y`: la *vérité terrain*: ce que l'on veut prédire; ici le type de
  fruit. Pour cela on définit:

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 041394e1c291f2d0b61fac21f4588421
  grade: false
  grade_id: cell-a032a5bd3cee8e8f
  locked: true
  schema_version: 3
  solution: false
  task: false
---
X = dfstd[['redness', 'elongation']]
Y = dfstd['class']
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "1caaa90f1eb8b930d257a0700e623b81", "grade": false, "grade_id": "cell-4ca41aad6aeac76f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

<div class="alert alert-info">

Pourquoi cette notation $X$ et $Y$ ? Car on essaye de définir un
*modèle prédictif* $f$; pour chaque élément d'index $i$, on veut
prédire la vérité terrain $Y_i$ à partir de la valeur $X_i$ des
attributs. Idéalement on aurait $Y_i = f(X_i)$, pour tout $i$.

</div>

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "70103dbd69c9d7003a716d7ecfc4e1ab", "grade": false, "grade_id": "cell-240a7fb7e963b11d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous allons maintenant partitionner nos images en un **ensemble
d'entraînement** et un **ensemble de test**.

- L'ensemble d'entraînement servira à **entraîner notre modèle
  prédictif $f$**, c'est-à-dire à ajuster ses paramètres pour qu'il
  colle au mieux aux données de cet ensemble.
  
- L'ensemble de test servira à mesurer la performance de ce modèle
  prédictif.
  
Comme notre problème est de petite taille, on va partitionner les
images en deux ensembles de même taille.

L'utilitaire `split_data` fourni dans `utilities.py` partitionne
aléatoirement l'index des lignes de `X` et `Y` en deux ensembles de
même taille:

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 8592a9ea5f16829cae5ad095c2b605d6
  grade: false
  grade_id: cell-6cf3f376975cea19
  locked: true
  schema_version: 3
  solution: false
  task: false
---
train_index, test_index = split_data(X, Y, seed=0)
train_index, test_index
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "4593e1d5ff4324f890d78230a2d3e3f1", "grade": false, "grade_id": "cell-0a0f464a80d9b33d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Séparons en conséquence la table des attributs `X`:

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 273c9ca41d88148315275c5c8ffc97e5
  grade: false
  grade_id: cell-6cf3f376975cea20
  locked: true
  schema_version: 3
  solution: false
  task: false
---
Xtrain = X.iloc[train_index]
Xtest = X.iloc[test_index]
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "878ee8b12dcecf4bed4f0182116c3337", "grade": false, "grade_id": "cell-844a1e6707830d05", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Faites de même pour les étiquettes.

```{code-cell} ipython3
---
deletable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 8636aeacb04af162578922b955c75298
  grade: false
  grade_id: cell-07ca6f0475d513c9
  locked: false
  schema_version: 3
  solution: true
  task: false
---
Ytrain = Y.iloc[train_index]
Ytest = Y.iloc[test_index]
```

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: b5c71dfaac331b73bcd04e9799359b70
  grade: true
  grade_id: cell-55cbfd3b374091b5
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert Ytest.shape == Ytrain.shape
assert pd.concat([Ytest, Ytrain]).sort_index().equals(Y.sort_index())
assert Ytest.value_counts().sort_index().equals(Ytrain.value_counts().sort_index())
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "4a268c37a5b12a5fe456e4f1a345c13b", "grade": false, "grade_id": "cell-87cb8544862cfb9d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On peut maintenant regarder les images qui serviront à entraîner notre
modèle prédictif.

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 813af3670f6c287c8353bb608de7987c
  grade: false
  grade_id: cell-e237d501cc19902f
  locked: true
  schema_version: 3
  solution: false
  task: false
---
image_grid(images.iloc[train_index], titles=train_index)
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "3e4a98881a3f2bb66957515e3c35a237", "grade": false, "grade_id": "cell-631da63da34faca9", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Faites de même avec les images de test.

```{code-cell} ipython3
---
deletable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: ed7e7cc7606a8c014870394b4073d127
  grade: false
  grade_id: cell-61df66254e2ef13e
  locked: false
  schema_version: 3
  solution: true
  task: false
---
image_grid(images.iloc[test_index], titles=test_index)
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "919e19a53e31740d9cb76489d96e51fd", "grade": false, "grade_id": "cell-63bc0f2a545e795e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

<div class="alert alert-info">

Notez que l'ensemble d'entraînement et l'ensemble de test contiennent
la même proportion de pommes et de bananes que le jeu de données
initial. L'utilitaire `split_data`a été conçu pour le garantir!

</div>

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "ec4942073d9a92669adca0a589ede9d9", "grade": false, "grade_id": "cell-284c022c7df9157d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

L'utilitaire `make_scatter_plot` fourni permet aussi de visualiser les
ensembles d'entrainement et de test comme des nuages de points, en
représentant chaque donnée d'entraînement par l'image associée et
chaque donnée de test un point d'interrogation car sa classe
(pomme/banane) est cachée.

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: a231e653ff17c8bd149e09a088f4b34f
  grade: false
  grade_id: cell-42fd5d0a9afe5e4d
  locked: true
  schema_version: 3
  solution: false
  task: false
---
make_scatter_plot(dfstd, images, train_index, test_index, axis='square')
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "e23642d2f42552ac6a39b4eb7ef870be", "grade": false, "grade_id": "cell-afad01634691448a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Calcul du taux d'erreur

On suppose que l'on a :

- Un vecteur `solutions` contenant les valeurs cibles (les "vraies"
  classes : 1 pour les pommes et -1 pour les bananes).
- Un vecteur `prédictions` contenant des valeur prédites (les classes
  estimées).

Le *taux d'erreur* (*error rate*) est défini comme la fraction $\frac
e n$, où $e$ est le nombre de prédictions incorrectes et $n$ le nombre
total de prédictions. C'est une mesure de performance les prédictions.

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "59f3fb183706bcd22ae7859597da330f", "grade": false, "grade_id": "cell-092a1faf3f2aba58", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :**
1.  Déterminer à la main $e$, $n$ et le taux d'erreur pour l'exemple
    suivant :

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 7671a98776913c1c5ac0bcff3b449f73
  grade: false
  grade_id: cell-d6e62d9e27ea3fb9
  locked: true
  schema_version: 3
  solution: false
  task: false
---
solutions = pd.Series([1, 1, -1, 1, 1])
predictions = pd.Series([1, -1, 1, 1, 1])
```

+++ {"deletable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "93ca60a77efae035db516cbed7395e19", "grade": true, "grade_id": "cell-6adb2830391869f3", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

$e = 2$ car deux valeurs pour le même indice des Series sont différentes.
$n = 5$ car la longueur des Series est de 5.
Nous avons donc $\frac{e}{n} = \frac{2}{5} = 0.4$.

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "c92037ab1e7fe66b07f68f908892b0b9", "grade": false, "grade_id": "cell-19a51f97d9c9e63d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

2.  Calculez le même taux d'erreur avec Python  
    **Défi :** cela peut se faire en une petite ligne 😉

```{code-cell} ipython3
---
deletable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 9226b8733b711bbacda1426bb52ac3b0
  grade: false
  grade_id: cell-cc44cd5916755f56
  locked: false
  schema_version: 3
  solution: true
  task: false
---
taux_erreur = (solutions!=predictions).sum()/len(solutions)
taux_erreur
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "6ee9e69c10c654dd171fb3967a24057c", "grade": false, "grade_id": "cell-afad01634691448b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

3.  Ouvrez le fichier <a href="utilities.py">utilities.py</a>, et
    complétez le code de la fonction `error_rate` en
    généralisant votre calcul précédent.

4.  Vérifiez votre fonction sur l'exemple ci-dessus

```{code-cell} ipython3
---
deletable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 6d72ed80432b7cc91632cdcc112a2d67
  grade: false
  grade_id: cell-a4706e9d08b0a817
  locked: false
  schema_version: 3
  solution: true
  task: false
---
error_rate(solutions, predictions)
```

+++ {"deletable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "0f0a0810b6b2ea1846f875738182230c", "grade": true, "grade_id": "cell-7ffc7bbe9657debe", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

5.  Écrivez des tests (avec `assert`) qui vérifient que :

    - le taux d'erreur entre `solution=Ytrain` et `prediction=Ytrain`
      est nul (pourquoi ?)

      Les données d'entraînement et de test étant les mêmes, il n'y a aucune différence entre les deux jeux de données donc $e$ le nombre de prédictions incorrectes est erroné est nul d'où le taux d'erreur $\frac{e}{n} = 0$.

    - le taux d'erreur entre `solution=Ytrain` et
      `prediction=[1,...,1]` est de 0,5 (pourquoi ?)

      D'après l'énoncé, on a : "Notez que l'ensemble d'entraînement et l'ensemble de test contiennent la même proportion de pommes et de bananes que le jeu de données initial. L'utilitaire `split_data` a été conçu pour le garantir !". Cela signifie que la moitié des données de Ytrain sont des 1 d'où le taux d'erreur $\frac{e}{n} = 0.5$. 

    - le taux d'erreur entre `solution=Ytrain` et
      `prediction=[0,...,0]` est de un (pourquoi ?)

      Il n'y a pas de classe valant 0 donc les prédictions sont toutes erronées on a donc $e = n$ avec $n$ la longueur du jeu de données des prédictions d'où le taux d'erreur $\frac{e}{n} = \frac{n}{n} = 1$.

    **Astuce** : vous pouvez utiliser `np.zeros(Ytrain.shape)` pour
    générer un tableau `[0,...,0]` de même taille que `Ytrain`, et de
    même `np.ones(Ytrain.shape)` pour `[1,. ..,1]`.

```{code-cell} ipython3
---
deletable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: ae6d1ed95fc42bc1c582f3c93d0f5237
  grade: false
  grade_id: cell-f10f63342860aa0d
  locked: false
  schema_version: 3
  solution: true
  task: false
---
assert error_rate(Ytrain, Ytrain) == 0
assert error_rate(Ytrain, np.ones(Ytrain.shape)) == 0.5
assert error_rate(Ytrain, np.zeros(Ytrain.shape)) == 1
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "e82a6914190ba7b539f54f27de473d2c", "grade": false, "grade_id": "cell-16fd7e648da0d5f0", "locked": true, "schema_version": 3, "solution": false, "task": false}}

La bibliothèque d'apprentissage statistique
[`scikit-learn`](https://en.wikipedia.org/wiki/Scikit-learn) également
appelée `sklearn` a une fonction `accuracy_score` qui calcule la
précision des prédictions. Ainsi, et comme vérification
supplémentaire, nous pouvons tester que
`error_rate + accuracy_score = 1` en utilisant les mêmes exemples que
ci-dessus.

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: cb9ef29503c5e772a2bc5eb8b42a2813
  grade: true
  grade_id: cell-f4c4c09dd8d3eed8
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
from sklearn.metrics import accuracy_score
assert abs(error_rate(Ytrain, Ytrain)                 + accuracy_score(Ytrain, Ytrain)                 - 1) <= .1
assert abs(error_rate(Ytrain, np.zeros(Ytrain.shape)) + accuracy_score(Ytrain, np.zeros(Ytrain.shape)) - 1) <= .1
assert abs(error_rate(Ytrain, np.ones(Ytrain.shape))  + accuracy_score(Ytrain, np.ones (Ytrain.shape)) - 1) <= .1
```

+++ {"deletable": false, "editable": false, "heading_collapsed": true, "nbgrader": {"cell_type": "markdown", "checksum": "26fd4e80ae94eeda4cd21212b4cc5b97", "grade": false, "grade_id": "cell-429fc2516bb30344", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 3: [RÉ]férence (*base line*)

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "2dcc27a3b7f2a01f61f9aee09c883631", "grade": false, "grade_id": "cell-1db4578e47bf6caf", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Mon premier classificateur : plus proche voisin

Le classificateur du **plus proche voisin** est une méthode très
simple: pour classer une entrée non étiquetée, nous cherchons l'entrée
étiquettée la plus proche et prenons son étiquette. Vous pourrez
facilement le mettre en oeuvre plus tard dans le semestre en fin de
projet 1.

Pour le moment nous allons utiliser `scikit-learn` qui implante un
classificateur plus général appelé **$k$-plus proches voisins** (KNN:
*$k$-Nearest Neighbors*). Avec ce classificateur, une entrée non
étiquetée est classée en fonction des étiquettes de ses $k$ plus
proches voisins. L'entrée sera prédite comme appartenant à la classe C
si la majorité de ces $k$ plus proches voisins appartient à la classe
C. Le classificateur du plus proche voisin correspond au cas
particulier $k=1$.

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "80900f6f36f277a6cc1ce35a0eeaea67", "grade": false, "grade_id": "cell-2317616397cfc6da", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :**
1.  Importez le classificateur `KNeighborsClassifier` à partir de
    `sklearn.neighbors`. Utilisez-le pour construire un nouveau
    modèle, en fixant le nombre de voisins à un (voir le
    [CM3](CM3.md)). Appelez-le `classifier`.
2.  Entraînez ce modèle avec `Xtrain` en appelant la méthode "fit".
3.  Utilisez ensuite le modèle formé pour créer deux vecteurs de
    prédiction `Ytrain_predicted` et `Ytest_predicted` en appelant le
    méthode `predict`.
4.  Calculez `e_tr`, le taux d'erreur de l'entrainement et `e_te` le
    taux d'erreur des tests.

**Indication** : consultez le cours et la documentation aussi souvent
que nécessaire, en commençant par taper `KNeighborsClassifier?`

<!-- WARNING: `scikit-learn` uses lists for prediction labels instead
of column vectors. You will have to replace `Ytrain` by
`Ytrain.ravel()` and `Ytest` by `Ytest.ravel()` to avoid an error
message and wrong error rates.-->

```{code-cell} ipython3
---
deletable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 38137163b5fb7cdcf89ec0c2249500e7
  grade: false
  grade_id: cell-85205b5012588319
  locked: false
  schema_version: 3
  solution: true
  task: false
---
from sklearn.neighbors import KNeighborsClassifier

k = 1
classifier = KNeighborsClassifier(n_neighbors=k)
classifier.fit(Xtrain, Ytrain) 

Ytrain_predicted = classifier.predict(Xtrain)
Ytest_predicted = classifier.predict(Xtest)

e_tr = error_rate(Ytrain, Ytrain_predicted)
e_te = error_rate(Ytest, Ytest_predicted)

print("NEAREST NEIGHBOR CLASSIFIER")
print("Training error:", e_tr)
print("Test error:", e_te)
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "a5209a5c489d9ed41d8ddb4ec071fe00", "grade": false, "grade_id": "cell-026c9eceb600f5f6", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Ce problème est simple: nous n'avons aucune erreur dans l'ensemble
d'entraînement et deux erreurs dans l'ensemble de test.

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "98f7d1d02b6f2ecd7167f6db71de6fd6", "grade": false, "grade_id": "cell-b479722a4484a04a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Ensuite, nous superposons les prédictions faites sur l'ensemble de test sur un nuage de points ...

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: edda8fb0f82faab0c25ddcf76405840d
  grade: false
  grade_id: cell-fdaa23f990c0b172
  locked: true
  schema_version: 3
  solution: false
  task: false
---
# The training examples are shown as white circles and the test examples are black squares.
# The predictions made are shown as letters in the black squares.
make_scatter_plot(X, images,
                  train_index, test_index, 
                  predicted_labels=Ytest_predicted, axis='square')
```

+++ {"deletable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "5325485526be3a441e3457ff7e8708e7", "grade": true, "grade_id": "cell-675f918294af4213", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

**Exercice :** Observez la figure. Qui y a-t-il selon l'axe des x et
des y ? Rédigez la réponse.

L'axe des x correspond à la rougeur des fruits tandis que l'axe des y correspond à l'élongation des fruits.
Plus l'élongation (l'axe y) est elevée, plus les fruits ont des chances d'être des bananes.

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "42cd48dce8b890a681facefaaa7a9a75", "grade": false, "grade_id": "cell-a11a418d2b25ea3e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### ... ensuite, nous montrons la "vérité terrain" et calculons le taux d'erreur

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 9e87d6d9ad5134d8620695f3cf33664a
  grade: false
  grade_id: cell-2dd6ec8b3c3c3005
  locked: true
  schema_version: 3
  solution: false
  task: false
---
# The training examples are shown as white circles and the test examples are blue squares.
make_scatter_plot(X, images.apply(transparent_background_filter),
                  train_index, test_index, 
                  predicted_labels='GroundTruth', axis='square')
```

+++ {"deletable": false, "editable": false, "heading_collapsed": true, "nbgrader": {"cell_type": "markdown", "checksum": "7b27f34015d7406bbbfb168e36622501", "grade": false, "grade_id": "cell-d9cb6b44a99ec6d2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 4: [BAR]res d'erreur (*error bar*)

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "fee8e815c64232e3d60bc0eda098fef1", "grade": false, "grade_id": "cell-d9cb6b44a99ec6d3", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Une fois les résultats obtenus nous devons évaluer leur
significativité en calculant les barres d'erreurs. Évidemment, comme
nous n'avons que dix exemples de test, on ne peut observer plus que
dix erreurs; dans l'absolu ce n'est pas énorme mais pour notre exemple
ça le serait !

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "286521534e2fa86153e0871fe5f78d3d", "grade": false, "grade_id": "cell-d9cb6b44a99ec6d4", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Barre d'erreur 1-sigma

**Exercice :** Déterminez une première estimation de la barre d'erreur
en calculant l'erreur standard $\sigma$ sur l'ensemble
d'entrainement. Pour rappel, $\sigma = \sqrt{\frac{e_{te} *
(1-e_{te})}{n}}$ où $e_{te}$ est le taux d'erreur et $n$ est le nombre
de tests effectués.

De combien d'exemples aurions nous eu besoin pour diviser cette barre
d'erreur par un facteur de deux?

```{code-cell} ipython3
---
deletable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 642a4ae820d406a98f1b14809e9c23ce
  grade: false
  grade_id: cell-f68b51ca08347f6b
  locked: false
  schema_version: 3
  solution: true
  task: false
---
sigma = np.sqrt((e_te*(1-e_te))/len(Xtest))
print(f"TEST SET ERROR RATE: {e_te:.2f}")
print(f"TEST SET STANDARD ERROR: {sigma:.2f}")
```

Pour diviser cette barre d'erreur par un facteur de deux, il faut augmenter le nombre d'exemples par un facteur de 4 car nous avons une racine carrée dans notre équation.

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 97077d222b8f3bab1adad923d6fc4db4
  grade: true
  grade_id: cell-c96fd570127e77c3
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert abs( sigma - 0.13 ) < 0.1
```

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "486d15f0e1bf6748b2eb55b6753ef774", "grade": false, "grade_id": "cell-209765e9c10f8f32", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Barre d'erreur par validation croisée (*cross-validation*)

Calculons maintenant une autre estimation de la barre d'erreur en
répétant l'évaluation de performance pour de multiples partitions
entre ensemble d'entraînement et ensemble de test. Pour cela on peut
répéter 100 fois la partition du jeu de données en ensemble
d'entraînement et de test et calculer la moyenne et l'écart-type de
l'erreur standard de ces réplicats. En un sens, ce résultat est plus
informatif puisque il prend en compte la variabilité de l'ensemble
d'entraînement et de test.

**Remarque:** cette estimation reste cependant biaisée; mais cela est
hors programme.

```{code-cell} ipython3
---
deletable: false
editable: false
hidden: true
nbgrader:
  cell_type: code
  checksum: 960d32fb3b3846bc5a4f0c68f9111731
  grade: false
  grade_id: cell-92de02e0f28233e9
  locked: true
  schema_version: 3
  solution: false
  task: false
---
n_te = 10
SSS = StratifiedShuffleSplit(n_splits=n_te, test_size=0.5, random_state=5)
E = np.zeros([n_te, 1])
k = 0
for train_index, test_index in SSS.split(X, Y):
    print("TRAIN:", train_index, "TEST:", test_index)
    Xtrain, Xtest = X.iloc[train_index], X.iloc[test_index]
    Ytrain, Ytest = Y.iloc[train_index], Y.iloc[test_index]
    classifier.fit(Xtrain, Ytrain.ravel()) 
    Ytrain_predicted = classifier.predict(Xtrain)
    Ytest_predicted = classifier.predict(Xtest)
    e_te = error_rate(Ytest, Ytest_predicted)
    print("TEST ERROR RATE:", e_te)
    E[k] = e_te
    k = k + 1
    
e_te_ave = np.mean(E)
# It is bad practice to show too many decimal digits:
print(f"\n\nCV ERROR RATE: {e_te_ave:.2f}")
print(f"CV STANDARD DEVIATION: {np.std(E):.2f}")

sigma = np.sqrt(e_te_ave * (1-e_te_ave) / n_te)
print(f"TEST SET STANDARD ERROR (for comparison): {sigma:.2f}")
```

+++ {"deletable": false, "editable": false, "heading_collapsed": true, "nbgrader": {"cell_type": "markdown", "checksum": "225ae8fad0414e70b2114dabfc466332", "grade": false, "grade_id": "cell-f2330dcf5f3ebc8c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Conclusion

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "27907bbbdf3fa325f77dddcabf9497d1", "grade": false, "grade_id": "cell-f2330dcf5f3ebc8e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

<div class="alert alert-info">

C'est la fin de notre première classification d'images par apprentissage
statistique. Nous avons appliqué le schéma VI-ME-RÉ-BAR: nous avons
[VI]sualisé les données prétraitées, introduit une [ME]sure pour le
problème de classification, à savoir le taux d'erreur pour les
prédictions. Nous avons procédé avec une méthode de [RÉ]férence
(*baseline* en anglais) en utilisant le classificateur du plus proche
voisin vu en cours. Enfin, nous avons estimé les performances de ce
premier classificateur en calculant les [BAR]res d'erreurs sur de
nombreux échantillons d'ensembles d'apprentissage/de test.

Les prédictions obtenues sont assez robustes, ce qui n'est pas
surprenant étant donné que, à quelques valeurs aberrantes près, les
images sont bien contraintes (fond blanc, taille constante des images
et des fruits, ...).

La semaine prochaine nous verrons comment prétraiter un nouveau jeu de
données que vous aurez choisi; la semaine suivante nous testerons
d'autres classificateurs.

</div>

+++ {"deletable": false, "editable": false, "hidden": true, "nbgrader": {"cell_type": "markdown", "checksum": "ad5b7fd4102e91eb99151d26eb4d64d5", "grade": false, "grade_id": "cell-f2330dcf5f3ebc8d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Mettez à jour votre [rapport](index.md) et déposez votre travail.

Pour préparer la semaine prochaine, il vous reste à choisir un jeu de
données parmi ceux proposés. Pour cela ouvrez la feuille [jeux de
données](3_jeux_de_donnees.md).
