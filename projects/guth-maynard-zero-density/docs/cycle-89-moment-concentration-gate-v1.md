# Cycle 89: upper-band success forces fourth-moment concentration

## Claim boundary

`PROVED`: an exact Hölder reduction turns the upper signed range into a
quantitative fourth-moment concentration problem.  Conditional on a
diagonal-size second moment, meeting the raw first-moment target at frequency
exponent `xi` forces fourth-moment excess `2xi-116/75` above the
diagonal/random scale.  This excess is zero at `58/75` and grows to `2/3` at
the Fourier ceiling `83/75`.

No second- or fourth-moment estimate, large-value theorem, Fourier-band
closure, density gain, or interval gain is proved.  Fourth-moment
concentration is necessary under the stated second-moment hypothesis; it is
not sufficient for cancellation.

## Exact interpolation

For `a_k=|S_k|>=0`, write

```text
L1=sum_k a_k,  M2=sum_k a_k^2,  M4=sum_k a_k^4.
```

Hölder applied to `a_k^2=a_k^(2/3)a_k^(4/3)` gives

```text
M2 <= L1^(2/3) M4^(1/3),
M4 >= M2^3/L1^2.                                  (1)
```

This is a deterministic inequality for every frequency block.

## Exponent gate

Suppose, conditionally, that the Cycle-86 diagonal scale is also a lower
bound,

```text
M2 >= X^(xi+14/15-o(1)),                           (2)
```

and that the desired raw target holds with saving `delta>=0`,

```text
L1 <= X^(31/25-delta+o(1)).                        (3)
```

Then (1) forces

```text
M4 >= X^(3xi+8/25+2delta-o(1)).                    (4)
```

The diagonal/random fourth-moment scale `K(DQ)^2` has exponent

```text
xi+28/15.                                         (5)
```

Subtracting (5) from (4), the necessary excess is

```text
2xi-116/75+2delta.                                (6)
```

At `xi=58/75`, (6) is `2delta`; at `delta=0` this is exactly the Cycle-86
split.  At `xi=83/75`, the required excess is `2/3+2delta`.

## Strategic consequence

`CONJECTURED`: the upper band should be attacked by an inverse fourth-moment
theorem.  Either the arithmetic projector cannot generate the excess in
(6), proving a saturation barrier for this route, or the excess localizes on
Mellin aliases and produces the anchor/valuation/transport structure needed
by E16.  Generic claims of additional cancellation are no longer the primary
upper-band target.

## Gate effect

E14D-high advances from `SIGNED_LARGE_VALUE_SPARSITY_OPEN` to
`MOMENT_CONCENTRATION_OR_SATURATION_INVERSE_OPEN`.

