# Cycle 77 discovery note: critical anchored saddle

Status: `EXPLORATORY`. Nothing in this note is proof.

At the critical cell

```text
(theta,alpha,kappa)=(1/3,1/3,8/75),
Delta=X^(3/5), Q=X^(1/3), eta=X^(-83/75),
```

choose one packet `(ell_0,n_0,q_0)`, with `n=a+q`. Dividing the relation for
another packet by the seed suggests the anchored incidence

```text
|n-c_0 q exp(2pi d/Delta)| <= O(eta),
c_0=n_0/q_0, d=ell-ell_0.                           (A)
```

The candidate surface in `(d,q)` is a saddle with Hessian determinant of
order `Delta^(-2)`. After `d=Delta*x`, `q=Q*y`, `n=Q*z`, it becomes a fixed
curved surface sampled on mesh `(Delta^-1,Q^-1,Q^-1)` with normalized tube
`eta/Q=X^(-36/25)`.

Candidate target: uniformly in a primitive seed, the number in (A) should be
`<X^(2/15+o(1))`. A ratio-only pair census appears to lose the anchor and has
random-volume exponent `37/75`, above its squared target `4/15=20/75` by
`17/75`.

The common-denominator embedding uses height `R=Delta*Q=X^(14/15)` and seems
to erase the anisotropic divisibility. The source applicability and every
exponent in this note must be checked independently under preregistration.
