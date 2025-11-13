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

+++ {"editable": true, "slideshow": {"slide_type": "slide"}}

<center>

# Cours: Initiation à la Science des données
## Analyses de données

</center>

<br>

<center>Fanny Pouyet</center>

<center>L1 Informatique</center>

<center>Semestre 2</center>

+++ {"editable": true, "slideshow": {"slide_type": "slide"}}

**La semaine dernière**

* Définition et objectif de la science des données
* Introduction à la bibliothèque `Pandas` et `Numpy`

**Cette semaine**

* Présentation de plus de tests statistiques
* Visualisation des données
* Analyse de données
* Modélisation avec un Modèles linéaires généralisés (GLM)
* Bibliothèques `Matplotlib` et `Seaborn`

+++ {"editable": true, "slideshow": {"slide_type": "slide"}}

## Contexte

Dans ce cours, nous utiliserons l'exemple du jeu de données du Titanic, un énorme paquebot pour l'époque qui fait naufrage en 1912 à la suite d'une collision avec un iceberg, lors de son voyage inaugural de Southampton à New York.

* Nous avons accès à des informations sur une partie des passagers (891 passagers) du Titanic. 
* *Pourquoi certains passagers ont survécu et d'autres sont morts?*
* Commencons l'analyse de données


```{image} media/titanic.jpeg
:alt: source :https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqRekfGrFFbNX1LxVcw5uy_kPRMBJfSvz9cA&usqp=CAU
:class: bg-primary
:width: 400px
:align: center
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}}

## Chargement des données

Les données sont dans un tableau au format CSV (*comma separated values*):

```{code-cell} ipython3
---
editable: true
jupyterlab-deck:
  layer: fragment
slideshow:
  slide_type: ''
---
import pandas as pd
import numpy as np
 
titanic = pd.read_csv("media/titanic.csv")
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}}

Ensuite, on **OBSERVE** ce qu'on a!!

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
titanic.head(10)
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
titanic.shape
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
titanic.describe(include='all')
```

+++ {"slideshow": {"slide_type": "slide"}}

Les colonnes sont:
* *PassengerId* : Identifiant du passager
* *Survived* : True (1) / False (0)
* *Pclass* : Classe du ticket : 1, 2 ou 3.
* *Name* : Nom du passager
* *Sex* : Genre du passager (male/female)
* *Age* : Age en années
* *Cabin* : Numéro de cabine
* *Embarked* : Port d'embarquement ( *C* : Cherbourg; *Q* Queenstown; *S* Southampton)

+++ {"slideshow": {"slide_type": "slide"}}

## Question / objectif

**Pourquoi certains passagers ont survécu et d'autres sont morts?**

+++ {"editable": true, "slideshow": {"slide_type": "fragment"}}

On veut trouver les colonnes qui expliquent le 0/1 dans `Survived` et construire un modèle qui permettrait d'expliquer au mieux `Survived` étant donné nos informations.

* On va commencer par **observer nos données**, en répondant à  des questions descriptives:

+++ {"editable": true, "slideshow": {"slide_type": "fragment"}}

    1. Quel sexe a le plus de chances de survie ?
    2. Est-ce que les enfants ont eu plus de chances de survie ?
    3. Quelle est la proportion de survie selon le port d'embarquement ?

+++ {"editable": true, "slideshow": {"slide_type": "slide"}}

### Quel sexe a le plus de chances de survie ?

1. Comparaison de la proportion d'hommes et de femmes *passagers du Titanic*
2. *qui ont survécu*

+++

Utilisons `groupby`, qui permet de produire des tables de synthèses par catégories:

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
titanic.groupby(['Sex','Survived']).count()['PassengerId']
```

+++ {"slideshow": {"slide_type": "slide"}}

