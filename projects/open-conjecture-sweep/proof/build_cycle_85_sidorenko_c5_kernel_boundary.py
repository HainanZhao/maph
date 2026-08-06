"""Seal C85's bounded C5 triple-kernel method boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-85-b085-sidorenko-c5-kernel-boundary-v1.json"
HASHES = {
    "preregistration": ("docs/cycle-85-b085-sidorenko-c5-kernel-preregistration-v1.md", "f5e7f7b077dfa7578754e50568afeeaf8eb19db7584f5405b59df5f1662b299b"),
    "idea_selection": ("discovery/cycle85_sidorenko_tensor_selection.md", "6b21dfcbc48c76c6611f1ddb7a212de10b8a13f6775d97d27cfde78109a4bf6b"),
    "source_audit": ("discovery/cycle85_sidorenko_source_audit.md", "41621d7a8b90c1886db0e1ad5c3b0919dbbd1f72907a74e88be3660db293b674"),
    "symbolic_cap": ("discovery/cycle85_symbolic_cap.md", "d525b7f30389e5c2e2a1a034ca4b0eff2fb1572708e278db310f8b5ac39da6ae"),
    "eligibility_audit": ("discovery/problem2_eligibility_audit.md", "196c30a07951a091fefd10d1d2550e111d614664f3aea7fc70eebe9b70fc3250"),
    "kernel_checker": ("proof/check_cycle85_c5_kernel.py", "e38d6ace9f318c8034374701933a1a0243b96ad25319b62b7abe8de00a30613e"),
    "direct_checker": ("proof/check_cycle85_direct_bigraphon.py", "cf6326372e0568af0e8b004471a74ab9f98dace2ea333f028b399577a7f8146d"),
    "expansion_checker": ("proof/check_cycle85_cp_expansion.py", "0ace15fa34504fac18ace1a198f3a318d55ae3c83e5804af313da1f9b749dbd6"),
    "factor_attempt": ("proof/check_cycle85_cp_symbolic.py", "facb1db9a77cc4dd4ae241968a671aa5ba02fd244a6c87a5b2106c70995a8f60"),
    "boundary": ("proof/cycle85_c5_kernel_boundary.md", "6650b808266a6bf826f706323994ec15c8727c420a18f519f8c699bc8f573099"),
    "test": ("tests/test_cycle85_c5_kernel.py", "39b2b45563f352aa8072b9e1152a2a27533d55a8bdb902a3e44e3635934e7c8c"),
    "prior_c68": ("artifacts/cycle-68-b068-s3-fixed-comparison-v1.json", "2a6b725bbe1ab23aa0c44d244acb87cc297a5f210d44798a0ac169c940c33498"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def run(path: str) -> dict:
    return json.loads(subprocess.check_output([sys.executable, str(ROOT / path)], text=True))


def audit() -> dict:
    kernel = run(HASHES["kernel_checker"][0])
    direct = run(HASHES["direct_checker"][0])
    expansion = run(HASHES["expansion_checker"][0])
    require(kernel == direct, "direct and kernel packets disagree")
    require(kernel["status"] == expansion["status"] == "PASS", "checker failure")
    require(kernel["packet_rows"] == 729 and kernel["negative_rows"] == 0 and kernel["zero_rows"] == 81, "packet drift")
    require(kernel["minimum_positive_defect"] == "7381/14281868906496", "positive margin drift")
    require(expansion["expanded_terms"] == 8771 and expansion["total_degree"] == 35 and expansion["uv_total_degree"] == 15, "polynomial fingerprint drift")
    require(expansion["expanded_sha256"] == "5cd3cc7d244ae83ce8c55fa335ee4806038570b76d71da016496ed4c52fd2397", "expanded polynomial hash drift")
    return {"kernel_packet": kernel, "direct_packet": direct, "cp_expansion": expansion}


def payload() -> dict:
    return {
        "artifact_id": "cycle-85-b085-sidorenko-c5-kernel-boundary-v1",
        "budget_ordinal": "B085",
        "cycle": 85,
        "record_type": "METHOD_BOUNDARY",
        "recorded_at_utc": "2026-08-06T00:44:14Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The declared 729 two-atom rational bigraphon controls satisfy C5-K by matching direct and triple-kernel routes; the two-atom CP defect expands exactly to 8,771 terms. No factorization/SOS or negative specialization was produced under the frozen symbolic cap.",
        "claim_boundary": "This seals only the finite C5-kernel method attempt. It neither proves nor refutes C5-K outside the packet, nor the Sidorenko inequality for K_{5,5} minus C_{10}.",
        "cycle_decision": {
            "companion_identity": "/root/oracle_c85_portfolio (Oracle)",
            "companion_advice": "Do not add a grid; pursue one exact two-atom CP factorization/SOS gate, then pivot if it yields neither a certificate nor a rational negative specialization.",
            "decision": "Seal the bounded method boundary and return to portfolio discovery because the authorized symbolic gate produced no checked identity or falsifier.",
            "falsifier": "A negative exact packet row, a rational negative CP specialization, or disagreement between the direct and kernel density routes.",
        },
        "audit": audit(),
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, digest) for key, (path, digest) in HASHES.items()}),
        "runtime": check_runtime("c85"),
        "sealer": {"path": "proof/build_cycle_85_sidorenko_c5_kernel_boundary.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "audit": "python3 proof/check_cycle85_c5_kernel.py && python3 proof/check_cycle85_direct_bigraphon.py && python3 proof/check_cycle85_cp_expansion.py",
            "test": "python3 -c 'from tests.test_cycle85_c5_kernel import test_c85_packet_routes_and_cp_expansion; test_c85_packet_routes_and_cp_expansion()'",
            "check": "python3 proof/build_cycle_85_sidorenko_c5_kernel_boundary.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
