# SIC--Stark research cycle 108: totally imaginary is not CM

Date: 2026-07-28

## Loophole tested

The full two-place ray field is totally imaginary and abelian over
\(K=\mathbf Q(\sqrt{21})\).  Could one inflate the mixed character to
this field and apply the modern Brumer--Stark theorem for CM extensions?

## Exact CM test

A degree-\(24\) CM field must contain a totally real subfield of degree
\(12\), fixed by its global complex-conjugation involution.

The script

```text
scripts/dimension_six_full_ray_cm_gate.gp
```

enumerates all degree-\(12\) subfields of the full ray field.  There are
nine:

- seven have signature \((0,6)\);
- two have signature \((6,3)\);
- none has signature \((12,0)\).

Therefore

\[
\boxed{\text{the full ray field is totally imaginary but not CM.}}
\]

The two real places of \(K\) have different complex-conjugation elements
in the ray group.  There is no single involution whose fixed field is
totally real.

## Consequence

Inflating the one-place character to the conjugation-stable full ray
field does not place it within the hypotheses of the CM
Brumer--Stark theorem.  This closes a stronger loophole than the
signature check on the original one-place field: neither the field nor
its natural Galois completion is CM.

