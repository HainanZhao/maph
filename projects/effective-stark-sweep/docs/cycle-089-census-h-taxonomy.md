# Cycle 089: exact H taxonomy and deduplicated Roblot sextic census

## Outcomes and claim boundary

`PROVED` — Every one of the 764 frozen order-six inverse-pair kernels
now has an exact Roblot Theorem 7.1 applicability decision.  This is a
prior-work eligibility statement, not a Stark packet identity.

`PROVED` — For each of 73 residual candidate 3-divisible sextic fields,
an exact irreducible cyclic cubic extension with relative discriminant
ideal norm one proves \(3\mid h_H\).  All four pre-existing
full-`bnfcertify` class-number-three controls pass the same independent
certificate.

`OBSERVED` — The complete 2,704-row H taxonomy has exclusive route
counts \(232+881+1591\), 1,079 rows with full Roblot weak coverage, and
1,359 rows failing every currently registered mechanism.  Five rows
remain mechanism-status-incomplete because of the separately preserved
quartic construction failures; no sextic row is incomplete.

`PROVED` — The \(\mathbb Q(\sqrt{21})\) wall is RQ-000692.  Its support
profile is \((2,6)\), Shintani index is six, A1--A3 and
\(3\nmid h_H\) pass, but the exact relative ramification index above
three is divisible by three, so Roblot Theorem 7.1 fails through wild
ramification.

## Optimization and containment

The initial sequential population attempted 119/764 kernels, completed
109, and recorded ten 600-second timeouts.  A timeout serializer bug and
seven orphaned GP children were contained; the failed route is preserved
in
`artifacts/roblot-sextic-population-sequential-partial-v0.json`.

The versioned replacement:

1. extracted all 764 primitive routes in 1.71 aggregate seconds;
2. collapsed them to 407 primitive field keys;
3. removed 25 keys by exact A3/\(S\)-equality failures;
4. certified 382 required distinct fields, reusing 48 already completed
   full certificates and running 334 new screens;
5. used the quotient class-group certificate for the prime-to-three
   branch and isolated 73 candidate 3-divisible fields;
6. closed all 73 by unramified cyclic cubic certificates in 303.27
   aggregate seconds.

The new field sweep had zero timeouts or construction failures and
peaked at 22,740 KiB per degree-12 field.  The unramified-cubic stage
peaked at 495,120 KiB.

## Evidence

- `artifacts/roblot-sextic-route-inventory-v1.json`
- `artifacts/roblot-sextic-field-inventory-v1.json`
- `artifacts/roblot-sextic-3class-v1.json`
- `artifacts/roblot-sextic-population-v1.json`
- `artifacts/census-h-taxonomy-v1.json`
- preregistration amendments v7--v11
