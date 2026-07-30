#!/usr/bin/env python3
"""Measure both Engine-B route exponents for the 11 overlap candidates."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "artifacts" / "dual-engine-alignment-queue-v1.json"
SCREEN = ROOT / "scripts" / "screen_engine_b_two_route.gp"
EXPONENT = ROOT / "scripts" / "compute_imaginary_divisor_exponent.gp"
OUTPUT = ROOT / "artifacts" / "dual-engine-exponent-screen-v1.json"
TRANSCRIPT = ROOT / "artifacts" / "dual-engine-exponent-screen-v1.transcript"


def scalar(text: str, key: str) -> str:
    matches = re.findall(rf"^{re.escape(key)}=(.+)$", text, re.MULTILINE)
    if len(matches) != 1:
        raise RuntimeError(f"expected one {key}, got {len(matches)}")
    return matches[0].strip()


def polynomial_coefficients(polynomial: str) -> tuple[int, int]:
    compact = polynomial.replace(" ", "")
    match = re.fullmatch(r"x\^2(?:(?P<a>[+-])x)?(?P<b>[+-]\d+)?", compact)
    if not match:
        raise RuntimeError(f"unsupported quadratic model: {polynomial}")
    a_value = -1 if match.group("a") == "-" else 1 if match.group("a") == "+" else 0
    b_value = int(match.group("b") or "0")
    return a_value, b_value


def hnf(text: str) -> list[list[int]]:
    match = re.fullmatch(
        r"\[(-?\d+),\s*(-?\d+);\s*(-?\d+),\s*(-?\d+)\]",
        text,
    )
    if not match:
        raise RuntimeError(f"unsupported conductor HNF: {text}")
    values = [int(value) for value in match.groups()]
    return [[values[0], values[1]], [values[2], values[3]]]


def run_gp(prelude: str, script: Path) -> str:
    completed = subprocess.run(
        ["gp", "-q"],
        input=(prelude + script.read_text()).encode(),
        capture_output=True,
        cwd=ROOT,
        timeout=3600,
        check=False,
    )
    text = (completed.stdout + completed.stderr).decode(errors="replace")
    if completed.returncode:
        raise RuntimeError(
            f"GP exit {completed.returncode}: {text[-1000:]}"
        )
    return text


def main() -> None:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    records = []
    with TRANSCRIPT.open("w", encoding="utf-8") as transcript:
        for case_index, case in enumerate(queue["records"], start=1):
            hnf_value = case["finite_ideal_hnf"]
            prelude = (
                f'CASE_ID="{case["case_id"]}";\n'
                f'D_VALUE={case["d"]};\n'
                f"H11={hnf_value[0][0]};H12={hnf_value[0][1]};"
                f"H21={hnf_value[1][0]};H22={hnf_value[1][1]};\n"
            )
            screen_text = run_gp(prelude, SCREEN)
            base_count = int(
                scalar(screen_text, "ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT")
            )
            if base_count != 2:
                raise RuntimeError(
                    f"{case['case_id']}: expected two bases, got {base_count}"
                )
            routes = []
            for route_index in range(1, base_count + 1):
                polynomial = scalar(
                    screen_text,
                    f"ROUTE2_BASE_{route_index}_POLYNOMIAL",
                )
                conductor = hnf(
                    scalar(
                        screen_text,
                        f"ROUTE2_BASE_{route_index}_CONDUCTOR",
                    )
                )
                a_value, b_value = polynomial_coefficients(polynomial)
                exponent_prelude = (
                    f'CASE_ID="{case["case_id"]}";\n'
                    f'ROUTE_LABEL="base_{route_index}";\n'
                    f"BASE_A={a_value};BASE_B={b_value};\n"
                    f"H11={conductor[0][0]};H12={conductor[0][1]};"
                    f"H21={conductor[1][0]};H22={conductor[1][1]};\n"
                )
                exponent_text = run_gp(exponent_prelude, EXPONENT)
                route = {
                    "route_index": route_index,
                    "base_polynomial": polynomial,
                    "conductor_hnf": conductor,
                    "divisor_count": int(
                        scalar(exponent_text, "SHINTANI_DIVISOR_COUNT")
                    ),
                    "safe_exponent": int(
                        scalar(exponent_text, "SHINTANI_SAFE_EXPONENT")
                    ),
                    "output_sha256": hashlib.sha256(
                        exponent_text.encode()
                    ).hexdigest(),
                }
                routes.append(route)
                transcript.write(
                    f"===== {case['case_id']} BASE {route_index} =====\n"
                    f"{exponent_text}\n"
                )
            best = min(
                routes,
                key=lambda route: (
                    route["safe_exponent"],
                    route["divisor_count"],
                    route["route_index"],
                ),
            )
            records.append(
                {
                    "case_id": case["case_id"],
                    "d": case["d"],
                    "finite_norm": case["finite_norm"],
                    "normal_closure_degree": 32,
                    "c_passing_packet_index": case[
                        "c_passing_packet_indices"
                    ][0],
                    "c_passing_packet_bases": case[
                        "c_passing_packet_bases"
                    ][0],
                    "b_bases": case["b_abelian_imaginary_bases"],
                    "base_sets_match_exactly": (
                        case["c_passing_packet_bases"][0]
                        == case["b_abelian_imaginary_bases"]
                    ),
                    "routes": routes,
                    "best_route": best,
                }
            )
            print(
                f"DUAL_EXPONENT={case_index}/11 "
                f"CASE={case['case_id']} BEST={best['safe_exponent']}",
                flush=True,
            )
    selected = min(
        records,
        key=lambda record: (
            record["best_route"]["safe_exponent"],
            record["normal_closure_degree"],
            record["finite_norm"],
            record["case_id"],
        ),
    )
    payload = {
        "schema": "effective-stark-dual-engine-exponent-screen-v1",
        "claim_tag": "VERIFIED_SELECTION_INPUTS",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_hashes": {
            "queue_sha256": hashlib.sha256(QUEUE.read_bytes()).hexdigest(),
            "b_screen_sha256": hashlib.sha256(SCREEN.read_bytes()).hexdigest(),
            "exponent_engine_sha256": hashlib.sha256(
                EXPONENT.read_bytes()
            ).hexdigest(),
        },
        "record_count": len(records),
        "records": records,
        "selected_case_id": selected["case_id"],
        "selected_safe_exponent": selected["best_route"]["safe_exponent"],
        "selection_rule": (
            "minimum measured safe exponent, then normal-closure degree, "
            "finite norm, and case ID"
        ),
        "transcript_sha256": hashlib.sha256(
            TRANSCRIPT.read_bytes()
        ).hexdigest(),
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"DUAL_SELECTED_CASE={selected['case_id']}")
    print(f"DUAL_SELECTED_EXPONENT={selected['best_route']['safe_exponent']}")


if __name__ == "__main__":
    main()
