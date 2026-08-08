from __future__ import annotations

import unittest

from proof.generate_encoder_incidence_tables import build_payload, render_latex


class EncoderIncidenceTableTests(unittest.TestCase):
    def test_symbolic_boundaries_and_rotation_firewall(self):
        payload = build_payload()
        self.assertEqual([row["width"] for row in payload["rows"]], list(range(4, 9)))
        for row in payload["rows"]:
            self.assertTrue(all(item["unclassified_count"] == 0 for item in row["normal"]))
            self.assertTrue(all(item["is_dual_component"] for item in row["normal"]))
            self.assertEqual(row["opposite"].get("unclassified_count", 0), 0)
        self.assertEqual(payload["rows"][0]["opposite"]["case"], "width-four base trace")
        self.assertEqual(payload["rows"][2]["opposite"]["case"], "even symbolic cut")
        self.assertTrue(payload["rows"][2]["opposite"]["connected_before_exceptional_deletion"])
        self.assertEqual(payload["rows"][2]["opposite"]["components_after_exceptional_deletion"], 2)

    def test_latex_is_deterministic_and_complete(self):
        first = render_latex(build_payload())
        second = render_latex(build_payload())
        self.assertEqual(first, second)
        self.assertIn("normal islands", first)
        self.assertIn("$49;32/1/3$", first)
        self.assertIn(" & 0 \\\\", first)


if __name__ == "__main__":
    unittest.main()
