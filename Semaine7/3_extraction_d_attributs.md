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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4e0e153a44dc5f4793169f37ee7486b8", "grade": false, "grade_id": "cell-cd0cec4179e6c7e1", "locked": true, "schema_version": 3, "solution": false, "task": false}}

# Extraction d'attributs

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "30e91a629323925df1b39131af22aa98", "grade": false, "grade_id": "cell-363b8f6e2af016ab", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Les traitements réalisés dans cette feuille sont majoritairement des
rappels des semaines précédentes. **Le but de cette feuille est de
vous fournir une trame afin d'appliquer sereinement les traitements
vus les semaines précédentes**

La feuille comprends trois parties:
1. Le prétraitement de vos données par extraction d'avant plan,
   recentrage et recadrage (rappels de la semaine 6)
2. L'extraction d'attributs ad-hoc (rappels de la semaine 4)
3. La sélection d'attributs pertinents

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1e98d329a6b9a8e168499aee556e3c3d", "grade": false, "grade_id": "cell-c7ef38442d032da9", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Dans un premier temps, vous exécuterez cette feuille sur le jeu de
données de pommes et de bananes. Puis vous la reprendrez avec votre
propre jeu de données, en visualisant les résultats à chaque étape, et
en ajustant comme nécessaire.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7a99d311f2ca1bda4c60c8ed01ff6176", "grade": false, "grade_id": "cell-76a04ac85061d8e0", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## 1. Prétraitement (rappels de la semaine 6)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d4f48fcf8b1815629cf70dc004773012", "grade": false, "grade_id": "cell-329ade064e61886f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous allons détecter le centre du fruit et recadrer l'image sur ce
centre (comme en Semaine 6). Nous ferons ensuite une sauvegarde
intermédiaire: Enfin nous enregistrerons les images prétraitées dans
un dossier `clean_data`, ainsi qu'une table des pixels dans
`clean_data.csv`.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "38c730e7bf0343fd9b430ff9e09abe89", "grade": false, "grade_id": "cell-08fdab925024f2c8", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Import des bibliothèques

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0726b06d5f3e8b6e37f2f5e806d8f90e", "grade": false, "grade_id": "cell-4645b8bbd98453be", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous commençons par importer les bibliothèques dont nous aurons
besoin. Comme d'habitude, nous vous fournissons quelques utilitaires
dans le fichier `utilities.py`. Vous pouvez ajouter vos propres
fonctions au fur et à mesure du projet:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 9db7a8e5073ed75f46e7a501138cdb11
  grade: false
  grade_id: cell-fbc4ace0d3351477
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
import scipy
from scipy import signal
import pandas as pd
import seaborn as sns
from glob import glob as ls
import sys
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import balanced_accuracy_score as sklearn_metric

from utilities import *
from intro_science_donnees import data
from intro_science_donnees import *
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fc25929b65aeee8b5b8e27d3c71c4bd1", "grade": false, "grade_id": "cell-91732550de16e30f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Pour avoir une première idée de l'impact des prétraitements sur la
classification, nous calculerons au fur et à mesure les performances
d'un classificateur -- ici du plus proche voisin kNN -- et nous les
stockerons dans une table de données `performances`:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: aa8fcb3a3ead9d90b756195010cd9563
  grade: false
  grade_id: cell-6fab593fafd5ac7b
  locked: true
  schema_version: 3
  solution: false
  task: false
---
sklearn_model = KNeighborsClassifier(n_neighbors=3)
performances = pd.DataFrame(columns = ['Traitement', 'perf_tr', 'std_tr', 'perf_te', 'std_te'])
performances
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e7a0d62653b7330e42cd30b4629af313", "grade": false, "grade_id": "cell-0b51395eaa6045fa", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Import des données

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4a4ca36d53b1acd9e4eff1d407489d1d", "grade": false, "grade_id": "cell-1dfc81a33d46608e", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

En mettant en commentaire la ligne 2 ou la ligne 1, vous choisirez
ici sur quel jeu de données le prétraitement s'applique: d'abord les
pommes et les bananes, puis le vôtre.

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 531fda9b452c22cc5eee6f40b6c6ee4a
  grade: false
  grade_id: cell-3bcd390fb338683b
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
dataset_dir = 'data'
images_a = load_images(dataset_dir, f"a*.{'jpeg'}")
images_b = load_images(dataset_dir, f"b*.{'jpeg'}")
images = pd.concat([images_a, images_b])

def resize_image(img):
    return img.resize((100, 100))

images_resized = images.apply(resize_image)

lst_effected = images_resized.iloc[:10].apply(lambda img: crop_image(img, (30, 20, 70, 60)))
lst_healthy = images_resized.iloc[10:].apply(lambda img: crop_image(img, (30, 20, 70, 60)))

images_cropped = pd.concat([lst_effected, lst_healthy])
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
---
image_grid(images_cropped, titles=images.index)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "81011707ccca466dd63894092cc5856b", "grade": false, "grade_id": "cell-7ed92f653dde82fb", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Calculons les performances de notre classificateur en l'appliquant
directement à la représentation en pixels des images :

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 83fcf497df2469a8e7552fb8ef5beea1
  grade: false
  grade_id: cell-d553b100d1f168af
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
df_raw = images_cropped.apply(image_to_series)
df_raw['class'] = df_raw.index.map(lambda name: 1 if name[0] == 'a' else -1)
df_raw
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7e1eb4b73bd1235ebb4386859c6556b3", "grade": false, "grade_id": "cell-7ca7d8dfc8f5cff4", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Calculez la validation croisée en appliquant `df_cross_validate` à la
table `df_raw` en nommant les performances `p_tr` et `p_te` ainsi que
les écart-types `s_tr` et `s_te`, pour les ensembles d'entrainement et
de test respectivement. La métrique de performance a été définie lors
de l'import des librairies et se nomme `sklearn_metric`.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 9f8d0e2ebd6c1ebaccb9f8c83ab78b9e
  grade: false
  grade_id: cell-7d957fe865ef838e
  locked: false
  schema_version: 3
  solution: true
  task: false
