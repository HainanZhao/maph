# Cycles 074--076 — B2 exact Artin-transport preregistration

Recorded: 2026-07-31 UTC, before running the five-case transport.

## Claim boundary

The objective is to determine, without reading any \(L'\)-derived
phase target, whether the order-four automorphism \(\gamma\) used by
each Roblot constructor is the positive or inverse Artin generator
selected by the exact analytic-character pipeline.

A successful transport fixes only the direct/inverse character
orientation. It does not prove a new Stark identity, does not select a
quarter-turn representative inside the signed-unit orbit, and does
not authorize B1 circulation or B3 target opening.

## Frozen cases and exact separators

The primary routes and exact separator rational primes are:

| case | primary route | separator |
|---|---|---:|
| RQ-000129 | \(\mathbf Q(\sqrt{-2})\) | 3 |
| RQ-001280 | \(\mathbf Q(\sqrt{-10})\) | 5 |
| RQ-001569 | \(\mathbf Q(\sqrt{-7})\) | 11 |
| RQ-001894 | \(\mathbf Q(\sqrt{-15})\) | 2 |
| RQ-007519 | \(\mathbf Q(\sqrt{-6})\) | 5 |

The four non-quarantined secondary routes are frozen as redundancy
checks. The RQ-000129 \(\mathbf Q(\sqrt{-3})\) route remains a
quarantined cross-check and cannot support promotion.

## Permitted inputs

- the exact packet-field polynomials and the deterministic
  first-order-four automorphisms in the sealed Roblot constructors;
- exact source ray-character coordinates and conductors from the
  Engine-C selection inputs and certificates;
- exact separator-prime Frobenius and normal-closure records;
- the DOI-bearing convention
  \(L(s,\chi)=\sum_A\chi(A)\zeta(s,A)\),
  \(\chi(\gamma)=i\), with positive Artin powers;
- PARI exact finite-field, ray-class, and Galois arithmetic.

The following are prohibited until the transport artifact is sealed:

- `artifacts/all-five-phase-gates-v1.json`;
- every `lprime_zero_ball`, phase, orientation, rotation, or residual;
- Roblot logarithmic coefficients and dominant-gauge labels;
- the direct/inverse strings selected by the old comparison script.

## Exact gates

For each case:

1. reconstruct the separator Frobenius on the packet field by the
   exact congruence \(\alpha\mapsto\alpha^p\) at a usable prime;
2. compare it algebraically with the constructor's frozen
   \(\gamma\), allowing only exponents \(1\) and \(3\);
3. evaluate the frozen source ray character on the corresponding
   prime ideal and reconcile PARI's `lfunan` coefficient convention
   with the published Artin convention;
4. require every non-quarantined secondary route to give the same
   orientation;
5. emit only the exact transport exponent and source provenance.

## Outcomes

- `PASS_EXACT_TRANSPORT`: all five primary routes close and every
  applicable secondary route agrees.
- `CONTAINED_ROUTE_DISAGREEMENT`: an exact route label disagrees;
  stop B2 immediately.
- `BLOCKED_MISSING_ARTIN_LINK`: exact Frobenius-to-ray-character
  identification cannot be reconstructed from the frozen data.
- `FAILED_CONVENTION_AUDIT`: the published transform, PARI character
  convention, and bridge implementation cannot be reconciled exactly.

No numerical target may be opened to repair a failed or ambiguous
row. The failed row and its full exact diagnostics must be preserved.
