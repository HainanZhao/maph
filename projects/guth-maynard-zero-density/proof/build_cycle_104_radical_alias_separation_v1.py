#!/usr/bin/env python3
"""Seal Cycle 104 single-radical alias separation."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-104-radical-alias-separation-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-104-radical-alias-candidate-v1.md", "31e3ecfaaec48261d9bc322709fdb0eb64d8c347e9a20fe8cf3d54a2675ab325"),
    "preregistration": (ROOT / "docs/cycle-104-radical-alias-preregistration-v1.md", "f9f6477a9665159ca34f88774a3eb11b8bc489d40f16d1a5f9f19a2303e929c0"),
    "document": (ROOT / "docs/cycle-104-radical-alias-separation-v1.md", "36492a449f1bfb10364a854a4007787e55029c857a1639dbced9195eff8ca8e5"),
    "conventions": (ROOT / "conventions/radical_alias_separation_v1.py", "01edb5f8bfb89f15e3a710dc396750faed0c7444bad9c3e3f54a75750eb33b47"),
    "tests": (ROOT / "tests/test_cycle_104_radical_alias_separation_v1.py", "d0a2ff8b88e35a9a13742ec606ecb076e0ae7d4f21488ceef82e519d851f9642"),
    "cycle103": (ROOT / "artifacts/cycle-103-critical-scale-alias-v1.json", "93514b9668c49beec4a11d3892af1ae6d4f0b80125bd927edb9f378c8eba5e15"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 104 runtime mismatch")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def load_theorem() -> dict[str, object]:
    path = INPUTS["conventions"][0]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location("radical_alias_separation_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 104 conventions")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.theorem_record()
    require("(d*R2/y)" in record["single_radical"], "radical collapse")
    require("perfect dth powers" in record["rational_classification"], "rational classification")
    require("2epsilon" in record["closure"], "separation closure")
    return record


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle103"][0].read_text(encoding="utf-8"))
    require(
        prior.get("status") == "SEALED_CRITICAL_SCALE_ONE_HIT_OR_SHORT_ALGEBRAIC_ALIAS",
        "Cycle 103 status mismatch",
    )
    return {"cycle103_role": "supply K and the one-hit-or-short-alias inverse"}


def seal() -> dict[str, Any]:
    theorem = load_theorem()
    return {
        "artifact_id": "cycle-104-radical-alias-separation-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SINGLE_RADICAL_RATIONAL_CLASSIFICATION_AND_NORM_SECTOR",
        "claim_boundary": (
            "This artifact proves the radical collapse, exact rational-alias "
            "classification, and an elementary norm-separated one-scale sector. It "
            "proves no closure for all radical degrees, aggregate exceptional-web "
            "bound, weak/simple-root estimate, complete moment, density, or interval gain."
        ),
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "radical_alias_theorem": {"epistemic_status": "PROVED", **theorem},
        "closed_sector": {
            "epistemic_status": "PROVED",
            "statement": (
                "an irrational core with 2epsilon below the rational safe norm bound "
                "has no q<=Lambda alias and at most one surviving coefficient scale"
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "aggregate large-degree and perfect-power radical cores with actual phases",
        },
        "containment": {
            "epistemic_status": "OBSERVED",
            "statement": (
                "three initial fixture expectations were corrected; the nontrivial "
                "9/4 square label confirms the predicted perfect-power class"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_104_radical_alias_separation_v1.py --write",
            "check_command": "python3 proof/build_cycle_104_radical_alias_separation_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_104_radical_alias_separation_v1.py",
        },
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = seal()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 104 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 104 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 104 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
