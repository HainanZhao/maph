# Cycle 37: degree-two signed product functional

## Claim boundary

`PROVED`: for p199 base 4 / leaf 78, the constant function is not in the
rational span of the direct uncovered predicates multiplied by one-hot
coordinate monomials of degree at most two. This concerns the frozen direct-
predicate calculus only. It does not classify nonproduct duals, ownership
semantics, higher degree, the leaf itself, or LRC(13).

## Exact compression theorem

For local mass-one vectors \(u_i\), write
\(z_{t,i}=\langle u_i,b_{t,i}\rangle\). A coordinate is *ordinary zero* when
\(z_{t,i}=0\), and *strong zero* when
\(u_i(a)b_{t,i}(a)=0\) for every local option.

All products \(mF_t\) with \(m\) supported on at most two distinct
coordinates have zero product-functional value if and only if either:

- at least three coordinates are ordinary zero; or
- at least one coordinate is strong zero.

Three ordinary zeros survive deletion of any two contractions. A strong zero
kills a multiplier whether or not its coordinate is selected. Conversely, if
there are at most two ordinary zeros and none is strong, select all zero
coordinates and at each choose an option with nonzero point factor; this gives
a nonzero multiplier of degree at most two. Same-coordinate quadratic
monomials reduce by the one-hot rules to degree one or zero.

## Exact result and replay

The sealed Cycle 36 normals leave 54 predicates and 2,010 raw degree-two
labels escaping. The Cycle 37 exact span search found new local integer normals
after 7,012 states. Every local mass is one; every predicate has either three
ordinary zeros or a strong zero; the maximum coefficient magnitude is five.

Primary exact contraction checks give zero for 1,394 degree-zero, 221,646
degree-one, and 16,170,400 distinct-coordinate degree-two labels. An
independent route rebuilt all direct masks as sets and explicitly reevaluated
every raw label. It reproduced the ordinary/strong histograms, unit mass, and
zero nonzero-count in all three degrees.

Applying this signed functional to a hypothetical degree-\(\le2\) identity
would give zero on the generator side and one on the constant side, a
contradiction. The functional is signed, not positive.

## Falsifiers

Any local mass different from one, any nonzero raw contraction, a mismatch in
the three-ordinary-or-strong equivalence, or an incorrect one-hot reduction
invalidates the claim.
