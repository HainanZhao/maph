import unittest
from fractions import Fraction as Q

from conventions.edge_packet_join_v1 import (
    Edge,
    Packet,
    compatible,
    incompatibility_reason,
    loop_difference,
    propagated_residual,
    verify_all,
    weighted_join_mass,
)


KWARGS = {"h_cap": 20, "critical_depth": 5, "join_constant": 2}
EDGE = Edge(target_label=7, h=30, j=45, beta=Q(0), strip_constant=1, weight=2)
PACKET = Packet(target_label=7, lower_h=20, upper_h=40, a=3, q=2, depth=5, strip_constant=1, weight=3)


class Cycle168EdgePacketJoinTests(unittest.TestCase):
    def test_exact_composition_and_weighted_bilinear_form(self):
        self.assertTrue(compatible(EDGE, PACKET, **KWARGS))
        self.assertEqual(weighted_join_mass((EDGE,), (PACKET,), **KWARGS), 6)
        self.assertEqual(
            [propagated_residual(edge=EDGE, packet=PACKET, alpha=Q(3, 2), k=k) for k in range(-5, 6)],
            [Q(0)] * 11,
        )

    def test_reason_partition_is_exhaustive_and_ordered(self):
        cases = {
            "target_label": (Edge(8, 30, 45, Q(0), 1), PACKET),
            "target_range": (Edge(7, 41, 45, Q(0), 1), PACKET),
            "packet_admissibility": (EDGE, Packet(7, 20, 40, 3, 5, 5, 1)),
            "subcritical_depth": (EDGE, Packet(7, 20, 40, 3, 2, 4, 1)),
            "strip_constant": (EDGE, Packet(7, 20, 40, 3, 2, 5, 2)),
        }
        for expected, (edge, packet) in cases.items():
            self.assertEqual(incompatibility_reason(edge, packet, **KWARGS), expected)

    def test_no_global_mass_overlap_inference_and_loop_containment(self):
        separated = Packet(target_label=8, lower_h=20, upper_h=40, a=3, q=2, depth=5, strip_constant=1, weight=999)
        self.assertEqual(weighted_join_mass((EDGE,), (separated,), **KWARGS), 0)
        self.assertEqual(loop_difference(h_initial=30, h_final=30, alpha=Q(3, 2)), 0)
        self.assertNotEqual(loop_difference(h_initial=30, h_final=29, alpha=Q(3, 2)), 0)

    def test_complete_ledger(self):
        checked = verify_all()
        self.assertIn("bipartite form", checked["overlap"])
        self.assertIn("does not lower-bound overlap", checked["boundary"])


if __name__ == "__main__":
    unittest.main()