---
p_tr, s_tr, p_te, s_te = df_cross_validate(df_raw, sklearn_model, sklearn_metric)
metric_name = sklearn_metric.__name__.upper()
print("AVERAGE TRAINING {0:s} +- STD: {1:.2f} +- {2:.2f}".format(metric_name, p_tr, s_tr))
print("AVERAGE TEST {0:s} +- STD: {1:.2f} +- {2:.2f}".format(metric_name, p_te, s_te))
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e1e2f1d056a19fb31be1c14a2c47ac4a", "grade": false, "grade_id": "cell-30f0e7d71c3bbb4d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Ajoutons ces résultats à notre table `performances` :

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 47ef4ec6938b1fbbef7f1cfc8a338499
  grade: false
  grade_id: cell-efbf187ec4de943f
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
performances.loc[0] = ["Images brutes", p_tr, s_tr, p_te, s_te]
performances.style.format(precision=2).background_gradient(cmap='Blues')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e3926fde21a9337c461af615be68d081", "grade": false, "grade_id": "cell-71f7a30f09a3597f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Extraction de l'avant-plan

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "797dd793d521eefe7aed274bc8873a2a", "grade": false, "grade_id": "cell-ed4a0600c5d07d01", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Pour trouver le centre du fruit, il faut déjà arriver à séparer les
pixels qui appartiennent au fruit de ceux qui appartiennent au
fond. Souvenez-vous, vous avez déjà fait cela en Semaine 6 avec la
fonction `foreground_filter`.

Dans l'exemple suivant, on utilise une variante
`foreground_redness_filter` qui sépare le fruit du fond en prenant en
compte la rougeur de l'objet et pas uniquement les valeurs de
luminosité.


:::{attention}

Comme pour `foreground_filter`, cette fonction a besoin d'un seuil
(compris entre 0 et 1) sur les valeurs des pixels à partir duquel on
décide s'il s'agit du fruit ou du fond. Avec les pommes et les
bananes, on se contentera de la valeur 2/3. Avec vos données, faites
varier cette valeur de seuil pour trouver la valeur qui semble la plus
adéquate.

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 6036833ade941ff736a3eb20cdc1c968
  grade: false
  grade_id: cell-1c9213f9f451e657
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
foreground_imgs1 = [foreground_redness_filter(img, theta=.25)
            for img in images_cropped]

image_grid(foreground_imgs1)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ee4dd2acd95084dc1fa40a42ca9ac228", "grade": false, "grade_id": "cell-0ec125a40745d032", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On peut voir que selon s'il s'agit d'objets sombres sur fond clair ou
d'objets clairs sur fond sombre, on n'obtient pas les mêmes valeurs
booléenne en sortie de `foreground_filter`. La fonction
`invert_if_light_background` inverse simplement les valeurs booléennes
si une majorité de `True` est détectée. Voilà le résultat.

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: fd93f157bac99a49b05f0d27d73d8af1
  grade: false
  grade_id: cell-68d213f1b8dde05d
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
foreground_imgs2 = [invert_if_light_background(foreground_redness_filter(img, theta=.25))
            for img in images_cropped]
image_grid(foreground_imgs2)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8daa19401c5e9ab20a79ca5dea758a2b", "grade": false, "grade_id": "cell-1a0bd73b2eb64491", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

C'est légèrement mieux mais les images restent très bruitées; on
choisit d'appliquer un filtre afin de réduire les pixels isolés. C'est
ce qu'on fait avec la fonction `scipy.ndimage.gaussian_filter()`.

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 3df6dbd2ef4e88d23330037162d0aade
  grade: false
  grade_id: cell-a7e311f99c04d100
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
foreground_imgs3 = [scipy.ndimage.gaussian_filter(
              invert_if_light_background(
                  foreground_redness_filter(img, theta=.25)),
              sigma=.2)
            for img in images_cropped]
image_grid(foreground_imgs3)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "882cb6e5f9e6ec877e54ea17f1dd749f", "grade": false, "grade_id": "cell-edcd1412e8780f7d", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Les traitements précédents résultent d'un certain nombre de choix
faits au fil de l'eau (seuil, filtre par rougeur, débruitage).

:::{admonition} Exercice

Définissez ci-dessous la fonction `my_foreground_filter` qui prend en
entrée une image et:
1. lui applique `foreground_redness_filter` 
2. inverse les valeurs booléennes si le fond est blanc avec la
   fonction `invert_if_light_background`
3. applique le filtre gaussien et supprime les pixels isolés avec un
   sigma à 0.2 <a name="choix_extraction"></a>

Cette fonction extrait donc l'objet de l'arrière-plan

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: b50d25ea788ea72cd35df29e44ae181f
  grade: false
  grade_id: cell-388f0e8b70d29570
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
def my_foreground_filter(image):
    # Appliquer le filtre de rougeur de premier plan
    foreground_mask = foreground_redness_filter(image)
    
    # Inverser les valeurs si le fond est blanc
    foreground_mask = invert_if_light_background(foreground_mask)
    
    # Appliquer le filtre gaussien avec un sigma de 0.2
    image_filtered = scipy.ndimage.gaussian_filter(image, sigma=0.2)
    
    
    return image_filtered
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "376de7ab06ef71f47d4575cf5a9d639f", "grade": false, "grade_id": "cell-ab925e70b4d327ad", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Cette fonction fait partie intégrale de la **narration des
traitements** que nous menons dans cette feuille. C'est pour cela que
nous la définissons directement dans cette feuille, et non dans
`utilities.py` comme on l'aurait fait pour du code réutilisable.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b2e7e9c175cc2c14cd971a1a13e8bf3a", "grade": false, "grade_id": "cell-3f74f24b54525ea2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Détection du centre du fruit

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8bc501ec45278c640bb446f7a2adfbed", "grade": false, "grade_id": "cell-7ccd60ee0acbc858", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous allons à présent déterminer la position du centre du fruit, en
prenant la moyenne des coordonnées des pixels de l'avant plan.

Faisons cela sur la première image:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 35b9952ce12e44f194a247022ecc3fa9
  grade: false
  grade_id: cell-688d32bef4b64ef2
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
img = images_cropped.iloc[0]
img
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a3339f8f7ede35fa4ca828e8c677cb19", "grade": false, "grade_id": "cell-71d4072d46cfa6cd", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Calculez l'avant plan de l'image dans`foreground` avec la fonction
`my_foreground_filter` que vous venez de créer. 

On extrait ensuite les coordonnées de ses pixels :

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 33a7087886e2222cdcf0ea8d1aef10f7
  grade: false
  grade_id: cell-456706f2053e3a68
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
foreground = my_foreground_filter(img)
coordinates = np.argwhere(foreground)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1e5a4835f1e426a8576eeb9b51466a47", "grade": false, "grade_id": "cell-2fafad09bd25eea7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

