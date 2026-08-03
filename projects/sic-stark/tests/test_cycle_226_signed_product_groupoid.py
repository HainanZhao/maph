"""Regression tests for Cycle 226's augmented-state groupoid audit."""
from __future__ import annotations

import unittest

from proof.verify_cycle_226_signed_product_groupoid import run


class SignedProductGroupoidTests(unittest.TestCase):
    def test_all_frozen_interfaces_are_retained(self) -> None:
        result = run()
        edges = result["edge_inventory"]
        loops = result["raw_loop_audit"]
        boundary = result["construction_boundary_audit"]
        self.assertEqual(edges["directed_edge_count"], 8)
        self.assertEqual(edges["source_defined_edge_count"], 4)
        self.assertTrue(all(len(row["ordinary_gamma_residuals"]) == 2 for row in edges["edges"]))
        self.assertEqual(loops["loop_count"], 12)
        self.assertEqual(loops["augmented_closed_loop_count"], 0)
        self.assertFalse(boundary["signed_product_groupoid_constructed"])


if __name__ == "__main__":
    unittest.main()
