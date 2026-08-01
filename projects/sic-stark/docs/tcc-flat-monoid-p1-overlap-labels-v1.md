# AFK flat-monoid P1 overlap pilot — characteristic labels

**Status:** PROVED_FINITE_LABEL_MAP
**Date:** 2026-08-01 UTC
**Preregistration:** data/tcc-flat-monoid-p1-preregistration-v3-labels.json

## Claim boundary

This note identifies all 144 AFK characteristics for the admissible
d=12, f=3 form Q=<1,-11,1> with the 50 classes of the previously
certified flat monoid. It does not evaluate a partial zeta value or make
a packet, support, radical-annihilation, or TCC claim.

## Derivation

The form has discriminant 117=3 squared times 13, so it has fundamental
discriminant 13 and conductor 3. Its positive fixed point is

    beta=(11+3 sqrt(13))/2=-14+theta_3,

and Z+beta Z=O_3. Kopp's correspondence theorem therefore applies at
the invertible modulus 12 O_3. With b=O_3 and alpha=12 in the inverse
Upsilon construction, the characteristic p=(p1,p2) gives the class

    [(p2 beta-p1) O_3].

A totally-positive lift leaves the residue unchanged modulo 12 O_3 and
sets the selected real-place sign positive. In the residue/sign basis of
the monoid artifact this is

    (-p1-14 p2, p2, +1) modulo 12.

The positive-trace stabilizer

    L=[[0,1],[-1,11]]

fixes beta and acts on column characteristics. Its 144-element finite
action has 50 orbits. The label formula is constant on every orbit and
maps those 50 orbits bijectively onto the 50 monoid elements.

## Exact replay

    python3 projects/sic-stark/discovery/build_tcc_flat_monoid_p1_overlap_labels.py
    python3 projects/sic-stark/proof/verify_tcc_flat_monoid_p1_overlap_labels.py

The independent verifier recomputes the stabilizer action, every residue
formula, orbit constancy, bijection, and the zero-class label.
