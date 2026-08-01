#!/usr/bin/env python3
"""Hostile audit of the preserved, pre-correction G1 finite-probe engine v1.

This audit deliberately targets only the v1 executable.  It never evaluates a
finite complex G1 row, mutates the executable, or writes a discovery result.
The synthetic calls below expose control-flow semantics with all finite-row
evaluation replaced by tiny deterministic stand-ins.
"""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from discovery import run_g1_atlas_v1 as engine


OUTPUT = ROOT / "artifacts/g1-probe-engine-hostile-audit-v1.json"
ENGINE = ROOT / "discovery/run_g1_atlas_v1.py"
CONVENTIONS = ROOT / "conventions/g1_atlas_v1.py"
PREREG = ROOT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json"
EXPECTED = {
    "engine_v1": "78f5088cbe615237d565854428511cda03e22fc04838d192c64d3215748c28ee",
    "conventions": "642a61fc03e5de6c7f7df5338e88da552ef1c72a7b7d7897898fb23740106ca5",
    "preregistration": "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def synthetic_row(spec: dict[str, Any], U: int = engine.SCREEN_SCALE, **_kwargs: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    """A no-complex-evaluation row whose validation score is intentionally worse."""
    is_screen = U == engine.SCREEN_SCALE
    row = {
        "row_id": spec["row_id"],
        "screen_index": spec["screen_index"],
        "status": "COMPLETED",
        "family": {
            "coefficient": spec["coefficient"],
            "set": spec["set"],
            "declared_energy_regime": engine.energy_regime(spec["set"]),
        },
        "retention": {
            # Exactly one retained screen row creates two validation replays.
            "eligible": bool(is_screen and spec["screen_index"] == 0),
            "score": "0.0" if is_screen else "-1.0",
            "reason": "PENDING_GLOBAL_QUOTA",
        },
    }
    return row, {"wall_seconds": 0.0, "cpu_seconds": 0.0, "peak_rss_bytes": 0}


def audit() -> dict[str, Any]:
    require(sys.flags.optimize == 0, "hostile audit must run without -O/-OO")
    paths = {"engine_v1": ENGINE, "conventions": CONVENTIONS, "preregistration": PREREG}
    hashes = {label: digest(path) for label, path in paths.items()}
    for label, wanted in EXPECTED.items():
        require(hashes[label] == wanted, "v1 frozen hash mismatch: " + label)

    # v1's only use of platform identities is artifact reporting.  Patch the
    # reporter briefly: a fake version reaches a would-be discovery record
    # rather than stopping frozen_config/build_observations.
    frozen_config_source = inspect.getsource(engine.frozen_config)
    require("platform." not in frozen_config_source, "unexpected v1 runtime enforcement found")
    original_python_version = engine.platform.python_version
    try:
        engine.platform.python_version = lambda: "AUDIT-UNPINNED-RUNTIME"
        observation = engine.build_observations([], [], run_mode="HOSTILE_AUDIT_NO_FINITE_ROWS")
    finally:
        engine.platform.python_version = original_python_version
    require(observation["runtime"]["python"] == "AUDIT-UNPINNED-RUNTIME", "runtime reporter was not patched")

    # A retained screen row with two deliberately lower validation scores is
    # still emitted as COMPLETED: v1 has no loss criterion or failure code.
    original_run = engine.run_screen_row
    try:
        engine.run_screen_row = synthetic_row
        observations, _ = engine.compute_full()
    finally:
        engine.run_screen_row = original_run
    validation = observations["validation"]["rows"]
    require(observations["retained_screen_row_ids"] == ["G1-S000"], "synthetic retained row changed")
    require(len(validation) == 2, "synthetic validation count changed")
    require(all(row["status"] == "COMPLETED" for row in validation), "v1 unexpectedly detects validation score loss")
    require(all(row["retention"]["score"] == "-1.0" for row in validation), "synthetic lower validation score lost")

    # Any unexpected exception from one finite row escapes the loop.  It does
    # not become a retained failure row, so an interrupted full run produces
    # no complete observation artifact.
    def unexpected_exception(*_args: Any, **_kwargs: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        raise ValueError("HOSTILE_SYNTHETIC_UNCAUGHT_ROW_EXCEPTION")

    try:
        engine.run_screen_row = unexpected_exception
        escaped = False
        try:
            engine.compute_full()
        except ValueError as error:
            escaped = str(error) == "HOSTILE_SYNTHETIC_UNCAUGHT_ROW_EXCEPTION"
    finally:
        engine.run_screen_row = original_run
    require(escaped, "v1 unexpectedly contained a generic row exception")

    return {
        "artifact_id": "g1-probe-engine-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Hostile control-flow audit of the preserved finite discovery engine v1. It proves no analytic statement and evaluates no finite complex G1 row.",
        "frozen_hashes": hashes,
        "checks": [
            {
                "id": "RUNTIME_PIN_NOT_ENFORCED",
                "status": "FAIL",
                "epistemic_status": "OBSERVED",
                "evidence": "frozen_config has no platform identity guard; an injected runtime identity is serialized by build_observations without rejection.",
                "impact": "A v1 observation record is not confined to its preregistered CPython 3.12.3/mpmath 1.2.1 execution environment.",
            },
            {
                "id": "VALIDATION_SCORE_LOSS_NOT_ADJUDICATED",
                "status": "FAIL",
                "epistemic_status": "OBSERVED",
                "evidence": "A retained synthetic screen score 0.0 and both validation scores -1.0 are emitted as COMPLETED; no score-loss failure or comparison appears.",
                "impact": "The preregistered larger-scale score-loss falsifier is not mechanically retained/adjudicated by v1.",
            },
            {
                "id": "GENERIC_ROW_EXCEPTION_ABORTS_RUN",
                "status": "FAIL",
                "epistemic_status": "OBSERVED",
                "evidence": "A synthetic ValueError from run_screen_row escapes compute_full rather than producing a failed-row record.",
                "impact": "An unexpected row error can end the full run before a complete retained-row observation artifact exists.",
            },
        ],
        "decision": {
            "status": "V1_CONTAINED_NOT_G1_AUTHORITY",
            "epistemic_status": "OBSERVED",
            "required_action": "Preserve v1 and any abandoned run evidence; issue a separately versioned corrected engine and rerun from the unchanged preregistration before any G1 route selection.",
        },
        "falsifier": "A source-hash mismatch, enforced runtime guard, mechanical validation-score-loss disposition, or generic-row-exception retention would refute the corresponding v1 finding.",
        "replay": {
            "script_sha256": digest(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_probe_engine_hostile_v1.py --write",
            "check_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_probe_engine_hostile_v1.py --check",
        },
    }


def render(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(audit())
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite hostile-audit artifact")
        OUTPUT.write_text(payload, encoding="utf-8")
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text(encoding="utf-8") == payload, "G1 probe-engine hostile audit mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "status": "V1_CONTAINED_NOT_G1_AUTHORITY", "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
