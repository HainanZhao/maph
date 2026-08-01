#!/usr/bin/env python3
"""Reconcile the independent exact Cycle-1 baseline routes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
ROUTE_A_PATH = PROJECT / "artifacts" / "baseline-route-a-v3.json"
ROUTE_B_PATH = PROJECT / "artifacts" / "cycle-1-route-b-baseline.json"
ROUTE_B_BOTTLENECK_PATH = (
    PROJECT / "artifacts" / "cycle-1-route-b-v2-bottleneck-cell.json"
)
ROUTE_A_CASE_SPLIT_PATH = (
    PROJECT / "artifacts" / "theorem-1-2-case-split-route-a-v4.json"
)
ROUTE_B_CASE_SPLIT_PATH = (
    PROJECT / "artifacts" / "cycle-1-route-b-v3-theorem-1-2-case-split.json"
)
DEFAULT_OUTPUT = PROJECT / "artifacts" / "cycle-1-route-reconciliation-v3.json"


def canonical_hash(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_expression(value: str) -> str:
    """Normalize harmless presentational differences, not mathematics."""
    return value.replace("*", "").replace(" ", "")


def audit() -> dict[str, Any]:
    a = load(ROUTE_A_PATH)
    b = load(ROUTE_B_PATH)
    b_bottleneck = load(ROUTE_B_BOTTLENECK_PATH)
    a_case = load(ROUTE_A_CASE_SPLIT_PATH)
    b_case = load(ROUTE_B_CASE_SPLIT_PATH)

    a_math = {
        key: value
        for key, value in a.items()
        if key not in {"mathematical_certificate_sha256", "replay"}
    }
    a_math_hash_ok = canonical_hash(a_math) == a["mathematical_certificate_sha256"]
    a_script = PROJECT / a["replay"]["script"]
    a_script_hash_ok = file_hash(a_script) == a["replay"]["script_sha256"]

    b_script = PROJECT / "proof" / "replay_baseline_route_b.py"
    b_script_hash_ok = file_hash(b_script) == b["replay"]["script_sha256"]
    b_bottleneck_script = PROJECT / "proof" / "replay_bottleneck_cell_route_b_v2.py"
    b_bottleneck_script_hash_ok = (
        file_hash(b_bottleneck_script)
        == b_bottleneck["replay"]["script_sha256"]
    )
    a_case_math = {
        key: value
        for key, value in a_case.items()
        if key not in {"mathematical_certificate_sha256", "replay"}
    }
    a_case_math_hash_ok = (
        canonical_hash(a_case_math) == a_case["mathematical_certificate_sha256"]
    )
    a_case_script = PROJECT / a_case["replay"]["script"]
    a_case_script_hash_ok = file_hash(a_case_script) == a_case["replay"]["script_sha256"]
    b_case_script = PROJECT / "proof" / "replay_theorem_1_2_case_split_route_b_v3.py"
    b_case_script_hash_ok = file_hash(b_case_script) == b_case["replay"]["script_sha256"]

    a_bottleneck = a["zero_density_bottleneck_cell"]
    b_theorem_rows = {
        row["term"]: row["U_exponent"]
        for row in b_bottleneck["theorem_1_1_term_table"]["rows"]
    }
    b_energy_rows = {
        row["term"]: row["U_exponent"]
        for row in b_bottleneck["proposition_11_1_energy_table"]["rows"]
    }

    labeled = {
        "crossover_sigma": (
            a["crossover"]["sigma"],
            b["exact_case_analysis"]["crossover"]["unique_root_in_domain"],
        ),
        "density_coefficient": (
            a["crossover"]["global_density_coefficient_b"],
            b["exact_case_analysis"]["global_envelope"]["b"],
        ),
        "uniform_theta": (
            a["uniform_short_interval"]["theta"],
            b["short_interval_thresholds"]["uniform"]["theta"],
        ),
        "almost_all_theta": (
            a["almost_all_short_interval"]["theta"],
            b["short_interval_thresholds"]["almost_all"]["theta"],
        ),
        "critical_new_max": (
            a["critical_large_values_cell"]["guth_maynard_theorem_1_1"][
                "maximum_T_exponent"
            ],
            b["critical_large_values_cell"]["guth_maynard_theorem_1_1"][
                "max_T_exponent"
            ],
        ),
        "critical_classical_max": (
            a["critical_large_values_cell"]["classical_equation_1_1"][
                "maximum_T_exponent"
            ],
            b["critical_large_values_cell"]["classical_equation_1_1"][
                "max_T_exponent"
            ],
        ),
        "critical_gain": (
            a["critical_large_values_cell"]["strict_gain_in_T_exponent"],
            b["critical_large_values_cell"]["strict_gain"][
                "classical_minus_guth_maynard"
            ],
        ),
        "bottleneck_theorem_L2_Vm2": (
            a_bottleneck["theorem_1_1_at_U"]["terms"]["L^2*V^-2"],
            b_theorem_rows["L^2*V^-2"],
        ),
        "bottleneck_theorem_L18o5_Vm4": (
            a_bottleneck["theorem_1_1_at_U"]["terms"]["L^(18/5)*V^-4"],
            b_theorem_rows["L^(18/5)*V^-4"],
        ),
        "bottleneck_theorem_U_L12o5_Vm4": (
            a_bottleneck["theorem_1_1_at_U"]["terms"][
                "U*L^(12/5)*V^-4"
            ],
            b_theorem_rows["U*L^(12/5)*V^-4"],
        ),
        "bottleneck_energy_W_L4m4s": (
            a_bottleneck["proposition_11_1_energy_bound_at_U"]["terms"][
                "|W|*L^(4-4*sigma)"
            ],
            b_energy_rows["|W|*L^(4-4*sigma)"],
        ),
        "bottleneck_energy_W21o8_U1o4_L1m2s": (
            a_bottleneck["proposition_11_1_energy_bound_at_U"]["terms"][
                "|W|^(21/8)*U^(1/4)*L^(1-2*sigma)"
            ],
            b_energy_rows["|W|^(21/8)*U^(1/4)*L^(1-2*sigma)"],
        ),
        "bottleneck_energy_W3_L1m2s": (
            a_bottleneck["proposition_11_1_energy_bound_at_U"]["terms"][
                "|W|^3*L^(1-2*sigma)"
            ],
            b_energy_rows["|W|^3*L^(1-2*sigma)"],
        ),
        "bottleneck_local_to_global": (
            a_bottleneck["subinterval_aggregation"]["total_T_exponent"],
            b_bottleneck["local_to_global_count"]["combined_T_exponent"],
        ),
        "bottleneck_density_target": (
            "9/13",
            b_bottleneck["local_to_global_count"][
                "theorem_1_2_density_exponent_at_sigma"
            ],
        ),
        "case_type_ii": (
            normalized_expression(a_case["type_ii"]["conclusion"].split(" on ", 1)[0]),
            normalized_expression(b_case["type_ii"]["conclusion"]),
        ),
        "case_small_n_choice": (
            normalized_expression(a_case["integer_choice"]["small_n"]["choice"]),
            normalized_expression(
                b_case["integer_choice_regimes"]["small_n"]["choice"]
            ),
        ),
        "case_large_n_choice": (
            a_case["integer_choice"]["large_n"]["choice"],
            b_case["integer_choice_regimes"]["large_n"]["choice"],
        ),
        "case_large_n_o_one_retained": (
            "o(1)" in a_case["integer_choice"]["large_n"]["contained_conclusion"]
            and "no finite-T" in a_case["integer_choice"]["large_n"]["contained_conclusion"],
            "o(1)" in b_case["integer_choice_regimes"]["large_n"]["endpoint_containment"]
            and "not asserted" in b_case["integer_choice_regimes"]["large_n"]["endpoint_containment"],
        ),
        "case_gm_term_1": (
            normalized_expression(
                a_case["guth_maynard_branch_q_le_alpha"]["first_term"]["exponent"]
                + "<=B(s)"
            ),
            normalized_expression(
                b_case["guth_maynard_branch_q_le_alpha"]["term_1"]["conclusion"]
            ),
        ),
        "case_gm_term_2": (
            normalized_expression(
                a_case["guth_maynard_branch_q_le_alpha"]["second_term"]["exponent"]
                + "<=B(s)"
            ),
            normalized_expression(
                b_case["guth_maynard_branch_q_le_alpha"]["term_2"]["conclusion"]
            ),
        ),
        "case_gm_term_3": (
            normalized_expression(
                a_case["guth_maynard_branch_q_le_alpha"]["third_term"]["exponent"]
                + "<=B(s)"
            ),
            normalized_expression(
                b_case["guth_maynard_branch_q_le_alpha"]["term_3"]["conclusion"]
            ),
        ),
        "case_mvt_term_2_strict": (
            normalized_expression(
                a_case["mean_value_branch_q_gt_alpha"]["second_term"]["exponent"]
                + "<B(s)"
            ),
            normalized_expression(
                b_case["mean_value_branch_q_gt_alpha"]["term_2_strict"]["conclusion"]
            ),
        ),
        "case_strict_margin_factored_numerator": (
            (
                "250(s-3/4)^2+3/8"
                if "250(s-3/4)^2+3/8"
                in a_case["mean_value_branch_q_gt_alpha"]["second_term"]["margin_identity"]
                else "missing"
            ),
            normalized_expression(
                b_case["mean_value_branch_q_gt_alpha"]["term_2_strict"]["M_factored"]
                .split("]", 1)[0]
                .lstrip("[")
            ),
        ),
    }
    agreement = {label: left == right for label, (left, right) in labeled.items()}
    source_hash_agreement = (
        a["frozen_source"]["source_tarball_sha256"]
        == b["source_inputs"]["source_tarball_sha256"]
        == b_bottleneck["source_inputs"]["source_tarball_sha256"]
        == a_case["frozen_source"]["source_tarball_sha256"]
        == b_case["source_inputs"]["source_tarball_sha256"]
    )
    passed = (
        a_math_hash_ok
        and a_script_hash_ok
        and b_script_hash_ok
        and b_bottleneck_script_hash_ok
        and a_case_math_hash_ok
        and a_case_script_hash_ok
        and b_case_script_hash_ok
        and source_hash_agreement
        and all(agreement.values())
    )
    return {
        "schema": 3,
        "audit": "Cycle-1 independent exact-route reconciliation",
        "claim_boundary": (
            "Exact algebraic agreement conditional on the analytic source inputs; "
            "this does not independently prove those analytic theorems."
        ),
        "passed": passed,
        "supersedes": {
            "artifact": "artifacts/cycle-1-route-reconciliation-v2.json",
            "reason": (
                "Route A v4 and Route B v3 add every preregistered branch of "
                "the Section 13.1 Theorem 1.2 exponent case split."
            ),
        },
        "integrity": {
            "route_a_mathematical_hash": a_math_hash_ok,
            "route_a_script_hash": a_script_hash_ok,
            "route_b_script_hash": b_script_hash_ok,
            "route_b_bottleneck_script_hash": b_bottleneck_script_hash_ok,
            "route_a_case_split_mathematical_hash": a_case_math_hash_ok,
            "route_a_case_split_script_hash": a_case_script_hash_ok,
            "route_b_case_split_script_hash": b_case_script_hash_ok,
            "frozen_source_hash_agreement": source_hash_agreement,
        },
        "labeled_comparisons": {
            label: {"route_a": left, "route_b": right, "agree": agreement[label]}
            for label, (left, right) in labeled.items()
        },
        "route_independence": {
            "route_a": (
                "direct Fraction substitution and exponent evaluation, including "
                "the section-13.1 bottleneck cell"
            ),
            "route_b": (
                "cleared-denominator sign/case certificate and an independent "
                "bottleneck-cell implementation"
            ),
            "shared_implementation": False,
        },
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path, nargs="?", const=DEFAULT_OUTPUT)
    action.add_argument("--check", type=Path, nargs="?", const=DEFAULT_OUTPUT)
    args = parser.parse_args()
    data = audit()
    output = render(data)
    if args.write:
        args.write.write_text(output, encoding="utf-8")
    elif args.check:
        if args.check.read_text(encoding="utf-8") != output:
            print(f"reconciliation mismatch: {args.check}", file=sys.stderr)
            return 1
    else:
        print(output, end="")
    return 0 if data["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
