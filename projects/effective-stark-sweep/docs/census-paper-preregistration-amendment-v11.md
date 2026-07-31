# Census-paper preregistration amendment v11: exact 3-class obstruction

Frozen: 2026-07-31 UTC, after the deduplicated field sweep isolated 73
candidate 3-divisible fields, before constructing an unramified cubic
extension for any residual field.

For each residual field \(H\), attempt to construct the exponent-three
Hilbert-class-field quotient suggested by the computed class group.
The construction is promoted only after independent exact checks:

1. the relative polynomial is monic cubic and has no root in \(H\),
   hence is irreducible;
2. its relative discriminant ideal has norm one, hence the extension is
   unramified at every finite prime;
3. the cubic polynomial discriminant is a square in \(H\), hence the
   irreducible cubic extension is cyclic.

An unramified cyclic cubic extension proves \(3\mid h_H\), so Roblot
Theorem 7.1 is exactly nonapplicable.  This argument does not rely on
the conditional class-number value after it proposes the extension.
Odd-degree cyclicity also excludes archimedean inertia.

The first controls are the four field keys already carrying a completed
full `bnfcertify` certificate and class number three:

- `0723a457...e9927609d`;
- `30c2d6d1...1b4f22`;
- `85f76a36...e972ab`;
- `cf2feada...c49825`.

Every residual key has a 600-second and 2 GiB cap.  A construction or
check failure remains incomplete and never becomes a class-number
claim.
