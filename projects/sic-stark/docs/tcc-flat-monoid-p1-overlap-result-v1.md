# AFK flat-monoid P1 overlap pilot — exact algebra result

**Status:** PROVED_FINITE_ALGEBRA_PILOT
**Date:** 2026-08-01 UTC
**Preregistration:** data/tcc-flat-monoid-p1-preregistration-v2.json

## Claim boundary

For the single AFK row d=12, K=Q(sqrt(13)), O_3, and modulus 12 O_3,
the finite flat O_3-invertible ray-class monoid has been constructed
exactly under the class-number-one quotient lemma. Its rational monoid
algebra has a nonzero Jacobson radical. This result does not evaluate
AFK's partial zeta functions, identify an overlap packet, classify
support, or prove TCC.

## Exact result

The monoid has 50 elements, of which 24 are primitive. Let A=Q[M] and
J=Jac(A). Exact regular-representation trace arithmetic gives

    dim_Q(A)=50,
    dim_Q(A/J)=31,
    dim_Q(J)=19,
    dim_Q(J squared)=2,
    J cubed=0.

The independent verifier reconstructs all 288 residue/sign pairs, their
unit orbits, the full multiplication table, the trace Gram matrix, and
the listed radical basis. It verifies rank 31, linear independence of the
19 radical vectors, dim(J squared)=2, and J cubed=0.

## Meaning

This is the first frozen AFK conductor-modulus-overlap control in the
successor plan. Unlike the benign d=7,f=2 control, it has a large
nonsemisimple direction. By the semisimple descent criterion, ordinary
monoid-character Engine-A data can describe the AFK differenced packet
only if the actual AFK functional vanishes on these 19 radical directions.
That vanishing is now a concrete, finite, separately unevaluated
obligation.

## Replay

    python3 projects/sic-stark/discovery/build_tcc_flat_monoid_p1_overlap_adapter.py
    python3 projects/sic-stark/proof/verify_tcc_flat_monoid_p1_overlap_adapter.py

The generated evidence is
discovery/tcc-flat-monoid-p1-overlap-adapter-v1.json. The first command
uses no partial-zeta or packet evaluation; the second is an independent
exact audit of the finite algebra.
