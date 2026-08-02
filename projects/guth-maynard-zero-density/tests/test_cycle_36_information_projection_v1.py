from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/information_projection_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("information_projection_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle36InformationProjectionV1Tests(unittest.TestCase):
    def test_bessel_rate_series(self):
        row = load_module().bessel_series()
        self.assertEqual(row["kappa_r_1_3_5_7"][:3], (Q(2), Q(1), Q(5, 6)))
        self.assertEqual(row["rate_r_2_4_6"], (Q(1), Q(1, 4), Q(5, 36)))
        self.assertEqual(row["second_harmonic_r_2"], (Q(1, 2),))

    def test_information_volume_exponents(self):
        row = load_module().exponent_match()
        self.assertEqual(row["information_leading"], Q(6, 25))
        self.assertEqual(row["determinant_leading"], Q(6, 25))
        self.assertEqual(row["information_quadratic_error"], Q(-9, 25))

    def test_second_harmonic_returns_to_cycle19(self):
        row = load_module().exponent_match()
        self.assertEqual(row["von_mises_second_harmonic_kernel"], Q(2, 5))
        self.assertEqual(row["von_mises_second_harmonic_kernel"], row["cycle19_popular_kernel"])

    def test_pythagorean_identity_is_explicit(self):
        row = load_module().pythagorean_identity()
        self.assertEqual(row["identity"], "D(q||u)=D(qstar||u)+D(q||qstar)")
        self.assertIn(">=0", row["excess"])

    def test_cross_checks(self):
        rows = load_module().verify_all()
        self.assertEqual(rows["bessel_series"]["rate_r_2_4_6"][0], 1)

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-36-information-projection-v1.md").read_text(encoding="utf-8")
        self.assertIn("only entropy excess", document)
        self.assertIn("No prime-kernel count", document)
        self.assertIn("scoped saturation", document)


if __name__ == "__main__":
    unittest.main()
