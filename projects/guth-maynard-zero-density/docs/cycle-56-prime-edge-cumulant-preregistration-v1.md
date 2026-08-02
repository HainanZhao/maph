# Cycle 56 preregistration: prime-coordinate edge cumulant

## Question

Construct the first E12 kernel by centering each actual prime coordinate
before tensorization. Determine its exact Gram formula, positivity,
diagonal-edge cancellation, diagonal norm, and signed expansion for `s=3,4`.

## Frozen conventions

- `k(h)=M^(-1) sum_p p^(-ih)` over one frozen dyadic prime block.
- `w_h(p)=p^(-ih)-k(h)` in normalized prime counting measure.
- `C(h,g)=<w_h,w_g>`.
- The powered coordinate uses `w_(mh)` and kernel `C_m(h,g)`.
- The all-centered `(m,s)` edge feature is
  `w_(mh)(q) product_(j=1)^s w_h(p_j)` on ordered prime coordinates.
- Evaluate `s=3,4`; do not collapse ordered coordinates to integer-frequency
  support in this cycle.

## Outcomes

- `SEALED_EDGE_CUMULANT`: the kernel is PSD, equals
  `C_m(h,g)C(h,g)^s`, vanishes if either edge is diagonal, and has an exact
  binomial signed expansion.
- `ALGEBRA_FAILS`: any one of those identities fails under the frozen
  conventions.

No analytic estimate, support-collapse theorem, `AMPR_s`, density gain, or
interval gain is asserted by the first outcome.
