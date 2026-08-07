# Cycle 9: all-q algorithmic application

## Decision question

Does the canonical all-spin-structure TT support an exact operation with an
asymptotic advantage over explicit enumeration of the `4^g` pre-Arf sectors?

## Question the questioning

Computing the final physical partition function is excluded: ordinary
zero-field transfer already has the same separator dependence.  The required
output must retain information about the complete sector family and have
output size polynomial in `g`.

## Exclusion map and alternatives

- A single Arf-weighted contraction is excluded by the goal boundary.
- Printing every sector is excluded because its output already has size
  `4^g`.
- Selected operation: all four single-handle Walsh marginals at every handle,
  under arbitrary product-form weights on all other handles.  It returns
  `4g` exact values and reuses the same left/right environments.
- Alternative retained: selected multi-handle Fourier coefficients.  It is
  no stronger for the present decision and has larger output-dependent cost.

## Input, map, verifier, and falsifier

- Input: exact four-state all-q TT cores from Cycle 7.
- Map: two environment sweeps followed by insertion of each local Walsh
  character.
- Smallest direct verifier: canonical `w=3` tensors at genus five and six,
  compared against literal all-sector summation over two primes.
- Falsifier: any marginal residue disagreement, or any hidden Arf contraction
  before the local Walsh observable is inserted.
- Resource stop: fewer than `10^5` explicitly enumerated validation sectors;
  the theorem itself is algebraic and does not depend on that cap.

