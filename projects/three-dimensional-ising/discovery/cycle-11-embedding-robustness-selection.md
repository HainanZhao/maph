# Cycle 11: embedding robustness

## Decision question

Which changes of embedding, gauge, stabilization, and canonical coordinates
preserve the all-q separator bound, and where does invariance fail exactly?

## Question the questioning

“Topological” does not mean independent of every rotation system.  The
complete pre-Arf tensor records the ambient surface genus and can change size
even when the final physical Ising polynomial does not.  Robustness must
therefore be scoped to transformations preserving the filtration hypotheses.

## Exclusion map and selected tests

- Filtration-compatible homeomorphisms, cochain gauges, completion changes,
  and transported affine quadratic origins are handled algebraically.
- A stabilization disjoint from the graph is tested separately because it
  leaves the cellular category.
- Arbitrary rotation robustness is falsified on the smallest useful graph:
  `K3,3` has explicit cellular rotations of genus one and two.
- Pair-cut coordinate changes and internal binary changes are separated; the
  K3,3 chain supplies the H3 obstruction.

## Input, verifier, and falsifier

- Input: the abstract separator theorem and its K3,3 sharpness family.
- Invariant: the relative-chain trace factorization, not surface genus alone.
- Direct verifier: exact face walks, homology rank, and normalized Arf sums
  for the two K3,3 rotations over two primes.
- Falsifier for full embedding invariance: different spin-structure tensor
  dimensions for the same abstract graph.  The genus-one/genus-two pair is
  such a falsifier.

