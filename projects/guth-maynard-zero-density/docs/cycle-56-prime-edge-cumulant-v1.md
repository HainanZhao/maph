# Cycle 56: an actual-prime centered edge kernel

## Claim boundary

`PROVED`: centering each ordered prime coordinate before tensorization gives
a positive semidefinite edge kernel

```text
E_(m,s)(h,g)=C_m(h,g) C(h,g)^s,
C(h,g)=k(h-g)-k(h)conj(k(g)).
```

It vanishes exactly when either edge is diagonal and has diagonal

```text
E_(m,s)(h,h)=(1-|k(mh)|^2)(1-|k(h)|^2)^s.
```

Its signed expansion has `2(s+1)` terms and coefficient `l1` norm
`2^(s+1)`, hence only constant cost for `s=3,4`.

This cycle works on ordered prime coordinates. It does not yet prove that
the kernel survives integer-frequency support collapse with acceptable
norm, nor any `3/50`, `AMPR_s`, density, or interval gain.

## Construction

On the frozen dyadic prime block with normalized counting measure, set

```text
k(h)=M^(-1) sum_p p^(-ih),
w_h(p)=p^(-ih)-k(h).
```

Then

```text
<w_h,w_g>=k(h-g)-k(h)conj(k(g))=C(h,g).
```

For the powered coordinate use `w_(mh)(q)`. The all-centered edge feature is

```text
W_(m,s),h(q,p_1,...,p_s)
  = w_(mh)(q) product_(j=1)^s w_h(p_j).
```

Independence of the ordered coordinates gives the displayed Gram formula.
It is positive semidefinite because it is an actual Gram kernel; equivalently
it is the Schur product of `C_m` and `s` copies of `C`.

If `h=0`, then `w_0=1-k(0)=0`, proving exact diagonal-edge annihilation. The
diagonal norm follows from `||w_h||^2=1-|k(h)|^2`.

## Signed cumulant expansion

Write

```text
A=k(h-g),                  B=k(h)conj(k(g)),
A_m=k(m(h-g)),             B_m=k(mh)conj(k(mg)).
```

Then

```text
E_(m,s)=(A_m-B_m)(A-B)^s
       = sum_(e=0)^1 sum_(j=0)^s
         (-1)^(e+j) binom(s,j)
         [A_m if e=0 else B_m] A^(s-j)B^j.
```

For `s=3` this has eight terms and coefficient `l1` norm `16`; for `s=4`
it has ten terms and norm `32`. The coefficient sum is zero, recording the
annihilation of a completely coherent scalar model.

## Why this differs from Cycle 55

Cycle 55 centered the row Gram only after all prime coordinates had been
collapsed. The abstract simplex could then erase the entire centered matrix.
Here centering occurs inside each actual coordinate and before tensorization.
The residual remembers the nonlinear prime curve through
`k(h-g)-k(h)conj(k(g))`; it is not determined by a common projection size.

## Analytic dichotomy to prove

`CONJECTURED`: on the popular-edge family produced after three ordinary
contractions, either

1. the spectrum/trace of `E_(m,4)` yields at least the missing `3/50`; or
2. many pairs satisfy approximate multiplicativity
   `k(h-g) approximately k(h)conj(k(g))` simultaneously at scales `1,m`,
   which forces a logarithmic recurrence family for E13/Cycle 52.

The next exact step is to push this ordered-coordinate cumulant through the
Cycle-51 support-partition map and quantify every collision stratum.

## Gate effect

E12 advances to `EDGE_CUMULANT_SUPPORT_COLLAPSE_3_50_OPEN`.
