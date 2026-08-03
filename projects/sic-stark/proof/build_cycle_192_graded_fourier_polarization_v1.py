#!/usr/bin/env python3
"""Seal Cycle 192's graded beta-Fourier finite obstruction result."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-192-graded-fourier-polarization-v1.json"
INPUTS = {
    "prior_central_character_result": (
        ROOT / "artifacts/cycle-191-central-character-fourier-v1.json",
        "c8382814c53bb67a5fdaa14f00eb72a14e46c2a0ac1781f9744b257e385f8e3c",
    ),
    "preregistration": (
        ROOT / "docs/cycle-192-graded-fourier-polarization-preregistration-v1.md",
        "0f54677a179de1c8967544b39c210e6012c9997181862ce38b09248ccfa7bb3a",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_192_graded_fourier_polarization.py",
        "fa8b7e3a49a442b46be740aa58cf3ee49cc08f5f83fa76f75449f95ca712077b",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_192_graded_fourier_polarization.py",
        "1fed7c3764d435b0387615d435dc60b390ea221f2f16e27cf72e291d56029d18",
    ),
    "prototype": (
        ROOT / "discovery/cycle-192-graded-fourier-polarization-prototype-v1.json",
        "f27cdffa7cd43efc9c83025122445345ad7e6e6df9068eccfb3ce0a76bb495c7",
    ),
    "beta_fourier": (
        ROOT / "scripts/dimension_six_beta_fourier.py",
        "d47242027af1851ea29b60b8e8c362f42fa5a1634fd0b375e39233b4d87f7a6e",
    ),
    "beta_kernel_match": (
        ROOT / "scripts/dimension_six_beta_kernel_match.py",
        "6210819200882c83ebaed4fc74c9cce220a0d09748a8343a8b02a609d1289e27",
    ),
    "heisenberg_descent": (
        ROOT / "scripts/dimension_six_heisenberg_descent.py",
        "ccc19fd158cc4714c2d5fcbecbb5c8091c2bdbd748561aed6736482bb2dbe11f",
    ),
    "level24_blocks": (
        ROOT / "scripts/dimension_six_level24_blocks.py",
        "23d98f0bfd3d43c475e10d212ee013cd286ff73be324fcf1982466be8490603e",
    ),
    "inversion_phase": (
        ROOT / "scripts/dimension_six_inversion_phase.py",
        "30234d2e0e87b03ca7109781b193c23751e9c30de9b498972ac2c551b64282be",
    ),
    "d6_paper": (
        ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex",
        "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7",
    ),
    "scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 192 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads(
        (ROOT / "discovery/cycle-192-graded-fourier-polarization-prototype-v1.json").read_text()
    )
    closure = result["forced_closure"]
    holonomy = result["alias_holonomy_intertwining"]
    carriers = result["all36_afk_carriers"]
    obstruction = result["finite_metaplectic_polarization_obstruction"]

    require(closure["closure_dimension"] == 18, "graded closure dimension drift")
    require(
        closure["unique_smallest_F24_invariant_closure"]
        == ["B_(0,+)", "B_(0,-)", "B_(1,+)"],
        "graded closure blocks drift",
    )
    require(not closure["two_block_sum_is_F24_invariant"], "two-block failure drift")
    require(len(holonomy["records"]) == 4, "holonomy block census drift")
    p_one = next(
        record for record in holonomy["records"]
        if record["source_block"] == "B_(1,+)"
    )
    require(
        [entry["root_exponent_mod_24"] for entry in p_one["monomial_three_shift_records"]]
        == [6, 6, 6, 18, 18, 18],
        "graded holonomy phase drift",
    )
    require(carriers["rows_checked"] == 36, "AFK carrier census drift")
    require(
        carriers["carrier_counts"] == {"W_0": 12, "W_1": 6, "W_2": 6, "W_3": 12},
        "AFK carrier count drift",
    )
    require(
        carriers["capital_gamma_normalization_retained_separately"]
        and carriers["afk_phase_retained_separately"],
        "normalization/phase retention drift",
    )
    require(
        obstruction["ideal_subgroup_exponent"] == 12
        and obstruction["coefficient_subgroup_exponent"] == 24,
        "polarization exponent drift",
    )
    require(
        not obstruction["finite_metaplectic_intertwiner_exists"],
        "finite-metaplectic obstruction drift",
    )

    return {
        "artifact_id": "cycle-192-graded-fourier-polarization-v1",
        "cycle": 192,
        "budget_ordinal": "B029",
        "epistemic_status": "PROVED",
        "status": "SEALED_GRADED_FOURIER_CLOSURE_AND_FINITE_METAPLECTIC_POLARIZATION_OBSTRUCTION",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The source level-24 Fourier component sends Cycle 191's forced two central-character blocks into a unique 18-dimensional three-block Z2-graded discrete closure. It exactly transports the non-scalar alias holonomy to a three-shift (boundary-twisted on the added p=1 block). All 36 AFK samples require four coefficient-polarized carriers, and the ideal carrier subgroup has exponent 12 whereas the coefficient subgroup has exponent 24. Thus no finite Heisenberg-normalizer/metaplectic matrix-valued all-36 AFK intertwiner exists in the declared class.",
        },
        "source_block_action": result["source_block_action"],
        "forced_closure": closure,
        "alias_holonomy_intertwining": holonomy,
        "all36_afk_carriers": carriers,
        "finite_metaplectic_polarization_obstruction": obstruction,
        "gate_outcome": {
            "d6_interface": "FINITE_GRADED_FOURIER_CLOSURE_PROVED_FINITE_METAPLECTIC_AF K_INTERTWINER_OBSTRUCTED_CONTINUOUS_POLARIZATION_CHANGING_OPERATOR_REQUIRED".replace(" ", ""),
            "resolved_class": "the source F_24 block maps and all finite Heisenberg-normalizer/metaplectic operators between the declared ideal and coefficient polarizations",
            "remaining_bottleneck": "Construct a genuinely continuous, polarization-changing Z2-graded Zak/theta lift, prove its preserved function space and amplitude action, and only then test an AFK coefficient intertwiner.",
            "disallowed_pseudo_progress": [
                "calling the discrete three-block closure continuous beta-transform preservation",
                "replacing the p=1 boundary-twisted three-shift by a scalar",
                "using a finite normalizer matrix after the exponent obstruction",
                "fitting a row-dependent carrier map or coefficient",
                "discarding capital Gamma_M normalization or AFK phase",
                "claiming a boundary, Stark, fusion, or TCC consequence",
            ],
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "A source-derived continuous Z2-graded Zak/theta lift may have the 18-dimensional discrete closure as its sampled restriction and may supply a genuinely polarization-changing amplitude intertwiner; no finite-normalizer construction can do so.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "Cycle 192 PROVED the 18-dimensional three-block discrete closure, its two graded S3 actions, the four required coefficient carriers, and the exponent-12 versus exponent-24 obstruction within the finite Heisenberg-normalizer/metaplectic class.",
            "recommendation": "Seal Cycle 192; the finite normalizer question is exactly resolved, while continuous lifting changes both state space and operator class.",
            "known_flaw": "The exponent obstruction does not exclude non-normalizer integral operators and proves no continuous preservation, amplitude identity, AFK evaluation, or boundary theorem.",
            "falsifier": "Any F24 kernel/permutation, forced-pair closure, carrier-lattice, subgroup-exponent, 36-row convention, or replay discrepancy.",
            "next_action": "Open a new cycle deriving a continuous Z2-graded Zak/theta lift whose sampled restriction is the 18D closure, then test source-derived continuous preservation and coefficient-carrier intertwining exactly.",
            "adopted": True,
            "reason": "The finite operator class is completely decided by a preserved subgroup invariant; the proposed continuous lift has a different state space and proof obligation.",
        },
        "preregistration_preflight": {
            "cycle": 192,
            "manifest_sha256": sha256(ROOT / "docs/cycle-192-graded-fourier-polarization-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-192-graded-fourier-polarization-preregistration-v1.md --expected-cycle 192 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_192_graded_fourier_polarization.py --output discovery/cycle-192-graded-fourier-polarization-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_192_graded_fourier_polarization.py",
            "write_command": "python3 proof/build_cycle_192_graded_fourier_polarization_v1.py --write",
            "check_command": "python3 proof/build_cycle_192_graded_fourier_polarization_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_192_graded_fourier_polarization_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
