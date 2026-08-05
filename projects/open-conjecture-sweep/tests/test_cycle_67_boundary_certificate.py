import unittest

from proof.check_cycle67_boundary_certificate import audit
from proof.cycle67_strip_boundary_factors import strip


class Cycle67BoundaryCertificateTest(unittest.TestCase):
    def test_complete_canonical_audit(self):
        checked = audit()
        self.assertEqual(checked["epistemic_status"], "PROVED")
        self.assertEqual(checked["source_invariant_charts"], 9)
        self.assertEqual(checked["final_certificate_charts"], 31)

    def test_exact_boundary_factor_multiplicity(self):
        # y^3 (1-x)^3 (2+r) in exponent order x,y,r,h.
        polynomial = {
            (0, 3, 0, 0): 2,
            (0, 3, 1, 0): 1,
            (1, 3, 0, 0): -6,
            (1, 3, 1, 0): -3,
            (2, 3, 0, 0): 6,
            (2, 3, 1, 0): 3,
            (3, 3, 0, 0): -2,
            (3, 3, 1, 0): -1,
        }
        quotient, factors = strip(polynomial)
        self.assertEqual(factors, {"y": 3, "1-x": 3})
        self.assertEqual(quotient, {(0, 0, 0, 0): 2, (0, 0, 1, 0): 1})


if __name__ == "__main__":
    unittest.main()
