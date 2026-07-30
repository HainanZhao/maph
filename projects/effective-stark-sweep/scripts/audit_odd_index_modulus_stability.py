#!/usr/bin/env python3
"""Correct the semantics of the 88-row odd-index proxy correlation."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from audit_engine_d_modulus_stability import run_stability_audit


ROOT = Path(__file__).resolve().parents[1]
W1 = ROOT / "artifacts/w1-full-census-v1.json"
ODD = ROOT / "artifacts/frontier-odd-index-correlates-v1.json"
OUTPUT = ROOT / "artifacts/frontier-odd-index-stability-correction-v1.json"
EXCEPTION_DIR = ROOT / "artifacts/frontier-odd-index-exceptions"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    w1 = json.loads(W1.read_text(encoding="utf-8"))
    by_id = {row["case_id"]: row for row in w1["records"]}
    old = json.loads(ODD.read_text(encoding="utf-8"))
    rows = [by_id[record["case_id"]] for record in old["records"]]
    stable = run_stability_audit(rows)
    commutator_exceptions = [
        row
        for row in rows
        if row["commutator_size"] != row["shintani_index"]
    ]

    def shares_support_prime(row: dict) -> bool:
        index = int(row["shintani_index"])
        prime = 3
        primes = []
        while prime * prime <= index:
            if index % prime == 0:
                primes.append(prime)
                while index % prime == 0:
                    index //= prime
            prime += 2
        if index > 1:
            primes.append(index)
        return any(
            order % prime == 0
            for order in row["support_orders"]
            for prime in primes
        )

    support_exceptions = [
        row for row in rows if not shares_support_prime(row)
    ]
    if len(commutator_exceptions) != 3:
        raise RuntimeError("expected three commutator exceptions")
    if len(support_exceptions) != 2:
        raise RuntimeError("expected two support-prime exceptions")
    if any(stable.values()):
        raise RuntimeError(
            "an odd-index row unexpectedly has stable finite modulus"
        )

    exception_records = []
    EXCEPTION_DIR.mkdir(parents=True, exist_ok=True)
    for row in commutator_exceptions + support_exceptions:
        exception_type = (
            "INDEX_3_COMMUTATOR_6"
            if row in commutator_exceptions
            else "SUPPORT_NO_COMMON_ODD_PRIME"
        )
        record = {
            "schema":
                "effective-stark-odd-index-proxy-exception-v1",
            "claim_tag": "VERIFIED_EXACT_PROXY_EXCEPTION",
            "case_id": row["case_id"],
            "exception_type": exception_type,
            "d": row["d"],
            "field_discriminant": row["field_discriminant"],
            "finite_ideal_hnf": row["finite_ideal_hnf"],
            "finite_norm": row["finite_norm"],
            "finite_modulus_galois_stable": False,
            "recorded_index_proxy": row["shintani_index"],
            "recorded_commutator_proxy": row["commutator_size"],
            "support_orders": row["support_orders"],
            "semantic_correction": (
                "because the finite modulus is not fixed by base "
                "conjugation, these exact coordinate outputs are not "
                "a Shintani index and normal-closure commutator size"
            ),
            "source_case_sha256": row["source_case_sha256"],
        }
        path = EXCEPTION_DIR / f"{row['case_id']}.json"
        path.write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        exception_records.append(
            {
                "case_id": row["case_id"],
                "exception_type": exception_type,
                "path": str(path.relative_to(ROOT)),
                "sha256": sha(path),
            }
        )

    payload = {
        "schema":
            "effective-stark-frontier-odd-index-stability-correction-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_RETRACTION_AND_PROXY_STATISTIC",
        "population": {
            "rows": len(rows),
            "galois_stable_finite_moduli": sum(stable.values()),
            "galois_unstable_finite_moduli":
                len(rows) - sum(stable.values()),
        },
        "old_exact_coordinate_regularities": {
            "index_proxy_equals_commutator_proxy": "85/88",
            "index_proxy_shares_odd_prime_with_support": "86/88",
        },
        "semantic_verdict": (
            "The two fractions remain reproducible statistics of the "
            "old coordinate proxy, but all 88 moduli are unstable. "
            "They are retracted as Shintani-index/normal-closure laws "
            "and may not be used in W4 as structural evidence."
        ),
        "exception_files": exception_records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (W1, ODD, Path(__file__).resolve())
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("ODD_PROXY_MODULUS_STABLE=0/88")
    print("EXCEPTION_FILES=5")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
