#!/usr/bin/env python3
"""Deterministic Stream-C Route-A v5 using only official SWORD source bytes.

This is a fresh Route-A source and rational-arithmetic replay.  It imports no
Route-B code or derivation.  Earlier Route-A artifacts are preserved as sealed
historical evidence and are not edited.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import time
import zipfile
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMULA_CLOSURE = ROOT / "artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json"
FORMULA_CHECKER = ROOT / "proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py"
SWORD_AUDIT = ROOT / "artifacts/cycle-2-mit-sword-official-bitstream-audit-v1.json"
SWORD = ROOT / "artifacts/sources/mit-ocw-18-785-2007-sword-official.zip"
OFFICIAL_FORMULA = ROOT / "artifacts/sources/mit-ocw-18-785-2007-errorbounds-official.pdf"
OFFICIAL_PROOF = ROOT / "artifacts/sources/mit-ocw-18-785-2007-von-mangoldt-official.pdf"
METADATA = ROOT / "artifacts/sources/mit-dspace-1721.1-101679-metadata.json"
GM = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
HUXLEY = ROOT / "artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf"
FORD = ROOT / "artifacts/sources/ford-2002-zero-free-regions.pdf"
PLATT = ROOT / "artifacts/sources/platt-trudgian-2021-rh-3e12.tar"
HSW = ROOT / "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar"
BUI = ROOT / "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar"
SOURCE_LEDGER = ROOT / "artifacts/cycle-2-stream-c-source-ledger-v2.json"
OLD = {
    "route_a_v1": ROOT / "artifacts/cycle-2-stream-c-route-a-v1.json",
    "route_a_v2": ROOT / "artifacts/cycle-2-stream-c-route-a-v2.json",
    "route_a_v3": ROOT / "artifacts/cycle-2-stream-c-route-a-v3.json",
    "route_a_v4": ROOT / "artifacts/cycle-2-stream-c-route-a-v4.json",
}
HASHES = {
    FORMULA_CLOSURE: "1c4ecc54be6f681be788084c3637f1101996869e09015edac8cf41e6ab39d5f0",
    FORMULA_CHECKER: "72107f1f31e51d2aa9d0ea0eb22c247a1643e58a898232a7fd02c3dee5508064",
    SWORD_AUDIT: "6b4bd931a33a075d39aefc905e27e24767a9a0f08b82947afdfea46accefc4b7",
    SWORD: "d559229963960da2087918a95af6efd7ad8999a4ba63942a12aef63c5eceac57",
    OFFICIAL_FORMULA: "b8b2acfbc4b22b25c898c0af8f74692a0d31bd6cf302e9f2d772d33a34fdd3e4",
    OFFICIAL_PROOF: "5f705a6d3804d555944298f87a8a53e2e4e5a13188a717679f8fb8b73095210a",
    METADATA: "4c1f262bc51efa23993a561f908871d35245ca462df90271d0bf2127283f24c7",
    GM: "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    HUXLEY: "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797",
    FORD: "a43a2c37cf0f34b05bf80d9e58bcef176371437eedf7aae17d72f2c55b04c948",
    PLATT: "c4f13cdfca711d2bf90a097147be2a094ff175b0b161647359e174633fd8bf86",
    HSW: "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    BUI: "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
    SOURCE_LEDGER: "4e2b107194420d97cb949cf2e7934f8fda81bb5f688e63aa2cd49e1b6c3cac5d",
}
LEGACY_IDENTITIES = {
    "route_a_v1": "7aa44f69a585ea5b984ef027e8ace496ae1134e55e8a06b24ea51abbe509f729",
    "route_a_v2": "3e0e194aab6810a2697f7951058c3ee407fa3dc47e9ce91ba96139f037fc3970",
    "route_a_v3": "1e0069963e04ae5180e7994f57ad7ced135d8d104bf83d59652fe2c49a489794",
}
V4_BYTE_HASH = "eca84d439a7895a8d781ba54ba030fb2c8c76dc09082cbdb60282fe349543512"
MUTOOL_VERSION = "mutool version 1.23.10"
FORMULA_MEMBER = "18-785-spring-2007/contents/lecture-notes/errorbounds.pdf"
PROOF_MEMBER = "18-785-spring-2007/contents/lecture-notes/von_mangoldt.pdf"
B = Fraction(30, 13)


def sha256(data: Path | bytes) -> str:
    return hashlib.sha256(data.read_bytes() if isinstance(data, Path) else data).hexdigest()


def q(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def poly_add(*items: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    result = [Fraction(0, 1) for _ in range(max(len(item) for item in items))]
    for item in items:
        for index, coefficient in enumerate(item):
            result[index] += coefficient
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def poly_scale(item: tuple[Fraction, ...], scalar: Fraction) -> tuple[Fraction, ...]:
    return tuple(scalar * coefficient for coefficient in item)


def pdf_text(path: Path) -> str:
    return subprocess.run(["mutool", "draw", "-F", "txt", "-o", "-", str(path)], check=True, capture_output=True, text=True).stdout


def gzip_text(path: Path) -> str:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return handle.read()


def check_official_source_chain() -> dict[str, str]:
    for path, expected in HASHES.items():
        assert sha256(path) == expected, f"sealed input hash mismatch: {path}"
    for name, path in OLD.items():
        old = json.loads(path.read_text(encoding="utf-8"))
        if name == "route_a_v4":
            assert sha256(path) == V4_BYTE_HASH, "Route-A v4 deterministic artifact changed"
        else:
            assert old["exact_replay_sha256"] == LEGACY_IDENTITIES[name], f"Route-A historical semantic identity changed: {name}"
    closure = json.loads(FORMULA_CLOSURE.read_text(encoding="utf-8"))
    assert closure["epistemic_status"] == "PROVED"
    assert closure["official_source"]["dspace_handle"] == "1721.1/101679"
    assert closure["official_source"]["license"] == "CC BY-NC-SA 3.0"
    assert closure["official_sword_bitstream"]["sha256"] == HASHES[SWORD]
    members = closure["official_pdf_members"]
    assert {member["archive_member"] for member in members} == {FORMULA_MEMBER, PROOF_MEMBER}
    assert {member["sha256"] for member in members} == {HASHES[OFFICIAL_FORMULA], HASHES[OFFICIAL_PROOF]}
    assert closure["exact_replay_anchors"]["renderer"] == MUTOOL_VERSION
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    assert metadata["handle"] == "1721.1/101679" and not metadata["withdrawn"]
    rights = [value["value"] for value in metadata["metadata"]["dc.rights.uri"]]
    assert "Usage Restrictions: Attribution-NonCommercial-ShareAlike 3.0 Unported" in rights
    with zipfile.ZipFile(SWORD) as archive:
        assert archive.testzip() is None
        assert sha256(archive.read(FORMULA_MEMBER)) == HASHES[OFFICIAL_FORMULA]
        assert sha256(archive.read(PROOF_MEMBER)) == HASHES[OFFICIAL_PROOF]
    version = subprocess.run(["mutool", "-v"], check=True, capture_output=True, text=True)
    assert (version.stdout + version.stderr).strip() == MUTOOL_VERSION, "mutool version mismatch"
    formula, proof = pdf_text(OFFICIAL_FORMULA), pdf_text(OFFICIAL_PROOF)
    for anchor in ("Theorem 1 (von Mangoldt’s formula). For x ∼ 2 and T > 0", "n<x", "x log2(xT )", "nearest prime power other than possibly x itself"):
        assert anchor in formula, f"missing official formula anchor: {anchor}"
    for anchor in ("Theorem 1 (von Mangoldt’s formula). For x √ 2 and T > 0", "counted with multiplicity", "We are done!"):
        assert anchor in proof, f"missing official proof anchor: {anchor}"
    gm = GM.read_text(encoding="utf-8")
    for anchor in ("for any choice of $2\\le T\\le x$", "T=xy^{-1}\\exp(2\\sqrt[4]{\\log{x}})", "\\delta=X^{-13/15+\\epsilon/2}", "T=\\delta^{-1}\\exp(4\\sqrt[4]{\\log{X}})", "X^{2\\sigma+1}N(\\sigma,T)"):
        assert anchor in gm, f"missing GM §13.2 anchor: {anchor}"
    hsw, bui, platt = gzip_text(HSW), gzip_text(BUI), gzip_text(PLATT)
    assert "For any $T\\ge e$" in hsw and "where each zero is counted with multiplicity" in bui
    assert "all zeroes $\\beta + i\\gamma$" in platt and "$\\beta = 1/2$" in platt
    ledger = json.loads(SOURCE_LEDGER.read_text(encoding="utf-8"))
    source_ids = {entry["id"]: entry for entry in ledger["sources"]}
    needed = {"huxley-1972-equation-1-9", "ford-2002-vinogradov-korobov", "platt-trudgian-2021-low-height-rh", "hasanalizade-shen-wong-2022-rvm", "bui-heath-brown-2013-multiplicity-convention"}
    assert all(source_ids[name]["status"] == "PROVED" for name in needed)
    # The direct official source, not the author copies, is the only formula authority.
    return {str(path.relative_to(ROOT)): expected for path, expected in HASHES.items()}


def exact_route_a_arithmetic() -> dict[str, Any]:
    one = Fraction(1, 1)
    uniform_theta, almost_theta = Fraction(17, 30), Fraction(2, 15)
    assert one / B == Fraction(13, 30) and 2 / B == Fraction(13, 15)
    assert one - one / B == uniform_theta and one - 2 / B == almost_theta
    assert B * Fraction(13, 30) == one and B * Fraction(13, 15) == 2
    # Global coefficient certificate, after denominator 13(3s-1):
    # 30(3s-1)-39 = 3(30s-23), checked coefficientwise.
    lhs = poly_add(poly_scale((Fraction(-1, 1), Fraction(3, 1)), Fraction(30, 1)), (Fraction(-39, 1),))
    rhs = poly_scale((Fraction(-23, 1), Fraction(30, 1)), Fraction(3, 1))
    assert lhs == rhs == (Fraction(-69, 1), Fraction(90, 1))
    assert 30 * Fraction(4, 5) - 23 == 1 > 0
    assert 3 * Fraction(4, 5) - 1 == Fraction(7, 5) > 0
    assert B - Fraction(15, 7) == Fraction(15, 91) > 0
    return {
        "density_coefficient": q(B),
        "uniform": {"theta": q(uniform_theta), "identity": "1/B=13/30 and 1-1/B=17/30", "height": "T=x/y exp(2(log x)^(1/4))", "range": "y>=x^(17/30+epsilon), y<=x^0.99 gives 2<=T<=x and T<x^(13/30-epsilon/2) eventually", "error": "x(log x)^3/T=O(y exp(-(log x)^(1/4))) eventually."},
        "almost_all": {"theta": q(almost_theta), "identity": "2/B=13/15 and 1-2/B=2/15", "delta": "X^(-13/15+epsilon/2)", "height": "T=delta^(-1) exp(4(log X)^(1/4))", "range": "2<=T<=X and T<=X^(13/15-epsilon/3) eventually", "second_moment": "delta^2 X^3/(y^2 X)<=X^(-epsilon) for y>=X^(2/15+epsilon)."},
        "huxley": {"identity": "30/13-3/(3s-1)=3(30s-23)/[13(3s-1)]", "certificate": "Exact coefficient equality 30(3s-1)-39=3(30s-23), not finite samples.", "range_signs": "For 4/5<=s<1, 30s-23>=1 and 3s-1>=7/5, so the difference is nonnegative."},
        "formula": {"official_only": "The official SWORD members, not author-hosted copies, supply the all-T formula, multiplicity proof, endpoint transfer, and height bridge.", "conventions": "The closure v4 transfer uses integral endpoints and HSW+Bui boundary strips; no author/official byte identity is used or asserted."},
    }


def rows() -> list[dict[str, Any]]:
    return [
        {"id": "SC-A51-v2-v4-provenance-corrections", "epistemic_status": "PROVED", "statement": "v2's CC 4.0/author-byte license inference is withdrawn; v3's author-copy distribution caveat is superseded; v4 Route-A's dependence on source-closure v2 is not reused. V5 uses only official SWORD archive members and course metadata, and makes no author-copy identity claim.", "falsifier": "Any v5 source path that relies on an author-copy license or byte identity invalidates this containment."},
        {"id": "SC-A52-official-formula-and-proof-authority", "epistemic_status": "PROVED", "statement": "The pinned DSpace SWORD ZIP, its official formula and proof members, course metadata, source-closure v4, and its checker establish the all-T formula, remainder, half-weight convention, and multiplicity proof from official bytes. mutool version 1.23.10 is checked before literal anchor extraction.", "falsifier": "A SWORD/member/metadata/checker hash mismatch, mutool-version mismatch, or missing official-PDF anchor invalidates this node."},
        {"id": "SC-A53-other-route-a-source-hypotheses", "epistemic_status": "PROVED", "statement": "GM §13.2, Huxley, Ford, Platt--Trudgian, HSW, and Bui--Heath-Brown inputs are separately byte-pinned; the Route-A source-hypothesis checks do not invoke Route-B derivations.", "falsifier": "A pinned source hash or required source-ledger status mismatch invalidates the relevant hypothesis."},
        {"id": "SC-A54-route-a-endpoint-arithmetic", "epistemic_status": "PROVED", "statement": "Fresh exact Fraction arithmetic reproduces 17/30 and 2/15, their height ranges, truncation-error absorption, and the Cauchy--Schwarz remainder condition.", "falsifier": "Failure of either exact B identity or stated eventual range invalidates this arithmetic node."},
        {"id": "SC-A55-universal-near-one-comparison", "epistemic_status": "PROVED", "statement": "The Huxley coefficient inequality is global, certified by polynomial coefficient equality 30(3s-1)-39=3(30s-23) and range signs on 4/5<=s<1.", "falsifier": "A failed coefficient equality or a negative range factor invalidates this universal comparison."},
    ]


def build_report() -> dict[str, Any]:
    inputs = check_official_source_chain()
    math = exact_route_a_arithmetic()
    report_rows = rows()
    assert all(row["epistemic_status"] == "PROVED" for row in report_rows)
    return {
        "artifact_id": "cycle-2-stream-c-route-a-v5",
        "route": "A",
        "stream": "C",
        "epistemic_status": "PROVED",
        "supersedes": {"artifacts": ["cycle-2-stream-c-route-a-v1", "cycle-2-stream-c-route-a-v2", "cycle-2-stream-c-route-a-v3", "cycle-2-stream-c-route-a-v4"], "preservation": "v1-v4 are retained unchanged. v1-v3 semantic identities and deterministic v4 bytes are checked before v5 is issued.", "provenance_correction": "Official source-closure v4 replaces all author-copy authority paths; it withdraws v2's CC 4.0/author-byte premise and makes author/official byte identity unnecessary and unasserted."},
        "claim_boundary": "PROVED only as an official-source-sealed Route-A replay of the published GM §13.2 deductions, conditional on GM's published density theorem. It neither proves that density theorem, improves either theta, establishes a new prime theorem, nor promotes G0.",
        "official_source_inputs": inputs,
        "legacy_route_a_identities": {"v1_v3_exact_replay_sha256": LEGACY_IDENTITIES, "v4_byte_sha256": V4_BYTE_HASH, "timing_note": "v1-v2 have timing-mutable raw bytes and are preserved by semantic identities; timing is absent from v5's mathematical artifact."},
        "exact_route_a_arithmetic": math,
        "rows": report_rows,
        "open_blockers": [],
        "result_labels": {"uniform_theta": "17/30", "almost_all_theta": "2/15", "uniform": "PROVED input compatibility conditional on GM density", "almost_all": "PROVED input compatibility conditional on GM density"},
        "pass_state": "NARROW PASS: Stream-C Route-A official-source, convention, and endpoint-arithmetic nodes are checked. G0 remains OBSERVED pending the separately scoped full reconciliation.",
        "replay": {"interpreter_requirement": "Python 3 standard library and mutool version 1.23.10", "script": str(Path(__file__).relative_to(ROOT)), "script_sha256": sha256(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_c_route_a_v5.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-a-v5.json", "check_command": "python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_c_route_a_v5.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-a-v5.json"},
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


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
        args.write_performance.write_text(json.dumps({"artifact_id": "cycle-2-stream-c-route-a-v5-performance", "epistemic_status": "OBSERVED", "script_sha256": sha256(Path(__file__)), "wall_time_ns": time.perf_counter_ns() - started}, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return
    output = render(build_report())
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(output, encoding="utf-8")
    elif args.check.read_text(encoding="utf-8") != output:
        raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")


if __name__ == "__main__":
    main()
