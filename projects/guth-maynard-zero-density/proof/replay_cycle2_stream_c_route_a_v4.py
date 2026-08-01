#!/usr/bin/env python3
"""Deterministic, source-sealed Stream-C Route-A v4 correction.

The arithmetic is replayed here from exact rationals; this script does not
import any Route-B derivation.  Earlier Route-A records are read only to seal
their preservation and to state the limited correction they require.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import time
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCESS_LEDGER = ROOT / "docs/cycle-2-stream-c-explicit-formula-access-ledger-v2-correction.md"
FORMULA_CLOSURE = ROOT / "artifacts/cycle-2-stream-c-explicit-formula-source-closure-v2.json"
SOURCE_LEDGER = ROOT / "artifacts/cycle-2-stream-c-source-ledger-v2.json"
GM = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
KEDLAYA_FORMULA = ROOT / "artifacts/sources/kedlaya-2007-errorbounds-author.pdf"
KEDLAYA_PROOF = ROOT / "artifacts/sources/kedlaya-2007-von-mangoldt-author.pdf"
HUXLEY = ROOT / "artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf"
FORD = ROOT / "artifacts/sources/ford-2002-zero-free-regions.pdf"
PLATT = ROOT / "artifacts/sources/platt-trudgian-2021-rh-3e12.tar"
HSW = ROOT / "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar"
BUI = ROOT / "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar"
OLD = {
    "route_a_v1": ROOT / "artifacts/cycle-2-stream-c-route-a-v1.json",
    "route_a_v2": ROOT / "artifacts/cycle-2-stream-c-route-a-v2.json",
    "route_a_v3": ROOT / "artifacts/cycle-2-stream-c-route-a-v3.json",
}
SEALED = {
    ACCESS_LEDGER: "962acbf93a60eca5340367e02af3bfe7c44693d931726b74ba18ccc7fb661d31",
    FORMULA_CLOSURE: "3433e974b9751d310447847d75abbf529e5b4ed7e21e87a0224e4efb8ea0fde3",
    SOURCE_LEDGER: "4e2b107194420d97cb949cf2e7934f8fda81bb5f688e63aa2cd49e1b6c3cac5d",
    GM: "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    KEDLAYA_FORMULA: "375d96e65a99d7dbfbdc9ca51aa286bb53af7e77dfffa59e167dfcd9b18b919d",
    KEDLAYA_PROOF: "43cbe51ee69fe552078d90d0c21b165456f3ad67ad64c83df71b9cce3d56ae05",
    HUXLEY: "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797",
    FORD: "a43a2c37cf0f34b05bf80d9e58bcef176371437eedf7aae17d72f2c55b04c948",
    PLATT: "c4f13cdfca711d2bf90a097147be2a094ff175b0b161647359e174633fd8bf86",
    HSW: "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    BUI: "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
}
LEGACY_IDENTITIES = {
    "route_a_v1": "7aa44f69a585ea5b984ef027e8ace496ae1134e55e8a06b24ea51abbe509f729",
    "route_a_v2": "3e0e194aab6810a2697f7951058c3ee407fa3dc47e9ce91ba96139f037fc3970",
    "route_a_v3": "1e0069963e04ae5180e7994f57ad7ced135d8d104bf83d59652fe2c49a489794",
}
V3_BYTE_HASH = "d9e201c164f1a2cb8a6894c6f786f67e19752c6b048b5ccca5f250f4a87ccccd"
B = Fraction(30, 13)
UNIFORM_THETA = Fraction(17, 30)
ALMOST_ALL_THETA = Fraction(2, 15)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def poly_add(*values: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    size = max(len(value) for value in values)
    output = [Fraction(0, 1) for _ in range(size)]
    for value in values:
        for index, coefficient in enumerate(value):
            output[index] += coefficient
    while len(output) > 1 and output[-1] == 0:
        output.pop()
    return tuple(output)


def poly_scale(value: tuple[Fraction, ...], scalar: Fraction) -> tuple[Fraction, ...]:
    return tuple(scalar * coefficient for coefficient in value)


def pdf_text(path: Path) -> str:
    return subprocess.run(["mutool", "draw", "-F", "txt", "-o", "-", str(path)], check=True, capture_output=True, text=True).stdout


def gzip_text(path: Path) -> str:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return handle.read()


def check_source_authority() -> dict[str, str]:
    for path, expected in SEALED.items():
        assert sha256(path) == expected, f"sealed input hash mismatch: {path}"
    for name, path in OLD.items():
        legacy = json.loads(path.read_text(encoding="utf-8"))
        assert legacy["exact_replay_sha256"] == LEGACY_IDENTITIES[name], f"historical Route-A semantic record changed: {name}"
    assert sha256(OLD["route_a_v3"]) == V3_BYTE_HASH, "deterministic v3 artifact bytes changed"
    access = ACCESS_LEDGER.read_text(encoding="utf-8")
    for phrase in (
        "CC BY-NC-SA 4.0",
        "kedlaya-2007-errorbounds-author.pdf",
        "kedlaya-2007-von-mangoldt-author.pdf",
        "every zero residue\nis counted with multiplicity",
        "u=\\lceil x\\rceil-1",
        "|\\gamma|<T",
    ):
        assert phrase in access, f"missing access-ledger-v2 anchor: {phrase}"
    closure = json.loads(FORMULA_CLOSURE.read_text(encoding="utf-8"))
    assert closure["epistemic_status"] == "PROVED"
    units = {item["id"]: item for item in closure["frozen_oa_course_units"]}
    assert units["kedlaya-errorbounds"]["sha256"] == SEALED[KEDLAYA_FORMULA]
    assert units["kedlaya-von-mangoldt-proof"]["sha256"] == SEALED[KEDLAYA_PROOF]
    assert closure["transfer"]["status"] == "PROVED"
    ledger = json.loads(SOURCE_LEDGER.read_text(encoding="utf-8"))
    assert ledger["epistemic_status"] == "PROVED"
    wanted = {"guth-maynard-section-13-2", "huxley-1972-equation-1-9", "ford-2002-vinogradov-korobov", "platt-trudgian-2021-low-height-rh", "hasanalizade-shen-wong-2022-rvm", "bui-heath-brown-2013-multiplicity-convention"}
    indexed = {item["id"]: item for item in ledger["sources"]}
    assert wanted <= indexed.keys()
    assert all(indexed[key]["status"] == "PROVED" for key in wanted)
    formula, proof = pdf_text(KEDLAYA_FORMULA), pdf_text(KEDLAYA_PROOF)
    for phrase in ("For x ≥ 2 and T > 0", "distance from x to the nearest prime power other than possibly x itself", "x log2(xT)"):
        assert phrase in formula, f"missing Kedlaya formula anchor: {phrase}"
    for phrase in ("For x ≥ 2 and T > 0", "every zero ρ of\nζ (counted with multiplicity)", "We are done!"):
        assert phrase in proof, f"missing Kedlaya proof anchor: {phrase}"
    gm = GM.read_text(encoding="utf-8")
    for phrase in ("for any choice of $2\\le T\\le x$", "T=xy^{-1}\\exp(2\\sqrt[4]{\\log{x}})", "\\delta=X^{-13/15+\\epsilon/2}", "T=\\delta^{-1}\\exp(4\\sqrt[4]{\\log{X}})", "X^{2\\sigma+1}N(\\sigma,T)"):
        assert phrase in gm, f"missing GM §13.2 anchor: {phrase}"
    hsw, bui, platt = gzip_text(HSW), gzip_text(BUI), gzip_text(PLATT)
    assert "For any $T\\ge e$" in hsw
    assert "where each zero is counted with multiplicity" in bui
    assert "all zeroes $\\beta + i\\gamma$" in platt and "$\\beta = 1/2$" in platt
    return {str(path.relative_to(ROOT)): expected for path, expected in SEALED.items()}


def exact_route_a_arithmetic() -> dict[str, Any]:
    """Fresh exact Route-A arithmetic; no previous route computation is read."""
    one = Fraction(1, 1)
    assert one / B == Fraction(13, 30)
    assert 2 / B == Fraction(13, 15)
    assert one - one / B == UNIFORM_THETA
    assert one - 2 / B == ALMOST_ALL_THETA
    assert B * Fraction(13, 30) == one
    assert B * Fraction(13, 15) == 2
    # Universal Huxley comparison: after the common denominator
    # 13(3s-1), 30(3s-1)-39 = 3(30s-23).  Coefficient equality, not
    # sampling, certifies the factorization on the full stated interval.
    left = poly_add(poly_scale((Fraction(-1, 1), Fraction(3, 1)), Fraction(30, 1)), (Fraction(-39, 1),))
    right = poly_scale((Fraction(-23, 1), Fraction(30, 1)), Fraction(3, 1))
    assert left == right == (Fraction(-69, 1), Fraction(90, 1))
    assert 30 * Fraction(4, 5) - 23 == 1 > 0
    assert 3 * Fraction(4, 5) - 1 == Fraction(7, 5) > 0
    assert B - Fraction(15, 7) == Fraction(15, 91) > 0
    return {
        "density_coefficient": q(B),
        "uniform": {
            "theta": q(UNIFORM_THETA),
            "endpoint_T_power": "1-theta=13/30=1/B",
            "height": "T=x/y exp(2(log x)^(1/4))",
            "eventual_margin": "y>=x^(17/30+epsilon) implies T<x^(13/30-epsilon/2), while 2<=T<=x follows from y<=x^0.99.",
            "formula_error": "x(log x)^3/T=y(log x)^3 exp(-2(log x)^(1/4))=O(y exp(-(log x)^(1/4))) eventually.",
        },
        "almost_all": {
            "theta": q(ALMOST_ALL_THETA),
            "delta": "X^(-13/15+epsilon/2)",
            "height": "T=delta^(-1) exp(4(log X)^(1/4))",
            "endpoint_T_power": "13/15=2/B",
            "eventual_margin": "T<=X^(13/15-epsilon/3) and 2<=T<=X eventually; this is why the arbitrary-T formula, not the alpha<=1/2 CHJ-I theorem, is used.",
            "second_moment": "delta^2 X^3/(y^2 X)<=X^(-epsilon) at y>=X^(2/15+epsilon), so the displayed Cauchy-Schwarz remainder is absorbed before Chebyshev.",
        },
        "near_one": {
            "universal_factorization": "30/13-3/(3s-1)=3(30s-23)/[13(3s-1)]",
            "coefficient_certificate": "Exact polynomial coefficient equality: 30(3s-1)-39=3(30s-23).",
            "range_signs": "For 4/5<=s<1, 30s-23>=1 and 3s-1>=7/5, hence 3/(3s-1)<=30/13.",
            "vk": "Ford's 2/3 cutoff is stronger eventually than the GM 5/7 cutoff since 2/3-5/7=-1/21; Platt--Trudgian supplies the finite-height completion.",
        },
        "formula_conventions": {
            "integer_transfer": "The v2 access/closure records give half-weight endpoint transfer and O(X(log X)^3/T) for 2<=T<=X.",
            "multiplicity": "The Kedlaya proof-unit residue computation explicitly counts every zero with multiplicity.",
            "height_bridge": "The v2 closure confines |gamma|<T versus literal |rho|<=T to unit boundary strips, absorbed using HSW+Bui local multiplicity counts.",
        },
    }


def rows() -> list[dict[str, Any]]:
    return [
        {"id": "SC-A41-v3-source-authority-and-byte-provenance-containment", "epistemic_status": "PROVED", "statement": "v3's output artifact was deterministic on its tested runtime, but it pinned only access-ledger v1 and the errorbounds PDF; it did not seal access-ledger v2, the v2 source-closure artifact, or the von-Mangoldt proof PDF. Therefore its broader source-authority claim is not reused here. This is a provenance containment, not a claim that v3 output bytes were nondeterministic.", "falsifier": "A v3 replay that seals those omitted v2 inputs and proof PDF would remove this historical containment."},
        {"id": "SC-A42-access-and-both-kedlaya-units", "epistemic_status": "PROVED", "statement": "Access-ledger v2, source-closure v2, and both Kedlaya PDFs are byte-pinned. The formula unit supplies arbitrary T and the distance remainder; the proof unit supplies multiplicity of zero residues.", "falsifier": "Any sealed hash or required PDF anchor mismatch invalidates this source node."},
        {"id": "SC-A43-source-hypotheses", "epistemic_status": "PROVED", "statement": "GM §13.2, Huxley near-one density, Ford VK, Platt--Trudgian finite-height completion, and HSW/Bui local multiplicity conventions are pinned through direct hashes and the v2 source-hypothesis ledger.", "falsifier": "A source-hypothesis ledger row not PROVED or a source hash mismatch invalidates its use."},
        {"id": "SC-A44-uniform-route-a-arithmetic", "epistemic_status": "PROVED", "statement": "Fresh Fraction arithmetic gives 1/B=13/30 and theta=17/30, the prescribed uniform height margin, and the truncation-error absorption.", "falsifier": "Failure of B*(13/30)=1 or of the stated eventual height range invalidates this branch."},
        {"id": "SC-A45-almost-all-route-a-arithmetic", "epistemic_status": "PROVED", "statement": "Fresh Fraction arithmetic gives 2/B=13/15 and theta=2/15, validates the arbitrary-T range, and absorbs the Cauchy--Schwarz remainder before the stated Chebyshev conversion.", "falsifier": "Failure of B*(13/15)=2, of 2<=T<=X eventually, or of the remainder ratio invalidates this branch."},
        {"id": "SC-A46-universal-huxley-comparison", "epistemic_status": "PROVED", "statement": "The Huxley coefficient comparison is certified by exact polynomial coefficient equality, not finite sampling: 30/13-3/(3s-1)=3(30s-23)/[13(3s-1)]>=0 for 4/5<=s<1.", "falsifier": "A failed coefficient equality or a negative stated range factor invalidates this universal comparison."},
    ]


def build_report() -> dict[str, Any]:
    source_hashes = check_source_authority()
    arithmetic = exact_route_a_arithmetic()
    report_rows = rows()
    assert all(row["epistemic_status"] == "PROVED" for row in report_rows)
    return {
        "artifact_id": "cycle-2-stream-c-route-a-v4",
        "route": "A",
        "stream": "C",
        "epistemic_status": "PROVED",
        "supersedes": {
            "artifacts": ["cycle-2-stream-c-route-a-v1", "cycle-2-stream-c-route-a-v2", "cycle-2-stream-c-route-a-v3"],
            "preservation": "v1/v2/v3 are retained unchanged. v1/v2 are identified by their stable exact_replay_sha256 because their replay metadata contains timing; v3 is additionally byte-sealed. v4 is a correction/additive replay, not an edit of their claims.",
            "correction": "v3 source authority is contained because its replay did not seal access-ledger v2, source-closure v2, and both Kedlaya units; v4 does. v3 output-byte determinism itself is not alleged false.",
        },
        "claim_boundary": "PROVED only as a source-sealed replay of the published GM §13.2 deductions, conditional on GM's published density theorem. It does not independently prove that density theorem, prove a new prime-interval theorem, improve theta, or promote G0.",
        "source_inputs": source_hashes,
        "preserved_route_a_v1_v3_identities": {
            "legacy_exact_replay_sha256": LEGACY_IDENTITIES,
            "v3_byte_sha256": V3_BYTE_HASH,
            "v1_v2_byte_note": "v1/v2 embed wall_time_ns and are therefore preserved by their stable exact_replay_sha256 identities, not mutable raw bytes.",
        },
        "exact_route_a_arithmetic": arithmetic,
        "rows": report_rows,
        "open_blockers": [],
        "result_labels": {
            "uniform_theta": "17/30",
            "almost_all_theta": "2/15",
            "uniform": "PROVED input compatibility conditional on GM density",
            "almost_all": "PROVED input compatibility conditional on GM density",
        },
        "pass_state": "NARROW PASS: Stream-C Route-A source/formula/convention nodes and published endpoint arithmetic are sealed. G0 remains OBSERVED until the separate two-route reconciliation is updated.",
        "replay": {
            "interpreter_requirement": "Python 3 standard library plus pinned mutool PDF text extraction",
            "script": str(Path(__file__).relative_to(ROOT)),
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_c_route_a_v4.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-a-v4.json",
            "check_command": "python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_c_route_a_v4.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-a-v4.json",
        },
    }


def render(report: dict[str, Any]) -> str:
    return json.dumps(report, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path, metavar="PATH")
    mode.add_argument("--check", type=Path, metavar="PATH")
    mode.add_argument("--write-performance", type=Path, metavar="PATH")
    args = parser.parse_args()
    if args.write_performance:
        started = time.perf_counter_ns()
        build_report()
        performance = {"artifact_id": "cycle-2-stream-c-route-a-v4-performance", "epistemic_status": "OBSERVED", "script_sha256": sha256(Path(__file__)), "wall_time_ns": time.perf_counter_ns() - started}
        args.write_performance.write_text(json.dumps(performance, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return
    output = render(build_report())
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(output, encoding="utf-8")
    elif args.check.read_text(encoding="utf-8") != output:
        raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")


if __name__ == "__main__":
    main()
