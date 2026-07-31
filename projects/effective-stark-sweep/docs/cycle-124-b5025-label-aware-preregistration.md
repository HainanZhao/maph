# Cycle 124 — B5-025 label-aware preregistration

Amendment v17 freezes a correction batch of exactly RQ-000221 and
RQ-000228.  Both passed the exact B5-025 geometry gates apart from the
then-pre-registered identity-generator condition; both have `Mat(5)`.
The later label-aware proof is now part of the frozen input and maps a
target Artin label (a) to source label (5a) modulo six.

The batch validates the original RQ-000190 source certificate by hash,
then records its exact added-prime ray logs and the resulting
Artin-labelled subset products.  RQ-000216 and RQ-000246 stay excluded
because their source quotients are not coprime.  No packet claim is
made until the new sealer and successor ledger pass.
