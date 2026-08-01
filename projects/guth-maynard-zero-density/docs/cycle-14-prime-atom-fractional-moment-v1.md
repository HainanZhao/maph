# Cycle 14: the prime atom is an integer-moment quantization barrier

## Claim boundary

`PROVED`: in the frozen standard mean-value exponent model, the
prime-supported critical detector component cannot beat local exponent eight
at any integer moment order, although the continuous optimum is `36/5`.
`CONJECTURED`: a prime-specific fractional weak-type or moment theorem at
order `24/5` may realize that continuous optimum.

No such fractional theorem, zero-density gain, or interval improvement is
claimed.

## Exact envelope

For length `X=v^5`, time `H=v^12`, threshold `v^(7/2-delta)`, and integer
half-order `k`, the standard mean-value model gives

```text
I_(2k) <= v^max(12+5k,10k)+o(1),
R <= v^(max(12-2k,3k)+2k delta+o(1)).
```

`PROVED`: the two affine branches cross at `k=12/5`; the continuous minimum
is `36/5`. Among integer `k>=1`, the minimum is `8` at `k=2`, while `k=3`
already gives `9`. The exact cost of integer quantization is `4/5`, identical
to the gain furnished by the balanced fractional tensor.

## Why interpolation is not the missing theorem

Log-convex interpolation between the fourth-moment exponent `22` and the
sixth-moment exponent `30` gives moment exponent `126/5` at order `24/5`.
The threshold exponent is `84/5`, leaving local exponent `42/5`, worse than
the fourth moment. Ordinary interpolation therefore follows the chord
between integer moments, not the lower continuous envelope.

## Source scope

`PROVED` from the pinned Maynard--Pratt statements: their unconditional
smooth `Lambda` detector applies to `Y`-half-isolated zeros, and their stated
consequence already bounds all half-isolated zeros by
`T^(2(1-sigma)+o(1))`. At `sigma=7/10` this class is far below the GM
bottleneck. Replacing the full Type-I detector by that polynomial is thus not
source-valid for arbitrary zeros and would spend the new machinery on a
class already controlled.

The productive use of the prime atom must instead do one of two things:

1. extend prime/logarithmic detection from half-isolated zeros to a
   quantitatively large part of the clustered class; or
2. prove a fractional prime large-value theorem for the prime-supported
   remainder of the current detector.

## New engine: fractional prime restriction

The exact target is

```text
integral_H |P(t)|^(24/5) dt <= v^(24+o(1))
```

for the source-derived prime polynomial, or a restricted weak-type estimate
with the same exponent. It would give local exponent `36/5` immediately.
This is not a generic Dirichlet-polynomial conjecture: it must use unique
factorization, logarithmic prime frequencies, or source-specific coefficient
signs.

Candidate routes are a squarefree/exterior-power tensor that suppresses
repeated primes, decoupling for the logarithmic prime curve, a rigorous
random-Euler-product comparison outside a certified exceptional set, or a
direct distributional estimate for large values. A prime-supported lower
bound exceeding `v^(24+o(1))` at order `24/5` would falsify the target and
become the structural result.
