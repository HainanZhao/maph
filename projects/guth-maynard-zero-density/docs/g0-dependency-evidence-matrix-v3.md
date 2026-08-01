# G0 dependency/evidence matrix v3 correction

**Claim boundary — OBSERVED.** This is a versioned correction to the G0
evidence matrix record. It reports a finite set of sealed artifacts and their
existing bounded labels; it does not re-prove the mathematics or declare G0
PASS.

Run:

```sh
python3 proof/audit_g0_dependency_evidence_v3.py --check
```

## Correction

V2 dynamically inventoried all JSON artifacts. It was subsequently refreshed
in place after official-source and Route-B-v5 artifacts were created. That was
incorrect for an evidence record: it changed v2 inventory membership, counts,
source-manifest-currentness, timing enumeration, and raw artifact identity.

V3 preserves the current post-refresh v2 byte hash
`504cc31047ba8191cd1996ee7238cf3f95ab8e007f75824b39307999abb131ae` and
does not edit v2 further. No pre-refresh v2 hash, archive, commit, or retained
correction record was recoverable from the local worktree, so v3 records it as
`UNRECOVERABLE_FROM_LOCAL_WORKTREE` rather than guessing an identity.

## Fixed scope

The v3 replay checks only its named frozen dependencies: source-manifest v3;
Cycle-1 and Stream-B reconciliations; official source closure v4/checker and
the independent SWORD audit; and Stream-C Routes A/B v5. Future G1 artifacts
are explicitly outside this scope and cannot stale v3.

G0 remains open. A hostile v5 Route-A/Route-B reconciliation and complete
preregistered per-route resource evidence remain required. Route-v5 timing
files are intentionally mutable `OBSERVED` measurements and are not sealed as
mathematical evidence.
