# Cycle 169: source-coupled target-label energy no-go

## Claim boundary

`PROVED`: unnormalized common-source provenance and separate edge/packet
marginal masses alone cannot force common target-label energy. The exact mixed
energy is a two-source-copy pair sum, and arbitrary nonnegative marginals
admit a two-label anticorrelated realization with zero energy.

This theorem does not use the actual exponential curve or the detailed
Cycle-165--167 fibre geometry. It proves no label overlap, compatible join,
recurrence, E7/E9 skeleton, density gain, or interval result.

## Exact identity

For a labelled source space with nonnegative weights, let `E_L` and `P_L` be
the unnormalized edge and packet pushforwards. Then

```text
M=sum_L E_L P_L
 =sum_(omega,omega') w(omega)e(omega)w(omega')p(omega')
       1_[L_E(omega)=L_P(omega')].                  (1)
```

Thus `M` is a bilinear statistic on two independent labelled source copies.
It is not the same-source diagonal, and it cannot be created by normalizing
the two branch populations after they are selected.

## Sharp anticorrelation model

For arbitrary nonnegative prescribed **total** edge and packet masses `A,B`,
use two target labels and two common-source atoms: an edge-only atom of mass
`A` at label zero and a packet-only atom of mass `B` at label one. Then

```text
sum_L E_L=A,       sum_L P_L=B,       M=0.           (2)
```

The source provenance is fully retained. Hence no inequality using only these
total masses and their common-source origin can imply positive `M`. This says
nothing about prescribed label-wise vectors with overlapping support.

## Consequence

Cycle 165's disjunctive terminal selections and Cycle 167's edge extraction
must be supplemented by a genuine geometric correlation theorem before
Cycle 168 compatibility can be invoked. The next engine must use an actual
exponential/fibre invariant that forbids the two-label anticorrelation model,
or else turn the realized target-label separator into a quantitative structural
output.
