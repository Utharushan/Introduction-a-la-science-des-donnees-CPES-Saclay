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
  header: <div><img src='media/logoParisSaclay.png' width='150' align=right></div>
  height: 100%
  margin: 0
  maxScale: 1
  minScale: 1
  scroll: true
  slideNumber: true
  start_slideshow_at: selected
  transition: none
  width: 90%
---

+++ {"slideshow": {"slide_type": "slide"}}

<center>

# Cours: Initiation à la Science des Données : VI-ME-RÉ-BAR

</center>

<center>Fanny Pouyet</center>

<center>L1 Informatique</center>

<center>Janvier - Avril 2024</center>

+++ {"slideshow": {"slide_type": "slide"}}

**Précédemment**

* Définition et objectifs de la science des données
* Découverte des bibliothèques `Pandas`, `Matplotlib`, `Seaborn` et
  `Statsmodels`
* Observation des données

**Cette semaine**

* Chaîne de traitement en analyse des données
* Un peu d'interprétation des résultats

Remerciements: Isabelle Guyon

+++ {"heading_collapsed": true, "slideshow": {"slide_type": "slide"}}

## Chaine de traitement en analyse des données

* **EXPLORATION**

    1. Observer les données : Combien d'instances a-t-on ? (CM2)
    2. Identifier la question posée. (CM2)
    3. Comprendre ce qu'est un attribut (feature) voire en calculer d'autres (CM3) pour répondre à la question.
    

* ***VI*sualisation** , ***ME*sures**, ***RÉ*férences** et ***BAR*res d'erreurs**  

VI-ME-RÉ-BAR (CM3)

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

* **OBSERVATIONS** 

La conclusion se fait en 2 temps: l'observation de nos résultats 

* **INTERPRÉTATIONS**

Et leur interprétation. Qu'est ce qu'on peut raconter ?

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

### Problématique

Nous allons aborder un problème de classification automatique d'images de
fruits par apprentissage statistique (*machine learning*). A part
l'intérêt pédagogique, quelle peut être l'utilité d'étudier un tel
problème ?

