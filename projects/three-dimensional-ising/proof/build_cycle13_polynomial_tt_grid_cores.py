#!/usr/bin/env python3
"""Seal the denominator-free grid TT proof and direct two-route firewall."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_polynomial_tt_grid_cores import render_latex, verify  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-13-b13-polynomial-tt-grid-cores-v1.json"
HASHES: dict[str, tuple[str, str]] = {
    "preregistration": (
        "discovery/cycle-13-polynomial-tt-preregistration.md",
        "4edc2aafff084bebfeb5edb6aa46eb4f68ea3b3fdfc90a931fcb9d87198a405b",
    ),
    "failure_ledger": (
        "discovery/failure-ledger-cycle13.md",
        "18f29ce151056454119bfd04f3948eb650d435135b889ad852dd11f862c82275",
    ),
    "label_audit": (
        "discovery/cycle-13-label-dependency-audit.md",
        "3153df174c08b52248d4345f6f93c49aacbbbe088e1329b1c6cfa1a1b6f5e026",
    ),
    "proof": (
        "proof/polynomial_tt_telescoping_proof.md",
        "c55df74246996d493579d0bfca300e993b54fe596316212d6e87e31d9d26b399",
    ),
    "verifier": (
        "proof/verify_polynomial_tt_grid_cores.py",
        "ce8b69d1d2570e971cd2d3fdce65ea93c40c1372287da448869455e8058b4082",
    ),
    "spin_reference": (
        "proof/lane_b_direct_core_reference.cpp",
        "033e007d006ed32561a0dd721027af2d76f04a02523fbe68e97821ddd66afc04",
    ),
    "tests": (
        "tests/test_polynomial_tt_grid_cores.py",
        "c93ade9fa60c26b773070e6ee3c9bec7bda0f4a566efd350abdeebad62ff150a",
    ),
    "phase_verifier": (
        "proof/verify_global_phase_telescoping.py",
        "7baaa6164f8bd4f1b6d66e47f337a34081953e1f1933a0edd79913556e7bfa91",
    ),
    "phase_tests": (
        "tests/test_global_phase_telescoping.py",
        "fba5ff275ebae64ba601c87ca3a0f9f0bba781197ff8b2ac957acf4d025b2912",
    ),
    "generated_table": (
        "paper/canonical-spin-structure-compression/polynomial-core-firewall.tex",
        "9d3c2a35234fd589a6cff00d363f221991acf20998110631e4f62f0dba994019",
    ),
    "frontier_dependency": (
        "proof/verify_lane_b_arbitrary_width_frontier.py",
        "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615",
    ),
    "canonical_dependency": (
        "proof/verify_lane_b_universal_canonical_ranks.py",
        "d631149c9429d921359a6a67042b0e476cb681b9bc8aa63de42bcac6503662b0",
    ),
    "width_dependency": (
        "proof/verify_lane_b_width_scaling.py",
        "2cb86284481e69b26bea8d9f7a52e91664a7b2b7869cdf1915795bef18926ae4",
    ),
    "homology_dependency": (
        "proof/verify_lane_b_genus3.py",
        "1f5a944a1249525ff75b4a471da73e55709de169f0e53d0540ede14b1bb298a4",
    ),
    "intersection_dependency": (
        "proof/verify_lane_b_intersection.py",
        "1b6b59d188dfdc033b1c37c0059ee3e068181c458a9da028d0a8e0f1a273abd9",
    ),
    "embedding_dependency": (
        "src/lane_b_universal_embedding.py",
        "62e57075103f4f2f252f30f9bd1e01c63820656455900b6db0b875e5294ab430",
    ),
    "recursive_dependency": (
        "src/lane_b_recursive_family.py",
        "2c945132811228cb33acc8a98d1602d3e7133c474b219ceaab73a4e8e72b171e",
    ),
    "conventions": (
        "src/conventions.py",
        "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3",
    ),
    "requirements": (
        "requirements.txt",
        "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a",
    ),
    "scaffold": (
        "proof/cycle_seal_v1.py",
        "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163",
    ),
}


def payload() -> dict[str, object]:
    replay = verify()
    replay.pop("wall_seconds")
    replay.pop("peak_rss_kib")
    rows = replay["rows"]
    if len(rows) != 12:
        raise RuntimeError("direct-core replay lost a case")
    expected = {
        ((6, 3, 3), prime, evaluation)
        for prime in (1_000_000_007, 1_000_000_009)
        for evaluation in (0, 1)
    } | {
        ((7, 3, 3), prime, evaluation)
        for prime in (1_000_000_007, 1_000_000_009)
        for evaluation in (0, 1)
    } | {
        ((4, 4, 4), prime, evaluation)
        for prime in (1_000_000_007, 1_000_000_009)
        for evaluation in (0, 1)
    }
    observed = {
        (tuple(row["shape"]), row["prime"], row["evaluation"]) for row in rows
    }
    if observed != expected:
        raise RuntimeError("direct-core replay case grid changed")
    if not replay["no_final_tensor_factorization"] or any(
        not row["direct_core_matches_independent_reference"] for row in rows
    ):
        raise RuntimeError("direct-core/reference equality regressed")
    generated = (
        ROOT
        / "paper/canonical-spin-structure-compression/polynomial-core-firewall.tex"
    )
    if generated.read_text() != render_latex({**replay, "rows": rows}):
        raise RuntimeError("checked-in polynomial-core table differs from replay")
    return {
        "artifact_id": "cycle-13-b13-polynomial-tt-grid-cores-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B13",
        "cycle": 13,
        "status": "SEALED",
        "epistemic_status": "PROVED_WITH_TWO_ROUTE_EXACT_FINITE_FIREWALL",
        "record_type": "DENOMINATOR_FREE_GRID_TT_AND_PHASE0_CLOSURE",
        "outcome": (
            "One global cochain gauge and phase potential give polynomial-ring "
            "all-sector cores of bond 2^(w^2-1). Direct parity-mask core actions "
            "agree with an independent spin-slice all-character reference in every "
            "declared two-prime, two-evaluation case."
        ),
        "gate_outcome": "PAPER_PHASE0_COMPLETE",
        "claim_boundary": (
            "The finite replay audits the construction but does not prove arbitrary "
            "width; that proof is the frozen telescoping argument. The result removes "
            "spin-structure/genus overhead only. For cubic boxes the carrier remains "
            "2^(L^2-1); no thermodynamic or homogeneous-weight conclusion follows."
        ),
        "theorem": {
            "coefficient_ring": "Z[t_e : e in E]",
            "bond": "2^(w^2-1)",
            "physical_indices": "all canonical spin-structure bits before Arf sum",
            "local_phase": "Q_j + epsilon_j H_j from one global gauge",
            "edge_counting": "every even subgraph and monomial occurs exactly once",
        },
        "exact_replay": replay,
        "benchmark": {
            "canonical_wall_seconds": 124.260542,
            "canonical_peak_rss_kib": 339784,
            "measurement_note": (
                "Recorded from the pre-seal full replay on the pinned runtime; "
                "volatile measurements are excluded from deterministic replay."
            ),
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-13-polynomial-tt-grid-cores"),
        "sealer": {
            "path": "proof/build_cycle13_polynomial_tt_grid_cores.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "verification": "python3 proof/verify_polynomial_tt_grid_cores.py",
            "tests": (
                "python3 -m unittest tests/test_polynomial_tt_grid_cores.py "
                "tests/test_global_phase_telescoping.py -v"
            ),
            "artifact_check": (
                "python3 proof/build_cycle13_polynomial_tt_grid_cores.py --check"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
