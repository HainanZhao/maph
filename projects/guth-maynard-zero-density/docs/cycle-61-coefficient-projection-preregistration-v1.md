# Cycle 61 preregistration: coefficient-projection inverse form

## Question

Express the Cycle-57 Hilbert coefficient family as an exact tensor projection
of prime-monomial fiber indicators. Prove its Bessel bound and characterize
near-saturation by coordinate marginals of the actual row-Fourier vector.

## Frozen setup

- Ordered tuple space is `Omega=P^(s+1)`.
- `L(tau)=q^m p_1...p_s` is the integer-frequency label map.
- `B` lifts a scalar label vector `beta` by `(B beta)_tau=beta_(L(tau))`.
- `P=I-J/M` on one prime coordinate and `C=P tensor ... tensor P` on all
  `s+1` coordinates.
- Hilbert synthesis is `A=C B`; equivalently its label coefficient is
  `a_n=C 1_(L^(-1)(n))`.
- Fiber size is bounded by `D_s=(1+floor(s/2))s!`.
- Evaluate `s=3,4` and write the first-coordinate marginal formulas for
  Fourier vectors `beta_n=sum_e omega_e n^(-ih_e)`.

## Outcomes

- `PROJECTED_BESSEL`: `A*A<=D_s I`; the exact loss
  `||B beta||^2-||A beta||^2` is the sum of non-full coordinate-ANOVA energies,
  and saturation forces every coordinate marginal small.
- `REPRESENTATION_FAILS`: the Hilbert coefficients are not `C`-projected
  fiber indicators or the operator bound fails.

No power saving, annihilator exclusion, `AMPR_s`, density gain, or interval
gain is asserted by the first outcome.
