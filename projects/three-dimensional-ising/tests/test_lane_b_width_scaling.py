from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.lane_b_width_scaling import (  # noqa: E402
    checkerboard_boundary_rotation,
    genus_bounds,
    physical_frontier_dimension,
    symbolic_rank_upper_bound,
)
from proof.verify_lane_b_genus3 import _rotation_faces  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


class WidthScalingTest(unittest.TestCase):
    def test_dimensions_and_bounds(self) -> None:
        self.assertEqual([physical_frontier_dimension(w) for w in (2, 3, 4)], [8, 256, 32768])
        self.assertEqual(genus_bounds(7, 2), (0, 0))
        self.assertEqual(genus_bounds(7, 3), (6, 6))
        self.assertEqual(genus_bounds(6, 4), (9, 9))
        self.assertEqual(genus_bounds(5, 4), (7, 8))
        self.assertEqual(symbolic_rank_upper_bound(4), 1 << 23)

    def test_width_four_quadrangulation(self) -> None:
        for n, expected_genus in ((2, 1), (4, 5), (6, 9)):
            vertices, edges = cubic_box((n, 4, 4))
            rotation = checkerboard_boundary_rotation(n, 4)
            _, faces = _rotation_faces(vertices, edges, rotation)
            self.assertTrue(all(len(face) == 4 for face in faces))
            self.assertEqual((2 - (len(vertices) - len(edges) + len(faces))) // 2, expected_genus)


if __name__ == "__main__":
    unittest.main()
