from __future__ import annotations

import unittest

from proof.verify_cycle_203_inverse_normal_line import run


class InverseNormalLineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = run()

    def test_a6_contraction_is_exact(self) -> None:
        multiplier = self.result["a6_axis_multiplier"]
        self.assertEqual(multiplier["mobius_derivative_at_beta"], "A6'(beta)=1/(24*beta-5)^2=beta^(-6)")
        self.assertEqual(multiplier["cross_ratio_coordinate"], "(gamma(s)-beta)/(gamma(s)-beta^(-1))=i*s")
        self.assertEqual(multiplier["endpoint_tangent"], "gamma'(0)=i*sqrt(21)!=0")

    def test_positive_rescalings_preserve_declared_source_data(self) -> None:
        symmetry = self.result["rescaling_symmetry"]
        self.assertEqual(symmetry["scaling_group"], "c in R_{>0}")
        self.assertEqual(symmetry["not_fixed_by_source_data"], "a nonzero scale for s")

    def test_logarithmic_form_is_not_normal_trivialization(self) -> None:
        line = self.result["normal_line_obstruction"]
        self.assertIn("not a nonzero element", line["logarithmic_form_failure"])
        self.assertEqual(line["only_invariant_inverse_vector"], "0")

    def test_scope_is_limited(self) -> None:
        self.assertIn("does not exclude", self.result["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
