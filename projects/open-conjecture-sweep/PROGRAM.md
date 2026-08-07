# PROGRAM: Open Conjecture Sweep

## Objective and active state

- **Project objective:** obtain a complete result or a publishable, rigorously
  scoped advance on a human-selected open problem.
- **Active problem:** **F001**, the asymmetric book-Ramsey construction
  target
  \[
  R(B_{n-1},B_n)=4n-1 \quad (n\ge2).
  \]
  Only a human may select or switch problems.
- **Status:** `F001_ACTIVE`.
- **Claim boundary:** F001 has no all-\(n\) construction or impossibility
  theorem.  Every finite replay or family obstruction below is limited to its
  stated state space.
- **Stop condition:** stop F001 only for a complete construction/proof,
  decisive loss of eligibility, or a reasoned saturation decision.  A
  bounded no-hit closes only its tested mechanism.

## Current gate: C108 border over the published \(n=70\) seed

**Decision question (`CONJECTURED`):** Does the verified order-278 Seidel
seed admit the six-state balanced four-vertex border that would give the
\(n=71\) construction?

- **Input (`PROVED` finite replay):** `proof/cycle108_seed70.py`
  reproduces Epoch's public \(n=70\) construction at \(q=139\).  It checks
  symmetry, signs, row sum \(-1\), the full Seidel-square condition
  \((S^2)_{ij}\in\{0,-4\}\) off diagonal, and book maxima \((68,69)\).
  See `discovery/cycle108_seed70_source_audit.md`.
- **State:** append four vertices.  Each old row receives one of the six
  vectors in \(\{x\in\{\pm1\}^4:\sum x=0\}\); the four-by-four bottom
  Seidel block ranges over its 64 symmetric sign matrices.
- **Direct verifier:** construct the 282-by-282 Seidel matrix and check row
  sum \(-1\), diagonal \(281\), off-diagonal square entries \(0\) or
  \(-4\), then both book caps exactly.
- **Falsifier / scope:** an exhaustive no-hit in this state space excludes
  only this border.  It neither refutes F001 nor rules out a different lift,
  seed, or non-border construction.
- **Next authorized action:** formulate a bounded encoder that preserves this
  state space without materializing every pair constraint.

## Relevant constraints

These are constraints on the next mechanism, not a substitute for it.

| Record | Tag | Boundary |
| --- | --- | --- |
| C101/C103/C104 | `PROVED` | Fixed six-block character completions and the four-bit \(D_{14}\) Cayley class are no-hits. |
| C105/C106 | `PROVED` | The complement-transition and inverse-closed degree-\(q\) dihedral Cayley families are uniformly impossible. |
| C107/C109/C111--C114 | `PROVED` | The fixed Paley-cross, inversion-warp, polarity, norm-kernel, paired-fiber, and two-block-circulant families are no-hits in their stated state spaces. |
| C117 | `PROVED` | The fixed Sylvester two-vertex-puncture family is a no-hit. |

The canonical details, frozen inputs, and replay commands are in the named
immutable records under `artifacts/`.  C108's former no-seed preflight is
superseded by the source replay above; it was an incomplete literature check,
not a mathematical boundary.

## Research graph

```text
published n=70 seed (verified)
        |
        v
C108 balanced four-vertex border ---- hit ----> exact full-matrix replay
        |                                         |
      no-hit                                       v
        |                                  scoped n=71 construction
        v
select a distinct F001 mechanism
```

Do not revive a boundary listed above by renaming it.  The workflow rules are
in the repository `AGENTS.md`, not here.

## Recovery and checks

From the repository root:

```sh
git status --short
cd projects/open-conjecture-sweep
source ../../tools/dev-env.sh
research rebuild
research check
python3 proof/cycle108_seed70.py
```

Read this file and only the artifact or source directly relevant to the next
question.  Keep exploratory material in `discovery/`; seal an artifact only
when a result must be relied on later.
