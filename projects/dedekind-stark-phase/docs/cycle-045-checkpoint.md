# Cycle 045 checkpoint

Recorded: 2026-07-31 UTC

## Outcome first

Cycles 026--045 completed the independent calibration experiment. All
five Roblot weak-solution controls pass phase quantization: after the
character orientation is fixed, each independently constructed
coefficient differs from the certified \(L'\)-ball by a unique fourth
root of unity.

This is a strong positive result about the phase phenomenon, but it does
not yet yield a Dedekind-sum formula. Two exact structural audits prevent
overclaiming:

- the raw quarter-turn label changes under the permitted
  \(\mathbf Z[i]^\times\)-orbit of the weak solution;
- after fixing a canonical dominant-embedding gauge, the simplest
  field-only Dedekind--Rademacher family fails exactly: RQ-000129 and
  RQ-001569 have the same feature vector modulo \(4\) and different
  labels.

The missing information is ray/modulus-specific cocycle data. Existing
code extracts it only for special SIC tuples, not from a general
\((K,\mathfrak m,\chi)\). The empirical fitting track therefore stops,
and the project pivots to the theorem-level ray-class/cocycle bridge.

## Phase-gate results

| case | analytic orientation | constructor rotation | raw quarter turn |
|---|---:|---:|---:|
| RQ-000129 | inverse | 1 | 3 |
| RQ-001280 | inverse | 0 | 0 |
| RQ-001569 | direct | 1 | 3 |
| RQ-001894 | direct | 1 | 3 |
| RQ-007519 | inverse | 0 | 0 |

The \(L'\)-side uses certified rectangular balls. The independently
constructed coefficient is presently a high-precision numerical
embedding of exact unit-lattice data, so the combined claim remains
`NUMERICAL_PHASE_MATCH_WITH_CERTIFIED_LPRIME_BALLS`.

## Canonical gauge

For a cyclic quartic weak solution, write its logarithmic orbit as
\((a,b,-a,-b)\). When \(|a|\ne|b|\), the unique orbit member maximizing
the logarithm at the distinguished embedding defines the
dominant-embedding gauge. All five controls are nondegenerate.

The canonical quarter turns are:

| case | dominant orbit index | canonical quarter turn |
|---|---:|---:|
| RQ-000129 | 1 | 0 |
| RQ-001280 | 1 | 1 |
| RQ-001569 | 2 | 1 |
| RQ-001894 | 0 | 3 |
| RQ-007519 | 3 | 3 |

## Exact feature verdict

The pre-registered third feature \(12s(a,|c|)\) is nonintegral for two
of five rows, so the frozen family is rejected before fitting.

The natural integral repair
\[
q_{\rm dom}=\beta_0+\beta_1\Phi(A_K)
 +\beta_2\,12|c|s(a,|c|)\pmod4
\]
also fails without fitting: RQ-000129 and RQ-001569 both have feature
vector \((1,3,0)\) modulo \(4\), while their canonical labels are \(0\)
and \(1\). Thus field-only fundamental-unit data cannot determine the
phase.

## Cycle ledger

| cycle | result |
|---:|---|
| 026 | froze the remaining-constructor and feature protocol |
| 027 | reconstructed the \(\mathbf Q(\sqrt{35})\) unit data |
| 028 | sealed the RQ-001280 independent constructor |
| 029 | computed the RQ-001569 relative class/Fitting data |
| 030 | sealed the RQ-001569 constructor |
| 031 | computed the RQ-007519 relative class/Fitting data |
| 032 | sealed the RQ-007519 constructor |
| 033 | computed the RQ-001894 relative class and norm index |
| 034 | sealed the RQ-001894 constructor |
| 035 | demonstrated deterministic byte replay of all constructors |
| 036 | opened the four remaining certified phase balls |
| 037 | resolved direct versus inverse character orientation |
| 038 | banked the five-for-five phase-quantization result |
| 039 | proved the weak-solution gauge-ambiguity lemma |
| 040 | replayed the ambiguity on all five controls |
| 041 | computed exact fundamental-unit \(SL_2(\mathbf Z)\) matrices |
| 042 | computed exact Rademacher and Dedekind features |
| 043 | rejected the frozen feature family before fitting |
| 044 | fixed the dominant gauge and proved the field-only no-go |
| 045 | audited available cocycle machinery and declared the theory pivot |

## Next authorized work

Draft a separate plan for a ray-class cocycle phase theorem. Its first
gate is a convention-preserving construction of form/geodesic data from
an oriented quartic ray character, replayed on the existing SIC anchors.
No coefficient fitting or large holdout run precedes that gate.
