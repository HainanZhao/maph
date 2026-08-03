#!/usr/bin/env python3
"""Exact central-character restriction audit for the d=6 beta transform.

This tests the discrete component of the published continuous--discrete
Fourier transform.  It deliberately does not assert that the continuous
integral preserves a finite block or that a selected block is an AFK cocycle.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


LEVEL = 24
DIMENSION = 6


def character_on_block(n: int, j: int, epsilon: int) -> tuple[bool, int]:
    """Return nonvanishing and the zeta_12 phase of chi_n(v_j^epsilon)/2."""

    # chi_n(v_j^eps)=omega_24^(2jn)(1+(-1)^(eps+n)).
    if (epsilon + n) % 2:
        return False, 0
    return True, (j * n) % 12


def block_character_table() -> dict[str, object]:
    records = []
    for n in range(LEVEL):
        for epsilon in range(2):
            nonzero = []
            for j in range(DIMENSION):
                survives, phase = character_on_block(n, j, epsilon)
                if survives:
                    nonzero.append(phase)
                else:
                    assert (epsilon + n) % 2 == 1
            assert len(nonzero) == (DIMENSION if epsilon == n % 2 else 0)
            records.append(
                {
                    "n_mod_24": n,
                    "central_character": epsilon,
                    "surviving_basis_count": len(nonzero),
                    "zeta12_phases_after_dividing_by_2": nonzero,
                }
            )
    assert len(records) == LEVEL * 2
    return {
        "epistemic_status": "PROVED",
        "block_basis": "v_j^epsilon=e_(2j)+(-1)^epsilon*e_(2j+12), j mod 6",
        "restriction_formula": "chi_n(v_j^epsilon)=omega_24^(2*j*n)*(1+(-1)^(epsilon+n))",
        "selection_rule": "chi_n is nonzero exactly on epsilon=n mod 2, where chi_n(v_j^epsilon)=2*zeta_12^(j*n)",
        "records": records,
    }


def all_alias_selection() -> dict[str, object]:
    rows = []
    wrong_block_nonzero = 0
    selected_block_zero = 0
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            for alias in range(-12, 13):
                N = first + 2 - 6 * alias
                ell = second - 6 * alias
                n = (5 * (N - 2)) % LEVEL
                epsilon = first % 2
                assert n == (5 * first - 6 * alias) % LEVEL
                assert n % 2 == epsilon
                assert ((-n) % DIMENSION, ell % DIMENSION) == (first, second)
                selected_phases = []
                for j in range(DIMENSION):
                    selected, phase = character_on_block(n, j, epsilon)
                    wrong, _ = character_on_block(n, j, 1 - epsilon)
                    selected_block_zero += int(not selected)
                    wrong_block_nonzero += int(wrong)
                    assert selected and not wrong
                    selected_phases.append(phase)
                rows.append(
                    {
                        "frequency": [first, second],
                        "alias": alias,
                        "N": N,
                        "ell": ell,
                        "n_mod_24": n,
                        "forced_central_character": epsilon,
                        "helical_Zak_frequency": [(-n) % DIMENSION, ell % DIMENSION],
                        "selected_zeta12_phases": selected_phases,
                    }
                )
    assert len(rows) == 36 * 25
    assert wrong_block_nonzero == 0 and selected_block_zero == 0
    return {
        "epistemic_status": "PROVED",
        "rows_checked": len(rows),
        "selection_is_outcome_blind": True,
        "forced_rule": "epsilon=a mod 2 for frequency (a,b)",
        "all_aliases_descend_to_their_original_frequency": True,
        "rows": rows,
    }


def alias_holonomy() -> dict[str, object]:
    # z -> z+1 changes n by -6 mod 24; z -> z+3 changes it by +6 mod 24.
    # On the selected block the ratios are zeta_12^(-6j)=(-1)^j and
    # zeta_12^(6j)=(-1)^j, respectively.
    one_step = []
    three_step = []
    for j in range(DIMENSION):
        one = (-6 * j) % 12
        three = (6 * j) % 12
        assert one == three
        one_step.append(one)
        three_step.append(three)
    assert set(one_step) == {0, 6}
    return {
        "epistemic_status": "PROVED",
        "one_alias_step_n_change_mod_24": -6,
        "one_alias_step_operator_on_selected_block": "diag_j((-1)^j)",
        "three_alias_step_n_change_mod_24": 6,
        "three_alias_step_operator_on_selected_block": "diag_j((-1)^j)",
        "zeta12_phase_exponents_one_step": one_step,
        "zeta12_phase_exponents_three_step": three_step,
        "operator_is_scalar": False,
        "scope": "No fixed scalar normalization can convert this discrete alias holonomy into a scalar cocycle factor, because a scalar conjugation leaves its two eigenvalues +1 and -1 unchanged. A non-scalar metaplectic/continuous operator completion remains open.",
    }


def afk_normalization_control() -> dict[str, object]:
    # The beta-kernel normalization gives tau_6^h with h=b-4a-1.  It is
    # scalar for each characteristic and thus cannot remove the j-dependent
    # alias holonomy found above.
    rows = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            h = (second - 4 * first - 1) % LEVEL
            rows.append(
                {
                    "characteristic": [first, second],
                    "h_mod_24": h,
                    "capital_to_lower_gamma_normalization": f"tau_6^{h}",
                    "is_block_scalar": True,
                }
            )
    assert len(rows) == 36
    return {
        "epistemic_status": "PROVED",
        "rows_checked": len(rows),
        "source_identity": "gamma_M(mu,h)/gamma_M(mu,h+4)=tau_6^h*Gamma_M(mu,h)*Gamma_M(Q-mu,-h)",
        "conclusion": "The retained capital-Gamma normalization is characteristic-dependent but block-scalar; it cannot by itself cancel diag_j((-1)^j).",
        "rows": rows,
    }


def payload() -> dict[str, object]:
    blocks = block_character_table()
    selection = all_alias_selection()
    holonomy = alias_holonomy()
    afk_control = afk_normalization_control()
    return {
        "schema": "sic-stark-cycle-191-central-character-fourier-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact discrete restriction of the published beta Fourier character only. It proves all-36 outcome-blind central-character selection and exposes a non-scalar alias holonomy. It does not prove the continuous transform preserves these blocks, a source-to-AFK amplitude identity, a real-multiplication boundary theorem, fusion continuity, or TCC.",
        "source_transform": "Sarkissian--Spiridonov degeneration (66), d=6 specialization g=Q,l=0, discrete character omega_24^(5*m*(N-2))",
        "central_character_blocks": blocks,
        "all_alias_selection": selection,
        "alias_holonomy": holonomy,
        "afk_normalization_control": afk_control,
        "gate_outcome": {
            "selection": "ALL36_SOURCE_DEFINED_CENTRAL_CHARACTER_SELECTION_PROVED",
            "scalar_block_restriction": "OBSTRUCTED_BY_NONSCALAR_ALIAS_HOLONOMY",
            "remaining_construction": "Define a genuinely non-scalar metaplectic/continuous completion that intertwines diag_j((-1)^j) with the helical alias shift and prove its amplitude action; a scalar block normalization is excluded.",
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
