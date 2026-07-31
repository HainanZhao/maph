# Cycle 105 — Cohen--Roblot object-control closure

## Outcome

The preregistered Cycle-104 exact subfield tranche completed under PARI
2.15.4.  Each selected degree-eight ray selector has an irreducible
degree-16 splitting polynomial and seven degree-four subfields.  The
associated Hilbert biquadratic field is contained for RQ-001569 over
Q(sqrt(42)) and RQ-007519 over Q(sqrt(186)), while it is not contained
for RQ-001894 over Q(sqrt(51)).

Together with the earlier degree-32 RQ-001262 control over Q(sqrt(35)),
the four-control result is three containments and one noncontainment.
Each result is `PROVED_EXACT_SUBFIELD_TEST`: PARI enumerates quartic
subfields exactly and tests their isomorphism to the frozen Hilbert
polynomial exactly.  The source transcript includes every nonzero
isomorphism.

## Claim boundary

This closes only the registered four-control field-object question.  It
does not establish a general containment law, identify a Stark unit or
packet, compare Artin labels, or certify that a row satisfies the
hypotheses of any Cohen--Roblot construction.  The mixed result is
therefore reported as a control table rather than generalized.

## Evidence and replay

Run:

```sh
python3 scripts/run_b5079_hilbert_containment.py
python3 scripts/run_hilbert_ray_containment_tranche.py
```

The versioned evidence is
`artifacts/b5079-hilbert-ray-containment-v1.json` and
`artifacts/hilbert-ray-containment-tranche-v1.json`.
