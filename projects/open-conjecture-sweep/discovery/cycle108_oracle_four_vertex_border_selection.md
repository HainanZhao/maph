# Oracle C108 selection: four-vertex Seidel border transition

**`CONJECTURED` planning decision.**  The human-selected problem remains F001,
the asymmetric book-Ramsey construction problem.  Oracle selects C108 and its
method only; it does not select or change a problem or project.

## Question, critique, and brainstorm

**Question.**  Can one pass from a frozen valid order-(4n-2) Seidel state to
order (4(n+1)-2) by adjoining four vertices, and in particular extend the
public exact (n=70) state to (n=71)?

**Question the questioning.**  The preceding route was shaped by whichever
character or translation algebra made multiplication cheap.  That can hide
the actual missing interface: a parameter transition.  Conversely, merely
asking a SAT solver for the next graph would be an uninformative census.  The
border must therefore be derived before solving, restricted to four new
columns, and independently checked as a transition of the frozen input.

**Question that critique.**  Requiring a uniform symbolic formula immediately
may discard a small exact transition whose row types expose the formula.  A
single certified border at (70\to71) is not an all-(n) theorem, but it tests
the constructor interface directly and can reveal the invariant needed for
iteration.

Three genuinely different mechanisms were compared:

1. invert (S^2=(4n-3)I-4B) from a prescribed regular square graph (B);
   this has no bounded integral square-root family yet;
2. use a nontranslation coherent-configuration orbit algebra; this lacks a
   source-cleared smallest orbit state and risks another fixed block family;
3. adjoin a four-vertex border to a frozen valid (S); this has six row
   states, an exact equivalence, a direct verifier, and a checkable bounded
   stop.  **Oracle selects (3).**

The strongest flaw is seed dependence: an UNSAT result excludes only this
four-vertex border of the frozen (n=70) state, while a SAT result supplies
only (n=71).  Its expected information gain is nevertheless highest because
both outcomes test a reusable (n\mapsto n+1) interface rather than another
character kernel.

## Selected state, transition, and invariant

Freeze and independently validate the public exact (278\times278) Seidel
matrix (S_{70}): symmetric, zero diagonal, off-diagonal entries in
(\{\pm1\}), (S_{70}\mathbf1=-\mathbf1), and off-diagonal entries of
(S_{70}^2) in (\{0,-4\}).  The public constructor and the normalized
matrix must both be frozen before execution; the current C101 code is not by
itself evidence that the published (n=70) sign choice was reconstructed.

For a symmetric (4\times4) Seidel matrix (T) and
(X\in\{\pm1\}^{278\times4}), set

\[
 S' = \begin{pmatrix}S_{70}&X\\X^{\mathsf T}&T\end{pmatrix}.
\]

The top row-sum equations force every row (x_i) of (X) to be one of the
six balanced vectors

\[
 \mathcal P=\{x\in\{\pm1\}^4:x\mathbf1=0\}.
\]

For each old pair, the top-left square equation is exactly

\[
 (S_{70}^2)_{ij}+x_i\!\cdot x_j\in\{0,-4\}.
\]

Thus a pair with square entry (0) permits dot product (0) or (-4),
whereas a pair with square entry (-4) permits (0) or (4).  This is a
six-state pair constraint, not a free edge search.  The remaining exact
constraints are

\[
 S_{70}X+XT\in\{0,-4\}^{278\times4},\qquad
 (X^{\mathsf T}X+T^2)_{ab}\in\{0,-4\}\ (a\ne b),
\]

and (X^{\mathsf T}\mathbf1+T\mathbf1=-\mathbf1).  These equations are the
proposed transition and invariant.  Encode all (2^6=64) labelled choices
of (T) and the 278 six-valued row variables exactly.

## Verifier, caps, falsifier, and stop

- **Smallest direct verifier:** for a hit, reconstruct (S') and independently
  multiply the full (282\times282) integer matrix, then independently check
  the corresponding graph and complement common-neighbour thresholds.  For a
  no-hit, independently regenerate the Boolean encoding and check a proof of
  UNSAT for every one of the 64 (T) cases; a solver exit code is not proof.
- **Caps:** at most 64 (T) cases, 278 six-state variables, two worker
  processes, 1,800 aggregate wall seconds, 2 GiB aggregate peak memory, and
  512 MiB aggregate proof/output data.  No random search, edge variables,
  second seed, eight-vertex border, or unrestricted graph census.
- **Falsifier:** a mismatch between the six-state reduction and direct block
  multiplication, a rejected SAT/UNSAT certificate, or failure of the frozen
  (S_{70}) source reconstruction.
- **Advance/stop:** a verified SAT witness banks an exact (n=71) border and
  exposes its six-state pattern for later theorem design.  Checked UNSAT for
  all 64 cases proves only that this frozen (S_{70}) has no balanced
  four-vertex border.  A cap is inconclusive and remains C108 for an amended
  optimization tranche.  After SAT or certified UNSAT, stop C108; do not
  patch it with another seed or a larger border.

Before promotion, source-check whether (n=71) has since been constructed;
overlap changes novelty, not the exact transition result.

## Artifact-cited exclusion map

| record | former question and outcome | exact C108 delta |
| --- | --- | --- |
| `cycle-103-b103-book-ramsey-reflection-boundary-correction-v2` | fixed public six-block placement with 19 signs and six inversion bits; exact (q=7) no-hit | no character block placement or inversion bit; the old valid matrix is an opaque frozen input and only four new columns are designed |
| `cycle-104-b104-book-ramsey-dihedral-cayley-boundary-v1` | all 16 four-bit (D_{14}) Cayley states fail | no group connection set; six row patterns describe a border of a non-Cayley input |
| `cycle-105-b105-book-ramsey-complement-translate-boundary-v1` | uniform obstruction for (B=\mathbb Z_q\setminus A) | no complement transition or autocorrelation state |
| `cycle-106-b106-book-ramsey-mixed-reflection-boundary-v1` | uniform obstruction for every inverse-closed degree-(q) dihedral Cayley state | leaves the entire dihedral-Cayley state space and uses an (n\mapsto n+1) border transition |
| `cycle-107-b107-book-ramsey-paley-cross-boundary-v1` | fixed-Paley-cross two-layer translation state is uniformly impossible | no Paley cross kernel, no two-layer translation invariance, and no restricted-(P_i) patch |
| `discovery/f001_dai_lin_2026_source_audit.md` | Dai--Lin construct diagonal exact families from PC graphs/symmetric conference matrices | asymmetric order-(4n-2\) to order-(4n+2) border of a frozen Seidel state; no PC graph, conference matrix, Mathon product, or clone-pair rederivation |

**Historical gap:** the repository does not yet freeze the public (n=70)
adjacency/Seidel bytes or establish current (n=71) novelty.  C108 must freeze
and validate the former before preregistration execution and must not claim
the latter without a current primary-source screen.

## Pre-execution containment

**`OBSERVED`, 2026-08-06 UTC:** the required valid \(S_{70}\) was not found.
The C101 public n=70 six-block placement is a sealed no-hit, and Wesley's
checked 2-block theorem applies only when \(2n-1\equiv1\pmod4\), whereas
\(2\cdot70-1=139\equiv3\pmod4\).  See
`discovery/cycle108_seed_preflight.md`.  Therefore this selection creates no
executable cycle, consumes no budget, and records no SAT/UNSAT result.
