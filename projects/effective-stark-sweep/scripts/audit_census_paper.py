#!/usr/bin/env python3
"""Check that the census manuscript states only frozen artifact facts."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper/effective-stark-census.tex"
PDF = ROOT / "paper/effective-stark-census.pdf"
LAYER0 = ROOT / "artifacts/census-paper-layer0-reconciliation-v1.json"
Q_AUDIT = ROOT / "artifacts/census-q-packet-corpus-audit-v1.json"
H_TAXONOMY = ROOT / "artifacts/census-h-taxonomy-v2.json"
TRANSPORT = ROOT / "artifacts/engine-b-transport-manifest-v5.json"
TRANSPORT_LEDGER = ROOT / "artifacts/engine-b-transport-ledger-v4.json"
IMPRIMITIVE = ROOT / "artifacts/rq000013-engine-a-imprimitive-certificate-v1.json"
HILBERT_B5079 = ROOT / "artifacts/b5079-hilbert-ray-containment-v1.json"
HILBERT_TRANCHE = ROOT / "artifacts/hilbert-ray-containment-tranche-v1.json"
B5086 = ROOT / "artifacts/b5086-transport-geometry-v1.json"
FINAL_DIRECT = ROOT / "artifacts/final-direct-source-coprime-screen-v1.json"
FROZEN_UNIVERSE = ROOT / "artifacts/frozen-ideal-census-v1.json"
RANGE_AMENDMENT = ROOT / "data/census-paper-preregistration-amendment-v18.json"
Q_ARB = ROOT / "artifacts/census-q-arb-audit-v1.json"
COVER = ROOT / "artifacts/q-euler-deleted-prime-cover-theorem-v1.json"


def require(text: str, snippets: tuple[str, ...]) -> None:
    absent = [snippet for snippet in snippets if snippet not in text]
    if absent:
        raise RuntimeError(f"manuscript missing: {absent}")


def main() -> None:
    source = PAPER.read_text(encoding="utf-8")
    layer0 = json.loads(LAYER0.read_text(encoding="utf-8"))
    q = json.loads(Q_AUDIT.read_text(encoding="utf-8"))
    h = json.loads(H_TAXONOMY.read_text(encoding="utf-8"))
    transport = json.loads(TRANSPORT.read_text(encoding="utf-8"))
    transport_ledger = json.loads(TRANSPORT_LEDGER.read_text(encoding="utf-8"))
    imprimitive = json.loads(IMPRIMITIVE.read_text(encoding="utf-8"))
    b5079 = json.loads(HILBERT_B5079.read_text(encoding="utf-8"))
    tranche = json.loads(HILBERT_TRANCHE.read_text(encoding="utf-8"))
    b5086 = json.loads(B5086.read_text(encoding="utf-8"))
    final_direct = json.loads(FINAL_DIRECT.read_text(encoding="utf-8"))
    frozen = json.loads(FROZEN_UNIVERSE.read_text(encoding="utf-8"))
    amendment = json.loads(RANGE_AMENDMENT.read_text(encoding="utf-8"))
    q_arb = json.loads(Q_ARB.read_text(encoding="utf-8"))
    cover = json.loads(COVER.read_text(encoding="utf-8"))

    split = layer0["structural_trichotomy"]
    require(source, (
        f"|T|={split['T_empty_support']}",
        f"|Q|={split['Q_nonempty_quadratic_support']}",
        f"|H|={split['H_nonempty_higher_order_support']}",
        str(q["chain"]["row_count"]),
        q["chain"]["final_sha256"],
        str(h["counts"]["H_rows"]),
        f"{h['counts']['all_known_mechanisms_fail']:,}",
        str(transport_ledger["counts"]["member_transport_completed"]),
        str(transport_ledger["counts"]["member_transport_open"]),
        "nor a new higher-order packet identity",
        "does not promote another member",
        imprimitive["case_id"],
        f"E_\\chi={imprimitive['exact_result']['E_chi']}",
        f"I_\\chi={imprimitive['exact_result']['I_chi']}",
        "This is a canonical",
        "selected-modulus census",
        "not the full isomorphism-class quotient",
        "The converse is false",
        "346-row value-one",
        "packet-value-orbit polynomial",
        "complete on 2,699 rows",
        "five old quartic constructions remain",
        "not counted as failures",
        "10^{-38}",
        "RQ-006617",
        "census-paper-preregistration-amendment-v18.json",
        "Deleted-prime cover criterion",
        "1,516 deleted",
        "Exactly 699 deleted",
        "[42,0;0,6]",
        "four-support nondegeneracy",
        "q-euler-deleted-prime-cover-theorem-v1.json",
        "10.5281/zenodo.21729947",
    ))
    if (
        cover["status"] != "PASS_PROVED_THEOREM_AND_FINITE_COROLLARY"
        or cover["finite_census_corollary"]["all_zero_rows"] != 346
        or cover["finite_census_corollary"]["row_level_false_positives"] != 0
        or cover["finite_census_corollary"]["row_level_false_negatives"] != 0
        or cover["falsification_result"]["status"] != "REFUTED"
        or cover["falsification_result"]["counterexample"]["finite_norm"] != 252
    ):
        raise RuntimeError("quadratic deleted-prime theorem artifact drifted")
    if (
        frozen["raw_ideal_count"],
        frozen["self_conjugate_raw_count"],
        frozen["nonself_conjugate_raw_count"],
        frozen["deduplicated_case_count"],
    ) != (13939, 2461, 11478, 8200):
        raise RuntimeError("frozen universe count changed")
    if amendment["correction"]["count_identity"] != "2461 + 11478/2 = 8200":
        raise RuntimeError("range correction identity drifted")
    if q_arb["claim_tag"] != "CERTIFIED_NUMERICAL" or q_arb["precision"]["bits"] != 384:
        raise RuntimeError("Q Arb certification boundary drifted")
    if transport["counts"]["member_transport_completed"] != 0:
        raise RuntimeError("immutable v5 scope manifest drifted")
    if transport_ledger["counts"] != {
        "v5_engine_b_rows": 232,
        "member_transport_completed": 12,
        "member_transport_open": 220,
    }:
        raise RuntimeError("Engine-B transport successor ledger drifted")
    completed_transport = [row for row in transport_ledger["members"]
                           if row["transport_status"] == "PROVED_EXACT_MEMBER_TRANSPORT"]
    if sorted(row["case_id"] for row in completed_transport) != [
            "RQ-000039", "RQ-000195", "RQ-000200", "RQ-000205", "RQ-000213",
            "RQ-000221", "RQ-000228",
            "RQ-000425", "RQ-000436", "RQ-000457", "RQ-000459", "RQ-000465"]:
        raise RuntimeError("unexpected Engine-B member promotion")
    if (b5086["claim_tag"], b5086["eligible_count"], len(b5086["records"])) != (
            "PROVED_EXACT_TRANSPORT_GEOMETRY", 0, 7):
        raise RuntimeError("B5-086 no-go screen drifted")
    direct_counts = {row["closure_id"]: row["eligible_count"]
                     for row in final_direct["closures"]}
    if (final_direct["claim_tag"] != "PROVED_EXACT_TRANSPORT_GEOMETRY"
            or direct_counts != {"B5-021": 0, "B5-033": 0}):
        raise RuntimeError("final direct-source no-go screen drifted")
    if (b5079["claim_tag"], b5079["hilbert_field_match_count"],
            b5079["hilbert_field_contained"]) != (
                "PROVED_EXACT_SUBFIELD_TEST", 1, True):
        raise RuntimeError("B5-079 Hilbert containment artifact drifted")
    expected_hilbert = {
        42: ("RQ-001569", 1, True),
        51: ("RQ-001894", 0, False),
        186: ("RQ-007519", 1, True),
    }
    actual_hilbert = {
        row["base_radicand"]: (row["case_id"],
                               row["hilbert_field_match_count"],
                               row["hilbert_field_contained"])
        for row in tranche["records"]
    }
    if (tranche["claim_tag"] != "PROVED_EXACT_SUBFIELD_TEST"
            or actual_hilbert != expected_hilbert):
        raise RuntimeError("Hilbert/ray containment tranche drifted")
    require(source, (
        "bases $35$, $42$, and $186$ contain",
        "base-$51$ closure does not",
        "four frozen normal closures only",
        "neither a Stark unit nor an Artin-labelled packet",
        "hilbert-ray-containment-tranche-v1.json",
    ))
    require(source, (
        "Shintani transfer & 70 & 45 & 117 & 0 & 232",
        "cyclic-quartic CM & 782 & 99 & 0 & 0 & 881",
        "exclusive frontier & 227 & 261 & 1098 & 5 & 1591",
        "total & 1079 & 405 & 1215 & 5 & 2704",
    ))
    rq5298 = next(
        row for row in h["records"] if row["case_id"] == "RQ-005298"
    )
    if (rq5298["legacy_w1_shintani_index"],
            rq5298["genuine_derived_subgroup_order"],
            rq5298["engine_b_route_eligible"]) != (2, 4, False):
        raise RuntimeError("RQ-005298 genuine Engine-B predicate drifted")
    require(source, (
        "RQ-005298",
        "derived-subgroup order",
        "$128/32=4$",
        "actual Engine-B index-two predicate",
    ))
    if not PDF.exists():
        raise RuntimeError("compiled census PDF missing")
    rendered = subprocess.run(
        ["mutool", "draw", "-F", "txt", str(PDF)],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    ).stdout
    require(rendered, (
        "A Certified Canonical Census of One-Place Stark Invariants",
        "canonical selected-modulus census",
        "not the full isomorphism-class quotient",
        "The converse is false",
        "packet-value-orbit polynomial",
        "Exhaustive quadratic stratum",
        "Deleted-prime cover criterion",
        "four-support nondegeneracy",
        "Engine-B transport scope",
        "All proved noncanonical Engine-B member transports",
        "UNSTARTED NO CASE LEVEL PACKET CLAIM",
        "A worked imprimitive row",
        "RQ-005298",
        "128/32 = 4",
        "base-51 closure does not",
        "RQ-000039",
        "RQ-000195",
        "RQ-000221",
        "RQ-000228",
        "B5-022",
        "B5-086 direct-source closure shares source prime 11",
        "B5-021 and B5-033 admit no integral",
        "10.5281/zenodo.21729947",
    ))
    print("CENSUS_PAPER_AUDIT=PASS")


if __name__ == "__main__":
    main()
