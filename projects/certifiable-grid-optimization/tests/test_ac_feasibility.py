from pathlib import Path
import unittest

from src.ac_feasibility import recover_operational_dispatch
from src.ac_power_flow import build_ybus, solve_power_flow_with_q_limits
from src.full_ac_recovery import recover_full_ac_candidates, relaxed_injections
from src.matpower import load_matpower_case
from src.socp_relaxation import solve_socp_relaxation


DATA = Path(__file__).resolve().parents[1] / "data" / "pglib-opf-v23.07"


class ACFeasibilityTests(unittest.TestCase):
    def test_ieee14_socp_recovery_produces_audited_dispatch(self):
        case = load_matpower_case(DATA / "pglib_opf_case14_ieee.m")
        relaxation = solve_socp_relaxation(case)
        ybus = build_ybus(case)
        target = relaxed_injections(ybus, relaxation.moments)
        recovery = recover_full_ac_candidates(
            case, relaxation.moments
        )["weighted phase LS"]
        limited = solve_power_flow_with_q_limits(
            case,
            target,
            recovery.voltage_magnitudes,
            recovery.voltage_angles,
        )
        power_flow = limited.power_flow
        dispatch = recover_operational_dispatch(
            case,
            power_flow,
            relaxation.generator_p,
            relaxation.generator_q,
        )
        self.assertTrue(power_flow.converged)
        self.assertLess(dispatch.audit.maximum_violation, 1e-5)
        self.assertGreaterEqual(dispatch.objective, relaxation.objective)


if __name__ == "__main__":
    unittest.main()
