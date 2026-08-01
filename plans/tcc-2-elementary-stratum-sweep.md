# The 2-elementary TCC stratum sweep

## Status and claim boundary

**Status:** `READY_FOR_PHASE_0`; no eligibility scan, bridge computation,
or new TCC claim has been run from this plan.

**Objective.** For every scanned admissible Appleby--Flammia--Kopp (AFK)
tuple whose relevant one-place ray packet has purely quadratic support,
mechanically prove the formal TCC by combining the unconditional
quadratic-support identification with exact packet synthesis and a
finite bridge-and-minor certificate. The two acceptable terminal outcomes
are:

1. new, individually certified TCC dimensions/strata above dimension 8;
   or
2. an exact, bounded boundary statement saying that no full quadratic-
   support tuple was found in the preregistered scan universe.

This plan does **not** claim a TCC result for an unscanned tuple, a result
for partial/higher-order support, a general AFK modulus formula, or an
asymptotic statement. An eligibility verdict is not a TCC proof.

## Why this is now feasible

The Effective-Stark census has already banked the shared quadratic packet
component:

- `PROVED` compositum-free trace descent for the denominator-cleared
  sign-orbit polynomial, including the required denominator-lift gate;
- `PROVED` exact packet polynomials for all 1,560 rows in its frozen
  quadratic stratum; and
- `OBSERVED` end-to-end corpus runtime of 43.46 seconds for those rows,
  with a maximum exact coefficient-coordinate height of 62 digits.

See `projects/effective-stark-sweep/PLAN.md`, cycles 085--087, and
`artifacts/census-q-packet-corpus-audit-v1.json` in that project. The
recurrence avoids a degree-\(2^N\) compositum by using only
\(u+u^{-1}\in K\) and successive resultants over the quadratic base.

This removes the former compositum-degree blocker, but it does **not**
establish a universal one-millisecond cost. The AFK adapter must benchmark
its own full-row cost and preregister a height/resource cap before Phase 2.
The already-banked synthesis is a shared dependency, so Phase 2 does not
wait for a future census-C2 milestone; it does wait for the Phase-0
convention lock and a positive Phase-1 gate.

## Dependencies and interfaces

```text
AFK source/convention audit (Phase 0)
        -> exact eligibility scan (Phase 1)
             -> no full-support hits: bounded boundary statement, close
             -> full-support hits
                    -> exact bridge generator (Phase 2)
                         -> minor certificates and companion note (Phase 3)
```

Shared, already available components:

- the Effective-Stark conventions discipline and trace-descent packet
  synthesis, adapted rather than copied into a second implementation;
- the dimension-4/5 bridge pattern in
  `projects/sic-stark/paper/sic-stark-dimensions-four-five.tex`;
- the existing exact bridge/minor scripts under `projects/sic-stark/scripts/`.

This program does not consume Engines B/C, Arb recognition, or a
higher-order/cyclic-support mechanism. A nonempty quadratic *slice* in an
otherwise higher-order packet is recorded for a separate peeling program;
it is not a Phase-2 hit.

## Phase 0 — convention and universe lock

**State:** `READY`; **estimated scope:** one research cycle.

Before any scan, read AFK §1 and the dimension-4/5 paper's corresponding
convention sections, then create a versioned convention record containing:

1. the exact finite and infinite modulus for each admissible tuple and
   the pinned real-place/embedding labels;
2. the relation between \((d,r)\), \((K,j,m)\), and a form \(Q\), including
   the fact that form conductor data can vary while the proposed group
   test is tuple-level;
3. the exact ray-class representative used for the sign class \(R\),
   and a derivation—not an analogy—from the dimension-4 demonstration;
4. the precise equivalence between the selected ray-group predicate and
   complete quadratic support.

The known calibration instances are \((4)\infty_2\) over
\(\mathbb Q(\sqrt5)\) and \((5)\infty_2\) over
\(\mathbb Q(\sqrt3)\), as recorded in the dimension-4/5 manuscript.
They are controls, not proof of the general modulus rule.

**Gate G0.** If the general modulus is not exactly the proposed
\((d)\mathcal O_K\) with the specified one-place signature, revise and
version the scan design before computing. No rows may be silently carried
across a changed convention.

