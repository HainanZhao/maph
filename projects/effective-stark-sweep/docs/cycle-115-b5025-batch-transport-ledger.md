# Cycle 115 — B5-025 transport batch and ledger successor

The corrected Cycle-112 batch promotes RQ-000195, RQ-000200,
RQ-000205, and RQ-000213 from the sealed RQ-000190 source packet.
Their exact local factor logs are respectively `(1)`, `(2)`, `(1)`
with exponent two, and `(1,2)`.  The formulas are the labelled
Euler-deletion subset products recorded in the batch artifact.

`engine-b-transport-ledger-v2.json` preserves v1 and records five
completed transports total (the earlier RQ-000039 plus these four),
leaving 227 unpromoted rows.  The rejected empty-factor v1 batch and
the RQ-000195 direct-replay cap record remain part of the history.
