---
jupytext:
  notebook_metadata_filter: rise
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
rise:
  auto_select: first
  autolaunch: false
  centered: false
  controls: false
  enable_chalkboard: true
  height: 100%
  margin: 0
  maxScale: 1
  minScale: 1
  overlay: "<div style='position: absolute; top: 0; left: 0'>Introduction \xE0 la\
    \ Science des Donn\xE9es, L1 Math-Info, Facult\xE9 des Sciences d'Orsay</div><div\
    \ style='position: absolute; top: 0; right: 0'><img src='media/logoParisSaclay.png'\
    \ width='150'></div>"
  scroll: true
  slideNumber: true
  start_slideshow_at: selected
  transition: none
  width: 90%
---

+++ {"slideshow": {"slide_type": "slide"}}

<center>

# Cours 4: Construction et sélection d'attributs

</center>

<br>

<center>Fanny Pouyet</center>

<center>L1 Mathématique-Informatique</center>

<center>Janvier - Avril 2024</center>

$\newcommand{\var}{\operatorname{var}}$
$\newcommand{\Proba}{\operatorname{Proba}}$

+++ {"slideshow": {"slide_type": "slide"}}

**Précédemment**

* Définition et objectif de la science des données
* Introduction à la librairie Pandas, Numpy, Matplotlib, Sklearn
* Visualisation des données
* Chaine de traitement en analyses des données

**Cette Semaine**

* Retour sur les statistiques
* Extraction de features à partir d'images
* Votre propre jeu de données

+++ {"slideshow": {"slide_type": "slide"}}

## Statistiques

### Loi Normale

Loi de probabilité continue de moyenne $\mu$ et de variance $\sigma^2$. Cette «courbe en cloche» a les propriétés suivantes:
* la moyenne et la médiane sont égales
* la courbe est symétrique et centrée sur la moyenne
* 95% des observations sont comprises entre $[\mu - 2 \sigma; \mu + 2 \sigma]$.
* si $\mu=0$ et $\sigma^2=1$, on parle de *loi normale centrée réduite*.

```{figure} media/Normal_Distribution.svg
---
alt: media/Normal_Distribution.svg
width: 500px
align: center
---
    <a href="https://fr.wikipedia.org/wiki/Loi_normale">Wikipedia: Loi Normale</a>
```

+++ {"slideshow": {"slide_type": "slide"}}

### Taille d'échantillon $n$

Dans notre étude, la moyenne de «redness» de nos dix pommes est *très probablement* différente de la moyenne de «redness» de toutes les photos de pommes sur Terre.

```{figure} media/taille_echantillon.svg
---
alt: taille_echantillon.svg
width: 600px
align: center
---
```





Intuitivement, plus la taille de l'échantillon $n$ est grande et plus précise sera l'estimation de la moyenne. 

Mathématiquement, on dit que la **variance de la moyenne est inversement proportionnelle à $n$**.

+++ {"slideshow": {"slide_type": "slide"}}

### Retour sur la moyenne $\mu$

Notre objectif étant de distinguer n'importe quelle photo de pomme de celle de banane, on cherche la <b><font color = 'red'>vraie moyenne (= l'attendu mathématique)</font></b> d'une quantité (la redness, notée $X$).

Mathématiquement, on distingue:
* $\mu$: la vraie moyenne de $X$, obtenue sur un nombre infini d'exemple
* $\hat{\mu} = (1/n) (\sum_{i=1}^n X_i)$: l'estimateur empirique de la moyenne (calculé sur seulement $n$ exemples). 

Mais dans la pratique, on écrit souvent $\mu$ alors qu'on parle de $\hat{\mu}$ (cf. les cours précédents).  
Alors pourquoi je mentionne cela ?

+++ {"slideshow": {"slide_type": "slide"}}

### Distribution de la moyenne et théorème central limite

* $\hat{\mu}$ dépend des $n$ échantillons ($\bar{X}$).
* Avec $n$ autres échantillons pris **aléatoirement et indépendamment**, $\hat{\mu}$ serait différent. 
* $\hat{X}$ est une **variable aléatoire** (ou random variable). 
* En  échantillonnant de nombreuses fois, on peut dessiner la *distribution de la moyenne*.

