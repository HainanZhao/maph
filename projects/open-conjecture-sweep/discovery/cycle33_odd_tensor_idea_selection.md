# Cycle 33 idea selection: change characteristic before degree

## Candidate engines

1. **Degree-zero GF(3) and GF(5).**  Reuse the exact 1,394 rank-one uncovered
   predicates and deterministic 4,243-row evaluation set.  Perform bit-sliced
   modular elimination with full provenance.  A candidate must pass the same
   exact tensor CEGAR used conceptually in Cycle 32; an inconsistent subsystem
   closes that field immediately.
2. **Degree-one GF(2).**  Multiply the uncovered predicates by option variables.
   This may escape the parity no-go, but changes the column geometry from 1,394
   compact tensors to a much larger, not-yet-counted family.
3. **Rational Gram span.**  Odd signed coefficients are most naturally tested
   over the rationals, where a positive Gram norm gives exact verification.
   Dense rational elimination at dimension 1,395 is much more expensive than
   two small-characteristic screens.
4. **Ownership signature auxiliaries.**  Replace direct tensors by Cycle 29's
   unary/binary/ternary blockers.  This lowers axiom degree but risks expanding
   12,264 symbolic patterns into a larger state space without a variable census.

## Questioning the questioning

Why can odd fields differ from GF(2)?  Parity identifies plus and minus and can
force left-null contradictions unavailable when coefficients 2, 3, or 4 are
distinct.  Testing two odd characteristics is a cheap discriminator, not a
proxy for the rationals.

Why is sampled consistency still insufficient?  A solution on 4,243 rows can
fail elsewhere in the huge digit product.  The full tensor decision diagram
must either certify the identity or return the first exact tuple to add.

What could make both field tests misleading?  Modular inconsistency can occur
at small primes while a rational identity exists, and degree zero may simply
be too weak.  Therefore a two-field negative result is a bounded family
closure, not evidence that algebraic proof is saturated.

## Choice and falsifier

Choose GF(3) and GF(5) in parallel, with identical rows and independent field
provenance.  The main rejected alternative is degree-one GF(2) because its
monomial count has not earned the runtime.  A field is closed by a displayed
linear combination whose 1,394 predicate columns sum to zero and whose right
side sums to one.  A proposed identity is falsified by one full-domain digit
tuple where its weighted predicate sum is not one.
