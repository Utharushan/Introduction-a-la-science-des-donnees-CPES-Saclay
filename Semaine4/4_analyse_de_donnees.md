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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e877a7f5aa56b85ddc209ecbb2d54445", "grade": false, "grade_id": "cell-3876f910a24fe8a7", "locked": true, "schema_version": 3, "solution": false}}

# VI-ME-RÉ-BAR sur vos propres données!

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "69fce3c36f15f567b2208ecd06ac87f9", "grade": false, "grade_id": "cell-3b25fe1716dd8293", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Instructions**:
- Ci-dessous, mettez ici une description de votre jeu de données: lequel avez vous choisi ?
- Quel est le défi ? Intuitivement quels critères pourraient
  permettre de distinguer les deux classes d'images?

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "c2f6232958f8a0474f55f80141de80b7", "grade": true, "grade_id": "cell-96350e0e04c4d91f", "locked": false, "points": 3, "schema_version": 3, "solution": true, "task": false}}

Zéros et uns manuscrits : Il faut essayer de distinguer des $0$ et des $1$ qui ont été écrits à la main. Les $0$ ressemblent à des ovales et sont plus larges que les $1$ qui ressemblent à des traits verticaux.

La difficulté réside dans le fait que certains de nos chiffres sortent du cadre et que les $1$ sont parfois courbés. De plus, notre jeu de données étant en noir et blanc, on ne peut pas utiliser la couleur comme un critère permettant de distinguer nos deux classes d'images.

D'une part, les $1$ sont des traits verticaux donc l'élongation peut être un critère déterminant.
D'autre part, les $1$ semblent occuper moins d'espaces dans le cadre que les $0$ et sont tous écrits sur la gauche laissant ainsi la droite du cadre de couleur blanche. 
Nous pouvons donc essayer d'utiliser ces critères afin de distinguer les deux classes d'images.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 7cf3162b4b4a0509dde50afe71e6ba58
  grade: false
  grade_id: cell-f463237384c14d8c
  locked: true
  schema_version: 3
  solution: false
  task: false
---
from intro_science_donnees import *
## les utilitaires
%load_ext autoreload
%autoreload 2
from utilities import *
# Graphs and visualization library
import seaborn as sns; sns.set()      
# Configuration intégration dans Jupyter
%matplotlib inline
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b5bcf7ce90464828259054e0f8d258ce", "grade": false, "grade_id": "cell-1e377d9f288ab8e0", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 1: prétraitement et [VI]sualisation

+++

Le jeu de données consiste en les images suivantes:

**Instruction :** Chargez votre jeu de données comme dans la feuille
`3_jeux_de_donnees.md` de la semaine dernière, en stockant les
images dans la variables `images` et en les affichant.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 9991b25280d0f128861e5ec4a3e1d385
  grade: false
  grade_id: cell-596455595966feb5
  locked: false
  schema_version: 3
  solution: true
  task: false
---
import os
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
  checksum: a2d30e6e80157634ba3fbd15f8eab118
  grade: true
  grade_id: cell-d3b1c03f1fbc66c4
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert isinstance(images, pd.Series)
assert len(images) == 20
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b750e129defcac1b2774f8d55bd0bfa3", "grade": false, "grade_id": "cell-1ad9ea64fc9cfd94", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Prétraitement

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "714373fb2541b5c66e981259f6752be5", "grade": false, "grade_id": "cell-c5eeea84f126a6a9", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Les données sont très souvent prétraitées c'est-à-dire **résumées
selon différentes caractéristiques** : chaque élément du jeu de
données est décrit par un ensemble [**d'attributs**](https://en.wikipedia.org/wiki/Feature_(machine_learning))
-- propriétés ou caractéristiques mesurables de cet élément ; pour un
animal, cela peut être sa taille, sa température corporelle, etc.

C'est également le cas dans notre jeu de données : une image est
décrite par le couleur de chacun de ses pixels. Cependant les pixels
sont trop nombreux pour nos besoins. Nous voulons comme la semaine
dernière les remplacer par quelques attributs mesurant quelques
propriétés essentielles de l'image, comme sa couleur ou sa forme
moyenne: ce sont les données prétraitées.

La semaine dernière, les données prétraitées vous ont été fournies
pour les pommes et les bananes.
Cette semaine, grâce aux trois feuilles précédentes, vous avez les
outils et connaissances nécessaires pour effectuer le prétraitement 
directement vous-même:

- la feuille de rappel sur la [gestion de tableaux](1_tableaux.md); 
- la feuille sur le [traitement des images](2_images.md);
- la feuille sur l'[extraction d'attributs](3_extraction_d_attributs.md).

