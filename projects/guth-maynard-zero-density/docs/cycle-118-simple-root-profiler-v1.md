# Cycle 118: simple roots do not collapse to integer-jet classes

`OBSERVED`. The frozen profiler evaluated 80-decimal residuals on three
scaled grids. It retained respectively 4,360, 9,584, and 21,477 near rows;
3,461, 7,400, and 16,128 passed the Cycle-115 local simple-root threshold.

In every grid, the dominant simple signatures were

```text
J0_NONZERO/J1_NONZERO/OPPOSITE,
J0_NONZERO/J1_NONZERO/SAME.
```

At `D=48`, these classes contain 9,184 and 6,754 rows, while the two
zero-jet classes together contain only 190. Thus the discovery hypothesis
that simple roots concentrate on `J0=0` or `J1=0` is falsified on the frozen
grid.

This is not proof of asymptotic abundance or a universal negative statement.
It redirects the theorem target: simple roots require a derivative-weighted
discrepancy or covering theorem for

```text
A=B exp(2pi a/D)+C exp(2pi b/D),
```

with same-sign and opposite-sign sectors retained separately. The full
payload `(A,B,C,a,b,J0,J1,delta,eta)` remains available in representative
rows. No moment, density, or interval conclusion is promoted.
