# Cycle 161: high-cell refinement into four-atom mass or a labelled star

## Claim boundary

`PROVED`: conditional on the Cycle-160 heavy labelled pair-difference cell,
one fixed finite refinement produces either a coefficient-weighted,
positive-real population of phase-aligned four-distinct-atom configurations,
or a labelled common-anchor star with large effective neighbor degree. This is
a structural dichotomy, not a proof that the Cycle-89 fourth-moment excess
occurs.

More precisely, suppose an original Cycle-160 cell has effective multiplicity
`C=L^2/E >= X^(1/75-o(1))`, where `L=sum_r|b_r|` and
`E=sum_r|b_r|^2`, with

```text
r=(u,v), u!=v, delta_r=z_u-z_v, b_r=a_u conjugate(a_v).
```

Discard only zero-weight edges, while retaining every label of every remaining
atom, anchor, denominator, tail, orientation, and coefficient. Choose fixed
half-open circular representatives and split the difference cell into 24
subcells of width `1/(24K)` and the coefficient arguments into 12 half-open
sectors of width `pi/6`. One of the resulting `B=288` classes has mass `L_j`,
square mass `E_j`, and effective multiplicity
`C_j=L_j^2/E_j>=C/B=X^(1/75-o(1))`.

Write `x_r=|b_r|`, `L=L_j=sum_r x_r`, and
`D_x=sum_(r incident to x)x_r` in this retained class, and put
`tau=X^(-1/300)`. The frozen `o(1)` slack is below `1/600`.

- If `max_x D_x<tau L`, the coefficient-weighted ordered mass of pairs
  `(r,s)` with four distinct endpoints is at least `(1-2tau)L^2`. For every
  such pair, and each `K<=k<=2K`,

  ```text
  Re(b_r conjugate(b_s)e(k(delta_r-delta_s))) >= |b_r b_s|/2.       (1)
  ```

  Thus a fixed proportion of the retained mass is an actual phase-aligned,
  coefficient-weighted colored four-atom population.
- Otherwise some fully labelled atom `x_*` has `D_x*>=tau L`. One of its
  incoming or outgoing oriented fans has incidence at least `D_x*/2`; its
  effective neighbor degree is at least

  ```text
  (D_x*/2)^2 / E_j >= tau^2 C_j/4 = X^(1/150-o(1)),               (2)
  ```

  and therefore at least the preregistered `X^(1/300-o(1))`. This is a star
  degeneracy, not yet a rational web.

This does not prove a rational web, transport seed, fourth-moment estimate,
density improvement, or interval improvement.

## Exact accounting

For the finite-refinement claim, let the nonempty classes have mass `L_j` and
square mass `E_j`. If every class had `L_j^2/E_j<C/B`, summing would give
`sum_j L_j^2<L^2/B`, contradicting Cauchy's `sum_j L_j^2>=L^2/B`. Therefore
one class has the stated retained multiplicity.

For the nondegenerate case, an ordered edge pair that is not disjoint shares
at least one endpoint. Its weighted mass is bounded by

```text
sum_x D_x^2 <= (max_x D_x)sum_x D_x < 2tau L^2.                  (3)
```

Here `sum_xD_x=2L`, including orientations and all coincidence rows. This
gives the first arm without dropping coefficients or labels. The inherited
Cycle-160 cutoff is frozen nonnegative and supported on integer `k` with
`K<=k<=2K`. In one retained circular subcell, the exponential phase change
there is at most `pi/6`; in one coefficient sector the coefficient phase
change is at most `pi/6`. Their combined angle is at most `pi/3`, proving
(1).

For the star arm, choose the heavier orientation, whose incidence is at least
`D_x*/2`; its sum of squares is at most `E_j`. The usual weighted
effective-support bound gives (2). Every incident edge retains its frozen
labels, so this is a consistently oriented labelled common-anchor
near-translate fan.

## Gate effect

`PHASE_ALIGNED_FOUR_CYCLE_OR_LABELLED_STAR_DEGENERACY_BANKED` is reached at
the structural level: Cycle 160's high cell cannot remain an unstructured
coefficient-free collision population. The next authorized action must use
one arm with its actual labels—either compile the positive-real four-cycle
mass into a moment saving, or analyse the labelled star for a rational web or
an admissible obstruction.