+++ {"slideshow": {"slide_type": "slide"}}

#### Théorème central limite

 Si $X$ suit une distribution de moyenne $\mu$ et d'écart-type (standard deviation) $\sigma$ et si $X$ est normalement distribué ou bien que $n$ est suffisamment large alors **$\hat{X}$ est distribuée normalement avec une moyenne $\mu$ et un écart-type $\sigma/\sqrt{n}$**.
 
```{figure} media/tcl.png
---
alt: media/tcl.png
width: 500px
align: center
---
    <a href="https://fr.wikipedia.org/wiki/Théorème_central_limite">Wikipédia: Théorème central limite</a>
```

+++ {"slideshow": {"slide_type": "slide"}}

**Démonstration**

Soit $n$ variables aléatoires distribuées identiquement et indépendantes l'une de l'autre : $X_1, X_2, \ldots, X_n$. Elles suivent la même loi de probabilité de moyenne $\mu$ et de variance $\sigma^2$.

De facon générale on a : $$ V(X+Y) = V(X) + V(Y) + cov(X,Y) $$

Et si 2 variables aléatoires sont indépendantes, leur covariance est nulle. C'est notre cas ici  donc la variance de la somme est égale à la somme des variances:

$$V(\sum_{i=1}^n X_i) = \sum_{i=1}^n V(X_i) = n \sigma^2$$

+++ {"slideshow": {"slide_type": "slide"}}

Par ailleurs, la moyenne empirique des $n$ variables aléatoires est:

$$ \hat{\mu} = (1/n)(\sum_{i=1}^n X_i) $$.

+++ {"slideshow": {"slide_type": "fragment"}}

Et si on calcule $V(\hat{\mu})$, on finit par trouver que la **variance de la moyenne** est: 

$$V(\hat{\mu}) = \sigma^2/n$$

