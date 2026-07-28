# SIC--Stark research cycle 79: exact real/CM unit identity

The CM orientation must still be compared with the real-quadratic
Roblot units \(\eta_0,\eta_1\).  This comparison is now exact.

Embed each real quartic field and the corresponding CM quartic field in
their common degree-sixteen normal closure.  For every real embedding of
\(\eta_b\), the script identifies a complex-conjugate pair
\((\rho,\bar\rho)\) of the CM field and proves one of the identities

\[
\eta_b
 =\rho(u_{b,3}^{\,2})\bar\rho(u_{b,3}^{\,2}),
\qquad\text{or}\qquad
\eta_b^{-1}
 =\rho(u_{b,3}^{\,2})\bar\rho(u_{b,3}^{\,2}).
\]

Complex conjugations are detected algebraically as the involutions whose
fixed fields have a real place; the normal closure itself has signature
\((0,8)\).  Every displayed identity is checked by exact equality in the
degree-sixteen number field.  Thus the real and CM
logarithmic-resolvent orbits agree exactly, not just to high precision.

Reproduction:

```bash
gp -q scripts/dimension_eight_cm_real_unit_bridge.gp
```