**Autres tables de synthèse**

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
passengers = titanic.groupby('Sex')['PassengerId'].count()
passengers
```

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
survivors = titanic.groupby('Sex')['Survived'].sum()
#pourquoi j'utilise sum() et pas count() ?
survivors
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: fragment
---
summary = pd.DataFrame({"Survivants": survivors,
                        "Passagers": passengers,
                        "%": round(100*survivors / passengers,1)})
summary
```

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
#Et au total ?
titanic['Survived'].sum() / titanic['PassengerId'].count()
```

+++ {"slideshow": {"slide_type": "slide"}}

**Visualisation**

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
import matplotlib.pyplot as plt
#Ici je représente un barplot car on a des catégories
 
```

+++ {"slideshow": {"slide_type": "fragment"}}

Le même graphique, avec titre et labels:

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
summary[["Survivants", "Passagers"]].plot(kind='bar');
plt.xlabel('Sexe')
plt.ylabel('Total')
plt.title('Comparaison de la survie selon le sexe');
```

+++ {"slideshow": {"slide_type": "slide"}}

**Conclusions**

* *Observation* : 
    * 38% des passengers ont survécus et plus précisément 74% des femmes contre seulement 19% des hommes
    * Il y a plus d'hommes que de femmes sur le paquebot
    
* *Interprétation* : Les femmes ont eu plus de chances de survivre que les hommes

Pour aller plus loin, on pourrait regarder à quel âge les hommes et femmes avaient la plus grande chance de survie.

+++ {"slideshow": {"slide_type": "slide"}}

### Est-ce que les enfants ont eu plus de chances de survie ?

* On va commencer par séparer les enfants des adultes selon l'age. Problème, on a des données manquantes.

#### Gestion des données manquantes

Il manque certaines informations. Que feriez-vous ?

On pourrait décider de supprimer les individus sans informations sur l'âge (**pensez à vérifier les dimensions de votre table!**)

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
print("Si j'enlève toutes les lignes contenant un 'NaN': ", titanic.dropna().shape)
print("\nSi je n'enlève que les 'NaN' de la colonne Age : ", titanic.loc[titanic['Age'].notna(),:].shape)
```

+++ {"slideshow": {"slide_type": "slide"}}

Maintenant on va créer une nouvelle colonne indiquant si l'on est adulte:

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
titanic['Adult'] = titanic['Age'] >=18  
titanic.head()
```

+++ {"slideshow": {"slide_type": "fragment"}}

Et *quid* des individus dont on ne connait pas l'âge ?

```{code-cell} ipython3
titanic.head(n=6)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
titanic_filt_age = titanic.loc[titanic['Age'].notna(),:]
passengers = titanic_filt_age.groupby(['Adult','Sex']).count()['PassengerId']
passengers
```

+++ {"slideshow": {"slide_type": "fragment"}}

Il y a sur le bateau:
* 55 enfants de sexe féminin
* 58 enfants masculin
* 206 adultes femmes
* 395 adultes hommes

Quid des survivant.es ?

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
survivors = titanic_filt_age.groupby(['Adult','Sex'])['Survived'].sum()
survivors
```

+++ {"slideshow": {"slide_type": "slide"}}

### Résumons et visualisons

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
passengers = titanic_filt_age.groupby(['Adult','Sex'])['PassengerId'].count()
summary = pd.DataFrame({"Survivants": survivors,
                       "Passagers": passengers,
                       "%": round(survivors/passengers*100, 1)})
summary.index=['Girl','Boy','Woman','Man']
summary
```

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
#On représente ici un barplot car on a des catégories
summary.plot(kind='bar')
plt.xlabel("Personnes classées selon l'age et le sexe")
plt.ylabel('Total')
plt.title("Comparaison de la survie selon l'age et le sexe");
```

+++ {"slideshow": {"slide_type": "slide"}}

**Conclusions**

* *Observations*:

    * Il y a plus d'adultes que d'enfants.
    * Ainsi, on a respectivement 69%, 40%, 77% et 18% de survivant-es parmi les filles, garcons, femmes et hommes. 
    
    
