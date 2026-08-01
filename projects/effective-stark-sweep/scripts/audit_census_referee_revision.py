#!/usr/bin/env python3
"""Audit the Cycle-127 census claim-boundary and referee repairs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper/effective-stark-census.tex"
LOG = ROOT / "paper/effective-stark-census.log"
AMENDMENT = ROOT / "data/census-paper-preregistration-amendment-v18.json"
FROZEN = ROOT / "artifacts/frozen-ideal-census-v1.json"
Q_AUDIT = ROOT / "artifacts/census-q-packet-corpus-audit-v1.json"
H = ROOT / "artifacts/census-h-taxonomy-v2.json"
RQ39 = ROOT / "artifacts/rq000039-engine-b-transport-v1.json"
B5025 = ROOT / "artifacts/b5025-euler-deletion-transports-v2.json"
B5025_LABEL = ROOT / "artifacts/b5025-label-aware-transports-v1.json"
B5022_LABEL = ROOT / "artifacts/b5022-label-aware-transports-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(text: str, snippets: tuple[str, ...]) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        raise RuntimeError(f"missing Cycle-127 manuscript content: {missing}")


def transport_row(record: dict, coefficient: int) -> str:
    factors = "$" + ",".join(
        f"({item['source_ray_log']},{item['exponent']})"
        for item in record["factors"]
    ) + "$"
    return (
        f"{record['case_id']} & {record['source_case_id']} & "
        f"{record['closure_id']} & {coefficient} & {factors} & PROVED"
    )


def main() -> None:
    source = PAPER.read_text(encoding="utf-8")
    amendment = json.loads(AMENDMENT.read_text(encoding="utf-8"))
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    q = json.loads(Q_AUDIT.read_text(encoding="utf-8"))
    h = json.loads(H.read_text(encoding="utf-8"))

    for relative, expected in amendment["source_hashes"].items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"Cycle-127 source hash drifted: {relative}")

    if (
        frozen["self_conjugate_raw_count"]
        + frozen["nonself_conjugate_raw_count"] // 2
        != frozen["deduplicated_case_count"]
        or frozen["deduplicated_case_count"] != 8200
    ):
        raise RuntimeError("finite-ideal orbit identity failed")

    forbidden = (
        "conjugate one-place pairs identified",
        "conjugate real places identified",
        "empty support is exactly the trivial packet condition",
        "exact higher-order mechanism eligibility",
        "all registered mechanisms fail & 1359",
        "incomplete legacy quartic construction & 5",
    )
    present = [phrase for phrase in forbidden if phrase in source]
    if present:
        raise RuntimeError(f"withdrawn wording returned: {present}")

    require(source, (
        "This is a canonical",
        "selected-modulus census",
        "not the full isomorphism-class quotient",
        "2461+\\frac{11478}{2}=8200",
        "The converse is false",
        "346-row value-one",
        "packet-value-orbit polynomial",
        "not, by itself, a class-to-root labelling",
        "integrity record, not a",
        "complete on 2,699 rows",
        "five old quartic constructions remain",
        "not counted as failures",
        "10^{-38}",
        "RQ-006617",
        "10.5281/zenodo.21729947",
        "Deleted-prime cover criterion",
        "four-support nondegeneracy",
    ))
    if q["population"]["all_zero_X_minus_1_rows"] != 346:
        raise RuntimeError("Q value-one degeneracy changed")

    cross = Counter(
        (row["exclusive_v5_route"], row["roblot_full_row_status"])
        for row in h["records"]
    )
    expected_cross = {
        ("ENGINE_B_ELIGIBLE", "FULL_ROW_WEAK_COVERAGE"): 70,
        ("ENGINE_B_ELIGIBLE", "NOT_COVERED_HYPOTHESIS_FAILURE"): 45,
        ("ENGINE_B_ELIGIBLE", "NOT_COVERED_UNSUPPORTED_ORDER"): 117,
        ("ENGINE_C_ELIGIBLE", "FULL_ROW_WEAK_COVERAGE"): 782,
        ("ENGINE_C_ELIGIBLE", "NOT_COVERED_HYPOTHESIS_FAILURE"): 99,
        ("FRONTIER", "FULL_ROW_WEAK_COVERAGE"): 227,
        ("FRONTIER", "NOT_COVERED_HYPOTHESIS_FAILURE"): 261,
        ("FRONTIER", "NOT_COVERED_UNSUPPORTED_ORDER"): 1098,
        ("FRONTIER", "INCOMPLETE_KERNEL_FAILURE"): 5,
    }
    if dict(cross) != expected_cross:
        raise RuntimeError("H route-by-Roblot cross-table drifted")
    if sum(value for (route, status), value in cross.items()
           if status != "INCOMPLETE_KERNEL_FAILURE") != 2699:
        raise RuntimeError("complete H status count changed")

    records = []
    rq39 = json.loads(RQ39.read_text(encoding="utf-8"))
    records.append(
        {
            "case_id": rq39["target_case_id"],
            "source_case_id": rq39["source_case_id"],
            "closure_id": rq39["closure_id"],
            "factors": [{"source_ray_log": 1, "exponent": 1}],
            "coefficient": 1,
        }
    )
    for path in (B5025, B5025_LABEL, B5022_LABEL):
        artifact = json.loads(path.read_text(encoding="utf-8"))
        for record in artifact["records"]:
            record = dict(record)
            record["coefficient"] = record.get(
                "ray_map_generator_coefficient", 1
            )
            records.append(record)
    if len(records) != 12:
        raise RuntimeError("transport table row count changed")
    for record in records:
        if transport_row(record, record["coefficient"]) not in source:
            raise RuntimeError(
                f"transport table mismatch: {record['case_id']}"
            )

    citations = set(re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}", source))
    cited_keys = {key for group in citations for key in group.split(",")}
    bib_keys = set(re.findall(r"\\bibitem\{([^}]+)\}", source))
    if cited_keys != bib_keys:
        raise RuntimeError(
            f"citation/bibliography mismatch: cited={cited_keys}, bib={bib_keys}"
        )

    if LOG.exists():
        log = LOG.read_text(encoding="utf-8", errors="replace")
        bad = [token for token in ("Overfull \\hbox", "undefined references")
               if token in log]
        if bad:
            raise RuntimeError(f"rendered manuscript warnings: {bad}")

    print("CENSUS_REFEREE_REVISION_AUDIT=PASS")


if __name__ == "__main__":
    main()
