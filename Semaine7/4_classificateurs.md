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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d07c8764fba1b4d7f0ea2277a4a2081d", "grade": false, "grade_id": "cell-6cfa223d34cccf44", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

# Comparer des classificateurs

Dans la [feuille précédente](3_extraction_d_attributs.md), nous avons
observé que les performances pouvaient varier selon le niveau de
prétraitement des données (données brutes, données nettoyées,
extractions d'attributs, etc.). Cependant, l'analyse de performance
n'a été conduite qu'avec un seul classificateur (plus proches
voisins).

Il est posssible que chaque classificateur donne des résultats
différents pour un niveau de pré-traitement donné.

Dans cette feuille, on étudie les performances selon le type de
classificateur. Les étapes seront:
1. Déclarer et entraîner les différents classificateurs sur nos
   données;
2. Visualiser les performances de chaque classificateur;
3. Comprendre et identifier le sous-apprentisssage et le
   surapprentissage;
4. Étudier un comité de classificateurs et
   l'incertitude dans les données;
5. **Pour aller plus loin ♣**: Apprentissage profond et transfert
   d'apprentissage.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "03e5d0917d76860a096938f4ea934c38", "grade": false, "grade_id": "cell-88f029d0e00b1e14", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Entraînement des différents classificateurs

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ac6554c6da8049e5b0dffa5555a08dfa", "grade": false, "grade_id": "cell-12a48b53cb2b329c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Import des bibliothèques

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: da41b2f7b3362c8c7693c5b328115982
  grade: false
  grade_id: cell-bdc62a79c458052f
  locked: true
  schema_version: 3
  solution: false
  task: false
---
import os, re
from glob import glob as ls
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import pandas as pd
import seaborn as sns; sns.set()
from PIL import Image
%load_ext autoreload
%autoreload 2
import warnings
warnings.filterwarnings("ignore")
from sys import path

from utilities import *
from intro_science_donnees import data
from intro_science_donnees import *
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4346685a972caed09764f36288d66a7a", "grade": false, "grade_id": "cell-b3011b2b81ff1237", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Import des données

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b177335d943971cee0655fd5fccee414", "grade": false, "grade_id": "cell-f511a65f58aac0d7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous chargeons les images prétraitées dans la feuille précédente :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 720a30085c1caca7ad1990de11afa760
  grade: false
  grade_id: cell-d8bcf6df946d3631
  locked: true
  schema_version: 3
  solution: false
  task: false
---
dataset_dir = 'clean_data'

images = load_images(dataset_dir, "*.png")
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2e0195048a2892e62032f05446e322eb", "grade": false, "grade_id": "cell-543e7be63e4a1b63", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Vérifions l'import en affichant les 20 premières images :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 358c7060e8754d3dfc2ff565457d4f64
  grade: false
  grade_id: cell-8cf64e3e7c57bcba
  locked: true
  schema_version: 3
  solution: false
  task: false
---
image_grid(images[:20])
```

```{code-cell} ipython3
#TRAITEMENT DES IMAGES EFFECTUES DANS LA FEUILLE 3

df_clean = pd.read_csv('clean_data.csv', index_col=0)
df_clean
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e2c27e4ff8c33ecd484637a207c00612", "grade": false, "grade_id": "cell-33930eb177ebd842", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Pour mettre en œuvre des classificateurs, chargez dans `df_features` les 
attributs extraits dans la fiche précédente.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 6db01de0fd5fd066b5c1b96d0b4092fd
  grade: false
  grade_id: cell-9b7ec7e81dca8f9a
  locked: false
  schema_version: 3
  solution: true
  task: false
---
def grayscale(img: Image.Image) -> np.ndarray:
    """Return image in gray scale"""
    return np.mean(np.array(img)[:, :, :3], axis=2)

class MatchedFilter:
    ''' Matched filter class to extract a feature from a template'''
    def __init__(self, examples):
        ''' Create the template for a matched filter; use only grayscale'''
        # Compute the average of all images after conversion to grayscale
        M = np.mean([grayscale(img)
                     for img in examples], axis=0)
        # Standardize
        self.template = (M - M.mean()) / M.std()

    def show(self):
        """Show the template"""
        fig = Figure(figsize=(3, 3))
        ax = fig.add_subplot()
        ax.imshow(self.template, cmap='gray')
        return fig

    def match(self, img):
        '''Extract the matched filter value for a PIL image.'''
        # Convert to grayscale and standardize
        M = grayscale(img)
        M = (M - M.mean()) / M.std()
        # Compute scalar product with the template
        # This reinforce black and white if they agree
        return np.mean(np.multiply(self.template, M))

#MATCHED FILTER
filtre = MatchedFilter(clean_images)
filtre_zero = MatchedFilter(clean_images[:10]) 
filtre_un = MatchedFilter(clean_images[10:])
display(filtre.show())

print("MATCH ZERO OU UN \nPour un 0 :", filtre_zero.match(clean_images[19]))
print("Pour un 1 :" , filtre_un.match(clean_images[19]))

filtre_zero_images = [filtre_zero.match(clean_images[i]) for i in range(20)]
filtre_un_images = [filtre_un.match(clean_images[i]) for i in range(20)]
for i in range(20):
    print(f"{i} : {filtre_zero_images[i]}  {filtre_un_images[i]}")

# Assuming filtre_zero_images and filtre_un_images are already defined

# Create a dictionary with the desired attributes and their corresponding values
data = {
    'filtre_zero_images': filtre_zero_images,
    'filtre_un_images': filtre_un_images,
    'avg_pixel_value' : avg_pixel_value,
            'class':      images.index.map(lambda name: 1 if name[0] == 'a' else -1)

}

# Assuming you have a list of file names to use as index for the Series
file_names = [f'image_{i}.png' for i in range(20)]

# Create the pandas Series
series = pd.DataFrame(data, index=file_names)

# Display the series
print(series)

df = pd.read_csv("../Semaine3/attributs.csv", index_col=0)
df
# standardisation
dfstd =  (df - df.mean()) / df.std()
dfstd['class'] = df['class']
```

```{code-cell} ipython3
X = dfstd[['redness', 'elongation']]
Y = dfstd['class']
#partition des images
train_index, test_index = split_data(X, Y, seed=3)

#partition de la table des attributs
Xtrain = X.iloc[train_index]
Xtest = X.iloc[test_index]
#partition de la table des étiquettes
Ytrain = Y.iloc[train_index]
Ytest = Y.iloc[test_index]
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bd0fa687a58501d48b18eac08050084a", "grade": false, "grade_id": "cell-4cf16710f27a0f3a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On vérifie que nos données sont normalisées :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 67ad4d45ad5a24d2fdfa2a426eb27bae
  grade: false
  grade_id: cell-fb4a3a55919f5dbc
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df_features.describe()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5342f94306725fddfc30af53878e4240", "grade": false, "grade_id": "cell-a1370cb13b62811d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Déclaration des classificateurs

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "30a5e62b3ae3ace075561f17d4636c27", "grade": false, "grade_id": "cell-485190599069b9ed", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous allons à présent importer les classificateurs depuis la librairie
`scikit-learn`. Pour cela, on stockera:
- les noms des classificateurs dans la variable `model_name`;
- les classificateurs eux-mêmes dans la variable `model_list`.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 8a07223e02cbaf66c87e9f55ac997b31
  grade: false
  grade_id: cell-7ea31b030159c666
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

model_name = ["Nearest Neighbors", "Parzen Windows",  "Linear SVM", "RBF SVM", "Gaussian Process",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA"]
model_list = [
    KNeighborsClassifier(3),
    RadiusNeighborsClassifier(radius=12.0),
    SVC(kernel="linear", C=0.025, probability=True),
    SVC(gamma=2, C=1, probability=True),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=10),
    RandomForestClassifier(max_depth=10, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1, max_iter=1000),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "59fa4bc0f1c7687b142942bd9727985b", "grade": false, "grade_id": "cell-8bd61b03b2d9ca78", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

La bibliothèque `scikit-learn` nous simplifie la tâche : bien que les
classificateurs aient des fonctionnements très différents, leurs
interfaces sont identiques (rappelez vous la notion d'encapsulation
vue dans le cours «Programmation Modulaire»). Les méthodes sont:
- `.fit` pour entraîner le classificateur sur des données
  d'entraînement;
- `.predict` pour prédire des étiquettes sur les données de test;
- `.predict_proba` pour obtenir des prédictions sur les données de
  test sous forme de probabilités sur les classes;
- `.score` pour calculer la performance du classificateur.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5db027d943e135a1abfe8bcc3ea13f7f", "grade": false, "grade_id": "cell-7ad47d64e9489ab2", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

## Visualisation des performances des classificateurs

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3ff41f00a1c64c1b970e621058a414e7", "grade": false, "grade_id": "cell-0e402814b4b67a62", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Nous allons à présent faire des tests systématiques sur cet ensemble
de données (attributs de l'analyse de variance univiarié). La fonction
`systematic_model_experiment(data_df, model_name, model_list,
sklearn_metric)` permet de réaliser ces tests systématiques.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 77a5bc452230387762fa550ac6eb04bd
  grade: false
  grade_id: cell-f1250a383287f8ca
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
??systematic_model_experiment
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a7d121143da56d819c4fcc37fa2cc8a8", "grade": false, "grade_id": "cell-b75e05e6b7fb13a1", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Que renvoit cette fonction ?

+++ {"deletable": false, "editable": true, "nbgrader": {"cell_type": "markdown", "checksum": "b4a096bf3ddaf0fb0c59a21a62953ebf", "grade": true, "grade_id": "cell-3097cbc02cd7cccb", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

VOTRE RÉPONSE ICI

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 27dd3529cbf85954fe1572edd4820fe8
  grade: false
  grade_id: cell-eb3cbeb9d276e186
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
from sklearn.metrics import balanced_accuracy_score as sklearn_metric
compar_results = systematic_model_experiment(df_features, model_name, model_list, sklearn_metric)
compar_results.style.format(precision=2).background_gradient(cmap='Blues')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "942233865d9b63b146700d789855276a", "grade": false, "grade_id": "cell-79df935d9f0c8344", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

Quelle méthode obtient les meilleures performances de test?

:::

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 049482cf42bf228c3f073ee945281809
  grade: false
  grade_id: cell-695c5801f831d0ac
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
model_list[compar_results.perf_te.argmax()]
```

+++ {"deletable": false, "editable": true, "nbgrader": {"cell_type": "markdown", "checksum": "c3546817d987a9cf26095d410d344ab8", "grade": true, "grade_id": "cell-b65bf594f7626e4e", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

VOTRE RÉPONSE ICI

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "11316010316b36d94ad81178756c7228", "grade": false, "grade_id": "cell-961879212e462260", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

On peut également représenter les performances dans un graphique en
barres. Sachant que le nom de la métrique s'obtient avec `sklearn_metric.__name__`, ajouter à la figure le nom des axes pertinents.

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 080cd27b9a465d1b052f10649a9a2dc5
  grade: true
  grade_id: cell-1c13f5967f208b71
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
compar_results[['perf_tr', 'perf_te']].plot.bar()
plt.ylim(0.5, 1)

# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9eae5f60545a3f343da208837e696935", "grade": false, "grade_id": "cell-ae42ddffdafe2624", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

##  Sous-apprentissage et surapprentissage

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8632d8f026fab6677151290d2b02763b", "grade": false, "grade_id": "cell-7bce4f2d0e3af501", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Lorsque l'on entraîne un classificateur sur des données, deux
comportements sont à éviter:

- Le ***sous-apprentissage*** (*under-fitting*).
- Le ***sur-apprentissage*** (*over-fitting*).

Ces concepts sont vus en [Semaine 8](../Semaine8/CM8.md)


Analysons quels classificateurs ont sur-appris respectivement sous-appris. Pour
cela nous allons identifier les classificateurs dont les *performances de **test*** sont
   inférieures à la *performance de **test** médiane*. `tebad` est un vecteur de booléens.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: f31ee3f5e0efa68ea667b4685586a307
  grade: false
  grade_id: cell-f4aa00764a84d72a
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
tebad = compar_results.perf_te < compar_results.perf_te.median()
tebad
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bcb6ab0264d30d34e6e43a2ab797b4f8", "grade": false, "grade_id": "cell-7647298fb39a7d9a", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

Calculer maintenant dans `trbad`  les classificateurs dont les performances
   d'entrainement sont inférieurs à la performance d'entrainement médiane. `trbad` est un vecteur de booléens.

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 9de2940c08bab41f26dcca421ac07538
  grade: true
  grade_id: cell-502cf2f04f40a8c8
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "56df06cdbf78fa69817bebdd752ba4ca", "grade": false, "grade_id": "cell-674c1cc795d75b15", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

On peut alors identifier les classificateurs qui ont sur-appris (qui correpondent à `True`)
c'est-à-dire ceux dont la performance d'entraînement est **supérieure à la médiane** et 
celle de test est **inférieure à la médiane**. On écrit :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 13891475d4087936c14486f8abcb45f4
  grade: false
  grade_id: cell-925e0e3b353a126b
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
overfitted = tebad & ~trbad
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0955b4f5597dcfcba14098ae47166102", "grade": false, "grade_id": "cell-1f6926f6861f5c4f", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

De la même facon, définir `underfitted` un vecteur de booléens qui indique les classificateurs dont les performances
    d'entrainement et de test sont inférieures à la médiane

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 3195a23d5822e431ea8afc2ce154cca0
  grade: true
  grade_id: cell-393d48b50625f575
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "17dad4f7b27d8a20141d3f0898d9fd57", "grade": false, "grade_id": "cell-221642d5537da55a", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

Implémenter en vous inspirant du code ci-dessus la fonction `analyse_model_experiments` qui:
- prend en entrée les résultats de plusieurs classificateurs sous la forme d'un tableau
- identifie par deux vecteurs de booléens les classificateurs dont les performances de test, respectivement d'entrainement, sont inférieures à la performance de test, resp d'entrainement médiane.
- identifie dans des vecteurs de booléens les classificateurs qui ont sur-appris dans `overfitted` et respectivement sous-appris dans `underfitted`
- ajoute deux colonnes au tableau puis le renvoit
:::

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 66012a0227948aa05b583e95069b6eb9
  grade: false
  grade_id: cell-bf5de279a6b91aac
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
show_source(analyze_model_experiments)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ea23c1401b5bf67b1a7e6788814e4cfa", "grade": false, "grade_id": "cell-3d2b08fc31dfc5c7", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Puis on applique la fonction à compar_results

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 0dbfd8e74c5b89918f20eadc601305eb
  grade: false
  grade_id: cell-47b4be19fd08b955
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
analyze_model_experiments(compar_results)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "31052686c69de534cf28826ecec44f5b", "grade": false, "grade_id": "cell-c4a46b1532ae7fe4", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

Quelles sont les classificateurs qui ont sous-appris resp. sur-appris?

:::

+++ {"deletable": false, "editable": true, "nbgrader": {"cell_type": "markdown", "checksum": "cda4d2af71e41fea244d7704a5eb8e0a", "grade": true, "grade_id": "cell-9e913181dae0665d", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

VOTRE RÉPONSE ICI

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1bcd9f096b652c3c05e903cc38359bb0", "grade": false, "grade_id": "cell-0f2a5f4ad1df888b", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

## Comité de classificateurs et incertitude

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e692af2b4fbdb048b79c421b69b7eb18", "grade": false, "grade_id": "cell-d85f6153b8c45c56", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Un comité de classificateurs est un classificateur dans lequel les
réponses de plusieurs classificateurs sont combinées en une seule
réponse. En d'autres termes, les classificateurs **votent** pour les
prédictions émises.

On pourrait considérer notre liste de classificateur `model_list`
comme un comité de classificateurs, entraînés sur les mêmes données
d'entraînement, et faisant des prédictions sur les mêmes données de
test. Regardez le code suivant; il est en réalité simple: on définit
les méthodes `fit`, `predict`, `predict_proba` et `score` comme
faisant la synthèse des résultats des classificateurs contenus dans
`self.model_list`.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: dd5ff03c3342a8e9b6ae82aab7087fcc
  grade: false
  grade_id: cell-4c2fdd613259b27c
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
class ClassifierCommittee():
    def __init__(self, model_list):
        self.model_list = model_list
        
    def fit(self,X,y):
        for model in self.model_list:
            model.fit(X,y)
    def predict(self,X):
        predictions = []
        for model in self.model_list:
            predictions.append(model.predict(X))
        predictions = np.mean(np.array(predictions),axis = 0)
        results = []
        for v in predictions:
            if v < 0:
                results.append(-1)
            else:
                results.append(1)
        return np.array(results)
    
    def predict_proba(self,X):
        predictions = []
        for model in self.model_list:
            predictions.append(model.predict_proba(X))
        return np.swapaxes(np.array(predictions), 0, 1)
    def score(self,X):
        scores = []
        for model in self.model_list:
            scores.append(model.score(X,y))
        return np.swapaxes(np.array(scores), 0, 1)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7d1911825fe6724859fbcfe1d62dc02b", "grade": false, "grade_id": "cell-452758ca86801b63", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

On définit un comité à l'aide de ce code:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 07de6e9dc6b8360cc5bbb427252173c9
  grade: false
  grade_id: cell-c41772320064e711
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
commitee = ClassifierCommittee(model_list)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0cebecc4a725f98bc12066643637db73", "grade": false, "grade_id": "cell-0f0d841fcc1b3058", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice 

Quelles seraient les performances d'un tel classificateur?  Calculer les performances de `commitee`

::::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 4251d1c67486b09e0d357fbfa7083799
  grade: true
  grade_id: cell-e2a2cd51a5aec85e
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "762e8ae2505c019d1ad004a5c9a67c6e", "grade": false, "grade_id": "cell-7c9cfd87890b021f", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

La performance de l'ensemble de classificateurs n'est pas forcément
meilleure que les classificateurs pris individuellement. Cependant,
l'accord ou le désaccord des classificateurs sur les prédictions peut
nous donner des informations sur l'incertitude des données.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6fae4dc43c94a47c1d04001ebd123eb3", "grade": false, "grade_id": "cell-645f39bd1be4bf65", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

En effet, chaque classificateur peut émettre des probabilités sur les
classes avec la méthode `predict_proba`.  Pour quantifier
l'incertitude d'une image, on peut distinguer deux cas de figure :
- **l'incertitude aléatorique** : les classificateurs sont plus ou moins certains de leur prédiction. 
- **l'incertitude épistémique** : les classificateurs sont d'accord ou pas entre eux. 

Ces incertitudes vont être d'autant plus fortes pour les images proches des frontières de décision (les bananes rouges par exemple).
Intéressons nous aux images avec une faible incertitude épistémique
(les classificateurs sont d'accord) et une grande incertitude
aléatorique (les classificateurs sont incertains de la
prédiction). Cela correspond à des images se situant aux abords de la
frontière de décision entre nos deux catégories.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1700a72f498d5596b4d490a6b6de8a72", "grade": false, "grade_id": "cell-0fea84bc70094418", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

### Incertitude aléatorique

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6f2e581f20f17ffd59c4c5127d96a503", "grade": false, "grade_id": "cell-3f21c655edcfd8ab", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Nous allons utiliser l'[entropie de
Shannon](https://fr.wikipedia.org/wiki/Entropie_de_Shannon), qui est
une mesure en théorie de l'information permettant d'estimer la
quantité d'information contenu dans une source d'information (ici
notre probabilité sur les classes): 

$$H(X) = - \sum_{i=1}^{n}P(x_i)log_2(x_i)$$

où $x_i$ est la probabilité de classification sur la classe $i$.

On récupère alors les prédictions de nos images pour les 11
classificateurs :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 5362c786e5ef2c69491d10d2ee81fb51
  grade: false
  grade_id: cell-3c34e1651bb890d5
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
X = df_features.iloc[:, :-1].to_numpy()
Y = df_features.iloc[:, -1].to_numpy()
commitee.fit(X, Y)
prediction_probabilities = commitee.predict_proba(X)
prediction_probabilities.shape
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2e604742a060b96fee211d4434e5c84d", "grade": false, "grade_id": "cell-0e697b40b4cd7d5c", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

La dimension de notre matrice de prédiction est donc: `(nombre
d'images, nombre de classificateur, nombre de classess)`. Appliquons
l'entropie pour chaque prédiction de chaque classificateur :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 442a78916f4968d2123c742a784a6cf1
  grade: false
  grade_id: cell-1ba73503201dffe9
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
from scipy.stats import entropy
entropies_per_classifier = entropy(np.swapaxes(prediction_probabilities, 0, 2))
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "af1d0c57e4e16635efd36827df98e422", "grade": false, "grade_id": "cell-f5c2145fe08fa7d8", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

On moyenne les entropies d'une image entre les classificateurs :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: bb57f6978cfb9233c5ac5eda457fa4e9
  grade: false
  grade_id: cell-73427b1fa71fa9e1
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
entropies = np.mean(entropies_per_classifier, axis = 0)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e362f815120c54d2dcb78e09bd948def", "grade": false, "grade_id": "cell-9679ab6f47fd7bf1", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Puis on ajoute ces valeurs dans une table que l'on trie par ordre
décroissant d'entropie. Les images avec l'entropie la plus grande sont
les plus incertaines et donc les plus informatives pour le modèle :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 0b85d70f51c3d7ff5be3373bf6726704
  grade: false
  grade_id: cell-d220e1fb8963eaa7
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
df_uncertainty = pd.DataFrame({"images" : images,
                           "aleatoric" : entropies})
df_uncertainty = df_uncertainty.sort_values(by=['aleatoric'],ascending=False)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 1d628feba8f099ab3e978887541fcc7e
  grade: false
  grade_id: cell-b55334aaccacdc1e
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
df_uncertainty.style.background_gradient(cmap='RdYlGn_r')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "820858ad5bd4bdb646b3f815eea63e8a", "grade": false, "grade_id": "cell-dd18631ce35028c4", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Affichons les 10 images **les plus incertaines** pour le comité de
classificateurs, selon cette mesure aléatorique de l'incertitude. Ces
images nous donne une idée de l'ambiguité intrinsèque de notre base de
données.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 8e59de3eaa90738fe47a4eef68bedb38
  grade: false
  grade_id: cell-8876c75845013319
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
uncertain_aleatoric_images = df_uncertainty['images'].tolist()
image_grid(uncertain_aleatoric_images[:10])
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2f247af9d02e840566bff80d25de6150", "grade": false, "grade_id": "cell-e978b5155f366bac", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition}

Afficher maintenant les 10 images les **plus certaines** pour
notre comité de classificateurs 

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 9cb74c0117b4605ac165ee4fbd77fce8
  grade: true
  grade_id: cell-b763c71e41096556
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "editable": true, "nbgrader": {"cell_type": "markdown", "checksum": "51f68a9045cca467d7d81fe694f6a848", "grade": true, "grade_id": "cell-a4f0ee22f69b361f", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

Ces résultats vous semblent-ils surprenants? Expliquer.

VOTRE RÉPONSE ICI

:::

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "dcb929b82cad5e239c92ed22403fa8c3", "grade": false, "grade_id": "cell-6b9360942d3fe79e", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

### Incertitude épistémique

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7d5c0d89c7b2c4203c0cee559fdcf2af", "grade": false, "grade_id": "cell-c4382c4bc5b4e599", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Pour l'incertitude épistémique, on va simplement moyenner les écarts types entre  entre les
classificateurs. Comme on n'a que deux classes l'écart type entre les classificateurs pour la première classe est la même que pour la seconde:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: f1a341327c5ee06956f7fe4cbd8704d4
  grade: false
  grade_id: cell-3728f14b1c193eea
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
# std entre les classificateurs
epistemic_uncertainty = np.std(prediction_probabilities[:,:,0], axis = 1)
print(epistemic_uncertainty.shape)

print(epistemic_uncertainty)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d9cb5a4fc442d71b779c26caec54dc45", "grade": false, "grade_id": "cell-04b95b8d4e6c61dd", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

Ajouter cette mesure au tableau `df_uncertainty` .

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: f730458e4944b4297b5d0ce15609cb58
  grade: true
  grade_id: cell-0b5180d6df21bdeb
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
# VOTRE CODE ICI
raise NotImplementedError()
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 834337bd006f098a1c0df5a0ff2ba7f4
  grade: false
  grade_id: cell-dac2e40e9ec3ff2d
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
df_uncertainty = df_uncertainty.sort_values(by=['epistemic'],ascending=False)
df_uncertainty.style.background_gradient(cmap='RdYlGn_r')
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 6681d1d9ab7a3e4e0ce1e7c9aac79f6d
  grade: false
  grade_id: cell-265a2aec9d6e94da
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df_uncertainty[["aleatoric",'epistemic']].corr()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "396efed5449206d0823fcbaad92cbd3d", "grade": false, "grade_id": "cell-26aeb59af687a719", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Les valeurs d'incertitude aléatorique (entropie) et épistémiques (std)
ne semblent pas très corrélées. Afficher les 10 images les plus
incertaines selon la mesure d'incertitude épistémique :

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: af5bb506d03cef74636cfff21d2424aa
  grade: true
  grade_id: cell-f4b879de9d85049a
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
---
# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a87c41e2a2a1bdb1795f0d36f41251fd", "grade": false, "grade_id": "cell-5adf2198497793b2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Afficher les 10 images les plus
certaines selon la mesure d'incertitude épistémique :

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 93e5b72dc7c830d233541a055c57c11a
  grade: true
  grade_id: cell-5cf73e64fa0f9ed3
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
---
# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6fbe77d94306114f7f32e8a6d5e8aac7", "grade": true, "grade_id": "cell-d32fa098a68274b0", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

:::{admonition} Exercice

Ces résultats vous semblent-ils surprenants? Expliquer.

VOTRE RÉPONSE ICI

:::

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "04816f4e26f160710b6259a88aeeb3ef", "grade": false, "grade_id": "cell-e21df36132dcc29a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Pour aller plus loin ♣: apprentissage profond

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "dbb37f28bfa956280b302df64184c7f3", "grade": false, "grade_id": "cell-bcf62dc4cad097c5", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

En classe, vous avez vu ce qu'est un ***réseau de neurones
artificiel*** et l'***apprentissage profond***. En résumé, il s'agit
de modèles (classificateurs par exemple) dont l'architecture est
articulée en «couches» composées de différentes transformations non
linéaires: des couches de neurones, des convolutions ou d'autres
transformations.

Ces réseaux profonds comptent beaucoup de paramètres (neurones) à
optimiser. Ils nécessitent des infrastructures spéciales pour les
entraîner: de puissantes cartes graphiques (GPU), comme celles
utilisées pour les jeux vidéos, qui permettent de paralléliser les
calculs. Nous ne disposons pas de telles infrastructures sur le
service JupyterHub de l'université.

Nous allons donc utiliser l'***apprentissage par transfert*** (*Transfer Learning*) pour quand même faire du deep dans ce cours.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "31234eb0bd90869a35eac05805279731", "grade": false, "grade_id": "cell-bb4786bfae4ebb44", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### MobileNet et transfert

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e0e3907cd950c7ef84e4f6bdd9ecd7b3", "grade": false, "grade_id": "cell-d51f1d6d3771c9f5", "locked": true, "schema_version": 3, "solution": false, "task": false}}

<div class="alert alert-info" role="alert">

La suite de cette feuille utilise les bibliothèques `tensorflow` et
`keras`. Celles-ci sont installées sur JupyterHub, mais pas forcément
ailleurs (elles sont assez volumineuses).

</div>

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fb98d9a7edaef9407615981f21e362e9", "grade": false, "grade_id": "cell-fea459b200630244", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous allons utiliser un réseau pré-entraîné appelé `MobileNet`, dont
l'architecture a été optimisé pour fonctionner sur les téléphones
portables. Il a été pré-entraîné pour reconnaître mille catégories
différentes (dont des animaux, des objets de la vie courante etc.). Nous n'avons plus qu'à l'entraîner un peu plus pour notre tâche spécifique.

Depuis la librairie `keras`, importons le modèle pré-entraîné sur la
base de donnée `imagenet` :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 499d1b6ab12213622fd75881c8d38d9a
  grade: false
  grade_id: cell-cfffd10728c5eb98
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
import tensorflow as tf
tf.config.run_functions_eagerly(True)

mobilenet = tf.keras.applications.MobileNet(include_top=False, weights='imagenet', input_shape = (32,32,3))
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5ff2240aac49ddb8868dbba4e3abca9f", "grade": false, "grade_id": "cell-a9f0752ceaf7de9c", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Observons l'architecture en couches de ce réseau de neurones; chaque
ligne ci-dessous décrit brièvement l'une des couches successives :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: a84ad2539a6dddc33fad9d18a39a7c6b
  grade: false
  grade_id: cell-23f12beded0c804e
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
mobilenet.summary()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b995463982f2476a5cc16d239a543411", "grade": false, "grade_id": "cell-8c9901655c0067be", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

Combien ce réseau a-t-il de paramètres? Parmi ces paramètres, combien
sont entraînables?



:::

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "618e80b05c4fd25df6c78e5c10505c75", "grade": true, "grade_id": "cell-129248d47e2dc9ab", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

VOTRE RÉPONSE ICI

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fbeb063dab7f90ad1c3cffd0e24d4dbd", "grade": false, "grade_id": "cell-1f90a855d18805c4", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

En déclarant le réseau avec le paramètre `include_top=False`, on a
retiré la dernière couche de neurone. **Le transfert d'apprentissage
va pouvoir être fait en ajoutant des nouvelles couches de neurones
entraînables à la fin de ce réseau pré-entraîné (dont les paramètres
vont être gelés).** Ainsi, on pourra entraîner seulement les dernières
couches de notre réseau sans avoir à réentraîner tout le réseau, ce
qui nécessiterait autrement une puissante carte graphique. En d'autres
termes, le réseau `mobilenet` va nous donner des attributs abstraits
sur lesquels nous allons réentraîner un nouveau réseau de neurones,
plus petit.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6c580d517f57594b7b0893f5c15d954b", "grade": false, "grade_id": "cell-b543a11206b8fbbd", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On commence par geler les poids du réseau `mobilenet` :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 596f7af588ad6f4e8013db0066e714c0
  grade: false
  grade_id: cell-d3bbe8081c0f86f5
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
for layer in mobilenet.layers:
    layer.trainable=False
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f6f4adf756b0f310c62e68e2e7b3f993", "grade": false, "grade_id": "cell-5fa106f4be6594e8", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Vérifiez que tous les paramètres de `mobilenet` sont à présent
non-entraînables :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: fb0684a22e735aa7b1f9cc107ecc8061
  grade: false
  grade_id: cell-39a648cf03608dc1
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
mobilenet.summary()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2f17e9535f6341a7e75dd0b2b88d35e6", "grade": false, "grade_id": "cell-86f7e5aa18f2615a", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

On va à présent ajouter de nouvelles couches entraînables de neurones :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: f9fe09039f2f9dfbbb805e1d1e4908ac
  grade: false
  grade_id: cell-e7e08d5fe1dfeae2
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
from tensorflow import keras
from keras.models import Model
from keras.layers import Dense,GlobalAveragePooling2D

myneuralnet = keras.Sequential(
    [
        mobilenet,
        GlobalAveragePooling2D(),
        Dense(64, activation="relu", name="layer1"),
        Dense(64, activation="relu", name="layer2"),
        Dense(2, activation="softmax",name="layer3"),
    ]
)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bd4a4e77479322256c04be116bd8ccef", "grade": false, "grade_id": "cell-626c5a396790185d", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Configurons le réseau `mobilenet` pour prendre en entrée des images de
taille `(32,32,3)`:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: cf8a715508464d6070d101e7f48a9487
  grade: false
  grade_id: cell-9e1b73d35645f450
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
myneuralnet.build((None,32,32,3))
myneuralnet.summary()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d49087f4832d3cd892dcf1d772f46b4e", "grade": false, "grade_id": "cell-134c13e252ae4e67", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

À présent combien ce réseau a-t-il de paramètres? Parmi ces
paramètres, combien sont entraînables?



:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 95a673a8eb9672bb7904b72fcc799b04
  grade: true
  grade_id: cell-1cf176c276fc231f
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
---
# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ba301411851b8eb0aaef1276aaafaf57", "grade": false, "grade_id": "cell-ab1b74c4452637b4", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Chargeons nos données recentrées et recadrées de taille 32x32 :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: fe183f408aba29c9f7c07c0de4ae9eaa
  grade: false
  grade_id: cell-eab2cf85f5d6540b
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
df_clean = pd.read_csv('clean_data.csv', index_col=0)  # chargement du fichier dans le notebook
df_clean
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6e4a2003026a1e2f397b7acff6a28f74", "grade": false, "grade_id": "cell-5eed3b16767c2609", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

On souhaite avoir une variable `X` de type `np.ndarray` de taille
`(nimages, 32, 32, 3)` c'est à dire `(nombre d'images, largeur, hauteur,
nombre de couches de couleurs)` :

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a7c9779d3691c5a774ca91da2e99374c", "grade": false, "grade_id": "cell-7c2935fe284d9f37", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

Définissez le nombre d'images que vous avez dans nimages. 
::::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: b5d41143805ab6b44c6ec14d3b763ea7
  grade: true
  grade_id: cell-9dd372c7718d0763
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
# VOTRE CODE ICI
raise NotImplementedError()
X = np.array(df_clean.drop(['class'], axis=1)).reshape((nimages, 32, 32, 3))
```

+++ {"editable": true, "slideshow": {"slide_type": ""}, "tags": []}

Il est nécessaire d'encoder les étiquettes sous la forme d'un *one-hot
vector* c'est-à-dire d'un tableau `y_onehot` de taille `(nombre
d'images, nombre de classes)` tel que `y_onehot[i,j]==1` si la i-ème
étiquette est la j-ème classe et `0` sinon. Dans notre cas, la i-ème
ligne vaut `(1,0)` si le i-ème fruit est une pomme, et `(0,1)` si
c'est une banane :

```{code-cell} ipython3
y = np.array(df_clean["class"])
classes = np.unique(y)
class_to_class_number = { cls: number for number, cls in enumerate(classes) }
y_onehot = np.zeros((len(y), len(np.unique(y))))
for i, label in enumerate(y):
    y_onehot[i, class_to_class_number[label]] = 1
```

On doit maintenant définir l'***optimisateur*** et la ***fonction de
coût*** qui vont permettre d'optimiser les paramètres de nos
neurones. Les poids des neurones vont être optimisés pour ***minimiser
la fonction de coût*** (*loss*) :

```{code-cell} ipython3
opt = keras.optimizers.Adam(learning_rate=0.01)
myneuralnet.compile(loss='categorical_crossentropy', metrics=["accuracy"], optimizer=opt)
```

Avant de pouvoir entraîner notre réseau, on va d'abord diviser nos
données en deux: les données d'entraînement et les données de test :

```{code-cell} ipython3
test = np.array(y == 1, dtype = int)
X_train = np.concatenate((X[:165], X[333:333+ 79]), axis = 0)
y_train = np.concatenate((y_onehot[:165], y_onehot[333:333+ 79]), axis = 0)

X_test = np.concatenate((X[165:333], X[333+ 79:]), axis = 0)
y_test = np.concatenate((y_onehot[165:333], y_onehot[333+ 79:]), axis = 0)
```

On peut finalement entraîner notre réseau de neurone !  

**Attention :** Le temps de calcul étant potentiellement élevé, la
cellule ci-dessous est désactivée par défaut. Mettez en commentaire la
première ligne pour lancer le calcul.

```{code-cell} ipython3
%%script echo cellule désactivée

from sklearn.model_selection import StratifiedKFold
import pdb
stop = pdb.set_trace
def create_model():
    myneuralnet = keras.Sequential(
    [
        mobilenet,
        GlobalAveragePooling2D(),
        Dense(64, activation="relu", name="layer1"),
        Dense(64, activation="relu", name="layer2"),
        Dense(2, activation="softmax",name="layer3"),
    ])
    myneuralnet.build((None,32,32,3))
    opt = keras.optimizers.Adam(learning_rate=0.01)
    myneuralnet.compile(loss='categorical_crossentropy', metrics=["accuracy"], optimizer=opt)
    return myneuralnet

def train_evaluate(model, x_train, y_train, x_test, y_test):
    history = model.fit(x_train, y_train, epochs = 10, shuffle = True)
    return model.evaluate(x_test, y_test)

kFold = StratifiedKFold(n_splits=10)
scores = np.zeros(10)
idx = 0
for train, test in kFold.split(X, y):
    model = create_model()
    scores[idx] = train_evaluate(model, X[train], y_onehot[train], X[test], y_onehot[test])[1]
    idx += 1
print(scores)
print(scores.mean())
```

Afficher les valeurs d'accuracy au fur et à mesure des itérations
d'optimisations :

```{code-cell} ipython3
%%script echo cellule désactivée

plt.plot(scores)
plt.xlabel("Nombre d'itération d'optimisations")
plt.ylabel("Accuracy")
```

## Conclusion

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "175abe395c45f2d230bcc2e7396363ac", "grade": true, "grade_id": "cell-48ecfb6975c2fe0b", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

Cette feuille a fait un tour d'horizon d'outils de classification à
votre disposition. Prenez ici quelques notes sur ce que vous avez
appris, observé, interprété.

VOTRE RÉPONSE ICI

+++

Faites maintenant votre propre [analyse](0_analyse.md) et préparez votre [diaporama](0_diaporama.md)!

```{code-cell} ipython3

```
