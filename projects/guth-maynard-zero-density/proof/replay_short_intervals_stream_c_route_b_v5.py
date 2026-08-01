#!/usr/bin/env python3
"""Standalone v5 narrow replay of Stream-C Route B using official SWORD evidence."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "cycle-2-stream-c-route-b-v5.json"
PERFORMANCE = ROOT / "artifacts" / "cycle-2-stream-c-route-b-v5-performance.json"
B = Fraction(30, 13)
MUTOOL_VERSION = "mutool version 1.23.10"
FROZEN = {
    "source_closure_v4": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json", "1c4ecc54be6f681be788084c3637f1101996869e09015edac8cf41e6ab39d5f0"),
    "source_closure_checker_v4": ("proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py", "72107f1f31e51d2aa9d0ea0eb22c247a1643e58a898232a7fd02c3dee5508064"),
    "official_sword_independent_audit": ("artifacts/cycle-2-mit-sword-official-bitstream-audit-v1.json", "6b4bd931a33a075d39aefc905e27e24767a9a0f08b82947afdfea46accefc4b7"),
    "official_sword_independent_audit_script": ("proof/audit_mit_sword_official_bitstream_v1.py", "00e6a46e575502c4ef525ce04007b701d4535a5b4e3710dbac4f2fc6bb9cc596"),
    "route_b_v3": ("artifacts/cycle-2-stream-c-route-b-v3.json", "9eca349eae8721e1b0c80a5d54ccf75a08cc7e1fdf99ca887548891c480d53f5"),
    "route_b_v3_replay": ("proof/replay_short_intervals_stream_c_route_b_v3.py", "254899acff31f3fa4eb644ab677b13ed5c928719ab789195fe11323660556d74"),
    "route_b_v4": ("artifacts/cycle-2-stream-c-route-b-v4.json", "a8c7be629b8bff5cce4ce4a7ee5e5c1e52969b0681a45008834f7e548a8db249"),
    "official_sword_zip": ("artifacts/sources/mit-ocw-18-785-2007-sword-official.zip", "d559229963960da2087918a95af6efd7ad8999a4ba63942a12aef63c5eceac57"),
    "official_errorbounds_pdf": ("artifacts/sources/mit-ocw-18-785-2007-errorbounds-official.pdf", "b8b2acfbc4b22b25c898c0af8f74692a0d31bd6cf302e9f2d772d33a34fdd3e4"),
    "official_von_mangoldt_pdf": ("artifacts/sources/mit-ocw-18-785-2007-von-mangoldt-official.pdf", "5f705a6d3804d555944298f87a8a53e2e4e5a13188a717679f8fb8b73095210a"),
    "dspace_item_metadata": ("artifacts/sources/mit-dspace-1721.1-101679-metadata.json", "4c1f262bc51efa23993a561f908871d35245ca462df90271d0bf2127283f24c7"),
    "gm_tex": ("artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def verify() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"frozen dependency hash mismatch: {relative}"
        hashes[name] = actual
    version = subprocess.run(["mutool", "-v"], check=True, capture_output=True, text=True)
    assert (version.stdout + version.stderr).strip() == MUTOOL_VERSION, "mutool version mismatch"
    subprocess.run([sys.executable, str(ROOT / "proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py")], check=True, capture_output=True, text=True)
    subprocess.run([sys.executable, str(ROOT / "proof/audit_mit_sword_official_bitstream_v1.py"), "--check"], check=True, capture_output=True, text=True)
    subprocess.run([sys.executable, str(ROOT / "proof/replay_short_intervals_stream_c_route_b_v3.py"), "--check", str(ROOT / "artifacts/cycle-2-stream-c-route-b-v3.json")], check=True, capture_output=True, text=True)
    closure = json.loads((ROOT / FROZEN["source_closure_v4"][0]).read_text())
    audit = json.loads((ROOT / FROZEN["official_sword_independent_audit"][0]).read_text())
    v3 = json.loads((ROOT / FROZEN["route_b_v3"][0]).read_text())
    v4 = json.loads((ROOT / FROZEN["route_b_v4"][0]).read_text())
    assert closure["official_source"]["license"] == "CC BY-NC-SA 3.0"
    assert closure["official_sword_bitstream"]["uuid"] == "7292f134-d4a7-4063-bd7e-2084259b8fa9"
    assert audit["epistemic_status"] == "OBSERVED"
    assert all(row["exact_internal_to_frozen_official_bytes"] for row in audit["official_sword_zip"]["required_entries"])
    assert v3["retained_v2_nodes"]["status"] == "PROVED"
    assert v4["retained_route_b_v3_nodes"]["status"] == "PROVED"
    assert v3["exact_transfer_invariants"]["b"] == v4["exact_transfer_invariants"]["b"] == "30/13"
    return hashes


def certificate() -> dict[str, Any]:
    hashes = verify()
    one_over_b, two_over_b = Fraction(1, 1) / B, Fraction(2, 1) / B
    uniform_theta, almost_all_theta = 1 - one_over_b, 1 - two_over_b
    assert (one_over_b, two_over_b, uniform_theta, almost_all_theta) == (Fraction(13, 30), Fraction(13, 15), Fraction(17, 30), Fraction(2, 15))
    return {
        "artifact_type": "stream-c-route-b-narrow-replay-certificate",
        "certificate_version": 5,
        "supersedes": "v4 only for its source-closure-v2 provenance premise; v1-v4 remain preserved",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED narrow Stream-C Route-B pass conditional on Guth--Maynard's published zero-density theorem. This seals the official source chain and replays Route-B arithmetic; it neither re-proves the density theorem, promotes a two-route Stream-C result, nor declares G0 PASS.",
        "frozen_dependencies": hashes,
        "official_formula_source_chain": {
            "status": "PROVED",
            "source_closure": "v4, not v2",
            "provenance_correction": "The v4 premise citing source-closure v2 and CC BY-NC-SA 4.0 is not used. V5 seals source-closure v4, which records the official DSpace SWORD course metadata as CC BY-NC-SA 3.0.",
            "official_bitstream": "SWORD UUID 7292f134-d4a7-4063-bd7e-2084259b8fa9; ZIP and both official PDF members are hash-sealed.",
            "independent_audit": "The separate v1 official-SWORD audit verifies the item/bundle/bitstream chain, ZIP integrity, member paths, page counts, and anchors; its OBSERVED status is retained.",
            "renderer": MUTOOL_VERSION,
        },
        "external_truncated_explicit_formula": {
            "status": "PROVED",
            "range": "all x>=2, T>0; the Guth--Maynard deduction uses 2<=T<=x",
            "endpoint_remainder_transfer": "The v4 source closure records u=ceil(x)-1, v=floor(x+y), half-weight endpoint cost O(log x), and formula errors O(x(log x)^3/T).",
            "multiplicity_and_height": "The official proof anchors multiplicity in the residue calculation; the retained HSW/Bui node controls the |gamma|<T to literal |rho|<=T boundary-strip comparison.",
        },
        "retained_nonformula_route_b_nodes": {
            "status": "PROVED",
            "from_v3": ["Huxley corrected bibliographic/theorem node", "Ford high-height zero-free node", "Platt--Trudgian low-height zero-free node", "HSW plus Bui--Heath-Brown local-pair node"],
            "from_v4": "Only v4's retained non-formula node declaration and exact arithmetic are used; v4's source-closure-v2 provenance premise is expressly excluded.",
        },
        "exact_transfer_invariants": {"status": "PROVED", "b": q(B), "1_over_b": q(one_over_b), "2_over_b": q(two_over_b), "uniform_theta": q(uniform_theta), "almost_all_theta": q(almost_all_theta)},
        "route_conclusion": {
            "status": "PROVED narrow Stream-C Route-B pass conditional on Guth--Maynard's published zero-density theorem",
            "uniform": "Replays the published Route-B uniform threshold theta=17/30+epsilon.",
            "almost_all": "Replays the published Route-B almost-all threshold theta=2/15+epsilon.",
            "not_promoted": ["no new density exponent", "no new prime-interval exponent", "no two-route Stream-C pass", "no G0 PASS"],
        },
        "replay": {"script_sha256": sha256(Path(__file__)), "timing_policy": "No timing field occurs in this mathematical artifact; optional timing is written only by --write-performance.", "write_command": "python3 projects/guth-maynard-zero-density/proof/replay_short_intervals_stream_c_route_b_v5.py --write"},
    }


def write_performance(path: Path, started_ns: int) -> None:
    path.write_text(json.dumps({"artifact_id": "cycle-2-stream-c-route-b-v5-performance", "epistemic_status": "OBSERVED", "claim_boundary": "One host runtime observation; not mathematical evidence or an independent route.", "script_sha256": sha256(Path(__file__)), "wall_time_ns": time.perf_counter_ns() - started_ns}, indent=2, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write-performance", action="store_true")
    args = parser.parse_args()
    started_ns = time.perf_counter_ns()
    rendered = json.dumps(certificate(), indent=2, sort_keys=True) + "\n"
    if args.write:
        OUTPUT.write_text(rendered)
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
    elif args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text() != rendered:
            print("Route-B v5 certificate mismatch; rerun with --write", file=sys.stderr)
            return 1
        print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    elif args.write_performance:
        write_performance(PERFORMANCE, started_ns)
        print(f"wrote {PERFORMANCE.relative_to(ROOT)}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
