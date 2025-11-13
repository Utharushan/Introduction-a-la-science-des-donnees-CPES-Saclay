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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "afbf34e64e7471cefc07d9483063e7a8", "grade": false, "grade_id": "cell-3876f910a24fe8a7", "locked": true, "schema_version": 3, "solution": false}}

# Classificateurs

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f1092a8183464dd2e0b498c1337d6626", "grade": false, "grade_id": "cell-65c63f4be1820d2e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Dans cette feuille, nous allons explorer l'utilisation de plusieurs
classificateurs sur l'exemple des pommes et des bananes. Vous pourrez
ensuite les essayer sur votre jeu de données.

Commencons par charger les utilitaires et autres librairies:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 1ea7da415eef57aad06d2165be7ca4ff
  grade: true
  grade_id: cell-a2ccd1e13b05762c
  locked: false
  points: 0
  schema_version: 3
  solution: true
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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d880dfccac7e7bb362d70f774bf09ebb", "grade": false, "grade_id": "cell-875bebae978f4f5a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Chargement et préparation des données

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b4c6e614484358e629bcce73f49598b8", "grade": false, "grade_id": "cell-ce0810dd4273ea24", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On charge le jeu de données prétraité (attributs rougeur et élongation
et classes des fruits). Cela correspond au fichier `attributs.csv` utilisé en Semaine3 :

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 66b99e424464516b2382bde9cbcbc8de
  grade: false
  grade_id: cell-e6d48e8b35c2d42a
  locked: true
  schema_version: 3
  solution: false
  task: false
---
df = pd.read_csv("../Semaine3/attributs.csv", index_col=0)
df
# standardisation
dfstd =  (df - df.mean()) / df.std()
dfstd['class'] = df['class']
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5e412381817b3618b8a7a7ca91094d61", "grade": false, "grade_id": "cell-24210bafac4b3490", "locked": true, "schema_version": 3, "solution": false, "task": false}}

On partitionne le jeu de données en ensemble de test et
d'entraînement:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 153d7ed14b1d95db0e1a369c646c7c44
  grade: false
  grade_id: cell-00b3f36097ec9704
  locked: true
  schema_version: 3
  solution: false
  task: false
---
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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "741881738d7829a3b3d62de9cceb02f2", "grade": false, "grade_id": "cell-9e3cf5dde27fbb00", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Classificateurs basés sur les exemples (*examples-based*)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "45db778c1166c64282fd7d8e20a03d1b", "grade": false, "grade_id": "cell-f7f11edbe1e13a7d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous allons maintenant voir comment appliquer des classificateurs
fournis par la librairie `scikit-learn`.  Commençons par le
classificateur plus proche voisin déjà vu en semaines 3 et 4.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "40979d861a5204582bc97eca2e359c92", "grade": false, "grade_id": "cell-28f37cb9aba3b0d6", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### KNN : $k$-plus proche voisins

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: eedf6344cb5b6474a8330504c426b4c8
  grade: false
  grade_id: cell-786fada559c8c5e0
  locked: true
  schema_version: 3
  solution: false
  task: false
---
from sklearn.neighbors import KNeighborsClassifier

#définition du classificateur, ici on l'appelle classifier
# on choisit k=1
classifier = KNeighborsClassifier(n_neighbors=1)
# on l'ajuste aux données d'entrsainement
classifier.fit(Xtrain, Ytrain) 
# on calcule ensuite le taux d'erreur lors de l'entrainement et pour le test
Ytrain_predicted = classifier.predict(Xtrain)
Ytest_predicted = classifier.predict(Xtest)
# la fonction error_rate devrait etre présente dans votre utilities.py (TP3), sinon ajoutez-la
e_tr = error_rate(Ytrain, Ytrain_predicted)
e_te = error_rate(Ytest, Ytest_predicted)

print("Classificateur: 1 Nearest Neighbor")
print("Training error:", e_tr)
print("Test error:", e_te)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "77059be22c3c54130c6b58a0a0a17ef2", "grade": false, "grade_id": "cell-4db77bd51d290099", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Quels sont les taux d'erreur pour l'ensemble
d'entraînement et l'ensemble de test ?

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "c84bc8bccecc65edc309a08bdbc00fa9", "grade": true, "grade_id": "cell-2bcc05988216d1c5", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

Le taux d'erreur pour l'ensemble d'entraînement est de $0$.
Le taux d'erreur pour l'ensemble de test est de $0.2$ soit $20$%.

+++

On mémorise ces taux dans une table `error_rates` que l'on complétera
au fur et à mesure de cette feuille:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: be4ace641636b1b069ceaaa16204f33e
  grade: false
  grade_id: cell-84331f5cb22a0f87
  locked: true
  schema_version: 3
  solution: false
  task: false
