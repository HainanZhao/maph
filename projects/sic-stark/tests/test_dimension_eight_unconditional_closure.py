"""End-to-end regression checks for both unconditional d=8 strata."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_gp(relative: str) -> str:
    result = subprocess.run(
        ["gp", "-q", relative],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    fatal_markers = (
        "syntax error",
        "user error",
        "nonexistent component",
        "at top-level",
    )
    lowered = result.stderr.lower()
    if any(marker in lowered for marker in fatal_markers):
        raise RuntimeError(
            f"PARI/GP reported an error in {relative}:\n{result.stderr}"
        )
    return result.stdout


class DimensionEightUnconditionalClosureTests(unittest.TestCase):
    def test_conductor_three_linear_cm_closure(self) -> None:
        reinduction = run_gp(
            "scripts/dimension_eight_linear_cm_reinduction.gp"
        )
        self.assertEqual(
            reinduction.count("LINEAR_REINDUCTION_VERIFIED_PACKET="),
            4,
        )
        self.assertEqual(
            reinduction.count("LINEAR_REINDUCTION_VERIFIED_PACKET=0"),
            2,
        )
        self.assertEqual(
            reinduction.count("LINEAR_REINDUCTION_VERIFIED_PACKET=1"),
            2,
        )

        lattice = run_gp("scripts/dimension_eight_cm_unit_lattice.gp")
        self.assertIn("CM_UNIT_LATTICE_AUDIT_COMPLETE=1", lattice)
        self.assertIn(
            "PACKET_0_SELECTED_RAY_CHARACTER=[6, 1]", lattice
        )
        self.assertIn(
            "PACKET_1_SELECTED_RAY_CHARACTER=[2, 1]", lattice
        )
        self.assertIn(
            "FINITE_CANDIDATE_RAY_LABEL_SELECTION=1", lattice
        )
        bridge = run_gp(
            "scripts/dimension_eight_cm_real_unit_bridge.gp"
        )
        self.assertIn("CM_TO_REAL_UNIT_BRIDGE_CERTIFIED=1", bridge)

        orientation = (
            ROOT / "certificates/dimension-eight-cm-orientation.txt"
        ).read_text()
        self.assertIn(
            "CM_STARK_UNIT_COORDINATE_ORBITS_ISOLATED=1",
            orientation,
        )
        self.assertIn(
            "DIMENSION_EIGHT_ORIENTED_CM_BRIDGE_CERTIFIED=1",
            orientation,
        )

    def test_maximal_order_quadratic_closure(self) -> None:
        tuple_audit = run_gp(
            "scripts/dimension_eight_maximal_tuple_audit.gp"
        )
        self.assertIn("RAY_8_INFINITY_2_STRUCTURE=[2, 2]", tuple_audit)
        self.assertIn("KOPP_EXPONENT=1", tuple_audit)
        self.assertEqual(tuple_audit.count("CHARACTERISTIC="), 63)
        self.assertIn(
            "SIX_FACTOR_AFK_SPECIALIZATION_DATA=1", tuple_audit
        )
        self.assertIn(
            "EXACT_QUADRATIC_INVERSE_FOURIER_MAGNITUDE_TABLE=1",
            tuple_audit,
        )

        units = run_gp(
            "scripts/dimension_eight_maximal_quadratic_units.gp"
        )
        self.assertIn("BNFCERTIFY_0=1", units)
        self.assertIn("BNFCERTIFY_1=1", units)
        self.assertIn("REGULATOR_INDEX_0=2", units)
        self.assertIn("REGULATOR_INDEX_1=2", units)
        self.assertIn(
            "QUADRATIC_CHARACTER_PACKET_UNCONDITIONAL=1",
            units,
        )

        finite = subprocess.run(
            [
                sys.executable,
                "scripts/dimension_eight_maximal_exact_tcc.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertIn(
            "DIMENSION_EIGHT_MAXIMAL_EXACT_TCC_CERTIFIED=1",
            finite,
        )
        self.assertEqual(finite.count("NONZERO_MINORS=0"), 2)


if __name__ == "__main__":
    unittest.main()
