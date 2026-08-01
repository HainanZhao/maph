# Engine-A / AFK interface scope audit — corrected flat-monoid identification

**Status:** `TERMINAL_SCOPE_MISMATCH_RECONFIRMED`
**Date:** 2026-08-01 UTC
**Claim boundary:** This corrects v2's overbroad source identification. It
does not prove an order-monoid Engine-A analogue, a support predicate, a
scan result, or a TCC result.

## Corrected result

**PROVED (checked primary definitions):** AFK's flat imprimitive ray class
monoid is the **non-coprime flat/invertible** ray class monoid: its elements
are invertible fractional \(\mathcal O\)-ideals satisfying semilocal
integrality at \(\mathfrak m\), modulo the imprimitive congruence relation.
It is not a ray class group because its elements need not be coprime to
\(\mathfrak m\).

This is exactly the construction Kopp calls the flat imprimitive ray class
monoid in arXiv:2411.06763, Section 3.2. It corresponds to the
non-coprime invertible construction \(\operatorname{Clm}^{*}_{\mathfrak
m,\Sigma}(\mathcal O)\) in Kopp--Lagarias Appendix A, not to the
coprime potentially-invertible Clifford monoid of Proposition A.4.

Kopp--Lagarias states immediately after (A.29) that its non-coprime
invertible monoid is not generally Clifford, and Example A.9 exhibits the
obstruction at a squared principal prime modulus. Thus the proposed repair
by a disjoint union of finite abelian groups is unavailable for AFK's
actual monoid. The v1 terminal interface conclusion remains valid.

## Checked source correspondence

| AFK / Kopp cocycle source | Kopp--Lagarias Appendix A | Consequence |
|---|---|---|
| Kopp arXiv:2411.06763, `sec:monoid`, equations (3.2)--(3.4): \(J^{\flat}_{\mathfrak m}(\mathcal O)=\{\mathfrak a\in J^*(\mathcal O):\mathfrak a\mathcal O[S_{\mathfrak m}^{-1}]\subseteq\mathcal O[S_{\mathfrak m}^{-1}]\}\), and \(\operatorname{Clt}=J^{\flat}_{\mathfrak m}/\sim\). | Definition A.7 gives the same semilocal-integrality condition for invertible ideals; Definition A.8 / (A.28) names the quotient \(\operatorname{Clm}^{*}_{\mathfrak m,\Sigma}(\mathcal O)\). | This is the exact AFK construction. |
| AFK arXiv:2501.03970v2, `defn:rayclassmonoid`, repeats the same defining set and equivalence relation and calls it the flat imprimitive monoid. | Kopp--Lagarias, after (A.29): \(\operatorname{Clm}^{*}_{\mathfrak m,\Sigma}(\mathcal O)\) is not generally a Clifford monoid. | AFK cannot be replaced uniformly by maximal subgroups/groups. |
| — | Proposition A.4 / (A.10) proves a Clifford decomposition only for the **coprime potentially-invertible** monoid. | This attractive decomposition is a different object and does not supply Engine A. |
| AFK `conj:msc` says Monoid Stark is not known to follow completely from Stark/Stark--Tate outside the maximal order. | — | Even a finite monoid spectral construction would still need a proved regulator/unit closure before it could substitute for Engine A. |

Primary-source pins: AFK source SHA-256
`bc742b19594b5842d1edc343d9b48616273e8225c76910f7d758722cf6761519`;
Kopp cocycle source SHA-256
`87d273e270259af93ea27189001bebc4d540f5d28f0f173a799b1257faaac746`;
Kopp--Lagarias December-2022 PDF SHA-256
`3fdf11b0a581a6499c653e45c4e5f6c5665f84b942c8d341e29313756537e1d0`.

## Consequence

**PROVED:** The full-family chain cannot be reopened by either of these
shortcuts:

```text
AFK flat monoid -> maximal-order ray group
AFK flat monoid -> Kopp--Lagarias Proposition A.4 group components.
```

The first lacks a proved label/zeta reduction; the second begins with the
wrong monoid. Any successor still needs a spectral theory for the actual
non-coprime flat monoid, a label-preserving differenced-zeta formula and
quadratic-support predicate, and a compatible proved Stark/Tate closure.
