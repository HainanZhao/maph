#!/usr/bin/env python3
"""Replay the shared exact Engine-A packet construction for exploratory D12.

The D12 candidate was selected post hoc from discovery, so this artifact is
explicitly exploratory.  It certifies no AFK bridge and no TCC identity.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
EFFECTIVE = ROOT.parents[0] / "effective-stark-sweep"
SOURCE = EFFECTIVE / "scripts" / "certify_census_q_packet.gp"
OUTPUT = ROOT / "discovery" / "tcc-sweep-d12-engine-a-packet-exploratory-v1.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    started = time.monotonic()
    prelude = 'CASE_ID="TCC-D12";\nD_VALUE=13;\nH11=12;H12=0;H21=0;H22=12;\n'
    completed = subprocess.run(
        ["gp", "-q"], input=prelude + SOURCE.read_text(), text=True,
        cwd=EFFECTIVE, check=True, capture_output=True,
    )
    values: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    required = {
        "PACKET_POLYNOMIAL_SYNTHESIS": "PASS",
        "RAY_CYC": "[2, 2, 2]",
        "SIGN_LOG": "[0, 1, 1]",
        "COMMON_DENOMINATOR": "1",
        "PACKET_FACTOR_DEGREE": "4",
        "PACKET_FACTOR_IRREDUCIBLE_OVER_K": "1",
        "PACKET_FACTOR_POSITIVE_ROOT_SIGN_PATTERN": "1",
    }
    if any(values.get(key) != value for key, value in required.items()):
        raise RuntimeError({key: values.get(key) for key in required})
    payload = {
        "schema": "tcc-sweep-d12-engine-a-packet-exploratory-v1",
        "claim_tag": "EXPLORATORY",
        "claim_boundary": "Exact Engine-A packet construction only; no AFK characteristic-to-ray bridge, multiplier comparison, signed reconstruction, or TCC conclusion.",
        "candidate": {"d": 12, "r": 1, "field": "Q(sqrt(13))", "form_conductor": 1, "modulus": "(12) infinity_2"},
        "exact_engine_a_output": {key: values[key] for key in set(required) | {"SUPPORTED_CHARACTERS", "EFFECTIVE_CHARACTERS", "CHARACTER_RECORDS", "POWERED_EXPONENTS", "POWERED_TRACES", "PACKET_FACTOR_OVER_K", "ABSOLUTE_PACKET_RESULTANT", "COEFFICIENT_COORDINATE_DECIMAL_DIGITS"}},
        "replay": {"command": "python3 discovery/certify_tcc_sweep_d12_engine_a_exploratory.py", "pari_version": values.get("PARI_VERSION"), "wall_seconds": time.monotonic() - started},
        "source_hashes": {str(path): digest(path) for path in (Path(__file__), SOURCE, EFFECTIVE / "scripts" / "census_packet_conventions.gp")},
        "gp_stderr": completed.stderr,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("TCC_SWEEP_D12_ENGINE_A_EXPLORATORY=PASS")


if __name__ == "__main__":
    main()
