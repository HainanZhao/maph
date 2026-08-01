# Cycle 14 prime-atom fractional-moment preregistration v1

## Claim boundary

`OBSERVED`: Cycle 13 isolates prime-supported coefficients as an exact
obstruction to product factorization. This cycle asks whether their failure
is arithmetic or merely caused by integer moment orders.

The cycle may prove an exact exponent-envelope theorem for the standard
mean-value treatment of a prime-supported length-`v^5` polynomial and state
the precise fractional-moment input that would beat it. It may not assert
that such a fractional-moment estimate is known, prove a zero-density gain,
or transfer a detector valid only for half-isolated zeros to all zeros.

## Frozen source map

- Guth--Maynard detector source and critical scales are those frozen in
  Cycles 12--13.
- Maynard--Pratt TeX SHA-256:
  `ec22dfdb8394b8ab4b228d0f438d19858015fc74330e247d08f36e5830782426`.
- Freeze their Definition `YHalfIsolated` (TeX lines 380--405) and
  Proposition `HalfIsolated` (lines 721--729): a `Y`-half-isolated zero has a
  large smooth `Lambda` polynomial for one of only polylogarithmically many
  lengths `U in [Y,Y^2]`.
- Freeze their stated consequence near TeX lines 201--208: half-isolated
  zeros already number at most `T^(2(1-sigma)+o(1))`.

Thus the `Lambda` detector is a source-valid product-decomposition target on
an already subcritical class. It cannot simply replace the full Type-I
detector at the critical bottleneck. This is a scope theorem, not a criticism
of that detector.

## Frozen prime-atom model

Let `P` be a Dirichlet polynomial of length `X=v^5`, sampled on a
one-separated set in an interval of length `H=v^12`, with threshold
`|P(t)|>=v^(7/2-delta)`. For integer `k>=1`, freeze the standard moment model

```text
integral_H |P|^(2k) <= v^(max(12+5k,10k)+o(1)).
```

This is the exponent supplied by `(H+X^k) ||coeff(P^k)||_2^2` under
`||coeff(P^k)||_2^2<=v^(5k+o(1))`. The resulting local-row exponent is

```text
E(k)=max(12-2k,3k) + 2k delta.
```

Freeze exact checks for integer `1<=k<=12`, and an algebraic proof over real
`k>=0`:

- the continuous minimum is at `k=12/5`, with `E=36/5`;
- the integer minimum is at `k=2`, with `E=8`;
- `k=3` gives `E=9`;
- the integer penalty is exactly `4/5`.

## Frozen interpolation comparison

Ordinary log-convex interpolation between the `2k=4` and `2k=6` integral
bounds, evaluated at `2k=24/5`, has exponent

```text
(3/5)*22+(2/5)*30=126/5.
```

After division by the threshold exponent `(24/5)*(7/2)=84/5`, this gives
local exponent `42/5`, worse than eight. Consequently ordinary interpolation
does not realize the continuous envelope.

## New engine target

`CONJECTURED`: prime/logarithmic frequency structure may support a direct
fractional moment estimate at `p=24/5` of the form

```text
integral_H |P(t)|^(24/5) dt <= v^(24+o(1)),
```

or a restricted large-value analogue with the same exponent. Markov would
then give local exponent `36/5`. The target is deliberately phrased for the
prime atom; applying the generic integer-moment estimate at a noninteger
power is forbidden.

Candidate constructions that remain authorized include squarefree exterior
tensors, decoupling for the logarithmic prime curve, random Euler-product
comparison with rigorous exceptional-set control, and a restricted weak-type
estimate proved directly rather than through a global `L^p` norm.

Falsifier: a lower-bound family of prime-supported polynomials with the
frozen coefficient scale whose `24/5` moment is `v^(24+kappa-o(1))` for some
fixed `kappa>0`. Generic Dirichlet-polynomial examples do not falsify the
prime-restricted target.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact integers/Fractions, no
  RNG, third-party libraries, or network.
- Enumeration cap: 12 integer moments.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
