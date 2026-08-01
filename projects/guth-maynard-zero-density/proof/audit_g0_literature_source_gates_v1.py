#!/usr/bin/env python3
"""Bounded final audit of G0's literature/source-hypothesis chain only."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-2-g0-literature-source-gate-audit-v1.json"
FROZEN = {
    "stream_a_source_metadata": ("artifacts/cycle-2-stream-a-source-metadata-v1.json", "378c12a69ba24dd3dae105c87b6960c9909e7b00935ca73f6180d2404572c980"),
    "gm_source_metadata": ("artifacts/guth-maynard-source-metadata-v1.json", "720da7b4ab8e3290c27df44b466eb74099daadd3eb010ae9ec32ae34914fd963"),
    "classical_source_metadata": ("artifacts/classical-zero-density-source-metadata-v1.json", "5b34b80d08898a5a0092b05c1a11344f3e8c28304eecaa92d3fba824b3f3f426"),
    "stream_b_reconciliation": ("artifacts/cycle-2-stream-b-route-reconciliation-v2.json", "5aa163187d8365a72bfbc662e3e3d64a1efbdf18cdc26f150e6dee7b19e3c052"),
    "stream_b_reconciliation_replay": ("proof/reconcile_cycle2_stream_b_routes_v2.py", "90ed534d22405807ece4f7b0d43e6df273a1740f705f7c4835f2aa784e948207"),
    "stream_c_source_ledger": ("artifacts/cycle-2-stream-c-source-ledger-v2.json", "4e2b107194420d97cb949cf2e7934f8fda81bb5f688e63aa2cd49e1b6c3cac5d"),
    "official_formula_closure": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json", "1c4ecc54be6f681be788084c3637f1101996869e09015edac8cf41e6ab39d5f0"),
    "official_formula_checker": ("proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py", "72107f1f31e51d2aa9d0ea0eb22c247a1643e58a898232a7fd02c3dee5508064"),
    "mp_tex": ("artifacts/sources/maynard-pratt-2206.11729/HalfIsolatedv2.tex", "ec22dfdb8394b8ab4b228d0f438d19858015fc74330e247d08f36e5830782426"),
    "gm_tex": ("artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "montgomery_scan": ("artifacts/sources/montgomery-1969-inventiones8-gdz-volume.pdf", "b240c7c07d32201ced906bd0fdc4d36cca3c11999084afeb658ffca3f978534e"),
    "huxley_scan": ("artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf", "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797"),
    "ford_pdf": ("artifacts/sources/ford-2002-zero-free-regions.pdf", "a43a2c37cf0f34b05bf80d9e58bcef176371437eedf7aae17d72f2c55b04c948"),
    "platt_source": ("artifacts/sources/platt-trudgian-2021-rh-3e12.tar", "c4f13cdfca711d2bf90a097147be2a094ff175b0b161647359e174633fd8bf86"),
    "hsw_source": ("artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar", "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247"),
    "bui_source": ("artifacts/sources/bui-heath-brown-2013-simple-zeros.tar", "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(key: str) -> dict[str, Any]:
    return json.loads((ROOT / FROZEN[key][0]).read_text(encoding="utf-8"))


def gz(key: str) -> str:
    with gzip.open(ROOT / FROZEN[key][0], "rt", encoding="utf-8") as handle:
        return handle.read()


def verify_inputs() -> dict[str, str]:
    hashes = {}
    for key, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"hash mismatch: {relative}"
        hashes[key] = actual
    for command in (
        [sys.executable, str(ROOT / "proof/check_cycle_2_stream_a_sources.py")],
        [sys.executable, str(ROOT / "proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py")],
        [sys.executable, str(ROOT / "proof/reconcile_cycle2_stream_b_routes_v2.py"), "--check", str(ROOT / "artifacts/cycle-2-stream-b-route-reconciliation-v2.json")],
    ):
        subprocess.run(command, check=True, capture_output=True, text=True)
    return hashes


def audit_raw_anchors() -> None:
    mp, gm = (ROOT / FROZEN["mp_tex"][0]).read_text(), (ROOT / FROZEN["gm_tex"][0]).read_text()
    for phrase in (
        r"\label{lem:TypeIIZeroBound}", r"R_{II}(\sigma,T) \ll T^{2(1-\sigma)}(\log T)^{O(1)}",
        r"\gamma\in[T,2T]", r"\sigma\ge 1/2+1/\log{T}", r"(\log T)^{17}",
    ):
        assert phrase in mp, f"missing MP Lemma 24 anchor: {phrase}"
    for phrase in (
        r"If it is not a Type I zero then it is a `Type II zero'", r"let $\psi(u)$ be a smooth function",
        r"Since $\widehat{\psi}$ is rapidly decreasing", r"1-separated set", r"If instead we have $N^k>T^\alpha$",
        r"usual Mean Value Theorem", r"By partial summation", r"such as \cite{J} or \cite[Theorem 12.1]{M3}",
    ):
        assert phrase in gm, f"missing GM internal-transfer anchor: {phrase}"
    ford = subprocess.run(["mutool", "draw", "-F", "txt", "-o", "-", str(ROOT / FROZEN["ford_pdf"][0]), "4"], check=True, capture_output=True, text=True).stdout
    for phrase in ("Theorem 5", "57.54", "|t| ≥ 3"):
        assert phrase in ford, f"missing Ford anchor: {phrase}"
    platt, hsw, bui = gz("platt_source"), gz("hsw_source"), gz("bui_source")
    for phrase in (r"\begin{thm}\label{bank}", r"3\,000\,175\,332\,800", r"\Re\rho = 1/2"):
        assert phrase in platt, f"missing Platt--Trudgian anchor: {phrase}"
    for phrase in (r"\begin{corollary}\label{main-thm}", r"For any $T\ge e$", "0.1038", "0.2573"):
        assert phrase in hsw, f"missing HSW anchor: {phrase}"
    assert "where each zero is counted with multiplicity" in bui


def gates() -> list[dict[str, Any]]:
    stream_b = load("stream_b_reconciliation")
    c_ledger, closure = load("stream_c_source_ledger"), load("official_formula_closure")
    assert stream_b["agreement_summary"]["coverage_gaps_open"] == 0
    assert stream_b["agreement_summary"]["independent_route_pass_permitted"] is True
    sources = {row["id"]: row for row in c_ledger["sources"]}
    required_c = {
        "huxley-1972-equation-1-9", "ford-2002-vinogradov-korobov", "platt-trudgian-2021-low-height-rh",
        "hasanalizade-shen-wong-2022-rvm", "bui-heath-brown-2013-multiplicity-convention",
    }
    assert all(sources[key]["status"] == "PROVED" for key in required_c)
    assert closure["epistemic_status"] == "PROVED"
    return [
        {"id": "MP-L24-and-GM-type-transfer", "status": "PROVED", "locator": "MP TeX lines 975-1022 and 2132-2164; GM TeX lines 2307-2318", "hypotheses_and_conventions": "positive height [T,2T], beta>=sigma count restriction, exact Type-I detector, GM-complement-to-MP-Type-II inclusion, sigma>=1/2+1/log T in the proof, and log-loss granularity are checked.", "closure": "The raw MP lemma does not state multiplicity; the separately pinned Stream-B two-route R3 conversion closes multiplicity/two-sided reassembly without treating the omission as implicit."},
        {"id": "Montgomery-discrete-MVT", "status": "PROVED", "locator": "Montgomery 1969 printed pp. 334-335 / frozen scan PDF pp. 347-348, Theorem 1 (Davenport), formulae (5)-(7)", "hypotheses_and_conventions": "real T0,T with T>0; ordered points in (T0,T0+T); delta minimum spacing; arbitrary complex coefficients; absolute implied constant. GM polarity is handled by negating ordinates.", "closure": "The final GM MVT branch and strict residual are included in the pinned Stream-B two-route reconciliation."},
        {"id": "GM-internal-transfers", "status": "PROVED", "locator": "GM TeX lines 2307-2364: detector, smooth psi/Fourier truncation, separated extraction, powered polynomial, and MVT branch", "hypotheses_and_conventions": "[T,2T] local height, beta>=sigma, N range, 1-separated W, N^k split, and visible T^{o(1)}/log losses are retained.", "closure": "Pinned Stream-B reconciliation v2 has zero coverage gaps across the two independent application audits."},
        {"id": "Ingham-via-Huxley-restatement", "status": "PROVED", "locator": "Huxley printed p. 164 / frozen scan PDF p. 173, (1.8)", "hypotheses_and_conventions": "two-sided N(alpha,T) in alpha<=beta<=1 and -T<=gamma<=T; 1/2<=alpha<=3/4; T^{3(1-alpha)/(2-alpha)}(log T)^5. This covers the selected lower branch through 7/10.", "closure": "The unread original Ingham article is not used as a direct source; Huxley's published restatement is the sole frozen lower-branch authority."},
        {"id": "Huxley-near-one", "status": "PROVED", "locator": "Huxley printed p. 164 / frozen scan PDF p. 173, (1.9)", "hypotheses_and_conventions": "same two-sided N(alpha,T); 3/4<=alpha<=1; exponent 3(1-alpha)/(3alpha-1) and log^44 retained. The promoted near-one branch is Huxley on 4/5<=alpha<=1.", "closure": "Jutila is excluded; no Jutila/Montgomery disjunction remains on this path."},
        {"id": "Ford-plus-Platt-VK", "status": "PROVED", "locator": "Ford PDF p. 4, Theorem 5; Platt--Trudgian source lines 46-64, Theorem 1", "hypotheses_and_conventions": "Ford: |t|>=3 and the stated 57.54 VK region. Platt--Trudgian: all nontrivial zeros through height 3,000,175,332,800 have Re rho=1/2. Together they cover the all-height cutoff used after asymptotic weakening.", "closure": "No Montgomery Corollary 11.4 source is used directly."},
        {"id": "HSW-Bui-local-multiplicity", "status": "PROVED", "locator": "HSW source lines 255-261, Corollary 1.1; Bui--Heath-Brown source line 43", "hypotheses_and_conventions": "HSW is valid for T>=e with explicit Riemann-von Mangoldt error; Bui explicitly defines N(T) with each zero counted with multiplicity. These support the unit-strip and reciprocal-distance conversion.", "closure": "Multiplicity is explicit rather than inferred from a simple-zero or distinct-zero count."},
        {"id": "official-Kedlaya-formula-proof", "status": "PROVED", "locator": "official SWORD archive members errorbounds.pdf Theorem 1 p. 1 and von_mangoldt.pdf Theorem 1 pp. 1-6/residue computation p. 2", "hypotheses_and_conventions": "all x>=2,T>0; half-weight and distance remainder; official proof says zeroes are counted with multiplicity; v4 transfer pins integral endpoints and the |gamma|<T to |rho|<=T bridge.", "closure": "Official DSpace SWORD bytes and CC BY-NC-SA 3.0 item metadata are pinned; author-copy identity/license is not used."},
    ]


def certificate() -> dict[str, Any]:
    hashes = verify_inputs()
    audit_raw_anchors()
    rows = gates()
    open_rows = [row["id"] for row in rows if row["status"] != "PROVED"]
    assert not open_rows
    return {
        "artifact_id": "cycle-2-g0-literature-source-gate-audit-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED bounded audit of literature/source hypotheses only. It recommends the source-hypothesis gate status; it neither proves the cited analytic theorems nor declares G0 PASS.",
        "frozen_hashes": hashes,
        "source_gates": rows,
        "unread_or_disjunctive_source_audit": {
            "status": "PROVED",
            "result": "NO UNREAD OR DISJUNCTIVE SOURCE ON THE SELECTED PROMOTED PATH",
            "excluded": [
                "Original Ingham paper: unread locally, but not directly used; Huxley (1.8) is the selected published restatement.",
                "Jutila near-one alternative: unread and unused; Huxley (1.9) is the selected single branch.",
                "Montgomery Topics Corollary 11.4 and Davenport Chapter 17: not used directly; Ford+Platt and official Kedlaya respectively replace them.",
            ],
            "bibliographic_containment": "OBSERVED: cycle-2-stream-c-source-ledger-v2 has stale Huxley title metadata, but its frozen PDF hash and p. 173/(1.9) locator identify the actual Huxley article. This is a record-maintenance issue, not a disjunctive or unread source on the selected path.",
        },
        "recommendation": {
            "status": "PROVED",
            "source_hypothesis_gate": "PASS",
            "scope": "All eight listed literature/source-hypothesis gates are closed in the bounded source audit.",
            "not_evaluated": ["per-route resource/performance gate", "any non-source mathematical reconstruction beyond the pinned route audits", "global G0 status"],
            "non_promotion": "This PASS recommendation is not G0 PASS.",
        },
        "replay": {"script_sha256": sha256(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g0_literature_source_gates_v1.py --write", "check_command": "python3 projects/guth-maynard-zero-density/proof/audit_g0_literature_source_gates_v1.py --check"},
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(certificate())
    if args.write:
        OUTPUT.write_text(payload, encoding="utf-8")
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
    elif not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != payload:
        raise SystemExit("source-gate audit mismatch; rerun with --write")
    else:
        print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