que l'on affiche comme un nuage de points :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: c84f889586fad16d7168e0a777f06cf2
  grade: false
  grade_id: cell-91d0510e1a875614
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
plt.scatter(coordinates[:,1], -coordinates[:,0], marker="x");
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0a052f8b4a95c0667a26f30a8fc3cc90", "grade": false, "grade_id": "cell-1f208b3395f73b47", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

Calculez les coordonnées du barycentre des pixels de l'avant plan --
c'est-à-dire la moyenne des coordonnées sur les X et les Y -- afin
d'estimer les coordonnées du centre du fruit. On garde le résultat
dans `center`. Pour rappel, vous avez déjà calculé cela en Semaine 6.

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 109c9e40583d4102208a8f672b4bfaa9
  grade: false
  grade_id: cell-1b73566df4dc76d3
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
foreground_pixels = np.where(foreground)
center = (np.mean(foreground_pixels[1]), np.mean(foreground_pixels[0]))
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: b54b887bb8f8e33cc10ca3b9614556da
  grade: false
  grade_id: cell-c4d67ad00158fe1e
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
plt.scatter(coordinates[:,1], -coordinates[:,0], marker="x");
plt.scatter(center[0], -center[1], 300, c='r', marker='+',linewidth=5);
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "c8dfe80ddbb3909b7c19efc4fbe40aff", "grade": false, "grade_id": "cell-f279a67a6adb0a13", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Ce n'est pas parfait: du fait des groupes de pixels à droite qui ont
été détectées comme de l'avant plan, le centre calculé est plus à
droite que souhaité. Mais cela reste un bon début.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "675bd5d08aab92812118e642faee66eb", "grade": false, "grade_id": "cell-b44c46cf2c257a9b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Recadrage

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9cb3a6eea3d10014dc68bf1fbf0ea2e6", "grade": false, "grade_id": "cell-73b745f379708a66", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Maintenant que nous avons (approximativement) détecté le centre du
fruit, il nous suffit de recadrer autour de ce centre. Une fonction
`crop_around_center` est fournie pour cela. Comparons le résultat de
cette fonction par rapport à `crop_image` utilisé en [feuille2](2_premiere_analyse_ACP.md) :

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: a1561781c018d076418a35ada53b637d
  grade: false
  grade_id: cell-4044e1d8ca3d20b6
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
crop_image(img, (0, 0, 40, 40))
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7664eafed7feed347c6f29c47459b499", "grade": false, "grade_id": "cell-6a73f050a21dd317", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

**Exercice :** Finissez d'écrire la fonction `crop_around_center`. Il ne manque que les coordonnées à droite (right) et en bas (bottom).

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: eebc19814314dd4123bdcc38e96aeb9c
  grade: false
  grade_id: cell-5ad18b7f58bfacc9
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
crop_around_center(img, center)
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
---
plt.imshow(crop_around_center(img, center))
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "72142c7da0bbb12ce0c416a65d6b8221", "grade": false, "grade_id": "cell-3e34f81c400abb8c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On constate que le recadrage sur le fruit est amélioré, même si pas
encore parfait.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "594673c7c1fee6a4d04f77e4eb8fd414", "grade": false, "grade_id": "cell-d56b644d2b458540", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Récapitulatif du prétraitement

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fb26eaea60feac92b40943ac8e8ee3b8", "grade": false, "grade_id": "cell-1c80da3d9ef180d1", "locked": true, "schema_version": 3, "solution": false, "task": false}}

À nouveau, nous centralisons tous les choix faits au fil de l'eau en
une unique fonction effectuant le prétraitement<a
name="choix_pretraitement"></a>. Cela facilite l'application de ce
traitement à toute image et permet de documenter les choix faits :

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: f4c1d3cf6fa19b9b2538571fbfd83e53
  grade: false
  grade_id: cell-a031ad0180c19815
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
def my_preprocessing(img):
    """
    Prétraitement d'une image
    
    - Calcul de l'avant plan
    - Mise en transparence du fond
    - Calcul du centre
    - Recadrage autour du centre
    """
    foreground = my_foreground_filter(img)
    coordinates = np.argwhere(foreground)
    foreground_pixels = np.where(foreground)
    center = (np.mean(foreground_pixels[1]), np.mean(foreground_pixels[0]))
    crop_image(img, (0, 0, 40, 40))
    img = crop_around_center(img, center)
    return img
