# `LANE_B_GOAL.md` completion audit

## Claim boundary

`PROVED`: all four upgrade completion criteria are met by immutable replayed
records.  This audit concerns the Lane B upgrade campaign only.  It does not
claim an exact cubic Ising free energy, critical temperature, critical
exponents, or sub-area complexity.

## Upgrade 1 — G1

Requirement: arbitrary-width generic nonuniform equality and an explicit
length bound, not a finite-width extrapolation.

Evidence:

- `artifacts/cycle-8-b11-g1-generic-tightness-v2.json` is the authoritative
  correction artifact and passes byte-identical `--check` replay.
- The symbolic proof gives
  `R_infinity(w)=2^(w^2-1)` for every `w>=3` and the uniform sufficient bound
  `n_0(w)=11`.
- The lower bound uses separate full-rank separator factors: normal and
  opposite-phase one-sided encoders plus an invertible two-slab diagonal
  propagation.  It does not extrapolate the checked widths.
- Independent connected lifted-matroid specializations at `w=3,...,7` and a
  two-prime dense width-three minor audit the coordinate and sign route.

Classification: **complete**.  Homogeneous anisotropic and isotropic
tightness remain explicitly outside the required generic-nonuniform claim.

## Upgrade 2 — Abstract separator theorem

Requirement: intrinsic hypotheses, affine corrections, boundaries, grid
corollary, and a meaningful non-grid family.

Evidence:

- `artifacts/cycle-10-b9-abstract-separator-k33-sharpness-v1.json` passes
  immutable replay.
- The theorem is stated on relative chain spaces with intrinsic trace maps;
  H1--H3 are identified as sufficient rather than necessary.
- Quadratic affine corrections and free, periodic, antiperiodic and fixed-spin
  boundary behavior are stated.
- The checkerboard grid is a corollary with `|S|=w^2`.
- Toroidal `K_(3,3)` two-sum chains are an infinite non-grid sharpness family:
  generic pair rank two and internal rank four, proving H3 essential.

Classification: **complete**.

## Upgrade 3 — All-spin-structure algorithm

Requirement: an exact operation on the complete family, asymptotic advantage
over sector enumeration, and nontrivial exact validation.

Evidence:

- `artifacts/cycle-9-b8-lane-b-all-q-marginals-v1.json` passes immutable
  replay.
- Two TT environment sweeps compute all four single-handle Walsh marginals at
  every handle under arbitrary product-form sector weights in
  `O(g*4*d_w^2)` dense ring operations.
- Exact values agree with explicit `4^g` enumeration for genera five and six
  over two primes.
- The comparison is explicitly not against ordinary transfer for one `Z`.

Classification: **complete**.

## Upgrade 4 — Embedding robustness

Requirement: classify the positive embedding class, stabilization, rotation
changes, nonminimum genus, and basis changes; include the requested same-grid
test or a sharp permitted obstruction.

Evidence:

- `artifacts/cycle-11-b10-lane-b-embedding-robustness-v1.json` proves the
  filtration-compatible robustness class, noncellular rank-one stabilization,
  cellular-surjectivity obstruction, and pair/internal coordinate boundary.
- `artifacts/cycle-11-b10-lane-b-embedding-robustness-v2.json` passes immutable
  replay and adds the explicit same-grid test.  Exhausting all 256 local
  orientations of `P_2 square P_2 square P_2` gives genus counts
  `2,54,200` at genera `0,1,2`; selected genus-zero and genus-two rotations
  have one and sixteen pre-Arf sectors but identical physical contractions
  over two primes.
- The genus-two cube rotation is an explicit nonminimum-genus cellular
  embedding of the same cubic grid graph.

Classification: **complete**.

## Artifact integrity

The initial Cycle 8 v1 artifact is immutable but noncanonical because it
embedded volatile timing and memory measurements.  Its mathematical replay
passed; its byte check correctly failed.  The Cycle 8 v2 correction removes
only those volatile fields, freezes v1 and its cause, and passes `--check`.
No completion claim relies on v1 as the canonical record.

All four authoritative artifact checks pass in CPython 3.12.3 with the pinned
project conventions.  No required upgrade item remains open.
