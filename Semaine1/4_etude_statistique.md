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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "eaca0ec6c9ac70c67bb8c9aeb43a015f", "grade": false, "grade_id": "cell-63247b06949c9808", "locked": true, "schema_version": 3, "solution": false}}

# Une première étude statistique

## Introduction

Le monde étant complexe, nous construisons constamment -- consciemment
ou non -- des **modèles** pour le simplifier, afin d'émettre des
questions et valider des **hypothèses** qui vont ensuite guider nos
décisions et nos actes. Par exemple, pour lutter contre les
discriminations de genre, d'origine, d'âge, on catalogue la population
entre hommes et femmes, habitants des villes, des banlieues ou des
campagnes, nationaux et étrangers, jeunes et vieux, pour étudier des
questions comme «y-a-t'il discrimination entre X et Y?», afin de
prendre des mesures adéquates.

Un des rôles de la statistique en général et de la sciences des
données en particulier est de formaliser ce processus afin d'exercer
un regard critique sur toute la chaîne. Regard critique essentiel car,
comme chacun sait, «il y a les petits mensonges, les gros mensonges, et
les statistiques»: entre modèles trop-simplifiés (par exemple la
classification non inclusive homme/femme) et biais en tous genres, il
n'est que trop facile de faire dire (volontairement ou non) n'importe
quoi. Pour interpréter un résultat statistique, il est essentiel de
connaître tout le contexte (réalité terrain, données, modèle, ...) qui
a amené à son calcul.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7d18717a4812d76c46a9cf11bd541864", "grade": false, "grade_id": "cell-63247b06949c9806", "locked": true, "schema_version": 3, "solution": false}}

