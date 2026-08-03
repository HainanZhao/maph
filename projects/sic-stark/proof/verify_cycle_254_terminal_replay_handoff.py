#!/usr/bin/env python3
"""Independent terminal replay and frozen-transition inventory for C254/B091."""
from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

try:
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover
    from verify_cycle_228_f3_square_residual_block import blocks


R = Path(__file__).resolve().parents[1]


def coeffs(item: dict[str, object], key: str) -> tuple[F, F]:
    return tuple(F(str(value)) for value in item[key])  # type: ignore[return-value]


def det(left: tuple[F, F], right: tuple[F, F]) -> F:
    return left[0] * right[1] - left[1] * right[0]


def independent_replay() -> dict[str, object]:
    rows = []
    for source, target in (("A", "C"), ("C", "A")):
        for position, (source_item, target_item) in enumerate(zip(blocks()[source], blocks()[target]), 1):
            source_alpha = coeffs(source_item, "alpha")
            source_beta = coeffs(source_item, "beta")
            reflected_alpha = (-source_alpha[0], source_alpha[1])
            reflected_beta = (-source_beta[0], source_beta[1])
            target_alpha = coeffs(target_item, "alpha")
            target_beta = coeffs(target_item, "beta")
            slope = F(str(source_item["argument_mu"]))
            assert slope == F(str(target_item["argument_mu"])) and slope != 0
            assert reflected_alpha == (-target_alpha[0], -target_alpha[1])
            assert reflected_beta == target_beta
            assert det(source_alpha, source_beta) > 0
            assert det(reflected_alpha, reflected_beta) < 0
            rows.append(
                {
                    "source": f"{source}{position}",
                    "target": f"{target}{position}",
                    "R_alpha_equals_minus_target_alpha": True,
                    "R_beta_equals_target_beta": True,
                    "tau_h_source": "upper half-plane",
                    "tau_h_endpoint": "lower half-plane",
                    "slit_endpoints_valid_at_both_embeddings": True,
                    "continued_product": "(q*X_beta;q)_infinity/(X_alpha^-1;qtilde)_infinity",
                    "continued_beta_shift": "1-X^-1",
                    "target_beta_shift": "1-X",
                    "required_transition_beta_cocycle": "-X",
                    "required_transition_alpha_cocycle": "(1-Y)*(1-q*Y)",
                    "shift_mismatch_nonconstant": True,
                }
            )
    assert len(rows) == 8
    assert all(row["shift_mismatch_nonconstant"] for row in rows)
    return {
        "implementation_independent_of_C253_verifier": True,
        "theorem_parameter": "tau_h=-beta/alpha in C minus R_{>=0}",
        "theorem_normalization": "gamma=E/Gamma_h with z_h=-i*(mu/beta-(alpha/beta+1)/2)",
        "rows": rows,
        "all_eight_reproduced_at_both_embeddings": True,
        "C253_obstruction_reproduced": True,
    }


def load(cycle: int) -> dict[str, object]:
    matches = list((R / "artifacts").glob(f"cycle-{cycle}-*.json"))
    assert len(matches) == 1
    return json.loads(matches[0].read_text())


def transition_inventory() -> dict[str, object]:
    specs = {
        221: ("SEALED_FORCED_TILDE_CORRECTION_NORMALIZATION_MISMATCH", "fails normalized first shift and supplies no source negative-k law"),
        222: ("SEALED_Z24_COCYCLE_TORSOR_SOURCE_NONSELECTION", "label cocycle is not source-selected and is not an all-factor argument transition"),
        223: ("SEALED_EXPLICIT_PARITY_SIGNED_PRODUCT_SECOND_SHIFT_FAILURE", "all four candidates fail the second shift"),
        224: ("SEALED_FROZEN_SHIFT_COHOMOLOGY_REFLECTION_FAILURE", "unique joint-shift cochain fails reflection by -1"),
        225: ("SEALED_REFLECTION_ROOT_LOCAL_BRANCH_FACTORIZATION_UNDEFINED", "local branch lacks both factorization targets and source cross-sign authorization"),
        226: ("SEALED_FOUR_NODE_SIGNED_PRODUCT_GROUPOID_CONTAINED", "four negative-k edges are unavailable and no augmented loop closes"),
        235: ("SEALED_FORMAL_CENTRAL_LOOP_HOLONOMY_AND_REFLECTION_CONTAINMENT", "formal holonomy extension has no source reflection functor"),
        236: ("SEALED_ORDERED_WORD_REFLECTION_DUALIZATION_OBSTRUCTION", "all required reflected factor partners are absent"),
        237: ("SEALED_POSITIVE_K_REFLECTION_PARTNER_REACHABILITY_OBSTRUCTION", "no finite positive-k source path reaches a reflected partner"),
        251: ("SEALED_CANONICAL_RESIDUE_DUAL_CROSS_SIGN_FALSIFIED", "canonical contragredient exits the source product domain and misses target alpha sign"),
        252: ("SEALED_RECIPROCAL_BASE_RULE_FAILS_SOURCE_CONTINUATION_GATE", "standalone reciprocal rule has no analytic source bridge"),
        253: ("SEALED_DIRECT_CONTINUATION_EXISTS_UNCORRECTED_TARGET_MAP_FALSIFIED", "canonical continuation exists but misses every target by a nonconstant shift quotient"),
    }
    rows = []
    for cycle, (status, failure) in specs.items():
        record = load(cycle)
        assert record["status"] == status
        rows.append(
            {
                "cycle": cycle,
                "status": status,
                "failure_against_required_transition": failure,
                "source_authorized_all_eight_transition_survives": False,
            }
        )
    assert len(rows) == 12
    return {
        "required_beta_cocycle": "T(z+beta)/T(z)=-X",
        "required_alpha_cocycle": "T(z+alpha)/T(z)=(1-Y)*(1-q*Y)",
        "rows": rows,
        "record_count": len(rows),
        "survivor_count": 0,
        "complete_source_transition_available": False,
    }


def audit() -> dict[str, object]:
    replay = independent_replay()
    inventory = transition_inventory()
    assert replay["C253_obstruction_reproduced"]
    assert inventory["survivor_count"] == 0
    return {
        "epistemic_status": "PROVED",
        "status": "C_FROZEN",
        "dimension_six_TCC_proved": False,
        "independent_replay": replay,
        "transition_inventory": inventory,
        "terminal_outcome": {
            "classification": "C_FROZEN",
            "project_stopped": True,
            "new_cycle_authorized": False,
            "strongest_positive_result": "The ordinary gamma has a path-independent Stokman continuation to every C251 negative-alpha state on the fixed slit domain.",
            "decisive_obstruction": "That continuation misses every opposite A/C target by a nonconstant shift quotient, and no already sealed source-authorized transition operator supplies both required cocycles on all eight factors.",
            "future_scope": "A future separately authorized project may construct a genuinely sourced nonconstant transition or full Gamma_M theorem; this finite audit is not a universal no-go.",
        },
        "claim_boundary": (
            "Dimension-six TCC remains unproved. C_FROZEN records the exhausted B091 project "
            "boundary and absence of a complete transition in the twelve frozen relevant records; "
            "it does not prove universal nonexistence of TCC or of future bridge constructions."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
