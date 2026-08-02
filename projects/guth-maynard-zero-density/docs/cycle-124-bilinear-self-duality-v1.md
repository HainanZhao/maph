# Cycle 124: the separated alias operator is norm-self-dual

Set

```text
a=u,  b=u+v,  alpha=q0/p0.
```

Cycle 123's phase becomes

```text
e(-ell n'g^a)e(-ell alpha m g^b).                 (1)
```

The remaining coupling is smooth: on fixed charts it depends on normalized
variables

```text
rho=ell/K,  x=n'g^a/Q,  y=alpha m g^b/Q           (2)
```

and on the compact mode coordinates `a/D,b/D`. A Fourier expansion on a
fixed box gives, for every fixed `epsilon,A>0`, a tensor decomposition with
rank and coefficient `l1` norm `O(X^epsilon)` and uniform remainder
`O(X^(-A))`. This follows by truncating at `X^(epsilon/C)` and taking enough
fixed derivatives of the frozen smooth symbol. All anchor and mode labels
remain in the separated weights.

Consequently, up to `X^epsilon` separated terms and a power-negligible error,
the normalized Cycle-123 operator is a sum of expressions

```text
sum_(ell~K) T_1(ell)T_alpha(ell),                 (3)

T_alpha(ell)
 =sum_(a,n)w_alpha(a,n;ell)e(-ell alpha n g^a),   (4)
```

where the two lengths in (4) are `D` and `Q`. Cauchy--Schwarz gives

```text
|(3)| <=
 (sum|T_1(ell)|^2)^(1/2)
 (sum|T_alpha(ell)|^2)^(1/2).                     (5)
```

The diagonal second-moment estimate for either factor is

```text
sum_(ell~K)|T_alpha(ell)|^2 << K D Q X^epsilon.   (6)
```

Inserting (6) into (5) gives `K D Q X^epsilon`, exactly the Cycle-87
lower-band target. Moreover, (4) is the original primal sparse-exponential
polynomial, with bounded rational anchor `alpha`, up to a sign, smooth
weights, and harmless tensor-frequency shifts.

Thus the Cycle-119--123 transform chain is norm-neutral at the level of
tensor separation, Cauchy, and diagonal second moments. It removes the false
positive volume term and exposes the correct signs, but it does not make the
remaining diagonal estimate easier by exponent alone.

The statement has an inverse form. If one separated term in (3) exceeds
`L K D Q`, then (5) forces at least one of the two normalized second moments
to exceed its diagonal size by a factor at least `L`. Expanding that moment
returns a labelled pair-collision energy witness for the points
`alpha n g^a`, suitable for the Cycle-90/92 collision-web branch.

This is not an impossibility theorem for correlated bilinear cancellation,
nor for methods outside the stated tensor--Cauchy architecture. No
simple-root closure, complete moment, density gain, or interval gain is
proved.
