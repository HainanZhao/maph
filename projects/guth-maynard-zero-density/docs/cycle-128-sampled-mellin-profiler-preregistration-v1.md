# Cycle 128 preregistration: sampled-Mellin alias profiler

Date frozen: 2026-08-02 UTC.

This is discovery only. Use `mpmath 1.2.1` at 80 decimal digits and no RNG.
Freeze

```text
D in {72,108,162},
xi in {16/25,7/10,23/30},
Q=round(D^(5/9)),
K=round(D^(5xi/3)).
```

Enumerate `Q<=n,n'<2Q` and every nonzero integer
`|a|<=floor(D log(2)/(2pi))`. Retain rows at both
`|n'-n exp(2pi a/D)|<=1/K` and `<=4/K`. Reduce each label `n'/n`, group
multiplicity by mode, and record:

- total hits, occupied modes, and maximum ray multiplicity;
- the volume proxy `DQ/K` and target `Q`;
- whether each reduced label occurs among the continued-fraction convergents
  of `exp(2pi a/D)` before denominator `2Q`;
- additive energy, most popular nonzero difference, and longest chain on the
  occupied mode set;
- how many rays exceed the finite-grid Cycle-125 threshold `(Q^3/K)^(1/4)`.

The profiler selects the next theorem formulation. No finite-grid sparsity,
continued-fraction pattern, or absence of a counterexample is proof.
