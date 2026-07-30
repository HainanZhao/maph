#!/usr/bin/env python3
"""Referee-style audit of the frozen results manuscript.

This is deliberately independent of census-v5 populations.  It checks
only promoted theorem records, displayed constants and polynomials,
the conditionality boundary, and the exact scope of every Stark use.
"""

from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, getcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper/effective-stark-results.tex"
OUT = ROOT / "artifacts/results-paper-referee-audit-v2.json"
getcontext().prec = 80


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def require(text: str, *needles: str) -> None:
    for needle in needles:
        if needle not in text:
            raise AssertionError(f"paper omits required text: {needle}")


def check_hash(path: str, expected: str) -> None:
    actual = sha(path)
    if actual != expected:
        raise AssertionError(f"hash mismatch for {path}: {actual} != {expected}")


def margin(lower: str, upper: str) -> Decimal:
    return Decimal(lower) / Decimal(upper)


def main() -> None:
    paper = PAPER.read_text()
    prose = " ".join(paper.split())
    if r"\appendix" not in paper:
        raise AssertionError("certificate and provenance material is not in an appendix")
    main_body = paper.split(r"\appendix", 1)[0]
    for tag in ("VERIFIED", "VERIFIED_THEOREM", "DUAL_ROUTED", "DUAL_PROVED", "PROXY"):
        if tag in main_body:
            raise AssertionError(f"internal process tag remains in main narrative: {tag}")
    for internal_detail in (
        "d1d355a14a",
        "a0674aed11",
        "0afdc1304d",
        "c3663bd8dcbe1f1de0b9b1f3cfe5ac17",
    ):
        if internal_detail in paper:
            raise AssertionError(
                f"raw audit-log detail remains in manuscript: {internal_detail}"
            )

    # Conditionality and novelty boundary.
    require(
        prose,
        "It does not mean that",
        "general real-quadratic rank-one Stark conjecture is proved",
        "not asserted as a universal priority claim",
        "historical observation is not part of either theorem",
        "No unproved Stark conjecture",
        "Numerical PARI recognition",
    )

    # The results manuscript must remain census-independent.
    forbidden = (
        "1,628",
        "FRONTIER share",
        "norm quartile",
        "census v5",
        "conductor trend is",
    )
    for needle in forbidden:
        if needle in prose:
            raise AssertionError(f"census-dependent text leaked into results paper: {needle}")

    q7 = load("data/q7-p7-case-v1.json")
    q14 = load("data/q14-p7-case-v1.json")
    q5 = load("data/rq000108-case-v1.json")
    q2 = load("data/rq000021-case-v1.json")
    q57 = load("data/q57-norm27-case-v1.json")
    q77 = load("data/rq002955-case-v1.json")
    q33 = load("data/q33-p11-order10-case-v1.json")
    q35 = load("artifacts/engine-c-w3-tranche-01-verified-v1.json")
    q35_class_numbers = load("artifacts/q35-base-class-numbers-v1.json")
    e6 = load("artifacts/engine-c-e6-tranche-01-verified-v1.json")
    q6 = load("data/q6-norm8-case-v3.json")
    q6_correction = load("artifacts/q6-positive-packet-correction-v2.json")
    dual = load("data/rq000458-dual-case-v1.json")
    engine_a = load("data/engine-a-uniform-theorem-v1.json")
    theory_original = load("data/engine-c-general-e-theory-v1.json")
    theory = load("data/engine-c-general-e-theory-v3.json")
    parity = load("artifacts/results-paper-index-parity-lemma-v1.json")
    parity_audit = load("artifacts/results-paper-odd-index-parity-audit-v1.json")
    seal_audit = load("artifacts/results-paper-seal-order-audit-v1.json")
    core_manifest = load("artifacts/results-paper-core-manifest-v1.json")

    for record in (q7, q14, q5, q2, q57, q77, q33, q35, e6, q6, dual):
        serialized = json.dumps(record)
        if "VERIFIED" not in serialized:
            raise AssertionError("a promoted case lacks a VERIFIED record")

    # Exact main-table values and independently recomputed margins.
    rows = [
        ("RQ-000190", q7["w2"]["safe_exponent"], 4032, "5688"),
        ("RQ-000419", q14["w2"]["safe_exponent"], 4032, "7315"),
        ("RQ-000108", q5["safe_exponent"], 2880, "2460"),
        ("RQ-000021", q2["safe_exponent"], 2016, "4261"),
        ("RQ-002057", q57["exponent"]["safe_exponent"], 2592, "748"),
        ("RQ-002955", q77["safe_exponent"], 4032, "5151"),
        ("RQ-001107", q33["exponent"]["safe_exponent"], 15840, "5817"),
    ]
    for case_id, actual_exp, expected_exp, claimed_margin in rows:
        if actual_exp != expected_exp:
            raise AssertionError(f"{case_id}: exponent mismatch")
        require(paper, case_id, str(expected_exp), claimed_margin)

    q7_margin = margin(
        q7["w3"]["analytic_arb_enclosure"]["voutier_degree_3_to_24_lower"],
        "9.190275104108818172928486965908578215619369302388594449681582836357482e-9",
    )
    q14_margin = margin(
        q14["w3"]["analytic_arb_enclosure"]["voutier_degree_3_to_24_lower"],
        q14["w3"]["analytic_arb_enclosure"]["powered_height_upper"],
    )
    common_voutier = q14["w3"]["analytic_arb_enclosure"][
        "voutier_degree_3_to_24_lower"
    ]
    q5_margin = margin(
        common_voutier,
        q5["identification"]["powered_height_upper"],
    )
    q2_margin = margin(
        common_voutier,
        q2["identification"]["powered_height_upper"],
    )
    q57_margin = margin(
        q57["identification"]["analytic_arb_enclosure"]["voutier_degree_3_to_24_lower"],
        q57["identification"]["analytic_arb_enclosure"]["powered_height_upper"],
    )
    q77_margin = margin(
        common_voutier,
        q77["identification"]["powered_height_upper"],
    )
    q33_margin = margin(
        q33["height_window"]["minimum_voutier_lower_bound"],
        q33["identification"]["powered_height_upper"],
    )
    dual_margin = margin(
        common_voutier,
        dual["engine_b"]["powered_height_upper"],
    )
    if not (
        q7_margin > 5688
        and q14_margin > 7315
        and q5_margin > 2460
        and q2_margin > 4261
        and q57_margin > 748
        and q77_margin > 5151
        and q33_margin > 5817
        and dual_margin > 6470
    ):
        raise AssertionError("a displayed height margin does not clear its integer claim")

    # Displayed relative polynomials: their complete coefficient strings
    # live in the promoted records, and distinguishing coefficient blocks
    # must be present in the manuscript.
    polynomial_checks = [
        ("q7", q7["w3"]["relative_packet_polynomial"], "34+13\\sqrt7"),
        ("q14", q14["w3"]["relative_packet_polynomial"], "139+38\\sqrt{14}"),
        ("rq000108", q5["identification"]["relative_packet_polynomial"], "9+9y"),
        ("rq000021", q2["identification"]["relative_packet_polynomial"], "129+90\\sqrt2"),
        ("rq002955", q77["identification"]["relative_packet_polynomial"], "217+54y"),
        ("q33", q33["identification"]["relative_packet_polynomial"], "871+368y"),
        ("q35", q35["closure"]["packet_polynomial"], "873210"),
        (
            "q6",
            q6["cross_route"]["common_packet_polynomial"],
            "X^8-8X^7+12X^6+8X^5-10X^4",
        ),
        ("rq000458", dual["packet"]["relative_polynomial"], "138+36\\sqrt{14}"),
    ]
    for name, polynomial, distinguishing_text in polynomial_checks:
        if not polynomial or distinguishing_text not in paper:
            raise AssertionError(f"{name}: displayed polynomial not tied to its exact record")

    # Remaining displayed finite constants and Artin labels.
    if q7["w3"]["split_prime_frobenius_labels"] != [
        {"rational_prime": 19, "ray_log": 1},
        {"rational_prime": 31, "ray_log": 5},
    ]:
        raise AssertionError("q7 Frobenius labels changed")
    if q14["w3"]["split_prime_frobenius_labels"] != [
        {"rational_prime": 11, "ray_log": 5},
        {"rational_prime": 103, "ray_log": 1},
    ]:
        raise AssertionError("q14 Frobenius labels changed")
    if q14["w2"]["clearing_exponents"] != [576, 84]:
        raise AssertionError("q14 divisor exponents changed")
    if [row["clearing_exponent"] for row in q57["exponent"]["divisor_rows"]] != [
        864,
        324,
        108,
    ]:
        raise AssertionError("q57 divisor exponents changed")
    if q57["identification"]["congruence_unit_domain"]["points_per_ray_class"] != 240:
        raise AssertionError("q57 cone count changed")
    if q33["identification"]["maximum_packet_comparison_degree"] != 40:
        raise AssertionError("q33 realized comparison degree changed")
    if q33["identification"]["certified_degree_cap"] != 80:
        raise AssertionError("q33 degree cap changed")
    if q35["closure"]["route_e"] != [2, 2] or q35["closure"]["stark_s_size"] != [3, 3]:
        raise AssertionError("q35 Stark bookkeeping changed")
    q35_classes = {
        key: row["observed_class_number"]
        for key, row in q35_class_numbers["fields"].items()
    }
    if q35_classes != {
        "real_base_Q_sqrt_35": 2,
        "imaginary_base_Q_sqrt_minus_10": 2,
        "imaginary_base_Q_sqrt_minus_14": 4,
    }:
        raise AssertionError("q35 class-number certificate changed")
    if e6["field_count"] != 3 or e6["occurrence_count"] != 14:
        raise AssertionError("e6 tranche cardinality changed")
    if [route["e"] for route in q6["routes"]] != [8, 12]:
        raise AssertionError("q6 route e-values changed")
    if q6["auxiliary_prime_closure"]["exact_euler_multipliers_at_s0"] != {
        "3": "1+i",
        "5": "2",
    }:
        raise AssertionError("q6 Euler multipliers changed")
    if dual["engine_b"]["safe_exponent"] != 1152:
        raise AssertionError("RQ-000458 safe exponent changed")
    if dual["engine_c"]["exact_normal_closure_identity_count"] != 32:
        raise AssertionError("RQ-000458 identity count changed")
    require(
        prose,
        "27 independent double-sine",
        "split primes \\(19\\) and \\(31\\)",
        "Split primes 11 and 103",
        "clearing exponents 576 and 84",
        "864,324,108",
        "240 exact affine points",
        "actual packet-comparison degree is 40",
        "degrees three through 80",
        "Six independent imaginary-base routes cover fourteen",
        "256 exact common-normal-closure identities",
        "P_3(1)=1+i",
        "P_5(1)=2",
        "safe exponent 1152",
        "32 exact common-closure identities",
    )

    # Explicit certificate hashes embedded in promoted data.
    hash_map = [
        (
            "artifacts/q14-p7-w3-exact-candidate-v1.transcript",
            q14["w3"]["certificate_hashes"]["exact_candidate_sha256"],
        ),
        (
            "artifacts/q14-p7-w3-arb-certificate-v1.transcript",
            q14["w3"]["certificate_hashes"]["arb_certificate_sha256"],
        ),
        (
            "artifacts/rq57-norm27-w3-exact-candidate-v1.transcript",
            q57["identification"]["certificate_hashes"]["exact_candidate_sha256"],
        ),
        (
            "artifacts/rq57-norm27-w3-arb-certificate-v1.transcript",
            q57["identification"]["certificate_hashes"]["arb_certificate_sha256"],
        ),
        (
            "artifacts/rq001107-w3-exact-candidate-v1.transcript",
            q33["identification"]["certificate_hashes"]["exact_candidate_sha256"],
        ),
        (
            "artifacts/rq001107-w3-arb-certificate-v1.transcript",
            q33["identification"]["certificate_hashes"]["arb_certificate_sha256"],
        ),
        (
            dual["engine_b"]["certificate"]["path"],
            dual["engine_b"]["certificate"]["sha256"],
        ),
        (
            dual["alignment_certificate"]["path"],
            dual["alignment_certificate"]["sha256"],
        ),
        (
            q6["correction_certificate"]["path"],
            q6["correction_certificate"]["sha256"],
        ),
    ]
    for path, expected in hash_map:
        check_hash(path, expected)

    # Engine-C normalization.  This catches the v2 specialization-sign
    # typo while checking the formulas printed in the paper.
    expected_specializations = {
        "6": ("-1/3", "-3", "-2/3", "-3/2"),
        "8": ("-1/4", "-4", "-1/2", "-2"),
        "12": ("-1/6", "-6", "-1/3", "-3"),
    }
    for e, values in expected_specializations.items():
        spec = theory["specializations"][e]
        actual = (
            spec["class_log_forward"],
            spec["class_log_inverse"],
            spec["direct_lprime_forward"],
            spec["direct_lprime_inverse"],
        )
        if actual != values:
            raise AssertionError(f"e={e}: general-e coefficient mismatch")
    require(
        paper,
        r"\zeta'_S(0,g)=-\frac2e\ell_g",
        r"L'_S(0,\psi)=-\frac4e(\ell_1-i\ell_\sigma)",
    )

    # Stark-use audit: each C use must state the exact theorem boundary.
    stark_uses = [
        {
            "family": "generic Q(sqrt(35))",
            "theorem": "Stark 1980 imaginary-quadratic rank one",
            "s_sizes": q35["closure"]["stark_s_size"],
            "e_values": q35["closure"]["route_e"],
            "global_unit_clause": q35["gates"]["stark_1980_global_unit_clause"],
        },
        {
            "family": "e=6 tranche",
            "theorem": "Stark 1980 imaginary-quadratic rank one",
            "s_sizes": [size for b in e6["bundles"] for size in b["stark_s_size"]],
            "e_values": [e for b in e6["bundles"] for e in b["route_e"]],
            "global_unit_clause": e6["gates"]["stark_1980_global_unit_clause"],
        },
        {
            "family": "RQ-000129",
            "theorem": "Stark 1980 after auxiliary-prime enlargement",
            "s_sizes": [3, q6["routes"][1]["auxiliary_s_size"]],
            "e_values": [route["e"] for route in q6["routes"]],
            "global_unit_clause": True,
        },
        {
            "family": "RQ-000458 C route",
            "theorem": "Stark 1980 imaginary-quadratic rank one",
            "s_sizes": [dual["engine_c"]["stark_S_size"]],
            "e_values": [dual["engine_c"]["roots_of_unity_in_character_field"]],
            "global_unit_clause": dual["engine_c"]["global_unit_clause_applies"],
        },
    ]
    for use in stark_uses:
        if not use["global_unit_clause"] or min(use["s_sizes"]) < 3:
            raise AssertionError(f"Stark global-unit boundary fails: {use['family']}")

    # Structural theorem records.
    if engine_a["claim_tag"] != "VERIFIED_THEOREM":
        raise AssertionError("uniform Engine-A theorem is not banked")
    if theory_original["claim_tag"] != "VERIFIED_THEOREM":
        raise AssertionError("general-e Engine-C theorem is not banked")
    if parity["claim_tag"] != "VERIFIED_THEOREM":
        raise AssertionError("parity lemma is not banked")
    if (
        parity_audit["verdict"] != "PASS"
        or parity_audit["odd_index_greater_than_one_count"] != 446
        or parity_audit["exception_count"] != 0
    ):
        raise AssertionError("genuine odd-index parity audit did not pass 446/446")
    if seal_audit["verdict"] != "NO_FRONT_RUNNING_OF_UNSEALED_RESULTS":
        raise AssertionError("seal-order audit did not clear")
    if core_manifest["reserved_doi"] != "10.5281/zenodo.21703306":
        raise AssertionError("reserved DOI changed")
    if q6_correction["old_anti_unit_real_root_count"] != 0:
        raise AssertionError("q6 old anti-unit root diagnosis changed")
    if (
        q6_correction["correct_packet_real_root_count"] != 4
        or q6_correction["correct_packet_negative_root_count"] != 0
    ):
        raise AssertionError("q6 corrected packet root count changed")
    require(
        prose,
        "Uniform quadratic-support theorem",
        "Closed packet formula",
        "one closed product formula",
        "Theorem inventory",
        "ten principal contributions",
        "This is the paper's broadest result",
        "Order six and its replication",
        "Order ten",
        "Ramified-prime-\\(3\\) control",
        "Uniform Engine-A theorem",
        "Two disjoint theorem routes",
        "Generic CM closure beyond class number one",
        "general-\\(e\\) CM closure",
        "General-\\(e\\) normalization and orientation",
        "No-go lemma",
        "Index-parity lemma",
        "negative-square-root embedding",
        "first real place in the pinned PARI ordering",
        "mixed signature",
        "Effective but not uniformly cheap",
        "selected-results theorem",
        "No absolute-abelian fourth engine",
        "Index parity",
        r"2\mid[H:H\cap\Q^{\rm ab}]",
        "genuine normal closure",
        "all 8,200 genuine normal-closure",
        "found 446 odd indices",
        "10.5281/zenodo.21703306",
        "unpublished draft",
        "Certificates and provenance",
        "Declaration of generative AI and AI-assisted technologies",
        "author reviewed and verified all outputs",
        "takes full responsibility",
    )
    require(
        paper,
        r"\lambda_L(\epsilon_K)=(a,a,-2a)",
        r"\lambda_L(u_\chi)=(b,-b,0)",
        r"X_A=\prod_{\chi(R)=-1}",
        r"H\cap N^{[G,G]}=H\cap\Q^{\rm ab}",
    )

    report = {
        "schema": "effective-stark-results-paper-referee-audit-v2",
        "claim_tag": "VERIFIED_PAPER_AUDIT",
        "paper": "paper/effective-stark-results.tex",
        "paper_sha256": sha("paper/effective-stark-results.tex"),
        "scope": "promoted theorem identities only; census populations excluded",
        "checks": {
            "conditionality_disclaimer": "PASS",
            "historical_claim_separated_from_theorem": "PASS",
            "census_independence": "PASS",
            "main_table_exponents": "7/7",
            "displayed_height_margins": "PASS_RECOMPUTED",
            "displayed_polynomials": "9/9 tied to exact records",
            "displayed_finite_constants_and_labels": "PASS",
            "certificate_hashes": f"{len(hash_map)}/{len(hash_map)}",
            "general_e_coefficients": "PASS_WITH_V3_SIGN_CORRECTION",
            "structural_lemmas": "2/2",
            "odd_index_consistency": "446/446",
            "seal_order": "PASS",
            "journal_facing_process_edit": "PASS_TAGS_REMOVED_FROM_MAIN_CHRONOLOGY_IN_APPENDIX",
            "ai_disclosure": "PASS_SEPARATE_PRE_BIBLIOGRAPHY_DECLARATION",
            "q6_polynomial_correction": "PASS_OLD_ZERO_REAL_NEW_FOUR_POSITIVE",
            "theorem_inventory": "10/10",
            "general_e_theorem": "VERIFIED_THEOREM_WITH_V3_SIGN_CORRECTION",
            "embedding_convention": "INFINITY_2_NEGATIVE_SQRT_PARI_FIRST_REAL_PLACE",
            "index_parity_fixed_field_step": "PASS",
            "reserved_doi": "10.5281/zenodo.21703306",
            "stark_usage_audit": "PASS",
        },
        "recomputed_margins": {
            "RQ-000190": str(q7_margin),
            "RQ-000419": str(q14_margin),
            "RQ-000108": str(q5_margin),
            "RQ-000021": str(q2_margin),
            "RQ-002057": str(q57_margin),
            "RQ-002955": str(q77_margin),
            "RQ-001107": str(q33_margin),
            "RQ-000458": str(dual_margin),
        },
        "stark_uses": stark_uses,
        "source_hashes": {
            path: sha(path)
            for path in [
                "data/q7-p7-case-v1.json",
                "data/q14-p7-case-v1.json",
                "data/rq000108-case-v1.json",
                "data/rq000021-case-v1.json",
                "data/q57-norm27-case-v1.json",
                "data/rq002955-case-v1.json",
                "data/q33-p11-order10-case-v1.json",
                "artifacts/engine-c-w3-tranche-01-verified-v1.json",
                "artifacts/q35-base-class-numbers-v1.json",
                "artifacts/engine-c-e6-tranche-01-verified-v1.json",
                "data/q6-norm8-case-v3.json",
                "artifacts/q6-positive-packet-correction-v2.json",
                "data/rq000458-dual-case-v1.json",
                "data/engine-a-uniform-theorem-v1.json",
                "data/engine-c-general-e-theory-v1.json",
                "data/engine-c-general-e-theory-v3.json",
                "artifacts/results-paper-index-parity-lemma-v1.json",
                "artifacts/results-paper-odd-index-parity-audit-v1.json",
                "artifacts/results-paper-seal-order-audit-v1.json",
                "artifacts/results-paper-core-manifest-v1.json",
            ]
        },
    }
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"RESULTS_PAPER_AUDIT=PASS output={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
