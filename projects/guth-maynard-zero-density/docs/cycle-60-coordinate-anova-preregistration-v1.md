# Cycle 60 preregistration: coordinate-ANOVA identity

## Question

Link E11's successive coordinate contractions exactly to E12's edge
cumulant by decomposing the tuple-energy density into coordinatewise
Hoeffding/ANOVA components.

## Frozen setup

- Coordinates are one powered prime `q` and `s` ordinary primes
  `p_1,...,p_s`, each with normalized counting measure.
- For finite row weights `z_t`, set
  `S(q,p_1,...,p_s)=sum_t z_t q^(-imt) product_j p_j^(-it)`.
- The energy density is `E=|S|^2`.
- For coordinate `j`, `A_j` is conditional expectation in that coordinate
  and `D_j=I-A_j`.
- For every coordinate subset `J`, define
  `E_J=product_(j in J)D_j product_(j notin J)A_j E`.
- Evaluate component counts and symmetry types for `s=3,4`.

## Outcomes

- `ORTHOGONAL_ANOVA`: the `E_J` form an exact orthogonal decomposition; each
  centered coordinate contributes `p^(-ih)-k(h)` (or its powered analogue),
  and the fully centered component has Cycle-56 quadratic form.
- `IDENTITY_FAILS`: the proposed component formula or orthogonality fails.

No component lower bound, restriction estimate, `AMPR_s`, density gain, or
interval gain is asserted by the first outcome.
