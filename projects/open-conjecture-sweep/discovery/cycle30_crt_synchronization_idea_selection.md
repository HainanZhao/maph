# Cycle 30 idea selection: CRT synchronization rather than local coloring

## Brainstormed engines

1. **Gcd-stratified transport algebra.**  For the bad-time mask
   \(M_a=\{t:at\bmod q\in B_q\}\), classify speeds by \(g=\gcd(a,q)\).
   Speeds in one stratum are unit associates, and multiplication by the
   relative unit transports their masks on the *shared labeled time set*.
   Build the smallest unital pointwise algebra containing the canonical masks
   and closed under every allowed transport.  Its atoms are an exact quotient
   for arbitrary intersections and hence for the full uncovered product.  Ask
   whether this synchronization algebra is proper and small on H11 and frozen
   p199 base 4 / leaf 78.
2. **Coordinate-specific polynomial calculus.**  Translate the exact
   rank-three ownership blockers to a Boolean ideal and seek a bounded-degree
   Nullstellensatz refutation after CRT normalization.  This has high upside,
   but before a synchronization quotient it recreates tens of thousands of
   ownership variables and risks becoming another opaque SAT proof.
3. **Deleted-join topology.**  Form the deleted join of the 13 local legal
   complexes and seek a quotient with nontrivial homology.  This is genuinely
   different, but there is not yet a small exact complex whose homology is
   known to obstruct a full labeled ownership face.
4. **Fractional entropy/capacity.**  Apply Shearer-type inequalities to the
   rank-three blockers.  This is cheap, but it forgets precisely the CRT
   synchronization that survived Cycles 23--28 and is likely another capacity
   relaxation.

## Questioning the questions

Why not continue Cycle 29 with a generic rank-three solver?  Cycle 29's gain
is exactness and coordinate asymmetry.  Forgetting those labels reduces it
toward Cycle 6's necessary-only weak coloring, while feeding the complete
constraints to SAT merely recreates the already certified CNF engine.

What attractive shortcut is false?  Coordinates 3--12 all allow 14 digits,
but they are not interchangeable on the same times: each fixes a different
residue modulo 199.  Their mask families are related only by coordinate-
specific multiplicative transports, with nonunit speeds separated by gcd
strata.  A four-omitted-digit independent-set quotient would erase this
coupling and is rejected before execution.

Why might the transport algebra itself mislead?  The transport theorem can be
automatic while its generated pointwise algebra is the full function algebra
on labeled times.  In that case “normalization” gives no compression and must
be recorded as containment, not renamed as an invariant.  The discriminating
test is the fully stabilized atom count, not a few favorable characters.

Does this repeat Cycles 24--25?  Those cycles optimized nonnegative weights
constant on eight or twelve additive CRT classes inside selected block
capacity LPs.  This candidate instead uses exact multiplicative unit action,
all gcd strata, and closure under pointwise products so that the full
13-factor uncovered product is represented.  No floating objective or
class-constant weight is used.

## Choice, rejected alternative, and falsifier

Choose the gcd-stratified transport algebra.  It asks whether the local
rank-three complexes synchronize through a compact exact algebra, rather than
whether they are generically colorable.  The main rejected alternative is
polynomial calculus: it becomes worthwhile only if the transport algebra
first supplies a strict quotient.

The engine is falsified as a compression if exact transport fails for any
mask, the stabilized algebra does not reproduce every H11 direct-cover row,
or the p199 algebra has one atom per labeled time.  A proper algebra that still
cannot distinguish any H11 infeasible row is a non-discriminating containment
result.  A proper, control-passing algebra advances to an exact quotient
search; it is not itself a leaf certificate.
