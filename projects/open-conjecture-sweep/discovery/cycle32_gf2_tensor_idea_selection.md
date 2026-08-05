# Cycle 32 idea selection: algebra without repainting SAT

## Candidate engines

1. **Degree-zero GF(2) uncovered tensor.**  For each labeled time orbit, its
   uncovered predicate factors as a product of 13 coordinate-local bad-option
   indicators.  Seek coefficients whose XOR is the constant one function.
   Use exact evaluation-rank cuts and a memoized tensor verifier, adding the
   lexicographically first failed digit tuple until a certificate, rank
   contradiction, or cap.  This uses at most 1,394 predicate columns.
2. **Ownership-blocker polynomial calculus.**  Put one color variable on each
   time/coordinate pair and use Cycle 29's unary, binary, and ternary blocker
   monomials.  The axioms have low degree, but even after negation merging the
   variable and blocker expansions risk recreating the old SAT state space.
3. **Rational Gram certificate.**  Test whether the constant tensor lies in
   the rational span of uncovered predicates using the factorized Gram matrix.
   Positivity gives a clean verifier, but exact dense rational elimination at
   dimension 1,395 is a poor first runtime bet.
4. **Finite-field degree-one closure immediately.**  Multiply predicates by
   option variables before testing degree zero.  This spends the monomial
   budget before learning whether the smallest algebraic layer is already
   impossible.

## Questioning the questioning

Why does this differ from SAT?  It does not branch on digit tuples to prove
UNSAT.  It asks for one global signed parity identity among rank-one uncovered
functions.  A certificate is a short algebraic equality; a rank contradiction
is an exact no-go for degree zero only.

Why not trust a sampled linear solve?  Agreement on sampled assignments is not
a polynomial identity.  Every candidate must be checked against the full
Cartesian product by an exact memoized tensor decision diagram.  Its first
counterexample becomes a new equation; no probabilistic identity test is
promoted.

What can make the idea misleading?  A random-looking family of 1,394 rank-one
tensors is unlikely to span the constant function in an enormous assignment
space.  The engine is useful only if it falsifies itself cheaply or finds a
highly structured certificate.  Failure in GF(2), degree zero says nothing
about rational coefficients, higher degree, or the ownership ideal.

## Choice and falsifier

Choose the degree-zero GF(2) tensor CEGAR engine.  The main rejected alternative
is ownership polynomial calculus because it lacks a small monomial benchmark.
The certificate falsifier is one exact digit tuple where the claimed XOR is
not one.  The method falsifier is an exact inconsistent evaluation subsystem,
which proves no degree-zero GF(2) identity exists.  A verifier-node or equation
cap is only `CAP`.
