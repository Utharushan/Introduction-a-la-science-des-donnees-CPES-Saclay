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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "56952047c4310bf0c313ca44bb5af720", "grade": false, "grade_id": "cell-883bbb5e1919ca1e", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": ""}, "tags": []}

# Analyse de données

:::{admonition} Consignes
:class: dropdown

Vous documenterez votre analyse de données dans cette feuille. Nous
vous fournissons seulement l'ossature. À vous de piocher dans les
feuilles et TPs précédents les éléments que vous souhaiterez
réutiliser et adapter pour composer votre propre analyse!

:::

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "07b6f7ec89dbe99e092902adb7ff9cc8", "grade": false, "grade_id": "cell-e15fdd0116a9b9e2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Import des bibliothèques

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "96489bd4f670f5daa152f95fa18ce301", "grade": false, "grade_id": "cell-406ad2a159064cfa", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On commence par importer les bibliothèques dont nous aurons besoin.

:::{admonition} Consignes
:class: dropdown

Inspirez vous des précédentes feuilles. N'oubliez pas d'importer
`utilities` et `intro_science_donnees`.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 8e6a7da13b6e1d41caa1c33a8c0104e5
  grade: false
  grade_id: cell-76e64ee7bcb96bb5
  locked: false
  schema_version: 3
  solution: true
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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e319f7fbbc65f7368fd94b546edb9e34", "grade": false, "grade_id": "cell-6ec03d05a4e1c693", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Chargement des images

:::{admonition} Consignes
:class: dropdown

- Chargez vos images recentrées et réduites.
- Affichez les.

:::

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: a842cb19c2f315d9a183cf8a17bd295f
  grade: false
  grade_id: cell-211e275ccc954714
  locked: false
  schema_version: 3
  solution: true
  task: false
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
image_grid(images_cropped, titles=images.index)
```

```{code-cell} ipython3
def my_foreground_filter(image):
    # Appliquer le filtre de rougeur de premier plan
    foreground_mask = foreground_redness_filter(image)
    
    # Inverser les valeurs si le fond est blanc
    foreground_mask = invert_if_light_background(foreground_mask)
    
    # Appliquer le filtre gaussien avec un sigma de 0.2
    image_filtered = scipy.ndimage.gaussian_filter(image, sigma=0.2)
    
    return image_filtered

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

clean_images = images_cropped.apply(my_preprocessing)
```

```{code-cell} ipython3
image_grid(clean_images)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0e4e77fedcf1d467c6139e4c44ff1e5e", "grade": false, "grade_id": "cell-e723e3fb5001bd97", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Prétraitement : extraction des attributs

:::{admonition} Consignes
:class: dropdown

- Choisissez entre des attributs ad-hoc ou obtenus via une ACP depuis
  les données brutes (représentation en pixel).
- N'oubliez pas de normaliser votre table une fois les traitements
  effectués.
  
:::

```{code-cell} ipython3
noirblanc=([np.mean(np.array(img), axis = 2) < 100 
            for img in clean_images])

def ennoir(array):
    for i in range(len(array)):
        for j in range(0,5):
            array[i][j]=False
        for j in range(len(array)-5,len(array)):
            array[i][j]=False
        if i>=27 or i<=4:
            array[i]=[False]*len(array)
    return array


arrayennoir = [ennoir(x) for x in noirblanc] 
image_grid(arrayennoir)
```

```{code-cell} ipython3
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
filtre_effected = MatchedFilter(clean_images[:10]) 
filtre_healthy = MatchedFilter(clean_images[10:])
display(filtre.show())
display(filtre_effected.show())
display(filtre_healthy.show())

print("MATCH EFFECTED OU HEALTHY \nPour un effected :", filtre_effected.match(clean_images[19]))
print("Pour un healthy :" , filtre_healthy.match(clean_images[19]))

filtre_effected_images = [filtre_effected.match(clean_images[i]) for i in range(20)]
filtre_healthy_images = [filtre_healthy.match(clean_images[i]) for i in range(20)]
for i in range(20):
    print(f"{i} : {filtre_effected_images[i]}  {filtre_healthy_images[i]}")
```

