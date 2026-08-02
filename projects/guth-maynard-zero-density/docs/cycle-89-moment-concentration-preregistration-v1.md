# Cycle 89 preregistration: moment-concentration inverse gate

## Claim boundary

This cycle may prove only an exact norm-interpolation reduction and its
exponent consequences.  It may not promote a second- or fourth-moment
estimate, a large-value theorem, a Fourier-band closure, a density gain, or
an interval gain.

## Frozen objects

For a dyadic frequency block let `a_k=|S_k|>=0` and

```text
L1=sum_k a_k,  M2=sum_k a_k^2,  M4=sum_k a_k^4.
```

Freeze the atom exponent `14/15`, raw `L1` target `31/25`, lower/upper split
`58/75`, and Fourier ceiling `83/75` from Cycle 86.

## Frozen calculation

1. Derive the exact Hölder inequality
   `M2<=L1^(2/3) M4^(1/3)` and its rearrangement
   `M4>=M2^3/L1^2`.
2. Under the explicitly conditional hypotheses
   `M2>=X^(xi+14/15-o(1))` and `L1<=X^(31/25+o(1))`, compute the necessary
   fourth-moment exponent.
3. Compare it with the diagonal/random scale `K(DQ)^2`, exponent
   `xi+28/15`, and compute the excess at `xi=58/75` and `xi=83/75`.

## Promotion and failure rules

- All algebraic identities and inequalities may be `PROVED` after exact
  rational replay.
- The hypotheses on `M2`, `L1`, and any arithmetic interpretation of fourth-
  moment excess remain `CONJECTURED` unless separately proved.
- Any mismatch in an endpoint or rational exponent halts this cycle; no
  endpoint may be adjusted after the calculation.

