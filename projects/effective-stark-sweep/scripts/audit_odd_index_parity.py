#!/usr/bin/env python3
"""Independent preregistered consistency audit for the index-parity lemma."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
PREREG = ROOT / "data/results-paper-odd-index-parity-preregistration-v1.json"
LEDGER = ROOT / "artifacts/genuine-index-ledger-8200-v3.json"
FOURIER = ROOT / "artifacts/w1-full-census-v1.json"
WITHDRAWN = ROOT / "artifacts/frontier-odd-index-stability-correction-v1.json"
OUTPUT = ROOT / "artifacts/results-paper-odd-index-parity-audit-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    inputs = prereg["inputs"]
    for key, path in (
        ("genuine_index_ledger", LEDGER),
        ("exact_fourier_screen", FOURIER),
        ("withdrawn_proxy_population", WITHDRAWN),
    ):
        expected = inputs[key]["sha256"]
        actual = sha(path)
        if actual != expected:
            raise RuntimeError(f"{key}: hash changed: {actual} != {expected}")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    fourier_rows = json.loads(FOURIER.read_text(encoding="utf-8"))["records"]
    fourier = {row["case_id"]: row for row in fourier_rows}
    if len(ledger["records"]) != 8200 or len(fourier) != 8200:
        raise RuntimeError("the frozen 8200-row population changed")
    if {row["case_id"] for row in ledger["records"]} != set(fourier):
        raise RuntimeError("genuine-index and exact-Fourier case sets differ")

    index_histogram: Counter[int] = Counter()
    odd_records = []
    failures = []
    for row in ledger["records"]:
        case_id = row["case_id"]
        if row["predicate_provenance"] != "GENUINE":
            failures.append({"case_id": case_id, "failure": "non-genuine provenance"})
            continue
        transcript = ROOT / row["transcript"]
        if sha(transcript) != row["transcript_sha256"]:
            failures.append({"case_id": case_id, "failure": "transcript hash"})
            continue
        text = transcript.read_text(encoding="utf-8")
        match = re.findall(r"^DERIVED_SUBGROUP_ORDER=(\d+)$", text, re.MULTILINE)
        if len(match) != 1:
            failures.append({"case_id": case_id, "failure": "index parse"})
            continue
        genuine_index = int(match[0])
        if genuine_index != row["derived_subgroup_order"]:
            failures.append({"case_id": case_id, "failure": "ledger/transcript index"})
            continue
        index_histogram[genuine_index] += 1
        if genuine_index > 1 and genuine_index % 2 == 1:
            exact = fourier[case_id]
            trivial_sign = all(int(value) == 0 for value in exact["sign_log"])
            empty_support = (
                exact["support_count"] == 0 and exact["support_orders"] == []
            )
            record = {
                "case_id": case_id,
                "genuine_shintani_index": genuine_index,
                "sign_log": exact["sign_log"],
                "sign_class_trivial": trivial_sign,
                "support_count": exact["support_count"],
                "support_orders": exact["support_orders"],
                "support_empty": empty_support,
                "index_transcript": row["transcript"],
                "index_transcript_sha256": row["transcript_sha256"],
                "fourier_source_case_sha256": exact["source_case_sha256"],
            }
            odd_records.append(record)
            if not trivial_sign or not empty_support:
                failures.append({"case_id": case_id, "failure": "parity counterexample"})

    withdrawn = json.loads(WITHDRAWN.read_text(encoding="utf-8"))
    if withdrawn["population"]["rows"] != 88:
        raise RuntimeError("withdrawn proxy control population changed")
    if failures:
        verdict = "FAIL_WITHDRAW_LEMMA"
        claim_tag = "FAIL"
    else:
        verdict = "PASS"
        claim_tag = "VERIFIED_CONSISTENCY_AUDIT"
    payload = {
        "schema": "effective-stark-results-paper-odd-index-parity-audit-v1",
        "claim_tag": claim_tag,
        "verdict": verdict,
        "preregistration": {
            "path": str(PREREG.relative_to(ROOT)),
            "sha256": sha(PREREG),
            "recorded_at_utc": prereg["recorded_at_utc"],
        },
        "genuine_population": len(ledger["records"]),
        "genuine_index_histogram": {
            str(key): value for key, value in sorted(index_histogram.items())
        },
        "odd_index_greater_than_one_count": len(odd_records),
        "odd_index_rows_with_trivial_sign_class": sum(
            row["sign_class_trivial"] for row in odd_records
        ),
        "odd_index_rows_with_empty_support": sum(
            row["support_empty"] for row in odd_records
        ),
        "exception_count": len(failures),
        "exceptions": failures,
        "records": odd_records,
        "withdrawn_proxy_control": {
            "row_count": 88,
            "use": "provenance control only; excluded from the lemma test",
            "semantic_verdict": withdrawn["semantic_verdict"],
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (PREREG, LEDGER, FOURIER, WITHDRAWN, SELF)
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"GENUINE_POPULATION={len(ledger['records'])}")
    print(f"ODD_INDEX_GT_ONE_COUNT={len(odd_records)}")
    print(f"TRIVIAL_SIGN_CLASS_COUNT={payload['odd_index_rows_with_trivial_sign_class']}")
    print(f"EMPTY_SUPPORT_COUNT={payload['odd_index_rows_with_empty_support']}")
    print(f"EXCEPTION_COUNT={len(failures)}")
    print(f"VERDICT={verdict}")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
