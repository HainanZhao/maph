# Cycle 21 continuum-volume correction preregistration v2

## Correction boundary

Cycle 21 v1 used uniform measure in `y=log(p/X)` as its reference frame.
That continuous theorem is valid, and the stated closeness assumption is
logically sufficient, but uniform log measure is not the natural prime
quadrature limit on `[X,2X]`.

This correction preserves v1, records the cause, and replaces the reference
measure by

```text
dnu(y)=e^y dy,    0<=y<=log 2,
```

which has total mass one. It may reprove the determinant bridge with this
weight. It may not assert the required prime discrepancy or promote a
density or interval result.

## Corrected kernel

Register

```text
H_nu(t,s)=integral_0^(log 2) e^y exp(-i(t-s)y)dy.
```

Its diagonal is one. For `h=t-s!=0`, direct integration gives

```text
H_nu(h)=(2^(1-ih)-1)/(1-ih),
|H_nu(h)|<=3/|h|.
```

For `Delta`-separated ordered times, the absolute off-diagonal row sum is at
most

```text
epsilon_nu=6H_(k-1)/Delta.
```

All Gershgorin, perturbation, coloring, and determinant comparisons from v1
then hold with this corrected constant. With
`Delta>=X^(3/5)(log X)^2`, still

```text
epsilon_nu=O(X^(-3/5)/log X)=o(X^(-3/5)).
```

## Corrected prime discrepancy gate

Let `H_P` be the normalized prime Gram matrix and define

```text
eta_C=||H_P-H_nu||_op.
```

The corrected sufficient analytic input is uniformly
`eta_C=o(X^(-3/5))` on the retained color class. This remains
`CONJECTURED`; it is not claimed necessary.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact `Fraction` arithmetic for
  exponent and finite constant checks.
- No RNG, third-party library, or network.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
