# Cycle 178 working ledger: diagonal-aware fixed-beta fibre extraction

## Frozen question

See `docs/cycle-178-diagonal-aware-fibre-preregistration-v1.md`.  This is one
actual-mass engine: a heavy fixed-beta fibre is to become its own seeded
packet.  The remaining mass must then carry two distinct label fields.

## Candidate invariant — `CONJECTURED` pending exact replay

For a base row `(h0,j0)` and any other actual row `(h,j)`, write
`d=h-h0`, `b=j-j0`.  Then `|d alpha-b|<=2C/X`.  If `(d0,a0)` comes from the
first adjacent pair, the integer

```text
d0*b - d*a0
```

has absolute value at most `2C(d0+|d|)/X<=4CH/X<1`; hence it should vanish.
This would put every row in one residue class modulo the reduced denominator
`q=d0/gcd(d0,a0)` and improve the approximation using the fibre span.

## Planned exact checks

1. Prove the determinant, divisibility, span, primitive reduction, and
   one-sided packet propagation in a general exact-arithmetic convention
   module, including `a=0`.
2. Test adversarial finite rational examples and boundary cases: consecutive
   rows, sparse rows, zero numerator, negative numerator, and equality just
   below the integer-forcing cutoff.
3. Derive the exact diagonal/cross-label identity
   `U_cross=T^2-sum N_ell^2` and the heavy/light inequality with floors.
4. Assess whether either retained branch feeds an existing Cycle-165--176
   terminal entry.  Do not call it a recurrence bound or density advance
   without a separate coefficient/transport theorem.

## Rejected shortcuts

- `REJECTED`: C177's beta-zero rational-root ray is not a full-census
  saturator; it is only a one-label packet spike.
- `REJECTED`: an unqualified beta-free pair estimate is non-progress after
  C177.
- `REJECTED`: declaring a cross-label mass lower bound to be an analytic
  cross-label estimate.
