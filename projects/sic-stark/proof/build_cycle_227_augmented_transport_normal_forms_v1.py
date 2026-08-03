#!/usr/bin/env python3
"""Seal Cycle 227/B064's augmented-transport normal-form result."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_227_augmented_transport_normal_forms import run as normal_form_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-227-b064-augmented-transport-normal-forms-v1.json"
INPUTS = {
    "positive_scaling": (ROOT / "artifacts/cycle-218-b055-signed-period-cover-v1.json", "7b456c630bbcc40c632c4b8b0a9ffe0aa128a6bbacf51813a7b029bb13da40a6"),
    "prior_groupoid": (ROOT / "artifacts/cycle-226-b063-signed-product-groupoid-v1.json", "c1c3fd23d20a3cd2e40a84dda8e0fade3b1aa873d5c8b66a2b532a1c79fb516c"),
    "preregistration": (ROOT / "docs/cycle-227-b064-augmented-transport-normal-forms-preregistration-v1.md", "5b3d031a1f449fef293211a2a6437c5f2a214d1dd0e1933b9686ff570eb4a00d"),
    "prior_transport": (ROOT / "proof/verify_cycle_226_signed_product_groupoid.py", "51eb9d4f07b7c6a2a19ac4229d84badac876adfa0ca394a1cf2d5b2a5a5132b9"),
    "prior_scaling_replay": (ROOT / "proof/verify_cycle_218_signed_period_cover.py", "8fca003418e205595fa2474449574b7e2577a59e768d065df1eb663ccff7ddb3"),
    "replay": (ROOT / "proof/verify_cycle_227_augmented_transport_normal_forms.py", "973fc04edd953d840a84d41647ad44279eb49b55944cc3de143b83f22dd5513c"),
    "regression_test": (ROOT / "tests/test_cycle_227_augmented_transport_normal_forms.py", "d3b59cceb01a6be18b2330e5ba4275e5ab2564ae205abe160d64aa8b1b8794b4"),
    "prototype": (ROOT / "discovery/cycle-227-b064-augmented-transport-normal-forms-prototype-v1.json", "3af3a057f5144d7db6b3da2189a5c92c08b9738715341066037b7f48f1a2d0b1"),
    "source_audit": (ROOT / "scripts/dimension_six_ss_evaluation_audit.py", "24c9258e46a1233c552017f3b58de0d45acd0197c8c807579f090ca1332f626f"),
    "source_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    frozen = freeze_inputs(ROOT, INPUTS)
    result = normal_form_run()
    normal = result["normal_form_audit"]
    quotient = result["quotient_audit"]
    require(normal["rows_checked"] == 32764, "normal-form census drift")
    require(normal["all_rows_match_closed_form"], "normal form failure")
    require(len(normal["paired_generator_induction"]["rows"]) == 16, "paired induction drift")
    require(quotient["generic_full_label_scaling_quotient_count"] == 0, "unearned generic quotient")
    require(quotient["zero_label_candidate_count"] == 12, "zero-label quotient census drift")
    require(all(row["ordinary_gamma_factors_retained"] > 0 for row in quotient["zero_label_product_node_scaling_candidates"]), "residual word lost")
    return {
        "artifact_id": "cycle-227-b064-augmented-transport-normal-forms-v1",
        "cycle": 227,
        "budget_ordinal": "B064",
        "epistemic_status": "PROVED",
        "status": "SEALED_AUGMENTED_TRANSPORT_NORMAL_FORM_AND_SCALING_BOUNDARY",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The augmented F2/F3 transport has an exact parity/576/affine-sign normal form; generic labels admit no C218 scaling quotient, while m=0 positive F3-even product-node returns retain their ordinary-gamma residual words."},
        "normal_form_audit": normal,
        "quotient_audit": quotient,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The paired-generator induction, 32,764-row census, raw parity, period scaling, affine sign, label reset, source-path classification, m=0 specialization, and residual ordering/count were reviewed together.",
            "recommendation": "Seal C227 as the completed normal-form/quotient block and open a new cycle; residual-word reduction introduces a distinct ordinary-gamma identity engine.",
            "known_flaw": "The bounded census is not itself the theorem, and the m=0 product-node returns neither preserve generic labels nor close a factorization/cochain loop while 4j residual factors remain.",
            "falsifier": "Any paired-generator induction, raw parity, period scaling, affine sign, label-reset, source-path classification, m=0 specialization, residual ordering/count, or replay discrepancy invalidates the seal.",
            "next_action": "Preregister the minimal F3^2 residual block at m=0 for starts A and C, admit only source-cited ordinary-gamma reflection/multiplication identities, and test whether its four factors reduce to a scalar/cocycle before attempting the full residual monoid.",
            "adopted": True,
            "reason": "The normal-form and quotient question is complete; residual-word reduction is a different formula family and must be frozen separately.",
        },
        "preregistration_preflight": {"cycle": 227, "manifest_sha256": sha256(ROOT / "docs/cycle-227-b064-augmented-transport-normal-forms-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-227-b064-augmented-transport-normal-forms-preregistration-v1.md --expected-cycle 227 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_227_augmented_transport_normal_forms.py --output discovery/cycle-227-b064-augmented-transport-normal-forms-prototype-v1.json", "test_command": "python3 -m unittest tests/test_cycle_227_augmented_transport_normal_forms.py", "write_command": "python3 proof/build_cycle_227_augmented_transport_normal_forms_v1.py --write", "check_command": "python3 proof/build_cycle_227_augmented_transport_normal_forms_v1.py --check"},
        "runtime": check_runtime("Cycle 227 seal"),
        "sealer": {"path": "proof/build_cycle_227_augmented_transport_normal_forms_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
