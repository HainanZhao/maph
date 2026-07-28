# SIC--Stark research cycle 109: the projective CM near miss

Date: 2026-07-28

## Unexpected finding

The full degree-\(24\) ray field is not CM, but the unique faithful
degree-\(12\) projective quotient is:

\[
 \operatorname{Gal}(M/\mathbf Q)\simeq D_{12},\qquad
 \operatorname{sig}(M)=(0,6).
\]

Among its seven degree-\(6\) subfields, exactly one is totally real; the
other six have signature \((0,3)\).  Hence \(M\) has a unique totally
real half-field \(E\) and \(M/E\) is a quadratic CM extension.

This is certified by

```text
scripts/dimension_six_projective_cm_gate.gp
```

## Why it does not orient the target

Let \(N\) be the degree-\(24\) linear ray closure and

\[
 Z=\operatorname{Gal}(N/M)\simeq C_2
\]

the scalar kernel of the projectivization.  Every character constructed
from \(M/E\), inflated to \(N\), is trivial on \(Z\).

The original two-dimensional weight-one representation is not: the
nontrivial element of \(Z\) acts as the scalar \(-I\).  Therefore the two
packets lie in opposite central eigenspaces:

\[
 \rho_{\mathrm{target}}|_Z=-1,\qquad
 \rho_{\mathrm{projective\ CM}}|_Z=+1.
\]

Their character inner product is zero, so the target cannot occur as a
constituent of an Artin induction from the quadratic CM step \(M/E\).

## Result

\[
\boxed{\text{a CM projective quotient exists, but it forgets the
linear scalar orientation.}}
\]

Modern CM Brumer--Stark results may evaluate the projective norm packet;
they cannot supply the missing \(\mathbf Q(\sqrt{-3})\)-oriented linear
value.  This is the same central distinction detected computationally
by the absence of a lower scalar twist, now expressed at the field level.

