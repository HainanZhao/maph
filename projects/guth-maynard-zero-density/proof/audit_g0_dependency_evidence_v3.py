#!/usr/bin/env python3
"""Versioned correction and fixed-scope G0 evidence audit, v3.

This replaces neither the preserved v2 artifact nor its script.  It records
the accidental in-place v2 refresh and freezes a finite evidence scope.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "g0-dependency-evidence-matrix-v3.json"
FROZEN = {
    "post_refresh_v2_artifact": ("artifacts/g0-dependency-evidence-matrix-v2.json", "504cc31047ba8191cd1996ee7238cf3f95ab8e007f75824b39307999abb131ae"),
    "cycle1_two_route_reconciliation": ("artifacts/cycle-1-route-reconciliation-v3.json", "2a8c2a8edf06b9c5bfd0ae5d98e64a9f174555841aa41e3133850d94938943a8"),
    "stream_b_two_route_reconciliation": ("artifacts/cycle-2-stream-b-route-reconciliation-v2.json", "5aa163187d8365a72bfbc662e3e3d64a1efbdf18cdc26f150e6dee7b19e3c052"),
    "source_manifest_v3": ("artifacts/source-manifest-verification-v3.json", "cdea13dfba737cb4b065aa0de3dcc62f9afbe5fffe37837ddd27c67a6aed594b"),
    "source_manifest_v3_builder": ("proof/build_source_manifest_v3.py", "74b23bd528436b7a9651aad4654a8ed424363c11dae4325cfdb8fb5f65e21c15"),
    "official_source_closure_v4": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json", "1c4ecc54be6f681be788084c3637f1101996869e09015edac8cf41e6ab39d5f0"),
    "official_source_checker_v4": ("proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py", "72107f1f31e51d2aa9d0ea0eb22c247a1643e58a898232a7fd02c3dee5508064"),
    "official_sword_independent_audit": ("artifacts/cycle-2-mit-sword-official-bitstream-audit-v1.json", "6b4bd931a33a075d39aefc905e27e24767a9a0f08b82947afdfea46accefc4b7"),
    "official_sword_independent_audit_script": ("proof/audit_mit_sword_official_bitstream_v1.py", "00e6a46e575502c4ef525ce04007b701d4535a5b4e3710dbac4f2fc6bb9cc596"),
    "stream_c_route_a_v5": ("artifacts/cycle-2-stream-c-route-a-v5.json", "eaa6e831a147b8a509b0ddd2523515444cc3dfc6f4dc5cff0723097da047d150"),
    "stream_c_route_a_v5_replay": ("proof/replay_cycle2_stream_c_route_a_v5.py", "34cc195040d61ea7bd5bb142ad244ae21fc3a1f86b7c093cdfa00fbd5f3bf076"),
    "stream_c_route_b_v5": ("artifacts/cycle-2-stream-c-route-b-v5.json", "62b98779c5e65266ff0c81c26f312c73ce9a4462534e9d6a0395ef7fc9ed87c5"),
    "stream_c_route_b_v5_replay": ("proof/replay_short_intervals_stream_c_route_b_v5.py", "444defd7fb03b679603dd2e65cc1ac32c1810aed07c26f80036601e00f4ef6f1"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify() -> dict[str, str]:
    hashes = {}
    for name, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"frozen dependency hash mismatch: {relative}"
        hashes[name] = actual
    commands = (
        [sys.executable, str(ROOT / "proof/audit_cycle1_routes.py"), "--check", str(ROOT / "artifacts/cycle-1-route-reconciliation-v3.json")],
        [sys.executable, str(ROOT / "proof/reconcile_cycle2_stream_b_routes_v2.py"), "--check", str(ROOT / "artifacts/cycle-2-stream-b-route-reconciliation-v2.json")],
        [sys.executable, str(ROOT / "proof/build_source_manifest_v3.py"), "--check"],
        [sys.executable, str(ROOT / "proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py")],
        [sys.executable, str(ROOT / "proof/audit_mit_sword_official_bitstream_v1.py"), "--check"],
        [sys.executable, str(ROOT / "proof/replay_cycle2_stream_c_route_a_v5.py"), "--check", str(ROOT / "artifacts/cycle-2-stream-c-route-a-v5.json")],
        [sys.executable, str(ROOT / "proof/replay_short_intervals_stream_c_route_b_v5.py"), "--check"],
    )
    for command in commands:
        subprocess.run(command, check=True, capture_output=True, text=True)
    route_a = json.loads((ROOT / FROZEN["stream_c_route_a_v5"][0]).read_text())
    route_b = json.loads((ROOT / FROZEN["stream_c_route_b_v5"][0]).read_text())
    assert route_a["result_labels"]["uniform_theta"] == route_b["exact_transfer_invariants"]["uniform_theta"] == "17/30"
    assert route_a["result_labels"]["almost_all_theta"] == route_b["exact_transfer_invariants"]["almost_all_theta"] == "2/15"
    return hashes


def certificate() -> dict:
    hashes = verify()
    nodes = [
        {"id": "SOURCE-MANIFEST-V3", "status": "PROVED byte inventory replay", "evidence": ["source_manifest_v3", "source_manifest_v3_builder"], "gap": "Metadata inventory does not itself establish mathematical source authority.", "epistemic_status": "OBSERVED"},
        {"id": "CYCLE1-EXACT-ARITHMETIC", "status": "PROVED conditional exact two-route agreement", "evidence": ["cycle1_two_route_reconciliation"], "gap": "No analytic theorem is re-proved.", "epistemic_status": "OBSERVED"},
        {"id": "STREAM-B-SECTION-13.1", "status": "PROVED narrow two-route application reconciliation", "evidence": ["stream_b_two_route_reconciliation"], "gap": "Stream C and G0 are outside its claim boundary.", "epistemic_status": "OBSERVED"},
        {"id": "STREAM-C-OFFICIAL-FORMULA-CHAIN", "status": "PROVED narrow source/application closure", "evidence": ["official_source_closure_v4", "official_source_checker_v4", "official_sword_independent_audit", "official_sword_independent_audit_script"], "gap": "The independent SWORD audit remains OBSERVED provenance/anchor evidence, not a new prime theorem.", "epistemic_status": "OBSERVED"},
        {"id": "STREAM-C-ROUTE-A-V5", "status": "PROVED narrow Route-A replay conditional on GM density", "evidence": ["stream_c_route_a_v5", "stream_c_route_a_v5_replay"], "gap": "Not a full Stream-C reconciliation or G0 decision.", "epistemic_status": "OBSERVED"},
        {"id": "STREAM-C-ROUTE-B-V5", "status": "PROVED narrow Route-B replay conditional on GM density", "evidence": ["stream_c_route_b_v5", "stream_c_route_b_v5_replay"], "gap": "Not a full Stream-C reconciliation or G0 decision.", "epistemic_status": "OBSERVED"},
        {"id": "STREAM-C-V5-RECONCILIATION", "status": "OPEN", "evidence": [], "gap": "No frozen v5-versus-v5 hostile reconciliation artifact is in this fixed scope.", "epistemic_status": "OBSERVED"},
        {"id": "G0-RESOURCE-PERFORMANCE", "status": "OPEN", "evidence": [], "gap": "Route-A/B v5 performance records are intentionally mutable timing observations and do not record the preregistered complete per-route 60-second/256-MiB compliance evidence.", "epistemic_status": "OBSERVED"},
        {"id": "G0-FULL-RECONSTRUCTION", "status": "OPEN", "evidence": ["CYCLE1-EXACT-ARITHMETIC", "STREAM-B-SECTION-13.1", "STREAM-C-OFFICIAL-FORMULA-CHAIN", "STREAM-C-ROUTE-A-V5", "STREAM-C-ROUTE-B-V5"], "gap": "Withheld pending v5 hostile reconciliation and complete preregistered performance/resource evidence.", "epistemic_status": "OBSERVED"},
    ]
    return {
        "artifact_id": "g0-dependency-evidence-matrix-v3",
        "schema": 3,
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Versioned correction and fixed-scope evidence matrix. It reports sealed prior artifacts and their bounded labels, does not re-prove mathematics, and does not declare G0 PASS.",
        "v2_in_place_refresh_correction": {
            "status": "OBSERVED CORRECTION",
            "event": "The v2 builder and its v2 artifact were refreshed in place after later official-source and Route-B-v5 artifacts were added.",
            "cause": "The v2 design dynamically inventoried every artifact directly under artifacts/, and the refresh was run to admit later artifacts instead of issuing a versioned successor.",
            "affected_claims": ["v2 artifact-inventory membership and all counts", "v2 source-manifest-currentness observation", "v2 timing-artifact enumeration", "any reliance on v2 raw artifact bytes as an immutable historical evidence record"],
            "post_refresh_v2_sha256": hashes["post_refresh_v2_artifact"],
            "pre_refresh_v2_identity": "UNRECOVERABLE_FROM_LOCAL_WORKTREE: no prior v2 byte hash, immutable archive, commit, or retained correction record was found during this run; it must not be reconstructed or guessed.",
            "containment": "v2 is preserved from this point forward and is not edited by v3. This v3 artifact supplies the correction record and fixed successor scope.",
            "reruns": ["proof/audit_g0_dependency_evidence_v3.py --check", "python3 -m unittest tests/test_g0_dependency_evidence_matrix_v3.py"],
            "epistemic_status": "OBSERVED",
        },
        "fixed_scope": {
            "rule": "Only the named FROZEN inputs are checked. Newly created G1 or other future artifacts are intentionally outside scope and cannot stale this artifact.",
            "frozen_dependencies": hashes,
            "excluded_future_scope": ["all future G1 artifacts", "unlisted future artifacts", "mutable raw timing artifacts"],
            "epistemic_status": "OBSERVED",
        },
        "nodes": nodes,
        "timing_boundary": {"route_a_v5_performance": "OBSERVED, intentionally mutable and excluded from hashes", "route_b_v5_performance": "OBSERVED, intentionally mutable and excluded from hashes", "effect": "They do not supply full preregistered resource compliance.", "epistemic_status": "OBSERVED"},
        "replay": {"script_sha256": sha256(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g0_dependency_evidence_v3.py --write", "epistemic_status": "OBSERVED"},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(certificate(), indent=2, sort_keys=True) + "\n"
    if args.write:
        OUTPUT.write_text(rendered)
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
        return 0
    if not OUTPUT.is_file() or OUTPUT.read_text() != rendered:
        print("G0 v3 correction artifact mismatch; rerun with --write", file=sys.stderr)
        return 1
    print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
