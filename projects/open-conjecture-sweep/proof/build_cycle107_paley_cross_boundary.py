#!/usr/bin/env python3
"""Seal C107's fixed-Paley-cross bi-translation obstruction."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256

OUT = ROOT / "artifacts/cycle-107-b107-book-ramsey-paley-cross-boundary-v1.json"
H = {
    "prereg": ("docs/cycle-107-b107-book-ramsey-paley-cross-preregistration-v1.md", "5f3760ea5159daa7d0ba5a953641cc16474947e55c8983bd0d1334c469705bf1"),
    "selection": ("discovery/cycle107_oracle_paley_cross_selection.md", "2a33bcd86002d4999cbfd9f2ed1cedf29c53e992a69a1766894050db73a1fdc9"),
    "source_audit": ("discovery/f001_dai_lin_2026_source_audit.md", "d1d1944f7582b44bfda953e6d2862070bf0d705aa584c43ba659b9a8c19a4824"),
    "proof": ("proof/cycle107_paley_cross_proof.md", "00225bcbe2249046f3f6f2555c9ee52bb60ac534eed79c3643af72c51fcc736c"),
    "checker": ("proof/check_cycle107_paley_cross.py", "202c8716d3e984dcaa413e80ec8b54538c28fd54be4b27f46b0d5555b4f4bbf2"),
    "check": ("discovery/out/cycle107-paley-cross-check.json", "47b5cb47998936792b5bc98fb1196c9186963fd9047288e42254e766be4e3065"),
    "prior": ("artifacts/cycle-106-b106-book-ramsey-mixed-reflection-boundary-v1.json", "132739c195b5ca5df036e2c8b1748f7a31b0ceab80f044103bd83cbfce53676f"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload():
    audit = json.loads((ROOT / H["check"][0]).read_text())
    require(audit["status"] == "PASS", "checker did not pass")
    require(
        [(r["q"], r["shifts_checked"], r["all_forced_values_non_even_integral"]) for r in audit["controls"]]
        == [(7, 7, True), (23, 23, True)],
        "control coverage drift",
    )
    return {
        "artifact_id": "cycle-107-b107-book-ramsey-paley-cross-boundary-v1",
        "cycle": 107,
        "budget_ordinal": "B107",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "record_type": "UNIFORM_METHOD_FAMILY_OBSTRUCTION",
        "outcome": "For every prime power q=7 mod 8, the fixed-Paley-cross two-layer translation Seidel state with independent symmetric within-layer blocks of row sum -2 cannot meet the frozen off-diagonal Seidel-square condition.",
        "claim_boundary": "Only the displayed fixed-Paley-cross two-layer translation state; not other cross kernels, nontranslation constructions, conference/PC-graph constructions, or book Ramsey generally.",
        "audit": audit,
        "frozen_hashes": freeze_inputs(ROOT, {k: (ROOT / p, h) for k, (p, h) in H.items()}),
        "runtime": check_runtime("c107"),
        "sealer": {"path": "proof/build_cycle107_paley_cross_boundary.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "proof": "sed -n '1,220p' proof/cycle107_paley_cross_proof.md",
            "checker": "python3 proof/check_cycle107_paley_cross.py",
            "check": "python3 proof/build_cycle107_paley_cross_boundary.py --check",
        },
        "cycle_decision": {
            "decision": "Seal and close C107.",
            "stop": "Do not patch with restricted P_i or a subset census; a successor must change the cross kernel or leave two-layer translation invariance.",
            "falsifier": "An admissible P0,P1,c satisfying the forced equation or a failure of the Paley and matrix identities.",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUT, payload_factory=payload))
