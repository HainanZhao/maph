# Cycle 17: finite prime-phase separable search

## Claim boundary

`OBSERVED`: the preregistered finite search returns `BASELINE_APPROACHED`.
This is neither an asymptotic counterexample nor evidence sufficient to
promote the separable prime-phase conjecture.

## Registered outcome

The search completed all 80 alternating runs and 35 deterministic families.
The best registered row is the deterministic alternating-sign family at
`m=16`:

```text
count=67,       count exponent=1.5165222976,
target exponent=36/25=1.44,       baseline marker=3/2.
```

At `m=24`, optimized random seed 2 also crosses the target, with count 101
and exponent `1.452185`. The best registered outcomes at larger sizes are:

| `m` | best count | count exponent | family |
|---:|---:|---:|---|
| 32 | 98 | 1.322942 | quadratic index phase |
| 48 | 110 | 1.214218 | optimized random seed 7 |
| 64 | 165 | 1.227720 | quadratic index phase |

`OBSERVED`: the largest values in each best row occur in consecutive integer
clusters, consistent with local coherent spikes rather than a visibly
extended phase lattice. This is a structural clue only.

## Containment and exploratory follow-up

The preregistered `BASELINE_APPROACHED` label is retained because the
`m=16` exponent exceeds `3/2`. It is not weakened after seeing the larger
sizes.

`EXPLORATORY`: regressions of log best-count on log `m` have slopes between
approximately `0.47` and `0.72`, depending on which suffix is fitted. Large
finite prefactors make per-row exponents at `m=16,24` misleading. These fits
were not preregistered and carry no theorem status.

The result changes the next action: reconstruct the short coherent clusters
analytically and separate their contribution before searching for a diffuse
rank-one overlap obstruction. A valid asymptotic countermodel would need the
number of separated clusters, not merely the width or prefactor of one local
spike, to grow at exponent at least `36/25`.

## Evidence

- Result SHA-256:
  `8ce4a5592b1ce895b62c659b4568e10992f84f92574db9f2b3f799d1189b89f6`.
- Search source SHA-256:
  `13d194106631511d69fe71ec28aad7f4ca1ca583763a863d2aa214e292372dfc`.
- Preregistration SHA-256:
  `e6b46f7dd33f19fd606289a38860a6731b00813ad5bcad823c2ae8c91fbe666f`.
- Runtime: 74.492 seconds; peak RSS 55,192 KiB; CPython 3.12.3,
  NumPy 1.26.4.
