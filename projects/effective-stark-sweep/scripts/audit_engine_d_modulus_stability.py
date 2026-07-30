#!/usr/bin/env python3
"""Re-screen the proposed Engine-D population for Galois-stable moduli.

The Shintani index computation in ``screen_w1_case.gp`` models
``[H:H intersect Q^ab]`` only when the finite modulus is fixed by the
non-trivial automorphism of the real quadratic base.  Applying its
``index == 1`` output to a single split prime is unsound: conjugation
changes the ray problem itself.  This independent audit supplies the
missing predicate before any Engine-D theorem or census promotion.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
W1 = ROOT / "artifacts/w1-full-census-v1.json"
OLD_D = ROOT / "artifacts/engine-d-index-one-candidates-v1.json"
OUTPUT = ROOT / "artifacts/engine-d-modulus-stability-audit-v1.json"
INVALIDATED_CONTROLS = ("RQ-000018", "RQ-000032", "RQ-000274")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field_polynomial(d: int) -> str:
    if d % 4 == 1:
        return f"y^2-y+({1-d})/4"
    return f"y^2-{d}"


def run_stability_audit(rows: list[dict]) -> dict[str, bool]:
    """Evaluate ideal conjugation in one persistent GP process."""
    lines = [
        "default(parisizemax,4000000000);",
        'print("PARI_VERSION|",version());',
    ]
    current_d = None
    for row in rows:
        d = int(row["d"])
        if d != current_d:
            current_d = d
            lines.extend(
                [
                    f"kfield=bnfinit({field_polynomial(d)},1);",
                    "autos=nfgaloisconj(kfield);autq=autos[1];",
                    (
                        "if(autq==Mod(y,kfield.pol),"
                        "autq=autos[2]);"
                    ),
                ]
            )
        hnf = row["finite_ideal_hnf"]
        lines.extend(
            [
                (
                    f"finiteideal=[{hnf[0][0]},{hnf[0][1]};"
                    f"{hnf[1][0]},{hnf[1][1]}];"
                ),
                (
                    'print("STABLE|'
                    f'{row["case_id"]}|",'
                    "idealhnf(kfield,nfgaloisapply("
                    "kfield,autq,finiteideal))=="
                    "idealhnf(kfield,finiteideal));"
                ),
            ]
        )
    lines.append("quit;")
    completed = subprocess.run(
        ["gp", "-q"],
        input="\n".join(lines) + "\n",
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=3600,
        check=False,
    )
    fatal = "\n".join(
        line
        for line in completed.stderr.splitlines()
        if "Warning:" not in line
    )
    if completed.returncode or "***" in fatal:
        raise RuntimeError(
            "modulus-stability GP audit failed:\n"
            f"{completed.stdout}\n{completed.stderr}"
        )
    result: dict[str, bool] = {}
    for line in completed.stdout.splitlines():
        if not line.startswith("STABLE|"):
            continue
        _, case_id, value = line.split("|")
        result[case_id] = value == "1"
    expected = {str(row["case_id"]) for row in rows}
    if set(result) != expected:
        missing = sorted(expected - set(result))
        raise RuntimeError(f"missing GP stability results: {missing[:10]}")
    return result


def main() -> None:
    w1 = json.loads(W1.read_text(encoding="utf-8"))
    rows = w1["records"]
    index_one_proxy = [
        row
        for row in rows
        if row["shintani_index"] == 1 and row["commutator_size"] == 1
    ]
    stable = run_stability_audit(index_one_proxy)
    stable_rows = [
        row for row in index_one_proxy if stable[row["case_id"]]
    ]
    exact_substantive = [
        row
        for row in stable_rows
        if row["verdict"] == "FRONTIER" and row["support_count"] > 0
    ]
    unstable_substantive = [
        row
        for row in index_one_proxy
        if not stable[row["case_id"]]
        and row["verdict"] == "FRONTIER"
        and row["support_count"] > 0
    ]
    overlap = Counter()
    for row in index_one_proxy:
        if row["support_count"] == 0:
            overlap["proved_trivial_empty_support"] += 1
        elif row["engine"] == "A":
            overlap["engine_a_substantive"] += 1
        elif stable[row["case_id"]]:
            overlap["engine_d_exact_substantive"] += 1
        else:
            overlap["invalidated_unstable_modulus_substantive"] += 1
    if sum(overlap.values()) != len(index_one_proxy):
        raise RuntimeError("index-one overlap partition is not exhaustive")

    payload = {
        "schema": "effective-stark-engine-d-modulus-stability-audit-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_EXACT_STRUCTURAL_CORRECTION",
        "finding": (
            "The former criterion shintani_index=1 and "
            "commutator_size=1 is insufficient unless the finite "
            "modulus is Galois-stable.  For an unstable modulus the "
            "conjugation matrix compares different ray problems, so "
            "its commutator/index output cannot certify that the "
            "one-place ray field is abelian over Q."
        ),
        "corrected_predicate": {
            "finite_modulus_fixed_by_base_conjugation": True,
            "shintani_index": 1,
            "commutator_size": 1,
            "meaning": (
                "under modulus stability, the one-place field equals "
                "its intersection with Q^ab"
            ),
        },
        "counts": {
            "former_index_one_abelian_proxy_occurrences":
                len(index_one_proxy),
            "galois_stable_modulus_occurrences": len(stable_rows),
            "corrected_substantive_engine_d_occurrences":
                len(exact_substantive),
            "corrected_substantive_engine_d_fields": len(
                {row["d"] for row in exact_substantive}
            ),
            "invalidated_unstable_substantive_occurrences":
                len(unstable_substantive),
        },
        "former_3521_overlap_partition": dict(sorted(overlap.items())),
        "former_anchor_stability": [
            {
                "case_id": case_id,
                "finite_modulus_galois_stable": stable[case_id],
                "field_discriminant": next(
                    row["field_discriminant"]
                    for row in index_one_proxy
                    if row["case_id"] == case_id
                ),
                "finite_norm": next(
                    row["finite_norm"]
                    for row in index_one_proxy
                    if row["case_id"] == case_id
                ),
            }
            for case_id in INVALIDATED_CONTROLS
        ],
        "corrected_candidate_case_ids": [
            row["case_id"] for row in exact_substantive
        ],
        "corrected_candidate_support_distribution": [
            {"orders": list(orders), "count": count}
            for orders, count in sorted(
                Counter(
                    tuple(row["support_orders"])
                    for row in exact_substantive
                ).items(),
                key=lambda item: (-item[1], item[0]),
            )
        ],
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (W1, OLD_D, Path(__file__).resolve())
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "FORMER_PROXY_OCCURRENCES="
        f"{len(index_one_proxy)}"
    )
    print(
        "CORRECTED_ENGINE_D_SUBSTANTIVE_OCCURRENCES="
        f"{len(exact_substantive)}"
    )
    print(
        "CORRECTED_ENGINE_D_SUBSTANTIVE_FIELDS="
        f"{len({row['d'] for row in exact_substantive})}"
    )
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