* *Interprétation*: 

    Quelque soit la catégorie, les personnes de sexe féminin ont une plus grande chance de survie que les masculins. Les enfants de sexe masculin ont une plus grande chance de survie que les adultes mais ce n'est pas réciproque pour les personnes de sexe féminin. Pour aller plus loin, que pourrions nous regarder ?

+++ {"slideshow": {"slide_type": "slide"}}

### Calculer la proportion de survie selon le port d'embarquement

La colonne du port d'embarquement à des valeurs manquantes (889 disponibles/891). Comme la plupart des passagers et passagères sont montées à Southampton, on peut supposer que les données manquantes viennent de là. 

*Attention ceci est un choix. Toujours garder en tête qu'il modifie vos résultats et peut donc modifier vos interpétations ! Ici, c'est vraiment à la marge*

```{code-cell} ipython3
titanic["Embarked"] = titanic["Embarked"].fillna('S')
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
survivors_per_port = titanic.groupby('Embarked')['Survived'].sum()
passengers_per_port = titanic.groupby('Embarked')['PassengerId'].count()
comparaison_port_survie = pd.DataFrame({"Survivants": survivors_per_port,
                                        "Passagers": passengers_per_port,
                                        "%": round(survivors_per_port/passengers_per_port*100, 1)})
comparaison_port_survie
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
comparaison_port_survie.plot(kind='bar')
plt.xlabel("Port d'Embarquement")
plt.ylabel("Nombre d'individus")
plt.title('Comparaison de survie selon le port')
```

+++ {"slideshow": {"slide_type": "slide"}}

La figure indique que:
- la plupart des individus sont montés à Southampton puis Cherbourg puis Queenstown.
- le nombre de survivants et survivantes est plus grand selon le meme ordre.
- Respectivement 219/646; 93/168 et 30/77 ont survécus selon le port d'embarquement Southampton, Cherbourg, Queenstown.
- L'analyse de proportionnalité nous informe que les individus étant montés à Cherbourg ont eu plus de chance de survie. Pourquoi cela ?

+++ {"slideshow": {"slide_type": "slide"}}

## C'est quoi la corrélation ? Et la causalité ?

Il existe trois types de relations statistiques:
- *corrélation positive*: si une variable augmente, l'autre aussi.
- *corrélation négative*: si une variable augmente, l'autre diminue.
- *absence de corrélation*: si une variable augmente, l'autre peut ou pas varier sans lien entre elle.

Exemple de corrélation:

```{image} media/correlationChocolatNobels.png
:alt: Chocolat et Prix Nobels
:class: bg-primary
:width: 500px
:align: center
```

+++ {"slideshow": {"slide_type": "slide"}}

Cette corrélation est tirée d'un papier de 2012 par F. Messerli.

C. Pissarides, prix Nobel d'économie en 2010 suite à ce papier à commenté:

"To win a Nobel Prize you have to produce something that others haven't thought about - chocolate that makes you feel good might contribute a little bit. Of course it's not the main factor but... anything that contributes to a better life and a better outlook in your life then contributes to the quality of your work."


1. Décrivez la figure
2. Qu'est-ce qu'on observe?
3. Qu'en conclut-on?

+++ {"slideshow": {"slide_type": "slide"}}

Depuis, il a été montré que la **corrélation positive** est due à la richesse économique (economic wealth). 

Alors qu'est ce que **la causalité** ? 

Dans notre exemple, la richesse économique *implique*
* une plus grande dépense en recherche 
* ce qui *implique* une corrélation positive avec le nombre de prix Nobel. 

Par ailleurs et *indépendamment*, la richesse économique *implique* :
* de plus grandes dépenses dans les produits de luxe, dont le chocolat.

+++ {"slideshow": {"slide_type": "slide"}}

### Causalité n'est pas corrélation

1. Les corrélations relèvent de l'**observation**;

2. Les causalités relèvent de l'**interprétation** !

+++ {"slideshow": {"slide_type": "slide"}}

♣ Pour vous montrer par l'exemple que correlation ne veut pas dire causalité, faites un tour ici: 

