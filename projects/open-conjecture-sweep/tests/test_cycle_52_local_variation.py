from __future__ import annotations

import unittest

from proof.check_cycle_52_local_variation import audit


class Cycle52LocalVariationTest(unittest.TestCase):
    def test_exact_census_audit(self):
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["directions"], 512)
        self.assertEqual(result["local_negative"], 0)
        self.assertEqual(result["first_degree_counts"], {"2": 489, "4": 23})


if __name__ == "__main__":
    unittest.main()
