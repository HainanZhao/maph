#!/usr/bin/env python3
"""Quantify the census exposure to the missing modulus-stability gate."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from audit_engine_d_modulus_stability import run_stability_audit


ROOT = Path(__file__).resolve().parents[1]
W1 = ROOT / "artifacts/w1-full-census-v1.json"
QUEUES = ROOT / "artifacts/identification-queues-v2.json"
OUTPUT = ROOT / "artifacts/conjugation-dependent-census-audit-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_count(case_ids: set[str], stable: dict[str, bool]) -> dict:
    count = len(case_ids)
    stable_count = sum(stable[case_id] for case_id in case_ids)
    return {
        "total": count,
        "galois_stable_finite_modulus": stable_count,
        "galois_unstable_finite_modulus": count - stable_count,
    }


def main() -> None:
    w1 = json.loads(W1.read_text(encoding="utf-8"))
    queues = json.loads(QUEUES.read_text(encoding="utf-8"))
    rows = w1["records"]
    all_ids = {row["case_id"] for row in rows}
    stable = run_stability_audit(rows)

    trivial = {
        row["case_id"]
        for row in rows
        if row["engine"] == "A" and row["support_count"] == 0
    }
    engine_a = {
        row["case_id"]
        for row in rows
        if row["engine"] == "A" and row["support_count"] > 0
    }
    engine_b = set(queues["engine_b"]["two_route_pass_case_ids"])
    engine_c = set(queues["engine_c"]["geometry_eligible_case_ids"])
    named = {
        "PROVED_TRIVIAL": trivial,
        "ENGINE_A_NONTRIVIAL_ELIGIBLE": engine_a,
        "ENGINE_B_ELIGIBLE": engine_b,
        "ENGINE_C_ELIGIBLE": engine_c,
    }
    union = set().union(*named.values())
    if sum(map(len, named.values())) != len(union):
        raise RuntimeError("formal theorem-route sets overlap")
    frontier = all_ids - union
    if len(frontier) != 1818:
        raise RuntimeError(f"expected 1818 FRONTIER rows, got {len(frontier)}")
    named["FRONTIER"] = frontier

    unstable_b = sorted(
        case_id for case_id in engine_b if not stable[case_id]
    )
    stable_b = sorted(
        case_id for case_id in engine_b if stable[case_id]
    )
    payload = {
        "schema":
            "effective-stark-conjugation-dependent-census-audit-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_EXACT_CONTAINMENT_AUDIT",
        "all_rows": split_count(all_ids, stable),
        "formal_split_exposure": {
            label: split_count(case_ids, stable)
            for label, case_ids in named.items()
        },
        "route_semantics": {
            "PROVED_TRIVIAL": (
                "does not need the conjugation action; no change"
            ),
            "ENGINE_A_NONTRIVIAL_ELIGIBLE": (
                "the quadratic ACNF theorem is relative and does not "
                "need finite-modulus stability; no change"
            ),
            "ENGINE_C_ELIGIBLE": (
                "the complete C geometry screen constructs the actual "
                "packet splitting closure and checks its group and CM "
                "bases; the later gate supersedes W1's heuristic "
                "conjugation calculation"
            ),
            "ENGINE_B_ELIGIBLE": (
                "the two-route B screen calls the one finite-modulus "
                "ray field its normal closure. This is justified only "
                "for the 131 stable rows; 64 unstable rows are "
                "quarantined pending reconstruction from the "
                "compositum with the conjugate-modulus field"
            ),
            "FRONTIER": (
                "no promotions follow from this audit; conjugation-"
                "dependent proxy values on unstable rows lose their "
                "Shintani-index interpretation"
            ),
        },
        "engine_b_containment": {
            "safe_stable_case_ids": stable_b,
            "quarantined_unstable_case_ids": unstable_b,
            "next_gate": (
                "construct the actual normal closure as the compositum "
                "of the finite-modulus ray field and its conjugate; "
                "then recompute the maximal absolutely abelian "
                "subfield and Shintani index"
            ),
        },
        "banked_headline_controls": {
            case_id: stable[case_id]
            for case_id in ("RQ-000458", "RQ-000129", "RQ-002057")
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (W1, QUEUES, Path(__file__).resolve())
        },
    }
    if not all(payload["banked_headline_controls"].values()):
        raise RuntimeError("a banked headline control is exposed")
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"ALL_STABLE={sum(stable.values())}/8200")
    print(f"B_SAFE_STABLE={len(stable_b)}/195")
    print(f"B_QUARANTINED_UNSTABLE={len(unstable_b)}")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