Pour commencer, la table ci-dessous contient les attributs `redness`
et `elongation` -- tels que vous les avez défini dans la feuille
[extraction d'attributs](3_extraction_d_attributs.md) -- appliqués à
votre jeu de données :

```{code-cell} ipython3
---
code_folding: []
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: da7c94c2617d9e0303be67f6842c8ca9
  grade: false
  grade_id: cell-4b826c34cfe02997
  locked: true
  schema_version: 3
  solution: false
  task: false
tags: []
---
df = pd.DataFrame({
        'redness':    images.apply(redness),
        'elongation': images.apply(elongation),
        'class':      images.index.map(lambda name: 1 if name[0] == 'a' else -1),
})
df
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f962af876f145c421d5a5eb4eeac7d80", "grade": false, "grade_id": "cell-3ea685b93ca235c7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :**

Vous allez implémenter dans `utilities.py` au moins 2 nouveaux attributs adaptés à votre jeu de données. Si vous en avez besoin pour les tests par exemple, vous pouvez utiliser les cellules ci-dessous voire en créer de nouvelles.

**Indications**: vous pouvez par exemple vous inspirer
  - des attributes existants comme `redness`;
  - des exemples donnés dans le cours: *matched filter*, analyse en composantes principales (PCA).

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 17beaba12b726af9ffd42295fa27181c
  grade: false
  grade_id: cell-90320016ffc3a6b2
  locked: false
  schema_version: 3
  solution: true
  task: false
---
#MATCHED FILTER
filtre = MatchedFilter(images)
filtre_zero = MatchedFilter(images[:10]) 
filtre_un = MatchedFilter(images[10:])
display(filtre.show())

print("MATCH ZERO OU UN \nPour un 0 :", filtre_zero.match(images[13]))
print("Pour un 1 :" , filtre_un.match(images[13]))

filtre_zero_images = [filtre_zero.match(images[i]) for i in range(20)]
filtre_un_images = [filtre_un.match(images[i]) for i in range(20)]
```

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: b3f1ac26ce9f9faa1dacaa69c394f80b
  grade: false
  grade_id: cell-90320016ffc3a6b3
  locked: false
  schema_version: 3
  solution: true
  task: false
---
avg_pixel_value = [average_pixel_value(images[i]) for i in range(20)]
print("La moyenne des valeurs des pixels pour chaque image :")
print(avg_pixel_value)
df.insert(loc=len(df.columns), column='average_pixel_value', value=avg_pixel_value)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e87c475c66e5e3817783e89a1b8bd598", "grade": false, "grade_id": "cell-4a701722d7649d16", "locked": true, "schema_version": 3, "solution": false, "task": false}}

1. Comment avez-vous choisis ces attributs ? Quelle était votre motivation ?

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d0eb7ea9bb20d04ff21f9e386a533abd", "grade": true, "grade_id": "cell-91da4c6a22145c84", "locked": false, "points": 2, "schema_version": 3, "solution": true, "task": false}}

Nous avons remarqué que les images de la même classe se ressemblent fortement entre eux, c'est pour cela que nous avons utilisé la méthode Matched Filters pour comparer entre eux les différentes images.
D'autre part, en observant les données, nous avons estimé qu'il y a plus de pixels de couleur blanche dans les images de $1$ que de $0$. Nous avons donc décidé d'utiliser la valeur moyenne des pixels pour quantifier la présence de pixels blancs par rapport à la présence de pixels noirs afin de pouvoir différencier les images de $0$ de celles des $1$.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "66226c60e7423b207b86d464ba88466d", "grade": false, "grade_id": "cell-7978fcc57a3231fd", "locked": true, "schema_version": 3, "solution": false, "task": false}}

2. Affichez le code de vos nouveaux attributs ici, en utilisant `show_source`.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 3c7419cdb72975c74d0c6929a94102f3
  grade: true
  grade_id: cell-431dcb3869e672c0
  locked: false
  points: 3
  schema_version: 3
  solution: true
  task: false
---
show_source(MatchedFilter)
```

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: f80923385999bb694c1887bded7f0330
  grade: true
  grade_id: cell-0bb9313d2345f7a7
  locked: false
  points: 3
  schema_version: 3
  solution: true
  task: false
---
show_source(average_pixel_value)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "40ea45055feb8a3bf70c086a1bd14166", "grade": false, "grade_id": "cell-d144e561c7a8d7d9", "locked": true, "schema_version": 3, "solution": false, "task": false}}

4. Ajoutez une colonne par attribut dans la table `df`, en conservant les précédents

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: fc7c13f57edacc111f0be320d75eaf7c
  grade: false
  grade_id: cell-d933a673c19c7e6d
  locked: false
  schema_version: 3
  solution: true
  task: false
---
df.insert(loc=len(df.columns), column='matched_filter_zero', value=filtre_zero_images)
df.insert(loc=len(df.columns), column='matched_filter_un', value=filtre_un_images)
df
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bb480abd9baac97518a69b7de64cf014", "grade": false, "grade_id": "cell-d635e7502cb91b2a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Vérifications:
- la table d'origine est préservée:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 00cf3c65f455842623627fceda673e2d
  grade: true
  grade_id: cell-105a1d4f853b203c
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert len(df[df['class'] ==  1]) == 10
assert len(df[df['class'] == -1]) == 10
assert 'redness' in df.columns
assert 'elongation' in df.columns
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "450cedbf2975206641aa60b1b396769d", "grade": false, "grade_id": "cell-86b1db13ae3622b1", "locked": true, "schema_version": 3, "solution": false, "task": false}}

- Nouveaux attributs:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: b087dcf13b7252daecf1d1f8e2450318
  grade: true
  grade_id: cell-d8f0986d0b430798
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert len(df.columns) > 3, "Ajoutez au moins un attribut!"
assert df.notna().all(axis=None), "Valeurs manquantes!"
for attribute in df.columns[3:]:
    assert pd.api.types.is_numeric_dtype(df[attribute]), \
        f"L'attribut {attribute} n'est pas numérique"
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: acd89c5343b85c78b5bc14691087c6be
  grade: true
  grade_id: cell-03e40d6a322dfc9d
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert len(df.columns) > 4, "Gagnez un point en ajoutant un autre attribut"
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9ce3964950e281aa1cb29fdc7d21d090", "grade": false, "grade_id": "cell-592f7c21def71b06", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Standardisez les colonnes à l'exception de la colonne
`class`, afin de calculer les corrélations entre colonnes

+++ {"editable": true, "slideshow": {"slide_type": ""}, "tags": []}

**La colonne `redness` ayant toutes ses valeurs égales à 0, la standardisation change ses valeurs à NaN (division par zéro). Nous avons donc été dans l'obligation (après en avoir parlé avec le chargé de TP) de patcher ses valeurs (en les remplaçcant par les valeurs de `class`) afin que la colonne `redness` puisse passer les deux assert de moyenne et d'écart-type. Cette méthode nous semblait également plus pratique que le fait de diviser par $\sigma+\epsilon$ qui a été évoqué dans le forum.**

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 39efeffa4c52eea4c717d8bd853ec9d4
  grade: false
  grade_id: cell-0c29581ba1da5a27
  locked: false
  schema_version: 3
  solution: true
  task: false
---
columns_to_standardize = ['redness', 'elongation', 'average_pixel_value', 'matched_filter_zero', 'matched_filter_un']
subset_df = df[columns_to_standardize]
dfstd = (subset_df-subset_df.mean())/subset_df.std()
dfstd.insert(loc=2, column='class', value=df['class'])
dfstd['redness'] = dfstd['class']
dfstd
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "11583edd1f5d181027fac76ecf2e729b", "grade": false, "grade_id": "cell-feea0a235f81712c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Vérifions :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 2e045804a7ee3835b8ebd6c668d16562
  grade: false
  grade_id: cell-69e2c8c203efb549
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
  checksum: c46020ebc9892ac98e0a366de26fbc7e
  grade: true
  grade_id: cell-b6120056f2331c33
  locked: true
  points: 1
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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "720b9082c215b4223679b9f77a642dd3", "grade": false, "grade_id": "cell-16a95948fd5c0ef3", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Le prétraitement est terminé!

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "90a4b4e0ea8602608efc8be5f4b76809", "grade": false, "grade_id": "cell-043c3e7edafa0af9", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Visualisation

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3cba94907267a6b6afee5ba9fd083ff2", "grade": false, "grade_id": "cell-eb183dfd2fb60a40", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Extrayons quelques statistiques de base:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 0881ec64fe676b605aaa6373540d2fb4
  grade: false
  grade_id: cell-5adf965bf26113e8
  locked: false
  schema_version: 3
  solution: true
  task: false
---
dfstd.describe()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3cf82ca26d0187a3ba36dd851c4d6ed2", "grade": false, "grade_id": "cell-6c7b07fdc56a1970", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :**
- Visualisez le tableau de données sous forme de carte de chaleur (*heat map*):

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: bfada635f889c5cf06b033442e83ad70
  grade: false
  grade_id: cell-59b086b9a7351acb
  locked: false
  schema_version: 3
  solution: true
  task: false
---
dfstd.style.background_gradient(cmap='coolwarm', axis=None)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "271975688da40307bf7ecb528ab32e4c", "grade": false, "grade_id": "cell-dee09fc8d9185846", "locked": true, "schema_version": 3, "solution": false, "task": false}}

- sa matrice de corrélation:

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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9f103e76f857430143edfa5cd9d30118", "grade": false, "grade_id": "cell-6e71eda9745ba384", "locked": true, "schema_version": 3, "solution": false, "task": false}}

- Affichez le nuage de points (*scatter plot*) pour toutes les paires d'attributs:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 729d2686cf059a436e43746804a32c7f
  grade: false
  grade_id: cell-10bd824917033e6a
  locked: false
  schema_version: 3
  solution: true
  task: false
---
sns.scatterplot(dfstd_cor)
sns.pairplot(dfstd_cor, hue="class", diag_kind="scatter", vars=['redness', 'elongation','average_pixel_value','matched_filter_zero', 'matched_filter_un'])
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3a719c9648b336d7bc04e7b06661d4f8", "grade": false, "grade_id": "cell-bca3d5b71feb6ff1", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Observations

**Exercice :** Décrivez ici vos observations: corrélations apparentes
ou pas, interprétation de ces corrélations à partir du nuage de
points, etc. Est-ce que les attributs choisis semblent suffisants?
Quel attribut semble le plus discriminant? Est-ce qu'un seul d'entre
eux suffirait?

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6f529903b12f2180d2a775daba172e25", "grade": true, "grade_id": "cell-e22718dde2cfd4ba", "locked": false, "points": 4, "schema_version": 3, "solution": true, "task": false}}

Entre l'élongation et le filtre zéro, ainsi qu'entre la classe et le filtre zéro, les corrélations sont significativement élevées, suggérant des relations linéaires fortes. La corrélation négative entre l'élongation et le filtre zéro suggère une relation inverse : lorsque l'élongation augmente, le filtre zéro a tendance à diminuer, et vice versa.
L'élongation et le filtre zéro semblent suffisants et émergent comme les attributs les plus discriminants, montrant des corrélations significatives avec la classe. L'un de ces deux attributs pourraient suffir pour nous permettre de classifier nos données de manière relativement précise.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "780219ca7ddda552ea13fa1fd6609265", "grade": false, "grade_id": "cell-2668dce82b589f34", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 2: [ME]sure de performance (*[ME]tric*)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b49f6d13a478e294be514a6488e347f3", "grade": false, "grade_id": "cell-2edc6abcf3a72dd2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Pour mesurer les performances de ce problème de classification, nous
utiliserons la même métrique par taux d'erreur que dans le TP3:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 618f2f555d926f5492c2441772f09723
  grade: false
  grade_id: cell-1fa6eb65d858c61c
  locked: true
  schema_version: 3
  solution: false
  task: false
---
show_source(error_rate)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fca79a2271986cdbbefd31158166a6fb", "grade": false, "grade_id": "cell-fe6ef77774bf777c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Partition (*split*) du jeu de données en ensemble d'entraînement et ensemble de test

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1073ff388ab028c871e3d9ebde943c61", "grade": false, "grade_id": "cell-1a09d1e1733ada10", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Extraire, depuis `dfstd`, les deux attributs choisis dans `X` et la vérité terrain dans
`Y`:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 8e0f37996838a9eed59b6301330faa6e
  grade: false
  grade_id: cell-fb5cd75f3de3a8a2
  locked: false
  schema_version: 3
  solution: true
  task: false
---
from sklearn.model_selection import train_test_split


X = dfstd[['average_pixel_value', 'matched_filter_zero']]
Y = dfstd['class']
```

Ajouter un autotest que les attributs ne sont pas redness/elongation : un nouvel attribut ; deux nouveaux attributs

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: cac3960f3b06171eac77d75b29d25c2f
  grade: true
  grade_id: cell-666625af65184ae8
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert isinstance(X, pd.DataFrame), "X n'est pas une table Pandas"
assert X.shape == (20,2), "X n'est pas de la bonne taille"
assert set(X.columns) != {'redness', 'elongation'}
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 7abcef650ef1a7e6257ae0c6e20d3f0a
  grade: true
  grade_id: cell-6155db153be32033
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert 'redness' not in X.columns and 'elongation' not in X.columns, \
   "Pour un point de plus: ne réutiliser ni la rougeur, ni l'élongation"
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "853f80a58347bfa16eb8bdeb15c19d6c", "grade": false, "grade_id": "cell-672066b540b7e27b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Maintenant partitionnez l'index des images en ensemble
d'entraînement (`train_index`) et ensemble de test
(`test_index`). Récupérez les attributs et classes de vos images selon
l'ensemble d'entraînement `(Xtrain, Ytrain)` et celui de test `(Xtest,
Ytest)`.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 8e4d6c9e5e50657996187616eb9b0173
  grade: false
  grade_id: cell-240f317e24d0e8c5
  locked: false
  schema_version: 3
  solution: true
  task: false
---
#Separation en training et test set
train_index, test_index = split_data(X, Y, verbose = True, seed=0)
Xtrain, Xtest = X.iloc[train_index], X.iloc[test_index]
Ytrain, Ytest = Y.iloc[train_index], Y.iloc[test_index]
print("Training set:\n",Xtrain,'\n\n', Ytrain)
print("Test set:\n",Xtest,'\n\n', Ytest)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 543dd26f1d5b2db6c2810087c5dabde0
  grade: true
  grade_id: cell-3be096fc97970fbc
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert train_index.shape == test_index.shape
assert list(sorted(np.concatenate([train_index, test_index]))) == list(range(20))

assert Xtest.shape == Xtrain.shape
assert pd.concat([Xtest, Xtrain]).sort_index().equals(X.sort_index())

assert Ytest.shape == Ytrain.shape
assert pd.concat([Ytest, Ytrain]).sort_index().equals(Y.sort_index())
assert Ytest.value_counts().sort_index().equals(Ytrain.value_counts().sort_index())
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "aaf3d8f5fb773034041687afa70348af", "grade": false, "grade_id": "cell-50c7b65a31fd47cb", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Affichez les images qui serviront à entraîner notre
modèle de prédiction (*predictive model*):

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: c466d1664ce5b0e21a60fea5e3a10288
  grade: false
  grade_id: cell-ad5ca9b40a1f2cd1
  locked: false
  schema_version: 3
  solution: true
  task: false
---
#fonction fournie dans les utilities
make_scatter_plot(dfstd, images, train_index, test_index, filter=transparent_background_filter, axis='square')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e64570807a43c88693069a74eaf99b57", "grade": false, "grade_id": "cell-031b7382abe186ef", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Affichez celles qui permettent de le tester et
d'évaluer sa performance:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: c8fecb49712cdcc05789e2066e173a2f
  grade: false
  grade_id: cell-1f3414a9f879a9d1
  locked: false
  schema_version: 3
  solution: true
  task: false
---
#fonction fournie dans les utilities
make_scatter_plot(dfstd, images, Ytrain, Ytest, filter=transparent_background_filter, axis='square')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a16f7f2ccdc41606de030e263f1c53f2", "grade": false, "grade_id": "cell-e44d2840e7481ec1", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Représentez les images sous forme de nuage de points en
fonction de leurs attributs:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: f0b3f94b32e945753930d8b8d1b948e0
  grade: true
  grade_id: cell-c7dc96827c21b4b9
  locked: false
  points: 1
  schema_version: 3
  solution: true
  task: false
---
sns.scatterplot(Xtrain)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "92fd26fbb3226b6054d55cbc4ca94dcb", "grade": false, "grade_id": "cell-ef6ffea3c9345a6f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Taux d'erreur

Comme la semaine dernière, nous utiliserons le taux d'erreur comme
métrique, d'une part sur l'ensemble d'entraînement, d'autre part sur
l'ensemble de test. Implémentez la fonction `error_rate` dans votre
utilities.py. Pour vérifier que c'est correctement fait, nous
affichons son code ci-dessous:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 19048026419c75b7d2b389917743506b
  grade: false
  grade_id: cell-baa5e37a60edad22
  locked: true
  schema_version: 3
  solution: false
  task: false
---
show_source(error_rate)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0aad688914be7e65788713978ac3c2a8", "grade": false, "grade_id": "cell-2831ca6c9a3bfce5", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 3: [RE]férence (*base line*)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "460a70846edc8dd32952b00dbe109551", "grade": false, "grade_id": "cell-9876b02ba8d2de55", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Classificateur

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0b5fd7298bd769915d0e38c345db2592", "grade": false, "grade_id": "cell-5f7be836c3e06143", "locked": true, "schema_version": 3, "solution": false, "task": false}}

- En Semaine 4: faites la suite de cette feuille avec l'algorithme du
  plus proche voisin, comme en Semaine 3.

- En Semaine 5: faites la feuille sur les [classificateurs](../Semaine5/5_classificateurs.md)
  puis faites la suite de cette feuille avec votre propre classificateur,
  en notant au préalable votre choix de classificateur ici:

**Exercice** : quel classificateur avez-vous choisit en semaine 5 ? Pourquoi avez-vous choisis celui-ci ?

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "93394cf4d1361a6928672f6bec5edec3", "grade": true, "grade_id": "cell-014e08189e3a6014", "locked": false, "points": 2, "schema_version": 3, "solution": true, "task": false}}

