# Cycle 144: the inverse has not yet transported the coefficient vector

## Claim boundary

`PROVED`: the coefficient produced by an actual sparse-exponential second
moment is an oriented correlation coefficient depending on the Fourier
frequency.  The sealed Cycle-123/124 operator has such coefficient functions,
but the Cycle-132--136 inverse records only support and arithmetic labels; it
does not define a coefficient-preserving pushforward to the scalar `w_a` used
in the paired norm.  Thus Cycle 143's scalar moment hierarchy is a valid
generic target, not yet the actual operator's extracted moment hierarchy.

No signed-moment saving, coefficient-faithful saturator, paired norm,
endpoint, complete moment, density gain, or interval gain is proved.

## The exact coefficient type

For one Cycle-124 separated polynomial write

```text
T(ell)=sum_j c_j(ell)e(-ell z_j).                 (1)
```

Expansion is exact:

```text
|T(ell)|^2=sum_(j,j') c_j'(ell) conjugate(c_j(ell))
                         e(-ell(z_j'-z_j)).       (2)
```

Consequently a collision edge is not naturally weighted by one arbitrary
scalar `w_a`.  Its coefficient is the oriented product

```text
C_e(ell)=c_(e,+)(ell) conjugate(c_(e,-)(ell)),    (3)
```

which may vary with `ell`.  The coefficient-faithful edge object for a fixed
difference is therefore the complex measure

```text
nu_(d,ell)=sum_(e in E_d) C_e(ell)
 delta_(x_e,theta_e^-,theta_e^+,s_e^-,s_e^+),    (4)
```

with the tensor-frequency and rational-anchor labels retained as well.

## Where the existing bridge stops

Cycle 124 explicitly records weights `w_alpha(a,n;ell)`.  Its inverse says
that an excessive normalized second moment yields a labelled pair-collision
energy witness.  Cycles 132--134 then retain occupied modes, multiplicities,
rational centers, next-convergent matrices, orientations, and tails.  None of
their sealed maps retains (3), and Cycle 135 introduces `w_a` only in the
statement of a proposed generic paired norm.

This is a type mismatch, not evidence for or against cancellation.  The
Cycle-143 expansion

```text
M_m(d)=sum_a w_a x_a^m                            (5)
```

is exact for a frequency-independent scalar edge vector.  Before a
factorization theorem is proved, the actual formal hierarchy is instead

```text
M_m(d;ell)=sum_(e in E_d) C_e(ell)x_e^m.          (6)
```

In particular, no current artifact proves `M_0(d;ell)=0`, or even identifies
it with the scalar `M_0(d)` from Cycle 143.

## What the stationary amplitude does and does not supply

Before tensor separation, Cycle 123's leading coefficient is

```text
e(1/8)(q0/p0)g^(u+v)
 V(n'/Q)V(S/(p0Q))U(ell S/(p0cH0))
 W(-(u+v)/D)W(-v/D).                              (7)
```

All displayed algebraic and Jacobian factors are positive.  The only
explicit stationary phase is the common factor `e(1/8)`.  Hence any real
smooth symbol that is nonzero at an interior point has a smaller chart on
which (7) has fixed phase and sign.  This proves that the saddle itself does
not force zeroth-moment cancellation.  It does not prove a full saturator:
the frozen symbol class does not require every cutoff to be nonnegative, and
the coefficient-preserving inverse (4) is still absent.

Cycle 122's vanishing continuous moments do not repair this gap.  They kill
the zero Poisson mode before the nonzero aliases `ell~K` are selected; they
do not imply a vanishing identity for (6).

## New theorem contract

The next engine must prove one of two typed statements:

1. a weighted collision inverse transporting the measures (4), with their
   `ell` dependence, through the continued-fraction decomposition; or
2. a tensor-frequency factorization
   `C_e(ell)=t_d(ell)w_e+acceptable error` that genuinely reduces (6) to one
   scalar edge vector.

Only after that interface is sealed is it meaningful to seek cancellation
in the actual zeroth and higher path moments.

## Gate effect

The gate becomes
`COEFFICIENT_PRESERVING_WEIGHTED_COLLISION_INVERSE_OPEN`.
