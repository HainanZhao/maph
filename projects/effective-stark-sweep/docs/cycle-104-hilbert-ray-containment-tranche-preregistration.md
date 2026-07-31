# Cycle 104 — Hilbert/ray containment tranche preregistration

This cycle completes three more object-level controls for the
Cohen--Roblot comparison.  It follows, but does not modify, the first
control in `cycle-102-hilbert-ray-containment-preregistration.md`.

The frozen targets are the following certified Engine-C real selector
fields, together with the Hilbert biquadratic field for the indicated
real quadratic base.

| case | base | real selector polynomial | Hilbert field polynomial |
|---|---|---|---|
| RQ-001569 | Q(sqrt(42)) | `x^8+10*x^6-12*x^5+9*x^4+24*x^3-44*x^2+12*x+1` | `y^4-46*y^2+361` = Q(sqrt(2),sqrt(21)) |
| RQ-001894 | Q(sqrt(51)) | `x^8+10*x^6-120*x^5-1050*x^4+1950*x^3+5875*x^2-14550*x+8725` | `y^4-40*y^2+196` = Q(sqrt(3),sqrt(17)) |
| RQ-007519 | Q(sqrt(186)) | `x^8+10*x^6-12*x^5-99*x^4+312*x^3-584*x^2+372*x+217` | `y^4-190*y^2+8281` = Q(sqrt(2),sqrt(93)) |

For each target, construct the splitting field of the frozen selector
polynomial using PARI's exact `nfsplitting`, enumerate its degree-four
subfields using `nfsubfields`, and test isomorphism to the stated
Hilbert polynomial using `nfisisom`.  Record every nonzero isomorphism
and the resulting count.  The initial resource ceiling is 3 GB PARI
stack and 3,600 seconds per target.

A positive test proves only that the selected ray normal closure
contains an isomorphic copy of the displayed Hilbert field.  A negative
test proves only noncontainment for that frozen normal closure.  Neither
outcome identifies a Stark unit, an Artin-labelled packet, or a
row-level theorem-hypothesis match with Cohen--Roblot.
