# Cycle 142: the recurrence compiler saturates at logarithmic depth

Let `r=A/B` be a fixed nontrivial reduced multiplier and write the chain
labels as `x_t=p_t/q_t` in lowest terms.  Exact reduction gives

```text
z_t=gcd(Ap_t,Bq_t)=gcd(A,q_t)gcd(B,p_t),
p_(t+1)=A p_t/z_t,
q_(t+1)=B q_t/z_t.                                (1)
```

Primewise, if `alpha=v_l(A)`, `beta=v_l(B)`, then `alpha*beta=0` and

```text
v_l(z_t)=min(alpha,v_l(q_t))+min(beta,v_l(p_t)).   (2)
```

Equations (1)--(2) show that the changing divisor color is determined by the
current rational label.  It is not an independent source of repeated
transition entropy.

Cycle 78 already supplies the relevant global constraint.  Along a complete
chain,

```text
x_t=x_0(A/B)^t,
height(x_t)>=2^t/(C^2N^2).                        (3)
```

Since every supported label has height `O(N)`, (3) gives

```text
t=O(log N).                                       (4)
```

Let `Lambda` be a valid logarithmic ceiling.  A fixed-difference graph on
`R` vertices with `L` edges forces a chain of `Lambda+1` edges only when

```text
L>=ceil((Lambda+1)R/(Lambda+2)).                  (5)
```

Thus the contradiction threshold has density

```text
L/R=1-O(1/log N).                                 (6)
```

No fixed exponent saving follows from (6).  Fiber saturation compares `L`
with an arithmetic capacity, not with `R`, and therefore cannot supply this
near-complete mode-graph density.

This proves a scoped saturation result for the fixed-multiplier
divisor/continuation compiler.  The surviving path components must be
returned to the paired Fourier norm, retaining each component start, the
scalar `r_d-g^d`, and the signed tails.  Analytic cancellation across those
components is not obstructed by this theorem.

No paired norm, endpoint, moment, density, or prime-interval theorem is
proved.