<https://www.tylervigen.com/spurious-correlations>

<https://www.lemonde.fr/les-decodeurs/article/2019/01/02/correlation-ou-causalite-brillez-en-societe-avec-notre-generateur-aleatoire-de-comparaisons-absurdes_5404286_4355770.html>


Pour comprendre les biais d'interprétation induits par les représentations graphiques faites un tour là:

<https://www.lemonde.fr/les-decodeurs/article/2018/05/22/sept-conseils-pour-ne-pas-se-faire-avoir-par-les-representations-graphiques_5302680_4355770.html>

+++ {"slideshow": {"slide_type": "slide"}}

Retour au port d'embarquement. Pourquoi on survit plus si on a embarqué a Cherbourg ?

+++ {"slideshow": {"slide_type": "fragment"}}

**Hypothèse 1**: Il y a plus de femmes à Cherbourg (?)

**Hypothèse 2**: On est plus riche à Cherbourg et plus on est riche plus on a survécu (?)

+++ {"slideshow": {"slide_type": "slide"}}

**Hypothèse 1:** Il y a plus de femmes à Cherbourg

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
female_per_port = titanic[titanic['Sex']=='female'].groupby('Embarked')['PassengerId'].count()
male_per_port = titanic[titanic['Sex']=='male'].groupby('Embarked')['PassengerId'].count()
pd.DataFrame({"Female": female_per_port,
              "Male" : male_per_port,
              "Total": passengers_per_port,
              "% Female": female_per_port / passengers_per_port
              })
```

+++ {"slideshow": {"slide_type": "fragment"}}

Il n'y a pas plus d'individus féminins à Cherbourg qu'à Queenstown.

+++ {"slideshow": {"slide_type": "slide"}}

**Hypothèse 2**: on est plus riche à Cherbourg et plus on est riche plus on a survécu (?)

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
survivors_per_class = titanic.groupby('Pclass')['Survived'].sum()
passengers_per_class = titanic['Pclass'].value_counts()
pd.DataFrame({"Survivants": survivors_per_class,
              "Passagers": passengers_per_class,
              "%": round(survivors_per_class/passengers_per_class*100, 1)})
```

+++ {"slideshow": {"slide_type": "fragment"}}

Il y a une nette corrélation entre la classe et la probabilité de survie!

+++ {"slideshow": {"slide_type": "fragment"}}

On peut même l'expliquer causalement !

+++

Regardons la répartition entre classes, selon le port d'embarquement

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
pclass1_per_port = titanic[titanic['Pclass']==1].groupby('Embarked')['PassengerId'].count()
pclass2_per_port = titanic[titanic['Pclass']==2].groupby('Embarked')['PassengerId'].count()
pclass3_per_port = titanic[titanic['Pclass']==3].groupby('Embarked')['PassengerId'].count()


pd.DataFrame({'Classe 1': pclass1_per_port,
              'Classe 2': pclass2_per_port,
              'Classe 3': pclass3_per_port,
              'Passengers': passengers_per_port,
              '% Classe 1': round(pclass1_per_port/passengers_per_port*100,1)})
