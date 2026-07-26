from pathlib import Path
import unittest

import numpy as np

from src.ac_power_flow import (
    build_ybus,
    complex_injections,
    polar_jacobian,
    solve_power_flow,
)
from src.matpower import load_matpower_case, parse_matpower_text


DATA = Path(__file__).resolve().parents[1] / "data" / "pglib-opf-v23.07"


class MatpowerTests(unittest.TestCase):
    def test_loads_pglib_case5(self):
        case = load_matpower_case(DATA / "pglib_opf_case5_pjm.m")
        self.assertEqual(case.base_mva, 100.0)
        self.assertEqual(case.bus.shape, (5, 13))
        self.assertEqual(case.gen.shape, (5, 10))
        self.assertEqual(case.branch.shape, (6, 13))

    def test_parser_does_not_evaluate_expressions(self):
        text = """
        mpc.version = '2';
        mpc.baseMVA = 100;
        mpc.bus = [1 3 0 0 0 0 1 1 0 1 1 1.1 0.9];
        mpc.gen = [1 0 0 1 -1 1 100 1 1 0];
        mpc.branch = [1 1 0.1 0.2 0 0 0 0 0 0 0 -360 360];
        mpc.gencost = [2 0 0 2 (1+1) 0];
        """
        with self.assertRaises(ValueError):
            parse_matpower_text(text)

    def test_tap_and_phase_shift_follow_matpower_convention(self):
        text = """
        mpc.version = '2';
        mpc.baseMVA = 100;
        mpc.bus = [
          10 3 0 0 0 0 1 1 0 1 1 1.1 0.9;
          20 1 0 0 0 0 1 1 0 1 1 1.1 0.9;
        ];
        mpc.gen = [10 0 0 1 -1 1 100 1 1 0];
        mpc.branch = [10 20 0.1 0.2 0.04 0 0 0 1.1 10 1 -30 30];
        """
        case = parse_matpower_text(text)
        ybus = build_ybus(case)
        series = 1 / complex(0.1, 0.2)
        tap = 1.1 * np.exp(1j * np.radians(10))
        ytt = series + 0.02j
        expected = np.array(
            [
                [ytt / (tap * np.conj(tap)), -series / np.conj(tap)],
                [-series / tap, ytt],
            ]
        )
        np.testing.assert_allclose(ybus, expected)

    def test_full_polar_jacobian_matches_finite_differences(self):
        case = load_matpower_case(DATA / "pglib_opf_case14_ieee.m")
        ybus = build_ybus(case)
        rng = np.random.default_rng(20260726)
        vm = 1.0 + rng.normal(0.0, 0.01, len(case.bus))
        va = rng.normal(0.0, 0.05, len(case.bus))
        analytical = polar_jacobian(ybus, vm, va)
        state = np.concatenate((va, vm))
        numerical = np.zeros_like(analytical)
        step = 1e-7
        for column in range(len(state)):
            plus = state.copy()
            minus = state.copy()
            plus[column] += step
            minus[column] -= step
            plus_s = complex_injections(
                ybus, plus[len(vm) :], plus[: len(vm)]
            )
            minus_s = complex_injections(
                ybus, minus[len(vm) :], minus[: len(vm)]
            )
            numerical[:, column] = np.concatenate(
                ((plus_s.real - minus_s.real), (plus_s.imag - minus_s.imag))
            ) / (2 * step)
        np.testing.assert_allclose(analytical, numerical, rtol=2e-7, atol=2e-7)

    def test_newton_power_flow_converges_on_vendored_cases(self):
        for filename in (
            "pglib_opf_case5_pjm.m",
            "pglib_opf_case14_ieee.m",
        ):
            with self.subTest(filename=filename):
                case = load_matpower_case(DATA / filename)
                result = solve_power_flow(case)
                self.assertTrue(result.converged)
                self.assertLess(result.mismatch_inf, 1e-9)


if __name__ == "__main__":
    unittest.main()
