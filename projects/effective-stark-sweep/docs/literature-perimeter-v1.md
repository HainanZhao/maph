# Literature perimeter v1

Frozen: 2026-07-29 UTC

Scope: the eleven named primary works in
`data/literature-perimeter-v1.json`.  This is a bounded perimeter, not
a universal claim about all published mathematics.

## What is already proved or computed

1. **Shintani (1978)** is the foundational unconditional source for
   the special real-quadratic ray invariants and the index-two
   algebraicity engine.  The sweep industrializes explicit hypotheses,
   clearing exponents, labels, and height closure; it does not claim to
   replace Shintani's theorem.
2. **Stark (1980)** supplies the proved imaginary-quadratic rank-one
   result used by Engine C.
3. **Yamamoto (2009)** proves the factorization of Shintani's invariant
   into real-place components and its independence from cone choices.
   This is structural theory, not a certified finite census of
   algebraic packets.
4. **Tangedal (2007)** gives canonical double-sine expressions for the
   two real embeddings.  The general unit statements are conditional
   on the Stark units' existence, with special cases proved.
5. **Dummit--Sands--Tangedal (1997)** performs systematic numerical
   Stark-unit computation over totally real cubic base fields.  It is a
   computational precedent, but not the proposed real-quadratic
   unconditional archimedean census.
6. **Dummit--Sands--Tangedal (2003)** proves the refined equality for
   exponent-two abelian groups and fully handles many multiquadratic
   cases.  These belong naturally beside Engine A and must not be
   relabeled as new instances if the W1 support test lands in their
   proved zone.
7. **Cohen--Roblot (2000)** gives a Stark-unit algorithm and a table of
   real-quadratic Hilbert class fields below discriminant 2000.  Its
   analytic construction assumes Stark's conjecture, although the
   resulting field is independently verified.  Every overlapping W3
   case must be compared with this table.
8. **Roblot (2013)** proves index formulae assuming the Stark unit
   exists and obtains unconditional weak “up to absolute values”
   results in several cyclic degrees.  The sweep must distinguish an
   index constraint or absolute-value result from an oriented
   archimedean packet certificate.
9. **Kopp (arXiv:2411.06763v3)** proves the exact bridge from
   real-multiplication modular cocycles to square roots of Stark class
   invariants.  It is an analytic bridge, not an algebraicity census.
10. **Dasgupta--Kakde (2023)** proves Brumer--Stark away from 2 for CM
    extensions of totally real fields.  This is a finite-place/CM
    theorem and is not the same object as the real archimedean
    one-place invariants certified here.
11. **Tangedal--Young (2013)** computes Gross--Stark units over real
    quadratic fields using \(p\)-adic multiple-zeta/log-gamma methods.
    It is the closest large computational analogue, but it concerns
    the \(p\)-adic Gross--Stark setting rather than these archimedean
    invariants.

## Frozen novelty sentence

The allowed Phase-0 novelty claim is:

> Within the named perimeter, we found no systematic corpus that
> certifies, case by case and unconditionally, the oriented
> archimedean differenced ray invariants
> \(X_A=\exp Z'_{\mathfrak m}(0,A)\) over a finite range of real
> quadratic fields and one-place moduli, with explicit packet
> polynomials, Artin labels, and replay certificates.

The sentence must retain “within the named perimeter.”  It may be
strengthened only after a new hash-frozen perimeter revision.

## Mandatory overlap comparisons

- Cohen--Roblot's discriminant-\(<2000\) Hilbert-class-field table;
- any pair explicitly computed in Tangedal's special cases;
- any exponent-two support case covered by
  Dummit--Sands--Tangedal;
- Papers I–II's seven anchor bundles.

Agreement with conditional or numerical prior values is tagged
`VERIFIED_COMPARISON`; it does not retroactively make the prior method
unconditional.  A disagreement is a halt until conventions, field
labels, and orientation are reconciled.
