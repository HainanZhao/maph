# Cycle 097 — RQ-005298 partial-run correction

The original Cycle-093 process reached the order-16 subgroup-resolution
stage and grew its PARI stack to the full 4,000,000,000-byte cap.  It
was intentionally interrupted after 3,485.72 seconds to apply the
authorized 10 GB resource amendment.  As with the RQ-002397 retry, GP
returned exit status zero; the preserved v1 process-status field
therefore says `COMPLETED` even though stderr says `user interrupt` and
stdout lacks the final geometry verdict.

The v2 successor corrects the status to `PARTIAL_RESOURCE_CAP_RUN`.
It establishes neither eligibility nor ineligibility.  The identical
calculation is restarted under the Cycle-096 10 GB cap.