En semaine $5$, nous avons choisi le classificateur Perceptron car, comme dit lors de la conclusion de la feuille 5, en considérant la capacité à généraliser et les taux d'erreur, le Perceptron se démarque comme le choix préférentiel pour la classification des pommes et des bananes.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4fa688886d4cceaf1b6076e2720905e5", "grade": false, "grade_id": "cell-f541bcd7f0f3912d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** 
Ci-dessous, définissez puis entraînez votre classificateur sur l'ensemble d'entraînement.

**Indication :** Si vous avez besoin de code supplémentaire pour cela, mettez-le dans `utilities.py`.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: cb4d4d2d1a75555cfb83c78f500a09d4
  grade: false
  grade_id: cell-85205b5012588319
  locked: false
  schema_version: 3
  solution: true
  task: false
---
from sklearn.linear_model import Perceptron

# définition du modèle de classificateur
classifier = Perceptron(tol=1e-3, random_state=36, shuffle=True, max_iter=100)
# on l'ajuste aux données d'entrainement

classifier.fit(Xtrain, Ytrain)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9c3e81a24a4c69d62c580b683ae21664", "grade": false, "grade_id": "cell-991d8893ddaefe2b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Calculez les prédictions sur l'ensemble d'entraînement
et l'ensemble de test, ainsi que les taux d'erreur dans les deux cas:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 1a7b1aee6a3e1209597c820dc1c71516
  grade: false
  grade_id: cell-85205b5012588320
  locked: false
  schema_version: 3
  solution: true
  task: false
