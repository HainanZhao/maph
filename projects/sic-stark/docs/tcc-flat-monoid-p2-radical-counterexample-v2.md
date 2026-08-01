# AFK flat-monoid P2 — certified radical counterexample

**Status:** CERTIFIED_NUMERICAL
**Date:** 2026-08-01 UTC
**Preregistration:** data/tcc-flat-monoid-p2-preregistration-v2.json

## Claim boundary

For the single admissible AFK overlap pilot

    d=12, K=Q(sqrt(13)), O=O_3, Q=<1,-11,1>,

the exact differenced partial-zeta derivative is nonzero on a certified
radical direction of the flat ray-class monoid algebra. This refutes the
universal route that would identify every AFK order-ray packet using only
ordinary monoid characters. It does not assert that no other
nonsemisimple theory exists, and it does not prove TCC.

## Certified result

The finite-algebra certificate gives the first radical basis vector

    y=e_3-e_0,

where e_0 is the zero class and e_3 is the class labelled by the AFK
characteristic (4,10). Kopp's zero-class statement gives
Z'(0,e_0)=0. The HJ period for the labelled class is [11], with three
double-sine arguments. Rigorous Arb integration gives

    Z'_(12 infinity_2)(0,e_3)
      in [-4.348280582567914, -4.348280577050716].

The interval excludes zero by more than 4.348. Hence the differenced
partial-zeta functional does not annihilate y.

By the proved semisimple descent criterion, this packet functional cannot
be a linear combination of ordinary monoid characters on this monoid.

## Replay

    projects/sic-stark/.venv/bin/python \
      projects/sic-stark/proof/certify_tcc_flat_monoid_p2_radical_counterexample.py
    python3 projects/sic-stark/proof/verify_tcc_flat_monoid_p2_radical_counterexample.py

The first command pins python-flint/Arb in the project virtual
environment. The second checks the frozen target, source and input hashes,
label, radical vector, fiber factor, and exclusion interval.