```

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: d47edb6af8253419dfb0e2665627cd48
  grade: false
  grade_id: cell-9073d5973279ee91
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
plt.imshow(my_preprocessing(img));
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ea788113ceeffc653bb0995fc9e6ff23", "grade": false, "grade_id": "cell-684d382ecf73fbd4", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

Appliquez le prétraitement à toutes les images que vous mettrez dans `clean_images`.

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 16e2c4434177cac64f4f1c29e8c0f504
  grade: false
  grade_id: cell-e6ba50c596ac4cb7
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
clean_images = images_cropped.apply(my_preprocessing)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: c8756c133dcc20fd0733b97b05db8be8
  grade: false
  grade_id: cell-072b37a051ad21b8
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
image_grid(clean_images)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "c64d321fc2d7e6171a7a11613fb38690", "grade": false, "grade_id": "cell-3e5e9bcb1156db08", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

### Performance de la classification après prétraitement

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "66fcbd8e0aec3e466e1616631a2f9c4b", "grade": false, "grade_id": "cell-6fa96d5702dbfa14", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Convertissons maintenant les images prétraitées dans leurs
représentations en pixels, regroupées dans une table:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 8cf6e4be69dcb67a37a57a0bbf3023f8
  grade: false
  grade_id: cell-74c3e74f13e65f6b
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
# conversion
df_clean = clean_images.apply(image_to_series)
# ajout des étiquettes
df_clean['class'] = df_clean.index.map(lambda name: 1 if name[0] == 'a' else -1)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4c489558582376fb94a5b044cc11c321", "grade": false, "grade_id": "cell-0c354611f4a4a20f", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

:::{admonition} Exercice

À l'aide de la fonction `df_cross_validate`, calculez les performance
du classificateur sur les images prétraitées.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: bd09f3344731521b48ee72b821a96290
  grade: false
  grade_id: cell-1991dee7ba243e14
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
p_tr, s_tr, p_te, s_te = df_cross_validate(df_clean, sklearn_model, sklearn_metric)
metric_name = sklearn_metric.__name__.upper()
print("AVERAGE TRAINING {0:s} +- STD: {1:.2f} +- {2:.2f}".format(metric_name, p_tr, s_tr))
print("AVERAGE TEST {0:s} +- STD: {1:.2f} +- {2:.2f}".format(metric_name, p_te, s_te))
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1f97bec6c6716ed18b756866de5b7fc9", "grade": false, "grade_id": "cell-8d5a1c7e25940bee", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Ajoutez ces résultats à la table `performances`.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 2bc50d7c06baefa796a348b771e3f350
  grade: false
  grade_id: cell-c021c8286c45a400
  locked: false
  schema_version: 3
  solution: true
  task: false
---
performances.loc[1] = ["Images prétraitées", p_tr, s_tr, p_te, s_te]
performances.style.format(precision=2).background_gradient(cmap='Blues')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e6822c094fe0641ed5bce87a5ea3b607", "grade": false, "grade_id": "cell-f7d03b3fc781b97a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Sauvegarde intermédiaire

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "dabae3f947381b36b45a76d17421f00c", "grade": false, "grade_id": "cell-db2821b8e4311df0", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous sauvegardons maintenant les images prétraitées dans le répertoire
`clean_data` au format `PNG` :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 2dcc9e7946e5448680eaeb42a733984a
  grade: false
  grade_id: cell-bff603f0c67536ee
  locked: true
  schema_version: 3
  solution: false
  task: false
---
os.makedirs('clean_data', exist_ok=True)
for name, img in clean_images.items():
    img.save(os.path.join('clean_data', os.path.splitext(name)[0]+".png"))
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7373d179996db56f34c3c21c2d3da840", "grade": false, "grade_id": "cell-a3a9fe4bdfe6d657", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Explication
:class: hint

`splitext` sépare un nom de fichier de son extension :

:::

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: a475d6bc3b31a429a5324fc4622e36cd
  grade: false
  grade_id: cell-6f60c622fcabfa42
  locked: true
  schema_version: 3
  solution: false
  task: false
---
os.path.splitext("machin.jpeg")
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "99cda8dd3139332f7178fb1cab778bf0", "grade": false, "grade_id": "cell-819eeb3105af988b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous sauvegardons la table de données dans un fichier `clean_data.csv` :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 056538ec0277ce91793beae4a6ed53c5
  grade: false
  grade_id: cell-8414b0591c1ec961
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df_clean.to_csv('clean_data.csv')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "478fb7c8febef71e07adfe7c4b312731", "grade": false, "grade_id": "cell-43540e550e722346", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Ainsi il sera possible de travailler sur la suite de cette feuille et
les feuilles ultérieures sans avoir besoin de refaire le
prétraitement :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 6778836eba10769e18d6676940830d82
  grade: false
  grade_id: cell-58699d169f3ec5ea
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df_clean = pd.read_csv('clean_data.csv', index_col=0)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "009c6b03b651da32e6ff30a503d4d11f", "grade": false, "grade_id": "cell-d241acc2b2ed27f7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Extraction des attributs (rappels de la semaine 4)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fda2454d11d4112ce384ebc28dc153a3", "grade": false, "grade_id": "cell-3114446f2f5ae708", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Durant les semaines précédentes, vous avez déjà implémenté des
attributs tels que :
- La rougeur (*redness*) et l'élongation durant la semaine 4;
- D'autres attributs (adhoc, pattern matching, PCA, etc.) durant le
  premier projet.

L'idée de cette section est de réappliquer ces attributs sur vos
nouvelles données.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b837b5a30e743e46197d299a5491c496", "grade": false, "grade_id": "cell-8658d6e5b24407f1", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Filtres

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8eb49779550fce2e489a45efd16260c4", "grade": false, "grade_id": "cell-ed19444303560eac", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Récapitulons les types de filtres que nous avons en magasin:

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a31f5603e9f34b5e7c0372b9620d4269", "grade": false, "grade_id": "cell-e32ece543b8553b8", "locked": true, "schema_version": 3, "solution": false, "task": false}}

#### La rougeur (redness)

Il s'agit d'un filtre de couleur qui extrait la différence entre la
couche rouge et la couche verte (R-G). Lors de la Semaine 2, nous
avons fait la moyenne de ce filtre sur les fruits pour obtenir un
attribut (valeur unique par image). Ici, affichons simplement la
différence `R-G` :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 56763238cf676a330c25b76485d635f9
  grade: false
  grade_id: cell-c3b13a4e3c38e9e7
  locked: true
  schema_version: 3
  solution: false
  task: false
---
image_grid([redness_filter(img)
            for img in clean_images])
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e13fb84ab64ee1bfbed0c8e878ce0a7e", "grade": true, "grade_id": "cell-2ba20f803e981265", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

:::{admonition} Exercice

À quelles couleurs correspondent les zones claires resp. sombres?
Pourquoi le fond n'apparaît-il pas toujours avec la même clarté?

VOTRE RÉPONSE ICI

:::

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b45a7b66bebf5249b0188c385c6c7d03", "grade": false, "grade_id": "cell-c285f4ed7c06c6fb", "locked": true, "schema_version": 3, "solution": false, "task": false}}

#### Variante de la rougeur

Il s'agit d'un filtre de couleur qui extrait la rougeur de chaque
pixel calculée avec $R-(G+B)/2$ :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 83d4cf5f89225ae6d5f563e08014b428
  grade: false
  grade_id: cell-878582633eda952d
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
image_grid([difference_filter(img)
            for img in clean_images])
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4623548f6dc451a2facc4636bd357552", "grade": false, "grade_id": "cell-e60d97b83d7a3fb5", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Pour d'autres idées de mesures sur les couleurs, consulter [cette page
wikipédia](https://en.wikipedia.org/wiki/HSL_and_HSV).

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b4cd104e72053c89ff4903059a057e4e", "grade": false, "grade_id": "cell-743271b9cf06d0e1", "locked": true, "schema_version": 3, "solution": false, "task": false}}

#### Seuillage

+++ {"deletable": false, "editable": true, "nbgrader": {"cell_type": "markdown", "checksum": "5c92cd9e375f0960e7c0ba0343cf1314", "grade": false, "grade_id": "cell-caf1f18c7fe5f505", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

Souvenez vous que vous pouvez également seuiller les valeurs des
pixels (par couleur ou bien par luminosité). C'est ce que l'on fait
dans les fonctions `foreground_filter` ou `foreground_color_filter`.

:::{admonition} Indication
:class: hint

N'oubliez pas de convertir les images en tableau `numpy` pour
appliquer les opérateurs binaires `<`, `>`, `==`, etc.

:::

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 21ad23af4c65c78983f723e50cbbb9d1
  grade: false
  grade_id: cell-6774ff1e2a9696bb
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
noirblanc=([np.mean(np.array(img), axis = 2) < 100 
            for img in clean_images])

#noirblanccropped = noirblanc.apply(crop(

def ennoir(array):
    for i in range(len(array)):
        for j in range(0,5):
            array[i][j]=False
        for j in range(len(array)-5,len(array)):
            array[i][j]=False
        if i>=27 or i<=4:
            array[i]=[False]*len(array)
    return array


    
arrayennoir0= [ennoir(x) for x in noirblanc] 
arrayennoir1 = [ennoir(x) for x in foreground_imgs1] 
arrayennoir2 = [ennoir(x) for x in foreground_imgs2] 
arrayennoir3 = [ennoir(x) for x in foreground_imgs3] 

image_grid(arrayennoir0)
#noirblanc[12]
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
---
noirblanc[12][0]
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
---
image_grid(noirblanc)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "52a984e5f0ce91d72dfc9a49c086d297", "grade": false, "grade_id": "cell-17090d1991f77f23", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

#### Contours

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "32e9a7f2e5f87ce68e1e8fff1cab5612", "grade": false, "grade_id": "cell-2ee4d4b6672cbfff", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Pour extraire les contours d'une image (préalablement seuillée), on
doit soustraire l'image seuillée avec elle même en la décalant d'un
pixel vers le haut (resp. à droite). On fourni cette extraction de
contours avec la fonction `contours` :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 8b7cf2f62226479a4f77c8007cef5369
  grade: false
  grade_id: cell-102b63a88cde7374
  locked: true
  schema_version: 3
  solution: false
  task: false
---
image_grid([contours(np.mean(np.array(img), axis = 2) < 100 ) 
            for img in clean_images])
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "13579e20c6b172c1b792ced203613da9", "grade": false, "grade_id": "cell-ff6e22bb84fc2e5f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Création d'attributs à partir des filtres

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5a48de0bdf1eeb4e9991a5fbcc2ad497", "grade": false, "grade_id": "cell-2d2198862d185cd5", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Maintenant que nous avons récapitulé les filtres en notre possession,
nous allons calculer un large ensemble d'attributs sur nos images. Une
fois cet ensemble recueilli, nous allons ensuite sélectionner
uniquement les attributs les plus pertinents.

On se propose d'utiliser trois attributs sur les couleurs:

1. `redness` : moyenne de la différence des couches rouges et vertes
   (R-G), en enlevant le fond avec `foreground_color_filter`;
2. `greenness` : La même chose avec les couches (G-B);
3. `blueness` : La même chose avec les couches (B-R).

Ainsi que trois autres attributs sur la forme:

4. `elongation` : différence de variance selon les axes principaux des
   pixels du fruits (cf Semaine2);
5. `perimeter` : nombre de pixels extraits du contour;
6. `surface` : nombre de pixels `True` après avoir extrait la forme.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f33b4ac3054e042372070425bb0c8dce", "grade": false, "grade_id": "cell-47f4de897fca2092", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

::::{admonition} Exercice

Créez la table `df_features` qui contient ces six paramètres ainsi que
les attributs que vous avez implémenté dans le projet précédent.

:::{admonition} Indications
:class: hint

Dans le Projet 1, nous avions défini la table ainsi:

:::

::::

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
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

"""filtre1 = MatchedFilter(arrayennoir0)
filtre_zero1 = MatchedFilter(arrayennoir0[:10]) 
filtre_un1 = MatchedFilter(arrayennoir0[10:])
display(filtre1.show())

print("MATCH ZERO OU UN \nPour un 0 :", filtre_zero1.match(arrayennoir0[19]))
print("Pour un 1 :" , filtre_un1.match(arrayennoir0[19]))

filtre_zero_images1 = [filtre_zero1.match(arrayennoir0[i]) for i in range(20)]
filtre_un_images1 = [filtre_un1.match(arrayennoir0[i]) for i in range(20)]
for i in range(20):
    print(f"{i} : {filtre_zero_images1[i]}  {filtre_un_images1[i]}")"""
```