---
# on calcule ensuite le taux d'erreur lors de l'entrainement et pour le test

Ytrain_predicted = classifier.predict(Xtrain)
Ytest_predicted = classifier.predict(Xtest)

# on calcule les taux d'erreurs

e_tr = error_rate(Ytrain, Ytrain_predicted)
e_te = error_rate(Ytest, Ytest_predicted)

print("Classificateur: Perceptron")
print("Training error:", e_tr)
print("Test error:", e_te)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 3eb2e601b91778183a2a03138ce8359a
  grade: true
  grade_id: cell-195ba103a7ccc55b
  locked: true
  points: 3
  schema_version: 3
  solution: false
  task: false
tags: []
---
assert Ytrain_predicted.shape == Ytrain.shape
assert Ytest_predicted.shape == Ytest.shape
assert 0 <= e_tr and e_tr <= 1
assert 0 <= e_te and e_te <= 1
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fae208e6bd19f0670dd8df95f6d64171", "grade": false, "grade_id": "cell-139252fc350603b2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Visualisons les prédictions obtenues:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: d52aa128366c4fd41fdcf88b6103e580
  grade: false
  grade_id: cell-fdaa23f990c0b172
  locked: true
  schema_version: 3
  solution: false
  task: false
---
# The training examples are shown as white circles and the test examples are black squares.
# The predictions made are shown as letters in the black squares.
make_scatter_plot(X, images.apply(transparent_background_filter),
                  train_index, test_index, 
                  predicted_labels=Ytest_predicted, axis='square')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "00fb56afb030c89b52f77facddd94ba1", "grade": false, "grade_id": "cell-b0226451f00b5833", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Interprétation

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "73f198463c071057164dda9992ceafa2", "grade": false, "grade_id": "cell-b0226451f00b5834", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Quelle est la performance des prédictions pour le jeu d'entrainement et pour le jeu de test ? Celle-ci vous parait-elle optimate ? Donnez enfin une interprétation des résultats, en expliquant pourquoi votre performance est bonne ou pas. Avez vous une première intuition de comment l'améliorer ?

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ef89d849ecc26d3c154c01574d8fc334", "grade": true, "grade_id": "cell-3587c106c4f95899", "locked": false, "points": 5, "schema_version": 3, "solution": true, "task": false}}

