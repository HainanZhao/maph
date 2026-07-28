import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


def run_python(script: str) -> dict:
    process = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(process.stdout)


class DimensionSevenClosureTests(unittest.TestCase):
    def run_gp(self, script: str, stack: str = "256000000") -> str:
        process = subprocess.run(
            [
                "gp",
                "-q",
                "-s",
                stack,
                str(ROOT / "scripts" / script),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return process.stdout

    def test_exact_phase_packet(self) -> None:
        packet = run_python("dimension_seven_phase_audit.py")
        self.assertEqual(packet["rademacher_invariant"], 9)
        self.assertEqual(
            packet["phase_formula"], "zeta_56^(7-32*Q(p))"
        )
        self.assertEqual(len(packet["records"]), 48)
        self.assertLess(packet["reciprocal_residual"], 1e-7)

    def test_complete_phase_and_ray_label_packet(self) -> None:
        packet = run_python("dimension_seven_packet_certificate.py")
        self.assertEqual(packet["characteristic_count"], 48)
        self.assertEqual(packet["lowered_factor_count"], 96)
        self.assertTrue(
            all(len(record["factors"]) == 2 for record in packet["records"])
        )

    def test_exact_ray_fields_and_candidate_unit_fields(self) -> None:
        output = self.run_gp("dimension_seven_ray_fields.gp")
        self.assertIn("BNF_CERTIFIED=1", output)
        self.assertIn("SCALAR_7_ABSOLUTE_IRREDUCIBLE=1", output)
        self.assertIn("SCALAR_14_ABSOLUTE_IRREDUCIBLE=1", output)
        self.assertIn("SCALAR_7_FIELD_MATCH=1", output)
        self.assertIn("SCALAR_14_FIELD_MATCH=1", output)

    def test_shintani_index_conductor_and_safe_power(self) -> None:
        output = self.run_gp(
            "dimension_seven_shintani_audit.gp", "2000000000"
        )
        self.assertIn("SHINTANI_INDEX=2", output)
        self.assertIn("MAXIMAL_ABELIAN_IS_Q_ZETA_56=1", output)
        self.assertIn(
            "NORMAL_CLOSURE_ABELIAN_OVER_Q_SQRT_MINUS_7=1", output
        )
        self.assertIn("SHINTANI_DIVISOR_COUNT=32", output)
        self.assertIn("SHINTANI_W_TWO_DIVISOR_COUNT=4", output)
        self.assertIn("SHINTANI_SAFE_EXPONENT=16128", output)
        self.assertIn("SHINTANI_CONDITION_0_3=0", output)
        self.assertIn("SHINTANI_CONDITION_0_6=0", output)
        self.assertIn(
            "REAL_DISTRIBUTION_DENOMINATORS_CLEARED=1", output
        )

    def test_exact_artin_and_archimedean_labels(self) -> None:
        output = self.run_gp(
            "dimension_seven_artin_labels.gp", "2000000000"
        )
        self.assertIn("PRIME_17_RAY_LOG=[1, 0]", output)
        self.assertIn("PRIME_41_RAY_LOG=[0, 1]", output)
        self.assertIn(
            "H_TO_RAY_14_BASE_PRESERVING_COUNT=12", output
        )
        self.assertIn("PLUS_STRATUM_RECIPROCAL_ROOTS=", output)
        self.assertIn("MINUS_STRATUM_RECIPROCAL_ROOTS=", output)
        self.assertIn("ALL_ARTIN_AND_ROOT_LABELS_CERTIFIED=1", output)

    def test_exact_both_shift_tcc_certificate(self) -> None:
        output = self.run_gp(
            "dimension_seven_exact_tcc.gp", "4000000000"
        )
        self.assertIn("COMPOSITUM_ABSOLUTE_DEGREE=48", output)
        self.assertIn(
            "REAL_CYCLOTOMIC_INTERSECTION_CERTIFIED=1", output
        )
        self.assertIn(
            "POSITIVE_SQRT_TWO_CYCLOTOMIC_COMPATIBILITY=1", output
        )
        self.assertIn("INSTALLED_NONZERO_OVERLAPS=48", output)
        for shift in (1, 0):
            self.assertIn(f"SHIFT_{shift}_TRACE_CERTIFIED=1", output)
            self.assertIn(
                f"SHIFT_{shift}_IDEMPOTENCY_CERTIFIED=1", output
            )
            self.assertIn(f"SHIFT_{shift}_RANK_ONE_CERTIFIED=1", output)

    def test_symbolic_orbit_reduction(self) -> None:
        packet = run_python("dimension_seven_symbolic_reduction.py")
        self.assertEqual(packet["zauner_orbit_count"], 16)
        self.assertEqual(packet["independent_reciprocal_variables"], 8)
        self.assertEqual(packet["rank_two_minors_for_two_shifts"], 882)

    def test_both_formal_shifts(self) -> None:
        packet = run_python("dimension_seven_tcc_shifts.py")
        self.assertEqual(
            [audit["shift"] for audit in packet["audits"]], [1, 0]
        )
        for audit in packet["audits"]:
            self.assertEqual(audit["twist_shift_congruence"], 1)
            self.assertLess(audit["idempotency_residual"], 1e-8)
            self.assertLess(audit["maximum_minor_residual"], 1e-8)


if __name__ == "__main__":
    unittest.main()
