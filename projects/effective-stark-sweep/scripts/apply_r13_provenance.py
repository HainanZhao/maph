#!/usr/bin/env python3
"""Issue the append-only R-13 provenance ledger for computational predicates.

Historical certificates remain byte-for-byte evidence of what was computed.  This
ledger is authoritative for their *effective* tags: a historical VERIFIED label is
not effective unless every load-bearing predicate is GENUINE.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from audit_engine_d_modulus_stability import run_stability_audit


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
W1 = ARTIFACTS / "w1-full-census-v1.json"
SCOPE = ARTIFACTS / "proxy-scope-and-tag-audit-v1.json"
OUTPUT = ARTIFACTS / "predicate-provenance-ledger-r13-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entry(
    path: Path,
    provenance: str,
    effective_tag: str,
    reason: str,
) -> dict:
    if provenance not in {"GENUINE", "PROXY", "MIXED"}:
        raise ValueError(provenance)
    return {
        "artifact": str(path.relative_to(ROOT)),
        "artifact_sha256": sha(path),
        "predicate_provenance": provenance,
        "effective_tag": effective_tag,
        "reason": reason,
    }


def main() -> None:
    rows = json.loads(W1.read_text(encoding="utf-8"))["records"]
    stable = run_stability_audit(rows)
    records: list[dict] = []

    # Canonical W2 closure certificates are genuine exactly when the finite
    # modulus is fixed by conjugation.  In that case the one-modulus two-place
    # ray field used by the old implementation is the required compositum.
    for path in sorted(ARTIFACTS.glob("rq*-b-closure-w2-v1.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        case_id = data["canonical_representative"]
        if stable[case_id]:
            records.append(
                entry(
                    path,
                    "GENUINE",
                    "VERIFIED_W2",
                    "finite modulus is conjugation-fixed; direct two-place reconstruction is genuine",
                )
            )
        else:
            if case_id != "RQ-007500":
                raise RuntimeError(f"unexpected unstable W2 closure {case_id}")
            records.append(
                entry(
                    path,
                    "PROXY",
                    "SUPERSEDED_PROXY_W2",
                    "one-modulus two-place field is not the actual normal closure for this unstable modulus",
                )
            )

    # Batch and summary artifacts mixed genuine and proxy predicates.  Their
    # historical VERIFIED tags are therefore ineffective as a whole.
    mixed_paths = [
        ARTIFACTS / "engine-b-two-route-analysis-v1.json",
        ARTIFACTS / "engine-b-two-route-degree24-v1.json",
        ARTIFACTS / "engine-b-two-route-degree32-v1.json",
        ARTIFACTS / "engine-b-two-route-degree40-v1.json",
        ARTIFACTS / "engine-b-closure-tranche-09-v1.json",
        ARTIFACTS / "engine-b-closure-w2-coverage-v1.json",
        ARTIFACTS / "corrected-battery-b195-v1.json",
    ]
    for path in mixed_paths:
        records.append(
            entry(
                path,
                "MIXED",
                "SUPERSEDED_MIXED_PROVENANCE",
                "contains at least one proxy-dependent unstable-modulus predicate",
            )
        )

    # The other completed closure tranches contain only stable-modulus
    # certificates and remain effective.
    for path in sorted(ARTIFACTS.glob("engine-b-closure-tranche-*-v1.json")):
        if path in mixed_paths:
            continue
        records.append(
            entry(
                path,
                "GENUINE",
                "VERIFIED_W2_TRANCHE",
                "all member closure certificates have GENUINE provenance",
            )
        )

    # Bespoke anchor paths construct the theorem fields directly.
    anchor_paths = [
        ARTIFACTS / "corrected-battery-anchor-b-v1.json",
        ARTIFACTS / "corrected-battery-anchor-reproduction-v1.json",
    ]
    for path in anchor_paths:
        records.append(
            entry(
                path,
                "GENUINE",
                "VERIFIED_ANCHOR_REPLAY",
                "bespoke anchor path reconstructs the required fields directly",
            )
        )

    recovery = ARTIFACTS / "rq007500-genuine-recovery-v1.json"
    if recovery.exists():
        records.append(
            entry(
                recovery,
                "GENUINE",
                "VERIFIED_W2_GENUINE_RECOVERY",
                "actual splitting field and two independent imaginary-base ray reconstructions agree",
            )
        )

    counts: dict[str, int] = {}
    for record in records:
        key = record["predicate_provenance"]
        counts[key] = counts.get(key, 0) + 1
        if key != "GENUINE" and record["effective_tag"].startswith("VERIFIED"):
            raise RuntimeError("R-13 violation: proxy/mixed artifact retains VERIFIED tag")

    relabelled = {record["artifact"] for record in records}
    historical_verified_w2 = set()
    for path in ARTIFACTS.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if str(data.get("claim_tag", "")).startswith("VERIFIED_W2"):
            historical_verified_w2.add(str(path.relative_to(ROOT)))
    missing = historical_verified_w2 - relabelled
    if missing:
        raise RuntimeError(
            f"historical VERIFIED_W2 artifacts lack R-13 labels: {sorted(missing)}"
        )

    payload = {
        "schema": "effective-stark-predicate-provenance-r13-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "rule": {
            "id": "R-13",
            "marks": ["GENUINE", "PROXY"],
            "mixed_aggregate_policy": (
                "an aggregate containing both marks is recorded as MIXED and "
                "cannot carry an effective VERIFIED tag"
            ),
            "verified_invariant": (
                "no effective VERIFIED_* tag at any level may depend on a "
                "PROXY predicate"
            ),
            "historical_artifact_policy": (
                "source artifacts remain immutable; this ledger supersedes "
                "their embedded tag for all downstream use"
            ),
        },
        "counts": counts,
        "historical_verified_w2_artifact_count":
            len(historical_verified_w2),
        "records": records,
        "rq007500_effective_state": (
            "VERIFIED_W2_GENUINE_RECOVERY"
            if recovery.exists()
            else "SUPERSEDED_PROXY_W2_PENDING_GENUINE_RECONSTRUCTION"
        ),
        "source_hashes": {
            str(W1.relative_to(ROOT)): sha(W1),
            str(SCOPE.relative_to(ROOT)): sha(SCOPE),
            "scripts/apply_r13_provenance.py": sha(Path(__file__)),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
