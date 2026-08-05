from __future__ import annotations

import unittest

from proof.audit_cycle_61_flat_stratum import audit


class Cycle61FlatStratum(unittest.TestCase):
    def test_exact_audit(self) -> None:
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["c55_independent_axis_and_sign_checks"], 8)


if __name__ == "__main__":
    unittest.main()