```{code-cell} ipython3
def average_pixel_value(image):
    # Calculer la moyenne des valeurs des pixels
    avg_value = np.mean(image)
    return avg_value

images_traitees = [np.mean(np.array(img), axis = 2) < 100 
            for img in clean_images]
avg_pixel_value = [average_pixel_value(arrayennoir[i]) for i in range(20)]
print("La moyenne des valeurs des pixels pour chaque image :")
print(avg_pixel_value)
```

```{code-cell} ipython3
# Create a dictionary with the desired attributes and their corresponding values
data = {
    'filtre_effected_images': filtre_effected_images,
    'filtre_healthy_images': filtre_healthy_images,
    'avg_pixel_value' : avg_pixel_value,
            'class':      images.index.map(lambda name: 1 if name[0] == 'a' else -1)

}

file_names = [f'a0{i}.png' for i in range(1, 10)] + ['a10.png'] + [f'b0{i}.png' for i in range(1, 10)] + ['b10.png']

# Create the pandas Series
series = pd.DataFrame(data, index=file_names)

# Display the series
print(series)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0b04fc60580d53165e039ab88751a746", "grade": false, "grade_id": "cell-a69bb602ef2221a4", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Sauvegarde intermédiaire

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "35a89b8dc927e0dd763e9cdf592c4bdf", "grade": false, "grade_id": "cell-8cb1846130b9cfe2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Consignes
:class: dropdown

Une fois que vous êtes satisfaits des attributs obtenus, faites en une
sauvegarde intermédiaire.

:::

```{code-cell} ipython3
csv_filename = "attributs.csv"
series.to_csv(csv_filename)
print(f"Attributs sauvegardées avec succès dans le fichier {csv_filename}.")
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b11c92757f734a72bf65f47b9513ca5f", "grade": false, "grade_id": "cell-4576e2c2723b724d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Visualisation des données

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ba2beca9ed69fdecbf145787bb70f7af", "grade": false, "grade_id": "cell-2a67648ea9c07906", "locked": true, "schema_version": 3, "solution": false, "task": false}}

:::{admonition} Consignes
:class: dropdown

Visualisez les attributs et leur corrélation. Mettez en œuvre les
formes que vous jugerez les plus pertinentes (carte thermique, ...).

:::

```{code-cell} ipython3
attributs = pd.read_csv(csv_filename, index_col=0)

corr_matrix = attributs.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Heatmap de corrélation des attributs')
plt.show()
```

```{code-cell} ipython3
sns.pairplot(attributs, hue='class', palette='coolwarm')
plt.suptitle('Paire de graphiques des attributs')
plt.show()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fed3b57a555c863751f511011266a6de", "grade": false, "grade_id": "cell-c103279002f68467", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Performance 

:::{admonition} Consignes
:class: dropdown

- Choisissez un ou plusieurs classificateurs et calculez leur
  performances.
- Comparez les performances selon les attributs utilisés (ad-hoc,
  ...).
- Si vous le souhaitez, vous pouvez aussi:
    - comparer un ou plusieurs classificateurs
	- comparer les performances selon le nombre de colonnes (pixels ou
      attributs) considérées.

:::

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
         "Naive Bayes", "QDA","Perceptron"]
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
    Perceptron(tol=1e-3, random_state=36, shuffle=True, max_iter=100)]


from sklearn.metrics import balanced_accuracy_score as sklearn_metric
compar_results = systematic_model_experiment(series, model_name, model_list, sklearn_metric)
compar_results.style.format(precision=2).background_gradient(cmap='Blues')

compar_results[['perf_tr', 'perf_te']].plot.bar()
```

```{code-cell} ipython3
compar_results
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ae7f04d9aea4689c8f25f33fd8cddf30", "grade": true, "grade_id": "cell-c5a8e3d90bb35375", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

VOTRE RÉPONSE ICI
