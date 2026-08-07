# Lane B Gate B5 report: transfer equivalence and first width ranks

## Outcome

`PROVED`: the width-three 256-state carrier is ordinary zero-field
slice-transfer space in a Walsh basis:

```
Q H = 2^(w^2) H K.
```

Consequently the carrier itself supplies no new topological mechanism.

`CERTIFIED_NUMERICAL`: for the frozen `n=4` embedding, homology basis, and
binary ordering, the central twist flattenings are generically full:

```
R(4,3)=8,
R(4,4)=32,
```

for nonuniform weights, homogeneous anisotropic weights, and a homogeneous
isotropic specialization.  Both `GF(1000000007)` and `GF(1000000009)` give
nonzero central determinants with complete elimination transcripts.

These statements do not determine the basis-optimized rank, the longitudinal
saturation rank `R_infinity(w)`, or an asymptotic law in `w`.

## Compression-source audit

| source | exact contribution |
|---|---|
| fixed frontier | carrier dimension `2^(w^2-1)` |
| global spin flip | one factor of two removed from `2^(w^2)` spins |
| Walsh transform | invertible basis change; no carrier reduction |
| Arf transform | local and rank-preserving only in an adapted handle split |
| repeated handles | locality of twist dependence along `n` |
| translation invariance | repeated cores, not smaller generic bond rank |

## Genus table and attribution

| `w` | frontier | proved minimum-genus information |
|---:|---:|---|
| 2 | 8 | `0` |
| 3 | 256 | `n-1` |
| 4 | 32768 | `2n-3` for even `n`; between `2n-3` and `2n-2` for odd `n` |

The all-size width-three minimum-genus claim explicitly invokes
Millichap--Salinas Theorem 4.  Our contribution there is the explicit nested
embedding and relative-homology construction.

## Gate status

No B0--B3 terminal classification is made.  The next decisive gate is B6.2:
increase `n` at `w=3,4` and distinguish `R(n,w)` from a proved saturation rank
`R_infinity(w)`.  Width five is deliberately deferred.

