# Cycle 162: mass-sensitive high-cell extraction

## Claim boundary

`PROVED`: under the conditional Cycle-89 excess, the Cycle-160/161 inverse is globally mass-sensitive. It yields either coefficient-weighted positive-real four-distinct-atom mass `>>_B A2^2X^(1/75-o(1))`, or a labelled consistently oriented star family with actual squared edge mass `>>_B A2^2X^(1/150-o(1))` and individual effective degree `X^(1/300-o(1))`. Here `B=288` is fixed.

No excess, coordinate pullback, rational web, moment estimate, density, or interval result is proved.

## Mass extraction

For Cycle-160 cells let `L_I=sum|b_r|`, `rho_I=sum|b_r|^2`, and `C_I=L_I^2/rho_I`. The local Schur decomposition gives

```text
sum_k U(k/K)|P_off(k)|^2 <= C K sum_I L_I^2.                       (1)
```

The diagonal/off-diagonal split and conditional excess force `sum_I L_I^2 >> A2^2X^(1/75-o(1))`. Cells with `C_I<X^(1/100)` contribute at most `A2^2X^(1/100)`, so one deterministic dyadic high level retains this scale after only logarithmically many levels.

For each retained parent cell, its `B` refined masses satisfy `sum_jL_j^2>=L_I^2/B`. Classes below `X^(1/100)/(2B)` contribute at most `L_I^2/(2B)`, so high refined classes retain at least `L_I^2/(2B)`. Apply Cycle 161 class-by-class. Its nondegenerate arm contributes a fixed proportion as positive-real four-atom mass. In the star arm the heavier orientation has incidence at least `tau L_j/2`, hence

```text
sum D_(j,or)^2 >= tau^2/4 sum L_j^2 >>_B A2^2X^(1/150-o(1)).     (2)
```

Every such star has effective degree at least `tau^2X^(1/100)/(8B)=X^(1/300-o(1))/(8B)`. This is literal star-edge mass, not merely certificate provenance.

## Gate effect

`GLOBAL_ALIGNED_FOUR_CYCLE_MASS_OR_WEIGHTED_HIGH_DEGREE_STAR_INVERSE_BANKED`. The next action is a label-preserving coordinate pullback through `z_(d,q)=c0q exp(2pi d/D)`.
