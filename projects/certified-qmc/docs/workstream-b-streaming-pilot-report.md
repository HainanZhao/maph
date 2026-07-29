# Workstream B streaming pilot report

Date: 2026-07-29

## Outcome

The corrected prime-major incremental pilot passes every prospectively
frozen predicate and authorizes the **full exact fidelity-grid
throughput branch**.

On four visible AMD EPYC 9354P cores, the median of five measured runs
was 2.482743143245874 aggregate wall ns per modular update.  Applying
that number to the confirmed incremental count of
54,901,459,582,976 updates projects 1.5776183140488904 node-days,
against the frozen maximum of seven.  Median replay overhead was
0.03700124187661215, against the frozen maximum of 0.15.

This is a local `NUMERICAL` runtime projection, not a portable
performance guarantee.  The authorization itself is the mechanical
result of the frozen predicate.

## Correctness and replay

The native plain-remainder `__int128` implementation evaluated 151 work
primes and two universal overflow primes at every prefix dimension
through 256.  Its prime-major state was 8,192 bytes per prime.

All 25 selected checks—five dimensions across the first, middle, and
last work primes plus both overflow primes—equal the independent Python
modular oracle.  Each of the five checkpoints reloaded with the same
digest, and all 39,168 output words were present.  These facts are
`VERIFIED`.

## Failed first transcript

The first run is retained rather than overwritten.  It passed throughput
and replay but failed every selected residue check because the native
constant product used \(F_j(0)\) instead of \(C_j\).  Its gate result was
`REDESIGN_REQUIRED`.

Its top-level combined residue/replay claim tag was emitted as
`VERIFIED` unconditionally and is invalid for that failed artifact; the
detailed `all_selected_residues_match=false` and
`REDESIGN_REQUIRED` fields are authoritative.  The generator now emits
`FAILED_ORACLE_OR_REPLAY_CHECK` on that branch.  The original transcript
is left byte-for-byte intact so this erratum cannot hide the defect.

The v2 preregistration froze the single correction
\(C_j=6j^2N^2\) while retaining the original 7-node-day, 15%-replay,
five-run, 151-plus-two-prime gate.  The successful transcript therefore
does not benefit from a post-measurement threshold change.

## Decision and remaining launch gates

The measured exact branch passes, so the preregistered exact/Arb
dimension split is not activated.  This resolves the throughput
go/no-go only.  Full table production still waits for:

1. provenance and license review plus local vendoring of both complete
   source families;
2. generation and verification of the full deterministic prime
   schedule;
3. chunked production manifests and independent selected-entry replay.

The two overflow primes remain universal in production.  The artifact
contract remains approximately 2–3 GB before compression, with 29,904
work-residue bytes at the worst logical entry.

## Claim boundary

Across the frozen distribution sites and the named, hash-frozen
six-paper primary-literature perimeter, we found no numerical merit
attached to the frozen vectors; this is not a universal claim about the
QMC literature.

Primary artifacts:

- `data/workstream-b-streaming-pilot-preregistration.json`
- `data/workstream-b-streaming-pilot-preregistration-v2.json`
- `certificates/workstream-b-streaming-pilot-failed-v1.json`
- `certificates/workstream-b-streaming-pilot.json`
