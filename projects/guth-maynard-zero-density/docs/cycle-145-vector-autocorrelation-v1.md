# Cycle 145: the actual zeroth moment is a selected autocorrelation

## Claim boundary

`PROVED`: the `ell`-dependent edge coefficients admit an exact
vector-valued Taylor compiler.  For a complete fixed-difference class, the
zeroth vector moment is a coefficient autocorrelation and has a
positive-definite Fourier representation.  The arithmetic inverse inserts a
selection mask; cancellation must be proved for that mask or obtained from a
separate Gram factorization.

No selected-autocorrelation saving, paired norm, endpoint, complete moment,
density gain, or interval gain is proved.

## Hilbert-space moment expansion

Fix an edge set `E`, labels `|x_e|<=B`, coefficient functions `C_e(ell)`,
and `|ell|<=L`.  Put

```text
F(ell)=sum_(e in E) C_e(ell)e(ell kappa x_e),
M_m(ell)=sum_(e in E) C_e(ell)x_e^m.              (1)
```

Let `D_ell` denote multiplication by `ell`.  Componentwise Taylor expansion
gives, for every integer `R>=1`,

```text
F=sum_(0<=m<R) (2pi i kappa)^m/m! D_ell^m M_m
  +Rem_R.                                         (2)
```

With

```text
z=2pi |kappa| L B,
A=||(sum_e |C_e(ell)|)_ell||_2,
```

the elementary exponential remainder yields

```text
||Rem_R||_2 <= exp(z) z^R/R! A.                   (3)
```

Therefore

```text
||F||_2 <= sum_(0<=m<R) (2pi|kappa|)^m/m!
                         ||D_ell^m M_m||_2
          +exp(z)z^R/R! A.                        (4)
```

This is the coefficient-faithful replacement for Cycle 143's scalar Taylor
series.  In particular, the first lock is the vector norm `||M_0||_2`; the
frequency factors in all higher terms are explicit and cannot be absorbed
into an unweighted scalar moment.

## Complete differences give autocorrelation

Before the arithmetic collision selection, index coefficient atoms by the
mode `a`.  The complete difference-`d` zeroth moment is

```text
R_ell(d)=sum_a c_(a+d)(ell) conjugate(c_a(ell)).  (5)
```

Zero-extending the coefficient sequence, direct expansion gives

```text
sum_d R_ell(d)e(-d theta)
 =|sum_a c_a(ell)e(-a theta)|^2 >=0.              (6)
```

Thus the sequence of complete zeroth moments is positive definite.  It does
not generically vanish: `R_ell(0)=sum_a|c_a(ell)|^2`, and a fixed-phase
nonnegative local coefficient chart has nonnegative products at every
selected difference.

## The arithmetic mask is the live object

The continued-fraction inverse does not retain every pair.  Its actual
zeroth term must have the form

```text
R_ell^chi(d)=sum_a chi_(a,d,ell)
 c_(a+d)(ell)conjugate(c_a(ell)),                 (7)
```

where `chi` records the collision cell, denominator shell, rational-tail
conditions, tensor term, and orientation.  An arbitrary mask destroys (6).
The identity survives if `chi` itself is proved to be a positive Gram or
convolution kernel, but no such factorization is currently sealed.

Equation (7), rather than an unweighted rational-ray count, is now the
minimal analytic target.  A fixed-phase selected block is adverse inverse
data, not yet a full saturator, because it must also carry enough of the
original excessive norm.

## Gate effect

The gate becomes
`ARITHMETIC_SELECTION_MASK_AUTOCORRELATION_OPEN`.
