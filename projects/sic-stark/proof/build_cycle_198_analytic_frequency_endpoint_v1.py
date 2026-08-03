#!/usr/bin/env python3
"""Seal Cycle 198/B035's source analytic-frequency endpoint functional."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json"
INPUTS = {
    "prior_gaussian_falsifier": (
        ROOT / "artifacts/cycle-197-b034-gaussian-abel-tail-v1.json",
        "f18e2fdfad7f98551171cd9dc7b1d06dd0d4e76e13ee158a25e8009ab0ad198f",
    ),
    "prior_characteristic_interface": (
        ROOT / "artifacts/cycle-189-regularized-jacobi-lens-interface-v1.json",
        "f46b6bedbef2ac8fbdf63da7864879086ce72dba8becb534f0bc9c20d9725da7",
    ),
    "preregistration": (
        ROOT / "docs/cycle-198-b035-analytic-frequency-endpoint-preregistration-v1.md",
        "87192319a66c1c2f9a2d0307905634f46cc83d9a76090288c90834b45edf5c0a",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_198_analytic_frequency_endpoint.py",
        "fd659f66af2d31dbe1e94d6956a22be211ce279cfb93253ee91e0fb2bebb169d",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_198_analytic_frequency_endpoint.py",
        "277cb9e9a5644b7c7724f07ed7673a7c51d382d8ca82f315158fea26ccf7d2f8",
    ),
    "prototype": (
        ROOT / "discovery/cycle-198-b035-analytic-frequency-endpoint-prototype-v1.json",
        "a37aacb8419d7a0e4f71fd092bd28c9d0ad69f338df309b89348f9b40a4738cc",
    ),
    "beta_fourier": (
        ROOT / "scripts/dimension_six_beta_fourier.py",
        "d47242027af1851ea29b60b8e8c362f42fa5a1634fd0b375e39233b4d87f7a6e",
    ),
    "beta_kernel_match": (
        ROOT / "scripts/dimension_six_beta_kernel_match.py",
        "6210819200882c83ebaed4fc74c9cce220a0d09748a8343a8b02a609d1289e27",
    ),
    "helical_dual_crosscheck": (
        ROOT / "scripts/dimension_six_helical_zak.py",
        "185f79ae0c3e5b560939a81551877cf0d14401100466793cc2d7fa4973061bf0",
    ),
    "d6_paper": (
        ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex",
        "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7",
    ),
    "source_hypothesis_audit": (
        ROOT / "docs/sic-stark-cycle146.md",
        "32a8f4cf4d64e1137ef09807683475aac9f8978397703be81fe7ce670cd367bd",
    ),
    "scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 198 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads(
        (
            ROOT
            / "discovery/cycle-198-b035-analytic-frequency-endpoint-prototype-v1.json"
        ).read_text()
    )
    ledger = result["characteristic_ledger"]
    functional = result["endpoint_functional"]
    require(ledger["row_count"] == 36, "characteristic census drift")
    require(
        ledger["distinct_continuous_discrete_character_count"] == 36,
        "test-space injectivity drift",
    )
    require(
        ledger["all_36_endpoint_values_finite_nonzero"],
        "endpoint divisor audit drift",
    )
    require(
        ledger["zero_frequency_N_mod_24"] == [2, 6, 10, 14, 18, 22],
        "zero-frequency label drift",
    )
    require(
        functional["unique_under_frozen_source_rule"]
        and not functional["ordinary_raw_contour_value"],
        "continuation claim boundary drift",
    )
    return {
        "artifact_id": "cycle-198-b035-analytic-frequency-endpoint-v1",
        "cycle": 198,
        "budget_ordinal": "B035",
        "epistemic_status": "PROVED",
        "status": "SEALED_SOURCE_ANALYTIC_FREQUENCY_ENDPOINT_FUNCTIONAL_ON_T6",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "Sarkissian--Spiridonov equation (66), continued "
                "meromorphically from its source convergence chamber, defines "
                "a unique linear endpoint transform on the frozen 36-character "
                "space T_6. The exact helical lift is injective and all 72 "
                "frequency Gamma_M factors plus Gamma_M(Q,0) are finite and "
                "nonzero."
            ),
        },
        "endpoint_parameters": result["endpoint_parameters"],
        "source_continuation": result["source_continuation"],
        "fixed_Gamma_M_Q_0": result["fixed_Gamma_M_Q_0"],
        "characteristic_ledger": ledger,
        "endpoint_functional": functional,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Promote and seal C198/B035 as PROVED only for the unique "
                "equation-(66) meromorphic endpoint functional on frozen T_6; "
                "advance the gate to helical/Zak amplitude matching."
            ),
            "known_flaw": (
                "Uniqueness of the source transform on T_6 does not identify "
                "its values with a periodized beta channel, AFK coefficients, "
                "Stark data, fusion, or TCC."
            ),
            "falsifier": (
                "Any equation-(66) hypothesis or normalization, helical-lift "
                "injectivity, divisor-finiteness, zero-mode, connected-domain, "
                "identity-theorem, or replay discrepancy."
            ),
            "next_action": (
                "Preregister a source-derived Zak/periodization map from the "
                "full 24-dimensional theta carrier to T_6 and test exact "
                "amplitude equality, preserving all phases and zero modes "
                "without fitted scalars."
            ),
            "adopted": True,
            "reason": (
                "The source theorem, exact all-row lift, and divisor audit close "
                "the narrowly frozen endpoint-definition gate while leaving "
                "the amplitude and arithmetic interfaces explicit."
            ),
        },
        "preregistration_preflight": {
            "cycle": 198,
            "manifest_sha256": sha256(
                ROOT
                / "docs/cycle-198-b035-analytic-frequency-endpoint-preregistration-v1.md"
            ),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check "
                "docs/cycle-198-b035-analytic-frequency-endpoint-preregistration-v1.md "
                "--expected-cycle 198 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_198_analytic_frequency_endpoint.py "
                "--output discovery/cycle-198-b035-analytic-frequency-endpoint-prototype-v1.json"
            ),
            "test_command": (
                "python3 -m unittest "
                "tests/test_cycle_198_analytic_frequency_endpoint.py "
                "tests/test_cycle_197_gaussian_abel_tail.py"
            ),
            "write_command": (
                "python3 proof/build_cycle_198_analytic_frequency_endpoint_v1.py --write"
            ),
            "check_command": (
                "python3 proof/build_cycle_198_analytic_frequency_endpoint_v1.py --check"
            ),
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_198_analytic_frequency_endpoint_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(
        run_cli(description=__doc__, output=OUTPUT, payload_factory=payload)
    )