```{code-cell} ipython3
def average_pixel_value(image):
    # Calculer la moyenne des valeurs des pixels
    avg_value = np.mean(image)
    return avg_value
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
---
images_traitees = [np.mean(np.array(img), axis = 2) < 100 
            for img in clean_images]
avg_pixel_value = [average_pixel_value(arrayennoir0[i]) for i in range(20)]
print("La moyenne des valeurs des pixels pour chaque image :")
print(avg_pixel_value)
```

```{code-cell} ipython3
import pandas as pd

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
```

```{code-cell} ipython3
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
from sklearn.linear_model import Perceptron

model_name = ["Nearest Neighbors", "Parzen Windows",  "Linear SVM", "RBF SVM", "Gaussian Process",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA","Perceptron","Commitee"]
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
    QuadraticDiscriminantAnalysis(),
    Perceptron(tol=1e-3, random_state=36, shuffle=True, max_iter=100),
    ClassifierCommittee(model_list)]

from sklearn.metrics import balanced_accuracy_score as sklearn_metric
compar_results = systematic_model_experiment(series, model_name, model_list, sklearn_metric)
compar_results.style.format(precision=2).background_gradient(cmap='Blues')

compar_results

compar_results[['perf_tr', 'perf_te']].plot.bar()
plt.ylim(0.5, 1)
```

```{code-cell} ipython3
compar_results
```

```{code-cell} ipython3
tebad = compar_results.perf_te < compar_results.perf_te.median()
tebad
```

```{code-cell} ipython3
trbad = compar_results.perf_tr < compar_results.perf_tr.median()
trbad
```

```{code-cell} ipython3
overfitted = tebad & ~trbad
overfitted
```

```{code-cell} ipython3
underfitted = trbad & ~tebad
underfitted
```

```{code-cell} ipython3
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

commitee = ClassifierCommittee(model_list)
```

