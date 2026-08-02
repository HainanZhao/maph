import unittest

from conventions.vector_autocorrelation_v1 import (
    autocorrelation,
    selected_autocorrelation,
    taylor_remainder_factor,
    theorem_record,
    vector_moments,
)


class VectorAutocorrelationTests(unittest.TestCase):
    def test_vector_moment_orientation(self) -> None:
        rows = ((1 + 0j, -1 + 0j), (2 + 0j, 3 + 0j))
        moments = vector_moments(rows, (2 + 0j, 3 + 0j), 1)
        self.assertEqual(moments[0], (0j, 5 + 0j))
        self.assertEqual(moments[1], (-1 + 0j, 13 + 0j))

    def test_autocorrelation_sum_identity(self) -> None:
        sequence = (1 + 1j, 2 - 1j, -1 + 2j)
        total = sum((autocorrelation(sequence, d) for d in range(-2, 3)), 0j)
        self.assertEqual(total, sum(sequence, 0j) * sum(sequence, 0j).conjugate())

    def test_selected_mask_is_explicit(self) -> None:
        sequence = (1 + 0j, 2 + 0j, 3 + 0j)
        self.assertEqual(selected_autocorrelation(sequence, 1, (1 + 0j, 0j)), 2 + 0j)
        self.assertNotEqual(selected_autocorrelation(sequence, 1, (1 + 0j, -1 + 0j)), autocorrelation(sequence, 1))

    def test_remainder_factor(self) -> None:
        self.assertEqual(taylor_remainder_factor(0.0, 3), 0.0)

    def test_record_preserves_frequency_and_mask(self) -> None:
        row = theorem_record()
        self.assertIn("ell^m", row["vector_moments"])
        self.assertIn("mask", row["selection_mask"])
        self.assertIn("no bound", row["boundary"])


if __name__ == "__main__":
    unittest.main()
