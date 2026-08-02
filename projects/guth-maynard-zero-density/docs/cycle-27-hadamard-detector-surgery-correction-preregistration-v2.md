# Cycle 27 Hadamard detector-surgery application correction preregistration v2

## Correction boundary

The sealed v1 theorem assumes exactly equal block mass and remains valid.
Its prose application to an arbitrary dyadic prime count omitted the possible
remainder modulo `J`. This correction may repair only that application by
discarding fewer than `J` prime coordinates. It may not strengthen the v1
dichotomy or promote an analytic gain.

## Frozen repair

For `M` equal-modulus prime coordinates and `J` a power of two, retain

```text
M'=J floor(M/J)
```

coordinates, partition them into `J` blocks of size `M'/J`, and discard
`r=M-M'<J`. If the original detector value has modulus at least `V`, the
retained detector value has modulus at least `V-r>V-J` by the triangle
inequality. Its squared norm is `M'` rather than `M`.

For `J=X^o(1)`, `M=X^(1-o(1))`, and `V=X^(7/10-o(1))`, register

```text
r/V=X^(-7/10+o(1)),   r/M=X^(-1+o(1)).
```

Thus v1 applies with `V'=V-O(J)` and loses no fixed power.

## Checks

- Exact `M=11`, `J=4`: retain eight, discard three.
- CPython `3.12.3`, exact `Fraction`, no RNG/network.
- Pin the v1 artifact and do not overwrite it.