Dans cette feuille, nous allons illustrer sur un exemple comment on
peut étudier une question et tenter d'y répondre en mettant en action
la démarche statistique. Nous nous appuyons sur un exemple tiré du
cours Data 8 de
[sélection du jury d'assise pour les procès de crimes](https://www.inferentialthinking.com/chapters/11/1/Assessing_a_Model.html).
Cet exemple est inspiré par des études statistiques réalisées dans le
contexte de la lutte pour les droits civiques aux États-Unis (voir par
exemple
[U.S. Supreme Court, 1965: Swain vs. Alabama](https://en.wikipedia.org/wiki/Swain_v._Alabama))
et prend une actualité toute particulière avec le procès en cours
suite à la mort de Georges Floyd et plus généralement le mouvement
«Black Lives Matter».

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bdfa777321d7c25e0895b79e75e0f03f", "grade": false, "grade_id": "cell-08ccbe42dc086995", "locked": true, "schema_version": 3, "solution": false, "task": false}}

<div class="alert alert-warning">

Ce sont des sujets importants et très sensibles; la plus grande
prudence doit être observée dans l'interprétation des résultats.
Voir notamment [le préambule de l'exemple](https://www.inferentialthinking.com/chapters/11/1/Assessing_a_Model.html)
dans le cours Data 8.

</div>

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "39cbc64e2d83d726327897ff7b6ce1ac", "grade": false, "grade_id": "cell-63247b06949c9807", "locked": true, "schema_version": 3, "solution": false}}

## De l'impartialité des jurys d'assise

Le point de départ est l'amendement suivant de la constitution
américaine qui encadre la composition des jurys populaires dans
l'équivalent de nos cours d'assise où l'on juge des crimes:

> «Amendment VI of the United States Constitution states that, "In all
> criminal prosecutions, the accused shall enjoy the right to a speedy
> and public trial, by an impartial jury of the State and district
> wherein the crime shall have been committed." One characteristic of
> an impartial jury is that it should be selected from a jury panel
> that is representative of the population of the relevant region. The
> jury panel is the group of people from which jurors are selected.»

Nous traduirons librement «jury panel» par «présélection de jurés».

La question de savoir si une présélection de jurés est
représentative de la population de la région, a une implication légale
importante: on pourrait en effet remettre en cause l'impartialité du
jury si un groupe de la population était systématiquement
sous-représenté dans cette présélection.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "460b138f3bb33a9990b277b430148689", "grade": false, "grade_id": "cell-e5f1ccb7c7d42270", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### La question étudiée

Prenons par exemple une région hypothétique dont la population serait
répartie en deux groupes A et B (par exemple habitants des villes ou des
campagnes). Disons que 26% des jurés potentiels sont dans A. Supposons
de plus que, à l'occasion d'un procès donné, une présélection $P$ de
cent jurés ait été faite dans laquelle seuls huit membres sont dans A,
soit (8%). On pourrait certainement questionner cette différence de
proportion entre 26% et 8%, tout particulièrement si l'accusé est dans
A. Considérons l'hypothèse «cette différence est l'effet du hasard plutôt
que d'un biais systématique contre la sélection de juré dans A».
On ne peut exclure cette hypothèse, mais est-elle plausible?

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "784acc21605c21111f620237b076fcd2", "grade": false, "grade_id": "cell-b4beeead06949fbb", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Modélisation

Quantifions cela. Pour commencer introduisons un **modèle** pour le
processus de sélection des jurés basé sur un processus aléatoire.

**Modèle:** les 100 membres de la présélection sont tirés de façon
aléatoire uniforme à partir de la population éligible de la région,
dont 26% est dans A.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "50af149eecd0636d3ace610b09e89170", "grade": false, "grade_id": "cell-8b19b8b2da2455f3", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Nous allons maintenant étudier l'hypothèse suivante: ce modèle est
représentatif du processus réel qui a conduit à la préselection $P$
(que nous appellerons **réalité terrain**); ce n'est que l'effet du
hasard qui s'il n'y a au final que 8 jurés de A.

<div class="alert alert-info">

Comment tester la validité de cette hypothèse?

</div>

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "572f50941894cdeaf0539573cf1c26a8", "grade": false, "grade_id": "cell-095ab5ac43c89c70", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Le modèle étant très simple, il serait possible de mener une **étude
probabiliste**. Nous allons ici nous contenter de procéder par
**simulation**, en produisant un **jeu de données** sur la base de ce
modèle, c'est-à-dire en tirant un grand nombre de présélections
aléatoirement. Ces données donneront des prédictions sur ce à quoi
ressemble une présélection aléatoire. Si ces prédictions ne sont pas
cohérente avec la présélection, cela donnera un faisceau d'indice
contre l'hypothèse et donc contre l'impartialité du procès.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "6aa822b585f98cb983ef9358107cfb46", "grade": false, "grade_id": "cell-d1a09ad870231bf2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Voyons cela en détail.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "8c4d33d12615e8aa4a63c49bfc3bd5b2", "grade": false, "grade_id": "cell-26dc243123ccda5e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

### Étude par simulation

De même que dans le modèle, il est souhaitable d'avoir la simulation
la plus simple qui ne perde pas l'essence du problème.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9ba6094765affa229aa2f36d1dfef3ef", "grade": false, "grade_id": "cell-5d79c8e88b903759", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Pour le problème étudié, la seule information pertinente a propos d'un
juré est son appartenance au groupe A ou B. Nous allons donc
représenter une présélection par une liste de cent lettres, où la i-ème
lettre est 'A' ou 'B' selon si le i-ème membre du jury est dans A ou
B. 

Si l'on poursuit le raisonnement, l'ordre d'apparition des `A` et `B`
dans notre liste n'a pas d'importance, puisqu'elle représente un
ensemble de jurés. Tout ce qui compte est le nombre de `A` (et donc de
`B`). Ce nombre est la **statistique** sur les présélections que nous
allons simuler, pour la comparer ensuite avec celle dans la présélection
$P$ du jury réel.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bf6e76224fbce6559f67bc7b18602276", "grade": false, "grade_id": "cell-0a54c95a45078280", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice**: Implémenter une fonction qui, étant donné une liste de 'A'
et de 'B', renvoie le nombre de 'A'. 

*Indication:* Utiliser une compréhension dans la fonction pour ce calcul.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 7e8ddbf8cc93ff056275e32f0b7dccc2
  grade: false
  grade_id: cell-b356d1b1d1a9faba
  locked: false
  schema_version: 3
  solution: true
  task: false
---
def compteA(preselection: list) -> int:
    """
    Renvoie le nombre de 'A' dans preselection
    """
    c = 0
    for i in range(len(preselection)):
        if preselection[i]=='A':
            c+=1
    return c
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "d839d489d0cd760a79d74e3341393613", "grade": false, "grade_id": "cell-d68d55ffaaa74faa", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Vérifiez votre fonction sur l'exemple suivant:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 5a633435a2d57a4555093f95496c8253
  grade: false
  grade_id: cell-8eefbe984899ed10
  locked: true
  schema_version: 3
  solution: false
  task: false
---
compteA(['A', 'B', 'B', 'A'])
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a76ff19b2506b712b70619fdb5042138", "grade": false, "grade_id": "cell-cbb22381dffa06ff", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Faites quelques essais supplémentaires:

```{code-cell} ipython3
compteA(['A', 'B', 'B', 'A', 'B', 'B', 'A', 'B', 'B', 'A'])
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "18d170d53efa6a5697feb26f602c3a15", "grade": false, "grade_id": "cell-6eea0bd634ca4a64", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Lancez ces tests sur les cas de base:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 4b5c22b6bfbeaee39bef0cd4e5651edf
  grade: true
  grade_id: cell-fec5f37ff6532c2c
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert compteA([]) == 0
assert compteA(['A']) == 1
assert compteA(['B']) == 0
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "33d3a74405d72b093fa5642a10de2509", "grade": false, "grade_id": "cell-092aa3d7f79f2c31", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Lancez les tests systématiques suivants:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 0fb2a116baaa95107398de1db9ba3f4a
  grade: true
  grade_id: cell-61a6a4b86a580626
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
import random
for n in range(10):
    for a in range(n):
        # Fabrication d'une liste aléatoire de taille n avec a 'A'
        l = ['A'] * a + ['B'] * (n-a)
        random.shuffle(l)
        assert compteA(l) == a
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "1d309d8feef27aa371d2cb121729fec3", "grade": false, "grade_id": "cell-c174894e0356cbd0", "locked": true, "schema_version": 3, "solution": false, "task": false}}

#### Simulation d'un tirage aléatoire d'une présélection

Nous souhaitons maintenant simuler le tirage au hasard de 100 personnes
distinctes dans la population, puis compter le nombre d'entre eux dans
A. Un algorithme possible serait de réellement tirer 100 personnes
distinctes dans la population (on pourrait utiliser `random.sample`
pour cela, ou tirer à la main les personnes les unes après les autres); pour
ce faire, il faudrait connaître la taille totale de la
population. Pour simplifier, nous supposerons qu'elle est très grande
par rapport à la présélection. De ce fait, même lorsque l'on a tiré un
certain nombre de personnes, la proportion de membres de A dans la
population restante n'est pas modifiée significativement.

Du coup, à chaque tirage, la probabilité que la nouvelle personne
choisie soit dans A est de 0,26.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "279ce1684fcfb1aff1b2420f144ec571", "grade": false, "grade_id": "cell-cd9d5db972469739", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice:** implémenter une fonction `lettreAleatoire(p)` qui
renvoie aléatoirement 'A' ou 'B' avec probabilité $p$ pour 'A'.  
**Indications**:
- Consultez la documentation de `random.random`:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 440edb07fb7db12eeea7c27990472f35
  grade: false
  grade_id: cell-6ae75ba96081b0ad
  locked: true
  schema_version: 3
  solution: false
  task: false
---
random.random?
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "09b64d2cc641ab7991b8103b2b4520ca", "grade": false, "grade_id": "cell-cd9d5db972469740", "locked": true, "schema_version": 3, "solution": false, "task": false}}

- Essayez plusieurs fois `random.random`:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 0620631fce06828b859c20aa9792d5ff
  grade: false
  grade_id: cell-b55c0ff44e1b7923
  locked: true
  schema_version: 3
  solution: false
  task: false
---
random.random()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "832e5dda934bd7c6cbeaebc847c4f62e", "grade": false, "grade_id": "cell-1cf1cc2c7416bfb7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

À vous de jouer maintenant: implémenter la fonction `lettreAleatoire()` en utilisant `random.random()`.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 126ac8cb8e6efec149a263c171129ce8
  grade: false
  grade_id: cell-df03759f8aa6428b
  locked: false
  schema_version: 3
  solution: true
  task: false
---
import random
def lettreAleatoire(p: float) -> str:
    a = random.random()
    if a<p:
        return 'A'
    else:
        return 'B'
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fa04c2bae1b9c1b73f4946f953c321ce", "grade": false, "grade_id": "cell-c12ca94a3c2c07c3", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Essayez quelques fois votre fonction:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: ae1f4816336624fda4c95185db252c33
  grade: false
  grade_id: cell-8c9d899dd3c19a2d
  locked: true
  schema_version: 3
  solution: false
  task: false
---
lettreAleatoire(0.26)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b1579c926a509eca1752bf8a7f3d991c", "grade": false, "grade_id": "cell-fbec4f2d5dd3f426", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Lancez les tests suivants qui vérifient 20 fois que lettreAleatoire() renvoie 'A' ou 'B'

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: e30a0303c5517de3c68ec17dd2f91ffc
  grade: true
  grade_id: cell-dfa741aff298a186
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
for i in range(20):
    assert lettreAleatoire(0.26) in ['A', 'B']
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fb2f80ae51637432f1e71b3fda1d3dd7", "grade": false, "grade_id": "cell-95e42301fd0037c0", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice:** implémenter une fonction `preselection` qui construit une
liste de n lettres avec `n=100` par défaut, où chaque lettre est tirée
aléatoirement de façons indépendant parmi 'A' et 'B' avec probabilité
0,26 pour 'A'.  
**Indication**: utilisez une compréhension

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 3976db30dbbd7c148d97d0982548a6b6
  grade: false
  grade_id: cell-df03759f8aa6428c
  locked: false
  schema_version: 3
  solution: true
  task: false
---
def preselection(n: int = 100) -> list:
    L = []
    for i in range(n):
        a = random.random()
        if a<=0.26:
            L.append('A')
        else:
            L.append('B')
    return L
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "5194da882dfe492165dda4122f9155b7", "grade": false, "grade_id": "cell-437fe696d4713ffa", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Essayez quelques fois votre fonction:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 45d40289532885afa3fcfb91ebabb318
  grade: false
  grade_id: cell-8c9d899dd3c19a2e
  locked: true
  schema_version: 3
  solution: false
  task: false
---
preselection(10)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "da0e0d37c903b2ea58b814967465b577", "grade": false, "grade_id": "cell-57df925cf488a633", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Lancez les tests suivants qui vérifient que la fonction renvoie bien
des listes de 100 lettres `A` ou `B`:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: db726a3b0151972ce7f2312663947838
  grade: true
  grade_id: cell-dfa741aff298a187
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
for i in range(20):
    l = preselection()
    assert isinstance(l, list)
    assert len(l) == 100
    assert all(lettre in ['A', 'B'] for lettre in l)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "889086e24aceaa7601ceb54d3484f9a8", "grade": false, "grade_id": "cell-a46779e2e76de9e9", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Il serait souhaitable aussi de vérifier que la liste est bien
aléatoire. Cela demanderait des tests statistiques; ce sera pour
plus tard :-)

Calculez la statistique du nombre de `A` pour un échantillon aléatoire;
réitérer plusieurs fois le calcul pour vous faire une première intuition
de la variabilité de cette statistique.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 9a6d39b275843799e5a8e05328daaec8
  grade: false
  grade_id: cell-4b8e1fa2cdee868b
  locked: false
  schema_version: 3
  solution: true
  task: false
---
nb_A = 0
liste = preselection()
for i in range(len(liste)):
    if liste[i]=='A':
        nb_A+=1
nb_A
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "56de57bee7f54fc272845dabba7d5907", "grade": false, "grade_id": "cell-5532d709dad242f2", "locked": true, "schema_version": 3, "solution": false, "task": false}}

#### Simulation d'un grand nombre de tirages aléatoires de présélections

Pour affiner cette intuition, nous allons faire un grand nombre de
tirages aléatoires et des statistiques sur le résultat.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "832a56c142d9eb750612e4737a9d321a", "grade": false, "grade_id": "cell-b329552cee8f1817", "locked": true, "schema_version": 3, "solution": false, "task": false}}

<!-- TODO: quel nom utiliser plutôt que statistique: caractéristique? variable? !-->

Tirez aléatoirement dix mille présélections, calculez la statistique
de chacune d'entre elle et stockez le résultat dans une série pandas
`dataset` de nom «nombre de jurés dans A».  

**Indications:**
- utiliser une compréhension;
- revoir les exemples d'utilisation de `pandas.Series` et notamment l'argument `name=...`.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 4e9608dfed185c61872db1e2f6d9ff39
  grade: false
  grade_id: cell-79fa4c1a8609f844
  locked: false
  schema_version: 3
  solution: true
  task: false
---
import pandas as pd
stats = []
for _ in range(10000):
    nb_A = 0
    liste = preselection()
    for i in range(len(liste)):
        if liste[i]=='A':
            nb_A+=1
    stats.append(nb_A)

dataset = pd.Series(stats, name = 'nombre de jurés dans A')
dataset
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bf606a95d2f9501aac04268363225e45", "grade": false, "grade_id": "cell-600f243540f67c2d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Ce sera notre jeu de données; un tel jeu de données est souvent dit
*synthétique* car obtenu par une simulation.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "fe9dbbca3fbe5ca2a47778e0b962ea5c", "grade": false, "grade_id": "cell-42685c1574fb8aef", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Reste à interpréter les résultats de la simulation. Cela
commence toujours par de l'extraction de statistiques simples et de la visualisation!

Affichez les statistiques simples du jeu de donnée (`describe`):

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 2592673ddefec619f112b123640a38be
  grade: false
  grade_id: cell-1a58eafa7f9b0b81
  locked: false
  schema_version: 3
  solution: true
  task: false
---
dataset.describe()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "c5fe6e313b7fa942c3ce37650af7b3d9", "grade": false, "grade_id": "cell-64503fdcf6986343", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Affichez un histogramme du jeu de données (`hist`):

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 30008b92111f3533472e6be205f71ab6
  grade: false
  grade_id: cell-6cffa8974cf71fdc
  locked: false
  schema_version: 3
  solution: true
  task: false
---
dataset.hist()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0458542b3c14c24a486be1a803dd58f3", "grade": false, "grade_id": "cell-1f3004ff54d92731", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Cet histogramme nous prédit empiriquement le nombre de jurés dans `A`
dans une présélection aléatoire. Comme on s'y attendait ce nombre est
autour de 26, avec des variations.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "9c3a50778e73105f4e9151e2091822f7", "grade": false, "grade_id": "cell-1f3004ff54d92732", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Relancez la simulation pour évaluer intuitivement si la forme générale
de l'histogramme varie d'une simulation à l'autre.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "7c19c09022b91e8cfa8e4648bbec79c9", "grade": false, "grade_id": "cell-b344eb38e909671a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

#### Comparaison entre prédiction et réalité terrain

La marque rouge sur l'axe horizontal ci-dessous indique
la position de la valeur 8 dans l'histogramme:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 8c139bb1b38405cd2ce1e57033ea3dea
  grade: false
  grade_id: cell-9e16df8ef7307289
  locked: true
  schema_version: 3
  solution: false
  task: false
---
from matplotlib import pyplot
dataset.hist()
pyplot.scatter(x=[8], y=[0], color="red", marker=2)
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "defcf1dc459778ddcf5c2bd7873954d0", "grade": true, "grade_id": "cell-2bf06362f7911c48", "locked": false, "points": 0, "schema_version": 3, "solution": true, "task": false}}

Comment interprétez vous le résultat des simulations? Le modèle
colle-t-il avec la réalité terrain? Autrement dit, paraît-il plausible
que la présélection ait été tirée aléatoirement?  Est-ce impossible?

On observe que la valeur 8 n'appartient pas à l'histogramme obtenu à l'aide de nos simulations et que cette valeur est éloignée de la valeur minimale qui a été trouvé suite à notre modèle. De plus, la différence observée semble être suffisamment importante pour soulever des questions sur la plausibilité de l'effet du hasard en tant qu'explication unique de la présélection. Cependant, il est tout de même possible avec une chance relativement faible qu'un tirage aléatoire ait donné uniquement 8 jurés de A.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "40cac1db3ac8083f518c49c8e2c0b28f", "grade": false, "grade_id": "cell-40ac0ce439faa7fe", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Conclusion

Nous avons esquissé sur cet exemple une méthode très générale pour
évaluer la validité d'un modèle, méthode que nous formaliserons et
développerons dans les cours suivants.

+++

Le TP est fini! Il ne vous reste plus qu'à déposer votre travail.
