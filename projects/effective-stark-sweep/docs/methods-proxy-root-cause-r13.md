# R-13 provenance rule and proxy-containment root cause

Effective 2026-07-30, every computational predicate that feeds a
classification or certificate is marked **GENUINE** (the required field or
group was fully reconstructed) or **PROXY** (a surrogate was used).  An
aggregate containing both is marked **MIXED**.  No effective `VERIFIED_*` tag,
including an intermediate W2 tag, may depend on a PROXY predicate.  Historical
artifacts are retained byte-for-byte; the R-13 provenance ledger is
authoritative for their current tags.

## Root cause

The proxy applied base conjugation to ideals and represented the images in the
same ray group without first proving that the finite modulus was fixed.  For a
conjugation-stable modulus this coincides with the required two-place
reconstruction; for an unstable modulus it does not reconstruct the actual
normal closure.  It entered five load-bearing paths without a provenance mark:
W1 Engine-B eligibility and index taxonomy, the Engine-C structural prefilter,
C-to-B rerouting, generic Engine-B W2 reconstruction, and the W4 index/trend
pass.  The tag taxonomy recorded whether two computed routes agreed, but not
whether either route reconstructed the intended object, so
`VERIFIED_W2_*` could be issued for proxy-on-one-side agreement.  This was a
joint architecture-and-verifier failure: the implementation treated agreement
as provenance, while the human verifier banked "246-for-246 two-route agreement"
under the same architecture-implies-genuine assumption.  R-13 separates those
questions mechanically.

## Containment

Case-level theorem promotion required genuine multi-route or complete splitting
closure evidence.  The audit therefore found zero false case-level theorem
tags.  Intermediate W2 aggregates containing proxy results are nevertheless
superseded.  RQ-007500's individual historical W2 tag was withdrawn, then
restored through a separate GENUINE reconstruction after the actual splitting
field and both imaginary-base ray reconstructions matched.  The containment
cost the census its statistics but not one of its theorems: the deepest
promotion layer held while the classification layer leaked.
