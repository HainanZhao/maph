# Cycle 27 v2 correction: arbitrary prime counts

## Correction

`OBSERVED` error in the sealed v1 exposition: equal-cardinality grouping into
`J` blocks was stated as automatic for the prime atom, but the dyadic prime
count `M` need not be divisible by `J`. The conditional equal-mass theorem is
unchanged.

`PROVED` repair: retain `M'=J floor(M/J)` prime coordinates and discard
`r=M-M'<J`. Equal-modulus coefficients then give exactly equal block mass.
For every phase row, the discarded coordinates change the detector value by
at most `r`, so an original value at least `V` leaves a retained value at
least `V-r>V-J`.

At the critical scales

```text
J=X^o(1),  M=X^(1-o(1)),  V=X^(7/10-o(1)),
```

the relative detector and mass losses are respectively

```text
X^(-7/10+o(1)),  X^(-1+o(1)).
```

They cost no fixed power. Apply the v1 Hadamard dichotomy to the retained
coordinates with `V'=V-O(J)` and squared detector norm `M'`.

## Claim effect

The v1 algebraic theorem and its subpower-loss conclusion survive. Any exact
finite statement for the prime atom must use the retained coordinate set or
allow unequal-mass block corrections explicitly.
