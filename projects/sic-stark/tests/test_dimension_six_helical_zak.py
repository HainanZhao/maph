#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixHelicalZakTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/dimension_six_helical_zak.py"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_helical_quotient_is_the_valid_compact_quotient(self) -> None:
        self.assertTrue(
            self.result[
                "helical_cyclic_subgroup_is_discrete_and_cocompact"
            ]
        )
        self.assertEqual(self.result["finite_subgroup"], "(Z/6)^2")

    def test_dual_restriction_is_exact(self) -> None:
        self.assertEqual(
            self.result["restricted_character_map"],
            "(xi,n,ell)->(-n,ell) mod 6",
        )
        self.assertTrue(
            all(
                len(record["finite_frequency"]) == 2
                for record in self.result["restriction_records"]
            )
        )

    def test_each_finite_frequency_has_alias_family(self) -> None:
        aliases = self.result["finite_frequency_aliases"]
        self.assertEqual(len(aliases), 36)
        self.assertTrue(
            all(record["finite_alias_count"] == 4 for record in aliases)
        )
        self.assertTrue(
            all(
                record["three_step_alias_translation"]
                == "(alpha,N)->(alpha+Delta,N+6)"
                for record in aliases
            )
        )
        self.assertFalse(
            self.result["single_beta_mode_equals_finite_transform"]
        )


if __name__ == "__main__":
    unittest.main()
