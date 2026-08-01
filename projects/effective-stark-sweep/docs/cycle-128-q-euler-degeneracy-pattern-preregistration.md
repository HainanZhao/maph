# Cycle 128 — quadratic Euler-degeneracy pattern preregistration

## Objective and claim boundary

Find a structural characterization of the 346 rows in the frozen
1,560-row quadratic-support stratum whose packet-value-orbit polynomial
is `X-1`.  Discovery uses the already labelled finite corpus and is
therefore `EXPLORATORY`; it may suggest a statement but cannot prove
one.  A promoted theorem must follow from the pinned imprimitive
Euler-factor formula and exact conductor/local-character calculations.

The population, case ordering, support definition, and 346 positive
labels are frozen by
`artifacts/engine-a-euler-degeneracy-v1.json`.  No row may be removed,
relabelled, or treated as missing.

## Frozen feature families

The new exact export may inspect only these preregistered families:

1. per supported quadratic character: ray coordinates, primitive
   conductor, and primitive ray-group coordinates;
2. every prime ideal dividing the selected finite modulus but not the
   primitive conductor, including its exponent, absolute norm,
   underlying rational prime, residue degree, ramification index, and
   primitive-character value;
3. row-level combinations of finite norm, base discriminant, support
   count, ray-group invariants, number of removed primes, and the local
   data in item 2;
4. predicates formed by universal or existential quantification of an
   item-2 local condition across the supported characters.

No floating-point values, packet coefficients, RQ identifier ordering,
or post-result feature family may enter a claimed characterization.

## Candidate statements and gates

The theorem-level candidate fixed before the enriched export is:

> For a supported quadratic character \(\chi\), its imprimitive factor
> at zero vanishes exactly when at least one prime deleted from the
> selected finite modulus has trivial primitive-character value.
> Consequently the quadratic packet is value one exactly when this
> condition holds for every supported character.

This is to be derived from
\[
 E_\chi=\prod_{\mathfrak p\mid\mathfrak f,
 \mathfrak p\nmid\mathfrak f_\chi}(1-\chi^*(\mathfrak p)).
\]
For quadratic \(\chi^*\), every defined local value is \(\pm1\), so a
factor is respectively zero or two.

The following gates are frozen:

- exact local criterion: zero character-level false positives and zero
  character-level false negatives over all 2,232 supported occurrences;
- packet criterion: zero row-level false positives and zero row-level
  false negatives over all 1,560 rows;
- any coarser pattern must be printed with its full confusion matrix
  and the least RQ counterexample in each nonempty error cell;
- a coarse pattern is a theorem candidate only if its zero-error status
  is subsequently derived without using the census bounds;
- the known 346 count is a finite corollary, never the theorem itself.

## Resource and replay boundary

The exact enriched export is capped at 20 minutes wall time and 2 GiB
resident memory under the pinned PARI/GP 2.15.4 route.  It has no RNG.
The output must record source hashes and retain all row and character
records.  A separate audit will recompute the stated confusion matrices
from the export and the frozen v1 labels.

## Stop condition

Stop this cycle after either (a) a bound-independent local theorem and
its complete finite corollary are written and replayed, or (b) every
preregistered coarse feature family has surviving counterexamples.  In
case (b), preserve the exact local criterion as the only theorem and
record the failed simplifications rather than selecting a post-hoc
subpopulation.
