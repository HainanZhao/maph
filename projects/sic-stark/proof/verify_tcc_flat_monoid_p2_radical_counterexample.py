#!/usr/bin/env python3
"""Structural audit for the certified d=12,f=3 radical counterexample."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "tcc-flat-monoid-p2-radical-counterexample-v2.json"
PREREG = ROOT / "data" / "tcc-flat-monoid-p2-preregistration-v2.json"
MONOID = ROOT / "discovery" / "tcc-flat-monoid-p1-overlap-adapter-v1.json"
LABELS = ROOT / "discovery" / "tcc-flat-monoid-p1-overlap-labels-v1.json"
SCRIPT = ROOT / "proof" / "certify_tcc_flat_monoid_p2_radical_counterexample.py"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    record = json.loads(ARTIFACT.read_text())
    if record["preregistration_sha256"] != digest(PREREG):
        raise AssertionError("preregistration hash mismatch")
    if record["monoid_artifact_sha256"] != digest(MONOID):
        raise AssertionError("monoid artifact hash mismatch")
    if record["label_artifact_sha256"] != digest(LABELS):
        raise AssertionError("label artifact hash mismatch")
    if record["source_script_sha256"] != digest(SCRIPT):
        raise AssertionError("source script hash mismatch")
    if record["radical_vector"] != {"0": "-1", "3": "1"}:
        raise AssertionError("target radical vector changed")
    lower = float(record["enclosure_lower"].split()[0].strip("["))
    upper = float(record["enclosure_upper"].split()[0].strip("["))
    if not (lower < upper < 0):
        raise AssertionError("certified enclosure no longer excludes zero")
    monoid = json.loads(MONOID.read_text())["case"]
    vector = monoid["radical"]["basis"][0]
    if [(i, value) for i, value in enumerate(vector) if value != "0"] != [(0, "-1"), (3, "1")]:
        raise AssertionError("radical basis changed")
    labels = json.loads(LABELS.read_text())
    class_three = next(
        row for row in labels["stabilizer_orbits"] if row["monoid_element"] == 3
    )
    if class_three["representative"] != [4, 10]:
        raise AssertionError("characteristic label changed")
    if record["checks"]["one_place_fiber_cardinality"] != 2:
        raise AssertionError("one-place fiber factor changed")
    print("TCC_FLAT_MONOID_P2_RADICAL_COUNTEREXAMPLE_AUDIT=PASS")
    print("D12_RADICAL_VECTOR=e_3-e_0")
    print(f"D12_RADICAL_DERIVATIVE_INTERVAL=[{lower},{upper}]")


if __name__ == "__main__":
    main()
