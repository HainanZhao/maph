#!/usr/bin/env python3
"""Referee audit for the Engine-A/Engine-B results manuscript.

The historical combined-paper audit remains untouched.  This audit enforces
the major-revision split, checks the written proof surface, recomputes the
displayed height margins from promoted case records, and runs the independent
exact all-archimedean-place certificate.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from decimal import Decimal, getcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper/effective-stark-results.tex"
OUT = ROOT / "artifacts/results-paper-ab-referee-audit-v1.json"
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
            raise AssertionError(f"split manuscript retains forbidden text: {needle}")


def ratio(lower: str, upper: str) -> Decimal:
    return Decimal(lower) / Decimal(upper)


def run_archimedean_audit() -> str:
    completed = subprocess.run(
        ["gp", "-q", "scripts/certify_engine_b_archimedean_places.gp"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "all-archimedean-place GP audit failed:\n"
            + completed.stdout
            + completed.stderr
        )
    verdict = "ENGINE_B_ARCHIMEDEAN_PLACE_AUDIT=VERIFIED"
    if verdict not in completed.stdout:
        raise AssertionError("all-archimedean-place audit emitted no VERIFIED verdict")
    return completed.stdout


def main() -> None:
    paper = PAPER.read_text()
    prose = " ".join(paper.split())
    main_body = paper.split(r"\appendix", 1)[0]

    # The split is a mathematical containment gate, not an editorial preference.
    reject(
        main_body,
        "Engine C",
        "General-e",
        "DUAL_ROUTED",
        "RQ-000458",
        r"\Q(\sqrt6)",
        "auxiliary-prime",
        "Stark 1980",
    )
    require(
        prose,
        "not a census-completeness statement",
        "not asserted as a universal priority claim",
        "unproved Stark conjecture",
        "Numerical PARI recognition",
    )

    # The formerly sketched arguments must now be named written results.
    require(
        paper,
        r"\begin{proposition}[Explicit quadratic formula]",
        r"\begin{proposition}[Shintani transfer in one-place notation]",
        r"\begin{lemma}[All-embeddings height rigidity]",
        r"\begin{lemma}[Absolutely abelian ray fields]",
        r"\begin{lemma}[Index parity]",
        r"\tag{11}",
        r"\tag{12}",
        r"\tag{13}",
        r"\texttt{bnfcertify(bnf)} returning \(1\)",
        "quotient-only flag is not used",
    )
    require(
        prose,
        "Shintani's Theorem~1",
        "Shintani's Theorem~2",
        "Shintani's Proposition~5",
        "remaining roots on the unit circle",
    )

    # The theorem table must identify ideals in an unambiguous basis.
    require(
        paper,
        r"\omega=(1+\sqrt D)/2",
        r"\omega=\sqrt D",
        r"\left[\begin{smallmatrix}7&0\\0&1\end{smallmatrix}\right]",
        r"\left[\begin{smallmatrix}15&6\\0&3\end{smallmatrix}\right]",
        r"\left[\begin{smallmatrix}7&0\\0&7\end{smallmatrix}\right]",
        r"\left[\begin{smallmatrix}9&3\\0&3\end{smallmatrix}\right]",
        r"\left[\begin{smallmatrix}7&3\\0&1\end{smallmatrix}\right]",
        r"\left[\begin{smallmatrix}11&5\\0&1\end{smallmatrix}\right]",
    )

    q7 = load("data/q7-p7-case-v1.json")
    q14 = load("data/q14-p7-case-v1.json")
    q5 = load("data/rq000108-case-v1.json")
    q2 = load("data/rq000021-case-v1.json")
    q57 = load("data/q57-norm27-case-v1.json")
    q77 = load("data/rq002955-case-v1.json")
    q33 = load("data/q33-p11-order10-case-v1.json")

    records = (q7, q14, q5, q2, q57, q77, q33)
    if any("VERIFIED" not in json.dumps(record) for record in records):
        raise AssertionError("a selected case has no promoted exact record")

    rows = (
        ("RQ-000190", q7["w2"]["safe_exponent"], 4032, Decimal("5688")),
        ("RQ-000419", q14["w2"]["safe_exponent"], 4032, Decimal("7315")),
        ("RQ-000108", q5["safe_exponent"], 2880, Decimal("2460")),
        ("RQ-000021", q2["safe_exponent"], 2016, Decimal("4261")),
        ("RQ-002057", q57["exponent"]["safe_exponent"], 2592, Decimal("748")),
        ("RQ-002955", q77["safe_exponent"], 4032, Decimal("5151")),
        ("RQ-001107", q33["exponent"]["safe_exponent"], 15840, Decimal("5817")),
    )
    common_v = q14["w3"]["analytic_arb_enclosure"][
        "voutier_degree_3_to_24_lower"
    ]
    margins = {
        "RQ-000190": ratio(
            q7["w3"]["analytic_arb_enclosure"]["voutier_degree_3_to_24_lower"],
            q7["w3"]["analytic_arb_enclosure"]["powered_height_upper"],
        ),
        "RQ-000419": ratio(
            common_v,
            q14["w3"]["analytic_arb_enclosure"]["powered_height_upper"],
        ),
        "RQ-000108": ratio(common_v, q5["identification"]["powered_height_upper"]),
        "RQ-000021": ratio(common_v, q2["identification"]["powered_height_upper"]),
        "RQ-002057": ratio(
            q57["identification"]["analytic_arb_enclosure"][
                "voutier_degree_3_to_24_lower"
            ],
            q57["identification"]["analytic_arb_enclosure"]["powered_height_upper"],
        ),
        "RQ-002955": ratio(common_v, q77["identification"]["powered_height_upper"]),
        "RQ-001107": ratio(
            q33["height_window"]["minimum_voutier_lower_bound"],
            q33["identification"]["powered_height_upper"],
        ),
    }
    for case_id, actual_exp, expected_exp, claimed in rows:
        if actual_exp != expected_exp:
            raise AssertionError(f"{case_id}: safe exponent changed")
        if margins[case_id] <= claimed:
            raise AssertionError(f"{case_id}: displayed strict margin is not certified")
        require(paper, case_id, str(expected_exp), f">{claimed}")

    # Every theorem row has a displayed relative polynomial, not only a JSON pointer.
    for distinguishing_text in (
        r"34+13\sqrt7",
        r"139+38\sqrt{14}",
        r"9+9y",
        r"129+90\sqrt2",
        r"2529+772y",
        r"217+54y",
        r"871+368y",
    ):
        require(paper, distinguishing_text)

    # The representative printed transfer table is complete and arithmetically sound.
    q7_divisor_transcript = (
        ROOT / "artifacts/q7-p7-w2-divisor-table-v1.txt"
    ).read_text()
    if q7["w2"]["safe_exponent"] != 4032:
        raise AssertionError("Q(sqrt(7)) transfer table changed")
    require(q7_divisor_transcript, "576", "84", "SAFE_EXPONENT=4032")
    require(
        paper,
        r"\mathcal O_k&1&4&48&1&576",
        r"(7)&12&1&1&7&84",
        r"\operatorname{lcm}(576,84,6)=4032",
    )

    # Order-ten degree and raw/powered distinction must be explicit.
    if q33["height_window"]["maximum_packet_comparison_degree_cap"] != 80:
        raise AssertionError("order-ten archived comparison cap changed")
    require(
        prose,
        "absolute degree \\(20\\)",
        "normal closure used to compute the Frobenius action has degree \\(40\\)",
        "comparison quotient",
        "needs only \\(d\\le20\\)",
        "raw-error target",
    )

    arch_output = run_archimedean_audit()
    arch_record = load("artifacts/engine-b-archimedean-place-audit-v1.json")
    if arch_record["verdict"] != "VERIFIED_EXACT_ALL_SEVEN":
        raise AssertionError("archimedean-place record is not VERIFIED")
    if arch_record["script"]["sha256"] != sha(
        "scripts/certify_engine_b_archimedean_places.gp"
    ):
        raise AssertionError("archimedean-place script hash changed")
    kopp_watch = load("artifacts/kopp-arxiv-watch-2026-07-30.json")
    if (
        kopp_watch["observed_current_version"] != "v3"
        or kopp_watch["change_from_frozen_perimeter"]
    ):
        raise AssertionError("Kopp arXiv watch no longer matches the manuscript footnote")

    artifact = {
        "schema": "effective-stark-results-paper-ab-referee-audit-v1",
        "claim_tag": "VERIFIED_REFEREE_AUDIT",
        "paper": "paper/effective-stark-results.tex",
        "paper_sha256": sha("paper/effective-stark-results.tex"),
        "split_gate": "PASS",
        "written_proof_surface": {
            "engine_a_formula": "PASS",
            "shintani_transfer": "PASS",
            "all_embeddings_height_rigidity": "PASS",
            "structural_lemmas": "PASS",
        },
        "selected_cases": [row[0] for row in rows],
        "recomputed_margin_lower_bounds": {
            key: str(value) for key, value in margins.items()
        },
        "archimedean_place_audit": {
            "verdict": "VERIFIED",
            "script_sha256": sha(
                "scripts/certify_engine_b_archimedean_places.gp"
            ),
            "stdout_sha256": hashlib.sha256(arch_output.encode()).hexdigest(),
        },
        "literature_watch": {
            "artifact": "artifacts/kopp-arxiv-watch-2026-07-30.json",
            "sha256": sha("artifacts/kopp-arxiv-watch-2026-07-30.json"),
            "current_version": "v3",
        },
    }
    OUT.write_text(json.dumps(artifact, indent=2) + "\n")
    print("RESULTS_PAPER_AB_AUDIT=PASS")


if __name__ == "__main__":
    main()
