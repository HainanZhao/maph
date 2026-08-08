import json
from pathlib import Path
import unittest

from proof.verify_lane_b_homogeneous_w3 import (
    ANISOTROPIC_POINTS,
    ISOTROPIC_POINTS,
    _frozen_indices,
    _parameterized_source,
)


ROOT = Path(__file__).resolve().parents[1]


class HomogeneousWidthThreeTests(unittest.TestCase):
    def test_preregistered_points_and_degree_bounds(self):
        prereg = json.loads(
            (ROOT / "discovery/cycle-14-homogeneous-locus-preregistration.json").read_text()
        )
        self.assertEqual([list(point) for point in ANISOTROPIC_POINTS], prereg["fixed_points"]["anisotropic_per_prime"])
        self.assertEqual(list(ISOTROPIC_POINTS), prereg["fixed_points"]["isotropic_per_prime"])
        self.assertEqual(prereg["degree_bounds"]["minor_multidegree_at_most"], {"tx": 20736, "ty": 15360, "tz": 15360})
        self.assertEqual(prereg["degree_bounds"]["isotropic_determinant_degree_at_most"], 51456)

    def test_frozen_minor_and_parameterization_anchors(self):
        indices = _frozen_indices()
        self.assertEqual(indices["shift"], 10)
        self.assertEqual(len(indices["left_characters"]), 256)
        self.assertEqual(len(indices["right_characters"]), 256)
        source = _parameterized_source()
        self.assertIn("const u64 axis_weight[3] = {tx, ty, tz};", source)
        self.assertIn("#pragma omp parallel for", source)


if __name__ == "__main__":
    unittest.main()
