import unittest

from conventions.full_triple_b_symbol_v1 import anchor_absorption, symbolic_full_symbol, theorem_record


class FullTripleBSymbolTests(unittest.TestCase):
    def test_symbol(self) -> None:
        row = symbolic_full_symbol()
        self.assertIn("sqrt(m*n*n')", row["chart_amplitude"])
        self.assertEqual(row["V_arguments"], ("n/Q", "n'/Q"))
        self.assertIn("translates", row["anchor_role"])

    def test_anchor_absorption(self) -> None:
        self.assertTrue(anchor_absorption(scale=30, p0=5, q0=6, B0=5, C0=6, Q=30))
        self.assertFalse(anchor_absorption(scale=6, p0=5, q0=6, B0=5, C0=6, Q=30))

    def test_boundary(self) -> None:
        row = theorem_record()
        self.assertIn("1/30", row["aggregate"])
        self.assertIn("smooth perfect-power", row["boundary"])


if __name__ == "__main__":
    unittest.main()
