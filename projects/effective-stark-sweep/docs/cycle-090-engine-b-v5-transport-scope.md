# Cycle 090 — v5 Engine-B transport scope

## Outcome

`artifacts/engine-b-transport-manifest-v5.json` freezes the complete
member population for the next Engine-B stage.  It is a scope and
reconciliation artifact, not a packet-transport certificate.

- 232 genuine v5 Engine-B rows, partitioned into 88 exact
  normal-closure-polynomial groups;
- all 195 historical eligible IDs and all 159 historical pending member
  IDs remain in v5;
- 37 newly eligible v5 IDs are added;
- 73 v5 IDs lie outside the old pending-member list because that list
  excluded 36 historical direct/banked cases as well as the 37 new IDs;
- no member is promoted: all 232 records remain
  `UNSTARTED_NO_CASE_LEVEL_PACKET_CLAIM`.

## Historical polynomial-key discrepancy

Six historical Engine-B rows (`RQ-000970`, `RQ-000991`, `RQ-000993`,
`RQ-001004`, `RQ-002416`, and `RQ-004845`) have a different printed
normal-closure polynomial in the v5 reconstruction.  They retain their
v5 eligibility, but literal polynomial equality is not used to infer a
closure identity or transport relation.  The manifest preserves the
old and new populations and marks only the 59 literal historical
polynomial keys; 29 v5 polynomial keys are absent from the historical
ledger.

## Next gate

For every member, certify finite-modulus/conductor relation, ray-class
map including identity and sign labels, orientation at the frozen split
place, and an Artin-labelled packet distribution relation or direct
packet equality.  A failed or capped member remains visible.
