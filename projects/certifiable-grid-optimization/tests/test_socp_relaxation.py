from pathlib import Path
import unittest

from src.matpower import load_matpower_case
from src.socp_relaxation import audit_socp_solution, solve_socp_relaxation


DATA = Path(__file__).resolve().parents[1] / "data" / "pglib-opf-v23.07"


class SOCPRelaxationTests(unittest.TestCase):
    def test_pinned_cases_match_reported_socp_scale_and_audit(self):
        expectations = {
            "pglib_opf_case5_pjm.m": (14500.0, 15500.0),
            "pglib_opf_case14_ieee.m": (2100.0, 2200.0),
            "pglib_opf_case5_pjm__api.m": (77000.0, 78000.0),
            "pglib_opf_case14_ieee__api.m": (5600.0, 5800.0),
        }
        for filename, interval in expectations.items():
            with self.subTest(filename=filename):
                case = load_matpower_case(DATA / filename)
                solution = solve_socp_relaxation(case)
                audit = audit_socp_solution(case, solution)
                self.assertGreater(solution.objective, interval[0])
                self.assertLess(solution.objective, interval[1])
                self.assertLess(audit.maximum_violation, 2e-6)


if __name__ == "__main__":
    unittest.main()
