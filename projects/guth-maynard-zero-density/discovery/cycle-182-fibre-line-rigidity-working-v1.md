# Cycle 182 working ledger: common-intercept fibre-line rigidity

## Frozen question

For one C181 common-intercept packet, test whether every participating
non-singleton actual fibre is an exact rational affine progression. The
preregistration fixes the state, rational separation cutoff, and required
consequences.

## Working derivation (CONJECTURED until sealed)

Two pair slopes in one fibre are within `4C/X` of each other. Once
`4CH^2/X<1`, Farey separation forces one reduced slope `A/U`. A reference row
then fixes the intercept; C181 makes it `p/v`. The congruence

```text
v*A*h + p*U == 0 (mod U*v)
```

should force `v|U` and one height class modulo `U`. Convexity of the affine
residual between the extreme rows should fill every intermediate lattice
point.

## Candidate engine and falsifier

The candidate engine is a primitive-denominator capacity ledger indexed by
`(p,v,A,U,residue)`. Its immediate falsifier is a legal three-row fibre whose
two pair slopes reduce differently, or a legal intermediate lattice row that
misses the original strip. Exact rational test vectors must include nonzero
beta and a nontrivial `v|U` example.

## Log

- 2026-08-02: opened from the C181 common-intercept packet. No result
  promoted.
