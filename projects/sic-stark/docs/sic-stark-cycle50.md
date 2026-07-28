# SIC--Stark research cycle 50: complete complex characteristic packet

## Result

The dimension-seven packet is now machine-readable at the complex-cocycle
level, not only at the level of absolute values.

For each of the \(48\) nonzero characteristics, the certificate records:

- \(Q(p)\);
- the exact SF phase as a \(\zeta_{56}\)-exponent;
- the normalized-overlap sign;
- the exact raw-shin \(\zeta_{56}\)-exponent;
- the numerical absolute value;
- both conductor-lowered characteristics;
- their \(\Upsilon\) elements and positive representatives;
- reduced HNF moduli and ray-class logs;
- Kopp's sign class and exponent; and
- the predicted zeta log-square.

The packet therefore contains \(48\) characteristic rows and \(96\)
lowered-factor rows.

## Reproducibility

Run

```text
python3 scripts/dimension_seven_packet_certificate.py
```

The output schema is
`sic-stark-dimension-seven-complete-packet-v1`.

This closes the bookkeeping problem that caused repeated ambiguity in the
dimension-four review.  The remaining issue is not an unidentified phase or
ray class; it is exact algebraic certification of the positive roots.

