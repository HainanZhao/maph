# Cycle 94 preregistration: triple-B entropy atlas

## Claim boundary

This cycle may prove only the exact combined stationary phase from the
`k,r,r'` B-processes, its central stationary equations, the anchor-difference
relation, and its projective Hessian degeneracy. It may not bound the
stationary-alias branch, discard nonzero Poisson modes in `(h,Delta)`, close
the signed moment, or promote density/interval consequences.

## Frozen conventions

- `e(x)=exp(2pi i x)`, `c=D/(2pi)`, `h'=h-Delta`.
- `m` is the positive `k`-stationary alias after matching signs.
- `n,n'` are the positive B-process indices of the negative-`r` and
  positive-`r'` logarithmic phases respectively.
- `c0>0` is the original frozen packet anchor and is not normalized away.

## Frozen gates

1. Sum the three stationary values with their registered signs and show that
   all linear terms and all `log c` terms cancel.
2. Obtain
   `F=Delta log(c0 Delta/m)-h log(h/n)+(h-Delta)log((h-Delta)/n')`.
3. Verify
   `F_h=log((h-Delta)n/(hn'))` and
   `F_Delta=log(c0 Delta n'/(m(h-Delta)))`.
4. Solve the central equations `F_h=F_Delta=0` and derive
   `(h-Delta)/h=n'/n` and `m=c0(n-n')`.
5. Compute the full `(h,Delta)` Hessian and prove its determinant is zero
   identically, not only at stationarity.
6. State nonzero Poisson modes in `(h,Delta)` as open projective entropy
   aliases; do not treat the zero-mode relation as exhaustive.

## Failure rule

Any uncancelled linear or `log c` term, loss of `c0`, nonzero Hessian
determinant, or claim that central stationarity exhausts the alias branch
halts the cycle.

