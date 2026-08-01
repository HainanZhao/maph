"""v2 status correction for the frozen P7 Q(i) conventions.

No family, range, gate, source, or mathematical threshold changes from v1.
The preselected repeated-norm witness is now explicitly CONJECTURED until
P7-1 performs its separately authorized exact calculation.
"""
from __future__ import annotations

from conventions.p7_hecke_qi_v1 import (  # re-export frozen v1 conventions
    FAMILY_CONVENTION,
    FIELD,
    GATE_IDS,
    L_FUNCTION_CONVENTION,
    NO_GO_OR_NON_PROMOTION,
    ZERO_CONVENTION,
)


SCHEMA_VERSION = "p7-hecke-qi-v2"
REPEATED_NORM_WITNESS = {
    "epistemic_status": "CONJECTURED",
    "status_boundary": "Frozen prospective algebraic witness only. It becomes PROVED only if P7-1 independently checks the exact ray-class quotient, conductor, and evaluations.",
    "shell": "Q=8, so N(3)=9 and N((1+i)^4)=16 both lie in (Q,2Q]",
    "moduli": ["f_3=(3)", "f_4=(1+i)^4=(4) up to a unit"],
    "ray_class_quotients": {
        "f_3": "(Z[i]/(3))^*/mu_4 has order 2",
        "f_4": "(Z[i]/(1+i)^4)^*/mu_4 has order 2; every proper pi-power quotient is trivial after dividing by mu_4",
    },
    "characters": "choose the unique nontrivial character in each displayed order-two quotient; both are expected to have exact displayed conductor",
    "split_prime": "17=(4+i)(4-i)",
    "evaluations": {
        "chi_3": "(1+i)^4=-1 in F_9, expected to give chi_3((4+i))=chi_3((4-i))=-1",
        "chi_4": "4+i=i and 4-i=-i modulo (4), expected to give chi_4((4+i))=chi_4((4-i))=1",
    },
    "aggregated_coefficients": {
        "A_chi_3(17)": -2,
        "A_chi_4(17)": 2,
    },
    "conjectured_conclusion": "two members of the same Q=8 shell have different aggregated coefficients at repeated norm 17",
}
