"""Seal Cycle 23's adaptive width-four finite-method boundary."""

from __future__ import annotations

from pathlib import Path

from check_cycle_23_adaptive_width_four import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle23-adaptive-width-four"
OUTPUT = ROOT / "artifacts/cycle-23-b023-lrc-adaptive-width-four-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-23-b023-lrc-adaptive-width-four-preregistration-v1.md", "ae71151c5e1c2e4ea5794e537985c7f2d13ad7d0d5d637ee100f4cf90acdf3d1"),
    "prior_artifact": (ROOT / "artifacts/cycle-22-b022-lrc-width-four-v1.json", "512ecc6f854e2400b6ee733fd2d91f8860de50a522820703d44290ad53aab58d"),
    "soundness": (ROOT / "proof/cycle_23_adaptive_width_four_soundness.md", "e6ebfbbbfb5bf3bf8177596977ddc7c0d338286501b4e83d334c12e35d463f8d"),
    "oracle": (ROOT / "discovery/lrc_adaptive_width_four_oracle.py", "dd4525e9a68da4bd4ae575481171f75813c183052ee20fac455e0bc7018a47cb"),
    "wave_zero": (ROOT / "discovery/lrc_adaptive_width_four_wave0.py", "1b5cc91c27137e35d5aefe5901dfc8f0a56b70c6ee59eb11bd3808c8bfc77104"),
    "wave_one": (ROOT / "discovery/lrc_adaptive_width_four_wave1.py", "d55b499eaa49c94c316145d326661ee3af3ad6546fbbce947a3d7719d06a0219"),
    "audit": (ROOT / "proof/check_cycle_23_adaptive_width_four.py", "c609b1b0fbc2bdc1f8b8409b3ca82ba43b719ee67e074580bb71fc254bb2f54d"),
    "test": (ROOT / "tests/test_cycle_23_adaptive_width_four.py", "66c1c96e7f028e991f442556180f163695907d8a3dbe4e7c812001b28cdc8f58"),
    "oracle_results": (OUT / "oracle.tsv", "ebdc00dafea2c4a805400627e6aff1bb4b589ca057a3eab8b3387863e4f38b93"),
    "oracle_summary": (OUT / "oracle-result.txt", "4a813b34304d679f474283ff4bce602d9dec36782490d774bce94c3e465f125d"),
    "oracle_timing": (OUT / "oracle.time", "5e86e8107a4dfb7fb56262646da02360848193958cc8377c95541f67fff60c57"),
    "wave_zero_results": (OUT / "wave0.tsv", "250a5f1dafb422ad69476bc3bb991fb14c70ae5f26c938b9415abcb86161371b"),
    "wave_zero_summary": (OUT / "wave0-result.txt", "21d1798f7d46ec0399366b21dc71131d7e280be68015c75c5d9b6dd959f21e9b"),
    "wave_zero_timing": (OUT / "wave0.time", "2562793d0af5bd232b94aa27ba5b0c27c38b609c9416981f3a19f7a2ad3898d9"),
    "wave_one_results": (OUT / "wave1.tsv", "92df7a43372c4e4f54a768f5ed90cd69c07ee661a215d339f2e665a903ef1b75"),
    "wave_one_summary": (OUT / "wave1-result.txt", "39ab26713ede0b46b46b8556601949c0c802f2963ab6d86719823b4125ef6fc6"),
    "wave_one_timing": (OUT / "wave1.time", "b22fd45b755f1462f5f8cc9021f359c2d98cc868d89c5796c0246306a98aa365"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict:
    return {
        "artifact_id": "cycle-23-b023-lrc-adaptive-width-four-v1",
        "budget_ordinal": "B023",
        "cycle": 23,
        "record_type": "OBSERVED_FINITE_METHOD_BOUNDARY_AND_SOLVER_CONTAINMENT",
        "recorded_at_utc": "2026-08-04T04:11:41Z",
        "status": "SEALED",
        "epistemic_status": "OBSERVED",
        "outcome": "The exact 200,200-partition width-four oracle transfers no Cycle-22 witness to any of the 60 survivors. Wave zero and one distinct LP-weight reselection both leave all 60 rows without an integer deficit; no leaf is newly excluded.",
        "claim_boundary": "This is a complete result only for the frozen initial witness, exact pair-savings selector, one-four-plus-three-triples partition family, one reselection, denominators, support cap, and 60 named leaves. It does not prove a width-four no-go, LP dual saturation, a primal lift, F_1, J, or LRC(13).",
        "audit": audit(),
        "proved_interface": {"epistemic_status": "PROVED", "statement": "At a no-violation termination, exhaustive cutting-plane separation has the same feasible set and optimum as the finite all-option LP; U<W remains the only promotion criterion."},
        "method_outcome": {"epistemic_status": "OBSERVED", "initial_transfers": {"need_lp": 60, "certificates": 0, "wall_seconds": 16.588814}, "wave_zero": {"need_reselect": 60, "certificates": 0, "wall_seconds": 122.443306}, "wave_one": {"distinct_reselections": 60, "unresolved": 60, "certificates": 0, "wall_seconds": 197.207038}},
        "implementation_containment": {"epistemic_status": "OBSERVED", "failure": "The original explicit all-option sparse LP used 8.65 GiB on one target and was OOM-killed at three workers; the attempted interior-point control used 8.58 GiB and was slower.", "replacement": "Deterministic exhaustive cutting-plane separation matched the simplex control objective 1.0 in 4.75 seconds and 1.0 GiB peak RSS, enabling three-worker execution.", "failed_wave_one_parse": "One first wave-one launch stopped before writing a TSV because serialized LP entries reached -3.7e-14; the preregistered retry clips only [-1e-12,0) and renormalizes before the non-proof selector."},
        "companion_decision": {"identity": "/root/darwin_cycle23_review", "scope_review": "All 60 exact oracle ties and all 60 float reselector ties are independently recomputed; no direct-CNF certificate is emitted.", "recommendation": "Seal Cycle 23 as an OBSERVED finite-method boundary and open a distinct Fourier/CRT higher-order dual cycle.", "strongest_flaw": "Pairwise savings and one reselection can miss higher-order interactions; absent certificates are not a width-four no-go.", "independent_ideas": ["Fourier/CRT low-degree nonnegative character dual", "width-five heterogeneous capacity LP after a compact control", "semantic primal assignment search only after proving its lift equivalence"], "final_action": "Seal and select the Fourier/CRT higher-order dual as the next distinct question."},
        "resources": {"aggregate_wall_seconds": 908.0, "aggregate_wall_cap_seconds": 3600, "worker_cpus": [0, 1, 2], "reserved_cpu": 3, "final_run_peak_rss_kib": 1069996, "temporary_disk_cap_bytes": 21474836480},
        "runtime": check_runtime("Cycle 23 adaptive width four"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"oracle_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_adaptive_width_four_oracle.py", "wave_zero_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_adaptive_width_four_wave0.py", "wave_one_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_adaptive_width_four_wave1.py", "audit_command": ".venv/bin/python proof/check_cycle_23_adaptive_width_four.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_23_adaptive_width_four -v", "check_command": ".venv/bin/python proof/build_cycle_23_lrc_adaptive_width_four.py --check"},
        "sealer": {"path": "proof/build_cycle_23_lrc_adaptive_width_four.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
