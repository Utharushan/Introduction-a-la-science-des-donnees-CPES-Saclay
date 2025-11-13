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

NROWS: CONST = RANDOM_INT(2, 6)
NCOLUMNS: CONST = RANDOM_INT(10,12)
START: CONST = RANDOM_INT(1, NCOLUMNS-1)     # number of first selected column
END: CONST = RANDOM_INT(START+2, NCOLUMNS+1) # number of last selected column, excluded
SIZE: CONST = END - START                    # number of selected columns
TEST: CONST = RANDOM_INT(1, 3)
```

```{code-cell} ipython3
:tags: [hide-cell]

T = np.array(range(NROWS*NCOLUMNS)).reshape(NROWS, NCOLUMNS)
```

```{code-cell} ipython3
:tags: [hide-cell]

solution = T[:, START-1:END-1]
```

:::{admonition} Consigne

Soit T un tableau numpy à NROWS lignes et NCOLUMNS colonnes.

Extraire SIZE colonnes du tableau T à partir de la START ème colonne.

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
