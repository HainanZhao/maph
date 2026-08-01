# Cycle 134 — Engine-B integral-basis correction

## Correction

The B5-086 direct-source geometry screen (Cycle 120) and the B5-021 /
B5-033 screen (Cycle 121) used defining polynomials `y^2-d` for
\(d=33,57,77\).  Each of these fields has \(d\equiv1\pmod4\), so
the frozen census HNFs are expressed in the integral basis of
\(y^2-y+(1-d)/4\), not the nonintegral basis of `y^2-d`.

Applying the frozen integral-basis HNFs to the nonintegral model
produced false modulus-divisibility and coprimality failures. The
original artifacts remain preserved as historical failed screens:

- `artifacts/b5086-transport-geometry-v1.json`;
- `artifacts/final-direct-source-coprime-screen-v1.json`.

The corrected global screen reconstructs each base field at its frozen
discriminant before testing ideal multiplication. It finds seven
geometrically eligible directions from RQ-001107 in B5-086, one from
RQ-002057 in B5-021, and two from RQ-002955 in B5-033. This is
**OBSERVED exact geometry only**. No packet transport is promoted here:
each needs a successor label-aware Euler-deletion and orientation proof.

## Affected claims

The statements that B5-086 has seven source-prime obstructions and
that B5-021/B5-033 have no integral direct quotients are withdrawn.
They must not appear in the local census correction candidate or any
future Zenodo version. The existing twelve packet transports are
unaffected.

## Falsification and replay

The correction would fail if the reconstructed field discriminant did
not equal the frozen W1 discriminant, if
\(\mathfrak m_s\mathfrak q\ne\mathfrak m_t\), or if the target sign
class did not map to the source sign class. All three conditions are
recorded per direction by
`discovery/screen_engine_b_global_coprime_geometry.py`; its full
sealed audit is the required successor evidence.