```{code-cell} ipython3

```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
---
"""df = pd.read_csv("../Semaine3/attributs.csv", index_col=0)
df
# standardisation
dfstd =  (df - df.mean()) / df.std()
dfstd['class'] = df['class']
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

from sklearn.linear_model import Perceptron
# définition du modèle de classificateur
classifier = Perceptron(tol=1e-3, random_state=36, shuffle=True, max_iter=100)
# on l'ajuste aux données d'entrainement

classifier.fit(Xtrain, Ytrain)

# on calcule ensuite le taux d'erreur lors de l'entrainement et pour le test

Ytrain_predicted = classifier.predict(Xtrain)
Ytest_predicted = classifier.predict(Xtest)

# on calcule les taux d'erreurs

e_tr = error_rate(Ytrain, Ytrain_predicted)
e_te = error_rate(Ytest, Ytest_predicted)

print("Classificateur: Perceptron")
print("Training error:", e_tr)
print("Test error:", e_te)"""
```

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 526c711a2c5da53529c85f6344c746c0
  grade: false
  grade_id: cell-bed895de20c6450b
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: []
---
df = pd.DataFrame({
        'redness':    img.apply(redness),
        'elongation': img.apply(elongation),
        'class':      img.index.map(lambda name: 1 if name[0] == 'a' else -1),
})
df
```

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 36e8fc419e3c057c1872f0066de8ed0e
  grade: false
  grade_id: cell-e185754c43dc2d17
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
df_features
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "cd839ff972db0169f1ffedbde7e591b7", "grade": false, "grade_id": "cell-dea972a044f9aaa7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Les amplitudes des valeurs sont très différentes. Il faut donc
normaliser ce tableau de données (rappel de la semaine 3 et du projet
1) afin que les moyennes des colonnes soient égales à 0 et les
déviations standard des colonnes soient égales à 1.

***Rappel:*** notez l'utilisation d'une toute petite valeur epsilon
pour éviter une division par 0 au cas où une colonne soit constante :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 91d97d3151da81e4d7c41a4122523a3f
  grade: false
  grade_id: cell-674aab215fb89b4d
  locked: true
  schema_version: 3
  solution: false
  task: false
---
epsilon = sys.float_info.epsilon
df_features = (df_features - df_features.mean())/(df_features.std() + epsilon) # normalisation 
df_features.describe() # nouvelles statistiques de notre jeu de donnée
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "127a2ce11f3bbace08b37987614d51bf", "grade": false, "grade_id": "cell-53b4be052dea2ca4", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On ajoute nos étiquettes (1 pour les pommes, -1 pour les bananes) dans
la dernière colonne :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 61384399b82cc079b48f2040c381944d
  grade: false
  grade_id: cell-98e267993504172d
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df_features["class"] = df_clean["class"]
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0f3f21cb3651113e2d643831bae8afcc", "grade": false, "grade_id": "cell-c3c83a907ce1aa73", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Et on remplace les NA par des 0, par défaut:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 4a0509d9fd42ca3373ab797d062f5fa5
  grade: false
  grade_id: cell-cc9c6b17fd135446
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df_features[df_features.isna()] = 0
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 049476ba4fc37a04c96f37b5e847d35c
  grade: false
  grade_id: cell-f2756c09cdbe187c
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df_features.style.background_gradient(cmap='coolwarm')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "48a008562474d5e84912493f4f4b944c", "grade": false, "grade_id": "cell-f2182f636dd00352", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Calculer les performances de notre classificateur sur les attributs et
ajouter les à notre table `performances` :

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: ef2c0404f4ab884e45c1b089b3ecacd3
  grade: false
  grade_id: cell-c478d620f43d863f
  locked: false
  schema_version: 3
  solution: true
  task: false
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
  checksum: 9266a0fe4e0fdfd7fd25672ff1eaeaad
  grade: false
  grade_id: cell-e6dd889619f98afc
  locked: true
  schema_version: 3
  solution: false
  task: false
---
performances.style.format(precision=2).background_gradient(cmap='Blues')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "c2d817e3f785737ee442eeb348fee989", "grade": false, "grade_id": "cell-4d940c8d994be5a3", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Sélection des attributs (**nouveau!**)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "65ea456bd9b7fc067fbbad15649d175a", "grade": false, "grade_id": "cell-64b949f4d23c2eb0", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Maintenant que nous avons extrait un ensemble d'attributs, nous
souhaitons analyser lesquels améliorent le plus les performances de
notre classificateur. Pour cela, nous tenterons deux approches :

- **Analyse de variance univariée** : On considère que les attributs
  qui, pris individuellement, corrèlent le plus avec nos étiquettes
  amélioreront le plus la performance une fois groupés.
- **Analyse de variance multi-variée** : On considère qu'il existe un
  sous-ensemble d'attributs permettant d'améliorer davantage les
  performances que les attributs étudiés séparément.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0882c7254b14069b0cf35cb9a2ab7724", "grade": false, "grade_id": "cell-84a65b446afad5f2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Analyse de variance univariée

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "333823e5cfcc749299a829f52075b641", "grade": false, "grade_id": "cell-c03bea43c3f668f2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Dans cette approche, on commence par calculer les corrélations de
chacun de nos attributs avec les étiquettes :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 51853c2fc00736755150720c4f6b016e
  grade: false
  grade_id: cell-851a22de4ae157ac
  locked: true
  schema_version: 3
  solution: false
  task: false
---
# Compute correlation matrix
corr = df_features.corr()
corr.style.format(precision=2).background_gradient(cmap='coolwarm')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a8f68621f759f4f41ddaf8635f59396e", "grade": false, "grade_id": "cell-5528d4e1f55152fa", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Pour les pommes et les bananes, seule la "redness" resp. l'"elongation"
a une légère correlation resp. anti-corrélation avec les
étiquettes. Nous allons rajouter de nouveaux attributs sur les
couleurs afin d'identifier s'il y aurait un attribut qui corrélerait
davantage avec les étiquettes.

**NB**: On en profite pour renormaliser en même temps que l'on ajoute
des attributs.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ca3c385819fd13bd8aaa69302bf0e267", "grade": false, "grade_id": "cell-d42fac6b12b6720a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On utilise la fonction `get_colors()` donnée dans utilities

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: a677013657ec89571a4798d27eed3f86
  grade: false
  grade_id: cell-8131a375f984abbc
  locked: true
  schema_version: 3
  solution: false
  task: false
