from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import unittest

from src.exact_error import exact_squared_error
from src.modular_error import certified_crt_cbc
from src.ntt_prime import generate_ntt_prime_schedule
from src.scaled_integer import (
    balanced_crt_bits,
    candidate_difference_bound,
    error_numerator_bound,
)


PROJECT = Path(__file__).resolve().parents[1]


class CycleArtifactTests(unittest.TestCase):
    def load(self, name: str):
        return json.loads((PROJECT / "certificates" / name).read_text())

    def test_cycle001_scope_and_snapshots_are_frozen(self):
        audit = self.load("cycle-001-source-audit.json")
        self.assertEqual(audit["tag"], "VERIFIED_SOURCE_AUDIT")
        self.assertIn("not a universal", audit["scope_limit"])
        self.assertEqual(len(audit["repositories"]), 2)
        self.assertTrue(
            all(not row["certified_merit_path_found"]
                for row in audit["repositories"])
        )

    def test_cycle002_bounds_recompute(self):
        audit = self.load("cycle-002-scaled-bounds.json")
        cases = [
            (2**20, [Fraction(1)] * 100),
            (1024, [Fraction(1, j * j) for j in range(1, 17)]),
        ]
        for row, (modulus, weights) in zip(audit["cases"], cases):
            error_bound = error_numerator_bound(modulus, weights)
            branch_bound = candidate_difference_bound(
                modulus, weights[:-1], weights[-1]
            )
            self.assertEqual(int(row["error_numerator_bound"]), error_bound)
            self.assertEqual(
                row["error_crt_product_required_bits"],
                balanced_crt_bits(error_bound),
            )
            self.assertEqual(
                int(row["last_stage_difference_bound"]), branch_bound
            )

    def test_cycle003_schedule_replays(self):
        audit = self.load("cycle-003-prime-schedule.json")
        self.assertEqual(audit["primes"], generate_ntt_prime_schedule(16))

    def test_cycle004_crt_cbc_replays(self):
        audit = self.load("cycle-004-crt-cbc-n31-d5.json")
        expected = certified_crt_cbc(
            31,
            [Fraction(1, j * j) for j in range(1, 6)],
            generate_ntt_prime_schedule(4),
        )
        self.assertEqual(audit, expected)

    def test_cycle005_exact_rows_replay(self):
        audit = self.load("cycle-005-benchmark.json")
        generator = [1, 275, 179, 319, 299, 451, 417, 167,
                     289, 109, 395, 81, 215, 115, 143, 361]
        for row in audit["rows"]:
            dimension = row["dimension"]
            value = exact_squared_error(
                1024,
                generator[:dimension],
                [Fraction(1, j * j) for j in range(1, dimension + 1)],
            )
            self.assertEqual(
                row["exact_result"],
                {
                    "numerator": str(value.numerator),
                    "denominator": str(value.denominator),
                    "tag": "VERIFIED",
                },
            )
            self.assertTrue(row["all_three_exactly_equal"])


if __name__ == "__main__":
    unittest.main()