## Phase 1 — exact eligibility scan

**State:** `BLOCKED` on G0; **decision-relevant cost:** expected days,
pending a preregistered pilot benchmark.

### Proposed preregistration

- Scan every admissible tuple with \(d\le 1024\), every arising
  fundamental-discriminant field, and both AFK \(j\)-branches.
- Record every tuple, including rejected/skipped tuples and the exact
  reason.
- Freeze the tuple enumeration, PARI version, modulus rule, resource cap,
  hash-chain schema, and failure-row policy before the first result is
  opened.

### Per-tuple exact record

1. construct the locked one-place ray group and record its invariant
   factors;
2. compute the locked sign class \(R\);
3. apply the Phase-0-derived full-support predicate (expected to involve
   the exponent of the relevant quotient and the square-class of \(R\),
   but not assumed until G0);
4. separately count quadratic characters odd on \(R\) to form a
   partial-support slice ledger; and
5. emit a hash-chained JSON row with elapsed time and peak memory.

### Gate G1

- **No full-support hit above \(d=8\):** close Phases 2--3 and write the
  resulting finite boundary statement for the census frontier discussion
  and the dimension-4/5 outlook. It remains a statement only about the
  frozen scan range.
- **One or more full-support hits:** preserve and report the hit list,
  then authorize Phase 2 for those exact tuples only.

## Phase 2 — bridge automation

**State:** `BLOCKED` on G1-positive and an AFK adapter benchmark.

For each hit, generate independently checkable finite certificates for:

1. **Characteristic-to-ray map.** Positive lifts and ray-class discrete
   logs of \((q\beta-\widetilde p)\), normalized by the frozen generator.
2. **Multiplier ledger.** The Kopp theta-character exponent, squared AFK
   phase, and Rademacher invariant for every nonzero characteristic. A
   mismatch contains that tuple and triggers a convention audit; it is
   never repaired by relabeling output.
3. **Packet construction and labels.** Reuse trace descent over \(K\),
   perform the required square-root/denominator lift, isolate roots, and
   assign Frobenius/Artin labels at a frozen split prime.
4. **Signed reconstruction table.** Derive signs from the ray logs and
   parity exponents; do not store them as expected answers.
5. **Engine-A closure.** Record the theorem and hypotheses establishing
   the quadratic-support identification. No Shintani height argument or
   Arb recognition is substituted for this step.

Pre-register a certificate schema, per-tuple time/memory/height caps, and
the rule for a resource-cap failure. The generator must first reproduce
the published dimension-4 and dimension-5 tables exactly, with all labels,
before it is applied to a new dimension.

## Phase 3 — exact minor certificates and note

**State:** `BLOCKED` on Phase 2 certificates.

For each Phase-2 tuple:

1. build the reconstruction matrix over the declared cyclotomic/subfield
   presentation and reduce every rank-two minor exactly modulo the chosen
   packet factor;
2. verify factor selection non-circularly by recording the nonzero-minor
   counts for rejected factors;
3. derive trace-one/rank-one idempotency, the coefficient bridge,
   endpoint correction, twist congruence, conjugation for the
   \(\lambda=0\) shift, and integral-form transport; and
4. produce a replayable theorem row plus a compact companion note with a
   claim-boundary section first.

Before circulation, archive the proof scripts, certificate outputs,
environment pins, and deterministic manifest under an immutable DOI.

## Failure handling and research hygiene

- A convention mismatch, multiplier mismatch, failed minor, or failure to
  reproduce a published calibration is recorded with its transcript and
  affects only the implicated tuple/claim while safe independent work
  continues.
- A resource cap cannot be bypassed with an unregistered method change.
  Amend the preregistration first, retain the failed result, and rerun.
- A surprising hit receives heightened checks: independent derivation of
  the characteristic map and labels, plus replay from a clean extracted
  archive.
- The scan's output is a finite census. It must never be rewritten as an
  asymptotic claim or as evidence for partial-support TCC instances.

## Initial next action

Create the Phase-0 convention dossier with primary-source page/theorem
references and calibration replays for dimensions 4 and 5. Only after its
review may the \(d\le1024\) universe, group predicate, and resource caps
be frozen.
