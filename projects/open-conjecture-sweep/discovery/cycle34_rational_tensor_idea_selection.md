# Cycle 34 idea selection: characteristic-zero affine obstruction

## Brainstorm

1. **Exact affine-basis lift (chosen).** Rebuild the GF(5) echelon only to
   select 1,228 original rows and pivot columns. Solve the corresponding
   square system over \(\mathbb Q\), verify the induced dependence across all
   1,394 columns, and clear denominators to an integer left-null certificate.
   If a column fails, promote that row and first failed column into an enlarged
   exact basis and continue under a small augmentation cap.
2. **Degree-one GF(2) census.** Expand products of uncovered predicates and
   test whether the extra monomials span one. This changes expressive power but
   risks recreating SAT at much larger width before characteristic zero is
   classified.
3. **Ownership-blocker auxiliaries.** Add the 12,264-pattern semantic family.
   This is genuinely broader, but no low-degree mechanism yet explains why the
   larger interface should compress.
4. **More modular primes.** Fast and useful for diagnosis, but no finite prime
   list proves rational inconsistency because a rational solution may have all
   tested primes in its denominator.

## Decision questions

- Idea 1: does the modular skeleton lift to an exact affine dependence with
  coefficient sum different from one, or does exact augmentation expose a
  larger characteristic-zero row rank?
- Idea 2: is the degree-one column set small enough to be meaningfully
  different from the prior SAT state space?
- Idea 3: is there an invariant that selects a small ownership subfamily
  before enumeration?
- Idea 4: do ranks stabilize across primes? Even a favorable answer would
  remain diagnostic rather than proof.

## Questioning the questioning

The tempting question is “how many characteristics fail?” That framing is
misleading: modular failure can merely record denominator primes. The actual
missing object is an exact affine dependence among evaluation rows. Asking
for that object turns characteristic zero into a construction with a local
falsifier—one failed integer column—rather than another rank survey.

The main risk is that exact coefficient heights, not mathematics, dominate
the run. The response is not dense Gram elimination: select a nonsingular
sparse square skeleton modulo 5, use exact PARI/GMP solving, verify every
column with Python integers, and allow only a frozen number of exact basis
augmentations. A cap has no algebraic meaning.

## Choice, rejected alternative, falsifier

Choose Idea 1. The companion independently recommended the same
characteristic-zero target and warned that finite-field ranks alone are not a
rational conclusion. Reject degree one for now because it spends expression
complexity before resolving the natural degree-zero field.

The claimed obstruction is falsified by any nonzero recombined predicate
column or by zero recombined RHS after denominators are cleared. A verified
rational solution of the restricted primal system would instead falsify only
the restricted-row obstruction, not prove a full tensor identity.
