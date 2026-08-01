from __future__ import annotations

import ast
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/p1r_fs_route_b_v1.py"
ARTIFACT = PROJECT / "artifacts/p1r-fs-route-b-v1.json"
DOCUMENT = PROJECT / "docs/p1r-fs-route-b-v1.md"


def load_module():
    spec = importlib.util.spec_from_file_location("p1r_fs_route_b_v1_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load P1R-FS Route B module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class P1RFSRouteBV1Tests(unittest.TestCase):
    def test_replay_identity_runtime_and_overwrite_refusal(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertEqual(data["runtime"], {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0})
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        overwrite = subprocess.run(
            [sys.executable, str(SCRIPT), "--write"],
            cwd=PROJECT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(overwrite.returncode, 0)
        self.assertIn("refusing to overwrite", overwrite.stderr)
        for flag in ("-O", "-OO"):
            optimized = subprocess.run(
                [sys.executable, flag, str(SCRIPT), "--check"],
                cwd=PROJECT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(optimized.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", optimized.stderr)

    def test_source_pins_v4_hostile_pass_and_tamper_failure(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        expected = {
            "p1r_preregistration_v4": "e2aeec9ec90e1fea0a9eade53d5ff1e57020df48bd92ae852121a941fbadd7f9",
            "p1r_preregistration_v4_hostile_audit": "bdb60d416fee628d309e025a493c45383ccc50e3ee41a9bdb0d6b8a7d73235ad",
            "huxley_pdf": "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797",
            "classical_ledger": "5005dc96deca85d930b710000b1faccdce093e8574dc44f9730fa4a570529f11",
            "route_b_document": "935ee988f3074d0d7e29c2af0833bb0fa812948a65692d85ba92148446c785e7",
        }
        self.assertEqual({key: row["sha256"] for key, row in data["frozen_inputs"].items()}, expected)
        hostile = json.loads((PROJECT / data["frozen_inputs"]["p1r_preregistration_v4_hostile_audit"]["path"]).read_text(encoding="utf-8"))
        self.assertEqual(hostile["status"], "PASS")
        module = load_module()
        original = module.INPUTS["huxley_pdf"]
        module.INPUTS["huxley_pdf"] = (original[0], "0" * 64)
        try:
            with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: huxley_pdf"):
                module.verify_frozen_inputs()
        finally:
            module.INPUTS["huxley_pdf"] = original

    def test_cleared_identities_and_universal_eta_constructor(self) -> None:
        module = load_module()
        benchmark = Fraction(30, 13)
        for h in (Fraction(1, 5), Fraction(1, 10), Fraction(1, 1000), Fraction(1, 10**9)):
            coefficient = module.ingham_coefficient_from_h(h)
            self.assertEqual(coefficient, Fraction(30, 1) / (13 + 10 * h))
            self.assertEqual(module.endpoint_gap(h), 300 * h / (169 + 130 * h))
            self.assertLess(coefficient, benchmark)
        for eta in (
            Fraction(1, 10**12),
            Fraction(1, 1000),
            Fraction(1, 13),
            Fraction(1, 1),
            benchmark - Fraction(1, 10**12),
        ):
            row = module.eta_witness(eta)
            h = Fraction(row["h"])
            gap = Fraction(row["gap"])
            coefficient = Fraction(row["I_sigma"])
            self.assertGreater(h, 0)
            self.assertLessEqual(h, Fraction(1, 5))
            self.assertLess(gap, eta)
            self.assertGreater(coefficient, benchmark - eta)
        for inadmissible in (Fraction(0), benchmark, benchmark + 1):
            with self.assertRaisesRegex(RuntimeError, "eta must satisfy"):
                module.eta_witness(inadmissible)

    def test_arbitrary_right_branch_order_obstruction(self) -> None:
        module = load_module()
        benchmark = Fraction(30, 13)
        for right in (Fraction(-10**20), Fraction(0), benchmark, benchmark + Fraction(1, 10**20), Fraction(10**20)):
            row = module.finite_right_supremum(right)
            self.assertEqual(Fraction(row["combined_supremum"]), max(benchmark, right))
            self.assertGreaterEqual(Fraction(row["combined_supremum"]), benchmark)
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        branch = data["arbitrary_right_branch"]
        self.assertEqual(branch["quantifier"], "for every extended-real-valued J on [7/10,1]")
        self.assertEqual(branch["supremum_identity"], "sup F_J=max(30/13,sup J)")
        self.assertIn("subset", branch["set_inclusion"])

    def test_claim_scope_independence_and_code_hygiene(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        boundary = data["claim_boundary"]
        for excluded in (
            "not a lower bound for the actual zero count",
            "not saturation of the Guth--Maynard method",
            "not a zero-density theorem",
            "not a short-interval theorem",
        ):
            self.assertIn(excluded, boundary)
        self.assertEqual(data["gate_effect"], "ROUTE_B_ONLY_PENDING_ROUTE_A_RECONCILIATION_AND_HOSTILE_AUDIT")
        self.assertEqual(data["independence"]["route_a_inputs_read"], [])
        self.assertEqual(data["independence"]["future_route_a_imports"], [])
        module = load_module()
        self.assertEqual(
            set(module.INPUTS),
            {
                "p1r_preregistration_v4",
                "p1r_preregistration_v4_hostile_audit",
                "huxley_pdf",
                "classical_ledger",
                "route_b_document",
            },
        )
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
        self.assertFalse(any(isinstance(node, ast.Constant) and isinstance(node.value, float) for node in ast.walk(tree)))
        imported = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported.update(
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        self.assertTrue(imported.isdisjoint({"random", "socket", "urllib", "http", "requests"}))
        document = DOCUMENT.read_text(encoding="utf-8")
        normalized_document = " ".join(document.split())
        self.assertIn("not a lower bound for the actual zero count", normalized_document)
        self.assertIn("not saturation of the Guth--Maynard method", normalized_document)

    def test_tampered_self_fails_against_sealed_artifact(self) -> None:
        with tempfile.NamedTemporaryFile(dir=PROJECT / "proof", suffix=".py") as handle:
            handle.write(SCRIPT.read_bytes() + b"\n# hostile self mutation\n")
            handle.flush()
            result = subprocess.run(
                [sys.executable, handle.name, "--check"],
                cwd=PROJECT,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("artifact mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()
