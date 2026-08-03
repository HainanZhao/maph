from __future__ import annotations

import unittest

from proof.verify_cycle_211_cusp_asymptotic_flat_sections import run


class CuspAsymptoticFlatSectionTests(unittest.TestCase):
    def setUp(self):
        self.result = run()

    def test_unique_exponent_extrema(self):
        extrema = self.result["exponent_extrema"]
        self.assertEqual(extrema["maximum"], {"exponent": 20, "unique_label": [0, 5]})
        self.assertEqual(extrema["minimum"], {"exponent": -25, "unique_label": [5, 0]})

    def test_two_all_channel_cusp_lines(self):
        sections = self.result["cusp_sections"]
        self.assertEqual(sections["record_count"], 6)
        self.assertEqual(sections["all_h_infinity_line"], "[e_(0,5)]")
        self.assertEqual(sections["all_h_zero_line"], "[e_(5,0)]")

    def test_declared_symmetry_does_not_select(self):
        self.assertTrue(self.result["a6_preservation_audit"]["all_cusp_lines_projectively_preserved"])
        self.assertEqual(self.result["nonselection_audit"]["selection_status"], "OPEN_REQUIRES_ADDITIONAL_SOURCE_ORIENTATION_OR_BOUNDARY_THEOREM")


if __name__ == "__main__":
    unittest.main()
