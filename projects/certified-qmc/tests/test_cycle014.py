from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

from src.certificate import canonical_sha256


PROJECT = Path(__file__).resolve().parents[1]


class Cycle014Tests(unittest.TestCase):
    def test_full_schedule_manifest_and_samples_replay(self):
        manifest_path = (
            PROJECT
            / "certificates"
            / "cycle-014-prime-schedule-manifest.json"
        )
        manifest = json.loads(manifest_path.read_text())
        supplied = manifest.pop("certificate_sha256")
        self.assertEqual(canonical_sha256(manifest), supplied)
        self.assertTrue(manifest["gate"]["cycle_014_exit_gate_passed"])
        self.assertTrue(
            manifest["gate"][
                "byte_identical_regeneration_demonstrated"
            ]
        )
        schedule_path = PROJECT / manifest["schedule"]["path"]
        raw = schedule_path.read_bytes()
        self.assertEqual(
            sha256(raw).hexdigest(), manifest["schedule"]["sha256"]
        )
        schedule = json.loads(raw)
        self.assertEqual(schedule["count"], 3740)
        self.assertEqual(len(schedule["primes"]), 3740)
        self.assertEqual(
            [row["role"] for row in schedule["primes"][-2:]],
            ["OVERFLOW", "OVERFLOW"],
        )
        self.assertTrue(
            all(row["c"].bit_length() <= 30 for row in schedule["primes"])
        )
        old = json.loads(
            (
                PROJECT
                / "certificates"
                / "cycle-009-prime-schedule-40.json"
            ).read_text()
        )
        for current, previous in zip(schedule["primes"][:40], old["primes"]):
            self.assertEqual(current["p"], previous["prime"])
            self.assertEqual(current["c"], previous["coefficient"])
            self.assertEqual(
                current["primitive_root"], previous["primitive_root"]
            )
        for section in ("generator", "independent_verifier"):
            self.assertEqual(
                sha256(
                    (PROJECT / manifest[section]["path"]).read_bytes()
                ).hexdigest(),
                manifest[section]["sha256"],
            )
        for index in (0, 39, 3737, 3738, 3739):
            row = schedule["primes"][index]
            p = int(row["p"])
            c = row["c"]
            self.assertEqual(p, c * 2**32 + 1)
            certificate = row["n_minus_one_certificate"]
            witness = certificate["witness_a"]
            self.assertEqual(pow(witness, p - 1, p), 1)
            self.assertTrue(
                all(
                    int(check["gcd_power_residue_minus_one_with_p"]) == 1
                    for check in certificate["prime_divisor_checks"]
                )
            )


if __name__ == "__main__":
    unittest.main()
