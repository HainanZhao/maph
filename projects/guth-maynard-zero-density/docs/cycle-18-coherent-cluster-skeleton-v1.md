# Cycle 18: coherent clusters reduce to a separated recurrence skeleton

## Claim boundary

`PROVED`: all bounded-width coherent clusters can be removed at an exact
`X^(3/5+o(1))` multiplicity cost, reducing the prime-atom target to an
`X^(3/5)`-separated skeleton bound. `OBSERVED`: the skeleton bound itself is
open.

## Local cluster theorem

At threshold `V=X^(7/10)`, the checked classical large-values estimate on an
interval of length `Y` becomes

```text
#large rows <= X^o(1)[X^(3/5)+Y X^(-2/5)].
```

Taking `Y=2X^(3/5)` shows that every such interval contains at most
`X^(3/5+o(1))` one-separated large rows. This contains the consecutive
clusters seen in Cycle 17 without assuming that their coefficients or shapes
are coherent in any particular way.

## Skeleton reduction

Choose a maximal `X^(3/5)`-separated subset `C` of the full row set `W`.
Maximality makes its radius-`X^(3/5)` intervals cover `W`, and the local
theorem gives

```text
|W| <= X^(3/5+o(1)) |C|.
```

Therefore it suffices to prove

```text
|C| <= X^(21/25+o(1))
```

to obtain `|W|<=X^(36/25+o(1))`. The generic `X^(8/5)` bound corresponds to
the weaker skeleton exponent one. The missing saving remains exactly
`4/25`: clustering is quarantined, not counted as progress toward the power
saving.

## New arithmetic object

The principal object is now a recurrence skeleton of ordinates separated by
more than `X^(3/5)` on which the same prime coefficient vector has size
`X^(7/10)`. Equivalently, after squaring, the same Veronese tensor has large
evaluation on widely separated rows of the Schur-square prime Gram matrix.

This is materially narrower than the unrestricted separable tensor gate:
identical and bounded-gap row countermodels are excluded by construction.
The next proof attempt should exploit the long gaps through prime exponential
sum estimates, a recurrence entropy lemma, or an inverse theorem for repeated
phase alignment.
