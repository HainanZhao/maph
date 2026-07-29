# Cycle 001 — source-level certification audit

Date: 2026-07-29

## Question

Do maintained, widely visible QMC packages already provide the exact or
enclosure-certified lattice-merit path proposed here?

## Frozen snapshots

- LatNet Builder, commit
  `39dd60fceb0c86a6124b701072d91f8e3aed73df`
  (2025-08-22).
- QMCPy, commit
  `a774f3a1297b982f2544742e8c691e035c9fc0a7`
  (2026-07-23).

The audit inspected the official repositories, not only their
documentation.

## Findings

### LatNet Builder

The lattice merit scalar and vector types are `double`.  Bernoulli
polynomials are evaluated using decimal binary64 constants, the fast
inner product is performed through FFTW's double-precision transform,
and the minimum functor selects a branch using an ordinary `<`
comparison.  The search state and pruning threshold are likewise
floating-point `Real` values.  No exact-rational, interval, Arb/MPFR, or
replay-certificate path for these decisions was found in this snapshot.

Evidence locations:

- `include/latbuilder/Types.h`
- `include/latbuilder/Functor/BernoulliPoly.h`
- `include/latbuilder/MeritSeq/CoordUniformInnerProdFast.h`
- `include/latbuilder/Functor/MinElement.h`
- `include/latbuilder/Task/Search.h`

### QMCPy

QMCPy preserves loaded generating-vector entries as integers and emits
lattice points in NumPy floating point.  It is chiefly a sampling and
integration package, not a lattice-merit construction engine.  Its
LatNet Builder linker is marked under reconstruction.  No exact or
interval lattice worst-case-merit evaluator, certified CBC search, or
replay certificate was found in this snapshot.

Evidence locations:

- `qmcpy/discrete_distribution/lattice/lattice.py`
- `qmcpy/util/latnetbuilder_linker.py`

## Decision

**CONTINUE.**  The inspected flagship implementations do not close the
arithmetic-certification gap.  This is deliberately a snapshot-scoped
result, not a proof that no certified implementation exists anywhere.
Phase 0 literature searching therefore remains open while the project
can proceed with a clearly differentiated exact prototype.

Tag: `VERIFIED_SOURCE_AUDIT`.
