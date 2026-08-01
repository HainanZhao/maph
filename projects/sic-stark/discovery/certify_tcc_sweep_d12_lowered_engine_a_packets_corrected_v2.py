#!/usr/bin/env python3
"""Corrected Engine-A packets for all D12 fixed-point lowering moduli."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
EFFECTIVE = ROOT.parents[0] / "effective-stark-sweep"
SOURCE = EFFECTIVE / "scripts" / "certify_census_q_packet.gp"
LOWERING = ROOT / "discovery" / "tcc-sweep-d12-conductor-lowering-corrected-v2.json"
OUTPUT = ROOT / "discovery" / "tcc-sweep-d12-lowered-engine-a-packets-corrected-v2.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def parse(output: str) -> dict[str, str]:
    return {key: value for line in output.splitlines() if "=" in line for key, value in [line.split("=", 1)]}


def main() -> None:
    started = time.monotonic()
    lowering = json.loads(LOWERING.read_text())
    moduli = sorted({tuple(row["reduced_finite_modulus_hnf"]) for row in lowering["records"]})
    source = SOURCE.read_text()
    rows = []
    for h11, h12, h21, h22 in moduli:
        prelude = f'CASE_ID="TCC-D12-corrected-{h11}-{h12}-{h22}";\nD_VALUE=13;\nH11={h11};H12={h12};H21={h21};H22={h22};\n'
        run = subprocess.run(["gp", "-q"], input=prelude + source, text=True,
                             cwd=EFFECTIVE, capture_output=True, check=True)
        values = parse(run.stdout)
        if values.get("PACKET_POLYNOMIAL_SYNTHESIS") != "PASS":
            raise AssertionError((h11, h12, h21, h22, values))
        rows.append({"reduced_finite_modulus_hnf": [h11, h12, h21, h22],
                     "finite_modulus_norm": h11*h22-h12*h21,
                     "ray_cyc": values["RAY_CYC"], "sign_log": values["SIGN_LOG"],
                     "supported_characters": values["SUPPORTED_CHARACTERS"],
                     "effective_characters": values["EFFECTIVE_CHARACTERS"],
                     "character_records": values["CHARACTER_RECORDS"],
                     "packet_factor_over_K": values["PACKET_FACTOR_OVER_K"],
                     "packet_factor_degree": values["PACKET_FACTOR_DEGREE"],
                     "absolute_packet_resultant": values["ABSOLUTE_PACKET_RESULTANT"],
                     "gp_stderr": run.stderr})
    if len(rows) != 11:
        raise AssertionError(len(rows))
    payload = {"schema": "tcc-sweep-d12-lowered-engine-a-packets-corrected-v2",
               "claim_tag": "EXPLORATORY",
               "claim_boundary": "Exact Engine-A packet synthesis only for the correctly lowered D12 maximal-order moduli; no AFK sign/reconstruction/minor/TCC claim.",
               "correction_of": "tcc-sweep-d12-lowered-engine-a-packets-v1.json",
               "lowering_predecessor": str(LOWERING.relative_to(ROOT)), "rows": rows,
               "replay": {"command": "python3 discovery/certify_tcc_sweep_d12_lowered_engine_a_packets_corrected_v2.py", "wall_seconds": time.monotonic()-started},
               "source_hashes": {"wrapper": digest(Path(__file__)), "engine_a": digest(SOURCE), "lowering_ledger": digest(LOWERING)}}
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print("TCC_SWEEP_D12_LOWERED_ENGINE_A_PACKETS_CORRECTED_V2=PASS")


if __name__ == "__main__":
    main()
