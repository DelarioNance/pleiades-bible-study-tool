# Test Suite Organization: Mathematical Guidance

## Single Test Runner

### Definitions

To choose between a **layer‑first** or **domain‑first** test organization for efficient CI/CD against a single test runner (e.g., Pytest), define:

- **L** — the set of test layers (e.g., `{unit, integration, e2e}`)

- **D** — the set of domains (e.g., `{utils, db, etl, api, ui}`)

We then define four retrieval costs:

- **LL** — retrieving all tests for a *layer* in a **layer‑first** structure  
- **LD** — retrieving all tests for a *domain* in a **layer‑first** structure  
- **DL** — retrieving all tests for a *layer* in a **domain‑first** structure  
- **DD** — retrieving all tests for a *domain* in a **domain‑first** structure  

The key comparison is between:

- **LD** — cost of retrieving a domain in a layer‑first structure  
- **DL** — cost of retrieving a layer in a domain‑first structure  

### Mathematical Facts

In a **layer‑first** structure, retrieving a layer requires traversing one layer:  
  
$$
  |LL| = 1
$$

In a **domain-first** structure, retrieving a domain requires traversing one domain:  
  
$$
  |DD| = 1
$$


In a **layer‑first** structure, retrieving a domain requires traversing all layers:  
  
$$
  |LD| = |L|
$$

In a **domain‑first** structure, retrieving a layer requires traversing all domains  
  
$$
  |DL| = |D|
$$

Thus, retrieving tests in a **layer‑first** structure is found by the following:

$$
|LL| + |LD| = 1 + |L|
$$

Likewise, retrieving tests in a **domain-first** structure is found by the following:

$$
|DD| + |DL| = 1 + |D|
$$


### Decision Rule (Mathematical)

- If $|L| < |D|$, then choose a **layer-first** structure.
- If $|D| < |L|$, then choose a **domain-first** structure.

### Decision Rule (English)

- If there are less **layers** than domains, then choose a **layer-first** structure.
- If there are less **domains** than layers, then choose a **domain-first** structure.

### Example

- If the test layers are **unit**, **integration**, and **e2e** but the test domains are **db**, **api**, **ui**, **auth**, then choose a **layer-first** domain.

## Multiple Test Runners