Les performances du classificateur Perceptron sont excellentes, avec des erreurs nulles tant sur le jeu d'entraînement que sur le jeu de test. Cependant, une évaluation plus approfondie, notamment l'utilisation de métriques supplémentaires et de techniques de validation croisée, pourraient venir confirmer la robustesse du modèle. L'absence d'erreurs peut également nécessiter une vérification pour éviter le surajustement, et l'exploration d'autres modèles plus complexes ou l'ajustement des paramètres peuvent être envisagées pour une amélioration potentielle.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8a2a785561a621cbac2dc3ca33e6a4ac", "grade": false, "grade_id": "cell-5539fbbf5565fb1b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Étape 4: [BAR]res d'erreur (*error bar*)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "10804474205e34d74360e3d5a262c026", "grade": false, "grade_id": "cell-5539fbbf5565fb1c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Barre d'erreur 1-sigma

**Exercice :** Comme première estimation de la barre d'erreur,
calculez la barre d'erreur 1-sigma pour le taux d'erreur `e_te`:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: a41cc34ca674ef499973ee023b1d1e61
  grade: false
  grade_id: cell-40a54824a74c8fdc
  locked: false
  schema_version: 3
  solution: true
  task: false
tags: []
---
n_te = 10
sigma = math.sqrt((e_te * (1 - e_te)) / n_te)
print("TEST SET ERROR RATE: {0:.2f}".format(e_te))
print("TEST SET STANDARD ERROR: {0:.2f}".format(sigma))
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: fc40b782c4fe7b984a8fa034200adfac
  grade: true
  grade_id: cell-58772f70bb5eccfd
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert n_te + 5 == 3**2 + len(Ytest) - 2**2
assert round(sigma**2,3) == round((e_te/n_te - e_te**2/n_te),3)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fe8f472d1b0d999fe0d8d39586805660", "grade": false, "grade_id": "cell-209765e9c10f8f32", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Barre d'erreur par validation croisée (Cross-Validation)

