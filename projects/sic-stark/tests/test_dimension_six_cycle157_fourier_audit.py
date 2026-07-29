#!/usr/bin/env python3
"""Regression gates for the cycle-157 Fourier-normalization audit."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import unittest

import mpmath as mp


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
CERTIFICATE = (
    ROOT
    / "certificates"
    / "dimension-six-cycle157-fourier-normalization-audit.json"
)
sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "cycle157",
    SCRIPTS / "dimension_six_cycle157_fourier_normalization_audit.py",
)
CYCLE157 = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CYCLE157)


class DimensionSixCycle157FourierAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = json.loads(CERTIFICATE.read_text())

    def test_all_aliases_keep_one_finite_frequency(self):
        ledger = CYCLE157.finite_frequency_ledger()
        self.assertEqual(ledger["records_checked"], 900)
        self.assertTrue(ledger["all_aliases_keep_frequency_(a,b)"])

    def test_restored_gauge_has_boundary_minus_q_step(self):
        with mp.workdps(60):
            beta = CYCLE157.cycle156.beta_endpoint()
            actual = CYCLE157.gauge_step_ratio(beta)
            expected = -mp.e ** (2 * mp.pi * 1j * beta)
            self.assertLess(abs(actual / expected - 1), mp.mpf("1e-50"))

    def test_certificate_retires_unsupported_implication(self):
        result = self.certificate
        self.assertEqual(result["precision"]["dps_high"], 40)
        self.assertFalse(
            result["verdict"]["BF6_implies_MFC6_supported"]
        )
        self.assertFalse(
            result["verdict"][
                "MFC6_is_operationally_testable_from_current_definition"
            ]
        )
        for mode in result["numerical"].values():
            records = mode["records"]
            self.assertGreater(
                records[-1]["ordinary_transformed_abs"],
                records[0]["ordinary_transformed_abs"],
            )
            self.assertGreater(
                min(r["two_precision_agreement_digits"] for r in records),
                30,
            )


if __name__ == "__main__":
    unittest.main()
