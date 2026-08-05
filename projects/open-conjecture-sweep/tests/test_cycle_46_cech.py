from fractions import Fraction
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
sys.path.insert(0, str(ROOT / "proof"))

from lrc_cech_total import (
    canonical_cycle_lift,
    cone,
    downward_closure,
    owner_star_cover,
    solve_injected_class,
    solve_total_class,
    total_chain_boundary,
)
from lrc_morse_critical_projection import add, boundary, boundary_cell
from replay_cycle_46_cech_independent import highest_solve


class Cycle46CechTest(unittest.TestCase):
    def test_independent_highest_pivot_solver(self):
        tetrahedron = tuple((part, 0) for part in range(4))
        oriented = list(boundary_cell(tetrahedron).items())
        rows = [{0: coefficient} for _face, coefficient in reversed(oriented)]
        rhs = [coefficient for _face, coefficient in reversed(oriented)]
        solved = highest_solve(rows, rhs, 1)
        self.assertEqual(solved["status"], "CONSISTENT")
        self.assertEqual(solved["solution"], [Fraction(1)])
        failed = highest_solve([{}], [Fraction(1)], 0)
        self.assertEqual(failed["status"], "INCONSISTENT")
        self.assertEqual(failed["pairing"], 1)

    def test_filled_and_uncovered_tetrahedron_boundary(self):
        tetrahedron = tuple((part, 0) for part in range(4))
        cycle = boundary({tetrahedron: Fraction(1)})
        full = downward_closure([tetrahedron])
        sphere = downward_closure(boundary_cell(tetrahedron))
        for complex_cells, expected in ((full, "BOUNDARY"), (sphere, "UNCOVERED")):
            _owners, cover = owner_star_cover(complex_cells, 0)
            self.assertEqual(solve_injected_class(complex_cells, cover, cycle)["status"], expected)
            self.assertEqual(solve_total_class(complex_cells, cover, cycle)["status"], expected)

    def test_covered_nonboundary_and_lift_linearity(self):
        apex = ((0, 0), (0, 1))
        left = ((1, 0), (1, 1))
        right = ((2, 0), (2, 1))
        edges = ((left[0], right[0]), (left[1], right[0]), (left[1], right[1]), (left[0], right[1]))
        base = {
            tuple(sorted(edges[0])): Fraction(1), tuple(sorted(edges[1])): Fraction(-1),
            tuple(sorted(edges[2])): Fraction(1), tuple(sorted(edges[3])): Fraction(-1),
        }
        self.assertFalse(boundary(base))
        left_cone = cone(apex[0], base)
        right_cone = cone(apex[1], base)
        cycle = add(left_cone, right_cone, scale=Fraction(-1))
        complex_cells = downward_closure([tuple(sorted((vertex,) + edge)) for vertex in apex for edge in edges])
        _owners, cover = owner_star_cover(complex_cells, 0)
        result = solve_injected_class(complex_cells, cover, cycle)
        self.assertEqual(result["status"], "NONBOUNDARY")
        self.assertEqual(solve_total_class(complex_cells, cover, cycle)["status"], "NONBOUNDARY")
        lift, uncovered = canonical_cycle_lift(cycle, cover)
        triple_lift, _ = canonical_cycle_lift({cell: 3 * value for cell, value in cycle.items()}, cover)
        self.assertFalse(uncovered)
        self.assertFalse(total_chain_boundary(lift))
        self.assertEqual(triple_lift, {key: 3 * value for key, value in lift.items()})


if __name__ == "__main__":
    unittest.main()
