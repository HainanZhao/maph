# Cycle 53: self-duality needs a multilinear trigger

## Claim boundary

`PROVED`: failure of `AMPR_3` or `AMPR_4` does not by itself cross the
diagonal threshold in the one-shot Cycle 50 Halász--Montgomery inequality.
The missing trigger exponents are respectively `11/5` and `16/5`.

This is scoped to one-shot Bessel/Halász--Montgomery on the full distinct
support. It does not obstruct coordinatewise Bessel, a centered higher trace,
entropy conditioning, or use of the original row large value before support
collapse. No engine is terminated and no density or interval gain is proved.

## Exact ledger

If `AMPR_s` fails at exponent `s+31/10`, dyadic selection of one among
`X^(3/10)` harmonic orders produces a row/value class

```text
R=X^r, V=X^v,       r+2v>=s+14/5.                    (1)
```

The coefficient square norm and the distinct support in Cycle 50 each have
exponent `s+1`. The diagonal in the phase-aligned inequality is therefore
`X^(r+2s+2)`, while its left side is `X^(2r+2v)`. A factored off-diagonal is
forced only when

```text
r+2v>2s+2.                                           (2)
```

The difference between (2) and the guaranteed level (1) is

```text
(2s+2)-(s+14/5)=s-4/5.                               (3)
```

It equals `11/5` for `s=3` and `16/5` for `s=4`.

## Redesign

Cycle 52 remains useful as the inverse theorem once a large support
correlation has been produced. The production mechanism must avoid paying
the whole `X^(s+1)` support dimension in one step. Two registered designs
are:

1. **coordinatewise Bessel:** expose the `q` coordinate and the `s` ordinary
   prime coordinates successively, applying Cycle 48 or row separation at
   each stage;
2. **centered support trace:** subtract the diagonal and lower collision
   strata from a higher Gram trace before using the self-dual leading term.

The first target is an exact tensor ledger showing how much support dimension
each exposed coordinate removes and where the `7/50` Huxley--Sargos saving
enters.

## Gate effect

The popular-difference route is retained behind
`MULTILINEAR_TRIGGER_THEN_TWO_SCALE_INVERSE_OPEN`.
