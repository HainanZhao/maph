# Cycle 168 working decision summary v1

`SEALED`: the canonical record is
`artifacts/cycle-168-edge-packet-join-v1.json`. The frozen question is in
`docs/cycle-168-edge-packet-join-preregistration-v1.md`.

## Strategic checkpoint

`OBSERVED` mentor decision: pursue a target-local packet/cross-edge join,
not closed-loop propagation. A loop has identity holonomy: its affine updates
telescope and same-label strip subtraction forces the terminal integer row to
equal the initial one for large `X`.

The live failure mode is support separation. Edge mass and packet mass must be
kept on their complete label/range/fraction/depth/constant fibres; their
global products have no incidence content.

`CORRECTION`: the join is not equality of a common key containing the packet
fraction/depth. An edge only needs a compatible packet at the same target
label and range. The exact ledger is the bipartite compatibility form
`J=sum_(e,p) E_e P_p 1_Comp(e,p)`, with depth and constants tested on the
packet/output side. This narrows the proposed engine and prevents an
artificial denominator-separation claim.

## First tasks

- `CONJECTURED`: derive the exact seed-plus-local-packet composition with the
  target edge endpoint as the Cycle-67 seed.
- `CONJECTURED`: build the weighted complete-key overlap ledger and identify
  the minimum labelled overlap that would retain a critical-depth recurrence.
- `CONJECTURED`: construct finite disjoint-support and trivial-holonomy
  countermodels before claiming a join mechanism.

## First finite probe

`OBSERVED`: `cycle_168_edge_packet_join_probe.py` verifies the target seed plus
local packet propagation identity, a compatible labelled join, a disjoint
target-label support model with zero join mass, and nontrivial-loop residual
failure. Thus weighted global populations cannot be multiplied into a join;
the next exact task is the complete-key fibre ledger.

## Seal outcome

`PROVED`: compatibility is a bipartite relation, not equality of an
over-refined key; the exact join mass is
`sum_(e,p) weight(e)weight(p)1_Comp(e,p)`. Compatible pairs have the exact
Cycle-67 propagation identity. Every nonjoin has exactly one ordered reason:
label, range, packet admissibility, depth, or strip constant. Direct loops
have trivial holonomy.

`OBSERVED` companion seal checkpoint: `APPROVE SEAL`. Its falsifier is a
misclassified pair, a mismatch in the weighted compatibility sum, or a
nontrivial valid loop. The next task is a genuine lower bound for the
compatibility form or a labelled support-separation inverse for actual banks.
