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

### Objectif pédagogique : extraire des tranches de tableaux numpy

```{code-cell} ipython3
:tags: [hide-cell]

import numpy as np
from jupylates.jupylates_helpers import RANDOM_INT, CONST, INPUT
```

```{code-cell} ipython3
:tags: [hide-cell, variable]

NROWS: CONST = RANDOM_INT(2, 8)
NCOLUMNS: CONST = RANDOM_INT(10,12)
NLAYERS: CONST = RANDOM_INT(4,8)
# number of the first selected row/column/layer
START: CONST = RANDOM_INT(1, min(NROWS, NCOLUMNS, NLAYERS)-1)
# number of the last selected row/column/layer
END:   CONST = RANDOM_INT(START+2, min(NROWS, NCOLUMNS, NLAYERS)+1)
# number of selected rows/columns/layers
SIZE: CONST = END - START
```

```{code-cell} ipython3
:tags: [hide-cell]

T = np.array(range(NROWS*NCOLUMNS*NLAYERS)).reshape(NROWS, NCOLUMNS, NLAYERS)
```

```{code-cell} ipython3
:tags: [hide-cell]

solution = T[START-1:END-1, START-1:END-1, START-1:END-1]
```

:::{admonition} Consigne

Soit T un tableau numpy à NROWS lignes, NCOLUMNS colonnes et NLAYERS
couches.

Extraire de T un cube de taille $SIZE \times SIZE \times SIZE$, à
partir des START èmes lignes, colonnes, et couches.

:::

```{code-cell} ipython3
---
editable: true
nbgrader:
  grade: false
  grade_id: init
  locked: false
  schema_version: 3
  solution: true
---
answer = INPUT(
    ### BEGIN SOLUTION
    solution
    ### END SOLUTION
    )
```

```{code-cell} ipython3
---
editable: false
nbgrader:
  grade: true
  grade_id: check
  locked: true
  points: 1
  schema_version: 3
  solution: false
tags: [hide-cell]
---
assert answer.shape == solution.shape
assert np.all(answer == solution)
```
