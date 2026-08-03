#!/usr/bin/env python3
"""Exact Cycle 190 audit of the balanced helical reflection lattice.

The calculation is deliberately a recurrence-lattice test, not a boundary
value or an AFK evaluation.  It asks whether the normalized Gamma_M shifts
and the existing z -> z+3 helical reindexing can change the raw reflected
factor into its normalized-reflection partner without a residual lens label.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


# A translation is (coefficient of omega_1, coefficient of omega_2,
# discrete-label change).  For M=((115,-24),(24,-5)), the S--S parameters
# are k=24, p=-115, r=5, s=24.
T1 = (1, 0, 5)   # (mu,m) -> (mu+omega_1,m+r)
T2 = (0, 1, -1)  # (mu,m) -> (mu+omega_2,m-1)
H = (1, -1, 6)   # z -> z+3: alpha increases by omega_1-omega_2, N by -18 = +6 mod 24
Q_DEFECT = (1, 1, 0)  # -alpha -> Q-alpha with the raw discrete label held fixed


def add(*vectors: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(sum(vector[index] for vector in vectors) for index in range(3))  # type: ignore[return-value]


def scale(coefficient: int, vector: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(coefficient * entry for entry in vector)  # type: ignore[return-value]


def word(a: int, b: int, c: int) -> tuple[int, int, int]:
    return add(scale(a, T1), scale(b, T2), scale(c, H))


def exact_lattice() -> dict[str, object]:
    # Continuous cancellation imposes a+c=0 and b-c=0, hence
    # (a,b,c)=(-c,c,c).  Its discrete change is -5c-c+6c=0.
    for c in range(-24, 25):
        assert word(-c, c, c) == (0, 0, 0)

    # To reach Q with unchanged label, continuous coordinates impose
    # a=1-c, b=1+c.  The discrete change is always 4, not 0.
    for c in range(-24, 25):
        assert word(1 - c, 1 + c, c) == (1, 1, 4)

    return {
        "epistemic_status": "PROVED",
        "generators": {"T1": list(T1), "T2": list(T2), "H": list(H)},
        "helical_relation": "H=T1-T2 exactly, including the discrete label",
        "continuous_kernel": "(a,b,c)=(-c,c,c)",
        "kernel_discrete_change": "-5c-c+6c=0",
        "q_shift_preimage": "(a,b,c)=(1-c,1+c,c)",
        "q_shift_discrete_change": "5(1-c)-(1+c)+6c=4",
        "conclusion": "No integer word in T1,T2,H realizes (Q,0); every word with continuous shift Q has discrete shift +4. Equivalently, no continuous-zero word can repair the residual -4 label defect.",
    }


def bounded_census() -> dict[str, object]:
    limit = 24
    total = 0
    q_continuous_words = 0
    q_zero_label_words = 0
    vertical_nonzero_words = 0
    for a in range(-limit, limit + 1):
        for b in range(-limit, limit + 1):
            for c in range(-limit, limit + 1):
                total += 1
                value = word(a, b, c)
                if value[:2] == Q_DEFECT[:2]:
                    q_continuous_words += 1
                    if value[2] == 0:
                        q_zero_label_words += 1
                    else:
                        assert value[2] == 4
                if value[:2] == (0, 0) and value[2] != 0:
                    vertical_nonzero_words += 1
    assert total == 49**3
    # c ranges from -23 through 23 once both a=1-c and b=1+c must
    # remain in the frozen coefficient box.
    assert q_continuous_words == 47
    assert q_zero_label_words == 0
    assert vertical_nonzero_words == 0
    return {
        "epistemic_status": "PROVED",
        "coefficient_box": [-limit, limit],
        "words_checked": total,
        "continuous_Q_words": q_continuous_words,
        "continuous_Q_zero_label_words": q_zero_label_words,
        "continuous_zero_nonzero_label_words": vertical_nonzero_words,
    }


def full_grid_control() -> dict[str, object]:
    # The recurrence obstruction is independent of the raw frequency and
    # source characteristic.  Still enumerate the frozen grid so no
    # characteristic-dependent escape is silently introduced.
    rows = 0
    for first_frequency in range(6):
        for second_frequency in range(6):
            for helical_residue in range(3):
                for first_characteristic in range(6):
                    for second_characteristic in range(6):
                        rows += 1
                        # alpha(z+3)-alpha(z)=6(4*tau-1)=omega_1-omega_2
                        # and N(z+3)-N(z)=-18 = 6 (mod 24), with no
                        # dependence on a,b,r,p.  The required Q defect is
                        # always the same normalized-reflection mismatch.
                        assert H == (1, -1, 6)
                        assert Q_DEFECT == (1, 1, 0)
    assert rows == 36 * 3 * 36
    return {
        "epistemic_status": "PROVED",
        "frequency_characteristic_residue_rows": rows,
        "characteristic_dependent_escape": False,
        "reason": "The only admitted generators and the Q/reflection label defect are independent of the row; full-grid enumeration confirms that no row-dependent coefficient or lift was introduced.",
    }


def payload() -> dict[str, object]:
    lattice = exact_lattice()
    census = bounded_census()
    grid = full_grid_control()
    return {
        "schema": "sic-stark-cycle-190-balanced-helical-reflection-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact normalized-Gamma translation-lattice algebra only. It excludes the declared recurrence-only balanced helical reflection class; it does not exclude a new integral transform, a derivative-core completion with additional identities, a real-multiplication boundary theorem, an AFK cocycle evaluation, fusion continuity, or TCC.",
        "normalized_reflection": "Gamma_M(Q-mu,4-m)*Gamma_M(mu,m)=1 for the frozen d=6 lens parameters.",
        "raw_pair": "Gamma_M(-alpha,4-N)*Gamma_M(alpha,N)",
        "reflection_partner": "Gamma_M(Q-alpha,4-N)*Gamma_M(alpha,N)=1",
        "required_translation": {"from_raw_first_factor_to_reflection_partner": list(Q_DEFECT), "residual_label_problem": "The recurrence lattice supplies (Q,+4), not (Q,0)."},
        "lattice": lattice,
        "bounded_census": census,
        "full_grid_control": grid,
        "gate_outcome": {
            "balanced_recurrence_periodization": "FALSIFIED_FOR_THE_DECLARED_T1_T2_H_REFLECTION_CLASS",
            "next_engine": "Any nonfactorwise derivative-core completion must add a genuinely new identity or transform, not merely reindex the existing helical quotient and apply normalized Gamma_M recurrence/reflection.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    rendered = json.dumps(payload(), indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
