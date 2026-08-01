#!/usr/bin/env python3
"""Post-correction hostile re-audit of G1 exact structural atlas v2."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from proof.audit_g1_exact_structural_atlas_hostile_v1 import audit_local_rows, audit_transfer_rows


OUTPUT = ROOT / "artifacts/g1-exact-structural-atlas-v2-hostile-audit-v1.json"
ATLAS = ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v2.json"
PREREG = ROOT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json"
SCRIPT = ROOT / "discovery/run_g1_exact_structural_atlas_v2.py"
CONVENTIONS = ROOT / "conventions/g1_atlas_v1.py"
FROZEN = {
    "atlas": (ATLAS, "fd66d17664ca921795617c6bfca76c3be49246ea9351644848a2aadf9e680b08"),
    "preregistration": (PREREG, "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8"),
    "script": (SCRIPT, "e082b998a15ee0a595f58a53f568050e97934d245f448d8c030fa4feaedcb3c8"),
    "corrected_conventions": (CONVENTIONS, "642a61fc03e5de6c7f7df5338e88da552ef1c72a7b7d7897898fb23740106ca5"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(command: list[str], wanted: int, label: str) -> None:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    require(completed.returncode == wanted, label + ": " + json.dumps({"returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}, sort_keys=True))


def certificate() -> dict[str, Any]:
    require(sys.flags.optimize == 0, "G1 v2 hostile audit forbids -O/-OO")
    hashes = {}
    for label, (path, expected) in FROZEN.items():
        actual = digest(path)
        require(actual == expected, "frozen hash mismatch: " + str(path))
        hashes[label] = actual
    atlas, prereg = json.loads(ATLAS.read_text()), json.loads(PREREG.read_text())
    require(atlas["epistemic_status"] == "PROVED", "v2 status is not PROVED")
    require(atlas["scope"] == {"finite_complex_probes_evaluated": 0, "screen_rows_evaluated": 0, "local_rows": 7744, "transfer_rows": 560}, "v2 scope changed")
    audit_local_rows(atlas["local_rows"])
    audit_transfer_rows(atlas["transfer_rows"], prereg)
    inputs = atlas["frozen_inputs"]
    require(inputs["hashes"]["frozen_conventions"] == hashes["corrected_conventions"], "v2 does not pin corrected conventions")
    correction = inputs["convention_runtime_correction"]
    require(correction["old_sha256"] == "3d3cef60c32dff2a2e4cbd3c10b229464d74aadbbaef53ba1fccc7158b78d726", "old convention identity missing")
    require(correction["new_sha256"] == hashes["corrected_conventions"], "new convention identity mismatch")
    require(correction["checked"] == {"local_rows": 7744, "primary_spine_rows": 42, "registered_pairs": 14, "screen_scale_U": 4096, "validation_scales_U": [32768, 262144], "precisions_bits": [256, 384]}, "convention semantic correction scope changed")
    require(inputs["runtime"] == {"implementation": "CPython", "python": "3.12.3", "mpmath": "1.2.1", "optimization": 0}, "v2 runtime preflight was not recorded")
    checked([sys.executable, str(SCRIPT), "--check"], 0, "normal v2 replay failed")
    checked([sys.executable, "-O", str(SCRIPT), "--check"], 1, "v2 optimized replay does not fail closed")
    return {
        "artifact_id": "g1-exact-structural-atlas-v2-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED post-correction hostile audit. It independently recomputes all v2 rational row data and checks the corrected source/document/runtime/convention boundary. It proves no new analytic theorem and is not a G1 route decision.",
        "frozen_hashes": hashes,
        "exact_recomputation": {"status": "PASS", "epistemic_status": "PROVED", "local_rows": 7744, "transfer_rows": 560, "energy_diagonal_rows": 704},
        "hardening": {"status": "PASS", "epistemic_status": "OBSERVED", "normal_replay": "exit status 0", "optimized_replay": "exit status 1", "direct_source_document_runtime_convention_pins": "PASS", "convention_correction": "old-to-new identity and full frozen semantic comparison present"},
        "decision": {"status": "V2_AUTHORITY_REPLAYED", "epistemic_status": "OBSERVED", "v1": "Preserved historical artifact and hostile finding; not overwritten.", "v2": "May serve as the exact structural G1 authority within its stated conditional claim boundary."},
        "falsifier": "Any frozen-hash, source/document/runtime/convention-correction, exact row/residual/tie/anchor, or execution-mode mismatch invalidates this re-audit and requires a new versioned record.",
        "replay": {"script_sha256": digest(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_exact_structural_atlas_v2_hostile_v1.py --write", "check_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_exact_structural_atlas_v2_hostile_v1.py --check"},
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(certificate())
    if args.write:
        OUTPUT.write_text(payload)
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "G1 v2 hostile audit mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "status": "V2_AUTHORITY_REPLAYED", "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
