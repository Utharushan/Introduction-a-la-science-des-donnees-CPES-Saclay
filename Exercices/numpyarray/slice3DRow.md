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
NLAYERS: CONST = RANDOM_INT(4,8)
I: CONST = RANDOM_INT(1, NROWS-1)
```

```{code-cell} ipython3
:tags: [hide-cell]

T = np.array(range(NROWS*NCOLUMNS*NLAYERS)).reshape(NROWS, NCOLUMNS, NLAYERS)
```

```{code-cell} ipython3
:tags: [hide-cell]

solution = T[I-1, :, :]
```

:::{admonition} Consigne

Soit T un tableau numpy à NROWS lignes, NCOLUMNS colonnes et NLAYERS
couches.

Extraire les I èmes lignes du tableau T.

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
