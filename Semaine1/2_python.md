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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "dc9b800c481debd93ceb3922399fb4b5", "grade": false, "grade_id": "cell-d7d1bb6ef72c7615", "locked": true, "schema_version": 3, "solution": false, "task": false}}

# Python: fonctions et compréhensions

Cette feuille donne des rappels de syntaxe Python tels que les **compréhensions** vues en introduction à l'informatique au semestre précédent.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a5e06e48dbb4c849ba946501c4a5adfd", "grade": false, "grade_id": "cell-289da30635e3d347", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## De C++ à Python

Vous trouverez ci-dessous quelques rappels à propos du langage de
programmation Python en comparaison avec C++:

- les instructions sont séparées par des sauts de ligne (pas de `;`)
- les blocs sont déterminés par l'indentation (et non les accolades `{}`)
- le type est attaché aux valeurs et non aux variables
- déclaration optionnelle des variables 
- déclaration optionnelle du type des entrées et sorties des fonctions  
  mais c'est possible et recommandé par **annotations de types**

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ed40df195e28c5047b11bb3f3df547d5", "grade": false, "grade_id": "cell-289da30635e3d348", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Constantes et affectations:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: fc5945bb419884eed05c7191215963fb
  grade: false
  grade_id: cell-dc84a7006df389ec
  locked: true
  schema_version: 3
  solution: false
  task: false
---
x = 42
message = "Bonjour!"
pi = 3.14159
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ef19a9c087bd0491704fde3eb083b703", "grade": false, "grade_id": "cell-00635ac8661e6ea7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Dans une cellule Jupyter: seule la valeur de la dernière **expression** est affichée:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: a93c1e27f9cbdee54c770cac02598b64
  grade: false
  grade_id: cell-1ee690c1362bdae3
  locked: true
  schema_version: 3
  solution: false
  task: false
---
message
x + pi
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2b9e36e9a9fa7268b396971cc7c86e33", "grade": false, "grade_id": "cell-361ec16e1df96be8", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Avec un `;` la dernière expression est vide; il n'y a donc rien d'affiché:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: b4312d6cf553d1cbbdc848a836f13018
  grade: false
  grade_id: cell-411a888561fead89
  locked: true
  schema_version: 3
  solution: false
  task: false
---
message
x + pi;
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2a8fa2e435a68bc027cdef6144d09653", "grade": false, "grade_id": "cell-489a3b0263b9c8ab", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Les chaînes de format `f"..."` permettre de construire aisément des chaînes de
caractères avec des paramètres:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 6c0fe5d9734d0f1d2762dea20c1aeb85
  grade: false
  grade_id: cell-90e482b3e971288c
  locked: true
  schema_version: 3
  solution: false
  task: false
---
f"La somme de x et pi vaut: {x+pi}; cela vaut bien un message: {message}"
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "ec6e69c0e2732366d02b770e4e4a8353", "grade": false, "grade_id": "cell-289da30635e3d349", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Un `if` en C++:

    if ( x < 10 ) {
        cout << "x est strictement plus petit que 10" << endl;
    } else {
        cout << "x est plus grand que 10" << endl;
    }

Le même `if` en Python:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 99dc916bf07f8e13943b7d2782bbda7d
  grade: false
  grade_id: cell-a435b2fbd0565b18
  locked: true
  schema_version: 3
  solution: false
  task: false
---
if x < 10:
    print("x est strictement plus petit que 10")
else:
    print("x est plus grand que 10")
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "34a6e7bdd85aa7797b17a0e59d6a8c35", "grade": false, "grade_id": "cell-289da30635e3d350", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Une boucle for en C++:

    for (int i = 0; i < 10 ; i++) {
        cout << i << endl;
    }

La même boucle `for` en Python:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 6267e6ac7c2c71aa842c9f76354e9672
  grade: false
  grade_id: cell-fcb8946e8549144d
  locked: true
  schema_version: 3
  solution: false
  task: false
---
for i in range(0, 10):
    print(i)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "96574977f82b0cc62c16590e89b9a477", "grade": false, "grade_id": "cell-a99fc2998b2d3696", "locked": true, "schema_version": 3, "solution": false, "task": false}}

où `range` permet de construire des séquences d'entiers:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: f43035865f41e5404768807499378cfd
  grade: false
  grade_id: cell-e325098096d15c74
  locked: true
  schema_version: 3
  solution: false
  task: false
