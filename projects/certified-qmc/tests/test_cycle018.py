from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

from src.certificate import canonical_sha256


PROJECT = Path(__file__).resolve().parents[1]
SPEC = PROJECT / "data" / "cycle-018-usability-spec.json"
PREREG = (
    PROJECT
    / "data"
    / "cycle-018-usability-preregistration.json"
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


class Cycle018Tests(unittest.TestCase):
    def test_usability_preregistration_and_schedule_budget(self):
        prereg = json.loads(PREREG.read_text())
        supplied = prereg.pop("preregistration_sha256")
        self.assertEqual(canonical_sha256(prereg), supplied)
        self.assertFalse(prereg["production_started"])
        self.assertEqual(
            prereg["production_spec"]["sha256"],
            digest(SPEC),
        )
        self.assertFalse(
            prereg["schedule"]["extension_required"]
        )
        self.assertLessEqual(
            prereg["schedule"]["maximum_required_work_primes"],
            prereg["schedule"]["available_work_primes"],
        )
        self.assertEqual(prereg["grid"]["logical_entries"], 54)
        self.assertEqual(prereg["grid"]["reused_j2_entries"], 18)

    def test_only_nonduplicated_profiles_are_computed(self):
        spec = json.loads(SPEC.read_text())
        self.assertEqual(len(spec["tables"]), 12)
        self.assertEqual(spec["logical_dimensions"], [16, 64, 256])
        self.assertEqual(
            {table["weight_power"] for table in spec["tables"]},
            {1, 3},
        )
        self.assertEqual(
            {table["N"] for table in spec["tables"]},
            {2**10, 2**15, 2**20},
        )


if __name__ == "__main__":
    unittest.main()