---
error_rates = pd.DataFrame([], columns=['entrainement', 'test'])
error_rates.loc["1 Nearest Neighbor",:] = [e_tr, e_te]
error_rates
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1dd2e40abcbbaec8ad5dbd190a66d33a", "grade": false, "grade_id": "cell-2034d3a7e9dbbfad", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Fenêtres de Parzen (*Parzen window* ou *radius neighbors*)

Pour ce classificateur, on ne fixe pas le nombre de voisins mais un
rayon $r$; la classe d'un élément $e$ est prédite par la classe
majoritaire parmi les éléments de l'ensemble d'entraînement dans la
sphère de centre $e$ et de rayon $r$.

**Exercice :** Complétez le code ci-dessous:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 075ee8d9c439da9d08817ef6753e3fd3
  grade: false
  grade_id: cell-64dfc640f023f84e
  locked: false
  schema_version: 3
  solution: true
  task: false
---
from sklearn.neighbors import RadiusNeighborsClassifier
classifier = RadiusNeighborsClassifier(radius=1.5)

# on l'ajuste aux données d'entrainement

classifier.fit(Xtrain, Ytrain) 

# on calcule ensuite le taux d'erreur lors de l'entrainement et pour le test

Ytrain_predicted = classifier.predict(Xtrain)
Ytest_predicted = classifier.predict(Xtest)

# on calcule les taux d'erreurs

e_tr = error_rate(Ytrain, Ytrain_predicted)
e_te = error_rate(Ytest, Ytest_predicted)

print("Classificateur: Parzen Window")
print("Training error:", e_tr)
print("Test error:", e_te)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1e18644108e320442bc0b8634f81b21e", "grade": false, "grade_id": "cell-540f1e8f9850f69f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Complétez la table `error_rates` avec ce modèle, en
rajoutant une ligne d'index `Parzen Window`.

**Indication :** Utiliser `.loc` comme ci-dessus.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 6c97291bbff6a5bfcdc72decb782bd3e
  grade: false
  grade_id: cell-4274f47e142d9ed1
  locked: false
  schema_version: 3
  solution: true
  task: false
---
error_rates.loc["Parzen Window",:] = [e_tr, e_te]
error_rates
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 94009d7f2c58ec5ad7e96258e1585d05
  grade: true
  grade_id: cell-6ac30547e91d336f
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert isinstance(error_rates, pd.DataFrame)
assert list(error_rates.columns) == ['entrainement', 'test']
assert list(error_rates.index) == ['1 Nearest Neighbor', 'Parzen Window']
assert (0 <= error_rates).all(axis=None), "Les taux d'erreurs doivent être positifs"
assert (error_rates <= 1).all(axis=None), "Les taux d'erreurs doivent être inférieur à 1"
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "efc91c583821071bd7d6708312997c0e", "grade": false, "grade_id": "cell-7ca6c7b760e2f6d3", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice $\clubsuit$ :** Faites varier le rayon $r$. Que se passe-t-il quand le rayon est grand ? petit ? Vous pouvez ajouter des modèles à la table
`error_rates` s'ils vous semblent pertinents. A quoi correspond un taux d'erreur de 0.5 ?

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "907f7d1366791fc82015fecbb1f759ed", "grade": true, "grade_id": "cell-77915ac0dc089d51", "locked": false, "points": 3, "schema_version": 3, "solution": true, "task": false}}

Lorsque le rayon $r$ de la fenêtre de Parzen est grand, le modèle peut trop généraliser, conduisant à une diminution du taux d'erreur sur l'ensemble d'entraînement mais potentiellement à une augmentation sur l'ensemble de test en ignorant les structures locales. De plus, à partir d'un certain seuil, si une catégorie est en majorité elle peut être surreprésentée lors des résultats ce qui entraîne un biais en fonction des proportions de chaque catégorie dans notre jeu de données.
En revanche, un rayon petit peut entraîner un surajustement aux données d'entraînement, augmentant le taux d'erreur sur les deux ensembles en raison d'une sensibilité excessive aux variations locales. Un taux d'erreur de 0.5 indique une performance équivalente à une prédiction aléatoire, signalant une absence de capacité discriminatoire dans le modèle.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "11aa8b1bee7bca0e0941f5be75907e9b", "grade": false, "grade_id": "cell-7474d5437867f93b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Classificateurs basés sur les attributs (*feature based*)

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7f142dd64f1cac9b6487260ca1cff01d", "grade": false, "grade_id": "cell-bc351a36f5734e8b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Régression linéaire

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b6b80b5d2c6aa80c8a5ad69b4bddf7fb", "grade": true, "grade_id": "cell-aa0635012d566877", "locked": false, "points": 1, "schema_version": 3, "solution": true, "task": false}}

