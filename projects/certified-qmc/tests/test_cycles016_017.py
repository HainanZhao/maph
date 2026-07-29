from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

from src.certificate import canonical_sha256
from src.crt import choose_moduli
from src.scaled_integer import error_numerator_bound

from fractions import Fraction


PROJECT = Path(__file__).resolve().parents[1]
SPEC = PROJECT / "data" / "cycles-016-017-fidelity-spec.json"
PREREG = (
    PROJECT / "data" / "cycles-016-017-preregistration.json"
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


class Cycles016017Tests(unittest.TestCase):
    def test_preregistration_self_hash_and_spec_pin(self):
        prereg = json.loads(PREREG.read_text())
        supplied = prereg.pop("preregistration_sha256")
        self.assertEqual(canonical_sha256(prereg), supplied)
        self.assertFalse(prereg["production_started"])
        self.assertEqual(
            prereg["production_spec"]["sha256"],
            digest(SPEC),
        )
        self.assertEqual(
            prereg["run_gate"]["maximum_aggregate_ns_per_update"],
            "3.10342892905734250",
        )
        self.assertEqual(
            prereg["post_run_audit"]["sample_count"],
            100,
        )

    def test_fidelity_grid_and_minimal_prime_counts(self):
        spec = json.loads(SPEC.read_text())
        self.assertEqual(len(spec["tables"]), 22)
        self.assertEqual(spec["parallel_workers"], 4)
        self.assertIn("not redistributed", spec["boundary"])
        schedule = json.loads(
            (PROJECT / spec["prime_schedule"]).read_text()
        )
        primes = [
            int(row["p"]) for row in schedule["primes"][:3738]
        ]
        by_modulus = {}
        for table in spec["tables"]:
            self.assertEqual(table["dimension"], 3600)
            self.assertEqual(table["weight_power"], 2)
            by_modulus.setdefault(
                table["N"], table["work_prime_count"]
            )
            self.assertEqual(
                by_modulus[table["N"]],
                table["work_prime_count"],
            )
        self.assertEqual(
            sorted(by_modulus),
            [2**exponent for exponent in range(10, 21)],
        )

        # Replay the smallest and largest cell budgets independently.
        weights = [
            Fraction(1, index * index)
            for index in range(1, 3601)
        ]
        for modulus in (2**10, 2**20):
            bound = error_numerator_bound(modulus, weights)
            self.assertEqual(
                len(choose_moduli(primes, bound)),
                by_modulus[modulus],
            )

    def test_frozen_source_hashes(self):
        if not (PROJECT / ".run-inputs").is_dir():
            self.skipTest("keyed external vectors are intentionally absent")
        prereg = json.loads(PREREG.read_text())
        for filename, expected in prereg[
            "pre_run_freeze"
        ]["input_table_hashes"].items():
            self.assertEqual(
                digest(PROJECT / ".run-inputs" / filename),
                expected,
            )


if __name__ == "__main__":
    unittest.main()
