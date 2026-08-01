# Engine-A / AFK interface scope audit — flat-monoid refinement

**Status:** `SUPERSEDED_BY_V3_SOURCE_IDENTIFICATION_CORRECTION`
**Date:** 2026-08-01 UTC
**Claim boundary:** This is a source-theorem refinement of the v1 interface
audit. It neither proves an order-monoid analogue of Engine A nor proves
that one is impossible. In particular, it makes no TCC claim and no
bounded scan claim.

## Result

**Invalidated source identification:** AFK's
\(\operatorname{Clt}_{\mathfrak m,\Sigma}(\mathcal O)\), called the
*flat imprimitive ray class monoid*, was here identified as the
non-coprime potentially-invertible ray class monoid of Kopp--Lagarias.
That is too broad: Kopp's current primary source defines AFK's flat monoid
using \(\mathcal O\)-invertible ideals which are semilocally integral at
\(\mathfrak m\), without coprimality. See the correction in v3.

The conclusion survives with a stronger exact source map, but this v2
document must not be cited for the identification itself.

This refines, but does not invalidate, the v1 conclusion: v1 correctly
withheld a maximal-order group/Fourier input. The stronger precise reason is
now recorded here.

## Exact source map

| Object | Checked source statement | Consequence |
|---|---|---|
| AFK's `Clt` | AFK source `macros.sty` defines `Clt` as \(\overline{\mathrm{Clm}}^\flat\); Definition `defn:rayclassmonoid` defines it from semilocally integral \(\overline J^\flat_{\mathfrak m}\) ideals, allowing ideals not coprime to \(\mathfrak m\). | It is the *non-coprime* construction, even though its ideals are potentially invertible. |
| Kopp--Lagarias' group decomposition | *Class Field Theory for Orders of Number Fields* (2022 version), Appendix A, Definition A.2 and Proposition A.4 / (A.10), defines the coprime potentially-invertible monoid \(\mathrm{Clm}^{\flat}_{\mathfrak m,\Sigma}(\mathcal O)\) and proves it is Clifford. | This is a different monoid: the coprimality condition is essential. |
| The AFK matching construction | Kopp--Lagarias Appendix A, Definitions A.7--A.8 / (A.26)--(A.29), defines semilocally integral ideals and the **non-coprime** potentially-invertible monoid \(\mathrm{Clm}^{\flat}_{\mathfrak m,\Sigma}(\mathcal O)\). Its defining condition and equivalence relation agree with AFK `defn:rayclassmonoid` after notation changes. | AFK is in this larger construction, not (A.10). |
| Failure of the shortcut | Kopp--Lagarias immediately after (A.29) says the non-coprime invertible monoid, and hence the larger potentially-invertible monoid, is not generally Clifford. Example A.9 takes \(\mathfrak m=\pi^2\mathcal O\): the class of \(\pi\mathcal O\) belongs to no maximal subgroup. | A universal decomposition into finite abelian groups, needed for a direct character-Fourier reuse of Engine A, is false at this level of generality. |
| AFK's analytic status | AFK `conj:msc` and the text immediately preceding it state that its Monoid Stark Conjecture is not known to follow completely from Stark/Stark--Tate except at maximal order. | Replacing the monoid by group components would not by itself supply the Tate-backed regulator/unit identity required by Engine A. |

The AFK source is arXiv:2501.03970v2, source SHA-256
`bc742b19594b5842d1edc343d9b48616273e8225c76910f7d758722cf6761519`.
The inspected Kopp--Lagarias primary preprint is arXiv:2212.09177,
December-2022 PDF, SHA-256
`3fdf11b0a581a6499c653e45c4e5f6c5665f84b942c8d341e29313756537e1d0`,
Appendix A pp. 42--44. The v1 audit's Kopp cocycle source hash remains
unchanged.

## Consequence for the sweep

**PROVED:** The following candidate repair is invalid as a general theorem:

```text
AFK flat monoid -> Proposition A.4 Clifford group components
                -> apply Engine A componentwise.
```

The first arrow has the wrong source monoid. A viable successor must instead
prove all of the following, for AFK's non-coprime flat monoid itself:

1. a finite spectral/reinduction theory that handles its nonregular classes;
2. a label-preserving formula for the differenced partial zeta packet,
   including the deleted Euler factors at conductor primes;
3. a definition and an exact test for complete quadratic support in that
   spectral object; and
4. a Tate- or other proved regulator/unit closure compatible with the
   resulting labels.

Until then, P1--P3 remain blocked. The conductor-one D12 experiment is
unchanged: it exercises a maximal-order group case only and cannot validate
this non-coprime order-monoid interface.