**Exercice :** Pourquoi ne peut-on pas appliquer la méthode de
régression linéaire pour classer nos pommes et nos bananes ?

La régression linéaire est adaptée pour des variables dépendantes continues, tandis que les problèmes de classification impliquent des variables catégorielles. La régression logistique est préférable pour modéliser la probabilité d'appartenance à une classe dans un contexte de classification. Appliquer la régression linéaire sur un classificateur basé sur des attributs n'est pas approprié, car cela ne tient pas compte de la nature discrète des classes.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6e75b4ffc13642cda57f2610ee0b93dc", "grade": false, "grade_id": "cell-f3fe417cf16e9bb2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Arbres de décision

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ca97a3e6e5fb381ffa0cf367ac37dd72", "grade": false, "grade_id": "cell-0c0e203b37439b49", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Les arbres de décison correspondent à des modèles avec des décisions
imbriquées où chaque noeud teste une condition sur une variable.  Les
étiquettes se trouvent aux feuilles.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "65228b363cf73812186190baeb789507", "grade": false, "grade_id": "cell-da133a018c6e8417", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Complétez le code ci-dessous.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: a123282b37a47fa67ced79dab08f4543
  grade: false
  grade_id: cell-8e19513e3f66e21a
  locked: false
  schema_version: 3
  solution: true
  task: false
---
from sklearn import tree

classifier = tree.DecisionTreeClassifier()
# on l'ajuste aux données d'entrainement

classifier.fit(Xtrain, Ytrain)

# on calcule les prédictions du classifieur sur les ensembles d'entrainement et de test

Ytrain_predicted = classifier.predict(Xtrain)
Ytest_predicted = classifier.predict(Xtest)

# on calcule les taux d'erreurs

e_tr = error_rate(Ytrain, Ytrain_predicted)
e_te = error_rate(Ytest, Ytest_predicted)

print("Classificateur: Arbre de decision")
print("Training error:", e_tr)
print("Test error:", e_te)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7349afd1535a78ef980d8f6760875d5d", "grade": false, "grade_id": "cell-d818ab75031ccf3c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Complétez la table `error_rates` avec ce modèle.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 54e602f2d585ff5dfc81c09fa54777d2
  grade: false
  grade_id: cell-b2218cbf456bd91c
  locked: false
  schema_version: 3
  solution: true
  task: false
---
error_rates.loc["Arbre de decision",:] = [e_tr, e_te]
print(error_rates)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 33f0ea85f8cee192d6dc5c287456f00a
  grade: true
  grade_id: cell-57894376c13e530a
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
tags: []
---
assert isinstance(error_rates, pd.DataFrame)
assert list(error_rates.columns) == ['entrainement', 'test']
assert error_rates.shape[0] >= 3
assert (0 <= error_rates).all(axis=None), "Les taux d'erreurs doivent être positifs"
assert (error_rates <= 1).all(axis=None), "Les taux d'erreurs doivent être inférieur à 1"
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4fa7e91b5a9e8184312ecfe62340a032", "grade": false, "grade_id": "cell-f1f775a2ccb77c41", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Représentez l'arbre de décision comme vu lors du CM5.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: ab4ebccfd10bfb3b26cd7a85e24a3e5e
  grade: true
  grade_id: cell-e4ce3f1406e9fe61
  locked: false
  points: 1
  schema_version: 3
  solution: true
  task: false
tags: []
---
import matplotlib.pyplot as plt

plt.figure(figsize=(12,12)) 
tree.plot_tree(classifier, fontsize=10)
plt.show()
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "13ee0f12287d5da70c3db74deb623101", "grade": true, "grade_id": "cell-316a87fad1287712", "locked": false, "points": 2, "schema_version": 3, "solution": true, "task": false}}

**Exercice :** Interprétez cette figure. Combien de critère(s) ont été pris en compte pour séparer les pommes des bananes ?  Quel est le premier critère (attribut et valeur seuil) de séparation des échantillons ? Que signifie une mesure de gini à 0.0 ?