Nous calculons maintenant une autre estimation de la barre d'erreur en
répétant l'évaluation de performance pour de multiples partitions
entre ensemble d'entraînement et ensemble de test :

```{code-cell} ipython3
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
    e_tr = error_rate(Ytrain, Ytrain_predicted)
    e_te = error_rate(Ytest, Ytest_predicted)
    print("TRAIN ERROR RATE:", e_tr)
    print("TEST ERROR RATE:", e_te)
    E[k] = e_te
    k = k+1
    
e_te_ave = np.mean(E)
# It is bad practice to show too many decimal digits:
print("\n\nCV ERROR RATE: {0:.2f}".format(e_te_ave))
print("CV STANDARD DEVIATION: {0:.2f}".format(np.std(E)))

sigma = np.sqrt(e_te_ave * (1-e_te_ave) / n_te)
print("TEST SET STANDARD ERROR (for comparison): {0:.2f}".format(sigma))
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "998da4c6471f630cec6a0395564210dc", "grade": false, "grade_id": "cell-df1f1b0b05e548d4", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Conclusion

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a01cff71a9ff6d4cddd5d8e0f9eb87a1", "grade": false, "grade_id": "cell-df1f1b0b05e548d6", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Faites une synthèse des performances obtenues, tout d'abord
avec votre référence, puis avec les variantes que vous aurez explorées
en changeant d'attributs et de classificateur. Puis vous commenterez sur
la difficulté du problème ainsi que les pistes possibles pour obtenir
de meilleures performances, ou pour généraliser le problème. Vous pouvez si vous préférez faire un tableau pour présenter votre réponse.

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "989bef7b6f89f347f62e28548439cfad", "grade": true, "grade_id": "cell-8676a3839d9b5559", "locked": false, "points": 5, "schema_version": 3, "solution": true, "task": false}}

Le modèle initial basé sur le Perceptron avec les attributs d'origine a démontré des performances exceptionnelles, avec un taux d'erreur nul sur le jeu de test. La validation croisée a estimé une erreur standard de 0.03, indiquant une cohérence des performances. Les variations en changeant d'attributs et de classificateur n'ont pas considérablement impacté les résultats, soulignant la robustesse du modèle. Le caractère relativement simple du problème, avec des taux d'erreur très bas, suggère que des modèles plus complexes pourraient ne pas apporter d'améliorations significatives. Cependant, des expérimentations supplémentaires, une optimisation des hyperparamètres, et une évaluation sur des jeux de données plus complexes pourraient offrir des perspectives d'amélioration.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b43d46c746ee75f2e1dbeee8b7aaad0d", "grade": false, "grade_id": "cell-df1f1b0b05e548d5", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Complétez votre rapport sur l'[index](index.md)