```

+++ {"slideshow": {"slide_type": "fragment"}}

**Observations**

* Les passagers ayant embarqué à Cherbourg regroupent principalement des individus de première classe.
* Les 77 passagers qui embarquent à Queenstown (Irlande) sont principalement de la classe 3 des migrants en route vers les États-Unis.

+++ {"slideshow": {"slide_type": "slide"}}

**Conclusions**
- Les passagers ayant embarqué à Cherbourg arrivent de Paris (France) et sont plutôt riches.
- Les 77 passagers qui embarquent à Queenstown (Irlande) sont principalement des migrants en route vers les États-Unis. 
- Il semble que la classe plus que le port d'embarquement a une relation de causalité avec la survie (à vérifier).

+++ {"slideshow": {"slide_type": "slide"}}

### Corrélation (point mathématique)

Le coefficient de [corrélation linéaire de Pearson](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient) se calcule facilement en python . Il correspond à la version normalisée de l'écart-type par la standard deviation (écart-type) de la covariance. 

Mathématiquement, on a: $\rho_{xy} = \frac{\sigma_{xy}}{\sigma_x\sigma_y}$

$\rho_{xy}$ varie entre -1 et 1 et représente la force de la relation linéaire qui existe entre les 2 vecteurs/séries.

* 0 : pas de corrélation
* 1 : corrélation positive parfaite (si on connait $x$ alors on peut déduire $y$, les points sont alignés le long d'une droite)
* -1: corrélation négative parfaite (idem)
* en réalité, on a souvent des corrélations intermédiaires

+++ {"slideshow": {"slide_type": "slide"}}

"The intention of this contribution was to show that the correlation between chocolate consumption per capita and the number of Nobel laureates per capita (as reported by Messerli, 2012) will vanish if one controls for relevant other variables and if one uses a sophisticated estimation technique." par Prinz A. L. (2020)

```{image} media/correlationsChocolat.jpeg
:alt: Chocolat et autres
:class: bg-primary
:width: 900px
:align: center
```

+++ {"slideshow": {"slide_type": "slide"}}

On peut calculer la **matrice de corrélation** qui correspond à la corrélation entre les colonnes d'une table,
et utiliser une **carte de chaleur** (*heatmap* en anglais) pour mieux la visualiser:

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
titanic_cor = titanic.corr(numeric_only=True)
titanic_cor.style.background_gradient(cmap='coolwarm', axis=None)
#remarque on ne peut pas calculer de correlation linéaire 
#avec des données ayant plus de 2 catégories comme le port d'embarquement
# il faudrait faire une ANOVA (hors programme)
```

+++ {"slideshow": {"slide_type": "fragment"}}

**Attention**: par défaut, pour attribuer des couleurs aux nombres dans une carte de chaleur,
`Pandas` applique une standardisation par colonne. Le `axis=None` assure que la
normalisation est appliquée à l'ensemble des valeurs de la table.

+++ {"slideshow": {"slide_type": "fragment"}}

Variante, avec `Seaborn`:

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
import seaborn as sns

sns.heatmap(titanic_cor, fmt='0.2f', annot=True, square=True);
```

+++ {"slideshow": {"slide_type": "slide"}}

Représentation des données à l'aide de pair plots.

* On a un aperçu rapide en une seule ligne de code
* En diagonale, la distribution des valeurs de la colonne selon un histogramme
* Pour le reste, des scatter plots (un point = une case)
* Mais c'est lourd et lent. Ça ne marche pas avec un gros jeu de données
* Tout n'est pas intéressant...

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
sns.pairplot(titanic, hue="Survived", diag_kind="hist", vars=['Sex','Age','Embarked','Pclass'])
```

+++ {"slideshow": {"slide_type": "slide"}}

## Et maintenant ?

On peut proposer un modèle d'explication de nos données.

+++ {"slideshow": {"slide_type": "fragment"}}

### Modèles linéaires

Un modèle linéaire permet d'exprimer une variable aléatoire (notée
$Y$) en fonction d'une combinaison linéaire des variables explicatives
($X$) :

$$Y = AX + B \,,$$

où $A$ est une matrice de paramètres à estimer et $B$ est une matrice
contenant le *bruit* (ce que l'on n'arrive pas à expliquer).

**Ajuster** le modèle (*fit*) à des données revient à rechercher la
combinaison linéaire $A$ qui minimise le bruit $B$ sur ces données.

Une fois ajusté, le modèle peut être utilisé pour **estimer** $Y$ pour
d'autres valeurs de $X$.

+++ {"slideshow": {"slide_type": "slide"}}

### Modèles Linéaires Généralisés (GLM)

Lorsque les variables ne sont pas continues la regression linéaire
n'est pas possible. Rappelez vous les problèmes de visualisation avec
nos pair plots.

