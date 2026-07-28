# SIC--Stark research cycle 107: maximal absolute-abelian quotient

Date: 2026-07-28

## Question

Even though the full ray field is nonabelian over \(\mathbf Q\), could a
large absolute-abelian subfield still retain the faithful order-six
orientation?

## Exact abelianization

Starting from the certified permutation group of the degree-\(24\) full
ray field, the script

```text
scripts/dimension_six_absolute_abelian_gate.gp
```

computes all commutators and closes them under multiplication.  The
derived subgroup has order \(6\), so

\[
 G^{\mathrm{ab}}\simeq C_2\times C_2.
\]

The maximal subfield abelian over \(\mathbf Q\) consequently has degree
four.  Using the already certified three quadratic subfields, it is

\[
 \mathbf Q(\sqrt{21},\sqrt{-3})
 =
 \mathbf Q(\sqrt{21},\sqrt{-7}).
\]

## Consequence

The commutator contains the cubic rotation.  Passing to the absolute
abelianization kills exactly the faithful cubic component of
\(\chi_1\), leaving only the three quadratic characters.

\[
\boxed{\text{the maximal absolute-abelian subfield contains no
faithful order-six orientation.}}
\]

Thus an absolute-abelian special-value theorem cannot be combined with
subfield descent to recover the missing value.  It reaches only the
quadratic data already present in the project.

