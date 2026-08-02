from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/joint_pk_large_sieve_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("joint_pk_large_sieve_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle45JointPkLargeSieveV1Tests(unittest.TestCase):
    def test_naive_wrap_coloring(self):
        row = load_module().joint_sum(Q(11, 25), Q(1))
        self.assertEqual(row["joint_bound"], Q(38, 25))
        self.assertEqual(row["saving"], Q(2, 25))

    def test_full_dealiasing(self):
        row = load_module().joint_sum(Q(11, 25), Q(0))
        self.assertEqual(row["joint_bound"], Q(13, 10))
        self.assertEqual(row["saving"], Q(3, 10))

    def test_alias_thresholds(self):
        module = load_module()
        self.assertEqual(module.required_alias_exponent(Q(11, 25), Q(4, 25)), Q(7, 11))
        self.assertEqual(module.required_alias_exponent(Q(11, 25), Q(7, 50)), Q(8, 11))

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-45-joint-pk-large-sieve-v1.md").read_text(encoding="utf-8")
        self.assertIn("Primality is not used", document)
        self.assertIn("not yet an `LCAM_s`", document)
        self.assertIn("No curved prime-pair estimate", document)


if __name__ == "__main__":
    unittest.main()
