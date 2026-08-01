# Engine-A / AFK interface scope audit

**Status:** `TERMINAL_SCOPE_MISMATCH_CONTAINED`
**Date:** 2026-08-01 UTC
**Claim boundary:** this is a primary-source and theorem-hypothesis
audit.  It does not assert that no order-ray analogue exists; it proves
only that the component chain specified in the sweep plan does not
presently supply one for every admissible AFK form.

## Result

**PROVED (checked source and theorem hypotheses):** the advertised
chain
\[
 \text{AFK tuple}\ \longrightarrow\ \text{Engine-A quadratic packet}
 \longrightarrow\ \text{TCC bridge}
\]
has a proved interface only at the maximal order \(\mathcal O_K\).
AFK permits admissible forms of every conductor \(f\mid f_j\), and
for \(f>1\) it indexes squared overlaps by the flat imprimitive
order-ray *monoid*
\(\operatorname{Clt}_{d\infty_2}(\mathcal O_f)\).  Engine A instead
assumes a finite abelian *group*
\(G=\operatorname{Cl}_{\mathfrak m}(K)\), then applies Fourier
inversion to its Hecke characters.  No checked theorem identifies these
objects, their differenced zeta functions, or their support predicates
for nonmaximal \(\mathcal O_f\).

Consequently the original objective's phrase “every admissible AFK tuple
whose one-place ray packet has purely quadratic support” has no locked
Engine-A predicate for the allowed \(f>1\) strata.  This is a
specification/theorem gap, not a performance issue.  A finite scan under
the original gates cannot establish the requested full-family theorem or
its proposed bounded-negative alternative.

## Checked interfaces

The source record is Appleby--Flammia--Kopp, arXiv:2501.03970v2
(2025-03-17), source SHA-256
`bc742b19594b5842d1edc343d9b48616273e8225c76910f7d758722cf6761519`.
The internal labels below are stable in that source release.

The independent monoid source is G. S. Kopp, *The
Shintani--Faddeev modular cocycle: Stark units from q-Pochhammer ratios*,
arXiv:2411.06763 source archive SHA-256
`87d273e270259af93ea27189001bebc4d540f5d28f0f173a799b1257faaac746`.

| Source | Checked statement | Consequence |
|---|---|---|
| AFK Definitions `defn:rayclassgroup`, `defn:rayclassmonoid` (source pp./lines 1547--1600) | A ray class group uses ideals coprime to the modulus; the flat imprimitive ray-class monoid weakens that condition and is a finite commutative monoid. | A group-character Fourier transform is not supplied merely by naming a monoid. |
| AFK theorem `thm:nupnumpeq1`, equation `eq:nusquared` (lines 4781--4800) | For an admissible tuple and nonzero characteristic, the selected object is a unique \(\mathcal A\in\operatorname{Clt}_{d\infty_2}(\mathcal O_f)\). | The object changes with the form conductor. |
| AFK Definitions `dfn:sequenceofconductors`, `dfn:admissibleform` | The allowed form conductors satisfy \(f\mid f_j\); AFK gives an admissible conductor-8 example at \(d=19\). | The nonmaximal strata are inside the stated universe, not a removable edge case. |
| AFK discussion after `defn:rayclasspartialzeta` (lines 1669--1672) and after `thm:RayClassField2plus` (lines 5630--5635) | The maximal-order monoid/ray relation is special; AFK says the nonmaximal order theory is insufficient for the displayed analogue of the classical theorem. | No source-backed reduction to maximal-order Engine A was found. |
| Kopp `thm:correspondence`, example `eg:notraygroupimage`, and the non-isomorphism example after `prop:exmonoid` | The monoid correspondence is injective only under a multiplier-order condition; the paper gives RM points not in any ray-group image and shows extension from a nonmaximal order can identify distinct monoid classes. | A uniform label-preserving conversion of all AFK order-monoid classes to a maximal-order ray group is contradicted by the cited theory's examples. |
| `effective-stark-results.tex`, Theorem `thm:A` and Proposition `prop:A` | Engine A sets \(G=\operatorname{Cl}_{\mathfrak m}(K)\), requires quadratic characters in the differenced Fourier support, and proves its formula by character inversion in \(\widehat G\). | Its hypotheses do not name an order \(\mathcal O_f\), a monoid class, or a nonmaximal-order partial zeta function. |

The last comparison is exact hypothesis alignment, rather than an
argument from the absence of code.  It explains why the existing D4/D5
controls are valid at \(f=1\) but cannot validate a generic AFK
adapter.

## What would reopen the full-family objective

Exactly one of the following must be supplied and independently audited
before a new P1 scan can be preregistered:

1. a theorem giving a canonical, label-preserving reduction from each
   relevant \(\operatorname{Clt}_{d\infty_2}(\mathcal O_f)\) to a
   maximal-order ray group and proving equality of the relevant
   differenced partial-zeta packets, including all deleted Euler
   factors; or
2. an order-ray monoid analogue of Engine A: a finite support object,
   a proved quadratic predicate, exact Fourier/reinduction formula,
   and a regulator/unit formula for every allowed \(\mathcal O_f\).

A definition of “purely quadratic support” for the nonmaximal monoid
must be part of either result.  Enumerating forms, calling
`bnrinit` on \(\mathcal O_K\), or observing a local quotient cannot
replace this interface theorem.

## Consequence for the D12 lead

**EXPLORATORY:** D12 has \(f=1\), so the maximal-order part of the
interface is available in principle.  It remains outside the plan's G1
path because it was selected after an unregistered screen, and its bridge
still requires characteristic-dependent conductor lowering (the
fixed-full-ray shortcut audit records 71 noncoprime characteristics).
Kopp Proposition `prop:changemodzeta` gives this particular
maximal-order lowering: the exact D12 ledger has 72 full-modulus rows and
71 reduced rows, at finite modulus norms \(36,16,9,4,1\).  It is
recorded in `discovery/tcc-sweep-d12-conductor-lowering-v1.json`; no phase
or reconstruction conclusion follows from it.
This does not repair the full-family objective and must not be presented
as a sweep result.

**Correction D12-C1:** the numerical counts in the preceding D12
lowering sentence refer to a superseded eigenunit-based representative.
They are invalidated by
`docs/tcc-sweep-d12-correction-v1.md`.  The corrected fixed-point branch
has eleven reduced HNF moduli, not the six scalar moduli stated above;
this changes no conclusion of this interface-scope audit.
