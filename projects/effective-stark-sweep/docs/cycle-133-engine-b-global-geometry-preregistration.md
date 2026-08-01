# Cycle 133 — global Engine-B coprime-deletion geometry screen

Recorded: 2026-08-01 UTC, before evaluating a new directed
source-to-target pair.

## Objective and claim boundary

Classify the *geometric reach* of the direct coprime Euler-deletion
transport method on every ordered pair of distinct members within the
88 frozen Engine-B normal-closure groups.  For a pair
\((\mathfrak m_s,\mathfrak m_t)\), the screen asks whether
\(\mathfrak m_t=\mathfrak m_s\mathfrak q\) with integral,
finite, source-coprime quotient \(\mathfrak q\), and whether the
exact ray-class map preserves the identity and the distinguished sign
class.  It records the map matrix and generator image; it does not
assume an identity matrix.

The resulting categories are deliberately narrow:

1. `GEOMETRICALLY_ELIGIBLE`: this direction passes the modulus,
   coprimality, and ray-map gates.  It is not a packet theorem without
   an independently certified source, Euler formula, and orientation
   proof.
2. `GEOMETRICALLY_OBSTRUCTED`: no ordered member pair in the closure
   passes those gates.  This proves only the direct coprime-deletion
   route unavailable within that closure, not a general no-go result.
3. `SOURCE_OR_PROOF_OPEN`: a geometrically eligible direction exists
   but no existing sealed source-and-orientation proof is being
   promoted in this cycle.

No L-values, packet polynomials, numerical recognition, or new source
certificates are computed.  Existing twelve promoted transports remain
unchanged and serve only as regression controls.

## Frozen inputs and gates

- `artifacts/engine-b-transport-ledger-v4.json`: exactly 232 members,
  88 closures, 12 already promoted and 220 open.
- `artifacts/w1-full-census-v1.json`: base discriminants, finite ideal
  HNFs, one-place ray invariants, and sign generators.
- One deterministic PARI/GP 2.15.4 process per direction, with a
  120-second cap and 2 GiB PARI stack cap.
- Gate 1: reconstructed real-quadratic field has the frozen
  discriminant.
- Gate 2: \(\mathfrak m_s\mathfrak q=\mathfrak m_t\) exactly.
- Gate 3: \(N(\mathfrak m_s+\mathfrak q)=1\).
- Gate 4: `bnrmap` exists and maps identity to identity and the target
  distinguished sign class to the source one; the source/target ray
  groups and all map data are retained.

A tool failure is retained as `TOOL_FAILURE`, and prevents a
closure-level `GEOMETRICALLY_OBSTRUCTED` conclusion.  The full screen
stops after one pass; a later source proof may promote an eligible
direction only in a successor artifact.
