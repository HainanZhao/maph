#!/usr/bin/env python3
"""Certified anti-unit orbit isolation for three e=6 fields."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

from flint import acb, ctx, fmpz_poly


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CONFIG = ROOT / "data/engine-c-e6-tranche-01-unit-orbits-v1.json"
THETA_CONFIG = ROOT / "data/engine-c-e6-tranche-01-theta-v1.json"
ORBIT_MODULE = ROOT / "scripts/certify_engine_c_unit_orbits.py"
LATTICE_SOURCE = ROOT / "scripts/export_engine_c_unit_lattice.gp"
OUTPUT = ROOT / "artifacts/engine-c-e6-tranche-01-unit-orbits-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-c-e6-tranche-01-unit-orbits-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_orbit():
    spec = importlib.util.spec_from_file_location("generic_orbit", ORBIT_MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError("orbit module import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    orbit = load_orbit()
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    theta_config = json.loads(THETA_CONFIG.read_text(encoding="utf-8"))
    theta_records = {
        (row["case_id"], row["route_id"]): row
        for row in theta_config["records"]
    }
    theta_source = orbit.theta.GP_SOURCE.read_text(encoding="utf-8")
    lattice_source = LATTICE_SOURCE.read_text(encoding="utf-8")
    ctx.dps = config["working_digits"]
    num, den = config["isolation_radius"].split("/")
    radius = Fraction(int(num), int(den))
    bound = config["coordinate_search_bound"]
    records = []
    transcripts = []

    for record in config["records"]:
        key = (record["case_id"], record["route_id"])
        completed = subprocess.run(
            ["gp", "-q"],
            input=(
                "CHARACTER_FIELD_POLYNOMIAL="
                f"{record['character_field_polynomial']};\n"
                + lattice_source
            ),
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=600,
            check=False,
        )
        if (
            completed.returncode != 0
            or "EXACT_ANTI_UNIT_LATTICE_EXPORT_COMPLETE=1"
            not in completed.stdout
        ):
            raise RuntimeError(completed.stdout + completed.stderr)
        text = completed.stdout
        if int(orbit.scalar(text, "CHARACTER_FIELD_BNFCERTIFY")) != 1:
            raise RuntimeError(f"{key}: bnfcertify failed")
        e = int(orbit.scalar(text, "CHARACTER_FIELD_ROOTS_OF_UNITY"))
        if e != record["expected_roots_of_unity"]:
            raise RuntimeError(f"{key}: e changed")
        polynomial_q = orbit.parse_polynomial(text, "CHARACTER_FIELD")
        if any(value.denominator != 1 for value in polynomial_q):
            raise RuntimeError(f"{key}: nonintegral polynomial")
        polynomial = fmpz_poly([int(value) for value in polynomial_q])
        sigma = orbit.parse_polynomial(text, "C4_SIGMA")
        units = [
            orbit.parse_polynomial(text, "ANTI_UNIT_1"),
            orbit.parse_polynomial(text, "ANTI_UNIT_2"),
        ]
        action = [
            [
                int(orbit.scalar(text, "ANTI_ACTION_11")),
                int(orbit.scalar(text, "ANTI_ACTION_12")),
            ],
            [
                int(orbit.scalar(text, "ANTI_ACTION_21")),
                int(orbit.scalar(text, "ANTI_ACTION_22")),
            ],
        ]
        primitive = orbit.live_theta_target(
            theta_records[key], theta_config, theta_source
        )
        target = primitive * e / 4
        roots = [
            root
            for root, multiplicity in polynomial.complex_roots()
            if multiplicity == 1 and root.imag > 0
        ]
        if len(roots) != 4:
            raise RuntimeError(f"{key}: upper-root count changed")
        isolated: set[tuple[int, int]] = set()
        per_root = []
        for root_index, root in enumerate(roots):
            sigma_root = orbit.evaluate(sigma, root)
            matrix = [
                [abs(orbit.evaluate(unit, root)).log() for unit in units],
                [
                    abs(orbit.evaluate(unit, sigma_root)).log()
                    for unit in units
                ],
            ]
            matches = []
            for transform, transformed in orbit.transformed_targets(primitive):
                # transformed_targets operates on L'; apply e/4 after
                # transforming so every component remains an Arb ball.
                scaled = (
                    transformed[0] * e / 4,
                    transformed[1] * e / 4,
                )
                coordinates = orbit.solve(matrix, scaled)
                nearby = [
                    (first, second)
                    for first in range(-bound, bound + 1)
                    for second in range(-bound, bound + 1)
                    if orbit.near_integer(coordinates[0], first, radius)
                    and orbit.near_integer(coordinates[1], second, radius)
                ]
                for candidate in nearby:
                    isolated.add(candidate)
                    matches.append(
                        {
                            "transform": transform,
                            "coordinates": list(candidate),
                            "coordinate_balls": [
                                str(coordinates[0]),
                                str(coordinates[1]),
                            ],
                        }
                    )
            if not matches:
                raise RuntimeError(f"{key}: root {root_index} has no match")
            per_root.append(
                {"root_index": root_index, "matches": matches}
            )
        seed = min(isolated)
        exact_orbit = orbit.orbit(seed, action)
        if isolated != exact_orbit or len(exact_orbit) != 4:
            raise RuntimeError(f"{key}: not one exact C4 orbit: {isolated}")
        records.append(
            {
                **record,
                "character_field_class_number": int(
                    orbit.scalar(text, "CHARACTER_FIELD_CLASS_NUMBER")
                ),
                "anti_action": action,
                "primitive_lprime_ball": str(primitive),
                "direct_lprime_to_class_log_coefficient": f"{e}/4",
                "isolated_integral_orbit": [
                    list(item) for item in sorted(isolated)
                ],
                "per_root_isolation": per_root,
            }
        )
        transcripts.append(
            f"===== {record['case_id']} {record['route_id']} =====\n{text}"
        )
    TRANSCRIPT.write_text("\n".join(transcripts), encoding="utf-8")
    payload = {
        "schema": "effective-stark-engine-c-e6-tranche-01-unit-orbits-v1",
        "claim_tag": "ENCLOSED_UNIQUE_INTEGRAL_UNIT_ORBITS",
        "field_count": 3,
        "route_count": 6,
        "records": records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                CONFIG,
                THETA_CONFIG,
                ORBIT_MODULE,
                LATTICE_SOURCE,
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
    print("E6_UNIT_ORBITS_ENCLOSED=1")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
