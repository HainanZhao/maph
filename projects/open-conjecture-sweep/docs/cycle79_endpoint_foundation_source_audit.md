# C79 published-source audit: compatible \(Q=I/2\) endpoint

## Result sought

For a three-qubit state \(\rho_{ABC}\) and \(a,b,c\geq0\) with
\(a+b+c=1\), prove majorization of

\[
a\rho_{AB}\otimes I_C+b\rho_{AC}\otimes I_B+cI_A\otimes\rho_{BC}
\]

by its aligned counterpart. This audit does not use Song--Chen Proposition 3
as authority.

## Published ingredient and checked scope

**PROVED source applicability.** Higuchi--Sudbery--Szulc, *One-qubit reduced
states of a pure many-qubit state: polygon inequalities*, Physical Review
Letters 90, 107902 (2003), proves that the smaller eigenvalues
\(r_A,r_B,r_C\in[0,1/2]\) of one-qubit marginals of a pure three-qubit state
obey \(r_A\le r_B+r_C\) and cyclic permutations. These are exactly the
hypotheses invoked in C79's pure-state three-prefix bound.

The qubit spin-flip identity and the two-projection principal-angle lemma are
proved directly in the C79 proof note; the latter removes any dependence on
Alhejji--Knill's two-summand result.

## Direct-endpoint screen

**OBSERVED:** A primary-source search through 2026-08-05 found no
peer-reviewed source stating the full weighted compatible three-prefix
endpoint. Song--Chen arXiv:2603.25410 remains v1-only. This is bounded search
evidence, not an absence or novelty proof. C79 instead establishes the
endpoint from the published polygon theorem and independently replayed
algebra.

## Source boundary

The Higuchi--Sudbery--Szulc theorem applies only after C79's Ky Fan convexity
reduction to a pure global state. It does not independently establish the
mixed-state endpoint, the direct two-prefix lemma, arbitrary \(Q\), other
supports, more parties, or higher local dimension.
