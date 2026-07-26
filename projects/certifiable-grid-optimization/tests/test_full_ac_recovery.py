from pathlib import Path
import math
import unittest

import numpy as np

from src.ac_power_flow import (
    build_ybus,
    solve_power_flow,
    solve_power_flow_to_injections,
)
from src.full_ac_recovery import (
    generate_edge_relaxed_moments,
    recover_full_ac_candidates,
    relaxed_injections,
    score_full_ac_recovery,
)
from src.matpower import load_matpower_case


DATA = Path(__file__).resolve().parents[1] / "data" / "pglib-opf-v23.07"


class FullACRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = load_matpower_case(DATA / "pglib_opf_case5_pjm.m")
        cls.solution = solve_power_flow(cls.case)
        cls.ybus = build_ybus(cls.case)

    def test_exact_moments_recover_zero_residual(self):
        moments = generate_edge_relaxed_moments(
            self.ybus,
            self.solution.voltage_magnitudes,
            self.solution.voltage_angles,
            np.random.default_rng(1),
            phase_sigma=0.0,
            radial_sigma=0.0,
        )
        for name, recovery in recover_full_ac_candidates(
            self.case, moments
        ).items():
            with self.subTest(name=name):
                score = score_full_ac_recovery(
                    self.case, moments, recovery
                )
                self.assertLess(score.injection_residual_inf, 1e-10)
                self.assertLess(score.moment_residual_bound, 1e-10)

    def test_local_edge_psd_and_residual_certificate(self):
        moments = generate_edge_relaxed_moments(
            self.ybus,
            self.solution.voltage_magnitudes,
            self.solution.voltage_angles,
            np.random.default_rng(20260726),
            phase_sigma=0.01,
            radial_sigma=0.005,
        )
        for u in range(len(moments)):
            for v in range(u + 1, len(moments)):
                if moments[u, v] != 0:
                    self.assertLessEqual(
                        abs(moments[u, v]) ** 2,
                        (moments[u, u] * moments[v, v]).real + 1e-12,
                    )
        for name, recovery in recover_full_ac_candidates(
            self.case, moments
        ).items():
            with self.subTest(name=name):
                score = score_full_ac_recovery(
                    self.case, moments, recovery
                )
                self.assertLessEqual(
                    score.injection_residual_inf,
                    score.moment_residual_bound + 1e-12,
                )
                self.assertTrue(
                    np.isfinite(score.inverse_reduced_jacobian_inf)
                )

    def test_recovered_voltage_repairs_to_relaxed_injections(self):
        moments = generate_edge_relaxed_moments(
            self.ybus,
            self.solution.voltage_magnitudes,
            self.solution.voltage_angles,
            np.random.default_rng(7),
            phase_sigma=0.005,
            radial_sigma=0.002,
        )
        target = relaxed_injections(self.ybus, moments)
        for name, recovery in recover_full_ac_candidates(
            self.case, moments
        ).items():
            with self.subTest(name=name):
                repaired = solve_power_flow_to_injections(
                    self.case,
                    target,
                    recovery.voltage_magnitudes,
                    recovery.voltage_angles,
                )
                self.assertTrue(repaired.converged)
                self.assertLess(repaired.mismatch_inf, 1e-9)

    def test_radial_approximation_factor(self):
        rng = np.random.default_rng(19)
        gamma = 1.0
        kappa = 0.2
        factor = math.sqrt(
            1.0
            + (
                gamma
                / (2.0 * math.sin(gamma / 2.0))
            )
            ** 2
            / kappa
        )
        for _ in range(1000):
            rank_one_magnitude = float(rng.uniform(0.5, 2.0))
            target_magnitude = rank_one_magnitude * float(
                rng.uniform(kappa, 1.0)
            )
            correction = float(rng.uniform(-gamma, gamma))
            exact = abs(
                rank_one_magnitude * np.exp(1j * correction)
                - target_magnitude
            )
            surrogate = (
                rank_one_magnitude
                - target_magnitude
                + rank_one_magnitude * abs(correction)
            )
            self.assertLessEqual(exact, surrogate + 1e-12)
            self.assertLessEqual(surrogate, factor * exact + 1e-12)


if __name__ == "__main__":
    unittest.main()