Les **modèles linéaires généralisés** sont des modèles qui permettent
de prendre en compte tous types de variables -- comme `PClass`, `Sex`
ou `Embarked` qui prennent un nombre restreint de valeurs.

Le prix à payer est de la complexité supplémentaire: ce n'est plus $Y$ qui est estimée par une
combinaison linéaire des variables explicatives, mais $g(Y)$ où $g$
est une fonction de lien. Il faut aussi spécifier une famille qui
indique le type de loi de distribution des variables.

Dans ce cours, nous utiliserons ces modèles un peu comme des boîtes noires.

+++ {"slideshow": {"slide_type": "slide"}}

### Étapes d'utilisation d'un modèle linéaire généralisé

1. Construction du modèle avec `glm()`:
    1. Un modèle
    2. Des données
    3. Une famille de regression (ici binomiale)

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
import statsmodels.formula.api as smf
import statsmodels.api as sm
frm = "Survived ~  C(Pclass) + C(Sex) + Age + C(Embarked)"
model = smf.glm(formula = frm, data = titanic_filt_age, family=sm.families.Binomial())
```

+++ {"slideshow": {"slide_type": "fragment"}}

2. Ajustement du modèle aux données avec `.fit()`

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
result = model.fit()
```

+++ {"slideshow": {"slide_type": "fragment"}}

3. Description du modèle ajusté avec `.summary()`

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
result.summary()
```

+++ {"slideshow": {"slide_type": "fragment"}}

4. Observation des p-values

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
result.pvalues[result.pvalues < (0.05/6)]
# le 6 vient de la correction de Bonnferroni
```

+++ {"slideshow": {"slide_type": "slide"}}

### Que sont les p-values ?

La **p-value** est la probabilité d'obtenir au moins la même valeur
(ici, *z*) alors qu'on est sous l'hypothèse nulle.

L'**hypothèse nulle** est une notion indispensable: elle permet
d'effectuer des *tests statistiques*. Si on veut montrer que des
nombres sont différents, l'hypothèse nulle correspond à l'hypothèse
que les deux nombres sont égaux ("nulle" se lit dans le sens "pas de
différence").

Fisher en étudiant la relation entre la taille des enfants et de leurs parents, a introduit le concept de p-value. On ne peut jamais accepter l'hypothèse nulle (les enfants font en moyenne la même taille que leurs parents) mais on peut la rejeter si la p-value est suffisamment faible (on est sûr que les enfants ne font pas la même taille que leurs parents en moyenne). La p-value mesure *grosso modo* à quel point les données plaident contre l'hypothèse nulle.


```{image} media/pvalue.png
:alt: source: https://www.gigacalculator.com/articles/p-value-definition-and-interpretation-in-statistics/
:class: bg-primary
:width: 400px
:align: center
```

+++ {"slideshow": {"slide_type": "slide"}}

## Conclusions

* **Initiation à la science des données**
    * l'observation est primordiale, l'interprétation vient après
    * les modèles linéaires ne sont parfois pas suffisant

+++ {"slideshow": {"slide_type": "slide"}}

* **Langage Python 3**
    * `Pandas`, pour la structuration et la manipulation de tables
    * `Numpy`, pour les calculs scientifiques
    * `MatplotLib`, pour la visualisation de base (lib la plus utilisée)
    * `Seaborn`, pour la visualisation de graphiques statistiques. S'utilise entre autres avec des objets `Pandas`.
    * (`Statsmodels`, pour faire un modèle)

+++ {"slideshow": {"slide_type": "slide"}}

## Perspectives

* **TP 2**
    * Utilisation de `Pandas`, `Numpy`, `Matplotlib` et `Seaborn`
    * Un autre jeu de données
    * Travail en binome
    * TP noté

+++ {"slideshow": {"slide_type": "slide"}}

* **CM 3 : analyse de données et classification d'images**
    * Chaine d'analyse des données entière: VI-ME-RE-BAR
    * Interprétation des résultats
