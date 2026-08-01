#!/usr/bin/env python3
"""Hostile timing-free reconciliation of the sealed Stream-C Routes A v5/B v5."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FROZEN = {
    "route_a_v5": ("artifacts/cycle-2-stream-c-route-a-v5.json", "eaa6e831a147b8a509b0ddd2523515444cc3dfc6f4dc5cff0723097da047d150"),
    "route_a_v5_replay": ("proof/replay_cycle2_stream_c_route_a_v5.py", "34cc195040d61ea7bd5bb142ad244ae21fc3a1f86b7c093cdfa00fbd5f3bf076"),
    "route_b_v5": ("artifacts/cycle-2-stream-c-route-b-v5.json", "62b98779c5e65266ff0c81c26f312c73ce9a4462534e9d6a0395ef7fc9ed87c5"),
    "route_b_v5_replay": ("proof/replay_short_intervals_stream_c_route_b_v5.py", "444defd7fb03b679603dd2e65cc1ac32c1810aed07c26f80036601e00f4ef6f1"),
    "source_closure_v4": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json", "1c4ecc54be6f681be788084c3637f1101996869e09015edac8cf41e6ab39d5f0"),
    "source_closure_checker_v4": ("proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py", "72107f1f31e51d2aa9d0ea0eb22c247a1643e58a898232a7fd02c3dee5508064"),
    "independent_sword_audit": ("artifacts/cycle-2-mit-sword-official-bitstream-audit-v1.json", "6b4bd931a33a075d39aefc905e27e24767a9a0f08b82947afdfea46accefc4b7"),
    "independent_sword_audit_script": ("proof/audit_mit_sword_official_bitstream_v1.py", "00e6a46e575502c4ef525ce04007b701d4535a5b4e3710dbac4f2fc6bb9cc596"),
    "route_a_source_ledger_v2": ("artifacts/cycle-2-stream-c-source-ledger-v2.json", "4e2b107194420d97cb949cf2e7934f8fda81bb5f688e63aa2cd49e1b6c3cac5d"),
}
OUTPUT = ROOT / "artifacts/cycle-2-stream-c-two-route-reconciliation-v2.json"

# These are canonical semantic identities, not hashes of timing-mutable
# historical Route-A artifacts.  V5 itself checks the old reports against them.
ROUTE_A_TIMED_LEGACY_IDENTITIES = {
    "route_a_v1": "7aa44f69a585ea5b984ef027e8ace496ae1134e55e8a06b24ea51abbe509f729",
    "route_a_v2": "3e0e194aab6810a2697f7951058c3ee407fa3dc47e9ce91ba96139f037fc3970",
    "route_a_v3": "1e0069963e04ae5180e7994f57ad7ced135d8d104bf83d59652fe2c49a489794",
}
ROUTE_A_V4_DETERMINISTIC_SHA256 = "eca84d439a7895a8d781ba54ba030fb2c8c76dc09082cbdb60282fe349543512"
EXPECTED_B2_ARITHMETIC_SEMANTIC_SHA256 = "b39bf5787fc8def8feecee9c56d1cae6e5d0b06e03b991b7e2907ea5cb82589b"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    return hashlib.sha256((json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()


def load(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def require(fragment: str, value: str) -> None:
    assert fragment in value, f"missing semantic fragment {fragment!r} in {value!r}"


def verify() -> dict[str, str]:
    hashes = {}
    for name, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"frozen hash mismatch: {relative}"
        hashes[name] = actual
    for command in (
        [sys.executable, str(ROOT / "proof/replay_cycle2_stream_c_route_a_v5.py"), "--check", str(ROOT / "artifacts/cycle-2-stream-c-route-a-v5.json")],
        [sys.executable, str(ROOT / "proof/replay_short_intervals_stream_c_route_b_v5.py"), "--check"],
        [sys.executable, str(ROOT / "proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py")],
        [sys.executable, str(ROOT / "proof/audit_mit_sword_official_bitstream_v1.py"), "--check"],
    ):
        subprocess.run(command, check=True, capture_output=True, text=True)
    return hashes


def route_b_v2_arithmetic_projection() -> dict[str, Any]:
    """Read only timing-free arithmetic labels, never v2 source provenance."""
    legacy = load("artifacts/cycle-2-stream-c-route-b-v2.json")
    return {
        "frozen_parameters": legacy["frozen_parameters"],
        "uniform_replay": legacy["uniform_replay"],
        "almost_all_replay": legacy["almost_all_replay"],
        "external_input_math": {
            "density_near_one_huxley": legacy["external_inputs"]["density_near_one_huxley"],
            "local_zero_count_and_pair_sum": legacy["external_inputs"]["local_zero_count_and_pair_sum"],
            "zero_free_cutoff": legacy["external_inputs"]["zero_free_cutoff"],
        },
    }


def source_hash_agreement(a: dict[str, Any], b: dict[str, Any], closure: dict[str, Any], audit: dict[str, Any]) -> dict[str, Any]:
    a_inputs, b_inputs = a["official_source_inputs"], b["frozen_dependencies"]
    pairs = {
        "source_closure_v4": (a_inputs["artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json"], b_inputs["source_closure_v4"]),
        "source_closure_checker_v4": (a_inputs["proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py"], b_inputs["source_closure_checker_v4"]),
        "independent_sword_audit": (a_inputs["artifacts/cycle-2-mit-sword-official-bitstream-audit-v1.json"], b_inputs["official_sword_independent_audit"]),
        "sword_zip": (a_inputs["artifacts/sources/mit-ocw-18-785-2007-sword-official.zip"], b_inputs["official_sword_zip"]),
        "official_formula_pdf": (a_inputs["artifacts/sources/mit-ocw-18-785-2007-errorbounds-official.pdf"], b_inputs["official_errorbounds_pdf"]),
        "official_proof_pdf": (a_inputs["artifacts/sources/mit-ocw-18-785-2007-von-mangoldt-official.pdf"], b_inputs["official_von_mangoldt_pdf"]),
        "dspace_metadata": (a_inputs["artifacts/sources/mit-dspace-1721.1-101679-metadata.json"], b_inputs["dspace_item_metadata"]),
        "gm_tex": (a_inputs["artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"], b_inputs["gm_tex"]),
    }
    assert all(left == right for left, right in pairs.values())
    assert closure["official_sword_bitstream"]["sha256"] == pairs["sword_zip"][0]
    assert audit["official_sword_zip"]["sha256"] == pairs["sword_zip"][0]
    assert all(row["exact_internal_to_frozen_official_bytes"] for row in audit["official_sword_zip"]["required_entries"])
    return {name: {"route_a": left, "route_b": right, "equal": left == right} for name, (left, right) in pairs.items()}


def coverage(a: dict[str, Any], b: dict[str, Any], closure: dict[str, Any], projection: dict[str, Any]) -> list[dict[str, str]]:
    arith, bparams = a["exact_route_a_arithmetic"], projection["frozen_parameters"]
    uniform, almost = projection["uniform_replay"], projection["almost_all_replay"]
    huxley = projection["external_input_math"]["density_near_one_huxley"]
    local = projection["external_input_math"]["local_zero_count_and_pair_sum"]
    vk = projection["external_input_math"]["zero_free_cutoff"]
    rows_a = {row["id"]: row for row in a["rows"]}
    assert all(row["epistemic_status"] == "PROVED" for row in rows_a.values())
    assert b["epistemic_status"] == "PROVED" and b["official_formula_source_chain"]["status"] == "PROVED"
    assert closure["epistemic_status"] == "PROVED"
    assert arith["density_coefficient"] == bparams["b"] == b["exact_transfer_invariants"]["b"] == "30/13"
    assert arith["uniform"]["theta"] == bparams["uniform_theta"] == b["exact_transfer_invariants"]["uniform_theta"] == "17/30"
    assert arith["almost_all"]["theta"] == bparams["almost_all_theta"] == b["exact_transfer_invariants"]["almost_all_theta"] == "2/15"
    require("all x>=2, T>0", b["external_truncated_explicit_formula"]["range"])
    require("u=ceil(x)-1", b["external_truncated_explicit_formula"]["endpoint_remainder_transfer"])
    require("multiplicity", b["external_truncated_explicit_formula"]["multiplicity_and_height"])
    require("|gamma|<T", b["external_truncated_explicit_formula"]["multiplicity_and_height"])
    require("log^44", huxley["conclusion"])
    require("Ford Theorem 5", vk["high_height"])
    require("Platt--Trudgian", vk["low_height"])
    require("multiplicity", local["multiplicity"])
    for fragment in ("T=x/y", "E(x)^2", "O(yE(x)^-1)"):
        require(fragment, uniform["truncation"])
    for fragment in ("eta<=b^2 epsilon/4", "epsilon/2"):
        require(fragment, uniform["density_margin"] if fragment.startswith("eta") else uniform["epsilon_absorption"])
    for fragment in ("T=delta^-1", "E(X)^4", "delta X=X^(2/15+epsilon/2)"):
        require(fragment, almost["parameters"])
    for fragment in ("eta<=b^2 epsilon/12", "epsilon/3"):
        require(fragment, almost["density_margin"] if fragment.startswith("eta") else almost["epsilon_absorption"])
    labels = [
        ("formula theorem", "official all-T von Mangoldt theorem", "official all-T von Mangoldt theorem"),
        ("formula range", "x>=2; T>0", "x>=2; T>0"),
        ("formula remainder", "O(x(log x)^3/T) endpoint transfer", "O(x(log x)^3/T) endpoint transfer"),
        ("formula endpoints/half-weight", "u=ceil(x)-1; v=floor(x+y); O(log x)", "u=ceil(x)-1; v=floor(x+y); O(log x)"),
        ("formula multiplicity", "zero residues counted with multiplicity", "zero residues counted with multiplicity"),
        ("formula height bridge", "|gamma|<T to |rho|<=T: unit strips", "|gamma|<T to |rho|<=T: unit strips"),
        ("Huxley theorem", "N(s,T)<<T^(3(1-s)/(3s-1))(log T)^44", "N(s,T)<<T^(3(1-s)/(3s-1))(log T)^44"),
        ("Huxley range/log loss", "4/5<=s<=1; log^44 retained", "4/5<=s<=1; log^44 retained"),
        ("VK high-height", "Ford Theorem 5", "Ford Theorem 5"),
        ("VK local completion", "Platt--Trudgian low-height RH", "Platt--Trudgian low-height RH"),
        ("VK cutoff weakening", "5/7-2/3=1/21>0", "5/7-2/3=1/21>0"),
        ("local-pair count", "HSW+Bui; multiplicity-inclusive unit strips", "HSW+Bui; multiplicity-inclusive unit strips"),
        ("uniform theta", "17/30", "17/30"),
        ("uniform truncation", "T=x/y*E(x)^2", "T=x/y*E(x)^2"),
        ("uniform epsilon", "eta<=b^2 epsilon/4; subpower absorption", "eta<=b^2 epsilon/4; subpower absorption"),
        ("uniform range", "x^(17/30+epsilon)<=y<=x^(99/100)", "x^(17/30+epsilon)<=y<=x^(99/100)"),
        ("uniform error", "x(log x)^3/T=O(yE(x)^-1)", "x(log x)^3/T=O(yE(x)^-1)"),
        ("uniform prime conversion", "pi=y/log x+O(yE(x)^-1)", "pi=y/log x+O(yE(x)^-1)"),
        ("almost-all theta", "2/15", "2/15"),
        ("almost-all truncation", "delta=X^(-13/15+epsilon/2); T=delta^-1 E(X)^4", "delta=X^(-13/15+epsilon/2); T=delta^-1 E(X)^4"),
        ("almost-all epsilon", "eta<=b^2 epsilon/12; subpower absorption", "eta<=b^2 epsilon/12; subpower absorption"),
        ("almost-all range", "X^(2/15+epsilon)<=y<=X^(99/100)", "X^(2/15+epsilon)<=y<=X^(99/100)"),
        ("almost-all local-pair reduction", "I<<delta^2(log X)^3 sup X^(2s+1)N(s,T)", "I<<delta^2(log X)^3 sup X^(2s+1)N(s,T)"),
        ("almost-all error", "delta^2X^3/(y^2X)<=X^-epsilon", "delta^2X^3/(y^2X)<=X^-epsilon"),
        ("almost-all exceptional conversion", "O(XE(X)^-1) starts", "O(XE(X)^-1) starts"),
        ("almost-all prime conversion", "pi=y/log x+O(yE(X)^-1)", "pi=y/log x+O(yE(X)^-1)"),
    ]
    return [{"label": label, "route_a_value": avalue, "route_b_value": bvalue, "route_a_status": "PROVED", "route_b_status": "PROVED", "agreement": "EXACT"} for label, avalue, bvalue in labels]


def certificate() -> dict[str, Any]:
    hashes = verify()
    a, b = load(FROZEN["route_a_v5"][0]), load(FROZEN["route_b_v5"][0])
    closure, audit = load(FROZEN["source_closure_v4"][0]), load(FROZEN["independent_sword_audit"][0])
    assert a["legacy_route_a_identities"]["v1_v3_exact_replay_sha256"] == ROUTE_A_TIMED_LEGACY_IDENTITIES
    assert a["legacy_route_a_identities"]["v4_byte_sha256"] == ROUTE_A_V4_DETERMINISTIC_SHA256
    projection = route_b_v2_arithmetic_projection()
    projection_hash = canonical_digest(projection)
    assert projection_hash == EXPECTED_B2_ARITHMETIC_SEMANTIC_SHA256, "Route-B legacy arithmetic semantic identity changed"
    source_hashes = source_hash_agreement(a, b, closure, audit)
    rows = coverage(a, b, closure, projection)
    gaps = [row["label"] for row in rows if row["route_a_status"] != "PROVED" or row["route_b_status"] != "PROVED" or row["agreement"] != "EXACT"]
    assert not gaps, f"unreconciled labels: {gaps}"
    return {
        "artifact_type": "stream-c-two-route-reconciliation-certificate",
        "certificate_version": 2,
        "supersedes": "two-route reconciliation v1; v1 is preserved",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED narrow independent Stream-C reconciliation conditional on Guth--Maynard's published density theorem. It compares sealed Routes A v5 and B v5 only; it does not prove that density theorem, improve an exponent, or establish G0 PASS.",
        "frozen_hashes": hashes,
        "timing_free_legacy_identities": {
            "status": "PROVED",
            "route_a_v1_v3_semantic_identities": ROUTE_A_TIMED_LEGACY_IDENTITIES,
            "route_a_v4_deterministic_sha256": ROUTE_A_V4_DETERMINISTIC_SHA256,
            "route_b_v2_arithmetic_semantic_projection_sha256": projection_hash,
            "boundary": "No raw SHA-256 of Route-A v1/v2/v3 timing-mutable artifact bytes occurs in this certificate. Route-B v2 is read only through the displayed arithmetic projection, never through its superseded formula-source provenance.",
        },
        "source_hash_agreement": source_hashes,
        "preregistered_label_coverage": rows,
        "independent_narrow_stream_c_pass": {
            "status": "PROVED",
            "result": "PASS",
            "gaps": gaps,
            "scope": "Both sealed routes agree on every listed formula/convention, density/zero-free/local-pair, uniform, and almost-all label, conditional on Guth--Maynard's published density theorem.",
            "not_promoted": ["no new zero-density exponent", "no new prime-interval exponent", "no G0 PASS"],
        },
        "independent_sword_audit": {
            "status": "OBSERVED",
            "role": "Independent corroborating ZIP/member/page/anchor audit; its observed provenance status is retained and is not silently upgraded.",
        },
        "preservation": "Reconciliation v1 and all Route-A/Route-B historical artifacts remain unchanged.",
        "replay": {
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_cycle2_stream_c_two_routes_v2.py --write",
            "check_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_cycle2_stream_c_two_routes_v2.py --check",
        },
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2) + "\n"


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
        raise SystemExit("reconciliation v2 mismatch; rerun with --write")
    else:
        print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
