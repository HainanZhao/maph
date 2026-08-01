from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/build_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.json"
SNAPSHOT = PROJECT / "artifacts/cycle-4-p6-cgl-v2-authorization-snapshot-v1.json"
DOCUMENT = PROJECT / "docs/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.md"
TEX_NAME = "Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"


def load_artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def run_mutated(old: bytes, new: bytes, mode: str = "--check") -> subprocess.CompletedProcess[str]:
    source = SCRIPT.read_bytes()
    if old not in source:
        raise RuntimeError(f"mutation anchor absent: {old!r}")
    mutated = source.replace(old, new, 1)
    with tempfile.NamedTemporaryFile(dir=PROJECT / "proof", suffix=".py") as handle:
        handle.write(mutated)
        handle.flush()
        return subprocess.run(
            [sys.executable, handle.name, mode],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            timeout=60,
        )


class Cycle4P6CGLV2PreregistrationV1Tests(unittest.TestCase):
    def test_exact_46_row_registry_and_explicit_count_correction(self) -> None:
        data = load_artifact()
        expected_ids = (
            [f"S{index:02d}" for index in range(1, 7)]
            + [f"L{index:02d}" for index in range(1, 13)]
            + [f"M{index:02d}" for index in range(1, 9)]
            + [f"Z{index:02d}" for index in range(1, 11)]
            + [f"F{index:02d}" for index in range(1, 11)]
        )
        rows = data["row_registry"]
        self.assertEqual(len(rows), 46)
        self.assertEqual([row["id"] for row in rows], expected_ids)
        self.assertEqual(len({row["id"] for row in rows}), 46)
        self.assertTrue(all(row["initial_status"] == "UNEXECUTED" for row in rows))
        self.assertNotIn("L13", expected_ids)
        by_id = {row["id"]: row for row in rows}
        self.assertEqual(by_id["L12"]["mandatory_subchecks"], ["odd_prime", "two_power"])
        correction = data["registry_count_correction"]
        self.assertEqual(correction["draft_arithmetic"], "6+13+8+10+10=47, not 46")
        self.assertEqual(correction["canonical_count"], 46)
        self.assertEqual(correction["retired_draft_aliases"], {"L13": "L12.two_power"})
        self.assertTrue(correction["no_obligation_dropped"])
        snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        self.assertEqual(snapshot["registry_count_correction"]["canonical_count"], 46)
        self.assertIn("6+13+8+10+10=47", DOCUMENT.read_text(encoding="utf-8"))
        table_rows = [line for line in DOCUMENT.read_text(encoding="utf-8").splitlines() if len(line) > 5 and line[0] == "|" and line[2:5].isalnum()]
        self.assertEqual(len(table_rows), 46)

    def test_source_hashes_tar_member_and_self_identity(self) -> None:
        data = load_artifact()
        expected = {
            "authorization_snapshot": "c8183266cbfab602ba3c05c120a80293b7741284d6c46a08a88c03c3b46f25b3",
            "preregistration_document": "2208164bdb207c0322fe376c21553f7dc4f307625328b8542fa2abe358dafd47",
            "cgl_v2_tex": "0b9ebb6b604944b7c59a9ec37a75c48f6a08f88611f911ff5f02dc013b848e2f",
            "cgl_v2_tar": "b982cd5afa5b5e8a9abff2c6306519ba558d321b19aadd3fdbe59b3750f8e9ae",
            "cgl_v2_pdf": "adfe65cf0952bbb4eddfdaec7a8d3341130e427827f9159d9da039fc16336058",
            "bounded_literature_audit_v1": "49da2e838ce60699ba870e0c532aab5ec8ba564c560811d9683ac92f0afbe6be",
            "bounded_literature_correction_v2": "f56529c5919971385cc583b51255636022a5b33fb0cfd4857a587f1d3e099076",
        }
        self.assertEqual({key: row["sha256"] for key, row in data["frozen_inputs"].items()}, expected)
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        tex_path = PROJECT / data["frozen_inputs"]["cgl_v2_tex"]["path"]
        tar_path = PROJECT / data["frozen_inputs"]["cgl_v2_tar"]["path"]
        with tarfile.open(tar_path, mode="r:*") as archive:
            member = archive.getmember(TEX_NAME)
            extracted = archive.extractfile(member)
            self.assertIsNotNone(extracted)
            if extracted is None:
                raise RuntimeError("tar member unexpectedly absent")
            self.assertEqual(extracted.read(), tex_path.read_bytes())
        self.assertTrue(data["source_integrity"]["tar_member_equals_canonical_tex"])
        self.assertEqual(data["source_integrity"]["logical_line_count"], 2468)
        self.assertEqual(data["source_integrity"]["newline_count"], 2467)

    def test_expected_open_blockers_and_nonpromotion_boundary(self) -> None:
        data = load_artifact()
        self.assertEqual(data["expected_reconstruction_outcome"], "OPEN_ANALYTIC_INPUT")
        self.assertEqual(data["gate_rule"]["expected"], "OPEN_ANALYTIC_INPUT")
        blockers = [row["id"] for row in data["expected_blockers"]]
        self.assertEqual(
            blockers,
            [
                "S06_EXTERNAL_INPUTS",
                "Z03_TAIL_X_RANGE",
                "Z05_PRIMITIVE_EULER_FACTORS",
                "Z06_CONDUCTOR_SUM_Q1",
                "F08_T_SMOOTH_UNDEFINED",
            ],
        )
        primitive = [row for row in data["expected_blockers"] if row.get("group") == "PRIMITIVE_TO_ALL"]
        self.assertEqual([row["row"] for row in primitive], ["Z05", "Z06"])
        boundary = data["claim_boundary"]
        for fragment in (
            "no reconstruction is executed",
            "no CGL theorem is proved or repaired",
            "no 7/3 result is promoted",
            "no novelty claim is made",
            "no P7 family is selected",
            "no zero-density or short-interval theorem follows",
        ):
            self.assertIn(fragment, boundary)
        self.assertIn("preprint and prior work", data["source_disposition"])

    def test_conventions_crossings_routes_and_forbidden_repairs(self) -> None:
        data = load_artifact()
        self.assertEqual(
            data["route_b_coordinates"],
            {
                "alpha": "log(q)/log(qT)",
                "tau": "1-alpha",
                "lambda": "log(q1)/log(qT)",
                "beta": "lambda+tau=log(q1*T)/log(qT)",
                "q1_at_least_sqrt_q": "beta>=1/2",
            },
        )
        formulas = data["frozen_crossing_formulas"]
        self.assertEqual(formulas["C1"], "3*(1+lambda/3)/(1+sigma)")
        self.assertEqual(formulas["C2"], "3*(1-beta/2)/sigma")
        self.assertEqual(formulas["C3"], "((21-20*sigma)/6-beta/2)/(1-sigma)")
        self.assertEqual(formulas["C4"], "15/(3+5*sigma)")
        self.assertEqual(formulas["crossing_C3_polynomial"], "20*sigma^2-(43-3*beta)*sigma+24-6*beta=0")
        self.assertEqual(formulas["B"], "(37+3*beta-sqrt(9*beta^2+222*beta-71))/12")
        self.assertEqual(formulas["q1_equals_q_reductions"], ["q^(7/3)*T^2", "9/4", "(10-sqrt(10))/3", "30/13"])
        self.assertEqual(len(formulas["uniform_7_over_3_checks"]), 4)
        routes = data["route_design"]
        self.assertIn("literal source-order", routes["route_A"])
        self.assertIn("independent alpha/tau/lambda/beta", routes["route_B"])
        self.assertIn("may not import Route A", routes["independence"])
        self.assertEqual(
            data["conventions"]["forbidden_repairs"],
            [
                "q<=T^C",
                "replace log^2 T by log^2(qT)",
                "invent T-smooth definition",
                "supply primitive/all proof without source or proved derivation",
            ],
        )

    def test_historical_replay_runtime_resources_and_code_hygiene(self) -> None:
        data = load_artifact()
        self.assertEqual(
            data["runtime"],
            {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0, "platform": "linux"},
        )
        historical = data["historical_replay"]
        self.assertFalse(historical["mutable_research_plan_read"])
        self.assertFalse(historical["mutable_research_plan_hash_pinned"])
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("PLAN.md", source)
        self.assertNotIn("PLAN", " ".join(row["path"] for row in data["frozen_inputs"].values()))
        tree = ast.parse(source)
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
        self.assertFalse(any(isinstance(node, ast.Constant) and isinstance(node.value, float) for node in ast.walk(tree)))
        direct_imports = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        direct_imports.update(
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        self.assertTrue(direct_imports.isdisjoint({"random", "secrets", "socket", "urllib", "http", "requests"}))
        policy = data["resource_policy"]
        self.assertEqual(policy["wall_cap_ns"], 60_000_000_000)
        self.assertEqual(policy["rss_cap_kib"], 262_144)
        self.assertEqual(policy["floating_point"], "PROHIBITED")
        self.assertEqual(policy["rng"], "PROHIBITED")
        self.assertEqual(policy["network"], "PROHIBITED")

    def test_cli_optimized_overwrite_self_and_source_tamper_fail_closed(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True, timeout=60)
        before = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()
        overwrite = subprocess.run(
            [sys.executable, str(SCRIPT), "--write"],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertNotEqual(overwrite.returncode, 0)
        self.assertIn("refusing to overwrite", overwrite.stderr)
        for flag in ("-O", "-OO"):
            optimized = subprocess.run(
                [sys.executable, flag, str(SCRIPT), "--check"],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertNotEqual(optimized.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", optimized.stderr)
        self_tamper = run_mutated(b"\n", b"\n# hostile self mutation\n", "--check")
        self.assertNotEqual(self_tamper.returncode, 0)
        self.assertIn("artifact mismatch", self_tamper.stderr)
        source_tamper = run_mutated(
            b"0b9ebb6b604944b7c59a9ec37a75c48f6a08f88611f911ff5f02dc013b848e2f",
            b"0000000000000000000000000000000000000000000000000000000000000000",
        )
        self.assertNotEqual(source_tamper.returncode, 0)
        self.assertIn("frozen input hash mismatch: cgl_v2_tex", source_tamper.stderr)
        snapshot_tamper = run_mutated(
            b"c8183266cbfab602ba3c05c120a80293b7741284d6c46a08a88c03c3b46f25b3",
            b"0000000000000000000000000000000000000000000000000000000000000000",
        )
        self.assertNotEqual(snapshot_tamper.returncode, 0)
        self.assertIn("frozen input hash mismatch: authorization_snapshot", snapshot_tamper.stderr)
        self.assertEqual(hashlib.sha256(ARTIFACT.read_bytes()).hexdigest(), before)

    def test_resource_cap_failures_precede_write(self) -> None:
        before = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()
        wall = run_mutated(b"WALL_CAP_NS = 60_000_000_000", b"WALL_CAP_NS = 1", "--write")
        self.assertNotEqual(wall.returncode, 0)
        self.assertIn("60-second wall cap", wall.stderr)
        rss = run_mutated(b"RSS_CAP_KIB = 262_144", b"RSS_CAP_KIB = 1", "--write")
        self.assertNotEqual(rss.returncode, 0)
        self.assertIn("256-MiB RSS cap", rss.stderr)
        self.assertEqual(hashlib.sha256(ARTIFACT.read_bytes()).hexdigest(), before)


if __name__ == "__main__":
    unittest.main()