(en cours: à faire au tableau, à la maison : voir la [page Wikipedia de variance](https://fr.wikipedia.org/wiki/Variance_(math%C3%A9matiques)#Somme_de_variables_ind%C3%A9pendantes))

+++ {"slideshow": {"slide_type": "slide"}}

Concernant la moyenne, d'après la **[loi des grands nombres](https://en.wikipedia.org/wiki/Law_of_large_numbers)**, si $n$ tend vers l'infini alors la moyenne empirique $\hat{\mu}$ converge vers l'attendu mathématique $\mu$ et la variance de la moyenne tend vers 0. En effet:

$$\operatorname{Proba}(\mu - 2\sigma/\sqrt{n} < \hat{\mu} < \mu + 2\sigma/\sqrt{n}) = 0.95$$

Ainsi $\hat{\mu}$ converge vers $\mu$ .

+++ {"slideshow": {"slide_type": "slide"}}

### Intervalles de confiance (CI, confidence intervals)
    
*Problème:* Comment savoir si on estime *bien* les vraies valeurs ?

Connaissant nos contraintes (que 10 photos), on peut donner un intervalle dans lequel on est sûre de trouver la rougeur moyenne d'une photo de pomme. On parle d'**intervalle de confiance**.

+++ {"slideshow": {"slide_type": "slide"}}

Pour une distribution normale, on a :


* $P(\mu-\sigma<Redness<\mu+\sigma) = 0.68$
* $P(\mu-2\sigma<Redness<\mu+2\sigma) = 0.95$


Souvent vous verrez écrit : Redness = $\mu \pm 2 \sigma$, ce qui se lit "La rougeur moyenne des pommes est de $\mu$ à + ou - deux $\sigma$ pour l'intervalle de confiance à 95% dans le cas de données distribuées normalement". Ou bien on indiquera les limites supérieures ($U$) et inférieures ($L$) avec le niveau de confiance : Redness = $[L, U]$, 95% CI.

+++ {"slideshow": {"slide_type": "slide"}}

### Rééchantillonnage par bootstrap

*Problème*: Avec 10 photos de pommes, on ne peut pas échantillonner indépendamment un grand nombre de fois des photos. Comment mesurer des intervalles de confiance ?

La méthode de **bootstrap** permet d'estimer des quantités (des moyennes de rougeurs ici) d'une population en moyennant les estimations à partir de plusieurs de sous-echantillons.

```{figure} media/bootstrap.svg
---
alt: media/bootstrap.svg
width: 500px
align: center
---
```

**Par rapport à avant, ici, nos échantillons ne sont pas indépendants !! Il y a un biais dans cette méthode**

+++ {"slideshow": {"slide_type": "slide"}}

L'échantillonnage se fait **avec remise** (*sampling with replacement*) et ainsi, une instance peut être prise *plus d'une fois* par échantillon.

Pseudo-code: 
1. Soit *B* le nombre de bootstrap
2. Soit $n$ la taille d'échantillon (sample size)
3. Pour chaque $b \in B$:
    1. Echantillonnage avec remise de $n$ valeurs
    2. Calcul de la statistique sur cette instance
4. Calcul de la moyenne et de la variance des *B* statistiques estimées

Le bootstrap permet de quantifier l'incertitude associée à un estimateur. La distribution des estimateurs suit généralement une loi normale centrée autour de la moyenne observée de notre jeu de données.

+++ {"slideshow": {"slide_type": "slide"}}

En TP, on verra comment le bootstrap permet d'estimer l'efficacité d'un modèle de machine learning.

Pseudo-code:
1. Soit *B* le nombre de bootstrap
2. **Soit $n_{tr} + n_{te}$ la taille d'échantillon (sample size)**
3. Pour chaque $b \in B$ (boucle *for*):
    1. Echantillonnage d'un *training* ($n_{tr}$) et d'un *test* set ($n_{te}$)
    2. **Optimisation du modèle sur le training set actuel (*model fit*)**
    3. **Calcul du taux d'erreur ou de l'accuracy sur le test set actuel**
4. Calcul de la moyenne et de la variance des $B$ **taux d'erreurs**.

*Remarque importante*: toute filtration des données effectuée avant de fitter un modèle doit être inclue dans la boucle *for* afin d'éviter d'introduire des biais et ainsi de surestimer la précision de notre modèle.

+++ {"slideshow": {"slide_type": "slide"}}

## Extraction et sélection d'attributs : redness et elongation

+++ {"slideshow": {"slide_type": "slide"}}

On va voir comment extraire la rougeur et l'élongation d'images en Python.  
Lors de vos projets, vous serez amenés à adapter ce code à la spécificité de votre jeu de données.

En Python, nous utiliserons la bibliothèque *PIL* et *Matplotlib*

+++ {"slideshow": {"slide_type": "slide"}}

### Librairie *PIL*

PIL ([Python Imaging Library](https://he-arc.github.io/livre-python/pillow/index.html)) est une bibliothèque de traitement d’image de formats tels que PNG, JPEG, TIFF etc, qui utilise le principe d'images matricielles:

* un pixel = un élément d'une matrice. 
* Une image en couleur contient plusieurs bandes de données (les 4 bandes RGBA vu précédemment par exemple). 

PIL permet de filtrer, redimensionner, tourner, transformer les images. Grâce aux bandes on peut également agir indépendamment sur l'une ou l'autre.

```{figure} media/pil.png
---
alt: media/pil.png
width: 120px
align: center
---
```

+++ {"slideshow": {"slide_type": "slide"}}

### Pixels RGBA

Red, Green, Blue, Alpha (transparence)

Pixels RGBA:
* Les bandes RGB varient de 0 à 255 (vu en TP2); 
* la bande A varie de 0 (transparent) à 255 (opaque)
* Plus le chiffre est élevé plus la couleur est forte.

```{figure} media/features_images.svg
---
alt: media/features_images.svg
width: 200px
align: center
---
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
from PIL import Image
import matplotlib.pyplot as plt 
import numpy as np 
import os
#On charge l'image : étiquette de la librairie PIL
image = Image.open("media/pil.png")

#Exemple pour transformer l'image en noir et blanc
imageNB = image.convert('L')
arrNB = np.asarray(imageNB)
#matplotlib prend en entrée des array
plt.imshow(arrNB, cmap='gray', vmin=0, vmax=255)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# Manipulation des bandes, on échange les intensités de rouge, vert, bleu

# On obtient 4 sous matrices
r, g, b, a = image.split()

# on change l'ordre !
image_ordered = Image.merge("RGBA", (b, r, g, a))

plt.imshow(image_ordered) 
```

+++ {"slideshow": {"slide_type": "slide"}}

### Distinction entre l'objet et l'arrière plan

Avant d'étudier les attributs de nos images, on souhaite extraire objet (le *foreground*) de l'arrière-plan (*background*). Ce dernier pourrait en effet influencer nos estimateurs. 

Dans nos exemples (pommes et logo PIL):

```{code-cell} ipython3
:tags: []

# Hack: select which bytecode file to use for utilities_cours_correction depending on Python's version
import sys
ver = ''.join(str(i) for i in sys.version_info[:2])
!cp __pycache__/utilities_cours_correction.cpython-{ver}.pyc utilities_cours_correction.pyc
```

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
from utilities import *
from utilities_cours_correction import *
from intro_science_donnees import *

dataset_dir = os.path.join(data.dir, "ApplesAndBananasSimple")

# Reload code when changes are made
%load_ext autoreload
%autoreload 2
```

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
carte_RGB(image)
```

+++ {"slideshow": {"slide_type": "slide"}}

* **Observation** : l'arrière plan est clair voire *blanc* :
    * beaucoup de rouge, 
    * de vert et
    * de bleu.

* **Stratégie** :
    * on choisit un seuil (*threshold*)
    * chaque pixel dont le rouge, le bleu **et** le vert est > ce seuil appartient à l'arrière-plan.

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# Transform img into a numpy dataframe
M = np.array(image)

# create a dataframe (same size as each layer of M) with the lowest intensity for the RGB layers
rgb_minimal = np.min(M[:,:,0:3], axis=2)

# threshold for the background/forground distinction
threshold_background = 250
# M_background is a T/F matrix whether the pixel belongs to the background
M_background = (rgb_minimal >= threshold_background)
print(M_background)
img_background = Image.fromarray(M_background)
plt.imshow(img_background) 
```

+++ {"slideshow": {"slide_type": "slide"}}

### Objectif en TP

* Implémenter une fonction `foreground_filter()`
    * prend comme paramètre le seuil (*threshold*)
    * renvoie une matrice T/F selon que le pixel appartienne à l'objet (*foreground*) ou pas

+++ {"slideshow": {"slide_type": "slide"}}

On peut alors utiliser `foreground_filter()` pour extraire notre objet (*foreground*) et rogner l'arrière-plan.

+++ {"slideshow": {"slide_type": "slide"}}

La fonction `transparent_background_filter()` transforme tous les pixels du background en transparents.

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
from typing import Callable, List, Optional, Iterable, Union

# Fonction transparent_background_filter() qui prend en entrée 
# soit une img soit une dataframe et le seuil (theta)
def transparent_background_filter(
    img: Union[Image.Image, np.ndarray], theta: int = 150
) -> Image.Image:
    """Create a cropped image with transparent background."""
    # F est donc une matrice T/F selon que le pixel soit 
    # dans le foreground ou pas
    F = foreground_filter(img, theta=theta)
    # on transforme l'image en matrice RGBA
    M = np.array(img)
    # N est la nouvelle image rognée, on commenca par recopier
    # les couches R, G et B
    N = np.zeros([M.shape[0], M.shape[1], 4], dtype=M.dtype)
    N[:, :, :3] = M[:, :, :3]
    # On modifie la couche d'opacité, A. On met:
    # 0 pour le background (si F[i,j] = False  
    # et False peut etre lu comme 0)
    # 255 pour le foreground (F[i,j] = True 
    # et True peut etre lu comme 1)
    N[:, :, 3] = F * 255
    return Image.fromarray(N)
```

+++ {"slideshow": {"slide_type": "slide"}}

### Extraction de la rougeur (retour à l'exemple pommes/bananes)

* les pommes sont plutôt rouges
* les bananes sont jaunes (généralement)

On peut distinguer ces fruits selon leur rougeur, c'est-à-dire la différence entre l'intensité moyenne de la bande rouge de notre objet et celle de la bande verte. Une image avec une forte rougeur aura beaucoup de rouge et peu de vert.

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
apple = load_images(dataset_dir, "a01.png")[0]
print(redness(apple))
extraction_objet(apple)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
banana = load_images(dataset_dir, "b01.png")[0]
print(redness(banana))
extraction_objet(banana)
```

+++ {"slideshow": {"slide_type": "slide"}}

### Objectif en TP

Vous implémenterez la fonction `redness()`.

Pour une image:
1. Extraction de la matrice des rouges et des verts (M[:,:,0] et M[:,:,1] resp.) 
2. Transformation en nombre à virgules (*floating numbers*) pour faire des calculs.
3. Extraction de l'objet (*foreground_filter()*)
4. Calcul de la redness d'une image
    1. Calcul de la moyenne des rouges
    2. Calcul de la moyenne des verts
    3. Différence
5. Retourne la différence

+++ {"slideshow": {"slide_type": "slide"}}

### Extraction de l'élongation

* les pommes sont rondes
* les bananes sont allongées

*Elongation*: Ratio de la longueur sur la largeur de l'objet. Une pomme ronde aura la largeur $\approx$ la longueur donc une élongation proche de 1.

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# Build the cloud of points defined by the foreground image pixels
dataset_dir = os.path.join(data.dir, 'ApplesAndBananasSimple')
banana=load_images(dataset_dir, "b01.png")[0]

#fonction fournie
cloud(banana)
```

+++ {"slideshow": {"slide_type": "slide"}}

On va voir comment calculer l'élongation sachant que les fruits peuvent avoir différentes orientations et qu'il peut y avoir du bruit. Pour ce faire on va décomposer l'object en valeurs singulières

+++ {"slideshow": {"slide_type": "slide"}}

### Singular vector decomposition

La SVD est une méthode mathématique de factorisation de matrices. Elle permet d'identifier les axes d'un nuage de points pour lequel on a la plus grande variation, par une série de transformations linéaires.

```{figure} media/svd.png
---
alt: media/svd.png
width: 500px
align: center
---
    <a href="https://fr.wikipedia.org/wiki/D%C3%A9composition_en_valeurs_singuli%C3%A8res">Wikipédia: Décomposition en valeurs singulières</a>
```

+++ {"slideshow": {"slide_type": "slide"}}

**Transformations linéaires/non-linéaires**

Une transformation est linéaire ssi les coordonnées des points après la transformation sont une combinaison linéaire (addition, multiplication) des coordonnées avant transformation. La même formule s'applique pour tous les points.

* M est linéaire
* M' n'est pas linéaire

```{figure} media/nonlinear.png
---
alt: media/nonlinear.png
width: 500px
align: center
---
    <a href="https://gregorygundersen.com/blog/2018/12/10/svd/">https://gregorygundersen.com/blog/2018/12/10/svd/</a>
```

+++ {"slideshow": {"slide_type": "slide"}}

En pratique:
* on convertit l'image en un nuage de points (les coordonées des pixels de l'image)
* on centre l'image
* on applique l'algorithme de SVD 
* puis, on extrait l'axe 1 et 2 qui correspondent aux deux axes orthogonaux pour lesquels on a le plus de variation
* on calcule l'élongation

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
def elongation(img: Image.Image) -> float:
    """Extract the scalar value elongation from a PIL image."""
    F = foreground_filter(img)
    # Build the cloud of points given by the foreground image pixels
    xy = np.argwhere(F)
    # Center the data
    C = np.mean(xy, axis=0)
    Cxy = xy - np.tile(C, [xy.shape[0], 1])
    # Apply singular value decomposition
    U,  s, V = np.linalg.svd(Cxy)
    return s[0] / s[1] 
```

+++ {"slideshow": {"slide_type": "slide"}}

### Objectif en TP

* **Pour les bananes/pommes**
    * implémenter et calculer l'attribut de rougeur
    * Calculer l'attribut d'élongation
* **Pour votre jeu de données**
    * les appliquer

+++ {"slideshow": {"slide_type": "slide"}}

## Autres attributs plus généraux

+++ {"slideshow": {"slide_type": "slide"}}

**Cas "difficiles" ?**

Parfois les 2 catégories n'auront pas de différences de couleur (redness) ni de forme (elongation).

```{code-cell} ipython3
---
slideshow:
  slide_type: '-'
---
images = load_images(os.path.join(data.dir, 'Smiley'), "*.png")
image_grid(images, titles=images.index)
```

+++ {"slideshow": {"slide_type": "slide"}}

```{figure} media/smiley_2.png
---
alt: media/smiley_2.png
width: 500px
align: center
---
```

Pourtant, les smiley contents sourient et les smiley pas contents ne sourient pas, c'est simple de les distinguer !

+++ {"slideshow": {"slide_type": "slide"}}

### 1ère méthode : Matched filters

On peut calculer les smiley *moyens* du training set:
* Pour chaque classe (notée *A* et *B*), on calcule un template (le modèle):
    * on transforme les images en NB
    * on calcule la moyenne de noir qu'on a pour chaque pixel

```{figure} media/templates.svg
---
alt: media/templates.svg
width: 500px
align: center
---
```

+++ {"slideshow": {"slide_type": "slide"}}

* Pour chaque image test, on calcule sa corrélation avec les 2 modèles

```{figure} media/correlations.png
---
alt: media/correlations.png
width: 400px
align: center
---
Deux exemples de correlation
```

+++ {"slideshow": {"slide_type": "slide"}}

* On représente les liens entre nos jeux de données test et nos modèles

```{figure} media/correlations_2.png
---
alt: media/correlations_2.png
width: 400px
align: center
---
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
from numbers import Number

def grayscale(img: Image.Image) -> np.ndarray:
    """Return image in gray scale"""
    return np.mean(np.array(img)[:, :, :3], axis=2)

class MatchedFilter:
    ''' Matched filter class to extract a feature from a template'''
    def __init__(self, examples: Iterable[Image.Image]):
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

    def match(self, img: Image.Image) -> Number:
        '''Extract the matched filter value for a PIL image.'''
        # Convert to grayscale and standardize
        M = grayscale(img)
        M = (M - M.mean()) / M.std()
        # Compute scalar product with the template
        # This reinforce black and white if they agree
        return np.mean(np.multiply(self.template, M))
```

```{code-cell} ipython3
#Comment utiliser MatchFilter ?

# on match avec les 10 premières images : celles qui sourient
filtre_sourire = MatchedFilter(images[:10]) 

#on regarde le filtre moyen
#display(filtre_sourire.show())

# on calcule la correlation moyenne entre une figure à tester et le filtre moyen
print("MATCH SOURIRE \n Pour un sourire :", filtre_sourire.match(images[9]))
print("Pour un smiley triste :" , filtre_sourire.match(images[19]))

# il faudrait encore calculer la corrélation moyenne avec le filtre moyen des smileys tristes
# puis comparer les ratios pour savoir à quelle classe appartient notre smiley !!
```

+++ {"slideshow": {"slide_type": "slide"}}

### Objectif du TP

* Utiliser MatchFilter si besoin sur votre jeu de données
* Calculer les pairplots/autres représentations pour analyser vos données

+++ {"slideshow": {"slide_type": "slide"}}

### 2ème méthode : Analyse en Composantes Principales (PCA ou ACP)

* Dans les cas généraux, le nombre de variables pour représenter les données est très élevé.
* Pour nos (petites) images, on a *4096* variables

* Intuitivement, plus on a de variables mieux c'est
* Mais aussi, plus on s'emmêle les pinceaux (exemple: 4096 éléments vs. 2 attributs)


* *Stratégie* : On peut extraire les composantes principales de nos images comme des attributs

+++ {"slideshow": {"slide_type": "slide"}}

### Intérêt: extraire les composantes principales d'une image

1. Visualiser les données
    * filtration des outliers (données aberrantes)
2. Réduire les coûts algorithmiques
    * mémoire
    * temps de calcul
    * identifie la redondance des variables
3. Améliorer de la qualité d'apprentissage des modèles par
    * sélection (choix de qq pixels) ou
    * extraction de variables

+++ {"slideshow": {"slide_type": "slide"}}

### Analyse en Composantes Principales (ACP)

Extraction de variables = création de *m* nouvelles variables à partir des *p* initiales, $m << p$ (redness/elongation sont des combinaisons linéaires des 4096 éléments).

Méthode classique ACP : 
Représentation des données afin de maximiser la variance selon les nouvelles dimensions (comme la SVD). Cette méthode est classiquement utilisée afin de distinguer les classes. Ici on l'utilise pour extraire des attributs = les axes principaux


```{figure} media/PCA_fish.png
---
alt: ACP de poisson
width: 400px
align: center
---
https://fr.wikipedia.org/wiki/Analyse_en_composantes_principales
```

+++ {"slideshow": {"slide_type": "slide"}}

### Différence entre SVD et ACP

* La SVD transforme linéairement l'ensemble de la matrice et détermine l'ensemble des dimensions indépendantes
* L'ACP ne gardent que les *composantes principales*
* On peut utiliser la SVD pour trouver l'ACP en tronquant les vecteurs de base les moins importants dans la matrice SVD d'origine.

+++ {"slideshow": {"slide_type": "slide"}}

En pratique, la classe *PCAFilter* est fournie.

```{code-cell} ipython3
class PCAFilter:
    """PCAFilter

    Similar to matched filter, but using one of the principal
    components of the input images (in grayscale) instead of their
    average.
    """
    def __init__(self,
                 examples: List[Image.Image],
                 num: int = 0):
        # Create the data matrix:
        # each image contributes a column vector made of its pixels
        # in grayscale
        X = np.array([grayscale(img).ravel()
                      for img in examples])
        w, h = examples[0].size
        # Standardize the columns
        X = (X - X.mean(axis=0)) / (X.std(axis=0)+0.000000001)
        # Extract the num-th Principal Component and convert it back
        # to a grayscale image
        U, s, V = np.linalg.svd(X)
        self.template = np.reshape(V[num, :], (h, w))

    def show(self):
        """Show the template"""
        fig = Figure(figsize=(3, 3))
        ax = fig.add_subplot()
        ax.imshow(self.template, cmap='gray')
        return fig

    def match(self, img, debug=False):
        '''Extract the PCA filter value for a PIL image.'''
        # Convert to grayscale and standardize
        M = grayscale(img)
        M = (M - M.mean()) / M.std()
        # Compute scalar product with the template
        # This reinforce black and white if they agree
        return np.mean(np.multiply(self.template, M))
```

+++ {"slideshow": {"slide_type": "slide"}}

### Objectif du TP

* Utiliser PCAFilter si besoin sur votre jeu de données
* Calculer les pairplots/autres représentations pour analyser vos données

+++ {"slideshow": {"slide_type": "slide"}}

## Quelques commentaires sur les jeux de données possibles pour le projet

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
images = load_images(os.path.join(data.dir, 'Farm'), "*.jpeg")
image_grid(images, titles=images.index)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
dataset_dir = os.path.join(data.dir, 'Hands')
images = load_images(dataset_dir, "*.jpeg")
image_grid(images, titles=images.index)
```

```{code-cell} ipython3
images = load_images(os.path.join(data.dir, 'ZeroOne'), "*.png")
image_grid(images, titles=images.index)
```

+++ {"slideshow": {"slide_type": "slide"}}

<center> Le vôtre pour le projet 2 ?
      
 * feuilles d'arbres ou plante pour reconnaitre l'espèce (voir [plantnet](https://plantnet.org/))
    
 * animaux
    
 * etc.
</center>

+++ {"slideshow": {"slide_type": "slide"}}

### Conclusion

* **Comprendre, distinguer et utiliser les différentes notions**:
     * vraie moyenne de la population, moyenne de l'échantillon
     * variance, ecart-type
     * intervalles de confiance
     * distribution
     * échantillonage, bootstrap
        
* **Python**
    * implémenter des attributs
    * les appliquer à un ensemble d'image

+++ {"slideshow": {"slide_type": "slide"}}

* **Science des données**
    * adapter les attributs selon le problème de classification
    * interpréter les résultats
        * est-ce un bon classificateur ?
        * sur quelles bases distingue-t-il les classes ?

+++ {"slideshow": {"slide_type": "slide"}}

### Perspectives

* **CM5**
    * Introduction aux différentes catégories de classificateurs en machine learning
    
    
* **TP4**
    * [En binome](https://codimd.math.cnrs.fr/3f98v4-YT4CN2ktM6_g5lw?both)
    * Calcul de features
    * Application à votre jeu de données (préparation des données, calcul des attributs)

```{code-cell} ipython3

```
