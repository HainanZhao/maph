#!/usr/bin/env python3
"""Exact Phase-0 controls for the 2-elementary TCC sweep.

This is deliberately only a calibration verifier.  PARI's bnrinit handles
the maximal order O_K; AFK's general formula uses the order O_f.  The
script therefore verifies the conductor-one D4/D5 controls and refuses to
pretend that they establish the nonmaximal-order general case.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "tcc-sweep-phase0-calibrations-v1.json"
D4 = ROOT / "certificates" / "dimension-four-certificate.json"
D5 = ROOT / "certificates" / "dimension-five-character-support.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pari_structure(polynomial: str, modulus: int) -> list[int]:
    program = f"""K=bnfinit({polynomial},1);R=bnrinit(K,[{modulus},[1,0]],1);print(Vec(R.cyc));"""
    completed = subprocess.run(
        ["gp", "-q"], input=program, text=True, capture_output=True,
        check=True, cwd=ROOT,
    )
    line = completed.stdout.strip()
    if not (line.startswith("[") and line.endswith("]")):
        raise RuntimeError(f"unexpected PARI invariant factors: {line!r}")
    return [int(entry) for entry in line[1:-1].split(",") if entry]


def cyclic_character_rows(order: int, sign_log: int) -> list[dict[str, int | bool]]:
    rows: list[dict[str, int | bool]] = []
    for exponent in range(order):
        value_is_one = (exponent * sign_log) % order == 0
        character_order = 1 if exponent == 0 else order // __import__("math").gcd(order, exponent)
        rows.append(
            {
                "character_exponent": exponent,
                "character_order": character_order,
                "odd_on_R": not value_is_one,
                "fourier_coefficient_of_1_minus_R": 0 if value_is_one else 2,
            }
        )
    return rows


def main() -> None:
    started = time.monotonic()
    d4 = json.loads(D4.read_text())
    d5 = json.loads(D5.read_text())
    d4_cyc = pari_structure("x^2-x-1", 4)
    d5_cyc = pari_structure("y^2-4*y+1", 5)
    if d4_cyc != [2] or d5_cyc != [8]:
        raise AssertionError((d4_cyc, d5_cyc))

    d4_kopp = d4["ray_and_unit_arithmetic"]
    if d4_kopp["kopp_modulus"] != "(4) infinity_2":
        raise AssertionError("D4 modulus drift")
    if d4_kopp["modulus_audits"]["4"]["one_real_place_ray_group_order"] != 2:
        raise AssertionError("D4 certificate/group disagreement")
    if d5["ray_group"] != "C8" or d5["sign_class"] != "R=g^4":
        raise AssertionError("D5 sign-class drift")
    if d5["orders_on_support"] != [8, 8, 8, 8]:
        raise AssertionError("D5 support drift")

    d4_rows = cyclic_character_rows(2, 1)
    d5_rows = cyclic_character_rows(8, 4)
    d4_support_orders = [row["character_order"] for row in d4_rows if row["odd_on_R"]]
    d5_support_orders = [row["character_order"] for row in d5_rows if row["odd_on_R"]]
    if d4_support_orders != [2] or d5_support_orders != [8, 8, 8, 8]:
        raise AssertionError((d4_support_orders, d5_support_orders))

    output = {
        "schema": "tcc-sweep-phase0-calibrations-v1",
        "claim_tag": "PROVED",
        "scope": "conductor-one maximal-order controls only",
        "pari": {"command": "gp -q", "version": subprocess.run(["gp", "-q"], input="print(version());", text=True, capture_output=True, check=True).stdout.strip()},
        "embedding_convention": {
            "pari_real_place_selector": "[1,0]",
            "meaning": "the increasing-root embedding, i.e. infinity_2 with sqrt(D)<0 in the two controls",
        },
        "controls": {
            "D4": {
                "field": "Q(sqrt(5))", "conductor": 1, "modulus": "(4) infinity_2",
                "ray_invariant_factors": d4_cyc, "sign_class_log": 1,
                "support_character_orders": d4_support_orders,
                "complete_quadratic_support": True,
                "source_certificate_modulus": d4_kopp["kopp_modulus"],
            },
            "D5": {
                "field": "Q(sqrt(3))", "conductor": 1, "modulus": "(5) infinity_2",
                "ray_invariant_factors": d5_cyc, "sign_class_log": 4,
                "support_character_orders": d5_support_orders,
                "complete_quadratic_support": False,
                "reason": "all four characters in the 1-R support have order eight",
            },
        },
        "predicate_used_for_controls": "For a cyclic ray group C_N=<g>, the support of 1-g^a is exactly the characters k with k*a not congruent to 0 mod N.",
        "containment": {
            "tag": "PROVED",
            "statement": "These controls do not justify a tuple-only maximal-order scan: AFK's general squared-overlap formula is indexed by Clt_{d infinity_2}(O_f), so a nonmaximal form conductor changes the ray object.",
        },
        "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in (D4, D5, Path(__file__))},
        "wall_seconds": time.monotonic() - started,
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print("TCC_SWEEP_PHASE0_CALIBRATIONS=PASS")


if __name__ == "__main__":
    main()
