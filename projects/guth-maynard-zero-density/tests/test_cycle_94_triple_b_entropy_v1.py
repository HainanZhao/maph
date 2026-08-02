import sys
import unittest
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from triple_b_entropy_v1 import (  # noqa: E402
    F,
    c0,
    delta,
    h,
    m,
    n,
    n_prime,
    verify_all,
)


class TripleBEntropyTests(unittest.TestCase):
    def test_first_derivatives(self) -> None:
        self.assertEqual(
            sp.simplify(sp.diff(F, h)),
            sp.log(n * (h - delta) / (h * n_prime)),
        )
        actual = sp.expand_log(sp.diff(F, delta), force=True)
        expected = sp.expand_log(
            sp.log(c0 * delta * n_prime / (m * (h - delta))), force=True
        )
        self.assertEqual(sp.simplify(actual - expected), 0)

    def test_hessian_degeneracy(self) -> None:
        self.assertEqual(sp.simplify(sp.hessian(F, (h, delta)).det()), 0)

    def test_homogeneity(self) -> None:
        lam = sp.symbols("lam", positive=True)
        scaled = sp.expand_log(F.subs({h: lam * h, delta: lam * delta}), force=True)
        self.assertEqual(sp.simplify(scaled - lam * F), 0)

    def test_anchor_difference(self) -> None:
        central = c0 * n * delta / h
        self.assertEqual(
            sp.simplify(central.subs(delta, h * (n - n_prime) / n)),
            c0 * (n - n_prime),
        )

    def test_verification(self) -> None:
        row = verify_all()
        self.assertEqual(row["hessian_determinant"], "0 identically")
        self.assertIn("not covered", row["open_modes"])


if __name__ == "__main__":
    unittest.main()
