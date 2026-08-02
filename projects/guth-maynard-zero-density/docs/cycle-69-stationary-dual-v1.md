# Cycle 69: folding destroys Hessian curvature but exposes `21/25`

## Claim boundary

`PROVED`: Poisson summation in the curve index transforms the folded phase
into a stationary Legendre phase homogeneous of degree one in `(m,k)`. Its
two-dimensional Hessian determinant vanishes identically, so a generic
nonzero-Hessian estimate cannot supply the missing Cycle-68 saving after
frequency folding.

`PROVED`: at the maximum folded frequency `X^(36/25)`, the stationary dual
index has exponent `36/25-3/5=21/25`, exactly the critical skeleton target.
This exponent identity does not itself bound either object. No primitive
Poisson, packet, recurrence, powered, density, or interval gain is proved.

## Poisson transform and stationary phase

With a smooth fixed-proportion cutoff `w` and `x=ell/Delta`, Poisson
summation writes

```text
sum_ell w(ell/Delta)e(m(exp(2pi ell/Delta)-1))
 =Delta sum_k integral w(x)
  e(m(exp(2pi x)-1)-k Delta x) dx.                  (1)
```

The stationary equation is

```text
2pi m exp(2pi x)=k Delta.                           (2)
```

For matching signs and ratios in the fixed support of `w`, put

```text
u=k Delta/(2pi).
```

Then `exp(2pi x)=u/m`, and the stationary value of the phase in (1) is

```text
Psi(m,k)=u-m-u log(u/m).                             (3)
```

## Exact degeneracy

The phase obeys

```text
Psi(lambda m,lambda k)=lambda Psi(m,k).             (4)
```

Writing `D=Delta/(2pi)` and `u=Dk`, direct differentiation gives

```text
Psi_mm=-u/m^2,
Psi_mk=D/m,
Psi_kk=-D^2/u.
```

Therefore

```text
det Hess_(m,k) Psi
 =(-u/m^2)(-D^2/u)-(D/m)^2
 =0.                                                (5)
```

This is an exact structural loss caused by folding to the product frequency
`m=rq'`. It does not contradict Cycle 63: the original surface in `(h,ell)`
has nonzero Monge--Ampère determinant, while its stationary projective dual
has only ratio curvature.

## Stationary-index scale

Equation (2) and the fixed support of `w` imply

```text
k asymp m/Delta.
```

Thus stationary terms begin at `m` exponent `3/5`. At the Cycle-66 ceiling
`m<=X^(36/25+o(1))`, their index satisfies

```text
k<=X^(36/25-15/25+o(1))=X^(21/25+o(1)).             (6)
```

The right side is exactly the target cardinality of the separated prime-row
skeleton. This suggests a possible interface: treat stationary aliases as a
projective code of size at most the desired skeleton scale, rather than seek
two-dimensional curvature that (5) proves absent.

## Strategic route

`PROVED` scoped boundary: a proof that folds completely to `(m,k)` and then
invokes only a nonzero two-dimensional Hessian cannot work, because that
Hessian is zero. The surviving options are:

- retain an unfurled variable such as `b`, `q'`, or the original `h` so the
  nondegenerate transport geometry remains visible;
- exploit one-dimensional curvature in the projective ratio `k/m` together
  with the arithmetic coefficients;
- map the at-most-`X^(21/25)` stationary-index family into the existing
  skeleton/seeded-recurrence engines.

The third option is `CONJECTURED`; the exponent match in (6) is necessary
bookkeeping, not a theorem identifying stationary indices with zero rows.

## Gate effect

E13 becomes
`UNFURLED_TRANSPORT_OR_PROJECTIVE_X21_25_DUAL_OPEN` inside the broader
`PRIMITIVE_POISSON_X31_25_OR_SEEDED_RECURRENCE_OPEN` gate.
