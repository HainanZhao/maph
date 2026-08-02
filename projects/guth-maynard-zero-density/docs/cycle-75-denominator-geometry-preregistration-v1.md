# Cycle 75 preregistration: denominator-average geometry

## Question

Freeze the exact geometry and exponent contract shared by E14 and E15 before
attempting an analytic denominator-average theorem.

## Frozen setup

- `C=Delta/(2pi)>0` and `Y(a,q)=C log(1+a/q)`.
- Dyadic scaling is `a=A x`, `q=Q y`, where `0<A<=Q` and
  `1<=x,y<=2`; `A=X^(alpha+o(1))`, `Q=X^(theta+o(1))`.
- The shifted coordinate is `n=q+a`.
- The registered exponent domain is
  `0<=alpha<=theta`, `theta+kappa<=11/25`.
- Cycle 70 supplies packet count `X^(lambda+o(1))` from curve-index
  injectivity, where `lambda=3/5+alpha-theta`.
- Cycle 74 supplies packet count `X^(theta+w+o(1))`, where
  `w=min(alpha,max(0,alpha+1/10-theta/2))`.
- The strict packet target is `X^(6/25-kappa)`.

## Exact checks

1. Derive both Hessians in `(a,q)` and `(n,q)` and prove that their
   determinants agree under the unimodular coordinate change.
2. Normalize to `(x,y)` and prove explicit absolute upper and lower bounds
   for both Hessian singular values in units of `CA/Q`.
3. Prove that primitive integer pairs remove exact radial repetitions and
   that the shifted phase factors multiplicatively.
4. Form the combined banked exponent
   `B=min(lambda,theta+w)`, derive the live residual, and maximize the exact
   additional saving `B+kappa-6/25` on the registered domain.

## Outcomes

- `NORMALIZED_CURVATURE_CONTRACT`: all four checks hold; seal the exact E14
  and E15 input contract without claiming an analytic saving.
- `GEOMETRY_CORRECTION`: any proposed identity, uniform bound, atlas
  condition, or maximum fails; record the corrected statement and do not
  promote the candidate.

No denominator-average estimate, seed-extraction theorem, powered saving,
density gain, or interval gain is asserted by either outcome.
