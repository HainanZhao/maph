from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

from src.certificate import canonical_sha256
from src.crt import choose_moduli
from src.scaled_integer import error_numerator_bound
from scripts.audit_fidelity_production import expected_update_count

from fractions import Fraction


PROJECT = Path(__file__).resolve().parents[1]
SPEC = PROJECT / "data" / "cycles-016-017-fidelity-spec.json"
PREREG = (
    PROJECT / "data" / "cycles-016-017-preregistration.json"
)
V2_SPEC = (
    PROJECT / "data" / "cycles-016-017-fidelity-spec-v2.json"
)
V2_PREREG = (
    PROJECT / "data" / "cycles-016-017-preregistration-v2.json"
)
PAUSE = (
    PROJECT
    / "certificates"
    / "cycles-016-017-throughput-pause-v1.json"
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


class Cycles016017Tests(unittest.TestCase):
    def test_frozen_grid_exact_update_count(self):
        spec = json.loads(V2_SPEC.read_text())
        self.assertEqual(
            expected_update_count(spec), 53_797_264_588_800
        )

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

    def test_v1_pause_is_preserved_and_v2_is_prospective(self):
        pause = json.loads(PAUSE.read_text())
        supplied = pause.pop("certificate_sha256")
        self.assertEqual(canonical_sha256(pause), supplied)
        self.assertTrue(pause["frozen_trigger"]["triggered"])
        self.assertEqual(
            pause["frozen_trigger"]["driver_exit_code"], 76
        )
        self.assertTrue(
            pause["preservation"]["resume_under_v1_forbidden"]
        )

        v2 = json.loads(V2_PREREG.read_text())
        v2_hash = v2.pop("preregistration_sha256")
        self.assertEqual(canonical_sha256(v2), v2_hash)
        self.assertFalse(v2["production_started"])
        self.assertGreater(
            v2["frozen_at_utc"], pause["recorded_at_utc"]
        )
        self.assertEqual(
            v2["predecessor"]["preregistration"]["sha256"],
            digest(PREREG),
        )
        self.assertEqual(
            v2["predecessor"]["pause_transcript"]["sha256"],
            digest(PAUSE),
        )
        self.assertEqual(
            v2["production_spec"]["sha256"],
            digest(V2_SPEC),
        )
        self.assertEqual(
            v2["run_gate"]["maximum_aggregate_ns_per_update"],
            "4.34480050068027950",
        )
        self.assertEqual(v2["run_gate"]["maximum_node_days"], 7)

    def test_v2_changes_only_versioned_monitor_metadata(self):
        v1 = json.loads(SPEC.read_text())
        v2 = json.loads(V2_SPEC.read_text())
        self.assertEqual(v1["tables"], v2["tables"])
        self.assertEqual(
            v1["throughput_monitor"][
                "minimum_updates_before_enforcement"
            ],
            v2["throughput_monitor"][
                "minimum_updates_before_enforcement"
            ],
        )
        self.assertEqual(
            v2["throughput_monitor"]["drift_fraction"], "0.75"
        )
        self.assertEqual(
            v2["throughput_monitor"][
                "maximum_aggregate_ns_per_update"
            ],
            "4.34480050068027950",
        )


if __name__ == "__main__":
    unittest.main()
