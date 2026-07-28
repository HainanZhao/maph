# SIC--Stark research cycle 51: exact ray fields for all six strata

## Result

PARI class-field computation gives the exact ambient one-place ray fields
for every conductor-lowered stratum.

| modulus HNF | ray group | absolute class-field polynomial degree |
|---|---:|---:|
| \(\begin{psmallmatrix}14&0\\0&14\end{psmallmatrix}\) | \(C_6\times C_2\) | 24 |
| \(\begin{psmallmatrix}7&0\\0&7\end{psmallmatrix}\) | \(C_6\) | 12 |
| \(\begin{psmallmatrix}14&6\\0&2\end{psmallmatrix}\) | \(C_2\) | 4 |
| \(\begin{psmallmatrix}14&8\\0&2\end{psmallmatrix}\) | \(C_2\) | 4 |
| \(\begin{psmallmatrix}7&3\\0&1\end{psmallmatrix}\) | \(C_2\) | 4 |
| \(\begin{psmallmatrix}7&4\\0&1\end{psmallmatrix}\) | trivial | 2 |

The two nontrivial quartic fields are

\[
x^4+2x^2-7,\qquad x^4-2x^2-7.
\]

The computation includes `bnfcertify(K)=1`.  Complete polynomials and
software version information are emitted by
`scripts/dimension_seven_ray_fields.gp`.

## Consequence

There is no unknown ambient field left in dimension seven.  Exact overlap
coordinates may be sought in two quartic fields and the two scalar ray
fields of degrees \(12\) and \(24\) over \(\mathbb Q\).

