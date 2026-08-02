import unittest
from fractions import Fraction
from math import gcd

import sympy as sp

from conventions.actual_scale_phase_v1 import (
    ActualScaleLattice,
    bounded_variation_bound,
    exact_root_of_unity_sum,
    geometric_factor,
    symbolic_phase_homogeneity,
    theorem_record,
)


class ActualScalePhaseTests(unittest.TestCase):
    def test_scale_lattice_exhaustive(self) -> None:
        for A0 in range(1, 9):
            for S0 in range(1, 9):
                if gcd(A0, S0) != 1:
                    continue
                for B0 in range(1, 6):
                    for C0 in range(1, 6):
                        for p0, q0 in ((1, 1), (2, 3), (3, 5), (5, 2)):
                            lattice = ActualScaleLattice(A0, S0, B0, C0, p0, q0)
                            lattice.verify_range(5 * lattice.lambda0 + 3)
                            self.assertTrue(all(value > 0 for value in lattice.base_indices))

    def test_symbolic_homogeneity(self) -> None:
        record = symbolic_phase_homogeneity()
        self.assertIn("Phi_ell=ell*Phi0", record["full_phase"])

    def test_exact_root_of_unity_sums(self) -> None:
        self.assertEqual(exact_root_of_unity_sum(1, 2, 8), 0)
        self.assertEqual(exact_root_of_unity_sum(1, 3, 3), 0)
        self.assertEqual(sp.simplify(exact_root_of_unity_sum(0, 5, 7)), 7)

    def test_geometric_factor(self) -> None:
        self.assertEqual(geometric_factor(Fraction(0), 10), 10)
        self.assertEqual(geometric_factor(Fraction(1, 2), 10), 1)
        self.assertEqual(geometric_factor(Fraction(1, 100), 10), 10)

    def test_exact_bv_alternating_example(self) -> None:
        weights = (Fraction(1), Fraction(3, 4), Fraction(1, 2), Fraction(1, 4))
        actual = abs(sum(weight * (-1) ** (index + 1) for index, weight in enumerate(weights)))
        variation = sum(abs(weights[index] - weights[index + 1]) for index in range(3))
        bound = bounded_variation_bound(
            phase=Fraction(1, 2),
            length=4,
            terminal_abs=abs(weights[-1]),
            variation=variation,
        )
        self.assertLessEqual(actual, bound)

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("lcm", record["lambda0"])
        self.assertIn("Phi_ell=ell*Phi0", record["phase"])
        self.assertIn("amplitude variation", record["boundary"])


if __name__ == "__main__":
    unittest.main()
