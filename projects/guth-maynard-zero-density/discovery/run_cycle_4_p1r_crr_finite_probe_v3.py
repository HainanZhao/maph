#!/usr/bin/env python3
"""Execute/check the v3 dimensional-correction CRR finite probe."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "discovery/run_cycle_4_p1r_crr_finite_probe_v2.py"
spec = importlib.util.spec_from_file_location("crr_probe_v2_runner_base", BASE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load v2 runner implementation")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

base.SELF = Path(__file__).resolve()
base.PREREG = ROOT / "artifacts/cycle-4-p1r-crr-finite-probe-preregistration-v3.json"
base.OUTPUT = ROOT / "discovery/cycle-4-p1r-crr-finite-probe-v3.json"
base.PREREG_BUILDER = ROOT / "discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v3.py"
base.CONVENTIONS = ROOT / "conventions/crr_finite_analogue_probe_v3.py"


def validate_prereg():
    """v3 equivalent of the base validation, with its own frozen key."""
    builder = base.load_module(base.PREREG_BUILDER, "crr_probe_v3_prereg_builder")
    expected = builder.render(builder.seal())
    base.require(base.PREREG.is_file() and base.PREREG.read_bytes() == expected, "sealed v3 preregistration byte replay failed")
    artifact = base.json.loads(expected)
    base.require(artifact["status"] == "SEALED_DISCOVERY_PREREGISTRATION_EXECUTABLE", "v3 preregistration is not executable")
    conventions = base.load_module(base.CONVENTIONS, "crr_probe_v3_conventions")
    base.require(base.runtime_metadata() == artifact["runtime"], "runtime does not match sealed v3 preregistration")
    base.require(base.sha256(base.CONVENTIONS) == artifact["frozen_hashes"]["v3_conventions"]["sha256"], "v3 convention hash mismatch")
    return artifact, conventions


base.validate_prereg = validate_prereg
_execute = base.execute


def execute():
    payload = _execute()
    payload["artifact_id"] = "cycle-4-p1r-crr-finite-probe-v3"
    payload["cubic_dimensional_identity"] = "tr(B_M^3)=tr((DG)^3)-3M tr((DG)^2)+3M^2 tr(DG)-R*M^3; no 2M-dimensional shifted trace was used"
    return payload


base.execute = execute


if __name__ == "__main__":
    raise SystemExit(base.main())
