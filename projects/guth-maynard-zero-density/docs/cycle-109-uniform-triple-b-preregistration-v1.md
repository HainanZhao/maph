# Cycle 109 preregistration: uniform smooth triple-B kernel

Date frozen: 2026-08-02 UTC.

## Claim boundary

This cycle treats the complete three-variable oscillatory integral generated
by the registered fixed smooth Cycle-81/87/90 weights on one actual scale
ray. It may close the full perfect-power coefficient-scale multiplicity in
that smooth model. It does not aggregate distinct cores, alter the model to
arithmetic nonsmooth coefficients, or control weak/simple-root branches.

## Frozen kernel

- On fixed compact positive charts, the phase is a sum of three logarithmic-
  linear phases in `(k,r,r')`; after the Cycle-107 scale substitution it is
  `ell*(phi_k(k)+phi_r(r)+phi_r'(r'))`.
- Each one-variable second derivative has fixed sign and magnitude comparable
  to `ell` throughout its chart.
- The joint amplitude is fixed `C_c^infinity`; constants may depend on a
  finite collection of its mixed derivative norms and on fixed chart
  comparability constants, never on `ell` or the scale length.

## Gates

1. Prove a self-contained one-dimensional lemma: if `|phi''|>=lambda>0`
   with fixed sign, then a compact smooth oscillatory integral is
   `O(lambda^(-1/2))`, with an explicit norm contract.
2. Iterate the lemma in the three separable variables, allowing a joint
   smooth amplitude, to obtain `|I_ell|<=C_W ell^(-3/2)`.
3. Check the three actual logarithmic phases have the required second
   derivatives and fixed-sign compact lower bounds after scale normalization.
4. Sum the complete kernels absolutely to get
   `sum_{ell<=L}|I_ell|<3C_W`, uniformly in `L` and independently of the base
   phase resonance.
5. Freeze Cycle 81/87/90 as the source of fixed smooth weights and Cycle 100
   as the sign-provenance boundary: no Möbius weight is inserted or needed.
6. State that nonsmooth/arithmetic coefficient variants are outside this
   theorem rather than hidden in the constant.
7. Replay symbolic derivative checks and deterministic numerical integrals
   only as consistency checks; theorem closure rests on the proved lemma.

## Outcomes

- Passing all gates closes the full perfect-power coefficient-scale
  multiplicity in the registered smooth stationary-alias model.
- Distinct core aggregation and other root branches remain open.
- No hostile audit is authorized.

## Replay

```sh
python3 proof/build_cycle_109_uniform_triple_b_v1.py --check
python3 -m unittest tests/test_cycle_109_uniform_triple_b_v1.py
```
