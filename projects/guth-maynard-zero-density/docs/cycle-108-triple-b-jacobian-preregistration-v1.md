# Cycle 108 preregistration: triple-B Jacobian summability

Date frozen: 2026-08-02 UTC.

## Claim boundary

This cycle traces only the leading square-root stationary amplitudes of the
three B-processes along a Cycle-107 actual scale ray. It may prove exact
scale homogeneity and absolute summability. It does not silently absorb
untraced arithmetic coefficients, nonleading stationary-phase remainders, or
cutoffs depending on non-invariant variables.

## Frozen data

- `c=D/(2pi)>0`, stationary coordinates `H>Delta>0`, and positive
  `(m,n,n')`.
- The three frozen stationary amplitudes are
  `sqrt(c Delta)/m`, `sqrt(c H)/n`, and
  `sqrt(c(H-Delta))/n'`, with the signs/phases kept separately.
- Along the actual scale ray,
  `(H,Delta,m,n,n')=ell(H0,Delta0,m0,n0,n0')`.
- The stationary evaluation points are
  `k*=c*c0*Delta/m`, `r*=c*H/n`, and
  `r'*=c*(H-Delta)/n'`.
- Every untraced coefficient/cutoff factor is isolated as a residual weight
  `omega_ell`; no bound on it is assumed unless stated.

## Gates

1. Prove the three stationary evaluation points are invariant in `ell`.
2. Prove the Jacobian product is
   `J=c^(3/2)sqrt(Delta H(H-Delta))/(m n n')` and
   `J_ell=ell^(-3/2)J0` exactly.
3. Prove `sum_{ell<=L}ell^(-3/2)<=3` and that the finite BV norm
   `L^(-3/2)+sum_{ell<L}(ell^(-3/2)-(ell+1)^(-3/2))` equals one.
4. Deduce
   `sum |omega_ell J_ell|<=3 J0 sup|omega_ell|`; in particular the leading
   scale multiplicity loses no power if the residual envelope is `X^o(1)`.
5. Keep the Cycle-107 geometric-phase bound as an optional stronger estimate,
   but do not require phase cancellation once absolute summability applies.
6. State the precise untraced inputs: arithmetic payload weights, cutoff
   variation outside invariant stationary coordinates, and B-process
   remainders. A failure must export one of these sequences.
7. Verify the identities symbolically and test finite sums/BV with rigorous
   rational inequalities.

## Outcomes

- Passing the gates removes the raw `Lambda` multiplicity from the leading
  perfect-power stationary term under a subpower residual envelope.
- It does not yet aggregate different cores or close nonleading terms.
- No hostile audit is authorized.

## Replay

```sh
python3 proof/build_cycle_108_triple_b_jacobian_v1.py --check
python3 -m unittest tests/test_cycle_108_triple_b_jacobian_v1.py
```
