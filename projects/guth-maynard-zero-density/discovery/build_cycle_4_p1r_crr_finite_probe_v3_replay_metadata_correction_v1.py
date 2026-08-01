#!/usr/bin/env python3
"""Seal/check the narrow replay-metadata correction for CRR probe v3."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import statistics
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-4-p1r-crr-finite-probe-v3-replay-metadata-correction-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "immutable_v3_result": (ROOT / "discovery/cycle-4-p1r-crr-finite-probe-v3.json", "41576b9ad21d44435d251a8fefad1cc64bb038384644ce93c1d1a4314c38a0cb"),
    "immutable_v3_runner": (ROOT / "discovery/run_cycle_4_p1r_crr_finite_probe_v3.py", "667207f0f690aaf36f33fa498a5b90594e2ac500173c44db64388e2958b4d90f"),
    "semantic_replay": (ROOT / "discovery/cycle-4-p1r-crr-finite-probe-v3-semantic-replay-v1.json", "8d4524a43220d067d56d2adb36f33fb8580b732ef9b862d47b582d10e3c35721"),
    "correction_document": (ROOT / "docs/cycle-4-p1r-crr-finite-probe-v3-replay-metadata-correction-v1.md", "cb67f420157858d6ada3497766711fda77e03352f85bd550132d217ff0cd5d87"),
}
CORRECTED_CHECK = "python3 discovery/run_cycle_4_p1r_crr_finite_probe_v3.py --check"
CORRECTED_WRITE = "python3 discovery/run_cycle_4_p1r_crr_finite_probe_v3.py --write"
EXPECTED_STATUS_COUNTS = {"NO_RETAINED_HIT": 160}
EXPECTED_RESOURCES = {
    "wall_seconds": 713.8161791041493,
    "peak_rss_bytes": 564809728,
    "cap_seconds": 3300,
    "cap_rss_bytes": 1073741824,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def triple(values: list[float]) -> dict[str, float]:
    return {"min": min(values), "median": statistics.median(values), "max": max(values)}


def binary64_screen_census(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {"large_value": 0, "energy_lower": 0, "energy_upper": 0, "rational_measure": 0, "quadrature_agreement": 0, "cubic_positive_and_size": 0, "cubic_agreement": 0}
    lv_ratios: list[float] = []
    mu_ratios: list[float] = []
    quadrature_ratios: list[float] = []
    for row in rows:
        n = row["N"]
        values = row["binary64"]
        margin = 1.05
        lv_cut = margin * 0.75 * n**0.7
        low, high = margin * 0.25 * n * n, 4 * n * n / margin
        mu_cut = margin * 0.2 * n**(-0.4)
        agreement_allowance = 0.01 * max(float(values["mu32"]), 0.2 * n**(-0.4))
        lv_ratio = float(values["min_abs_D"]) / lv_cut
        mu_ratio = float(values["mu32"]) / mu_cut
        quadrature_ratio = abs(float(values["mu16"]) - float(values["mu32"])) / agreement_allowance
        lv_ratios.append(lv_ratio)
        mu_ratios.append(mu_ratio)
        quadrature_ratios.append(quadrature_ratio)
        counts["large_value"] += lv_ratio >= 1
        counts["energy_lower"] += int(values["energy_exact"]) >= low
        counts["energy_upper"] += int(values["energy_exact"]) <= high
        counts["rational_measure"] += mu_ratio >= 1
        counts["quadrature_agreement"] += quadrature_ratio <= 1
        recognized = row["recognized_cubic"]["dual_precision"]["384"]
        c8, c12 = float(recognized["C8"]), float(recognized["C12"])
        cubic_cut = margin * 0.05 * n**3.6
        cubic_allowance = 0.05 * max(abs(c12), 0.05 * n**3.6)
        counts["cubic_positive_and_size"] += c8 > 0 and c12 > 0 and c12 >= cubic_cut
        counts["cubic_agreement"] += abs(c8 - c12) <= cubic_allowance
    return {"classification": "OBSERVED/EXPLORATORY binary64 screen census, except cubic rows additionally have recorded RECOGNIZED 256/384 diagnostics", "pass_counts": counts, "ratios": {"large_value_to_cut": triple(lv_ratios), "rational_measure_to_cut": triple(mu_ratios), "quadrature_disagreement_to_allowed": triple(quadrature_ratios)}}


def seal() -> dict[str, Any]:
    pins: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing input: {label}")
        actual = sha256(path)
        require(actual == expected, f"immutable input hash mismatch: {label}")
        pins[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    result = json.loads(INPUTS["immutable_v3_result"][0].read_text(encoding="utf-8"))
    semantic = json.loads(INPUTS["semantic_replay"][0].read_text(encoding="utf-8"))
    require(result["artifact_id"] == "cycle-4-p1r-crr-finite-probe-v3", "v3 result identity mismatch")
    require(result["runner"]["path"] == "discovery/run_cycle_4_p1r_crr_finite_probe_v3.py", "v3 result runner path mismatch")
    require(result["runner"]["sha256"] == INPUTS["immutable_v3_runner"][1], "v3 result runner hash mismatch")
    require(result["replay"] == {
        "check_command": "python3 discovery/run_cycle_4_p1r_crr_finite_probe_v2.py --check",
        "execution_command": "python3 discovery/run_cycle_4_p1r_crr_finite_probe_v2.py --write",
        "no_resume": True,
    }, "expected inherited v2 replay metadata is absent")
    rows = result["rows"]
    require(len(rows) == 160 and len({row["id"] for row in rows}) == 160, "v3 retained-row invariant changed")
    require(result["status_counts"] == EXPECTED_STATUS_COUNTS, "v3 status-count invariant changed")
    require(result["resources"] == EXPECTED_RESOURCES, "v3 resource invariant changed")
    require(semantic["status"] == "SEMANTIC_REPLAY_MATCH", "semantic replay did not match immutable result")
    require(semantic["immutable_inputs"]["result"]["sha256"] == INPUTS["immutable_v3_result"][1], "semantic replay result pin mismatch")
    census = binary64_screen_census(rows)
    require(census["pass_counts"] == {"large_value": 0, "energy_lower": 160, "energy_upper": 147, "rational_measure": 13, "quadrature_agreement": 10, "cubic_positive_and_size": 160, "cubic_agreement": 0}, "binary64 screen census mismatch")
    return {
        "artifact_id": "cycle-4-p1r-crr-finite-probe-v3-replay-metadata-correction-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Metadata correction only. It does not edit or rerun v3, alter any row, seed, candidate, numerical value, status, resource observation, or mathematical claim.",
        "status": "SEALED_METADATA_CORRECTION",
        "correction": {
            "field": "replay.check_command and replay.execution_command",
            "incorrect_values": result["replay"],
            "corrected_values": {"check_command": CORRECTED_CHECK, "execution_command": CORRECTED_WRITE, "no_resume": True},
            "cause": "v3 wrapper corrected the runner path/hash but inherited literal replay strings from the v2 base payload",
            "write_command_interpretation": "historical-only; immutable result exists and the v3 runner refuses overwrite",
        },
        "immutable_inputs": pins,
        "invariants_verified": {"row_count": len(rows), "unique_row_ids": len({row["id"] for row in rows}), "status_counts": result["status_counts"], "resources": result["resources"], "runner": result["runner"]},
        "semantic_replay": {"status": semantic["status"], "comparison": semantic["comparison"], "resources": semantic["replay_resources"]},
        "post_result_screen_census": census,
        "research_stage_review_policy": {"hostile_audit": "NOT_INITIATED; metadata-only lightweight correction", "search_rerun": "PROHIBITED_BY_CORRECTION_SCOPE"},
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "replay": {"check_command": "python3 discovery/build_cycle_4_p1r_crr_finite_probe_v3_replay_metadata_correction_v1.py --check", "write_command": "python3 discovery/build_cycle_4_p1r_crr_finite_probe_v3_replay_metadata_correction_v1.py --write", "corrected_result_check_command": CORRECTED_CHECK},
    }


def render(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = seal()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite metadata correction")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file() and OUTPUT.read_bytes() == render(payload), "metadata correction byte mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"], "rows": payload["invariants_verified"]["row_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
