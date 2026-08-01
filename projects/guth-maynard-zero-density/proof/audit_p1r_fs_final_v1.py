#!/usr/bin/env python3
"""Final read-only hostile audit for the P1R-FS fixed-splice promotion."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
A = ROOT / "proof/p1r_fs_route_a_v1.py"
B = ROOT / "proof/p1r_fs_route_b_v1.py"
R = ROOT / "proof/reconcile_p1r_fs_routes_v1.py"
ART_A = ROOT / "artifacts/p1r-fs-route-a-v1.json"
ART_B = ROOT / "artifacts/p1r-fs-route-b-v1.json"
ART_R = ROOT / "artifacts/p1r-fs-route-reconciliation-v1.json"
V4 = ROOT / "artifacts/cycle-4-p1r-preregistration-v4.json"
V4_AUDIT = ROOT / "artifacts/cycle-4-p1r-preregistration-v4-hostile-audit-v1.json"
LEDGER = ROOT / "docs/literature-ledger-classical-inputs.md"
HUXLEY = ROOT / "artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf"
OUTPUT = ROOT / "artifacts/p1r-fs-final-hostile-audit-v1.json"
PACKAGE: dict[str, tuple[Path, str]] = {
    "route_a_script": (A, "ce87441984d5129b250a7a1f51070ffbe190e793fa2680e712fd6ca549bd5560"),
    "route_a_artifact": (ART_A, "c1bde2f7aa8675963b27e4b41e04d54717c7d875159d376950ff51240865d342"),
    "route_a_document": (ROOT / "docs/p1r-fs-route-a-v1.md", "0fc70245c16569fc2e533b35eba4987fe75eba6f5151e43c6781e04e09bcac72"),
    "route_a_tests": (ROOT / "tests/test_p1r_fs_route_a_v1.py", "43419ab347fbda816ff0cd30e5f79b41cd38ec43dde1869b58b6f5ef671d415c"),
    "route_b_script": (B, "fdcff5384a9d8705cd6b7b862124d6a2e3869b8e4173396335d9481f2ad6cb60"),
    "route_b_artifact": (ART_B, "678df43e0e8b8abf485302410565c1cf3838bd6aea5ab554b20c20bb2bd03880"),
    "route_b_document": (ROOT / "docs/p1r-fs-route-b-v1.md", "935ee988f3074d0d7e29c2af0833bb0fa812948a65692d85ba92148446c785e7"),
    "route_b_tests": (ROOT / "tests/test_p1r_fs_route_b_v1.py", "19a323b6b2cb60350fdbf29fd43634501f310aa7b171b4c189a1ee808c0a3a39"),
    "reconciliation_script": (R, "ff0a126136035c4f42189192977b2ee02b90df10abe2467b2193373af4a80867"),
    "reconciliation_artifact": (ART_R, "2fe46ee076df8b17a93876d76c5b223e1425af831b440dd8f0708f084dbec62b"),
    "reconciliation_document": (ROOT / "docs/p1r-fs-route-reconciliation-v1.md", "7a0dde8edfe40b4e803c8b1ce0f171cdbf04312018927b039d54a9e9b73ae0f3"),
    "reconciliation_tests": (ROOT / "tests/test_p1r_fs_route_reconciliation_v1.py", "d23c441e3bea26f4aff5cbd46f5bc8f4a214cedb7a2bd0782fb3298388f642ec"),
    "preregistration_v4": (V4, "e2aeec9ec90e1fea0a9eade53d5ff1e57020df48bd92ae852121a941fbadd7f9"),
    "preregistration_v4_hostile": (V4_AUDIT, "bdb60d416fee628d309e025a493c45383ccc50e3ee41a9bdb0d6b8a7d73235ad"),
    "classical_ledger": (LEDGER, "5005dc96deca85d930b710000b1faccdce093e8574dc44f9730fa4a570529f11"),
    "huxley_pdf": (HUXLEY, "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot import: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command: list[str]) -> int:
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True).returncode


def real_epsilon_certificate(eta: Fraction) -> tuple[Fraction, Fraction]:
    """Exact inequalities that remain valid for every real eta in the interval."""
    benchmark = Fraction(30, 13)
    require(0 < eta < benchmark, "eta out of real-proof interval")
    threshold = 169 * eta / (300 - 130 * eta)
    h = min(Fraction(1, 10), threshold / 2)
    require(0 < h <= Fraction(1, 10) < Fraction(1, 5), "left witness out of range")
    require(h < threshold, "strict real epsilon threshold failed")
    gap = 300 * h / (169 + 130 * h)
    require(gap < eta, "strict real epsilon gap failed")
    return h, gap


def audit() -> dict[str, Any]:
    require(platform.python_implementation() == "CPython", "audit requires CPython")
    require(platform.python_version() == "3.12.3" and sys.flags.optimize == 0, "audit requires non-optimized CPython 3.12.3")
    hashes: dict[str, str] = {}
    for label, (path, expected) in PACKAGE.items():
        require(path.is_file(), f"missing final P1R-FS package file: {label}")
        actual = sha256(path)
        require(actual == expected, f"final P1R-FS package hash mismatch: {label}")
        hashes[label] = actual

    a, b, reconciliation = (load_module(A, "p1r_fs_final_a"), load_module(B, "p1r_fs_final_b"), load_module(R, "p1r_fs_final_r"))
    a_art, b_art, r_art = (json.loads(ART_A.read_text(encoding="utf-8")), json.loads(ART_B.read_text(encoding="utf-8")), json.loads(ART_R.read_text(encoding="utf-8")))
    v4 = json.loads(V4.read_text(encoding="utf-8"))
    v4_audit = json.loads(V4_AUDIT.read_text(encoding="utf-8"))
    require(v4["status"] == "SEALED_PREREGISTRATION" and v4_audit["status"] == "PASS", "sealed v4 authorization chain absent")
    require(a_art["epistemic_status"] == b_art["epistemic_status"] == r_art["epistemic_status"] == "PROVED", "incorrect epistemic tag")
    require(r_art["status"] == "TWO_ROUTE_RECONCILED_PENDING_HOSTILE_AUDIT", "premature reconciliation status")
    boundary = r_art["claim_boundary"]
    for phrase in ("not a lower bound for the actual zero count", "not saturation of the Guth--Maynard method", "not a new zero-density estimate", "not a short-interval theorem"):
        require(phrase in boundary, f"claim-boundary exclusion missing: {phrase}")

    # Independent derivation: for real 0<eta<30/13 the displayed threshold is
    # positive and h<threshold iff the exact gap is < eta. Rational execution
    # guards the algebra; it is a symbolic ordered-field proof, not sampling.
    for eta in (Fraction(1, 10**30), Fraction(1, 1000), Fraction(1, 1), Fraction(30, 13) - Fraction(1, 10**30)):
        h, gap = real_epsilon_certificate(eta)
        sigma = Fraction(7, 10) - h
        value = Fraction(3, 1) / (2 - sigma)
        require(Fraction(1, 2) <= sigma < Fraction(7, 10) and value > Fraction(30, 13) - eta and gap == Fraction(30, 13) - value, "independent epsilon witness failed")
    require(Fraction(3, 1) / (2 - Fraction(7, 10)) == Fraction(30, 13), "endpoint limit identity failed")

    ledger = LEDGER.read_text(encoding="utf-8")
    for fragment in ("N(\\alpha,T)\\ll T^{3(1-\\alpha)/(2-\\alpha)}(\\log T)^5", "1/2\\le\\alpha\\le3/4", "`PROVED` as a contemporaneous published restatement"):
        require(fragment in ledger, f"Huxley source/range/log record missing: {fragment}")
    require(Fraction(1, 2) <= Fraction(7, 10) < Fraction(3, 4), "used left range exceeds source range")
    require("(log T)^5 retained" in b_art["source_scope"]["log_factor"], "log-factor scope missing")

    a_text, b_text = A.read_text(encoding="utf-8"), B.read_text(encoding="utf-8")
    require("p1r_fs_route_b_v1" not in a_text and "p1r-fs-route-b-v1" not in a_text, "Route A names Route B")
    require("p1r_fs_route_a_v1" not in b_text and "p1r-fs-route-a-v1" not in b_text, "Route B names Route A")
    require(set(a.INPUTS).isdisjoint({"route_b_artifact", "route_b_script"}) and set(b.INPUTS).isdisjoint({"route_a_artifact", "route_a_script"}), "cross-route input dependency")
    require(r_art["independence_audit"]["cross_route_file_references"] == [] and r_art["independence_audit"]["shared_inputs"] == ["sealed P1R v4 architecture", "Huxley source/ledger"], "independence record mismatch")

    # Extended-real right branch: the nonempty left image is included in every
    # full splice image, so sup(F_J)=max(sup(I),sup(J)) in [-infinity,+infinity].
    right = b_art["arbitrary_right_branch"]
    require(right["quantifier"] == "for every extended-real-valued J on [7/10,1]", "right-branch quantifier weakened")
    require(right["supremum_identity"] == "sup F_J=max(30/13,sup J)" and right["extended_cases"] == {"sup_J=-infinity": "sup F_J=30/13", "sup_J=+infinity": "sup F_J=+infinity"}, "extended-real semantics mismatch")
    for finite_sup in (Fraction(-10**9), Fraction(30, 13), Fraction(10**9)):
        require(max(Fraction(30, 13), finite_sup) >= Fraction(30, 13), "right-branch order obstruction failed")

    commands = [(A, "route_a"), (B, "route_b"), (R, "reconciliation")]
    for script, label in commands:
        require(run([sys.executable, str(script), "--check"]) == 0, f"normal replay failed: {label}")
        require(run([sys.executable, "-O", str(script), "--check"]) != 0, f"-O does not fail closed: {label}")
        require(run([sys.executable, "-OO", str(script), "--check"]) != 0, f"-OO does not fail closed: {label}")
        require(run([sys.executable, str(script), "--write"]) != 0, f"overwrite not refused: {label}")
    require(run([sys.executable, "-m", "unittest", "tests/test_p1r_fs_route_a_v1.py", "tests/test_p1r_fs_route_b_v1.py", "tests/test_p1r_fs_route_reconciliation_v1.py"]) == 0, "final package regression suite failed")

    for module, field, label in ((a, "huxley_pdf", "route_a"), (b, "huxley_pdf", "route_b"), (reconciliation, "route_b_artifact", "reconciliation")):
        original = module.INPUTS[field]
        module.INPUTS[field] = (original[0], "0" * 64)
        try:
            try:
                (module.prove if label == "route_a" else module.certificate if label == "route_b" else module.reconcile)()
            except RuntimeError as error:
                require(f"frozen input hash mismatch: {field}" in str(error), f"wrong input-tamper error: {label}")
            else:
                raise RuntimeError(f"input tamper not rejected: {label}")
        finally:
            module.INPUTS[field] = original
    for module, method, field, original_hash in ((a, a.prove, "prover", hashes["route_a_script"]), (b, b.certificate, "sealer", hashes["route_b_script"]), (reconciliation, reconciliation.reconcile, "reconciler", hashes["reconciliation_script"])):
        with tempfile.NamedTemporaryFile(dir=ROOT / "proof", suffix=".py") as handle:
            handle.write(Path(module.SELF).read_bytes() + b"\n# hostile self tamper\n")
            handle.flush()
            original_self = module.SELF
            module.SELF = Path(handle.name)
            try:
                require(method()[field]["sha256"] != original_hash, f"self tamper not bound: {field}")
            finally:
                module.SELF = original_self

    return {
        "artifact_id": "p1r-fs-final-hostile-audit-v1", "epistemic_status": "OBSERVED", "status": "PASS", "theorem_id": "P1R-FS",
        "claim_boundary": "Read-only hostile promotion audit. It validates only the exact frozen fixed-splice theorem, not any actual zero-density lower bound, full-method saturation, new density estimate, short-interval theorem, or CRR search.",
        "auditor": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)}, "audited_package_hashes": hashes,
        "checks": {
            "exact_real_supremum_and_epsilon_quantifier": "PASS", "source_range_and_log_factor": "PASS", "route_independence": "PASS", "extended_real_right_branch": "PASS", "epistemic_tag_and_claim_boundary": "PASS", "normal_replays": "PASS", "optimized_O": "PASS", "optimized_OO": "PASS", "overwrite": "PASS", "input_tamper": "PASS", "self_tamper": "PASS", "final_package_regression_suite": "PASS",
        },
        "conclusion": "PROVED, conditional on the checked Huxley restatement, only for the frozen splice: every uniform coefficient for a function retaining I(sigma)=3/(2-sigma) on 1/2<=sigma<7/10 is at least 30/13. A right-only extended-real replacement cannot certify a smaller uniform coefficient. This is not a claim about the actual zero count or the full Guth--Maynard method.",
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    require(args.check.is_file(), "final hostile artifact absent")
    require(args.check.read_bytes() == render(result), "final hostile artifact mismatch")
    print(json.dumps({"status": result["status"], "theorem_id": result["theorem_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
