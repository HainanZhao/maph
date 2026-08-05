from __future__ import annotations
import unittest
from proof.check_cycle_54_bipartite_directional import audit

class Cycle54Test(unittest.TestCase):
    def test_control(self):
        self.assertEqual(audit()["status"], "PASS")

if __name__ == "__main__": unittest.main()
