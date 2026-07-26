import cmath
import math
import unittest

from src.cycle_certificate import (
    balanced_unit_triangle_recovery,
    EdgeMoment,
    cycle_holonomy,
    cycle_phase_defect,
    defect_to_repair_certificate,
    edge_residual,
    injection_residual_bound,
    radial_defect,
    reconstruct_from_tree,
    residual_from_defects,
    residual_identity,
)


class CycleCertificateTests(unittest.TestCase):
    def setUp(self):
        self.diagonal = {0: 1.0, 1: 4.0, 2: 9.0}

    def exact_triangle(self):
        phases = {0: 0.2, 1: -0.4, 2: 0.7}
        voltage = {
            vertex: math.sqrt(self.diagonal[vertex]) * cmath.exp(1j * phase)
            for vertex, phase in phases.items()
        }
        edges = [
            EdgeMoment(0, 1, voltage[0] * voltage[1].conjugate()),
            EdgeMoment(1, 2, voltage[1] * voltage[2].conjugate()),
            EdgeMoment(0, 2, voltage[0] * voltage[2].conjugate()),
        ]
        return voltage, edges

    def test_exact_triangle_has_no_defects(self):
        _, edges = self.exact_triangle()
        for edge in edges:
            self.assertAlmostEqual(radial_defect(self.diagonal, edge), 0.0)
        self.assertAlmostEqual(cycle_phase_defect(edges, [0, 1, 2]), 0.0)
        self.assertAlmostEqual(abs(cycle_holonomy(edges, [0, 1, 2])), 1.0)

    def test_tree_recovery_matches_exact_triangle(self):
        _, edges = self.exact_triangle()
        recovered = reconstruct_from_tree(
            self.diagonal, edges, [(0, 1), (1, 2)], root=0
        )
        for edge in edges:
            self.assertAlmostEqual(edge_residual(recovered, edge), 0.0)

    def test_phase_only_certificate_is_false(self):
        diagonal = {0: 1.0, 1: 1.0, 2: 1.0}
        edges = [
            EdgeMoment(0, 1, 0.8),
            EdgeMoment(1, 2, 0.8),
            EdgeMoment(0, 2, 0.8),
        ]
        self.assertAlmostEqual(cycle_phase_defect(edges, [0, 1, 2]), 0.0)
        for edge in edges:
            self.assertAlmostEqual(radial_defect(diagonal, edge), 0.36)

    def test_chord_phase_error_equals_cycle_error(self):
        _, edges = self.exact_triangle()
        perturbed = [
            edges[0],
            edges[1],
            EdgeMoment(0, 2, edges[2].value * cmath.exp(0.17j)),
        ]
        recovered = reconstruct_from_tree(
            self.diagonal, perturbed, [(0, 1), (1, 2)], root=0
        )
        self.assertGreater(edge_residual(recovered, perturbed[2]), 0.0)
        left, right = residual_identity(
            self.diagonal, recovered, perturbed[2]
        )
        self.assertAlmostEqual(left, right)

    def test_residual_identity_with_radial_and_phase_error(self):
        _, edges = self.exact_triangle()
        perturbed_edge = EdgeMoment(
            0, 2, 0.73 * edges[2].value * cmath.exp(-0.31j)
        )
        all_edges = [edges[0], edges[1], perturbed_edge]
        recovered = reconstruct_from_tree(
            self.diagonal, all_edges, [(0, 1), (1, 2)], root=0
        )
        left, right = residual_identity(
            self.diagonal, recovered, perturbed_edge
        )
        self.assertAlmostEqual(left, right)

        phase_defect = abs(
            1.0
            - (
                recovered[perturbed_edge.u]
                * recovered[perturbed_edge.v].conjugate()
                / abs(
                    recovered[perturbed_edge.u]
                    * recovered[perturbed_edge.v].conjugate()
                )
            )
            / (perturbed_edge.value / abs(perturbed_edge.value))
        )
        predicted = residual_from_defects(
            self.diagonal, perturbed_edge, phase_defect
        )
        self.assertAlmostEqual(predicted**2, left)

    def test_injection_bound_dominates_complex_residual(self):
        diagonal = {0: 1.0, 1: 1.0, 2: 1.0}
        edges = [
            EdgeMoment(0, 1, 0.8),
            EdgeMoment(1, 2, 0.9),
            EdgeMoment(0, 2, 0.7 * cmath.exp(0.2j)),
        ]
        recovered = reconstruct_from_tree(
            diagonal, edges, [(0, 1), (1, 2)], root=0
        )
        y01 = 2.0 - 3.0j
        y02 = -1.5 + 0.25j
        actual = abs(
            y01.conjugate()
            * (
                recovered[0] * recovered[1].conjugate()
                - edges[0].value
            )
            + y02.conjugate()
            * (
                recovered[0] * recovered[2].conjugate()
                - edges[2].value
            )
        )
        chord_phase_defect = abs(
            1.0
            - (
                recovered[0] * recovered[2].conjugate()
                / abs(recovered[0] * recovered[2].conjugate())
            )
            / (edges[2].value / abs(edges[2].value))
        )
        bound = injection_residual_bound(
            0,
            [(edges[0], 0.0), (edges[2], chord_phase_defect)],
            {1: abs(y01), 2: abs(y02)},
            diagonal,
        )
        self.assertLessEqual(actual, bound + 1e-12)

    def test_defect_to_repair_composition(self):
        certificate = defect_to_repair_certificate(
            residual_bound=0.01,
            inverse_jacobian_norm=1.0,
            jacobian_lipschitz=5.0,
        )
        self.assertTrue(certificate.certified)
        self.assertGreaterEqual(certificate.radius_bound, 0.01)

        ill_conditioned = defect_to_repair_certificate(
            residual_bound=1e-9,
            inverse_jacobian_norm=1e9,
            jacobian_lipschitz=5.0,
        )
        self.assertFalse(ill_conditioned.certified)

    def test_balanced_projection_beats_spanning_tree_on_phase_error(self):
        delta = 0.3
        diagonal = {0: 1.0, 1: 1.0, 2: 1.0}
        edges = [
            EdgeMoment(0, 1, 1.0),
            EdgeMoment(1, 2, 1.0),
            EdgeMoment(0, 2, cmath.exp(-1j * delta)),
        ]
        tree_voltage = reconstruct_from_tree(
            diagonal, edges, [(0, 1), (1, 2)], root=0
        )
        balanced_voltage = balanced_unit_triangle_recovery(edges)
        tree_squared = sum(
            edge_residual(tree_voltage, edge) ** 2 for edge in edges
        )
        balanced_squared = sum(
            edge_residual(balanced_voltage, edge) ** 2 for edge in edges
        )
        expected_balanced = 12.0 * math.sin(delta / 6.0) ** 2
        self.assertAlmostEqual(balanced_squared, expected_balanced)
        self.assertLess(balanced_squared, tree_squared)


if __name__ == "__main__":
    unittest.main()
