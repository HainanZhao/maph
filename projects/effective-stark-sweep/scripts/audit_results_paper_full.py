#!/usr/bin/env python3
"""Referee audit for the complete A/B/C major-revision manuscript."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from decimal import Decimal, getcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper/effective-stark-results.tex"
SUPPLEMENT = ROOT / "paper/effective-stark-results-supplement.tex"
OUT = ROOT / "artifacts/results-paper-referee-audit-v3.json"
getcontext().prec = 80


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def require(text: str, *needles: str) -> None:
    for needle in needles:
        if needle not in text:
            raise AssertionError(f"manuscript omits required text: {needle}")


def reject(text: str, *needles: str) -> None:
    for needle in needles:
        if needle in text:
            raise AssertionError(f"manuscript retains superseded claim: {needle}")


def run(command: list[str], verdict: str) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode or verdict not in completed.stdout:
        raise AssertionError(
            f"{' '.join(command)} failed:\n"
            + completed.stdout
            + completed.stderr
        )
    return completed.stdout


def margin(lower: str, upper: str) -> Decimal:
    return Decimal(lower) / Decimal(upper)


def main() -> None:
    paper = PAPER.read_text()
    supplement = SUPPLEMENT.read_text()
    prose = " ".join(paper.split())
    supplement_prose = " ".join(supplement.split())
    main_body = paper.split(r"\appendix", 1)[0]

    # The complete paper must contain the three mechanisms and the written
    # bridges; auxiliary data cannot substitute for these statements.
    require(
        paper,
        r"\begin{proposition}[Explicit quadratic formula]",
        r"\begin{proposition}[Shintani transfer in one-place notation]",
        r"\begin{lemma}[All-embeddings height rigidity]",
        r"\begin{theorem}[Cyclic-quartic CM norm bridge]",
        r"\begin{theorem}[Selected cyclic-quartic CM packets]",
        r"\begin{lemma}[Absolutely abelian ray fields]",
        r"\begin{lemma}[Index parity]",
        r"Y_{\bar A}",
        r"\operatorname{Ind}_{G_K}^{G_\Q}\theta",
        r"L_{\mathfrak m}(s,\theta)=L_S(s,\psi)",
        r"\varepsilon=u^{e/2}",
        r"Y_{\bar s^r}",
        r"N_{E/E^+}(\sigma^ru)^{-1}",
        r"\zeta'_S(0,g)=-\frac2e\ell_g",
        r"L'_S(0,\psi)",
        r"=-\frac4e(\ell_1+i\ell_\sigma)",
        r"\frac1m\log|\sigma_v(X_A^m)|",
        r"j(E)=E,\qquad j|_k\ne1",
        r"Put \(E^+=E^{\langle j\rangle}\)",
        r"\phantomsection\label{par:conventions}",
        r"\theta(\bar s)=i",
        r"\psi(\sigma)=i",
        r"\label{eq:index-parity}",
        r"\label{sec:rq458}",
        r"\section{Exact finite moduli}\label{app:moduli}",
        r"\begin{center}\footnotesize",
    )
    require(
        prose,
        "Global complex conjugation is a different automorphism",
        "Scalar twists are not permitted",
        "Equality of unlabeled polynomials is never the bridge",
        "not used in the theorem",
        "The theorem claim for this row rests solely on Engine B",
        "We therefore make no claim to the first unconditional weak Stark result",
        "componentwise Artin-labelled identification",
        "RQ-002057: the prime above \\(3\\) has relative ramification index",
        r"Tate \cite[Thm.~IV.5.4]{Tate1984}",
        r"Arakawa's relative-index formula",
        "Thus the algebraicity underlying Engine~A is classical",
        "algorithmically closed stratum",
        "with no analytic enclosure, safe exponent, or height comparison",
        "The dominant per-character cost is one quartic-field call",
        r"\(2\times2\) determinant",
        r"\(2^{r_\chi}\)",
        "packet minimal polynomial is obtained by an exact resultant",
        "exhaustively verifiable rather than sampled",
        "quadratic Fourier slice can be evaluated and removed exactly",
        "higher-order residual",
        "Roblot's (A4) is not a hypothesis of these existence theorems",
        "It is not an application of Roblot's squareness criteria",
        "explicitly excludes imaginary quadratic bases",
        "https://doi.org/10.5281/zenodo.21708121",
        "PDF and",
        "source are exposed as top-level files",
        "Shintani's Proposition~4 on pp.~154--156",
        "Shintani's Proposition~5(i)--(iii) on pp.~156--158",
        "stated for every degree",
        "complete the proof of Theorem",
        "Supplementary Table~S1",
        "Supplementary Table~S2",
        "Supplementary Table~S3",
        r"\cite{Zhao45}",
        r"\cite{Zhao78}",
        r"J.\ Number Theory \textbf{133} (2013), 1045--1061",
        "support order ten",
    )
    reject(
        main_body,
        "General-\\(e\\) CM normalization and orientation",
        "proved through the \\(e=8\\) and \\(e=12\\) CM routes",
        "DUAL_PROVED",
        "DUAL_ROUTED",
        "X^8+24X^7+732X^6",
        r"\left|\log|X_A|_v-\log|\alpha_A|_v\right|",
        "so these are apparently the first examples",
        r"Put \(E^+=E^{\langle j\rangle}\) inside the common normal closure",
        r"\tag{",
        r"e=|\mu(E)|=2,4,6,8",
        "1022--1045",
        r"\ell_1-i\ell_\sigma",
        r"\sigma^{-r}u",
        r"\begin{center}\scriptsize",
        "support orders six or ten",
    )
    require(
        supplement_prose,
        "Supplementary Table S1: certificate record map",
        "Supplementary Table S2: complete Artin-label interval replay",
        "Supplementary Table S3: relation to Roblot's sextic theorem",
        "Roblot's (A4) is not part of the existence statement",
        "neither assumed nor silently included",
        r"\path{data/q7-p7-case-v1.json}",
        r"\path{artifacts/engine-c-fourier-convention-correction-v1.json}",
        r"\path{artifacts/roblot-sextic-overlap-audit-v1.json}",
        "672 zero Euler products",
        "affecting 603 rows",
        "In 346 rows every supported derivative vanishes",
    )
    reject(
        main_body,
        r"\path{data/q7-p7-case-v1.json}",
        "672 such characters among 2,232",
        "affecting 603 rows",
    )

    # Engine A: the closed formula includes exact imprimitive
    # degeneracies, which are audited over the frozen queue.
    euler_output = run(
        ["python3", "scripts/audit_engine_a_euler_degeneracy.py"],
        "ENGINE_A_EULER_DEGENERACY_AUDIT=VERIFIED",
    )
    euler = load("artifacts/engine-a-euler-degeneracy-v1.json")
    expected_euler = {
        "case_count": 1560,
        "supported_quadratic_character_count": 2232,
        "characters_with_zero_euler_product": 672,
        "cases_with_zero_euler_product": 603,
        "cases_with_all_supported_euler_products_zero": 346,
    }
    if any(euler.get(key) != value for key, value in expected_euler.items()):
        raise AssertionError("Engine-A Euler-degeneracy counts changed")

    # Prior-work boundary: test Roblot's sextic hypotheses on all five
    # selected order-six ray fields.
    roblot_output = run(
        ["gp", "-q", "scripts/audit_roblot_sextic_overlap.gp"],
        "ROBLOT_SEXTIC_OVERLAP_AUDIT=PASS",
    )
    roblot = load("artifacts/roblot-sextic-overlap-audit-v1.json")
    roblot_cases = {row["case_id"]: row for row in roblot["cases"]}
    expected_roblot = {
        "RQ-000190": True,
        "RQ-000419": True,
        "RQ-000021": True,
        "RQ-002057": False,
        "RQ-002955": True,
    }
    if set(roblot_cases) != set(expected_roblot):
        raise AssertionError("Roblot overlap case set changed")
    for case_id, applies in expected_roblot.items():
        row = roblot_cases[case_id]
        if (
            not all(row[key] for key in ("A1", "A2", "A3"))
            or row["class_number_H"] != 1
            or row["roblot_theorem_7_1_applies"] is not applies
        ):
            raise AssertionError(f"Roblot overlap changed for {case_id}")
    if (
        not roblot_cases["RQ-002057"]["wild_above_3"]
        or roblot_cases["RQ-002057"]["relative_ramification_index_above_3"]
        != 6
    ):
        raise AssertionError("RQ-002057 wild-3 boundary changed")

    # Engine B: all eight selected rows and their exact root geometry.
    q7 = load("data/q7-p7-case-v1.json")
    q14 = load("data/q14-p7-case-v1.json")
    q5 = load("data/rq000108-case-v1.json")
    q2 = load("data/rq000021-case-v1.json")
    q57 = load("data/q57-norm27-case-v1.json")
    q77 = load("data/rq002955-case-v1.json")
    q33 = load("data/q33-p11-order10-case-v1.json")
    dual = load("data/rq000458-dual-case-v1.json")
    common_v = q14["w3"]["analytic_arb_enclosure"][
        "voutier_degree_3_to_24_lower"
    ]
    b_rows = {
        "RQ-000190": (
            q7["w2"]["safe_exponent"],
            Decimal(q7["w3"]["analytic_arb_enclosure"][
                "voutier_degree_3_to_24_lower"
            ])
            / Decimal(q7["w3"]["analytic_arb_enclosure"][
                "powered_height_upper"
            ]),
            Decimal(5688),
        ),
        "RQ-000419": (
            q14["w2"]["safe_exponent"],
            margin(common_v, q14["w3"]["analytic_arb_enclosure"][
                "powered_height_upper"
            ]),
            Decimal(7315),
        ),
        "RQ-000108": (
            q5["safe_exponent"],
            margin(common_v, q5["identification"]["powered_height_upper"]),
            Decimal(2460),
        ),
        "RQ-000021": (
            q2["safe_exponent"],
            margin(common_v, q2["identification"]["powered_height_upper"]),
            Decimal(4261),
        ),
        "RQ-002057": (
            q57["exponent"]["safe_exponent"],
            margin(
                q57["identification"]["analytic_arb_enclosure"][
                    "voutier_degree_3_to_24_lower"
                ],
                q57["identification"]["analytic_arb_enclosure"][
                    "powered_height_upper"
                ],
            ),
            Decimal(748),
        ),
        "RQ-002955": (
            q77["safe_exponent"],
            margin(common_v, q77["identification"]["powered_height_upper"]),
            Decimal(5151),
        ),
        "RQ-001107": (
            q33["exponent"]["safe_exponent"],
            margin(
                q33["height_window"]["minimum_voutier_lower_bound"],
                q33["identification"]["powered_height_upper"],
            ),
            Decimal(5817),
        ),
        "RQ-000458": (
            dual["engine_b"]["safe_exponent"],
            margin(common_v, dual["engine_b"]["powered_height_upper"]),
            Decimal(6470),
        ),
    }
    expected_exponents = [4032, 4032, 2880, 2016, 2592, 4032, 15840, 1152]
    for (case_id, (exponent, actual_margin, claim)), expected in zip(
        b_rows.items(), expected_exponents, strict=True
    ):
        if exponent != expected or actual_margin <= claim:
            raise AssertionError(f"{case_id}: B-row arithmetic failed")
        require(paper, case_id, str(exponent), f">{claim}")

    arch_output = run(
        ["gp", "-q", "scripts/certify_engine_b_archimedean_places.gp"],
        "ENGINE_B_ARCHIMEDEAN_PLACE_AUDIT=VERIFIED",
    )
    arch_record = load("artifacts/engine-b-archimedean-place-audit-v1.json")
    if (
        arch_record["verdict"] != "VERIFIED_EXACT_ALL_EIGHT"
        or len(arch_record["cases"]) != 8
        or arch_record["script"]["sha256"]
        != sha("scripts/certify_engine_b_archimedean_places.gp")
    ):
        raise AssertionError("Engine-B archimedean audit record is stale")

    # Engine C: replay the corrected e=6 primitive bridge and audit all
    # theorem rows against their exact records.
    correction_output = run(
        ["python3", "scripts/correct_engine_c_e6_primitive_packets.py"],
        "E6_PRIMITIVE_PACKET_CORRECTION=VERIFIED",
    )
    correction = load(
        "artifacts/engine-c-e6-primitive-packet-correction-v1.json"
    )
    if (
        correction["claim_tag"]
        != "VERIFIED_EXACT_PRIMITIVE_PACKET_CORRECTION"
        or len(correction["records"]) != 6
    ):
        raise AssertionError("e=6 primitive correction is incomplete")
    for row in correction["records"]:
        if row["e"] != 6:
            raise AssertionError("non-e=6 row entered correction")
        if any(
            powered != 3 * primitive
            for powered, primitive in zip(
                row["powered_stark_coordinates"],
                row["primitive_coordinates"],
                strict=True,
            )
        ):
            raise AssertionError("e=6 coordinate division is not exact")
        if row["exact_sturm_counts"] != {
            "real": 4,
            "positive": 4,
            "negative": 0,
        }:
            raise AssertionError("corrected e=6 packet root count changed")
    normalized_paper = re.sub(r"[^a-z0-9+\-^]", "", paper.lower())
    for polynomial in correction["case_polynomials"].values():
        compact = re.sub(r"[^a-z0-9+\-^]", "", polynomial.lower())
        if compact not in normalized_paper:
            raise AssertionError("corrected e=6 polynomial is not printed")

    q35 = load("artifacts/engine-c-w3-tranche-01-verified-v1.json")
    q6 = load("data/q6-norm8-case-v3.json")
    scope_correction = load("artifacts/engine-c-claim-scope-correction-v1.json")
    if not all(q35["gates"].values()):
        raise AssertionError("Q(sqrt(35)) CM gate is not closed")
    if q35["closure"]["route_e"] != [2, 2]:
        raise AssertionError("Q(sqrt(35)) e-values changed")
    if q6["routes"][0]["e"] != 8 or q6["routes"][0]["natural_s_size"] != 3:
        raise AssertionError("Q(sqrt(6)) direct proof route changed")
    if q6["routes"][1]["natural_s_size"] != 2:
        raise AssertionError("Q(sqrt(6)) quarantined route boundary changed")
    current_tags = scope_correction["current_theorem_tags"]
    if (
        current_tags["q6_e12_route"] != "CROSS_CHECK_NOT_IN_PROOF"
        or current_tags["rq000458_engine_c"] != "DIAGNOSTIC_NOT_IN_PROOF"
        or current_tags["e6_primitive_packets"] != "VERIFIED_AFTER_CORRECTION"
    ):
        raise AssertionError("Engine-C scope correction is stale")

    convention_output = run(
        ["python3", "scripts/audit_engine_c_fourier_convention_v2.py"],
        "ENGINE_C_FOURIER_CONVENTION_V2_AUDIT=VERIFIED",
    )
    convention = load(
        "artifacts/engine-c-fourier-convention-correction-v2.json"
    )
    if (
        convention["claim_tag"]
        != "VERIFIED_EXACT_CONVENTION_REAUDIT"
        or convention["verdict"] != "PASS"
        or convention["packet_log_coefficients_m0_m1"]
        != [[-2, 0], [0, -2], [2, 0], [0, 2]]
    ):
        raise AssertionError("Engine-C Fourier convention audit failed")

    required_polynomial_fragments = (
        "38904X^7",
        "416X^7",
        "90243296X^7",
        "1430858X^7",
        "X^8-8X^7+12X^6",
        "138+36\\sqrt{14}",
    )
    require(paper, *required_polynomial_fragments)
    reject(
        main_body,
        "69087392X^7",
        "734872314691037197497824X^7",
        "2928113119148411258X^7",
    )

    # Verify the four Fourier/CM signs in the written bridge.
    # L'=-2(m0+i*m1); Re(i^{-r}L') must equal
    # (-2m0,-2m1,2m0,2m1).
    expected = ((-2, 0), (0, -2), (2, 0), (0, 2))
    actual = []
    for r in range(4):
        coefficient = (1j) ** (-r) * -2
        # coefficient multiplies m0+i*m1.
        actual.append(
            (round(coefficient.real), round((coefficient * 1j).real))
        )
    if tuple(actual) != expected:
        raise AssertionError("cyclic-quartic Fourier sign audit failed")

    artifact = {
        "schema": "effective-stark-results-paper-full-referee-audit-v3",
        "claim_tag": "VERIFIED_V1_4_PREPUBLICATION_AUDIT",
        "paper": "paper/effective-stark-results.tex",
        "paper_sha256": sha("paper/effective-stark-results.tex"),
        "supplement": "paper/effective-stark-results-supplement.tex",
        "supplement_sha256": sha(
            "paper/effective-stark-results-supplement.tex"
        ),
        "engine_a": {
            "uniform_theorem": "PASS",
            "euler_degeneracy": expected_euler,
            "euler_replay_stdout_sha256": hashlib.sha256(
                euler_output.encode()
            ).hexdigest(),
        },
        "engine_b": {
            "case_count": 8,
            "margins": {
                case_id: str(values[1]) for case_id, values in b_rows.items()
            },
            "archimedean_stdout_sha256": hashlib.sha256(
                arch_output.encode()
            ).hexdigest(),
        },
        "prior_work": {
            "roblot_7_1_applies_count": 4,
            "roblot_7_1_wild_exception": "RQ-002057",
            "roblot_replay_stdout_sha256": hashlib.sha256(
                roblot_output.encode()
            ).hexdigest(),
        },
        "engine_c": {
            "proved_case_count": 5,
            "e_values": [2, 6, 8],
            "formal_bridge": "PASS",
            "fourier_convention": "PASS",
            "fourier_replay_stdout_sha256": hashlib.sha256(
                convention_output.encode()
            ).hexdigest(),
            "e6_primitive_correction": "PASS",
            "e6_replay_stdout_sha256": hashlib.sha256(
                correction_output.encode()
            ).hexdigest(),
            "q6_e12_status": "CROSS_CHECK_NOT_IN_PROOF",
            "rq000458_c_status": "DIAGNOSTIC_NOT_IN_PROOF",
            "scope_correction_sha256": sha(
                "artifacts/engine-c-claim-scope-correction-v1.json"
            ),
        },
        "structural_lemmas": "PASS",
    }
    OUT.write_text(json.dumps(artifact, indent=2) + "\n")
    print("RESULTS_PAPER_FULL_AUDIT=PASS")


if __name__ == "__main__":
    main()
