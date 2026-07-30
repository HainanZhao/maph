#!/usr/bin/env python3
"""Certified L'(0) balls for the first three e=6 Engine-C fields."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from flint import acb, arb, ctx


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CONFIG = ROOT / "data/engine-c-e6-tranche-01-theta-v1.json"
SELECTION = ROOT / "artifacts/engine-c-e6-tranche-01-selection-v1.json"
THETA_MODULE = ROOT / "scripts/certify_engine_c_theta_targets.py"
GP_SOURCE = ROOT / "scripts/export_engine_c_lfunction_coefficients.gp"
OUTPUT = ROOT / "artifacts/engine-c-e6-tranche-01-theta-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-c-e6-tranche-01-theta-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_theta():
    spec = importlib.util.spec_from_file_location("generic_theta", THETA_MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError("theta module import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def live_ball(theta, conductor: int, coefficients: list[tuple[int, int]]) -> acb:
    qscale = arb(conductor).sqrt() / (2 * arb.pi())
    c = 1 / qscale
    q = (-c).exp()
    theta_one = acb(0)
    i0 = acb(0)
    i1 = acb(0)
    for n, (real, imag) in enumerate(coefficients, start=1):
        aa = acb(real, imag)
        z = arb(n) * c
        ez = (-z).exp()
        theta_one += aa * ez
        i0 += aa * acb(z).gamma_upper(0)
        i1 += aa.conjugate() * qscale / arb(n) * ez
    limit = len(coefficients)
    theta_tail = q ** (limit + 1) * (
        arb(limit + 1) - arb(limit) * q
    ) / (1 - q) ** 2
    integral_tail = qscale * q ** (limit + 1) / (1 - q)
    theta_one += theta.complex_error(theta_tail)
    i0 += theta.complex_error(integral_tail)
    i1 += theta.complex_error(integral_tail)
    return i0 + theta_one / theta_one.conjugate() * i1


def overlaps(left: acb, right: acb) -> bool:
    return left.real.overlaps(right.real) and left.imag.overlaps(right.imag)


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    selected = {
        (row["case_id"], row["route_id"]): row["selected_cm_character"]
        for row in selection["records"]
    }
    theta = load_theta()
    source = GP_SOURCE.read_text(encoding="utf-8")
    ctx.dps = config["working_digits"]
    records = []
    transcripts = []
    live: dict[tuple[str, str], acb] = {}
    for record in config["records"]:
        key = (record["case_id"], record["route_id"])
        if "".join(selected[key].split()) != "".join(
            record["selected_cm_character"].split()
        ):
            raise RuntimeError(f"{key}: character mismatch")
        conductor, coefficients, transcript = theta.run_gp(
            record, config["coefficient_limit"], source
        )
        if conductor != record["expected_analytic_conductor"]:
            raise RuntimeError(f"{key}: conductor mismatch")
        records.append({**record, **theta.evaluate(conductor, coefficients)})
        live[key] = live_ball(theta, conductor, coefficients)
        transcripts.append(
            f"===== {record['case_id']} {record['route_id']} =====\n"
            f"{transcript}"
        )
    cases = sorted({row["case_id"] for row in config["records"]})
    for case_id in cases:
        routes = [
            live[(row["case_id"], row["route_id"])]
            for row in config["records"]
            if row["case_id"] == case_id
        ]
        if len(routes) != 2 or not overlaps(routes[0], routes[1]):
            raise RuntimeError(f"{case_id}: two-route target mismatch")
    TRANSCRIPT.write_text("\n".join(transcripts), encoding="utf-8")
    payload = {
        "schema": "effective-stark-engine-c-e6-tranche-01-theta-v1",
        "claim_tag": "ENCLOSED_PRIMITIVE_LPRIME_TARGETS",
        "field_count": 3,
        "route_count": 6,
        "all_two_route_targets_overlap": True,
        "coefficient_limit": config["coefficient_limit"],
        "working_digits": config["working_digits"],
        "records": records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                CONFIG,
                SELECTION,
                THETA_MODULE,
                GP_SOURCE,
                SELF,
            )
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha(TRANSCRIPT),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("FIELD_COUNT=3")
    print("ROUTE_COUNT=6")
    print("ALL_TWO_ROUTE_TARGETS_OVERLAP=1")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
