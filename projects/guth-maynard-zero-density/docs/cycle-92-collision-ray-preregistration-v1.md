# Cycle 92 preregistration: collision-ray inverse lemma

## Claim boundary

This cycle may prove only the finite/asymptotic combinatorial rigidity of the
Cycle-90 collision relation: fixed-`a` ray uniqueness, cross-`a` injectivity,
multiplicity versus primitive denominator, and dyadic excess extraction. It
may not prove the collision count `O(QX^o(1))`, convert a ray web to a
transport seed, close the equal-height branch, prove a moment theorem, or
promote a density/interval gain.

## Frozen hypotheses

- Positive parameters satisfy `K/Q -> infinity` and `KQ/D -> infinity`.
  On the lower band their minimum exponent margins are respectively
  `16/25-1/3=23/75` and `16/25+1/3-3/5=28/75`.
- `a` lies in a fixed interval `|a|<=cD`.
- `n,n'` lie in fixed positive dyadic intervals comparable to `Q`.
- A collision satisfies
  `|n'-n exp(beta a/D)|<=C/K`, with fixed `C` and `beta=2pi`.
- The primitive label of `(n,n')` is `(p,q)=(n'/g,n/g)`,
  `g=gcd(n,n')`.

## Frozen gates

1. Prove that two collisions at the same `a` have the same primitive label,
   using Farey separation and `K/Q -> infinity`.
2. Prove that one primitive label cannot occur at two distinct `a`, using
   the mean-value theorem and `KQ/D -> infinity`.
3. If a fixed-`a` class has multiplicity `M`, prove its primitive denominator
   is `O(Q/M)`.
4. Partition multiplicities into powers of two. From total collision count
   `C_tot`, extract a dyadic `M` and at least
   `C_tot/(O(M log Q))` distinct `a` values with injective primitive labels
   of denominator `O(Q/M)`.
5. State the exact dichotomy at threshold `QX^epsilon`: either the collision
   count is within the analytic target or the extracted web is the explicit
   E16 output. Do not call the web a transport seed.

## Failure rule

Any loss requiring `K>Q^2`, any use of unproved transcendence separation,
failure of cross-`a` injectivity, or loss of the primitive labels halts the
cycle.

