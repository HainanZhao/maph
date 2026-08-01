#!/usr/bin/env python3
"""Exact d=12, f=3 conductor-modulus-overlap flat-monoid pilot."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from build_tcc_flat_monoid_p1_adapter import build_case  # noqa: E402


PREREG = ROOT / "data" / "tcc-flat-monoid-p1-preregistration-v2.json"
V1 = ROOT / "discovery" / "tcc-flat-monoid-p1-adapter-v1.json"
SOURCE_NOTE = ROOT / "docs" / "tcc-flat-monoid-p1-source-interface-v1.md"
OUT = ROOT / "discovery" / "tcc-flat-monoid-p1-overlap-adapter-v1.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    started = time.monotonic()
    prereg = json.loads(PREREG.read_text())
    d12 = build_case(
        name="AFK overlap pilot d=12, K=Q(sqrt(13)), O_3",
        delta=13,
        f=3,
        d=12,
        # eta=(11+3sqrt(13))/2=-14+theta_3 is positive at infinity_2.
        unit_actions=[(-14, 1, 1), (-1, 0, -1)],
        expected_total=50,
        expected_primitive=24,
    )
    radical = d12["radical"]
    if (len(radical["basis"]), radical["power_dimensions"]) != (19, [19, 2, 0]):
        raise AssertionError("overlap radical invariant changed")
    payload = {
        "schema": "tcc-flat-monoid-p1-overlap-adapter-v1",
        "claim_tag": "PROVED_FINITE_ALGEBRA_PILOT",
        "scope": (
            "The frozen d=12,f=3 conductor-modulus-overlap monoid under the "
            "class-number-one direct equivalence lemma. No AFK partial-zeta "
            "value, packet, support, or TCC claim is made."
        ),
        "preregistration_sha256": digest(PREREG),
        "v1_control_sha256": digest(V1),
        "source_note_sha256": digest(SOURCE_NOTE),
        "source_hashes": prereg["input_sha256"],
        "case": d12,
        "checks": {
            "ordinary_order_class_number": 1,
            "class_number_proof": (
                "h(117)=h(13)*3*(1-(13/3)/3)/2=1; the denominator is "
                "[O_K^x:O_3^x]=2 because epsilon^2 is the first unit in O_3."
            ),
            "radical_dimension": 19,
            "radical_power_dimensions": [19, 2, 0],
            "target_functional_evaluated": False,
        },
        "wall_seconds": round(time.monotonic() - started, 6),
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("TCC_FLAT_MONOID_P1_OVERLAP_ADAPTER=PASS")
    print(f"D12_MONOID_ELEMENTS={d12['element_count']}")
    print(f"D12_RADICAL_DIMENSION={len(radical['basis'])}")
    print(f"D12_RADICAL_POWER_DIMENSIONS={radical['power_dimensions']}")


if __name__ == "__main__":
    main()
