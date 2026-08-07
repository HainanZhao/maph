# Cycle 7 selection: arbitrary-width canonical closure

## Decision question

Does there exist an explicit deletion-compatible orientable embedding and
filtration-compatible canonical symplectic ordering for every
`G_(n,w)=P_n square P_w square P_w` such that every pair and internal
spin-structure cut glues through only the even frontier mask
`V_w`, of size `2^(w^2-1)`?  If not, what is the first intrinsic quotient
memory `h(w)`?

## Question the questioning

The corrected `w=3` result does not justify extrapolation.  Its raw canonical
labels are actually nonlocal; closure survives only because every propagated
old mode is a transverse coboundary.  A width-independent proof must therefore
control the quotient `C^1/B^1`, not imitate the four visible `w=3` masks.

Minimum genus is also not logically required for an upper representation.
Insisting on an unknown minimum-genus formula could hide a valid theorem for
an explicit nested embedding.  Conversely, adding redundant handles can make
an all-spin-structure statement artificially easy or expensive, so redundant
handle removal and its effect on the tensor must be audited separately.

## Exclusion map

- Former question: do the width-three ranks saturate at `1024/2048`?  Killed
  by the missing conjugate correction; corrected saturation is `256/256`.
- Former state: raw canonical labels have bounded local support.  Killed;
  only their classes modulo coboundaries are local.
- Former method: deterministic symplectic Gram--Schmidt without regard to the
  slice filtration.  Excluded as the primary constructor because it can mix
  both sides of a cut and manufacture nonlocal handle coordinates.
- New delta: the embedding, filtration, symplectic normalization, quadratic
  affine correction, and all twist-coordinate maps must be frozen together.

## Brainstormed mechanisms

1. **Selected:** a deletion-compatible ribbon rotation followed by a
   filtration-adapted symplectic/Witt decomposition.  At a cut, exact modes are
   gauged away and only persistent relative-homology intervals are tested for
   frontier determinacy.
2. A crossing-handle embedding from a fixed planar drawing, with one local
   canonical handle per resolved crossing.  This makes handles explicit but
   may add many redundant genera and obscure comparison with minimal genus.
3. An abstract separator theorem for quadratic refinements of filtered cycle
   spaces, independent of a grid embedding.  This is potentially strongest,
   but its hypotheses must first be extracted and falsified on `w=4`.

## Frozen first experiment

- Input state: the Cycle 6 corrected gluing identity and an explicit fixed
  cyclic order of lattice directions, restricted at boundary vertices so
  deletion of the terminal slice preserves the old rotation.
- Map/invariant: exact intersection matrix, filtration-compatible symplectic
  transport, and `h_cut=dim(W_cut/(W_cut intersect B^1))` for every pair and
  internal cut.
- Smallest verifier: `w=4`, two successive even longitudinal sizes, with exact
  `S^T Omega S=J`, polarization, Arf, and local-mode classification.
- Advance condition: `h_cut=0` plus an explicit `V_4` left/right factorization
  for every cut type; or a rigorous nonzero quotient class giving G3/G4.
- Stop criterion: no dense `32768` carrier matrix before the local quotient
  theorem is settled; one run below 30 minutes and 8 GiB.
- Falsifier: a canonical phase whose restriction to two partial configurations
  with the same frontier mask differs after every allowed coboundary gauge.

## Claim boundary

G0 removes genus-based redundancy only.  With `w=L`, the remaining carrier is
still `2^(L^2-1)`.  No cubic free energy, critical temperature, or polynomial
algorithm follows.
