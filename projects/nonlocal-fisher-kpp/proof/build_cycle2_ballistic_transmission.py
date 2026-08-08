#!/usr/bin/env python3
"""Seal the Cycle-2 frozen-barrier ballistic transmission theorem."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-2-b002-frozen-ballistic-transmission-v1.json"
INPUTS = {
    "mathematical_record": (
        "proof/frozen_barrier_ballistic_transmission.md",
        "55bac53a96949c7f5b6aae5f9d7974862d1f1f51309163a1203ea0352b40b91e",
    ),
    "exact_step_audit": (
        "proof/verify_ballistic_transmission.py",
        "b9a0584543507fa49b70272ad597002648666ae3b8b2b37bb8b0e1f95423a7ca",
    ),
    "sealing_scaffold": (
        "proof/cycle_seal_v1.py",
        "2061713b05a9c2a64677a7fd504d6c987ecae7ef9cf46da218b803d92b0816d6",
    ),
    "scaffold_test": (
        "proof/test_cycle_seal_v1.py",
        "13b7c93eaadba30e33a39aa0ad3e31431af5ec47296aa30e0d6df0639e55be04",
    ),
}


def run_json(relative: str) -> dict[str, object]:
    output = subprocess.check_output(
        [sys.executable, str(ROOT / relative)], cwd=ROOT, text=True
    )
    return json.loads(output)


def payload() -> dict[str, object]:
    exact = run_json("proof/verify_ballistic_transmission.py")
    scaffold = run_json("proof/test_cycle_seal_v1.py")
    require(exact.get("status") == "PASS", "step-barrier audit failed")
    require(
        exact.get("ballistic_interface_transmission") == "2/3",
        "step transmission mismatch",
    )
    require(scaffold.get("status") == "PASS", "scaffold self-test failed")
    return {
        "artifact_id": "cycle-2-b002-frozen-ballistic-transmission-v1",
        "budget_ordinal": "B002",
        "cycle": 2,
        "record_type": "THEOREM_AND_METHOD_CORRECTION",
        "recorded_at_utc": "2026-08-08T13:42:28Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": (
            "For q_t=q_xx+(1-C)q, the critical-ray coefficient at x=2t+s "
            "is the drift-two survival-weighted moment integral e^y H_C(y) "
            "q_0(y)dy. The same weight is an exact generalized moment."
        ),
        "theorem": {
            "ray_limit": (
                "sqrt(4*pi*t)*exp(s)*q(t,2*t+s) -> "
                "integral exp(y)*H_C(y)*q_0(y)dy"
            ),
            "transmission_ode": "H_C''+2*H_C'-C*H_C=0; H_C(+infinity)=1",
            "generalized_eigenfunction": (
                "phi_C=exp(x)*H_C; phi_C''+(1-C)*phi_C=2*phi_C"
            ),
        },
        "claim_boundary": (
            "The potential C is frozen, bounded, nonnegative, and exponentially "
            "decaying to the unpopulated side. This does not justify freezing "
            "K*u during nonlinear hump formation, prove seed universality, "
            "select a wavelength, or prove P1/P2."
        ),
        "cycle_decision": {
            "abandoned": (
                "The zero-energy scattering fixed point L=z_L; it samples the "
                "diffusive spectral edge rather than the ballistic critical ray."
            ),
            "surviving_state": (
                "The ballistic transmission function H_C together with the "
                "incoming exponentially weighted seed moment."
            ),
            "next_falsifier": (
                "Two admissible nonlinear formation histories with the same "
                "proposed hump state but different leading transmission moments."
            ),
        },
        "published_dependency": {
            "source": "Barry Simon, A Feynman-Kac Formula for Unbounded Semigroups",
            "identifier": "arXiv:math-ph/9907022",
            "result": "Theorem 1.1",
            "hypothesis_check": (
                "C is continuous and bounded nonnegative, hence the corresponding "
                "Schrodinger potential is continuous and bounded below; the "
                "generator normalization differs by a factor-two time rescaling."
            ),
            "use": "Brownian-bridge heat-kernel representation only",
        },
        "audit": {"exact_step_barrier": exact, "scaffold": scaffold},
        "frozen_hashes": freeze_inputs(
            ROOT,
            {label: (ROOT / path, digest) for label, (path, digest) in INPUTS.items()},
        ),
        "runtime": check_runtime("cycle-2 frozen ballistic transmission"),
        "sealer": {
            "path": "proof/build_cycle2_ballistic_transmission.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "exact_step_audit": "python3 proof/verify_ballistic_transmission.py",
            "scaffold_test": "python3 proof/test_cycle_seal_v1.py",
            "artifact_check": (
                "python3 proof/build_cycle2_ballistic_transmission.py --check"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(
        run_cli(description=__doc__, output=OUTPUT, payload_factory=payload)
    )
