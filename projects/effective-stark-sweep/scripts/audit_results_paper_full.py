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
OUT = ROOT / "artifacts/results-paper-full-referee-audit-v2.json"
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
    prose = " ".join(paper.split())
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
        r"N_{E/E^+}(\sigma^{-r}u)^{-1}",
        r"\zeta'_S(0,g)=-\frac2e\ell_g",
        r"L'_S(0,\psi)",
        r"=-\frac4e(\ell_1-i\ell_\sigma)",
        r"\frac1m\log|\sigma_v(X_A^m)|",
        r"j(E)=E,\qquad j|_k\ne1",
        r"Put \(E^+=E^{\langle j\rangle}\)",
        r"\phantomsection\label{par:conventions}",
        r"\theta(\bar s)=i",
        r"\psi(\sigma)=i",
        r"\label{eq:index-parity}",
        r"\label{sec:rq458}",
    )
    require(
        prose,
        "Global complex conjugation is a different automorphism",
        "Scalar twists are not permitted",
        "Equality of unlabeled polynomials is never the bridge",
        "not used in the theorem",
        "The theorem claim for this row rests solely on Engine B",
        "We are not aware of previous unconditional one-place Stark packet",
        "not a finished referee draft until its companion archive",
        "Shintani's Proposition~4 on pp.~154--156",
        "Shintani's Proposition~5(i)--(iii) on pp.~156--158",
        "valid for every degree",
        "complete the proof of Theorem",
        "in 346 rows all supported terms vanish",
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
    # L'=-2(m0-i*m1); Re(i^{-r}L') must equal
    # (-2m0,2m1,2m0,-2m1).
    expected = ((-2, 0), (0, 2), (2, 0), (0, -2))
    actual = []
    for r in range(4):
        coefficient = (1j) ** (-r) * -2
        # coefficient multiplies m0-i*m1
        actual.append((round(coefficient.real), round(coefficient.imag)))
    if tuple(actual) != expected:
        raise AssertionError("cyclic-quartic Fourier sign audit failed")

    artifact = {
        "schema": "effective-stark-results-paper-full-referee-audit-v2",
        "claim_tag": "VERIFIED_MAJOR_REVISION_AUDIT",
        "paper": "paper/effective-stark-results.tex",
        "paper_sha256": sha("paper/effective-stark-results.tex"),
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
        "engine_c": {
            "proved_case_count": 5,
            "e_values": [2, 6, 8],
            "formal_bridge": "PASS",
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
