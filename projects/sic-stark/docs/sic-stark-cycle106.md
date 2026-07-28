# SIC--Stark research cycle 106: the full-ray Kashio gate

Date: 2026-07-28

## Loophole tested

Cycle 104 noted that the one-place ray field is nonabelian over
\(\mathbf Q\).  Kashio's hypothesis is naturally phrased using a narrow
ray field, however, so the conjugation-stable two-place ray compositum
must be tested separately.

## Exact computation

For

\[
 K=\mathbf Q(\sqrt{21}),\qquad
 \mathfrak m=(6)\infty_1\infty_2,
\]

PARI gives

\[
 \operatorname{Cl}_{\mathfrak m}(K)\simeq C_6\times C_2.
\]

Its ray class field has degree \(12\) over \(K\), hence degree \(24\)
over \(\mathbf Q\).  It is Galois over \(\mathbf Q\), but its absolute
Galois group is

\[
 \operatorname{SmallGroup}(24,8)
 \simeq C_3\rtimes D_4,
\]

which is nonabelian.  These assertions are certified by

```text
scripts/dimension_six_normal_closure.gp
```

Thus passing from the one-place field to the full narrow ray field does
not activate Kashio's abelian-over-\(\mathbf Q\) partial theorem.

## Result

\[
\boxed{\text{the full two-place ray field is Galois but nonabelian over
\(\mathbf Q\).}}
\]

The distinction matters: stability of the modulus under conjugation
gives normality, not commutativity.  The possible Kashio shortcut is
therefore excluded for the correct full ray field, not merely for the
asymmetric one-place subfield.