---
show_source(get_colors)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b26552d33812061aa8c7457a37aca236", "grade": false, "grade_id": "cell-efb894fcbb34e174", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Appliquez `get_colors()` à vos images `clean_images`.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: bf27eb0e141693e3c639ec8bcb3f1200
  grade: false
  grade_id: cell-5bd09201a8b4bd74
  locked: false
  schema_version: 3
  solution: true
  task: false
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
  checksum: ba3cad4c3ed0c94a8d4f8386d74aca2d
  grade: false
  grade_id: cell-3736a9656686bc4f
  locked: true
  schema_version: 3
  solution: false
  task: false
---
s = df_features.iloc[3].replace({'redness': 4})
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 9a507b882df64ca15aefbd4702f439e7
  grade: false
  grade_id: cell-e8a77493164c858a
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df_features
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 0b48bf24ada3c5126f97994215445745
  grade: false
  grade_id: cell-7a8d945a628ee001
  locked: true
  schema_version: 3
  solution: false
  task: false
---
header = ['R','G','B','M=maxRGB', 'm=minRGB', 'C=M-m', 'R-(G+B)/2', 'G-B', 'G-(R+B)/2', 'B-R', 'B-(G+R)/2', 'R-G', '(G-B)/C', '(B-R)/C', '(R-G)/C', '(R+G+B)/3', 'C/V']

df_features_large = df_features.drop("class", axis = 1)

df_features_large = pd.concat([df_features_large, clean_images.apply(get_colors)], axis=1)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7b6b8939d6c04cbe3e719f31e9400b2e", "grade": false, "grade_id": "cell-982683b31329f838", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Normalisez `df_features_large`. On utilisera un epsilon au cas où certaines valeurs de std() soit nulles.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 99198800e4b309b146e0fc786b603514
  grade: false
  grade_id: cell-63a6570df5a2cfe2
  locked: false
  schema_version: 3
  solution: true
  task: false
---
# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3df374293ee9526a20ff99fc0c0c7e15", "grade": false, "grade_id": "cell-ab6144ffbb8ba5a6", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Remplacez les valeurs de NA par des 0 puis rajouter les étiquettes (1
pour les pommes, -1 pour les bananes) dans la dernière colonne (sans
normalisation!)

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 2bb7ff623b6fb2dc250b9ec410a04093
  grade: false
  grade_id: cell-5cf962af903dc619
  locked: false
  schema_version: 3
  solution: true
  task: false
---
# VOTRE CODE ICI
raise NotImplementedError()

df_features_large
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8e7461339f2be6b37214611c78e6434c", "grade": false, "grade_id": "cell-01264880bfe0fb0c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On vérifie les performances de notre classificateur sur ce large
ensemble d'attributs et on les ajoute à notre table `performances` :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: fe03ed6100d7b5645ffd2bd3ba6e9fe9
  grade: false
  grade_id: cell-02093f583ba285cf
  locked: true
  schema_version: 3
  solution: false
  task: false
---
# Validation croisée (LENT)
p_tr, s_tr, p_te, s_te = df_cross_validate(df_features_large, sklearn_model, sklearn_metric)
metric_name = sklearn_metric.__name__.upper()
print("AVERAGE TRAINING {0:s} +- STD: {1:.2f} +- {2:.2f}".format(metric_name, p_tr, s_tr))
print("AVERAGE TEST {0:s} +- STD: {1:.2f} +- {2:.2f}".format(metric_name, p_te, s_te))
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 4c9f60bb1967ee68017fa74f55bec01d
  grade: false
  grade_id: cell-c603be191196eab2
  locked: true
  schema_version: 3
  solution: false
  task: false
---
performances.loc[3] = ["23 attributs ad-hoc", p_tr, s_tr, p_te, s_te]
performances.style.format(precision=2).background_gradient(cmap='Blues')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b13fb51af134dd39ababef32a80c0d58", "grade": false, "grade_id": "cell-aa559e5db97a48c8", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Calculez la matrice de correlation comme on a fait plus haut.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: a8fab7ced6e1e89b1f73fc02b854fb14
  grade: false
  grade_id: cell-33e34bbffac3ecf9
  locked: false
  schema_version: 3
  solution: true
  task: false
---
# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d332757810d4a16fe5bb6404f38036b3", "grade": false, "grade_id": "cell-bca813be79b87807", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Dans l'approche univariée, les attributs qui nous intéresse le plus
sont ceux qui ont une grande corrélation en valeur absolue avec les
étiquettes. Autrement dit, les valeurs très positives (corrélation) ou
très négatives (anti-corrélation) de la dernière colonne sont
intéressants pour nous.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "33d7ee18b632343f7052892cfbf35e58", "grade": false, "grade_id": "cell-d5acd45db38cea70", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On va donc ordonner les attributs qui corrèlent le plus avec nos
étiquettes (en valeur absolue) :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 500a9f8647a7114de2aff5369129cce3
  grade: false
  grade_id: cell-7c3e67dfcca6f41c
  locked: true
  schema_version: 3
  solution: false
  task: false
---
# Sort by the absolute value of the correlation coefficient
sval = corr_large['class'][:-1].abs().sort_values(ascending=False)
ranked_columns = sval.index.values
print(ranked_columns) 
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "959f919b65cf38439ab7041bfecd3c40", "grade": false, "grade_id": "cell-4a9f0260493fe6a0", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Sélectionnons seulement les trois premiers attributs et visualisons
leur valeurs dans un pair-plot :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 83254613519671656824b5a8c0a336b5
  grade: false
  grade_id: cell-e08b03acd62683c6
  locked: true
  schema_version: 3
  solution: false
  task: false
---
col_selected = ranked_columns[0:3]
df_features_final = pd.DataFrame.copy(df_features_large)
df_features_final = df_features_final[col_selected]

df_features_final['class'] = df_features_large["class"]
g = sns.pairplot(df_features_final, hue="class", markers=["o", "s"], diag_kind="hist")
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8a70a137e49d48782ef60560ba90521d", "grade": false, "grade_id": "cell-7002dd8fbb10e127", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Trouver le nombre optimal d'attributs

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e33e4bcc0124ea0ae3d101858ba83256", "grade": false, "grade_id": "cell-2a2b1eb294872e13", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On s'intéresse à présent au nombre optimal d'attributs. Pour cela, on
calcule les performances en rajoutant les attributs dans l'ordre du
classement fait dans la sous-section précédente (classement en
fonction de la corrélation avec les étiquettes).

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9460f2448750ebc658df8cb2def0d77a", "grade": false, "grade_id": "cell-793922168d252b11", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Importez le modèle KNN avec trois voisins dans l'objet `sklearn_model`.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: b2fe892cfa899dbdc07a9f97d1bacbc2
  grade: false
  grade_id: cell-e7597615c5ad6d84
  locked: false
  schema_version: 3
  solution: true
  task: false
