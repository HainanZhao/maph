# Cycle 147: a strict collision core is positively coherent

## Claim boundary

`PROVED`: for an additionally chosen nonnegative dyadic moment cutoff, an
isolated collision cell of radius `1/(12bK)` has a positive real signed
contribution whenever its atom coefficients lie in a phase wedge of width at
most `pi/12`.  The fixed-phase leading smooth charts exposed in Cycle 123 are
compatible with this adverse case.  Negative high-pass cancellation must
come from residuals outside a wider `1/(4bK)` collar.

This does not prove that such a chart carries target-sized mass.  No paired
norm, endpoint, complete moment, density gain, or interval gain is proved.

## Exact frequency summation on the cell

Choose a nonnegative cutoff `U` supported on

```text
0<k<=bK
```

and let

```text
W_K=sum_k U(k/K).
```

For every oriented endpoint pair `e=(i,j)`, write its circle residual as
`t_e=z_j-z_i (mod 1)`.  On the strict core

```text
||t_e||_(R/Z)<=1/(12bK),                          (1)
```

every retained frequency satisfies

```text
|2pi k t_e|<=pi/6.                                (2)
```

Suppose the atom coefficients have the form

```text
c_j=e^(i gamma) r_j e^(i epsilon_j),
r_j>=0, |epsilon_j|<=phi.                         (3)
```

Then the oriented product `c_j conjugate(c_i)` has phase at most `2phi`.
Consequently, for any set `C` of strict-core pairs,

```text
Re sum_k U(k/K) sum_(e=(i,j) in C)
 c_j conjugate(c_i)e(k t_e)
 >=cos(pi/6+2phi) W_K sum_(e=(i,j) in C) r_i r_j. (4)
```

In particular, when `phi<=pi/12`, the cosine in (4) is at least `1/2`.
This is a lower bound in the adverse direction: exact summation in the
cheapest remaining variable, `k`, gives coherence rather than saving.

## Connection with the actual leading symbol

Cycle 123's leading stationary coefficient has one common explicit phase
`e(1/8)`; all displayed algebraic and Jacobian factors are positive.  A real
smooth symbol nonzero at an interior point has a smaller chart of constant
sign, so the common phase cancels from its oriented correlation products and
the block fits (3) with `phi=0`.

This is coefficient-faithful for that leading smooth subchart.  It is not a
full saturator because no lower bound is proved for the chart's share of the
original excessive quadratic form, and nonsmooth payload remains outside the
model.

## The halo cannot be frozen away

For exact common-phase coefficients, if

```text
||t||_(R/Z)<=1/(4bK),                             (5)
```

then every `cos(2pi kt)` is nonnegative.  Thus a negative real kernel value
capable of cancelling (4) must use residuals outside (5).  The mean-zero
identity from Cycle 146 balances the collision core only after those halo
pairs are restored.

Therefore the Cycle-146 single signed-cell pigeonhole is not, by itself, an
upper-bound strategy.  The next analytic unit must be a balanced bundle
containing a strict endpoint core and coefficient-faithful halo cells.  A
bundle may be discarded or promoted only according to its total signed
contribution, never according to its positive incidence mass.

## Gate effect

The gate becomes `COEFFICIENT_FAITHFUL_CORE_HALO_BUNDLE_OPEN`.
