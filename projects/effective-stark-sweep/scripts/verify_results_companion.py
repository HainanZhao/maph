#!/usr/bin/env python3
"""Minimal verifier for the Effective-Stark results-paper companion.

This program is deliberately smaller than the discovery pipeline.  It
checks the written theorem surface against the frozen exact records and
reruns the two independent exact computations used by the complete
referee audit: the Engine-B archimedean root audit and the corrected
six-route Engine-C primitive-packet bridge.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from decimal import Decimal, getcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
getcontext().prec = 80


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def run(command: list[str], marker: str) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode or marker not in result.stdout:
        raise RuntimeError(
            f"{' '.join(command)} failed\n{result.stdout}{result.stderr}"
        )


def verify_engine_a() -> None:
    paper = (ROOT / "paper/effective-stark-results.tex").read_text()
    record = load("data/engine-a-uniform-theorem-v1.json")
    if record["claim_tag"] != "VERIFIED_THEOREM":
        raise RuntimeError("Engine-A theorem tag changed")
    required = (
        "Uniform quadratic-support theorem",
        r"c_{A,\chi}",
        r"X_A=\prod_{\chi(R)=-1}",
        r"\frac{2}{I_\chi}",
    )
    if any(text not in paper for text in required):
        raise RuntimeError("Engine-A written theorem is incomplete")
    print("ENGINE_A=VERIFIED")


def ratio(lower: str, upper: str) -> Decimal:
    return Decimal(lower) / Decimal(upper)


def verify_engine_b() -> None:
    records = {
        "RQ-000190": load("data/q7-p7-case-v1.json"),
        "RQ-000419": load("data/q14-p7-case-v1.json"),
        "RQ-000108": load("data/rq000108-case-v1.json"),
        "RQ-000021": load("data/rq000021-case-v1.json"),
        "RQ-002057": load("data/q57-norm27-case-v1.json"),
        "RQ-002955": load("data/rq002955-case-v1.json"),
        "RQ-001107": load("data/q33-p11-order10-case-v1.json"),
        "RQ-000458": load("data/rq000458-dual-case-v1.json"),
    }
    q7 = records["RQ-000190"]
    common_v = q7["w3"]["analytic_arb_enclosure"][
        "voutier_degree_3_to_24_lower"
    ]
    values = {
        "RQ-000190": (
            q7["w2"]["safe_exponent"],
            ratio(
                common_v,
                q7["w3"]["analytic_arb_enclosure"]["powered_height_upper"],
            ),
            Decimal(5688),
        ),
        "RQ-000419": (
            records["RQ-000419"]["w2"]["safe_exponent"],
            ratio(
                common_v,
                records["RQ-000419"]["w3"]["analytic_arb_enclosure"][
                    "powered_height_upper"
                ],
            ),
            Decimal(7315),
        ),
        "RQ-000108": (
            records["RQ-000108"]["safe_exponent"],
            ratio(
                common_v,
                records["RQ-000108"]["identification"][
                    "powered_height_upper"
                ],
            ),
            Decimal(2460),
        ),
        "RQ-000021": (
            records["RQ-000021"]["safe_exponent"],
            ratio(
                common_v,
                records["RQ-000021"]["identification"][
                    "powered_height_upper"
                ],
            ),
            Decimal(4261),
        ),
        "RQ-002057": (
            records["RQ-002057"]["exponent"]["safe_exponent"],
            ratio(
                records["RQ-002057"]["identification"][
                    "analytic_arb_enclosure"
                ]["voutier_degree_3_to_24_lower"],
                records["RQ-002057"]["identification"][
                    "analytic_arb_enclosure"
                ]["powered_height_upper"],
            ),
            Decimal(748),
        ),
        "RQ-002955": (
            records["RQ-002955"]["safe_exponent"],
            ratio(
                common_v,
                records["RQ-002955"]["identification"][
                    "powered_height_upper"
                ],
            ),
            Decimal(5151),
        ),
        "RQ-001107": (
            records["RQ-001107"]["exponent"]["safe_exponent"],
            ratio(
                records["RQ-001107"]["height_window"][
                    "minimum_voutier_lower_bound"
                ],
                records["RQ-001107"]["identification"][
                    "powered_height_upper"
                ],
            ),
            Decimal(5817),
        ),
        "RQ-000458": (
            records["RQ-000458"]["engine_b"]["safe_exponent"],
            ratio(
                common_v,
                records["RQ-000458"]["engine_b"]["powered_height_upper"],
            ),
            Decimal(6470),
        ),
    }
    expected = (4032, 4032, 2880, 2016, 2592, 4032, 15840, 1152)
    for (case_id, (exponent, margin, threshold)), wanted in zip(
        values.items(), expected, strict=True
    ):
        if exponent != wanted or margin <= threshold:
            raise RuntimeError(f"{case_id}: exponent or margin failed")
    run(
        ["gp", "-q", "scripts/certify_engine_b_archimedean_places.gp"],
        "ENGINE_B_ARCHIMEDEAN_PLACE_AUDIT=VERIFIED",
    )
    print("ENGINE_B=VERIFIED")


def verify_engine_c() -> None:
    run(
        ["python3", "scripts/correct_engine_c_e6_primitive_packets.py"],
        "E6_PRIMITIVE_PACKET_CORRECTION=VERIFIED",
    )
    correction = load(
        "artifacts/engine-c-e6-primitive-packet-correction-v1.json"
    )
    if (
        correction["claim_tag"]
        != "VERIFIED_EXACT_PRIMITIVE_PACKET_CORRECTION"
        or len(correction["records"]) != 6
    ):
        raise RuntimeError("corrected e=6 record failed")
    q35 = load("artifacts/engine-c-w3-tranche-01-verified-v1.json")
    q6 = load("data/q6-norm8-case-v3.json")
    scope = load("artifacts/engine-c-claim-scope-correction-v1.json")[
        "current_theorem_tags"
    ]
    if not all(q35["gates"].values()):
        raise RuntimeError("Q(sqrt(35)) gate failed")
    if q6["routes"][0]["e"] != 8 or q6["routes"][0]["natural_s_size"] != 3:
        raise RuntimeError("Q(sqrt(6)) proof route changed")
    if (
        scope["q6_e12_route"] != "CROSS_CHECK_NOT_IN_PROOF"
        or scope["rq000458_engine_c"] != "DIAGNOSTIC_NOT_IN_PROOF"
    ):
        raise RuntimeError("Engine-C scope boundary changed")
    print("ENGINE_C=VERIFIED")


def verify_structural() -> None:
    paper = (ROOT / "paper/effective-stark-results.tex").read_text()
    parity = load("artifacts/results-paper-index-parity-lemma-v1.json")
    replay = load("artifacts/results-paper-odd-index-parity-audit-v1.json")
    if parity["claim_tag"] != "VERIFIED_THEOREM":
        raise RuntimeError("parity theorem tag changed")
    if (
        replay["verdict"] != "PASS"
        or replay["odd_index_greater_than_one_count"] != 446
        or replay["odd_index_rows_with_empty_support"] != 446
        or replay["odd_index_rows_with_trivial_sign_class"] != 446
        or replay["exception_count"] != 0
    ):
        raise RuntimeError("genuine odd-index replay failed")
    for name in ("Absolutely abelian ray fields", "Index parity"):
        if name not in paper:
            raise RuntimeError(f"written structural lemma missing: {name}")
    print("STRUCTURAL_LEMMAS=VERIFIED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "group",
        nargs="?",
        choices=("all", "engine-a", "engine-b", "engine-c", "structural"),
        default="all",
    )
    args = parser.parse_args()
    functions = {
        "engine-a": verify_engine_a,
        "engine-b": verify_engine_b,
        "engine-c": verify_engine_c,
        "structural": verify_structural,
    }
    selected = functions if args.group == "all" else {args.group: functions[args.group]}
    for function in selected.values():
        function()
    print("RESULTS_COMPANION=VERIFIED")


if __name__ == "__main__":
    main()