[Réponse](https://youtu.be/h0-NS3z-EXo)



```{image} media/fruits.jpeg
:alt: source :https://observatoire-des-aliments.fr/wp-content/uploads/2015/09/fruit8.jpg
:class: bg-primary
:width: 400px
:align: center
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

### Connaissez-vous l'apprentissage statistique? l'intelligence artificielle ?

* Êtes vous capable de définir ces termes?
  
* Connaissez-vous des entreprises qui en font ? Des exemples
  d'application ?

  Répondez au [sondage sur wooclap](https://app.wooclap.com/ISDCM3)

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

Une révolution très récente : [ChatGPT](https://chat.openai.com/)

```{figure} https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg
---
alt: logo de ChatGPT
width: 100px
align: center
---
```

Une autre révolution en IA : [Alphafold](https://www.youtube.com/watch?v=B9PL__gVxLI&ab_channel=YannicKilcher)

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Définition de l'apprentissage statistique**

L'apprentissage statistique (*Machine Learning*), combinant
statistiques et informatique, est au coeur de la science des données
et de l’intelligence artificielle. L'objectif est d'obtenir une
fonction prédictive à partir d'un jeu de données; ***ici: la
classification d'images de fruits***.

**Applications diverses**

* moteurs de recherche
* banque
* médecine
* énergie

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Overview - Marcelle**

*Marcelle* est une boîte à outil qui permet de concevoir des
applications interactives d'apprentissage statistique dans le
navigateur. Elle permet de programmer le flux de données (*pipeline*) vers les modèles et d'intéragir sur les composants du flux
avec des outils interactifs (visualisations, choix des paramètres
etc.).  Les applications ainsi réalisées peuvent être utilisées dans des
contextes variés:
* **Pédagogie**: démonstrations et utilisation de l'apprentissage
  machine sans programmation.
* **Recherche**: Conception et évaluation de nouvelles interactions
  avec les algorithmes de ML
* **Collaboration** entre différents domaines. Par exemple, un médecin
  peut s'occuper de vérifier les données tandis qu'un chercheur en
  apprentissage statistique conçoit le modèle. Ils peuvent collaborer
  via Marcelle.

```{image} media/marcelle.png
:alt: Marcelle
:class: bg-primary
:width: 400px
:align: center
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Overview - Chaîne de Traitement**

Classification en direct à l'aide d'un exemple
utilisant [Marcelle](https://demos.marcelle.dev/webcam-dashboard/)

*N.B: Marcelle* est développé à Saclay par J. Francoise, B. Caramiaux
et T. Sanchez.  Vous pouvez aller sur le site pour tester les exemple
vous même (ne fonctionne pas sur mobile):
[https://marcelle.dev/](https://marcelle.dev/).

*Marcelle: Composing Interactive Machine Learning Workflows and Interfaces. Annual ACM Symposium on User Interface Software and Technology (UIST ’21)*, Oct 2021, Virtual. DOI: 10.1145/3472749.3474734

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

Exemple de questions:
- combien d'instance ?
- pas d'infos d'attributs
- notion de matrice de confusion (*confusion matrix*): combien on a
  juste / combien on a faux?

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Notre jeu de données (CMs et TP3)**

Nous cherchons à classer des pommes et des bananes.

```{code-cell} ipython3
# Hack: select which bytecode file to use for utilities_cours_correction depending on Python's version
import sys
ver = ''.join(str(i) for i in sys.version_info[:2])
!cp __pycache__/utilities_cours_correction.cpython-{ver}.pyc utilities_cours_correction.pyc
```

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
from utilities_cours_correction import *
from intro_science_donnees import *
import os
# Configuration intégration dans Jupyter
%matplotlib inline

# Reload code when changes are made
%load_ext autoreload
%autoreload 2

dataset_dir = os.path.join(data.dir, 'ApplesAndBananasSimple')
images = load_images(dataset_dir, "*.png")
```

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: slide
---
image_grid(images, titles=images.index)
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**EXPLORATION**

* 10 images de chaque type
* Label / Etiquette : l'étiquetage est le processus d'identification
  des données brutes. Cet étiquetage permet d'estimer l'efficacité de
  classification du modèle prédictif.

Quel était l'**étiquette** sur le jeu de données du titanic ?

* Question : séparer correctement les pommes des bananes.
* Attributs : les données que nous allons traiter
* Etiquettes : l'appartenance aux classes de nos images

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

### Comment peut-on manipuler des images en Python ?

Une image est un tableau de pixels

Dans le TP, un pixel de couleur est défini comme la superposition de
quatre couches d'information, RGBA (Red Green Blue Alpha): trois
couleurs + l'opacité (alpha).

```{image} media/features_images.svg
:alt: RGBA définition
:class: bg-primary
:width: 200px
:align: center
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Exemples de cartes RGB**

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
carte_RGB(images[0])
```

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
carte_RGB(images[10])
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Histogramme des couleurs**


On peut aussi visualiser les données comme un histogramme. Comment le lisez vous ?

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
color_histogram(images[0])
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Une vraie pomme**

Refaisons l'exercice avec une image d'une vraie pomme.

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
trueapple = images[8]
carte_RGB(trueapple)
```

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
color_histogram(trueapple)
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Des images aux dataframes**

Vous apprendrez à passer d'une image à un tableau dans la feuille
[Manipulation d'images](../Semaine4/2_images.md) du TP4. Le tableau
est en 3D car on a:
- le nombre de pixels en largeur (32 dans notre cas)
- le nombre de pixels en hauteur (32 dans notre cas)
- les quatre couches: R, G, B et A


[Quelle bibliothèque (qu'on a déjà mentionnée) va-t-on utiliser lors du
TP3 pour manipuler ces images manipulées?](https://app.wooclap.com/ISDCM3)

+++ {"hidden": true, "slideshow": {"slide_type": "fragment"}}

Bibliothèque : 
* `Pandas`

+++

Combien de cases a-t-on par image ?

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
#Nombre d'infos "raw" par image
32*32*4
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

### Attributs (*features*)

Finalement, ce qui nous intéresse ce ne sont pas les 4096 cases mais
seulement celles associées au fruit et pas au fond (au décor) à partir
desquelles nous pourrons calculer des attributs explicites tels que:

* la couleur;
* la forme du fruit.

Lors du CM4/TP4, nous apprendrons à extraire automatiquement ce genre
d'information de nos images. Pour aujourd'hui, nous supposons
simplement qu'elles sont disponibles.

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: slide
---
import pandas as pd                   

df = pd.read_csv("media/preprocessed_data.csv", index_col=0)
df.head()
```

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
df.shape
```

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
df.describe()
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Description de la table de données:**

* 20 instances
* 3 attributs dont une étiquette (ou *label* en anglais, lequel ?):
    * *redness* : couleur, à quel point le fruit est rouge
    * *elongation* : elongation, la ratio entre hauteur et longeur
    * *fruit* : 1 c'est une pomme, -1 c'est une banane

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Observation - Objectif en TP:**

Faire la description de la table, comme vu la semaine dernière :
* quelle est la rougeur moyenne des pommes ? des bananes ?
* quelle est l'élongation moyenne des pommes ? des bananes ?
* quelles sont les échelles de valeurs des attributs ? Peut-on les comparer entre elles ?

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

### Standardisation des données

*Motivation*: On veut interpréter la valeur d'un
attribut indépendamment de son échelle de valeur
(range).

Géométriquement, standardiser c'est:
* translater la distribution à droite ou à gauche
* étendre ou compresser les données en largeur


```{image} media/standarization.png
:alt: Standardisation distributions
:class: bg-primary
:width: 500px
:align: center
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Définition:**

La standardisation revient à:
1. **centrer** les valeurs d'un attribut autour de sa moyenne. Si la
   valeur est >0 alors elle est plus grande que la moyenne (<0, plus
   petite que la moyenne). **Chaque attribut standardisé aura une
   moyenne de 0.**
2. **réduire** les valeurs d'un attribut. Une valeur absolue de $v=2$
   (par exemple) veut dire qu'on est à 2 écart-types de la
   moyenne. **Chaque attribut standardisé (chaque colonne) aura un
   écart-type de 1.**

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

Mathématiquement cela revient à calculer pour chaque attribut $X$:

$ X_{stz} = (X - \mu)/\sigma$

La **standardisation** permet de mettre en évidence les valeurs
aberrantes (*outliers*) qui auront une valeur largement différente de
0 (loin de la moyenne).


```{image} media/standarization.svg
:alt: Standardisation données
:class: bg-primary
:width: 500px
:align: center
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Objectifs du TP:**

* Standardiser les attributs selon la formule présentée (= question
  d'algorithmique en Python). On notera *dfstz* cette
  table. *Remarquez que le label 'fruit' n'a pas à être standardisé;
  c'est un attribut catégoriciel*.

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

### Étude de nos attributs

En TP vous ferez:
* Calcul des corrélations entre les attributs et le label
* Représentation et analyse de ces relations à l'aide d'un pairplot
* Observation des résultats
* Interprétation: en quoi les attributs élongation/rougeur permettent
  de différencier les pommes des bananes ?

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
dfstz = (df-df.mean()) / df.std()
#on ne veut pas standardiser le label !
dfstz['fruit'] = df['fruit']
```

+++ {"heading_collapsed": true, "slideshow": {"slide_type": "slide"}}

## *VI*sualisation

Passons ensuite à l'étape de Visualisation (nouveau). Commençons par
représenter les fruits selon nos 2 attributs:

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: slide
---
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#Create a label with names instead of -1/1 for the legend
dfstz['Fruits'] = np.where(dfstz['fruit'] == 1, "Pommes", "Bananes")

#Make the plot, hue= "nuance" in french
sns.scatterplot(data=dfstz, x="redness", y="elongation", hue="Fruits")
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

### Problème de classification

Maintenant que les données ont été observées et préparées, on va
répondre à notre question : peut-on séparer les pommes des bananes ?

Pour cela, on va définir un *modèle* qui selon des *critères*
déterminera la *nature* des fruits:
* le *modèle* permet de faire des prédictions; on veut mesurer ses
  performances
* les *critères* se basent sur les *attributs*
* la *nature* des fruits est encodé par l'*étiquette*

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

#### a. Séparation des attributs et des étiquettes

On va séparer l'information de la table en deux sous-tables:
* $X$ contiendra les attributs pour faire des prédictions
* $Y$ contiendra ce qu'on cherche à prédire: l'étiquette

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
X = dfstz[['redness', 'elongation']]
Y = dfstz['fruit']
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

**Notations $X$ et $Y$ :**

Mathématiquement, on cherche une fonction $f$ qui, pour chaque
instance $i$, permet de prédire $Y_i$ en fonction des valeurs $X_i$
des attributs.

On cherche $f$ telle que:
$\forall i, Y_i = f(X_i)$

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

#### b. Séparation du jeu de données

Afin de mesurer la performance de notre modèle, on le sépare en deux
groupes:
* l'ensemble d'entraînement (*training set*) à partir duquel on
  ajustera (*fit*) les paramètres du modèle

  *Le modèle doit apprendre à partir d'exemples.*

* l'ensemble de test (*test set*) à partir duquel on mesurera la
  performance du modèle.

  *Le modèle est-il capable de classifier de nouveaux fruits, qu'il ne connaissait pas?*
  
```{image} media/test_training_sets.svg
:alt: Training et tests sets
:class: bg-primary
:width: 600px
:align: center
```

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: slide
---
from sklearn.model_selection import train_test_split

#Separation en training et test set
train_index, test_index = split_data(X, Y, verbose = True, seed=0)
Xtrain, Xtest = X.iloc[train_index], X.iloc[test_index]
Ytrain, Ytest = Y.iloc[train_index], Y.iloc[test_index]
print("Training set:\n",Xtrain,'\n\n', Ytrain)
```

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: slide
---
print("Test set:\n",Xtest,'\n\n', Ytest)
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

Représentation des données

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: fragment
---
#fonction fournie dans les utilities
make_scatter_plot(dfstz, images, train_index, test_index, filter=transparent_background_filter, axis='square')
```

+++ {"heading_collapsed": true, "slideshow": {"slide_type": "slide"}}

## *RE*férence, Modélisation

On peut **enfin** passer à la modélisation. **En fait, la préparation
des données, le calcul des attributs, etc. est ce qui prend le plus de
temps et requiert le plus d'expertise!**

Il existe pléthores de modèles. On va commencer par les $k$ plus
proches voisins mais nous en verrons d'autres au cours de l'UE.

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

### KNN : $k$-Nearest Neighbors

Le classificateur *$k$-nearest neighbors* est une méthode assez
intuitive, l'objet est définit selon le label majoritaire de ses $k$
voisins. Les résultats changent selon la valeur de $k$ utilisée.

```{image} media/knn.svg
:alt: Les plus proches voisins
:class: bg-primary
:width: 600px
:align: center
```


Le classificateur KNN est implémenté dans la bibliothèque
`scikit-learn` (notée `sklearn`) dans la classe `KNeighborsClassifier`
de `sklearn.neighbors`. En pratique cela donne:

```{code-cell} ipython3
---
hidden: true
slideshow:
  slide_type: slide
---
from sklearn.neighbors import KNeighborsClassifier

#Posons :
k = 3

# Définissons le modèle KNN avec k=3
my_first_model = KNeighborsClassifier(n_neighbors=k)

# Apprentissage automatique à partir de l'ensemble d'entrainement
my_first_model.fit(Xtrain, Ytrain) 
```

+++ {"hidden": true, "slideshow": {"slide_type": "slide"}}

```{image} media/knn3_predict.svg
:alt: Prediction KNN
:class: bg-primary
:width: 600px
:align: center
```

+++ {"slideshow": {"slide_type": "slide"}}

## *ME*sure des performances

L'ensemble de test (*test set*) permet de mesurer les performances en appliquant le modèle ajusté au test. Le modèle détermine si le fruit est une pomme ou pas.

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
Ytest_predicted = my_first_model.predict(Xtest)
```

+++ {"slideshow": {"slide_type": "slide"}}

La prédiction correspond-t-elle à la vérité de l'ensemble de *test* ?

Pour mesurer les performances de notre modèle prédictif on peut
compter le nombre d'erreurs:
* **Faux positifs (FP)** : Nombre de bananes (négatif) prises pour des
  pommes (positif) 

  
```{image} media/falsepositive.svg
:alt: Exemple de Faux positif
:class: bg-primary
:width: 600px
:align: center
```

+++ {"slideshow": {"slide_type": "slide"}}

* **Faux négatifs (FN)** : Nombre de pommes (positif) prises pour des bananes (négatif)

```{image} media/falsenegative.svg
:alt: Exemple de Faux négatif
:class: bg-primary
:width: 600px
:align: center
```

+++ {"slideshow": {"slide_type": "slide"}}

|                      | TRUE = Pomme = 1 | FALSE = Banane = -1 |
| -------------------- | ---------------- | ------------------- | 
| PREDICT Pomme = 1    | TP               | FP                  |
| PREDICT Banane = -1  | FN               | TN                  |

Ceci est une **matrice de confusion**.

**TP** = vrai (true) positif; **TN** = vrai (true) négatif

+++ {"slideshow": {"slide_type": "slide"}}

Au total on a $n$ prédictions et $n= TP + TN + FP + FN$

Le **taux d'erreur** $e$ est donc:

$e  = \frac{(FP + FN)}{ n}= \frac{n_{erreurs}}{n_{prédictions}}$

+++ {"slideshow": {"slide_type": "slide"}}

En pratique, on va comparer les labels estimés donc *Ytest_predicted*
avec les véritables labels *Ytest*.

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
e = np.sum((Ytest_predicted != Ytest))  / len(Ytest)
e
```

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
#Strictement équivalent à
e_v2 = np.mean(Ytest_predicted != Ytest)
e_v2
```

+++ {"slideshow": {"slide_type": "slide"}}

On peut également calculer 

* La **précision de la classification (*accuracy*)**,  a = 1 – e

* Le **Balanced Error Rate, BER** = 0.5 (T1 + T2)
    * avec T1 = Type I error = FP / (TN+FP) 
    * et T2 = Type II error = FN / (TP+FN) 

Le BER est utilisé lorsque le nombre d'échantillons par classe
(pommes/bananes) est déséquilibré car on calcule la moyenne du taux
d'erreur de *chaque* classe. Ce n'est pas le cas ici.

+++ {"slideshow": {"slide_type": "slide"}}

### Objectifs en TP

* Implémenter une fonction `error_rate()` pour automatiser ce calcul
  et l'utiliser.
* Calculer la précision de la classification
* Représenter graphiquement les données et observer les résultats

+++ {"slideshow": {"slide_type": "slide"}}

## *BAR*res d'erreurs et significativité

L'objectif est de répondre à la question : *A quel point avons-nous
confiance dans notre modèle ?*

C'est seulement **après** cette étape que nous pourrons **interpréter**
les résultats.

Pour ce faire nous cherchons à estimer *l'erreur de notre
taux d'erreur*. On peut faire 2 options:

+++ {"slideshow": {"slide_type": "slide"}}

1. **Calculer l'erreur standard 1-$\sigma$** de notre modèle prédictif:

$\sigma = \sqrt{\frac{e *
(1-e)}{n}}$ où $e$ est le taux d'erreur et $n$ est le nombre
de tests effectués dans une instance.

Sauriez-vous indiquer ce qui se passerait si on faisait plus de tests ?

+++ {"slideshow": {"slide_type": "slide"}}

2. **Estimer la barre d'erreur par validation croisée CV** 

  * répéter $N=100$ ou $1000$ (ou encore plus) fois la séparation
    entre l'ensemble de test et d'entrainement;
  * recalculer la performance du modèle réapprenant.
  
On a donc $N$ taux d'erreurs à partir desquels on peut estimer *le taux d'erreur moyen*.

+++ {"slideshow": {"slide_type": "slide"}}

La distribution des $e$ observées par
rééchantillonnage se rapproche d'une courbe gaussiene définies par sa moyenne ($\bar{e}$) et son
écart-type $\sigma$ (voir théorème central limite en
[CM4](../Semaine4/CM4.md))

+++ {"slideshow": {"slide_type": "slide"}}

On peut définir un **intervalle de
confiance** de notre taux d'erreur car 95% des mesures du taux d'erreur
tomberaient entre $\bar{e}+2\sigma$ et $\bar{e}-2\sigma$.

```{image} media/tcl.png
:alt: source : https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_central_limite
:class: bg-primary
:width: 600px
:align: center
```

+++ {"slideshow": {"slide_type": "slide"}}

## Conclusions

**Science des données** 
* Chaîne de traitement en analyses des données:
    * on peut synthétiser l'information dans les images en une table
    * préparer les données prend du temps
* L'interprétation des résultats dépend des barres d'erreurs !

**Langage Python 3**
* `sklearn` pour l'apprentissage statistique et les problèmes de classification
* *PIL* pour le traitement d'images (en détail lors du [CM4](../Semaine4/CM4.md))

+++ {"slideshow": {"slide_type": "slide"}}

## Perspectives

**CM 4 : Construction & selection d'attributs**
* Retour sur les barres d'erreurs: compréhension, calcul et interprétation
* Extraction d'attributs a partir d'images
* Votre propre jeu de données

**TP 3**
* Observer les attributs
* Calculer un modèle prédictif (prédeterminé: le 1-NN)
* Calculer des barres d'erreur

+++ {"slideshow": {"slide_type": "slide"}}

**TP 4 et 5 : Mini-projet**

* Classification d'**images** en **binôme**
    * Choisissez deux catégories d'images que vous aimeriez classer
      parmi un ensemble fourni en TP3:
        * canards/poulets, zeros/uns,  ...
        * il y aura 10 images par classe

```{code-cell} ipython3

```