---
list(range(5, 10))
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: d1a5e0a88c2659f2481d59103a4dd2dc
  grade: false
  grade_id: cell-23d4057648ebe029
  locked: true
  schema_version: 3
  solution: false
  task: false
---
list(range(5, 95, 10))
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 0c91a7f3b50dc2b8e1808e355e24a9c1
  grade: false
  grade_id: cell-05fea603b2f96ea0
  locked: true
  schema_version: 3
  solution: false
  task: false
---
list(range(10, 5, -1))
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "12eddee46917f1ff296cf73013ccbdfe", "grade": false, "grade_id": "cell-bb1926b3e4decbf8", "locked": true, "schema_version": 3, "solution": false, "task": false}}

<!--
## Utiliser une compréhension pour fabriquer une image; essayer les commandes suivantes:

    def cercle(x,y,r):
        return Point([x,y]).buffer(r).boundary

    cercle(0,0,1)

    cascaded_union([cercle(0,0,1), cercle(0,0,2), cercle(0,0,3)])

    cascaded_union( [ cercle(0,0,r) for r in range(10) ])
!-->

## Fonctions mathématiques usuelles

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: a8b822273bc39a89da7984f4adf34679
  grade: false
  grade_id: cell-82cb666a6ab835ba
  locked: true
  schema_version: 3
  solution: false
  task: false
---
from math import sin, cos, tan
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: a7ce875295e8ba00dde0cfb007d06845
  grade: false
  grade_id: cell-bc63c30fe842c7b7
  locked: true
  schema_version: 3
  solution: false
  task: false
---
sin(3.14)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "0b4f8e24f376b7fdf4f23f094fb34382", "grade": false, "grade_id": "cell-1006ff08a1e2fe42", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Définir une fonction

En C++:

    int f(int x, int y, int r) {
        return x + y - r
    }
    
En Python:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 540819b2b767030233d47748380ce08d
  grade: false
  grade_id: cell-124a851a49c7db43
  locked: true
  schema_version: 3
  solution: false
  task: false
---
def f(x, y, r):
    return x + y - r
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "de1976f061f4f056f5d081a4bc5a9591", "grade": false, "grade_id": "cell-55082a4f66402cfd", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice:** Écrire une fonction `aire_rectangle(l,h)` qui renvoie
l'aire d'un rectangle de longueur `l` et de hauteur `h`.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 19493633b68faf6fcea1c6bed1c18188
  grade: false
  grade_id: cell-84dc375403ba0a41
  locked: false
  schema_version: 3
  solution: true
  task: false
---
def aire_rectangle(l,h):
    return l*h
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 4aca3517952dff9c90cc5e0fb0e05f51
  grade: true
  grade_id: cell-59f95bacd807e53d
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert aire_rectangle(3, 7) == 21
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b9faad4859132d965b9f69e48cc3f313", "grade": false, "grade_id": "cell-cb5cb937894c652f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Il est possible -- et même recommandé -- de rajouter de la documentation,
ainsi que des **annotations de type**. Ici nous précisons que les entrées
et les sorties sont des nombres à virgule:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: b4d88ce6a06d63cce654b02179071c84
  grade: false
  grade_id: cell-22ea70328ae3e51c
  locked: true
  schema_version: 3
  solution: false
  task: false
---
def f(x: float, y: float, r: float) -> float:
    """
    Renvoie x plus y moins r
    
    Ici, des explications sur la fonction
    """
    return x + y - r
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "626e56c0f2ee0963be44c8447ebf642c", "grade": false, "grade_id": "cell-54141b68f027b242", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Vous pouvez ensuite accéder à la documentation de la fonction
comme d'habitude avec:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: e8336f26249098767e26a44400ef5368
  grade: false
  grade_id: cell-22ea70328ae3e51b
  locked: true
  schema_version: 3
  solution: false
  task: false
---
f?
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "c1d5f49d7c2a579da73e9793928f0bdb", "grade": false, "grade_id": "cell-54141b68f027b241", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Rajoutez de la documentation et des annotations de types
à votre fontion `aire_rectangle` pour indiquer que les entrées
et les sorties sont des entiers.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 1cef3323b7972f2f298a875d0f84d9b0
  grade: false
  grade_id: cell-f6c0b119068057c4
  locked: false
  schema_version: 3
  solution: true
  task: false