Un seul critère a été pris en compte pour séparer les pommes des bananes, il s'agit de x[1], à savoir l'élongation. Le seuil de séparation des échantillons est de $-0.192$.
Le gini est la mesure de l'impureté du jeu de données. Une mesure de gini à 0.0 signifie qu'il y a une égalité parfaite entre toutes les données de notre jeu.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4d130da1537149b2d938f87bb679c7c1", "grade": false, "grade_id": "cell-ff5d2dccfd4a6505", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Perceptron

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e493f04249e130eb23a4e0d6b7f05a98", "grade": false, "grade_id": "cell-e4a08d06646c875e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Le perceptron est un réseau de neurones artificiels à une seule couche
et donc avec une capacité de modélisation limitée; pour le problème
qui nous intéresse cela est suffisant. Pour plus de détails, revenez
au [cours](CM5.md)

**Exercice :** Complétez le code ci-dessous, où l'on définit un modèle
de type `Perceptron` avec comme paramètres $10^{-3}$ pour la tolérence, $36$ pour l'état aléatoire (*random state*) et 100 époques (*max_iter*)

```{code-cell} ipython3
---
deletable: false
editable: true
nbgrader:
  cell_type: code
  checksum: 1616f84f831b6981890b007c5c53afe7
  grade: false
  grade_id: cell-c6bfeee5a4a966cc
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
tags: []
---
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
print("Test error:", e_te)
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9976c26d3d2c1e44c76a11b3d7d6b95a", "grade": true, "grade_id": "cell-f8994015ecc492d3", "locked": false, "points": 1, "schema_version": 3, "solution": true, "task": false}}

**Exercice :** Lisez la documentation de `Perceptron`. À quoi
correspond le paramètre `random_state` ?

Le paramètre `random_state` dans la documentation du `Perceptron` contrôle l'initialisation aléatoire des poids du modèle. En fixant une valeur spécifique, on assure la reproductibilité des résultats entre différentes exécutions. Cela est utile pour garantir la cohérence des expérimentations et des validations du modèle.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 6c06d000995285781775ef088b2f0bfb
  grade: false
  grade_id: cell-4f0cec434737cda7
  locked: false
  schema_version: 3
  solution: true
  task: false
---
Perceptron?
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4913e916d7d45477247b2487260702b3", "grade": false, "grade_id": "cell-65470533b4335e5a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Complétez la table `error_rates` avec ce modèle.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: a71a5f08c8bdf5f6e2efee8d4768eea4
  grade: false
  grade_id: cell-cfe370c6b70f6d27
  locked: false
  schema_version: 3
  solution: true
  task: false
---
error_rates.loc["Perceptron",:] = [e_tr, e_te]
error_rates
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 49ed7a76afdf1c5075ac8514f69c24b5
  grade: true
  grade_id: cell-b72fa191a2a82889
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert error_rates.shape[0] >= 4
assert error_rates.shape[1] == 2
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "80d4edc5a25b3393f6278c3563c15406", "grade": false, "grade_id": "cell-b546e3375477b608", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## $\clubsuit$ Points bonus : construction du classificateur «une règle» (*One Rule*)

Faites cette partie ou bien passez directement à la conclusion.

En complétant le code ci-dessous, créez votre premier classificateur
qui:
* sélectionne le "bon" attribut (rougeur ou élongation pour le
  problème des pommes/bananes), appelé $G$ (pour *good*). C'est
  l'attribut qui est le plus corrélé (en valeur absolue, toujours !)
  aux valeurs cibles $y = ± 1$;
* détermine une valeur seuil (*threshold*);
* utilise l'attribut `G` et le seuil pour prédire la classe des éléments.
        
Un canevas de la classe `OneRule` est fournit dans la fichier
`utilities.py`; vous pouvez le compléter ou bien la programmer
entièrement vous même.

Ce classificateur est-il basé sur les attributs ou sur les exemples?

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: e10fefacfc33dd0acf640372d2790081
  grade: false
  grade_id: cell-f300c99cf16ddefb
  locked: true
  schema_version: 3
  solution: false
  task: false
tags: []
---
from utilities_cours_correction import *
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 9f7385d47625cbe5517b632691a023d4
  grade: false
  grade_id: cell-b72b2907842cb7fb
  locked: true
  schema_version: 3
  solution: false
  task: false
---
# Use this code to test your classifier
classifier = OneRule()
classifier.fit(Xtrain, Ytrain) 
Ytrain_predicted = classifier.predict(Xtrain)
Ytest_predicted = classifier.predict(Xtest)
e_tr = error_rate(Ytrain, Ytrain_predicted)
e_te = error_rate(Ytest, Ytest_predicted)
print("Classificateur: One rule")
print("Training error:", e_tr)
print("Test error:", e_te)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "63825ae948ab016d3e3be1b480b0c325", "grade": false, "grade_id": "cell-472a8c23ef803ec9", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Complétez la table `error_rates` avec ce modèle.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 48da8b079dc5d00daf3aa8b11b312858
  grade: true
  grade_id: cell-7b189e436af168e3
  locked: false
  points: 3
  schema_version: 3
  solution: true
  task: false
---
error_rates.loc["One rule",:] = [e_tr, e_te]
print(error_rates)
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: d9cc4e307aa25ea9db7429b85c63e193
  grade: true
  grade_id: cell-14c847f98a88a373
  locked: true
  points: 0
  schema_version: 3
  solution: false
  task: false
---
assert error_rates.shape[0] >= 5
assert error_rates.shape[1] == 2
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 9eac0c359d449ad1c0026e38854320af
  grade: false
  grade_id: cell-587a9581023e668d
  locked: true
  schema_version: 3
  solution: false
  task: false
---
# On charge les images
dataset_dir = os.path.join(data.dir, 'ApplesAndBananasSimple')
images = load_images(dataset_dir, "*.png")
# This is what you get as decision boundary.
# The training examples are shown as white circles and the test examples are blue squares.
make_scatter_plot(X, images.apply(transparent_background_filter),
                  [], test_index, 
                  predicted_labels='GroundTruth',
                  feat = classifier.attribute, theta=classifier.theta, axis='square')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e9f6c1a409234b6d29ce5f38de89a7bf", "grade": false, "grade_id": "cell-1b8779ac28a26c59", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Comparez avec ce que vous auriez obtenu en utilisant les 2 attributs avec le même poids lors de la décision de classe.

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 5f6db3de94731a2fbf4749d55449b82f
  grade: false
  grade_id: cell-d0e8bd2a9132fea6
  locked: true
  schema_version: 3
  solution: false
  task: false
---
make_scatter_plot(X, images.apply(transparent_background_filter),
                  [], test_index, 
                  predicted_labels='GroundTruth',
                  show_diag=True, axis='square')
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8db48dc81f852cf17c594ed3396acf42", "grade": false, "grade_id": "cell-28e6ef8e4fa12a3c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Conclusion

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5100cb76750f75f261150a575aaf1019", "grade": false, "grade_id": "cell-1b50f7767c53d39b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice :** Comparez les taux d'erreur de vos différents
classificateurs, lors de l'entraînement et du test et pour le problème
des pommes et des bananes. 

**Indications:**
- Vous commencerez par *observer* les différents taux d'erreurs d'entrainement et d'apprentissage de vos classificateurs.
- Vous interpréterez le résultat en expliquant quel est le meilleur classificateur pour les pommes/bananes.

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e547d4f47e160f74d5df32a060f61b3a", "grade": true, "grade_id": "cell-a326ec80e8758fb8", "locked": false, "points": 2, "schema_version": 3, "solution": true, "task": false}}

Le classificateur "Perceptron" affiche la meilleure performance avec une erreur de seulement $0.1$ sur l'ensemble de test, indiquant une excellente capacité de généralisation.
Les classificateurs "1 Nearest Neighbor" et "Parzen Window" montrent une performance parfaite sur l'ensemble d'entraînement, mais une erreur de $0.2$ sur l'ensemble de test, suggérant une sensibilité aux nouvelles données.
L'arbre de décision présente des résultats similaires à "1 Nearest Neighbor" et "Parzen Window", suggérant une possible tendance au surajustement.
Malgré une performance parfaite sur l'ensemble d'entraînement, le classificateur "One Rule" montre une erreur de 0.2 sur l'ensemble de test, indiquant des limitations dans la généralisation.
En considérant la capacité à généraliser et les taux d'erreur, le "Perceptron" se démarque comme le choix préférentiel pour la classification des pommes et des bananes.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "623cd73082a3b65a692ad8b02da7e0ba", "grade": false, "grade_id": "cell-466bf7addb6e465a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Dans cette feuille vous avez découvert comment utiliser un certain
nombre de classificateurs, voire comment implanter le vôtre, et
comment jouer sur les paramètres de ces classificateurs (par exemple
la tolérance du perceptron ou le nombre de voisins du KNN) pour
essayer d'optimiser leur performance.

Mettez à jour votre rapport et déposez votre travail.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3e3d916a7c8ce54f4dc14284f4de3fc4", "grade": false, "grade_id": "cell-466bf7addb6e465b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Vous êtes maintenant prêts pour revenir à votre [analyse de
données](4_analyse_de_donnees.md) pour mettre en œuvre ces
classificateurs sur votre jeu de données.

**Dans le projet 1, on vous demande de choisir un seul classificateur,
ainsi que ses paramètres**.  Nous verrons dans la seconde partie de
l'UE comment comparer systématiquement les classificateurs.
