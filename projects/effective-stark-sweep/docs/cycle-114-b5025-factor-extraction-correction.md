# Cycle 114 — B5-025 factor-extraction correction

The first B5-025 batch sealer produced an empty factor list for every
target.  The cause is concrete: its GP input lacked a final newline, so
GP accepted no final top-level expression when run through standard
input.  The resulting v1 artifact is preserved but rejected; it cannot
support a transport formula or ledger promotion.

The successor reruns the exact factor-log screen with a terminated GP
program and requires at least one explicit factor for every eligible
target.  It additionally checks the expected distinct-prime counts:
one for RQ-000195, RQ-000200, and RQ-000205, and two for RQ-000213.
