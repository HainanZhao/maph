import unittest

from conventions.actual_edge_coefficient_v1 import (
    correlation_weights,
    frequency_dependent_moments,
    theorem_record,
)


class ActualEdgeCoefficientTests(unittest.TestCase):
    def test_oriented_correlation_coefficients(self) -> None:
        left = (1 + 2j, 2 - 1j)
        right = (3 - 1j, -1 + 4j)
        self.assertEqual(
            correlation_weights(left, right),
            tuple(r * l.conjugate() for l, r in zip(left, right)),
        )

    def test_moments_remain_frequency_dependent(self) -> None:
        rows = frequency_dependent_moments(
            ((1 + 0j, -1 + 0j), (1 + 0j, 1 + 0j)),
            (2 + 0j, 3 + 0j),
            1,
        )
        self.assertEqual(rows[0], (0j, -1 + 0j))
        self.assertEqual(rows[1], (2 + 0j, 5 + 0j))

    def test_record_marks_the_type_boundary(self) -> None:
        row = theorem_record()
        self.assertIn("no sealed coefficient-preserving", row["typed_boundary"])
        self.assertIn("M_m(d;ell)", row["cycle143_correction"])
        self.assertIn("not a signed-moment", row["boundary"])


if __name__ == "__main__":
    unittest.main()