---
def aire_rectangle(l: int, h: int) -> int:
    return l*h
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3d20d488cc532cd9c219c053c4980e7a", "grade": false, "grade_id": "cell-d740c766a2946515", "locked": true, "schema_version": 3, "solution": false, "task": false}}

À noter que les annotations de type ne sont pas vérifiées
à l'exécution. Votre fonction acceptera quand même des arguments
non entiers:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 2a3b495b3106ef589023e0010e0d8019
  grade: false
  grade_id: cell-3d197f41af618593
  locked: true
  schema_version: 3
  solution: false
  task: false
---
aire_rectangle(1.2, 1.3)
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3c4e4666caa3c003b1ef72edabe4d3a2", "grade": false, "grade_id": "cell-4249d1f81089ad3d", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Ces annotations servent d'une part de documentation et
d'autre part peuvent servir pour de l'*analyse
statique de code* pour détecter automatiquement d'éventuelles
incohérences.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "3de15b8ea9d70cc93e14c2698aa98744", "grade": false, "grade_id": "cell-289da30635e3d351", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Les compréhensions


Les compréhensions sont un moyen confortable de construire
des listes (ou autres collections) en décrivant tous les éléments,
avec une syntaxe proche de la notation mathématiques pour l'ensemble
des $f(x)$ pour $x$ dans $X$ tels que $c(x)$. 

$$ \{ f(x) \mid  x\in X, c(x) \}$$

En Python la syntaxe est:
```
      [ <expr> for <name> in <iterable> ]
      [ <expr> for <name> in <iterable> if <condition> ]

```

Voici par exemple la liste des $i^2$ où $i$ est dans $\{1, 3, 7\}$:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 21cfc1831431af6bbce387e8a24192cd
  grade: false
  grade_id: cell-f325fdaef0c7bc9f
  locked: true
  schema_version: 3
  solution: false
  task: false
---
[ i**2 for i in [1, 3, 7] ]
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "61aae33de24f4169719ef8c236027bd3", "grade": false, "grade_id": "cell-45facb6e9efc3a7a", "locked": true, "schema_version": 3, "solution": false, "task": false}}

La même où $i$ parcoure l'intervale $[0, 10[$:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: fbbc2b9eacbbeed72b2b1306a8d1de79
  grade: false
  grade_id: cell-263569b429309796
  locked: true
  schema_version: 3
  solution: false
  task: false
---
[ i**2 for i in range(0, 10) ]
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "b15fcf02c04e36890237ef34440d6356", "grade": false, "grade_id": "cell-04f815000e174f4e", "locked": true, "schema_version": 3, "solution": false, "task": false}}

La liste des $i^2$ dans l'intervale $[0,10[$ tels que $i$ n'est pas divisible par trois:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: e07671b1a4950af056e9b0f48a2aca2d
  grade: false
  grade_id: cell-4b473f5b507bf3a0
  locked: true
  schema_version: 3
  solution: false
  task: false
---
[ i**2 for i in range(0, 10) if i % 3 != 0]
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f2c089ab5955e7775c7d8ecb59fcbfc8", "grade": false, "grade_id": "cell-3577f245bfef4bd7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice:**
Écrire une fonction `aire_rectangles(h)` qui renvoie la liste
des surfaces de tous les rectangles de hauteur `h` et de largeur
entière dans l'intervale $[1, 5[$, en utilisant votre fonction
`aire_rectangle`:

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 43a3bbb10903b27b95b9d07d2cc29eb0
  grade: false
  grade_id: cell-4585d2e5e9cd033d
  locked: false
  schema_version: 3
  solution: true
  task: false
---
def aire_rectangles(h):
    return [i*h for i in range(1,5)]
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 11fe4cccae9001b126649fd14f69219b
  grade: true
  grade_id: cell-bffe680c74dd990b
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
assert aire_rectangles(3) == [3, 6, 9, 12]
```

## Conclusion

<!-- TODO: qu'est-ce qui a été vu dans cette feuille? !-->

Enregistrez les modifications de votre feuille (`Ctrl + s `), déposez-la avec le tableau de bord puis passez à la [feuille 3](3_pandas.md).
