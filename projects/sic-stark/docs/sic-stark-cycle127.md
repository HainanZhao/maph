# SIC--Stark research cycle 127: exact AFK/Ishibashi phase repair

Date: 2026-07-28

This cycle produced a genuine phase breakthrough.

Let

\[
 Q(a,b)=a^2-5ab+b^2,\qquad h=b-4a-1,
\]

and write the canonical AFK phase as a \(48\)-th root of unity. Exact
reduction gives

\[
\boxed{
 \frac{\Phi_{\mathrm{AFK}}(a,b)}{\gamma_{24}(h)}
 =
 \zeta_{48}^{c_b}
 \zeta_{12}^{a^2+\kappa_ba},
 \qquad
 \kappa_b=b+4+6(b\bmod2)\pmod {12}.
}
\]

Thus the AFK phase supplies precisely the nondegenerate quadratic term
missing from the restricted level-24 inversion Gaussian. This is an
identity of roots of unity in all \(36\) cases, not a numerical fit.

The exact certificate is
`scripts/dimension_six_inversion_phase.py`.
