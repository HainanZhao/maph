# Correction to the Cycle 4 canonical-handle claim

## Corrected claim boundary

`PROVED`: the Cycle 4 relative defect generator

```
d=old_last+raw_new_a
```

is correct.  Its claimed conjugate `c=raw_new_b` is not orthogonal to the old
homology space and therefore does not extend the old canonical handles.

`PROVED`: solving the exact intersection equations at every transition
`4->5,...,11->12` gives

```
c=old_second_last+raw_new_b.
```

With both corrections, the transported intersection matrix is exactly the
standard symplectic matrix.

## Cause

The Cycle 4 verifier checked that `d` was orthogonal to every old generator
and that `<d,raw_new_b>=1`.  It did not check
`<old_generator,raw_new_b>=0`.  Those missing pairings are nonzero.  Pairing
with `old_second_last` cancels them exactly.

## Affected claims

- The minimum-genus embedding, face surgery, relative defect dimension,
  parity carrier, and character-transfer identity are unaffected.
- The literal statement `c=raw_new_b` is withdrawn.
- The `1024/2048` rank proof for the complete canonical quadratic-refinement
  tensor is withdrawn because its per-handle transform was applied in a
  non-symplectic coordinate system.
- The corresponding bound for the Walsh tensor in its explicitly displayed
  noncanonical coordinates remains an algebraic finite-state bound, but it is
  not a canonical-handle theorem.
- Cycle 5's raw-basis finite determinants and spin/parity intertwiner are
  unaffected; its references to the Cycle 4 canonical `F` bound inherit this
  correction.

## Replacement

The corrected coordinates have growing raw support.  All propagated old
modes are exact transverse coboundaries.  The separate Cycle 6 cochain proof
uses this quotient structure and targets a stronger canonical bound `256`.
That replacement is not made retroactive: the sealed Cycle 4 artifact remains
immutable and this correction supersedes only the affected claims.
