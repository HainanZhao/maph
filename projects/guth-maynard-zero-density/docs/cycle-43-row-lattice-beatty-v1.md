# Cycle 43: row-lattice resonance becomes a curved prime Beatty strip

## Claim boundary

`PROVED`: for arithmetic-progression rows, large row Fourier resonance at a
one-prime coefficient ratio is equivalent to a prime pair lying in an
explicit exponentially curved strip. At the target row exponent the strip
has width `X^(-11/25)`, so it contains at most one integer shift and cannot
be replaced by its first-order linearization.

This is a stress model and arithmetic reduction. It does not reduce an
arbitrary separated row set to an arithmetic progression, prove the needed
prime-pair cancellation, close `LCAM_s`, or improve density or intervals.

## 1. Exact row resonance

For

```text
C_R={Delta,2Delta,...,RDelta},
```

the row Fourier sum is the Dirichlet kernel

```text
R_(C_R)(xi)
 =exp(-i(R+1)Delta xi/2)
   sin(R Delta xi/2)/sin(Delta xi/2).                 (1)
```

If

```text
|xi-2pi k/Delta| <= 1/(R Delta),                      (2)
```

then the sine-quotient bounds give `|R_(C_R)(xi)|>=cR` for an absolute
`c>0`. Thus spacing alone permits full row resonance in windows of width
`1/(R Delta)`.

## 2. Open one prime variable

Consider coefficient labels differing only by replacing `p` with `p+r`.
Their log ratio is

```text
xi=log(1+r/p).
```

Combining this with (2), and using the derivative of `log(1+r/p)` in `r`,
gives the equivalent strip up to absolute constant factors:

```text
|r-p(exp(2pi k/Delta)-1)| <= C p/(R Delta).           (3)
```

The exact center is a Beatty-type sequence with slope
`alpha_k=exp(2pi k/Delta)-1`. The remaining `s-1` ordinary prime factors and
the harmonic prime `q^m` weight this prime-pair strip inside `LCAM_s`.

## 3. Critical scales

At

```text
R=X^(21/25),       Delta=X^(3/5),       p asymp X,
```

the log-resonance and integer-shift widths are

```text
1/(R Delta)=X^(-36/25),
p/(R Delta)=X^(-11/25).                               (4)
```

The second width is `o(1)`, so for fixed `(p,k)` there is at most one
integer `r` in the resonant strip. For fixed small nonzero `k`, the shift
itself has scale

```text
r asymp p/Delta=X^(2/5).                              (5)
```

The error in replacing the exponential center by `2pi kp/Delta` is of
scale

```text
r^2/p=X^(-1/5),                                       (6)
```

which is larger than the admissible width `X^(-11/25)`. Therefore the exact
exponential center in (3) is mandatory; a first-derivative linearization
loses the resonance condition.

At maximal occupancy `R=X^(9/5)`, the integer-shift width is even smaller,
`X^(-7/5)`.

## 4. Arithmetic theorem exposed by the stress model

The AP-row obstruction can be defeated only by showing cancellation or
sparsity for prime pairs

```text
p prime,   p+r prime,
r=nearest_integer[p(exp(2pi k/Delta)-1)],             (7)
```

uniformly over the relevant `k`, with the residual prime-monomial weights
retained. This is a curved Beatty-prime-pair problem, not an ordinary fixed
shift problem. Averaging over `k`, applying a sieve before the subunit strip
is frozen, or proving equidistribution of the fractional parts
`{p alpha_k}` are concrete candidate mechanisms.

## Gate effect

`PROVED` stress reduction: the lead gate is
`CURVED_BEATTY_PRIME_PAIR_OR_NONLATTICE_ROW_OPEN`. For lattice-like rows,
prove a weighted curved Beatty-prime-pair estimate. For nonlattice rows,
prove that `R_C` cannot remain large on enough prime-monomial ratios. Neither
branch is currently closed.
