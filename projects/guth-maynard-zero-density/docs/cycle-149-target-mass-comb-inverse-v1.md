# Cycle 149: excess endpoint mass forces near-perfect anti-alignment

## Claim boundary

`PROVED`: the exact occupancy threshold for the Cycle-148 endpoint comb is
`R_C/D=N/Q`.  If a strict endpoint population exceeds that threshold by a
factor `Lambda` while the full polynomial retains diagonal second moment,
the exact complement must be within relative Hilbert distance
`O(Lambda^(-1/2))` of the negative endpoint comb.  One endpoint denominator
then has a quantified negative-correlation witness.

The theorem does not exclude that anti-alignment.  No full second moment,
endpoint, complete moment, density gain, or interval gain is proved.

## Global budget comparison

Let `C` be the strict endpoint operator, `R` its exact complement on the same
frequency block, and

```text
F=C+R.
```

If `R_C` endpoint modes lie in a denominator shell `N`, Cycle 148 gives

```text
||C||_2^2 >> KQ^2 R_C/N.                          (1)
```

The full diagonal budget is

```text
B0=KDQ.                                           (2)
```

Thus the endpoint-to-global ratio is

```text
Lambda=(R_C/D)(Q/N).                              (3)
```

The critical occupation is exactly

```text
R_C/D=N/Q.                                       (4)
```

This is much smaller than full density whenever `N<<Q`.

## Hilbert-space inverse

Assume, with fixed chart constants absorbed into `C_diag`, that

```text
||F||_2^2<=C_diag B0,
||C||_2^2>=Lambda B0.                             (5)
```

Since `R+C=F`, division by `||C||_2` gives the exact inverse

```text
||R+C||_2/||C||_2<=sqrt(C_diag/Lambda).           (6)
```

The reverse triangle inequality also yields

```text
| ||R||_2/||C||_2-1 |<=sqrt(C_diag/Lambda).       (7)
```

If `Lambda=X^(omega+o(1))`, then the complement is
`X^(-omega/2+o(1))`-close to `-C`.  This is substantially stronger than a
large unsigned collision count: the same coefficient vector must reproduce
the endpoint comb with opposite phase across almost the whole frequency
block.

## A retained denominator witness

Discarding the power-negligible Cycle-148 Poisson error, write the ideal comb
as

```text
C_comb(k)=Q sum_(h|k) A_h,
A_h>=0.                                           (8)
```

From (6), with `epsilon=sqrt(C_diag/Lambda)<1`,

```text
Re <R,C_comb>
 =Re <R+C_comb,C_comb>-||C_comb||_2^2
 <=-(1-epsilon)||C_comb||_2^2.                    (9)
```

Expanding (8),

```text
sum_h A_h Re<R,Q 1_(h|k)>
 <=-(1-epsilon)||C_comb||_2^2.                    (10)
```

Therefore at least one actual endpoint denominator satisfies

```text
Re<R,Q 1_(h|k)>
 <=-(1-epsilon)||C_comb||_2^2/sum_h A_h.          (11)
```

Equation (11) retains a concrete modulus rather than exporting anonymous
negative mass.  Substituting `k=h ell` into the complement is the next
analytic problem.

## Structural consequence

A supercritical endpoint population has only two possible outcomes:

1. the full lower-band moment is super-diagonal; or
2. modes outside that endpoint class generate a near-perfect negative copy
   of its divisor-incidence comb, including the common coefficient vector.

The second alternative is a coefficient-sensitive inverse theorem.  It is
not yet impossible: halo modes or other rational denominators may have the
required negative projection.

## Gate effect

The gate becomes `DIVISOR_COMB_ANTIALIGNMENT_EXCLUSION_OR_MODEL_OPEN`.
