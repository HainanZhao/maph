import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from mellin_alias_atlas_v1 import (  # noqa: E402
    ATOM_EXP,
    DENOM_EXP,
    XI_MAX,
    XI_MIN,
    alias_exponents,
    dual_support,
    stationary_formula,
    verify_all,
)

Q = Fraction


class MellinAliasAtlasTests(unittest.TestCase):
    def test_atom_diagonal(self) -> None:
        self.assertEqual(ATOM_EXP, Q(14, 15))

    def test_alias_support_endpoints(self) -> None:
        for xi in (XI_MIN, XI_MAX):
            support = dual_support(xi)
            floor = alias_exponents(xi, support["delta_h_stationary_floor"])
            top = alias_exponents(xi, support["h"])
            self.assertEqual(floor["m"], 0)
            self.assertEqual(top["m"], DENOM_EXP)

    def test_stationary_hessian_and_amplitude(self) -> None:
        row = stationary_formula()
        self.assertEqual(row["first_derivative"], "Phi'(k)=t/k-m")
        self.assertIn("-m^2/t", row["hessian_at_stationary"])
        self.assertIn("sqrt(K/|m|)", row["amplitude"])

    def test_top_alias_amplitude(self) -> None:
        xi = XI_MIN
        row = alias_exponents(xi, dual_support(xi)["h"])
        self.assertEqual(row["stationary_amplitude"], (xi - DENOM_EXP) / 2)

    def test_verification(self) -> None:
        row = verify_all()
        self.assertIn("U(0)=0", row["pair_zero_mode"])
        self.assertIn("three Mellin-alias branches", row["gate"])


if __name__ == "__main__":
    unittest.main()

