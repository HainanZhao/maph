"""Frozen conventions for the first P7 Hecke-family transfer attempt.

The family is deliberately finite-order and finite-modulus only.  In
particular, no angular Groessencharacter parameter is present; adding one
would change both the conductor and the large-sieve geometry and therefore
requires a new preregistration.
"""
from __future__ import annotations


SCHEMA_VERSION = "p7-hecke-qi-v1"
FIELD = {
    "label": "K=Q(i)",
    "ring_of_integers": "Z[i]",
    "degree": 2,
    "absolute_discriminant": 4,
    "real_places": 0,
    "complex_places": 1,
    "class_number": 1,
}

FAMILY_CONVENTION = {
    "moduli": "nonzero integral ideals f of Z[i] with Q<Nf<=2Q",
    "Q_range": "real Q>=8; lower endpoint strict and upper endpoint inclusive",
    "characters": "one primitive character of the finite ray class group Cl(f) for each character whose exact finite conductor is f",
    "archimedean_type": "trivial; no angular parameter m is allowed",
    "infinity": "K has no real places, so narrow and ordinary finite ray-class conventions agree here",
    "character_multiplicity": "characters are counted as distinct functions on ideals; do not quotient by conjugation, inverse, Galois action, or a choice of ideal representative",
    "modulus_multiplicity": "each pair (f,chi) occurs once, indexed by its exact conductor f",
}

ZERO_CONVENTION = {
    "zero_set": "nontrivial zeros of the uncompleted L(s,chi) in 0<Re(s)<1",
    "region": "sigma<=Re(rho)<1 and |Im(rho)|<=T",
    "multiplicity": "included",
    "sigma_range": "1/2<=sigma<1",
    "height_range": "T>=2",
}

L_FUNCTION_CONVENTION = {
    "ideal_series": "L(s,chi)=sum_a chi(a)(Na)^(-s), with chi(a)=0 when (a,f)!=1",
    "ideal_euler_product": "product_p (1-chi(p)(Np)^(-s))^(-1) over prime ideals p",
    "norm_aggregation": "A_chi(n)=sum_{Na=n} chi(a), so L(s,chi)=sum_{n>=1} A_chi(n)n^(-s)",
    "ideal_count": "a_K(n)=#{a integral ideal of Z[i]: Na=n}=sum_{d|n} chi_{-4}(d)<=tau(n)",
}

# This is a prechosen algebraic witness for the *type-mismatch* half of G7.1.
# It is not a zero-density computation and does not claim a character-family
# large-values theorem.  Its calculation must be rerun before the gate can
# close.
REPEATED_NORM_WITNESS = {
    "shell": "Q=8, so N(3)=9 and N((1+i)^4)=16 both lie in (Q,2Q]",
    "moduli": ["f_3=(3)", "f_4=(1+i)^4=(4) up to a unit"],
    "ray_class_quotients": {
        "f_3": "(Z[i]/(3))^*/mu_4 has order 2",
        "f_4": "(Z[i]/(1+i)^4)^*/mu_4 has order 2; every proper pi-power quotient is trivial after dividing by mu_4",
    },
    "characters": "choose the unique nontrivial character in each displayed order-two quotient; both have exact displayed conductor",
    "split_prime": "17=(4+i)(4-i)",
    "evaluations": {
        "chi_3": "(1+i)^4=-1 in F_9, hence chi_3((4+i))=chi_3((4-i))=-1",
        "chi_4": "4+i=i and 4-i=-i modulo (4), both in mu_4, hence chi_4((4+i))=chi_4((4-i))=1",
    },
    "aggregated_coefficients": {
        "A_chi_3(17)": -2,
        "A_chi_4(17)": 2,
    },
    "conclusion": "two members of the same Q=8 shell give different aggregated coefficients at the repeated norm 17",
}

GATE_IDS = (
    "P7-0-SOURCE-FAMILY",
    "P7-1-NORM-AGGREGATION",
    "P7-2-RAY-CLASS-ORTHOGONALITY",
    "P7-3-IDEAL-CUBIC-ENERGY",
    "P7-4-DETECTOR-TAIL",
    "P7-5-PRIME-IDEAL-SHORT-INTERVALS",
)

NO_GO_OR_NON_PROMOTION = (
    "No direct import of the single-coefficient-vector Guth--Maynard large-value theorem to the joint (chi,t) family.",
    "No new Hecke zero-density estimate, zero-free region, Bombieri--Vinogradov theorem, bounded-gap theorem, or short-interval theorem.",
    "No assertion that a tau(n) loss is harmless until the exact target large-value statement and its epsilon bookkeeping are checked.",
    "No treatment of angular characters, variable fields, varying discriminants, or arbitrary Hecke characters.",
)
