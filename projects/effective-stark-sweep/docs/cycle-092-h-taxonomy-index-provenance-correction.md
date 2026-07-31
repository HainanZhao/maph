# Cycle 092 — H taxonomy index-provenance correction

`census-h-taxonomy-v1.json` copied its displayed `shintani_index` from
the legacy W1 record, although v5 eligibility is governed by the
genuine common-stable-modulus index ledger.  The error is corrected in
the successor `census-h-taxonomy-v2.json`; v1 remains unchanged.

RQ-005298 is the decisive control.  W1 displayed index two, but the
genuine reconstruction has normal-closure relative degree 128,
maximal abelian relative degree 32, and derived subgroup order four.
It is therefore not Shintani index-two eligible.  Its separate quartic
Engine-C record remains tool-deferred: the order-16 normal-closure
resolvent exceeded the registered computation cap.

The correction changes only displayed index provenance.  It changes no
H-row count, no Engine-B or Engine-C eligibility flag, no Roblot status,
and no frontier minimum.  The manuscript now states this distinction
explicitly.
