# C78 certification correction

## Correction — PROVED record defect

The sealed C78 v1 artifact labeled its endpoint theorem `PROVED`.  That
label is invalid under the repository epistemic rule: the \(Q=I/2\) endpoint
used in the proof is Song--Chen Proposition 3, currently arXiv:2603.25410v1,
a preprint rather than a published theorem.  The C78 source audit confirmed
the proposition's hypotheses and normalization, but did not independently
prove it.

## Affected and unaffected statements

- **Withdrawn:** C78's unconditional `PROVED` status and paper/publication
  readiness.
- **Retained — CONJECTURED conditional reduction:** if Song--Chen Proposition
  3 is correct, then endpoint interpolation proves the arbitrary-qubit,
  compatible three-qubit two-body-support extension exactly as stated in the
  C78 theorem note.
- **Unaffected:** C77's finite `OBSERVED` packet, its prior-known classical
  consistency replay, and all unrelated project artifacts.

## Required next action

Before any new proof/paper claim, either (a) give an independently replayable
proof of the \(Q=I/2\) compatible weighted endpoint, or (b) re-audit a
peer-reviewed source proving it.  The C78 manuscript remains an unpublished
draft and must say ``conditional on Proposition 3'' until then.