---
# On importe notre modèle
from sklearn.metrics import balanced_accuracy_score as sklearn_metric

# VOTRE CODE ICI
raise NotImplementedError()

feat_lc_df, ranked_columns = feature_learning_curve(df_features_large, sklearn_model, sklearn_metric)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: fdbaf2dce314fb31c46258619c2f471b
  grade: false
  grade_id: cell-b5e1e0f4d421c2d3
  locked: true
  schema_version: 3
  solution: false
  task: false
---
plt.errorbar(feat_lc_df.index+1, feat_lc_df['perf_tr'], yerr=feat_lc_df['std_tr'], label='Training set')
plt.errorbar(feat_lc_df.index+1, feat_lc_df['perf_te'], yerr=feat_lc_df['std_te'], label='Test set')
plt.xticks(np.arange(1, 22, 1)) 
plt.xlabel('Number of features')
plt.ylabel(sklearn_metric.__name__)
plt.legend(loc='lower right');
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "790e646c27c05dcd65ab7e28a0e3e183", "grade": true, "grade_id": "cell-4996b8b770bbb95c", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

**Exercice** Combien d'attributs pensez-vous utile de conserver?
Justifiez.

VOTRE RÉPONSE ICI

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "99667d049552603b6287ced97c3ae79e", "grade": false, "grade_id": "cell-9006ed5128fae6b4", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Exercice

Exportez votre table `df_features_final` dans le fichier
`features_data.csv` contenant les attributs utiles. Pour l'exemple,
nous exporterons les trois premiers attributs comme dans l'exemple
plus haut :

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 2f8d3f1c8dc5427fcff1d2a6d785cef9
  grade: false
  grade_id: cell-a4b1b56535d0b411
  locked: false
  schema_version: 3
  solution: true
  task: false
---
# VOTRE CODE ICI
raise NotImplementedError()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9f1f01dfa8975125a80ce64c72561ecd", "grade": false, "grade_id": "cell-e65607c5d0372c04", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Enfin, on ajoute les performance de notre classificateur sur ce
sous-ensemble d'attributs sélectionnées par analyse de variance
univariée et on les ajoute à notre tableau de données `performances` :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 19ce9404b6581952c31e6d7785b84d39
  grade: false
  grade_id: cell-bb10bc28a727b6d0
  locked: true
  schema_version: 3
  solution: false
  task: false
---
# Validation croisée
p_tr, s_tr, p_te, s_te = df_cross_validate(df_features_final, sklearn_model, sklearn_metric)
metric_name = sklearn_metric.__name__.upper()
print("AVERAGE TRAINING {0:s} +- STD: {1:.2f} +- {2:.2f}".format(metric_name, p_tr, s_tr))
print("AVERAGE TEST {0:s} +- STD: {1:.2f} +- {2:.2f}".format(metric_name, p_te, s_te))
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 763f49124cf808e55e70e46dddf6c18c
  grade: false
  grade_id: cell-f9293553bc3eb23b
  locked: true
  schema_version: 3
  solution: false
  task: false
---
performances.loc[4] = ["3 attributs par analyse de variance univarié", p_tr, s_tr, p_te, s_te]
performances.style.format(precision=2).background_gradient(cmap='Blues')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "17f14be9751aa2eb6b9c1a36902de0aa", "grade": false, "grade_id": "cell-f8492a11c05e01bc", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### ♣ Analyse de variance multi-variée

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "14c4ab8a928f9b5d852804257c517aac", "grade": false, "grade_id": "cell-d21fa0397d45598e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

La seconde approche est de considérer les attributs de manière groupés
et non pas par ordre d'importance en fonction de leur corrélation
individuelle avec les étiquettes. Peut-être que deux attributs, ayant
chacun une faible corrélation avec les étiquettes, permettront une
bonne performance de classification pris ensemble.

Pour analyser cela, on considère toutes les paires d'attributs et on
calcule nos performances avec ces paires. Si le calcul est trop long,
réduisez le nombre d'attributs à considérer.

```{code-cell} ipython3
best_perf = -1
std_perf = -1
best_i = 0
best_j = 0
nattributs = 23
for i in np.arange(nattributs): 
    for j in np.arange(i+1,nattributs): 
        df = df_features_large[[ranked_columns[i], ranked_columns[j], 'class']]
        p_tr, s_tr, p_te, s_te = df_cross_validate(df_features_large, sklearn_model, sklearn_metric)
        if p_te > best_perf: 
            best_perf = p_te
            std_perf = s_te
            best_i = i
            best_j = j
            
metric_name = sklearn_metric.__name__.upper()
print('BEST PAIR: {}, {}'.format(ranked_columns [best_i], ranked_columns[best_j]))
print("AVERAGE TEST {0:s} +- STD: {1:.2f} +- {2:.2f}".format(metric_name, p_te, s_te))
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b36b464e908b6101bd20b0632143a673", "grade": true, "grade_id": "cell-3bc0c874f5b7944c", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

:::{admonition} Exercice

Quelle est la paire d'attributs qui donne les meilleurs performances?
Est-ce que l'approche multi-variée est nécessaire avec les pommes et
les bananes? Avec votre jeu de données?

VOTRE RÉPONSE ICI

:::

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6a9647d7892a4e119043c0f227810df0", "grade": false, "grade_id": "cell-f510a13268759d00", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Conclusion

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d046af2d4434384d61b7e9b63596b6e5", "grade": true, "grade_id": "cell-c5a8e3d90bxe5375", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

Cette feuille a fait un tour d'horizon d'outils à votre disposition
pour le prétraitement de vos images et l'extraction
d'attributs. Prenez ici quelques notes sur ce que vous avez appris,
observé, interprété.

VOTRE RÉPONSE ICI

Si le cours de la Semaine 8 a eu lieu, vous pouvez passer à la feuille
sur la [comparaison de classificateurs](4_classificateurs.md)!

Sinon, commencez votre propre [analyse](0_analyse.md).

```{code-cell} ipython3

```
