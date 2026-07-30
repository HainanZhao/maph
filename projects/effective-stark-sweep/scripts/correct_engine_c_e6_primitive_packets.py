#!/usr/bin/env python3
"""Correct the e=6 bridge from powered Stark units to primitive packets.

The banked analytic inversion isolates the Stark unit epsilon in the
torsion-free unit lattice.  For e=6 the Fourier-to-norm formula uses
u with epsilon=u^(e/2)=u^3.  The earlier bridge took norms of epsilon
itself.  This replay divides the exact lattice coordinates by three
before taking CM norms and requires the two independent routes to give
the same Artin-labeled polynomial.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CONFIG = ROOT / "data/engine-c-e6-tranche-01-packet-bridge-v1.json"
POWERED_ORBITS = (
    ROOT / "artifacts/engine-c-e6-tranche-01-unit-orbits-v1.json"
)
GENERIC_RUNNER = ROOT / "scripts/run_engine_c_packet_bridge.py"
GP_SOURCE = ROOT / "scripts/generic_engine_c_packet_bridge.gp"
OUT = ROOT / "artifacts/engine-c-e6-primitive-packet-correction-v1.json"
TRANSCRIPT = (
    ROOT / "artifacts/engine-c-e6-primitive-packet-correction-v1.transcript"
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_generic():
    spec = importlib.util.spec_from_file_location("bridge", GENERIC_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import generic packet bridge")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sturm_counts(polynomial: str) -> dict[str, int]:
    source = (
        f"Q={polynomial};"
        'print("REAL=",polsturm(Q));'
        'print("POSITIVE=",polsturm(Q,0));'
        'print("NEGATIVE=",polsturm(Q,-oo,0));'
    )
    completed = subprocess.run(
        ["gp", "-q"],
        input=source,
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stdout + completed.stderr)
    result = {}
    for line in completed.stdout.splitlines():
        key, value = line.split("=", 1)
        result[key.lower()] = int(value)
    return result


def main() -> None:
    config = json.loads(CONFIG.read_text())
    powered = json.loads(POWERED_ORBITS.read_text())
    certified = {
        (row["case_id"], row["route_id"]): {
            tuple(value) for value in row["isolated_integral_orbit"]
        }
        for row in powered["records"]
    }
    generic = load_generic()
    gp_source = GP_SOURCE.read_text()
    records = []
    transcripts = []
    by_case: dict[str, set[str]] = {}

    for row in config["records"]:
        key = (row["case_id"], row["route_id"])
        powered_coordinates = tuple(
            int(value)
            for value in row["candidate_coordinates"].strip("[]").split(",")
        )
        if powered_coordinates not in certified[key]:
            raise RuntimeError(f"{key}: powered coordinate is not certified")
        if any(value % 3 for value in powered_coordinates):
            raise RuntimeError(f"{key}: Stark unit is not a cube in free lattice")
        primitive = tuple(value // 3 for value in powered_coordinates)
        prelude = "\n".join(
            [
                f'CASE_ID="{row["case_id"]}-PRIMITIVE";',
                f'ROUTE_ID="{row["route_id"]}";',
                "CHARACTER_FIELD_POLYNOMIAL="
                f'{row["character_field_polynomial"]};',
                "REAL_SELECTOR_FIELD_POLYNOMIAL="
                f'{row["real_selector_field_polynomial"]};',
                f"CANDIDATE_COORDINATES=[{primitive[0]},{primitive[1]}];",
                f'SEPARATOR_PRIME={row["separator_prime"]};',
            ]
        )
        completed = subprocess.run(
            ["gp", "-q"],
            input=prelude + "\n" + gp_source,
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=600,
            check=False,
        )
        if (
            completed.returncode
            or "GENERIC_ENGINE_C_PACKET_BRIDGE_VERIFIED=1"
            not in completed.stdout
        ):
            raise RuntimeError(
                f"{key} failed:\n{completed.stdout}\n{completed.stderr}"
            )
        polynomial = generic.scalar(
            completed.stdout, "ARTIN_LABELED_PACKET_POLYNOMIAL"
        )
        counts = sturm_counts(polynomial)
        if counts != {"real": 4, "positive": 4, "negative": 0}:
            raise RuntimeError(f"{key}: unexpected real-root counts {counts}")
        by_case.setdefault(row["case_id"], set()).add(polynomial)
        records.append(
            {
                "case_id": row["case_id"],
                "route_id": row["route_id"],
                "e": 6,
                "powered_stark_coordinates": list(powered_coordinates),
                "primitive_coordinates": list(primitive),
                "artin_labeled_primitive_packet_polynomial": polynomial,
                "exact_sturm_counts": counts,
            }
        )
        transcripts.append(
            f"===== {row['case_id']} {row['route_id']} =====\n"
            + completed.stdout
        )

    if any(len(polynomials) != 1 for polynomials in by_case.values()):
        raise RuntimeError("two-route primitive packet disagreement")
    TRANSCRIPT.write_text("\n".join(transcripts))
    payload = {
        "schema": "effective-stark-engine-c-e6-primitive-correction-v1",
        "claim_tag": "VERIFIED_EXACT_PRIMITIVE_PACKET_CORRECTION",
        "correction": (
            "The former bridge took CM norms of epsilon.  The primitive "
            "one-place packet uses u with epsilon=u^3; exact lattice "
            "coordinates are divided by three before the CM norm."
        ),
        "case_polynomials": {
            case_id: next(iter(polynomials))
            for case_id, polynomials in sorted(by_case.items())
        },
        "records": records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                CONFIG,
                POWERED_ORBITS,
                GENERIC_RUNNER,
                GP_SOURCE,
                SELF,
            )
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha(TRANSCRIPT),
        },
        "verdict": "VERIFIED",
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("E6_PRIMITIVE_CASE_COUNT=3")
    print("E6_PRIMITIVE_ROUTE_COUNT=6")
    print("E6_PRIMITIVE_PACKET_CORRECTION=VERIFIED")


if __name__ == "__main__":
    main()
