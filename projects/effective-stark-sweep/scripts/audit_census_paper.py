#!/usr/bin/env python3
"""Check that the census manuscript states only frozen artifact facts."""

from __future__ import annotations

import hashlib
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
TRANSPORT_LEDGER = ROOT / "artifacts/engine-b-transport-ledger-v5.json"
IMPRIMITIVE = ROOT / "artifacts/rq000013-engine-a-imprimitive-certificate-v1.json"
HILBERT_B5079 = ROOT / "artifacts/b5079-hilbert-ray-containment-v1.json"
HILBERT_TRANCHE = ROOT / "artifacts/hilbert-ray-containment-tranche-v1.json"
GLOBAL_COPRIME = ROOT / "artifacts/engine-b-global-coprime-geometry-audit-v1.json"
FROZEN_UNIVERSE = ROOT / "artifacts/frozen-ideal-census-v1.json"
RANGE_AMENDMENT = ROOT / "data/census-paper-preregistration-amendment-v18.json"
Q_ARB = ROOT / "artifacts/census-q-arb-audit-v1.json"
COVER = ROOT / "artifacts/q-euler-deleted-prime-cover-theorem-v1.json"
V5 = ROOT / "artifacts/full-census-yield-declaration-v5.json"
V5_SCRIPT = ROOT / "scripts/declare_census_v5.py"
SEXTIC_FIELDS = ROOT / "artifacts/roblot-sextic-field-inventory-v1.json"
SEXTIC_3CLASS = ROOT / "artifacts/roblot-sextic-3class-v1.json"


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
    global_coprime = json.loads(GLOBAL_COPRIME.read_text(encoding="utf-8"))
    frozen = json.loads(FROZEN_UNIVERSE.read_text(encoding="utf-8"))
    amendment = json.loads(RANGE_AMENDMENT.read_text(encoding="utf-8"))
    q_arb = json.loads(Q_ARB.read_text(encoding="utf-8"))
    cover = json.loads(COVER.read_text(encoding="utf-8"))
    v5 = json.loads(V5.read_text(encoding="utf-8"))
    sextic_fields = json.loads(SEXTIC_FIELDS.read_text(encoding="utf-8"))
    sextic_3class = json.loads(SEXTIC_3CLASS.read_text(encoding="utf-8"))

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
        "10.5281/zenodo.21730707",
        "2461+5739=8200",
        "(iii) and (iv)",
        "Prop.~4 and Eq.~(9)",
        "no doubly assigned row",
        "not a general theorem",
        "Of those 382, 309 complete",
        "48 reuse full \\texttt{bnfcertify}",
        "261",
        "remaining 73",
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
        v5["histogram"]["ENGINE_B_ELIGIBLE"] != 232
        or v5["histogram"]["ENGINE_C_ELIGIBLE"] != 881
        or hashlib.sha256(V5_SCRIPT.read_bytes()).hexdigest()
        != v5["source_hashes"]["scripts/declare_census_v5.py"]
        or "engine populations overlap" not in V5_SCRIPT.read_text()
    ):
        raise RuntimeError("v5 disjoint assignment audit drifted")
    if (
        sextic_fields["counts"]["required_distinct_field_keys"] != 382
        or sextic_fields["counts"]["reused_sequential_field_certificates"] != 48
        or sextic_fields["counts"]["new_deduplicated_field_screens"] != 334
        or sextic_fields["counts"]["status"] != {
            "EXACT_FIELD_GATES_COMPLETE": 309,
            "NEEDS_STRONG_3_CLASS_CERTIFICATE": 73,
        }
        or sextic_3class["counts"]["residual_fields"] != 73
        or sextic_3class["counts"]["failures"] != 0
    ):
        raise RuntimeError("sextic field-certificate partition drifted")
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
        "member_transport_completed": 22,
        "member_transport_open": 210,
    }:
        raise RuntimeError("Engine-B transport successor ledger drifted")
    completed_transport = [row for row in transport_ledger["members"]
                           if row["transport_status"] == "PROVED_EXACT_MEMBER_TRANSPORT"]
    if len(completed_transport) != 22 or not {"RQ-002079", "RQ-002964", "RQ-002983", "RQ-001115", "RQ-001125", "RQ-001132", "RQ-001133", "RQ-001149", "RQ-001164", "RQ-001172"} <= {row["case_id"] for row in completed_transport}:
        raise RuntimeError("unexpected Engine-B member promotion")
    if (global_coprime["status"] != "PASS_EXACT_GEOMETRY_CLASSIFICATION"
            or global_coprime["open_member_partition"]["route_obstructed_direct_coprime"] != 116
            or global_coprime["open_member_partition"]["source_or_proof_open"] != 104):
        raise RuntimeError("global direct-source geometry screen drifted")
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
        "First twelve proved noncanonical Engine-B member transports",
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
        "earlier B5-086/B5-021/B5-033 direct-source exclusions used",
        "116 have no incoming direct coprime-deletion direction",
        "104 retained a",
        "10.5281/zenodo.21730707",
        "2461 + 5739 = 8200",
        "equivalence of (iii) and",
        "(iv). The companion paper",
        "finds no doubly",
        "assigned row in this finite corpus",
    ))
    print("CENSUS_PAPER_AUDIT=PASS")


if __name__ == "__main__":
    main()
